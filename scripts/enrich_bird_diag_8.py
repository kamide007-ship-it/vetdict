#!/usr/bin/env python3
"""Enrich Bird diagnosis_ja — batch 8 (entries 101-150 of 233 remaining)."""
import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 101. bird_infectious_bursal_disease_gumboro — Infectious Bursal Disease (Gumboro)
ENRICHMENTS["bird_infectious_bursal_disease_gumboro"] = {
    "diagnosis_ja": "幼鳥（3-6週齢）の沈鬱・白色水様性下痢・膨羽の臨床評価。IBDV特異的RT-PCR検査（ファブリキウス嚢組織）でウイルスを検出。血清学検査（ELISA・VN試験）で抗体価を測定。CBC（採血量≤体重の1%）でリンパ球著減（B細胞破壊による免疫抑制）を確認。剖検でファブリキウス嚢の腫大→萎縮・出血を確認。病理組織検査でリンパ濾胞壊死を評価。鳥類のIBDVはファブリキウス嚢のB細胞を標的とし、重度免疫抑制を惹起するため二次感染リスクが急増する"
}

# 102. bird_avian_spirochetosis — Avian Spirochetosis
ENRICHMENTS["bird_avian_spirochetosis"] = {
    "diagnosis_ja": "急性沈鬱・発熱・チアノーゼ・緑色下痢の臨床評価。末梢血塗抹のギムザ染色で血中のBorrelia anserina（スピロヘータ）を検出。暗視野顕微鏡で運動性スピロヘータを確認。CBC（採血量≤体重の1%）でヘテロフィル変動・PCV低下（貧血）を確認。血液生化学でAST・LDH上昇（肝脾障害）を測定。剖検で脾腫・肝腫大を確認。鳥類のスピロヘータ症はダニ（Argas属）が媒介し、家禽群で急性死として集団発生する。血液塗抹での直接検出が最も迅速な診断法"
}

# 103. bird_avian_haemoproteosis — Avian Haemoproteosis
ENRICHMENTS["bird_avian_haemoproteosis"] = {
    "diagnosis_ja": "末梢血塗抹のギムザ染色で有核赤血球内のHaemoproteus配偶子母体（ソーセージ状・核を半月状に偏位させる）を検出。Haemoproteus属特異的PCR検査で種同定。CBC（採血量≤体重の1%）でPCV低下（軽度貧血）・赤血球形態異常を評価。血液生化学でAST・LDH変動を測定。脾臓超音波で脾腫を検索。鳥類のHaemoproteusはCulicoides（ヌカカ）やHippoboscidae（シラミバエ）が媒介し、多くの場合は不顕性感染だが、免疫低下時に臨床的貧血を惹起する"
}

# 104. bird_leucocytozoonosis — Leucocytozoonosis
ENRICHMENTS["bird_leucocytozoonosis"] = {
    "diagnosis_ja": "急性沈鬱・貧血・呼吸困難・緑色便の臨床評価。末梢血塗抹のギムザ染色で白血球/赤血球内のLeucocytozoon配偶子母体（宿主細胞を変形させる大型の丸型ガメトサイト）を検出。Leucocytozoon属特異的PCR検査で種同定。CBC（採血量≤体重の1%）でPCV著低（重度再生性貧血）を確認。血液生化学でAST・LDH上昇（肝障害）を測定。鳥類のLeucocytozoonosisはブユ（Simulium属）が媒介し、家禽（特にアヒル・七面鳥）での急性大量死が特徴的"
}

# 105. bird_avian_cholera_fowl_cholera — Avian Cholera (Fowl Cholera)
ENRICHMENTS["bird_avian_cholera_fowl_cholera"] = {
    "diagnosis_ja": "急性死・沈鬱・チアノーゼ・粘液性鼻汁の臨床評価。病変部・血液・臓器の細菌培養でPasteurella multocidaを分離同定。CBC（採血量≤体重の1%）でヘテロフィル著増（急性型）を確認。血液生化学でAST・LDH上昇（肝障害）を測定。剖検で肝臓の多発性点状壊死巣（特徴的所見）・脾腫・心外膜出血を確認。PCR検査で病原型を判定。鳥類のFowl Choleraは急性敗血症型（致死率>80%）と慢性型（肉垂腫脹・関節炎）があり、水禽で特に重篤"
}

# 106. bird_erysipelas — Erysipelas
ENRICHMENTS["bird_erysipelas"] = {
    "diagnosis_ja": "急性死・沈鬱・皮膚チアノーゼの臨床評価。血液・臓器の細菌培養でErysipelothrix rhusiopathiaeを分離同定。感受性試験で抗菌薬選択（ペニシリン系が第一選択）。CBC（採血量≤体重の1%）でヘテロフィル著増を確認。血液生化学でAST・LDH上昇を測定。剖検で脾腫・肝腫大・漿膜出血を確認。病理組織検査で血管内菌塊・臓器壊死を評価。鳥類のErysipelasは七面鳥・アヒルに好発し、人獣共通感染症としても重要（類丹毒）"
}

