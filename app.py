#!/usr/bin/env python3
"""
VetDict — Multi-Species Veterinary Diagnostic Platform
Entry point: imports Flask app from API module.
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
    port = int(os.getenv('PORT') or 5000)
    app.run(host="0.0.0.0", port=port, debug=is_debug_mode_enabled())
