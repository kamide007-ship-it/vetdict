"""validators.py – Response validation and schema enforcement

Validates Claude responses, ensures symptom IDs are valid, and enforces
confidence thresholds. Provides fallback decision logic.
"""

import json
import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


def validate_claude_response(
    response: Dict[str, Any],
    symptom_ids: set,
    confidence_threshold: float = 0.7,
) -> Tuple[bool, List[str], str]:
    """
    Validate Claude response structure and content.

    Args:
        response: Parsed response dict from Claude
        symptom_ids: Set of valid symptom IDs
        confidence_threshold: Minimum confidence (0.0-1.0)

    Returns:
        Tuple of (is_valid, validated_symptoms, validation_message)
    """
    if not isinstance(response, dict):
        return False, [], "Response is not a dict"

    # Check required fields
    if "extracted_symptoms" not in response:
        return False, [], "Missing 'extracted_symptoms' field"

    symptoms = response.get("extracted_symptoms", [])
    if not isinstance(symptoms, list):
        return False, [], "'extracted_symptoms' is not a list"

    # Check confidence
    confidence = response.get("confidence", 0.0)
    try:
        confidence = float(confidence)
    except (ValueError, TypeError):
        return False, [], f"Invalid confidence value: {confidence}"

    if confidence < 0.0 or confidence > 1.0:
        return False, [], f"Confidence out of range: {confidence}"

    if confidence < confidence_threshold:
        return False, [], f"Confidence {confidence} below threshold {confidence_threshold}"

    # Validate symptom IDs
    invalid_symptoms = []
    valid_symptoms = []

    for symptom in symptoms:
        if not isinstance(symptom, str):
            invalid_symptoms.append(f"non-string: {symptom}")
            continue

        if symptom not in symptom_ids:
            invalid_symptoms.append(symptom)
        else:
            valid_symptoms.append(symptom)

    if invalid_symptoms:
        msg = f"Invalid symptom IDs: {invalid_symptoms}"
        logger.warning(msg)
        if not valid_symptoms:
            return False, [], msg

    return True, valid_symptoms, "OK"


def is_valid_symptom_id(symptom_id: str, symptom_ids_set: set) -> bool:
    """
    Check if symptom ID is valid.

    Args:
        symptom_id: Symptom ID to check
        symptom_ids_set: Set of valid IDs

    Returns:
        True if valid, False otherwise
    """
    return isinstance(symptom_id, str) and symptom_id in symptom_ids_set


def should_fallback(
    response: Optional[Dict[str, Any]],
    exception: Optional[Exception],
    confidence_threshold: float = 0.7,
) -> bool:
    """
    Determine if manual alias fallback should be used.

    Args:
        response: Claude response (None if API error)
        exception: Any exception that occurred
        confidence_threshold: Minimum acceptable confidence

    Returns:
        True if fallback should be used
    """
    # If there was an exception, always fallback
    if exception is not None:
        return True

    # If no response, fallback
    if response is None:
        return True

    # If response is not dict, fallback
    if not isinstance(response, dict):
        return True

    # If confidence too low, fallback
    try:
        confidence = float(response.get("confidence", 0.0))
        if confidence < confidence_threshold:
            return True
    except (ValueError, TypeError):
        return True

    # If no symptoms extracted, fallback
    symptoms = response.get("extracted_symptoms", [])
    if not isinstance(symptoms, list) or len(symptoms) == 0:
        return True

    return False


def parse_json_response(raw_response: str) -> Optional[Dict[str, Any]]:
    """
    Parse JSON response from Claude with fallback.

    Args:
        raw_response: Raw response string from Claude

    Returns:
        Parsed dict, or None on parse error
    """
    if not isinstance(raw_response, str):
        logger.warning(f"Response is not string: {type(raw_response)}")
        return None

    try:
        # Try direct parse
        return json.loads(raw_response)
    except json.JSONDecodeError:
        logger.debug(f"Failed to parse JSON: {raw_response[:100]}")

    # Try to extract JSON from markdown code blocks
    try:
        if "```json" in raw_response:
            start = raw_response.find("```json") + 7
            end = raw_response.find("```", start)
            if end > start:
                json_str = raw_response[start:end].strip()
                return json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        pass

    # Try to extract any JSON object
    try:
        start = raw_response.find("{")
        if start >= 0:
            # Find matching closing brace
            depth = 0
            for i, char in enumerate(raw_response[start:]):
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                    if depth == 0:
                        json_str = raw_response[start : start + i + 1]
                        return json.loads(json_str)
    except (json.JSONDecodeError, ValueError):
        pass

    logger.warning(f"Could not parse any JSON from response: {raw_response[:100]}")
    return None
