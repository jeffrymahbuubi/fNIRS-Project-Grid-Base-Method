# pylint: disable=missing-module-docstring, missing-function-docstring, too-many-arguments, too-many-locals, too-many-statements, reimported, trailing-whitespace, line-too-long, invalid-name, wrong-import-order, ungrouped-imports, no-else-return, consider-using-f-string

import os
import time
import pickle as pk
from collections import defaultdict
from typing import Tuple, List, Union

import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from torch.optim.lr_scheduler import _LRScheduler
from sklearn.metrics import confusion_matrix

from src.datasets import get_data
from src.config import TrainingConfiguration, SystemConfig
from src.config import setup_system


#############################################################
#################### TRAINING PIPELINE ######################
#############################################################

def train_single_task(train_config, model, optimizer, train_loader, epoch_idx, loss_fn
                     ) -> Tuple[float, float, List[float]]:
    model.train()
    batch_loss = np.array([])
    batch_acc = np.array([])
    pred_probs = []
    flooding_levels = [0.45, 0.40, 0.35]

    if epoch_idx < 30:
        flooding_level = flooding_levels[0]
    elif epoch_idx < 50:
        flooding_level = flooding_levels[1]
    else:
        flooding_level = flooding_levels[2]

    for batch_idx, (data, target, _) in enumerate(train_loader):
        data, target = data.to(train_config.device), target.to(train_config.device)
        optimizer.zero_grad()
        output = model(data)
        loss = loss_fn(output, target)
        loss = (loss - flooding_level).abs() + flooding_level
        loss.backward()
        optimizer.step()
        batch_loss = np.append(batch_loss, loss.item())
        pred = torch.sigmoid(output)
        pred_probs.extend(pred.detach().cpu().numpy().flatten())
        correct = (pred.round() == target.float().unsqueeze(1)).sum().item()
        acc = correct / len(data)
        batch_acc = np.append(batch_acc, acc)
        if batch_idx % train_config.log_interval == 0:
            print('Train Epoch: {} [Single-task] Batch: {} Loss: {:.6f} Acc: {:.4f}'.format(
                epoch_idx, batch_idx, batch_loss[-1], batch_acc[-1]
            ))
    return batch_loss.mean(), batch_acc.mean(), pred_probs


def train(train_config, model, optimizer, train_loader, epoch_idx, loss_fn
         ) -> Tuple[float, float, List[float]]:
    first_batch = next(iter(train_loader))
    if isinstance(first_batch, list) and len(first_batch) == 3:
        print("Training single-task model...")
        return train_single_task(train_config, model, optimizer, train_loader, epoch_idx, loss_fn)
    else:
        raise ValueError("Unexpected batch structure in data loader.")


def validate_single_task(train_config, model, test_loader, loss_fn
                        ) -> Tuple[float, float, List[int], List[float]]:
    model.eval()
    test_loss = 0
    subject_predictions = defaultdict(list)
    subject_labels = {}

    with torch.no_grad():
        for data, target, subjects in test_loader:
            data, target = data.to(train_config.device), target.to(train_config.device)
            output = model(data)
            loss = loss_fn(output, target)
            test_loss += loss.item()
            pred = torch.sigmoid(output)
            predicted_labels = pred.round().cpu().numpy().flatten()
            for i, subject in enumerate(subjects):
                subject_predictions[subject].append(predicted_labels[i])
                subject_labels[subject] = target[i].item()

    for subject, preds in subject_predictions.items():
        print(f"Subject {subject}: True Label = {subject_labels[subject]}")
        print(f"  Sequence-level Predictions: {preds}\n")

    all_predictions = [pred for preds in subject_predictions.values() for pred in preds]
    all_labels = [subject_labels[subject] for subject in subject_predictions for _ in subject_predictions[subject]]
    correct = sum(1 for i in range(len(all_predictions)) if all_predictions[i] == all_labels[i])
    accuracy = correct / len(all_labels)
    test_loss /= len(test_loader)
    print(f'\nSequence-level Test set: Average loss: {test_loss:.4f}, '
          f'Accuracy: {accuracy:.2%} ({correct}/{len(all_labels)})\n')
    return test_loss, accuracy, all_labels, all_predictions


def validate(train_config, model, test_loader, loss_fn
            ) -> Tuple[float, float, List[int], List[float]]:
    first_batch = next(iter(test_loader))
    if isinstance(first_batch, list) and len(first_batch) == 3:
        print("Validating single-task model...")
        return validate_single_task(train_config, model, test_loader, loss_fn)
    else:
        raise ValueError("Unexpected batch structure in data loader.")


