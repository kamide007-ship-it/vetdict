#!/usr/bin/env python3
"""Enrich diagnosis_ja for the first 50 Tortoise diseases with disease-specific
diagnostic protocols. Each entry uses tortoise-specific terminology (plastron
transillumination, shell fracture evaluation, herpesvirus PCR, Mycoplasma
agassizii nasal wash, URTD diagnostics, pyramiding assessment, aural abscess,
hibernation health check, POTZ management) and is 150-350 characters."""

import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# tortoise_0038: Chrysosporium (CANV) Infection / クリソスポリウム感染（リクガメ）
ENRICHMENTS["tortoise_0038"] = {
    "diagnosis_ja": (
        "甲羅・皮膚病変部の圧挫標本でKOH処理後に太い分岐菌糸を確認。"
        "真菌培養（SDA培地、25-30℃、2-4週間）でCANV特有の白〜黄色コロニーを分離。"
        "PCR（ITS領域）による分子同定でNannizziopsis guarroi等を確定。"
        "皮膚生検でPAS/GMS染色陽性の深部菌糸侵入と肉芽腫性炎症を病理確認。"
        "リクガメでは甲羅の変色・軟化から骨板浸潤への進行を評価。POTZ管理下で採血しCBC・生化学で全身状態を確認。"
    )
}

# tortoise_0063: Egg Binding (Dystocia) / 卵詰まり（難産）（リクガメ）
ENRICHMENTS["tortoise_0063"] = {
    "diagnosis_ja": (
        "腹部X線で卵殻の石灰化・数・位置・骨盤腔との大きさの比較を評価。"
        "超音波で卵管壁肥厚・自由液体（卵黄性体腔炎の合併）を確認。"
        "血液生化学でiCa（＜1.0 mmol/Lは子宮収縮不全を示唆）・総蛋白・UA上昇（腎障害合併）を評価。"
        "CBC（ヘテロフィル増多→卵管炎合併）。プラストロン透過光検査で卵の位置を非侵襲的に評価。"
        "環境歴聴取（産卵場所の有無・基質深さ・温度・湿度）が閉塞性 vs 非閉塞性の鑑別に重要。"
    )
}

# tortoise_0130: Wound Infection / 創傷感染（リクガメ）
ENRICHMENTS["tortoise_0130"] = {
    "diagnosis_ja": (
        "創傷部スワブの好気・嫌気培養＋感受性試験でグラム陰性桿菌（Pseudomonas、Aeromonas等）を同定。"
        "創傷の深度評価：表在性→筋膜到達→甲羅骨板損傷の段階分類。"
        "甲羅損傷を伴う場合はX線で骨板亀裂・骨髄炎の有無を確認。"
        "CBC（ヘテロフィル増多＋毒性変化→全身性炎症波及）、血液生化学（UA→腎機能、低蛋白→敗血症）。"
        "咬傷（犬・齧歯類）、芝刈り機外傷、落下衝撃等の外傷機転の聴取が重要。"
    )
}

# tortoise_shell_fracture: Shell Injury (Tortoise) / 甲殻損傷（リクガメ）
ENRICHMENTS["tortoise_shell_fracture"] = {
    "diagnosis_ja": (
        "甲羅損傷の分類：背甲（carapace）vs 腹甲（plastron）、亀裂 vs 陥凹 vs 欠損の評価。"
        "X線（DV・lateral）で骨板の骨折線・転位・体腔への穿通を確認。CT（利用可能時）で三次元的損傷範囲を評価。"
        "プラストロン透過光検査で体腔内出血・臓器損傷を非侵襲的にスクリーニング。"
        "CBC（ヘテロフィル増多→感染リスク）、血液生化学（CK→筋損傷、UA→ショック時腎障害）。"
        "外傷機転（犬咬傷・車両・落下・芝刈り機）の詳細聴取が予後判定に不可欠。"
    )
}

# tortoise_0005: Shell Rot / 甲羅腐敗（リクガメ）
ENRICHMENTS["tortoise_0005"] = {
    "diagnosis_ja": (
        "甲羅の視診で甲板の変色（褐色〜黒色）・軟化・陥凹・異臭・甲板下浸出液を確認。"
        "病変部の培養・感受性試験（Pseudomonas、Aeromonas、Citrobacter等のグラム陰性桿菌が多い）。"
        "真菌培養（Fusarium等の真菌性甲羅腐敗の鑑別）。プローブで病変深度を評価（表層限局 vs 骨板貫通）。"
        "X線で甲羅骨板の骨溶解・骨髄炎を評価。CBC（ヘテロフィル増多→全身性波及）。"
        "飼育環境（過湿・不衛生な基材・水質悪化）が根本原因であり環境歴聴取が必須。"
    )
}

# tortoise_0008: Beak Overgrowth / 嘴過成長（リクガメ）
ENRICHMENTS["tortoise_0008"] = {
    "diagnosis_ja": (
        "口腔の視診で上嘴（rhamphotheca）の過成長・咬合異常・左右非対称を評価。"
        "頭部X線/CTで嘴基部の骨構造異常・歯列不整・前上顎骨の変形を確認。"
        "食餌歴聴取：高繊維食（牧草・野草）の不足による摩耗不足が最多原因。"
        "MBD（代謝性骨疾患）の合併評価として血液生化学（iCa・P・ALP）・四肢骨X線を実施。"
        "先天性奇形 vs 後天性（外傷・栄養不良・感染）の鑑別が治療計画に重要。"
    )
}

