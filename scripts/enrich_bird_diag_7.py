#!/usr/bin/env python3
"""Enrich Bird diagnosis_ja — batch 7 (entries 51-100 of 233 remaining)."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 51. bird_0301 — Hematological Nutritional Deficiency
ENRICHMENTS["bird_0301"] = {
    "diagnosis_ja": "CBC（採血量≤体重の1%）でPCV低下・赤血球形態異常（小球性低色素性→Fe欠乏、大球性→VitB12/葉酸欠乏）を評価。血液生化学でFe・TIBC・フェリチンを測定。食餌歴の詳細聴取（種子食偏重によるFe・VitE・VitK欠乏リスク）。凝固検査でVitK欠乏性凝固障害を除外。末梢血塗抹で赤血球形態異常を確認。鳥類の有核赤血球はMCV測定が哺乳類と異なるため、形態学的評価が重要。VitE欠乏は白筋病・脳軟化症と貧血を同時に惹起する"
}

# 52. bird_0302 — Reproductive Bacterial Infection
ENRICHMENTS["bird_0302"] = {
    "diagnosis_ja": "排泄腔スワブの細菌培養・感受性試験で起炎菌（E. coli・Klebsiella・Salmonella等）を同定。腹部X線・超音波で卵管腫脹・腹腔内液体貯留・卵殻異常を評価。CBC（採血量≤体重の1%）でヘテロフィル著増・H/L比上昇を確認。血液生化学でCa・TP・AST・UA上昇を測定。触診で卵管腫大・腹腔内腫瘤を確認。鳥類では卵管炎（salpingitis）がE. coli上行感染で多発し、卵黄性腹膜炎（egg yolk peritonitis）への進展が致死的となりうる"
}

# 53. bird_0303 — Reproductive Viral Infection
ENRICHMENTS["bird_0303"] = {
    "diagnosis_ja": "産卵異常・不妊・卵殻品質低下の臨床評価。PCR検査でウイルス（Polyomavirus・Herpesvirus・EDS-76 Adenovirus等）を検出。血清学的検査で抗体価を測定。CBC（採血量≤体重の1%）でリンパ球変動を確認。腹部超音波で卵巣・卵管の形態異常を評価。病理組織検査（生検/剖検）で卵管・卵巣のウイルス性変化を確認。鳥類ではPolyomavirus感染が幼鳥の急性死と成鳥の繁殖障害を引き起こし、羽毛異常も伴うことがある"
}

# 54. bird_0304 — Reproductive Metabolic Disease
ENRICHMENTS["bird_0304"] = {
    "diagnosis_ja": "血液生化学（採血量≤体重の1%）でCa（産卵関連低Ca血症→正常8-12 mg/dL、低Ca<8 mg/dL）・P・TP・グルコースを測定。ホルモン検査（エストロゲン・プロゲステロン）で生殖内分泌を評価。腹部X線で多骨性骨過形成症（産卵活発時の骨髄骨形成）・卵殻石灰化不全を確認。超音波で卵胞活動を評価。鳥類の産卵関連低Ca血症は重篤な筋力低下・痙攣・卵つまりを惹起し、緊急治療を要する。慢性産卵鳥では骨枯渇→病的骨折のリスクが高い"
}

# 55. bird_0305 — Reproductive Congenital Anomaly
ENRICHMENTS["bird_0305"] = {
    "diagnosis_ja": "繁殖不能・異常産卵パターンの経過確認。腹部超音波・X線で卵巣・卵管の構造異常（欠損・低形成・嚢胞性変化）を評価。排泄腔の視診で総排泄腔異常を確認。CBC・血液生化学（採血量≤体重の1%）で全身状態を評価。ホルモン検査で性腺機能を確認。鳥類では通常左卵巣のみが機能的に発達し、右卵巣は退化するが、稀に両側発達や精巣卵巣（ovotestis）の報告がある。遺伝的性判定にはPCR性別鑑定（CHD遺伝子）が有用"
}

# 56. bird_0306 — Reproductive Inflammatory Disease
ENRICHMENTS["bird_0306"] = {
    "diagnosis_ja": "排泄腔の視診で分泌物・腫脹を確認。腹部超音波で卵管壁肥厚・卵管内液体貯留・卵巣周囲炎を評価。X線で腹腔内液体貯留・軟部組織腫瘤を確認。CBC（採血量≤体重の1%）でヘテロフィル増加・H/L比上昇を確認。血液生化学でTP上昇（腹膜炎）・AST・UA変動を測定。腹水穿刺液の細胞診・培養で卵黄性腹膜炎を確定。鳥類の卵管炎は排泄腔からの上行感染が主因で、卵黄の体腔内遊離により重篤な体腔炎に進展する"
}

# 57. bird_0307 — Systemic Bacterial Infection
ENRICHMENTS["bird_0307"] = {
    "diagnosis_ja": "全身状態の評価（沈鬱・膨羽・食欲廃絶・体重減少）。CBC（採血量≤体重の1%）でヘテロフィル著増（>12,000/μL）・H/L比上昇・単球増多を確認。血液培養で菌血症/敗血症を証明。血液生化学でAST・LDH・UA・グルコース変動を測定。全身X線・超音波で多臓器病変（肝腫大・脾腫・気嚢混濁）を評価。培養・感受性試験で起炎菌同定。鳥類は高代謝率のため敗血症の進行が急速で、Gram陰性菌（E. coli・Pseudomonas）による内毒素ショックが急性死の主因"
}

# 58. bird_0308 — Systemic Viral Infection
ENRICHMENTS["bird_0308"] = {
    "diagnosis_ja": "全身状態の評価（沈鬱・膨羽・食欲廃絶・急激な体重減少）。CBC（採血量≤体重の1%）でリンパ球減少（免疫抑制）・ヘテロフィル変動を確認。PCR検査で特定ウイルス（Polyomavirus・Circovirus・ABV・Paramyxovirus等）を検出。血清学的検査で抗体価を測定。全身X線で多臓器病変を評価。血液生化学でAST・LDH・TP変動を測定。鳥類の全身性ウイルス感染は免疫抑制を伴うことが多く、二次的細菌感染・真菌感染の合併リスクが高い"
}

# 59. bird_avian_poxvirus — Avian Poxvirus
ENRICHMENTS["bird_avian_poxvirus"] = {
    "diagnosis_ja": "皮膚型：嘴基部・眼周囲・脚の皮膚に痘疹性結節・痂皮を視診で確認。湿型（粘膜型）：口腔・咽頭のジフテリア様偽膜を観察。病変部の組織生検・病理組織検査でBollinger小体（細胞質内封入体）を確認。PCR検査でPoxvirus DNAを検出。電子顕微鏡でPoxウイルス粒子を同定。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。鳥類のPoxvirusは媒介昆虫（蚊等）による伝播が主で、皮膚型は予後良好だが粘膜型は上気道閉塞により重篤化する"
}

# 60. bird_mycoplasmosis — Mycoplasmosis
ENRICHMENTS["bird_mycoplasmosis"] = {
    "diagnosis_ja": "臨床症状の評価（副鼻腔腫脹・結膜炎・鼻汁・くしゃみ・呼吸困難）。Mycoplasma gallisepticum/synoviae特異的PCR検査（鼻腔・副鼻腔スワブ）で病原体を検出。血清学検査（急速凝集試験・HI試験・ELISA）で抗体価を測定。副鼻腔X線で副鼻腔内液体貯留を評価。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。培養はPPLO培地で可能だが成長遅く2-4週間。鳥類のMycoplasmosis は家禽・野鳥で世界的に重要な呼吸器感染症で、慢性化・保菌鳥化しやすい"
}

# 61. bird_streptococcal_infection — Streptococcal Infection
ENRICHMENTS["bird_streptococcal_infection"] = {
    "diagnosis_ja": "臨床症状の評価（沈鬱・膨羽・関節腫脹・神経症状・突然死）。病変部・血液の細菌培養でStreptococcus属（S. zooepidemicus・S. gallolyticus等）を分離同定。感受性試験で抗菌薬選択。CBC（採血量≤体重の1%）でヘテロフィル著増・H/L比上昇を確認。血液生化学でAST・LDH・CK上昇を測定。関節液分析でヘテロフィル浸潤・細菌を確認。鳥類ではStreptococcus感染は急性敗血症型と慢性関節炎型があり、ストレス（環境変化・過密飼育）が発症誘因"
}

# 62. bird_citrobacter_infection — Citrobacter Infection
ENRICHMENTS["bird_citrobacter_infection"] = {
    "diagnosis_ja": "臨床症状の評価（下痢・沈鬱・膨羽・突然死：特に幼鳥で重篤）。糞便・排泄腔スワブの細菌培養でCitrobacter属を分離同定。感受性試験で抗菌薬を選択（多剤耐性に注意）。CBC（採血量≤体重の1%）でヘテロフィル増加・H/L比上昇を確認。血液生化学でAST・LDH上昇を測定。剖検例では肝壊死巣・脾腫を確認。鳥類ではCitrobacter freundiiによる幼鳥の敗血症が報告されており、免疫未熟な雛鳥での致死率が高い。衛生環境の評価も重要"
}

# 63. bird_tracheal_obstruction — Tracheal Obstruction
ENRICHMENTS["bird_tracheal_obstruction"] = {
    "diagnosis_ja": "吸気性喘鳴・開口呼吸・呼吸努力増大の臨床評価。頸部・胸部X線（VD・lateral）で気管内異物・腫瘤・外圧性狭窄を確認。透視検査で呼吸相による気管動態を観察。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。硬性内視鏡で気管内腔を直視し閉塞原因（異物・肉芽・腫瘤・Syngamus虫体）を確認。血液ガス分析で低酸素血症の程度を判定。鳥類の気管は完全気管輪で構成され拡張性がないため、50%以上の内腔狭窄で著明な呼吸困難を呈する"
}

# 64. bird_crop_foreign_body — Crop Foreign Body
ENRICHMENTS["bird_crop_foreign_body"] = {
    "diagnosis_ja": "そのう（crop）の触診で異物の存在・硬さ・サイズを確認。頸部X線（VD・lateral）で金属異物・不透過性異物を検出。造影X線（バリウム/ヨード造影剤）で非不透過性異物の輪郭を描出。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でTP・グルコースを測定（栄養障害の評価）。内視鏡検査でそのう内腔を直視し異物を確認。鳥類のそのうは食道拡張部で容量が大きく、布片・金属片・種子塊等の蓄積が発生する。嘔吐歴の聴取も重要"
}

# 65. bird_ingluvitis_crop_infection — Ingluvitis (Crop Infection)
ENRICHMENTS["bird_ingluvitis_crop_infection"] = {
    "diagnosis_ja": "そのう（crop）の触診でガス貯留・液体貯留・壁肥厚を評価。そのう洗浄液のグラム染色・KOH直接鏡検でCandida酵母体・細菌を検索。細菌・真菌培養で起炎微生物を同定。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。X線でそのう拡張・ガス貯留を評価。血液生化学でTP・グルコースを測定。鳥類のそのう炎はCandida albicansによるカンジダ症が最多で、特に手餌育雛・抗生物質長期投与・ビタミンA欠乏で好発。pH測定も有用（正常pH 5-6）"
}

# 66. bird_gastrointestinal_foreign_body — Gastrointestinal Foreign Body
ENRICHMENTS["bird_gastrointestinal_foreign_body"] = {
    "diagnosis_ja": "腹部X線（VD・lateral）で金属異物・不透過性異物・消化管拡張を評価。造影X線で通過障害・異物の位置を特定。腹部超音波で消化管壁肥厚・蠕動異常を確認。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でグルコース低下（栄養障害）・AST上昇・UA変動を測定。内視鏡で前胃（proventriculus）・筋胃（ventriculus）内異物を直視確認。鳥類の筋胃は強力な筋肉壁で異物を破砕・圧縮するが、金属片（鉛・亜鉛）は中毒を惹起する"
}

# 67. bird_aflatoxicosis — Aflatoxicosis
ENRICHMENTS["bird_aflatoxicosis"] = {
    "diagnosis_ja": "飼料のアフラトキシン汚染歴の聴取（湿潤環境で保管されたトウモロコシ・落花生が高リスク）。血液生化学（採血量≤体重の1%）で肝酵素（AST・GGT）著増・胆汁酸上昇・TP/アルブミン低下・凝固時間延長を確認。CBC で貧血・白血球減少を評価。腹部超音波・X線で肝腫大・脂肪肝を描出。肝生検・病理組織検査で胆管過形成・脂肪変性・壊死を確認。飼料のアフラトキシン定量検査。鳥類はアフラトキシンに高感受性で、特にアヒル・七面鳥の感受性が極めて高い"
}

# 68. bird_hepatic_amyloidosis — Hepatic Amyloidosis
ENRICHMENTS["bird_hepatic_amyloidosis"] = {
    "diagnosis_ja": "血液生化学（採血量≤体重の1%）で肝酵素（AST・LDH）上昇・TP/アルブミン低下・胆汁酸上昇を確認。腹部超音波で肝腫大・均一な高エコー実質を描出。X線で肝陰影拡大を評価。肝FNA細胞診・生検でコンゴーレッド染色陽性のアミロイド沈着を確認（偏光顕微鏡でapple-green偏光）。CBC で慢性変化を評価。鳥類ではアヒル・ガチョウ等の水禽類に肝アミロイドーシスが多発し、慢性炎症（足底皮膚炎等）が続発性AA型アミロイドの誘因"
}

# 69. bird_articular_gout — Articular Gout
ENRICHMENTS["bird_articular_gout"] = {
    "diagnosis_ja": "関節の視診・触診で腫脹・白色結節（tophi）・疼痛を確認。関節穿刺液の偏光顕微鏡検査で針状尿酸ナトリウム結晶（負の複屈折）を検出。血液生化学（採血量≤体重の1%）でUA著増（正常2-10 mg/dL、痛風>15 mg/dL）・BUN上昇を確認。X線で関節周囲の軟部組織腫脹・�ite erosionを評価。腎機能検査（UA・BUN）で腎不全を評価。鳥類は尿酸排泄型であり、腎機能低下→尿酸蓄積→痛風の病態が哺乳類より発生しやすい"
}

# 70. bird_visceral_gout — Visceral Gout
ENRICHMENTS["bird_visceral_gout"] = {
    "diagnosis_ja": "急性沈鬱・膨羽・食欲廃絶の臨床評価。血液生化学（採血量≤体重の1%）でUA著増（>20 mg/dLで強く疑う）・BUN上昇・K上昇を確認。腹部超音波で腎腫大・高エコー実質・漿膜面の白色沈着を描出。X線で腎陰影拡大を評価。CBC でヘテロフィル変動を確認。体腔穿刺液の分析で尿酸結晶を検出。鳥類の内臓痛風は急性腎不全の終末像として発生し、心外膜・肝被膜・気嚢・腎表面に白色尿酸塩沈着が広がる。脱水・腎毒性薬剤・高蛋白食が主要リスク因子"
}

# 71. bird_nephritis — Nephritis
ENRICHMENTS["bird_nephritis"] = {
    "diagnosis_ja": "多尿・尿酸排泄変化（水様尿・尿酸色調異常）の臨床評価。血液生化学（採血量≤体重の1%）でUA上昇・BUN上昇・K・Ca・Pの電解質異常を測定。CBC でヘテロフィル増加（感染性腎炎）を確認。腹部超音波で腎腫大・実質エコー異常を描出。X線で腎陰影拡大を評価。尿沈渣検査で細胞・円柱・結晶を評価。培養・PCRで感染性原因（E. coli・Polyomavirus・腎炎ウイルス等）を検索。鳥類の腎臓は腰仙部に固定され、3葉構造で腎門脈系を有する特殊な解剖学的特徴がある"
}

# 72. bird_malnutrition___cachexia — Malnutrition / Cachexia
ENRICHMENTS["bird_malnutrition___cachexia"] = {
    "diagnosis_ja": "体重測定・BCS評価（胸筋触診で竜骨突出の程度を4段階スコアリング）。食餌歴の詳細聴取（種子食偏重・偏食・食事量不足）。血液生化学（採血量≤体重の1%）でTP/アルブミン低下・グルコース低下・AST上昇を測定。CBC で貧血・白血球変動を評価。全身X線で骨密度低下・臓器萎縮を確認。糞便検査で消化管寄生虫を除外。基礎疾患のスクリーニング（慢性感染・腫瘍・消化管疾患）。鳥類は高代謝率のため体脂肪消費が急速で、24-48時間の絶食で低血糖・肝リピドーシスに陥る"
}

# 73. bird_vitamin_e___selenium_deficiency — Vitamin E / Selenium Deficiency
ENRICHMENTS["bird_vitamin_e___selenium_deficiency"] = {
    "diagnosis_ja": "食餌歴の詳細聴取（酸化した種子・古い飼料・VitE/Se無添加食）。神経学的検査で運動失調・頭部振戦・脚麻痺（白筋病）を評価。血液生化学（採血量≤体重の1%）でCK著増（筋障害マーカー）・AST上昇を確認。血漿VitE（α-トコフェロール）測定（<2 μg/mLで欠乏）。全血Se測定。X線で筋胃壁石灰化（white muscle disease）を検索。病理組織検査で脳軟化症・筋変性・心筋壊死を確認。鳥類ではVitE欠乏は脳軟化症（encephalomalacia）として神経症状が前面に出る"
}

# 74. bird_folliculitis — Folliculitis
ENRICHMENTS["bird_folliculitis"] = {
    "diagnosis_ja": "皮膚・羽毛濾胞の視診で発赤・腫脹・膿疱・痂皮形成を確認。罹患濾胞のFNA細胞診でヘテロフィル浸潤・細菌を検索。細菌培養・感受性試験で起炎菌（Staphylococcus・Pseudomonas等）を同定。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。血液生化学でTP・AST変動を測定。皮膚生検・病理組織検査で濾胞周囲炎・濾胞破壊を評価。鳥類の羽毛濾胞は皮膚深層に位置し、感染が深部に波及すると羽毛嚢胞・蜂窩織炎に進展する"
}

# 75. bird_splay_leg_spraddle_leg — Splay Leg (Spraddle Leg)
ENRICHMENTS["bird_splay_leg_spraddle_leg"] = {
    "diagnosis_ja": "幼鳥の視診で両脚の外側偏位・起立不能を確認。X線検査で股関節・大腿骨頭の位置異常・骨変形を評価。腱の触診で腓腹筋腱の脱臼を確認。CBC・血液生化学（採血量≤体重の1%）で栄養状態を評価（Ca・P・VitD3）。巣材・育雛環境の聴取（滑りやすい底材が最大の発症因子）。親鳥の栄養状態評価。鳥類のsplay legは孵化直後の脚固定（テーピング）で矯正可能だが、発見が遅れると永続的変形となる。栄養性MBDの合併も確認する"
}

# 76. bird_osteoporosis — Osteoporosis
ENRICHMENTS["bird_osteoporosis"] = {
    "diagnosis_ja": "全身X線で骨密度低下・皮質菲薄化・含気骨の過度な透過性を評価。血液生化学（採血量≤体重の1%）でCa・P・ALP・VitD3を測定。竜骨・脛足根骨の触診で骨軟化・変形を確認。食餌歴の詳細聴取（Ca:P比・UVB曝露・種子食偏重）。産卵歴の確認（慢性産卵による骨ミネラル枯渇）。鳥類は含気骨構造のため骨密度の画像評価が哺乳類より困難で、皮質の菲薄化と病的骨折が診断の手がかりとなる。産卵鳥では骨髄骨の形成と消費のバランスを評価する"
}

# 77. bird_pdd_neurological_form — PDD Neurological Form
ENRICHMENTS["bird_pdd_neurological_form"] = {
    "diagnosis_ja": "神経学的検査で運動失調・頭部振戦・痙攣・失明・固有受容覚障害を系統的に評価。ABV（Avian Bornavirus/PaBV）PCR検査（排泄腔スワブ・血液）でウイルスを検出。抗PaBV抗体（ELISA/IFA）の測定。CBC（採血量≤体重の1%）でリンパ球変動を評価。そのう生検で筋層間神経叢のリンパ球性神経節神経炎を確認（感度約60-70%）。頭部CT/MRIで脳実質変化を検索。鳥類のPDD神経型は大型オウム目に好発し、消化管型症状なしに神経症状のみで発症することがある"
}

# 78. bird_head_trauma — Head Trauma
ENRICHMENTS["bird_head_trauma"] = {
    "diagnosis_ja": "外傷歴の聴取（窓・鏡への衝突、落下、他動物による攻撃）。意識レベルの評価（正常・沈鬱・昏迷・昏睡の段階分類）。神経学的検査で瞳孔反射・眼球運動・脳神経機能・姿勢反射を系統的に評価。頭部X線で頭蓋骨折を検索。CT検査で頭蓋内出血・脳浮腫を評価。CBC（採血量≤体重の1%）でPCV低下（出血）を確認。血液生化学でCK・AST・グルコースを測定。鳥類の頭蓋は含気骨構造で衝撃緩衝効果があるが、小型種では軽微な衝突でも脳震盪を起こしうる"
}

# 79. bird_seizure_disorder — Seizure Disorder
ENRICHMENTS["bird_seizure_disorder"] = {
    "diagnosis_ja": "発作の詳細な病歴聴取（発作型・持続時間・頻度・誘発因子）。神経学的検査で発作間欠期の異常を評価。血液生化学（採血量≤体重の1%）で代謝性原因を除外（低Ca・低血糖・肝性脳症・鉛/亜鉛中毒）。CBC で感染マーカーを評価。頭部CT/MRI（大型鳥で実施可能）で構造的病変を検索。ABV/PaBV PCR検査。血中鉛・亜鉛濃度測定。鳥類の痙攣発作は低Ca血症（産卵関連）・重金属中毒・PDD・感染性脳炎が主要原因で、特発性てんかんは稀"
}

# 80. bird_star-gazing_opisthotonus — Star-Gazing (Opisthotonus)
ENRICHMENTS["bird_star-gazing_opisthotonus"] = {
    "diagnosis_ja": "特徴的姿勢（頭部後屈・star-gazing posture・後弓反張）の観察。神経学的検査で脳幹・小脳病変を示す所見を評価。血液生化学（採血量≤体重の1%）でVitB1（チアミン）・Ca・グルコース・鉛・亜鉛を測定。CBC でヘテロフィル/リンパ球変動を確認。PCR検査でParamyxovirus-1（NDV）・ABV・Avian Encephalomyelitis Virusを検索。食餌歴聴取（VitB1欠乏リスク）。鳥類のstar-gazingはチアミン欠乏・PMV-1感染・重金属中毒・PDD等の多様な原因で発生し、緊急性の評価が重要"
}

# 81. bird_egg_yolk_peritonitis — Egg Yolk Peritonitis
ENRICHMENTS["bird_egg_yolk_peritonitis"] = {
    "diagnosis_ja": "腹部膨満・呼吸困難・産卵停止の臨床評価。腹部X線で体腔内液体貯留・粒状陰影を確認。腹部超音波で遊離卵黄・卵管異常・体腔液を描出。CBC（採血量≤体重の1%）でヘテロフィル著増・H/L比上昇を確認。血液生化学でTP上昇・Ca上昇（産卵活動）・AST上昇を測定。体腔穿刺液の細胞診で卵黄物質・ヘテロフィル浸潤を確認。培養でE. coli等の二次感染菌を同定。鳥類では卵胞破裂や逆蠕動により卵黄が体腔内に遊離し、重篤な体腔炎を惹起する"
}

# 82. bird_oviductal_prolapse — Oviductal Prolapse
ENRICHMENTS["bird_oviductal_prolapse"] = {
    "diagnosis_ja": "排泄腔からの赤色組織の脱出を視診で確認（卵管・総排泄腔・腸管の鑑別が重要）。脱出組織の色調・浮腫・壊死の有無を評価。腹部X線で卵の有無・腹腔内異常を確認。超音波で卵管壁肥厚・卵胞活動を評価。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。血液生化学でCa（低Ca→筋力低下が脱出誘因）・TP・グルコースを測定。鳥類の卵管脱出は難産・慢性産卵・低Ca血症・肥満が主要リスク因子で、組織壊死前の迅速な整復が予後を左右する"
}

# 83. bird_ovarian_tumor — Ovarian Tumor
ENRICHMENTS["bird_ovarian_tumor"] = {
    "diagnosis_ja": "腹部膨満・産卵異常・体重増加の臨床評価。腹部X線で腹腔内腫瘤影・臓器変位を確認。超音波検査で卵巣腫瘤のサイズ・エコーパターン・血流を評価。CT検査で腫瘤の範囲・浸潤度を判定。CBC（採血量≤体重の1%）で貧血・白血球変動を確認。血液生化学でCa上昇（エストロゲン産生腫瘍）・AST・LDH上昇を測定。体腔穿刺液の細胞診で腫瘍細胞を検索。鳥類では左卵巣のみが機能的に発達するため、卵巣腫瘍は左側に発生し、腺癌・顆粒膜細胞腫が多い"
}

# 84. bird_pituitary_adenoma — Pituitary Adenoma
ENRICHMENTS["bird_pituitary_adenoma"] = {
    "diagnosis_ja": "内分泌異常の臨床評価（多飲多尿・肥満・羽毛異常・行動変化）。頭部CT/MRIで下垂体腫瘤を描出（大型鳥で実施可能）。血液生化学（採血量≤体重の1%）でホルモン値（コルチコステロン・T4・性ホルモン）を測定。CBC で白血球変動を評価。視覚障害の評価（下垂体腫瘤による視交叉圧迫）。X線で骨密度変化を確認。鳥類の下垂体腺腫はセキセイインコに多く報告され、ACTH産生腫瘍による副腎皮質機能亢進症様症状を呈することがある"
}

# 85. bird_lice_mallophaga — Lice (Mallophaga)
ENRICHMENTS["bird_lice_mallophaga"] = {
    "diagnosis_ja": "羽毛・皮膚の詳細な視診で咀嚼シラミの虫体（1-6mm）・卵（nits）を肉眼/拡大鏡で確認。罹患羽毛の顕微鏡検査で虫体の形態学的同定（咀嚼口器・幅広い頭部が特徴）。羽毛損傷パターンの評価（羽毛の食害痕・先端の不整）。CBC（採血量≤体重の1%）で軽度貧血・好酸球増加を確認。体重・BCSの評価（重度感染では体重減少）。鳥類のMallophagaは宿主特異性が高く、直接接触で伝播する。羽毛の断裂パターンは機械的毛引きとの鑑別点となる"
}

# 86. bird_tapeworms_cestodes — Tapeworms (Cestodes)
ENRICHMENTS["bird_tapeworms_cestodes"] = {
    "diagnosis_ja": "糞便検査（直接塗抹法・浮遊法）で特徴的な卵嚢（egg packet）内の六鉤幼虫を検出。糞便中の白色片節（proglottid）を肉眼で確認。虫体の形態学的同定（頭節のrostellum・吸盤構造）。CBC（採血量≤体重の1%）で好酸球増加を確認。血液生化学でTP低下・アルブミン低下（栄養吸収障害）を測定。腹部X線で消化管拡張を評価。鳥類ではRaillietina・Davainea等が多く、中間宿主（甲虫・アリ等）の摂取が感染経路のため、屋外飼育鳥に好発する"
}

# 87. bird_capillaria_hairworm — Capillaria (Hairworm)
ENRICHMENTS["bird_capillaria_hairworm"] = {
    "diagnosis_ja": "糞便検査（浮遊法）でCapillaria特有の樽型虫卵（両極に栓構造）を検出。そのう洗浄液の検鏡でC. contorta（そのう・食道寄生型）の虫卵を確認。CBC（採血量≤体重の1%）で好酸球増加・ヘテロフィル変動を評価。血液生化学でTP低下・アルブミン低下を測定。体重・BCSの評価（消耗性変化）。そのう・前胃の内視鏡検査で粘膜内の虫体を直視確認。鳥類ではCapillaria obsignataが小腸寄生、C. contortaがそのう/食道寄生で、重感染では重度の消耗と死亡をもたらす"
}

# 88. bird_atherosclerosis — Atherosclerosis
ENRICHMENTS["bird_atherosclerosis"] = {
    "diagnosis_ja": "臨床症状の評価（呼吸困難・運動不耐性・突然死・脚跛行）。心エコーで大動脈壁肥厚・弁膜変性・心機能低下を評価。心電図で不整脈・ST変化を記録。胸部X線で大動脈走行の不整・心拡大を確認。血液生化学（採血量≤体重の1%）で総コレステロール・中性脂肪・HDL/LDLを測定。CBC で白血球変動を評価。食餌歴聴取（高脂肪種子食が最大のリスク因子）。鳥類の動脈硬化はアマゾン・ヨウム・コンゴウインコ等の老齢大型オウムに好発し、生前診断は困難で剖検での確定が多い"
}

# 89. bird_ptfe___teflon_toxicosis — PTFE / Teflon Toxicosis
ENRICHMENTS["bird_ptfe___teflon_toxicosis"] = {
    "diagnosis_ja": "曝露歴の緊急聴取（加熱されたPTFEコーティング調理器具・オーブン・アイロン等のフッ素樹脂製品の使用）。急性呼吸困難・突然死の臨床評価。胸部X線で肺浮腫・気嚢混濁を確認。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でAST・LDH上昇を測定。血液ガス分析で低酸素血症を確認。鳥類の気嚢系は非常に効率的なガス交換を行うため、PTFE熱分解産物への感受性が哺乳類の100倍以上とされ、微量曝露でも急性肺浮腫・出血性肺炎を起こす"
}

# 90. bird_zinc_poisoning — Zinc Poisoning
ENRICHMENTS["bird_zinc_poisoning"] = {
    "diagnosis_ja": "曝露歴の聴取（亜鉛メッキケージ金網・亜鉛製玩具・硬貨の摂取）。腹部X線で消化管内金属異物を確認。血中亜鉛濃度測定（正常<200 μg/dL、中毒>300 μg/dL）。CBC（採血量≤体重の1%）でPCV低下（溶血性貧血）・赤血球形態異常を評価。血液生化学でAST・LDH上昇（肝/膵障害）・UA上昇（腎障害）を測定。膵酵素（リパーゼ/アミラーゼ）上昇。鳥類の亜鉛中毒は「new wire disease」とも呼ばれ、新しいケージの亜鉛メッキ金網を齧ることが最多の感染経路"
}

# 91. bird_copper_poisoning — Copper Poisoning
ENRICHMENTS["bird_copper_poisoning"] = {
    "diagnosis_ja": "曝露歴の聴取（銅製品・銅線・銅含有殺藻剤・銅メッキ金属の摂取）。腹部X線で消化管内金属異物を確認。血中銅濃度測定。血液生化学（採血量≤体重の1%）で肝酵素（AST・LDH）著増・胆汁酸上昇（肝障害）・UA上昇（腎障害）を確認。CBC でPCV低下（溶血性貧血）・赤血球形態異常を評価。肝生検で銅沈着を確認（ロダニン染色）。鳥類では銅中毒は肝壊死として現れやすく、溶血発作を伴う急性型と慢性肝障害型がある"
}

# 92. bird_screaming_excessive_vocalization — Screaming (Excessive Vocalization)
ENRICHMENTS["bird_screaming_excessive_vocalization"] = {
    "diagnosis_ja": "詳細な行動歴の聴取（過剰発声の時間帯・持続時間・誘発状況・社会的文脈）。身体検査で疼痛・不快感の器質的原因を除外。CBC・血液生化学（採血量≤体重の1%）で全身疾患を除外。X線検査で内臓疾患・骨折等の疼痛源を検索。環境評価（ケージサイズ・設置場所・光周期・社会的刺激の適否）。ビデオ観察で飼い主不在時の行動パターンを分析。鳥類の過剰発声は注意要求行動が最多の原因だが、疼痛・ホルモン変動・不安障害の除外診断が不可欠"
}

# 93. bird_avian_chlamydial_conjunctivitis — Avian Chlamydial Conjunctivitis
ENRICHMENTS["bird_avian_chlamydial_conjunctivitis"] = {
    "diagnosis_ja": "眼科検査で結膜充血・眼脂（粘液膿性）・眼瞼腫脹・角膜浮腫を評価。結膜スワブのChlamydia psittaci PCR検査で病原体を検出。細胞診でヘテロフィル・マクロファージ浸潤と細胞質内封入体を検索。血清学検査（CF試験・ELISA）で抗体価を測定。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多を確認。副鼻腔X線で副鼻腔炎の合併を評価。鳥類のChlamydia結膜炎は片側性で発症し全身感染（オウム病）の部分症状であることが多く、人獣共通感染症として公衆衛生上も重要"
}

# 94. bird_avian_erythroblastosis_leukosis — Avian Erythroblastosis (Leukosis)
ENRICHMENTS["bird_avian_erythroblastosis_leukosis"] = {
    "diagnosis_ja": "CBC（採血量≤体重の1%）で異型赤芽球の著増・PCV変動を確認。末梢血塗抹のライト・ギムザ染色で未熟な有核赤血球（赤芽球）の形態異常を評価。血液生化学でLDH著増・AST上昇を測定。腹部X線・超音波で肝脾腫を確認。ALV（鳥白血病ウイルス）ELISA/PCR検査で病原体を検出。骨髄穿刺・細胞診で赤芽球系の異常増殖を確認。鳥類の赤芽球症はALV-Jによるウイルス誘導性腫瘍で、主に家禽に発生するが、稀にオウム目でも報告がある"
}

# 95. bird_avian_encephalomyelitis — Avian Encephalomyelitis
ENRICHMENTS["bird_avian_encephalomyelitis"] = {
    "diagnosis_ja": "幼鳥（1-3週齢）の運動失調・頭部振戦・起立不能の臨床評価。神経学的検査で小脳症状（意図振戦・測距異常）を確認。Avian Encephalomyelitis Virus PCR検査（脳組織・糞便）でウイルスを検出。血清学検査（ELISA・中和試験）で抗体価を測定。CBC（採血量≤体重の1%）でリンパ球変動を評価。病理組織検査（剖検例）で脳幹・脊髄のリンパ球性囲管性浸潤を確認。鳥類のAEは経卵伝播と水平伝播があり、ワクチン未接種群で集団発生する"
}

# 96. bird_marek's_disease — Marek's Disease
ENRICHMENTS["bird_marek's_disease"] = {
    "diagnosis_ja": "臨床症状の評価（片脚麻痺・翼下垂・運動失調・虹彩変色→灰色眼）。神経学的検査で末梢神経障害パターン（非対称性肢麻痺）を確認。Marek's Disease Virus PCR検査（羽毛濾胞・血液）で病原体を検出。CBC（採血量≤体重の1%）でリンパ球異常を確認。剖検・病理組織検査で末梢神経（坐骨神経等）のリンパ腫様浸潤・内臓腫瘤を確認。鳥類のMDVはα-ヘルペスウイルスによるT細胞リンパ腫で、日齢ワクチン接種が予防の根幹。家禽で最も経済的損失の大きいウイルス疾患"
}

# 97. bird_avian_metapneumovirus_infection — Avian Metapneumovirus Infection
ENRICHMENTS["bird_avian_metapneumovirus_infection"] = {
    "diagnosis_ja": "上部呼吸器症状の評価（鼻汁・副鼻腔腫脹・頭部振り・開口呼吸）。aMPV特異的RT-PCR検査（鼻腔/気管スワブ）でウイルスRNAを検出。血清学検査（ELISA）で抗体価を測定（ペア血清で4倍以上の上昇）。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。副鼻腔X線で副鼻腔液体貯留を評価。気管洗浄液の細胞診で炎症パターンを確認。鳥類のaMPV感染は七面鳥で最も重篤（TRT：七面鳥鼻気管炎）で、鶏ではSHS（腫脹頭症候群）として発現する"
}

# 98. bird_duck_viral_hepatitis — Duck Viral Hepatitis
ENRICHMENTS["bird_duck_viral_hepatitis"] = {
    "diagnosis_ja": "幼アヒル（1-4週齢）の急性死・後弓反張の臨床評価。血液生化学（採血量≤体重の1%）で肝酵素（AST・LDH）著増・胆汁酸上昇を確認。CBC でリンパ球減少を評価。Duck Hepatitis Virus PCR検査（肝臓・血清）でウイルスを検出。血清学検査で抗体価を測定。剖検で肝臓の著明な腫大・出血性壊死を確認。病理組織検査で肝細胞壊死・リンパ球浸潤を評価。鳥類のDHVは主にDHV-1（Picornavirus）が原因で、致死率は1週齢以下で95%に達する"
}

# 99. bird_infectious_laryngotracheitis_ilt — Infectious Laryngotracheitis (ILT)
ENRICHMENTS["bird_infectious_laryngotracheitis_ilt"] = {
    "diagnosis_ja": "呼吸困難・血様気管分泌物・開口呼吸の臨床評価。気管の視診で出血性炎症・偽膜形成を確認。ILTV特異的PCR検査（気管スワブ）でGallid herpesvirus 1を検出。CBC（採血量≤体重の1%）でヘテロフィル変動を確認。気管洗浄液の細胞診でヘテロフィル浸潤・核内封入体を検索。病理組織検査で気管上皮の壊死・合胞体形成・Cowdry A型核内封入体を確認。鳥類のILTは鶏に特異的なヘルペスウイルス感染症で、潜伏感染鳥が間欠的に排出する"
}

# 100. bird_infectious_bronchitis — Infectious Bronchitis
ENRICHMENTS["bird_infectious_bronchitis"] = {
    "diagnosis_ja": "呼吸器症状（ラ音・くしゃみ・鼻汁）・産卵低下・腎症状の臨床評価。IBV特異的RT-PCR検査（気管・腎臓スワブ）でウイルスRNAを検出。血清学検査（ELISA・HI試験）でIBV抗体価を測定。CBC（採血量≤体重の1%）でヘテロフィル変動を確認。気管洗浄液の細胞診で炎症パターンを評価。血液生化学でUA上昇（腎型IBV）を確認。鳥類のIBVはγ-コロナウイルスで多数の血清型が存在し、呼吸器型・腎型・生殖器型の3つの臨床型を呈する。ワクチン株との型一致が重要"
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
