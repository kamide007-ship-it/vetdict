#!/usr/bin/env python3
"""Enrich diagnosis_ja for 50 Rabbit diseases with disease-specific diagnostic protocols.

Replaces short generic text with detailed, rabbit-specific diagnostic methods
including stress-free handling considerations, specific test values/thresholds,
and species-appropriate procedures.
"""
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 1. Limb Fracture (rabbit_fracture_limb)
ENRICHMENTS["rabbit_fracture_limb"] = {
    "diagnosis_ja": (
        "触診で疼痛・腫脹・クレピタス・異常可動性を確認。X線検査（2方向以上）で骨折型・転位を評価。"
        "ウサギは後肢骨折時に脊椎骨折（L7）を併発しやすいため腰椎〜仙椎のX線も必須。"
        "複雑骨折・関節内骨折ではCTで詳細評価。血液検査でCa（正常12-16 mg/dL）・P値を確認し代謝性骨疾患を除外。"
        "ストレス最小化のため保定時間を短縮し、必要に応じブトルファノール0.1-0.5 mg/kg SCで鎮痛後に撮影。"
    )
}

# 2. Osteoarthritis (rabbit_osteoarthritis)
ENRICHMENTS["rabbit_osteoarthritis"] = {
    "diagnosis_ja": (
        "X線検査で骨棘形成・関節裂隙狭小化・軟骨下骨硬化を評価。好発部位は膝関節・足根関節・脊椎。"
        "関節液分析で細胞数<5,000/μL・粘稠度良好なら非感染性と判断。CBC・生化学（BUN 15-23 mg/dL、Cre 0.5-2.5 mg/dL）で"
        "腎機能評価（NSAIDs使用前に必須）。免疫学的検査でRAを除外。跛行スコアリング（0-5段階）で重症度を客観評価。"
        "高齢ウサギ（5歳以上）では脊椎症との合併が多く、腰椎X線も追加。"
    )
}

# 3. Hindlimb Paresis/Paralysis (rabbit_hind_limb_paresis)
ENRICHMENTS["rabbit_hind_limb_paresis"] = {
    "diagnosis_ja": (
        "神経学的検査で麻痺の左右差・深部痛覚・膀胱機能を評価。脊椎X線で骨折（特にL7）・脱臼・椎間板疾患を確認。"
        "MRI/CTで脊髄圧迫・椎間板ヘルニアの詳細評価。E. cuniculiの血清抗体価（IgG/IgM）測定—IgM陽性は活動性感染を示唆。"
        "血液検査で血糖値（正常75-150 mg/dL）・Ca・腎機能を確認し代謝性原因を除外。"
        "外傷歴（不適切な保定・落下）の聴取が重要。排尿障害があれば膀胱触診と残尿評価。"
    )
}

# 4. Mucormycosis (rabbit_0044)
ENRICHMENTS["rabbit_0044"] = {
    "diagnosis_ja": (
        "病変部の直接鏡検（KOH標本）で幅広・無隔壁・直角分岐の菌糸を確認。"
        "培養はSDA培地25-37℃で3-5日（Mucor/Rhizopus属の同定）。PCRで属レベルの迅速同定が可能。"
        "組織生検・病理でPAS/GMS染色により組織侵襲性を評価—血管浸潤は予後不良の指標。"
        "画像検査（X線/CT）で肺・副鼻腔・脳への波及を評価。CBC（白血球数2-12×10³/μL）で免疫抑制状態を確認。"
        "免疫抑制要因（ストレス・ステロイド投与歴・栄養不良）の聴取。"
    )
}

# 5. Endometrial Hyperplasia (rabbit_0115)
ENRICHMENTS["rabbit_0115"] = {
    "diagnosis_ja": (
        "腹部超音波で子宮壁の不均一な肥厚・嚢胞性変化を描出。子宮径>10 mmで異常。"
        "X線で子宮のソフトティッシュ陰影拡大を確認。CBC・生化学でPCV（正常33-45%）・TP（正常5.4-8.3 g/dL）を評価し貧血の有無を確認。"
        "血尿がある場合は尿検査で腎性血尿との鑑別（尿沈渣で赤血球形態評価）。"
        "未避妊雌ウサギの3歳以上で発生率が急増（4歳以上で60%以上）。確定診断は卵巣子宮摘出術後の病理組織検査。"
    )
}

# 6. Pyometra (rabbit_0116)
ENRICHMENTS["rabbit_0116"] = {
    "diagnosis_ja": (
        "腹部超音波で子宮内腔の液体貯留・子宮壁肥厚を確認。X線で腫大した子宮陰影を描出。"
        "CBC（白血球数>12×10³/μLで白血球増多、左方移動）・生化学でBUN/Creを評価し腎機能障害の有無を確認。"
        "CRP上昇で全身性炎症を評価。膣分泌物がある場合（開放性）は細菌培養・感受性試験を実施—"
        "Pasteurella multocida・Staphylococcus aureus が多い。ペニシリン系は禁忌のため感受性結果に基づき抗菌薬を選択。"
        "術前血液検査で凝固系・電解質も確認。"
    )
}

