#!/usr/bin/env python3
"""Enrich diagnosis_ja for Exotic Other entries with short/missing text."""
import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# === Porcine (Mini Pig) diseases ===

ENRICHMENTS["exotic_other_porcine_parvovirus_ppv"] = {
    "diagnosis_ja": "血清学的検査（ELISA・HI法）でPPV抗体価を測定（ペア血清で4倍以上の上昇が確定的）。PCR（血液・胎児組織）でウイルスDNAを検出。繁殖障害（死産・ミイラ化胎児・小産子数）が主要臨床徴候。死産胎児・胎盤の病理組織学的検査で特徴的な封入体を確認。CBC・血液生化学で全身状態を評価。ワクチン接種歴の確認が重要。TORCH症候群の他の病原体（レプトスピラ・豚繁殖呼吸障害症候群ウイルス等）との鑑別が必要。"
}

ENRICHMENTS["exotic_other_porcine_circovirus_disease_pcv2"] = {
    "diagnosis_ja": "PCR（血清・リンパ節・組織）でPCV2ウイルスDNAを検出・定量。血清学的検査（ELISA）で抗PCV2抗体価を測定。病理組織検査でリンパ節のリンパ球枯渇・肉芽腫性炎症・細胞質内封入体を確認。CBC（リンパ球減少）で免疫抑制状態を評価。PMWS（離乳後多臓器消耗症候群）として発育不良・被毛粗剛・下痢・呼吸困難・黄疸が臨床徴候。免疫組織化学染色（IHC）でPCV2抗原のリンパ組織内分布を確認。ワクチン接種歴の確認。"
}

ENRICHMENTS["exotic_other_porcine_rotavirus"] = {
    "diagnosis_ja": "糞便検査でロタウイルス抗原を検出（ELISA・ラテックス凝集法・免疫クロマトグラフィー）。電子顕微鏡で特徴的な車輪状ウイルス粒子を確認。RT-PCRでウイルスRNAを同定・遺伝子型分類。幼若子豚の急性水様性下痢が主要臨床徴候。CBC・血液生化学（電解質異常・代謝性アシドーシス・BUN上昇）で脱水・全身状態を評価。糞便培養で細菌性腸炎の併発を除外。TGE・PEDとの鑑別が重要。"
}

ENRICHMENTS["exotic_other_transmissible_gastroenteritis_tge"] = {
    "diagnosis_ja": "RT-PCR（糞便・腸管組織）でTGEウイルスRNAを検出。蛍光抗体法（FA）で腸管凍結切片のウイルス抗原を確認。ELISA（糞便抗原・血清抗体）で補助診断。幼若子豚の急性水様性下痢・嘔吐・高死亡率が特徴的臨床徴候。CBC・血液生化学（重度脱水・電解質異常・代謝性アシドーシス）で全身状態を評価。病理組織検査で空腸・回腸の絨毛萎縮・融合を確認。PED・ロタウイルスとの鑑別にPCRパネルが有用。"
}

ENRICHMENTS["exotic_other_porcine_epidemic_diarrhea_ped"] = {
    "diagnosis_ja": "RT-PCR（糞便・腸管組織）でPEDウイルスRNAを検出。蛍光抗体法で腸管組織のウイルス抗原を確認。ELISA（血清IgG/IgA）で抗体応答を評価。全日齢の豚に感染するが、新生子豚で致死率が最も高い（水様性下痢・嘔吐・脱水）。CBC・血液生化学で脱水・電解質異常を評価。病理組織検査で小腸絨毛の著明な萎縮・短縮を確認。TGE・ロタウイルスとの臨床的鑑別は困難であり、PCR複合パネルによる確定診断が必須。"
}

ENRICHMENTS["exotic_other_clostridial_enteritis"] = {
    "diagnosis_ja": "糞便培養でClostridium perfringens等のClostridium属菌を同定。毒素検出（ELISA・PCR）でα・β・ε・ι毒素型を分類。糞便のグラム染色で大型グラム陽性桿菌を確認。CBC（白血球増多または減少・左方移動）で敗血症の重症度を評価。血液生化学（乳酸上昇・電解質異常・代謝性アシドーシス）でショック状態を確認。血性下痢・急性腹痛・突然死が臨床徴候。病理組織検査で壊死性腸炎を確認。ワクチン接種歴と食餌変更歴の聴取が重要。"
}

