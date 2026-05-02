#!/usr/bin/env python3
"""Enrich diagnosis_ja for the first 50 Reptile diseases with disease-specific
diagnostic protocols. Each entry uses reptile-specific terminology (heterophils,
POTZ, renal portal system, iCa, etc.) and is 150-400 characters."""

import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# reptile_0001: Atadenovirus Infection / アタデノウイルス感染
ENRICHMENTS["reptile_0001"] = {
    "diagnosis_ja": (
        "口腔・総排泄腔スワブPCR（アタデノウイルス特異的プライマー）が確定診断の第一選択。"
        "CBC（ヘテロフィル減少・リンパ球減少は免疫抑制を示唆）、血液生化学（AST・UA上昇で肝・腎障害評価）。"
        "肝生検の封入体検出（好塩基性核内封入体）が病理確定所見。POTZ内での採血が必須。"
        "血清学的抗体検査は集団スクリーニングに有用。剖検では肝壊死・脾腫が特徴的。"
    )
}

# reptile_0002: Yellow Fungus Disease (Chrysosporium)
ENRICHMENTS["reptile_0002"] = {
    "diagnosis_ja": (
        "皮膚病変部の圧挫標本・細胞診で分岐する菌糸・分節型分生子を確認。"
        "真菌培養（25-30℃、SDA培地、2-4週間）でChryosporium anamorph of Nannizziopsis vriesiiを同定。"
        "PCR（ITS領域）による分子生物学的種同定が確定診断に推奨。"
        "皮膚生検・病理でPAS/GMS染色陽性の菌糸侵入を確認。CBC（ヘテロフィル増多→全身性炎症）、"
        "血液生化学（低アルブミン→慢性消耗）。X線・CTで深部組織・骨浸潤の評価。"
    )
}

# reptile_0003: Nannizziopsis Infection
ENRICHMENTS["reptile_0003"] = {
    "diagnosis_ja": (
        "病変部皮膚の直接鏡検（KOH処理）で太い隔壁菌糸と節分生子を観察。"
        "真菌培養（SDA/DTM培地、25-30℃）で白色〜黄色コロニーを確認、顕微鏡的形態でNannizziopsis属を同定。"
        "PCR（ITS・LSU領域）による分子同定が種レベルの確定に必須。"
        "皮膚生検でGMS/PAS染色陽性の真菌侵入と肉芽腫性炎症。"
        "CBC（ヘテロフィル増多）、生化学（CK上昇→筋浸潤時）。POTZ管理下で全身状態を評価。"
    )
}

# reptile_0004: Ophidiomyces Infection (Snake Fungal Disease)
ENRICHMENTS["reptile_0004"] = {
    "diagnosis_ja": (
        "顔面・体幹の痂皮形成・鱗下結節からのスワブPCR（Ophidiomyces ophidiicola特異的）が第一選択。"
        "皮膚生検で真皮深層への菌糸浸潤、肉芽腫性〜壊死性皮膚炎を確認（PAS/GMS染色）。"
        "真菌培養（SDA培地、24℃、3-4週間）で黄色コロニー。"
        "CBC（ヘテロフィル増多・単球増加→慢性炎症）、血液生化学で全身状態評価。"
        "眼瞼癒着・鼻孔閉塞の有無を視診で確認。"
    )
}

# reptile_0005: Septicemic Cutaneous Ulcerative Disease
ENRICHMENTS["reptile_0005"] = {
    "diagnosis_ja": (
        "皮膚潰瘍部の培養・感受性試験（好気・嫌気培養）でグラム陰性桿菌（Citrobacter、Aeromonas等）を同定。"
        "血液培養（敗血症評価）。CBC（ヘテロフィル増多・毒性変化→重症度指標）。"
        "血液生化学（UA・AST上昇→腎・肝障害、低アルブミン→敗血症性消耗）。"
        "皮膚生検で壊死性血管炎・細菌塊を病理確認。POTZ内で採血し、脱水補正後に評価。"
        "甲羅・鱗の潰瘍分布パターンから水質環境因子を推定。"
    )
}

# reptile_0006: Necrotic Dermatitis
ENRICHMENTS["reptile_0006"] = {
    "diagnosis_ja": (
        "壊死組織の圧挫標本・細胞診で変性ヘテロフィル・細菌塊を確認。"
        "病変部の好気・嫌気培養＋感受性試験でグラム陰性桿菌（Pseudomonas、Aeromonas等）を同定。"
        "皮膚生検で表皮全層壊死・真皮血管炎・細菌侵入を病理評価。"
        "CBC（ヘテロフィル増多・左方移動→急性炎症）、血液生化学（CK上昇→筋壊死波及、UA→腎機能）。"
        "飼育環境（温度・湿度・基材）の不適切さが誘因となるため環境歴の聴取が重要。"
    )
}

