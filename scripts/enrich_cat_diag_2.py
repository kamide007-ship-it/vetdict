#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["cat_congenital_heart_defect_-_ventricular_septal_defect"] = {
    "diagnosis_ja": (
        "聴診で右胸骨縁の全収縮期雑音。心エコー（2D+カラードプラ）で欠損孔の位置・サイズ・"
        "シャント方向を評価。Qp/Qs比でシャント量定量。胸部X線: 大欠損で肺過灌流+左心拡大。"
        "猫では小欠損が多く無症状で偶発的に発見されることが多い。心電図でLV肥大パターン。"
    )
}

ENRICHMENTS["cat_congenital_heart_defect_-_patent_ductus_arteriosus"] = {
    "diagnosis_ja": (
        "聴診で左心基底部の連続性（continuous）機械様雑音が特徴的。"
        "心エコー: カラードプラで大動脈→肺動脈のシャント血流を確認。LA/Ao比増大。"
        "胸部X線: 肺過灌流、左心拡大、大動脈弓/肺動脈の拡大（3 knob sign）。"
        "猫ではまれだが右→左シャント（逆PDA）→後肢チアノーゼの鑑別が重要。"
    )
}

ENRICHMENTS["cat_arrhythmia_-_atrial_fibrillation"] = {
    "diagnosis_ja": (
        "心電図で不整なRR間隔、f波（P波消失）、正常QRS幅。猫ではAFは稀で基礎心疾患が重篤。"
        "ホルター心電図で持続性/発作性を判定。心エコーで著明なLA拡大（基礎にHCM/DCM/RCM）。"
        "心室レートコントロール（目標<200bpm）。甲状腺機能亢進症の合併除外（T4測定）。"
    )
}

ENRICHMENTS["cat_arrhythmia_-_ventricular_tachycardia"] = {
    "diagnosis_ja": (
        "心電図で幅広いQRS（≥0.06sec）、連続3拍以上の規則的頻脈（>240bpm）。"
        "ホルター心電図で頻度・持続時間を定量。心エコーで基礎心疾患（HCM、DCM）評価。"
        "血液検査: 電解質（K、Mg）、T4（甲状腺機能亢進症は猫VTの重要な原因）。"
        "トロポニンI上昇は心筋障害を示唆。鑑別: 上室性頻脈の変行伝導との区別。"
    )
}

ENRICHMENTS["cat_pericardial_effusion"] = {
    "diagnosis_ja": (
        "元気消失、呼吸困難、腹部膨満（右心不全→腹水）。聴診で心音減弱。"
        "心エコーで心嚢液の貯留量+心タンポナーデ（右心房/右心室の拡張期虚脱）を評価。"
        "胸部X線: 球形心影。心嚢穿刺で液体の性状確認（血性→腫瘍性、黄色透明→感染性/特発性）。"
        "猫はFIPが最重要鑑別（黄色粘稠液、Rivalta陽性）。リンパ腫、心筋症関連も考慮。"
    )
}

ENRICHMENTS["cat_systemic_hypertension"] = {
    "diagnosis_ja": (
        "ドプラ血圧測定で収縮期>160mmHg（重度>180mmHg）。複数回の測定で確認（白衣高血圧除外）。"
        "標的臓器障害評価: 眼底検査（網膜剥離/出血→急性失明が初発症状のことがある）、"
        "心エコー（LV肥大）、腎機能（BUN/Cre/UPC/SDMA）。"
        "原因検索: CKD（最多）、甲状腺機能亢進症（T4）、DM、原発性アルドステロン症、"
        "褐色細胞腫。ISFMガイドラインに基づくリスク分類。"
    )
}

ENRICHMENTS["cat_inflammatory_bowel_disease_ibd"] = {
    "diagnosis_ja": (
        "慢性嘔吐/下痢（>3週）、体重減少。CBC/生化学でcobalamin(B12)低値、folate変動。"
        "腹部エコーで腸壁肥厚・層構造変化・リンパ節腫大を評価。"
        "消化管内視鏡+生検が確定: リンパ球プラスマ細胞性腸炎（最多型）のWSAVA組織学的スコアリング。"
        "小細胞型リンパ腫との鑑別が最重要（免疫組織化学: CD3/CD20、クロナリティ検査: PARR）。"
        "fPLI/Spec fPLで膵炎合併（triaditis）、TLIでEPIを除外。"
    )
}

