#!/usr/bin/env python3
"""Enrich Parakeet diagnosis_ja — batch 8 (50 entries of 72 remaining after batch 7)."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 1. parakeet_contact_dermatitis — Contact Dermatitis / 接触性皮膚炎
ENRICHMENTS["parakeet_contact_dermatitis"] = {
    "diagnosis_ja": "皮膚の発赤・腫脹・びらん（特に足底部・脚部・腹部の接触面）を身体検査で確認。病変分布パターンと刺激物質への接触歴の一致を評価。皮膚掻爬検査で感染性原因（真菌・ダニ）を除外。皮膚生検で表在性皮膚炎パターン・好酸球浸潤を確認。CBC（採血量≤体重の1%）で好酸球増加を評価。飼育環境の聴取（新しいケージ・消毒剤残留・亜鉛メッキ・人工芝等の化学物質接触を特定）。インコ類では足底皮膚炎との鑑別が重要であり、原因物質の除去が治療の根幹となる"
}

# 2. parakeet_myiasis_fly_strike — Myiasis (Fly Strike) / 蝿蛆症（フライストライク）
ENRICHMENTS["parakeet_myiasis_fly_strike"] = {
    "diagnosis_ja": "皮膚・羽毛下・肛門周囲のハエ幼虫（蛆虫）を身体検査で直接確認。創傷部位の組織壊死・悪臭の範囲を評価。蛆虫の形態学的同定（Lucilia・Calliphora等）。CBC（採血量≤体重の1%）で貧血・脱水・ヘテロフィル著増（二次感染）を確認。血液生化学でAST・LDH・UA変動を測定。X線で深部組織への波及を評価。インコ類では屋外飼育・下痢による糞便汚染・衰弱が蝿蛆症のリスク因子であり、蛆虫除去・創傷洗浄・抗菌薬投与に加え原因疾患の治療が不可欠"
}

# 3. parakeet_tick_infestation — Tick Infestation / ダニ寄生症
ENRICHMENTS["parakeet_tick_infestation"] = {
    "diagnosis_ja": "体表の精査で吸血中のダニ（頭部・耳孔・眼周囲・総排泄腔周囲を重点検索）を確認。ダニ種の形態学的同定。CBC（採血量≤体重の1%）でPCV低下（大量寄生時の貧血）・好酸球増加を確認。血液塗抹でダニ媒介性血液寄生虫（Haemoproteus等）を検索。鳥類ではArgasダニ（軟ダニ）は夜間吸血性のため日中の検査では見逃しやすく、ケージ・巣箱内の精査が重要。インコ類は室内飼育が多いためダニ寄生は稀であるが、屋外飼育鳥や野鳥との接触歴がある場合にリスクが高まる"
}

# 4. parakeet_hippoboscid_fly_infestation — Hippoboscid Fly Infestation / シラミバエ寄生症
ENRICHMENTS["parakeet_hippoboscid_fly_infestation"] = {
    "diagnosis_ja": "羽毛間を走行する扁平な有翅/無翅ハエ（Hippoboscidae科）を身体検査で直接確認。シラミバエの形態学的同定（Pseudolynchia・Ornithomya等）。CBC（採血量≤体重の1%）で貧血の程度を評価。血液塗抹でシラミバエ媒介性血液寄生虫（Haemoproteus属）を検索。羽毛損傷・掻痒行動の評価。インコ類ではシラミバエ寄生は稀であるが、屋外飼育鳥や新規導入鳥から持ち込まれることがある。シラミバエはHaemoproteus属の生物学的ベクターであり、寄生虫検査の同時実施が推奨される"
}

# 5. parakeet_reproductive_tract_infection_salpingitis — Reproductive Tract Infection (Salpingitis)
ENRICHMENTS["parakeet_reproductive_tract_infection_salpingitis"] = {
    "diagnosis_ja": "産卵異常・腹部膨満・排泄腔からの分泌物の臨床評価。排泄腔スワブの細菌培養・感受性試験で起炎菌（E. coli・Klebsiella等）を同定。腹部超音波で卵管腫大・卵管内液体貯留・体腔液を検出。X線で異常卵殻・軟部組織腫瘤を確認。CBC（採血量≤体重の1%）でヘテロフィル著増・H/L比上昇を確認。血液生化学でCa・TP・AST上昇を測定。インコ類では慢性産卵に伴う卵管炎がE. coliの上行感染で多発し、卵黄性腹膜炎への進展が致死的となりうる"
}

# 6. parakeet_phallus_prolapse — Phallus Prolapse / 陰茎脱出
ENRICHMENTS["parakeet_phallus_prolapse"] = {
    "diagnosis_ja": "総排泄腔からの組織脱出を視診で確認（注：インコ類（Psittaciformes）は陰茎を持たず、脱出組織は総排泄腔粘膜・卵管・腸管の脱出と鑑別が必要）。脱出組織の同定・生存性（色調・浮腫・壊死）の評価。X線・超音波で腹腔内腫瘤・卵管異常を検索。CBC（採血量≤体重の1%）で二次感染を評価。血液生化学でTP・UA・グルコースを測定。インコ類では総排泄腔脱（cloacal prolapse）が正しい診断名であり、慢性いきみ・産卵障害・テネスムスが原因となる"
}

# 7. parakeet_subcutaneous_emphysema — Subcutaneous Emphysema / 皮下気腫
ENRICHMENTS["parakeet_subcutaneous_emphysema"] = {
    "diagnosis_ja": "体表の触診で皮下のcrepitus（捻髪音）を確認し、気腫の範囲を評価。外傷歴（衝突・咬傷・過度の保定）を聴取。X線で皮下ガス像・気嚢壁の不連続を検出。CT検査（大型種で実施可能）で破裂気嚢を同定。CBC（採血量≤体重の1%）で二次感染を評価。経皮的穿刺で一時的減圧。インコ類では気嚢破裂が皮下気腫の最も一般的な原因であり、セキセイインコの小さな体格では少量の皮下気腫でも呼吸効率に影響する。軽度例は安静で自然治癒するが再発性の場合は外科的修復を検討"
}

# 8. parakeet_adrenal_gland_disease — Adrenal Gland Disease / 副腎疾患
ENRICHMENTS["parakeet_adrenal_gland_disease"] = {
    "diagnosis_ja": "多飲多尿・体重変動・羽毛異常・筋力低下の臨床評価。血液生化学（採血量≤体重の1%）でグルコース・Na・K・Ca変動を測定。コルチコステロン濃度の測定（鳥類の主要グルココルチコイド）。ACTH刺激試験でコルチコステロン反応を評価。腹部超音波で副腎の腫大・結節を検出。CBC で全身状態を確認。インコ類では副腎疾患は診断困難であり、慢性ストレスによるHPA軸過活動が羽毛障害・免疫低下の要因となることがある。剖検での確定診断となるケースが多い"
}

# 9. parakeet_aortic_rupture — Aortic Rupture / 大動脈破裂
ENRICHMENTS["parakeet_aortic_rupture"] = {
    "diagnosis_ja": "突然死・急性呼吸困難・チアノーゼ・虚脱の臨床評価（多くの場合、死後診断）。剖検で体腔内大量出血・大動脈壁の裂傷を確認。動脈硬化性変化（アテローム性プラーク・石灰化・中膜変性）の病理組織評価。CBC・血液生化学（生前検査が可能な場合）でPCV低下・コレステロール・トリグリセリド上昇を確認。心エコーで大動脈の評価。インコ類では大動脈破裂はアテローム性動脈硬化症の最終段階として高齢鳥で発生し、高脂肪種子食・運動不足が主要危険因子"
}

# 10. parakeet_niacin_deficiency — Niacin Deficiency / ナイアシン欠乏症
ENRICHMENTS["parakeet_niacin_deficiency"] = {
    "diagnosis_ja": "口腔内炎症・舌腫脹・皮膚炎・下痢の臨床評価。食餌歴の詳細聴取（種子食偏重によるナイアシン・トリプトファン不足）。血液生化学（採血量≤体重の1%）で全身状態を評価。CBC で貧血を確認。尿中N-メチルニコチンアミド測定でナイアシン状態を間接評価。インコ類ではナイアシン欠乏は種子食偏重飼育で発生しうるが単独欠乏は稀で、複合的なビタミンB群欠乏の一部として現れることが多い。ナイアシン補充への臨床反応で診断を確認し、食餌改善（ペレット食への移行）を指導する"
}

# 11. parakeet_riboflavin_deficiency — Riboflavin Deficiency / リボフラビン欠乏症
ENRICHMENTS["parakeet_riboflavin_deficiency"] = {
    "diagnosis_ja": "脚の麻痺（curled toe paralysis：趾巻曲症）・成長遅延・羽毛異常の臨床評価。神経学的検査で末梢神経障害を評価。食餌歴の聴取（種子食偏重によるVitB2不足）。血液生化学（採血量≤体重の1%）で全身状態を評価。赤血球グルタチオンレダクターゼ活性でリボフラビン状態を間接評価。CBC で貧血を確認。インコ類のリボフラビン欠乏は幼鳥のcurled toe paralysis（坐骨神経ミエリン変性）が特徴的で、マレック病の末梢神経型と鑑別が必要。早期VitB2補充で可逆的"
}

# 12. parakeet_copper_poisoning — Copper Poisoning / 銅中毒
ENRICHMENTS["parakeet_copper_poisoning"] = {
    "diagnosis_ja": "急性嘔吐・血性下痢・沈鬱・黄色尿酸塩（肝障害）の臨床評価。曝露歴の聴取（銅線・銅製飼育器具・銅含有殺菌剤への接触）。血液生化学（採血量≤体重の1%）で肝酵素著増（AST・LDH）・胆汁酸上昇・溶血性貧血を確認。血清銅濃度の測定。腹部X線で消化管内の金属異物を検索。CBC で貧血（溶血性）を確認。肝生検で銅沈着を確認。インコ類では銅線咬傷が中毒の主因であり、銅は酸化ストレスを介して肝壊死・溶血性貧血を引き起こす。キレーション療法と曝露源除去が治療の基本"
}

# 13. parakeet_toxoplasmosis — Toxoplasmosis / トキソプラズマ症
ENRICHMENTS["parakeet_toxoplasmosis"] = {
    "diagnosis_ja": "急性沈鬱・神経症状（痙攣・運動失調・失明）・呼吸困難の臨床評価。PCR検査でToxoplasma gondii DNAを検出（血液・組織検体）。血清学検査（ELISA・IFA）で抗体価を測定。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でAST・LDH上昇（肝障害）を測定。病理組織検査でタキゾイト・ティッシュシスト（ブラディゾイト）を確認。インコ類ではトキソプラズマ症は急性致死性であることが多く、猫の糞便に含まれるオーシストの摂取が主感染経路。猫との同居環境を確認する"
}

# 14. parakeet_psittacine_poxvirus_parakeet — Psittacine Poxvirus (Parakeet)
ENRICHMENTS["parakeet_psittacine_poxvirus_parakeet"] = {
    "diagnosis_ja": "皮膚型：嘴基部・眼周囲・脚の痘疹性結節・痂皮を視診で確認。粘膜型：口腔・上部気道のジフテリア様偽膜を確認。病変部の組織生検でBollinger小体（細胞質内封入体）を確認。電子顕微鏡でPoxウイルス粒子を同定。PCR検査でPoxvirus DNAを検出。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。インコ類では皮膚型が多く予後は比較的良好であるが、粘膜型は上気道閉塞・二次感染で重篤化する。蚊等の媒介昆虫による伝播が主経路であり、蚊対策が予防に重要"
}

# 15. parakeet_papillomavirus_infection — Papillomavirus Infection / パピローマウイルス感染症
ENRICHMENTS["parakeet_papillomavirus_infection"] = {
    "diagnosis_ja": "皮膚・口腔・総排泄腔の乳頭状〜カリフラワー状腫瘤を身体検査で確認。病変部の生検・病理組織検査で乳頭腫の組織パターンを確認（線維血管芯を覆う重層扁平上皮の増殖）。PCR検査でパピローマウイルスDNAを検出。CBC（採血量≤体重の1%）で全身状態を評価。内視鏡で消化管内への進展を検索。インコ類ではパピローマウイルス感染は口腔・総排泄腔に好発し、悪性転化のリスクは低いが、大きな乳頭腫は物理的障害を引き起こす。外科的切除・レーザー焼灼が治療選択肢"
}

# 16. parakeet_proventricular_neoplasia — Proventricular Neoplasia / 腺胃腫瘍
ENRICHMENTS["parakeet_proventricular_neoplasia"] = {
    "diagnosis_ja": "慢性嘔吐・体重減少・食欲低下・未消化便の臨床評価。腹部X線で前胃（proventriculus）の拡張・腫瘤影を検出。造影X線で前胃壁の不整・充満欠損を確認。腹部超音波で腫瘤の範囲を評価。内視鏡で前胃粘膜の腫瘤を直視確認・生検。病理組織検査で腫瘍の組織型（腺癌・リンパ腫・平滑筋腫瘍等）を確定。CBC・血液生化学（採血量≤体重の1%）で貧血・AST変動を評価。インコ類ではPDD（前胃拡張症：ABV感染）との鑑別が重要であり、ABV-PCRを必ず実施する"
}

# 17. parakeet_renal_adenocarcinoma_parakeet — Renal Adenocarcinoma (Parakeet) / 腎腺癌（インコ）
ENRICHMENTS["parakeet_renal_adenocarcinoma_parakeet"] = {
    "diagnosis_ja": "片脚麻痺（腎腫瘤による坐骨神経叢圧迫が第一徴候となることが多い）・腹部膨満・多飲多尿の臨床評価。腹部超音波で腎臓の腫瘤を検出。X線で腹腔内腫瘤影・腎陰影拡大を確認。血液生化学（採血量≤体重の1%）でUA著増・電解質異常を確認。CBC で貧血・白血球変動を評価。FNA細胞診で腺癌細胞を確認。インコ類（特にセキセイインコ）では腎腺癌が最も一般的な腎腫瘍であり、片脚麻痺が初発症状として診察に訪れるケースが多い。予後は一般に不良"
}

# 18. parakeet_cutaneous_fibroma — Cutaneous Fibroma / 皮膚線維腫
ENRICHMENTS["parakeet_cutaneous_fibroma"] = {
    "diagnosis_ja": "皮膚の硬い結節性腫瘤（可動性・非疼痛性）を身体検査で確認。FNA細胞診で紡錘形線維芽細胞・コラーゲン基質を確認。外科切除検体の病理組織検査で線維腫（良性）を確定し、切除マージンを評価。X線で骨浸潤の有無を確認。CBC・血液生化学（採血量≤体重の1%）で全身状態を評価。インコ類の皮膚線維腫は良性腫瘍であり外科的完全切除で予後良好。悪性の線維肉腫との鑑別は病理組織検査でのみ可能であり、核分裂指数・浸潤パターンが鑑別の鍵となる"
}

# 19. parakeet_subcutaneous_lipoma_advanced — Subcutaneous Lipoma (Advanced) / 皮下脂肪腫（進行型）
ENRICHMENTS["parakeet_subcutaneous_lipoma_advanced"] = {
    "diagnosis_ja": "大型の皮下腫瘤（軟性・可動性・非疼痛性が典型だが進行型では固着・浸潤性）を身体検査で確認。FNA細胞診で成熟脂肪細胞を確認。外科切除検体の病理組織検査で脂肪腫を確定し、浸潤性脂肪腫・脂肪肉腫との鑑別。X線・超音波で腫瘤の範囲・周囲組織への浸潤を評価。CBC・血液生化学（採血量≤体重の1%）で全身状態を確認。インコ類（特にセキセイインコ・オカメインコ）では脂肪腫が好発し、進行型では歩行・飛翔障害を引き起こす。食餌改善（低脂肪食）が再発予防に重要"
}

# 20. parakeet_aortic_atherosclerosis_parakeet — Aortic Atherosclerosis (Parakeet)
ENRICHMENTS["parakeet_aortic_atherosclerosis_parakeet"] = {
    "diagnosis_ja": "高齢インコの運動不耐性・呼吸困難・チアノーゼ・突然死の臨床評価。心エコー検査で大動脈壁の肥厚・石灰化・内腔狭窄を評価。胸部X線で大動脈の石灰化・心拡大を検出。血液生化学（採血量≤体重の1%）でコレステロール・トリグリセリド上昇（高脂血症）を確認。心電図で不整脈を記録。食餌歴の聴取（高脂肪種子食偏重）。インコ類ではアテローム性動脈硬化は高齢鳥で高頻度であり、ヒマワリの種等の高脂肪食・運動不足が主要危険因子。予防には食餌改善が最重要"
}

# 21. parakeet_right-sided_heart_failure_parakeet — Right-Sided Heart Failure (Parakeet)
ENRICHMENTS["parakeet_right-sided_heart_failure_parakeet"] = {
    "diagnosis_ja": "腹水貯留・肝腫大・頸静脈怒張・運動不耐性の臨床評価。心エコー検査で右心房/右心室拡大・三尖弁逆流を評価。胸部X線で心拡大（右心系優位）・体腔液貯留を検出。心電図で不整脈・右心負荷パターンを記録。CBC・血液生化学（採血量≤体重の1%）でAST・LDH・UA上昇を確認。体腔穿刺液の分析（漏出液パターン）。インコ類の右心不全は慢性呼吸器疾患（アスペルギルス症・気嚢炎）→肺高血圧→右心負荷が主要病態であり、原因疾患の治療と利尿薬が治療の基本"
}

# 22. parakeet_bacterial_airsacculitis — Bacterial Airsacculitis / 細菌性気嚢炎
ENRICHMENTS["parakeet_bacterial_airsacculitis"] = {
    "diagnosis_ja": "呼吸困難・開口呼吸・テイルボビング・運動不耐性の臨床評価。胸部X線で気嚢壁の肥厚・混濁を検出。気嚢穿刺液の細菌培養・感受性試験で起炎菌（E. coli・Pseudomonas・Klebsiella等）を同定。グラム染色で菌種を推定。CBC（採血量≤体重の1%）でヘテロフィル著増・H/L比上昇を確認。血液生化学でAST・LDH上昇を測定。インコ類では気嚢炎は呼吸器感染の重要な構成要素であり、真菌性気嚢炎（アスペルギルス）との鑑別が治療方針に直結する"
}

# 23. parakeet_tracheal_aspergillosis — Tracheal Aspergillosis / 気管アスペルギルス症
ENRICHMENTS["parakeet_tracheal_aspergillosis"] = {
    "diagnosis_ja": "声の変化（嗄声・失声）・吸気性呼吸困難・気管レベルのストリドールの臨床評価。気管内視鏡で気管内腔の白色〜黄緑色真菌腫・肉芽腫を直視確認・生検。気管洗浄液の真菌培養でAspergillus fumigatusを分離。細胞診で分枝隔壁菌糸を確認。ガラクトマンナン抗原検査。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多を確認。胸部X線・CTで気管内軟部組織腫瘤を検出。インコ類の気管アスペルギルス症は声の変化が初発症状であり、進行すると気道閉塞→窒息のリスクがある"
}

# 24. parakeet_candidal_ingluvitis — Candidal Ingluvitis / カンジダ性嗉嚢炎
ENRICHMENTS["parakeet_candidal_ingluvitis"] = {
    "diagnosis_ja": "嘔吐・嗉嚢膨満・食欲低下・嗉嚢内容停滞の臨床評価。嗉嚢洗浄液の鏡検で出芽酵母・菌糸（Candida albicans）を確認。グラム染色でグラム陽性の酵母細胞を検出。真菌培養で菌種同定と感受性試験。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でTP低下・グルコース変動を測定。X線で嗉嚢拡張を確認。インコ類のカンジダ性嗉嚢炎は幼鳥の手差し飼育（温度不適切・器具汚染）・抗菌薬長期使用・免疫低下で多発する。ナイスタチン/フルコナゾール経口投与が治療の基本"
}

# 25. parakeet_macrorhabdus_ornithogaster_parakeet — Macrorhabdus ornithogaster (Parakeet)
ENRICHMENTS["parakeet_macrorhabdus_ornithogaster_parakeet"] = {
    "diagnosis_ja": "慢性体重減少・膨羽・未消化粒状便・嘔吐の臨床評価。新鮮糞便のグラム染色・ギムザ染色で大型棒状酵母体（Macrorhabdus ornithogaster: 20-90μm）を検出。腹部X線で前胃拡張・筋胃菲薄化を評価。内視鏡で前胃粘膜の白色結節・びらんを確認。CBC（採血量≤体重の1%）でH/L比上昇を確認。血液生化学でTP低下・グルコース低下を測定。インコ類（特にセキセイインコ）ではAGY（Avian Gastric Yeast）感染は極めて一般的であり、慢性消耗性疾患の主要原因。アムホテリシンB経口投与が第一選択"
}

# 26. parakeet_cnemidocoptes_scaly_face_advanced — Cnemidocoptes (Scaly Face Advanced)
ENRICHMENTS["parakeet_cnemidocoptes_scaly_face_advanced"] = {
    "diagnosis_ja": "嘴基部・蝋膜・眼周囲・脚の重度過角化病変（白色〜灰色の蜂巣状痂皮が広範囲に拡大）を視診で確認。嘴変形（過長・交差咬合）の評価。皮膚掻爬検体のKOH処理・鏡検でCnemidocoptes pilae（球形ダニ・200-400μm）を検出。X線で嘴骨・趾骨の変形を評価。CBC（採血量≤体重の1%）で免疫状態を確認。インコ類（特にセキセイインコ）のCnemidocoptes進行型では嘴の著明な変形により採食困難となる。イベルメクチン局所/経口投与を2週間隔で反復し、嘴トリミングを併用する"
}

# 27. parakeet_mandibular_prognathism_parakeet — Mandibular Prognathism (Parakeet)
ENRICHMENTS["parakeet_mandibular_prognathism_parakeet"] = {
    "diagnosis_ja": "下嘴の上嘴に対する前方偏位（アンダーバイト）を視診で確認。嘴の咬合パターン・角度・対称性を評価。頭部X線で骨格構造の異常・嘴根部の変形を描出。口腔内検査で舌・口蓋への嘴先端の外傷を検索。CBC（採血量≤体重の1%）で二次感染を評価。飼育歴の聴取（遺伝的素因・不適切な手差し給餌による嘴変形・カルシウム不足）。インコ類の幼鳥では下顎前突が比較的多く報告され、早期（成長期）の定期的な嘴トリミング・矯正で改善可能な場合がある"
}

# 28. parakeet_thyroid_carcinoma_parakeet — Thyroid Carcinoma (Parakeet) / 甲状腺癌（インコ）
ENRICHMENTS["parakeet_thyroid_carcinoma_parakeet"] = {
    "diagnosis_ja": "頸部腫脹・嚥下困難・呼吸困難（気管圧迫）・声の変化の臨床評価。頸部触診で甲状腺領域の腫瘤を確認。FNA細胞診で甲状腺腫瘍細胞を確認。頸部X線・CTで腫瘤のサイズ・気管圧迫・浸潤範囲を評価。病理組織検査で甲状腺癌を確定。血液生化学（採血量≤体重の1%）でT4値を測定。CBC で全身状態を評価。インコ類ではセキセイインコの甲状腺癌が最も多く報告され、ヨード欠乏性甲状腺腫（良性過形成）との鑑別が重要。甲状腺腫はヨード補充で退縮するが癌は退縮しない"
}

# 29. parakeet_vitamin_e_deficiency_parakeet — Vitamin E Deficiency (Parakeet)
ENRICHMENTS["parakeet_vitamin_e_deficiency_parakeet"] = {
    "diagnosis_ja": "筋力低下・運動失調・斜頸（脳軟化症）・免疫低下の臨床評価。食餌歴の聴取（種子食偏重→VitE・Se不足、酸化脂肪の多い古い種子摂取）。血液生化学（採血量≤体重の1%）でCK上昇（筋障害）・AST上昇を確認。血漿VitE濃度の測定。CBC で全身状態を評価。病理組織検査で脳軟化症・白筋病（栄養性ミオパチー）を確認。インコ類のVitE欠乏は抗酸化能低下→酸化的組織障害を引き起こし、脳軟化症（後弓反張）と白筋病（飛翔不能）が特徴的。VitE・Se補充で早期なら改善可能"
}

# 30. parakeet_pantothenic_acid_deficiency — Pantothenic Acid Deficiency / パントテン酸欠乏症
ENRICHMENTS["parakeet_pantothenic_acid_deficiency"] = {
    "diagnosis_ja": "皮膚炎（特に眼周囲・嘴角部の痂皮形成）・成長遅延・羽毛異常の臨床評価。食餌歴の聴取（種子食偏重・加工飼料のVitB群不足）。血液生化学（採血量≤体重の1%）で全身状態を評価。CBC で貧血を確認。全血パントテン酸濃度の測定（利用可能な場合）。鳥類のパントテン酸欠乏は家禽で眼周囲の顆粒状皮膚病変・足底皮膚炎が特徴的。インコ類では単独欠乏は稀であり、複合的なVitB群欠乏の一部として現れることが多い。食餌改善とVitB群補充で改善する"
}

# 31. parakeet_teflon_toxicosis_parakeet — Teflon Toxicosis (Parakeet) / テフロン中毒（インコ）
ENRICHMENTS["parakeet_teflon_toxicosis_parakeet"] = {
    "diagnosis_ja": "突然死（最も一般的な転帰）または急性重度呼吸困難・開口呼吸・チアノーゼの臨床評価。テフロン（PTFE）加熱製品への曝露歴の聴取（テフロン加工フライパン・オーブン・アイロン・ヘアドライヤー等の過熱）。剖検で肺の重度出血性水腫・気嚢混濁を確認。病理組織検査で肺毛細血管のびまん性内皮障害を確認。CBC・血液生化学（生前検査が可能な場合）で呼吸不全を評価。インコ類はPTFEガスへの感受性が極めて高く、260℃以上で加熱されたテフロンから放出される超微粒子が致死的肺障害を引き起こす"
}

# 32. parakeet_avocado_toxicosis_parakeet — Avocado Toxicosis (Parakeet) / アボカド中毒（インコ）
ENRICHMENTS["parakeet_avocado_toxicosis_parakeet"] = {
    "diagnosis_ja": "急性呼吸困難・羽毛逆立て・沈鬱・突然死の臨床評価。アボカド（果実・種・葉・樹皮）への曝露歴を聴取。剖検で心筋壊死・肺水腫・肝壊死を確認。CBC・血液生化学（採血量≤体重の1%、生前検査の場合）でCK著増（心筋障害）・AST・LDH上昇を確認。心電図で不整脈を記録。X線で肺水腫・心拡大を検出。インコ類のアボカド中毒はpersin（脂肪酸誘導体）による心筋壊死が主要病態であり、摂取後12-24時間で症状が出現し、致死率が極めて高い。対症療法のみで特異的解毒薬はない"
}

# 33. parakeet_capillaria_parakeet — Capillaria (Parakeet) / 毛頭虫症（インコ）
ENRICHMENTS["parakeet_capillaria_parakeet"] = {
    "diagnosis_ja": "体重減少・下痢・嗉嚢病変（そのう寄生の場合：嘔吐・嗉嚢肥厚）の臨床評価。糞便検査（浮遊法）でCapillaria属虫卵（バレル型・両極に栓を有する特徴的な虫卵：50-70×25-30μm）を検出。嗉嚢洗浄液の鏡検で嗉嚢寄生型の虫体を検索。CBC（採血量≤体重の1%）で好酸球増加を確認。血液生化学でTP低下を測定。インコ類ではCapillaria感染は嗉嚢型（C. contorta）と腸管型（C. obsignata）があり、嗉嚢粘膜への潜入が嗉嚢壁肥厚と慢性消耗を引き起こす"
}

# 34. parakeet_knemidocoptic_mange_–_severe — Knemidocoptic Mange – Severe / 重度疥癬ダニ症
ENRICHMENTS["parakeet_knemidocoptic_mange_–_severe"] = {
    "diagnosis_ja": "嘴・蝋膜・眼周囲・脚部の広範囲にわたる重度過角化病変（白色〜灰色の厚い痂皮・蜂巣状変形）を視診で確認。嘴変形（過長・交差）・趾変形の評価。皮膚掻爬検体のKOH処理・鏡検でKnemidocoptes（Cnemidocoptes）ダニを検出。X線で骨変形・骨膜反応を評価。CBC（採血量≤体重の1%）で免疫低下の基礎疾患を検索。インコ類の重度疥癬は免疫低下個体で進行し、嘴変形による採食困難が生命を脅かす。イベルメクチン反復投与と嘴整形が必要"
}

# 35. parakeet_goiter_–_severe_tracheal_compression — Goiter – Severe Tracheal Compression
ENRICHMENTS["parakeet_goiter_–_severe_tracheal_compression"] = {
    "diagnosis_ja": "重度の吸気性呼吸困難・ストリドール・嚥下困難の臨床評価。頸部触診で甲状腺領域の著明な腫大を確認。頸部X線・CTで甲状腺腫による気管の圧迫・偏位を検出。血液生化学（採血量≤体重の1%）でT4低下を確認。食餌歴の聴取（ヨード欠乏：種子食偏重・ゴイトロゲン含有食の過剰摂取）。CBC で全身状態を評価。インコ類（特にセキセイインコ）ではヨード欠乏性甲状腺腫が気管を圧迫して重度呼吸困難を引き起こし、ヨード補充（飲水添加・直接投与）で数週間以内に過形成が退縮する"
}

# 36. parakeet_reproductive_tract_prolapse — Reproductive Tract Prolapse / 生殖器脱出
ENRICHMENTS["parakeet_reproductive_tract_prolapse"] = {
    "diagnosis_ja": "総排泄腔から突出した組織（卵管・子宮・腸管の鑑別が必要）を視診で確認。突出組織の生存性（色調・浮腫・壊死・乾燥）を評価。腹部X線・超音波で体腔内の卵・腫瘤を検索。CBC（採血量≤体重の1%）でヘテロフィル増加（二次感染）を確認。血液生化学でCa（低Ca血症→子宮筋力低下）・TP・UA変動を測定。インコ類の生殖器脱出は慢性産卵・卵詰まり・低Ca血症に続発し、組織の洗浄・整復後にパーストリング縫合で保持する。壊死組織は外科的切除が必要"
}

# 37. parakeet_night_fright_injuries — Night Fright Injuries / 夜間パニック外傷
ENRICHMENTS["parakeet_night_fright_injuries"] = {
    "diagnosis_ja": "夜間のパニック発作後の外傷（翼・脚の骨折・出血・打撲・嘴損傷）を身体検査で確認。X線で骨折の有無を評価。外傷の範囲と出血量を評価。CBC（採血量≤体重の1%）で出血性貧血を確認。血液生化学で臓器損傷を評価。飼育環境の聴取（夜間の光・音・振動等のパニック誘因を特定）。インコ類（特にオカメインコ）では夜間パニック（night fright）が好発し、ケージ内での激しい暴れにより重度外傷を負う。夜間の常夜灯設置・ケージカバーの使用・誘因除去が予防策"
}

# 38. parakeet_scaly_leg_mites — Scaly Leg Mites / 脚疥癬ダニ症
ENRICHMENTS["parakeet_scaly_leg_mites"] = {
    "diagnosis_ja": "脚部の鱗屑・白色〜灰色の厚い痂皮・蜂巣状変形（ハニカム状隆起）を視診で確認。進行例では趾の腫脹・変形を評価。皮膚掻爬検体のKOH処理・鏡検でKnemidocoptes（Cnemidocoptes）属ダニの虫体・卵を検出。X線で長期感染例の趾骨変形・骨膜反応を評価。CBC（採血量≤体重の1%）で全身状態を確認。インコ類ではKnemidocoptes mutans（脚疥癬の主要種）による脚鱗の過角化が特徴的。イベルメクチン投与（経口/局所）を2週間隔で3-4回反復し、環境消毒を併用する"
}

# 39. parakeet_psittacosis_–_respiratory_form — Psittacosis – Respiratory Form / オウム病呼吸器型
ENRICHMENTS["parakeet_psittacosis_–_respiratory_form"] = {
    "diagnosis_ja": "鼻汁・くしゃみ・結膜炎・呼吸困難・開口呼吸の臨床評価。排泄腔・後鼻孔スワブのPCR検査でChlamydia psittaci DNAを検出。血清学検査（ELISA・CF）で抗体価を測定（ペア血清で4倍以上上昇が有意）。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多を確認。血液生化学でAST・LDH上昇を測定。胸部X線で気嚢混濁・肺浸潤影を検出。インコ類のオウム病は人獣共通感染症であり、飼い主のインフルエンザ様症状の有無を必ず確認する。ドキシサイクリン45日間投与が標準治療"
}

# 40. parakeet_avian_gastric_yeast_–_refractory — Avian Gastric Yeast – Refractory
ENRICHMENTS["parakeet_avian_gastric_yeast_–_refractory"] = {
    "diagnosis_ja": "治療抵抗性の慢性削痩・嘔吐・未消化粒状便の臨床評価。糞便のグラム染色で大型棒状酵母体（Macrorhabdus ornithogaster）の持続的排出を確認。定量的糞便スコアで菌量をモニタリング。CBC（採血量≤体重の1%）でH/L比上昇を確認。血液生化学でTP低下・グルコース低下を測定。腹部X線で前胃拡張の進行を評価。インコ類のAGY難治例ではアムホテリシンB単独抵抗性を考慮し、NaHCO3併用（胃内pH上昇で菌増殖を抑制）・投与期間延長（6-8週間）・免疫状態の再評価（PBFD除外等）を行う"
}

# 41. parakeet_french_moult_–_severe — French Moult – Severe / フレンチモールト重症型
ENRICHMENTS["parakeet_french_moult_–_severe"] = {
    "diagnosis_ja": "巣立ち前後の幼鳥での初列風切羽・尾羽の著明な脱落・発育不全（飛翔不能の「ランナー」となる）を身体検査で確認。PCR検査でAvian Polyomavirus（APV）DNAを検出（羽毛・排泄腔スワブ・血液）。CBC（採血量≤体重の1%）でリンパ球変動を確認。血液生化学でAST・LDH変動を測定。PBFD-PCR検査でCircovirus感染を除外（鑑別疾患）。インコ類（特にセキセイインコ）のFrench moultはAPV感染による羽毛発育障害であり、重症型では永続的な飛翔不能となる"
}

# 42. parakeet_feather_cysts_–_recurrent — Feather Cysts – Recurrent / 反復性羽嚢腫
ENRICHMENTS["parakeet_feather_cysts_–_recurrent"] = {
    "diagnosis_ja": "皮下の反復性嚢胞性腫瘤（角化物質・変性羽毛を含む）を身体検査で確認。FNA で角化物質・変性羽毛断片を確認。外科切除検体の病理組織検査で毛包上皮由来の嚢胞壁を確認。X線で骨浸潤の有無を評価。CBC（採血量≤体重の1%）で二次感染を評価。インコ類では羽嚢腫は巻毛品種のカナリアに最も多いが、セキセイインコでも報告がある。遺伝的素因により羽毛が皮膚を穿通できず嚢胞化する。反復例では外科的完全摘出（嚢胞壁を含む）が根治的治療"
}

# 43. parakeet_testicular_tumor_–_sertoli_cell — Testicular Tumor – Sertoli Cell
ENRICHMENTS["parakeet_testicular_tumor_–_sertoli_cell"] = {
    "diagnosis_ja": "雄鳥の腹部膨満・蝋膜の褐色化（エストロゲン産生による雌性化）・片脚麻痺（腎/坐骨神経圧迫）の臨床評価。腹部超音波で精巣腫瘤を検出。X線で腹腔内腫瘤影を確認。CBC・血液生化学（採血量≤体重の1%）で全身状態を評価。FNA細胞診でセルトリ細胞腫瘍を確認。病理組織検査で確定。インコ類（特にセキセイインコ）ではセルトリ細胞腫はエストロゲン産生腫瘍として雌性化徴候（蝋膜色変化・行動変化）を呈し、臨床的にセミノーマとの鑑別が重要"
}

# 44. parakeet_ovarian_adenocarcinoma — Ovarian Adenocarcinoma / 卵巣腺癌
ENRICHMENTS["parakeet_ovarian_adenocarcinoma"] = {
    "diagnosis_ja": "腹部膨満・体重増加（体腔液貯留）・呼吸困難・産卵異常の臨床評価。腹部超音波で卵巣の腫瘤を検出。X線で腹腔内腫瘤影・体腔液を確認。CT検査で腫瘤の範囲・転移を評価。体腔穿刺液の細胞診で腺癌細胞を確認。CBC・血液生化学（採血量≤体重の1%）でCa上昇（傍腫瘍性高Ca血症の場合あり）・AST変動を確認。インコ類ではセキセイインコの卵巣腺癌が最も一般的な卵巣腫瘍であり、腹腔内播種（carcinomatosis）による体腔液貯留が進行期の特徴。予後は不良"
}

# 45. parakeet_renal_adenocarcinoma — Renal Adenocarcinoma / 腎腺癌
ENRICHMENTS["parakeet_renal_adenocarcinoma"] = {
    "diagnosis_ja": "片脚麻痺（坐骨神経叢への腫瘤圧迫が初発症状のことが多い）・腹部膨満・多飲多尿の臨床評価。腹部超音波で腎腫瘤を検出。X線で腎陰影拡大・腹腔内腫瘤影を確認。血液生化学（採血量≤体重の1%）でUA著増・電解質異常を確認。CBC で貧血・白血球変動を評価。FNA細胞診/生検で腺癌細胞を確認。インコ類の腎腺癌はセキセイインコの最も一般的な腎腫瘍であり、片脚跛行→麻痺が初発症状として来院するパターンが典型的。外科的摘出は困難で予後は不良"
}

# 46. parakeet_wing_fracture_–_humerus — Wing Fracture – Humerus / 翼骨折上腕骨型
ENRICHMENTS["parakeet_wing_fracture_–_humerus"] = {
    "diagnosis_ja": "翼の下垂・飛翔不能・上腕部の腫脹・クレピタス（骨折端の軋音）を身体検査で確認。X線（最低2方向）で上腕骨骨折の型（横・斜・螺旋・粉砕）・偏位を評価。CBC（採血量≤体重の1%）で出血性貧血を確認。血液生化学でCa・P・ALP（代謝性骨疾患の除外）を測定。インコ類の上腕骨は含気骨（pneumatic bone）であるため呼吸器系との連絡があり、開放骨折では気嚢との交通による二次感染リスクがある。IMピニング・ESF・テープスプリントで整復固定する"
}

# 47. parakeet_beak_injury_–_fracture — Beak Injury – Fracture / 嘴損傷骨折型
ENRICHMENTS["parakeet_beak_injury_–_fracture"] = {
    "diagnosis_ja": "嘴の亀裂・破折・偏位・出血を視診で確認。嘴の機能評価（採食能力・咬合パターン）。頭部X線で嘴骨の骨折線・偏位を評価。出血の止血（硝酸銀・エポキシ樹脂）。CBC（採血量≤体重の1%）で出血性貧血を確認。創傷培養で二次感染を検索。インコ類の嘴は持続成長するケラチン構造であり、軽度の亀裂はエポキシ樹脂・アクリル修復で管理可能。重度の基部骨折は嘴の永続的喪失リスクがあり、長期の経管栄養管理と複数回の外科的修復が必要となることがある"
}

# 48. parakeet_crop_candidiasis_–_neonatal — Crop Candidiasis – Neonatal / 新生児そ嚢カンジダ症
ENRICHMENTS["parakeet_crop_candidiasis_–_neonatal"] = {
    "diagnosis_ja": "幼鳥の嗉嚢内容停滞・嗉嚢膨満・嘔吐・成長遅延・食欲低下の臨床評価。嗉嚢洗浄液の鏡検でCandida albicansの出芽酵母・偽菌糸を確認。グラム染色でグラム陽性の大型酵母細胞を検出。真菌培養で菌種同定。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でTP低下・グルコース低下を測定。インコ類の新生児そ嚢カンジダ症は手差し飼育時の器具汚染・給餌温度不適切・抗菌薬使用が素因であり、ナイスタチン経口投与と衛生管理改善が治療の基本"
}

# 49. parakeet_trichomoniasis_–_crop_form — Trichomoniasis – Crop Form / トリコモナス症嗉嚢型
ENRICHMENTS["parakeet_trichomoniasis_–_crop_form"] = {
    "diagnosis_ja": "嘔吐・嗉嚢膨満・食欲低下・口腔内白色〜黄色チーズ様病変の臨床評価。嗉嚢洗浄液の直接塗抹鏡検で活発に運動するTrichomonas gallinae栄養体（10-20μm・洋梨型・4本前鞭毛と波動膜）を検出。検体は採取後速やかに鏡検（原虫運動性が急速に低下）。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。口腔内視鏡で嗉嚢粘膜の壊死性病変を評価。インコ類のトリコモナス症は嗉嚢型が多く、カンジダ症との併発も多い。メトロニダゾール経口投与が第一選択"
}

# 50. parakeet_budgerigar_pituitary_adenoma — Budgerigar Pituitary Adenoma / セキセイインコ下垂体腺腫
ENRICHMENTS["parakeet_budgerigar_pituitary_adenoma"] = {
    "diagnosis_ja": "多飲多尿・肥満・羽毛変化・神経症状（失明・旋回・痙攣：下垂体腫瘤による視交叉/脳幹圧迫）の臨床評価。頭部CT/MRI（大型種で可能）で下垂体領域の腫瘤を検出。血液生化学（採血量≤体重の1%）でグルコース変動・副腎皮質ホルモン異常を測定。CBC で全身状態を評価。神経学的検査で視覚障害・前庭障害を評価。インコ類（特にセキセイインコ）では下垂体腺腫が比較的多い脳腫瘍であり、多飲多尿が初発症状のことが多い。確定診断は剖検での病理組織検査による"
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
