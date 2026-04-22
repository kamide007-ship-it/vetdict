"""Tests for api/ai/adaptive_question_ranker.py."""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.ai.adaptive_question_ranker import AdaptiveQuestionRanker, RankedQuestion
from api.ai.question_features import QuestionFeatures

# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


def make_question(
    q_id: str,
    targets: List[str],
    q_type: str = "binary",
    answer_types: Optional[Dict[str, List[str]]] = None,
) -> Dict[str, Any]:
    if answer_types is None:
        answer_types = {"yes": targets, "no": []}
    return {
        "id": q_id,
        "type": q_type,
        "targets": targets,
        "answer_types": answer_types,
    }


def make_disease(name: str, match_percent: int) -> Dict[str, Any]:
    return {"name": name, "match_percent": match_percent}


DISEASES = [
    make_disease("Canine Parvovirus", 80),
    make_disease("Pancreatitis", 60),
    make_disease("Kidney Disease (CKD)", 40),
    make_disease("Pneumonia", 30),
]

QUESTIONS = [
    make_question(
        "vomiting_frequency",
        ["Canine Parvovirus", "Pancreatitis", "Gastric Dilatation-Volvulus (GDV/Bloat)"],
        q_type="multiselect",
    ),
    make_question(
        "blood_in_vomit",
        ["Canine Parvovirus", "Hemorrhagic Gastroenteritis (HGE)"],
    ),
    make_question(
        "cough_type",
        ["Pneumonia", "Tracheal Collapse", "Heart Disease/CHF"],
        q_type="multiselect",
    ),
    make_question(
        "fever_present",
        ["Infection", "Meningitis", "Pyometra"],
    ),
]


# ---------------------------------------------------------------------------
# RankedQuestion tests
# ---------------------------------------------------------------------------


class TestRankedQuestion:
    def _make_features(self) -> QuestionFeatures:
        return QuestionFeatures(
            question_id="q1",
            differentiator_score=0.7,
            coverage_score=0.5,
            answer_specificity=0.6,
            fatigue_score=0.2,
            symptom_alignment_bonus=0.4,
            category_diversity=0.8,
        )

    def test_instantiation(self):
        features = self._make_features()
        rq = RankedQuestion(
            question_id="q1",
            rank=1,
            composite_score=0.75,
            information_gain=0.3,
            features=features,
            score_breakdown={"information_gain": 0.3, "coverage": 0.45},
        )
        assert rq.question_id == "q1"
        assert rq.rank == 1
        assert rq.composite_score == pytest.approx(0.75)

    def test_to_dict_structure(self):
        features = self._make_features()
        rq = RankedQuestion(
            question_id="q1",
            rank=2,
            composite_score=0.654321,
            information_gain=0.123456,
            features=features,
            score_breakdown={"x": 0.111111},
        )
        d = rq.to_dict()
        assert d["question_id"] == "q1"
        assert d["rank"] == 2
        assert d["composite_score"] == round(0.654321, 3)
        assert d["information_gain"] == round(0.123456, 3)
        assert "features" in d
        assert "score_breakdown" in d
        # Score breakdown values should be rounded to 3 decimal places
        assert d["score_breakdown"]["x"] == round(0.111111, 3)


# ---------------------------------------------------------------------------
# AdaptiveQuestionRanker.rank_questions (ML path)
# ---------------------------------------------------------------------------