# 107. bird_listeriosis — Listeriosis
ENRICHMENTS["bird_listeriosis"] = {
    "diagnosis_ja": "神経症状（斜頸・旋回運動・運動失調）・急性死の臨床評価。血液・臓器の細菌培養でListeria monocytogenesを分離同定（4℃cold enrichment法が有用）。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多を確認。血液生化学でAST・LDH上昇を測定。剖検で肝臓・脾臓・心筋の多発性壊死巣を確認。病理組織検査で脳幹の微小膿瘍・壊死巣を評価。鳥類のListeriosis は汚染サイレージ・土壌からの経口感染が主因で、人獣共通感染症として要注意"
}

# 108. bird_ornithobacterium_rhinotracheale_ort_infection — ORT Infection
ENRICHMENTS["bird_ornithobacterium_rhinotracheale_ort_infection"] = {
    "diagnosis_ja": "呼吸器症状（鼻汁・副鼻腔腫脹・呼吸困難・産卵低下）の臨床評価。気管・副鼻腔スワブの細菌培養でOrnithobacterium rhinotrachealeを分離（5% CO2・48時間・血液寒天）。PCR検査でORT特異的遺伝子を検出。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。胸部X線で気嚢混濁・肺野濃度上昇を評価。血清学検査（ELISA）で抗体価を測定。鳥類のORT感染は鶏・七面鳥で気嚢炎・肺炎を惹起し、E. coliとの混合感染で重篤化する"
}

# 109. bird_avian_gastric_yeast_macrorhabdus_ornithogaster_refractory — AGY Refractory
ENRICHMENTS["bird_avian_gastric_yeast_macrorhabdus_ornithogaster_refractory"] = {
    "diagnosis_ja": "治療抵抗性の慢性削痩・嘔吐・粒状未消化便の臨床評価。糞便のグラム染色・ギムザ染色で大型桿菌状酵母体（6-20μm）の持続的排出を確認。定量的糞便検査で菌量をモニタリング。CBC（採血量≤体重の1%）でH/L比上昇を確認。血液生化学でTP低下・AST上昇・グルコース低下を測定。腹部X線で前胃拡張・筋胃菲薄化の進行を評価。内視鏡で前胃粘膜の慢性変化を確認。鳥類のAGY難治例ではアムホテリシンBの長期投与（4-6週間）後も再発することがあり、免疫状態の評価が重要"
}

# 110. bird_mycotic_pneumonia — Mycotic Pneumonia
ENRICHMENTS["bird_mycotic_pneumonia"] = {
    "diagnosis_ja": "呼吸困難・開口呼吸・尾振り呼吸の臨床評価。胸部X線で肺野結節影・気嚢混濁・気管分岐部肥厚を確認。CT検査で真菌性肉芽腫の範囲を精密判定。CBC（採血量≤体重の1%）でヘテロフィル著増・単球増多を確認。気管洗浄液の細胞診でヘテロフィル浸潤・真菌菌糸を検索。Aspergillus属PCR・ガラクトマンナン抗原検査。真菌培養（Sabouraud寒天）で起炎真菌を同定。鳥類の気嚢系は横隔膜がなく真菌胞子が直接肺・気嚢に到達するため、Aspergillosisが最多の真菌性肺炎原因"
}

# 111. bird_dermatophytosis_ringworm — Dermatophytosis (Ringworm)
ENRICHMENTS["bird_dermatophytosis_ringworm"] = {
    "diagnosis_ja": "皮膚病変の視診（円形脱羽・鱗屑・痂皮：特に頭部・脚部）。皮膚掻破のKOH直接鏡検で真菌菌糸・分節胞子を検出。真菌培養（DTM培地・Sabouraud寒天）でMicrosporum・Trichophyton等を同定。Wood灯検査（一部のMicrosporum属でapple-green蛍光）。皮膚生検・病理組織検査でPAS染色陽性の真菌要素を確認。CBC（採血量≤体重の1%）で全身状態を評価。鳥類の皮膚糸状菌症は比較的稀だが、免疫低下鳥やストレス下の鳥で発症しうる"
}

# 112. bird_dactylariosis — Dactylariosis
ENRICHMENTS["bird_dactylariosis"] = {
    "diagnosis_ja": "神経症状（運動失調・斜頸・起立不能）の臨床評価。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多を確認。血液生化学でAST・LDH上昇を測定。頭部CT/MRI（大型鳥で実施可能）で脳実質の肉芽腫性病変を検索。真菌培養でDactylaria（Ochroconis）gallopavaを同定。病理組織検査（剖検例）で脳・肺・肝臓の肉芽腫内に暗色分節菌糸を確認。鳥類のDactylariosis は七面鳥・鶏に好発する深在性真菌症で、脳型は致死率が高い。環境中の腐敗有機物が感染源"
}