# reptile_0007: Nutritional Secondary Hyperparathyroidism
ENRICHMENTS["reptile_0007"] = {
    "diagnosis_ja": (
        "血液生化学でiCa低値（＜1.0 mmol/L）・総Ca低値・P高値・Ca:P比逆転（正常1.5-2:1）が特徴的。"
        "X線で全身性の骨密度低下・病的骨折・線維性骨異栄養症（顎骨膨化＝ラバージョー）を評価。"
        "PTH測定（上昇）で副甲状腺機能亢進を確認。25(OH)D3測定でUVB曝露不足を評価。"
        "食餌歴の詳細聴取（Ca:P比、UVB照射時間、ビタミンD3サプリメント使用状況）が診断に不可欠。"
        "POTZ管理下での採血が正確な結果に必須。"
    )
}

# reptile_0008: Renal Secondary Hyperparathyroidism
ENRICHMENTS["reptile_0008"] = {
    "diagnosis_ja": (
        "血液生化学でUA上昇（爬虫類の主要窒素排泄物）・P上昇・iCa低値・Ca:P比逆転が特徴。"
        "尿酸塩結晶の関節・内臓沈着（二次性痛風）をX線・超音波で評価。"
        "腎臓超音波で腎腫大・実質エコー輝度上昇を確認。PTH上昇（測定可能な場合）。"
        "X線で骨密度低下・線維性骨異栄養症を評価。腎生検で尿細管変性・間質性腎炎・尿酸塩沈着を確認。"
        "脱水補正後の再検査で腎前性と腎性の鑑別を行う。"
    )
}

# reptile_0009: Hypovitaminosis A
ENRICHMENTS["reptile_0009"] = {
    "diagnosis_ja": (
        "臨床診断が主体：眼瞼浮腫（カメ類で特徴的な両側性眼瞼腫脹）、口腔粘膜の扁平上皮化生を視診。"
        "食餌歴聴取（ビタミンA前駆体不足：レタス主体飼育等）が診断の鍵。"
        "細胞診で口腔・結膜の扁平上皮化生（角化亢進）を確認。"
        "血漿レチノール測定（低値）が可能な場合は確定的。CBC（ヘテロフィル増多→二次感染）。"
        "二次的呼吸器感染の評価にX線撮影。治療的診断としてビタミンA投与への反応を評価。"
    )
}

# reptile_0010: Thiamine Deficiency
ENRICHMENTS["reptile_0010"] = {
    "diagnosis_ja": (
        "食餌歴の聴取が最重要：冷凍魚の長期給餌（チアミナーゼ含有）や単一食餌が誘因。"
        "神経学的検査で斜頸・眼振・運動失調・opisthotonusを評価。"
        "血中チアミン（ビタミンB1）測定が可能であれば低値を確認。"
        "赤血球トランスケトラーゼ活性測定（TPP効果＞25%で欠乏確定）。"
        "治療的診断：チアミン投与（25-100 mg/kg IM）後24-48時間以内の神経症状改善で臨床的に確定。"
        "MRI（利用可能な場合）で脳幹病変を評価。POTZ管理下での評価が必須。"
    )
}

# reptile_0011: Biotin Deficiency
ENRICHMENTS["reptile_0011"] = {
    "diagnosis_ja": (
        "食餌歴の聴取：生卵白の過剰給餌（アビジンによるビオチン結合）が最も一般的な原因。"
        "皮膚症状（脱皮異常・鱗の変色・皮膚炎）と食餌内容の相関で臨床診断。"
        "血漿ビオチン測定（低値確認、ただし爬虫類の基準値は確立されていない）。"
        "皮膚生検で表皮の過角化・錯角化を確認。CBC・血液生化学で全身状態評価。"
        "治療的診断：ビオチン補充と食餌改善（生卵白除去）への反応で確定。"
        "鑑別診断として真菌性皮膚炎・脱皮不全・ビタミンA欠乏との区別が必要。"
    )
}

# reptile_0012: Metabolic Bone Disease (MBD)
ENRICHMENTS["reptile_0012"] = {
    "diagnosis_ja": (
        "X線で全身性骨密度低下（骨皮質菲薄化）・病的骨折・顎骨の線維性骨異栄養症を評価。"
        "血液生化学でiCa低値（＜1.0 mmol/L、総Caでなくイオン化Caが必須）・P上昇・ALP上昇を確認。"
        "Ca:P比の逆転（正常1.5-2:1→1:1以下）が特徴的。PTH上昇（測定可能時）。"
        "25(OH)D3測定でUVB曝露不足を評価。飼育環境詳細聴取（UVB光源の種類・距離・交換頻度、Ca:Pサプリメント、食餌構成）。"
        "POTZ内（種適温）での採血が正確な血液データに必須。"
    )
}

# reptile_0013: Respiratory Infection
ENRICHMENTS["reptile_0013"] = {
    "diagnosis_ja": (
        "視診で口呼吸・鼻汁・頭部挙上・開口呼吸・気管音（ヘビでのwheezing）を評価。"
        "X線（DV・lateral）で肺野混濁・エアブロンコグラム・気嚢壁肥厚を確認。"
        "気管洗浄液の細胞診（ヘテロフィル増多・細菌/真菌体）＋培養・感受性試験。"
        "CBC（ヘテロフィル増多＋毒性変化→細菌性、リンパ球増加→ウイルス性示唆）。"
        "PCR（パラミクソウイルス・ニドウイルス・マイコプラズマ等の特異的検査）。"
        "POTZ管理下評価。環境温度・湿度の不適が誘因となるため飼育環境歴聴取必須。"
    )
}

