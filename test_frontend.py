#!/usr/bin/env python3
"""
Frontend Integration Tests
Tests the HTML/CSS/JS frontend and API integration
"""

import os
import json
from pathlib import Path


def test_frontend_files_exist():
    """Check that all frontend files exist"""
    files = [
        'static/index.html',
        'static/css/app.css',
        'static/js/app.js',
        'web_app.py'
    ]

    for file in files:
        path = Path(file)
        assert path.exists(), f"Missing file: {file}"
        print(f"✓ {file} exists")


def test_html_structure():
    """Validate HTML structure"""
    with open('static/index.html', 'r') as f:
        html = f.read()

    assert '<html' in html, "Missing <html> tag"
    assert '<head>' in html, "Missing <head> tag"
    assert '<body>' in html, "Missing <body> tag"
    assert 'id="root"' in html, "Missing root div"
    assert 'react.min.js' in html, "Missing React script"
    assert 'app.js' in html, "Missing app.js script"
    assert 'app.css' in html, "Missing app.css stylesheet"

    print("✓ HTML structure valid")


def test_css_content():
    """Validate CSS has required styles"""
    with open('static/css/app.css', 'r') as f:
        css = f.read()

    required = [
        '.header',
        '.disease-card',
        '.disease-list',
        '.search-section',
        '.pagination',
        '.stats-grid',
        '.disease-badge',
        '.tab-button'
    ]

    for selector in required:
        assert selector in css, f"Missing CSS selector: {selector}"
        print(f"✓ {selector} CSS defined")


def test_javascript_structure():
    """Validate JavaScript has required components"""
    with open('static/js/app.js', 'r') as f:
        js = f.read()

    required = [
        'const API =',
        'const DiseaseCard =',
        'const StatCard =',
        'const PaginationControls =',
        'const VetDictApp =',
        'API_BASE',
        'health:',
        'diseases:',
        'search:',
        'useState',
        'useEffect',
        'ReactDOM.createRoot'
    ]

    for item in required:
        assert item in js, f"Missing JavaScript component: {item}"
        print(f"✓ {item} found")


def test_api_endpoints_in_code():
    """Verify API endpoints match FastAPI implementation"""
    with open('static/js/app.js', 'r') as f:
        js = f.read()

    endpoints = [
        '/health',
        '/diseases',
        '/diseases/search',
        '/species',
        '/stats'
    ]

    for endpoint in endpoints:
        assert endpoint in js, f"Missing API endpoint in code: {endpoint}"
        print(f"✓ API endpoint {endpoint} referenced")


def test_web_app_config():
    """Test web_app.py configuration"""
    with open('web_app.py', 'r') as f:
        code = f.read()

    required = [
        'Flask',
        'CORS',
        'static_folder',
        "route('/')",
        'index.html',
        '404'
    ]

    for item in required:
        assert item in code, f"Missing configuration: {item}"
        print(f"✓ {item} configured")


def test_responsive_design():
    """Verify responsive CSS is present"""
    with open('static/css/app.css', 'r') as f:
        css = f.read()

    responsive = [
        '@media (max-width: 768px)',
        '@media (max-width: 480px)',
        'grid-template-columns: repeat(auto-fit'
    ]

    for media in responsive:
        assert media in css, f"Missing responsive rule: {media}"
        print(f"✓ Responsive design: {media}")


def test_color_scheme():
    """Verify color scheme is defined"""
    with open('static/css/app.css', 'r') as f:
        css = f.read()

    colors = [
        '--primary',
        '--secondary',
        '--success',
        '--danger',
        '--dark',
        '--light'
    ]

    for color in colors:
        assert color in css, f"Missing color variable: {color}"
        print(f"✓ Color variable {color} defined")


if __name__ == '__main__':
    print("=" * 70)
    print("VetDict Frontend Test Suite")
    print("=" * 70)

    tests = [
        test_frontend_files_exist,
        test_html_structure,
        test_css_content,
        test_javascript_structure,
        test_api_endpoints_in_code,
        test_web_app_config,
        test_responsive_design,
        test_color_scheme,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            print(f"\n{test.__name__}:")
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)

    if failed == 0:
        print("\n✅ All frontend tests passed!")
        print("\nTo run the application:")
        print("  Terminal 1: python3 -m uvicorn fastapi_app:app --host 0.0.0.0 --port 8000")
        print("  Terminal 2: python3 web_app.py")
        print("  Browser: http://localhost:3000")

    exit(0 if failed == 0 else 1)
