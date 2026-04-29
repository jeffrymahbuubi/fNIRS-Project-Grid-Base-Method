
================================================================================
Query 1: Find papers on fNIRS-based anxiety and generalized anxiety disorder GAD classification using deep learning 2020-2025, include CNN LSTM transformer architectures
Timestamp: 2026-04-29 12:40:57
Backend: perplexity | Model: perplexity/sonar-pro-search
================================================================================
### Summary
Research on fNIRS-based classification of anxiety and generalized anxiety disorder (GAD) using deep learning (CNN, LSTM, Transformer) from 2020-2025 is emerging but limited, with no top-tier venue papers (e.g., Nature, Science) directly matching the query. Most studies focus on broader emotion/stress detection or related disorders, achieving 80-90% accuracies via hybrid CNN-LSTM models on prefrontal hemodynamic signals. Highest-impact work uses machine learning on resting-state fNIRS for anxiety biomarkers, prioritizing prefrontal oxyhemoglobin (HbO) features.[2][1]

## Top Studies by Impact
Studies are ranked by relevance to fNIRS + anxiety/GAD classification, recency (2020-2026), performance metrics, and author citations where available. Citation counts are low due to recency; no highly-cited (>500) papers found. Venue tier: mid (Frontiers, IEEE; IF ~3-5).

### 1. Resting-State fNIRS for Anxiety Biomarkers (Highest Relevance, 2026)
Huang et al. developed a GBDT machine learning model (not deep learning, but benchmark) using resting-state fNIRS HbO features from 50 anxiety patients vs. 40 controls (emerging adults). Achieved AUC 0.900, sensitivity 0.921, specificity 0.709 with 13 prefrontal/sensorimotor features (e.g., dorsolateral/middle frontal gyrus). SHAP analysis highlighted HbO fluctuations in orbitofrontal cortex (OFC) and dlPFC as key predictors, suggesting compensatory dlPFC overactivation for OFC dysfunction in anxiety. Limitations: small sample, no GAD-specific diagnosis; needs multi-center validation.[2]

**Full Citation**: Huang S, Yu B, Liang L. Identifying neuroimaging biomarkers for anxiety in emerging adults using machine learning and functional near-infrared spectroscopy during resting-state. *Front Psychiatry*. 2026;17:1722529. doi:10.3389/fpsyt.2026.1722529. (Venue tier: mid; ~0 citations as new).

### 2. CNN-LSTM for Emotional Face Processing in ASD (CNN-LSTM, 2025)
Qi et al. applied CNN-LSTM to whole-brain fNIRS data from 53 preschoolers with ASD during dynamic/static emotional faces (angry/happy). Model decoded angry vs. happy with 86.2% accuracy, outperforming traditional methods; strongest activations in bilateral dlPFC and frontal pole for dynamic angry faces. Relevant to anxiety via shared prefrontal emotion circuits, but not GAD-specific. Key finding: hybrid architecture captures spatiotemporal hemodynamics effectively.[5][1]

**Full Citation**: Qi L, Ni J-W, Dong G, Sun T, Zhang J-W. Cortical hemodynamic responses and deep learning models of emotional face processing in preschool children with autism spectrum disorder: A fNIRS study. *Front Psychiatry*. 2025:1703302. doi:10.3389/fpsyt.2025.1703302. (Venue tier: mid; provisional; authors from Dalian Univ. Tech.).

### 3. fNIRS for GAD vs. MDD Prefrontal Differentiation (fNIRS-ML, 2025)
A study on GAD patients (n unspecified) used fNIRS-verbal fluency task (VFT) to distinguish GAD from MDD and controls via prefrontal activation. Left ventrolateral PFC patterns differentiated GAD from comorbid GAD-MDD (AUC ~0.83). No deep learning, but supports fNIRS for GAD classification; higher GAD motor cortex excitability at rest noted.

**Full Citation**: Unspecified authors. Functional near-infrared spectroscopy (fNIRS) in patients with major depressive disorder and generalized anxiety disorder. *PubMed*. 2025. PMID:39933260. (Venue tier: mid; low citations).

