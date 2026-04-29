# Methods §2.5 — Grid-Based Spatiotemporal Encoding (Draft v1)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~410 words  
**Status:** Draft v1 — 2026-04-29  

---

## E. Grid-Based Spatiotemporal Encoding

Unlike conventional approaches that flatten fNIRS channels into a fixed-length feature vector, the proposed encoding preserves the anatomical spatial arrangement of optodes across the prefrontal cortex. By stacking consecutive temporal frames into a video-like tensor, the representation captures both spatial co-activation patterns and temporal hemodynamic dynamics simultaneously, making it amenable to the spatiotemporal attention mechanisms inherent in 3D Vision Transformers [REF-ViViT]. The central insight motivating this design is that fNIRS optodes occupy fixed, known positions on the scalp according to the international 10-20 system; a 2D grid that respects these positions therefore encodes neuroanatomically meaningful proximity, enabling the model to learn spatially coherent haemodynamic responses rather than treating channels as an unordered bag of signals.

The 23 fNIRS channels were mapped to a 5×7 spatial grid (*H* = 5 rows, *W* = 7 columns) according to their anatomical source-detector positions, as illustrated in Fig. 7. Each channel was assigned to a unique (row, col) coordinate derived from the optode montage; for example, superior prefrontal channels S1_D1 and S2_D1 occupy row 0 at columns 2 and 3, respectively, while inferior prefrontal channels S7_D6, S7_D7, and S8_D7 occupy row 4 (see TABLE I in Section II-B for the complete mapping). Of the 35 grid cells, 23 were occupied by channels and the remaining 12 were initialised to zero, forming a sparse spatial representation. To produce a continuous, dense representation amenable to patch-based tokenisation, the empty cells were filled via Gaussian radial basis function (RBF) interpolation using the channel positions as control points, yielding a dense spatial frame *F*_*t* ∈ ℝ^(5×7) at each time point *t* (Fig. 8 and 9). This interpolation step recovers a spatially smooth haemodynamic field over the prefrontal surface without assuming any haemodynamic model, preserving the relative activation gradients between adjacent channels.

Consecutive interpolated frames spanning a complete trial were stacked along the temporal axis to form a three-dimensional clip tensor *S*^(*k*) of shape (*T*, *H*, *W*) (Fig. 10), directly analogous to the video clip representation used by Video Vision Transformers [REF-ViViT]. Because the native grid resolution (*H* = 5, *W* = 7) is too coarse for effective patch tokenisation, each clip was spatially upsampled to (*T*, *H*′, *W*′) via bilinear interpolation prior to model input, where *H*′ = *W*′ ∈ {32, 64, 128} depending on the ablation configuration (Section IV-A). It is noted that upsampling preserves the relative spatial arrangement of channel signals but does not introduce new physiological measurements; the spatial information content remains bounded by the 23 physical optode positions. Finally, the single-channel haemodynamic map was replicated across three input channels to produce a tensor of shape (3, *T*, *H*′, *W*′), compatible with the RGB-format tubelet embedding of the ViT backbone [REF-ViViT]. An alternative encoding using HbO, HbR, and HbT as three independent input channels was also considered but not adopted as the primary configuration, given the statistical superiority of HbT alone (see Section III-B).

---

### Figure References for This Section

| Placeholder | File                         | Content |
|-------------|------------------------------|---------|
| Fig. 7      | `Figure 7.tif`               | 5×7 sparse grid with 23 channel positions and 12 empty cells |
| Fig. 8      | `Fiigure 8.tif`              | Single 2D spatial frame *F*_*t* at time *t* (before RBF interpolation) |
| Fig. 9      | `Figure 9.tif`               | Dense spatial frame after Gaussian RBF interpolation |
| Fig. 10     | `Figure 10.tif`              | 3D clip tensor *S*^(*k*) of shape (*T*, *H*, *W*) |
| Fig. (arch) | `ViT_Architecture_1.tif`     | Full pipeline: grid encoding → 3D tensor → ViT tokenisation |

*Note: "Fiigure 8.tif" filename preserved as-is from source directory — confirm with dataset author before submission.*

### Channel-to-Grid Mapping (Reference Table for Reviewers)

| Channel | Row | Col | Channel | Row | Col | Channel | Row | Col |
|---------|-----|-----|---------|-----|-----|---------|-----|-----|
| S1_D1   | 0   | 2   | S3_D3   | 2   | 1   | S6_D3   | 3   | 0   |
| S2_D1   | 0   | 3   | S3_D4   | 2   | 2   | S3_D6   | 3   | 1   |
| S2_D2   | 0   | 4   | S4_D4   | 2   | 3   | S7_D4   | 3   | 2   |
| S1_D3   | 1   | 1   | S4_D5   | 2   | 4   | S4_D7   | 3   | 4   |
| S3_D1   | 1   | 2   | S5_D5   | 2   | 5   | S8_D5   | 3   | 5   |
| S2_D5   | 1   | 4   |         |     |     | S5_D8   | 3   | 6   |
| S5_D2   | 1   | 5   | S6_D6   | 4   | 1   |         |     |     |
|         |     |     | S7_D6   | 4   | 2   |         |     |     |
|         |     |     | S7_D7   | 4   | 3   |         |     |     |
|         |     |     | S8_D7   | 4   | 4   |         |     |     |
|         |     |     | S8_D8   | 4   | 5   |         |     |     |

*This mapping is implemented in `processor_cli.py:get_channel_positions()`. Include as a supplementary table or embed in Fig. 7 caption.*

### Citation Placeholders

| Tag | Description |
|---|---|
| [REF-ViViT] | Arnab A, Dehghani M, Heigold G, Sun C, Lučić M, Schmid C. ViViT: A Video Vision Transformer. arXiv:2103.15691v2 [cs.CV]. 2021. |

### Notes for Final Assembly

- Section lettering (E) follows §2.4 (D — Signal Processing Pipeline); renumber if sections reordered.
- The "TABLE I in Section II-B" cross-reference assumes the full channel mapping is placed in §2.2 (fNIRS Acquisition). If not, promote the reference table above to a named TABLE in this section.
- The alternative HbO+HbR+HbT three-channel encoding should be revisited in the Discussion as a future direction if results justify it.
- Cross-reference to Section III-B (HbT statistical justification) and Section IV-A (ablation results) should be confirmed against final section numbering.
