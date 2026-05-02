#!/usr/bin/env python3
import json
import os
import time

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diseases_all_species.json")

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_iliopsoas_muscle_strain"] = {
    "diagnosis_ja": (
        "触診で腸腰筋部の疼痛・緊張を確認。股関節伸展+内旋で疼痛誘発（iliopsoas stretch test陽性）。"
        "X線で骨盤・腰椎の異常を除外。超音波で筋肉の腫脹・エコー輝度変化・線維断裂を評価。"
        "MRIで筋肉内T2高信号（浮腫/出血）を確認。CT/MRIで腰椎椎間板疾患との鑑別。"
        "CRP/SAAで炎症マーカーを評価。慢性例では筋萎縮の有無を触診・画像で確認。"
    )
}

ENRICHMENTS["dog_gracilis_semitendinosus_myopathy"] = {
    "diagnosis_ja": (
        "歩様検査で特徴的な外旋歩行（circumduction gait）を確認。触診で薄筋・半腱様筋の索状硬化・短縮を検出。"
        "超音波で筋線維の線維化・石灰化を評価。MRIでT1低信号/T2高信号の筋変性パターン。"
        "筋生検で線維化・変性・再生像を確認。CK値は正常～軽度上昇。EMGで異常自発電位の有無。"
        "ジャーマン・シェパード、ベルジアン・マリノアの好発犬種歴を確認。"
    )
}

ENRICHMENTS["dog_sesamoid_disease"] = {
    "diagnosis_ja": (
        "X線で種子骨の骨折・断片化・変形・石灰化を確認。屈曲・伸展ストレスビューで評価。"
        "触診で中手骨パッド部の腫脹・疼痛を検出。デジタルX線で微細骨折を検出。"
        "CTで複雑な骨折パターンを三次元評価。超音波で周囲軟部組織の炎症を評価。"
        "関節液検査で二次性関節炎の有無を確認。歩様解析で荷重異常を定量化。"
    )
}

ENRICHMENTS["dog_necrotizing_meningoencephalitis_nme"] = {
    "diagnosis_ja": (
        "MRIで大脳皮質・皮髄境界のT2/FLAIR高信号、造影後増強を確認。病変は非対称性で壊死巣を伴う。"
        "CSF検査で単核球優位の細胞数増多（50-500/μL）、蛋白上昇。抗GFAPα抗体陽性が特異的。"
        "感染性脳炎（CDV、真菌、トキソプラズマ）を血清学・PCRで除外。CT/MRIで腫瘍性病変を除外。"
        "パグ、マルチーズ、チワワ、ヨークシャー・テリアの好発犬種。脳生検で壊死性炎症を確認。"
    )
}

ENRICHMENTS["dog_necrotizing_leukoencephalitis_nle"] = {
    "diagnosis_ja": (
        "MRIで脳幹・小脳白質のT2/FLAIR高信号、壊死性変化を確認。大脳白質にも非対称性病変。"
        "CSF検査で単核球優位の軽度～中等度細胞数増多、蛋白上昇。"
        "感染性疾患（CDV、真菌、原虫）をPCR・血清学で除外。血液検査でCBC、生化学は概ね正常。"
        "ヨークシャー・テリア、フレンチ・ブルドッグに好発。NMEとの鑑別はMRI病変分布と病理で行う。"
    )
}

ENRICHMENTS["dog_spinal_arachnoid_diverticulum"] = {
    "diagnosis_ja": (
        "脊髄造影（myelography）で背側くも膜下腔の嚢状拡張を確認。CT myelographyで三次元評価。"
        "MRIでT2高信号の嚢胞性病変が脊髄背側に描出。脊髄の圧迫・変形を評価。"
        "CSF検査で感染・炎症を除外（通常正常）。X線で椎体異常を除外。"
        "好発部位はC2-C3（頸部型）またはT10-L2（胸腰部型）。進行性後肢不全麻痺の鑑別に含む。"
    )
}

