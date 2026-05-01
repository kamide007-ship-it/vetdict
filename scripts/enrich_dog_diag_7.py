#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

ENRICHMENTS["dog_atrial_fibrillation"] = {
    "diagnosis_ja": (
        "心電図で不整なRR間隔、f波（P波消失）、正常QRS幅を確認。"
        "ホルター心電図（24時間）で持続性vs発作性を判定。心エコーで左房拡大（LA/Ao>1.6）、"
        "基礎疾患（DCM、MMVD、先天性心疾患）を評価。心室レート測定（>160bpmで高レートAF）。"
        "甲状腺機能検査（T4/TSH）で甲状腺機能亢進を除外。大型犬（アイリッシュウルフハウンド、"
        "グレートデーン）にlone AFとして発生。胸部X線で肺うっ血・心拡大を評価。"
    )
}

ENRICHMENTS["dog_infective_endocarditis"] = {
    "diagnosis_ja": (
        "発熱+新規心雑音（主に大動脈弁・僧帽弁）で疑診。血液培養3セット（好気+嫌気、異なる時間）が必須。"
        "心エコーで弁上の疣贅（vegetation）を検出。CBC: 好中球増加+左方移動、単球増加。"
        "生化学: CRP著増、低Alb。尿検査で蛋白尿/血尿（免疫複合体性糸球体腎炎）。"
        "塞栓性合併症の評価: 腎梗塞（腹部エコー）、DIC（凝固パネル）、関節炎。"
        "素因: 先行感染（椎間板脊椎炎、歯科疾患、前立腺炎）、免疫抑制。大型犬に好発。"
    )
}

ENRICHMENTS["dog_pulmonary_fibrosis"] = {
    "diagnosis_ja": (
        "進行性の運動不耐性、呼吸困難、乾性咳嗽。聴診で吸気末期のベルクロ様ラ音（fine crackles）。"
        "胸部X線: びまん性間質パターン。胸部CTで蜂巣肺（honeycombing）、スリガラス影。"
        "気管支肺胞洗浄液（BALF）で好中球/マクロファージ増加。肺生検（経気管支or外科的）が確定。"
        "動脈血液ガスで低酸素血症（PaO2低下）。6分間歩行試験でSpO2低下を確認。"
        "ウエストハイランドホワイトテリアに好発（犬特発性肺線維症、CIPF）。"
    )
}

ENRICHMENTS["dog_nasal_tumor"] = {
    "diagnosis_ja": (
        "慢性片側性（→両側性）鼻汁（血性）、顔面変形、くしゃみ、エピスタキシス。"
        "頭部CT/MRIで鼻腔内腫瘤の範囲・篩板浸潤・脳浸潤を評価（CT必須でステージングに使用）。"
        "鼻腔鏡+生検で組織学的確定（腺癌が最多60%、SCC、軟骨肉腫、リンパ腫）。"
        "胸部X線/CTで肺転移評価（転移率は診断時10-15%）。所属リンパ節FNA。"
        "鑑別: 鼻腔アスペルギルス症、異物、歯根膿瘍。長頭種に好発。"
    )
}

ENRICHMENTS["dog_lung_lobe_torsion"] = {
    "diagnosis_ja": (
        "急性呼吸困難、咳嗽、発熱、虚脱。胸部X線で含気低下した肺葉の不透過性増大、"
        "気管支透過像（空気気管支造影）、胸水貯留。患側肺葉の葉間裂拡大。"
        "胸部CTで捻転した肺門血管・気管支の確認。胸水穿刺: 変性好中球、漿液血性。"
        "気管支鏡で気管支の閉塞/捻転を直視確認。右中葉が最多。"
        "好発犬種: アフガンハウンド（自発性）、大型深胸種。胸水/乳び胸の二次性にも発生。"
    )
}

ENRICHMENTS["dog_cerebellar_hypoplasia"] = {
    "diagnosis_ja": (
        "生後歩行開始時からの非進行性小脳失調: 測定過大（hypermetria）、企図振戦、"
        "広基歩様（wide-based stance）、前方への転倒。MRIで小脳の小型化を確認。"
        "子宮内感染（イヌパルボ、イヌヘルペス）が原因となる。先天性奇形との鑑別。"
        "神経学的検査: 姿勢反応正常（脊髄機能保持）、威嚇まばたき反応低下、前庭眼反射正常。"
        "進行がないことを経過観察で確認（進行性なら変性疾患を疑う）。"
    )
}

