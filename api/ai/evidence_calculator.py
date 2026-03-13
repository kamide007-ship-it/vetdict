"""Evidence-based confidence scoring for disease diagnosis.

Applies medical evidence levels to adjust disease confidence scores
based on scientific literature support and clinical evidence quality.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

# Import evidence data
try:
    from api.data.disease_evidence import EvidenceRetriever, DISEASE_EVIDENCE
except ImportError:
    logger.warning("Could not import disease evidence data")
    EvidenceRetriever = None
    DISEASE_EVIDENCE = {}


@dataclass
class EvidenceBreakdown:
    """Detailed breakdown of evidence-based confidence calculation."""

    disease_name: str
    raw_symptom_score: float  # Initial symptom match score (0-1)
    evidence_level: int  # 1-4 (1=strongest RCT/meta-analysis, 4=clinical)
    evidence_multiplier: float  # 1.40-1.50 (level 1), 1.20-1.35 (level 2), etc.
    weighted_evidence_component: float  # evidence_multiplier * 0.25
    demographic_adjustment: float  # Gender, age, severity adjustments (0-1.5+)
    weighted_demographic_component: float  # demographic_adjustment * 0.15
    final_confidence: float  # Final score (0-1.0)
    calculation_notes: str = ""

    def to_dict(self):
        return {
            "disease_name": self.disease_name,
            "raw_symptom_score": round(self.raw_symptom_score, 3),
            "evidence_level": self.evidence_level,
            "evidence_multiplier": round(self.evidence_multiplier, 3),
            "weighted_evidence_component": round(self.weighted_evidence_component, 3),
            "demographic_adjustment": round(self.demographic_adjustment, 3),
            "weighted_demographic_component": round(self.weighted_demographic_component, 3),
            "final_confidence": round(self.final_confidence, 3),
            "calculation_notes": self.calculation_notes,
        }


class EvidenceScorer:
    """Calculates confidence scores using evidence-based weighting."""

    # Weighting formula components:
    # final_confidence = (
    #     raw_symptom_score × 0.60 +
    #     evidence_multiplier × 0.25 +
    #     demographic_adjustment × 0.15
    # ) × normalization

    SYMPTOM_WEIGHT = 0.60  # 60% from symptom matching
    EVIDENCE_WEIGHT = 0.25  # 25% from medical evidence
    DEMOGRAPHIC_WEIGHT = 0.15  # 15% from patient demographics

    @classmethod
    def calculate_evidence_score(
        cls,
        disease_name: str,
        raw_symptom_score: float,
        demographic_adjustment: float = 1.0,
        use_evidence: bool = True,
    ) -> tuple[float, EvidenceBreakdown]:
        """
        Calculate final confidence score using evidence-based weighting.

        Args:
            disease_name: Name of disease being scored
            raw_symptom_score: Initial score from symptom matching (0-1.0)
            demographic_adjustment: Score adjustment from demographics (0-1.5+)
            use_evidence: Whether to apply evidence weighting (default True)

        Returns:
            Tuple of (final_confidence, EvidenceBreakdown)
        """
        # Clamp inputs to valid ranges
        raw_symptom_score = max(0.0, min(raw_symptom_score, 1.0))
        demographic_adjustment = max(0.0, demographic_adjustment)

        # Get evidence for disease
        evidence_level = 4  # Default to weakest (clinical level)
        evidence_multiplier = 1.0  # Default no boost

        if use_evidence and EvidenceRetriever:
            evidence = EvidenceRetriever.get_evidence(disease_name)
            if evidence:
                evidence_level = evidence.level
                evidence_multiplier = evidence.confidence_multiplier
            else:
                # Assign evidence_multiplier based on absence of formal evidence
                evidence_level = 4
                evidence_multiplier = 1.0

        # Calculate weighted components
        symptom_component = raw_symptom_score * cls.SYMPTOM_WEIGHT
        evidence_component = evidence_multiplier * cls.EVIDENCE_WEIGHT
        demographic_component = demographic_adjustment * cls.DEMOGRAPHIC_WEIGHT

        # Sum weighted components
        combined_score = symptom_component + evidence_component + demographic_component

        # Normalize to 0-1.0 range
        # Max possible is: 1.0*0.6 + 1.5*0.25 + 1.5*0.15 = 0.6 + 0.375 + 0.225 = 1.2
        # So we normalize by dividing by 1.2
        normalization_factor = 1.2
        final_confidence = combined_score / normalization_factor

        # Ensure final confidence is in valid range
        final_confidence = max(0.0, min(final_confidence, 1.0))

        # Build breakdown for transparency
        breakdown = EvidenceBreakdown(
            disease_name=disease_name,
            raw_symptom_score=raw_symptom_score,
            evidence_level=evidence_level,
            evidence_multiplier=evidence_multiplier,
            weighted_evidence_component=evidence_component,
            demographic_adjustment=demographic_adjustment,
            weighted_demographic_component=demographic_component,
            final_confidence=final_confidence,
            calculation_notes=cls._build_notes(
                evidence_level, evidence_multiplier, demographic_adjustment
            ),
        )

        return final_confidence, breakdown

    @staticmethod
    def _build_notes(
        evidence_level: int, evidence_multiplier: float, demographic_adjustment: float
    ) -> str:
        """Build human-readable notes about score calculation."""
        level_desc = {
            1: "RCT/Meta-analysis (strongest)",
            2: "Cohort study",
            3: "Case series",
            4: "Clinical observation (weakest)",
        }

        notes = f"Evidence Level {evidence_level}: {level_desc.get(evidence_level, 'Unknown')}. "

        if evidence_multiplier > 1.0:
            notes += f"Evidence multiplier: {evidence_multiplier:.2f}x (boosted). "
        else:
            notes += f"Evidence multiplier: {evidence_multiplier:.2f}x (no boost). "

        if demographic_adjustment < 1.0:
            notes += f"Demographic adjustment: {demographic_adjustment:.2f}x (reduced by demographics). "
        elif demographic_adjustment > 1.0:
            notes += f"Demographic adjustment: {demographic_adjustment:.2f}x (enhanced by demographics). "
        else:
            notes += "Demographic adjustment: neutral. "

        return notes.strip()

    @classmethod
    def score_multiple_diseases(
        cls,
        diseases_with_scores: List[Dict[str, Any]],
        demographic_adjustments: Optional[Dict[str, float]] = None,
        use_evidence: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Score multiple diseases with evidence weighting.

        Args:
            diseases_with_scores: List of dicts with 'name' and 'match_percent'
            demographic_adjustments: Optional dict mapping disease names to demographic adjustments
            use_evidence: Whether to apply evidence weighting

        Returns:
            List of scored diseases with confidence_breakdown
        """
        scored_diseases = []

        for disease in diseases_with_scores:
            disease_name = disease.get("name", "")
            raw_score = disease.get("match_percent", 0) / 100.0  # Convert from percentage to 0-1

            # Get demographic adjustment if provided
            demographic_adjustment = 1.0
            if demographic_adjustments and disease_name in demographic_adjustments:
                demographic_adjustment = demographic_adjustments[disease_name]

            # Calculate evidence-based score
            final_score, breakdown = cls.calculate_evidence_score(
                disease_name, raw_score, demographic_adjustment, use_evidence
            )

            # Create output dict
            scored = disease.copy()
            scored["match_percent"] = int(final_score * 100)  # Convert back to percentage
            scored["confidence_before_evidence"] = disease.get("match_percent", 0)
            scored["confidence_breakdown"] = breakdown.to_dict()

            scored_diseases.append(scored)

        # Re-sort by final match_percent (descending)
        scored_diseases.sort(key=lambda d: d.get("match_percent", 0), reverse=True)

        return scored_diseases

    @classmethod
    def apply_evidence_adjustment(
        cls,
        disease_dict: Dict[str, Any],
        demographic_adjustment: float = 1.0,
        use_evidence: bool = True,
    ) -> Dict[str, Any]:
        """
        Apply evidence adjustment to a single disease dict.

        Args:
            disease_dict: Dict with 'name' and 'match_percent' keys
            demographic_adjustment: Optional demographic adjustment factor
            use_evidence: Whether to apply evidence weighting

        Returns:
            Updated disease dict with evidence information
        """
        disease_name = disease_dict.get("name", "")
        raw_score = disease_dict.get("match_percent", 0) / 100.0

        final_score, breakdown = cls.calculate_evidence_score(
            disease_name, raw_score, demographic_adjustment, use_evidence
        )

        result = disease_dict.copy()
        result["match_percent"] = int(final_score * 100)
        result["confidence_before_evidence"] = disease_dict.get("match_percent", 0)
        result["confidence_breakdown"] = breakdown.to_dict()

        return result


def build_confidence_breakdown_response(
    disease_name: str,
    raw_symptom_score: float,
    demographic_adjustment: float = 1.0,
) -> Dict[str, Any]:
    """
    Build a response showing confidence calculation breakdown.

    Returns API response object with detailed calculation steps.
    """
    final_score, breakdown = EvidenceScorer.calculate_evidence_score(
        disease_name, raw_symptom_score, demographic_adjustment
    )

    return {
        "disease": disease_name,
        "final_confidence": final_score,
        "final_confidence_percent": int(final_score * 100),
        "breakdown": breakdown.to_dict(),
        "formula_explanation": (
            "final_confidence = "
            "(raw_symptom_score × 0.60 + evidence_multiplier × 0.25 + "
            "demographic_adjustment × 0.15) / 1.2"
        ),
    }