# 113. bird_histoplasmosis — Histoplasmosis
ENRICHMENTS["bird_histoplasmosis"] = {
    "diagnosis_ja": "呼吸器症状・全身性感染徴候の臨床評価。CBC（採血量≤体重の1%）でヘテロフィル増加・単球増多を確認。血液生化学でAST・LDH上昇（肝脾障害）を測定。胸部X線で肺野結節影・肝脾腫を評価。FNA細胞診でマクロファージ内の小型酵母体（2-4μm）を確認（ギムザ染色）。真菌培養（BSL-3施設）でHistoplasma capsulatumを同定。Histoplasma抗原検査。鳥類は本菌の主要保有宿主（鳥糞中で増殖）だが臨床感染は稀で、免疫抑制鳥で発症する。人獣共通感染症として公衆衛生上重要"
}

# 114. bird_microsporidiosis — Microsporidiosis
ENRICHMENTS["bird_microsporidiosis"] = {
    "diagnosis_ja": "慢性削痩・下痢・神経症状の臨床評価。糞便検査で特殊染色（ウェーバー変法トリクローム染色・カルコフロールホワイト蛍光染色）により微胞子虫の胞子（1-3μm）を検出。PCR検査でEncephalitozoon属等の種同定。CBC（採血量≤体重の1%）でリンパ球変動を評価。血液生化学でAST・UA上昇を測定。腎超音波で腎腫大を評価。病理組織検査で腎尿細管・脳・消化管内の胞子を確認。鳥類ではEncephalitozoon hellemによる腎炎・脳炎が報告されている"
}

# 115. bird_hexamitosis — Hexamitosis
ENRICHMENTS["bird_hexamitosis"] = {
    "diagnosis_ja": "水様性下痢・削痩・膨羽の臨床評価（特に幼鳥で重篤）。新鮮糞便の直接塗抹鏡検で運動性のある洋梨型原虫（Spironucleus/Hexamita: 6-12μm・6-8本鞭毛）を検出。糞便のギムザ染色で形態確認。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でTP低下・グルコース低下を測定。そのう洗浄液の鏡検（上部消化管感染型）。鳥類ではHexamitosis は家禽・猛禽・フィンチに好発し、冷温環境下での検体処理が原虫運動性保持に重要（室温で急速に死滅）"
}

# 116. bird_cochlosoma_infection — Cochlosoma Infection
ENRICHMENTS["bird_cochlosoma_infection"] = {
    "diagnosis_ja": "水様性下痢・削痩・成長遅延の臨床評価（特にフィンチ類の幼鳥）。新鮮糞便の直接塗抹鏡検で運動性のあるCochlosoma原虫（5-10μm・楕円形・腹面吸着盤が特徴）を検出。ギムザ染色で形態確認。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でTP低下・グルコース低下を測定。鳥類のCochlosoma感染は文鳥・十姉妹等のフィンチ類に好発し、Trichomonasとの形態学的鑑別が重要。検体は採取後30分以内に検鏡する（原虫の運動性が急速に低下）"
}

# 117. bird_syngamus_gapeworm — Syngamus (Gapeworm)
ENRICHMENTS["bird_syngamus_gapeworm"] = {
    "diagnosis_ja": "開口呼吸・頭部振り・呼吸困難（gaping behavior）の臨床評価。気管内視鏡でY字型に永久交尾した赤色の雌雄虫体（Syngamus trachea）を直視確認。糞便検査（浮遊法）で楕円形の虫卵（70-100×40-50μm）を検出。CBC（採血量≤体重の1%）で好酸球増加・ヘテロフィル変動を評価。気管X線で気管内軟部組織影を確認。鳥類のSyngamus trachea は気管内に寄生するため少数の虫体でも重篤な呼吸困難を惹起し、小型種では気道閉塞が致死的となる"
}

# 118. bird_acanthocephalan_infection_thorny-headed_worms — Acanthocephalan Infection
ENRICHMENTS["bird_acanthocephalan_infection_thorny-headed_worms"] = {
    "diagnosis_ja": "削痩・下痢・消化管出血の臨床評価。糞便検査（浮遊法）で楕円形の厚殻虫卵を検出。排泄された虫体の形態学的同定（吻部の鉤を持つ棘頭が特徴）。CBC（採血量≤体重の1%）で好酸球増加・PCV低下（消化管出血）を確認。血液生化学でTP低下・アルブミン低下を測定。腹部X線で消化管壁肥厚を評価。鳥類ではPolymorphus属・Filicollis属が水禽に好発し、棘頭虫の吻部が腸壁に深く穿入して穿孔・腹膜炎を起こすことがある。中間宿主は淡水甲殻類"
}

# 119. bird_cnemidocoptes_pilae_scaly_leg_mite — Cnemidocoptes pilae (Scaly Leg Mite)
ENRICHMENTS["bird_cnemidocoptes_pilae_scaly_leg_mite"] = {
    "diagnosis_ja": "嘴・蝋膜・脚の過角化病変（白色〜灰色の蜂巣状痂皮：honeycomb appearance）の視診。皮膚掻破検体の顕微鏡検査でCnemidocoptes pilae（球形・短脚のダニ・200-400μm）を検出。KOH処理で角質を透明化し虫体・虫卵を確認。CBC（採血量≤体重の1%）で軽度ヘテロフィル変動を評価。鳥類ではセキセイインコに最も好発し、嘴基部の蜂巣状過角化が特徴的な初発徴候。進行すると嘴変形・脚鱗の著明な肥厚をもたらす。イベルメクチン局所/経口投与で治療反応性の確認も診断的"
}