# reptile_0014: Stomatitis (Mouth Rot)
ENRICHMENTS["reptile_0014"] = {
    "diagnosis_ja": (
        "口腔内視診で歯肉・口腔粘膜の充血・点状出血・乾酪様壊死物（黄白色）を確認。"
        "重症度分類：Grade I（点状出血のみ）→Grade III（骨露出・顎骨溶解）。"
        "口腔スワブの細菌培養・感受性試験（Pseudomonas、Aeromonas等のグラム陰性桿菌が多い）。"
        "CBC（ヘテロフィル増多→細菌感染の重症度指標）。頭部X線で顎骨の骨溶解・骨髄炎を評価。"
        "基礎疾患（免疫抑制・POTZ逸脱・ストレス）の評価が再発防止に重要。"
    )
}

# reptile_0015: Inclusion Body Disease (IBD)
ENRICHMENTS["reptile_0015"] = {
    "diagnosis_ja": (
        "ボア・パイソンの神経症状（stargazing、協調運動障害、正向反射消失）が臨床的に強く示唆。"
        "肝・腎・膵臓の生検でエオジン好性〜好塩基性の大型細胞質内封入体をH&E染色で確認（確定診断）。"
        "食道扁桃・末梢血白血球の封入体検出が低侵襲スクリーニング法（感度限定的）。"
        "CBC（リンパ球減少→免疫抑制）、血液生化学（AST・UA上昇→肝腎障害）。"
        "PCR（アレナウイルス検出）が補助診断。X線で消化管異常ガス像。"
        "確定には剖検が最も信頼性が高い。"
    )
}

# reptile_0016: Cryptosporidiosis
ENRICHMENTS["reptile_0016"] = {
    "diagnosis_ja": (
        "糞便の酸抗染色（modified Ziehl-Neelsen）でオーシスト（4-6μm）検出。"
        "胃洗浄液の酸抗染色・PCR（Cryptosporidium serpentis→胃、C. varanii→腸）が種同定に有用。"
        "X線・造影検査で胃壁肥厚（ヘビの中部体幹腫大）を評価。"
        "胃・腸粘膜生検でクリプトスポリジウム虫体と粘膜肥厚を病理確認。"
        "CBC（ヘテロフィル増多は限定的）、血液生化学（低蛋白→慢性消耗）。"
        "ELISA・IFA法による抗原検出も利用可能。感染個体の隔離と環境消毒計画が必須。"
    )
}

# reptile_0017: Paramyxovirus
ENRICHMENTS["reptile_0017"] = {
    "diagnosis_ja": (
        "ヘビ類の神経症状（stargazing、正向反射消失、フリッキング異常）＋呼吸器症状が臨床的に示唆。"
        "口腔・気管スワブPCR（パラミクソウイルス特異的）が生前診断の第一選択。"
        "血清学的HI試験（赤血球凝集抑制試験）でペア血清の抗体価上昇を確認。"
        "CBC（リンパ球減少→ウイルス性免疫抑制）、血液生化学。"
        "X線で肺野混濁。気管洗浄液の細胞診で封入体を検索。"
        "剖検では肺・脳のウイルス性封入体とHE染色所見が確定的。集団発生時は全頭検査。"
    )
}

# reptile_0018: Adenovirus Infection
ENRICHMENTS["reptile_0018"] = {
    "diagnosis_ja": (
        "肝臓・消化管の生検で好塩基性核内封入体（カウドリーA型）をH&E染色で確認（確定診断）。"
        "PCR（アデノウイルス特異的プライマー、口腔・総排泄腔スワブ）が生前診断に有用。"
        "CBC（ヘテロフィル減少・リンパ球減少→免疫抑制状態）。"
        "血液生化学（AST・LDH著明上昇→肝壊死、UA上昇→腎障害）。"
        "X線・超音波で肝腫大を評価。剖検で肝臓の多巣性壊死・腸炎が特徴的所見。"
        "POTZ管理下での採血と全身状態評価が必須。"
    )
}

# reptile_0019: Herpesvirus Infection
ENRICHMENTS["reptile_0019"] = {
    "diagnosis_ja": (
        "カメ類の口腔内白色プラーク・壊死性口内炎・鼻汁が臨床的に強く示唆。"
        "口腔スワブPCR（ヘルペスウイルス特異的）が生前確定診断の第一選択。"
        "口腔粘膜の細胞診で好酸性核内封入体（カウドリーA型）を検索。"
        "皮膚・粘膜生検でH&E染色による封入体確認と壊死性炎症の病理評価。"
        "CBC（ヘテロフィル増多→二次感染、リンパ球減少→ウイルス免疫抑制）。"
        "血液生化学で肝機能評価。ウイルス分離（細胞培養）は研究機関限定。"
    )
}