def predict_single_task(model: torch.nn.Module, data_loader: torch.utils.data.DataLoader,
                        device: torch.device, return_metrics=True
                       ) -> Union[
                           Tuple[List[int], float, float, float, float, float, np.ndarray, List[int], List[float]],
                           Tuple[List[int], List[float]]
                       ]:
    model.eval()
    all_predictions = []
    all_labels = []
    with torch.no_grad():
        for data, target, subjects in data_loader:
            data = data.to(device)
            output = model(data)
            pred = torch.sigmoid(output)
            predicted_labels = pred.round().cpu().numpy().flatten()
            all_predictions.extend(predicted_labels)
            all_labels.extend(target.cpu().numpy().flatten())
    if return_metrics:
        conf_matrix = confusion_matrix(all_labels, all_predictions, labels=[0, 1])
        if conf_matrix.size == 4:
            tn, fp, fn, tp = conf_matrix.ravel()
        else:
            tn, fp, fn, tp = conf_matrix[0, 0], 0, 0, conf_matrix[0, 0]
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        f1 = 2 * precision * sensitivity / (precision + sensitivity) if (precision + sensitivity) > 0 else 0
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp + tn + fp + fn) > 0 else 0
        return (all_predictions, precision, sensitivity, specificity, f1, accuracy, conf_matrix,
                all_labels, [np.mean(pred) for pred in all_predictions])
    return all_predictions, [np.mean(pred) for pred in all_predictions]


def predict(model: torch.nn.Module, data_loader: torch.utils.data.DataLoader,
            device: torch.device, return_metrics=True
           ) -> Union[
               Tuple[List[int], float, float, float, float, np.ndarray, List[int], List[float]],
               Tuple[List[int], List[float]]
           ]:
    print("Running single-task prediction...")
    return predict_single_task(model, data_loader, device, return_metrics)


#############################################################
###################### MAIN PIPELINE ########################
#############################################################

def save_best_model(model, fold_idx, best_val_accuracy, save_dir, model_name):
    os.makedirs(save_dir, exist_ok=True)
    best_model_path = os.path.join(save_dir, f"{model_name}_fold_{fold_idx + 1}.pt")
    torch.save(model.state_dict(), best_model_path)
    print(f"New best model for fold {fold_idx + 1} saved with accuracy: {best_val_accuracy:.4f}")


def save_best_model_loso(model, val_subject, best_val_accuracy, save_dir, model_name):
    os.makedirs(save_dir, exist_ok=True)
    best_model_path = os.path.join(save_dir, f"{model_name}_subject_{val_subject}.pt")
    torch.save(model.state_dict(), best_model_path)
    print(f"New best model for subject {val_subject} saved with accuracy: {best_val_accuracy:.4f}")


def save_metrics(results, save_dir, name):
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, f"{name}.pkl")
    with open(save_path, "wb") as file:
        pk.dump(results, file)


def train_and_validate_loso(model, optimizer, train_loader, val_loader, fold_identifier, scheduler,
                            training_configuration, save_dir, model_name, loss_fn):
    best_val_accuracy = 0.0
    train_losses, val_losses = [], []
    train_accuracies, val_accuracies = [], []
    all_train_probs, all_val_probs = [], []
    all_val_labels = []

    for epoch in range(training_configuration.epochs_count):
        train_loss, train_acc, train_probs = train_single_task(
            training_configuration, model, optimizer, train_loader, epoch, loss_fn
        )
        train_losses.append(train_loss)
        train_accuracies.append(train_acc)
        all_train_probs.extend(train_probs)
        val_loss, val_accuracy, val_labels, val_probs = validate_single_task(
            training_configuration, model, val_loader, loss_fn
        )
        val_losses.append(val_loss)
        val_accuracies.append(val_accuracy)
        all_val_labels.extend(val_labels)
        all_val_probs.extend(val_probs)
        print(f"Epoch {epoch + 1} - Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, "
              f"Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.4f}")
        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            save_best_model_loso(model, fold_identifier, best_val_accuracy, save_dir, model_name)
        if scheduler:
            scheduler.step()
    return train_losses, val_losses, train_accuracies, val_accuracies, all_val_labels, all_val_probs