# tortoise_0035: Dermatophytosis / 皮膚糸状菌症（リクガメ）
ENRICHMENTS["tortoise_0035"] = {
    "diagnosis_ja": (
        "甲羅・皮膚病変部の直接鏡検（KOH処理）で菌糸・分節胞子を観察。"
        "真菌培養（DTM/SDA培地、25-30℃、2-3週間）で皮膚糸状菌（Trichophyton、Microsporum等）を分離同定。"
        "皮膚生検でPAS染色陽性の角質内菌糸を確認。リクガメでは甲板表面の白色〜灰色変色が特徴的初発症状。"
        "CANV（Chrysosporium）感染・細菌性甲羅腐敗・脱皮異常との鑑別が重要。"
        "POTZ管理下での免疫状態評価とUVB照射環境の確認。"
    )
}

# tortoise_0048: Dysecdysis (Retained Shed) / 脱皮不全（リクガメ）
ENRICHMENTS["tortoise_0048"] = {
    "diagnosis_ja": (
        "視診でリクガメの甲板・四肢・頸部に残存する脱皮片を確認。"
        "甲板の異常剥離（過剰脱落 vs 異常蓄積）のパターンを評価。"
        "飼育環境歴聴取：湿度不足（適正種により40-80%）、温浴頻度、UVB照射状況。"
        "基礎疾患スクリーニング：血液生化学（甲状腺機能・肝機能・iCa）、CBC（ヘテロフィル増多→二次感染）。"
        "四肢指趾の絞扼性壊死（残存皮膚による血流遮断）の有無を確認。"
        "甲羅腐敗・真菌感染・ビタミンA欠乏との鑑別が必要。"
    )
}

# tortoise_0051: Blister Disease / 水疱病（リクガメ）
ENRICHMENTS["tortoise_0051"] = {
    "diagnosis_ja": (
        "腹甲（plastron）・四肢腹側の水疱形成・膨隆・液体貯留を視診で確認。"
        "水疱液の細胞診（ヘテロフィル・細菌→感染性水疱）と好気培養・感受性試験。"
        "皮膚生検で表皮下水疱・真皮の急性〜亜急性炎症・細菌侵入を病理評価。"
        "CBC（ヘテロフィル増多→全身性炎症波及）。飼育環境：過湿基材・排泄物接触・温度不適が根本原因。"
        "進行例では敗血症リスク評価のため血液培養を追加。甲羅腐敗への進展を監視。"
    )
}

# tortoise_0052: Scale Rot / 鱗腐敗（リクガメ）
ENRICHMENTS["tortoise_0052"] = {
    "diagnosis_ja": (
        "四肢・頸部・尾の鱗の変色（ピンク〜褐色〜黒色）・壊死・潰瘍を視診で確認。"
        "病変部スワブの細菌培養・感受性試験（Pseudomonas、Aeromonas等のグラム陰性桿菌が主要病原体）。"
        "細胞診で変性ヘテロフィル・細菌塊を確認。真菌培養で真菌性合併感染を鑑別。"
        "CBC（ヘテロフィル増多→全身性炎症）。飼育環境：過湿基材・糞便接触・温度不適が誘因。"
        "進行例ではX線で深部組織・骨への波及を評価。甲羅腐敗との同時罹患が多い。"
    )
}

# tortoise_septicemic_cutaneous_ulcerative_disease_scud: SCUD
ENRICHMENTS["tortoise_septicemic_cutaneous_ulcerative_disease_scud"] = {
    "diagnosis_ja": (
        "皮膚・甲羅の潰瘍性病変からの培養・感受性試験でCitrobacter freundii等のグラム陰性桿菌を同定。"
        "血液培養（敗血症評価が必須、SCUDは高率に菌血症を伴う）。"
        "CBC（ヘテロフィル増多＋毒性変化→重症度指標）、血液生化学（UA上昇→腎障害、AST→肝障害）。"
        "甲羅のX線で骨板の骨溶解・深部浸潤を評価。プラストロン透過光検査で体腔内膿瘍を検索。"
        "皮膚生検で壊死性血管炎・細菌塊を病理確認。水質検査が環境因子の評価に重要。"
    )
}

# tortoise_bacterial_dermatitis: Bacterial Dermatitis / 細菌性皮膚炎
ENRICHMENTS["tortoise_bacterial_dermatitis"] = {
    "diagnosis_ja": (
        "皮膚病変部（四肢・頸部・尾基部に好発）の視診で発赤・腫脹・浸出液・痂皮形成を評価。"
        "病変部スワブの好気培養・感受性試験でグラム陰性桿菌（Pseudomonas、Aeromonas等）を同定。"
        "細胞診で変性ヘテロフィル・細胞内細菌を確認。嫌気培養（深部潰瘍時）も追加。"
        "CBC（ヘテロフィル増多→全身性炎症波及）。基礎疾患（POTZ逸脱・免疫抑制・栄養不良）の検索。"
        "飼育環境（基材の衛生状態・湿度・温度勾配）が根本原因であり環境改善指導が再発防止に重要。"
    )
}

