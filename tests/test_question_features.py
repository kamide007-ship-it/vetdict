"""Tests for api/ai/question_features.py."""

import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Set

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.ai.question_features import QuestionFeatureExtractor, QuestionFeatures


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_disease(name: str, match_percent: int = 50) -> Dict[str, Any]:
    return {"name": name, "match_percent": match_percent}


CANDIDATES = [
    make_disease("Canine Parvovirus", 80),
    make_disease("Pancreatitis", 60),
    make_disease("Kidney Disease (CKD)", 40),
    make_disease("Pneumonia", 30),
]


# ---------------------------------------------------------------------------
# QuestionFeatures dataclass
# ---------------------------------------------------------------------------


class TestQuestionFeatures:
    def _make(self, **overrides) -> QuestionFeatures:
        defaults = dict(
            question_id="q1",
            differentiator_score=0.6,
            coverage_score=0.5,
            answer_specificity=0.4,
            fatigue_score=0.2,
            symptom_alignment_bonus=0.3,
            category_diversity=0.8,
        )
        defaults.update(overrides)
        return QuestionFeatures(**defaults)

    def test_instantiation(self):
        f = self._make()
        assert f.question_id == "q1"
        assert f.coverage_score == pytest.approx(0.5)

    def test_to_dict_keys(self):
        d = self._make().to_dict()
        assert set(d.keys()) == {
            "question_id",
            "differentiator_score",
            "coverage_score",
            "answer_specificity",
            "fatigue_score",
            "symptom_alignment_bonus",
            "category_diversity",
        }

    def test_to_dict_rounding(self):
        f = self._make(differentiator_score=0.123456789)
        d = f.to_dict()
        assert d["differentiator_score"] == round(0.123456789, 3)

    def test_to_dict_values(self):
        f = self._make(question_id="abc", coverage_score=0.75)
        d = f.to_dict()
        assert d["question_id"] == "abc"
        assert d["coverage_score"] == round(0.75, 3)


# ---------------------------------------------------------------------------
# QuestionFeatureExtractor.calculate_coverage_score
# ---------------------------------------------------------------------------


class TestCalculateCoverageScore:
    def test_empty_candidates_returns_zero(self):
        score = QuestionFeatureExtractor.calculate_coverage_score(
            ["Canine Parvovirus"], []
        )
        assert score == 0.0

    def test_empty_targets_returns_zero(self):
        score = QuestionFeatureExtractor.calculate_coverage_score([], CANDIDATES)
        assert score == 0.0

    def test_full_overlap(self):
        targets = [d["name"] for d in CANDIDATES]
        score = QuestionFeatureExtractor.calculate_coverage_score(targets, CANDIDATES)
        assert score == pytest.approx(1.0)

    def test_no_overlap(self):
        score = QuestionFeatureExtractor.calculate_coverage_score(
            ["NonExistentDisease"], CANDIDATES
        )
        assert score == 0.0

    def test_partial_overlap(self):
        targets = ["Canine Parvovirus", "Pancreatitis"]  # 2 of 4
        score = QuestionFeatureExtractor.calculate_coverage_score(targets, CANDIDATES)
        assert score == pytest.approx(0.5)

    def test_candidates_without_name_ignored(self):
        candidates_no_name = [{"match_percent": 50}, make_disease("Canine Parvovirus")]
        score = QuestionFeatureExtractor.calculate_coverage_score(
            ["Canine Parvovirus"], candidates_no_name
        )
        # Only 1 valid candidate; 1 overlaps → 1/1 = 1.0
        assert score == pytest.approx(1.0)


# ---------------------------------------------------------------------------
# QuestionFeatureExtractor.calculate_answer_specificity
# ---------------------------------------------------------------------------


