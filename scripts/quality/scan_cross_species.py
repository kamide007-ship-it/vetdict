#!/usr/bin/env python3
"""Cross-species contamination scanner (READ-ONLY).

An earlier enrichment pass stamped a "<Species>における…" framing onto disease
records. When that label names a species OTHER than the record's own, the
Japanese content was copied from the wrong species class — e.g. a hamster
Diabetes entry framed as "オウム（parrot）における…", or a bird Candidiasis
entry framed as "両生類（amphibian）における…". This is the same class of bug
as the degu otitis "爬虫類における…" contamination.

This scanner flags every JA field whose text carries a *foreign* species'
"<label>における" framing. It never mutates data — it only reports, so the fix
can be reviewed per species/severity.

Severity:
  * cross-class  — mammal/bird/reptile/amphibian/fish framing landing on a
    record of a different class (e.g. hamster ← parrot). Content is almost
    certainly wrong.
  * within-class — a label wrong only within a class (reptile ↔ lizard,
    bird ↔ parrot ↔ parakeet). Usually a mislabel; content may still be
    class-appropriate. Lower severity.

Usage:
    python3 scripts/quality/scan_cross_species.py            # print summary
    python3 scripts/quality/scan_cross_species.py --json     # machine-readable
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.quality.detect import ALL_SPECIES, load_species_records  # noqa: E402

SP_JA = {
    "dog": "犬", "cat": "猫", "horse": "馬", "rabbit": "ウサギ", "hamster": "ハムスター",
    "guinea_pig": "モルモット", "chinchilla": "チンチラ", "ferret": "フェレット", "hedgehog": "ハリネズミ",
    "sugar_glider": "フクロモモンガ", "degu": "デグー", "bird": "鳥", "parakeet": "インコ", "parrot": "オウム",
    "reptile": "爬虫類", "tortoise": "リクガメ", "snake": "ヘビ", "lizard": "トカゲ", "amphibian": "両生類",
    "fish": "魚",
}  # fmt: skip
# Class membership for within-class vs cross-class severity.
CLASS = {
    "mammal": {"dog", "cat", "horse", "rabbit", "hamster", "guinea_pig", "chinchilla",
               "ferret", "hedgehog", "sugar_glider", "degu"},
    "bird": {"bird", "parakeet", "parrot"},
    "reptile": {"reptile", "tortoise", "snake", "lizard"},
    "amphibian": {"amphibian"},
    "fish": {"fish"},
}  # fmt: skip
ALIAS = {"爬虫類": {"reptile", "tortoise", "snake", "lizard"}, "鳥類": {"bird", "parakeet", "parrot"}}
LABEL_TO_SPECIES = {ja: sp for sp, ja in SP_JA.items()}
ALL_LABELS = set(SP_JA.values()) | set(ALIAS)
FIELDS = ("treatment_ja", "causes_ja", "pathophysiology_ja", "description_ja", "prevention_ja", "prognosis_ja")
# comparative phrasing that legitimately names another species
COMPARATIVE = ("異な", "同様", "比べ", "違い", "より", "以外")


def _class_of(sp: str) -> str:
    for cls, members in CLASS.items():
        if sp in members:
            return cls
    return "other"


def _own_labels(sp: str) -> set[str]:
    labs = {SP_JA[sp]}
    for al, members in ALIAS.items():
        if sp in members:
            labs.add(al)
    return labs


def _label_species(label: str) -> set[str]:
    if label in ALIAS:
        return ALIAS[label]
    sp = LABEL_TO_SPECIES.get(label)
    return {sp} if sp else set()


def scan() -> dict:
    out: dict[str, list[dict]] = {}
    for sp in ALL_SPECIES:
        if sp not in SP_JA:  # exotic_other: mixed bucket, framing is inherently mixed
            continue
        own = _own_labels(sp)
        own_cls = _class_of(sp)
        for r in load_species_records(sp, served=False):
            for f in FIELDS:
                v = r.get(f) or ""
                for lab in ALL_LABELS:
                    if lab in own or (lab + "における") not in v:
                        continue
                    idx = v.find(lab + "における")
                    if any(x in v[max(0, idx - 6) : idx] for x in COMPARATIVE):
                        continue
                    foreign_cls = {_class_of(s) for s in _label_species(lab)}
                    severity = "within-class" if own_cls in foreign_cls else "cross-class"
                    out.setdefault(sp, []).append(
                        {
                            "name": r.get("name"),
                            "field": f,
                            "foreign_label": lab,
                            "severity": severity,
                            "snippet": v[idx : idx + 30],
                        }
                    )
                    break
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Read-only cross-species contamination scanner")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args()
    report = scan()
    total = sum(len(v) for v in report.values())
    cross = sum(1 for v in report.values() for h in v if h["severity"] == "cross-class")
    if args.json:
        print(json.dumps({"species": report, "total": total, "cross_class": cross}, ensure_ascii=False, indent=2))
        return 0
    print("=== cross-species contamination ('<other-species>における' framing) ===")
    print(f"species affected: {len(report)} | fields: {total} | cross-class: {cross}\n")
    for sp, hits in sorted(report.items(), key=lambda kv: -len(kv[1])):
        cc = sum(1 for h in hits if h["severity"] == "cross-class")
        print(f"--- {sp}: {len(hits)} ({cc} cross-class) ---")
        for h in hits:
            print(f"    [{h['severity']:12}] [{h['name']}] {h['field']}: {h['snippet']}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
