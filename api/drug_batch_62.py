"""Drug batch 62 – referenced-but-absent agents surfaced by the 2026-09 audit (27th sweep).

A dose-context katakana/English token sweep against the live text matcher found
three true monograph gaps (every other candidate already resolved):

  - Prucalopride — the formulary's own feline megacolon/constipation entries
    prescribe it by name with doses ("プルカロプリド0.5-2 mg/cat PO q24h —
    シサプリド代替、ヒト用" ×3 entries). Cisapride was withdrawn from human
    markets (hERG/QT toxicity) and survives only as a compounded product in
    Japan, so the referenced alternative deserved its own monograph with the
    class-defining facts: highly selective 5-HT4 agonism WITHOUT the hERG
    potassium-channel affinity that killed cisapride, and the prokinetic-class
    contraindication in mechanical obstruction.

  - Niclosamide — referenced with doses in hamster Rodentolepis (Hymenolepis)
    nana ("100 mg/kg PO", praziquantel alternative), avian cestodes
    ("250 mg/kg PO 単回") and amphibian GI trematodes ("150 mg/kg PO 単回").
    Classic anticestodal whose defining property is that it is essentially not
    absorbed from the GI tract — it kills intestinal adult tapeworms only and
    has no activity against larval/tissue stages.

  - Brinzolamide — referenced in the avian glaucoma protocol ("ブリンゾラミド
    1%: 1滴 q8-12h") while only dorzolamide was listed. Standard topical
    carbonic anhydrase inhibitor in dogs/cats; formulated at physiological pH
    so it stings less than dorzolamide 2% (a real compliance factor).

References:
  - Washabau & Day, Canine and Feline Gastroenterology — feline megacolon
    management; 5-HT4 prokinetics.
  - Briejer MR et al., Eur J Pharmacol 2001 — prucalopride canine GI motility
    pharmacology (selective 5-HT4 agonist, no hERG affinity).
  - Plumb's Veterinary Drug Handbook 10th ed — niclosamide (anticestodal,
    minimal absorption), brinzolamide/dorzolamide topical CAIs.
  - Gelatt's Veterinary Ophthalmology 6th ed — topical CAI therapy of canine
    and feline glaucoma.
  - Carpenter's Exotic Animal Formulary 6th ed — avian/exotic anticestodal
    dosing.
"""

