# Methods §2.5 — Grid-Based Spatiotemporal Encoding (Draft v2)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~530 words  
**Status:** Draft v2 — 2026-05-01 (full mathematical formalisation; Eqs. (3)–(9) added; NB02 cross-ref removed)

---

## E. Grid-Based Spatiotemporal Encoding

Unlike conventional approaches that flatten fNIRS channels into a fixed-length feature
vector, the proposed encoding preserves the anatomical spatial arrangement of optodes
across the prefrontal cortex. fNIRS optodes occupy fixed, known positions on the scalp
according to the international 10-20 system; a 2D grid respecting these positions
encodes neuroanatomically meaningful proximity, enabling the model to learn spatially
coherent haemodynamic patterns rather than treating channels as an unordered bag of
signals. By stacking consecutive spatial frames into a video-like tensor, the
representation simultaneously captures both spatial co-activation structure and temporal
haemodynamic dynamics, making it amenable to the spatiotemporal attention mechanisms
of 3D Vision Transformers [REF-ViViT]. The seven-step formalisation of this encoding
pipeline is presented below; Figs. 7–10 illustrate each transformation.

**Step 1 — Epoch matrix.** Each trial epoch is represented as a haemodynamic-concentration
matrix

$$\mathbf{H}^{(k)} = [\mathbf{h}_t]_{t \in \tau_k} \in \mathbb{R}^{C \times L} \tag{3}$$

where $C = 23$ is the number of fNIRS channels, $L$ is the number of time samples in
epoch $k$, and the column vector
$\mathbf{h}_t = [\Delta\text{HbT}_{1,t}, \ldots, \Delta\text{HbT}_{C,t}]^\top$
contains the HbT concentration change at time $t$ for every channel.

**Step 2 — Channel-wise z-score normalisation.** Each epoch is normalised channel-wise
by subtracting the per-channel mean $\boldsymbol{\mu}_k$ and dividing by the per-channel
standard deviation $\boldsymbol{\sigma}_k$:

$$\hat{\mathbf{h}}_t^{(k)} = \bigl(\mathbf{h}_t^{(k)} - \boldsymbol{\mu}_k\bigr) \oslash \boldsymbol{\sigma}_k \tag{4}$$

where $\oslash$ denotes element-wise division. This produces zero-mean, unit-variance
signals across all 23 channels, placing channels on a common scale regardless of
inter-subject haemodynamic amplitude differences.

**Step 3 — Mapping to 5×7 sparse grid.** Each normalised sample vector
$\hat{\mathbf{h}}_t^{(k)} \in \mathbb{R}^{23}$ is placed into a $5 \times 7$ spatial
grid via a fixed bijective mapping

$$M : \{1, \ldots, 23\} \to \{1, \ldots, 5\} \times \{1, \ldots, 7\}, \quad M(c) = (i_c,\, j_c) \tag{5}$$

derived from the anatomical optode positions (confirmed in `processor_cli.py:get_channel_positions()`). The resulting sparse spatial frame at time $t$ is

$$F_t(i,\, j) = \begin{cases} \hat{h}_{c,t} & \text{if } (i,j) = M(c) \text{ for some } c \\ 0 & \text{otherwise} \end{cases} \tag{6}$$

Of the 35 grid cells, 23 are occupied and the remaining 12 are initialised to zero
(Fig. 7).

**Step 4 — Gaussian RBF interpolation to dense frame.** The 12 zero-filled cells are
recovered via Gaussian radial-basis function interpolation. For any unoccupied grid
point $(x, y)$,

$$\hat{F}_t(x,\,y) = \sum_{m=1}^{23} w_m \exp\!\left[-\varepsilon^2 \bigl\|(x,y) - (x_m, y_m)\bigr\|^2\right] \tag{7}$$

The weights $w_m$ are determined by solving the linear system $\boldsymbol{\Phi}\mathbf{w} = \mathbf{z}$, where $\Phi_{mn} = \exp[-\varepsilon^2 \|(x_m,y_m)-(x_n,y_n)\|^2]$ and $z_m = F_t(x_m, y_m)$. This produces a fully populated dense frame $\hat{F}_t \in \mathbb{R}^{5\times 7}$ that preserves the topographic structure of the original optode array (Figs. 8 and 9).

**Step 5 — Stacking to 3D clip.** The sequence of dense frames
$\{\hat{F}_t\}_{t \in T_k}$ is stacked along the temporal axis to form a
spatiotemporal clip tensor

$$\mathbf{S}^{(k)} = [\hat{F}_t]_{t \in T_k} \in \mathbb{R}^{L \times 5 \times 7} \tag{8}$$

directly mirroring the video clip representation used by Video Vision Transformers
[REF-ViViT] (Fig. 10).

**Step 6 — Uniform temporal subsampling.** Because trials have variable length $L$,
a uniform temporal subsampling operation selects $T^*$ uniformly spaced frame indices

$$\text{idx}_i = \left\lfloor \frac{(i-1)(L-1)}{T^*-1} \right\rfloor, \quad i = 1, \ldots, T^* \tag{9}$$

