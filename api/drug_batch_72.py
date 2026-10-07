"""Drug batch 72 – 2026-10 session: Credelio Quattro (lotilaner + moxidectin +
praziquantel + pyrantel), the first monthly oral endectocide for dogs that
adds tapeworm coverage to flea/tick/heartworm/roundworm/hookworm protection.

The dictionary carried lotilaner alone (Credelio) and the individual
anthelmintics, but no single-product monograph for the 4-way combination.
Its per-component doses differ from the stand-alone products (e.g. moxidectin
0.02 mg/kg monthly oral is a heartworm-preventive micro-dose, not the
topical/injectable moxidectin doses), so it is kept as its own entry rather
than merged into lotilaner.

Evidence:
  - FDA NADA 141-581 Freedom of Information Summary / product label
    (Elanco, approved 2024): monthly oral, minimum 20 mg/kg lotilaner,
    0.02 mg/kg moxidectin, 5 mg/kg praziquantel, 5 mg/kg pyrantel (pamoate)
    (label ranges 20-41 / 0.02-0.04 / 5-10 / 5-10 mg/kg); dogs >= 8 weeks
    and >= 3.3 lb (1.5 kg); give with or within 30 min after a meal.
  - Long-term safety of Credelio Quattro in dogs, Parasites & Vectors
    2025/2026 (PMC12821975).
  - Isoxazoline class warning (FDA 2018): neurologic adverse events
    (tremor, ataxia, seizures) — use with caution in dogs with a history
    of seizures.
"""

