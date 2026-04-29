# Methods §2.1 — Participants and Dataset Characteristics (Draft v1)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~310 words  
**Status:** Draft v1 — 2026-04-29  

---

## A. Participants

The study was approved by the Institutional Review Board of [INSTITUTION — TO BE PROVIDED] (approval no. [IRB NUMBER — TO BE PROVIDED]), and all participants provided written informed consent prior to enrollment. Fifty-three adults were recruited, of whom 48 completed the full experimental protocol and were retained for analysis: 32 healthy controls (HC) and 16 individuals with a confirmed clinical diagnosis of generalized anxiety disorder (GAD). Five participants were excluded owing to incomplete task recordings (one HC, four GAD).

Demographic and clinical characteristics are summarized in TABLE I. HC participants were older on average (72.7 ± 5.2 years; range 65–84) than GAD participants (49.5 ± 14.3 years; range 29–70), a statistically significant difference (*t*(46) = 8.20, *p* = 1.50 × 10⁻¹⁰) that constitutes a known demographic confound; this age disparity is discussed as a study limitation in Section V. Sex distribution did not differ significantly between groups (χ²(1) = 0.13, *p* = 0.72): 23 of 32 HC participants were female (72%) and 13 of 16 GAD participants were female (81%), indicating that sex was not a confounding factor in the present analysis.

Clinical anxiety was assessed using the Hamilton Anxiety Rating Scale (HAMA) and the State-Trait Anxiety Inventory (STAI). HAMA scores were available for 15 of 16 GAD participants (23.5 ± 8.7); including one participant for whom the instrument was not administered (coded 0), the group mean was 22.0 ± 10.3 (range 0–40).† GAD participants exhibited markedly elevated state and trait anxiety relative to HC: STAI-State (GAD: 45.8 ± 8.7 vs. HC: 29.4 ± 8.5; *t*(46) = −6.26, *p* < 0.001, Cohen's *d* = 1.90) and STAI-Trait (GAD: 57.2 ± 6.8 vs. HC: 34.1 ± 9.7; *t*(46) = −8.54, *p* < 0.001, Cohen's *d* = 2.59), confirming robust clinical separation between the two groups.

---

### TABLE I
**Participant Demographic and Clinical Characteristics**

| Characteristic | HC (*n* = 32) | GAD (*n* = 16) | Statistic | *p*-value |
|---|---|---|---|---|
| Age (years), mean ± SD | 72.7 ± 5.2 | 49.5 ± 14.3 | *t*(46) = 8.20 | 1.50 × 10⁻¹⁰ * |
| Age range (years) | 65–84 | 29–70 | — | — |
| Sex (F / M) | 23 / 9 | 13 / 3 | χ²(1) = 0.13 | 0.72 |
| Female (%) | 72% | 81% | — | — |
| HAMA, mean ± SD | — | 22.0 ± 10.3 † | — | — |
| STAI-State, mean ± SD | 29.4 ± 8.5 | 45.8 ± 8.7 | *t*(46) = −6.26 | < 0.001 * |
| STAI-Trait, mean ± SD | 34.1 ± 9.7 | 57.2 ± 6.8 | *t*(46) = −8.54 | < 0.001 * |

\* *p* < 0.05 (statistically significant).  
† HAMA mean includes one participant (LA063) for whom the instrument was not administered (coded 0). Excluding this participant: mean = 23.5 ± 8.7 (*n* = 15).

---

### Footnotes

†  Participant LA063 (GAD): HAMA was not administered and was coded as 0 in the dataset. This participant was retained in all analyses on the basis of clinically elevated STAI scores (STAI-S = 55, STAI-T = 63), which are consistent with a GAD diagnosis. HAMA-dependent analyses report both the inclusive (*n* = 16) and exclusive (*n* = 15) statistics.

‡  Participant AH029 (HC): self-reported a history of major depressive disorder and was receiving psychotherapy and pharmacological treatment at the time of data acquisition. No independent clinical diagnosis was confirmed by the research team; results pertaining to this participant should therefore be interpreted with caution.
