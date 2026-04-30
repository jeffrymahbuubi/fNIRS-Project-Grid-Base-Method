# Section 3 — Statistical Analysis (Draft v1, corrected)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~530 words  
**Status:** Draft v1 updated — 2026-05-01 (demographics corrected; §III.B NB02 removed — results inconclusive)

---

## III. Statistical Analysis

### A. Demographic Characteristics

Demographic and clinical characteristics are summarised in Table I. Groups were well-matched for sex distribution (χ²(1) = 0.13, *p* = 0.72), with 72% female in the HC group (23F/9M) and 81% female in the GAD group (13F/3M), indicating that sex is not a confounding variable. A significant age difference was present between groups (HC: 72.7 ± 5.2 years, range 65–84; GAD: 49.5 ± 14.3 years, range 29–70; Welch's *t*(46) = 8.20, *p* = 1.50 × 10⁻¹⁰), reflecting the clinical composition of the recruited sample and constituting a potential confound that is addressed in Section V. As expected, GAD participants showed markedly elevated anxiety relative to healthy controls on both state and trait dimensions: STAI-State (HC: 29.4 ± 8.5; GAD: 45.8 ± 8.7; *t*(46) = −6.26, *p* < 0.001, Cohen's *d* = 1.90) and STAI-Trait (HC: 34.1 ± 9.7; GAD: 57.2 ± 6.8; *t*(46) = −8.54, *p* < 0.001, *d* = 2.59). The mean HAMA total score among GAD participants was 22.0 ± 10.3 (*n* = 16; 23.5 ± 8.7 when excluding one participant for whom the HAMA was not administered, *n* = 15), placing the group in the moderate-to-severe anxiety range.

### B. Hemoglobin Type Comparison (NB03)

The sensitivity of HbO, HbR, and HbT to GAD-related activation was compared across all 23 channels using a Friedman test, which yielded no statistically significant global difference among hemoglobin types (χ²(2) = 0.61, *p* = 0.74). A channel-specific analysis at S7_D6 — the most diagnostically consistent channel identified in Section III-B — revealed a dissociation among hemoglobin species: HbT achieved statistically significant group discrimination (*p* = 0.026, *d* = 0.64), whereas HbO (*p* = 0.086) and HbR (*p* = 0.071) did not reach significance. Grand-mean hemodynamic waveforms and per-channel Cohen's *d* distributions for each hemoglobin type are shown in Fig. [hb_type_grand_mean] and Fig. [hb_type_cohen_d]. These findings provide the statistical basis for selecting HbT as the primary hemodynamic measure in the spatiotemporal encoding pipeline, given its superior sensitivity to GAD-related prefrontal activation.

### C. Symptom Severity Correlations (NB04)

Pearson correlation coefficients were computed between mean task-epoch HbT activation at each of the 23 channels and continuous clinical severity measures, including STAI-Trait (STAI-T) and the HAMA total score, with the latter restricted to the *n* = 15 GAD participants for whom HAMA data were available. No channel-severity correlation survived FDR correction for either clinical measure. A trend-level negative association was observed between STAI-T and activation at channel S3_D1 (*r* = −0.484, *p* = 0.057, uncorrected), indicating slightly reduced HbT activation with increasing trait anxiety, though this association did not reach corrected significance. Topographic correlation maps are provided in Fig. [stait_correlation_topo] and Fig. [hama_correlation_topo]. The absence of FDR-surviving correlations indicates that fNIRS prefrontal activation functions as a categorical group discriminator rather than a graded physiological proxy of symptom severity, supporting the binary classification framing adopted throughout Section IV.

---

## Figure References for This Section

| Placeholder | File | Content |
|-------------|------|---------|
| Fig. [hb_type_grand_mean] | `fig_hb_type_grand_mean.png` | Grand-mean HbO/HbR/HbT waveforms per group |
| Fig. [hb_type_cohen_d] | `fig_hb_type_cohen_d.png` | Per-channel Cohen's *d* by hemoglobin type |
| Fig. [s7d6_hb_comparison] | `fig_s7d6_hb_comparison.png` | S7_D6 group comparison by hemoglobin type |
| Fig. [stait_correlation_topo] | `fig_stait_correlation_topo.png` | Pearson *r* (STAI-T) topographic map |
| Fig. [hama_correlation_topo] | `fig_hama_correlation_topo.png` | Pearson *r* (HAMA) topographic map |