class TestCalculateAnswerSpecificity:
    def test_less_than_two_answers_low_specificity(self):
        score = QuestionFeatureExtractor.calculate_answer_specificity(
            ["DiseaseA"], {"yes": ["DiseaseA"]}
        )
        assert score == pytest.approx(0.1)

    def test_empty_answer_types_low_specificity(self):
        score = QuestionFeatureExtractor.calculate_answer_specificity(
            ["DiseaseA"], {}
        )
        assert score == pytest.approx(0.1)

    def test_equal_distribution_high_gini(self):
        # Two answers each targeting same number of diseases → Gini = 0.5
        score = QuestionFeatureExtractor.calculate_answer_specificity(
            ["DiseaseA", "DiseaseB"],
            {"yes": ["DiseaseA"], "no": ["DiseaseB"]},
        )
        assert 0.0 < score <= 1.0

    def test_skewed_distribution_lower_gini(self):
        # One answer targets 3 diseases, other targets 1 → less uniform
        score_skewed = QuestionFeatureExtractor.calculate_answer_specificity(
            ["DiseaseA", "DiseaseB", "DiseaseC", "DiseaseD"],
            {"yes": ["DiseaseA", "DiseaseB", "DiseaseC"], "no": ["DiseaseD"]},
        )
        score_equal = QuestionFeatureExtractor.calculate_answer_specificity(
            ["DiseaseA", "DiseaseB"],
            {"yes": ["DiseaseA"], "no": ["DiseaseB"]},
        )
        # Equal distribution has higher Gini (more diversity)
        assert score_equal >= score_skewed

    def test_zero_overlap_returns_zero(self):
        # Targets are completely disjoint from answer disease lists
        score = QuestionFeatureExtractor.calculate_answer_specificity(
            ["DiseaseA"],
            {"yes": ["OtherDisease1"], "no": ["OtherDisease2"]},
        )
        assert score == 0.0

    def test_score_in_range(self):
        score = QuestionFeatureExtractor.calculate_answer_specificity(
            ["DiseaseA", "DiseaseB"],
            {"yes": ["DiseaseA"], "no": ["DiseaseB"], "maybe": ["DiseaseA"]},
        )
        assert 0.0 <= score <= 1.0


# ---------------------------------------------------------------------------
# QuestionFeatureExtractor.calculate_fatigue_penalty
# ---------------------------------------------------------------------------


class TestCalculateFatiguePenalty:
    def test_not_asked_only_burden(self):
        # Question never asked → fatigue = 0 + burden * 0.3
        score = QuestionFeatureExtractor.calculate_fatigue_penalty(
            "q1", set(), "binary"
        )
        expected_burden = QuestionFeatureExtractor.QUESTION_TYPE_BURDEN["binary"] * 0.3
        assert score == pytest.approx(expected_burden)

    def test_asked_no_timestamps(self):
        score = QuestionFeatureExtractor.calculate_fatigue_penalty(
            "q1", {"q1"}, "binary"
        )
        # 0.6 for recently asked + 0.2*0.3 for binary burden
        expected = 0.6 + QuestionFeatureExtractor.QUESTION_TYPE_BURDEN["binary"] * 0.3
        assert score == pytest.approx(min(expected, 1.0))

    def test_asked_with_timestamps_recent(self):
        now = time.time()
        score = QuestionFeatureExtractor.calculate_fatigue_penalty(
            "q1", {"q1"}, "binary", last_asked_times={"q1": now}
        )
        # Very recent → high penalty, capped at 1.0
        assert 0.0 < score <= 1.0

    def test_multiselect_higher_burden_than_binary(self):
        binary_score = QuestionFeatureExtractor.calculate_fatigue_penalty(
            "q1", set(), "binary"
        )
        multi_score = QuestionFeatureExtractor.calculate_fatigue_penalty(
            "q1", set(), "multiselect"
        )
        assert multi_score > binary_score

    def test_capped_at_one(self):
        # Previously asked with no timestamp → max fatigue scenario
        score = QuestionFeatureExtractor.calculate_fatigue_penalty(
            "q1", {"q1"}, "numeric"
        )
        assert score <= 1.0

    def test_unknown_type_defaults_to_0_5_burden(self):
        score = QuestionFeatureExtractor.calculate_fatigue_penalty(
            "q1", set(), "unknown_type"
        )
        expected = 0.5 * 0.3
        assert score == pytest.approx(expected)


# ---------------------------------------------------------------------------
# QuestionFeatureExtractor.calculate_symptom_alignment
# ---------------------------------------------------------------------------


