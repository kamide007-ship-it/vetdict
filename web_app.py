#!/usr/bin/env python3
"""
Web Server for VetDict Frontend
Serves static HTML/CSS/JS files and proxies API calls to FastAPI backend
"""

from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')


@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory(STATIC_DIR, 'index.html')


@app.route('/api/<path:subpath>')
def proxy_api(subpath):
    """
    Note: In production, use a proper reverse proxy (nginx) or
    update frontend to call API directly with CORS headers
    """
    return {'error': 'Use API_BASE=http://localhost:8000/api in frontend'}, 400


@app.errorhandler(404)
def not_found(error):
    """Serve index.html for all non-API routes (SPA support)"""
    return send_from_directory(STATIC_DIR, 'index.html')


if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.getenv('FLASK_DEBUG', '0') == '1'
    )