# 7. Ovarian Cyst (rabbit_0118)
ENRICHMENTS["rabbit_0118"] = {
    "diagnosis_ja": (
        "腹部超音波で卵巣内の液体貯留嚢胞を描出—直径>3 mmで有意。漿液性嚢胞（無エコー）と"
        "粘液性嚢胞（低エコー）の鑑別。X線で腹腔内腫瘤陰影を確認。"
        "ホルモン検査でエストラジオール値の持続高値（>50 pg/mL）は卵胞嚢胞を示唆。"
        "CBC（PCV低下<30%は再生不良性貧血を示唆—エストロゲン過剰による骨髄抑制）。"
        "子宮内膜過形成・子宮腺癌の合併評価のため子宮も超音波で精査。確定は摘出後病理。"
    )
}

# 8. Orchitis (rabbit_0120)
ENRICHMENTS["rabbit_0120"] = {
    "diagnosis_ja": (
        "視診・触診で精巣の腫脹・硬度変化・疼痛・発赤を評価。超音波で精巣実質のエコー変化・膿瘍形成を確認。"
        "精巣周囲液貯留（陰嚢水腫との鑑別）を評価。分泌物がある場合は細菌培養・感受性試験—"
        "Pasteurella multocida・Treponema cuniculiが原因菌として多い。"
        "CBC（白血球数上昇・左方移動）・生化学で全身性炎症を評価。"
        "トレポネーマ症との鑑別にダークフィールド顕微鏡検査・RPR。確定診断は去勢術後の病理組織検査。"
    )
}

# 9. Pregnancy Toxemia (rabbit_0121)
ENRICHMENTS["rabbit_0121"] = {
    "diagnosis_ja": (
        "妊娠末期〜分娩直後の肥満雌で疑う。血液検査で血糖値低下（<60 mg/dL）・ケトン体陽性・"
        "BUN上昇（>25 mg/dL）・肝酵素上昇（ALT>80 U/L）を確認。尿検査でケトン尿（ケトスティック陽性）。"
        "腹部超音波で胎仔生存確認・肝臓のエコー輝度上昇（脂肪肝）を評価。"
        "血液ガス分析で代謝性アシドーシス（pH<7.3、HCO3<15 mEq/L）を評価。"
        "体重減少・食欲廃絶・嗜眠の臨床徴候と併せて診断。ストレス最小化のため迅速に検査を完了。"
    )
}

# 10. Pseudopregnancy (rabbit_0123)
ENRICHMENTS["rabbit_0123"] = {
    "diagnosis_ja": (
        "巣作り行動・腹部膨満・乳腺腫大・毛抜き行動の臨床徴候を確認。"
        "腹部超音波で妊娠（胎仔の確認）を除外—超音波では妊娠10日目以降で胎嚢が描出可能。"
        "腹部X線で胎仔骨格の石灰化（妊娠21日目以降）を確認し偽妊娠と鑑別。"
        "プロゲステロン値測定（黄体機能評価）。子宮内膜過形成・子宮水腫の合併を超音波で評価。"
        "通常16-18日で自然消退。繰り返す場合は卵巣子宮摘出術を推奨。行動歴（他ウサギとの接触）を聴取。"
    )
}

# 11. Wound Infection (rabbit_0211)
ENRICHMENTS["rabbit_0211"] = {
    "diagnosis_ja": (
        "創傷部の視診で発赤・腫脹・排膿・壊死組織を評価。ウサギの膿は犬猫と異なりクリーム状で粘稠（ケース状膿瘍）。"
        "創傷スワブ培養・感受性試験を実施—Pasteurella multocida・Staphylococcus aureusが主要原因菌。"
        "ペニシリン系経口投与は致死的腸内細菌叢破壊を起こすため禁忌（注射は可）。"
        "CBC（白血球数>12×10³/μLで感染示唆、ヘテロフィル優位）。深部感染疑いではX線/超音波で膿瘍・骨髄炎を評価。"
        "破傷風リスクも考慮。"
    )
}

# 12. Agalactia (rabbit_0223)
ENRICHMENTS["rabbit_0223"] = {
    "diagnosis_ja": (
        "分娩後24-48時間以内の乳汁分泌不全を確認。乳腺の視診・触診で腫脹・硬結・発赤（乳腺炎合併）を評価。"
        "CBC・生化学でCa（正常12-16 mg/dL、低Ca血症では泌乳障害）・血糖値・PCV（貧血の有無）を確認。"
        "プロラクチン値測定（低値で診断的）。子仔の体重推移を記録（生後1-2日で5-10%増加が正常）。"
        "腹部超音波で子宮復古・乳腺の構造を評価。ストレス要因（環境変化・過密飼育）の聴取。"
        "栄養状態と飼料内容（高繊維食・適切なCa/P比）を確認。"
    )
}

# 13. Testicular Seminoma (rabbit_0256)
ENRICHMENTS["rabbit_0256"] = {
    "diagnosis_ja": (
        "精巣の片側性腫大・硬度変化を触診で確認。超音波で精巣実質の均一な低エコー腫瘤を描出。"
        "腹部X線/超音波で腹腔内リンパ節腫大（転移評価）を確認。胸部X線で肺転移の有無をスクリーニング。"
        "CBC・生化学（LDH上昇は腫瘍マーカーとして参考）。FNA（細胞診）で大型均一な腫瘍細胞を確認。"
        "確定診断は去勢術後の病理組織検査（HE染色+免疫組織化学：PLAP、c-kit）。"
        "ウサギのセミノーマは犬と比較して転移率が低いが、対側精巣も評価。"
    )
}

