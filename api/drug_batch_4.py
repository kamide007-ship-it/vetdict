"""Drug batch 4 – Fish-specific medications and fish species_info.

Adds fish (観賞魚) specific drugs and dosage data.
Note: Fish medications are typically administered via bath/dip, not oral/injection.

References:
  - Noga, E.J. Fish Disease: Diagnosis and Treatment, 2nd ed.
  - Stoskopf, M.K. Fish Medicine.
  - Wildgoose, W.H. BSAVA Manual of Ornamental Fish, 2nd ed.
"""

from __future__ import annotations

# Fish-specific drugs (not in main drug dictionary)
FISH_DRUGS: list[dict] = [
    {
        "id": "methylene_blue",
        "name": "Methylene Blue",
        "name_ja": "メチレンブルー",
        "category": "antiparasitics",
        "category_ja": "駆虫薬・抗寄生虫薬",
        "description": "Antifungal and antiparasitic dye used as a bath treatment for external infections in fish.",
        "description_ja": "魚の外部感染症に対する薬浴に使用される抗真菌・抗寄生虫色素。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "2-3 mg/L bath for 1-4 hours; or 0.1-0.2 mg/L prolonged bath",
                "dosage_ja": "2-3 mg/L 薬浴 1-4時間; または 0.1-0.2 mg/L 長時間浴",
                "notes": "Effective against Ich free-swimmers, fungus, and external parasites. Stains silicone, equipment, and biological filtration. Remove activated carbon before use.",
                "notes_ja": "白点病遊走子、真菌、外部寄生虫に有効。シリコン・器具・生物ろ過を染色する。使用前に活性炭を除去。",
            },
        },
    },
    {
        "id": "malachite_green",
        "name": "Malachite Green",
        "name_ja": "マラカイトグリーン",
        "category": "antiparasitics",
        "category_ja": "駆虫薬・抗寄生虫薬",
        "description": "Antiparasitic and antifungal dye for fish. Often combined with formalin.",
        "description_ja": "魚の抗寄生虫・抗真菌色素。ホルマリンとの併用が多い。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "0.05-0.1 mg/L prolonged bath; 0.1-0.15 mg/L short bath (1h)",
                "dosage_ja": "0.05-0.1 mg/L 長時間浴; 0.1-0.15 mg/L 短時間浴（1時間）",
                "notes": "Toxic to scaleless fish (loaches, catfish) — use at half dose. Teratogenic; do not use on food fish. Stains everything.",
                "notes_ja": "無鱗魚（ドジョウ、ナマズ）には毒性あり — 半量で使用。催奇形性あり。食用魚には使用不可。全てを染色する。",
            },
        },
    },
    {
        "id": "formalin_fish",
        "name": "Formalin (37% Formaldehyde)",
        "name_ja": "ホルマリン（37%ホルムアルデヒド）",
        "category": "antiparasitics",
        "category_ja": "駆虫薬・抗寄生虫薬",
        "description": "Broad-spectrum antiparasitic for external parasites in fish.",
        "description_ja": "魚の外部寄生虫に対する広域スペクトル抗寄生虫薬。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "15-25 mg/L (ppm) prolonged bath; 150-250 mg/L short dip (30-60 min)",
                "dosage_ja": "15-25 mg/L 長時間浴; 150-250 mg/L 短時間ディップ（30-60分）",
                "notes": "Depletes oxygen — increase aeration during treatment. Toxic at high temperatures (>27°C reduce dose). Do not use with methylene blue simultaneously.",
                "notes_ja": "酸素を消費 — 治療中はエアレーションを強化。高温（>27°C）では減量。メチレンブルーとの同時使用不可。",
            },
        },
    },
    {
        "id": "copper_sulfate",
        "name": "Copper Sulfate",
        "name_ja": "硫酸銅",
        "category": "antiparasitics",
        "category_ja": "駆虫薬・抗寄生虫薬",
        "description": "Copper-based antiparasitic for marine and freshwater fish.",
        "description_ja": "海水魚・淡水魚の銅系抗寄生虫薬。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "0.15-0.20 mg/L free copper (marine); 0.15 mg/L (freshwater); maintain for 14-21 days",
                "dosage_ja": "0.15-0.20 mg/L 遊離銅（海水）; 0.15 mg/L（淡水）; 14-21日間維持",
                "notes": "TOXIC to invertebrates and corals — use in treatment tank only. Monitor copper levels with test kit. Chelated copper preferred for stability.",
                "notes_ja": "無脊椎動物・サンゴに有毒 — 治療用水槽でのみ使用。テストキットで銅濃度を監視。安定性のためキレート銅が好ましい。",
            },
        },
    },
    {
        "id": "potassium_permanganate",
        "name": "Potassium Permanganate",
        "name_ja": "過マンガン酸カリウム",
        "category": "antiparasitics",
        "category_ja": "駆虫薬・抗寄生虫薬",
        "description": "Oxidizing agent used as an antiparasitic and antibacterial bath for fish.",
        "description_ja": "魚の抗寄生虫・抗菌薬浴に使用される酸化剤。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "2-4 mg/L prolonged bath (repeat q5-7d); 10 mg/L short dip (5-10 min)",
                "dosage_ja": "2-4 mg/L 長時間浴（5-7日毎に反復）; 10 mg/L 短時間ディップ（5-10分）",
                "notes": "Neutralize with hydrogen peroxide or sodium thiosulfate if fish show distress. Organic-rich water reduces efficacy.",
                "notes_ja": "魚がストレスを示したら過酸化水素またはチオ硫酸ナトリウムで中和。有機物の多い水では効果が低下。",
            },
        },
    },
    {
        "id": "acriflavine",
        "name": "Acriflavine",
        "name_ja": "アクリフラビン",
        "category": "antibiotics",
        "category_ja": "抗菌薬・抗生物質",
        "description": "Antiseptic dye used for external bacterial and fungal infections in fish.",
        "description_ja": "魚の外部細菌・真菌感染に使用される消毒色素。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "3-10 mg/L prolonged bath",
                "dosage_ja": "3-10 mg/L 長時間浴",
                "notes": "Effective for mild bacterial infections and egg fungus prevention. May damage biological filtration.",
                "notes_ja": "軽度の細菌感染と卵の真菌予防に有効。生物ろ過にダメージを与える可能性。",
            },
        },
    },
    {
        "id": "oxylinic_acid",
        "name": "Oxolinic Acid",
        "name_ja": "オキソリン酸",
        "category": "antibiotics",
        "category_ja": "抗菌薬・抗生物質",
        "description": "Quinolone antibiotic commonly used in fish medicine, particularly in Japan.",
        "description_ja": "魚病に広く使用されるキノロン系抗菌薬。日本で特に一般的。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "5-10 mg/L bath for 5-7 days; or 10 mg/kg in medicated feed q24h for 5-7 days",
                "dosage_ja": "5-10 mg/L 薬浴 5-7日間; または 10 mg/kg 薬餌 24時間毎 5-7日間",
                "notes": "First-line for Aeromonas, Pseudomonas, Columnaris. Available as commercial fish medication in Japan.",
                "notes_ja": "エロモナス、シュードモナス、カラムナリスに第一選択。日本では市販魚病薬として入手可能。",
            },
        },
    },
    {
        "id": "kanamycin_fish",
        "name": "Kanamycin Sulfate (Fish)",
        "name_ja": "カナマイシン硫酸塩（魚用）",
        "category": "antibiotics",
        "category_ja": "抗菌薬・抗生物質",
        "description": "Aminoglycoside antibiotic effective against gram-negative bacteria in fish.",
        "description_ja": "魚のグラム陰性菌に有効なアミノグリコシド系抗菌薬。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "50-100 mg/L bath for 5-7 days (50% water change before re-dosing)",
                "dosage_ja": "50-100 mg/L 薬浴 5-7日間（再投与前に50%換水）",
                "notes": "Effective for dropsy, columnaris, fin rot. Does not significantly harm biological filtration.",
                "notes_ja": "松かさ病、カラムナリス、尾ぐされ病に有効。生物ろ過への影響は少ない。",
            },
        },
    },
    {
        "id": "trichlorfon",
        "name": "Trichlorfon (Dipterex / Masoten)",
        "name_ja": "トリクロルホン（ジプテレックス / マゾテン）",
        "category": "antiparasitics",
        "category_ja": "駆虫薬・抗寄生虫薬",
        "description": "Organophosphate antiparasitic for anchor worms, fish lice, and gill flukes.",
        "description_ja": "イカリムシ、ウオジラミ、鰓吸虫に対する有機リン系駆虫薬。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "0.25-0.5 mg/L (ppm) prolonged bath; repeat weekly x3",
                "dosage_ja": "0.25-0.5 mg/L 長時間浴; 週1回×3回反復",
                "notes": "Toxic to invertebrates and some catfish. Decomposes in alkaline water (pH>8.5). Handle with gloves — organophosphate.",
                "notes_ja": "無脊椎動物・一部のナマズに毒性。アルカリ性の水（pH>8.5）で分解。有機リン系 — 手袋を着用。",
            },
        },
    },
    {
        "id": "levamisole_fish",
        "name": "Levamisole (Fish)",
        "name_ja": "レバミゾール（魚用）",
        "category": "antiparasitics",
        "category_ja": "駆虫薬・抗寄生虫薬",
        "description": "Anthelmintic used for nematodes and some external parasites in fish.",
        "description_ja": "魚の線虫・一部の外部寄生虫に使用される駆虫薬。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "2-5 mg/L prolonged bath for 24h; or 10 mg/kg in medicated feed",
                "dosage_ja": "2-5 mg/L 長時間浴 24時間; または 10 mg/kg 薬餌",
                "notes": "Effective for Camallanus (red worms). Do a large water change 24h after bath treatment.",
                "notes_ja": "カマラヌス（赤虫）に有効。薬浴24時間後に大量換水。",
            },
        },
    },
    {
        "id": "epsom_salt",
        "name": "Epsom Salt (Magnesium Sulfate)",
        "name_ja": "エプソムソルト（硫酸マグネシウム）",
        "category": "supplements",
        "category_ja": "サプリメント・支持療法",
        "description": "Osmotic agent used to reduce swelling and treat constipation/bloating in fish.",
        "description_ja": "魚の浮腫・便秘・膨満に使用される浸透圧剤。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "1-3 tablespoons per 20L (1-3 tsp/5 gal) prolonged bath",
                "dosage_ja": "20Lあたり大さじ1-3杯 長時間浴",
                "notes": "Helps with dropsy, swim bladder issues, and egg binding. Different from aquarium salt (NaCl).",
                "notes_ja": "松かさ病、浮袋障害、過抱卵に有効。アクアリウムソルト（NaCl）とは異なる。",
            },
        },
    },
    {
        "id": "aquarium_salt",
        "name": "Aquarium Salt (NaCl)",
        "name_ja": "アクアリウムソルト（塩化ナトリウム）",
        "category": "supplements",
        "category_ja": "サプリメント・支持療法",
        "description": "Non-iodized salt used for osmotic therapy, parasite treatment, and stress reduction in freshwater fish.",
        "description_ja": "淡水魚の浸透圧療法、寄生虫治療、ストレス軽減に使用される無ヨウ素塩。",
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "1-3 g/L (0.1-0.3%) prophylactic; 5-10 g/L (0.5-1%) therapeutic dip 15-30 min; 10-30 g/L (1-3%) short dip 1-5 min",
                "dosage_ja": "1-3 g/L (0.1-0.3%) 予防的; 5-10 g/L (0.5-1%) 治療的ディップ 15-30分; 10-30 g/L (1-3%) 短時間ディップ 1-5分",
                "notes": "Not suitable for all species (Corydoras, tetras, and other soft-water fish are salt-sensitive). Use non-iodized salt only.",
                "notes_ja": "全ての種に適するわけではない（コリドラス、テトラ等の軟水魚は塩に敏感）。無ヨウ素塩のみ使用。",
            },
        },
    },
]