# reptile_0020: Nidovirus Infection
ENRICHMENTS["reptile_0020"] = {
    "diagnosis_ja": (
        "パイソン類の増殖性肺炎・口腔内粘液過多が臨床的に示唆。"
        "口腔・気管スワブのRT-PCR（ニドウイルス特異的）が確定診断の第一選択。"
        "X線で肺野のびまん性混濁・気嚢壁肥厚を評価。"
        "気管洗浄液の細胞診（ヘテロフィル・マクロファージ増多）＋培養（二次細菌感染評価）。"
        "CBC（ヘテロフィル増多→二次感染、単球増加→慢性炎症）。"
        "肺生検でII型肺胞上皮の増殖性変化が病理的特徴。POTZ管理下での評価必須。"
    )
}

# reptile_0021: Iridovirus (Ranavirus)
ENRICHMENTS["reptile_0021"] = {
    "diagnosis_ja": (
        "急性の全身性出血・浮腫・皮膚壊死が臨床的に示唆（カメ・トカゲで多い）。"
        "PCR（ラナウイルスMCP遺伝子）が生前確定診断に最も有用。"
        "CBC（ヘテロフィル減少・血小板減少→汎血球減少症）、血液生化学（AST・LDH上昇→多臓器障害）。"
        "肝・脾・腎の生検で好塩基性細胞質内封入体を確認。"
        "ウイルス分離（FHM・VERO細胞）は研究施設限定。剖検で肝脾壊死・出血が特徴的。"
        "集団死亡例では複数検体のPCRスクリーニングが疫学管理に重要。"
    )
}

# reptile_0022: Mycoplasma Infection
ENRICHMENTS["reptile_0022"] = {
    "diagnosis_ja": (
        "リクガメの慢性上部呼吸器症状（漿液性〜粘液膿性鼻汁、結膜炎）が臨床的に示唆。"
        "鼻腔スワブPCR（Mycoplasma agassizii / M. testudineum特異的）が確定診断の標準法。"
        "血清ELISA（抗マイコプラズマ抗体）は集団スクリーニングに有用（ペア血清推奨）。"
        "CBC（ヘテロフィル増多→二次細菌感染合併時）。X線で鼻腔骨溶解を評価。"
        "培養は特殊培地（SP4）で長期培養が必要なため一般臨床では困難。"
        "POTZ管理下での採血と脱水状態の補正後評価が正確な結果に必須。"
    )
}

# reptile_0023: Salmonellosis
ENRICHMENTS["reptile_0023"] = {
    "diagnosis_ja": (
        "糞便の直接培養（SS寒天・XLD培地等）でSalmonella属を分離同定。"
        "血清型別（Kauffmann-White分類）で疫学的解析。PCRによる迅速検出も利用可能。"
        "血液培養（敗血症疑い時）。薬剤感受性試験で治療薬選択。"
        "CBC（ヘテロフィル増多→急性炎症、毒性変化→敗血症）。"
        "血液生化学（UA上昇→腎障害、AST上昇→肝障害、低アルブミン→敗血症性消耗）。"
        "人獣共通感染症であり、飼育者への感染リスク評価・衛生指導が診断時に必須。"
    )
}

# reptile_0024: Pseudomonas Infection
ENRICHMENTS["reptile_0024"] = {
    "diagnosis_ja": (
        "病変部（皮膚潰瘍・膿瘍・口腔・呼吸器）からの好気培養で緑色色素産生のグラム陰性桿菌を分離。"
        "薬剤感受性試験が治療薬選択に必須（多剤耐性株が多い）。"
        "気管洗浄液の培養・細胞診（ヘテロフィル主体の化膿性炎症、細胞内細菌）。"
        "CBC（ヘテロフィル増多＋毒性変化→重症感染）、血液生化学（UA→腎機能評価）。"
        "水質・湿度過多など環境因子の評価。POTZ逸脱が免疫低下→日和見感染の誘因。"
    )
}

# reptile_0025: Aeromonas Infection
ENRICHMENTS["reptile_0025"] = {
    "diagnosis_ja": (
        "皮膚潰瘍・体腔液からの培養（血液寒天37℃好気培養）でAeromonas属（A. hydrophila等）を分離。"
        "薬剤感受性試験で治療薬選択（β-ラクタマーゼ産生株に注意）。"
        "血液培養（敗血症評価）。CBC（ヘテロフィル増多＋毒性変化→急性細菌感染）。"
        "血液生化学（UA上昇→腎機能、AST→肝障害、低蛋白→敗血症）。"
        "水棲・半水棲種で多く、水質検査（アンモニア・亜硝酸・pH）が環境因子として重要。"
        "皮膚生検で壊死性血管炎を確認。"
    )
}