# 120. bird_myiasis_fly_strike — Myiasis (Fly Strike)
ENRICHMENTS["bird_myiasis_fly_strike"] = {
    "diagnosis_ja": "皮膚・創傷部の視診でハエ幼虫（蛆虫）を確認。創傷周囲の組織壊死・悪臭を評価。幼虫の形態学的同定（Lucilia・Calliphora・Sarcophaga等）。CBC（採血量≤体重の1%）でヘテロフィル著増（二次感染）・PCV低下（出血・消耗）を確認。血液生化学でTP低下・AST上昇・UA変動を測定。X線で深部組織浸潤を評価。鳥類では屋外飼育鳥の排泄腔周囲・創傷部にハエが産卵し、幼虫の組織侵食で急速に重篤化する。衰弱鳥・汚染環境が最大のリスク因子"
}

# 121. bird_tick_infestation — Tick Infestation
ENRICHMENTS["bird_tick_infestation"] = {
    "diagnosis_ja": "体表の詳細な視診・触診で吸血中のマダニ（Ixodes・Haemaphysalis等）を確認。頭部・眼周囲・耳孔周囲・翼下・総排泄腔周囲を重点的に検索。虫体の形態学的同定。CBC（採血量≤体重の1%）でPCV低下（大量寄生時の貧血）・好酸球増加を確認。血液塗抹で媒介性血液寄生虫（Borrelia・Haemoproteus等）を検索。鳥類のマダニ寄生は各種病原体（Borrelia・Anaplasma・ウイルス等）の媒介リスクがあり、野鳥のダニモニタリングは疫学的にも重要"
}

# 122. bird_hippoboscid_fly_infestation — Hippoboscid Fly Infestation
ENRICHMENTS["bird_hippoboscid_fly_infestation"] = {
    "diagnosis_ja": "体表・羽毛間の視診でシラミバエ（Hippoboscidae：扁平な体形・強靭な脚で羽毛に固着）を確認。虫体の形態学的同定（Pseudolynchia・Ornithomya等）。CBC（採血量≤体重の1%）でPCV低下（大量寄生時の貧血）を確認。血液塗抹でHaemoproteus等の血液寄生虫（シラミバエ媒介）を検索。羽毛損傷パターンの評価。鳥類のシラミバエはHaemoproteusの主要媒介者であり、寄生虫感染の同時スクリーニングが不可欠。猛禽類・ハト類に特に多い"
}

# 123. bird_proventricular_nematodes — Proventricular Nematodes
ENRICHMENTS["bird_proventricular_nematodes"] = {
    "diagnosis_ja": "慢性嘔吐・削痩・未消化便の臨床評価。糞便検査（浮遊法）で特徴的な線虫卵を検出。そのう/前胃洗浄液の鏡検で幼虫・虫卵を検索。内視鏡で前胃（proventriculus）粘膜の発赤・腫脹と虫体を直視確認。CBC（採血量≤体重の1%）で好酸球増加・ヘテロフィル変動を評価。血液生化学でTP低下・グルコース低下を測定。X線で前胃拡張を評価。鳥類ではDispharynx nasuta・Tetrameres属が前胃に寄生し、粘膜の肉芽腫性炎症と消化障害を惹起する"
}

# 124. bird_valvular_heart_disease — Valvular Heart Disease
ENRICHMENTS["bird_valvular_heart_disease"] = {
    "diagnosis_ja": "聴診で収縮期/拡張期心雑音を評価（鳥類の正常心拍数は種により200-600 bpm）。心エコーで弁膜肥厚・逆流ジェット・心腔拡大・FSを測定。胸部X線で心拡大・肺うっ血・肝うっ血を確認。心電図で不整脈パターンを記録。CBC・血液生化学（採血量≤体重の1%）でAST・LDH・UA・cTnI上昇を測定。鳥類の弁膜疾患は老齢大型オウム（アマゾン・ヨウム）に多く、僧帽弁閉鎖不全と動脈硬化の合併が高頻度。超音波ドプラでの逆流評価が確定診断に不可欠"
}

# 125. bird_amyloidosis_systemic — Amyloidosis (Systemic)
ENRICHMENTS["bird_amyloidosis_systemic"] = {
    "diagnosis_ja": "慢性削痩・肝腫大・腹水の臨床評価。血液生化学（採血量≤体重の1%）でTP/アルブミン低下・肝酵素（AST・LDH）上昇・UA上昇を測定。腹部超音波で肝腫大・脾腫・腎腫大を描出。FNA細胞診・臓器生検でコンゴーレッド染色陽性のアミロイド沈着を確認（偏光顕微鏡でapple-green偏光が特徴的）。CBC で慢性変化を評価。鳥類ではアヒル・ガチョウ等の水禽類に全身性AAアミロイドーシスが多発し、慢性炎症性疾患（bumblefoot等）が続発性アミロイドの誘因となる"
}