class TestCalculateSymptomAlignment:
    IMPLICATIONS = {
        "vomiting_frequency": ["vomiting"],
        "cough_type": ["coughing"],
        "fever_present": ["fever", "lethargy"],
    }

    def test_unknown_question_returns_zero(self):
        score = QuestionFeatureExtractor.calculate_symptom_alignment(
            "unknown_q", self.IMPLICATIONS, {"vomiting"}
        )
        assert score == 0.0

    def test_empty_related_symptoms_returns_zero(self):
        implications = {"vaccine_status": []}
        score = QuestionFeatureExtractor.calculate_symptom_alignment(
            "vaccine_status", implications, {"fever"}
        )
        assert score == 0.0

    def test_full_overlap_returns_one(self):
        score = QuestionFeatureExtractor.calculate_symptom_alignment(
            "vomiting_frequency", self.IMPLICATIONS, {"vomiting"}
        )
        assert score == pytest.approx(1.0)

    def test_partial_overlap(self):
        # fever_present relates to fever and lethargy; only fever detected
        score = QuestionFeatureExtractor.calculate_symptom_alignment(
            "fever_present", self.IMPLICATIONS, {"fever"}
        )
        assert score == pytest.approx(0.5)

    def test_no_overlap_returns_zero(self):
        score = QuestionFeatureExtractor.calculate_symptom_alignment(
            "cough_type", self.IMPLICATIONS, {"vomiting"}
        )
        assert score == 0.0

    def test_score_range(self):
        score = QuestionFeatureExtractor.calculate_symptom_alignment(
            "fever_present", self.IMPLICATIONS, {"fever", "lethargy"}
        )
        assert 0.0 <= score <= 1.0


# ---------------------------------------------------------------------------
# QuestionFeatureExtractor.calculate_category_diversity
# ---------------------------------------------------------------------------


class TestCalculateCategoryDiversity:
    def test_not_asked_returns_one(self):
        score = QuestionFeatureExtractor.calculate_category_diversity(
            "vomiting_frequency", []
        )
        assert score == pytest.approx(1.0)

    def test_different_category_asked_returns_one(self):
        # Asked cough_type (respiratory), asking vomiting_frequency (gastrointestinal)
        score = QuestionFeatureExtractor.calculate_category_diversity(
            "vomiting_frequency", ["cough_type"]
        )
        assert score == pytest.approx(1.0)

    def test_same_category_reduces_diversity(self):
        # blood_in_vomit is also gastrointestinal
        score = QuestionFeatureExtractor.calculate_category_diversity(
            "vomiting_frequency", ["blood_in_vomit"]
        )
        assert score < 1.0

    def test_diversity_decreases_with_more_same_category(self):
        score_one = QuestionFeatureExtractor.calculate_category_diversity(
            "vomiting_frequency", ["blood_in_vomit"]
        )
        score_two = QuestionFeatureExtractor.calculate_category_diversity(
            "vomiting_frequency", ["blood_in_vomit", "diarrhea_consistency"]
        )
        assert score_two < score_one

    def test_unknown_question_category_other(self):
        score = QuestionFeatureExtractor.calculate_category_diversity(
            "unknown_question", []
        )
        assert score == pytest.approx(1.0)

    def test_score_range(self):
        asked = ["blood_in_vomit", "diarrhea_consistency", "vomiting_frequency"]
        score = QuestionFeatureExtractor.calculate_category_diversity(
            "vomiting_frequency", asked
        )
        assert 0.0 < score <= 1.0


# ---------------------------------------------------------------------------
# QuestionFeatureExtractor.extract_features
# ---------------------------------------------------------------------------


