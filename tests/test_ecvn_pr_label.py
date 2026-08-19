"""T107 — the ECVN sponsor block must render as a clearly labelled PR/own-product
note, never as (or mistakeable for) standard evidence-based treatment."""

from __future__ import annotations

from api.data.sponsor_adjuncts import apply_sponsor_adjuncts_dict
from api.vetdict_api import _render_treatment_adjunct_html


def _block_disease():
    d = {
        "name": "Osteoarthritis",
        "name_ja": "変形性関節症",
        "treatment_ja": "標準治療: メロキシカム 0.1 mg/kg PO q24h。",
        "treatment": "Standard: meloxicam 0.1 mg/kg PO q24h.",
    }
    apply_sponsor_adjuncts_dict(d, "dog")
    return d


def test_data_header_is_pr_labelled():
    d = _block_disease()
    assert "[ECVN:Block]" in d["treatment_ja"]
    assert "PR・自社製品" in d["treatment_ja"]
    assert "標準治療ではありません" in d["treatment_ja"]


def test_server_render_shows_pr_block_not_marker():
    d = _block_disease()
    html = str(_render_treatment_adjunct_html(d["treatment_ja"]))
    # marker never leaks to the page
    assert "[ECVN:Block]" not in html
    # explicit PR badge + label + disclaimer
    assert "ecvn-pr-badge" in html
    assert "PR・自社製品" in html
    assert "エビデンスに基づく治療ではありません" in html
    # the real treatment is preserved above the block
    assert "メロキシカム" in html
    # vendor link is present
    assert 'href="https://www.caninevet.jp/"' in html


def test_server_render_escapes_and_plain_passthrough():
    assert str(_render_treatment_adjunct_html("plain tx")) == "<p>plain tx</p>"
    assert "&lt;script&gt;" in str(_render_treatment_adjunct_html("<script>"))


def test_no_adjunct_treatment_has_no_pr_block():
    html = str(_render_treatment_adjunct_html("メロキシカム 0.1 mg/kg PO q24h。"))
    assert "ecvn-adjunct-block" not in html


def test_sponsor_block_is_collapsed_details_with_product_links():
    """2026-08 sponsor feedback: the block must not compete with treatment text
    (collapsed <details> by default) and each product name must link straight
    to its caninevet.jp product page."""
    from api.data.sponsor_adjuncts import _PRODUCTS, PRODUCT_URLS

    d = _block_disease()
    html = str(_render_treatment_adjunct_html(d["treatment_ja"]))
    assert "<details" in html and "</details>" in html
    assert "<summary" in html  # one-tap expand affordance
    # Every product mentioned in this block links to its own page.
    assert f'href="{PRODUCT_URLS["For Joint"]}"' in html
    # Sponsored links are labelled per Google guidance.
    assert 'rel="sponsored noopener noreferrer"' in html
    # The URL registry covers every product in the sponsor registry.
    names = {p.get("name_ja") for p in _PRODUCTS}
    # NMN registry name has no space; map key must match the block text form.
    assert names <= set(PRODUCT_URLS), names - set(PRODUCT_URLS)
    for url in PRODUCT_URLS.values():
        assert url.startswith("https://www.caninevet.jp/")


def test_app_js_mirrors_product_url_map_and_collapses_block():
    """The SPA renderer must mirror the canonical PRODUCT_URLS map and render
    the block as a collapsed <details> with linked product names."""
    from pathlib import Path

    from api.data.sponsor_adjuncts import PRODUCT_URLS

    js = (Path(__file__).resolve().parents[1] / "static" / "js" / "app.js").read_text(encoding="utf-8")
    assert "ECVN_PRODUCT_URLS" in js
    for name, url in PRODUCT_URLS.items():
        assert url in js, f"app.js missing URL for {name}"
    fn = js[js.index("function renderTreatmentWithAdjunct") :]
    fn = fn[: fn.index("\n}") + 2]
    assert "<details" in fn and "<summary" in fn
    assert "ECVN_PRODUCT_URLS" in fn
    assert 'rel="sponsored noopener noreferrer"' in fn
