"""Replace generic viral-category etiology/pathophysiology with named-pathogen prose.

Diseases whose name identifies the causative virus (canine parvovirus, feline
herpesvirus, rabies, avian influenza …) shipped the generic viral category
template for ``causes`` / ``pathophysiology`` in both languages:

    JA causes:  「…の原因はウイルス感染である。特異的ウイルス病原体が宿主細胞に…」
    EN causes:  "Viral infection. Transmission via direct contact with infected…"

The pathogen — and therefore the aetiology — is a textbook fact derivable from
the disease name, so this pass writes pathogen-specific ``causes`` and
``pathophysiology`` (JA+EN) from ``pathogen_library``. Fields are replaced ONLY
when they currently hold a recognised category template or vague stub, so
genuine curated prose (flagship PBFD/PDD, the JA-curated parvovirus/FeLV/FIP
entries) is preserved — and for those flagships the still-templated *English*
field is upgraded while the curated Japanese field is left intact.

Run with ``--apply`` to write ``diseases_all_species.json``; default is a dry run.
The served-DB safety net ``regenerate_named_pathogen_etiology`` in
``migrate_to_sqlite.py`` applies the same correction to module-sourced records.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.bacterial_library import (  # noqa: E402
    bacterial_clinical_fields,
)
from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    build_etiology_fingerprints,
    fingerprint_etiology,
    gen_causes_ja,
    gen_pathophysiology_ja,
)
from scripts.template_elimination.curated_etiology import STUB_SIGNATURES  # noqa: E402
from scripts.template_elimination.eliminate_templates import SPECIES_NORM  # noqa: E402
from scripts.template_elimination.flagship_noninfectious_library import (  # noqa: E402
    flagship_clinical_fields,
)
from scripts.template_elimination.fungal_library import (  # noqa: E402
    fungal_clinical_fields,
)
from scripts.template_elimination.nutritional_library import (  # noqa: E402
    nutrient_clinical_fields,
)
from scripts.template_elimination.parasite_library import (  # noqa: E402
    parasite_clinical_fields,
)
from scripts.template_elimination.pathogen_library import (  # noqa: E402
    GENERIC_CAUSES_EN_MARKS,
    GENERIC_CAUSES_JA_MARKS,
    GENERIC_PATHO_EN_MARKS,
    viral_clinical_fields,
)

JSON_PATH = ROOT / "diseases_all_species.json"

# Explicit category-template signatures (belt-and-braces alongside fingerprints).
CAUSES_JA_MARKS = GENERIC_CAUSES_JA_MARKS
CAUSES_EN_MARKS = GENERIC_CAUSES_EN_MARKS
PATHO_JA_MARKS = ("病態生理はウイルス侵入", "病原ウイルスは特異的細胞受容体")
PATHO_EN_MARKS = GENERIC_PATHO_EN_MARKS


def _clinical_fields(species: str, name_ja: str, name_en: str):
    """Curated causes/pathophysiology: named pathogen (viral/bacterial/fungal/
    parasite), then named nutrient, then non-infectious flagship; None if none."""
    return (
        viral_clinical_fields(species, name_ja, name_en)
        or bacterial_clinical_fields(species, name_ja, name_en)
        or fungal_clinical_fields(species, name_ja, name_en)
        or parasite_clinical_fields(species, name_ja, name_en)
        or nutrient_clinical_fields(species, name_ja, name_en)
        or flagship_clinical_fields(species, name_ja, name_en)
    )


def _make_replaceable(fingerprints, marks, en=False):
    def _replaceable(text: str) -> bool:
        if not text:
            return True
        if not en and fingerprint_etiology(text, fingerprints) is not None:
            return True
        if any(sig in text for sig in STUB_SIGNATURES):
            return True
        hay = text.lower() if en else text
        return any((m.lower() if en else m) in hay for m in marks)

    return _replaceable


def remediate(data: list[dict], apply: bool) -> dict:
    causes_fps = build_etiology_fingerprints(gen_causes_ja)
    patho_fps = build_etiology_fingerprints(gen_pathophysiology_ja)
    causes_ja_ok = _make_replaceable(causes_fps, CAUSES_JA_MARKS)
    causes_en_ok = _make_replaceable(None, CAUSES_EN_MARKS, en=True)
    patho_ja_ok = _make_replaceable(patho_fps, PATHO_JA_MARKS)
    patho_en_ok = _make_replaceable(None, PATHO_EN_MARKS, en=True)

    stats = {"causes_ja": 0, "causes": 0, "pathophysiology_ja": 0, "pathophysiology": 0, "diseases": 0}
    examples: list[str] = []

    for entry in data:
        name_ja = entry.get("name_ja") or ""
        name_en = entry.get("name") or ""
        raw_species = entry.get("species", "")
        species = SPECIES_NORM.get(raw_species, (raw_species or "").lower())
        fields = _clinical_fields(species, name_ja, name_en)
        if not fields:
            continue
        touched = False
        for field, checker in (
            ("causes_ja", causes_ja_ok),
            ("causes", causes_en_ok),
            ("pathophysiology_ja", patho_ja_ok),
            ("pathophysiology", patho_en_ok),
        ):
            if checker(entry.get(field) or "") and fields[field] != (entry.get(field) or ""):
                stats[field] += 1
                touched = True
                if apply:
                    entry[field] = fields[field]
        if touched:
            stats["diseases"] += 1
            if len(examples) < 25:
                examples.append(f"[{raw_species}] {name_ja or name_en}")

    stats["_examples"] = examples
    return stats


def main() -> None:
    apply = "--apply" in sys.argv
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    stats = remediate(data, apply)
    examples = stats.pop("_examples")
    print(f"Named-pathogen viral diseases touched: {stats['diseases']}")
    for f in ("causes_ja", "causes", "pathophysiology_ja", "pathophysiology"):
        print(f"  {f}: {stats[f]} replaced")
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
