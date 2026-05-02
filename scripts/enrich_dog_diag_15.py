#!/usr/bin/env python3
import json
import os
import time

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diseases_all_species.json")

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_acquired_myasthenia_gravis_focal"] = {"diagnosis_ja": (
    "抗AChR（アセチルコリン受容体）抗体価上昇が確定診断（感度85-90%）。ELISA法で測定。"
    "局所型: 食道（巨大食道症）、咽頭（嚥下困難）、顔面（表情筋）の限局性筋力低下。"
    "テンシロン（エドロフォニウム）試験で一過性の症状改善。EMGで漸減反応（decremental response）。"
    "胸部X線で巨大食道症と吸引性肺炎。前縦隔腫瘤（胸腺腫: 3-5%で合併）をCTで評価。"
)}

ENRICHMENTS["dog_hepatocutaneous_syndrome_snd"] = {"diagnosis_ja": (
    "皮膚生検で表皮の赤白青の三層パターン（red-white-blue pattern: 錯角化+浮腫+過角化）を確認。"
    "腹部超音波で肝臓の「ハチの巣」様エコーパターン（Swiss cheese/honeycomb pattern）が特徴的。"
    "血液検査で低アミノ酸血症（複数アミノ酸低値）。ALP/ALT上昇、低アルブミン血症、高NH3。"
    "肉球のひび割れ・過角化、口周囲・眼周囲・圧迫部位の紅斑・痂皮が特徴。アミノ酸輸液が治療。"
)}

ENRICHMENTS["dog_idiopathic_head_tremor_syndrome"] = {"diagnosis_ja": (
    "ビデオ記録で反復性の頭部振戦（vertical「yes-yes」/horizontal「no-no」/rotational）を確認。"
    "意識レベル正常、振戦中も注意の転換で停止可能（てんかん発作との鑑別点）。"
    "MRI/CTで構造的脳病変を除外。脳波（EEG）でてんかん性放電なし。CBC/生化学正常。"
    "ブルドッグ、ドーベルマン、ラブラドールに好発。良性の経過。治療不要の場合が多い。"
)}

ENRICHMENTS["dog_idiopathic_chylothorax"] = {"diagnosis_ja": (
    "胸腔穿刺で乳白色の胸水を回収。胸水のTG（トリグリセリド）>100 mg/dL、胸水TG>血清TG。"
    "胸水の細胞診でリンパ球優位。コレステロール/TG比<1.0で乳び胸を確定。"
    "リンパ管造影/CT angiographyで胸管の走行・漏出部位を評価。心エコーで心疾患を除外。"
    "基礎疾患（心膜炎、右心不全、前縦隔腫瘤、外傷）を除外→特発性。アフガン・ハウンド、柴犬に好発。"
)}

ENRICHMENTS["dog_canine_leproid_granuloma"] = {"diagnosis_ja": (
    "皮膚生検で真皮の結節性肉芽腫性炎症と、Ziehl-Neelsen染色で抗酸菌を確認。"
    "FNA/生検で類上皮細胞・多核巨細胞（Langhans型）の肉芽腫。PCRで非結核性抗酸菌を同定。"
    "CBC/生化学は概ね正常。リンパ節のFNAで播種性を除外。"
    "耳介の無痛性結節が特徴的。ボクサー、ダックスフンドに好発。自然退縮する場合あり。リファンピシン/クラリスロマイシン。"
)}

ENRICHMENTS["dog_canine_distemper_-_hardpad_disease"] = {"diagnosis_ja": (
    "身体検査で肉球・鼻鏡の角化亢進（hyperkeratosis）を確認。ジステンパー感染の慢性後遺症。"
    "血液/結膜スワブのRT-PCRでCDV RNAを検出。免疫蛍光法（IFA）で確認。"
    "MRIでCNS病変（脱髄性白質脳炎）を評価。CSFで抗CDV抗体/PCR。"
    "ワクチン未接種歴の確認。急性期の鼻汁・結膜炎→CNS症状（ミオクローヌス、痙攣）→硬蹠症の経過。"
)}

