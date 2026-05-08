#!/usr/bin/env python3
"""
VetDict — Multi-Species Veterinary Diagnostic Platform
Entry point: imports Flask app from API module.

Production: use gunicorn (see Procfile / render.yaml)
  gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --preload

Development only: python app.py
"""

import os
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

try:
    from api.vetdict_api import app, is_debug_mode_enabled
except ImportError:
    from api.showdog_api import app, is_debug_mode_enabled

if __name__ == "__main__":
    port = int(os.getenv("PORT") or 5000)
    debug = is_debug_mode_enabled()
    if not debug:
        print(
            "WARNING: Running Flask dev server in production. Use 'gunicorn app:app' instead. See Procfile.",
            file=sys.stderr,
        )
    app.run(host="0.0.0.0", port=port, debug=debug)
