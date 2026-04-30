#!/usr/bin/env bash
# Generate .npy epoch datasets from motion-corrected fNIRS CSVs using processor_cli.py.
#
# Iterates over all 4 tasks (GNG, 1backWM, VF, SS) × all 3 hemoglobin types
# (hbo, hbr, hbt) and calls processor_cli.py in batch mode for each combination.
# Epochs are saved as .npy files under OUTPUT_DIR.
#
# Flags (1 = enabled, 0 = disabled):
#   APPLY_BASELINE   Baseline correction via first Rest epoch   (default: 1)
#   APPLY_ZSCORE     Per-channel z-score normalization           (default: 1)
#   SAVE_PLOTS       Save evoked + time-marker PNGs per subject  (default: 1)
#
# Environment overrides:
#   ROOT_DIR         Input folder containing healthy/ and anxiety/ sub-dirs
#                    (default: data/raw_w_additional_mc)
#   OUTPUT_DIR       Output root for .npy files
#                    (default: data/processed-old-new-mc)
#   SUBJECTS_JSON    Path to subjects JSON; auto-discovered from ROOT_DIR if unset
#   MONTAGE_FILE     Path to .elc montage file
#                    (default: data/brainproducts-RNP-BA-128-custom.elc)
#
# Usage:
#   bash scripts/run_batch_npy.sh
#   ROOT_DIR=data/processed-mc bash scripts/run_batch_npy.sh
#   OUTPUT_DIR=data/my-output APPLY_ZSCORE=0 bash scripts/run_batch_npy.sh
#   SAVE_PLOTS=0 APPLY_BASELINE=0 bash scripts/run_batch_npy.sh

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# ── Toggles ───────────────────────────────────────────────────────────────────
APPLY_BASELINE="${APPLY_BASELINE:-1}"
APPLY_ZSCORE="${APPLY_ZSCORE:-1}"
SAVE_PLOTS="${SAVE_PLOTS:-1}"

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT_DIR="${ROOT_DIR:-${PROJECT_ROOT}/data/raw_w_additional_mc}"
OUTPUT_DIR="${OUTPUT_DIR:-${PROJECT_ROOT}/data/processed-old-new-mc}"
MONTAGE_FILE="${MONTAGE_FILE:-${PROJECT_ROOT}/data/brainproducts-RNP-BA-128-custom.elc}"
PROCESSOR="${PROJECT_ROOT}/data/processor_cli.py"
TMP_SUBJECTS_JSON="${PROJECT_ROOT}/data/_tmp_subjects_$$.json"

# ── Validation ────────────────────────────────────────────────────────────────
if [[ ! -f "${PROCESSOR}" ]]; then
    echo "ERROR: processor_cli.py not found: ${PROCESSOR}" >&2
    exit 1
fi

if [[ ! -d "${ROOT_DIR}" ]]; then
    echo "ERROR: ROOT_DIR does not exist: ${ROOT_DIR}" >&2
    exit 1
fi

if [[ ! -f "${MONTAGE_FILE}" ]]; then
    echo "WARNING: Montage file not found: ${MONTAGE_FILE}" >&2
    echo "         Proceeding without custom montage." >&2
    MONTAGE_FILE=""
fi

# ── Subject discovery ─────────────────────────────────────────────────────────
if [[ -n "${SUBJECTS_JSON:-}" && -f "${SUBJECTS_JSON}" ]]; then
    echo "Using provided SUBJECTS_JSON: ${SUBJECTS_JSON}"
else
    echo "Auto-discovering subjects from: ${ROOT_DIR}"
    SUBJECTS_JSON="${TMP_SUBJECTS_JSON}"

    python3 - "${ROOT_DIR}" "${SUBJECTS_JSON}" <<'PYEOF'
import json, os, sys

root, out = sys.argv[1], sys.argv[2]
result = {}
for group in ("healthy", "anxiety"):
    gdir = os.path.join(root, group)
    result[group] = sorted(
        d for d in os.listdir(gdir)
        if os.path.isdir(os.path.join(gdir, d))
    ) if os.path.isdir(gdir) else []

with open(out, "w") as f:
    json.dump(result, f, indent=2)

total = sum(len(v) for v in result.values())
for g, subs in result.items():
    print(f"  {g}: {len(subs)} subjects")
print(f"  Total: {total}")
PYEOF
fi

# ── Build flag array ──────────────────────────────────────────────────────────
FLAGS=()
[[ "${APPLY_BASELINE}" == "1" ]] && FLAGS+=(--apply-baseline)
[[ "${APPLY_ZSCORE}"   == "1" ]] && FLAGS+=(--apply-zscore)
[[ "${SAVE_PLOTS}"     == "1" ]] && FLAGS+=(--save-plots)

MONTAGE_ARGS=()
[[ -n "${MONTAGE_FILE}" ]] && MONTAGE_ARGS+=(--montage-file "${MONTAGE_FILE}")

# ── Summary ───────────────────────────────────────────────────────────────────
TASKS=("GNG" "1backWM" "VF" "SS")
DTYPES=("hbo" "hbr" "hbt")
TOTAL_RUNS=$(( ${#TASKS[@]} * ${#DTYPES[@]} ))

echo ""
echo "=== fNIRS batch .npy generator ==="
echo ""
echo "Root dir     : ${ROOT_DIR}"
echo "Output dir   : ${OUTPUT_DIR}"
echo "Montage      : ${MONTAGE_FILE:-<none>}"
echo "Subjects JSON: ${SUBJECTS_JSON}"
echo "Tasks        : ${TASKS[*]}"
echo "Data types   : ${DTYPES[*]}"
echo "apply-baseline : ${APPLY_BASELINE}"
echo "apply-zscore   : ${APPLY_ZSCORE}"
echo "save-plots     : ${SAVE_PLOTS}"
echo "Total runs   : ${TOTAL_RUNS}"
echo ""

mkdir -p "${OUTPUT_DIR}"

# ── Main loop ─────────────────────────────────────────────────────────────────
RUN=0
FAILED=()

for TASK in "${TASKS[@]}"; do
    for DTYPE in "${DTYPES[@]}"; do
        RUN=$(( RUN + 1 ))
        echo "--- [${RUN}/${TOTAL_RUNS}] task=${TASK}  dtype=${DTYPE} ---"

        if python3 "${PROCESSOR}" \
            --mode batch \
            --root-dir "${ROOT_DIR}" \
            --output-dir "${OUTPUT_DIR}" \
            --subjects-json "${SUBJECTS_JSON}" \
            --task "${TASK}" \
            --data-type "${DTYPE}" \
            --save-preprocessed \
            --save-format npy \
            "${MONTAGE_ARGS[@]+"${MONTAGE_ARGS[@]}"}" \
            "${FLAGS[@]+"${FLAGS[@]}"}"; then
            echo "    OK"
        else
            echo "    FAILED"
            FAILED+=("${TASK}/${DTYPE}")
        fi
        echo ""
    done
done

# ── Cleanup ───────────────────────────────────────────────────────────────────
[[ -f "${TMP_SUBJECTS_JSON}" ]] && rm -f "${TMP_SUBJECTS_JSON}"

# ── Result ────────────────────────────────────────────────────────────────────
echo "=== Done. Output: ${OUTPUT_DIR} ==="
if [[ ${#FAILED[@]} -gt 0 ]]; then
    echo ""
    echo "WARNING: ${#FAILED[@]} run(s) failed:"
    printf '  - %s\n' "${FAILED[@]}"
    exit 1
fi