ENRICHMENTS["exotic_other_swine_dysentery_brachyspira"] = {
    "diagnosis_ja": "糞便培養（嫌気条件）でBrachyspira hyodysenteriae（豚赤痢菌）を分離・同定。PCRで菌種特異的遺伝子を検出。糞便の暗視野顕微鏡検査で大型スピロヘータを確認。粘液血性下痢が特徴的臨床徴候。CBC（白血球増多）・血液生化学（電解質異常・低アルブミン血症）で全身状態を評価。病理組織検査で大腸粘膜の表在性壊死・粘液分泌亢進を確認。B. pilosicoliとの鑑別が重要。感染源の疫学調査と飼育衛生管理の評価が必要。"
}

ENRICHMENTS["exotic_other_actinobacillosis_porcine"] = {
    "diagnosis_ja": "気管洗浄液・肺組織からの細菌培養でActinobacillus pleuropneumoniaeを分離・同定。PCRで血清型を決定。胸部X線で壊死性出血性肺炎パターン・胸水を確認。CBC（白血球増多・左方移動）で急性細菌感染を評価。血液生化学（乳酸上昇・CRP上昇）でショック・全身炎症を確認。急性型では突然死・呼吸困難・発熱・血性泡沫状鼻汁が臨床徴候。病理組織検査で壊死性線維素性胸膜肺炎を確認。血清学（ApxⅣ-ELISA）で抗体価を測定。"
}

ENRICHMENTS["exotic_other_pasteurellosis_porcine"] = {
    "diagnosis_ja": "気管洗浄液・鼻腔スワブからの細菌培養でPasteurella multocidaを分離・同定。PCR・莢膜型別で菌株を分類。胸部X線で気管支肺炎パターンを確認。CBC（白血球増多・左方移動）で細菌感染の重症度を評価。血液生化学で全身状態を確認。鼻汁・咳嗽・呼吸困難・発熱が主要臨床徴候。重度例ではA型莢膜株による進行性萎縮性鼻炎（PAR）を鑑別するため、鼻甲介のX線/CT評価が重要。他の呼吸器病原体との混合感染を考慮する。"
}

ENRICHMENTS["exotic_other_mycoplasma_pneumonia_porcine"] = {
    "diagnosis_ja": "気管洗浄液のPCRでMycoplasma hyopneumoniaeを検出（培養は極めて困難で数週間を要する）。胸部X線で肺前腹葉の限局性硬化像を評価。血清学的検査（ELISA）で抗体価を測定（ペア血清が推奨）。乾性咳嗽・発育遅延が特徴的臨床徴候で、急性死亡は稀。CBC・血液生化学で全身状態を確認。病理組織検査で気管支周囲リンパ球集簇・カタル性気管支肺炎を確認。二次感染菌（P. multocida, A. pleuropneumoniae）の混合感染評価が重要。"
}

ENRICHMENTS["exotic_other_streptococcal_meningitis_porcine"] = {
    "diagnosis_ja": "CSF分析で好中球性細胞増多・蛋白上昇を確認。CSF・血液培養でStreptococcus suisを分離・同定。PCRで菌種確認と血清型決定。神経症状（運動失調・旋回運動・角弓反張・痙攣・振戦）と高熱が主要臨床徴候。CBC（白血球増多・左方移動）で急性細菌感染を評価。血液生化学（乳酸上昇・CRP上昇）でショック・全身炎症を確認。人獣共通感染症であり、養豚従事者への感染リスクがあるため防護措置を講じる。ワクチン接種歴を確認。"
}

ENRICHMENTS["exotic_other_glasser's_disease_haemophilus_parasuis"] = {
    "diagnosis_ja": "体腔液（胸水・腹水・心嚢液・関節液）の細菌培養でGlaesserella（Haemophilus）parasuisを分離。PCRで血清型を決定。漿膜炎（多発性漿膜炎）が特徴的で、線維素性胸膜炎・腹膜炎・心嚢炎・関節炎を呈する。CBC（白血球増多・左方移動）・血液生化学（フィブリノーゲン上昇・CRP上昇）で全身炎症を評価。発熱・跛行・呼吸困難・CNS症状が臨床徴候。離乳後の移動ストレスが発症誘因となることが多い。"
}

ENRICHMENTS["exotic_other_porcine_dermatitis___nephropathy_syndrome_pdns"] = {
    "diagnosis_ja": "皮膚生検で壊死性血管炎（全身性壊死性血管炎）を確認。腎生検で線維素壊死性糸球体腎炎を確認。PCV2のPCR/IHCで関連を評価（PDNSはPCV2関連疾患群の一つ）。特徴的な暗赤色〜紫色の皮膚丘疹（特に後肢・会陰部）が臨床的に診断的。CBC・血液生化学（BUN・クレアチニン上昇・低アルブミン血症）で腎機能障害を評価。尿検査で蛋白尿・血尿を確認。免疫複合体の沈着がIII型過敏反応として病態に関与する。"
}

