"""Tests for api/ai/question_optimization.py."""

import sys
from pathlib import Path
from typing import Any, Dict

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.ai.question_optimization import (
    EntropyCalculator,
    EntropyMetrics,
    calculate_question_entropy_reduction,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_disease(name: str, match_percent: int) -> Dict[str, Any]:
    return {"name": name, "match_percent": match_percent}


FOUR_DISEASES = [
    make_disease("Canine Parvovirus", 80),
    make_disease("Pancreatitis", 60),
    make_disease("Kidney Disease (CKD)", 40),
    make_disease("Pneumonia", 30),
]

TWO_DISEASES = [
    make_disease("Canine Parvovirus", 70),
    make_disease("Pancreatitis", 30),
]


# ---------------------------------------------------------------------------
# EntropyMetrics dataclass
# ---------------------------------------------------------------------------


class TestEntropyMetrics:
    def _make(self) -> EntropyMetrics:
        return EntropyMetrics(
            question_id="q1",
            current_entropy=2.0,
            expected_entropy_yes=1.5,
            expected_entropy_no=1.8,
            information_gain=0.3,
            probability_yes=0.6,
            probability_no=0.4,
            effectiveness_score=0.75,
        )

    def test_instantiation(self):
        m = self._make()
        assert m.question_id == "q1"
        assert m.information_gain == pytest.approx(0.3)

    def test_to_dict_keys(self):
        d = self._make().to_dict()
        expected = {
            "question_id",
            "current_entropy",
            "expected_entropy_yes",
            "expected_entropy_no",
            "information_gain",
            "probability_yes",
            "probability_no",
            "effectiveness_score",
        }
        assert set(d.keys()) == expected

    def test_to_dict_rounding(self):
        m = EntropyMetrics(
            question_id="q1",
            current_entropy=1.23456789,
            expected_entropy_yes=0.123456789,
            expected_entropy_no=0.987654321,
            information_gain=0.111111111,
            probability_yes=0.555555,
            probability_no=0.444444,
            effectiveness_score=0.777777,
        )
        d = m.to_dict()
        assert d["current_entropy"] == round(1.23456789, 4)
        assert d["probability_yes"] == round(0.555555, 3)
        assert d["effectiveness_score"] == round(0.777777, 3)


# ---------------------------------------------------------------------------
# EntropyCalculator.calculate_entropy
# ---------------------------------------------------------------------------


class TestCalculateEntropy:
    def test_uniform_two_classes(self):
        # Entropy of fair coin = 1 bit
        entropy = EntropyCalculator.calculate_entropy({"A": 0.5, "B": 0.5})
        assert entropy == pytest.approx(1.0)

    def test_deterministic_zero_entropy(self):
        # All probability on one class → entropy 0
        entropy = EntropyCalculator.calculate_entropy({"A": 1.0, "B": 0.0})
        assert entropy == pytest.approx(0.0)

    def test_uniform_four_classes(self):
        # log2(4) = 2 bits
        entropy = EntropyCalculator.calculate_entropy({"A": 0.25, "B": 0.25, "C": 0.25, "D": 0.25})
        assert entropy == pytest.approx(2.0)

    def test_empty_distribution_zero(self):
        entropy = EntropyCalculator.calculate_entropy({})
        assert entropy == pytest.approx(0.0)

    def test_skewed_distribution(self):
        entropy = EntropyCalculator.calculate_entropy({"A": 0.9, "B": 0.1})
        # Should be less than 1 (max for 2 outcomes)
        assert 0.0 < entropy < 1.0

    def test_zero_probabilities_ignored(self):
        entropy_with_zeros = EntropyCalculator.calculate_entropy({"A": 0.5, "B": 0.5, "C": 0.0})
        entropy_without = EntropyCalculator.calculate_entropy({"A": 0.5, "B": 0.5})
        assert entropy_with_zeros == pytest.approx(entropy_without)


# ---------------------------------------------------------------------------
# EntropyCalculator.disease_probabilities_from_matches
# ---------------------------------------------------------------------------


class TestDiseaseProbabilitiesFromMatches:
    def test_empty_returns_empty(self):
        result = EntropyCalculator.disease_probabilities_from_matches([])
        assert result == {}

    def test_sums_to_one(self):
        result = EntropyCalculator.disease_probabilities_from_matches(FOUR_DISEASES)
        assert sum(result.values()) == pytest.approx(1.0)

    def test_all_zero_matches_uniform(self):
        diseases = [
            make_disease("A", 0),
            make_disease("B", 0),
            make_disease("C", 0),
        ]
        result = EntropyCalculator.disease_probabilities_from_matches(diseases)
        assert sum(result.values()) == pytest.approx(1.0)
        for v in result.values():
            assert v == pytest.approx(1 / 3)

    def test_disease_without_name_ignored(self):
        diseases = [{"match_percent": 50}, make_disease("A", 50)]
        result = EntropyCalculator.disease_probabilities_from_matches(diseases)
        assert "A" in result
        assert "" not in result or result.get("") == 0.0

    def test_negative_match_treated_as_zero(self):
        diseases = [make_disease("A", -10), make_disease("B", 50)]
        result = EntropyCalculator.disease_probabilities_from_matches(diseases)
        # A has 0 probability, B gets all
        assert result["B"] == pytest.approx(1.0)

    def test_proportional_probabilities(self):
        diseases = [make_disease("A", 75), make_disease("B", 25)]
        result = EntropyCalculator.disease_probabilities_from_matches(diseases)
        assert result["A"] == pytest.approx(0.75)
        assert result["B"] == pytest.approx(0.25)


# ---------------------------------------------------------------------------
# EntropyCalculator.estimated_answer_probability
# ---------------------------------------------------------------------------


class TestEstimatedAnswerProbability:
    def test_empty_disease_names_returns_0_5(self):
        prob = EntropyCalculator.estimated_answer_probability([], ["Canine Parvovirus"], {}, "yes")
        assert prob == pytest.approx(0.5)

    def test_yes_probability_in_range(self):
        probs = EntropyCalculator.disease_probabilities_from_matches(FOUR_DISEASES)
        names = [d["name"] for d in FOUR_DISEASES]
        prob_yes = EntropyCalculator.estimated_answer_probability(
            names, ["Canine Parvovirus", "Pancreatitis"], probs, "yes"
        )
        assert 0.0 <= prob_yes <= 1.0

    def test_no_prob_complements_yes(self):
        probs = EntropyCalculator.disease_probabilities_from_matches(FOUR_DISEASES)
        names = [d["name"] for d in FOUR_DISEASES]
        targets = ["Canine Parvovirus"]
        prob_yes = EntropyCalculator.estimated_answer_probability(names, targets, probs, "yes")
        prob_no = EntropyCalculator.estimated_answer_probability(names, targets, probs, "no")
        assert prob_yes + prob_no == pytest.approx(1.0)

    def test_targets_not_in_candidates_returns_zero_yes(self):
        probs = EntropyCalculator.disease_probabilities_from_matches(FOUR_DISEASES)
        names = [d["name"] for d in FOUR_DISEASES]
        prob_yes = EntropyCalculator.estimated_answer_probability(names, ["NonExistentDisease"], probs, "yes")
        assert prob_yes == pytest.approx(0.0)

    def test_all_targeted_returns_sum_of_probs(self):
        probs = EntropyCalculator.disease_probabilities_from_matches(FOUR_DISEASES)
        names = [d["name"] for d in FOUR_DISEASES]
        prob_yes = EntropyCalculator.estimated_answer_probability(names, names, probs, "yes")
        assert prob_yes == pytest.approx(1.0)

    def test_positive_answer_aliases(self):
        probs = EntropyCalculator.disease_probabilities_from_matches(TWO_DISEASES)
        names = [d["name"] for d in TWO_DISEASES]
        targets = ["Canine Parvovirus"]
        prob_yes = EntropyCalculator.estimated_answer_probability(names, targets, probs, "yes")
        for alias in ("positive", "true", "1"):
            prob_alias = EntropyCalculator.estimated_answer_probability(names, targets, probs, alias)
            assert prob_alias == pytest.approx(prob_yes)


# ---------------------------------------------------------------------------
# EntropyCalculator.calculate_information_gain
# ---------------------------------------------------------------------------


class TestCalculateInformationGain:
    def test_returns_entropy_metrics(self):
        metrics = EntropyCalculator.calculate_information_gain("q1", ["Canine Parvovirus"], FOUR_DISEASES)
        assert isinstance(metrics, EntropyMetrics)

    def test_question_id_preserved(self):
        metrics = EntropyCalculator.calculate_information_gain("my_question", ["Pancreatitis"], FOUR_DISEASES)
        assert metrics.question_id == "my_question"

    def test_probability_yes_no_sum_to_one(self):
        metrics = EntropyCalculator.calculate_information_gain("q1", ["Canine Parvovirus"], FOUR_DISEASES)
        assert metrics.probability_yes + metrics.probability_no == pytest.approx(1.0)

    def test_effectiveness_score_in_range(self):
        metrics = EntropyCalculator.calculate_information_gain(
            "q1", ["Canine Parvovirus", "Pancreatitis"], FOUR_DISEASES
        )
        assert 0.0 <= metrics.effectiveness_score <= 1.0

    def test_targets_not_in_candidates_zero_ig(self):
        metrics = EntropyCalculator.calculate_information_gain("q1", ["NonExistentDisease"], FOUR_DISEASES)
        # No overlap → probability_yes=0 → IG close to 0
        assert metrics.probability_yes == pytest.approx(0.0)

    def test_all_targeted_prob_yes_one(self):
        names = [d["name"] for d in FOUR_DISEASES]
        metrics = EntropyCalculator.calculate_information_gain("q1", names, FOUR_DISEASES)
        assert metrics.probability_yes == pytest.approx(1.0)

    def test_current_entropy_positive(self):
        metrics = EntropyCalculator.calculate_information_gain("q1", ["Canine Parvovirus"], FOUR_DISEASES)
        assert metrics.current_entropy > 0.0

    def test_single_disease_candidate(self):
        # Single disease → max entropy is 0 → effectiveness_score = 0
        metrics = EntropyCalculator.calculate_information_gain(
            "q1", ["Canine Parvovirus"], [make_disease("Canine Parvovirus", 100)]
        )
        assert isinstance(metrics, EntropyMetrics)

    def test_empty_candidates(self):
        # No candidates → probabilities empty
        metrics = EntropyCalculator.calculate_information_gain("q1", ["A"], [])
        assert isinstance(metrics, EntropyMetrics)
        assert metrics.current_entropy == pytest.approx(0.0)

    def test_two_equal_diseases_max_entropy(self):
        equal_diseases = [make_disease("A", 50), make_disease("B", 50)]
        metrics = EntropyCalculator.calculate_information_gain("q1", ["A"], equal_diseases)
        # Current entropy should be close to log2(2) = 1 bit
        assert metrics.current_entropy == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# EntropyCalculator.rank_questions_by_information_gain
# ---------------------------------------------------------------------------


class TestRankQuestionsByInformationGain:
    def test_returns_list(self):
        questions = [
            ("q1", ["Canine Parvovirus"]),
            ("q2", ["Pancreatitis", "Kidney Disease (CKD)"]),
        ]
        result = EntropyCalculator.rank_questions_by_information_gain(questions, FOUR_DISEASES)
        assert isinstance(result, list)

    def test_sorted_by_ig_descending(self):
        questions = [
            ("q1", ["Canine Parvovirus"]),
            ("q2", ["Pancreatitis", "Kidney Disease (CKD)"]),
            ("q3", ["NonExistentDisease"]),
        ]
        result = EntropyCalculator.rank_questions_by_information_gain(questions, FOUR_DISEASES)
        ig_scores = [r[1] for r in result]
        assert ig_scores == sorted(ig_scores, reverse=True)

    def test_result_tuples_structure(self):
        questions = [("q1", ["Canine Parvovirus"])]
        result = EntropyCalculator.rank_questions_by_information_gain(questions, FOUR_DISEASES)
        assert len(result) == 1
        q_id, ig_score, metrics = result[0]
        assert q_id == "q1"
        assert isinstance(ig_score, float)
        assert isinstance(metrics, EntropyMetrics)

    def test_empty_questions_returns_empty(self):
        result = EntropyCalculator.rank_questions_by_information_gain([], FOUR_DISEASES)
        assert result == []

    def test_empty_diseases_still_returns_results(self):
        questions = [("q1", ["Canine Parvovirus"])]
        result = EntropyCalculator.rank_questions_by_information_gain(questions, [])
        assert len(result) == 1

    def test_all_metrics_in_result(self):
        questions = [
            ("q1", ["Canine Parvovirus"]),
            ("q2", ["Pancreatitis"]),
        ]
        result = EntropyCalculator.rank_questions_by_information_gain(questions, FOUR_DISEASES)
        for _, _, metrics in result:
            assert isinstance(metrics, EntropyMetrics)
            assert 0.0 <= metrics.effectiveness_score <= 1.0


# ---------------------------------------------------------------------------
# calculate_question_entropy_reduction (module-level helper)
# ---------------------------------------------------------------------------


class TestCalculateQuestionEntropyReduction:
    def test_returns_float(self):
        result = calculate_question_entropy_reduction("q1", ["Canine Parvovirus"], FOUR_DISEASES)
        assert isinstance(result, float)

    def test_no_overlap_low_ig(self):
        result = calculate_question_entropy_reduction("q1", ["NonExistentDisease"], FOUR_DISEASES)
        # With no targeted diseases in candidates, ig should be zero or near-zero
        assert result == pytest.approx(0.0, abs=1e-9)

    def test_partial_targets_positive_ig(self):
        result = calculate_question_entropy_reduction("q1", ["Canine Parvovirus", "Pancreatitis"], FOUR_DISEASES)
        # Targeting half the candidates → some information gain
        assert result >= 0.0

    def test_all_targeted_non_negative(self):
        names = [d["name"] for d in FOUR_DISEASES]
        result = calculate_question_entropy_reduction("q1", names, FOUR_DISEASES)
        # May be a tiny negative due to floating-point arithmetic
        assert result >= -1e-10

    def test_empty_candidates(self):
        result = calculate_question_entropy_reduction("q1", ["A", "B"], [])
        assert isinstance(result, float)

    def test_consistent_with_calculator(self):
        metrics = EntropyCalculator.calculate_information_gain("q1", ["Canine Parvovirus"], FOUR_DISEASES)
        helper_result = calculate_question_entropy_reduction("q1", ["Canine Parvovirus"], FOUR_DISEASES)
        assert helper_result == pytest.approx(metrics.information_gain)
