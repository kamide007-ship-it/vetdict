#!/usr/bin/env python3
"""Enrich diagnosis_ja for Rabbit entries (batch 8: remaining 54 entries)."""
import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# 1. rabbit_polydipsia___polyuria — Polydipsia / Polyuria / 多飲多尿
ENRICHMENTS["rabbit_polydipsia___polyuria"] = {
    "diagnosis_ja": "飲水量増加（>120 mL/kg/日）と尿量増加から多飲多尿を疑う。尿検査で尿比重低下を確認。生化学でBUN/Cre（腎疾患）・Ca（高Ca血症）・血糖（糖尿病）を評価。E. cuniculi抗体検査で腎型エンセファリトゾーン症を除外。肝機能検査（胆汁酸）で肝疾患を評価。超音波で腎形態・副腎を確認。24時間飲水量の正確な測定が重要。ウサギのCa代謝は腎依存性が高く、高Ca食による多尿が多い。鑑別に腎疾患・子宮疾患・副腎疾患・心因性多飲を考慮する。"
}

# 2. rabbit_chronic_weight_loss_marasmus — Chronic Weight Loss / 慢性体重減少
ENRICHMENTS["rabbit_chronic_weight_loss_marasmus"] = {
    "diagnosis_ja": "進行性の体重減少・筋萎縮・BCS低下から慢性消耗を疑う。口腔検査で臼歯不正咬合（spurs・過長）を確認（最も一般的な原因）。頭部X線で歯根伸長を評価。CBC/生化学で慢性感染・腎疾患・肝疾患を除外。糞便検査でコクシジウム・寄生虫を除外。E. cuniculi抗体検査を実施。腹部超音波で腫瘤・臓器異常を精査。食餌歴（牧草摂取量・ペレット量）と盲腸便（cecotrophy）の摂取状況を確認。ウサギの常生歯は不正咬合で咀嚼不能となり急速に削痩する。"
}

# 3. rabbit_viral_haemorrhagic_disease_vhd_-_classical — VHD Classical / ウイルス性出血病（古典型）
ENRICHMENTS["rabbit_viral_haemorrhagic_disease_vhd_-_classical"] = {
    "diagnosis_ja": "突然死・血性鼻汁・呼吸困難・けいれんからVHD古典型を疑う。RHDV1 RT-PCR（肝・脾）で確定。剖検で劇症壊死性肝炎・DIC・多臓器出血を確認。肝臓の急速自己融解が特徴的。CBC/生化学でAST・ALT著増・凝固異常・血小板減少を評価。ELISA抗体検査でワクチン接種歴との鑑別が必要。古典型は生後8週齢以上で発症し、致死率80-100%。ウサギは嘔吐反射がないため前駆症状なく突然死として発見される。RHDV2との型別はシークエンス解析で確認。"
}

# 4. rabbit_lawsonia_intracellular_infection — Lawsonia Intracellular Infection / ローソニア細胞内感染症
ENRICHMENTS["rabbit_lawsonia_intracellular_infection"] = {
    "diagnosis_ja": "幼若ウサギの慢性下痢・体重減少・削痩からLawsonia intracellularis感染を疑う。糞便PCRでLawsonia intracellularisを検出。糞便のWarthin-Starry銀染色で細胞内細菌を確認。腸管生検で回腸・盲腸の陰窩上皮細胞内に湾曲桿菌を確認し確定。CBC/生化学で低蛋白血症を評価。血清学的検査（IFA）で抗体を検出。ウサギでは増殖性腸症として回腸・盲腸の粘膜肥厚を起こす。鑑別にコクシジウム・腸管毒素血症・E. cuniculi腸管型を考慮する。"
}

# 5. rabbit_encephalitozoonosis_-_ocular_form — Encephalitozoonosis - Ocular Form / エンセファリトゾーン症 - 眼型
ENRICHMENTS["rabbit_encephalitozoonosis_-_ocular_form"] = {
    "diagnosis_ja": "白内障（特に水晶体前嚢破裂）・ぶどう膜炎・虹彩後癒着からE. cuniculi眼型を疑う。スリットランプ検査で水晶体前嚢の限局性破裂・レンズ誘発性肉芽腫性ぶどう膜炎を確認。E. cuniculi抗体検査（IgM/IgG）で感染を評価。眼超音波で水晶体構造・後方合併症を確認。房水PCRでE. cuniculiスポアを検出。眼圧測定で二次性緑内障を除外。先天性白内障との鑑別が重要で、水晶体前嚢の限局性破裂はE. cuniculi眼型に特徴的な所見。通常片側性で幼若期に発症することが多い。"
}

# 6. rabbit_spinal_cord_compression — Spinal Cord Compression / 脊髄圧迫
ENRICHMENTS["rabbit_spinal_cord_compression"] = {
    "diagnosis_ja": "後肢の進行性不全麻痺・排尿障害・固有受容感覚低下から脊髄圧迫を疑う。X線で脊椎骨折・変形性脊椎症・椎間板石灰化を確認。MRIで脊髄圧迫の部位・原因（椎間板突出・腫瘤・骨片）を精密に評価。CT検査で骨性病変の詳細を精査。神経学的検査で病変局在を特定。CBC/生化学で基礎疾患を除外。ウサギは後肢の筋量に対して脊椎が脆弱であり、保定時のパニック（キック）で脊椎骨折→脊髄圧迫が発生しやすい。E. cuniculi関連の中枢神経病変も鑑別に含める。"
}

