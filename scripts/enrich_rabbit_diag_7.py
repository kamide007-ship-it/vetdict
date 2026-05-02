#!/usr/bin/env python3
"""Enrich diagnosis_ja for Rabbit entries (batch 7: 50 entries)."""
import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 1. rabbit_0251 — Pancytopenia / 汎血球減少症（ウサギ）
ENRICHMENTS["rabbit_0251"] = {
    "diagnosis_ja": "沈鬱・食欲不振・蒼白粘膜・出血傾向・易感染から汎血球減少症を疑う。CBC/血液塗抹で貧血・白血球減少・血小板減少の3系統減少を確認。網状赤血球数で骨髄再生能を評価。生化学でBUN/Cre・肝酵素を確認し臓器障害を除外。骨髄穿刺・生検で骨髄低形成・線維化・腫瘍浸潤（リンパ腫等）を鑑別。感染症検査（E. cuniculi抗体）で基礎疾患を評価。ウサギでは骨髄疾患の診断に骨髄生検が不可欠。鑑別にエストロゲン中毒（未避妊雌）を考慮。"
}

# 2. rabbit_0252 — Hemolytic Disease / 溶血性疾患（ウサギ）
ENRICHMENTS["rabbit_0252"] = {
    "diagnosis_ja": "蒼白粘膜・黄疸・赤褐色尿・沈鬱から溶血性疾患を疑う。CBCでPCV低下・網状赤血球増多（再生性貧血）を確認。血液塗抹で球状赤血球・多染性赤血球・Heinz小体を評価。生化学で間接ビリルビン上昇・LDH上昇を確認。直接クームス試験で免疫介在性溶血を評価。尿検査でヘモグロビン尿を確認。酸化性物質への曝露歴（タマネギ・銅）を聴取。ウサギでは正常尿が赤色を呈することがあり、真の血尿・ヘモグロビン尿との鑑別が重要。"
}

# 3. rabbit_0253 — Renal Carcinoma / 腎癌（ウサギ）
ENRICHMENTS["rabbit_0253"] = {
    "diagnosis_ja": "血尿・腹部腫瘤触知・体重減少・多飲多尿から腎癌を疑う。超音波で腎実質内の充実性腫瘤・腎変形を確認。X線で腎腫大・石灰化を評価。FNA細胞診で腫瘍細胞を確認。確定は腎生検または摘出腎の病理組織検査。CT検査で対側腎・転移の有無を精査。生化学でBUN/Cre・SDMA上昇・電解質異常を評価。尿検査で血尿・蛋白尿を確認。ウサギでは腎胚芽腫（nephroblastoma）も報告されており組織型鑑別が重要。"
}

# 4. rabbit_0254 — Bile Duct Adenoma / 胆管腺腫（ウサギ）
ENRICHMENTS["rabbit_0254"] = {
    "diagnosis_ja": "慢性食欲不振・体重減少・肝腫大から胆管腺腫を疑う。超音波で肝内の嚢胞状〜充実性腫瘤を確認。生化学で肝酵素上昇（ALP・GGT・AST）・胆汁酸上昇を評価。FNA細胞診で良性胆管上皮細胞のクラスターを確認。確定は肝生検の病理組織検査で胆管上皮の腺腫性増殖を確認。CT検査で腫瘤の範囲・多発性を評価。ウサギではコクシジウム（E. stiedai）の慢性肝感染が胆管増生の素因となるため、糞便検査でオーシストを除外する。"
}

# 5. rabbit_0255 — Mesothelioma / 中皮腫（ウサギ）
ENRICHMENTS["rabbit_0255"] = {
    "diagnosis_ja": "腹水・胸水貯留・呼吸困難・腹部膨満から中皮腫を疑う。体腔液の細胞診で特徴的な中皮腫細胞（大型で核小体明瞭、細胞塊形成）を確認。超音波で胸腔・腹腔の液体貯留と腫瘤性病変を評価。CT検査で胸膜・腹膜の結節性肥厚を精査。組織生検で確定し免疫組織化学（カルレチニン・サイトケラチン5/6陽性）で腺癌と鑑別。CBC/生化学で低蛋白血症を評価。ウサギの中皮腫は稀だが、腹水・胸水の原因精査で鑑別に含める必要がある。"
}

# 6. rabbit_0257 — Retinal Degeneration / 網膜変性（ウサギ）
ENRICHMENTS["rabbit_0257"] = {
    "diagnosis_ja": "視力低下・物にぶつかる行動・瞳孔散大（対光反射遅延）から網膜変性を疑う。眼底検査で網膜血管の細小化・網膜菲薄化・タペタム反射異常を確認。網膜電図（ERG）で網膜機能の客観的評価を実施。眼超音波で網膜剥離・眼内腫瘤を除外。CBC/生化学で基礎疾患（腎不全・E. cuniculi感染）を評価。E. cuniculi抗体検査で眼型エンセファリトゾーン症を除外。ウサギでは先天性（遺伝性）と後天性（炎症後・栄養欠乏）を鑑別する。"
}

