#!/usr/bin/env python3
"""Build a lightweight cross-species disease search index.

The full disease database is too large to migrate into SQLite on a 512 MB
host (peak ~535 MB RSS when every species module is imported at once), so
low-memory deploys keep the SQLite ``diseases`` table empty and serve
per-species browsing from the Python modules one at a time.

That leaves cross-species search (``GET /api/diseases?q=``) with no backing
store.  This script produces a compact name index — ``id``, ``species``,
``name``, ``name_ja`` and ``urgency`` for every disease — that
``api.disease_store.search_diseases`` falls back to when SQLite is empty.

Two modes:

* ``--species <key>``  Emit the index entries for ONE species as JSON to
  stdout.  Importing a single module peaks at ~50-80 MB, so this is the
  memory-safe unit used both here and by the runtime fallback.
* (no args)            Orchestrate: run this script once per species in a
  separate subprocess, accumulate the results, and write
  ``api/data/disease_search_index.json``.  Spawning a fresh interpreter per
  species keeps peak RSS bounded to a single module.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
_OUTPUT_PATH = _REPO_ROOT / "api" / "data" / "disease_search_index.json"

if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# species key -> (module path, diseases attribute)
SPECIES_MODULE_MAP: dict[str, tuple[str, str]] = {
    "dog": ("api.species.dog_diseases", "DISEASES"),
    "horse": ("api.species.equine_diseases", "DISEASE_DATABASE"),
    "cat": ("api.species.cat_diseases", "DISEASES"),
    "rabbit": ("api.species.rabbit_diseases", "DISEASES"),
    "hamster": ("api.species.hamster_diseases", "DISEASES"),
    "guinea_pig": ("api.species.guinea_pig_diseases", "DISEASES"),
    "chinchilla": ("api.species.chinchilla_diseases", "DISEASES"),
    "ferret": ("api.species.ferret_diseases", "DISEASES"),
    "hedgehog": ("api.species.hedgehog_diseases", "DISEASES"),
    "sugar_glider": ("api.species.sugar_glider_diseases", "DISEASES"),
    "degu": ("api.species.degu_diseases", "DISEASES"),
    "bird": ("api.species.bird_diseases", "DISEASES"),
    "parakeet": ("api.species.parakeet_diseases", "DISEASES"),
    "parrot": ("api.species.parrot_diseases", "DISEASES"),
    "reptile": ("api.species.reptile_diseases", "DISEASES"),
    "tortoise": ("api.species.tortoise_diseases", "DISEASES"),
    "snake": ("api.species.snake_diseases", "DISEASES"),
    "lizard": ("api.species.lizard_diseases", "DISEASES"),
    "amphibian": ("api.species.amphibian_diseases", "DISEASES"),
    "fish": ("api.species.fish_diseases", "DISEASES"),
    "exotic_other": ("api.species.exotic_other_diseases", "DISEASES"),
}


def _attr(obj, key: str, default=""):
    """Read a field from either a dict or a dataclass-style object."""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def build_species_entries(species: str) -> list[dict]:
    """Return compact index entries for a single species' disease module."""
    import importlib

    module_path, attr = SPECIES_MODULE_MAP[species]
    mod = importlib.import_module(module_path)
    diseases = getattr(mod, attr, []) or []

    entries: list[dict] = []
    for i, d in enumerate(diseases):
        # Horse uses a dataclass with name_en/name_ja; other species use
        # dicts with name/name_ja.  Mirror migrate_to_sqlite.py's id scheme.
        name = _attr(d, "name_en", "") or _attr(d, "name", "")
        name_ja = _attr(d, "name_ja", "") or name
        urgency = _attr(d, "urgency", "") or _attr(d, "severity", "") or ""
        disease_id = _attr(d, "id", "") or f"{species}_{i:04d}"
        if not name and not name_ja:
            continue
        entries.append(
            {
                "id": disease_id,
                "species": species,
                "name": name,
                "name_ja": name_ja,
                "urgency": urgency,
            }
        )
    return entries


def build_full_index() -> list[dict]:
    """Build the whole index, one species per subprocess to bound memory."""
    all_entries: list[dict] = []
    for species in SPECIES_MODULE_MAP:
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).resolve()), "--species", species],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(_REPO_ROOT),
        )
        if proc.returncode != 0:
            raise RuntimeError(f"index build failed for {species}: {proc.stderr.strip()[:300]}")
        all_entries.extend(json.loads(proc.stdout))
    return all_entries


def main(argv: list[str]) -> int:
    if len(argv) >= 2 and argv[0] == "--species":
        species = argv[1]
        if species not in SPECIES_MODULE_MAP:
            print(f"unknown species: {species}", file=sys.stderr)
            return 2
        json.dump(build_species_entries(species), sys.stdout, ensure_ascii=False)
        return 0

    entries = build_full_index()
    _OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    _OUTPUT_PATH.write_text(json.dumps(entries, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {len(entries)} disease index entries to {_OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
