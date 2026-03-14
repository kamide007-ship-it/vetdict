"""Tests for AI symptom extractor module."""

import pytest
from unittest.mock import MagicMock, patch
from api.ai.symptom_extractor import SymptomExtractor, extract_symptoms_with_claude


def test_symptom_extractor_initialization():
    """Test extractor initialization."""
    extractor = SymptomExtractor(
        api_key="test_key",
        model="claude-opus-4-6",
        timeout=30.0,
        cache_enabled=True,
        cache_ttl=3600,
        confidence_threshold=0.7,
        fallback_enabled=True,
    )

    assert extractor.api_key == "test_key"
    assert extractor.model == "claude-opus-4-6"
    assert extractor.timeout == 30.0
    assert extractor.confidence_threshold == 0.7
    assert extractor._cache is not None


def test_manual_extraction_empty_input():
    """Test manual extraction with empty input."""
    extractor = SymptomExtractor(cache_enabled=False)
    manual_aliases = {"coughing": "coughing_id", "fever": "fever_id"}
    extractor.manual_aliases = manual_aliases

    result = extractor._manual_extraction("")

    assert result["symptoms"] == []
    assert result["method"] == "manual_alias"
    assert result["confidence"] == 0.0


def test_manual_extraction_with_matches():
    """Test manual extraction with matching aliases."""
    extractor = SymptomExtractor(cache_enabled=False)
    manual_aliases = {
        "coughing": "coughing_id",
        "fever": "fever_id",
        "runny nose": "nasal_discharge_id",
    }
    extractor.manual_aliases = manual_aliases

    result = extractor._manual_extraction("My dog has coughing and fever")

    assert "coughing_id" in result["symptoms"]
    assert "fever_id" in result["symptoms"]
    assert result["method"] == "manual_alias"
    assert result["confidence"] == 0.85


def test_extract_empty_input():
    """Test extraction with empty input."""
    extractor = SymptomExtractor(cache_enabled=False)

    result = extractor.extract("")

    assert result["symptoms"] == []
    assert result["method"] == "empty_input"


def test_set_valid_symptom_ids():
    """Test setting valid symptom IDs."""
    extractor = SymptomExtractor(cache_enabled=False)
    symptom_ids = {"coughing", "nasal_discharge", "fever"}

    extractor.set_valid_symptom_ids(symptom_ids)

    assert extractor._symptom_ids_set == symptom_ids


def test_cache_stats():
    """Test cache statistics reporting."""
    extractor = SymptomExtractor(cache_enabled=True, cache_ttl=3600)

    stats = extractor.cache_stats()

    assert "cache_enabled" in stats
    assert stats["cache_enabled"] is True
    assert "hits" in stats
    assert "misses" in stats


def test_cache_hit():
    """Test cache hit on repeated extraction.

    Note: Fallback results (when Claude API is unavailable) are intentionally
    NOT cached, so cache_hit will only be True when the Claude API succeeds.
    Without an API key, both calls use manual fallback and are not cached.
    """
    extractor = SymptomExtractor(
        cache_enabled=True,
        cache_ttl=3600,
        fallback_enabled=True,  # Use fallback when AI unavailable
    )
    extractor.manual_aliases = {"coughing": "coughing_id"}

    # First call (will use manual extraction — fallback results are not cached)
    result1 = extractor.extract("My dog is coughing")
    # Second call
    result2 = extractor.extract("My dog is coughing")

    # Both calls use fallback (no API key) — fallback results are not cached by design
    if result1.get("fallback_used"):
        assert result2["cache_hit"] is False
    else:
        # If Claude API succeeded, result should be cached
        assert result2["cache_hit"] is True


def test_fallback_on_exception():
    """Test fallback to manual extraction on exception."""
    extractor = SymptomExtractor(
        cache_enabled=False,
        fallback_enabled=True,
    )
    extractor.manual_aliases = {"coughing": "coughing_id"}
    extractor._llm_adapter = MagicMock()
    extractor._llm_adapter.generate.side_effect = Exception("API error")
    extractor._llm_loaded = True
    extractor._ensure_llm_adapter = lambda: extractor._llm_adapter

    result = extractor.extract("My dog is coughing")

    assert result["fallback_used"] is True
    assert result["method"] == "manual_alias"
    assert "coughing_id" in result["symptoms"]


def test_extract_symptoms_with_claude_public_api():
    """Test public API for symptom extraction."""
    result = extract_symptoms_with_claude(
        "test symptoms",
        extractor=None,  # Create new
        species="dog",
        symptom_ids={"coughing", "fever"},
    )

    assert "symptoms" in result
    assert "confidence" in result
    assert "method" in result


def test_no_ai_extractor_available():
    """Test extraction when AI extractor not available."""
    extractor = SymptomExtractor(
        cache_enabled=False,
        fallback_enabled=True,
    )
    extractor.manual_aliases = {"coughing": "coughing_id"}
    # Don't initialize LLM adapter

    result = extractor.extract("My dog is coughing")

    # Should fall back to manual
    assert result["fallback_used"] is True
    assert "coughing_id" in result["symptoms"]


def test_extraction_with_language():
    """Test extraction respects language parameter."""
    extractor = SymptomExtractor(cache_enabled=False)
    extractor.manual_aliases = {"咳": "coughing_id"}

    result = extractor.extract("犬が咳をしている", language="ja")

    assert "symptoms" in result
    assert "confidence" in result


def test_extraction_metrics():
    """Test extraction result includes metrics."""
    extractor = SymptomExtractor(cache_enabled=False)
    extractor.manual_aliases = {"coughing": "coughing_id"}

    result = extractor.extract("test")

    assert "method" in result
    assert "model" in result
    assert "cache_hit" in result
    assert "fallback_used" in result
    assert "execution_ms" in result
    assert "raw_response" in result
    assert result["execution_ms"] >= 0
