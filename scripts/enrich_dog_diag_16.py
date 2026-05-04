#!/usr/bin/env python3
import json
import os
import time

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "diseases_all_species.json")

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_ethylene_glycol_toxicosis"] = {
    "diagnosis_ja": (
        "血液ガスで重度の代謝性アシドーシス（pH<7.1、AG>25 mEq/L）。浸透圧ギャップ上昇（>15 mOsm/kg）。"
        "尿検査でシュウ酸Ca結晶（monohydrate/dihydrate）を検出。ウッド灯で尿のフルオレセイン蛍光。"
        "血中EG濃度測定（酵素法）。BUN/Cre上昇（AKI: 24-72時間で発症）。低Ca血症。"
        "致死量: 4.4-6.6 mL/kg。フォメピゾール（4-MP）が拮抗薬（摂取8時間以内に開始）。エタノール療法は代替。"
    )
}

ENRICHMENTS["dog_metaldehyde_toxicosis"] = {
    "diagnosis_ja": (
        "病歴でナメクジ・カタツムリ駆除剤（メタアルデヒド）の摂取を確認。致死量100-250 mg/kg。"
        "全身性振戦・痙攣・高体温（>41℃）・頻脈が特徴的三徴。血液ガスで代謝性アシドーシス。"
        "血中/尿中メタアルデヒド検出（GC-MS）。ALT/AST上昇（肝障害: 24-72時間後）。"
        "ペレット状の嘔吐物。CBC/生化学で脱水、乳酸上昇。緊急痙攣管理（ジアゼパム→プロポフォール CRI）。"
    )
}

ENRICHMENTS["dog_esophageal_foreign_body"] = {
    "diagnosis_ja": (
        "頸部/胸部X線で食道内の放射線不透過性異物（骨が最多）を確認。造影検査で透過性異物を検出。"
        "内視鏡で異物の直接確認・位置・食道壁損傷を評価。同時に内視鏡的摘出を試みる。"
        "CT三次元再構成で異物と周囲構造（大動脈、気管）の関係を評価。"
        "嗜好部位: 胸部入口部、心基底部、横隔膜直前。嘔吐・吐出・流涎・嚥下困難の臨床症状。"
    )
}

ENRICHMENTS["dog_gastric_ulceration"] = {
    "diagnosis_ja": (
        "内視鏡で胃粘膜の潰瘍（深達度: びらん→潰瘍→穿孔）を直接確認。生検で腫瘍性を除外。"
        "CBC/血液塗抹で貧血（慢性出血→鉄欠乏性小球性低色素性貧血）。便潜血/黒色タール便。"
        "腹部超音波で胃壁肥厚・穿孔を評価。腹腔液で遊離ガスを確認（穿孔時）。"
        "原因: NSAIDs（最多）、肥満細胞腫（ヒスタミン過剰）、肝疾患、ストレス。PPI/スクラルファートが治療。"
    )
}

ENRICHMENTS["dog_intestinal_lymphangiectasia"] = {
    "diagnosis_ja": (
        "血液検査で低アルブミン+低グロブリン+低コレステロール+リンパ球減少（PLE四徴）。"
        "内視鏡/全層生検で十二指腸/空腸絨毛のリンパ管拡張を確認。乳糜槽の白濁化。"
        "α1-PIクリアランス上昇はPLEの証拠。腹水・胸水は低蛋白性漏出液。"
        "腹部超音波で腸壁の高エコーストリエーション。ヨークシャー・テリアに好発。超低脂肪食+MCTオイル。"
    )
}

ENRICHMENTS["dog_prostatic_abscess"] = {
    "diagnosis_ja": (
        "腹部超音波で前立腺内の嚢胞性/液体貯留（低エコー腔）を確認。ドプラで周囲炎症の血流増加。"
        "超音波ガイド下穿刺で膿を吸引→細菌培養+感受性（E. coli が最多）。"
        "CBC/CRPで白血球増多（左方移動）、炎症マーカー著増。尿培養で同一起炎菌を同定。"
        "直腸触診で前立腺の腫大・非対称性・疼痛。未去勢雄犬。去勢+外科的ドレナージ+長期抗生剤。"
    )
}

ENRICHMENTS["dog_benign_prostatic_hyperplasia"] = {
    "diagnosis_ja": (
        "腹部超音波で前立腺の対称性腫大と小嚢胞を確認。エコー輝度は均一。"
        "直腸触診で前立腺の対称性腫大・非疼痛性を確認。血尿・排便困難。"
        "前立腺液/精液の細胞診で感染・腫瘍を除外。尿培養で感染性前立腺炎を除外。"
        "未去勢雄犬の加齢性変化（6歳以上の95%）。去勢が最も効果的な治療。去勢後4-8週で縮小。"
    )
}

