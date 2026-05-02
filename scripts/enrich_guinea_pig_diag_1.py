#!/usr/bin/env python3
"""Enrich diagnosis_ja for 50 Guinea Pig diseases (guinea_pig_0001–0050)."""

import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# guinea_pig_0001 Scurvy (Vitamin C Deficiency)
ENRICHMENTS["guinea_pig_0001"] = {
    "diagnosis_ja": (
        "血漿ビタミンC濃度測定（正常0.9–1.6 mg/dL、<0.5で欠乏確定）。口腔内検査で歯肉出血・潰瘍を確認。"
        "四肢X線で骨端線開大・骨膜下出血・長管骨の骨折を評価。CBC（貧血・白血球増多）・血液生化学。"
        "皮膚所見として粗剛被毛・脱毛・点状出血を視診。関節腫脹・疼痛による歩行異常の触診。"
        "鑑別：不正咬合、骨折、敗血症。ビタミンC 50–100 mg/日投与への反応で確定的診断。"
    )
}

# guinea_pig_0002 Pneumonia (Bacterial)
ENRICHMENTS["guinea_pig_0002"] = {
    "diagnosis_ja": (
        "聴診で捻髪音・湿性ラ音を確認。胸部X線で肺野浸潤影・気管支肺炎パターンを評価。"
        "鼻汁・気管洗浄液の細菌培養・感受性試験（Bordetella, Streptococcus, Pasteurellaを標的）。"
        "CBC（好中球増多・左方移動）・血液生化学（急性期蛋白上昇）。動脈血ガス分析（重症時）。"
        "鑑別：心不全による肺水腫、胸水、肺腫瘍。ペニシリン系・リンコサミド系は致死的腸内細菌叢破壊のため禁忌。"
    )
}

# guinea_pig_0003 Bordetella bronchiseptica Infection
ENRICHMENTS["guinea_pig_0003"] = {
    "diagnosis_ja": (
        "鼻汁の細菌培養でBordetella bronchisepticaを同定。PCR検査による迅速確定診断。"
        "胸部X線で気管支肺炎像を評価。鼻腔スワブのグラム染色（グラム陰性小桿菌）。"
        "CBC（好中球増多）・血液生化学。聴診で呼吸音異常（捻髪音・喘鳴）を確認。"
        "鑑別：Streptococcus pneumoniae肺炎、マイコプラズマ、アデノウイルス。ウサギとの同居歴を確認（感染源）。"
    )
}

# guinea_pig_0004 Streptococcus pneumoniae Infection
ENRICHMENTS["guinea_pig_0004"] = {
    "diagnosis_ja": (
        "鼻汁・中耳液・髄液の細菌培養でStreptococcus pneumoniaeを同定。血液培養（菌血症疑い時）。"
        "胸部X線で肺炎・胸水を評価。鼓室包X線またはCTで中耳炎・内耳炎を確認。"
        "CBC（好中球増多・左方移動）・血液生化学（CRP上昇）。斜頸がある場合は内耳炎を精査。"
        "鑑別：Bordetella感染、リンパ球性脈絡髄膜炎（LCMV）、Pasteurella。ペニシリン系は腸管毒性のため禁忌。"
    )
}

# guinea_pig_0005 Malocclusion
ENRICHMENTS["guinea_pig_0005"] = {
    "diagnosis_ja": (
        "無麻酔下での口腔内視診（耳鏡・頬拡張器使用）で切歯・臼歯の過長・棘状突起を確認。"
        "頭部X線（側面・腹背）で常生歯の歯根伸長・歯根膿瘍・顎骨変形を評価。CT推奨（重症例）。"
        "流涎・食欲低下・体重減少の経過を聴取。眼球突出・鼻涙管閉塞は上顎臼歯根尖異常を示唆。"
        "鑑別：壊血病による歯肉炎、顎骨骨髄炎、口腔内腫瘍。常生歯のため定期トリミングが必要。"
    )
}

# guinea_pig_0006 Bumblefoot (Pododermatitis)
ENRICHMENTS["guinea_pig_0006"] = {
    "diagnosis_ja": (
        "足底部の視診でグレード分類（Ⅰ：発赤→Ⅱ：潰瘍→Ⅲ：腱・骨浸潤）。触診で腫脹・熱感・疼痛を評価。"
        "足部X線で骨髄炎の有無を確認。潰瘍部の細菌培養・感受性試験（Staphylococcus aureus多発）。"
        "CBC・血液生化学（慢性感染時のアミロイドーシスリスク評価）。体重・BMI・飼育環境（床材）を確認。"
        "鑑別：外傷性足底潰瘍、真菌感染、扁平上皮癌。肥満・金網床・ビタミンC欠乏が素因。"
    )
}

