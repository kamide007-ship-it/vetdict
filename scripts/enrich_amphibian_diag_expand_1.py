#!/usr/bin/env python3
"""Amphibian diagnosis_ja expansion — batch 1 (28 entries under 150 chars)."""

import json
import os
import time

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["amphibian_0002"] = {
    "diagnosis_ja": "qPCR（皮膚スワブまたは生検）でBsal特異的プライマー使用。Bdとの同時検査（duplex qPCR）が望ましい。組織学的にPAS染色陽性のcolonial thallusと表皮全層性潰瘍を確認。OIE報告対象疾患であり、疑い例では当局報告が必要。野生個体ではスワブの繰り返し採取で感度向上。鑑別: Bd感染症、細菌性皮膚炎、化学的熱傷。"
}

ENRICHMENTS["amphibian_0006"] = {
    "diagnosis_ja": "肉眼的な綿状菌糸の確認で暫定診断。湿潤標本（菌糸を生理食塩水でマウント）で無隔・分枝菌糸を顕微鏡確認。培養はGY agarまたはコーンミール寒天で実施し、遊走子嚢の形態で属レベル同定。鑑別: 細菌性皮膚炎、Aphanomyces、Achlya感染。基礎疾患（外傷、水質悪化、免疫抑制）の評価が重要。水温低下時に発症しやすい。"
}

ENRICHMENTS["amphibian_0023"] = {
    "diagnosis_ja": "肉眼観察で色素異常部位の範囲・形態を記録。細胞診（メラニン顆粒含有細胞を確認）、組織生検でHE染色・メラニン染色（Fontana-Masson）。良性と悪性の鑑別には組織学的評価が必須（核異型、有糸分裂像、浸潤性増殖の有無）。全身評価（X線、超音波）で転移病変の検索。両生類では良性が多いが、経時的サイズ変化のモニタリングが推奨。"
}

ENRICHMENTS["amphibian_0025"] = {
    "diagnosis_ja": "臨床所見（全身性浮腫、腹水）＋水質検査＋穿刺液分析。穿刺液: 透明=リンパ液、混濁=感染、血性=ranavirus/外傷。培養・感受性試験で細菌感染を除外。ranavirus PCR（重症例・集団発生時）。血液検査（腎・肝機能、電解質）、超音波（内臓評価、腹水量推定）。剖検（死亡例）: 腎・肝・脾臓の病理組織評価。心不全・低蛋白血症の鑑別も重要。"
}

ENRICHMENTS["amphibian_0043"] = {
    "diagnosis_ja": "皮膚スクレイピング・KOH直接鏡検で菌糸・分節分生子を確認。サブロー寒天培養（25°C, 2-4週間）で菌種同定。Wood灯検査（Microsporum canisで青緑色蛍光）。分子同定（ITS領域のPCR）で正確な菌種特定。鑑別: ツボカビ症（qPCR必須）、Chromomycosis、細菌性皮膚炎、栄養性皮膚症。免疫抑制個体で日和見感染として発症。"
}

ENRICHMENTS["amphibian_0045"] = {
    "diagnosis_ja": "病変部の細胞診でPAS染色陽性の出芽酵母・偽菌糸を確認。サブロー寒天培養（25-37°C）でクリーム色コロニーを形成、germ tube test陽性でC. albicansを同定。PCR・MALDI-TOF MSで菌種特定。消化管内カンジダは低レベルでは正常フローラの可能性があり、過剰増殖の背景因子（免疫抑制、長期抗菌薬投与）を調査。鑑別: 細菌性口内炎、ツボカビ症。"
}

ENRICHMENTS["amphibian_0066"] = {
    "diagnosis_ja": "確定診断は剖検（漿膜面・腎・肝・心膜の白色尿酸塩結晶沈着）。偏光顕微鏡で針状尿酸結晶確認。生前診断は困難だが、血漿尿酸値↑（正常値は種により異なる）、BUN↑が参考所見。超音波で腎腫大・腎実質高輝度。X線で腎石灰化。飼育環境（脱水、高蛋白食、腎毒性物質）の評価。鑑別: 腎結石（nephrocalcinosis）、腎腫瘍、関節痛風、敗血症。"
}

