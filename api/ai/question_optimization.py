"""Question optimization using information theory for intelligent question selection.

Implements information-theoretic approach to calculate question utility
based on entropy reduction. This enables efficient differential diagnosis
through adaptive questioning.
"""

import logging
import math
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


@dataclass
class EntropyMetrics:
    """Entropy and information gain metrics for a question."""

    question_id: str
    current_entropy: float  # Entropy of disease distribution before question
    expected_entropy_yes: float  # Expected entropy if answer is "yes"
    expected_entropy_no: float  # Expected entropy if answer is "no"
    information_gain: float  # Information gain (entropy reduction)
    probability_yes: float  # P(answer="yes" | current_candidates)
    probability_no: float  # P(answer="no" | current_candidates)
    effectiveness_score: float  # Normalized IG score (0-1)

    def to_dict(self):
        return {
            "question_id": self.question_id,
            "current_entropy": round(self.current_entropy, 4),
            "expected_entropy_yes": round(self.expected_entropy_yes, 4),
            "expected_entropy_no": round(self.expected_entropy_no, 4),
            "information_gain": round(self.information_gain, 4),
            "probability_yes": round(self.probability_yes, 3),
            "probability_no": round(self.probability_no, 3),
            "effectiveness_score": round(self.effectiveness_score, 3),
        }


