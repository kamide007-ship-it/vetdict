"""diseases_all_species.json 内に残存する英語フィールドを日本語化する。

対象:
1. differential_diagnosis: 56件の英語表記
2. recommended_tests: 4件の英語表記 (MRI/CT, CBC)
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "diseases_all_species.json"

GENERIC_DD_EN = "Rule out other conditions with similar clinical presentation through diagnostic testing."
GENERIC_DD_JA = "類似した臨床像を呈する他疾患を診断検査により除外する。"

# 個別翻訳マップ
SPECIFIC_DD_TRANSLATIONS: dict[str, str] = {
    # Horse 行動学
    "horse_0026": "胃潰瘍、歯科疼痛、消化器系の不快感など、行動の引き金となる原発疾患を除外する。",
    "horse_0027": "神経疾患（馬原虫性脊髄脳炎(EPM)、頚椎脊髄症(wobblers)）、前庭疾患、疼痛性の重心移動を鑑別する。",
    "horse_0028": "疝痛、神経疾患、疼痛、前庭機能障害を鑑別する。",
    "horse_0029": "さく癖（首を反らせて空気嚥下を伴う点で異なる）、異食症、栄養欠乏を鑑別する。",
    "horse_0030": "栄養欠乏、異食症、退屈に関連する行動、消化器疾患を鑑別する。",
    "horse_0031": "疼痛による回避、運動器損傷、視覚障害、神経疾患を鑑別する。",
    "horse_0032": "疼痛性攻撃行動、狂犬病、神経疾患、ホルモン異常を鑑別する。",
    # Dog 行動学
    "dog_leash_reactivity": "疼痛性攻撃行動、甲状腺機能異常、神経疾患、真の攻撃行動と反応性の鑑別。",
    "dog_interdog_aggression": "疼痛性攻撃行動、甲状腺機能異常、神経疾患、てんかん関連攻撃行動を鑑別する。",
    "dog_coprophagy": "膵外分泌不全(EPI)、吸収不良症候群、寄生虫症、栄養欠乏、異食症を鑑別する。",
    "dog_tail_chasing": "部分発作、肛門嚢疾患、肛門周囲瘻、馬尾症候群、皮膚炎、前庭疾患を鑑別する。",
    "dog_excessive_barking": "分離不安、認知機能不全症候群(CDS)、疼痛、聴力低下、強迫性障害、縄張り行動を鑑別する。",
    # Cat 行動学
    "cat_intercat_aggression": "再指向性攻撃、疼痛性攻撃行動、遊戯性攻撃、地位関連攻撃を鑑別する。",
    "cat_0026": "ノミアレルギー性皮膚炎、食物アレルギー、アトピー性皮膚炎、皮膚糸状菌症、Demodex gatoi、好酸球性肉芽腫症候群、甲状腺機能亢進症を鑑別する。",
    # Bird
    "bird_hormonal_behavior": "卵詰まり（緊急）、卵管炎、卵黄性腹膜炎、卵巣嚢胞、卵巣腫瘍を鑑別する。",
}

# recommended_tests の英語項目 → 日本語表記
TEST_TRANSLATIONS: dict[str, str] = {
    "MRI/CT": "MRI/CT検査",
    "CBC": "全血球計算 (CBC)",
}


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup = JSON_PATH.with_suffix(f".json.backup_{timestamp}_pre_translate")
    if not backup.exists():
        shutil.copy2(JSON_PATH, backup)
        print(f"backup written: {backup.name}")

    stats = {
        "dd_generic_translated": 0,
        "dd_specific_translated": 0,
        "tests_translated": 0,
    }

    for entry in data:
        # differential_diagnosis
        dd = entry.get("differential_diagnosis") or ""
        if dd == GENERIC_DD_EN:
            entry["differential_diagnosis"] = GENERIC_DD_JA
            stats["dd_generic_translated"] += 1
        elif entry.get("id") in SPECIFIC_DD_TRANSLATIONS:
            entry["differential_diagnosis"] = SPECIFIC_DD_TRANSLATIONS[entry["id"]]
            stats["dd_specific_translated"] += 1

        # recommended_tests
        rt = entry.get("recommended_tests")
        if isinstance(rt, list):
            translated = []
            changed = False
            for item in rt:
                if item in TEST_TRANSLATIONS:
                    translated.append(TEST_TRANSLATIONS[item])
                    changed = True
                else:
                    translated.append(item)
            if changed:
                entry["recommended_tests"] = translated
                stats["tests_translated"] += 1

    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== translation stats ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
