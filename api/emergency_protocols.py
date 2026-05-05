"""emergency_protocols.py - 緊急プロトコル/クイックリファレンス

Vetlexicon-style の緊急対応プロトコル集。
獣医師が瞬時に参照できる構造化された緊急対応ガイド。

参考:
- RECOVER CPR Guidelines 2012/2024
- ACVECC Emergency Drug Reference
- BSAVA Emergency & Critical Care 3rd ed.
- Lumb & Jones Veterinary Anesthesia 5th ed.
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# 緊急プロトコルカテゴリ
# ---------------------------------------------------------------------------
PROTOCOL_CATEGORIES = {
    "cpr": {"ja": "心肺蘇生法 (CPR)", "en": "Cardiopulmonary Resuscitation"},
    "shock": {"ja": "ショック対応", "en": "Shock Management"},
    "anaphylaxis": {"ja": "アナフィラキシー", "en": "Anaphylaxis"},
    "respiratory": {"ja": "呼吸不全/気道閉塞", "en": "Respiratory Failure / Airway Obstruction"},
    "neurologic": {"ja": "神経救急", "en": "Neurologic Emergency"},
    "toxicity": {"ja": "中毒対応", "en": "Toxicity / Poisoning"},
    "trauma": {"ja": "外傷対応", "en": "Trauma"},
    "metabolic": {"ja": "代謝救急", "en": "Metabolic Emergency"},
    "fluids": {"ja": "輸液療法", "en": "Fluid Therapy"},
}


# ---------------------------------------------------------------------------
# 緊急プロトコル本体
# ---------------------------------------------------------------------------
EMERGENCY_PROTOCOLS: list[dict[str, Any]] = [
    # ============================================================
    # CPR
    # ============================================================
    {
        "id": "cpr_basic",
        "category": "cpr",
        "title_ja": "心肺停止 - 基本BLS/ALSプロトコル (RECOVER 2012)",
        "title_en": "Cardiopulmonary Arrest — Basic BLS/ALS (RECOVER 2012)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": ["意識消失", "呼吸停止", "脈拍触知不能", "瞳孔散大"],
        "trigger_signs_en": ["Unresponsiveness", "Apnea", "No palpable pulse", "Dilated pupils"],
        "steps": [
            {
                "order": 1,
                "phase": "Recognize",
                "ja": "10秒以内に評価: 意識・呼吸・脈拍。確認できなければ即CPR開始。",
                "en": "Assess in <10 sec: responsiveness, breathing, pulse. If absent, start CPR immediately.",
                "time_target": "0-10秒",
            },
            {
                "order": 2,
                "phase": "Compressions",
                "ja": "胸部圧迫: 100-120/分、深さ胸郭の1/3-1/2、最小中断。",
                "en": "Chest compressions: 100-120/min, depth 1/3-1/2 chest width, minimize interruption.",
                "time_target": "継続的",
            },
            {
                "order": 3,
                "phase": "Airway/Breathing",
                "ja": "挿管 + IPPV 10/分（圧迫:呼吸 = 30:2 不要 — 同時実施）。",
                "en": "Intubate + IPPV at 10/min (no 30:2 ratio — simultaneous with compressions).",
                "time_target": "並行",
            },
            {
                "order": 4,
                "phase": "Drugs (asystole/PEA)",
                "ja": "エピネフリン 0.01 mg/kg IV（1:1000 の 0.01 mL/kg）q3-5分。アトロピン 0.04 mg/kg IV q3-5分（迷走神経関連時）。",
                "en": "Epinephrine 0.01 mg/kg IV q3-5min. Atropine 0.04 mg/kg IV q3-5min (vagal mechanisms).",
                "time_target": "2分毎の評価サイクル後",
            },
            {
                "order": 5,
                "phase": "Drugs (VF/pulseless VT)",
                "ja": "除細動 2-4 J/kg 単相 または 1-2 J/kg 二相。アミオダロン 5 mg/kg IV ボーラス。",
                "en": "Defibrillate 2-4 J/kg monophasic or 1-2 J/kg biphasic. Amiodarone 5 mg/kg IV bolus.",
                "time_target": "VF/VT確認後即時",
            },
            {
                "order": 6,
                "phase": "Cycle assessment",
                "ja": "2分毎にECG・ETCO2確認。ROSC後はpost-cardiac arrest care。",
                "en": "Reassess ECG and ETCO2 every 2 min. After ROSC, initiate post-cardiac arrest care.",
                "time_target": "2分毎",
            },
        ],
        "key_drugs": [
            {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.01 mg/kg IV q3-5min"},
            {"name": "Atropine", "name_ja": "アトロピン", "dose": "0.04 mg/kg IV q3-5min"},
            {"name": "Amiodarone", "name_ja": "アミオダロン", "dose": "5 mg/kg IV bolus (VF/VT)"},
            {"name": "Lidocaine", "name_ja": "リドカイン", "dose": "2 mg/kg IV (alternative to amiodarone)"},
        ],
        "monitoring": ["ECG", "ETCO2", "Pulse", "Pupillary reflex"],
        "ref": "Fletcher et al. 2012 J Vet Emerg Crit Care (RECOVER); Hopper et al. 2024 update",
    },
    # ============================================================
    # Shock
    # ============================================================
    {
        "id": "shock_hypovolemic",
        "category": "shock",
        "title_ja": "低容量性ショック - 初期蘇生輸液",
        "title_en": "Hypovolemic Shock — Initial Resuscitation",
        "species": ["dog", "cat", "horse"],
        "trigger_signs_ja": ["頻脈", "弱脈", "CRT延長>2秒", "粘膜蒼白", "末梢冷感", "意識低下"],
        "trigger_signs_en": [
            "Tachycardia",
            "Weak pulses",
            "CRT >2s",
            "Pale mucous membranes",
            "Cold extremities",
            "Altered mentation",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "IV access",
                "ja": "大口径IVカテーテル（最低20G）2本確保。困難ならIO（成人犬: 上腕骨 / 大腿骨）。",
                "en": "Establish 2 large-bore IV catheters (≥20G). If difficult, intraosseous (humerus/femur in adult dog).",
                "time_target": "最初の数分",
            },
            {
                "order": 2,
                "phase": "Crystalloid bolus",
                "ja": "犬: LRS 10-20 mL/kg IV 15分。 猫: 5-10 mL/kg IV 15分。 馬: 10-20 mL/kg IV 15分。",
                "en": "Dog: LRS 10-20 mL/kg IV over 15 min. Cat: 5-10 mL/kg IV over 15 min. Horse: 10-20 mL/kg IV over 15 min.",
                "time_target": "15分",
            },
            {
                "order": 3,
                "phase": "Reassess",
                "ja": "ボーラス後の血圧・心拍数・乳酸値・尿量を再評価。Shock index改善を目標。",
                "en": "Reassess BP, HR, lactate, urine output. Target shock index improvement.",
                "time_target": "ボーラス完了後",
            },
            {
                "order": 4,
                "phase": "Repeat or escalate",
                "ja": "犬: 3回まで反復（最大60 mL/kg）→ 反応不良ならコロイド5 mL/kg or 高張食塩水4 mL/kg。",
                "en": "Dog: up to 3 boluses (max 60 mL/kg) → if poor response, colloid 5 mL/kg or hypertonic saline 4 mL/kg.",
                "time_target": "個別評価",
            },
            {
                "order": 5,
                "phase": "Vasopressors (refractory)",
                "ja": "輸液不応性低血圧: ノルエピネフリン CRI 0.05-1 μg/kg/min または ドパミン CRI 5-10 μg/kg/min。",
                "en": "Fluid-refractory hypotension: Norepinephrine CRI 0.05-1 μg/kg/min or Dopamine CRI 5-10 μg/kg/min.",
                "time_target": "MAP <65 mmHg持続時",
            },
            {
                "order": 6,
                "phase": "Identify cause",
                "ja": "出血源特定（FAST scan）→ 必要なら緊急止血手術 + 輸血（PCV<20% or 急性失血）。",
                "en": "Identify hemorrhage source (FAST scan) → emergency hemostasis surgery + transfusion if PCV <20% or acute loss.",
                "time_target": "並行実施",
            },
        ],
        "key_drugs": [
            {
                "name": "Lactated Ringer's",
                "name_ja": "乳酸リンゲル",
                "dose": "10-20 mL/kg dog / 5-10 mL/kg cat IV bolus",
            },
            {"name": "Hypertonic saline 7.5%", "name_ja": "高張食塩水7.5%", "dose": "4 mL/kg IV slow bolus"},
            {
                "name": "Hydroxyethyl starch",
                "name_ja": "ヒドロキシエチルデンプン",
                "dose": "5 mL/kg IV (caution: AKI risk)",
            },
            {"name": "Norepinephrine", "name_ja": "ノルエピネフリン", "dose": "CRI 0.05-1 μg/kg/min"},
        ],
        "monitoring": [
            "Blood pressure (MAP target >65 mmHg)",
            "Lactate (target <2 mmol/L)",
            "Urine output (>1 mL/kg/h)",
            "PCV/TP",
            "ECG",
        ],
        "ref": "Silverstein & Hopper Small Animal Critical Care 2nd ed.",
    },
    # ============================================================
    # Anaphylaxis
    # ============================================================
    {
        "id": "anaphylaxis",
        "category": "anaphylaxis",
        "title_ja": "アナフィラキシー反応",
        "title_en": "Anaphylactic Reaction",
        "species": ["dog", "cat", "horse", "rabbit", "ferret"],
        "trigger_signs_ja": ["急性虚脱", "呼吸困難", "低血圧", "蕁麻疹/血管浮腫", "嘔吐/下痢", "顔面浮腫"],
        "trigger_signs_en": [
            "Acute collapse",
            "Dyspnea",
            "Hypotension",
            "Urticaria/angioedema",
            "Vomiting/diarrhea",
            "Facial edema",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Stop trigger",
                "ja": "原因薬物・抗原暴露を即座に中止。",
                "en": "Immediately stop the offending agent.",
                "time_target": "0秒",
            },
            {
                "order": 2,
                "phase": "Epinephrine (first-line)",
                "ja": "エピネフリン 0.01 mg/kg IM（1:1000の0.01 mL/kg）— 最重要。重症: 0.01-0.02 mg/kg IV slow ゆっくり静注。",
                "en": "Epinephrine 0.01 mg/kg IM (1:1000 0.01 mL/kg) — most important. Severe: 0.01-0.02 mg/kg IV slow.",
                "time_target": "即時",
            },
            {
                "order": 3,
                "phase": "Airway/Oxygen",
                "ja": "酸素投与 100% フローバイ または挿管。喉頭浮腫で挿管困難 → 緊急気管切開準備。",
                "en": "100% O2 flow-by or intubate. Laryngeal edema may require emergency tracheotomy.",
                "time_target": "並行",
            },
            {
                "order": 4,
                "phase": "Fluids",
                "ja": "LRS 10-20 mL/kg IV ボーラス（低血圧時）。",
                "en": "LRS 10-20 mL/kg IV bolus for hypotension.",
                "time_target": "並行",
            },
            {
                "order": 5,
                "phase": "Adjunct drugs",
                "ja": "デキサメタゾン 0.1-0.2 mg/kg IV。ジフェンヒドラミン 1-2 mg/kg IM（IVだと低血圧悪化）。",
                "en": "Dexamethasone 0.1-0.2 mg/kg IV. Diphenhydramine 1-2 mg/kg IM (IV worsens hypotension).",
                "time_target": "エピネフリン後",
            },
            {
                "order": 6,
                "phase": "Bronchodilator (if wheezing)",
                "ja": "テルブタリン 0.01 mg/kg SC または アルブテロール ネブライザー。",
                "en": "Terbutaline 0.01 mg/kg SC or albuterol nebulization.",
                "time_target": "気管支痙攣時",
            },
            {
                "order": 7,
                "phase": "Monitor & reassess",
                "ja": "二相性反応リスク → 4-6時間以上監視。エピネフリン反復可（5-15分間隔）。",
                "en": "Biphasic reaction risk → monitor ≥4-6h. Epinephrine may be repeated q5-15min.",
                "time_target": "持続",
            },
        ],
        "key_drugs": [
            {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.01 mg/kg IM (1:1000 = 0.01 mL/kg)"},
            {"name": "Dexamethasone", "name_ja": "デキサメタゾン", "dose": "0.1-0.2 mg/kg IV"},
            {"name": "Diphenhydramine", "name_ja": "ジフェンヒドラミン", "dose": "1-2 mg/kg IM"},
            {"name": "Terbutaline", "name_ja": "テルブタリン", "dose": "0.01 mg/kg SC (bronchospasm)"},
        ],
        "monitoring": ["Blood pressure", "Heart rate", "Respiratory rate", "SpO2", "Mucous membrane color"],
        "ref": "Shmuel & Cortes 2013 J Vet Emerg Crit Care",
    },
    # ============================================================
    # Status epilepticus
    # ============================================================
    {
        "id": "status_epilepticus",
        "category": "neurologic",
        "title_ja": "てんかん重積状態",
        "title_en": "Status Epilepticus",
        "species": ["dog", "cat"],
        "trigger_signs_ja": ["5分以上持続する痙攣", "意識回復のない反復痙攣"],
        "trigger_signs_en": [">5 min continuous seizure", "Recurrent seizures without consciousness recovery"],
        "steps": [
            {
                "order": 1,
                "phase": "Initial benzodiazepine",
                "ja": "ジアゼパム 0.5-1 mg/kg IV (slow). IV確保不能なら直腸内 1-2 mg/kg または鼻腔内。",
                "en": "Diazepam 0.5-1 mg/kg IV (slow). If no IV: per rectum 1-2 mg/kg or intranasal.",
                "time_target": "0-5分",
            },
            {
                "order": 2,
                "phase": "Repeat or escalate",
                "ja": "5-10分後再投与可（最大3回）。 反応不良 → ミダゾラム 0.2 mg/kg IV/IM/IN。",
                "en": "May repeat after 5-10 min (max 3 doses). If no response: Midazolam 0.2 mg/kg IV/IM/IN.",
                "time_target": "5-15分",
            },
            {
                "order": 3,
                "phase": "Loading",
                "ja": "持続: フェノバルビタール 16 mg/kg IV slow（必要に応じ4-8時間後追加 4 mg/kg）。",
                "en": "Persistent: Phenobarbital 16 mg/kg IV slow (additional 4 mg/kg q4-8h if needed).",
                "time_target": "15-30分",
            },
            {
                "order": 4,
                "phase": "Refractory SE",
                "ja": "プロポフォール CRI 0.1-0.6 mg/kg/min（挿管必要）。 または ケタミン 0.5-2 mg/kg IV bolus + CRI 5-30 μg/kg/min。",
                "en": "Propofol CRI 0.1-0.6 mg/kg/min (intubation required). Or Ketamine 0.5-2 mg/kg IV bolus + CRI 5-30 μg/kg/min.",
                "time_target": "30分以降",
            },
            {
                "order": 5,
                "phase": "Identify cause",
                "ja": "血糖（低血糖）、Ca、Na、毒物暴露、頭蓋内疾患、アジソン病を評価。",
                "en": "Evaluate glucose (hypoglycemia), Ca, Na, toxin exposure, intracranial disease, Addison's.",
                "time_target": "並行",
            },
            {
                "order": 6,
                "phase": "Supportive",
                "ja": "頭部冷却（高体温時）、酸素、IVF維持、体位変換、尿カテーテル。",
                "en": "Cooling (hyperthermia), oxygen, IVF, positional changes, urinary catheter.",
                "time_target": "持続",
            },
        ],
        "key_drugs": [
            {"name": "Diazepam", "name_ja": "ジアゼパム", "dose": "0.5-1 mg/kg IV / 1-2 mg/kg PR"},
            {"name": "Midazolam", "name_ja": "ミダゾラム", "dose": "0.2 mg/kg IV/IM/IN"},
            {"name": "Phenobarbital", "name_ja": "フェノバルビタール", "dose": "16 mg/kg IV slow loading"},
            {"name": "Propofol", "name_ja": "プロポフォール", "dose": "CRI 0.1-0.6 mg/kg/min"},
            {"name": "Levetiracetam", "name_ja": "レベチラセタム", "dose": "30-60 mg/kg IV slow (alternative)"},
        ],
        "monitoring": ["Body temperature", "ECG", "Blood pressure", "SpO2", "Glucose", "Pupillary reflexes"],
        "ref": "Charalambous et al. 2017 BMC Vet Res; ACVIM Consensus 2016",
    },
    # ============================================================
    # GDV
    # ============================================================
    {
        "id": "gdv",
        "category": "trauma",
        "title_ja": "胃拡張捻転 (GDV)",
        "title_en": "Gastric Dilatation-Volvulus (GDV)",
        "species": ["dog"],
        "trigger_signs_ja": ["腹部膨満", "非生産的嘔吐", "頻脈", "ショック徴候", "大型/胸深犬種"],
        "trigger_signs_en": [
            "Abdominal distension",
            "Non-productive vomiting",
            "Tachycardia",
            "Shock signs",
            "Large/deep-chested breed",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Stabilize",
                "ja": "大口径IV 2本 → LRS 20-30 mL/kg ボーラス（ショック輸液）。 酸素フローバイ。",
                "en": "Two large-bore IV lines → LRS 20-30 mL/kg bolus (shock fluids). Oxygen flow-by.",
                "time_target": "0-15分",
            },
            {
                "order": 2,
                "phase": "Decompression",
                "ja": "経鼻胃管 (オロガストリック) 試行 → 失敗時は経皮的trocarization (右側肋骨弓直後)。",
                "en": "Attempt orogastric intubation → if failed, percutaneous trocarization (right side, just behind costal arch).",
                "time_target": "輸液開始後即時",
            },
            {
                "order": 3,
                "phase": "Analgesia",
                "ja": "ブトルファノール 0.2-0.4 mg/kg IV または メタドン 0.2 mg/kg IV。",
                "en": "Butorphanol 0.2-0.4 mg/kg IV or Methadone 0.2 mg/kg IV.",
                "time_target": "並行",
            },
            {
                "order": 4,
                "phase": "Pre-op labs",
                "ja": "PCV/TP, 乳酸（>9 mmol/L = 胃壊死リスク高）、ECG（VPC多い）、電解質。",
                "en": "PCV/TP, lactate (>9 mmol/L = gastric necrosis risk), ECG (VPCs common), electrolytes.",
                "time_target": "並行",
            },
            {
                "order": 5,
                "phase": "Surgery",
                "ja": "緊急開腹 → 胃整復、胃壁検査（壊死部切除）、脾摘（梗塞時）、右胃固定術。",
                "en": "Emergency laparotomy → derotation, gastric viability assessment (resect necrotic), splenectomy if infarcted, right-sided gastropexy.",
                "time_target": "安定化後直ちに",
            },
            {
                "order": 6,
                "phase": "Post-op",
                "ja": "ICU管理: 輸液維持、抗菌薬、PPI、制吐薬、ECG連続監視（再灌流性不整脈）。",
                "en": "ICU: maintenance fluids, antibiotics, PPI, antiemetics, continuous ECG (reperfusion arrhythmias).",
                "time_target": "24-72時間",
            },
        ],
        "key_drugs": [
            {"name": "LRS", "name_ja": "乳酸リンゲル", "dose": "20-30 mL/kg shock bolus"},
            {"name": "Butorphanol", "name_ja": "ブトルファノール", "dose": "0.2-0.4 mg/kg IV"},
            {"name": "Methadone", "name_ja": "メタドン", "dose": "0.2 mg/kg IV"},
            {"name": "Cefazolin", "name_ja": "セファゾリン", "dose": "22 mg/kg IV pre-op"},
            {"name": "Lidocaine", "name_ja": "リドカイン", "dose": "2 mg/kg IV bolus + CRI for VPCs"},
        ],
        "monitoring": ["Lactate", "ECG", "Blood pressure", "PCV/TP", "Urine output"],
        "ref": "Beck et al. 2006 J Am Anim Hosp Assoc; Sharp & Rozanski 2014",
    },
    # ============================================================
    # Hypoglycemia
    # ============================================================
    {
        "id": "hypoglycemia",
        "category": "metabolic",
        "title_ja": "低血糖症",
        "title_en": "Hypoglycemia",
        "species": ["dog", "cat", "ferret", "puppy"],
        "trigger_signs_ja": ["虚脱", "痙攣", "失見当識", "震え", "低体温", "血糖<60 mg/dL"],
        "trigger_signs_en": ["Collapse", "Seizure", "Disorientation", "Trembling", "Hypothermia", "BG <60 mg/dL"],
        "steps": [
            {
                "order": 1,
                "phase": "Confirm",
                "ja": "血糖値測定（耳介・大網静脈）。<60 mg/dLで治療開始。",
                "en": "Measure BG (ear vein/marginal vein). Treat if <60 mg/dL.",
                "time_target": "即時",
            },
            {
                "order": 2,
                "phase": "Acute IV dextrose",
                "ja": "50%デキストロース 1-2 mL/kg を希釈（1:4以上）して IV slow（純50%は静脈炎）。",
                "en": "50% dextrose 1-2 mL/kg diluted (≥1:4) IV slow (undiluted causes phlebitis).",
                "time_target": "0-2分",
            },
            {
                "order": 3,
                "phase": "Maintenance",
                "ja": "2.5-5%デキストロース含有 LRS CRI（2 mL/kg/h目安）。 ⚠ インスリノーマ疑い時は控えめ（反跳性低血糖防止）。",
                "en": "Maintenance fluids with 2.5-5% dextrose (e.g., 2 mL/kg/h LRS). ⚠ If insulinoma suspected, use sparingly (rebound hypoglycemia).",
                "time_target": "2分以降",
            },
            {
                "order": 4,
                "phase": "Identify cause",
                "ja": "若齢: 異常哺育/敗血症/門脈シャント。成体: インスリノーマ/肝不全/アジソン/敗血症/中毒（キシリトール）。",
                "en": "Juvenile: starvation/sepsis/PSS. Adult: insulinoma/liver failure/Addison's/sepsis/xylitol toxicity.",
                "time_target": "並行",
            },
            {
                "order": 5,
                "phase": "Insulinoma-specific",
                "ja": "インスリノーマ確定 → プレドニゾロン 0.5-2 mg/kg PO q12h + ジアゾキシド 5-30 mg/kg PO q12h。 頻回給餌。",
                "en": "Confirmed insulinoma → Prednisolone 0.5-2 mg/kg PO q12h + Diazoxide 5-30 mg/kg PO q12h. Frequent small meals.",
                "time_target": "確定後",
            },
        ],
        "key_drugs": [
            {"name": "50% Dextrose", "name_ja": "50%デキストロース", "dose": "1-2 mL/kg IV slow (diluted ≥1:4)"},
            {"name": "Glucagon", "name_ja": "グルカゴン", "dose": "50 ng/kg/min CRI (refractory cases)"},
            {"name": "Diazoxide", "name_ja": "ジアゾキシド", "dose": "5-30 mg/kg PO q12h (insulinoma)"},
            {"name": "Prednisolone", "name_ja": "プレドニゾロン", "dose": "0.5-2 mg/kg PO q12h"},
        ],
        "monitoring": ["Blood glucose q1-2h initially", "Mentation", "Body temperature", "ECG"],
        "ref": "Plumb's 9th ed.; Macintire et al. Manual of Small Animal Emergency 2nd ed.",
    },
    # ============================================================
    # Acute kidney injury
    # ============================================================
    {
        "id": "aki",
        "category": "metabolic",
        "title_ja": "急性腎障害 (AKI)",
        "title_en": "Acute Kidney Injury (AKI)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": ["乏尿/無尿", "嘔吐", "BUN/クレアチニン急上昇", "高K血症", "脱水"],
        "trigger_signs_en": ["Oliguria/anuria", "Vomiting", "Acute BUN/creatinine rise", "Hyperkalemia", "Dehydration"],
        "steps": [
            {
                "order": 1,
                "phase": "Volume status",
                "ja": "脱水評価 → 等張晶質液で補正（15-30分でショックボーラス、その後欠乏量を6-12時間で補充）。",
                "en": "Assess hydration → correct with isotonic crystalloids (shock bolus 15-30 min, then deficit over 6-12h).",
                "time_target": "0-30分",
            },
            {
                "order": 2,
                "phase": "Hyperkalemia (K+ >7)",
                "ja": "Ca gluconate 10% 0.5-1 mL/kg IV（心筋保護）+ デキストロース+インスリン or NaHCO3 1-2 mEq/kg IV。",
                "en": "Ca gluconate 10% 0.5-1 mL/kg IV (cardioprotection) + dextrose+insulin OR NaHCO3 1-2 mEq/kg IV.",
                "time_target": "緊急",
            },
            {
                "order": 3,
                "phase": "Diuresis",
                "ja": "尿量モニタリング（目標>1 mL/kg/h）。 乏尿持続: フロセミド 2-6 mg/kg IV → 反応なし → マンニトール 0.5-1 g/kg IV slow。",
                "en": "Monitor urine output (target >1 mL/kg/h). Persistent oliguria: Furosemide 2-6 mg/kg IV → if no response → Mannitol 0.5-1 g/kg IV slow.",
                "time_target": "輸液後評価",
            },
            {
                "order": 4,
                "phase": "Identify cause",
                "ja": "毒物暴露（ブドウ・レーズン・エチレングリコール・NSAID・LIly猫）、感染（レプトスピラ等）、虚血を評価。",
                "en": "Evaluate toxin exposure (grapes, EG, NSAID, lilies in cats), infection (Lepto), ischemia.",
                "time_target": "並行",
            },
            {
                "order": 5,
                "phase": "Antiemetic",
                "ja": "マロピタント 1 mg/kg SC q24h + オンダンセトロン 0.5-1 mg/kg IV q8-12h。",
                "en": "Maropitant 1 mg/kg SC q24h + Ondansetron 0.5-1 mg/kg IV q8-12h.",
                "time_target": "並行",
            },
            {
                "order": 6,
                "phase": "Refractory",
                "ja": "輸液不応性乏尿/anuria → 透析（HD/PD）紹介検討。",
                "en": "Fluid-refractory oliguria/anuria → consider referral for dialysis (HD/PD).",
                "time_target": "24-48時間以内",
            },
        ],
        "key_drugs": [
            {"name": "Calcium gluconate 10%", "name_ja": "グルコン酸カルシウム10%", "dose": "0.5-1 mL/kg IV slow"},
            {"name": "Furosemide", "name_ja": "フロセミド", "dose": "2-6 mg/kg IV"},
            {"name": "Mannitol", "name_ja": "マンニトール", "dose": "0.5-1 g/kg IV slow over 15-20 min"},
            {"name": "Maropitant", "name_ja": "マロピタント", "dose": "1 mg/kg SC q24h"},
            {"name": "Ondansetron", "name_ja": "オンダンセトロン", "dose": "0.5-1 mg/kg IV q8-12h"},
        ],
        "monitoring": [
            "Urine output q4h",
            "BUN/Creatinine q12-24h",
            "Electrolytes (K+, Na+) q12h",
            "Body weight",
            "Blood pressure",
        ],
        "ref": "IRIS AKI Guidelines 2020; ACVIM Consensus 2018",
    },
    # ============================================================
    # Severe dyspnea / Respiratory failure
    # ============================================================
    {
        "id": "respiratory_failure",
        "category": "respiratory",
        "title_ja": "重度呼吸不全/気道閉塞",
        "title_en": "Severe Respiratory Distress / Airway Obstruction",
        "species": ["dog", "cat", "rabbit"],
        "trigger_signs_ja": ["開口呼吸（猫）", "起立呼吸", "チアノーゼ", "SpO2 <90%", "呼吸数>40（犬）/>50（猫）"],
        "trigger_signs_en": [
            "Open-mouth breathing (cat)",
            "Orthopnea",
            "Cyanosis",
            "SpO2 <90%",
            "RR >40 (dog) / >50 (cat)",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Minimize stress",
                "ja": "最小限の取扱い。酸素ケージ40-60%（フローバイより低ストレス）。",
                "en": "Minimal handling. Oxygen cage 40-60% (less stressful than flow-by).",
                "time_target": "即時",
            },
            {
                "order": 2,
                "phase": "Sedation if anxious",
                "ja": "ブトルファノール 0.2 mg/kg IM ± ミダゾラム 0.2 mg/kg IM。 ⚠ アセプロマジンは血圧低下リスク。",
                "en": "Butorphanol 0.2 mg/kg IM ± Midazolam 0.2 mg/kg IM. ⚠ Acepromazine causes hypotension.",
                "time_target": "酸素安定化後",
            },
            {
                "order": 3,
                "phase": "Localize cause",
                "ja": "上気道（吸気性ストライダー）/ 下気道（呼気性ウィーズ）/ 胸腔（胸腔穿刺で気胸/胸水確認）。",
                "en": "Localize: upper airway (inspiratory stridor) / lower airway (expiratory wheeze) / pleural space (thoracocentesis).",
                "time_target": "並行",
            },
            {
                "order": 4,
                "phase": "Pleural disease",
                "ja": "気胸/胸水疑い → 即時胸腔穿刺（背側 7-9肋間 = 気胸、腹側 = 胸水）。",
                "en": "Suspected pneumothorax/effusion → immediate thoracocentesis (dorsal 7-9 ICS = air, ventral = fluid).",
                "time_target": "即時",
            },
            {
                "order": 5,
                "phase": "Upper airway obstruction",
                "ja": "BOAS急性増悪/喉頭浮腫 → デキサメタゾン 0.1-0.2 mg/kg IV、酸素、 緊急挿管/気管切開準備。",
                "en": "BOAS crisis/laryngeal edema → Dexamethasone 0.1-0.2 mg/kg IV, oxygen, prep for emergency intubation/tracheostomy.",
                "time_target": "緊急",
            },
            {
                "order": 6,
                "phase": "Lower airway / asthma (cat)",
                "ja": "猫喘息: テルブタリン 0.01 mg/kg SC または アルブテロール ネブライザー + デキサメタゾン 0.1-0.2 mg/kg IV。",
                "en": "Feline asthma: Terbutaline 0.01 mg/kg SC or albuterol nebulization + Dexamethasone 0.1-0.2 mg/kg IV.",
                "time_target": "緊急",
            },
            {
                "order": 7,
                "phase": "Pulmonary edema (CHF)",
                "ja": "フロセミド 2-4 mg/kg IV/IM (犬) / 1-2 mg/kg (猫)、酸素、ピモベンダン 0.25 mg/kg PO（治療後）。",
                "en": "Furosemide 2-4 mg/kg IV/IM (dog) / 1-2 mg/kg (cat), oxygen, Pimobendan 0.25 mg/kg PO (after stabilization).",
                "time_target": "緊急",
            },
        ],
        "key_drugs": [
            {"name": "Furosemide", "name_ja": "フロセミド", "dose": "2-4 mg/kg IV/IM dog; 1-2 mg/kg cat (CHF)"},
            {"name": "Dexamethasone", "name_ja": "デキサメタゾン", "dose": "0.1-0.2 mg/kg IV"},
            {"name": "Terbutaline", "name_ja": "テルブタリン", "dose": "0.01 mg/kg SC (bronchospasm)"},
            {"name": "Butorphanol", "name_ja": "ブトルファノール", "dose": "0.2 mg/kg IM (sedation)"},
            {"name": "Midazolam", "name_ja": "ミダゾラム", "dose": "0.2 mg/kg IM (sedation)"},
        ],
        "monitoring": ["SpO2 (target >95%)", "RR/effort", "Mucous membrane color", "Lung auscultation"],
        "ref": "Mazzaferro Small Animal Emergency 2018; ACVIM CHF Consensus 2019",
    },
]


def list_protocols(species: str = "", category: str = "", search: str = "") -> list[dict[str, Any]]:
    """プロトコル一覧を取得（フィルタ対応）"""
    species = (species or "").lower().strip()
    category = (category or "").lower().strip()
    search = (search or "").lower().strip()

    out = []
    for p in EMERGENCY_PROTOCOLS:
        if species and species not in p.get("species", []):
            continue
        if category and category != p.get("category", ""):
            continue
        if search:
            haystack = " ".join(
                [
                    p.get("title_ja", ""),
                    p.get("title_en", ""),
                    " ".join(p.get("trigger_signs_ja", [])),
                    " ".join(p.get("trigger_signs_en", [])),
                ]
            ).lower()
            if search not in haystack:
                continue
        out.append(p)
    return out


def get_protocol(protocol_id: str) -> dict[str, Any] | None:
    """ID指定でプロトコル取得"""
    for p in EMERGENCY_PROTOCOLS:
        if p.get("id") == protocol_id:
            return p
    return None