ENRICHMENTS["dog_tick_paralysis"] = {
    "diagnosis_ja": (
        "ダニ寄生5-7日後の急性上行性弛緩性麻痺。後肢→前肢→呼吸筋と進行。"
        "全身の入念な体表検査でダニを発見・除去（耳内、趾間、会陰部を重点的に）。"
        "ダニ除去後24-72時間で症状改善が診断的。筋電図で正常（脱髄/軸索障害なし）。"
        "鑑別: ボツリヌス中毒、多発性筋炎、急性多発性神経根炎（Coonhound paralysis）。"
        "呼吸機能モニタリング（呼吸筋麻痺は致死的）。オーストラリアでは特に重篤な転帰。"
    )
}

ENRICHMENTS["dog_fibrocartilaginous_embolism_fce"] = {
    "diagnosis_ja": (
        "運動中の突然の疼痛+急性非対称性脊髄障害（片麻痺が典型）。発症6-12時間で疼痛消失。"
        "MRIで脊髄実質内のT2高信号（虚血巣）を確認—確定診断はMRIが唯一。"
        "脊髄造影X線/CTでは脊髄圧迫なし（椎間板ヘルニアとの鑑別）。"
        "CSF分析は正常～軽度蛋白上昇。病理学的にはFCEが脊髄血管を閉塞。"
        "大型犬の若～中年に好発（ミニチュアシュナウザーにも）。予後は初期神経学的重症度で判定。"
    )
}

ENRICHMENTS["dog_canine_distemper_encephalitis"] = {
    "diagnosis_ja": (
        "若齢未ワクチン犬の多系統症状（鼻汁、咳嗽、下痢）後に進行性神経症状: "
        "ミオクローヌス（律動性筋攣縮、特に咀嚼筋）が病的に特徴的。発作、旋回、失明、不全麻痺。"
        "CSF分析: 単核球増多、蛋白上昇。血清/CSF中抗CDV IgM。結膜/膀胱上皮のFNA→IFA。"
        "RT-PCR（血液、尿、CSF、結膜スワブ）で確定。MRIで白質のT2高信号（脱髄）。"
        "ハードパッド（foot pad角質増殖）、エナメル質低形成は慢性感染の徴候。"
    )
}

ENRICHMENTS["dog_scotty_cramp"] = {
    "diagnosis_ja": (
        "スコティッシュテリアの運動・興奮時に発現する一過性の筋緊張亢進: "
        "弓なり姿勢、歩行困難、後肢の過伸展、転倒。安静時は完全に正常。"
        "臨床診断（運動負荷テスト+品種で診断）。神経学的検査は発作間欠期に正常。"
        "セロトニン代謝異常が原因（セロトニン作動薬で症状増悪、拮抗薬で改善）。"
        "筋電図/生検は正常。遺伝子検査が利用可能。常染色体劣性遺伝。"
        "鑑別: てんかん発作、低血糖、筋ジストロフィー。"
    )
}

ENRICHMENTS["dog_cauda_equina_syndrome_lumbosacral_stenosis"] = {
    "diagnosis_ja": (
        "腰仙部痛（尾の挙上困難、階段昇り拒否）、後肢跛行、尾の弛緩、排尿/排便障害。"
        "腰仙部の過伸展時に疼痛誘発。MRIが確定診断: L7-S1の椎間板突出/椎間孔狭窄/"
        "靭帯肥厚による馬尾神経圧迫を描出。CT+造影脊髄造影も有用。"
        "腰仙部X線で変形性変化（椎間腔狭小化、終板硬化）。筋電図で神経根障害パターン。"
        "大型犬（ジャーマンシェパード、ラブラドール）に好発。作業犬・警察犬に多い。"
    )
}

ENRICHMENTS["dog_brain_tumor"] = {
    "diagnosis_ja": (
        "中高齢犬の進行性神経症状: 発作（初発発作が最多の主訴）、行動変化、旋回、"
        "視力低下、意識レベル変化。症状は腫瘍の部位に依存。"
        "頭部MRI（造影）が確定に最も重要: 髄膜腫は均一造影+硬膜テールサイン、"
        "グリオーマは不均一造影+脳実質内。CT造影も使用可。"
        "CSF分析（蛋白上昇、細胞増多は非特異的）。定位的生検で組織学的確定。"
        "好発腫瘍: 髄膜腫（長頭種）、グリオーマ（短頭種: ボクサー、ブルドッグ）。"
    )
}

ENRICHMENTS["dog_spondylosis_deformans"] = {
    "diagnosis_ja": (
        "多くは偶発的画像所見で無症状。症候性の場合は背部硬直、疼痛、運動性低下。"
        "脊椎X線で椎体腹側/側方の骨棘形成（骨橋: bridging spondylosis）を確認。"
        "CT/MRIで神経根圧迫の評価（骨棘が椎間孔に突出する場合）。"
        "加齢性変化（中～高齢犬で高頻度）。椎間板変性との合併が多い。"
        "鑑別: 椎間板脊椎炎（感染性: 椎間腔狭小化+終板溶解）、IVDD、脊髄腫瘍。"
    )
}

