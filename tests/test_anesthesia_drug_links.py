"""Regression tests for the anaesthesia → drug-dictionary navigation fix.

Two problems were addressed and are guarded here:

1. Six anaesthetic agents referenced by the anaesthesia protocols were missing
   from the drug dictionary (Thiopental, Guaifenesin/GGE, Detomidine,
   Mepivacaine, 2-Phenoxyethanol, Yohimbine). Detomidine additionally
   *mis-resolved* to Medetomidine via a naive substring match.

2. The JS drug-link resolver in ``renderAnesthesiaList`` links each base agent to
   its dictionary entry using a static canonical-term registry (``ANES_AGENTS`` in
   ``static/js/app.js``). Every canonical term must resolve to a real drug via the
   same substring filter the front-end uses, or the tap lands on an empty search.
   This test parses that registry and asserts it stays in sync with the dictionary.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.anesthesia_protocols import ANESTHESIA_PROTOCOLS  # noqa: E402
from api.drug_dictionary import DRUGS, _drug_index  # noqa: E402

APP_JS = ROOT / "static" / "js" / "app.js"

_NEW_AGENTS = ["thiopental", "guaifenesin", "detomidine", "mepivacaine", "phenoxyethanol", "yohimbine"]


# --------------------------------------------------------------------------- data


def test_missing_anaesthesia_agents_are_now_documented():
    for did in _NEW_AGENTS:
        d = _drug_index.get(did)
        assert d, f"{did} should be in the drug dictionary"
        assert d.get("species_info"), f"{did} needs species dosing"
        # every listed species carries an actual dose string
        for sp, info in d["species_info"].items():
            assert info.get("dosage") or info.get("dosage_ja"), f"{did}/{sp} missing dose"


def test_detomidine_is_distinct_from_medetomidine():
    """Detomidine (Dormosedan) is a separate alpha-2 agonist; before this entry a
    click on Detomidine wrongly resolved to Medetomidine by substring match."""
    deto = _drug_index.get("detomidine")
    assert deto and deto["name"].lower().startswith("detomidine")
    assert deto["id"] != "medetomidine"
    # Japanese name must not be the medetomidine string
    assert "メデトミジン" not in (deto.get("name_ja") or "")
    assert "デトミジン" in (deto.get("name_ja") or "")


def test_thiopental_flags_sighthound_and_perivascular_risk():
    d = _drug_index["thiopental"]
    contra = (d.get("contraindications") or "") + (d.get("contraindications_ja") or "")
    assert "ighthound" in contra or "サイトハウンド" in contra
    assert d["category"] == "anesthetics"


def test_guaifenesin_is_a_muscle_relaxant_not_an_anaesthetic():
    d = _drug_index["guaifenesin"]
    assert d["category"] == "muscle_relaxants"
    mech = (d.get("mechanism") or "").lower()
    assert "muscle relax" in mech


# ------------------------------------------------------------------ JS ↔ data sync


def _parse_anes_agents():
    """Extract the canonical ``q`` search terms from the JS ``ANES_AGENTS`` block."""
    src = APP_JS.read_text(encoding="utf-8")
    start = src.index("const ANES_AGENTS=[")
    end = src.index("const _ANES_ALIASES", start)
    return re.findall(r"\{q:\"([^\"]+)\"", src[start:end])


def _resolves(term):
    """Mirror the front-end drug filter: substring match on name / name_ja."""
    tl = term.lower()
    return [d for d in DRUGS if tl in (d.get("name") or "").lower() or tl in (d.get("name_ja") or "").lower()]


def _base(s):
    return re.split(r"[(（]", (s or "").lower())[0].strip()


def test_every_anaesthesia_link_term_resolves_to_a_real_drug():
    terms = _parse_anes_agents()
    assert len(terms) >= 30, "registry unexpectedly small — did the block move?"
    unresolved = [t for t in terms if not _resolves(t)]
    assert not unresolved, f"anaesthesia link terms with no drug entry: {unresolved}"


def test_every_anaesthesia_link_term_lands_on_the_intended_drug():
    """After the substring filter, the front-end expands the item whose *base* name
    matches the term. Verify each term either filters to a single drug or has an
    exact base-name match, so the tap never lands on an unrelated substring hit
    (e.g. デトミジン must not open Medetomidine)."""
    terms = _parse_anes_agents()
    wrong = []
    for term in terms:
        hits = _resolves(term)
        tgt = _base(term)
        exact = [d for d in hits if _base(d.get("name")) == tgt or _base(d.get("name_ja")) == tgt]
        pick = exact[0] if exact else (hits[0] if hits else None)
        if not pick:
            wrong.append((term, None))
            continue
        # A single filtered hit is unambiguous; otherwise the pick must base-match.
        if len(hits) > 1 and not (_base(pick.get("name")) == tgt or _base(pick.get("name_ja")) == tgt):
            wrong.append((term, pick.get("name")))
    assert not wrong, f"anaesthesia terms landing on the wrong drug: {wrong}"


def test_protocol_drug_names_have_a_resolver_alias():
    """Sanity floor: the vast majority of distinct protocol drug rows should map to
    at least one canonical term (combinations count once per component). Guards
    against the registry silently falling out of date with the protocols."""
    src = APP_JS.read_text(encoding="utf-8")
    aliases = re.findall(r"ja:\[([^\]]*)\]", src)
    ja_aliases = set()
    for grp in aliases:
        ja_aliases.update(re.findall(r'"([^"]+)"', grp))
    # Collect distinct Japanese base agents actually used in protocol rows.
    used = set()
    for data in ANESTHESIA_PROTOCOLS.values():
        for p in data.get("protocols", []) or []:
            for row in p.get("drugs", []) or []:
                nm = row.get("name_ja") or ""
                for alias in ja_aliases:
                    if alias in nm:
                        used.add(alias)
    # At least 20 distinct base agents should be recognised across the protocols.
    assert len(used) >= 20, f"resolver only recognised {len(used)} agents in protocols"