# guinea_pig_0007 Barbering
ENRICHMENTS["guinea_pig_0007"] = {
    "diagnosis_ja": (
        "被毛の咬断パターンを視診（自己咬毛 vs 同居個体による咬毛：部位で鑑別）。"
        "皮膚掻爬検査・トリコグラムで外部寄生虫（Trixacarus caviae、Chirodiscoides caviae）を除外。"
        "真菌培養（Trichophyton mentagrophytes）で皮膚糸状菌症を除外。飼育環境・ストレス要因を聴取。"
        "CBC・血液生化学・甲状腺ホルモン（内分泌疾患の除外）。卵巣嚢腫に伴う脱毛との鑑別（腹部超音波）。"
    )
}

# guinea_pig_0008 Ovarian Cysts
ENRICHMENTS["guinea_pig_0008"] = {
    "diagnosis_ja": (
        "腹部超音波検査で卵巣嚢腫の大きさ・数・両側性を評価（最大10 cm以上になることもある）。"
        "腹部X線で腹腔内占拠性病変・腸管圧排を確認。CBC・血液生化学。"
        "左右体側の対称性脱毛を視診（エストロゲン過剰による）。乳腺肥大・外陰部腫脹を確認。"
        "鑑別：子宮疾患（子宮蓄膿症・子宮腺癌）、副腎腫瘍、妊娠。2歳以上の未避妊雌で好発。"
    )
}

# guinea_pig_0009 Urolithiasis
ENRICHMENTS["guinea_pig_0009"] = {
    "diagnosis_ja": (
        "腹部X線で尿路結石の位置・サイズ・数を確認（炭酸カルシウム結石が最多で高X線不透過性）。"
        "腹部超音波で腎盂拡張・膀胱壁肥厚・尿管結石を評価。尿検査（血尿・結晶尿・pH・比重）。"
        "CBC・血液生化学（BUN・Cre上昇で腎後性腎不全を評価）。排尿姿勢・血尿・鳴き声の経過聴取。"
        "鑑別：膀胱炎、子宮疾患による血尿、腎腫瘍。カルシウム代謝異常が背景にあるため食事内容を精査。"
    )
}

# guinea_pig_0010 LCMV (Lymphocytic Choriomeningitis Virus)
ENRICHMENTS["guinea_pig_0010"] = {
    "diagnosis_ja": (
        "血清学的検査（IFA法・ELISA法）でLCMV抗体を検出。RT-PCRによるウイルスRNA検出（血液・臓器）。"
        "ヒトへの人獣共通感染症リスクがあるため取扱い注意。CBC（リンパ球増多）・血液生化学。"
        "神経症状（振戦・痙攣・運動失調）の有無を確認。無症候性キャリアが多い（持続感染）。"
        "鑑別：中耳炎による斜頸、脳炎（細菌性）、外傷性脊髄損傷。野生マウスとの接触歴を確認。"
    )
}

# guinea_pig_0011 GI Stasis
ENRICHMENTS["guinea_pig_0011"] = {
    "diagnosis_ja": (
        "腹部X線で消化管ガス像・胃拡張・糞便停滞を評価。腹部超音波で腸管蠕動低下を確認。"
        "CBC・血液生化学（肝リピドーシス合併時のALT・AST上昇、低血糖）。糞便量・形状の変化を聴取。"
        "腹部触診で鼓腸・硬結した糞便塊を確認。体温測定（低体温は予後不良因子）。"
        "鑑別：腸閉塞、盲腸捻転、腹腔内腫瘍。ストレス・食事変更・抗菌薬投与・疼痛が誘因。ビタミンC欠乏も素因。"
    )
}

# guinea_pig_0012 Cecal Dysbiosis
ENRICHMENTS["guinea_pig_0012"] = {
    "diagnosis_ja": (
        "糞便検査（直接塗抹・グラム染色）で腸内細菌叢の異常（グラム陽性菌過増殖・クロストリジウム優勢）を評価。"
        "糞便培養・嫌気培養でClostridium spp.等の病原菌を同定。糞便PCR（C. difficileトキシン）。"
        "腹部X線で盲腸ガス像・鼓腸を確認。CBC・血液生化学（脱水・電解質異常）。"
        "鑑別：抗菌薬関連下痢、サルモネラ症、コクシジウム症。ペニシリン系・リンコサミド系の使用歴を必ず確認。"
    )
}

# guinea_pig_0013 Bloat (Gastric Tympany)
ENRICHMENTS["guinea_pig_0013"] = {
    "diagnosis_ja": (
        "腹部X線で胃の著明なガス拡張を確認（緊急評価）。腹部触診で腹部膨満・鼓音を確認。"
        "CBC・血液生化学（乳酸値上昇・電解質異常・低血糖）。腹部超音波で胃壁浮腫・腸管蠕動停止を評価。"
        "経口ゾンデまたは経皮的胃穿刺によるガス減圧（治療的かつ診断的）。体温・心拍・呼吸数の連続モニタリング。"
        "鑑別：GI stasis、盲腸捻転、腸閉塞。発酵性食物の過剰摂取・急激な食事変更が誘因。"
    )
}

