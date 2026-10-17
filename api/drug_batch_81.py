"""Drug batch 81 – 2026-10 第72弾.

1. Carbimazole (Vidalta) — EU/UK-authorised controlled-release prodrug of
   methimazole for feline hyperthyroidism. The feline hyperthyroidism and
   drug-reaction entries already quote "Carbimazole 5 mg PO q8-12h" and the
   methimazole-hepatopathy row warns of carbimazole cross-reactivity, but the
   agent itself had no monograph (referenced-but-absent).
2. Tasipimidine (Tessie) — EU-authorised (EMA 2022, Orion) selective α2A-
   adrenoceptor agonist oral solution for situational anxiety and fear in
   dogs (noise, car travel, veterinary visits): a newly approved anxiolytic
   class member that complements trazodone/gabapentin/Sileo.

Evidence:
  - Frenais R et al. Clinical efficacy and safety of a once-daily formulation
    of carbimazole in cats with hyperthyroidism. J Small Anim Pract
    2009;50:510-515.
  - Carney HC et al. 2016 AAFP Guidelines for the Management of Feline
    Hyperthyroidism. J Feline Med Surg 2016;18:400-416.
  - Vidalta SPC (MSD Animal Health, UK VMD).
  - Tessie EPAR / SPC (EMA, Orion Corporation, 2022).
"""

