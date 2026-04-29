# Methods §2.2 — fNIRS Data Acquisition (Draft v1)
**Paper:** Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer  
**Target:** IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)  
**Word count (body prose):** ~195 words  
**Status:** Draft v1 — 2026-04-29  

---

## B. fNIRS Data Acquisition

Cerebral hemodynamic activity was recorded using a continuous-wave fNIRS system (NIRx Medical Technologies, Berlin, Germany) comprising 8 source and 8 detector optodes that formed 23 measurement channels over the prefrontal cortex. Near-infrared illumination was delivered at two wavelengths (760 nm and 850 nm), with source-detector separations ranging from 2.49 to 4.19 cm. Optode placement followed the international 10-20 electrode positioning system, targeting the prefrontal cortex (PFC); the resulting channel configuration and anatomical coverage are illustrated in Fig. 1 (channel locations diagram) and Fig. 2 (brain montage with channel overlay).

Raw light intensity data were acquired at 10 Hz and subsequently converted to changes in oxyhemoglobin (HbO), deoxyhemoglobin (HbR), and total hemoglobin (HbT = HbO + HbR) via the modified Beer-Lambert Law (mBLL), using a differential partial pathlength factor of 6 per wavelength [REF — standard mBLL citation]. All three hemodynamic species were retained through the preprocessing pipeline; HbT was selected as the primary classification input because it captures the aggregate vascular response and was the only hemoglobin type to reach statistical significance in discriminating GAD from HC at the most responsive prefrontal channel (see Section III-C for full statistical justification).

---

### Figure References for This Section

| Placeholder | File | Content |
|---|---|---|
| Fig. 1 | `Channel Locations.tif` | fNIRS optode placement over prefrontal cortex (10-20 layout) |
| Fig. 2 | `brain_montage_clean_high_quality.tiff` | Brain montage with 23-channel overlay |

### Citation Placeholder

| Tag | Description |
|---|---|
| [REF — standard mBLL citation] | Delpy et al. 1988 or Cope & Delpy 1988 — standard mBLL reference for fNIRS; verify with dataset author |