# guinea_pig_0014 Antibiotic-Associated Diarrhea
ENRICHMENTS["guinea_pig_0014"] = {
    "diagnosis_ja": (
        "抗菌薬投与歴の詳細聴取（ペニシリン系・セファロスポリン系・リンコサミド系・マクロライド系が高リスク）。"
        "糞便培養・嫌気培養でClostridium difficile・C. perfringensを検出。糞便PCR（トキシンA/B）。"
        "CBC（好中球増多・左方移動）・血液生化学（電解質異常・脱水・低アルブミン）。腹部X線で鼓腸・盲腸拡張を確認。"
        "鑑別：原発性腸炎、コクシジウム症、サルモネラ症。モルモットは盲腸発酵依存のため抗菌薬選択が極めて重要。"
    )
}

# guinea_pig_0015 Clostridioides difficile Colitis
ENRICHMENTS["guinea_pig_0015"] = {
    "diagnosis_ja": (
        "糞便PCRでClostridioides difficileトキシンA/B遺伝子を検出。糞便ELISA（GDH抗原＋トキシン検出）。"
        "糞便嫌気培養でC. difficileを分離・同定。CBC（好中球増多・左方移動）・血液生化学（低アルブミン・電解質異常）。"
        "腹部X線で結腸・盲腸の拡張・壁肥厚を評価。体温・脱水度・糞便性状（粘液血便）を記録。"
        "鑑別：他のクロストリジウム症、サルモネラ、コクシジウム。抗菌薬投与後3–7日での発症が典型的。"
    )
}

# guinea_pig_0016 Salmonellosis
ENRICHMENTS["guinea_pig_0016"] = {
    "diagnosis_ja": (
        "糞便培養（選択培地：SS寒天・XLD寒天）でSalmonella spp.を分離。血液培養（敗血症疑い時）。"
        "CBC（好中球増多または減少・左方移動）・血液生化学（肝酵素上昇・電解質異常）。"
        "腹部超音波で肝脾腫・腸管壁肥厚を確認。剖検では肝臓・脾臓の壊死巣が特徴的。"
        "鑑別：エルシニア症、大腸菌性腸炎、C. difficile。人獣共通感染症のため取扱い注意。急性型は敗血症で突然死あり。"
    )
}

# guinea_pig_0017 Yersiniosis
ENRICHMENTS["guinea_pig_0017"] = {
    "diagnosis_ja": (
        "糞便培養・冷温増菌培養（4℃）でYersinia pseudotuberculosisを分離。血液培養（敗血症型）。"
        "CBC（好中球増多）・血液生化学（肝酵素上昇）。腹部超音波で腸間膜リンパ節腫大・肝脾膿瘍を評価。"
        "剖検で腸間膜リンパ節・肝臓・脾臓の乾酪壊死巣が特徴。腹部X線で腸管壁肥厚・リンパ節腫大。"
        "鑑別：サルモネラ症、結核、リンパ腫。慢性型は消耗・体重減少が主訴。人獣共通感染症。"
    )
}

# guinea_pig_0018 E. coli Enteritis
ENRICHMENTS["guinea_pig_0018"] = {
    "diagnosis_ja": (
        "糞便培養で病原性大腸菌を分離（血清型・病原因子遺伝子のPCR同定）。薬剤感受性試験を実施。"
        "CBC（好中球増多）・血液生化学（BUN上昇・電解質異常・脱水）。糞便検査で他の病原体を除外。"
        "腹部X線で腸管拡張・ガス像を評価。脱水度・体重・糞便性状（水様性・粘血便）を記録。"
        "鑑別：サルモネラ症、クロストリジウム腸炎、コクシジウム。幼若個体・ストレス時に好発。"
    )
}

# guinea_pig_0019 Cryptosporidiosis
ENRICHMENTS["guinea_pig_0019"] = {
    "diagnosis_ja": (
        "糞便検査（抗酸染色・蛍光抗体法）でCryptosporidiumオーシストを検出。糞便PCRで種同定。"
        "糞便ELISA（Cryptosporidium抗原検出）。CBC・血液生化学（脱水・電解質異常）。"
        "腹部X線で腸管拡張を評価。体重減少・慢性下痢の経過を聴取。免疫抑制状態の評価。"
        "鑑別：ジアルジア、コクシジウム、細菌性腸炎。人獣共通感染症のため取扱い注意。幼若個体で重症化。"
    )
}

