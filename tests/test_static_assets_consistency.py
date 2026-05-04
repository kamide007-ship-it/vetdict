"""Regression tests for static asset consistency.

Catches drift between marketing copy embedded in static files and the
real database state — outdated counts in PWA manifest, social share text,
or service worker cache identifiers easily slip past code review.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# manifest.json (PWA)
# ---------------------------------------------------------------------------
def test_manifest_is_valid_json_and_has_shortcuts():
    data = json.loads(_read("static/manifest.json"))
    assert data["name"]
    assert data["start_url"] == "/"
    shortcuts = data.get("shortcuts") or []
    # Must list every primary tab so PWA users can deep-link from the
    # home-screen shortcut menu.
    urls = {s["url"] for s in shortcuts}
    for required in ("/#checker", "/#database", "/#chat", "/#drugs", "/#anesthesia"):
        assert required in urls, f"PWA shortcut missing for {required}"


def test_manifest_has_no_stale_counts():
    text = _read("static/manifest.json")
    # Old counts that historically drifted out of sync with the live DB.
    # Each represents a regression we don't want to reintroduce.
    assert "220+薬品" not in text, "Stale drug count (220+) — current is 250+"
    assert "194薬品" not in text, "Stale drug count (194) — current is 250+"
    assert "6,400+疾患" not in text, "Stale disease count (6,400+) — current is 7,000+"


# ---------------------------------------------------------------------------
# Footer social share URLs
# ---------------------------------------------------------------------------
def test_footer_share_text_does_not_use_brittle_exact_count():
    """Twitter/X share text should use the rounded "7,000+" form, not an
    exact figure that drifts each time we add diseases."""
    text = _read("templates/partials/_footer.html")
    # Find each share href and decode the text= param.
    for href in re.findall(r'href="([^"]*intent/tweet[^"]*)"', text):
        decoded = unquote(href)
        # Brittle exact counts (full-width comma) that have appeared before.
        assert "7,146" not in decoded, "Found stale exact count 7,146 in share URL"
        assert "7,162" not in decoded, "Embed rounded counts (7,000+), not exact"
        assert "7,000" in decoded, "Share URL should mention 7,000+ diseases"


# ---------------------------------------------------------------------------
# app.js — keyboard shortcut wiring
# ---------------------------------------------------------------------------
def test_slash_shortcut_targets_existing_search_input_id():
    """The `/` shortcut focuses the global search box. The element ID
    in the DOM is `globalSearch`; we previously looked up `globalSearchInput`,
    which silently no-op'd."""
    js = _read("static/js/app.js")
    header = _read("templates/partials/_header.html")

    # Verify the DOM input id we expect to focus.
    assert 'id="globalSearch"' in header

    # Locate the `/` key handler and assert it references the right id.
    match = re.search(r'e\.key==="/"[^}]+\}', js)
    assert match, "Could not locate `/` keyboard shortcut handler"
    handler = match.group(0)
    assert 'getElementById("globalSearch")' in handler
    assert "globalSearchInput" not in handler, "Keyboard shortcut still references non-existent #globalSearchInput"


# ---------------------------------------------------------------------------
# Service worker cache version
# ---------------------------------------------------------------------------
def test_service_worker_cache_name_is_versioned():
    sw = _read("static/sw.js")
    m = re.search(r"CACHE_NAME\s*=\s*['\"]vetdict-v(\d+)['\"]", sw)
    assert m, "sw.js must declare CACHE_NAME = 'vetdict-vN'"
    # We never want the cache version to slide backwards.
    assert int(m.group(1)) >= 36, (
        "CACHE_NAME must be bumped (>= v36) so returning users pick up manifest/share-text fixes."
    )
