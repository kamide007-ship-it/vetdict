#!/usr/bin/env python3
"""Enrich Bird diagnosis_ja — batch 10 (entries 201-233, final batch)."""
import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 201. bird_thyroid_hyperplasia_–_tracheal_compression — Thyroid Hyperplasia – Tracheal Compression
ENRICHMENTS["bird_thyroid_hyperplasia_–_tracheal_compression"] = {
    "diagnosis_ja": "呼吸困難・吸気性喘鳴（ストリドール）・嚥下困難・声の変化の臨床評価。頸部触診で甲状腺領域の腫大を確認。頸部X線・CTで甲状腺腫大による気管圧迫・偏位を検出。血液生化学（採血量≤体重の1%）でT4低下（甲状腺機能低下）を確認。食餌歴の聴取（ヨード欠乏：種子食偏重・キャベツ等のゴイトロゲン含有食の過剰摂取）。鳥類ではセキセイインコの甲状腺過形成がヨード欠乏で最も多く発生し、気管圧迫による呼吸困難が致命的となりうる。ヨード補充で過形成は退縮する"
}

# 202. bird_vitamin_a_deficiency_–_oral_abscesses — Vitamin A Deficiency – Oral Abscesses
ENRICHMENTS["bird_vitamin_a_deficiency_–_oral_abscesses"] = {
    "diagnosis_ja": "口腔内の白色結節・膿瘍（扁平上皮化生に伴う粘膜下膿瘍）を口腔検査で確認。後鼻孔（choana）の鈍化・乳頭消失を評価。嗉嚢・食道粘膜の白色病変を検索。食餌歴の詳細聴取（種子食偏重→VitA不足）。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。血液生化学でVitA値を測定（正常値は種により異なる）。鳥類のVitA欠乏は上皮組織の扁平上皮化生を引き起こし、口腔・後鼻孔・唾液腺の膿瘍形成が特徴的。VitA補充と口腔膿瘍のデブリードマンが治療の基本"
}

# 203. bird_calcium_deficiency_–_reproductive_laying_hens — Calcium Deficiency – Reproductive (Laying Hens)
ENRICHMENTS["bird_calcium_deficiency_–_reproductive_laying_hens"] = {
    "diagnosis_ja": "産卵鳥の薄殻卵・軟殻卵・卵詰まり・病的骨折・痙攣の臨床評価。血液生化学（採血量≤体重の1%）で総Ca低下（<8 mg/dL）・イオン化Ca低下・P上昇を確認。X線で骨密度低下（皮質菲薄化・髄質骨減少）・病的骨折・卵殻石灰化不全を評価。食餌歴の聴取（Ca:P比不適切・カットルボーン/鉱物補充不足）。鳥類の産卵関連低Ca血症は慢性産卵鳥で骨Ca貯蔵が枯渇して発症し、重度低Ca血症は痙攣・テタニー→急性死に至る。緊急Ca補充（グルコン酸Ca静注）が救命に必要"
}

# 204. bird_proventricular_impaction — Proventricular Impaction / 腺胃閉塞
ENRICHMENTS["bird_proventricular_impaction"] = {
    "diagnosis_ja": "嘔吐・食欲廃絶・嗉嚢内容停滞・体重減少の臨床評価。腹部X線で拡張した前胃（proventriculus）と高密度内容物（砂礫・異物蓄積）を検出。造影X線で消化管通過遅延を確認。腹部超音波で前胃壁肥厚を評価。CBC（採血量≤体重の1%）でヘテロフィル変動を確認。血液生化学でTP低下・グルコース低下を測定。内視鏡で前胃内の閉塞性内容物を直視確認。鳥類の前胃閉塞は異物摂取・筋胃機能障害・PDD（前胃拡張症）・線虫感染に続発し、前胃の運動性低下が閉塞を増悪させる"
}

