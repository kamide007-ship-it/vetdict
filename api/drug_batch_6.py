"""Drug batch 6 – Emergency, cardiovascular & miscellaneous drugs.

References:
  - Plumb's Veterinary Drug Handbook, 10th ed.
  - BSAVA Small Animal Formulary, 10th ed.
  - Carpenter's Exotic Animal Formulary, 6th ed.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# New drugs (not in main dictionary or batches 1-5)
# ---------------------------------------------------------------------------
DRUGS_BATCH_6: list[dict] = [
    # ------------------------------------------------------------------
    # Epinephrine – emergency
    # ------------------------------------------------------------------
    {
        "id": "epinephrine",
        "name": "Epinephrine (Adrenaline)",
        "name_ja": "エピネフリン（アドレナリン）",
        "category": "cardiovascular",
        "mechanism": "Non-selective adrenergic agonist (α1, α2, β1, β2). Increases heart rate, contractility, and systemic vascular resistance. Bronchodilation via β2. First-line for cardiac arrest and anaphylaxis.",
        "mechanism_ja": "非選択的アドレナリン作動薬（α1, α2, β1, β2）。心拍数・収縮力・全身血管抵抗を増加。β2による気管支拡張。心停止・アナフィラキシーの第一選択薬。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Cardiac arrest: 0.01-0.02 mg/kg IV/IO q3-5min; Anaphylaxis: 0.01 mg/kg IM",
                "dosage_ja": "心停止: 0.01-0.02 mg/kg 静注/骨髄内 3-5分毎；アナフィラキシー: 0.01 mg/kg 筋注",
                "notes": "Use 1:10,000 dilution IV for arrest; 1:1,000 IM for anaphylaxis. Monitor ECG",
                "notes_ja": "心停止には1:10,000希釈を静注、アナフィラキシーには1:1,000を筋注。ECGモニター",
            },
            "cat": {
                "safe": True,
                "dosage": "Cardiac arrest: 0.01-0.02 mg/kg IV/IO q3-5min; Anaphylaxis: 0.01 mg/kg IM",
                "dosage_ja": "心停止: 0.01-0.02 mg/kg 静注/骨髄内 3-5分毎；アナフィラキシー: 0.01 mg/kg 筋注",
                "notes": "Same protocol as dogs; cats more sensitive to tachyarrhythmias",
                "notes_ja": "犬と同じプロトコル。猫は頻脈性不整脈に敏感",
            },
            "horse": {
                "safe": True,
                "dosage": "Anaphylaxis: 3-5 mL of 1:1,000 IV/IM (adult horse)",
                "dosage_ja": "アナフィラキシー: 1:1,000を3-5 mL 静注/筋注（成馬）",
                "notes": "For anaphylaxis and cardiac arrest; titrate carefully",
                "notes_ja": "アナフィラキシー・心停止に。慎重に投与量調整",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.01 mg/kg IV/IO/IT",
                "dosage_ja": "0.01 mg/kg 静注/骨髄内/気管内",
                "notes": "Emergency use for cardiac arrest or severe anaphylaxis",
                "notes_ja": "心停止・重度アナフィラキシーの救急使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.02 mg/kg IV/IO/IM",
                "dosage_ja": "0.02 mg/kg 静注/骨髄内/筋注",
                "notes": "Emergency resuscitation",
                "notes_ja": "救急蘇生",
            },
            "bird": {
                "safe": True,
                "dosage": "0.01-0.1 mg/kg IV/IM/IO",
                "dosage_ja": "0.01-0.1 mg/kg 静注/筋注/骨髄内",
                "notes": "For cardiac arrest in birds; IO route preferred if IV not available",
                "notes_ja": "鳥の心停止に。静脈確保困難時は骨髄内経路",
            },
        },
        "side_effects": ["tachycardia", "arrhythmias", "hypertension", "tremors", "tissue necrosis (perivascular)"],
        "side_effects_ja": ["頻脈", "不整脈", "高血圧", "振戦", "血管外漏出時の組織壊死"],
        "contraindications": "Halothane anesthesia (arrhythmia risk). Use with extreme caution in patients with pre-existing tachyarrhythmias.",
        "contraindications_ja": "ハロタン麻酔下（不整脈リスク）。既存の頻脈性不整脈には極めて慎重に使用。",
    },
    # ------------------------------------------------------------------
    # Vasopressin – emergency
    # ------------------------------------------------------------------
    {
        "id": "vasopressin",
        "name": "Vasopressin (ADH/Pitressin)",
        "name_ja": "バソプレシン（抗利尿ホルモン）",
        "category": "cardiovascular",
        "mechanism": "V1 receptor agonist causing peripheral vasoconstriction independent of adrenergic receptors. Used as alternative/adjunct to epinephrine in CPR. Also V2 agonist (antidiuretic effect).",
        "mechanism_ja": "V1受容体作動薬でアドレナリン受容体非依存性に末梢血管収縮。CPRでエピネフリンの代替/補助。V2作動薬としての抗利尿作用も。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Cardiac arrest: 0.8 U/kg IV once; CRI: 0.5-5 mU/kg/min for vasodilatory shock",
                "dosage_ja": "心停止: 0.8 U/kg 静注 1回；持続: 0.5-5 mU/kg/分 血管拡張性ショックに",
                "notes": "Alternative to epinephrine in refractory arrest. Does not increase myocardial O2 demand as much as epinephrine",
                "notes_ja": "難治性心停止でエピネフリンの代替。エピネフリンほど心筋酸素需要を増加させない",
            },
            "cat": {
                "safe": True,
                "dosage": "Cardiac arrest: 0.8 U/kg IV once",
                "dosage_ja": "心停止: 0.8 U/kg 静注 1回",
                "notes": "Limited feline data; extrapolated from canine protocols",
                "notes_ja": "猫のデータは限定的。犬のプロトコルから外挿",
            },
            "horse": {
                "safe": True,
                "dosage": "0.25-0.5 U/kg IV (resuscitation)",
                "dosage_ja": "0.25-0.5 U/kg 静注（蘇生）",
                "notes": "For refractory hypotension; monitor for excessive vasoconstriction",
                "notes_ja": "難治性低血圧に。過度の血管収縮に注意",
            },
        },
        "side_effects": ["peripheral vasoconstriction", "tissue ischemia", "hypertension", "bradycardia", "GI cramping"],
        "side_effects_ja": ["末梢血管収縮", "組織虚血", "高血圧", "徐脈", "消化管攣縮"],
        "contraindications": "Chronic nephritis with nitrogen retention. Ischemic heart disease (relative).",
        "contraindications_ja": "窒素貯留を伴う慢性腎炎。虚血性心疾患（相対的禁忌）。",
    },
    # ------------------------------------------------------------------
    # Dopamine – emergency vasopressor
    # ------------------------------------------------------------------
    {
        "id": "dopamine",
        "name": "Dopamine",
        "name_ja": "ドパミン",
        "category": "cardiovascular",
        "mechanism": "Dose-dependent effects: low dose (1-3 µg/kg/min) = dopaminergic (renal/splanchnic vasodilation); medium (3-10) = β1 (increased contractility/HR); high (>10) = α1 (vasoconstriction). Endogenous catecholamine precursor.",
        "mechanism_ja": "用量依存的作用：低用量(1-3 µg/kg/分)=ドパミン作動性(腎/内臓血管拡張)；中用量(3-10)=β1(収縮力/心拍数増加)；高用量(>10)=α1(血管収縮)。内因性カテコラミン前駆体。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-10 µg/kg/min IV CRI (titrate to effect)",
                "dosage_ja": "2-10 µg/kg/分 静注持続（効果に応じて調整）",
                "notes": "Requires ECG and BP monitoring. Use central line if possible. Inactivated by alkaline solutions",
                "notes_ja": "ECGと血圧モニタリング必要。可能なら中心静脈から。アルカリ溶液で失活",
            },
            "cat": {
                "safe": True,
                "dosage": "2-10 µg/kg/min IV CRI",
                "dosage_ja": "2-10 µg/kg/分 静注持続",
                "notes": "Same dosing as dogs; cats may be more sensitive to arrhythmias",
                "notes_ja": "犬と同用量。猫は不整脈に敏感な場合あり",
            },
            "horse": {
                "safe": True,
                "dosage": "3-10 µg/kg/min IV CRI",
                "dosage_ja": "3-10 µg/kg/分 静注持続",
                "notes": "For neonatal foal hypotension/sepsis; monitor closely",
                "notes_ja": "新生子馬の低血圧/敗血症に。厳密にモニター",
            },
            "ferret": {
                "safe": True,
                "dosage": "2-10 µg/kg/min IV CRI",
                "dosage_ja": "2-10 µg/kg/分 静注持続",
                "notes": "Emergency vasopressor support",
                "notes_ja": "救急時の昇圧サポート",
            },
        },
        "side_effects": ["tachycardia", "arrhythmias", "hypertension", "tissue necrosis (extravasation)", "nausea"],
        "side_effects_ja": ["頻脈", "不整脈", "高血圧", "血管外漏出時の組織壊死", "嘔気"],
        "contraindications": "Pheochromocytoma. Uncorrected tachyarrhythmia. Do not mix with alkaline IV solutions.",
        "contraindications_ja": "褐色細胞腫。未是正の頻脈性不整脈。アルカリ性輸液と混合不可。",
    },
    # ------------------------------------------------------------------
    # Dobutamine – emergency inotrope
    # ------------------------------------------------------------------
    {
        "id": "dobutamine",
        "name": "Dobutamine",
        "name_ja": "ドブタミン",
        "category": "cardiovascular",
        "mechanism": "Synthetic catecholamine; primarily β1 agonist with some β2 and α1 activity. Increases myocardial contractility with less chronotropic and vasoconstrictive effect than dopamine.",
        "mechanism_ja": "合成カテコラミン。主にβ1作動薬でβ2・α1活性も一部あり。ドパミンより心拍数増加・血管収縮作用が少なく心筋収縮力を増加。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-20 µg/kg/min IV CRI (start low, titrate up)",
                "dosage_ja": "2-20 µg/kg/分 静注持続（低用量開始、漸増）",
                "notes": "Preferred over dopamine for cardiogenic shock/CHF decompensation. Short half-life (2 min)",
                "notes_ja": "心原性ショック/CHF急性増悪にはドパミンより推奨。半減期が短い（2分）",
            },
            "cat": {
                "safe": True,
                "dosage": "2-10 µg/kg/min IV CRI",
                "dosage_ja": "2-10 µg/kg/分 静注持続",
                "notes": "Cats more sensitive; use lower doses. Risk of seizures at higher doses",
                "notes_ja": "猫は感受性が高い。低用量を使用。高用量で痙攣リスク",
            },
            "horse": {
                "safe": True,
                "dosage": "1-10 µg/kg/min IV CRI",
                "dosage_ja": "1-10 µg/kg/分 静注持続",
                "notes": "For neonatal foals with septic shock; monitor cardiac output",
                "notes_ja": "敗血症性ショックの新生子馬に。心拍出量をモニター",
            },
            "ferret": {
                "safe": True,
                "dosage": "5-10 µg/kg/min IV CRI",
                "dosage_ja": "5-10 µg/kg/分 静注持続",
                "notes": "For acute heart failure; limited data",
                "notes_ja": "急性心不全に。データ限定的",
            },
        },
        "side_effects": ["tachycardia", "arrhythmias", "hypertension", "seizures (cats, high dose)"],
        "side_effects_ja": ["頻脈", "不整脈", "高血圧", "痙攣（猫、高用量）"],
        "contraindications": "Hypertrophic cardiomyopathy (HCM) with outflow tract obstruction. Ventricular tachycardia.",
        "contraindications_ja": "流出路閉塞を伴う肥大型心筋症（HCM）。心室頻拍。",
    },
]

# ---------------------------------------------------------------------------
# Species-specific dosage patches for existing drugs (batch 6)
# ---------------------------------------------------------------------------
SPECIES_INFO_PATCH_6: dict[str, dict[str, dict]] = {}
