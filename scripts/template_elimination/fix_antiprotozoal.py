"""Replace the deworming treatment template on protozoal diseases with curated antiprotozoal protocols.

Protozoa (Babesia, Toxoplasma, Leishmania, Hepatozoon, Cytauxzoon,
Encephalitozoon, coccidia, Sarcocystis, Atoxoplasma, Leucocytozoon, avian
malaria) are not treated by anthelmintics, yet ~40 served records and their JSON
overlay carry the generic deworming template. This pass writes evidence-based,
species-aware antiprotozoal treatment (the clinically dangerous field) and a
pathogen-specific pathophysiology into ``diseases_all_species.json``.

Gating:
* ``treatment_ja`` / ``treatment`` — replaced whenever the deworming fingerprint
  is present and the disease resolves to a protozoal agent (the dewormer text is
  clinically wrong, so it is always corrected).
* ``pathophysiology_ja`` / ``pathophysiology`` — replaced only when the existing
  field is empty, a recognised category template, or a vague stub, so genuine
  curated mechanism prose is never overwritten.

The served-database safety net (``regenerate_protozoal_treatments`` in
``migrate_to_sqlite.py``) applies the same correction to module-sourced records,
so the fix holds in both the JSON-overlay (low-memory) and migrated paths.

Run ``python3 scripts/template_elimination/fix_antiprotozoal.py`` for a dry run,
``--apply`` to write.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.antiprotozoal_library import (  # noqa: E402
    DEWORM_SIG,
    PATHO_EN_STUB_MARKS,
    PATHO_JA_STUB_MARKS,
    protozoal_clinical_fields,
    resolve_protozoal_agent,
)
from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    build_etiology_fingerprints,
    fingerprint_etiology,
    gen_pathophysiology_ja,
)
from scripts.template_elimination.curated_etiology import STUB_SIGNATURES  # noqa: E402
from scripts.template_elimination.eliminate_templates import SPECIES_NORM  # noqa: E402

JSON_PATH = ROOT / "diseases_all_species.json"


def _patho_ja_replaceable(text: str, fingerprints) -> bool:
    if not text:
        return True
    if fingerprint_etiology(text, fingerprints) is not None:
        return True
    if any(sig in text for sig in STUB_SIGNATURES):
        return True
    return any(m in text for m in PATHO_JA_STUB_MARKS)


def _patho_en_replaceable(text: str) -> bool:
    if not text:
        return True
    low = text.lower()
    return any(m in low for m in PATHO_EN_STUB_MARKS)


def remediate(data: list[dict], apply: bool) -> dict:
    patho_fps = build_etiology_fingerprints(gen_pathophysiology_ja)
    stats = {"treatment": 0, "pathophysiology_ja": 0, "pathophysiology": 0}
    examples: list[str] = []

    for entry in data:
        tx = entry.get("treatment_ja") or ""
        if DEWORM_SIG not in tx:
            continue
        name_ja = entry.get("name_ja") or ""
        name_en = entry.get("name") or ""
        if resolve_protozoal_agent(name_ja, name_en) is None:
            continue
        raw_species = entry.get("species", "")
        species = SPECIES_NORM.get(raw_species, (raw_species or "").lower())
        fields = protozoal_clinical_fields(species, name_ja, name_en, tx)
        if not fields:
            continue

        stats["treatment"] += 1
        if len(examples) < 25:
            examples.append(f"[{raw_species}] {name_ja or name_en}")
        if apply:
            entry["treatment_ja"] = fields["treatment_ja"]
            entry["treatment"] = fields["treatment"]

        if _patho_ja_replaceable(entry.get("pathophysiology_ja") or "", patho_fps):
            stats["pathophysiology_ja"] += 1
            if apply:
                entry["pathophysiology_ja"] = fields["pathophysiology_ja"]
        if _patho_en_replaceable(entry.get("pathophysiology") or ""):
            stats["pathophysiology"] += 1
            if apply:
                entry["pathophysiology"] = fields["pathophysiology"]

    stats["_examples"] = examples
    return stats


def main() -> None:
    apply = "--apply" in sys.argv
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    stats = remediate(data, apply)
    examples = stats.pop("_examples")
    print(f"Protozoal diseases corrected (treatment): {stats['treatment']}")
    print(f"  pathophysiology_ja replaced: {stats['pathophysiology_ja']}")
    print(f"  pathophysiology (EN) replaced: {stats['pathophysiology']}")
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
