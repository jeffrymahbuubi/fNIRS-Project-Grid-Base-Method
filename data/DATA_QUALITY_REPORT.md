# fNIRS Dataset Quality Report

**Generated:** 2026-04-30  
**Assessed by:** Automated quality scan + Homer3 best-practice cross-reference  
**Datasets:** `data/raw` (64 subjects, all 4 tasks) and `data/additional-raw` (11 subjects, GNG+SS)  
**Basis:** Signal quality metrics computed from HbO/HbR CSV files + raw .nirs intensity CV (additional-raw only)

---

## 1. Quality Metrics Used

| Metric | Source | Threshold | Meaning |
|--------|--------|-----------|---------|
| **Mean spike count** | HbO CSV (amplitude jumps > 5× mean diff) | >3000 severe, 1500–3000 moderate | Motion artifact density |
| **HbO/HbR correlation** | Channel-wise Pearson r | >0.5 severe, >0.2 moderate | Systemic noise dominance (ideal: negative) |
| **Raw intensity CV** | .nirs file (additional-raw only) | >15% bad, 7.5–15% acceptable | Scalp contact / optode coupling quality |
| **Signal scale** | Mean \|HbO\| | 1–4×10⁻⁷ M ideal | Calibration / Beer-Lambert validity |

### Risk Classification

| Flag | Condition |
|------|-----------|
| **HIGH-RISK** | Score ≥ 4 (severe motion + systemic noise, or bad raw channels) |
| **WATCH** | Score 2–3 (moderate issues — usable but may degrade model performance) |
| **OK** | Score 0–1 (no significant issues detected) |

> **Important context:** The positive HbO/HbR correlation seen in many subjects is partially expected when no motion correction is applied (see §4). It does NOT automatically mean the data is unusable — but it does indicate that systemic physiological noise (heartbeat, Mayer waves) is not suppressed.

---

## 2. HIGH-RISK Subjects (11 total)

These subjects show a combination of high motion artifact density and/or strong systemic noise dominance. Their inclusion in training may introduce label-irrelevant signal variation.

### data/raw — Anxiety (2 subjects)

| Subject | Mean Spikes | HbO/HbR Corr | Primary Issue |
|---------|-------------|--------------|---------------|
| **AA011** | 4,493 | +0.479 | Severe motion + strong systemic noise |
| **EA055** | 3,438 | +0.441 | Severe motion + strong systemic noise |
| **LA063** | 3,879 | +0.604 | Severe motion + very strong systemic noise (highest corr in anxiety group) |

### data/raw — Healthy (4 subjects)

| Subject | Mean Spikes | HbO/HbR Corr | Primary Issue |
|---------|-------------|--------------|---------------|
| **AH024** | 3,443 | +0.560 | Severe motion + very strong systemic noise |
| **AH045** | 3,399 | +0.458 | Severe motion + strong systemic noise |
| **AH046** | 3,420 | +0.489 | Severe motion + strong systemic noise |
| **AH049** | 3,469 | +0.468 | Highest spike count in healthy group |

### data/additional-raw — Anxiety (4 subjects)

| Subject | Mean Spikes | HbO/HbR Corr | Raw CV (nirs) | Bad Ch | Primary Issue |
|---------|-------------|--------------|---------------|--------|---------------|
| **AA093** | 4,867 | +0.319 | 4.9% | 0 | Severe motion + moderate systemic noise |
| **AA094** | 3,209 | +0.321 | 6.8% | 1 | Severe motion + moderate systemic noise |
| **AA099** | 3,395 | −0.120 | 7.5% | 1 | Severe motion + 1 marginal channel (note: HbO/HbR corr is actually good) |
| **LA096** | 3,587 | +0.182 | 6.9% | 1 | Severe motion + 1 marginal channel |

> **Note on AA099:** Despite being HIGH-RISK due to motion artifacts and 1 marginal channel, the HbO/HbR correlation is negative (−0.12) which is the correct physiological direction. AA099's risk is primarily motion-artifact driven, not systemic noise. It may still be usable after motion correction.

---

## 3. WATCH Subjects (22 total)

Moderate concerns. Usable for training but should be monitored for outlier behavior during cross-validation.

### data/raw — Anxiety (8 subjects)

| Subject | Mean Spikes | HbO/HbR Corr | Watch Reason |
|---------|-------------|--------------|-------------|
| AA003 | 1,959 | +0.421 | Moderate motion + moderate noise |
| AA004 | 1,736 | +0.214 | Moderate motion + moderate noise |
| EA060 | 1,623 | +0.221 | Moderate motion + moderate noise |
| EA062 | 2,414 | +0.404 | Moderate-high motion + moderate noise |
| LA042 | 1,703 | +0.264 | Moderate motion + moderate noise |
| LA054 | 2,047 | +0.386 | Moderate motion + moderate noise |
| LA057 | 1,946 | +0.340 | Moderate motion + moderate noise |
| LA059 | 2,227 | +0.401 | Moderate motion + moderate noise |

### data/raw — Healthy (9 subjects)

| Subject | Mean Spikes | HbO/HbR Corr | Watch Reason |
|---------|-------------|--------------|-------------|
| AH015 | 1,816 | +0.256 | Moderate motion + noise |
| AH022 | 1,634 | +0.263 | Moderate motion + noise |
| AH025 | 2,612 | +0.478 | Moderate-high motion + high noise |
| AH027 | 1,904 | +0.344 | Moderate motion + moderate noise |
| AH028 | 2,204 | +0.374 | Moderate motion + moderate noise |
| AH030 | 2,028 | +0.277 | Moderate motion + moderate noise |
| AH032 | 2,462 | +0.408 | Moderate motion + moderate noise |
| AH035 | 2,501 | +0.324 | Moderate motion + moderate noise |
| AH040 | 2,162 | +0.620 | Highest noise in healthy WATCH group |