# 205. bird_gastric_dilatation_non-pdd — Gastric Dilatation (Non-PDD) / 胃拡張（PDD以外）
ENRICHMENTS["bird_gastric_dilatation_non-pdd"] = {
    "diagnosis_ja": "嗉嚢内容停滞・嘔吐・腹部膨満・体重減少の臨床評価。腹部X線で前胃・筋胃の拡張を確認（PDD除外が前提）。造影X線で消化管通過時間を測定。ABV-PCR検査でABV（Avian Bornavirus: PDD原因ウイルス）を除外。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でTP・グルコース変動を測定。異物・重金属中毒・消化管腫瘍・線虫感染を鑑別。鳥類のPDD以外の胃拡張は異物性・神経原性・感染性等の原因で発生し、PDD除外が診断の第一歩"
}

# 206. bird_ventricular_foreign_body_gizzard — Ventricular Foreign Body (Gizzard) / 筋胃異物
ENRICHMENTS["bird_ventricular_foreign_body_gizzard"] = {
    "diagnosis_ja": "食欲低下・嘔吐・体重減少・便の異常の臨床評価。腹部X線で筋胃（gizzard）内の異物（金属片・プラスチック・砂利過多等）を検出。造影X線で消化管通過障害を確認。血中鉛・亜鉛濃度測定で重金属異物を評価。CBC（採血量≤体重の1%）でヘテロフィル変動を確認。血液生化学でAST・UA変動を測定。内視鏡で筋胃内異物を直視確認・可能であれば摘出。鳥類は探索行動で様々な異物を摂取し、金属異物は重金属中毒を併発するリスクがある。外科的摘出が必要な場合がある"
}

# 207. bird_intestinal_intussusception — Intestinal Intussusception / 腸重積
ENRICHMENTS["bird_intestinal_intussusception"] = {
    "diagnosis_ja": "急性の嘔吐・血便（暗赤色便）・腹部疼痛・急性沈鬱の臨床評価。腹部超音波でtarget sign（同心円状腸管断面: 腸重積の典型的所見）を検出。腹部X線で腸管拡張・腸閉塞パターンを確認。造影X線で陰影欠損を評価。CBC（採血量≤体重の1%）でヘテロフィル増加（炎症/壊死）を確認。血液生化学でAST・LDH上昇・UA変動を測定。鳥類の腸重積は腸管蠕動異常・寄生虫感染・腸壁腫瘤が誘因であり、虚血性腸壊死が急速に進行するため緊急外科的整復が必要"
}

# 208. bird_air_sac_cyst — Air Sac Cyst / 気嚢嚢胞
ENRICHMENTS["bird_air_sac_cyst"] = {
    "diagnosis_ja": "体表の膨隆（皮下気腫様だが持続性・再発性）・呼吸困難の臨床評価。X線で気嚢壁の嚢胞性拡張・限局的ガス貯留を検出。CT検査で嚢胞の正確な位置・気嚢との連絡を確認。経皮的穿刺で嚢胞内ガスを吸引・一時的軽減。CBC（採血量≤体重の1%）で二次感染を評価。血液生化学で全身状態を確認。鳥類の気嚢嚢胞は先天性の気嚢壁異常または外傷後の弁機構形成で発生し、ガスが一方向的に嚢胞内に蓄積する。根治には外科的嚢胞壁切除・マーサピアライゼーションが必要"
}

# 209. bird_preen_gland_carcinoma — Preen Gland Carcinoma / 尾脂腺癌
ENRICHMENTS["bird_preen_gland_carcinoma"] = {
    "diagnosis_ja": "尾部背側の尾脂腺の急速増大する腫瘤・潰瘍化・出血を身体検査で確認。FNA細胞診で異型腺上皮細胞を確認。外科切除検体の病理組織検査で腺癌を確定し、浸潤度・核分裂指数・切除マージンを評価。X線・CT検査で転移（肺・肝臓・リンパ節）を検索。CBC・血液生化学（採血量≤体重の1%）で全身状態を評価。鳥類の尾脂腺癌は局所浸潤性で再発率が高い悪性腫瘍であり、広範囲切除が推奨される。腺腫との鑑別は病理組織検査でのみ可能"
}

