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
