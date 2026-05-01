# Section 5 — Discussion (Draft v1)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~910 words  
**Status:** Draft v1 updated — 2026-05-01 (§V-E: Ma 2020 removed — BD vs MDD paper, incorrect comparison; Shao 2024 DOI verified; prose corrected)  

---

## V. Discussion

### A. Grid Encoding as a Topology-Preserving Spatiotemporal Representation

The central methodological contribution of this work is the translation of 23 fNIRS
channel time series into a topology-preserving 5×7 spatial grid, enabling the
construction of video-like clip tensors that can be processed by a spatiotemporal
Vision Transformer. Conventional fNIRS classification pipelines collapse channel
signals into a fixed-length feature vector prior to classification, discarding the
anatomical proximity relationships between optodes. This imposes a critical information
bottleneck: channels whose source-detector pairs occupy adjacent scalp positions measure
spatially correlated haemodynamic activity, and treating them as unordered features
prevents any learning model from exploiting these co-activation patterns. By contrast,
the proposed grid encoding assigns each channel a unique (row, column) coordinate
derived from its anatomical position, preserving spatial neighbourhoods that carry
neurophysiological meaning.

Beyond spatial structure, stacking successive dense frames into a 3D clip tensor
allows both spatial co-activation patterns and the full temporal trajectory of the
haemodynamic response function to be represented jointly. Critically, the 3D Vision
Transformer extends global self-attention to the spatiotemporal domain from its first
encoder layer [REF-ViViT], enabling every token to attend to every other
spatio-temporal location simultaneously — a capability inaccessible to convolutional
architectures whose receptive fields expand only gradually with depth. This global
attention mechanism is well-suited to the diffuse, slow haemodynamic fluctuations
characteristic of fNIRS, where diagnostically relevant signal patterns may span
multiple channels and hundreds of milliseconds simultaneously.

### B. HbT as the Primary Hemodynamic Measure

