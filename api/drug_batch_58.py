"""Drug batch 58 – referenced-but-absent agents surfaced by the 2026-09 audit (24th sweep).

A combined katakana + English drug-like-token sweep (dose-context filtered,
cross-checked against find_drugs_in_text on real context snippets) confirmed the
matcher is otherwise saturated and found two true monograph gaps:

  - Tetanus antitoxin (TAT) — the formulary's own disease entries prescribe it
    by name with doses (dog Tetanus: "TAT 100-500 IU/kg IV/IM … 試験量投与後";
    horse Tetanus: "破傷風抗毒素（TAT）1,500-10,000 IU IV/IM（早期投与が重要）")
    yet no antitoxin monograph existed. Horse tetanus is a flagship equine
    emergency (the developer's specialty species). Defining safety facts:
    equine-origin serum anaphylaxis in non-equine species (test dose first),
    and Theiler's disease (serum-associated hepatitis) 4-10 weeks after TAT in
    adult horses — the classic iatrogenic risk of the product itself.

  - Flucytosine (5-FC) — cryptococcosis combination-therapy entries in cats and
    birds cite it with doses ("Flucytosine 30-50 mg/kg PO q6-8h", cat CNS
    cryptococcosis "125-250 mg/kg/day divided"), but no monograph existed.
    Class-defining species gate: dogs develop severe cutaneous drug eruptions /
    toxic epidermal necrolysis-like reactions — contraindicated (Malik 1996;
    Sykes, Canine and Feline Infectious Diseases). Monotherapy resistance
    emerges rapidly — always combine with amphotericin B (± azole).

References:
  - Plumb's Veterinary Drug Handbook 10th ed — tetanus antitoxin, flucytosine.
  - Greene's Infectious Diseases of the Dog and Cat 4th ed — tetanus
    (canine/feline TAT dosing), cryptococcosis (flucytosine combinations).
  - Reed & Bayly's Equine Internal Medicine 4th ed — equine tetanus therapy;
    Theiler's disease (serum hepatitis) after equine-origin antitoxin.
  - Sykes JE. Canine and Feline Infectious Diseases — flucytosine canine
    cutaneous eruption contraindication; feline cryptococcosis therapy.
  - Malik R et al. Cryptococcosis in cats: clinical and mycological assessment
    and response to treatment. J Med Vet Mycol 1992/1996 series.
  - Carpenter's Exotic Animal Formulary 6th ed — avian flucytosine adjunct.
"""

