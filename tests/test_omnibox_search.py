"""Omnibox 2.0 (2026-09): the header search reaches everything.

Before this round the global search box matched drugs by raw lowercase name
only (so 「バイトリル」 — the brand-name fix from the drug tab — was 0 hits
here), the drug dictionary was not loaded until a species tap or a drug-tab
visit (so first-visit drug queries were silently empty), emergency protocols
were unreachable from the box, and a no-hit query dead-ended on a single
"no matching diseases" line.  The cross-species disease API also missed
hiragana / full-width input.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_JS = (PROJECT_ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
HEADER = (PROJECT_ROOT / "templates" / "partials" / "_header.html").read_text(encoding="utf-8")
CSS = (PROJECT_ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")


def _omnibox_block() -> str:
    start = APP_JS.index("function setupGlobalSearch(")
    end = APP_JS.index("function setupSearchFilters(", start)
    return APP_JS[start:end]


# ---------------------------------------------------------------------------
# Server: kana / width normalised disease name search
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def client():
    os.environ.setdefault("SECRET_KEY", "test-omnibox")
    from api.vetdict_api import app

    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_disease_search_folds_hiragana_and_fullwidth(client):
    """「ぱるぼ」 must reach パルボ names and 「ＦＩＰ」 must reach FIP names —
    the same NFKC + hiragana→katakana rule the drug dictionary uses."""
    hira = client.get("/api/diseases?q=ぱるぼ&limit=20").get_json()
    assert hira["success"] and hira["diseases"], hira
    assert any("パルボ" in (d.get("name_ja") or "") for d in hira["diseases"])
    wide = client.get("/api/diseases?q=ＦＩＰ&limit=20").get_json()
    assert wide["diseases"], wide
    assert any("FIP" in (d.get("name") or d.get("name_ja") or "") for d in wide["diseases"])
    # Exact input keeps working (no regression on the primary path).
    exact = client.get("/api/diseases?q=白点&limit=5").get_json()
    assert any("白点病" in (d.get("name_ja") or "") for d in exact["diseases"])


def test_normalizer_unit():
    from api.disease_store import _normalize_search_text

    assert _normalize_search_text("ぱるぼ") == "パルボ"
    assert _normalize_search_text("ＦＩＰ") == "fip"
    assert _normalize_search_text("ﾊﾞｲﾄﾘﾙ") == "バイトリル"


# ---------------------------------------------------------------------------
# Client: omnibox wiring
# ---------------------------------------------------------------------------


def test_omnibox_drug_matching_uses_normalised_brand_alias_rule():
    block = _omnibox_block()
    # Same matcher as the drug tab: normalised query + name/alias/brand rule.
    assert "const nq=normalizeDrugSearchText(rawQ);" in block
    assert "_drugMatchesSearch(d,nq)" in block
    # Brand hits are labelled so the vet sees why バイトリル returned enrofloxacin.
    assert 'class="drug-brand-hit"' in block
    # Raw lowercase includes() on drug names must be gone.
    assert 'const name=(d.name||"").toLowerCase();' not in block


def test_omnibox_loads_drug_dictionary_on_first_use_and_prefetches():
    block = _omnibox_block()
    assert "_rerunWhenDrugsLoaded(reqId,0)" in block
    assert "loadDrugDictionary()" in block
    assert "requestIdleCallback" in block  # idle prefetch no longer gated on a species tap
    # Pending state is surfaced instead of a silent empty drug section.
    assert "薬品辞書を読み込み中" in block
    # Overlapping prefetch paths cannot double-fetch the formulary.
    assert "let _drugLoadInFlight=false;" in APP_JS
    assert "if(_drugLoadInFlight)return;" in APP_JS


def test_omnibox_surfaces_emergency_protocols():
    assert "function ensureEmergencySearchData(" in APP_JS
    block = _omnibox_block()
    assert "ensureEmergencySearchData().then(" in block
    assert 'type:"emergency"' in block
    # Tap routes through the exact-landing emergency navigator.
    assert 'item.dataset.type==="emergency"' in block
    assert "navigateToEmergencyProtocol(item.dataset.proto)" in block
    # The omnibox cache must not alias the emergency tab's own state.
    helper = APP_JS[APP_JS.index("function ensureEmergencySearchData(") :][:900]
    assert "_omniEmergency=" in helper
    assert "emergencyLoaded=" not in helper


def test_omnibox_action_rows_connect_checker_anesthesia_and_chat():
    block = _omnibox_block()
    for action in ("checker", "anesthesia", "chat"):
        assert f'data-action="{action}"' in block, action
        assert f'item.dataset.action==="{action}"' in block, action
    # Symptom row only when a species vocabulary is loaded (never guesses).
    assert "currentSpecies&&Array.isArray(symptomData)&&symptomData.length" in block
    assert '_runCheckerWithSymptoms(currentSpecies||"dog",[item.dataset.symptom],"checker_from_search")' in block
    # Chat row pre-fills the free-input box with the query and focuses it.
    assert 'switchChatMode("free")' in block
    assert "ci.value=rawQ" in block
    # Anesthesia row pre-fills the protocol search (drug→anesthesia pattern).
    assert 'document.getElementById("anesthesiaSearch")' in block
    # No-hit state keeps the action rows instead of dead-ending.
    assert "該当する疾患・薬品が見つかりません" in block
    assert "${actions}" in block


def test_omnibox_recent_items_carry_species_and_protocol():
    assert "function saveRecentSearch(type,name,nameJa,extra)" in APP_JS
    recent = APP_JS[APP_JS.index("function showRecentSearches(") :][:1200]
    assert 'data-species="${escapeHtml(m.species||"")}"' in recent
    assert 'data-proto="${escapeHtml(m.proto||"")}"' in recent


def test_omnibox_placeholder_and_styles():
    assert "バイトリル" in HEADER  # example in the placeholder teaches brand search
    assert 'globalSearchPh:"疾患・薬品・症状・救急を検索' in APP_JS
    assert ".search-action-item{" in CSS
    assert ".search-action-head{" in CSS