# 14. Mammary Gland Tumour (rabbit_mammary_gland_tumour)
ENRICHMENTS["rabbit_mammary_gland_tumour"] = {
    "diagnosis_ja": (
        "乳腺の触診で腫瘤の大きさ・硬度・可動性・皮膚との癒着を評価。FNA（細胞診）で良悪性の予備評価。"
        "胸部X線（3方向）で肺転移スクリーニング—転移陰影の有無を確認。"
        "腹部超音波で腹腔内リンパ節・臓器転移を評価。CBC・生化学（ALP上昇は骨転移を示唆）。"
        "確定診断は摘出後の病理組織検査（HE染色）—乳腺癌・乳腺腺腫・乳管内乳頭腫の鑑別。"
        "未避妊雌で好発（ホルモン依存性）。避妊歴・年齢（2歳以上でリスク上昇）を聴取。"
    )
}

# 15. Testicular Tumour (rabbit_testicular_tumour)
ENRICHMENTS["rabbit_testicular_tumour"] = {
    "diagnosis_ja": (
        "精巣の大きさ・左右差・硬度変化・表面性状を触診で評価。超音波で腫瘤のエコーパターンを確認—"
        "セルトリ細胞腫（不均一エコー）・ライディッヒ細胞腫（高エコー結節）・セミノーマ（均一低エコー）の鑑別。"
        "腹腔内X線/超音波で後腹膜リンパ節転移を評価。胸部X線で遠隔転移を確認。"
        "CBC・生化学で全身状態を評価。エストロゲン産生腫瘍ではPCV低下（骨髄抑制）・雌性化徴候に注意。"
        "確定は去勢術後の病理（HE+免疫染色）。"
    )
}

# 16. Leiomyoma (Uterine) (rabbit_leiomyoma_uterine)
ENRICHMENTS["rabbit_leiomyoma_uterine"] = {
    "diagnosis_ja": (
        "腹部超音波で子宮壁内の境界明瞭な均一エコー腫瘤を描出。子宮腺癌との鑑別が重要—"
        "腺癌は不整形・不均一エコーで浸潤性。腹部X線で軟部組織陰影を確認。"
        "CBC・生化学でPCV（貧血の有無）・TP・肝腎機能を術前評価。"
        "胸部X線で肺転移を除外（平滑筋腫は良性だが腺癌との術前鑑別は困難）。"
        "血尿がある場合は尿検査で腎性出血との鑑別。"
        "確定は卵巣子宮摘出術後の病理組織検査。未避妊雌ウサギ3歳以上で好発。"
    )
}

# 17. Endometritis (rabbit_endometritis)
ENRICHMENTS["rabbit_endometritis"] = {
    "diagnosis_ja": (
        "膣分泌物（血性・膿性）の性状を確認。腹部超音波で子宮内膜の肥厚・子宮内液貯留を描出。"
        "子宮壁の構造異常（子宮内膜過形成・腺癌との合併）も評価。"
        "分泌物の細菌培養・感受性試験—Pasteurella multocida・Staphylococcus aureus・大腸菌が主要原因。"
        "ペニシリン系経口は腸内細菌叢破壊により致死的なため禁忌。"
        "CBC（白血球増多・ヘテロフィル増加）・生化学（TP上昇はグロブリン上昇を示唆）。"
        "確定は術後病理。未避妊雌ウサギ3歳以上でリスク高。"
    )
}

# 18. Mammary Cyst (rabbit_mammary_cyst)
ENRICHMENTS["rabbit_mammary_cyst"] = {
    "diagnosis_ja": (
        "乳腺の触診で波動感のある腫瘤を確認。超音波で無エコー〜低エコーの嚢胞性病変を描出—"
        "嚢胞壁の肥厚・内部充実成分があれば腫瘍性病変を疑う。FNA（細胞診）で嚢胞液の性状を確認—"
        "漿液性（黄色透明）なら良性嚢胞、血性なら腫瘍を疑い切除生検を検討。"
        "CBC・生化学で全身状態の評価。ホルモン依存性のため避妊歴を確認。"
        "多発性の場合は卵巣嚢胞・子宮疾患の合併を腹部超音波で評価。"
    )
}

# 19. Testicular Abscess (rabbit_testicular_abscess)
ENRICHMENTS["rabbit_testicular_abscess"] = {
    "diagnosis_ja": (
        "精巣の触診で腫脹・疼痛・波動感・発赤を確認。超音波で精巣内の低エコー病変（膿瘍腔）と周囲の高エコーカプセルを描出。"
        "精巣腫瘍との鑑別が重要—膿瘍は辺縁不整で後方エコー増強。"
        "FNA/穿刺液の細菌培養・感受性試験—Pasteurella multocidaが最多原因菌。"
        "ウサギの膿はクリーム状で粘稠（ケース状）のため排膿困難なことが多い。"
        "CBC（ヘテロフィル増加>50%）・CRP上昇で全身性感染を評価。去勢術後の病理で確定。"
    )
}

# 20. Staphylococcal Dermatitis (rabbit_0010)
ENRICHMENTS["rabbit_0010"] = {
    "diagnosis_ja": (
        "皮膚病変部の視診で膿皮症・痂皮・脱毛パターンを評価。皮膚掻破検査で外部寄生虫を除外。"
        "病変部スワブの細菌培養・感受性試験—Staphylococcus aureus（MRSA含む）の同定と薬剤感受性パターンの確認。"
        "細胞診（スタンプ・テープストリップ）で好中球貪食像・球菌を確認。"
        "皮膚生検・病理で深在性感染（蜂窩織炎・膿瘍）の深達度を評価。"
        "基礎疾患（免疫抑制・栄養不良・ストレス・不衛生な環境）の聴取。"
        "抗菌薬選択時にペニシリン系経口は禁忌。"
    )
}