ENRICHMENTS["exotic_other_greasy_pig_disease_exudative_epidermitis"] = {
    "diagnosis_ja": "皮膚病変の視診で油性・灰褐色の痂皮形成・全身性滲出性皮膚炎を確認。皮膚スワブの細菌培養でStaphylococcus hyicusを分離・同定。細胞診で好中球・細菌を確認。新生〜離乳子豚に好発し、全身の皮膚が「脂ぎった」外観を呈する。CBC・血液生化学（低アルブミン血症・脱水）で全身状態を評価。皮膚生検で表皮の剥離・膿疱形成を確認。外傷（闘争・歯のクリッピング不良）が侵入門戸となるため飼育管理の確認が重要。"
}

ENRICHMENTS["exotic_other_porcine_pityriasis_rosea"] = {
    "diagnosis_ja": "特徴的な皮膚病変パターンの視診で臨床診断。丸〜楕円形の紅斑性丘疹が腹部・鼠径部から始まり体幹に拡大し、環状に融合して地図状模様を呈する。主に3-14週齢の子豚に発生。皮膚生検で表皮肥厚・不全角化・真皮浅層の血管周囲炎を確認。CBCは通常正常。皮膚掻爬でダニ・真菌を除外。遺伝的素因（ランドレース種で多い）があり、同腹子での発生を確認。自然治癒性（4-8週で消退）であり、予後は良好。"
}

ENRICHMENTS["exotic_other_porcine_mastitis"] = {
    "diagnosis_ja": "乳房の触診で腫脹・硬結・熱感・疼痛を評価。乳汁の細胞診・細菌培養・感受性試験で原因菌（E. coli, Klebsiella, Staphylococcus等）を同定。体温測定で発熱を確認。CBC（白血球増多・左方移動）で全身感染を評価。血液生化学で臓器障害を確認。泌乳低下・子豚の発育不良・母豚の食欲低下が臨床徴候。MMA症候群（乳房炎・子宮炎・無乳症）の一部として発症することが多く、子宮排出物の評価と併せて診断する。"
}

ENRICHMENTS["exotic_other_porcine_uterine_infection_metritis"] = {
    "diagnosis_ja": "膣排出物の性状（膿性・血膿性・悪臭）を評価。子宮スワブの細菌培養・感受性試験で原因菌（E. coli, Streptococcus, Arcanobacterium等）を同定。腹部超音波で子宮内液貯留・子宮壁肥厚を確認。体温測定で発熱を確認。CBC（白血球増多・左方移動）で全身感染を評価。血液生化学で臓器障害を確認。分娩後の合併症（難産・胎盤遺残・助産操作）との関連を聴取。MMA症候群の一環として乳房炎・無乳症の併発を評価する。"
}

ENRICHMENTS["exotic_other_salt_poisoning___water_deprivation_porcine"] = {
    "diagnosis_ja": "血液生化学でNa濃度上昇（>160 mEq/L）を確認。CSF分析でNa上昇・好酸球性髄膜脳炎の所見。神経症状（間欠的痙攣・旋回運動・盲目・角弓反張・犬座姿勢）が特徴的臨床徴候。飼育管理の聴取（飲水制限・ミネラル過剰給餌・飲水器の故障）が診断の鍵。CBC・血液生化学（電解質パネル・浸透圧）で高浸透圧状態を評価。病理組織検査で脳の好酸球性髄膜脳炎・大脳皮質壊死が確定的。水分の急速補正は脳浮腫を悪化させるため、緩徐な是正が必須。"
}

# === Caprine (Goat) diseases ===

ENRICHMENTS["exotic_other_caprine_arthritis_encephalitis_cae"] = {
    "diagnosis_ja": "血清学的検査（ELISA・AGID）で抗CAEウイルス抗体を検出。PCR（血液・乳汁・滑膜液）でウイルスRNAを確認。レンチウイルス感染であり、成ヤギでは慢性進行性関節炎（手根関節腫脹が特徴的）、子ヤギでは脳脊髄炎として発現。滑膜液分析で単核球増多を確認。CSF分析で蛋白上昇・リンパ球性細胞増多。CBC・血液生化学で全身状態を評価。感染は経乳汁伝播が主であり、飼育歴・母畜の感染状況を聴取。根治治療はなく淘汰が基本。"
}

