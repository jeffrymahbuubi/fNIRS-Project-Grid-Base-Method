# Methods §2.7 — Evaluation Framework (Draft v1)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~270 words  
**Status:** Draft v1 — 2026-04-29  

---

## G. Evaluation Framework

Model performance was assessed using three complementary cross-validation (CV) strategies, each operating at the subject level to prevent data leakage between training and test sets. All partitioning was stratified by diagnostic label to preserve the approximately 2:1 healthy control (HC) to GAD class ratio across folds. Five-fold CV (5-Fold) partitioned the 48 subjects into five equal folds and was employed primarily for ablation studies and hyperparameter comparisons due to its lower computational overhead. Ten-fold CV (10-Fold) subdivided subjects into ten folds, yielding more stable performance estimates with reduced variance across partitions and was adopted as the primary reporting protocol. Leave-one-subject-out CV (LOSO) held out each of the 48 subjects in turn as an independent test set, producing 48 separate training-test iterations (32 HC + 16 GAD), and constitutes the strongest evidence for generalisation to previously unseen individuals—an essential criterion for clinical deployment. Together, the three strategies provide mutually reinforcing evidence: 5-Fold enables rapid architectural exploration, 10-Fold anchors reported performance on stable estimates, and LOSO directly quantifies subject-level transferability.

Nine classification metrics were computed for each fold and reported as mean ± standard deviation (SD) with 95% confidence intervals (CIs) derived across folds. Accuracy (Acc) captured the overall correct-classification rate. Sensitivity (Sens) and specificity (Spec) quantified the model's ability to identify GAD and HC individuals respectively, with balanced accuracy (BA = (Sens + Spec) / 2) providing an imbalance-robust summary. Precision (Prec; positive predictive value) and negative predictive value (NPV) reflected the reliability of positive and negative predictions, while the F1-score (harmonic mean of Prec and Sens) synthesised detection performance into a single scalar. Cohen's kappa (κ) measured agreement beyond chance, and the Matthews correlation coefficient (MCC; range [−1, 1]) offered a balanced assessment robust to the asymmetric class distribution. Area under the receiver operating characteristic curve (AUC) was not computed, as the model produces hard binary predictions and probability scores are not retained in the current training pipeline. Aggregate performance was additionally derived from the pooled confusion matrix concatenated across all folds, with per-fold results tabulated in full in the supplementary material.

---

### Citation Placeholders

| Tag | Description |
|---|---|
| — | No new external citations required; cross-validation and metric definitions are standard and do not require citation in IEEE TNSRE style unless a specific implementation library is referenced |

### Notes for Final Assembly

- Confirm whether 95% CI is computed via bootstrap or normal approximation across fold scores — specify method in revision.
- "Supplementary material" reference should be updated to match final submission structure if TNSRE permits supplementary tables.
- Section lettering (G) follows §2.6 (F — ViT Architecture); renumber if sections are reordered.