ENRICHMENTS["dog_steroid-responsive_meningitis-arteritis_srma"] = {
    "diagnosis_ja": (
        "CSF検査で好中球優位の著明な細胞数増多（100-10,000/μL）、蛋白著増。CSF中IgA濃度上昇が特徴的。"
        "血清IgA上昇。CRP/SAA著増（急性期マーカー）。CBC/生化学で白血球増多。"
        "血液培養で細菌性髄膜炎を除外。MRIで髄膜造影増強（dural enhancement）を確認。"
        "頸部硬直・発熱・疼痛の三徴。ビーグル、ボクサー、バーニーズに好発。ステロイド反応性を治療的に確認。"
    )
}

ENRICHMENTS["dog_canine_spinal_muscular_atrophy"] = {
    "diagnosis_ja": (
        "EMG（筋電図）で脱神経電位（線維自発電位、陽性鋭波）を検出。神経伝導速度は正常または軽度低下。"
        "筋生検で群性萎縮（neurogenic atrophy）を確認。遺伝子検査で原因変異を同定（犬種特異的）。"
        "CK値は正常～軽度上昇。MRIで脊髄の形態異常を評価。CSF検査は正常。"
        "ブリタニー・スパニエル、ジャーマン・シェパード等に好発。若齢発症の進行性四肢筋萎縮で疑う。"
    )
}

ENRICHMENTS["dog_lissencephaly"] = {
    "diagnosis_ja": (
        "MRIで大脳皮質の脳溝・脳回の欠如（agyria）または減少（pachygyria）を確認。皮質の肥厚・平滑化。"
        "CT/MRIで水頭症の合併を評価。EEGで異常脳波パターン（てんかん性放電）を確認。"
        "神経学的検査で視覚障害、行動異常、学習能力低下を評価。血液検査は概ね正常。"
        "リャサ・アプソ、ワイヤーヘアード・フォックス・テリアに好発。先天性で幼若齢から症状。"
    )
}

ENRICHMENTS["dog_peripheral_nerve_sheath_tumor"] = {
    "diagnosis_ja": (
        "MRIで神経に沿った紡錘形の造影増強腫瘤を確認。T1等～低信号、T2高信号。"
        "EMGで脱神経パターンを検出。CT/MRIで腫瘍の範囲・脊柱管内進展を評価。"
        "超音波ガイド下FNA/生検で細胞診・病理診断。組織学的にS-100蛋白陽性。"
        "進行性の単肢跛行・筋萎縮・根性疼痛で疑う。術前CT/MRIで切除可能性を評価。"
    )
}

ENRICHMENTS["dog_spongiform_leukoencephalomyelopathy"] = {
    "diagnosis_ja": (
        "MRIで脊髄・脳幹白質のびまん性T2高信号を確認。海綿状変化に対応する画像所見。"
        "CSF検査は通常正常。EMG/神経伝導速度検査で中枢性病変パターンを確認。"
        "神経学的検査で全身性UMN/LMN徴候を評価。血液検査・尿検査で代謝性疾患を除外。"
        "オーストラリアン・キャトル・ドッグ、サルーキ等に犬種特異的。確定診断は病理（白質空胞変性）。"
    )
}

ENRICHMENTS["dog_tricuspid_valve_dysplasia"] = {
    "diagnosis_ja": (
        "心エコー検査で三尖弁の形態異常（弁葉肥厚、腱索短縮、乳頭筋異常）と三尖弁逆流を確認。"
        "カラードプラで逆流ジェットの重症度を評価。右房・右室の拡大を定量化。"
        "心電図でP波増大（右房拡大）、右軸偏位、心房細動の有無。X線で右心系拡大・肝腫大。"
        "ラブラドール・レトリーバー、グレート・デーンに好発。先天性心疾患として幼若齢から聴診で雑音。"
    )
}

ENRICHMENTS["dog_subaortic_stenosis_sas"] = {
    "diagnosis_ja": (
        "心エコー検査で左室流出路（LVOT）の線維性リング/膜様狭窄を確認。連続波ドプラで圧較差を測定"
        "（軽度<50 mmHg、中等度50-80、重度>80 mmHg）。M-モードで大動脈弁閉鎖不全を評価。"
        "聴診で左心基底部の駆出性収縮期雑音（grade III-VI/VI）。X線で左室肥大・大動脈後拡張。"
        "心電図でST変化・不整脈。ニューファンドランド、ゴールデン・レトリーバー、ボクサーに好発。"
    )
}