# 21. Dermatophytosis (rabbit_0041)
ENRICHMENTS["rabbit_0041"] = {
    "diagnosis_ja": (
        "Wood灯検査でTrichophyton mentagrophytes（ウサギの最多原因菌）は蛍光陰性が多い点に注意。"
        "毛検査（KOH標本）で毛幹内の分節分生子・菌糸を確認。DTM培地での真菌培養（14-21日）で菌種同定。"
        "PCRで迅速な属レベル同定（T. mentagrophytes vs Microsporum canis）。"
        "皮膚掻破検査で疥癬・毛包虫との鑑別。病変は典型的に鼻・耳・前肢に環状脱毛斑。"
        "人獣共通感染症のため飼い主へのリスク説明と手袋着用指導。CBC（免疫抑制の評価）。"
    )
}

# 22. Dental Abscess (rabbit_0047)
ENRICHMENTS["rabbit_0047"] = {
    "diagnosis_ja": (
        "頭部触診で下顎・上顎の腫脹を確認。頭部X線（最低4方向：DV/VD/側面/斜位）で歯根尖周囲の透過性亢進・骨溶解を評価。"
        "CT（推奨）は歯根膿瘍の範囲・骨浸潤を正確に描出。麻酔下口腔内検査で罹患歯の動揺・歯肉腫脹・瘻管を確認。"
        "ウサギの膿はケース状で粘稠なため切開排膿のみでは治癒困難—根治には罹患歯抜歯+掻爬が必要。"
        "培養（嫌気性培養含む）でPseudomonas・Pasteurella・嫌気性菌を同定。"
        "CBC・生化学で全身状態評価。"
    )
}

# 23. Retrobulbar Dental Abscess (rabbit_0049)
ENRICHMENTS["rabbit_0049"] = {
    "diagnosis_ja": (
        "眼球突出・流涙・眼脂の視診で後眼窩腫瘤を疑う。頭部CT（推奨）で上顎臼歯歯根の尖端が眼窩底に達し"
        "膿瘍形成している所見を確認—X線では重複影で評価困難。麻酔下口腔内検査で上顎臼歯の動揺・歯肉腫脹を評価。"
        "眼科検査（眼底・眼圧測定IOP正常10-20 mmHg）で視神経障害・網膜剥離を評価。"
        "超音波で後眼窩腔の液体貯留・腫瘤性病変を確認。培養（嫌気性含む）で起因菌同定。"
        "ウサギ上顎臼歯の歯根は眼窩に近接するため歯科疾患と眼科疾患の関連を常に考慮。"
    )
}

# 24. Periodontal Disease (rabbit_0053)
ENRICHMENTS["rabbit_0053"] = {
    "diagnosis_ja": (
        "麻酔下口腔内検査で歯肉発赤・腫脹・出血・歯周ポケット深度を歯科プローブで計測。"
        "頭部X線（4方向）で歯槽骨吸収・歯根尖周囲病変を評価—CTは歯根の三次元的評価に優れる。"
        "ウサギは常生歯のため不正咬合との合併が多く、切歯・臼歯の咬合関係も評価。"
        "食餌内容の聴取（干し草摂取量不足が主因—1日体重の約80%の干し草が理想）。"
        "CBC・生化学で慢性感染による貧血・低アルブミンを確認。体重推移の記録（食欲低下の客観評価）。"
    )
}

# 25. Wet Dewlap / Moist Dermatitis (rabbit_0089)
ENRICHMENTS["rabbit_0089"] = {
    "diagnosis_ja": (
        "肉垂（dewlap）部の視診で湿潤・発赤・脱毛・細菌性皮膚炎を確認。"
        "皮膚スワブの細菌培養・感受性試験でPseudomonas aeruginosa・Staphylococcus aureusを同定。"
        "細胞診で好中球浸潤・細菌を確認。皮膚掻破検査で真菌・外部寄生虫を除外。"
        "基礎疾患の評価—不正咬合（過度の流涎原因）、歯科X線で切歯・臼歯を確認。"
        "飲水器タイプの確認（ボウル型は肉垂を濡らすためボトル型を推奨）。"
        "肥満度評価（BCS>4/5で肉垂が大きく発症リスク上昇）。"
    )
}

# 26. Sebaceous Adenitis (rabbit_0225)
ENRICHMENTS["rabbit_0225"] = {
    "diagnosis_ja": (
        "皮膚生検・病理組織検査が確定診断に必須—脂腺周囲の肉芽腫性炎症・脂腺の破壊像を確認。"
        "複数部位からのパンチ生検（6 mm）を推奨。毛検査で鋳型様の毛幹付着物（角質鋳型）を確認。"
        "皮膚掻破検査で疥癬・真菌症を除外。細菌培養で二次感染菌を同定。"
        "鑑別疾患として皮膚糸状菌症・疥癬・細菌性皮膚炎・栄養性脱毛を考慮。"
        "CBC・生化学で甲状腺機能低下症などの内分泌疾患を除外。"
    )
}

