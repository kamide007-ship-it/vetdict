#!/usr/bin/env python3
"""Enrich diagnosis_ja for the first 50 Snake diseases with disease-specific
diagnostic protocols. Each entry uses snake-specific terminology (ventral tail
vein cardiocentesis, spectacle/retained eye cap, IBD inclusion bodies, tracheal
wash via single lung, cloacal exam, POTZ considerations) and is 150-350 chars."""

import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# snake_0001: Inclusion Body Disease (IBD)
ENRICHMENTS["snake_0001"] = {
    "diagnosis_ja": (
        "ボア・パイソンの神経症状（stargazing、正向反射消失、協調運動障害）が臨床的に強く示唆。"
        "肝・腎生検でエオジン好性の大型細胞質内封入体をH&E染色で確認が確定診断。"
        "食道扁桃の生検・末梢血白血球塗抹での封入体検索が低侵襲スクリーニング法。"
        "PCR（アレナウイルス/レプタレナウイルス検出）が補助的確定法。"
        "尾腹側静脈から採血しCBC（リンパ球減少→免疫抑制）・生化学（AST上昇→肝障害）を評価。POTZ内管理必須。"
    )
}

# snake_0002: Snake Fungal Disease (Ophidiomyces)
ENRICHMENTS["snake_0002"] = {
    "diagnosis_ja": (
        "顔面・体幹の痂皮形成・鱗下結節・眼鏡鱗混濁からのスワブPCR（Ophidiomyces ophidiicola特異的）が第一選択。"
        "皮膚生検でPAS/GMS染色陽性の真皮深層菌糸浸潤・肉芽腫性壊死性皮膚炎を確認。"
        "真菌培養（SDA培地、24℃、3-4週間）で黄色コロニー。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→慢性炎症）を評価。"
        "眼鏡鱗癒着・鼻孔閉塞の視診確認。POTZ内での全身状態評価が必須。"
    )
}

# snake_0003: Nidovirus Respiratory Disease
ENRICHMENTS["snake_0003"] = {
    "diagnosis_ja": (
        "パイソン類の粘液性口腔分泌物・開口呼吸・頭部挙上が臨床的に示唆。"
        "口腔・気管スワブのRT-PCR（ニドウイルス特異的）が確定診断の第一選択。"
        "ヘビは単肺構造のため気管洗浄は慎重に実施（カテーテルを右肺に挿入、過剰液量を回避）。"
        "洗浄液の細胞診でヘテロフィル・マクロファージ増多を確認。"
        "X線で肺野びまん性混濁を評価。尾腹側静脈からCBC・生化学を採血。POTZ管理下での評価必須。"
    )
}

# snake_0004: Paramyxovirus Pneumonia
ENRICHMENTS["snake_0004"] = {
    "diagnosis_ja": (
        "ヘビ類の神経症状（stargazing、正向反射消失）＋呼吸器症状（開口呼吸・粘液性鼻汁）が強く示唆。"
        "口腔・気管スワブPCR（パラミクソウイルス特異的）が生前診断の第一選択。"
        "単肺への気管洗浄液の細胞診＋培養で二次細菌感染を評価。"
        "血清HI試験（ペア血清）で抗体価上昇を確認。"
        "尾腹側静脈採血でCBC（リンパ球減少→ウイルス性免疫抑制）。X線で肺野混濁。集団発生時は全頭検査。"
    )
}

# snake_0005: Cryptosporidium serpentis
ENRICHMENTS["snake_0005"] = {
    "diagnosis_ja": (
        "慢性的な吐き戻し・体幹中部の腫大（胃壁肥厚）がヘビでの特徴的臨床所見。"
        "胃洗浄液の酸抗染色（modified Ziehl-Neelsen）でオーシスト検出。"
        "PCR（C. serpentis特異的プライマー）が種同定に最も有用。"
        "X線・造影検査で体幹中部の胃壁肥厚・通過遅延を評価。"
        "尾腹側静脈採血で生化学（低蛋白→慢性消耗）を評価。"
        "POTZ内管理。感染個体の厳格な隔離と環境消毒（アンモニア5%、加熱）が必須。"
    )
}

# snake_0006: Arenavirus Infection
ENRICHMENTS["snake_0006"] = {
    "diagnosis_ja": (
        "ボア科でのIBD関連アレナウイルスとして、神経症状・慢性消耗が臨床的に示唆。"
        "口腔・総排泄腔スワブのRT-PCR（アレナウイルスS/Lセグメント特異的）が確定診断。"
        "肝生検でエオジン好性細胞質内封入体の検出（IBDと共通病理所見）。"
        "末梢血白血球塗抹での封入体スクリーニング。"
        "尾腹側静脈採血でCBC（リンパ球減少）・生化学（AST・UA上昇→肝腎障害）。"
        "POTZ内管理。新規導入個体の検疫PCRスクリーニングが感染拡大防止に重要。"
    )
}