# 210. bird_cloacal_stricture — Cloacal Stricture / 総排泄腔狭窄
ENRICHMENTS["bird_cloacal_stricture"] = {
    "diagnosis_ja": "排便困難（テネスムス）・排尿障害・便の細径化・腹部膨満の臨床評価。総排泄腔の視診・触診で狭窄の位置・程度を確認。造影X線・CT検査で狭窄の範囲を描出。内視鏡で総排泄腔内腔の狭窄・瘢痕・腫瘤を直視確認。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でUA上昇（尿酸塩排泄障害）を測定。鳥類の総排泄腔狭窄は慢性炎症（クラミジア・乳頭腫等）・外傷後瘢痕・腫瘍が原因で発生し、外科的拡張術やステント留置が治療選択肢となる"
}

# 211. bird_articular_gout_–_chronic_progressive — Articular Gout – Chronic Progressive
ENRICHMENTS["bird_articular_gout_–_chronic_progressive"] = {
    "diagnosis_ja": "関節腫脹・運動障害・跛行・趾関節周囲の白色結節（tophi: 尿酸塩結晶沈着）の臨床評価。関節液の偏光顕微鏡検査で針状の尿酸ナトリウム結晶（負の複屈折）を確認。X線で関節周囲の軟部組織腫脹・骨びらんを評価。血液生化学（採血量≤体重の1%）でUA著増を確認。腎機能評価（UA上昇は腎排泄障害を示唆）。CBC で慢性炎症変化を確認。鳥類の関節痛風は腎不全に伴う高尿酸血症の結果であり、高蛋白食・脱水・腎毒性薬物が誘因。アロプリノール投与と食餌改善が治療の基本"
}

# 212. bird_visceral_gout_–_acute_form — Visceral Gout – Acute Form / 内臓痛風急性型
ENRICHMENTS["bird_visceral_gout_–_acute_form"] = {
    "diagnosis_ja": "急性沈鬱・食欲廃絶・膨羽・多飲多尿・急性死の臨床評価。血液生化学（採血量≤体重の1%）でUA著増（>15 mg/dL）・K上昇・Ca/P異常を確認。腹部超音波で腎腫大・高エコー腎実質を検出。X線で内臓表面の石灰化沈着を評価。剖検で心臓・肝臓・腎臓・気嚢表面の白色チョーク様尿酸塩沈着（内臓痛風の特徴的所見）を確認。CBC で脱水・ヘテロフィル変動を確認。鳥類の急性内臓痛風は急性腎不全→高尿酸血症→尿酸塩の漿膜面析出が病態で、予後は極めて不良"
}

# 213. bird_atherosclerosis_–_aortic — Atherosclerosis – Aortic / 動脈硬化症大動脈型
ENRICHMENTS["bird_atherosclerosis_–_aortic"] = {
    "diagnosis_ja": "高齢鳥の運動不耐性・呼吸困難・突然死の臨床評価。心エコー検査で大動脈壁の肥厚・石灰化・内腔狭窄を評価。胸部X線で大動脈の石灰化・心拡大を検出。心電図で不整脈を記録。血液生化学（採血量≤体重の1%）でコレステロール・トリグリセリド上昇（高脂血症）を測定。CBC で全身状態を確認。食餌歴の聴取（高脂肪種子食偏重）。鳥類の大動脈アテローム硬化はアマゾン・ヨウム等の高齢大型オウムで高頻度であり、高脂肪食・運動不足・甲状腺機能低下が危険因子。突然死の主要原因の一つ"
}

# 214. bird_pulmonary_mycosis — Pulmonary Mycosis / 肺真菌症
ENRICHMENTS["bird_pulmonary_mycosis"] = {
    "diagnosis_ja": "慢性の呼吸困難・運動不耐性・開口呼吸・テイルボビングの臨床評価。胸部X線で肺野結節影・びまん性浸潤影・気嚢混濁を検出。CT検査で真菌腫の範囲を精密描出。気管洗浄液の培養でAspergillus・Candida等の病原真菌を分離。細胞診で菌糸・分生子を確認。ガラクトマンナン抗原検査で補助診断。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多を確認。鳥類ではAspergillus fumigatusによる肺・気嚢感染が最も多い真菌性呼吸器疾患であり、免疫低下が主要素因"
}

