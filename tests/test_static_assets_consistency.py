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
    # start_url may include utm_source query for analytics tracking
    assert data["start_url"].startswith("/")
    shortcuts = data.get("shortcuts") or []
    # Must list every primary tab so PWA users can deep-link from the
    # home-screen shortcut menu. Tracking params (utm_source) are allowed.
    fragments = {s["url"].split("#")[-1] for s in shortcuts if "#" in s["url"]}
    for required in ("checker", "database", "chat", "drugs", "anesthesia"):
        assert required in fragments, f"PWA shortcut missing for #{required}"


def test_manifest_has_no_stale_counts():
    text = _read("static/manifest.json")
    # Old counts that historically drifted out of sync with the live DB.
    # Each represents a regression we don't want to reintroduce.
    assert "220+薬品" not in text, "Stale drug count (220+) — current is 630+"
    assert "194薬品" not in text, "Stale drug count (194) — current is 630+"
    # 2026-08: the duplicate-card merge (dedupe round 2) brought the browsable
    # corpus to ~6.9k rows / 6.4k cross-species entries, so the truthful rounded
    # claim moved DOWN from 7,000+ to 6,400+. Never re-inflate past the number
    # a user can actually browse.
    assert "7,000+疾患" not in text, "Inflated disease count (7,000+) — current truthful claim is 6,400+"
    assert "6,500+疾患" not in text, "Stale disease count (6,500+) — current truthful claim is 6,400+"


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
        assert "7,162" not in decoded, "Embed rounded counts, not exact"
        # 2026-08 dedupe round 2: truthful rounded claim is 6,400+ (see
        # test_disease_count_truthful.py for the advertised==browsable invariant).
        assert "7,000" not in decoded, "Inflated count (7,000+) — current truthful claim is 6,400+"
        assert "6,400" in decoded, "Share URL should mention 6,400+ diseases"


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
# app.js — disease search must not lurch the mobile page while typing
# ---------------------------------------------------------------------------
def test_disease_search_input_pins_scroll_anchor():
    """On mobile the disease list is in normal document flow (max-height:none),
    so re-rendering it on each keystroke changed the document height and made the
    page jump up and down. The debounced search handler must route its re-render
    through _renderPinningAnchor so the search box stays put while typing."""
    js = _read("static/js/app.js")

    # The helper must exist and correct the scroll after the render.
    assert "function _renderPinningAnchor(" in js, "scroll-pinning helper is missing"
    assert "window.scrollBy(0, delta)" in js, "_renderPinningAnchor must restore scroll position with window.scrollBy"

    # The disease search input handler must use it (not call renderDiseaseDb bare).
    assert 'diseaseSearch.addEventListener("input"' in js, "Could not locate the disease search input handler"
    assert "_renderPinningAnchor(diseaseSearch,renderDiseaseDb)" in js, (
        "disease search handler must pin the scroll anchor while re-rendering"
    )


# ---------------------------------------------------------------------------
# app.js — expanding a disease detail must not drift the mobile page
# ---------------------------------------------------------------------------
def test_disease_detail_expand_does_a_single_scroll():
    """Expanding a disease/drug/anaesthesia detail scrolls it to a reading
    position once. It must NOT run scrollToAnchor's 12s re-anchoring watcher
    (which chased the async drug tables and drifted the page up and down on
    mobile), and focus() must not scroll-into-view."""
    js = _read("static/js/app.js")

    match = re.search(r"function toggleDbItem\(el\)\{.*?\n\}", js, re.S)
    assert match, "Could not locate toggleDbItem"
    body = match.group(0)
    assert "scrollToAnchor(el,{settle:false})" in body, (
        "detail expansion must use a one-shot scroll (settle:false), not the 12s watcher"
    )
    assert "focus({preventScroll:true})" in body, "detail expansion focus() must not scroll-into-view"


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
