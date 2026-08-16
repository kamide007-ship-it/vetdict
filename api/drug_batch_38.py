"""Drug batch 38 – referenced-but-absent agents surfaced by the 2026-08 audit (6th sweep).

A katakana token-frequency sweep of disease treatment protocols, cross-checked
against the drug keyword index with the real text matcher, found three agents
that VetDict's own content instructs clinicians to use — with explicit doses —
yet were absent from the formulary:

  - パンクレアチン/パンクレリパーゼ (pancreatic enzyme, pancrelipase): the
    lifelong, definitive therapy for exocrine pancreatic insufficiency (EPI).
    VetDict's flagship dog/cat EPI entries prescribe "粉末状膵酵素
    （パンクレアチン/パンクレリパーゼ）を毎食に混合。推奨量：1 tsp/10kg/食"
    yet no enzyme product was carried.
  - ベンズブロマロン (benzbromarone): named with a dose (5 mg/kg PO q24h) in
    the avian and reptile gout protocols as the uricosuric alternative to
    allopurinol; absent from the formulary.
  - メトホルミン (metformin): named with doses in the horse EMS / insulin
    resistance / chronic laminitis entries (15-30 mg/kg PO q8-12h) — the
    developer's own specialty species — yet absent.

References:
  - Westermarck E, Wiberg M. Vet Clin North Am Small Anim Pract 2003;33:
    1165-1179 — canine EPI enzyme replacement.
  - German AJ. J Small Anim Pract 2012 — EPI management; pre-incubation of
    enzyme with food is unnecessary.
  - Steiner JM. Vet Clin North Am 2010 — feline EPI; concurrent cobalamin
    deficiency near-universal.
  - Poffers J, Lumeij JT et al. Avian Pathology 2002;31:567-572 — uricosuric
    effect of benzbromarone in pigeons; experimental avian use.
  - Lumeij JT et al. Avian Pathology 1998 — allopurinol toxicity in
    red-tailed hawks (rationale for uricosuric alternatives).
  - Durham AE et al. Equine Vet J 2008;40:493-500 — metformin 15 mg/kg PO
    q12h improved insulin sensitivity in EMS ponies/horses.
  - Rendle DI et al. Vet Rec 2013 — metformin pharmacokinetics in horses
    (low oral bioavailability); dose timing before feeding.
  - Nelson RW et al. — metformin in diabetic cats: limited efficacy, GI
    adverse effects; insulin/SGLT2 inhibitors preferred.
  - Plumb's Veterinary Drug Handbook, 10th ed — pancrelipase, metformin.
  - Carpenter's Exotic Animal Formulary, 6th ed — avian/reptile gout agents.
"""