ENRICHMENTS["exotic_other_caseous_lymphadenitis_cl"] = {
    "diagnosis_ja": "体表リンパ節（下顎・肩前・膝窩）の腫脹を触診で確認。膿瘍穿刺で特徴的な層状の乾酪壊死物質（「玉ねぎの皮」様）を採取。細菌培養でCorynebacterium pseudotuberculosisを分離・同定。PCRによる迅速確認。血清学的検査（SHI・ELISA）で抗体を検出（内臓型の診断補助）。CBC・血液生化学（低アルブミン血症・高グロブリン血症）で慢性感染を評価。胸部・腹部超音波/X線で内臓型（肺・肝・腎の膿瘍）を評価。人獣共通感染症の可能性に注意。"
}

ENRICHMENTS["exotic_other_caprine_contagious_pleuropneumonia"] = {
    "diagnosis_ja": "胸部X線で片側性の線維素性胸膜肺炎パターン・胸水貯留を確認。気管洗浄液・胸水からの培養でMycoplasma capricolum subsp. capripneumoniaeを分離（培養は専門施設が必要）。PCRによる迅速検出が推奨される。CBC（白血球増多）・血液生化学（フィブリノーゲン上昇）で急性炎症を評価。高熱・呼吸困難・咳嗽・鼻汁が急性臨床徴候。病理組織検査で線維素性胸膜肺炎・肺の肝変化を確認。OIE届出疾病であり、疫学調査と報告義務がある。"
}

ENRICHMENTS["exotic_other_enterotoxemia_overeating_disease"] = {
    "diagnosis_ja": "腸管内容物からのClostridium perfringens毒素検出（ELISA・PCR）が確定診断の鍵。C. perfringens D型のε毒素が最も一般的。急性死亡・軟腎（pulpy kidney）が特徴的。CBC・血液生化学（高血糖＝ε毒素の膵島破壊、BUN上昇）で代謝異常を評価。尿検査で糖尿を確認（高血糖の反映）。穀物過剰摂取・急激な食餌変更の既往聴取が診断の鍵。病理組織検査で腎皮質の自己融解・脳の対称性軟化を確認。CDTワクチン接種歴の確認が重要。"
}

ENRICHMENTS["exotic_other_caprine_foot_rot"] = {
    "diagnosis_ja": "蹄の視診で蹄間部の発赤・腫脹・壊死・悪臭・蹄壁の剥離を確認。蹄間部スワブの嫌気性培養でDichelobacter nodosusを分離。PCRで毒力遺伝子（aprV2/B2）を検出し良性型・悪性型を鑑別。跛行スコアリングで重症度を評価。蹄の削蹄後に蹄底の病変範囲を確認。CBC・血液生化学は重度例で全身感染を評価。Fusobacterium necrophorumとの混合感染が多い。飼育環境（泥濘・湿潤な放牧地）の確認が重要。群全体の蹄の検査が推奨される。"
}

ENRICHMENTS["exotic_other_listeriosis_goat"] = {
    "diagnosis_ja": "神経症状（旋回運動・斜頸・顔面神経麻痺・流涎・嚥下困難）の臨床評価。CSF分析でリンパ球性細胞増多・蛋白上昇を確認。血液培養・CSF培養でListeria monocytogenesを分離。PCRによる迅速検出。CBC（単球増多が示唆的）・血液生化学で全身状態を評価。汚染サイレージ（pH>5.0でListeria増殖）からの経口感染が最も多い経路であり、飼料の品質・保管状態の聴取が重要。人獣共通感染症であり、妊娠女性への感染リスクに注意。"
}

ENRICHMENTS["exotic_other_polioencephalomalacia_goat"] = {
    "diagnosis_ja": "神経症状（盲目・運動失調・角弓反張・痙攣・昏睡）の臨床評価。チアミン（ビタミンB1）欠乏が主因であり、血中チアミン濃度・赤血球トランスケトラーゼ活性の測定で確認。チアミン投与への劇的な臨床応答が治療的診断となる。CBC・血液生化学（乳酸上昇・代謝性アシドーシス）で全身状態を評価。MRI（利用可能な場合）で大脳皮質の対称性壊死を確認。穀物過剰摂取・硫黄過剰（水・飼料中）・チアミナーゼ産生菌の増殖がリスク因子。食餌歴の聴取が必須。"
}

