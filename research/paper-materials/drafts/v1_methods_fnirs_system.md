---
section: "2.2 fNIRS Data Acquisition"
paper: "Grid-Based Spatiotemporal Encoding of fNIRS Signals for GAD Classification Using a 3D Vision Transformer"
journal: "IEEE Transactions on Neural Systems and Rehabilitation Engineering (TNSRE)"
status: draft-v1
date: 2026-04-29
figures:
  - Channel Locations.tif
  - brain_montage_clean_high_quality.tiff
---

## 2.2 fNIRS Data Acquisition

fNIRS data were acquired using a NIRx continuous-wave system with 8 optode sources and
an array of photodetectors configured to yield 23 measurement channels. Dual-wavelength
near-infrared illumination at 760 nm and 850 nm was applied, providing the differential
spectral sensitivity required to resolve changes in oxyhemoglobin (HbO) and
deoxyhemoglobin (HbR) concentrations. Source-detector separations ranged from 2.49 to
4.19 cm, ensuring adequate sensitivity to cortical hemodynamic activity within the
superficial gray matter of the prefrontal region.

Optodes were positioned over the prefrontal cortex (PFC) following the international
10-20 electrode positioning system, affording bilateral coverage of frontal regions
associated with executive function, emotion regulation, and inhibitory control. The
spatial arrangement of all 23 channels is illustrated in Fig. 1 (optode layout) and
Fig. 2 (source-detector pairs projected onto the cortical surface), where Fig. 1
corresponds to the measured channel locations (Channel Locations.tif) and Fig. 2 to
the high-resolution brain montage (brain_montage_clean_high_quality.tiff).

Raw optical intensity measurements were converted to hemodynamic concentration changes
using the modified Beer-Lambert Law (MBLL), yielding per-channel time series for HbO,
HbR, and total hemoglobin (HbT = HbO + HbR). HbT was adopted as the primary signal
for all downstream analyses because it integrates the full hemodynamic response and was
statistically confirmed as the most discriminative measure at channel S7_D6
(see Section 3.3).