# 126. bird_adrenal_gland_disease — Adrenal Gland Disease
ENRICHMENTS["bird_adrenal_gland_disease"] = {
    "diagnosis_ja": "内分泌症状の評価（多飲多尿・筋萎縮・羽毛異常・沈鬱/過活動）。血液生化学（採血量≤体重の1%）で電解質（Na/K比）・グルコース・TP変動を測定。コルチコステロン基礎値測定（鳥類はコルチゾールでなくコルチコステロンが主要グルココルチコイド）。ACTH刺激試験（合成ACTH 25μg/kg IM、0分/60分のコルチコステロン比較）。腹部超音波で副腎の腫大/萎縮を評価。鳥類の副腎疾患はアスペルギルス感染による副腎破壊や腫瘍性病変が主因として報告されている"
}

# 127. bird_thyroid_carcinoma — Thyroid Carcinoma
ENRICHMENTS["bird_thyroid_carcinoma"] = {
    "diagnosis_ja": "頸部腫瘤・呼吸困難（気管圧迫）・嚥下困難の臨床評価。頸部触診で甲状腺領域の硬い腫瘤を確認。頸部X線・CTで腫瘤のサイズ・気管偏位・浸潤範囲を判定。FNA細胞診で甲状腺腫瘍細胞の形態評価（濾胞型・乳頭型の鑑別）。組織生検・病理組織検査で確定診断。血液生化学（採血量≤体重の1%）でT4値を測定。CBC で全身状態を評価。鳥類の甲状腺癌は甲状腺腺腫と鑑別が必要で、浸潤性増殖・転移の有無が鑑別点となる"
}

# 128. bird_seminoma — Seminoma
ENRICHMENTS["bird_seminoma"] = {
    "diagnosis_ja": "腹部膨満・片脚麻痺（腎/坐骨神経圧迫）・雌性化（蝋膜色変化）の臨床評価。腹部X線で腹腔内腫瘤影を確認。超音波検査で精巣腫瘤のサイズ・エコーパターンを評価。CT検査で腫瘤の範囲・浸潤度を判定。CBC（採血量≤体重の1%）で貧血・白血球変動を確認。血液生化学でAST・LDH・エストロゲン上昇を測定。鳥類のセミノーマはセキセイインコの精巣腫瘍として最も多く、エストロゲン産生により蝋膜の褐色化（雌性化）が特徴的な臨床徴候"
}

# 129. bird_cholangiocellular_carcinoma — Cholangiocellular Carcinoma
ENRICHMENTS["bird_cholangiocellular_carcinoma"] = {
    "diagnosis_ja": "腹部膨満・削痩・黄色尿酸（肝障害示唆）の臨床評価。血液生化学（採血量≤体重の1%）で肝酵素（AST・GGT・LDH）著増・胆汁酸上昇・TP/アルブミン低下を確認。腹部超音波で肝実質の不均一なエコーパターン・腫瘤を描出。X線で肝陰影拡大を評価。肝FNA細胞診で腫瘍細胞（胆管上皮由来の腺癌細胞）を確認。CT検査で転移を検索。鳥類では胆管細胞癌はアマゾン等の大型オウムで報告があり、進行例では体腔液貯留を伴う"
}

# 130. bird_proventricular_ulceration — Proventricular Ulceration
ENRICHMENTS["bird_proventricular_ulceration"] = {
    "diagnosis_ja": "嘔吐（血液混入）・黒色便（メレナ）・食欲低下・削痩の臨床評価。内視鏡で前胃（proventriculus）粘膜の潰瘍・出血・浮腫を直視確認し生検。CBC（採血量≤体重の1%）でPCV低下（消化管出血）・ヘテロフィル変動を確認。血液生化学でTP低下・AST上昇を測定。糞便潜血検査。腹部X線で前胃拡張を評価。鳥類の前胃潰瘍はMacrorhabdus感染・NSAID投与・ストレス・重金属中毒・ABV/PDD等が原因で、前胃の腺分泌機能障害が消化障害を増悪させる"
}

# 131. bird_ingluvoliths_crop_stones — Ingluvoliths (Crop Stones)
ENRICHMENTS["bird_ingluvoliths_crop_stones"] = {
    "diagnosis_ja": "そのう（crop）触診で硬い腫瘤を確認。頸部X線でそのう内の高密度結石影を検出。造影X線で結石と周囲軟部組織の関係を評価。CBC（採血量≤体重の1%）でヘテロフィル変動を評価。血液生化学でTP・グルコースを測定（栄養障害の評価）。内視鏡でそのう内腔の結石と粘膜状態を直視確認。鳥類のそのう結石は慢性そのう炎・異物摂取・脱水によるそのう内容物の乾燥固化が原因で、食道閉塞→嘔吐・栄養障害を惹起する"
}