ENRICHMENTS["dog_cardiac_tamponade"] = {
    "diagnosis_ja": (
        "心エコー検査で心嚢液貯留と右房・右室の拡張期虚脱（diastolic collapse）を確認。"
        "心嚢穿刺で液性状を評価（血性：HSA/腫瘍、滲出性：感染/特発性）。PCV/TP・細胞診を実施。"
        "心電図で電気的交互脈（electrical alternans）、低電位。X線で球状心陰影。"
        "血圧低下、頸静脈怒張、心音減弱のBeck三徴。ゴールデン・レトリーバーにHSA好発。緊急心嚢穿刺が必要。"
    )
}

ENRICHMENTS["dog_cor_pulmonale"] = {
    "diagnosis_ja": (
        "心エコー検査で右室壁肥厚・右室拡大、心室中隔の左方偏位を確認。三尖弁逆流速度から肺動脈圧を推定。"
        "X線で右心拡大、肺動脈拡張、肺血管パターン異常を評価。肺野にびまん性間質パターン。"
        "心電図で右軸偏位、P pulmonale、右室肥大パターン。動脈血ガスで低酸素血症（PaO₂<60 mmHg）。"
        "基礎肺疾患（フィラリア症、肺線維症、慢性気管支炎）の精査。NT-proBNP上昇。"
    )
}

ENRICHMENTS["dog_ventricular_tachycardia"] = {
    "diagnosis_ja": (
        "心電図でワイドQRS頻拍（>160 bpm）を確認。3連発以上の心室性期外収縮が連続。"
        "ホルター心電図で24時間の不整脈頻度・重症度を評価（>1,000 VPCs/日は有意）。"
        "心エコーで基礎心疾患（DCM、SAS、腫瘍）を評価。血液検査で電解質異常（K⁺, Mg²⁺）を除外。"
        "トロポニンI上昇は心筋障害を示唆。ボクサー（ARVC）、ドーベルマン（DCM）に好発。"
    )
}

ENRICHMENTS["dog_third-degree_atrioventricular_block"] = {
    "diagnosis_ja": (
        "心電図でP波とQRS群の完全解離を確認。心室レートは低い補充調律（20-40 bpm）。"
        "ホルター心電図で間欠性/持続性を評価。心エコーで基礎心疾患・心筋症を除外。"
        "血液検査でBUN/Cre（腎性徐脈）、電解質（高K⁺）、甲状腺機能を評価。"
        "トロポニンI・NT-proBNPで心筋障害を評価。失神・運動不耐性の病歴。永久ペースメーカー適応の判断。"
    )
}

ENRICHMENTS["dog_hyperaldosteronism_conn's_syndrome"] = {
    "diagnosis_ja": (
        "血液検査で低カリウム血症（K⁺<3.5 mEq/L）、代謝性アルカローシスを確認。"
        "血漿アルドステロン濃度上昇、血漿レニン活性抑制（ARR比上昇）。ACTH刺激試験でクッシング除外。"
        "腹部超音波/CT/MRIで副腎腫瘤を同定。対側副腎の萎縮を確認。"
        "尿比重低下、多飲多尿の病歴。全身性高血圧の合併を血圧測定で評価。犬では極めて稀。"
    )
}

ENRICHMENTS["dog_acromegaly_growth_hormone_excess"] = {
    "diagnosis_ja": (
        "血清IGF-1（インスリン様成長因子）上昇が最も信頼性の高い指標。血清GH上昇。"
        "頭部MRI/CTで下垂体腫大・腫瘍を確認。血糖値上昇・インスリン抵抗性（糖尿病合併）。"
        "身体検査で顔面・四肢の軟部組織肥大、下顎突出、歯間離開を確認。"
        "未避妊雌ではプロゲステロン誘導性GH過剰を鑑別（OHE後に改善）。犬では稀。"
    )
}