# snake_0007: Sunshine Virus (Reptarenavirus)
ENRICHMENTS["snake_0007"] = {
    "diagnosis_ja": (
        "パイソン類の神経症状・呼吸器症状・慢性消耗がIBD様の臨床像として示唆。"
        "RT-PCR（レプタレナウイルス特異的、Sunshine virus系統群）が確定診断の標準法。"
        "肝・脾・腎生検で細胞質内封入体を確認（H&E染色、電子顕微鏡でアレナウイルス粒子）。"
        "末梢血白血球の封入体スクリーニング（低侵襲）。"
        "尾腹側静脈採血でCBC・生化学を評価。POTZ管理下。"
        "IBDとの臨床的鑑別は困難でありPCRによるウイルス種同定が必須。"
    )
}

# snake_0008: Snake Mite (Ophionyssus natricis)
ENRICHMENTS["snake_0008"] = {
    "diagnosis_ja": (
        "鱗間・眼鏡鱗周囲・顎下・総排泄腔周囲に黒〜赤褐色のダニを肉眼で確認。"
        "水浸法（温水浸漬後に浮遊するダニを回収）で寄生数の半定量評価。"
        "セロファンテープ法で虫卵・幼虫を採取し実体顕微鏡でOphionyssus natricisを同定。"
        "眼鏡鱗下への侵入による眼障害の視診確認。"
        "尾腹側静脈採血でCBC（貧血→重度寄生時の慢性吸血、ヘテロフィル増多→二次感染）。"
        "環境中のダニ生活環評価（ケージ隙間の産卵場所特定）が再発防止に重要。"
    )
}

# snake_0009: Regurgitation Syndrome
ENRICHMENTS["snake_0009"] = {
    "diagnosis_ja": (
        "給餌後24-72時間以内の未消化〜部分消化餌の吐き戻しパターンを病歴で確認。"
        "飼育環境歴聴取：給餌後のハンドリング、POTZ逸脱（低温→消化酵素不活性化）、ストレス源。"
        "X線・造影検査で消化管異物・閉塞・胃壁肥厚（Cryptosporidium serpentis除外）を評価。"
        "糞便PCR（クリプトスポリジウム）・酸抗染色でオーシスト検索。"
        "尾腹側静脈採血で生化学（電解質異常・低蛋白→慢性嘔吐の代謝影響）。"
        "寄生虫検査（線虫・条虫の消化管寄生除外）。"
    )
}

# snake_0010: Prey-Related Injury
ENRICHMENTS["snake_0010"] = {
    "diagnosis_ja": (
        "生餌（齧歯類）による咬傷の分布パターン・深度を視診で評価（頭部・体幹に好発）。"
        "X線で骨折・深部組織損傷・齧歯類歯片の残存異物を確認。"
        "創傷スワブの好気・嫌気培養＋感受性試験（Pasteurella等の混合感染が多い）。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→感染リスク）・生化学（CK上昇→筋損傷範囲）。"
        "体腔穿通の評価として超音波で自由液体を検索。"
        "給餌管理歴（生餌 vs 冷凍解凍餌、監視下給餌の有無）の聴取が再発防止に重要。"
    )
}

# snake_0011: Retained Spectacle
ENRICHMENTS["snake_0011"] = {
    "diagnosis_ja": (
        "眼鏡鱗（spectacle）の混濁・皺形成・多層化を拡大鏡またはスリットランプで確認。"
        "脱皮殻の検査で眼鏡鱗部分の欠損（脱皮殻に穴がない＝正常脱落、穴あり＝retained）を判定。"
        "実体顕微鏡で重層した眼鏡鱗の層数を評価（複数回分の蓄積）。"
        "眼鏡鱗下膿瘍（subspectacular abscess）の合併を超音波・細隙灯で評価。"
        "飼育環境歴：湿度不足（最適50-70%）、脱皮用水容器・粗面の有無。"
        "基礎疾患としてダニ寄生・栄養不良・甲状腺機能異常を検討。"
    )
}

# snake_0012: Subspectacular Abscess
ENRICHMENTS["snake_0012"] = {
    "diagnosis_ja": (
        "眼鏡鱗下の腫脹・混濁・膨隆を細隙灯顕微鏡で確認（片側性が多い）。"
        "眼鏡鱗の穿刺吸引で乾酪様膿（爬虫類特有の固形膿）を採取し細胞診・培養。"
        "好気・嫌気培養＋感受性試験で起因菌（Pseudomonas、Aeromonas等）を同定。"
        "超音波（眼窩）で膿瘍サイズ・眼球圧迫の程度を評価。"
        "口腔内からの上行性感染経路として涙管の評価。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→感染重症度）。POTZ管理下で評価。"
    )
}