ENRICHMENTS["cat_feline_pancreatitis"] = {
    "diagnosis_ja": (
        "非特異的症状: 食欲不振、嘔吐（犬ほど顕著でない）、腹痛（猫では見逃されやすい）。"
        "fPLI/Spec fPL>5.4μg/Lで感度79%。SNAP fPLがスクリーニングに有用。"
        "腹部エコーで膵臓の腫大・低輝度・周囲脂肪高輝度を評価（感度35-67%）。"
        "CBC: 軽度好中球増加。生化学: ALT/ALP上昇（肝併発）、黄疸（胆管閉塞）。"
        "Triaditis（IBD+胆管炎+膵炎の三臓器炎）の同時評価。cobalamin測定。"
    )
}

ENRICHMENTS["cat_hepatic_lipidosis_fatty_liver_disease"] = {
    "diagnosis_ja": (
        "肥満猫の2日以上の食欲廃絶→黄疸+肝腫大で強く疑診。生化学: 著明なALP上昇（猫では"
        "ALP半減期が短く上昇は有意）、GGT正常～軽度上昇、T-Bil上昇、低K。"
        "エコーガイド下FNA: 肝細胞内の空胞変性（脂肪滴）が細胞学的に確定。"
        "腹部エコーで肝臓の高輝度（高エコー）。凝固パネル（PT/APTT）で凝固障害評価。"
        "基礎疾患の検索（IBD、膵炎、DM、甲状腺機能亢進症、ストレス/環境変化）が必須。"
    )
}

ENRICHMENTS["cat_cholangitis___cholangiohepatitis"] = {
    "diagnosis_ja": (
        "黄疸、食欲不振、嘔吐、発熱。好中球性（急性: 細菌性）vsリンパ球性（慢性: 免疫介在性）。"
        "生化学: ALT/ALP/GGT/T-Bil上昇。fPLで膵炎合併評価。"
        "腹部エコー: 胆嚢壁肥厚、胆管拡張、肝実質輝度変化。エコーガイド下胆嚢穿刺→"
        "細菌培養（E. coli/Enterococcus多い）。肝生検でWSAVA分類（好中球性/リンパ球性/慢性）。"
        "猫はtriaditis（膵炎+IBD+胆管炎の三臓器炎）として発症することが多い。"
    )
}

ENRICHMENTS["cat_gastrointestinal_lymphoma"] = {
    "diagnosis_ja": (
        "高齢猫の慢性嘔吐、下痢、体重減少。低グレード（小細胞型T細胞、最多）vs高グレード（大細胞型）。"
        "腹部エコーで腸壁肥厚（筋層肥厚が特徴的）、腸管腫瘤、腸間膜リンパ節腫大。"
        "全層生検（外科的）>>内視鏡生検（低グレードの検出に限界あり）。"
        "免疫組織化学: CD3+（T細胞型が多い）/CD20+（B細胞型）。"
        "クロナリティ検査（PARR）でIBDとの鑑別。cobalamin(B12)低値は予後不良因子。"
    )
}

ENRICHMENTS["cat_megacolon"] = {
    "diagnosis_ja": (
        "慢性便秘→便秘→巨大結腸。直腸内指診で結腸内の石様硬い宿便。"
        "腹部X線で結腸の著明な拡張+宿便の貯留を確認。腸骨径/骨盤入口径の比>1.48で巨大結腸。"
        "骨盤骨折後の骨盤狭窄（二次性）vs特発性の鑑別。骨盤X線で骨折既往を確認。"
        "T4測定（甲状腺機能低下は稀だが除外）、脊髄/腰仙部の神経学的検査。"
        "電解質（低K→腸運動低下）、血糖。長期のマネジメント失敗で亜全結腸切除の適応。"
    )
}

ENRICHMENTS["cat_foreign_body_obstruction"] = {
    "diagnosis_ja": (
        "急性嘔吐、食欲廃絶、脱水。線状異物（糸/紐/リボン）が猫で特に多い→舌根部を確認。"
        "腹部X線: 腸管拡張、gas-fluid level、plication pattern（線状異物特異的）。"
        "腹部エコー: 拡張腸管、アコーディオン様蛇行（線状異物）、異物のエコー像。"
        "造影X線で閉塞部位の同定。CBC/生化学で脱水、電解質異常、腹膜炎評価。"
        "線状異物は絶対に口から引っ張って除去してはならない（腸管裂傷リスク）。"
    )
}