ENRICHMENTS["dog_hypoparathyroidism"] = {
    "diagnosis_ja": (
        "血液検査で低カルシウム血症（総Ca<7.0 mg/dL、イオン化Ca低下）と高リン血症を確認。"
        "血清PTH濃度低値～測定感度以下（低Ca+低PTH=原発性副甲状腺機能低下症の確定）。"
        "25(OH)ビタミンD・マグネシウム値を評価。心電図でQT延長、徐脈を確認。"
        "振戦、テタニー、痙攣の臨床症状。甲状腺術後の医原性、免疫介在性破壊が主因。"
    )
}

ENRICHMENTS["dog_diabetic_ketoacidosis_dka"] = {
    "diagnosis_ja": (
        "血糖値著増（>300 mg/dL）、血液ガスで代謝性アシドーシス（pH<7.3、HCO₃⁻<15 mEq/L）。"
        "尿検査でグルコース尿・ケトン尿（3+以上）。血中β-ヒドロキシ酪酸上昇。"
        "電解質で低K⁺・低Na⁺・低Pを確認。CBC/生化学で脱水、腎前性高窒素血症を評価。"
        "膵炎・UTI・クッシング等の誘因を精査（cPLI、尿培養、ACTH刺激試験）。緊急治療が必要。"
    )
}

ENRICHMENTS["dog_hyperadrenocorticism_-_iatrogenic"] = {
    "diagnosis_ja": (
        "病歴聴取でステロイド長期投与歴（プレドニゾロン等）を確認。クッシング様症状（PU/PD、腹部膨満、皮膚菲薄化）。"
        "ACTH刺激試験でコルチゾール反応低値（副腎萎縮を反映）。低用量DEX試験では抑制される。"
        "血液検査でALP上昇（ステロイド誘導性）、ストレス白血球像、高血糖。"
        "腹部超音波で両側副腎の萎縮を確認。薬剤漸減中止が治療。急な中止で副腎クリーゼのリスク。"
    )
}

ENRICHMENTS["dog_canine_atopic_dermatitis"] = {
    "diagnosis_ja": (
        "Favrotの診断基準（8項目中5項目以上で感度85%）に基づく臨床診断。初発3歳以下、室内飼育。"
        "皮内テスト（IDT）またはアレルゲン特異的IgE血清検査で原因アレルゲンを同定。"
        "皮膚掻爬検査で疥癬・毛包虫を除外。細菌/真菌培養で二次感染を評価。"
        "食物アレルギーとの鑑別に8週間の除去食試験。好発部位：顔面、耳、腋窩、指間、腹部。"
    )
}

ENRICHMENTS["dog_zinc-responsive_dermatosis_-_syndrome_i"] = {
    "diagnosis_ja": (
        "皮膚生検で著明な表皮の錯角化（parakeratosis）を確認。特に眼周囲・口周囲・耳介・肉球。"
        "血清亜鉛濃度低値（<0.7 μg/mL）。血液検査でCBC、肝・腎機能は概ね正常。"
        "病理組織学的に表在性化膿性壊死性皮膚炎パターン。真菌培養で皮膚糸状菌を除外。"
        "シベリアン・ハスキー、アラスカン・マラミュートに好発（Syndrome I=遺伝的亜鉛吸収障害）。亜鉛補充で改善。"
    )
}

ENRICHMENTS["dog_dermatomyositis"] = {
    "diagnosis_ja": (
        "皮膚生検で表皮基底層の液状変性（interface dermatitis）と真皮筋層の炎症性ミオパチーを確認。"
        "EMG（筋電図）で異常自発電位を検出。CK値は正常～軽度上昇。"
        "臨床症状：顔面（眼周囲・口周囲・耳介）の脱毛・痂皮・紅斑と咀嚼筋萎縮。"
        "シェットランド・シープドッグ、コリーに好発。DMS遺伝子検査（PAN2遺伝子座）で感受性評価。"
    )
}

ENRICHMENTS["dog_canine_pattern_baldness"] = {
    "diagnosis_ja": (
        "身体検査で対称性の非炎症性脱毛を確認。好発部位：耳介（ダックスフンド）、腹側頸部・胸部・大腿部。"
        "皮膚生検で毛包のミニチュア化（miniaturization）を確認。炎症所見は乏しい。"
        "甲状腺機能検査（T4、fT4、TSH）で甲状腺機能低下症を除外。"
        "毛包の休止期率増加。犬種・好発部位のパターンで臨床診断。進行性だが全身状態は良好。"
    )
}

