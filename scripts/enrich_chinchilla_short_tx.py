#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# --- Batch 1: 毛抜け, 鼓脹症, 便秘(巨大結腸), Ca欠乏, 砂浴び皮膚炎 ---

ENRICHMENTS["chinchilla_0002"] = {
    "treatment_ja": (
        "毛抜け（fur slip）。ストレス/不適切な保定時に大面積の毛が一度に脱落する防御反応。"
        "治療: 基本的に不要（自然に再生 — 数週〜数ヶ月）。"
        "  皮膚損傷がある場合: 希釈クロルヘキシジン（0.05%）で洗浄。"
        "  二次感染予防: エンロフロキサシン5-10 mg/kg PO q12h（感染徴候時のみ）。"
        "  ★フィプロニルはチンチラに致死的 — 絶対禁忌★"
        "予防（最重要）: "
        "  適切な保定法: 尾基部を持ち、体を支える。強く掴まない。"
        "  ストレス最小化: 静かな環境。急な動き/大きな音の回避。"
        "  子供への教育: チンチラの保定方法の指導。"
        "砂浴び: 通常通り継続可能（傷口がない場合）。"
        "鑑別: 皮膚糸状菌症（T. mentagrophytes）、barberring（同居個体による咬毛）、"
        "  栄養性脱毛、ストレス性脱毛。"
        "予後: 優秀。完全な毛の再生（通常6-8週間）。"
    ),
}

ENRICHMENTS["chinchilla_0006"] = {
    "treatment_ja": (
        "鼓脹症（胃鼓脹）。ガス産生食物/急激な食事変更/消化管運動低下が原因。"
        "緊急治療: "
        "  シメチコン: 経口投与（ガス破泡剤 — 即効性）。"
        "  疼痛管理: メロキシカム0.5 mg/kg PO/SC q24h。"
        "  消化管運動促進: メトクロプラミド0.5 mg/kg PO/SC q8h。"
        "  シサプリド0.5 mg/kg PO q8-12h。"
        "  輸液: 皮下輸液（乳酸リンゲル）10-15 mL/kg q12-24h。"
        "  保温: 低体温防止（ただしチンチラは暑さに弱い — 22°C以下を維持）。"
        "  胃管による減圧（重度 — 全身麻酔下）。"
        "食事管理: 絶食（急性期）→ チモシーヘイのみ → 段階的にペレット再開。"
        "  ガス産生食物の除外: キャベツ、ブロッコリー、豆類、果物。"
        "★抗菌薬禁忌★: ペニシリン系/セファロスポリン系経口 → 致死的腸内細菌叢破壊。"
        "予後: 早期治療で良好。胃破裂は致死的。"
    ),
}

ENRICHMENTS["chinchilla_0007"] = {
    "treatment_ja": (
        "便秘/巨大結腸症。食物繊維不足、脱水、ストレス、消化管運動低下が原因。"
        "治療: "
        "  消化管運動促進: メトクロプラミド0.5 mg/kg PO/SC q8h。"
        "  シサプリド0.5 mg/kg PO q8-12h（結腸運動促進）。"
        "  輸液: 皮下輸液10-15 mL/kg q12-24h（脱水補正）。"
        "  疼痛管理: メロキシカム0.5 mg/kg PO/SC q24h。"
        "  強制給餌: Critical Care/ペレット溶解液のシリンジ給餌。"
        "  腹部マッサージ: 穏やかに（蠕動促進）。"
        "  浣腸: 温生理食塩水5-10 mL（直腸内の乾燥糞塊 — 穿孔注意）。"
        "食事改善: チモシーヘイを無制限（繊維が最重要）。"
        "  新鮮な水の確保。ペレットは制限量。おやつ最小限。"
        "巨大結腸症（megacolon — 先天性/慢性）: "
        "  生涯にわたる食事管理+運動促進薬。手術適応は稀。"
        "★抗菌薬禁忌★: ペニシリン系/セファロスポリン系経口は致死的。"
        "予後: 軽度は食事改善で回復。巨大結腸症は慢性管理必要。"
    ),
}

ENRICHMENTS["chinchilla_0018"] = {
    "treatment_ja": (
        "カルシウム欠乏症/栄養性二次性上皮小体機能亢進症。"
        "急性（低Ca痙攣/振戦時）: "
        "  グルコン酸カルシウム10%: 50-100 mg/kg IM/SC。"
        "  経口カルシウム補助: カルシウムシロップ/粉末を食事に添加。"
        "ビタミンD3: 経口サプリメント。"
        "食事改善（根本治療）: "
        "  Ca:P比 2:1を目標。チモシーヘイを基本食に。"
        "  カルシウム豊富食: ケール、チンゲン菜（少量）。"
        "  リン過剰の回避: 種子類/穀物の過給与制限。"
        "  良質なペレット食（チンチラ専用 — Ca/P比調整済み）。"
        "病的骨折管理: "
        "  ケージ内安静（多段ケージの段を減らす — 落下防止）。"
        "  スプリント（可能であれば）。鎮痛: メロキシカム0.5 mg/kg PO q24h。"
        "鑑別: 骨粗鬆症（高齢）、代謝性骨疾患、外傷性骨折。"
        "予後: 食事改善で回復可能。重度の骨変形は不可逆的。"
    ),
}

ENRICHMENTS["chinchilla_0013"] = {
    "treatment_ja": (
        "砂浴び関連の皮膚炎。汚染された砂浴び材、過度の砂浴び、不適切な材料が原因。"
        "治療: "
        "  砂浴び材の変更: 清潔な火山灰系パウダーに変更（Blue Cloud等）。"
        "  砂浴び頻度の調整: 週2-3回、15-30分/回に制限。"
        "  汚染砂の交換: 毎回 or 少なくとも週1回。"
        "  — 砂浴び材に糞便/尿が混入 → 細菌/真菌汚染。"
        "局所治療: "
        "  軽度: 自然回復を待つ（砂浴び材変更のみで改善）。"
        "  中等度: 希釈クロルヘキシジン（0.05%）での患部洗浄。"
        "  二次感染: エンロフロキサシン5-10 mg/kg PO q12h × 7-10日。"
        "  ★フィプロニルはチンチラに致死的 — 絶対禁忌★"
        "  ★ペニシリン系/セファロスポリン系経口は致死的禁忌★"
        "皮膚糸状菌症の鑑別: 砂浴び皮膚炎に見える症例でT. mentagrophytes感染あり。"
        "  DTM培養で確認。人獣共通。"
        "予後: 砂浴び材の改善で速やかに回復。"
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} chinchilla disease entries")


if __name__ == "__main__":
    apply_enrichments()