ENRICHMENTS["dog_masticatory_muscle_myositis"] = {
    "diagnosis_ja": (
        "急性期: 咀嚼筋（側頭筋、咬筋）の腫脹・疼痛、開口困難（trismus）。"
        "慢性期: 咀嚼筋萎縮、開口制限（線維化）。眼球陥凹（側頭筋萎縮による）。"
        "血清中抗2M線維抗体（2M fiber antibody ELISA）が確定診断—感度90%、特異度100%。"
        "CK上昇（急性期）。筋生検で2M線維の壊死・リンパ球浸潤。"
        "鑑別: 多発性筋炎（四肢筋も侵す）、三叉神経炎、破傷風、外傷性。"
        "大型犬に好発だが全犬種で発生。"
    )
}

ENRICHMENTS["dog_craniomandibular_osteopathy"] = {
    "diagnosis_ja": (
        "3-8ヶ月齢の成長期に発熱、下顎腫脹、開口時の疼痛、摂食困難。"
        "頭部X線で下顎骨（特に角部）・側頭骨鼓室部の不規則な骨増殖を確認。"
        "CTで骨増殖の範囲と顎関節への波及を詳細評価。"
        "CBC: 軽度白血球増加、CRP上昇。骨生検は通常不要（画像で典型的）。"
        "ウエストハイランドホワイトテリア、スコティッシュテリア、ケアーンテリアに好発。"
        "常染色体劣性遺伝。骨成長停止（12-14ヶ月）で自然寛解する場合が多い。"
    )
}

ENRICHMENTS["dog_immune-mediated_polyarthritis_impa"] = {
    "diagnosis_ja": (
        "多発性関節の疼痛・腫脹・跛行（移動性）、発熱、元気消失。小型関節（手根、足根）に好発。"
        "関節液分析が確定: 混濁、粘稠度低下、好中球優位の細胞増多（>5,000/μL、非変性型）。"
        "細菌培養陰性（感染性関節炎との鑑別）。X線で骨びらんなし（びらん性ならリウマチ様）。"
        "ANA、RF検査。全身検索: 感染症、腫瘍、薬剤性、炎症性腸疾患の二次性IMPAを除外。"
        "特発性が最多（Type I）。SLE関連の場合は多臓器病変を伴う。"
    )
}

ENRICHMENTS["dog_luxating_shoulder"] = {
    "diagnosis_ja": (
        "前肢跛行、肩関節の不安定性、外側または内側への脱臼（触診で確認）。"
        "肩関節の整形外科的検査: drawer sign（前方引出し）、外転/内転テスト。"
        "X線（前後像+側面像）で脱臼の方向と骨折合併を評価。"
        "関節鏡で関節包・靭帯損傷・関節唇損傷の直視評価。CT/MRIで軟部組織評価。"
        "先天性（小型犬、発育期）vs 外傷性（全犬種）の鑑別。習慣性脱臼の頻度評価。"
    )
}

ENRICHMENTS["dog_hypertrophic_osteopathy"] = {
    "diagnosis_ja": (
        "四肢遠位の対称性腫脹・疼痛（特にメタカルパル/メタタルサル部）。発熱、跛行。"
        "四肢X線で長骨骨膜のpalisading（柵状）骨膜反応を確認。"
        "胸部X線/CTで原発性肺腫瘤（肺腫瘍が最多原因: 腺癌、SCC等）を検索。"
        "腹部エコーで腹腔内腫瘤を除外。肺病変のFNA/生検で組織学的確定。"
        "原発腫瘍切除後に骨膜反応が退縮すれば診断的。迷走神経切断でも改善しうる（神経性機序）。"
    )
}

ENRICHMENTS["dog_discoid_lupus_erythematosus_dle"] = {
    "diagnosis_ja": (
        "鼻鏡の脱色素、紅斑、痂皮、潰瘍、cobblestone外観の消失（鼻鏡の正常な凹凸が平坦化）。"
        "紫外線で増悪。皮膚生検: 表皮基底層の液状変性（interface dermatitis）、"
        "リンパ球・形質細胞浸潤。免疫蛍光法/免疫組織化学で基底膜帯のIg/C3沈着。"
        "ANA通常陰性（SLEとの鑑別点）。CBC/尿検査正常（SLEでは多臓器病変）。"
        "好発犬種: コリー、シェルティ、ジャーマンシェパード、シベリアンハスキー。"
    )
}

ENRICHMENTS["dog_follicular_dysplasia"] = {
    "diagnosis_ja": (
        "特定の被毛色部位の対称性非掻痒性脱毛。カラーダイリューション脱毛症（CDA）: "
        "淡色被毛部のみの脱毛（ブルー、フォーン）。季節性側腹脱毛（cyclical flank alopecia）。"
        "皮膚生検: 毛包の形態異常（歪んだ毛包、メラニン凝集体）が確定診断。"
        "トリコグラム（毛検査）でメラニン凝集（macromelanosomes）を確認。"
        "甲状腺機能検査（T4/TSH/fT4）でhypothyroidismを除外。好発犬種依存。"
    )
}

