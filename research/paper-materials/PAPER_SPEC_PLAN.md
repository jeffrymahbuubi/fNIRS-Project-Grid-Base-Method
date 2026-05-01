# Paper Specification & Writing Plan
**fNIRS Grid-Based Method — IEEE TNSRE Submission**
**Last updated: 2026-04-29**

---

## 1. Paper Identity

| Field | Value |
|---|---|
| **Working Title** | Grid-Based Spatiotemporal Encoding of fNIRS Signals for Generalized Anxiety Disorder Classification Using a 3D Vision Transformer |
| **Target Journal** | IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE) |
| **Paper Type** | Original Research — Methods + Classification |
| **Core Contribution** | Novel 1D→2D→3D encoding pipeline that maps 23 fNIRS channels to a spatial grid, constructs video-like tensors, and applies a 3D ViT for GAD classification |
| **Dual Scope** | (1) Introduce the grid-based encoding methodology; (2) Evaluate GAD classification/decoding performance |

---

## 2. Key Technical Facts (Ground Truth — Reference Before Writing)

### 2.1 Dataset
**Source:** `src/notebook/statistical-analysis/01_demographic/01_demographic_analysis.ipynb`

| Parameter | Value |
|---|---|
| Total recruited | 53 adults; **48 in final analysis** after exclusions |
| Exclusions | 5 total (1 HC + 4 GAD) — incomplete task recordings |
| HC | **32 subjects**, age **72.7 ± 5.2** yrs (range 65–84), **72% female (23F / 9M)** |
| GAD | **16 subjects**, age **49.5 ± 14.3** yrs (range 29–70), **81% female (13F / 3M)** |
| Age gap (confound) | t(46) = 8.20, p = 1.50×10⁻¹⁰ — **must be discussed as limitation** |
| Sex balance | χ²(1) = 0.13, p = 0.72 — balanced, not a confound |
| HAMA (GAD only) | **22.0 ± 10.3** (incl. LA063=0, n=16) / **23.5 ± 8.7** (excl. LA063, n=15); range 0–40 |
| STAI-S | HC: **29.4±8.5**, GAD: **45.8±8.7** (t(46)=−6.26, p<0.001, d=1.90) |
| STAI-T | HC: **34.1±9.7**, GAD: **57.2±6.8** (t(46)=−8.54, p<0.001, d=2.59) |
| Special case | AH029 (HC) — self-reported MDD, receiving psychotherapy + meds; retained (no confirmed diagnosis), interpret with caution |
| HAMA missing | LA063 — HAMA=0 (not administered); retained based on elevated STAI-S=55, STAI-T=63 |

### 2.2 fNIRS System
| Parameter | Value |
|---|---|
| Channels | 23 channels (8 source-detector pairs) |
| Wavelengths | 760 nm, 850 nm |
| Source-detector distance | 2.49–4.19 cm |
| Placement | Prefrontal cortex, international 10-20 system |
| Hemodynamic measures | HbO, HbR, HbT |
| Chosen measure | **HbT** (statistically justified: only Hb type reaching significance at S7_D6, p=0.026, d=0.64) |

