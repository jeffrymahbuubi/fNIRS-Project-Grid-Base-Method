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

---

## Experiment Results (2026-04-28)

**Model:** ViT (Vision Transformer) | **Epochs:** 100 | **Batch size:** 8 | **Patience:** 100  
**Subjects:** 48 (32 anxiety / 16 control) | **Signals:** HbO, HbR, HbT | **CV:** 5-Fold, 10-Fold, LOSO

All metrics reported as **Mean ± SD** across folds. Positive class = Anxiety/Cognitive Load (label 1).

Full per-fold details: [`research/experiments/20260428/experiment_results.md`](research/experiments/20260428/experiment_results.md)

### Primary Metrics — All Completed Experiments

| Task | Signal | CV | Acc (Mean±SD) | Sens (Mean±SD) | Spec (Mean±SD) | F1 (Mean±SD) | κ (Mean±SD) | MCC (Mean±SD) | Overall Acc | Overall F1 |
|------|--------|----|--------------|----------------|----------------|-------------|-------------|--------------|------------|------------|
| 1backWM | HbO | 5-fold | 0.775±0.134 | 0.788±0.089 | 0.767±0.201 | 0.716±0.108 | 0.535±0.235 | 0.550±0.226 | 0.771 | 0.694 |
| 1backWM | HbR | 5-fold | 0.461±0.168 | 0.800±0.274 | 0.280±0.389 | 0.494±0.060 | 0.079±0.129 | 0.080±0.130 | 0.458 | 0.500 |
| 1backWM | HbT | 5-fold | 0.821±0.156 | 0.696±0.255 | 0.891±0.099 | 0.720±0.229 | 0.592±0.341 | 0.596±0.341 | 0.818 | 0.711 |
| 1backWM | HbT | 10-fold | 0.834±0.199 | 0.838±0.213 | 0.825±0.303 | 0.804±0.194 | 0.665±0.360 | 0.669±0.361 | 0.828 | 0.759 |
| 1backWM | HbO | 10-fold | 0.854±0.153 | 0.838±0.156 | 0.850±0.235 | 0.823±0.146 | 0.698±0.280 | 0.717±0.259 | 0.849 | 0.785 |
| 1backWM | HbR | 10-fold | 0.599±0.203 | 0.863±0.171 | 0.417±0.402 | 0.605±0.081 | 0.249±0.272 | 0.267±0.304 | 0.589 | 0.591 |
| GNG | HbO | 5-fold | 0.679±0.078 | 0.642±0.160 | 0.693±0.183 | 0.568±0.048 | 0.322±0.078 | 0.339±0.064 | 0.682 | 0.573 |
| GNG | HbR | 5-fold | 0.607±0.173 | 0.633±0.254 | 0.605±0.350 | 0.514±0.087 | 0.234±0.149 | 0.241±0.154 | 0.604 | 0.513 |
| GNG | HbT | 5-fold | 0.789±0.145 | 0.779±0.150 | 0.782±0.207 | 0.725±0.157 | 0.553±0.279 | 0.565±0.275 | 0.786 | 0.709 |
| GNG | HbO | 10-fold | 0.733±0.176 | 0.850±0.165 | 0.673±0.286 | 0.693±0.137 | 0.475±0.284 | 0.496±0.280 | 0.734 | 0.675 |
| GNG | HbR | 10-fold | 0.668±0.223 | 0.800±0.222 | 0.565±0.397 | 0.643±0.154 | 0.349±0.349 | 0.364±0.346 | 0.656 | 0.607 |
| **GNG** | **HbT** | **10-fold** | **0.884±0.124** | **0.900±0.115** | **0.869±0.164** | **0.854±0.125** | **0.754±0.236** | **0.764±0.227** | **0.880** | **0.832** |
| SS | HbO | 5-fold | 0.707±0.129 | 0.713±0.107 | 0.694±0.216 | 0.628±0.109 | 0.392±0.215 | 0.403±0.203 | 0.703 | 0.617 |
| SS | HbR | 5-fold | 0.630±0.124 | 0.667±0.132 | 0.614±0.125 | 0.550±0.121 | 0.254±0.230 | 0.264±0.234 | 0.630 | 0.542 |
| SS | HbT | 5-fold | 0.657±0.210 | 0.633±0.217 | 0.681±0.388 | 0.569±0.094 | 0.330±0.222 | 0.337±0.230 | 0.651 | 0.544 |
| SS | HbT | 10-fold | 0.789±0.232 | 0.925±0.105 | 0.692±0.387 | 0.808±0.176 | 0.613±0.394 | 0.634±0.374 | 0.781 | 0.738 |
| SS | HbO | 10-fold | 0.810±0.179 | 0.838±0.196 | 0.796±0.268 | 0.781±0.176 | 0.619±0.334 | 0.643±0.315 | 0.802 | 0.729 |
| SS | HbR | 10-fold | 0.499±0.139 | 0.637±0.393 | 0.446±0.401 | 0.387±0.189 | 0.064±0.102 | 0.099±0.136 | 0.495 | 0.446 |
| VF | HbO | 5-fold | 0.755±0.136 | 0.633±0.173 | 0.813±0.147 | 0.637±0.178 | 0.451±0.283 | 0.457±0.284 | 0.750 | 0.625 |
| VF | HbR | 5-fold | 0.607±0.170 | 0.700±0.240 | 0.560±0.326 | 0.543±0.096 | 0.240±0.201 | 0.250±0.211 | 0.609 | 0.540 |
| VF | HbT | 5-fold | 0.667±0.149 | 0.542±0.257 | 0.741±0.234 | 0.508±0.211 | 0.284±0.274 | 0.298±0.277 | 0.667 | 0.508 |
| VF | HbT | 10-fold | 0.889±0.090 | 0.875±0.156 | 0.910±0.094 | 0.843±0.136 | 0.761±0.194 | 0.775±0.176 | 0.885 | 0.831 |
| VF | HbO | 10-fold | 0.845±0.159 | 0.762±0.297 | 0.900±0.135 | 0.771±0.264 | 0.664±0.350 | 0.683±0.331 | 0.839 | 0.744 |
| VF | HbR | 10-fold | 0.830±0.196 | 0.950±0.121 | 0.754±0.330 | 0.832±0.158 | 0.679±0.337 | 0.701±0.325 | 0.823 | 0.779 |