# 7. rabbit_cerebral_larval_migrans — Cerebral Larval Migrans / 脳幼虫移行症
ENRICHMENTS["rabbit_cerebral_larval_migrans"] = {
    "diagnosis_ja": "急性神経症状（旋回・運動失調・けいれん・斜頸・視力障害）から脳幼虫移行症を疑う。MRIで脳実質内の移動性病変・浮腫を確認。CBC/生化学で好酸球増多を評価。血清学的検査でBaylisascaris procyonis（アライグマ回虫）抗体を検出。髄液検査で好酸球性髄膜脳炎を確認。確定診断は脳組織の病理検査で幼虫を確認するが生前診断は困難。アライグマとの接触歴・汚染牧草の摂取歴を聴取。E. cuniculi・中耳炎との鑑別が重要。致死率が高く予後不良。"
}

# 8. rabbit_tularaemia — Tularaemia / 野兎病
ENRICHMENTS["rabbit_tularaemia"] = {
    "diagnosis_ja": "急性発熱・沈鬱・リンパ節腫大・突然死から野兎病を疑う。血液培養でFrancisella tularensisを分離（BSL-3施設必要）。PCRで迅速検出。血清学的検査（凝集試験）でペア血清抗体価上昇を確認。剖検で肝・脾の壊死巣（白色点状）を確認。CBC/生化学でヘテロフィル著増を評価。ダニ刺咬歴・野生ウサギとの接触歴を聴取。重要な人獣共通感染症であり検体取扱いに厳重な注意が必要。届出義務のある四類感染症（日本）。"
}

# 9. rabbit_dermatophilosis — Dermatophilosis / 皮膚糸状菌症
ENRICHMENTS["rabbit_dermatophilosis"] = {
    "diagnosis_ja": "皮膚の痂皮形成・膿痂疹・「ペイントブラシ」様毛束凝集からDermatophilus congolensis感染を疑う。痂皮のギムザ染色・グラム染色で特徴的な「鉄道線路」様の横走菌糸と胞子列を確認。培養で確認するがCO2環境と特殊培地が必要。皮膚生検で表層性膿皮症と菌体を確認。CBC/生化学で基礎疾患を除外。高湿度環境・皮膚の常時湿潤が素因。ウサギでは皮膚糸状菌症（Trichophyton）や細菌性膿皮症との鑑別が重要。人獣共通感染症として注意。"
}

# 10. rabbit_mycoplasmosis — Mycoplasmosis / マイコプラズマ症
ENRICHMENTS["rabbit_mycoplasmosis"] = {
    "diagnosis_ja": "慢性呼吸器症状（くしゃみ・鼻汁・呼吸困難）・関節炎・結膜炎からマイコプラズマ症を疑う。鼻腔・気管スワブのPCRでMycoplasma pulmonis等を検出。培養は特殊培地（PPLO）が必要で時間を要する。血清学的検査で抗体を確認。気管洗浄液の細胞診で慢性炎症を評価。X線で肺野陰影を確認。CBC/生化学でヘテロフィル軽度増多を評価。ウサギではP. multocida感染との混合感染が多く、両者の同時検査が推奨される。慢性不顕性感染でストレス時に再燃する。"
}

# 11. rabbit_papilloma_virus_infection — Papilloma Virus Infection / パピローマウイルス感染症
ENRICHMENTS["rabbit_papilloma_virus_infection"] = {
    "diagnosis_ja": "皮膚の角化性疣贅状腫瘤から乳頭腫ウイルス感染を疑う。組織生検で乳頭腫性過形成と好酸性核内封入体を確認。PCRでRabbit Papillomavirus（CRPV/ROPV）を検出。免疫組織化学でウイルス抗原を検出。病理組織検査で悪性転化（扁平上皮癌）の有無を評価。CBC/生化学は通常正常。Shope乳頭腫ウイルス（CRPV）は実験的癌モデルとして有名であり、自然感染でも悪性転化の可能性がある。鑑別に扁平上皮癌・基底細胞腫・角化嚢胞を考慮する。"
}

# 12. rabbit_metastatic_calcification — Metastatic Calcification / 転移性石灰化
ENRICHMENTS["rabbit_metastatic_calcification"] = {
    "diagnosis_ja": "多臓器の石灰化（大動脈・腎・胃・心臓）・腎不全・関節硬直から転移性石灰化を疑う。X線で軟部組織（大動脈・腎・胃壁）の石灰化を確認。生化学でCa上昇・P上昇・Ca×P積の異常を評価。BUN/Cre上昇で腎機能障害を確認。超音波で腎石灰化・血管壁石灰化を評価。ウサギのCa代謝は腎排泄依存性が高く、高Ca食（アルファルファ偏重）と腎機能低下が転移性石灰化の主因。組織生検でvon Kossa染色陽性のCa沈着を確認。食餌歴の聴取が不可欠。"
}

# 13. rabbit_hypoproteinaemia — Hypoproteinaemia / 低タンパク血症
ENRICHMENTS["rabbit_hypoproteinaemia"] = {
    "diagnosis_ja": "浮腫・腹水・体重減少・削痩から低タンパク血症を疑う。生化学で総蛋白・アルブミン低値を確認。蛋白分画（電気泳動）でアルブミン/グロブリン比を評価。尿検査で蛋白尿（腎性喪失）を確認。糞便検査で寄生虫・コクシジウム（消化管性喪失）を除外。肝機能検査（胆汁酸・AST）で肝合成能低下を評価。腸管生検で蛋白漏出性腸症を鑑別。ウサギでは不正咬合による摂食不良・コクシジウム感染・腎疾患が低タンパク血症の主要原因。"
}

