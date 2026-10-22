"""Drug batch 84 – 2026-10 第75弾 (referenced-but-absent sweep #38).

Both agents are named with doses in the site's own treatment texts but had no
monograph, so the treatment chips, the reverse "diseases using this drug"
index and the interaction checker could not resolve them.

1. Ertugliflozin — horse laminitis (endocrinopathic / insulin-dysregulation
   associated) text: "SGLT2阻害薬(エルツグリフロジン 0.05-0.15 mg/kg PO SID)
   (Sundra et al. EVJ 2023)".
   Evidence: Sundra T, Kelty E, Rendle D. Preliminary observations on the use
   of ertugliflozin in the management of hyperinsulinaemia and laminitis in 51
   horses: a case series. Equine Vet J 2023 (0.05 mg/kg PO q24h; marked fall
   in insulin; hypertriglyceridaemia the main adverse finding). Class proof of
   concept: Meier A et al. velagliflozin in insulin-dysregulated ponies,
   PLOS One 2018. Off-label human drug; no veterinary authorisation.

2. Methylphenidate — dog "Hyperkinesis (Canine ADHD)" text: diagnostic trial
   0.2-1 mg/kg PO single dose (paradoxical calming with falls in heart rate,
   respiratory rate and activity in true hyperkinesis), then 0.2-1 mg/kg PO
   q12h long term.
   Evidence: Overall KL, Manual of Clinical Behavioral Medicine for Dogs and
   Cats (Elsevier 2013); Luescher UA in Horwitz & Mills (eds) BSAVA Manual of
   Canine and Feline Behavioural Medicine 2nd ed (2009); Plumb's Veterinary
   Drug Handbook 10th ed. In Japan methylphenidate is a Class 1 psychotropic
   with restricted distribution, so veterinary access is limited.
"""