# 27. Contact Dermatitis (rabbit_0226)
ENRICHMENTS["rabbit_0226"] = {
    "diagnosis_ja": (
        "病変部位の分布パターンから原因物質を推定—足底部（床材）、腹部（消毒剤）、顔面（食器）。"
        "皮膚掻破検査で寄生虫・真菌を除外。細胞診でアレルギー性炎症（好酸球浸潤）を確認。"
        "パッチテスト（原因物質の同定）—ウサギでは臨床的に実施困難なことが多い。"
        "環境因子の聴取（床材変更・新しい洗剤・消毒剤の使用開始時期）。"
        "皮膚生検・病理で表皮スポンジオーシス・真皮浅層の炎症細胞浸潤を確認。"
        "原因物質除去後の改善で臨床的に診断確定。"
    )
}

# 28. Cellulitis (rabbit_0236)
ENRICHMENTS["rabbit_0236"] = {
    "diagnosis_ja": (
        "視診・触診で患部のびまん性腫脹・発赤・熱感・疼痛を評価。膿瘍との鑑別—膿瘍は境界明瞭・波動感あり。"
        "超音波で皮下組織の浮腫・液体貯留を確認し膿瘍形成の有無を評価。"
        "細菌培養・感受性試験（穿刺液/病変部スワブ）—Pasteurella multocida・嫌気性菌が主要原因。"
        "CBC（ヘテロフィル増加・左方移動・白血球数>12×10³/μL）で全身性感染を評価。"
        "生化学でTP・ALB・グロブリン比を確認。X線で深部組織・骨への波及（骨髄炎）を除外。"
        "ペニシリン系経口は致死的腸炎リスクあり禁忌。"
    )
}

# 29. Tooth Root Abscess (rabbit_tooth_root_abscess)
ENRICHMENTS["rabbit_tooth_root_abscess"] = {
    "diagnosis_ja": (
        "顔面・下顎の触診で硬い腫脹を確認。頭部CT（推奨）で歯根尖周囲の骨溶解・膿瘍形成の範囲を三次元的に評価。"
        "X線（側面・DV・斜位）では歯根尖透過性亢進を確認するが重複影で限界あり。"
        "麻酔下口腔内検査で罹患歯の動揺・歯肉瘻管を確認。歯科プローブで歯周ポケット深度を計測。"
        "ウサギの膿はケース状で粘稠—切開排膿のみでは治癒せず根治的掻爬+抜歯が必要。"
        "培養（嫌気性培養必須）で起因菌同定。CBC・生化学で全身状態評価。"
    )
}

# 30. Tooth Root Elongation (rabbit_tooth_root_elongation)
ENRICHMENTS["rabbit_tooth_root_elongation"] = {
    "diagnosis_ja": (
        "頭部X線（DV・側面・斜位）で臼歯歯根の尖端伸長を評価—上顎臼歯歯根の眼窩方向への伸長、"
        "下顎臼歯歯根の下顎骨腹側への突出を確認。CT（推奨）で歯根と周囲構造の関係を正確に評価。"
        "麻酔下口腔内検査で臼歯の棘状突起（スパー）・舌潰瘍・頬粘膜損傷を確認。"
        "食餌歴の聴取—干し草摂取不足による咬耗不足が主因。体重減少曲線で食欲低下の時期を推定。"
        "流涙・眼脂がある場合は鼻涙管の圧迫を疑い眼科検査を追加。"
    )
}

# 31. Demodex Mange (rabbit_demodex_mange)
ENRICHMENTS["rabbit_demodex_mange"] = {
    "diagnosis_ja": (
        "皮膚深層掻破検査で毛包内のDemodex cuniculiを確認—オイル浸標本で紡錘形のダニを鏡検。"
        "複数部位（病変辺縁部）からの掻破を推奨（感度向上）。毛検査（トリコグラム）で毛包内ダニを確認。"
        "皮膚生検・病理で毛包虫性毛包炎・脂腺の変化を評価。"
        "鑑別疾患として疥癬（Sarcoptes scabiei）・皮膚糸状菌症・細菌性皮膚炎を除外。"
        "免疫抑制状態（ストレス・栄養不良・ステロイド投与歴・併発疾患）の聴取が重要—"
        "ウサギのDemodexは免疫抑制時に発症しやすい。"
    )
}

# 32. Perineal Dermatitis (rabbit_perineal_dermatitis)
ENRICHMENTS["rabbit_perineal_dermatitis"] = {
    "diagnosis_ja": (
        "会陰部の視診で発赤・湿潤・痂皮・脱毛・尿やけを確認。皮膚スワブの細菌培養で二次感染菌を同定。"
        "尿検査（比重・pH・沈渣）で泌尿器疾患（膀胱結石・膀胱炎）を除外—X線で尿路結石の有無を確認。"
        "糞便検査で下痢の原因（コクシジウム・細菌性腸炎）を評価。"
        "肥満度評価（BCS>4/5ではグルーミング不能が原因）。関節疾患（変形性関節症）の併発評価—"
        "高齢ウサギでは後肢関節炎によりセカルトロフ（盲腸便）摂取困難→会陰部汚染。"
        "食餌内容の確認（高炭水化物→軟便→会陰汚染の悪循環）。"
    )
}

