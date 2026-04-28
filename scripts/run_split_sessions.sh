#!/usr/bin/env bash
# run_split_sessions.sh — Split combined GNG+SS CSVs into per-task windows.
#
# Run AFTER run_homer3_nirs2csv.sh.  Overwrites the identical combined CSV
# in each task folder with a task-specific time window so that
# processor_cli.py can process new subjects without changes to event logic.
#
# Usage:
#   bash scripts/run_split_sessions.sh [additional_raw_dir]
#
# Default additional_raw_dir: data/additional-raw (relative to project root).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

ADDITIONAL_RAW="${1:-$PROJECT_ROOT/data/additional-raw}"
TOOLCHAIN_DIR="$PROJECT_ROOT/references/synology_0331/clinical data/rawdata/data_NIRx/Toolchain"

if [[ ! -d "$ADDITIONAL_RAW" ]]; then
    echo "ERROR: additional-raw directory not found: $ADDITIONAL_RAW" >&2
    exit 1
fi

if [[ ! -f "$TOOLCHAIN_DIR/split_combined_sessions.m" ]]; then
    echo "ERROR: split_combined_sessions.m not found in Toolchain." >&2
    exit 1
fi

echo "Splitting combined session CSVs in: $ADDITIONAL_RAW"

matlab -batch "addpath('${TOOLCHAIN_DIR}'); split_combined_sessions('${ADDITIONAL_RAW}');"

echo "Done. Task-specific CSVs written to each task folder."
