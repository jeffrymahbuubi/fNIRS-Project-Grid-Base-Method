# pylint: disable=missing-module-docstring, missing-function-docstring, too-many-arguments, too-many-locals, trailing-whitespace, line-too-long

import os
import time
import pickle as pk
from typing import Tuple

import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from torch.optim.lr_scheduler import LRScheduler
from sklearn.metrics import confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
import torchmetrics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from .datasets import get_data
from .config import TrainingConfiguration


def calculate_class_weights(train_loader, device, use_sqrt: bool = False) -> torch.Tensor:
    labels = []
    for _, target, *_ in train_loader:
        labels.extend(target.cpu().numpy().tolist())
    labels = np.array(labels)
    weights = compute_class_weight('balanced', classes=np.unique(labels), y=labels)
    if use_sqrt:
        weights = np.sqrt(weights)
        weights = weights / weights.min()
    return torch.tensor(weights, dtype=torch.float).to(device)


def _make_loss_fn(use_class_weights: bool, use_sqrt: bool, train_loader, device, label_smoothing: float = 0.0) -> nn.Module:
    if use_class_weights:
        w = calculate_class_weights(train_loader, device, use_sqrt=use_sqrt)
        print(f"  Class weights: {w.cpu().numpy()} (sqrt={use_sqrt})")
        return nn.CrossEntropyLoss(weight=w, label_smoothing=label_smoothing)
    return nn.CrossEntropyLoss(label_smoothing=label_smoothing)


def train(
    model, train_loader, optimizer, loss_fn, device,
    epoch: int = None, n_epochs: int = None,
    verbose: bool = True, log_freq: int = 10,
    use_amp: bool = False
) -> Tuple[float, float, float]:
    model.train()
    total_loss = 0.0
    acc_m = torchmetrics.Accuracy(task='binary').to(device)
    f1_m = torchmetrics.F1Score(task='binary').to(device)
    total_batches = len(train_loader)
    epoch_str = f"{epoch+1}/{n_epochs}" if (epoch is not None and n_epochs) else "?"
    amp_device = device if isinstance(device, str) else device.type

    for batch_idx, (data, target, *_) in enumerate(train_loader):
        data, target = data.to(device), target.to(device).long()
        optimizer.zero_grad()
        with torch.autocast(device_type=amp_device, dtype=torch.bfloat16, enabled=use_amp):
            logits = model(data)
            loss = loss_fn(logits, target)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
        preds = torch.argmax(logits, dim=-1)
        acc_m.update(preds, target)
        f1_m.update(preds, target)
        cur = batch_idx + 1
        if verbose and (cur % log_freq == 0 or cur == total_batches):
            print(f"  Epoch [{epoch_str}] Step [{cur}/{total_batches}] "
                  f"Loss: {total_loss/cur:.4f} Acc: {acc_m.compute():.4f} "
                  f"F1: {f1_m.compute():.4f}")

    return total_loss / len(train_loader), acc_m.compute().item(), f1_m.compute().item()


