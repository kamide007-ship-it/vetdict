"""Drug batch 66 – 2026-09 audit (第53弾): evidence-based new oncology agents.

Two modern, fully approved canine oncology drugs the formulary's own disease
content already points at but never carried as monographs:

  - Rabacfosadine (Tanovea) — the first drug ever FULLY FDA-approved for
    canine lymphoma (conditional approval 2016 → full approval 2021). The
    formulary's canine lymphoma rescue text already names it
    (「レスキュー：…ラバクフォサジン」) with no monograph to land on.
    Label-defining safety facts are documented: the West Highland White
    Terrier contraindication (breed predisposition to fatal pulmonary
    fibrosis), 30-minute infusion requirement, and the characteristic
    dermatopathy/otitis toxicity.

  - Tigilanol tiglate (Stelfonta) — intratumoral protein-kinase-C activator
    for non-metastatic canine mast cell tumors (FDA/EMA approved). Fills the
    non-surgical local-therapy gap next to the formulary's existing MCT
    content (vinblastine, toceranib, lomustine, Oncept). The label's
    mandatory concomitant-medication protocol (corticosteroid + H1 + H2
    blockers to blunt degranulation) and the expected wound-formation course
    are the class-defining facts owners and clinicians must know.

This batch also accompanies the batch-15 correction that replaced the
fabricated "Epofolaner (Zenrelia)" entry with the real ilunocitinib
monograph (Zenrelia is Elanco's JAK inhibitor, not an isoxazoline).

References:
  - TANOVEA (rabacfosadine for injection) US label; FDA full approval 2021
    (first fully approved treatment for canine lymphoma).
  - Thamm DH et al., J Vet Intern Med 2017 — rabacfosadine in relapsed
    canine multicentric lymphoma.
  - Saba CF et al., J Vet Intern Med 2018 — rabacfosadine/doxorubicin
    alternating protocol in naive canine lymphoma.
  - STELFONTA (tigilanol tiglate injection, 1 mg/mL) US label (DailyMed):
    0.5 mL per cm³ tumor volume intratumorally, max 0.25 mL/kg and 5 mL
    total; tumors ≤10 cm³; mandatory concomitant prednisone/prednisolone +
    H1 + H2 blockers.
  - De Ridder TR et al., J Vet Intern Med 2021 — randomized controlled trial
    of single intratumoral tigilanol tiglate: 75% complete response at 28
    days after one treatment.
"""