ENRICHMENTS["dog_nictitans_gland_prolapse_cherry_eye"] = {
    "diagnosis_ja": (
        "身体検査で瞬膜背側からの赤色球状腫瘤（突出した瞬膜腺）を直接確認。片側性or両側性。"
        "眼科検査で角膜潰瘍（機械的刺激）を除外。STT（シルマー涙液試験）で涙液量を基準値として測定。"
        "FNA/生検は通常不要（臨床診断で十分）。腫瘤の色・サイズ・炎症程度を評価。"
        "短頭種（ブルドッグ、コッカー・スパニエル、ビーグル）に好発。モーガンポケット法/包埋法で腺を温存。"
    )
}

ENRICHMENTS["dog_canine_brucellosis"] = {
    "diagnosis_ja": (
        "RSAT（迅速スライド凝集試験）でスクリーニング。偽陽性多いためAGID/iELISAで確認。"
        "血液培養でBrucella canisを分離（確定：感度60-70%）。PCRでDNA検出。"
        "精液検査で精子異常・炎症細胞。雌: 後期流産（45-55日目）。雄: 精巣上体炎→精巣萎縮。"
        "脊椎X線で椎間板脊椎炎。眼科検査でぶどう膜炎。人獣共通感染症。ドキシサイクリン+アミノグリコシド。"
    )
}

ENRICHMENTS["dog_canine_leptospirosis"] = {
    "diagnosis_ja": (
        "MAT（顕微鏡的凝集反応試験）で血清抗体価上昇（≧1:800 or ペア血清で4倍以上）を確認。"
        "尿PCRでLeptospira DNAを検出。血液/尿培養（EMJH培地: 数週間）。"
        "血液検査でBUN/Cre著増（AKI）、ALT/ALP上昇（肝障害）、血小板減少。"
        "尿検査で糖尿、円柱、等張尿。黄疸。人獣共通感染症。ドキシサイクリン（排菌停止）。ワクチン接種歴の確認。"
    )
}

ENRICHMENTS["dog_canine_herpesvirus"] = {
    "diagnosis_ja": (
        "新生子犬（<3週齢）の急性死亡で疑う。PCRで組織/スワブからCHV-1 DNAを検出。"
        "剖検で肝臓・腎臓の点状出血/壊死が特徴的。組織検査でintranuclear inclusion bodyを確認。"
        "成犬では不顕性感染が多い。生殖器水疱性病変の検査。ペア血清で中和抗体価上昇。"
        "繁殖管理: 母犬の抗体価確認。新生子犬の低体温がウイルス増殖を促進。環境温維持が予防的。"
    )
}

ENRICHMENTS["dog_salmon_poisoning_disease"] = {
    "diagnosis_ja": (
        "リンパ節FNAでNeorickettsia helminthoeca（マクロファージ内の好塩基性小体）を検出。"
        "糞便検査で媒介吸虫Nanophyetus salmincola の虫卵（52-82μm）を検出。"
        "CBC/生化学で白血球減少→増多、血小板減少、低アルブミン血症。"
        "太平洋岸北西部（オレゴン～北カリフォルニア）で生魚摂取歴。致死率90%（未治療）。ドキシサイクリン/テトラサイクリン。"
    )
}

ENRICHMENTS["dog_leishmaniosis"] = {
    "diagnosis_ja": (
        "骨髄/リンパ節/皮膚のFNA/生検でマクロファージ内のアマスチゴートを確認（Giemsa染色）。"
        "血清学（IFAT/ELISA）で抗Leishmania抗体価上昇。定量PCRで寄生虫量を評価。"
        "血液検査で高γグロブリン血症、低A/G比、貧血、血小板減少。尿検査で蛋白尿（腎障害）。"
        "皮膚病変（鱗屑、脱毛、潰瘍）+全身症状（体重減少、リンパ節腫大）。地中海沿岸の流行地。"
    )
}

ENRICHMENTS["dog_primary_ciliary_dyskinesia"] = {
    "diagnosis_ja": (
        "鼻腔/気管粘膜の生検で電子顕微鏡による線毛超微細構造異常を確認（外腕ダイニン欠損が最多）。"
        "鼻腔ブラッシングの高速度ビデオ顕微鏡で線毛運動解析。nasal NO測定（低値）。"
        "胸部X線/CTで気管支拡張、慢性鼻副鼻腔炎。内臓逆位（situs inversus: 50%で合併）。"
        "精液検査で精子運動能低下。幼若齢からの慢性鼻汁・咳。オールド・イングリッシュ・シープドッグ等に好発。"
    )
}

