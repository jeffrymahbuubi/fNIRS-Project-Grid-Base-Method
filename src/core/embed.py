import json
import os
from typing import Dict

import numpy as np
import torch
from torchvision.transforms.v2 import Compose, UniformTemporalSubsample, Resize

from .models import ViT
from .datasets import (
    FNIRSSequenceDatasetV2,
    TransformWrapper,
    RearrangeToTCHW,
    RearrangeBackToCTHW,
    ConvertToRGB,
)

# Matches the hardcoded config in src/core/main.py
_VIT_CONFIG = dict(
    image_size=(128, 128),
    image_patch_size=(8, 8),
    frames=256,
    frame_patch_size=16,
    num_classes=2,
    dim=64,
    depth=6,
    heads=8,
    mlp_dim=512,
    channels=3,
)

_MAX_TRIALS = 4  # consistent with training


def build_model() -> ViT:
    return ViT(**_VIT_CONFIG)


def load_checkpoint(model: ViT, checkpoint_path: str, device: str = 'cpu') -> ViT:
    state_dict = torch.load(checkpoint_path, map_location=device, weights_only=True)
    model.load_state_dict(state_dict)
    model.eval()
    return model


def get_val_transform() -> Compose:
    return Compose([
        RearrangeToTCHW(),
        UniformTemporalSubsample(num_samples=256),
        Resize((128, 128)),
        RearrangeBackToCTHW(),
        ConvertToRGB(),
    ])


def extract_cls_embeddings(
    model: ViT,
    dataset: FNIRSSequenceDatasetV2,
    subject_set: set,
    device: str = 'cpu',
    batch_size: int = 8,
) -> Dict[str, np.ndarray]:
    """Run inference for subjects in subject_set, return {subject: mean CLS embedding}.

    Hooks the Transformer block output to capture the CLS token (index 0, shape dim=64).
    Each subject's embedding is averaged across all their trials.
    """
    from torch.utils.data import Subset, DataLoader

    val_transform = get_val_transform()
    indices = [i for i, s in enumerate(dataset.subjects) if s in subject_set]
    if not indices:
        return {}

    subset = TransformWrapper(Subset(dataset, indices), val_transform)
    loader = DataLoader(subset, batch_size=batch_size, shuffle=False, num_workers=0)

    captured = {}

    def _cls_hook(module, input, output):
        captured['cls'] = output[:, 0].detach().cpu()  # (batch, dim)

    handle = model.transformer.register_forward_hook(_cls_hook)
    model.to(device)
    model.eval()

    subject_embeddings: Dict[str, list] = {}

    with torch.no_grad():
        for data, _label, subject_batch in loader:
            data = data.to(device)
            _ = model(data)
            emb_batch = captured['cls'].numpy()
            for emb, subj in zip(emb_batch, subject_batch):
                if subj not in subject_embeddings:
                    subject_embeddings[subj] = []
                subject_embeddings[subj].append(emb)

    handle.remove()
    return {s: np.mean(embs, axis=0) for s, embs in subject_embeddings.items()}


def extract_kfold_embeddings(
    checkpoint_dir: str,
    task: str,
    data_dir: str,
    splits_json: str,
    data_type: str = 'hbt',
    device: str = 'cpu',
    batch_size: int = 8,
) -> Dict[str, np.ndarray]:
    """Extract CLS embeddings for all subjects using their respective held-out fold model.

    For each fold k, loads ViT_fold_k.pt and runs inference only on that fold's
    val_subjects (subjects the model never saw during training). Returns a merged
    dict of all subjects — no train-data leakage into the embeddings.

    Args:
        checkpoint_dir: Path to the experiment folder containing ViT_fold_*.pt files.
        task: Task name for data loading (GNG, 1backWM, VF, SS).
              Can differ from the model's training task for cross-task analysis.
        data_dir: Root data directory (e.g. 'data/processed/').
        splits_json: Path to kfold_splits.json.
        data_type: Hemoglobin type ('hbt', 'hbo', 'hbr').
        device: Torch device string.
        batch_size: DataLoader batch size.

    Returns:
        Dict mapping subject_id → embedding vector (shape: dim=64).
    """
    with open(splits_json) as f:
        splits = json.load(f)

    fold_files = sorted(
        f for f in os.listdir(checkpoint_dir)
        if f.startswith('ViT_fold_') and f.endswith('.pt')
    )
    n_folds = len(fold_files)
    fold_key = f'kfold_{n_folds}'

    if fold_key not in splits:
        available = [k for k in splits if k.startswith('kfold_')]
        raise ValueError(
            f"No '{fold_key}' entry in splits JSON. Available: {available}. "
            f"Found {n_folds} checkpoint file(s) in {checkpoint_dir}."
        )

    dataset = FNIRSSequenceDatasetV2(
        root_dir=data_dir,
        transform=None,
        data_type=data_type,
        task_type=task,
        max_trials=_MAX_TRIALS,
    )
    print(f"[embed] Dataset loaded: {task}/{data_type} — {len(dataset)} trials across "
          f"{len(set(dataset.subjects))} subjects")

    all_embeddings: Dict[str, np.ndarray] = {}

    for fold_def in splits[fold_key]:
        fold_idx = fold_def['fold']
        val_subjects = set(fold_def['val_subjects'])

        # Only include subjects that exist in this task's dataset
        available_subjects = set(dataset.subjects)
        extractable = val_subjects & available_subjects
        missing = val_subjects - available_subjects
        if missing:
            print(f"  [fold {fold_idx}] Warning: {len(missing)} val_subject(s) not in "
                  f"{task} dataset (may lack data for this task): {sorted(missing)}")

        if not extractable:
            print(f"  [fold {fold_idx}] Skipped — no extractable subjects.")
            continue

        checkpoint_path = os.path.join(checkpoint_dir, f'ViT_fold_{fold_idx}.pt')
        if not os.path.exists(checkpoint_path):
            raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")

        model = build_model()
        model = load_checkpoint(model, checkpoint_path, device=device)

        fold_embeddings = extract_cls_embeddings(
            model=model,
            dataset=dataset,
            subject_set=extractable,
            device=device,
            batch_size=batch_size,
        )
        all_embeddings.update(fold_embeddings)
        print(f"  [fold {fold_idx}] Extracted {len(fold_embeddings)} subjects: "
              f"{sorted(fold_embeddings.keys())}")

    print(f"[embed] Done: {len(all_embeddings)} total subjects for task={task}")
    return all_embeddings