class EntropyCalculator:
    """Calculates entropy and information gain for disease distributions."""

    @staticmethod
    def calculate_entropy(probabilities: Dict[str, float]) -> float:
        """
        Calculate Shannon entropy of a probability distribution.

        Args:
            probabilities: {disease_name: probability} dict (should sum to ~1.0)

        Returns:
            Entropy in bits
        """
        entropy = 0.0
        for prob in probabilities.values():
            if prob > 0:
                entropy -= prob * math.log2(prob)
        return entropy

    @staticmethod
    def disease_probabilities_from_matches(
        diseases_with_matches: List[Dict[str, Any]],
    ) -> Dict[str, float]:
        """
        Convert disease match percentages to probability distribution.

        Args:
            diseases_with_matches: List of {name, match_percent, ...} dicts

        Returns:
            {disease_name: probability} dict (sum = 1.0)
        """
        if not diseases_with_matches:
            return {}

        # Extract match percentages
        match_dict = {
            d.get("name", ""): max(0, d.get("match_percent", 0)) for d in diseases_with_matches if d.get("name")
        }

        # Normalize to probabilities
        total = sum(match_dict.values())
        if total == 0:
            # Uniform distribution if all matches are 0
            n = len(match_dict)
            return {name: 1.0 / n for name in match_dict} if n > 0 else {}

        return {name: score / total for name, score in match_dict.items()}

    @staticmethod
    def estimated_answer_probability(
        disease_names: List[str],
        question_targets: List[str],
        prior_probabilities: Dict[str, float],
        answer_value: str = "yes",
    ) -> float:
        """
        Estimate P(answer=value | disease_set, question).

        Simplified model:
        - P("yes") = |diseases_targeted ∩ disease_set| / |disease_set|
        - P("no") = 1 - P("yes")

        Args:
            disease_names: Current candidate diseases
            question_targets: Diseases this question targets
            prior_probabilities: {disease: prob} for current set
            answer_value: "yes" or "no"

        Returns:
            Estimated probability
        """
        if not disease_names:
            return 0.5

        # Count how many candidates are targeted by this question
        target_set = set(question_targets)
        disease_set = set(disease_names)
        overlap = target_set & disease_set

        # Probability is weighted by disease probabilities
        overlap_prob = sum(prior_probabilities.get(d, 0) for d in overlap if d in disease_set)

        if answer_value.lower() in ("yes", "positive", "true", "1"):
            return overlap_prob
        else:  # "no"
            return 1.0 - overlap_prob

    @classmethod
    def calculate_information_gain(
        cls,
        question_id: str,
        question_targets: List[str],
        current_diseases: List[Dict[str, Any]],
    ) -> EntropyMetrics:
        """
        Calculate information gain (entropy reduction) for a question.

        Args:
            question_id: ID of the question
            question_targets: Disease names this question targets
            current_diseases: Current disease candidates with match_percent

        Returns:
            EntropyMetrics with IG calculation
        """
        # Calculate current entropy (before asking question)
        current_probs = cls.disease_probabilities_from_matches(current_diseases)
        current_entropy = cls.calculate_entropy(current_probs)

        # Estimate probabilities
        disease_names = [d.get("name", "") for d in current_diseases if d.get("name")]

        prob_yes = cls.estimated_answer_probability(disease_names, question_targets, current_probs, answer_value="yes")
        prob_no = 1.0 - prob_yes

        # Estimate entropy after positive answer
        # If answer is "yes", boost probability of targeted diseases
        if prob_yes > 0:
            boosted_probs_yes = {}
            for disease in disease_names:
                if disease in question_targets:
                    # Targeted diseases become more likely
                    boosted_probs_yes[disease] = current_probs.get(disease, 0) * 1.5
                else:
                    boosted_probs_yes[disease] = current_probs.get(disease, 0) * 0.7

            # Normalize
            total_yes = sum(boosted_probs_yes.values())
            if total_yes > 0:
                boosted_probs_yes = {k: v / total_yes for k, v in boosted_probs_yes.items()}
            expected_entropy_yes = cls.calculate_entropy(boosted_probs_yes)
        else:
            expected_entropy_yes = current_entropy

        # Estimate entropy after negative answer
        if prob_no > 0:
            boosted_probs_no = {}
            for disease in disease_names:
                if disease in question_targets:
                    # Targeted diseases become less likely
                    boosted_probs_no[disease] = current_probs.get(disease, 0) * 0.5
                else:
                    boosted_probs_no[disease] = current_probs.get(disease, 0) * 1.2

            # Normalize
            total_no = sum(boosted_probs_no.values())
            if total_no > 0:
                boosted_probs_no = {k: v / total_no for k, v in boosted_probs_no.items()}
            expected_entropy_no = cls.calculate_entropy(boosted_probs_no)
        else:
            expected_entropy_no = current_entropy

        # Calculate expected entropy after question
        expected_entropy = prob_yes * expected_entropy_yes + prob_no * expected_entropy_no

        # Information gain = entropy reduction
        information_gain = current_entropy - expected_entropy

        # Normalize IG to 0-1 scale (max entropy for N items is log2(N))
        max_entropy = math.log2(len(disease_names)) if len(disease_names) > 1 else 1.0
        effectiveness_score = information_gain / max_entropy if max_entropy > 0 else 0.0
        effectiveness_score = max(0.0, min(effectiveness_score, 1.0))  # Clamp to [0,1]

        return EntropyMetrics(
            question_id=question_id,
            current_entropy=current_entropy,
            expected_entropy_yes=expected_entropy_yes,
            expected_entropy_no=expected_entropy_no,
            information_gain=information_gain,
            probability_yes=prob_yes,
            probability_no=prob_no,
            effectiveness_score=effectiveness_score,
        )

    @classmethod
    def rank_questions_by_information_gain(
        cls,
        questions_with_targets: List[Tuple[str, List[str]]],
        current_diseases: List[Dict[str, Any]],
    ) -> List[Tuple[str, float, EntropyMetrics]]:
        """
        Rank questions by information gain.

        Args:
            questions_with_targets: List of (question_id, [target_diseases])
            current_diseases: Current disease candidates

        Returns:
            List of (question_id, ig_score, metrics) sorted by IG descending
        """
        results = []

        for question_id, targets in questions_with_targets:
            metrics = cls.calculate_information_gain(question_id, targets, current_diseases)
            results.append((question_id, metrics.information_gain, metrics))

        # Sort by information gain (descending)
        results.sort(key=lambda x: x[1], reverse=True)

        return results


def calculate_question_entropy_reduction(
    question_id: str,
    question_targets: List[str],
    suspected_diseases: List[Dict[str, Any]],
) -> float:
    """
    Helper function to calculate information gain for a single question.

    Args:
        question_id: ID of the question
        question_targets: Diseases this question targets
        suspected_diseases: Current disease candidates

    Returns:
        Information gain (entropy reduction) score
    """
    metrics = EntropyCalculator.calculate_information_gain(question_id, question_targets, suspected_diseases)
    return metrics.information_gain
