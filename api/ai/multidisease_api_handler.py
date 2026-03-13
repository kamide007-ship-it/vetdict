"""Multi-disease diagnosis API handler for Stage 6 integration.

Orchestrates Stage 3-5 components to provide comprehensive multi-disease
diagnostic analysis through a single API endpoint.
"""

from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

from api.ai.multidisease_detector import MultiDiseaseDetector
from api.ai.symptom_context_engine import (
    SymptomContextualizer,
    AmbiguitySolver,
)
from api.ai.combined_confidence_calculator import CombinedConfidenceCalculator
from api.ai.multidisease_question_generator import (
    MultiDiseaseQuestionGenerator,
    DiscriminativeQuestionRanker,
)


class MultiDiseaseAnalyzer:
    """Orchestrates multi-disease analysis across all Phase 6 stages."""

    @classmethod
    def analyze_for_multidisease(
        cls,
        symptom_ids: List[str],
        detected_symptoms_ja: Optional[str] = None,
        detected_symptoms_en: Optional[str] = None,
        suspected_diseases: Optional[List[Dict[str, Any]]] = None,
        disease_database: Optional[List[Dict[str, Any]]] = None,
        patient_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Perform comprehensive multi-disease analysis.

        Orchestrates Stage 3-5 analysis for multi-disease diagnosis scenarios.

        Args:
            symptom_ids: List of detected symptom IDs
            detected_symptoms_ja: Japanese symptom description
            detected_symptoms_en: English symptom description
            suspected_diseases: Current disease candidates with scores
            disease_database: Disease database for context
            patient_context: Patient information (age, species, etc.)

        Returns:
            Comprehensive analysis response
        """
        if not suspected_diseases:
            suspected_diseases = []
        if not disease_database:
            disease_database = []

        # Stage 1: Check if multi-disease mode should be activated
        should_explore = MultiDiseaseDetector.should_explore_multidisease(
            detected_symptoms=symptom_ids,
            suspected_diseases=suspected_diseases,
            patient_context=patient_context,
        )

        response = {
            "multidisease_mode_enabled": should_explore,
            "symptom_count": len(symptom_ids),
            "disease_candidates_count": len(suspected_diseases),
        }

        if not should_explore:
            # Single disease mode - return minimal multi-disease data
            return response

        # Stage 2: Generate multi-disease combination candidates
        combinations = MultiDiseaseDetector.generate_multidisease_candidates(
            suspected_diseases=suspected_diseases,
            detected_symptoms=symptom_ids,
            patient_context=patient_context,
        )

        response["combinations_found"] = len(combinations)
        response["combinations"] = [c.to_dict() for c in combinations[:3]]  # Top 3

        # Stage 3: Analyze symptom ambiguities
        ambiguity_analysis = MultiDiseaseDetector.analyze_symptom_ambiguity(
            detected_symptoms=symptom_ids,
            suspected_diseases=suspected_diseases,
            disease_database=disease_database,
        )

        response["ambiguity_analysis"] = {
            "high_ambiguity_symptoms": ambiguity_analysis.get("high_ambiguity_symptoms", []),
            "adjustment_factor": ambiguity_analysis.get("adjustment_factor", 1.0),
            "recommendations": ambiguity_analysis.get("recommendations", {}),
            "reports_count": len(ambiguity_analysis.get("ambiguity_reports", [])),
        }

        # Stage 4: If we have combinations, calculate combined confidence
        if combinations:
            primary_combination = combinations[0]

            # Apply ambiguity adjustment
            adjusted_combination = MultiDiseaseDetector.apply_ambiguity_adjustment(
                combination=primary_combination,
                adjustment_factor=ambiguity_analysis.get("adjustment_factor", 1.0),
            )

            # Calculate detailed Bayesian breakdown
            breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
                diseases=adjusted_combination.diseases,
                individual_confidences=adjusted_combination.component_confidences,
                detected_symptoms=symptom_ids,
                symptom_disease_mapping=cls._build_symptom_mapping(
                    symptom_ids, adjusted_combination.diseases, disease_database
                ),
                patient_context=patient_context,
            )

            response["confidence_breakdown"] = breakdown.to_dict()

            # Stage 5: Generate optimized questions
            questions = MultiDiseaseQuestionGenerator.generate_combination_focused_questions(
                diseases=adjusted_combination.diseases,
                detected_symptoms=symptom_ids,
                disease_database=disease_database,
            )

            # Rank questions by discriminative value
            if questions:
                ranked = DiscriminativeQuestionRanker.rank_questions_for_combination(
                    diseases=adjusted_combination.diseases,
                    candidate_questions=questions,
                    detected_symptoms=symptom_ids,
                )

                response["next_questions"] = [
                    {
                        "question": q.to_dict(),
                        "ranking_score": round(score, 3),
                        "explanation": explanation,
                    }
                    for q, score, explanation in ranked[:3]  # Top 3 questions
                ]

        # Add English explanation
        if response.get("confidence_breakdown"):
            response["explanation_en"] = response["confidence_breakdown"].get(
                "explanation_en", ""
            )
            response["explanation_ja"] = response["confidence_breakdown"].get(
                "explanation_ja", ""
            )

        return response

    @staticmethod
    def _build_symptom_mapping(
        symptom_ids: List[str],
        disease_names: List[str],
        disease_database: List[Dict[str, Any]],
    ) -> Dict[str, set]:
        """
        Build symptom-to-disease mapping.

        Args:
            symptom_ids: List of symptom IDs
            disease_names: List of disease names
            disease_database: Disease database

        Returns:
            {symptom_id: {disease_names_with_symptom}}
        """
        mapping = {}

        for symptom_id in symptom_ids:
            mapping[symptom_id] = set()

            for disease_name in disease_names:
                disease = next(
                    (d for d in disease_database if d.get("name") == disease_name),
                    None,
                )

                if disease:
                    disease_symptoms = disease.get("symptoms", [])
                    if any(symptom_id in str(s) for s in disease_symptoms):
                        mapping[symptom_id].add(disease_name)

        return mapping

    @classmethod
    def validate_request(
        cls,
        request_data: Dict[str, Any],
    ) -> tuple[bool, Optional[str]]:
        """
        Validate multi-disease analysis request.

        Args:
            request_data: Request JSON data

        Returns:
            (is_valid, error_message) tuple
        """
        # Require symptom_ids
        if "symptom_ids" not in request_data or not request_data["symptom_ids"]:
            return False, "symptom_ids required and cannot be empty"

        if not isinstance(request_data["symptom_ids"], list):
            return False, "symptom_ids must be a list"

        # Optional: suspected_diseases should be list if present
        if "suspected_diseases" in request_data:
            if not isinstance(request_data["suspected_diseases"], list):
                return False, "suspected_diseases must be a list"

        return True, None
