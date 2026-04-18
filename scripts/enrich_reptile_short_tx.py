#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# Reptile (17件)
# ============================================================

# --- Reptile Batch 1: Ca欠乏, 卵詰まり, 慢性卵貯留, 膿瘍, 眼鏡鱗下膿瘍 ---

ENRICHMENTS["reptile_0113"] = {
    "treatment_ja": (
        "カルシウム欠乏症/栄養性二次性上皮小体機能亢進症（NSHP/MBD）。"
        "急性（低Ca痙攣/振戦時）: "
        "  グルコン酸カルシウム10%: 50-100 mg/kg IM/ICe（骨髄内）。"
        "  — 心拍モニタリング（徐脈に注意）。"
        "維持: カルシウム補充（炭酸Ca粉末を食事に添加）。"
        "UVB照射（最重要 — ビタミンD3合成に必須）: "
        "  UVB 10-12%ランプ。照射距離30-45cm。1日10-12時間。"
        "  6ヶ月毎にランプ交換（UVB出力低下）。"
        "ビタミンD3: 経口補充（UVB不足時）。過剰投与は高Ca血症のリスク。"
        "食事改善: Ca:P比2:1。昆虫食にはCaパウダーをダスティング。"
        "  草食種: カルシウム豊富な葉野菜（コマツナ、チンゲン菜）。"
        "  シュウ酸含有食物（ホウレンソウ）はCa吸収を阻害 → 制限。"
        "POTZ（適正体温帯）の維持: Ca代謝に温度管理が不可欠。"
        "予後: 早期なら回復可能。重度の骨変形/病的骨折は不可逆的。"
    ),
}

ENRICHMENTS["reptile_0057"] = {
    "treatment_ja": (
        "卵詰まり（難産/dystocia）。不適切な産卵環境、Ca欠乏、卵殻異常が原因。"
        "内科的介入: "
        "  環境調整: 温度上昇（POTZ上限）+ 湿度増加。適切な産卵場所の提供。"
        "  グルコン酸カルシウム10%: 50-100 mg/kg IM。"
        "  → オキシトシン1-10 IU/kg IM（Ca投与15-20分後）。"
        "  — 爬虫類はオキシトシン感受性が種により異なる → 低用量から開始。"
        "  潤滑剤: 総排泄腔内に水溶性潤滑剤。"
        "  輸液: 皮下/骨髄内/ICe輸液（脱水補正）。"
        "外科的介入: "
        "  卵穿刺（ovocentesis）: 針で卵殻を穿刺 → 内容物吸引 → 卵殻崩壊・排出。"
        "  開腹卵管切開（salpingotomy）: 卵管を切開して卵を摘出。"
        "  卵管摘出術（salpingohysterectomy）: 慢性再発性の場合。"
        "  — 爬虫類の麻酔: イソフルラン/セボフルラン吸入。POTZ維持が重要。"
        "予後: 早期介入で良好。卵管破裂/卵黄性体腔炎は予後不良。"
    ),
}

ENRICHMENTS["reptile_egg_retention_chronic"] = {
    "treatment_ja": (
        "慢性卵貯留。排卵後に卵管内に長期間卵が停滞。"
        "治療: "
        "  環境改善: 適切な産卵場所（湿潤な基質、適温）の提供。"
        "  カルシウム補充: グルコン酸Ca 50-100 mg/kg IM。"
        "  オキシトシン試験: 1-10 IU/kg IM（反応を評価）。"
        "  — 慢性例ではオキシトシン反応が低下していることが多い。"
        "  GnRHアゴニスト: ロイプロリド（100-400 μg/kg IM）— 排卵抑制。"
        "  デスロレリンインプラント（将来の排卵抑制に）。"
        "外科: "
        "  卵管切開 or 卵管摘出 → 根治的。"
        "  慢性例は卵の石灰化/癒着 → 卵管壁の損傷リスク。"
        "  麻酔: イソフルラン。POTZ維持。"
        "合併症: 卵黄性体腔炎、敗血症、卵管破裂。"
        "予後: 手術で回復可能。卵黄性体腔炎合併は予後不良。"
    ),
}

ENRICHMENTS["reptile_0047"] = {
    "treatment_ja": (
        "膿瘍。爬虫類の膿は固形（caseous — チーズ様）で液状化しない。"
        "外科的処置（第一選択）: "
        "  完全切除（en bloc excision）が最も推奨。"
        "  — 爬虫類の膿は固形 → ドレーンは無効。I&Dだけでは不十分。"
        "  膿瘍嚢壁ごとの完全摘出が理想。"
        "  洗浄: 温生理食塩水/希釈クロルヘキシジン（0.05%）。"
        "抗菌薬: "
        "  セフタジジム20 mg/kg IM q72h（第一選択 — グラム陰性菌カバー）。"
        "  エンロフロキサシン5-10 mg/kg IM/PO q24-48h。"
        "  — 爬虫類はグラム陰性菌感染が多い（Pseudomonas、Aeromonas）。"
        "  培養+感受性試験推奨。"
        "疼痛管理: メロキシカム0.2-0.5 mg/kg PO/IM q24-48h。"
        "飼育環境: POTZ維持（免疫機能に直結）。適切な湿度。清潔な環境。"
        "予後: 完全切除で良好。飼育環境改善が再発予防に最重要。"
    ),
}

ENRICHMENTS["reptile_0084"] = {
    "treatment_ja": (
        "眼鏡鱗下膿瘍（subspectacular abscess）。ヘビ/一部トカゲ（ヤモリ）に発生。"
        "  眼瞼がなく眼鏡鱗（spectacle）で覆われた種で発生。"
        "治療: "
        "  外科的ドレナージ: 眼鏡鱗を切開 → 固形膿の除去 → 洗浄。"
        "  — 眼鏡鱗の腹側に切開（次回脱皮で再生）。"
        "  洗浄: 温生理食塩水。ポビドンヨード希釈液。"
        "  局所抗菌薬: 点眼（オフロキサシン/ゲンタマイシン）q12h。"
        "全身抗菌薬: "
        "  セフタジジム20 mg/kg IM q72h。"
        "  エンロフロキサシン5-10 mg/kg IM q24-48h。"
        "  培養+感受性試験（Pseudomonas等のグラム陰性菌が多い）。"
        "飼育環境: POTZ維持。適切な湿度（脱皮不全 → 眼鏡鱗下に菌侵入の原因）。"
        "  脱皮不全の予防: 湿度管理、水浴び場の提供。"
        "鑑別: 眼鏡鱗下液貯留（retained spectacle fluid）、眼腫瘍。"
        "予後: 早期治療で良好。慢性例は眼球摘出が必要な場合あり。"
    ),
}


def apply_enrichments() -> None:
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for entry in data:
        eid = entry.get("id")
        if eid in ENRICHMENTS:
            patch = ENRICHMENTS[eid]
            for k, v in patch.items():
                entry[k] = v
            updated += 1

    missing = set(ENRICHMENTS) - {e.get("id") for e in data}
    if missing:
        print(f"WARNING: {len(missing)} IDs in ENRICHMENTS not found in JSON:")
        for m in sorted(missing):
            print(f"  {m}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated}/{len(ENRICHMENTS)} reptile-group entries")


if __name__ == "__main__":
    apply_enrichments()
