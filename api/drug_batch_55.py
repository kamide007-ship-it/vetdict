"""Drug batch 55 – referenced-but-absent agents surfaced by the 2026-09 audit (21st sweep).

The dose-context token audit (treatment texts cross-checked against
find_drugs_in_text) found three agents that the site's own curated disease
content prescribes, yet no monograph existed:

  - Bezafibrate — the dog Miniature Schnauzer Hyperlipidemia entry
    prescribes "ベザフィブラート5-10 mg/kg PO q24h（フィブラート系）" with
    gemfibrozil as the alternative, and the Bile Peritonitis entry names it
    for mucocele-driving hyperlipidaemia, yet no fibrate of any kind was in
    the formulary (De Marco et al. JVIM 2017 — effective, well-tolerated TG
    reduction in dogs with primary hyperlipidaemia).
  - Medroxyprogesterone acetate (MPA, Depo) — referenced by the feline
    eosinophilic keratoconjunctivitis entry (depot progestin rescue), dosed
    explicitly by the hamster uterine endometrial hyperplasia entry
    ("酢酸メドロキシプロゲステロン 50 mg/kg SC 単回") and explicitly
    NOT recommended by the avian chronic-egg-laying entry — the
    defining safety profile (diabetes induction, mammary hyperplasia/
    neoplasia, adrenal suppression, pyometra) belongs in the formulary.
  - Oncept canine melanoma vaccine — the dog Melanoma / Oral Melanoma
    entries cite the USDA-licensed xenogeneic human-tyrosinase DNA vaccine
    with a dosing schedule; the correct label administration is 0.4 mL via
    transdermal needle-free device (not 1 mL IM — the disease texts were
    corrected in the same audit).

References:
  - De Marco V et al. Therapy of dogs with primary hyperlipidemia using
    bezafibrate. J Vet Intern Med 2017.
  - Xenoulis PG, Steiner JM. Canine hyperlipidaemia. J Small Anim Pract 2015.
  - Plumb's Veterinary Drug Handbook 10th ed — medroxyprogesterone acetate.
  - Quesenberry & Carpenter, Ferrets, Rabbits and Rodents 4th ed — rodent
    progestin use.
  - Bergman PJ et al. Long-term survival of dogs with advanced malignant
    melanoma after DNA vaccination. Clin Cancer Res 2003; Grosenbaugh DA
    et al. AJVR 2011 (Oncept licensure study); Ottnod JM et al. Vet Comp
    Oncol 2013 (retrospective — benefit not confirmed; honest equipoise).
"""

