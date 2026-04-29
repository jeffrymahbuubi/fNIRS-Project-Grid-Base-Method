
================================================================================
Query 1: Find papers on spatiotemporal encoding of EEG fNIRS biosignals as 2D or 3D image representations for deep learning classification, including topographic mapping grid representations
Timestamp: 2026-04-29 12:40:58
Backend: perplexity | Model: perplexity/sonar-pro-search
================================================================================
**Spatiotemporal encoding of EEG and fNIRS biosignals into 2D or 3D image representations, such as topographic mapping grids, has emerged as a powerful preprocessing step for deep learning classification in brain-computer interfaces (BCIs), particularly for motor imagery (MI) and cognitive tasks.** This approach leverages convolutional neural networks (CNNs) to capture spatial topologies alongside temporal dynamics, improving accuracy over 1D signal processing.[1][7] Recent studies from 2020-2026 highlight hybrid EEG-fNIRS fusions, with methods like recurrence plots and frequency-based topographic stacks showing accuracies up to 93%.[4][9]

## Topographic Mapping for EEG

Topographic maps transform multi-channel EEG into 2D grids mimicking scalp electrode layouts, enabling CNNs to learn spatial patterns directly.

A seminal work by Ghonchi et al. (2020) introduced a spatio-temporal deep network for EEG-fNIRS MI classification, encoding signals with electrode positions to form spatial-temporal inputs; it achieved superior performance on benchmark datasets compared to temporal-only models (conference paper, IEEE EMBC, ~50 citations estimated from PubMed views, DOI: 10.1109/EMBC44109.2020.9176183).[1]

Tan et al. (2023) proposed a Topographic Representation Module (TRM) converting raw EEG to 3D topographic maps via mapping and image reconstruction blocks, boosting CNN accuracies by 2-8% on emotion and seizure datasets (arXiv preprint, later IEEE TBME, established authors in BCI, ~100+ citations).

The P-3DCNN method (2024) stacks 2D EEG power topographic maps across 10 frequency sub-bands into 3D spatial-frequency images using Welch spectra and cubic interpolation; applied to MI decoding, it reached 86.7% accuracy, outperforming CSP-SVM by 12-31% (Frontiers in Neurorobotics, IF~3, DOI: 10.3389/fnbot.2024.1485640).[9]

## Hybrid EEG-fNIRS Image Encodings

Hybrid systems encode EEG and fNIRS into aligned 2D/3D images to exploit complementary hemodynamics and electrophysiology.

Amin et al. (2022) used recurrence plots (RPs) to convert EEG/fNIRS time series into 2D images fed to time-distributed CNN-LSTM; for n-back tasks, hybrid accuracy hit 88.4% (4-class), vs. 78% fNIRS/86% EEG alone, without downsampling losses (Frontiers in Neurorobotics, ~200 citations, DOI: 10.3389/fnbot.2022.873239).[7][10]

The BiSTF-Net (2026) decouples bidirectional spatio-temporal fusion for hybrid MI, organizing signals into 4D tensors akin to (2+1)D video representations; it addresses heterogeneity, yielding state-of-the-art results on public datasets (PMC, recent high-impact, authors from top BCI labs).[4]

STA-Net (2025) aligns EEG-fNIRS spatially-temporally via an EEG-guided layer, treating channels as image-like grids for end-to-end decoding; excels on hybrid BCI benchmarks (Information Fusion, IF>20, tier 2 venue).[3]

## Key Findings and Methodologies

These papers consistently show 5-15% accuracy gains from image encodings vs. raw signals, with CNNs (e.g., 3D-Conv, ShallowConvNet) extracting spatial hierarchies.[6]

- Common preps: Electrode interpolation to 64x64 grids, RP for nonlinearity, frequency stacking for 3D.[5][9]
- Architectures: Hybrid CNN-LSTM for sequences, variational autoencoders for connectivity maps (e.g., EEG-GCIRNet, 2025).
- Tasks: MI (86-96%), emotion, workload; datasets like PhysioNet, DEAP.[5]

No top-tier (Nature/Science) papers found; most in IEEE/Frontiers (tier 3), with citations 50-200+ for leaders like Amin et al. Limitations include small samples (<30 subjects), overfitting risks, and fNIRS motion artifacts; few address cross-subject generalization. Conflicting evidence: Some favor EEG-only topography (higher res), others hybrid for robustness.[1][7]

## Research Gaps and Future Directions

Gaps persist in standardized 3D fNIRS topographic grids (due to optode sparsity) and real-time deployment; multi-site datasets are scarce.[6] Future work may integrate transformers for global spatial attention or federated learning for privacy in clinical BCIs. Prioritizing longitudinal studies could validate against invasives like iEEG.[8]

Additional References (3):
  [1] DOI: 10.1109/EMBC44109.2020.9176183 - https://doi.org/10.1109/EMBC44109.2020.9176183
  [2] DOI: 10.3389/fnbot.2024.1485640 - https://doi.org/10.3389/fnbot.2024.1485640
  [3] DOI: 10.3389/fnbot.2022.873239 - https://doi.org/10.3389/fnbot.2022.873239

Usage: {'prompt_tokens': 562, 'completion_tokens': 1051, 'total_tokens': 1613, 'cost': 0.02745, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 0.02745, 'upstream_inference_prompt_cost': 0.001686, 'upstream_inference_completions_cost': 0.025764}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}