# guinea_pig_0020 Giardiasis
ENRICHMENTS["guinea_pig_0020"] = {
    "diagnosis_ja": (
        "糞便直接塗抹（生理食塩水マウント）で栄養体の運動を確認。硫酸亜鉛浮遊法でシストを検出。"
        "糞便ELISA（Giardia抗原検出キット）。糞便PCRで種・遺伝子型を同定。"
        "3日間連続の糞便検査を推奨（間欠的排出のため1回では偽陰性リスク）。CBC・血液生化学（慢性例で低アルブミン）。"
        "鑑別：クリプトスポリジウム、コクシジウム、トリコモナス、細菌性腸炎。"
    )
}

# guinea_pig_0021 Coccidiosis
ENRICHMENTS["guinea_pig_0021"] = {
    "diagnosis_ja": (
        "糞便浮遊法（飽和食塩水・硫酸亜鉛）でEimeriaオーシストを検出。オーシストの形態・サイズで種同定。"
        "糞便直接塗抹で出血性下痢の有無を確認。OPG（oocysts per gram）で感染強度を定量評価。"
        "CBC・血液生化学（貧血・低アルブミン・脱水）。腹部X線で腸管拡張を評価。"
        "鑑別：ジアルジア、クリプトスポリジウム、細菌性腸炎、蟯虫症。幼若・ストレス下の個体で臨床症状を発現。"
    )
}

# guinea_pig_0022 Pinworm Infection
ENRICHMENTS["guinea_pig_0022"] = {
    "diagnosis_ja": (
        "肛門周囲へのセロハンテープ法で蟯虫（Paraspidodera uncinata）の虫卵を検出。"
        "糞便浮遊法でも虫卵検出可能。肛門周囲の視診で成虫を直接確認できることもある。"
        "CBC（好酸球増多は軽度）。通常は無症候性だが、大量感染時は肛門掻痒・軟便を呈する。"
        "鑑別：コクシジウム、ジアルジア、皮膚糸状菌による肛門周囲炎。直接的な病原性は低いが衛生指標。"
    )
}

# guinea_pig_0023 Intestinal Obstruction
ENRICHMENTS["guinea_pig_0023"] = {
    "diagnosis_ja": (
        "腹部X線（立位・側臥位）で拡張腸管ループ・液体レベル・ガス像を確認。造影X線（バリウム非推奨、ガストログラフィン使用）。"
        "腹部超音波で腸管蠕動停止・拡張・腸重積を評価。CBC・血液生化学（電解質異常・脱水・乳酸上昇）。"
        "腹部触診で腫瘤・腸管硬結を確認。排便停止・腹部膨満・食欲廃絶の急性発症を聴取。"
        "鑑別：GI stasis、盲腸捻転、腸重積、腹腔内腫瘍。外科的介入が必要な場合はモルモットの麻酔リスクを考慮。"
    )
}

# guinea_pig_0024 Rectal Prolapse
ENRICHMENTS["guinea_pig_0024"] = {
    "diagnosis_ja": (
        "視診で肛門から脱出した直腸粘膜を確認（鮮紅色～暗赤色）。脱出組織の生存性（色調・浮腫・壊死）を評価。"
        "基礎疾患の精査：糞便検査（寄生虫・コクシジウム）、腹部X線・超音波（腸管腫瘤・腸重積）。"
        "CBC・血液生化学（脱水・電解質異常）。怒責の原因検索（下痢、便秘、泌尿器疾患、難産）。"
        "鑑別：腸重積の脱出、膣脱（雌）、腫瘤状病変。再発性の場合は結腸固定術（colopexy）を検討。"
    )
}

# guinea_pig_0025 Constipation
ENRICHMENTS["guinea_pig_0025"] = {
    "diagnosis_ja": (
        "腹部X線で結腸・直腸内の糞便貯留・ガス像を確認。腹部触診で硬結した糞便塊を触知。"
        "腹部超音波で腸管蠕動・盲腸の状態を評価。CBC・血液生化学（脱水・電解質異常・低カリウム）。"
        "食事内容（繊維不足）・飲水量・運動量・環境変化を聴取。肛門周囲の視診（糞便付着・会陰汚染）。"
        "鑑別：GI stasis、腸閉塞、盲腸便秘、巨大結腸症。高齢・肥満・運動不足が素因。"
    )
}

# guinea_pig_0026 Intussusception
ENRICHMENTS["guinea_pig_0026"] = {
    "diagnosis_ja": (
        "腹部超音波で「ターゲットサイン」（同心円状の腸管壁層構造）を確認——最も感度の高い検査。"
        "腹部X線で拡張腸管ループ・閉塞像を評価。腹部触診でソーセージ様腫瘤を触知することがある。"
        "CBC・血液生化学（脱水・電解質異常・乳酸上昇）。血便・粘液便・急性腹痛の経過を聴取。"
        "鑑別：腸閉塞（異物）、腸捻転、腸管腫瘍。基礎疾患（腸炎・寄生虫症）の精査が必須。外科的整復が第一選択。"
    )
}