# 215. bird_tracheal_papilloma — Tracheal Papilloma / 気管乳頭腫
ENRICHMENTS["bird_tracheal_papilloma"] = {
    "diagnosis_ja": "声の変化（嗄声）・吸気性呼吸困難・呼吸時の異常音の臨床評価。気管内視鏡で気管内腔の乳頭状腫瘤を直視確認・生検。病理組織検査で乳頭腫の組織パターン（線維血管芯を覆う重層扁平上皮の増殖）を確認。PCR検査でヘルペスウイルスDNAを検索。胸部X線・CTで気管内腫瘤の位置・サイズを評価。CBC（採血量≤体重の1%）で全身状態を確認。鳥類の気管乳頭腫はアマゾン・マコーで報告があり、内部乳頭腫症の一部として発現する。気道閉塞が進行すると呼吸不全に至る"
}

# 216. bird_air_sac_herniation — Air Sac Herniation / 気嚢ヘルニア
ENRICHMENTS["bird_air_sac_herniation"] = {
    "diagnosis_ja": "体壁欠損部からの気嚢の膨隆（皮下の軟性膨隆・呼吸同期性の大きさ変動）を身体検査で確認。X線で体壁欠損を通じた気嚢の腹側・側方への膨出を検出。CT検査でヘルニア門のサイズ・気嚢壁の状態を評価。CBC（採血量≤体重の1%）で二次感染を確認。血液生化学で全身状態を評価。鳥類の気嚢ヘルニアは外傷後の体壁筋層断裂が原因で発生し、呼吸同期性に大きさが変動する点が皮下気腫との鑑別点。外科的体壁修復が根治的治療"
}

# 217. bird_ingluvoliths_crop_concretions — Ingluvoliths (Crop Concretions) / 嗉嚢結石
ENRICHMENTS["bird_ingluvoliths_crop_concretions"] = {
    "diagnosis_ja": "嗉嚢部の触診で硬い結石様腫瘤を確認。嗉嚢膨満・食欲低下・嘔吐の臨床評価。頸部X線で嗉嚢内の高密度結石影を検出。造影X線で嗉嚢の通過障害を確認。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でTP・グルコース変動を測定。嗉嚢洗浄液の培養でカンジダ等の感染を検索。鳥類の嗉嚢結石は脱水・慢性嗉嚢炎・異物摂取・嗉嚢運動障害が原因で嗉嚢内容物が固化して形成される。内視鏡的摘出が可能であるが、大型結石は嗉嚢切開が必要"
}

# 218. bird_avian_polyomavirus_–_chronic_carrier — Avian Polyomavirus – Chronic Carrier
ENRICHMENTS["bird_avian_polyomavirus_–_chronic_carrier"] = {
    "diagnosis_ja": "無症状だが間欠的にウイルスを排出する成鳥の評価。排泄腔スワブ・血液のPCR検査でAvian Polyomavirus（APV）DNAを検出（間欠的排出のため複数回検査を推奨）。血清学検査（HI・ELISA）で抗体価を測定。CBC（採血量≤体重の1%）で軽度リンパ球変動を評価。血液生化学で肝機能を確認。鳥類のAPV慢性キャリアは臨床的に健康であるが、同居幼鳥への感染源として重要。繁殖群では新規導入鳥のPCRスクリーニングと検疫隔離（30日以上）が感染管理の基本"
}

# 219. bird_egg_retention_pre-laying — Egg Retention (Pre-laying) / 卵停滞（産卵前）
ENRICHMENTS["bird_egg_retention_pre-laying"] = {
    "diagnosis_ja": "産卵予定鳥の腹部膨満・沈鬱・食欲低下・排便困難の臨床評価。腹部触診で停滞卵を触知。X線で卵管内の卵（石灰化卵殻の有無・位置・数）を確認。血液生化学（採血量≤体重の1%）でCa低下（<8 mg/dL）を確認（低Ca血症は子宮筋収縮障害の主因）。CBC で全身状態を評価。超音波で卵管の状態を確認。鳥類の産卵前卵停滞は低Ca血症・卵管筋力低下・卵過大・卵管感染が原因で発生し、Ca補充・温浴・PGE2等の保存的治療で多くは排出される"
}

