"""Strip herbivore/avian enumeration clauses from the JSON overlay (2026-10 第76弾).

The digestive and dental category generators appended the same multi-taxon
sentences to every species' record — e.g. dog GDV prevention ending with
"草食動物（ウサギ・モルモット・チンチラ・デグー）: 高繊維チモシー乾草を給与量の80%以上",
cat periodontal prevention recommending a cuttlebone for "鳥類", and English causes
"In herbivores, insufficient dietary fibre…". The served DB build and the SPA
browse path strip these at read time (``strip_cross_species_clauses``); this
script applies the same, sentence-level rule to the overlay itself so SEO pages
and any other consumer see clean text too. Only whole, self-contained sentences
(or one listed inline item) are removed; owners (herbivores / birds) keep them.

Usage: python3 -m scripts.template_elimination.strip_cross_taxon_gi_dental_clauses [--apply]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from api.species.helpers import strip_cross_species_clauses  # noqa: E402

JSON_PATH = ROOT / "diseases_all_species.json"


def species_id(label: str) -> str:
    return label.strip().lower().replace(" ", "_")


def main(apply: bool) -> int:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    recs = data if isinstance(data, list) else data["diseases"]
    changed = 0
    for rec in recs:
        sp = species_id(rec.get("species") or "")
        if sp == "multiple":
            continue
        before = dict(rec)
        strip_cross_species_clauses(rec, sp)
        changed += sum(1 for k in rec if rec[k] != before.get(k))
    print(f"fields changed: {changed}")
    if apply and changed:
        JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return changed


if __name__ == "__main__":
    main("--apply" in sys.argv)
