"""Drug batch 36 – referenced-but-absent agents surfaced by the 2026-08 audit (4th sweep).

A katakana token-frequency sweep of disease treatment protocols found that
enoxaparin — the low-molecular-weight heparin VetDict's own DIC and
thromboembolism protocols instruct clinicians to use, with explicit doses, in
13 disease entries across dog/cat/rabbit/rodents/ferret/hedgehog/bird — was
absent from the formulary (only unfractionated heparin and dalteparin were
carried).

References:
  - Plumb's Veterinary Drug Handbook, 10th ed — enoxaparin canine/feline dosing.
  - Lunsford KV et al. J Vet Intern Med 2009;23(3):598-602 — canine enoxaparin
    pharmacodynamics: 0.8 mg/kg SC q6h needed to sustain anti-Xa targets.
  - Alwood AJ et al. J Vet Intern Med 2007;21(3):378-387 — feline enoxaparin
    1.25 mg/kg SC q6h based on anti-Xa activity.
  - Feige K et al. J Vet Intern Med 2003 / Equine Vet J — LMWH (enoxaparin
    40-80 anti-Xa IU/kg SC q24h) vs UFH for jugular thrombosis/laminitis
    prophylaxis in colic horses; fewer bleeding complications than UFH.
  - Carpenter's Exotic Animal Formulary, 6th ed — empirical small-mammal LMWH
    dosing.
"""

DRUGS_BATCH_36: list[dict] = [
    {
        "id": "enoxaparin",
        "search_aliases": ["エノキサパリン", "クレキサン", "Lovenox"],
        "name": "Enoxaparin (Lovenox)",
        "name_ja": "エノキサパリン（クレキサン）",
        "category": "anticoagulants",
        "mechanism": "Low-molecular-weight heparin. Potentiates antithrombin III with preferential inhibition of factor Xa over thrombin (anti-Xa:anti-IIa ≈ 3-4:1), giving a more predictable dose-response than unfractionated heparin with minimal aPTT prolongation — efficacy is monitored by anti-Xa activity, not aPTT.",
        "mechanism_ja": "低分子量ヘパリン。アンチトロンビンIIIを介して第Xa因子をトロンビンより優先的に阻害（抗Xa:抗IIa比 約3-4:1）。未分画ヘパリンより用量反応が予測しやすく、aPTT延長はごく軽度 — 効果判定はaPTTではなく抗Xa活性で行う。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.8 mg/kg SC q6h (anti-Xa target 0.5-1.0 IU/mL); 0.8-1 mg/kg SC q12h has been used empirically in DIC with close monitoring.",
                "dosage_ja": "0.8 mg/kg 皮下 6時間毎（抗Xa目標 0.5-1.0 IU/mL）。DICでは経験的に0.8-1 mg/kg 皮下 12時間毎も用いられる（厳密モニタリング下）。",
                "notes": "Canine pharmacodynamics (Lunsford 2009) show q6h dosing is required to sustain anti-Xa targets — once-daily human regimens underdose dogs. For PTE/hypercoagulable states; transition to clopidogrel for long-term maintenance.",
                "notes_ja": "犬の薬力学（Lunsford 2009）ではヒトの1日1回投与では不十分で、抗Xa目標維持にq6hが必要。肺血栓塞栓症・過凝固状態に使用し、長期維持はクロピドグレルへ移行。",
            },
            "cat": {
                "safe": True,
                "dosage": "1.25 mg/kg SC q6h (anti-Xa-based; Alwood 2007). 1 mg/kg SC q12h used empirically for lower-risk prophylaxis.",
                "dosage_ja": "1.25 mg/kg 皮下 6時間毎（抗Xa活性準拠、Alwood 2007）。低リスク予防では経験的に1 mg/kg 皮下 12時間毎。",
                "notes": "For aortic thromboembolism (ATE) adjunct/prophylaxis. Clopidogrel is first-line for long-term ATE prevention (FATCAT); LMWH is used acutely or when antiplatelet therapy alone is insufficient.",
                "notes_ja": "大動脈血栓塞栓症（ATE）の急性期補助・予防に使用。長期のATE再発予防はクロピドグレルが第一選択（FATCAT試験）。LMWHは急性期または抗血小板薬単独で不十分な場合に併用。",
            },
            "horse": {
                "safe": True,
                "dosage": "40-80 anti-Xa IU/kg (≈0.35-0.9 mg/kg) SC q24h.",
                "dosage_ja": "40-80 抗Xa IU/kg（約0.35-0.9 mg/kg）皮下 24時間毎。",
                "notes": "Jugular thrombosis / laminitis prophylaxis in colic and SIRS; fewer bleeding and injection-site complications than unfractionated heparin (Feige 2003).",
                "notes_ja": "疝痛・SIRS症例の頸静脈血栓・蹄葉炎予防。未分画ヘパリンより出血・注射部位合併症が少ない（Feige 2003）。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.8-1 mg/kg SC q12h (empirical; anti-Xa monitoring recommended where available).",
                "dosage_ja": "0.8-1 mg/kg 皮下 12時間毎（経験的。可能であれば抗Xaモニタリング推奨）。",
                "notes": "Thromboembolism / hypercoagulable-phase DIC. Contraindicated in the hypocoagulable (bleeding) phase of DIC.",
                "notes_ja": "血栓塞栓症・DIC過凝固期に使用。DIC低凝固期（出血期）は禁忌。",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.8-1 mg/kg SC q12h (empirical, extrapolated).",
                "dosage_ja": "0.8-1 mg/kg 皮下 12時間毎（経験的・外挿）。",
                "notes": "Small-mammal dosing is extrapolated; weigh thrombosis risk against bleeding risk in each case.",
                "notes_ja": "小型哺乳類の用量は外挿。症例毎に血栓リスクと出血リスクを慎重に比較考量。",
            },
            "bird": {
                "safe": True,
                "dosage": "0.75-1 mg/kg SC q12h (limited evidence).",
                "dosage_ja": "0.75-1 mg/kg 皮下 12時間毎（エビデンス限定的）。",
                "notes": "Avian coagulation differs from mammals (short RBC lifespan, thrombocytes); monitor closely and reassess need daily.",
                "notes_ja": "鳥類の凝固系は哺乳類と異なる（赤血球寿命が短い・栓球）。厳密にモニタリングし、必要性を毎日再評価。",
            },
        },
        "side_effects": "Bleeding, injection-site bruising/pain, thrombocytopenia (rare)",
        "side_effects_ja": "出血、注射部位の紫斑・疼痛、血小板減少（稀）",
        "contraindications": "Active hemorrhage, hypocoagulable (bleeding) phase of DIC, severe thrombocytopenia. Protamine only partially (~60%) reverses LMWH anti-Xa activity.",
        "contraindications_ja": "活動性出血、DIC低凝固期（出血期）、重度の血小板減少。プロタミンはLMWHの抗Xa活性を部分的（約60%）にしか中和できない点に注意。",
        "drug_interactions": [
            {"drug": "NSAIDs", "effect": "Increased bleeding risk", "severity": "major"},
            {
                "drug": "Aspirin",
                "effect": "Additive bleeding risk (antiplatelet + anticoagulant)",
                "severity": "major",
            },
            {
                "drug": "Clopidogrel",
                "effect": "Additive bleeding risk; combination used intentionally in high-risk ATE with close monitoring",
                "severity": "moderate",
            },
            {
                "drug": "Other anticoagulants",
                "effect": "Additive bleeding risk",
                "severity": "major",
            },
        ],
    },
]
