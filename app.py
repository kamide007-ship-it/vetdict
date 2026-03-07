#!/usr/bin/env python3
"""
Application entry point for ShowDog Analysis Platform.
Imports Flask app from API module for compatibility with tests and deployment.
"""

import os
import sys
from pathlib import Path

# Ensure API module is importable
root = Path(__file__).resolve().parent
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

# Import Flask app from API
try:
    from api.showdog_api import app
except ImportError:
    from showdog_api import app

if __name__ == "__main__":
    app.run(debug=os.getenv('FLASK_DEBUG', '0') == '1')
