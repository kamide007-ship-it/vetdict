#!/usr/bin/env python3
"""Enrich Bird diagnosis_ja — batch 6 (entries 1-50 of 233 remaining)."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 1. bird_0251 — Respiratory Neoplasia
ENRICHMENTS["bird_0251"] = {
    "diagnosis_ja": "胸部X線（VD・lateral）で肺野腫瘤影・気嚢壁不整肥厚・縦隔偏位を評価。CT検査で腫瘤の正確なサイズ・浸潤範囲・気嚢への波及を精密判定。CBC（採血量≤体重の1%、有核赤血球を手動カウント）でヘテロフィル増加・貧血を確認。FNA細胞診（超音波ガイド下）で腫瘍細胞の形態学的評価。組織生検・病理組織検査で確定診断（扁平上皮癌・腺癌・リンパ腫の鑑別）。血液生化学（AST・LDH・UA）で臓器障害を評価。気管洗浄液の細胞診で悪性細胞の有無を検索"
}

# 2. bird_0252 — Respiratory Inflammatory Disease
ENRICHMENTS["bird_0252"] = {
    "diagnosis_ja": "臨床症状の評価（開口呼吸・尾振り呼吸・鼻汁・くしゃみ）。胸部X線（VD・lateral）で肺野濃度上昇・気嚢壁肥厚・気管狭窄を評価。CBC（採血量≤体重の1%）でヘテロフィル増加・H/L比上昇（>0.8で炎症示唆）を確認。血漿蛋白電気泳動でβ-γグロブリン上昇（慢性炎症）。気管洗浄液の細胞診でヘテロフィル優位炎症パターンを評価。培養・感受性試験で起炎菌同定。鳥類は横隔膜を欠き気嚢系で換気するため、呼吸器炎症の評価には全気嚢の画像検査が不可欠"
}

# 3. bird_0253 — Lower Respiratory Tract Infection
ENRICHMENTS["bird_0253"] = {
    "diagnosis_ja": "胸部X線（VD・lateral）で肺野びまん性濃度上昇・気嚢壁肥厚・混濁を評価。CT検査で下部気道の病変範囲を正確に把握。CBC（採血量≤体重の1%）でヘテロフィル著増・H/L比上昇・単球増加を確認。気管洗浄液の細胞診・培養・感受性試験で起炎菌同定。PCR検査で特定病原体（Chlamydia psittaci・Mycoplasma等）を検出。血漿蛋白電気泳動で慢性感染のβ-γグロブリン上昇を評価。鳥類の傍気管支構造と気嚢系の連続性から、下部気道感染は容易に全気嚢に波及する"
}

# 4. bird_0254 — Chronic Respiratory Disease
ENRICHMENTS["bird_0254"] = {
    "diagnosis_ja": "詳細な病歴聴取（発症時期・経過・環境因子・同居鳥の状態）。胸部X線で気嚢壁肥厚・慢性肺野変化を評価。CT検査で気嚢肉芽腫・慢性炎症の範囲を精密判定。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多（慢性感染指標）・H/L比を確認。血漿蛋白電気泳動でγグロブリン上昇。Chlamydia psittaci PCR・Aspergillus抗原・Mycoplasma PCRの包括的病原体スクリーニング。気管洗浄液の細胞診・培養。鳥類の気嚢系は横隔膜がなく直接体腔と連続するため慢性化しやすい"
}

# 5. bird_0255 — Dermatological Bacterial Infection
ENRICHMENTS["bird_0255"] = {
    "diagnosis_ja": "皮膚病変の詳細な視診（発赤・腫脹・痂皮・潰瘍・排膿の性状と分布）。病変部の細菌培養・感受性試験で起炎菌（Staphylococcus・Pseudomonas・E. coli等）を同定。FNA細胞診でヘテロフィル浸潤と細菌貪食像を確認。CBC（採血量≤体重の1%）でヘテロフィル増加・H/L比上昇を評価。血液生化学でTP・AST・UAを測定。X線検査で深部感染による骨髄炎を除外。鳥類の皮膚は薄く皮下脂肪が乏しいため、細菌感染が急速に深部組織に波及しやすい"
}

# 6. bird_0256 — Dermatological Viral Infection
ENRICHMENTS["bird_0256"] = {
    "diagnosis_ja": "皮膚病変の詳細な視診（乳頭腫・痘疹・羽毛異常・皮膚結節の分布パターン）。PCR検査でウイルスDNA/RNAを検出（Poxvirus・Polyomavirus・Circovirus等）。皮膚生検・病理組織検査でボリンガー小体（Pox）・核内封入体等のウイルス性細胞変性効果を確認。CBC（採血量≤体重の1%）で白血球変動・貧血を評価。血清学検査（抗体価）で感染歴を確認。PBFD疑いではCircovirus PCRと羽毛パルプPCRを実施。鳥類の羽毛・嘴・爪はケラチン組織でウイルス親和性が高い"
}

# 7. bird_0257 — Dermatological Fungal Infection
ENRICHMENTS["bird_0257"] = {
    "diagnosis_ja": "皮膚病変の視診（脱羽・痂皮・鱗屑・結節・色素変化の分布パターン）。皮膚掻破検査でKOH直接鏡検により真菌菌糸・分節胞子を確認。真菌培養（Sabouraud寒天・DTM培地）で起炎真菌の同定と感受性評価。皮膚生検・病理組織検査でPAS染色陽性の真菌要素を確認。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多を評価。血液生化学でAST・TPを測定。鳥類の皮膚は薄く角質層が未発達なため真菌の侵入障壁が低く、環境性真菌（Aspergillus・Mucor等）にも感受性が高い"
}

# 8. bird_0258 — Dermatological Parasitic Infestation
ENRICHMENTS["bird_0258"] = {
    "diagnosis_ja": "皮膚・羽毛の詳細な視診（掻痒・脱羽・痂皮・過角化の分布）。皮膚掻破検査で外部寄生虫（Cnemidocoptes・Dermanyssus・Ornithonyssus等）を顕微鏡下で同定。羽毛検査でMallophaga（咀嚼シラミ）の虫体・虫卵を確認。CBC（採血量≤体重の1%）で好酸球増加・ヘテロフィル変動を評価。血液生化学でTP低下（慢性寄生による栄養障害）を確認。セロハンテープ法で体表のダニ・シラミを採取。鳥類ではCnemidocoptes pilaeによる嘴・脚の過角化病変が特徴的"
}

# 9. bird_0259 — Dermatological Neoplasia
ENRICHMENTS["bird_0259"] = {
    "diagnosis_ja": "皮膚腫瘤の視診・触診（サイズ・硬さ・可動性・色調・表面性状を記録）。FNA細胞診で腫瘍細胞の形態学的評価（扁平上皮癌・線維肉腫・脂肪腫・黄色腫の鑑別）。組織生検・病理組織検査で確定診断と悪性度判定。X線・CT検査で深部浸潤・骨侵襲・転移を評価。CBC（採血量≤体重の1%）で貧血・ヘテロフィル変動を確認。血液生化学（AST・LDH・UA）で全身状態を評価。鳥類ではXanthoma（黄色腫）が高脂肪食で多発し、真の腫瘍との鑑別が重要"
}

# 10. bird_0260 — Dermatological Autoimmune Disease
ENRICHMENTS["bird_0260"] = {
    "diagnosis_ja": "皮膚病変の分布パターン評価（対称性・粘膜皮膚接合部・羽毛濾胞周囲の病変に注目）。皮膚生検・病理組織検査で表皮内水疱・界面皮膚炎・リンパ球浸潤パターンを評価。直接免疫蛍光法でIgG/IgM/C3の沈着を確認。CBC（採血量≤体重の1%）でリンパ球変動・ヘテロフィル増減を評価。血液生化学でTP・グロブリン分画を測定。感染性皮膚炎の除外（培養・PCR）。鳥類の自己免疫性皮膚疾患は稀だが、天疱瘡様疾患の報告があり、嘴・脚の痂皮性病変として発現しうる"
}

# 11. bird_0261 — Dermatological Allergic Disease
ENRICHMENTS["bird_0261"] = {
    "diagnosis_ja": "詳細な環境歴・食餌歴の聴取（新規素材・洗剤・芳香剤・煙草煙への曝露）。皮膚病変の視診（掻痒・発赤・自己損傷による脱羽パターン）。皮膚生検で好酸球性・リンパ球性炎症を評価。CBC（採血量≤体重の1%）で好酸球増加を確認（鳥類では好酸球は少数のため軽度増加でも有意）。血液生化学でTPを測定。感染性原因（細菌・真菌・寄生虫）の除外。除去食試験（2-4週間）で食物アレルギーを評価。鳥類のアレルギーは行動性毛引きとの鑑別が臨床上最も重要"
}

# 12. bird_0262 — Chronic Dermatitis
ENRICHMENTS["bird_0262"] = {
    "diagnosis_ja": "慢性皮膚病変の詳細な視診（苔癬化・色素沈着・瘢痕化・慢性脱羽パターン）。病歴聴取（発症時期・経過・治療歴・環境変化）。皮膚掻破・培養で感染性原因を除外。皮膚生検・病理組織検査で慢性炎症パターン（線維化・リンパ球浸潤）を評価。CBC（採血量≤体重の1%）で慢性炎症マーカー（単球増多・H/L比）を確認。血漿蛋白電気泳動でγグロブリン上昇。甲状腺機能検査（T4）で内分泌性脱羽を除外。鳥類の慢性皮膚炎では行動性毛引き・栄養欠乏・低湿度環境の関与を系統的に評価"
}

# 13. bird_0263 — Urogenital Bacterial Infection
ENRICHMENTS["bird_0263"] = {
    "diagnosis_ja": "排泄腔スワブの細菌培養・感受性試験で起炎菌（E. coli・Klebsiella・Pseudomonas等）を同定。尿酸・糞便の外観変化（多尿・尿酸色調変化）を評価。CBC（採血量≤体重の1%）でヘテロフィル増加・H/L比上昇を確認。血液生化学でUA上昇・BUN上昇・AST変動を測定。腹部X線・超音波で腎腫大・卵管腫脹・排泄腔異常を評価。鳥類は腎臓と生殖器が密接に隣接し、排泄腔で尿路・消化管・生殖管が合流するため、泌尿生殖器感染は急速に全系統に波及する"
}

# 14. bird_0264 — Urogenital Neoplasia
ENRICHMENTS["bird_0264"] = {
    "diagnosis_ja": "腹部X線（VD・lateral）で腎腫大・腹腔内腫瘤影・骨盤変位を評価。超音波検査で腎実質エコー異常・卵巣/精巣腫瘤を描出。CT検査で腫瘤の正確な範囲・浸潤度を判定。FNA細胞診で腫瘍細胞の形態評価（腎細胞癌・精巣腫瘍・卵巣腫瘍の鑑別）。CBC（採血量≤体重の1%）で貧血・ヘテロフィル変動を確認。血液生化学（UA・BUN）で腎機能を評価。鳥類ではセキセイインコの腎腫瘍が好発し、坐骨神経圧迫による片脚麻痺が初発症状となることが多い"
}

# 15. bird_0265 — Urogenital Inflammatory Disease
ENRICHMENTS["bird_0265"] = {
    "diagnosis_ja": "排泄腔の視診（発赤・腫脹・分泌物の性状）。排泄腔スワブの細胞診でヘテロフィル浸潤を評価。腹部X線・超音波で腎腫大・卵管壁肥厚・体腔内液体貯留を評価。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多を確認。血液生化学でUA上昇・AST上昇・TP変動を測定。培養・PCR検査で感染性原因を除外。尿酸排泄の変化（多尿・尿酸結晶異常）を観察。鳥類は尿酸排泄型であり、炎症による尿酸クリアランス低下は急速に高尿酸血症・内臓痛風を惹起する"
}

# 16. bird_0266 — Urogenital Congenital Anomaly
ENRICHMENTS["bird_0266"] = {
    "diagnosis_ja": "幼鳥期からの泌尿生殖器症状の経過確認。腹部X線・超音波で腎の形態異常（無形成・低形成・嚢胞腎）・卵管/精巣の構造異常を評価。排泄腔の視診で形態異常（閉鎖・狭窄・総排泄腔外反）を確認。CBC（採血量≤体重の1%）・血液生化学（UA・BUN）で腎機能を評価。CT検査で複雑な構造異常の三次元的把握。鳥類は総排泄腔に泌尿・消化・生殖管が合流する特殊構造のため、先天異常は複数系統に同時に影響しうる。遺伝的背景の評価も重要"
}

# 17. bird_0267 — Neurological Bacterial Infection
ENRICHMENTS["bird_0267"] = {
    "diagnosis_ja": "神経学的検査（姿勢反射・脳神経評価・瞳孔対光反射・握力）で病変局在を推定。CBC（採血量≤体重の1%）でヘテロフィル著増・H/L比上昇・単球増多を確認。血液生化学でAST・LDH・グルコース変動を評価。頭部X線・CT/MRIで脳実質病変・膿瘍を検索。細菌培養・感受性試験（血液・排泄腔スワブ）で起炎菌同定。鳥類の脳脊髄液採取は後頭下穿刺で可能だが体格制限あり。E. coli・Pasteurella・Listeria等の血行性播種による髄膜脳炎を鑑別"
}

# 18. bird_0268 — Neurological Viral Infection
ENRICHMENTS["bird_0268"] = {
    "diagnosis_ja": "神経学的検査で運動失調・斜頸・頭部振戦・痙攣・眼振・star-gazingを系統的に評価。CBC（採血量≤体重の1%）でリンパ球変動を確認。PCR検査で特定ウイルス（ABV/PaBV・Paramyxovirus・Polyomavirus・Avian Encephalomyelitis Virus等）を検出。血清学的検査で抗体価を測定。CT/MRI（大型鳥で実施可能）で脳実質病変を評価。ABV/PaBV抗体・PCR陽性はPDD神経型を強く示唆。鳥類のウイルス性脳炎では急速な代謝低下（高代謝率のため）が予後を左右する"
}

# 19. bird_0269 — Neurological Parasitic Disease
ENRICHMENTS["bird_0269"] = {
    "diagnosis_ja": "神経学的検査で病変局在を推定（運動失調・頭部傾斜・旋回運動・肢麻痺）。CBC（採血量≤体重の1%）で好酸球増加を確認（寄生虫感染示唆）。血液塗抹でHaemoproteus・Plasmodium等の血液寄生虫を検索。糞便検査（直接塗抹・浮遊法）で消化管寄生虫の虫卵を検出。頭部CT/MRIで脳実質内の寄生虫移行巣を検索。Baylisascaris幼虫移行症では脳好酸球性肉芽腫が特徴的。鳥類ではSarcocystis等の原虫による脳脊髄炎も鑑別に含める"
}

# 20. bird_0270 — Neurological Neoplasia
ENRICHMENTS["bird_0270"] = {
    "diagnosis_ja": "神経学的検査で病変局在を推定（片側性脳神経麻痺→小脳橋角部、両側性運動失調→小脳）。頭部CT/MRI（大型鳥で実施可能）で脳内腫瘤・脊髄圧迫病変を評価。CBC（採血量≤体重の1%）で貧血・白血球異常を確認。血液生化学でLDH上昇・AST上昇を評価。FNA細胞診（体表腫瘤併発時）で腫瘍型を推定。鳥類ではリンパ腫・下垂体腺腫が神経症状の原因として多く、セキセイインコの腎腫瘍による坐骨神経圧迫も鑑別に含める。剖検・病理が確定診断の主要手段"
}

# 21. bird_0271 — Neurological Degenerative Disease
ENRICHMENTS["bird_0271"] = {
    "diagnosis_ja": "神経学的検査で進行性の運動失調・筋萎縮・姿勢異常を評価（発症年齢・進行速度を記録）。CBC（採血量≤体重の1%）・血液生化学で代謝性・栄養性原因を除外（VitE・VitB1・Ca欠乏）。頭部CT/MRIで構造的病変を除外。ABV/PaBV PCR・抗体検査でPDD（腺胃拡張症の神経型）を鑑別。鳥類の変性性神経疾患は生前確定診断が困難で、臨床経過と除外診断に基づく推定診断が主体。老齢鳥の進行性運動障害では脊髄変性・末梢神経障害を考慮する"
}

# 22. bird_0272 — Neurological Inflammatory Disease
ENRICHMENTS["bird_0272"] = {
    "diagnosis_ja": "神経学的検査で炎症性病変の局在を推定（脳炎→意識障害・痙攣、脊髄炎→四肢麻痺）。CBC（採血量≤体重の1%）でヘテロフィル/単球増多・リンパ球変動を確認。血漿蛋白電気泳動でγグロブリン上昇。感染性原因のスクリーニング（Chlamydia PCR・ABV PCR・細菌培養）。頭部CT/MRI（大型鳥で実施可能）で脳実質の炎症性変化を評価。血液生化学でAST・LDH・CK上昇を確認。鳥類の非感染性脳脊髄炎は報告が限られるが、ABV関連の非化膿性脳脊髄炎が最も重要な鑑別疾患"
}

# 23. bird_0273 — Neurological Traumatic Injury
ENRICHMENTS["bird_0273"] = {
    "diagnosis_ja": "外傷歴の聴取（窓への衝突・落下・他動物による咬傷等）。神経学的検査で意識レベル・瞳孔反射・脳神経機能・四肢運動機能を系統的に評価。頭部・脊椎X線で骨折・脱臼を検索。CT検査で頭蓋内出血・脳浮腫・脊椎変位を評価。CBC（採血量≤体重の1%）でPCV低下（出血性）・ヘテロフィル増加（ストレス）を確認。血液生化学でCK上昇（筋損傷）・グルコース変動を測定。鳥類の頭部外傷では気腔構造（副鼻腔・含気骨）が緩衝となるが、小型種では脳震盪の重症度が高い"
}

# 24. bird_0274 — Neurological Metabolic Disease
ENRICHMENTS["bird_0274"] = {
    "diagnosis_ja": "血液生化学（採血量≤体重の1%）でCa（低Ca痙攣）・グルコース（低血糖発作）・UA・電解質を測定。肝機能検査（AST・胆汁酸・TP）で肝性脳症を評価。甲状腺機能検査（T4）。ビタミンB群（B1・B6・B12）欠乏の評価。神経学的検査で代謝性脳症パターン（対称性・びまん性の神経機能障害）を確認。食餌歴の詳細聴取（種子食偏重は多種ビタミン欠乏のリスク）。鳥類は高代謝率のため低血糖に極めて脆弱で、4-6時間の絶食で神経症状が出現しうる"
}

# 25. bird_0275 — Ophthalmological Bacterial Infection
ENRICHMENTS["bird_0275"] = {
    "diagnosis_ja": "眼科検査（拡大鏡・スリットランプ）で結膜充血・眼脂・角膜混濁・前房蓄膿を評価。フルオレセイン染色で角膜潰瘍の有無と範囲を確認。眼脂の細菌培養・感受性試験で起炎菌（Staphylococcus・Pseudomonas・Mycoplasma等）を同定。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。副鼻腔X線・CTで副鼻腔炎の眼窩波及を除外。鳥類の眼は頭部体積の大部分を占め、強膜骨輪で固定されているため、眼窩感染は急速に視力喪失をもたらす"
}

# 26. bird_0276 — Ophthalmological Viral Infection
ENRICHMENTS["bird_0276"] = {
    "diagnosis_ja": "眼科検査で結膜炎・角膜炎・ぶどう膜炎・眼瞼腫脹を評価。フルオレセイン染色で角膜潰瘍を確認。PCR検査（結膜スワブ・涙液）でウイルス（Avian Poxvirus・Paramyxovirus-1・Marek's Disease Virus等）を検出。CBC（採血量≤体重の1%）でリンパ球変動を確認。副鼻腔X線で副鼻腔炎併発を評価。Chlamydia psittaci PCR（眼結膜炎の重要な鑑別）。鳥類ではPoxvirus感染による眼瞼の痘疹性病変が特徴的で、二次性角膜損傷のリスクが高い"
}

# 27. bird_0277 — Ophthalmological Neoplasia
ENRICHMENTS["bird_0277"] = {
    "diagnosis_ja": "眼科検査で腫瘤の位置・サイズ・眼球/眼瞼/眼窩の関与を評価。スリットランプで前眼部腫瘤の詳細観察。眼窩超音波で眼球後方腫瘤を描出。頭部CT/MRIで眼窩内腫瘤の範囲・骨浸潤を判定。FNA細胞診で腫瘍型を推定（扁平上皮癌・メラノーマ・リンパ腫）。組織生検・病理組織検査で確定診断。CBC（採血量≤体重の1%）で全身状態を評価。鳥類の眼窩腫瘍は強膜骨輪の存在により眼球突出として顕在化しやすく、副鼻腔膿瘍との鑑別が重要"
}

# 28. bird_0278 — Ophthalmological Degenerative Disease
ENRICHMENTS["bird_0278"] = {
    "diagnosis_ja": "眼科検査（スリットランプ・眼底検査・眼圧測定）で白内障・網膜変性・角膜変性を系統的に評価。ERG（網膜電図、大型鳥で実施可能）で網膜機能を客観的に評価。超音波検査（Bモード）で水晶体混濁度・硝子体変性を確認。CBC・血液生化学（採血量≤体重の1%）で代謝性原因（糖尿病・腎不全）を除外。食餌歴聴取でVitA・VitE欠乏を評価。鳥類は視覚優位動物であり、変性性眼疾患は行動変化（止まり木からの落下・衝突）として初めて気づかれることが多い"
}

# 29. bird_0279 — Ophthalmological Congenital Anomaly
ENRICHMENTS["bird_0279"] = {
    "diagnosis_ja": "幼鳥期からの眼異常の経過確認。眼科検査で小眼球・無眼球・眼瞼欠損・虹彩異形成・水晶体脱臼を評価。スリットランプで前眼部の構造異常を詳細観察。超音波検査（Bモード）で眼球内部構造の先天異常を描出。頭部X線で眼窩骨格異常を確認。CBC・血液生化学（採血量≤体重の1%）で全身状態を評価。遺伝的背景の聴取（近親交配歴）。鳥類では色素変異個体（ルチノー・アルビノ）に先天性眼異常が多く、視覚障害が行動異常として表れる"
}

# 30. bird_0280 — Cardiovascular Bacterial Infection
ENRICHMENTS["bird_0280"] = {
    "diagnosis_ja": "聴診で心雑音・不整脈を評価（鳥類の正常心拍数は小型種300-600 bpm）。胸部X線で心拡大・肺うっ血・肝腫大を確認。心エコーで弁膜疣贅・心嚢液・心機能低下を評価。CBC（採血量≤体重の1%）でヘテロフィル著増・H/L比上昇を確認。血液培養で菌血症を証明。血液生化学でAST・LDH・CK上昇（心筋障害）を評価。鳥類は4腔心で右大動脈弓を有し、心内膜炎はStaphylococcus・Streptococcus・E. coli等による血行性感染が主因"
}

# 31. bird_0281 — Cardiovascular Neoplasia
ENRICHMENTS["bird_0281"] = {
    "diagnosis_ja": "胸部X線で心陰影の異常拡大・不整形を評価。心エコーで心腔内腫瘤・心嚢液・心筋壁異常を描出。CT検査で腫瘤の範囲・大血管との関係を精密判定。CBC（採血量≤体重の1%）で貧血・白血球異常を確認。血液生化学でAST・LDH・CK上昇を評価。心嚢穿刺液の細胞診で腫瘍細胞を検索。鳥類の心臓腫瘍は稀だが、リンパ腫・血管肉腫・横紋筋腫が報告されている。心嚢液貯留による心タンポナーデは急性死の原因となりうる"
}

# 32. bird_0282 — Cardiovascular Degenerative Disease
ENRICHMENTS["bird_0282"] = {
    "diagnosis_ja": "聴診で心雑音・不整脈を評価。胸部X線で心拡大像・肝うっ血・肺野変化を確認。心エコーで弁膜変性（弁肥厚・逆流）・心室壁運動低下・FS低下を測定。心電図で不整脈パターンを記録。CBC・血液生化学（採血量≤体重の1%）でAST・LDH・UA・コレステロールを測定。鳥類の動脈硬化症はアマゾン・ヨウム・コンゴウインコ等の老齢大型鳥に多発し、高脂肪種子食が主要リスク因子。心臓バイオマーカー（cTnI）の上昇は心筋障害を示唆"
}

# 33. bird_0283 — Cardiovascular Inflammatory Disease
ENRICHMENTS["bird_0283"] = {
    "diagnosis_ja": "聴診で心雑音・摩擦音・不整脈を評価。胸部X線で心拡大・心嚢液貯留像を確認。心エコーで心嚢液・心筋壁エコー異常・弁膜炎性変化を描出。心電図で炎症に伴うST変化・不整脈を記録。CBC（採血量≤体重の1%）でヘテロフィル増加・H/L比上昇を確認。血漿蛋白電気泳動でγグロブリン上昇。血液培養・Chlamydia PCRで感染性心筋炎の原因を検索。鳥類ではChlamydia psittaciによる心嚢炎・心筋炎が重要で、呼吸器症状に先行することがある"
}

# 34. bird_0284 — Cardiovascular Congenital Anomaly
ENRICHMENTS["bird_0284"] = {
    "diagnosis_ja": "幼鳥期からの運動不耐性・チアノーゼ・成長遅延の経過確認。聴診で先天性心雑音を評価。胸部X線で心陰影異常・肺血管パターンを確認。心エコーで心室中隔欠損・心房中隔欠損・動脈管開存・大血管転位等を描出。心電図で心腔負荷パターンを記録。CBC・血液生化学（採血量≤体重の1%）で多血症（右左シャント時）・低酸素を評価。鳥類は右大動脈弓が正常であり、哺乳類の先天性心疾患分類をそのまま適用できない点に注意が必要"
}

# 35. bird_0285 — Musculoskeletal Bacterial Infection
ENRICHMENTS["bird_0285"] = {
    "diagnosis_ja": "患肢の視診・触診（腫脹・熱感・疼痛・可動域制限）。X線検査で骨溶解像・骨膜反応・関節腫脹を評価。FNA細胞診・関節液分析でヘテロフィル優位炎症と細菌を確認。細菌培養・感受性試験で起炎菌（Staphylococcus aureus・E. coli等）を同定。CBC（採血量≤体重の1%）でヘテロフィル著増・H/L比上昇を確認。血液生化学でAST・UA上昇を評価。鳥類の含気骨は骨髄腔と気嚢が連続しているため、骨感染が気嚢炎に波及しやすい特異的リスクがある"
}

# 36. bird_0286 — Musculoskeletal Neoplasia
ENRICHMENTS["bird_0286"] = {
    "diagnosis_ja": "患肢・体幹の腫瘤の視診・触診（硬さ・可動性・骨との癒着を評価）。X線検査で骨破壊像・骨新生・軟部組織腫瘤影を確認。CT検査で腫瘤の正確な範囲・骨浸潤度を判定。FNA細胞診で腫瘍型を推定（骨肉腫・軟骨肉腫・線維肉腫の鑑別）。組織生検・病理組織検査で確定診断と悪性度評価。CBC（採血量≤体重の1%）で貧血・白血球異常を確認。鳥類の含気骨では骨腫瘍が病的骨折を起こしやすく、翼・脛足根骨に好発する"
}

# 37. bird_0287 — Musculoskeletal Degenerative Disease
ENRICHMENTS["bird_0287"] = {
    "diagnosis_ja": "患肢の視診・触診で関節腫脹・可動域制限・疼痛反応を評価。X線検査で関節腔狭小化・骨棘形成・軟骨下骨硬化を確認。CBC・血液生化学（採血量≤体重の1%）で栄養性因子（Ca・P・VitD3）を測定。食餌歴・飼育環境の聴取（不適切な止まり木サイズ・硬さ）。関節液分析で炎症性/非炎症性を鑑別。鳥類では足底潰瘍（bumblefoot）との合併が多く、不適切な止まり木→足底圧集中→関節変性の悪循環を形成する。老齢大型鳥に好発"
}

# 38. bird_0288 — Musculoskeletal Congenital Anomaly
ENRICHMENTS["bird_0288"] = {
    "diagnosis_ja": "幼鳥の四肢・翼の視診で変形・短縮・回旋異常を確認。X線検査で骨格異常（多指症・合指症・肢欠損・翼変形）を評価。全身X線で脊椎・骨盤の先天異常を検索。CBC・血液生化学（採血量≤体重の1%）で栄養状態を評価。食餌歴聴取（親鳥の栄養状態・育雛時のVitA/D3/Ca不足）。鳥類ではSplay Leg（開脚症）が滑りやすい巣材で多発し、早期の肢固定で矯正可能。Angel Wing（天使の翼）は成長期の過剰蛋白摂取が原因とされる"
}

# 39. bird_0289 — Musculoskeletal Inflammatory Disease
ENRICHMENTS["bird_0289"] = {
    "diagnosis_ja": "患部の視診・触診で腫脹・発赤・熱感・疼痛を評価。X線検査で軟部組織腫脹・骨膜反応・関節液貯留を確認。関節液分析（関節穿刺）でヘテロフィル浸潤・蛋白上昇を評価。細菌培養で感染性関節炎を除外。CBC（採血量≤体重の1%）でヘテロフィル増加・H/L比上昇を確認。血液生化学でUA上昇（痛風性関節炎の鑑別）・CK上昇（筋炎）を測定。鳥類の関節炎では痛風（尿酸結晶沈着）が最も重要な鑑別疾患で、関節液の偏光顕微鏡検査で尿酸結晶を確認"
}

# 40. bird_0290 — Musculoskeletal Nutritional Deficiency
ENRICHMENTS["bird_0290"] = {
    "diagnosis_ja": "食餌歴の詳細聴取（種子食偏重・Ca/P比不適切・UVBライト不使用）。全身X線で骨密度低下・病的骨折・骨変形・皮質菲薄化を評価。血液生化学（採血量≤体重の1%）でCa・P・ALP・VitD3を測定。竜骨・長管骨の触診で骨軟化を確認。CBC でヘテロフィル変動を評価。鳥類ではMBD（代謝性骨疾患）が種子食偏重の飼育鳥で極めて多く、Ca:P比の不適切（理想は2:1）とUVB不足によるVitD3活性化障害が主因。幼鳥の嘴軟化・脚変形は早期介入が必要"
}

# 41. bird_0291 — Endocrine Bacterial Infection
ENRICHMENTS["bird_0291"] = {
    "diagnosis_ja": "内分泌臓器の二次感染を疑う臨床所見の評価（甲状腺領域腫脹・多飲多尿・体重変動）。血液生化学（採血量≤体重の1%）でホルモン値（T4・コルチコステロン）と臓器マーカー（AST・UA）を測定。CBC でヘテロフィル増加・H/L比上昇を確認。細菌培養・感受性試験で起炎菌を同定。腹部超音波・X線で副腎・甲状腺・膵臓の腫大を評価。鳥類では副腎の感染性炎症がアスペルギルス等の全身性真菌症に続発することがあり、コルチコステロン分泌障害を惹起する"
}

# 42. bird_0292 — Endocrine Neoplasia
ENRICHMENTS["bird_0292"] = {
    "diagnosis_ja": "内分泌関連の臨床症状評価（多飲多尿・肥満/削痩・羽毛異常・行動変化）。血液生化学（採血量≤体重の1%）でホルモン値（T4・コルチコステロン・インスリン・性ホルモン）を測定。腹部超音波・X線で内分泌臓器（甲状腺・副腎・生殖腺）の腫大を評価。CT検査で腫瘤の範囲・浸潤度を判定。FNA細胞診で腫瘍細胞を評価。鳥類ではセキセイインコの甲状腺腺腫が多く、気管圧迫による呼吸困難が主訴となる。下垂体腺腫は多飲多尿・肥満を呈する"
}

# 43. bird_0293 — Endocrine Metabolic Disorder
ENRICHMENTS["bird_0293"] = {
    "diagnosis_ja": "血液生化学（採血量≤体重の1%）でグルコース・Ca・P・UA・電解質・コレステロール・中性脂肪を測定。ホルモン検査（T4・コルチコステロン）で甲状腺/副腎機能を評価。食餌歴の詳細聴取（高脂肪種子食→脂質代謝異常）。体重・BCS（胸筋触診）で栄養状態を判定。鳥類は高代謝率のため内分泌障害の臨床発現が急速で、甲状腺機能低下は肥満・脂肪肝・産卵障害として現れる。糖尿病は稀だが主にオウム目で報告があり、持続的高血糖（>400 mg/dL）で診断"
}

# 44. bird_0294 — Endocrine Autoimmune Disease
ENRICHMENTS["bird_0294"] = {
    "diagnosis_ja": "内分泌機能低下を示す臨床症状の評価（肥満・脱羽・嗜眠・産卵障害）。血液生化学（採血量≤体重の1%）でホルモン基礎値（T4・コルチコステロン）を測定。TSH刺激試験（T4の反応評価）。ACTH刺激試験（コルチコステロン反応）。CBC でリンパ球増加（ストレスロイコグラム欠如）を確認。抗甲状腺抗体の測定（利用可能な場合）。鳥類の自己免疫性内分泌疾患は報告が限られるが、甲状腺炎がセキセイインコで記載されている。除外診断的アプローチが主体"
}

# 45. bird_0295 — Endocrine Nutritional Disorder
ENRICHMENTS["bird_0295"] = {
    "diagnosis_ja": "食餌歴の詳細聴取（ヨウ素欠乏→甲状腺過形成、種子食偏重→多種ビタミン/ミネラル欠乏）。血液生化学（採血量≤体重の1%）でCa・P・T4・VitA・VitD3を測定。頸部触診・X線で甲状腺腫大を確認（特にセキセイインコ：ヨウ素欠乏で顕著）。全身X線で骨密度・骨変形を評価。鳥類ではヨウ素欠乏性甲状腺腫が最も重要な栄養性内分泌疾患で、種子食（特にアワ・ヒエ）のみの飼育鳥に多発。甲状腺腫大による気管圧迫が呼吸困難・嘔吐の原因となる"
}

# 46. bird_0296 — Endocrine Degenerative Disease
ENRICHMENTS["bird_0296"] = {
    "diagnosis_ja": "内分泌機能低下を示す慢性進行性症状の評価（体重変動・羽毛質低下・活動性低下）。血液生化学（採血量≤体重の1%）でホルモン基礎値（T4・コルチコステロン）を測定。動的負荷試験（TSH刺激試験・ACTH刺激試験）で内分泌予備能を評価。腹部超音波で副腎・甲状腺の萎縮性変化を検索。CBC で慢性変化（リンパ球優位）を確認。鳥類の老齢化に伴う内分泌機能低下は十分に研究されていないが、老齢大型鳥での甲状腺機能低下・副腎機能低下が臨床的に示唆される"
}

# 47. bird_0297 — Hematological Neoplasia
ENRICHMENTS["bird_0297"] = {
    "diagnosis_ja": "CBC（採血量≤体重の1%、有核赤血球を手動カウント）で白血球の著増・異型細胞・芽球の出現を確認。末梢血塗抹のライト・ギムザ染色で異型リンパ球・前駆細胞を形態評価。血液生化学でLDH・AST・UA上昇を測定。腹部X線・超音波で肝脾腫・腎腫大を評価。骨髄穿刺・細胞診（竜骨・脛足根骨から採取）で芽球比率を確認。鳥類のリンパ腫/白血病はマレック病ウイルス・鳥白血病ウイルス関連が家禽で多く、オウム目では自発性リンパ腫が報告される"
}

# 48. bird_0298 — Hematological Infectious Disease
ENRICHMENTS["bird_0298"] = {
    "diagnosis_ja": "CBC（採血量≤体重の1%）でヘテロフィル増加・リンパ球減少・貧血（PCV・赤血球形態）を評価。末梢血塗抹でHaemoproteus・Plasmodium・Leucocytozoon等の血液寄生虫を検索。PCR検査で特定病原体を検出。血液培養で菌血症を証明。血液生化学でAST・LDH・TP変動を測定。鳥類の有核赤血球は寄生虫が細胞内に侵入する標的となり、Haemoproteusの配偶子母体が赤血球内に観察される。Plasmodiumは脾腫・肝腫大を伴い急性死を起こしうる"
}

# 49. bird_0299 — Hematological Autoimmune Disease
ENRICHMENTS["bird_0299"] = {
    "diagnosis_ja": "CBC（採血量≤体重の1%）でPCV低下・網状赤血球増加（再生性貧血）を確認。末梢血塗抹で球状赤血球・赤血球凝集を検索。自己凝集試験（生理食塩水希釈試験）で自己免疫性溶血を評価。血液生化学でビリベルジン上昇（鳥類はビリルビンでなくビリベルジンが主要胆汁色素）・AST・LDHを測定。鳥類の自己免疫性血液疾患は報告が限られるが、免疫介在性溶血性貧血・血小板減少症が記載されている。感染性・中毒性貧血の除外が診断の鍵"
}

# 50. bird_0300 — Hematological Metabolic Disease
ENRICHMENTS["bird_0300"] = {
    "diagnosis_ja": "CBC（採血量≤体重の1%、有核赤血球を手動カウント）でPCV・赤血球形態・白血球分画を評価。血液生化学でFe・TIBC（鉄欠乏性貧血）・VitB12・葉酸（巨赤芽球性貧血）を測定。血漿蛋白電気泳動でTP・アルブミンを評価。食餌歴の詳細聴取（種子食偏重によるFe・VitE・VitB12欠乏）。肝機能検査（AST・胆汁酸）で肝疾患関連凝固障害を除外。鳥類ではFe貯蔵障害（ヘモクロマトーシス）がオオハシ・ムクドリ等で好発し、肝鉄沈着による慢性肝障害を惹起する"
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