ENRICHMENTS["dog_compulsive_disorder"] = {
    "diagnosis_ja": (
        "行動診察で反復的・固定的な行動パターン（旋回、尾追い、光/影追い、flanksucking）を評価。"
        "ビデオ記録で行動の詳細パターン・頻度・持続時間を分析。てんかんとの鑑別。"
        "MRI/CTで脳構造的病変を除外。EEGでてんかん性放電を除外。CBC/T4/生化学で内科的原因を除外。"
        "ドーベルマン（flank sucking）、ブル・テリア（spinning）に犬種特異的。SSRI（フルオキセチン）+行動修正。"
    )
}

ENRICHMENTS["dog_portosystemic_shunt_pss"] = {
    "diagnosis_ja": (
        "食前/食後胆汁酸上昇（食前>25、食後>50 μmol/L）が高感度スクリーニング。血清NH3上昇。"
        "腹部超音波で異常血管を同定。造影CT（CTA）で門脈系の三次元評価が最も信頼性高い。"
        "生化学でBUN低値、Alb低値、Glu低値、Chol低値。尿酸アンモニウム結晶。"
        "先天性（肝外性: 小型犬、肝内性: 大型犬）。肝性脳症（食後の異常行動・痙攣）。外科的結紮/ameroid。"
    )
}

ENRICHMENTS["dog_uroabdomen"] = {
    "diagnosis_ja": (
        "腹腔穿刺で腹水を回収。腹水/血漿クレアチニン比>2.0で尿腹を確定。腹水K⁺>血漿K⁺。"
        "腹腔液BUN/血漿BUN比>1.0。X線造影で膀胱破裂/尿管断裂/腎損傷の部位を特定。"
        "CBC/生化学でBUN/Cre上昇（腹膜からの再吸収）、高K⁺（致死的不整脈リスク）。"
        "原因: 外傷（交通事故）、尿道閉塞後の膀胱破裂、医原性。緊急K⁺管理+外科的修復。"
    )
}

ENRICHMENTS["dog_bile_peritonitis"] = {
    "diagnosis_ja": (
        "腹腔穿刺で緑色～黄色の腹水を回収。腹腔液ビリルビン/血漿ビリルビン比>2.0で確定。"
        "腹腔液の細菌培養（胆汁性腹膜炎は無菌性と感染性あり）。細胞診で胆汁色素貪食マクロファージ。"
        "CBC/CRP/SAAで重度炎症反応。生化学でTBil著増、ALP/ALT/GGT上昇。"
        "原因: 胆嚢破裂/穿孔、胆嚢粘液嚢腫破裂、外傷、手術後。緊急外科的探索+胆嚢切除+腹腔洗浄。"
    )
}

ENRICHMENTS["dog_salivary_mucocele"] = {
    "diagnosis_ja": (
        "身体検査で顎下/舌下の波動性腫脹を確認。FNAで粘稠な透明～淡黄色液体（ムチン）を回収。"
        "細胞診で少数のマクロファージ・好中球。血性ではない（膿瘍/腫瘍と鑑別）。"
        "超音波で嚢胞構造を確認。CT/シアログラフィーで原因唾液腺を同定。"
        "舌下型（ranula）、頸部型、咽頭型に分類。下顎腺+舌下腺摘出が根治療法。"
    )
}

ENRICHMENTS["dog_immune-mediated_polyarthritis"] = {
    "diagnosis_ja": (
        "関節液検査で非感染性炎症（WBC>3,000/μL、好中球>10%、培養陰性）を確認。多関節罹患。"
        "血清学（ANA、RF、抗CCP抗体）で分類。びらん性（ANA+）vs非びらん性。"
        "X線で関節周囲の軟部組織腫脹。びらん性ではjoint space narrowing/骨びらんを確認。"
        "CBC/CRP/SAAで全身性炎症。ダニ媒介疾患をPCR/血清学で除外。プレドニゾロン+シクロスポリン/レフルノミド。"
    )
}

ENRICHMENTS["dog_extraocular_myositis"] = {
    "diagnosis_ja": (
        "眼科検査で両側性の眼球突出を確認。外眼筋の腫脹（急性期）→萎縮（慢性期）。"
        "CT/MRIで外眼筋の肥厚・造影増強を確認。眼窩内の脂肪組織との鑑別。"
        "抗2M線維抗体検査（咀嚼筋炎と同じ自己抗体だが異なる標的筋）。CK上昇（軽度）。"
        "ゴールデン・レトリーバーの若齢犬に好発。両側性の眼球突出と制限性斜視。ステロイド反応性。"
    )
}

