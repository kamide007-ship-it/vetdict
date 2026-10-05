"""Drug batch 69 – 2026-10 audit (第62弾): referenced-but-absent agents.

Detected by the English drug-token sweep (dose-context tokens matched
against the real find_drugs_in_text matcher):

  - EPSIPRANTEL (Cestex) — 11 tapeworm entries across species dose it
    ("Epsiprantel 5.5 mg/kg PO single dose") yet the only cestocide in
    the dictionary was praziquantel.  The same sweep exposed a dose
    ERROR in the disease texts: the label cat dose is 2.75 mg/kg, not
    5.5 mg/kg — the texts said "(dogs/cats)" for the dog dose.  Fixed
    in diseases_all_species.json alongside this batch.
  - DAPSONE — the canine refractory-vasculitis and rhinosporidiosis
    entries dose it ("Dapsone 1 mg/kg PO q8h ... monitor for
    methemoglobinemia"; JA「ダプソン 1 mg/kg PO q8h — 定期的なCBC監視
    必須」) yet no sulfone existed in the dictionary.  Cats are a
    hard safety gate (hemolytic anemia / neurotoxicity — not
    recommended, Plumb's).

References:
  - CESTEX (epsiprantel) US label, NADA 140-893 (Zoetis) — dogs
    5.5 mg/kg PO, cats 2.75 mg/kg PO, single dose; not for animals
    under 7 weeks of age.
  - Plumb's Veterinary Drug Handbook 10th ed — epsiprantel and
    dapsone monographs.
  - Manning TO, et al. Dapsone in canine dermatology (cutaneous
    vasculitis, pemphigus adjunct); Muller & Kirk's Small Animal
    Dermatology 7th ed — dapsone monitoring (CBC, hepatic,
    methemoglobin) and feline toxicity.
  - ESCCAP GL1 / CAPC tapeworm guidance — flea control essential for
    Dipylidium; praziquantel (not epsiprantel) for Echinococcus.
"""