class TestRankQuestionsML:
    def test_returns_list(self):
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=QUESTIONS,
            candidate_diseases=DISEASES,
            detected_symptoms={"vomiting"},
        )
        assert isinstance(result, list)

    def test_ranks_are_sequential(self):
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=QUESTIONS,
            candidate_diseases=DISEASES,
            detected_symptoms={"vomiting"},
        )
        for i, rq in enumerate(result, 1):
            assert rq.rank == i

    def test_sorted_by_score_descending(self):
        # Disable diversity so reordering doesn't break score sort
        original = AdaptiveQuestionRanker.ENABLE_DIVERSITY
        AdaptiveQuestionRanker.ENABLE_DIVERSITY = False
        try:
            result = AdaptiveQuestionRanker.rank_questions(
                questions_with_metadata=QUESTIONS,
                candidate_diseases=DISEASES,
                detected_symptoms={"vomiting"},
            )
        finally:
            AdaptiveQuestionRanker.ENABLE_DIVERSITY = original
        scores = [rq.composite_score for rq in result]
        assert scores == sorted(scores, reverse=True)

    def test_composite_score_in_range(self):
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=QUESTIONS,
            candidate_diseases=DISEASES,
            detected_symptoms={"vomiting"},
        )
        for rq in result:
            assert 0.0 <= rq.composite_score <= 1.0

    def test_skips_questions_without_id(self):
        questions = [{"id": "", "targets": ["Pneumonia"], "type": "binary", "answer_types": {}}]
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=questions,
            candidate_diseases=DISEASES,
            detected_symptoms=set(),
        )
        assert result == []

    def test_skips_questions_without_targets(self):
        questions = [{"id": "q_no_targets", "targets": [], "type": "binary", "answer_types": {}}]
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=questions,
            candidate_diseases=DISEASES,
            detected_symptoms=set(),
        )
        assert result == []

    def test_previously_asked_included(self):
        # Providing previously_asked should not crash; fatigue is applied
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=QUESTIONS,
            candidate_diseases=DISEASES,
            detected_symptoms={"vomiting"},
            previously_asked={"blood_in_vomit"},
        )
        assert isinstance(result, list)

    def test_learned_weights_used(self):
        custom_weights = {
            "information_gain": 0.5,
            "fisher_ratio": 0.2,
            "coverage": 0.15,
            "fatigue": -0.05,
            "alignment": 0.1,
        }
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=QUESTIONS,
            candidate_diseases=DISEASES,
            detected_symptoms=set(),
            learned_weights=custom_weights,
        )
        assert isinstance(result, list)

    def test_empty_questions_returns_empty(self):
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=[],
            candidate_diseases=DISEASES,
            detected_symptoms=set(),
        )
        assert result == []

    def test_empty_diseases_still_returns(self):
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=QUESTIONS,
            candidate_diseases=[],
            detected_symptoms=set(),
        )
        # Questions targeting nothing will have coverage 0 → filtered out
        assert isinstance(result, list)


# ---------------------------------------------------------------------------
# AdaptiveQuestionRanker.rank_questions (simple fallback path)
# ---------------------------------------------------------------------------


class TestRankQuestionsSimple:
    def test_use_ml_false_returns_simple_ranking(self):
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=QUESTIONS,
            candidate_diseases=DISEASES,
            detected_symptoms=set(),
            use_ml=False,
        )
        assert isinstance(result, list)

    def test_simple_ranking_ranks_sequential(self):
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=QUESTIONS,
            candidate_diseases=DISEASES,
            detected_symptoms=set(),
            use_ml=False,
        )
        for i, rq in enumerate(result, 1):
            assert rq.rank == i

    def test_simple_ranking_features_none(self):
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=QUESTIONS,
            candidate_diseases=DISEASES,
            detected_symptoms=set(),
            use_ml=False,
        )
        for rq in result:
            assert rq.features is None
            assert rq.information_gain == 0.0

    def test_simple_ranking_skips_no_id(self):
        questions = [{"id": "", "targets": ["Pancreatitis"], "type": "binary"}]
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=questions,
            candidate_diseases=DISEASES,
            detected_symptoms=set(),
            use_ml=False,
        )
        assert result == []

    def test_simple_ranking_skips_no_targets(self):
        questions = [{"id": "q1", "targets": [], "type": "binary"}]
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=questions,
            candidate_diseases=DISEASES,
            detected_symptoms=set(),
            use_ml=False,
        )
        assert result == []

    def test_simple_ranking_zero_coverage_excluded(self):
        # Question targets disease not in candidates → coverage 0 → excluded
        questions = [
            make_question("q_never_covered", ["NonExistentDisease"]),
        ]
        result = AdaptiveQuestionRanker.rank_questions(
            questions_with_metadata=questions,
            candidate_diseases=DISEASES,
            detected_symptoms=set(),
            use_ml=False,
        )
        assert result == []


