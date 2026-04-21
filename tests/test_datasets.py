"""Tests for datasets.py — verifies TransformWrapper correctness across all three
loader strategies (holdout, k-fold, LOSO).

Run from project root with the project venv active:
    pytest tests/test_datasets.py -v
"""

import torch
import pytest
from torch.utils.data import Subset

from src.core.datasets import (
    AddGaussianNoise,
    TransformWrapper,
    create_single_task_dataset,
    get_data,
)

TASK = 'GNG'
DATA_TYPE = 'hbt'
TASK_TYPES = {TASK: {}}


class _OffsetTransform(torch.nn.Module):
    """Adds a fixed scalar offset — deterministic, trivially detectable."""
    def __init__(self, offset: float):
        super().__init__()
        self.offset = offset

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x + self.offset


def _mean_of_loader(loader) -> float:
    total, count = 0.0, 0
    for batch, _, _ in loader:
        total += batch.float().sum().item()
        count += batch.numel()
    return total / count


# ---------------------------------------------------------------------------
# TransformWrapper unit tests
# ---------------------------------------------------------------------------

class TestTransformWrapper:
    def test_applies_transform(self, synthetic_data_dir):
        dataset = create_single_task_dataset(str(synthetic_data_dir), TASK, DATA_TYPE)
        subset = Subset(dataset, list(range(min(4, len(dataset)))))
        wrapped = TransformWrapper(subset, _OffsetTransform(offset=50.0))

        seq_wrapped, _, _ = wrapped[0]
        seq_raw, _, _ = dataset[0]
        assert (seq_wrapped - seq_raw).mean().item() == pytest.approx(50.0, abs=1e-4)

    def test_none_transform_returns_unmodified(self, synthetic_data_dir):
        dataset = create_single_task_dataset(str(synthetic_data_dir), TASK, DATA_TYPE)
        subset = Subset(dataset, [0])
        wrapped = TransformWrapper(subset, transform=None)

        seq_wrapped, _, _ = wrapped[0]
        seq_raw, _, _ = dataset[0]
        assert torch.allclose(seq_wrapped, seq_raw)

    def test_base_dataset_transform_unchanged(self, synthetic_data_dir):
        """TransformWrapper must not mutate dataset.transform on the shared object."""
        dataset = create_single_task_dataset(str(synthetic_data_dir), TASK, DATA_TYPE)
        assert dataset.transform is None
        subset = Subset(dataset, [0])
        _ = TransformWrapper(subset, _OffsetTransform(offset=1.0))
        assert dataset.transform is None, "TransformWrapper must not touch dataset.transform"


# ---------------------------------------------------------------------------
# Holdout
# ---------------------------------------------------------------------------

class TestHoldoutTransforms:
    def test_train_gets_train_transform(self, synthetic_data_dir):
        train_loader, val_loader = get_data(
            root_dir=str(synthetic_data_dir),
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            test_size=0.5,
            train_transform=_OffsetTransform(offset=100.0),
            val_transform=_OffsetTransform(offset=0.0),
        )
        assert _mean_of_loader(train_loader) > _mean_of_loader(val_loader) + 50.0

    def test_train_val_subjects_disjoint(self, synthetic_data_dir):
        train_loader, val_loader = get_data(
            root_dir=str(synthetic_data_dir),
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            test_size=0.5,
        )
        train_subj = {s for _, _, batch in train_loader for s in batch}
        val_subj = {s for _, _, batch in val_loader for s in batch}
        assert train_subj.isdisjoint(val_subj)


# ---------------------------------------------------------------------------
# Stratified K-Fold
# ---------------------------------------------------------------------------

class TestKFoldTransforms:
    def test_every_fold_train_gets_train_transform(self, synthetic_data_dir):
        fold_data = get_data(
            root_dir=str(synthetic_data_dir),
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_stratified_kfold=True,
            k_folds=2,
            train_transform=_OffsetTransform(offset=100.0),
            val_transform=_OffsetTransform(offset=0.0),
        )
        for fold_idx, (train_loader, val_loader) in enumerate(fold_data):
            assert _mean_of_loader(train_loader) > _mean_of_loader(val_loader) + 50.0, \
                f"Fold {fold_idx}: train transform not applied independently of val transform"

    def test_every_fold_subjects_disjoint(self, synthetic_data_dir):
        fold_data = get_data(
            root_dir=str(synthetic_data_dir),
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_stratified_kfold=True,
            k_folds=2,
        )
        for fold_idx, (train_loader, val_loader) in enumerate(fold_data):
            train_subj = {s for _, _, batch in train_loader for s in batch}
            val_subj = {s for _, _, batch in val_loader for s in batch}
            assert train_subj.isdisjoint(val_subj), \
                f"Fold {fold_idx}: subject leakage between train and val"


# ---------------------------------------------------------------------------
# LOSO
# ---------------------------------------------------------------------------

class TestLOSOTransforms:
    def test_every_fold_train_gets_train_transform(self, synthetic_data_dir):
        fold_data = get_data(
            root_dir=str(synthetic_data_dir),
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_loso_cv=True,
            train_transform=_OffsetTransform(offset=100.0),
            val_transform=_OffsetTransform(offset=0.0),
        )
        for fold_idx, (train_loader, val_loader, _) in enumerate(fold_data):
            assert _mean_of_loader(train_loader) > _mean_of_loader(val_loader) + 50.0, \
                f"LOSO fold {fold_idx}: train transform not applied independently"

    def test_val_contains_exactly_one_subject(self, synthetic_data_dir):
        fold_data = get_data(
            root_dir=str(synthetic_data_dir),
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_loso_cv=True,
        )
        for _, val_loader, val_subject in fold_data:
            val_subj = {s for _, _, batch in val_loader for s in batch}
            assert val_subj == {val_subject}, \
                f"Expected only '{val_subject}' in val, got {val_subj}"

    def test_train_val_subjects_disjoint(self, synthetic_data_dir):
        fold_data = get_data(
            root_dir=str(synthetic_data_dir),
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_loso_cv=True,
        )
        for fold_idx, (train_loader, val_loader, _) in enumerate(fold_data):
            train_subj = {s for _, _, batch in train_loader for s in batch}
            val_subj = {s for _, _, batch in val_loader for s in batch}
            assert train_subj.isdisjoint(val_subj), \
                f"LOSO fold {fold_idx}: subject leakage"
