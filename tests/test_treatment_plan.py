"""treatment_plan モジュールのテスト"""

from __future__ import annotations

import os

import pytest

from api.treatment_plan import build_treatment_plan, to_dict


@pytest.fixture
def drug_lookup():
    """テスト用薬品DB"""
    return {
        "meloxicam": {
            "id": "meloxicam",
            "name": "Meloxicam",
            "name_ja": "メロキシカム",
            "category": "nsaids",
            "species_info": {
                "dog": {"safe": True, "dosage": "0.2 mg/kg PO q24h"},
                "cat": {"safe": True, "dosage": "0.05 mg/kg PO q24h"},
            },
        },
        "prednisolone": {
            "id": "prednisolone",
            "name": "Prednisolone",
            "name_ja": "プレドニゾロン",
            "category": "corticosteroids",
            "species_info": {
                "dog": {"safe": True, "dosage": "0.5-2 mg/kg PO q12h"},
            },
        },
        "cefazolin": {
            "id": "cefazolin",
            "name": "Cefazolin",
            "name_ja": "セファゾリン",
            "category": "antibiotics",
            "species_info": {
                "dog": {"safe": True, "dosage": "20-35 mg/kg IV q6-8h"},
            },
        },
    }


def test_basic_plan_with_single_drug(drug_lookup):
    disease = {
        "id": "test1",
        "name": "Test Disease",
        "name_ja": "テスト疾患",
        "treatment": "Administer cefazolin 22 mg/kg IV q8h. Monitor BUN, creatinine.",
        "treatment_ja": "セファゾリン 22 mg/kg IV q8h を投与。BUN、クレアチニンをモニタリング。",
        "urgency": "moderate",
    }
    plan = build_treatment_plan(disease, drug_lookup, species="dog", body_weight_kg=10.0)
    drug_ids = [d.drug_id for d in plan.drugs]
    assert "cefazolin" in drug_ids
    assert plan.drugs[0].calculated_dose is not None
    assert plan.drugs[0].calculated_dose["low_dose"] == 200.0  # 20 mg/kg × 10 kg
    assert any("BUN" in m["key"] for m in plan.monitoring_parameters)


def test_plan_detects_drug_interactions(drug_lookup):
    """治療文に併用禁忌薬品が含まれたら相互作用を検出"""
    disease = {
        "id": "test2",
        "name": "Test",
        "name_ja": "テスト",
        "treatment": "Use meloxicam 0.2 mg/kg PO q24h with prednisolone 1 mg/kg PO q12h.",
        "treatment_ja": "メロキシカム 0.2 mg/kg + プレドニゾロン 1 mg/kg を併用。",
        "urgency": "moderate",
    }
    plan = build_treatment_plan(disease, drug_lookup, species="dog", body_weight_kg=10.0)
    assert len(plan.drug_drug_interactions) >= 1
    assert any(i["severity"] == "contraindicated" for i in plan.drug_drug_interactions)


def test_plan_warns_when_weight_missing(drug_lookup):
    disease = {
        "id": "test3",
        "name": "Test",
        "name_ja": "テスト",
        "treatment": "Administer cefazolin 20 mg/kg IV.",
        "treatment_ja": "セファゾリン 20 mg/kg IV。",
        "urgency": "moderate",
    }
    plan = build_treatment_plan(disease, drug_lookup, species="dog", body_weight_kg=None)
    assert any("体重" in w or "weight" in w.lower() for w in plan.warnings)


def test_plan_includes_checklist(drug_lookup):
    disease = {
        "id": "test4",
        "name": "Test",
        "name_ja": "テスト",
        "treatment": "Use cefazolin.",
        "treatment_ja": "セファゾリン投与。",
        "urgency": "moderate",
    }
    plan = build_treatment_plan(disease, drug_lookup, species="dog")
    cats = {c["category"] for c in plan.checklist}
    assert "assessment" in cats
    assert "consent" in cats


def test_plan_evidence_grade_for_well_cited(drug_lookup):
    """ACVIM引用 + 用量 + モニタリング → 高グレード"""
    disease = {
        "id": "test5",
        "name": "Test",
        "name_ja": "テスト",
        "treatment": ("Cefazolin 20-35 mg/kg IV q6-8h. Monitor BUN, creatinine. Per ACVIM consensus 2019."),
        "treatment_ja": "セファゾリン 20-35 mg/kg q6-8h。BUN・Crモニタリング。ACVIM 2019準拠。",
        "urgency": "moderate",
    }
    plan = build_treatment_plan(disease, drug_lookup, species="dog", body_weight_kg=10)
    assert plan.overall_evidence_grade in ("A", "B")


def test_to_dict_serializable(drug_lookup):
    disease = {
        "id": "x",
        "name": "X",
        "name_ja": "X",
        "treatment": "Use cefazolin 20 mg/kg IV q8h.",
        "treatment_ja": "セファゾリン投与。",
        "urgency": "moderate",
    }
    plan = build_treatment_plan(disease, drug_lookup, species="dog", body_weight_kg=10)
    d = to_dict(plan)
    assert d["disease_id"] == "x"
    assert isinstance(d["drugs"], list)
    assert isinstance(d["checklist"], list)


def test_api_endpoint():
    os.environ.setdefault("SECRET_KEY", "test_plan")
    from api.vetdict_api import app

    client = app.test_client()
    res = client.post(
        "/api/treatment-plan/generate",
        json={
            "disease": {
                "id": "test_d",
                "name": "Test Disease",
                "name_ja": "テスト疾患",
                "treatment": "Cefazolin 22 mg/kg IV q8h. Monitor BUN.",
                "treatment_ja": "セファゾリン投与。",
                "urgency": "moderate",
            },
            "species": "dog",
            "body_weight_kg": 15,
            "lang": "ja",
        },
    )
    assert res.status_code == 200
    data = res.get_json()
    assert "plan" in data
    assert data["plan"]["species"] == "dog"
