"""Fix clinically dangerous category miscategorisations in the JSON overlay.

``diseases_all_species.json`` is the authoritative enrichment overlay: it is
overlaid onto the Python species modules at runtime (``helpers.enrich_diseases``)
AND drives the SQLite build. On the low-memory production deploy the SQLite
``diseases`` table is left empty (OOM guard) and per-species browsing serves the
module + JSON overlay directly — so a fix that lives only in the migration's
served-DB passes never reaches users. This script applies the same two
corrections to the JSON itself, in place:

1. **Curated dangerous-treatment replacements** — toxin-decontamination protocols
   on dysbiosis / ulcers / haemolytic anaemia and deworming protocols on a
   cerebral infarct / rectal prolapse, replaced with condition-specific,
   species-appropriate protocols (see ``curated_dangerous_treatments``).

2. **Etiology / pathophysiology re-categorisation** — ``causes_ja`` /
   ``pathophysiology_ja`` that carry the WRONG category template (e.g.
   arteriosclerosis or a cerebral disease described with a fracture cause,
   rickets described with a fracture cause, equine thrush described with a
   fracture cause) are re-rendered with the category resolved from the disease
   name (see ``clinical_fields_generator.resolve_category_from_name``).

Both corrections are idempotent: a re-run only rewrites entries that still match
a dangerous fingerprint / wrong-category template. Curated, disease-specific text
(no recognised template) is never touched.

Usage::

    python3 scripts/template_elimination/fix_category_miscategorization.py [--apply]

Followed by ``python3 scripts/migrate_to_sqlite.py`` (the served-DB passes then
find nothing left to fix) and
``python3 scripts/build_disease_search_index.py`` (names are unchanged, so this
is a no-op but keeps the artifact in sync).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    build_etiology_fingerprints,
    decide_etiology_category,
    fingerprint_etiology,
    gen_causes_ja,
    gen_pathophysiology_ja,
)
from scripts.template_elimination.curated_dangerous_treatments import (  # noqa: E402
    curated_dangerous_treatment,
)
from scripts.template_elimination.eliminate_templates import SPECIES_NORM  # noqa: E402

JSON_PATH = ROOT / "diseases_all_species.json"


def remediate(data: list[dict], apply: bool) -> dict:
    fps = {
        "causes_ja": (build_etiology_fingerprints(gen_causes_ja), gen_causes_ja),
        "pathophysiology_ja": (
            build_etiology_fingerprints(gen_pathophysiology_ja),
            gen_pathophysiology_ja,
        ),
    }

    stats = {"treatment": 0, "causes_ja": 0, "pathophysiology_ja": 0}
    treatment_examples: list[str] = []

    for entry in data:
        name_ja = entry.get("name_ja") or ""
        name_en = entry.get("name") or ""
        raw_species = entry.get("species", "")
        species = SPECIES_NORM.get(raw_species, (raw_species or "").lower())

        # 1. Curated dangerous-treatment replacement.
        tx = entry.get("treatment_ja") or ""
        new_tx = curated_dangerous_treatment(species, name_ja, name_en, tx)
        if new_tx:
            stats["treatment"] += 1
            if len(treatment_examples) < 20:
                treatment_examples.append(f"[{raw_species}] {name_ja or name_en}")
            if apply:
                entry["treatment_ja"] = new_tx

        # 2. Etiology / pathophysiology re-categorisation.
        for field, (fingerprints, gen_fn) in fps.items():
            text = entry.get(field) or ""
            applied = fingerprint_etiology(text, fingerprints)
            if applied is None:
                continue  # curated / disease-specific — leave alone
            target = decide_etiology_category(name_ja, name_en, applied)
            if target == applied:
                continue
            new = gen_fn(target, name_ja, species)
            if new and new != text:
                stats[field] += 1
                if apply:
                    entry[field] = new

    print(f"{'APPLIED' if apply else 'DRY-RUN'} JSON category remediation:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    if treatment_examples:
        print("\nCurated treatment replacements:")
        for ex in treatment_examples:
            print(f"  {ex}")
    return stats


def main() -> None:
    apply = "--apply" in sys.argv
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    remediate(data, apply)
    if apply:
        # Preserve the source's compact formatting so the diff is limited to the
        # changed field values (not a whole-file reformat).
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        print(f"\nWrote {JSON_PATH}")
    else:
        print("\n(dry-run; pass --apply to write)")


if __name__ == "__main__":
    main()
