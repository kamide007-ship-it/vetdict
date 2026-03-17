"""Tests for AI validators module."""

from api.ai.validators import (
    is_valid_symptom_id,
    parse_json_response,
    should_fallback,
    validate_claude_response,
)


def test_validate_claude_response_valid():
    """Test validation of valid Claude response."""
    response = {
        "extracted_symptoms": ["coughing", "nasal_discharge"],
        "confidence": 0.95,
        "reasoning": "User mentioned coughing and runny nose",
    }
    symptom_ids = {"coughing", "nasal_discharge", "fever"}

    is_valid, symptoms, msg = validate_claude_response(
        response, symptom_ids, confidence_threshold=0.7
    )

    assert is_valid is True
    assert symptoms == ["coughing", "nasal_discharge"]
    assert msg == "OK"


def test_validate_claude_response_low_confidence():
    """Test validation fails when confidence below threshold."""
    response = {
        "extracted_symptoms": ["coughing"],
        "confidence": 0.5,
    }
    symptom_ids = {"coughing"}

    is_valid, symptoms, msg = validate_claude_response(
        response, symptom_ids, confidence_threshold=0.7
    )

    assert is_valid is False
    assert "confidence" in msg.lower()


def test_validate_claude_response_invalid_symptom():
    """Test validation with invalid symptom ID."""
    response = {
        "extracted_symptoms": ["coughing", "invalid_symptom"],
        "confidence": 0.95,
    }
    symptom_ids = {"coughing", "nasal_discharge"}

    is_valid, symptoms, msg = validate_claude_response(
        response, symptom_ids, confidence_threshold=0.7
    )

    # Should be valid but return only valid symptoms
    assert is_valid is True
    assert symptoms == ["coughing"]
    assert "invalid_symptom" not in symptoms


def test_validate_claude_response_missing_field():
    """Test validation fails when required field missing."""
    response = {
        "confidence": 0.95,
        # missing extracted_symptoms
    }
    symptom_ids = {"coughing"}

    is_valid, symptoms, msg = validate_claude_response(
        response, symptom_ids, confidence_threshold=0.7
    )

    assert is_valid is False
    assert "extracted_symptoms" in msg.lower()


def test_validate_claude_response_invalid_type():
    """Test validation fails when response is not dict."""
    is_valid, symptoms, msg = validate_claude_response(
        "not a dict", {"coughing"}, confidence_threshold=0.7
    )

    assert is_valid is False


def test_is_valid_symptom_id():
    """Test symptom ID validation."""
    symptom_ids = {"coughing", "nasal_discharge", "fever"}

    assert is_valid_symptom_id("coughing", symptom_ids) is True
    assert is_valid_symptom_id("invalid", symptom_ids) is False
    assert is_valid_symptom_id("", symptom_ids) is False
    assert is_valid_symptom_id(None, symptom_ids) is False


def test_should_fallback_on_exception():
    """Test fallback decision on exception."""
    assert should_fallback(None, Exception("API error")) is True
    assert should_fallback(None, TimeoutError("timeout")) is True


def test_should_fallback_low_confidence():
    """Test fallback decision on low confidence."""
    response = {"extracted_symptoms": ["coughing"], "confidence": 0.5}
    assert should_fallback(response, None, confidence_threshold=0.7) is True

    response = {"extracted_symptoms": ["coughing"], "confidence": 0.8}
    assert should_fallback(response, None, confidence_threshold=0.7) is False


def test_should_fallback_empty_symptoms():
    """Test fallback decision when no symptoms extracted."""
    response = {"extracted_symptoms": [], "confidence": 0.95}
    assert should_fallback(response, None) is True


def test_parse_json_response_valid():
    """Test parsing valid JSON response."""
    raw = '{"extracted_symptoms": ["coughing"], "confidence": 0.95}'
    result = parse_json_response(raw)

    assert result is not None
    assert result["extracted_symptoms"] == ["coughing"]
    assert result["confidence"] == 0.95


def test_parse_json_response_with_markdown():
    """Test parsing JSON wrapped in markdown code block."""
    raw = """Here's the result:
```json
{"extracted_symptoms": ["coughing"], "confidence": 0.95}
```
Done."""
    result = parse_json_response(raw)

    assert result is not None
    assert result["extracted_symptoms"] == ["coughing"]


def test_parse_json_response_invalid():
    """Test parsing invalid JSON."""
    raw = "not json {at all"
    result = parse_json_response(raw)

    assert result is None


def test_parse_json_response_invalid_type():
    """Test parsing when input is not string."""
    result = parse_json_response(123)
    assert result is None

    result = parse_json_response(None)
    assert result is None
