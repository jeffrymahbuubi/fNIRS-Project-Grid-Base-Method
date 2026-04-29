# Methods §2.4 — Signal Processing Pipeline (Draft v1)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~420 words  
**Status:** Draft v1 — 2026-04-29  

---

## D. Signal Processing Pipeline

Signal preprocessing comprised two sequential stages: haemoglobin concentration estimation performed offline in Homer3 [REF-Homer3] using MATLAB, followed by epoch extraction, normalisation, spatial grid construction, and tensor preparation in Python using the MNE-Python library [REF-MNE].

In the first stage, raw NIRx light intensity recordings were processed via the custom script `nirs2csv_homer3.m`. Intensities were first converted to changes in optical density (OD) using `hmrR_Intensity2OD`. The resulting OD signals were then bandpass-filtered with `hmrR_BandpassFilt`, applying a fifth-order high-pass Butterworth filter at 0.01 Hz to remove slow physiological drift and DC offset, and a third-order low-pass filter at 0.5 Hz to suppress cardiac-frequency components and high-frequency noise. Haemoglobin concentration changes were subsequently derived from the filtered OD signals using the modified Beer-Lambert Law (mBLL) via `hmrR_OD2Conc`, with a differential partial pathlength factor (PPF) of 6 applied uniformly to both wavelengths (760 nm and 850 nm) [REF-mBLL], yielding oxyhemoglobin (HbO), deoxyhemoglobin (HbR), and total hemoglobin (HbT = HbO + HbR) time series for all 23 channels. Each subject's output was exported as a structured CSV file containing the time vector and the 23-channel haemoglobin concentration arrays.

In the second stage, the CSV files were loaded in Python and HbT was recomputed channel-wise as HbT = HbO + HbR from the stored concentration arrays. For participants whose recordings spanned split sessions, a temporal offset (*t*-offset) correction was applied to the event annotations prior to epoching to ensure accurate alignment of task onset markers with the continuous haemodynamic signal. Epochs were extracted for each paradigm using event onset codes 3.0 and 4.0; a paradigm-specific preparation period was discarded from the beginning of each epoch to retain only the active task phase, yielding retained windows of 32 s (GNG), 53 s (SS), 85 s (1-back working memory), and 53 s (VF). Each epoch was subsequently normalised channel-wise by subtracting the per-channel mean and dividing by the per-channel standard deviation (z-score normalisation), producing zero-mean, unit-variance signals across all 23 channels.

The normalised channel time series were mapped to a 5×7 spatial grid according to the anatomical optode positions shown in Fig. 7, with the 12 unoccupied grid cells initialised to zero. Empty cells were filled via Gaussian radial basis function (RBF) interpolation using `scipy.interpolate.Rbf` with a Gaussian kernel, producing a dense spatial frame *F*_*t* ∈ ℝ^(5×7) at each time point *t* (Fig. 8 and 9). Consecutive frames were stacked to form a 3D clip tensor of shape (*T*, 5, 7) (Fig. 10). Because the native 5×7 spatial resolution is insufficient for patch-based tokenisation by the ViT, each clip was spatially upsampled to (*T*, *H*, *W*) via bilinear interpolation using `torchvision.transforms.v2.Resize`, where *H* = *W* ∈ {32, 64, 128} was treated as an ablation variable (see Section IV-A). Critically, upsampling preserves the relative spatial topology of the channel arrangement but does not introduce additional cortical information; the spatial content remains bounded by the 23 physical optode positions. A uniform temporal subsampling operation (`UniformTemporalSubsample`) was then applied to standardise the number of time frames to the target clip length *T* for a given configuration. Finally, the single-channel spatial maps were replicated across three channels to produce the model input tensor of shape (3, *T*, *H*, *W*), compatible with standard ViT tubelet-embedding implementations [REF-ViViT].

---

### Figure References for This Section

| Placeholder | File            | Content |
|-------------|-----------------|---------|
| Fig. 7      | `Figure 7.tif`  | 5×7 sparse grid with 23 channel positions (12 empty cells) |
| Fig. 8      | `Fiigure 8.tif` | Single 2D spatial frame *F*_*t* before RBF interpolation |
| Fig. 9      | `Figure 9.tif`  | Dense spatial frame after Gaussian RBF interpolation |
| Fig. 10     | `Figure 10.tif` | 3D clip tensor *S*^(*k*) of shape (*T*, *H*, *W*) |

*Note: "Fiigure 8.tif" filename preserved as-is from source directory — confirm with dataset author.*

### Citation Placeholders

| Tag | Description |
|---|---|
| [REF-Homer3] | Huppert et al. 2009 HomER / Homer3 — confirm exact Homer3 citation |
| [REF-MNE] | Gramfort et al. 2013 MNE-Python (DOI: 10.3389/fnins.2013.00267) |
| [REF-mBLL] | Delpy et al. 1988 or Cope & Delpy 1988 — standard mBLL derivation |
| [REF-ViViT] | Arnab et al. 2021 ViViT (arXiv:2103.15691v2) |

### Notes for Final Assembly

- Section lettering (D) follows §2.3 (C — Experimental Tasks); renumber if sections are reordered.
- Confirm the epoching preparation-period crops: GNG 3 s, SS 7 s, 1-backWM 5 s, VF 7 s — verify against `processor_cli.py` epoch extraction code.
- The spatial resize step (step 9) should be noted as a methodological limitation in the Discussion: spatial resolution beyond 23 channels adds no new physiological information.