ENRICHMENTS["dog_cutaneous_vasculitis"] = {
    "diagnosis_ja": (
        "皮膚生検で血管壁の好中球浸潤、フィブリノイド壊死、核塵を確認（白血球破砕性血管炎）。"
        "臨床症状：紫斑、点状出血、潰瘍、壊死。耳介辺縁、肉球、尾端に好発。"
        "CBC/生化学で全身性疾患を評価。ANA、RF等の自己抗体検査。尿検査でタンパク尿（腎血管炎）。"
        "薬剤性、感染性、免疫介在性の原因を鑑別。寒冷凝集素症、SLE、IMHA等の基礎疾患を精査。"
    )
}

ENRICHMENTS["dog_nasal_hyperkeratosis"] = {
    "diagnosis_ja": (
        "身体検査で鼻鏡表面の角質増殖・乾燥・亀裂を確認。肉球の角化亢進の合併を評価。"
        "皮膚生検で著明な正角化症（orthokeratotic hyperkeratosis）を確認。"
        "CDV抗体検査/PCRでジステンパー後遺症を除外。甲状腺機能検査で内分泌性を除外。"
        "落葉状天疱瘡の除外に直接免疫蛍光法。亜鉛欠乏症の鑑別に血清亜鉛測定。特発性は犬種素因あり。"
    )
}

ENRICHMENTS["dog_calcinosis_cutis"] = {
    "diagnosis_ja": (
        "X線/超音波で皮膚・皮下組織の石灰化沈着を確認。皮膚生検で真皮内のカルシウム塩結晶沈着。"
        "von Kossa染色で石灰沈着を確認。ACTH刺激試験/LDDST/UCCRでクッシング症候群を精査（最多原因）。"
        "血液検査でCa、P、ALP、BUN/Cre、コルチゾールを評価。ステロイド投与歴の確認。"
        "二次感染の有無を細菌培養。医原性/内因性クッシング、慢性腎不全、特発性を鑑別。"
    )
}

ENRICHMENTS["dog_vitiligo"] = {
    "diagnosis_ja": (
        "身体検査で鼻鏡、口唇、眼瞼、肉球等の色素脱失（白斑化）を確認。進行性の脱色素。"
        "皮膚生検でメラノサイトの消失・減少を確認。炎症所見は乏しい（非炎症性色素脱失）。"
        "DLE（円板状エリテマトーデス）との鑑別に免疫組織化学。真菌培養で白癬を除外。"
        "ロットワイラー、ジャーマン・シェパード、ベルジアン・タービュレンに好発。美容的問題が主で全身状態は良好。"
    )
}

ENRICHMENTS["dog_iris_atrophy"] = {
    "diagnosis_ja": (
        "細隙灯顕微鏡検査で虹彩ストロマの菲薄化・透光性増加、瞳孔縁の不整を確認。"
        "散瞳反応の異常（不完全散瞳、dyscoria）。眼圧測定で緑内障の合併を除外。"
        "眼底検査で網膜病変の有無を評価。前眼房の炎症所見（ぶどう膜炎）の除外。"
        "老齢犬に生理的に発生（senile iris atrophy）。羞明の訴えがあれば対症療法。"
    )
}

ENRICHMENTS["dog_anterior_lens_luxation"] = {
    "diagnosis_ja": (
        "細隙灯顕微鏡検査で水晶体の前房内脱臼を確認。水晶体が瞳孔前方に移動。"
        "眼圧測定で続発性緑内障を評価（IOP>25 mmHg）。隅角鏡検査で隅角閉塞を確認。"
        "超音波検査で硝子体・網膜の状態を評価（網膜剥離の合併）。対側眼のチン小帯脆弱を評価。"
        "ジャック・ラッセル・テリア、ミニチュア・ブル・テリア等にADAMTS17遺伝子変異。緊急手術適応。"
    )
}

