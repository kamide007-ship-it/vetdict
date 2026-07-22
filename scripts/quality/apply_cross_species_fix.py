#!/usr/bin/env python3
"""Apply the vet-approved (A: label-swap, B: clinical-draft) cross-species
contamination fixes to the species disease modules.

Approval: Kentaro DVM — "ABを採用" (adopt A = mechanical label swaps, and
B = the clinical draft rewrites from the .spec/*_CONTAMINATION_FIX_REVIEW.md
worksheets). C (T106 dosage publish) is NOT covered here and is left gated.

Scope: all 65 fields flagged by scripts/quality/scan_cross_species.py across
9 species. Every flagged field is served from the module (overlay=False,
verified), so this edits ONLY api/species/<species>_diseases.py — no JSON
overlay surgery.

Modes per field:
  * label   — swap the foreign "<species>における" framing for the record's own
              species label; clinical content is otherwise unchanged.
  * rewrite — replace the field value with the worksheet's vet-approved draft
              (used where the content/category was clinically wrong, e.g. gout
              framed as an endocrine template, heatstroke as trauma, heavy-metal
              antidotes VitK1/NAC instead of CaEDTA).

Idempotent: re-running yields byte-identical files (already-applied fields are
skipped). Backs up every touched module to backups/<timestamp>/ before writing.

Usage:
    python3 scripts/quality/apply_cross_species_fix.py --dry-run
    python3 scripts/quality/apply_cross_species_fix.py --apply
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SPECIES_DIR = REPO / "api" / "species"

OWN = {
    "sugar_glider": "フクロモモンガ", "bird": "鳥", "parakeet": "インコ",
    "parrot": "オウム", "reptile": "爬虫類", "tortoise": "リクガメ",
    "snake": "ヘビ", "lizard": "トカゲ", "hamster": "ハムスター",
}  # fmt: skip


def lbl(foreign: str) -> dict:
    return {"mode": "label", "foreign": foreign}


def rw(text: str) -> dict:
    return {"mode": "rewrite", "text": text}


# (species, english name, field) -> action. Faithful to the worksheets.
SPEC: list[tuple[str, str, str, dict]] = [
    # ---- sugar_glider ----
    (
        "sugar_glider",
        "Proptosis (Eye Prolapse)",
        "treatment_ja",
        rw(
            "フクロモモンガにおける眼球突出症の治療は緊急対応が原則。突出が軽度で角膜・視神経が保たれる"
            "場合は潤滑・保護下に用手整復と一時的眼瞼縫合を試みる。重度の脱出・眼球破裂・不可逆性視力喪失"
            "では眼球摘出を選択する。全身鎮痛・抗炎症、二次感染予防の抗菌薬、原因（外傷・咬傷・後眼窩病変）"
            "の検索を併せて行う。"
        ),
    ),
    (
        "sugar_glider",
        "Proptosis (Eye Prolapse)",
        "causes_ja",
        rw(
            "フクロモモンガにおける眼球突出症の原因: 外傷・咬傷・不適切なハンドリングによる眼球の異常突出が"
            "多く、後眼窩膿瘍・占拠性病変、緑内障による牛眼なども原因となる。"
        ),
    ),
    ("sugar_glider", "Nutritional Osteodystrophy", "causes_ja", lbl("リクガメ")),
    ("sugar_glider", "Nutritional Osteodystrophy", "pathophysiology_ja", lbl("リクガメ")),
    # ---- bird (all label-only) ----
    ("bird", "Candidiasis", "causes_ja", lbl("両生類")),
    ("bird", "Candidiasis", "pathophysiology_ja", lbl("両生類")),
    ("bird", "Mucormycosis (Zygomycosis)", "causes_ja", lbl("トカゲ")),
    ("bird", "Mucormycosis (Zygomycosis)", "pathophysiology_ja", lbl("トカゲ")),
    ("bird", "Cloacal Papillomatosis", "causes_ja", lbl("オウム")),
    ("bird", "Egg Binding (Dystocia)", "pathophysiology_ja", lbl("両生類")),
    ("bird", "Atoxoplasmosis", "treatment_ja", lbl("インコ")),
    ("bird", "Atoxoplasmosis", "causes_ja", lbl("インコ")),
    ("bird", "Atoxoplasmosis", "pathophysiology_ja", lbl("インコ")),
    ("bird", "Avian Nephropathy", "causes_ja", lbl("オウム")),
    ("bird", "Avian Nephropathy", "pathophysiology_ja", lbl("オウム")),
    ("bird", "Smoke Inhalation", "causes_ja", lbl("インコ")),
    ("bird", "Smoke Inhalation", "pathophysiology_ja", lbl("インコ")),
    # ---- parakeet (gout rewrites + label) ----
    (
        "parakeet",
        "Gout (Visceral)",
        "causes_ja",
        rw(
            "インコにおける内臓痛風の原因: 鳥は尿酸排泄型のため、腎機能低下・脱水・高蛋白/高Ca食・"
            "ビタミンA欠乏による高尿酸血症が持続すると、尿酸ナトリウム結晶が肝・腎・心膜など内臓漿膜面に"
            "沈着する。"
        ),
    ),
    (
        "parakeet",
        "Gout (Visceral)",
        "pathophysiology_ja",
        rw(
            "内臓痛風はインコにおける尿酸代謝異常である。持続する高尿酸血症により尿酸塩結晶が内臓漿膜面"
            "（心膜・肝・腎表面）に沈着し、臓器機能不全を来す。内臓型は予後不良のことが多い。"
        ),
    ),
    (
        "parakeet",
        "Gout (Articular)",
        "causes_ja",
        rw(
            "インコにおける関節痛風の原因: 鳥は尿酸排泄型のため、腎機能低下・脱水・高蛋白/高Ca食・"
            "ビタミンA欠乏による高尿酸血症が持続すると、尿酸ナトリウム結晶が趾・跗関節など関節周囲に"
            "沈着する。"
        ),
    ),
    (
        "parakeet",
        "Gout (Articular)",
        "pathophysiology_ja",
        rw(
            "関節痛風はインコにおける尿酸代謝異常である。持続する高尿酸血症により尿酸塩結晶が関節"
            "（趾・跗関節など）に沈着し、疼痛・腫脹・跛行を生じる。"
        ),
    ),
    ("parakeet", "Feather Follicle Cyst (Chronic)", "causes_ja", lbl("オウム")),
    ("parakeet", "Feather Follicle Cyst (Chronic)", "pathophysiology_ja", lbl("オウム")),
    ("parakeet", "Vitamin E / Selenium Deficiency", "causes_ja", lbl("オウム")),
    ("parakeet", "Vitamin E / Selenium Deficiency", "pathophysiology_ja", lbl("オウム")),
    # ---- parrot ----
    ("parrot", "Candidiasis", "causes_ja", lbl("両生類")),
    ("parrot", "Candidiasis", "pathophysiology_ja", lbl("両生類")),
    (
        "parrot",
        "Heavy Metal Poisoning (Lead/Zinc)",
        "treatment_ja",
        rw(
            "オウムにおける重金属中毒（鉛・亜鉛）の治療: CaEDTA によるキレート療法を主軸に、消化管内"
            "金属片の除去（そ嚢/砂嚢洗浄・内視鏡的摘出・下剤）、輸液で腎排泄を促進、痙攣・神経症状への"
            "対症、支持療法を行う。ビタミンK1やN-アセチルシステインは本中毒には適応でない。"
        ),
    ),
    ("parrot", "Heavy Metal Poisoning (Lead/Zinc)", "causes_ja", lbl("インコ")),
    ("parrot", "Heavy Metal Poisoning (Lead/Zinc)", "pathophysiology_ja", lbl("インコ")),
    (
        "parrot",
        "Atherosclerosis",
        "causes_ja",
        rw(
            "オウムにおける動脈硬化症の原因: 動脈壁へのコレステロール・脂質沈着によるプラーク形成。"
            "高脂・種子偏重食、運動不足、加齢が関与し、高齢の中〜大型オウム（ヨウム・コンゴウインコ等）"
            "で好発する。"
        ),
    ),
    (
        "parrot",
        "Atherosclerosis",
        "pathophysiology_ja",
        rw(
            "動脈硬化症はオウムにおける循環器疾患である。動脈壁への脂質・コレステロール沈着でプラークが"
            "形成され、血管内腔の狭窄・硬化により血流障害と臓器灌流低下を来す。進行すると虚脱や突然死の"
            "原因となる。"
        ),
    ),
    ("parrot", "Cloacal Papilloma", "causes_ja", lbl("インコ")),
    # ---- reptile (soft rewrite to drop the '<lizard>における' framing while
    #      keeping the correct susceptible-subgroup meaning) ----
    (
        "reptile",
        "Ivermectin Toxicosis",
        "description_ja",
        rw("カメや小型トカゲで特に重篤となるイベルメクチン過剰投与による神経毒性。"),
    ),
    ("reptile", "Chronic Respiratory Disease Complex", "causes_ja", lbl("トカゲ")),
    ("reptile", "Chronic Respiratory Disease Complex", "pathophysiology_ja", lbl("トカゲ")),
    # ---- tortoise ----
    ("tortoise", "Articular Gout", "causes_ja", lbl("鳥")),
    (
        "tortoise",
        "Articular Gout",
        "pathophysiology_ja",
        rw(
            "関節痛風はリクガメにおける尿酸代謝異常である。脱水・高蛋白食・腎機能低下による高尿酸血症で"
            "尿酸塩結晶が関節に沈着し、疼痛・腫脹・運動障害を生じる。"
        ),
    ),
    ("tortoise", "Visceral Gout", "causes_ja", lbl("鳥")),
    (
        "tortoise",
        "Visceral Gout",
        "pathophysiology_ja",
        rw(
            "内臓痛風はリクガメにおける尿酸代謝異常である。高尿酸血症により尿酸塩結晶が内臓漿膜面・腎に"
            "沈着し、臓器機能不全を来す。内臓型は予後不良のことが多い。"
        ),
    ),
    ("tortoise", "Follicular Stasis (Chronic)", "causes_ja", lbl("トカゲ")),
    (
        "tortoise",
        "Follicular Stasis (Chronic)",
        "pathophysiology_ja",
        rw(
            "慢性濾胞停滞はリクガメにおける生殖器疾患である。排卵に至らない卵胞が卵巣に停滞し、卵黄性"
            "体腔炎・卵閉塞・全身状態悪化のリスクとなる。低Ca・栄養/環境不良・雄不在などが誘因となる。"
        ),
    ),
    ("tortoise", "Chronic Respiratory Disease Complex", "causes_ja", lbl("トカゲ")),
    ("tortoise", "Chronic Respiratory Disease Complex", "pathophysiology_ja", lbl("トカゲ")),
    # ---- snake ----
    ("snake", "Articular Gout", "causes_ja", lbl("鳥")),
    (
        "snake",
        "Articular Gout",
        "pathophysiology_ja",
        rw(
            "関節痛風はヘビにおける尿酸代謝異常である。脱水・高蛋白食・腎機能低下による高尿酸血症で"
            "尿酸塩結晶が関節に沈着し、疼痛・腫脹・運動障害を生じる。"
        ),
    ),
    ("snake", "Visceral Gout", "causes_ja", lbl("鳥")),
    (
        "snake",
        "Visceral Gout",
        "pathophysiology_ja",
        rw(
            "内臓痛風はヘビにおける尿酸代謝異常である。高尿酸血症により尿酸塩結晶が内臓漿膜面・腎に"
            "沈着し、臓器機能不全を来す。内臓型は予後不良のことが多い。"
        ),
    ),
    ("snake", "Spinal Osteopathy / Spondylosis", "causes_ja", lbl("トカゲ")),
    ("snake", "Spinal Osteopathy / Spondylosis", "pathophysiology_ja", lbl("トカゲ")),
    # ---- lizard ----
    (
        "lizard",
        "Nutritional Secondary Hyperparathyroidism (NSHP)",
        "causes_ja",
        rw(
            "トカゲにおける栄養性二次性副甲状腺機能亢進症（NSHP／代謝性骨疾患）の原因: 食事中の"
            "カルシウム:リン比の不均衡（低Ca・高P）、UVB照射不足によるビタミンD3合成障害、Ca・D3補給の"
            "不足。飼育下トカゲ（特に昆虫食・草食性種）で最も一般的な代謝性疾患の一つ。"
        ),
    ),
    (
        "lizard",
        "Nutritional Secondary Hyperparathyroidism (NSHP)",
        "pathophysiology_ja",
        rw(
            "NSHPはトカゲにおける代謝性骨疾患である。低Ca・高P食とUVB/D3不足により血中Caが低下し、"
            "上皮小体ホルモン（PTH）分泌が持続的に亢進する。PTHは骨からのCa動員を促し、線維性骨異栄養症"
            "（骨の菲薄化・変形・病的骨折）、下顎の柔化（ゴムあご）、テタニー・振戦・後肢麻痺を生じる。"
        ),
    ),
    ("lizard", "Articular Gout", "causes_ja", lbl("鳥")),
    (
        "lizard",
        "Articular Gout",
        "pathophysiology_ja",
        rw(
            "関節痛風はトカゲにおける尿酸代謝異常である。脱水・高蛋白食・腎機能低下による高尿酸血症で"
            "尿酸塩結晶が関節に沈着し、疼痛・腫脹・運動障害を生じる。"
        ),
    ),
    ("lizard", "Visceral Gout", "causes_ja", lbl("鳥")),
    (
        "lizard",
        "Visceral Gout",
        "pathophysiology_ja",
        rw(
            "内臓痛風はトカゲにおける尿酸代謝異常である。高尿酸血症により尿酸塩結晶が内臓漿膜面・腎に"
            "沈着し、臓器機能不全を来す。"
        ),
    ),
    ("lizard", "UV Light Deficiency", "causes_ja", lbl("両生類")),
    (
        "lizard",
        "UV Light Deficiency",
        "pathophysiology_ja",
        rw(
            "紫外線不足症はトカゲにおける代謝性骨疾患の一因である。多くのトカゲは皮膚での前駆体からの"
            "ビタミンD3合成にUVB（290–315 nm）を必要とし、UVB不足下ではD3が不足して腸管Ca吸収が低下する。"
            "結果として低Ca血症・NSHP（代謝性骨疾患）を招き、UV不足症とNSHPは連続した病態として扱う。"
        ),
    ),
    # ---- hamster ----
    (
        "hamster",
        "Diabetes Mellitus",
        "causes_ja",
        rw(
            "ハムスターにおける糖尿病の原因: 膵島β細胞機能障害・インスリン抵抗性による高血糖。"
            "チャイニーズハムスターは自然発症糖尿病の古典的モデルであり、ジャンガリアン／キャンベルの"
            "ドワーフハムスター（Phodopus）でも比較的多くみられる。高脂肪・高糖質食や肥満が発症・増悪に"
            "関与する。"
        ),
    ),
    (
        "hamster",
        "Diabetes Mellitus",
        "pathophysiology_ja",
        rw(
            "糖尿病はハムスターにおける内分泌代謝疾患である。インスリン分泌不全ないし作用不全により持続的"
            "高血糖を来し、多飲多尿・体重減少・白内障などを生じる。ドワーフハムスターでは変動しやすい"
            "血糖と自然寛解も報告され、食事管理（低糖質）が中心となる。"
        ),
    ),
    (
        "hamster",
        "Heatstroke",
        "treatment_ja",
        rw(
            "ハムスターにおける熱中症の治療は、速やかだが管理された冷却と循環支持を優先する。まず涼しい"
            "環境へ移し、常温〜微温水で体表を濡らす（氷水は末梢血管収縮・過冷却を招くため避ける）。目標"
            "体温付近で冷却を止め、過度の低体温を防ぐ。輸液（皮下／静脈内）で循環を支え、高体温による"
            "臓器障害に備える。DIC・急性腎障害・中枢神経症状をモニタリングし、必要に応じ酸素・対症療法を"
            "行う。予後は重症度と初期対応の速さに依存する。"
        ),
    ),
    ("hamster", "Heatstroke", "causes_ja", lbl("インコ")),
    (
        "hamster",
        "Heatstroke",
        "pathophysiology_ja",
        rw(
            "熱中症はハムスターにおける熱性の全身性疾患である。体温調節能を超える高温環境曝露により深部"
            "体温が上昇し、熱による細胞障害・血管内皮障害・全身性炎症反応を惹起する。進行すると多臓器"
            "不全（急性腎障害・肝障害・中枢神経障害）や播種性血管内凝固（DIC）を来し、迅速な冷却が行われ"
            "ないと致死的となる。"
        ),
    ),
    ("hamster", "Renal Amyloidosis", "causes_ja", lbl("フクロモモンガ")),
    (
        "hamster",
        "Renal Amyloidosis",
        "pathophysiology_ja",
        rw(
            "腎アミロイドーシスはハムスターにおける進行性腎疾患である。慢性炎症などに伴い産生された前駆"
            "蛋白（主にAA）がアミロイド線維として糸球体・間質に沈着し、濾過障害と進行性の腎機能低下"
            "（蛋白尿・多飲多尿・体重減少・終末期の尿毒症）を来す。高齢個体に多く、根治的治療は困難で"
            "対症・支持療法が中心となる。"
        ),
    ),
]

_ALL_LABELS = "|".join(map(re.escape, set(OWN.values()) | {"両生類", "鳥"}))


def _field_span(text: str, en_name: str, field: str) -> tuple[int, int, str] | None:
    """Return (value_start, value_end, current_value) for record `en_name`'s
    single-line `field` string literal, scoped between this record's name anchor
    and the next name anchor."""
    name_re = re.compile(r'"name":\s*"' + re.escape(en_name) + r'"')
    m = name_re.search(text)
    if not m:
        return None
    nxt = re.compile(r'"name":\s*"').search(text, m.end())
    block_end = nxt.start() if nxt else len(text)
    fld = re.compile(r'"' + re.escape(field) + r'":\s*"([^"\n]*)"')
    fm = fld.search(text, m.end(), block_end)
    if not fm:
        return None
    return fm.start(1), fm.end(1), fm.group(1)


def apply(dry: bool) -> int:
    touched: dict[str, str] = {}
    per_species: dict[str, list[str]] = {}
    already = 0
    for species, en_name, field, action in SPEC:
        path = SPECIES_DIR / f"{species}_diseases.py"
        src = touched.get(species) or path.read_text(encoding="utf-8")
        span = _field_span(src, en_name, field)
        if span is None:
            print(f"  !! NOT FOUND: {species} / {en_name} / {field}", file=sys.stderr)
            return 2
        vstart, vend, cur = span
        if action["mode"] == "label":
            own = OWN[species]
            foreign = action["foreign"]
            if f"{foreign}における" not in cur:
                if f"{own}における" in cur:
                    already += 1
                    continue
                print(f"  !! label token '{foreign}における' absent: {species}/{en_name}/{field}", file=sys.stderr)
                return 2
            new = cur.replace(f"{foreign}における", f"{own}における", 1)
        else:
            new = action["text"]
            if cur == new:
                already += 1
                continue
        touched[species] = src[:vstart] + new + src[vend:]
        per_species.setdefault(species, []).append(f"{en_name} / {field} [{action['mode']}]")

    print(
        f"planned edits: {sum(len(v) for v in per_species.values())} "
        f"| already-applied (skipped): {already} | species touched: {len(touched)}"
    )
    for sp, items in sorted(per_species.items()):
        print(f"  {sp}: {len(items)}")
        for it in items:
            print(f"      - {it}")

    if dry:
        print("\n(dry-run: no files written)")
        return 0

    if touched:
        ts = datetime.now().strftime("%Y-%m-%d-%H%M")
        bdir = REPO / "backups" / ts
        bdir.mkdir(parents=True, exist_ok=True)
        for sp in touched:
            shutil.copy2(SPECIES_DIR / f"{sp}_diseases.py", bdir / f"{sp}_diseases.py")
        print(f"backup: {bdir.relative_to(REPO)} ({len(touched)} modules)")
        for sp, new_src in touched.items():
            (SPECIES_DIR / f"{sp}_diseases.py").write_text(new_src, encoding="utf-8")
        print("written.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    return apply(dry=args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
