"""Replace template-shaped clinical fields with disease-specific content.

For each disease entry, detect which non-treatment JA clinical fields are
filled with category-level templates (i.e. text shared verbatim by many other
entries) and regenerate disease-specific replacements using
``clinical_fields_generator``.

This addresses 21,000+ cross-category template misapplications and removes
the "tumors don't transmit between individuals" / "rare in psittacines"
type credibility-killing errors from a clinical decision support tool.

Run with::

    python3 scripts/template_elimination/eliminate_clinical_field_templates.py

Followed by ``python3 scripts/migrate_to_sqlite.py``.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import re  # noqa: E402

from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    SPECIES_JA,
    generate_clinical_fields,
)
from scripts.template_elimination.eliminate_templates import SPECIES_NORM  # noqa: E402

# Japanese clinical fields whose generated text opens with a
# "<species>における<disease>" lead-in built by ``_disease_prefix``.
_JA_LEAD_FIELDS = [
    "causes_ja",
    "transmission_ja",
    "clinical_signs_ja",
    "differential_diagnosis_ja",
    "prevention_ja",
    "prognosis_ja",
    "pathophysiology_ja",
    "diagnosis_ja",
]

_PAREN_TAG = re.compile(r"[（(][^（）()]*[）)]\s*$")


def strip_redundant_species_lead(data: list[dict]) -> int:
    """Remove a doubled species tag from the generated lead-in.

    Disease names in the species modules sometimes carry a trailing species
    tag (e.g. ``四肢骨折（ハムスター）``). Earlier generator runs produced
    ``ハムスターにおける四肢骨折（ハムスター）`` — the species named twice.
    This rewrites only the exact redundant lead-in to
    ``ハムスターにおける四肢骨折``, touching nothing else, so curated or
    otherwise disease-specific text is left untouched. Descriptive tags such
    as ``（ヨウ素欠乏性）`` are preserved because they do not name the species.
    """
    fixed = 0
    for entry in data:
        name_ja = (entry.get("name_ja") or "").strip()
        if not name_ja:
            continue
        species = entry.get("species", "")
        sp_ja = SPECIES_JA.get(SPECIES_NORM.get(species, species).lower())
        if not sp_ja:
            continue
        m = _PAREN_TAG.search(name_ja)
        if not (m and sp_ja in m.group(0)):
            continue
        clean = _PAREN_TAG.sub("", name_ja).strip()
        redundant_lead = f"{sp_ja}における{name_ja}"
        clean_lead = f"{sp_ja}における{clean}"
        for field in _JA_LEAD_FIELDS:
            val = entry.get(field)
            if isinstance(val, str) and val.startswith(redundant_lead):
                entry[field] = clean_lead + val[len(redundant_lead) :]
                fixed += 1
    return fixed


CLINICAL_FIELDS = [
    "causes_ja",
    "transmission_ja",
    "clinical_signs_ja",
    "differential_diagnosis_ja",
    "prevention_ja",
    "prognosis_ja",
    "pathophysiology_ja",
    "nutrition_management_ja",
    "prognosis_detailed_ja",
    "rehabilitation_protocol_ja",
    "diagnosis_ja",
    # English-language counterparts. These shipped almost entirely as
    # category boilerplate (e.g. one transmission paragraph on 6,000+ diseases,
    # one diagnosis paragraph on 1,600+), so the English site showed identical
    # text for nearly every disease.
    "clinical_signs",
    "transmission",
    "diagnosis",
]

# Minimum text length to consider "non-trivial" (shorter strings are placeholders)
MIN_TEXT_LEN = 50

# A field instance is treated as a template if its text appears in 3+ entries
# (any species, any disease). Disease-specific text is unique or near-unique.
TEMPLATE_DUPLICATE_THRESHOLD = 3


def find_template_texts(data: list[dict]) -> dict[str, set[str]]:
    """Return {field: set_of_template_texts}. A text is a "template" iff used by 3+ entries."""
    result: dict[str, set[str]] = {}
    for field in CLINICAL_FIELDS:
        cnt: Counter = Counter()
        for entry in data:
            text = (entry.get(field) or "").strip()
            if text and len(text) >= MIN_TEXT_LEN:
                cnt[text] += 1
        templates = {text for text, c in cnt.items() if c >= TEMPLATE_DUPLICATE_THRESHOLD}
        result[field] = templates
    return result


def update_json(json_path: Path) -> tuple[int, dict[str, int]]:
    """Update diseases_all_species.json in-place.

    Returns (total_entries_modified, per_field_replacement_count).
    """
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    templates_per_field = find_template_texts(data)
    print("Detected templates:")
    for field, tmpls in templates_per_field.items():
        print(f"  {field}: {len(tmpls)} template texts")

    entries_modified = 0
    field_counts: dict[str, int] = {f: 0 for f in CLINICAL_FIELDS}

    for entry in data:
        species = entry.get("species", "")
        species_norm = SPECIES_NORM.get(species, species).lower()
        name_ja = entry.get("name_ja", "")
        name_en = entry.get("name", "")
        tagged_cat = entry.get("category", "")

        # Identify which fields need regeneration
        fields_to_regen = []
        for field in CLINICAL_FIELDS:
            current = (entry.get(field) or "").strip()
            if not current:
                continue
            if len(current) < MIN_TEXT_LEN:
                continue
            if current in templates_per_field.get(field, set()):
                fields_to_regen.append(field)

        if not fields_to_regen:
            continue

        new_content = generate_clinical_fields(species_norm, name_ja, name_en, tagged_cat, fields_to_regen)

        any_changed = False
        for field, new_text in new_content.items():
            if new_text and new_text != entry.get(field, ""):
                entry[field] = new_text
                field_counts[field] += 1
                any_changed = True
        if any_changed:
            entries_modified += 1

    lead_fixed = strip_redundant_species_lead(data)
    if lead_fixed:
        print(f"Stripped redundant species tag from {lead_fixed} generated lead-ins")

    with open(json_path, "w", encoding="utf-8") as f:
        # Compact (no indent): the file would exceed GitHub's 100 MiB blob
        # limit if pretty-printed, and it is NOT LFS-tracked (read at runtime).
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    return entries_modified, field_counts


def main() -> None:
    json_path = ROOT / "diseases_all_species.json"
    if not json_path.exists():
        print(f"ERROR: {json_path} not found")
        sys.exit(1)

    print(f"Processing {json_path}...")
    modified, counts = update_json(json_path)
    print(f"\nEntries modified: {modified}")
    print("Per-field replacement counts:")
    for field, n in counts.items():
        print(f"  {field}: {n}")


if __name__ == "__main__":
    main()