def perform_loso_training(data_dir, data_type, task_types, batch_size, model,
                          optimizer_class, optimizer_params, scheduler_class, scheduler_params,
                          save_dir, model_name, training_configuration, loss_fn,
                          max_trials=None, train_transform=None, val_transform=None):
    fold_data = get_data(
        root_dir=data_dir,
        data_type=data_type,
        task_types=task_types,
        batch_size=batch_size,
        use_loso_cv=True,
        max_trials=max_trials,
        train_transform=train_transform,
        val_transform=val_transform
    )
    fold_metrics = {
        "train_loss": [], "val_loss": [], "train_accuracy": [], "val_accuracy": [],
        "accuracies": [], "precisions": [], "sensitivity": [], "specificity": [], "f1_scores": [],
        "conf_matrix": np.zeros((2, 2), dtype=int),
        "true_labels": [], "pred_probs": []
    }

    for fold_idx, (train_loader, val_loader, val_subject) in enumerate(fold_data):
        fold_identifier = val_subject
        print(f"Starting LOSO Fold {fold_idx + 1}/{len(fold_data)} with Validation Subject: {fold_identifier}")
        start_time = time.time()  # Start timing for this fold
        
        model.apply(lambda m: m.reset_parameters() if hasattr(m, 'reset_parameters') else None)
        for module in model.modules():
            if isinstance(module, nn.BatchNorm3d):
                module.running_mean = torch.zeros_like(module.running_mean)
                module.running_var = torch.ones_like(module.running_var)
        optimizer = optimizer_class(model.parameters(), **optimizer_params)
        scheduler = scheduler_class(optimizer, **scheduler_params)
        (train_losses, val_losses, train_accuracies, val_accuracies,
         val_labels, val_probs) = train_and_validate_loso(
            model, optimizer, train_loader, val_loader, fold_identifier, scheduler,
            training_configuration, save_dir, model_name, loss_fn
        )
        fold_metrics["train_loss"].append(train_losses)
        fold_metrics["val_loss"].append(val_losses)
        fold_metrics["train_accuracy"].append(train_accuracies)
        fold_metrics["val_accuracy"].append(val_accuracies)
        (_, precision, sensitivity, specificity, f1, accuracy, conf_matrix,
         true_labels, pred_probs) = predict(model, val_loader, training_configuration.device, return_metrics=True)
        fold_metrics["accuracies"].append(accuracy)
        fold_metrics["precisions"].append(precision)
        fold_metrics["sensitivity"].append(sensitivity)
        fold_metrics["specificity"].append(specificity)
        fold_metrics["f1_scores"].append(f1)
        fold_metrics["conf_matrix"] += conf_matrix
        fold_metrics["true_labels"].extend(true_labels)
        fold_metrics["pred_probs"].extend(pred_probs)
        save_metrics({
            "train_loss": train_losses,
            "val_loss": val_losses,
            "train_accuracy": train_accuracies,
            "val_accuracy": val_accuracies,
            "accuracy": accuracy,
            "precision": precision,
            "sensitivity": sensitivity,
            "specificity": specificity,
            "f1_score": f1,
            "conf_matrix": conf_matrix,
            "true_labels": true_labels,
            "pred_probs": pred_probs
        }, save_dir, f"{model_name}_subject_{fold_identifier}")
        
        elapsed_time = time.time() - start_time  # Calculate the elapsed time for the fold
        print(f"Fold {fold_idx + 1} finished in {elapsed_time:.2f} seconds.")
    return fold_metrics


def train_and_validate(model, optimizer, train_loader, val_loader, fold_idx, scheduler,
                       training_configuration, save_dir, model_name, loss_fn):
    best_val_accuracy = 0.0
    train_losses, val_losses = [], []
    train_accuracies, val_accuracies = [], []
    all_train_probs, all_val_probs = [], []
    all_val_labels = []
    for epoch in range(training_configuration.epochs_count):
        train_loss, train_acc, train_probs = train_single_task(
            training_configuration, model, optimizer, train_loader, epoch, loss_fn
        )
        train_losses.append(train_loss)
        train_accuracies.append(train_acc)
        all_train_probs.extend(train_probs)
        val_loss, val_accuracy, val_labels, val_probs = validate_single_task(
            training_configuration, model, val_loader, loss_fn
        )
        val_losses.append(val_loss)
        val_accuracies.append(val_accuracy)
        all_val_labels.extend(val_labels)
        all_val_probs.extend(val_probs)
        print(f"Epoch {epoch + 1} - Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}, "
              f"Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.4f}")
        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            if fold_idx is not None:
                save_best_model(model, fold_idx, best_val_accuracy, save_dir, model_name)
        if scheduler:
            scheduler.step()
    return train_losses, val_losses, train_accuracies, val_accuracies, all_val_labels, all_val_probs