# snake_0013: Rostral Abrasion (Nose Rub)
ENRICHMENTS["snake_0013"] = {
    "diagnosis_ja": (
        "吻端の鱗損傷・擦過傷・出血・痂皮形成を視診で確認。"
        "重症度評価：表在性擦過→深部潰瘍→前上顎骨露出。"
        "頭部X線で前上顎骨・鼻骨の骨折・骨溶解を評価（慢性反復例）。"
        "病変部の細菌培養で二次感染（Pseudomonas等）を評価。"
        "飼育環境歴聴取：ケージサイズ不足、透明壁面への反復衝突（escape behavior）、"
        "視覚的ストレス源・温度勾配不適が根本原因。CBC（ヘテロフィル増多→感染合併）。"
    )
}

# snake_0014: Thermal Gradient Deficiency Disease
ENRICHMENTS["snake_0014"] = {
    "diagnosis_ja": (
        "飼育環境の温度勾配記録を詳細に聴取（POTZ範囲：種別に25-35℃、ホット/クールゾーンの有無）。"
        "慢性的POTZ逸脱による消化不良・免疫抑制・脱皮不全が臨床徴候として出現。"
        "尾腹側静脈からPOTZ内で採血しCBC・生化学を評価（POTZ外での血液検査は不正確）。"
        "免疫抑制に伴う二次感染（呼吸器・皮膚）のスクリーニング。"
        "X線で骨密度低下（MBD合併）を評価。"
        "サーモスタット・温度計の校正確認と環境改善が治療的診断を兼ねる。"
    )
}

# snake_0015: Spinal Osteopathy
ENRICHMENTS["snake_0015"] = {
    "diagnosis_ja": (
        "全身X線（ヘビの体長に応じて複数枚分割撮影）で椎体の変形・骨増殖・椎間板石灰化を評価。"
        "CT（利用可能時）で脊柱管狭窄・脊髄圧迫の程度を精密評価。"
        "神経学的検査で後躯麻痺・正向反射消失・尾部知覚低下の有無を確認。"
        "尾腹側静脈採血で血液生化学（iCa・P・ALP→代謝性骨疾患の鑑別）。"
        "鑑別診断：MBD、外傷性骨折、感染性骨髄炎、IBD（神経症状の鑑別）。"
        "飼育歴（栄養・UVB・外傷歴）の聴取が病因特定に重要。"
    )
}

# snake_0016: Kinking (Spinal Deformity)
ENRICHMENTS["snake_0016"] = {
    "diagnosis_ja": (
        "体幹の屈曲・キンク部位を触診・視診で確認し、X線で椎体奇形（半椎・楔状椎・癒合椎）を評価。"
        "先天性 vs 後天性の鑑別：出生時からの変形（遺伝的・孵化温度異常）vs 成長後の発症（MBD・外傷）。"
        "血液生化学（iCa・P・ALP）で代謝性骨疾患を除外。"
        "神経学的検査で脊髄圧迫の有無を評価（排泄障害・後躯不全麻痺）。"
        "繁殖個体では近交係数・孵化温度記録を確認。"
        "総排泄腔検査で排泄機能への影響を評価。POTZ管理下で実施。"
    )
}

# snake_0017: Retained Hemipenes
ENRICHMENTS["snake_0017"] = {
    "diagnosis_ja": (
        "総排泄腔からの片方または両方のヘミペニス脱出・腫脹・変色を視診で確認。"
        "脱出したヘミペニスの生存性評価：色調（ピンク＝血行良好 vs 暗紫〜黒＝壊死）、浮腫の程度。"
        "総排泄腔検査（cloacal exam）で嵌頓の程度・基部の絞扼を確認。"
        "X線で総排泄腔周囲の腫瘤性病変・異物を除外。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→二次感染）・生化学を評価。"
        "壊死例では切断術の術前評価として全身状態をPOTZ管理下で確認。"
    )
}

# snake_0018: Cloacal Calculi
ENRICHMENTS["snake_0018"] = {
    "diagnosis_ja": (
        "総排泄腔の触診・デジタル検査（cloacal exam）で硬い結石を触知。"
        "X線で総排泄腔内の石灰化陰影を確認（尿酸塩結石は高い放射線不透過性）。"
        "超音波で結石サイズ・数・周囲組織の炎症を評価。"
        "尾腹側静脈採血で血液生化学（UA上昇→高尿酸血症・腎機能障害、Ca・P→代謝異常）を評価。"
        "結石成分分析（尿酸塩が最多）で基礎疾患を推定。"
        "飼育環境歴：脱水（水場不足・湿度不足）・高蛋白食過剰が誘因。POTZ管理下で評価。"
    )
}

