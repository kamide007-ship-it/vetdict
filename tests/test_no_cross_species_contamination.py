"""CI regression guard: no disease record may carry a *foreign* species'
"<species>における…" framing (cross-species contamination).

An earlier enrichment pass copied Japanese content between species classes and
stamped the wrong "<Species>における" label on it (e.g. a hamster Diabetes entry
framed as "オウムにおける…"). All such contamination was eliminated in the
2026-07 quality pass; this test freezes that at zero so the bug cannot silently
return via a future enrichment/import.

The scanner (scripts/quality/scan_cross_species.py) is read-only and reused
here verbatim — the test asserts it finds nothing.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.quality.scan_cross_species import scan  # noqa: E402


@pytest.fixture(scope="module")
def report() -> dict:
    return scan()


def test_no_cross_species_contamination(report: dict) -> None:
    """Zero fields may carry a foreign-species 'における' framing."""
    offenders = {
        sp: [f"{h['name']}.{h['field']} (→{h['foreign_label']})" for h in hits]
        for sp, hits in report.items()
        if hits
    }
    total = sum(len(v) for v in offenders.values())
    assert total == 0, (
        f"{total} cross-species contaminated field(s) detected — a species record "
        f"carries another species' 'における' framing. Fix with the batch relabel/"
        f"clinical scripts under scripts/quality/. Offenders: {offenders}"
    )


def test_no_cross_class_contamination(report: dict) -> None:
    """Cross-class contamination (mammal<->bird<->reptile<->amphibian) is the
    highest-severity form; guard it explicitly with a clearer message."""
    cross = [
        f"{sp}: {h['name']}.{h['field']} (→{h['foreign_label']})"
        for sp, hits in report.items()
        for h in hits
        if h["severity"] == "cross-class"
    ]
    assert not cross, f"cross-class contamination detected: {cross}"