ENRICHMENTS["amphibian_0067"] = {
    "diagnosis_ja": "関節穿刺→偏光顕微鏡で針状尿酸ナトリウム結晶（負の複屈折）確認が確定診断。X線で関節周囲軟部組織腫脹・骨びらん・石灰化。血漿尿酸値測定（上昇が参考だが正常値でも除外不可）。腎機能評価（BUN、水質検査）。飼育環境・食餌内容の評価が病因特定に重要。鑑別: 細菌性関節炎、外傷、骨折、MBD（代謝性骨疾患）、腫瘍。"
}

ENRICHMENTS["amphibian_0081"] = {
    "diagnosis_ja": "腹部触診で肝腫大、超音波検査・X線で肝実質の不均一性・腫瘤を確認。血液検査: 肝酵素上昇（AST, ALT）、ビリルビン上昇、低アルブミン血症、凝固異常。細胞診（経皮的肝穿刺、出血リスクに注意）、外科的生検・剖検で組織学的確定診断。免疫組織化学で腫瘍型を分類。鑑別: 慢性肝炎、肝肉芽腫、肝嚢胞、他臓器の腫瘤、肝転移。"
}

ENRICHMENTS["amphibian_0106"] = {
    "diagnosis_ja": "X線検査で骨密度低下、成長板の異常拡大、自発骨折、骨皮質の菲薄化を確認。血液検査: イオン化Ca測定（ヘパリン血漿）、総Ca、P、25-(OH)D3、PTH（実施可能な施設）。Ca:P比が1:1未満で示唆的。飼料・サプリメント・UVB環境の問診が診断の鍵。成長期の個体で顕著。鑑別: NSHP、原発性副甲状腺機能亢進症、CKD関連骨症、骨折・外傷。"
}

ENRICHMENTS["amphibian_0118"] = {
    "diagnosis_ja": "細胞診（FNA）でリンパ球系細胞の単一性増殖を確認。組織生検でHE染色＋免疫組織化学（CD3, CD20等のマーカー）でT/B細胞リンパ腫を分類。全身評価（X線、超音波）で内臓病変・リンパ節腫大の検索。血液検査で白血球異常・貧血の有無を評価。両生類では腎臓・肝臓に好発。鑑別: 反応性リンパ過形成、感染性肉芽腫、他の腫瘍（肥満細胞腫等）。"
}

ENRICHMENTS["amphibian_0120"] = {
    "diagnosis_ja": "肉眼観察で潰瘍性・増殖性病変の範囲を記録。細胞診（FNA、scraping）で角化扁平上皮細胞を確認。組織生検でHE染色（細胞異型、角化真珠、浸潤性増殖パターン）。分化度と浸潤深度の評価が予後判定に重要。全身評価（X線、超音波）で転移検索。両生類ではUV曝露との関連が示唆。鑑別: 慢性肉芽腫、感染性潰瘍、乳頭腫、他の上皮性腫瘍。"
}

ENRICHMENTS["amphibian_0121"] = {
    "diagnosis_ja": "肉眼観察で腫瘤の大きさ・位置・増殖速度を記録。超音波・X線で腫瘤評価と周囲組織浸潤を確認。細胞診（FNA）、組織生検でHE染色（紡錘形細胞の束状配列、herring-bone pattern）、免疫染色（vimentin陽性、desmin陰性）。核分裂像の計数でグレード評価。全身評価で転移検索。鑑別: 線維腫（良性）、神経鞘腫、平滑筋肉腫、その他の間葉系腫瘍。"
}

ENRICHMENTS["amphibian_0122"] = {
    "diagnosis_ja": "肉眼観察で色素性病変の範囲・色調・表面性状を記録。細胞診でメラニン顆粒含有細胞を確認。組織生検でHE染色＋メラニン染色（Fontana-Masson）＋免疫染色（S-100, Melan-A, HMB-45）。良性/悪性の判定には核異型度・核分裂像・浸潤パターンが重要。全身評価で転移検索。鑑別: 良性色素性腫瘤、慢性炎症性色素沈着、クロマトフォーマ。"
}

