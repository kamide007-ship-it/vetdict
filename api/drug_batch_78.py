"""Drug batch 78 – 2026-10 第70弾 (parallel session; renumbered from 77 on merge).

1. Paroxetine — referenced with a dose in the cat feline psychogenic
   alopecia / urine-marking entries (「代替: パロキセチン0.5-1mg/kg PO q24h」) and the
   sugar-glider self-mutilation entry, but absent from the dictionary
   (referenced-but-absent; sertraline/fluoxetine were present).
2. Felpreva (tigolaner + emodepside + praziquantel) — EU-authorised 2021
   (EMA) feline spot-on giving up to 13 weeks of flea/tick control plus
   endoparasite treatment.

Evidence:
  - Plumb's Veterinary Drug Handbook 10th ed (paroxetine monograph).
  - Landsberg, Hunthausen & Ackerman, Behavior Problems of the Dog and Cat
    3rd ed (2013) — SSRI dosing, anticholinergic profile of paroxetine.
  - Felpreva EPAR / SPC (EMA, Vetoquinol, 2021).
"""

DRUGS_BATCH_78 = [
    {
        "id": "paroxetine",
        "search_aliases": ["パロキセチン", "パキシル", "Paxil", "paroxetine"],
        "name": "Paroxetine",
        "name_ja": "パロキセチン",
        "category": "behavioral",
        "mechanism": "Selective serotonin reuptake inhibitor (SSRI). Of the SSRIs it has the strongest anticholinergic (muscarinic) activity and a short half-life without active metabolites, so it is shorter-acting than fluoxetine but more prone to constipation/urinary retention and to discontinuation signs if stopped abruptly.",
        "mechanism_ja": "選択的セロトニン再取り込み阻害薬（SSRI）。SSRIの中で抗コリン（ムスカリン受容体）作用が最も強く、活性代謝物を持たず半減期が短い — フルオキセチンより作用は短いが、便秘・尿閉と急な中止での離脱症状が出やすい。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO q24h (practically 1/8-1/4 of a 10 mg tablet per cat), as an alternative SSRI for urine marking, feline psychogenic alopecia/overgrooming and anxiety when fluoxetine is not tolerated. Allow 4-6 weeks for effect; combine with environmental/behavioural management (MEMO). Taper over 2-4 weeks when stopping.",
                "dosage_ja": "0.5-1 mg/kg PO q24h（実際には10 mg錠の1/8-1/4錠/頭）— 尿マーキング・心因性脱毛（過剰グルーミング）・不安症でフルオキセチンが合わない場合の代替SSRI。効果判定に4-6週。環境・行動修正（MEMO）と併用。中止時は2-4週かけて漸減。",
                "notes": "Most anticholinergic SSRI — monitor for constipation (avoid in cats with megacolon/chronic constipation) and urinary retention. Sedation or irritability early in treatment. Rule out medical causes (FIC/UTI, dermatologic pruritus) before attributing signs to behaviour.",
                "notes_ja": "SSRIで最も抗コリン作用が強い — 便秘（巨大結腸症・慢性便秘の猫では避ける）・尿閉に注意。投与初期の鎮静またはいらいら。行動学的と判断する前に医学的原因（FIC・尿路感染・皮膚疾患の掻痒）を除外する。",
            },
            "dog": {
                "safe": True,
                "dosage": "1 mg/kg PO q24h (range 1-1.5 mg/kg) for anxiety-related disorders (generalized anxiety, compulsive disorder) as an alternative to fluoxetine. Onset 4-6 weeks; taper over 2-4 weeks when discontinuing.",
                "dosage_ja": "1 mg/kg PO q24h（範囲 1-1.5 mg/kg）— 全般性不安・常同障害でフルオキセチンの代替。効果発現4-6週、中止時は2-4週かけて漸減。",
                "notes": "Lower the seizure threshold modestly — caution in epileptic dogs. Monitor diabetic dogs (glycemic changes).",
                "notes_ja": "けいれん閾値をわずかに下げる — てんかん犬では慎重に。糖尿病犬は血糖変動に注意。",
            },
            "sugar_glider": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO q24h (extrapolated; limited data) as an alternative SSRI in self-mutilation once pain, parasites and husbandry/social causes are addressed.",
                "dosage_ja": "0.5-1 mg/kg PO q24h（外挿・データ限定的）— 疼痛・寄生虫・飼育環境・社会的要因に対処した上での自咬症の代替SSRI。",
                "notes": "Correct husbandry (companion, enrichment, diet) is the primary treatment; drug therapy is adjunctive.",
                "notes_ja": "飼育環境（同居個体・環境エンリッチメント・食餌）の是正が主治療で、薬物療法は補助。",
            },
        },
        "contraindications": "Concurrent or recent (within 2 weeks) MAO inhibitors — selegiline, amitraz (incl. amitraz collars/dips) — serotonin syndrome. Megacolon/severe constipation, urinary retention, narrow-angle glaucoma (anticholinergic effects). Known hypersensitivity.",
        "contraindications_ja": "MAO阻害薬（セレギリン、アミトラズ — アミトラズ首輪・薬浴を含む）の併用または中止後2週間以内（セロトニン症候群）。巨大結腸症・重度便秘・尿閉・閉塞隅角緑内障（抗コリン作用）。過敏症。",
        "side_effects": [
            "Sedation or anxiety/irritability early in treatment",
            "Decreased appetite, vomiting",
            "Constipation, urinary retention (anticholinergic)",
            "Discontinuation signs if stopped abruptly",
        ],
        "side_effects_ja": [
            "投与初期の鎮静または不安・いらいら",
            "食欲低下・嘔吐",
            "便秘・尿閉（抗コリン作用）",
            "急な中止による離脱症状",
        ],
        "drug_interactions": [
            {
                "drug": "Selegiline",
                "effect": "Serotonin syndrome — contraindicated; allow a 2-week washout.",
                "effect_ja": "セロトニン症候群 — 併用禁忌。2週間の休薬期間を置く。",
                "severity": "major",
            },
            {
                "drug": "Amitraz",
                "effect": "MAO-inhibiting acaricide — serotonin syndrome risk; avoid amitraz collars/dips during SSRI therapy.",
                "effect_ja": "MAO阻害作用を持つ殺ダニ剤 — セロトニン症候群のリスク。SSRI投与中はアミトラズ首輪・薬浴を避ける。",
                "severity": "major",
            },
            {
                "drug": "Tramadol / Trazodone",
                "effect": "Additive serotonergic effect — monitor for serotonin syndrome (agitation, tremor, hyperthermia).",
                "effect_ja": "セロトニン作用の相加 — セロトニン症候群（興奮・振戦・高体温）を監視。",
                "severity": "moderate",
            },
            {
                "drug": "Fluoxetine / Clomipramine",
                "effect": "Duplicate serotonergic therapy — do not combine; fluoxetine needs a 5-week washout before switching.",
                "effect_ja": "セロトニン作動薬の重複 — 併用しない。フルオキセチンからの切替は5週間の休薬が必要。",
                "severity": "major",
            },
        ],
        "references": [
            "Plumb's Veterinary Drug Handbook, 10th ed — Paroxetine",
            "Landsberg G, Hunthausen W, Ackerman L. Behavior Problems of the Dog and Cat, 3rd ed. 2013",
            "Overall KL. Manual of Clinical Behavioral Medicine for Dogs and Cats. 2013",
        ],
    },
    {
        "id": "felpreva",
        "search_aliases": [
            "フェルプレバ",
            "Felpreva",
            "チゴラネル",
            "tigolaner",
            "チゴラネル・エモデプシド・プラジカンテル",
        ],
        "name": "Felpreva (tigolaner/emodepside/praziquantel)",
        "name_ja": "フェルプレバ（チゴラネル・エモデプシド・プラジカンテル配合）",
        "category": "antiparasitics",
        "mechanism": "Feline spot-on. Tigolaner (bispyrazole) blocks insect/acarine GABA-gated chloride channels with a long half-life — fleas, ticks and mites for up to 13 weeks; emodepside (cyclic depsipeptide, SLO-1 potassium channel agonist) — roundworms, hookworms and lungworms; praziquantel — tapeworms.",
        "mechanism_ja": "猫用スポットオン。チゴラネル（ビスピラゾール系）が長い半減期で昆虫・ダニのGABA作動性Cl-チャネルを遮断し最長13週間ノミ・マダニ・ダニを駆除、エモデプシド（環状デプシペプチド・SLO-1カリウムチャネル作動薬）が回虫・鉤虫・肺虫を、プラジカンテルが条虫を駆除。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Single topical spot-on at minimum 14.4 mg/kg tigolaner + 3 mg/kg emodepside + 12 mg/kg praziquantel (weight-band pipette, applied to the skin at the base of the skull). Up to 13 weeks of flea and tick control; for mixed infestations re-treat at no less than 13-week intervals (EU SPC). Cats >= 10 weeks of age and >= 1.0 kg.",
                "dosage_ja": "スポットオン単回、最低用量: チゴラネル 14.4 mg/kg + エモデプシド 3 mg/kg + プラジカンテル 12 mg/kg（体重帯別ピペットを頭蓋底部の皮膚に塗布）。1回で最長13週間のノミ・マダニ駆除効果。混合寄生には13週以上の間隔で再投与（EU SPC）。10週齢以上かつ体重1.0 kg以上の猫。",
                "notes": "EU indications: fleas, ticks, Notoedres and Otodectes mites, roundworms (Toxocara cati), hookworms, tapeworms (Dipylidium, Taenia/Hydatigera, Echinococcus multilocularis) and lungworms (Aelurostrongylus, Troglostrongylus). Do not let the cat lick the site; avoid contact with treated cats for children until dry. Not approved in Japan as of this entry.",
                "notes_ja": "EUでの適応: ノミ、マダニ、ネコショウセンコウヒゼンダニ（Notoedres）・ミミヒゼンダニ（Otodectes）、回虫（Toxocara cati）、鉤虫、条虫（瓜実条虫・テニア・多包条虫）、肺虫（猫肺虫・Troglostrongylus）。塗布部位を舐めさせない。乾くまで子どもとの接触を避ける。本収載時点で国内未承認。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not for use in dogs — feline-only product (emodepside is a P-glycoprotein substrate; ABCB1-mutant dogs are at risk of neurotoxicity).",
                "dosage_ja": "犬には使用しない — 猫専用製剤（エモデプシドはP糖タンパク質の基質で、ABCB1変異犬では神経毒性のリスク）。",
                "notes": "Canine products with emodepside are separately licensed.",
                "notes_ja": "エモデプシド配合の犬用製剤は別途承認製剤を使用。",
            },
        },
        "contraindications": "Kittens < 10 weeks or < 1.0 kg. Safety not established in pregnant/lactating breeding cats. Do not use in dogs.",
        "contraindications_ja": "10週齢未満・体重1.0 kg未満の子猫。妊娠・授乳中の繁殖猫では安全性未確立。犬には使用しない。",
        "side_effects": [
            "Transient salivation/vomiting if the site is licked",
            "Local alopecia or pruritus at the application site",
            "Rare neurologic signs (ataxia, tremor) with oral exposure or overdose",
        ],
        "side_effects_ja": [
            "塗布部位を舐めた場合の一過性流涎・嘔吐",
            "塗布部位の局所的脱毛・掻痒",
            "経口曝露・過量時のまれな神経症状（運動失調・振戦）",
        ],
        "drug_interactions": [
            {
                "drug": "P-glycoprotein inhibitors (ketoconazole, cyclosporine, macrocyclic lactones at high dose)",
                "effect": "May increase emodepside exposure — monitor for neurologic signs.",
                "effect_ja": "エモデプシドの曝露増加の可能性 — 神経症状を監視。",
                "severity": "moderate",
            },
            {
                "drug": "Other isoxazoline/bispyrazole ectoparasiticides",
                "effect": "Duplicate flea/tick therapy — no added benefit.",
                "effect_ja": "ノミ・マダニ駆除薬の重複 — 追加効果なし。",
                "severity": "minor",
            },
        ],
        "references": [
            "Felpreva EPAR / Summary of Product Characteristics, European Medicines Agency (Vetoquinol), 2021",
            "ESCCAP Guideline GL3: Control of Ectoparasites in Dogs and Cats, 2022",
        ],
    },
]