DRUGS_BATCH_72 = [
    {
        "id": "credelio_quattro",
        "search_aliases": [
            "クレデリオクワトロ",
            "Credelio Quattro",
            "ロチラネル・モキシデクチン・プラジクアンテル・ピランテル",
        ],
        "name": "Credelio Quattro (lotilaner/moxidectin/praziquantel/pyrantel)",
        "name_ja": "クレデリオクワトロ（ロチラネル・モキシデクチン・プラジカンテル・ピランテル配合）",
        "category": "antiparasitics",
        "mechanism": "Fixed four-drug monthly oral endectocide. Lotilaner (isoxazoline) blocks insect/acarine GABA-gated chloride channels — fleas and ticks; moxidectin (macrocyclic lactone, micro-dose) kills Dirofilaria immitis L3/L4 larvae — heartworm prevention; praziquantel increases tapeworm tegument Ca2+ permeability — Dipylidium caninum / Taenia; pyrantel pamoate (nicotinic agonist, spastic paralysis) — roundworms and hookworms. The only single monthly chew combining flea/tick, heartworm and tapeworm coverage.",
        "mechanism_ja": "4成分配合の月1回経口エンデクトサイド。ロチラネル（イソキサゾリン系）が昆虫・ダニのGABA作動性Cl-チャネルを遮断しノミ・マダニを駆除、モキシデクチン（マクロライド系・微量）が犬糸状虫L3/L4幼虫を殺滅しフィラリアを予防、プラジカンテルが条虫外皮のCa2+透過性を高め瓜実条虫・テニア属を駆除、パモ酸ピランテル（ニコチン作動薬・痙攣性麻痺）が回虫・鉤虫を駆除する。ノミ・マダニ・フィラリア・条虫を1剤で網羅する唯一の月1回チュアブル。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "PO once monthly with food (or within 30 min after a meal), at minimum 20 mg/kg lotilaner + 0.02 mg/kg moxidectin + 5 mg/kg praziquantel + 5 mg/kg pyrantel (label ranges 20-41 / 0.02-0.04 / 5-10 / 5-10 mg/kg) — dose by the weight-band tablet, do not split. Dogs >= 8 weeks of age and >= 1.5 kg (3.3 lb). Heartworm-negative test required before starting (FDA NADA 141-581 label).",
                "dosage_ja": "月1回経口、食事と共に（または食後30分以内）。最低用量: ロチラネル 20 mg/kg + モキシデクチン 0.02 mg/kg + プラジカンテル 5 mg/kg + ピランテル 5 mg/kg（ラベル範囲 20-41 / 0.02-0.04 / 5-10 / 5-10 mg/kg）— 体重帯別の錠剤で投与し分割しない。8週齢以上かつ体重1.5 kg以上。開始前にフィラリア陰性を確認（FDA NADA 141-581 ラベル）。",
                "notes": "Indications (US label): prevention of heartworm disease; treatment/control of fleas and ticks; roundworms (Toxocara canis, Toxascaris leonina), hookworms and tapeworms (Dipylidium caninum, Taenia). Isoxazoline class warning: tremor/ataxia/seizures reported — use with caution in dogs with a seizure history. Not a heartworm adulticide (follow AHS protocol if positive). Dipylidium re-infection requires concurrent flea control (covered by lotilaner). Not approved in Japan as of this entry — US/overseas product; Japanese clinics use the separately licensed components.",
                "notes_ja": "適応（米国ラベル）: 犬糸状虫症の予防、ノミ・マダニの駆除・予防、回虫（Toxocara canis・Toxascaris leonina）・鉤虫・条虫（瓜実条虫・テニア属）の駆除。イソキサゾリン系クラス警告: 振戦・運動失調・発作の報告 — 発作歴のある犬では慎重に。成虫駆除薬ではない（陽性時はAHS 3回メラルソミン法）。瓜実条虫の再感染予防にはノミ対策の継続が必要（ロチラネルで同時カバー）。本収載時点で国内未承認の海外製品 — 国内では各成分の承認製剤を個別に使用。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not for use in cats — canine-only product (cats have a separate Credelio CAT lotilaner product without this combination).",
                "dosage_ja": "猫には使用しない — 犬専用製剤（猫用はロチラネル単剤のクレデリオCAT）。",
                "notes": "No feline safety data for the combination.",
                "notes_ja": "配合剤としての猫の安全性データはない。",
            },
        },
        "contraindications": "Dogs < 8 weeks of age or < 1.5 kg. Heartworm-positive dogs without prior evaluation (not an adulticide). Caution: history of seizures or neurologic disorders (isoxazoline class warning).",
        "contraindications_ja": "8週齢未満・体重1.5 kg未満の犬。事前評価のないフィラリア陽性犬（成虫駆除薬ではない）。発作歴・神経疾患のある犬は慎重に（イソキサゾリン系クラス警告）。",
        "side_effects": [
            "Vomiting, diarrhea, decreased appetite (uncommon, usually transient)",
            "Lethargy",
            "Neurologic signs: tremor, ataxia, seizures (isoxazoline class warning)",
        ],
        "side_effects_ja": [
            "嘔吐・下痢・食欲低下（まれ・通常一過性）",
            "嗜眠",
            "神経症状: 振戦・運動失調・発作（イソキサゾリン系クラス警告）",
        ],
        "drug_interactions": [
            {
                "drug": "Other isoxazolines (fluralaner, afoxolaner, sarolaner)",
                "effect": "Duplicate isoxazoline exposure — no added benefit, additive neurologic risk.",
                "effect_ja": "イソキサゾリン系の重複投与 — 追加効果なく神経系リスクが相加。",
                "severity": "moderate",
            },
            {
                "drug": "Other macrocyclic lactones (ivermectin, milbemycin, selamectin)",
                "effect": "Duplicate heartworm preventive — avoid stacking; relevant in ABCB1 (MDR1)-mutant breeds at higher ML doses.",
                "effect_ja": "フィラリア予防薬の重複 — 併用しない。ABCB1（MDR1）変異犬種で高用量MLとの重複は特に注意。",
                "severity": "moderate",
            },
        ],
        "references": [
            "FDA NADA 141-581 Freedom of Information Summary / Credelio Quattro label (Elanco, 2024)",
            "Long-term safety of Credelio Quattro in dogs. Parasit Vectors (PMC12821975)",
            "American Heartworm Society Canine Guidelines 2024",
        ],
    },
]