ENRICHMENTS["dog_dermoid_sinus"] = {
    "diagnosis_ja": (
        "背正中線上の管腔性構造（皮膚から深部組織/硬膜に向かう）。"
        "触診で背正中線の小結節/瘻管を確認。排膿や毛の突出を伴うことがある。"
        "MRI/CTで管の深さ・脊柱管への交通を評価（硬膜交通型は最も重篤）。"
        "造影瘻管造影で管の走行を描出。超音波で管の深さを簡易評価。"
        "ローデシアンリッジバック、タイリッジバックに好発（リッジの神経管閉鎖異常）。"
        "Type I-V分類（I: 皮下のみ、V: 硬膜交通）。"
    )
}

ENRICHMENTS["dog_zinc-responsive_dermatosis"] = {
    "diagnosis_ja": (
        "Syndrome I（北方犬種: ハスキー、マラミュート）: 眼囲/口囲/耳介/肉球の痂皮性皮膚炎。"
        "Syndrome II（急速成長大型犬）: フィチン酸（穀物ベース食）によるZn吸収阻害。"
        "皮膚生検: 著明な表面性不全角化（parakeratosis）が診断的。"
        "血清亜鉛濃度測定（<70μg/dLで低値）。食餌歴の詳細聴取。"
        "Zn補充試験への反応（2-6週で改善）が診断的治療。"
        "鑑別: 表在性膿皮症、天疱瘡、皮膚糸状菌症。"
    )
}

ENRICHMENTS["dog_malassezia_dermatitis"] = {
    "diagnosis_ja": (
        "脂漏性皮膚炎（油性フケ、悪臭）、掻痒、皮膚の肥厚・色素沈着。"
        "好発部位: 耳、腹側頸部、腋窩、鼠径、趾間、口唇皺壁。"
        "皮膚細胞診（セロファンテープ法/圧抵塗抹）でMalassezia pachydermatis酵母を確認。"
        "高倍率（×1000油浸）で>2個/HPFで診断的。"
        "基礎疾患の検索: アトピー性皮膚炎、食物アレルギー、内分泌疾患（甲状腺低下、Cushing）。"
        "好発犬種: バセットハウンド、コッカースパニエル、ウエストハイランドホワイトテリア。"
    )
}

ENRICHMENTS["dog_systemic_lupus_erythematosus_sle"] = {
    "diagnosis_ja": (
        "多臓器病変（2系統以上）: 多発性関節炎+糸球体腎炎+皮膚病変+血液学的異常が典型。"
        "ANA検査陽性（力価≥1:160、均質型パターン）が感度高い。抗dsDNA抗体で特異度向上。"
        "CBC: 非再生性貧血（IMHA）、血小板減少（ITP）、白血球減少。Coombs試験陽性。"
        "尿検査: 蛋白尿（UPC>0.5）、糸球体腎炎。関節液: 非変性性好中球増多。"
        "皮膚生検: interface dermatitis + 基底膜帯のIg沈着（lupus band test）。"
        "LE細胞テスト（古典的だが感度低い）。"
    )
}

ENRICHMENTS["dog_interdigital_cyst_furuncle"] = {
    "diagnosis_ja": (
        "趾間の結節性病変（紅斑性、腫脹、排膿性）。前肢に好発。単発性vs多発性/再発性。"
        "細胞診（FNA）で化膿性肉芽腫性炎症を確認。細菌培養・感受性試験（深在性感染）。"
        "皮膚生検: 毛包破裂＋異物反応（角化物・毛幹断片に対する肉芽腫）が典型的所見。"
        "基礎疾患の検索: アトピー性皮膚炎、Demodex、外傷性、Malassezia、"
        "体型（短趾種: ブルドッグ、ラブラドール）。X線で骨/関節病変を除外。"
    )
}

ENRICHMENTS["dog_seborrhea"] = {
    "diagnosis_ja": (
        "鱗屑（乾性: seborrhea sicca / 油性: seborrhea oleosa）、脂漏臭、被毛質低下。"
        "全身性分布: 背部、腋窩、鼠径、耳。皮膚細胞診でMalassezia/球菌の二次感染評価。"
        "皮膚生検: 表面性不全角化、表皮肥厚（原発性脂漏症の確認）。"
        "基礎疾患の徹底検索: 甲状腺機能低下（T4/TSH）、Cushing（LDDS/ACTH刺激）、"
        "アトピー性皮膚炎（アレルギー検査）、食物アレルギー（除去食試験）。"
        "原発性: アメリカンコッカースパニエル、イングリッシュスプリンガースパニエル。"
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
