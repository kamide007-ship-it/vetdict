"""Replace generic category templates on toxicoses with curated, agent-specific
pathophysiology and etiology.

Why
---
Every poison in the database received the SAME category paragraph for its
``pathophysiology`` / ``pathophysiology_ja`` and ``causes`` / ``causes_ja``
fields — a generic "毒物は特異的標的に作用し…肝・腎は代謝・排泄の主要臓器" text
that is *wrong* for almost every agent (chocolate acts on heart/CNS, xylitol on
insulin/liver, ethylene glycol on renal oxalate crystals, lead on haem
synthesis…).  This is clinically misleading, not merely repetitive.

This script detects entries that (a) still carry the generic toxin template and
(b) map to a curated toxic agent in ``toxicology_library``, and rewrites the
field with that agent's accurate, species-independent mechanism / source text,
prefixed with the localized "<species>における<disease>" lead-in.

It is conservative: an entry is rewritten only when its name resolves to a
curated agent (``resolve_toxic_agent``) AND the existing field matches a known
toxin template (so genuinely curated content is never overwritten).  Disease
names that merely *contain* a toxin keyword but are not chemical toxicoses
(e.g. "サケ中毒症" = salmon poisoning, an infection) resolve to ``None`` and are
left untouched.

Idempotent: re-running detects that curated text no longer matches the template
markers and makes no further changes.

Usage::

    python3 scripts/template_elimination/eliminate_toxicology_templates.py          # dry run
    python3 scripts/template_elimination/eliminate_toxicology_templates.py --apply   # write
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from clinical_fields_generator import (  # noqa: E402
    SPECIES_EN,
    SPECIES_JA,
    _disease_prefix,
)
from toxicology_library import agent_content, resolve_toxic_agent  # noqa: E402

# Repo root (this file lives in scripts/template_elimination/).
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
JSON_PATH = os.path.join(ROOT, "diseases_all_species.json")

# --- Template markers ------------------------------------------------------
# A field is considered "generic toxin template" when it contains one of these
# fingerprints.  JA has a single template; EN has a couple of variants.
TOXIN_PATHO_JA_MARKER = "毒物は特異的標的"
TOXIN_CAUSE_JA_MARKER = "特定の毒性物質への摂取"

TOXIN_PATHO_EN_PREFIXES = (
    "The pathophysiology of toxicosis involves",
    "Toxic exposures affecting",
)
TOXIN_CAUSE_EN_PREFIXES = (
    "Exposure to toxic substance",
    "Toxicosis results from exposure to harmful substances",
)


def _species_key(species: str) -> str:
    """Normalise a JSON species value ("Guinea Pig") to a key ("guinea_pig")."""
    return (species or "").strip().lower().replace(" ", "_")


def _ja_prefix(name_ja: str, species: str) -> str:
    sp_ja = SPECIES_JA.get(_species_key(species), species)
    return _disease_prefix(name_ja, sp_ja)


def _en_subject(name_en: str, species: str) -> str:
    sp_en = SPECIES_EN.get(_species_key(species), (species or "").lower())
    return f"In {sp_en}, {name_en}"


def _is_toxin_patho_ja(text: str) -> bool:
    return bool(text) and TOXIN_PATHO_JA_MARKER in text


def _is_toxin_cause_ja(text: str) -> bool:
    return bool(text) and TOXIN_CAUSE_JA_MARKER in text


def _is_toxin_patho_en(text: str) -> bool:
    return bool(text) and any(text.startswith(p) for p in TOXIN_PATHO_EN_PREFIXES)


def _is_toxin_cause_en(text: str) -> bool:
    return bool(text) and any(text.startswith(p) for p in TOXIN_CAUSE_EN_PREFIXES)


def curated_fields_for(entry: dict) -> Optional[dict[str, str]]:
    """Return the curated replacement fields for an entry, or None.

    Only fields that are *currently a toxin template* are returned, so curated
    or already-rewritten content is preserved.
    """
    name_ja = str(entry.get("name_ja", "") or "")
    name_en = str(entry.get("name", "") or "")
    species = str(entry.get("species", "") or "")

    agent = resolve_toxic_agent(name_ja, name_en)
    if not agent:
        return None
    body = agent_content(agent)
    if not body:
        return None

    out: dict[str, str] = {}

    if _is_toxin_patho_ja(str(entry.get("pathophysiology_ja", ""))):
        out["pathophysiology_ja"] = f"{_ja_prefix(name_ja, species)}は、{body['patho_ja']}"
    if _is_toxin_cause_ja(str(entry.get("causes_ja", ""))):
        out["causes_ja"] = f"{_ja_prefix(name_ja, species)}は、{body['causes_ja']}"
    if _is_toxin_patho_en(str(entry.get("pathophysiology", ""))):
        out["pathophysiology"] = f"{_en_subject(name_en, species)} is {body['patho_en']}"
    if _is_toxin_cause_en(str(entry.get("causes", ""))):
        out["causes"] = f"{_en_subject(name_en, species)} results from {body['causes_en']}"

    return out or None


def run(apply: bool) -> dict[str, int]:
    with open(JSON_PATH, encoding="utf-8") as fh:
        data = json.load(fh)

    stats = {
        "entries_touched": 0,
        "pathophysiology_ja": 0,
        "causes_ja": 0,
        "pathophysiology": 0,
        "causes": 0,
        "agents_used": 0,
    }
    agents_seen: set[str] = set()
    examples: list[str] = []

    for entry in data:
        if not isinstance(entry, dict):
            continue
        fields = curated_fields_for(entry)
        if not fields:
            continue
        stats["entries_touched"] += 1
        agents_seen.add(resolve_toxic_agent(str(entry.get("name_ja", "")), str(entry.get("name", ""))))
        for field, value in fields.items():
            stats[field] += 1
            if apply:
                entry[field] = value
        if len(examples) < 4 and "pathophysiology_ja" in fields:
            examples.append(
                f"[{entry.get('species')}] {entry.get('name_ja')}\n  → {fields['pathophysiology_ja'][:140]}…"
            )

    stats["agents_used"] = len(agents_seen)

    if apply:
        # Match the source file's compact, single-line encoding so the diff is
        # limited to the rewritten fields rather than a full re-indent.
        with open(JSON_PATH, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))

    print(f"{'APPLIED' if apply else 'DRY RUN'} — toxicology template elimination")
    print(f"  entries touched : {stats['entries_touched']}")
    print(f"  pathophysiology_ja rewritten : {stats['pathophysiology_ja']}")
    print(f"  causes_ja          rewritten : {stats['causes_ja']}")
    print(f"  pathophysiology    rewritten : {stats['pathophysiology']}")
    print(f"  causes             rewritten : {stats['causes']}")
    print(f"  distinct agents used         : {stats['agents_used']}")
    if examples:
        print("\n  examples:")
        for ex in examples:
            print("   " + ex.replace("\n", "\n   "))
    return stats


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="write changes to the JSON file")
    args = parser.parse_args()
    run(apply=args.apply)


if __name__ == "__main__":
    main()