ENRICHMENTS["cat_gastric_ulcer"] = {
    "diagnosis_ja": (
        "嘔吐（吐血: coffee ground様/鮮血）、メレナ、食欲低下、腹痛。"
        "上部消化管内視鏡で潰瘍の直視確認+生検（腫瘍性vs非腫瘍性鑑別が必須）。"
        "CBC: 鉄欠乏性貧血（慢性出血）。便潜血陽性。"
        "原因検索: NSAIDs/コルチコステロイド使用歴、肥満細胞腫（皮膚/内臓型）、"
        "CKD（BUN/Cre）、肝疾患、IBD。腹部エコーで胃壁肥厚・腫瘤を評価。"
    )
}

ENRICHMENTS["cat_triaditis"] = {
    "diagnosis_ja": (
        "IBD+胆管炎+膵炎の三臓器同時炎症。嘔吐、食欲不振、黄疸、体重減少。"
        "Spec fPL（膵炎）、ALT/ALP/GGT/T-Bil（肝胆道）、cobalamin/folate（IBD）の統合評価。"
        "腹部エコーで膵臓・肝臓・腸管の同時異常所見を確認。"
        "消化管内視鏡+生検（IBD評価）、エコーガイド下胆嚢穿刺+培養（細菌性胆管炎評価）。"
        "猫の消化管解剖的特殊性: 総胆管と主膵管が十二指腸大乳頭で合流→感染の相互波及。"
    )
}

ENRICHMENTS["cat_gastroenteritis"] = {
    "diagnosis_ja": (
        "急性嘔吐+下痢。食餌変更、異物、感染（パルボ、サルモネラ）、中毒の鑑別。"
        "CBC/生化学/電解質で脱水度・臓器障害を評価。糞便検査（浮遊法+直接鏡検+抗原検査）。"
        "パルボウイルス抗原SNAP検査。腹部X線で閉塞除外。エコーで腸壁肥厚・異物評価。"
        "重症例: 血液培養、凝固パネル。猫汎白血球減少症（FPV）は緊急疾患→WBC著減が特徴。"
    )
}

ENRICHMENTS["cat_intestinal_parasitism"] = {
    "diagnosis_ja": (
        "糞便検査（浮遊法: 硫酸亜鉛/飽和食塩水）で虫卵/オーシスト/シストを検出。"
        "直接鏡検でGiardia/Tritrichomonas栄養体の運動を確認。Giardia SNAP抗原検査。"
        "主要寄生虫: 回虫（Toxocara cati）、鉤虫、条虫（Dipylidium/Taenia）、"
        "コクシジウム、Giardia、Tritrichomonas。CBC: 好酸球増加（寄生虫示唆）。"
        "子猫は重度感染で低蛋白血症、貧血、成長障害。複数回検査で検出率向上。"
    )
}

ENRICHMENTS["cat_rectal_prolapse"] = {
    "diagnosis_ja": (
        "肛門からの直腸粘膜/全層の脱出を肉眼確認。脱出組織の色調・浮腫・壊死を評価。"
        "プローブ挿入テスト: 脱出部と直腸壁間にプローブ挿入可=全層脱出。"
        "基礎疾患: 寄生虫（糞便検査）、大腸炎（細胞診）、巨大結腸、膀胱/尿道疾患。"
        "慢性しぶりの原因検索。全身状態（脱水、電解質）評価。子猫で寄生虫関連が多い。"
    )
}

ENRICHMENTS["cat_esophagitis"] = {
    "diagnosis_ja": (
        "嚥下困難、嚥下痛（食事中の鳴き声）、流涎、逆流。嘔吐との鑑別: 腹圧なし。"
        "食道内視鏡で粘膜発赤、びらん、潰瘍、狭窄を直視確認。"
        "食道造影X線で通過障害・狭窄を評価。原因: 全身麻酔後の胃酸逆流（最多）、"
        "異物（骨片）、腐食性物質、薬剤性（ドキシサイクリン錠が猫で特に重要→水で流すこと）。"
        "食道狭窄の合併評価。バルーン拡張術の適応検討。"
    )
}