ENRICHMENTS["dog_cranial_cruciate_ligament_rupture"] = {"diagnosis_ja": (
    "整形外科検査で前方引き出し試験（cranial drawer test）陽性と脛骨圧迫試験陽性を確認。"
    "X線で関節液貯留（脂肪パッド変位）、骨棘形成（慢性例）を確認。脛骨高平部角（TPA）測定。"
    "MRIで靭帯の断裂と半月板損傷を評価。関節液検査で非感染性炎症を確認。"
    "中～大型犬に好発。TPA>30°はTPLO適応。半月板の内側メニスカス損傷（50-70%で合併）の術中評価。"
)}

ENRICHMENTS["dog_medial_patellar_luxation"] = {"diagnosis_ja": (
    "整形外科検査で膝蓋骨の内方脱臼を確認。Putnamグレーディング（I: 手動脱臼→自然整復、"
    "II: 手動or自然脱臼→手動整復、III: 常時脱臼→手動整復可、IV: 常時脱臼→整復不能）。"
    "X線で膝蓋骨の位置、脛骨粗面の内側変位、大腿骨溝の浅さを確認。"
    "小型犬（ポメラニアン、チワワ、ヨークシャー・テリア）に好発。Grade II以上で手術適応。"
)}

ENRICHMENTS["dog_legg-calve-perthes_disease"] = {"diagnosis_ja": (
    "X線（VD view）で大腿骨頭の不整・骨透亮・扁平化を確認。初期は微細な骨密度低下のみ。"
    "CT/MRIで大腿骨頭の虚血性壊死の範囲と関節適合性を評価。"
    "触診で股関節の疼痛・可動域制限・クレピタスを確認。ROM測定。"
    "小型犬（ヨークシャー・テリア、ミニチュア・プードル、ウエスティ）の成長期（4-12ヶ月）に好発。大腿骨頭切除術。"
)}

ENRICHMENTS["dog_fragmented_coronoid_process"] = {"diagnosis_ja": (
    "CT三次元再構成で内側鉤状突起の骨折・断片化を確認（X線より高感度）。"
    "X線で二次性OA変化（骨棘形成）を確認。直接的な断片描出はX線では困難。"
    "関節鏡で断片の直接確認と摘出。関節液検査で非感染性炎症。"
    "肘関節形成不全の一型。ラブラドール、ゴールデン、ロットワイラーの成長期（5-9ヶ月）に好発。"
)}

ENRICHMENTS["dog_cervical_spondylomyelopathy_wobbler_syndrome"] = {"diagnosis_ja": (
    "MRIで頸椎の脊柱管狭窄・脊髄圧迫を確認。椎間板突出/骨性狭窄の鑑別。"
    "頸部X線で椎体の変形・椎間板腔の狭小化。ストレスビュー（屈曲/伸展）で動的圧迫を評価。"
    "脊髄造影+CT myelographyで圧迫の程度を三次元評価。CSF正常。"
    "ドーベルマン（椎間板型: C5-C7）、グレート・デーン（骨関節型: C3-C5）。頸部疼痛+進行性後肢不全麻痺。"
)}

ENRICHMENTS["dog_lumbosacral_stenosis"] = {"diagnosis_ja": (
    "MRIでL7-S1椎間板の突出/脱出と馬尾圧迫を確認。T2高信号の神経根病変。"
    "CT myelographyで硬膜嚢/神経根の圧迫を評価。X線で腰仙関節の変性変化。"
    "神経学的検査で尾部の疼痛、排尿/排便障害、後肢筋萎縮を確認。"
    "腰仙部の過伸展で疼痛誘発。ジャーマン・シェパード等の大型犬に好発。保存療法or外科的減圧。"
)}