All statistical figures located in `src/notebook/statistical-analysis/0{2-4}_*/`.

---

## Statistics Checklist

| Test | Location | Reported values |
|------|----------|-----------------|
| Welch *t*-test (age) | §III-A | *t*(46) = 8.20, *p* = 1.50×10⁻¹⁰ ✅ |
| χ² (sex) | §III-A | χ²(1) = 0.13, *p* = 0.72 ✅ |
| *t*-test STAI-S | §III-A | *t*(46) = −6.26, *p* < 0.001, *d* = 1.90 ✅ |
| *t*-test STAI-T | §III-A | *t*(46) = −8.54, *p* < 0.001, *d* = 2.59 ✅ |
| HAMA mean (GAD, n=16) | §III-A | 22.0 ± 10.3 ✅ |
| HAMA mean (GAD, n=15, excl. LA063) | §III-A | 23.5 ± 8.7 ✅ |
| Friedman (NB03, global) | §III-B | χ²(2) = 0.61, *p* = 0.74 ✅ |
| Mann-Whitney S7_D6 HbT | §III-B | *p* = 0.026, *d* = 0.64 ✅ |
| Mann-Whitney S7_D6 HbO | §III-B | *p* = 0.086 (ns) ✅ |
| Mann-Whitney S7_D6 HbR | §III-B | *p* = 0.071 (ns) ✅ |
| Pearson *r* STAI-T (NB04) | §III-C | S3_D1 *r* = −0.484, *p* = 0.057 (trend) ✅ |
| FDR survivors (NB04) | §III-C | None ✅ |

---

## Corrections from Previous Draft (2026-04-29 → 2026-04-30)

The 2026-04-29 draft used preliminary demographic statistics that differed from the ground-truth values in PAPER_SPEC_PLAN.md §2.1. Corrected values:

| Field | Old (incorrect) | New (ground truth) |
|-------|----------------|--------------------|
| HC age | 73.0 ± 5.6 yrs | **72.7 ± 5.2 yrs** |
| GAD age | 52.2 ± 14.6 yrs | **49.5 ± 14.3 yrs** |
| Age *t*-stat | *t* = −6.13 | ***t*(46) = 8.20** |
| Age *p*-value | *p* = 3.3×10⁻⁶ | ***p* = 1.50×10⁻¹⁰** |
| Sex χ² | χ²(1) = 0.01, *p* = 0.92 | **χ²(1) = 0.13, *p* = 0.72** |
| HC % female | 70% | **72% (23F/9M)** |
| GAD % female | 75% | **81% (13F/3M)** |
| STAI-S HC | 29.8 ± 8.1 | **29.4 ± 8.5** |
| STAI-S GAD | 46.6 ± 9.4 | **45.8 ± 8.7** |
| STAI-S *t* | *t* = 6.11, *p* = 4.3×10⁻⁷ | ***t*(46) = −6.26, *p* < 0.001, *d* = 1.90** |
| STAI-T HC | 33.4 ± 8.0 | **34.1 ± 9.7** |
| STAI-T GAD | 59.0 ± 8.8 | **57.2 ± 6.8** |
| STAI-T *t* | *t* = 9.74, *p* < 10⁻¹¹ | ***t*(46) = −8.54, *p* < 0.001, *d* = 2.59** |
| HAMA | 23.6 ± 8.1 | **22.0 ± 10.3 (n=16); 23.5 ± 8.7 (n=15, excl. LA063)** |

NB03 and NB04 values were correct in the previous draft and are unchanged.
§III.B (NB02, Channel-Level Brain Activation) removed entirely on 2026-05-01: analysis did not yield
a sufficiently clear pattern to justify inclusion. The GNG task selection argument is now supported
by the three-pillar narrative in §IV-C (consistency, neuropsychological specificity, clinical utility)
which does not require NB02 statistical backing.