def val(
    model, val_loader, loss_fn, device,
    epoch: int = None, n_epochs: int = None,
    verbose: bool = True, use_amp: bool = False
) -> Tuple[float, float, float, float, float, float, np.ndarray, list, list]:
    model.eval()
    total_loss = 0.0
    acc_m = torchmetrics.Accuracy(task='binary').to(device)
    f1_m = torchmetrics.F1Score(task='binary').to(device)
    prec_m = torchmetrics.Precision(task='binary').to(device)
    rec_m = torchmetrics.Recall(task='binary').to(device)
    all_preds, all_labels = [], []
    amp_device = device if isinstance(device, str) else device.type

    with torch.no_grad():
        for data, target, *_ in val_loader:
            data, target = data.to(device), target.to(device).long()
            with torch.autocast(device_type=amp_device, dtype=torch.bfloat16, enabled=use_amp):
                logits = model(data)
                total_loss += loss_fn(logits, target).item()
            preds = torch.argmax(logits, dim=-1)
            acc_m.update(preds, target)
            f1_m.update(preds, target)
            prec_m.update(preds, target)
            rec_m.update(preds, target)
            all_preds.extend(preds.cpu().numpy().tolist())
            all_labels.extend(target.cpu().numpy().tolist())

    avg_loss = total_loss / len(val_loader)
    accuracy = acc_m.compute().item()
    f1 = f1_m.compute().item()
    precision = prec_m.compute().item()
    sensitivity = rec_m.compute().item()
    cm = confusion_matrix(all_labels, all_preds, labels=[0, 1])
    tn, fp_val = (cm[0, 0], cm[0, 1]) if cm.shape == (2, 2) else (0, 0)
    specificity = tn / (tn + fp_val) if (tn + fp_val) > 0 else 0.0

    if verbose:
        epoch_str = f" Epoch [{epoch+1}/{n_epochs}]" if (epoch is not None and n_epochs) else ""
        print(f"Val{epoch_str}: Loss={avg_loss:.4f} Acc={accuracy:.4f} F1={f1:.4f} "
              f"Prec={precision:.4f} Sens={sensitivity:.4f} Spec={specificity:.4f}")

    return avg_loss, accuracy, f1, precision, sensitivity, specificity, cm, all_labels, all_preds


class EarlyStopping:
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