# snake_0019: Metabolic Bone Disease (MBD)
ENRICHMENTS["snake_0019"] = {
    "diagnosis_ja": (
        "X線で全身性骨密度低下・病的骨折・顎骨の線維性骨異栄養症（ラバージョー）を評価。"
        "尾腹側静脈からPOTZ内で採血し血液生化学でiCa低値・P上昇・Ca:P比逆転（正常1.5-2:1）を確認。"
        "ALP上昇は骨代謝亢進を示唆。25(OH)D3測定でUVB曝露不足を評価。"
        "食餌歴の詳細聴取：Ca:Pバランス（齧歯類主食種では稀だが昆虫食種で多発）、"
        "UVB照射（ヘビでは議論あるが一部種で必要）。"
        "触診で顎・肋骨の軟化を確認。POTZ管理下での採血が正確な結果に必須。"
    )
}

# snake_0020: Respiratory Infection
ENRICHMENTS["snake_0020"] = {
    "diagnosis_ja": (
        "開口呼吸・頭部挙上・粘液性鼻汁・wheezing音・口腔内泡沫状分泌物が臨床的に示唆。"
        "ヘビは単肺構造（右肺が機能肺）のため気管洗浄は右肺にカテーテル挿入し少量の滅菌生食で実施。"
        "洗浄液の細胞診（ヘテロフィル増多・細菌体）＋培養・感受性試験。"
        "X線で肺野混濁・液体貯留を評価。PCR（パラミクソウイルス・ニドウイルス等）。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→細菌性、リンパ球減少→ウイルス性示唆）。"
        "飼育環境歴（POTZ逸脱・低湿度が誘因）の聴取必須。"
    )
}

# snake_0021: Stomatitis (Mouth Rot)
ENRICHMENTS["snake_0021"] = {
    "diagnosis_ja": (
        "口腔内視診で歯肉・粘膜の充血・点状出血・乾酪様壊死物（黄白色）を確認。"
        "重症度分類：Grade I（点状出血）→Grade II（乾酪物付着）→Grade III（骨露出・顎骨溶解）。"
        "口腔スワブの培養・感受性試験（Pseudomonas、Aeromonas等のグラム陰性桿菌が主要）。"
        "頭部X線で顎骨の骨溶解・骨髄炎を評価。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→重症度指標）。"
        "基礎疾患（POTZ逸脱・免疫抑制・外傷）の評価が再発防止に重要。"
    )
}

# snake_0022: Cryptosporidiosis
ENRICHMENTS["snake_0022"] = {
    "diagnosis_ja": (
        "ヘビでは体幹中部の持続的腫大（胃壁肥厚）と慢性的吐き戻しが特徴的臨床所見。"
        "糞便・胃洗浄液の酸抗染色（modified Ziehl-Neelsen）でオーシストを検出。"
        "PCR（C. serpentis=胃寄生、C. varanii=腸寄生）で種同定。"
        "X線造影検査で胃壁肥厚・通過遅延を評価。"
        "尾腹側静脈採血で生化学（低蛋白→慢性消耗）。ELISA抗原検出も補助的に有用。"
        "感染個体の厳格な隔離。環境消毒（アンモニア5%）とPOTZ管理が必須。"
    )
}

# snake_0023: Paramyxovirus
ENRICHMENTS["snake_0023"] = {
    "diagnosis_ja": (
        "ヘビ類の急性神経症状（stargazing・正向反射消失・フリッキング異常）＋呼吸器症状が臨床的に示唆。"
        "口腔・気管スワブPCR（パラミクソウイルス特異的）が生前診断の第一選択。"
        "血清HI試験でペア血清の抗体価上昇を確認。"
        "単肺への気管洗浄液の細胞診で封入体を検索。"
        "尾腹側静脈採血でCBC（リンパ球減少→免疫抑制）。X線で肺野混濁。"
        "集団発生時は全頭PCRスクリーニングが必須。剖検で肺・脳の封入体が確定的。"
    )
}

# snake_0024: Adenovirus Infection
ENRICHMENTS["snake_0024"] = {
    "diagnosis_ja": (
        "肝臓生検で好塩基性核内封入体（カウドリーA型）をH&E染色で確認が確定診断。"
        "口腔・総排泄腔スワブPCR（アデノウイルス特異的プライマー）が生前診断に有用。"
        "尾腹側静脈採血でCBC（ヘテロフィル・リンパ球減少→免疫抑制）。"
        "生化学（AST・LDH著明上昇→肝壊死、UA上昇→腎障害）。"
        "超音波で肝腫大・実質エコー輝度変化を評価。POTZ管理下での採血が正確な結果に必須。"
        "剖検で肝臓の多巣性壊死が特徴的所見。"
    )
}

