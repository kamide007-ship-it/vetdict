"""Replace the elodont-herbivore dental template in non-herbivore species.

2026-11 第83弾: the dental fallback block

    {name}の治療には全身麻酔下での歯科処置が必須…
    高速ダイヤモンドバーで臼歯研磨、過長切歯トリミング、{species}の上下咬合バランス回復。
    膿瘍合併時は外科的排膿＋ドキシサイクリン 5-10 mg/kg PO q12h × 4-6週…
    鎮痛: メロキシカム 0.5-1 mg/kg PO q12-24h、強オピオイド使用時はモニタ強化。
    予防のため繊維質食材（チモシー、葉物野菜）を主食、咀嚼促進のためペレットを最小化。

describes rabbit/rodent dentistry, yet it was served for dog oral papillomas,
feline oral eosinophilic granuloma, equine floating, bird beaks, reptiles,
ferrets and hedgehogs — with a rodent meloxicam dose that is a 5-10x overdose
for dogs and up to 20x for cats. Elodont herbivores keep the block; other
species receive ``dental_lines_ja`` (species-appropriate). Three dog/cat
entries whose treatment is not dentistry at all get a fully curated text.

Usage:
    python3 -m scripts.template_elimination.fix_dental_template_cross_species [--apply]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.fallback_generator import (  # noqa: E402
    _ELODONT_HERBIVORES,
    dental_lines_ja,
)
from scripts.template_elimination.fix_species_dose_templates import (  # noqa: E402
    JSON_SPECIES,
    MODULE_SPECIES,
)
from scripts.template_elimination.template_content_library import (  # noqa: E402
    NON_HERBIVORE_SMALL_MAMMAL_SUPPORTIVE,
    OLD_SMALL_MAMMAL_SUPPORTIVE,
)

_BLOCK = re.compile(
    r"(?P<name>[^\n【】]+?)の治療には全身麻酔下での歯科処置が必須（無麻酔処置は不十分かつ安全性に欠ける）。"
    r"(?P<sep>\n|\\n)"
    r"高速ダイヤモンドバーで臼歯研磨、過長切歯トリミング、[^\n\\]+?の上下咬合バランス回復。(?P=sep)"
    r"膿瘍合併時は外科的排膿＋ドキシサイクリン 5-10 mg/kg PO q12h × 4-6週（嫌気性菌カバー）。(?P=sep)"
    r"鎮痛: メロキシカム 0.5-1 mg/kg PO q12-24h、強オピオイド使用時はモニタ強化。(?P=sep)"
    r"予防のため繊維質食材（チモシー、葉物野菜）を主食、咀嚼促進のためペレットを最小化。"
)

# Entries whose correct treatment is not dentistry — replace the whole text.
CURATED: dict[tuple[str, str], str] = {
    ("dog", "口腔乳頭腫症"): (
        "【犬の口腔乳頭腫症（犬口腔パピローマウイルス）】\n"
        "多くは若齢犬で、細胞性免疫の成立とともに1〜3ヶ月（最長5ヶ月程度）で自然退縮するため、"
        "摂食・呼吸に支障がなければ経過観察が基本。\n"
        "持続例・多発で咀嚼障害や出血がある場合は外科的切除・凍結手術・レーザー蒸散を行い、切除組織は病理検査に提出する"
        "（長期持続・高齢発症例では扁平上皮癌への移行を鑑別）。\n"
        "アジスロマイシン 10 mg/kg PO q24h × 10日で退縮が早まったとする小規模試験がある（Yağci 2008 Vet Dermatol）"
        "— エビデンスは限定的。\n"
        "グルココルチコイド等の免疫抑制薬は退縮を遅らせるため避ける。接触感染するため、退縮まで他の犬との直接接触・"
        "食器の共有を控える。\n"
        "疼痛時の鎮痛: メロキシカム 0.2 mg/kg PO 初回→0.1 mg/kg PO q24h（Muller & Kirk's Small Animal Dermatology 7th ed）。"
    ),
    ("cat", "猫口腔好酸球性肉芽腫"): (
        "【猫の口腔好酸球性肉芽腫（好酸球性肉芽腫群）】\n"
        "診断は生検（病理組織検査）で腫瘍（扁平上皮癌・リンパ腫）を除外してから治療を開始する。\n"
        "第一選択はプレドニゾロン 1-2 mg/kg PO q12-24h を2〜4週続け、病変の改善に合わせ4〜8週かけて最小有効量へ漸減。"
        "経口投与が難しい場合は酢酸メチルプレドニゾロン 20 mg/頭 SC（反復は2〜3週間隔・糖尿病誘発に注意）。\n"
        "基礎のアレルギーを特定する: 同居動物を含む厳格なノミ駆除、8週間の除去食試験、環境アレルゲンの評価。\n"
        "二次細菌感染が疑われる場合はアモキシシリン・クラブラン酸 12.5-20 mg/kg PO q12h × 3週間"
        "（細菌感染の関与で改善する例がある）。\n"
        "ステロイド抵抗性・再発例はシクロスポリン 7 mg/kg PO q24h（開始前にFeLV/FIV検査・完全室内飼育）。\n"
        "（Muller & Kirk's Small Animal Dermatology 7th ed; Buckley & Nuttall, Vet Clin North Am 2012）"
    ),
    ("cat", "口腔腫瘤・エプリス"): (
        "【猫の口腔腫瘤・エプリス】\n"
        "猫の口腔腫瘤は扁平上皮癌が最多で悪性の割合が高いため、外観で良性と判断せず、全身麻酔下で切開生検（病理組織検査）と"
        "頭部X線/CTで骨浸潤を評価する（所属リンパ節の細胞診・胸部画像で病期分類）。\n"
        "良性の歯原性腫瘍（末梢性歯原性線維腫・若齢猫の猫誘導性歯原性腫瘍）は、原因歯を含めたマージン付き切除で根治が期待できる。\n"
        "悪性腫瘍は顎骨部分切除を含む広範囲切除が第一選択で、不完全切除・切除不能例は放射線治療を検討する。\n"
        "術後の栄養管理（食道瘻チューブ等）を計画する。\n"
        "鎮痛: メロキシカム 0.05 mg/kg PO 初回→0.01-0.03 mg/kg PO q24h（最小有効量・腎機能監視 — ISFM/AAFP 2010）、"
        "術後はブプレノルフィン 0.02-0.03 mg/kg 口腔粘膜投与 q6-8h。\n"
        "（Withrow & MacEwen's Small Animal Clinical Oncology 6th ed; Verstraete, Oral and Maxillofacial Surgery 2nd ed）"
    ),
}


def fix_supportive(text: str, species: str) -> str:
    """Herbivore supportive block → carnivore/insectivore/omnivore version."""
    new = NON_HERBIVORE_SMALL_MAMMAL_SUPPORTIVE.get(species)
    return text.replace(OLD_SMALL_MAMMAL_SUPPORTIVE, new) if new else text


# 他の多種共通テンプレート（足底皮膚炎・前庭疾患等）に残る齧歯類用量の言い換え
_RODENT_MELOX = re.compile(r"メロキシカム\s*0\.5[-–]1(?:\.0)?\s*mg/kg(?:\s*PO)?(?:\s*q12-24h)?")
_SPECIES_MELOX = {
    "ferret": "メロキシカム 0.2 mg/kg PO/SC q24h",
    "hedgehog": "メロキシカム 0.1-0.2 mg/kg PO/SC q24h",
    "sugar_glider": "メロキシカム 0.1-0.2 mg/kg PO/SC q24h",
}


def fix_text(text: str, species: str) -> str:
    text = fix_supportive(text, species)
    if species in _SPECIES_MELOX:
        text = _RODENT_MELOX.sub(_SPECIES_MELOX[species], text)
    if species in _ELODONT_HERBIVORES or "強オピオイド使用時はモニタ強化" not in text:
        return text

    def _sub(m: re.Match) -> str:
        return m.group("sep").join(dental_lines_ja(species, m.group("name").strip()))

    return _BLOCK.sub(_sub, text)


def main(apply: bool) -> None:
    path = ROOT / "diseases_all_species.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n_json = 0
    for x in data:
        sp = JSON_SPECIES.get(x.get("species", ""))
        if not sp:
            continue
        cur = x.get("treatment_ja") or ""
        curated = CURATED.get((sp, x.get("name_ja", "")))
        new = curated if curated else fix_text(cur, sp)
        if new != cur:
            x["treatment_ja"] = new
            n_json += 1
    print(f"JSON treatment_ja fixed: {n_json}")

    n_mod = 0
    for f in sorted((ROOT / "api" / "species").glob("*_diseases.py")):
        stem = f.stem[: -len("_diseases")]
        sp = MODULE_SPECIES.get(stem, stem)
        src = f.read_text(encoding="utf-8")
        new = fix_text(src, sp)
        if new != src:
            n_mod += 1
            if apply:
                f.write_text(new, encoding="utf-8")
    print(f"species modules changed: {n_mod}")

    supp = ROOT / "api" / "data" / "supplementary_diseases.json"
    n_supp = 0
    if supp.exists():
        sdata = json.loads(supp.read_text(encoding="utf-8"))
        rows = (
            sdata
            if isinstance(sdata, list)
            else [r for v in sdata.values() for r in (v if isinstance(v, list) else [])]
        )
        for x in rows:
            if not isinstance(x, dict):
                continue
            raw_sp = str(x.get("species", ""))
            sp = JSON_SPECIES.get(raw_sp, raw_sp.lower().replace(" ", "_"))
            for fld in ("treatment_ja",):
                cur = x.get(fld) or ""
                new = fix_text(cur, sp)
                if new != cur:
                    x[fld] = new
                    n_supp += 1
        print(f"supplementary treatment_ja fixed: {n_supp}")
        if apply and n_supp:
            with open(supp, "w", encoding="utf-8") as fh:
                json.dump(sdata, fh, ensure_ascii=False, indent=None, separators=(",", ":"))

    if apply:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main("--apply" in sys.argv)