ENRICHMENTS["exotic_other_pregnancy_toxemia_ketosis_-_goat"] = {
    "diagnosis_ja": "血液生化学で低血糖・高βヒドロキシ酪酸（BHB>3.0 mmol/L）・高NEFA（遊離脂肪酸）を確認。尿検査でケトン体陽性を検出。妊娠末期（最後の6週間）の多胎妊娠ヤギに好発。食欲低下・抑うつ・運動失調・歯ぎしり・盲目が臨床徴候。超音波で胎児数を確認（多胎ほどリスク高）。CBC・血液生化学（肝酵素上昇・BUN上昇・電解質異常）で肝リピドーシス・腎障害を評価。栄養管理歴（エネルギー摂取不足）の聴取が診断の鍵。"
}

ENRICHMENTS["exotic_other_goat_lice_infestation"] = {
    "diagnosis_ja": "被毛の直接検査でシラミ成虫・卵（ニット）を確認。テープ法・毛の顕微鏡検査で種を同定（咬むシラミ：Bovicola caprae、吸血シラミ：Linognathus stenopsis）。冬季に症状が増悪する傾向。掻痒・脱毛・被毛粗剛・痂皮形成が臨床徴候。CBC（好酸球増多・吸血シラミでは貧血）で寄生による影響を評価。飼育環境（過密飼育・栄養不良）の確認が重要。群全体の検査と同時治療が再発予防に不可欠。他の外部寄生虫（疥癬ダニ）との鑑別も実施。"
}

ENRICHMENTS["exotic_other_caprine_mastitis"] = {
    "diagnosis_ja": "乳房の触診で腫脹・硬結・熱感・疼痛・左右差を評価。乳汁のCMT（カリフォルニア乳房炎テスト）で体細胞数増加を確認。乳汁の細菌培養・感受性試験で原因菌（Staphylococcus aureus, Streptococcus, Mannheimia, Mycoplasma等）を同定。CBC（白血球増多）・血液生化学で全身感染を評価。体温測定で発熱を確認。壊疽性乳房炎（特にS. aureus, C. perfringens）では乳房の変色・冷感・壊死が特徴的。泌乳量低下・乳汁性状変化が初期徴候。"
}

ENRICHMENTS["exotic_other_haemonchosis_barber_pole_worm"] = {
    "diagnosis_ja": "糞便検査（McMaster法）でHaemonchus contortus虫卵を検出・EPG（卵数/g）を定量。FAMACHA法で結膜蒼白度を5段階評価（貧血の臨床的スクリーニング）。PCV/Ht測定で貧血の程度を確認（正常22-38%、<15%で重度）。血液生化学（低アルブミン血症・低総蛋白）で慢性失血を評価。ボトルジョー（顎下浮腫）・被毛粗剛・体重減少が臨床徴候。駆虫薬耐性検査（FECRT：糞便虫卵減少率試験）で適切な薬剤選択を行う。放牧管理の聴取が重要。"
}

ENRICHMENTS["exotic_other_tetanus_goat"] = {
    "diagnosis_ja": "特徴的な臨床徴候（全身性筋強直・開口障害・第三眼瞼突出・鋸馬姿勢・四肢伸展硬直・外部刺激への過敏反応）に基づく臨床診断。創傷（去勢・除角・蹄のトリミング・分娩）の既往を聴取。Clostridium tetaniの培養は困難で臨床的意義は限定的。血清中テタノスパスミン抗体の測定は実用的でない。CBC・血液生化学で二次的な代謝異常（呼吸性アシドーシス・横紋筋融解によるCK上昇）を評価。CDTワクチン接種歴の確認が重要。"
}

# === Hedgehog diseases (in Exotic Other) ===

ENRICHMENTS["exotic_other_hedgehog_wobbly_hedgehog_syndrome_whs"] = {
    "diagnosis_ja": "進行性の後肢不全麻痺・運動失調・筋萎縮の神経学的検査。WHSは進行性の脱髄性脊髄症であり、後肢から始まり前肢・全身に波及する。EMG（筋電図、利用可能な場合）で脱神経パターンを確認。CBC・血液生化学で代謝性・感染性の鑑別疾患を除外。X線で脊椎の構造的異常を除外。確定診断は死後の脊髄・脳組織の病理組織検査（脱髄・軸索変性）による。遺伝性疾患であり治療法はなく、3歳以下で発症が多い。QOL評価に基づく対症療法と予後説明が重要。"
}

