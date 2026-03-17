"""Comorbidity scoring engine for disease interaction quantification.

Calculates how likely two diseases coexist given patient context and
applies interaction effects to confidence scores.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

from api.ai.disease_interactions import DiseaseInteractionMatrix


@dataclass
class InteractionEffect:
    """Quantifies how two diseases interact."""

    disease_a: str
    disease_b: str
    base_interaction_score: float  # -1.0 (competitive) to 1.0 (synergistic)
    symptom_overlap_ratio: float  # 0-1: how much do symptoms overlap?
    confidence_amplification: float  # Multiplier effect on combined confidence
    explanation: str


class ComorbidityScorer:
    """Scores and models disease interactions."""

    @staticmethod
    def calculate_interaction_effect(
        disease_a: str,
        disease_b: str,
        disease_a_symptoms: List[str],
        disease_b_symptoms: List[str],
        detected_symptoms: List[str],
    ) -> InteractionEffect:
        """
        Calculate interaction effect between two diseases.

        Args:
            disease_a: First disease name
            disease_b: Second disease name
            disease_a_symptoms: Symptoms characteristic of disease_a
            disease_b_symptoms: Symptoms characteristic of disease_b
            detected_symptoms: Symptoms actually detected in patient

        Returns:
            InteractionEffect quantifying the interaction
        """
        # Calculate symptom overlap
        set_a = set(disease_a_symptoms)
        set_b = set(disease_b_symptoms)
        detected_set = set(detected_symptoms)

        union_size = len(set_a | set_b)
        overlap_size = len(set_a & set_b)

        symptom_overlap_ratio = overlap_size / union_size if union_size > 0 else 0.0

        # Determine interaction type
        len(set_a - set_b)
        len(set_b - set_a)
        both_in_detected = len((set_a & set_b) & detected_set)

        # Scoring logic
        if overlap_size == 0:
            # No overlap: diseases likely independent or synergistic
            base_interaction_score = 0.3  # Slightly positive (different systems)
            confidence_amplification = 1.15  # Both diseases explain different symptoms
        elif symptom_overlap_ratio > 0.7:
            # High overlap: likely only one disease (competitive)
            base_interaction_score = -0.6  # Strongly negative
            confidence_amplification = 0.75  # Reduce combined confidence
        else:
            # Moderate overlap: possible comorbidity with some competition
            base_interaction_score = 0.0  # Neutral
            confidence_amplification = 1.0

        # Adjust if both overlap symptoms are detected (suggests genuine comorbidity)
        if both_in_detected > 0:
            base_interaction_score += 0.2
            confidence_amplification += 0.05

        # Generate explanation
        explanation = ComorbidityScorer._generate_interaction_explanation(
            disease_a, disease_b, symptom_overlap_ratio, base_interaction_score
        )

        return InteractionEffect(
            disease_a=disease_a,
            disease_b=disease_b,
            base_interaction_score=base_interaction_score,
            symptom_overlap_ratio=symptom_overlap_ratio,
            confidence_amplification=confidence_amplification,
            explanation=explanation,
        )

    @staticmethod
    def _generate_interaction_explanation(
        disease_a: str,
        disease_b: str,
        overlap_ratio: float,
        interaction_score: float,
    ) -> str:
        """Generate plain-text explanation of disease interaction."""
        if interaction_score > 0.2:
            if overlap_ratio < 0.3:
                return f"{disease_a}と{disease_b}は異なる器官系に影響し、共存の可能性があります。"
            else:
                return f"{disease_a}と{disease_b}は関連のある症状を示す可能性があります。"
        elif interaction_score < -0.2:
            return f"{disease_a}と{disease_b}は症状が類似しており、どちらか一方の可能性が高い場合があります。"
        else:
            return f"{disease_a}と{disease_b}は独立して発生する可能性があります。"

    @classmethod
    def score_disease_combination(
        cls,
        disease_a: str,
        disease_b: str,
        confidence_a: float,
        confidence_b: float,
        age_years: Optional[float] = None,
        severity: str = "moderate",
        breed: Optional[str] = None,
        symptom_overlap_ratio: float = 0.5,
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate combined confidence score for two coexisting diseases.

        Args:
            disease_a: First disease name
            disease_b: Second disease name
            confidence_a: Individual confidence for disease_a (0-1)
            confidence_b: Individual confidence for disease_b (0-1)
            age_years: Patient age
            severity: Symptom severity ("mild", "moderate", "severe")
            breed: Patient breed
            symptom_overlap_ratio: How much do symptoms overlap? (0-1)

        Returns:
            (combined_confidence, breakdown) tuple
        """
        # Get base comorbidity probability
        comorbidity_prob = DiseaseInteractionMatrix.get_comorbidity_probability(
            disease_a, disease_b, age_years, severity, breed
        )

        # Calculate Bayesian combined probability
        # P(A and B | symptoms) = P(A|S) * P(B|S) * coexistence_prob * (1 - symptom_penalty)
        symptom_penalty = symptom_overlap_ratio * 0.3  # Up to 30% penalty for overlap

        combined_confidence = (
            confidence_a * confidence_b * comorbidity_prob * (1.0 - symptom_penalty)
        )

        # Ensure result is in valid range
        combined_confidence = max(0.0, min(combined_confidence, 1.0))

        # Build breakdown for transparency
        breakdown = {
            "confidence_a": round(confidence_a, 3),
            "confidence_b": round(confidence_b, 3),
            "comorbidity_probability": round(comorbidity_prob, 3),
            "symptom_overlap_penalty": round(symptom_penalty, 3),
            "combined_confidence": round(combined_confidence, 3),
            "formula_explanation": (
                "combined = P(A|S) × P(B|S) × coexistence_prob × (1 - overlap_penalty)"
            ),
        }

        return combined_confidence, breakdown

    @classmethod
    def adjust_individual_confidences_for_combination(
        cls,
        confidence_a: float,
        confidence_b: float,
        symptom_overlap_ratio: float,
        comorbidity_known: bool = True,
    ) -> Tuple[float, float]:
        """
        Adjust individual disease confidences when both are considered together.

        Args:
            confidence_a: Original confidence for disease A
            confidence_b: Original confidence for disease B
            symptom_overlap_ratio: Symptom overlap (0-1)
            comorbidity_known: Whether this is a known comorbidity

        Returns:
            (adjusted_confidence_a, adjusted_confidence_b) tuple
        """
        if symptom_overlap_ratio > 0.7:
            # High overlap: reduce both confidences
            # Overlapping symptoms are now "split" between two diseases
            adjustment_factor = 0.85
        elif symptom_overlap_ratio > 0.4:
            # Moderate overlap: small reduction
            adjustment_factor = 0.95
        else:
            # Low overlap: no reduction or slight boost
            adjustment_factor = 1.0 if not comorbidity_known else 1.05

        adjusted_a = confidence_a * adjustment_factor
        adjusted_b = confidence_b * adjustment_factor

        # Clamp to valid range
        adjusted_a = max(0.0, min(adjusted_a, 1.0))
        adjusted_b = max(0.0, min(adjusted_b, 1.0))

        return adjusted_a, adjusted_b

    @staticmethod
    def estimate_symptom_overlap(
        disease_a_symptoms: List[str],
        disease_b_symptoms: List[str],
    ) -> float:
        """
        Estimate overlap between symptom sets of two diseases.

        Args:
            disease_a_symptoms: Symptoms of disease A
            disease_b_symptoms: Symptoms of disease B

        Returns:
            Overlap ratio (0-1)
        """
        if not disease_a_symptoms or not disease_b_symptoms:
            return 0.0

        set_a = set(disease_a_symptoms)
        set_b = set(disease_b_symptoms)

        intersection = len(set_a & set_b)
        union = len(set_a | set_b)

        return intersection / union if union > 0 else 0.0

    @staticmethod
    def calculate_comorbidity_severity_adjustment(
        combined_confidence: float,
        symptom_severity: str,
    ) -> float:
        """
        Adjust combined confidence based on overall symptom severity.

        Args:
            combined_confidence: Base combined confidence score
            symptom_severity: "mild", "moderate", or "severe"

        Returns:
            Adjusted confidence
        """
        if symptom_severity == "severe":
            # Severe presentation more likely to have multiple conditions
            return combined_confidence * 1.15
        elif symptom_severity == "mild":
            # Mild presentation: less likely to have multiple conditions
            return combined_confidence * 0.8
        else:  # moderate
            return combined_confidence

    @classmethod
    def rank_disease_combinations(
        cls,
        potential_combinations: List[Tuple[str, str, float, float]],
        age_years: Optional[float] = None,
        severity: str = "moderate",
        breed: Optional[str] = None,
    ) -> List[Tuple[str, str, float]]:
        """
        Rank disease combinations by combined confidence.

        Args:
            potential_combinations: List of (disease_a, disease_b, conf_a, conf_b)
            age_years: Patient age
            severity: Symptom severity
            breed: Patient breed

        Returns:
            List of (disease_a, disease_b, combined_confidence) sorted descending
        """
        ranked = []

        for disease_a, disease_b, conf_a, conf_b in potential_combinations:
            combined_conf, _ = cls.score_disease_combination(
                disease_a,
                disease_b,
                conf_a,
                conf_b,
                age_years,
                severity,
                breed,
            )

            if combined_conf > 0.0:  # Only include positive scores
                ranked.append((disease_a, disease_b, combined_conf))

        # Sort by combined confidence (descending)
        ranked.sort(key=lambda x: x[2], reverse=True)

        return ranked
