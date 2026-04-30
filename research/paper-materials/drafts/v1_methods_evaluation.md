# Methods §2.7 — Evaluation Framework (Draft v1, updated)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~280 words  
**Status:** Draft v1 updated — 2026-04-30 (added compact metrics table; prose condensed to reference Table I)

---

## G. Evaluation Framework

Model performance was assessed using three complementary cross-validation (CV) strategies,
each operating at the subject level to prevent data leakage between training and test sets.
All partitioning was stratified by diagnostic label to preserve the approximately 2:1
healthy control (HC) to GAD class ratio across folds. Five-fold CV (5-Fold) partitioned
the 48 subjects into five equal folds and was employed primarily for ablation studies and
hyperparameter comparisons due to its lower computational overhead. Ten-fold CV (10-Fold)
subdivided subjects into ten folds, yielding more stable performance estimates with reduced
variance across partitions and was adopted as the primary reporting protocol.
Leave-one-subject-out CV (LOSO) held out each of the 48 subjects in turn as an independent
test set, producing 48 separate training-test iterations (32 HC + 16 GAD), and constitutes
the strongest evidence for generalisation to previously unseen individuals—an essential
criterion for clinical deployment. Together, the three strategies provide mutually
reinforcing evidence: 5-Fold enables rapid architectural exploration, 10-Fold anchors
reported performance on stable estimates, and LOSO directly quantifies subject-level
transferability.

The approximate class composition of each test partition warrants explicit disclosure.
Under stratified 5-Fold CV, each test fold contains approximately 6–7 HC and 3 GAD
subjects (~9–10 per fold). Under 10-Fold CV, each test fold contains approximately 3–4 HC
and 1–2 GAD subjects (~4–5 per fold). The small per-fold GAD count (1–2 subjects) in the
10-Fold setting is an inherent consequence of the cohort size (16 GAD total) and motivates
presenting the pooled confusion matrix—computed by concatenating predictions across all
held-out folds—as the primary performance summary alongside per-fold mean ± standard
deviation. Under LOSO, each of the 48 test iterations contains exactly one subject (32
HC, 16 GAD), reflecting the overall 2:1 class ratio. Because every LOSO test fold is
single-class, per-fold sensitivity and specificity are undefined for individual subjects;
all LOSO aggregate metrics are therefore derived exclusively from the pooled confusion
matrix across all 48 held-out subjects.

Nine classification metrics were computed for each fold using the formulae in Table I,
with the positive class defined as GAD (label 1) and the negative class as HC (label 0).
Results are reported as mean ± standard deviation (SD) across folds; overall performance
is additionally derived from the pooled confusion matrix. Cohen's kappa (κ) and the
Matthews correlation coefficient (MCC) are the primary ranking metrics as both are
robust to the 2:1 class imbalance. Area under the receiver operating characteristic
curve (AUC) was not computed, as the model produces hard binary predictions and
probability scores are not retained in the current training pipeline.

**TABLE I**
*Classification Metrics. Positive class = GAD (label 1); Negative class = HC (label 0).*

| Metric | Symbol | Formula |
|--------|--------|---------|
| Accuracy | Acc | (TP + TN) / (TP + TN + FP + FN) |
| Sensitivity (Recall) | Sens | TP / (TP + FN) |
| Specificity | Spec | TN / (TN + FP) |
| Precision (PPV) | Prec | TP / (TP + FP) |
| F1-Score | F1 | 2·TP / (2·TP + FP + FN) |
| Balanced Accuracy | BA | (Sens + Spec) / 2 |
| Neg. Predictive Value | NPV | TN / (TN + FN) |
| Cohen's Kappa | κ | (*p*_o − *p*_e) / (1 − *p*_e) |
| Matthews Corr. Coeff. | MCC | (TP·TN − FP·FN) / √[(TP+FP)(TP+FN)(TN+FP)(TN+FN)] |

*p*_o = observed agreement; *p*_e = expected agreement by chance (κ). MCC range [−1, 1].

---

### Notes for Final Assembly

- **Table I numbering**: Placeholder "Table I" — assign final sequential number during manuscript assembly. If Table I conflicts with the demographics table in §2.1, renumber sequentially.
- **95% CI**: The previous draft mentioned 95% CIs across fold scores — confirm whether CIs are computed via bootstrap resampling or normal approximation; specify method in revision before submission. Remove if not computed.
- **Supplementary material**: If per-fold breakdown tables are moved to supplementary, add cross-reference here; TNSRE does permit supplementary material.
- **Section lettering (G)**: Follows §2.6 (F — ViT Architecture); renumber if sections are reordered.
- **LaTeX table**: The MCC formula uses `\sqrt{...}` with a long radicand — typeset with `\sqrt{(\text{TP}+\text{FP})(\text{TP}+\text{FN})(\text{TN}+\text{FP})(\text{TN}+\text{FN})}` and wrap in a `tabular` with appropriate column widths.