# 220. bird_uropygial_gland_impaction — Uropygial Gland Impaction / 尾脂腺閉塞
ENRICHMENTS["bird_uropygial_gland_impaction"] = {
    "diagnosis_ja": "尾脂腺（uropygial gland）の腫脹・硬結（非疼痛性・非炎症性）を身体検査で確認。導管開口部の閉塞を視診で確認。圧迫で分泌物（蝋様・粘稠）の排出を試みる。FNA細胞診で腺分泌物・炎症細胞の有無を評価。CBC（採血量≤体重の1%）で二次感染を確認。膿瘍・腫瘍との鑑別。鳥類の尾脂腺閉塞は導管の角化栓・感染による導管狭窄が原因で、温罨法・導管マッサージで分泌物排出を促す。慢性閉塞では外科的導管拡張・腺摘出を検討する"
}

# 221. bird_nutritional_hyperparathyroidism — Nutritional Hyperparathyroidism / 栄養性上皮小体機能亢進症
ENRICHMENTS["bird_nutritional_hyperparathyroidism"] = {
    "diagnosis_ja": "骨軟化・病的骨折・嘴変形・脚の弯曲変形を身体検査で確認。X線で骨密度低下・皮質菲薄化・病的骨折を評価。血液生化学（採血量≤体重の1%）でCa低値〜正常・P上昇・ALP上昇を確認。PTH測定（上昇）。食餌歴の聴取（Ca/P比不適切・VitD3不足・UVBライト不使用）。CBC で全身状態を評価。鳥類の栄養性上皮小体機能亢進症は種子食偏重飼育鳥で極めて多く、Ca:P比の適正化（2:1以上）とVitD3補充（UVBライトまたは経口）が治療・予防の基本"
}

# 222. bird_avian_coronavirus_infection — Avian Coronavirus Infection / 鳥コロナウイルス感染症
ENRICHMENTS["bird_avian_coronavirus_infection"] = {
    "diagnosis_ja": "呼吸器症状（くしゃみ・鼻汁・気管ラ音）・消化器症状（下痢）・腎障害・産卵低下の臨床評価。RT-PCR検査で鳥コロナウイルスRNAを検出し株同定。血清学検査（ELISA・VN試験）でペア血清の抗体上昇を確認。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でAST・UA変動を測定。胸部X線で気管・気嚢の変化を検出。鳥類のコロナウイルスはIBV（鶏伝染性気管支炎ウイルス）が代表であり、呼吸器型・腎型・生殖器型の各臨床型を示す"
}

# 223. bird_avian_rotavirus_infection — Avian Rotavirus Infection / 鳥ロタウイルス感染症
ENRICHMENTS["bird_avian_rotavirus_infection"] = {
    "diagnosis_ja": "幼鳥の急性水様性下痢・脱水・成長遅延の臨床評価。糞便のELISA検査（ロタウイルス抗原検出キット）でロタウイルス抗原を検出。電子顕微鏡で特徴的な車輪状（rota）ウイルス粒子を確認。RT-PCR検査でロタウイルスRNAを検出し型別。CBC（採血量≤体重の1%）で脱水・ヘテロフィル変動を確認。血液生化学でTP低下・電解質異常を測定。鳥類のロタウイルス感染は七面鳥・鶏のヒナで急性腸炎を引き起こし、経口-糞便経路で迅速に群内伝播する"
}

