"""Drug batch 77 – 2026-10 session (第70弾).

Two widely used, label-defined parasiticide combinations that the dictionary
lacked (the single-agent components were present, but the combination
products — with their own minimum doses, age/weight limits and heartworm
claims — were not, so a vet searching the brand got nothing):

- Fluralaner + moxidectin topical solution for cats (Bravecto Plus):
  FDA NADA 141-518 (2019); EU authorised. Every 2 months: fleas/ticks,
  heartworm (Dirofilaria immitis) prevention, and treatment of roundworm
  (Toxocara cati) and hookworm (Ancylostoma tubaeforme); EU label also
  ear mites.
- Afoxolaner + moxidectin + pyrantel chewable for dogs (NexGard PLUS):
  FDA approval 2023. Monthly: fleas/ticks, heartworm prevention,
  roundworm/hookworm treatment. (Japan's domestic analogue is NexGard
  Spectra — afoxolaner + milbemycin oxime — which is already listed.)

Evidence: US labels (DailyMed); Plumb's Veterinary Drug Handbook 10th ed;
American Heartworm Society guidelines (test before starting a preventive);
Rohdich N et al. Parasit Vectors 2018 (fluralaner/moxidectin in cats).
"""

_ISOX_NOTE_EN = (
    "Isoxazoline class warning: neurologic adverse reactions (tremor, ataxia, seizures) have been reported, "
    "including in animals without a seizure history — use with caution in animals with neurologic disorders. "
)
_ISOX_NOTE_JA = (
    "イソキサゾリン系のクラス警告: 神経系の副作用（振戦・運動失調・痙攣）が報告されており、発作歴のない動物でも起こりうる"
    " — 神経疾患のある動物には慎重に使用する。"
)