# 33. Molar Root Infection (rabbit_molar_root_infection)
ENRICHMENTS["rabbit_molar_root_infection"] = {
    "diagnosis_ja": (
        "頭部CT（推奨）で罹患歯根周囲の骨溶解・膿瘍形成を三次元的に評価。X線（4方向）で歯根尖透過性亢進を確認。"
        "上顎臼歯感染では眼窩・鼻腔・副鼻腔への波及を評価—流涙・鼻汁は上顎歯根感染の間接徴候。"
        "下顎臼歯感染では下顎骨腹側の膨隆を触診。麻酔下口腔内検査で歯冠の変色・動揺・歯肉瘻管を確認。"
        "嫌気性培養を含む細菌培養・感受性試験。CBC（慢性感染でヘテロフィル増加）。"
        "食欲低下・体重減少の経時変化を確認。"
    )
}

# 34. Cheek Tooth Overgrowth (rabbit_cheek_tooth_overgrowth)
ENRICHMENTS["rabbit_cheek_tooth_overgrowth"] = {
    "diagnosis_ja": (
        "麻酔下口腔内検査で臼歯の棘状突起（スパー）の方向・長さを評価—上顎スパーは頬側、下顎スパーは舌側に形成。"
        "頬粘膜・舌の潰瘍・白苔を確認。頭部X線で歯冠の過長・歯根の変形・咬合関係を評価。"
        "CT（推奨）は歯根の三次元的評価に最適。食餌歴の聴取—干し草（チモシー等）不足が根本原因。"
        "体重推移（食欲低下→体重減少）を確認。流涎・流涙・下顎湿性皮膚炎は間接的徴候。"
        "GI stasisの合併評価（腹部触診で胃内容・盲腸ガス貯留）。"
    )
}

# 35. Dental Fistula (rabbit_dental_fistula)
ENRICHMENTS["rabbit_dental_fistula"] = {
    "diagnosis_ja": (
        "顔面・下顎の皮膚瘻管（排膿孔）の位置から罹患歯を推定。瘻管プローブで深度・方向を確認。"
        "頭部CT（推奨）で瘻管の起始歯根・走行経路・骨浸潤範囲を評価。X線で歯根尖病変・骨溶解を確認。"
        "麻酔下口腔内検査で罹患歯の動揺・歯肉腫脹を評価。歯科プローブで歯周ポケット深度計測。"
        "瘻管排膿の細菌培養（嫌気性培養必須）・感受性試験。"
        "ウサギでは慢性歯根膿瘍→瘻管形成が多く、ケース状膿は自然排膿困難。"
        "根治には罹患歯抜歯+瘻管掻爬が必要。"
    )
}

# 36. Dewlap Fold Dermatitis (rabbit_dewlap_fold_dermatitis)
ENRICHMENTS["rabbit_dewlap_fold_dermatitis"] = {
    "diagnosis_ja": (
        "肉垂皮膚襞の視診で発赤・湿潤・悪臭・分泌物・脱毛を評価。皮膚襞内のスワブ培養で"
        "二次感染菌（Pseudomonas aeruginosa・S. aureus・酵母菌）を同定。細胞診で炎症細胞・微生物を確認。"
        "基礎疾患の評価—不正咬合による過度の流涎（歯科X線で評価）、多飲多尿（血液検査で腎機能確認）。"
        "飲水器の種類確認（ボウル型→ボトル型への変更を推奨）。"
        "肥満度評価（BCS>4/5ではskin fold拡大）。甲状腺機能評価。"
        "重症例では皮膚生検で慢性炎症の深達度を確認。"
    )
}

# 37. Ulcerative Pododermatitis - Grade I
ENRICHMENTS["rabbit_ulcerative_pododermatitis_-_grade_i"] = {
    "diagnosis_ja": (
        "足底部の視診で初期脱毛・紅斑・軽度角質肥厚を確認。Grade Iでは潰瘍形成なし・感染徴候なし。"
        "足底圧迫試験で疼痛反応を評価。X線で骨髄炎の有無を確認（Grade Iでは通常陰性）。"
        "リスク因子の評価—体重（BW>4 kgでリスク上昇）、床材（ワイヤーメッシュは最大リスク）、"
        "後肢筋肉量（加齢・運動不足で減少→足底圧集中）、爪の長さ。"
        "肥満度（BCS）、品種（レッキスは足底被毛が薄く好発）を確認。"
        "早期介入が重要—進行するとGrade IV-Vの難治性病変に至る。"
    )
}

# 38. Ulcerative Pododermatitis - Grade IV-V
ENRICHMENTS["rabbit_ulcerative_pododermatitis_-_grade_iv-v"] = {
    "diagnosis_ja": (
        "足底部の視診で深部潰瘍・腱露出・骨露出・壊死組織を確認。Grade IVは深部感染+滑膜炎、"
        "Grade Vは骨髄炎+関節炎。X線で骨溶解・骨膜反応・関節破壊を評価。"
        "創傷スワブの細菌培養・感受性試験（嫌気性培養含む）—S. aureus・Pasteurellaが主要原因。"
        "CBC（ヘテロフィル増加・慢性炎症による貧血PCV<33%）・生化学（アミロイドーシスリスク→TP/ALB）。"
        "両後肢を必ず評価（両側性が多い）。全身状態の悪化（食欲廃絶・GI stasis併発）に注意。"
        "ペニシリン系経口は禁忌。治療反応が乏しければ断脚の検討。"
    )
}

