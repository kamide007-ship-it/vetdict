"""Drug batch 59 – referenced-but-absent agents surfaced by the 2026-09 audit (25th sweep).

An English drug-like-token sweep (dose-context filtered, cross-checked against
find_drugs_in_text on real context snippets) confirmed the katakana matcher is
saturated and found three true monograph gaps plus one large alias gap:

  - Vinorelbine — the formulary's own bronchogenic-carcinoma entries (dog and
    cat) prescribe it by name with doses ("Vinorelbine 15-18 mg/m² IV weekly")
    yet no vinca-alkaloid entry beyond vincristine/vinblastine existed. The
    drug concentrates in lung tissue, which is exactly why the lung-carcinoma
    protocols cite it (Poirier 2004 JVIM).

  - Metyrapone — the feline hyperadrenocorticism entry cites "Metyrapone
    65 mg/kg PO q12h (alternative)" but no 11β-hydroxylase inhibitor existed.
    It is the classic pre-adrenalectomy stabiliser in cats (Feldman & Nelson;
    Plumb's 10th ed).

  - Pasireotide — the feline acromegaly (hypersomatotropism) entry cites
    "Pasireotide 0.03 mg/kg SC q12h" but no somatostatin analog for cats
    existed (octreotide is documented as near-ineffective in cats in its own
    monograph). Scudder 2015 / Gostelow 2017 JVIM.

  - PSGAG alias gap — the Adequan monograph existed
    (id=polysulfated_glycosaminoglycan, name_ja 多硫酸化グリコサミノグリカン) but
    dozens of equine musculoskeletal treatment texts cite it as
    ポリ硫酸グリコサミノグリカン(Adequan) and dog/cat texts as "Adequan (PSGAG)",
    none of which reached the keyword index (Latin paren parts are not
    indexed). Registered in _KATAKANA_VARIANT_ALIASES, not here.

References:
  - Poirier VJ et al. Efficacy of vinorelbine for the treatment of primary
    pulmonary carcinoma in dogs. J Vet Intern Med 2004;18:536-539.
  - Wouda RM et al. / feline vinorelbine case-level reports (limited data).
  - Withrow & MacEwen's Small Animal Clinical Oncology 6th ed — vinca
    alkaloids, neutropenia nadirs, perivascular irritation.
  - Feldman & Nelson, Canine and Feline Endocrinology 4th ed — feline
    hyperadrenocorticism, metyrapone pre-surgical stabilisation.
  - Plumb's Veterinary Drug Handbook 10th ed — metyrapone (cat 65 mg/kg PO
    q8-12h).
  - Scudder CJ et al. Pasireotide for insulin-resistant diabetes mellitus in
    cats with hypersomatotropism. J Vet Intern Med 2015;29:1074-1080.
  - Gostelow R et al. Pasireotide long-acting release treatment for diabetic
    cats with hypersomatotropism. J Vet Intern Med 2017;31:355-364.
"""