# snake_0025: Herpesvirus Infection
ENRICHMENTS["snake_0025"] = {
    "diagnosis_ja": (
        "口腔内の白色プラーク・壊死性口内炎・皮膚小水疱がヘビでの臨床的特徴。"
        "口腔・皮膚スワブPCR（ヘルペスウイルス特異的）が生前確定診断の第一選択。"
        "細胞診で好酸性核内封入体（カウドリーA型）を検索。"
        "皮膚・粘膜生検でH&E染色による封入体確認と壊死性炎症を病理評価。"
        "尾腹側静脈採血でCBC（リンパ球減少→ウイルス免疫抑制）・生化学で肝機能評価。"
        "ウイルス分離は研究機関限定。POTZ管理下で評価。"
    )
}

# snake_0026: Nidovirus Infection
ENRICHMENTS["snake_0026"] = {
    "diagnosis_ja": (
        "パイソン類で増殖性肺炎・口腔内粘液過多・開口呼吸が特徴的臨床像。"
        "口腔・気管スワブのRT-PCR（ニドウイルス特異的）が確定診断。"
        "ヘビの単肺構造を考慮し気管洗浄は右肺に少量注入で実施。"
        "洗浄液細胞診でヘテロフィル・マクロファージ増多を確認＋二次細菌培養。"
        "X線で肺野びまん性混濁を評価。尾腹側静脈採血でCBC・生化学。"
        "肺生検でII型肺胞上皮の増殖性変化が病理的特徴。POTZ管理下で評価必須。"
    )
}

# snake_0027: Iridovirus (Ranavirus)
ENRICHMENTS["snake_0027"] = {
    "diagnosis_ja": (
        "急性の全身性出血・浮腫・皮膚壊死・突然死が臨床的に示唆。"
        "PCR（ラナウイルスMCP遺伝子特異的）が生前確定診断に最も有用。"
        "尾腹側静脈採血でCBC（汎血球減少）・生化学（AST・LDH上昇→多臓器障害）。"
        "肝・脾・腎生検で好塩基性細胞質内封入体を確認。"
        "ウイルス分離（細胞培養）は研究施設限定。"
        "集団死亡時は複数検体のPCRスクリーニングが疫学管理に重要。POTZ管理下で評価。"
    )
}

# snake_0028: Mycoplasma Infection
ENRICHMENTS["snake_0028"] = {
    "diagnosis_ja": (
        "慢性上部呼吸器症状（漿液性〜粘液膿性鼻汁、口腔内粘液増加）が臨床的に示唆。"
        "鼻腔・口腔スワブPCR（Mycoplasma特異的16S rRNA）が確定診断の標準法。"
        "培養は特殊培地（SP4）＋長期培養が必要で一般臨床では困難。"
        "単肺への気管洗浄液の細胞診＋培養で呼吸器の炎症程度を評価。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→二次感染合併時）。"
        "POTZ管理下での採血。集団スクリーニングにはペア血清のELISA法が有用。"
    )
}

# snake_0029: Salmonellosis
ENRICHMENTS["snake_0029"] = {
    "diagnosis_ja": (
        "糞便の直接培養（SS寒天・XLD培地）でSalmonella属を分離同定。"
        "PCRによる迅速検出・血清型別（Kauffmann-White分類）で疫学解析。"
        "総排泄腔スワブからの培養も有効（cloacal exam時に同時採取）。"
        "敗血症疑い時は尾腹側静脈から血液培養。薬剤感受性試験で治療薬選択。"
        "CBC（ヘテロフィル増多→急性炎症、毒性変化→敗血症）・生化学（UA→腎障害）。"
        "人獣共通感染症であり飼育者への衛生指導が診断時に必須。POTZ管理下で実施。"
    )
}

# snake_0030: Pseudomonas Infection
ENRICHMENTS["snake_0030"] = {
    "diagnosis_ja": (
        "病変部（口内炎・皮膚潰瘍・膿瘍・呼吸器）からの好気培養で緑色色素産生のグラム陰性桿菌を分離。"
        "薬剤感受性試験が治療薬選択に必須（多剤耐性株が多い）。"
        "気管洗浄液（単肺へのカテーテル挿入）の培養・細胞診。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多＋毒性変化→重症感染）・生化学（UA→腎機能）。"
        "POTZ逸脱による免疫低下が日和見感染の誘因。"
        "水質・湿度環境因子の評価。POTZ管理下で全身状態を評価。"
    )
}

# snake_0031: Aeromonas Infection
ENRICHMENTS["snake_0031"] = {
    "diagnosis_ja": (
        "皮膚潰瘍・体腔液からの培養（血液寒天37℃）でAeromonas属（A. hydrophila等）を分離。"
        "薬剤感受性試験で治療薬選択（β-ラクタマーゼ産生株に注意）。"
        "敗血症評価のため尾腹側静脈から血液培養。"
        "CBC（ヘテロフィル増多＋毒性変化→急性細菌感染）・生化学（UA→腎機能、低蛋白→敗血症）。"
        "水棲・半水棲ヘビ種で多く水質検査（アンモニア・亜硝酸・pH）が重要。"
        "皮膚生検で壊死性血管炎を確認。POTZ管理下で評価。"
    )
}

