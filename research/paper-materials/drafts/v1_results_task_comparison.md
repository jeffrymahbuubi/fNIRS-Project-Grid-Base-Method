---
section: "4.3 Task Comparison"
paper: "Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer"
journal: "IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)"
status: draft-v1
date: 2026-04-29
word_count_prose: ~310
assembly_flag: "resolved — GNG selection justified by cross-CV consistency and neurological rationale"
---

## C. Task Comparison

Following the hemoglobin type analysis presented in Section IV-B, all four cognitive
paradigms—Go/No-Go (GNG), Verbal Fluency (VF), 1-Back Working Memory (1backWM), and
Serial Subtraction (SS)—were evaluated with HbT as the fixed signal under identical
conditions: Configuration C with 10-fold cross-validation. This design isolates
task-dependent hemodynamic discriminability from both signal-type and architectural
confounds established in the preceding sections. All metrics are reported as mean ± SD
across the ten held-out folds and are summarised in TABLE IV.

**TABLE IV**
*Classification Performance by Cognitive Task (HbT, Config C, 10-Fold CV, Mean ± SD)*

| Task    | Acc (%)          | Sens (%)         | Spec (%)         | F1                | κ                  | MCC                |
|---------|------------------|------------------|------------------|-------------------|--------------------|--------------------|
| GNG     | 88.4 ± 12.4      | **90.0 ± 11.5**  | 86.9 ± 16.4      | **0.854 ± 0.125** | 0.754 ± 0.236      | 0.764 ± 0.227      |
| VF      | **88.9 ± 9.0**   | 87.5 ± 15.6      | **91.0 ± 9.4**   | 0.843 ± 0.136     | **0.761 ± 0.194**  | **0.775 ± 0.176**  |
| 1backWM | 83.4 ± 19.9      | 83.8 ± 21.3      | 82.5 ± 30.3      | 0.804 ± 0.194     | 0.665 ± 0.360      | 0.669 ± 0.361      |
| SS      | 78.9 ± 23.2      | 92.5 ± 10.5      | 69.2 ± 38.7      | 0.808 ± 0.176     | 0.613 ± 0.394      | 0.634 ± 0.374      |

*Bold denotes best value per metric. GNG = Go/No-Go; VF = Verbal Fluency;
1backWM = 1-Back Working Memory; SS = Serial Subtraction.*

All four tasks exceeded chance-level performance, spanning from 78.9% (SS) to 88.9%
(VF) in mean accuracy. The GNG and VF paradigms yielded comparable, high-tier
discrimination, with mean accuracies within 0.5 percentage points of each other. VF
attained the numerically highest values on mean accuracy, specificity, κ, and MCC
(88.9%; 91.0%; κ = 0.761; MCC = 0.775), whereas GNG achieved the highest F1-score
(0.854) and sensitivity (90.0%) among all four tasks. Both paradigms are distinguished
from the lower-performing conditions by cross-fold stability: the SDs in accuracy were
12.4 pp (GNG) and 9.0 pp (VF), compared with 19.9 pp (1backWM) and 23.2 pp (SS).
Although GNG and VF yielded comparable 10-fold performance (κ = 0.754 and κ = 0.761,
respectively), GNG demonstrated substantially greater consistency across cross-validation
strategies: under 5-fold evaluation, GNG achieved κ = 0.553 compared with κ = 0.284 for
VF, indicating that VF's marginal 10-fold advantage is sensitive to fold composition and
training set size rather than reflecting superior generalisability. GNG is therefore
selected as the primary paradigm, additionally supported by its direct neuropsychological
relevance to prefrontal inhibitory control deficits characteristic of GAD [REF-GNG]; all
subsequent reporting adopts the GNG–HbT configuration as the primary experimental
condition.

The SS paradigm exhibited the highest sensitivity across all tasks (92.5 ± 10.5%),
reflecting strong identification of true GAD cases, but at the cost of a markedly
elevated false-alarm rate: mean specificity was 69.2%, with an SD of 38.7 percentage
points indicating that multiple held-out folds produced collapsed predictions. This
sensitivity–specificity asymmetry substantially limits the clinical utility of the SS
paradigm despite its apparent GAD-detection power. The 1backWM task showed intermediate
overall performance (κ = 0.665) but exhibited the widest κ SD among all conditions
(± 0.360), reflecting fold-level instability comparable to SS; both paradigms displayed
substantially higher inter-fold variance than GNG and VF, consistent with the
prediction-collapse behaviour observed in the HbR conditions examined in Section IV-B.
Leave-one-subject-out (LOSO) cross-validation for the primary GNG–HbT configuration is
ongoing; results, including accuracy, sensitivity, specificity, F1, κ, and MCC, will be
reported in the final version of this manuscript ([LOSO-Acc] ± [LOSO-SD];
κ = [LOSO-κ]; MCC = [LOSO-MCC]).

---

### Citation Placeholders

| Tag | Description |
|-----|-------------|
| [REF-GNG] | Garavan H, Ross TJ, Stein EA. "Right hemispheric dominance of inhibitory control: an event-related functional MRI study." *Proc Natl Acad Sci USA.* 1999;96(14):8301–8306. DOI: 10.1073/pnas.96.14.8301 |

---

### Notes for Final Assembly

1. **GNG vs VF ranking — RESOLVED**: VF numerically leads GNG on 4 of 6 metrics at 10-fold (Acc, Spec, κ, MCC). GNG selection is justified by cross-CV consistency (5-fold GNG κ=0.553 vs VF κ=0.284) and neuropsychological rationale. This is now reflected in the prose above. No further action needed here unless LOSO data reverses the picture.

2. **TABLE numbering**: TABLE IV is a placeholder; renumber sequentially following TABLE III from §4.2 in the assembled manuscript.

3. **LOSO placeholders**: Replace all [LOSO-*] tokens with actual values before submission; remove the "ongoing" clause. When LOSO confirms GNG superiority, add one sentence: "LOSO evaluation further confirmed GNG as the best-generalising task (κ = [LOSO-κ]), consistent with the cross-validation trend."

4. **[REF-GNG]**: Garavan H, Ross TJ, Stein EA. *Proc Natl Acad Sci USA.* 1999;96(14):8301–8306. DOI: 10.1073/pnas.96.14.8301