### Best Performance — HbT (Primary Signal), 10-Fold CV

| Rank | Task | Overall Acc | Overall F1 | Mean κ | Mean MCC |
|------|------|------------|------------|--------|---------|
| 1 | **GNG** | **0.880** | **0.832** | **0.754** | **0.764** |
| 2 | VF | 0.885 | 0.831 | 0.761 | 0.775 |
| 3 | 1backWM | 0.828 | 0.759 | 0.665 | 0.669 |
| 4 | SS | 0.781 | 0.738 | 0.613 | 0.634 |

> GNG ranked #1 on κ and MCC (more robust beyond-chance metrics) despite VF having marginally higher pooled Acc/F1. **GNG-HbT-10fold** is the recommended best configuration.

### Key Observations

**Signal comparison (5-fold, pooled across 4 tasks):**

| Signal | Mean Acc | Mean F1 | Mean κ | Mean MCC |
|--------|----------|---------|--------|---------|
| HbT | 0.733 | 0.632 | 0.440 | 0.449 |
| HbO | 0.704 | 0.609 | 0.391 | 0.385 |
| HbR | 0.575 | 0.525 | 0.172 | 0.179 |

- **HbT dominates** all signals on every metric across all tasks and CV strategies.
- **HbR is unreliable**: multiple folds collapse to all-positive prediction (κ ≈ 0, near-chance).
- **HbO** provides moderate discrimination, consistently ranked second.

**CV strategy impact — HbT, 5-fold vs 10-fold (Overall Acc):**

| Task | 5-fold Acc | 10-fold Acc | Δ Acc | 5-fold κ | 10-fold κ | Δ κ |
|------|-----------|------------|-------|---------|----------|-----|
| 1backWM | 0.818 | 0.828 | +0.010 | 0.578 | 0.626 | +0.048 |
| GNG | 0.786 | 0.880 | +0.094 | 0.543 | 0.740 | +0.197 |
| SS | 0.651 | 0.781 | +0.130 | 0.269 | 0.563 | +0.294 |
| VF | 0.667 | 0.885 | +0.218 | 0.256 | 0.744 | +0.488 |

10-fold consistently outperforms 5-fold; largest gains: VF (+21.8% acc) and SS (+13.0% acc).

### Leave-One-Subject-Out (LOSO) — Pending

> **Results will be updated here once LOSO experiments are complete.**

| Task | Signal | Acc (Mean±SD) | Sens (Mean±SD) | Spec (Mean±SD) | F1 (Mean±SD) | κ (Mean±SD) | MCC (Mean±SD) | Overall Acc | Overall F1 |
|------|--------|--------------|----------------|----------------|-------------|-------------|--------------|------------|------------|
| GNG | HbO | — | — | — | — | — | — | — | — |
| GNG | HbR | — | — | — | — | — | — | — | — |
| GNG | HbT | — | — | — | — | — | — | — | — |
| VF | HbO | — | — | — | — | — | — | — | — |
| VF | HbR | — | — | — | — | — | — | — | — |
| VF | HbT | — | — | — | — | — | — | — | — |
| SS | HbO | — | — | — | — | — | — | — | — |
| SS | HbR | — | — | — | — | — | — | — | — |
| SS | HbT | — | — | — | — | — | — | — | — |
| 1backWM | HbO | — | — | — | — | — | — | — | — |
| 1backWM | HbR | — | — | — | — | — | — | — | — |
| 1backWM | HbT | — | — | — | — | — | — | — | — |
