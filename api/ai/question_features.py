"""Question feature extraction for machine learning-based ranking.

Extracts discriminative features from questions that enable intelligent
ranking based on disease differentiation power, coverage, and user burden.
"""

import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


@dataclass
class QuestionFeatures:
    """Machine learning features for a diagnostic question."""

    question_id: str
    differentiator_score: float  # Fisher ratio or similar (0-1)
    coverage_score: float  # Fraction of candidates this question targets
    answer_specificity: float  # How much variation in answers across diseases
    fatigue_score: float  # User burden penalty (0-1, higher = more burden)
    symptom_alignment_bonus: float  # How much this overlaps with reported symptoms
    category_diversity: float  # Encourages spread across disease categories (0-1)

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "differentiator_score": round(self.differentiator_score, 3),
            "coverage_score": round(self.coverage_score, 3),
            "answer_specificity": round(self.answer_specificity, 3),
            "fatigue_score": round(self.fatigue_score, 3),
            "symptom_alignment_bonus": round(self.symptom_alignment_bonus, 3),
            "category_diversity": round(self.category_diversity, 3),
        }


class QuestionFeatureExtractor:
    """Extracts features from diagnostic questions."""

    # Question categories for diversity calculation
    QUESTION_CATEGORIES = {
        "vomiting_frequency": "gastrointestinal",
        "blood_in_vomit": "gastrointestinal",
        "diarrhea_consistency": "gastrointestinal",
        "cough_type": "respiratory",
        "urine_color": "urinary",
        "onset_timeline": "systemic",
        "vaccine_status": "preventive",
        "fever_present": "systemic",
    }

    # Question type burden scoring
    QUESTION_TYPE_BURDEN = {
        "binary": 0.2,  # Least burden (yes/no)
        "multiselect": 0.5,  # Medium burden (multiple choices)
        "numeric": 0.6,  # Moderate burden (entering numbers)
    }

    @staticmethod
    def calculate_coverage_score(
        question_targets: List[str],
        candidate_diseases: List[Dict[str, Any]],
    ) -> float:
        """
        Calculate what fraction of candidates this question targets.

        Args:
            question_targets: Diseases this question targets
            candidate_diseases: Current disease candidates

        Returns:
            Coverage score (0-1)
        """
        if not candidate_diseases:
            return 0.0

        target_set = set(question_targets)
        candidate_names = {d.get("name", "") for d in candidate_diseases if d.get("name")}

        if not candidate_names:
            return 0.0

        overlap = len(target_set & candidate_names)
        return overlap / len(candidate_names)

    @staticmethod
    def calculate_answer_specificity(
        question_targets: List[str],
        target_diseases_per_answer: Dict[str, List[str]],
    ) -> float:
        """
        Calculate how specific (discriminative) the question answers are.

        Specificity is high if different diseases give different answers.

        Args:
            question_targets: Main target diseases
            target_diseases_per_answer: {answer_option: [target_diseases]}

        Returns:
            Specificity score (0-1)
        """
        if len(target_diseases_per_answer) < 2:
            return 0.1  # Binary question, low specificity

        # Calculate Gini impurity of answer distribution
        target_set = set(question_targets)
        answer_counts = {}

        for answer, diseases in target_diseases_per_answer.items():
            overlap = len(set(diseases) & target_set)
            answer_counts[answer] = overlap

        total = sum(answer_counts.values())
        if total == 0:
            return 0.0

        # Gini = 1 - sum(p_i^2)
        gini = 1.0
        for count in answer_counts.values():
            p = count / total
            gini -= p * p

        return gini  # Higher gini = more specific

    @staticmethod
    def calculate_fatigue_penalty(
        question_id: str,
        previously_asked: Set[str],
        question_type: str,
        last_asked_times: Optional[Dict[str, float]] = None,
    ) -> float:
        """
        Calculate user fatigue penalty for this question.

        Penalizes:
        - Recently asked questions (exponential decay)
        - Multiselect questions (higher burden than binary)

        Args:
            question_id: ID of the question
            previously_asked: Set of question IDs already asked
            question_type: Type of question (binary, multiselect, numeric)
            last_asked_times: {question_id: timestamp} of when asked

        Returns:
            Fatigue score (0-1, higher = more burden)
        """
        fatigue = 0.0

        # Penalty for recently asked question
        if question_id in previously_asked:
            if last_asked_times and question_id in last_asked_times:
                # Exponential decay: penalty decreases as time passes
                time_since = time.time() - last_asked_times[question_id]
                recency_hours = time_since / 3600.0
                # After 6 hours, penalty drops to ~0.1
                recency_penalty = 0.8 * math.exp(-recency_hours / 6.0)
                fatigue += recency_penalty
            else:
                # Recently asked in this session
                fatigue += 0.6

        # Penalty for question type burden
        question_burden = QuestionFeatureExtractor.QUESTION_TYPE_BURDEN.get(question_type, 0.5)
        fatigue += question_burden * 0.3  # 30% weight for burden

        return min(fatigue, 1.0)  # Cap at 1.0

    @staticmethod
    def calculate_symptom_alignment(
        question_id: str,
        symptom_implications: Dict[str, List[str]],
        detected_symptoms: Set[str],
    ) -> float:
        """
        Calculate how much this question aligns with reported symptoms.

        High alignment bonus when question relates to symptoms already reported.
        Negative alignment when question seems to contradict reported absence.

        Args:
            question_id: ID of the question
            symptom_implications: {question_id: [symptoms_it_relates_to]}
            detected_symptoms: Set of detected symptom IDs

        Returns:
            Alignment bonus (-1.0 to 1.0)
        """
        if question_id not in symptom_implications:
            return 0.0

        related_symptoms = set(symptom_implications[question_id])
        if not related_symptoms:
            return 0.0

        # Check overlap with detected symptoms
        positive_overlap = len(related_symptoms & detected_symptoms)
        total_related = len(related_symptoms)

        if total_related == 0:
            return 0.0

        # Positive bonus if symptoms are detected
        if positive_overlap > 0:
            return positive_overlap / total_related  # 0 to 1

        # Neutral if we don't know
        return 0.0

    @staticmethod
    def calculate_category_diversity(
        question_id: str,
        asked_questions: List[str],
    ) -> float:
        """
        Calculate diversity bonus based on question categories.

        Encourages spreading questions across different disease categories
        rather than clustering in one area.

        Args:
            question_id: ID of the question
            asked_questions: List of question IDs already asked

        Returns:
            Diversity score (0-1, higher = more diverse)
        """
        question_category = QuestionFeatureExtractor.QUESTION_CATEGORIES.get(question_id, "other")

        # Count categories already asked
        asked_categories = {}
        for q_id in asked_questions:
            category = QuestionFeatureExtractor.QUESTION_CATEGORIES.get(q_id, "other")
            asked_categories[category] = asked_categories.get(category, 0) + 1

        # If this category hasn't been asked, full diversity bonus
        if question_category not in asked_categories:
            return 1.0

        # If already asked, penalty decreases with number asked
        times_asked = asked_categories[question_category]
        # After asking 3 times in same category, diversity penalty is high
        diversity = 1.0 / (1.0 + times_asked)

        return diversity

    @classmethod
    def extract_features(
        cls,
        question_id: str,
        question_type: str,
        question_targets: List[str],
        target_diseases_per_answer: Dict[str, List[str]],
        candidate_diseases: List[Dict[str, Any]],
        detected_symptoms: Set[str],
        symptom_implications: Dict[str, List[str]],
        previously_asked: Set[str],
        last_asked_times: Optional[Dict[str, float]] = None,
    ) -> QuestionFeatures:
        """
        Extract all features for a question.

        Args:
            question_id: ID of the question
            question_type: Type (binary, multiselect, numeric)
            question_targets: Diseases this question targets
            target_diseases_per_answer: {answer: [diseases]}
            candidate_diseases: Current candidates
            detected_symptoms: Detected symptoms
            symptom_implications: Symptoms related to this question
            previously_asked: Questions already asked
            last_asked_times: When each question was last asked

        Returns:
            QuestionFeatures with all extracted features
        """
        # Calculate each feature
        coverage = cls.calculate_coverage_score(question_targets, candidate_diseases)
        differentiator = cls.calculate_answer_specificity(question_targets, target_diseases_per_answer)
        specificity = differentiator  # Reuse
        fatigue = cls.calculate_fatigue_penalty(question_id, previously_asked, question_type, last_asked_times)
        alignment = cls.calculate_symptom_alignment(question_id, symptom_implications, detected_symptoms)
        diversity = cls.calculate_category_diversity(question_id, list(previously_asked))

        return QuestionFeatures(
            question_id=question_id,
            differentiator_score=differentiator,
            coverage_score=coverage,
            answer_specificity=specificity,
            fatigue_score=fatigue,
            symptom_alignment_bonus=alignment,
            category_diversity=diversity,
        )


# Import math here to avoid circular dependency
import math
