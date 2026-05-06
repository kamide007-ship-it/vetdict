"""drug_interactions モジュールの単体テスト"""

from __future__ import annotations

from api.drug_interactions import (
    INTERACTIONS,
    SEVERITY_CONTRAINDICATED,
    SEVERITY_MAJOR,
    SEVERITY_MODERATE,
    find_interactions,
    find_species_specific_warnings,
    get_all_interactions_for_drug,
    normalize_drug_id,
)


def test_data_integrity():
    """全エントリに必須フィールドが揃っている"""
    required = {"drug_a", "drug_b", "severity", "effect_en", "effect_ja"}
    for ix in INTERACTIONS:
        missing = required - set(ix.keys())
        assert not missing, f"Missing fields in {ix.get('drug_a')}/{ix.get('drug_b')}: {missing}"


def test_severities_are_valid():
    valid = {SEVERITY_CONTRAINDICATED, SEVERITY_MAJOR, SEVERITY_MODERATE}
    for ix in INTERACTIONS:
        assert ix["severity"] in valid


def test_normalize():
    assert normalize_drug_id("Cefazolin") == "cefazolin"
    assert normalize_drug_id("Trimethoprim-Sulfa") == "trimethoprim_sulfa"
    assert normalize_drug_id("  ENROFLOXACIN  ") == "enrofloxacin"


def test_find_nsaid_steroid_combo():
    """NSAID + ステロイドは禁忌として検出される"""
    found = find_interactions(["meloxicam", "prednisolone"])
    assert len(found) == 1
    assert found[0]["severity"] == SEVERITY_CONTRAINDICATED


def test_find_double_nsaid():
    """NSAID 2剤併用は禁忌"""
    found = find_interactions(["meloxicam", "carprofen"])
    assert len(found) == 1
    assert found[0]["severity"] == SEVERITY_CONTRAINDICATED


def test_no_match_when_only_one_drug():
    found = find_interactions(["meloxicam"])
    assert found == []


def test_severity_sort_order():
    """重症度順にソートされる: contraindicated → major → moderate"""
    found = find_interactions(["meloxicam", "prednisolone", "furosemide", "morphine", "acepromazine"])
    severities = [f["severity"] for f in found]
    severity_order = {SEVERITY_CONTRAINDICATED: 0, SEVERITY_MAJOR: 1, SEVERITY_MODERATE: 2}
    sorted_severities = sorted(severities, key=lambda s: severity_order[s])
    assert severities == sorted_severities


def test_species_specific_fipronil_rabbit():
    """ウサギにフィプロニルは禁忌"""
    warnings = find_species_specific_warnings("fipronil", "rabbit")
    assert len(warnings) == 1
    assert warnings[0]["severity"] == SEVERITY_CONTRAINDICATED


def test_species_specific_oral_amoxicillin_rabbit():
    """ウサギに経口アモキシシリンは禁忌"""
    warnings = find_species_specific_warnings("amoxicillin", "rabbit")
    assert len(warnings) >= 1
    assert any(w["severity"] == SEVERITY_CONTRAINDICATED for w in warnings)


def test_no_species_warning_for_safe_combo():
    """犬にメロキシカムは特異的警告なし"""
    warnings = find_species_specific_warnings("meloxicam", "dog")
    assert warnings == []


def test_get_all_interactions_for_meloxicam():
    """メロキシカムは複数の相互作用を持つ"""
    found = get_all_interactions_for_drug("meloxicam")
    assert len(found) >= 3  # carprofen, prednisolone, furosemide, warfarin等


def test_no_duplicate_pairs():
    """find_interactions は重複ペアを返さない"""
    found = find_interactions(["meloxicam", "carprofen", "meloxicam"])
    pairs = {tuple(sorted([f["drug_a"], f["drug_b"]])) for f in found}
    assert len(pairs) == len(found)
