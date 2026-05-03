#!/usr/bin/env python3
"""Cat description_ja expansion — batch 3."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["cat_feline_heat_stroke"] = {
    "description_ja": "猫は汗腺が乏しく体温調節能が低いため熱中症に脆弱である。閉め切った車内・室内の高温環境曝露が主因で、体温41°C超で多臓器不全・DICに進展する。短頭種（ペルシャ・ヒマラヤン）、肥満猫、心肺疾患既往が高リスク。初期徴候はパンティング・流涎・頻脈で、進行すると虚脱・痙攣・血便を呈する。直腸温39.5°C到達で冷却中止が鍵。"
}

ENRICHMENTS["cat_feline_hepatic_amyloidosis"] = {
    "description_ja": "肝臓への反応性AA型アミロイド沈着により肝構造が破壊され、突然の肝破裂と血腹を引き起こす致死的疾患。シャムとアビシニアンに強い品種素因があり、家族性アミロイドーシスとして遺伝する。中高齢で発症し、臨床徴候なく急死することも多い。肝腫大・腹水・黄疸がみられ、コンゴーレッド染色で確定診断する。予後不良で根治療法はない。"
}

ENRICHMENTS["cat_feline_hepatocutaneous_syndrome"] = {
    "description_ja": "重度の肝疾患（肝硬変・肝空胞変性）または膵グルカゴノーマに続発する壊死性遊走性紅斑の猫版。アミノ酸・亜鉛の代謝異常により表皮壊死が生じ、足蹠パッドの著明な角化亢進・亀裂・痂皮が特徴的。顔面・耳・鼠径部にも病変が及ぶ。超音波で「ハニカムパターン」の肝実質像を認める。高アミノ酸輸液と卵黄レシチン補充が緩和的に有効。"
}

ENRICHMENTS["cat_feline_hepatozoonosis"] = {
    "description_ja": "Hepatozoon felisの感染ダニ経口摂取で感染するアピコンプレックス原虫症。猫では犬より稀で、筋炎・発熱・体重減少を呈するが無症候キャリアも多い。免疫抑制状態（FIV/FeLV併発）で臨床症状が顕在化する。血液塗抹でシゾント/ガモントを検出、筋生検で確定診断。特異的治療薬は確立されておらず、抗コクシジウム薬とNSAIDsの併用が試みられる。"
}

ENRICHMENTS["cat_feline_hereditary_myopathy_devon_rex"] = {
    "description_ja": "デボンレックスとスフィンクスに発症する常染色体劣性遺伝のジストロフィン関連筋障害。生後3-6ヶ月齢で全身性の筋力低下が顕在化し、巨大食道・頸部腹屈・運動不耐性を呈する。ジストロフィン複合体の欠損が病因で、血清CK著明上昇を認める。進行性だが生命予後は比較的保たれる個体もある。根治療法はなく、高カロリー立位給餌と誤嚥性肺炎の予防が管理の要。"
}

ENRICHMENTS["cat_feline_herpesvirus_fhv-1_infection"] = {
    "description_ja": "猫ヘルペスウイルス1型（FHV-1）は猫上部呼吸器感染症の最多原因で、三叉神経節に終生潜伏する。初感染は子猫で重症化しやすく、発熱・くしゃみ・漿液膿性鼻汁・結膜炎・角膜樹枝状潰瘍を呈する。ストレスで再活性化し間欠的排菌する。多頭飼育・シェルターで蔓延。ファムシクロビル90mg/kg BIDが有効で、L-リジン補充の効果は議論がある。"
}

ENRICHMENTS["cat_feline_high-rise_syndrome_thoracic_trauma"] = {
    "description_ja": "2階以上からの落下による多発外傷症候群。猫は空中で正位反射をとるが、落下高度7階以上で終末速度に達し衝撃が一定化する。胸部外傷として気胸（45%）・肺挫傷・横隔膜破裂が多く、顔面外傷（硬口蓋裂）と四肢骨折を高率に併発する。ショックと呼吸不全への迅速な安定化が優先。5-7階の「危険帯」では死亡率が高いとされる。"
}

ENRICHMENTS["cat_feline_horner_syndrome"] = {
    "description_ja": "眼への交感神経支配の障害により縮瞳・眼瞼下垂・眼球陥没・第三眼瞼突出の4徴を呈する症候群。猫では中耳炎・鼻咽頭ポリープが主因で、特発性も約25%を占める。一次（中枢）・二次（頸部）・三次（節後）ニューロンのいずれの障害でも発症する。フェニレフリン点眼による薬理学的局在診断が有用。基礎疾患の治療で多くは回復するが特発性は数週-数ヶ月で自然寛解する。"
}

ENRICHMENTS["cat_feline_hyperkalemia"] = {
    "description_ja": "血清カリウム6.5mEq/L超で心伝導障害を引き起こす生命を脅かす電解質異常。猫では尿道閉塞・急性腎不全・副腎皮質機能低下症が主因。心電図でT波尖鋭化・QRS幅延長・洞停止が進行性に出現する。緊急治療はグルコン酸Ca静注（心筋保護）+インスリン・デキストロース（細胞内シフト）。原疾患の解除（尿路閉塞の導尿等）が根本的治療となる。"
}

ENRICHMENTS["cat_feline_hyperparathyroidism_primary"] = {
    "description_ja": "副甲状腺の腺腫または過形成によるPTH自律的過剰分泌で持続性高Ca血症を呈する内分泌疾患。猫では稀だが高齢猫で報告が増加。多飲多尿・食欲不振・便秘・筋力低下が主徴候。腎石灰化とCKDへの進行リスクがある。イオン化Ca上昇+PTH不適切高値で診断。超音波ガイド下エタノール注入または外科的副甲状腺摘出が治療選択肢。術後の低Ca血症管理が重要。"
}

ENRICHMENTS["cat_feline_hyperphosphatemia"] = {
    "description_ja": "血清リン濃度の異常上昇で、猫ではCKDのステージ進行に伴い高頻度に認められる。リン貯留はFGF23・PTH上昇を介して腎性二次性副甲状腺機能亢進症と軟部組織石灰化を促進し、CKD進行の独立危険因子である。IRIS分類に基づくリン制限食が第一選択で、食事療法不十分ならリン吸着剤（水酸化Al・炭酸La・キトサン）を追加する。目標は血清P<4.5mg/dL。"
}

ENRICHMENTS["cat_feline_hyperthyroid_cardiomyopathy"] = {
    "description_ja": "慢性甲状腺機能亢進症に続発する心筋リモデリングで、T4過剰による血行動態負荷と直接的心筋毒性が機序。左室求心性肥厚・左房拡大・頻脈性不整脈を呈し、HCMとの鑑別が重要。約70%の甲状腺機能亢進猫に心エコー異常を認める。甲状腺機能の正常化（メチマゾール・I-131）により数ヶ月で心肥大は可逆的に改善するが、潜在性原発性HCMが露呈する場合もある。"
}

ENRICHMENTS["cat_feline_hypertrophic_cardiomyopathy_obstructive"] = {
    "description_ja": "肥大型心筋症のうち、心室中隔の非対称性肥厚により動的左室流出路閉塞（LVOTO）を伴う病型。僧帽弁収縮期前方運動（SAM）で流出路圧較差≥30mmHgを生じ、失神・運動不耐性・急死リスクが高い。メインクーン・ラグドールに好発。β遮断薬（アテノロール）が第一選択で心拍数低下と流出路閉塞軽減を図る。利尿薬・血管拡張薬は閉塞悪化リスクがあり慎重投与。"
}

ENRICHMENTS["cat_feline_hypervitaminosis_a_chronic"] = {
    "description_ja": "レバー食の長期過剰摂取による脂溶性ビタミンA蓄積で骨増殖症を引き起こす。頸椎・胸椎の骨棘形成と関節強直が特徴的で、頸部硬直・毛繕い不能・前肢跛行を呈する。中高齢の室内猫に多い。骨変化は不可逆だが、食事是正で進行を停止できる。X線で椎体間の骨架橋形成を確認。NSAIDs疼痛管理とビタミンA制限食（レバー中止）が基本治療。"
}

ENRICHMENTS["cat_feline_hyponatremia"] = {
    "description_ja": "血清Na<135mEq/Lの電解質異常で、猫では慢性腎臓病・心不全・副腎不全・過剰輸液が主因。急性低Na血症は脳浮腫により嗜眠・痙攣・昏睡を引き起こす。慢性例は非特異的消化器症状のみのことが多い。補正速度は8-10mEq/L/24h以下とし、急速補正による浸透圧性脱髄症候群を回避する。基礎疾患の治療と等張液による段階的補正が原則。"
}

ENRICHMENTS["cat_feline_hypoparathyroidism"] = {
    "description_ja": "PTH分泌不全による低Ca血症で、猫では甲状腺摘出術後の医原性が最多。特発性（免疫介在性副甲状腺破壊）もある。イオン化Ca低下により筋痙攣・テタニー・痙攣・顔面こすり行動が出現する。急性低Ca血症はグルコン酸Ca緩徐静注で管理。長期はカルシトリオール0.02-0.03μg/kg/日+経口Ca補充で血清Ca 8-9.5mg/dLを目標に維持する。"
}

ENRICHMENTS["cat_feline_idiopathic_chylothorax"] = {
    "description_ja": "明確な基礎原因なく胸腔内にリンパ液（乳び）が貯留する疾患で、猫では犬より発生率が高い。シャム猫とヒマラヤンに品種素因。胸管の機能的閉塞または胸管圧上昇が推定機序。呼吸困難・運動不耐性で発見され、胸水はトリグリセリド高値の白色混濁液。内科試行（ルチン30mg/kg BID・低脂肪MCT食・オクトレオチド）4-8週で改善なければ胸管結紮+心膜切除の外科的介入。"
}

ENRICHMENTS["cat_feline_idiopathic_megacolon"] = {
    "description_ja": "結腸平滑筋の進行性機能障害により巨大結腸と難治性便秘/宿便を呈する猫特有の疾患。中高齢の雄猫に好発し、結腸筋層のカハール介在細胞減少が病因として示唆される。X線で著明に拡張した糞便充満結腸を認める。初期はラクツロース・シサプリド(2.5-5mg TID)で管理可能だが、不応例は亜全結腸切除術が根治的。術後の軟便は数週で正常化する。"
}

ENRICHMENTS["cat_feline_infectious_peritonitis_fip_-_wet_form"] = {
    "description_ja": "猫腸コロナウイルス（FECV）の体内変異により発症するFIPの滲出型。若齢猫（<2歳）と純血種に多く、マクロファージ内でのウイルス複製と免疫複合体沈着により漿膜炎と血管炎を生じる。腹水・胸水（高蛋白・低細胞の黄色粘稠液）が特徴的。リバルタ試験陽性とα1-AGP上昇が診断補助。GS-441524(4-8mg/kg SC×84日)が革命的治療薬として確立されつつある。"
}

ENRICHMENTS["cat_feline_interstitial_nephritis"] = {
    "description_ja": "腎間質のリンパ球・形質細胞浸潤と線維化を特徴とする慢性炎症で、猫CKDの最も一般的な組織学的所見。高齢猫に好発し病因は多因子（虚血・免疫・加齢性変化）。初期は無症状で進行性に多飲多尿・体重減少・食欲低下が出現する。IRIS分類に基づくステージ管理で、腎臓食・リン制限・ACEi・エリスロポエチンを組み合わせた支持療法が標準。"
}

ENRICHMENTS["cat_feline_intussusception"] = {
    "description_ja": "腸管の一部が隣接腸管内に陥入し閉塞と虚血壊死を引き起こす外科的緊急疾患。猫では若齢で腸炎・寄生虫感染・線状異物に続発することが多い。回盲部（回腸-結腸）が最好発部位。嘔吐・血便・腹部腫瘤触知が三徴で、腹部超音波で「ターゲットサイン」を確認する。手動整復は再発率高く、壊死腸管を含む切除吻合術が標準治療。"
}

ENRICHMENTS["cat_feline_iris_melanosis"] = {
    "description_ja": "虹彩表面のメラノサイト増殖による扁平色素斑で、中高齢の猫に多い。単発~多発性の褐色~黒色斑として発見され、虹彩表面は平坦で構造変化を伴わない良性病変が大部分。しかしびまん性虹彩メラノーマへの悪性転化リスクがあり、虹彩肥厚・色素分散・眼圧上昇は悪性化の徴候。6-12ヶ月毎の眼科写真記録による経時変化モニタリングが推奨される。"
}

ENRICHMENTS["cat_feline_ischemic_encephalopathy"] = {
    "description_ja": "脳血管の血栓塞栓による突発性脳梗塞で、猫ではクテレブラ幼虫の頭蓋内迷入が特異的原因として知られる。中大脳動脈領域の梗塞が多く、急性の片側性神経徴候（旋回・半側無視・対側不全麻痺）を呈する。MRIで梗塞領域を同定。基礎疾患として心筋症（血栓源）・甲状腺機能亢進症・高血圧を精査する。急性期は支持療法が中心で、多くは数週で部分回復する。"
}

ENRICHMENTS["cat_feline_ischemic_myelopathy_fibrocartilaginous_embolism"] = {
    "description_ja": "椎間板の線維軟骨性物質が脊髄血管に塞栓し急性脊髄梗塞を引き起こす疾患。猫では犬より稀だが報告がある。超急性発症の非対称性脊髄障害で、運動直後に突然の麻痺が出現し以後進行しない点が特徴。疼痛を伴わないことが多い。MRI T2WIで髄内高信号を認め、椎間板ヘルニアとの鑑別が重要。治療は支持療法とリハビリで、数週-数ヶ月で機能回復が期待できる。"
}

ENRICHMENTS["cat_feline_laryngitis"] = {
    "description_ja": "喉頭粘膜の炎症で声の変化（嗄声・失声）・咳・嚥下困難を引き起こす。猫ではFHV-1/FCV等のURI続発が最多で、吸入刺激物・外傷・腫瘍も原因となる。慢性例ではポリープ形成や喉頭浮腫による上気道閉塞のリスクがある。喉頭鏡検査で粘膜発赤・腫脹・潰瘍を確認。感染性にはアモキシシリン/クラブラン酸、炎症性には短期プレドニゾロンとネブライザーが有効。"
}

ENRICHMENTS["cat_feline_leishmaniasis"] = {
    "description_ja": "サシチョウバエ媒介のLeishmania infantum感染で、地中海沿岸・南米の流行地域で猫にも発症する。皮膚型（結節・潰瘍・脱毛）が最多で、内臓型（肝脾腫・リンパ節腫・腎障害）は免疫抑制猫で発現する。FIV共感染が重症化リスク。骨髄/リンパ節穿刺の細胞診・PCRで確定診断。アロプリノール10mg/kg BIDが第一選択で、メグルミンアンチモンは猫での安全性データが限定的。"
}

ENRICHMENTS["cat_feline_linear_foreign_body"] = {
    "description_ja": "糸・紐・リボン等の線状物を誤食し、一端が舌根部や幽門に固定されて腸管に襞（アコーディオン状変形）を形成する。猫は遊びで紐状物を飲み込みやすく特に若齢猫で多発。腸間膜側で穿孔し腹膜炎に至るリスクが高い。嘔吐・食欲廃絶・腹痛が主徴で、舌下の紐確認が診断の手がかり。内視鏡的除去または開腹複数箇所切開（enterotomy）が必要。"
}

ENRICHMENTS["cat_feline_liver_fluke_infection_opisthorchis"] = {
    "description_ja": "Opisthorchis/Platynosomum属の肝吸虫が胆管系に寄生し慢性胆管炎・胆管肥厚・肝線維化を引き起こす。中間宿主（淡水魚/トカゲ）の生食で感染し、熱帯・亜熱帯地域の屋外猫に多い。軽症は無症候だが大量寄生で黄疸・嘔吐・体重減少を呈する。糞便沈殿法で虫卵検出。プラジカンテル20mg/kg×3日が有効で、重度胆管閉塞には外科的介入が必要な場合がある。"
}

ENRICHMENTS["cat_feline_lymphocytic_cholangitis"] = {
    "description_ja": "猫特有の慢性進行性胆管炎で、門脈域へのリンパ球・形質細胞浸潤を特徴とする。好中球性胆管炎からの移行や免疫介在性機序が想定される。中高齢猫に多く、慢性の食欲低下・体重減少・間欠的黄疸・肝腫大を呈する。炎症性腸疾患・膵炎との三臓器炎（triaditis）併発が約50%。肝生検で確定診断。ウルソデオキシコール酸+プレドニゾロンの長期投与が標準治療。"
}

ENRICHMENTS["cat_feline_malassezia_dermatitis"] = {
    "description_ja": "皮膚常在酵母Malassezia pachydermatisの過増殖による脂漏性掻痒性皮膚炎。猫ではアレルギー性皮膚炎・内分泌疾患・FIV感染等の基礎疾患に続発する。顎・耳・爪床・腹側に好発し、褐色蝋様分泌物と脂臭を特徴とする。デボンレックス・スフィンクスに品種素因。細胞診で酵母確認。イトラコナゾール5mg/kg/日×21-30日またはミコナゾール外用で管理する。"
}

ENRICHMENTS["cat_feline_mammary_carcinoma_triple_negative"] = {
    "description_ja": "エストロゲン受容体・プロゲステロン受容体・HER2全て陰性の高悪性度乳腺癌。猫乳腺腫瘍の85-90%は悪性で、トリプルネガティブ型はホルモン療法無効のため予後が特に不良。シャム猫に品種素因。肺・リンパ節転移が早期から生じる。根治的乳腺切除（片側or両側全摘）+ドキソルビシン化学療法が標準だが、生存期間中央値は6-12ヶ月。早期避妊で発症リスクは91%低減する。"
}

ENRICHMENTS["cat_feline_mediastinal_cyst"] = {
    "description_ja": "前縦隔内に発生する液体充満嚢胞で、猫では胸腺嚢胞と気管支原性嚢胞が多い。若齢~中齢猫に発見され、小型では無症候だが増大により気管圧迫・呼吸困難・嚥下障害を呈する。胸部X線で前縦隔腫瘤影、超音波で嚢胞性構造を確認する。胸腺腫・リンパ腫との鑑別が重要。穿刺排液は一時的で再貯留するため、外科的切除が根治的治療。予後は良好。"
}

ENRICHMENTS["cat_feline_metabolic_epidermal_necrosis_superficial_necrolytic_dermatitis"] = {
    "description_ja": "肝疾患・膵グルカゴノーマに伴う低アミノ酸血症により表皮壊死を生じる稀な代謝性皮膚疾患。足蹠パッドの著明な潰瘍・角化亢進・痂皮が病的で、口唇・耳介・会陰部にも及ぶ。犬の肝皮症候群に相当し猫では極めて稀。超音波で肝臓の特徴的ハニカム像を認める。高用量アミノ酸輸液・卵黄・亜鉛補充で皮膚病変は改善しうるが基礎肝疾患の予後が規定因子となる。"
}

ENRICHMENTS["cat_feline_myiasis_fly_strike"] = {
    "description_ja": "ハエ（主にニクバエ・クロバエ）が開放創・汚染被毛に産卵し、孵化した蛆虫（幼虫）が生体組織を侵食する外部寄生虫症。外飼い猫、高齢・衰弱・失禁で会陰部汚染のある猫に好発する。夏季に多く、臭気を伴う壊死創と大量の蛆を認める。治療は全身麻酔下での蛆除去・壊死組織デブリードマン・洗浄、全身性抗菌薬投与。広範例はショックと敗血症で致死的。"
}

ENRICHMENTS["cat_feline_myocarditis"] = {
    "description_ja": "心筋の炎症性疾患で、猫ではパルボウイルス（FPV）・トキソプラズマ・バルトネラが主要病因。急性では突然死や不整脈（心室期外収縮・房室ブロック）として発症し、慢性化すると拡張型心筋症様の心不全に移行する。心筋トロポニンI著明上昇が診断の手がかり。心内膜心筋生検が確定診断だが侵襲的。基礎感染の治療+抗不整脈薬+心不全管理の複合的アプローチが必要。"
}

ENRICHMENTS["cat_feline_nasopharyngeal_cryptococcosis"] = {
    "description_ja": "Cryptococcus neoformans/gattiiの吸入感染で鼻腔・鼻咽頭に肉芽腫性病変を形成する。猫のクリプトコッカス症で最多の臨床型（約70%）。鼻梁上の硬い皮下腫脹（「ローマの鼻」）・慢性くしゃみ・漿液血性鼻汁が特徴的。ラテックス凝集法（LCAT）による抗原価測定で迅速診断可能。フルコナゾール50mg/cat BID×数ヶ月が第一選択で、抗原価陰転まで継続する。"
}

ENRICHMENTS["cat_feline_neonatal_isoerythrolysis_type_b_queen_x_type_a_kitten"] = {
    "description_ja": "B型母猫の初乳中に含まれる強力な抗A抗体がA型新生子猫の赤血球を溶血させる新生児疾患。ブリティッシュショートヘア・デボンレックス・コーニッシュレックス等B型頻度の高い品種で問題となる。出生後24-72時間で黄疸・血色素尿・尾尖壊死・急死を呈する。予防は繁殖前の血液型判定で、B型母×A型父の組み合わせでは生後16-24時間の哺乳回避が必須。"
}

ENRICHMENTS["cat_feline_nephrogenic_diabetes_insipidus"] = {
    "description_ja": "腎集合管がADH（バソプレシン）に反応できず尿濃縮障害を生じる疾患。猫では先天性は極めて稀で、CKD・高Ca血症・低K血症・リチウム投与等に続発する後天性が大部分。著明な多尿多飲（尿比重<1.008）を呈し脱水リスクが高い。水制限試験とデスモプレシン反応試験で中枢性尿崩症と鑑別する。治療は基礎疾患の是正と自由飲水の確保が基本。"
}

ENRICHMENTS["cat_feline_noise_phobia"] = {
    "description_ja": "雷・花火・工事音等の突発的大音量に対する病的恐怖反応で、パニック・隠蔽・排泄失禁・破壊行動を呈する不安障害。猫は犬より騒音恐怖が潜在化しやすく、フリーズ反応や長時間の隠蔽で見過ごされることが多い。慢性化するとストレス関連FIC・過剰グルーミングを併発する。安全な隠れ場所の確保が第一で、重症例にはガバペンチン50-100mg/cat頓用やトラゾドンが有効。"
}

ENRICHMENTS["cat_feline_orofacial_pain_syndrome"] = {
    "description_ja": "三叉神経の神経障害性疼痛により口腔・顔面の激しい不快感と自傷行為（顔・口の引っ掻き）を呈する猫特有の疾患。バーミーズに強い品種素因があり遺伝的背景が示唆される。歯の萌出・口腔疾患がトリガーとなることが多い。発作的に口をかきむしり出血性潰瘍を自ら形成する。ガバペンチン5-10mg/kg BID・カルバマゼピンが第一選択で、エリザベスカラーで自傷を防止する。"
}

ENRICHMENTS["cat_feline_paraneoplastic_alopecia"] = {
    "description_ja": "膵臓癌（膵管腺癌）または胆管癌に伴う稀な傍腫瘍症候群で、腹側を中心とした急速進行性の対称性脱毛と皮膚の光沢化を呈する。脱毛部位は無痛で容易に抜毛でき、足蹠パッドの剥離も認める。診断時に腫瘍は既に進行していることが多く、超音波で膵腫瘤を確認する。外科的腫瘍切除以外に有効な治療はなく、予後は極めて不良で診断後数週-数ヶ月で死亡する。"
}

ENRICHMENTS["cat_feline_pituitary_dwarfism"] = {
    "description_ja": "下垂体前葉の発育不全または嚢胞形成によるGH欠乏で均整のとれた矮小症を呈する。猫では極めて稀で、4-5ヶ月齢で成長停止・乳歯残存・被毛発育不良（軟毛のみ）・精神発達遅延が顕在化する。TSH・ACTH・ゴナドトロピンの複合欠乏を伴うことが多い。MRIで下垂体低形成/嚢胞を確認。GH補充療法は入手困難で対症的管理が主体となる。"
}

ENRICHMENTS["cat_feline_pneumonia"] = {
    "description_ja": "肺実質の感染性炎症で、猫では細菌性（誤嚥性が最多）・ウイルス性（FCV・FHV-1）・真菌性・寄生虫性に分類される。発熱・湿性咳・頻呼吸・鼻汁が主徴候で、聴診で捻髪音を聴取する。X線で肺胞パターンの浸潤影を確認。猫は呼吸困難に対しストレスに極弱く、低ストレスでの酸素供給が重要。気管洗浄液の培養感受性に基づく抗菌薬選択が標準で、嫌気性菌カバーも考慮する。"
}

ENRICHMENTS["cat_feline_polycystic_liver_disease"] = {
    "description_ja": "肝実質内に多発性嚢胞を形成する遺伝性疾患で、ペルシャ猫とその関連種に好発するPKD1遺伝子変異（常染色体優性）に伴い多嚢胞腎と高率に併発する。嚢胞は加齢に伴い増大し、肝腫大・腹部膨満・食欲低下を引き起こすが、多くの猫は長期間無症候。巨大嚢胞による圧迫症状には超音波ガイド下穿刺排液が有効。根治療法はなく経過観察が基本。"
}

ENRICHMENTS["cat_feline_proliferative_and_necrotizing_otitis_externa"] = {
    "description_ja": "子猫・若齢猫に好発する稀な両側性の増殖性外耳炎で、耳垢腺上皮の過形成と表在性壊死を特徴とする。外耳道内に暗褐色の壊死性痂皮と乳頭状増殖が充満し、強い臭気を伴う。細菌・真菌培養は陰性で、免疫介在性機序が推定される。成長とともに自然寛解する傾向がある。タクロリムス外用やシクロスポリンが有効との報告があるが、標準治療は確立されていない。"
}

ENRICHMENTS["cat_feline_pure_red_cell_aplasia"] = {
    "description_ja": "赤芽球前駆細胞に対する免疫介在性破壊により骨髄での赤血球産生が選択的に停止する重度の非再生性貧血。網状赤血球絶対数<10,000/μLと骨髄中の赤芽球系細胞消失が特徴的。FeLV感染・エリスロポエチン抗体（rHuEPO投与後）が既知の原因で、特発性も多い。プレドニゾロン2mg/kg+シクロスポリン5-7mg/kgの免疫抑制が第一選択。輸血支持しつつ骨髄回復を待つ。"
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