# 7. rabbit_0258 — Iris Prolapse / 虹彩脱出（ウサギ）
ENRICHMENTS["rabbit_0258"] = {
    "diagnosis_ja": "角膜穿孔部からの虹彩組織の突出を視診で確認。スリットランプ検査で角膜穿孔の部位・大きさ・虹彩嵌頓の程度を評価。フルオレセイン染色で角膜上皮欠損・房水漏出（Seidel試験陽性）を確認。眼圧測定で低眼圧を確認。眼超音波で水晶体脱臼・眼内異物を除外。細菌培養で感染を評価。ウサギでは外傷（同居ウサギとの喧嘩・鋭利物）が主因であり、E. cuniculi関連の水晶体誘発性ぶどう膜炎による角膜穿孔も考慮する。緊急眼科処置が必要。"
}

# 8. rabbit_0260 — Mandibular Fracture / 下顎骨折（ウサギ）
ENRICHMENTS["rabbit_0260"] = {
    "diagnosis_ja": "食欲不振・流涎・下顎の腫脹/変形・歯列不整から下顎骨折を疑う。X線（頭部：lateral・DV・oblique）で骨折線・転位を確認。CT検査で骨折の詳細な3D評価と歯根への影響を精査。口腔内検査で歯牙損傷・咬合異常を確認。CBC/生化学で全身状態を評価。ウサギは常生歯（open-rooted teeth）であるため骨折に伴う歯根損傷が二次的不正咬合の原因となる。外傷歴（落下・踏みつけ・過度の保定）を聴取。代謝性骨疾患（Ca/VitD欠乏）も骨折素因として評価。"
}

# 9. rabbit_0261 — Tibial Fracture / 脛骨骨折（ウサギ）
ENRICHMENTS["rabbit_0261"] = {
    "diagnosis_ja": "後肢の挙上・腫脹・疼痛・異常可動性・軋轢音から脛骨骨折を疑う。X線（2方向）で骨折の部位・型（斜骨折・螺旋骨折・粉砕骨折）・転位を確認。触診で開放骨折の有無を評価。CBC/生化学でCa/P・ALP（代謝性骨疾患の評価）を確認。ウサギは後肢の筋量に対して骨が脆弱であり、不適切な保定や保定中のパニック（キック）で脛骨骨折が好発する。後腸発酵動物のため術後のGI stasis予防が重要。鑑別に脊椎骨折・股関節脱臼を考慮。"
}

# 10. rabbit_0262 — Hip Dysplasia / 股関節形成不全（ウサギ）
ENRICHMENTS["rabbit_0262"] = {
    "diagnosis_ja": "後肢の跛行・歩行異常・運動嫌い・立ち上がり困難から股関節形成不全を疑う。X線（VD伸展位）で寛骨臼の浅さ・大腿骨頭の亜脱臼・骨棘形成を確認。触診でOrtolani試験陽性を評価。CT検査で骨形態の3D評価を実施。CBC/生化学で基礎疾患を除外。ウサギでは大型品種（フレミッシュジャイアント等）で報告がある。鑑別に脊椎変形性脊椎症・E. cuniculi関連後肢不全麻痺・脛骨骨折・腰仙部疾患を考慮する。"
}

# 11. rabbit_0264 — Thyroid Disorder / 甲状腺疾患（ウサギ）
ENRICHMENTS["rabbit_0264"] = {
    "diagnosis_ja": "体重変化（増加/減少）・活動性変化・毛並み異常・心拍数異常から甲状腺疾患を疑う。血清T4・fT4測定で甲状腺機能を評価。TSH刺激試験で機能低下症を確認。超音波で甲状腺のサイズ・形態・結節を確認。FNA細胞診で結節性病変の性状を評価。CBC/生化学でコレステロール・トリグリセリド・肝酵素を確認。ウサギの甲状腺疾患は犬猫と比較して報告が少なく、基準値の種差に注意が必要。鑑別に副腎疾患・肝疾患を考慮する。"
}

# 12. rabbit_0266 — Destructive Chewing Behavior / 破壊的咀嚼行動（ウサギ）
ENRICHMENTS["rabbit_0266"] = {
    "diagnosis_ja": "ケージ・家具・電気コードの過度な咀嚼から破壊的咀嚼行動を疑う。口腔検査で臼歯不正咬合（spurs・過長）を除外。頭部X線で歯根伸長・歯根膿瘍を確認。CBC/生化学で基礎疾患を除外。食餌内容の聴取（繊維不足・牧草摂取量）で栄養面を評価。ウサギは常生歯であるため本能的に咀嚼行動が必須であり、適切な咀嚼対象（牧草・安全な木材）の不足が破壊的行動の主因。環境エンリッチメント不足・退屈・ストレスも行動学的素因として評価する。"
}

# 13. rabbit_0267 — Fear Response Syndrome / 恐怖反応症候群（ウサギ）
ENRICHMENTS["rabbit_0267"] = {
    "diagnosis_ja": "過剰な逃避反応・フリージング（凍結行動）・スタンピング・攻撃性から恐怖反応症候群を疑う。身体検査で外傷（パニック時の骨折・脊椎損傷）の有無を確認。CBC/生化学でストレスマーカー（コルチゾール・H/L比）を評価。X線で脊椎骨折を除外（パニック時の後肢キックで発生）。器質的疾患（痛み・E. cuniculi・中耳炎による前庭障害）を除外。飼育環境（捕食者の存在・騒音・不適切な取り扱い）の聴取が診断の核心。ウサギは被捕食動物であり恐怖反応が致死的となりうる。"
}

