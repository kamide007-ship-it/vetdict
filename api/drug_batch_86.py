"""Drug batch 86 – 2026-10 第77弾 (referenced-but-absent sweep #39).

All three agents are named with doses in the site's own treatment texts but had
no monograph, so the treatment chips, the reverse "diseases using this drug"
index and the interaction checker could not resolve them.

1. Potassium gluconate — feline CKD / hypokalaemic polymyopathy / RTA /
   hyperaldosteronism texts (~15 references): "Potassium gluconate 2-4 mEq/cat
   PO q12h". The dictionary carried IV potassium chloride and potassium
   citrate but no oral gluconate salt — the standard chronic oral supplement.
   Evidence: Dow SW et al. Hypokalemia in cats: 186 cases (1984-1987). JAVMA
   1989;194:1604-1608; Plumb's Veterinary Drug Handbook 10th ed; IRIS 2023
   treatment recommendations (hypokalaemia in CKD).

2. Imatinib mesylate — canine/feline mast cell tumour and GIST texts:
   "Imatinib mesylate 10 mg/kg PO q24h (KIT-positive tumors)".
   Evidence: Isotani M et al. Efficacy and safety of imatinib in dogs with
   mast cell tumors. JVIM 2008;22:985-988; Isotani M et al. feline MCT, JVIM
   2010;24:1490-1493; Irie M et al. canine GIST, J Vet Med Sci 2015.

3. Zoledronate (zoledronic acid) — canine osteosarcoma bone pain and
   hypercalcaemia texts: "zoledronate 0.1 mg/kg IV q28d" / "0.1-0.25 mg/kg IV".
   Evidence: Fan TM et al. Evaluation of intravenous zoledronate in dogs with
   malignant osteolysis. JVIM 2008;22:380-387; Fan TM et al. Double-blind
   placebo-controlled trial of zoledronate in dogs with bone pain, JVIM 2009;
   Withrow & MacEwen's Small Animal Clinical Oncology 6th ed (2019).
"""

