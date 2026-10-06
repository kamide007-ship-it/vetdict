"""Drug batch 70 – 2026-10 audit (第63弾): newly approved agent.

  - FLURALANER EXTENDED-RELEASE INJECTABLE (Bravecto Quantum) — the first
    12-month flea and tick product for dogs (US FDA approval July 2025;
    marketed earlier in the EU/Australia as the Bravecto injectable,
    150 mg/mL).  Same isoxazoline as the oral/spot-on fluralaner entries,
    but a distinct product with a distinct dose (15 mg/kg SC once — NOT
    the 25-56 mg/kg oral chew range), a veterinarian-administered route,
    an age floor of 6 months, and a 12-month duration — so it is kept as
    its own monograph rather than merged (the oral dose must never be
    carried over to the injectable).

References:
  - Bravecto Quantum (fluralaner extended-release injectable suspension)
    US label, Merck Animal Health (FDA approved 2025) — 15 mg/kg SC once
    every 12 months; dogs 6 months of age and older; isoxazoline class
    neurologic warning.
  - Bravecto injectable 150 mg/ml SPC (EMA) — 15 mg/kg (0.1 mL/kg) SC.
  - FDA CVM 2018 class communication: isoxazoline products and
    neurologic adverse events (muscle tremors, ataxia, seizures).
"""

DRUGS_BATCH_70 = [
    {
        "id": "fluralaner_injectable",
        "search_aliases": [
            "ブラベクトクオンタム",
            "ブラベクト クオンタム",
            "ブラベクト注射",
            "フルララネル注射",
            "フルララネル徐放性注射",
            "bravecto quantum",
            "bravecto injectable",
        ],
        "name": "Fluralaner Extended-Release Injectable (Bravecto Quantum)",
        "name_ja": "フルララネル徐放性注射剤（ブラベクト クオンタム）",
        "category": "antiparasitics",
        "mechanism": "Isoxazoline ectoparasiticide (GABA- and glutamate-gated chloride channel antagonist, selective for arthropods) in an extended-release injectable suspension that forms a subcutaneous depot, giving 12 months of flea and tick protection from a single veterinarian-administered injection. Removes the owner-compliance gap of monthly/quarterly products.",
        "mechanism_ja": "イソキサゾリン系外部寄生虫駆除薬（節足動物選択的なGABA/グルタミン酸作動性塩素チャネル拮抗）の徐放性注射懸濁剤。皮下にデポを形成し、獣医師による1回の注射で12ヶ月間ノミ・マダニを防除する。月1回/3ヶ月毎製剤の飼い主の投与忘れ（コンプライアンス・ギャップ）を解消する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "15 mg/kg SC once (150 mg/mL suspension = 0.1 mL/kg), every 12 months; administered by a veterinarian. Dogs 6 months of age and older. Do NOT apply the oral chew dose (25-56 mg/kg) to the injectable.",
                "dosage_ja": "15 mg/kg 皮下注射 1回（150 mg/mL懸濁液 = 0.1 mL/kg）、12ヶ月毎。獣医師が投与する。6ヶ月齢以上の犬。**経口チュアブル錠の用量（25-56 mg/kg）を注射剤に流用しない**。",
                "notes": "Indication: prevention/treatment of flea infestations and treatment/control of tick infestations for 12 months (individual tick species and durations per the national label). Gently shake before use; inject SC (dorsal neck/interscapular). Isoxazoline class warning: muscle tremors, ataxia and seizures have been reported — use with caution in dogs with a seizure history; a depot cannot be withdrawn once given, so choose an oral/spot-on product when a trial of tolerance is desirable. Not for cats. Safety in breeding, pregnant or lactating dogs not established. Approval is product- and country-specific — confirm local availability.",
                "notes_ja": "適応: ノミ寄生の予防・治療およびマダニ寄生の治療・防除（12ヶ月間。対象マダニ種と持続期間は各国ラベルに従う）。使用前に軽く振とうし、頸背部〜肩甲間に皮下注射。イソキサゾリン系の共通警告: 筋振戦・運動失調・痙攣の報告あり — 痙攣既往の犬では慎重に。**注射デポは投与後に除去できない**ため、忍容性を試したい症例ではまず経口/スポットオン製剤を選ぶ。猫には使用しない。繁殖・妊娠・授乳中の犬での安全性は未確立。承認は製剤・国ごとに異なる — 国内の入手可否を確認すること。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not approved for cats — use the fluralaner spot-on (Bravecto Plus/Spot-On) instead",
                "dosage_ja": "猫には未承認 — フルララネル外用（ブラベクトスポットオン/プラス）を使用する",
                "notes": "The extended-release injectable is a canine product only",
                "notes_ja": "徐放性注射剤は犬専用製剤",
            },
        },
        "side_effects": [
            "Injection-site swelling or pain (transient)",
            "Vomiting, lethargy, decreased appetite (uncommon)",
            "Neurologic signs — tremors, ataxia, seizures (isoxazoline class, rare)",
        ],
        "side_effects_ja": [
            "注射部位の腫脹・疼痛（一過性）",
            "嘔吐・元気消失・食欲低下（まれ）",
            "神経症状 — 振戦・運動失調・痙攣（イソキサゾリン系共通、まれ）",
        ],
        "contraindications": "Dogs under 6 months of age; cats; hypersensitivity to fluralaner; caution in dogs with a history of seizures or neurologic disorders (the depot cannot be removed after injection)",
        "contraindications_ja": "6ヶ月齢未満の犬。猫。フルララネル過敏症。痙攣・神経疾患の既往がある犬では慎重に（注射後にデポを除去できない）",
        "drug_interactions": [
            {
                "drug": "Other isoxazolines (afoxolaner, sarolaner, lotilaner, oral/topical fluralaner)",
                "effect": "Duplicate isoxazoline exposure with no added benefit and additive neurologic risk — do not layer another isoxazoline during the 12-month protection period",
                "effect_ja": "イソキサゾリン系の重複曝露で上乗せ効果なく神経系リスクが相加 — 12ヶ月の防除期間中に他のイソキサゾリン製剤を重ねない",
                "severity": "moderate",
            },
        ],
    },
]