# reptile_0026: Mycobacteriosis
ENRICHMENTS["reptile_0026"] = {
    "diagnosis_ja": (
        "病変部（肉芽腫・皮膚結節）の抗酸菌染色（Ziehl-Neelsen）で抗酸菌体を検出。"
        "培養（Löwenstein-Jensen培地・液体培養、4-12週間）で菌種同定。"
        "PCR（16S rRNA・hsp65遺伝子）による迅速な分子同定が推奨。"
        "病理組織検査で多核巨細胞を伴う肉芽腫性炎症を確認。"
        "CBC（単球増加→慢性肉芽腫性炎症）、血液生化学（低アルブミン→慢性消耗）。"
        "X線・CTで内臓肉芽腫・骨病変を評価。人獣共通感染リスクの評価が必須。"
    )
}

# reptile_0027: Chlamydiosis
ENRICHMENTS["reptile_0027"] = {
    "diagnosis_ja": (
        "結膜・鼻腔・総排泄腔スワブのPCR（Chlamydia特異的）が生前確定診断の第一選択。"
        "細胞診で上皮細胞質内の好塩基性封入体（Giemsa染色）を検索。"
        "血清学（CFT・ELISA）で抗体検出。ペア血清の抗体価4倍以上上昇で活動性感染を示唆。"
        "CBC（ヘテロフィル増多→急性感染、単球増加→慢性化）。"
        "X線で肝脾腫・気嚢炎を評価。肝生検で肉芽腫性肝炎・封入体確認が確定的。"
        "人獣共通感染症の可能性があり取扱い注意。"
    )
}

# reptile_0028: Dermatophytosis
ENRICHMENTS["reptile_0028"] = {
    "diagnosis_ja": (
        "鱗・皮膚病変部の直接鏡検（KOH処理）で菌糸・分節胞子を観察。"
        "真菌培養（DTM/SDA培地、25-30℃、2-3週間）で皮膚糸状菌（Trichophyton、Microsporum等）を分離。"
        "Wood灯検査（M. canisの一部株のみ蛍光陽性、感度限定的）。"
        "皮膚生検でPAS染色陽性の角質内菌糸・胞子を確認。"
        "鑑別診断として脱皮不全・細菌性皮膚炎・Nannizziopsis感染・ビタミンA欠乏を除外。"
        "POTZ管理下で免疫状態を評価。"
    )
}

# reptile_0029: Aspergillosis
ENRICHMENTS["reptile_0029"] = {
    "diagnosis_ja": (
        "呼吸器症状のある個体でX線・CTにより肺野結節影・気嚢壁肥厚・骨溶解を評価。"
        "気管洗浄液の細胞診でY字分岐する隔壁菌糸を直接確認。"
        "培養（SDA培地、37℃）で特徴的なコロニー形態とコニディア形成を確認しAspergillus属を同定。"
        "血清ガラクトマンナン抗原検査が侵襲性アスペルギルス症の補助診断に有用。"
        "CBC（ヘテロフィル増多→炎症、単球増加→肉芽腫形成）。"
        "POTZ逸脱による免疫抑制状態の確認が背景因子の評価に重要。"
    )
}

# reptile_0030: Candidiasis
ENRICHMENTS["reptile_0030"] = {
    "diagnosis_ja": (
        "口腔・消化管粘膜の白色偽膜状プラークが臨床的に特徴的。"
        "直接鏡検（KOH処理・グラム染色）で出芽酵母と偽菌糸を確認。"
        "培養（SDA培地・CHROMagar Candida）でCandida属を分離し、種同定。"
        "細胞診で多数の酵母細胞と炎症細胞（ヘテロフィル）を確認。"
        "CBC・血液生化学で全身状態評価。基礎疾患（免疫抑制・長期抗菌薬使用・POTZ逸脱）の検索が重要。"
        "胃腸管のX線造影で消化管粘膜の不整を評価。"
    )
}

# reptile_0031: Chrysosporium (CANV) Infection
ENRICHMENTS["reptile_0031"] = {
    "diagnosis_ja": (
        "皮膚の黄色〜褐色変色・壊死性痂皮から圧挫標本を作成し、KOH処理で太い菌糸を確認。"
        "真菌培養（SDA培地、24-30℃、2-4週間）でCANV特有の白〜黄色コロニー。"
        "PCR（ITS領域）でChryosporium anamorph of Nannizziopsis vriesiiを分子同定（確定診断）。"
        "皮膚生検でGMS/PAS染色陽性菌糸の深部侵入と肉芽腫性〜壊死性皮膚炎を確認。"
        "CBC（ヘテロフィル増多）、血液生化学（CK上昇→筋浸潤時、低アルブミン→慢性消耗）。"
    )
}

# reptile_0032: Mite Infestation (Ophionyssus)
ENRICHMENTS["reptile_0032"] = {
    "diagnosis_ja": (
        "肉眼的検査で鱗間・眼窩周囲・総排泄腔周囲に黒〜赤褐色のダニ（Ophionyssus natricis）を確認。"
        "水浸法（個体を温水に浸し浮遊するダニを回収）で虫体数を半定量評価。"
        "セロファンテープ法で鱗間のダニ卵・幼虫を採取し顕微鏡同定。"
        "CBC（ヘテロフィル増多→二次感染、貧血→重度寄生時の吸血による）。"
        "血液生化学で低蛋白・低アルブミン（慢性重度寄生時）。"
        "環境中のダニ生活環（卵→幼虫→成虫、ケージ内の隙間に産卵）の評価が再発防止に重要。"
    )
}

