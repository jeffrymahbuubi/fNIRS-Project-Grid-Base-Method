# pylint: disable=missing-module-docstring, missing-function-docstring, too-many-arguments, too-many-locals, too-many-statements, trailing-whitespace, line-too-long, invalid-name, wrong-import-order, ungrouped-imports

import os
import time
import pickle as pk
from typing import Tuple, List

import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from torch.optim.lr_scheduler import LRScheduler
from sklearn.metrics import confusion_matrix
import torchmetrics

from .datasets import get_data
from .config import TrainingConfiguration, SystemConfig, setup_system


#############################################################
#################### TRAINING PIPELINE ######################
#############################################################

def train_single_task(train_config, model, optimizer, train_loader, epoch_idx, loss_fn
                     ) -> Tuple[float, float, float]:
    model.train()
    total_loss = 0.0
    acc_metric = torchmetrics.Accuracy(task='binary').to(train_config.device)
    f1_metric = torchmetrics.F1Score(task='binary').to(train_config.device)

    # Flooding regularization — disabled; high floor values suppress early learning.
    # Ishida et al. (2020): loss = |loss - b| + b keeps training loss near floor b.
    # flooding_levels = [0.45, 0.40, 0.35]
    # flooding_level = (flooding_levels[0] if epoch_idx < 30
    #                   else flooding_levels[1] if epoch_idx < 50
    #                   else flooding_levels[2])

    for batch_idx, (data, target, _) in enumerate(train_loader):
        data, target = data.to(train_config.device), target.to(train_config.device)
        optimizer.zero_grad()
        output = model(data)
        loss = loss_fn(output, target)
        # loss = (loss - flooding_level).abs() + flooding_level
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        pred = torch.sigmoid(output).round().long().squeeze(1)
        acc_metric.update(pred, target.long())
        f1_metric.update(pred, target.long())
        if batch_idx % train_config.log_interval == 0:
            print(f'Train Epoch: {epoch_idx} Batch: {batch_idx} '
                  f'Loss: {total_loss/(batch_idx+1):.6f} '
                  f'Acc: {acc_metric.compute().item():.4f} '
                  f'F1: {f1_metric.compute().item():.4f}')
    return total_loss / len(train_loader), acc_metric.compute().item(), f1_metric.compute().item()


def val_single_task(train_config, model, val_loader, loss_fn
                   ) -> Tuple[float, float, float, float, float, float, np.ndarray, list, list]:
    model.eval()
    total_loss = 0.0
    acc_metric = torchmetrics.Accuracy(task='binary').to(train_config.device)
    f1_metric = torchmetrics.F1Score(task='binary').to(train_config.device)
    prec_metric = torchmetrics.Precision(task='binary').to(train_config.device)
    rec_metric = torchmetrics.Recall(task='binary').to(train_config.device)
    all_preds, all_labels = [], []

    with torch.no_grad():
        for data, target, _ in val_loader:
            data, target = data.to(train_config.device), target.to(train_config.device)
            output = model(data)
            total_loss += loss_fn(output, target).item()
            pred = torch.sigmoid(output).round().long().squeeze(1)
            target_long = target.long()
            acc_metric.update(pred, target_long)
            f1_metric.update(pred, target_long)
            prec_metric.update(pred, target_long)
            rec_metric.update(pred, target_long)
            all_preds.extend(pred.cpu().numpy().tolist())
            all_labels.extend(target_long.cpu().numpy().tolist())

    avg_loss = total_loss / len(val_loader)
    accuracy = acc_metric.compute().item()
    f1 = f1_metric.compute().item()
    precision = prec_metric.compute().item()
    sensitivity = rec_metric.compute().item()
    cm = confusion_matrix(all_labels, all_preds, labels=[0, 1])
    tn = cm[0, 0] if cm.shape == (2, 2) else 0
    fp_val = cm[0, 1] if cm.shape == (2, 2) else 0
    specificity = tn / (tn + fp_val) if (tn + fp_val) > 0 else 0.0
    return avg_loss, accuracy, f1, precision, sensitivity, specificity, cm, all_labels, all_preds