# 224. bird_splenic_disease_splenitis — Splenic Disease (Splenitis) / 脾臓疾患（脾炎）
ENRICHMENTS["bird_splenic_disease_splenitis"] = {
    "diagnosis_ja": "非特異的な沈鬱・食欲低下・体重減少の臨床評価。腹部超音波で脾腫（正常サイズの2倍以上）・脾実質エコー異常を検出。X線で腹腔内軟部組織陰影の拡大を確認。CBC（採血量≤体重の1%）で白血球数変動・異型細胞を評価。血液生化学でAST・LDH変動を測定。FNA細胞診で脾臓の細胞構成を評価。感染性原因（クラミジア・マイコバクテリウム・ウイルス等）のPCR検索。鳥類の脾炎は多くの全身感染症で認められる所見であり、原因同定が治療方針決定に不可欠"
}

# 225. bird_zinc-responsive_dermatosis — Zinc-Responsive Dermatosis / 亜鉛反応性皮膚症
ENRICHMENTS["bird_zinc-responsive_dermatosis"] = {
    "diagnosis_ja": "皮膚の乾燥・鱗屑・痂皮形成・羽毛異常（脆弱化・光沢消失）の臨床評価。血清亜鉛濃度の測定（低値を確認）。食餌歴の聴取（種子食偏重・Ca過剰摂取による亜鉛吸収阻害）。皮膚生検で角化異常・表皮過角化のパターンを確認。CBC（採血量≤体重の1%）で全身状態を評価。亜鉛中毒との鑑別（高亜鉛血症は別病態）。鳥類の亜鉛反応性皮膚症は亜鉛欠乏に起因する皮膚疾患であり、亜鉛補充（経口）への臨床反応で診断を確認する"
}

# 226. bird_amyloidosis_–_hepatic — Amyloidosis – Hepatic / アミロイドーシス肝型
ENRICHMENTS["bird_amyloidosis_–_hepatic"] = {
    "diagnosis_ja": "肝腫大・腹水・慢性消耗の臨床評価。血液生化学（採血量≤体重の1%）で肝酵素上昇（AST・LDH）・アルブミン低下・胆汁酸上昇を確認。腹部超音波で肝腫大・びまん性高エコー肝実質を検出。肝FNA/生検のコンゴーレッド染色で偏光顕微鏡下にapple-green複屈折のアミロイド沈着を確認。CBC で慢性変化を評価。鳥類の肝アミロイドーシスはアヒル・ガチョウに好発するAA型アミロイドーシスであり、慢性炎症（bumblefoot・気嚢炎等）が先行する。進行性で根治困難"
}

# 227. bird_amyloidosis_–_renal — Amyloidosis – Renal / アミロイドーシス腎型
ENRICHMENTS["bird_amyloidosis_–_renal"] = {
    "diagnosis_ja": "多飲多尿・体重減少・慢性消耗の臨床評価。血液生化学（採血量≤体重の1%）でUA著増・電解質異常（K上昇・Na低下）・アルブミン低下を確認。腹部超音波で腎腫大・腎実質エコー異常を検出。腎FNA/生検のコンゴーレッド染色でアミロイド沈着を確認。CBC で慢性変化を評価。尿酸塩排泄評価。鳥類の腎アミロイドーシスは慢性腎不全→高尿酸血症→痛風の連鎖を引き起こし、AA型アミロイドーシスとして慢性感染症に続発する"
}

# 228. bird_myopathy_nutritional___capture — Myopathy (Nutritional / Capture)
ENRICHMENTS["bird_myopathy_nutritional___capture"] = {
    "diagnosis_ja": "筋力低下・飛翔不能・歩行困難・急性後肢麻痺の臨床評価。捕獲歴（長時間保定・過度の運動・ストレス）を聴取。血液生化学（採血量≤体重の1%）でCK著増（>10,000 U/L）・AST著増・LDH上昇（横紋筋融解の指標）・UA上昇（腎障害）を確認。CBC で脱水を評価。食餌歴の聴取（VitE/Se欠乏：栄養性ミオパチーの原因）。鳥類の捕獲性ミオパチーは野鳥・猛禽の捕獲・保定時に急性横紋筋融解を引き起こし、ミオグロビン尿による腎不全が致死的となる"
}