def perform_kfold_training(data_dir, data_type, test_size, task_types, batch_size, k_folds, model,
                           optimizer_class, optimizer_params, scheduler_class, scheduler_params,
                           save_dir, model_name, training_configuration, loss_fn,
                           max_trials, train_transform, val_transform):
    fold_data = get_data(
        root_dir=data_dir,
        data_type=data_type,
        task_types=task_types,
        batch_size=batch_size,
        test_size=test_size,
        k_folds=k_folds,
        use_stratified_kfold=True,
        max_trials=max_trials,
        train_transform=train_transform,
        val_transform=val_transform
    )
    fold_metrics = {
        "train_loss": [], "val_loss": [], "train_accuracy": [], "val_accuracy": [],
        "accuracies": [], "precisions": [], "sensitivity": [], "specificity": [], "f1_scores": [],
        "conf_matrix": np.zeros((2, 2), dtype=int),
        "true_labels": [], "pred_probs": []
    }
    for fold_idx, (train_loader, val_loader) in enumerate(fold_data):
        print(f"Starting Fold {fold_idx + 1}/{k_folds}")
        start_time = time.time()  # Start timing for this fold
        model.apply(lambda m: m.reset_parameters() if hasattr(m, 'reset_parameters') else None)
        for module in model.modules():
            if isinstance(module, nn.BatchNorm3d):
                module.running_mean = torch.zeros_like(module.running_mean)
                module.running_var = torch.ones_like(module.running_var)
        optimizer = optimizer_class(model.parameters(), **optimizer_params)
        scheduler = scheduler_class(optimizer, **scheduler_params)
        (train_losses, val_losses, train_accuracies, val_accuracies,
         val_labels, val_probs) = train_and_validate(
            model, optimizer, train_loader, val_loader, fold_idx, scheduler, training_configuration, save_dir, 
            model_name, loss_fn
        )
        fold_metrics["train_loss"].append(train_losses)
        fold_metrics["val_loss"].append(val_losses)
        fold_metrics["train_accuracy"].append(train_accuracies)
        fold_metrics["val_accuracy"].append(val_accuracies)
        (_, precision, sensitivity, specificity, f1, accuracy, conf_matrix,
         true_labels, pred_probs) = predict(model, val_loader, training_configuration.device, return_metrics=True)
        fold_metrics["accuracies"].append(accuracy)
        fold_metrics["precisions"].append(precision)
        fold_metrics["sensitivity"].append(sensitivity)
        fold_metrics["specificity"].append(specificity)
        fold_metrics["f1_scores"].append(f1)
        fold_metrics["conf_matrix"] += conf_matrix
        fold_metrics["true_labels"].extend(true_labels)
        fold_metrics["pred_probs"].extend(pred_probs)
        save_metrics({
            "train_loss": train_losses,
            "val_loss": val_losses,
            "train_accuracy": train_accuracies,
            "val_accuracy": val_accuracies,
            "accuracy": accuracy,
            "precision": precision,
            "sensitivity": sensitivity,
            "specificity": specificity,
            "f1_score": f1,
            "conf_matrix": conf_matrix,
            "true_labels": true_labels,
            "pred_probs": pred_probs
        }, save_dir, f"{model_name}_fold_{fold_idx + 1}")

        elapsed_time = time.time() - start_time  # Calculate the elapsed time for the fold
        print(f"Fold {fold_idx + 1} finished in {elapsed_time:.2f} seconds.")
    return fold_metrics


