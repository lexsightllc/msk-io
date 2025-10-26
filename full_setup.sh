#!/usr/bin/env bash
# SPDX-License-Identifier: MPL-2.0
set -euo pipefail

# --- Configuration ---
VENV_DIR="./.venv"
CHROMIUM_BOOTSTRAP="./bootstrap_chromium.sh"
PYTHON_BOOTSTRAP="./bootstrap_pipeline.py"
CHROMIUM_ARCHIVE="./assets/resources/chromium/chromium.tar.xz"

# --- Ensure toolchain ---
./scripts/bootstrap

# --- Run quality gates ---
./scripts/check

# --- Validate Chromium setup ---
if ! command -v chromium-browser &> /dev/null && [ ! -f "$CHROMIUM_ARCHIVE" ]; then
    echo "❌ Chromium not found and no local archive present: $CHROMIUM_ARCHIVE"
    echo "Please download a compatible Chromium binary and place it there."
    exit 1
fi
bash "$CHROMIUM_BOOTSTRAP"

# --- Launch pipeline ---
if [ -z "${MSK_REMOTE_URL:-}" ] || [ -z "${MSK_AUTH_TOKEN:-}" ]; then
    echo "❌ MSK_REMOTE_URL and MSK_AUTH_TOKEN must be set as environment variables."
    exit 1
fi
python "$PYTHON_BOOTSTRAP"
