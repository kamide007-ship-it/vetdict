"""Multi-disease detection engine for simultaneous diagnosis scenarios.

Identifies when multiple diseases likely coexist and generates disease
combination hypotheses for further investigation.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
import logging
import math

logger = logging.getLogger(__name__)

from api.ai.disease_interactions import DiseaseInteractionMatrix
from api.ai.comorbidity_scorer import ComorbidityScorer


@dataclass
class DiseaseCombination:
    """Represents a pair or triple of coexisting diseases."""

    diseases: List[str]  # e.g., ["Hip Dysplasia", "Osteoarthritis"]
    combined_confidence: float  # 0-1, overall score
    component_confidences: Dict[str, float]  # Individual disease scores
    interaction_effect: float  # -1.0 (competitive) to 1.0 (synergistic)
    shared_symptom_count: int  # Symptoms explained by multiple diseases
    unique_symptoms_per_disease: Dict[str, List[str]] = field(
        default_factory=dict
    )  # Each disease's specific symptoms
    explanation_ja: str = ""  # Plain-text explanation in Japanese
    explanation_en: str = ""  # Plain-text explanation in English
    mechanism: str = ""  # Medical mechanism
    confidence_sources: List[str] = field(
        default_factory=list
    )  # ["symptom_overlap", "comorbidity_db", "age_factor"]

    def to_dict(self):
        return {
            "diseases": self.diseases,
            "combined_confidence": round(self.combined_confidence, 3),
            "component_confidences": {
                k: round(v, 3) for k, v in self.component_confidences.items()
            },
            "interaction_effect": round(self.interaction_effect, 3),
            "shared_symptom_count": self.shared_symptom_count,
            "unique_symptoms_per_disease": self.unique_symptoms_per_disease,
            "explanation_ja": self.explanation_ja,
            "explanation_en": self.explanation_en,
            "mechanism": self.mechanism,
            "confidence_sources": self.confidence_sources,
        }


class MultiDiseaseDetector:
    """Detects and scores multi-disease diagnostic hypotheses."""

    # Heuristic thresholds
    MIN_SYMPTOM_DIVERSITY = 5  # Minimum symptom categories for multi-disease
    MIN_CONFIDENCE_THRESHOLD = 0.25  # Minimum individual disease confidence
    MIN_COMBINATION_CONFIDENCE = 0.30  # Minimum combined score

    @classmethod
    def should_explore_multidisease(
        cls,
        detected_symptoms: List[str],
        suspected_diseases: List[Dict[str, Any]],
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Determine if multi-disease exploration should be activated.

        Args:
            detected_symptoms: List of detected symptom IDs
            suspected_diseases: Current disease candidates with confidences
            patient_context: Optional context (age, severity, breed, etc.)

        Returns:
            True if multi-disease mode should be enabled
        """
        # Heuristic 1: Symptom diversity check
        if len(detected_symptoms) < cls.MIN_SYMPTOM_DIVERSITY:
            return False

        # Heuristic 2: Disease match pattern
        if len(suspected_diseases) < 2:
            return False

        # Get top confidences
        confidences = [d.get("match_percent", 0) / 100.0 for d in suspected_diseases[:3]]
        if not confidences:
            return False

        # Check if top diseases have similar confidence (within 15%)
        if len(confidences) >= 2:
            confidence_spread = confidences[0] - confidences[1]
            if confidence_spread < 0.15:
                # Similar confidence: ambiguous diagnosis, might be multiple
                return True

        # Heuristic 3: Age factor
        if patient_context:
            age_years = patient_context.get("age_years")
            if age_years and age_years > 10:
                # Seniors more likely to have multiple conditions
                return True

        # Heuristic 4: Symptom divergence check
        # TODO: Implement clustering to detect symptom groups
        # For now, use simple heuristic: 7+ symptoms suggests multiple systems
        if len(detected_symptoms) >= 7:
            return True

        return False

    @classmethod
    def generate_multidisease_candidates(
        cls,
        suspected_diseases: List[Dict[str, Any]],
        detected_symptoms: List[str],
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> List[DiseaseCombination]:
        """
        Generate disease combination hypotheses.

        Args:
            suspected_diseases: Initial single-disease candidates
            detected_symptoms: Detected symptom IDs
            patient_context: Patient context (age, breed, severity, etc.)

        Returns:
            List of DiseaseCombination sorted by confidence (descending)
        """
        combinations = []

        # Get top candidates
        top_candidates = suspected_diseases[:5]
        if len(top_candidates) < 2:
            return combinations

        # Extract context
        age_years = patient_context.get("age_years") if patient_context else None
        severity = patient_context.get("severity", "moderate") if patient_context else "moderate"
        breed = patient_context.get("breed") if patient_context else None

        # Generate pairwise combinations
        for i, disease_a in enumerate(top_candidates):
            for disease_b in top_candidates[i + 1 :]:
                name_a = disease_a.get("name", "")
                name_b = disease_b.get("name", "")
                conf_a = disease_a.get("match_percent", 0) / 100.0
                conf_b = disease_b.get("match_percent", 0) / 100.0

                if conf_a < cls.MIN_CONFIDENCE_THRESHOLD or conf_b < cls.MIN_CONFIDENCE_THRESHOLD:
                    continue

                # Score this combination
                combination = cls._score_combination(
                    name_a,
                    name_b,
                    conf_a,
                    conf_b,
                    detected_symptoms,
                    age_years,
                    severity,
                    breed,
                )

                if combination.combined_confidence >= cls.MIN_COMBINATION_CONFIDENCE:
                    combinations.append(combination)

        # Sort by combined confidence
        combinations.sort(key=lambda x: x.combined_confidence, reverse=True)

        return combinations

    @classmethod
    def _score_combination(
        cls,
        disease_a: str,
        disease_b: str,
        confidence_a: float,
        confidence_b: float,
        detected_symptoms: List[str],
        age_years: Optional[float],
        severity: str,
        breed: Optional[str],
    ) -> DiseaseCombination:
        """
        Score a specific disease combination.

        Args:
            disease_a: First disease name
            disease_b: Second disease name
            confidence_a: Individual confidence for A
            confidence_b: Individual confidence for B
            detected_symptoms: Detected symptom IDs
            age_years: Patient age
            severity: Symptom severity
            breed: Patient breed

        Returns:
            DiseaseCombination with calculated scores
        """
        # TODO: Get actual symptom lists from disease database
        # For now, use empty lists
        symptoms_a = []
        symptoms_b = []

        # Analyze shared symptoms
        shared_set = set(symptoms_a) & set(symptoms_b)
        shared_count = len(shared_set)
        unique_a = list(set(symptoms_a) - shared_set)
        unique_b = list(set(symptoms_b) - shared_set)

        # Calculate comorbidity score
        combined_conf, breakdown = ComorbidityScorer.score_disease_combination(
            disease_a,
            disease_b,
            confidence_a,
            confidence_b,
            age_years,
            severity,
            breed,
            symptom_overlap_ratio=len(shared_set) / (len(symptoms_a | symptoms_b) + 1),
        )

        # Get interaction effect
        interaction_effect = cls._calculate_interaction_effect(
            disease_a, disease_b, len(shared_set), len(symptoms_a) + len(symptoms_b)
        )

        # Get mechanism and explanation
        mechanism = DiseaseInteractionMatrix.COMORBIDITY_DATABASE.get(
            (disease_a, disease_b)
        )
        mechanism_name = mechanism.mechanism if mechanism else "unknown"

        explanation_ja = cls._generate_explanation_ja(disease_a, disease_b, mechanism)
        explanation_en = cls._generate_explanation_en(disease_a, disease_b, mechanism)

        # Determine confidence sources
        confidence_sources = []
        if mechanism:
            confidence_sources.append("comorbidity_database")
        if age_years and age_years > 7:
            confidence_sources.append("age_factor")
        if severity == "severe":
            confidence_sources.append("severity_factor")

        return DiseaseCombination(
            diseases=[disease_a, disease_b],
            combined_confidence=combined_conf,
            component_confidences={disease_a: confidence_a, disease_b: confidence_b},
            interaction_effect=interaction_effect,
            shared_symptom_count=shared_count,
            unique_symptoms_per_disease={disease_a: unique_a, disease_b: unique_b},
            explanation_ja=explanation_ja,
            explanation_en=explanation_en,
            mechanism=mechanism_name,
            confidence_sources=confidence_sources,
        )

    @staticmethod
    def _calculate_interaction_effect(
        disease_a: str,
        disease_b: str,
        shared_symptom_count: int,
        total_symptoms: int,
    ) -> float:
        """
        Calculate interaction effect between two diseases.

        Returns: -1.0 (competitive) to 1.0 (synergistic)
        """
        if total_symptoms == 0:
            return 0.0

        overlap_ratio = shared_symptom_count / total_symptoms

        # High overlap → competitive (likely only one is true)
        if overlap_ratio > 0.6:
            return -0.5

        # Low overlap → synergistic (complement each other)
        if overlap_ratio < 0.3:
            return 0.3

        # Moderate overlap → neutral
        return 0.0

    @staticmethod
    def _generate_explanation_ja(
        disease_a: str,
        disease_b: str,
        mechanism: Optional[Any] = None,
    ) -> str:
        """Generate Japanese explanation for disease combination."""
        if mechanism:
            return f"{disease_a}と{disease_b}は共存する可能性があります（{mechanism.mechanism}）。"
        return f"{disease_a}と{disease_b}の組み合わせの可能性があります。"

    @staticmethod
    def _generate_explanation_en(
        disease_a: str,
        disease_b: str,
        mechanism: Optional[Any] = None,
    ) -> str:
        """Generate English explanation for disease combination."""
        if mechanism:
            return f"{disease_a} and {disease_b} may coexist ({mechanism.mechanism})."
        return f"Both {disease_a} and {disease_b} are possible."

    @classmethod
    def validate_combination(
        cls,
        combination: DiseaseCombination,
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[bool, str]:
        """
        Validate if a disease combination makes clinical sense.

        Args:
            combination: DiseaseCombination to validate
            patient_context: Patient context for validation

        Returns:
            (is_valid, reason) tuple
        """
        # Check comorbidity database
        disease_a, disease_b = combination.diseases[0], combination.diseases[1]
        relation = DiseaseInteractionMatrix.COMORBIDITY_DATABASE.get(
            (disease_a, disease_b)
        )

        if relation is None:
            # Unknown combination: not explicitly invalid, but less confident
            return True, "Uncommon but possible combination"

        # Known relationship: generally valid
        return True, f"Known comorbidity: {relation.mechanism}"

    @classmethod
    def rank_combinations_by_likelihood(
        cls,
        combinations: List[DiseaseCombination],
    ) -> List[DiseaseCombination]:
        """
        Rank combinations by likelihood (confidence score).

        Args:
            combinations: List of DiseaseCombination

        Returns:
            Sorted list (highest confidence first)
        """
        sorted_combinations = sorted(
            combinations,
            key=lambda c: c.combined_confidence,
            reverse=True,
        )
        return sorted_combinations

    @staticmethod
    def estimate_symptom_allocation(
        diseases: List[str],
        detected_symptoms: List[str],
    ) -> Dict[str, List[str]]:
        """
        Estimate which symptoms belong to which disease in combination.

        Args:
            diseases: Disease names in combination
            detected_symptoms: Detected symptoms

        Returns:
            {disease_name: [allocated_symptoms]}
        """
        # TODO: Implement Bayesian symptom allocation
        # For now, return empty allocation
        return {disease: [] for disease in diseases}


class MultiDiseaseSession:
    """Session context for multi-disease diagnosis exploration."""

    def __init__(
        self,
        session_id: str,
        detected_symptoms: List[str],
        initial_candidates: List[DiseaseCombination],
    ):
        """Initialize multi-disease session."""
        self.session_id = session_id
        self.detected_symptoms = detected_symptoms
        self.explored_combinations = initial_candidates.copy()
        self.current_focus: Optional[DiseaseCombination] = (
            initial_candidates[0] if initial_candidates else None
        )
        self.confidence_history: Dict[str, List[float]] = {}

        # Track confidence changes
        for combo in initial_candidates:
            key = tuple(sorted(combo.diseases))
            self.confidence_history[key] = [combo.combined_confidence]

    def update_combination_confidence(
        self,
        combination: DiseaseCombination,
        new_confidence: float,
    ) -> None:
        """Track confidence change for a combination."""
        key = tuple(sorted(combination.diseases))
        if key not in self.confidence_history:
            self.confidence_history[key] = []
        self.confidence_history[key].append(new_confidence)
        self.current_focus = combination

    def should_continue_exploration(self) -> bool:
        """Determine if multi-disease exploration should continue."""
        # Continue if current focus confidence is below threshold
        if self.current_focus is None:
            return False

        # Stop if high confidence achieved
        if self.current_focus.combined_confidence > 0.80:
            return False

        # Stop after 10+ questions
        # (would need question counter in actual implementation)
        return True