DRUGS_BATCH_77 = [
    {
        "id": "fluralaner_moxidectin_topical",
        "search_aliases": [
            "ブラベクトプラス",
            "ブラベクト プラス",
            "ブラベクトプラス猫用",
            "Bravecto Plus",
            "bravecto plus",
            "フルララネル・モキシデクチン",
            "フルララネル＋モキシデクチン",
            "fluralaner/moxidectin",
        ],
        "name": "Fluralaner / Moxidectin topical (Bravecto Plus)",
        "name_ja": "フルララネル・モキシデクチン スポットオン（ブラベクトプラス）",
        "category": "antiparasitics",
        "mechanism": "Fluralaner (isoxazoline) blocks arthropod GABA- and glutamate-gated chloride channels (fleas, ticks, mites); moxidectin (macrocyclic lactone) opens invertebrate glutamate-gated chloride channels, killing heartworm larvae and intestinal nematodes. The long fluralaner half-life gives a 2-month dosing interval.",
        "mechanism_ja": "フルララネル（イソキサゾリン系）が節足動物のGABA・グルタミン酸作動性クロライドチャネルを阻害（ノミ・マダニ・ダニ）、モキシデクチン（大環状ラクトン系）が無脊椎動物のグルタミン酸作動性クロライドチャネルを開口し、犬糸状虫幼虫と消化管線虫を駆除する。フルララネルの長い半減期により2ヶ月間隔で投与する。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Topical every 2 months at a minimum of 40 mg/kg fluralaner + 2 mg/kg moxidectin (dose band by body weight; label range 40-94 / 2-4.7 mg/kg). Cats and kittens >= 6 months of age and >= 1.2 kg (2.6 lb). Claims: fleas and ticks (2 months), heartworm prevention (Dirofilaria immitis), treatment of roundworm (Toxocara cati) and hookworm (Ancylostoma tubaeforme); EU label also ear mites (Otodectes).",
                "dosage_ja": "2ヶ月毎に外用（最低用量 フルララネル 40 mg/kg＋モキシデクチン 2 mg/kg、体重帯別製剤。ラベル範囲 40-94 / 2-4.7 mg/kg）。生後6ヶ月以上かつ体重1.2 kg以上の猫。効能: ノミ・マダニ（2ヶ月）、犬糸状虫（フィラリア）予防、猫回虫・猫鉤虫の駆除。EUラベルは耳ダニ（ミミヒゼンダニ）も含む。",
                "notes": "Apply to the skin at the base of the skull where the cat cannot lick; avoid contact with the site until dry. Heartworm preventive: test for existing infection per local guidance before starting (cats are non-permissive hosts — adulticides are not used in cats). "
                + _ISOX_NOTE_EN
                + "Most common reactions: vomiting, transient hair loss/pruritus at the application site. Not established in breeding, pregnant or lactating cats. Follow the domestic package insert where a local product exists.",
                "notes_ja": "猫が舐められない後頭部の皮膚に滴下し、乾くまで接触させない。フィラリア予防として開始前に既存感染を地域の指針に従って評価する（猫は非好適宿主で成虫駆除薬は用いない）。"
                + _ISOX_NOTE_JA
                + "主な副作用は嘔吐、塗布部位の一過性脱毛・掻痒。繁殖・妊娠・授乳中の猫での安全性は未確立。国内製品がある場合は添付文書に従う。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not for dogs — this is the feline formulation. Use canine fluralaner products (Bravecto chewable/topical/Quantum) with a separate heartworm preventive, or a canine combination product.",
                "dosage_ja": "犬には使用しない（猫用製剤）。犬は犬用フルララネル製剤（ブラベクト錠/スポット/クオンタム）＋別途フィラリア予防薬、または犬用配合剤を用いる。",
                "notes": "Species-specific formulation and dose bands.",
                "notes_ja": "動物種別の製剤・体重帯である。",
            },
        },
        "contraindications": "Cats < 6 months of age or < 1.2 kg; known hypersensitivity to either ingredient. Use with caution in cats with a history of neurologic disorders.",
        "contraindications_ja": "生後6ヶ月未満または体重1.2 kg未満の猫、成分に対する過敏症。神経疾患の既往がある猫には慎重に使用。",
        "side_effects": [
            "Vomiting",
            "Application-site hair loss, pruritus or scabbing",
            "Neurologic signs (tremor, ataxia, seizures) — isoxazoline class warning",
            "Lethargy / inappetence",
        ],
        "side_effects_ja": [
            "嘔吐",
            "塗布部位の脱毛・掻痒・痂皮",
            "神経症状（振戦・運動失調・痙攣）— イソキサゾリン系のクラス警告",
            "元気消失・食欲低下",
        ],
        "drug_interactions": [
            {
                "drug": "Other isoxazolines (fluralaner, sarolaner, lotilaner)",
                "effect": "Duplicate isoxazoline exposure — do not stack products",
                "effect_ja": "イソキサゾリン系の重複 — 製品を重ねない",
                "severity": "moderate",
            },
            {
                "drug": "Other macrocyclic lactones (selamectin, ivermectin, milbemycin)",
                "effect": "Duplicate macrocyclic lactone — no added benefit for heartworm prevention",
                "effect_ja": "大環状ラクトン系の重複 — フィラリア予防の上乗せ効果なし",
                "severity": "moderate",
            },
        ],
        "references": [
            "Bravecto Plus (fluralaner and moxidectin topical solution) for cats — US label, FDA NADA 141-518 (2019)",
            "Rohdich N et al. Efficacy of fluralaner plus moxidectin spot-on in cats. Parasit Vectors 2018.",
            "American Heartworm Society. Current Feline Guidelines for the Prevention, Diagnosis, and Management of Heartworm Infection in Cats.",
            "Plumb's Veterinary Drug Handbook, 10th ed. — Fluralaner",
        ],
    },
    {
        "id": "afoxolaner_moxidectin_pyrantel",
        "search_aliases": [
            "ネクスガードプラス",
            "ネクスガード プラス",
            "NexGard PLUS",
            "Nexgard Plus",
            "nexgard plus",
            "アフォキソラネル・モキシデクチン・ピランテル",
        ],
        "name": "Afoxolaner / Moxidectin / Pyrantel chewable (NexGard PLUS)",
        "name_ja": "アフォキソラネル・モキシデクチン・ピランテル（ネクスガードプラス）",
        "category": "antiparasitics",
        "mechanism": "Afoxolaner (isoxazoline) kills fleas and ticks via arthropod chloride-channel blockade; moxidectin (macrocyclic lactone) prevents heartworm by killing tissue-stage larvae; pyrantel (tetrahydropyrimidine, nicotinic agonist) causes spastic paralysis of roundworms and hookworms.",
        "mechanism_ja": "アフォキソラネル（イソキサゾリン系）が節足動物のクロライドチャネル阻害でノミ・マダニを駆除、モキシデクチン（大環状ラクトン系）が組織移行期の幼虫を駆除してフィラリアを予防、ピランテル（ニコチン受容体作動薬）が回虫・鉤虫を痙性麻痺させる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Orally once a month at a minimum of 2.5 mg/kg afoxolaner + 24 µg/kg (0.024 mg/kg) moxidectin + 5 mg/kg pyrantel (as pamoate), by body-weight band. Dogs >= 8 weeks of age and >= 1.8 kg (4 lb). Claims: fleas and ticks, heartworm prevention, treatment/control of roundworm (Toxocara canis, Toxascaris leonina) and hookworm (Ancylostoma caninum, A. braziliense, Uncinaria stenocephala).",
                "dosage_ja": "月1回経口（最低用量 アフォキソラネル 2.5 mg/kg＋モキシデクチン 24 µg/kg（0.024 mg/kg）＋ピランテル（パモ酸塩）5 mg/kg、体重帯別）。生後8週齢以上かつ体重1.8 kg以上の犬。効能: ノミ・マダニ、犬糸状虫（フィラリア）予防、犬回虫・犬小回虫・鉤虫の駆除。",
                "notes": "Test for existing heartworm infection before starting (American Heartworm Society) — preventives do not kill adult worms. The preventive moxidectin dose was evaluated in ABCB1 (MDR1)-deficient collies at multiples of the label dose. "
                + _ISOX_NOTE_EN
                + "Common reactions: vomiting, diarrhoea, lethargy, pruritus. Not licensed in Japan — the domestic analogue is NexGard Spectra (afoxolaner + milbemycin oxime).",
                "notes_ja": "開始前にフィラリアの既存感染を検査する（米国犬糸状虫学会）— 予防薬は成虫を駆除しない。予防用量のモキシデクチンはABCB1（MDR1）欠損コリーでラベル用量の数倍で評価済み。"
                + _ISOX_NOTE_JA
                + "主な副作用: 嘔吐・下痢・元気消失・掻痒。国内未承認 — 国内の類似製剤はネクスガードスペクトラ（アフォキソラネル＋ミルベマイシンオキシム）。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not for cats (canine product). Use a feline-licensed product (e.g. Bravecto Plus, Revolution Plus).",
                "dosage_ja": "猫には使用しない（犬用製品）。猫用の承認製剤（ブラベクトプラス、レボリューションプラス等）を用いる。",
                "notes": "Species-specific product.",
                "notes_ja": "動物種別の製品である。",
            },
        },
        "contraindications": "Dogs < 8 weeks of age or < 1.8 kg; known hypersensitivity. Existing heartworm infection must be diagnosed first. Use with caution in dogs with a history of seizures or neurologic disorders.",
        "contraindications_ja": "生後8週齢未満または体重1.8 kg未満の犬、成分に対する過敏症。フィラリアの既存感染は事前に診断しておく。発作・神経疾患の既往がある犬には慎重に使用。",
        "side_effects": [
            "Vomiting / diarrhoea",
            "Lethargy, inappetence",
            "Pruritus",
            "Neurologic signs (tremor, ataxia, seizures) — isoxazoline class warning",
        ],
        "side_effects_ja": [
            "嘔吐・下痢",
            "元気消失・食欲低下",
            "掻痒",
            "神経症状（振戦・運動失調・痙攣）— イソキサゾリン系のクラス警告",
        ],
        "drug_interactions": [
            {
                "drug": "Other isoxazolines (fluralaner, sarolaner, lotilaner)",
                "effect": "Duplicate isoxazoline exposure — do not stack products",
                "effect_ja": "イソキサゾリン系の重複 — 製品を重ねない",
                "severity": "moderate",
            },
            {
                "drug": "High-dose ivermectin / other macrocyclic lactones",
                "effect": "Additive macrocyclic-lactone neurotoxicity risk, especially in ABCB1-mutant breeds",
                "effect_ja": "大環状ラクトン系の神経毒性の相加（特にABCB1変異犬種）",
                "severity": "moderate",
            },
        ],
        "references": [
            "NexGard PLUS (afoxolaner, moxidectin, and pyrantel chewable tablets) — US label, FDA approval 2023",
            "American Heartworm Society. Current Canine Guidelines for the Prevention, Diagnosis, and Management of Heartworm Infection in Dogs (2024).",
            "Plumb's Veterinary Drug Handbook, 10th ed. — Afoxolaner; Moxidectin; Pyrantel",
        ],
    },
]
