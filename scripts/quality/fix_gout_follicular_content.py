#!/usr/bin/env python3
"""Disease-specific rewrites for two clinically-coherent groups whose causes /
pathophysiology were left as generic category templates after the cross-species
relabel pass (surfaced in .spec/BATCH2_CONTAMINATION_FIX_REVIEW.md).

  1. GOUT family (birds + reptiles are uricotelic; amphibians handled cautiously)
     — replaces the generic '代謝・内分泌疾患' / grounded '…における代謝性の…' /
       parakeet '臓器機能障害、ホルモンバランス異常…' templates with the standard
       uric-acid pathophysiology, distinguished by articular vs visceral vs pre-gout.
       Mirrors the vet-approved lizard gout content.
  2. FOLLICULAR STASIS — fixes pathophysiology miscategorised as '消化器疾患' (GI)
     to the correct reproductive (ovarian) description.

Only fields that match a *generic-template marker* are replaced; already
disease-specific entries (e.g. reptile Articular Gout, parrot, lizard) are left
untouched. Both module `.py` (source of truth) and the JSON overlay (scoped by
species) are patched. Backed up, idempotent.

    python3 scripts/quality/fix_gout_follicular_content.py --ts <ts> [--apply]
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

SP_JA = {"bird": "鳥", "parakeet": "インコ", "parrot": "オウム", "reptile": "爬虫類",
         "tortoise": "リクガメ", "snake": "ヘビ", "lizard": "トカゲ", "amphibian": "両生類"}  # fmt: skip
JSON_CAP = {"bird": "Bird", "parakeet": "Parakeet", "parrot": "Parrot", "reptile": "Reptile",
            "tortoise": "Tortoise", "snake": "Snake", "lizard": "Lizard", "amphibian": "Amphibian"}  # fmt: skip
BIRDS = {"bird", "parakeet", "parrot"}

# generic-template markers — a field is replaceable only if it matches one
PATHO_GENERIC = ("代謝・内分泌疾患である", "代謝性の泌尿器系疾患", "代謝性の筋骨格系疾患")
CAUSES_GENERIC = ("における代謝性の", "臓器機能障害、ホルモンバランス異常")
FOLLIC_GI_MARKER = "における消化器疾患である"
# a value is only ever overwritten if it still matches one of these generic
# templates — a hard guard so good, disease-specific content is never clobbered.
GENERIC_ALL = (*PATHO_GENERIC, *CAUSES_GENERIC, FOLLIC_GI_MARKER)


def _is_generic(val: str) -> bool:
    return any(m in (val or "") for m in GENERIC_ALL)


def _sp_ja(sp: str) -> str:
    return SP_JA[sp]


def gout_type(name: str) -> str:
    n = name.lower()
    if "pre-gout" in n or "hyperuric" in n or "高尿酸" in name or "前" in name:
        return "pregout"
    art = ("articular" in n) or ("関節" in name)
    vis = ("visceral" in n) or ("内臓" in name)
    if art and not vis:
        return "articular"
    if vis and not art:
        return "visceral"
    return "both"


def gout_causes(sp: str, t: str) -> str:
    s = _sp_ja(sp)
    if sp == "amphibian":
        site = {"articular": "関節周囲", "visceral": "内臓表面", "both": "関節や内臓表面",
                "pregout": "組織"}[t]  # fmt: skip
        return (
            f"{s}における痛風の原因: 両生類は主にアンモニア・尿素を排泄するため痛風はまれだが、"
            f"重度の腎機能不全・慢性脱水下では血中尿酸／尿酸塩が上昇し、尿酸塩結晶が{site}に沈着しうる。"
        )
    if t == "articular":
        return (
            f"{s}における関節痛風の原因: 尿酸排泄型の代謝ゆえ、腎機能不全・慢性脱水・高蛋白食・"
            f"腎毒性薬（アミノグリコシド・NSAIDs）等により高尿酸血症が持続すると、尿酸ナトリウム結晶が"
            f"四肢関節・腱鞘に沈着する。"
        )
    if t == "visceral":
        return (
            f"{s}における内臓痛風の原因: 重度・末期の腎不全や高度脱水による著明な高尿酸血症で、"
            f"尿酸結晶が心膜・肝・腎・漿膜など内臓表面に広汎に沈着する。しばしば致死的。"
        )
    if t == "pregout":
        return (
            f"{s}における高尿酸血症・痛風前状態の原因: 腎機能低下・脱水・高蛋白食による血中尿酸の上昇で、"
            f"まだ結晶沈着（痛風）に至っていない前段階。早期是正で痛風への進展を防げる。"
        )
    return (
        f"{s}における痛風の原因: 尿酸排泄型の代謝で、腎機能不全・脱水・高蛋白食等による高尿酸血症から、"
        f"尿酸結晶が関節（関節型）や内臓漿膜（内臓型）に沈着する。"
    )


def gout_patho(sp: str, t: str) -> str:
    s = _sp_ja(sp)
    if sp == "amphibian":
        return (
            f"痛風は{s}ではまれな尿酸沈着性疾患である。腎機能の高度低下・慢性脱水により尿酸塩結晶が"
            f"関節や内臓表面に沈着し、疼痛・臓器機能障害を生じる。"
        )
    if t == "articular":
        return (
            f"関節痛風は{s}における尿酸代謝異常である。尿酸排泄型の代謝ゆえ腎障害・脱水下で高尿酸血症が進むと、"
            f"尿酸ナトリウム結晶が四肢関節・腱鞘に沈着してトーファス（痛風結節）を形成し、疼痛・関節腫脹・跛行・"
            f"可動域制限を生じる。慢性進行例では関節破壊に至る。"
        )
    if t == "visceral":
        return (
            f"内臓痛風は{s}における尿酸代謝異常である。高度の高尿酸血症により尿酸結晶が心膜・肝・腎・漿膜面など"
            f"内臓に沈着し、多臓器機能不全を来す。急性・末期腎不全に伴うことが多く予後不良。"
        )
    if t == "pregout":
        return (
            f"高尿酸血症は{s}における痛風の前段階である。尿酸の産生過剰ないし腎排泄低下により血中尿酸が上昇し、"
            f"放置すると尿酸ナトリウム結晶が関節・内臓に沈着して痛風へ移行する。"
        )
    return (
        f"痛風は{s}における尿酸代謝異常である。持続する高尿酸血症により尿酸ナトリウム結晶が関節や内臓に沈着し、"
        f"関節型では疼痛・腫脹・跛行を、内臓型では多臓器不全を来す。"
    )


def follic_patho(sp: str) -> str:
    s = _sp_ja(sp)
    return (
        f"卵胞停滞は{s}における生殖器（卵巣）疾患である。排卵に至らない卵胞が卵巣に停滞・貯留し、"
        f"腹腔内圧迫・食欲不振・卵黄性体腔炎・二次感染のリスクを生じる。ホルモン失調、不適切な環境"
        f"（温度・営巣場所・栄養）、肥満などが誘因となる。"
    )


def build_plan() -> dict[str, list[tuple[str, str, str, str]]]:
    """{species: [(name, field, old, new), …]} — only generic fields."""
    from scripts.quality.detect import load_species_records  # noqa: PLC0415

    plan: dict[str, list] = {}
    for sp in SP_JA:
        for r in load_species_records(sp, served=False):
            name = r.get("name") or ""
            name_ja = r.get("name_ja") or ""
            is_gout = "Gout" in name or "Hyperuric" in name or "痛風" in name_ja or "高尿酸" in name_ja
            is_follic = "Follicular Stasis" in name or "卵胞停滞" in name_ja or "濾胞停滞" in name_ja
            if is_gout:
                t = gout_type(name or name_ja)
                for field, gen_new in (("causes_ja", gout_causes(sp, t)), ("pathophysiology_ja", gout_patho(sp, t))):
                    cur = r.get(field) or ""
                    markers = CAUSES_GENERIC if field == "causes_ja" else PATHO_GENERIC
                    if any(m in cur for m in markers) and cur != gen_new:
                        plan.setdefault(sp, []).append((name, field, cur, gen_new))
            elif is_follic:
                cur = r.get("pathophysiology_ja") or ""
                if FOLLIC_GI_MARKER in cur:
                    plan.setdefault(sp, []).append((name, "pathophysiology_ja", cur, follic_patho(sp)))
    return plan


def _replace_in_module(sp: str, targets, apply: bool, log: list) -> None:
    path = REPO / f"api/species/{sp}_diseases.py"
    text = path.read_text(encoding="utf-8")
    orig = text
    mod = importlib.import_module(f"api.species.{sp}_diseases")
    raw = {}
    for d in mod.DISEASES:
        raw.setdefault(d.get("name"), []).append(d)
    for name, field, _cur_loader, new in targets:
        done = False
        for d in raw.get(name, []):
            src = d.get(field)
            if src == new:
                log.append(f"MODULE {sp}: {name}.{field} already (skip)")
                done = True
            elif src and _is_generic(src) and src in text:
                text = text.replace(src, new)
                log.append(f"MODULE {sp}: {name}.{field} rewritten")
                done = True
        if not done:
            log.append(f"· MODULE {sp}: {name}.{field} not in module (JSON-only)")
    if apply and text != orig:
        path.write_text(text, encoding="utf-8")


def _replace_in_json(plan, apply: bool, log: list) -> None:
    want = {(JSON_CAP[sp], name, field): new for sp, items in plan.items() for (name, field, _c, new) in items}
    with (REPO / "diseases_all_species.json").open(encoding="utf-8") as f:
        data = json.load(f)
    changed = 0
    for rec in data:
        for field in ("causes_ja", "pathophysiology_ja"):
            new = want.get((rec.get("species"), rec.get("name"), field))
            cur = rec.get(field)
            if new and cur != new and _is_generic(cur):
                rec[field] = new
                changed += 1
    if apply and changed:
        with (REPO / "diseases_all_species.json").open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    log.append(f"JSON changed fields: {changed}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ts", required=True)
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    plan = build_plan()

    if args.apply:
        bdir = REPO / "backups" / args.ts
        bdir.mkdir(parents=True, exist_ok=True)
        for sp in plan:
            p = REPO / f"api/species/{sp}_diseases.py"
            shutil.copy2(p, bdir / p.name)
        print(f"backup → {bdir}")

    log: list[str] = []
    for sp in plan:
        _replace_in_module(sp, plan[sp], args.apply, log)
    _replace_in_json(plan, args.apply, log)
    for line in log:
        print(line)
    total = sum(len(v) for v in plan.values())
    print(f"target fields: {total} across {len(plan)} species")
    print("APPLIED" if args.apply else "DRY-RUN")
    return 0


if __name__ == "__main__":
    sys.exit(main())
