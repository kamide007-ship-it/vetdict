#!/usr/bin/env python3
"""Batch-2 cross-species contamination relabels for the remaining 7 species
(bird, parakeet, parrot, tortoise, snake, sugar_glider, reptile).

Every field handled here is a SAFE relabel: the disease genuinely occurs in the
record's own species and the etiology/pathophysiology text is generic — only the
"<foreign-species>における" framing word is wrong. Swapping it to the record's own
species introduces NO new clinical claim (pure correction).

Two genuinely cross-class CLINICAL cases are deliberately EXCLUDED (they need a
vet-reviewed rewrite, not a relabel) and are handled in a separate worksheet:
  - parrot   Atherosclerosis            (budgerigar-specific epidemiology)
  - sugar_glider Proptosis (Eye Prolapse) (reptile abscess content vs mammal trauma)

Both the source-of-truth module `.py` and the JSON overlay (scoped by species so
the legitimate source-species entries are never touched) are corrected.
Backed up, idempotent (re-run = byte-identical), read each layer's own value.

    python3 scripts/quality/fix_cross_species_batch2.py --ts 2026-07-21-XXXX [--apply]
"""

from __future__ import annotations

import argparse
import importlib
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts.quality.scan_cross_species import ALIAS, SP_JA, scan  # noqa: E402

SPECIES = ["bird", "parakeet", "parrot", "tortoise", "snake", "sugar_glider", "reptile"]
OWN_JA = {"bird": "鳥", "parakeet": "インコ", "parrot": "オウム", "tortoise": "リクガメ",
          "snake": "ヘビ", "sugar_glider": "フクロモモンガ", "reptile": "爬虫類"}  # fmt: skip
JSON_CAP = {"bird": "Bird", "parakeet": "Parakeet", "parrot": "Parrot", "tortoise": "Tortoise",
            "snake": "Snake", "sugar_glider": "Sugar Glider", "reptile": "Reptile"}  # fmt: skip
FIELDS = ("treatment_ja", "causes_ja", "pathophysiology_ja", "description_ja", "prevention_ja", "prognosis_ja")
ALL_LABELS = set(SP_JA.values()) | set(ALIAS)
COMPARATIVE = ("異な", "同様", "比べ", "違い", "より", "以外")

# vet-review clinical cases — never relabelled here
C_EXCLUDE = {("parrot", "Atherosclerosis"), ("sugar_glider", "Proptosis (Eye Prolapse)")}


def _own_labels(sp: str) -> set[str]:
    labs = {SP_JA[sp]}
    for al, members in ALIAS.items():
        if sp in members:
            labs.add(al)
    return labs


def swap_framing(val: str, sp: str) -> str | None:
    """Swap the first *foreign* '<label>における' framing to the own-species label.
    Mirrors the scanner's guards (comparative phrasing, kanji-preceded compound).
    Returns the new string, or None if nothing to change."""
    if not val:
        return None
    own = _own_labels(sp)
    own_ja = OWN_JA[sp]
    best = None
    for lab in ALL_LABELS:
        if lab in own:
            continue
        key = lab + "における"
        idx = val.find(key)
        if idx < 0:
            continue
        if any(x in val[max(0, idx - 6) : idx] for x in COMPARATIVE):
            continue
        if idx > 0 and "一" <= val[idx - 1] <= "鿿":  # kanji-preceded compound (幼鳥 …)
            continue
        if best is None or idx < best[0]:
            best = (idx, lab)
    if best is None:
        return None
    _, lab = best
    return val.replace(lab + "における", own_ja + "における", 1)


def collect_targets() -> dict[str, set[tuple[str, str]]]:
    """{species: {(name, field), …}} from the scanner, minus the C-cases."""
    report = scan()
    out: dict[str, set[tuple[str, str]]] = {}
    for sp in SPECIES:
        for h in report.get(sp, []):
            if (sp, h["name"]) in C_EXCLUDE:
                continue
            out.setdefault(sp, set()).add((h["name"], h["field"]))
    return out


def patch_modules(targets, apply: bool) -> list[str]:
    log = []
    for sp in SPECIES:
        if sp not in targets:
            continue
        path = REPO / f"api/species/{sp}_diseases.py"
        text = path.read_text(encoding="utf-8")
        orig = text
        mod = importlib.import_module(f"api.species.{sp}_diseases")
        by_name: dict[str, list[dict]] = {}
        for d in mod.DISEASES:
            by_name.setdefault(d.get("name"), []).append(d)
        for name, field in sorted(targets[sp]):
            for d in by_name.get(name, []):
                cur = d.get(field)
                new = swap_framing(cur or "", sp)
                if not new or new == cur:
                    if cur and new is None:
                        log.append(f"MODULE {sp}: {name}.{field} already clean (skip)")
                    continue
                if cur in text:
                    # raw field value is verbatim in source
                    text = text.replace(cur, new)
                    log.append(f"MODULE {sp}: {name}.{field} relabelled")
                    continue
                # enriched field (e.g. treatment_ja gets an ECVN suffix at import):
                # swap only the leading disease-specific framing snippet, which IS
                # verbatim in the raw source (the enrichment is a suffix).
                snip_old = (cur or "")[:24]
                snip_new = swap_framing(snip_old, sp)
                if snip_new and snip_new != snip_old and text.count(snip_old) == 1:
                    text = text.replace(snip_old, snip_new)
                    log.append(f"MODULE {sp}: {name}.{field} relabelled (snippet)")
                else:
                    log.append(f"⚠️ MODULE {sp}: {name}.{field} NOT matched — SKIP")
        if apply and text != orig:
            path.write_text(text, encoding="utf-8")
    return log


def patch_json(targets, apply: bool) -> list[str]:
    log = []
    want = {(JSON_CAP[sp], name, field): sp for sp in targets for (name, field) in targets[sp]}
    with (REPO / "diseases_all_species.json").open(encoding="utf-8") as f:
        data = json.load(f)
    changed = 0
    for rec in data:
        sp_cap = rec.get("species")
        name = rec.get("name")
        for field in FIELDS:
            sp = want.get((sp_cap, name, field))
            if not sp:
                continue
            cur = rec.get(field)
            new = swap_framing(cur or "", sp)
            if new and new != cur:
                rec[field] = new
                changed += 1
                log.append(f"JSON {sp_cap}: {name}.{field} relabelled")
    if apply and changed:
        with (REPO / "diseases_all_species.json").open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    log.append(f"JSON changed fields: {changed}")
    return log


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ts", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    targets = collect_targets()

    if args.apply:
        bdir = REPO / "backups" / args.ts
        bdir.mkdir(parents=True, exist_ok=True)
        for sp in targets:
            p = REPO / f"api/species/{sp}_diseases.py"
            shutil.copy2(p, bdir / p.name)
        with (REPO / "diseases_all_species.json").open(encoding="utf-8") as f:
            data = json.load(f)
        caps = {JSON_CAP[sp] for sp in targets}
        subset = [r for r in data if r.get("species") in caps]
        (bdir / "diseases_all_species.batch2_subset.json").write_text(
            json.dumps(subset, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"backup → {bdir}")

    for line in patch_modules(targets, args.apply):
        print(line)
    for line in patch_json(targets, args.apply):
        print(line)
    total = sum(len(v) for v in targets.values())
    print(f"target (name,field) pairs: {total}")
    print("APPLIED" if args.apply else "DRY-RUN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
