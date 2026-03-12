"""patient_personalization.py – Patient demographics extraction and confidence adjustment

Extracts age/severity from symptom text and adjusts disease confidence scores
based on patient characteristics (age, symptom severity).
"""

import logging
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


@dataclass
class PatientContext:
    """Extracted patient demographic information."""

    age_stage: Optional[str] = None  # "puppy" | "young" | "adult" | "senior" | None
    extracted_age_years: Optional[float] = None  # Numeric age if extracted
    severity: str = "moderate"  # "mild" | "moderate" | "severe"
    extraction_method: str = "unknown"  # "text_extraction" | "user_input" | "inference"
    confidence: float = 0.5  # How confident we are in extracted values


class AgeExtractor:
    """Extracts patient age from natural language text."""

    # Age keywords and their corresponding stage + confidence
    KEYWORDS_EN = {
        "puppy": ("puppy", 0.8),
        "puppies": ("puppy", 0.8),
        "kitten": ("puppy", 0.8),
        "baby": ("puppy", 0.6),
        "juvenile": ("young", 0.7),
        "young": ("young", 0.6),
        "adult": ("adult", 0.6),
        "middle-aged": ("adult", 0.7),
        "senior": ("senior", 0.8),
        "elderly": ("senior", 0.85),
        "old": ("senior", 0.6),
    }

    KEYWORDS_JA = {
        "子犬": ("puppy", 0.8),
        "子猫": ("puppy", 0.8),
        "幼犬": ("puppy", 0.75),
        "仔犬": ("puppy", 0.75),
        "若い": ("young", 0.6),
        "成犬": ("adult", 0.7),
        "成猫": ("adult", 0.7),
        "シニア": ("senior", 0.8),
        "老犬": ("senior", 0.8),
        "老猫": ("senior", 0.8),
        "高齢": ("senior", 0.75),
    }

    # Regex patterns for numeric age extraction
    REGEX_PATTERNS = [
        (r"(\d+)\s*(?:years?|yo|year\s+old|y\.o\.|yrs?)", 1.0),  # "3 years", "3yo", "3 year old"
        (r"(\d+)\s*(?:months?|mo)", 1 / 12),  # Convert months to years
        (r"(\d+)\s*(?:週|weeks?|wks?)", 1 / 52),  # Convert weeks to years
        (r"(\d+)\s*(?:才|歳)", 1.0),  # Japanese age
    ]

    @classmethod
    def extract(cls, text: str) -> PatientContext:
        """
        Extract age from natural language text.

        Args:
            text: User input describing patient

        Returns:
            PatientContext with extracted age information
        """
        if not text or not isinstance(text, str):
            return PatientContext()

        text_lower = text.lower()

        # Try regex patterns for numeric age FIRST (most precise)
        for pattern, multiplier in cls.REGEX_PATTERNS:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    age_value = float(match.group(1)) * multiplier
                    stage = cls._stage_from_age(age_value)
                    return PatientContext(
                        age_stage=stage,
                        extracted_age_years=round(age_value, 1),
                        confidence=0.95,
                        extraction_method="text_extraction",
                    )
                except (ValueError, IndexError):
                    pass

        # Try keyword matching (English) second
        for keyword, (stage, confidence) in cls.KEYWORDS_EN.items():
            if keyword in text_lower:
                return PatientContext(
                    age_stage=stage,
                    extracted_age_years=None,
                    confidence=confidence,
                    extraction_method="text_extraction",
                )

        # Try Japanese keywords last
        for keyword, (stage, confidence) in cls.KEYWORDS_JA.items():
            if keyword in text:
                return PatientContext(
                    age_stage=stage,
                    extracted_age_years=None,
                    confidence=confidence,
                    extraction_method="text_extraction",
                )

        # No age found
        return PatientContext()

    @classmethod
    def _stage_from_age(cls, age_years: float) -> str:
        """Map numeric age to age stage."""
        if age_years < 1:
            return "puppy"
        elif age_years < 3:
            return "young"
        elif age_years < 7:
            return "adult"
        else:
            return "senior"


class SeverityInference:
    """Infers disease severity from symptom count and types."""

    # High-urgency symptoms that indicate severity
    URGENT_SYMPTOMS = {
        "bleeding",
        "seizure",
        "unconscious",
        "difficulty_breathing",
        "severe_pain",
        "severe_vomiting",
        "dehydration",
        "trauma",
        "collapse",
        "extreme_lethargy",
    }

    @staticmethod
    def assess(symptom_count: int, symptom_ids: List[str]) -> str:
        """
        Assess severity from symptom count and types.

        Args:
            symptom_count: Number of symptoms detected
            symptom_ids: List of symptom IDs

        Returns:
            "mild" | "moderate" | "severe"
        """
        # Check for urgent symptoms (override other factors)
        urgent_count = sum(
            1 for sid in symptom_ids if any(u in sid for u in SeverityInference.URGENT_SYMPTOMS)
        )

        if urgent_count > 0:
            return "severe"

        # Assess by symptom count
        if symptom_count <= 1:
            return "mild"
        elif symptom_count <= 4:
            return "moderate"
        else:
            return "severe"


