# Paper Specification & Writing Plan
**fNIRS Grid-Based Method — IEEE TNSRE Submission**
**Last updated: 2026-04-28**

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
| Go/No-Go | GNG | **Best classifier** (LOSO 97.6%, sensitivity 100%) |
| Stop-Signal | SS | Secondary |
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
| **Clip size** (T, H, W) | (64, 32, 32) / (128, 64, 64) / (256, 128, 128) |
| **Patch size** (t, h, w) | (4, 2, 2) / others under experimentation |
| Spatial patch | 4×4 |
| Temporal frame patch | 8 frames |
| Depth | Transformer layers (exact depth TBD) |
| Heads | 8 |
| Channels | 3 (RGB-replicated or HbO+HbR+HbT) |
| Pool | CLS token |
| Classes | 2 (HC=0, GAD=1) |
| Note | Configuration space being ablated — final config pending |

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
- Age confound disclosure: Welch t=-6.13, p=3.3×10⁻⁶ — acknowledge here; expand in limitations
- Sex balance: χ²=0.01, p=0.92
- Ethics statement (IRB approval — confirm with advisor)

#### 2.2 fNIRS Data Acquisition
- 23 channels, 8 source-detector pairs, 10-20 placement
- Wavelengths: 760 nm, 850 nm
- Source-detector separation: 2.49–4.19 cm
- Figure: Channel Locations.tif + brain_montage_clean_high_quality.tiff

#### 2.3 Experimental Paradigms
- Go/No-Go (GNG), Stop-Signal (SS), 1-Back Working Memory, Verbal Fluency
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

#### 3.2 Brain Activation Analysis (NB02)
- Per-channel Mann-Whitney U tests (HC vs GAD), FDR-corrected (Benjamini-Hochberg)
- Topographic activation maps by task → Figure: fig_topo_activation.png, fig_topo_effect_size.png
- Key finding: S7_D6 significant across all 4 tasks
- Task-channel heatmap: fig_channel_task_heatmap.png
- Effect size topomaps: fig_gng_sig_channels.png

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
**Status: PARTIALLY READY — §4.1 ablation (5-fold GNG-HbT) complete; §4.2–4.4 blocked pending training**
**Placeholder structure:**

#### 4.1 Ablation Study: Clip Size × Patch Size
**Data source:** `research/paper-materials/temporal_context_analysis.md`
All three configs share identical token budget (4096 tokens). Task: GNG | Signal: HbT | CV: 5-fold.

| Config | Clip Size (T,H,W) | Patch Size (t,h,w) | 5-Fold Acc | 5-Fold κ | 5-Fold MCC | 10-Fold Acc | LOSO Acc |
|---|---|---|---|---|---|---|---|
| A | (64, 32, 32) | (4, 2, 2) | 61.98% | 0.272 | 0.305 | TBD | TBD |
| B | (128, 64, 64) | (8, 4, 4) | 72.40% | 0.409 | 0.413 | TBD | TBD |
| **C** | **(256, 128, 128)** | **(16, 8, 8)** | **78.65%** | **0.543** | **0.549** | TBD | TBD |

**Key finding:** Monotonic improvement A→B→C on all metrics. Config C recommended as primary model — full HRF coverage (~25.6 s at 10 Hz), backed by ViViT §4.2 Fig.9 frame-count ablation.

#### 4.2 Hemoglobin Type Results
- HbO vs HbR vs HbT classification comparison per task

#### 4.3 Task Comparison Results
- GNG vs SS vs 1backWM vs VF — best configuration
- Reference old result as preliminary baseline: GNG LOSO 97.6%, Sensitivity 100%

#### 4.4 t-SNE Embedding Visualization (BLOCKED — depends on final model)
- CLS token embeddings colored by HC/GAD per task
- Expected: GNG shows clearest cluster separation

---

### Section 5: Discussion
**Status: PARTIALLY READY**
**Word target: ~800–1000 words**