# 132. bird_coelomic_effusion_ascites — Coelomic Effusion (Ascites)
ENRICHMENTS["bird_coelomic_effusion_ascites"] = {
    "diagnosis_ja": "腹部膨満・呼吸困難（体腔液による気嚢圧迫）の臨床評価。腹部超音波で体腔液貯留を確認・半定量評価。体腔穿刺（coelomocentesis）で液体を採取し、細胞診・蛋白/比重測定（漏出液vs滲出液の鑑別）・培養を実施。CBC（採血量≤体重の1%）でヘテロフィル変動・PCV変動を確認。血液生化学でTP/アルブミン（低蛋白性漏出液）・肝酵素・UA（腎不全）を測定。鳥類では横隔膜がなく体腔（coelom）は単一腔のため、体腔液は呼吸機能に直接影響する"
}

# 133. bird_feather_follicle_cyst_chronic — Feather Follicle Cyst (Chronic)
ENRICHMENTS["bird_feather_follicle_cyst_chronic"] = {
    "diagnosis_ja": "皮膚の腫瘤性病変の視診・触診（嚢胞性・波動感のある腫瘤、反復性腫脹歴）。切開排液で嚢胞内容物（ケラチン・変性羽毛物質）を確認。FNA細胞診で嚢胞壁細胞とケラチン片を評価。X線で深部浸潤・骨関与を除外。CBC（採血量≤体重の1%）で二次感染に伴うヘテロフィル増加を確認。病理組織検査で濾胞壁の慢性炎症・線維化を評価。鳥類の羽毛嚢胞はカナリア（特にNorwich・Gloucester種）に好発し、遺伝的に柔らかい羽毛が皮膚を穿通できず嚢胞化する"
}

# 134. bird_nutritional_secondary_hyperparathyroidism — Nutritional Secondary Hyperparathyroidism
ENRICHMENTS["bird_nutritional_secondary_hyperparathyroidism"] = {
    "diagnosis_ja": "食餌歴の詳細聴取（Ca欠乏・Ca:P比不適切・VitD3不足・UVBライト不使用）。全身X線で骨密度低下・皮質菲薄化・病的骨折・骨変形を評価。血液生化学（採血量≤体重の1%）でCa低下/正常（PTH代償）・P上昇・ALP上昇を確認。PTH測定（上昇）。竜骨・長管骨の触診で骨軟化を確認。鳥類では種子食偏重の飼育鳥に極めて多く、Ca:P比の不適切（理想は2:1）とVitD3不足が主因。幼鳥では嘴軟化・脚変形・病的骨折が特徴的所見"
}

# 135. bird_biotin_deficiency — Biotin Deficiency
ENRICHMENTS["bird_biotin_deficiency"] = {
    "diagnosis_ja": "食餌歴の詳細聴取（生卵白の過剰摂取→アビジンによるビオチン結合、単調な種子食）。皮膚・羽毛の視診で鱗屑性皮膚炎・脱羽・羽毛質低下を確認。足底の皮膚炎（足底皮膚炎との鑑別）。血液生化学（採血量≤体重の1%）でTP・アルブミン低下を測定。CBC で貧血を評価。鳥類のビオチン欠乏は家禽で脂肪肝腎症候群（FLKS）の一因として重要。幼鳥では足底皮膚炎・嘴周囲の痂皮・孵化率低下が特徴的。ビオチン補充への反応で診断を確認"
}

# 136. bird_niacin_deficiency_pellagra — Niacin Deficiency (Pellagra)
ENRICHMENTS["bird_niacin_deficiency_pellagra"] = {
    "diagnosis_ja": "食餌歴の詳細聴取（トウモロコシ主体食→トリプトファン/ナイアシン欠乏リスク）。臨床症状の評価（口腔/舌の炎症・下痢・皮膚炎・脚の腫脹）。血液生化学（採血量≤体重の1%）でTP低下・代謝異常を評価。CBC で貧血を確認。X線で脛足根骨の弯曲・関節腫脹（perosis様変化）を評価。鳥類のナイアシン欠乏はアヒル・七面鳥の幼鳥でperosis（腱脱臼）の一因となり、ナイアシン補充への臨床反応（口腔炎・下痢の改善）が診断的価値を持つ"
}

# 137. bird_riboflavin_deficiency — Riboflavin Deficiency
ENRICHMENTS["bird_riboflavin_deficiency"] = {
    "diagnosis_ja": "食餌歴の詳細聴取（種子食偏重・単調食・VitB2無添加）。臨床症状の評価：幼鳥のcurled toe paralysis（趾巻き込み麻痺）・成鳥の脚麻痺・成長遅延。神経学的検査で末梢神経障害を評価。血液生化学（採血量≤体重の1%）でTP低下を測定。CBC で貧血を評価。X線で骨格異常を確認。鳥類のリボフラビン欠乏はcurled toe paralysisが最も特徴的な臨床徴候で、坐骨神経の髄鞘変性が原因。早期のVitB2補充で可逆的だが、遅れると永続的変形となる"
}