# tortoise_0002: Mycoplasma agassizii (URTD)
ENRICHMENTS["tortoise_0002"] = {
    "diagnosis_ja": (
        "鼻腔洗浄液（nasal wash）のPCR（Mycoplasma agassizii / M. testudineum特異的プライマー）が確定診断の標準法。"
        "血清ELISA（抗マイコプラズマ抗体）は集団スクリーニングに有用。ペア血清で4倍以上の抗体価上昇で活動性感染を確認。"
        "鼻汁の性状評価（漿液性→粘液膿性への進行）と鼻腔X線で骨溶解の有無を確認。"
        "CBC（ヘテロフィル増多→二次細菌感染合併時）。URTD（上部気道疾患）はリクガメの集団管理で最重要感染症であり、"
        "新規導入個体の検疫PCRスクリーニングが推奨。"
    )
}

# tortoise_0029: Mycoplasma Infection / マイコプラズマ感染（リクガメ）
ENRICHMENTS["tortoise_0029"] = {
    "diagnosis_ja": (
        "鼻腔洗浄液（nasal flush、温生理食塩水0.5-1 mL）からのPCR検出が最も感度の高い確定法。"
        "鼻腔スワブPCRも利用可能だが、洗浄液より感度が低い。"
        "培養（SP4培地、37℃、2-6週間）は技術的に困難で一般臨床ではPCRを優先。"
        "血清ELISA：抗体陽性は感染既往を示すが活動性感染の証明には限界あり。"
        "CBC（ヘテロフィル増多→二次感染）、血液生化学で全身状態評価。"
        "リクガメのURTDは慢性経過が多く、ストレス・POTZ逸脱で再燃するため飼育環境の評価が不可欠。"
    )
}

# tortoise_0031: Pseudomonas Infection / 緑膿菌感染（リクガメ）
ENRICHMENTS["tortoise_0031"] = {
    "diagnosis_ja": (
        "病変部（甲羅腐敗・皮膚潰瘍・口腔・呼吸器分泌物）からの好気培養で緑色色素産生のグラム陰性桿菌を分離。"
        "薬剤感受性試験が治療薬選択に必須（多剤耐性株が多く、エンロフロキサシン・アミカシンの感受性を確認）。"
        "甲羅病変ではプローブで骨板浸潤深度を評価。"
        "CBC（ヘテロフィル増多＋毒性変化→重症感染の指標）、血液生化学（UA→腎機能、アミノグリコシド使用前に確認必須）。"
        "リクガメではPOTZ逸脱・過湿環境が日和見感染の主要誘因。"
    )
}

# tortoise_0032: Aeromonas Infection / エロモナス感染（リクガメ）
ENRICHMENTS["tortoise_0032"] = {
    "diagnosis_ja": (
        "皮膚潰瘍・甲羅病変からの培養（血液寒天37℃好気培養）でAeromonas属（A. hydrophila等）を分離。"
        "薬剤感受性試験で治療薬選択（β-ラクタマーゼ産生株に注意、エンロフロキサシン・TMS感受性を確認）。"
        "血液培養で敗血症評価。CBC（ヘテロフィル増多＋毒性変化→急性細菌感染）。"
        "血液生化学（UA→腎機能、低蛋白→敗血症性消耗）。"
        "水棲・半水棲リクガメで特に多く、水質検査（アンモニア・亜硝酸・pH）が環境因子評価に重要。"
    )
}

# tortoise_0033: Mycobacteriosis / マイコバクテリウム症（リクガメ）
ENRICHMENTS["tortoise_0033"] = {
    "diagnosis_ja": (
        "病変部（皮膚結節・肉芽腫）の抗酸菌染色（Ziehl-Neelsen）で抗酸菌体を検出。"
        "培養（Löwenstein-Jensen培地・液体培養、4-12週間）で菌種同定。"
        "PCR（16S rRNA・hsp65遺伝子）による迅速な分子同定が推奨。"
        "皮膚生検・病理で多核巨細胞を伴う肉芽腫性炎症を確認。"
        "CBC（単球増加→慢性肉芽腫性炎症）、血液生化学（低アルブミン→慢性消耗）。"
        "X線・CTで内臓肉芽腫を評価。人獣共通感染リスクの評価が必須。"
    )
}

# tortoise_0034: Chlamydiosis / クラミジア症（リクガメ）
ENRICHMENTS["tortoise_0034"] = {
    "diagnosis_ja": (
        "結膜・鼻腔スワブのPCR（Chlamydia特異的）が生前確定診断の第一選択。"
        "細胞診でGiemsa染色にて上皮細胞質内の好塩基性封入体を検索。"
        "血清学（CFT・ELISA）で抗体検出、ペア血清の4倍以上の抗体価上昇で活動性感染を示唆。"
        "CBC（ヘテロフィル増多→急性感染期）。リクガメでは結膜炎・鼻汁・肺炎として発症し、"
        "ヘルペスウイルス・マイコプラズマURTDとの鑑別・混合感染の評価が重要。"
        "人獣共通感染症の可能性があり取扱い注意。"
    )
}