ENRICHMENTS["dog_granulomatous_meningoencephalomyelitis_gme"] = {"diagnosis_ja": (
    "MRIで脳実質の多発性/単発性の造影増強病変を確認。白質優位のT2/FLAIR高信号。"
    "CSF検査で単核球優位の中等度～高度細胞数増多（50-500/μL）、蛋白上昇。"
    "感染性脳炎（CDV、真菌、原虫）をPCR/血清学で除外。脳生検で血管周囲の肉芽腫性炎症を確認。"
    "トイプードル、テリア系の小型犬に好発。限局型（optic型含む）vs播種型。免疫抑制療法（プレドニゾロン+ara-C/シクロスポリン）。"
)}

ENRICHMENTS["dog_necrotizing_meningoencephalitis_pug_dog_encephalitis"] = {"diagnosis_ja": (
    "MRIで大脳皮質の非対称性T2/FLAIR高信号と壊死性変化を確認。造影後増強。"
    "CSF検査で単核球優位の細胞数増多、蛋白上昇。抗GFAPα抗体が特異的。"
    "感染性脳炎をPCR/血清学で除外。脳生検で壊死性炎症を確認。"
    "パグに好発（Pug Dog Encephalitis: PDE）。急性進行性の痙攣・失明・旋回。予後不良。免疫抑制療法。"
)}

ENRICHMENTS["dog_fibrocartilaginous_embolic_myelopathy"] = {"diagnosis_ja": (
    "MRIで脊髄実質内の非対称性T2高信号を確認。造影増強なし（非圧迫性脊髄症）。"
    "急性の非疼痛性不全麻痺で、分布が血管領域に一致（片側性が多い）。"
    "CSF検査は正常～軽度蛋白上昇。X線/CT myelographyで椎間板脱出を除外。"
    "運動中の発症が特徴的。大型犬に好発。非進行性で24時間以内に安定。理学療法で回復。"
)}

ENRICHMENTS["dog_degenerative_myelopathy"] = {"diagnosis_ja": (
    "SOD1遺伝子変異検査で確定（A/A: 高リスク）。DNA検査は生前に実施可能。"
    "臨床的に後肢の進行性固有受容感覚喪失（ナックリング）→不全麻痺→麻痺で診断。"
    "MRIで脊髄の圧迫性病変を除外（DM自体はMRI正常）。CBC/生化学正常。"
    "ジャーマン・シェパード、ウェルシュ・コーギー等に好発。8歳以上。確定診断は死後病理（白質変性）のみ。"
)}

ENRICHMENTS["dog_canine_cognitive_dysfunction_syndrome"] = {"diagnosis_ja": (
    "DISHAAL評価: 見当識障害(D)、社会的交流変化(I)、睡眠覚醒サイクル変化(S)、"
    "不適切排泄(H)、活動量変化(A)、不安(A)、学習記憶低下(L)のスコアリング。"
    "MRI/CTで脳萎縮・脳室拡大を確認。脳腫瘍を除外。CBC/生化学/T4で代謝性原因を除外。"
    "11歳以上の犬の28%以上が罹患。行動変化の詳細な飼い主アンケート。セレギリン/SAMe+中鎖脂肪酸食が治療。"
)}

ENRICHMENTS["dog_syringomyelia"] = {"diagnosis_ja": (
    "MRIで脊髄中心管の嚢胞性拡張（syrinx）を確認。T2高信号。頸部～胸部に好発。"
    "キアリ様奇形（CM）の合併を後頭骨大孔レベルで評価。小脳扁桃のヘルニア。"
    "CSF流動態（cine MRI）で異常なCSF拍動を確認。X線/CTで骨格異常を評価。"
    "CKCS（キャバリア・キング・チャールズ・スパニエル）に極めて高い有病率（>70%）。幻肢掻爬が特徴的。"
)}