DRUGS_BATCH_81 = [
    {
        "id": "carbimazole",
        "search_aliases": ["カルビマゾール", "ビダルタ", "Vidalta", "carbimazole"],
        "name": "Carbimazole (Vidalta)",
        "name_ja": "カルビマゾール（ビダルタ）",
        "category": "endocrine",
        "mechanism": "Prodrug rapidly converted to methimazole (thiamazole); blocks thyroid peroxidase-mediated iodination and coupling, reducing T4/T3 synthesis. 10 mg carbimazole yields ≈6 mg methimazole.",
        "mechanism_ja": "体内で速やかにメチマゾール（チアマゾール）に変換されるプロドラッグ。甲状腺ペルオキシダーゼによるヨウ素化・縮合を阻害しT4/T3合成を抑制する。カルビマゾール10 mg ≒ メチマゾール約6 mg。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Controlled-release tablets (Vidalta): 15 mg PO q24h starting dose (10 mg q24h if total T4 is only mildly elevated); adjust in 5 mg steps to 10-25 mg q24h to keep T4 in the lower half of the reference range (Frenais 2009 JSAP). Conventional (non-controlled-release) carbimazole: 5 mg PO q8-12h. Recheck T4, CBC, liver enzymes and renal values 3, 5, 8 weeks after starting/dose change, then every 3 months.",
                "dosage_ja": "徐放錠（ビダルタ）: 開始量 15 mg PO q24h（総T4が軽度上昇のみなら 10 mg q24h）。総T4を基準範囲下半分に保つよう 5 mg 単位で 10-25 mg q24h に調整（Frenais 2009 JSAP）。通常製剤（非徐放）は 5 mg PO q8-12h。開始/変更後3・5・8週でT4・CBC・肝酵素・腎機能を再検し、以後3ヶ月毎。",
                "notes": "Same adverse-effect profile as methimazole (cross-reactive): vomiting/anorexia, facial excoriation, hepatopathy, neutropenia/thrombocytopenia — STOP (do not merely reduce) for facial excoriation, hepatopathy or blood dyscrasias and move to radioiodine, surgery or iodine-restricted diet. Renal masking: CKD may be unmasked once euthyroid (Williams 2010 JVIM). Controlled-release tablets must not be crushed or split. Not marketed in Japan — methimazole is the domestic equivalent.",
                "notes_ja": "副作用はメチマゾールと同一（交差反応あり）: 嘔吐・食欲不振・顔面掻爬・肝障害・好中球/血小板減少 — 顔面掻爬・肝障害・血球減少は減量ではなく中止し、I-131・手術・ヨウ素制限食へ。腎マスキング: 正甲状腺化後にCKDが顕在化しうる（Williams 2010 JVIM）。徐放錠は粉砕・分割しない。国内未承認 — 国内ではメチマゾールが同等薬。",
            },
            "dog": {
                "safe": True,
                "dosage": "Rarely indicated (canine hyperthyroidism is usually thyroid carcinoma — surgery/radioiodine). Off-label palliative use extrapolated from methimazole equivalents only.",
                "dosage_ja": "適応はまれ（犬の甲状腺機能亢進症は大半が甲状腺癌 — 手術・放射性ヨウ素が主）。メチマゾール換算での緩和的な適応外使用に限る。",
                "notes": "Off-label. Monitor CBC and liver enzymes as for methimazole.",
                "notes_ja": "適応外使用。メチマゾールと同様にCBC・肝酵素を監視。",
            },
        },
        "contraindications": "Previous methimazole/carbimazole hypersensitivity, facial excoriation, hepatopathy or blood dyscrasia (cross-reactive); primary hepatic disease; pregnancy/lactation; autoimmune disease.",
        "contraindications_ja": "メチマゾール/カルビマゾールでの過敏症・顔面掻爬・肝障害・血球減少の既往（交差反応）、原発性肝疾患、妊娠・授乳中、自己免疫疾患。",
        "side_effects": [
            "Vomiting / anorexia",
            "Facial excoriation",
            "Hepatopathy",
            "Neutropenia / thrombocytopenia",
            "Iatrogenic hypothyroidism",
        ],
        "side_effects_ja": ["嘔吐・食欲不振", "顔面掻爬", "肝障害", "好中球減少・血小板減少", "医原性甲状腺機能低下症"],
        "drug_interactions": [
            {
                "drug": "Methimazole",
                "effect": "Same active moiety — never combine; switching requires dose conversion (10 mg carbimazole ≈ 6 mg methimazole).",
                "effect_ja": "同一の活性体 — 併用しない。切替時は換算（カルビマゾール10 mg ≒ メチマゾール6 mg）。",
                "severity": "major",
            },
            {
                "drug": "Radioiodine (I-131)",
                "effect": "Antithyroid drugs are usually stopped 1-2 weeks before radioiodine therapy.",
                "effect_ja": "放射性ヨウ素治療の1-2週間前には通常休薬する。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Frenais R et al. Clinical efficacy and safety of a once-daily formulation of carbimazole in cats with hyperthyroidism. J Small Anim Pract 2009;50:510-515.",
            "Carney HC et al. 2016 AAFP Guidelines for the Management of Feline Hyperthyroidism. J Feline Med Surg 2016;18:400-416.",
            "Williams TL et al. Association of iatrogenic hypothyroidism with azotemia and reduced survival time in cats treated for hyperthyroidism. J Vet Intern Med 2010;24:1086-1092.",
            "Vidalta SPC, MSD Animal Health (UK VMD).",
        ],
    },
    {
        "id": "tasipimidine",
        "search_aliases": ["タシピミジン", "テッシー", "Tessie", "tasipimidine"],
        "name": "Tasipimidine (Tessie)",
        "name_ja": "タシピミジン（テッシー）",
        "category": "behavioral",
        "mechanism": "Selective α2A-adrenoceptor agonist; reduces noradrenergic (locus coeruleus) activity driving acute fear and anxiety at doses that produce minimal sedation.",
        "mechanism_ja": "選択的α2Aアドレナリン受容体作動薬。急性の恐怖・不安を駆動するノルアドレナリン作動性（青斑核）活動を、鎮静の少ない用量で抑制する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "30 µg/kg PO (0.3 mg/mL oral solution, measured with the supplied syringe) about 1 hour before the anxiety-provoking event (noise, car travel, separation, veterinary visit) — follow the EU SPC for repeat dosing within the same day and the maximum daily number of doses.",
                "dosage_ja": "30 µg/kg PO（0.3 mg/mL 経口液、付属シリンジで計量）を不安誘発イベント（騒音・車移動・留守番・来院）の約1時間前。同日内の追加投与と1日最大投与回数はEUの添付文書（SPC）に従う。",
                "notes": "Situational use alongside behavioural modification. Transient sedation, vomiting and pale mucous membranes (α2 vasoconstriction) can occur; reduced heart rate. Not authorised in Japan. Reversible with atipamezole if over-sedation occurs.",
                "notes_ja": "行動修正と併用する状況的投与。一過性の鎮静・嘔吐・粘膜蒼白（α2血管収縮）・心拍数低下がみられうる。国内未承認。過鎮静時はアチパメゾールで拮抗可能。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not authorised for cats — no established dose.",
                "dosage_ja": "猫には未承認 — 用量未確立。",
                "notes": "Use gabapentin or other evidence-based feline options.",
                "notes_ja": "猫ではガバペンチン等のエビデンスのある選択肢を使用。",
            },
        },
        "contraindications": "Cardiovascular disease, severe systemic disease (ASA III+), hepatic or renal impairment, pregnancy/lactation, dogs under 6 months. Do not combine with other α2-agonists.",
        "contraindications_ja": "心血管疾患・重度の全身疾患（ASA III以上）・肝/腎機能障害・妊娠授乳中・6ヶ月齢未満。他のα2作動薬と併用しない。",
        "side_effects": [
            "Sedation / lethargy",
            "Vomiting",
            "Pale mucous membranes",
            "Bradycardia",
            "Hypothermia (transient)",
        ],
        "side_effects_ja": ["鎮静・元気消失", "嘔吐", "粘膜蒼白", "徐脈", "一過性の低体温"],
        "drug_interactions": [
            {
                "drug": "Dexmedetomidine / Medetomidine",
                "effect": "Duplicate α2-agonism — additive bradycardia, sedation and cardiovascular depression.",
                "effect_ja": "α2作動作用の重複 — 徐脈・鎮静・循環抑制の相加。",
                "severity": "major",
            },
            {
                "drug": "Atipamezole",
                "effect": "Reverses tasipimidine effects.",
                "effect_ja": "タシピミジンの作用を拮抗する。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Tessie EPAR / SPC, European Medicines Agency (Orion Corporation), 2022.",
            "Landsberg G, Hunthausen W, Ackerman L. Behavior Problems of the Dog and Cat, 3rd ed. 2013.",
        ],
    },
]