# tortoise_0112: Squamous Cell Carcinoma / 扁平上皮癌（リクガメ）
ENRICHMENTS["tortoise_0112"] = {
    "diagnosis_ja": (
        "FNA細胞診で大型の異型扁平上皮細胞・角化異常・核分裂像を確認。切除生検による病理組織検査が確定診断に必須。"
        "CT/X線で局所浸潤範囲・骨浸潤・リンパ節腫大・肺転移の評価。"
        "リクガメでは四肢・眼瞼・口腔粘膜に好発し、慢性潰瘍からの発生が多い。"
        "CBC・血液生化学で全身状態評価。外科的切除マージンの術前計画にCTが有用。"
        "UVB過剰曝露との関連が示唆されるため飼育環境歴の聴取も重要。"
    )
}

# tortoise_mycoplasmosis_mycoplasma_agassizii___testudineum: Mycoplasmosis
ENRICHMENTS["tortoise_mycoplasmosis_mycoplasma_agassizii___testudineum"] = {
    "diagnosis_ja": (
        "鼻腔洗浄液PCR（M. agassizii / M. testudineum二重標的）が確定診断の第一選択。"
        "鼻腔スワブは洗浄液より感度が低いが、フィールドでの簡便法として利用可。"
        "血清ELISA（IgM/IgY抗体）で感染既往・活動性を評価。ペア血清の抗体価上昇で急性感染を確認。"
        "鼻腔X線で慢性URTD例の鼻甲介骨溶解を評価。CBC（ヘテロフィル増多→二次細菌感染）。"
        "M. testudineumはヨーロッパリクガメ属に多く、種レベルのPCR鑑別が疫学管理に重要。"
    )
}

# tortoise_pasteurellosis: Pasteurellosis / パスツレラ症
ENRICHMENTS["tortoise_pasteurellosis"] = {
    "diagnosis_ja": (
        "呼吸器分泌物・膿瘍からの好気培養でPasteurella属のグラム陰性短桿菌を分離。"
        "薬剤感受性試験で治療薬選択（ペニシリン系・テトラサイクリン系が一般に有効）。"
        "リクガメでは上部呼吸器感染として発症し、URTDとの鑑別にPCRが有用。"
        "CBC（ヘテロフィル増多→急性細菌感染）、血液生化学で全身状態評価。"
        "X線で肺野混濁・鼻腔の軟部組織腫脹を確認。混合感染（マイコプラズマ・ヘルペスウイルス）の除外検査が推奨。"
    )
}

# tortoise_citrobacter_infection: Citrobacter Infection / シトロバクター感染症
ENRICHMENTS["tortoise_citrobacter_infection"] = {
    "diagnosis_ja": (
        "皮膚潰瘍・甲羅病変・血液からの培養でCitrobacter freundii等を分離同定。"
        "薬剤感受性試験が必須（セファロスポリナーゼ産生による第一世代セフェム耐性が多い）。"
        "SCUD（敗血症性皮膚潰瘍症）の主要起因菌であり、血液培養による敗血症評価が重要。"
        "CBC（ヘテロフィル増多＋毒性変化→全身性感染）、血液生化学（UA→腎障害、AST→肝障害）。"
        "甲羅X線で骨板の骨溶解・深部浸潤を評価。水質・飼育環境の改善が再発防止に不可欠。"
    )
}

# tortoise_0030: Salmonellosis / サルモネラ症（リクガメ）
ENRICHMENTS["tortoise_0030"] = {
    "diagnosis_ja": (
        "糞便の直接培養（SS寒天・XLD培地）でSalmonella属を分離。PCRによる迅速検出も利用可能。"
        "血清型別（Kauffmann-White分類）で疫学的解析。薬剤感受性試験で治療薬選択。"
        "リクガメは高率にサルモネラの無症候性保菌者であり、臨床症状のない個体でも排菌する。"
        "血液培養（敗血症疑い時）。CBC（ヘテロフィル増多→急性炎症）、血液生化学（UA→腎機能、低アルブミン→消耗）。"
        "人獣共通感染症であり、飼育者（特に小児・免疫不全者）への感染リスク評価・衛生指導が診断時に必須。"
    )
}

# tortoise_0114: Melanoma / メラノーマ（リクガメ）
ENRICHMENTS["tortoise_0114"] = {
    "diagnosis_ja": (
        "FNA細胞診で褐色〜黒色のメラニン顆粒を含む多形性細胞を確認。"
        "切除生検による病理組織検査が確定診断に必須（有糸分裂指数・浸潤深度・マージン評価）。"
        "リクガメでは四肢・頸部の皮膚に好発。リンパ節FNA・胸部X線で転移評価。"
        "CT（利用可能時）で局所浸潤範囲と遠隔転移の三次元評価。"
        "CBC・血液生化学で全身状態・麻酔リスク評価。良性メラノサイトーマとの鑑別にKi-67免疫染色が有用。"
    )
}

# tortoise_0123: Hypothermia / 低体温症（リクガメ）
ENRICHMENTS["tortoise_0123"] = {
    "diagnosis_ja": (
        "直腸温（またはプローブ温）の測定でPOTZ下限以下の体温を確認。"
        "血液ガス・電解質検査（低体温時の代謝性アシドーシス・高K血症・低血糖）。"
        "心電図で徐脈・不整脈の評価。CBC・血液生化学で基礎疾患の検索。"
        "冬眠（hibernation）前後の健康診断として糞便検査（寄生虫フリーの確認）・体重測定・"
        "血液検査が推奨。冬眠中の不適切な温度管理（0℃以下の凍結リスク or 10℃以上の中途半端な覚醒）の環境歴聴取が重要。"
    )
}

