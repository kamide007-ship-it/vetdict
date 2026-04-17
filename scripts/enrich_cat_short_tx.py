#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# --- Batch 1: 胃腸炎, 食道狭窄, 胆嚢炎, EPI ---

ENRICHMENTS["cat_gastroenteritis"] = {
    "treatment_ja": (
        "猫の慢性胃腸炎（IBD）。食事療法と免疫抑制が治療の柱。"
        "食事療法（第一段階 — 4-8週間の試験）: "
        "  新奇蛋白食（ベニソン、ラビット等）or 加水分解蛋白食。"
        "  最低8-12週間の厳格な除去食試験（おやつ含め厳密に）。"
        "  反応率40-50%（食事のみで改善する猫が存在）。"
        "免疫抑制療法: "
        "  プレドニゾロン1-2 mg/kg PO q24h × 2-4週 → 漸減（0.5 mg/kg q48h目標）。"
        "  クロラムブシル0.1-0.2 mg/kg PO q24-48h（ステロイド不応時 — 低悪性度リンパ腫との鑑別重要）。"
        "  ブデソニド1 mg/cat PO q24h（全身性ステロイド忌避時 — 肝初回通過代謝）。"
        "コバラミン補充（必須）: "
        "  250 μg SC 週1回 × 6週 → 月1回。or 経口（250 μg/日）。"
        "  猫のIBDでは90%以上がコバラミン低値。"
        "プロバイオティクス: FortiFlora等。"
        "確定診断: 内視鏡＋生検（リンパ腫との鑑別が最も重要）。"
        "  クロナリティ検査（PARR）: リンパ球のモノクローナル性 → リンパ腫。"
        "鑑別: 低悪性度消化管リンパ腫（IBDと臨床的に区別困難）。"
        "予後: IBDは管理可能（良好）。リンパ腫併存時はクロラムブシル+ステロイドで中央生存期間2年。"
    ),
}

ENRICHMENTS["cat_feline_esophageal_stricture"] = {
    "treatment_ja": (
        "食道の瘢痕性狭窄。麻酔後の胃食道逆流（GER）が最多原因。"
        "バルーン拡張術（第一選択）: "
        "  内視鏡下でバルーンカテーテルを狭窄部に留置→段階的拡張。"
        "  1回の拡張では不十分な場合が多い → 2-4回の繰り返しが必要。"
        "  拡張間隔: 1-2週間毎。過度の拡張 → 穿孔リスク。"
        "再狭窄予防: "
        "  プレドニゾロン1 mg/kg PO q24h × 2-4週（抗線維化）。"
        "  トリアムシノロン局所注射（拡張後に狭窄部粘膜下に）。"
        "  オメプラゾール1 mg/kg PO q12h（酸逆流による再損傷防止）。"
        "  スクラルファート25-50 mg/kg PO q8h（粘膜保護）。"
        "難治性狭窄: "
        "  食道ステント留置（self-expanding metallic stent）。"
        "  外科的食道切除＋吻合（最終手段 — 合併症率高い）。"
        "原因: 麻酔後GER（最多）、異物、腐食性物質の誤飲、ドキシサイクリン（猫で食道炎の原因）。"
        "  ドキシサイクリン投与後は必ず水（5 mL以上）を飲ませること。"
        "栄養管理: 流動食 → 段階的に固形食。経胃瘻チューブ（重度の狭窄時）。"
        "予後: バルーン拡張で60-80%が改善。多発性/長い狭窄は予後不良。"
    ),
}

ENRICHMENTS["cat_feline_cholecystitis"] = {
    "treatment_ja": (
        "胆嚢の炎症/感染。猫では犬より稀だがtriaditis（膵炎+胆管肝炎+IBD）の一環として好発。"
        "抗菌薬療法（4-6週間以上の長期投与）: "
        "  アモキシシリン/クラブラン酸12.5-25 mg/kg PO q12h（嫌気性菌カバー）。"
        "  + メトロニダゾール7.5-10 mg/kg PO q12h（嫌気性菌追加カバー）。"
        "  代替: マルボフロキサシン2 mg/kg PO q24h（グラム陰性菌）。"
        "  胆汁培養に基づく調整が理想的（胆嚢穿刺 or 術中採取）。"
        "  一般的起因菌: E. coli, Enterococcus, Clostridium, Bacteroides。"
        "肝保護: "
        "  UDCA（ウルソデオキシコール酸）10-15 mg/kg PO q24h（胆汁うっ滞改善）。"
        "  SAMe（S-アデノシルメチオニン）90 mg/cat PO q24h（抗酸化）。"
        "  シリマリン（マリアアザミ）— 補助的。"
        "外科適応: "
        "  胆嚢穿孔/破裂 → 緊急胆嚢摘出術（cholecystectomy）+ 腹腔洗浄。"
        "  胆嚢粘液嚢腫（mucocele — 犬ほど一般的ではない）。"
        "  総胆管閉塞 → 胆管-十二指腸吻合/胆管ステント。"
        "Triaditis同時評価: 膵炎（fPLI）+ 腸生検（IBD/リンパ腫）の精査。"
        "予後: 内科管理で改善が期待できるが、triaditis併発時は長期管理が必要。"
    ),
}

ENRICHMENTS["cat_feline_exocrine_pancreatic_insufficiency_epi"] = {
    "treatment_ja": (
        "膵外分泌不全。猫では犬より稀（慢性膵炎後の続発が多い — 犬は膵腺房萎縮が主因）。"
        "膵酵素補充療法（PERT — 生涯投与）: "
        "  粉末酵素製剤（パンクレアチン）: 食事毎に混合。"
        "  小さじ1/2〜1杯/食（体重・症状で調整）。"
        "  生の膵臓組織: 30-60g/食（代替 — 酵素活性が高い）。"
        "  食事20-30分前に混合し室温で放置（酵素の事前活性化）。"
        "コバラミン補充（猫で特に重要 — ほぼ全例で低値）: "
        "  250 μg SC 週1回 × 6週 → 月1回。"
        "  or 経口コバラミン250 μg/日（最近のエビデンスで注射と同等の有効性）。"
        "  コバラミン低値 → 治療反応不良の最大の原因。"
        "食事: 高消化性/低繊維食。脂肪制限は不要（酵素補充で脂肪吸収改善）。"
        "  少量頻回給餌（3-4回/日）。"
        "診断: fTLI<8 μg/L（確定診断）。コバラミン/葉酸同時測定。"
        "基礎疾患: 慢性膵炎の管理（猫EPIの主因）。"
        "  triaditis（膵炎+IBD+胆管肝炎）の評価。"
        "予後: PERT+コバラミン補充で良好。体重増加は2-4週間で確認。"
        "  猫は犬と異なり、膵臓の部分的機能回復の可能性あり。"
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} cat disease entries")


if __name__ == "__main__":
    apply_enrichments()