# 14. rabbit_hyponatraemia — Hyponatraemia / 低ナトリウム血症
ENRICHMENTS["rabbit_hyponatraemia"] = {
    "diagnosis_ja": "沈鬱・食欲不振・筋力低下・けいれん（重度時）から低ナトリウム血症を疑う。生化学でNa低値を確認し重症度を評価。浸透圧測定で低浸透圧性を確認。尿Na・尿浸透圧で腎性/腎外性を鑑別。水分バランスの評価（脱水の有無・体液量状態）。副腎機能検査（コルチゾール）で副腎不全を除外。BUN/Cre測定で腎機能を評価。原因疾患の検索（消化管喪失・腎疾患・副腎不全・心因性多飲）が治療方針に不可欠。ウサギでは過度の水分摂取や下痢に伴う喪失が多い。"
}

# 15. rabbit_megaoesophagus — Megaoesophagus / 巨大食道症
ENRICHMENTS["rabbit_megaoesophagus"] = {
    "diagnosis_ja": "流涎・嚥下困難・食欲不振・体重減少から巨大食道症を疑う。造影X線（バリウム造影）で食道の拡張・蠕動低下を確認。透視検査で嚥下動態を評価。CT検査で食道壁の構造異常・周囲組織の圧迫を精査。CBC/生化学で基礎疾患を除外。神経学的検査で全身性神経筋疾患を評価。ウサギでは本症の報告が稀であり、先天性と後天性（鉛中毒・神経障害・胸腔内腫瘤）を鑑別。ウサギは嘔吐ができないため食道内容の逆流は起こりにくいが、摂食障害による急速な削痩が問題となる。"
}

# 16. rabbit_cholelithiasis — Cholelithiasis / 胆石症
ENRICHMENTS["rabbit_cholelithiasis"] = {
    "diagnosis_ja": "食欲不振・沈鬱・腹部疼痛・黄疸から胆石症を疑う。超音波で胆嚢内の高エコー構造物と音響陰影を確認。X線でCa含有結石の高密度影を確認。生化学で肝酵素上昇（ALP・GGT）・胆汁酸上昇・ビリルビン上昇を評価。CBC/生化学でヘテロフィル増多（胆管炎合併時）を確認。糞便検査でEimeria stiedai（肝コクシジウム）のオーシストを除外。ウサギの胆石はCa含有量が高い傾向があり、高Ca食との関連が示唆される。鑑別に肝コクシジウム症・肝腫瘍を考慮。"
}

# 17. rabbit_pancreatic_disease — Pancreatic Disease / 膵臓疾患
ENRICHMENTS["rabbit_pancreatic_disease"] = {
    "diagnosis_ja": "食欲不振・腹部疼痛・下痢・体重減少から膵臓疾患を疑う。生化学でアミラーゼ・リパーゼ上昇を確認するが、ウサギでの特異度は限定的。血糖値の異常（高血糖/低血糖）で膵内分泌機能を評価。超音波で膵臓の腫大・エコー変化・嚢胞を確認。CT検査で膵腫瘤を精査。CBC/生化学で脱水・電解質異常・肝酵素異常を確認。膵生検で確定するが侵襲的。ウサギの膵疾患は犬猫と比較して報告が少なく、高脂肪食や肥満が素因として考慮される。"
}

# 18. rabbit_adrenal_hyperplasia — Adrenal Hyperplasia / 副腎過形成
ENRICHMENTS["rabbit_adrenal_hyperplasia"] = {
    "diagnosis_ja": "脱毛・攻撃性変化・外陰部腫大（雌）・乳腺発達異常から副腎過形成を疑う。超音波で両側副腎の均一な腫大を確認。ACTH刺激試験でコルチゾール過剰応答を評価。性ホルモンパネル（エストラジオール・テストステロン・17-OHプロゲステロン）を測定。CT検査で副腎の詳細形態を精査。CBC/生化学で電解質異常・高血糖を評価。ウサギでは避妊/去勢後の性ホルモン異常上昇が副腎原性を示唆する。鑑別に副腎腫瘍・卵巣遺残・外因性ホルモン曝露を考慮する。"
}

# 19. rabbit_thyroid_neoplasia — Thyroid Neoplasia / 甲状腺腫瘍
ENRICHMENTS["rabbit_thyroid_neoplasia"] = {
    "diagnosis_ja": "頸部腫瘤触知・嚥下困難・呼吸困難から甲状腺腫瘍を疑う。超音波で甲状腺の結節状腫瘤を確認。FNA細胞診で腫瘍細胞の性状を評価。甲状腺機能検査（T4・fT4）で機能性腫瘍の有無を確認。CT検査で腫瘤の大きさ・浸潤範囲・転移を精査。確定は組織生検で濾胞腺腫・濾胞癌等を分類。CBC/生化学でCa異常（C細胞腫瘍の場合カルシトニン異常）を評価。ウサギの甲状腺腫瘍は稀だが、慢性ヨウ素欠乏が甲状腺腫→腫瘍化の素因となりうる。"
}

# 20. rabbit_hydrocephalus — Hydrocephalus / 水頭症
ENRICHMENTS["rabbit_hydrocephalus"] = {
    "diagnosis_ja": "ドーム状頭蓋・斜視・運動失調・けいれん・発育遅延から水頭症を疑う。頭部MRI/CTで脳室拡大・大脳皮質菲薄化を確認し確定。超音波（幼若で泉門開存時）で脳室拡大を簡易評価。神経学的検査で意識レベル・視力・運動機能を評価。CBC/生化学で基礎疾患を除外。E. cuniculi抗体検査で感染性脳炎を鑑別。先天性（遺伝性・発達異常）と後天性（E. cuniculi脳炎後・腫瘍による閉塞）を鑑別。ウサギでは矮小品種で先天性水頭症の報告がある。"
}

