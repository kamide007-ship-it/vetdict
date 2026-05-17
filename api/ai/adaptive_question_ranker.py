"""Adaptive question ranking engine using machine learning features.

Combines information gain, question features, and learning signals to rank
diagnostic questions for optimal disease differentiation.
"""

import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

# Import optimization and feature modules
from api.ai.question_features import QuestionFeatureExtractor, QuestionFeatures
from api.ai.question_optimization import EntropyCalculator


@dataclass
class RankedQuestion:
    """Ranked diagnostic question with scoring breakdown."""

    question_id: str
    rank: int
    composite_score: float  # Final ranking score (0-1)
    information_gain: float  # IG component
    features: QuestionFeatures  # Extracted features
    score_breakdown: Dict[str, float]  # Component scores

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "rank": self.rank,
            "composite_score": round(self.composite_score, 3),
            "information_gain": round(self.information_gain, 3),
            "features": self.features.to_dict(),
            "score_breakdown": {k: round(v, 3) for k, v in self.score_breakdown.items()},
        }


class AdaptiveQuestionRanker:
    """ML-based question ranking engine."""

    # Default weights for composite scoring
    DEFAULT_WEIGHTS = {
        "information_gain": float(os.getenv("PHASE5_IG_WEIGHT", "0.40")),
        "fisher_ratio": float(os.getenv("PHASE5_FISHER_WEIGHT", "0.25")),
        "coverage": float(os.getenv("PHASE5_COVERAGE_WEIGHT", "0.15")),
        "fatigue": float(os.getenv("PHASE5_FATIGUE_WEIGHT", "-0.10")),
        "alignment": float(os.getenv("PHASE5_ALIGNMENT_WEIGHT", "0.20")),
    }

    # Configuration
    ENABLE_ML_RANKING = os.getenv("PHASE5_ML_OPTIMIZATION_ENABLED", "true").lower() == "true"
    ENABLE_DIVERSITY = os.getenv("PHASE5_DIVERSITY_CONSTRAINT", "true").lower() == "true"
    CANDIDATE_PRUNING_THRESHOLD = float(os.getenv("PHASE5_CANDIDATE_PRUNING_THRESHOLD", "0.05"))
    LEARNING_WEIGHT = float(os.getenv("PHASE5_LEARNING_FEEDBACK_WEIGHT", "0.8"))

    @classmethod
    def rank_questions(
        cls,
        questions_with_metadata: List[Dict[str, Any]],
        candidate_diseases: List[Dict[str, Any]],
        detected_symptoms: Set[str],
        previously_asked: Optional[Set[str]] = None,
        learned_weights: Optional[Dict[str, float]] = None,
        use_ml: bool = True,
    ) -> List[RankedQuestion]:
        """
        Rank diagnostic questions using ML-based scoring.

        Args:
            questions_with_metadata: List of question dicts with:
                - id: question ID
                - type: question type (binary, multiselect, numeric)
                - targets: diseases this question targets
                - answer_types: {answer_value: [targeted_diseases]}
            candidate_diseases: Current disease candidates with match_percent
            detected_symptoms: Set of detected symptom IDs
            previously_asked: Set of question IDs already asked
            learned_weights: Weights from learning feedback
            use_ml: Whether to use ML ranking (False = simple heuristic)

        Returns:
            List of RankedQuestion sorted by score (descending)
        """
        if not use_ml or not cls.ENABLE_ML_RANKING:
            return cls._simple_ranking(questions_with_metadata, candidate_diseases)

        ranked = []

        # Use learned weights if provided, otherwise defaults
        weights = learned_weights or cls.DEFAULT_WEIGHTS.copy()

        for question_metadata in questions_with_metadata:
            question_id = question_metadata.get("id", "")

            # Filter out invalid questions
            if not question_id or not question_metadata.get("targets"):
                continue

            # Calculate information gain
            ig = EntropyCalculator.calculate_information_gain(
                question_id,
                question_metadata.get("targets", []),
                candidate_diseases,
            )

            # Extract features
            features = QuestionFeatureExtractor.extract_features(
                question_id=question_id,
                question_type=question_metadata.get("type", "binary"),
                question_targets=question_metadata.get("targets", []),
                target_diseases_per_answer=question_metadata.get("answer_types", {}),
                candidate_diseases=candidate_diseases,
                detected_symptoms=detected_symptoms,
                symptom_implications=cls._build_symptom_implications(),
                previously_asked=previously_asked or set(),
            )

            # Calculate composite score
            score_breakdown = {}
            composite_score = 0.0

            # Information gain component
            ig_weight = weights.get("information_gain", 0.40)
            ig_score = ig.effectiveness_score
            score_breakdown["information_gain"] = ig_score * ig_weight
            composite_score += score_breakdown["information_gain"]

            # Fisher ratio (differentiator) component
            fisher_weight = weights.get("fisher_ratio", 0.25)
            fisher_score = features.differentiator_score
            score_breakdown["fisher_ratio"] = fisher_score * fisher_weight
            composite_score += score_breakdown["fisher_ratio"]

            # Coverage component
            coverage_weight = weights.get("coverage", 0.15)
            coverage_score = features.coverage_score
            score_breakdown["coverage"] = coverage_score * coverage_weight
            composite_score += score_breakdown["coverage"]

            # Fatigue penalty (negative weight)
            fatigue_weight = weights.get("fatigue", -0.10)
            fatigue_penalty = features.fatigue_score
            score_breakdown["fatigue"] = fatigue_penalty * fatigue_weight
            composite_score += score_breakdown["fatigue"]

            # Symptom alignment bonus
            alignment_weight = weights.get("alignment", 0.20)
            alignment_score = features.symptom_alignment_bonus
            score_breakdown["alignment"] = alignment_score * alignment_weight
            composite_score += score_breakdown["alignment"]

            # Diversity bonus
            diversity_score = features.category_diversity * 0.05  # Small bonus
            score_breakdown["diversity"] = diversity_score
            composite_score += diversity_score

            # Normalize to 0-1
            composite_score = max(0.0, min(composite_score, 1.0))

            ranked.append(
                RankedQuestion(
                    question_id=question_id,
                    rank=0,  # Will be set after sorting
                    composite_score=composite_score,
                    information_gain=ig.information_gain,
                    features=features,
                    score_breakdown=score_breakdown,
                )
            )

        # Sort by composite score
        ranked.sort(key=lambda x: x.composite_score, reverse=True)

        # Apply diversity constraint if enabled
        if cls.ENABLE_DIVERSITY:
            ranked = cls._apply_diversity_constraint(ranked)

        # Filter out low-coverage questions
        ranked = [q for q in ranked if q.features.coverage_score > 0.0]

        # Set ranks
        for i, q in enumerate(ranked, 1):
            q.rank = i

        return ranked

    @staticmethod
    def _simple_ranking(
        questions_with_metadata: List[Dict[str, Any]],
        candidate_diseases: List[Dict[str, Any]],
    ) -> List[RankedQuestion]:
        """
        Simple heuristic ranking (backward compatibility fallback).

        Ranks by coverage score only.
        """
        ranked = []

        for question_metadata in questions_with_metadata:
            question_id = question_metadata.get("id", "")
            targets = question_metadata.get("targets", [])

            if not question_id or not targets:
                continue

            # Calculate coverage
            coverage = QuestionFeatureExtractor.calculate_coverage_score(targets, candidate_diseases)

            if coverage > 0:
                ranked.append(
                    RankedQuestion(
                        question_id=question_id,
                        rank=0,
                        composite_score=coverage,
                        information_gain=0.0,
                        features=None,
                        score_breakdown={"coverage": coverage},
                    )
                )

        # Sort by coverage
        ranked.sort(key=lambda x: x.composite_score, reverse=True)

        # Set ranks
        for i, q in enumerate(ranked, 1):
            q.rank = i

        return ranked

    @staticmethod
    def _apply_diversity_constraint(
        ranked_questions: List[RankedQuestion],
    ) -> List[RankedQuestion]:
        """
        Apply diversity constraint to prevent clustering questions.

        Reorders questions to spread across disease categories.
        """
        if len(ranked_questions) <= 3:
            return ranked_questions

        # Group by category
        categories = {}
        for q in ranked_questions:
            cat = QuestionFeatureExtractor.QUESTION_CATEGORIES.get(q.question_id, "other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(q)

        # Interleave questions from different categories
        result = []
        max_per_category = 3
        category_counts = {cat: 0 for cat in categories}

        # Round-robin selection
        while len(result) < len(ranked_questions):
            for cat in categories:
                if category_counts[cat] < max_per_category and len(categories[cat]) > 0:
                    # Find next question from this category
                    for q in categories[cat]:
                        if q not in result:
                            result.append(q)
                            category_counts[cat] += 1
                            break

        return result

    @staticmethod
    def _build_symptom_implications() -> Dict[str, List[str]]:
        """
        Build mapping of question ID to related symptoms.

        Returns:
            {question_id: [symptom_ids]}
        """
        return {
            "vomiting_frequency": ["vomiting"],
            "blood_in_vomit": ["vomiting", "bloody_stool"],
            "diarrhea_consistency": ["diarrhea", "bloody_stool"],
            "cough_type": ["coughing"],
            "urine_color": ["blood_urine"],
            "onset_timeline": ["fever", "lethargy"],
            "vaccine_status": [],  # Not directly related to symptoms
            "fever_present": ["fever"],
        }

    @classmethod
    def update_weights_from_feedback(
        cls,
        current_weights: Dict[str, float],
        feedback_signal: Dict[str, Any],
    ) -> Dict[str, float]:
        """
        Update ML weights based on feedback from diagnostic outcomes.

        Args:
            current_weights: Current weight dict
            feedback_signal: {question_id: effectiveness_score, ...}

        Returns:
            Updated weights dict
        """
        # Simple exponential moving average update
        updated = current_weights.copy()

        # This is a placeholder for more sophisticated learning
        # In production, would use gradient descent or bandit algorithm

        return updated