ENRICHMENTS["dog_tetralogy_of_fallot"] = {"diagnosis_ja": (
    "心エコーで4徴（VSD+肺動脈狭窄+大動脈騎乗+右室肥大）を確認。"
    "カラードプラで右左シャント（R-L shunt）を確認。連続波ドプラで肺動脈圧較差を測定。"
    "動脈血ガスで低酸素血症（PaO₂<60 mmHg）、チアノーゼ。血液検査で赤血球増加症（PCV>65%）。"
    "聴診で収縮期雑音。X線で右心拡大、肺血流減少。心血管造影/CTで確定。ケシュホンド、ブルドッグに好発。"
)}

ENRICHMENTS["dog_pulmonary_thromboembolism"] = {"diagnosis_ja": (
    "CT肺動脈造影（CTPA）で肺動脈内の充満欠損を確認。動脈血ガスで低酸素血症、A-aDO₂勾配上昇。"
    "D-ダイマー上昇（感度高い）。胸部X線で楔状陰影、右心拡大を評価。"
    "心エコーで右心負荷所見（RV拡大、三尖弁逆流速度上昇）。NT-proBNP上昇。"
    "基礎疾患精査: IMHA、クッシング、ネフローゼ症候群、DIC、腫瘍。AT III低下は素因。抗凝固療法。"
)}

ENRICHMENTS["dog_hemangiosarcoma_splenic"] = {"diagnosis_ja": (
    "腹部超音波で脾臓の不均一エコー腫瘤（低エコー/高エコー混在、嚢胞性成分）を確認。腹腔内遊離液体。"
    "穿刺液PCV>腹水PCV（血腹）。胸部X線/CTで肺転移、心エコーで右房腫瘤を同時評価。"
    "CBC/凝固でDIC、貧血。FNA/生検でHSA確定。TNMステージング。"
    "ゴールデン・レトリーバー、ジャーマン・シェパードに好発。緊急脾摘出。ドキソルビシン化学療法でMST 5-7ヶ月。"
)}

ENRICHMENTS["dog_hemangiosarcoma_cardiac"] = {"diagnosis_ja": (
    "心エコーで右房壁の不均一エコー腫瘤と心嚢液貯留を確認。右房虚脱でタンポナーデ。"
    "心嚢穿刺で血性液回収。PCV測定。液体細胞診（感度<30%）。"
    "CT/造影CTで腫瘤の範囲、肺転移、脾臓HSA同時発生を評価。"
    "トロポニンI上昇。DIC合併。ゴールデン・レトリーバーに好発。心膜切除+化学療法。MST 2-4ヶ月。"
)}

ENRICHMENTS["dog_primary_hyperparathyroidism"] = {"diagnosis_ja": (
    "血液検査で高Ca血症（イオン化Ca上昇）+PTH上昇（不適切なPTH分泌）を確認。"
    "頸部超音波で副甲状腺の腫大（腺腫>過形成>腺癌）を確認。正常は<3mm。"
    "尿検査でCa排泄増加、カルシウム結石のリスク。腎超音波で腎石灰化を評価。"
    "PTHrP正常（腫瘍性高Ca血症との鑑別）。25(OH)VitD正常。外科的副甲状腺摘出が根治療法。"
)}

ENRICHMENTS["dog_pemphigus_foliaceus"] = {"diagnosis_ja": (
    "皮膚生検で表皮内の棘融解と好中球優位の角層下膿疱を確認（acantholytic keratinocytes）。"
    "直接免疫蛍光法（DIF）で角化細胞間のIgG沈着を確認。"
    "臨床症状: 鼻梁・耳介・肉球の膿疱→痂皮→びらん。対称性分布。"
    "細菌培養で二次感染を評価。SLE・薬剤性を鑑別。秋田犬、チャウチャウに好発。プレドニゾロン+アザチオプリン。"
)}

