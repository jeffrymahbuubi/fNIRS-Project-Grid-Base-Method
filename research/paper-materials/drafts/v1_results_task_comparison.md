---
section: "4.3 Task Comparison"
paper: "Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer"
journal: "IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)"
status: draft-v2
date: 2026-05-01
word_count_prose: ~360
assembly_flag: "Three-pillar GNG argument. LOSO complete. NB02 removed from §III — neuropsychological pillar now self-contained."
---

## C. Task Comparison

Following the hemoglobin type analysis presented in Section IV-B, all four cognitive
paradigms—Go/No-Go (GNG), Verbal Fluency (VF), 1-Back Working Memory (1backWM), and
Serial Subtraction (SS)—were evaluated with HbT as the fixed signal under identical
conditions: Configuration C with 10-fold cross-validation. This design isolates
task-dependent hemodynamic discriminability from signal-type and architectural confounds
established in the preceding sections. All metrics are reported as mean ± SD across the
ten held-out folds and are summarised in TABLE IV.

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

TABLE IV reports within-cohort performance under 10-fold CV. TABLE V reports
cross-subject generalisation under Leave-One-Subject-Out (LOSO) cross-validation,
where each of the 48 subjects is held out in turn as the independent test set.
LOSO metrics are derived from the pooled confusion matrix across all held-out subjects;
per-fold mean±SD is not reported because each LOSO test fold contains exactly one
subject (single-class), rendering per-fold Sensitivity/Specificity undefined.

**TABLE V**
*Classification Performance by Cognitive Task — LOSO Cross-Validation (HbT, Config C,
pooled confusion matrix, *n* = 48 subjects: 32 HC + 16 GAD)*

| Task     | Acc (%)      | Sens (%)     | Spec (%) | F1        | κ         | MCC       |
|----------|--------------|--------------|----------|-----------|-----------|-----------|
| GNG †    | **71.4**     | **95.3**     | 59.4     | **0.689** | **0.459** | **0.524** |
| VF †     | **71.4**     | **95.3**     | 59.4     | **0.689** | **0.459** | **0.524** |
| 1backWM  | 70.3         | 92.2         | 59.4     | 0.674     | 0.436     | 0.492     |
| SS       | 69.8         | 92.2         | 58.6     | 0.671     | 0.428     | 0.486     |

*Bold denotes best value per metric. †GNG and VF yield identical LOSO confusion matrices
([[76, 52], [3, 61]]) and are co-ranked first on all metrics. Positive class = GAD (label 1);
Negative class = HC (label 0).*

All four tasks exceeded chance-level performance, spanning 78.9% (SS) to 88.9% (VF)
in mean accuracy. GNG was selected as the primary paradigm based on convergent evidence
from three complementary pillars: cross-strategy consistency, neuropsychological
specificity, and clinical utility.

GNG demonstrated the most stable classification performance across all three evaluation
strategies. Its Cohen's κ followed a trajectory of 0.553 (5-fold), 0.754 (10-fold), and
0.459 (LOSO), yielding a cross-strategy coefficient of variation (CV) of 0.209. VF
attained the numerically highest 10-fold κ (0.761) and MCC (0.775), marginally
exceeding GNG on both metrics; however, VF collapsed to κ = 0.284 at 5-fold
(Δ = +0.477 from 5- to 10-fold, versus GNG Δ = +0.201), indicating that its peak
performance is sensitive to fold composition rather than reflecting a robust underlying
signal. GNG ranked second or higher on κ in every evaluation regime and is the only
task that never falls below second place. Under leave-one-subject-out (LOSO)
cross-validation—the most stringent benchmark for cross-subject generalisation—GNG
and VF reached an identical κ = 0.459 (pooled confusion matrices were identical across
tasks), yet GNG arrives at this floor from a substantially more stable trajectory,
providing stronger evidence that its discriminability generalises to unseen subjects.

