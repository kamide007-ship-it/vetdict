"""Tests for Stage 9: Frontend Integration.

Tests HTML/CSS/JS integration and API frontend compatibility.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _read_all_multidisease_css():
    """Read all multi-disease CSS files (main + split components)."""
    css_dir = PROJECT_ROOT / "static" / "css"
    content = ""
    for css_file in sorted(css_dir.glob("multidisease-*.css")):
        content += css_file.read_text() + "\n"
    return content


class TestFrontendAssets:
    """Test frontend asset files exist and are valid."""

    def test_multidisease_css_exists(self):
        """Test that multi-disease CSS file exists."""
        css_path = PROJECT_ROOT / "static" / "css" / "multidisease-ui.css"
        assert css_path.exists(), "multidisease-ui.css should exist"

    def test_multidisease_js_exists(self):
        """Test that multi-disease JavaScript file exists."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        assert js_path.exists(), "multidisease-ui.js should exist"

    def test_css_contains_required_classes(self):
        """Test that CSS includes all required UI classes (across split files)."""
        css_content = _read_all_multidisease_css()

        required_classes = [
            ".multidisease-badge",
            ".multidisease-combinations",
            ".combination-item",
            ".ambiguity-section",
            ".clarifying-questions",
            ".confidence-breakdown",
        ]

        for css_class in required_classes:
            assert css_class in css_content, f"{css_class} should be in CSS"

    def test_js_contains_required_methods(self):
        """Test that JavaScript includes required methods."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        required_methods = [
            "class MultiDiseaseUIHandler",
            "init()",
            "performMultiDiseaseAnalysis",
            "renderMultiDiseaseUI",
            "renderCombinations",
            "renderAmbiguityAnalysis",
            "renderConfidenceBreakdown",
            "renderClarifyingQuestions",
        ]

        for method in required_methods:
            assert method in js_content, f"{method} should be in JavaScript"


class TestHTMLIntegration:
    """Test HTML includes frontend assets."""

    def test_html_includes_multidisease_css(self):
        """Test that index.html includes main CSS (which now contains multidisease styles)."""
        html_path = PROJECT_ROOT / "templates" / "index.html"
        html_content = html_path.read_text()

        assert "main.css" in html_content, "CSS should be linked in HTML"

    def test_html_includes_multidisease_js(self):
        """Test that index.html includes app JS (which now contains multidisease scripts)."""
        html_path = PROJECT_ROOT / "templates" / "index.html"
        html_content = html_path.read_text()

        assert "app.js" in html_content, "JS should be linked in HTML"

    def test_css_loaded_before_body_content(self):
        """Test that CSS is loaded in head before body."""
        html_path = PROJECT_ROOT / "templates" / "index.html"
        html_content = html_path.read_text()

        css_index = html_content.find("main.css")
        body_index = html_content.find("<body")

        assert css_index < body_index, "CSS should be in <head>, before <body>"

    def test_js_loaded_at_end_of_body(self):
        """Test that JavaScript is loaded at end of body."""
        html_path = PROJECT_ROOT / "templates" / "index.html"
        html_content = html_path.read_text()

        js_index = html_content.find("app.js")
        body_end = html_content.rfind("</body>")

        assert js_index > body_end - 500, "JS should be near end of body"


class TestCSSValidation:
    """Test CSS syntax and completeness (across split component files)."""

    def test_css_valid_syntax(self):
        """Test that CSS files have valid syntax."""
        css_content = _read_all_multidisease_css()

        # Basic syntax checks
        opening_braces = css_content.count("{")
        closing_braces = css_content.count("}")
        assert opening_braces == closing_braces, "CSS braces should be balanced"

    def test_css_has_media_queries(self):
        """Test that CSS includes responsive design."""
        css_content = _read_all_multidisease_css()

        assert "@media" in css_content, "CSS should include media queries"
        assert "max-width" in css_content, "CSS should have responsive rules"

    def test_css_has_animations(self):
        """Test that CSS includes animations."""
        css_content = _read_all_multidisease_css()

        assert "@keyframes" in css_content, "CSS should include animations"
        assert "animation:" in css_content, "CSS should use animations"

    def test_css_has_accessibility_styles(self):
        """Test that CSS includes accessibility features."""
        css_content = _read_all_multidisease_css()

        assert ":focus" in css_content, "CSS should include focus styles"
        assert "outline" in css_content, "CSS should include outline for focus"


class TestJSValidation:
    """Test JavaScript code quality."""

    def test_js_valid_javascript_syntax(self):
        """Test that JavaScript has valid syntax."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        # Basic syntax checks
        opening_braces = js_content.count("{")
        closing_braces = js_content.count("}")
        assert opening_braces == closing_braces, "JS braces should be balanced"

    def test_js_has_error_handling(self):
        """Test that JavaScript includes error handling."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        assert "catch" in js_content, "JS should include error handling"
        assert "try" in js_content, "JS should include try blocks"

    def test_js_api_endpoint_defined(self):
        """Test that API endpoint is properly defined."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        assert "/api/multidisease/analyze" in js_content, "API endpoint should be defined"

    def test_js_event_listeners_setup(self):
        """Test that JavaScript sets up event listeners."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        assert "addEventListener" in js_content, "Should setup event listeners"
        assert "setupEventListeners" in js_content, "Should have event setup method"

    def test_js_has_initialization_logic(self):
        """Test that JavaScript initializes on page load."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        assert "DOMContentLoaded" in js_content, "Should initialize on DOM ready"
        assert "window.multiDiseaseUI" in js_content, "Should expose global instance"


