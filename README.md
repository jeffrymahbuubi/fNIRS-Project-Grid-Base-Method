# fNIRS Grid-Based Method for GAD Classification

This repository contains the implementation for **"Grid-Based Spatiotemporal Encoding of fNIRS Signals for Generalized Anxiety Disorder Classification Using a 3D Vision Transformer"** (target: IEEE TNSRE).

The core contribution is a novel 1D→2D→3D encoding pipeline that maps 23 fNIRS channels to a spatial grid, constructs video-like tensors, and applies a 3D Vision Transformer (ViT) for binary GAD classification (anxiety vs. healthy control). Four cognitive tasks are evaluated — Go/No-Go (GNG), 1-Back Working Memory (1backWM), Verbal Fluency (VF), and Serial Subtraction (SS) — across three hemoglobin signal types (HbO, HbR, HbT), with performance validated using 5-fold, 10-fold, and leave-one-subject-out (LOSO) cross-validation.

---

## Environment Setup

### 1. Install `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create and activate a virtual environment

```bash
uv venv .venv --python 3.12
source .venv/bin/activate
```

### 3. Install PyTorch (CUDA 12.4)

```bash
uv pip install torch==2.6.0+cu124 torchvision==0.21.0+cu124 torchaudio==2.6.0+cu124 \
  --index-url https://download.pytorch.org/whl/cu124
```

> **CPU-only systems:** replace `cu124` with `cpu` in both the package names and the index URL.

### 4. Install remaining dependencies

```bash
uv pip install -r requirements.txt
```

---

## Reproducing Results

All commands are run from the **project root directory**.

### Step 0 — Generate k-fold splits (run once)

K-fold experiments require a deterministic splits file so fold assignments are identical across runs and collaborators:

```bash
python data/generate_splits.py --processed_dir data/processed
```

Output: `data/splits/kfold_splits.json`

---

### 5-Fold Cross-Validation

```bash
python -m src.core.main \
  --data_dir data/processed/ \
  --task GNG \
  --data_type hbo \
  --use_kfold --k_folds 5 \
  --splits_json data/splits/kfold_splits.json \
  --epochs 100 --batch_size 8 --patience 100 --num_workers 4
```

---

### 10-Fold Cross-Validation

```bash
python -m src.core.main \
  --data_dir data/processed/ \
  --task GNG \
  --data_type hbo \
  --use_kfold --k_folds 10 \
  --splits_json data/splits/kfold_splits.json \
  --epochs 100 --batch_size 8 --patience 100 --num_workers 4
```

---

### Leave-One-Subject-Out (LOSO)

```bash
python -m src.core.main \
  --data_dir data/processed/ \
  --task GNG \
  --data_type hbo \
  --use_loso \
  --epochs 100 --batch_size 8 --patience 100 --num_workers 4
```

> LOSO does not require `--splits_json`.

---

## Parameter Reference

Vary `--task` and `--data_type` to reproduce all experiment combinations.

| Argument | Values |
|----------|--------|
| `--task` | `GNG`, `1backWM`, `VF`, `SS` |
| `--data_type` | `hbo`, `hbr`, `hbt` |

Results are saved to `./experiments/saved_models/<experiment_name>/`. Use `--save_dir <path>` to change the output location.
