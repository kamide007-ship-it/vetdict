"""Fix clinically dangerous treatment_ja miscategorisations.

Some disease records carry a *category-specific* treatment template whose
category contradicts the disease — producing recommendations that would harm a
patient if published:

* **Deworming protocol on rickettsial / tick-borne bacteria.** Canine
  ehrlichiosis, anaplasmosis, Rocky-Mountain spotted fever and hemoplasmosis
  were tagged ``parasite`` and received an "適切な駆虫薬" (antihelmintic)
  protocol. They are doxycycline-responsive bacteria; dewormers and
  fluoroquinolones are ineffective.
* **Deworming / oncology protocol on toxicoses.** Permethrin / Teflon (PTFE)
  toxicosis received a deworming protocol instead of decontamination.
* **Chemotherapy / biopsy-staging protocol on benign cysts & polyps.** Ovarian
  cysts, sebaceous cysts, feather cysts, renal cysts and polyps were tagged
  ``oncology`` and received a TNM-staging / chemotherapy protocol. They are not
  neoplasms.

The fix is conservative and *gated on the corrected name-priority class*
(``fallback_generator._disease_class_hint``): a templated treatment is only
regenerated when the disease name unambiguously resolves to a non-parasitic /
non-neoplastic class, so genuine parasites (疥癬, 食道虫症, …) and genuine
tumours are never touched.

Run with::

    python3 scripts/template_elimination/fix_dangerous_treatment_miscategorization.py [--apply]

Followed by ``python3 scripts/migrate_to_sqlite.py``.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.eliminate_templates import SPECIES_NORM  # noqa: E402
from scripts.template_elimination.fallback_generator import (  # noqa: E402
    _disease_class_hint,
    generate_fallback_content,
)

JSON_PATH = ROOT / "diseases_all_species.json"

# Treatment-template fingerprints that are dangerous when mis-applied.
DEWORM_SIG = "駆虫薬"
ONCOLOGY_SIG = "腫瘍の組織学的型・グレード"

# A deworming template is only overridden when the corrected class is one of
# these unambiguously-non-parasitic classes. (derm / respiratory / GI / general
# are intentionally excluded: a generically-named parasite, e.g. 疥癬, can land
# there and its deworming protocol is correct.)
DEWORM_OVERRIDE_CLASSES = {"rickettsial", "toxic", "nutritional"}

# Salmon-poisoning disease (Neorickettsia) carries 中毒 in its name but is
# fluke-vectored — its deworming component is legitimate, so never override it.
DEWORM_OVERRIDE_NAME_EXCLUSIONS = ("サーモン中毒", "サケ中毒")


def _norm_species(raw: str) -> str:
    return SPECIES_NORM.get(raw, raw).lower()


def remediate(data: list[dict], apply: bool) -> dict:
    stats = {"rickettsial": 0, "toxic": 0, "nutritional": 0, "cyst_polyp": 0}
    changes: list[tuple[str, str, str]] = []

    for entry in data:
        tx = (entry.get("treatment_ja") or "").strip()
        if not tx:
            continue
        name_ja = entry.get("name_ja") or ""
        name_en = entry.get("name") or ""
        klass = _disease_class_hint(name_ja or name_en)

        target = None
        if DEWORM_SIG in tx and klass in DEWORM_OVERRIDE_CLASSES:
            if any(x in (name_ja + name_en) for x in DEWORM_OVERRIDE_NAME_EXCLUSIONS):
                continue
            target = klass
        elif ONCOLOGY_SIG in tx and klass == "cyst_polyp":
            target = "cyst_polyp"

        if target is None:
            continue

        species = _norm_species(entry.get("species", ""))
        new = generate_fallback_content(species, name_ja, name_en, en_treatment=entry.get("treatment"))
        new_tx = new.get("treatment_ja")
        if not new_tx or new_tx == tx:
            continue

        changes.append((name_ja or name_en, entry.get("species", ""), target))
        stats[target] = stats.get(target, 0) + 1
        if apply:
            entry["treatment_ja"] = new_tx

    print(f"{'APPLIED' if apply else 'DRY-RUN'} treatment remediation:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"  total: {sum(stats.values())}")
    print("\nChanged entries:")
    for name, sp, tgt in changes:
        print(f"  [{tgt}] {name} ({sp})")
    return stats


def main() -> None:
    apply = "--apply" in sys.argv
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    remediate(data, apply)
    if apply:
        with open(JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"\nWrote {JSON_PATH}")
    else:
        print("\n(dry-run; pass --apply to write)")


if __name__ == "__main__":
    main()