def plot_training_curves(history: dict, save_dir: str, experiment_name: str, best_epoch: int = None):
    os.makedirs(save_dir, exist_ok=True)
    for key, title in [('loss', 'Loss'), ('accuracy', 'Accuracy'), ('f1', 'F1 Score')]:
        train_vals = history.get(f'train_{key}', [])
        val_vals = history.get(f'val_{key}', [])
        if not train_vals:
            continue
        epochs = range(1, len(train_vals) + 1)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(epochs, train_vals, label='Train', color='steelblue')
        ax.plot(epochs, val_vals, label='Val', color='darkorange')
        if best_epoch is not None and best_epoch < len(val_vals):
            ax.axvline(x=best_epoch + 1, color='green', linestyle='--', alpha=0.7,
                       label=f'Best (ep {best_epoch+1})')
            ax.scatter([best_epoch + 1], [val_vals[best_epoch]], color='green', s=80, zorder=5)
        ax.set_xlabel('Epoch')
        ax.set_ylabel(title)
        ax.set_title(f'{title} — {experiment_name}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(os.path.join(save_dir, f"{experiment_name}_{key}.png"), dpi=150, bbox_inches='tight')
        plt.close(fig)


def _plot_confusion_matrix(cm: np.ndarray, save_dir: str, experiment_name: str, best_epoch: int = None):
    os.makedirs(save_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    fig.colorbar(im, ax=ax)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha='center', va='center',
                    color='white' if cm[i, j] > cm.max() / 2 else 'black')
    labels = ['Healthy', 'Anxiety']
    ax.set_xticks([0, 1]); ax.set_xticklabels(labels)
    ax.set_yticks([0, 1]); ax.set_yticklabels(labels)
    ax.set_xlabel('Predicted'); ax.set_ylabel('True')
    title = f'Confusion Matrix — {experiment_name}'
    if best_epoch is not None:
        title += f'\n(Best Epoch: {best_epoch+1})'
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(os.path.join(save_dir, f"{experiment_name}_confusion_matrix.png"), dpi=150, bbox_inches='tight')
    plt.close(fig)


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


def _empty_fold_metrics():
    return {
        "train_loss": [], "train_accuracy": [], "train_f1": [],
        "val_loss": [], "val_accuracy": [], "val_f1": [],
        "accuracies": [], "precisions": [], "sensitivity": [], "specificity": [], "f1_scores": [],
        "conf_matrix": np.zeros((2, 2), dtype=int), "true_labels": [], "pred_labels": []
    }


def _run_fold(model, optimizer, scheduler, train_loader, val_loader, device,
              epochs_count, loss_fn, patience, use_amp: bool = False):
    early_stopper = EarlyStopping(patience=patience)
    best_model_state = None
    best_val_f1 = -1.0
    best_epoch = 0
    history = {k: [] for k in ['train_loss', 'train_accuracy', 'train_f1',
                                'val_loss', 'val_accuracy', 'val_f1']}
    for epoch in range(epochs_count):
        tr_loss, tr_acc, tr_f1 = train(
            model, train_loader, optimizer, loss_fn, device,
            epoch=epoch, n_epochs=epochs_count, use_amp=use_amp
        )
        vl_loss, vl_acc, vl_f1, *_ = val(
            model, val_loader, loss_fn, device,
            epoch=epoch, n_epochs=epochs_count, verbose=False, use_amp=use_amp
        )
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


def _collect_fold_results(model, val_loader, device, loss_fn, best_model_state, fold_metrics, history,
                          use_amp: bool = False):
    if best_model_state is not None:
        model.load_state_dict({k: v.to(device) for k, v in best_model_state.items()})
    _, acc, f1, precision, sensitivity, specificity, cm, true_labels, pred_labels = val(
        model, val_loader, loss_fn, device, verbose=True, use_amp=use_amp
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
    _plot_confusion_matrix(cm, save_dir, f"{model_name}_{suffix}_overall")
    save_metrics(overall, save_dir, f"{model_name}_{suffix}_overall")


def perform_holdout_training(
    data_dir, data_type, test_size, task_name, batch_size, model,
    optimizer_class, optimizer_params, scheduler_class, scheduler_params,
    save_dir, model_name, training_configuration,
    use_class_weights: bool = False, use_sqrt_class_weights: bool = False,
    max_trials=None, train_transform=None, val_transform=None, patience=25, label_smoothing: float = 0.0
):
    device = training_configuration.device
    train_loader, val_loader = get_data(
        root_dir=data_dir, data_type=data_type, task_name=task_name,
        batch_size=batch_size, test_size=test_size, use_stratified_kfold=False,
        max_trials=max_trials, train_transform=train_transform, val_transform=val_transform
    )
    use_amp = training_configuration.use_amp
    loss_fn = _make_loss_fn(use_class_weights, use_sqrt_class_weights, train_loader, device, label_smoothing)
    os.makedirs(save_dir, exist_ok=True)
    best_model_path = os.path.join(save_dir, f"{model_name}.pt")
    optimizer = optimizer_class(model.parameters(), **optimizer_params)
    scheduler = scheduler_class(optimizer, **scheduler_params)
    t_begin = time.time()
    history, best_epoch, best_model_state = _run_fold(
        model, optimizer, scheduler, train_loader, val_loader, device,
        training_configuration.epochs_count, loss_fn, patience, use_amp=use_amp
    )
    print(f"Holdout finished in {time.time()-t_begin:.2f}s. Best epoch: {best_epoch+1}")
    if best_model_state is not None:
        model.load_state_dict({k: v.to(device) for k, v in best_model_state.items()})
        torch.save(model.state_dict(), best_model_path)
    _, final_acc, final_f1, final_prec, final_sens, final_spec, final_cm, final_labels, final_preds = val(
        model, val_loader, loss_fn, device, verbose=True, use_amp=use_amp
    )
    name = f"{model_name}_holdout"
    plot_training_curves(history, save_dir, name, best_epoch)
    _plot_confusion_matrix(final_cm, save_dir, name, best_epoch)
    results = {
        **{k: np.array(v, dtype=np.float32) for k, v in history.items()},
        "best_epoch": best_epoch, "stopped_at_epoch": len(history['train_loss']) - 1,
        "true_labels": final_labels, "pred_labels": final_preds,
        "precision": final_prec, "sensitivity": final_sens, "specificity": final_spec,
        "f1_score": final_f1, "accuracy": final_acc, "conf_matrix": final_cm,
        "best_model_path": best_model_path
    }
    save_metrics(results, save_dir, name)
    return results


def perform_kfold_training(
    data_dir, data_type, test_size, task_name, batch_size, k_folds, model,
    optimizer_class, optimizer_params, scheduler_class, scheduler_params,
    save_dir, model_name, training_configuration,
    use_class_weights: bool = False, use_sqrt_class_weights: bool = False,
    max_trials=None, train_transform=None, val_transform=None, patience=25, label_smoothing: float = 0.0,
    splits_json: str = None
):
    device = training_configuration.device
    fold_data = get_data(
        root_dir=data_dir, data_type=data_type, task_name=task_name,
        batch_size=batch_size, test_size=test_size, k_folds=k_folds,
        use_stratified_kfold=True, max_trials=max_trials,
        train_transform=train_transform, val_transform=val_transform,
        splits_json=splits_json
    )
    use_amp = training_configuration.use_amp
    os.makedirs(save_dir, exist_ok=True)
    fold_metrics = _empty_fold_metrics()
    for fold_idx, (train_loader, val_loader) in enumerate(fold_data):
        print(f"\nStarting Fold {fold_idx+1}/{k_folds}")
        start_time = time.time()
        loss_fn = _make_loss_fn(use_class_weights, use_sqrt_class_weights, train_loader, device, label_smoothing)
        _reset_model(model)
        optimizer = optimizer_class(model.parameters(), **optimizer_params)
        scheduler = scheduler_class(optimizer, **scheduler_params)
        history, best_epoch, best_model_state = _run_fold(
            model, optimizer, scheduler, train_loader, val_loader, device,
            training_configuration.epochs_count, loss_fn, patience, use_amp=use_amp
        )
        acc, f1, precision, sensitivity, specificity, cm, true_labels, pred_labels = _collect_fold_results(
            model, val_loader, device, loss_fn, best_model_state, fold_metrics, history, use_amp=use_amp
        )
        fold_name = f"{model_name}_fold_{fold_idx+1}"
        torch.save(model.state_dict(), os.path.join(save_dir, f"{fold_name}.pt"))
        plot_training_curves(history, save_dir, fold_name, best_epoch)
        _plot_confusion_matrix(cm, save_dir, fold_name, best_epoch)
        save_metrics({
            **history, "best_epoch": best_epoch,
            "stopped_at_epoch": len(history['train_loss']) - 1,
            "accuracy": acc, "precision": precision, "sensitivity": sensitivity,
            "specificity": specificity, "f1_score": f1,
            "conf_matrix": cm, "true_labels": true_labels, "pred_labels": pred_labels
        }, save_dir, fold_name)
        print(f"Fold {fold_idx+1} finished in {time.time()-start_time:.2f}s.")
    return fold_metrics


def perform_loso_training(
    data_dir, data_type, task_name, batch_size, model,
    optimizer_class, optimizer_params, scheduler_class, scheduler_params,
    save_dir, model_name, training_configuration,
    use_class_weights: bool = False, use_sqrt_class_weights: bool = False,
    max_trials=None, train_transform=None, val_transform=None, patience=25, label_smoothing: float = 0.0
):
    device = training_configuration.device
    fold_data = get_data(
        root_dir=data_dir, data_type=data_type, task_name=task_name,
        batch_size=batch_size, use_loso_cv=True, max_trials=max_trials,
        train_transform=train_transform, val_transform=val_transform
    )
    use_amp = training_configuration.use_amp
    os.makedirs(save_dir, exist_ok=True)
    fold_metrics = _empty_fold_metrics()
    for fold_idx, (train_loader, val_loader, val_subject) in enumerate(fold_data):
        n_folds = len(fold_data)
        print(f"\nLOSO Fold {fold_idx+1}/{n_folds} — Subject: {val_subject}")
        start_time = time.time()
        loss_fn = _make_loss_fn(use_class_weights, use_sqrt_class_weights, train_loader, device, label_smoothing)
        _reset_model(model)
        optimizer = optimizer_class(model.parameters(), **optimizer_params)
        scheduler = scheduler_class(optimizer, **scheduler_params)
        history, best_epoch, best_model_state = _run_fold(
            model, optimizer, scheduler, train_loader, val_loader, device,
            training_configuration.epochs_count, loss_fn, patience, use_amp=use_amp
        )
        acc, f1, precision, sensitivity, specificity, cm, true_labels, pred_labels = _collect_fold_results(
            model, val_loader, device, loss_fn, best_model_state, fold_metrics, history, use_amp=use_amp
        )
        subj_name = f"{model_name}_subject_{val_subject}"
        torch.save(model.state_dict(), os.path.join(save_dir, f"{subj_name}.pt"))
        plot_training_curves(history, save_dir, subj_name, best_epoch)
        _plot_confusion_matrix(cm, save_dir, subj_name, best_epoch)
        save_metrics({
            **history, "best_epoch": best_epoch,
            "stopped_at_epoch": len(history['train_loss']) - 1,
            "accuracy": acc, "precision": precision, "sensitivity": sensitivity,
            "specificity": specificity, "f1_score": f1,
            "conf_matrix": cm, "true_labels": true_labels, "pred_labels": pred_labels
        }, save_dir, subj_name)
        print(f"LOSO fold {fold_idx+1} finished in {time.time()-start_time:.2f}s.")
    return fold_metrics


def main(data_dir: str, save_dir: str, test_size: float, data_type: str,
         model: nn.Module, model_name: str, task_name: str, **kwargs):
    optimizer = kwargs.get('optimizer')
    optimizer_params = kwargs.get('optimizer_params', {})
    scheduler = kwargs.get('scheduler')
    scheduler_params = kwargs.get('scheduler_params', {})
    training_configuration = kwargs.get('training_configuration', TrainingConfiguration())
    use_kfold = kwargs.get('use_kfold', False)
    k_folds = kwargs.get('k_folds', 5)
    use_loso = kwargs.get('use_loso', False)
    use_class_weights = kwargs.get('use_class_weights', False)
    use_sqrt_class_weights = kwargs.get('use_sqrt_class_weights', False)
    max_trials = kwargs.get('max_trials', None)
    train_transform = kwargs.get('train_transform', None)
    val_transform = kwargs.get('val_transform', None)
    patience = kwargs.get('patience', 25)
    label_smoothing = kwargs.get('label_smoothing', 0.0)
    splits_json = kwargs.get('splits_json', None)

    model.to(training_configuration.device)
    os.makedirs(save_dir, exist_ok=True)

    shared = dict(
        data_dir=data_dir, data_type=data_type, task_name=task_name,
        batch_size=training_configuration.batch_size, model=model,
        optimizer_class=optimizer, optimizer_params=optimizer_params,
        scheduler_class=scheduler, scheduler_params=scheduler_params,
        save_dir=save_dir, model_name=model_name,
        training_configuration=training_configuration,
        use_class_weights=use_class_weights,
        use_sqrt_class_weights=use_sqrt_class_weights,
        max_trials=max_trials, train_transform=train_transform,
        val_transform=val_transform, patience=patience,
        label_smoothing=label_smoothing, splits_json=splits_json
    )

    if use_loso:
        fold_metrics = perform_loso_training(**shared)
        _compute_overall_metrics(fold_metrics, save_dir, model_name, "loso")
    elif use_kfold:
        fold_metrics = perform_kfold_training(**shared, test_size=test_size, k_folds=k_folds)
        _compute_overall_metrics(fold_metrics, save_dir, model_name, "kfold")
    else:
        perform_holdout_training(**shared, test_size=test_size)


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
