# Section 3 — Statistical Analysis (Draft v1)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~510 words  
**Status:** Draft v1 — 2026-04-29  

---

## III. Statistical Analysis

### A. Demographic Characteristics

Demographic and clinical characteristics are summarized in Table I. Groups were well-matched for sex (χ²(1) = 0.01, *p* = 0.92), with 70% female in the HC group and 75% female in the GAD group. A significant age difference was observed between groups (HC: 73.0 ± 5.6 years; GAD: 52.2 ± 14.6 years; Welch's *t* = −6.13, *p* = 3.3 × 10⁻⁶, Cohen's *d* ≈ 2.1), reflecting the clinical composition of the recruited sample. This age disparity constitutes a confounding factor and is discussed further in Section V. As expected, GAD participants showed markedly elevated state and trait anxiety relative to healthy controls: STAI-S (HC: 29.8 ± 8.1; GAD: 46.6 ± 9.4; *t* = 6.11, *p* = 4.3 × 10⁻⁷) and STAI-T (HC: 33.4 ± 8.0; GAD: 59.0 ± 8.8; *t* = 9.74, *p* < 10⁻¹¹). The mean Hamilton Anxiety Rating Scale (HAMA) score among GAD participants was 23.6 ± 8.1, placing the sample within the moderate anxiety range (≥ 18).

### B. Channel-Level Brain Activation (NB02)

Per-channel hemodynamic activation was compared between GAD and HC groups using Mann-Whitney U tests, with *p*-values corrected for multiple comparisons via the Benjamini-Hochberg false discovery rate (FDR) procedure applied separately for each task. The most consistently activated channel across all four cognitive paradigms was S7_D6, which reached statistical significance under FDR correction in every task condition. Effect sizes at S7_D6, quantified by Cohen's *d*, ranked as follows across tasks: 1-Back Working Memory (*d* = 0.832), Verbal Fluency (*d* = 0.669), Go/No-Go (*d* = 0.644), and Stop-Signal (*d* = 0.583). Topographic activation maps and channel-by-task effect size heatmaps are presented in Fig. [topo_activation] and Fig. [channel_task_heatmap], respectively. Notably, the superior classification performance of the GNG paradigm documented in Section IV is not attributable to greater univariate amplitude at S7_D6 — GNG ranks third among the four tasks in channel-level effect size — suggesting that spatiotemporal hemodynamic dynamics across the prefrontal network, rather than single-channel amplitude, are the primary driver of task-specific discriminability.

### C. Hemoglobin Type Comparison (NB03)

The classification sensitivity of HbO, HbR, and HbT was compared across all 23 channels using a Friedman test, which yielded no statistically significant global difference among hemoglobin types (χ²(2) = 0.61, *p* = 0.74). However, a channel-specific analysis at S7_D6 — the most responsive prefrontal channel identified in Section III-B — revealed a dissociation among hemoglobin species. HbT achieved statistically significant group discrimination at this channel (*p* = 0.026, *d* = 0.64), whereas HbO (*p* = 0.086) and HbR (*p* = 0.071) did not reach significance. The grand-mean hemodynamic waveforms and per-channel Cohen's *d* distributions for each hemoglobin type are shown in Fig. [hb_type_grand_mean] and Fig. [hb_type_cohen_d]. These findings provide a statistical basis for the selection of HbT as the primary hemodynamic measure in the spatiotemporal encoding pipeline, reflecting its superior sensitivity to GAD-related prefrontal activation at the most diagnostically informative cortical location.

### D. Symptom Severity Correlations (NB04)

Pearson correlation coefficients were computed between mean task-epoch HbT activation at each of the 23 channels and continuous clinical severity scores, including STAI-Trait (STAI-T) and the HAMA total score (restricted to *n* = 15 GAD participants with complete HAMA data). No channel-severity correlation survived FDR correction for either measure. A trend-level association was observed between STAI-T and activation at channel S3_D1 (*r* = −0.484, *p* = 0.057, uncorrected), indicating slightly reduced HbT activation with increasing trait anxiety at this channel, though this did not reach corrected significance given the limited sample size. Topographic correlation maps are provided in Fig. [stait_correlation_topo] and Fig. [hama_correlation_topo]. The absence of FDR-surviving channel-severity correlations indicates that fNIRS prefrontal activation in this dataset functions as a categorical discriminator between GAD and HC rather than a graded physiological proxy of symptom severity, supporting the binary classification framing adopted in Section IV.

---

## Figure References for This Section

| Placeholder | File | Content |
|-------------|------|---------|
| Fig. [topo_activation] | `fig_topo_activation.png` | Topographic activation maps (HC vs GAD) by task |
| Fig. [topo_effect_size] | `fig_topo_effect_size.png` | Topographic Cohen's *d* maps by task |
| Fig. [channel_task_heatmap] | `fig_channel_task_heatmap.png` | Channel × task effect size heatmap |
| Fig. [gng_sig_channels] | `fig_gng_sig_channels.png` | FDR-significant channels for GNG task |
| Fig. [hb_type_grand_mean] | `fig_hb_type_grand_mean.png` | Grand-mean HbO/HbR/HbT waveforms per group |
| Fig. [hb_type_cohen_d] | `fig_hb_type_cohen_d.png` | Per-channel Cohen's *d* by hemoglobin type |
| Fig. [s7d6_hb_comparison] | `fig_s7d6_hb_comparison.png` | S7_D6 group comparison by hemoglobin type |
| Fig. [stait_correlation_topo] | `fig_stait_correlation_topo.png` | Pearson *r* (STAI-T) topographic map |
| Fig. [hama_correlation_topo] | `fig_hama_correlation_topo.png` | Pearson *r* (HAMA) topographic map |

All statistical figures located in `src/notebook/statistical-analysis/0{2-4}_*/`.

---

## Statistics Checklist (for revision)

| Test | Location | Reported values |
|------|----------|-----------------|
| Welch *t*-test (age) | §III-A | *t* = −6.13, *p* = 3.3×10⁻⁶, *d* ≈ 2.1 ✅ |
| χ² (sex) | §III-A | χ²(1) = 0.01, *p* = 0.92 ✅ |
| *t*-test STAI-S | §III-A | *t* = 6.11, *p* = 4.3×10⁻⁷ ✅ |
| *t*-test STAI-T | §III-A | *t* = 9.74, *p* < 10⁻¹¹ ✅ |
| Mann-Whitney U + FDR (NB02) | §III-B | S7_D6 significant all 4 tasks ✅ |
| Cohen's *d* at S7_D6 | §III-B | 1backWM 0.832, VF 0.669, GNG 0.644, SS 0.583 ✅ |
| Friedman (NB03, global) | §III-C | χ²(2) = 0.61, *p* = 0.74 ✅ |
| Mann-Whitney S7_D6 HbT | §III-C | *p* = 0.026, *d* = 0.64 ✅ |
| Mann-Whitney S7_D6 HbO | §III-C | *p* = 0.086 (ns) ✅ |
| Mann-Whitney S7_D6 HbR | §III-C | *p* = 0.071 (ns) ✅ |
| Pearson *r* STAI-T (NB04) | §III-D | S3_D1 *r* = −0.484, *p* = 0.057 (trend) ✅ |
| FDR survivors (NB04) | §III-D | None ✅ |
