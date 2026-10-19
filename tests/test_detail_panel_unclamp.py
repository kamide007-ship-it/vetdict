"""Regression tests for the "スマホで薬品を動物種から下にスクロールが進まない" report (2026-10).

Root cause: ``.disease-detail.open`` carries ``max-height:5000px`` +
``overflow-y:auto`` for the expand/collapse animation. Drugs whose expanded
panel exceeds 5,000px (meloxicam ≈6,500px, prednisolone ≈5,800px — any drug
with a long species-dose grid) silently became a *nested scroll container* on
mobile: a swipe over the 動物種別投与量 cards scrolled the panel's invisible
inner scrollbar instead of the page, so the page did not advance until the
~1,500px of hidden inner scroll was exhausted (reproduced with Playwright
touch: four full swipes moved the page 0px).

Fix: after the open animation finishes, ``_unclampDetailPanel`` lifts the cap
(``max-height:none``) so there is only ever one scroller — the page — and
``_clampDetailPanel`` strips the inline override before every close (direct
toggle, accordion close, ✕ button) so the collapse animation still works.
"""

import re
from pathlib import Path

APP_JS = Path(__file__).resolve().parent.parent / "static" / "js" / "app.js"
SW_JS = Path(__file__).resolve().parent.parent / "static" / "sw.js"


def _src():
    return APP_JS.read_text(encoding="utf-8")


class TestDetailPanelUnclamp:
    def test_unclamp_helper_lifts_max_height_after_open(self):
        src = _src()
        m = re.search(r"function _unclampDetailPanel\(detail\)\{(.*?)\n\}", src, re.S)
        assert m, "_unclampDetailPanel must exist"
        body = m.group(1)
        # Lifts the animation cap so the panel never becomes a nested scroller
        assert 'maxHeight="none"' in body
        # Only while the panel is still open (guards the async paths)
        assert 'classList.contains("open")' in body
        # transitionend can be skipped (reduced motion / hidden tab): a timer
        # fallback longer than the 0.4s animation must still lift the cap
        assert "transitionend" in body
        assert re.search(r"setTimeout\([^)]*\)", body) or "setTimeout(" in body

    def test_clamp_helper_strips_inline_override(self):
        src = _src()
        m = re.search(r"function _clampDetailPanel\(detail\)\{(.*?)\n\}", src, re.S)
        assert m, "_clampDetailPanel must exist"
        body = m.group(1)
        # Clearing the inline style restores the CSS animation values; leaving
        # max-height:none inline would make the panel impossible to close
        assert 'maxHeight=""' in body

    def test_toggle_db_item_wires_unclamp_and_clamp(self):
        src = _src()
        m = re.search(r"function toggleDbItem\(el\)\{(.*?)\n\}\n", src, re.S)
        assert m, "toggleDbItem must exist"
        body = m.group(1)
        assert "_unclampDetailPanel(detail)" in body
        # clamp before the closing toggle so the collapse transition can run
        assert "_clampDetailPanel(detail)" in body
        # accordion close of the previously open sibling must clamp too
        assert "_clampDetailPanel(od)" in body

    def test_toggle_detail_wires_unclamp_and_clamp(self):
        src = _src()
        m = re.search(r"function toggleDetail\(head\)\{(.*?)\n\}\n", src, re.S)
        assert m, "toggleDetail must exist"
        body = m.group(1)
        assert "_unclampDetailPanel(detail)" in body
        assert "_clampDetailPanel(detail)" in body

    def test_service_worker_version_bumped(self):
        sw = SW_JS.read_text(encoding="utf-8")
        m = re.search(r"CACHE_NAME = 'vetdict-v(\d+)'", sw)
        assert m and int(m.group(1)) >= 185