ENRICHMENTS["dog_eyelid_mass_meibomian_gland_adenoma"] = {
    "diagnosis_ja": (
        "眼科検査で眼瞼縁の結節性腫瘤を確認。多くは白～黄色の有茎性腫瘤。"
        "FNA（細針吸引）で脂腺由来の細胞を確認。悪性（脂腺癌）との鑑別に病理組織検査。"
        "細隙灯検査で角膜への機械的刺激（潰瘍）を評価。フルオレセイン染色で角膜びらんを確認。"
        "老齢犬に多い良性腫瘍。腫瘤が大きく角膜に接触する場合はV字切除術。"
    )
}

ENRICHMENTS["dog_optic_neuritis"] = {
    "diagnosis_ja": (
        "眼底検査で視神経乳頭の腫脹・充血、乳頭周囲出血を確認。PLR（対光反射）減弱～消失。"
        "威嚇瞬き反応陰性。MRIで視神経のT2高信号・造影増強を確認。"
        "CSF検査で単核球増多を評価。CDV PCR、トキソプラズマ/ネオスポラ抗体価、ANA等で原因精査。"
        "ERG（網膜電図）で網膜機能は保たれていることを確認（SARDS との鑑別に重要）。"
    )
}

ENRICHMENTS["dog_hyphema"] = {
    "diagnosis_ja": (
        "細隙灯顕微鏡検査で前房内の出血を確認。重症度をグレーディング（I: <1/3、II: 1/3-1/2、III: >1/2、IV: 全量）。"
        "眼圧測定で続発性緑内障を除外。超音波検査で眼内腫瘍・硝子体出血・網膜剥離を評価。"
        "CBC/凝固検査（PT、APTT、血小板数）で出血素因を評価。血圧測定で全身性高血圧を除外。"
        "原因：外傷、凝固障害、高血圧、眼内腫瘍、ぶどう膜炎、網膜剥離。原因治療と安静。"
    )
}

ENRICHMENTS["dog_canine_chronic_ulcerative_stomatitis_ccus"] = {
    "diagnosis_ja": (
        "口腔内検査で歯肉・頬粘膜・舌の慢性潰瘍を確認。特に歯牙接触部位（kissing lesions）。"
        "全顎歯科X線で歯周病・歯根吸収の程度を評価。生検で組織球性/リンパ球性炎症を確認。"
        "免疫組織化学で自己免疫性を評価。培養で感染性を除外。血液検査で全身性疾患を精査。"
        "CCUS特異的：歯垢抗原に対する過剰免疫反応。全臼歯抜歯が根治療法。80%が著明改善。"
    )
}

ENRICHMENTS["dog_mandibular_fracture"] = {
    "diagnosis_ja": (
        "口腔内検査で下顎の変形・不正咬合・歯肉出血を確認。触診で骨折部位のクレピタス・疼痛。"
        "頭部X線（DV/lateral oblique）で骨折線・転位を確認。歯科X線で歯根部の骨折を評価。"
        "CT三次元再構成で複雑骨折の術前計画。CBC/生化学で全身状態と麻酔リスクを評価。"
        "好発部位：下顎結合部、犬歯部、下顎角部。外傷歴、歯周病（病的骨折）の確認。"
    )
}

ENRICHMENTS["dog_oral_papillomatosis"] = {
    "diagnosis_ja": (
        "口腔内検査で特徴的な乳頭状（カリフラワー様）の白～ピンク色腫瘤を確認。多発性。"
        "生検/組織検査で扁平上皮の乳頭状増殖とコイロサイト（koilocyte）を確認。"
        "PCRでイヌパピローマウイルス（CPV）を同定。免疫組織化学で確認。"
        "若齢犬（<2歳）に好発。通常6-12週で自然退縮（免疫獲得）。広範な場合はクリオサージェリー。"
    )
}

ENRICHMENTS["dog_enamel_hypoplasia"] = {
    "diagnosis_ja": (
        "口腔検査で歯表面のエナメル質欠損・粗造・変色（黄褐色）を確認。歯冠全周に及ぶ場合あり。"
        "歯科X線でエナメル質の菲薄化・欠如を確認。象牙質露出の有無を評価。"
        "CDV既往歴（ジステンパー歯）の確認。発熱性疾患・栄養障害の乳歯～永久歯移行期の病歴。"
        "プローブ検査でう蝕・歯髄露出の有無。シーラント/修復が治療。予防的抜歯は重症例のみ。"
    )
}