DRUGS_BATCH_69 = [
    {
        "id": "epsiprantel",
        "search_aliases": [
            "エプシプランテル",
            "セステックス",
            "cestex",
        ],
        "name": "Epsiprantel (Cestex)",
        "name_ja": "エプシプランテル（セステックス）",
        "category": "antiparasitics",
        "mechanism": "Cestocidal pyrazinoisoquinoline (praziquantel analogue). Disrupts the tapeworm's tegument calcium homeostasis, causing paralysis and loss of attachment; the worm is digested in the gut. Defining pharmacologic property: essentially NOT absorbed from the GI tract (<0.1% systemic exposure) — it acts purely in the intestinal lumen, which is why systemic toxicity is minimal but it has no activity against larval/tissue cestode stages.",
        "mechanism_ja": "ピラジノイソキノリン系の条虫駆除薬（プラジカンテルの類縁体）。条虫体表（テグメント）のカルシウム恒常性を破綻させて麻痺・固着喪失を起こし、虫体は腸管内で消化される。定義的な薬理特性: 消化管からほぼ吸収されない（全身曝露 <0.1%）— 作用は腸管腔内に限局するため全身毒性が極めて少ない一方、幼虫・組織内ステージの条虫には無効。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5.5 mg/kg PO single dose (label). Repeat in 2-3 weeks if reinfection is suspected. Indicated for Dipylidium caninum and Taenia pisiformis.",
                "dosage_ja": "5.5 mg/kg PO 単回（ラベル用量）。再感染が疑われる場合は2-3週間後に再投与。適応: 瓜実条虫（Dipylidium caninum）・テニア条虫（Taenia pisiformis）。",
                "notes": "Flea control is essential with Dipylidium (flea is the intermediate host — without it reinfection is the rule). NOT labeled for Echinococcus: where Echinococcus multilocularis is a concern (e.g., Hokkaido), praziquantel is the drug of choice. Not for puppies under 7 weeks.",
                "notes_ja": "瓜実条虫ではノミ対策が必須（ノミが中間宿主 — 対策なしでは再感染が常）。エキノコックスには適応外: 多包条虫（E. multilocularis）が問題となる地域（北海道等）ではプラジカンテルが第一選択。7週齢未満の子犬には使用しない。",
            },
            "cat": {
                "safe": True,
                "dosage": "2.75 mg/kg PO single dose (label — HALF the canine dose; do not carry the dog dose over to cats). Repeat in 2-3 weeks if reinfection is suspected. Indicated for Dipylidium caninum and Taenia taeniaeformis.",
                "dosage_ja": "2.75 mg/kg PO 単回（ラベル用量 — **犬用量の半分**。犬の5.5 mg/kgを猫に流用しない）。再感染が疑われる場合は2-3週間後に再投与。適応: 瓜実条虫・猫条虫（Taenia taeniaeformis）。",
                "notes": "Well tolerated (minimal absorption). Flea control essential for Dipylidium. Not for kittens under 7 weeks.",
                "notes_ja": "忍容性良好（ほぼ非吸収）。瓜実条虫ではノミ対策が必須。7週齢未満の子猫には使用しない。",
            },
        },
        "side_effects": [
            "Vomiting (uncommon)",
            "Diarrhea (uncommon)",
            "Tapeworm segments may not be seen after treatment (worms are digested — absence of segments does not mean failure or success)",
        ],
        "side_effects_ja": [
            "嘔吐（まれ）",
            "下痢（まれ）",
            "投与後に片節が見えないことがある（虫体は消化されるため、片節の有無で成否を判定しない）",
        ],
        "contraindications": "Not for puppies/kittens under 7 weeks of age; no activity against nematodes, trematodes, or larval (tissue) cestode stages; not a substitute for praziquantel where Echinococcus coverage is required",
        "contraindications_ja": "7週齢未満の子犬・子猫には使用しない。線虫・吸虫・条虫の幼虫（組織内）ステージには無効。エキノコックス対策が必要な場面でプラジカンテルの代替にはならない",
        "drug_interactions": [],
    },
    {
        "id": "dapsone",
        "search_aliases": [
            "ダプソン",
            "ジアフェニルスルホン",
        ],
        "name": "Dapsone",
        "name_ja": "ダプソン",
        "category": "immunosuppressives",
        "mechanism": "Sulfone with dual action: antimicrobial (folate-pathway inhibition, mycobacteria/some protozoa) and — the reason it appears in this formulary — anti-inflammatory via inhibition of neutrophil myeloperoxidase and chemotaxis. Used in dogs as an adjunct for neutrophilic/immune-mediated dermatoses (cutaneous vasculitis, pemphigus complex adjunct, symmetrical lupoid onychodystrophy) and reported to suppress recurrence after excision of rhinosporidiosis (Rhinosporidium seeberi — a mesomycetozoean, not a true fungus; antifungals are ineffective).",
        "mechanism_ja": "スルホン系薬。二重の作用を持つ: 抗微生物作用（葉酸経路阻害 — 抗酸菌・一部原虫）と、本辞書での使用理由である抗炎症作用（好中球ミエロペルオキシダーゼ・遊走の阻害）。犬では好中球性・免疫介在性皮膚疾患（皮膚血管炎、天疱瘡群の補助、対称性ループス様爪異栄養症）の補助薬として、またライノスポリジウム症（Rhinosporidium seeberi — 真の真菌ではない中間的微生物で抗真菌薬無効）の切除後再発抑制の報告がある。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1 mg/kg PO q8-12h for refractory immune-mediated dermatoses (cutaneous vasculitis, pemphigus adjunct, SLO); taper to the lowest effective frequency once controlled. Rhinosporidiosis recurrence suppression: 1 mg/kg PO q8h as a post-surgical adjunct (limited evidence).",
                "dosage_ja": "難治性の免疫介在性皮膚疾患（皮膚血管炎・天疱瘡補助・対称性ループス様爪異栄養症）: 1 mg/kg PO q8-12h。コントロール後は最小有効頻度へ漸減。ライノスポリジウム症の切除後再発抑制: 1 mg/kg PO q8h（エビデンス限定的・外科補助）。",
                "notes": "Mandatory monitoring: CBC with platelets and liver enzymes every 2-3 weeks initially, then every 3-4 months — hemolytic anemia, methemoglobinemia, thrombocytopenia, neutropenia and hepatotoxicity are the dose-limiting toxicities. Stop for cyanosis/brown blood (methemoglobinemia) or cytopenias. Second-line agent: use when pentoxifylline/steroid-sparing standards fail.",
                "notes_ja": "モニタリング必須: 開始初期は2-3週毎に血小板込みCBC+肝酵素、安定後も3-4ヶ月毎 — 溶血性貧血・メトヘモグロビン血症・血小板減少・好中球減少・肝毒性が用量規制毒性。チアノーゼ/血液の褐色化（メトヘモグロビン血症）や血球減少で中止。第二選択薬: ペントキシフィリン・ステロイド節約標準療法が不奏効の難治例に用いる。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not recommended in cats",
                "dosage_ja": "猫には推奨されない",
                "notes": "Cats are markedly sensitive — hemolytic anemia and neurotoxicity are reported at clinical doses (Plumb's); safer alternatives exist for feline immune-mediated skin disease",
                "notes_ja": "猫は感受性が顕著に高く、臨床用量で溶血性貧血・神経毒性の報告がある（Plumb's）。猫の免疫介在性皮膚疾患にはより安全な代替薬を選ぶ",
            },
        },
        "side_effects": [
            "Hemolytic anemia (dose-related)",
            "Methemoglobinemia (cyanosis, brown-tinged blood)",
            "Thrombocytopenia, neutropenia",
            "Hepatotoxicity (elevated liver enzymes)",
            "Cutaneous drug eruptions (paradoxical — discontinue)",
        ],
        "side_effects_ja": [
            "溶血性貧血（用量依存性）",
            "メトヘモグロビン血症（チアノーゼ・血液の褐色化）",
            "血小板減少・好中球減少",
            "肝毒性（肝酵素上昇）",
            "皮膚薬疹（逆説的 — 発現時は中止）",
        ],
        "contraindications": "Cats (hemolysis/neurotoxicity); sulfonamide/sulfone hypersensitivity; pre-existing anemia, hepatopathy or cytopenias; do not use without scheduled CBC and hepatic monitoring",
        "contraindications_ja": "猫（溶血・神経毒性）。スルホンアミド/スルホン過敏症。既存の貧血・肝障害・血球減少。定期的なCBC・肝酵素モニタリングなしでの使用は不可",
        "drug_interactions": [
            {
                "drug": "Trimethoprim-sulfonamides",
                "effect": "Additive folate-pathway inhibition and additive risk of blood dyscrasias/KCS-type sulfonamide toxicity — avoid combining",
                "effect_ja": "葉酸経路阻害と血液障害・サルファ毒性リスクが相加 — 併用を避ける",
                "severity": "major",
            },
            {
                "drug": "Other oxidant/methemoglobin-forming drugs (e.g., topical benzocaine, high-dose acetaminophen exposure)",
                "effect": "Additive methemoglobinemia risk",
                "effect_ja": "メトヘモグロビン血症リスクが相加",
                "severity": "moderate",
            },
        ],
    },
]
