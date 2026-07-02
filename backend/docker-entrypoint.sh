#!/usr/bin/env bash
# Container entrypoint for the LocalIntel AI backend.
#
# 1. Bootstrap model files (skips if already present in the named volume).
# 2. Hand off to uvicorn.
#
# Environment variables:
#   LOCALINTEL_SKIP_MODEL_DOWNLOAD=1   skip the download step (e.g. when
#                                      baking the model into the image)
#   LOCALINTEL_HOST  (default: 0.0.0.0)
#   LOCALINTEL_PORT  (default: 8000)
set -euo pipefail

cd /app

if [[ "${LOCALINTEL_SKIP_MODEL_DOWNLOAD:-0}" != "1" ]]; then
    echo "[entrypoint] Checking for AI model files…"
    python scripts/download_models.py || {
        echo "[entrypoint] WARNING: model download failed; app will use deterministic fallback."
    }
else
    echo "[entrypoint] LOCALINTEL_SKIP_MODEL_DOWNLOAD=1; skipping model download."
fi

# Ensure outputs/ is writable for SQLite + uploaded files.
mkdir -p /app/outputs
chmod -R 0777 /app/outputs || true

HOST="${LOCALINTEL_HOST:-0.0.0.0}"
PORT="${LOCALINTEL_PORT:-8000}"

echo "[entrypoint] Starting uvicorn on ${HOST}:${PORT}"
exec uvicorn app.main:app \
    --host "${HOST}" \
    --port "${PORT}" \
    --proxy-headers \
    --forwarded-allow-ips="*"
