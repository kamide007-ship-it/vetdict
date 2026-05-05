"""dose_calculator モジュールの単体テスト"""

from __future__ import annotations

import pytest

from api.dose_calculator import calculate_dose, parse_dosage, to_dict


def test_parse_simple_range():
    p = parse_dosage("20-35 mg/kg IV q6-8h")
    assert p.parsed
    assert p.low_mg_per_kg == 20.0
    assert p.high_mg_per_kg == 35.0
    assert p.unit == "mg"
    assert "IV" in p.routes
    assert p.interval_low_h == 6.0
    assert p.interval_high_h == 8.0


def test_parse_single_value():
    p = parse_dosage("0.2 mg/kg PO q24h")
    assert p.parsed
    assert p.low_mg_per_kg == 0.2
    assert p.high_mg_per_kg == 0.2
    assert "PO" in p.routes
    assert p.interval_low_h == 24.0


def test_parse_microgram():
    p = parse_dosage("10-20 μg/kg IM q12h")
    assert p.parsed
    # μg は mg に正規化される（10 μg = 0.01 mg）
    assert p.low_mg_per_kg == pytest.approx(0.01)
    assert p.high_mg_per_kg == pytest.approx(0.02)


def test_parse_iu_preserved():
    p = parse_dosage("100 IU/kg SC q24h")
    assert p.parsed
    assert p.is_iu
    assert p.unit == "IU"
    # IU は数値そのまま
    assert p.low_mg_per_kg == 100.0


def test_parse_no_match():
    p = parse_dosage("apply topically as needed")
    assert not p.parsed


def test_parse_fixed_dose():
    p = parse_dosage("100 mg/cat PO q12h")
    assert p.parsed
    assert p.fixed_low == 100.0
    assert p.unit == "mg"


def test_calculate_simple():
    drug = {
        "id": "test_drug",
        "name": "Test Drug",
        "species_info": {"dog": {"safe": True, "dosage": "10-20 mg/kg PO q12h"}},
    }
    calc = calculate_dose(drug, "dog", 10.0)
    assert calc.low_dose == 100.0  # 10 kg × 10 mg/kg
    assert calc.high_dose == 200.0  # 10 kg × 20 mg/kg
    assert "PO" in calc.routes


def test_calculate_with_concentration():
    drug = {
        "id": "test_drug",
        "name": "Test Drug",
        "species_info": {"cat": {"safe": True, "dosage": "5 mg/kg IV q8h"}},
    }
    calc = calculate_dose(drug, "cat", 4.0, concentration_mg_per_ml=10.0)
    assert calc.low_dose == 20.0  # 4 kg × 5 mg/kg
    # 20 mg / 10 mg/mL = 2 mL
    assert calc.volume_low_ml == 2.0


def test_calculate_warns_on_outlier_weight():
    drug = {
        "id": "test_drug",
        "name": "Test",
        "species_info": {"cat": {"safe": True, "dosage": "5 mg/kg IV"}},
    }
    # 50 kg の猫は異常
    calc = calculate_dose(drug, "cat", 50.0)
    assert any("通常範囲" in w for w in calc.warnings)


def test_calculate_warns_on_unsafe():
    drug = {
        "id": "fipronil_test",
        "name": "Fipronil",
        "species_info": {"rabbit": {"safe": False, "dosage": "topical"}},
    }
    calc = calculate_dose(drug, "rabbit", 2.0)
    assert any("安全性" in w or "禁忌" in w for w in calc.warnings)


def test_to_dict_roundtrip():
    drug = {
        "id": "test",
        "name": "Test",
        "species_info": {"dog": {"safe": True, "dosage": "20-30 mg/kg IV q8h"}},
    }
    calc = calculate_dose(drug, "dog", 15.0)
    d = to_dict(calc)
    assert d["drug_id"] == "test"
    assert d["body_weight_kg"] == 15.0
    assert d["low_dose"] == 300.0  # 15 × 20
    assert d["high_dose"] == 450.0  # 15 × 30
    assert d["interval"] == "q8h"
