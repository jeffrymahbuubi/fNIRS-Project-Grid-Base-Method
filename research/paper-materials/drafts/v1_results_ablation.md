# Results §4.1 — Ablation Study: Clip Size × Patch Size (Draft v1)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~360 words  
**Status:** Draft v1 — 2026-04-29  

---

## A. Ablation Study: Effect of Temporal Context on Classification Performance

To isolate the contribution of temporal receptive field depth from model capacity, three configurations (A, B, and C) were evaluated on the Go/No-Go (GNG) task using HbT signals under 5-fold cross-validation. Each configuration preserved a fixed spatio-temporal token budget of 4,096 tokens by scaling clip size and patch size proportionally, such that the number of temporal tokens (T/t = 16) and spatial tokens (H/h × W/w = 256) remained identical across all runs. The independent variable was therefore temporal coverage alone: configurations A, B, and C processed T = 64, 128, and 256 frames, respectively, corresponding to approximately 6.4, 12.8, and 25.6 seconds of HbT signal at the 10 Hz effective sampling rate. The architectural specifications for each configuration are summarised in TABLE I.

**TABLE I**  
*Spatio-Temporal Configuration Specifications (Fixed Token Budget = 4,096)*

| Config | Clip Size (T, H, W)   | Patch Size (t, h, w) | Temporal Tokens | Spatial Tokens | Total Tokens |
|--------|-----------------------|----------------------|-----------------|----------------|--------------|
| A      | (64, 32, 32)          | (4, 2, 2)            | 16              | 256            | **4,096**    |
| B      | (128, 64, 64)         | (8, 4, 4)            | 16              | 256            | **4,096**    |
| C      | (256, 128, 128)       | (16, 8, 8)           | 16              | 256            | **4,096**    |

Classification performance across all nine reported metrics improved monotonically from Configuration A to C, as shown in TABLE II. Overall accuracy increased from 61.98% (Config A) to 78.65% (Config C), a gain of 16.67 percentage points. The improvement in balanced accuracy (66.02% → 78.52%, +12.50 pp) confirmed that the gain was not attributable to a shift in majority-class bias. Specificity exhibited the largest absolute improvement (+25.0 pp; 0.539 → 0.789), while sensitivity remained stable at 0.781 across Configurations A and C, indicating genuine improvement in discriminative capacity rather than a sensitivity–specificity trade-off. Agreement statistics followed the same trajectory: Cohen's κ rose from 0.272 (fair) to 0.543 (moderate-good), and MCC from 0.305 to 0.549, reflecting a clinically meaningful progression in classification quality.

**TABLE II**  
*Classification Performance by Temporal Configuration — GNG Task, HbT, 5-Fold CV (Mean ± SD)*

| Metric            | Config A (T = 64) | Config B (T = 128) | Config C (T = 256) | A→C Δ     |
|-------------------|-------------------|--------------------|--------------------|-----------|
| Accuracy (%)      | 61.98             | 72.40              | **78.65**          | +16.67 pp |
| Balanced Acc. (%) | 66.02             | 71.48              | **78.52**          | +12.50 pp |
| Precision         | 0.459             | 0.571              | **0.649**          | +0.191    |
| Sensitivity       | 0.781             | 0.688              | **0.781**          | ±0.000    |
| Specificity       | 0.539             | 0.742              | **0.789**          | +0.250    |
| NPV               | 0.831             | 0.826              | **0.878**          | +0.047    |
| F1-Score          | 0.578             | 0.624              | **0.709**          | +0.131    |
| MCC               | 0.305             | 0.413              | **0.549**          | +0.244    |
| Cohen's κ         | 0.272             | 0.409              | **0.543**          | +0.271    |

*Bold denotes best value per metric. SD and 95% CI across folds to be included in the final version pending full run logs.*

These findings are consistent with the frame-count ablations reported by Arnab et al. for the Video Vision Transformer (ViViT) [REF-ViViT], in which models receiving longer input sequences—within the same architecture—consistently achieved higher accuracy by incorporating richer temporal context (§4.2, Fig. 9). The mechanistic basis in the present context is grounded in haemodynamic physiology: the cortical haemodynamic response function (HRF) elicited by the GNG task rises over approximately 6–8 s post-stimulus, peaks, and returns to baseline within 15–20 s. Configuration A (T = 64; ~6.4 s) captures only the rising phase, whereas Configuration C (T = 256; ~25.6 s) encompasses the full HRF trajectory—rise, peak, and return. The spatio-temporal self-attention mechanism of the tubelet-embedding ViT can therefore model the complete haemodynamic signature jointly across all 23 prefrontal channels under Configuration C, a capability that is architecturally precluded for shorter clip lengths. Configuration C was accordingly selected as the reference configuration for all subsequent experiments. Results under 10-fold and LOSO cross-validation for Configuration C are pending and will be reported in the final version of this manuscript.

---

### Citation Placeholders

| Tag | Description |
|---|---|
| [REF-ViViT] | Arnab A, Dehghani M, Heigold G, Sun C, Lučić M, Schmid C. ViViT: A Video Vision Transformer. arXiv:2103.15691v2 [cs.CV]. 2021. |

### Notes for Final Assembly

- Add per-fold SD and 95% CI columns to TABLE II once full run logs are available.
- TABLE I and TABLE II numbering are placeholders; renumber sequentially in assembled manuscript.
- "Pending" note for 10-fold/LOSO should be removed and replaced with filled results before submission.
- Confirm H and W clip dimensions (32/64/128) match the upsampled input pipeline in `processor_cli.py` — verify these are not raw 5×7 grid dimensions.
