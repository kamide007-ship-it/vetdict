"""Upgrade generic English ``causes`` templates to category-resolved parity text.

The English ``causes`` field historically carried a single contentless catch-all
("Multifactorial etiology depending on disease type.") for hundreds of diseases,
plus English category templates out of sync with the (correct) Japanese category.
This pass replaces those generic templates with ``gen_causes`` (EN) text resolved
to the same category the reviewed Japanese ``causes_ja`` already uses — so the
English reader sees the correct, category-appropriate aetiology instead of
boilerplate. See ``generic_english_causes`` for the full rationale and guards.

Named-agent diseases (owned by ``fix_named_pathogens``) are skipped, so no
pathogen-specific prose is overwritten. Curated English causes (not a recognised
generic template) are left untouched.

Run with ``--apply`` to write ``diseases_all_species.json``; default is a dry run.
The served-DB safety net ``ground_english_causes_to_category`` in
``migrate_to_sqlite.py`` applies the same correction to module-sourced records.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.eliminate_templates import SPECIES_NORM  # noqa: E402
from scripts.template_elimination.generic_english_causes import (  # noqa: E402
    upgrade_english_causes,
)

JSON_PATH = ROOT / "diseases_all_species.json"


def remediate(data: list[dict], apply: bool) -> dict:
    stats = {"causes": 0, "diseases": 0}
    examples: list[str] = []
    for entry in data:
        name_ja = entry.get("name_ja") or ""
        name_en = entry.get("name") or ""
        raw_species = entry.get("species", "")
        species = SPECIES_NORM.get(raw_species, (raw_species or "").lower())
        new = upgrade_english_causes(
            species,
            name_ja,
            name_en,
            entry.get("causes_ja") or "",
            entry.get("causes") or "",
            entry.get("category") or "",
        )
        if new is None:
            continue
        stats["causes"] += 1
        stats["diseases"] += 1
        if apply:
            entry["causes"] = new
        if len(examples) < 20:
            examples.append(f"[{raw_species}] {name_en or name_ja}")
    stats["_examples"] = examples
    return stats


def main() -> None:
    apply = "--apply" in sys.argv
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    stats = remediate(data, apply)
    examples = stats.pop("_examples")
    print(f"Generic English causes upgraded to category parity: {stats['causes']}")
    if examples:
        print("  e.g. " + ", ".join(examples[:12]))
    if apply:
        with JSON_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        print(f"Wrote {JSON_PATH}")
    else:
        print("Dry run — pass --apply to write.")


if __name__ == "__main__":
    main()