# guinea_pig_0027 Cecal Impaction
ENRICHMENTS["guinea_pig_0027"] = {
    "diagnosis_ja": (
        "腹部X線で盲腸の著明な拡張・糞便物質の停滞を確認。腹部超音波で盲腸内容物の性状を評価。"
        "腹部触診で右下腹部に硬結した盲腸を触知。CBC・血液生化学（脱水・電解質異常・肝酵素上昇）。"
        "食事歴（低繊維食）・抗菌薬使用歴・ストレス要因を聴取。糞便量減少・食欲低下の経過を確認。"
        "鑑別：GI stasis、盲腸捻転、腸閉塞。モルモットは大きな盲腸を持ち、繊維発酵に依存するため食事管理が重要。"
    )
}

# guinea_pig_0028 Gastric Ulcer
ENRICHMENTS["guinea_pig_0028"] = {
    "diagnosis_ja": (
        "臨床徴候（食欲不振・歯ぎしり・前屈姿勢・血便・メレナ）から疑診。腹部X線で胃拡張・遊離ガスを評価。"
        "腹部超音波で胃壁肥厚・腹水を確認。CBC（貧血——慢性出血性）・血液生化学（BUN上昇・低アルブミン）。"
        "糞便潜血検査。内視鏡検査は小型齧歯類では困難だが可能な施設もある。ビタミンC欠乏の評価。"
        "鑑別：GI stasis、腸閉塞、肝疾患、壊血病。NSAIDs投与歴・ストレス・不適切な食事が素因。"
    )
}

# guinea_pig_0029 Hepatic Lipidosis
ENRICHMENTS["guinea_pig_0029"] = {
    "diagnosis_ja": (
        "血液生化学で肝酵素上昇（ALT・AST・ALP・GGT）、高ビリルビン血症、低アルブミン血症を確認。"
        "腹部超音波で肝臓のびまん性高エコー輝度を評価（脂肪浸潤を示唆）。腹部X線で肝腫大。"
        "CBC（軽度貧血）。肝細胞診（超音波ガイド下FNA）で脂肪変性を細胞学的に確認。"
        "鑑別：胆管肝炎、肝腫瘍、中毒性肝障害。妊娠末期・肥満・食欲不振からの急性発症が典型的。ケトーシス合併に注意。"
    )
}

# guinea_pig_0030 Cholangiohepatitis
ENRICHMENTS["guinea_pig_0030"] = {
    "diagnosis_ja": (
        "血液生化学で肝酵素著明上昇（ALT・AST・ALP・GGT）、高ビリルビン血症を確認。CBC（好中球増多）。"
        "腹部超音波で胆管拡張・肝実質のエコー輝度変化・腹水を評価。肝臓FNA（超音波ガイド下）の細胞診。"
        "胆汁培養（穿刺吸引）で細菌感染を同定。尿検査（ビリルビン尿）。黄疸・食欲廃絶・体重減少の経過を聴取。"
        "鑑別：肝リピドーシス、肝腫瘍、中毒性肝障害、胆石症。確定診断は肝生検の病理組織検査。"
    )
}

# guinea_pig_0031 Intestinal Adenocarcinoma
ENRICHMENTS["guinea_pig_0031"] = {
    "diagnosis_ja": (
        "腹部超音波で腸管壁の限局性肥厚・腫瘤を確認。腹部X線で腸管閉塞像・腹水を評価。"
        "CBC・血液生化学（低アルブミン・貧血・肝酵素上昇は転移を示唆）。胸部X線で肺転移を精査。"
        "開腹による腫瘤の組織生検が確定診断。FNA細胞診（超音波ガイド下）で腺癌細胞を検出。"
        "鑑別：炎症性腸疾患、リンパ腫、腸管平滑筋腫、肉芽腫。高齢モルモットで慢性体重減少・下痢が主訴。"
    )
}

# guinea_pig_0032 Peritonitis
ENRICHMENTS["guinea_pig_0032"] = {
    "diagnosis_ja": (
        "腹部超音波で腹水の貯留・腸管壁肥厚・腹腔内膿瘍を確認。腹水穿刺・細胞診（変性好中球・細菌）で確定。"
        "腹水培養・感受性試験で原因菌を同定。CBC（著明な好中球増多・左方移動・毒性変化）・血液生化学（低アルブミン・BUN上昇）。"
        "腹部X線で腹腔内遊離ガス（消化管穿孔）・臓器変位を評価。全身状態（体温・脱水・ショック）の評価。"
        "鑑別：腸穿孔、子宮破裂、膿瘍破裂、腹腔内腫瘍。緊急手術の適応を迅速に判断。"
    )
}