# tortoise_0001: Tortoise Herpesvirus / リクガメヘルペスウイルス（リクガメ）
ENRICHMENTS["tortoise_0001"] = {
    "diagnosis_ja": (
        "口腔スワブ・鼻腔スワブPCR（リクガメヘルペスウイルスTeHV特異的プライマー）が確定診断の第一選択。"
        "口腔の視診で白色〜黄色の壊死性プラーク・ジフテリー様偽膜を確認（特にギリシャリクガメ・ヘルマンリクガメで重症化）。"
        "血清学（ELISA/SN試験）で抗体検出。ただし潜伏感染個体も抗体陽性のため活動性感染の証明には限界あり。"
        "CBC（ヘテロフィル減少→ウイルス性免疫抑制）、血液生化学（AST→肝障害）。"
        "新規導入個体のPCR検疫スクリーニングが集団管理に不可欠。"
    )
}

# tortoise_0006: Tortoise Ranavirus / リクガメラナウイルス（リクガメ）
ENRICHMENTS["tortoise_0006"] = {
    "diagnosis_ja": (
        "急性の全身性浮腫・皮膚壊死・鼻汁・口腔内出血が臨床的に示唆。"
        "PCR（ラナウイルスMCP遺伝子、口腔・総排泄腔スワブまたは血液）が確定診断に最も有用。"
        "CBC（ヘテロフィル減少・血小板減少→汎血球減少症）、血液生化学（AST・LDH上昇→多臓器障害）。"
        "肝・脾・腎の生検で好塩基性細胞質内封入体を確認。ウイルス分離（FHM・VERO細胞）は研究施設限定。"
        "集団発生時は全個体のPCRスクリーニングと死亡個体の剖検が疫学管理に重要。"
    )
}

# tortoise_0024: Paramyxovirus / パラミクソウイルス（リクガメ）
ENRICHMENTS["tortoise_0024"] = {
    "diagnosis_ja": (
        "呼吸器症状（鼻汁・開口呼吸・粘液過多）＋神経症状（斜頸・旋回・運動失調）が臨床的に示唆。"
        "口腔・気管スワブのRT-PCR（パラミクソウイルス特異的）が生前確定診断の第一選択。"
        "血清学的HI試験でペア血清の抗体価上昇を確認。X線で肺野混濁を評価。"
        "CBC（リンパ球減少→ウイルス性免疫抑制）。リクガメでは致死率が高く、"
        "異種混合飼育（ヘビからの伝播リスク）の飼育歴聴取が重要。"
    )
}

# tortoise_0025: Adenovirus Infection / アデノウイルス感染（リクガメ）
ENRICHMENTS["tortoise_0025"] = {
    "diagnosis_ja": (
        "肝臓FNA/生検で好塩基性核内封入体（カウドリーA型）をH&E染色で確認（確定診断）。"
        "PCR（アデノウイルス特異的プライマー、口腔・総排泄腔スワブ）が生前診断に有用。"
        "血液生化学（AST・LDH著明上昇→肝壊死、UA上昇→腎障害）が重症度の指標。"
        "CBC（ヘテロフィル減少・リンパ球減少→免疫抑制）。超音波で肝腫大を評価。"
        "リクガメでは幼体の急性致死例が多く、死亡個体の剖検・病理が集団管理に重要。"
    )
}

# tortoise_0026: Herpesvirus Infection / ヘルペスウイルス感染（リクガメ）
ENRICHMENTS["tortoise_0026"] = {
    "diagnosis_ja": (
        "口腔スワブPCR（カメヘルペスウイルスChHV特異的）が確定診断の標準法。"
        "口腔粘膜の視診で壊死性口内炎・白色プラーク・ジフテリー様偽膜を確認。"
        "細胞診でGiemsa/Diff-Quik染色にて好酸性核内封入体（カウドリーA型）を検索。"
        "血清ELISA/中和試験で抗体検出（潜伏感染のスクリーニングに有用）。"
        "CBC（ヘテロフィル増多→二次細菌感染、リンパ球減少→ウイルス性免疫抑制）。"
        "マイコプラズマURTD・クラミジアとの混合感染の鑑別PCRが推奨。"
    )
}

# tortoise_0027: Nidovirus Infection / ニドウイルス感染（リクガメ）
ENRICHMENTS["tortoise_0027"] = {
    "diagnosis_ja": (
        "口腔・気管分泌物のRT-PCR（ニドウイルスRdRp遺伝子特異的）が確定診断の第一選択。"
        "X線で肺野のびまん性混濁・肺実質の陰影増強を評価。"
        "気管洗浄液の細胞診（ヘテロフィル・マクロファージ増多）で炎症の性状を確認。"
        "CBC（ヘテロフィル増多→二次細菌感染合併、単球増加→慢性化）。"
        "リクガメではヘビほどの致死率は報告されていないが、ヘルペスウイルス・マイコプラズマとの"
        "混合感染が重症化因子。新規導入個体のPCR検疫が推奨。"
    )
}

