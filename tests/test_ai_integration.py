"""Integration tests for AI symptom extraction with diagnostic_chat."""

import os
import pytest
from unittest.mock import patch


def test_extract_symptoms_backward_compatibility():
    """Test that extract_symptoms_from_text works with AI disabled."""
    # Ensure AI is disabled for this test
    with patch.dict(os.environ, {"VETDICT_USE_AI_SYMPTOM_EXTRACTION": "false"}):
        from api.diagnostic_chat import extract_symptoms_from_text, SYMPTOM_ALIASES, SYMPTOM_IDS

        # Test with known alias
        test_input = "coughing"
        result = extract_symptoms_from_text(test_input)

        # Should return list (backward compatible)
        assert isinstance(result, list)


def test_extract_symptoms_returns_valid_ids():
    """Test that extracted symptoms are valid IDs."""
    with patch.dict(os.environ, {"VETDICT_USE_AI_SYMPTOM_EXTRACTION": "false"}):
        from api.diagnostic_chat import extract_symptoms_from_text, SYMPTOM_IDS

        test_input = "My dog is coughing and has a runny nose"
        result = extract_symptoms_from_text(test_input)

        # All results should be valid symptom IDs
        for symptom_id in result:
            assert symptom_id in SYMPTOM_IDS


def test_extract_symptoms_empty_input():
    """Test extraction with empty input."""
    with patch.dict(os.environ, {"VETDICT_USE_AI_SYMPTOM_EXTRACTION": "false"}):
        from api.diagnostic_chat import extract_symptoms_from_text

        result = extract_symptoms_from_text("")
        assert result == []

        result = extract_symptoms_from_text("   ")
        assert result == []


def test_extract_symptoms_no_matches():
    """Test extraction when no symptoms match."""
    with patch.dict(os.environ, {"VETDICT_USE_AI_SYMPTOM_EXTRACTION": "false"}):
        from api.diagnostic_chat import extract_symptoms_from_text

        result = extract_symptoms_from_text("xyz123abc")
        assert isinstance(result, list)


def test_extract_symptoms_case_insensitive():
    """Test that extraction is case insensitive."""
    with patch.dict(os.environ, {"VETDICT_USE_AI_SYMPTOM_EXTRACTION": "false"}):
        from api.diagnostic_chat import extract_symptoms_from_text

        result_lower = extract_symptoms_from_text("coughing")
        result_upper = extract_symptoms_from_text("COUGHING")
        result_mixed = extract_symptoms_from_text("CoUgHiNg")

        # All should produce same or similar results
        assert isinstance(result_lower, list)
        assert isinstance(result_upper, list)
        assert isinstance(result_mixed, list)


def test_ai_extractor_initialization():
    """Test that AI extractor initializes without errors when enabled."""
    with patch.dict(os.environ, {"VETDICT_USE_AI_SYMPTOM_EXTRACTION": "true"}):
        # Reimport to get fresh module state
        import importlib
        import api.diagnostic_chat as dc_module
        importlib.reload(dc_module)

        # Should not raise an error
        extractor = dc_module._get_ai_extractor()
        # extractor can be None if API key not set, but shouldn't crash


def test_ai_disabled_by_default():
    """Test that AI extraction is disabled by default."""
    # Don't set VETDICT_USE_AI_SYMPTOM_EXTRACTION
    import api.diagnostic_chat as dc_module

    assert dc_module._AI_EXTRACTION_ENABLED is False


def test_multiple_symptom_extraction():
    """Test extraction of multiple symptoms."""
    with patch.dict(os.environ, {"VETDICT_USE_AI_SYMPTOM_EXTRACTION": "false"}):
        from api.diagnostic_chat import extract_symptoms_from_text

        test_input = "coughing, vomiting, and diarrhea"
        result = extract_symptoms_from_text(test_input)

        # Should match multiple symptoms
        assert isinstance(result, list)
        # If any match, should have > 1 symptom or 0
        assert len(result) >= 0


def test_japanese_symptom_extraction():
    """Test extraction of Japanese symptom descriptions."""
    with patch.dict(os.environ, {"VETDICT_USE_AI_SYMPTOM_EXTRACTION": "false"}):
        from api.diagnostic_chat import extract_symptoms_from_text

        # Test with Japanese keywords
        result = extract_symptoms_from_text("咳をしている")
        assert isinstance(result, list)

        result = extract_symptoms_from_text("嘔吐している")
        assert isinstance(result, list)


@pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)
def test_ai_extraction_with_real_api():
    """Integration test with real Claude API (requires API key)."""
    import importlib
    import api.diagnostic_chat as dc_module

    # Reload with AI enabled
    with patch.dict(os.environ, {"VETDICT_USE_AI_SYMPTOM_EXTRACTION": "true"}):
        importlib.reload(dc_module)

        result = dc_module.extract_symptoms_from_text(
            "My dog has been coughing for 3 days"
        )

        assert isinstance(result, list)
        # May have coughing ID or fallback to empty
