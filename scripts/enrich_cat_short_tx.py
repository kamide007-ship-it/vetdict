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


# --- Batch 2: 熱射病, 好酸球性腸炎, ヘモミヌータム, PDA ---

ENRICHMENTS["cat_feline_heat_stroke"] = {
    "treatment_ja": (
        "体温>40.5°C（105°F）。猫は犬より熱射病は少ないが発症時は致死的。"
        "即座の冷却（最重要 — 搬送中にも開始）: "
        "  常温水（15-25°C）の散布 + 扇風機。"
        "  氷水/冷水は禁忌（末梢血管収縮 → 放熱阻害）。"
        "  四肢パッド・鼠径部・頸部にアルコールスプレー。"
        "  直腸温39.5°C（103.1°F）で冷却中止（過冷却防止）。"
        "輸液: 晶質液（乳酸リンゲル/生食）— 循環血液量の維持。"
        "  ショック用量: 45-60 mL/kg/hr（猫はショックレート低い）。"
        "臓器障害管理: "
        "  DIC: PT/aPTT/Dダイマー/血小板モニタリング。新鮮凍結血漿。"
        "  AKI: 尿量モニタリング（目標: 1-2 mL/kg/hr）。BUN/Cre/電解質。"
        "  消化管: メトロニダゾール（細菌転座予防）。スクラルファート。"
        "  脳浮腫: マンニトール0.5-1 g/kg IV（神経症状時）。"
        "48-72時間ICUモニタリング必須（遅発性臓器不全リスク）。"
        "リスク因子: 密閉車内、肥満、短頭種（ペルシャ、エキゾチックSH）、長毛種。"
        "予後: 体温>41.5°Cで予後悪化。DIC併発で致死率>50%。早期冷却で改善。"
    ),
}

ENRICHMENTS["cat_feline_eosinophilic_enteritis"] = {
    "treatment_ja": (
        "好酸球浸潤による消化管炎症。食物アレルギー/寄生虫が誘因の場合あり。"
        "食事試験（第一段階）: "
        "  新奇蛋白食（ベニソン、ラビット、ダック）or 加水分解蛋白食。"
        "  最低8-12週間の厳格な除去食試験。"
        "  食事反応性の場合 → 長期的にその食事を継続。"
        "寄生虫駆虫（全例で実施）: "
        "  フェンベンダゾール50 mg/kg PO q24h × 5日。"
        "  プラジカンテル5 mg/kg PO（条虫）。"
        "免疫抑制療法（食事不応時）: "
        "  プレドニゾロン2 mg/kg PO q24h × 2-4週 → 漸減（0.5-1 mg/kg q48h）。"
        "  クロラムブシル0.1-0.2 mg/kg PO q24-48h（ステロイド不応 or リンパ腫鑑別困難時）。"
        "コバラミン補充: 250 μg SC 週1回 × 6週 → 月1回。"
        "確定診断: 内視鏡＋生検（粘膜固有層の好酸球浸潤）。"
        "  好酸球増多症（末梢血）は存在しないこともある。"
        "鑑別: IBD（リンパ球性）、低悪性度リンパ腫、好酸球性肉芽腫複合体、"
        "  好酸球性増多症候群（hypereosinophilic syndrome — 多臓器浸潤）。"
        "予後: 食事反応性は優秀。ステロイド反応性も良好。"
    ),
}

ENRICHMENTS["cat_feline_feline_infectious_anemia_candidatus_m._haemominutum"] = {
    "treatment_ja": (
        "Candidatus M. haemominutum感染。M. haemofelisより病原性低い（日和見的）。"
        "治療適応の判断: "
        "  健常猫での検出 → 臨床的意義は低い（治療不要の場合が多い）。"
        "  免疫低下猫（FeLV/FIV陽性、化学療法中、脾摘後）→ 臨床化しうる → 治療。"
        "  貧血の存在 → 他の原因（M. haemofelis重複感染、IMHA、FeLV）を除外。"
        "抗菌薬療法（臨床症状がある場合）: "
        "  ドキシサイクリン10 mg/kg PO q12h × 28日。"
        "  — 食道炎予防: 投与後に水5 mL以上 or バターで服用。"
        "  代替: マルボフロキサシン2 mg/kg PO q24h × 28日。"
        "  — 完全なPCR陰転は困難（キャリア状態の持続が一般的）。"
        "FeLV/FIV検査: 全例で実施（免疫低下がM. haemominutumの臨床化に関与）。"
        "重度貧血時: 輸血（PCV<15%）。交差適合試験必須。"
        "  プレドニゾロン2 mg/kg PO q24h（免疫介在性溶血の成分がある場合）。"
        "予後: M. haemominutum単独感染は良好。"
        "  FeLV/FIV重複感染時は基礎疾患の予後に依存。"
    ),
}

ENRICHMENTS["cat_congenital_heart_defect_-_patent_ductus_arteriosus"] = {
    "treatment_ja": (
        "動脈管開存症（PDA）。猫では犬より稀だが病態・治療は類似。"
        "根治的治療: "
        "  ACDO（Amplatz Canine Duct Occluder）: カテーテルインターベンション。"
        "  — 低侵襲で成功率>95%（犬のデータ — 猫でも小型用デバイスで実施可能）。"
        "  外科的結紮: 左第4肋間開胸 → 動脈管の二重結紮。"
        "  — 猫の小さな体サイズでは技術的に繊細。"
        "  術前心不全管理: フロセミド2 mg/kg PO/IV q12h + ピモベンダン0.25 mg/kg PO q12h。"
        "心エコー所見: 連続性雑音（continuous machinery murmur — 左心基部）。"
        "  左心室・左心房の容量過負荷（拡張）。"
        "  ドップラー: 肺動脈内の連続性逆行血流。"
        "左→右シャント（典型的）: うっ血性心不全 → 早期手術推奨。"
        "右→左シャント（Eisenmenger化 — 稀）: 手術禁忌。"
        "  差別的チアノーゼ（後肢のみチアノーゼ）。赤血球増加症。"
        "術後: 心エコーフォローアップ。残存シャントの評価。"
        "  心腔サイズの正常化に数週-数ヶ月。"
        "予後: 早期手術で優秀（正常寿命期待可能）。無治療は1年以内に心不全進行。"
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
