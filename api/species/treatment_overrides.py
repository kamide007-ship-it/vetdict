"""Treatment dosage publish gate (T105/T106) — fail-closed.

Dosage protocols are patient-safety critical. This module enforces the SPEC
rule "投与量は必ず出典付き・公開前に獣医師レビュー・自動公開しない":

- Drafts live in ``api/data/treatment_overrides/<species>.json`` with a
  ``review_status`` of ``draft`` / ``approved`` / ``published``.
- **Only ``published`` entries ever reach the served view.** ``draft`` and
  ``approved`` entries are held back — they are never shown to users until a
  veterinarian explicitly sets ``published`` AND every dosage carries a source.
- An entry that is ``published`` but has no ``sources`` is refused (fail-closed),
  so a dose can never go live uncited even by mistake.

The generator (``scripts/quality/build_treatment_drafts.py``) only creates
``draft`` entries and NEVER fabricates doses. Publishing is a human action.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

_DIR = Path(__file__).resolve().parent.parent / "data" / "treatment_overrides"


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")


def _name_of(d: Any) -> str:
    if isinstance(d, dict):
        return d.get("name") or d.get("name_en") or ""
    return getattr(d, "name", "") or getattr(d, "name_en", "") or ""


@lru_cache(maxsize=32)
def load_overrides(species: str) -> dict | None:
    path = _DIR / f"{species}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


@lru_cache(maxsize=32)
def _published_index(species: str) -> dict[str, dict]:
    """slug -> published override, fail-closed (published + has sources only)."""
    data = load_overrides(species)
    if not data:
        return {}
    out: dict[str, dict] = {}
    for entry in data.get("entries", []):
        if entry.get("review_status") != "published":
            continue
        # Fail-closed: never serve a published dose without a citation.
        if not entry.get("sources"):
            continue
        slug = entry.get("slug")
        if slug and (entry.get("treatment_ja") or entry.get("treatment")):
            out[slug] = entry
    return out


def apply_treatment_overrides(diseases: list[Any], species: str) -> list[Any]:
    """Overlay veterinarian-published dosage text onto the served list.

    Only entries with ``review_status == "published"`` and at least one source
    are applied. Drafts/approved are ignored. Non-mutating (dicts copied only
    when overridden). Safe no-op when no published overrides exist.
    """
    pub = _published_index(species)
    if not pub or not diseases:
        return diseases
    out: list[Any] = []
    for d in diseases:
        if isinstance(d, dict):
            ov = pub.get(_slug(_name_of(d)))
            if ov:
                d = dict(d)
                if ov.get("treatment_ja"):
                    d["treatment_ja"] = ov["treatment_ja"]
                if ov.get("treatment"):
                    d["treatment"] = ov["treatment"]
                d["treatment_sources"] = ov.get("sources", [])
                d["treatment_reviewed"] = True
        out.append(d)
    return out