ENRICHMENTS["dog_dentigerous_cyst"] = {
    "diagnosis_ja": (
        "口腔X線/歯科X線で未萌出歯に関連した嚢胞性骨透亮像を確認。嚢胞壁が歯冠に付着。"
        "CT三次元再構成で嚢胞の範囲・隣接歯への影響を評価。下顎骨の菲薄化リスクを評価。"
        "FNA（穿刺吸引）で嚢胞液を確認。病理組織検査で非角化重層扁平上皮の嚢胞壁を確認。"
        "短頭種に好発（PM1欠損に関連）。嚢胞摘出＋原因歯抜歯が根治療法。"
    )
}

ENRICHMENTS["dog_thyroid_adenoma_benign"] = {
    "diagnosis_ja": (
        "頸部触診で甲状腺領域の腫瘤を確認。多くは可動性良好。超音波で嚢胞性/充実性を評価。"
        "FNA（細針吸引）で良性甲状腺細胞を確認。悪性（甲状腺癌）との鑑別が重要。"
        "血清T4・fT4・TSH測定で甲状腺機能を評価（多くは機能性腫瘤ではない）。"
        "頸部CT/MRIで腫瘤の範囲・血管浸潤・リンパ節転移を評価。99mTcシンチグラフィで機能性評価。"
    )
}

ENRICHMENTS["dog_hepatic_lymphoma"] = {
    "diagnosis_ja": (
        "腹部超音波で肝実質のびまん性低エコー化（diffuse hypoechoic pattern）または多発性結節を確認。"
        "超音波ガイド下FNA/Tru-cutで細胞診・病理診断。フローサイトメトリーでT/B細胞型を分類。"
        "CBC/生化学でALP・ALT・GGT上昇、低アルブミン血症。全身ステージングにCT/X線で胸部・脾臓・リンパ節を評価。"
        "骨髄穿刺でstage V（骨髄浸潤）を評価。cPLI/fPLIで膵炎合併を除外。LDH上昇は腫瘍量を反映。"
    )
}

ENRICHMENTS["dog_anal_gland_carcinoma"] = {
    "diagnosis_ja": (
        "直腸触診で肛門嚢の硬い腫瘤を確認。FNA（細針吸引）で腺癌細胞を検出。"
        "腹部超音波/CTで腸骨下リンパ節の腫大（転移）を評価。X線で肺転移を確認。"
        "血液検査で高カルシウム血症（偽性副甲状腺機能亢進症/PTHrP産生：25-50%で発生）。"
        "イオン化Ca上昇+PTH低値+PTHrP上昇で確定。ステージングにCT全身スキャン。外科切除+化学療法。"
    )
}

ENRICHMENTS["dog_chondrosarcoma"] = {
    "diagnosis_ja": (
        "X線で骨溶解と骨膜反応を伴う骨腫瘤を確認。扁平骨（肋骨、鼻腔、骨盤）に好発。"
        "CT/MRIで腫瘍の範囲・軟部組織浸潤を三次元評価。CT肺転移スクリーニング。"
        "生検で軟骨基質内の異型軟骨細胞を確認。組織学的グレーディング（I-III）で予後判定。"
        "ALP上昇は予後不良因子。FNA単独では診断困難（組織生検が必要）。外科的広範切除が第一選択。"
    )
}

ENRICHMENTS["dog_pulmonary_adenocarcinoma"] = {
    "diagnosis_ja": (
        "胸部X線で孤立性肺腫瘤（多くは右肺後葉）を確認。CT三次元再構成で腫瘤サイズ・位置・リンパ節を評価。"
        "超音波ガイド下FNA/経胸壁生検で腺癌細胞を確認。気管支洗浄液（BAL）の細胞診。"
        "CBC/生化学は概ね正常。原発性と転移性の鑑別に全身CT/腹部超音波。"
        "肥大性骨症（HO）の合併を四肢X線で確認。TNMステージングで予後評価。肺葉切除が根治療法。"
    )
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
