"""confidence_adapter.py – AI confidence integration with RECO2

Merges AI symptom extraction confidence and patient personalization data
into the RECO2 integrity calculation (ψ/psi) for enhanced verdict accuracy.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


@dataclass
class AIConfidenceContext:
    """Wrapped AI confidence scores from Phase 2b."""

    symptom_extraction_confidence: float = 0.5  # Base Claude extraction confidence (0.0-1.0)
    interaction_boost: float = 0.0  # Boost from symptom interactions (0.0-0.15)
    personalization_factor: float = 0.0  # Age/severity adjustment factor (-0.3 to +0.3)
    combined_confidence: float = 0.5  # Final merged confidence (0.0-1.0)
    age_stage: Optional[str] = None  # "puppy", "young", "adult", "senior", or None
    severity: str = "moderate"  # "mild", "moderate", "severe"
    confidence_source: str = "ai"  # "ai" or "manual"
    metadata: Dict[str, Any] = None  # Additional context (extraction_method, etc.)

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


def adjust_context_from_ai(
    context: Dict[str, Any], ai_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge AI extraction result into RECO2 context.

    Args:
        context: Original RECO2 context dict
        ai_result: Phase 2b extraction result with personalization data

    Returns:
        Updated context dict with AI confidence integrated
    """
    updated_context = context.copy()

    if not ai_result or not isinstance(ai_result, dict):
        logger.debug("No AI result provided, returning original context")
        return updated_context

    # Extract AI confidence components
    base_conf = float(ai_result.get("confidence", 0.5))
    interactions = ai_result.get("interactions", [])
    personalization = ai_result.get("personalization", {})

    # Calculate interaction boost (max 0.15 from strongest pair)
    interaction_boost = 0.0
    if interactions and len(interactions) > 0:
        strongest = interactions[0]
        interaction_boost = float(strongest.get("boost_factor", 0.0))

    # Calculate personalization factor from age/severity adjustments
    # This is estimated from the fact that personalization can adjust by ±30%
    personalization_factor = 0.0
    if personalization:
        age_stage = personalization.get("age_stage")
        severity = personalization.get("severity", "moderate")

        # Age-based factor (-0.15 to +0.15 range)
        age_factor = 0.0
        if age_stage == "puppy":
            age_factor = 0.12  # Puppies benefit from boost for certain conditions
        elif age_stage == "senior":
            age_factor = 0.15  # Seniors benefit from boost for age-related conditions
        elif age_stage == "young":
            age_factor = 0.08

        # Severity-based factor (-0.15 to +0.15 range)
        severity_factor = 0.0
        if severity == "severe":
            severity_factor = 0.15
        elif severity == "mild":
            severity_factor = -0.15
        # moderate stays at 0.0

        personalization_factor = age_factor + (severity_factor * 0.5)

    # Calculate combined confidence
    combined_conf = calculate_combined_confidence(
        base_conf, interaction_boost, personalization_factor
    )

    # Update context with AI-enhanced confidence
    updated_context["confidence"] = combined_conf
    updated_context["ai_confidence"] = {
        "symptom_extraction": base_conf,
        "interaction_boost": round(interaction_boost, 3),
        "personalization_factor": round(personalization_factor, 3),
        "combined": combined_conf,
        "age_stage": personalization.get("age_stage"),
        "severity": personalization.get("severity", "moderate"),
        "source": "ai",
    }

    # Mark that domain knowledge is now enhanced with AI
    if "domain_known" not in updated_context:
        updated_context["domain_known"] = False
    # If we have high AI confidence, boost the domain_known flag slightly
    if combined_conf > 0.8:
        updated_context["ai_enhanced"] = True

    logger.debug(
        f"Adjusted context from AI: base={base_conf:.3f}, "
        f"boost={interaction_boost:.3f}, personalization={personalization_factor:.3f}, "
        f"combined={combined_conf:.3f}"
    )

    return updated_context


