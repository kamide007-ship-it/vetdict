"""symptom_extractor.py – Claude-based natural language symptom extraction

Converts natural language symptom descriptions into standardized symptom IDs
with intelligent fallback to manual alias matching, symptom interactions,
and patient personalization.
"""

import logging
import os
import time
from typing import Any, Dict, List, Optional

from api.ai.cache_manager import SymptomCache
from api.ai.patient_personalization import (
    personalize_extraction_result,
)
from api.ai.prompt_manager import build_symptom_extraction_prompt
from api.ai.symptom_interactions import SymptomInteractionMatrix
from api.ai.validators import (
    parse_json_response,
    should_fallback,
    validate_claude_response,
)

logger = logging.getLogger(__name__)


class SymptomExtractor:
    """Claude-based symptom extractor with fallback and caching."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "claude-opus-4-6",
        timeout: float = 30.0,
        cache_enabled: bool = True,
        cache_ttl: int = 3600,
        confidence_threshold: float = 0.7,
        fallback_enabled: bool = True,
        manual_aliases: Optional[Dict[str, str]] = None,
        diseases: Optional[List[Dict[str, Any]]] = None,
        enable_interactions: bool = True,
        enable_personalization: bool = True,
    ):
        """
        Initialize symptom extractor.

        Args:
            api_key: Anthropic API key (uses env if None)
            model: Claude model name
            timeout: API timeout in seconds
            cache_enabled: Enable response caching
            cache_ttl: Cache time-to-live in seconds
            confidence_threshold: Min confidence for accepting response
            fallback_enabled: Enable fallback to manual aliases
            manual_aliases: Manual alias dict {alias: symptom_id}
            diseases: Disease list for Phase 2a (interactions, personalization)
            enable_interactions: Enable symptom interaction analysis (Phase 2a)
            enable_personalization: Enable patient personalization (Phase 2a)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self.timeout = timeout
        self.confidence_threshold = confidence_threshold
        self.fallback_enabled = fallback_enabled
        self.manual_aliases = manual_aliases or {}
        self.enable_interactions = enable_interactions
        self.enable_personalization = enable_personalization

        self._cache = SymptomCache(ttl_seconds=cache_ttl) if cache_enabled else None
        self._llm_adapter = None
        self._symptom_ids_set: set = set()

        # Phase 2a: Symptom interactions and personalization
        self._interaction_matrix: Optional[SymptomInteractionMatrix] = None
        if enable_interactions and diseases:
            try:
                self._interaction_matrix = SymptomInteractionMatrix(diseases)
            except Exception as e:
                logger.warning(f"Failed to initialize SymptomInteractionMatrix: {e}")

        # Lazy load LLM adapter on first use
        self._llm_loaded = False

    def _ensure_llm_adapter(self) -> bool:
        """Load LLM adapter if needed. Returns True if available."""
        if self._llm_loaded:
            return self._llm_adapter is not None

        try:
            from reco2.llm_adapter import ClaudeAdapter

            self._llm_adapter = ClaudeAdapter(api_key=self.api_key)
            self._llm_loaded = True
            return True
        except Exception as e:
            logger.warning(f"Failed to load ClaudeAdapter: {e}")
            self._llm_loaded = True
            self._llm_adapter = None
            return False

    def set_valid_symptom_ids(self, symptom_ids: set) -> None:
        """Set valid symptom IDs for validation."""
        self._symptom_ids_set = symptom_ids

    def _manual_extraction(self, text: str) -> Dict[str, Any]:
        """
        Extract symptoms using manual alias matching.

        Args:
            text: User input text

        Returns:
            Extraction result dict
        """
        start_time = time.time()
        text_lower = text.lower()
        matched_symptoms = set()

        for alias, symptom_id in self.manual_aliases.items():
            if alias.lower() in text_lower:
                matched_symptoms.add(symptom_id)

        elapsed_ms = int((time.time() - start_time) * 1000)

        return {
            "symptoms": list(matched_symptoms),
            "confidence": 0.85 if matched_symptoms else 0.0,
            "method": "manual_alias",
            "model": "manual",
            "cache_hit": False,
            "fallback_used": False,
            "execution_ms": elapsed_ms,
            "raw_response": None,
        }

    def extract(
        self,
        text: str,
        language: str = "auto",
        patient_species: str = "dog",
        allow_fallback: bool = True,
    ) -> Dict[str, Any]:
        """
        Extract symptom IDs from natural language text.

        Attempts Claude API first, falls back to manual aliases on failure.

        Args:
            text: User symptom description
            language: "en", "ja", or "auto"
            patient_species: Animal species (dog, cat, etc.)
            allow_fallback: Allow fallback to manual aliases

        Returns:
            Dict with extracted symptoms, confidence, and metadata
        """
        start_time = time.time()

        # Normalize input
        if not isinstance(text, str):
            text = str(text)
        text = text.strip()

        if not text:
            return {
                "symptoms": [],
                "confidence": 0.0,
                "method": "empty_input",
                "model": self.model,
                "cache_hit": False,
                "fallback_used": False,
                "execution_ms": 0,
                "raw_response": None,
            }

        # Check cache
        if self._cache is not None:
            cached = self._cache.get(text)
            if cached is not None:
                logger.debug("Cache hit for symptom extraction")
                return {
                    **cached,
                    "cache_hit": True,
                    "execution_ms": int((time.time() - start_time) * 1000),
                }

        # Try Claude API
        result = self._extract_with_claude(
            text=text,
            language=language,
            patient_species=patient_species,
        )

        # Check if we should fallback
        if allow_fallback and should_fallback(
            result.get("raw_response"),
            result.get("_exception"),
            self.confidence_threshold,
        ):
            if self.fallback_enabled:
                logger.debug(f"Falling back to manual extraction: {result.get('_reason')}")
                manual_result = self._manual_extraction(text)
                manual_result["fallback_used"] = True
                # Don't cache fallback results
                elapsed_ms = int((time.time() - start_time) * 1000)
                manual_result["execution_ms"] = elapsed_ms
                result = {k: v for k, v in manual_result.items() if not k.startswith("_")}
            else:
                # Remove internal fields
                result = {k: v for k, v in result.items() if not k.startswith("_")}
        else:
            # Remove internal fields and cache successful result
            result_clean = {k: v for k, v in result.items() if not k.startswith("_")}
            if self._cache is not None:
                self._cache.set(text, result_clean)
            result = result_clean

        # Phase 2a: Add symptom interactions and personalization metadata
        result = self._enhance_with_phase2a(result, text)

        elapsed_ms = int((time.time() - start_time) * 1000)
        result["execution_ms"] = elapsed_ms
        return result

    def _extract_with_claude(
        self,
        text: str,
        language: str,
        patient_species: str,
    ) -> Dict[str, Any]:
        """
        Internal method to call Claude API.

        Args:
            text: User input
            language: Language code
            patient_species: Species

        Returns:
            Result dict with internal fields starting with _
        """
        time.time()

        # Ensure LLM adapter is available
        if not self._ensure_llm_adapter():
            return {
                "symptoms": [],
                "confidence": 0.0,
                "method": "claude_unavailable",
                "model": self.model,
                "cache_hit": False,
                "fallback_used": False,
                "raw_response": None,
                "_exception": None,
                "_reason": "LLM adapter not available",
            }

        # Build prompt
        symptom_list = sorted(list(self._symptom_ids_set)) if self._symptom_ids_set else []
        system_prompt, user_prompt = build_symptom_extraction_prompt(
            user_input=text,
            species=patient_species,
            symptoms_list=symptom_list,
            language=language,
        )

        # Call Claude
        exception = None
        raw_response = None

        try:
            result = self._llm_adapter.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3,
                max_tokens=500,
            )
            raw_response = result.get("text", "") if result else None
        except TimeoutError as e:
            exception = e
            logger.warning(f"Claude API timeout: {e}")
        except Exception as e:
            exception = e
            logger.warning(f"Claude API error: {e}")

        # Parse response
        if raw_response:
            parsed = parse_json_response(raw_response)
            if parsed:
                is_valid, symptoms, msg = validate_claude_response(
                    parsed,
                    self._symptom_ids_set,
                    self.confidence_threshold,
                )
                if is_valid:
                    confidence = float(parsed.get("confidence", 0.0))
                    return {
                        "symptoms": symptoms,
                        "confidence": round(confidence, 3),
                        "method": "claude",
                        "model": self.model,
                        "cache_hit": False,
                        "fallback_used": False,
                        "raw_response": parsed,
                        "_exception": None,
                        "_reason": None,
                    }
                else:
                    exception = ValueError(f"Validation failed: {msg}")

        return {
            "symptoms": [],
            "confidence": 0.0,
            "method": "claude_failed",
            "model": self.model,
            "cache_hit": False,
            "fallback_used": False,
            "raw_response": raw_response,
            "_exception": exception,
            "_reason": str(exception) if exception else "No response",
        }

    def _enhance_with_phase2a(self, result: Dict[str, Any], text: str) -> Dict[str, Any]:
        """
        Enhance extraction result with Phase 2a data (interactions, personalization).

        Args:
            result: Extraction result from Phase 1
            text: Original user input

        Returns:
            Enhanced result with interactions and personalization metadata
        """
        # Phase 2a: Symptom interactions
        if self.enable_interactions and self._interaction_matrix:
            symptoms = result.get("symptoms", [])
            interactions = self._interaction_matrix.find_interactions(symptoms, weight_threshold=0.1)

            if interactions:
                # Apply confidence boost from strongest interaction
                original_confidence = result.get("confidence", 0.85)
                strongest_weight = interactions[0]["weight"]
                boost = strongest_weight * 0.15  # Max 15% boost
                result["confidence"] = min(original_confidence + boost, 1.0)

                result["interactions"] = interactions
            else:
                result["interactions"] = []
        else:
            result["interactions"] = []

        # Phase 2a: Patient personalization
        if self.enable_personalization:
            result = personalize_extraction_result(result, text)
        else:
            result["personalization"] = {
                "age_stage": None,
                "extracted_age_years": None,
                "severity": "moderate",
                "extraction_method": "disabled",
                "confidence": 0.5,
            }

        return result

    def extract_with_calibration(
        self,
        text: str,
        language: str = "auto",
        patient_species: str = "dog",
        allow_fallback: bool = True,
    ) -> Dict[str, Any]:
        """
        Extract symptoms with Phase 3 confidence calibration.

        Calls extract() and applies automatic confidence calibration based on
        historical AI accuracy per domain.

        Args:
            text: User symptom description
            language: "en", "ja", or "auto"
            patient_species: Animal species (dog, cat, etc.)
            allow_fallback: Allow fallback to manual aliases

        Returns:
            Extraction result with calibrated confidence
        """
        # Phase 1-2: Get extraction with interactions and personalization
        result = self.extract(text, language, patient_species, allow_fallback)

        # Phase 3: Apply confidence calibration
        try:
            from api.ai.confidence_calibration import ConfidenceCalibrator

            calibrator = ConfidenceCalibrator()
            result = calibrator.calibrate_extraction_result(result)
        except Exception as e:
            # Graceful degradation: calibration not critical to extraction
            logger.debug(f"Confidence calibration failed: {e}")
            # Result already has raw confidence, calibration just wasn't applied

        return result

    def cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if self._cache is None:
            return {"cache_enabled": False}
        return {"cache_enabled": True, **self._cache.stats()}


def extract_symptoms_with_claude(
    text: str,
    extractor: Optional[SymptomExtractor] = None,
    species: str = "dog",
    symptom_ids: Optional[set] = None,
) -> Dict[str, Any]:
    """
    Public API for symptom extraction.

    Args:
        text: User symptom description
        extractor: Optional pre-instantiated extractor
        species: Animal species
        symptom_ids: Valid symptom ID set

    Returns:
        Extraction result dict
    """
    if extractor is None:
        extractor = SymptomExtractor()

    if symptom_ids:
        extractor.set_valid_symptom_ids(symptom_ids)

    return extractor.extract(text, patient_species=species)
