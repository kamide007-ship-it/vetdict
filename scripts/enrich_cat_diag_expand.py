#!/usr/bin/env python3
"""Cat diagnosis_ja expansion — 4 entries under 150 chars."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["cat_arrhythmia_-_atrial_fibrillation"] = {
    "diagnosis_ja": "心電図で不整なRR間隔、f波（P波消失）、正常QRS幅を確認。猫ではAFは稀であり、存在すれば基礎心疾患が重篤であることを示唆。ホルター心電図で持続性/発作性を判定。心エコーで著明なLA拡大を確認（基礎にHCM/DCM/RCMがある場合が多い）。左房径>20 mmで発症リスク上昇。心室レートコントロール（目標<200bpm）。甲状腺機能亢進症の合併除外（T4測定必須）。血栓塞栓リスクの評価。"
}

ENRICHMENTS["cat_congenital_heart_defect_-_ventricular_septal_defect"] = {
    "diagnosis_ja": "聴診で右胸骨縁の全収縮期雑音（Levine分類でグレード評価）。心エコー（2D+カラードプラ）で欠損孔の位置・サイズ・シャント方向を評価。Qp/Qs比でシャント量定量（>1.5で血行動態的に有意）。胸部X線: 大欠損で肺過灌流+左心拡大。猫では小欠損が多く無症状で偶発的に発見されることが多い。心電図でLV肥大パターン。大欠損ではEisenmenger症候群のリスクを経時的に評価。"
}

ENRICHMENTS["cat_pemphigus_foliaceus"] = {
    "diagnosis_ja": "皮膚生検で表皮内の棘融解と好中球/好酸球の角層下膿疱を確認（生検は新鮮な膿疱から採取が重要）。直接免疫蛍光法（DIF）で角化細胞間のIgG沈着を確認。臨床症状: 耳介・鼻梁・爪床の痂皮・膿疱・びらんが好発部位。CBC/生化学は概ね正常だが好中球増多を認めることあり。細菌培養で二次感染を評価。SLE・薬剤性天疱瘡を鑑別。猫では自己免疫性皮膚疾患の中で最多。"
}

ENRICHMENTS["cat_rectal_prolapse"] = {
    "diagnosis_ja": "肛門からの直腸粘膜/全層の脱出を肉眼確認。脱出組織の色調（ピンク=新鮮、暗紫色=鬱血、黒色=壊死）・浮腫・壊死を評価。プローブ挿入テスト: 脱出部と直腸壁間にプローブ挿入可=全層脱出（不可=粘膜脱出）。基礎疾患の検索: 寄生虫（糞便検査）、大腸炎（細胞診）、巨大結腸、膀胱/尿道疾患。慢性しぶり（tenesmus）の原因検索が必須。全身状態（脱水、電解質）評価。子猫で寄生虫関連が多い。"
}


def apply_enrichments() -> None:
    for attempt in range(3):
        try:
            with open(JSON_PATH, encoding="utf-8") as f:
                content = f.read()
            decoder = json.JSONDecoder()
            data, _ = decoder.raw_decode(content)
            break
        except (json.JSONDecodeError, ValueError):
            if attempt < 2:
                time.sleep(5)
            else:
                raise

    updated = 0
    for entry in data:
        eid = entry.get("id")
        if eid in ENRICHMENTS:
            for k, v in ENRICHMENTS[eid].items():
                entry[k] = v
            updated += 1

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated}/{len(ENRICHMENTS)} entries")


if __name__ == "__main__":
    apply_enrichments()