def perform_holdout_training(data_dir, data_type, test_size, task_types, batch_size, model,
                             optimizer_class, optimizer_params, scheduler_class, scheduler_params,
                             save_dir, model_name, training_configuration, loss_fn, max_trials,
                             train_transform, val_transform):
    train_loader, val_loader = get_data(
        root_dir=data_dir,
        data_type=data_type,
        task_types=task_types,
        batch_size=batch_size,
        test_size=test_size,
        use_stratified_kfold=False,
        max_trials=max_trials,
        train_transform=train_transform,
        val_transform=val_transform
    )
    best_loss = float("inf")
    epoch_train_loss, epoch_test_loss = [], []
    epoch_train_acc, epoch_test_acc = [], []
    all_val_labels, all_val_probs = [], []
    optimizer = optimizer_class(model.parameters(), **optimizer_params)
    scheduler = scheduler_class(optimizer, **scheduler_params)
    t_begin = time.time()
    for epoch in range(training_configuration.epochs_count):
        train_loss, train_acc, _ = train(training_configuration, model, optimizer, train_loader, epoch, loss_fn)
        epoch_train_loss.append(train_loss)
        epoch_train_acc.append(train_acc)
        elapsed_time = time.time() - t_begin
        speed_epoch = elapsed_time / (epoch + 1)
        speed_batch = speed_epoch / len(train_loader)
        eta = speed_epoch * training_configuration.epochs_count - elapsed_time
        print("Elapsed {:.2f}s, {:.2f} s/epoch, {:.2f} s/batch, eta {:.2f}s".format(
            elapsed_time, speed_epoch, speed_batch, eta
        ))
        if (epoch + 1) % training_configuration.test_interval == 0:
            val_loss, val_accuracy, val_labels, val_probs = validate(training_configuration, model, val_loader, loss_fn)
            epoch_test_loss.append(val_loss)
            epoch_test_acc.append(val_accuracy)
            all_val_labels.extend(val_labels)
            all_val_probs.extend(val_probs)
            if val_loss < best_loss:
                best_loss = val_loss
                best_model_path = os.path.join(save_dir, f"{model_name}.pt")
                torch.save(model.state_dict(), best_model_path)
                print(f"New best model saved with validation loss: {best_loss:.4f}")
        if scheduler:
            scheduler.step()
    (_, precision, sensitivity, specificity, f1, accuracy, conf_matrix,
     true_labels, pred_probs) = predict(model, val_loader, training_configuration.device, return_metrics=True)
    return {
        "train_loss": np.array(epoch_train_loss, dtype=np.float32),
        "train_accuracy": np.array(epoch_train_acc, dtype=np.float32),
        "val_loss": np.array(epoch_test_loss, dtype=np.float32),
        "val_accuracy": np.array(epoch_test_acc, dtype=np.float32),
        "true_labels": true_labels,
        "pred_probs": pred_probs,
        "precision": precision,
        "sensitivity": sensitivity,
        "specificity": specificity,
        "f1_score": f1,
        "accuracy": accuracy,
        "conf_matrix": conf_matrix,
        "best_model_path": best_model_path
    }