The selection of total haemoglobin (HbT) as the primary signal was motivated by
statistical analysis rather than convention. A global Friedman test across all 23
channels yielded no significant difference among the three haemoglobin species
(χ²(2) = 0.61, *p* = 0.74), indicating that no single Hb type uniformly dominates
prefrontal activation in this cohort. However, a channel-specific examination at S7_D6
— the most diagnostically relevant prefrontal channel — revealed a clear dissociation:
HbT achieved significant group discrimination (*p* = 0.026, Cohen's *d* = 0.64),
whereas HbO (*p* = 0.086) and HbR (*p* = 0.071) did not reach significance. This
finding is consistent with the physiological interpretation that HbT, as the sum of
oxyhemoglobin and deoxyhaemoglobin, integrates the full neurovascular response and is
therefore less susceptible to noise-induced cancellation between the two component
signals. The classification experiments independently converged on the same conclusion:
HbR yielded near-chance discrimination (κ = 0.349 under 10-fold CV), while HbT
outperformed HbO by 15.1 percentage points in accuracy and 0.279 in κ, confirming
that the statistical justification and the discriminative classification evidence are
mutually reinforcing.

### C. GNG Task Selection: Three Convergent Lines of Evidence

The Go/No-Go task was selected as the primary paradigm based on three independent,
converging lines of evidence rather than marginal numerical superiority alone.

The first and primary line of evidence is cross-strategy consistency. Across the three
evaluation frameworks — 5-fold CV, 10-fold CV, and LOSO — GNG's Cohen's κ followed a
trajectory of 0.553, 0.754, and 0.459, yielding a coefficient of variation (CV) of
0.209. In contrast, Verbal Fluency (VF) exhibited a CV of 0.393, collapsing from
κ = 0.761 at 10-fold to κ = 0.284 at 5-fold (Δ = +0.477), compared with GNG's more
modest sensitivity to fold size (Δ = +0.201). Although VF attained marginally higher
10-fold κ (0.761) and MCC (0.775) than GNG (0.754 and 0.764, respectively), these
values are fold-composition-dependent peaks rather than stable estimates: VF's
advantage evaporates under the more demanding 5-fold and LOSO regimes. GNG ranks
second or higher in κ across every evaluation regime and is the only task that never
falls below second place. GNG arrives at the LOSO floor from a markedly more consistent
trajectory, making it the most replication-ready task and the most appropriate
candidate for independent validation.

The second line of evidence is neuropsychological specificity. The GNG paradigm
requires prepotent response inhibition — a cognitive demand mediated primarily by the
right ventrolateral prefrontal cortex (rVLPFC) and inferior frontal gyrus (IFG)
[REF-GNG], the circuitry most directly implicated in GAD's core deficit of voluntary
worry suppression [REF-GAD-IFG]. By contrast, the 1-Back Working Memory task recruits
dorsolateral prefrontal cortex (dlPFC)-dominant circuits that impose executive load
without the sustained inhibitory demand characteristic of GAD pathophysiology, making
it a less specific probe for the disorder's neurobiology. GNG is therefore theoretically
motivated by the known neuroanatomy of GAD, not merely selected for empirical performance.

The third line of evidence is clinical utility. At 32 seconds, GNG is the shortest of
the four paradigms, minimising cognitive and time burden on the HC cohort (mean age
72.7 years) and maximising feasibility for deployment in clinical screening contexts.
Under LOSO evaluation, GNG achieved a sensitivity of 95.3%, indicating that fewer than
1 in 20 GAD cases are missed under fully cross-subject conditions — a critical criterion
for a screening instrument intended to triage individuals for further clinical assessment.

### D. Configuration C and Temporal Context

The monotonic improvement in classification performance from Configuration A (T = 64)
through Configuration B (T = 128) to Configuration C (T = 256) across all metrics in
the ablation study (Section IV-A) provides direct empirical support for the importance
of temporal context in fNIRS-based GAD classification. Configuration C captures
approximately 25.6 seconds of haemodynamic activity at 10 Hz — sufficient to cover
the full canonical haemodynamic response function including both its rise phase and
peak plateau — while Configurations A and B capture only the initial rise phase
(~6.4 s and ~12.8 s, respectively). This finding echoes the frame-count ablation
reported by Arnab et al. for the ViViT architecture [REF-ViViT], where classification
accuracy increased monotonically with the number of input frames, and is consistent
with the expectation that the full temporal dynamics of the prefrontal haemodynamic
response carry more discriminative information than any short temporal window. It
should be noted that Configuration C imposes the highest computational cost, requiring
spatial dimensions of 128×128 and a token budget of 4,096; the accuracy–compute
tradeoff may favour smaller configurations in resource-constrained deployment settings.

### E. Comparison with Prior Work

The proposed grid-based ViT approach achieved a 10-fold cross-validation accuracy of
88.4% and a LOSO accuracy of 71.4% (GNG–HbT, Config C), situating it within the range
of recently reported fNIRS-based anxiety and depression classification results. In the
most directly comparable prior study, Wang et al. [REF-Wang2025] reported 96.5% accuracy
and 95.4 F1-score for binary healthy-control versus anxiety discrimination using a
feedforward neural network trained on temporal-average HbO features and functional
connectivity measures derived from an emotional attention multitasking paradigm (EAMT).
For HCs versus major depressive disorder (MDD) — a related but clinically distinct
population — Shao et al. [REF-Shao2024] achieved 90.5% accuracy using a cross-modal
data-augmented deep neural network applied to pseudo-sequence activation images derived
from fNIRS signals. Direct numerical comparison across these studies
is limited by differences in target population (GAD versus MDD), task paradigm, and
validation protocol (cross-validated subject-level splits versus holdout). The present
method distinguishes itself through its end-to-end spatiotemporal learning paradigm: no
hand-crafted features are extracted from the fNIRS signals, and the topology-preserving
grid encoding exposes neuroanatomically structured spatial information directly to the
attention mechanism, which prior flattening-based approaches discard entirely.

### F. Limitations

Several limitations should be considered when interpreting the present findings. The
most substantial is a significant age confound between groups: HC participants were
substantially older than GAD participants (HC: 72.7 ± 5.2 years vs. GAD: 49.5 ± 14.3
years; Welch's *t*(46) = 8.20, *p* < 0.001). Age-related changes in neurovascular
coupling, cerebrovascular reactivity, and prefrontal grey matter volume are well
documented and may contribute to systematic haemodynamic differences between the groups
that are independent of anxiety diagnosis. Although diagnostic label discrimination was
confirmed by clinical instruments with large effect sizes (STAI-T Cohen's *d* = 2.59),
the possibility that haemodynamic aging effects partially drive the observed group
separation cannot be fully excluded. An age-matched cohort design would be required to
disentangle these confounds.

A second limitation is the small GAD sample (*n* = 16). The modest cohort size limits
statistical power in the channel-level FDR analysis — no channel-severity correlation
survived correction in NB04 — and contributes to the narrow per-fold positive-class
counts (1–2 GAD subjects per fold) that increase fold-level variance in 10-fold CV.

A third, substantive limitation is the cross-subject HC specificity gap observed under
LOSO evaluation. Thirteen of 32 HC participants (40.6%) were systematically misclassified
as GAD across all four cognitive tasks, driving LOSO specificity to 59.4%. This pattern
warrants dual interpretation. Methodologically, the model fails to generalise to a
phenotypically distinct subgroup of HC participants, likely those exhibiting elevated
motion artefact or atypical haemodynamic profiles; a pre-screening step based on
subject-level data quality stratification, combined with motion-corrected preprocessing
(Wavelet detrending with CBSI), is a concrete mitigation strategy for future work.
Clinically, however, the systematic nature of this misclassification — occurring
consistently across all four paradigms, independent of task content — raises the
alternative hypothesis that this HC subgroup harbours subclinical anxiety states or
age-related haemodynamic changes that genuinely overlap with GAD task-evoked responses,
and that current clinical screening instruments are insufficient to capture. Both
interpretations deserve prospective investigation.

Finally, the effective spatial resolution of the encoding remains bounded by the 23
discrete physical optode positions regardless of the bilinear upsampling factor
applied during preprocessing: upsampling from 5×7 to 128×128 increases the token count
for the ViT but introduces no additional physiological measurement information. Concrete future mitigations include: wavelet-based motion correction combined
with CBSI preprocessing to reduce artefact-driven false-positive GAD classifications
in the aging HC cohort; channel contribution analysis via ViT CLS-token attention map
extraction — and optionally graph-based spatial interpretation of those attention weights
— to identify which prefrontal optodes are most informative for the HC vs. GAD
discrimination and to guide targeted sensor reduction for clinical deployment; and
extension to full-head fNIRS coverage beyond the prefrontal cortex.

---

### Citation Placeholders

| Tag | Description |
|-----|-------------|
| [REF-ViViT] | Arnab et al. (2021). ViViT: A Video Vision Transformer. arXiv:2103.15691v2 |
| [REF-GNG] | Garavan H, Ross TJ, Stein EA. *Proc Natl Acad Sci USA.* 1999;96(14):8301–8306. DOI: 10.1073/pnas.96.14.8301 |
| [REF-GAD-IFG] | Etkin A, Wager TD. Functional neuroimaging of anxiety: a meta-analysis of emotional processing in PTSD, social anxiety disorder, and specific phobia. *Am J Psychiatry.* 2007;164(10):1476–1488. (or equivalent GAD-IFG meta-analysis — confirm with advisor) |
| [REF-Wang2025] | Wang et al. (2025). Biomed. Signal Process. Control. DOI: 10.1016/j.bspc.2025.107503. ✅ Prose filled. |
| [REF-Shao2024] | Shao K, Liu Y, Mo Y, Yang Q, Hao Y, Chen M. "fNIRS-Driven Depression Recognition Based on Cross-Modal Data Augmentation." *IEEE Trans. Neural Syst. Rehabil. Eng.*, vol. 32, pp. 2688–2698, 2024. DOI: 10.1109/TNSRE.2024.3429337. ✅ Verified (PubMed PMID 39012734). Note: published in TNSRE (same target journal). |

### Notes for Final Assembly

1. **Prior art values**: ✅ Filled (2026-05-01) — Wang 2025: 96.5% (HC vs Anxiety, comparable); Shao 2024: 90.5% (depression recognition, TNSRE). Ma 2020 REMOVED — actual paper (DOI: 10.2528/PIER20102202) classifies bipolar depression vs MDD, not HC vs MDD; citing it was factually incorrect. Current paper: 88.4% (10-fold) / 71.4% (LOSO).
2. **[REF-GAD-IFG]**: The neuropsychological pillar in §V-C requires a published meta-analysis linking rVLPFC/IFG to GAD worry suppression. Etkin & Wager 2007 is the canonical candidate; confirm with advisor. If a more GAD-specific citation exists (e.g., Britton et al. 2011), prefer it.
3. **Section lettering**: V-A through V-F follows the TNSRE two-column convention of using lettered sub-sections within numbered sections. Adjust if the journal requires numbered sub-sections (e.g., 5.1, 5.2, ...).