# 14. rabbit_0268 — Overgrooming / 過剰グルーミング（ウサギ）
ENRICHMENTS["rabbit_0268"] = {
    "diagnosis_ja": "限局性脱毛・毛球の過剰摂取・消化管毛球症からの二次問題から過剰グルーミングを疑う。皮膚掻破検体で外部寄生虫（Cheyletiella・Psoroptes）を除外。真菌培養で皮膚糸状菌症を除外。CBC/生化学で基礎疾患（肝疾患・腎疾患）を除外。ホルモン検査で卵巣嚢胞・副腎疾患を評価。X線で消化管毛球の有無を確認。ウサギは嘔吐ができないため毛球が胃内に蓄積する。環境ストレス・同居動物との関係・退屈が行動学的原因として重要。"
}

# 15. rabbit_0269 — Iatrogenic GI Dysbiosis / 医原性消化管細菌叢異常（ウサギ）
ENRICHMENTS["rabbit_0269"] = {
    "diagnosis_ja": "抗生物質投与後の急性下痢・食欲不振・腹部膨満・ガス貯留から医原性消化管細菌叢異常を疑う。糞便の直接塗抹・グラム染色で細菌叢の異常（Clostridium過増殖）を確認。糞便培養でClostridium spiroforme等を同定。CBC/生化学で脱水・電解質異常・肝酵素上昇を評価。X線で腸管ガス貯留・イレウスを確認。投与薬歴の聴取が不可欠で、ウサギではペニシリン系（経口）・リンコマイシン・クリンダマイシン・エリスロマイシンがClostridium過増殖と致死的腸炎を惹起する。"
}

# 16. rabbit_0270 — Spleen Abscess / 脾臓膿瘍（ウサギ）
ENRICHMENTS["rabbit_0270"] = {
    "diagnosis_ja": "腹部膨満・食欲不振・発熱・沈鬱から脾臓膿瘍を疑う。超音波で脾臓内の低エコー領域・嚢胞状構造を確認。X線で脾腫大を評価。FNA細胞診でヘテロフィル性炎症と変性好中球を確認。培養・感受性試験でPasteurella multocida・Staphylococcus等を同定。CBC/生化学でヘテロフィル増多・フィブリノーゲン上昇を確認。ウサギではP. multocidaによる血行性播種が脾臓膿瘍の主要原因。他臓器の膿瘍（肝・肺・子宮）の併発を評価する。"
}

# 17. rabbit_0271 — Encephalitozoon Intestinalis Infection / エンセファリトゾーンインテスティナリス感染
ENRICHMENTS["rabbit_0271"] = {
    "diagnosis_ja": "慢性下痢・体重減少・削痩からE. intestinalis感染を疑う。糞便PCRでEncephalitozoon intestinalisを検出。糞便の変法トリクローム染色・カルコフルオール白染色でスポアを確認。血清学的検査（IFA・ELISA）で抗体を検出するがE. cuniculiとの交差反応に注意。腸生検で腸管上皮内のスポロフォラスベシクルを確認し確定。CBC/生化学で低蛋白血症を評価。E. cuniculiとの鑑別が重要で、腸管親和性がE. intestinalisの特徴。免疫抑制状態で重症化しやすい。"
}

# 18. rabbit_enterotoxemia — Enterotoxemia / 腸管毒素血症
ENRICHMENTS["rabbit_enterotoxemia"] = {
    "diagnosis_ja": "急性の水様性〜出血性下痢・腹部膨満・急速な衰弱・突然死から腸管毒素血症を疑う。糞便グラム染色でClostridium（大型グラム陽性桿菌）の過増殖を確認。糞便培養でClostridium spiroforme・C. perfringensを同定。毒素検出（iota毒素等）で確認。CBC/生化学で脱水・代謝性アシドーシス・電解質異常を評価。X線で腸管ガス貯留・盲腸拡張を確認。ウサギは後腸発酵動物であるため盲腸内細菌叢の破綻が致死的毒素血症に直結する。食餌変更歴・抗生物質投与歴を聴取。"
}

# 19. rabbit_intestinal_coccidiosis — Intestinal Coccidiosis / 腸コクシジウム症
ENRICHMENTS["rabbit_intestinal_coccidiosis"] = {
    "diagnosis_ja": "下痢（水様性〜粘液性）・体重減少・腹部膨満・削痩から腸コクシジウム症を疑う。糞便浮遊法でEimeria属オーシスト（E. magna, E. irresidua, E. media等）を検出・形態で種同定。オーシスト排泄量の定量（McMaster法）で感染強度を評価。CBC/生化学で低蛋白血症・脱水を確認。腸管生検で粘膜上皮内のシゾントとオーシストを確認。ウサギでは肝コクシジウム症（E. stiedai）との鑑別が重要。幼若ウサギ・過密飼育・衛生不良で重症化する。"
}