def main(data_dir: str, save_dir: str, test_size: float, data_type: str, 
         model: nn.Module, model_name: str, task_types: dict, **kwargs):
    optimizer = kwargs.get('optimizer')
    optimizer_params = kwargs.get('optimizer_params', {})
    scheduler = kwargs.get('scheduler')
    scheduler_params = kwargs.get('scheduler_params', {})
    training_configuration = kwargs.get('training_configuration', TrainingConfiguration())
    use_kfold = kwargs.get('use_kfold', False)
    k_folds = kwargs.get('k_folds', 5)
    use_loso = kwargs.get('use_loso', False)
    loss_fn = kwargs.get('loss_fn')
    max_trials = kwargs.get('max_trials', None)
    train_transform = kwargs.get('train_transform', None)
    val_transform = kwargs.get('val_transform', None)

    model.to(training_configuration.device)
    setup_system(SystemConfig)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if use_loso:
        fold_metrics = perform_loso_training(
            data_dir, data_type, task_types, training_configuration.batch_size, 
            model, optimizer, optimizer_params, scheduler, scheduler_params, 
            save_dir, model_name, training_configuration, loss_fn, 
            max_trials, train_transform, val_transform
        )
        avg_train_loss = np.mean(fold_metrics["train_loss"], axis=0).tolist()
        avg_val_loss = np.mean(fold_metrics["val_loss"], axis=0).tolist()
        avg_train_accuracy = np.mean(fold_metrics["train_accuracy"], axis=0).tolist()
        avg_val_accuracy = np.mean(fold_metrics["val_accuracy"], axis=0).tolist()
        cm = fold_metrics["conf_matrix"]
        tn, fp, fn, tp = cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]
        total = tn + fp + fn + tp
        overall_accuracy = (tp + tn) / total if total > 0 else 0
        overall_sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        overall_specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        overall_precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        overall_f1_score = (2 * tp) / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0
        overall_metrics = {
            "overall_accuracy": overall_accuracy,
            "overall_precision": overall_precision,
            "overall_sensitivity": overall_sensitivity,
            "overall_specificity": overall_specificity,
            "overall_f1_score": overall_f1_score,
            "confusion_matrix": cm,
            "avg_train_loss": avg_train_loss,
            "avg_val_loss": avg_val_loss,
            "avg_train_accuracy": avg_train_accuracy,
            "avg_val_accuracy": avg_val_accuracy,
            "true_labels": fold_metrics["true_labels"],
            "pred_probs": fold_metrics["pred_probs"]
        }
        save_metrics(overall_metrics, save_dir, f"{model_name}_loso_overall")
    elif use_kfold:
        fold_metrics = perform_kfold_training(
            data_dir, data_type, test_size, task_types, 
            training_configuration.batch_size, k_folds, model, optimizer, optimizer_params, scheduler, 
            scheduler_params, save_dir, model_name, training_configuration, loss_fn, max_trials, 
            train_transform, val_transform
        )
        avg_train_loss = np.mean(fold_metrics["train_loss"], axis=0).tolist()
        avg_val_loss = np.mean(fold_metrics["val_loss"], axis=0).tolist()
        avg_train_accuracy = np.mean(fold_metrics["train_accuracy"], axis=0).tolist()
        avg_val_accuracy = np.mean(fold_metrics["val_accuracy"], axis=0).tolist()
        cm = fold_metrics["conf_matrix"]
        tn, fp, fn, tp = cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]
        total = tn + fp + fn + tp
        overall_accuracy = (tp + tn) / total if total > 0 else 0
        overall_sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
        overall_specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
        overall_precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        overall_f1_score = (2 * tp) / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0
        overall_metrics = {
            "overall_accuracy": overall_accuracy,
            "overall_precision": overall_precision,
            "overall_sensitivity": overall_sensitivity,
            "overall_specificity": overall_specificity,
            "overall_f1_score": overall_f1_score,
            "confusion_matrix": cm,
            "avg_train_loss": avg_train_loss,
            "avg_val_loss": avg_val_loss,
            "avg_train_accuracy": avg_train_accuracy,
            "avg_val_accuracy": avg_val_accuracy,
            "true_labels": fold_metrics["true_labels"],
            "pred_probs": fold_metrics["pred_probs"]
        }
        save_metrics(overall_metrics, save_dir, f"{model_name}_kfold_overall")
    else:
        results = perform_holdout_training(
            data_dir, data_type, test_size, task_types, training_configuration.batch_size, 
            model, optimizer, optimizer_params, scheduler, scheduler_params, save_dir, model_name, 
            training_configuration, loss_fn, max_trials, train_transform, val_transform
        )
        save_metrics(results, save_dir, f"{model_name}_holdout")

#############################################################
###################### CUSTOM PIPELINE ######################
#############################################################

## Custom Loss Function & Scheduler Defenition
class LabelSmoothing(nn.Module):
    """Label Smoothing Loss, supports binary and multi-class classification."""
    def __init__(self, smoothing=0.1):
        super(LabelSmoothing, self).__init__()
        self.smoothing = smoothing

    def forward(self, output, target):
        # Apply log_softmax on the output to get log-probabilities
        log_probs = F.log_softmax(output, dim=-1)
        
        if output.size(-1) == 1:  # Binary classification case
            # Smooth the binary target to be between 0 and 1
            target = target.float() * (1 - self.smoothing) + 0.5 * self.smoothing
            return F.binary_cross_entropy_with_logits(output.squeeze(), target)
        else:
            # Multi-class case
            n_classes = output.size(-1)
            true_dist = torch.zeros_like(log_probs)
            true_dist.fill_(self.smoothing / (n_classes - 1))
            true_dist.scatter_(1, target.data.unsqueeze(1), 1.0 - self.smoothing)
            return torch.mean(torch.sum(-true_dist * log_probs, dim=-1))

class CosineWarmupScheduler(_LRScheduler):
    def __init__(self, optimizer, warmup, max_iters):
        self.warmup = warmup
        self.max_num_iters = max_iters
        super().__init__(optimizer)
        
    def get_lr(self):
        lr_factor = self.get_lr_factor(epoch=self.last_epoch)
        return [base_lr * lr_factor for base_lr in self.base_lrs]
    
    def get_lr_factor(self, epoch):
        lr_factor = 0.5 * (1 + np.cos(np.pi * epoch / self.max_num_iters))
        if epoch <= self.warmup:
            lr_factor *= epoch / self.warmup
        return lr_factor