class PersonalizationEngine:
    """Applies patient personalization to confidence scores."""

    # Age-based prevalence multipliers for common diseases
    # Format: {disease_name: {age_stage: multiplier}}
    AGE_PREVALENCE_MULTIPLIERS = {
        "hip_dysplasia": {"senior": 1.4, "adult": 1.2},
        "arthritis": {"senior": 1.5, "adult": 1.1},
        "hypoglycemia": {"puppy": 1.3, "young": 1.2},
        "parvovirus": {"puppy": 1.4},
        "heartworm": {"adult": 1.2, "senior": 1.3},
        "dental_disease": {"senior": 1.5, "adult": 1.1},
        "cognitive_dysfunction": {"senior": 1.6},
        "obesity": {"senior": 1.2, "adult": 1.1},
    }

    # Severity-based confidence multipliers
    SEVERITY_MULTIPLIERS = {
        "mild": 0.85,
        "moderate": 1.0,
        "severe": 1.15,
    }

    @classmethod
    def personalize_disease_confidence(
        cls,
        disease_name: str,
        base_confidence: float,
        patient_context: PatientContext,
    ) -> float:
        """
        Adjust disease confidence based on patient context.

        Args:
            disease_name: Name of the disease
            base_confidence: Base confidence score (0.0-1.0)
            patient_context: PatientContext with extracted demographics

        Returns:
            Adjusted confidence score (0.0-1.0)
        """
        adjusted = base_confidence

        # Apply age-based multiplier
        if patient_context.age_stage:
            multipliers = cls.AGE_PREVALENCE_MULTIPLIERS.get(disease_name.lower(), {})
            if patient_context.age_stage in multipliers:
                mult = multipliers[patient_context.age_stage]
                adjusted *= mult
                logger.debug(
                    f"Age adjustment for {disease_name}: "
                    f"{base_confidence} * {mult} = {adjusted}"
                )

        # Apply severity multiplier
        severity_mult = cls.SEVERITY_MULTIPLIERS.get(patient_context.severity, 1.0)
        adjusted *= severity_mult

        # Cap at 0.0-1.0
        adjusted = max(0.0, min(adjusted, 1.0))

        return round(adjusted, 3)

    @classmethod
    def personalize_all_diseases(
        cls,
        diseases_with_confidence: List[Dict[str, Any]],
        patient_context: PatientContext,
    ) -> List[Dict[str, Any]]:
        """
        Apply personalization to multiple diseases.

        Args:
            diseases_with_confidence: List of dicts with 'name' and 'confidence'
            patient_context: PatientContext for personalization

        Returns:
            List with updated confidence scores
        """
        personalized = []
        for disease in diseases_with_confidence:
            updated = disease.copy()
            original_confidence = disease.get("confidence", 0.5)
            updated["confidence"] = cls.personalize_disease_confidence(
                disease.get("name", ""),
                original_confidence,
                patient_context,
            )
            updated["confidence_adjustment"] = updated["confidence"] - original_confidence
            personalized.append(updated)

        return personalized

    @classmethod
    def build_context_from_text(
        cls, text: str, symptoms: List[str]
    ) -> PatientContext:
        """
        Build complete patient context from text and symptoms.

        Args:
            text: User symptom description
            symptoms: Extracted symptom IDs

        Returns:
            Complete PatientContext
        """
        # Extract age
        context = AgeExtractor.extract(text)

        # Infer severity
        severity = SeverityInference.assess(len(symptoms), symptoms)
        context.severity = severity

        # Set extraction method
        if context.extraction_method == "unknown":
            context.extraction_method = "inference"
            context.confidence = 0.5

        return context


def personalize_extraction_result(
    extraction_result: Dict[str, Any], text: str
) -> Dict[str, Any]:
    """
    Enhance extraction result with personalization data.

    Args:
        extraction_result: Result from SymptomExtractor.extract()
        text: Original user input

    Returns:
        Enhanced result with personalization metadata
    """
    symptoms = extraction_result.get("symptoms", [])

    # Build patient context
    context = PersonalizationEngine.build_context_from_text(text, symptoms)

    # Add to result
    result = extraction_result.copy()
    result["personalization"] = {
        "age_stage": context.age_stage,
        "extracted_age_years": context.extracted_age_years,
        "severity": context.severity,
        "extraction_method": context.extraction_method,
        "confidence": context.confidence,
    }

    return result