ENRICHMENTS["dog_immune-mediated_thrombocytopenia_itp"] = {
    "diagnosis_ja": (
        "CBC/血液塗抹で重度血小板減少（<20,000/μL）を確認。大型血小板（若齢血小板）の出現。"
        "骨髄穿刺で巨核球数正常～増加（末梢での破壊を反映）。"
        "抗血小板抗体検査（感度限定的）。クームス試験でIMHA併発（Evans症候群）を評価。"
        "ダニ媒介疾患（エールリヒア、アナプラズマ）をPCR/血清学で除外。点状出血、鼻出血、血尿。プレドニゾロン2 mg/kg/日。"
    )
}

ENRICHMENTS["dog_immune-mediated_hemolytic_anemia_imha"] = {
    "diagnosis_ja": (
        "CBC/血液塗抹で再生性溶血性貧血（PCV<20%、網赤血球増加、球状赤血球、自己凝集）を確認。"
        "クームス試験（直接抗グロブリン試験）陽性。血漿の溶血（ヘモグロビン血症）。高ビリルビン血症。"
        "尿検査でヘモグロビン尿/ビリルビン尿。凝固検査でDIC合併を評価（血小板低下、FDP上昇）。"
        "基礎原因精査: ダニ媒介疾患（PCR）、腫瘍（画像）、薬剤性。コッカー・スパニエルに好発。血栓予防が重要。"
    )
}

ENRICHMENTS["dog_canine_chronic_hepatitis"] = {
    "diagnosis_ja": (
        "血液検査でALT持続上昇>3ヶ月。ALP/GGT上昇。低Alb、低BUN、低コレステロール（合成能低下）。"
        "超音波ガイド下肝生検（Tru-cut）で門脈周囲炎症/線維化/肝硬変を確認（確定診断に必須）。"
        "肝臓銅定量で銅蓄積性肝症を鑑別（>400 ppm dry weight）。"
        "食前後胆汁酸上昇。腹部超音波で肝臓の辺縁不整、腹水。コッカー、ラブラドール、ドーベルマンに好発。"
    )
}

ENRICHMENTS["dog_copper_storage_hepatopathy"] = {
    "diagnosis_ja": (
        "肝生検で肝臓銅定量>400 μg/g dry weight（正常<400）を確認。Rhodanine/rubeanic acid染色で銅沈着を視覚化。"
        "血液検査でALT/ALP上昇。進行例で低Alb、凝固障害、高ビリルビン。"
        "腹部超音波で肝臓のエコー輝度変化。慢性肝炎/肝硬変パターン。"
        "ベドリントン・テリア（COMMD1変異）、ラブラドール（ATP7A/B変異）、ドーベルマンに好発。銅キレート剤（ペニシラミン/トリエンチン）+低銅食。"
    )
}

ENRICHMENTS["dog_perianal_fistula"] = {
    "diagnosis_ja": (
        "身体検査で肛門周囲の深い潰瘍性瘻孔を確認。疼痛が激しく、鎮静/麻酔下で詳細検査。"
        "瘻孔の数・深さ・範囲をマッピング。プローブで瘻管の走行を確認。"
        "直腸検査で肛門嚢との交通、直腸粘膜への進展を評価。生検でSCCを除外。"
        "ジャーマン・シェパード（80%以上）に好発。免疫介在性病態。シクロスポリン5-10 mg/kg/日が第一選択治療。"
    )
}

ENRICHMENTS["dog_idiopathic_epilepsy"] = {
    "diagnosis_ja": (
        "MRI/CTで構造的脳病変を除外（特発性てんかんの診断に必須）。"
        "CBC/生化学/NH3/血中鉛で代謝性・中毒性原因を除外。胆汁酸でPSSを除外。"
        "CSF検査で炎症性脳疾患を除外。EEGで発作間欠期のてんかん性放電を確認。"
        "発症年齢6ヶ月～6歳。発作のビデオ記録と詳細なログが重要。フェノバルビタール/ゾニサミド/レベチラセタムが第一選択。"
    )
}

ENRICHMENTS["dog_ventricular_premature_complexes"] = {
    "diagnosis_ja": (
        "心電図でワイドQRS群（>0.06秒）の期外収縮を確認。形態・頻度・R on T現象を評価。"
        "ホルター心電図で24時間のVPC頻度を定量化（>1,000/日は有意、連発/多形性は高リスク）。"
        "心エコーで基礎心疾患（DCM、SAS、心筋炎、腫瘍）を評価。トロポニンI測定。"
        "電解質（K⁺、Mg²⁺）、甲状腺機能を確認。ボクサー（ARVC）、ドーベルマン（DCM）に好発。ソタロール/メキシレチンが治療。"
    )
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
