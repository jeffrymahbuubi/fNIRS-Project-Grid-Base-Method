---
section: "4.2 Hemoglobin Type Comparison"
paper: "Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer"
journal: "IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)"
status: draft-v1
date: 2026-04-29
word_count_prose: ~250
---

## B. Hemoglobin Type Comparison

To isolate the independent contribution of hemoglobin signal type to classification
performance, all three fNIRS-derived signals—total hemoglobin (HbT), oxyhemoglobin
(HbO), and deoxyhemoglobin (HbR)—were evaluated under a fixed experimental condition:
the Go/No-Go (GNG) task, Configuration C, with 10-fold cross-validation. As
established in Section IV-C, the GNG paradigm yields the highest overall classification
accuracy among the four tasks evaluated; holding the task constant ensures that observed
differences in performance are attributable to signal type rather than task-specific
confounds. All metrics are reported as mean ± standard deviation (SD) across the ten
held-out folds and are summarised in TABLE III.

**TABLE III**
*Classification Performance by Hemoglobin Signal Type (GNG Task, Config C, 10-Fold CV, Mean ± SD)*

| Signal | Acc (%)        | Sens (%)       | Spec (%)       | F1                | κ                 | MCC               |
|--------|----------------|----------------|----------------|-------------------|-------------------|-------------------|
| HbT    | **88.4 ± 12.4** | **90.0 ± 11.5** | **86.9 ± 16.4** | **0.854 ± 0.125** | **0.754 ± 0.236** | **0.764 ± 0.227** |
| HbO    | 73.3 ± 17.6    | 85.0 ± 16.5    | 67.3 ± 28.6    | 0.693 ± 0.137     | 0.475 ± 0.284     | 0.496 ± 0.280     |
| HbR    | 66.8 ± 22.3    | 80.0 ± 22.2    | 56.5 ± 39.7    | 0.643 ± 0.154     | 0.349 ± 0.349     | 0.364 ± 0.346     |

*Bold denotes best value per metric. Acc = accuracy; Sens = sensitivity; Spec = specificity;
κ = Cohen's kappa; MCC = Matthews correlation coefficient.*

HbT achieved the highest performance across all six reported metrics, attaining 88.4 ±
12.4% accuracy and a Cohen's κ of 0.754 ± 0.236—substantially superior to both HbO
(73.3 ± 17.6%; κ = 0.475 ± 0.284) and HbR (66.8 ± 22.3%; κ = 0.349 ± 0.349). The
accuracy margin between HbT and HbO was 15.1 percentage points, with a corresponding
κ gap of 0.279; between HbT and HbR the gap widened to 21.6 percentage points. HbR
performance was notably unstable: the SD in specificity reached 39.7 percentage points,
and Cohen's κ equalled its own SD (0.349 ± 0.349), indicating that multiple held-out
folds yielded collapsed predictions in which the classifier assigned all test samples to
the majority class, producing zero specificity on those folds. This pattern is
consistent with the channel-level statistical analysis reported in Section III-C, where
the HbR signal at channel S7_D6 failed to reach significance (p = 0.071, not
significant), confirming that deoxyhemoglobin conveys markedly weaker discriminative
information for GAD classification within this prefrontal configuration. HbO provided
moderate but limited discrimination (κ = 0.475), remaining substantially below HbT on
all metrics. The superior performance of HbT is mechanistically consistent with its
definition as the linear sum of its components (HbT = HbO + HbR [REF-mBLL]): by
integrating both the oxygenation increase and the concurrent deoxygenation that jointly
constitute the neurovascular coupling response, HbT captures a more complete
hemodynamic signature than either component in isolation. These results confirm the
signal selection rationale presented in Section III-C, and HbT is accordingly adopted
as the primary signal type for all subsequent analyses reported in Section IV-C.

---

### Citation Placeholders

| Tag | Description |
|-----|-------------|
| [REF-mBLL] | Delpy DT, Cope M, van der Zee P, Arridge S, Wray S, Wyatt J. "Estimation of optical pathlength through tissue from direct time of flight measurement." *Phys Med Biol.* 1988;33(12):1433–1442. DOI: 10.1088/0031-9155/33/12/008 |

### Notes for Final Assembly

- TABLE III numbering is a placeholder; renumber sequentially in the assembled manuscript (follows TABLE I and TABLE II in §4.1).
- "Section IV-C" cross-reference assumes the task comparison subsection is lettered C in Part IV; adjust if subsection lettering changes.
- The Section III-C cross-reference for p = 0.071 (S7_D6 HbR) should point to the statistical analysis subsection in Methods/Results; confirm label in final assembly.
- LOSO results for Hb comparison are not included here; if collected, add a parallel LOSO row or separate column to TABLE III before submission.
