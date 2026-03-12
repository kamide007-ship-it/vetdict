"""AI Integration Module – Claude-based diagnostic support

Provides symptom extraction, caching, and prompt management for AI-powered
veterinary diagnostic assistance.
"""

from api.ai.cache_manager import SymptomCache
from api.ai.prompt_manager import PromptManager, build_symptom_extraction_prompt
from api.ai.symptom_extractor import SymptomExtractor, extract_symptoms_with_claude
from api.ai.validators import (
    parse_json_response,
    should_fallback,
    validate_claude_response,
)

__all__ = [
    "SymptomExtractor",
    "SymptomCache",
    "PromptManager",
    "extract_symptoms_with_claude",
    "build_symptom_extraction_prompt",
    "validate_claude_response",
    "should_fallback",
    "parse_json_response",
]