def train(train_config, model, optimizer, train_loader, epoch_idx, loss_fn):
    return train_single_task(train_config, model, optimizer, train_loader, epoch_idx, loss_fn)


def val(train_config, model, val_loader, loss_fn):
    return val_single_task(train_config, model, val_loader, loss_fn)


#############################################################
###################### EARLY STOPPING #######################
#############################################################

class EarlyStopping:
    """Stops training when val_f1 fails to improve for `patience` epochs."""
    def __init__(self, patience: int = 10, min_delta: float = 0.0001, verbose: bool = True):
        self.patience = patience
        self.min_delta = min_delta
        self.verbose = verbose
        self.counter = 0
        self.best_score = None
        self.early_stop = False
        self.best_epoch = 0

    def __call__(self, score: float, epoch: int) -> bool:
        if self.best_score is None or score > self.best_score + self.min_delta:
            self.best_score = score
            self.best_epoch = epoch
            self.counter = 0
        else:
            self.counter += 1
            if self.verbose:
                print(f"  EarlyStopping: {self.counter}/{self.patience} no F1 improvement")
        if self.counter >= self.patience:
            if self.verbose:
                print(f"  EarlyStopping triggered at epoch {epoch+1}. "
                      f"Best val_f1={self.best_score:.4f} at epoch {self.best_epoch+1}")
            self.early_stop = True
        return self.early_stop


#############################################################
###################### MAIN PIPELINE ########################
#############################################################

def save_metrics(results, save_dir, name):
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, f"{name}.pkl"), "wb") as f:
        pk.dump(results, f)


def _reset_model(model):
    model.apply(lambda m: m.reset_parameters() if hasattr(m, 'reset_parameters') else None)
    for module in model.modules():
        if isinstance(module, nn.BatchNorm3d):
            module.running_mean.zero_()
            module.running_var.fill_(1.0)


def _run_fold(model, optimizer, scheduler, train_loader, val_loader,
              training_configuration, loss_fn, patience):
    early_stopper = EarlyStopping(patience=patience)
    best_model_state = None
    best_val_f1 = -1.0
    best_epoch = 0
    history = {k: [] for k in ['train_loss', 'train_accuracy', 'train_f1',
                                'val_loss', 'val_accuracy', 'val_f1']}
    for epoch in range(training_configuration.epochs_count):
        tr_loss, tr_acc, tr_f1 = train(
            training_configuration, model, optimizer, train_loader, epoch, loss_fn
        )
        vl_loss, vl_acc, vl_f1, *_ = val(training_configuration, model, val_loader, loss_fn)
        history['train_loss'].append(tr_loss)
        history['train_accuracy'].append(tr_acc)
        history['train_f1'].append(tr_f1)
        history['val_loss'].append(vl_loss)
        history['val_accuracy'].append(vl_acc)
        history['val_f1'].append(vl_f1)
        print(f"Epoch {epoch+1}: TR L={tr_loss:.4f} Acc={tr_acc:.4f} F1={tr_f1:.4f} | "
              f"VL L={vl_loss:.4f} Acc={vl_acc:.4f} F1={vl_f1:.4f}")
        if vl_f1 > best_val_f1:
            best_val_f1 = vl_f1
            best_epoch = epoch
            best_model_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
        if early_stopper(vl_f1, epoch):
            print(f"Early stopping at epoch {epoch+1}")
            break
        if scheduler:
            scheduler.step()
    return history, best_epoch, best_model_state


def _collect_fold_results(model, val_loader, training_configuration, loss_fn,
                          best_model_state, fold_metrics, history):
    if best_model_state is not None:
        model.load_state_dict({k: v.to(training_configuration.device)
                               for k, v in best_model_state.items()})
    _, acc, f1, precision, sensitivity, specificity, cm, true_labels, pred_labels = val(
        training_configuration, model, val_loader, loss_fn
    )
    for key in ['train_loss', 'train_accuracy', 'train_f1', 'val_loss', 'val_accuracy', 'val_f1']:
        fold_metrics[key].append(history[key])
    fold_metrics["accuracies"].append(acc)
    fold_metrics["precisions"].append(precision)
    fold_metrics["sensitivity"].append(sensitivity)
    fold_metrics["specificity"].append(specificity)
    fold_metrics["f1_scores"].append(f1)
    fold_metrics["conf_matrix"] += cm
    fold_metrics["true_labels"].extend(true_labels)
    fold_metrics["pred_labels"].extend(pred_labels)
    return acc, f1, precision, sensitivity, specificity, cm, true_labels, pred_labels