### data/additional-raw — Anxiety (5 subjects)

| Subject | Mean Spikes | HbO/HbR Corr | Raw CV | Watch Reason |
|---------|-------------|--------------|--------|-------------|
| AA090 | 5,870 | +0.124 | 6.5% | Very high motion (highest in add-raw) |
| AA092 | 3,889 | +0.082 | 4.7% | High motion |
| AA097 | 2,786 | +0.357 | 2.3% | Moderate motion + moderate noise |
| LA091 | 3,701 | +0.150 | 3.7% | High motion |
| LA095 | 2,583 | +0.406 | 9.3% | Moderate motion + moderate noise + worst raw CV in add-raw group |

---

## 4. OK Subjects (42 total)

No significant quality concerns detected.

**data/raw — Anxiety (OK):**  
AA002, AA005, AA006, AA007, AA008, AA013, AA041, AA056, AA064, EA012, EA016, EA061, LA051, LA052, LA053, LA058

**data/raw — Healthy (OK):**  
AH009, AH010, AH014, AH017, AH018, AH019, AH020, AH021, AH023, AH026, AH029, AH031, AH033, AH034, AH036, AH037, AH038, AH039, AH043, AH044, AH047, AH048, AH050

**data/additional-raw — Anxiety (OK):**  
AA089, AA098

---

## 5. Dataset-Wide Summary Statistics

### data/raw (64 subjects, GNG–1backWM–SS–VF tasks)

| Metric | Healthy (36 subj) | Anxiety (28 subj) | All |
|--------|-------------------|-------------------|-----|
| Mean spike count | ~1,870 | ~1,780 | ~1,830 |
| Mean HbO/HbR corr | +0.22 | +0.21 | +0.21 |
| Mean signal scale | 2.69×10⁻⁷ M | 2.03×10⁻⁷ M | 2.44×10⁻⁷ M |
| HIGH-RISK | 4 (11%) | 3 (11%) | 7 (11%) |
| WATCH | 9 (25%) | 8 (29%) | 17 (26%) |
| OK | 23 (64%) | 17 (61%) | 40 (63%) |

### data/additional-raw (11 subjects, GNG+SS tasks)

| Metric | Value |
|--------|-------|
| Mean raw intensity CV | 5.9% (good: <7.5%) |
| Mean spike count | ~3,600 (higher than data/raw) |
| Mean HbO/HbR corr | +0.24 |
| Mean signal scale | 2.02×10⁻⁷ M |
| HIGH-RISK | 4 (36%) |
| WATCH | 5 (45%) |
| OK | 2 (18%) |

> The additional-raw group has higher motion artifact counts than data/raw overall. This may reflect the more recent recording protocol or the combined-session design (longer continuous recording = more opportunity for motion).

---

## 6. Recommendations for AI Training

### High priority actions

1. **Exclude or closely monitor HIGH-RISK subjects** in your cross-validation splits.  
   Consider running your experiments both with and without these 11 subjects to quantify their impact on model performance.

2. **Note: HIGH-RISK ≠ automatic exclusion.**  
   After motion correction (Wavelet + CBSI), some HIGH-RISK subjects may improve to an acceptable quality level. Re-assess post-correction.

3. **Balance check across groups:**  
   HIGH-RISK distribution is roughly equal between groups (11% anxiety, 11% healthy in data/raw), so excluding them should not create significant class imbalance.

4. **data/additional-raw subjects (AA089–AA099) have not had motion correction applied.**  
   Their higher spike counts are expected. Process with Wavelet + CBSI before final inclusion.

### Specific subject recommendations

| Subject | Dataset | Recommendation |
|---------|---------|----------------|
| LA063 | raw/anxiety | Highest combined risk score — consider excluding |
| AH024 | raw/healthy | Highest noise in healthy group — consider excluding |
| AH049 | raw/healthy | Highest spike count in healthy group — consider excluding |
| AA089 | add-raw | Cleanest additional-raw subject — reliable training sample |
| AA098 | add-raw | Second cleanest — reliable training sample |
| AA090 | add-raw | Very high motion — prioritize for motion correction |

---

## 7. Processing Pipeline Gap (Root Cause)

The current pipeline (`nirs2csv_homer3.m`) applies:
```
Intensity → OD → Bandpass(0.01–0.5 Hz) → Conc(HbO/HbR/HbT)
```

It is **missing**:
- Channel quality check before conversion
- Motion artifact correction (Wavelet, CBSI, Spline)

The positive HbO/HbR correlation observed across most subjects is a direct consequence of this omission — physiological noise (cardiac, Mayer waves) at frequencies below 0.5 Hz passes through the bandpass filter and remains in the signal.

**Recommended addition** (no channel removal — see §8):
```
Intensity → OD → WaveletCorrect → CBSI → Bandpass(0.01–0.5 Hz) → Conc
```

---

## 8. Channel Preservation Policy

All 23 channels are **mandatory** for this study's 5×7 grid encoding. The `hmrIntensityPrune` function (which removes bad channels) is therefore **not applicable** here.

Instead:
- **Identify** bad channels from raw CV metrics (flagged in additional-raw above) for reporting purposes only.
- **Apply motion correction** (Wavelet + CBSI) on all 23 channels without removal.
- Bad channels flagged in raw CV (AA094 ch, AA099 ch, LA096 ch) will retain noise, but RBF interpolation in `generate_matrix()` provides partial spatial smoothing from neighboring channels.

---

*Report generated from automated quality scan. All metrics are based on GNG task (data/raw) and GNG+SS tasks (data/additional-raw). Full per-task, per-channel breakdown available in `/tmp/fnirs_quality_full.csv`.*