# 21. rabbit_meningoencephalitis — Meningoencephalitis / 髄膜脳炎
ENRICHMENTS["rabbit_meningoencephalitis"] = {
    "diagnosis_ja": "急性神経症状（けいれん・運動失調・斜頸・旋回・意識障害）から髄膜脳炎を疑う。頭部MRI/CTで脳実質の浮腫・造影増強・髄膜増強を確認。髄液検査で細胞数増多・蛋白上昇を確認し、細胞診でリンパ球性/好中球性を分類。髄液培養・PCR（P. multocida、E. cuniculi、Listeria等）で起因菌を同定。CBC/生化学でヘテロフィル増多を評価。E. cuniculi抗体検査を実施。ウサギではE. cuniculiによる肉芽腫性脳炎とP. multocidaによる化膿性髄膜脳炎が最も一般的。"
}

# 22. rabbit_aural_polyp — Aural Polyp / 耳ポリープ
ENRICHMENTS["rabbit_aural_polyp"] = {
    "diagnosis_ja": "耳道内の腫瘤・慢性耳漏・頭振り・耳掻きから耳ポリープを疑う。耳鏡検査で外耳道内のポリープ状腫瘤を確認。頭部CT/X線で中耳・鼓室胞への波及を評価。組織生検で炎症性ポリープ（粘膜固有層の浮腫・血管増生・炎症細胞浸潤）を確認し腫瘍を除外。培養で二次感染菌を同定。CBC/生化学でヘテロフィル増多を評価。ウサギの耳ポリープは慢性中耳炎に続発することが多く、P. multocida感染が基礎にある場合が多い。ロップ種で好発する。"
}

# 23. rabbit_perineal_hernia — Perineal Hernia / 会陰ヘルニア
ENRICHMENTS["rabbit_perineal_hernia"] = {
    "diagnosis_ja": "会陰部の腫脹・膨隆・排便困難・しぶりから会陰ヘルニアを疑う。触診で会陰部の軟性腫脹と還納性を確認。X線・超音波でヘルニア内容（膀胱・腸管・脂肪）を確認。造影X線で膀胱の変位を評価。直腸検査（可能な場合）で直腸嚢の有無を確認。CBC/生化学で全身状態を評価。尿検査で膀胱変位に伴う排尿障害を確認。ウサギの会陰ヘルニアは稀であるが、未去勢雄や肥満が素因として報告されている。鑑別に膿瘍・腫瘍・脂肪腫を考慮する。"
}

# 24. rabbit_cystic_mastitis — Cystic Mastitis / 嚢胞性乳腺炎
ENRICHMENTS["rabbit_cystic_mastitis"] = {
    "diagnosis_ja": "乳腺の腫脹・波動感のある嚢胞状腫瘤・乳汁異常から嚢胞性乳腺炎を疑う。FNA細胞診で嚢胞液（漿液性〜膿性）と炎症細胞を確認。超音波で乳腺内の嚢胞構造を確認し充実性腫瘤（腫瘍）と鑑別。嚢胞液の培養で二次感染菌を同定。CBC/生化学でヘテロフィル増多・ホルモン異常を評価。ウサギでは偽妊娠・ホルモン失調が嚢胞性変化の素因。未避妊雌で好発し、乳腺腫瘍（腺癌）との鑑別が重要。鑑別に乳腺腫瘍・脂肪腫・膿瘍を考慮する。"
}

# 25. rabbit_vaginal_hyperplasia — Vaginal Hyperplasia / 膣過形成
ENRICHMENTS["rabbit_vaginal_hyperplasia"] = {
    "diagnosis_ja": "外陰部からの腫瘤状突出・排尿困難・外陰部腫脹から膣過形成を疑う。身体検査で膣粘膜の浮腫性腫脹・突出を確認。組織生検で間質の浮腫・過形成を確認し腫瘍を除外。超音波で子宮疾患（子宮腺癌・子宮蓄膿症）を同時評価。CBC/生化学でホルモン異常を評価。エストロゲン上昇の原因（卵巣嚢胞・卵巣腫瘍）を検索。ウサギでは未避妊雌のエストロゲン過剰が主因。子宮腺癌（4歳以上の未避妊雌で60-80%の発生率）の併発検索が不可欠。"
}

# 26. rabbit_neonatal_mortality_complex — Neonatal Mortality Complex / 新生児死亡症候群
ENRICHMENTS["rabbit_neonatal_mortality_complex"] = {
    "diagnosis_ja": "生後1-14日の仔ウサギの連続死亡から新生児死亡症候群を疑う。死亡仔の剖検で感染症（P. multocida・E. coli）・低体温・脱水・外傷を確認。母乳栄養の評価（母ウサギの乳腺・授乳行動）。巣の環境（温度・巣材）を確認。母ウサギのCBC/生化学・感染症検査を実施。ウサギは1日1回のみ授乳（約3-5分）する特殊な授乳パターンであり、初産母・ストレス環境で育児放棄が起こりやすい。死産・カニバリズムとの鑑別も必要。飼育環境の総合評価が重要。"
}

# 27. rabbit_ectopic_pregnancy — Ectopic Pregnancy / 子宮外妊娠
ENRICHMENTS["rabbit_ectopic_pregnancy"] = {
    "diagnosis_ja": "腹部膨満・腹膜炎徴候・食欲不振・沈鬱から子宮外妊娠を疑う。超音波で子宮外の胎仔構造を確認。X線で腹腔内の胎仔骨格を確認し子宮外の位置を評価。腹腔穿刺で血性液を確認。CBC/生化学でヘテロフィル増多・貧血を評価。ウサギでは子宮角破裂による胎仔の腹腔内脱出が子宮外妊娠の主要機序。交尾歴・妊娠歴を聴取。吸収された胎仔が腹腔内でミイラ化する場合もある。緊急外科介入が必要な場合が多い。"
}