# 138. bird_thiamine_deficiency_star-gazing — Thiamine Deficiency (Star-Gazing)
ENRICHMENTS["bird_thiamine_deficiency_star-gazing"] = {
    "diagnosis_ja": "食餌歴の詳細聴取（生魚の過剰摂取→チアミナーゼによるVitB1分解、加熱処理された魚は安全）。神経学的検査でstar-gazing posture（頭部後屈）・後弓反張・運動失調・痙攣を評価。血液生化学（採血量≤体重の1%）で乳酸上昇を確認。全血チアミン（VitB1）測定。CBC で全身状態を評価。鳥類のチアミン欠乏は魚食性鳥類（ペンギン・サギ等）で好発し、Chastek paralysisとして知られる。チアミン補充（IM投与）への急速な臨床反応が診断的"
}

# 139. bird_vitamin_k_deficiency — Vitamin K Deficiency
ENRICHMENTS["bird_vitamin_k_deficiency"] = {
    "diagnosis_ja": "出血傾向（皮下出血・血便・出血斑）の臨床評価。凝固検査でPT延長・APTT延長を確認。血液生化学（採血量≤体重の1%）でTP・アルブミンを測定。CBC でPCV低下（出血性貧血）を確認。食餌歴聴取（VitK欠乏リスク：長期抗菌薬投与による腸内細菌叢破壊）。殺鼠剤曝露歴の確認（抗凝固性殺鼠剤はVitK拮抗薬）。鳥類のVitK欠乏は長期抗菌薬投与後のcecal flora破壊や、抗凝固性殺鼠剤中毒で発生し、VitK1補充（IM）への反応で診断を確認"
}

# 140. bird_hypervitaminosis_d — Hypervitaminosis D
ENRICHMENTS["bird_hypervitaminosis_d"] = {
    "diagnosis_ja": "食餌・サプリメント歴の詳細聴取（VitD3過剰補充・不適切なサプリメント投与）。血液生化学（採血量≤体重の1%）で高Ca血症（>12 mg/dL）・高P血症・BUN/UA上昇（腎障害）を確認。X線で軟部組織石灰化（腎・血管・消化管壁）・骨密度異常を評価。腹部超音波で腎高エコー実質（石灰化）を確認。CBC で全身状態を評価。鳥類のVitD過剰症は腎臓のCa沈着→腎不全→痛風の連鎖を惹起し、軟部組織のmetastatic calcificationが致死的"
}

# 141. bird_hypervitaminosis_a — Hypervitaminosis A
ENRICHMENTS["bird_hypervitaminosis_a"] = {
    "diagnosis_ja": "食餌・サプリメント歴の詳細聴取（VitA過剰補充・レバー過剰摂取）。臨床症状の評価（皮膚乾燥・脱羽・骨格異常・肝障害）。血液生化学（採血量≤体重の1%）で肝酵素（AST）上昇・Ca変動を確認。X線で骨膜増殖・骨格異常を評価。肝超音波で肝実質変化を確認。CBC で全身状態を評価。鳥類ではVitA過剰はVitA欠乏より稀だが、不適切なサプリメント使用で発生する。VitA欠乏（口腔内白色結節・扁平上皮化生）との鑑別が重要"
}

# 142. bird_plant_toxicity — Plant Toxicity
ENRICHMENTS["bird_plant_toxicity"] = {
    "diagnosis_ja": "曝露歴の詳細聴取（摂取した植物の同定・摂取量・経過時間）。臨床症状の評価（嘔吐・下痢・神経症状・心臓症状は植物種により異なる）。血液生化学（採血量≤体重の1%）で肝酵素・UA・グルコース・電解質変動を測定。CBC でヘテロフィル変動を評価。そのう洗浄液の分析で植物片を確認。心電図（ジギタリス含有植物の場合）。鳥類ではアボカド（persin→心筋壊死）・ユリ科・ナス科・イチイ等が特に危険で、少量摂取でも致死的な中毒を起こしうる"
}

# 143. bird_rodenticide_poisoning — Rodenticide Poisoning
ENRICHMENTS["bird_rodenticide_poisoning"] = {
    "diagnosis_ja": "曝露歴の聴取（殺鼠剤への直接摂取・中毒げっ歯類の二次摂取）。臨床症状の評価（出血傾向・血便・呼吸困難・神経症状）。凝固検査でPT・APTT著延長を確認（抗凝固性殺鼠剤の場合）。CBC（採血量≤体重の1%）でPCV低下（出血性貧血）を確認。血液生化学でAST・UA変動を測定。腹部X線で消化管内異物を検索。毒物分析で血中殺鼠剤成分を検出。鳥類は抗凝固性殺鼠剤（ブロマジオロン等）に感受性が高く、二次中毒（中毒げっ歯類を捕食）が猛禽類で重要"
}

# 144. bird_essential_oil_toxicity — Essential Oil Toxicity
ENRICHMENTS["bird_essential_oil_toxicity"] = {
    "diagnosis_ja": "曝露歴の詳細聴取（芳香精油の種類・ディフューザー使用・直接接触/吸入の区別）。呼吸器症状（呼吸困難・気嚢炎症状）の評価。CBC（採血量≤体重の1%）でヘテロフィル変動を確認。血液生化学でAST・LDH上昇（肝障害）を測定。胸部X線で肺野・気嚢の変化を評価。鳥類は高効率な気嚢系ガス交換のため揮発性有機化合物への感受性が極めて高く、ティーツリーオイル・ユーカリ・ペパーミント等の精油蒸気は微量でも呼吸器障害を惹起する"
}

