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
    # ------------------------------------------------------------------
    # Theophylline – bronchodilator
    # ------------------------------------------------------------------
    {
        "id": "theophylline",
        "name": "Theophylline (Theo-Dur)",
        "name_ja": "テオフィリン（テオドール）",
        "category": "bronchodilators",
        "mechanism": "Methylxanthine; inhibits phosphodiesterase, increases cAMP. Bronchodilation, mild diuresis, positive chronotrope/inotrope, respiratory stimulant. Narrow therapeutic index.",
        "mechanism_ja": "メチルキサンチン系。ホスホジエステラーゼ阻害でcAMP増加。気管支拡張、軽度利尿、陽性変時/変力作用、呼吸促進。治療域が狭い。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "SR: 10 mg/kg PO q12h; IR: 5-8 mg/kg PO q6-8h",
                "dosage_ja": "徐放: 10 mg/kg 経口 12時間毎；速放: 5-8 mg/kg 経口 6-8時間毎",
                "notes": "Monitor serum levels (10-20 µg/mL). For chronic bronchitis, collapsing trachea",
                "notes_ja": "血中濃度モニター（10-20 µg/mL）。慢性気管支炎・気管虚脱に",
            },
            "cat": {
                "safe": True,
                "dosage": "SR: 10-15 mg/kg PO q24h evening; IR: 4 mg/kg PO q8-12h",
                "dosage_ja": "徐放: 10-15 mg/kg 経口 24時間毎 夕方；速放: 4 mg/kg 経口 8-12時間毎",
                "notes": "Cats metabolize more slowly; once daily SR may suffice. For feline asthma",
                "notes_ja": "猫は代謝が遅い。1日1回徐放で十分な場合あり。猫喘息に",
            },
            "horse": {
                "safe": True,
                "dosage": "5-15 mg/kg PO q12h",
                "dosage_ja": "5-15 mg/kg 経口 12時間毎",
                "notes": "For recurrent airway obstruction (RAO/heaves); variable oral bioavailability",
                "notes_ja": "反復性気道閉塞（RAO/喘鳴）に。経口バイオアベイラビリティにばらつき",
            },
            "ferret": {
                "safe": True,
                "dosage": "4 mg/kg PO q8-12h",
                "dosage_ja": "4 mg/kg 経口 8-12時間毎",
                "notes": "For bronchospasm; limited data",
                "notes_ja": "気管支攣縮に。データ限定的",
            },
        },
        "side_effects": ["tachycardia", "restlessness", "GI upset", "seizures (toxic levels)", "arrhythmias"],
        "side_effects_ja": ["頻脈", "不穏", "消化器症状", "痙攣（中毒域）", "不整脈"],
        "contraindications": "Active seizure disorder. Severe cardiac arrhythmias. Narrow therapeutic index: monitor levels.",
        "contraindications_ja": "活動性てんかん。重度の心不整脈。治療域が狭い：血中濃度モニター必須。",
    },
    # ------------------------------------------------------------------
    # Lomustine (CCNU) – antineoplastic
    # ------------------------------------------------------------------
    {
        "id": "lomustine",
        "name": "Lomustine (CCNU/CeeNU)",
        "name_ja": "ロムスチン（CCNU）",
        "category": "antineoplastics",
        "mechanism": "Alkylating nitrosourea agent. Crosses BBB. Cell-cycle non-specific. Used for CNS tumors, mast cell tumors, lymphoma, and histiocytic sarcoma in veterinary oncology.",
        "mechanism_ja": "アルキル化ニトロソウレア系薬剤。血液脳関門を通過。細胞周期非特異的。獣医腫瘍学でCNS腫瘍、肥満細胞腫、リンパ腫、組織球性肉腫に使用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "60-90 mg/m² PO once q3-6 weeks",
                "dosage_ja": "60-90 mg/m² 経口 3-6週毎に1回",
                "notes": "Cumulative hepatotoxicity; check ALT before each dose. Myelosuppression nadir at 7 days (thrombocytopenia) and 14-21 days (neutropenia). CBC weekly",
                "notes_ja": "累積性肝毒性あり。各投与前にALT確認。骨髄抑制の最低値は7日目（血小板減少）と14-21日目（好中球減少）。毎週CBC",
            },
            "cat": {
                "safe": True,
                "dosage": "50-60 mg/m² PO q3-6 weeks",
                "dosage_ja": "50-60 mg/m² 経口 3-6週毎",
                "notes": "More sensitive to myelosuppression; use lower doses. For lymphoma, mast cell tumors",
                "notes_ja": "骨髄抑制に敏感。低用量を使用。リンパ腫・肥満細胞腫に",
            },
            "ferret": {
                "safe": True,
                "dosage": "50 mg/m² PO q3 weeks",
                "dosage_ja": "50 mg/m² 経口 3週毎",
                "notes": "For lymphoma; monitor CBC and liver values closely",
                "notes_ja": "リンパ腫に。CBC・肝機能を厳密にモニター",
            },
        },
        "side_effects": ["myelosuppression (cumulative)", "hepatotoxicity (cumulative, dose-limiting)", "GI upset", "anorexia"],
        "side_effects_ja": ["骨髄抑制（累積性）", "肝毒性（累積性、用量制限因子）", "消化器症状", "食欲不振"],
        "contraindications": "Pre-existing hepatic disease (ALT >3x ULN). Severe myelosuppression. Do not handle with bare hands (cytotoxic).",
        "contraindications_ja": "既存の肝疾患（ALT >正常上限3倍）。重度の骨髄抑制。素手で取り扱わないこと（細胞毒性）。",
    },
    # ------------------------------------------------------------------
    # Leflunomide – immunosuppressive
    # ------------------------------------------------------------------
    {
        "id": "leflunomide",
        "name": "Leflunomide (Arava)",
        "name_ja": "レフルノミド（アラバ）",
        "category": "immunosuppressives",
        "mechanism": "Isoxazole derivative; inhibits dihydroorotate dehydrogenase (DHODH), blocking de novo pyrimidine synthesis. Immunomodulatory; suppresses T and B lymphocyte proliferation.",
        "mechanism_ja": "イソオキサゾール誘導体。ジヒドロオロト酸脱水素酵素（DHODH）を阻害しピリミジンのde novo合成を遮断。T・Bリンパ球増殖を抑制する免疫調節薬。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-4 mg/kg PO q24h (loading: 4 mg/kg x3d, then 2 mg/kg maintenance)",
                "dosage_ja": "2-4 mg/kg 経口 24時間毎（負荷: 4 mg/kg×3日後、維持2 mg/kg）",
                "notes": "For IMHA, IMTP, immune-mediated polyarthritis, vasculitis. Monitor CBC and liver enzymes q2 weeks initially. Therapeutic drug monitoring available (teriflunomide level 20-40 µg/mL)",
                "notes_ja": "IMHA、IMTP、免疫介在性多発関節炎、血管炎に。初期は2週毎にCBC・肝酵素モニター。TDM可能（テリフルノミド値 20-40 µg/mL）",
            },
            "cat": {
                "safe": True,
                "dosage": "10 mg/cat PO q24-48h",
                "dosage_ja": "10 mg/匹 経口 24-48時間毎",
                "notes": "For FIP (dry form), immune-mediated disease. Less data in cats than dogs",
                "notes_ja": "FIP（ドライ型）、免疫介在性疾患に。猫のデータは犬より少ない",
            },
        },
        "side_effects": ["GI upset", "hepatotoxicity", "myelosuppression", "weight loss"],
        "side_effects_ja": ["消化器症状", "肝毒性", "骨髄抑制", "体重減少"],
        "contraindications": "Pregnancy (teratogenic). Severe hepatic disease. Concurrent other immunosuppressives may increase toxicity.",
        "contraindications_ja": "妊娠（催奇形性）。重度の肝疾患。他の免疫抑制薬併用で毒性増加の可能性。",
    },
    # ------------------------------------------------------------------
    # Nitenpyram – fast-acting flea killer
    # ------------------------------------------------------------------
    {
        "id": "nitenpyram",
        "name": "Nitenpyram (Capstar)",
        "name_ja": "ニテンピラム（キャプスター）",
        "category": "antiparasitics",
        "mechanism": "Neonicotinoid insecticide; nicotinic acetylcholine receptor agonist in insect neurons. Rapid oral flea kill (begins within 30 min). No residual activity (24h duration).",
        "mechanism_ja": "ネオニコチノイド系殺虫薬。昆虫ニューロンのニコチン性アセチルコリン受容体作動薬。経口投与で速やかにノミ駆除（30分以内に効果発現）。残効性なし（24時間持続）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1 mg/kg PO once (can repeat daily if needed)",
                "dosage_ja": "1 mg/kg 経口 1回（必要時毎日繰返し可）",
                "notes": "For rapid flea knockdown; no residual. Safe for puppies ≥4 weeks and ≥0.9 kg",
                "notes_ja": "ノミの速効駆除に。残効なし。4週以上・0.9kg以上の子犬に安全",
            },
            "cat": {
                "safe": True,
                "dosage": "1 mg/kg PO once (can repeat daily)",
                "dosage_ja": "1 mg/kg 経口 1回（毎日繰返し可）",
                "notes": "Safe for kittens ≥4 weeks and ≥0.9 kg. Combine with long-acting product for sustained control",
                "notes_ja": "4週以上・0.9kg以上の子猫に安全。持続制御には長時間作用製品と併用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1 mg/kg PO once",
                "dosage_ja": "1 mg/kg 経口 1回",
                "notes": "Off-label; safe and effective for rapid flea removal in rabbits",
                "notes_ja": "適応外。ウサギのノミ速効駆除に安全かつ有効",
            },
            "ferret": {
                "safe": True,
                "dosage": "1 mg/kg PO once",
                "dosage_ja": "1 mg/kg 経口 1回",
                "notes": "Off-label use; well-tolerated",
                "notes_ja": "適応外使用。忍容性良好",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "1 mg/kg PO once",
                "dosage_ja": "1 mg/kg 経口 1回",
                "notes": "Off-label; anecdotal safety in guinea pigs",
                "notes_ja": "適応外。モルモットでの経験的安全性",
            },
        },
        "side_effects": ["transient hyperexcitability (flea biting sensation)", "itching", "rare GI upset"],
        "side_effects_ja": ["一過性の過興奮（ノミの咬傷感覚）", "掻痒", "稀に消化器症状"],
        "contraindications": "Puppies/kittens <4 weeks or <0.9 kg.",
        "contraindications_ja": "4週齢未満または0.9kg未満の子犬/子猫。",
    },
    # ------------------------------------------------------------------
    # Tadalafil – PDE5 inhibitor (pulmonary hypertension)
    # ------------------------------------------------------------------
    {
        "id": "tadalafil",
        "name": "Tadalafil (Cialis)",
        "name_ja": "タダラフィル（シアリス）",
        "category": "cardiovascular",
        "mechanism": "Phosphodiesterase-5 (PDE5) inhibitor. Increases cGMP in pulmonary vascular smooth muscle, causing vasodilation. Longer half-life than sildenafil (17.5h vs 4h in dogs).",
        "mechanism_ja": "ホスホジエステラーゼ5（PDE5）阻害薬。肺血管平滑筋のcGMPを増加させ血管拡張。シルデナフィルより長い半減期（犬で17.5時間 vs 4時間）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q24h",
                "dosage_ja": "1-2 mg/kg 経口 24時間毎",
                "notes": "For pulmonary hypertension; once-daily alternative to sildenafil. May have better compliance",
                "notes_ja": "肺高血圧症に。シルデナフィルの1日1回代替薬。コンプライアンス向上の可能性",
            },
            "cat": {
                "safe": True,
                "dosage": "1 mg/kg PO q24h",
                "dosage_ja": "1 mg/kg 経口 24時間毎",
                "notes": "Limited feline data; extrapolated from canine. For pulmonary hypertension",
                "notes_ja": "猫のデータは限定的。犬から外挿。肺高血圧症に",
            },
        },
        "side_effects": ["hypotension", "facial flushing", "GI upset", "nasal congestion"],
        "side_effects_ja": ["低血圧", "顔面紅潮", "消化器症状", "鼻閉"],
        "contraindications": "Concurrent nitrates (severe hypotension). Severe aortic stenosis. Systemic hypotension.",
        "contraindications_ja": "硝酸薬との併用（重度低血圧）。重度大動脈弁狭窄症。全身性低血圧。",
    },
    # ------------------------------------------------------------------
    # Cabergoline – dopamine agonist
    # ------------------------------------------------------------------
    {
        "id": "cabergoline",
        "name": "Cabergoline (Galastop/Dostinex)",
        "name_ja": "カベルゴリン（ギャラストップ/カバサール）",
        "category": "hormones",
        "mechanism": "Ergot-derived dopamine D2 receptor agonist. Inhibits prolactin secretion from anterior pituitary. Used for pregnancy termination, pseudopregnancy, and galactorrhea.",
        "mechanism_ja": "麦角由来ドパミンD2受容体作動薬。下垂体前葉からのプロラクチン分泌を抑制。偽妊娠の治療・妊娠中絶・乳汁漏出に使用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5 µg/kg PO q24h for 5-10 days",
                "dosage_ja": "5 µg/kg 経口 24時間毎 5-10日間",
                "notes": "For pseudopregnancy (usually 5-7 days); pregnancy termination (combine with PGF2α after day 25). Licensed veterinary product (Galastop) in EU",
                "notes_ja": "偽妊娠に（通常5-7日間）。妊娠中絶（25日以降にPGF2αと併用）。EU圏で動物用医薬品（ギャラストップ）として承認",
            },
            "cat": {
                "safe": True,
                "dosage": "5 µg/kg PO q24h for 5-7 days",
                "dosage_ja": "5 µg/kg 経口 24時間毎 5-7日間",
                "notes": "For pseudopregnancy and lactation suppression",
                "notes_ja": "偽妊娠・泌乳抑制に",
            },
            "ferret": {
                "safe": True,
                "dosage": "5 µg/kg PO q24h for 5-7 days",
                "dosage_ja": "5 µg/kg 経口 24時間毎 5-7日間",
                "notes": "Off-label; for persistent estrus or pseudopregnancy",
                "notes_ja": "適応外。持続発情・偽妊娠に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "5 µg/kg PO q24h for 5-7 days",
                "dosage_ja": "5 µg/kg 経口 24時間毎 5-7日間",
                "notes": "For pseudopregnancy in rabbits",
                "notes_ja": "ウサギの偽妊娠に",
            },
        },
        "side_effects": ["vomiting (transient)", "anorexia (mild)", "drowsiness"],
        "side_effects_ja": ["嘔吐（一過性）", "食欲不振（軽度）", "眠気"],
        "contraindications": "Pregnancy (unless intended termination). Hypersensitivity to ergot alkaloids.",
        "contraindications_ja": "妊娠中（中絶目的でない限り）。麦角アルカロイド過敏症。",
    },
    # ------------------------------------------------------------------
    # Tranexamic acid – antifibrinolytic
    # ------------------------------------------------------------------
    {
        "id": "tranexamic_acid",
        "name": "Tranexamic Acid (TXA/Transamin)",
        "name_ja": "トラネキサム酸（トランサミン）",
        "category": "cardiovascular",
        "mechanism": "Synthetic lysine analog; competitively inhibits plasminogen activation, preventing fibrinolysis. Stabilizes clots. Used for hemorrhage, DIC (hyperfibrinolytic phase), and surgical bleeding.",
        "mechanism_ja": "合成リジンアナログ。プラスミノゲン活性化を競合的に阻害し線溶を防止。血栓を安定化。出血、DIC（線溶亢進相）、手術出血に使用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-25 mg/kg IV/PO q8-12h",
                "dosage_ja": "10-25 mg/kg 静注/経口 8-12時間毎",
                "notes": "For life-threatening hemorrhage, hemoabdomen, post-surgical bleeding. Can give as CRI 10 mg/kg/h",
                "notes_ja": "生命を脅かす出血、血腹、術後出血に。持続投与 10 mg/kg/時も可",
            },
            "cat": {
                "safe": True,
                "dosage": "10-20 mg/kg IV/PO q8-12h",
                "dosage_ja": "10-20 mg/kg 静注/経口 8-12時間毎",
                "notes": "For hemorrhage control; limited feline-specific data",
                "notes_ja": "止血に。猫固有のデータは限定的",
            },
            "horse": {
                "safe": True,
                "dosage": "5-10 mg/kg IV q8-12h",
                "dosage_ja": "5-10 mg/kg 静注 8-12時間毎",
                "notes": "For exercise-induced pulmonary hemorrhage (EIPH); intra-operative hemorrhage",
                "notes_ja": "運動誘発性肺出血（EIPH）、術中出血に",
            },
        },
        "side_effects": ["GI upset", "thromboembolism (theoretical risk)", "seizures (rare, high dose)"],
        "side_effects_ja": ["消化器症状", "血栓塞栓症（理論的リスク）", "痙攣（稀、高用量）"],
        "contraindications": "Active thromboembolic disease. DIC (hypercoagulable phase). Severe renal impairment (adjust dose). Hematuria of upper urinary tract origin (risk of ureteral obstruction).",
        "contraindications_ja": "活動性血栓塞栓症。DIC（過凝固相）。重度腎障害（用量調整）。上部尿路由来の血尿（尿管閉塞リスク）。",
    },
    # ------------------------------------------------------------------
    # Aminocaproic acid – antifibrinolytic
    # ------------------------------------------------------------------
    {
        "id": "aminocaproic_acid",
        "name": "Aminocaproic Acid (Amicar)",
        "name_ja": "アミノカプロン酸（イプシロン）",
        "category": "cardiovascular",
        "mechanism": "Lysine analog; inhibits plasminogen activation and fibrinolysis. Also used empirically for degenerative myelopathy (DM) in dogs to slow progression.",
        "mechanism_ja": "リジンアナログ。プラスミノゲン活性化・線溶を阻害。犬の変性性脊髄症（DM）の進行遅延に経験的にも使用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Hemorrhage: 15-40 mg/kg IV/PO q8h; DM: 500 mg PO q8h (large dogs)",
                "dosage_ja": "出血: 15-40 mg/kg 静注/経口 8時間毎；DM: 500 mg 経口 8時間毎（大型犬）",
                "notes": "For DM in German Shepherds/Corgis (empirical). For hemorrhagic conditions and post-surgical bleeding",
                "notes_ja": "ジャーマンシェパード/コーギーのDMに（経験的）。出血性疾患・術後出血に",
            },
            "cat": {
                "safe": True,
                "dosage": "15-20 mg/kg IV/PO q8h",
                "dosage_ja": "15-20 mg/kg 静注/経口 8時間毎",
                "notes": "For hemorrhage control; less data than tranexamic acid in cats",
                "notes_ja": "止血に。猫ではトラネキサム酸よりデータが少ない",
            },
            "horse": {
                "safe": True,
                "dosage": "30-50 mg/kg IV slow q6-8h",
                "dosage_ja": "30-50 mg/kg 緩徐静注 6-8時間毎",
                "notes": "For surgical hemorrhage; give IV slowly to avoid hypotension",
                "notes_ja": "手術出血に。低血圧回避のため緩徐に静注",
            },
        },
        "side_effects": ["GI upset", "hypotension (rapid IV)", "myopathy (prolonged use)", "thrombosis (theoretical)"],
        "side_effects_ja": ["消化器症状", "低血圧（急速静注時）", "筋症（長期使用）", "血栓症（理論的）"],
        "contraindications": "Active intravascular clotting (DIC hypercoagulable phase). Upper urinary tract bleeding (ureteral clot risk).",
        "contraindications_ja": "活動性血管内凝固（DIC過凝固相）。上部尿路出血（尿管血栓リスク）。",
    },
    # ------------------------------------------------------------------
    # Cosyntropin – diagnostic (ACTH stimulation test)
    # ------------------------------------------------------------------
    {
        "id": "cosyntropin",
        "name": "Cosyntropin (Cortrosyn/Synacthen)",
        "name_ja": "コシントロピン（コートロシン/シナクテン）",
        "category": "endocrine",
        "mechanism": "Synthetic ACTH (1-24) analog. Stimulates adrenal cortex to produce cortisol. Used as diagnostic agent for ACTH stimulation test to evaluate adrenal function (Addison's, Cushing's, and iatrogenic hypoadrenocorticism).",
        "mechanism_ja": "合成ACTH（1-24）アナログ。副腎皮質を刺激しコルチゾール産生を促進。ACTH刺激試験の診断薬として副腎機能評価に使用（アジソン病、クッシング症候群、医原性副腎皮質機能低下症）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5 µg/kg IV/IM (max 250 µg); measure cortisol at 0 and 60 min post-injection",
                "dosage_ja": "5 µg/kg 静注/筋注（最大250 µg）；投与前と投与後60分にコルチゾール測定",
                "notes": "Gold standard for Addison's diagnosis and trilostane monitoring. Can use low-dose (1 µg/kg) protocol for increased sensitivity",
                "notes_ja": "アジソン病診断・トリロスタンモニタリングのゴールドスタンダード。感度向上には低用量（1 µg/kg）プロトコルも可",
            },
            "cat": {
                "safe": True,
                "dosage": "125 µg/cat IV/IM; measure cortisol at 0 and 60 min",
                "dosage_ja": "125 µg/匹 静注/筋注；投与前と投与後60分にコルチゾール測定",
                "notes": "Feline Addison's is rare but increasing recognition. Also for monitoring exogenous steroid effects",
                "notes_ja": "猫のアジソン病は稀だが認識増加中。外因性ステロイド効果のモニタリングにも",
            },
            "horse": {
                "safe": True,
                "dosage": "1 µg/kg IV or 100 µg/horse IV; cortisol at 0 and 30 min",
                "dosage_ja": "1 µg/kg 静注 または 100 µg/頭 静注；投与前と投与後30分にコルチゾール測定",
                "notes": "For evaluation of PPID; TRH stimulation test is preferred for equine Cushing's",
                "notes_ja": "PPID評価に。馬のクッシングにはTRH刺激試験が推奨",
            },
            "ferret": {
                "safe": True,
                "dosage": "1 µg/kg IV/IM; cortisol at 0 and 60 min",
                "dosage_ja": "1 µg/kg 静注/筋注；投与前と投与後60分にコルチゾール測定",
                "notes": "For suspected iatrogenic or naturally occurring hypoadrenocorticism",
                "notes_ja": "医原性または自然発生副腎皮質機能低下症の診断に",
            },
        },
        "side_effects": ["hypersensitivity (rare)", "flushing", "tachycardia"],
        "side_effects_ja": ["過敏反応（稀）", "紅潮", "頻脈"],
        "contraindications": "Known hypersensitivity to cosyntropin. Not a therapeutic agent (diagnostic only).",
        "contraindications_ja": "コシントロピン過敏症。治療薬ではなく診断薬。",
    },
    # ------------------------------------------------------------------
    # Bosentan – endothelin receptor antagonist
    # ------------------------------------------------------------------
    {
        "id": "bosentan",
        "name": "Bosentan (Tracleer)",
        "name_ja": "ボセンタン（トラクリア）",
        "category": "cardiovascular",
        "mechanism": "Dual endothelin receptor antagonist (ETA and ETB). Blocks endothelin-1-mediated vasoconstriction and smooth muscle proliferation in pulmonary vasculature. Used for pulmonary arterial hypertension.",
        "mechanism_ja": "デュアルエンドセリン受容体拮抗薬（ETAおよびETB）。肺血管でエンドセリン-1による血管収縮と平滑筋増殖を遮断。肺動脈性高血圧症に使用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2 mg/kg PO q12h",
                "dosage_ja": "2 mg/kg 経口 12時間毎",
                "notes": "For pulmonary hypertension refractory to sildenafil; can combine with PDE5 inhibitors. Monitor liver enzymes monthly (hepatotoxicity risk)",
                "notes_ja": "シルデナフィル抵抗性肺高血圧症に。PDE5阻害薬と併用可。肝毒性リスクのため月1回肝酵素モニター",
            },
        },
        "side_effects": ["hepatotoxicity (dose-dependent)", "anemia", "edema", "headache", "teratogenicity"],
        "side_effects_ja": ["肝毒性（用量依存性）", "貧血", "浮腫", "頭痛", "催奇形性"],
        "contraindications": "Pregnancy (teratogenic). Moderate-severe hepatic impairment. Concurrent cyclosporine or glyburide.",
        "contraindications_ja": "妊娠（催奇形性）。中等度-重度の肝障害。シクロスポリンまたはグリベンクラミドとの併用。",
    },
    # ------------------------------------------------------------------
    # Xylazine – α2 agonist sedative/analgesic
    # ------------------------------------------------------------------
    {
        "id": "xylazine",
        "name": "Xylazine (Rompun/Sedazine)",
        "name_ja": "キシラジン（ロンプン/セダジン）",
        "category": "sedatives",
        "mechanism": "Alpha-2 adrenergic agonist. Provides dose-dependent sedation, analgesia, and muscle relaxation. Also causes bradycardia, respiratory depression, and transient hyperglycemia.",
        "mechanism_ja": "α2アドレナリン作動薬。用量依存的に鎮静・鎮痛・筋弛緩作用。徐脈、呼吸抑制、一過性高血糖も引き起こす。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Sedation: 0.5-1.1 mg/kg IV (or 1-2 mg/kg IM); Standing sedation: 0.3-0.5 mg/kg IV",
                "dosage_ja": "鎮静: 0.5-1.1 mg/kg 静注（または1-2 mg/kg 筋注）；立位鎮静: 0.3-0.5 mg/kg 静注",
                "notes": "Standard equine sedative. Often combined with butorphanol for enhanced sedation/analgesia. Reversal: yohimbine or atipamezole. Onset IV: 3-5 min",
                "notes_ja": "馬の標準的鎮静薬。ブトルファノールと併用で鎮静・鎮痛増強。拮抗: ヨヒンビンまたはアチパメゾール。静注効果発現: 3-5分",
            },
            "dog": {
                "safe": True,
                "dosage": "0.5-1.1 mg/kg IV/IM",
                "dosage_ja": "0.5-1.1 mg/kg 静注/筋注",
                "notes": "Less commonly used in dogs vs dexmedetomidine; causes vomiting (useful for emesis induction). Bradycardia expected",
                "notes_ja": "犬ではデクスメデトミジンより使用頻度低い。催吐作用あり（催吐に利用可能）。徐脈は予期される反応",
            },
            "cat": {
                "safe": True,
                "dosage": "0.5-1.1 mg/kg IM",
                "dosage_ja": "0.5-1.1 mg/kg 筋注",
                "notes": "Effective emetic in cats; also sedation. Profound bradycardia possible",
                "notes_ja": "猫で有効な催吐薬。鎮静にも。高度徐脈の可能性あり",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1-5 mg/kg IM (usually combined with ketamine)",
                "dosage_ja": "1-5 mg/kg 筋注（通常ケタミンと併用）",
                "notes": "Part of ketamine-xylazine protocol; monitor respiratory depression closely",
                "notes_ja": "ケタミン-キシラジンプロトコルの一部。呼吸抑制を厳密にモニター",
            },
        },
        "side_effects": ["bradycardia", "respiratory depression", "hyperglycemia", "vomiting (dogs/cats)", "bloat (horses)", "muscle tremors"],
        "side_effects_ja": ["徐脈", "呼吸抑制", "高血糖", "嘔吐（犬/猫）", "鼓脹（馬）", "筋振戦"],
        "contraindications": "Severe cardiac disease. Last trimester of pregnancy (oxytocic effect). GI obstruction (vomiting risk). Do not use IV in cats.",
        "contraindications_ja": "重度の心疾患。妊娠末期（子宮収縮作用）。消化管閉塞（嘔吐リスク）。猫に静注不可。",
    },
    # ------------------------------------------------------------------
    # Detomidine – α2 agonist (primarily equine)
    # ------------------------------------------------------------------
    {
        "id": "detomidine",
        "name": "Detomidine (Dormosedan)",
        "name_ja": "デトミジン（ドルモセダン）",
        "category": "sedatives",
        "mechanism": "Potent alpha-2 adrenergic agonist with higher α2 selectivity than xylazine. Provides profound sedation and visceral analgesia. Available as injectable and oral transmucosal gel (Dormosedan Gel).",
        "mechanism_ja": "キシラジンよりα2選択性が高い強力なα2アドレナリン作動薬。深い鎮静と内臓鎮痛作用。注射剤および口腔粘膜ジェル（ドルモセダンジェル）がある。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "IV: 10-40 µg/kg; IM: 20-80 µg/kg; OTM gel: 40 µg/kg sublingual",
                "dosage_ja": "静注: 10-40 µg/kg；筋注: 20-80 µg/kg；口腔ジェル: 40 µg/kg 舌下",
                "notes": "Gold standard equine sedative. More potent and longer-lasting than xylazine. OTM gel for non-injectable sedation (farrier, clipping). Combine with butorphanol for procedures",
                "notes_ja": "馬鎮静のゴールドスタンダード。キシラジンより強力で長時間。OTMジェルで非注射鎮静（装蹄、クリッピング）。処置にはブトルファノール併用",
            },
            "dog": {
                "safe": True,
                "dosage": "10-30 µg/kg IV/IM",
                "dosage_ja": "10-30 µg/kg 静注/筋注",
                "notes": "Rarely used in dogs; dexmedetomidine preferred. Research setting mainly",
                "notes_ja": "犬では殆ど使用しない。デクスメデトミジンが推奨。主に研究用途",
            },
        },
        "side_effects": ["bradycardia", "AV block", "respiratory depression", "sweating (horses)", "ataxia", "penile prolapse (horses)"],
        "side_effects_ja": ["徐脈", "房室ブロック", "呼吸抑制", "発汗（馬）", "運動失調", "陰茎脱出（馬）"],
        "contraindications": "Severe cardiac disease. Last trimester pregnancy. Not for food-producing horses in some jurisdictions. Reversal: atipamezole.",
        "contraindications_ja": "重度の心疾患。妊娠末期。一部法域で食用馬には使用不可。拮抗: アチパメゾール。",
    },
    # ------------------------------------------------------------------
    # Romifidine – α2 agonist (equine)
    # ------------------------------------------------------------------
    {
        "id": "romifidine",
        "name": "Romifidine (Sedivet)",
        "name_ja": "ロミフィジン（セディベット）",
        "category": "sedatives",
        "mechanism": "Alpha-2 adrenergic agonist with highest α2:α1 selectivity ratio among equine sedatives. Provides reliable standing sedation with less ataxia than xylazine or detomidine.",
        "mechanism_ja": "馬用鎮静薬の中で最もα2:α1選択性比が高いα2アドレナリン作動薬。キシラジンやデトミジンより運動失調が少なく、安定した立位鎮静を提供。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "40-120 µg/kg IV",
                "dosage_ja": "40-120 µg/kg 静注",
                "notes": "Best standing sedation with minimal ataxia. Longer onset (5-10 min) but longer duration than xylazine. Often combined with butorphanol",
                "notes_ja": "最小限の運動失調で最良の立位鎮静。効果発現はやや遅い（5-10分）がキシラジンより長時間。ブトルファノールと併用が多い",
            },
        },
        "side_effects": ["bradycardia", "AV block", "reduced GI motility", "mild ataxia", "sweating"],
        "side_effects_ja": ["徐脈", "房室ブロック", "消化管運動低下", "軽度運動失調", "発汗"],
        "contraindications": "Severe cardiac disease. Pre-existing bradycardia/AV block. Last trimester pregnancy.",
        "contraindications_ja": "重度の心疾患。既存の徐脈/房室ブロック。妊娠末期。",
    },
    # ------------------------------------------------------------------
    # Clenbuterol – β2 agonist bronchodilator (equine)
    # ------------------------------------------------------------------
    {
        "id": "clenbuterol",
        "name": "Clenbuterol (Ventipulmin)",
        "name_ja": "クレンブテロール（ベンティプルミン）",
        "category": "bronchodilators",
        "mechanism": "Selective beta-2 adrenergic agonist. Relaxes bronchial smooth muscle causing bronchodilation. Also has mucolytic properties. Long half-life in horses.",
        "mechanism_ja": "選択的β2アドレナリン作動薬。気管支平滑筋を弛緩し気管支拡張。粘液溶解作用もあり。馬で長い半減期。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "0.8-3.2 µg/kg PO q12h (start low, titrate up over 3 days)",
                "dosage_ja": "0.8-3.2 µg/kg 経口 12時間毎（低用量から3日かけて漸増）",
                "notes": "FDA-approved for horses (Ventipulmin syrup). For RAO/heaves and IAD. Taper down when discontinuing to prevent rebound bronchoconstriction. Withdrawal time applies for competition horses",
                "notes_ja": "馬にFDA承認（ベンティプルミンシロップ）。RAO/喘鳴・IADに。中止時は漸減（リバウンド気管支収縮予防）。競走馬は休薬期間あり",
            },
        },
        "side_effects": ["tachycardia", "sweating", "muscle tremors", "restlessness", "decreased appetite (initial)"],
        "side_effects_ja": ["頻脈", "発汗", "筋振戦", "不穏", "食欲低下（初期）"],
        "contraindications": "Cardiac arrhythmias. Concurrent β-blocker use (antagonism). Not approved for food animals in many countries.",
        "contraindications_ja": "心不整脈。β遮断薬との併用（拮抗）。多くの国で食用動物には未承認。",
    },
    # ------------------------------------------------------------------
    # Famciclovir – antiviral (feline herpesvirus)
    # ------------------------------------------------------------------
    {
        "id": "famciclovir",
        "name": "Famciclovir (Famvir)",
        "name_ja": "ファムシクロビル（ファムビル）",
        "category": "antibiotics",
        "mechanism": "Prodrug of penciclovir; converted to penciclovir triphosphate which inhibits viral DNA polymerase. Active against feline herpesvirus-1 (FHV-1). Oral bioavailability is superior to acyclovir in cats.",
        "mechanism_ja": "ペンシクロビルのプロドラッグ。ペンシクロビル三リン酸に変換されウイルスDNAポリメラーゼを阻害。猫ヘルペスウイルス1型（FHV-1）に有効。猫ではアシクロビルより経口バイオアベイラビリティが優れる。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "40-90 mg/kg PO q8-12h",
                "dosage_ja": "40-90 mg/kg 経口 8-12時間毎",
                "notes": "First-line antiviral for FHV-1 (rhinotracheitis, keratitis, dermatitis). High doses needed due to cat metabolism. 90 mg/kg q8h for severe cases. Safe long-term",
                "notes_ja": "FHV-1（鼻気管炎、角膜炎、皮膚炎）の第一選択抗ウイルス薬。猫の代謝のため高用量が必要。重症例は90 mg/kg 8時間毎。長期使用安全",
            },
        },
        "side_effects": ["rare GI upset", "mild elevation of liver enzymes (rare)"],
        "side_effects_ja": ["稀に消化器症状", "軽度肝酵素上昇（稀）"],
        "contraindications": "Severe renal impairment (dose adjustment needed). Not effective against calicivirus.",
        "contraindications_ja": "重度腎障害（用量調整必要）。カリシウイルスには無効。",
    },
    # ------------------------------------------------------------------
    # L-Lysine – supplement (feline herpesvirus)
    # ------------------------------------------------------------------
    {
        "id": "lysine",
        "name": "L-Lysine",
        "name_ja": "L-リジン",
        "category": "supplements",
        "mechanism": "Essential amino acid that may antagonize arginine, theoretically reducing herpesvirus replication. Widely used as FHV-1 supplement, though recent evidence questions efficacy.",
        "mechanism_ja": "必須アミノ酸でアルギニンに拮抗し、理論的にヘルペスウイルス複製を減少。FHV-1サプリメントとして広く使用されるが、近年のエビデンスでは有効性に疑問。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "250-500 mg/cat PO q12-24h",
                "dosage_ja": "250-500 mg/匹 経口 12-24時間毎",
                "notes": "Widely used for FHV-1 but 2015 ABCD and recent meta-analyses found insufficient evidence of efficacy. Low risk, may have placebo value. Not a substitute for famciclovir in severe cases",
                "notes_ja": "FHV-1に広く使用されるが、2015年ABCDおよび最近のメタアナリシスで有効性のエビデンス不十分。リスクは低い。重症例ではファムシクロビルの代替にならない",
            },
        },
        "side_effects": ["rare GI upset"],
        "side_effects_ja": ["稀に消化器症状"],
        "contraindications": "None significant.",
        "contraindications_ja": "特になし。",
    },
    # ------------------------------------------------------------------
    # Interferon omega – antiviral/immunomodulator
    # ------------------------------------------------------------------
    {
        "id": "interferon_omega",
        "name": "Feline Interferon Omega (Virbagen Omega)",
        "name_ja": "猫インターフェロンオメガ（インターキャット/ビルバゲンオメガ）",
        "category": "immunosuppressives",
        "mechanism": "Recombinant feline interferon omega (rFeIFN-ω). Antiviral and immunomodulatory. Binds cell surface receptors to induce antiviral state. Licensed in EU/Japan for canine parvovirus and feline retroviral infections.",
        "mechanism_ja": "組換え猫インターフェロンオメガ（rFeIFN-ω）。抗ウイルス・免疫調節作用。細胞表面受容体に結合し抗ウイルス状態を誘導。EU/日本で犬パルボウイルスおよび猫レトロウイルス感染に承認。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "FeLV/FIV: 1 MU/kg SC q48h x 3 doses, 3 cycles (weeks 0, 2, 8); Stomatitis: 0.1 MU oral daily",
                "dosage_ja": "FeLV/FIV: 1 MU/kg 皮下 48時間毎×3回、3サイクル（0,2,8週）；口内炎: 0.1 MU 経口 毎日",
                "notes": "For FeLV/FIV (improves clinical signs, not curative), chronic gingivostomatitis (oral mucosal application). Licensed in Japan (インターキャット)",
                "notes_ja": "FeLV/FIV（臨床症状改善、治癒ではない）、慢性歯肉口内炎（口腔粘膜塗布）に。日本で承認（インターキャット）",
            },
            "dog": {
                "safe": True,
                "dosage": "Parvovirus: 2.5 MU/kg IV q24h x 3 days (start as early as possible)",
                "dosage_ja": "パルボウイルス: 2.5 MU/kg 静注 24時間毎×3日（できるだけ早期に開始）",
                "notes": "Licensed for canine parvovirus in EU/Japan. Most effective when started within 3 days of symptom onset. Reduces mortality in clinical trials",
                "notes_ja": "EU/日本で犬パルボウイルスに承認。症状発現3日以内の開始が最も有効。臨床試験で死亡率低下",
            },
        },
        "side_effects": ["transient hyperthermia", "lethargy", "vomiting (rare)", "mild transient leukopenia"],
        "side_effects_ja": ["一過性発熱", "倦怠感", "嘔吐（稀）", "軽度一過性白血球減少"],
        "contraindications": "Hypersensitivity to feline interferon. Not for use in pregnancy.",
        "contraindications_ja": "猫インターフェロン過敏症。妊娠中は使用不可。",
    },
    # ------------------------------------------------------------------
    # Methylprednisolone – corticosteroid
    # ------------------------------------------------------------------
    {
        "id": "methylprednisolone",
        "name": "Methylprednisolone (Depo-Medrol/Medrol)",
        "name_ja": "メチルプレドニゾロン（デポメドロール/メドロール）",
        "category": "corticosteroids",
        "mechanism": "Intermediate-acting synthetic glucocorticoid with minimal mineralocorticoid activity. Available as oral tablets (Medrol) and injectable depot (Depo-Medrol, methylprednisolone acetate). 5x potency of cortisol.",
        "mechanism_ja": "ミネラルコルチコイド活性が少ない中間型合成グルココルチコイド。経口錠（メドロール）と注射用デポ剤（デポメドロール、酢酸メチルプレドニゾロン）がある。コルチゾールの5倍の力価。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Anti-inflammatory: 0.5-1 mg/kg PO q12-24h; Immunosuppressive: 2-4 mg/kg PO q12-24h; Depot IM: 1-2 mg/kg (duration 2-6 weeks)",
                "dosage_ja": "抗炎症: 0.5-1 mg/kg 経口 12-24時間毎；免疫抑制: 2-4 mg/kg 経口 12-24時間毎；デポ筋注: 1-2 mg/kg（持続2-6週）",
                "notes": "Oral for IMHA/IMTP/IBD; Depo-Medrol for allergic skin disease when compliance difficult. Taper slowly",
                "notes_ja": "経口はIMHA/IMTP/IBDに。デポメドロールはコンプライアンス困難時のアレルギー性皮膚疾患に。ゆっくり漸減",
            },
            "cat": {
                "safe": True,
                "dosage": "Anti-inflammatory: 0.5-1 mg/kg PO q12-24h; Depot: 10-20 mg/cat IM/SC q2-6 weeks",
                "dosage_ja": "抗炎症: 0.5-1 mg/kg 経口 12-24時間毎；デポ: 10-20 mg/匹 筋注/皮下 2-6週毎",
                "notes": "Depo-Medrol widely used in Japan for feline asthma, eosinophilic granuloma, allergic dermatitis. Risk of diabetes with repeated depot injections",
                "notes_ja": "デポメドロールは日本で猫喘息・好酸球性肉芽腫・アレルギー性皮膚炎に広く使用。デポ繰返し投与で糖尿病リスク",
            },
            "horse": {
                "safe": True,
                "dosage": "Intra-articular: 40-120 mg per joint; Systemic: 0.5-1 mg/kg IM",
                "dosage_ja": "関節内: 40-120 mg/関節；全身: 0.5-1 mg/kg 筋注",
                "notes": "Commonly used intra-articularly for OA. Withdrawal time for competition horses. Risk of laminitis with systemic use",
                "notes_ja": "OAの関節内注射に頻用。競走馬は休薬期間あり。全身投与で蹄葉炎リスク",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5-2 mg/kg IM/SC (depot)",
                "dosage_ja": "0.5-2 mg/kg 筋注/皮下（デポ）",
                "notes": "Use cautiously; rabbits susceptible to immunosuppression. Short-term only",
                "notes_ja": "慎重に使用。ウサギは免疫抑制に感受性が高い。短期使用のみ",
            },
        },
        "side_effects": ["PU/PD", "polyphagia", "iatrogenic Cushing's", "diabetes (cats)", "GI ulceration", "immunosuppression"],
        "side_effects_ja": ["多飲多尿", "多食", "医原性クッシング症候群", "糖尿病（猫）", "消化管潰瘍", "免疫抑制"],
        "contraindications": "Systemic fungal infections. Diabetes mellitus (relative). GI ulceration. Active infections without antibiotic coverage.",
        "contraindications_ja": "全身性真菌感染症。糖尿病（相対的禁忌）。消化管潰瘍。抗菌薬カバーのない活動性感染症。",
    },
    # ------------------------------------------------------------------
    # Imidacloprid + Moxidectin (Advocate/Advantage Multi)
    # ------------------------------------------------------------------
    {
        "id": "imidacloprid_moxidectin",
        "name": "Imidacloprid + Moxidectin (Advocate/Advantage Multi)",
        "name_ja": "イミダクロプリド＋モキシデクチン（アドボケート）",
        "category": "antiparasitics",
        "mechanism": "Combination topical: imidacloprid (neonicotinoid, kills fleas) + moxidectin (macrocyclic lactone, kills heartworm larvae, GI nematodes, ear mites, and Demodex/Sarcoptes). Broad-spectrum endo/ectoparasiticide.",
        "mechanism_ja": "配合外用薬：イミダクロプリド（ネオニコチノイド、ノミ駆除）＋モキシデクチン（マクロライド系、フィラリア幼虫・消化管線虫・ミミヒゼンダニ・ニキビダニ/疥癬虫を駆除）。広域スペクトル内外部寄生虫駆除薬。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10 mg/kg imidacloprid + 2.5 mg/kg moxidectin topical monthly",
                "dosage_ja": "イミダクロプリド10 mg/kg＋モキシデクチン2.5 mg/kg 外用 月1回",
                "notes": "Heartworm prevention + flea treatment + GI nematodes + mites. AVOID in dogs with MDR1 mutation at high doses. Do not use orally",
                "notes_ja": "フィラリア予防＋ノミ駆除＋消化管線虫＋ダニ。MDR1変異犬は高用量で注意。経口使用不可",
            },
            "cat": {
                "safe": True,
                "dosage": "10 mg/kg imidacloprid + 1 mg/kg moxidectin topical monthly",
                "dosage_ja": "イミダクロプリド10 mg/kg＋モキシデクチン1 mg/kg 外用 月1回",
                "notes": "Heartworm prevention + flea/ear mite/roundworm treatment. Safe for cats ≥9 weeks",
                "notes_ja": "フィラリア予防＋ノミ・ミミヒゼンダニ・回虫駆除。9週齢以上の猫に安全",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.4 mL/ferret (cat <4kg pipette) topical monthly",
                "dosage_ja": "0.4 mL/匹（猫4kg未満用ピペット）外用 月1回",
                "notes": "Approved for ferrets in EU (Advocate). Heartworm prevention and flea control",
                "notes_ja": "EUでフェレットに承認（アドボケート）。フィラリア予防＋ノミ駆除",
            },
        },
        "side_effects": ["transient skin irritation", "lethargy (rare)", "GI upset if ingested"],
        "side_effects_ja": ["一過性皮膚刺激", "倦怠感（稀）", "経口摂取時の消化器症状"],
        "contraindications": "Not for oral use. Puppies/kittens <7-9 weeks. Caution in MDR1 mutant breeds (collies).",
        "contraindications_ja": "経口使用不可。7-9週齢未満の子犬/子猫。MDR1変異種（コリー系）は注意。",
    },
    # ------------------------------------------------------------------
    # Milbemycin oxime + Praziquantel (Milbemax/Interceptor Plus)
    # ------------------------------------------------------------------
    {
        "id": "milbemycin_praziquantel",
        "name": "Milbemycin Oxime + Praziquantel (Milbemax/Interceptor Plus)",
        "name_ja": "ミルベマイシンオキシム＋プラジクアンテル（ミルベマックス）",
        "category": "antiparasitics",
        "mechanism": "Combination oral: milbemycin oxime (macrocyclic lactone, heartworm prevention + nematodes) + praziquantel (isoquinolone, cestodes including Echinococcus). Monthly broad-spectrum internal parasiticide.",
        "mechanism_ja": "配合経口薬：ミルベマイシンオキシム（マクロライド系、フィラリア予防＋線虫）＋プラジクアンテル（イソキノロン系、エキノコックス含む条虫）。月1回の広域スペクトル内部寄生虫駆除薬。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1 mg/kg milbemycin + 5 mg/kg praziquantel PO monthly",
                "dosage_ja": "ミルベマイシン0.5-1 mg/kg＋プラジクアンテル5 mg/kg 経口 月1回",
                "notes": "Heartworm prevention + roundworm/hookworm/whipworm + tapeworm (including Echinococcus). Very commonly used in Japan (ミルベマックス)",
                "notes_ja": "フィラリア予防＋回虫/鉤虫/鞭虫＋条虫（エキノコックス含む）。日本で非常に頻用（ミルベマックス）",
            },
            "cat": {
                "safe": True,
                "dosage": "2 mg/kg milbemycin + 5 mg/kg praziquantel PO monthly",
                "dosage_ja": "ミルベマイシン2 mg/kg＋プラジクアンテル5 mg/kg 経口 月1回",
                "notes": "All-in-one dewormer for cats; safe from 6 weeks. Covers roundworm, hookworm, tapeworm",
                "notes_ja": "猫のオールインワン駆虫薬。6週齢から安全。回虫、鉤虫、条虫に対応",
            },
        },
        "side_effects": ["rare GI upset", "rare lethargy", "hypersalivation (cats, if tablet crushed)"],
        "side_effects_ja": ["稀に消化器症状", "稀に倦怠感", "流涎（猫、錠剤を砕いた場合）"],
        "contraindications": "Puppies <2 weeks or kittens <6 weeks. Caution in MDR1 mutant breeds at higher doses.",
        "contraindications_ja": "2週齢未満の子犬・6週齢未満の子猫。MDR1変異種は高用量で注意。",
    },
    # ------------------------------------------------------------------
    # Selamectin + Sarolaner (Stronghold Plus/Revolution Plus)
    # ------------------------------------------------------------------
    {
        "id": "selamectin_sarolaner",
        "name": "Selamectin + Sarolaner (Revolution Plus/Stronghold Plus)",
        "name_ja": "セラメクチン＋サロラネル（レボリューションプラス/ストロングホールドプラス）",
        "category": "antiparasitics",
        "mechanism": "Combination topical for cats: selamectin (avermectin, heartworm + roundworm + ear mites + fleas) + sarolaner (isoxazoline, ticks + fleas). Broadest spectrum cat-approved topical parasiticide.",
        "mechanism_ja": "猫用配合外用薬：セラメクチン（アベルメクチン系、フィラリア＋回虫＋ミミヒゼンダニ＋ノミ）＋サロラネル（イソオキサゾリン系、マダニ＋ノミ）。猫に承認された最も広いスペクトルの外用駆虫薬。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "6 mg/kg selamectin + 1 mg/kg sarolaner topical monthly",
                "dosage_ja": "セラメクチン6 mg/kg＋サロラネル1 mg/kg 外用 月1回",
                "notes": "Covers fleas, ticks, heartworm, roundworm, hookworm, ear mites. For cats ≥8 weeks and ≥1.25 kg. Very popular in Japan",
                "notes_ja": "ノミ、マダニ、フィラリア、回虫、鉤虫、ミミヒゼンダニに対応。8週齢以上・1.25kg以上の猫に。日本で非常に人気",
            },
        },
        "side_effects": ["transient hair loss at application site", "lethargy (rare)", "GI upset (rare)"],
        "side_effects_ja": ["塗布部位の一過性脱毛", "倦怠感（稀）", "消化器症状（稀）"],
        "contraindications": "Kittens <8 weeks or <1.25 kg. Not for dogs (sarolaner component dose differs).",
        "contraindications_ja": "8週齢未満または1.25kg未満の子猫。犬には不可（サロラネル成分の用量が異なる）。",
    },
    # ------------------------------------------------------------------
    # Spinosad (Comfortis) – oral flea control
    # ------------------------------------------------------------------
    {
        "id": "spinosad",
        "name": "Spinosad (Comfortis)",
        "name_ja": "スピノサド（コンフォティス）",
        "category": "antiparasitics",
        "mechanism": "Spinosyn insecticide derived from Saccharopolyspora spinosa. Activates nicotinic acetylcholine receptors in insects causing hyperexcitation and death. Rapid oral flea kill (begins within 30 min, 100% in 4h).",
        "mechanism_ja": "放線菌Saccharopolyspora spinosa由来のスピノシン系殺虫薬。昆虫のニコチン性アセチルコリン受容体を活性化し過興奮と死滅。速効性経口ノミ駆除（30分以内に効果発現、4時間で100%）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "30-60 mg/kg PO monthly (with food)",
                "dosage_ja": "30-60 mg/kg 経口 月1回（食事と）",
                "notes": "FDA-approved for dogs ≥14 weeks and ≥2.3 kg. Give with food for best absorption. Fastest flea kill among monthly orals",
                "notes_ja": "14週齢以上・2.3kg以上の犬にFDA承認。食事と投与で吸収向上。月1回経口薬の中で最速のノミ駆除",
            },
            "cat": {
                "safe": True,
                "dosage": "50-100 mg/kg PO monthly (with food)",
                "dosage_ja": "50-100 mg/kg 経口 月1回（食事と）",
                "notes": "FDA-approved for cats ≥14 weeks and ≥1.8 kg. Higher dose needed in cats. Vomiting common initially",
                "notes_ja": "14週齢以上・1.8kg以上の猫にFDA承認。猫は犬より高用量が必要。初期に嘔吐が多い",
            },
        },
        "side_effects": ["vomiting (most common, especially cats)", "diarrhea", "anorexia", "lethargy"],
        "side_effects_ja": ["嘔吐（最多、特に猫）", "下痢", "食欲不振", "倦怠感"],
        "contraindications": "Do not combine with high-dose ivermectin (increased ivermectin toxicity via P-gp). Dogs/cats <14 weeks. Epileptic dogs (may lower seizure threshold).",
        "contraindications_ja": "高用量イベルメクチンとの併用不可（P-gp阻害でイベルメクチン毒性増加）。14週齢未満の犬/猫。てんかん犬（痙攣閾値低下の可能性）。",
    },
    # ------------------------------------------------------------------
    # Hydrochlorothiazide – thiazide diuretic
    # ------------------------------------------------------------------
    {
        "id": "hydrochlorothiazide",
        "name": "Hydrochlorothiazide (HCTZ)",
        "name_ja": "ヒドロクロロチアジド",
        "category": "diuretics",
        "mechanism": "Thiazide diuretic; inhibits Na-Cl cotransporter in distal convoluted tubule. Mild diuresis. Also reduces urinary calcium excretion (useful for calcium oxalate urolithiasis prevention).",
        "mechanism_ja": "チアジド系利尿薬。遠位尿細管のNa-Cl共輸送体を阻害。軽度の利尿作用。尿中カルシウム排泄を減少（シュウ酸カルシウム尿石予防に有用）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Diuretic: 2-4 mg/kg PO q12h; Ca-oxalate prevention: 2 mg/kg PO q12h",
                "dosage_ja": "利尿: 2-4 mg/kg 経口 12時間毎；シュウ酸Ca予防: 2 mg/kg 経口 12時間毎",
                "notes": "Often combined with furosemide for refractory CHF. Reduces urinary calcium for CaOx stone prevention. Monitor electrolytes (hypokalemia, hyponatremia)",
                "notes_ja": "難治性CHFでフロセミドと併用が多い。CaOx結石予防に尿中カルシウム低下。電解質モニター（低K、低Na）",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q12-24h",
                "dosage_ja": "1-2 mg/kg 経口 12-24時間毎",
                "notes": "For calcium oxalate stone prevention; less commonly used as diuretic in cats",
                "notes_ja": "シュウ酸カルシウム結石予防に。猫では利尿薬としてはあまり使用されない",
            },
            "horse": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO/IV q12-24h",
                "dosage_ja": "0.5-1 mg/kg 経口/静注 12-24時間毎",
                "notes": "For edema; limited equine use",
                "notes_ja": "浮腫に。馬での使用は限定的",
            },
        },
        "side_effects": ["hypokalemia", "hyponatremia", "dehydration", "hyperglycemia", "hypercalcemia"],
        "side_effects_ja": ["低カリウム血症", "低ナトリウム血症", "脱水", "高血糖", "高カルシウム血症"],
        "contraindications": "Anuria. Severe renal failure. Hypercalcemia. Hypokalemia.",
        "contraindications_ja": "無尿。重度腎不全。高カルシウム血症。低カリウム血症。",
    },
    # ------------------------------------------------------------------
    # Miconazole + Chlorhexidine (Malaseb)
    # ------------------------------------------------------------------
    {
        "id": "miconazole_chlorhex",
        "name": "Miconazole + Chlorhexidine (Malaseb)",
        "name_ja": "ミコナゾール＋クロルヘキシジン（マラセブ）",
        "category": "dermatological",
        "mechanism": "Combination medicated shampoo: miconazole (imidazole antifungal, inhibits ergosterol synthesis) + chlorhexidine (cationic antiseptic, disrupts bacterial cell membranes). Synergistic activity against Malassezia and bacteria.",
        "mechanism_ja": "配合薬用シャンプー：ミコナゾール（イミダゾール系抗真菌薬、エルゴステロール合成阻害）＋クロルヘキシジン（カチオン性殺菌薬、細菌細胞膜破壊）。マラセチアと細菌に相乗作用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2% miconazole + 2% chlorhexidine shampoo; lather and leave on 10 min, rinse. q3-7 days",
                "dosage_ja": "ミコナゾール2%＋クロルヘキシジン2%シャンプー；泡立て10分放置後すすぐ。3-7日毎",
                "notes": "Gold standard for Malassezia dermatitis and pyoderma. Leave-on time important for efficacy. Can also use as pre-surgical scrub component",
                "notes_ja": "マラセチア皮膚炎・膿皮症のゴールドスタンダード。効果のため放置時間が重要。術前消毒の成分としても使用可",
            },
            "cat": {
                "safe": True,
                "dosage": "Same formulation; lather and leave on 10 min, rinse. q3-7 days",
                "dosage_ja": "同製剤；泡立て10分放置後すすぐ。3-7日毎",
                "notes": "Safe for cats; effective for Malassezia and dermatophytosis adjunct therapy",
                "notes_ja": "猫に安全。マラセチア・皮膚糸状菌症の補助療法に有効",
            },
            "horse": {
                "safe": True,
                "dosage": "Apply to affected areas, lather 10 min, rinse. q3-7 days",
                "dosage_ja": "患部に塗布、10分泡立て放置後すすぐ。3-7日毎",
                "notes": "For dermatophilosis (rain scald), dermatophytosis",
                "notes_ja": "皮膚糸状菌症（レインスカルド）、白癬に",
            },
        },
        "side_effects": ["skin dryness (frequent bathing)", "rare contact irritation"],
        "side_effects_ja": ["皮膚乾燥（頻回入浴時）", "稀に接触性刺激"],
        "contraindications": "Known hypersensitivity to chlorhexidine or miconazole. Avoid contact with eyes and ears.",
        "contraindications_ja": "クロルヘキシジンまたはミコナゾール過敏症。目と耳への接触を避ける。",
    },
]