# 28. rabbit_ovarian_neoplasia — Ovarian Neoplasia / 卵巣腫瘍
ENRICHMENTS["rabbit_ovarian_neoplasia"] = {
    "diagnosis_ja": "腹部膨満・性行動変化・脱毛パターン異常・乳腺発達から卵巣腫瘍を疑う。超音波で卵巣の腫大・内部構造異常を確認。X線で腹腔内腫瘤影を評価。FNA細胞診で腫瘍細胞を確認。性ホルモンパネル（エストラジオール・プロゲステロン・テストステロン）を測定。CBC/生化学でCa異常・貧血を評価。CT検査で転移を精査。確定は摘出組織の病理検査。ウサギでは4歳以上の未避妊雌で子宮腺癌が60-80%に発生し、卵巣腫瘍の併発も多い。早期避妊が推奨される。"
}

# 29. rabbit_haemolytic_anaemia — Haemolytic Anaemia / 溶血性貧血
ENRICHMENTS["rabbit_haemolytic_anaemia"] = {
    "diagnosis_ja": "蒼白粘膜・黄疸・赤褐色尿・沈鬱・頻呼吸から溶血性貧血を疑う。CBCでPCV低下・網状赤血球増多（再生性）を確認。血液塗抹で球状赤血球・多染性・Heinz小体・赤血球寄生虫を評価。生化学で間接ビリルビン上昇・LDH上昇・ハプトグロビン低下を確認。直接クームス試験で免疫介在性溶血を評価。毒物曝露歴（タマネギ・銅・鉛）を聴取。ウサギでは正常尿が赤色を呈するためヘモグロビン尿との鑑別にはディップスティック検査が必要。鑑別に出血性貧血を考慮。"
}

# 30. rabbit_pyelonephritis — Pyelonephritis / 腎盂腎炎
ENRICHMENTS["rabbit_pyelonephritis"] = {
    "diagnosis_ja": "発熱・腰部疼痛・多飲多尿・食欲不振から腎盂腎炎を疑う。尿検査（膀胱穿刺採取）で膿尿・細菌尿・白血球円柱を確認。尿培養・感受性試験でE. coli・P. multocida等を同定。超音波で腎盂拡張・腎実質のエコー変化・腎周囲液体貯留を確認。生化学でBUN/Cre上昇・SDMA上昇を評価。CBC/生化学でヘテロフィル著増・左方移動を確認。X線で腎結石を除外（ウサギの炭酸Ca結石は高X線透過性）。下部尿路感染からの上行感染が最も多い経路。"
}

# 31. rabbit_cecoliths — Cecoliths / 盲腸結石
ENRICHMENTS["rabbit_cecoliths"] = {
    "diagnosis_ja": "食欲不振・腹部膨満・排便減少・盲腸便産生低下から盲腸結石を疑う。X線で盲腸内の高密度陰影を確認。超音波で盲腸内の石灰化物を確認し大きさ・数量を評価。CBC/生化学でCa・BUN/Cre・電解質を確認。食餌歴（Ca過剰摂取・繊維不足・飲水不足）を聴取。ウサギの盲腸は後腸発酵の中心臓器であり、盲腸結石は盲腸機能障害→細菌叢破綻→腸管毒素血症のリスクとなる。鑑別に腸管異物・膀胱結石・GI stasisを考慮する。"
}

# 32. rabbit_enamel_hypoplasia — Enamel Hypoplasia / エナメル質形成不全
ENRICHMENTS["rabbit_enamel_hypoplasia"] = {
    "diagnosis_ja": "切歯の変色・表面不整・脆弱性・不正咬合からエナメル質形成不全を疑う。口腔検査で切歯表面の横溝・白斑・褐色変色を確認。頭部X線で歯の構造異常・歯根伸長を評価。CT検査で歯冠・歯根の詳細な構造を精査。CBC/生化学でCa・P・ビタミンD3を評価し代謝性骨疾患を除外。ウサギの常生歯（open-rooted teeth）ではエナメル質形成不全が歯の構造脆弱化→不正咬合の悪循環を引き起こす。幼若期の栄養障害・感染症・外傷が素因となる。"
}

# 33. rabbit_cutaneous_horn — Cutaneous Horn / 皮角
ENRICHMENTS["rabbit_cutaneous_horn"] = {
    "diagnosis_ja": "皮膚表面から突出する角状の硬い構造物を視診で確認。基部の皮膚病変を評価し、組織生検で基底部の組織型（角化症・ウイルス性乳頭腫・日光角化症・扁平上皮癌）を確定。CRPV PCRでパピローマウイルス感染を評価。CBC/生化学で基礎疾患を除外。ウサギではShope乳頭腫ウイルスが皮角様病変を形成することがあり、悪性転化（扁平上皮癌）の可能性があるため基部の病理組織学的評価が不可欠。完全切除後の組織検査で良悪性を判定する。"
}

# 34. rabbit_acariasis_notoedres — Acariasis (Notoedres) / ノトエドレス疥癬
ENRICHMENTS["rabbit_acariasis_notoedres"] = {
    "diagnosis_ja": "顔面・耳介・脚部の激しい掻痒・痂皮形成・脱毛からNotoedres cati var. cuniculiによる疥癬を疑う。皮膚掻破検体のKOH直接鏡検でダニ虫体・卵・糞粒を確認。Notoedresは球形の虫体で背側に肛門が位置する特徴を持つ。皮膚生検で表皮内トンネルとダニ断面を確認。CBC/生化学で好酸球増多を評価。Sarcoptes・Cheyletiella・Psoroptes等他のダニ種との鑑別が重要。人獣共通感染症の可能性があり飼い主への感染注意を説明する。"
}