DRUGS_BATCH_59 = [
    {
        "id": "vinorelbine",
        "search_aliases": [
            "ビノレルビン",
            "ナベルビン",
            "navelbine",
        ],
        "name": "Vinorelbine",
        "name_ja": "ビノレルビン（ナベルビン）",
        "category": "antineoplastics",
        "mechanism": "Semi-synthetic vinca alkaloid; binds tubulin and inhibits microtubule polymerisation, arresting mitosis in M phase. Unlike vincristine/vinblastine it concentrates in lung tissue (pulmonary concentrations up to 300x plasma), the rationale for its use in primary lung carcinoma.",
        "mechanism_ja": "半合成ビンカアルカロイド。チューブリンに結合して微小管重合を阻害し、M期で細胞分裂を停止させる。ビンクリスチン/ビンブラスチンと異なり肺組織へ高度に集積する（肺内濃度は血漿の最大300倍）ことが、原発性肺癌への使用根拠。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "15 mg/m² IV over 5-10 min q7d (dose escalation to 18 mg/m² if well tolerated — Poirier 2004 JVIM). Primary pulmonary (bronchogenic) carcinoma, pulmonary metastatic disease, histiocytic sarcoma (rescue). CBC before each dose: withhold if neutrophils <2,000-3,000/µL (nadir day 4-7). Administer through a free-flowing IV catheter — perivascular irritant.",
                "dosage_ja": "15 mg/m² を5-10分かけて静注 q7d（忍容性良好なら18 mg/m²まで漸増 — Poirier 2004 JVIM）。原発性肺癌（気管支原性癌）・肺転移病変・組織球性肉腫（レスキュー）。毎回投与前にCBC: 好中球<2,000-3,000/µLで休薬（ナディア4-7日）。血管外漏出は刺激性 — 確実に開通した静脈カテーテルから投与。",
                "notes": "Cytotoxic — handle with chemotherapy precautions (closed-system transfer, gloves). Myelosuppression is dose-limiting; GI upset usually mild. Reduce dose 25-30% in significant hepatic dysfunction (hepatic metabolism/biliary excretion).",
                "notes_ja": "細胞傷害性抗がん薬 — 閉鎖式器具・手袋等の抗がん薬取扱い手順を遵守。用量制限毒性は骨髄抑制で、消化器症状は通常軽度。肝機能障害では25-30%減量（肝代謝・胆汁排泄）。",
            },
            "cat": {
                "safe": True,
                "dosage": "15 mg/m² IV q7-14d (limited feline data — case-level evidence for bronchogenic carcinoma; the site's oncology entries cite 15 mg/m² IV q7d). CBC before each dose; withhold if neutrophils <2,000/µL.",
                "dosage_ja": "15 mg/m² IV q7-14d（猫のデータは限定的 — 気管支原性癌での症例レベルの報告。毎回投与前にCBC、好中球<2,000/µLで休薬）。",
                "notes": "Evidence in cats is far more limited than in dogs — reserve for cases where carboplatin/palliative options have been weighed. Perivascular irritant.",
                "notes_ja": "猫でのエビデンスは犬より大幅に限定的 — カルボプラチンや緩和的選択肢と比較検討のうえで使用。血管外漏出は刺激性。",
            },
        },
        "side_effects": "Neutropenia (dose-limiting, nadir day 4-7), mild GI upset, perivascular irritation on extravasation, lethargy.",
        "side_effects_ja": "好中球減少（用量制限毒性、ナディア4-7日）、軽度の消化器症状、血管外漏出時の血管周囲炎、元気消失。",
        "contraindications": "Pre-existing severe myelosuppression; active infection; do not substitute mg-for-mg for other vinca alkaloids (vincristine/vinblastine doses differ by an order of magnitude).",
        "contraindications_ja": "重度の骨髄抑制・活動性感染症。他のビンカアルカロイドとのmg換算の流用は禁止（ビンクリスチン/ビンブラスチンとは用量が桁違い）。",
        "drug_interactions": [
            {
                "drug": "Other myelosuppressive chemotherapy",
                "effect": "Additive neutropenia — stagger nadirs and monitor CBC",
                "effect_ja": "好中球減少の相加 — ナディアをずらしCBC監視",
                "severity": "major",
            },
            {
                "drug": "Ketoconazole/itraconazole (CYP3A inhibitors)",
                "effect": "Reduced vinca clearance — increased toxicity",
                "effect_ja": "ビンカ系のクリアランス低下 — 毒性増強",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "metyrapone",
        "search_aliases": [
            "メチラポン",
            "メトピロン",
            "metopirone",
        ],
        "name": "Metyrapone",
        "name_ja": "メチラポン（メトピロン）",
        "category": "hormones",
        "mechanism": "11β-hydroxylase (CYP11B1) inhibitor — blocks the final step of cortisol synthesis in the adrenal cortex, lowering circulating cortisol without adrenolysis. Effect is enzymatic and reversible on discontinuation.",
        "mechanism_ja": "11β-ヒドロキシラーゼ（CYP11B1）阻害薬 — 副腎皮質でのコルチゾール合成の最終段階を阻害し、副腎破壊を伴わずに血中コルチゾールを低下させる。作用は酵素阻害で、休薬により可逆。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "65 mg/kg PO q8-12h (Plumb's 10th ed; Feldman & Nelson). Main use: pre-surgical stabilisation of feline hyperadrenocorticism before adrenalectomy — improves skin fragility and diabetic control over 2-4 weeks. Monitor glucose (most cats are diabetic — insulin needs fall as cortisol falls), electrolytes, and for signs of iatrogenic hypoadrenocorticism.",
                "dosage_ja": "65 mg/kg PO q8-12h（Plumb's 10th ed; Feldman & Nelson）。主用途は猫クッシング症候群の副腎摘出前の内科的安定化 — 2-4週間で皮膚脆弱性と糖尿病コントロールが改善。血糖（大半が糖尿病併発 — コルチゾール低下に伴いインスリン必要量が減少）・電解質・医原性副腎皮質機能低下の徴候を監視。",
                "notes": "Availability is limited (human orphan-type product); trilostane is the usual first-line where obtainable. Definitive therapy remains adrenalectomy/hypophysectomy.",
                "notes_ja": "入手性が限られる（ヒト希少疾病用医薬品扱い）。入手可能ならトリロスタンが通常の第一選択。根治は副腎摘出/下垂体摘出。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not used in dogs — trilostane (or mitotane) is the standard medical therapy for canine hyperadrenocorticism; canine metyrapone experience is anecdotal.",
                "dosage_ja": "犬では使用しない — 犬クッシングの内科標準治療はトリロスタン（またはミトタン）で、犬でのメチラポン使用経験は逸話的レベルにとどまる。",
            },
        },
        "side_effects": "Vomiting, lethargy, iatrogenic hypocortisolism (weakness, anorexia); hypoglycemia in diabetic cats as insulin resistance resolves.",
        "side_effects_ja": "嘔吐・元気消失・医原性コルチゾール低下（脱力・食欲不振）。糖尿病猫ではインスリン抵抗性の解除に伴う低血糖。",
        "contraindications": "Documented hypoadrenocorticism. Do not combine with trilostane (additive adrenal suppression).",
        "contraindications_ja": "副腎皮質機能低下症。トリロスタンとの併用禁止（副腎抑制の相加）。",
        "drug_interactions": [
            {
                "drug": "Trilostane",
                "effect": "Additive cortisol suppression — risk of Addisonian crisis",
                "effect_ja": "コルチゾール抑制の相加 — アジソンクリーゼのリスク",
                "severity": "major",
            },
            {
                "drug": "Insulin",
                "effect": "Insulin requirement falls as cortisol falls — monitor for hypoglycemia and reduce dose",
                "effect_ja": "コルチゾール低下に伴いインスリン必要量が減少 — 低血糖を監視し減量",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "pasireotide",
        "search_aliases": [
            "パシレオチド",
            "シグニフォー",
            "signifor",
        ],
        "name": "Pasireotide (Signifor)",
        "name_ja": "パシレオチド（シグニフォー）",
        "category": "hormones",
        "mechanism": "Multireceptor somatostatin analog with high affinity for somatostatin receptor subtypes 1, 2, 3 and 5. Feline somatotroph adenomas express sst5, which octreotide (sst2-selective) barely engages — the pharmacologic reason pasireotide lowers IGF-1 in cats where octreotide fails.",
        "mechanism_ja": "ソマトスタチン受容体サブタイプ1・2・3・5に高親和性のマルチ受容体ソマトスタチンアナログ。猫の成長ホルモン産生下垂体腺腫はsst5を発現し、sst2選択的なオクトレオチドはほぼ作用しない — パシレオチドが猫でIGF-1を低下させうる薬理学的根拠。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Short-acting: 0.03 mg/kg SC q12h (Scudder 2015 JVIM — lowers IGF-1 and insulin requirement in hypersomatotropism/acromegaly). Long-acting release (LAR): 6-8 mg/kg IM q4wk (Gostelow 2017 JVIM — some cats achieved diabetic remission). Monitor blood glucose closely and reduce insulin as sensitivity improves — hypoglycemia is the main practical risk.",
                "dosage_ja": "短時間作用型: 0.03 mg/kg SC q12h（Scudder 2015 JVIM — 先端巨大症/下垂体性ソマトトロピン過剰症でIGF-1とインスリン必要量を低下）。持続性（LAR）: 6-8 mg/kg IM 4週毎（Gostelow 2017 JVIM — 一部の猫で糖尿病寛解）。インスリン感受性の改善に伴い血糖を厳密に監視しインスリンを減量 — 実務上の主リスクは低血糖。",
                "notes": "Extremely expensive; diarrhea/soft stool common. Definitive therapy remains hypophysectomy or radiotherapy — pasireotide is medical management where surgery/RT is unavailable or declined.",
                "notes_ja": "極めて高価。下痢・軟便が高頻度。根治療法は下垂体摘出術または放射線治療 — パシレオチドは手術/放射線が選択できない場合の内科管理。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not established in dogs — canine pituitary-dependent hyperadrenocorticism is managed with trilostane; pasireotide remains investigational in dogs.",
                "dosage_ja": "犬では確立していない — 犬の下垂体性クッシングはトリロスタンで管理し、パシレオチドは研究段階。",
            },
        },
        "side_effects": "Diarrhea/soft stool, hypoglycemia (as insulin resistance resolves), injection-site reactions, cholelithiasis with chronic use (human data).",
        "side_effects_ja": "下痢・軟便、低血糖（インスリン抵抗性の解除に伴う）、注射部位反応、長期使用での胆石（ヒトデータ）。",
        "contraindications": "Do not start without concurrent glucose monitoring in insulin-treated cats.",
        "contraindications_ja": "インスリン治療中の猫では血糖モニタリング体制なしに開始しない。",
        "drug_interactions": [
            {
                "drug": "Insulin",
                "effect": "Rapidly falling insulin requirement — hypoglycemia if dose not reduced",
                "effect_ja": "インスリン必要量が急速に低下 — 減量しないと低血糖",
                "severity": "major",
            },
            {
                "drug": "Cyclosporine",
                "effect": "Reduced cyclosporine absorption (human data)",
                "effect_ja": "シクロスポリンの吸収低下（ヒトデータ）",
                "severity": "moderate",
            },
        ],
    },
]