DRUGS_BATCH_38: list[dict] = [
    {
        "id": "pancrelipase",
        "search_aliases": [
            "パンクレアチン",
            "パンクレリパーゼ",
            "膵酵素補充",
            "膵酵素製剤",
            "Pancreatin",
            "PERT",
        ],
        "name": "Pancrelipase (Pancreatic Enzyme, PERT)",
        "name_ja": "パンクレリパーゼ（パンクレアチン/膵酵素製剤）",
        "category": "gastrointestinal",
        "mechanism": "Porcine-derived mixture of lipase, protease and amylase that replaces the missing exocrine pancreatic secretion in EPI, restoring luminal digestion of fat, protein and starch. Powdered (non-enteric-coated) formulations are preferred in dogs and cats; activity begins in the duodenum alongside the meal.",
        "mechanism_ja": "ブタ膵由来のリパーゼ・プロテアーゼ・アミラーゼ混合物。膵外分泌不全（EPI）で欠落した膵外分泌を補充し、脂肪・蛋白・デンプンの管腔内消化を回復させる。犬猫では粉末（非腸溶）製剤が推奨され、食餌とともに十二指腸で作用する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Powder: 1 tsp per 10 kg body weight mixed into each meal, adjusted to stool quality/weight gain (lifelong). Raw pancreas 30-100 g per meal is an equivalent alternative. Pre-incubation with food is unnecessary (German 2012).",
                "dosage_ja": "粉末: 体重10 kgあたり小さじ1杯を毎食に混合（生涯継続）。便性状・体重増加をみて調整。代替として生膵臓 30-100 g/食も同等。食餌との事前インキュベーションは不要（German 2012）。",
                "notes": "Definitive therapy for EPI (TLI <2.5 μg/L). Supplement cobalamin (B12) SC — deficiency is common and blunts response. If oral/gingival bleeding occurs (reported at high doses), reduce dose or moisten food. Enteric-coated human capsules are less reliable in dogs.",
                "notes_ja": "EPI（TLI <2.5 μg/L）の根本治療。コバラミン（B12）皮下補充を併用 — 欠乏は高頻度で治療反応を鈍らせる。高用量で口腔・歯肉出血の報告あり — 発現時は減量またはフードを湿らせる。ヒト用腸溶カプセルは犬では効果が不安定。",
            },
            "cat": {
                "safe": True,
                "dosage": "Powder: 1/2-1 tsp mixed into each meal (lifelong), adjusted to effect. Raw pancreas 30-60 g per meal is an alternative.",
                "dosage_ja": "粉末: 小さじ1/2〜1杯を毎食に混合（生涯継続）、効果をみて調整。代替として生膵臓 30-60 g/食。",
                "notes": "Feline EPI (fTLI <8 μg/L) is under-diagnosed. Concurrent cobalamin deficiency is near-universal — supplement B12 250 μg SC weekly (Steiner 2010). Evaluate for concurrent chronic pancreatitis/IBD/cholangitis (triaditis).",
                "notes_ja": "猫EPI（fTLI <8 μg/L）は見逃されやすい。コバラミン欠乏はほぼ必発 — B12 250 μg 皮下 週1回を併用（Steiner 2010）。慢性膵炎・IBD・胆管炎（三臓器炎）の併発を評価する。",
            },
        },
        "side_effects": "Oral/gingival irritation or bleeding in dogs at high powder doses; hyperuricosuria (purine-rich); rare hypersensitivity to porcine protein",
        "side_effects_ja": "犬で高用量粉末による口腔・歯肉刺激/出血。プリン体豊富なため高尿酸尿。ブタ蛋白過敏（稀）",
        "contraindications": "None significant in EPI. Not indicated for uncomplicated pancreatitis without documented exocrine insufficiency.",
        "contraindications_ja": "EPIでの重大な禁忌なし。膵外分泌不全の証明がない単純な膵炎には適応外。",
        "drug_interactions": [],
    },
    {
        "id": "benzbromarone",
        "search_aliases": ["ベンズブロマロン", "ウリノーム", "Urinorm"],
        "name": "Benzbromarone",
        "name_ja": "ベンズブロマロン",
        "category": "urinary",
        "mechanism": "Uricosuric: inhibits renal tubular urate reabsorption (URAT1 transporter), increasing uric acid excretion and lowering plasma uric acid. In birds and reptiles (uricotelic species) it offers an alternative pathway to xanthine-oxidase inhibition by allopurinol.",
        "mechanism_ja": "尿酸排泄促進薬。腎尿細管の尿酸再吸収（URAT1トランスポーター）を阻害して尿酸排泄を増やし血漿尿酸値を低下させる。尿酸排泄型の鳥類・爬虫類では、アロプリノール（キサンチンオキシダーゼ阻害）に代わる作用経路を提供する。",
        "species_info": {
            "bird": {
                "safe": True,
                "dosage": "5 mg/kg PO q24h (experimental). Uricosuric effect demonstrated in pigeons (Poffers & Lumeij 2002).",
                "dosage_ja": "5 mg/kg 経口 24時間毎（試験的）。ハトで尿酸降下作用が実証されている（Poffers & Lumeij 2002）。",
                "notes": "Alternative when allopurinol is poorly tolerated (allopurinol toxicity reported in red-tailed hawks — Lumeij 1998). Ensure vigorous hydration — increased urate excretion without diuresis risks renal urate deposition. Address the diet (excess protein) and dehydration first.",
                "notes_ja": "アロプリノール不耐時の代替（アカオノスリでアロプリノール毒性の報告 — Lumeij 1998）。十分な水和が必須 — 利尿を伴わない尿酸排泄増加は腎への尿酸沈着リスク。まず食事（蛋白過剰）と脱水を是正する。",
            },
            "reptile": {
                "safe": True,
                "dosage": "5 mg/kg PO q24h (experimental, extrapolated). Combine with fluid therapy, POTZ correction and dietary protein reduction.",
                "dosage_ja": "5 mg/kg 経口 24時間毎（試験的・外挿）。輸液・POTZ是正・蛋白制限と併用する。",
                "notes": "Gout in reptiles is usually secondary to chronic dehydration, renal disease or excess dietary protein — correct husbandry first. Monitor uric acid; discontinue if renal function deteriorates.",
                "notes_ja": "爬虫類の痛風は慢性脱水・腎疾患・蛋白過剰食に続発することが多い — まず飼育環境を是正。尿酸値をモニタリングし、腎機能悪化時は中止。",
            },
        },
        "side_effects": "Hepatotoxicity (reported in humans — monitor if used long term), GI upset, urate crystalluria if dehydrated",
        "side_effects_ja": "肝毒性（ヒトで報告 — 長期使用時はモニタリング）、消化器症状、脱水下では尿酸結晶尿",
        "contraindications": "Significant renal impairment with urolithiasis risk; dehydration (correct first). Human hepatotoxicity led to market withdrawal in some countries — use is experimental and adjunctive in animals.",
        "contraindications_ja": "尿石リスクを伴う重度腎障害。脱水（先に補正）。ヒトでは肝毒性により一部の国で販売中止 — 動物での使用は試験的・補助的。",
        "drug_interactions": [],
    },
    {
        "id": "metformin",
        "search_aliases": ["メトホルミン", "メトグルコ", "グリコラン", "Metformin"],
        "name": "Metformin",
        "name_ja": "メトホルミン",
        "category": "endocrine",
        "mechanism": "Biguanide insulin sensitizer: activates AMP-kinase, suppressing hepatic gluconeogenesis and enhancing peripheral (muscle) insulin-mediated glucose uptake without stimulating insulin secretion — no hypoglycemia risk as monotherapy.",
        "mechanism_ja": "ビグアナイド系インスリン抵抗性改善薬。AMPキナーゼを活性化して肝糖新生を抑制し、末梢（筋）でのインスリン介在性グルコース取り込みを増強する。インスリン分泌は刺激しないため単剤で低血糖を起こさない。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "15-30 mg/kg PO q8-12h, given 30-60 min before feeding/turnout (oral bioavailability is low, ~4-7%; peak effect timed to the glycemic challenge). Durham 2008: 15 mg/kg q12h improved insulin sensitivity in EMS ponies.",
                "dosage_ja": "15-30 mg/kg 経口 8-12時間毎。給餌・放牧の30-60分前に投与（経口バイオアベイラビリティは約4-7%と低く、血糖負荷に合わせる）。Durham 2008: 15 mg/kg 12時間毎でEMSポニーのインスリン感受性が改善。",
                "notes": "Adjunct for EMS / insulin dysregulation with laminitis risk when diet + exercise are insufficient. Evidence is mixed (effect may act largely at the enteric level) — dietary NSC restriction and weight loss remain primary. Reassess insulin (oral sugar test) after 6-12 weeks.",
                "notes_ja": "食事・運動療法で不十分なEMS/インスリン調節異常（蹄葉炎リスク例)の補助療法。エビデンスは限定的（作用は主に腸管レベルの可能性）— NSC制限と減量が第一。6-12週後にインスリン（経口糖負荷試験）を再評価。",
            },
            "cat": {
                "safe": True,
                "dosage": "25-50 mg/cat PO q12h (historic; limited efficacy). Insulin (glargine/PZI) or SGLT2 inhibitors (bexagliflozin/velagliflozin) are strongly preferred for feline diabetes.",
                "dosage_ja": "25-50 mg/頭 経口 12時間毎（過去の用法。有効性は限定的）。猫糖尿病にはインスリン（グラルギン/PZI）またはSGLT2阻害薬（ベキサグリフロジン/ベラグリフロジン）が強く優先される。",
                "notes": "Trials in diabetic cats showed poor response with lethargy, inappetence and vomiting. Avoid in renal insufficiency (lactic acidosis risk). Retained mainly for historical completeness.",
                "notes_ja": "糖尿病猫での試験は反応不良で、元気消失・食欲不振・嘔吐が報告された。腎機能低下例では使用を避ける（乳酸アシドーシスリスク）。現在は主に歴史的位置づけ。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not indicated — canine diabetes is insulin-dependent (β-cell loss); insulin sensitizer monotherapy cannot control glycemia.",
                "dosage_ja": "適応なし — 犬の糖尿病はインスリン依存性（β細胞喪失）であり、インスリン抵抗性改善薬の単独では血糖管理不能。",
                "notes": "Use insulin. No established metformin role in dogs.",
                "notes_ja": "インスリンを使用する。犬でのメトホルミンの確立された役割はない。",
            },
            "degu": {
                "safe": True,
                "dosage": "Not established; degu insulin resistance is managed with strict diet (no sugars/fruit), weight control and exercise — drug therapy is rarely required.",
                "dosage_ja": "用量未確立。デグーのインスリン抵抗性は厳格な食事管理（糖分・果物禁止）・体重管理・運動で管理し、薬物療法が必要になることは稀。",
                "notes": "Degus develop diet-induced hyperglycemia/cataracts readily; prevention through husbandry is the standard of care.",
                "notes_ja": "デグーは食事性の高血糖・白内障を起こしやすい。飼育管理による予防が標準。",
            },
        },
        "side_effects": "GI upset (inappetence, vomiting, diarrhea), lethargy (cats); lactic acidosis with renal impairment (rare)",
        "side_effects_ja": "消化器症状（食欲不振・嘔吐・下痢）、猫で元気消失。腎機能低下例で乳酸アシドーシス（稀）",
        "contraindications": "Renal insufficiency, hepatic failure, dehydration/shock, severe illness (lactic acidosis risk). Not a substitute for insulin in insulin-dependent diabetes.",
        "contraindications_ja": "腎機能不全、肝不全、脱水・ショック、重症疾患（乳酸アシドーシスリスク）。インスリン依存性糖尿病でのインスリンの代替にはならない。",
        "drug_interactions": [
            {
                "drug": "Insulin",
                "effect": "Additive glucose lowering when combined; monitor for hypoglycemia (combination rarely used in veterinary patients)",
                "effect_ja": "併用で血糖降下作用が相加的。低血糖に注意（獣医療での併用は稀）",
            },
            {
                "drug": "Furosemide",
                "effect": "May increase metformin levels; monitor renal function and hydration",
                "effect_ja": "メトホルミン血中濃度を上昇させることがある。腎機能と水和状態をモニタリング",
            },
        ],
    },
]
