#!/usr/bin/env python3
"""Cat diagnosis_ja enrichment — batch 10 (entries 0-49 of remaining)."""

import json
import os
import time

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diseases_all_species.json")

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["cat_feline_peritonitis_septic"] = {
    "diagnosis_ja": "急性腹痛・発熱・嘔吐・ショック徴候を呈する。腹部触診で腹壁緊張・疼痛を確認。腹部超音波で腹水を検出し、腹腔穿刺で混濁腹水を採取。腹水分析で好中球優位（変性好中球・細菌貪食像）、蛋白>2.5g/dL、グルコース<50mg/dL。腹水の細菌培養・感受性試験を実施。CBC白血球増多（左方移動）、CRP著明上昇。血液培養で菌血症を評価。消化管穿孔、膵壊死、術後感染を鑑別。"
}
ENRICHMENTS["cat_feline_laryngitis"] = {
    "diagnosis_ja": "嗄声・発声変化・咳嗽・吸気性ストライダーを認める。口腔内検査で咽頭発赤を確認。喉頭鏡検査で喉頭粘膜の発赤・腫脹・浮腫を直接観察。CBC/CRP上昇は感染性を示唆。FHV-1/FCV PCR検査でウイルス性原因を評価。頸部X線で喉頭領域の軟部組織腫脹を確認。慢性例では喉頭生検で腫瘍性変化を除外。喘息、気管虚脱、喉頭麻痺、異物との鑑別が必要。"
}
ENRICHMENTS["cat_feline_glomerulonephritis"] = {
    "diagnosis_ja": "蛋白尿（UPC>2.0）を主徴とし、浮腫・腹水・体重減少を伴う。血液化学でBUN/Cre上昇、低アルブミン血症、高コレステロール血症（ネフローゼ症候群）を認める。尿検査で蛋白尿と円柱を確認。血圧測定で全身性高血圧を評価。FeLV/FIV検査、FIP抗体価で感染性原因を検索。抗核抗体（ANA）でSLEを除外。確定診断は腎生検（光顕・電顕・蛍光抗体法）。アミロイドーシス、CKD、腎リンパ腫との鑑別が必要。"
}
ENRICHMENTS["cat_feline_nephrogenic_diabetes_insipidus"] = {
    "diagnosis_ja": "著明な多飲多尿（尿量>50mL/kg/日）を呈する。尿比重持続的低値（<1.015）。水制限試験で尿濃縮不良を確認。外因性バソプレシン（DDAVP）投与試験で尿濃縮が改善しない（中枢性DIとの鑑別）。血清Na/浸透圧は正常〜軽度上昇。BUN/Cre測定でCKDを除外。血清Ca測定で高Ca血症を除外。T4測定で甲状腺機能亢進症を除外。薬剤歴（リチウム等）の確認。腎盂腎炎、子宮蓄膿症との鑑別も必要。"
}
ENRICHMENTS["cat_feline_interstitial_nephritis"] = {
    "diagnosis_ja": "慢性腎臓病の臨床徴候（多飲多尿・体重減少・食欲不振・嘔吐）を呈する。血液化学でBUN/Cre上昇、P上昇、K異常を認める。尿検査で等張尿（比重1.008-1.012）、蛋白尿を確認。腹部超音波で腎臓のサイズ縮小・高エコー化・辺縁不整を評価。SDMA早期上昇はGFR低下の敏感な指標。血圧測定で高血圧を評価。確定診断は腎生検（間質のリンパ球・形質細胞浸潤と線維化）。CKD、腎リンパ腫、アミロイドーシスとの鑑別が必要。"
}
ENRICHMENTS["cat_feline_dermatophilosis"] = {
    "diagnosis_ja": "痂皮性〜膿疱性皮膚病変を認める。湿潤環境・免疫抑制が素因。痂皮の剥離面の印象塗抹でDermatophilus congolensisの特徴的な「レールロード」様配列の球菌を確認（グラム染色陽性）。細菌培養で確定（CO2環境下でβ溶血コロニー）。皮膚生検で表皮の膿疱形成と痂皮内の特徴的な菌体配列を認める。皮膚糸状菌症、天疱瘡、細菌性膿皮症との鑑別が必要。FIV/FeLV検査で免疫状態を評価。"
}
ENRICHMENTS["cat_feline_malassezia_dermatitis"] = {
    "diagnosis_ja": "脂漏性皮膚炎・搔痒・耳の分泌物を認める。好発部位は顎下・腹側頸部・鼠径部・趾間。皮膚印象塗抹（セロハンテープ法）でマラセチア酵母（ピーナッツ型）を確認（>1個/HPFで有意）。ウッド灯検査は陰性（マラセチアは蛍光しない）。基礎疾患（アレルギー性皮膚炎、FIV、内分泌疾患）の検索が重要。皮膚生検で表皮過形成・表層酵母菌体を確認。皮膚糸状菌症、細菌性膿皮症、好酸球性肉芽腫との鑑別が必要。"
}
ENRICHMENTS["cat_feline_cutaneous_lymphoma"] = {
    "diagnosis_ja": "孤立性〜多発性の皮膚結節・プラーク・紅斑性病変を認める。搔痒を伴うことがある。FNA細胞診で均一な大型リンパ球（核分裂像多数）を確認。皮膚生検で真皮〜皮下の腫瘍性リンパ球浸潤を評価（上皮向性の有無でmycosis fungoides型を鑑別）。免疫組織化学（CD3/CD20/CD79a）でT細胞性vsB細胞性を判定。CBC/血液化学で全身性リンパ腫を除外。骨髄検査・腹部超音波でステージングを実施。好酸球性肉芽腫、肥満細胞腫、扁平上皮癌との鑑別が必要。"
}
ENRICHMENTS["cat_feline_fibrosarcoma_non-injection_site"] = {
    "diagnosis_ja": "皮下〜筋肉内の硬い結節性腫瘤を触知（注射部位以外に発生）。FNA細胞診で紡錘形細胞を認める（確定は困難な場合が多い）。切除生検による組織病理で線維芽細胞の束状配列・異型性を確認。胸部X線で肺転移を検索。CT/MRIで腫瘤の浸潤範囲を術前評価。FeLV検査（若齢猫の多中心性線維肉腫はFeLV関連）。注射部位肉腫（FISS）との鑑別は発生部位と組織学的特徴による。末梢神経鞘腫、平滑筋肉腫との鑑別が必要。"
}
ENRICHMENTS["cat_feline_thyroid_carcinoma"] = {
    "diagnosis_ja": "頸部腫瘤の触知、甲状腺機能亢進症状（体重減少・多食・頻脈・嘔吐）を呈する。血清T4/fT4上昇で甲状腺機能亢進を確認。頸部超音波で甲状腺腫瘤のサイズ・エコー輝度・血管分布を評価。99mTc甲状腺シンチグラフィで機能性腫瘍の範囲と異所性組織を同定。FNA細胞診で濾胞細胞の異型性を評価（良悪性鑑別は細胞診では困難）。胸部X線で肺転移を検索。組織病理で濾胞性vs充実性パターンを確定。甲状腺腺腫との鑑別が重要。"
}
ENRICHMENTS["cat_feline_adrenal_tumor"] = {
    "diagnosis_ja": "多飲多尿・多食・腹部膨満・脱毛（クッシング様）、または高血圧・低K血症（アルドステロン産生腫瘍）を呈する。腹部超音波で副腎腫瘤（>1cm）を確認し、対側副腎の萎縮を評価。ACTH刺激試験・低用量デキサメタゾン抑制試験でコルチゾール過剰を確認。血漿アルドステロン/レニン比上昇は原発性高アルドステロン症を示唆。CT/MRIで腫瘤の血管浸潤・転移を評価。褐色細胞腫、副腎皮質癌との鑑別が必要。"
}
ENRICHMENTS["cat_feline_pancreatic_adenocarcinoma"] = {
    "diagnosis_ja": "体重減少・食欲不振・嘔吐・黄疸（胆管閉塞時）を呈する。腹部超音波で膵臓領域の低エコー腫瘤を確認。膵管拡張・胆管拡張を伴うことがある。CT造影検査で腫瘤の血管浸潤・肝転移を評価。FNA細胞診で腺癌細胞を確認（超音波ガイド下）。血液化学で肝酵素上昇・T-Bil上昇・血糖異常を認める。fPLI上昇は膵炎の併発を示唆。リンパ腫、膵臓炎、胆管癌との鑑別が必要。"
}
ENRICHMENTS["cat_feline_pheochromocytoma"] = {
    "diagnosis_ja": "発作性高血圧・頻脈・パンティング・不穏・虚脱を呈する。血圧測定で持続性〜発作性高血圧を確認。腹部超音波で副腎腫瘤を検出。尿中カテコラミン/メタネフリン上昇で確定的。CT/MRIで腫瘤の範囲・大静脈浸潤を評価。対側副腎・傍大動脈体のパラガングリオーマを検索。術前のα遮断薬投与が必須（術中カテコラミンクリーゼ予防）。副腎皮質腫瘍、甲状腺機能亢進症、心疾患との鑑別が必要。"
}
ENRICHMENTS["cat_feline_orbital_tumor"] = {
    "diagnosis_ja": "眼球突出（眼球偏位）・結膜充血・瞬膜突出・視力障害を認める。眼窩触診で硬い腫瘤を触知することがある。CT/MRIで眼窩内腫瘤の範囲・骨浸潤・頭蓋内進展を評価。超音波で眼球後方の腫瘤を確認。FNA細胞診（CT/超音波ガイド下）で腫瘍細胞型を同定。眼圧測定で続発性緑内障を評価。眼底検査で網膜剥離を確認。扁平上皮癌、リンパ腫、髄膜腫が好発。眼窩膿瘍、眼窩蜂窩織炎との鑑別が必要。"
}
ENRICHMENTS["cat_feline_ceruminous_gland_adenoma"] = {
    "diagnosis_ja": "外耳道内の有茎性〜広基性腫瘤として発見。通常良性で緩徐に増大。耳鏡検査で外耳道内の暗色結節を確認。FNA細胞診で分泌顆粒を含む均一な腺上皮細胞を認める。CT/MRIは大型腫瘤で外耳道閉塞が疑われる場合に実施。確定診断は切除生検による組織病理（良性の管状〜嚢胞状構造、細胞異型性なし）。耳垢腺腺癌、炎症性ポリープ、扁平上皮癌との鑑別が重要。外耳炎の二次感染を併発することが多い。"
}
ENRICHMENTS["cat_feline_chronic_colitis"] = {
    "diagnosis_ja": "慢性下痢（粘液便・血便・しぶり）・体重減少を呈する。糞便検査で寄生虫・C. difficile毒素・トリトリコモナスPCRを除外。CBC/血液化学で炎症マーカーと栄養状態を評価。T4測定で甲状腺機能亢進症を除外。腹部超音波で結腸壁肥厚・リンパ節腫大を確認。大腸内視鏡検査と粘膜生検で組織病理学的分類（リンパ球形質細胞性、好酸球性）を確定。食物反応性を除外するための除去食試験。リンパ腫、腺癌との鑑別が必要。"
}
ENRICHMENTS["cat_feline_chronic_bronchitis"] = {
    "diagnosis_ja": "2ヶ月以上持続する咳嗽・喘鳴を呈する。胸部X線でbronchial patternの増強（ドーナツ・レールロードサイン）を確認。気管支肺胞洗浄（BAL）で好中球優位（感染性）〜好酸球優位（アレルギー性）の細胞診を評価。BAL液の細菌培養・感受性試験。糞便検査でAelurostrongylus（猫肺虫）を除外。SpO2/血液ガス分析で酸素化状態を評価。猫喘息、肺虫感染、心疾患（胸部X線でvascular pattern）との鑑別が必要。"
}
ENRICHMENTS["cat_feline_pulmonary_thromboembolism"] = {
    "diagnosis_ja": "急性呼吸困難・頻呼吸・チアノーゼ・虚脱を呈する。基礎疾患（HCM、腫瘍、蛋白漏出性疾患）の確認が重要。胸部X線で限局性血管陰影減少・肺野透過性亢進を認める。CT血管造影（CTA）で肺動脈内の充盈欠損を確認（確定的）。心エコーで右心負荷所見（右室拡大、三尖弁逆流、肺動脈圧上昇）を評価。D-dimer上昇は示唆的。血液ガス分析でPaO2低下・A-aDO2開大。DIC合併時はPT/APTT延長・血小板減少。"
}
ENRICHMENTS["cat_feline_pneumothorax"] = {
    "diagnosis_ja": "急性呼吸困難・浅速呼吸・チアノーゼを呈する。聴診で患側の呼吸音減弱〜消失。胸部X線で肺葉の虚脱と胸腔内気体を確認（立位/側臥位で撮影）。緊張性気胸では縦隔偏位を認め緊急脱気が必要。胸腔穿刺で気体を吸引し診断と治療を兼ねる。外傷歴の確認（肋骨骨折・胸壁創）。自然気胸では肺嚢胞/ブラの破裂を疑いCT検査。血胸（PCV確認）、横隔膜ヘルニア、胸水との鑑別が必要。"
}
ENRICHMENTS["cat_feline_pulmonary_fibrosis"] = {
    "diagnosis_ja": "進行性の呼吸困難・運動不耐性・乾性咳嗽を呈する。高齢猫に好発。胸部X線で瀰漫性間質パターン（網状〜蜂巣肺）を確認。高分解能CT（HRCT）で間質性変化の分布・パターンを詳細評価。BAL液分析で好中球・マクロファージ優位を確認。SpO2低下（<92%）は予後不良を示唆。心エコーで肺高血圧による右心負荷を評価。確定診断は肺生検だが侵襲性が高い。喘息、肺腫瘍、心不全との鑑別が必要。"
}
ENRICHMENTS["cat_feline_allergic_bronchopulmonary_disease"] = {
    "diagnosis_ja": "慢性咳嗽・喘鳴・呼吸困難を呈する。好酸球増多を認めることが多い。胸部X線でbronchial pattern増強と気管支拡張を確認。BAL液で好酸球優位（>17%）を確認。BAL液の真菌培養でAspergillus等を検索。血清IgE上昇は示唆的。糞便検査で肺虫を除外。アレルゲン特異的IgE検査（環境アレルゲンパネル）。ステロイド反応性で診断的治療。猫喘息（feline asthma）、肺虫感染、肺腫瘍との鑑別が必要。"
}
ENRICHMENTS["cat_feline_nasal_polyp"] = {
    "diagnosis_ja": "慢性鼻汁（片側性〜両側性）・くしゃみ・いびき様呼吸を呈する。若齢猫に好発。口腔検査で軟口蓋背側からポリープが確認できることがある。耳鏡検査で鼓膜越しに鼓室胞内のポリープを評価。CT/MRIで鼻咽頭〜鼓室胞のポリープ範囲を確認。確定診断は切除生検（有茎性の炎症性粘膜被覆ポリープ）。鼻腔腫瘍、鼻腔真菌症、慢性鼻炎との鑑別が必要。外耳炎・中耳炎の併発を確認。"
}
ENRICHMENTS["cat_feline_sinonasal_aspergillosis"] = {
    "diagnosis_ja": "慢性鼻汁（膿性〜出血性）・くしゃみ・顔面変形を呈する。短頭種に好発。CT検査で副鼻腔内の軟部組織陰影と骨溶解を確認。鼻腔鏡検査で真菌プラーク（白色〜黄色）を直接観察。鼻汁/組織の真菌培養でAspergillus fumigatusを同定。組織生検で菌糸の浸潤を確認（GMS/PAS染色）。Aspergillus抗体検査は補助的。クリプトコッカス症（抗原検査）、鼻腔腫瘍（リンパ腫、SCC）との鑑別が必要。"
}
ENRICHMENTS["cat_feline_diabetes_insipidus_central"] = {
    "diagnosis_ja": "著明な多飲多尿（尿量>50mL/kg/日）、尿比重<1.010を呈する。水制限試験で尿濃縮不良を確認（危険を伴うため入院管理下で実施）。DDAVP（デスモプレシン）投与試験で尿比重が上昇すれば中枢性DIを確定。MRI/CTで下垂体〜視床下部病変（腫瘍・炎症・外傷後）を検索。血清Na/浸透圧は正常〜軽度上昇。CKD（BUN/Cre）、甲状腺機能亢進症（T4）、糖尿病（血糖）、腎性DIとの鑑別が必要。"
}
ENRICHMENTS["cat_feline_hyperparathyroidism_primary"] = {
    "diagnosis_ja": "高Ca血症（>12mg/dL）に伴う多飲多尿・食欲不振・嘔吐・便秘を呈する。血清iPTH上昇（高Ca血症の存在下で不適切に高値）で確定。血清P低下〜正常。腎機能検査（BUN/Cre）でCKD合併を評価。頸部超音波で副甲状腺腫瘤を検索。尿Ca排泄量測定。X線で骨密度低下・病的骨折を確認。悪性腫瘍随伴高Ca血症（PTHrP測定）、ビタミンD中毒、CKD関連二次性副甲状腺機能亢進症との鑑別が必要。"
}
ENRICHMENTS["cat_feline_hypoparathyroidism"] = {
    "diagnosis_ja": "低Ca血症（<8mg/dL）による筋硬直・振戦・テタニー・痙攣を呈する。血清Ca低下、P上昇、iPTH低値〜測定感度以下で確定。Mg測定（低Mg血症はPTH分泌を抑制）。心電図でQT延長を確認。甲状腺手術後の医原性が最多。特発性は免疫介在性の可能性。イオン化Ca測定がより正確。総Caはアルブミン補正が必要。CKD（二次性副甲状腺機能亢進症）、ビタミンD欠乏、低アルブミン血症（偽性低Ca）との鑑別が必要。"
}
ENRICHMENTS["cat_feline_pituitary_dwarfism"] = {
    "diagnosis_ja": "生後3-4ヶ月齢以降の成長停止、同腹仔と比較した体格の小ささを認める。被毛は柔らかい子猫様被毛が残存。血清IGF-1低値、GH刺激試験（クロニジン/GHRH投与後のGH反応欠如）で確定。甲状腺機能検査（T4/TSH）で甲状腺機能低下症を併発評価。MRIで下垂体嚢胞・低形成を確認。骨端線の閉鎖遅延をX線で評価。栄養不良、門脈シャント、先天性心疾患など他の成長障害との鑑別が必要。"
}
ENRICHMENTS["cat_feline_hypermagnesemia"] = {
    "diagnosis_ja": "徐脈・筋弛緩・低血圧・呼吸抑制を呈する。血清Mg>3.0mg/dLで診断。腎不全（BUN/Cre上昇）が最も多い原因。Mg含有制酸薬・下剤の過剰投与歴を確認。心電図でPR延長・QRS幅増大・T波増高を認める。重度（>6mg/dL）では心停止リスク。血清Ca/K/Naの同時測定（電解質異常の併発評価）。CKD、副腎不全（ACTH刺激試験）、甲状腺機能低下症との鑑別。緊急時はCa静注が拮抗薬として作用する。"
}
ENRICHMENTS["cat_feline_hyperphosphatemia"] = {
    "diagnosis_ja": "高P血症（>6.5mg/dL）は通常CKDに伴う。軟部組織石灰化（腎石灰化、血管石灰化）・二次性副甲状腺機能亢進症の進行を引き起こす。血液化学でBUN/Cre上昇、Ca低下、iPTH上昇を確認。尿検査で等張尿。腹部超音波で腎臓のサイズ・エコー輝度を評価。IRIS分類に基づくCKDステージングを実施。FGF23測定は早期P代謝異常の指標。急性腎障害、腫瘍崩壊症候群、ビタミンD中毒との鑑別が必要。"
}
ENRICHMENTS["cat_feline_hepatic_abscess"] = {
    "diagnosis_ja": "発熱・食欲不振・嘔吐・腹部疼痛を呈する。血液化学でALT/AST上昇、ALP/GGT上昇、T-Bil上昇を認める。CBC白血球増多（好中球左方移動）、CRP著明上昇。腹部超音波で肝実質内の低エコー〜無エコー腫瘤（厚い被膜・内部デブリ）を確認。超音波ガイド下穿刺で膿汁を採取し細菌培養・感受性試験を実施。嫌気性菌を含む培養が重要。肝腫瘍（嚢胞性変化）、肝嚢胞、胆嚢膿瘍との鑑別が必要。"
}
ENRICHMENTS["cat_feline_bile_duct_obstruction"] = {
    "diagnosis_ja": "進行性黄疸（皮膚・粘膜・強膜の黄染）、食欲不振・嘔吐・灰白色便を呈する。血液化学でT-Bil著明上昇（>5mg/dL）、ALP/GGT上昇（ALT/ASTより顕著）、胆汁酸上昇を認める。腹部超音波で胆管拡張（CBD>4mm）、胆嚢拡張、閉塞部位を確認。膵頭部腫瘤・胆管腫瘍・胆石の有無を評価。CT造影で閉塞の正確な部位と原因を同定。凝固系検査でビタミンK依存因子の低下を確認。膵炎、胆管炎、肝リピドーシスとの鑑別が必要。"
}
ENRICHMENTS["cat_feline_gastric_hairball_obstruction"] = {
    "diagnosis_ja": "慢性嘔吐・食欲不振・体重減少を呈する。腹部触診で胃内の硬い腫瘤を触知することがある。腹部X線で胃内の軟部組織様腫瘤陰影を確認（放射線不透過性は乏しい場合がある）。バリウム造影で胃内充盈欠損を評価。腹部超音波で胃内の高エコー構造物と音響陰影を確認。内視鏡検査で直接観察し、小型の毛球は内視鏡的除去も可能。血液化学で脱水・電解質異常を評価。胃腫瘍、異物、幽門狭窄症との鑑別が必要。"
}
ENRICHMENTS["cat_feline_intussusception"] = {
    "diagnosis_ja": "急性嘔吐・血性下痢・腹部疼痛・食欲廃絶を呈する。腹部触診で管状のソーセージ様腫瘤を触知。腹部超音波で「ターゲットサイン」（同心円状の多重層構造）を確認（感度>90%）。腹部X線で腸管の拡張・ガス貯留と軟部組織腫瘤を認める。CBC/血液化学で脱水・電解質異常・炎症マーカーを評価。若齢猫では線状異物・寄生虫感染が誘因として多い。腸管腫瘍（リンパ腫）、腸管異物、腸捻転との鑑別が必要。"
}
ENRICHMENTS["cat_feline_colonic_neoplasia"] = {
    "diagnosis_ja": "慢性下痢・血便・しぶり・体重減少を呈する。直腸指診で直腸〜結腸遠位の腫瘤を触知。腹部超音波で結腸壁の限局性肥厚・腫瘤を確認し、腸間膜リンパ節腫大を評価。大腸内視鏡検査で腫瘤を直接観察し、生検による組織病理学的診断を実施。FNA細胞診は補助的。CBC/血液化学で貧血・低蛋白を評価。胸部X線/腹部CTでステージングを実施。リンパ腫、腺癌、肥満細胞腫が好発。IBD、感染性大腸炎との鑑別が必要。"
}
ENRICHMENTS["cat_feline_perianal_fistula"] = {
    "diagnosis_ja": "肛門周囲の潰瘍性病変・排膿・疼痛・しぶりを認める。肛門周囲の視診で瘻管開口部を確認。直腸指診で瘻管の走行と深さを評価（鎮静下が望ましい）。瘻管からの分泌物の細菌培養。組織生検で肉芽腫性炎症を確認し、腫瘍性変化を除外（肛門嚢腺癌、扁平上皮癌）。CBC/血液化学で全身性炎症を評価。FIV/FeLV検査で免疫状態を確認。肛門嚢疾患、肛門嚢腫瘍、猫白血病関連病変との鑑別が必要。"
}
ENRICHMENTS["cat_feline_histoplasmosis"] = {
    "diagnosis_ja": "呼吸器症状（咳嗽、呼吸困難）、消化器症状（下痢、体重減少）、または汎発性（発熱、リンパ節腫大、肝脾腫）を呈する。胸部X線で瀰漫性間質〜結節性肺パターンを確認。FNA細胞診で細胞内の小型酵母菌体（2-4μm、偏心性核）を検出。骨髄穿刺でマクロファージ内のHistoplasma capsulatumを確認。尿中Histoplasma抗原検査が有用。組織生検でGMS/PAS染色陽性。CBC汎血球減少、肝酵素上昇を認める。結核、リンパ腫、FIPとの鑑別が必要。"
}
ENRICHMENTS["cat_feline_blastomycosis"] = {
    "diagnosis_ja": "呼吸器症状（咳嗽、呼吸困難）、皮膚病変（排膿性結節）、眼病変（ぶどう膜炎、網膜剥離）を呈する。胸部X線で結節性〜瀰漫性肺浸潤影を確認。FNA/圧挫細胞診で大型厚壁の酵母菌体（8-20μm、広基性出芽）を検出（特徴的）。組織生検でPAS/GMS染色陽性の酵母菌体を確認。尿中Blastomyces抗原検査が高感度。血清抗体検査は補助的。CBC炎症パターン、高Ca血症を伴うことがある。ヒストプラズマ症、クリプトコッカス症、肺腫瘍との鑑別が必要。"
}
ENRICHMENTS["cat_feline_coccidioidomycosis"] = {
    "diagnosis_ja": "慢性咳嗽・発熱・体重減少・跛行（骨病変）を呈する。米国南西部の渡航歴/居住歴が重要。胸部X線で肺門リンパ節腫大・肺結節を確認。骨X線で溶骨性病変を検索。FNA/組織生検で大型の球形体（spherule、20-80μm、内部に内生胞子）を検出。血清抗Coccidioides抗体検査（AGID/CF）が有用。CSF検査で播種性を評価。CBC好酸球増多、グロブリン上昇。結核、骨腫瘍、他の深在性真菌症との鑑別が必要。"
}
ENRICHMENTS["cat_feline_phaeohyphomycosis"] = {
    "diagnosis_ja": "皮下結節性腫瘤（特に鼻鏡・四肢）を認める。黒色〜暗褐色の分泌物を伴うことがある。FNA細胞診で褐色の分隔菌糸を確認。組織生検でフォンテーナ・マッソン染色陽性のメラニン含有菌糸を認める。真菌培養で暗色真菌（Alternaria、Cladophialophora、Exophiala等）を同定（培養に2-4週要する）。頭蓋内進展が疑われる場合MRI検査。免疫状態の評価（FIV/FeLV）。スポロトリコーシス、クリプトコッカス症、肉芽腫性炎症との鑑別が必要。"
}
ENRICHMENTS["cat_feline_pythiosis"] = {
    "diagnosis_ja": "消化管型（嘔吐、下痢、腹部腫瘤）または皮膚型（潰瘍性結節）を呈する。温暖湿潤な環境での水辺接触歴が重要。腹部超音波で腸管壁の著明な肥厚・腫瘤を確認。FNA/組織生検でGMS染色陽性の幅広い隔壁のない菌糸を確認。Pythium insidiosum特異的ELISA抗体検査が有用。培養では真菌培地に発育しない（卵菌類）。CBC好酸球増多。消化管リンパ腫、IBD、他の深在性真菌症との鑑別が必要。"
}
ENRICHMENTS["cat_feline_mycetoma"] = {
    "diagnosis_ja": "皮下の硬い結節性腫瘤で、瘻孔形成と排膿を認める。排膿液中の顆粒（菌塊）を肉眼で確認（色により真菌性vs放線菌性を推定）。組織生検で顆粒の構造を評価（Splendore-Hoeppli現象）。真菌培養で起因菌を同定。グラム染色・抗酸菌染色で放線菌性を鑑別。X線/CTで骨浸潤を評価。FIV/FeLV検査で免疫状態を確認。スポロトリコーシス、暗色真菌症、異物反応性肉芽腫との鑑別が必要。"
}
ENRICHMENTS["cat_feline_haemobartonellosis"] = {
    "diagnosis_ja": "急性発症の貧血（蒼白粘膜・頻脈・呼吸促迫）・発熱・脾腫を呈する。CBC再生性貧血（PCV急低下、網赤血球増加）。血液塗抹で赤血球表面のMycoplasma haemofelis小体を確認（感度は変動する）。PCR検査が確定診断のゴールドスタンダード（3種：M. haemofelis、Ca. M. haemominutum、Ca. M. turicensis）。直接クームス試験陽性のことがある（IMHA合併）。FeLV/FIV検査は必須（免疫抑制が素因）。IMHA、FeLV関連貧血との鑑別が必要。"
}
ENRICHMENTS["cat_feline_hemoplasmosis_candidatus_mycoplasma_turicensis"] = {
    "diagnosis_ja": "Ca. M. turicensisは3種のヘモプラズマ中最も病原性が低い。免疫抑制猫（FIV/FeLV陽性）で臨床的貧血を引き起こす。CBC軽度〜中等度の貧血。血液塗抹では菌体検出困難（菌量少ない）。確定診断はリアルタイムPCR（種特異的プライマー使用）。M. haemofelis、Ca. M. haemominutumとの混合感染を評価。FIV/FeLV検査は必須。直接クームス試験でIMHA合併を評価。他のヘモプラズマ種、IMHA、FeLV関連貧血との鑑別が必要。"
}
ENRICHMENTS["cat_feline_anaplasma_infection"] = {
    "diagnosis_ja": "発熱・食欲不振・関節痛・跛行を呈する。マダニ曝露歴を確認。CBC血小板減少、好中球減少を認める。血液塗抹で好中球内のAnaplasma phagocytophilum桑実胚様封入体（morulae）を検索（感度低い）。PCR検査で確定。血清抗体検査（IFA/ELISA）は急性期には陰性のことがある（ペア血清で4倍以上の上昇で確定）。肝酵素上昇を伴うことがある。エーリキア症、バベシア症、ヘモプラズマ症との鑑別が必要。"
}
ENRICHMENTS["cat_feline_ehrlichiosis"] = {
    "diagnosis_ja": "発熱・食欲不振・体重減少・リンパ節腫大を呈する。マダニ曝露歴を確認。CBC汎血球減少（急性期は血小板減少が先行）、高グロブリン血症。血液塗抹で単球内の封入体（morulae）を検索（感度低い）。PCR検査で確定（Ehrlichia canis）。血清抗体検査（IFA）はペア血清で評価。骨髄穿刺で形質細胞増生・骨髄球系低形成を確認。蛋白電気泳動でポリクローナルγグロブリン上昇。FIP、リンパ腫、多発性骨髄腫との鑑別が必要。"
}
ENRICHMENTS["cat_feline_babesiosis"] = {
    "diagnosis_ja": "貧血（蒼白粘膜・頻脈）・発熱・黄疸・脾腫を呈する。CBC再生性溶血性貧血。血液塗抹で赤血球内のBabesia felis小体（小型環状体）を検索。PCR検査で確定診断と種同定。直接クームス試験陽性のことがある。血液化学でT-Bil上昇、肝酵素上昇、BUN上昇を認める。尿検査でヘモグロビン尿。FIV/FeLV検査で免疫状態を確認。IMHA、ヘモプラズマ症、タマネギ中毒性溶血との鑑別が必要。"
}
ENRICHMENTS["cat_feline_leishmaniasis"] = {
    "diagnosis_ja": "皮膚病変（非搔痒性の結節・潰瘍・落屑性皮膚炎）、体重減少、リンパ節腫大、脾腫を呈する。地中海沿岸・南米等の流行地の滞在歴を確認。FNA細胞診でマクロファージ内のLeishmania amastigote（キネトプラスト付きの小体）を検出。PCR検査で確定・種同定。血清抗体検査（IFA/ELISA）。CBC非再生性貧血、高グロブリン血症。蛋白電気泳動でポリクローナルγグロブリン上昇。腎機能検査で蛋白尿を評価。FIP、リンパ腫、ヘモプラズマ症との鑑別が必要。"
}
ENRICHMENTS["cat_feline_hepatozoonosis"] = {
    "diagnosis_ja": "発熱・食欲不振・体重減少・筋肉痛・リンパ節腫大を呈する。CBC好中球増多と好中球内のHepatozoon felisの配偶子母体（gamont）を確認。PCR検査で確定診断と種同定。血液化学で肝酵素上昇、CK上昇を認めることがある。筋生検で筋線維内のシゾントを確認できることがある。マダニ曝露歴を確認（猫ではマダニの経口摂取が感染経路）。FIV/FeLV検査で免疫状態を評価。トキソプラズマ症、エーリキア症、ヘモプラズマ症との鑑別が必要。"
}
ENRICHMENTS["cat_feline_tritrichomonas_infection"] = {
    "diagnosis_ja": "大腸性下痢（粘液便・軟便〜水様便）を呈する若齢〜中齢猫。多頭飼育環境に好発。直接糞便塗抹で運動性のある栄養型を観察（特徴的な波動膜運動）。InPouch TF培養キットで増殖を確認。リアルタイムPCR検査が確定診断のゴールドスタンダード。Giardia抗原検査との交差反応に注意。糞便検査で他の寄生虫を除外。T. foetus感染は自然治癒傾向があるが長期保菌となる。IBD、食物反応性腸症、コクシジウム症との鑑別が必要。"
}
ENRICHMENTS["cat_feline_strongyloides_infection"] = {
    "diagnosis_ja": "下痢（水様〜粘血便）・体重減少を呈する。免疫抑制猫で重症化。糞便検査で特徴的な幼虫含有虫卵を確認（直接法・浮遊法）。バーマン法で糞便中の第一期幼虫を検出。重症例では血便・蛋白漏出性腸症を呈する。CBC好酸球増多を認めることがある。免疫抑制時は幼虫の過感染（hyperinfection）による肺移行症（咳嗽・呼吸困難）を評価。FIV/FeLV検査。鉤虫症、コクシジウム症、トリトリコモナス症との鑑別が必要。"
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
