#!/usr/bin/env python3
import json
import os
import time

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diseases_all_species.json")

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["cat_renal_lymphoma"] = {"diagnosis_ja": (
    "腹部超音波で両側腎臓の腫大・低エコー化（正常腎臓の2-3倍）を確認。腎盂の消失。"
    "超音波ガイド下FNA/Tru-cutで大型リンパ球を確認。フローサイトメトリーでB細胞型（最多）を確定。"
    "CBC/生化学でBUN/Cre上昇（腎不全）、高Ca血症、貧血を評価。FeLV/FIV検査（陽性率10-25%）。"
    "全身ステージングにCT/X線、骨髄穿刺。CNS転移のリスクありCSF検査を検討。CHOP系化学療法。"
)}

ENRICHMENTS["cat_polycystic_kidney_disease_pkd"] = {"diagnosis_ja": (
    "腹部超音波で両側腎臓の多発性嚢胞を確認。10週齢から検出可能（感度75%→12ヶ月齢で91%）。"
    "遺伝子検査でPKD1遺伝子変異を確認（ペルシャ型: AD-PKD1、感度/特異度99%）。"
    "血液検査でBUN/Cre/SDMAの経時的上昇（CKD進行）。尿検査で低比重尿・蛋白尿。"
    "ペルシャ、エキゾチックショートヘアに好発。常染色体優性遺伝。肝臓嚢胞の合併を評価。治療はCKD管理。"
)}

ENRICHMENTS["cat_urinary_tract_infection_uti"] = {"diagnosis_ja": (
    "尿検査で膿尿（WBC>5/HPF）、細菌尿、蛋白尿、血尿を確認。尿培養+感受性試験で起炎菌を同定。"
    "膀胱穿刺（cystocentesis）で採取した尿で≧1,000 CFU/mLが有意。"
    "CBC/生化学で全身性感染の有無を評価。腹部超音波で結石・腫瘍・解剖学的異常を除外。"
    "猫のUTIは犬より稀（FLUTD全体の1-3%）。高齢猫・CKD・糖尿病・甲状腺機能亢進症との関連が多い。"
)}

ENRICHMENTS["cat_diabetic_ketoacidosis_dka"] = {"diagnosis_ja": (
    "血糖値>300 mg/dL、血液ガスでpH<7.3、HCO₃⁻<15 mEq/L。尿ケトン体3+以上。"
    "血中β-ヒドロキシ酪酸上昇。電解質で低K⁺・低Na⁺・低Pを確認（補正が重要）。"
    "CBC/生化学で脱水、BUN/Cre上昇、肝酵素上昇を評価。"
    "誘因の精査: 膵炎（fPLI）、UTI（尿培養）、ステロイド投与歴。猫は2型DMが多い。緊急入院+輸液+インスリン。"
)}

ENRICHMENTS["cat_hyperaldosteronism_conn's_syndrome"] = {"diagnosis_ja": (
    "血液検査で低K⁺血症（<3.5 mEq/L）を確認。血漿アルドステロン濃度上昇。"
    "腹部超音波/CTで副腎腫大（単側性腺腫/腺癌が多い）を確認。対側副腎の萎縮。"
    "血漿レニン活性低値（ARR比上昇）。全身性高血圧（収縮期>160 mmHg）の合併。"
    "CKDとの合併が多い。筋力低下（低K⁺による）、頸部腹屈（ventroflexion）が特徴的臨床徴候。副腎摘出術。"
)}

ENRICHMENTS["cat_acromegaly_hypersomatotropism"] = {"diagnosis_ja": (
    "血清IGF-1上昇（>1,000 ng/mL で強く疑う）が最も信頼性の高いスクリーニング。"
    "頭部MRI/CTで下垂体腫大を確認。血糖値上昇+インスリン抵抗性（>6-8 U/回でも高血糖持続）。"
    "身体検査で体重増加（肥満でなく除脂肪体重増加）、下顎突出、手根関節肥大を確認。"
    "糖尿病のインスリン抵抗性が治療手がかり。英国の猫DM患者の最大25%がGH過剰。放射線療法/下垂体摘出。"
)}

ENRICHMENTS["cat_hypoadrenocorticism_addison's_disease"] = {"diagnosis_ja": (
    "ACTH刺激試験でコルチゾール反応低値（基礎値・刺激後ともに<2 μg/dL）を確認。"
    "電解質でNa⁺/K⁺比<27（典型的: 高K⁺+低Na⁺）。非定型型ではNa⁺/K⁺正常。"
    "CBC/生化学で低血糖、高Ca血症、高BUN（腎前性）、好酸球増加、リンパ球増加。"
    "猫では極めて稀。非特異的症状（食欲不振、嘔吐、嗜眠）。副腎危機時は緊急輸液+デキサメタゾン。"
)}