# guinea_pig_0033 Megacolon
ENRICHMENTS["guinea_pig_0033"] = {
    "diagnosis_ja": (
        "腹部X線で結腸の著明な拡張・糞便貯留を確認（正常結腸径の2倍以上）。腹部触診で拡張結腸を触知。"
        "造影X線（バリウム通過試験）で結腸通過時間延長を評価。CBC・血液生化学（脱水・電解質異常）。"
        "生検で腸管神経叢の異常（神経節細胞減少・欠如）を確認——先天性（lethal white syndrome）vs 後天性。"
        "鑑別：便秘、盲腸便秘、腸閉塞、GI stasis。ローン×ローン交配（白色被毛・暗眼）の個体で先天性巨大結腸症が好発。"
    )
}

# guinea_pig_0034 Adenovirus Pneumonia
ENRICHMENTS["guinea_pig_0034"] = {
    "diagnosis_ja": (
        "胸部X線で間質性～気管支肺炎パターンを確認。鼻咽頭スワブ・気管洗浄液のPCRでアデノウイルスを検出。"
        "ウイルス分離（細胞培養）。血清学的検査（ペア血清でIgG 4倍以上上昇）。"
        "CBC（リンパ球減少・好中球増多）・血液生化学。聴診で呼吸音異常を評価。"
        "鑑別：細菌性肺炎（Bordetella, Streptococcus）、マイコプラズマ肺炎、センダイウイルス。免疫抑制個体で重症化。"
    )
}

# guinea_pig_0035 Sendai Virus Infection
ENRICHMENTS["guinea_pig_0035"] = {
    "diagnosis_ja": (
        "鼻咽頭スワブのRT-PCRでセンダイウイルス（パラインフルエンザ1型）RNAを検出。血清学的検査（ELISA・HI法）。"
        "胸部X線で間質性肺炎パターンを評価。CBC（リンパ球減少）・血液生化学。"
        "聴診で呼吸音異常（湿性ラ音・喘鳴）を確認。鼻汁・くしゃみ・呼吸困難の経過を聴取。"
        "鑑別：アデノウイルス肺炎、細菌性肺炎、マイコプラズマ。研究施設のコロニー管理で重要（定期血清モニタリング）。"
    )
}

# guinea_pig_0036 Mycoplasma Pneumonia
ENRICHMENTS["guinea_pig_0036"] = {
    "diagnosis_ja": (
        "気管洗浄液・鼻腔スワブのPCRでMycoplasma spp.を検出。特殊培地（PPLO培地）での培養（増殖遅延に注意）。"
        "胸部X線で間質性～気管支肺炎パターンを評価。CBC（軽度好中球増多）・血液生化学。"
        "聴診で両側肺の捻髪音・喘鳴を確認。慢性経過の鼻汁・くしゃみ・体重減少を聴取。"
        "鑑別：Bordetella肺炎、Streptococcus pneumoniae、アデノウイルス。細胞壁欠如のためペニシリン系は無効（かつ腸管毒性で禁忌）。"
    )
}

# guinea_pig_0037 Upper Respiratory Infection (URI)
ENRICHMENTS["guinea_pig_0037"] = {
    "diagnosis_ja": (
        "鼻汁の性状（漿液性→粘液膿性）を視診。頭部X線で副鼻腔内液体貯留・鼻甲介変形を評価。"
        "鼻腔スワブの細菌培養・感受性試験（Bordetella, Streptococcus, Pasteurellaが主要病原体）。"
        "CBC（好中球増多）・血液生化学。聴診で上気道の狭窄音・喘鳴を確認。眼脂・結膜炎の併発を評価。"
        "鑑別：下気道感染（肺炎）、歯科疾患に伴う鼻腔瘻、アレルギー性鼻炎。ペニシリン系禁忌のため安全な抗菌薬を選択。"
    )
}

# guinea_pig_0038 Rhinitis
ENRICHMENTS["guinea_pig_0038"] = {
    "diagnosis_ja": (
        "鼻汁の視診（片側性 vs 両側性、漿液性 vs 粘液膿性）。頭部X線で鼻腔・副鼻腔の液体貯留を確認。"
        "CT推奨（歯根膿瘍による鼻腔浸潤の精査）。鼻腔スワブの細菌培養・感受性試験。"
        "CBC（好中球増多）・血液生化学。口腔内検査で上顎臼歯根尖の異常を除外。"
        "鑑別：副鼻腔炎、上顎臼歯根尖膿瘍、アレルギー、鼻腔内異物、肺炎からの鼻汁。くしゃみの頻度・鼻出血の有無を記録。"
    )
}