DRUGS_BATCH_62 = [
    {
        "id": "prucalopride",
        "search_aliases": [
            "プルカロプリド",
            "prucalopride",
            "レゾロール",
            "resolor",
            "motegrity",
        ],
        "name": "Prucalopride",
        "name_ja": "プルカロプリド（レゾロール）",
        "category": "gastrointestinal",
        "mechanism": "Highly selective serotonin 5-HT4 receptor agonist (benzofuran carboxamide). Stimulates colonic (and whole-gut) propulsive motility. Unlike cisapride it has essentially no hERG potassium-channel affinity, so it lacks the QT-prolongation/arrhythmia liability that withdrew cisapride from human markets.",
        "mechanism_ja": "高選択的セロトニン5-HT4受容体作動薬（ベンゾフラン・カルボキサミド系）。結腸（および全腸管）の推進性運動を促進する。シサプリドと異なりhERGカリウムチャネルへの親和性が実質的に無く、シサプリドがヒト市場から撤退する原因となったQT延長・不整脈リスクを持たない。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Megacolon / refractory constipation (off-label human drug; cisapride alternative now that cisapride is compounding-only): 0.5-2 mg/cat PO q24h, titrated to stool quality. Combine with the core plan — hydration, dietary fiber strategy (or low-residue diet in severe megacolon), lactulose/PEG 3350, and treatment of any underlying cause (Washabau & Day).",
                "dosage_ja": "巨大結腸症・難治性便秘（ヒト用のoff-label使用。シサプリドが院内特殊調剤のみとなった現在の代替）: 0.5-2 mg/頭 PO q24h、便性状で漸増調整。水和・食物繊維戦略（重度巨大結腸では逆に低残渣食）・ラクツロース/PEG 3350・基礎疾患治療という基本プランに併用する（Washabau & Day）。",
                "notes": "Prokinetics are an adjunct, not a substitute: recurrent obstipation despite optimized medical therapy is a subtotal-colectomy discussion. Mostly renally excreted — reduce dose/frequency in significant CKD.",
                "notes_ja": "プロキネティクスは補助であって代替ではない: 内科最適化にもかかわらず反復する宿便は結腸亜全摘の相談対象。主に腎排泄のため、有意なCKDでは減量・投与間隔延長。",
            },
            "dog": {
                "safe": True,
                "dosage": "Limited clinical data — canine use is extrapolated from pharmacologic studies showing dose-dependent gastric emptying and colonic motility stimulation (Briejer 2001): 0.1-0.3 mg/kg PO q24h has been used anecdotally for refractory colonic hypomotility. Cisapride (compounded) and metoclopramide remain the usual choices.",
                "dosage_ja": "臨床データ限定的 — 犬での使用は用量依存性の胃排出・結腸運動促進を示した薬理研究（Briejer 2001）からの外挿: 難治性結腸運動低下に 0.1-0.3 mg/kg PO q24h の経験的使用報告がある。通常はシサプリド（調剤）・メトクロプラミドが先。",
            },
        },
        "contraindications": "Mechanical GI obstruction or perforation — prokinetic-class contraindication: rule out obstruction (radiographs ± contrast) before starting.",
        "contraindications_ja": "機械的消化管閉塞・穿孔 — プロキネティクス共通の禁忌: 開始前に閉塞を除外（X線±造影）。",
        "drug_interactions": [
            {
                "drug": "Anticholinergics (atropine, glycopyrrolate)",
                "effect": "Pharmacologic antagonism — anticholinergics blunt the prokinetic effect",
                "effect_ja": "薬理学的拮抗 — 抗コリン薬はプロキネティック効果を減弱させる",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "niclosamide",
        "search_aliases": [
            "ニクロサミド",
            "niclosamide",
        ],
        "name": "Niclosamide",
        "name_ja": "ニクロサミド",
        "category": "antiparasitics",
        "mechanism": "Anticestodal salicylanilide: uncouples oxidative phosphorylation in cestode mitochondria, killing intestinal adult tapeworms on contact. Essentially not absorbed from the GI tract — activity (and safety) are luminal only, so it has NO effect on larval/tissue cestode stages.",
        "mechanism_ja": "サリチルアニリド系条虫駆虫薬: 条虫ミトコンドリアの酸化的リン酸化を脱共役し、腸管内の成虫を接触的に殺滅する。消化管からの吸収が実質的に無い — 作用（と安全性）は管腔内に限局し、幼虫・組織内ステージには無効。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Intestinal cestodes (classic regimen, now largely superseded by praziquantel): 157 mg/kg PO after an overnight fast; repeat fecal exam in 2-3 weeks. Not effective against Echinococcus tissue stages (Plumb's).",
                "dosage_ja": "腸管条虫（古典的レジメン — 現在はプラジカンテルがほぼ第一選択）: 一晩絶食後に 157 mg/kg PO。2-3週後に糞便再検査。エキノコックスの組織内ステージには無効（Plumb's）。",
            },
            "cat": {
                "safe": True,
                "dosage": "Intestinal cestodes: 157 mg/kg PO after fasting (classic regimen; praziquantel preferred). Repeat fecal exam in 2-3 weeks.",
                "dosage_ja": "腸管条虫: 絶食後 157 mg/kg PO（古典的レジメン。プラジカンテル優先）。2-3週後に糞便再検査。",
            },
            "hamster": {
                "safe": True,
                "dosage": "Rodentolepis (Hymenolepis) nana as praziquantel alternative: 100 mg/kg PO once, repeat in 7 days (less reliably effective than praziquantel). Environmental decontamination is critical because of R. nana's direct/autoinfective life cycle; zoonotic — advise hand hygiene (Harkness & Wagner; CDC).",
                "dosage_ja": "小形条虫（Rodentolepis/Hymenolepis nana）のプラジカンテル代替: 100 mg/kg PO 単回、7日後反復（効果の信頼性はプラジカンテルに劣る）。R. nana は直接・自家感染サイクルを持つため環境消毒が極めて重要。人獣共通感染症 — 手洗い指導（Harkness & Wagner; CDC）。",
            },
            "bird": {
                "safe": True,
                "dosage": "Intestinal cestodes: 250 mg/kg PO once; recheck feces in 2-3 weeks (Carpenter 6th ed). Control intermediate hosts (insects) to prevent reinfection in outdoor birds.",
                "dosage_ja": "腸管条虫: 250 mg/kg PO 単回。2-3週後に糞便再検査（Carpenter 6th ed）。屋外飼育鳥では中間宿主（昆虫）対策が再感染防止に重要。",
            },
            "amphibian": {
                "safe": True,
                "dosage": "GI trematode/cestode alternative: 150 mg/kg PO once (praziquantel is first-line for amphibian flukes — Wright & Whitaker).",
                "dosage_ja": "消化管吸虫・条虫の代替: 150 mg/kg PO 単回（両生類の吸虫はプラジカンテルが第一選択 — Wright & Whitaker）。",
            },
        },
        "contraindications": "Larval/tissue cestode disease (e.g., Echinococcus cysts) — luminal drug with no systemic activity; use appropriate systemic therapy instead.",
        "contraindications_ja": "幼虫・組織内条虫症（エキノコックス嚢胞等） — 管腔内限局薬で全身作用が無いため不適。全身療法を選択する。",
        "drug_interactions": [],
    },
    {
        "id": "brinzolamide",
        "search_aliases": [
            "ブリンゾラミド",
            "brinzolamide",
            "エイゾプト",
            "azopt",
        ],
        "name": "Brinzolamide 1% Ophthalmic",
        "name_ja": "ブリンゾラミド1%点眼（エイゾプト）",
        "category": "ophthalmic",
        "mechanism": "Topical carbonic anhydrase inhibitor (CA-II) suspension: reduces aqueous humor production by the ciliary body epithelium, lowering intraocular pressure. Formulated at physiological pH, so it stings less on instillation than dorzolamide 2% — a real compliance advantage in fractious patients.",
        "mechanism_ja": "点眼用炭酸脱水酵素（CA-II）阻害薬懸濁液: 毛様体上皮での房水産生を抑制し眼圧を下降させる。生理的pHで製剤化されているため、点眼時の刺激（しみる感覚）がドルゾラミド2%より少ない — 扱いにくい患者で実際的なコンプライアンス上の利点。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Glaucoma: 1 drop in affected eye q8-12h. IOP-lowering efficacy comparable to dorzolamide 2%; choose brinzolamide when dorzolamide causes blepharospasm/stinging (Gelatt's 6th ed). Often combined with a prostaglandin analog (latanoprost) in primary glaucoma.",
                "dosage_ja": "緑内障: 患眼に1滴 q8-12h。眼圧下降効果はドルゾラミド2%と同等で、ドルゾラミドで眼瞼痙攣・刺激が出る症例に選択（Gelatt's 6th ed）。原発緑内障ではプロスタグランジン類似体（ラタノプロスト）としばしば併用。",
            },
            "cat": {
                "safe": True,
                "dosage": "Glaucoma: 1 drop q8-12h. Topical CAIs are a mainstay in cats (prostaglandin analogs are poorly effective in this species), and brinzolamide's lower sting improves acceptance (Gelatt's 6th ed).",
                "dosage_ja": "緑内障: 1滴 q8-12h。猫はプロスタグランジン類似体の効果が乏しいため点眼CAIが主力であり、刺激の少なさが受容性を高める（Gelatt's 6th ed）。",
            },
            "bird": {
                "safe": True,
                "dosage": "Avian glaucoma (referenced protocol): 1 drop q8-12h. Avian ocular anatomy (scleral ossicles, striated ciliary muscle) alters drug response versus mammals — monitor IOP response individually.",
                "dosage_ja": "鳥の緑内障（参照プロトコル）: 1滴 q8-12h。鳥の眼解剖（強膜小骨・横紋筋性毛様体筋）により薬物反応が哺乳類と異なる — 眼圧反応を個体別にモニタリング。",
            },
        },
        "contraindications": "Do not combine with a systemic carbonic anhydrase inhibitor (acetazolamide/methazolamide) — no additive IOP effect, only additive toxicity; use one route or the other.",
        "contraindications_ja": "全身性炭酸脱水酵素阻害薬（アセタゾラミド/メタゾラミド）との併用不可 — 眼圧下降の追加効果は無く毒性のみ相加。経路はどちらか一方。",
        "drug_interactions": [
            {
                "drug": "Acetazolamide / Methazolamide (systemic CAI)",
                "effect": "No additive IOP reduction; additive systemic CA inhibition toxicity — do not combine",
                "effect_ja": "眼圧下降の追加効果なし。全身性CA阻害毒性のみ相加 — 併用不可",
                "severity": "major",
            },
        ],
    },
]