# 20. rabbit_urinary_sludge — Urinary Sludge / 尿路スラッジ
ENRICHMENTS["rabbit_urinary_sludge"] = {
    "diagnosis_ja": "排尿困難・血尿・尿の白色ペースト状変化・会陰部の尿やけから尿路スラッジを疑う。X線で膀胱内の均一な高密度陰影（スラッジ）を確認（ウサギのカルシウム代謝は独特で過剰Caは腎排泄される）。超音波で膀胱内の浮遊性沈殿物を確認。尿検査で炭酸カルシウム結晶の大量沈着・比重亢進を確認。生化学でCa・BUN/Cre・SDMA を評価。食餌歴（Ca過剰摂取・アルファルファ偏重）と飲水量を聴取。鑑別に膀胱結石・膀胱炎・子宮疾患由来の血尿を考慮。"
}

# 21. rabbit_chronic_renal_failure — Chronic Renal Failure / 慢性腎不全
ENRICHMENTS["rabbit_chronic_renal_failure"] = {
    "diagnosis_ja": "多飲多尿・体重減少・食欲不振・被毛粗剛から慢性腎不全を疑う。生化学でBUN/Cre上昇・SDMA上昇・Ca/P異常を確認。尿検査で尿比重低下（等張尿）・蛋白尿を確認。超音波で腎サイズ縮小・皮髄境界不明瞭・腎石灰化を評価。X線で腎石灰化・軟部組織石灰化を確認。ウサギのCa代謝は腎依存性が高く、腎不全ではCa排泄障害と軟部組織石灰化が進行しやすい。E. cuniculi抗体検査で腎型エンセファリトゾーン症を鑑別する。"
}

# 22. rabbit_encephalitozoon_cuniculi_e._cuniculi — E. cuniculi / エンセファリトゾーン・クニクリ感染症
ENRICHMENTS["rabbit_encephalitozoon_cuniculi_e._cuniculi"] = {
    "diagnosis_ja": "斜頸・眼振・後肢不全麻痺・腎不全・水晶体破裂性ぶどう膜炎からE. cuniculi感染を疑う。血清学的検査（IFA・ELISA）でIgM（急性期）・IgG抗体価を測定。ペア血清で4倍以上の抗体価上昇が有意。尿PCRでスポア排泄を確認。頭部MRIで脳内肉芽腫性病変を評価。生化学でBUN/Cre上昇（腎型）を確認。眼科検査で水晶体前嚢破裂・レンズ誘発性ぶどう膜炎を確認（眼型）。ウサギの感染率は40-80%と高く抗体陽性のみでは確定できないため臨床症状との総合判断が必要。"
}

# 23. rabbit_rabbit_haemorrhagic_disease_rhdv_vhd — RHD / ウサギ出血病
ENRICHMENTS["rabbit_rabbit_haemorrhagic_disease_rhdv_vhd"] = {
    "diagnosis_ja": "突然死・血性鼻汁・呼吸困難・けいれん・肝腫大からRHD/VHDを疑う。確定診断はRHDV RT-PCR（肝臓・脾臓）。剖検で劇症壊死性肝炎・DIC所見（肝斑状出血・脾腫・多臓器出血）を確認。生前検査としてELISA抗体検査（ワクチン接種歴との鑑別要）。CBC/生化学でAST・ALT著増・血小板減少・凝固異常を評価。ウサギは嘔吐反射がないため消化器症状なく突然死が主訴となることが多い。RHDV1/RHDV2の型別はシークエンス解析で確認する。"
}

# 24. rabbit_rhdv2 — RHDV2 / ウサギ出血病2型
ENRICHMENTS["rabbit_rhdv2"] = {
    "diagnosis_ja": "突然死・血性鼻汁・黄疸・肝不全からRHDV2を疑う。RHDV2特異的RT-PCR（肝・脾）で確定。RHDV1との型別はシークエンス解析で確認。RHDV2はRHDV1ワクチン接種済みウサギも感染しうる点が重要。剖検で肝壊死・DIC・多臓器出血を確認。CBC/生化学でAST・ALT著増・凝固異常を評価。RHDV2は従来型より若齢ウサギへの感染力が強く、子ウサギでも発症する。ウサギは嘔吐不能のため突然死で発見されることが多い。疫学情報・ワクチン接種歴を確認。"
}

# 25. rabbit_retrobulbar_abscess — Retrobulbar Abscess / 球後膿瘍
ENRICHMENTS["rabbit_retrobulbar_abscess"] = {
    "diagnosis_ja": "片側性眼球突出・結膜充血・流涙・第三眼瞼突出から球後膿瘍を疑う。頭部X線・CTで眼窩内の膿瘍腔・上顎臼歯歯根への波及を評価。超音波で眼球後方の低エコー液体貯留を確認。FNA細胞診で乾酪様膿と変性好中球を確認。培養・感受性試験でP. multocida・Staphylococcus等を同定。CBC/生化学でヘテロフィル増多を確認。ウサギの球後膿瘍は上顎臼歯の歯根膿瘍からの波及が最も多く、口腔検査・歯科X線が不可欠。"
}

