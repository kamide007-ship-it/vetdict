#!/bin/bash
# VetDict production startup script
# Handles $PORT env var fallback (Render sets PORT=10000 by default)
set -e

PORT="${PORT:-10000}"

exec gunicorn app:app \
  --bind "0.0.0.0:${PORT}" \
  --workers 1 \
  --threads 2 \
  --timeout 120 \
  --preload \
  --access-logfile - \
  --error-logfile -