ENRICHMENTS["cat_hyperadrenocorticism_cushing's_disease"] = {"diagnosis_ja": (
    "UCCRスクリーニング（上昇時のみ追加検査）。LDDSTでコルチゾール抑制不良。"
    "ACTH刺激試験でコルチゾール過反応。腹部超音波で副腎腫大（両側:下垂体性、片側:副腎腫瘍）。"
    "頭部MRI/CTで下垂体腫大を確認。血液検査でALP上昇は犬ほど顕著でない。"
    "猫では稀で糖尿病の合併が多い（80%+）。皮膚菲薄化（紙のように薄い）が特徴的。皮膚が容易に裂ける。"
)}

ENRICHMENTS["cat_insulinoma"] = {"diagnosis_ja": (
    "血糖値低値（<60 mg/dL）と同時にインスリン上昇（不適切なインスリン分泌）を確認。"
    "改正インスリン/グルコース比（AIGR）上昇。72時間絶食試験で低血糖を誘発。"
    "腹部超音波で膵臓の低エコー結節を検索（感度限定的）。CT/造影CTが検出率向上。"
    "猫では犬より極めて稀。痙攣・失神・脱力の低血糖症状。外科的膵部分切除が治療。"
)}

ENRICHMENTS["cat_feline_infectious_peritonitis_fip_-_wet_form"] = {"diagnosis_ja": (
    "腹水/胸水の分析: 黄色粘稠な高蛋白滲出液（TP>3.5 g/dL）、Rivalta試験陽性。A/G比<0.4が強く示唆。"
    "体腔液の免疫染色でFCoV抗原陽性。RT-PCRでFCoV RNA検出。"
    "血液検査で高γグロブリン血症、低アルブミン血症、A/G比<0.8。高ビリルビン血症。"
    "抗FCoV抗体価は参考値。全身性肉芽腫性血管炎が病態。GS-441524/モルヌピラビル抗ウイルス療法。"
)}

ENRICHMENTS["cat_feline_infectious_peritonitis_fip_-_dry_form"] = {"diagnosis_ja": (
    "眼科検査で前部ぶどう膜炎（前房フレア、角膜後面沈着物 keratic precipitates）を確認。"
    "神経学的検査で発作・運動失調・不全麻痺（CNS病変）。MRIで脳室周囲の造影増強。"
    "血液検査で高γグロブリン血症、A/G比<0.8、高ビリルビン。抗FCoV抗体価上昇。"
    "組織生検/FNAの免疫組織化学でFCoV抗原検出が確定診断。ウェット型より診断困難。GS-441524治療。"
)}

ENRICHMENTS["cat_feline_calicivirus_infection"] = {"diagnosis_ja": (
    "口腔内検査で舌・口蓋の潰瘍を確認（FCV特徴的所見）。鼻汁・結膜炎を評価。"
    "口腔/鼻腔スワブからRT-PCRでFCVを検出。ウイルス分離培養（CRFK細胞）。"
    "CBC/生化学は概ね正常（二次感染時は白血球増多）。胸部X線で肺炎を除外。"
    "VS-FCV（virulent systemic FCV）では浮腫、DIC、多臓器不全。FHV-1との混合感染を評価。ワクチン接種歴の確認。"
)}

ENRICHMENTS["cat_feline_herpesvirus_fhv-1_infection"] = {"diagnosis_ja": (
    "結膜/角膜スワブからPCRでFHV-1 DNAを検出（急性期の感度高い）。"
    "眼科検査で樹枝状角膜潰瘍（dendritic ulcer: FHV-1に特異的）をフルオレセイン染色で確認。"
    "結膜生検/スワブの免疫蛍光法（DFA）。ウイルス分離培養。"
    "くしゃみ・漿液性→膿性鼻汁・発熱・食欲不振の臨床症状。潜伏感染→ストレスで再活性化。抗ウイルス薬+支持療法。"
)}

ENRICHMENTS["cat_toxoplasmosis"] = {"diagnosis_ja": (
    "血清学的検査で抗Toxoplasma IgM上昇（急性感染）、IgGペア血清で4倍以上上昇。"
    "PCRで血液/CSF/組織からToxoplasma gondii DNAを検出。糞便中オーシスト検出（感度低い）。"
    "CBC/生化学でCK上昇（筋炎）、ALT上昇（肝炎）、高ビリルビン血症。胸部X線で間質性肺炎。"
    "眼科検査で前部ぶどう膜炎・脈絡網膜炎を確認。クリンダマイシン25 mg/kg/日が治療。人獣共通感染症。"
)}

ENRICHMENTS["cat_feline_panleukopenia_feline_distemper"] = {"diagnosis_ja": (
    "CBC/血液塗抹で全白血球著減（WBC<2,000/μL）を確認。好中球減少が特に顕著。"
    "糞便の犬パルボウイルス迅速抗原検査（SNAP Parvo）で陽性（交差反応で検出可能）。"
    "PCRで糞便/血液からFPV DNAを検出。血清学的検査は限定的（ワクチン接種歴で干渉）。"
    "嘔吐・血性下痢・急速な脱水・敗血症。子猫の死亡率90%以上。ワクチン未接種歴が最大リスク。集中支持療法。"
)}