# 229. bird_cloacal_calculus_cloacolith — Cloacal Calculus (Cloacolith) / 総排泄腔結石
ENRICHMENTS["bird_cloacal_calculus_cloacolith"] = {
    "diagnosis_ja": "排便困難（テネスムス）・腹部膨満・総排泄腔周囲の腫脹の臨床評価。総排泄腔の視診・触診で硬い結石を触知。X線で総排泄腔内の高密度結石影を確認。血液生化学（採血量≤体重の1%）でUA著増（高尿酸血症→尿酸塩結石）を確認。CBC でヘテロフィル変動を評価。腎機能評価。超音波で結石のサイズを測定。鳥類の総排泄腔結石は高尿酸血症（脱水・腎疾患・高蛋白食）に伴う尿酸塩の析出が原因で形成され、結石除去と原因治療（腎疾患管理・食餌改善）が必要"
}

# 230. bird_hormonal_behavior — Chronic Egg Laying / Hormonal Behavior
ENRICHMENTS["bird_hormonal_behavior"] = {
    "diagnosis_ja": "過剰産卵（正常な繁殖期以外の連続的産卵）・巣作り行動・攻撃性増加・ペアボンディング行動の臨床評価。触診で卵管内の卵を触知。X線で卵の有無・多骨性骨過形成症（medullary bone）の有無を確認。血液生化学（採血量≤体重の1%）でCa・TP・エストロゲン変動を測定。CBC で全身状態を評価。飼育環境の聴取（日照時間・巣箱・鏡等のホルモン刺激因子）。鳥類の慢性産卵はCa枯渇→低Ca血症→卵詰まり→骨粗鬆症の連鎖を引き起こし、環境管理（日照制限・巣箱撤去）が治療の基本"
}

# 231. bird_fracture_wing — Wing Fracture (Bird) / 翼骨折（鳥）
ENRICHMENTS["bird_fracture_wing"] = {
    "diagnosis_ja": "翼の下垂・飛翔不能・腫脹・クレピタス（骨折端の軋音）を身体検査で確認。X線（最低2方向撮影）で骨折の部位（上腕骨・尺骨・橈骨）・型（横骨折・斜骨折・螺旋骨折・粉砕骨折）・偏位を評価。CT検査で複雑骨折の詳細描出。CBC（採血量≤体重の1%）で出血性貧血を評価。血液生化学でCa・P・ALP（代謝性骨疾患の除外）を測定。鳥類の翼骨折はIMピニング・ESF（創外固定）・FMP（副木固定）で治療し、骨折部位に応じて飛翔能力の予後を判定する"
}

# 232. bird_fracture_leg — Leg Fracture (Bird) / 脚骨折（鳥）
ENRICHMENTS["bird_fracture_leg"] = {
    "diagnosis_ja": "脚の挙上・非荷重・腫脹・クレピタスを身体検査で確認。X線（最低2方向撮影）で骨折の部位（大腿骨・脛足根骨・足根中足骨）・型・偏位を評価。CT検査で関節内骨折を詳細描出。CBC（採血量≤体重の1%）で出血性貧血を評価。血液生化学でCa・P・ALP測定（代謝性骨疾患の素因を検索）。鳥類の脚骨折はIMピニング・ESF・テープスプリントで整復固定し、小型鳥では外副木固定が多用される。竜骨上の安静位確保と対側脚への負荷分散管理が回復に重要"
}

# 233. bird_arthritis — Arthritis (Bird) / 関節炎（鳥）
ENRICHMENTS["bird_arthritis"] = {
    "diagnosis_ja": "関節腫脹・疼痛・跛行・運動制限を身体検査で確認。関節液穿刺の分析（細胞数・蛋白濃度・培養・結晶検査）で感染性・痛風性・免疫介在性を鑑別。X線で関節裂隙の狭小化・骨びらん・軟部組織腫脹を評価。CBC（採血量≤体重の1%）でヘテロフィル増加（感染性）を確認。血液生化学でUA上昇（関節痛風）を測定。関節液培養でStaphylococcus等の起炎菌を同定。鳥類の関節炎は感染性（バンブルフット関連）・関節痛風・外傷後変形性の3型が主要であり、原因に応じた治療が必要"
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
