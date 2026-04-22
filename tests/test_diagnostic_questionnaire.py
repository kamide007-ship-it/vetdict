"""Tests for api/ai/diagnostic_questionnaire.py."""

import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.ai.diagnostic_questionnaire import (
    DiagnosticQuestion,
    DiagnosticQuestionnaireEngine,
    build_next_question_response,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_disease(name: str, match_percent: int) -> Dict[str, Any]:
    return {"name": name, "match_percent": match_percent}


MANY_DISEASES = [
    make_disease("Canine Parvovirus", 80),
    make_disease("Pancreatitis", 60),
    make_disease("Kidney Disease (CKD)", 40),
    make_disease("Pneumonia", 30),
    make_disease("Bladder Stones", 25),
]

FEW_DISEASES = [
    make_disease("Canine Parvovirus", 80),
    make_disease("Pancreatitis", 60),
]


# ---------------------------------------------------------------------------
# DiagnosticQuestion dataclass
# ---------------------------------------------------------------------------


class TestDiagnosticQuestion:
    def test_instantiation(self):
        q = DiagnosticQuestion(
            id="blood_in_vomit",
            question_ja="嘔吐物に血液が含まれていますか？",
            question_en="Is there blood in the vomit?",
            question_type="binary",
            priority=75,
            options=[{"value": "yes", "label_ja": "はい", "label_en": "Yes"}],
            disease_targets=["Canine Parvovirus"],
            reasoning_ja="理由",
            reasoning_en="Reason",
        )
        assert q.id == "blood_in_vomit"
        assert q.question_type == "binary"
        assert q.priority == 75
        assert len(q.options) == 1


# ---------------------------------------------------------------------------
# DiagnosticQuestionnaireEngine.generate_questions
# ---------------------------------------------------------------------------


class TestGenerateQuestions:
    def test_empty_diseases_returns_empty(self):
        result = DiagnosticQuestionnaireEngine.generate_questions([], [])
        assert result == []

    def test_single_disease_returns_empty(self):
        result = DiagnosticQuestionnaireEngine.generate_questions([make_disease("Pancreatitis", 80)], [])
        assert result == []

    def test_returns_list_of_diagnostic_questions(self):
        result = DiagnosticQuestionnaireEngine.generate_questions(MANY_DISEASES, ["vomiting"], limit=3)
        assert isinstance(result, list)
        for q in result:
            assert isinstance(q, DiagnosticQuestion)

    def test_respects_limit(self):
        result = DiagnosticQuestionnaireEngine.generate_questions(MANY_DISEASES, ["vomiting"], limit=2)
        assert len(result) <= 2

    def test_default_limit_three(self):
        result = DiagnosticQuestionnaireEngine.generate_questions(MANY_DISEASES, ["vomiting"])
        assert len(result) <= 3

    def test_ml_path_with_two_diseases(self):
        result = DiagnosticQuestionnaireEngine.generate_questions(FEW_DISEASES, ["vomiting"], use_ml=True)
        assert isinstance(result, list)

    def test_traditional_path_with_two_diseases(self):
        result = DiagnosticQuestionnaireEngine.generate_questions(FEW_DISEASES, ["vomiting"], use_ml=False)
        assert isinstance(result, list)

    def test_use_ml_false_uses_traditional(self):
        result = DiagnosticQuestionnaireEngine.generate_questions(MANY_DISEASES, [], use_ml=False, limit=3)
        for q in result:
            assert isinstance(q, DiagnosticQuestion)
            assert q.id in DiagnosticQuestionnaireEngine.QUESTION_TEMPLATES

    def test_previously_asked_parameter_accepted(self):
        result = DiagnosticQuestionnaireEngine.generate_questions(
            MANY_DISEASES,
            ["vomiting"],
            use_ml=True,
            previously_asked={"blood_in_vomit"},
        )
        assert isinstance(result, list)

    def test_limit_zero_returns_empty_or_limited(self):
        result = DiagnosticQuestionnaireEngine.generate_questions(MANY_DISEASES, [], limit=0)
        assert len(result) == 0


# ---------------------------------------------------------------------------
# DiagnosticQuestionnaireEngine._generate_questions_traditional
# ---------------------------------------------------------------------------


class TestGenerateQuestionsTraditional:
    def test_returns_diagnostic_questions(self):
        questions = DiagnosticQuestionnaireEngine._generate_questions_traditional(MANY_DISEASES, limit=3)
        assert isinstance(questions, list)
        for q in questions:
            assert isinstance(q, DiagnosticQuestion)

    def test_question_fields_populated(self):
        questions = DiagnosticQuestionnaireEngine._generate_questions_traditional(MANY_DISEASES, limit=3)
        for q in questions:
            assert q.id
            assert q.question_ja
            assert q.question_en
            assert q.question_type in ("binary", "multiselect", "numeric")
            assert isinstance(q.options, list)
            assert isinstance(q.disease_targets, list)
            assert q.reasoning_ja
            assert q.reasoning_en

    def test_limit_respected(self):
        questions = DiagnosticQuestionnaireEngine._generate_questions_traditional(MANY_DISEASES, limit=1)
        assert len(questions) <= 1

    def test_no_match_diseases_returns_fewer_or_zero(self):
        # Diseases that no template targets
        diseases = [make_disease("RareAlienDisease", 100), make_disease("AnotherAlienDisease", 50)]
        questions = DiagnosticQuestionnaireEngine._generate_questions_traditional(diseases, limit=3)
        # No question should match → empty list
        assert questions == []

    def test_partial_match_returns_questions(self):
        # At least "Canine Parvovirus" is in many templates
        diseases = [
            make_disease("Canine Parvovirus", 80),
            make_disease("XAlienDisease", 50),
        ]
        questions = DiagnosticQuestionnaireEngine._generate_questions_traditional(diseases, limit=3)
        assert len(questions) > 0

    def test_sorted_by_priority_descending(self):
        questions = DiagnosticQuestionnaireEngine._generate_questions_traditional(MANY_DISEASES, limit=5)
        priorities = [q.priority for q in questions]
        assert priorities == sorted(priorities, reverse=True)


# ---------------------------------------------------------------------------
# DiagnosticQuestionnaireEngine._generate_questions_ml
# ---------------------------------------------------------------------------


class TestGenerateQuestionsML:
    def test_returns_list(self):
        questions = DiagnosticQuestionnaireEngine._generate_questions_ml(
            MANY_DISEASES, ["vomiting"], limit=3, previously_asked=set()
        )
        assert isinstance(questions, list)

    def test_returns_diagnostic_question_objects(self):
        questions = DiagnosticQuestionnaireEngine._generate_questions_ml(
            MANY_DISEASES, [], limit=3, previously_asked=set()
        )
        for q in questions:
            assert isinstance(q, DiagnosticQuestion)

    def test_limit_respected(self):
        questions = DiagnosticQuestionnaireEngine._generate_questions_ml(
            MANY_DISEASES, [], limit=2, previously_asked=set()
        )
        assert len(questions) <= 2

    def test_previously_asked_passed_through(self):
        questions = DiagnosticQuestionnaireEngine._generate_questions_ml(
            MANY_DISEASES,
            ["vomiting"],
            limit=3,
            previously_asked={"vomiting_frequency"},
        )
        assert isinstance(questions, list)

    def test_reasoning_contains_ig_score(self):
        questions = DiagnosticQuestionnaireEngine._generate_questions_ml(
            MANY_DISEASES, [], limit=3, previously_asked=set()
        )
        for q in questions:
            assert "Information gain" in q.reasoning_en or "information" in q.reasoning_en.lower()


# ---------------------------------------------------------------------------
# DiagnosticQuestionnaireEngine.update_diseases_from_answer
# ---------------------------------------------------------------------------


class TestUpdateDiseasesFromAnswer:
    def test_unknown_question_id_returns_unchanged(self):
        result = DiagnosticQuestionnaireEngine.update_diseases_from_answer(MANY_DISEASES, "nonexistent_question", "yes")
        assert result == MANY_DISEASES

    def test_yes_answer_increases_confidence(self):
        diseases = [
            make_disease("Canine Parvovirus", 100),
            make_disease("Pancreatitis", 50),
        ]
        result = DiagnosticQuestionnaireEngine.update_diseases_from_answer(diseases, "blood_in_vomit", "yes")
        parvovirus = next(d for d in result if d["name"] == "Canine Parvovirus")
        # blood_in_vomit targets Canine Parvovirus → should increase
        assert parvovirus["match_percent"] > 100

    def test_no_answer_decreases_confidence(self):
        diseases = [
            make_disease("Canine Parvovirus", 100),
            make_disease("Pancreatitis", 50),
        ]
        result = DiagnosticQuestionnaireEngine.update_diseases_from_answer(diseases, "blood_in_vomit", "no")
        parvovirus = next(d for d in result if d["name"] == "Canine Parvovirus")
        assert parvovirus["match_percent"] < 100

    def test_neutral_answer_unchanged(self):
        diseases = [
            make_disease("Canine Parvovirus", 100),
        ]
        result = DiagnosticQuestionnaireEngine.update_diseases_from_answer(diseases, "blood_in_vomit", "maybe")
        parvovirus = next(d for d in result if d["name"] == "Canine Parvovirus")
        assert parvovirus["match_percent"] == 100

    def test_non_targeted_disease_unchanged(self):
        diseases = [
            make_disease("Kidney Disease (CKD)", 80),
            make_disease("Canine Parvovirus", 50),
        ]
        result = DiagnosticQuestionnaireEngine.update_diseases_from_answer(diseases, "blood_in_vomit", "yes")
        kidney = next(d for d in result if d["name"] == "Kidney Disease (CKD)")
        # blood_in_vomit doesn't target Kidney Disease → unchanged
        assert kidney["match_percent"] == 80

    def test_result_sorted_by_match_percent(self):
        diseases = [
            make_disease("Canine Parvovirus", 50),
            make_disease("Pancreatitis", 80),
        ]
        result = DiagnosticQuestionnaireEngine.update_diseases_from_answer(diseases, "blood_in_vomit", "yes")
        percentages = [d["match_percent"] for d in result]
        assert percentages == sorted(percentages, reverse=True)

    def test_does_not_mutate_input(self):
        diseases = [make_disease("Canine Parvovirus", 80)]
        original_percent = diseases[0]["match_percent"]
        DiagnosticQuestionnaireEngine.update_diseases_from_answer(diseases, "blood_in_vomit", "yes")
        # Original list should be unchanged
        assert diseases[0]["match_percent"] == original_percent


# ---------------------------------------------------------------------------
# DiagnosticQuestionnaireEngine._get_adjustment_factor
# ---------------------------------------------------------------------------


class TestGetAdjustmentFactor:
    def test_yes_returns_1_3(self):
        assert DiagnosticQuestionnaireEngine._get_adjustment_factor("any", "yes") == 1.3

    def test_no_returns_0_7(self):
        assert DiagnosticQuestionnaireEngine._get_adjustment_factor("any", "no") == 0.7

    def test_other_returns_1_0(self):
        assert DiagnosticQuestionnaireEngine._get_adjustment_factor("any", "maybe") == 1.0
        assert DiagnosticQuestionnaireEngine._get_adjustment_factor("any", "") == 1.0
        assert DiagnosticQuestionnaireEngine._get_adjustment_factor("any", "positive") == 1.0


# ---------------------------------------------------------------------------
# build_next_question_response
# ---------------------------------------------------------------------------


class TestBuildNextQuestionResponse:
    def test_returns_dict(self):
        response = build_next_question_response(MANY_DISEASES, ["vomiting"])
        assert isinstance(response, dict)

    def test_required_keys(self):
        response = build_next_question_response(MANY_DISEASES, ["vomiting"])
        required = {
            "next_questions",
            "question_count",
            "current_candidates",
            "estimated_next_questions",
            "recommendation_ja",
            "recommendation_en",
        }
        assert required.issubset(response.keys())

    def test_current_candidates_matches_input(self):
        response = build_next_question_response(MANY_DISEASES, [])
        assert response["current_candidates"] == len(MANY_DISEASES)

    def test_question_count_matches_list(self):
        response = build_next_question_response(MANY_DISEASES, [])
        assert response["question_count"] == len(response["next_questions"])

    def test_question_limit_respected(self):
        response = build_next_question_response(MANY_DISEASES, [], question_limit=1)
        assert response["question_count"] <= 1

    def test_serialized_question_structure(self):
        response = build_next_question_response(MANY_DISEASES, ["vomiting"])
        for q in response["next_questions"]:
            assert "id" in q
            assert "question_ja" in q
            assert "question_en" in q
            assert "type" in q
            assert "options" in q
            assert "priority" in q
            assert "targets" in q
            assert "reasoning_ja" in q
            assert "reasoning_en" in q

    def test_estimated_next_questions_formula(self):
        # expected = max(0, (len - 1) // 2)
        response = build_next_question_response(MANY_DISEASES, [])
        expected = max(0, (len(MANY_DISEASES) - 1) // 2)
        assert response["estimated_next_questions"] == expected

    def test_recommendation_strings_non_empty(self):
        response = build_next_question_response(MANY_DISEASES, [])
        assert response["recommendation_ja"]
        assert response["recommendation_en"]


# ---------------------------------------------------------------------------
# QUESTION_TEMPLATES sanity check
# ---------------------------------------------------------------------------


class TestQuestionTemplates:
    def test_all_templates_have_required_fields(self):
        for q_id, q_data in DiagnosticQuestionnaireEngine.QUESTION_TEMPLATES.items():
            assert "question_ja" in q_data, f"Missing question_ja for {q_id}"
            assert "question_en" in q_data, f"Missing question_en for {q_id}"
            assert "question_type" in q_data, f"Missing question_type for {q_id}"
            assert "options" in q_data, f"Missing options for {q_id}"
            assert "disease_targets" in q_data, f"Missing disease_targets for {q_id}"

    def test_question_types_valid(self):
        valid_types = {"binary", "multiselect", "numeric"}
        for q_id, q_data in DiagnosticQuestionnaireEngine.QUESTION_TEMPLATES.items():
            assert q_data["question_type"] in valid_types, f"Invalid type for {q_id}"

    def test_at_least_seven_templates(self):
        assert len(DiagnosticQuestionnaireEngine.QUESTION_TEMPLATES) >= 7