def _empty_fold_metrics():
    return {
        "train_loss": [], "train_accuracy": [], "train_f1": [],
        "val_loss": [], "val_accuracy": [], "val_f1": [],
        "accuracies": [], "precisions": [], "sensitivity": [], "specificity": [], "f1_scores": [],
        "conf_matrix": np.zeros((2, 2), dtype=int), "true_labels": [], "pred_labels": []
    }


def perform_holdout_training(data_dir, data_type, test_size, task_types, batch_size, model,
                             optimizer_class, optimizer_params, scheduler_class, scheduler_params,
                             save_dir, model_name, training_configuration, loss_fn, max_trials,
                             train_transform, val_transform, patience=25):
    train_loader, val_loader = get_data(
        root_dir=data_dir, data_type=data_type, task_types=task_types,
        batch_size=batch_size, test_size=test_size, use_stratified_kfold=False,
        max_trials=max_trials, train_transform=train_transform, val_transform=val_transform
    )
    os.makedirs(save_dir, exist_ok=True)
    best_model_path = os.path.join(save_dir, f"{model_name}.pt")
    optimizer = optimizer_class(model.parameters(), **optimizer_params)
    scheduler = scheduler_class(optimizer, **scheduler_params)
    early_stopper = EarlyStopping(patience=patience)
    best_model_state = None
    best_val_f1 = -1.0
    best_epoch = 0
    history = {k: [] for k in ['train_loss', 'train_accuracy', 'train_f1',
                                'val_loss', 'val_accuracy', 'val_f1']}
    t_begin = time.time()
    for epoch in range(training_configuration.epochs_count):
        tr_loss, tr_acc, tr_f1 = train(
            training_configuration, model, optimizer, train_loader, epoch, loss_fn
        )
        elapsed = time.time() - t_begin
        speed_epoch = elapsed / (epoch + 1)
        eta = speed_epoch * training_configuration.epochs_count - elapsed
        print(f"Elapsed {elapsed:.2f}s, {speed_epoch:.2f} s/epoch, eta {eta:.2f}s")
        vl_loss, vl_acc, vl_f1, *_ = val(training_configuration, model, val_loader, loss_fn)
        history['train_loss'].append(tr_loss)
        history['train_accuracy'].append(tr_acc)
        history['train_f1'].append(tr_f1)
        history['val_loss'].append(vl_loss)
        history['val_accuracy'].append(vl_acc)
        history['val_f1'].append(vl_f1)
        print(f"Epoch {epoch+1}: TR L={tr_loss:.4f} Acc={tr_acc:.4f} F1={tr_f1:.4f} | "
              f"VL L={vl_loss:.4f} Acc={vl_acc:.4f} F1={vl_f1:.4f}")
        if vl_f1 > best_val_f1:
            best_val_f1 = vl_f1
            best_epoch = epoch
            best_model_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            torch.save(model.state_dict(), best_model_path)
            print(f"  New best model (val_f1={vl_f1:.4f}) saved.")
        if early_stopper(vl_f1, epoch):
            print(f"Early stopping at epoch {epoch+1}")
            break
        if scheduler:
            scheduler.step()
    if best_model_state is not None:
        model.load_state_dict({k: v.to(training_configuration.device)
                               for k, v in best_model_state.items()})
    _, final_acc, final_f1, final_prec, final_sens, final_spec, final_cm, final_labels, final_preds = val(
        training_configuration, model, val_loader, loss_fn
    )
    return {
        **{k: np.array(v, dtype=np.float32) for k, v in history.items()},
        "best_epoch": best_epoch,
        "stopped_at_epoch": len(history['train_loss']) - 1,
        "true_labels": final_labels,
        "pred_labels": final_preds,
        "precision": final_prec,
        "sensitivity": final_sens,
        "specificity": final_spec,
        "f1_score": final_f1,
        "accuracy": final_acc,
        "conf_matrix": final_cm,
        "best_model_path": best_model_path
    }