# ---------------------------------------------------------------------------
# _apply_diversity_constraint
# ---------------------------------------------------------------------------


class TestApplyDiversityConstraint:
    def _make_rq(self, q_id: str, score: float) -> RankedQuestion:
        features = QuestionFeatures(
            question_id=q_id,
            differentiator_score=0.5,
            coverage_score=0.5,
            answer_specificity=0.5,
            fatigue_score=0.1,
            symptom_alignment_bonus=0.0,
            category_diversity=1.0,
        )
        return RankedQuestion(
            question_id=q_id,
            rank=0,
            composite_score=score,
            information_gain=0.1,
            features=features,
            score_breakdown={},
        )

    def test_small_list_returned_as_is(self):
        questions = [
            self._make_rq("vomiting_frequency", 0.9),
            self._make_rq("blood_in_vomit", 0.8),
        ]
        result = AdaptiveQuestionRanker._apply_diversity_constraint(questions)
        assert len(result) == 2

    def test_exactly_three_returned_as_is(self):
        questions = [
            self._make_rq("vomiting_frequency", 0.9),
            self._make_rq("blood_in_vomit", 0.8),
            self._make_rq("cough_type", 0.7),
        ]
        result = AdaptiveQuestionRanker._apply_diversity_constraint(questions)
        assert len(result) == 3

    def test_longer_list_reordered(self):
        questions = [
            self._make_rq("vomiting_frequency", 0.9),  # gastrointestinal
            self._make_rq("blood_in_vomit", 0.85),  # gastrointestinal
            self._make_rq("diarrhea_consistency", 0.8),  # gastrointestinal
            self._make_rq("cough_type", 0.75),  # respiratory
            self._make_rq("urine_color", 0.7),  # urinary
            self._make_rq("onset_timeline", 0.65),  # systemic
        ]
        result = AdaptiveQuestionRanker._apply_diversity_constraint(questions)
        assert len(result) == len(questions)
        # All original questions are still in result
        original_ids = {q.question_id for q in questions}
        result_ids = {q.question_id for q in result}
        assert original_ids == result_ids


# ---------------------------------------------------------------------------
# _build_symptom_implications
# ---------------------------------------------------------------------------


class TestBuildSymptomImplications:
    def test_returns_dict(self):
        result = AdaptiveQuestionRanker._build_symptom_implications()
        assert isinstance(result, dict)

    def test_known_keys_present(self):
        result = AdaptiveQuestionRanker._build_symptom_implications()
        assert "vomiting_frequency" in result
        assert "fever_present" in result
        assert "vaccine_status" in result

    def test_values_are_lists(self):
        result = AdaptiveQuestionRanker._build_symptom_implications()
        for _key, value in result.items():
            assert isinstance(value, list)

    def test_vaccine_status_empty(self):
        result = AdaptiveQuestionRanker._build_symptom_implications()
        assert result["vaccine_status"] == []


# ---------------------------------------------------------------------------
# update_weights_from_feedback
# ---------------------------------------------------------------------------


class TestUpdateWeightsFromFeedback:
    def test_returns_copy_of_weights(self):
        weights = {"information_gain": 0.4, "coverage": 0.15}
        updated = AdaptiveQuestionRanker.update_weights_from_feedback(weights, {"q1": 0.9})
        assert updated == weights
        # Ensure it's a copy, not the same object
        assert updated is not weights

    def test_does_not_modify_original(self):
        weights = {"information_gain": 0.4}
        original_copy = weights.copy()
        AdaptiveQuestionRanker.update_weights_from_feedback(weights, {})
        assert weights == original_copy