ENRICHMENTS["amphibian_0124"] = {
    "diagnosis_ja": "X線検査で骨破壊・骨形成混在像（sunburst pattern等）、軟組織腫脹を確認。細胞診（FNA）、組織生検でHE染色（骨芽細胞性異型細胞、類骨・骨様組織形成が確定所見）。アルカリフォスファターゼ免疫染色が補助的。胸部X線で肺転移検索。血液検査でALP上昇の可能性。鑑別: 骨折（修復過程）、骨炎、骨髄炎、転移性骨腫瘍、軟骨肉腫。"
}

ENRICHMENTS["amphibian_0128"] = {
    "diagnosis_ja": "血液検査でイオン化Ca測定（基準値 種により1.0-1.4 mmol/L）が最も信頼性が高い。総Ca測定（タンパク質補正が必要）、P、Mg、アルブミン併測。Ca:P比の逆転は重度を示唆。病歴（食事内容、UVB環境、繁殖状況、カルシウム補給）の聴取が重要。ECG（実施可能な施設）で心不整脈評価。テタニー症状（筋痙攣）は緊急対応が必要。鑑別: 中毒、神経疾患。"
}

ENRICHMENTS["amphibian_0129"] = {
    "diagnosis_ja": "血液検査でP（基準値 種により2-4 mg/dL）、Ca、Ca×P積（>60 mg²/dL²で軟組織石灰化リスク）、BUN、Cr測定。X線で骨格・腎臓の石灰化評価。尿検査（実施可能な水生種）でリン排泄を評価。病歴聴取（食事内容、サプリメント使用、特に高リン食品の給餌頻度）。腎不全の合併評価が重要。鑑別: 腎性骨異栄養症、NSHP、内臓痛風。"
}

ENRICHMENTS["amphibian_0130"] = {
    "diagnosis_ja": "臨床所見（皮膚turgor低下、眼球陥凹、体重減少、活動性低下）で暫定診断。体重変化（脱水%推定: 前体重との比較が理想）。血液検査: PCV↑（血液濃縮）、総蛋白↑、BUN↑、尿酸↑（腎前性高窒素血症）。環境湿度・温度測定が水生種・陸生種で必須。尿酸結晶沈着の有無（痛風合併リスク）。鑑別: 慢性消耗性疾患、腎疾患、痛風、感染症。"
}

ENRICHMENTS["amphibian_acanthocephalan_infection"] = {
    "diagnosis_ja": "糞便沈殿法で特徴的な厚壁卵（楕円形、60-100 × 30-50 μm、卵殻内に有刺幼虫を含む）を確認。間欠排卵のため繰り返し検査が必要。剖検では腸壁に固着した成虫を確認（吻の有刺構造が腸壁を穿通）。組織学的に吻周囲の肉芽腫性炎症。重度感染では腸穿孔・腹膜炎のリスク。鑑別: 他の消化管線虫、コクシジウム症、腸管腫瘍。"
}

ENRICHMENTS["amphibian_ammonia_poisoning"] = {
    "diagnosis_ja": "水質検査（最重要）: 総アンモニア（NH3+NH4+）、pH、温度測定で非イオン化NH3濃度を計算（Henderson-Hasselbalch式）。NH3 >0.02 mg/Lで毒性域。市販水質検査キット（NH3/NH4+試薬）の即時使用。病歴聴取（最近の換水、新規水槽、給餌量、死体の有無、フィルター状態）。鑑別: 亜硝酸中毒、塩素中毒、低酸素症、感染症。"
}

ENRICHMENTS["amphibian_axolotl_floating_disorder"] = {
    "diagnosis_ja": "浮遊の持続時間・パターン確認（一過性 vs 持続性、体位）。腹部触診: ガス貯留、便塊、卵塊の触知。水質検査（アンモニア・亜硝酸・水温・pH）。食事歴の詳細聴取（最近の給餌内容・頻度）。X線: 消化管ガス像、便秘、卵詰まり、腹水評価。超音波で腹腔内臓器を精査。鑑別: 腹水（腎不全）、卵詰まり、腫瘍、正常な一過性浮遊（空気嚥下後）。"
}

