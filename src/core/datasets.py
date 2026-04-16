# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring, too-many-instance-attributes, too-many-arguments, too-many-locals, redefined-argument-from-local, reimported, invalid-name, wrong-import-order, ungrouped-imports, no-else-return, redefined-outer-name

import os
from collections import defaultdict

import numpy as np
import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader, Subset
from einops import rearrange
from sklearn.model_selection import StratifiedKFold, train_test_split


class FNIRSSequenceDatasetV2(Dataset):
    def __init__(self, root_dir, transform=None, data_type='hbo', task_type='GNG',
                 max_trials=None):
        self.root_dir = root_dir
        self.transform = transform
        self.data_type = data_type.lower()
        self.data = []
        self.labels = []
        self.subjects = []
        self.task_type = task_type
        self.max_trials = max_trials
        self.class_subject_count = {'healthy': set(), 'anxiety': set()}
        self.subject_trial_count = {}
        self.total_npy_files = 0
        self.required_types = (
            self.data_type.split('+')
            if self.data_type != "all" else ['hbo', 'hbr', 'hbt']
        )
        label_map = {'healthy': 0, 'anxiety': 1}

        for label_name, label in label_map.items():
            label_path = os.path.join(self.root_dir, label_name)
            for subject in os.listdir(label_path):
                subject_path = os.path.join(label_path, subject, self.task_type)
                self.class_subject_count[label_name].add(subject)
                # Initialize subject trial count
                self.subject_trial_count[subject] = 0
                for dt in self.required_types:
                    data_dir = os.path.join(subject_path, dt.upper())
                    if os.path.exists(data_dir):
                        self.append_trials(data_dir, label, subject)

    def append_trials(self, data_dir, label, subject):
        trial_count = 0
        for trial_file in sorted(os.listdir(data_dir),
                                 key=lambda x: int(x.split('.')[0])):
            if self.max_trials is not None and trial_count >= self.max_trials:
                break
            file_path = os.path.join(data_dir, trial_file)
            if os.path.exists(file_path):
                trial_data = np.load(file_path)
                self.data.append(trial_data)
                self.labels.append(label)
                self.subjects.append(subject)
                self.total_npy_files += 1
                trial_count += 1
                self.subject_trial_count[subject] += 1

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sequence = self.data[idx]  # Shape: (T, H, W)
        label = torch.tensor(self.labels[idx], dtype=torch.long)
        subject = self.subjects[idx]
        sequence = torch.tensor(sequence, dtype=torch.float32)  # (T, H, W)
        sequence = rearrange(sequence, 't h w -> 1 t h w')
        if self.transform:
            sequence = self.transform(sequence)
        return sequence, label, subject


class ConvertToRGB(nn.Module):
    def forward(self, sequence):
        if sequence.shape[0] != 1:
            raise ValueError(
                f"Input tensor must have a single channel, but got shape {sequence.shape}"
            )
        return sequence.repeat(3, 1, 1, 1)


class RearrangeToTCHW(nn.Module):
    def forward(self, x):
        return rearrange(x, 'c t h w -> t c h w')


class RearrangeBackToCTHW(nn.Module):
    def forward(self, x):
        return rearrange(x, 't c h w -> c t h w')


class AddGaussianNoise(nn.Module):
    def __init__(self, mean=0.0, std=1.0):
        super().__init__()
        self.mean = mean
        self.std = std

    def forward(self, x):
        return x + torch.randn_like(x) * self.std + self.mean


def get_loso_subject_loaders(dataset, batch_size, num_workers, train_transform=None,
                             val_transform=None):
    subject_to_indices = defaultdict(list)
    subject_labels = {}
    for idx, (_, label, subject) in enumerate(dataset):
        subject_to_indices[subject].append(idx)
        subject_labels[subject] = label.item() if hasattr(label, "item") else label
    subjects = list(subject_to_indices.keys())
    fold_data = []
    for i, val_subject in enumerate(subjects):
        print(f"\nPreparing fold {i + 1}/{len(subjects)} with validation subject: {val_subject}")
        val_indices = subject_to_indices[val_subject]
        train_indices = [idx for subj in subjects if subj != val_subject
                         for idx in subject_to_indices[subj]]
        train_subjects = [subj for subj in subjects if subj != val_subject]
        print(f"  Training subjects ({len(train_subjects)}): {train_subjects}")
        print(f"  Validation subject: {val_subject}")
        print(f"  Number of training sequences: {len(train_indices)}")
        print(f"  Number of validation sequences: {len(val_indices)}")
        train_dataset = Subset(dataset, train_indices)
        val_dataset = Subset(dataset, val_indices)
        train_dataset.dataset.transform = train_transform
        val_dataset.dataset.transform = val_transform
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                                  num_workers=num_workers)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False,
                                num_workers=num_workers)
        fold_data.append((train_loader, val_loader, val_subject))
    return fold_data