# 35. rabbit_warble_fly_larvae_hypoderma — Warble Fly Larvae / ウマバエ幼虫症
ENRICHMENTS["rabbit_warble_fly_larvae_hypoderma"] = {
    "diagnosis_ja": "皮下の腫脹・呼吸孔（気門孔）を持つ皮下結節からウマバエ（Cuterebra）幼虫寄生を疑う。視診・触診で皮下結節内の幼虫の運動を確認。結節の呼吸孔から幼虫を直接確認し摘出。摘出幼虫の形態で虫種を同定。CBC/生化学で好酸球増多を評価。二次感染の培養・感受性試験を実施。屋外飼育歴・季節（夏季〜秋季）を聴取。ウサギでは頸部・胸部に好発し、幼虫の不完全摘出はアナフィラキシー反応を起こす危険があるため慎重な摘出が必要。"
}

# 36. rabbit_calciphylaxis — Calciphylaxis / カルシフィラキシス
ENRICHMENTS["rabbit_calciphylaxis"] = {
    "diagnosis_ja": "皮膚の有痛性紫斑・壊死性潰瘍・壊疽（特に四肢末端・耳介）からカルシフィラキシスを疑う。皮膚生検で小血管の中膜石灰化・血管内血栓・皮下脂肪壊死を確認。生化学でCa・P上昇・Ca×P積の著増を確認。BUN/Cre測定で腎機能障害を評価。X線で広範な軟部組織石灰化を確認。PTH測定で二次性上皮小体機能亢進症を評価。ウサギのCa代謝は腎排泄依存性が高く、腎不全時のCa×P積上昇が小血管石灰化の主因。致死率が高い。"
}

# 37. rabbit_pulmonary_oedema — Pulmonary Oedema / 肺水腫
ENRICHMENTS["rabbit_pulmonary_oedema"] = {
    "diagnosis_ja": "急性呼吸困難・チアノーゼ・湿性ラ音・開口呼吸から肺水腫を疑う。X線で肺野のびまん性陰影増強・気管支周囲のカフィング像を確認。超音波心臓検査で心不全の有無を評価。血液ガス分析で低酸素血症を確認。CBC/生化学で低蛋白血症・心筋マーカー・腎機能を評価。ウサギは絶対的経鼻呼吸動物であるため肺水腫による呼吸困難は極めて危険。原因鑑別（心原性 vs 非心原性：過剰輸液・毒素・感染・アナフィラキシー）が治療方針に不可欠。"
}

# 38. rabbit_chordoma — Chordoma / 脊索腫
ENRICHMENTS["rabbit_chordoma"] = {
    "diagnosis_ja": "尾部・仙骨部の緩徐増大する腫瘤から脊索腫を疑う。X線で仙尾椎の骨溶解性病変を確認。CT/MRIで腫瘤の範囲・脊柱管浸潤を精査。FNA細胞診で特徴的な物理化学様（physaliphorous）細胞を確認。組織生検で確定し、粘液基質内の空胞化細胞を確認。免疫組織化学（ブラキュリー・サイトケラチン陽性）で確認。CBC/生化学で全身状態を評価。ウサギでは仙尾部の脊索腫が比較的多く報告されており、緩徐に局所浸潤性に増大する低悪性度腫瘍。"
}

# 39. rabbit_tracheal_stenosis — Tracheal Stenosis / 気管狭窄
ENRICHMENTS["rabbit_tracheal_stenosis"] = {
    "diagnosis_ja": "吸気性喘鳴・呼吸困難・運動不耐性から気管狭窄を疑う。X線で気管内腔の局所的狭窄を確認。CT検査で狭窄の部位・範囲・程度を精密評価。気管内視鏡で狭窄部を直視下確認し、肉芽腫・瘢痕・圧迫を鑑別。気管洗浄液の培養・細胞診で感染を評価。CBC/生化学で基礎疾患を除外。ウサギは絶対的経鼻呼吸動物であるため気管狭窄による呼吸障害は重篤度が高い。先天性（気管低形成）と後天性（挿管後瘢痕・膿瘍圧迫）を鑑別する。"
}

# 40. rabbit_portosystemic_shunt — Portosystemic Shunt / 門脈体循環シャント
ENRICHMENTS["rabbit_portosystemic_shunt"] = {
    "diagnosis_ja": "成長遅延・神経症状（けいれん・沈鬱・旋回）・食後の異常行動から門脈体循環シャントを疑う。生化学で食前・食後胆汁酸の著増・BUN低値・低アルブミン血症を確認。血中アンモニア上昇を確認。超音波で門脈系の異常血管（シャント血管）を検出。造影CT血管造影で確定し、シャントの形態（肝内型/肝外型）を分類。CBC/生化学で小赤血球症・低コレステロールを確認。尿検査で尿酸アンモニウム結晶を確認。ウサギの門脈シャントは稀だが報告があり、肝性脳症との鑑別が重要。"
}

# 41. rabbit_elodontoma — Elodontoma / エロドントーマ
ENRICHMENTS["rabbit_elodontoma"] = {
    "diagnosis_ja": "上顎前歯部の進行性腫脹・鼻閉・眼球突出から歯原性腫瘍（エロドントーマ）を疑う。頭部X線・CTで上顎骨内の無秩序な歯組織増殖・骨膨隆を確認。MRIで軟部組織浸潤を精査。組織生検で歯牙組織（エナメル質・象牙質・セメント質）の無秩序な増殖を確認し確定。CBC/生化学で基礎疾患を除外。ウサギの常生歯（open-rooted teeth）は持続的に成長するため、歯原性腫瘍が歯根から発生し上顎骨を破壊的に浸潤する。ロップ種・ドワーフ種で報告が多い。"
}