# guinea_pig_0039 Sinusitis
ENRICHMENTS["guinea_pig_0039"] = {
    "diagnosis_ja": (
        "頭部X線で副鼻腔内の液体貯留・骨溶解を確認。CT検査で副鼻腔壁の破壊・歯根との関連を精査（推奨）。"
        "鼻腔スワブまたは副鼻腔穿刺液の細菌培養・感受性試験。CBC（好中球増多）・血液生化学。"
        "口腔内検査で上顎臼歯過長・歯根膿瘍を除外（歯性副鼻腔炎が多い）。片側性鼻汁に注目。"
        "鑑別：鼻炎、鼻腔内腫瘍、歯根膿瘍、真菌性鼻炎。慢性例は骨溶解・顔面変形を呈することがある。"
    )
}

# guinea_pig_0040 Aspiration Pneumonia
ENRICHMENTS["guinea_pig_0040"] = {
    "diagnosis_ja": (
        "胸部X線で腹側肺葉（右中葉・左前葉）の浸潤影を確認——重力依存性分布が特徴。"
        "気管洗浄液の細胞診（変性好中球・細菌・食物残渣）・細菌培養・感受性試験。"
        "CBC（好中球増多・左方移動）・血液生化学。動脈血ガス分析（低酸素血症の評価）。"
        "誤嚥の誘因精査：強制給餌の手技、口腔内疾患、意識障害、巨大食道。鑑別：細菌性肺炎、肺水腫、肺腫瘍。"
    )
}

# guinea_pig_0041 Pulmonary Edema
ENRICHMENTS["guinea_pig_0041"] = {
    "diagnosis_ja": (
        "胸部X線で肺野のびまん性間質～肺胞パターン（心原性：背尾側分布、非心原性：びまん性）を評価。"
        "心臓超音波検査で心拡大・弁逆流・収縮能低下を確認（心原性肺水腫の鑑別）。"
        "CBC・血液生化学（BNP相当指標なし——臨床徴候で判断）。動脈血ガス分析（低酸素血症）。"
        "鑑別：細菌性肺炎、胸水、肺腫瘍、アナフィラキシー。呼吸困難・チアノーゼ・開口呼吸は緊急対応。"
    )
}

# guinea_pig_0042 Pleural Effusion
ENRICHMENTS["guinea_pig_0042"] = {
    "diagnosis_ja": (
        "胸部X線で胸腔内液体貯留（肺葉間裂の拡大・横隔膜ラインの不明瞭化）を確認。"
        "胸部超音波で胸水量・性状・心タンポナーデの有無を評価。胸腔穿刺による胸水採取が診断的かつ治療的。"
        "胸水分析：細胞診・蛋白濃度・比重・LDH（漏出液 vs 滲出液 vs 乳糜 vs 膿胸の鑑別）。胸水培養。"
        "CBC・血液生化学。鑑別：心不全、感染性胸膜炎、胸腔内腫瘍、外傷性血胸。心臓超音波で心疾患を精査。"
    )
}

# guinea_pig_0043 Heat Stroke
ENRICHMENTS["guinea_pig_0043"] = {
    "diagnosis_ja": (
        "直腸温測定（>40.5℃で確定）——モルモットの正常体温は37.2–39.5℃。環境温度・湿度の記録。"
        "CBC・血液生化学（肝酵素上昇・腎機能低下・電解質異常・高乳酸血症）。凝固検査（DIC合併の評価）。"
        "尿検査（ミオグロビン尿・蛋白尿）。心電図（不整脈の検出）。神経学的検査（意識レベル・痙攣・昏睡）。"
        "鑑別：感染性発熱、中毒、てんかん。モルモットは暑熱耐性が極めて低い（適温18–24℃）。30℃以上で高リスク。"
    )
}

# guinea_pig_0044 Lung Tumor
ENRICHMENTS["guinea_pig_0044"] = {
    "diagnosis_ja": (
        "胸部X線（3方向）で肺野の結節性・腫瘤性陰影を確認。CT検査で腫瘤のサイズ・浸潤範囲・リンパ節転移を精査。"
        "超音波ガイド下FNA（経胸壁）の細胞診で腫瘍細胞型を推定。気管洗浄液の細胞診。"
        "CBC・血液生化学。腹部超音波・X線で遠隔転移（肝臓・脾臓）を精査。"
        "鑑別：細菌性肺炎、肺膿瘍、転移性腫瘍、肉芽腫。原発性肺腫瘍はモルモットでは稀——転移性を先に除外。"
    )
}

# guinea_pig_0045 Molar Elongation
ENRICHMENTS["guinea_pig_0045"] = {
    "diagnosis_ja": (
        "無麻酔下での口腔内視診（頬拡張器・耳鏡使用）で臼歯の過長・舌側/頬側の棘状突起を確認。"
        "頭部X線（側面・正面）で臼歯の歯冠過長・歯根伸長・下顎骨変形を評価。CT推奨（重症例）。"
        "流涎・食欲低下・体重減少・食物選り好みの経過を聴取。舌の損傷（舌側棘）・頬粘膜潰瘍（頬側棘）を確認。"
        "鑑別：切歯過長、歯根膿瘍、口腔内腫瘍、壊血病。常生歯の特性上、定期的なトリミング（2–4週毎）が必要。"
    )
}

