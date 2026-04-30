# Methods §2.6 — 3D Vision Transformer Architecture (Draft v1, updated)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~380 words  
**Status:** Draft v1 updated — 2026-04-30 (added numbered display equation Eq. (3) for token count; added [REF-Adam])

---

## F. 3D Vision Transformer Architecture

The proposed classifier is a 3D Vision Transformer (ViT) adapted from the Video Vision
Transformer (ViViT) framework of Arnab et al. [REF-ViViT], which extends the
image-domain ViT [REF-ViT] to spatiotemporal video inputs. The overall pipeline is
illustrated in Fig. 11 (Picture1.tif), with architectural details provided in
Figs. 12–14. The primary configuration used throughout this work is Configuration C,
selected on the basis of an ablation study described in Section IV-A; Config C achieves
monotonically best classification performance (5-fold accuracy 78.65%, κ = 0.543) and
captures the full haemodynamic response function with a temporal receptive field of
approximately 25.6 s at 10 Hz sampling.

**Tubelet embedding.** Following the tubelet embedding approach of ViViT §3.2
[REF-ViViT], the input tensor of shape (3, *T*, *H*, *W*) = (3, 256, 128, 128) was
partitioned into non-overlapping 3D patches of size (*t*, *p*_h, *p*_w) = (16, 8, 8)
along the temporal, height, and width dimensions, respectively. Each patch was flattened
into a vector of length 3 × 16 × 8 × 8 = 3,072 and linearly projected to a
*d*-dimensional embedding space via a learned weight matrix, producing one token per
patch. The total number of spatiotemporal tokens per clip is given by:

$$N = \frac{T}{t} \times \frac{H}{p_h} \times \frac{W}{p_w}
    = \frac{256}{16} \times \frac{128}{8} \times \frac{128}{8}
    = 16 \times 16 \times 16 = 4{,}096 \tag{3}$$

The fixed token budget of $N = 4{,}096$ [Eq. (3)] is held constant across all three
ablation configurations in Section IV-A by jointly co-varying the clip dimensions and
patch sizes, isolating the effect of temporal context length from model capacity.

**Token sequence and positional encoding.** A learnable classification token (CLS) was
prepended to the *N*-element token sequence, resulting in a sequence of length
*N* + 1 = 4,097. Learnable 3D positional embeddings of dimension *d* were added to all
tokens to encode spatiotemporal position information [REF-ViT].

**Transformer encoder and classification head.** The token sequence was processed by
a stack of **L = 6** transformer encoder blocks (confirmed in `src/core/main.py`). Each
block comprised multi-head self-attention with **8 attention heads**, a per-head
dimension of **dim_head = 64** (inner projection dimension 512), a position-wise
feed-forward MLP with hidden dimension **512** and GELU activation, residual
connections, and Layer Normalisation applied before each sub-layer (pre-norm). The
embedding dimension throughout was *d* = 64. The final CLS token representation was
passed to a two-layer MLP head (LayerNorm → Linear) producing logits over two output
classes (HC = 0, GAD = 1).

**Training configuration.** The model was optimised using Adam [REF-Adam] with
β₁ = 0.9, β₂ = 0.999, and an initial learning rate of 1 × 10⁻³. A cosine warm-up
scheduler increased the learning rate linearly from zero over the first 10 epochs and
subsequently applied cosine decay over the remaining budget. Training ran for a fixed
100 epochs with batch size 8. The checkpoint achieving the highest validation F1-score
was restored at completion for evaluation. The loss function was cross-entropy without
label smoothing. No data augmentation was applied in the default pipeline. All
experiments used random seed 42 with deterministic CUDA operations to ensure full
reproducibility. Architecture and training hyperparameters are summarised in Table [X].

---

### Figure References for This Section

| Placeholder | File | Content |
|---|---|---|
| Fig. 11 | `Picture1.tif` | Overall workflow of the proposed 3D ViT methodology |
| Fig. 12 | `ViT_Architecture_1.tif` | ViT architecture overview (input → tubelet embedding → transformer → head) |
| Fig. 13 | `ViT_Architecture_2.tif` | Patch/tubelet embedding detail |
| Fig. 14 | `ViT_Architecture_3.tif` | Transformer encoder block detail |

*Note: Fig. 11–14 numbering is a placeholder pending final figure ordering in assembly.*

### Equation Summary

| No. | Expression | Location in prose |
|-----|-----------|-------------------|
| (3) | N = (T/t) × (H/p_h) × (W/p_w) = 4,096 | Tubelet embedding paragraph; referenced again in §IV-A ablation |

*Eqs. 1–2 are defined in §2.4 (mBLL and HbT derivation).*

### Table [X]: Model Architecture and Training Configuration (Config C)

*Table number [X] is a placeholder — assign final number during manuscript assembly.*

**Architecture**

| Parameter | Value |
|---|---|
| Input (*C*, *T*, *H*, *W*) | (3, 256, 128, 128) |
| Tubelet size (*t*, *p*_h, *p*_w) | (16, 8, 8) |
| Token count *N* [Eq. (3)] | 4,096 |
| Embedding dim *d* | 64 |
| Attention heads | 8 |
| dim_head (per head) | 64 |
| MLP hidden dim | 512 |
| Encoder depth *L* | 6 |
| Output classes | 2 (HC = 0, GAD = 1) |
| Weight init (Linear) | Xavier uniform |
| Weight init (LayerNorm) | 1.0 (weight), 0.0 (bias) |

**Training**

| Parameter | Value |
|---|---|
| Optimizer | Adam (β₁ = 0.9, β₂ = 0.999) |
| Initial learning rate | 1 × 10⁻³ |
| LR schedule | Linear warm-up (10 ep) → cosine decay |
| Epochs | 100 |
| Batch size | 8 |
| Loss function | Cross-entropy (label smoothing = 0) |
| Early stopping criterion | Best validation F1 checkpoint |
| Random seed | 42 (deterministic) |
| Data augmentation | None |

### Citation Placeholders

| Tag | Reference |
|---|---|
| [REF-ViViT] | Arnab et al. (2021). ViViT: A Video Vision Transformer. arXiv:2103.15691v2 |
| [REF-ViT] | Dosovitskiy et al. (2021). An Image is Worth 16×16 Words. ICLR 2021. arXiv:2010.11929 |
| [REF-Adam] | Kingma D, Ba J. (2015). Adam: A Method for Stochastic Optimization. ICLR 2015. arXiv:1412.6980 |

### Notes for Final Assembly

- In the LaTeX manuscript, replace `$$...$$` with `\begin{equation}...\end{equation}`, label as `\label{eq:tokens}`, and reference as `\eqref{eq:tokens}`.
- The [Eq. (3)] cross-reference in §IV-A (ablation study) should read: "All three configurations share an identical token budget of $N = 4{,}096$ [Eq. (3)], ensuring that observed performance differences reflect temporal context rather than model capacity."
- Section lettering (F) assumes §2.5 is E (Grid Encoding); renumber if sections are reordered.
- "patience=25" in early stopping was confirmed from `src/core/main.py`; the effective epoch budget of 100 means stopping rarely fires, which is disclosed in the spec plan.
