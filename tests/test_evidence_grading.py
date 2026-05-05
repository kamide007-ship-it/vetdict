"""evidence_grading モジュールの単体テスト"""

from __future__ import annotations

from api.evidence_grading import (
    AI_CONTENT_DISCLAIMER,
    DIAGNOSTIC_DISCLAIMER,
    DOSE_CALCULATOR_DISCLAIMER,
    GRADE_A,
    GRADE_B,
    GRADE_C,
    GRADE_D,
    GRADE_LABELS,
    assess,
    to_dict,
)


def test_grade_a_with_high_quality_ref_and_dosing():
    """ACVIMガイドライン+用量+経路+モニタリング → グレードA"""
    text = (
        "Furosemide 1-2 mg/kg IV q12h. Monitor BUN, creatinine, electrolytes. "
        "Reduce dose if azotemia develops. (Ref: ACVIM Cardiac Consensus 2019)"
    )
    a = assess(text)
    assert a.grade == GRADE_A
    assert a.has_citation
    assert a.has_dosing
    assert a.has_route
    assert a.has_interval
    assert a.has_monitoring


def test_grade_b_with_textbook_ref():
    """Plumb's教科書引用+用量 → グレードB以上"""
    text = "Cefazolin 20-35 mg/kg IV q6-8h. (Ref: Plumb's 9th ed.)"
    a = assess(text)
    assert a.grade in (GRADE_A, GRADE_B)
    assert a.citation_quality == "textbook"


def test_grade_c_no_citation_minimal_dosing():
    """引用なし、用量のみ"""
    text = "Apply meloxicam 0.2 mg/kg PO once daily."
    a = assess(text)
    assert a.grade in (GRADE_B, GRADE_C)
    assert a.has_dosing


def test_grade_d_template_text():
    """無内容のテンプレ文 → グレードD"""
    text = "Provide supportive care. Consult a veterinarian."
    a = assess(text)
    assert a.grade == GRADE_D
    assert not a.has_citation
    assert not a.has_dosing


def test_grade_d_empty():
    a = assess("")
    assert a.grade == GRADE_D
    assert a.score == 0


def test_extract_acvim_reference():
    a = assess("Use enalapril per ACVIM consensus 2019.")
    assert a.has_citation
    assert a.citation_quality == "high"
    assert "ACVIM" in [r.upper() for r in a.detected_refs]


def test_extract_journal_reference():
    a = assess("Per JAVMA 2020, dosing recommendations updated.")
    assert a.has_citation
    assert a.citation_quality == "journal"


def test_label_lookup():
    assert GRADE_LABELS[GRADE_A]["en"] == "Strong evidence"
    assert GRADE_LABELS[GRADE_A]["ja"] == "高エビデンス"


def test_to_dict_serializable():
    text = "Cefazolin 20 mg/kg IV q8h. Monitor renal function. (Ref: Plumb's 9th ed.)"
    a = assess(text)
    d = to_dict(a)
    assert d["grade"] in ("A", "B", "C", "D")
    assert isinstance(d["score"], int)
    assert isinstance(d["detected_refs"], list)


def test_disclaimer_strings_have_both_languages():
    for _key, disclaimer in [
        ("ai_content", AI_CONTENT_DISCLAIMER),
        ("diagnostic", DIAGNOSTIC_DISCLAIMER),
        ("dose_calculator", DOSE_CALCULATOR_DISCLAIMER),
    ]:
        assert "ja" in disclaimer
        assert "en" in disclaimer
        assert len(disclaimer["ja"]) > 30
        assert len(disclaimer["en"]) > 30


def test_evidence_endpoint(monkeypatch):
    import os

    os.environ.setdefault("SECRET_KEY", "test_evidence")
    from api.vetdict_api import app

    client = app.test_client()
    res = client.post(
        "/api/evidence/assess",
        json={"text": "Cefazolin 20-35 mg/kg IV q8h. (Ref: Plumb's 9th ed.)"},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert "assessment" in data
    assert data["assessment"]["grade"] in ("A", "B", "C", "D")


def test_disclaimers_endpoint():
    import os

    os.environ.setdefault("SECRET_KEY", "test_evidence")
    from api.vetdict_api import app

    client = app.test_client()
    res = client.get("/api/disclaimers")
    assert res.status_code == 200
    data = res.get_json()
    assert "ai_content" in data
    assert "diagnostic" in data
    assert "dose_calculator" in data
    assert "ja" in data["ai_content"]
