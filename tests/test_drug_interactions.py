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


class TestInteractionCheckerNameResolution:
    """2026-09 UX: the interaction checker used to accept only exact lowercase
    drug ids — バイトリル/メロキシカム or brand names all came back unknown.
    resolve_drug_reference now resolves ids, Japanese names, English names and
    brand aliases (with kana/width normalisation), and the endpoint returns a
    `resolved` mapping so the UI can confirm what each input matched."""

    def test_resolve_drug_reference_accepts_natural_inputs(self):
        from api.drug_dictionary import resolve_drug_reference

        cases = {
            "meloxicam": "meloxicam",  # id (legacy behavior)
            "メロキシカム": "meloxicam",  # Japanese name
            "バイトリル": "enrofloxacin",  # brand name
            "ばいとりる": "enrofloxacin",  # hiragana input
            "メタカム": "meloxicam",  # brand name
            "ラシックス": "furosemide",  # human brand in vet use
            "クラバモックス": "amoxicillin_clavulanate",
            "CBD": "cannabidiol",  # short Latin exact alias
            "hCG": "hcg",
        }
        for token, want in cases.items():
            assert resolve_drug_reference(token) == want, token
        assert resolve_drug_reference("存在しない薬") is None
        assert resolve_drug_reference("") is None

    def test_check_interactions_endpoint_resolves_names(self, client=None):
        import json

        from api.vetdict_api import app

        c = app.test_client()
        r = c.post(
            "/api/drugs/check-interactions",
            data=json.dumps({"drug_ids": ["バイトリル", "メロキシカム", "謎の薬X"], "species": "dog"}),
            content_type="application/json",
        )
        assert r.status_code == 200
        d = r.get_json()
        assert d["unknown_drug_ids"] == ["謎の薬X"]
        ids = {row["id"] for row in d["resolved"]}
        assert ids == {"enrofloxacin", "meloxicam"}
        # every resolved row carries display names for the UI confirmation line
        for row in d["resolved"]:
            assert row["name"] and "input" in row
        # the classic NSAID+steroid pair still fires through name inputs
        r2 = c.post(
            "/api/drugs/check-interactions",
            data=json.dumps({"drug_ids": ["メロキシカム", "プレドニゾロン"]}),
            content_type="application/json",
        )
        assert r2.get_json()["total_interactions"] >= 1

    def test_app_js_one_tap_add_to_interaction_checker(self):
        from pathlib import Path

        js = Path("static/js/app.js").read_text(encoding="utf-8")
        # one-tap add helper + delegated routing from drug detail cards
        assert "function addDrugToInteractionChecker" in js
        assert 'closest(".drug-interaction-add")' in js
        assert "drug-interaction-add" in js and "相互作用チェックに追加" in js
        # the client must send raw trimmed tokens (no lowercase/underscore
        # mangling that broke every non-id input)
        assert 'replace(/\\s+/g,"_")' not in js.split("function runInteractionCheck")[1].split("function ")[0]
        css = Path("static/css/main.css").read_text(encoding="utf-8")
        assert ".drug-interaction-add" in css