# 26. rabbit_vertebral_spondylosis — Vertebral Spondylosis / 脊椎変形性脊椎症
ENRICHMENTS["rabbit_vertebral_spondylosis"] = {
    "diagnosis_ja": "後肢の跛行・運動嫌い・背部疼痛・姿勢異常から脊椎変形性脊椎症を疑う。X線で椎体辺縁の骨棘形成・椎間板腔狭小化・終板硬化を確認。CT/MRIで脊柱管狭窄・神経根圧迫を精査。神経学的検査で後肢の固有受容感覚低下・反射異常を評価。CBC/生化学で基礎疾患を除外。E. cuniculi抗体検査で神経型エンセファリトゾーン症を鑑別。ウサギでは加齢性変化と肥満が主な素因であり、適切な体重管理が重要。鑑別に脊椎骨折・椎間板ヘルニアを考慮。"
}

# 27. rabbit_otitis_media___interna — Otitis Media / Interna / 中耳炎・内耳炎
ENRICHMENTS["rabbit_otitis_media___interna"] = {
    "diagnosis_ja": "斜頸・眼振・旋回運動・バランス喪失から中耳炎・内耳炎を疑う。頭部X線で鼓室胞の骨肥厚・液体貯留を確認。CT/MRIで中耳・内耳の詳細な評価と膿瘍の範囲を精査。耳鏡検査で鼓膜の異常（混濁・膨隆・穿孔）を確認。鼓室穿刺で膿の培養・感受性試験を実施。CBC/生化学でヘテロフィル増多を確認。ウサギではP. multocidaが最も一般的な起因菌。E. cuniculi関連前庭障害との鑑別が最重要であり、抗体検査と画像所見の組み合わせで判断する。"
}

# 28. rabbit_otitis_externa — Otitis Externa / 外耳炎
ENRICHMENTS["rabbit_otitis_externa"] = {
    "diagnosis_ja": "頭振り・耳掻き・耳道内の痂皮/分泌物・耳介発赤から外耳炎を疑う。耳鏡検査で外耳道の腫脹・分泌物・鼓膜の状態を確認。耳道スワブの細胞診でヘテロフィル・細菌・酵母を確認。培養・感受性試験で起因菌を同定。皮膚掻破検体でPsoroptes cuniculi（耳疥癬）を除外。CBC/生化学で全身性疾患を除外。ウサギでは耳疥癬が外耳炎の最も一般的な原因であり、特にロップ種は垂れ耳による換気不良で外耳炎が好発する。"
}

# 29. rabbit_hind_limb_paresis___paralysis — Hind Limb Paresis / Paralysis / 後肢不全麻痺・麻痺
ENRICHMENTS["rabbit_hind_limb_paresis___paralysis"] = {
    "diagnosis_ja": "後肢の脱力・引きずり・排尿障害・排便障害から後肢不全麻痺・麻痺を疑う。X線で脊椎骨折（特にL7・腰仙部）・椎間板疾患を確認。MRIで脊髄圧迫・脊髄病変を精査。神経学的検査で病変の局在を特定（上位/下位運動ニューロン徴候）。E. cuniculi抗体検査で神経型エンセファリトゾーン症を評価。CBC/生化学で代謝性疾患を除外。ウサギでは保定時のパニックによる脊椎骨折が最も多い原因。鑑別にE. cuniculi・脊椎変形症・腎腫大による神経圧迫を考慮。"
}

# 30. rabbit_atherosclerosis — Atherosclerosis / 動脈硬化症
ENRICHMENTS["rabbit_atherosclerosis"] = {
    "diagnosis_ja": "沈鬱・運動不耐性・突然死から動脈硬化症を疑う。生化学で高コレステロール血症・高トリグリセリド血症を確認。超音波で大動脈壁肥厚・プラークを検出。X線で大動脈石灰化を確認。心エコーで心機能評価。剖検で大動脈内膜のアテローム性プラーク・石灰化・管腔狭窄を確認し確定。ウサギは実験的にコレステロール食で容易に動脈硬化を発症するモデル動物であり、高脂肪食・運動不足が主要リスク因子。鑑別にCa代謝異常による血管石灰化を考慮。"
}

# 31. rabbit_encephalitozoonosis_-_renal_form — Encephalitozoonosis - Renal Form / エンセファリトゾーン症（腎型）
ENRICHMENTS["rabbit_encephalitozoonosis_-_renal_form"] = {
    "diagnosis_ja": "多飲多尿・体重減少・腎不全所見からE. cuniculi腎型を疑う。血清学的検査（IFA・ELISA）でIgM/IgG抗体価を測定。尿PCRでE. cuniculiスポアを検出。生化学でBUN/Cre上昇・SDMA上昇を確認。超音波で腎の瘢痕化・腎縮小・表面不整を確認。尿検査で蛋白尿・円柱を確認。腎生検で肉芽腫性間質性腎炎とスポアを確認し確定。ウサギのE. cuniculi感染の腎型は慢性経過で進行し、終末期に腎不全として顕在化することが多い。"
}

