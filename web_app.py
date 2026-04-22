#!/usr/bin/env python3
"""
Web Server for VetDict Frontend
Lightweight HTTP server for static HTML/CSS/JS files
"""

import http.server
import os
import socketserver
from pathlib import Path


class SPAHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP handler that serves index.html for SPA routing"""

    def do_GET(self):
        """Handle GET requests with SPA fallback"""
        # Serve static files from the static directory
        self.path = f"/static{self.path}" if not self.path.startswith("/static") else self.path

        # For any path, try to serve the file
        try:
            # Remove /static prefix to get actual file path
            file_path = self.path.replace("/static/", "").replace("/static", "")

            if file_path.startswith("/"):
                file_path = file_path[1:]

            if not file_path:
                file_path = "index.html"

            full_path = Path("static") / file_path

            if full_path.exists() and full_path.is_file():
                # Serve the file
                return super().do_GET()
        except Exception:
            pass

        # For root or non-existent paths, serve index.html
        self.path = "/static/index.html"
        return super().do_GET()

    def end_headers(self):
        """Add CORS headers"""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{self.client_address[0]}] {format % args}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    port = int(os.getenv("PORT", 3000))
    handler = SPAHandler

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"✓ Web server running at http://0.0.0.0:{port}")
        print(f"✓ Serving files from: {os.path.abspath('static')}")
        print("✓ API endpoint: http://localhost:8000/api")
        print(f"\nOpen browser: http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✓ Server stopped")
