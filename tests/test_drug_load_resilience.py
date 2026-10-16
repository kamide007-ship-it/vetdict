"""Regression tests for the "デポメドロール search dead" report (2026-10).

Root cause was not data (the entry exists and matches) but load resilience:
when the first /api/drugs fetch failed (Render cold start exceeding the 10s
fetch timeout, or a flaky connection), the drug tab replaced the retry UI with
the misleading zero-results message on the next keystroke, and the omnibox's
one-shot ``_drugLoadKicked`` guard left it stuck on "薬品辞書を読み込み中…"
forever. Typing then never recovered — "デポメドロールと入れて反応しない".
"""

import re
from pathlib import Path

APP_JS = Path(__file__).resolve().parent.parent / "static" / "js" / "app.js"
SW_JS = Path(__file__).resolve().parent.parent / "static" / "sw.js"


def _src():
    return APP_JS.read_text(encoding="utf-8")


class TestDepoMedrolSearchData:
    """The dictionary itself must keep resolving the brand name."""

    def test_backend_search_and_resolver_hit_methylprednisolone(self):
        from api.drug_dictionary import resolve_drug_reference, search_drugs

        hits = search_drugs("デポメドロール")
        assert any(d["id"] == "methylprednisolone" for d in hits)
        # hiragana / English brand / generic-name variants
        for q in ("でぽめどろーる", "depo-medrol", "medrol", "メドロール"):
            assert resolve_drug_reference(q) == "methylprednisolone", q

    def test_text_matcher_resolves_depot_mentions(self):
        from api.drug_dictionary import find_drugs_in_text

        ids = {d["id"] for d in find_drugs_in_text("デポメドロール 20 mg/頭 SC")}
        assert "methylprednisolone" in ids


class TestDrugLoadResilience:
    """Front-end wiring: a failed first load must stay recoverable."""

    def test_render_drug_list_self_heals_when_dictionary_not_loaded(self):
        src = _src()
        m = re.search(r"function renderDrugList\(\)\{(.{0,900})", src, re.S)
        assert m, "renderDrugList missing"
        head = m.group(1)
        # Early return before any filtering: never overwrite the skeleton or
        # the error+retry UI with the zero-results message, and re-kick the
        # load so typing itself recovers from a failed fetch.
        guard = re.search(r"if\(!drugsLoaded\)\{(.*?)\breturn;", head, re.S)
        assert guard, "renderDrugList lacks the !drugsLoaded self-heal guard"
        assert "loadDrugDictionary()" in guard.group(1)
        assert "_drugLoadInFlight" in guard.group(1)
        # The guard must come before the search filtering logic.
        assert head.index("if(!drugsLoaded)") < head.index("drugSearch")

    def test_drug_dictionary_fetch_uses_cold_start_tolerant_timeout(self):
        src = _src()
        assert re.search(r'fetchWithTimeout\("/api/drugs",\{\},45000\)', src), (
            "/api/drugs fetch must use a 45s timeout (Render cold start > 10s default)"
        )

    def test_omnibox_rekicks_drug_load_after_failure(self):
        src = _src()
        # The one-shot kick at the omnibox search site was the stuck-loading
        # bug; the kick must now depend only on drugsLoaded (the global
        # _drugLoadInFlight guard inside loadDrugDictionary dedupes).
        assert not re.search(r"drugsPending=true;\s*(/\*.*?\*/\s*)?if\(!_drugLoadKicked\)", src, re.S), (
            "omnibox drug branch must not use the one-shot _drugLoadKicked guard"
        )
        pending = re.search(r"drugsPending=true;(.{0,500})", src, re.S)
        assert pending and "if(!drugsLoaded)loadDrugDictionary();" in pending.group(1)

    def test_service_worker_cache_version_bumped(self):
        m = re.search(r"const CACHE_NAME = 'vetdict-v(\d+)';", SW_JS.read_text(encoding="utf-8"))
        assert m and int(m.group(1)) >= 182