# snake_0032: Mycobacteriosis
ENRICHMENTS["snake_0032"] = {
    "diagnosis_ja": (
        "皮膚肉芽腫・結節の抗酸菌染色（Ziehl-Neelsen）で抗酸菌体を検出。"
        "培養（Löwenstein-Jensen培地、4-12週間）で菌種同定。PCR（16S rRNA）による迅速分子同定推奨。"
        "病理組織検査で多核巨細胞を伴う肉芽腫性炎症を確認。"
        "尾腹側静脈採血でCBC（単球増加→慢性肉芽腫性炎症）・生化学（低アルブミン→慢性消耗）。"
        "X線・CTで内臓肉芽腫・脊椎骨病変を評価。"
        "人獣共通感染リスクの評価が必須。POTZ管理下で実施。"
    )
}

# snake_0033: Chlamydiosis
ENRICHMENTS["snake_0033"] = {
    "diagnosis_ja": (
        "口腔・総排泄腔スワブのPCR（Chlamydia特異的）が生前確定診断の第一選択。"
        "総排泄腔検査（cloacal exam）時にスワブ採取し培養・PCRを同時実施。"
        "細胞診でGiemsa染色による上皮細胞質内の好塩基性封入体を検索。"
        "血清ELISA（ペア血清で4倍以上の抗体価上昇）で活動性感染を示唆。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→急性感染）・生化学で肝機能評価。"
        "肝生検で肉芽腫性肝炎が確定的。人獣共通感染の可能性があり取扱い注意。"
    )
}

# snake_0034: Dermatophytosis
ENRICHMENTS["snake_0034"] = {
    "diagnosis_ja": (
        "鱗・皮膚病変部の直接鏡検（KOH処理）で菌糸・分節胞子を観察。"
        "真菌培養（DTM/SDA培地、25-30℃、2-3週間）で皮膚糸状菌を分離同定。"
        "皮膚生検でPAS染色陽性の角質内菌糸・胞子を確認。"
        "鑑別診断：Ophidiomyces（SFD）・脱皮不全・細菌性皮膚炎との区別が重要。"
        "尾腹側静脈採血でCBC・生化学による全身状態評価。"
        "POTZ逸脱・過湿環境による免疫低下が素因となるため環境歴を聴取。"
    )
}

# snake_0035: Aspergillosis
ENRICHMENTS["snake_0035"] = {
    "diagnosis_ja": (
        "呼吸器症状のある個体でX線により肺野結節影を評価。"
        "ヘビの単肺構造を考慮し気管洗浄カテーテルを右肺に挿入、洗浄液の細胞診でY字分岐菌糸を確認。"
        "培養（SDA培地、37℃）でAspergillus属を同定。"
        "血清ガラクトマンナン抗原検査が侵襲性アスペルギルス症の補助診断に有用。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→炎症、単球増加→肉芽腫形成）。"
        "POTZ逸脱による免疫抑制が背景因子。POTZ管理下で評価。"
    )
}

# snake_0036: Candidiasis
ENRICHMENTS["snake_0036"] = {
    "diagnosis_ja": (
        "口腔・消化管粘膜の白色偽膜状プラークが臨床的に特徴的。"
        "直接鏡検（KOH処理・グラム染色）で出芽酵母と偽菌糸を確認。"
        "培養（SDA培地・CHROMagar Candida）でCandida属を種同定。"
        "口腔スワブの細胞診で多数の酵母細胞とヘテロフィルを確認。"
        "尾腹側静脈採血でCBC・生化学による全身状態評価。"
        "基礎疾患（長期抗菌薬使用・POTZ逸脱・免疫抑制）の検索が重要。X線造影で消化管粘膜不整を評価。"
    )
}

# snake_0037: Chrysosporium (CANV) Infection
ENRICHMENTS["snake_0037"] = {
    "diagnosis_ja": (
        "皮膚の黄色〜褐色変色・壊死性痂皮からKOH処理で太い菌糸を確認。"
        "真菌培養（SDA培地、24-30℃、2-4週間）でCANV特有の白〜黄色コロニー。"
        "PCR（ITS領域）でChryosporium anamorph of Nannizziopsis vriesiiを分子同定（確定診断）。"
        "皮膚生検でGMS/PAS染色陽性菌糸の深部侵入と肉芽腫性皮膚炎を確認。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多）・生化学（CK上昇→筋浸潤、低アルブミン→消耗）。"
        "Ophidiomyces（SFD）との鑑別にPCRが必須。"
    )
}