GNG selection is further supported by its neuropsychological specificity to GAD
pathophysiology. The paradigm requires prepotent response inhibition governed by the
right ventrolateral prefrontal cortex (rVLPFC) and inferior frontal gyrus [REF-GNG]—
the circuitry specifically implicated in GAD's core deficit of voluntary worry
suppression. In contrast, 1-Back Working Memory predominantly engages dorsolateral
prefrontal cortex (dlPFC) circuits that impose executive load without the sustained
inhibitory demand that characterises GAD-related prefrontal dysregulation, making GNG
the more theoretically motivated probe for the disorder.

From a clinical perspective, GNG is also the shortest paradigm at 32 seconds, imposing
the lowest cognitive burden on the HC cohort (mean age 72.7 years). Under LOSO
evaluation (TABLE V), GNG achieved a sensitivity of 95.3%, meaning that fewer than
1 in 20 GAD cases are missed under fully cross-subject conditions — the most
conservative generalisation estimate available. This high sensitivity is the critical
performance criterion for a clinical screening instrument and is prioritised accordingly;
the associated specificity gap (Spec = 59.4%) reflects hemodynamic heterogeneity
in a subgroup of HC participants and is addressed as a study limitation in Section V.

The SS paradigm exhibited the highest sensitivity across all tasks (92.5 ± 10.5%) but
at the cost of a markedly elevated false-alarm rate (Spec = 69.2%, SD = 38.7 pp),
indicating that multiple held-out folds produced collapsed predictions and limiting its
suitability as a primary paradigm. The 1backWM task showed intermediate overall
performance (κ = 0.665) but exhibited the widest κ SD (± 0.360), reflecting fold-level
instability comparable to SS and consistent with the prediction-collapse behaviour
observed in the HbR conditions in Section IV-B.

---

### Citation Placeholders

| Tag | Description |
|-----|-------------|
| [REF-GNG] | Garavan H, Ross TJ, Stein EA. "Right hemispheric dominance of inhibitory control: an event-related functional MRI study." *Proc Natl Acad Sci USA.* 1999;96(14):8301–8306. DOI: 10.1073/pnas.96.14.8301 |

*Consider adding a GAD-rVLPFC/IFG citation (e.g., Etkin & Wager 2007 meta-analysis) to reinforce the neuropsychological pillar.*

---

### Notes for Final Assembly

1. **Three-pillar structure (v2)**: Consistency → Neuropsychological specificity → Clinical utility.
   Each pillar is one paragraph. The table leads; GNG selection is justified before the
   SS/1backWM paragraph, which closes the section.

2. **NB02 removed from §III (2026-05-01)**: The neuropsychological pillar no longer
   cross-references §III-B activation data. It stands on cited literature ([REF-GNG]
   and optionally a GAD-IFG meta-analysis). Ensure the reference list includes these.

3. **VF vs GNG ranking — accurate framing**: VF numerically leads on 10-fold κ (0.761 vs
   0.754) and MCC (0.775 vs 0.764). Do NOT write "GNG achieves the highest κ/MCC."
   The prose correctly says "VF attained the numerically highest 10-fold κ and MCC."

4. **TABLE numbering**: TABLE IV and TABLE V are placeholders; renumber sequentially
   during final assembly (TABLE IV follows TABLE III from §IV-B; TABLE V follows TABLE IV).

5. **LOSO — TABLE V added (2026-05-01)**: GNG LOSO full metrics (pooled CM, n=48):
   Acc=71.4%, Sens=95.3%, Spec=59.4%, F1=0.689, κ=0.459, MCC=0.524.
   GNG and VF produce identical confusion matrices at LOSO — both bold in TABLE V.
   Note on bold: two tasks sharing the same best value should both be bolded.

6. **HC specificity subgroup (§5 link)**: 13/32 HC (40.6%) systematically misclassified
   as GAD across all 4 tasks; discussed as limitation with dual framing in §5.