# ---------------------------------------------------------------------------
# Species-specific dosage patches for existing drugs (batch 6)
# ---------------------------------------------------------------------------
SPECIES_INFO_PATCH_6: dict[str, dict[str, dict]] = {
    # Trazodone – add ferret, rabbit
    "trazodone": {
        "ferret": {
            "safe": True,
            "dosage": "2-4 mg/kg PO q12-24h",
            "dosage_ja": "2-4 mg/kg 経口 12-24時間毎",
            "notes": "For anxiety; limited data, start low",
            "notes_ja": "不安に。データ限定的、低用量から開始",
        },
        "rabbit": {
            "safe": True,
            "dosage": "1-2 mg/kg PO q12-24h",
            "dosage_ja": "1-2 mg/kg 経口 12-24時間毎",
            "notes": "For peri-operative/transport anxiety; anecdotal use",
            "notes_ja": "周術期・輸送時不安に。経験的使用",
        },
    },
    # Tobramycin ophthalmic – add rabbit, bird
    "tobramycin_ophthalmic": {
        "rabbit": {
            "safe": True,
            "dosage": "1 drop affected eye q6-8h",
            "dosage_ja": "患眼に1滴 6-8時間毎",
            "notes": "For bacterial conjunctivitis/keratitis; good gram-negative coverage",
            "notes_ja": "細菌性結膜炎・角膜炎に。グラム陰性菌に良好な活性",
        },
        "bird": {
            "safe": True,
            "dosage": "1 drop affected eye q4-6h",
            "dosage_ja": "患眼に1滴 4-6時間毎",
            "notes": "For ocular infections in psittacines and raptors",
            "notes_ja": "オウム目・猛禽類の眼感染症に",
        },
    },
    # Budesonide – add rabbit, guinea_pig
    "budesonide": {
        "rabbit": {
            "safe": True,
            "dosage": "0.5-1 mg/rabbit PO q24h",
            "dosage_ja": "0.5-1 mg/匹 経口 24時間毎",
            "notes": "For IBD; first-pass metabolism limits systemic effects",
            "notes_ja": "IBDに。初回通過代謝で全身作用が限定的",
        },
        "guinea_pig": {
            "safe": True,
            "dosage": "0.5 mg/kg PO q24h",
            "dosage_ja": "0.5 mg/kg 経口 24時間毎",
            "notes": "For chronic GI inflammation; limited data",
            "notes_ja": "慢性消化管炎症に。データ限定的",
        },
    },
    # Oclacitinib – add rabbit
    "oclacitinib": {
        "rabbit": {
            "safe": True,
            "dosage": "0.4-1 mg/kg PO q12h x14d then q24h",
            "dosage_ja": "0.4-1 mg/kg 経口 12時間毎×14日後、24時間毎",
            "notes": "Anecdotal use for pruritic dermatitis in rabbits; monitor CBC",
            "notes_ja": "ウサギの瘙痒性皮膚炎に経験的使用。CBCモニター",
        },
    },
    # Lomustine – add rabbit
    "lomustine": {
        "rabbit": {
            "safe": True,
            "dosage": "40-50 mg/m² PO q3-4 weeks",
            "dosage_ja": "40-50 mg/m² 経口 3-4週毎",
            "notes": "For thymoma, lymphoma; monitor CBC and liver closely",
            "notes_ja": "胸腺腫・リンパ腫に。CBC・肝機能を厳密にモニター",
        },
    },
    # Maropitant – add hedgehog, bird
    "maropitant": {
        "hedgehog": {
            "safe": True,
            "dosage": "1 mg/kg SC q24h",
            "dosage_ja": "1 mg/kg 皮下 24時間毎",
            "notes": "Anti-emetic; limited data but dose extrapolated from small mammals",
            "notes_ja": "制吐薬。データ限定的だが小型哺乳類から用量外挿",
        },
        "bird": {
            "safe": True,
            "dosage": "2 mg/kg IM/SC q24h",
            "dosage_ja": "2 mg/kg 筋注/皮下 24時間毎",
            "notes": "Anti-emetic and visceral analgesic; emerging avian data",
            "notes_ja": "制吐・内臓鎮痛。鳥類のデータ増加中",
        },
    },
    # Benazepril – add ferret, rabbit
    "benazepril": {
        "ferret": {
            "safe": True,
            "dosage": "0.25-0.5 mg/kg PO q24h",
            "dosage_ja": "0.25-0.5 mg/kg 経口 24時間毎",
            "notes": "For cardiac disease and proteinuria; preferred ACEi in renal patients (hepatic elimination)",
            "notes_ja": "心疾患・蛋白尿に。腎疾患患者に推奨のACE阻害薬（肝排泄）",
        },
        "rabbit": {
            "safe": True,
            "dosage": "0.25-0.5 mg/kg PO q24h",
            "dosage_ja": "0.25-0.5 mg/kg 経口 24時間毎",
            "notes": "For cardiomyopathy and renal disease; limited rabbit data",
            "notes_ja": "心筋症・腎疾患に。ウサギのデータは限定的",
        },
    },
    # Insulin – add guinea_pig, rabbit
    "insulin_vetsulin": {
        "guinea_pig": {
            "safe": True,
            "dosage": "0.5-1 U/kg SC q12h (start 0.5, titrate)",
            "dosage_ja": "0.5-1 U/kg 皮下 12時間毎（0.5から開始、漸増）",
            "notes": "Diabetes rare in guinea pigs; monitor blood glucose closely",
            "notes_ja": "モルモットの糖尿病は稀。血糖値を厳密にモニター",
        },
        "rabbit": {
            "safe": True,
            "dosage": "0.5-2 U/kg SC q12h (titrate to glucose)",
            "dosage_ja": "0.5-2 U/kg 皮下 12時間毎（血糖値に応じて調整）",
            "notes": "For diabetes mellitus; very rare in rabbits",
            "notes_ja": "糖尿病に。ウサギでは極めて稀",
        },
    },
    # Ampicillin – add ferret, bird, rabbit
    "ampicillin": {
        "ferret": {
            "safe": True,
            "dosage": "10-20 mg/kg SC/IM/IV q8-12h",
            "dosage_ja": "10-20 mg/kg 皮下/筋注/静注 8-12時間毎",
            "notes": "Broad-spectrum; parenteral for serious infections",
            "notes_ja": "広域スペクトル。重症感染には注射剤",
        },
        "bird": {
            "safe": True,
            "dosage": "100-200 mg/kg IM q8-12h",
            "dosage_ja": "100-200 mg/kg 筋注 8-12時間毎",
            "notes": "High doses needed due to rapid avian metabolism",
            "notes_ja": "鳥類の代謝が速いため高用量が必要",
        },
        "rabbit": {
            "safe": True,
            "dosage": "15-30 mg/kg SC/IV q8-12h (parenteral only)",
            "dosage_ja": "15-30 mg/kg 皮下/静注 8-12時間毎（注射剤のみ）",
            "notes": "NEVER give oral ampicillin to rabbits — fatal dysbiosis. Parenteral only",
            "notes_ja": "経口アンピシリンはウサギに絶対禁忌（致死的腸内細菌叢異常）。注射剤のみ",
        },
    },
    # Marbofloxacin – add reptile, amphibian
    "marbofloxacin": {
        "reptile": {
            "safe": True,
            "dosage": "5-10 mg/kg PO/IM q24-48h",
            "dosage_ja": "5-10 mg/kg 経口/筋注 24-48時間毎",
            "notes": "Good gram-negative activity; adjust interval based on ambient temperature",
            "notes_ja": "グラム陰性菌に良好な活性。環境温度に応じて投与間隔を調整",
        },
        "amphibian": {
            "safe": True,
            "dosage": "5 mg/kg PO/bath q24h",
            "dosage_ja": "5 mg/kg 経口/薬浴 24時間毎",
            "notes": "For bacterial dermatosepticemia; bath route may improve absorption in aquatic species",
            "notes_ja": "細菌性皮膚敗血症に。水棲種では薬浴経路で吸収改善の可能性",
        },
    },
    # Terbinafine – add reptile
    "terbinafine": {
        "reptile": {
            "safe": True,
            "dosage": "10-15 mg/kg PO q24h for 14-42 days",
            "dosage_ja": "10-15 mg/kg 経口 24時間毎 14-42日間",
            "notes": "For systemic mycoses (Chrysosporium/CANV); long treatment courses needed. Good shell/skin penetration",
            "notes_ja": "全身性真菌症（Chrysosporium/CANV）に。長期治療が必要。甲羅/皮膚への移行良好",
        },
    },
    # Ketoconazole – add rabbit, guinea_pig
    "ketoconazole": {
        "rabbit": {
            "safe": True,
            "dosage": "10-40 mg/kg PO q24h",
            "dosage_ja": "10-40 mg/kg 経口 24時間毎",
            "notes": "For dermatophytosis; hepatotoxicity risk with prolonged use",
            "notes_ja": "皮膚糸状菌症に。長期使用で肝毒性リスク",
        },
        "guinea_pig": {
            "safe": True,
            "dosage": "10-40 mg/kg PO q24h for 14-28 days",
            "dosage_ja": "10-40 mg/kg 経口 24時間毎 14-28日間",
            "notes": "For Trichophyton ringworm; give with food for absorption",
            "notes_ja": "トリコフィトン白癬に。食事と投与で吸収向上",
        },
    },
}