# snake_0038: Mite Infestation (Ophionyssus)
ENRICHMENTS["snake_0038"] = {
    "diagnosis_ja": (
        "鱗間・眼鏡鱗周囲・総排泄腔周囲にOphionyssus natricis（黒〜赤褐色）を肉眼確認。"
        "水浸法で浮遊ダニを回収し虫体数を半定量評価。セロファンテープ法で卵・幼虫を採取。"
        "眼鏡鱗下へのダニ侵入による spectacle混濁・subspectacular abscess合併を評価。"
        "尾腹側静脈採血でCBC（貧血→慢性吸血、ヘテロフィル増多→二次感染）。"
        "環境中のダニ生活環評価（ケージ隙間・基材の卵・幼虫検索）。"
        "重度寄生時はダニ媒介病原体（Hemogregarines等）のスクリーニング。"
    )
}

# snake_0039: Tick Infestation
ENRICHMENTS["snake_0039"] = {
    "diagnosis_ja": (
        "鱗間に付着するマダニ（Hyalomma、Amblyomma等）を肉眼・実体顕微鏡で種同定。"
        "虫体の顎体基部・盾板形態で分類学的同定。"
        "ダニ媒介病原体のスクリーニング：血液塗抹でHemogregarines（赤血球内寄生体）検出、PCR検査。"
        "尾腹側静脈採血でCBC（貧血→重度吸血、ヘテロフィル増多→二次感染）。"
        "刺咬部位の二次感染評価（細菌培養）。"
        "野外採集個体の検疫プロトコル確認。POTZ管理下で実施。"
    )
}

# snake_0040: Nematode Infection
ENRICHMENTS["snake_0040"] = {
    "diagnosis_ja": (
        "糞便検査（直接塗抹法・浮遊法・沈殿法）で線虫卵・幼虫を検出し形態同定。"
        "浮遊法（比重1.18-1.20の飽和食塩水またはシュガー溶液）が推奨。"
        "Strongyloides等は糞便中の幼虫を直接鏡検で確認。"
        "総排泄腔検査（cloacal exam）時に糞便サンプルを同時採取。"
        "X線造影で腸管壁肥厚・閉塞所見を評価（大量寄生時）。"
        "尾腹側静脈採血でCBC。剖検時に消化管・肺からの虫体回収が確定的。POTZ管理下で実施。"
    )
}

# snake_0041: Cestode Infection
ENRICHMENTS["snake_0041"] = {
    "diagnosis_ja": (
        "糞便検査（浮遊法・沈殿法）で条虫卵を検出。片節の肉眼的確認が最も簡便。"
        "総排泄腔検査（cloacal exam）時に総排泄腔内の片節を直接確認する場合あり。"
        "X線造影で腸管内の条虫体を陰影欠損として描出（大型種）。"
        "尾腹側静脈採血で生化学（低蛋白・低アルブミン→慢性消耗）。"
        "虫体・片節の形態同定（頭節の吸盤・鉤構造）で種同定。"
        "中間宿主（給餌げっ歯類・両生類）の感染状況評価と給餌管理改善が再感染防止に重要。"
    )
}

# snake_0042: Trematode Infection
ENRICHMENTS["snake_0042"] = {
    "diagnosis_ja": (
        "糞便沈殿法（吸虫卵は比重が大きく浮遊法では検出困難）で蓋付き虫卵を検出。"
        "口腔内の直接視診で咽頭部の吸虫体を肉眼確認（ヘビではReniferinae亜科が多い）。"
        "X線・超音波で肺・肝臓の吸虫嚢胞を評価。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→寄生虫反応）・生化学（AST→肝実質障害）。"
        "病理組織検査で肝・肺の肉芽腫内に虫体・虫卵を確認（確定診断）。"
        "給餌している両生類・魚類からの中間宿主経路の聴取が重要。"
    )
}

# snake_0043: Pentastomid Infection
ENRICHMENTS["snake_0043"] = {
    "diagnosis_ja": (
        "X線でヘビの肺実質内にC字型〜S字型の石灰化虫体（成虫）を確認。"
        "気管洗浄液（単肺へのカテーテル挿入）中の虫卵（4つの鉤を持つ幼虫含有）検出。"
        "口腔検査で気管開口部からの虫体頭部突出を視認する場合あり。"
        "内視鏡（気管鏡）で気管・肺内の虫体を直接観察。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→炎症）。"
        "Porocephalus、Armillifer等の形態同定。人獣共通感染リスクあり取扱い注意。"
    )
}

# snake_0044: Coccidia
ENRICHMENTS["snake_0044"] = {
    "diagnosis_ja": (
        "糞便浮遊法（飽和食塩水、比重1.18-1.20）でコクシジウムオーシストを検出。"
        "オーシスト形態（サイズ・形状・スポロシスト数）でEimeria、Isospora、Caryospora等を属レベルで同定。"
        "直接塗抹法で新鮮糞便中の運動性虫体を確認。"
        "総排泄腔検査（cloacal exam）時に糞便を同時採取。"
        "尾腹側静脈採血で生化学（低蛋白→慢性消耗性下痢）。"
        "連日3日間の連続採取で検出感度向上。POTZ管理下での評価必須。"
    )
}