DRUGS_BATCH_84 = [
    {
        "id": "ertugliflozin",
        "search_aliases": [
            "エルツグリフロジン",
            "えるつぐりふろじん",
            "スーグラ",
            "Steglatro",
            "ertugliflozin",
        ],
        "name": "Ertugliflozin (Steglatro)",
        "name_ja": "エルツグリフロジン（スーグラ）",
        "category": "endocrine",
        "mechanism": "Sodium-glucose co-transporter 2 (SGLT2) inhibitor. Blocks renal tubular glucose reabsorption, producing glucosuria and lowering post-prandial glucose and therefore insulin secretion. In insulin-dysregulated horses the aim is to reduce the hyperinsulinaemia that drives endocrinopathic laminitis, not to treat hyperglycaemia.",
        "mechanism_ja": "SGLT2（ナトリウム・グルコース共輸送体2）阻害薬。腎尿細管でのグルコース再吸収を阻害して尿糖を生じさせ、食後血糖とそれに伴うインスリン分泌を下げる。インスリン調節異常の馬では、高血糖の治療ではなく、内分泌性蹄葉炎の原因となる高インスリン血症を下げることが目的。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "0.05 mg/kg PO q24h (Sundra 2023 case series, 51 horses). Reserve for insulin-dysregulated horses (EMS/PPID) with laminitis or persistent hyperinsulinaemia that has not responded to diet (low NSC <10% DM), weight loss and, for PPID, pergolide. Recheck insulin (oral sugar test or resting) and triglycerides 2-4 weeks after starting, then periodically.",
                "dosage_ja": "0.05 mg/kg 経口 24時間毎（Sundra 2023 症例集積、51頭）。食事管理（NSC 10%未満/乾物）・減量、PPIDではペルゴリドを行っても蹄葉炎または高インスリン血症が続くインスリン調節異常の馬（EMS/PPID）に限って使う。開始2〜4週後にインスリン（経口糖負荷試験または安静時）と中性脂肪を再検し、以後も定期的に確認する。",
                "notes": "Off-label use of a human drug; evidence is a retrospective case series plus a class proof-of-concept in ponies (velagliflozin, Meier 2018) — no randomised trial yet. Hypertriglyceridaemia is the main adverse finding (mostly mild, without clinical hyperlipaemia in the series) — stop if triglycerides rise markedly or the horse becomes inappetent. Diet and exercise remain the foundation. Not for horses with hyperlipaemia, dehydration or reduced feed intake (ketosis/lipid mobilisation risk).",
                "notes_ja": "ヒト用医薬品の適応外使用。エビデンスは後ろ向き症例集積と、ポニーでの同クラス薬の概念実証（ベラグリフロジン、Meier 2018）のみで、無作為化試験はまだない。主な有害所見は高トリグリセリド血症（症例集積では多くが軽度で臨床的な高脂血症はなし） — 中性脂肪が大きく上昇した場合や食欲が落ちた場合は中止する。基本は食事管理と運動。高脂血症・脱水・採食量低下のある馬には使わない（ケトーシス・脂肪動員のリスク）。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not used — the authorised feline SGLT2 inhibitors are bexagliflozin (Bexacat) and velagliflozin (Senvelgo).",
                "dosage_ja": "使用しない — 猫で承認されているSGLT2阻害薬はベキサグリフロジン（ベクサキャット）とベラグリフロジン（センベルゴ）。",
                "notes": "No feline data.",
                "notes_ja": "猫でのデータなし。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not used — canine diabetes is insulin-dependent; SGLT2 monotherapy risks euglycaemic diabetic ketoacidosis.",
                "dosage_ja": "使用しない — 犬の糖尿病はインスリン依存性で、SGLT2阻害薬単剤は正常血糖性糖尿病性ケトアシドーシスのリスクがある。",
                "notes": "No canine indication.",
                "notes_ja": "犬での適応なし。",
            },
        },
        "contraindications": "Hyperlipaemia or hypertriglyceridaemia; anorexia, dehydration or reduced feed intake; pregnancy (no data). Not a substitute for dietary management.",
        "contraindications_ja": "高脂血症・高トリグリセリド血症、食欲不振・脱水・採食量低下、妊娠（データなし）。食事管理の代わりにはならない。",
        "side_effects": [
            "Hypertriglyceridaemia (main finding)",
            "Polyuria from glucosuria",
            "Potential ketosis / lipid mobilisation if feed intake falls",
        ],
        "side_effects_ja": [
            "高トリグリセリド血症（主な所見）",
            "尿糖による多尿",
            "採食量が落ちた場合のケトーシス・脂肪動員の可能性",
        ],
        "drug_interactions": [
            {
                "drug": "Metformin",
                "effect": "Both aim to reduce hyperinsulinaemia; combined use is not studied in horses — monitor insulin and triglycerides.",
                "effect_ja": "どちらも高インスリン血症の改善を狙う薬。馬での併用は未検討 — インスリンと中性脂肪を監視する。",
                "severity": "moderate",
            },
            {
                "drug": "Levothyroxine",
                "effect": "Weight-loss aid in EMS; additive metabolic effects — monitor body condition and triglycerides.",
                "effect_ja": "EMSでの減量補助薬。代謝への作用が重なる — 体格と中性脂肪を監視する。",
                "severity": "minor",
            },
        ],
        "references": [
            "Sundra T, Kelty E, Rendle D. Preliminary observations on the use of ertugliflozin in the management of hyperinsulinaemia and laminitis in 51 horses: a case series. Equine Vet J 2023.",
            "Meier A, de Laat M, Reiche D, et al. The sodium-glucose co-transporter 2 inhibitor velagliflozin reduces hyperinsulinemia and prevents laminitis in insulin-dysregulated ponies. PLoS One 2018;13:e0203655.",
            "Durham AE, Frank N, McGowan CM, et al. ECEIM consensus statement on equine metabolic syndrome. J Vet Intern Med 2019;33:335-349.",
        ],
    },
    {
        "id": "methylphenidate",
        "search_aliases": [
            "メチルフェニデート",
            "めちるふぇにでーと",
            "リタリン",
            "Ritalin",
            "methylphenidate",
        ],
        "name": "Methylphenidate (Ritalin)",
        "name_ja": "メチルフェニデート（リタリン）",
        "category": "behavioral",
        "mechanism": "Central nervous system stimulant that blocks dopamine and noradrenaline reuptake. In the rare dog with true hyperkinesis it has a paradoxical calming effect — the basis of the diagnostic trial; normal or merely under-exercised dogs become more excited.",
        "mechanism_ja": "ドパミンとノルアドレナリンの再取り込みを阻害する中枢神経刺激薬。まれな真の過活動症の犬では逆説的な鎮静効果を示し、これが診断的試験投与の根拠となる。正常な犬や運動不足なだけの犬では、かえって興奮が強まる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Diagnostic trial: 0.2-1 mg/kg PO once, recording heart rate, respiratory rate and activity before and 1-2 hours after the dose (true hyperkinesis = falls in all three and calmer behaviour; normal dogs become more aroused). If the trial is positive: 0.2-1 mg/kg PO q8-12h, started at the low end.",
                "dosage_ja": "診断的試験: 0.2〜1 mg/kg 経口単回。投与前と投与1〜2時間後に心拍数・呼吸数・活動量を記録する（真の過活動症ではいずれも低下して落ち着く。正常な犬はかえって興奮する）。試験が陽性の場合: 0.2〜1 mg/kg 経口 8〜12時間毎、低用量から開始。",
                "notes": "True hyperkinesis is rare — first rule out normal high energy, lack of exercise and anxiety, and pair any drug with a structured behaviour plan. Monitor heart rate, blood pressure, appetite and body weight. Stop if heart rate rises, or for agitation, anorexia or stereotypies. In Japan methylphenidate is a Class 1 psychotropic with restricted distribution, so veterinary access is limited.",
                "notes_ja": "真の過活動症はまれ — まず正常な高いエネルギー、運動不足、不安を除外し、薬は必ず構造化された行動修正計画と組み合わせる。心拍数・血圧・食欲・体重を監視する。心拍数の上昇、興奮、食欲不振、常同行動が出たら中止する。国内では第一種向精神薬で流通が厳しく管理されており、獣医療での入手は限られる。",
            },
            "cat": {
                "safe": False,
                "dosage": "No indication in cats.",
                "dosage_ja": "猫での適応なし。",
                "notes": "Stimulants can cause hyperthermia, tachycardia and seizures in cats.",
                "notes_ja": "猫では中枢刺激薬により高体温・頻脈・痙攣が起こりうる。",
            },
        },
        "contraindications": "Cardiac disease or arrhythmia, hypertension, seizure disorders, glaucoma, hyperthyroidism, concurrent MAO inhibitors (selegiline, amitraz). Not for aggression.",
        "contraindications_ja": "心疾患・不整脈、高血圧、てんかん等の痙攣性疾患、緑内障、甲状腺機能亢進症、MAO阻害薬（セレギリン・アミトラズ）との併用。攻撃行動には使わない。",
        "side_effects": [
            "Tachycardia, hypertension",
            "Anorexia, weight loss",
            "Agitation, insomnia, stereotypies",
            "Hyperthermia and seizures in overdose",
        ],
        "side_effects_ja": [
            "頻脈・高血圧",
            "食欲不振・体重減少",
            "興奮・不眠・常同行動",
            "過量投与で高体温・痙攣",
        ],
        "drug_interactions": [
            {
                "drug": "Selegiline",
                "effect": "MAO inhibitor plus stimulant — risk of hypertensive crisis; do not combine.",
                "effect_ja": "MAO阻害薬と中枢刺激薬 — 高血圧クリーゼのリスク。併用しない。",
                "severity": "contraindicated",
            },
            {
                "drug": "Amitraz",
                "effect": "Amitraz has MAO-inhibiting activity — avoid combining with stimulants.",
                "effect_ja": "アミトラズにはMAO阻害作用がある — 中枢刺激薬との併用を避ける。",
                "severity": "major",
            },
            {
                "drug": "Fluoxetine / clomipramine / trazodone",
                "effect": "Additive serotonergic and sympathomimetic effects — monitor for agitation and tachycardia.",
                "effect_ja": "セロトニン作用・交感神経作用が相加 — 興奮と頻脈を監視する。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Overall KL. Manual of Clinical Behavioral Medicine for Dogs and Cats. Elsevier, 2013.",
            "Luescher UA. Hyperkinesis in dogs: six case reports. Can Vet J 1993;34:368-370.",
            "Horwitz DF, Mills DS (eds). BSAVA Manual of Canine and Feline Behavioural Medicine, 2nd ed. BSAVA, 2009.",
            "Plumb's Veterinary Drug Handbook, 10th ed. Wiley, 2023.",
        ],
    },
]