# 32. rabbit_viral_papillomatosis — Viral Papillomatosis / ウイルス性乳頭腫症
ENRICHMENTS["rabbit_viral_papillomatosis"] = {
    "diagnosis_ja": "皮膚・粘膜のカリフラワー状腫瘤・疣贅状病変からウイルス性乳頭腫症を疑う。組織生検でパピローマウイルスの好酸性核内封入体を含む扁平上皮の乳頭腫性増殖を確認。PCRでウサギパピローマウイルス（CRPV/ROPV）を検出。病理組織検査で悪性転化（扁平上皮癌への移行：基底膜浸潤・角化異常）の有無を評価。CBC/生化学は通常正常。ワタオウサギ由来CRPVは実験的発癌モデルとして知られるが、家兎でも乳頭腫の悪性転化が報告されている。"
}

# 33. rabbit_urine_scald — Urine Scald / 尿やけ（尿性皮膚炎）
ENRICHMENTS["rabbit_urine_scald"] = {
    "diagnosis_ja": "会陰部・後肢内側・腹部の発赤・湿性皮膚炎・脱毛・痂皮から尿やけを疑う。身体検査で皮膚病変の範囲と二次感染を評価。尿検査で尿路感染・尿路スラッジを除外。X線で膀胱結石・尿路スラッジを確認。生化学でBUN/Cre・Caを評価し腎疾患を除外。基礎疾患の検索が重要で、排尿障害の原因（肥満・関節疾患・脊椎疾患・尿路疾患）を鑑別。ウサギは炭酸カルシウム尿（正常でも白濁）であるが、スラッジ蓄積による排尿困難が尿やけの素因となる。"
}

# 34. rabbit_nephrolithiasis_kidney_stones — Nephrolithiasis / 腎結石症
ENRICHMENTS["rabbit_nephrolithiasis_kidney_stones"] = {
    "diagnosis_ja": "血尿・排尿困難・腰部疼痛・食欲不振から腎結石症を疑う。X線で腎シルエット内の高密度結石影を確認（ウサギの結石は炭酸カルシウムが主成分で高X線透過性）。超音波で腎盂拡張・結石の部位/サイズ・水腎症を評価。尿検査で血尿・蛋白尿・結晶を確認。生化学でBUN/Cre・Ca・Pを評価。CT検査で結石の詳細な位置/数量を精査。ウサギのCa代謝は腎依存性が高く、Ca過剰食（アルファルファ偏重）が結石形成の主因。飲水量不足も重要なリスク因子。"
}

# 35. rabbit_cystitis — Cystitis / 膀胱炎
ENRICHMENTS["rabbit_cystitis"] = {
    "diagnosis_ja": "頻尿・排尿困難・血尿・尿失禁から膀胱炎を疑う。尿検査（カテーテルまたは膀胱穿刺採取）で膿尿・細菌尿・血尿を確認。尿培養・感受性試験でE. coli・P. multocida等を同定。超音波で膀胱壁肥厚・膀胱内沈殿物（スラッジ）を確認。X線で膀胱結石を除外。CBC/生化学で全身性感染・腎機能を評価。ウサギのカルシウム含有量の高い尿は結晶沈着→膀胱刺激→二次感染の悪循環を起こしやすい。鑑別に子宮疾患由来の血尿・尿路スラッジを考慮。"
}

# 36. rabbit_red_urine_non-pathological — Red Urine (Non-pathological) / 赤色尿（非病的）
ENRICHMENTS["rabbit_red_urine_non-pathological"] = {
    "diagnosis_ja": "赤色〜オレンジ色の尿排泄で飼い主が血尿を心配して来院。尿試験紙でヘモグロビン・潜血が陰性であることを確認し、真の血尿を除外。尿沈渣で赤血球の有無を顕微鏡的に確認。ウサギの尿はポルフィリン色素を含むため正常でも赤色〜オレンジ色を呈する。食餌内容（β-カロテン含有食品：にんじん・ビーツ等）を聴取。CBC/生化学・超音波で子宮疾患・膀胱疾患を念のため除外。赤色尿は通常1-3日で自然消退する。ウサギ特有の生理的現象であることを飼い主に説明。"
}

# 37. rabbit_nasal_polyps — Nasal Polyps / 鼻腔ポリープ
ENRICHMENTS["rabbit_nasal_polyps"] = {
    "diagnosis_ja": "慢性くしゃみ・鼻汁（漿液性〜膿性）・呼吸困難・鼻閉から鼻腔ポリープを疑う。鼻腔内視鏡で鼻腔内のポリープ状腫瘤を直視下確認。CT検査で鼻腔内の軟部組織腫瘤・鼻甲介の変形・副鼻腔への波及を精査。組織生検で炎症性ポリープ（粘膜固有層の浮腫・炎症細胞浸潤）と腫瘍を鑑別。培養で二次感染菌を同定。CBC/生化学でヘテロフィル増多を評価。ウサギは絶対的経鼻呼吸動物であるため鼻腔閉塞は呼吸困難に直結し、重篤度が高い。"
}

# 38. rabbit_pulmonary_abscess — Pulmonary Abscess / 肺膿瘍
ENRICHMENTS["rabbit_pulmonary_abscess"] = {
    "diagnosis_ja": "呼吸困難・鼻汁・沈鬱・体重減少から肺膿瘍を疑う。X線で肺野の結節状〜嚢胞状陰影を確認。CT検査で膿瘍の部位・大きさ・多発性を精査。気管洗浄液の培養・感受性試験でP. multocida・Staphylococcus等を同定。細胞診でヘテロフィル浸潤と変性好中球を確認。CBC/生化学でヘテロフィル著増・フィブリノーゲン上昇を評価。ウサギではP. multocida（スナッフル起因菌）による鼻腔・副鼻腔感染の肺への波及が最も一般的な原因。ウサギの膿瘍は乾酪様で排膿困難。"
}