DRUGS_BATCH_58 = [
    {
        "id": "tetanus_antitoxin",
        "search_aliases": [
            "破傷風抗毒素",
            "破傷風ウマ抗毒素",
            "tetanus antitoxin",
            "テタヌス抗毒素",
        ],
        "name": "Tetanus Antitoxin (TAT)",
        "name_ja": "破傷風抗毒素（TAT）",
        "category": "biologics",
        "mechanism": "Equine-origin hyperimmune antibody preparation that neutralises circulating (unbound) tetanospasmin from Clostridium tetani. It cannot displace toxin already bound to neuronal ganglioside receptors — hence early administration is critical and clinical signs progress for days despite antitoxin. Passive immunisation only: it provides no lasting immunity, so tetanus toxoid (active immunisation) is given concurrently at a separate site.",
        "mechanism_ja": "Clostridium tetani の破傷風毒素（テタノスパスミン）のうち血中の未結合毒素を中和するウマ由来高度免疫抗体製剤。神経のガングリオシド受容体に既に結合した毒素は中和できないため、早期投与が決定的に重要で、投与後も数日は症状が進行しうる。受動免疫のみで持続免疫は付与されない — 破傷風トキソイド（能動免疫）を別部位で同時接種する。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Treatment of clinical tetanus: 10,000-50,000 IU IV/IM (early administration critical; a portion may be infiltrated around the debrided wound). Wound prophylaxis in unvaccinated/unknown-status horses: 1,500-3,000 IU SC/IM, with tetanus toxoid at a separate site (Reed & Bayly 4th ed; Plumb's 10th ed). Combine with wound debridement, penicillin G 22,000 IU/kg IV q6h, muscle relaxants and quiet dark stabling.",
                "dosage_ja": "臨床的破傷風の治療: 10,000-50,000単位 IV/IM（早期投与が重要。一部をデブリードマン後の創部周囲に浸潤投与してもよい）。未接種/接種歴不明馬の創傷時予防: 1,500-3,000単位 SC/IM＋破傷風トキソイドを別部位に接種（Reed & Bayly 4th ed; Plumb's 10th ed）。創部デブリードマン・ペニシリンG 22,000 IU/kg IV q6h・筋弛緩薬・暗く静かな馬房管理を併用。",
                "notes": "Theiler's disease (serum-associated hepatitis, equine parvovirus-H): fulminant hepatic necrosis 4-10 weeks after equine-origin antitoxin in adult horses — the defining iatrogenic risk. Weigh in low-risk vaccinated horses; monitor liver enzymes if signs (icterus, encephalopathy) appear weeks later. Postpartum mares historically over-represented.",
                "notes_ja": "タイラー病（血清肝炎、equine parvovirus-H 関連）: 成馬でウマ由来抗毒素投与の4-10週間後に劇症肝壊死を起こしうる本剤固有の医原性リスク。ワクチン接種済みの低リスク馬では投与の要否を慎重に判断し、数週間後の黄疸・肝性脳症に注意。分娩後の繁殖雌馬での報告が歴史的に多い。",
            },
            "dog": {
                "safe": True,
                "dosage": "Clinical tetanus: 100-500 IU/kg IV/IM (some sources up to 1,000 IU/kg; total commonly capped around 20,000 IU — higher doses add little once binding sites are saturated). Give an intradermal/SC test dose (0.1-0.2 mL) 15-30 min before the full dose — equine-origin serum can cause anaphylaxis (Greene 4th ed). Combine with wound debridement and metronidazole 10-15 mg/kg IV q8h.",
                "dosage_ja": "臨床的破傷風: 100-500 IU/kg IV/IM（最大1,000 IU/kgとする資料もあり、総量は約20,000単位を上限とするのが一般的 — 結合部位飽和後の増量は無益）。ウマ由来血清のためアナフィラキシーに注意し、本投与の15-30分前に皮内/皮下試験量（0.1-0.2 mL）を先行させる（Greene 4th ed）。創部デブリードマン＋メトロニダゾール 10-15 mg/kg IV q8h を併用。",
                "notes": "Dogs are considerably more resistant to tetanospasmin than horses; localized tetanus (single-limb rigidity) may generalise — treat early. Recovery takes 2-4+ weeks (new axonal terminal sprouting required).",
                "notes_ja": "犬は馬よりテタノスパスミン感受性が大幅に低い。局所性破傷風（単肢の硬直）から全身化しうるため早期治療。回復には軸索終末の再形成が必要で2-4週間以上を要する。",
            },
            "cat": {
                "safe": True,
                "dosage": "Rarely required — cats are among the most tetanus-resistant species and usually present with localized tetanus. If generalised: 100-500 IU/kg IV/IM after an intradermal test dose, with wound debridement and metronidazole (Greene 4th ed).",
                "dosage_ja": "必要となることは稀 — 猫は最も破傷風抵抗性が高い種の一つで、多くは局所性破傷風にとどまる。全身型では皮内試験量の後に 100-500 IU/kg IV/IM。創部デブリードマンとメトロニダゾールを併用（Greene 4th ed）。",
                "notes": "Localized limb rigidity near a wound is the classic feline presentation and often resolves with wound care + antimicrobials alone.",
                "notes_ja": "創傷近傍の単肢硬直が猫の典型像で、創処置と抗菌薬のみで回復することも多い。",
            },
        },
        "side_effects": "Anaphylaxis/anaphylactoid reactions (equine-origin foreign protein — test dose in non-equine species), serum sickness (days-weeks later), and in adult horses Theiler's disease (serum-associated fulminant hepatitis) 4-10 weeks post-administration",
        "side_effects_ja": "アナフィラキシー/アナフィラキシー様反応（ウマ由来異種蛋白 — 非ウマ種では試験量を先行）、血清病（数日〜数週間後）、成馬ではタイラー病（血清肝炎 — 投与4-10週間後の劇症肝壊死）",
        "contraindications": "Known hypersensitivity to equine serum products. Not a substitute for toxoid vaccination — always give tetanus toxoid concurrently at a separate site. Repeat exposure to equine-origin serum increases anaphylaxis risk.",
        "contraindications_ja": "ウマ血清製剤への過敏症の既往。トキソイドワクチンの代替にはならない — 破傷風トキソイドを必ず別部位で同時接種。ウマ由来血清への再曝露はアナフィラキシーリスクを高める。",
        "drug_interactions": [
            {
                "drug": "Tetanus toxoid (vaccine)",
                "effect": "Give concurrently but at a SEPARATE site with a separate syringe — mixing inactivates the toxoid",
                "effect_ja": "同時接種は可だが必ず別部位・別シリンジで — 混合するとトキソイドが不活化される",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "flucytosine",
        "search_aliases": [
            "フルシトシン",
            "flucytosine",
            "5-FC",
            "5-フルオロシトシン",
        ],
        "name": "Flucytosine (5-FC)",
        "name_ja": "フルシトシン（5-FC）",
        "category": "antifungals",
        "mechanism": "Fluorinated pyrimidine taken up by fungal cytosine permease and deaminated intracellularly to 5-fluorouracil, disrupting fungal RNA and DNA synthesis. Mammalian cells largely lack cytosine deaminase (selective toxicity). Excellent CNS/ocular/urine penetration (small, water-soluble) — the basis for its role in cryptococcal meningitis combinations. Resistance emerges rapidly with monotherapy: always combine with amphotericin B (± azole).",
        "mechanism_ja": "フッ化ピリミジン。真菌のシトシンパーミアーゼで取り込まれ、菌体内で5-フルオロウラシルに脱アミノ化されて真菌のRNA/DNA合成を阻害する。哺乳類細胞はシトシンデアミナーゼをほぼ欠くため選択毒性が成立。低分子・水溶性でCNS・眼・尿への移行が極めて良好 — クリプトコッカス髄膜炎の併用療法における存在意義。単剤では急速に耐性化するため、必ずアムホテリシンB（±アゾール）と併用する。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Cryptococcosis with CNS/ocular involvement (combination therapy): 25-50 mg/kg PO q6-8h (≈75-120 mg/kg/day divided) WITH amphotericin B ± an azole (fluconazole/itraconazole) — never as monotherapy (Greene 4th ed; Sykes). Continue until antigen titres decline; monitor CBC (myelosuppression) and renal values — reduce dose in azotemia (renally excreted; toxicity rises with amphotericin-induced azotemia).",
                "dosage_ja": "CNS/眼病変を伴うクリプトコッカス症（併用療法）: 25-50 mg/kg PO q6-8h（1日総量約75-120 mg/kg分割）をアムホテリシンB±アゾール（フルコナゾール/イトラコナゾール）と併用 — 単剤使用は不可（Greene 4th ed; Sykes）。抗原価の低下まで継続。CBC（骨髄抑制）と腎数値を監視し、高窒素血症では減量（腎排泄のため、アムホテリシンによる腎障害で毒性が増強する）。",
                "notes": "Adds CNS penetration that azoles alone may lack in fulminant meningitis; myelosuppression and GI upset are the dose-limiting toxicities in cats.",
                "notes_ja": "劇症髄膜炎でアゾール単独では不足しうるCNS移行性を補う。猫では骨髄抑制と消化器症状が用量制限毒性。",
            },
            "dog": {
                "safe": False,
                "dosage": "Contraindicated in dogs: severe cutaneous drug eruptions — depigmenting, ulcerative dermatitis progressing to toxic epidermal necrolysis-like reactions — develop within weeks in most treated dogs (Malik; Sykes, Canine and Feline Infectious Diseases). Use amphotericin B + azole combinations instead.",
                "dosage_ja": "犬には禁忌: 投与開始数週間以内に大半の犬で重度の皮膚薬物反応（脱色素性・潰瘍性皮膚炎 → 中毒性表皮壊死症様反応へ進行）が発生する（Malik; Sykes）。犬のクリプトコッカス症はアムホテリシンB＋アゾール併用で治療する。",
                "notes": "This cutaneous eruption is species-specific to dogs and is the class-defining reason flucytosine is a feline/avian (not canine) drug in veterinary mycology.",
                "notes_ja": "この皮膚薬物反応は犬に特異的で、獣医真菌学でフルシトシンが「猫・鳥の薬であって犬の薬ではない」とされる決定的理由。",
            },
            "bird": {
                "safe": True,
                "dosage": "Adjunctive therapy for cryptococcosis/severe systemic mycoses: 30-50 mg/kg PO q6-8h with amphotericin B or an azole (limited avian data; Carpenter 6th ed lists 20-30 mg/kg PO q6h historically for aspergillosis prophylaxis in raptors/waterfowl). Monitor droppings volume/appetite; hydration is essential (renal excretion).",
                "dosage_ja": "クリプトコッカス症/重度全身性真菌症の補助療法: 30-50 mg/kg PO q6-8h をアムホテリシンBまたはアゾールと併用（鳥のデータは限定的。Carpenter 6th ed は猛禽/水禽のアスペルギルス症予防として 20-30 mg/kg PO q6h を歴史的に収載）。食欲・排泄の監視と十分な水和（腎排泄）が必須。",
                "notes": "Modern azoles (voriconazole/itraconazole) have largely replaced it for avian aspergillosis; reserve for cryptococcosis combinations.",
                "notes_ja": "鳥のアスペルギルス症では現代のアゾール（ボリコナゾール/イトラコナゾール）がほぼ置き換えており、クリプトコッカス併用療法に温存する。",
            },
        },
        "side_effects": "Myelosuppression (dose-related, via 5-FU conversion — monitor CBC), GI upset (vomiting/diarrhea), hepatic enzyme elevation; in dogs severe cutaneous drug eruption/TEN-like reaction (contraindicated)",
        "side_effects_ja": "骨髄抑制（5-FU変換による用量依存性 — CBC監視）、消化器症状（嘔吐/下痢）、肝酵素上昇。犬では重度の皮膚薬物反応/中毒性表皮壊死症様反応（禁忌）",
        "contraindications": "Dogs (severe cutaneous eruptions/TEN-like reactions). Monotherapy (rapid resistance — always combine with amphotericin B ± azole). Severe renal impairment without dose reduction (renally excreted). Severe pre-existing myelosuppression.",
        "contraindications_ja": "犬（重度皮膚薬物反応/TEN様反応）。単剤使用（急速な耐性化 — 必ずアムホテリシンB±アゾールと併用）。減量なしの重度腎機能障害（腎排泄）。重度の既存骨髄抑制。",
        "drug_interactions": [
            {
                "drug": "Amphotericin B",
                "effect": "Intended synergistic combination, but amphotericin nephrotoxicity reduces flucytosine clearance and raises myelotoxicity — monitor renal values and CBC, reduce dose with azotemia",
                "effect_ja": "意図されたシナジー併用だが、アムホテリシンの腎毒性でフルシトシンのクリアランスが低下し骨髄毒性が増す — 腎数値とCBCを監視し高窒素血症では減量",
                "severity": "moderate",
            },
            {
                "drug": "Cytarabine",
                "effect": "Competitive antagonism of antifungal activity reported — avoid concurrent use",
                "effect_ja": "抗真菌活性の拮抗が報告されている — 併用を避ける",
                "severity": "moderate",
            },
            {
                "drug": "Myelosuppressive chemotherapy",
                "effect": "Additive bone-marrow suppression",
                "effect_ja": "骨髄抑制が相加的に増強",
                "severity": "major",
            },
        ],
    },
]
