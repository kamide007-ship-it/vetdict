"""emergency_protocols モジュールのテスト"""

from __future__ import annotations

import os

import pytest

from api.emergency_protocols import (
    EMERGENCY_PROTOCOLS,
    PROTOCOL_CATEGORIES,
    get_protocol,
    list_protocols,
)


def test_data_integrity():
    """全プロトコルに必須フィールド"""
    required = {"id", "category", "title_ja", "title_en", "species", "steps", "key_drugs", "monitoring", "ref"}
    for p in EMERGENCY_PROTOCOLS:
        missing = required - set(p.keys())
        assert not missing, f"Missing in {p.get('id')}: {missing}"


def test_unique_ids():
    ids = [p["id"] for p in EMERGENCY_PROTOCOLS]
    assert len(ids) == len(set(ids))


def test_categories_valid():
    valid_cats = set(PROTOCOL_CATEGORIES.keys())
    for p in EMERGENCY_PROTOCOLS:
        assert p["category"] in valid_cats


def test_steps_well_ordered():
    """各プロトコルのstepsは順序付き"""
    for p in EMERGENCY_PROTOCOLS:
        steps = p["steps"]
        assert len(steps) >= 3
        orders = [s["order"] for s in steps]
        assert orders == sorted(orders)


def test_steps_have_bilingual_content():
    for p in EMERGENCY_PROTOCOLS:
        for s in p["steps"]:
            assert s.get("ja") and s.get("en")


def test_filter_by_species_dog():
    cpr = list_protocols(species="dog", category="cpr")
    assert len(cpr) >= 1
    assert all("dog" in p["species"] for p in cpr)


def test_filter_by_category():
    shock = list_protocols(category="shock")
    assert len(shock) >= 1
    assert all(p["category"] == "shock" for p in shock)


def test_search_by_keyword():
    results = list_protocols(search="anaphylactic")
    assert len(results) >= 1
    results = list_protocols(search="アナフィラキシー")
    assert len(results) >= 1


def test_get_protocol_existing():
    p = get_protocol("cpr_basic")
    assert p is not None
    assert p["category"] == "cpr"


def test_get_protocol_nonexistent():
    p = get_protocol("nonexistent_xyz")
    assert p is None


@pytest.fixture
def client():
    os.environ.setdefault("SECRET_KEY", "test_emergency")
    from api.vetdict_api import app

    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_api_list_protocols(client):
    res = client.get("/api/emergency/protocols")
    assert res.status_code == 200
    data = res.get_json()
    assert "protocols" in data
    assert data["total"] >= 5
    assert "categories" in data


def test_api_filter_by_species(client):
    res = client.get("/api/emergency/protocols?species=dog")
    assert res.status_code == 200
    data = res.get_json()
    for p in data["protocols"]:
        assert "dog" in p["species"]


def test_api_get_protocol(client):
    res = client.get("/api/emergency/protocols/cpr_basic")
    assert res.status_code == 200
    data = res.get_json()
    assert data["protocol"]["id"] == "cpr_basic"


def test_api_404_for_unknown(client):
    res = client.get("/api/emergency/protocols/nonexistent")
    assert res.status_code == 404


def test_api_categories(client):
    res = client.get("/api/emergency/categories")
    assert res.status_code == 200
    data = res.get_json()
    assert len(data["categories"]) >= 5
    assert data["total_protocols"] >= 5
