"""clinical_reasoning モジュールの単体テスト"""

from __future__ import annotations

import os

from api.clinical_reasoning import (
    RED_FLAG_SYMPTOMS,
    build_reasoning,
    to_dict,
)


def test_no_differentials_returns_d_grade():
    result = build_reasoning(input_symptoms=[], differentials=[])
    assert result.bottom_line_evidence == "D"
    assert "情報が不足" in result.bottom_line["ja"]


def test_high_confidence_disease_with_matching_symptoms():
    diffs = [
        {
            "id": "d1",
            "name": "Disease A",
            "name_ja": "疾患A",
            "confidence": 0.92,
            "urgency": "moderate",
            "symptoms": ["fever", "cough", "lethargy", "anorexia"],
            "recommended_tests": ["CBC", "thoracic_radiography"],
        }
    ]
    result = build_reasoning(input_symptoms=["fever", "cough", "lethargy"], differentials=diffs)
    assert len(result.differentials) == 1
    d = result.differentials[0]
    # 入力3つはすべて支持症状
    assert len(d.matching_symptoms) == 3
    # 該疾患の典型で未確認はanorexia
    assert any(m["id"] == "anorexia" for m in d.missing_typical_symptoms)
    # 信頼度高+症状3+ → grade B
    assert result.bottom_line_evidence in ("A", "B")
    assert not result.emergency_alert


def test_emergency_disease_triggers_emergency_alert():
    diffs = [
        {
            "id": "gdv",
            "name": "Gastric Dilatation-Volvulus",
            "name_ja": "胃拡張捻転",
            "confidence": 0.85,
            "urgency": "emergency",
            "symptoms": ["bloat", "non_productive_vomiting", "collapse"],
            "recommended_tests": ["abdominal_radiography", "lactate"],
        }
    ]
    result = build_reasoning(input_symptoms=["bloat", "non_productive_vomiting"], differentials=diffs)
    assert result.emergency_alert
    assert "緊急" in result.bottom_line["ja"]


def test_red_flag_symptoms_in_input_triggers_alert():
    diffs = [
        {
            "id": "d1",
            "name": "X",
            "name_ja": "X",
            "confidence": 0.4,
            "urgency": "moderate",
            "symptoms": ["lethargy"],
            "recommended_tests": [],
        }
    ]
    result = build_reasoning(input_symptoms=["seizure", "lethargy"], differentials=diffs)
    assert result.emergency_alert  # seizure is in RED_FLAG_SYMPTOMS


def test_low_input_count_warning():
    diffs = [
        {
            "id": "d1",
            "name": "X",
            "name_ja": "X",
            "confidence": 0.5,
            "urgency": "moderate",
            "symptoms": ["a"],
            "recommended_tests": [],
        }
    ]
    result = build_reasoning(input_symptoms=["a"], differentials=diffs)
    assert result.needs_more_info
    assert result.confidence_warning


def test_rule_out_questions_generated():
    diffs = [
        {
            "id": "d1",
            "name": "Disease",
            "name_ja": "疾患",
            "confidence": 0.7,
            "urgency": "moderate",
            "symptoms": ["fever", "weight_loss", "dyspnea"],
            "recommended_tests": [],
        }
    ]
    result = build_reasoning(input_symptoms=["fever"], differentials=diffs, lang="ja")
    d = result.differentials[0]
    assert len(d.rule_out_questions) >= 1
    assert "確認できますか" in d.rule_out_questions[0]


def test_next_steps_aggregated_across_top_differentials():
    diffs = [
        {
            "id": "d1",
            "name": "A",
            "name_ja": "A",
            "confidence": 0.8,
            "urgency": "moderate",
            "symptoms": ["x"],
            "recommended_tests": ["CBC", "biochem"],
        },
        {
            "id": "d2",
            "name": "B",
            "name_ja": "B",
            "confidence": 0.6,
            "urgency": "moderate",
            "symptoms": ["x"],
            "recommended_tests": ["urinalysis", "CBC"],
        },
    ]
    result = build_reasoning(input_symptoms=["x"], differentials=diffs)
    test_ids = {s["id"] for s in result.next_steps}
    assert "CBC" in test_ids
    assert "urinalysis" in test_ids


def test_to_dict_serializable():
    diffs = [
        {
            "id": "d1",
            "name": "A",
            "name_ja": "A",
            "confidence": 0.7,
            "urgency": "high",
            "symptoms": ["x", "y"],
            "recommended_tests": ["CBC"],
        }
    ]
    result = build_reasoning(input_symptoms=["x"], differentials=diffs)
    d = to_dict(result)
    assert "bottom_line" in d
    assert "differentials" in d
    assert d["differentials"][0]["disease_name"] == "A"
    assert d["differentials"][0]["confidence"] == 0.7


def test_red_flag_set_contains_critical_signs():
    """RED_FLAG_SYMPTOMSセットが臨床的に重要な徴候を含む"""
    critical = {"seizure", "collapse", "shock", "anaphylaxis", "urinary_obstruction"}
    assert critical.issubset(RED_FLAG_SYMPTOMS)


def test_chat_endpoint_includes_clinical_reasoning():
    os.environ.setdefault("SECRET_KEY", "test_reasoning")
    from api.vetdict_api import app

    client = app.test_client()
    res = client.post(
        "/api/diagnostic-chat/chat",
        json={"message": "発熱 咳 元気消失", "species": "dog", "lang": "ja"},
    )
    assert res.status_code == 200
    data = res.get_json()
    # clinical_reasoning is included (even if empty differentials)
    assert "clinical_reasoning" in data
    assert "bottom_line" in data["clinical_reasoning"]
