"""Data-leakage tests for holdout, k-fold, and LOSO loaders.

Each test class verifies a different leakage property.  All tests run
against synthetic data by default; pass --data-dir to also run against
real preprocessed data:

    pytest tests/test_data_leakage.py -v                          # synthetic only
    pytest tests/test_data_leakage.py -v --data-dir ./data        # synthetic + real

Leakage properties verified per strategy:

  Holdout  — index disjoint, full sample coverage
  K-Fold   — index disjoint within fold, val folds partition full dataset, subject disjoint
  LOSO     — index disjoint, val folds partition full dataset,
             each subject held out exactly once
"""

import pytest

from src.core.datasets import create_single_task_dataset, get_data

TASK = 'GNG'
DATA_TYPE = 'hbt'
TASK_TYPES = {TASK: {}}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _indices(loader) -> set:
    """Extract raw Subset indices from DataLoader → TransformWrapper → Subset."""
    return set(loader.dataset.subset.indices)


def _subjects(loader) -> set:
    result = set()
    for _, _, batch_subjects in loader:
        result.update(batch_subjects)
    return result


# ---------------------------------------------------------------------------
# Holdout
# ---------------------------------------------------------------------------

class TestHoldoutLeakage:
    def test_train_val_index_disjoint(self, any_data_dir):
        train_loader, val_loader = get_data(
            root_dir=any_data_dir,
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            test_size=0.5,
        )
        overlap = _indices(train_loader) & _indices(val_loader)
        assert not overlap, f"Index leakage: {len(overlap)} shared samples"

    def test_all_samples_covered(self, any_data_dir):
        """Every sample must end up in either train or val — none silently dropped."""
        dataset = create_single_task_dataset(any_data_dir, TASK, DATA_TYPE)
        train_loader, val_loader = get_data(
            root_dir=any_data_dir,
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            test_size=0.5,
        )
        covered = _indices(train_loader) | _indices(val_loader)
        assert covered == set(range(len(dataset))), \
            f"{len(set(range(len(dataset))) - covered)} samples missing from both splits"

    def test_train_val_subject_disjoint(self, any_data_dir):
        train_loader, val_loader = get_data(
            root_dir=any_data_dir,
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            test_size=0.5,
        )
        overlap = _subjects(train_loader) & _subjects(val_loader)
        assert not overlap, f"Subject leakage: {overlap}"


# ---------------------------------------------------------------------------
# Stratified K-Fold
# ---------------------------------------------------------------------------

class TestKFoldLeakage:
    def test_within_fold_index_disjoint(self, any_data_dir):
        fold_data = get_data(
            root_dir=any_data_dir,
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_stratified_kfold=True,
            k_folds=2,
        )
        for fold_idx, (train_loader, val_loader) in enumerate(fold_data):
            overlap = _indices(train_loader) & _indices(val_loader)
            assert not overlap, \
                f"Fold {fold_idx}: index leakage — {len(overlap)} shared samples"

    def test_val_folds_partition_full_dataset(self, any_data_dir):
        """Each sample must appear in validation exactly once across all folds."""
        dataset = create_single_task_dataset(any_data_dir, TASK, DATA_TYPE)
        fold_data = get_data(
            root_dir=any_data_dir,
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_stratified_kfold=True,
            k_folds=2,
        )
        all_val: list[int] = []
        for _, val_loader in fold_data:
            all_val.extend(_indices(val_loader))

        assert len(all_val) == len(set(all_val)), \
            "Some samples appear in validation more than once across folds"
        assert set(all_val) == set(range(len(dataset))), \
            f"{len(set(range(len(dataset))) - set(all_val))} samples never appear in validation"

    def test_within_fold_subject_disjoint(self, any_data_dir):
        fold_data = get_data(
            root_dir=any_data_dir,
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_stratified_kfold=True,
            k_folds=2,
        )
        for fold_idx, (train_loader, val_loader) in enumerate(fold_data):
            overlap = _subjects(train_loader) & _subjects(val_loader)
            assert not overlap, \
                f"Fold {fold_idx}: subject leakage — {overlap}"


# ---------------------------------------------------------------------------
# LOSO
# ---------------------------------------------------------------------------

class TestLOSOLeakage:
    def test_within_fold_index_disjoint(self, any_data_dir):
        fold_data = get_data(
            root_dir=any_data_dir,
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_loso_cv=True,
        )
        for fold_idx, (train_loader, val_loader, _) in enumerate(fold_data):
            overlap = _indices(train_loader) & _indices(val_loader)
            assert not overlap, \
                f"LOSO fold {fold_idx}: index leakage — {len(overlap)} shared samples"

    def test_val_folds_partition_full_dataset(self, any_data_dir):
        """Each sample must appear in validation exactly once across all LOSO folds."""
        dataset = create_single_task_dataset(any_data_dir, TASK, DATA_TYPE)
        fold_data = get_data(
            root_dir=any_data_dir,
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_loso_cv=True,
        )
        all_val: list[int] = []
        for _, val_loader, _ in fold_data:
            all_val.extend(_indices(val_loader))

        assert len(all_val) == len(set(all_val)), \
            "Some samples appear in LOSO validation more than once"
        assert set(all_val) == set(range(len(dataset))), \
            f"{len(set(range(len(dataset))) - set(all_val))} samples never appear in LOSO validation"

    def test_each_subject_held_out_exactly_once(self, any_data_dir):
        """Every subject must appear as val_subject exactly once — no subject skipped or duplicated."""
        dataset = create_single_task_dataset(any_data_dir, TASK, DATA_TYPE)
        all_subjects = set(dataset.subjects)

        fold_data = get_data(
            root_dir=any_data_dir,
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_loso_cv=True,
        )
        val_sequence = [val_subject for _, _, val_subject in fold_data]

        assert set(val_sequence) == all_subjects, \
            f"Missing subjects: {all_subjects - set(val_sequence)}"
        assert len(val_sequence) == len(all_subjects), \
            f"{len(val_sequence) - len(all_subjects)} subject(s) held out more than once"

    def test_within_fold_subject_disjoint(self, any_data_dir):
        fold_data = get_data(
            root_dir=any_data_dir,
            data_type=DATA_TYPE,
            task_types=TASK_TYPES,
            batch_size=4,
            use_loso_cv=True,
        )
        for fold_idx, (train_loader, val_loader, _) in enumerate(fold_data):
            overlap = _subjects(train_loader) & _subjects(val_loader)
            assert not overlap, \
                f"LOSO fold {fold_idx}: subject leakage — {overlap}"