# guinea_pig_0046 Incisor Overgrowth
ENRICHMENTS["guinea_pig_0046"] = {
    "diagnosis_ja": (
        "視診で切歯の過長・咬合不良を確認（上下切歯の咬合角度・長さ・対称性を評価）。"
        "頭部X線で切歯歯根の湾曲・鼻腔内浸潤・歯根膿瘍を評価。臼歯の咬合も同時に精査（連動して異常を生じるため）。"
        "食欲不振・流涎・体重減少の経過を聴取。口唇の損傷・食物把持困難を確認。"
        "鑑別：臼歯過長（多くの場合併発）、外傷性破折、壊血病（歯肉炎）、顎骨骨髄炎。常生歯のためトリミングで管理。"
    )
}

# guinea_pig_0047 Dental Abscess
ENRICHMENTS["guinea_pig_0047"] = {
    "diagnosis_ja": (
        "頭部X線で歯根周囲の骨溶解・歯根膿瘍を確認。CT検査推奨（膿瘍の範囲・副鼻腔浸潤の精査）。"
        "顎部腫脹の触診（波動性・硬結性）。穿刺吸引液の細胞診（変性好中球・細菌）・培養・感受性試験。"
        "口腔内検査で原因歯の同定（臼歯根尖膿瘍が最多）。CBC（好中球増多）・血液生化学。"
        "鑑別：顎骨骨髄炎、皮下膿瘍（咬傷由来）、口腔内腫瘍。モルモットの膿は固形で排膿困難——外科的掻爬が必要。"
    )
}

# guinea_pig_0048 Periapical Abscess
ENRICHMENTS["guinea_pig_0048"] = {
    "diagnosis_ja": (
        "頭部X線で歯根尖周囲の透過性病変（骨溶解像）を確認。CT検査で膿瘍のサイズ・隣接構造への波及を精査。"
        "上顎臼歯根尖膿瘍は鼻腔浸潤・眼球突出・鼻涙管閉塞を引き起こす。下顎臼歯根尖は下顎腹側の腫脹を呈する。"
        "穿刺吸引液の培養・感受性試験（嫌気性菌を含む）。CBC（好中球増多）・血液生化学。"
        "鑑別：顎骨骨髄炎、歯根嚢胞、腫瘍。モルモットの膿は乾酪状で排膿しにくいため外科的デブリードマンが標準治療。"
    )
}

# guinea_pig_0049 Jaw Osteomyelitis
ENRICHMENTS["guinea_pig_0049"] = {
    "diagnosis_ja": (
        "頭部X線で顎骨の骨溶解・骨膜反応・歯根異常を確認。CT検査推奨（病変範囲の正確な評価）。"
        "骨生検の病理組織検査で確定（慢性化膿性骨髄炎の所見）。骨培養・感受性試験（嫌気性菌含む）。"
        "CBC（好中球増多・慢性炎症パターン）・血液生化学（CRP相当指標・低アルブミン）。"
        "鑑別：歯根膿瘍、骨腫瘍（骨肉腫）、真菌性骨髄炎。歯科疾患からの二次感染が最多原因。長期抗菌薬治療が必要。"
    )
}

# guinea_pig_0050 Broken Tooth
ENRICHMENTS["guinea_pig_0050"] = {
    "diagnosis_ja": (
        "口腔内視診で破折歯を同定（切歯は直接観察、臼歯は頬拡張器・耳鏡使用）。破折のタイプ分類（歯冠/歯根破折）。"
        "頭部X線で歯根破折・歯槽骨損傷・歯根膿瘍の有無を評価。対合歯の過長リスクを確認。"
        "出血・食欲不振・流涎の有無を聴取。露髄の有無を確認（感染リスク）。CBC・血液生化学（感染合併時）。"
        "鑑別：不正咬合、歯根膿瘍、顎骨骨折。常生歯のため歯冠破折は再生する場合もあるが咬合管理が必須。"
    )
}


def apply_enrichments() -> None:
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for entry in data:
        eid = entry.get("id")
        if eid in ENRICHMENTS:
            for k, v in ENRICHMENTS[eid].items():
                entry[k] = v
            updated += 1

    missing = set(ENRICHMENTS) - {e.get("id") for e in data}
    if missing:
        print(f"WARNING: {len(missing)} IDs not found: {sorted(missing)}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated}/{len(ENRICHMENTS)} entries")


if __name__ == "__main__":
    apply_enrichments()
