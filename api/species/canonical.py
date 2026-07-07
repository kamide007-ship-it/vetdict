"""Canonical consolidation layer (T103) — non-destructive logical merge.

Disease sources (Python modules / JSON overlays) are never physically edited.
Instead, ``api/data/canonical/<species>.json`` (produced by
``scripts/quality/build_canonical.py`` and reviewed by a veterinarian) declares:

- ``merges``  : duplicate entries that collapse into one canonical entry. The
  canonical keeps its (clean) name; the merged entries are hidden from the
  served list and their old URLs 301-redirect to the canonical slug. The
  canonical inherits richer content from its merged siblings at load time.
- ``archives``: entries removed from the served list (e.g. research models).
- ``review``  : proposals awaiting veterinarian sign-off; NOT applied here.

Applied at load time on every serving path, so it works even on the 512 MB
production tier where SQLite is skipped and modules/overlays serve directly.
Fully reversible: delete or edit the map file.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

_CANON_DIR = Path(__file__).resolve().parent.parent / "data" / "canonical"

# Content fields a canonical entry may inherit from a richer merged sibling.
_CONTENT_FIELDS = (
    "description",
    "description_ja",
    "causes",
    "causes_ja",
    "pathophysiology",
    "pathophysiology_ja",
    "treatment",
    "treatment_ja",
    "prevention",
    "prevention_ja",
    "prognosis",
    "prognosis_ja",
    "recommended_tests",
)


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")


def _name_of(d: Any) -> str:
    if isinstance(d, dict):
        return d.get("name") or d.get("name_en") or ""
    return getattr(d, "name", "") or getattr(d, "name_en", "") or ""


def _get(d: Any, key: str, default: str = "") -> Any:
    if isinstance(d, dict):
        return d.get(key, default)
    return getattr(d, key, default)


@lru_cache(maxsize=32)
def load_canonical(species: str) -> dict | None:
    """Return the canonical map for *species*, or None if none exists."""
    path = _CANON_DIR / f"{species}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


@lru_cache(maxsize=32)
def _redirect_index(species: str) -> dict[str, str]:
    """merged/aliased slug -> canonical slug (for URL redirects)."""
    cm = load_canonical(species)
    if not cm:
        return {}
    idx: dict[str, str] = {}
    for mg in cm.get("merges", []):
        cslug = mg.get("canonical", {}).get("slug")
        if not cslug:
            continue
        for m in mg.get("merged", []):
            if m.get("slug"):
                idx[m["slug"]] = cslug
    return idx


def resolve_redirect(species: str, slug: str) -> str | None:
    """Return the canonical slug a merged/old slug should redirect to, or None."""
    return _redirect_index(species).get(slug)


def _inherit_content(canonical: dict, siblings: list[Any]) -> dict:
    """Return a copy of *canonical* whose empty/shorter content fields are
    filled from the richer merged siblings. Non-mutating."""
    out = dict(canonical)
    for field in _CONTENT_FIELDS:
        best = out.get(field)
        best_len = len(str(best or ""))
        for sib in siblings:
            val = _get(sib, field, "")
            if val and len(str(val)) > best_len:
                best, best_len = val, len(str(val))
        if best:
            out[field] = best
    return out


def apply_canonical_map(diseases: list[Any], species: str) -> list[Any]:
    """Apply the canonical map to a served disease list.

    Hides archived and merged-away entries, and lets each canonical inherit
    richer content from its merged siblings. Input is not mutated (dict entries
    are copied only when their content changes). Safe no-op when no map exists.
    """
    cm = load_canonical(species)
    if not cm or not diseases:
        return diseases

    canonical_slugs: set[str] = set()
    redirect: dict[str, str] = {}
    inherit: dict[str, list[str]] = {}
    for mg in cm.get("merges", []):
        cslug = mg.get("canonical", {}).get("slug")
        if not cslug:
            continue
        canonical_slugs.add(cslug)
        for m in mg.get("merged", []):
            mslug = m.get("slug")
            if mslug:
                redirect[mslug] = cslug
                inherit.setdefault(cslug, []).append(mslug)

    archived = {a.get("slug") for a in cm.get("archives", []) if a.get("slug")}
    if not archived and not redirect:
        return diseases

    by_slug: dict[str, Any] = {}
    for d in diseases:
        by_slug.setdefault(_slug(_name_of(d)), d)

    # Never drop a slug that is itself a canonical target — an identical-name
    # cluster (dedup already collapsed) can list the same slug on both sides.
    dropped = (archived | set(redirect)) - canonical_slugs
    out: list[Any] = []
    for d in diseases:
        s = _slug(_name_of(d))
        if s in dropped:
            continue
        if s in inherit and isinstance(d, dict):
            siblings = [by_slug[ms] for ms in inherit[s] if ms in by_slug]
            if siblings:
                d = _inherit_content(d, siblings)
        out.append(d)
    return out