def calculate_combined_confidence(
    base_confidence: float,
    interaction_boost: float = 0.0,
    personalization_factor: float = 0.0,
) -> float:
    """
    Calculate combined confidence from AI components.

    Formula: base_conf + (personalization_factor * 0.5) + interaction_boost

    Args:
        base_confidence: Symptom extraction confidence (0.0-1.0)
        interaction_boost: Confidence boost from interactions (0.0-0.15)
        personalization_factor: Age/severity adjustment (-0.3 to +0.3)

    Returns:
        Combined confidence score (0.0-1.0)
    """
    base_confidence = max(0.0, min(1.0, float(base_confidence)))
    interaction_boost = max(0.0, min(0.15, float(interaction_boost)))
    personalization_factor = max(-0.3, min(0.3, float(personalization_factor)))

    # Combine all components additively
    # Base confidence is primary (0.0-1.0)
    # Personalization factor scales up to ±0.15 effective boost
    # Interaction boost adds up to 0.15
    combined = base_confidence + (personalization_factor * 0.5) + interaction_boost
    combined = max(0.0, min(1.0, combined))

    return round(combined, 3)


def scale_confidence_to_psi_multiplier(
    combined_confidence: float, min_multiplier: float = 0.6, max_multiplier: float = 1.2
) -> float:
    """
    Convert AI confidence score to RECO2 psi multiplier.

    Linear scaling:
    - Confidence 0.0 → multiplier 0.6x (suspect, dampens psi)
    - Confidence 0.5 → multiplier 0.9x (baseline)
    - Confidence 1.0 → multiplier 1.2x (reliable, enhances psi)

    Args:
        combined_confidence: Combined confidence (0.0-1.0)
        min_multiplier: Multiplier at confidence 0.0 (default 0.6)
        max_multiplier: Multiplier at confidence 1.0 (default 1.2)

    Returns:
        Psi multiplier (0.6-1.2)
    """
    combined_confidence = max(0.0, min(1.0, float(combined_confidence)))

    # Linear interpolation from min to max multiplier
    multiplier = min_multiplier + (combined_confidence * (max_multiplier - min_multiplier))
    return round(multiplier, 3)


def create_ai_confidence_context(ai_result: Dict[str, Any]) -> AIConfidenceContext:
    """
    Create AIConfidenceContext from Phase 2b extraction result.

    Args:
        ai_result: Extraction result with personalization metadata

    Returns:
        AIConfidenceContext instance
    """
    if not ai_result or not isinstance(ai_result, dict):
        return AIConfidenceContext()

    base_conf = float(ai_result.get("confidence", 0.5))
    interactions = ai_result.get("interactions", [])
    personalization = ai_result.get("personalization", {})

    # Calculate components
    interaction_boost = 0.0
    if interactions and len(interactions) > 0:
        interaction_boost = float(interactions[0].get("boost_factor", 0.0))

    personalization_factor = 0.0
    age_stage = None
    severity = "moderate"

    if personalization:
        age_stage = personalization.get("age_stage")
        severity = personalization.get("severity", "moderate")

        # Estimate personalization factor from clinical adjustments
        age_factor = 0.0
        if age_stage == "puppy":
            age_factor = 0.12
        elif age_stage == "senior":
            age_factor = 0.15
        elif age_stage == "young":
            age_factor = 0.08

        severity_factor = 0.0
        if severity == "severe":
            severity_factor = 0.15
        elif severity == "mild":
            severity_factor = -0.15

        personalization_factor = age_factor + (severity_factor * 0.5)

    combined = calculate_combined_confidence(
        base_conf, interaction_boost, personalization_factor
    )

    return AIConfidenceContext(
        symptom_extraction_confidence=base_conf,
        interaction_boost=round(interaction_boost, 3),
        personalization_factor=round(personalization_factor, 3),
        combined_confidence=combined,
        age_stage=age_stage,
        severity=severity,
        confidence_source="ai",
        metadata={
            "extraction_method": personalization.get("extraction_method", "unknown"),
            "confidence_in_extraction": personalization.get("confidence", 0.5),
            "num_interactions": len(interactions) if interactions else 0,
        },
    )