# reptile_0033: Tick Infestation
ENRICHMENTS["reptile_0033"] = {
    "diagnosis_ja": (
        "肉眼的検査で鱗間に付着するマダニ（Hyalomma、Amblyomma等）を同定。"
        "虫体の実体顕微鏡検査で種同定（顎体基部・盾板形態による分類）。"
        "CBC（ヘテロフィル増多→二次感染、貧血→重度吸血時）。"
        "ダニ媒介病原体（Hemogregarines、Ehrlichia等）のスクリーニングとして"
        "血液塗抹（赤血球内寄生体）・PCR検査を実施。"
        "刺咬部位の二次感染評価（細菌培養）。飼育環境の評価と野外採集個体の検疫プロトコル確認。"
    )
}

# reptile_0034: Nematode Infection
ENRICHMENTS["reptile_0034"] = {
    "diagnosis_ja": (
        "糞便検査（直接塗抹法・浮遊法・沈殿法）で線虫卵・幼虫を検出し形態同定。"
        "Strongyloides等は糞便中の幼虫（L1）を直接鏡検で確認。"
        "糞便のfecal flotation（比重1.18-1.20の飽和食塩水またはシュガー溶液）が推奨。"
        "X線・造影検査で腸管壁肥厚・閉塞所見（大量寄生時）を評価。"
        "CBC（好酸球増多→寄生虫感染の間接的指標、ただし爬虫類ではヘテロフィルが主体で好酸球反応は限定的）。"
        "剖検時に消化管・肺からの虫体回収・同定が確定的。"
    )
}

# reptile_0035: Cestode Infection
ENRICHMENTS["reptile_0035"] = {
    "diagnosis_ja": (
        "糞便検査（浮遊法・沈殿法）で条虫卵（六鉤幼虫含有の特徴的な厚い卵殻）を検出。"
        "片節（proglottid）の肉眼的確認が最も簡便な診断法。"
        "X線・造影検査で腸管内の条虫体を陰影欠損として描出（大型種）。"
        "CBC・血液生化学で全身状態評価（慢性感染時の低蛋白・低アルブミン）。"
        "虫体・片節の形態学的同定（頭節の吸盤・鈎の構造）で種同定。"
        "中間宿主（給餌昆虫・げっ歯類）の感染状況評価と給餌管理改善が再感染防止に重要。"
    )
}

# reptile_0036: Trematode Infection
ENRICHMENTS["reptile_0036"] = {
    "diagnosis_ja": (
        "糞便沈殿法（吸虫卵は比重が大きく浮遊法では検出困難）で蓋付き虫卵を検出。"
        "口腔・咽頭の直接観察で舌下〜咽頭部の吸虫体を肉眼確認（Ochetosomatidae等）。"
        "X線・超音波で肝臓・肺の吸虫嚢胞を評価。"
        "CBC（ヘテロフィル・好酸球増多→寄生虫反応）、血液生化学（AST上昇→肝実質障害）。"
        "病理組織検査で肝・肺・腎の肉芽腫内に吸虫体・虫卵を確認（確定診断）。"
        "飼育環境での中間宿主（巻貝）との接触歴の聴取が疫学的に重要。"
    )
}

# reptile_0037: Pentastomid Infection
ENRICHMENTS["reptile_0037"] = {
    "diagnosis_ja": (
        "X線で肺実質内のC字型〜S字型の石灰化虫体（成虫）を確認（特にヘビ類）。"
        "気管洗浄液中の虫卵（楕円形、4つの鉤を持つ幼虫含有）検出。"
        "口腔検査で鼻腔・気管開口部からの虫体頭部の突出を視認する場合あり。"
        "CBC（ヘテロフィル増多→炎症反応）。血液生化学で全身状態評価。"
        "内視鏡（気管鏡）で気管・肺内の虫体を直接観察。"
        "剖検時に肺・気管から虫体を回収し形態同定（Porocephalus、Armillifer等）。"
        "人獣共通感染の可能性があり取扱い注意。"
    )
}

# reptile_0038: Coccidia
ENRICHMENTS["reptile_0038"] = {
    "diagnosis_ja": (
        "糞便浮遊法（飽和食塩水・ショ糖液、比重1.18-1.20）でコクシジウムオーシスト検出。"
        "オーシスト形態（サイズ・形状・スポロシスト数）でEimeria、Isospora、Caryospora等を属レベルで同定。"
        "直接塗抹法による新鮮糞便検査で運動性虫体の確認。"
        "CBC（ヘテロフィル増多は限定的）、血液生化学（低蛋白→慢性下痢・吸収不良）。"
        "重度感染時は糞便中の粘血便・腸管粘膜片を細胞診で評価。"
        "連日検査（3日間連続採取）で検出感度向上。POTZ管理下での評価が必須。"
    )
}

