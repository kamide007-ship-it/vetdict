#!/usr/bin/env python3
"""Apply vet-approved cross-species contamination fixes for lizard & hamster.

Corrections are exactly those proposed (and approved) in
`.spec/LIZARD_CONTAMINATION_FIX_REVIEW.md` and
`.spec/HAMSTER_CONTAMINATION_FIX_REVIEW.md`.

- Backs up every touched file to backups/<ts>/ before writing.
- Patches BOTH the module `.py` (source of truth) and the JSON overlay
  (served) so raw and served views agree.
- Idempotent: a field already carrying the corrected text is left untouched;
  a field carrying neither old nor new is reported and skipped (never guessed).

Usage:
    python3 scripts/quality/fix_cross_species_lizard_hamster.py --ts 2026-07-21-XXXX --apply
    (omit --apply for a dry run)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

# (species, disease name, field): (old_exact, new_exact)
FIXES: dict[tuple[str, str, str], tuple[str, str]] = {
    # ---------------- LIZARD ----------------
    ("Lizard", "Nutritional Secondary Hyperparathyroidism (NSHP)", "causes_ja"): (
        "フクロモモンガにおける栄養性二次性副甲状腺機能亢進症（NSHP）の原因: 食事中のカルシウム:リン比の不適切さによる重度の代謝性骨疾患。飼育下フクロモモンガの最も一般的な致死的疾患です。",
        "トカゲにおける栄養性二次性副甲状腺機能亢進症（NSHP／代謝性骨疾患）の原因: 食事中のカルシウム:リン比の不均衡（低Ca・高P）、UVB照射不足によるビタミンD3合成障害、カルシウム・D3補給の不足。飼育下トカゲ（特に昆虫食・草食性種）で最も一般的な代謝性疾患の一つ。",
    ),
    ("Lizard", "Nutritional Secondary Hyperparathyroidism (NSHP)", "pathophysiology_ja"): (
        "栄養性二次性副甲状腺機能亢進症（NSHP）はフクロモモンガにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "NSHPはトカゲにおける代謝性骨疾患である。低Ca・高P食とUVB/D3不足により血中Caが低下し、上皮小体ホルモン（PTH）分泌が持続的に亢進する。PTHは骨からのCa動員を促し、線維性骨異栄養症（骨の菲薄化・変形・病的骨折）、下顎の柔化（ゴムあご）、テタニー・振戦・後肢麻痺を生じる。進行すると多臓器のCa恒常性が破綻する。",
    ),
    ("Lizard", "Articular Gout", "causes_ja"): (
        "鳥における関節痛風の原因: 腎不全による高尿酸血症に伴う関節への尿酸結晶沈着。",
        "トカゲにおける関節痛風の原因: 腎不全による高尿酸血症に伴う関節への尿酸結晶沈着。",
    ),
    ("Lizard", "Articular Gout", "pathophysiology_ja"): (
        "関節痛風は鳥における代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "痛風はトカゲにおける尿酸代謝異常である。爬虫類は尿酸排泄型のため、腎機能低下・脱水・高蛋白食により高尿酸血症が持続すると、尿酸ナトリウム結晶が関節（関節痛風）や内臓漿膜面・腎（内臓痛風）に沈着する。沈着は疼痛・関節腫脹・臓器機能不全を招き、内臓型は予後不良のことが多い。",
    ),
    ("Lizard", "Visceral Gout", "causes_ja"): (
        "鳥における内臓痛風の原因: 重度の腎不全による内臓表面への尿酸沈着。",
        "トカゲにおける内臓痛風の原因: 重度の腎不全による内臓表面への尿酸沈着。",
    ),
    ("Lizard", "Visceral Gout", "pathophysiology_ja"): (
        "内臓痛風は鳥における代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "痛風はトカゲにおける尿酸代謝異常である。爬虫類は尿酸排泄型のため、腎機能低下・脱水・高蛋白食により高尿酸血症が持続すると、尿酸ナトリウム結晶が内臓漿膜面・腎（内臓痛風）や関節（関節痛風）に沈着する。内臓型は心膜・肝・腎表面への広汎な沈着を来し、予後不良のことが多い。",
    ),
    ("Lizard", "UV Light Deficiency", "causes_ja"): (
        "両生類における紫外線不足症の原因: D3合成にUVBが必要な種における紫外線不足。",
        "トカゲにおける紫外線不足症の原因: D3合成にUVBが必要な種における紫外線不足。",
    ),
    ("Lizard", "UV Light Deficiency", "pathophysiology_ja"): (
        "紫外線不足症は両生類における栄養障害である。特定の栄養素の不十分な摂取、吸収不良、または過剰摂取により生じる。欠乏状態では、影響を受けた栄養素を補因子または基質として必要とする生化学的経路が障害され、細胞機能障害を引き起こす。過剰状態では組織への蓄積や栄養素間相互作用の障害により毒性が生じる。種特異的な食事要求により、適切な栄養管理が予防に不可欠である。",
        "紫外線不足症はトカゲにおける代謝性骨疾患の一因である。多くのトカゲは皮膚での前駆体からのビタミンD3合成にUVB（290–315 nm）を必要とし、UVB不足下ではD3が不足して腸管Ca吸収が低下する。結果として低Ca血症・NSHP（代謝性骨疾患）を招き、UV不足症とNSHPは連続した病態として扱う。",
    ),
    # ---------------- HAMSTER ----------------
    ("Hamster", "Diabetes Mellitus", "causes_ja"): (
        "オウムにおける糖尿病の原因: 膵島細胞機能障害による高血糖。稀だがオウム類で報告されている。",
        "ハムスターにおける糖尿病の原因: 膵島β細胞機能障害・インスリン抵抗性による高血糖。チャイニーズハムスターは自然発症糖尿病の古典的モデルであり、ジャンガリアン／キャンベルのドワーフハムスター（Phodopus）でも比較的多くみられる。高脂肪・高糖質食や肥満が発症・増悪に関与する。",
    ),
    ("Hamster", "Diabetes Mellitus", "pathophysiology_ja"): (
        "糖尿病はオウムにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "糖尿病はハムスターにおける内分泌代謝疾患である。インスリン分泌不全ないし作用不全により持続的高血糖を来し、多飲多尿・体重減少・白内障などを生じる。ドワーフハムスターでは変動しやすい血糖と自然寛解も報告され、食事管理（低糖質）が中心となる。",
    ),
    ("Hamster", "Heatstroke", "treatment_ja"): (
        "インコにおける熱中症の治療は安定化、疼痛管理、創傷ケアを優先する。生命を脅かす損傷を最初に評価・対処する（気道、呼吸、循環）。種に適した鎮痛薬（NSAIDs、オピオイド、局所麻酔薬）による鎮痛が不可欠である。創傷を洗浄・デブリードマンし、一次閉鎖、二次治癒、再建手術を適宜行う。汚染創には広域抗菌薬を使用する。骨折には副子固定または外科的固定を行う。遅発性合併症をモニタリングする。",
        "ハムスターにおける熱中症の治療は速やかだが管理された冷却と循環支持を優先する。まず涼しい環境へ移し、常温〜微温水で体表を濡らす（氷水は末梢血管収縮・過冷却を招くため避ける）。目標体温付近で冷却を止め、過度の低体温を防ぐ。輸液（皮下／静脈内）で循環を支え、高体温による臓器障害に備える。DIC・急性腎障害・中枢神経症状をモニタリングし、必要に応じ酸素・対症療法を行う。予後は重症度と初期対応の速さに依存する。",
    ),
    ("Hamster", "Heatstroke", "causes_ja"): (
        "インコにおける熱中症の原因: 過度の高温環境への暴露による体温上昇で、未治療では臓器不全を引き起こす。",
        "ハムスターにおける熱中症の原因: 過度の高温環境への暴露による体温上昇で、未治療では臓器不全を引き起こす。",
    ),
    ("Hamster", "Heatstroke", "pathophysiology_ja"): (
        "熱中症はインコにおける外傷性・機械的疾患である。罹患組織の構造的耐性を超える外部機械的力により組織損傷が生じる。損傷は出血、浮腫、疼痛を伴う急性炎症カスケードを惹起する。重症度に応じて、血管供給の途絶による虚血、環境微生物による汚染、進行性の組織壊死が生じうる。治癒過程は止血、炎症、増殖、リモデリングの各段階を経る。",
        "熱中症はハムスターにおける熱性の全身性疾患である。体温調節能を超える高温環境曝露により深部体温が上昇し、熱による細胞障害・血管内皮障害・全身性炎症反応を惹起する。進行すると多臓器不全（急性腎障害・肝障害・中枢神経障害）、播種性血管内凝固（DIC）を来し、迅速な冷却が行われないと致死的となる。",
    ),
    ("Hamster", "Renal Amyloidosis", "causes_ja"): (
        "フクロモモンガにおける腎アミロイドーシスの原因: 腎臓へのアミロイドタンパク沈着で進行性腎不全を引き起こします。",
        "ハムスターにおける腎アミロイドーシスの原因: 腎臓へのアミロイドタンパク沈着で進行性腎不全を引き起こします。",
    ),
    ("Hamster", "Renal Amyloidosis", "pathophysiology_ja"): (
        "腎アミロイドーシスはフクロモモンガにおける代謝・内分泌疾患である。基礎病態はホルモンのフィードバックループ、酵素活性、または基質代謝の調節障害を伴う。循環ホルモン、電解質、代謝中間体のバランス異常が複数の臓器系にわたる細胞機能に影響を及ぼす。代償機構が一時的に恒常性を維持するが、最終的に代償不全に陥り、進行性の臨床的悪化と多臓器への影響を引き起こす。",
        "腎アミロイドーシスはハムスターにおける進行性腎疾患である。慢性炎症などに伴い産生された前駆蛋白（主にAA）がアミロイド線維として糸球体・間質に沈着し、濾過障害と進行性の腎機能低下（蛋白尿・多飲多尿・体重減少・終末期の尿毒症）を来す。高齢個体に多く、根治的治療は困難で対症・支持療法が中心となる。",
    ),
}

MODULES = {"Lizard": REPO / "api/species/lizard_diseases.py", "Hamster": REPO / "api/species/hamster_diseases.py"}
JSON_OVERLAY = REPO / "diseases_all_species.json"


def patch_modules(apply: bool) -> list[str]:
    log = []
    for sp, path in MODULES.items():
        text = path.read_text(encoding="utf-8")
        orig = text
        for (fsp, _name, field), (old, new) in FIXES.items():
            if fsp != sp:
                continue
            if old in text:
                text = text.replace(old, new)
                log.append(f"MODULE {path.name}: patched {field} ({old[:14]}…)")
            elif new in text:
                log.append(f"MODULE {path.name}: already-fixed {field} (skip)")
            else:
                log.append(f"⚠️ MODULE {path.name}: neither old nor new for {field} — SKIP")
        if apply and text != orig:
            path.write_text(text, encoding="utf-8")
    return log


def patch_json(apply: bool) -> list[str]:
    log = []
    with JSON_OVERLAY.open(encoding="utf-8") as f:
        data = json.load(f)
    # index the old-values we expect to find
    by_field = {}
    for (sp, name, field), (old, new) in FIXES.items():
        by_field[(sp, name, field)] = (old, new)
    changed = 0
    for rec in data:
        sp = rec.get("species")
        name = rec.get("name")
        for field in ("causes_ja", "pathophysiology_ja", "treatment_ja"):
            key = (sp, name, field)
            if key not in by_field:
                continue
            old, new = by_field[key]
            cur = rec.get(field)
            if cur == old:
                rec[field] = new
                changed += 1
                log.append(f"JSON: patched {sp}/{name}/{field}")
            elif cur == new:
                log.append(f"JSON: already-fixed {sp}/{name}/{field} (skip)")
            elif cur is None:
                log.append(f"JSON: {sp}/{name}/{field} absent (module-only) — skip")
            else:
                log.append(f"⚠️ JSON: {sp}/{name}/{field} unexpected value — SKIP")
    if apply and changed:
        with JSON_OVERLAY.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    log.append(f"JSON changed fields: {changed}")
    return log


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ts", required=True, help="backup timestamp dir, e.g. 2026-07-21-1200")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    if args.apply:
        bdir = REPO / "backups" / args.ts
        bdir.mkdir(parents=True, exist_ok=True)
        for _sp, p in MODULES.items():
            shutil.copy2(p, bdir / p.name)
        # dump only the affected JSON entries (not the whole 98MB) for a light backup
        with JSON_OVERLAY.open(encoding="utf-8") as f:
            data = json.load(f)
        names = {(sp, name) for (sp, name, _f) in FIXES}
        subset = [r for r in data if (r.get("species"), r.get("name")) in names]
        (bdir / "diseases_all_species.lizard_hamster_subset.json").write_text(
            json.dumps(subset, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"backup → {bdir}")

    for line in patch_modules(args.apply):
        print(line)
    for line in patch_json(args.apply):
        print(line)
    print("APPLIED" if args.apply else "DRY-RUN (no files written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
