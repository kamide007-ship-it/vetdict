"""Drug batch 79 – 2026-10 第71弾.

1. Apixaban (Eliquis) — oral direct factor Xa inhibitor listed alongside
   rivaroxaban as a DOAC option in the ACVECC CURATIVE consensus (Blais
   2019) for dogs and cats with thrombotic risk (feline ATE secondary
   prevention, canine IMHA/PLN/PTE). Rivaroxaban was present but its
   sister DOAC was absent, so the cat ATE / canine PTE entries had no
   apixaban option.
2. Credelio Plus (lotilaner + milbemycin oxime) — EU-authorised (EMA 2021,
   Elanco) monthly chewable for dogs: fleas/ticks plus heartworm
   prevention and roundworm/hookworm/whipworm/lungworm treatment.

Evidence:
  - Blais MC et al. Consensus on the Rational Use of Antithrombotics in
    Veterinary Critical Care (CURATIVE): Domain 3. JVECC 2019;29:60-74.
  - Myers JA et al. Pharmacokinetics and pharmacodynamics of apixaban in
    healthy cats. AJVR 2015.
  - Credelio Plus EPAR / SPC (EMA, Elanco Animal Health, 2021).
"""

DRUGS_BATCH_79 = [
    {
        "id": "apixaban",
        "search_aliases": ["アピキサバン", "エリキュース", "Eliquis", "apixaban"],
        "name": "Apixaban (Eliquis)",
        "name_ja": "アピキサバン（エリキュース）",
        "category": "anticoagulants",
        "mechanism": "Direct, reversible inhibitor of free and clot-bound factor Xa (direct oral anticoagulant, DOAC). Does not require antithrombin and needs no routine aPTT monitoring; anti-Xa activity can be measured if available.",
        "mechanism_ja": "遊離型・血栓結合型の第Xa因子を直接かつ可逆的に阻害する直接経口抗凝固薬（DOAC）。アンチトロンビン非依存で、通常 aPTT モニタリングは不要（測定可能なら抗Xa活性で評価）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5 mg/kg PO q12h (CURATIVE consensus range 0.5 mg/kg q12-24h) for thromboprophylaxis in dogs at risk (IMHA, protein-losing nephropathy/enteropathy, PTE, hyperadrenocorticism with thrombosis). Rivaroxaban 1-2 mg/kg q24h has more canine data and is the usual first DOAC choice.",
                "dosage_ja": "0.5 mg/kg PO q12h（CURATIVE コンセンサス範囲 0.5 mg/kg q12-24h）— 血栓リスクのある犬（IMHA・蛋白漏出性腎症/腸症・肺血栓塞栓症・血栓を伴うクッシング症候群）の血栓予防。犬のデータはリバーロキサバン（1-2 mg/kg q24h）の方が多く、DOACの第一候補は通常そちら。",
                "notes": "Off-label (human drug). Bleeding risk rises with concurrent anticoagulants/antiplatelets. Hepatically cleared with a renal component — reduce or avoid in severe hepatic disease.",
                "notes_ja": "適応外使用（ヒト用医薬品）。他の抗凝固薬・抗血小板薬との併用で出血リスク上昇。肝代謝（一部腎排泄）— 重度肝疾患では減量または回避。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.625 mg/cat PO q12h (≈1/4 of a 2.5 mg tablet; CURATIVE consensus) as an alternative DOAC for secondary prevention after aortic thromboembolism or in cats with HCM and a high-risk left atrium. Clopidogrel 18.75 mg/cat q24h remains first-line (FATCAT); a DOAC may be added or substituted in high-risk cats.",
                "dosage_ja": "0.625 mg/頭 PO q12h（2.5 mg錠の約1/4、CURATIVE コンセンサス）— 動脈血栓塞栓症（ATE）後の再発予防、または高リスク左房を伴うHCM猫の代替DOAC。第一選択は引き続きクロピドグレル 18.75 mg/頭 q24h（FATCAT試験）で、高リスク猫ではDOACを追加または代替する。",
                "notes": "Off-label; clinical outcome data in cats are limited (pharmacokinetic/pharmacodynamic studies — Myers 2015). Splitting tablets: give consistently. Monitor for bleeding (melena, hematuria, epistaxis).",
                "notes_ja": "適応外使用。猫の臨床転帰データは限定的（薬物動態・薬力学研究 — Myers 2015）。錠剤分割は一定量で継続。出血徴候（黒色便・血尿・鼻出血）を監視。",
            },
        },
        "contraindications": "Active bleeding or coagulopathy, severe thrombocytopenia, severe hepatic disease. Do not combine with another therapeutic-dose anticoagulant (heparin, LMWH, rivaroxaban) except during a planned switch.",
        "contraindications_ja": "活動性出血・凝固障害・重度血小板減少・重度肝疾患。計画的な切替時を除き、他の治療量抗凝固薬（ヘパリン・低分子ヘパリン・リバーロキサバン）と併用しない。",
        "side_effects": ["Bleeding (gastrointestinal, urinary, epistaxis)", "Vomiting or inappetence (uncommon)"],
        "side_effects_ja": ["出血（消化管・尿路・鼻出血）", "嘔吐・食欲低下（まれ）"],
        "drug_interactions": [
            {
                "drug": "Rivaroxaban",
                "effect": "Duplicate factor-Xa inhibition — do not combine; additive bleeding.",
                "effect_ja": "第Xa因子阻害の重複 — 併用しない（出血の相加）。",
                "severity": "major",
            },
            {
                "drug": "Heparin / Enoxaparin / Dalteparin",
                "effect": "Additive anticoagulation — only overlap during a planned switch.",
                "effect_ja": "抗凝固作用の相加 — 計画的な切替時以外は重ねない。",
                "severity": "major",
            },
            {
                "drug": "Clopidogrel / Aspirin",
                "effect": "Combined antiplatelet + anticoagulant therapy increases bleeding; reserve for high-risk cases with monitoring.",
                "effect_ja": "抗血小板薬との併用で出血リスク上昇 — 高リスク症例に限定し監視下で。",
                "severity": "moderate",
            },
            {
                "drug": "NSAIDs",
                "effect": "Increased gastrointestinal bleeding risk.",
                "effect_ja": "消化管出血リスクの上昇。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Blais MC et al. Consensus on the Rational Use of Antithrombotics in Veterinary Critical Care (CURATIVE): Domain 3. J Vet Emerg Crit Care 2019;29:60-74.",
            "Myers JA et al. Pharmacokinetics and pharmacodynamics of apixaban in healthy cats. Am J Vet Res 2015.",
            "Hogan DF et al. Secondary prevention of cardiogenic arterial thromboembolism in the cat (FATCAT). J Vet Cardiol 2015;17:S306-S317.",
        ],
    },
    {
        "id": "lotilaner_milbemycin",
        "search_aliases": [
            "クレデリオプラス",
            "クレデリオ プラス",
            "Credelio Plus",
            "credelio plus",
            "ロチラネル・ミルベマイシンオキシム",
        ],
        "name": "Lotilaner + Milbemycin Oxime (Credelio Plus)",
        "name_ja": "ロチラネル・ミルベマイシンオキシム（クレデリオプラス）",
        "category": "antiparasitic",
        "mechanism": "Lotilaner (isoxazoline) blocks insect/acarine GABA-gated chloride channels — fleas and ticks; milbemycin oxime (macrocyclic lactone) opens glutamate-gated chloride channels — heartworm (L3/L4) prevention and nematode treatment.",
        "mechanism_ja": "ロチラネル（イソキサゾリン系）は昆虫・ダニのGABA作動性クロライドチャネルを遮断しノミ・マダニを駆除。ミルベマイシンオキシム（大環状ラクトン）はグルタミン酸作動性クロライドチャネルを開口し、犬糸状虫（L3/L4幼虫）予防と線虫駆除を担う。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Monthly chewable with food: lotilaner 20-41 mg/kg + milbemycin oxime 0.75-1.53 mg/kg (minimum 20 / 0.75 mg/kg; EU label). Dogs ≥8 weeks and ≥1.4 kg. Fleas and ticks for 1 month, heartworm prevention when given monthly, and treatment of roundworm, hookworm, whipworm and lungworm (Angiostrongylus vasorum) infections.",
                "dosage_ja": "月1回、食事と共に経口: ロチラネル 20-41 mg/kg ＋ ミルベマイシンオキシム 0.75-1.53 mg/kg（最低 20 / 0.75 mg/kg、EUラベル）。8週齢以上・体重1.4 kg以上。ノミ・マダニを1ヶ月駆除、毎月投与で犬糸状虫予防、回虫・鉤虫・鞭虫・肺虫（Angiostrongylus vasorum）の駆除。",
                "notes": "Confirm heartworm-negative status before starting. Isoxazoline class warning — neurological adverse events (tremor, ataxia, seizures) reported; use with caution in dogs with a seizure history. Milbemycin at preventive dose is tolerated by ABCB1 (MDR1)-mutant dogs. Not approved in Japan (as of 2026-10); the Japanese single-agent Credelio (lotilaner) is available.",
                "notes_ja": "開始前に犬糸状虫陰性を確認。イソキサゾリン系のクラス警告 — 神経系副作用（振戦・運動失調・けいれん）の報告があり、けいれん歴のある犬では慎重に。予防用量のミルベマイシンはABCB1（MDR1）変異犬でも忍容される。国内未承認（2026-10時点） — 国内では単剤クレデリオ（ロチラネル）が利用可能。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not for cats — use the feline lotilaner product (Credelio CAT) or another feline-labelled combination.",
                "dosage_ja": "猫には使用しない — 猫用ロチラネル製剤（Credelio CAT）など猫用ラベルの製剤を使用する。",
                "notes": "Dog-only product.",
                "notes_ja": "犬専用製剤。",
            },
        },
        "contraindications": "Dogs <8 weeks or <1.4 kg; heartworm-positive dogs (microfilaricidal reactions); hypersensitivity. Caution with a history of seizures.",
        "contraindications_ja": "8週齢未満または1.4 kg未満、犬糸状虫陽性犬（ミクロフィラリア殺滅反応）、過敏症。けいれん歴のある犬では慎重に。",
        "side_effects": [
            "Vomiting, diarrhea (uncommon)",
            "Lethargy, anorexia",
            "Neurological signs (tremor, ataxia, seizures) — rare, isoxazoline class",
        ],
        "side_effects_ja": [
            "嘔吐・下痢（まれ）",
            "元気消失・食欲低下",
            "神経症状（振戦・運動失調・けいれん）— まれ、イソキサゾリン系のクラス効果",
        ],
        "drug_interactions": [
            {
                "drug": "Other isoxazolines (afoxolaner, fluralaner, sarolaner)",
                "effect": "Duplicate isoxazoline therapy — do not combine.",
                "effect_ja": "イソキサゾリン系の重複 — 併用しない。",
                "severity": "moderate",
            },
            {
                "drug": "Other macrocyclic lactones (ivermectin, moxidectin, selamectin)",
                "effect": "Duplicate macrocyclic-lactone therapy — avoid stacking, especially in ABCB1-mutant breeds.",
                "effect_ja": "大環状ラクトンの重複 — 特にABCB1変異犬種では重ねない。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Credelio Plus EPAR / Summary of Product Characteristics (EMA, Elanco Animal Health, 2021).",
            "Cavalleri D et al. Efficacy of a novel oral chewable tablet containing lotilaner and milbemycin oxime against Angiostrongylus vasorum. Parasit Vectors 2021.",
            "American Heartworm Society. Canine Guidelines 2024.",
        ],
    },
]