# 39. rabbit_torticollis_wry_neck — Torticollis (Wry Neck) / 斜頸
ENRICHMENTS["rabbit_torticollis_wry_neck"] = {
    "diagnosis_ja": "頭部の持続的傾斜・眼振・旋回運動・転倒から斜頸を疑う。頭部X線で鼓室胞の異常（骨肥厚・液体貯留：中耳炎）を確認。CT/MRIで中耳・内耳・脳幹病変を精査。E. cuniculi抗体検査（IgM/IgG）で急性エンセファリトゾーン症を評価。神経学的検査で末梢性（中耳/内耳）vs 中枢性（脳幹）前庭障害を鑑別。CBC/生化学で全身性疾患を除外。ウサギの斜頸の二大原因はE. cuniculi（中枢性）とP. multocida中耳炎（末梢性）であり、治療方針が異なるため鑑別が重要。"
}

# 40. rabbit_antibiotic-associated_enterotoxemia — Antibiotic-Associated Enterotoxemia / 抗生物質関連腸管毒素血症
ENRICHMENTS["rabbit_antibiotic-associated_enterotoxemia"] = {
    "diagnosis_ja": "特定の抗生物質投与後の急性水様性下痢・腹部膨満・ガス貯留・急速な衰弱から抗生物質関連腸管毒素血症を疑う。投与薬歴の聴取が最重要で、ペニシリン系（経口）・リンコマイシン・クリンダマイシン・エリスロマイシンが原因となる。糞便グラム染色でClostridium過増殖を確認。毒素検出で確定。CBC/生化学で脱水・アシドーシスを評価。X線で盲腸拡張を確認。ウサギの後腸発酵に依存する盲腸細菌叢が破壊され致死的Clostridium毒素血症が発生する。致死率が極めて高い。"
}

# 41. rabbit_hypercalcaemia — Hypercalcaemia / 高カルシウム血症
ENRICHMENTS["rabbit_hypercalcaemia"] = {
    "diagnosis_ja": "多飲多尿・尿路スラッジ・食欲不振・沈鬱から高Ca血症を疑う。生化学でCa（総Ca・イオン化Ca）上昇を確認。尿検査でCa結晶の著増を確認。X線で軟部組織石灰化・腎石灰化・尿路スラッジを評価。PTH測定で上皮小体機能亢進症を除外。超音波で腎石灰化・膀胱スラッジを確認。ウサギのCa代謝は腎排泄依存であり、食餌中Ca量が直接血中Caに反映される独特の生理学を持つ。食餌歴（アルファルファ・Ca含有ペレットの過剰摂取）の聴取が重要。"
}

# 42. rabbit_pericarditis — Pericarditis / 心膜炎
ENRICHMENTS["rabbit_pericarditis"] = {
    "diagnosis_ja": "呼吸困難・運動不耐性・頸静脈怒張・沈鬱から心膜炎を疑う。聴診で心音減弱・摩擦音を検出。X線で心陰影のグローブ状拡大を確認。超音波心臓検査で心嚢液貯留・心嚢膜肥厚を確認。心嚢穿刺で液体を採取し細胞診・培養・生化学を実施。CBC/生化学でヘテロフィル増多・炎症マーカー上昇を評価。心電図でlow voltage・電気的交互脈を確認。ウサギではP. multocidaによる血行性播種が心膜炎の原因となることがある。鑑別に胸水・心筋症を考慮。"
}

# 43. rabbit_ear_haematoma_aural_haematoma — Ear Haematoma / 耳血腫
ENRICHMENTS["rabbit_ear_haematoma_aural_haematoma"] = {
    "diagnosis_ja": "耳介の波動性腫脹・熱感・疼痛から耳血腫を疑う。触診で液体貯留（血液・漿液）を確認。FNA細胞診で血液成分と炎症細胞を確認し膿瘍・腫瘍を除外。耳鏡検査で外耳炎・耳疥癬（Psoroptes cuniculi）を確認し基礎疾患を評価。皮膚掻破検体でダニを除外。CBC/生化学で凝固異常を確認。ウサギの耳血腫は耳掻き・頭振り（耳疥癬等による掻痒が原因）に伴う耳介軟骨の血管損傷で発生する。ロップ種では耳介重量が素因。"
}

# 44. rabbit_snuffles_-_chronic — Snuffles - Chronic / 慢性スナッフル
ENRICHMENTS["rabbit_snuffles_-_chronic"] = {
    "diagnosis_ja": "慢性くしゃみ・膿性鼻汁・前肢内側の汚れ（鼻汁拭い跡）から慢性スナッフルを疑う。鼻腔スワブの培養・感受性試験でP. multocidaを同定。PCRで確認。頭部X線・CTで副鼻腔の液体貯留・骨変化を評価。鼻腔内視鏡で粘膜の炎症・腫脹・ポリープを確認。CBC/生化学でヘテロフィル増多を評価。ウサギは絶対的経鼻呼吸動物であるため慢性鼻閉は深刻な問題。P. multocidaは根絶が困難でストレス・免疫低下時に再燃する。"
}