ENRICHMENTS["exotic_other_hedgehog_skin_mites_caparinia_tripilis"] = {
    "diagnosis_ja": "皮膚掻爬検査でCaparinia tripilisダニ（成虫・卵・幼虫）を顕微鏡で確認。棘の基部と皮膚の境界部からの掻爬が検出率が高い。掻痒・落屑・痂皮形成・棘の脱落が主要臨床徴候。丸まった状態でのイソフルラン吸入鎮静により検査が容易になる。CBC（好酸球増多）で寄生虫感染を示唆。皮膚真菌培養でTrichophytonを除外（ダニ症と真菌症は類似の臨床像を呈する）。飼育環境（床材の種類・衛生状態）の確認が重要。同居個体の同時検査・治療を推奨。"
}

ENRICHMENTS["exotic_other_hedgehog_ringworm_trichophyton"] = {
    "diagnosis_ja": "皮膚掻爬・被毛（棘を含む）のDTM培養でTrichophyton mentagrophytes（最も一般的）またはT. erinaceiを同定。KOH標本で菌糸・分節胞子を鏡検。ウッド灯検査（T. mentagrophytesは通常蛍光陰性のため培養が必須）。棘基部の落屑・痂皮・棘脱落が臨床徴候。ダニ症との鑑別に皮膚掻爬を併せて実施。人獣共通感染症であり飼育者の皮膚症状を確認。丸まるハリネズミには吸入鎮静による検査が推奨される。CBC・血液生化学で免疫状態を評価。"
}

ENRICHMENTS["exotic_other_hedgehog_obesity"] = {
    "diagnosis_ja": "体重測定（正常値300-600g、種による差あり）と体型評価で肥満度を判定。ハリネズミが丸まれない場合は重度肥満を示唆。脂肪蓄積部位（脇腹・顎下・四肢基部）の触診。血液生化学（高血糖・高コレステロール・高中性脂肪・肝酵素上昇）で代謝異常を評価。肝臓超音波でエコー輝度亢進（脂肪肝）を確認。食餌内容（高脂肪昆虫・キャットフード過剰給餌）と運動量（回し車の使用状況）の詳細聴取が診断・管理の核心。心エコーで心血管系への影響を評価。"
}

ENRICHMENTS["exotic_other_hedgehog_cardiomyopathy"] = {
    "diagnosis_ja": "心エコー検査で心室壁厚・内腔径・収縮機能（FS%・EF%）を評価。拡張型心筋症（DCM）がハリネズミで最も多く報告されている。胸部X線で心拡大（VHS増大）・肺水腫・胸水を確認。ECG（利用可能な場合）で不整脈を検出。CBC・血液生化学（BUN・クレアチニン上昇＝心腎症候群）で全身状態を評価。NT-proBNP（利用可能な場合）で心不全の重症度を評価。運動不耐性・呼吸困難・腹水・嗜眠が臨床徴候。肥満との関連も示唆されている。"
}

# === Sugar Glider diseases (in Exotic Other) ===

ENRICHMENTS["exotic_other_sugar_glider_self-mutilation"] = {
    "diagnosis_ja": "自傷部位（陰茎・四肢・飛膜・尾が好発）の損傷程度を直接視診で評価。飼育環境の包括的聴取（単独飼育が最大のリスク因子・ケージサイズ・enrichment不足・不適切な光周期）。CBC・血液生化学で基礎疾患（疼痛の原因）を除外。皮膚掻爬・培養で感染性皮膚疾患を除外。フクロモモンガは社会的有袋類であり、孤独ストレスが自咬の主因。去勢雄での陰茎自咬が特に多い。エリザベスカラー代替法・同居個体導入・飼い主接触時間増加が治療戦略の中心。"
}

ENRICHMENTS["exotic_other_sugar_glider_nutritional_osteodystrophy"] = {
    "diagnosis_ja": "全身X線で骨密度低下・皮質菲薄化・病的骨折を確認。血液生化学でCa低下・P上昇・ALP上昇を測定。イオン化Ca測定が最も正確な低Ca血症の評価法。食餌内容の詳細聴取（果物偏食・Ca:P比の偏り・昆虫タンパク不足・ビタミンD3欠乏）が診断の核心。フクロモモンガのMBD（代謝性骨疾患）は不適切な食餌管理が最も多い原因。PTH測定で二次性副甲状腺機能亢進を確認。筋攣縮・後肢麻痺・ゴム様顎・病的骨折が臨床徴候。"
}

ENRICHMENTS["exotic_other_sugar_glider_aflatoxicosis"] = {
    "diagnosis_ja": "飼料のアフラトキシン検査（ELISA・HPLC）で汚染レベルを確認。血液生化学で肝酵素著増（ALT・AST・GGT・ALP）・高ビリルビン血症・低アルブミン血症を評価。CBC（血小板減少・貧血）で凝固障害を確認。凝固検査（PT・APTT延長）で肝合成機能低下を評価。肝臓超音波でエコー輝度変化・肝腫大を確認。食欲低下・黄疸・腹水・嗜眠が臨床徴候。汚染されたナッツ・穀物・昆虫飼料が暴露源。確定診断は肝生検による病理組織検査。"
}