ENRICHMENTS["amphibian_basidiobolus_infection"] = {
    "diagnosis_ja": "病変部の組織生検でPAS・GMS染色陽性の幅広（8-20 μm）の隔の少ない菌糸を確認。Splendore-Hoeppli現象（菌糸周囲の好酸性沈着物）が特徴的所見で診断の鍵。サブロー寒天培養（25-30°C）で2-7日でコロニー形成、衛星コロニア（satellite colony）パターン。PCR（ITS領域）で菌種特定。鑑別: ムコール症、アスペルギルス症、細菌性肉芽腫。"
}

ENRICHMENTS["amphibian_capillariasis"] = {
    "diagnosis_ja": "糞便浮遊法・直接塗抹で特徴的な両端卵蓋を持つ卵（樽型、35-50 × 20-25 μm）を確認。Trichuris卵との形態的鑑別が必要。繰り返し検査が重要（間欠的排卵）。剖検例では消化管粘膜から成虫を確認。重度感染では粘膜肥厚・出血性腸炎を認める。鑑別: 他の消化管線虫（Strongyloides, Rhabdias）、コクシジウム症、消化管原虫感染。"
}

ENRICHMENTS["amphibian_chemical_toxicity_pesticides_metals"] = {
    "diagnosis_ja": "病歴聴取（暴露源、農薬使用歴、容器・装飾品材質、水源、近隣の農地・工場）が最重要。水・基材・組織の毒性検査（実施可能な専門機関への送付）。血液中コリンエステラーゼ活性測定（有機リン/カーバメイト中毒）、重金属定量（鉛、銅、亜鉛）。臨床症状の経時記録。鑑別: 感染症、栄養性疾患、外傷、低酸素症、水質悪化。"
}

ENRICHMENTS["amphibian_chlorine___chloramine_toxicity"] = {
    "diagnosis_ja": "水質検査で遊離塩素（Cl2）、結合塩素（クロラミン）測定（DPD法、市販キット）。遊離塩素 >0.01 mg/Lで両生類に毒性。病歴聴取（最近の換水、使用水源、脱塩素処理の有無、コンディショナー使用量）。臨床症状は急性: 鰓の充血・壊死、皮膚発赤、異常行動。鑑別: アンモニア中毒、亜硝酸中毒、感染症、急性低酸素症。即座の水換えが治療の第一歩。"
}

ENRICHMENTS["amphibian_chronic_dehydration_terrestrial_species"] = {
    "diagnosis_ja": "飼育環境の湿度・温度記録の確認（種別適正範囲との比較）。体重推移（経時的減少は脱水を示唆）。皮膚の質感・弾力評価（乾燥、しわ、turgor低下）。血液検査: BUN↑、尿酸↑（慢性腎障害の合併）、PCV↑（血液濃縮）。X線/超音波: 腎石灰化、痛風結節。環境アセスメント（水場、隠れ場所、基質の保湿性）が診断と治療の鍵。"
}

ENRICHMENTS["amphibian_fusarium_infection"] = {
    "diagnosis_ja": "病変部の細胞診・組織生検でPAS・GMS染色陽性の隔のある分枝菌糸とマクロコニジア（カヌー型、多細胞性）を確認。サブロー寒天培養（25-30°C）でわらた色〜紫色のコロニー形成。PCR（TEF1-α遺伝子）で菌種特定が必須（耐性菌株の鑑別に重要、F. solaniは多剤耐性）。鑑別: アスペルギルス症、カンジダ症、細菌性肉芽腫、ムコール症。"
}

ENRICHMENTS["amphibian_hemolytic_anemia"] = {
    "diagnosis_ja": "PCV低下＋血漿の溶血所見（ピンク〜赤色血漿）で溶血を確認。血液塗抹: 赤血球形態異常（Heinz body、球状赤血球）、寄生虫（Trypanosoma等）、多染性赤血球（再生性の証拠）。鑑別: 非再生性貧血（慢性感染、栄養欠乏）、出血性貧血。水質検査（重金属・塩素・pH・アンモニア）。環境中の毒素スクリーニング。原因特定が治療方針決定に不可欠。"
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