def perform_kfold_training(data_dir, data_type, test_size, task_types, batch_size, k_folds, model,
                           optimizer_class, optimizer_params, scheduler_class, scheduler_params,
                           save_dir, model_name, training_configuration, loss_fn,
                           max_trials, train_transform, val_transform, patience=25):
    fold_data = get_data(
        root_dir=data_dir, data_type=data_type, task_types=task_types,
        batch_size=batch_size, test_size=test_size, k_folds=k_folds,
        use_stratified_kfold=True, max_trials=max_trials,
        train_transform=train_transform, val_transform=val_transform
    )
    os.makedirs(save_dir, exist_ok=True)
    fold_metrics = _empty_fold_metrics()
    for fold_idx, (train_loader, val_loader) in enumerate(fold_data):
        print(f"\nStarting Fold {fold_idx+1}/{k_folds}")
        start_time = time.time()
        _reset_model(model)
        optimizer = optimizer_class(model.parameters(), **optimizer_params)
        scheduler = scheduler_class(optimizer, **scheduler_params)
        history, best_epoch, best_model_state = _run_fold(
            model, optimizer, scheduler, train_loader, val_loader,
            training_configuration, loss_fn, patience
        )
        acc, f1, precision, sensitivity, specificity, cm, true_labels, pred_labels = _collect_fold_results(
            model, val_loader, training_configuration, loss_fn, best_model_state, fold_metrics, history
        )
        torch.save(model.state_dict(), os.path.join(save_dir, f"{model_name}_fold_{fold_idx+1}.pt"))
        save_metrics({
            **history, "best_epoch": best_epoch,
            "stopped_at_epoch": len(history['train_loss']) - 1,
            "accuracy": acc, "precision": precision, "sensitivity": sensitivity,
            "specificity": specificity, "f1_score": f1,
            "conf_matrix": cm, "true_labels": true_labels, "pred_labels": pred_labels
        }, save_dir, f"{model_name}_fold_{fold_idx+1}")
        print(f"Fold {fold_idx+1} finished in {time.time()-start_time:.2f}s.")
    return fold_metrics


def perform_loso_training(data_dir, data_type, task_types, batch_size, model,
                          optimizer_class, optimizer_params, scheduler_class, scheduler_params,
                          save_dir, model_name, training_configuration, loss_fn,
                          max_trials=None, train_transform=None, val_transform=None, patience=25):
    fold_data = get_data(
        root_dir=data_dir, data_type=data_type, task_types=task_types,
        batch_size=batch_size, use_loso_cv=True, max_trials=max_trials,
        train_transform=train_transform, val_transform=val_transform
    )
    os.makedirs(save_dir, exist_ok=True)
    fold_metrics = _empty_fold_metrics()
    for fold_idx, (train_loader, val_loader, val_subject) in enumerate(fold_data):
        print(f"\nLOSO Fold {fold_idx+1}/{len(fold_data)} — Subject: {val_subject}")
        start_time = time.time()
        _reset_model(model)
        optimizer = optimizer_class(model.parameters(), **optimizer_params)
        scheduler = scheduler_class(optimizer, **scheduler_params)
        history, best_epoch, best_model_state = _run_fold(
            model, optimizer, scheduler, train_loader, val_loader,
            training_configuration, loss_fn, patience
        )
        acc, f1, precision, sensitivity, specificity, cm, true_labels, pred_labels = _collect_fold_results(
            model, val_loader, training_configuration, loss_fn, best_model_state, fold_metrics, history
        )
        torch.save(model.state_dict(), os.path.join(save_dir, f"{model_name}_subject_{val_subject}.pt"))
        save_metrics({
            **history, "best_epoch": best_epoch,
            "stopped_at_epoch": len(history['train_loss']) - 1,
            "accuracy": acc, "precision": precision, "sensitivity": sensitivity,
            "specificity": specificity, "f1_score": f1,
            "conf_matrix": cm, "true_labels": true_labels, "pred_labels": pred_labels
        }, save_dir, f"{model_name}_subject_{val_subject}")
        print(f"LOSO fold {fold_idx+1} finished in {time.time()-start_time:.2f}s.")
    return fold_metrics