# reptile_0039: Flagellate Protozoan Infection
ENRICHMENTS["reptile_0039"] = {
    "diagnosis_ja": (
        "新鮮糞便の直接塗抹鏡検（37℃加温生理食塩水）で運動性のある鞭毛虫体を確認。"
        "形態学的同定：Trichomonas（洋梨形、4鞭毛＋波動膜）、Hexamita/Spironucleus（左右対称、6鞭毛）。"
        "胃洗浄液の直接鏡検（上部消化管寄生種の検出に重要）。"
        "CBC・血液生化学で全身状態評価（慢性感染時の低蛋白・脱水）。"
        "PCR（種レベルの同定が必要な場合）。糞便検体は採取後速やかに検査（虫体の運動性消失を防ぐ）。"
        "POTZ管理下で評価し環境ストレスの関与を検討。"
    )
}

# reptile_0040: Amoebic Infection
ENRICHMENTS["reptile_0040"] = {
    "diagnosis_ja": (
        "新鮮糞便（37℃加温）の直接塗抹法でアメーバ栄養体（偽足運動）とシスト（二重壁・4核）を検出。"
        "トリクローム染色・PAS染色で栄養体内の貪食赤血球を確認（Entamoeba invadensの病原性指標）。"
        "肝臓超音波でアメーバ性膿瘍（低エコー域）を検索。"
        "CBC（ヘテロフィル増多→腸壁侵入時）、血液生化学（AST上昇→肝膿瘍、低アルブミン→慢性腸炎）。"
        "大腸生検でフラスコ状潰瘍とPAS陽性栄養体を確認。PCRでE. invadens同定。"
        "肉食爬虫類→草食爬虫類への感染伝播リスク評価が重要。"
    )
}

# reptile_0041: Dysecdysis (Retained Shed)
ENRICHMENTS["reptile_0041"] = {
    "diagnosis_ja": (
        "視診で残存脱皮片（眼鏡鱗のretained spectacle、指趾先端・尾先端の残存皮膚）を確認。"
        "実体顕微鏡で眼鏡鱗の重層（複数回分の脱皮不全蓄積）を評価。"
        "飼育環境歴聴取：湿度不足（＜50-60%）、脱皮用水入れ・隠れ家の有無、温度勾配の適切性。"
        "基礎疾患スクリーニング：CBC（ヘテロフィル増多→二次感染）、血液生化学（甲状腺機能・栄養状態）。"
        "皮膚のダニ寄生（Ophionyssus natricis）の除外検査。"
        "慢性脱皮不全では指趾壊死・眼鏡鱗下膿瘍の合併を評価。"
    )
}

# reptile_0042: Thermal Burns
ENRICHMENTS["reptile_0042"] = {
    "diagnosis_ja": (
        "飼育環境歴：熱源（ヒートランプ・ホットロック・ヒーティングパッド）との接触歴、サーモスタット故障の有無。"
        "熱傷の深度分類：表在性（鱗変色のみ）→深達性（真皮壊死・水疱）→全層性（筋・骨露出）。"
        "体表面積の評価（爬虫類での9の法則は適用不可、体表マッピングで推定）。"
        "CBC（ヘテロフィル増多→二次感染）、血液生化学（CK上昇→筋障害、低蛋白→重症熱傷の蛋白漏出）。"
        "病変部の細菌培養・感受性試験（二次感染評価）。"
        "X線で深部骨障害の有無を確認。POTZ管理下で体液バランスを評価。"
    )
}

# reptile_0043: Rostral Abrasion
ENRICHMENTS["reptile_0043"] = {
    "diagnosis_ja": (
        "視診で吻端（rostrum）の鱗損傷・擦過傷・出血・痂皮形成を確認。"
        "重症度評価：表在性擦過→深部潰瘍→骨露出（前上顎骨・鼻骨の損傷）。"
        "頭部X線で前上顎骨・鼻骨の骨折・骨溶解（慢性例）を評価。"
        "病変部の細菌培養（二次感染評価・Pseudomonas等）。"
        "飼育環境歴聴取：ケージサイズ不足、透明壁面への反復衝突（escape behavior）、"
        "視覚的ストレス源の有無。CBC（ヘテロフィル増多→感染）。"
        "慢性例では口腔内への深部波及を内視鏡で確認。"
    )
}

# reptile_0044: Blister Disease
ENRICHMENTS["reptile_0044"] = {
    "diagnosis_ja": (
        "腹側鱗の水疱・膨隆・透明〜混濁液貯留を視診で確認（腹部接地面に好発）。"
        "水疱液の細胞診（ヘテロフィル・細菌→感染性）と培養・感受性試験。"
        "皮膚生検で表皮下水疱・真皮の急性炎症・細菌侵入を病理確認。"
        "CBC（ヘテロフィル増多→全身性炎症波及）、血液生化学（低アルブミン→重症例の蛋白漏出）。"
        "飼育環境歴：基材の過湿（不衛生な水浸し状態）、温度不適、衛生管理状態が根本原因。"
        "進行例では敗血症リスク評価のため血液培養を追加。"
    )
}

