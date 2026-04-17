#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# --- Batch 1: CKD, 喘息, 歯周病, 低血糖 ---

ENRICHMENTS["cat_0004"] = {
    "diagnosis_ja": (
        "慢性腎臓病（CKD）の診断は血液検査、尿検査、画像検査に基づく。"
        "猫で最も一般的な腎疾患。7歳以上の猫の約30-40%が罹患。"
        "IRIS（International Renal Interest Society）ステージ分類:"
        "  Stage 1: Cre<1.6 mg/dL（SDMA>14 μg/dL）— 非高窒素血症期。"
        "  Stage 2: Cre 1.6-2.8 mg/dL — 軽度高窒素血症。"
        "  Stage 3: Cre 2.9-5.0 mg/dL — 中等度高窒素血症。"
        "  Stage 4: Cre>5.0 mg/dL — 重度高窒素血症。"
        "血液検査: BUN/Cre上昇、SDMA上昇（Creより早期に上昇）、"
        "  高リン血症、低K血症、非再生性貧血（Epo産生低下）。"
        "尿検査: 尿比重低下（<1.035 — 濃縮能低下）、蛋白尿（UPC>0.4）。"
        "血圧測定: 高血圧（>160 mmHg — 標的臓器障害リスク）。"
        "腹部超音波: 腎サイズ縮小（慢性）・不整、皮髄境界不明瞭化。"
        "  腎盂拡張（水腎症の除外）、尿管結石の検索。"
        "鑑別診断: 急性腎障害（AKI）、尿管閉塞、腎リンパ腫、腎アミロイドーシス。"
    ),
}

ENRICHMENTS["cat_0008"] = {
    "diagnosis_ja": (
        "猫喘息（Feline Asthma）の診断は臨床所見、X線検査、除外診断に基づく。"
        "下気道の好酸球性炎症＋気管支攣縮。猫の慢性咳嗽の最多原因。"
        "推定有病率: 全猫の1-5%。シャム猫で好発傾向。"
        "臨床所見: 発作性咳嗽（乾性、非生産性）、呼気性呼吸困難（腹式呼吸）、"
        "  喘鳴（wheezing）、開口呼吸（重症発作時）。"
        "  慢性例: 運動不耐性、間欠性咳嗽。"
        "胸部X線: 気管支壁肥厚（donut sign/tram lines）、"
        "  肺過膨張（横隔膜の平坦化）、間質〜肺胞パターン。"
        "  重症発作時: 右中葉の無気肺（粘液栓塞）。"
        "BAL（気管支肺胞洗浄）: 好酸球>17%（正常<5%）— 確定的。"
        "  好中球優位→感染性気管支炎を示唆。"
        "糞便検査: 肺虫（Aelurostrongylus abstrusus）の除外。"
        "心エコー: 心原性呼吸困難の除外。"
        "鑑別診断: 慢性気管支炎、肺虫症、心不全、肺腫瘍、胸水。"
    ),
}

ENRICHMENTS["cat_0009"] = {
    "diagnosis_ja": (
        "猫の歯肉炎・歯周病の診断は口腔検査と歯科X線検査に基づく。"
        "歯周病は猫で最も一般的な口腔疾患（3歳以上の70%以上）。"
        "臨床所見: 口臭（最も早い徴候）、歯肉発赤・腫脹・出血、"
        "  歯石沈着、歯の動揺、食欲低下（疼痛による）、流涎、"
        "  片側咀嚼、食物の落下、顔面腫脹（根尖膿瘍時）。"
        "  猫特有: 歯頸部吸収病変（FORL/TR）の併発が多い。"
        "口腔検査: 歯肉指数（GI）、プロービング（歯周ポケット深度）、"
        "  歯の動揺度評価 — 全身麻酔下で実施。"
        "歯科X線（全口腔X線）: 歯槽骨吸収（水平性/垂直性）、"
        "  歯根吸収（FORL Type 1/2/3の鑑別）、根尖病変。"
        "  猫では全口腔X線が歯科処置の標準。"
        "血液検査: FIV/FeLV検査（免疫状態評価）、"
        "  基礎疾患スクリーニング（CKD、DM）。"
        "鑑別診断: 猫慢性歯肉口内炎（FCGS）、口腔腫瘍（SCC）、好酸球性肉芽腫。"
    ),
    "treatment_ja": (
        "歯科スケーリング＋ポリッシング: 全身麻酔下。歯石除去（超音波スケーラー）、"
        "  歯肉縁下キュレッタージ、研磨。"
        "重度歯周病: 罹患歯の抜歯（猫では保存療法より抜歯が推奨されることが多い）。"
        "  FORL Type 1: 全抜歯。Type 2: 歯冠切断術（Crown amputation）。"
        "  根尖膿瘍: 抜歯＋膿瘍ドレナージ。"
        "抗菌薬（重度感染時）: クリンダマイシン5.5-11 mg/kg PO q12h × 7-10日。"
        "  アモキシシリン-クラブラン酸12.5-25 mg/kg PO q12h。"
        "疼痛管理: メロキシカム0.05 mg/kg PO/SC q24h（短期）、"
        "  ブプレノルフィン0.02 mg/kg OTM q8-12h（周術期）。"
        "家庭ケア: 歯磨き（酵素歯磨き粉）、デンタルダイエット（VOHC認定製品）。"
        "予後: 定期的な歯科処置で管理可能。FCGS併発例は全臼歯抜歯が必要な場合あり。"
    ),
}

ENRICHMENTS["cat_0010"] = {
    "diagnosis_ja": (
        "猫の低血糖症の診断は血糖値測定に基づく。"
        "血糖値<60 mg/dL（3.3 mmol/L）で臨床症状発現。"
        "原因: インスリン過量投与（DM治療中 — 最多）、インスリノーマ（猫ではまれ）、"
        "  敗血症、重度肝不全、副腎皮質機能低下症、"
        "  新生子（低体温・低栄養）、腫瘍随伴症候群。"
        "臨床所見: 脱力、運動失調、震戦、嗜眠、痙攣、昏睡（重症）。"
        "  DM猫のインスリン過量: Somogyi効果（反跳性高血糖）にも注意。"
        "血液検査: 血糖値、血清インスリン（インスリノーマ疑い時 — インスリン/グルコース比）、"
        "  肝機能検査（ALT、ALP、アルブミン）、"
        "  コルチゾール（副腎機能低下症疑い）。"
        "腹部超音波: 膵腫瘤（インスリノーマ）、肝腫瘤、副腎サイズ。"
        "鑑別診断: 痙攣の他の原因（てんかん、中毒、脳疾患）。"
    ),
    "treatment_ja": (
        "緊急治療（痙攣・昏睡時）: 50%デキストロース0.5-1 mL/kg IV slow（5分で投与）→"
        "  2.5-5%デキストロース持続点滴で維持。"
        "  口腔粘膜にコーンシロップ/蜂蜜塗布（自宅応急処置）。"
        "インスリン過量（DM猫）: インスリン用量の再調整。"
        "  血糖曲線の再作成（8-12時間モニタリング）。"
        "  ナディア血糖値>80 mg/dLを目標。"
        "インスリノーマ（まれ）: 外科的切除、ジアゾキシド5-30 mg/kg PO q12h、"
        "  プレドニゾロン1-2 mg/kg PO q12h（糖新生促進）。"
        "肝不全: 原疾患治療、頻回少量給餌。"
        "新生子: 保温、頻回授乳/人工乳。"
        "敗血症: 原因感染症の治療＋デキストロース補充。"
        "予後: 原因に依存。インスリン調整で管理可能なDM猫は良好。"
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