# 39. Pododermatitis - Advanced (Grade IV-V)
ENRICHMENTS["rabbit_pododermatitis_-_advanced_grade_iv-v"] = {
    "diagnosis_ja": (
        "飛節部の視診で深部潰瘍・壊死組織・骨露出を確認。X線で飛節の骨溶解・骨膜反応・関節破壊の有無を評価。"
        "超音波で軟部組織の膿瘍形成を確認。細菌培養・感受性試験（嫌気性培養含む）で起因菌を同定。"
        "CBC（白血球>12×10³/μL、ヘテロフィル優位）で全身性感染を評価。生化学でTP・ALB（慢性炎症→低ALB）、"
        "腎機能（アミロイドーシスリスク→BUN/Cre）を確認。"
        "疼痛評価（ラビットグリマススケール：RbtGS 0-10）で鎮痛管理の必要性を判断。"
        "両後肢+前肢も評価。体重・BCS・床材・運動量の聴取。"
    )
}

# 40. Pasteurellosis / Snuffles (rabbit_0008)
ENRICHMENTS["rabbit_0008"] = {
    "diagnosis_ja": (
        "鼻汁の性状（漿液性→粘液膿性）を確認。鼻腔スワブ/気管洗浄液の細菌培養・感受性試験で"
        "Pasteurella multocida（最も多い血清型A:3）を同定。PCRで迅速検出。"
        "血清学（ELISA抗体検査）は集団スクリーニングに有用だが個体診断には限界あり。"
        "頭部X線/CTで副鼻腔・鼓室胞の液体貯留（中耳炎合併）を評価。胸部X線で肺炎像を確認。"
        "CBC（白血球>12×10³/μL・ヘテロフィル増加）。キャリア状態が多く（50-90%のウサギが保菌）、"
        "ストレスで発症。抗菌薬はペニシリン系経口禁忌、エンロフロキサシン5-20 mg/kg推奨。"
    )
}

# 41. Bordetella Bronchiseptica Infection (rabbit_0009)
ENRICHMENTS["rabbit_0009"] = {
    "diagnosis_ja": (
        "鼻汁・くしゃみ・呼吸音異常を確認。鼻腔/気管スワブの細菌培養で Bordetella bronchiseptica を同定—"
        "MacConkey/Bordet-Gengou培地。PCRで迅速検出可能。胸部X線で気管支肺炎パターン（びまん性間質〜肺胞パターン）を評価。"
        "CBC（ヘテロフィル増加）。Pasteurella との混合感染が多いため同時培養。"
        "感受性試験に基づき抗菌薬を選択—フルオロキノロン系・ST合剤が有効なことが多い。"
        "ペニシリン系経口は禁忌。モルモットと同居の場合、モルモットからの感染も考慮（モルモットは重症化しやすい）。"
    )
}

# 42. Tyzzer's Disease (rabbit_0011)
ENRICHMENTS["rabbit_0011"] = {
    "diagnosis_ja": (
        "急性水様性下痢・食欲廃絶・急速な体重減少の臨床徴候で疑う。特に離乳期（4-12週齢）の若齢ウサギで好発。"
        "確定診断は剖検・病理組織検査—肝臓の巣状壊死+Warthin-Starry銀染色でClostridium piliforme（細胞内桿菌）の証明。"
        "生前診断は困難—血清学（IFA法抗体検査）は集団レベルの監視に使用。"
        "PCR（糞便/肝臓）で遺伝子検出可能だが検査室が限られる。"
        "生化学で肝酵素上昇（ALT>80 U/L、GGT上昇）・BUN上昇を確認。"
        "CBC（急性期はヘテロフィル減少→免疫不全を示唆）。ストレス・過密飼育・不衛生環境が誘因。"
    )
}

# 43. Clostridial Enterotoxemia (rabbit_0012)
ENRICHMENTS["rabbit_0012"] = {
    "diagnosis_ja": (
        "急性水様性〜粘液血性下痢・腹部膨満・急速な虚脱で疑う。盲腸の異常発酵によるガス貯留を腹部触診/X線で確認。"
        "糞便の嫌気性培養でClostridium spiroforme（イオタ毒素産生）を同定。毒素検出（ELISA/PCR）で確定。"
        "抗菌薬投与歴の聴取—ペニシリン系・リンコマイシン系・マクロライド系経口投与は腸内細菌叢破壊→"
        "Clostridium過増殖の最大リスク因子。CBC（急性期はヘテロフィル減少→敗血症徴候）。"
        "生化学で血糖低下・電解質異常（低K・代謝性アシドーシス）を評価。"
        "超急性型は発症24-48時間で死亡するため迅速な診断と治療開始が必要。"
    )
}

# 44. Treponematosis / Rabbit Syphilis (rabbit_0015)
ENRICHMENTS["rabbit_0015"] = {
    "diagnosis_ja": (
        "外陰部・肛門周囲・鼻・口唇の痂皮性潰瘍病変を確認。ダークフィールド顕微鏡検査で病変部スワブから"
        "Treponema cuniculi のスピロヘータを直接観察（感度は病変活動期に高い）。"
        "血清学（RPR/VDRL）はヒトのT. pallidum試薬と交差反応するため利用可能だが偽陽性あり。"
        "PCR（特異的プライマー）で確定的。皮膚糸状菌症・疥癬・Pasteurella皮膚感染との鑑別が必要。"
        "皮膚生検・病理で表皮肥厚・真皮のリンパ形質細胞浸潤+Warthin-Starry銀染色でスピロヘータ証明。"
        "性感染症のため同居ウサギの検査も必須。"
    )
}