# snake_0045: Flagellate Protozoan Infection
ENRICHMENTS["snake_0045"] = {
    "diagnosis_ja": (
        "新鮮糞便の直接塗抹鏡検（POTZ温度で加温した生食）で運動性のある鞭毛虫体を確認。"
        "形態同定：Trichomonas（洋梨形、4鞭毛＋波動膜）、Hexamita（左右対称、6鞭毛）。"
        "胃洗浄液の直接鏡検で上部消化管寄生種を検出。"
        "総排泄腔検査（cloacal exam）で直接糞便採取。"
        "尾腹側静脈採血で生化学（脱水・低蛋白→慢性感染の代謝影響）。"
        "検体は採取後速やかに検査（虫体運動性の消失防止）。POTZ管理下で評価。"
    )
}

# snake_0046: Amoebic Infection
ENRICHMENTS["snake_0046"] = {
    "diagnosis_ja": (
        "新鮮糞便（POTZ温度で加温）の直接塗抹法でアメーバ栄養体（偽足運動）とシストを検出。"
        "トリクローム・PAS染色で栄養体内の貪食赤血球を確認（Entamoeba invadensの病原性指標）。"
        "超音波でアメーバ性肝膿瘍（低エコー域）を検索。"
        "尾腹側静脈採血で生化学（AST上昇→肝膿瘍、低アルブミン→慢性腸炎）。"
        "大腸生検でフラスコ状潰瘍とPAS陽性栄養体を確認。PCRでE. invadens同定。"
        "肉食性ヘビから草食爬虫類への感染伝播リスク評価が重要。"
    )
}

# snake_0047: Dysecdysis (Retained Shed)
ENRICHMENTS["snake_0047"] = {
    "diagnosis_ja": (
        "視診で眼鏡鱗（spectacle）の残存・混濁・多層化、尾先端・体幹の残存皮膚を確認。"
        "脱皮殻の検査で眼鏡鱗部分の脱落状態を判定（一体脱皮が正常、断片化は異常）。"
        "実体顕微鏡で重層した眼鏡鱗の層数を評価。"
        "飼育環境歴：湿度不足（最適50-70%）、脱皮用ウェットハイド・水容器の有無。"
        "基礎疾患スクリーニング：ダニ寄生、栄養状態、甲状腺機能。"
        "慢性例では指趾壊死・眼鏡鱗下膿瘍の合併をスリットランプで評価。"
    )
}

# snake_0048: Thermal Burns
ENRICHMENTS["snake_0048"] = {
    "diagnosis_ja": (
        "飼育環境歴：熱源（ヒートランプ・ホットロック・アンダータンクヒーター）との接触歴、サーモスタット故障。"
        "熱傷深度分類：表在性（鱗変色）→深達性（真皮壊死・水疱）→全層性（筋露出）。"
        "体表マッピングで損傷面積を推定（ヘビでは腹鱗数での区画化が有用）。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→二次感染）・生化学（CK→筋障害、低蛋白→蛋白漏出）。"
        "病変部の培養・感受性試験で二次感染を評価。"
        "POTZ管理下で体液バランスを評価。"
    )
}

# snake_0049: Rostral Abrasion
ENRICHMENTS["snake_0049"] = {
    "diagnosis_ja": (
        "吻端の鱗損傷・擦過傷・出血・痂皮を視診で確認（ヘビで最も一般的な外傷）。"
        "重症度：表在性擦過→深部潰瘍→前上顎骨・鼻骨露出。"
        "頭部X線で前上顎骨の骨折・骨溶解（慢性反復例）を評価。"
        "病変部の培養で二次感染（Pseudomonas等）を評価。"
        "飼育環境歴：ケージサイズ・透明壁面への衝突行動（escape behavior）・温度勾配不適が根本原因。"
        "尾腹側静脈採血でCBC。口腔内への波及は内視鏡で確認。"
    )
}

# snake_0050: Blister Disease
ENRICHMENTS["snake_0050"] = {
    "diagnosis_ja": (
        "腹側鱗の水疱・膨隆・液体貯留を視診で確認（腹部接地面に好発、ヘビで特に多い）。"
        "水疱液の細胞診（ヘテロフィル・細菌→感染性）と培養・感受性試験。"
        "皮膚生検で表皮下水疱・真皮急性炎症・細菌侵入を病理確認。"
        "尾腹側静脈採血でCBC（ヘテロフィル増多→全身性波及）・生化学（低アルブミン→重症蛋白漏出）。"
        "飼育環境歴：過湿基材・不衛生な水浸し状態・温度不適が根本原因。"
        "進行例では敗血症リスク評価のため血液培養を追加。POTZ管理下で実施。"
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
