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
    resolve_category_from_name,
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

# Structural ("name-interpolated") templates: the category generators slot the
# disease name + species into a fixed category paragraph, so the resulting text
# is byte-unique per disease yet structurally identical once the name/species
# and numbers are normalised out. Exact-match detection misses these entirely —
# which is how a thyroid-storm record kept the *neoplasia* etiology paragraph
# (its category tag was wrongly "oncology") without ever being flagged. A
# normalised cluster of >= STRUCT_MIN_CLUSTER entries spanning >=
# STRUCT_MIN_NAMES distinct base disease names is treated as a structural
# template and regenerated through the (name-priority) category resolver.
STRUCT_MIN_CLUSTER = 5
STRUCT_MIN_NAMES = 3

# Structural regeneration only runs on fields where the (name-priority) category
# generator strictly improves a templated value: every category has a distinct,
# evidence-based branch, so a wrong-category paragraph is replaced with the right
# one and contentless filler with category-specific mechanism. Fields whose
# legacy text is sometimes richer than the generator output (prevention,
# prognosis, nutrition, rehab, the *_ja signs/transmission/ddx) are intentionally
# excluded so structural regen never trades good content for a flatter template;
# they keep exact-duplicate detection only and are grounded at migration time.
STRUCT_REGEN_FIELDS = frozenset(
    {
        "causes_ja",
        "pathophysiology_ja",
        # English fields that shipped as a single paragraph reused across
        # thousands of diseases — category-specific text is unambiguously better.
        "clinical_signs",
        "transmission",
        "diagnosis",
    }
)

_NUM_RE = re.compile(r"\d+")
_PAREN_ANY = re.compile(r"[（(][^（）()]*[）)]")


def _normalize_struct(text: str, name_ja: str, name_en: str, sp_ja: str) -> str:
    """Strip disease name, species name and digits so structural twins collapse."""
    t = text
    for token in (name_ja, name_en, sp_ja):
        if token:
            t = t.replace(token, "✦")
            base = _PAREN_ANY.sub("", token).strip()
            if base and base != token:
                t = t.replace(base, "✦")
    t = _PAREN_ANY.sub("", t)
    t = _NUM_RE.sub("#", t)
    return re.sub(r"\s+", " ", t).strip()


def find_structural_template_norms(data: list[dict]) -> dict[str, set[str]]:
    """Return {field: set_of_normalised_keys that are structural templates}."""
    result: dict[str, set[str]] = {}
    for field in CLINICAL_FIELDS:
        clusters: dict[str, list[str]] = {}
        for entry in data:
            text = (entry.get(field) or "").strip()
            if not text or len(text) < MIN_TEXT_LEN:
                continue
            species = entry.get("species", "")
            sp_ja = SPECIES_JA.get(SPECIES_NORM.get(species, species).lower(), "")
            key = _normalize_struct(text, entry.get("name_ja", ""), entry.get("name", ""), sp_ja)
            base = _PAREN_ANY.sub("", entry.get("name_ja") or entry.get("name") or "").strip()
            clusters.setdefault(key, []).append(base)
        result[field] = {
            key
            for key, names in clusters.items()
            if len(names) >= STRUCT_MIN_CLUSTER and len(set(names)) >= STRUCT_MIN_NAMES
        }
    return result


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
    struct_per_field = find_structural_template_norms(data)
    print("Detected templates (exact / structural):")
    for field in CLINICAL_FIELDS:
        print(f"  {field}: {len(templates_per_field.get(field, set()))} / {len(struct_per_field.get(field, set()))}")

    entries_modified = 0
    field_counts: dict[str, int] = {f: 0 for f in CLINICAL_FIELDS}

    for entry in data:
        species = entry.get("species", "")
        species_norm = SPECIES_NORM.get(species, species).lower()
        name_ja = entry.get("name_ja", "")
        name_en = entry.get("name", "")
        tagged_cat = entry.get("category", "")
        sp_ja = SPECIES_JA.get(species_norm, "")

        # Structural regen only fires when the category is fixed by the disease
        # *name*, not by the stored tag. The tag is exactly what is unreliable
        # (a thyroid-storm record tagged "oncology"), and it is inconsistent
        # across species for the same disease — leaving "Gastrointestinal
        # Motility Disorder" tagged parasitic in parrots but toxic in birds. A
        # name-derived category is consistent disease-wide and is what the
        # (high-quality) description field already trusts, so a name match is the
        # gate; when the name doesn't resolve, the existing text is left intact.
        name_category = resolve_category_from_name(name_ja, name_en)

        # Identify which fields need regeneration (exact OR structural template)
        fields_to_regen = []
        for field in CLINICAL_FIELDS:
            current = (entry.get(field) or "").strip()
            if not current or len(current) < MIN_TEXT_LEN:
                continue
            if current in templates_per_field.get(field, set()):
                fields_to_regen.append(field)
                continue
            if field in STRUCT_REGEN_FIELDS and name_category is not None:
                norm = _normalize_struct(current, name_ja, name_en, sp_ja)
                if norm in struct_per_field.get(field, set()):
                    fields_to_regen.append(field)

        if not fields_to_regen:
            continue

        new_content = generate_clinical_fields(species_norm, name_ja, name_en, tagged_cat, fields_to_regen)

        any_changed = False
        for field, new_text in new_content.items():
            old_text = entry.get(field, "")
            if not new_text or new_text == old_text:
                continue
            # Only rewrite when the *structure* changes — i.e. a genuine category
            # correction (thyroid-storm neoplasia paragraph -> endocrine) or a
            # contentless-filler -> category-specific upgrade. Pure name/number
            # wording drift between generator versions is skipped so the diff
            # stays a credibility fix, not a mass reflow of every record.
            if _normalize_struct(new_text, name_ja, name_en, sp_ja) == _normalize_struct(
                old_text, name_ja, name_en, sp_ja
            ):
                continue
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
