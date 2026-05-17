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
    # ============================================================
    # Heatstroke
    # ============================================================
    {
        "id": "heatstroke",
        "category": "metabolic",
        "title_ja": "熱中症（重度高体温）",
        "title_en": "Heatstroke (Severe Hyperthermia)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": [
            "体温>41°C",
            "パンティング/開口呼吸",
            "粘膜充血→チアノーゼ",
            "虚脱",
            "嘔吐/下痢（血性）",
            "DIC徴候",
        ],
        "trigger_signs_en": [
            "BT >41°C (106°F)",
            "Excessive panting",
            "Brick-red→cyanotic MM",
            "Collapse",
            "Vomiting/bloody diarrhea",
            "DIC signs",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Active cooling",
                "ja": "冷水スプレー + 扇風機。⚠氷水浴は末梢血管収縮で逆効果。大血管走行部（頸・腋窩・鼠径）にクーリングパック。",
                "en": "Cool water spray + fan. ⚠ Ice bath causes vasoconstriction (counterproductive). Apply cooling packs to large vessels (neck, axilla, groin).",
                "time_target": "即時",
            },
            {
                "order": 2,
                "phase": "Target temp",
                "ja": "39.5°Cで積極的冷却中止（過冷却防止）。体温q5分モニタリング。",
                "en": "Stop active cooling at 39.5°C (103°F) to prevent overshoot. Monitor BT q5min.",
                "time_target": "10-30分",
            },
            {
                "order": 3,
                "phase": "IV fluids",
                "ja": "LRS 10-20 mL/kg IV ボーラス（室温液）。⚠冷却液は不要。",
                "en": "Room temp LRS 10-20 mL/kg IV bolus. ⚠ Chilled fluids not needed.",
                "time_target": "並行",
            },
            {
                "order": 4,
                "phase": "Coagulopathy",
                "ja": "PT/aPTT/フィブリノゲン/D-dimer/血小板。DIC → FFP 10-15 mL/kg IV。",
                "en": "Check PT/aPTT/fibrinogen/D-dimer/platelets. DIC → FFP 10-15 mL/kg IV.",
                "time_target": "30分以内",
            },
            {
                "order": 5,
                "phase": "Organ protection",
                "ja": "腎：輸液+尿量モニタリング。肝：ALT/biliモニタリング。腸：マロピタント+制酸薬。脳：痙攣→ジアゼパム。",
                "en": "Renal: fluids + UO monitoring. Hepatic: ALT/bili. GI: maropitant + PPI. CNS: diazepam if seizures.",
                "time_target": "持続",
            },
            {
                "order": 6,
                "phase": "⚠ Do NOT",
                "ja": "解熱薬（NSAIDs/ステロイド）禁忌：セットポイントは正常→薬理学的解熱は無意味かつ有害。",
                "en": "⚠ Do NOT give antipyretics (NSAIDs/steroids) — thermostat set-point is normal; chemical antipyresis is useless and harmful.",
                "time_target": "常に",
            },
        ],
        "key_drugs": [
            {"name": "LRS (room temp)", "name_ja": "乳酸リンゲル（室温）", "dose": "10-20 mL/kg IV bolus"},
            {"name": "FFP", "name_ja": "新鮮凍結血漿", "dose": "10-15 mL/kg IV (DIC)"},
            {"name": "Maropitant", "name_ja": "マロピタント", "dose": "1 mg/kg SC/IV q24h"},
            {"name": "Diazepam", "name_ja": "ジアゼパム", "dose": "0.5-1 mg/kg IV (seizures)"},
        ],
        "monitoring": [
            "Body temperature q5min until 39.5°C",
            "PT/aPTT/platelets",
            "BUN/Cr/ALT/bilirubin",
            "Urine output",
            "Blood glucose",
            "ECG",
        ],
        "ref": "Bruchim 2017 JVIM; Drobatz & Macintire 1996 JAVMA",
    },
    # ============================================================
    # Feline Urinary Obstruction
    # ============================================================
    {
        "id": "feline_urinary_obstruction",
        "category": "metabolic",
        "title_ja": "猫の尿路閉塞 (FUO)",
        "title_en": "Feline Urinary Obstruction (FUO)",
        "species": ["cat"],
        "trigger_signs_ja": [
            "排尿努責（空振り）",
            "嘔吐",
            "元気消失",
            "膀胱過膨張（硬い大きな膀胱触知）",
            "徐脈（高K）",
            "低体温",
        ],
        "trigger_signs_en": [
            "Stranguria (non-productive)",
            "Vomiting",
            "Lethargy",
            "Large firm bladder",
            "Bradycardia (hyperK)",
            "Hypothermia",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Stabilize hyperK",
                "ja": "ECG: テント状T波/QRS幅広/徐脈 → Ca gluconate 10% 0.5-1 mL/kg IV slow（心筋安定化）。",
                "en": "ECG: peaked T/wide QRS/bradycardia → Ca gluconate 10% 0.5-1 mL/kg IV slow (cardioprotection).",
                "time_target": "即時",
            },
            {
                "order": 2,
                "phase": "IV fluids",
                "ja": "0.9% NaCl IV（⚠LRSはK含有→高K時回避）。",
                "en": "0.9% NaCl IV (⚠ avoid LRS — contains K+).",
                "time_target": "即時",
            },
            {
                "order": 3,
                "phase": "Relieve obstruction",
                "ja": "鎮静（ブトルファノール0.2 mg/kg + ミダゾラム0.2 mg/kg IM/IV）→ 3.5Fr尿道カテーテル挿入+フラッシュ。",
                "en": "Sedate (butorphanol 0.2 mg/kg + midazolam 0.2 mg/kg IM/IV) → insert 3.5Fr urinary catheter, flush with saline.",
                "time_target": "安定化後",
            },
            {
                "order": 4,
                "phase": "Post-obstructive diuresis",
                "ja": "閉塞解除後は大量利尿あり → IV fluids 2-3×維持量 × 24-48h。尿量モニタリング。",
                "en": "Expect post-obstructive diuresis → IV fluids 2-3× maintenance × 24-48h. Monitor UO.",
                "time_target": "解除後24-48h",
            },
            {
                "order": 5,
                "phase": "Monitor",
                "ja": "電解質（K+, Ca, P）q6-12h。BUN/Cr q12-24h。ECG。",
                "en": "Electrolytes (K+, Ca, P) q6-12h. BUN/Cr q12-24h. ECG.",
                "time_target": "入院中",
            },
            {
                "order": 6,
                "phase": "Long-term",
                "ja": "再発予防: 処方食（S/O等）、飲水促進、ストレス軽減。再発3回以上 → 会陰尿道瘻術（PU）。",
                "en": "Prevention: prescription diet, increase water intake, reduce stress. Recurrence ≥3 → perineal urethrostomy (PU).",
                "time_target": "退院後",
            },
        ],
        "key_drugs": [
            {
                "name": "Calcium gluconate 10%",
                "name_ja": "グルコン酸カルシウム10%",
                "dose": "0.5-1 mL/kg IV slow over 5-10 min (hyperK)",
            },
            {"name": "0.9% NaCl", "name_ja": "生理食塩水", "dose": "IV at 2-3× maintenance"},
            {"name": "Butorphanol", "name_ja": "ブトルファノール", "dose": "0.2-0.4 mg/kg IM/IV (sedation/analgesia)"},
            {
                "name": "Buprenorphine",
                "name_ja": "ブプレノルフィン",
                "dose": "0.02 mg/kg IV/buccal q6-8h (post-op analgesia)",
            },
            {"name": "Prazosin", "name_ja": "プラゾシン", "dose": "0.25-0.5 mg/cat PO q12h (urethral relaxant)"},
        ],
        "monitoring": ["ECG (hyperK)", "Serum K+ q6-12h", "BUN/Cr", "Urine output q4h", "Bladder size (palpation/US)"],
        "ref": "Drobatz & Costello 2012 JVECCS; ACVIM Feline Lower Urinary Tract Disease 2016",
    },
    # ============================================================
    # Pyometra
    # ============================================================
    {
        "id": "pyometra",
        "category": "trauma",
        "title_ja": "子宮蓄膿症（開放/閉鎖）",
        "title_en": "Pyometra (Open / Closed)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": [
            "陰部膣分泌物（開放型）",
            "腹部膨満（閉鎖型）",
            "多飲多尿",
            "嘔吐/食欲廃絶",
            "発熱→低体温（敗血症）",
        ],
        "trigger_signs_en": [
            "Vaginal discharge (open)",
            "Abdominal distension (closed)",
            "PU/PD",
            "Vomiting/anorexia",
            "Fever→hypothermia (sepsis)",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Stabilize",
                "ja": "輸液: LRS 10-20 mL/kg ボーラス（敗血症ならショック輸液）。広域抗菌薬開始。",
                "en": "Fluids: LRS 10-20 mL/kg bolus (shock dose if sepsis). Start broad-spectrum antibiotics.",
                "time_target": "0-30分",
            },
            {
                "order": 2,
                "phase": "Antibiotics",
                "ja": "アンピシリン/スルバクタム 20 mg/kg IV q8h + エンロフロキサシン 5 mg/kg IV q24h。",
                "en": "Ampicillin/sulbactam 20 mg/kg IV q8h + Enrofloxacin 5 mg/kg IV q24h.",
                "time_target": "即時",
            },
            {
                "order": 3,
                "phase": "Surgery (definitive)",
                "ja": "OVH: 全身麻酔下卵巣子宮摘出術（可能な限り早期 — 閉鎖型は緊急度高）。",
                "en": "OVH: ovariohysterectomy under GA (ASAP — closed pyometra is more urgent).",
                "time_target": "安定化後6-12h以内",
            },
            {
                "order": 4,
                "phase": "Medical (breeding)",
                "ja": "繁殖希望: PGF2α（ジノプロスト）0.1-0.25 mg/kg SC q12-24h ×3-7d + 抗菌薬。⚠閉鎖型は子宮破裂リスク。",
                "en": "Breeding value: PGF2α (dinoprost) 0.1-0.25 mg/kg SC q12-24h ×3-7d + antibiotics. ⚠ Closed pyometra = uterine rupture risk.",
                "time_target": "OVH不可の場合のみ",
            },
            {
                "order": 5,
                "phase": "Post-op",
                "ja": "輸液維持、抗菌薬継続7-10日、メロキシカム0.1-0.2 mg/kg q24h。",
                "en": "Maintenance fluids, continue antibiotics 7-10d, meloxicam 0.1-0.2 mg/kg q24h.",
                "time_target": "術後",
            },
        ],
        "key_drugs": [
            {"name": "Ampicillin/sulbactam", "name_ja": "アンピシリン/スルバクタム", "dose": "20 mg/kg IV q8h"},
            {"name": "Enrofloxacin", "name_ja": "エンロフロキサシン", "dose": "5 mg/kg IV/PO q24h"},
            {"name": "Metronidazole", "name_ja": "メトロニダゾール", "dose": "10-15 mg/kg IV q12h (anaerobes)"},
            {
                "name": "PGF2α (dinoprost)",
                "name_ja": "ジノプロスト",
                "dose": "0.1-0.25 mg/kg SC (medical management only)",
            },
        ],
        "monitoring": [
            "Temperature q4h",
            "WBC/band neutrophils",
            "Blood glucose (hypoglycemia in sepsis)",
            "Blood pressure",
            "Urine output",
        ],
        "ref": "Jitpean et al. 2017 Theriogenology; Hagman 2018 Vet Clin NA",
    },
    # ============================================================
    # Pneumothorax
    # ============================================================
    {
        "id": "pneumothorax",
        "category": "respiratory",
        "title_ja": "気胸（緊張性/開放性/自然気胸）",
        "title_en": "Pneumothorax (Tension / Open / Spontaneous)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": ["急性呼吸困難", "頻呼吸", "浅速呼吸", "チアノーゼ", "聴診：背側で肺音減弱/消失", "外傷歴"],
        "trigger_signs_en": [
            "Acute dyspnea",
            "Tachypnea",
            "Shallow rapid breathing",
            "Cyanosis",
            "Absent lung sounds dorsally",
            "Trauma history",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Thoracocentesis",
                "ja": "即時胸腔穿刺: 背側7-9肋間、バタフライカテーテルまたは18-20G針+三方活栓+シリンジ。",
                "en": "Immediate thoracocentesis: dorsal 7-9th ICS, butterfly catheter or 18-20G needle + 3-way stopcock + syringe.",
                "time_target": "即時",
            },
            {
                "order": 2,
                "phase": "Oxygen",
                "ja": "100%酸素フローバイまたはケージ。",
                "en": "100% O2 flow-by or cage.",
                "time_target": "並行",
            },
            {
                "order": 3,
                "phase": "Tension pneumo",
                "ja": "緊張性: 縦隔偏位 → 即時大量脱気（生命を脅かす）。胸腔ドレーン留置。",
                "en": "Tension: mediastinal shift → immediate large-volume evacuation (life-threatening). Place chest drain.",
                "time_target": "緊急",
            },
            {
                "order": 4,
                "phase": "Chest drain",
                "ja": "持続/反復性 → 胸腔ドレーン（トロカール）留置。間欠的吸引または水封ドレナージ。",
                "en": "Persistent/recurrent → thoracostomy tube (trocar). Intermittent aspiration or underwater seal drainage.",
                "time_target": "穿刺で再貯留時",
            },
            {
                "order": 5,
                "phase": "Imaging",
                "ja": "安定後: 胸部X線。外傷性: 肺/大血管損傷評価。自然気胸: 肺ブラ/ブレブ（CT推奨）。",
                "en": "After stabilization: thoracic radiography. Traumatic: assess lung/vessel injury. Spontaneous: bullae/blebs (CT recommended).",
                "time_target": "安定後",
            },
            {
                "order": 6,
                "phase": "Surgery",
                "ja": "持続空気漏出/自然気胸 → 探索的開胸（肺葉切除）。外傷性大半は保存的管理で改善。",
                "en": "Persistent air leak / spontaneous → exploratory thoracotomy (lung lobectomy). Most traumatic cases resolve conservatively.",
                "time_target": "48-72h改善なし",
            },
        ],
        "key_drugs": [
            {
                "name": "Butorphanol",
                "name_ja": "ブトルファノール",
                "dose": "0.2-0.4 mg/kg IM/IV (analgesia/mild sedation)",
            },
            {"name": "Buprenorphine", "name_ja": "ブプレノルフィン", "dose": "0.02 mg/kg IV/buccal q6-8h (analgesia)"},
            {"name": "Lidocaine 2%", "name_ja": "リドカイン2%", "dose": "Local infiltration at drain site"},
        ],
        "monitoring": [
            "Respiratory rate/effort",
            "SpO2",
            "Chest drain output (volume + air)",
            "Thoracic radiography q12-24h",
        ],
        "ref": "Puerto et al. 2002 J Am Anim Hosp Assoc; Sigrist & Adamik 2019",
    },
    # ============================================================
    # Chocolate/Theobromine Toxicosis
    # ============================================================
    {
        "id": "chocolate_toxicosis",
        "category": "toxicity",
        "title_ja": "チョコレート中毒（テオブロミン/カフェイン）",
        "title_en": "Chocolate / Theobromine Toxicosis",
        "species": ["dog"],
        "trigger_signs_ja": ["嘔吐/下痢", "多尿", "興奮/過活動", "頻脈", "心室性不整脈", "痙攣（重症）"],
        "trigger_signs_en": [
            "Vomiting/diarrhea",
            "Polyuria",
            "Hyperactivity/restlessness",
            "Tachycardia",
            "Ventricular arrhythmias",
            "Seizures (severe)",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Assess dose",
                "ja": "テオブロミン有毒量: 犬20 mg/kg（軽度）→40-50 mg/kg（心毒性）→60+ mg/kg（痙攣/死亡）。チョコレート種別で含有量大幅差。",
                "en": "Toxic dose theobromine: 20 mg/kg (mild) → 40-50 mg/kg (cardiac) → 60+ mg/kg (seizures/death). Varies greatly by chocolate type.",
                "time_target": "即時評価",
            },
            {
                "order": 2,
                "phase": "Decontamination",
                "ja": "摂取2h以内: 催吐（アポモルフィン0.03 mg/kg IV/結膜嚢）。活性炭1-2 g/kg PO（カタルシス剤と）。",
                "en": "If <2h post-ingestion: emesis (apomorphine 0.03 mg/kg IV/conjunctival). Activated charcoal 1-2 g/kg PO (with cathartic).",
                "time_target": "摂取2h以内",
            },
            {
                "order": 3,
                "phase": "Cardiac monitoring",
                "ja": "ECG連続モニタリング。VPC/VT → リドカイン 2 mg/kg IV ボーラス → CRI 25-80 μg/kg/min。",
                "en": "Continuous ECG. VPCs/VT → Lidocaine 2 mg/kg IV bolus → CRI 25-80 μg/kg/min.",
                "time_target": "入院中",
            },
            {
                "order": 4,
                "phase": "Seizure control",
                "ja": "ジアゼパム 0.5-1 mg/kg IV。反復 → フェノバルビタール。",
                "en": "Diazepam 0.5-1 mg/kg IV. If refractory → phenobarbital.",
                "time_target": "痙攣時",
            },
            {
                "order": 5,
                "phase": "Supportive",
                "ja": "輸液: 排泄促進（テオブロミンは膀胱再吸収あり → 尿カテーテル留置推奨）。制吐薬。",
                "en": "IV fluids to promote excretion (theobromine undergoes enterohepatic recirculation → urinary catheter recommended). Antiemetics.",
                "time_target": "持続",
            },
        ],
        "key_drugs": [
            {"name": "Apomorphine", "name_ja": "アポモルフィン", "dose": "0.03 mg/kg IV or conjunctival (emesis)"},
            {
                "name": "Activated charcoal",
                "name_ja": "活性炭",
                "dose": "1-2 g/kg PO (repeat q6-8h for enterohepatic recirculation)",
            },
            {
                "name": "Lidocaine",
                "name_ja": "リドカイン",
                "dose": "2 mg/kg IV bolus → CRI 25-80 μg/kg/min (arrhythmias)",
            },
            {"name": "Diazepam", "name_ja": "ジアゼパム", "dose": "0.5-1 mg/kg IV (seizures)"},
            {"name": "Maropitant", "name_ja": "マロピタント", "dose": "1 mg/kg SC/IV q24h (antiemetic)"},
        ],
        "monitoring": ["ECG continuous", "Blood pressure", "Body temperature", "Urine output", "Neurological status"],
        "ref": "Gwaltney-Brant 2001 Vet Med; ASPCA APCC database",
    },
    # ============================================================
    # Xylitol Toxicosis
    # ============================================================
    {
        "id": "xylitol_toxicosis",
        "category": "toxicity",
        "title_ja": "キシリトール中毒",
        "title_en": "Xylitol Toxicosis",
        "species": ["dog"],
        "trigger_signs_ja": ["嘔吐", "虚脱/脱力", "低血糖（30分-12h後）", "肝不全（24-72h後、高用量）", "凝固障害"],
        "trigger_signs_en": [
            "Vomiting",
            "Weakness/collapse",
            "Hypoglycemia (30min-12h)",
            "Hepatic failure (24-72h, high dose)",
            "Coagulopathy",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Assess dose",
                "ja": "低血糖: >0.1 g/kg。肝不全: >0.5 g/kg。⚠ガム1枚≈0.3-1g。",
                "en": "Hypoglycemia: >0.1 g/kg. Hepatic failure: >0.5 g/kg. ⚠ One gum piece ≈ 0.3-1g.",
                "time_target": "即時",
            },
            {
                "order": 2,
                "phase": "Decontamination",
                "ja": "摂取30分以内かつ無症状: 催吐。⚠既に低血糖なら催吐禁忌（痙攣リスク）。",
                "en": "If <30min and asymptomatic: induce emesis. ⚠ If already hypoglycemic, do NOT induce vomiting (seizure risk).",
                "time_target": "30分以内",
            },
            {
                "order": 3,
                "phase": "Dextrose",
                "ja": "血糖確認 → 50%デキストロース 1-2 mL/kg 希釈IV → 2.5-5%デキストロースCRI維持。",
                "en": "Check BG → 50% dextrose 1-2 mL/kg diluted IV → maintain with 2.5-5% dextrose CRI.",
                "time_target": "即時",
            },
            {
                "order": 4,
                "phase": "Hepatoprotection",
                "ja": "高用量摂取 → SAMe 20 mg/kg PO q24h + シリマリン。肝酵素モニタリング72h。",
                "en": "High dose → SAMe 20 mg/kg PO q24h + silymarin. Monitor liver enzymes for 72h.",
                "time_target": ">0.5 g/kg時",
            },
            {
                "order": 5,
                "phase": "Monitor",
                "ja": "血糖q1-2h×12h。肝酵素/PT q12-24h×72h。FFP if凝固障害。",
                "en": "Blood glucose q1-2h ×12h. Liver enzymes/PT q12-24h ×72h. FFP if coagulopathy.",
                "time_target": "入院中",
            },
        ],
        "key_drugs": [
            {
                "name": "50% Dextrose",
                "name_ja": "50%デキストロース",
                "dose": "1-2 mL/kg diluted (≥1:4) IV slow → CRI 2.5-5%",
            },
            {"name": "SAMe", "name_ja": "S-アデノシルメチオニン", "dose": "20 mg/kg PO q24h (hepatoprotection)"},
            {"name": "Vitamin K1", "name_ja": "ビタミンK1", "dose": "2.5-5 mg/kg SC q12h (if coagulopathy)"},
            {"name": "FFP", "name_ja": "新鮮凍結血漿", "dose": "10-15 mL/kg IV (if PT prolonged)"},
        ],
        "monitoring": ["Blood glucose q1-2h ×12h", "ALT/AST/ALP q12-24h", "PT/aPTT", "Bilirubin", "Mentation"],
        "ref": "Dunayer 2006 Vet Ther; Murphy & Dunayer 2018 ASPCA",
    },
    # ============================================================
    # Rodenticide (Anticoagulant) Toxicosis
    # ============================================================
    {
        "id": "anticoagulant_rodenticide",
        "category": "toxicity",
        "title_ja": "抗凝固性殺鼠剤中毒",
        "title_en": "Anticoagulant Rodenticide Toxicosis",
        "species": ["dog", "cat"],
        "trigger_signs_ja": [
            "出血（摂取2-5日後）",
            "紫斑/点状出血",
            "血尿/メレナ/喀血",
            "虚脱/蒼白",
            "呼吸困難（胸腔内出血）",
        ],
        "trigger_signs_en": [
            "Hemorrhage (2-5d post-ingestion)",
            "Bruising/petechiae",
            "Hematuria/melena/hemoptysis",
            "Collapse/pallor",
            "Dyspnea (pleural hemorrhage)",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Recent ingestion",
                "ja": "摂取2-4h以内: 催吐 + 活性炭。⚠既に出血中なら催吐禁忌。",
                "en": "If <2-4h: induce emesis + activated charcoal. ⚠ If already bleeding, do NOT induce vomiting.",
                "time_target": "4h以内",
            },
            {
                "order": 2,
                "phase": "Vitamin K1",
                "ja": "ビタミンK1 2.5-5 mg/kg PO q12h（食事と — 脂肪で吸収↑）。第1世代: 14日。第2世代: 4-6週。",
                "en": "Vitamin K1 2.5-5 mg/kg PO q12h (with fatty food for absorption). 1st gen: 14d. 2nd gen: 4-6 weeks.",
                "time_target": "即時開始",
            },
            {
                "order": 3,
                "phase": "Active bleeding",
                "ja": "大量出血 → FFP 10-15 mL/kg IV + 全血輸血（PCV<15%）。⚠ 輸血はK1効果待ち（6-12h）のブリッジ。",
                "en": "Severe hemorrhage → FFP 10-15 mL/kg IV + whole blood transfusion (PCV <15%). Transfusion bridges until K1 takes effect (6-12h).",
                "time_target": "出血時即時",
            },
            {
                "order": 4,
                "phase": "Identify product",
                "ja": "殺鼠剤パッケージ確認: 第1世代（ワルファリン）vs 第2世代（ブロジファクム/ブロマジオロン）。世代で治療期間が異なる。",
                "en": "Identify product: 1st gen (warfarin) vs 2nd gen (brodifacoum/bromadiolone). Treatment duration differs.",
                "time_target": "並行",
            },
            {
                "order": 5,
                "phase": "PT test protocol",
                "ja": "K1投与終了48-72h後にPT再検 → 延長していれば継続。正常なら終了。",
                "en": "Recheck PT 48-72h after last K1 dose → if prolonged, continue. If normal, stop.",
                "time_target": "K1終了後",
            },
        ],
        "key_drugs": [
            {
                "name": "Vitamin K1 (phytonadione)",
                "name_ja": "ビタミンK1",
                "dose": "2.5-5 mg/kg PO q12h with fatty food (4-6 weeks for 2nd gen)",
            },
            {"name": "FFP", "name_ja": "新鮮凍結血漿", "dose": "10-15 mL/kg IV (immediate clotting factors)"},
            {"name": "Activated charcoal", "name_ja": "活性炭", "dose": "1-2 g/kg PO (recent ingestion only)"},
            {
                "name": "Apomorphine",
                "name_ja": "アポモルフィン",
                "dose": "0.03 mg/kg IV (emesis if <2-4h post ingestion)",
            },
        ],
        "monitoring": [
            "PT/PTT (baseline, 48-72h after K1 stops)",
            "PCV/TP",
            "Chest/abdominal radiographs (if hemorrhage suspected)",
            "Platelet count",
        ],
        "ref": "DeClementi & Sobczak 2012 Vet Clin NA; Waddell & Poppenga 2008 JVECCS",
    },
    # ============================================================
    # DKA
    # ============================================================
    {
        "id": "dka",
        "category": "metabolic",
        "title_ja": "糖尿病性ケトアシドーシス (DKA)",
        "title_en": "Diabetic Ketoacidosis (DKA)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": ["嘔吐/食欲廃絶", "多飲多尿", "脱水", "アセトン臭", "クスマウル呼吸（深大呼吸）", "虚脱"],
        "trigger_signs_en": [
            "Vomiting/anorexia",
            "PU/PD",
            "Dehydration",
            "Acetone breath",
            "Kussmaul breathing",
            "Collapse",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Fluids first",
                "ja": "0.9% NaCl IV: 脱水欠乏量を6-12hで補正 + 維持量。⚠脳浮腫防止のため急速補正回避。",
                "en": "0.9% NaCl IV: replace deficit over 6-12h + maintenance. ⚠ Avoid too-rapid correction (cerebral edema risk).",
                "time_target": "0-6h",
            },
            {
                "order": 2,
                "phase": "Insulin CRI",
                "ja": "レギュラーインスリン CRI: 犬 0.05-0.1 U/kg/hr IV、猫 0.05 U/kg/hr。⚠IM低用量法も可。",
                "en": "Regular insulin CRI: dog 0.05-0.1 U/kg/hr IV; cat 0.05 U/kg/hr. IM low-dose protocol alternative.",
                "time_target": "輸液開始1-2h後",
            },
            {
                "order": 3,
                "phase": "Glucose monitoring",
                "ja": "血糖q1-2h。BG 200-250 mg/dL到達 → 輸液に2.5-5%デキストロース追加（インスリン継続）。",
                "en": "BG q1-2h. When BG reaches 200-250 → add 2.5-5% dextrose to fluids (continue insulin).",
                "time_target": "q1-2h",
            },
            {
                "order": 4,
                "phase": "Potassium",
                "ja": "K+補正（ほぼ全例で必要）: インスリンがKを細胞内移行させるため。20-40 mEq/L添加。",
                "en": "K+ supplementation (needed in virtually all cases): insulin shifts K+ intracellular. Add 20-40 mEq/L to fluids.",
                "time_target": "K+結果後",
            },
            {
                "order": 5,
                "phase": "Phosphate",
                "ja": "重度低P（<1.5 mg/dL）→ KPO4 0.01-0.03 mmol/kg/hr IV。",
                "en": "Severe hypophosphatemia (<1.5 mg/dL) → KPO4 0.01-0.03 mmol/kg/hr IV.",
                "time_target": "P測定後",
            },
            {
                "order": 6,
                "phase": "Transition",
                "ja": "食欲回復+ケトン消失 → 皮下インスリン（NPH/グラルギン）に移行。CRI漸減。",
                "en": "When eating + ketones cleared → transition to SC insulin (NPH/glargine). Taper CRI.",
                "time_target": "臨床的改善後",
            },
        ],
        "key_drugs": [
            {
                "name": "Regular insulin",
                "name_ja": "レギュラーインスリン",
                "dose": "CRI 0.05-0.1 U/kg/hr IV (dog); 0.05 U/kg/hr (cat)",
            },
            {"name": "0.9% NaCl", "name_ja": "生理食塩水", "dose": "Deficit replacement + maintenance"},
            {
                "name": "KCl",
                "name_ja": "塩化カリウム",
                "dose": "20-40 mEq/L added to fluids (adjust based on serum K+)",
            },
            {"name": "Maropitant", "name_ja": "マロピタント", "dose": "1 mg/kg SC/IV q24h (nausea)"},
            {
                "name": "NaHCO3",
                "name_ja": "炭酸水素ナトリウム",
                "dose": "1-2 mEq/kg IV slow ONLY if pH <7.0 (controversial)",
            },
        ],
        "monitoring": [
            "Blood glucose q1-2h",
            "Serum K+ q4-6h",
            "Blood gas (pH, HCO3-) q6-12h",
            "Urine ketones",
            "Phosphorus q12h",
        ],
        "ref": "Hess 2010 JVIM; ACVIM Consensus Diabetes 2018",
    },
    # ============================================================
    # Addisonian Crisis
    # ============================================================
    {
        "id": "addisonian_crisis",
        "category": "metabolic",
        "title_ja": "副腎クリーゼ（アジソン病急性増悪）",
        "title_en": "Addisonian Crisis (Acute Hypoadrenocorticism)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": ["虚脱/ショック", "徐脈（高K）", "嘔吐/下痢", "低体温", "低血圧", "Na/K比<27"],
        "trigger_signs_en": [
            "Collapse/shock",
            "Bradycardia (hyperK)",
            "Vomiting/diarrhea",
            "Hypothermia",
            "Hypotension",
            "Na:K ratio <27",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Aggressive fluids",
                "ja": "0.9% NaCl 20-30 mL/kg IV ボーラス（ショック輸液）。⚠LRS回避（K含有）。",
                "en": "0.9% NaCl 20-30 mL/kg IV bolus (shock dose). ⚠ Avoid LRS (contains K+).",
                "time_target": "即時",
            },
            {
                "order": 2,
                "phase": "Treat hyperK",
                "ja": "K+>7 → Ca gluconate 10% 0.5-1 mL/kg IV slow。⚠輸液のみでK+は希釈・改善されることが多い。",
                "en": "K+ >7 → Ca gluconate 10% 0.5-1 mL/kg IV slow. ⚠ Fluids alone often dilute K+ sufficiently.",
                "time_target": "ECG異常時",
            },
            {
                "order": 3,
                "phase": "Glucocorticoid",
                "ja": "デキサメタゾン 0.1-0.2 mg/kg IV（ACTH刺激試験に干渉しない唯一のGC）。",
                "en": "Dexamethasone 0.1-0.2 mg/kg IV (only GC that does NOT interfere with ACTH stim test).",
                "time_target": "輸液と同時",
            },
            {
                "order": 4,
                "phase": "ACTH test",
                "ja": "安定後: ACTH刺激試験（cortisol pre/post）で確定診断。⚠危機的状況ではテスト前に治療開始。",
                "en": "After stabilization: ACTH stimulation test (confirm). ⚠ In crisis, treat BEFORE testing.",
                "time_target": "安定後",
            },
            {
                "order": 5,
                "phase": "Maintenance",
                "ja": "確定後: DOCP (desoxycorticosterone) 2.2 mg/kg IM q25d + プレドニゾロン 0.2 mg/kg PO q24h。",
                "en": "After diagnosis: DOCP 2.2 mg/kg IM q25d + prednisolone 0.2 mg/kg PO q24h.",
                "time_target": "確定後",
            },
        ],
        "key_drugs": [
            {"name": "0.9% NaCl", "name_ja": "生理食塩水", "dose": "20-30 mL/kg IV bolus (shock)"},
            {
                "name": "Dexamethasone",
                "name_ja": "デキサメタゾン",
                "dose": "0.1-0.2 mg/kg IV (doesn't interfere with ACTH test)",
            },
            {
                "name": "Ca gluconate 10%",
                "name_ja": "グルコン酸Ca10%",
                "dose": "0.5-1 mL/kg IV slow (hyperK cardioprotection)",
            },
            {
                "name": "DOCP",
                "name_ja": "デスオキシコルチコステロン",
                "dose": "2.2 mg/kg IM q25d (long-term mineralocorticoid)",
            },
            {
                "name": "Fludrocortisone",
                "name_ja": "フルドロコルチゾン",
                "dose": "0.02 mg/kg PO q12h (alternative to DOCP)",
            },
        ],
        "monitoring": [
            "Serum electrolytes (Na+, K+, Na:K ratio) q6-12h",
            "Blood pressure",
            "ECG",
            "BUN/Cr",
            "Cortisol (ACTH stim)",
        ],
        "ref": "Klein & Peterson 2010 JVIM; ACVIM Endocrine 2019",
    },
    # ============================================================
    # Dystocia
    # ============================================================
    {
        "id": "dystocia",
        "category": "trauma",
        "title_ja": "難産（犬・猫）",
        "title_en": "Dystocia (Dog / Cat)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": [
            "強い陣痛30分以上で胎児排出なし",
            "緑色分泌物（胎盤剥離）で分娩なし",
            "陣痛停止>2時間",
            "全身状態悪化",
            "異常胎位触知",
        ],
        "trigger_signs_en": [
            ">30min strong contractions without delivery",
            "Green discharge (placental separation) without delivery",
            "No labor >2h between pups",
            "Deteriorating condition",
            "Abnormal fetal presentation",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Medical trial",
                "ja": "子宮無力症: オキシトシン 0.5-2 IU IV/IM（最大3回、20分間隔）。Ca gluconate 10% 0.5-1 mL/kg IV slow（子宮収縮力増強）。",
                "en": "Uterine inertia: Oxytocin 0.5-2 IU IV/IM (max 3 doses, 20min apart). Ca gluconate 10% 0.5-1 mL/kg IV slow (augment contraction).",
                "time_target": "0-60分",
            },
            {
                "order": 2,
                "phase": "Assess response",
                "ja": "20-30分で胎児排出なし → 帝王切開。⚠閉塞性難産はオキシトシン禁忌（子宮破裂）。",
                "en": "No delivery within 20-30min → C-section. ⚠ Obstructive dystocia = oxytocin contraindicated (uterine rupture).",
                "time_target": "30分後",
            },
            {
                "order": 3,
                "phase": "C-section",
                "ja": "全身麻酔（プロポフォール導入→イソフルラン）。⚠α2/高用量オピオイドは新生児抑制。胎児取り出し後に子宮を体外に出してから閉鎖。",
                "en": "GA (propofol induction → isoflurane). ⚠ Avoid α2/high-dose opioids (neonatal depression). Exteriorize uterus, extract pups, then close.",
                "time_target": "決断後即時",
            },
            {
                "order": 4,
                "phase": "Neonatal resuscitation",
                "ja": "胎膜除去→鼻腔吸引→擦拭（タオルで刺激）→2-3回振り→ドキサプラム1-2滴舌下（最終手段）。",
                "en": "Remove membranes → suction nose → rub vigorously (towel stimulation) → gentle swing 2-3x → doxapram 1-2 drops sublingual (last resort).",
                "time_target": "取り出し後30秒以内",
            },
            {
                "order": 5,
                "phase": "Post-op dam",
                "ja": "オキシトシン 0.5-2 IU IM（子宮内容排出）。抗菌薬。メロキシカム0.1 mg/kg（授乳への影響最小）。",
                "en": "Oxytocin 0.5-2 IU IM (uterine involution). Antibiotics. Meloxicam 0.1 mg/kg (minimal lactation impact).",
                "time_target": "術後",
            },
        ],
        "key_drugs": [
            {
                "name": "Oxytocin",
                "name_ja": "オキシトシン",
                "dose": "0.5-2 IU IV/IM q20min (max 3 doses; NOT for obstructive)",
            },
            {
                "name": "Ca gluconate 10%",
                "name_ja": "グルコン酸Ca 10%",
                "dose": "0.5-1 mL/kg IV slow (augment contractions)",
            },
            {"name": "Propofol", "name_ja": "プロポフォール", "dose": "4-6 mg/kg IV (induction for C-section)"},
            {
                "name": "Doxapram",
                "name_ja": "ドキサプラム",
                "dose": "1-2 drops sublingual to neonates (respiratory stimulant)",
            },
        ],
        "monitoring": [
            "Fetal heart rates (US: >180 bpm normal; <150 distress)",
            "Maternal temperature/HR/BP",
            "Time between pups (<2h)",
            "Number of pups delivered vs expected (radiograph)",
        ],
        "ref": "Smith 2007 Theriogenology; Linde-Forsberg 2010 BSAVA Manual of Canine Reproduction",
    },
    # ============================================================
    # Lily Toxicosis (Cat)
    # ============================================================
    {
        "id": "lily_toxicosis_cat",
        "category": "toxicity",
        "title_ja": "猫のユリ中毒（急性腎不全）",
        "title_en": "Lily Toxicosis in Cats (Acute Renal Failure)",
        "species": ["cat"],
        "trigger_signs_ja": ["嘔吐（摂取2-6h後）", "食欲廃絶", "元気消失", "無尿/乏尿（24-72h後）", "ユリ科植物暴露歴"],
        "trigger_signs_en": [
            "Vomiting (2-6h post)",
            "Anorexia",
            "Lethargy",
            "Oliguria/anuria (24-72h)",
            "Lily plant exposure history",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Decontamination",
                "ja": "摂取6h以内: 催吐（デクスメデトミジン0.04 mg/kg IM — 猫でアポモルフィン禁忌）+ 活性炭1-2 g/kg PO。",
                "en": "If <6h: induce emesis (dexmedetomidine 0.04 mg/kg IM — apomorphine unreliable in cats) + activated charcoal 1-2 g/kg PO.",
                "time_target": "6h以内",
            },
            {
                "order": 2,
                "phase": "Aggressive IV fluids",
                "ja": "0.9% NaCl IV 2-3×維持量 ×48h（腎灌流維持が唯一の治療）。⚠遅延（>18h）で予後著しく悪化。",
                "en": "0.9% NaCl IV at 2-3× maintenance ×48h (fluid diuresis is the ONLY treatment). ⚠ Delay >18h dramatically worsens prognosis.",
                "time_target": "即時開始×48h",
            },
            {
                "order": 3,
                "phase": "Monitor renal",
                "ja": "BUN/Cr q12h。尿量 q4h（目標>2 mL/kg/h）。乏尿 → フロセミド2-6 mg/kg IV試行。",
                "en": "BUN/Cr q12h. Urine output q4h (target >2 mL/kg/h). If oliguria → furosemide 2-6 mg/kg IV trial.",
                "time_target": "48-72h",
            },
            {
                "order": 4,
                "phase": "Antiemetic",
                "ja": "マロピタント 1 mg/kg SC/IV q24h + オンダンセトロン 0.5 mg/kg IV q8h。",
                "en": "Maropitant 1 mg/kg SC/IV q24h + Ondansetron 0.5 mg/kg IV q8h.",
                "time_target": "並行",
            },
            {
                "order": 5,
                "phase": "Refractory",
                "ja": "48h以内にanuria → 透析（血液透析 or 腹膜透析）紹介検討。⚠早期治療で予後良好。",
                "en": "If anuria within 48h → refer for dialysis (hemodialysis or peritoneal). ⚠ Early treatment = good prognosis.",
                "time_target": "乏尿持続時",
            },
            {
                "order": 6,
                "phase": "⚠ Which lilies",
                "ja": "全パーツ（花粉含む）が毒性。Lilium属（テッポウユリ、オニユリ等）+ Hemerocallis属（ワスレグサ）。スズラン/カラーは別機序。",
                "en": "ALL parts toxic (including pollen). Lilium spp. + Hemerocallis spp. (daylilies). NOT lily-of-the-valley/calla (different toxins).",
                "time_target": "鑑別",
            },
        ],
        "key_drugs": [
            {"name": "0.9% NaCl", "name_ja": "生理食塩水", "dose": "IV at 2-3× maintenance rate ×48h minimum"},
            {"name": "Furosemide", "name_ja": "フロセミド", "dose": "2-6 mg/kg IV (if oliguria despite fluid loading)"},
            {"name": "Maropitant", "name_ja": "マロピタント", "dose": "1 mg/kg SC/IV q24h"},
            {"name": "Activated charcoal", "name_ja": "活性炭", "dose": "1-2 g/kg PO (if <6h post-ingestion)"},
        ],
        "monitoring": [
            "BUN/Cr q12h ×72h",
            "Urine output q4h (target >2 mL/kg/h)",
            "Electrolytes (K+) q12h",
            "Urinalysis (casts, glucosuria)",
            "Body weight (fluid balance)",
        ],
        "ref": "Bennett & Reineke 2013 JVECCS; Langston 2002 JAVMA",
    },
    # ============================================================
    # Acute Congestive Heart Failure (Pulmonary Edema)
    # ============================================================
    {
        "id": "acute_chf",
        "category": "respiratory",
        "title_ja": "急性うっ血性心不全（肺水腫）",
        "title_en": "Acute Congestive Heart Failure (Pulmonary Edema)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": ["起立呼吸", "湿性ラ音/咳", "頻呼吸", "チアノーゼ", "泡沫状鼻汁（重症）", "既知の心疾患歴"],
        "trigger_signs_en": [
            "Orthopnea",
            "Crackles/cough",
            "Tachypnea",
            "Cyanosis",
            "Foamy nasal discharge (severe)",
            "Known heart disease history",
        ],
        "steps": [
            {
                "order": 1,
                "phase": "Oxygen + minimal stress",
                "ja": "酸素40-60%（ケージ or フローバイ）。⚠猫は最小限のハンドリング（ストレス死のリスク）。",
                "en": "Oxygen 40-60% (cage or flow-by). ⚠ Cats: minimal handling (stress-induced death risk).",
                "time_target": "即時",
            },
            {
                "order": 2,
                "phase": "Furosemide",
                "ja": "犬: フロセミド 2-4 mg/kg IV/IM。猫: 1-2 mg/kg IV/IM。重症: q1h × 3回まで。",
                "en": "Dog: Furosemide 2-4 mg/kg IV/IM. Cat: 1-2 mg/kg IV/IM. Severe: q1h up to 3 doses.",
                "time_target": "即時",
            },
            {
                "order": 3,
                "phase": "Vasodilator (severe)",
                "ja": "重症肺水腫: ニトログリセリン軟膏2%（耳介内側 1/4-1/2インチ q6h）。⚠低血圧に注意。",
                "en": "Severe: Nitroglycerin 2% ointment (1/4-1/2 inch to pinna q6h). ⚠ Watch for hypotension.",
                "time_target": "フロセミド不応時",
            },
            {
                "order": 4,
                "phase": "Pimobendan",
                "ja": "犬: ピモベンダン0.25 mg/kg PO q12h（陽性変力+血管拡張）。猫: 0.1-0.25 mg/kg q12h。",
                "en": "Dog: Pimobendan 0.25 mg/kg PO q12h (inodilator). Cat: 0.1-0.25 mg/kg q12h.",
                "time_target": "経口可能になり次第",
            },
            {
                "order": 5,
                "phase": "Sedation if distressed",
                "ja": "極度の呼吸困難/興奮: ブトルファノール0.2 mg/kg IV/IM（呼吸を楽にし酸素消費↓）。",
                "en": "Severe distress: Butorphanol 0.2 mg/kg IV/IM (reduces anxiety, O2 demand).",
                "time_target": "興奮時",
            },
            {
                "order": 6,
                "phase": "Post-acute",
                "ja": "安定後: 経口フロセミド2 mg/kg PO q12h + ACE阻害薬（ベナゼプリル0.5 mg/kg） + ピモベンダン。胸水あれば穿刺。",
                "en": "After stabilization: oral furosemide 2 mg/kg PO q12h + ACE-I (benazepril 0.5 mg/kg) + pimobendan. Thoracocentesis if pleural effusion.",
                "time_target": "安定後",
            },
            {
                "order": 7,
                "phase": "⚠ Cat-specific",
                "ja": "猫のCHF: 胸水型が多い → 胸腔穿刺が第一処置の場合あり。肥大型心筋症(HCM)の猫にピモベンダンは議論あり。",
                "en": "Cat CHF: often pleural effusion → thoracocentesis may be first priority. Pimobendan in HCM cats is controversial.",
                "time_target": "猫特記",
            },
        ],
        "key_drugs": [
            {
                "name": "Furosemide",
                "name_ja": "フロセミド",
                "dose": "Dog 2-4 mg/kg, Cat 1-2 mg/kg IV/IM (may repeat q1h ×3)",
            },
            {"name": "Pimobendan", "name_ja": "ピモベンダン", "dose": "0.25 mg/kg PO q12h (dog); 0.1-0.25 mg/kg (cat)"},
            {
                "name": "Nitroglycerin 2%",
                "name_ja": "ニトログリセリン2%軟膏",
                "dose": "1/4-1/2 inch to pinna q6h (severe)",
            },
            {"name": "Butorphanol", "name_ja": "ブトルファノール", "dose": "0.2 mg/kg IV/IM (anxiolysis)"},
            {"name": "Benazepril", "name_ja": "ベナゼプリル", "dose": "0.5 mg/kg PO q12-24h (post-acute ACE-I)"},
        ],
        "monitoring": [
            "Respiratory rate (target <40 dog, <60 cat at rest)",
            "SpO2",
            "Thoracic radiography (pulmonary infiltrates)",
            "Blood pressure",
            "Renal values (BUN/Cr) with diuretics",
            "Echocardiography",
        ],
        "ref": "Keene et al. 2019 J Vet Intern Med (ACVIM CHF Consensus); Gordon et al. 2017 JVECCS",
    },
    # =====================================================================
    # 追加緊急シナリオ（v2: 敗血症・マムシ・出血性ショック・ARDS・血栓塞栓）
    # =====================================================================
    {
        "id": "sepsis_septic_shock",
        "category": "shock",
        "title_ja": "敗血症・敗血症性ショック（Sepsis/Septic Shock）",
        "title_en": "Sepsis / Septic Shock — Early Goal-Directed Therapy",
        "species": ["dog", "cat"],
        "trigger_signs_ja": [
            "発熱(>39.5℃)または低体温(<37.0℃、特に猫で予後不良)",
            "頻脈、頻呼吸、CRT延長(>2秒)",
            "意識障害、虚脱、低血圧(MAP<60 mmHg)",
            "感染源の存在(膿胸/腹膜炎/咬傷/UTI/肺炎)",
        ],
        "trigger_signs_en": [
            "Fever (>39.5°C) or hypothermia (<37.0°C, especially cats — poor prognosis)",
            "Tachycardia, tachypnea, prolonged CRT (>2s)",
            "Altered mentation, collapse, hypotension (MAP <60 mmHg)",
            "Identified infection source (pyothorax/peritonitis/bite/UTI/pneumonia)",
        ],
        "steps": [
            {
                "order": 1,
                "time_target": "0-15分",
                "ja": "末梢IVカテーテル確保(可能なら2本)、ベースライン採血(CBC/化学/乳酸/血液ガス)、血液培養2セット採取(抗菌薬投与前)",
                "en": "Place 2 IV catheters, baseline bloodwork (CBC/chem/lactate/blood gas), 2 sets blood cultures (before antibiotics)",
            },
            {
                "order": 2,
                "time_target": "15-60分",
                "ja": "1時間以内に経験的広域抗菌薬投与: アンピシリン-スルバクタム30 mg/kg IV q8h + エンロフロキサシン10 mg/kg IV q24h(犬)/5 mg/kg q24h(猫)。嫌気疑いでメトロニダゾール10 mg/kg IV q12h追加",
                "en": "Empirical broad-spectrum antibiotics within 1h: ampicillin-sulbactam 30 mg/kg IV q8h + enrofloxacin 10 mg/kg IV q24h (dog) / 5 mg/kg q24h (cat). Add metronidazole 10 mg/kg IV q12h if anaerobic suspected",
            },
            {
                "order": 3,
                "time_target": "0-30分",
                "ja": "輸液蘇生: 等張晶質液(LRS/Plasmalyte) 犬30 mL/kg IV、猫10-20 mL/kg IV を15-30分でボーラス。MAP/乳酸/尿量再評価しq15分繰り返し可。猫は急速肺水腫リスクあり総量60 mL/kg/24h目安",
                "en": "Fluid resuscitation: isotonic crystalloid (LRS/Plasmalyte) 30 mL/kg IV dog, 10-20 mL/kg IV cat bolus over 15-30 min. Reassess MAP/lactate/urine output, repeat q15 min. Cats prone to pulmonary edema — target ~60 mL/kg/24h total",
            },
            {
                "order": 4,
                "time_target": "60分以降",
                "ja": "輸液不応性低血圧(MAP<65)に昇圧剤: ノルエピネフリン0.1-1 μg/kg/min IV CRI(第一選択)、追加でバソプレシン0.5-2 mU/kg/min。心筋抑制疑いでドブタミン5-15 μg/kg/min併用",
                "en": "Fluid-refractory hypotension (MAP<65): vasopressors — norepinephrine 0.1-1 μg/kg/min IV CRI (first-line) + vasopressin 0.5-2 mU/kg/min. Add dobutamine 5-15 μg/kg/min if myocardial depression",
            },
            {
                "order": 5,
                "time_target": "24時間以内",
                "ja": "感染源コントロール(腹膜炎の開腹/膿瘍ドレナージ/カテーテル除去)。培養感受性に基づく抗菌薬de-escalation(48-72h)",
                "en": "Source control (laparotomy for peritonitis, abscess drainage, catheter removal). Antibiotic de-escalation based on culture/sensitivity at 48-72h",
            },
        ],
        "key_drugs": [
            {"name": "Ampicillin-sulbactam", "name_ja": "アンピシリン-スルバクタム", "dose": "30 mg/kg IV q8h"},
            {
                "name": "Enrofloxacin",
                "name_ja": "エンロフロキサシン",
                "dose": "10 mg/kg IV q24h (dog) / 5 mg/kg (cat — NEVER higher: retinotoxic)",
            },
            {"name": "Metronidazole", "name_ja": "メトロニダゾール", "dose": "10 mg/kg IV q12h (anaerobic coverage)"},
            {
                "name": "Norepinephrine",
                "name_ja": "ノルエピネフリン",
                "dose": "0.1-1 μg/kg/min IV CRI (vasopressor first-line)",
            },
            {
                "name": "Vasopressin",
                "name_ja": "バソプレシン",
                "dose": "0.5-2 mU/kg/min IV CRI (catecholamine-resistant)",
            },
            {"name": "Dobutamine", "name_ja": "ドブタミン", "dose": "5-15 μg/kg/min IV CRI (myocardial support)"},
            {
                "name": "Hydrocortisone",
                "name_ja": "ヒドロコルチゾン",
                "dose": "1 mg/kg IV q6h (vasopressor-refractory only)",
            },
        ],
        "monitoring": [
            "Lactate (target <2.5 mmol/L, clearance >10%/h)",
            "MAP (target >65 mmHg dog, >60 mmHg cat)",
            "Urine output (>1 mL/kg/h)",
            "CRT, mentation",
            "Body temperature (active warming if hypothermic — slowly)",
            "Glucose (insulin CRI if persistent hyperglycemia)",
            "Coagulation panel (DIC screening)",
        ],
        "ref": "Surviving Sepsis Campaign 2021; Boller & Otto 2009 JVECCS; Silverstein 2014 J Vet Emerg Crit Care",
    },
    {
        "id": "mamushi_envenomation",
        "category": "toxicity",
        "title_ja": "マムシ咬傷（Mamushi Snakebite — 日本特異的）",
        "title_en": "Japanese Mamushi (Pit Viper) Envenomation",
        "species": ["dog", "cat"],
        "trigger_signs_ja": [
            "顔面・前肢の急速腫脹(2-4 cm/h、最頻部位)",
            "局所疼痛、皮下出血、水疱、組織壊死",
            "頻脈、虚脱、ショック(全身性)",
            "VICC: PT/aPTT延長、低フィブリノゲン、血小板減少",
        ],
        "trigger_signs_en": [
            "Rapid facial/forelimb swelling (2-4 cm/h, most common sites)",
            "Local pain, ecchymosis, blistering, tissue necrosis",
            "Tachycardia, collapse, shock (systemic)",
            "VICC: prolonged PT/aPTT, low fibrinogen, thrombocytopenia",
        ],
        "steps": [
            {
                "order": 1,
                "time_target": "0-15分",
                "ja": "禁忌: 止血帯/切開/冷却(組織損傷悪化)。首部咬傷ではカラー除去。IVアクセス即時、0.9% NaCl 60-90 mL/kg/h(犬)で低血圧対応",
                "en": "AVOID tourniquet/incision/ice (worsens damage). Remove collar if neck bite. Establish IV immediately, 0.9% NaCl 60-90 mL/kg/h (dog) for hypotension",
            },
            {
                "order": 2,
                "time_target": "0-30分",
                "ja": "ベースライン採血: CBC/凝固検査/化学/乳酸/CK。腫脹辺縁をマーカーで30分毎にトレース、写真記録",
                "en": "Baseline bloodwork: CBC, coag panel, chemistry, lactate, CK. Mark swelling perimeter q30 min with skin marker, photograph",
            },
            {
                "order": 3,
                "time_target": "6時間以内が最効",
                "ja": "マムシ抗毒素血清(馬由来): 1バイアル(6,000単位)を100-250 mL生食で希釈、30-60分で緩徐IV。前投薬ジフェンヒドラミン2 mg/kg IM 15分前(アナフィラキシー予防)。Grade III-IV(全身性VICC/AKI)なら追加1バイアル",
                "en": "Mamushi antivenin (equine-derived): 1 vial (6,000 U) diluted in 100-250 mL saline, slow IV over 30-60 min. Pre-medicate diphenhydramine 2 mg/kg IM 15 min prior (anaphylaxis prevention). Add 1 more vial if Grade III-IV (systemic VICC/AKI)",
            },
            {
                "order": 4,
                "time_target": "継続",
                "ja": "鎮痛: モルヒネ0.3-0.5 mg/kg IM/SC q4-6h or ブプレノルフィン0.01-0.02 mg/kg IV q6h。AKI予防に強制利尿 0.9% NaCl 4-6 mL/kg/h。活動性出血+低フィブリノゲン<100時にFFP 10-20 mL/kg",
                "en": "Analgesia: morphine 0.3-0.5 mg/kg IM/SC q4-6h or buprenorphine 0.01-0.02 mg/kg IV q6h. Forced diuresis 0.9% NaCl 4-6 mL/kg/h for AKI prevention. FFP 10-20 mL/kg if active hemorrhage AND fibrinogen <100",
            },
            {
                "order": 5,
                "time_target": "24-48時間",
                "ja": "予防的抗菌薬: アモキシシリン-クラブラン酸12.5 mg/kg PO q12h(Pasteurella/口腔内常在菌)。組織壊死は24-48時間後にデブリ。最低24-48時間入院でVICC/AKI/コンパートメント症候群モニタ",
                "en": "Prophylactic antibiotic: amoxicillin-clavulanate 12.5 mg/kg PO q12h (Pasteurella/oral flora). Debride necrotic tissue at 24-48h. Hospitalize ≥24-48h to monitor VICC/AKI/compartment syndrome",
            },
        ],
        "key_drugs": [
            {
                "name": "Mamushi antivenin",
                "name_ja": "マムシ抗毒素血清（馬由来）",
                "dose": "1 vial (6,000 U) IV slow over 30-60 min within 6h of bite",
            },
            {
                "name": "Diphenhydramine",
                "name_ja": "ジフェンヒドラミン",
                "dose": "2 mg/kg IM 15 min prior to antivenin",
            },
            {
                "name": "Dexamethasone",
                "name_ja": "デキサメタゾン",
                "dose": "0.1-0.2 mg/kg IV pre-antivenin (anaphylaxis prophylaxis)",
            },
            {"name": "Morphine", "name_ja": "モルヒネ", "dose": "0.3-0.5 mg/kg IM/SC q4-6h (analgesia)"},
            {"name": "Buprenorphine", "name_ja": "ブプレノルフィン", "dose": "0.01-0.02 mg/kg IV q6h (cat preferred)"},
            {
                "name": "Amoxicillin-clavulanate",
                "name_ja": "アモキシシリン-クラブラン酸",
                "dose": "12.5 mg/kg PO q12h (oral flora prophylaxis)",
            },
        ],
        "monitoring": [
            "Limb circumference q30 min × 4h, then q1-2h",
            "Coagulation (PT/aPTT/fibrinogen) q6-12h",
            "Renal (BUN/Cr/UA) q12h for AKI",
            "Lactate, MAP",
            "ECG (arrhythmias from hyperkalemia/myocardial injury)",
            "CK (rhabdomyolysis severity)",
        ],
        "ref": "Hifumi et al. 2015 J Vet Med Sci; Hoshi et al. 2007 Toxicon; McKinnon Equine Reproduction 2nd ed (envenomation chapter); LeBlanc et al. 2008",
    },
    {
        "id": "hemorrhagic_shock",
        "category": "shock",
        "title_ja": "出血性ショック（HBC・脾破裂・腹腔内出血）",
        "title_en": "Hemorrhagic Shock (Trauma / Splenic Rupture / Hemoabdomen)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": [
            "急性虚脱、頻脈、CRT延長",
            "粘膜蒼白、弱脈",
            "腹部膨満(腹腔内出血)・四肢膨大(血腫)",
            "PCV低下(<25%)、TS<5 g/dL",
            "腹腔穿刺で血性液貯留",
        ],
        "trigger_signs_en": [
            "Acute collapse, tachycardia, prolonged CRT",
            "Pale mucous membranes, weak pulses",
            "Abdominal distention (hemoabdomen) or limb swelling (hematoma)",
            "Decreased PCV (<25%), TS <5 g/dL",
            "Abdominocentesis: bloody fluid",
        ],
        "steps": [
            {
                "order": 1,
                "time_target": "0-10分",
                "ja": "2本のIVカテーテル(>18G)、CBC/化学/凝固/乳酸/PCV+TS/血液型、酸素投与、ECG/BP/SpO2モニタ",
                "en": "Two large-bore IV catheters (>18G), CBC/chem/coag/lactate/PCV+TS/blood type, supplemental oxygen, ECG/BP/SpO2 monitoring",
            },
            {
                "order": 2,
                "time_target": "0-30分",
                "ja": "Hypotensive resuscitation(過度な蘇生を避ける): 等張晶質液10-20 mL/kg IVボーラス、MAP 60-65 mmHgで止め追加止血優先。猫は10 mL/kg/15min。Permissive hypotension戦略",
                "en": "Hypotensive resuscitation (avoid over-resuscitation): isotonic crystalloid 10-20 mL/kg IV bolus, target MAP 60-65 mmHg then stop and prioritize hemostasis. Cats 10 mL/kg/15 min. Permissive hypotension strategy",
            },
            {
                "order": 3,
                "time_target": "15-60分",
                "ja": "輸血適応: PCV<20%, クロスマッチ済全血15-20 mL/kg IV slow(2-4時間)、または濃厚赤血球10-15 mL/kg。低タンパクで新鮮凍結血漿(FFP)10-20 mL/kg追加。トラネキサム酸10 mg/kg IV q6h(止血補助)",
                "en": "Transfusion: PCV <20% — crossmatched whole blood 15-20 mL/kg IV slow (2-4h) or pRBC 10-15 mL/kg. Add FFP 10-20 mL/kg if hypoproteinemic. Tranexamic acid 10 mg/kg IV q6h (antifibrinolytic adjunct)",
            },
            {
                "order": 4,
                "time_target": "源同定",
                "ja": "FAST超音波(腹部/胸部)で出血源同定。脾腫瘤/破裂→緊急開腹脾摘。胸腔内出血→胸腔ドレーン。骨盤骨折→外固定+輸血、開腹後出血再評価",
                "en": "FAST ultrasound (abdomen/thorax) to identify source. Splenic mass/rupture → emergency splenectomy. Hemothorax → chest tube. Pelvic fracture → external coaptation + transfusion, reassess for ongoing hemorrhage",
            },
            {
                "order": 5,
                "time_target": "ICU管理",
                "ja": "輸血後抗凝固防止(ヘパリン使用注意)、術後分時換気・酸素化評価、AKI監視(BUN/Cr/UA)、ARDS発症リスク注意。鎮痛フェンタニルCRI 2-5 μg/kg/h",
                "en": "Post-transfusion: monitor for hyperkalemia/citrate toxicity, post-op ventilation/oxygenation assessment, AKI monitoring (BUN/Cr/UA), watch for ARDS development. Analgesia fentanyl CRI 2-5 μg/kg/h",
            },
        ],
        "key_drugs": [
            {
                "name": "Crystalloid (LRS/Plasmalyte)",
                "name_ja": "等張晶質液",
                "dose": "10-20 mL/kg IV bolus dog, 10 mL/kg cat (hypotensive resuscitation)",
            },
            {"name": "Tranexamic acid", "name_ja": "トラネキサム酸", "dose": "10 mg/kg IV q6h (antifibrinolytic)"},
            {"name": "Fentanyl", "name_ja": "フェンタニル", "dose": "2-5 μg/kg/h IV CRI (analgesia)"},
            {
                "name": "Hetastarch 6%",
                "name_ja": "ヘタスターチ6%",
                "dose": "5-10 mL/kg IV (colloid, dog) — use cautiously",
            },
            {
                "name": "Vitamin K1",
                "name_ja": "ビタミンK1",
                "dose": "1-2 mg/kg SC if anticoagulant rodenticide suspected",
            },
        ],
        "monitoring": [
            "PCV/TS q1-2h initially",
            "Lactate (perfusion marker)",
            "MAP (target 60-65 in active hemorrhage; >70 post-control)",
            "Coagulation (PT/aPTT, fibrinogen)",
            "Urine output (>1 mL/kg/h)",
            "FAST scan q4-6h for re-accumulation",
        ],
        "ref": "Davenport et al. 2017 J Vet Emerg Crit Care (transfusion guidelines); Boller & Otto 2014",
    },
    {
        "id": "ards_pulmonary_thromboembolism",
        "category": "respiratory",
        "title_ja": "ARDS・急性肺血栓塞栓症（Pulmonary Thromboembolism）",
        "title_en": "ARDS / Acute Pulmonary Thromboembolism (PTE)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": [
            "急性重度呼吸困難、頻呼吸(>60/min)、open-mouth breathing",
            "低酸素血症(SpO2<90%、PaO2<60 mmHg)",
            "聴診で正常 or 軽度ラ音(肺野が比較的clean — PTE特徴)",
            "ハイリスク: IMHA/PLN/HAC/腫瘍/長期臥床/最近の手術",
        ],
        "trigger_signs_en": [
            "Acute severe dyspnea, tachypnea (>60/min), open-mouth breathing",
            "Hypoxemia (SpO2 <90%, PaO2 <60 mmHg)",
            "Auscultation often unremarkable or mild crackles (relatively clean lungs — PTE clue)",
            "High-risk: IMHA, PLN, HAC, neoplasia, prolonged recumbency, recent surgery",
        ],
        "steps": [
            {
                "order": 1,
                "time_target": "0-5分",
                "ja": "酸素投与(フェイスマスク/酸素ケージ 40-60% FiO2)、ストレス最小化、IV確保",
                "en": "Oxygen supplementation (face mask / oxygen cage 40-60% FiO2), minimize stress handling, IV access",
            },
            {
                "order": 2,
                "time_target": "5-30分",
                "ja": "胸部X線/エコー(肺水腫除外、心臓肥大/PA拡張評価)、ABG、D-dimer/凝固検査、CBC/化学。CT血管造影が確定診断ゴールドスタンダード(可能なら)",
                "en": "Thoracic radiographs/echo (rule out pulmonary edema, assess cardiomegaly/PA distension), ABG, D-dimer/coag panel, CBC/chem. CT pulmonary angiography is gold standard if available",
            },
            {
                "order": 3,
                "time_target": "30-60分",
                "ja": "抗凝固療法: 未分画ヘパリン100-300 U/kg IV bolus → 200-300 U/kg SC q6h、または低分子ヘパリン(エノキサパリン)1 mg/kg SC q12h。長期管理にリバロキサバン1-2 mg/kg PO q24h(犬)or 1.25 mg/cat PO q24h",
                "en": "Anticoagulation: unfractionated heparin 100-300 U/kg IV bolus → 200-300 U/kg SC q6h, or LMWH (enoxaparin) 1 mg/kg SC q12h. Long-term: rivaroxaban 1-2 mg/kg PO q24h (dog) or 1.25 mg/cat PO q24h",
            },
            {
                "order": 4,
                "time_target": "重症例",
                "ja": "血栓溶解(tPA)5 mg/kg IV over 1h: 大量PTE+心血管虚脱で考慮(高出血リスク、慎重判断)。ARDS時はPEEP人工換気(5-10 cmH2O)、tidal volume 6-8 mL/kg(肺保護)",
                "en": "Thrombolysis (tPA) 5 mg/kg IV over 1h: consider for massive PTE + cardiovascular collapse (high bleeding risk, careful decision). For ARDS: PEEP mechanical ventilation (5-10 cmH2O), tidal volume 6-8 mL/kg (lung-protective)",
            },
            {
                "order": 5,
                "time_target": "基礎疾患治療",
                "ja": "原疾患特定・治療(IMHA→ステロイド、PLN→ACEi/ARB、腫瘍→化療検討)。再発予防のため抗血小板薬(クロピドグレル1-2 mg/kg PO q24h)併用",
                "en": "Identify and treat underlying cause (IMHA → steroids, PLN → ACEi/ARB, neoplasia → chemo). Antiplatelet (clopidogrel 1-2 mg/kg PO q24h) for recurrence prevention",
            },
        ],
        "key_drugs": [
            {
                "name": "Unfractionated heparin",
                "name_ja": "未分画ヘパリン",
                "dose": "100-300 U/kg IV bolus → 200-300 U/kg SC q6h",
            },
            {"name": "Enoxaparin (LMWH)", "name_ja": "エノキサパリン(低分子ヘパリン)", "dose": "1 mg/kg SC q12h"},
            {"name": "Rivaroxaban", "name_ja": "リバロキサバン", "dose": "1-2 mg/kg PO q24h dog; 1.25 mg/cat PO q24h"},
            {"name": "Clopidogrel", "name_ja": "クロピドグレル", "dose": "1-2 mg/kg PO q24h (antiplatelet)"},
            {
                "name": "tPA (alteplase)",
                "name_ja": "tPA(アルテプラーゼ)",
                "dose": "5 mg/kg IV over 1h (severe PTE only)",
            },
            {"name": "Furosemide", "name_ja": "フロセミド", "dose": "1-2 mg/kg IV q4-6h if pulmonary edema component"},
        ],
        "monitoring": [
            "SpO2, ABG q2-4h",
            "Respiratory rate, effort",
            "Coagulation: aPTT for unfractionated heparin (target 1.5-2× baseline)",
            "Anti-Xa for LMWH (target 0.5-1.0 U/mL)",
            "PCV/TS (bleeding risk on anticoagulants)",
            "Repeat echo if hemodynamic compromise",
        ],
        "ref": "deLaforcade et al. 2019 J Vet Emerg Crit Care (CURATIVE guidelines); Dixon-Jimenez et al. 2013",
    },
    {
        "id": "postpartum_eclampsia",
        "category": "metabolic",
        "title_ja": "産後子癇（Eclampsia / Puerperal Tetany — 低Ca血症）",
        "title_en": "Postpartum Eclampsia (Puerperal Tetany / Hypocalcemia)",
        "species": ["dog", "cat"],
        "trigger_signs_ja": [
            "産後1-4週(授乳期ピーク)に発症",
            "落ち着きなく、振戦、強直性痙攣、高体温(40-42℃)",
            "顔面掻痒、流涎、運動失調",
            "進行性: 全身性強直間代発作、昏睡",
            "イオン化Ca<0.8 mmol/L(<3.2 mg/dL)",
        ],
        "trigger_signs_en": [
            "Onset 1-4 weeks postpartum (peak lactation)",
            "Restlessness, tremors, tonic muscle spasms, hyperthermia (40-42°C)",
            "Facial pruritus, hypersalivation, ataxia",
            "Progressive: generalized tonic-clonic seizures, coma",
            "Ionized Ca <0.8 mmol/L (<3.2 mg/dL)",
        ],
        "steps": [
            {
                "order": 1,
                "time_target": "0-5分",
                "ja": "IV確保、ベースライン採血(イオン化Ca, Mg, P, 血糖, CBC/化学)。ECGモニタ装着(心臓毒性確認用)",
                "en": "IV access, baseline bloodwork (ionized Ca, Mg, P, glucose, CBC/chem). ECG monitoring (cardiac toxicity assessment)",
            },
            {
                "order": 2,
                "time_target": "5-30分",
                "ja": "カルシウムグルコネート10%を生食で1:1希釈、0.5-1.5 mL/kg(50-150 mg/kg) IV slow over 10-30分。ECG連続モニタ — 徐脈/QT短縮で投与中止(10-15分待機後再開可)",
                "en": "Calcium gluconate 10% diluted 1:1 with saline, 0.5-1.5 mL/kg (50-150 mg/kg) IV slow over 10-30 min. Continuous ECG — STOP if bradycardia/QT shortening (wait 10-15 min, may resume)",
            },
            {
                "order": 3,
                "time_target": "急性期後",
                "ja": "高体温対応: 体表冷却(冷水浴/扇風機/IV低温輸液)、目標38.5-39.5℃。低血糖併発時は50%ブドウ糖0.5-1 mL/kg slow IV",
                "en": "Hyperthermia management: surface cooling (cool water bath/fan/cool IV fluids), target 38.5-39.5°C. If concurrent hypoglycemia: 50% dextrose 0.5-1 mL/kg slow IV",
            },
            {
                "order": 4,
                "time_target": "重要",
                "ja": "子犬/子猫を授乳から完全離乳(母乳禁止) — 再発を防ぐ。人工哺乳に切り替え。母獣にカルシウム経口維持: グルコン酸Ca 25-50 mg/kg PO q8h、ビタミンD3 10-20 IU/kg q24h",
                "en": "FULLY WEAN puppies/kittens (no nursing) — prevents recurrence. Switch to bottle feeding. Maternal oral calcium maintenance: calcium gluconate 25-50 mg/kg PO q8h, vitamin D3 10-20 IU/kg q24h",
            },
            {
                "order": 5,
                "time_target": "24-48時間モニタ",
                "ja": "イオン化Ca q4-6h再検査(目標>1.0 mmol/L)。痙攣再発でカルシウム再投与。次回妊娠で予防的Ca補充を妊娠後期から授乳期に継続。次妊娠は1-2年空ける",
                "en": "Recheck ionized Ca q4-6h (target >1.0 mmol/L). Recurrent seizures → repeat calcium dose. For future pregnancies: prophylactic Ca supplementation from late gestation through lactation. Space pregnancies 1-2 years apart",
            },
        ],
        "key_drugs": [
            {
                "name": "Calcium gluconate 10%",
                "name_ja": "グルコン酸Ca 10%",
                "dose": "0.5-1.5 mL/kg IV slow over 10-30 min (DILUTE 1:1 with saline)",
            },
            {
                "name": "Calcium gluconate (oral)",
                "name_ja": "グルコン酸Ca（経口）",
                "dose": "25-50 mg/kg PO q8h maintenance",
            },
            {
                "name": "Vitamin D3 (cholecalciferol)",
                "name_ja": "ビタミンD3(コレカルシフェロール)",
                "dose": "10-20 IU/kg PO q24h",
            },
            {
                "name": "Diazepam",
                "name_ja": "ジアゼパム",
                "dose": "0.5 mg/kg IV bolus for breakthrough seizures (after Ca correction)",
            },
            {
                "name": "50% Dextrose",
                "name_ja": "50%ブドウ糖",
                "dose": "0.5-1 mL/kg slow IV if concurrent hypoglycemia",
            },
        ],
        "monitoring": [
            "Ionized calcium q4-6h until stable",
            "Continuous ECG during Ca infusion",
            "Body temperature (avoid <37°C from overcooling)",
            "Glucose (concurrent hypoglycemia common)",
            "Magnesium (if Mg low, Ca correction may fail)",
            "Mentation, seizure activity",
        ],
        "ref": "Drobatz & Casey 2000 JAVMA; Wehrend et al. 2015; Aroch et al. 1999 J Vet Med",
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