Sub-sections:
1. **Grid encoding as spatiotemporal representation** — why topology-preserving matters vs. feature vectors
2. **HbT superiority** — tie to NB03 statistical evidence; cite total hemodynamic response literature
3. **GNG task dominance** — not explained by univariate amplitude (NB02 d rankings); spatiotemporal temporal dynamics hypothesis; suggest attention map visualization (future/pending)
4. **Patch/clip size analysis** — tradeoff: larger clips capture more temporal context but higher compute
5. **Comparison with prior art** — Wang 2025, Shao 2024, Ma 2020 literature table
6. **Limitations**:
   - Age confound: HC (73.0±5.6) vs GAD (52.2±14.6), d≈2.1 — hemodynamic aging effects
   - Small GAD sample (n≈16): limits FDR power, no severity correlation survives correction
   - No attention map visualization yet (pending)
   - Single prefrontal region — no full-head coverage

---

### Section 6: Conclusion
**Status: READY (skeleton)**
- Summarize: grid-based encoding approach, HbT justified, GNG best task
- LOSO performance (fill with final numbers)
- Clinical implication: objective, portable fNIRS system for GAD screening
- Future work: age-matched cohort, attention visualization, multi-region coverage

---

## 4. Figures Available (Confirmed Assignments)

| File | Content | Paper Section |
|---|---|---|
| `Channel Locations.tif` | fNIRS optode placement diagram | Methods §2.2 |
| `brain_montage_clean_high_quality.tiff` | Brain montage with channel overlay | Methods §2.2 |
| `GNG.tif` | Go/No-Go task paradigm | Methods §2.3 |
| `SS.tif` | Stop-Signal task paradigm | Methods §2.3 |
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
- `02_brain_activation/`: fig_topo_activation.png, fig_topo_effect_size.png, fig_channel_task_heatmap.png, fig_gng_sig_channels.png, fig_task_grand_mean.png
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
2. Stop-Signal (SS): response inhibition with variable stop-signal delay;
   0–60 s window, crop first 7 s → 53 s effective trial
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

~400 words. IEEE TNSRE style.
Save to research/paper-materials/drafts/v1_methods_signal_processing.md
```

#### Step 3: Write Methods §2.5 (Grid-Based Spatiotemporal Encoding)
```
@scientific-writing Write Section 2.5 (Grid-Based Spatiotemporal Encoding) 
as described in PAPER_SPEC_PLAN.md. Include: 1D→2D motivation, 5×7 grid 
construction, 3D video tensor formation, channel mapping rationale. 
Use the motivation paragraph from the spec. IEEE TNSRE style, ~400 words.
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
6. Transformer encoder: L stacked blocks each with multi-head self-attention (8 heads),
   feed-forward MLP, residual connections, LayerNorm
   (exact depth L TBD; to be updated from final ablation)
7. Classification head: MLP applied to CLS token output → 2 classes (HC=0, GAD=1), softmax
8. Config C selection rationale (one sentence): Config C achieves monotonically best
   performance (Acc=78.65%, κ=0.543) and captures the full hemodynamic response
   function (~25.6 s at 10 Hz); see §4.1 for full ablation results.

Cite: Arnab et al. (2021) ViViT (arXiv:2103.15691); Dosovitskiy et al. (2021) ViT.
Reference figures: Picture1.tif (overall workflow), ViT_Architecture_1.tif,
ViT_Architecture_2.tif, ViT_Architecture_3.tif

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
3. Metrics reported (mean ± SD with 95% CI across folds):
   - Accuracy (Acc): overall correct classification rate
   - Sensitivity (Sens / Recall): TP/(TP+FN) — ability to detect GAD
   - Specificity (Spec): TN/(TN+FP) — ability to identify HC
   - Precision (Prec / PPV): TP/(TP+FP)
   - F1-Score: harmonic mean of Precision and Sensitivity
   - Balanced Accuracy (BA): (Sens+Spec)/2 — robust to class imbalance
   - Negative Predictive Value (NPV): TN/(TN+FN)
   - Cohen's Kappa (κ): beyond-chance agreement
   - Matthews Correlation Coefficient (MCC): robust to imbalanced classes, range [−1,1]
   Note: AUC not reported — model outputs binary predictions; probability scores
   not stored in current training pipeline.