# Existing drugs that also have fish dosages
FISH_SPECIES_INFO_PATCH: dict[str, dict] = {
    "metronidazole": {
        "fish": {
            "safe": True,
            "dosage": "5-10 mg/L bath for 24-48h, repeat x3; or 25-50 mg/kg in medicated feed q24h for 5-10 days",
            "dosage_ja": "5-10 mg/L 薬浴 24-48時間 3回反復; または 25-50 mg/kg 薬餌 24時間毎 5-10日間",
            "notes": "First-line for Hexamita/Spironucleus and hole-in-the-head disease. Remove carbon filtration during treatment.",
            "notes_ja": "ヘキサミタ/スピロヌクレウスと穴あき病の第一選択。治療中は活性炭ろ過を除去。",
        },
    },
    "praziquantel": {
        "fish": {
            "safe": True,
            "dosage": "2-10 mg/L bath for 3-6 hours; or 5-50 mg/kg in medicated feed",
            "dosage_ja": "2-10 mg/L 薬浴 3-6時間; または 5-50 mg/kg 薬餌",
            "notes": "Effective for gill and skin flukes (Dactylogyrus, Gyrodactylus), tapeworms. Safe for most fish species.",
            "notes_ja": "鰓・皮膚吸虫（ダクチロギルス、ギロダクチルス）、条虫に有効。ほとんどの魚種に安全。",
        },
    },
    "enrofloxacin": {
        "fish": {
            "safe": True,
            "dosage": "5-10 mg/L bath for 5 days; or 10 mg/kg in medicated feed q24h for 10 days",
            "dosage_ja": "5-10 mg/L 薬浴 5日間; または 10 mg/kg 薬餌 24時間毎 10日間",
            "notes": "Broad-spectrum fluoroquinolone for systemic bacterial infections.",
            "notes_ja": "全身性細菌感染に対する広域スペクトルフルオロキノロン。",
        },
    },
    "doxycycline": {
        "fish": {
            "safe": True,
            "dosage": "2.5-5 mg/L bath for 5-10 days",
            "dosage_ja": "2.5-5 mg/L 薬浴 5-10日間",
            "notes": "For bacterial infections, especially gram-positive. Photodegrades — use in dim lighting.",
            "notes_ja": "細菌感染、特にグラム陽性菌に使用。光分解する — 薄暗い照明で使用。",
        },
    },
    "itraconazole": {
        "fish": {
            "safe": True,
            "dosage": "1-5 mg/L bath for 7-14 days",
            "dosage_ja": "1-5 mg/L 薬浴 7-14日間",
            "notes": "For systemic mycosis. Limited fish data; monitor closely.",
            "notes_ja": "全身性真菌症に使用。魚でのデータは限られる。注意深く観察。",
        },
    },
    "fenbendazole": {
        "fish": {
            "safe": True,
            "dosage": "2 mg/L bath for 24h, repeat in 14 days; or 25-50 mg/kg in medicated feed q24h for 3 days",
            "dosage_ja": "2 mg/L 薬浴 24時間 14日後に反復; または 25-50 mg/kg 薬餌 24時間毎 3日間",
            "notes": "For internal nematodes (Camallanus, Capillaria). Repeat treatment important to catch life cycle.",
            "notes_ja": "内部線虫（カマラヌス、キャピラリア）に使用。生活環に合わせた反復治療が重要。",
        },
    },
    "chloramphenicol": {
        "fish": {
            "safe": True,
            "dosage": "20-50 mg/L bath for 5-7 days",
            "dosage_ja": "20-50 mg/L 薬浴 5-7日間",
            "notes": "Broad-spectrum; effective for resistant bacterial infections. Banned for food fish in many countries.",
            "notes_ja": "広域スペクトル。耐性菌感染に有効。多くの国で食用魚への使用は禁止。",
        },
    },
    "trimethoprim_sulfa": {
        "fish": {
            "safe": True,
            "dosage": "30-80 mg/L bath for 5-7 days; or 30-50 mg/kg in medicated feed q24h for 10 days",
            "dosage_ja": "30-80 mg/L 薬浴 5-7日間; または 30-50 mg/kg 薬餌 24時間毎 10日間",
            "notes": "Good for systemic bacterial infections. One of the safer antibiotics for fish.",
            "notes_ja": "全身性細菌感染に有効。魚にとって比較的安全な抗菌薬の一つ。",
        },
    },
    "ivermectin": {
        "fish": {
            "safe": False,
            "dosage": "N/A",
            "dosage_ja": "使用不可",
            "notes": "TOXIC to most fish species — causes acute mortality. Do NOT use in fish.",
            "notes_ja": "ほとんどの魚種に有毒 — 急性死亡を引き起こす。魚には使用しないこと。",
        },
    },
    "prednisolone": {
        "fish": {
            "safe": True,
            "dosage": "1-5 mg/kg IM/IP (large fish only)",
            "dosage_ja": "1-5 mg/kg 筋注/腹腔内（大型魚のみ）",
            "notes": "Anti-inflammatory for large koi/pond fish under veterinary supervision. Not practical for small aquarium fish.",
            "notes_ja": "獣医師の監督下で大型錦鯉/池魚の抗炎症に使用。小型水槽魚には実用的ではない。",
        },
    },
    "ketamine": {
        "fish": {
            "safe": True,
            "dosage": "1-2 mg/L bath immersion for sedation",
            "dosage_ja": "1-2 mg/L 浸漬浴で鎮静",
            "notes": "Fish anesthesia/sedation for examination or procedures. MS-222 (tricaine) is more commonly used.",
            "notes_ja": "検査や処置のための魚の麻酔/鎮静。MS-222（トリカイン）がより一般的に使用される。",
        },
    },
}
