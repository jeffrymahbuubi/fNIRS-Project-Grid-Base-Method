#!/usr/bin/env bash
# Convert .nirs files in data/raw and data/additional-raw to motion-corrected
# HbO/HbR/HbT CSVs using nirs2csv_homer3_mc.m.
#
# Pipeline: Intensity → OD → WaveletMC → Bandpass → Conc(HbO/HbR/HbT) → CBSI
#
# CSVs are written to SAVE_DIR (default: data/processed-mc/), mirroring the
# source directory structure (group/subject/task/) so the output is directly
# usable as --root-dir for processor_cli.py.
#
# Environment overrides:
#   PPF="6 6"   Partial path-length factor per wavelength (default: [6 6])
#   IQR="1.5"   Wavelet IQR threshold — higher = less aggressive (default: 1.5)
#               Set IQR="-1" to skip Wavelet step (CBSI still applied).
#
# Usage:
#   bash scripts/run_homer3_nirs2csv_mc.sh                     # defaults
#   SAVE_DIR=/custom/path bash scripts/run_homer3_nirs2csv_mc.sh
#   PPF="1 1"  bash scripts/run_homer3_nirs2csv_mc.sh          # Molar*mm scale
#   IQR="2.0"  bash scripts/run_homer3_nirs2csv_mc.sh          # gentler wavelet
#   IQR="-1"   bash scripts/run_homer3_nirs2csv_mc.sh          # CBSI only
#
# Output structure:
#   SAVE_DIR/
#   ├── healthy/AH001/GNG/2021-03-04_004_HbO.csv
#   ├── healthy/AH001/GNG/2021-03-04_004_HbR.csv
#   ├── healthy/AH001/GNG/2021-03-04_004_HbT.csv
#   └── anxiety/AA089/SS/2025-07-02_001_HbO.csv ...
#
# Requirements: MATLAB with Homer3 available via Toolchain/Homer3/

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOLCHAIN_DIR="${PROJECT_ROOT}/references/synology_0331/clinical data/rawdata/data_NIRx/Toolchain"

# Source folders — both processed in sequence
RAW_DIR="${PROJECT_ROOT}/data/raw"
ADD_RAW_DIR="${PROJECT_ROOT}/data/additional-raw"

# Output directory (override via SAVE_DIR= env var)
SAVE_DIR="${SAVE_DIR:-${PROJECT_ROOT}/data/processed-mc}"

# Processing parameters (override via env vars)
PPF_ARG="${PPF:-6 6}"
PPF_MATLAB="[${PPF_ARG}]"
IQR_FACTOR="${IQR:-1.5}"

# ── Validation ────────────────────────────────────────────────────────────────
if [[ ! -d "${TOOLCHAIN_DIR}" ]]; then
    echo "ERROR: Toolchain directory not found: ${TOOLCHAIN_DIR}" >&2
    exit 1
fi

RAW_NIRS=0
ADD_NIRS=0

if [[ -d "${RAW_DIR}" ]]; then
    RAW_NIRS=$(find "${RAW_DIR}" -name "*.nirs" | wc -l)
else
    echo "WARNING: data/raw not found — skipping: ${RAW_DIR}"
fi

if [[ -d "${ADD_RAW_DIR}" ]]; then
    ADD_NIRS=$(find "${ADD_RAW_DIR}" -name "*.nirs" | wc -l)
else
    echo "WARNING: data/additional-raw not found — skipping: ${ADD_RAW_DIR}"
fi

TOTAL_NIRS=$((RAW_NIRS + ADD_NIRS))
if [[ "${TOTAL_NIRS}" -eq 0 ]]; then
    echo "ERROR: No .nirs files found in either source directory." >&2
    exit 1
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo "=== nirs2csv_homer3_mc batch converter (Wavelet + CBSI) ==="
echo ""
echo "Toolchain  : ${TOOLCHAIN_DIR}"
echo "Source 1   : ${RAW_DIR}  (${RAW_NIRS} .nirs files)"
echo "Source 2   : ${ADD_RAW_DIR}  (${ADD_NIRS} .nirs files)"
echo "Output     : ${SAVE_DIR}"
echo "PPF        : ${PPF_MATLAB}"
echo "IQR        : ${IQR_FACTOR}"
echo ""
echo "Total .nirs files to process: ${TOTAL_NIRS}"
echo ""

mkdir -p "${SAVE_DIR}"

# ── Process data/raw ──────────────────────────────────────────────────────────
if [[ "${RAW_NIRS}" -gt 0 ]]; then
    echo "--- Processing data/raw (${RAW_NIRS} files) ---"
    matlab -batch "addpath('${TOOLCHAIN_DIR}'); nirs2csv_homer3_mc('${RAW_DIR}', '${SAVE_DIR}', ${PPF_MATLAB}, 0.01, 0.5, ${IQR_FACTOR});"
    echo ""
fi

# ── Process data/additional-raw ───────────────────────────────────────────────
if [[ "${ADD_NIRS}" -gt 0 ]]; then
    echo "--- Processing data/additional-raw (${ADD_NIRS} files) ---"
    matlab -batch "addpath('${TOOLCHAIN_DIR}'); nirs2csv_homer3_mc('${ADD_RAW_DIR}', '${SAVE_DIR}', ${PPF_MATLAB}, 0.01, 0.5, ${IQR_FACTOR});"
    echo ""
fi

echo "=== Done. Motion-corrected CSVs written to: ${SAVE_DIR} ==="
echo ""
echo "To process with processor_cli.py, use:"
echo "  python data/processor_cli.py --mode batch --root-dir ${SAVE_DIR} ..."