# 42. rabbit_encephalitozoonosis_-_neurological_form — Encephalitozoonosis - Neurological Form / エンセファリトゾーン症（神経型）
ENRICHMENTS["rabbit_encephalitozoonosis_-_neurological_form"] = {
    "diagnosis_ja": "斜頸・眼振・旋回運動・後肢不全麻痺・けいれんからE. cuniculi神経型を疑う。血清学的検査（IFA・ELISA）でIgM（急性期）・IgG抗体価を測定。ペア血清で4倍以上の抗体価上昇が有意。頭部MRIで脳幹・大脳の肉芽腫性病変を評価。尿PCRでE. cuniculiスポアを検出。CBC/生化学でBUN/Cre上昇（腎型合併）を確認。中耳炎（P. multocida）による末梢性前庭障害との鑑別が最重要であり、CTでの鼓室胞評価とE. cuniculi抗体検査の組み合わせで判断する。"
}

# 43. rabbit_heat_stroke_-_severe — Heat Stroke - Severe / 熱中症（重度）
ENRICHMENTS["rabbit_heat_stroke_-_severe"] = {
    "diagnosis_ja": "高温環境（>28°C）での虚脱・開口呼吸・流涎・けいれん・意識障害から重度熱中症を疑う。直腸温>41°Cで確認。CBC/生化学で脱水（PCV上昇）・電解質異常・肝酵素上昇・腎機能障害・CK上昇（横紋筋融解）を評価。血液ガスで代謝性アシドーシスを確認。凝固検査でDIC合併を評価。ウサギは汗腺を持たず耳介の血管拡張が主要な放熱機構であるため高温環境に極めて脆弱。28°C以上で熱中症リスクが急上昇する。致死率が高く緊急対応が必要。"
}

# 44. rabbit_lop_ear_canal_stenosis — Lop Ear Canal Stenosis / ロップ種耳道狭窄
ENRICHMENTS["rabbit_lop_ear_canal_stenosis"] = {
    "diagnosis_ja": "ロップ種ウサギの慢性耳漏・頭振り・耳掻き・悪臭から耳道狭窄を疑う。耳鏡検査で外耳道の狭窄・角化物蓄積を確認。頭部CT/X線で外耳道の骨性狭窄・鼓室胞の液体貯留/骨肥厚を評価。培養・感受性試験で二次感染菌を同定。CBC/生化学でヘテロフィル増多を確認。ロップ種は垂れ耳の解剖学的構造により外耳道の換気が不良で、耳道上皮の過角化→狭窄→二次感染の悪循環が発生する。鑑別に耳疥癬・中耳炎・耳ポリープを考慮する。"
}

# 45. rabbit_myxomatosis_-_amyxomatous_form — Myxomatosis - Amyxomatous Form / 粘液腫症（無粘液腫型）
ENRICHMENTS["rabbit_myxomatosis_-_amyxomatous_form"] = {
    "diagnosis_ja": "発熱・沈鬱・食欲不振・呼吸困難で典型的な粘液腫性腫脹を欠く症例から無粘液腫型粘液腫症を疑う。PCRでMyxoma virusを検出。皮膚生検で粘液腫ウイルス封入体を確認するが、無粘液腫型では皮下浮腫が軽微。CBC/生化学で白血球減少・肝酵素上昇を評価。呼吸器症状が主体の場合はX線で肺野陰影を確認。典型型と異なり眼瞼・外陰部の顕著な腫脹がないため臨床的に見落としやすい。蚊・ノミ媒介歴を聴取。鑑別にP. multocida感染・RHDを考慮する。"
}

# 46. rabbit_femoral_head_necrosis — Femoral Head Necrosis / 大腿骨頭壊死
ENRICHMENTS["rabbit_femoral_head_necrosis"] = {
    "diagnosis_ja": "後肢の跛行・股関節痛・運動嫌い・筋萎縮から大腿骨頭壊死を疑う。X線で大腿骨頭の扁平化・骨硬化・断裂・関節腔の不整を確認。CT/MRIで壊死範囲と軟骨下骨折を精査。CBC/生化学でCa・P・ALP（代謝性骨疾患）を評価。ステロイド使用歴を聴取。触診で股関節の可動域制限・疼痛を確認。ウサギでは外傷（落下・不適切な保定）や血管障害が原因として考慮される。鑑別に股関節形成不全・脊椎疾患・E. cuniculi関連後肢障害を考慮する。"
}

# 47. rabbit_myxomatosis_-_respiratory_form — Myxomatosis - Respiratory Form / 粘液腫症（呼吸器型）
ENRICHMENTS["rabbit_myxomatosis_-_respiratory_form"] = {
    "diagnosis_ja": "呼吸困難・鼻汁・結膜炎・沈鬱で典型的な皮下粘液腫を欠く症例から呼吸器型粘液腫症を疑う。PCRでMyxoma virusを検出し確定。X線で肺野のびまん性陰影・胸水を確認。気管洗浄液の細胞診で炎症所見を確認。CBC/生化学で白血球減少・肝酵素上昇を評価。蚊・ノミ媒介歴・野生ウサギとの接触歴を聴取。呼吸器型は典型型と異なり皮下腫脹が軽微で、P. multocida肺炎やRHDとの鑑別が困難。ウサギは経鼻呼吸動物のため呼吸器症状は重篤化しやすい。"
}