# 145. bird_phallus_prolapse — Phallus Prolapse
ENRICHMENTS["bird_phallus_prolapse"] = {
    "diagnosis_ja": "排泄腔からの陰茎（phallus）の脱出を視診で確認（アヒル・ガチョウ等の水禽類で発生、オウム目は陰茎なし）。脱出組織の色調・浮腫・壊死の有無を評価。CBC（採血量≤体重の1%）でヘテロフィル増加（二次感染）を確認。血液生化学でTP・UA・グルコースを測定。腹部X線で腹腔内異常を除外。培養で二次感染菌を同定。鳥類の陰茎脱出は交尾後の非整復・外傷・感染が主因で、脱出が長時間持続すると浮腫→壊死→壊疽に進展し切断が必要となる"
}

# 146. bird_air_sac_rupture — Air Sac Rupture
ENRICHMENTS["bird_air_sac_rupture"] = {
    "diagnosis_ja": "皮下気腫（subcutaneous emphysema）の触診で皮下のcrepitusを確認。外傷歴の聴取。胸部X線で気嚢壁の不連続・皮下気腫・腹腔内遊離ガスを評価。CT検査で破裂気嚢の特定と範囲を判定。CBC（採血量≤体重の1%）で二次感染の有無を確認。血液生化学でAST・LDH変動を測定。鳥類は9個の気嚢（頸部・鎖骨間・前胸・後胸・腹部の各対＋鎖骨間嚢）を有し、外傷・呼吸器感染による気嚢破裂は皮下気腫として顕在化する。穿刺脱気で症状緩和"
}

# 147. bird_nail_overgrowth___nail_injury — Nail Overgrowth / Nail Injury
ENRICHMENTS["bird_nail_overgrowth___nail_injury"] = {
    "diagnosis_ja": "爪の視診で過長・弯曲・血管走行を確認。爪損傷の評価（断裂・出血・基部腫脹）。止まり木の適切性評価（サイズ・材質・表面テクスチャー）。CBC（採血量≤体重の1%）で二次感染の有無を確認。X線検査で趾骨の骨折・骨髄炎を除外。基礎疾患のスクリーニング（肝疾患→爪の変形/過長、PBFD→爪異常）。鳥類の爪は持続成長するため定期的なトリミングが必要で、不適切な止まり木は爪過長と足底潰瘍の両方のリスク因子となる"
}

# 148. bird_contact_dermatitis — Contact Dermatitis
ENRICHMENTS["bird_contact_dermatitis"] = {
    "diagnosis_ja": "皮膚病変の分布パターン評価（接触部位限局性：足底・腹部・脚・嘴周囲）。曝露歴の聴取（新しいケージ材・洗剤・消毒薬・止まり木材質・床材）。皮膚掻破・細胞診で好酸球浸潤を評価。皮膚生検で表層性皮膚炎パターンを確認。CBC（採血量≤体重の1%）で好酸球増加を確認。感染性原因の除外（培養・KOH検鏡）。鳥類の接触性皮膚炎は亜鉛メッキケージ・消毒薬残留・人工芝等の化学物質接触で発生し、原因物質の除去が治療の根幹"
}

# 149. bird_preen_gland_abscess_uropygial_gland — Preen Gland Abscess
ENRICHMENTS["bird_preen_gland_abscess_uropygial_gland"] = {
    "diagnosis_ja": "尾腺（uropygial gland）の視診・触診で腫脹・発赤・波動感・排膿を確認。FNA細胞診でヘテロフィル優位炎症・細菌を検索。細菌培養・感受性試験で起炎菌を同定。CBC（採血量≤体重の1%）でヘテロフィル増加を確認。血液生化学でAST・TP変動を測定。X線で深部浸潤・骨関与を除外。鳥類の尾腺は防水脂を分泌する重要な腺で、導管閉塞→膿瘍形成が病態。尾腺腫瘍（腺腫・腺癌）との鑑別が重要で、慢性例では生検を推奨"
}

# 150. bird_preen_gland_adenoma_carcinoma — Preen Gland Adenoma/Carcinoma
ENRICHMENTS["bird_preen_gland_adenoma_carcinoma"] = {
    "diagnosis_ja": "尾腺（uropygial gland）の腫瘤の視診・触診（サイズ・硬さ・表面性状・潰瘍化の有無）。FNA細胞診で腫瘍細胞の形態評価（腺腫vs腺癌の鑑別）。組織生検・病理組織検査で確定診断と悪性度判定。X線・CT検査で局所浸潤・転移を評価。CBC（採血量≤体重の1%）で全身状態を確認。血液生化学でAST・LDH変動を測定。鳥類の尾腺腫瘍はセキセイインコ・オカメインコに好発し、腺腫は良性だが腺癌は局所浸潤性で再発率が高い"
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
