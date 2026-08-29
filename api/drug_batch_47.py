"""Drug batch 47 – referenced-but-absent agents surfaced by the 2026-08 audit (16th sweep).

The dosage-context katakana/English token sweep (treatment texts cross-checked
against find_drugs_in_text) found two agents that VetDict's own disease content
instructs clinicians to use, yet were absent from the formulary:

  - フルオロウラシル (fluorouracil, 5-FU): 11 references — the equine sarcoid,
    aural plaque and squamous cell carcinoma protocols (the developer's own
    specialty species) cite "5-FU局所" / "局所5-FU軟膏" and intralesional 5-FU
    as standard adjunctive therapy, and the canine gastrinoma entry references
    systemic 5-FU. Beyond the reference gap, the formulary lacked the single
    most important safety fact about this molecule in small-animal practice:
    5-FU is LETHAL to cats at any dose, and accidental exposure of dogs to
    human topical fluorouracil cream (Efudex) is a well documented fatal
    toxicosis.
The same sweep found 硫酸鉄 (ferrous sulfate, 26 references) unresolvable —
that one turned out to be an alias gap on the existing ferrous_sulfate_oral
entry (canonical name_ja 硫酸第一鉄), fixed in drug_batch_21.py by adding
search_aliases plus horse/ferret dosing rows.

References:
  - Stewart AA et al. JAVMA 2006;228:589 — intratumoral 5-FU for equine
    sarcoids: resolution in 61.5% of treated tumours.
  - Fortier LA, Mac Harg MA. JAVMA 1994;205:1183 — topical 5-FU for
    periocular sarcoids in horses.
  - Theon AP. Vet Clin North Am Equine Pract 1998 — adjunctive chemotherapy
    (5-FU, cisplatin) for equine cutaneous/ocular SCC.
  - Plumb's Veterinary Drug Handbook 10th ed — fluorouracil: absolute feline
    contraindication (fatal neurotoxicity), canine systemic dosing
    150 mg/m2 IV weekly, ferrous sulfate oral dosing dogs/cats/horses.
  - Dorman DC et al. JAVMA 1990 — 5-FU toxicosis in dogs and cats:
    seizures, death; no feline survivors.
  - Withrow & Vail, Small Animal Clinical Oncology 6th ed — 5-FU in
    canine carcinoma protocols; never in cats.
  - Weiss DJ, Wardrop KJ. Schalm's Veterinary Hematology 6th ed — iron
    deficiency anemia therapy: oral ferrous sulfate maintenance after
    parenteral repletion; iron chelation interactions.
"""

