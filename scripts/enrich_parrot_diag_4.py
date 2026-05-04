#!/usr/bin/env python3
"""Enrich diagnosis_ja for Parrot entries (batch 4: 50 entries)."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 1. parrot_0151 — Respiratory Fungal Infection / 呼吸器真菌感染（オウム）
ENRICHMENTS["parrot_0151"] = {
    "diagnosis_ja": "呼吸困難・開口呼吸・鼻汁から呼吸器真菌感染を疑う。X線・CTで気嚢壁肥厚・結節性病変・気管狭窄を評価。気管洗浄液の細胞診で真菌菌糸・胞子を確認し、培養でAspergillus属等を同定。CBC/生化学でヘテロフィル増多・低アルブミン血症。β-D-グルカン・ガラクトマンナン抗原で補助的に診断。気管内視鏡で気嚢内のプラーク・肉芽腫を直視下確認。大型オウム（ヨウム・コンゴウインコ）はストレス・免疫抑制で好発し、気嚢系の構造上、真菌感染が拡大しやすい。"
}

# 2. parrot_0152 — Respiratory Parasitic Disease / 呼吸器寄生虫疾患（オウム）
ENRICHMENTS["parrot_0152"] = {
    "diagnosis_ja": "開口呼吸・喘鳴・呼吸困難から呼吸器寄生虫を疑う。気管洗浄液の細胞診で寄生虫卵・幼虫を検出。糞便浮遊法でSyngamus（気管虫）卵を確認。X線で気管内腫瘤影や気嚢壁肥厚を評価。気管内視鏡で気管内の虫体を直接観察し確定。CBC/生化学で好酸球増多を確認。大型オウム類では屋外飼育・野鳥との接触歴が重要な疫学的リスク因子。鑑別にアスペルギルス症・細菌性気管炎・気管異物を考慮する。"
}

# 3. parrot_0153 — Respiratory Neoplasia / 呼吸器腫瘍（オウム）
ENRICHMENTS["parrot_0153"] = {
    "diagnosis_ja": "慢性呼吸困難・開口呼吸・削痩から呼吸器腫瘍を疑う。X線で肺野の腫瘤影・気嚢壁肥厚・胸郭内占拠性病変を評価。CT検査で腫瘤の範囲・浸潤度を精査。FNA細胞診または内視鏡下生検で組織型を確定。CBC/生化学で貧血・低蛋白血症を確認。気管洗浄液細胞診で悪性細胞の有無を評価。大型オウム類は長寿命（20-80年）のため加齢性腫瘍の発生頻度が高く、リンパ腫・腺癌の鑑別が重要。"
}

# 4. parrot_0154 — Respiratory Inflammatory Disease / 呼吸器炎症性疾患（オウム）
ENRICHMENTS["parrot_0154"] = {
    "diagnosis_ja": "くしゃみ・鼻汁・呼吸努力増大から呼吸器炎症性疾患を疑う。X線で肺野陰影増強・気嚢壁肥厚を評価。気管洗浄液の細胞診で炎症性細胞浸潤のパターン（ヘテロフィル性・リンパ形質細胞性）を確認。培養・感受性試験で感染性原因を除外。CBC/生化学でヘテロフィル増多・フィブリノーゲン上昇。環境因子（粉塵・エアロゾル・タバコ煙）の曝露歴を聴取。大型オウム類の気嚢系は複雑で炎症が波及しやすい。"
}

# 5. parrot_0155 — Lower Respiratory Tract Infection / 下部気道感染（オウム）
ENRICHMENTS["parrot_0155"] = {
    "diagnosis_ja": "開口呼吸・尾振り呼吸・チアノーゼから下部気道感染を疑う。X線で肺野のびまん性陰影・気嚢壁肥厚を評価。気管洗浄液の培養・感受性試験で原因菌を同定。細胞診でヘテロフィル浸潤・細菌・真菌菌糸を確認。CBC/生化学でヘテロフィル増多・AST上昇を確認。PCRでChlamydia psittaci・ABV等を除外。大型オウム類は気嚢システムにより感染が広範囲に波及しやすく、Aspergillus混合感染に注意。"
}

# 6. parrot_0156 — Chronic Respiratory Disease / 慢性呼吸器疾患（オウム）
ENRICHMENTS["parrot_0156"] = {
    "diagnosis_ja": "長期にわたる呼吸努力増大・くしゃみ・鼻汁・運動不耐性から慢性呼吸器疾患を疑う。X線・CTで気嚢壁肥厚・気管狭窄・肺野異常を評価。気管洗浄液の培養・細胞診で慢性炎症パターンと病原体を確認。PCRでChlamydia psittaci・Aspergillus・ABVを系統的に除外。CBC/生化学でヘテロフィル増多・慢性炎症マーカーを評価。環境要因（粉塵・低換気）の聴取が不可欠。大型オウムでは慢性アスペルギルス症が多い。"
}

# 7. parrot_0157 — Dermatological Bacterial Infection / 皮膚細菌感染（オウム）
ENRICHMENTS["parrot_0157"] = {
    "diagnosis_ja": "皮膚の発赤・腫脹・痂皮形成・排膿から皮膚細菌感染を疑う。患部の培養・感受性試験でグラム陰性菌（Pseudomonas・Klebsiella等）またはグラム陽性菌を同定。細胞診でヘテロフィル浸潤と細菌貪食像を確認。CBC/生化学でヘテロフィル増多・炎症マーカー上昇。羽毛損傷部・自咬部位の二次感染が多く、PBFD・PDD等の免疫抑制性疾患の基礎疾患検索が重要。グラム染色で迅速に菌形態を把握する。"
}

# 8. parrot_0158 — Dermatological Viral Infection / 皮膚ウイルス感染（オウム）
ENRICHMENTS["parrot_0158"] = {
    "diagnosis_ja": "皮膚・羽毛の異常病変（結節・痘疹・羽毛変形）から皮膚ウイルス感染を疑う。PCRで鳥痘ウイルス・サーコウイルス（PBFD）・ポリオーマウイルスを検出。皮膚生検で特徴的な封入体（鳥痘のBollinger小体、PBFDの好塩基性核内封入体）を確認。CBC/生化学でリンパ球減少・免疫抑制を評価。大型オウム類ではPBFDが慢性経過をとり羽毛の進行性脱落を呈する。鑑別に羽毛損壊行動・栄養欠乏を考慮。"
}

# 9. parrot_0159 — Dermatological Fungal Infection / 皮膚真菌感染（オウム）
ENRICHMENTS["parrot_0159"] = {
    "diagnosis_ja": "皮膚・嘴・脚部の鱗状病変・痂皮・脱羽から皮膚真菌感染を疑う。患部の掻破検体のKOH直接鏡検で真菌菌糸・胞子を確認。真菌培養（DTM・サブロー培地）で病原体を同定。ウッド灯検査は一部のMicrosporum属で蛍光を示す。皮膚生検でPAS染色により組織内真菌を確認。CBC/生化学で免疫抑制の有無を評価。大型オウム類では高湿度環境・免疫低下（PBFD等）が素因。鑑別に疥癬・細菌性皮膚炎を考慮。"
}

# 10. parrot_0160 — Dermatological Parasitic Infestation / 皮膚寄生虫寄生（オウム）
ENRICHMENTS["parrot_0160"] = {
    "diagnosis_ja": "皮膚の掻痒・脱羽・痂皮・過角化から外部寄生虫寄生を疑う。皮膚掻破検体の直接鏡検でKnemidocoptes（疥癬）・Dermanyssus・Ornithonyssus等を確認。嘴・脚部のハニカム状過角化はKnemidocoptes pilaの特徴的所見。CBC/生化学で好酸球増多を確認。羽毛検査で羽軸ダニ・羽毛ジラミを同定。大型オウム類では長寿命のため慢性寄生が進行しやすい。環境検査（ケージ・止まり木）でワクモ等の確認も必要。"
}

# 11. parrot_avian_poxvirus — Avian Poxvirus / 鳥痘
ENRICHMENTS["parrot_avian_poxvirus"] = {
    "diagnosis_ja": "皮膚型（嘴基部・眼周囲・脚部の結節性痘疹）または粘膜型（口腔・咽頭のジフテリア様偽膜）の臨床所見から疑診。皮膚生検でBollinger小体（好酸性細胞質内封入体）を確認し確定。PCRでAvipoxvirus DNAを検出。電子顕微鏡でポックスウイルス粒子を確認可能。CBC/生化学で白血球増多。大型オウム類では蚊媒介による感染が多く、飼育環境の蚊防除歴を聴取。粘膜型は呼吸困難を呈し重症化しやすい。"
}

# 12. parrot_bacterial_pneumonia — Bacterial Pneumonia / 細菌性肺炎
ENRICHMENTS["parrot_bacterial_pneumonia"] = {
    "diagnosis_ja": "開口呼吸・尾振り呼吸・鼻汁・沈鬱から細菌性肺炎を疑う。X線で肺野のびまん性陰影増強を評価。気管洗浄液の培養・感受性試験でグラム陰性菌（E. coli、Klebsiella、Pseudomonas等）を同定。細胞診でヘテロフィル浸潤と細菌貪食像を確認。CBC/生化学でヘテロフィル増多・フィブリノーゲン上昇。大型オウム類の気嚢系は細菌感染が広範囲に波及しやすく、気嚢炎合併の有無をCTで精査。Chlamydia psittaciのPCR除外が必須。"
}

# 13. parrot_gram-negative_bacterial_infection — Gram-negative Bacterial Infection / グラム陰性菌感染症
ENRICHMENTS["parrot_gram-negative_bacterial_infection"] = {
    "diagnosis_ja": "沈鬱・食欲不振・嘔吐・下痢等の非特異的症状からグラム陰性菌感染を疑う。クロアカ・そ嚢スワブのグラム染色で迅速にグラム陰性桿菌の優勢を確認。培養・感受性試験でE. coli・Klebsiella・Pseudomonas等を同定。CBC/生化学でヘテロフィル増多・AST上昇を評価。正常なオウム類の消化管フローラはグラム陽性菌優勢であり、グラム陰性菌の検出は病的意義が高い。血液培養で敗血症を除外。基礎疾患（PDD・PBFD）の検索も重要。"
}

# 14. parrot_cryptococcosis — Cryptococcosis / クリプトコッカス症
ENRICHMENTS["parrot_cryptococcosis"] = {
    "diagnosis_ja": "呼吸困難・鼻汁・副鼻腔腫脹・神経症状からクリプトコッカス症を疑う。鼻汁・病変部のインド墨汁染色で莢膜を有する酵母を確認。ラテックス凝集法で血清・体液中の莢膜抗原（CrAg）を検出。培養でCryptococcus neoformansを同定。組織生検でPAS・GMS染色陽性の酵母を確認。X線・CTで副鼻腔・肺野病変を評価。大型オウム類では鳩糞由来の環境曝露が主要感染経路。免疫抑制状態（PBFD等）で重症化リスクが高い。"
}

# 15. parrot_sarcocystosis — Sarcocystosis / サルコシスティス症
ENRICHMENTS["parrot_sarcocystosis"] = {
    "diagnosis_ja": "急性型では突然死・呼吸困難・沈鬱・黄色尿酸塩排泄からサルコシスティス症を疑う。確定診断は筋肉・臓器の病理組織検査でSarcocystis falcatula等のシストを確認。PCRで種特定が可能。CBC/生化学でヘテロフィル増多・AST・CK上昇・肝腎障害を評価。オポッサム由来のスポロシストがゴキブリ等中間宿主を介して感染するため、飼育環境での野生動物・昆虫アクセス歴を聴取。大型オウム（特に旧世界種）で致死率が高い。"
}

# 16. parrot_intestinal_parasites_roundworms_tapeworms — Intestinal Parasites / 腸内寄生虫症
ENRICHMENTS["parrot_intestinal_parasites_roundworms_tapeworms"] = {
    "diagnosis_ja": "体重減少・下痢・未消化便・削痩から腸内寄生虫を疑う。糞便検査（直接塗抹・浮遊法）でAscaridia（回虫）卵・Capillaria卵・条虫片節を検出。糞便PCRで虫種を特定。排泄された虫体の形態学的同定。CBC/生化学で好酸球増多・低蛋白血症を評価。腹部X線で腸管拡張・閉塞所見を確認。屋外飼育・他鳥との接触歴が重要なリスク因子。大型オウム類では慢性感染による栄養障害が削痩・免疫低下の原因となる。"
}

# 17. parrot_chocolate_toxicity — Chocolate Toxicity / チョコレート中毒
ENRICHMENTS["parrot_chocolate_toxicity"] = {
    "diagnosis_ja": "チョコレート摂取の確認された曝露歴と臨床症状（嘔吐・下痢・興奮・振戦・頻脈・けいれん）から診断。テオブロミン・カフェインの代謝が鳥類では遅く、少量でも致死的となりうる。CBC/生化学で肝酵素上昇・高血糖・電解質異常を評価。心電図で不整脈を確認。そ嚢内容物の確認・洗浄が有用。大型オウム類は好奇心旺盛で人間の食品への接触機会が多く、ダークチョコレート・ココアパウダーは特に危険。鑑別に他の食物中毒・重金属中毒を考慮。"
}

# 18. parrot_smoke_fume_inhalation_toxicosis — Smoke/Fume Inhalation Toxicosis / 煙・ガス吸入中毒
ENRICHMENTS["parrot_smoke_fume_inhalation_toxicosis"] = {
    "diagnosis_ja": "有毒ガス・煙への曝露歴（PTFE/テフロン加熱、自己洗浄オーブン、殺虫剤、塗料）と急性呼吸困難・突然死から診断。鳥類は気嚢システムにより哺乳類より毒素感受性が極めて高い。X線で肺野浮腫・気嚢壁肥厚を評価。CBC/生化学で肝酵素上昇・代謝性アシドーシスを確認。血液ガス分析で低酸素血症を評価。PTFE中毒は大型オウム類で致死率が極めて高く、曝露後数分〜数時間で死亡する。環境聴取が最重要の診断手段。"
}

# 19. parrot_plant_toxicity — Plant Toxicity / 植物中毒
ENRICHMENTS["parrot_plant_toxicity"] = {
    "diagnosis_ja": "有毒植物の摂取歴と臨床症状（嘔吐・下痢・流涎・神経症状・呼吸困難）から診断。そ嚢内容物の確認で植物片を同定。CBC/生化学で肝酵素上昇・腎機能障害・電解質異常を評価。X線でそ嚢・消化管内の植物異物を確認。大型オウム類は探索行動が活発で観葉植物への接触機会が多い。アボカド（persin含有）は鳥類で心筋壊死を引き起こし特に危険。その他ユリ科・ナス科植物にも注意。毒物種の同定が治療方針決定に不可欠。"
}

# 20. parrot_vitamin_d3_deficiency — Vitamin D3 Deficiency / ビタミンD3欠乏症
ENRICHMENTS["parrot_vitamin_d3_deficiency"] = {
    "diagnosis_ja": "骨軟化・病的骨折・嘴軟化・産卵障害からビタミンD3欠乏を疑う。血清Ca低値・P上昇（Ca:P比の異常）、ALP上昇を確認。PTH上昇で二次性上皮小体機能亢進症を評価。X線で骨密度低下・皮質菲薄化・病的骨折を確認。血中25(OH)D3濃度測定で確定。室内飼育のヨウム・コンゴウインコで好発し、UVB照射不足が主因。食餌内容（種子食偏重・ペレット未摂取）の聴取が重要。"
}

# 21. parrot_renal_disease — Renal Disease / 腎疾患
ENRICHMENTS["parrot_renal_disease"] = {
    "diagnosis_ja": "多飲多尿・脚麻痺（腎腫大による坐骨神経圧迫）・痛風結節から腎疾患を疑う。生化学でUA上昇・Ca/P異常・電解質異常を評価。X線で腎腫大・腎石灰化を確認。超音波で腎実質エコー変化・腫大を評価。尿検査で尿酸塩結晶の異常排泄を確認。組織生検で腎間質性腎炎・痛風結節（尿酸塩沈着）・腎腫瘍を鑑別。大型オウム類は長寿命のため慢性腎疾患が多く、ヨウムでは腎腫瘍が好発する。鑑別に痛風・脱水・重金属中毒を考慮。"
}

# 22. parrot_diabetes_mellitus — Diabetes Mellitus / 糖尿病
ENRICHMENTS["parrot_diabetes_mellitus"] = {
    "diagnosis_ja": "多飲多尿・体重減少・高血糖から糖尿病を疑う。空腹時血糖値の持続的高値（>400 mg/dL）を複数回確認。フルクトサミンで中期的血糖コントロールを評価。CBC/生化学で肝酵素上昇・高コレステロール血症を確認。尿検査で糖尿を確認。膵臓超音波で膵炎・膵腫瘍を除外。大型オウム類（特にオカメインコ）で報告があるが、鳥類の糖尿病は哺乳類と異なりグルカゴン依存性が高い。鑑別にストレス性高血糖・膵炎を考慮。"
}

# 23. parrot_pancreatitis — Pancreatitis / 膵炎
ENRICHMENTS["parrot_pancreatitis"] = {
    "diagnosis_ja": "急性嘔吐・下痢・沈鬱・腹部膨満から膵炎を疑う。血清アミラーゼ・リパーゼ上昇を確認するが、鳥類では感度が限られる。CBC/生化学でヘテロフィル増多・AST/ALT上昇・高血糖・高脂血症を評価。腹部超音波で膵臓の腫大・エコー輝度変化・腹腔液貯留を確認。X線で消化管イレウス所見を評価。確定診断は膵生検による壊死性膵炎の病理所見。大型オウム類では高脂肪食（種子食偏重）が誘因となりやすい。"
}

# 24. parrot_egg_yolk_peritonitis — Egg Yolk Peritonitis / 卵黄性腹膜炎
ENRICHMENTS["parrot_egg_yolk_peritonitis"] = {
    "diagnosis_ja": "雌鳥の腹部膨満・沈鬱・食欲不振・呼吸困難から卵黄性腹膜炎を疑う。X線・超音波で腹腔内液体貯留・卵管腫大を確認。腹腔穿刺で黄色〜クリーム色の卵黄含有液を採取し細胞診・培養を実施。CBC/生化学でヘテロフィル増多・高Ca血症・高蛋白血症・肝酵素上昇を評価。血清Ca/エストロゲン上昇は活動的卵巣を示唆。大型オウム類では慢性産卵（特に単独飼育の雌）が素因。E. coli等の二次感染で敗血症に進展しうる。"
}

# 25. parrot_foreign_body_ingestion — Foreign Body Ingestion / 異物摂取
ENRICHMENTS["parrot_foreign_body_ingestion"] = {
    "diagnosis_ja": "嘔吐・食欲不振・そ嚢膨満・沈鬱から異物摂取を疑う。X線で金属異物（鉛・亜鉛）・高密度異物を確認。造影X線でそ嚢・前胃・筋胃内の非金属異物を描出。そ嚢触診で異物を触知。内視鏡でそ嚢・前胃内の異物を直視下確認・摘出。CBC/生化学で血中鉛・亜鉛濃度を測定し重金属中毒を除外。大型オウム類は強力な嘴と好奇心旺盛な性質から金属片・繊維・プラスチック等の異物摂取が多い。"
}

# 26. parrot_gastric_ventricular_foreign_body — Gastric (Ventricular) Foreign Body / 胃（筋胃）内異物
ENRICHMENTS["parrot_gastric_ventricular_foreign_body"] = {
    "diagnosis_ja": "食欲不振・体重減少・嘔吐・未消化便から筋胃内異物を疑う。X線で筋胃内の金属異物・高密度物体を確認。造影X線でバリウム通過遅延・筋胃内充満欠損を描出。内視鏡でそ嚢経由で前胃・筋胃内の異物を直視下確認。血中鉛・亜鉛濃度を測定し重金属中毒の合併を評価。CBC/生化学で貧血・肝腎障害を確認。大型オウム類では金属製おもちゃ・ケージ部品の摂取が多く、亜鉛めっき製品が亜鉛中毒の主因となる。"
}

# 27. parrot_psittacine_stress_syndrome — Psittacine Stress Syndrome / オウム目ストレス症候群
ENRICHMENTS["parrot_psittacine_stress_syndrome"] = {
    "diagnosis_ja": "羽毛損壊行動・自咬・過度の鳴き声・常同行動からストレス症候群を疑う。身体検査で皮膚損傷・脱羽パターンを評価。CBC/生化学でストレス白血球像（H/L比上昇）・コルチコステロン上昇を確認。PBFD-PCR・内部寄生虫検査・甲状腺機能検査で器質的疾患を除外。環境評価（ケージサイズ・社会的隔離・刺激不足・睡眠不足）が診断の核心。大型オウム類は高い知能と社会的要求から環境性ストレスに脆弱。除外診断により確定する。"
}

# 28. parrot_contact_dermatitis — Contact Dermatitis / 接触性皮膚炎
ENRICHMENTS["parrot_contact_dermatitis"] = {
    "diagnosis_ja": "脚部・腹部・胸部の接触部位に限局した発赤・腫脹・落屑・痂皮から接触性皮膚炎を疑う。病歴聴取で新規導入物質（止まり木塗料・洗剤・消毒剤・金属）への曝露を確認。皮膚掻破検体で感染・寄生虫を除外。皮膚生検で表層性皮膚炎・好酸球浸潤を確認。CBC/生化学で全身性疾患を除外。原因物質の除去による症状改善で臨床的に確定。大型オウム類では亜鉛めっきケージ・特定の木材での接触反応に注意。"
}

# 29. parrot_beak_malocclusion — Beak Malocclusion / 嘴不正咬合
ENRICHMENTS["parrot_beak_malocclusion"] = {
    "diagnosis_ja": "上嘴・下嘴の咬合不全（上嘴過長・交差咬合・下嘴偏位）を視診で評価。X線で嘴骨基部の骨病変・骨折・腫瘍を確認。栄養歴の聴取（Ca/ビタミンD3欠乏）で代謝性骨疾患を除外。PBFD-PCRで嘴変形の原因となるサーコウイルス感染を除外。幼鳥では人工育雛時の給餌器具による外傷歴を確認。大型オウム類は嘴が持続的に成長するため不正咬合が進行しやすく、定期的な嘴整形が必要。鑑別に肝疾患・甲状腺機能低下症を考慮。"
}

# 30. parrot_wing_trauma___soft_tissue_injury — Wing Trauma / Soft Tissue Injury / 翼外傷・軟部組織損傷
ENRICHMENTS["parrot_wing_trauma___soft_tissue_injury"] = {
    "diagnosis_ja": "翼の下垂・腫脹・疼痛・運動制限から翼外傷を疑う。視診・触診で開放創・血腫・骨折の有無を評価。X線で骨折（上腕骨・橈骨・尺骨）を確認し、関節脱臼を除外。開放創の培養・感受性試験で二次感染を評価。CBC/生化学で失血性貧血・炎症を確認。大型オウム類はパニック飛行（ナイトフライト）による翼損傷が多く、クリッピング翼での着地失敗も原因となる。軟部組織損傷の範囲評価には超音波が有用。"
}

# 31. parrot_periorbital_abscess — Periorbital Abscess / 眼窩周囲膿瘍
ENRICHMENTS["parrot_periorbital_abscess"] = {
    "diagnosis_ja": "眼周囲の腫脹・発赤・眼球突出・結膜炎から眼窩周囲膿瘍を疑う。X線・CTで眼窩内の膿瘍腔・副鼻腔への波及を評価。FNA細胞診でヘテロフィル性炎症と乾酪様壊死物を確認。培養・感受性試験で原因菌を同定。CBC/生化学でヘテロフィル増多・炎症マーカー上昇を評価。眼科検査で角膜・眼球への影響を確認。大型オウム類では副鼻腔炎からの波及が多く、Chlamydia psittaciやAspergillus等の基礎感染を除外する。"
}

# 32. parrot_internal_tumors_neoplasia — Internal Tumors (Neoplasia) / 内部腫瘍
ENRICHMENTS["parrot_internal_tumors_neoplasia"] = {
    "diagnosis_ja": "腹部膨満・体重減少・沈鬱・多飲多尿から内部腫瘍を疑う。X線で腫瘤影・臓器腫大・体腔液貯留を確認。超音波で腫瘤の部位・大きさ・内部構造を評価。CT/MRIで浸潤範囲を精査。FNA細胞診または超音波ガイド下生検で組織型を確定。CBC/生化学で貧血・肝酵素上昇・高Ca血症を評価。大型オウム類は長寿命（20-80年）のため腫瘍発生率が高く、腎腫瘍（特にヨウム）・肝腫瘍・リンパ腫が多い。"
}

# 33. parrot_tracheal_obstruction — Tracheal Obstruction / 気管閉塞
ENRICHMENTS["parrot_tracheal_obstruction"] = {
    "diagnosis_ja": "急性呼吸困難・吸気性喘鳴・チアノーゼ・開口呼吸から気管閉塞を疑う。X線で気管内腫瘤・異物・狭窄部位を確認。気管内視鏡で閉塞原因（異物・肉芽腫・腫瘤・真菌プラーク）を直視下確認。CT検査で閉塞の範囲・気管壁浸潤を精査。CBC/生化学でヘテロフィル増多を確認。培養・感受性試験で感染性原因を同定。大型オウム類（特にアマゾン属）は気管の解剖学的特徴から閉塞を起こしやすい。緊急的な気道確保が必要な場合がある。"
}

# 34. parrot_aspiration_pneumonia — Aspiration Pneumonia / 誤嚥性肺炎
ENRICHMENTS["parrot_aspiration_pneumonia"] = {
    "diagnosis_ja": "強制給餌・手差し育雛後の急性呼吸困難・湿性ラ音・沈鬱から誤嚥性肺炎を疑う。X線で肺野のびまん性陰影増強（特に腹側肺）を確認。気管洗浄液の細胞診で食餌片・脂肪滴を含むマクロファージとヘテロフィル浸潤を確認。培養・感受性試験で二次感染菌を同定。CBC/生化学でヘテロフィル増多を評価。幼鳥の人工育雛時の給餌過誤が主因。大型オウム類では嘴の大きさに対してそ嚢チューブの不適切な挿入が原因となりやすい。"
}

# 35. parrot_hypothyroidism — Hypothyroidism / 甲状腺機能低下症
ENRICHMENTS["parrot_hypothyroidism"] = {
    "diagnosis_ja": "肥満・羽毛異常（脱羽・変色・成長不良）・沈鬱・寒がりから甲状腺機能低下症を疑う。血清T4低値で疑診するが、鳥類の基準値は種差が大きい。TSH刺激試験で確定（レスポンス不良）。CBC/生化学で高コレステロール血症・高トリグリセリド血症を確認。X線で甲状腺腫大を評価。超音波で甲状腺サイズ・エコーパターンを確認。ヨウ素欠乏食（種子食偏重）が主因であり食餌歴の聴取が重要。鑑別にPBFD・肝疾患・栄養欠乏を考慮。"
}

# 36. parrot_adrenal_disease — Adrenal Disease / 副腎疾患
ENRICHMENTS["parrot_adrenal_disease"] = {
    "diagnosis_ja": "多飲多尿・羽毛異常・沈鬱・筋萎縮から副腎疾患を疑う。基礎コルチコステロン値と刺激試験（ACTH刺激試験）で副腎機能を評価。CBC/生化学で電解質異常（Na/K比の変化）・高血糖・肝酵素異常を確認。超音波で副腎の大きさ・形態を評価。X線で副腎腫大・石灰化を確認。大型オウム類では慢性ストレスによる副腎皮質過形成が多く、過機能症と低機能症の鑑別が重要。鑑別に甲状腺疾患・腎疾患を考慮。"
}

# 37. parrot_avian_ganglioneuritis — Avian Ganglioneuritis / 鳥類神経節炎
ENRICHMENTS["parrot_avian_ganglioneuritis"] = {
    "diagnosis_ja": "消化管運動障害（そ嚢うっ滞・前胃拡張・嘔吐・未消化便）と神経症状（運動失調・けいれん）からPDD関連神経節炎を疑う。X線で前胃拡張を確認。ABV-PCR（クロアカ・そ嚢スワブ・血液）で病原体を検出。そ嚢生検で神経叢のリンパ形質細胞性浸潤を確認し確定。CBC/生化学でCK上昇・低蛋白血症を評価。CT/MRIで中枢神経系病変を精査。大型オウム類（コンゴウインコ・ヨウム）で好発し、ABV感染が主因とされる。"
}

# 38. parrot_epilepsy___idiopathic_seizures — Epilepsy / Idiopathic Seizures / てんかん・特発性けいれん
ENRICHMENTS["parrot_epilepsy___idiopathic_seizures"] = {
    "diagnosis_ja": "反復性けいれん発作（全身性強直間代性・焦点性）から鳥類てんかんを疑う。血中Ca・血糖・鉛・亜鉛濃度測定で代謝性・中毒性原因を除外。CBC/生化学で肝腎障害・感染を除外。X線で重金属異物を確認。CT/MRIで脳内占拠性病変・脳炎を除外。ABV-PCRでPDD関連脳炎を除外。特発性てんかんは除外診断で確定。大型オウム類では重金属中毒（鉛・亜鉛）と低Ca血症が発作の最も一般的な原因であり、これらの除外が最優先。"
}

# 39. parrot_chronic_rhinitis — Chronic Rhinitis / 慢性鼻炎
ENRICHMENTS["parrot_chronic_rhinitis"] = {
    "diagnosis_ja": "慢性くしゃみ・鼻汁（漿液性〜膿性）・鼻孔周囲の痂皮・副鼻腔腫脹から慢性鼻炎を疑う。後鼻孔検査で鼻甲介腫脹・膿性分泌物を確認。鼻腔スワブの培養・感受性試験で原因菌を同定。Chlamydia psittaci PCRで鳥クラミジア症を除外。CT検査で副鼻腔への波及・骨融解を評価。CBC/生化学でヘテロフィル増多を確認。大型オウム類ではビタミンA欠乏による扁平上皮化生が慢性鼻炎の素因。食餌歴（種子食偏重）の聴取が重要。"
}

# 40. parrot_choanal_atresia___choanal_slit_abnormality — Choanal Atresia / 後鼻孔閉鎖
ENRICHMENTS["parrot_choanal_atresia___choanal_slit_abnormality"] = {
    "diagnosis_ja": "呼吸困難・開口呼吸・鼻汁貯留から後鼻孔閉鎖・裂異常を疑う。口腔検査で後鼻孔（choanal slit）の形態異常・閉鎖・乳頭鈍化を確認。CT検査で後鼻孔の骨性閉鎖・軟部組織閉塞を精密に評価。内視鏡で鼻腔側からの後鼻孔開存性を確認。CBC/生化学で二次感染の有無を評価。先天性（幼鳥）と後天性（ビタミンA欠乏・慢性感染による瘢痕）を鑑別。大型オウム類ではビタミンA欠乏による扁平上皮化生が後鼻孔乳頭鈍化の主因。"
}

# 41. parrot_allergic_respiratory_disease — Allergic Respiratory Disease / アレルギー性呼吸器疾患
ENRICHMENTS["parrot_allergic_respiratory_disease"] = {
    "diagnosis_ja": "慢性くしゃみ・鼻汁・呼吸努力増大で感染性原因を除外した後にアレルギー性呼吸器疾患を疑う。気管洗浄液の細胞診で好酸球増多を確認。CBC/生化学でヘテロフィル増多がなく好酸球優位。環境抗原（羽毛粉・粉塵・カビ胞子・花粉）の曝露歴を詳細に聴取。X線で気嚢壁肥厚を確認。感染性原因（Chlamydia・Aspergillus・細菌）のPCR・培養で系統的除外。抗原除去による症状改善で臨床的に確定。除外診断が基本。"
}

# 42. parrot_gonadal_neoplasia — Gonadal Neoplasia / 生殖腺腫瘍
ENRICHMENTS["parrot_gonadal_neoplasia"] = {
    "diagnosis_ja": "腹部膨満・性行動変化・蝋膜色変化・片脚麻痺（坐骨神経圧迫）から生殖腺腫瘍を疑う。X線で腹腔内腫瘤影を確認。超音波で生殖腺の腫大・内部構造を評価。CBC/生化学で高Ca血症・性ホルモン異常を確認。FNA細胞診で腫瘍細胞を確認。CT検査で腫瘤の浸潤範囲・転移を精査。雄ではセルトリ細胞腫・精上皮腫、雌では卵巣癌が多い。大型オウム類では長寿命のため腫瘍発生頻度が高く、特にセキセイインコ・ヨウムで好発。"
}

# 43. parrot_splay_leg_spraddle_leg — Splay Leg (Spraddle Leg) / 開脚症
ENRICHMENTS["parrot_splay_leg_spraddle_leg"] = {
    "diagnosis_ja": "幼鳥の両脚外転・起立不能・脚の外側への開脚を視診で確認。X線で大腿骨頭の亜脱臼・股関節の形態異常・長骨変形を評価。栄養状態（Ca/ビタミンD3・タンパク質）の評価で代謝性骨疾患を除外。巣材の不適切さ（滑りやすい床材）が主要な発症因子。触診で股関節可動域と筋腱の緊張度を評価。早期発見・早期介入（テーピング・スプリント）が予後を大きく左右する。大型オウム類の幼鳥では体重増加が速く、不適切な巣材で発症しやすい。"
}

# 44. parrot_psittacine_proventricular_worm_spirurids — Psittacine Proventricular Worm / オウム目前胃寄生虫
ENRICHMENTS["parrot_psittacine_proventricular_worm_spirurids"] = {
    "diagnosis_ja": "体重減少・嘔吐・未消化便・削痩からオウム前胃旋尾線虫を疑う。糞便浮遊法でDispharynx・Spirurid等の厚殻卵を検出。内視鏡で前胃粘膜に穿入する虫体を直接確認。X線で前胃壁肥厚・前胃拡張を評価。CBC/生化学で好酸球増多・低蛋白血症を確認。前胃生検で虫体断面と肉芽腫性炎症を確認。中間宿主（昆虫）への曝露歴を聴取。鑑別にPDD・前胃拡張症・細菌性前胃炎を考慮する。"
}

# 45. parrot_feather_folliculitis — Feather Folliculitis / 羽毛毛包炎
ENRICHMENTS["parrot_feather_folliculitis"] = {
    "diagnosis_ja": "羽毛の脱落・変形・毛包周囲の発赤・腫脹・膿瘍形成から毛包炎を疑う。患部の細胞診でヘテロフィル浸潤と細菌を確認。培養・感受性試験で原因菌（Staphylococcus・Pseudomonas等）を同定。皮膚生検で毛包周囲の炎症浸潤パターンを評価。PBFD-PCRでサーコウイルス感染を除外。CBC/生化学で全身性炎症を確認。自咬・羽毛損壊による二次感染が多く、行動学的原因の評価も重要。大型オウム類では胸部・腹部の自咬部位に好発。"
}

# 46. parrot_hemorrhagic_syndrome___coagulopathy — Hemorrhagic Syndrome / 出血性症候群
ENRICHMENTS["parrot_hemorrhagic_syndrome___coagulopathy"] = {
    "diagnosis_ja": "自発性出血（皮下出血・血便・血尿・出血斑）から出血性症候群・凝固障害を疑う。凝固検査（PT・APTT・フィブリノーゲン・D-dimer）で凝固カスケード異常を評価。CBC/生化学で血小板減少（正確にはトロンボサイト減少）・貧血・肝酵素上昇を確認。血中鉛・亜鉛濃度で重金属中毒を除外。X線で金属異物を確認。肝機能検査（胆汁酸）で肝疾患による凝固因子産生低下を評価。ビタミンK欠乏・殺鼠剤中毒・DICを鑑別。"
}

# 47. parrot_polyfolliculosis — Polyfolliculosis / 多毛包症
ENRICHMENTS["parrot_polyfolliculosis"] = {
    "diagnosis_ja": "単一毛包から複数の羽毛が生えるクラスター状の羽毛異常を視診で確認。皮膚生検で毛包構造の異常（複数羽芽の形成）を病理組織学的に確認し確定。PBFD-PCRでサーコウイルス感染（毛包変性の原因）を除外。ポリオーマウイルスPCRも実施。CBC/生化学で基礎疾患を除外。先天性と後天性（ウイルス感染・外傷後）を鑑別。大型オウム類（特にヨウム・アマゾン）で散見され、慢性ウイルス感染が素因となることがある。"
}

# 48. parrot_paramyxovirus_infection_pmv — Paramyxovirus Infection (PMV) / パラミクソウイルス感染症
ENRICHMENTS["parrot_paramyxovirus_infection_pmv"] = {
    "diagnosis_ja": "神経症状（振戦・運動失調・斜頸・後弓反張）・下痢・呼吸困難からパラミクソウイルス感染を疑う。RT-PCRでAvian Paramyxovirus（APMV-1〜4等）を検出。赤血球凝集抑制試験（HI）で血清抗体価を測定。クロアカ・気管スワブからのウイルス分離。CBC/生化学で白血球減少・肝酵素上昇を確認。剖検で脳炎・膵壊死・腎炎所見を確認。大型オウム類では野鳥・鶏との接触歴を聴取。ニューカッスル病との型別鑑定が重要。"
}

# 49. parrot_circovirus_infection_non-pbfd_strains — Circovirus Infection (Non-PBFD Strains) / サーコウイルス感染症（非PBFD株）
ENRICHMENTS["parrot_circovirus_infection_non-pbfd_strains"] = {
    "diagnosis_ja": "免疫抑制症状（反復性感染・白血球減少・リンパ組織萎縮）からPBFD以外のサーコウイルス感染を疑う。PCRでBFDVと異なるサーコウイルス株を検出・シークエンス解析で型別。CBC/生化学でリンパ球減少・免疫グロブリン低値を確認。リンパ組織生検でリンパ球壊死・封入体を確認。PBFD-PCR陰性だが免疫抑制が持続する場合に本症を考慮。大型オウム類の幼鳥で重症化しやすく、二次感染（細菌・真菌）のリスク評価が重要。"
}

# 50. parrot_avian_herpesvirus_non-pacheco's — Avian Herpesvirus (Non-Pacheco's) / 鳥ヘルペスウイルス（非パチェコ型）
ENRICHMENTS["parrot_avian_herpesvirus_non-pacheco's"] = {
    "diagnosis_ja": "皮膚・粘膜の丘疹状病変（内部乳頭腫症）・消化管病変・肝炎から非パチェコ型ヘルペスウイルス感染を疑う。PCRでヘルペスウイルスDNAを検出しシークエンス解析でパチェコ病ウイルスとの型別。病理組織検査で好酸性核内封入体（Cowdry A型）を確認。CBC/生化学で肝酵素上昇・白血球減少を評価。内視鏡で消化管・クロアカ内の乳頭腫性病変を確認。大型オウム（特にアマゾン）では内部乳頭腫症として発現し、胆管癌への悪性転化リスクがある。"
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