yielding $\mathbf{S}^* \in \mathbb{R}^{T^* \times 5 \times 7}$. This preserves the full
chronological order of the epoch while standardising the temporal dimension across
subjects and tasks.

**Step 7 — Spatial upsampling and RGB replication.** Because the native $5 \times 7$
spatial resolution is too coarse for patch-based tokenisation, $\mathbf{S}^*$ is
upsampled to $(T^*, H', W')$ via bilinear interpolation, where $H' = W' \in \{32, 64, 128\}$
depending on the ablation configuration (Section IV-A). Upsampling preserves the relative
spatial topology of channel signals but introduces no new physiological information;
the spatial information content remains bounded by the 23 physical optode positions.
Finally, the single-channel haemodynamic map is replicated across three input channels
to yield the model input tensor of shape $(3, T^*, H', W')$, compatible with the
RGB-format tubelet embedding of the ViT backbone [REF-ViViT].

---

### Figure References for This Section

| Placeholder | File | Content |
|-------------|------|---------|
| Fig. 7 | `Figure 7.tif` | 5×7 sparse grid: 23 channel positions and 12 empty cells [Eq. (6)] |
| Fig. 8 | `Fiigure 8.tif` | Single 2D spatial frame $F_t$ at time $t$ (before RBF) |
| Fig. 9 | `Figure 9.tif` | Dense frame $\hat{F}_t$ after Gaussian RBF [Eq. (7)] |
| Fig. 10 | `Figure 10.tif` | 3D clip tensor $\mathbf{S}^{(k)}$ of shape $(T, H, W)$ [Eq. (8)] |

*Note: "Fiigure 8.tif" filename preserved as-is — confirm with dataset author before submission.*

### Equation Summary for This Section

| No. | Description | Step |
|-----|-------------|------|
| (3) | Epoch matrix $\mathbf{H}^{(k)} \in \mathbb{R}^{C \times L}$ | Step 1 |
| (4) | Channel-wise z-score normalisation | Step 2 |
| (5) | Bijective grid mapping $M$ | Step 3 |
| (6) | Sparse spatial frame $F_t$ | Step 3 |
| (7) | Gaussian RBF interpolation to $\hat{F}_t$ | Step 4 |
| (8) | 3D clip stacking $\mathbf{S}^{(k)}$ | Step 5 |
| (9) | Uniform temporal subsampling indices | Step 6 |

*Eqs. (1)–(2) are defined in §2.4 (mBLL and HbT derivation).*

### Numbering Conflict with §2.6

The existing §2.6 draft currently labels the token count formula as Eq. (3). With §2.5 now
occupying Eqs. (3)–(9), the §2.6 token count equation must be renumbered to **Eq. (10)**
during final manuscript assembly. Update the in-text reference in §2.6 and in §IV-A
(ablation discussion) accordingly:
> "All three configurations share an identical token budget of $N = 4{,}096$ [Eq. (10)],
> ensuring that observed performance differences reflect temporal context rather than model
> capacity."

### Channel-to-Grid Mapping (Reference for Fig. 7 Caption or Supplementary)

| Channel | Row | Col | Channel | Row | Col | Channel | Row | Col |
|---------|-----|-----|---------|-----|-----|---------|-----|-----|
| S1_D1 | 0 | 2 | S3_D3 | 2 | 1 | S6_D3 | 3 | 0 |
| S2_D1 | 0 | 3 | S3_D4 | 2 | 2 | S3_D6 | 3 | 1 |
| S2_D2 | 0 | 4 | S4_D4 | 2 | 3 | S7_D4 | 3 | 2 |
| S1_D3 | 1 | 1 | S4_D5 | 2 | 4 | S4_D7 | 3 | 4 |
| S3_D1 | 1 | 2 | S5_D5 | 2 | 5 | S8_D5 | 3 | 5 |
| S2_D5 | 1 | 4 | | | | S5_D8 | 3 | 6 |
| S5_D2 | 1 | 5 | S6_D6 | 4 | 1 | | | |
| | | | S7_D6 | 4 | 2 | | | |
| | | | S7_D7 | 4 | 3 | | | |
| | | | S8_D7 | 4 | 4 | | | |
| | | | S8_D8 | 4 | 5 | | | |

*Implemented in `processor_cli.py:get_channel_positions()`.*

### Citation Placeholders

| Tag | Description |
|-----|-------------|
| [REF-ViViT] | Arnab A, et al. ViViT: A Video Vision Transformer. arXiv:2103.15691v2. 2021. |

### Notes for Final Assembly

- Section lettering (E) follows §2.4 (D — Signal Processing Pipeline); renumber if sections are reordered.
- **NB02 cross-reference removed**: The old draft referenced "Section III-B" for HbT statistical justification via activation data. NB02 was dropped from §III. The HbT justification cross-reference now points to Section III-B (Hb Type Comparison, NB03), which remains correct in the revised structure.
- The alternative HbO+HbR+HbT three-channel encoding should be mentioned in the Discussion as a future direction.
- In LaTeX: replace `$$...$$` with `\begin{equation}...\end{equation}` and label each as `\label{eq:epochmat}`, `\label{eq:zscore}`, etc.
