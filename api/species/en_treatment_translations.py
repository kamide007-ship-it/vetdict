"""English mirrors of Japanese-only curated treatment protocols (2026-10 第71弾).

Some JA-first records (mainly horse toxicoses / GI / renal entries and two
canine neonatal entries) carry a detailed curated Japanese treatment protocol
but no English equivalent: the English JSON alternative was a generic category
template that the template guards correctly reject, so the English UI fell
back to showing the Japanese protocol.

``api/data/treatment_en_translations.json`` holds faithful English
translations of those *already-published* Japanese protocols. They add no new
clinical content: every numeric token (doses, rates, durations, thresholds) is
verified to be identical to the Japanese source when the file is generated
(scripts/template_elimination/apply_en_treatment_translations.py) and again by
tests. They only fill an English treatment field that is empty or
predominantly Japanese — curated English text is never replaced.
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

_PATH = Path(__file__).resolve().parent.parent / "data" / "treatment_en_translations.json"
_CJK = re.compile(r"[぀-ヿ一-鿿]")


@lru_cache(maxsize=1)
def _table() -> dict[str, str]:
    try:
        data = json.loads(_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {k: v for k, v in (data.get("entries") or {}).items() if isinstance(v, str) and v}


@lru_cache(maxsize=1)
def _ja_table() -> dict[str, str]:
    try:
        data = json.loads(_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {k: v for k, v in (data.get("ja_entries") or {}).items() if isinstance(v, str) and v}


def ja_treatment_upgrade(species: str, name: str, current: str | None) -> str | None:
    """Detailed curated Japanese protocol for records whose JA field is shorter.

    Some records held their detailed Japanese protocol only in the English
    column (the JA column carried a short or generic text). Returns the
    detailed version only when it is substantially longer than ``current``.
    """
    rich = _ja_table().get(f"{(species or '').lower()}|{name or ''}")
    if not rich:
        return None
    cur = (current or "").split("[ECVN:Block]")[0].strip()
    body = rich.split("[ECVN:Block]")[0].strip()
    return rich if len(body) > 1.5 * len(cur) else None


def is_mostly_japanese(text: str | None) -> bool:
    if not text:
        return False
    return len(_CJK.findall(text)) > len(text) * 0.3


def en_treatment_for(species: str, name: str) -> str | None:
    return _table().get(f"{(species or '').lower()}|{name or ''}")


def needs_en_treatment(current: str | None) -> bool:
    """True when the English treatment field is empty or predominantly Japanese."""
    return not (current or "").strip() or is_mostly_japanese(current)
