#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# --- Batch 1: GIイレウス/便秘/術後イレウス ---

ENRICHMENTS["rabbit_0071"] = {
    "treatment_ja": (
        "イレウス（ウサギ）。★GI stasis — ウサギで最も緊急性の高い疾患の一つ★。"
        "疼痛管理: メロキシカム 0.3-0.5 mg/kg PO/SC q12h。"
        "  ブプレノルフィン 0.03-0.05 mg/kg SC q6-8h（重症時）。"
        "消化管運動促進: メトクロプラミド 0.5 mg/kg PO/SC q6-8h。"
        "  シサプリド 0.5 mg/kg PO q8-12h。"
        "輸液: 乳酸リンゲル 60-100 mL/kg/day SC/IV。脱水補正。"
        "強制給餌: Critical Care 10-15 mL/kg q4-6h（腸閉塞を除外後）。"
        "  ★チモシーヘイの常時提供が腸運動の最大の刺激★。"
        "腸閉塞との鑑別: X線（ガス像の局在）+造影。"
        "  ★真の閉塞はメトクロプラミド禁忌 — 術前に除外必須★。"
        "★ペニシリン系/セファロスポリン系経口は致死的禁忌★。"
        "抗菌薬（二次感染時）: エンロフロキサシン 5-10 mg/kg PO q12h。"
        "予後: 早期治療（24h以内）で良好。48h超/閉塞合併は予後不良。"
    ),
}

ENRICHMENTS["rabbit_0078"] = {
    "treatment_ja": (
        "便秘（ウサギ）。★ウサギの便秘はGI stasis/腸閉塞との鑑別が必須★。"
        "まず腸閉塞を除外: X線（ガス像・盲腸拡張・小腸閉塞像）。"
        "食事管理: チモシーヘイを主食に（繊維>25%が腸運動維持に不可欠）。"
        "  ★ペレット過多/野菜不足/毛繕い過多が主因★。"
        "水分補給: 新鮮な水を常時提供。脱水改善に皮下輸液 20-30 mL/kg/day。"
        "消化管運動促進: メトクロプラミド 0.5 mg/kg PO/SC q6-8h。"
        "  シサプリド 0.5 mg/kg PO q8-12h。"
        "疼痛管理: メロキシカム 0.3-0.5 mg/kg PO q12h（腹痛時）。"
        "強制給餌: Critical Care（食欲廃絶時）。"
        "毛球管理: ラキサトーン（毛球除去ペースト）。"
        "  ★ウサギに催吐剤は禁忌（嘔吐できない）★。"
        "★ペニシリン系/セファロスポリン系経口は致死的禁忌★。"
        "予後: 早期治療で良好。完全閉塞/GI stasis重症例は予後慎重。"
    ),
}

ENRICHMENTS["rabbit_0219"] = {
    "treatment_ja": (
        "術後イレウス（ウサギ）。★術後GI stasis — 麻酔後の腸運動停止がウサギで最大の周術期リスク★。"
        "予防（術前・術中）: "
        "  絶食は4時間まで（長時間絶食はGI stasis誘発）。"
        "  術中保温（低体温→腸運動停止）。術中輸液。鎮痛の徹底。"
        "術後早期治療: "
        "  疼痛管理: メロキシカム 0.3-0.5 mg/kg PO/SC q12h。"
        "    ブプレノルフィン 0.03-0.05 mg/kg SC q6-8h。"
        "  消化管運動促進: メトクロプラミド 0.5 mg/kg PO/SC q6-8h。"
        "    シサプリド 0.5 mg/kg PO q8-12h。"
        "  輸液: 60-100 mL/kg/day SC/IV。"
        "  強制給餌: Critical Care 10-15 mL/kg q4-6h（腸蠕動確認後）。"
        "  チモシーヘイをケージに配置（嗅覚刺激→食欲回復促進）。"
        "  早期起立・運動促進。"
        "★ペニシリン系/セファロスポリン系経口は致死的禁忌★。"
        "予後: 術後12-24h以内の治療開始で良好。48h超は予後不良。"
    ),
}


def apply_enrichments() -> None:
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)
    updated = 0
    for entry in data:
        eid = entry.get("id")
        if eid in ENRICHMENTS:
            for k, v in ENRICHMENTS[eid].items():
                entry[k] = v
            updated += 1
    missing = set(ENRICHMENTS) - {e.get("id") for e in data}
    if missing:
        print(f"WARNING: {len(missing)} IDs not found: {sorted(missing)}")
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated {updated}/{len(ENRICHMENTS)} rabbit entries")


if __name__ == "__main__":
    apply_enrichments()