class TestExtractFeatures:
    IMPLICATIONS = {
        "vomiting_frequency": ["vomiting"],
        "blood_in_vomit": ["vomiting", "bloody_stool"],
    }

    def test_returns_question_features(self):
        result = QuestionFeatureExtractor.extract_features(
            question_id="vomiting_frequency",
            question_type="multiselect",
            question_targets=["Canine Parvovirus", "Pancreatitis"],
            target_diseases_per_answer={"once": ["Canine Parvovirus"], "frequent": ["Pancreatitis"]},
            candidate_diseases=CANDIDATES,
            detected_symptoms={"vomiting"},
            symptom_implications=self.IMPLICATIONS,
            previously_asked=set(),
        )
        assert isinstance(result, QuestionFeatures)
        assert result.question_id == "vomiting_frequency"

    def test_coverage_score_computed(self):
        result = QuestionFeatureExtractor.extract_features(
            question_id="vomiting_frequency",
            question_type="binary",
            question_targets=["Canine Parvovirus", "Pancreatitis"],
            target_diseases_per_answer={},
            candidate_diseases=CANDIDATES,
            detected_symptoms=set(),
            symptom_implications=self.IMPLICATIONS,
            previously_asked=set(),
        )
        # 2 of 4 candidates are targeted → coverage = 0.5
        assert result.coverage_score == pytest.approx(0.5)

    def test_fatigue_with_previously_asked(self):
        result = QuestionFeatureExtractor.extract_features(
            question_id="vomiting_frequency",
            question_type="binary",
            question_targets=["Canine Parvovirus"],
            target_diseases_per_answer={},
            candidate_diseases=CANDIDATES,
            detected_symptoms=set(),
            symptom_implications=self.IMPLICATIONS,
            previously_asked={"vomiting_frequency"},
        )
        # fatigue should be higher because question was previously asked
        binary_burden = QuestionFeatureExtractor.QUESTION_TYPE_BURDEN["binary"] * 0.3
        assert result.fatigue_score > binary_burden

    def test_symptom_alignment_bonus(self):
        result = QuestionFeatureExtractor.extract_features(
            question_id="vomiting_frequency",
            question_type="binary",
            question_targets=[],
            target_diseases_per_answer={},
            candidate_diseases=CANDIDATES,
            detected_symptoms={"vomiting"},
            symptom_implications=self.IMPLICATIONS,
            previously_asked=set(),
        )
        assert result.symptom_alignment_bonus == pytest.approx(1.0)

    def test_last_asked_times_accepted(self):
        result = QuestionFeatureExtractor.extract_features(
            question_id="vomiting_frequency",
            question_type="binary",
            question_targets=["Canine Parvovirus"],
            target_diseases_per_answer={},
            candidate_diseases=CANDIDATES,
            detected_symptoms=set(),
            symptom_implications=self.IMPLICATIONS,
            previously_asked={"vomiting_frequency"},
            last_asked_times={"vomiting_frequency": time.time()},
        )
        assert isinstance(result, QuestionFeatures)

    def test_all_feature_fields_present(self):
        result = QuestionFeatureExtractor.extract_features(
            question_id="cough_type",
            question_type="multiselect",
            question_targets=["Pneumonia"],
            target_diseases_per_answer={"dry": ["Pneumonia"], "wet": ["Pneumonia"]},
            candidate_diseases=CANDIDATES,
            detected_symptoms={"coughing"},
            symptom_implications={"cough_type": ["coughing"]},
            previously_asked=set(),
        )
        assert hasattr(result, "differentiator_score")
        assert hasattr(result, "coverage_score")
        assert hasattr(result, "answer_specificity")
        assert hasattr(result, "fatigue_score")
        assert hasattr(result, "symptom_alignment_bonus")
        assert hasattr(result, "category_diversity")


# ---------------------------------------------------------------------------
# QUESTION_CATEGORIES and QUESTION_TYPE_BURDEN constants
# ---------------------------------------------------------------------------


class TestConstants:
    def test_question_categories_non_empty(self):
        assert len(QuestionFeatureExtractor.QUESTION_CATEGORIES) > 0

    def test_binary_lowest_burden(self):
        assert (
            QuestionFeatureExtractor.QUESTION_TYPE_BURDEN["binary"]
            < QuestionFeatureExtractor.QUESTION_TYPE_BURDEN["multiselect"]
        )

    def test_known_categories_present(self):
        cats = QuestionFeatureExtractor.QUESTION_CATEGORIES
        assert "vomiting_frequency" in cats
        assert "cough_type" in cats
        assert cats["vomiting_frequency"] == "gastrointestinal"
        assert cats["cough_type"] == "respiratory"