# tortoise_0028: Iridovirus (Ranavirus) / イリドウイルス（ラナウイルス）（リクガメ）
ENRICHMENTS["tortoise_0028"] = {
    "diagnosis_ja": (
        "急性〜亜急性の全身性浮腫・皮膚壊死・口腔内出血・多臓器不全が臨床的に示唆。"
        "PCR（ラナウイルスMCP遺伝子、血液・組織・スワブ）が確定診断に最も有用。"
        "CBC（汎血球減少症→骨髄抑制）、血液生化学（AST・LDH著明上昇→多臓器壊死）。"
        "肝・脾の生検で好塩基性細胞質内封入体を確認。剖検で肝脾壊死・出血が特徴的。"
        "リクガメでは幼体で致死率が特に高い。集団死亡例では環境中のウイルスサーベイランスが重要。"
    )
}

# tortoise_0137: Hepatic Bacterial Infection / 肝細菌感染症（リクガメ）
ENRICHMENTS["tortoise_0137"] = {
    "diagnosis_ja": (
        "血液生化学で肝酵素上昇（AST・LDH・GGT）・ビリベルジン上昇（リクガメはビリルビンでなくビリベルジンが主要胆汁色素）を確認。"
        "超音波ガイド下肝FNA/生検の細胞診＋好気・嫌気培養で起因菌を同定。"
        "血液培養（敗血症性肝炎の評価）。CBC（ヘテロフィル増多＋毒性変化→急性細菌感染）。"
        "プラストロン透過光検査で肝腫大・体腔液貯留を非侵襲的に評価。"
        "血液凝固検査（フィブリノーゲン）で凝固障害の合併を確認。"
    )
}

# tortoise_0138: Hepatic Viral Infection / 肝ウイルス感染症（リクガメ）
ENRICHMENTS["tortoise_0138"] = {
    "diagnosis_ja": (
        "血液生化学で肝酵素上昇（AST・LDH）・ビリベルジン上昇を確認。"
        "肝生検の病理組織検査でウイルス性封入体（核内 or 細胞質内）と壊死性肝炎を確認（確定診断）。"
        "PCR（ヘルペスウイルス・アデノウイルス・ラナウイルス特異的）で起因ウイルスを同定。"
        "CBC（リンパ球減少→ウイルス性免疫抑制）。超音波で肝実質エコーパターンの異常・肝腫大を評価。"
        "プラストロン透過光検査が非侵襲的スクリーニングとして有用。"
    )
}

# tortoise_0141: Hepatic Metabolic Disorder / 肝代謝障害（リクガメ）
ENRICHMENTS["tortoise_0141"] = {
    "diagnosis_ja": (
        "血液生化学で肝酵素（AST・LDH・GGT）上昇・ビリベルジン上昇・低アルブミン・"
        "胆汁酸上昇・コレステロール異常値を総合評価。"
        "超音波で肝実質のエコー輝度変化（脂肪肝→高エコー、肝硬変→不均一）を評価。"
        "肝FNA/生検で肝細胞の脂肪変性・壊死・線維化を病理確認。"
        "食餌歴聴取が重要（高蛋白飼料・果物過多→脂肪肝、長期絶食→肝リピドーシス）。"
        "冬眠後の肝機能評価として定期的な生化学モニタリングが推奨。"
    )
}

# tortoise_ranavirus_infection: Ranavirus Infection / ラナウイルス感染症
ENRICHMENTS["tortoise_ranavirus_infection"] = {
    "diagnosis_ja": (
        "PCR（ラナウイルスMCP遺伝子）が確定診断の標準法。検体は口腔・総排泄腔スワブ、血液、または組織。"
        "急性の皮膚壊死・浮腫・口腔内出血・鼻汁の臨床所見が診断を示唆。"
        "CBC（汎血球減少症）、血液生化学（AST・LDH上昇→多臓器障害）。"
        "剖検で肝脾の多巣性壊死と好塩基性細胞質内封入体が確定的所見。"
        "リクガメの集団飼育施設では定期的PCRサーベイランスと新規導入個体の検疫隔離が疫学管理に不可欠。"
    )
}

# tortoise_iridovirus_infection: Iridovirus Infection / イリドウイルス感染症
ENRICHMENTS["tortoise_iridovirus_infection"] = {
    "diagnosis_ja": (
        "PCR（イリドウイルスMCP遺伝子特異的）が確定診断に最も有用。"
        "全身性の浮腫・皮膚壊死・出血傾向・急死が臨床的に示唆。"
        "CBC（汎血球減少→骨髄抑制）、血液生化学（AST・LDH著明上昇→肝脾壊死、UA→腎障害）。"
        "肝・脾の超音波で臓器腫大・実質異常を評価。生検でエオジン好性〜好塩基性封入体を確認。"
        "ラナウイルスとの鑑別にはPCRの塩基配列解析が必要。幼体で致死率が特に高い。"
    )
}

# tortoise_tortoise_intranuclear_coccidia_tinc: TINC
ENRICHMENTS["tortoise_tortoise_intranuclear_coccidia_tinc"] = {
    "diagnosis_ja": (
        "糞便検査では検出困難（腸管寄生ではなく全身性核内寄生）。"
        "肝・腎・脾の生検で核内の発育段階（メロント・ガモント・オーシスト）をH&E染色で確認（確定診断）。"
        "PCR（TINC特異的プライマー、血液または組織）が生前診断に最も有用。"
        "血液生化学（AST・LDH上昇→肝壊死、UA上昇→腎障害）。CBC（ヘテロフィル増多は限定的）。"
        "リクガメ特有の致死性原虫であり、ヘルマンリクガメ・マルギナータリクガメで報告が多い。"
    )
}