DRUGS_BATCH_47 = [
    {
        "id": "fluorouracil",
        "search_aliases": [
            "5-FU",
            "フルオロウラシル",
            "5-フルオロウラシル",
            "エフディックス",
        ],
        "name": "Fluorouracil (5-FU)",
        "name_ja": "フルオロウラシル（5-FU）",
        "category": "antineoplastics",
        "mechanism": "Pyrimidine analogue antimetabolite: converted intracellularly to 5-FdUMP, which irreversibly inhibits thymidylate synthase, blocking DNA synthesis; also misincorporated into RNA. Preferentially kills rapidly dividing neoplastic cells.",
        "mechanism_ja": "ピリミジンアナログ代謝拮抗薬。細胞内で5-FdUMPに変換されてチミジル酸合成酵素を不可逆的に阻害しDNA合成を遮断、RNAにも誤取込みされる。増殖の速い腫瘍細胞を選択的に傷害する。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Topical: 5% cream applied to sarcoid/SCC lesions q24-48h for several weeks-months (small lesions, periocular sarcoids — Fortier 1994). Intratumoral: 50 mg/mL solution injected intralesionally q2weeks (sarcoids — Stewart 2006, 61.5% resolution).",
                "dosage_ja": "外用: 5%クリームをサルコイド/扁平上皮癌病変に q24-48h、数週間〜数ヶ月（小病変・眼周囲サルコイド — Fortier 1994）。腫瘍内投与: 50 mg/mL 溶液を病変内注入 q2週（サルコイド — Stewart 2006、61.5%消退）。",
                "notes": "Standard adjunct for equine sarcoid, aural plaques and cutaneous/ocular SCC alongside surgery, cryotherapy and cisplatin. Wear gloves; prevent the horse licking treated sites. Local inflammation/ulceration at the application site is expected.",
                "notes_ja": "馬サルコイド・耳介プラーク・皮膚/眼扁平上皮癌の標準的補助療法（外科・凍結療法・シスプラチンと併用）。手袋着用、治療部位の舐め防止。塗布部の局所炎症・びらんは想定内の反応。",
            },
            "dog": {
                "safe": True,
                "dosage": "Systemic: 150 mg/m2 (5-10 mg/kg) IV once weekly for carcinomas (GI, hepatic) within combination protocols — oncologist guidance recommended. Do NOT use topically at home: accidental ingestion of human 5% cream (Efudex) causes fatal seizures.",
                "dosage_ja": "全身投与: 150 mg/m2（5-10 mg/kg）IV 週1回、癌腫（消化器・肝）の併用プロトコル内で — 腫瘍科医の指導下を推奨。家庭での外用は不可: ヒト用5%クリーム（エフディックス）の誤摂取は致死的痙攣を起こす。",
                "notes": "Dose-limiting neurotoxicity (cerebellar ataxia, seizures) and myelosuppression. Accidental exposure to an owner's topical fluorouracil is a well documented fatal canine toxicosis (Dorman 1990) — treat ingestion as an emergency (seizure control, decontamination).",
                "notes_ja": "用量規定毒性は神経毒性（小脳性運動失調・痙攣）と骨髄抑制。飼い主の外用フルオロウラシル誤摂取は致死的中毒として有名（Dorman 1990）— 摂取例は救急対応（痙攣管理・除染）。",
            },
            "cat": {
                "safe": False,
                "dosage": "ABSOLUTELY CONTRAINDICATED — fatal at any dose.",
                "dosage_ja": "絶対禁忌 — いかなる用量でも致死的。",
                "notes": "5-FU causes fatal neurotoxicity (status epilepticus) in cats by any route, including grooming contact with an owner's topical cream. No feline survivors reported (Dorman 1990; Plumb's 10th). Never prescribe; warn owners using Efudex to keep it away from cats.",
                "notes_ja": "猫では投与経路を問わず致死的な神経毒性（てんかん重積）を起こす。飼い主の外用クリームへのグルーミング接触でも死亡。生存例の報告なし（Dorman 1990; Plumb's 10th）。処方禁止。エフディックス使用中の飼い主には猫への接触防止を必ず指導。",
            },
        },
        "side_effects": "Neurotoxicity (cerebellar ataxia, seizures — dose-limiting in dogs, fatal in cats), myelosuppression, GI ulceration, local inflammation/ulceration with topical/intralesional use",
        "side_effects_ja": "神経毒性（小脳性運動失調・痙攣 — 犬で用量規定、猫で致死的）、骨髄抑制、消化管潰瘍、外用/腫瘍内投与部の局所炎症・びらん",
        "contraindications": "Cats (fatal — absolute contraindication by any route); pre-existing seizure disorders; severe myelosuppression. Cytotoxic handling precautions apply.",
        "contraindications_ja": "猫（経路を問わず致死的 — 絶対禁忌）、痙攣性疾患の既往、重度骨髄抑制。細胞傷害性薬剤としての取扱い注意が必要。",
        "drug_interactions": [
            {
                "drug": "Cimetidine",
                "effect": "Reduces 5-FU clearance — increased toxicity",
                "effect_ja": "5-FUのクリアランスを低下 — 毒性増強",
                "severity": "moderate",
            },
            {
                "drug": "Metronidazole",
                "effect": "Decreases 5-FU elimination — additive neurotoxicity risk",
                "effect_ja": "5-FUの排泄を低下 — 神経毒性リスクが相加的",
                "severity": "moderate",
            },
        ],
    },
]