# 45. Pseudomonas Infection (rabbit_0017)
ENRICHMENTS["rabbit_0017"] = {
    "diagnosis_ja": (
        "感染部位（皮膚・外耳・呼吸器・泌尿器）に応じた検体採取。細菌培養・感受性試験で"
        "Pseudomonas aeruginosa を同定（MacConkey培地で非発酵・酸化反応陽性・特有の甘い臭い・緑色色素産生）。"
        "多剤耐性パターンが多いため感受性試験は必須—フルオロキノロン系・アミノグリコシド系が有効なことが多い。"
        "ペニシリン系経口は禁忌（腸内細菌叢破壊リスク）。CBC（ヘテロフィル増加）・生化学で全身状態評価。"
        "画像検査で感染の深部波及（中耳炎→内耳炎→斜頸、肺炎）を確認。"
        "環境衛生・水質汚染の評価。"
    )
}

# 46. Streptococcal Infection (rabbit_0018)
ENRICHMENTS["rabbit_0018"] = {
    "diagnosis_ja": (
        "感染部位の検体（膿・分泌物・血液）の細菌培養で連鎖球菌（Streptococcus spp.）を同定。"
        "グラム染色でグラム陽性球菌の連鎖配列を確認。感受性試験で抗菌薬選択—ペニシリン系は注射のみ使用可（経口禁忌）。"
        "CBC（白血球増多>12×10³/μL・ヘテロフィル優位・左方移動）で感染の重症度を評価。"
        "生化学でTP上昇（グロブリン増加）・肝腎機能を確認。"
        "皮膚感染では膿瘍形成の画像評価（超音波）。呼吸器感染では胸部X線。"
        "敗血症が疑われる場合は血液培養（好気・嫌気）を実施。免疫抑制状態の評価。"
    )
}

# 47. Tularemia (rabbit_0020)
ENRICHMENTS["rabbit_0020"] = {
    "diagnosis_ja": (
        "人獣共通感染症（BSL-3病原体）のため取扱いに厳重注意。Francisella tularensisの培養は特殊培地"
        "（チョコレート寒天/システイン心臓寒天）で3-5日—バイオセーフティキャビネット内で操作必須。"
        "PCR（血液・リンパ節）で迅速検出可能。血清学（凝集反応）でペア血清（4倍以上の抗体価上昇）。"
        "臨床徴候：急性の発熱・脾腫・リンパ節腫大・急死（致死率高い）。剖検で脾臓・肝臓の多発巣状壊死。"
        "CBC（重症では汎血球減少）。野兎との接触歴・マダニ暴露歴を聴取。"
        "法定伝染病（四類感染症）のため診断確定時は保健所に届出義務。"
    )
}

# 48. Mycobacteriosis (rabbit_0021)
ENRICHMENTS["rabbit_0021"] = {
    "diagnosis_ja": (
        "病変部の組織生検・病理で類上皮細胞肉芽腫・ラングハンス巨細胞・乾酪壊死を確認。"
        "チール・ネールゼン（抗酸菌）染色で抗酸性桿菌を証明。培養は小川培地/MGIT（4-8週間）で同定—"
        "M. avium complex・M. bovisの鑑別。PCR（IS900/IS1081プライマー）で菌種の迅速同定。"
        "ツベルクリン皮内反応検査（0.1 mL、48-72時間後判定）はスクリーニングに使用。"
        "胸部X線で肺結節・リンパ節腫大を評価。腹部超音波で肝脾腫・腸間膜リンパ節腫大を確認。"
        "CBC・生化学で慢性消耗性変化（貧血・低ALB）を評価。人獣共通感染症のため飼い主への説明必須。"
    )
}

# 49. Yersiniosis (rabbit_0022)
ENRICHMENTS["rabbit_0022"] = {
    "diagnosis_ja": (
        "急性下痢・体重減少・リンパ節腫大で疑う。糞便培養（CIN培地/MacConkey培地4℃増菌法）で"
        "Yersinia pseudotuberculosis / Y. enterocolitica を同定。PCR（ail遺伝子/inv遺伝子）で迅速検出。"
        "血清学（凝集反応）で抗体価測定—ペア血清で4倍以上の上昇。"
        "剖検で腸間膜リンパ節・脾臓・肝臓の多発白色結節（乾酪壊死巣）が特徴的。"
        "CBC（ヘテロフィル増加）・生化学（肝酵素上昇）で全身感染の評価。"
        "鑑別疾患としてティザー病・コクシジウム症・クロストリジウム性腸炎を考慮。飼育環境・野生齧歯類との接触歴を聴取。"
    )
}

# 50. Squamous Cell Carcinoma (rabbit_0202)
ENRICHMENTS["rabbit_0202"] = {
    "diagnosis_ja": (
        "腫瘤の視診・触診で大きさ・硬度・潰瘍形成・皮膚との癒着を評価。組織生検（切開/パンチ生検6 mm）で"
        "HE染色により角化傾向のある扁平上皮の浸潤性増殖を確認—細胞異型度・核分裂像で悪性度を評価。"
        "FNA（細胞診）は予備評価に有用（角化細胞クラスターを確認）。"
        "CT（推奨）で局所浸潤範囲・リンパ節転移を三次元的に評価。胸部X線（3方向）で肺転移スクリーニング。"
        "所属リンパ節のFNAで転移を評価。CBC・生化学（ALP上昇は骨浸潤を示唆）で全身状態評価。"
        "好発部位は皮膚・口腔粘膜・外耳。高齢ウサギで好発。"
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