# tortoise_intestinal_nematodes_roundworms: Intestinal Nematodes
ENRICHMENTS["tortoise_intestinal_nematodes_roundworms"] = {
    "diagnosis_ja": (
        "糞便浮遊法（飽和食塩水・ショ糖液、比重1.18-1.20）で線虫卵を検出し形態同定。"
        "リクガメの主要線虫：Angusticaecum属（大型回虫）、Tachygonetria属（蟯虫類）。"
        "直接塗抹法で幼虫・虫卵を検索。連日検査（3日間連続採取）で検出感度向上。"
        "大量寄生時はX線で腸管内虫塊・閉塞所見を評価。"
        "CBC・血液生化学で全身状態評価。低蛋白・体重減少は慢性的な栄養吸収障害を示唆。"
    )
}

# tortoise_pinworm_oxyurid_infection: Pinworm (Oxyurid) Infection
ENRICHMENTS["tortoise_pinworm_oxyurid_infection"] = {
    "diagnosis_ja": (
        "糞便浮遊法（ショ糖液・硫酸亜鉛液）で特徴的な非対称形虫卵を検出。"
        "リクガメの蟯虫（Tachygonetria属等）は草食爬虫類に普遍的で、少数寄生は通常非病原性。"
        "直接塗抹法で成虫体（白色線状、5-15 mm）を確認することもある。"
        "臨床症状（下痢・体重減少・食欲不振）は大量寄生時のみ出現。"
        "CBC・血液生化学で全身状態評価。糞便の定期モニタリング（3-6ヶ月毎）が寄生虫量管理に推奨。"
    )
}

# tortoise_flagellate_protozoa_infection: Flagellate Protozoa Infection
ENRICHMENTS["tortoise_flagellate_protozoa_infection"] = {
    "diagnosis_ja": (
        "新鮮糞便の直接塗抹鏡検（加温生理食塩水）で運動性のある鞭毛虫体を確認。"
        "形態学的同定：Hexamita/Spironucleus（左右対称、6鞭毛）がリクガメで最も一般的。"
        "少数の鞭毛虫は正常腸内叢の一部であり、大量増殖時のみ病原性を示す。"
        "ストレス・POTZ逸脱・免疫抑制が増殖の誘因。CBC・血液生化学で基礎疾患の検索。"
        "腎障害（Hexamitaの腎寄生）の評価にUA・iCa測定を追加。治療的診断としてメトロニダゾール投与への反応を評価。"
    )
}

# tortoise_coccidia_infection: Coccidia Infection / コクシジウム症
ENRICHMENTS["tortoise_coccidia_infection"] = {
    "diagnosis_ja": (
        "糞便浮遊法（飽和食塩水・ショ糖液）でコクシジウムオーシストを検出。"
        "オーシスト形態（サイズ・壁厚・スポロシスト数）でEimeria属等を同定。"
        "リクガメでは腸管コクシジウム（糞便検査）とTINC（核内コクシジウム、生検必要）の鑑別が重要。"
        "連日検査（3日間連続採取）で検出感度向上。CBC（ヘテロフィル増多は限定的）、血液生化学（低蛋白→下痢・吸収不良）。"
        "幼体・免疫抑制個体で重症化しやすく、ストレス因子の環境評価が併せて重要。"
    )
}

# tortoise_myiasis_fly_strike: Myiasis (Fly Strike) / 蝿蛆症
ENRICHMENTS["tortoise_myiasis_fly_strike"] = {
    "diagnosis_ja": (
        "創傷部・総排泄腔周囲・甲羅損傷部に寄生するハエ幼虫（蛆）を肉眼的に確認。"
        "幼虫の形態学的種同定（Lucilia、Calliphora、Sarcophaga等）。"
        "創傷の深度評価：蛆の組織侵入範囲（表在性→筋膜到達→体腔穿通）を確認。"
        "CBC（ヘテロフィル増多→二次細菌感染）、血液生化学（低蛋白・UA上昇→敗血症・腎障害）。"
        "基礎疾患の検索（開放創傷・下痢・総排泄腔脱出等が蝿蛆症の誘因）。"
        "屋外飼育環境でのハエ防除対策の評価が再発防止に重要。"
    )
}

# tortoise_liver_failure_hepatopathy: Liver Failure (Hepatopathy) / 肝不全
ENRICHMENTS["tortoise_liver_failure_hepatopathy"] = {
    "diagnosis_ja": (
        "血液生化学でAST・LDH著明上昇、ビリベルジン上昇、低アルブミン、胆汁酸上昇を確認。"
        "超音波ガイド下肝FNA/生検で肝細胞壊死・脂肪変性・線維化・腫瘍性変化を病理評価。"
        "プラストロン透過光検査で肝腫大・体腔液貯留を非侵襲的にスクリーニング。"
        "CBC（ヘテロフィル増多→感染性肝炎、リンパ球減少→ウイルス性）。凝固検査（フィブリノーゲン低下→肝合成能低下）。"
        "鑑別：感染性（細菌・ウイルス・寄生虫）、中毒性、栄養性（脂肪肝）、冬眠後肝障害。"
    )
}