4. Per-fold metrics tabulated; overall from pooled confusion matrix across all folds

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
5. Note — 10-fold and LOSO results for Config C are pending and will be reported in the 
   final version.

IEEE TNSRE style. ~350 words. Include results table from the data source.
Save to research/paper-materials/drafts/v1_results_ablation.md
```

#### Step 4c: Write Discussion §5
```
@scientific-writing Write Section 5 (Discussion) for an IEEE TNSRE paper
on grid-based fNIRS GAD classification. Target ~900 words.

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

3. GNG task dominance (~200 words):
   - GNG is best classifier but univariate S7_D6 amplitude for GNG (d=0.644) is
     LOWER than 1backWM (d=0.832) — not explained by simple amplitude differences
   - Hypothesis: spatiotemporal dynamics of GNG inhibition better captured by 3D ViT
     than raw amplitude; GNG may elicit more consistent prefrontal activation patterns
   - NOTE: write as hypothesis only — attention map visualisation is pending (future work);
     do NOT state this as confirmed

4. Configuration C and temporal context (~150 words):
   - Config C (T=256) outperforms A and B on all metrics in ablation (§4.1)
   - Captures full HRF (~25.6 s) vs Config A only rise phase (~6.4 s)
   - ViViT Fig.9: more frames → higher accuracy (same principle demonstrated here)
   - Compute-accuracy tradeoff noted: Config C uses larger spatial dimensions (128×128)

5. Comparison with prior art (~100 words):
   - Compare against Wang 2025, Shao 2024, Ma 2020 (values from literature table)
   - Advantage: end-to-end spatiotemporal learning, no hand-crafted features,
     topology-preserving encoding

6. Limitations (~200 words):
   - Age confound: HC (72.7±5.2 yrs) vs. GAD (49.5±14.3 yrs), t(46)=8.20, p<0.001 —
     cannot fully rule out hemodynamic aging effects on PFC activation
   - Small GAD sample (n=16): limits FDR power; no severity correlation survives correction
   - Spatial resolution bound: effective spatial resolution is bounded by 23 discrete fNIRS
     channel positions; bilinear resize to H×W increases ViT token count but introduces
     no additional measurement information beyond the original optode arrangement
   - No attention map visualisation yet (pending ViT forward-hook implementation)
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
5. Final performance: LOSO accuracy [XX.X%], sensitivity [XX.X%]
   — leave as placeholder, to be filled after LOSO experiment completes
6. Clinical implication: portable, objective fNIRS-based screening tool for GAD;
   complements self-report instruments (GAD-7, STAI)
7. Future work (2–3 items): age-matched cohort; ViT attention map visualisation;
   multi-region fNIRS coverage beyond prefrontal cortex

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
| Section 4.1 10-fold + LOSO columns | Remaining experiments | After pending runs complete |
| Section 4.2 Hb type results | Model training | After training |
| Section 4.3 Task comparison table | Model training | After training |
| Section 4.4 t-SNE | Final model + embed.py | After training |
| Discussion §3 GNG mechanism | Attention maps | After implementing ViT hook |
| Final conclusion numbers | All results | Last step |

---

## 7. Pending Technical Items (Non-Writing)

- [ ] Confirm final 5×7 grid cell positions for all 23 channels
- [ ] Finalize clip size and patch size from ablation
- [ ] Implement ViT attention map visualization (forward hook on final attention block)
- [ ] Run t-SNE on CLS token embeddings per task (script in `src/core/embed.py`)
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
