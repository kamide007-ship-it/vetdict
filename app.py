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
    from api.vetdict_api import app
except ImportError:
    from api.showdog_api import app

if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_DEBUG', '0') == '1')
