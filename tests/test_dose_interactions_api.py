"""用量計算機・相互作用APIのE2Eテスト"""

from __future__ import annotations

import pytest


@pytest.fixture
def client():
    from api.vetdict_api import app

    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_calculate_dose_endpoint(client):
    res = client.post(
        "/api/drugs/calculate-dose",
        json={"drug_id": "cefazolin", "species": "dog", "body_weight_kg": 10.0},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert "calculation" in data
    calc = data["calculation"]
    assert calc["drug_id"] == "cefazolin"
    assert calc["body_weight_kg"] == 10.0
    # 20-35 mg/kg × 10 kg = 200-350 mg
    assert calc["low_dose"] == 200.0
    assert calc["high_dose"] == 350.0


def test_calculate_dose_with_concentration(client):
    res = client.post(
        "/api/drugs/calculate-dose",
        json={
            "drug_id": "cefazolin",
            "species": "cat",
            "body_weight_kg": 4.0,
            "concentration_mg_per_ml": 100.0,
        },
    )
    assert res.status_code == 200
    calc = res.get_json()["calculation"]
    # 20-35 mg/kg × 4 kg = 80-140 mg
    assert calc["low_dose"] == 80.0
    # 80 mg / 100 mg/mL = 0.8 mL
    assert calc["volume_low_ml"] == 0.8


def test_calculate_dose_missing_params(client):
    res = client.post("/api/drugs/calculate-dose", json={"drug_id": "cefazolin"})
    assert res.status_code == 400


def test_calculate_dose_unknown_drug(client):
    res = client.post(
        "/api/drugs/calculate-dose",
        json={"drug_id": "nonexistent_drug_xyz", "species": "dog", "body_weight_kg": 10.0},
    )
    assert res.status_code == 404


def test_check_interactions_endpoint(client):
    res = client.post(
        "/api/drugs/check-interactions",
        json={"drug_ids": ["meloxicam", "prednisolone"]},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_interactions"] >= 1
    # 禁忌が最初に来る
    assert data["interactions"][0]["severity"] == "contraindicated"


def test_check_interactions_with_species_warning(client):
    res = client.post(
        "/api/drugs/check-interactions",
        json={"drug_ids": ["fipronil"], "species": "rabbit"},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["species_specific_warnings"]) >= 1
    assert data["species_specific_warnings"][0]["severity"] == "contraindicated"


def test_check_interactions_empty(client):
    res = client.post("/api/drugs/check-interactions", json={"drug_ids": []})
    assert res.status_code == 200
    data = res.get_json()
    assert data["interactions"] == []


def test_drug_interactions_endpoint(client):
    res = client.get("/api/drugs/meloxicam/interactions")
    assert res.status_code == 200
    data = res.get_json()
    assert data["drug_id"] == "meloxicam"
    assert data["total"] >= 3