DRUGS_BATCH_55 = [
    {
        "id": "bezafibrate",
        "search_aliases": [
            "ベザトール",
            "Bezatol",
            "フィブラート",
            "ゲムフィブロジル",
            "gemfibrozil",
        ],
        "name": "Bezafibrate",
        "name_ja": "ベザフィブラート",
        "category": "endocrine",
        "mechanism": "Fibric-acid derivative; pan-PPAR (predominantly PPAR-α) agonist. Upregulates lipoprotein lipase and hepatic fatty-acid oxidation, markedly lowering serum triglycerides (and moderately cholesterol). First-line drug therapy for canine primary/idiopathic hyperlipidaemia (Miniature Schnauzer) when a low-fat diet alone fails, and for hypertriglyceridaemia driving gallbladder mucocele or pancreatitis risk.",
        "mechanism_ja": "フィブラート系脂質降下薬。PPAR-α優位の汎PPARアゴニストとしてリポ蛋白リパーゼと肝の脂肪酸β酸化を亢進し、血清トリグリセリド（TG）を大幅に低下させる（コレステロールも中等度低下）。低脂肪食のみで管理できない犬の原発性/特発性高脂血症（ミニチュアシュナウザー）や、胆嚢粘液嚢腫・膵炎リスクを高める高TG血症の第一選択薬物療法。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q24h with food (practical banding: <12 kg 100 mg/dog, 12-25 kg 200 mg/dog, >25 kg 400 mg/dog q24h — De Marco 2017: normalised TG in >90% within 30 days). Recheck fasting TG/cholesterol and hepatic enzymes at 4-6 weeks, then q3-6 months. Alternative fibrate: gemfibrozil 150-300 mg/dog PO q12h.",
                "dosage_ja": "5-10 mg/kg PO q24h 食事と共に（実用的な体重帯: <12 kg 100 mg/頭、12-25 kg 200 mg/頭、>25 kg 400 mg/頭 q24h — De Marco 2017: 30日以内に90%超でTG正常化）。4-6週後に空腹時TG/コレステロールと肝酵素を再検、以後3-6ヶ月毎。代替フィブラート: ゲムフィブロジル 150-300 mg/頭 PO q12h。",
                "notes": "Always rule out and treat secondary causes first (hypothyroidism, hyperadrenocorticism, diabetes — treating these often normalises lipids without a fibrate). Continue the low-fat diet; the drug is an adjunct, not a substitute.",
                "notes_ja": "先に続発性原因（甲状腺機能低下症・クッシング症候群・糖尿病）を除外・治療すること — これらの治療のみで脂質が正常化することが多い。低脂肪食は継続（本剤は食事療法の補助であり代替ではない）。",
            },
        },
        "side_effects": "Generally well tolerated in dogs; vomiting/soft stool, hepatic enzyme elevation (monitor), rarely myopathy",
        "side_effects_ja": "犬では概ね忍容性良好。嘔吐・軟便、肝酵素上昇（モニタリング必須）、稀にミオパチー",
        "contraindications": "Significant hepatic or renal dysfunction (renally excreted — reduce/avoid in azotaemia). Not established in cats. Avoid combining with other myotoxic lipid agents",
        "contraindications_ja": "重度の肝・腎機能障害（腎排泄のため高窒素血症では減量/回避）。猫では確立されていない。他の筋毒性脂質降下薬との併用回避",
        "drug_interactions": [
            {
                "drug": "Anticoagulants (warfarin)",
                "effect": "Fibrates potentiate oral anticoagulants — monitor coagulation closely",
                "effect_ja": "フィブラートは経口抗凝固薬の作用を増強 — 凝固能を厳重モニタリング",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "medroxyprogesterone",
        "search_aliases": [
            "MPA",
            "デポプロベラ",
            "Depo-Provera",
            "酢酸メドロキシプロゲステロン",
        ],
        "name": "Medroxyprogesterone Acetate (MPA)",
        "name_ja": "メドロキシプロゲステロン酢酸塩（MPA）",
        "category": "reproductive_hormones",
        "mechanism": "Long-acting depot synthetic progestin. Suppresses gonadotropin release and exerts anti-inflammatory/anti-proliferative effects on some tissues. In veterinary practice a LAST-RESORT agent: refractory feline eosinophilic keratoconjunctivitis/dermatoses and medical suppression of rodent uterine endometrial hyperplasia when surgery is not possible. Displaced from routine use by its endocrine toxicity.",
        "mechanism_ja": "長時間作用型デポ合成プロゲスチン。ゴナドトロピン分泌を抑制し、一部組織に抗炎症・抗増殖作用を示す。獣医療では最終手段の位置づけ: 難治性の猫好酸球性角結膜炎/皮膚症や、手術不能な齧歯類の子宮内膜過形成の内科的抑制に限定使用。内分泌毒性のため標準治療からは外れている。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Refractory eosinophilic keratoconjunctivitis/granuloma complex only, after steroid/ciclosporin failure: 5-10 mg/kg (or 10-20 mg/cat) SC as a single depot, repeated no sooner than q4 weeks and for the fewest possible doses (Plumb's 10th ed). Screen glucose before and 2-4 weeks after each dose.",
                "dosage_ja": "ステロイド/シクロスポリン不応の難治性好酸球性角結膜炎・肉芽腫群に限定: 5-10 mg/kg（または10-20 mg/頭）SC 単回デポ。反復は最短でも4週間隔とし、可能な限り最少回数に留める（Plumb's 10th ed）。各投与の前と2-4週後に血糖をスクリーニング。",
                "notes": "Defining risks in cats: diabetes mellitus induction, mammary fibroepithelial hyperplasia and mammary carcinoma, adrenocortical suppression. Intact queens: promotes cystic endometrial hyperplasia/pyometra — spay first whenever possible.",
                "notes_ja": "猫での定義的リスク: 糖尿病誘発・乳腺線維上皮過形成/乳腺癌・副腎皮質抑制。未避妊雌ではCEH/子宮蓄膿症を促進 — 可能な限り先に避妊手術を。",
            },
            "hamster": {
                "safe": True,
                "dosage": "Uterine endometrial hyperplasia, medical management only when ovariohysterectomy is not possible: 50 mg/kg SC once (Quesenberry & Carpenter 4th ed). OVH remains the definitive treatment.",
                "dosage_ja": "子宮内膜過形成で卵巣子宮摘出術（OVH）が不可能な場合の内科管理に限定: 50 mg/kg SC 単回（Quesenberry & Carpenter 4th ed）。根治はOVH。",
                "notes": "Side effects mirror other species: diabetes, adrenal suppression, worsening of pyometra if infection is already present.",
                "notes_ja": "副作用は他種と同様: 糖尿病・副腎抑制・感染併存時の子宮蓄膿症悪化。",
            },
            "bird": {
                "safe": False,
                "dosage": "Not recommended for chronic egg laying — historically used but abandoned: diabetes mellitus, hepatic lipidosis/damage, obesity and thromboembolism. Use GnRH agonists (deslorelin implant, leuprolide) instead.",
                "dosage_ja": "慢性産卵への使用は非推奨 — 歴史的に使用されたが糖尿病・肝リピドーシス/肝障害・肥満・血栓塞栓症のため廃止。GnRHアゴニスト（デスロレリンインプラント、リュープロレリン）を使用すること。",
            },
        },
        "side_effects": "Diabetes mellitus (progestin-induced insulin resistance ± acromegaly-like GH induction in cats), mammary hyperplasia/neoplasia, adrenocortical suppression, polyphagia/weight gain, cystic endometrial hyperplasia-pyometra in intact females",
        "side_effects_ja": "糖尿病（プロゲスチン誘発性インスリン抵抗性。猫では乳腺由来GH誘導によるアクロメガリー様変化も）、乳腺過形成/腫瘍、副腎皮質抑制、多食・体重増加、未避妊雌のCEH-子宮蓄膿症",
        "contraindications": "Diabetes mellitus or prediabetes, mammary masses, pregnancy, pyometra/active uterine infection, hepatic disease. Never a first-line agent — document informed consent for last-resort use",
        "contraindications_ja": "糖尿病・境界型高血糖、乳腺腫瘤、妊娠、子宮蓄膿症/活動性子宮感染、肝疾患。第一選択にしないこと — 最終手段としての使用はインフォームドコンセントを記録",
        "drug_interactions": [
            {
                "drug": "Corticosteroids",
                "effect": "Additive diabetogenic and immunosuppressive effects — avoid concurrent long-term use",
                "effect_ja": "糖尿病誘発作用・免疫抑制作用が相加的 — 長期併用を避ける",
                "severity": "moderate",
            },
            {
                "drug": "Insulin",
                "effect": "Progestin-induced insulin resistance destabilises diabetic control; anticipate dose changes",
                "effect_ja": "プロゲスチン誘発性インスリン抵抗性により血糖コントロールが不安定化 — 用量変更を想定",
                "severity": "major",
            },
        ],
    },
    {
        "id": "oncept_melanoma_vaccine",
        "search_aliases": [
            "Oncept",
            "オンセプト",
            "メラノーマワクチン",
            "melanoma vaccine",
            "チロシナーゼDNAワクチン",
        ],
        "name": "Oncept Canine Melanoma Vaccine",
        "name_ja": "Oncept 犬メラノーマワクチン",
        "category": "biologics",
        "mechanism": "Xenogeneic DNA vaccine encoding human tyrosinase (USDA-licensed 2010, first therapeutic cancer vaccine in veterinary medicine). The xenogeneic protein is different enough to break immune tolerance yet similar enough that the induced humoral/cell-mediated response cross-reacts with canine tyrosinase on melanoma cells. Adjunct immunotherapy AFTER locoregional control (surgery ± radiation) of oral melanoma.",
        "mechanism_ja": "ヒトチロシナーゼ遺伝子を組み込んだ異種DNAワクチン（2010年USDA承認 — 獣医療初の治療用がんワクチン）。異種蛋白であることで免疫寛容を破綻させつつ、誘導された液性/細胞性免疫が犬メラノーマ細胞のチロシナーゼに交差反応する。口腔メラノーマの局所制御（手術±放射線）後の補助免疫療法。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.4 mL via transdermal needle-free device (VET JET) into the medial thigh, q2 weeks × 4 doses, then a single 0.4 mL booster q6 months. Indication: stage II-III oral melanoma after locoregional control. Evidence: Bergman 2003 (phase I), Grosenbaugh 2011 AJVR (licensure — MST 389-589 days vs ~200 days historical surgery-alone controls); note Ottnod 2013 retrospective found no significant survival benefit — counsel owners on evidence equipoise.",
                "dosage_ja": "0.4 mL を経皮ニードルフリーデバイス（VET JET）で大腿内側に投与、2週毎 × 4回 → 以後6ヶ月毎に0.4 mLブースター。適応: 局所制御後のStage II-III口腔メラノーマ。エビデンス: Bergman 2003（第I相）、Grosenbaugh 2011 AJVR（承認試験 — MST 389-589日 vs 手術単独の歴史的対照約200日）。Ottnod 2013の後ろ向き研究では有意な生存延長を認めず — エビデンスの不確実性を飼い主に説明すること。",
                "notes": "Not a substitute for surgery/radiation — locoregional control first. Administered by/under supervision of a licensed veterinarian (US: specialty distribution). Transient injection-site reaction and low-grade depigmentation (vitiligo) reported.",
                "notes_ja": "手術/放射線の代替ではない — まず局所制御を達成すること。米国では専門医流通。注射部位の一過性反応と軽度の色素脱失（白斑）の報告あり。",
            },
            "horse": {
                "safe": True,
                "dosage": "Not licensed for horses (species-specificity); experimental use in grey horse melanoma reported (tyrosinase immune response demonstrated — Lembcke 2012; Phillips 2012) but efficacy unproven. Off-label investigational only.",
                "dosage_ja": "馬では非承認（種特異性）。芦毛馬メラノーマでの試験的使用の報告あり（チロシナーゼ免疫応答は確認 — Lembcke 2012; Phillips 2012）が有効性は未証明。オフラベルの研究的使用に限る。",
            },
        },
        "side_effects": "Transient injection-site swelling/pain, low-grade fever, depigmentation (vitiligo-like) at pigmented sites",
        "side_effects_ja": "注射部位の一過性腫脹・疼痛、微熱、色素部位の色素脱失（白斑様）",
        "contraindications": "Gross uncontrolled local disease (vaccine is an adjunct, not a debulking therapy). No known drug contraindications",
        "contraindications_ja": "未制御の肉眼的局所病変（本ワクチンは補助療法であり減量手術の代替ではない）。既知の薬物禁忌なし",
        "drug_interactions": [],
    },
]