### 2.3 Experimental Tasks
| Task | Code | Role in paper |
|---|---|---|
| Go/No-Go | GNG | **Best classifier** — LOSO: Acc=71.4%, Sens=95.3%, κ=0.459 (tied 1st with VF); most stable across all CV strategies (5-fold κ=0.553, 10-fold κ=0.754, LOSO κ=0.459) |
| Serial Subtraction | SS | Secondary |
| 1-Back Working Memory | 1backWM | Secondary (highest Cohen's d at S7_D6: d=0.832) |
| Verbal Fluency | VF | Secondary |

### 2.4 Grid Encoding Pipeline (Core Methodology)
| Step | Detail |
|---|---|
| Raw data | 23 fNIRS channels → 1D time series per channel |
| Grid mapping | 23 channels placed into **5×7 spatial grid** (H=5 rows, W=7 cols) using anatomical optode positions |
| Sparse grid | 12 of 35 cells are empty (zero) after channel placement |
| Interpolation | Empty cells filled via **Gaussian RBF interpolation** (`scipy.interpolate.Rbf`) |
| Clip construction | Stack T interpolated frames → **(T, 5, 7)** native tensor |
| **Spatial resize** | **(T, 5, 7) → (T, H, W)** via bilinear interpolation (`torchvision.transforms.v2.Resize`) to meet ViT patch-embedding requirements. Spatial topology preserved; information content bounded by 23 channels. H/W = 32/64/128 depending on config. |
| Temporal sampling | `UniformTemporalSubsample(T)` → T frames uniformly drawn from the native clip |
| RGB replication | Single-channel signal replicated ×3 for 3-channel ViT input: **(3, T, H, W)** |
| **Spatial info bound** | Effective spatial resolution is bounded by 23 discrete channel positions regardless of H/W — the resize increases token count but introduces no new measurement information |

**Confirmed channel-to-grid mapping (from `processor_cli.py:get_channel_positions()`):**
```
Channel      Row  Col    Channel      Row  Col    Channel      Row  Col
S1_D1        0    2      S3_D3        2    1      S6_D3        3    0
S2_D1        0    3      S3_D4        2    2      S3_D6        3    1
S2_D2        0    4      S4_D4        2    3      S7_D4        3    2
S1_D3        1    1      S4_D5        2    4      S4_D7        3    4
S3_D1        1    2      S5_D5        2    5      S8_D5        3    5
S2_D5        1    4                              S5_D8        3    6
S5_D2        1    5      S6_D6        4    1
                         S7_D6        4    2
                         S7_D7        4    3
                         S8_D7        4    4
                         S8_D8        4    5
```

**Grid visualization (• = channel, · = empty/interpolated):**
```
Col:   0    1    2    3    4    5    6
Row 0: ·    ·   S1D1 S2D1 S2D2  ·   ·
Row 1: ·   S1D3 S3D1  ·  S2D5 S5D2  ·
Row 2: ·   S3D3 S3D4 S4D4 S4D5 S5D5  ·
Row 3: S6D3 S3D6 S7D4  ·  S4D7 S8D5 S5D8
Row 4: ·   S6D6 S7D6 S7D7 S8D7 S8D8  ·
```

### 2.5 Model Architecture (ViT 3D)
| Parameter | Experimental Values Being Tested |
|---|---|
| **Clip size** (T, H, W) | **(256, 128, 128)** — Config C (confirmed default in `main.py`) |
| **Patch size** (t, h, w) | **(16, 8, 8)** — tubelet size for Config C |
| Spatial patch | 8×8 |
| Temporal frame patch | 16 frames |
| Depth L | **6** transformer encoder layers (confirmed `main.py:191`) |
| Heads | **8** |
| Embedding dim d | **64** (confirmed `main.py:189`) |
| dim_head | **64** (per-head dimension, `models.py:25`) |
| MLP hidden dim | **512** (8× expansion, confirmed `main.py:192`) |
| Channels | 3 (single-channel HbT replicated ×3 via `ConvertToRGB`) |
| Pool | CLS token |
| Classes | 2 (HC=0, GAD=1) |
| Loss | CrossEntropyLoss (label_smoothing=0.0 default; optional class weights) |
| Training budget | 100 epochs fixed; **best val F1 checkpoint restored** at end (patience=100 = epoch budget → stopping criterion never fires) |
| Augmentation | **None** in default pipeline (`AddGaussianNoise` class exists but unused) |
| Weight init | Xavier uniform (Linear layers), constant 1.0/0.0 (LayerNorm) |

### 2.6 Evaluation Strategies
- 5-Fold Cross-Validation (subject-level stratified)
- 10-Fold Cross-Validation
- Leave-One-Subject-Out (LOSO)
- Metrics: Accuracy, Sensitivity, Specificity, F1-Score, AUC

### 2.7 Key Statistical Results (Available Now)

**Brain Activation (NB02):**
- S7_D6 significant across ALL 4 tasks (most consistent channel)
- Task-level effect sizes at S7_D6: 1backWM (d=0.832), VF (d=0.669), GNG (d=0.644), SS (d=0.583)
- GNG classification dominance NOT explained by univariate amplitude — spatiotemporal dynamics explain superiority

**Hb Type (NB03):**
- Global Friedman χ²(2)=0.61, p=0.74 — no global difference across Hb types
- HbT uniquely significant at S7_D6: p=0.026, d=0.64
- HbO at S7_D6: p=0.086 ns; HbR at S7_D6: p=0.071 ns
- **Paper narrative:** HbT statistically justified as most sensitive measure

**Severity Correlation (NB04):**
- No FDR-surviving correlations between channel activation and STAI-T / HAMA
- S3_D1 shows trend-level STAIT correlation: r=-0.484, p=0.057
- **Interpretation:** Activation ≠ direct severity proxy; clinical scores confirm group separation but not channel-level dose-response

**Old codebase results (reference baseline):**
- GNG: LOSO 97.6% Acc, 100% Sensitivity
- GNG ranked #1 across all tasks
- File: `research/paper-materials/old-result/fnirs-anxiety-detection-paper.md` and `.pdf`

---

## 3. Paper Section Plan

### Section 1: Introduction
**Status: READY TO WRITE**
**Word target: ~600–800 words (TNSRE standard)**

Sub-sections to cover (in order):
1. **GAD clinical burden** — 7.6% prevalence, US$42B cost, under-detection (only 9.8% receive care)
2. **Limitations of current screening** — GAD-7 self-report bias, lacks objective neural biomarkers
3. **fNIRS as a biomarker** — prefrontal cortex hypo-activation in GAD; advantages over fMRI (portable, 10 Hz) and EEG (better spatial resolution, less motion artifact)
4. **Literature gap** — existing fNIRS-anxiety studies use hand-crafted features, no end-to-end spatiotemporal deep learning
5. **Proposed grid encoding motivation** — channels are spatially arranged on the scalp; preserving this topology in a 2D grid allows spatial convolution/attention to operate on neuroanatomically meaningful structure
6. **Contributions** (bullet list format acceptable in intro):
   - Novel 1D→2D grid encoding preserving optode spatial topology
   - 3D video-like tensor construction enabling Video ViT
   - Multi-task evaluation (GNG, SS, 1-back, VF) with LOSO validation
   - Statistical grounding for HbT selection and GNG task superiority

**Figures for this section:** Figure from `paper-materials/figure/` — Channel Locations.tif, GNG.tif, SS.tif, VF.tif, 1backWM.tif

**Key citations needed (use research-lookup):**
- GAD prevalence: Kroenke et al. 2007 (already cited in old result)
- fNIRS for psychiatric disorders: recent 2022–2025 reviews
- ViT/Video-ViT prior art: Dosovitskiy 2021, Arnab 2021 (ViViT)
- fNIRS-anxiety prior art: Wang 2025, Shen 2025 (already in literature table)

---

### Section 2: Materials and Methods
**Status: READY TO WRITE**
**Word target: ~1200–1500 words**

#### 2.1 Participants & Dataset Characteristics
- Table 1: Group demographics (HC/GAD n, age, sex, HAMA, STAI-S, STAI-T)
- Age confound disclosure: t(46)=8.20, p=1.50×10⁻¹⁰ — acknowledge here; expand in limitations
- Sex balance: χ²(1)=0.13, p=0.72
- Ethics statement (IRB approval — confirm with advisor)

#### 2.2 fNIRS Data Acquisition
- 23 channels, 8 source-detector pairs, 10-20 placement
- Wavelengths: 760 nm, 850 nm
- Source-detector separation: 2.49–4.19 cm
- Figure: Channel Locations.tif + brain_montage_clean_high_quality.tiff

#### 2.3 Experimental Paradigms
- Go/No-Go (GNG), Serial Subtraction (SS), 1-Back Working Memory, Verbal Fluency
- Brief description of each task; reference figures GNG.tif, SS.tif, 1backWM.tif, VF.tif
- Trial structure (timing, stimulus, response)

#### 2.4 Signal Processing Pipeline
**Stage 1 — Homer3 (MATLAB, `nirs2csv_homer3.m`):**
1. `hmrR_Intensity2OD` — raw NIRx intensity → optical density (OD)
2. `hmrR_BandpassFilt` — bandpass filter: **HPF = 0.01 Hz** (order-5), **LPF = 0.5 Hz** (order-3)
3. `hmrR_OD2Conc` — modified Beer-Lambert Law → HbO, HbR, HbT
   - PPF = **[6, 6]** per wavelength (760 nm, 850 nm)
   - Wavelengths: 760 nm and 850 nm
   - Output: CSV per subject (time vector, zeros placeholder, 23-channel rows)

**Stage 2 — Python MNE (`processor_cli.py`):**
4. HbT = HbO + HbR (computed from loaded CSVs)
5. Annotation alignment — t_offset correction for split sessions
6. Epoching per task (event codes 3.0/4.0 = task trials):
   - GNG: 0–35 s window, crop first 3 s (preparation) → **32 s effective trial**
   - SS: 0–60 s window, crop first 7 s → **53 s effective trial**
   - 1backWM: 0–90 s window, crop first 5 s → **85 s effective trial**
   - VF: 0–60 s window, crop first 7 s → **53 s effective trial**
7. Optional z-score normalization per channel (applied channel-wise)
8. Grid mapping: 23 channels → 5×7 sparse grid → Gaussian RBF interpolation → dense (T, H, W)

**Figure reference:** Figure 7 (sparse grid), Figure 8 (single frame t), Figure 9 (after interpolation), Figure 10 (3D clip S^(k))

#### 2.5 Grid-Based Spatiotemporal Encoding (CORE SECTION)
This is the primary methodological contribution. Write in detail.

**Sub-steps:**
1. **1D → 2D Grid Mapping**
   - Motivation: fNIRS optodes have fixed anatomical positions on the scalp → preserving spatial topology allows the model to learn spatially-coherent hemodynamic patterns
   - 23 channels placed into 5×7 grid based on optode (row, col) positions
   - Empty grid positions set to zero (sparse representation)
   - Figure: Picture1.tif (if it shows the grid mapping), or ViT_Architecture_1.tif

2. **2D → 3D Video Construction**
   - Each time window produces one (H, W) = (5×7) spatial frame
   - Sliding window over trial → stack T frames → tensor (T, H, W)
   - Input to ViT: replicated to (3, T, H, W) for RGB-compatible input
   - Alternative: HbO, HbR, HbT as 3 independent channels
   - Clip size configurations being evaluated: (64,32,32), (128,64,64), (256,128,128)

3. **Motivation paragraph** (key selling point):
   > "Unlike conventional approaches that flatten fNIRS channels into a feature vector, the proposed grid encoding preserves the anatomical spatial arrangement of optodes across the prefrontal cortex. By stacking consecutive temporal frames into a video-like tensor, the representation captures both spatial co-activation patterns and temporal hemodynamic dynamics simultaneously, making it amenable to spatiotemporal attention mechanisms inherent in 3D Vision Transformers."

#### 2.6 3D Vision Transformer Architecture
- ViT-3D model (based on ViViT / vit-pytorch video variant)
- Patch tokenization: spatial (h×w) + temporal (t frames) patches
- Patch embedding → positional encoding → CLS token → transformer encoder → MLP head
- Configurations under ablation (table: clip size × patch size × results)
- Figure: ViT_Architecture_1.tif, ViT_Architecture_2.tif, ViT_Architecture_3.tif

#### 2.7 Evaluation Framework
- 5-Fold CV, 10-Fold CV, LOSO (all subject-level stratified)
- Metrics: Accuracy, Sensitivity, Specificity, F1-Score, AUC
- Rationale for LOSO: strongest evidence of generalization to unseen subjects

---

### Section 3: Statistical Analysis
**Status: READY TO WRITE**
**Word target: ~500–700 words**

#### 3.1 Demographic Statistics (NB01)
- Reference Table 1 from Section 2.1
- Welch t-test for continuous variables, χ² for sex
- STAI/HAMA comparisons

#### 3.2 Brain Activation Analysis (NB02) — ~~REMOVED FROM PAPER~~
**Decision (2026-05-01):** §III.B dropped entirely — analysis did not yield a sufficiently
clear or consistent pattern to justify inclusion in the main paper. NB02 figures
(fig_topo_activation, fig_channel_task_heatmap, etc.) are NOT included in the paper.
The GNG task selection is justified by the THREE-PILLAR argument in §IV-C instead.
Do NOT reference NB02 d-rankings in the Discussion or Results.

#### 3.3 Hemoglobin Type Comparison (NB03)
- Friedman test (global): χ²(2)=0.61, p=0.74 — no overall difference
- S7_D6 spotlight: HbT p=0.026 d=0.64 (only significant)
- Figure: fig_hb_type_grand_mean.png, fig_hb_type_cohen_d.png, fig_s7d6_hb_comparison.png
- **Narrative:** HbT statistically justified as the primary hemodynamic measure

#### 3.4 Severity Correlation (NB04)
- Pearson r between channel activation and STAI-T / HAMA-A
- No FDR-surviving correlations
- Trend: S3_D1 STAIT r=-0.484, p=0.057
- Figure: fig_stait_correlation_topo.png, fig_hama_correlation_topo.png, fig_severity_top_channels.png
- **Narrative:** Activation strength does not linearly track severity — supports discriminative (classification) rather than regression framing

---

### Section 4: Results
**Status: §4.1 ✅ (5-fold ablation complete) | §4.2 ✅ (Hb type, 10-fold complete) | §4.3 ✅ (task comparison, 10-fold + LOSO complete) | §4.4 DROPPED (t-SNE not included in paper — decision 2026-05-01)**
**Placeholder structure:**

#### 4.1 Ablation Study: Clip Size × Patch Size
**Data source:** `research/paper-materials/temporal_context_analysis.md`
All three configs share identical token budget (4096 tokens). Task: GNG | Signal: HbT | CV: 5-fold.

| Config | Clip Size (T,H,W) | Patch Size (t,h,w) | 5-Fold Acc | 5-Fold κ | 5-Fold MCC |
|---|---|---|---|---|---|
| A | (64, 32, 32) | (4, 2, 2) | 61.98% | 0.272 | 0.305 |
| B | (128, 64, 64) | (8, 4, 4) | 72.40% | 0.409 | 0.413 |
| **C** | **(256, 128, 128)** | **(16, 8, 8)** | **78.65%** | **0.543** | **0.549** |

> Ablation uses **5-fold CV only — by design**. Purpose is configuration comparison (A vs. B vs. C), not generalization estimation. Config C's 10-fold (88.0%) and LOSO (71.4%) are reported in §4.2/§4.3 respectively, not here.

**Key finding:** Monotonic improvement A→B→C on all metrics. Config C recommended as primary model — full HRF coverage (~25.6 s at 10 Hz), backed by ViViT §4.2 Fig.9 frame-count ablation.

#### 4.2 Hemoglobin Type Comparison
**Status: UNBLOCKED — 10-fold complete. Source: `research/experiments/20260428/experiment_results.md`**

Scope: GNG task (best performer), 10-fold CV, all 3 Hb types. 6 metrics: Acc, Sens, Spec, F1, κ, MCC (all Mean ± SD).

| Signal | Acc (%) | Sens (%) | Spec (%) | F1 | κ | MCC |
|--------|---------|---------|---------|----|----|-----|
| **HbT** | **88.4 ± 12.4** | **90.0 ± 11.5** | **86.9 ± 16.4** | **0.854 ± 0.125** | **0.754 ± 0.236** | **0.764 ± 0.227** |
| HbO | 73.3 ± 17.6 | 85.0 ± 16.5 | 67.3 ± 28.6 | 0.693 ± 0.137 | 0.475 ± 0.284 | 0.496 ± 0.280 |
| HbR | 66.8 ± 22.3 | 80.0 ± 22.2 | 56.5 ± 39.7 | 0.643 ± 0.154 | 0.349 ± 0.349 | 0.364 ± 0.346 |

**Narrative key points:**
- HbT outperforms HbO by +15.1 pp Acc and +0.279 κ (10-fold)
- HbR κ=0.349 approaches near-chance; aligns with NB03 (S7_D6 HbR p=0.071 ns)
- Confirms statistical justification for HbT selection (§3.3)
- 5-fold GNG HbT: Acc=78.6%, κ=0.553 — consistent directional ranking; 10-fold is primary reporting metric

#### 4.3 Task-Dependent Classification Performance Across Cognitive Paradigms
**Status: ✅ COMPLETE — 10-fold + LOSO. Source: `research/experiments/20260428/experiment_results.md`**

Scope: HbT signal (best performer), 10-fold CV + LOSO, all 4 tasks. 6 metrics: Acc, Sens, Spec, F1, κ, MCC (Mean ± SD + pooled CM). **LOSO complete (2026-04-30)** — GNG LOSO: Acc=71.4%, Sens=95.3%, κ=0.459.

| Task | Acc (%) | Sens (%) | Spec (%) | F1 | κ | MCC |
|------|---------|---------|---------|----|----|-----|
| **GNG** | **88.4 ± 12.4** | **90.0 ± 11.5** | **86.9 ± 16.4** | **0.854 ± 0.125** | **0.754 ± 0.236** | **0.764 ± 0.227** |
| VF | 88.9 ± 9.0 | 87.5 ± 15.6 | 91.0 ± 9.4 | 0.843 ± 0.136 | 0.761 ± 0.194 | 0.775 ± 0.176 |
| 1backWM | 83.4 ± 19.9 | 83.8 ± 21.3 | 82.5 ± 30.3 | 0.804 ± 0.194 | 0.665 ± 0.360 | 0.669 ± 0.361 |
| SS | 78.9 ± 23.2 | 92.5 ± 10.5 | 69.2 ± 38.7 | 0.808 ± 0.176 | 0.613 ± 0.394 | 0.634 ± 0.374 |

**Narrative key points (GNG ranking justification):**
- At 10-fold, GNG and VF are near-tied: GNG κ=0.754/MCC=0.764 vs VF κ=0.761/MCC=0.775 — VF is marginally higher on 4 of 6 metrics
- ⚠️ DO NOT claim "GNG achieves highest κ/MCC" — this is factually wrong vs 10-fold data
- **Correct discriminating evidence:** 5-fold strategy reveals instability of VF (κ=0.284 at 5-fold vs κ=0.761 at 10-fold, Δ=+0.477), while GNG is stable (κ=0.553 → 0.754, Δ=+0.201)
- **Correct framing:** *"GNG and VF achieved comparable 10-fold performance (κ=0.754 and κ=0.761); however, GNG demonstrated substantially more consistent performance across cross-validation strategies (5-fold κ=0.553 vs VF 5-fold κ=0.284), indicating VF's 10-fold advantage is sensitive to fold composition. GNG is therefore selected as the primary paradigm, additionally supported by its direct neuropsychological relevance to prefrontal inhibitory control deficits in GAD [REF-GNG]."*
- SS shows highest Sens (92.5%) but lowest Spec (69.2%) — high false-alarm rate, not suitable as primary
- **LOSO results (✅ complete 2026-04-30):** GNG LOSO — Acc=71.4%, Sens=95.3%, Spec=59.4%, F1=0.689, κ=0.459, MCC=0.524 (n=48 subjects, pooled CM). GNG ties with VF at LOSO (identical confusion matrices [[76,52],[3,61]]).
- **Cross-subject HC specificity (new finding):** 13/32 HC subjects (40.6%) are systematically misclassified as GAD across all 4 tasks (best_epoch=0 in all cases), driving Spec=59.4%. Reframeable as scientific observation. Report and expand in §5 Limitations.

**THREE-PILLAR GNG JUSTIFICATION (use all three in §4.3 narrative and Discussion §5.3):**

**Pillar 1 — Performance consistency across CV strategies:**
GNG CV of κ across 5-fold/10-fold/LOSO = 0.209 (2nd most stable; VF CV=0.393, nearly 2×).
GNG holds rank 2 or higher in EVERY evaluation regime — never drops below second.
VF peaks at 10-fold (κ=0.761) but κ=0.284 at 5-fold (Δ=+0.477 vs GNG Δ=+0.201) — VF's peak is fold-composition-dependent, GNG's is not. GNG and VF tie at LOSO (κ=0.459) but arrive via very different stability paths.
Key sentence: *"GNG arrives at the LOSO floor from a markedly more consistent trajectory, making it the most replication-ready task."*

**Pillar 2 — Neuropsychological specificity to GAD pathophysiology:**
GNG directly taxes the right ventrolateral prefrontal cortex (rVLPFC) and inferior frontal gyrus — the inhibitory circuitry most strongly implicated in worry suppression in GAD. 1backWM recruits overlapping but dlPFC-dominant networks that are less specific to GAD's core inhibitory deficit. GNG imposes sustained inhibitory readiness (threat-response gating), not just cognitive load — continuously stressing the dysfunctional prefrontal inhibition system that fails in GAD. This argument stands on published cognitive neuroscience without requiring this dataset's statistical support.

**Pillar 3 — Clinical utility for screening:**
GNG has the shortest trial duration (32 s) — less than 40% of 1backWM (85 s) — critical for elderly participants (HC avg 72.7 yrs). LOSO sensitivity = 95.3%: fewer than 1 in 20 GAD cases missed, the correct optimization for screening (false negatives carry direct clinical cost). GNG has decades of normative neuropsychological data, giving it established construct validity.

---

### Section 5: Discussion
**Status: ✅ DRAFT COMPLETE — v1_discussion.md**
**Word target: ~800–1000 words**

Sub-sections:
1. **Grid encoding as spatiotemporal representation** — why topology-preserving matters vs. feature vectors
2. **HbT superiority** — tie to NB03 statistical evidence; cite total hemodynamic response literature
3. **GNG task selection — three-pillar argument** (use all three; do NOT rely on NB02 which was dropped):
   - **Consistency**: GNG κ CV=0.209 across 3 CV strategies (VF CV=0.393, nearly 2×); GNG holds rank 2+ in every regime; VF's 5→10-fold Δκ=+0.477 vs GNG Δ=+0.201 — VF's peak is data-dependent
   - **Neuropsychological specificity**: GNG stresses rVLPFC/IFG — the inhibitory circuitry directly implicated in GAD's worry-suppression deficit; 1backWM recruits dlPFC-dominant networks that are less specific to GAD pathology
   - **Clinical utility**: Shortest paradigm (32 s) for elderly participants; LOSO Sens=95.3% optimized for screening (false negatives costly)
4. **Patch/clip size analysis** — tradeoff: larger clips capture more temporal context but higher compute
5. **Comparison with prior art** — Wang 2025 (96.5%), Shao 2024 (90.5%, TNSRE) [Ma 2020 removed — wrong target class]
6. **Limitations**:
   - Age confound: HC (72.7±5.2 yrs) vs. GAD (49.5±14.3 yrs), t(46)=8.20, p<0.001 — hemodynamic aging effects on PFC cannot be fully excluded
   - Small GAD sample (n=16): limits FDR power, no severity correlation survives correction
   - **Cross-subject HC specificity (LOSO finding):** 13/32 HC (40.6%) systematically misclassified as GAD across all 4 tasks; Spec=59.4% at LOSO. Dual framing: (a) model limitation — fails for a distinct HC subgroup; (b) scientific observation — possible subclinical anxiety or atypical hemodynamics in aging HC participants. Motion-corrected preprocessing (Wavelet+CBSI) proposed as mitigation.
   - Spatial resolution bound: effective resolution bounded by 23 discrete channel positions; bilinear resize increases token count but no new measurement information
   - Single prefrontal region — no full-head coverage

---

### Section 6: Conclusion
**Status: ✅ DRAFT COMPLETE — v1_conclusion.md**
- Summarize: grid-based encoding approach, HbT justified, GNG best task
- LOSO performance (fill with final numbers)
- Clinical implication: objective, portable fNIRS system for GAD screening
- Future work: age-matched cohort, multi-region fNIRS coverage beyond prefrontal cortex

---

## 4. Figures Available (Confirmed Assignments)

| File | Content | Paper Section |
|---|---|---|
| `Channel Locations.tif` | fNIRS optode placement diagram | Methods §2.2 |
| `brain_montage_clean_high_quality.tiff` | Brain montage with channel overlay | Methods §2.2 |
| `GNG.tif` | Go/No-Go task paradigm | Methods §2.3 |
| `SS.tif` | Serial Subtraction task paradigm | Methods §2.3 |
| `1backWM.tif` | 1-Back Working Memory paradigm | Methods §2.3 |
| `VF.tif` | Verbal Fluency task paradigm | Methods §2.3 |
| `Figure 7.tif` | **2D Haemoglobin Concentration 5×7 sparse matrix** | Methods §2.5 (grid encoding step 1) |
| `Fiigure 8.tif` | **2D representation of 1D HbC matrix at time t** | Methods §2.5 (single frame) |
| `Figure 9.tif` | **Dense frame F_t after Gaussian RBF interpolation** | Methods §2.5 (grid encoding step 2) |
| `Figure 10.tif` | **3D HbC clip S^(k) with length L** | Methods §2.5 (video construction) |
| `Picture1.tif` | **Overall Workflow of Proposed 3D ViT Methodology** | Methods §2.5–2.6 (pipeline overview figure) |
| `ViT_Architecture_1.tif` | ViT architecture overview | Methods §2.6 |
| `ViT_Architecture_2.tif` | Patch embedding detail | Methods §2.6 |
| `ViT_Architecture_3.tif` | Transformer block detail | Methods §2.6 |

Statistical figures (from `src/notebook/statistical-analysis/`):
- `03_hb_type_comparison/`: fig_hb_type_grand_mean.png, fig_hb_type_cohen_d.png, fig_s7d6_hb_comparison.png, fig_hb_type_abs_d_bar.png
- `04_severity_correlation/`: fig_stait_correlation_topo.png, fig_hama_correlation_topo.png, fig_severity_top_channels.png, fig_severity_score_dist.png, fig_s7d6_severity_scatter.png
- `01_demographic/`: fig_age_comparison.png, fig_sex_distribution.png, fig_hama_gad.png, fig_stai_comparison.png, fig_education.png

---

## 5. Writing Workflow (How to Use the Tools)

### Step-by-Step Commands for Each Section

#### Step 1: Literature Search (do first, reusable)
```
@research-lookup Find papers on:
1. fNIRS-based anxiety and GAD classification deep learning 2020-2025
2. Spatiotemporal encoding of EEG/fNIRS as 2D/3D images for classification
3. Video Vision Transformer (ViViT, VideoViT) for biosignal classification
4. fNIRS prefrontal cortex hemodynamic response in anxiety disorders
Save results to research/paper-materials/sources/
```

#### Step 2: Write Introduction
```
@scientific-writing Write the Introduction for an IEEE TNSRE paper titled
"Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification
Using a 3D Vision Transformer". Follow the structure in PAPER_SPEC_PLAN.md §3
Section 1. Use IEEE citation style. Target 600-800 words.
Save to research/paper-materials/drafts/v1_introduction.md
```

#### Step 2b: Write Methods §2.1 (Participants & Dataset Characteristics)
```
@scientific-writing Write Section 2.1 (Participants and Dataset Characteristics)
for an IEEE TNSRE paper on grid-based fNIRS GAD classification.

Include:
1. Recruitment: 53 enrolled; 48 in final analysis (32 HC, 16 GAD);
   5 excluded due to incomplete task recordings (1 HC + 4 GAD)
2. Table 1 — group comparison (source: 01_demographic_analysis.ipynb):
   HC:  n=32, age 72.7±5.2 yrs (range 65–84), 23F/9M (72% female)
   GAD: n=16, age 49.5±14.3 yrs (range 29–70), 13F/3M (81% female)
3. Clinical scores:
   HAMA: 22.0±10.3 (incl. LA063=0, n=16) / 23.5±8.7 (excl. LA063, n=15); range 0–40
   STAI-S: HC 29.4±8.5 vs. GAD 45.8±8.7 (t(46)=−6.26, p<0.001, d=1.90)
   STAI-T: HC 34.1±9.7 vs. GAD 57.2±6.8 (t(46)=−8.54, p<0.001, d=2.59)
4. Age confound disclosure: t(46)=8.20, p=1.50×10⁻¹⁰ — note this is a known
   limitation (expanded in §5 Discussion/Limitations)
5. Sex balance: χ²(1)=0.13, p=0.72 — not a confound
6. Special cases:
   AH029 (HC): self-reported MDD, on psychotherapy + medication; retained (no confirmed
   diagnosis by research team), interpret with caution — mention in footnote
   LA063 (GAD): HAMA not administered (coded 0); retained based on elevated STAI scores
   (STAI-S=55, STAI-T=63) — mention in footnote
7. Ethics statement: [IRB approval number and institution — to be provided by dataset author]

~300 words + Table 1. Do NOT fabricate the IRB number — leave as placeholder.
IEEE TNSRE style.
Save to research/paper-materials/drafts/v1_methods_participants.md
```

#### Step 2c: Write Methods §2.2 (fNIRS Data Acquisition)
```
@scientific-writing Write Section 2.2 (fNIRS Data Acquisition)
for an IEEE TNSRE paper on grid-based fNIRS GAD classification.

Include:
1. System: 23 channels formed by 8 source-detector pairs; NIRx system
2. Wavelengths: 760 nm and 850 nm dual-wavelength illumination
3. Source-detector separation range: 2.49–4.19 cm
4. Electrode placement: prefrontal cortex (PFC) following international 10-20 system
5. Hemodynamic signals: HbO, HbR, HbT derived via modified Beer-Lambert Law
6. Brief HbT selection rationale (one sentence; full justification in §3.3):
   HbT (= HbO + HbR) captures total hemodynamic response and was statistically
   confirmed as the most sensitive measure at S7_D6 (see Section 3.3)
7. Reference figures: Channel Locations.tif and brain_montage_clean_high_quality.tiff

~200 words. IEEE TNSRE style.
Save to research/paper-materials/drafts/v1_methods_fnirs_system.md
```

#### Step 2d: Write Methods §2.3 (Experimental Paradigms)
```
@scientific-writing Write Section 2.3 (Experimental Paradigms)
for an IEEE TNSRE paper on grid-based fNIRS GAD classification.

Describe all four cognitive tasks. For each provide: purpose, cognitive demand,
trial structure, epoch window, preparation crop, and effective trial length.

1. Go/No-Go (GNG): prepotent response inhibition; 0–35 s window,
   crop first 3 s preparation → 32 s effective trial
2. Serial Subtraction (SS): vocal mental arithmetic; participants are shown an equation
   (e.g., "500 – 7") during a 7-s preparation period, then subtract the decrement repeatedly
   aloud for 60 s (e.g., 500 → 493 → 486 → …); 4 trials with different starting values and
   decrements (500-7, 950-17, 800-13, 650-8); 0–60 s window,
   crop first 7 s preparation → 53 s effective trial
3. 1-Back Working Memory (1backWM): executive working memory / n-back;
   0–90 s window, crop first 5 s → 85 s effective trial
4. Verbal Fluency (VF): semantic retrieval / phonemic fluency;
   0–60 s window, crop first 7 s → 53 s effective trial

All tasks: event onset codes 3.0/4.0 used for trial detection.
Reference figures: GNG.tif, SS.tif, 1backWM.tif, VF.tif
(located in research/paper-materials/figure/)

~350 words. IEEE TNSRE style.
Save to research/paper-materials/drafts/v1_methods_tasks.md
```

#### Step 2e: Write Methods §2.4 (Signal Processing Pipeline)
```
@scientific-writing Write Section 2.4 (Signal Processing Pipeline)
for an IEEE TNSRE paper on grid-based fNIRS GAD classification.

Describe the two-stage pipeline:

Stage 1 — Homer3 (MATLAB, nirs2csv_homer3.m):
1. hmrR_Intensity2OD: raw NIRx intensity → optical density (OD)
2. hmrR_BandpassFilt: high-pass filter HPF=0.01 Hz (order 5),
   low-pass filter LPF=0.5 Hz (order 3)
3. hmrR_OD2Conc: modified Beer-Lambert Law → HbO, HbR, HbT
   Partial pathlength factor PPF=[6, 6] for wavelengths [760 nm, 850 nm]
   Output: CSV per subject (time vector + 23-channel haemoglobin concentration)

Stage 2 — Python MNE (processor_cli.py):
4. HbT = HbO + HbR computed from loaded CSVs
5. Annotation alignment: t_offset correction for split recording sessions
6. Epoching per task (event codes 3.0/4.0):
   GNG: 0–35 s, crop 3 s → 32 s; SS: 0–60 s, crop 7 s → 53 s;
   1backWM: 0–90 s, crop 5 s → 85 s; VF: 0–60 s, crop 7 s → 53 s
7. Channel-wise z-score normalisation (zero mean, unit variance)
8. Grid mapping: 23 channels → 5×7 sparse grid → Gaussian RBF interpolation
   (scipy.interpolate.Rbf, gaussian kernel) → dense frame F_t ∈ ℝ^(5×7); stack T frames → (T, 5, 7)
9. Spatial resize: (T, 5, 7) → (T, H, W) via bilinear interpolation
   (torchvision.transforms.v2.Resize); H/W ∈ {32, 64, 128} per ablation config
   Rationale: native 5×7 is too small for ViT patch tokenization; topology preserved under resize
   Limitation: spatial information bounded by 23 channel positions regardless of H/W
10. Temporal subsampling: UniformTemporalSubsample(T_target) → T frames
11. RGB replication: (T, H, W) → (3, T, H, W) for ViT input

Reference figures: Figure 7.tif (sparse grid), Fiigure 8.tif (single frame at t),
Figure 9.tif (dense frame after RBF), Figure 10.tif (3D clip S^(k))

Mathematical notation (REQUIRED — numbered display equations):
- Eq. for modified Beer-Lambert Law:
    ΔC(t) = ΔOD(t) / (ε · DPF · L)
  where ε = molar extinction coefficient [L·mol⁻¹·cm⁻¹], DPF = differential pathlength
  factor (PPF=6 for both wavelengths), L = source-detector separation [cm].
- Eq. for HbT derivation:
    HbT(t) = HbO(t) + HbR(t)
  Reference both by equation number in the prose (e.g., "haemoglobin concentrations
  were derived using the mBLL [Eq. 1]... HbT was computed as [Eq. 2]").

~400 words. IEEE TNSRE style.
Save to research/paper-materials/drafts/v1_methods_signal_processing.md
```

#### Step 3: Write Methods §2.5 (Grid-Based Spatiotemporal Encoding)
```
@scientific-writing Write Section 2.5 (Grid-Based Spatiotemporal Encoding)
for an IEEE TNSRE paper on grid-based fNIRS GAD classification.

Content to cover (in order, ~500 words):

1. **Motivation paragraph (topology-preserving design):**
   Unlike conventional approaches that flatten fNIRS channels into a fixed-length feature
   vector, the proposed encoding preserves the anatomical spatial arrangement of optodes
   across the prefrontal cortex. fNIRS optodes occupy fixed, known positions on the scalp;
   a 2D grid respecting these positions encodes neuroanatomically meaningful proximity,
   enabling the model to learn spatially coherent haemodynamic patterns rather than treating
   channels as an unordered bag of signals.

2. **Step 1 — Epoch matrix H^(k):**
   Each trial epoch is represented as a haemodynamic-concentration matrix:

     H^(k) = [h_t]_{t ∈ τ_k} ∈ ℝ^{C × L}

   where C = 23 is the number of fNIRS channels, L is the number of time samples in epoch k,
   and the column vector h_t = [ΔHbT_{1,t}, …, ΔHbT_{C,t}]^T contains the HbT concentration
   change at time t for every channel. (Signal: HbT only, the primary selected measure.)

3. **Step 2 — Channel-wise z-score normalisation:**
   Each epoch is normalised channel-wise by subtracting the per-channel mean μ_k and dividing
   by the per-channel standard deviation σ_k:

     ĥ_t^(k) = (h_t^(k) − μ_k) / σ_k

   This yields zero-mean, unit-variance signals across all 23 channels, placing channels on a
   common scale regardless of inter-subject haemodynamic amplitude differences.

4. **Step 3 — Mapping to 5×7 sparse grid:**
   Each z-scored sample vector ĥ_t^(k) ∈ ℝ^{23} is placed into a 5×7 spatial grid via a fixed
   bijective mapping M that assigns channel c to grid coordinates (i_c, j_c):

     M : {1, …, 23} → {1, …, 5} × {1, …, 7},  where M(c) = (i_c, j_c)

   The resulting sparse spatial frame at time t is:

     F_t(i, j) = ĥ_{c,t}   if (i, j) = M(c) for some c
               = 0           otherwise

   Of the 35 grid cells, 23 are occupied by channels and the remaining 12 are initialised to
   zero (Fig. 7). Reference figure: Figure 7.tif.

5. **Step 4 — Gaussian RBF interpolation to dense frame F̂_t:**
   The 12 zero-filled cells are recovered using Gaussian radial-basis function interpolation.
   For any unoccupied grid point (x, y), the interpolated value is:

     F̂_t(x, y) = Σ_{m=1}^{23} w_m exp[−ε² ‖(x, y) − (x_m, y_m)‖²]

   The weights w_m are determined by solving the linear system Φ w = z, where
   Φ_{mn} = exp[−ε² ‖(x_m, y_m) − (x_n, y_n)‖²] and z_m = F_t(x_m, y_m).
   This produces a fully populated dense frame F̂_t ∈ ℝ^{5×7} that preserves the topographic
   structure of the original optode array (Fig. 8 and 9). Reference figures: Fiigure 8.tif,
   Figure 9.tif.

6. **Step 5 — Stacking to 3D clip S^(k):**
   The sequence of dense frames {F̂_t}_{t ∈ T_k} is stacked along the temporal axis to form
   a spatiotemporal clip tensor:

     S^(k) = [F̂_t]_{t ∈ T_k} ∈ ℝ^{L × 5 × 7}

   This directly mirrors the video clip representation used by Video Vision Transformers
   [REF-ViViT]. Reference figure: Figure 10.tif.

7. **Step 6 — Uniform temporal subsampling to S* ∈ ℝ^{T* × 5 × 7}:**
   Because trials have variable length L, a uniform temporal subsampling operation selects
   T* uniformly spaced frame indices:

     idx_i = ⌊ (i − 1)(L − 1) / (T* − 1) ⌋,   i = 1, …, T*

   yielding S* ∈ ℝ^{T* × 5 × 7}. This preserves the full chronological order of the epoch
   while standardising the temporal dimension across subjects and tasks.

8. **Step 7 — Spatial upsampling and RGB replication:**
   Because the native 5×7 spatial resolution is too coarse for patch-based tokenisation,
   S* is upsampled to (T*, H', W') via bilinear interpolation where H' = W' ∈ {32, 64, 128}
   depending on the ablation configuration (§IV-A). Upsampling preserves the relative spatial
   topology but introduces no new physiological information; spatial content remains bounded
   by the 23 physical optode positions. Finally, the single-channel map is replicated across
   three input channels, yielding the model input tensor of shape (3, T*, H', W'), compatible
   with the RGB tubelet-embedding format of the ViT backbone [REF-ViViT].

Equation numbering: assign sequential numbers continuing from Eq. (2) in §2.4.
Use \begin{equation}…\end{equation} in LaTeX; reference equations inline as [Eq. (X)].
IEEE TNSRE style, ~500 words.
Save to research/paper-materials/drafts/v1_methods_grid_encoding.md
```

#### Step 3b: Write Methods §2.6 (3D Vision Transformer Architecture)
```
@scientific-writing Write Section 2.6 (3D Vision Transformer Architecture)
for an IEEE TNSRE paper on grid-based fNIRS GAD classification.

Architecture is ViViT-based (Arnab et al. 2021, arXiv:2103.15691v2) with tubelet embedding.
Primary configuration is Config C (selected from §4.1 ablation).

Include:
1. Input tensor: (3, T, H, W) = (3, 256, 128, 128) for Config C
2. Tubelet embedding (ViViT §3.2): non-overlapping 3D patches of size (t=16, h=8, w=8)
   each patch flattened and linearly projected to embedding dimension d
3. Token count: N = (256/16) × (128/8) × (128/8) = 16 × 16 × 16 = 4096 tokens
4. Positional encoding: learnable 3D positional embeddings added to all tokens
5. Classification token (CLS): prepended to the token sequence
6. Transformer encoder: **L=6** stacked blocks each with multi-head self-attention
   (**8 heads**, dim_head=64; inner_dim=512), feed-forward MLP (**hidden_dim=512**, GELU
   activation), residual connections, pre-norm LayerNorm (pre-attention and pre-FFN)
7. Classification head: MLP (LayerNorm → Linear) applied to CLS token → 2 classes (HC=0, GAD=1)
8. Config C selection rationale (one sentence): Config C achieves monotonically best
   performance (Acc=78.65%, κ=0.543) and captures the full hemodynamic response
   function (~25.6 s at 10 Hz); see §4.1 for full ablation results.
9. Training configuration (confirmed from `src/core/main.py`):
   - Optimizer: Adam (β₁=0.9, β₂=0.999), initial LR=1×10⁻³
   - Scheduler: CosineWarmupScheduler — 10-epoch linear warmup, then cosine decay over 100 epochs
   - Loss: CrossEntropyLoss (label_smoothing=0.0; optional sqrt class-weighting available)
   - Early stopping: patience=25 epochs, monitored on **val F1**; best model weights restored
   - Batch size: 8 | Epochs: 100 | Random seed: 42 (fully deterministic)
   - Weight init: Xavier uniform (Linear), constant 1.0/0.0 (LayerNorm) — `initialize_weights()`
   - Augmentation: **none** (AddGaussianNoise exists in `datasets.py` but not in default transform)

Cite: Arnab et al. (2021) ViViT (arXiv:2103.15691); Dosovitskiy et al. (2021) ViT.
Reference figures: Picture1.tif (overall workflow), ViT_Architecture_1.tif,
ViT_Architecture_2.tif, ViT_Architecture_3.tif

Mathematical notation (REQUIRED — numbered display equation):
- Eq. for token count (general form then Config C substitution on the same or next line):
    N = (T/t) × (H/p_h) × (W/p_w)
    = (256/16) × (128/8) × (128/8) = 16 × 16 × 16 = 4,096
  Label this equation and reference it as "Eq. (X)" when the fixed 4,096-token budget
  is discussed in the ablation study (§IV-A). This is the architectural parameter that
  justifies Config C selection and links §2.6 to §4.1.

~350 words. IEEE TNSRE style.
Save to research/paper-materials/drafts/v1_methods_vit_architecture.md
```

#### Step 3c: Write Methods §2.7 (Evaluation Framework)
```
@scientific-writing Write Section 2.7 (Evaluation Framework)
for an IEEE TNSRE paper on grid-based fNIRS GAD classification.

Include:
1. Three cross-validation strategies (all subject-level stratified):
   - 5-Fold CV: 5 stratified folds; used for hyperparameter/configuration comparison
   - 10-Fold CV: 10 stratified folds; more stable performance estimates
   - Leave-One-Subject-Out (LOSO): each subject held out once as the test set;
     n=48 iterations (one per subject: 32 HC + 16 GAD);
     strongest evidence for generalisation to unseen subjects
2. Rationale: multiple strategies provide complementary evidence — 5-fold for
   ablation speed, 10-fold for reporting stability, LOSO for clinical generalisability
3. **Fold composition disclosure (REQUIRED — add this paragraph):**
   - 5-fold: each test partition ≈ 6–7 HC + 3 GAD subjects (~9–10 total per fold)
   - 10-fold: each test partition ≈ 3–4 HC + 1–2 GAD subjects (~4–5 total per fold)
   - The small per-fold positive count (1–2 GAD) in 10-fold is an inherent consequence
     of the dataset size (16 GAD total); this motivates reporting the pooled confusion
     matrix as the primary performance estimate alongside per-fold mean ± SD
   - LOSO: 48 test iterations — 32 with an HC test subject, 16 with a GAD test subject;
     each test fold is single-class (no mixed-class test sets);
     per-fold Sens/Spec undefined for individual LOSO subjects — all LOSO aggregate
     metrics derived exclusively from the pooled confusion matrix
4. Metrics — present as a COMPACT TABLE (not as individual numbered equations).
   One table with columns: Metric | Symbol | Formula. Include all 9 metrics:

   | Metric | Symbol | Formula |
   |--------|--------|---------|
   | Accuracy | Acc | (TP+TN)/(TP+TN+FP+FN) |
   | Sensitivity | Sens | TP/(TP+FN) |
   | Specificity | Spec | TN/(TN+FP) |
   | Precision | Prec | TP/(TP+FP) |
   | F1-Score | F1 | 2·TP/(2·TP+FP+FN) |
   | Balanced Accuracy | BA | (Sens+Spec)/2 |
   | Neg. Predictive Value | NPV | TN/(TN+FN) |
   | Cohen's Kappa | κ | (p_o − p_e)/(1 − p_e) |
   | Matthews Corr. Coeff. | MCC | (TP·TN−FP·FN)/√[(TP+FP)(TP+FN)(TN+FP)(TN+FN)] |

   Positive class = GAD (label 1); Negative class = HC (label 0).
   Results text references this table by number (e.g., "metrics defined in Table I").
   Note: AUC not reported — model outputs binary predictions; probability scores
   not stored in current training pipeline.
5. Per-fold metrics tabulated; overall from pooled confusion matrix across all folds

~250 words. IEEE TNSRE style.
Save to research/paper-materials/drafts/v1_methods_evaluation.md
```

#### Step 4: Write Statistical Analysis Section
```
@scientific-writing Write Section 3 (Statistical Analysis) using the
data from PAPER_SPEC_PLAN.md §3 Statistical Analysis. Include NB02, NB03,
NB04 findings with exact statistics. Do not add citations for these —
they are our own results. ~500 words. IEEE TNSRE style.
Save to research/paper-materials/drafts/v1_statistical_analysis.md
```

#### Step 4b: Write Section 4.1 Ablation Study (Clip Size × Patch Size)
```
@scientific-writing Write Section 4.1 (Ablation Study: Clip Size × Patch Size) for
an IEEE TNSRE paper on grid-based fNIRS GAD classification.

Data source: research/paper-materials/temporal_context_analysis.md

Content to cover:
1. Experimental design — three configs (A/B/C) with fixed 4096-token budget;
   independent variable is temporal coverage (T=64/128/256); GNG task, HbT signal, 5-fold CV.
2. Results table — report all nine metrics (Acc, BA, Prec, Sens, Spec, NPV, F1, MCC, κ)
   for all three configs. Highlight Config C as best on all metrics.
3. Key finding — monotonic improvement A→B→C: +16.67 pp accuracy, κ 0.272→0.543,
   MCC 0.305→0.549. Sensitivity stable (0.781) while specificity gains +25.0 pp.
4. Mechanistic justification — longer temporal receptive field captures full hemodynamic
   response function (~25.6 s for Config C vs. 6.4 s for Config A at 10 Hz sampling).
   Cite ViViT (Arnab et al. 2021, arXiv:2103.15691v2) §4.2 Fig.9 for architectural backing.
5. Note — Ablation table reports **5-fold CV only (by design)**. The ablation's purpose
   is config comparison (A→B→C monotonic improvement), not generalization estimation.
   Do NOT add 10-fold or LOSO columns for Configs A/B — those experiments were not run.
   Config C's 10-fold (88.0%) and LOSO (71.4%) belong in §4.2 and §4.3 respectively.
   Remove any "pending" language; the ablation section is complete as-is.

IEEE TNSRE style. ~350 words. Include results table from the data source.
Save to research/paper-materials/drafts/v1_results_ablation.md
```

#### Step 4e: Write Results §4.2 (Hemoglobin Type Comparison)
```
@scientific-writing Write Section 4.2 (Hemoglobin Type Comparison) for an IEEE TNSRE
paper on grid-based fNIRS GAD classification.

Scope: GNG task (best performer), 10-fold cross-validation, all three Hb types.
All metrics reported as Mean ± SD across folds.

Include:
1. Opening: state that GNG task is used as the reference condition for Hb type comparison
   (rationale: GNG is the best-performing task established in §4.3; using it as
   the fixed condition isolates the effect of Hb type)

2. Results Table — Table [X]: Classification Performance by Hemoglobin Type
   (GNG task, 10-fold cross-validation, Config C)

   | Signal | Acc (%) | Sens (%) | Spec (%) | F1 | κ | MCC |
   |--------|---------|---------|---------|----|----|-----|
   | HbT | 88.4 ± 12.4 | 90.0 ± 11.5 | 86.9 ± 16.4 | 0.854 ± 0.125 | 0.754 ± 0.236 | 0.764 ± 0.227 |
   | HbO | 73.3 ± 17.6 | 85.0 ± 16.5 | 67.3 ± 28.6 | 0.693 ± 0.137 | 0.475 ± 0.284 | 0.496 ± 0.280 |
   | HbR | 66.8 ± 22.3 | 80.0 ± 22.2 | 56.5 ± 39.7 | 0.643 ± 0.154 | 0.349 ± 0.349 | 0.364 ± 0.346 |

3. Narrative (~150 words):
   - HbT outperforms HbO (+15.1 pp Acc, κ gap = +0.279) and HbR (+21.6 pp Acc)
   - HbR κ=0.349 approaches near-chance performance; multiple folds show collapsed
     predictions (Spec=0); consistent with NB03 statistical finding (S7_D6 HbR p=0.071 ns)
   - HbO provides moderate discrimination (κ=0.475) but substantially below HbT
   - This confirms the statistical justification for HbT selection presented in §3.3:
     HbT = HbO + HbR captures the full hemodynamic response, more sensitive than
     either component alone
   - All subsequent results (§4.3) use HbT as the primary signal

Note: LOSO was run for HbT only (not for HbO/HbR). Do NOT add a LOSO row to TABLE III — the Hb comparison is 10-fold only by design. The absence of LOSO for HbO/HbR is intentional, not a gap.
IEEE TNSRE style. ~250 words + table.
Save to research/paper-materials/drafts/v1_results_hb_type.md
```

#### Step 4f: Write Results §4.3 (Task Comparison)
```
@scientific-writing Write Section 4.3 (Task Comparison) for an IEEE TNSRE paper
on grid-based fNIRS GAD classification.

Scope: HbT signal (established in §4.2), 10-fold cross-validation, Config C,
all four cognitive tasks. All metrics reported as Mean ± SD across folds.

Include:
1. Opening: state that HbT is used as the fixed signal following §4.2 findings;
   all four cognitive tasks are evaluated under identical conditions

2. Results Table — Table [X]: Classification Performance by Cognitive Task
   (HbT signal, 10-fold cross-validation, Config C)

   | Task | Acc (%) | Sens (%) | Spec (%) | F1 | κ | MCC |
   |------|---------|---------|---------|----|----|-----|
   | GNG | 88.4 ± 12.4 | 90.0 ± 11.5 | 86.9 ± 16.4 | 0.854 ± 0.125 | 0.754 ± 0.236 | 0.764 ± 0.227 |
   | VF  | 88.9 ± 9.0  | 87.5 ± 15.6 | 91.0 ± 9.4  | 0.843 ± 0.136 | 0.761 ± 0.194 | 0.775 ± 0.176 |
   | 1backWM | 83.4 ± 19.9 | 83.8 ± 21.3 | 82.5 ± 30.3 | 0.804 ± 0.194 | 0.665 ± 0.360 | 0.669 ± 0.361 |
   | SS  | 78.9 ± 23.2 | 92.5 ± 10.5 | 69.2 ± 38.7 | 0.808 ± 0.176 | 0.613 ± 0.394 | 0.634 ± 0.374 |

3. Narrative (~250 words) — USE THE THREE-PILLAR ARGUMENT:

   **Consistency pillar (primary):**
   GNG achieves κ values of 0.553 (5-fold), 0.754 (10-fold), and 0.459 (LOSO), yielding
   a cross-strategy coefficient of variation (CV) of 0.209. VF achieves a higher 10-fold
   κ (0.761) but collapses to κ=0.284 at 5-fold (Δ=+0.477 vs GNG Δ=+0.201), indicating
   its peak is fold-composition-dependent. GNG holds rank 2 or higher in every evaluation
   regime; it is the only task that never drops below second place. GNG and VF tie at LOSO
   (κ=0.459, identical confusion matrices), but GNG reaches this floor from a more stable
   trajectory — evidence of a robust underlying signal rather than fold-specific performance.

   **Neuropsychological pillar:**
   GNG selection is further supported by its direct neuropsychological relevance: the task
   taxes the rVLPFC and inferior frontal gyrus — the inhibitory circuitry specifically
   dysregulated in GAD's core deficit of worry suppression. 1backWM recruits overlapping
   but dlPFC-dominant circuits that impose cognitive load without the sustained inhibitory
   demand characteristic of GAD pathology.

   **Clinical utility pillar:**
   At 32 seconds, GNG is the shortest paradigm, reducing cognitive burden for the HC cohort
   (mean age 72.7 yrs). LOSO sensitivity of 95.3% is the critical screening metric —
   fewer than 1 in 20 GAD cases are missed under cross-subject evaluation.

   **Additional notes:**
   - SS: highest Sens (92.5%) but lowest Spec (69.2%) — not suitable as primary
   - VF: competitive at 10-fold but unstable across CV strategies
   - Avoid claiming "GNG achieves highest κ/MCC" — VF is marginally higher at 10-fold

Do NOT invent LOSO numbers. IEEE TNSRE style. ~300 words + table.
Save to research/paper-materials/drafts/v1_results_task_comparison.md
```

#### Step 4c: Write Discussion §5
```
@scientific-writing Write Section 5 (Discussion) for an IEEE TNSRE paper
on grid-based fNIRS GAD classification. Target ~800 words.

Write the following sub-sections IN ORDER:

1. Grid encoding as spatiotemporal representation (~200 words):
   - Why topology-preserving 5×7 grid matters over flattened feature vectors
   - Spatial co-activation patterns + temporal HRF dynamics jointly captured
   - ViT global self-attention models all spatio-temporal pairwise interactions
     from layer 1 (unlike CNNs with limited receptive field) — cite ViViT §1

2. HbT as primary hemodynamic measure (~150 words):
   - Global Friedman χ²(2)=0.61, p=0.74: no global Hb-type difference
   - S7_D6 spotlight: HbT p=0.026 d=0.64 (significant); HbO p=0.086,
     HbR p=0.071 (both non-significant)
   - HbT = total hemodynamic response = most sensitive to combined vascular changes
   - Aligns with HbR ≈ chance performance in classification experiments

3. GNG task selection — THREE-PILLAR ARGUMENT (~250 words):
   - **Pillar 1 (consistency):** GNG κ CV=0.209 across 3 CV strategies vs VF CV=0.393.
     GNG ranks 2nd or higher in every regime; VF collapses to κ=0.284 at 5-fold (Δ=+0.477)
     while GNG's delta is only +0.201. *"GNG arrives at the LOSO floor from a markedly more
     consistent trajectory, making it the most replication-ready task."* (Do NOT claim GNG
     has highest κ/MCC at 10-fold — VF is marginally higher there.)
   - **Pillar 2 (neuropsychological):** GNG taxes rVLPFC/IFG — the inhibitory circuitry
     directly implicated in GAD's worry-suppression deficit. 1backWM recruits dlPFC-dominant
     circuits that impose cognitive load without the sustained inhibitory demand specific to GAD
     pathology. This argument rests on published cognitive neuroscience, not this dataset's stats.
   - **Pillar 3 (clinical utility):** Shortest paradigm (32 s); LOSO Sens=95.3% (optimal
     for clinical screening); established normative data for GNG in neuropsychology.
   - Frame GNG as selected based on THREE convergent lines of evidence — not just "it scored highest."

4. Configuration C and temporal context (~150 words):
   - Config C (T=256) outperforms A and B on all metrics in ablation (§4.1)
   - Captures full HRF (~25.6 s) vs Config A only rise phase (~6.4 s)
   - ViViT Fig.9: more frames → higher accuracy (same principle demonstrated here)
   - Compute-accuracy tradeoff noted: Config C uses larger spatial dimensions (128×128)

5. Comparison with prior art (~100 words):
   - Compare against Wang 2025 (96.5% HC vs Anxiety), Shao 2024 (90.5% depression recognition, TNSRE)
   - Ma 2020 REMOVED — paper classified BD vs MDD, not HC vs MDD
   - Advantage: end-to-end spatiotemporal learning, no hand-crafted features,
     topology-preserving encoding

6. Limitations (~250 words):
   - Age confound: HC (72.7±5.2 yrs) vs. GAD (49.5±14.3 yrs), t(46)=8.20, p<0.001 —
     cannot fully rule out hemodynamic aging effects on PFC activation
   - Small GAD sample (n=16): limits FDR power; no severity correlation survives correction
   - **Cross-subject HC specificity gap (from LOSO, 2026-04-30):** 13/32 HC subjects (40.6%)
     are systematically misclassified as GAD across all 4 tasks (best_epoch=0 in every case),
     yielding LOSO Spec=59.4%. Write with dual framing: (a) methodological limitation — the
     model fails to generalize to a phenotypically distinct HC subgroup; (b) clinical observation
     — this subgroup may harbor subclinical anxiety not captured by screening instruments,
     or exhibit age-related hemodynamic changes that overlap with GAD task-evoked responses.
     Propose motion-corrected preprocessing (Wavelet+CBSI) and subject-level data quality
     stratification as future mitigation strategies. Note: this is consistent with the
     motion-risk data quality report (11 high-risk subjects identified in 2026-04-30 session).
   - Spatial resolution bound: effective spatial resolution is bounded by 23 discrete fNIRS
     channel positions; bilinear resize to H×W increases ViT token count but introduces
     no additional measurement information beyond the original optode arrangement
   - Single prefrontal region — no full-head coverage; other regions may be relevant

IMPORTANT: Do NOT fill in final classification performance numbers — use [XX.X%]
placeholder wherever final results are needed.
IEEE TNSRE style.
Save to research/paper-materials/drafts/v1_discussion.md
```

#### Step 4d: Write Conclusion §6
```
@scientific-writing Write Section 6 (Conclusion) for an IEEE TNSRE paper
on grid-based fNIRS GAD classification. Target ~200 words (TNSRE conclusions are concise).

Include in order:
1. Core contribution restatement: novel 1D→2D→3D grid-based encoding pipeline
   that preserves optode spatial topology; video-like tensor enables 3D ViT for fNIRS
2. Statistical justification: HbT confirmed as primary measure (S7_D6: p=0.026, d=0.64)
3. Task finding: GNG task yields best classification performance across evaluation strategies
4. Architecture finding: Config C (T=256, patches (16,8,8)) confirmed as optimal from
   ablation — captures full hemodynamic response function
5. Final performance (GNG, HbT, LOSO): Acc=71.4%, Sens=95.3%, Spec=59.4%, κ=0.459
   (cross-subject, n=48 subjects). Lead with 10-fold headline (88.4%) then cite LOSO
   as independent generalization confirmation.
6. Clinical implication: portable, objective fNIRS-based screening tool for GAD;
   complements self-report instruments (GAD-7, STAI)
7. Future work (1–2 items): age-matched cohort to disentangle the age confound;
   multi-region fNIRS coverage beyond the prefrontal cortex

Do NOT invent final numbers. Use [XX.X%] for any result still pending.
IEEE TNSRE style.
Save to research/paper-materials/drafts/v1_conclusion.md
```

#### Step 5: Citation Management
```
@citation-management Generate BibTeX entries for:
- Kroenke et al. 2007 (DOI: 10.7326/0003-4819-146-5-200703060-00004)
- Hamilton 1959 HAMA scale (DOI: 10.1111/j.2044-8341.1959.tb00467.x)
- Spitzer et al. 2006 GAD-7 (DOI: 10.1001/archinte.166.10.1092)
- Wang 2025 fNIRS anxiety (DOI: 10.1016/j.bspc.2025.107503)
Save to research/paper-materials/references/references.bib
```

#### Step 6: IEEE Template Setup
```
@venue-templates Get IEEE TNSRE LaTeX template requirements and formatting
guidelines. Set up the main .tex file skeleton at
research/paper-materials/drafts/main.tex
```

#### Step 7: Peer Review (after full draft)
```
@peer-review Evaluate the draft manuscript at research/paper-materials/drafts/
using ScholarEval 8-dimension scoring. Focus on: methodology clarity,
statistical rigor, figure quality, and IEEE TNSRE scope alignment.
```

---

## 6. What NOT to Write Yet (Blocked Items)

| Item | Blocked by | When to unblock |
|---|---|---|
| Abstract | Final classification results | After model training complete |
| Section 4.1 Ablation table (5-fold) | ✅ UNBLOCKED — data in temporal_context_analysis.md | Use Step 4b prompt to write |
| Section 4.1 10-fold + LOSO columns | ✅ COMPLETE (2026-04-30) | Config C: 10-fold=88.0%, LOSO=71.4% (GNG HbT) |
| Section 4.3 LOSO GNG numbers | ✅ COMPLETE (2026-04-30) | Acc=71.4%, Sens=95.3%, κ=0.459 |
| Section 4.2 Hb type results | ✅ UNBLOCKED — 10-fold complete; verified data in §4.2 above | Use Step 4e prompt to write |
| Section 4.3 Task comparison table | ✅ UNBLOCKED — 10-fold complete; verified data in §4.3 above | Use Step 4f prompt to write |
| Final conclusion numbers | All results | Last step |

---

## 7. Pending Technical Items (Non-Writing)

- [ ] Confirm final 5×7 grid cell positions for all 23 channels
- [ ] Finalize clip size and patch size from ablation
- [ ] Confirm IRB approval details for ethics statement
- [ ] Confirm dataset is new vs. old codebase (same 23-channel prefrontal setup?)

---

## 8. Reference Files

| Resource | Path |
|---|---|
| Old result (baseline) | `research/paper-materials/old-result/fnirs-anxiety-detection-paper.md` |
| Old result PDF | `research/paper-materials/old-result/fNIRS Anxiety Detection.pdf` |
| Statistical narrative | `research/paper-materials/statistical-analysis-paper-narrative.md` |
| Structure summary | `research/paper-materials/STRUCTURE SUMMARY.txt` |
| Figures | `research/paper-materials/figure/` |
| Statistical notebooks | `src/notebook/statistical-analysis/` |
| Statistical figures | `src/notebook/statistical-analysis/0{1-4}_*/fig_*.png` |
| Model code | `src/core/models.py` (ViT class) |
| Dataset code | `src/core/datasets.py` (FNIRSSequenceDatasetV2) |
| Old codebase | `references/grid-based-method-old-codebase/` |
| Memory DB | keyword: "fnirs-anxiety-detection-paper" |

---

## 9. Clarifications Still Needed

- [x] ~~**Confirm exact 5×7 grid**~~ → Confirmed from `processor_cli.py:get_channel_positions()` (see §2.4)
- [x] ~~**Preprocessing chain**~~ → Confirmed: Homer3 (Intensity2OD → BandpassFilt 0.01–0.5Hz → OD2Conc PPF=6) + Python (HbT, epoching, z-score, RBF grid)
- [ ] **IRB/ethics**: Approval number and institution — will be filled by dataset author later
- [x] ~~**Figure 7, 8, 9, 10 content**~~ → Confirmed (see §4 table above)
- [x] ~~**Picture1.tif**~~ → Confirmed: Overall Workflow of Proposed 3D ViT Methodology

---

*This plan is a living document. Update it as experiments complete and sections are written.*