ENRICHMENTS["dog_discoid_lupus_erythematosus"] = {"diagnosis_ja": (
    "皮膚生検で界面皮膚炎（基底層の液状変性、apoptotic keratinocytes）を確認。"
    "直接免疫蛍光法（DIF）で基底膜へのIgG/C3沈着（lupus band）を確認。"
    "臨床症状: 鼻鏡の色素脱失→紅斑→潰瘍→痂皮。鼻鏡のcobbble stone appearance消失。"
    "ANA陰性（SLEとの鑑別点）。紫外線暴露で悪化。ジャーマン・シェパード、コリーに好発。日光回避+局所ステロイド。"
)}

ENRICHMENTS["dog_color_dilution_alopecia"] = {"diagnosis_ja": (
    "毛の顕微鏡検査（trichogram）で毛幹内のメラニン顆粒の不均一な凝集塊を確認。"
    "皮膚生検で毛包の角化異常、毛包周囲の炎症、色素顆粒の凝集を確認。"
    "希釈色被毛（ブルー/フォーン）の部位に限局した進行性脱毛。非希釈色部位は正常。"
    "ドーベルマン（ブルー）、イタリアン・グレイハウンド、チワワに好発。MLPH遺伝子変異。治療は対症療法のみ。"
)}

ENRICHMENTS["dog_pulmonary_carcinoma"] = {"diagnosis_ja": (
    "胸部X線で孤立性/多発性の肺腫瘤を確認。CT三次元再構成で腫瘤サイズ・リンパ節・肺門を評価。"
    "超音波ガイド下FNA/経胸壁生検で腫瘍型を確定（腺癌、SCC、未分化癌）。BAL細胞診。"
    "CBC/生化学は概ね正常。転移性との鑑別に全身CT/腹部超音波。"
    "原発性肺腫瘍は犬の腫瘍全体の1-2%。咳・呼吸困難・HO（肥大性骨症）の合併。肺葉切除が根治療法。"
)}

ENRICHMENTS["dog_xylitol_toxicosis"] = {"diagnosis_ja": (
    "病歴聴取でキシリトール含有製品（ガム、菓子、歯磨き粉）の摂取を確認。摂取量推定。"
    "低血糖（<60 mg/dL）: 摂取後30-60分で発症。嘔吐、運動失調、痙攣。中毒量>0.1 g/kg。"
    "肝不全: 摂取後8-72時間。ALT/AST著増、凝固障害（PT/APTT延長）。中毒量>0.5 g/kg。"
    "血糖連続モニタリング（8-24時間）。催吐（摂取30分以内）+デキストロース持続点滴。肝保護療法。"
)}

ENRICHMENTS["dog_grape_and_raisin_toxicosis"] = {"diagnosis_ja": (
    "病歴聴取でブドウ/レーズンの摂取を確認。中毒量は個体差が大きく予測不能（酒石酸が毒性物質の候補）。"
    "血液検査でBUN/Cre上昇（AKI: 摂取後24-72時間で発症）。高Ca・高P。"
    "尿検査で無尿/乏尿、尿沈渣で腎尿細管上皮細胞、円柱。超音波で腎臓腫大・エコー輝度上昇。"
    "嘔吐が初期症状（6-12時間以内）。催吐+活性炭+積極的輸液（48-72時間）。腎透析が必要な場合あり。"
)}

ENRICHMENTS["dog_anticoagulant_rodenticide_toxicosis"] = {"diagnosis_ja": (
    "凝固検査でPT延長（最初に延長: 摂取後36-72時間）→APTT延長。PIVKA上昇。"
    "CBC/血液塗抹で急性失血による貧血。X線/超音波で体腔内出血を確認。"
    "製品の特定: 第1世代（ワルファリン）vs第2世代（ブロマジオロン/ブロジファコウム: 半減期長い）。"
    "出血兆候: 点状出血、血尿、血便、鼻出血、体腔内出血。ビタミンK1が拮抗薬（4-6週間投与）。"
)}

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
