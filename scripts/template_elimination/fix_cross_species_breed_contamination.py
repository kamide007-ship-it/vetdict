"""Remove cross-species breed contamination and the frozen "cardiovascular"
English aetiology organ from the disease database.

Two data bugs fixed here:

1. Cross-species breed clauses. Category templates embed dog- (and a few cat-)
   breed predispositions — the neurological aetiology template names
   "Border Collie storm anxiety", the cardiac prevention template lists
   Doberman/Cocker Spaniel/Maine Coon, the respiratory templates cite
   "brachycephalic airway syndrome". Applied to unrelated species these become
   contamination a clinician spots instantly (a horse's lameness aetiology
   citing Collie CDS; a rabbit's DCM prognosis warning about Dobermans).
   ``filter_species_inapplicable_clauses`` replaces each exact template fragment
   with a species-neutral (or removed) version for species the breed does not
   apply to. Dog/cat records are untouched.

2. Frozen organ in the degenerative English ``causes``. The exotic generator
   froze the organ word to "cardiovascular" for every degenerative English
   aetiology, so Cataracts / Osteoarthritis / Chronic Kidney Disease etc. all
   read "…deterioration of cardiovascular tissues…". ``correct_degenerative_organ_en``
   substitutes the organ the disease name denotes (ocular, musculoskeletal,
   renal, …). Genuinely cardiac diseases are left unchanged.

Run with::

    python3 scripts/template_elimination/fix_cross_species_breed_contamination.py --apply

Then regenerate the delivery DB with ``python3 scripts/migrate_to_sqlite.py``.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts" / "template_elimination"))

from clinical_fields_generator import (  # noqa: E402
    correct_degenerative_organ_en,
    filter_species_inapplicable_clauses,
)

JSON_PATH = ROOT / "diseases_all_species.json"
SUPPLEMENTARY_PATH = ROOT / "api" / "data" / "supplementary_diseases.json"

# Every free-text clinical field, both languages. The breed filter is a no-op on
# fields that contain none of its fragments, so listing them all is safe.
TEXT_FIELDS = (
    "causes",
    "causes_ja",
    "pathophysiology",
    "pathophysiology_ja",
    "prognosis",
    "prognosis_ja",
    "prevention",
    "prevention_ja",
    "clinical_signs",
    "clinical_signs_ja",
    "description",
    "description_ja",
    "treatment",
    "treatment_ja",
    "transmission",
    "transmission_ja",
    "diagnosis",
    "diagnosis_ja",
    "differential_diagnosis",
    "differential_diagnosis_ja",
    "nutrition_management",
    "nutrition_management_ja",
    "prognosis_detailed",
    "prognosis_detailed_ja",
    "rehabilitation_protocol",
    "rehabilitation_protocol_ja",
)


def process_file(path: Path, apply: bool) -> tuple[int, int]:
    records = json.loads(path.read_text(encoding="utf-8"))
    breed_by_field: Counter[str] = Counter()
    organ_fixed = 0
    samples: list[str] = []

    for r in records:
        species = r.get("species", "")
        # 1. Frozen-organ correction on the English aetiology.
        causes = r.get("causes")
        if causes:
            new_causes = correct_degenerative_organ_en(r.get("name_ja", ""), r.get("name", ""), causes)
            if new_causes != causes:
                organ_fixed += 1
                if apply:
                    r["causes"] = new_causes
                causes = new_causes

        # 2. Cross-species breed-clause filter on every text field.
        for f in TEXT_FIELDS:
            v = r.get(f)
            if not v:
                continue
            new = filter_species_inapplicable_clauses(v, species)
            if new != v:
                breed_by_field[f] += 1
                if len(samples) < 8:
                    samples.append(f"[{species}] .{f}: …{new[:70]}…")
                if apply:
                    r[f] = new

    breed_total = sum(breed_by_field.values())
    print(f"\n{path.name}:")
    print(f"  frozen-organ English aetiology corrected: {organ_fixed}")
    print(f"  breed-clause fields cleaned: {breed_total} across {len(breed_by_field)} fields")
    print("    by field:", dict(breed_by_field.most_common()))
    for s in samples:
        print("   ", s)

    if apply:
        if path == SUPPLEMENTARY_PATH:
            text = json.dumps(records, ensure_ascii=False, indent=2)
        else:
            text = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
        path.write_text(text, encoding="utf-8")

    return organ_fixed, breed_total


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="write changes (default: dry run)")
    args = ap.parse_args()

    total_organ = total_breed = 0
    for path in (JSON_PATH, SUPPLEMENTARY_PATH):
        if not path.exists():
            continue
        o, b = process_file(path, args.apply)
        total_organ += o
        total_breed += b

    print(f"\n=== TOTAL: {total_organ} organ fixes, {total_breed} breed-clause fields ===")
    if not args.apply:
        print("(dry run — pass --apply to write)")


if __name__ == "__main__":
    main()