ENRICHMENTS["exotic_other_sugar_glider_ick_bacterial_dermatitis"] = {
    "diagnosis_ja": "皮膚病変（発赤・落屑・脱毛・痂皮・自傷痕）の分布と重症度を視診で評価。皮膚掻爬検査でダニを除外。細菌培養・感受性試験で原因菌を同定。真菌培養で皮膚糸状菌を除外。CBCで炎症マーカーを確認。フクロモモンガの「Ick」はストレス誘発性の皮膚疾患であり、飼育環境のストレス因子（単独飼育・不適切な温度・騒音・光周期の乱れ）を包括的に評価。夜行性の活動時間帯の乱れがストレス性皮膚炎を誘発する。基礎疾患の除外と環境改善が治療の核心。"
}

# === Ferret diseases (in Exotic Other) ===

ENRICHMENTS["exotic_other_ferret_adrenal_gland_disease"] = {
    "diagnosis_ja": "血中ステロイドホルモンパネル（エストラジオール・17α-ヒドロキシプロゲステロン・アンドロステンジオン・DHEA-S）の上昇で内分泌的に診断。腹部超音波で副腎の腫大（正常<3.5mm幅）・形態変化を確認（左副腎の方が超音波で評価しやすい）。両側性脱毛（体幹・尾部から始まる）・外陰部腫脹（避妊済み雌）・前立腺肥大（去勢済み雄）が特徴的臨床徴候。CBC・血液生化学で全身状態を評価。中高齢の去勢/避妊済みフェレットに好発。"
}

ENRICHMENTS["exotic_other_ferret_insulinoma"] = {
    "diagnosis_ja": "血糖値測定で低血糖（<60 mg/dL）を確認。同時採血のインスリン値が相対的高値（正常低血糖時にはインスリン分泌抑制されるべき）であれば診断的。4-6時間絶食後の血糖・インスリン同時測定が推奨。腹部超音波で膵臓の結節を検出（感度は限定的）。CBC・血液生化学で肝機能・腎機能を確認。後肢脱力・嗜眠・流涎・空視・痙攣が低血糖の臨床徴候。中高齢フェレット（4歳以上）に好発。副腎疾患・リンパ腫との多重罹患が多く、包括的な評価が必要。"
}

ENRICHMENTS["exotic_other_ferret_lymphoma"] = {
    "diagnosis_ja": "末梢リンパ節の触診で腫大を評価。FNA細胞診で異型リンパ球を確認。確定診断は生検による病理組織学的検査とフローサイトメトリー。CBC（異常リンパ球・貧血・血小板減少）で白血化の有無を確認。血液生化学（LDH上昇・高Ca血症）で腫瘍随伴症候群を評価。胸部X線で前縦隔腫瘤・胸水を確認。腹部超音波で脾腫・肝腫大・腸管壁肥厚・腸間膜リンパ節腫大を評価。若齢型（<2歳）と中高齢型で臨床像が異なる。骨髄検査で浸潤を評価。"
}

ENRICHMENTS["exotic_other_ferret_aplastic_anemia_estrogen_toxicity"] = {
    "diagnosis_ja": "CBC・血液塗抹で重度の汎血球減少（貧血・白血球減少・血小板減少）を確認。PCV<20%で輸血の適応を検討。未避妊雌の持続発情（外陰部腫脹>1ヶ月）の既往が診断の鍵。血中エストラジオール測定で高値を確認。骨髄検査（生検）で低形成〜無形成骨髄を確認。フェレットは誘発排卵動物であり、交配がないと持続発情→慢性エストロゲン過剰→骨髄抑制に至る。避妊手術歴の確認が必須。血液凝固検査で出血傾向を評価。予後は骨髄回復能に依存する。"
}

ENRICHMENTS["exotic_other_ferret_canine_distemper"] = {
    "diagnosis_ja": "臨床徴候（鼻汁・結膜炎・皮疹[足底・口唇の過角化]・発熱・CNS症状）の評価。結膜・皮膚スワブのRT-PCRでCDVウイルスRNAを検出。蛍光抗体法（FA）で結膜上皮のウイルス抗原を確認。CBC（リンパ球減少）・血液生化学で全身状態を評価。ワクチン接種歴（フェレット用不活化CDVワクチンの使用が必須、犬用MLVワクチンは致死的）を確認。フェレットのジステンパーは致死率100%に近い。感染犬との接触歴の聴取が重要。"
}

