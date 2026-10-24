"""Drug batch 85 – 2026-10 第76弾 (referenced-but-absent sweep #39).

1. Deltamethrin 4% collar (Scalibor Protectorband) — the reference sand-fly
   repellent for prevention of canine leishmaniasis. The dog leishmaniasis
   entries (prevention and the post-treatment transmission-control line) now
   name it, but there was no monograph, and deltamethrin otherwise appeared in
   the dictionary only as a toxin in the pyrethroid toxicosis entries.
   Evidence: Killick-Kendrick R et al. Protection of dogs from bites of
   phlebotomine sandflies by deltamethrin collars for control of canine
   leishmaniasis. Med Vet Entomol 1997;11:105-111. Maroli M et al. Evidence for
   an impact on the incidence of canine leishmaniasis by the mass use of
   deltamethrin-impregnated dog collars in southern Italy. Med Vet Entomol
   2001;15:358-363. Foglia Manzillo V et al. Deltamethrin-impregnated collars
   for the control of canine leishmaniasis: evaluation of the protective effect
   and influence on the clinical outcome of Leishmania infection in kennelled
   stray dogs. Vet Parasitol 2006;142:142-145. Solano-Gallego L et al. LeishVet
   guidelines. Parasit Vectors 2011;4:86. Scalibor Protectorband SPC (MSD
   Animal Health). Toxic to cats (pyrethroid) and to aquatic organisms.
"""

DRUGS_BATCH_85 = [
    {
        "id": "deltamethrin_collar",
        "search_aliases": [
            "デルタメトリン",
            "でるためとりん",
            "デルタメトリン首輪",
            "スカリボール",
            "Scalibor",
            "Scalibor Protectorband",
            "deltamethrin",
        ],
        "name": "Deltamethrin 4% collar (Scalibor)",
        "name_ja": "デルタメトリン4%首輪（スカリボール）",
        "category": "antiparasitic",
        "mechanism": (
            "Synthetic pyrethroid released from a polymer collar into the skin lipid layer. Its repellent "
            "(anti-feeding) effect stops most phlebotomine sand flies from taking a blood meal, which is what "
            "prevents transmission of Leishmania infantum; it also repels/kills ticks and mosquitoes. Acts on "
            "insect voltage-gated sodium channels."
        ),
        "mechanism_ja": (
            "ポリマー製首輪から皮膚脂質層に放出される合成ピレスロイド。忌避（吸血阻止）作用によりサシチョウバエの吸血を"
            "大部分阻止し、これがLeishmania infantumの伝播予防の機序となる。マダニ・蚊にも忌避・殺虫作用を示す。"
            "昆虫の電位依存性ナトリウムチャネルに作用する。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "One collar (4% deltamethrin): 48 cm collar for small/medium dogs, 65 cm collar for large dogs; "
                    "fit snugly with two fingers' room and cut off the excess. Repellent effect against sand flies "
                    "develops over about 1 week and lasts 5-6 months; ticks up to 6 months. Fit before the "
                    "sand-fly season and replace for the whole season. From 7 weeks of age."
                ),
                "dosage_ja": (
                    "首輪1本（デルタメトリン4%）：小〜中型犬は48 cm、大型犬は65 cm。指2本が入る程度に装着し余分は切る。"
                    "サシチョウバエへの忌避効果は約1週間で発現し5〜6ヶ月持続、マダニには最長6ヶ月。"
                    "サシチョウバエの活動期の前に装着し、活動期を通じて交換しながら継続する。7週齢以上。"
                ),
                "notes": (
                    "Mainstay of leishmaniasis prevention for dogs in or travelling to endemic areas; also used in "
                    "seropositive or treated dogs to stop onward transmission (treated dogs stay infectious to sand "
                    "flies). Mass use reduced the incidence of canine leishmaniasis in an endemic area "
                    "(Maroli 2001). Combine with indoor housing at dusk/dawn. Avoid swimming for 5 days after "
                    "fitting; deltamethrin is highly toxic to fish and aquatic invertebrates."
                ),
                "notes_ja": (
                    "流行地に住む犬・渡航する犬のリーシュマニア症予防の中心。血清陽性犬や治療中・治療後の犬にも、"
                    "サシチョウバエを介した他の犬への伝播を防ぐ目的で装着する（治療後も感染源となる）。"
                    "流行地での集団使用で犬リーシュマニア症の発生が減少した（Maroli 2001）。夕方〜明け方の屋内飼育と併用する。"
                    "装着後5日間は水泳を避ける（魚類・水生生物に強い毒性）。"
                ),
            },
            "cat": {
                "safe": False,
                "dosage": "Do not use — pyrethroids are toxic to cats. For feline leishmaniasis prevention use the imidacloprid/flumethrin collar.",
                "dosage_ja": "使用しない — ピレスロイドは猫に有毒。猫のリーシュマニア症予防にはイミダクロプリド/フルメトリン首輪を使う。",
                "notes": "Keep cats from prolonged close contact with a newly collared dog (sleeping together, grooming the collar).",
                "notes_ja": "装着直後の犬と猫を長時間密着させない（同じ寝床、首輪を舐める等）。",
            },
        },
        "contraindications": (
            "Cats; puppies under 7 weeks; dogs with extensive skin lesions; known pyrethroid hypersensitivity. "
            "Not for use in fish ponds or where the dog swims daily."
        ),
        "contraindications_ja": (
            "猫、7週齢未満の子犬、広範な皮膚病変のある犬、ピレスロイド過敏症。"
            "日常的に泳ぐ犬・池のある環境では使用を避ける。"
        ),
        "side_effects": [
            "Local erythema, pruritus or alopecia under the collar (remove collar)",
            "Rarely ataxia, tremors or vomiting, mainly if the collar is chewed or ingested",
        ],
        "side_effects_ja": [
            "首輪の下の発赤・掻痒・脱毛（首輪を外す）",
            "まれに運動失調・振戦・嘔吐（主に首輪をかじった・飲み込んだ場合）",
        ],
        "drug_interactions": [
            {
                "drug": "Organophosphate insecticides",
                "severity": "moderate",
                "description": "Do not combine with organophosphate ectoparasiticides (additive neurotoxicity).",
                "description_ja": "有機リン系外部寄生虫駆除剤と併用しない（神経毒性の相加）。",
            },
            {
                "drug": "Permethrin",
                "severity": "moderate",
                "description": "Avoid stacking with other pyrethroid spot-ons; one repellent pyrethroid product is enough.",
                "description_ja": "他のピレスロイド系スポットオンと重ねない（忌避剤は1製剤で十分）。",
            },
        ],
        "references": [
            "Killick-Kendrick R et al. Med Vet Entomol 1997;11:105-111",
            "Maroli M et al. Med Vet Entomol 2001;15:358-363",
            "Foglia Manzillo V et al. Vet Parasitol 2006;142:142-145",
            "Solano-Gallego L et al. LeishVet guidelines. Parasit Vectors 2011;4:86",
            "Scalibor Protectorband SPC (MSD Animal Health)",
        ],
    },
]
