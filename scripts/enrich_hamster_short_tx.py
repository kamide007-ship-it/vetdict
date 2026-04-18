#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# --- Batch 1: 頬袋脱出, 頬袋膿瘍, 皮膚糸状菌症, 白癬, カルシウム欠乏 ---

ENRICHMENTS["hamster_0005"] = {
    "treatment_ja": (
        "頬袋脱出。食物の詰め込みすぎ、粘着性食物、腫瘍が原因。"
        "整復手順: "
        "  1) 脱出したポーチを温生理食塩水で湿潤保持（乾燥させない）。"
        "  2) 50%ブドウ糖液を塗布 → 浮腫軽減（浸透圧による脱水効果）。"
        "  3) 浮腫軽減後、綿棒/鈍棒で用手的に整復。"
        "  4) 整復後に巾着縫合（一時的 — 再脱出防止、24-48hで抜糸）。"
        "外科的切除（壊死組織がある場合）: "
        "  壊死ポーチの切除（partial buccal pouch resection）。"
        "  血管結紮 → 壊死部切除 → 粘膜縫合。"
        "  — 片側ポーチ切除しても摂食に影響は最小限。"
        "術後管理: 柔らかい食事（ペレットを水でふやかす）2-3日間。"
        "  抗菌薬: エンロフロキサシン5-10 mg/kg PO q12h × 5-7日。"
        "  疼痛管理: メロキシカム0.5 mg/kg PO q24h × 3日。"
        "再発予防: 粘着性食物の除外（チョコレート、キャンディ等）。"
        "  適切なサイズの食物。ケージ内の尖った突起物の除去。"
        "鑑別: 頬袋腫瘍（SCC、リンパ腫）、頬袋膿瘍、口腔腫瘍。"
        "予後: 整復成功で良好。腫瘍関連は予後不良。"
    ),
}

ENRICHMENTS["hamster_0006"] = {
    "treatment_ja": (
        "頬袋内の膿瘍形成。頬袋粘膜の損傷（尖った食物/床材）による二次感染。"
        "外科的処置: "
        "  切開排膿（I&D）: 頬袋を外翻 → 膿瘍切開 → 洗浄。"
        "  洗浄: 温生理食塩水 or 希釈クロルヘキシジン（0.05%）。"
        "  壊死組織のデブリードメント。"
        "  重度/再発性: 頬袋部分切除。"
        "抗菌薬（★ペニシリン系/セファロスポリン系経口は絶対禁忌★）: "
        "  エンロフロキサシン5-10 mg/kg PO q12h × 10-14日。"
        "  TMP-SMX 15-30 mg/kg PO q12h × 10-14日。"
        "  ドキシサイクリン2.5-5 mg/kg PO q12h。"
        "  メトロニダゾール20 mg/kg PO q12h（嫌気性菌）。"
        "疼痛管理: メロキシカム0.5 mg/kg PO/SC q24h。"
        "  ブプレノルフィン0.05-0.1 mg/kg SC q8-12h（重度の疼痛）。"
        "★致死的禁忌★: ペニシリン系/セファロスポリン系の経口投与 → "
        "  Clostridium difficile腸炎 → 致死的下痢（抗菌薬関連腸炎）。"
        "  注射は許容（経口のみ禁忌）。"
        "予後: 適切なI&Dと抗菌薬で良好。"
    ),
}

ENRICHMENTS["hamster_0014"] = {
    "treatment_ja": (
        "Trichophyton mentagrophytesが最多。人獣共通感染症（zoonosis）。"
        "治療: "
        "  局所: ミコナゾールクリーム q12h × 4-6週間（病変部に薄く塗布）。"
        "  全身: テルビナフィン20 mg/kg PO q24h × 4-6週間（広範囲/難治性時）。"
        "  代替: グリセオフルビン25 mg/kg PO q24h × 4-6週（催奇形性 — 妊娠禁忌）。"
        "  薬浴: 硫黄石灰（lime sulfur dip）— 希釈して週1-2回。"
        "環境消毒（再感染防止に極めて重要）: "
        "  床材の全交換。ケージの次亜塩素酸ナトリウム（1:10希釈）消毒。"
        "  感染動物の隔離。接触した器具の消毒 or 廃棄。"
        "診断: ウッド灯（M. canisのみ蛍光 — T. mentagrophytesは蛍光しない）。"
        "  皮膚掻爬+KOH鏡検。DTM培養（確定診断 — 2-3週間）。PCR。"
        "臨床症状: 円形脱毛、鱗屑、痂皮。耳介・鼻・四肢に好発。"
        "飼い主への注意: 人への感染リスク（免疫低下者で特に注意）。手洗い徹底。"
        "予後: 治療で良好。環境消毒が不十分だと再感染。"
    ),
}

ENRICHMENTS["hamster_0132"] = {
    "treatment_ja": (
        "白癬（Trichophyton mentagrophytes感染）。皮膚糸状菌症と同一病態。"
        "治療: "
        "  局所: ミコナゾール/クロトリマゾールクリーム q12h × 4-6週間。"
        "  全身: テルビナフィン20 mg/kg PO q24h × 4-6週間。"
        "  イトラコナゾール5-10 mg/kg PO q24h × 4-6週（代替）。"
        "環境消毒: 床材全交換、ケージ消毒（次亜塩素酸ナトリウム1:10）。"
        "  感染動物の隔離。接触器具の廃棄 or 消毒。"
        "  胞子は環境中に18ヶ月以上残存 → 徹底消毒。"
        "臨床症状: 円形〜不整形の脱毛斑。鱗屑、痂皮。"
        "  耳介辺縁・鼻・四肢に好発。"
        "  免疫低下（ストレス、過密飼育、高齢）で増悪。"
        "診断: DTM/SAB培養（確定 — T. mentagrophytesコロニー形態確認）。"
        "  KOH鏡検: 毛幹内の分節胞子。PCR。"
        "人獣共通感染症: 飼い主/家族への感染リスク。"
        "  特に小児・免疫不全者。手洗い+手袋の使用。"
        "予後: 治療で良好。免疫低下動物では遷延化。"
    ),
}

ENRICHMENTS["hamster_0182"] = {
    "treatment_ja": (
        "カルシウム欠乏症 / 栄養性二次性上皮小体機能亢進症（NSHP）。"
        "カルシウム補充: "
        "  急性（低Ca痙攣/振戦時）: "
        "    グルコン酸カルシウム10% — 50-100 mg/kg IM/SC（IV避ける — 小型で困難）。"
        "    — ECGモニタリング推奨（徐脈に注意）。"
        "  維持: カルシウム補助食品（カルシウムパウダーを食事に添加）。"
        "ビタミンD3: 経口ビタミンD3サプリメント（Ca吸収促進）。"
        "  UVBライト照射: 12時間/日の光周期内で適切なUVB供給。"
        "食事改善（根本治療）: "
        "  Ca:P比 2:1を目標。"
        "  カルシウム豊富食: ブロッコリー、ケール、チンゲン菜。"
        "  リン過剰の回避: ヒマワリの種の過給与を制限。"
        "  良質なペレット食を基本食に（栄養バランス確保）。"
        "病的骨折の管理: "
        "  スプリント/外固定（可能であれば — ハムスターのサイズでは困難）。"
        "  ケージ内安静: 多層ケージ・回し車を一時撤去（落下防止）。"
        "鑑別: 骨粗鬆症（高齢）、骨腫瘍、外傷性骨折。"
        "予後: 食事改善で回復可能。重度の骨変形は不可逆的。"
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} hamster disease entries")


if __name__ == "__main__":
    apply_enrichments()