class TestJavaScriptClasses:
    """Test JavaScript class structure."""

    def test_multi_disease_ui_handler_class_exists(self):
        """Test that MultiDiseaseUIHandler class is defined."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        assert "class MultiDiseaseUIHandler" in js_content

    def test_class_has_required_properties(self):
        """Test that class has required properties."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        properties = [
            "this.currentAnalysis",
            "this.apiEndpoint",
            "this.containerSelector",
        ]

        for prop in properties:
            assert prop in js_content, f"{prop} should be defined"

    def test_class_has_render_methods(self):
        """Test that class has all rendering methods."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        methods = [
            "renderCombinations",
            "renderAmbiguityAnalysis",
            "renderConfidenceBreakdown",
            "renderClarifyingQuestions",
            "renderUserGuidance",
        ]

        for method in methods:
            assert method in js_content, f"{method} should be defined"


class TestAPIFrontendIntegration:
    """Test frontend-API integration compatibility."""

    def test_api_request_structure(self):
        """Test that API request has correct structure."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        # Check for correct JSON structure
        assert "symptom_ids" in js_content
        assert "suspected_diseases" in js_content
        assert 'method: "POST"' in js_content or "method: 'POST'" in js_content

    def test_api_response_handling(self):
        """Test that API response is properly handled."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        # Check for response parsing
        assert "response.json()" in js_content
        assert "data.multidisease_mode_enabled" in js_content or "analysis.multidisease_mode_enabled" in js_content


class TestUIComponents:
    """Test that all UI components are defined."""

    def test_all_render_methods_exist(self):
        """Test that all render methods are implemented."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        components = [
            "renderMultiDiseaseUI",
            "createModeBadge",
            "renderCombinations",
            "renderAmbiguityAnalysis",
            "renderConfidenceBreakdown",
            "renderClarifyingQuestions",
            "renderUserGuidance",
        ]

        for component in components:
            assert component in js_content, f"{component} should exist"

    def test_container_management(self):
        """Test container management methods."""
        js_path = PROJECT_ROOT / "static" / "js" / "multidisease-ui.js"
        js_content = js_path.read_text()

        methods = [
            "getOrCreateContainer",
            "showLoading",
            "showError",
            "clearMultiDiseaseUI",
        ]

        for method in methods:
            assert method in js_content, f"{method} should exist"