ENRICHMENTS["cat_feline_chlamydiosis"] = {"diagnosis_ja": (
    "結膜スワブからPCRでChlamydia felis DNAを検出（ゴールドスタンダード）。"
    "結膜スワブの細胞診でintracytoplasmic inclusion bodyを確認（Giemsa染色: 感度低い）。"
    "眼科検査で片側性→両側性の結膜炎、結膜充血・浮腫、漿液性→膿性眼脂を確認。"
    "FHV-1/FCVとの鑑別・混合感染を評価。角膜潰瘍はクラミジア単独では稀。ドキシサイクリン4週間が治療。"
)}

ENRICHMENTS["cat_feline_bordetellosis"] = {"diagnosis_ja": (
    "鼻腔/咽頭スワブから培養でBordetella bronchisepticaを分離。選択培地（MacConkey/Bordet-Gengou）。"
    "PCRでBordetella DNAを検出。BAL液の細胞診で好中球増多。"
    "胸部X線で気管支間質パターン～気管支肺炎パターンを確認。CBC/CRPで炎症を評価。"
    "多頭飼育環境での発症。子猫で重症化（致死的肺炎）。FHV-1/FCVとの混合感染が多い。ドキシサイクリンが治療。"
)}

ENRICHMENTS["cat_bartonellosis_cat_scratch_disease_agent"] = {"diagnosis_ja": (
    "血液PCRでBartonella henselae DNAを検出。血液培養（lysis-centrifugation法: 2-6週培養）。"
    "血清学的検査でIgG抗体陽性（>1:64で現在/過去の感染）。IFA法/ELISA。"
    "CBC/生化学は概ね正常（多くは不顕性感染）。重症例ではリンパ節腫大、発熱、ぶどう膜炎。"
    "ノミ媒介感染。猫は保菌宿主（症状なし）で人への感染源。人獣共通感染症。アジスロマイシンが治療。"
)}

ENRICHMENTS["cat_mycoplasma_haemofelis_infection_feline_infectious_anemia"] = {"diagnosis_ja": (
    "血液PCRでMycoplasma haemofelisを検出（ゴールドスタンダード）。種の同定も可能。"
    "血液塗抹でRBC表面の小さなring/dot形の菌体を確認（感度低い: 間欠的菌血症のため）。"
    "CBC/血液塗抹で再生性溶血性貧血（PCV低下、網赤血球増加）。クームス試験陽性の場合あり。"
    "FeLV/FIV併発の確認（免疫抑制→臨床発症）。ダニ/ノミ媒介。ドキシサイクリン28日間が第一選択。"
)}

ENRICHMENTS["cat_rabies"] = {"diagnosis_ja": (
    "確定診断は死後の脳組織検査: DFA（直接蛍光抗体法）でウイルス抗原を確認。"
    "生前診断は困難: 皮膚生検（項部の有毛皮膚）のDFA、唾液のRT-PCR。"
    "血清中和抗体価はワクチン接種歴があると解釈困難。CSF検査は非特異的。"
    "行動変化（攻撃性/沈鬱）→麻痺→死亡の典型的経過。日本は清浄国（1957年以降発生なし）。法定伝染病。"
)}

ENRICHMENTS["cat_feline_coronavirus_enteritis"] = {"diagnosis_ja": (
    "糞便RT-PCRでFCoV RNAを検出。健康保菌猫も陽性のため解釈に注意。"
    "抗FCoV抗体価はFIP変異株との鑑別不能（同一ウイルス群）。"
    "CBC/生化学は概ね正常。軽度の軟便・下痢（自然回復が多い）。糞便検査で他の寄生虫を除外。"
    "多頭飼育環境で感染率高い（90%以上）。FIPへの変異は5-12%。糞便中ウイルス排出の経時的モニタリング。"
)}

ENRICHMENTS["cat_cryptococcosis"] = {"diagnosis_ja": (
    "ラテックス凝集試験（LCAT）で血清/CSF中のCryptococcal抗原を検出（感度/特異度>95%）。力価は治療効果指標。"
    "鼻腔/皮膚FNAの細胞診でインド墨汁染色による厚い莢膜を持つ酵母を確認。"
    "培養でCryptococcus neoformans/gatiiを分離。鼻腔/皮膚/CNS/眼の病変を検索。"
    "頭部CT/MRIでCNS型の肉芽腫性病変を確認。鼻腔型が猫で最多。フルコナゾール/イトラコナゾール長期治療。"
)}

ENRICHMENTS["cat_feline_cowpox"] = {"diagnosis_ja": (
    "皮膚病変部の生検/スワブからPCRで牛痘ウイルスDNAを検出。電子顕微鏡でオルソポックスウイルス粒子。"
    "ウイルス分離培養（Vero/BHK細胞）。細胞診で好酸性のintracytoplasmic inclusion bodyを確認。"
    "皮膚生検で表皮の壊死・水疱形成・封入体を確認。CBC/生化学は概ね正常。"
    "特徴的な皮膚潰瘍性結節。齧歯類（ネズミ）からの感染。欧州/英国で発生。人獣共通感染症。"
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
