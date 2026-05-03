#!/usr/bin/env python3
"""Amphibian diagnosis_ja expansion — batch 2 (28 entries under 150 chars)."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["amphibian_hepatocellular_carcinoma"] = {
    "diagnosis_ja": "腹部触診で肝腫大を確認。超音波検査・X線で肝実質の不均一性・腫瘤・腹水を確認。血液検査: 肝酵素上昇（AST, ALT）、ビリルビン上昇、低アルブミン、凝固異常。細胞診（経皮的肝穿刺、出血リスクに注意）、外科的生検・剖検で組織学的確定診断（特徴的な肝細胞異型、偽腺管構造）。免疫組織化学でHepPar-1等のマーカーを評価。鑑別: 慢性肝炎、肝肉芽腫、他の肝腫瘍、肝転移。"
}

ENRICHMENTS["amphibian_high_nitrate_toxicity"] = {
    "diagnosis_ja": "水質検査で硝酸塩（NO3-）濃度測定（市販キット、定期検査）。両生類では>40 mg/Lで慢性毒性、>200 mg/Lで急性症状。病歴聴取（換水頻度、飼育密度、給餌量、フィルター管理、水源の硝酸塩レベル）。慢性曝露では免疫抑制・成長遅延として顕在化。鑑別: アンモニア・亜硝酸中毒、慢性栄養性疾患、感染症、奇形原因の他要因（吸虫被嚢等）。"
}

ENRICHMENTS["amphibian_hypoglycemia"] = {
    "diagnosis_ja": "血液検査でグルコース測定（基準値 種により30-90 mg/dL）。携帯型血糖計を使用可能だがキャリブレーションに注意。病歴聴取（絶食期間、温度管理、慢性疾患の有無、最近のストレス要因）。低体温との複合評価が重要（変温動物のため環境温度低下でエネルギー消費パターンが変化）。鑑別: 中毒、外傷、感染症、低Ca血症テタニー、低体温症、肝不全、敗血症。"
}

ENRICHMENTS["amphibian_hypovitaminosis_a"] = {
    "diagnosis_ja": "臨床症状（特に短舌症候群: 舌の突出不全による捕食困難）と病歴（食事内容、サプリメント使用、β-カロテン含有飼料の割合）から推定診断。血液中レチノール測定（実施困難で臨床的には未普及）。病理組織学的検査で皮膚・口腔粘膜の扁平上皮化生を確認。ビタミンA投与への反応で臨床的確定。鑑別: NSHP、口腔感染症、神経学的疾患、外傷性舌損傷。"
}

ENRICHMENTS["amphibian_ichthyophthirius_white_spot_disease"] = {
    "diagnosis_ja": "白色斑点の肉眼確認＋皮膚スクレイピングの顕微鏡検査で馬蹄形核を持つ大型繊毛虫（trophont: 0.5-1 mm）を確認。鰓のwet mountも有用（鰓感染は致死的）。ライフサイクル理解が治療に必須（theront遊走子段階のみが薬剤感受性）。水温記録（ライフサイクル速度に影響）。鑑別: ツボカビ症、サプロレグニア感染、Costia感染、Trichodina感染。"
}

ENRICHMENTS["amphibian_iodine_deficiency_goiter"] = {
    "diagnosis_ja": "頸部触診で甲状腺腫を確認（両側対称性の腫大が典型的）。病歴（飼料内容、ヨウ素含有サプリメント使用、goitrogenを含む植物の給餌）の聴取。血液中T3・T4測定（実施可能な施設、両生類の基準値データは限定的）。幼生では変態遅延（給餌・温度適切なのに変態しない）が示唆所見。剖検で甲状腺過形成を組織学的に確認。鑑別: 他の代謝性疾患、外傷性頸部腫脹、新生物。"
}

ENRICHMENTS["amphibian_leech_infestation"] = {
    "diagnosis_ja": "肉眼でヒルの直接確認（体表の丁寧な観察が必要）。皮膚の皺・指間部・腋窩・総排泄孔・口腔内を重点的に確認。付着部位の潰瘍・出血点も確認。貧血評価のため血液検査（PCV測定）。重度寄生では著明なPCV低下。Trypanosoma感染合併（ヒルが媒介）の可能性あり、血液塗抹検査（Giemsa染色）推奨。飼育水中の野外採取物から侵入することが多い。"
}

ENRICHMENTS["amphibian_limb_deformity_developmental"] = {
    "diagnosis_ja": "肉眼的観察で奇形の分類（多肢症、欠肢症、短肢症、骨癒合等）。X線で骨格構造の詳細評価。寄生虫検査: metacercariae（吸虫Ribeiroia ondatrae等の幼虫）の四肢組織内確認（組織学）。飼育歴: 栄養・水質・親個体の遺伝的背景。集団発生→環境要因（寄生虫・化学物質・UV-B異常）を優先的に調査。孤発例は遺伝性・栄養性を考慮。"
}

ENRICHMENTS["amphibian_limb_fractures___trauma"] = {
    "diagnosis_ja": "視診・触診で骨折部位・種類（開放/閉鎖、単純/粉砕）の評価。X線で確定診断（骨折線、転位度、骨密度評価）。MBD（代謝性骨疾患）評価: X線での全身骨密度低下、血漿Ca・P・ビタミンD測定。病的骨折（MBD、痛風、腫瘍による骨脆弱性）の除外が重要。外傷歴の聴取。鑑別: 脱臼、軟部組織損傷単独、痛風結節、腫瘍、MBDに伴う自発骨折。"
}

ENRICHMENTS["amphibian_metamorphosis_failure_neoteny_complications"] = {
    "diagnosis_ja": "種の同定（幼形成熟種 vs 非幼形成熟種の確認が最重要: Axolotlは正常な幼形成熟）。発育段階（Gosner staging）の評価。飼育環境・水温・栄養歴の確認。甲状腺ホルモン（T3/T4）測定（技術的に困難だが参考）。水質検査（ヨウ素濃度、過塩素酸塩の汚染評価）。T4投与への反応試験が臨床的確定に有用。鑑別: 正常な幼形成熟（Axolotl等）、栄養性成長遅延、甲状腺腫。"
}

ENRICHMENTS["amphibian_mucormycosis"] = {
    "diagnosis_ja": "病変部の細胞診・組織生検でPAS染色・GMS染色陽性の幅広（10-20 μm）の無隔または希疎隔菌糸を確認（直角分枝が特徴的）。サブロー寒天培養（25-37°C）で1-3日で急速にコロニー形成。PCR（ITS, 28S rRNA領域）で菌種特定。血管侵入性の評価が予後に重要。鑑別: アスペルギルス症（菌糸の隔と45度分枝角度で鑑別）、Basidiobolus感染、細菌性壊死性皮膚炎。"
}

ENRICHMENTS["amphibian_myxosporean_infection"] = {
    "diagnosis_ja": "尿検査・体腔液検査での胞子確認（顕微鏡下に二極性胞子嚢を観察、種により胞子形態が異なる）。病理組織学検査でシストと胞子を確認（腎尿細管内に好発）。PCR（18S rRNA領域）で種同定（Myxobolus, Myxidium等）。剖検で腎腫大・白色結節を確認。慢性感染では腎機能低下（BUN↑）。鑑別: 細菌性腎炎、ラナウイルス、毒性腎症、内臓痛風。"
}

ENRICHMENTS["amphibian_neoplasia___tumors"] = {
    "diagnosis_ja": "全身検査: 触診、視診でサイズ・位置・増殖速度を記録。X線、超音波検査で深部腫瘤・転移を評価。細胞診（FNA）で暫定診断、組織生検でHE染色＋必要な特殊染色・免疫組織化学で確定。全身評価で転移検索、組織型・グレード・ステージ判定。両生類では良性腫瘍が比較的多い。鑑別: 感染性肉芽腫、肉芽腫性炎症、良性過形成、嚢胞、膿瘍。"
}

ENRICHMENTS["amphibian_nephrocalcinosis"] = {
    "diagnosis_ja": "X線: 腎臓の石灰化像（両側性高輝度領域が特徴的）。超音波: 腎実質の高エコー病変（音響陰影を伴うこともある）。血液検査: BUN↑、尿酸↑、Ca/P比異常、電解質異常。確定診断: 剖検（腎実質の白色石灰化斑）、病理組織でvon Kossa染色陽性のカルシウム沈着。飼育環境・食餌内容の評価が原因特定に重要。鑑別: 内臓痛風（尿酸沈着）、腎腫瘍、腎膿瘍。"
}

ENRICHMENTS["amphibian_nitrite_poisoning"] = {
    "diagnosis_ja": "水質検査で亜硝酸（NO2-）濃度測定（市販キット）。>0.5 mg/Lで毒性域。メトヘモグロビン血症の評価: 血液色の褐色化（チョコレート色）、PCV正常だが酸素運搬能低下。病歴聴取（換水状況、フィルター管理、新規水槽セットアップ — 窒素サイクル未確立）。鑑別: アンモニア中毒、低酸素症、感染症、出血。新規水槽症候群の一部として発症が典型的。"
}

ENRICHMENTS["amphibian_nutritional_secondary_hyperparathyroidism"] = {
    "diagnosis_ja": "X線検査で骨密度低下、骨皮質菲薄化、自発骨折、成長板異常拡大、椎骨・四肢の変形を確認。「ゴム顎」様の下顎軟化が特徴的。血液検査: イオン化Ca（低〜正常）、総Ca、P（上昇）、Ca×P積、25-(OH)D3（低下）、PTH上昇（実施可能な施設）。病歴聴取（食事のCa:P比、UVB環境）が診断の鍵。鑑別: 原発性副甲状腺機能亢進症、CKD関連骨症、外傷性骨折。"
}

ENRICHMENTS["amphibian_obesity"] = {
    "diagnosis_ja": "BCS（Body Condition Score）評価（理想: 3/5、肥満: 4-5/5）。体重測定と種別標準体重との比較。X線/超音波: 腹腔内脂肪体の評価、肝臓サイズ・エコー性（脂肪肝の有無）。血漿生化学: コレステロール↑、トリグリセリド↑、AST↑（肝リピドーシス併発時）。食事歴・給餌頻度・餌種類の詳細聴取。飼育環境評価（運動量、温度、スペース）。合併症としての脂肪肝・心臓疾患の評価。"
}

ENRICHMENTS["amphibian_oxyurid_pinworm_infection"] = {
    "diagnosis_ja": "糞便浮遊法または直接塗抹で特徴的な平側に偏った卵（asymmetric, 100-150 × 30-50 μm）を確認。総排泄孔周囲のセロハンテープ法も有用（Pinworm test）。剖検では大腸内成虫を確認。多くの両生類では低レベル感染は非病原性（常在虫）。重度感染時のみ臨床症状を呈する。鑑別: 他の消化管線虫（Capillaria, Strongyloides）、コクシジウム症。"
}

ENRICHMENTS["amphibian_perkinsea_infection"] = {
    "diagnosis_ja": "肝臓・腎臓・脾臓の組織学的検査で原生生物の組織内増殖を確認（特徴的な多核性栄養体）。PCR（18S rRNA領域）で病原体特定。死亡個体の剖検で肝腫大・脾腫・体腔液貯留を認める。集団死亡（mass mortality event）では本疾患を強く疑う。血液塗抹検査も補助的に有用。鑑別: ラナウイルス感染症、エロモナス症、ツボカビ症（成体期）、細菌性敗血症。"
}

ENRICHMENTS["amphibian_protein_deficiency"] = {
    "diagnosis_ja": "病歴（飼料内容、給餌頻度、餌の種類と栄養価）と臨床症状（体重減少・成長遅延・体型評価）から推定診断。血液検査: 総タンパク低下（基準値 種により3-6 g/dL）、アルブミン低下、グロブリン低下。BCS（Body Condition Score）評価で筋肉量減少を確認。免疫機能低下による日和見感染の合併を評価。鑑別: 慢性消耗性疾患、寄生虫感染、新生物、CKD。"
}

ENRICHMENTS["amphibian_rhabdias_lungworm"] = {
    "diagnosis_ja": "糞便浮遊法・Baermann法で幼虫（rhabditiform larva, 約0.3 mm）を確認。気管・肺洗浄液の顕微鏡検査も有用（成虫の直接確認）。胸部X線で肺野の浸潤影・結節影。剖検では肺胞内の成虫を確認。自家感染（autoinfection）サイクルにより免疫抑制個体で重症化。鑑別: Strongyloides感染、細菌性肺炎、真菌性肺炎、肺腫瘍。"
}

ENRICHMENTS["amphibian_saprolegniasis"] = {
    "diagnosis_ja": "肉眼的な綿状菌糸の確認で暫定診断。湿潤標本（生理食塩水でマウント）顕微鏡検査で無隔・分枝菌糸を確認。GY agar培養で診断確定し、遊走子嚢形態で属レベル同定。分子同定（ITS領域PCR）で種レベル同定が可能。鑑別: Aphanomyces, Achlya感染（形態的に類似）、細菌性皮膚炎。基礎疾患（外傷・水質悪化・低栄養・低温ストレス）の評価が治療に必須。"
}

ENRICHMENTS["amphibian_strongyloides_infection"] = {
    "diagnosis_ja": "糞便Baermann法で活動性の幼虫（rhabditiform larva, 約0.25 mm）を確認。新鮮糞便の直接塗抹も有用（排卵後速やかに孵化するため卵より幼虫で検出）。PCRで種同定。自由生活世代と寄生世代の交代があり、環境評価（基材の汚染度）も重要。重度感染では消化管粘膜の炎症・びらん。鑑別: Rhabdias肺虫症（幼虫形態が類似）、Capillariasis。"
}

ENRICHMENTS["amphibian_thiamine_deficiency"] = {
    "diagnosis_ja": "病歴（魚類単食、特に冷凍キビナゴ・ワカサギ等のチアミナーゼ含有魚）と臨床症状（神経症状: 運動失調、振戦、後弓反張）から推定診断。チアミン投与への治療反応で確定診断（24-48時間以内に劇的改善は本疾患に特異的）。血液中チアミン測定（赤血球トランスケトラーゼ活性、実施困難で臨床的には未普及）。鑑別: 中毒（重金属、殺虫剤）、感染性脳炎、外傷、低Ca血症テタニー。"
}

ENRICHMENTS["amphibian_trematode_encystment_heavy_burden"] = {
    "diagnosis_ja": "肉眼的に四肢奇形・皮下嚢胞の評価。皮下・腎臓のwet mountまたは組織生検でメタセルカリア（被嚢、楕円形、200-500 μm）を確認。被嚢壁の構造で寄生虫種の推定が可能。剖検では腎被嚢の集積を肉眼確認。PCR・形態学的検査で吸虫種同定（Ribeiroia ondatrae等）。野外集団での発生パターンが疫学的に重要。鑑別: MBD関連奇形、化学物質による催奇形性、遺伝性奇形。"
}

ENRICHMENTS["amphibian_trypanosomiasis"] = {
    "diagnosis_ja": "末梢血塗抹（Giemsa染色）で典型的な鞭毛虫を確認（細長く、波動膜と鞭毛を持つ、20-60 μm）。血液濃縮法（Knott法またはmicrohematocrit法）で低寄生虫血症の検出感度向上。PCR（18S rRNA領域）で種同定。貧血評価のためPCV測定。媒介者（ヒル、吸血性節足動物）の存在確認。多くの両生類では低レベル感染は非病原性。鑑別: microfilaria、他の血液原虫。"
}

ENRICHMENTS["amphibian_vitamin_e_deficiency"] = {
    "diagnosis_ja": "病歴（飼料内容、特に魚類単食や酸化した飼料の使用）と臨床症状（steatitis: 皮下硬結、活動性低下）から推定診断。皮下硬結の細胞診・組織生検でリポフスチン沈着と肉芽腫性炎症（ceroid/lipofuscin沈着を伴う脂肪織炎）を確認。血液中ビタミンE測定（α-tocopherol, 実施困難）。ビタミンE投与への治療反応で臨床的確定。鑑別: 細菌性肉芽腫、真菌性脂肪織炎、新生物。"
}

ENRICHMENTS["amphibian_zinc_toxicosis"] = {
    "diagnosis_ja": "血液中亜鉛濃度測定（基準値 種により異なるが>200 μg/dLで毒性域）。血液検査: 溶血性貧血（PCV低下）、Heinz body形成、ヘモグロビン尿。X線で消化管内不透過性物質（亜鉛メッキ部品、コイン等）を確認。病歴聴取（容器の材質、装飾品、暴露源の特定）。急性曝露と慢性曝露で臨床像が異なる。鑑別: 他の重金属中毒（鉛、銅）、感染性溶血、自己免疫性溶血、塩素中毒。"
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