# 48. rabbit_aortic_calcification — Aortic Calcification / 大動脈石灰化
ENRICHMENTS["rabbit_aortic_calcification"] = {
    "diagnosis_ja": "高齢ウサギの偶発的X線所見（大動脈壁の線状石灰化）または突然死で大動脈石灰化を疑う。X線で大動脈走行に沿った石灰化を確認。超音波で大動脈壁の肥厚・高エコー像を評価。生化学でCa・P・Ca×P積・BUN/Cre を確認。心エコーで心機能への影響を評価。ウサギのCa代謝は腎排泄依存性が高く、高Ca食（アルファルファ偏重）と加齢性腎機能低下が動脈壁石灰化の主因。食餌歴の聴取が重要。鑑別に動脈硬化症・転移性石灰化を考慮する。"
}

# 49. rabbit_shope_fibroma_virus — Shope Fibroma Virus / ショープ線維腫ウイルス
ENRICHMENTS["rabbit_shope_fibroma_virus"] = {
    "diagnosis_ja": "皮下の孤立性〜多発性結節状腫瘤（通常四肢に好発）からShope線維腫ウイルスを疑う。組織生検でレポリポックスウイルスの特徴的な細胞質内封入体を含む線維芽細胞増殖を確認。PCRでShope Fibroma Virusを検出。電子顕微鏡でポックスウイルス粒子を確認。CBC/生化学は通常正常。蚊媒介感染であり季節性・屋外飼育歴を聴取。家兎では通常自然退縮するが免疫抑制個体で全身化しうる。鑑別に粘液腫症・膿瘍・基底細胞腫を考慮する。"
}

# 50. rabbit_shope_papilloma_virus — Shope Papilloma Virus / ショープパピローマウイルス
ENRICHMENTS["rabbit_shope_papilloma_virus"] = {
    "diagnosis_ja": "皮膚の角化性疣贅状腫瘤・皮角様病変からShope乳頭腫ウイルス（CRPV）を疑う。組織生検で扁平上皮の乳頭腫性増殖と核内封入体を確認。PCRでCRPV DNAを検出。病理組織検査で悪性転化（扁平上皮癌への移行）の有無を評価。免疫組織化学でウイルス抗原を検出。CBC/生化学は通常正常。CRPVは実験的発癌モデルとして有名であり、自然感染でも約25%が悪性転化する。ワタオウサギが自然宿主であり、家兎での感染は環境曝露による。"
}

# 51. rabbit_renal_agenesis — Renal Agenesis / 腎無形成
ENRICHMENTS["rabbit_renal_agenesis"] = {
    "diagnosis_ja": "片側性の場合は偶発的所見として発見されることが多い。超音波で一側腎の欠如と対側腎の代償性腫大を確認。X線・CTで腎シルエットの欠如を確認。生化学でBUN/Cre・SDMAを評価し残存腎の機能を確認。尿検査で蛋白尿・尿比重を確認。ウサギでは先天性発達異常として報告がある。両側性は生存不能。片側性では対側腎の代償性肥大により長期間無症状で経過し、腎機能の定期的モニタリングが推奨される。超音波が非侵襲的スクリーニングとして最も有用。"
}

# 52. rabbit_urinary_calculi_ureteral — Urinary Calculi (Ureteral) / 尿管結石
ENRICHMENTS["rabbit_urinary_calculi_ureteral"] = {
    "diagnosis_ja": "急性腰部疼痛・血尿・食欲不振・排尿困難から尿管結石を疑う。X線で尿管走行に沿った高密度結石影を確認（ウサギの結石は炭酸カルシウム主成分でX線で明瞭）。超音波で水腎症（腎盂拡張）・尿管拡張を確認。CT検査で結石の正確な位置・大きさ・水腎症の程度を精査。生化学でBUN/Cre上昇・Ca上昇を評価。尿検査で血尿・結晶を確認。ウサギのCa代謝は腎排泄依存性が高く、高Ca食と飲水不足が結石形成の主因。両側性閉塞は急性腎不全をきたす。"
}

# 53. rabbit_intestinal_torsion — Intestinal Torsion / 腸捻転
ENRICHMENTS["rabbit_intestinal_torsion"] = {
    "diagnosis_ja": "超急性の腹痛・腹部膨満・ショック症状（蒼白粘膜・頻脈・低体温）・急速な衰弱から腸捻転を疑う。X線で腸管の著明な拡張・ガス貯留・液体レベル形成を確認。超音波で腸管壁の浮腫・血流低下（ドプラー）を評価。CBC/生化学で代謝性アシドーシス・乳酸上昇・電解質異常を確認。緊急外科的介入が必要な場合が多い。ウサギでは盲腸捻転が最も多く報告されており、GI stasis・食餌変更・盲腸拡張が素因。致死率が高く迅速な診断と外科的介入が予後を決定する。"
}

# 54. rabbit_floppy_rabbit_syndrome — Floppy Rabbit Syndrome / フロッピーラビット症候群
ENRICHMENTS["rabbit_floppy_rabbit_syndrome"] = {
    "diagnosis_ja": "急性発症の全身性筋弛緩・脱力（頭部を含む）で意識は保たれている状態からフロッピーラビット症候群を疑う。神経学的検査で意識清明だが全身の筋緊張低下を確認。CBC/生化学でK・Ca・Mg・血糖を測定し電解質・代謝異常を評価。X線で脊椎骨折を除外。E. cuniculi抗体検査を実施。血液ガスで代謝性アシドーシスを評価。CK測定で筋障害を確認。原因不明の場合が多い特発性疾患であり除外診断で確定。低K血症・脱水・ストレスが素因として報告されている。多くは支持療法で数日以内に回復。"
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
