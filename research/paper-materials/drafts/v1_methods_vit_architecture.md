# Methods §2.6 — 3D Vision Transformer Architecture (Draft v1)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~360 words  
**Status:** Draft v1 — 2026-04-29  

---

## F. 3D Vision Transformer Architecture

The proposed classifier is a 3D Vision Transformer (ViT) adapted from the Video Vision Transformer (ViViT) framework of Arnab et al. [REF-ViViT], which extends the image-domain ViT [REF-ViT] to spatiotemporal video inputs. The overall pipeline is shown in Fig. 11 (Picture1.tif), with architectural details provided in Fig. 12–14. The primary configuration used throughout this work is Configuration C, selected on the basis of an ablation study described in Section IV-A; Config C achieves monotonically best classification performance (5-fold accuracy 78.65%, κ = 0.543) and captures the full haemodynamic response function with a temporal receptive field of approximately 25.6 s at 10 Hz.

**Tubelet embedding.** Following the tubelet embedding approach of ViViT §3.2, the input tensor of shape (3, *T*, *H*, *W*) = (3, 256, 128, 128) was partitioned into non-overlapping 3D patches of size (*t*, *h*, *w*) = (16, 8, 8) along the temporal, height, and width dimensions, respectively. Each patch was flattened into a vector of length 3 × 16 × 8 × 8 = 3072 and linearly projected to a *d*-dimensional embedding space via a learned weight matrix, producing one token per patch. This yields a total of *N* = (256/16) × (128/8) × (128/8) = 16 × 16 × 16 = 4096 tokens per input clip.

**Token sequence and positional encoding.** A learnable classification token (CLS) was prepended to the *N*-element token sequence, resulting in a sequence of length *N* + 1 = 4097. Learnable 3D positional embeddings of dimension *d* were added to all tokens (including the CLS token) to encode spatiotemporal position information, following standard ViT practice [REF-ViT].

**Transformer encoder and classification head.** The token sequence was passed through a stack of *L* transformer encoder blocks (exact depth *L* to be finalised from the ablation study). Each block comprised multi-head self-attention with 8 attention heads, a position-wise feed-forward MLP, residual connections, and Layer Normalisation applied before each sub-layer (pre-norm convention). The output representation at the CLS token position was extracted from the final encoder block and passed to a two-layer MLP classification head, which produced logits over two output classes (HC = 0, GAD = 1) followed by a softmax activation.

---

### Figure References for This Section

| Placeholder | File | Content |
|---|---|---|
| Fig. 11 | `Picture1.tif` | Overall workflow of the proposed 3D ViT methodology |
| Fig. 12 | `ViT_Architecture_1.tif` | ViT architecture overview (input → tubelet embedding → transformer → head) |
| Fig. 13 | `ViT_Architecture_2.tif` | Patch/tubelet embedding detail |
| Fig. 14 | `ViT_Architecture_3.tif` | Transformer encoder block detail |

*Note: Fig. 11–14 numbering is a placeholder pending final figure ordering.*

### Configuration Summary (Config C)

| Parameter | Value |
|---|---|
| Input tensor | (3, 256, 128, 128) |
| Patch size (*t*, *h*, *w*) | (16, 8, 8) |
| Token count *N* | 4096 |
| Attention heads | 8 |
| Encoder depth *L* | TBD (from final ablation) |
| Classes | 2 (HC = 0, GAD = 1) |

### Citation Placeholders

| Tag | Reference |
|---|---|
| [REF-ViViT] | Arnab et al. (2021). ViViT: A Video Vision Transformer. arXiv:2103.15691v2 |
| [REF-ViT] | Dosovitskiy et al. (2021). An Image is Worth 16×16 Words. ICLR 2021. arXiv:2010.11929 |
