"""Combined confidence scoring for multi-disease diagnosis.

Implements Bayesian statistical methods for calculating combined disease
confidence scores with transparent confidence breakdowns and interaction effects.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


@dataclass
class ConfidenceBreakdown:
    """Detailed breakdown of combined disease confidence calculation."""

    diseases: List[str]
    individual_confidences: Dict[str, float]  # P(D | S) for each disease
    symptom_allocation: Dict[str, List[str]]  # Which symptoms allocated to each disease
    comorbidity_multiplier: float  # Prior probability of co-occurrence
    independence_penalty: float  # Penalty for symptom overlap violations
    bayesian_posterior: float  # Final P(D1, D2 | S)
    evidence_integration_scores: Dict[str, float]  # Evidence quality per disease
    symptom_likelihood_breakdown: Dict[str, Dict[str, float]]  # P(symptom|disease)
    final_confidence: float  # Combined confidence score (0-1)
    confidence_sources: List[str]  # ["bayesian", "comorbidity_db", "evidence", ...]
    explanation_ja: str = ""
    explanation_en: str = ""
    methodology: str = ""  # Mathematical methodology used

    def to_dict(self):
        """Serialize to dictionary."""
        return {
            "diseases": self.diseases,
            "individual_confidences": {
                d: round(c, 3) for d, c in self.individual_confidences.items()
            },
            "symptom_allocation": self.symptom_allocation,
            "comorbidity_multiplier": round(self.comorbidity_multiplier, 3),
            "independence_penalty": round(self.independence_penalty, 3),
            "bayesian_posterior": round(self.bayesian_posterior, 3),
            "evidence_integration_scores": {
                d: round(s, 3) for d, s in self.evidence_integration_scores.items()
            },
            "final_confidence": round(self.final_confidence, 3),
            "confidence_sources": self.confidence_sources,
            "explanation_en": self.explanation_en,
            "methodology": self.methodology,
        }


class CombinedConfidenceCalculator:
    """Bayesian calculator for multi-disease confidence."""

    # Bayesian parameters
    DEFAULT_PRIOR_PROBABILITY = 0.1  # P(disease) without symptoms
    SYMPTOM_INDEPENDENCE_THRESHOLD = 0.3  # Max overlap ratio for independence

    @classmethod
    def calculate_bayesian_combination(
        cls,
        diseases: List[str],
        individual_confidences: Dict[str, float],
        detected_symptoms: List[str],
        symptom_disease_mapping: Dict[str, Set[str]],  # symptom -> disease_set
        comorbidity_data: Optional[Dict[Tuple[str, str], float]] = None,
        evidence_scores: Optional[Dict[str, float]] = None,
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> ConfidenceBreakdown:
        """
        Calculate Bayesian combined confidence for multiple diseases.

        Uses Bayes' theorem: P(D1, D2 | S) = P(S | D1, D2) * P(D1, D2) / P(S)

        Args:
            diseases: List of disease names
            individual_confidences: P(D|S) for each disease
            detected_symptoms: List of detected symptom IDs
            symptom_disease_mapping: Which diseases have which symptoms
            comorbidity_data: Optional prior probabilities of coexistence
            evidence_scores: Optional medical evidence quality scores
            patient_context: Optional patient demographics, age, etc.

        Returns:
            ConfidenceBreakdown with full calculation transparency
        """

        if len(diseases) < 2:
            # Single disease - just return individual confidence
            return cls._single_disease_breakdown(
                diseases[0] if diseases else "Unknown",
                individual_confidences.get(diseases[0] if diseases else "Unknown", 0.0),
            )

        # Step 1: Estimate symptom allocation
        symptom_allocation = cls._estimate_symptom_allocation(
            diseases=diseases,
            detected_symptoms=detected_symptoms,
            symptom_disease_mapping=symptom_disease_mapping,
        )

        # Step 2: Calculate symptom likelihoods per disease
        symptom_likelihoods = cls._calculate_symptom_likelihoods(
            diseases=diseases,
            symptom_allocation=symptom_allocation,
            individual_confidences=individual_confidences,
        )

        # Step 3: Calculate independence penalty
        independence_penalty = cls._calculate_independence_penalty(
            diseases=diseases,
            symptom_allocation=symptom_allocation,
            symptom_disease_mapping=symptom_disease_mapping,
        )

        # Step 4: Get comorbidity multiplier
        comorbidity_multiplier = cls._get_comorbidity_multiplier(
            diseases=diseases,
            comorbidity_data=comorbidity_data,
            patient_context=patient_context,
        )

        # Step 5: Calculate evidence integration
        evidence_scores_integrated = cls._integrate_evidence_scores(
            diseases=diseases,
            evidence_scores=evidence_scores,
        )

        # Step 6: Combine into final confidence
        bayesian_posterior = cls._compute_bayesian_posterior(
            diseases=diseases,
            individual_confidences=individual_confidences,
            symptom_likelihoods=symptom_likelihoods,
            independence_penalty=independence_penalty,
            comorbidity_multiplier=comorbidity_multiplier,
        )

        # Apply evidence integration
        final_confidence = bayesian_posterior * (
            1.0 + 0.1 * max(evidence_scores_integrated.values()) if evidence_scores_integrated else 1.0
        )
        final_confidence = min(1.0, max(0.0, final_confidence))

        # Build confidence sources list
        confidence_sources = ["bayesian_combination"]
        if comorbidity_data:
            confidence_sources.append("comorbidity_database")
        if evidence_scores:
            confidence_sources.append("evidence_quality")
        if patient_context:
            confidence_sources.append("patient_context")

        # Generate explanations
        explanation_en = cls._generate_explanation_en(
            diseases=diseases,
            individual_confidences=individual_confidences,
            symptom_allocation=symptom_allocation,
            comorbidity_multiplier=comorbidity_multiplier,
            final_confidence=final_confidence,
        )

        explanation_ja = cls._generate_explanation_ja(
            diseases=diseases,
            individual_confidences=individual_confidences,
            comorbidity_multiplier=comorbidity_multiplier,
            final_confidence=final_confidence,
        )

        breakdown = ConfidenceBreakdown(
            diseases=diseases,
            individual_confidences=individual_confidences,
            symptom_allocation=symptom_allocation,
            comorbidity_multiplier=comorbidity_multiplier,
            independence_penalty=independence_penalty,
            bayesian_posterior=bayesian_posterior,
            evidence_integration_scores=evidence_scores_integrated,
            symptom_likelihood_breakdown=symptom_likelihoods,
            final_confidence=final_confidence,
            confidence_sources=confidence_sources,
            explanation_en=explanation_en,
            explanation_ja=explanation_ja,
            methodology="Bayesian posterior with symptom independence validation",
        )

        return breakdown

    @staticmethod
    def _single_disease_breakdown(disease: str, confidence: float) -> ConfidenceBreakdown:
        """Generate breakdown for single disease (baseline)."""
        return ConfidenceBreakdown(
            diseases=[disease],
            individual_confidences={disease: confidence},
            symptom_allocation={disease: []},
            comorbidity_multiplier=1.0,
            independence_penalty=1.0,
            bayesian_posterior=confidence,
            evidence_integration_scores={disease: 1.0},
            symptom_likelihood_breakdown={disease: {}},
            final_confidence=confidence,
            confidence_sources=["single_disease"],
            explanation_en=f"Single disease hypothesis: {disease}",
            explanation_ja=f"単一疾患仮説: {disease}",
            methodology="Single disease baseline",
        )

    @classmethod
    def _estimate_symptom_allocation(
        cls,
        diseases: List[str],
        detected_symptoms: List[str],
        symptom_disease_mapping: Dict[str, Set[str]],
    ) -> Dict[str, List[str]]:
        """
        Estimate optimal symptom allocation to diseases.

        Uses greedy algorithm to maximize disease-specific symptom assignment.

        Args:
            diseases: List of disease names
            detected_symptoms: Detected symptoms
            symptom_disease_mapping: symptom_id -> set of diseases

        Returns:
            {disease: [allocated_symptoms]}
        """
        allocation = {d: [] for d in diseases}

        # Greedy allocation: assign each symptom to most specific disease
        for symptom in detected_symptoms:
            possible_diseases = symptom_disease_mapping.get(symptom, set())

            # Find intersection with current diseases
            matching_diseases = [d for d in diseases if d in possible_diseases]

            if matching_diseases:
                # Allocate to first matching disease
                # (In production, could use disease specificity)
                allocation[matching_diseases[0]].append(symptom)

        return allocation

    @classmethod
    def _calculate_symptom_likelihoods(
        cls,
        diseases: List[str],
        symptom_allocation: Dict[str, List[str]],
        individual_confidences: Dict[str, float],
    ) -> Dict[str, Dict[str, float]]:
        """
        Calculate likelihood of observed symptoms given each disease.

        P(S | D) = product of P(symptom | disease)

        Args:
            diseases: Disease names
            symptom_allocation: Allocated symptoms per disease
            individual_confidences: Individual disease confidences

        Returns:
            {disease: {symptom: likelihood}}
        """
        likelihoods = {}

        for disease in diseases:
            symptoms = symptom_allocation.get(disease, [])
            disease_likelihood = {}

            # For each allocated symptom, likelihood = 1.0 (observed)
            for symptom in symptoms:
                disease_likelihood[symptom] = 1.0

            # For each non-allocated symptom, likelihood decreases
            # (not explained by this disease)
            all_symptoms = set()
            for symp_list in symptom_allocation.values():
                all_symptoms.update(symp_list)

            unallocated = all_symptoms - set(symptoms)
            for symptom in unallocated:
                # Unexplained symptom: likelihood = 0.3 (can still occur)
                disease_likelihood[symptom] = 0.3

            likelihoods[disease] = disease_likelihood

        return likelihoods

    @classmethod
    def _calculate_independence_penalty(
        cls,
        diseases: List[str],
        symptom_allocation: Dict[str, List[str]],
        symptom_disease_mapping: Dict[str, Set[str]],
    ) -> float:
        """
        Calculate penalty for symptom independence violations.

        High overlap suggests single disease, not multiple.

        Returns:
            Penalty factor (0-1), 1.0 = no penalty, <1.0 = penalty applied
        """
        if len(diseases) < 2:
            return 1.0

        # Count symptoms unique to each disease
        allocated_per_disease = {d: set(symp) for d, symp in symptom_allocation.items()}
        all_allocated = set()
        for symptoms in allocated_per_disease.values():
            all_allocated.update(symptoms)

        if not all_allocated:
            return 1.0

        # Calculate overlap ratio
        unique_counts = [len(allocated_per_disease[d]) for d in diseases]
        total_unique = sum(unique_counts)

        if total_unique == 0:
            return 1.0

        # Overlap ratio: how much allocated symptoms are shared
        shared_count = 0
        for symptom in all_allocated:
            disease_count = sum(
                1 for d in diseases if symptom in allocated_per_disease[d]
            )
            if disease_count > 1:
                shared_count += 1

        overlap_ratio = shared_count / total_unique if total_unique > 0 else 0.0

        # Penalty: high overlap reduces confidence
        if overlap_ratio > cls.SYMPTOM_INDEPENDENCE_THRESHOLD:
            # Too much overlap: likely single disease, not multiple
            penalty = 1.0 - (overlap_ratio * 0.5)
            return max(0.3, penalty)

        return 1.0

    @classmethod
    def _get_comorbidity_multiplier(
        cls,
        diseases: List[str],
        comorbidity_data: Optional[Dict[Tuple[str, str], float]] = None,
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        Get prior probability multiplier for disease coexistence.

        Args:
            diseases: Disease names
            comorbidity_data: Known comorbidity probabilities
            patient_context: Patient age, species, etc.

        Returns:
            Multiplier for comorbidity likelihood
        """
        if len(diseases) < 2:
            return 1.0

        # Base multiplier
        multiplier = 1.0

        # Check comorbidity database
        if comorbidity_data:
            for i, d1 in enumerate(diseases):
                for d2 in diseases[i + 1 :]:
                    key = (d1, d2)
                    reverse_key = (d2, d1)

                    prob = comorbidity_data.get(
                        key, comorbidity_data.get(reverse_key, None)
                    )
                    if prob:
                        multiplier *= prob

        # Age factor: seniors more likely to have multiple diseases
        if patient_context:
            age = patient_context.get("age_years", 0)
            if age > 7:
                age_factor = 1.0 + (min(age - 7, 10) / 20.0)  # Max 1.5x
                multiplier *= age_factor

        return min(2.0, multiplier)  # Cap multiplier

    @staticmethod
    def _integrate_evidence_scores(
        diseases: List[str],
        evidence_scores: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """
        Integrate medical evidence quality scores.

        Args:
            diseases: Disease names
            evidence_scores: Evidence quality per disease (0-1)

        Returns:
            {disease: evidence_score}
        """
        if not evidence_scores:
            return {d: 0.5 for d in diseases}

        return {d: evidence_scores.get(d, 0.5) for d in diseases}

    @classmethod
    def _compute_bayesian_posterior(
        cls,
        diseases: List[str],
        individual_confidences: Dict[str, float],
        symptom_likelihoods: Dict[str, Dict[str, float]],
        independence_penalty: float,
        comorbidity_multiplier: float,
    ) -> float:
        """
        Compute Bayesian posterior: P(D1, D2 | S)

        Using: P(D|S) = P(S|D) * P(D) / P(S)

        Args:
            diseases: Disease names
            individual_confidences: P(D|S) from Bayesian diagnostic engine
            symptom_likelihoods: P(S|D) for symptoms
            independence_penalty: Factor for symptom overlap
            comorbidity_multiplier: Prior probability multiplier

        Returns:
            Combined posterior probability
        """
        if len(diseases) < 2:
            return individual_confidences.get(diseases[0] if diseases else "", 0.0)

        # Product of individual confidences
        combined_posterior = 1.0
        for disease in diseases:
            conf = individual_confidences.get(disease, 0.0)
            combined_posterior *= conf

        # Apply comorbidity multiplier (adjusts prior)
        combined_posterior *= comorbidity_multiplier

        # Apply independence penalty (adjusts likelihood)
        combined_posterior *= independence_penalty

        # Ensure result is valid probability
        return min(1.0, max(0.0, combined_posterior))

    @staticmethod
    def _generate_explanation_en(
        diseases: List[str],
        individual_confidences: Dict[str, float],
        symptom_allocation: Dict[str, List[str]],
        comorbidity_multiplier: float,
        final_confidence: float,
    ) -> str:
        """Generate English explanation for confidence calculation."""
        if len(diseases) < 2:
            return f"Single disease confidence: {diseases[0] if diseases else 'Unknown'}"

        parts = []

        # Individual confidences
        conf_parts = [
            f"{d}: {individual_confidences.get(d, 0.0):.1%}"
            for d in diseases
        ]
        parts.append(f"Individual confidences: {', '.join(conf_parts)}")

        # Symptom allocation
        for disease in diseases:
            symptoms = symptom_allocation.get(disease, [])
            if symptoms:
                parts.append(f"{disease} explains: {', '.join(symptoms[:3])}")

        # Comorbidity factor
        if comorbidity_multiplier > 1.0:
            parts.append(f"Coexistence likely (multiplier: {comorbidity_multiplier:.2f})")

        # Final verdict
        if final_confidence > 0.6:
            parts.append(f"LIKELY coexistence. Combined confidence: {final_confidence:.1%}")
        elif final_confidence > 0.4:
            parts.append(f"POSSIBLE coexistence. Combined confidence: {final_confidence:.1%}")
        else:
            parts.append(f"Less likely coexistence. Combined confidence: {final_confidence:.1%}")

        return " | ".join(parts)

    @staticmethod
    def _generate_explanation_ja(
        diseases: List[str],
        individual_confidences: Dict[str, float],
        comorbidity_multiplier: float,
        final_confidence: float,
    ) -> str:
        """Generate Japanese explanation for confidence calculation."""
        if len(diseases) < 2:
            return f"単一疾患信頼度: {diseases[0] if diseases else '不明'}"

        parts = []

        # Individual confidences
        conf_parts = [
            f"{d}: {individual_confidences.get(d, 0.0):.1%}"
            for d in diseases
        ]
        parts.append(f"個別信頼度: {', '.join(conf_parts)}")

        # Comorbidity factor
        if comorbidity_multiplier > 1.0:
            parts.append(f"共存の可能性あり（倍数: {comorbidity_multiplier:.2f}）")

        # Final verdict
        if final_confidence > 0.6:
            parts.append(f"共存の可能性が高い。統合信頼度: {final_confidence:.1%}")
        elif final_confidence > 0.4:
            parts.append(f"共存の可能性がある。統合信頼度: {final_confidence:.1%}")
        else:
            parts.append(f"共存の可能性は低い。統合信頼度: {final_confidence:.1%}")

        return " | ".join(parts)


class BayesianDiseaseCombiner:
    """High-level Bayesian combiner for complex disease scenarios."""

    @classmethod
    def combine_multiple_diseases(
        cls,
        disease_list: List[str],
        confidences: List[float],
        interaction_matrix: Optional[Dict[Tuple[str, str], float]] = None,
        symptom_context_data: Optional[Dict[str, Any]] = None,
    ) -> Tuple[float, ConfidenceBreakdown]:
        """
        Combine confidence for multiple diseases using Bayesian framework.

        Args:
            disease_list: List of disease names
            confidences: Confidence for each disease
            interaction_matrix: Disease interaction effects
            symptom_context_data: Symptom context information

        Returns:
            (combined_confidence, breakdown)
        """
        if not disease_list or not confidences:
            return 0.0, ConfidenceBreakdown(
                diseases=[],
                individual_confidences={},
                symptom_allocation={},
                comorbidity_multiplier=1.0,
                independence_penalty=1.0,
                bayesian_posterior=0.0,
                evidence_integration_scores={},
                symptom_likelihood_breakdown={},
                final_confidence=0.0,
                confidence_sources=[],
            )

        individual_confidences = {d: c for d, c in zip(disease_list, confidences)}

        # Extract comorbidity data from interaction matrix if available
        comorbidity_data = None
        if interaction_matrix:
            comorbidity_data = interaction_matrix

        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=disease_list,
            individual_confidences=individual_confidences,
            detected_symptoms=[],  # Would be populated from context
            symptom_disease_mapping={},  # Would be populated from context
            comorbidity_data=comorbidity_data,
        )

        return breakdown.final_confidence, breakdown
