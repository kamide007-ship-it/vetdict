#!/usr/bin/env python3
"""Bring the English ``causes`` field to parity with the Japanese one.

Background
----------
Every non-Japanese clinical field was curated over many sessions, but the
English ``causes`` field was left carrying the old organ-system category
templates produced by the exotic-enrichment pipeline.  Worse than merely being
generic, many were **mis-categorised**: inflammatory "-itis" diseases
(keratitis, hepatitis, myocarditis, dermatitis ...) were described as
*"Caused by exposure to toxic substances ..."* — a claim a clinician would
immediately flag as wrong.  The Japanese ``causes`` for the same records is
already category-correct (bird keratitis JA = ophthalmic/infectious, not toxic).

This script detects the generic English category templates, resolves the
correct category from the disease **name** (the same trusted, name-based
resolver the Japanese generator relies on), and regenerates the English
``causes`` with :func:`gen_causes_en`.  Curated / named-agent text (which does
not match a generic fingerprint) is never touched, and records whose name does
not resolve to a category are left unchanged (conservative — no fabrication).

Reaches users through ``diseases_all_species.json`` (the runtime enrichment
overlay); a served-DB safety net in ``migrate_to_sqlite.py`` catches anything
sourced only from a module.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import re  # noqa: E402

from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    NAME_CATEGORY_PATTERNS,
    gen_causes_en,
    gen_pathophysiology_en,
    resolve_category_from_name,
)
from scripts.template_elimination.flagship_noninfectious_library import (  # noqa: E402
    flagship_clinical_fields,
)

JSON_PATH = ROOT / "diseases_all_species.json"


# Species display names in the JSON ("Guinea Pig") -> generator species codes
# ("guinea_pig"). Lower-casing and swapping spaces for underscores covers all.
def _species_code(display: str) -> str:
    return (display or "").strip().lower().replace(" ", "_")


# Leading fingerprints of the GENERIC English category ``causes`` templates.
# Curated / named-pathogen text does not start with any of these, so it is
# left alone. Kept deliberately specific to avoid catching hand-written prose.
GENERIC_CAUSES_EN_PREFIXES: tuple[str, ...] = (
    "Multifactorial etiology depending on disease type",
    "Neoplastic etiology, often unknown",
    "Neoplastic diseases arise from uncontrolled",
    "Caused by physical trauma to musculoskeletal tissues",
    "Caused by physical trauma to ",
    "Caused by exposure to toxic substances",
    "Toxicosis results from exposure to harmful",
    "Respiratory etiology",
    "Gastrointestinal etiology",
    "Infectious diseases are caused by pathogenic",
    "Endocrine or metabolic dysfunction",
    "Nutritional diseases result from",
    "Nutritional imbalance. Caused by inadequate",
    "Musculoskeletal etiology",
    "Neurological etiology",
    "Hepatic etiology",
    "Ophthalmic etiology",
    "Reproductive etiology",
    "Dermatological etiology",
    "Renal etiology",
    "Behavioral etiology",
    "Cardiac etiology",
    "Dental etiology",
    "Caused by dietary deficiency or excess",
    "Caused by parasites infecting affected tissues",
    "Traumatic etiology",
    "Traumatic injuries result from external",
    "Congenital and hereditary conditions result",
    "Autoimmune diseases result from a loss",
    "Parasitic diseases are caused by",
    "Caused by progressive deterioration of",
    "Caused by a specific virus targeting",
    "Caused by pathogenic bacteria infecting",
    "Caused by parasitic organisms infecting",
    "Caused by fungal organisms infecting",
    "Caused by neoplastic transformation of",
    "Caused by metabolic dysfunction affecting",
    "Caused by developmental abnormality of",
    "Caused by immune-mediated attack on",
    "Caused by maladaptive behavior related to",
    "The exact cause affecting",
    "Caused by inflammatory processes in",
)


def is_generic_causes_en(text: str) -> bool:
    if not text:
        return False
    t = text.lstrip()
    return any(t.startswith(p) for p in GENERIC_CAUSES_EN_PREFIXES)


# Word inside "The pathophysiology of <word> diseases involves ..." -> category.
# Deliberately EXCLUDES "infectious"/"bacterial": many organ-named inflammatory
# diseases (osteomyelitis, endocarditis, meningitis, mastitis, pyometra) are
# genuinely bacterial, so their bacterial pathophysiology is appropriate and
# must not be rewritten. We only correct the unambiguous mismatches — a
# parasitic/viral/fungal/toxicosis mechanism on a disease that carries no such
# signal in its name (e.g. the parasitic template on myocarditis).
_EN_PATHO_WORD_CATEGORY = {
    "viral": "viral_infection",
    "parasitic": "parasitic",
    "fungal": "fungal_infection",
    "toxicosis": "toxicity",
    "toxic": "toxicity",
}

# The category template reads either "The pathophysiology of <word> diseases
# involves ..." or "The pathophysiology of <word> involves ...". Keying on the
# category WORD (not the literal "diseases") catches both variants, while the
# regenerated text — "The pathophysiology of <DiseaseName> in <species> ..." —
# never begins with one of these category words, so re-running is a no-op.
_EN_PATHO_LEAD_RE = re.compile(
    r"^\s*The pathophysiology of (viral|parasitic|fungal|toxicosis|toxic|bacterial|infectious)\b",
    re.IGNORECASE,
)


def _name_matches_category(name_ja: str, name_en: str, category: str) -> bool:
    """True if the disease name matches the given category's patterns.

    Used to decide whether a pathophysiology template is legitimate: the
    *parasitic* template is appropriate only when the name signals a parasite
    (Thelazia *Eye Worm* is parasitic despite its ophthalmic-sounding name),
    but the *toxicosis* template on Cryptosporidiosis is wrong because the name
    signals a parasite, not a toxicosis — so we check the IMPLIED category, not
    infection in general.
    """
    combined = f"{name_ja or ''} {name_en or ''}"
    return any(cat == category and pattern.search(combined) for pattern, cat in NAME_CATEGORY_PATTERNS)


def regenerate_entry_pathophysiology(entry: dict) -> str | None:
    """Fix an English pathophysiology that carries an infection/toxicosis
    template on a disease that is not infectious/toxic. Returns the corrected
    text or None to leave as-is (conservative)."""
    patho = entry.get("pathophysiology") or ""
    m = _EN_PATHO_LEAD_RE.match(patho)
    if not m:
        return None
    implied = _EN_PATHO_WORD_CATEGORY.get(m.group(1).lower())
    if implied is None:
        return None  # bacterial/infectious or organ template — leave (often correct)
    name_ja = entry.get("name_ja") or ""
    name_en = entry.get("name") or ""
    if _name_matches_category(name_ja, name_en, implied):
        return None  # name genuinely signals this category — template is appropriate
    code = _species_code(entry.get("species", ""))

    flag = flagship_clinical_fields(code, name_ja, name_en)
    if flag and flag.get("pathophysiology"):
        text = flag["pathophysiology"]
        return text if not _EN_PATHO_LEAD_RE.match(text) and text != patho else None

    resolved = resolve_category_from_name(name_ja, name_en)
    if not resolved or resolved == implied:
        return None  # no name-based category, or already the implied one
    new = gen_pathophysiology_en(resolved, name_en, code)
    if not new or new == patho or _EN_PATHO_LEAD_RE.match(new):
        return None
    return new


def regenerate_entry_causes(entry: dict) -> str | None:
    """Return the corrected English causes for *entry*, or None to leave as-is."""
    causes = entry.get("causes") or ""
    if not is_generic_causes_en(causes):
        return None
    code = _species_code(entry.get("species", ""))
    name_ja = entry.get("name_ja") or ""
    name_en = entry.get("name") or ""

    # Prefer a bilingual curated generator (flagship non-infectious diseases,
    # e.g. laminitis) so a multifactorial disease is not flattened into the
    # single category the name resolver would pick.
    flag = flagship_clinical_fields(code, name_ja, name_en)
    if flag and flag.get("causes") and not is_generic_causes_en(flag["causes"]):
        return flag["causes"] if flag["causes"] != causes else None

    category = resolve_category_from_name(name_ja, name_en)
    if not category:
        return None  # name does not determine a category — do not fabricate
    new = gen_causes_en(category, name_en, code)
    if not new or new == causes or is_generic_causes_en(new):
        return None
    return new


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes to the JSON")
    ap.add_argument("--limit", type=int, default=0, help="report only N examples")
    args = ap.parse_args()

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    changed = 0
    patho_changed = 0
    examples = []
    patho_examples = []
    from collections import Counter

    by_cat = Counter()
    for entry in data:
        new = regenerate_entry_causes(entry)
        if new is not None:
            cat = resolve_category_from_name(entry.get("name_ja") or "", entry.get("name") or "") or "flagship/curated"
            by_cat[cat] += 1
            if len(examples) < 25:
                examples.append((entry.get("species"), entry.get("name"), cat))
            entry["causes"] = new
            changed += 1

        new_p = regenerate_entry_pathophysiology(entry)
        if new_p is not None:
            if len(patho_examples) < 20:
                patho_examples.append((entry.get("species"), entry.get("name")))
            entry["pathophysiology"] = new_p
            patho_changed += 1

    print(f"English causes regenerated: {changed}")
    print("by resolved category:")
    for cat, n in by_cat.most_common():
        print(f"  {cat:24s} {n}")
    print("\nexamples:")
    for e in examples:
        print("  ", e)
    print(f"\nEnglish pathophysiology miscategorisations fixed: {patho_changed}")
    for e in patho_examples:
        print("  ", e)

    if args.apply and (changed or patho_changed):
        with JSON_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        print(f"\nWROTE {JSON_PATH}")
    elif not args.apply:
        print("\n(dry-run; pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
