"""Drug batch 91 – 2026-11 第83弾.

Fipronil + (S)-methoprene + eprinomectin + praziquantel spot-on for cats
(Broadline, Boehringer Ingelheim; EU 2013, USA 2015). A widely used monthly
feline broad-spectrum parasiticide (fleas, ticks, roundworms, hookworms,
tapeworms including Dipylidium and Echinococcus multilocularis, lungworm,
heartworm prevention) that was absent from the dictionary, so cat flea /
tapeworm / heartworm protocols could not point to it. Component stems are not
indexed so that the bare words「フィプロニル」「プラジクアンテル」keep
resolving to their single-agent monographs.
Evidence: Broadline spot-on solution for cats — Summary of Product
Characteristics (EMA, EMEA/V/C/002700); Broadline US label (Boehringer
Ingelheim); Knaus M, et al. Efficacy of a novel topical combination of
fipronil, (S)-methoprene, eprinomectin and praziquantel against feline
endoparasites. Vet Parasitol 2014;202:34-39; Rehbein S, et al. Vet Parasitol
2014;202:10-17.
"""

DRUGS_BATCH_91 = [
    {
        "id": "fipronil_methoprene_eprinomectin_praziquantel",
        "no_component_index": True,
        "search_aliases": [
            "ブロードライン",
            "Broadline",
            "フィプロニル・メトプレン・エプリノメクチン・プラジクアンテル",
        ],
        "name": "Fipronil / (S)-Methoprene / Eprinomectin / Praziquantel Spot-on (Broadline)",
        "name_ja": "フィプロニル・(S)-メトプレン・エプリノメクチン・プラジクアンテル スポットオン（ブロードライン）",
        "category": "antiparasitics",
        "mechanism": "Four-agent feline spot-on: fipronil (GABA-gated chloride channel blocker — fleas, ticks), (S)-methoprene (insect growth regulator — prevents development of flea eggs and larvae), eprinomectin (macrocyclic lactone — nematodes and heartworm larvae) and praziquantel (tegument damage — cestodes).",
        "mechanism_ja": "猫用の4成分配合スポットオン: フィプロニル（GABA作動性クロライドチャネル阻害 — ノミ・マダニ）、(S)-メトプレン（昆虫成長制御剤 — ノミ卵・幼虫の発育阻止）、エプリノメクチン（大環状ラクトン — 線虫・犬糸状虫幼虫）、プラジクアンテル（外皮傷害 — 条虫）。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Minimum 0.12 mL/kg = fipronil 10 mg/kg + (S)-methoprene 12 mg/kg + eprinomectin 0.5 mg/kg + praziquantel 10 mg/kg, applied once to the skin at the base of the neck. Small applicator (0.3 mL) for cats 0.6-<2.5 kg; large applicator (0.9 mL) for 2.5-7.5 kg; combine applicators above 7.5 kg. Single treatment for intestinal worms; monthly for flea/tick control and heartworm prevention (product SPC/label).",
                "dosage_ja": "最低 0.12 mL/kg（フィプロニル 10 mg/kg＋(S)-メトプレン 12 mg/kg＋エプリノメクチン 0.5 mg/kg＋プラジクアンテル 10 mg/kg）を首の付け根の皮膚に1回滴下。0.6〜2.5 kg未満は小容量（0.3 mL）、2.5〜7.5 kgは大容量（0.9 mL）、7.5 kg超は組み合わせる。消化管内寄生虫は単回、ノミ・マダニ対策と犬糸状虫予防は月1回（添付文書）。",
                "notes": "Kittens from 7 weeks of age and 0.6 kg. Flea control lasts about a month (ticks about 3 weeks). Indicated against roundworms, hookworms, tapeworms (Dipylidium caninum, Echinococcus multilocularis), lungworm (Aelurostrongylus abstrusus) and for heartworm prevention. Apply where the cat cannot lick it — oral contact causes transient hypersalivation; local hair clumping/discolouration may occur. Treat all in-contact animals and the environment for fleas (Dipylidium is flea-borne). Follow the national label.",
                "notes_ja": "7週齢以上・0.6 kg以上の子猫から使用可。ノミへの効果は約1か月（マダニは約3週間）。回虫・鉤虫・条虫（瓜実条虫・多包条虫）・肺虫（猫肺虫）に有効で、犬糸状虫の予防にも用いる。舐められない部位に滴下する（経口摂取で一過性の流涎）。滴下部位の被毛の束状化・変色が起こることがある。瓜実条虫はノミが媒介するため、同居動物と環境のノミ対策を併せて行う。国内の添付文書に従う。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not for dogs — cat-only product; no canine dose.",
                "dosage_ja": "犬には使用しない（猫専用製剤・犬の用量はない）。",
                "notes": "Use a canine-labelled parasiticide.",
                "notes_ja": "犬用に承認された駆虫薬を用いる。",
            },
            "rabbit": {
                "safe": False,
                "dosage": "Contraindicated — fipronil causes fatal toxicity in rabbits.",
                "dosage_ja": "禁忌 — フィプロニルはウサギで致死的な中毒を起こす。",
                "notes": "Never use fipronil-containing products in rabbits.",
                "notes_ja": "フィプロニル含有製剤はウサギに絶対に使用しない。",
            },
        },
        "contraindications": "Rabbits (fipronil toxicity); dogs (no canine authorisation); sick or debilitated cats; broken skin at the application site; hypersensitivity to any component.",
        "contraindications_ja": "ウサギ（フィプロニル中毒）、犬（承認なし）、病気・衰弱した猫、滴下部位の皮膚損傷、成分への過敏症。",
        "side_effects": [
            "Transient hypersalivation if licked",
            "Local hair clumping or discolouration",
            "Transient application-site pruritus",
        ],
        "side_effects_ja": [
            "舐めた場合の一過性の流涎",
            "滴下部位の被毛の束状化・変色",
            "滴下部位の一過性の痒み",
        ],
        "drug_interactions": [
            {
                "drug": "Selamectin",
                "effect": "Duplicates macrocyclic-lactone cover (heartworm/nematodes) — do not stack products from the same class.",
                "effect_ja": "大環状ラクトンの重複（犬糸状虫・線虫）— 同系統の製剤を重ねて使わない。",
                "severity": "moderate",
            },
            {
                "drug": "Moxidectin",
                "effect": "Duplicates macrocyclic-lactone cover — avoid combining with other moxidectin/milbemycin products.",
                "effect_ja": "大環状ラクトンの重複 — 他のモキシデクチン・ミルベマイシン製剤と併用しない。",
                "severity": "moderate",
            },
            {
                "drug": "Fipronil",
                "effect": "Same active substance — do not apply another fipronil product in the same month.",
                "effect_ja": "同一成分 — 同じ月に他のフィプロニル製剤を重ねて使わない。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Broadline spot-on solution for cats — Summary of Product Characteristics (EMA, EMEA/V/C/002700; Boehringer Ingelheim).",
            "Knaus M, Chester ST, Rosentel J, Kühnert A, Rehbein S. Efficacy of a novel topical combination of fipronil, (S)-methoprene, eprinomectin and praziquantel against larval and adult stages of ascarids, hookworms and tapeworms in cats. Vet Parasitol 2014;202:34-39.",
            "Rehbein S, Capári B, Duscher G, et al. Efficacy against nematode and cestode infections and safety of a novel topical fipronil, (S)-methoprene, eprinomectin and praziquantel combination product in domestic cats under field conditions in Europe. Vet Parasitol 2014;202:10-17.",
        ],
    },
]