DRUGS_BATCH_86 = [
    {
        "id": "potassium_gluconate",
        "search_aliases": [
            "グルコン酸カリウム",
            "ぐるこんさんかりうむ",
            "トゥミルK",
            "Tumil-K",
            "Renal K+",
            "potassium gluconate",
        ],
        "name": "Potassium Gluconate (Tumil-K)",
        "name_ja": "グルコン酸カリウム（トゥミルK）",
        "category": "miscellaneous",
        "mechanism": "Oral potassium salt for chronic replacement. The gluconate salt is non-acidifying and palatable (powder/gel/tablet), so it is preferred to potassium chloride for long-term oral supplementation, particularly in cats with CKD.",
        "mechanism_ja": "慢性的なカリウム補充に用いる経口カリウム塩。グルコン酸塩は酸性化作用がなく嗜好性が良い（粉末・ゲル・錠剤）ため、特にCKDの猫の長期経口補充では塩化カリウムより好まれる。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "2-4 mEq/cat PO q12h for hypokalaemia (serum K <3.5 mEq/L) or hypokalaemic polymyopathy (ventroflexion of the neck, weakness), then adjust to keep serum K in the reference range; maintenance often 2-4 mEq/cat/day. Recheck serum potassium 1-2 weeks after starting or changing the dose, then every 1-3 months in CKD.",
                "dosage_ja": "低カリウム血症（血清K 3.5 mEq/L未満）または低カリウム性多発性筋症（頸部腹側屈曲・脱力）に 2〜4 mEq/頭 経口 12時間毎、以後は血清Kが基準範囲内に収まるよう調整（維持量は 2〜4 mEq/頭/日 程度が多い）。開始・変更の1〜2週後に血清カリウムを再検し、CKDでは以後1〜3ヶ月毎に確認する。",
                "notes": "Oral route only for chronic replacement — severe hypokalaemia (<2.5 mEq/L) or a cat that cannot take oral medication needs IV potassium chloride (never faster than 0.5 mEq/kg/h). IRIS recommends supplementation in hypokalaemic CKD cats. Do not supplement a hyperkalaemic or oliguric cat.",
                "notes_ja": "慢性的な補充は経口のみ — 重度の低カリウム血症（2.5 mEq/L未満）や経口投与できない猫は塩化カリウム静脈内投与（0.5 mEq/kg/時を超えない）。IRISは低カリウム血症を伴うCKDの猫で補充を推奨。高カリウム血症や乏尿の猫には補充しない。",
            },
            "dog": {
                "safe": True,
                "dosage": "Dose to serum potassium: about 2.2 mEq per 100 kcal of daily energy requirement PO, divided, then adjust (Plumb's). Recheck serum potassium 1-2 weeks after starting.",
                "dosage_ja": "血清カリウム値に合わせて用量設定: 1日のエネルギー要求量 100 kcalあたり約 2.2 mEq を経口で分割投与し、以後調整（Plumb's）。開始1〜2週後に血清カリウムを再検する。",
                "notes": "Hypokalaemia is less common in dogs than cats; identify the cause (GI loss, diuretics, insulin therapy, polyuric renal disease).",
                "notes_ja": "犬の低カリウム血症は猫より少ない。原因（消化管からの喪失・利尿薬・インスリン療法・多尿性腎疾患）を特定する。",
            },
        },
        "contraindications": "Hyperkalaemia; oliguric or anuric renal failure; untreated hypoadrenocorticism (Addison's disease); severe dehydration until rehydrated.",
        "contraindications_ja": "高カリウム血症、乏尿・無尿の腎不全、未治療の副腎皮質機能低下症（アジソン病）、重度脱水（補液で是正するまで）。",
        "side_effects": [
            "Vomiting, diarrhoea or inappetence (give with food)",
            "Hyperkalaemia with overdose or reduced renal function",
        ],
        "side_effects_ja": [
            "嘔吐・下痢・食欲低下（食事と一緒に与える）",
            "過量投与や腎機能低下時の高カリウム血症",
        ],
        "drug_interactions": [
            {
                "drug": "Spironolactone",
                "effect": "Potassium-sparing diuretic — additive hyperkalaemia risk; monitor serum potassium closely or reduce the supplement.",
                "effect_ja": "カリウム保持性利尿薬 — 高カリウム血症のリスクが重なる。血清カリウムを厳密に監視するか補充量を減らす。",
                "severity": "major",
            },
            {
                "drug": "Benazepril",
                "effect": "ACE inhibitors (and telmisartan) reduce aldosterone and raise serum potassium — monitor potassium when combining.",
                "effect_ja": "ACE阻害薬（およびテルミサルタン）はアルドステロンを下げて血清カリウムを上げる — 併用時はカリウムを監視する。",
                "severity": "moderate",
            },
            {
                "drug": "Furosemide",
                "effect": "Loop diuretics increase urinary potassium loss — the supplement may need to be increased.",
                "effect_ja": "ループ利尿薬は尿中へのカリウム喪失を増やす — 補充量の増量が必要になることがある。",
                "severity": "minor",
            },
        ],
        "references": [
            "Dow SW, LeCouteur RA, Fettman MJ, Spurgeon TL. Potassium depletion in cats: hypokalemic polymyopathy. JAVMA 1987;191:1563-1568.",
            "Dow SW, Fettman MJ, Curtis CR, LeCouteur RA. Hypokalemia in cats: 186 cases (1984-1987). JAVMA 1989;194:1604-1608.",
            "International Renal Interest Society (IRIS). Treatment recommendations for CKD in cats, 2023.",
            "Plumb's Veterinary Drug Handbook, 10th ed. Wiley-Blackwell, 2023.",
        ],
    },
    {
        "id": "imatinib",
        "search_aliases": [
            "イマチニブ",
            "いまちにぶ",
            "メシル酸イマチニブ",
            "グリベック",
            "Gleevec",
            "Glivec",
            "imatinib mesylate",
        ],
        "name": "Imatinib Mesylate (Gleevec)",
        "name_ja": "イマチニブメシル酸塩（グリベック）",
        "category": "antineoplastics",
        "mechanism": "Tyrosine kinase inhibitor of KIT, PDGFR and BCR-ABL. Most effective in mast cell tumours and gastrointestinal stromal tumours carrying an activating c-KIT mutation (exon 11 internal tandem duplication), where it blocks the constitutively active receptor.",
        "mechanism_ja": "KIT・PDGFR・BCR-ABLのチロシンキナーゼ阻害薬。活性化型c-KIT変異（エクソン11縦列重複）を持つ肥満細胞腫や消化管間質腫瘍（GIST）で最も効果が高く、恒常的に活性化した受容体を阻害する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10 mg/kg PO q24h (Isotani 2008: responses in 10/21 dogs with MCT, including all dogs with exon-11 c-KIT mutations). Used for non-resectable or recurrent KIT-mutated mast cell tumours and GIST, usually when toceranib is not tolerated or has failed. CBC, liver enzymes and creatinine at 2 and 4 weeks, then monthly.",
                "dosage_ja": "10 mg/kg 経口 24時間毎（Isotani 2008: 肥満細胞腫21頭中10頭で奏効、エクソン11のc-KIT変異を持つ例は全例が奏効）。切除不能・再発性のKIT変異陽性肥満細胞腫やGISTで、通常はトセラニブが忍容できないか無効だった場合に用いる。2週後・4週後、以後は毎月、CBC・肝酵素・クレアチニンを確認する。",
                "notes": "Off-label human drug. Test for c-KIT mutation (PCR) where possible — response is best in mutation-positive tumours. Hepatotoxicity is the main dose-limiting toxicity in dogs; stop and recheck if ALT rises markedly. Cytotoxic handling: wear gloves, do not split or crush tablets.",
                "notes_ja": "ヒト用医薬品の適応外使用。可能ならc-KIT変異（PCR）を検査する — 変異陽性腫瘍で反応が最も良い。犬では肝毒性が主な用量制限毒性で、ALTが大きく上昇したら中止して再評価する。細胞傷害性薬として取り扱う（手袋着用、錠剤を割らない・砕かない）。",
            },
            "cat": {
                "safe": True,
                "dosage": "10 mg/kg PO q24h (Isotani 2010: responses in feline mast cell tumours, including systemic disease). Monitor CBC and biochemistry every 2-4 weeks.",
                "dosage_ja": "10 mg/kg 経口 24時間毎（Isotani 2010: 全身性を含む猫の肥満細胞腫で奏効）。CBCと生化学検査を2〜4週毎に確認する。",
                "notes": "Generally better tolerated in cats than toceranib; vomiting and inappetence are the main adverse effects. Off-label human drug.",
                "notes_ja": "猫ではトセラニブより忍容性が良いことが多い。主な有害作用は嘔吐と食欲低下。ヒト用医薬品の適応外使用。",
            },
        },
        "contraindications": "Pregnancy and breeding animals (teratogenic); pre-existing hepatic disease; marked cytopenias. Do not combine with toceranib or masitinib (overlapping tyrosine kinase inhibition).",
        "contraindications_ja": "妊娠・繁殖動物（催奇形性）、既存の肝疾患、顕著な血球減少。トセラニブ・マシチニブとの併用は避ける（チロシンキナーゼ阻害が重複）。",
        "side_effects": [
            "Hepatotoxicity (raised ALT) — dose-limiting in dogs",
            "Vomiting, diarrhoea, inappetence",
            "Neutropenia, anaemia",
            "Peripheral oedema",
        ],
        "side_effects_ja": [
            "肝毒性（ALT上昇） — 犬での用量制限毒性",
            "嘔吐・下痢・食欲低下",
            "好中球減少・貧血",
            "末梢性浮腫",
        ],
        "drug_interactions": [
            {
                "drug": "Toceranib",
                "effect": "Overlapping KIT/PDGFR inhibition — additive toxicity without proven benefit; do not combine.",
                "effect_ja": "KIT/PDGFR阻害が重複 — 利益が証明されないまま毒性が重なる。併用しない。",
                "severity": "major",
            },
            {
                "drug": "Ketoconazole",
                "effect": "CYP3A4 inhibitors (azoles) raise imatinib exposure — monitor liver enzymes and blood counts.",
                "effect_ja": "CYP3A4阻害薬（アゾール系）はイマチニブの血中濃度を上げる — 肝酵素と血球数を監視する。",
                "severity": "moderate",
            },
            {
                "drug": "Phenobarbital",
                "effect": "CYP3A4 inducers lower imatinib exposure and may reduce efficacy.",
                "effect_ja": "CYP3A4誘導薬はイマチニブの血中濃度を下げ、効果を弱めることがある。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Isotani M, Ishida N, Tominaga M, et al. Effect of tyrosine kinase inhibition by imatinib mesylate on mast cell tumors in dogs. J Vet Intern Med 2008;22:985-988.",
            "Isotani M, Yamada O, Lachowicz JL, et al. Mutations in the fifth immunoglobulin-like domain of kit are common and potentially sensitive to imatinib mesylate in feline mast cell tumours. Br J Haematol 2010;148:144-153.",
            "Irie M, Takeuchi Y, Ohtake Y, et al. Imatinib mesylate treatment in a dog with gastrointestinal stromal tumors with a c-kit mutation. J Vet Med Sci 2015;77:1535-1539.",
            "Withrow & MacEwen's Small Animal Clinical Oncology, 6th ed. Elsevier, 2019.",
        ],
    },
    {
        "id": "zoledronate",
        "search_aliases": [
            "ゾレドロン酸",
            "ぞれどろんさん",
            "ゾレドロネート",
            "ゾメタ",
            "Zometa",
            "zoledronic acid",
            "zoledronate",
        ],
        "name": "Zoledronate (Zoledronic Acid, Zometa)",
        "name_ja": "ゾレドロン酸（ゾメタ）",
        "category": "musculoskeletal",
        "mechanism": "Nitrogen-containing bisphosphonate that binds bone mineral and inhibits osteoclast farnesyl pyrophosphate synthase, inducing osteoclast apoptosis. Reduces malignant osteolysis, bone pain and hypercalcaemia; more potent and given over a shorter infusion than pamidronate.",
        "mechanism_ja": "骨ミネラルに結合して破骨細胞のファルネシルピロリン酸合成酵素を阻害し、破骨細胞のアポトーシスを誘導する窒素含有ビスホスホネート。悪性骨溶解・骨痛・高カルシウム血症を軽減する。パミドロネートより強力で、点滴時間も短い。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Malignant osteolysis / bone pain (osteosarcoma, bone metastases): 0.1 mg/kg (maximum 4 mg) IV diluted in 50-100 mL 0.9% NaCl over 15 minutes, q28 days (Fan 2008/2009). Hypercalcaemia of malignancy: 0.1-0.25 mg/kg IV over 15-30 minutes once, repeated in 3-4 weeks if needed. Check creatinine and ionised calcium before each dose.",
                "dosage_ja": "悪性骨溶解・骨痛（骨肉腫・骨転移）: 0.1 mg/kg（最大4 mg）を0.9%生理食塩水 50〜100 mLで希釈し15分かけて静脈内投与、28日毎（Fan 2008/2009）。悪性腫瘍に伴う高カルシウム血症: 0.1〜0.25 mg/kg を15〜30分かけて静脈内単回投与、必要なら3〜4週後に再投与。各投与前にクレアチニンとイオン化カルシウムを確認する。",
                "notes": "A palliative analgesic adjunct (with NSAIDs, gabapentin, amantadine, radiation), not an antitumour treatment. Hydrate before and during the infusion; give over at least 15 minutes (rapid infusion is nephrotoxic). Hypocalcaemia can follow, especially with concurrent calcitonin or in dogs with low vitamin D.",
                "notes_ja": "抗腫瘍治療ではなく緩和的な鎮痛補助（NSAIDs・ガバペンチン・アマンタジン・放射線と併用）。投与前・投与中に補液し、少なくとも15分かけて投与する（急速投与は腎毒性）。特にカルシトニン併用時やビタミンDの低い犬では、投与後に低カルシウム血症が起こりうる。",
            },
            "cat": {
                "safe": True,
                "dosage": "Hypercalcaemia (idiopathic or malignant): 0.1-0.2 mg/kg IV diluted over 15-30 minutes, repeated in 3-4 weeks if needed; check creatinine first.",
                "dosage_ja": "高カルシウム血症（特発性・悪性）: 0.1〜0.2 mg/kg を希釈し15〜30分かけて静脈内投与、必要なら3〜4週後に再投与。事前にクレアチニンを確認する。",
                "notes": "Feline data are limited (case reports and small series). Oral alendronate is the usual long-term option for feline idiopathic hypercalcaemia; reserve IV zoledronate for severe or refractory cases. Avoid in azotaemic cats unless hypercalcaemia is life-threatening.",
                "notes_ja": "猫のデータは限られる（症例報告・小規模な症例集積）。猫の特発性高カルシウム血症の長期管理は経口アレンドロネートが一般的で、静脈内ゾレドロン酸は重度・難治例に限る。高窒素血症の猫では、高カルシウム血症が生命を脅かす場合を除き避ける。",
            },
        },
        "contraindications": "Hypocalcaemia; significant azotaemia or renal failure (dose-related nephrotoxicity); dehydration until corrected; pregnancy.",
        "contraindications_ja": "低カルシウム血症、顕著な高窒素血症・腎不全（用量依存性の腎毒性）、脱水（是正するまで）、妊娠。",
        "side_effects": [
            "Nephrotoxicity (with rapid infusion or pre-existing renal disease)",
            "Hypocalcaemia",
            "Transient fever or lethargy after infusion (acute-phase reaction)",
            "Osteonecrosis of the jaw (rare in dogs)",
        ],
        "side_effects_ja": [
            "腎毒性（急速投与や既存の腎疾患がある場合）",
            "低カルシウム血症",
            "投与後の一過性発熱・元気低下（急性期反応）",
            "顎骨壊死（犬ではまれ）",
        ],
        "drug_interactions": [
            {
                "drug": "Pamidronate",
                "effect": "Two bisphosphonates — no added benefit and additive nephrotoxicity/hypocalcaemia; do not combine.",
                "effect_ja": "ビスホスホネートの重複 — 追加の利益がなく腎毒性・低カルシウム血症が重なる。併用しない。",
                "severity": "major",
            },
            {
                "drug": "Amikacin",
                "effect": "Aminoglycosides and other nephrotoxins add to renal injury and can also lower calcium.",
                "effect_ja": "アミノグリコシド系などの腎毒性薬は腎障害を重ね、カルシウムも低下させうる。",
                "severity": "major",
            },
            {
                "drug": "Meloxicam",
                "effect": "NSAIDs are routinely combined for bone pain, but both stress the kidney — ensure hydration and monitor creatinine.",
                "effect_ja": "骨痛にはNSAIDsと日常的に併用するが、どちらも腎臓に負担をかける — 補液を十分に行いクレアチニンを監視する。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Fan TM, de Lorimier LP, Garrett LD, Lacoste HI. The bone biologic effects of zoledronate in healthy dogs and dogs with malignant osteolysis. J Vet Intern Med 2008;22:380-387.",
            "Fan TM, Charney SC, de Lorimier LP, et al. Double-blind placebo-controlled trial of adjuvant pamidronate with palliative radiotherapy and intravenous doxorubicin for canine appendicular osteosarcoma bone pain. J Vet Intern Med 2009;23:152-160.",
            "Withrow & MacEwen's Small Animal Clinical Oncology, 6th ed. Elsevier, 2019.",
            "Plumb's Veterinary Drug Handbook, 10th ed. Wiley-Blackwell, 2023.",
        ],
    },
]