# 45. rabbit_basal_cell_tumour — Basal Cell Tumour / 基底細胞腫
ENRICHMENTS["rabbit_basal_cell_tumour"] = {
    "diagnosis_ja": "皮膚の孤立性結節状腫瘤（通常頭部・頸部に好発）から基底細胞腫を疑う。FNA細胞診で小型均一な基底様細胞のクラスターを確認。組織生検で確定し組織亜型（充実型・嚢胞型等）を分類。CBC/生化学で全身状態を評価。X線・超音波で転移の有無を精査（通常は良性で転移稀）。ウサギでは皮膚腫瘍の中で比較的多く報告されており、外科的完全切除で予後良好。鑑別に毛包腫瘍・膿瘍・脂肪腫・肥満細胞腫を考慮する。"
}

# 46. rabbit_adrenal_disease — Adrenal Disease / 副腎疾患
ENRICHMENTS["rabbit_adrenal_disease"] = {
    "diagnosis_ja": "多飲多尿・脱毛・攻撃性変化・外陰部腫大（雌）から副腎疾患を疑う。コルチゾール基礎値とACTH刺激試験で副腎皮質機能を評価。超音波で副腎のサイズ・形態（腫大・結節）を確認。性ホルモン（エストラジオール・テストステロン・17-OHプロゲステロン）パネルを評価。CT検査で副腎腫瘤と周囲浸潤を精査。CBC/生化学で電解質異常・肝酵素異常を確認。ウサギの副腎疾患はフェレットほど頻度は高くないが、避妊/去勢済み個体での性ホルモン異常上昇は副腎原性を疑う。"
}

# 47. rabbit_hypoglycaemia — Hypoglycaemia / 低血糖症
ENRICHMENTS["rabbit_hypoglycaemia"] = {
    "diagnosis_ja": "沈鬱・虚脱・振戦・けいれん・低体温から低血糖症を疑う。血糖値測定で低血糖（<60 mg/dL）を確認。生化学で肝機能（ALT・胆汁酸）・腎機能を評価。インスリン/血糖比の測定でインスリノーマを除外。肝超音波で肝腫瘤・肝萎縮を確認。CBC/生化学で敗血症マーカーを評価。ウサギでは長時間の絶食（特に術前絶食を長くしすぎた場合）が低血糖の主因。後腸発酵動物であるため盲腸機能維持に持続的エネルギー供給が必要で、12時間以上の絶食は避ける。"
}

# 48. rabbit_retained_foetus — Retained Foetus / 胎仔遺残
ENRICHMENTS["rabbit_retained_foetus"] = {
    "diagnosis_ja": "分娩後の持続的腹部膨満・悪露異常・食欲不振・沈鬱から胎仔遺残を疑う。X線で子宮内の胎仔骨格陰影を確認。超音波で子宮内容（生存/死亡胎仔・液体貯留）を評価。CBC/生化学でヘテロフィル増多・肝酵素上昇（敗血症進行時）を確認。バイタルサインで発熱・脱水を評価。分娩歴の詳細聴取（分娩開始からの時間・既産仔数）が重要。ウサギの妊娠期間は30-33日で、正常分娩は通常30分以内に完了する。胎仔遺残は敗血症・子宮破裂に進展しうる緊急疾患。"
}

# 49. rabbit_ketoacidosis — Ketoacidosis / ケトアシドーシス
ENRICHMENTS["rabbit_ketoacidosis"] = {
    "diagnosis_ja": "沈鬱・食欲不振・脱水・アセトン臭・急速な衰弱からケトアシドーシスを疑う。血液ガス分析で代謝性アシドーシス（pH低下・HCO3-低下）を確認。尿検査でケトン体陽性を確認。血糖値測定で高血糖・低血糖を評価。生化学でBUN/Cre上昇・電解質異常（K変動）を確認。CBC/生化学で基礎疾患（肝リピドーシス・妊娠中毒症）を評価。ウサギではmまなし妊娠末期（妊娠中毒症）・肥満・長時間絶食が主因。後腸発酵動物のため絶食による急速な脂肪動員が起こりやすい。"
}

# 50. rabbit_septicaemia — Septicaemia / 敗血症
ENRICHMENTS["rabbit_septicaemia"] = {
    "diagnosis_ja": "発熱（>40°C）・沈鬱・食欲廃絶・頻呼吸・蒼白粘膜から敗血症を疑う。血液培養で起因菌を同定（P. multocida・E. coli・Staphylococcus等）。CBC/生化学でヘテロフィル著増（左方移動）・低血糖・乳酸上昇・肝腎障害を評価。凝固検査でDIC合併を確認。血液ガスで代謝性アシドーシスを評価。原発巣の検索（子宮蓄膿症・肺膿瘍・歯根膿瘍・腸管感染）が治療方針決定に不可欠。ウサギではP. multocidaが最も一般的な敗血症起因菌であり、慢性保菌からの急性増悪に注意。"
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