# tortoise_leech_infestation: Leech Infestation / ヒル寄生
ENRICHMENTS["tortoise_leech_infestation"] = {
    "diagnosis_ja": (
        "視診で四肢基部・腋窩・鼠径部・甲羅辺縁の皮膚に付着するヒル体を肉眼的に確認。"
        "ヒル除去後の吸着部位を検査：持続性出血（ヒルジン抗凝固作用）、二次感染兆候。"
        "CBC（貧血→重度寄生時の慢性吸血、ヘテロフィル増多→吸着部位の二次感染）。"
        "ヒル媒介病原体（Haemogregarines等の血液寄生虫）のスクリーニングとして血液塗抹を実施。"
        "屋外飼育環境（池・湿地との接触）の評価が予防管理に重要。"
    )
}

# tortoise_nematode_lung_infection: Nematode Lung Infection / 線虫性肺感染症
ENRICHMENTS["tortoise_nematode_lung_infection"] = {
    "diagnosis_ja": (
        "気管洗浄液の細胞診で肺線虫の虫卵・幼虫（L1）を検出。"
        "糞便検査（Baermann法）で一次幼虫を分離（肺→消化管経路で排出される種の場合）。"
        "X線で肺野の結節影・間質性パターン・気管壁肥厚を評価。"
        "CBC（ヘテロフィル増多→炎症反応）、血液生化学で全身状態評価。"
        "リクガメではRhabdias属等の肺線虫が報告されており、呼吸器症状（開口呼吸・鼻汁）の鑑別に含める。"
        "細菌性肺炎・マイコプラズマURTD・ウイルス性呼吸器感染との鑑別が重要。"
    )
}

# tortoise_paramyxovirus_infection: Paramyxovirus Infection
ENRICHMENTS["tortoise_paramyxovirus_infection"] = {
    "diagnosis_ja": (
        "口腔・気管分泌物のRT-PCR（パラミクソウイルス特異的）が生前確定診断の第一選択。"
        "血清学的HI試験（赤血球凝集抑制試験）でペア血清の抗体価上昇を確認。"
        "X線で肺野混濁・肺実質の陰影増強を評価。気管洗浄液の細胞診で封入体を検索。"
        "CBC（リンパ球減少→ウイルス性免疫抑制、ヘテロフィル増多→二次細菌感染合併）。"
        "リクガメでは呼吸器症状が主体で、致死率が高い。異種爬虫類との混合飼育歴の聴取が疫学的に重要。"
    )
}

# tortoise_poxvirus_infection: Poxvirus Infection / ポックスウイルス感染症
ENRICHMENTS["tortoise_poxvirus_infection"] = {
    "diagnosis_ja": (
        "皮膚の丘疹・結節・痘瘡様病変（灰白色の隆起性病変、臍窩形成）の視診が診断の端緒。"
        "皮膚生検で好酸性細胞質内封入体（ボリンジャー小体様）と表皮の過形成・風船様変性を確認。"
        "電子顕微鏡でレンガ状のポックスウイルス粒子を確認（研究施設限定）。"
        "PCR（ポックスウイルス特異的）が分子診断に有用。"
        "CBC（リンパ球減少→免疫抑制）、血液生化学で全身状態評価。"
        "リクガメでは口腔・鼻腔粘膜にも病変が出現しURTDとの鑑別が必要。"
    )
}

# tortoise_chelonian_herpesvirus_type_1: Chelonian Herpesvirus Type 1
ENRICHMENTS["tortoise_chelonian_herpesvirus_type_1"] = {
    "diagnosis_ja": (
        "口腔スワブPCR（ChHV-1特異的プライマー）が確定診断の標準法。"
        "口腔粘膜の壊死性口内炎・ジフテリー様偽膜・舌壊死が特徴的臨床所見。"
        "細胞診でH&E/Giemsa染色にて好酸性核内封入体（カウドリーA型）を検索。"
        "血清ELISA/中和試験で抗体検出（潜伏感染のスクリーニング）。"
        "CBC（ヘテロフィル増多→二次感染、リンパ球減少→ウイルス性免疫抑制）。"
        "地中海リクガメ属（ギリシャ・ヘルマン・マルギナータ）で特に高致死率。"
    )
}

# tortoise_chelonian_herpesvirus_type_2: Chelonian Herpesvirus Type 2
ENRICHMENTS["tortoise_chelonian_herpesvirus_type_2"] = {
    "diagnosis_ja": (
        "口腔・鼻腔スワブPCR（ChHV-2特異的プライマー、ChHV-1との鑑別を含む）が確定診断に必須。"
        "ChHV-2はChHV-1と比較して上部呼吸器症状（鼻汁・結膜炎）がより顕著で口腔病変は軽度。"
        "細胞診で核内封入体を検索。血清学的にはChHV-1との交差反応があるため、PCRによる型別が重要。"
        "CBC・血液生化学で全身状態評価。マイコプラズマURTDとの混合感染が多く、"
        "鼻腔洗浄液からの両病原体同時PCR検査が推奨。"
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
