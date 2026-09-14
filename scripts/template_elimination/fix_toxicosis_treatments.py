"""Replace the generic toxin-decontamination treatment template with curated
agent-specific protocols in ``diseases_all_species.json``.

See ``toxicosis_treatment_library`` for background. Gating (deliberately
conservative):

* Only entries on the curated exact-(species, name) list are ever touched.
* ``treatment_ja`` is replaced only when it carries the JA template
  fingerprint; ``treatment`` only when it carries the EN fingerprint. Curated
  prose in either language is never overwritten.
* Entries whose species module already holds an informative treatment (the
  33 records restored by the ``_guard_treatment`` fingerprint fix) are NOT on
  the curated list — the module text is richer and now wins in both serving
  paths.

Run ``python3 scripts/template_elimination/fix_toxicosis_treatments.py`` for a
dry run, ``--apply`` to write.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.eliminate_templates import SPECIES_NORM  # noqa: E402
from scripts.template_elimination.toxicosis_treatment_library import (  # noqa: E402
    TOXIN_TREATMENT_EN_SIG,
    TOXIN_TREATMENT_JA_SIG,
    curated_toxicosis_treatment,
    en_backfill_treatment,
    ja_mistemplate_fix,
)

JSON_PATH = ROOT / "diseases_all_species.json"


def remediate(data: list[dict], apply: bool) -> dict:
    stats = {"treatment_ja": 0, "treatment": 0}
    examples: list[str] = []

    for entry in data:
        raw_species = entry.get("species", "")
        species = SPECIES_NORM.get(raw_species, (raw_species or "").lower())
        name_en = entry.get("name") or ""
        tj = entry.get("treatment_ja") or ""
        te = entry.get("treatment") or ""
        touched = False

        fields = curated_toxicosis_treatment(species, name_en)
        if fields:
            if TOXIN_TREATMENT_JA_SIG in tj:
                stats["treatment_ja"] += 1
                touched = True
                if apply:
                    entry["treatment_ja"] = fields["treatment_ja"]
            if TOXIN_TREATMENT_EN_SIG in te:
                stats["treatment"] += 1
                touched = True
                if apply:
                    entry["treatment"] = fields["treatment"]

        # EN back-fill for JA-informative records whose EN carries the template.
        en_fields = en_backfill_treatment(species, name_en)
        if en_fields and TOXIN_TREATMENT_EN_SIG in (entry.get("treatment") or ""):
            stats["treatment"] += 1
            touched = True
            if apply:
                entry["treatment"] = en_fields["treatment"]

        # Records carrying some OTHER wrong-category template (work-up
        # boilerplate on femoral pore impaction; mammalian urolithiasis
        # protocol on avian AKI/urolithiasis; CKD protocol on acute renal
        # failure). Each language is gated on its own bad fingerprint.
        mis = ja_mistemplate_fix(species, name_en)
        if mis:
            ja_sig, en_sig, fix_fields = mis
            if ja_sig in (entry.get("treatment_ja") or ""):
                stats["treatment_ja"] += 1
                touched = True
                if apply:
                    entry["treatment_ja"] = fix_fields["treatment_ja"]
            if en_sig in (entry.get("treatment") or ""):
                stats["treatment"] += 1
                touched = True
                if apply:
                    entry["treatment"] = fix_fields["treatment"]

        if touched and len(examples) < 30:
            examples.append(f"[{raw_species}] {name_en}")

    stats["_examples"] = examples
    return stats


def main() -> None:
    apply = "--apply" in sys.argv
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    stats = remediate(data, apply)
    examples = stats.pop("_examples")
    print(f"treatment_ja replaced: {stats['treatment_ja']}")
    print(f"treatment (EN) replaced: {stats['treatment']}")
    if examples:
        print("  e.g. " + ", ".join(examples[:15]))
    if apply:
        with JSON_PATH.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
        print(f"Wrote {JSON_PATH}")
    else:
        print("Dry run — pass --apply to write.")


if __name__ == "__main__":
    main()