def get_stratified_kfold_subject_loaders(dataset, k_folds, batch_size, num_workers,
                                         train_transform=None, val_transform=None):
    subject_to_indices = defaultdict(list)
    subject_labels = {}
    for idx, (_, label, subject) in enumerate(dataset):
        subject_to_indices[subject].append(idx)
        subject_labels[subject] = label.item()
    subjects = list(subject_to_indices.keys())
    labels = [subject_labels[subject] for subject in subjects]
    skf = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=42)
    fold_data = []
    for fold_idx, (train_subject_indices, val_subject_indices) in enumerate(skf.split(subjects, labels)):
        print(f"\nPreparing fold {fold_idx + 1}/{k_folds}")
        train_indices = [
            idx for subj_idx in train_subject_indices
            for idx in subject_to_indices[subjects[subj_idx]]
        ]
        val_indices = [
            idx for subj_idx in val_subject_indices
            for idx in subject_to_indices[subjects[subj_idx]]
        ]
        train_subjects = [subjects[subj_idx] for subj_idx in train_subject_indices]
        val_subjects = [subjects[subj_idx] for subj_idx in val_subject_indices]
        train_trials = {subj: len(subject_to_indices[subj]) for subj in train_subjects}
        val_trials = {subj: len(subject_to_indices[subj]) for subj in val_subjects}
        print(f"  Train trials per subject: {train_trials}")
        print(f"  Validation trials per subject: {val_trials}")
        train_labels = [dataset.labels[i] for i in train_indices]
        val_labels = [dataset.labels[i] for i in val_indices]
        print(f"  Train class distribution: {dict(zip(*np.unique(train_labels, return_counts=True)))}")
        print(f"  Validation class distribution: {dict(zip(*np.unique(val_labels, return_counts=True)))}")
        train_dataset = Subset(dataset, train_indices)
        val_dataset = Subset(dataset, val_indices)
        train_dataset.dataset.transform = train_transform
        val_dataset.dataset.transform = val_transform
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                                  num_workers=num_workers)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False,
                                num_workers=num_workers)
        fold_data.append((train_loader, val_loader))
    return fold_data


def get_holdout_subject_loaders(dataset, test_size, batch_size, num_workers,
                                train_transform=None, val_transform=None):
    subjects = np.array(dataset.subjects)
    unique_subjects = np.unique(subjects)
    train_subjects, val_subjects = train_test_split(
        unique_subjects, test_size=test_size, random_state=42
    )
    train_indices = [i for i, subj in enumerate(subjects) if subj in train_subjects]
    val_indices = [i for i, subj in enumerate(subjects) if subj in val_subjects]
    print("\nHoldout Subject Validation")
    print(f"  Number of training subjects: {len(train_subjects)}")
    print(f"  Number of validation subjects: {len(val_subjects)}")
    print(f"  Number of training sequences: {len(train_indices)}")
    print(f"  Number of validation sequences: {len(val_indices)}")
    train_dataset = Subset(dataset, train_indices)
    val_dataset = Subset(dataset, val_indices)
    train_dataset.dataset.transform = train_transform
    val_dataset.dataset.transform = val_transform
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                              num_workers=num_workers)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False,
                            num_workers=num_workers)
    return train_loader, val_loader


def create_single_task_dataset(root_dir, task_name, data_type, max_trials=None):
    dataset = FNIRSSequenceDatasetV2(
        root_dir=root_dir,
        data_type=data_type,
        task_type=task_name,
        max_trials=max_trials,
        transform=None
    )
    return dataset


def get_data(root_dir, data_type='hbo', task_types=None, batch_size=8, test_size=0.2,
             num_workers=0, use_stratified_kfold=False, k_folds=5, use_loso_cv=False,
             max_trials=None, train_transform=None, val_transform=None):
    if task_types is None:
        task_types = {'GNG': {'window_duration': 0.8}}
    task_name, _ = next(iter(task_types.items()))
    dataset = create_single_task_dataset(root_dir, task_name, data_type, max_trials)
    print(f"Using single-task dataset for task '{task_name}' with task-specific configuration.")
    print(f"Total samples in dataset: {len(dataset)}")
    print(f"Trials per subject: {dataset.subject_trial_count}")
    sample_data, sample_label, sample_subject = dataset[0]
    print(f"{task_name} data shape: {sample_data.shape}, label: {sample_label}, subject: {sample_subject}")
    if use_loso_cv:
        return get_loso_subject_loaders(dataset, batch_size, num_workers, train_transform, val_transform)
    elif use_stratified_kfold:
        return get_stratified_kfold_subject_loaders(dataset, k_folds, batch_size, num_workers,
                                                      train_transform, val_transform)
    else:
        return get_holdout_subject_loaders(dataset, test_size, batch_size, num_workers,
                                           train_transform, val_transform)