ENRICHMENTS["exotic_other_ferret_influenza"] = {
    "diagnosis_ja": "鼻腔スワブのインフルエンザ迅速抗原検査・RT-PCRでA型またはB型インフルエンザウイルスを検出。くしゃみ・鼻汁・発熱・嗜眠・食欲低下が主要臨床徴候。フェレットはヒトインフルエンザウイルスに自然感受性があり、飼い主からの伝播が最も多い感染経路。CBC（リンパ球減少）・血液生化学で全身状態を評価。胸部X線で肺炎合併を除外。通常は自然治癒性（5-7日）だが、若齢・免疫抑制個体では重症化しうる。飼育者の上気道症状の聴取が重要。"
}

ENRICHMENTS["exotic_other_ferret_aleutian_disease"] = {
    "diagnosis_ja": "血清学的検査（CEP：向流免疫電気泳動、ELISA）でADV（アリューシャンミンクウイルス）抗体を検出。PCR（血液・糞便）でウイルスDNAを確認。血清蛋白電気泳動でポリクローナルγグロブリン上昇（>20%）が特徴的。CBC・血液生化学（高グロブリン血症・BUN/クレアチニン上昇・肝酵素上昇）で免疫複合体性臓器障害を評価。尿検査で蛋白尿を確認。慢性消耗・後肢麻痺・メレナが臨床徴候。確定診断は組織生検による免疫複合体の沈着確認。"
}

ENRICHMENTS["exotic_other_ferret_ece_epizootic_catarrhal_enteritis"] = {
    "diagnosis_ja": "特徴的な「緑色粘液便」（green slime）の視覚的確認が臨床的に最も示唆的。糞便のRT-PCRでフェレットコロナウイルス（FECV）を検出。CBC（リンパ球減少）・血液生化学（電解質異常・低アルブミン血症・肝酵素上昇）で脱水・栄養吸収障害を評価。腹部X線で腸管拡張を確認。病理組織検査で小腸絨毛の萎縮・壊死・リンパ球性腸炎を確認。新規導入個体からの感染が最も多い経路であり、導入歴の聴取が重要。若齢では軽症、高齢では重症化しやすい。"
}

ENRICHMENTS["exotic_other_ferret_gastric_foreign_body"] = {
    "diagnosis_ja": "腹部X線でX線不透過性異物を確認（ゴム・スポンジ等のX線透過性異物は造影検査が必要）。腹部超音波で胃内異物・胃壁浮腫・腸管拡張を評価。バリウム造影で通過障害・充満欠損を確認。CBC・血液生化学（電解質異常・BUN上昇）で脱水・全身状態を評価。嘔吐・食欲低下・嗜眠・歯ぎしり（疼痛徴候）が臨床徴候。フェレットはゴム製品を好んで咀嚼・嚥下する傾向があり、飼育環境の確認が重要。内視鏡的除去または外科的摘出の適応を判断する。"
}

ENRICHMENTS["exotic_other_ferret_helicobacter_gastritis"] = {
    "diagnosis_ja": "胃生検の病理組織検査（Warthin-Starry銀染色・ギムザ染色）でHelicobacter mustelaeを確認。胃粘膜の培養で菌を分離。PCRによる検出も可能。糞便抗原検査（利用可能な場合）。CBC・血液生化学で貧血（慢性出血性）・低アルブミン血症を評価。便潜血検査・メレナの確認で消化管出血を評価。食欲低下・体重減少・嘔吐・歯ぎしり・黒色便が臨床徴候。フェレットのH. mustelae保有率は非常に高く（>95%）、臨床症状の発現は免疫状態に依存する。"
}

ENRICHMENTS["exotic_other_ferret_proliferative_bowel_disease"] = {
    "diagnosis_ja": "糞便PCRでDesulfovibrio（旧Lawsonia intracellularis）を検出。腹部触診で肥厚した結腸・直腸を評価（「ソーセージ様」）。直腸生検で増殖性腸炎の特徴的な腸陰窩過形成を確認。CBC（白血球増多）・血液生化学（低アルブミン血症・電解質異常）で全身状態を評価。血性粘液便・テネスムス・直腸脱・体重減少が臨床徴候。若齢フェレット（4-8ヶ月）に好発。腹部超音波で結腸壁肥厚を確認。ストレス（環境変化・過密飼育）が発症誘因となる。"
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
