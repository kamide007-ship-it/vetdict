"""Stable disease-id resolution (Phase 2 quality program).

Problem this solves
-------------------
Dict-based species modules (``api/species/<species>_diseases.py``) do **not**
carry an explicit ``id`` field. Their served id is derived from the entry's
*position* in the ``DISEASES`` list (``f"{species}_{i:04d}"`` in
``scripts/migrate_to_sqlite.py``). That makes every public URL fragile:
re-ordering or removing a list entry silently renumbers everything after it and
breaks existing links.

This module reads a per-species **id-lock sidecar**
(``api/data/id_locks/<species>.json``) that pins a content-stable identity
(``name`` / ``name_ja``) to the id that entry has *today*. Once frozen, the id
follows the disease even if the list is later re-ordered.

Design guarantees
-----------------
* **Pure / read-only.** No writes, no network. Safe to call anywhere.
* **Byte-identical today.** Locks are generated from the current ids, so for
  every existing entry ``stable_id_for`` returns exactly the id it already had.
  The benefit only manifests when the source list is later re-ordered.
* **Non-destructive & reversible.** Delete the sidecar and resolution falls
  back to the position-derived id (current behaviour).
* Horse/equine already carries an explicit ``id`` and is not locked here.
"""

from __future__ import annotations

import json
import os
from functools import lru_cache
from typing import Any

_LOCK_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "id_locks")

# Unit-separator: joins name + name_ja into one collision-resistant key without
# risking a clash with characters that appear in disease names.
_KEY_SEP = "␟"


def stable_key(entry: Any) -> str:
    """Content-stable identity for a disease entry (dict or object).

    Uses English ``name`` joined with ``name_ja``. Two entries only share a key
    when they are genuine duplicates (which the dedupe pass already collapses).
    """

    def _get(obj: Any, field: str) -> str:
        if isinstance(obj, dict):
            val = obj.get(field)
        else:
            val = getattr(obj, field, None)
        return (val or "").strip()

    name = _get(entry, "name") or _get(entry, "name_en")
    name_ja = _get(entry, "name_ja")
    return f"{name}{_KEY_SEP}{name_ja}"


@lru_cache(maxsize=None)
def _load_lock(species_key: str) -> dict:
    """Load and cache ``api/data/id_locks/<species>.json`` (``{key: id}``)."""
    path = os.path.join(_LOCK_DIR, f"{species_key}.json")
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {}
    return data.get("locks", {}) if isinstance(data, dict) else {}


def stable_id_for(species_key: str, entry: Any, fallback_id: str) -> str:
    """Return the frozen id for ``entry`` if locked, else ``fallback_id``.

    ``fallback_id`` is the caller's position-derived id — used unchanged when no
    lock file exists or the entry is new (not yet frozen).
    """
    locks = _load_lock(species_key)
    if not locks:
        return fallback_id
    return locks.get(stable_key(entry), fallback_id)


def locked_id_for(species_key: str, entry: Any) -> str | None:
    """Return the frozen id for ``entry``, or ``None`` when it is not locked.

    Unlike :func:`stable_id_for` this distinguishes "locked to exactly the
    position-derived id" from "not locked at all", which id-allocation code
    needs: a locked id is authoritative and must never be reassigned, while an
    unlocked entry's positional fallback may be bumped to avoid colliding with
    another entry's lock.
    """
    locks = _load_lock(species_key)
    if not locks:
        return None
    return locks.get(stable_key(entry))


def clear_cache() -> None:
    """Drop the in-process lock cache (for tests / after regenerating locks)."""
    _load_lock.cache_clear()