DRUGS_BATCH_66 = [
    {
        "id": "rabacfosadine",
        "search_aliases": [
            "ラバクフォサジン",
            "タノベア",
            "tanovea",
        ],
        "name": "Rabacfosadine (Tanovea)",
        "name_ja": "ラバクフォサジン（タノベア）",
        "category": "antineoplastics",
        "mechanism": "Double prodrug of the nucleotide analogue PMEG; preferentially loads lymphoid cells, where the active metabolite inhibits DNA polymerases and triggers apoptosis of malignant lymphocytes. The first drug fully FDA-approved for canine lymphoma (conditional 2016 → full approval 2021). Single-agent activity in both naive and relapsed multicentric lymphoma (Thamm 2017; Saba 2018 alternating with doxorubicin).",
        "mechanism_ja": "ヌクレオチドアナログPMEGのダブルプロドラッグ。リンパ系細胞に選択的に取り込まれ、活性代謝物がDNAポリメラーゼを阻害して腫瘍性リンパ球のアポトーシスを誘導する。犬リンパ腫に対して史上初めてFDAが正式承認した薬剤（2016年条件付き→2021年正式承認）。未治療・再発の多中心型リンパ腫の双方で単剤活性が報告（Thamm 2017、ドキソルビシン交替投与は Saba 2018）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1 mg/kg IV infusion over 30 minutes, every 21 days for up to 5 doses (label). Give as a dilute 30-min infusion — never a bolus. Multicentric lymphoma (naive or rescue); often alternated with doxorubicin in naive B-cell protocols (Saba 2018).",
                "dosage_ja": "1 mg/kg を30分かけて点滴静注、21日毎に最大5回（ラベル用量）。必ず希釈して30分点滴 — ボーラス投与不可。多中心型リンパ腫（未治療・レスキューとも）。未治療B細胞ではドキソルビシンとの交替プロトコルも用いられる（Saba 2018）。",
                "notes": "Do NOT use in West Highland White Terriers (breed predisposition to fatal pulmonary fibrosis — see contraindications); use extreme caution in other terriers and avoid in dogs with pre-existing pulmonary disease. Characteristic toxicities: dermatopathy (pinnal/periocular erythema, otitis externa — often responds to dose delay + steroids), GI signs, myelosuppression (CBC before each dose), and delayed pulmonary fibrosis (monitor respiratory rate/effort between cycles).",
                "notes_ja": "ウエスト・ハイランド・ホワイト・テリアには使用しない（致死的肺線維症の品種素因）。他のテリア種も最大限慎重に、既存の肺疾患がある犬には使用しない。特徴的毒性: 皮膚障害（耳介・眼周囲の紅斑、外耳炎 — 休薬＋ステロイドで軽快することが多い）、消化器症状、骨髄抑制（毎回投与前にCBC）、遅発性肺線維症（サイクル間も呼吸数・努力性呼吸を監視）。",
            },
            "cat": {
                "safe": False,
                "dosage": "Do not use — feline safety not established",
                "dosage_ja": "使用しない — 猫での安全性は未確立",
                "notes": "Dog-only label; no feline safety data for PMEG prodrugs",
                "notes_ja": "犬専用ラベル。PMEGプロドラッグの猫での安全性データは無い",
            },
        },
        "side_effects": [
            "Dermatopathy (pinnal/periocular erythema, otitis externa)",
            "Vomiting/diarrhea",
            "Neutropenia (nadir ~7 days)",
            "Pulmonary fibrosis (potentially fatal, delayed)",
            "Lethargy/anorexia",
        ],
        "side_effects_ja": [
            "皮膚障害（耳介・眼周囲紅斑、外耳炎）",
            "嘔吐・下痢",
            "好中球減少（ナディア約7日）",
            "肺線維症（致死的になりうる遅発性毒性）",
            "元気消失・食欲不振",
        ],
        "contraindications": "West Highland White Terriers (fatal pulmonary fibrosis predisposition); pre-existing pulmonary fibrosis or significant pulmonary disease; pregnant/nursing handlers should not handle (cytotoxic)",
        "contraindications_ja": "ウエスト・ハイランド・ホワイト・テリア（致死的肺線維症の素因）；既存の肺線維症・重大な肺疾患；細胞傷害性薬のため妊娠中・授乳中の取扱者は調製・投与に関与しない",
        "drug_interactions": [
            {
                "drug": "Other myelosuppressive chemotherapy",
                "effect": "Additive myelosuppression — stagger nadirs and monitor CBC before each dose",
                "effect_ja": "骨髄抑制の相加 — ナディアをずらし毎回投与前にCBC監視",
                "severity": "major",
            },
            {
                "drug": "Drugs causing pulmonary toxicity (e.g. lomustine at high cumulative doses)",
                "effect": "Theoretical additive pulmonary injury — monitor respiratory signs closely",
                "effect_ja": "肺傷害の理論的相加 — 呼吸器徴候を厳重に監視",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "tigilanol_tiglate",
        "search_aliases": [
            "チギラノールチグラート",
            "チグラノール",
            "ステルフォンタ",
            "stelfonta",
        ],
        "name": "Tigilanol Tiglate (Stelfonta)",
        "name_ja": "チギラノールチグラート（ステルフォンタ）",
        "category": "antineoplastics",
        "mechanism": "Intratumoral protein kinase C (PKC) activator. A single injection triggers rapid localized inflammatory oncolysis and tumor vascular destruction, causing haemorrhagic necrosis and slough of the treated mast cell tumor followed by wound healing. Non-surgical local therapy for NON-metastatic cutaneous MCT (and subcutaneous MCT at or distal to the elbow/hock): 75% complete response 28 days after one injection in the randomized controlled trial (De Ridder 2021 JVIM).",
        "mechanism_ja": "腫瘍内注射用のプロテインキナーゼC（PKC）活性化薬。単回注射で局所の急速な炎症性腫瘍溶解と腫瘍血管の破壊が起こり、肥満細胞腫が出血性壊死→脱落し、その後創傷治癒に向かう。転移のない皮膚型MCT（および肘・飛節以遠の皮下型）に対する非外科的局所療法: 無作為化比較試験で単回注射28日後の完全奏効率75%（De Ridder 2021 JVIM）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Intratumoral, single treatment: 0.5 mL of the 1 mg/mL solution per cm³ of tumor volume (= 0.5 mg/cm³), using a fanning technique. Do not exceed 0.25 mL/kg body weight or 5 mL total per dog. Eligible tumors: non-metastatic cutaneous MCT anywhere, or subcutaneous MCT at/distal to elbow or hock, volume ≤10 cm³. An incompletely responding tumor may be re-treated once after 4 weeks (label).",
                "dosage_ja": "腫瘍内注射・単回: 1 mg/mL溶液を腫瘍体積1 cm³あたり0.5 mL（=0.5 mg/cm³）、ファニング法で腫瘍全体に分散注入。体重1 kgあたり0.25 mL・1頭あたり総量5 mLを超えない。適応腫瘍: 転移のない皮膚型MCT（部位不問）または肘・飛節以遠の皮下型MCTで体積10 cm³以下。奏効不十分例は4週後に1回のみ再投与可（ラベル）。",
                "notes": "MANDATORY concomitant medication to prevent severe degranulation reactions (including death): corticosteroid (prednisone/prednisolone) + H1 blocker (diphenhydramine) + H2 blocker (famotidine), started before injection and continued per label. Counsel owners BEFORE treatment: the tumor is EXPECTED to necrose and slough, leaving an open wound that heals by second intention (usually 4-6 weeks) — this is the mechanism, not a complication. Stage the tumor first (cytology + node assessment): metastatic disease is not an indication.",
                "notes_ja": "重度の脱顆粒反応（死亡例を含む）を防ぐための併用薬がラベル上必須: コルチコステロイド（プレドニゾン/プレドニゾロン）＋H1ブロッカー（ジフェンヒドラミン）＋H2ブロッカー（ファモチジン）を注射前から開始しラベルどおり継続。治療前に飼い主へ必ず説明: 腫瘍は壊死・脱落して開放創となり二次治癒する（通常4-6週）— これは作用機序そのものであり合併症ではない。事前に細胞診＋所属リンパ節評価でステージング: 転移例は適応外。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not approved for cats",
                "dosage_ja": "猫には承認されていない",
                "notes": "No feline label; feline MCT is managed surgically",
                "notes_ja": "猫用ラベルなし。猫のMCTは外科が基本",
            },
        },
        "side_effects": [
            "Injection-site wound formation with necrosis/slough (expected mechanism)",
            "Pain and lameness (limb sites)",
            "Mast cell degranulation signs (vomiting, hypotension, tachycardia) — blunted by mandatory concomitants",
            "Wound infection (secondary)",
        ],
        "side_effects_ja": [
            "注射部位の壊死・脱落を伴う創形成（作用機序として想定内）",
            "疼痛・跛行（四肢の病変）",
            "肥満細胞脱顆粒徴候（嘔吐・低血圧・頻脈）— 必須併用薬で軽減",
            "創部の二次感染",
        ],
        "contraindications": "Metastatic MCT; tumors >10 cm³ or exceeding dose caps; do not use without the mandatory corticosteroid + H1 + H2 concomitant protocol; avoid accidental self-injection (severe local inflammation in humans)",
        "contraindications_ja": "転移のあるMCT；体積10 cm³超・用量上限超の腫瘍；必須の併用プロトコル（ステロイド＋H1＋H2）なしでの使用；誤自己注射に注意（ヒトでも重度の局所炎症）",
        "drug_interactions": [
            {
                "drug": "Corticosteroids / H1 / H2 blockers",
                "effect": "REQUIRED concomitants per label — this is a mandatory combination, not an interaction to avoid",
                "effect_ja": "ラベル上の必須併用 — 避けるべき相互作用ではなく義務付けられた併用",
                "severity": "moderate",
            },
            {
                "drug": "NSAIDs",
                "effect": "Avoid alongside the mandatory corticosteroid course (GI ulceration risk)",
                "effect_ja": "必須ステロイド併用期間中はNSAIDsを避ける（消化管潰瘍リスク）",
                "severity": "major",
            },
        ],
    },
]
