#!/usr/bin/env python3
"""Build stable disease-id lock sidecars (Phase 2 quality program).

For each dict-based species module, freeze the id each disease has *today*
(position-derived, matching ``scripts/migrate_to_sqlite.py``) into
``api/data/id_locks/<species>.json`` keyed by content identity (name/name_ja).

Semantics (safe by construction)
--------------------------------
* **Append-only freeze.** An existing key's id is NEVER changed. New diseases
  get the current position id if free, else a content-hash id to avoid clash.
* **Idempotent.** Re-running on unchanged data produces an identical file.
* **Non-destructive.** Reads modules read-only; writes only the sidecar.
* Horse/equine is skipped — it already carries explicit stable ids.

Usage::

    python3 -m scripts.quality.build_id_locks            # all dict species
    python3 -m scripts.quality.build_id_locks degu       # one species
    python3 -m scripts.quality.build_id_locks --check    # verify, write nothing
"""

from __future__ import annotations

import hashlib
import importlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from api.species.id_locks import stable_key  # noqa: E402

LOCK_DIR = ROOT / "api" / "data" / "id_locks"

# Dict-based species (position-derived ids). Mirrors migrate_to_sqlite's
# SPECIES_MODULES + the dedicated dog module. Horse is intentionally excluded.
SPECIES_MODULES = {
    "cat": "api.species.cat_diseases",
    "rabbit": "api.species.rabbit_diseases",
    "bird": "api.species.bird_diseases",
    "hamster": "api.species.hamster_diseases",
    "guinea_pig": "api.species.guinea_pig_diseases",
    "ferret": "api.species.ferret_diseases",
    "hedgehog": "api.species.hedgehog_diseases",
    "chinchilla": "api.species.chinchilla_diseases",
    "reptile": "api.species.reptile_diseases",
    "snake": "api.species.snake_diseases",
    "lizard": "api.species.lizard_diseases",
    "tortoise": "api.species.tortoise_diseases",
    "parakeet": "api.species.parakeet_diseases",
    "parrot": "api.species.parrot_diseases",
    "amphibian": "api.species.amphibian_diseases",
    "fish": "api.species.fish_diseases",
    "degu": "api.species.degu_diseases",
    "sugar_glider": "api.species.sugar_glider_diseases",
    "exotic_other": "api.species.exotic_other_diseases",
    "dog": "api.species.dog_diseases",
}


def _current_ids(species_key: str, module_path: str) -> list[tuple[str, str]]:
    """Return [(stable_key, current_position_id), ...] exactly as migrate assigns.

    Replicates migrate_to_sqlite.migrate_species_diseases: dedupe the raw list
    but keep each kept entry's ORIGINAL index so generated ids stay stable.
    """
    mod = importlib.import_module(module_path)
    raw = getattr(mod, "DISEASES", [])
    try:
        from api.species.helpers import dedupe_disease_list

        diseases = dedupe_disease_list(raw)
    except Exception:
        diseases = raw
    orig_index = {id(e): i for i, e in enumerate(raw)}
    out = []
    for d in diseases:
        i = orig_index.get(id(d), 0)
        disease_id = (d.get("id") if isinstance(d, dict) else None) or f"{species_key}_{i:04d}"
        out.append((stable_key(d), disease_id))
    return out


def build_species(species_key: str, module_path: str, check: bool) -> tuple[int, int, int]:
    """Build/update one species lock. Returns (total, kept_frozen, newly_added)."""
    path = LOCK_DIR / f"{species_key}.json"
    existing = {}
    if path.exists():
        try:
            existing = json.loads(path.read_text(encoding="utf-8")).get("locks", {})
        except (OSError, ValueError):
            existing = {}

    locks = dict(existing)  # start from frozen state (append-only)
    taken = set(locks.values())
    kept = added = 0

    for key, cur_id in _current_ids(species_key, module_path):
        if key in locks:
            kept += 1
            continue
        # New disease: prefer its current position id; if that id is already
        # claimed by a frozen key (positions shifted), mint a content-hash id.
        new_id = cur_id
        if new_id in taken:
            h = hashlib.sha1(f"{species_key}:{key}".encode()).hexdigest()[:8]
            new_id = f"{species_key}_x{h}"
        locks[key] = new_id
        taken.add(new_id)
        added += 1

    payload = {
        "species": species_key,
        "schema_version": 1,
        "note": (
            "Frozen disease ids (name→id). Append-only: existing mappings are "
            "never changed. Delete to fall back to position-derived ids."
        ),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "count": len(locks),
        "locks": dict(sorted(locks.items())),
    }

    if not check:
        LOCK_DIR.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return len(locks), kept, added


def main(argv: list[str]) -> int:
    check = "--check" in argv
    args = [a for a in argv if not a.startswith("--")]
    targets = args or list(SPECIES_MODULES)

    grand_total = grand_new = 0
    for sp in targets:
        if sp not in SPECIES_MODULES:
            print(f"  skip {sp}: not a dict-based species (horse already has stable ids)")
            continue
        total, kept, added = build_species(sp, SPECIES_MODULES[sp], check)
        grand_total += total
        grand_new += added
        verb = "check" if check else "wrote"
        print(f"  {verb} {sp}: {total} locks ({kept} frozen kept, {added} new)")
    print(f"total locked ids: {grand_total} ({grand_new} newly assigned)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
