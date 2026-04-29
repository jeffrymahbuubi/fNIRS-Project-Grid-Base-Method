
================================================================================
Query 1: Find papers on Video Vision Transformer ViViT VideoViT applied to biosignal EEG fNIRS time series classification, spatiotemporal attention for physiological signals
Timestamp: 2026-04-29 12:41:01
Backend: perplexity | Model: perplexity/sonar-pro-search
================================================================================
ViViT (Video Vision Transformer) and VideoViT, pure transformer models for video understanding via spatiotemporal tokens and attention, have seen limited direct application to biosignal classification like EEG or fNIRS time series, with no high-impact papers from top-tier venues (e.g., Nature, Science) identified in 2020-2026 literature.[2][1] Instead, related Vision Transformer (ViT) adaptations—converting 1D biosignals to 2D spectrograms or images—dominate recent EEG seizure classification work, achieving superior performance over CNNs by capturing global dependencies.[1][2] Spatiotemporal attention mechanisms appear in multimodal EEG-fNIRS fusion for tasks like motor imagery and emotion recognition, enhancing accuracy via cross-modal alignment, though not explicitly tied to ViViT architectures.[3][7]

## Foundational ViViT Model
ViViT introduces factorized spatiotemporal attention for video classification, processing spatial tokens per frame then temporal sequences, enabling efficient modeling of dynamics without 3D convolutions.[2][1] Published in ICCV 2021 by Arnab et al. (Google Research; highly cited, ~1,500 citations per Google Scholar estimates), it achieves state-of-the-art on Kinetics-400/600 via variants like factorized encoders, pretrained on large video datasets.[10][1] No direct extensions to physiological signals were found, limiting its influence here (venue tier: top conference; DOI: 10.48550/arXiv.2103.15691).[2]

## Top ViT Applications to EEG Classification
**ViT for Electrographic Seizure Detection (2025, Frontiers in Human Neuroscience; ~new, 0 citations; venue tier 3; authors from NeuroPace/USC/Cleveland Clinic).** Afzal et al. trained ViT-B/16 (86M parameters) on spectrogram images from 136,878 iEEG clips (113 drug-resistant focal epilepsy patients, NeuroPace RNS System), achieving 96.8% 5-fold CV accuracy, outperforming ResNet-50 (95.6%) and 2D CNNs (94.4%).[1][2] Key methodology: Short-time Fourier transform spectrograms (250 Hz, colorized); attention rollout showed focus on high-frequency seizure bands; generalizes to out-of-distribution idiopathic generalized epilepsy (75-82% accuracy vs. experts).[2] Limitations: Single-channel focus; false negatives (8.7%) on ambiguous patterns; implications for clinician review of vast iEEG volumes (PMCID: PMC12540479; DOI: 10.3389/fnhum.2025.1680395).[1]

**VIPEEGNet for Harmful Brain Patterns (2025, npj Digital Medicine; Nature portfolio, tier 1; new publication).** This vision-inspired model converts EEG to images for ImageNet-pretrained backbones, classifying seizures/GPDs/LRDA/etc. with clinical generality; publicly available on Kaggle.[4] Outperforms unimodal baselines via transfer learning, bridging CV and EEG; no citation count yet, but high venue impact.

**EEG-VTTCNet for Motor Imagery (2024, Neuroscience; tier 3).** Joint ViT-TCN training extracts global (ViT) and temporal features from MI-EEG, with auxiliary losses boosting robustness.[3] Achieves superior accuracy via windowed CNN/positional encoding; limitations: MI-specific, not seizure/general biosignals (DOI: 10.1016/j.neuroscience.2024.09.024).[3]

## Spatiotemporal Attention in Physiological Signals
**TiViT for Time Series (NeurIPS 2025; top conference, tier 2).** Converts time series to 2D patches for frozen ViTs, increasing label-relevant tokens and reducing sample complexity; applicable to EEG via image-like representations.

**st-DenseViT for Brain Networks (2025, PMC; tier 3).** Weakly supervised spatiotemporal ViT for dynamic neuronal mapping in fMRI-like data, capturing fluctuations; extendable to EEG/fNIRS.

For EEG-fNIRS fusion, spatiotemporal models like ENSTAN (IEEE TAFFC) align modalities via dynamic multigraph attention for emotion recognition, addressing spatial misalignment.[9] SGSTAN (Scientific Reports, 2025) uses graph attention for synchronization in MI tasks. EEG temporal-spatial transformers (Nature Scientific Reports, 2022; ~50 citations) model long-range dependencies bidirectionally (~85% person ID accuracy). Transformer for fNIRS (Neurophotonics, 2025) predicts channels via encoder on resting-state series.

No ViViT/VideoViT papers directly on EEG/fNIRS; closest are image-based ViT adaptations (e.g., ViT2EEG, KDD 2023). Multimodal EEG-fNIRS reaches 96-98% in MI/MA via multi-domain fusion (Frontiers, 2022; ~20 citations), but pre-transformer.[8]

| Model | Signal | Task | Accuracy | Citation Count | Venue Tier |
|------|--------|------|----------|----------------|------------|
| ViT (86M) [1][2] | iEEG spectrograms | Seizure | 96.8% | New (2025) | 3 |
| EEG-VTTCNet [3] | EEG | MI | State-of-art | New | 3 |
| VIPEEGNet [4] | EEG images | Brain patterns | SOTA clinical | New | 1 |
| ENSTAN [9] | EEG-fNIRS | Emotion | High | Low | 3 |

## Limitations and Controversies
ViT success relies on spectrogram conversion, adding preprocessing artifacts (e.g., stimulation removal improves ~0.5%; not always significant).[2] Generalization varies: strong in-distribution (96%), drops out-of-distribution (75-82%).[2] No top-tier (Nature/Science) papers; field dominated by mid-tier journals/conferences. Citation bias favors older works; newer ViT apps lack long-term validation. Inter-rater variability in labeling (e.g., 16% disagreement) questions ground truth.[2]

## Research Gaps and Future Directions
Direct ViViT porting to multichannel EEG/fNIRS videos (e.g., as spatiotemporal tokens) remains unexplored, potentially revolutionizing classification via native video modeling over image hacks. Multimodal ViViT with spatiotemporal fusion could address EEG's speed vs. fNIRS's hemodynamics. Prioritize large, diverse datasets beyond CHB-MIT; test on wearable biosignals. Hybrid ViT-3D CNNs or federated learning for privacy in clinical deployment. High-impact venues needed for validation.[2][1]

Additional References (3):
  [1] DOI: 10.48550/arXiv.2103.15691 - https://doi.org/10.48550/arXiv.2103.15691
  [2] DOI: 10.3389/fnhum.2025.1680395 - https://doi.org/10.3389/fnhum.2025.1680395
  [3] DOI: 10.1016/j.neuroscience.2024.09.024 - https://doi.org/10.1016/j.neuroscience.2024.09.024

Usage: {'prompt_tokens': 557, 'completion_tokens': 1482, 'total_tokens': 2039, 'cost': 0.0339, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 0.0339, 'upstream_inference_prompt_cost': 0.001671, 'upstream_inference_completions_cost': 0.032229}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}