# ---------------------------------------------------------------------------
# Drug interaction patches for existing drugs (batch 6)
# ---------------------------------------------------------------------------
DRUG_INTERACTIONS_PATCH_6: dict[str, list[dict]] = {
    "enrofloxacin": [
        {"drug": "theophylline", "effect": "Inhibits theophylline metabolism; risk of toxicity", "effect_ja": "テオフィリン代謝阻害。中毒リスク"},
        {"drug": "NSAIDs", "effect": "Increased seizure risk", "effect_ja": "痙攣リスク増加"},
        {"drug": "sucralfate", "effect": "Reduced absorption if given concurrently; separate by 2h", "effect_ja": "同時投与で吸収低下。2時間間隔を空ける"},
        {"drug": "cyclosporine", "effect": "Increased cyclosporine levels", "effect_ja": "シクロスポリン濃度上昇"},
    ],
    "metronidazole": [
        {"drug": "phenobarbital", "effect": "Increased metronidazole clearance", "effect_ja": "メトロニダゾールのクリアランス増加"},
        {"drug": "warfarin", "effect": "Enhanced anticoagulant effect", "effect_ja": "抗凝固作用の増強"},
        {"drug": "cyclosporine", "effect": "Increased cyclosporine levels", "effect_ja": "シクロスポリン濃度上昇"},
    ],
    "doxycycline": [
        {"drug": "antacids/sucralfate", "effect": "Chelation reduces absorption; separate by 2-3h", "effect_ja": "キレート化で吸収低下。2-3時間間隔を空ける"},
        {"drug": "phenobarbital", "effect": "Decreased doxycycline half-life", "effect_ja": "ドキシサイクリン半減期短縮"},
        {"drug": "methotrexate", "effect": "Increased methotrexate toxicity", "effect_ja": "メトトレキサート毒性増加"},
    ],
    "itraconazole": [
        {"drug": "cyclosporine", "effect": "Markedly increases cyclosporine levels; reduce dose by 50%", "effect_ja": "シクロスポリン濃度を著明に上昇。用量50%減量"},
        {"drug": "midazolam/diazepam", "effect": "Prolonged sedation via CYP3A4 inhibition", "effect_ja": "CYP3A4阻害で鎮静延長"},
        {"drug": "antacids/H2 blockers", "effect": "Reduced absorption (needs acidic pH)", "effect_ja": "吸収低下（酸性pHが必要）"},
        {"drug": "ivermectin", "effect": "Increased ivermectin levels; neurotoxicity risk", "effect_ja": "イベルメクチン濃度上昇。神経毒性リスク"},
    ],
    "ketoconazole": [
        {"drug": "cyclosporine", "effect": "Increases cyclosporine levels (used therapeutically to reduce dose)", "effect_ja": "シクロスポリン濃度上昇（用量削減目的で治療的併用あり）"},
        {"drug": "antacids/H2 blockers", "effect": "Reduced absorption (needs acidic pH)", "effect_ja": "吸収低下（酸性pHが必要）"},
        {"drug": "ivermectin", "effect": "Increased ivermectin levels via P-gp inhibition", "effect_ja": "P-gp阻害でイベルメクチン濃度上昇"},
    ],
    "fluconazole": [
        {"drug": "cyclosporine", "effect": "Increased cyclosporine levels", "effect_ja": "シクロスポリン濃度上昇"},
        {"drug": "phenobarbital", "effect": "Decreased fluconazole efficacy", "effect_ja": "フルコナゾール有効性低下"},
        {"drug": "warfarin", "effect": "Enhanced anticoagulant effect", "effect_ja": "抗凝固作用の増強"},
    ],
    "gentamicin": [
        {"drug": "furosemide", "effect": "Synergistic nephro/ototoxicity", "effect_ja": "腎毒性・耳毒性の相乗作用"},
        {"drug": "amphotericin_b", "effect": "Additive nephrotoxicity", "effect_ja": "腎毒性の相加作用"},
        {"drug": "neuromuscular blockers", "effect": "Potentiated neuromuscular blockade", "effect_ja": "神経筋遮断の増強"},
        {"drug": "NSAIDs", "effect": "Increased nephrotoxicity risk", "effect_ja": "腎毒性リスク増加"},
    ],
    "chloramphenicol": [
        {"drug": "phenobarbital", "effect": "Mutual interaction: chloramphenicol increases phenobarbital levels; phenobarbital decreases chloramphenicol levels", "effect_ja": "相互作用: クロラムフェニコールがフェノバルビタール濃度を上昇、フェノバルビタールがクロラムフェニコール濃度を低下"},
        {"drug": "cyclophosphamide", "effect": "Delayed metabolism of cyclophosphamide", "effect_ja": "シクロホスファミドの代謝遅延"},
    ],
    "meloxicam": [
        {"drug": "other NSAIDs", "effect": "Increased GI ulceration risk; never combine", "effect_ja": "消化管潰瘍リスク増加。絶対に併用しない"},
        {"drug": "corticosteroids", "effect": "Markedly increased GI ulceration risk", "effect_ja": "消化管潰瘍リスクが著明に増加"},
        {"drug": "furosemide", "effect": "Reduced diuretic efficacy; nephrotoxicity risk", "effect_ja": "利尿効果低下。腎毒性リスク"},
        {"drug": "ACE inhibitors", "effect": "Reduced antihypertensive effect; renal risk", "effect_ja": "降圧効果低下。腎リスク"},
    ],
    "gabapentin": [
        {"drug": "opioids", "effect": "Additive sedation and respiratory depression", "effect_ja": "鎮静・呼吸抑制の相加作用"},
        {"drug": "antacids", "effect": "Reduced gabapentin absorption by 20%", "effect_ja": "ガバペンチン吸収約20%低下"},
    ],
    "tramadol": [
        {"drug": "SSRIs/MAOIs", "effect": "Serotonin syndrome risk", "effect_ja": "セロトニン症候群リスク"},
        {"drug": "other opioids", "effect": "Additive CNS depression", "effect_ja": "中枢抑制の相加作用"},
        {"drug": "ondansetron", "effect": "May reduce tramadol analgesic efficacy", "effect_ja": "トラマドール鎮痛効果低下の可能性"},
    ],
    "phenobarbital": [
        {"drug": "chloramphenicol", "effect": "Increased phenobarbital levels", "effect_ja": "フェノバルビタール濃度上昇"},
        {"drug": "doxycycline", "effect": "Decreased doxycycline half-life", "effect_ja": "ドキシサイクリン半減期短縮"},
        {"drug": "cyclosporine", "effect": "Decreased cyclosporine levels", "effect_ja": "シクロスポリン濃度低下"},
        {"drug": "corticosteroids", "effect": "Increased steroid metabolism", "effect_ja": "ステロイド代謝促進"},
        {"drug": "metronidazole", "effect": "Increased metronidazole clearance", "effect_ja": "メトロニダゾールクリアランス増加"},
    ],
    "cyclosporine": [
        {"drug": "ketoconazole/itraconazole", "effect": "Markedly increases cyclosporine levels (used therapeutically)", "effect_ja": "シクロスポリン濃度を著明に上昇（治療的に利用）"},
        {"drug": "phenobarbital", "effect": "Decreased cyclosporine levels", "effect_ja": "シクロスポリン濃度低下"},
        {"drug": "NSAIDs", "effect": "Additive nephrotoxicity", "effect_ja": "腎毒性の相加作用"},
        {"drug": "metoclopramide", "effect": "Increased cyclosporine absorption", "effect_ja": "シクロスポリン吸収増加"},
    ],
    "furosemide": [
        {"drug": "aminoglycosides", "effect": "Synergistic ototoxicity and nephrotoxicity", "effect_ja": "耳毒性・腎毒性の相乗作用"},
        {"drug": "ACE inhibitors", "effect": "Risk of hypotension; start ACEi at low dose", "effect_ja": "低血圧リスク。ACE阻害薬は低用量から開始"},
        {"drug": "NSAIDs", "effect": "Reduced diuretic efficacy", "effect_ja": "利尿効果の低下"},
        {"drug": "digoxin", "effect": "Hypokalemia potentiates digoxin toxicity", "effect_ja": "低カリウム血症でジゴキシン毒性増強"},
    ],
    "digoxin": [
        {"drug": "furosemide", "effect": "Hypokalemia increases digoxin toxicity risk", "effect_ja": "低カリウム血症でジゴキシン毒性リスク増加"},
        {"drug": "metoclopramide", "effect": "Reduced digoxin absorption", "effect_ja": "ジゴキシン吸収低下"},
        {"drug": "amiodarone", "effect": "Doubled digoxin levels; reduce digoxin dose by 50%", "effect_ja": "ジゴキシン濃度が2倍に。ジゴキシン用量50%減量"},
        {"drug": "verapamil/diltiazem", "effect": "Increased digoxin levels and additive bradycardia", "effect_ja": "ジゴキシン濃度上昇と徐脈の相加作用"},
    ],
    "omeprazole": [
        {"drug": "ketoconazole/itraconazole", "effect": "Reduced absorption of azole antifungals (need acidic pH)", "effect_ja": "アゾール系抗真菌薬の吸収低下（酸性pHが必要）"},
        {"drug": "clopidogrel", "effect": "May reduce clopidogrel activation via CYP2C19 inhibition", "effect_ja": "CYP2C19阻害でクロピドグレル活性化低下の可能性"},
        {"drug": "sucralfate", "effect": "Give omeprazole 30 min before sucralfate", "effect_ja": "オメプラゾールをスクラルファートの30分前に投与"},
    ],
    "sucralfate": [
        {"drug": "fluoroquinolones", "effect": "Chelation reduces FQ absorption by 50-70%; separate by 2h", "effect_ja": "キレート化でFQ吸収50-70%低下。2時間間隔を空ける"},
        {"drug": "doxycycline", "effect": "Reduced doxycycline absorption; separate by 2-3h", "effect_ja": "ドキシサイクリン吸収低下。2-3時間間隔を空ける"},
        {"drug": "digoxin", "effect": "Reduced digoxin absorption", "effect_ja": "ジゴキシン吸収低下"},
        {"drug": "levothyroxine", "effect": "Reduced thyroid hormone absorption; separate by 2h", "effect_ja": "甲状腺ホルモン吸収低下。2時間間隔を空ける"},
    ],
    "metoclopramide": [
        {"drug": "opioids", "effect": "Antagonistic on GI motility", "effect_ja": "消化管運動に対して拮抗"},
        {"drug": "phenothiazines", "effect": "Additive extrapyramidal effects", "effect_ja": "錐体外路症状の相加作用"},
        {"drug": "cyclosporine", "effect": "Increased cyclosporine absorption", "effect_ja": "シクロスポリン吸収増加"},
    ],
    "cisapride": [
        {"drug": "ketoconazole/itraconazole", "effect": "Increased cisapride levels; risk of cardiac arrhythmia (QT prolongation)", "effect_ja": "シサプリド濃度上昇。心不整脈リスク（QT延長）"},
        {"drug": "erythromycin", "effect": "Increased cisapride levels via CYP3A4 inhibition; arrhythmia risk", "effect_ja": "CYP3A4阻害でシサプリド濃度上昇。不整脈リスク"},
    ],
    "amlodipine": [
        {"drug": "ACE inhibitors", "effect": "Additive hypotension (often used together therapeutically)", "effect_ja": "低血圧の相加作用（治療的に併用されることが多い）"},
        {"drug": "cyclosporine", "effect": "Increased cyclosporine levels", "effect_ja": "シクロスポリン濃度上昇"},
    ],
    "pimobendan": [
        {"drug": "beta-blockers", "effect": "May partially antagonize inotropic effect", "effect_ja": "強心作用を部分的に拮抗する可能性"},
        {"drug": "verapamil/diltiazem", "effect": "Additive negative chronotropic effects; use cautiously", "effect_ja": "陰性変時作用の相加。慎重に使用"},
    ],
    "acepromazine": [
        {"drug": "opioids", "effect": "Additive sedation and hypotension", "effect_ja": "鎮静・低血圧の相加作用"},
        {"drug": "epinephrine", "effect": "Reversed pressor response (epinephrine reversal); use norepinephrine instead", "effect_ja": "昇圧反応の逆転（エピネフリン逆転）。ノルエピネフリンを代わりに使用"},
        {"drug": "organophosphates", "effect": "Potentiated toxicity", "effect_ja": "毒性増強"},
    ],
    "dexmedetomidine": [
        {"drug": "opioids", "effect": "Synergistic sedation; dose reduction of both drugs recommended", "effect_ja": "鎮静の相乗作用。両薬の用量削減を推奨"},
        {"drug": "ketamine", "effect": "Commonly combined; balanced anesthesia protocol", "effect_ja": "頻繁に併用。バランス麻酔プロトコル"},
        {"drug": "other alpha-2 agonists", "effect": "Do not combine; additive cardiovascular depression", "effect_ja": "併用不可。心血管系抑制の相加作用"},
    ],
    "ivermectin": [
        {"drug": "ketoconazole/itraconazole", "effect": "Increased ivermectin levels via P-gp/CYP3A4 inhibition; neurotoxicity risk", "effect_ja": "P-gp/CYP3A4阻害でイベルメクチン濃度上昇。神経毒性リスク"},
        {"drug": "spinosad", "effect": "Increased ivermectin toxicity; do not combine with high-dose ivermectin", "effect_ja": "イベルメクチン毒性増加。高用量イベルメクチンとの併用不可"},
    ],
    "clindamycin": [
        {"drug": "erythromycin/azithromycin", "effect": "Antagonistic binding at same ribosomal site; do not combine", "effect_ja": "同一リボソーム部位での拮抗結合。併用不可"},
        {"drug": "neuromuscular blockers", "effect": "Potentiated neuromuscular blockade", "effect_ja": "神経筋遮断の増強"},
    ],
    "azithromycin": [
        {"drug": "clindamycin", "effect": "Antagonistic ribosomal binding; do not combine", "effect_ja": "リボソーム結合の拮抗。併用不可"},
        {"drug": "cyclosporine", "effect": "Increased cyclosporine levels", "effect_ja": "シクロスポリン濃度上昇"},
        {"drug": "digoxin", "effect": "Increased digoxin levels", "effect_ja": "ジゴキシン濃度上昇"},
    ],
    "prednisolone": [
        {"drug": "NSAIDs", "effect": "Markedly increased GI ulceration risk; avoid concurrent use", "effect_ja": "消化管潰瘍リスクが著明に増加。併用を避ける"},
        {"drug": "insulin", "effect": "Antagonizes insulin effect; may require dose increase", "effect_ja": "インスリン効果を拮抗。増量が必要な場合あり"},
        {"drug": "furosemide", "effect": "Additive hypokalemia", "effect_ja": "低カリウム血症の相加作用"},
        {"drug": "phenobarbital", "effect": "Increased steroid metabolism; may need higher dose", "effect_ja": "ステロイド代謝促進。増量が必要な場合あり"},
    ],
    "dexamethasone": [
        {"drug": "NSAIDs", "effect": "Markedly increased GI ulceration risk", "effect_ja": "消化管潰瘍リスクが著明に増加"},
        {"drug": "insulin", "effect": "Antagonizes insulin effect", "effect_ja": "インスリン効果を拮抗"},
        {"drug": "phenobarbital", "effect": "Increased dexamethasone clearance", "effect_ja": "デキサメタゾンのクリアランス増加"},
        {"drug": "furosemide", "effect": "Additive hypokalemia", "effect_ja": "低カリウム血症の相加作用"},
    ],
    "carprofen": [
        {"drug": "other NSAIDs", "effect": "Never combine; marked GI ulceration risk", "effect_ja": "絶対に併用しない。消化管潰瘍リスクの著明な増加"},
        {"drug": "corticosteroids", "effect": "Increased GI ulceration risk; 5-day washout recommended", "effect_ja": "消化管潰瘍リスク増加。5日間の休薬期間を推奨"},
        {"drug": "ACE inhibitors", "effect": "Reduced antihypertensive effect; renal risk", "effect_ja": "降圧効果低下。腎リスク"},
        {"drug": "furosemide", "effect": "Reduced diuretic efficacy", "effect_ja": "利尿効果低下"},
    ],
    "firocoxib": [
        {"drug": "other NSAIDs", "effect": "Never combine; increased GI/renal toxicity", "effect_ja": "絶対に併用しない。消化管/腎毒性増加"},
        {"drug": "corticosteroids", "effect": "Increased GI ulceration risk", "effect_ja": "消化管潰瘍リスク増加"},
        {"drug": "ACE inhibitors", "effect": "Reduced renal blood flow", "effect_ja": "腎血流低下"},
    ],
    "butorphanol": [
        {"drug": "pure mu agonists", "effect": "Partial antagonism of morphine/fentanyl analgesia", "effect_ja": "モルヒネ/フェンタニルの鎮痛を部分的に拮抗"},
        {"drug": "alpha-2 agonists", "effect": "Synergistic sedation (commonly combined)", "effect_ja": "鎮静の相乗作用（頻繁に併用）"},
        {"drug": "other CNS depressants", "effect": "Additive CNS/respiratory depression", "effect_ja": "中枢/呼吸抑制の相加作用"},
    ],
    "buprenorphine": [
        {"drug": "pure mu agonists", "effect": "May partially antagonize full mu agonist analgesia", "effect_ja": "完全μ作動薬の鎮痛を部分的に拮抗する可能性"},
        {"drug": "other CNS depressants", "effect": "Additive sedation and respiratory depression", "effect_ja": "鎮静・呼吸抑制の相加作用"},
        {"drug": "MAOIs", "effect": "Potentially fatal interaction; avoid", "effect_ja": "致死的な相互作用の可能性。避ける"},
    ],
    "ketamine": [
        {"drug": "alpha-2 agonists", "effect": "Synergistic sedation/analgesia; commonly combined", "effect_ja": "鎮静/鎮痛の相乗作用。頻繁に併用"},
        {"drug": "benzodiazepines", "effect": "Smooth induction/recovery; commonly combined", "effect_ja": "滑らかな導入/覚醒。頻繁に併用"},
        {"drug": "chloramphenicol", "effect": "Prolonged ketamine effect (inhibits metabolism)", "effect_ja": "ケタミン効果延長（代謝阻害）"},
    ],
    "diazepam": [
        {"drug": "other CNS depressants", "effect": "Additive sedation and respiratory depression", "effect_ja": "鎮静・呼吸抑制の相加作用"},
        {"drug": "ketoconazole/itraconazole", "effect": "Prolonged sedation via CYP3A4 inhibition", "effect_ja": "CYP3A4阻害で鎮静延長"},
        {"drug": "phenobarbital", "effect": "Enhanced CNS depression", "effect_ja": "中枢抑制の増強"},
    ],
    "insulin_vetsulin": [
        {"drug": "corticosteroids", "effect": "Antagonize insulin effect; may need dose increase", "effect_ja": "インスリン効果を拮抗。用量増加が必要な場合あり"},
        {"drug": "thiazide diuretics", "effect": "Hyperglycemic effect; may increase insulin requirement", "effect_ja": "高血糖作用。インスリン必要量増加の可能性"},
        {"drug": "beta-blockers", "effect": "May mask hypoglycemia signs (tachycardia)", "effect_ja": "低血糖兆候（頻脈）を隠蔽する可能性"},
    ],
    "methimazole": [
        {"drug": "warfarin", "effect": "Altered anticoagulant effect as thyroid status changes", "effect_ja": "甲状腺状態の変化に伴い抗凝固作用が変動"},
        {"drug": "digoxin", "effect": "Digoxin levels change with thyroid normalization", "effect_ja": "甲状腺機能正常化に伴いジゴキシン濃度が変動"},
    ],
    "trilostane": [
        {"drug": "ACE inhibitors", "effect": "Additive aldosterone suppression; hyperkalemia risk", "effect_ja": "アルドステロン抑制の相加作用。高カリウム血症リスク"},
        {"drug": "potassium-sparing diuretics", "effect": "Risk of life-threatening hyperkalemia", "effect_ja": "生命を脅かす高カリウム血症のリスク"},
        {"drug": "ketoconazole", "effect": "Additive adrenal suppression", "effect_ja": "副腎抑制の相加作用"},
    ],
    "enalapril": [
        {"drug": "NSAIDs", "effect": "Reduced antihypertensive effect; increased renal risk", "effect_ja": "降圧効果低下。腎リスク増加"},
        {"drug": "potassium-sparing diuretics", "effect": "Risk of hyperkalemia", "effect_ja": "高カリウム血症リスク"},
        {"drug": "furosemide", "effect": "First-dose hypotension; start ACEi low", "effect_ja": "初回投与時低血圧。ACE阻害薬は低用量から開始"},
    ],
    "benazepril": [
        {"drug": "NSAIDs", "effect": "Reduced antihypertensive effect; increased renal risk", "effect_ja": "降圧効果低下。腎リスク増加"},
        {"drug": "potassium-sparing diuretics", "effect": "Risk of hyperkalemia", "effect_ja": "高カリウム血症リスク"},
        {"drug": "furosemide", "effect": "First-dose hypotension; start ACEi low", "effect_ja": "初回投与時低血圧。ACE阻害薬は低用量から開始"},
    ],
    "amoxicillin": [
        {"drug": "methotrexate", "effect": "Reduced methotrexate clearance; toxicity risk", "effect_ja": "メトトレキサートクリアランス低下。毒性リスク"},
        {"drug": "allopurinol", "effect": "Increased risk of skin rash", "effect_ja": "皮疹リスク増加"},
    ],
    "amoxicillin_clavulanate": [
        {"drug": "methotrexate", "effect": "Reduced methotrexate clearance; toxicity risk", "effect_ja": "メトトレキサートクリアランス低下。毒性リスク"},
        {"drug": "allopurinol", "effect": "Increased risk of skin rash", "effect_ja": "皮疹リスク増加"},
    ],
    "trimethoprim_sulfa": [
        {"drug": "ACE inhibitors", "effect": "Risk of hyperkalemia (trimethoprim acts like K-sparing diuretic)", "effect_ja": "高カリウム血症リスク（トリメトプリムがK保持性利尿薬様に作用）"},
        {"drug": "warfarin", "effect": "Enhanced anticoagulant effect", "effect_ja": "抗凝固作用の増強"},
        {"drug": "methotrexate", "effect": "Additive folate antagonism; increased toxicity", "effect_ja": "葉酸拮抗の相加作用。毒性増加"},
        {"drug": "phenytoin", "effect": "Increased phenytoin levels", "effect_ja": "フェニトイン濃度上昇"},
    ],
    "ondansetron": [
        {"drug": "tramadol", "effect": "May reduce tramadol analgesic efficacy", "effect_ja": "トラマドール鎮痛効果低下の可能性"},
        {"drug": "apomorphine", "effect": "Blocks emetic effect of apomorphine", "effect_ja": "アポモルフィンの催吐効果を遮断"},
        {"drug": "QT-prolonging drugs", "effect": "Additive QT prolongation risk", "effect_ja": "QT延長リスクの相加作用"},
    ],
    "famotidine": [
        {"drug": "ketoconazole/itraconazole", "effect": "Reduced azole absorption (need acidic pH)", "effect_ja": "アゾール系吸収低下（酸性pHが必要）"},
        {"drug": "sucralfate", "effect": "Reduced famotidine absorption; separate by 2h", "effect_ja": "ファモチジン吸収低下。2時間間隔を空ける"},
    ],
    "mannitol": [
        {"drug": "furosemide", "effect": "Additive diuresis; risk of dehydration/electrolyte imbalance", "effect_ja": "利尿の相加作用。脱水/電解質異常のリスク"},
        {"drug": "lithium", "effect": "Increased lithium clearance", "effect_ja": "リチウムクリアランス増加"},
    ],
    "levetiracetam": [
        {"drug": "phenobarbital", "effect": "Commonly combined; may slightly increase clearance", "effect_ja": "頻繁に併用。クリアランスがやや増加する可能性"},
        {"drug": "potassium_bromide", "effect": "Can be combined safely for multi-drug seizure control", "effect_ja": "多剤てんかん管理で安全に併用可能"},
    ],
    "sildenafil": [
        {"drug": "nitrates", "effect": "Severe life-threatening hypotension; absolutely contraindicated", "effect_ja": "重度の生命を脅かす低血圧。絶対禁忌"},
        {"drug": "alpha-blockers", "effect": "Additive hypotension", "effect_ja": "低血圧の相加作用"},
        {"drug": "bosentan", "effect": "Bosentan reduces sildenafil levels; may combine with dose adjustment", "effect_ja": "ボセンタンがシルデナフィル濃度を低下。用量調整で併用可"},
    ],
    "clopidogrel": [
        {"drug": "omeprazole", "effect": "May reduce clopidogrel activation; use famotidine instead", "effect_ja": "クロピドグレル活性化低下の可能性。ファモチジンを代わりに使用"},
        {"drug": "NSAIDs", "effect": "Increased bleeding risk", "effect_ja": "出血リスク増加"},
        {"drug": "aspirin", "effect": "Additive antiplatelet effect (sometimes used together for ATE in cats)", "effect_ja": "抗血小板作用の相加（猫のATEで併用されることあり）"},
    ],
    "ampicillin": [
        {"drug": "aminoglycosides", "effect": "Synergistic antibacterial effect but do not mix in same syringe (inactivation)", "effect_ja": "抗菌作用の相乗効果だが同一シリンジで混合不可（失活）"},
        {"drug": "allopurinol", "effect": "Increased risk of skin rash", "effect_ja": "皮疹リスク増加"},
    ],
    "lactulose": [
        {"drug": "antacids", "effect": "May reduce lactulose efficacy by altering colonic pH", "effect_ja": "結腸pHの変化でラクツロース有効性低下の可能性"},
        {"drug": "neomycin", "effect": "May reduce lactulose efficacy (kills bacteria needed for metabolism)", "effect_ja": "代謝に必要な細菌を殺すためラクツロース有効性低下の可能性"},
    ],
}