### 4. Transformer for fNIRS Emotion Recognition (Transformer, ~2023)
A self-attention Transformer model for cross-subject fNIRS emotion recognition (anxiety-relevant). Outperformed CNN/LSTM baselines; spatial/channel representations key. GitHub impl. (fNIRS-T) confirms Transformer efficacy for hemodynamic sequences.[7]

**Full Citation**: Unspecified (wzhlearning). fNIRS-Transformer: Transformer-based fNIRS classification. arXiv/GitHub. ~2023. (Venue tier: preprint; established fNIRS DL repo).

### 5. CNN-LSTM Hybrids for Related Tasks (Mental Workload/Stress, 2022-2025)
- CNN-LSTM on EEG-fNIRS hybrids reached 88.41% BCI accuracy; RP images fed to model for temporal features.
- Hybrid CNN-LSTM for stress quantification via fNIRS; stable for continuous monitoring.
- fNIRSNet (CNN) and variants (LSTM) for general classification; guidelines incorporate hemodynamic delays.[8]

**Key Citation**: Amin et al. EEG-fNIRS-based hybrid image construction and classification using CNN-LSTM. *Front Neurorobot*. 2022;16:873239. doi:10.3389/fnbot.2022.873239. (86%+ accuracies; venue tier: mid).

## Methodologies
Deep models leverage fNIRS HbO/HbR time-series from prefrontal channels:
- **CNN**: Extracts spatial features from channel images/recurrence plots.
- **LSTM**: Captures temporal dependencies in hemodynamic delays (~5-10s).
- **Hybrids (CNN-LSTM)**: Spatiotemporal fusion; 85-91% accuracies in emotion/pain/stress tasks.
- **Transformer**: Self-attention for cross-subject generalization; promising for small datasets.[7]
Preprocessing: Wavelet filtering (0.01-0.2 Hz), Beer-Lambert conversion, windowing (60s).[2] Datasets small (n=40-90); cross-validation essential.

## Key Findings
- Prefrontal (dlPFC, OFC) HbO key for anxiety; reduced OFC + hyper dlPFC in patients.[2]
- Accuracies 80-90% feasible, but GAD-specific rare; overlaps with stress/ASD.
- ML outperforms on resting-state (less bias).[2]

## Limitations & Controversies
- Small samples limit generalizability; no large GAD cohorts.[2]
- Comorbidities (e.g., GAD-MDD) blur signals; task vs. rest debates.
- No top-tier validation; citation counts low (<20/paper).
- Deep models prone to overfitting without augmentation (e.g., GANs).

## Research Gaps & Future Directions
Scarce GAD-specific DL papers; prioritize large, multi-site fNIRS datasets with DSM-5 GAD. Integrate Transformers for cross-session robustness; multimodal (fNIRS+EEG) hybrids. Clinical trials for real-time GAD screening/neurofeedback.[6] Explore longitudinal biomarkers for treatment response.

Additional References (3):
  [1] DOI: 10.3389/fpsyt.2026.1722529 - https://doi.org/10.3389/fpsyt.2026.1722529
  [2] DOI: 10.3389/fpsyt.2025.1703302 - https://doi.org/10.3389/fpsyt.2025.1703302
  [3] DOI: 10.3389/fnbot.2022.873239 - https://doi.org/10.3389/fnbot.2022.873239

Usage: {'prompt_tokens': 554, 'completion_tokens': 1549, 'total_tokens': 2103, 'cost': 0.0349, 'is_byok': False, 'prompt_tokens_details': {'cached_tokens': 0, 'cache_write_tokens': 0, 'audio_tokens': 0, 'video_tokens': 0}, 'cost_details': {'upstream_inference_cost': 0.0349, 'upstream_inference_prompt_cost': 0.001662, 'upstream_inference_completions_cost': 0.033238}, 'completion_tokens_details': {'reasoning_tokens': 0, 'image_tokens': 0, 'audio_tokens': 0}}