ENRICHMENTS["cat_constipation___obstipation"] = {
    "diagnosis_ja": (
        "排便困難、しぶり、少量硬便、食欲低下。直腸内指診で硬い宿便を確認。"
        "腹部X線で結腸内の宿便貯留と結腸拡張度を評価。骨盤X線で骨盤狭窄を除外。"
        "生化学: 低K（腸運動低下の原因/結果）、BUN/Cre（脱水評価）、Ca。"
        "T4測定（甲状腺機能低下は稀）。神経学的検査（馬尾症候群、仙骨神経障害）。"
        "巨大結腸への進展評価。肥満、脱水、運動不足、食物繊維不足が素因。"
    )
}

ENRICHMENTS["cat_acute_kidney_injury_aki"] = {
    "diagnosis_ja": (
        "急性の食欲廃絶、嘔吐、乏尿/無尿。BUN/Cre急速上昇（48時間以内）。IRIS AKI Grade I-V。"
        "尿検査: 等張尿（尿比重<1.035）、円柱（顆粒円柱は腎尿細管障害）、糖尿。"
        "腹部エコー: 腎腫大+皮質輝度亢進。腎盂拡張で閉塞性AKIを除外。"
        "電解質: 高K（心毒性！心電図モニタリング）、高P、代謝性アシドーシス。"
        "原因検索: ユリ中毒（猫特異的、致死的）、エチレングリコール、NSAIDs、腎盂腎炎、閉塞。"
    )
}

ENRICHMENTS["cat_urinary_obstruction_blocked_cat"] = {
    "diagnosis_ja": (
        "排尿姿勢+排尿不能、鳴き声、腹部膨満。膀胱触診で緊満した石様膀胱。"
        "緊急血液検査: 高K（>7mEq/Lで致死的不整脈）、高BUN/Cre、代謝性アシドーシス。"
        "心電図: 高K性変化（T波尖鋭化→P波消失→QRS幅広化→洞停止）。"
        "閉塞原因: 尿道栓子（ストルバイト結晶+粘液）、尿路結石、尿道攣縮、腫瘍。"
        "尿検査/培養（カテーテル減圧後）。腹部X線/エコーで結石・膀胱壁肥厚を評価。雄猫に圧倒的好発。"
    )
}

ENRICHMENTS["cat_urolithiasis_bladder_stones"] = {
    "diagnosis_ja": (
        "血尿、頻尿、排尿困難、不適切な排尿場所。腹部X線でストルバイト/シュウ酸Ca結石を検出。"
        "尿酸塩結石はX線透過性→エコーで検出。腹部エコーで膀胱内結石+膀胱壁肥厚を評価。"
        "尿検査: pH（ストルバイト>7.0、シュウ酸Ca<6.5）、結晶同定、尿培養。"
        "結石分析（定量分析: 赤外分光法）が結石組成確定に最重要。"
        "猫ではシュウ酸Caが約55%、ストルバイトが約45%（犬と異なる比率）。"
    )
}

ENRICHMENTS["cat_pyelonephritis"] = {
    "diagnosis_ja": (
        "発熱、腰背部痛（腎臓触診時の疼痛）、元気消失。"
        "尿検査: 膿尿+細菌尿+白血球円柱（上部尿路感染に特異的）。尿培養+感受性試験。"
        "CBC: 好中球増加+左方移動。生化学: BUN/Cre上昇（AKI合併時）。"
        "腹部エコー: 腎盂拡張、腎皮質輝度亢進、腎実質のheterogeneity。"
        "猫ではCKDや糖尿病が素因。E. coliが最も多い起因菌。上行性感染経路。"
    )
}

ENRICHMENTS["cat_feline_idiopathic_cystitis_fic"] = {
    "diagnosis_ja": (
        "若～中年猫の急性血尿、頻尿、排尿困難、不適切な排尿場所。自然寛解/再発を繰り返す。"
        "尿検査: 血尿+膿尿軽度、細菌培養陰性（FICは無菌性膀胱炎）。"
        "腹部X線/エコーで結石・腫瘤を除外。膀胱壁肥厚（非特異的）。"
        "除外診断: UTI（培養陰性）、結石（X線/エコー陰性）、腫瘍、行動性。"
        "ストレス因子の評価（多頭飼育、環境変化、トイレ条件）。MEMO（multimodal environmental "
        "modification）が治療の中心。猫FLUTDの55-69%がFIC。"
    )
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
    print(f"Updated {updated}/{len(ENRICHMENTS)} entries")


if __name__ == "__main__":
    apply_enrichments()