# reptile_0045: Shell Rot
ENRICHMENTS["reptile_0045"] = {
    "diagnosis_ja": (
        "甲羅の視診で軟化・変色（褐色〜黒色）・陥凹・異臭・甲板下浸出液を確認。"
        "病変部の培養・感受性試験（Pseudomonas、Aeromonas、Citrobacter等のグラム陰性桿菌が多い）。"
        "真菌培養（Fusarium等の真菌性甲羅腐敗の鑑別）。"
        "プローブによる病変深度評価（表層のみ or 骨板到達）。"
        "X線で甲羅骨板の骨溶解・骨髄炎を評価。CBC（ヘテロフィル増多→全身性波及）。"
        "水質検査（アンモニア・亜硝酸）と飼育環境の衛生状態評価が根本原因の特定に重要。"
    )
}

# reptile_0046: Scale Rot
ENRICHMENTS["reptile_0046"] = {
    "diagnosis_ja": (
        "腹側鱗の変色（ピンク〜褐色〜黒色）・壊死・潰瘍を視診で確認（ヘビ・トカゲの腹鱗に好発）。"
        "病変部スワブの細菌培養・感受性試験（Pseudomonas、Aeromonas等のグラム陰性桿菌が主要病原体）。"
        "細胞診で変性ヘテロフィル・細菌塊を確認。真菌培養で真菌性病変を鑑別。"
        "CBC（ヘテロフィル増多→全身性炎症波及時）、血液生化学（低蛋白→慢性消耗）。"
        "飼育環境：過湿基材・糞便接触・温度不適・不衛生が根本原因。"
        "進行例ではX線で深部組織・筋膜・骨への波及を評価。"
    )
}

# reptile_0047: Abscess
ENRICHMENTS["reptile_0047"] = {
    "diagnosis_ja": (
        "爬虫類の膿瘍はケースウス様（乾酪状の固形膿）で哺乳類と異なり液状膿を形成しない点が重要。"
        "穿刺吸引の細胞診で変性ヘテロフィル・マクロファージ・細菌塊を確認。"
        "好気・嫌気培養＋感受性試験で起因菌（Pseudomonas、Aeromonas、Proteus等）を同定。"
        "X線・CTで膿瘍の範囲・深部組織侵入・骨浸潤を評価。"
        "CBC（ヘテロフィル増多＋毒性変化→重症感染）、血液生化学（UA上昇→腎機能、低蛋白→慢性化）。"
        "外科的切除（en bloc excision）の術前評価として画像検査が重要。"
    )
}

# reptile_0048: Tail Necrosis
ENRICHMENTS["reptile_0048"] = {
    "diagnosis_ja": (
        "尾部の変色（暗褐色〜黒色）・乾燥・収縮・生死境界線のdemarcation lineを視診で確認。"
        "X線で壊死範囲の骨構造・骨折・骨溶解を評価し切断レベルを決定。"
        "壊死境界部の細菌培養・感受性試験（二次感染評価）。"
        "CBC（ヘテロフィル増多→上行性感染）、血液生化学（UA上昇→敗血症性腎障害）。"
        "原因の鑑別：脱皮不全による絞扼（環状残存皮膚）、咬傷、熱傷、血管障害。"
        "全身状態（POTZ管理・脱水補正後）の評価後に外科的断尾レベルを計画。"
    )
}

# reptile_0049: Bite Wounds
ENRICHMENTS["reptile_0049"] = {
    "diagnosis_ja": (
        "創傷の視診で咬傷パターン（同居個体 or 餌動物 or 外傷の鑑別）と深度を評価。"
        "X線で骨折・深部組織損傷・異物残存（齧歯類の歯片等）を確認。"
        "創傷スワブの好気・嫌気培養＋感受性試験（Pseudomonas、Aeromonas、Pasteurella等の混合感染が多い）。"
        "CBC（ヘテロフィル増多→感染リスク評価）、血液生化学（CK上昇→筋損傷範囲の推定）。"
        "体腔穿通の評価（腹腔洗浄液の細胞診、超音波で自由液体検索）。"
        "飼育管理歴（同居個体との体格差、給餌方法、ケージサイズ）の聴取。"
    )
}

# reptile_0050: Ulcerative Dermatitis
ENRICHMENTS["reptile_0050"] = {
    "diagnosis_ja": (
        "皮膚潰瘍の分布パターン（腹側優位→環境性、背側→外傷性、びまん性→全身性疾患）を視診で評価。"
        "潰瘍部の細菌培養・感受性試験（グラム陰性桿菌が主要起因菌）＋真菌培養。"
        "皮膚生検で潰瘍底の組織像（肉芽腫性 vs 化膿性 vs 壊死性）と微生物侵入深度を病理評価。"
        "CBC（ヘテロフィル増多＋毒性変化→全身性炎症）、血液生化学（低アルブミン→慢性蛋白喪失性皮膚症）。"
        "基礎疾患スクリーニング（ウイルス性免疫抑制・POTZ逸脱・栄養不良）。"
        "環境因子（湿度過多・不衛生基材・温度不適）の評価が根本治療に必須。"
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