def _compute_overall_metrics(fold_metrics, save_dir, model_name, suffix):
    cm = fold_metrics["conf_matrix"]
    tn, fp, fn, tp = cm[0, 0], cm[0, 1], cm[1, 0], cm[1, 1]
    total = int(tn + fp + fn + tp)
    overall = {
        "overall_accuracy": (tp + tn) / total if total > 0 else 0,
        "overall_precision": tp / (tp + fp) if (tp + fp) > 0 else 0,
        "overall_sensitivity": tp / (tp + fn) if (tp + fn) > 0 else 0,
        "overall_specificity": tn / (tn + fp) if (tn + fp) > 0 else 0,
        "overall_f1_score": (2 * tp) / (2 * tp + fp + fn) if (2 * tp + fp + fn) > 0 else 0,
        "confusion_matrix": cm,
        "true_labels": fold_metrics["true_labels"],
        "pred_labels": fold_metrics["pred_labels"]
    }
    save_metrics(overall, save_dir, f"{model_name}_{suffix}_overall")


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
    patience = kwargs.get('patience', 25)

    model.to(training_configuration.device)
    setup_system(SystemConfig)
    os.makedirs(save_dir, exist_ok=True)

    if use_loso:
        fold_metrics = perform_loso_training(
            data_dir, data_type, task_types, training_configuration.batch_size,
            model, optimizer, optimizer_params, scheduler, scheduler_params,
            save_dir, model_name, training_configuration, loss_fn,
            max_trials, train_transform, val_transform, patience
        )
        _compute_overall_metrics(fold_metrics, save_dir, model_name, "loso")
    elif use_kfold:
        fold_metrics = perform_kfold_training(
            data_dir, data_type, test_size, task_types,
            training_configuration.batch_size, k_folds, model, optimizer, optimizer_params,
            scheduler, scheduler_params, save_dir, model_name, training_configuration, loss_fn,
            max_trials, train_transform, val_transform, patience
        )
        _compute_overall_metrics(fold_metrics, save_dir, model_name, "kfold")
    else:
        results = perform_holdout_training(
            data_dir, data_type, test_size, task_types, training_configuration.batch_size,
            model, optimizer, optimizer_params, scheduler, scheduler_params, save_dir, model_name,
            training_configuration, loss_fn, max_trials, train_transform, val_transform, patience
        )
        save_metrics(results, save_dir, f"{model_name}_holdout")


#############################################################
###################### CUSTOM CLASSES #######################
#############################################################

class LabelSmoothing(nn.Module):
    def __init__(self, smoothing=0.1):
        super().__init__()
        self.smoothing = smoothing

    def forward(self, output, target):
        log_probs = F.log_softmax(output, dim=-1)
        if output.size(-1) == 1:
            target = target.float() * (1 - self.smoothing) + 0.5 * self.smoothing
            return F.binary_cross_entropy_with_logits(output.squeeze(), target)
        n_classes = output.size(-1)
        true_dist = torch.zeros_like(log_probs)
        true_dist.fill_(self.smoothing / (n_classes - 1))
        true_dist.scatter_(1, target.data.unsqueeze(1), 1.0 - self.smoothing)
        return torch.mean(torch.sum(-true_dist * log_probs, dim=-1))


class CosineWarmupScheduler(LRScheduler):
    def __init__(self, optimizer, warmup, max_iters):
        self.warmup = warmup
        self.max_num_iters = max_iters
        super().__init__(optimizer)

    def get_lr(self):
        return [base_lr * self.get_lr_factor(self.last_epoch) for base_lr in self.base_lrs]

    def get_lr_factor(self, epoch):
        lr_factor = 0.5 * (1 + np.cos(np.pi * epoch / self.max_num_iters))
        if epoch <= self.warmup:
            lr_factor *= epoch / self.warmup
        return lr_factor
