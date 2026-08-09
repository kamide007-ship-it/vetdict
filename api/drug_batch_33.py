"""Drug batch 33 – referenced-but-absent drugs found by the 2026-08 audit.

An is-referenced-but-absent sweep of the drug dictionary's own
`drug_interactions` lists and of the anesthesia protocols found five drugs
that the manual talks about but never defines:

  - Methotrexate — referenced by 10 interaction entries (NSAIDs,
    penicillins, salicylates each warn about "methotrexate clearance") and a
    core multi-agent lymphoma / immune-mediated disease drug, yet it had no
    formulary entry of its own.
  - Quinidine sulfate — the treatment of choice for conversion of atrial
    fibrillation in horses (the single most clinically important equine
    antiarrhythmic); referenced by digoxin's interaction list.
  - Pyrimethamine — the backbone (with sulfadiazine) of EPM treatment in
    horses and of avian toxoplasmosis/atoxoplasmosis protocols; referenced by
    the trimethoprim-sulfonamide entry.
  - EMLA cream (lidocaine/prilocaine) — named explicitly by the rabbit
    anesthesia protocols ("EMLA cream for IV catheter placement") with no
    dictionary entry describing dose, onset or the feline methemoglobinemia
    caution.
  - Niacinamide — half of the classic tetracycline/doxycycline +
    niacinamide immunomodulatory combination for canine discoid lupus
    erythematosus and related sterile/immune-mediated dermatoses.

References:
  - Plumb's Veterinary Drug Handbook, 10th ed.
  - Reed SM, Bayly WM, Sellon DC. Equine Internal Medicine, 4th ed —
    quinidine AF conversion protocol; EPM therapy.
  - Reef VB et al. ACVIM consensus statement on equine cardiac disease,
    JVIM 2014 — quinidine monitoring and toxicity endpoints.
  - MacKay RJ et al. EPM treatment review, Vet Clin North Am Equine Pract
    2006; ReBalance (sulfadiazine/pyrimethamine) FDA NADA 141-240.
  - White SD et al. JAVMA 1992;200(9):1497-1500 — tetracycline/niacinamide
    for canine discoid lupus erythematosus.
  - Flecknell PA. BSAVA Manual of Rabbit Medicine — EMLA for marginal ear
    vein catheterisation.
  - Withrow & MacEwen's Small Animal Clinical Oncology, 6th ed —
    methotrexate in multi-agent lymphoma protocols.
"""

from __future__ import annotations

DRUGS_BATCH_33: list[dict] = [
    {
        "id": "methotrexate",
        "name": "Methotrexate (MTX)",
        "name_ja": "メトトレキサート（MTX）",
        "category": "antineoplastics",
        "mechanism": (
            "Folate antagonist: competitively inhibits dihydrofolate reductase, "
            "blocking synthesis of tetrahydrofolate and therefore of purines and "
            "thymidylate. S-phase specific — kills rapidly dividing cells "
            "(lymphoid neoplasia, gut epithelium, marrow). Used in multi-agent "
            "lymphoma protocols and occasionally for immune-mediated disease."
        ),
        "mechanism_ja": (
            "葉酸拮抗薬：ジヒドロ葉酸還元酵素を競合的に阻害し、テトラヒドロ葉酸ひいては"
            "プリン・チミジル酸の合成を阻止する。S期特異的で分裂が速い細胞（リンパ系腫瘍・"
            "腸上皮・骨髄）を傷害する。多剤併用リンパ腫プロトコルの一員として、"
            "また稀に免疫介在性疾患に用いられる。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Multi-agent lymphoma protocols (protocol-dependent): 2.5 mg/m2 PO "
                    "2-3 times weekly, or 0.5-0.8 mg/kg IV every 1-3 weeks per protocol. "
                    "Always verify against the specific written protocol; do not use "
                    "as monotherapy."
                ),
                "dosage_ja": (
                    "多剤併用リンパ腫プロトコル内で使用（プロトコル依存）：2.5 mg/m2 経口 "
                    "週2-3回、またはプロトコルに従い 0.5-0.8 mg/kg 静注 1-3週毎。"
                    "必ず当該プロトコルの記載量を確認し、単剤では使用しない。"
                ),
                "notes": (
                    "CBC before each dose (neutrophil nadir ~4-6 days). Leucovorin "
                    "(folinic acid) 15 mg/m2 q6h rescues overdose/toxicity. GI toxicity "
                    "(vomiting, diarrhea) is dose-limiting in dogs."
                ),
                "notes_ja": (
                    "各投与前にCBC（好中球最低値は約4-6日）。過量・毒性発現時はロイコボリン"
                    "（ホリナートカルシウム）15 mg/m2 q6h でレスキュー。犬では消化器毒性"
                    "（嘔吐・下痢）が用量制限因子。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": (
                    "2.5 mg/m2 (approx. 0.8 mg/kg) PO 2-3 times weekly within "
                    "multi-agent protocols; protocol-dependent."
                ),
                "dosage_ja": ("多剤併用プロトコル内で 2.5 mg/m2（約0.8 mg/kg）経口 週2-3回。プロトコル依存。"),
                "notes": "Monitor CBC and renal values; reduce/withhold if azotemic.",
                "notes_ja": "CBCと腎数値を監視。高窒素血症では減量または休薬。",
            },
            "rabbit": {
                "safe": False,
                "dosage": "Not recommended",
                "dosage_ja": "推奨されない",
                "notes": "Severe GI epithelial toxicity risk in hindgut fermenters; safer protocols exist.",
                "notes_ja": "後腸発酵動物では消化管上皮毒性のリスクが高い。より安全なプロトコルを選択する。",
            },
        },
        "side_effects": (
            "Myelosuppression (neutropenia, thrombocytopenia), GI toxicity "
            "(vomiting, diarrhea, mucositis), hepatotoxicity with chronic use, "
            "nephrotoxicity at high doses (tubular precipitation), alopecia in "
            "predisposed breeds."
        ),
        "side_effects_ja": (
            "骨髄抑制（好中球減少・血小板減少）、消化器毒性（嘔吐・下痢・粘膜炎）、"
            "長期投与での肝毒性、高用量での腎毒性（尿細管内析出）、素因のある犬種での脱毛。"
        ),
        "contraindications": (
            "Renal insufficiency (reduced clearance greatly increases toxicity), "
            "pre-existing myelosuppression, hepatic failure, pregnancy "
            "(teratogenic). Handle as a hazardous drug (chemotherapy precautions)."
        ),
        "contraindications_ja": (
            "腎機能不全（クリアランス低下で毒性が著増）、既存の骨髄抑制、肝不全、"
            "妊娠（催奇形性）。抗がん薬としての取扱い（曝露防護）が必須。"
        ),
        "drug_interactions": [
            {
                "drug": "NSAIDs",
                "effect": "Reduced renal clearance of methotrexate; markedly increased myelosuppression and GI toxicity",
                "effect_ja": "メトトレキサートの腎クリアランス低下。骨髄抑制・消化器毒性が著明に増強",
                "severity": "major",
            },
            {
                "drug": "trimethoprim_sulfa",
                "effect": "Additive folate antagonism — increased risk of megaloblastic cytopenias",
                "effect_ja": "葉酸拮抗作用が相加 — 巨赤芽球性血球減少のリスク増加",
                "severity": "major",
            },
            {
                "drug": "amoxicillin",
                "effect": "Penicillins compete for renal tubular secretion; methotrexate levels rise",
                "effect_ja": "ペニシリン系が腎尿細管分泌で競合し、メトトレキサート血中濃度が上昇",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "quinidine",
        "name": "Quinidine Sulfate",
        "name_ja": "キニジン硫酸塩",
        "category": "antiarrhythmics",
        "mechanism": (
            "Class IA antiarrhythmic: blocks fast sodium channels (slows phase-0 "
            "depolarisation) and potassium channels (prolongs the action "
            "potential and effective refractory period), with vagolytic "
            "(anticholinergic) effects. Prolonging the atrial refractory period "
            "extinguishes the re-entry circuits of atrial fibrillation — the "
            "treatment of choice for pharmacologic conversion of AF in horses."
        ),
        "mechanism_ja": (
            "クラスIA抗不整脈薬：速いナトリウムチャネル遮断（第0相脱分極の減速）と"
            "カリウムチャネル遮断（活動電位持続時間・有効不応期の延長）に加え、"
            "迷走神経遮断（抗コリン）作用を持つ。心房不応期の延長により心房細動の"
            "リエントリー回路を消失させる — 馬の心房細動の薬理学的洞調律復帰における"
            "第一選択薬。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": (
                    "AF conversion: quinidine sulfate 22 mg/kg via nasogastric tube "
                    "q2h until conversion, adverse signs, or 4-6 doses; then q6h "
                    "(ideally guided by plasma quinidine 2-5 ug/mL). Continuous ECG "
                    "throughout. STOP if QRS widens >25% of baseline, rapid "
                    "supraventricular rate >100 bpm, ventricular arrhythmias, "
                    "hypotension, colic or depression develop."
                ),
                "dosage_ja": (
                    "心房細動の洞調律復帰：キニジン硫酸塩 22 mg/kg を経鼻胃チューブで2時間毎、"
                    "復帰・副作用出現・4-6回投与のいずれかまで。その後は6時間毎"
                    "（可能なら血漿キニジン濃度 2-5 μg/mL を指標）。投与中は持続心電図が必須。"
                    "QRS幅が基礎値の25%超に延長、上室性頻拍>100 bpm、心室性不整脈、低血圧、"
                    "疝痛、沈鬱の出現で直ちに中止。"
                ),
                "notes": (
                    "Best conversion rates in AF of <3 months' duration with no "
                    "structural disease. Toxicity: paraphimosis, urticaria, nasal "
                    "mucosal swelling, colic, laminitis (rare), sudden death from "
                    "ventricular tachyarrhythmia. Treat quinidine-induced "
                    "tachycardia with digoxin; sodium bicarbonate IV for QRS "
                    "prolongation/toxicity. Transvenous electrical cardioversion is "
                    "the referral alternative."
                ),
                "notes_ja": (
                    "罹病期間3ヶ月未満・器質的心疾患のない心房細動で復帰率が最良。"
                    "毒性：持続勃起様の陰茎脱出、蕁麻疹、鼻粘膜腫脹、疝痛、蹄葉炎（稀）、"
                    "心室性頻拍による突然死。キニジン誘発性頻拍にはジゴキシン、"
                    "QRS延長・中毒には炭酸水素ナトリウム静注で対応。"
                    "経静脈電気的除細動が紹介施設での代替法。"
                ),
            },
            "dog": {
                "safe": True,
                "dosage": (
                    "6-16 mg/kg PO q6-8h (historic use for supraventricular and "
                    "ventricular arrhythmias). Largely superseded by newer agents "
                    "(sotalol, amiodarone, diltiazem); reserve for refractory cases."
                ),
                "dosage_ja": (
                    "6-16 mg/kg 経口 6-8時間毎（上室性・心室性不整脈への歴史的使用）。"
                    "現在はソタロール・アミオダロン・ジルチアゼム等の新しい薬剤にほぼ置換"
                    "されており、難治例に限って考慮する。"
                ),
                "notes": "GI upset and hypotension common; monitor ECG.",
                "notes_ja": "消化器症状と低血圧が多い。心電図を監視。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not recommended",
                "dosage_ja": "推奨されない",
                "notes": "Safer alternatives exist for feline arrhythmias (atenolol, sotalol, diltiazem).",
                "notes_ja": "猫の不整脈にはより安全な代替薬がある（アテノロール・ソタロール・ジルチアゼム）。",
            },
        },
        "side_effects": (
            "Horses: depression, paraphimosis, urticaria, nasal edema, colic, "
            "diarrhea, hypotension, QRS/QT prolongation, ventricular "
            "tachyarrhythmias, sudden death. Dogs: vomiting, diarrhea, weakness, "
            "hypotension, thrombocytopenia (immune-mediated, rare)."
        ),
        "side_effects_ja": (
            "馬：沈鬱、陰茎脱出、蕁麻疹、鼻粘膜浮腫、疝痛、下痢、低血圧、QRS/QT延長、"
            "心室性頻拍性不整脈、突然死。犬：嘔吐、下痢、脱力、低血圧、"
            "血小板減少（免疫介在性・稀）。"
        ),
        "contraindications": (
            "Complete AV block, congestive heart failure (negative inotropy at "
            "toxic levels), digoxin toxicity, myasthenia gravis. In horses: AF "
            "with resting tachycardia >60 bpm or fractional shortening <32% "
            "warrants pre-treatment digoxin and specialist supervision."
        ),
        "contraindications_ja": (
            "完全房室ブロック、うっ血性心不全（中毒域で陰性変力作用）、ジゴキシン中毒、"
            "重症筋無力症。馬では安静時心拍数>60 bpmまたは左室内径短縮率<32%の心房細動は"
            "ジゴキシン前投与と専門医管理を要する。"
        ),
        "drug_interactions": [
            {
                "drug": "digoxin",
                "effect": "Quinidine roughly doubles serum digoxin (displacement + reduced clearance) — reduce digoxin dose by half and monitor levels",
                "effect_ja": "キニジンは血清ジゴキシン濃度を約2倍に上昇させる（置換＋クリアランス低下）— ジゴキシンを半量に減量し血中濃度を監視",
                "severity": "major",
            },
            {
                "drug": "phenobarbital",
                "effect": "Hepatic enzyme induction accelerates quinidine metabolism; reduced efficacy",
                "effect_ja": "肝酵素誘導によりキニジン代謝が促進され、効果が減弱",
                "severity": "moderate",
            },
            {
                "drug": "cimetidine",
                "effect": "Inhibits quinidine metabolism; increased plasma levels and toxicity risk",
                "effect_ja": "キニジン代謝を阻害し、血中濃度と中毒リスクが上昇",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "pyrimethamine",
        "name": "Pyrimethamine",
        "name_ja": "ピリメタミン",
        "category": "antiparasitics",
        "mechanism": (
            "Inhibits protozoal dihydrofolate reductase with far higher affinity "
            "than for the mammalian enzyme; combined with a sulfonamide "
            "(sequential blockade of folate synthesis) it is synergistically "
            "antiprotozoal against Sarcocystis neurona (EPM), Toxoplasma gondii "
            "and related apicomplexans."
        ),
        "mechanism_ja": (
            "原虫のジヒドロ葉酸還元酵素を哺乳類酵素よりはるかに高い親和性で阻害する。"
            "スルホンアミド（葉酸合成の逐次遮断）との併用で Sarcocystis neurona（EPM）、"
            "Toxoplasma gondii などのアピコンプレクサ原虫に相乗的な抗原虫作用を示す。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": (
                    "EPM: pyrimethamine 1 mg/kg PO q24h WITH sulfadiazine 20 mg/kg "
                    "PO q24h (ReBalance, FDA NADA 141-240) for 90-270 days, 1 hour "
                    "before feeding. Continue until CSF/serologic and clinical "
                    "response criteria are met."
                ),
                "dosage_ja": (
                    "EPM：ピリメタミン 1 mg/kg 経口 1日1回をスルファジアジン 20 mg/kg "
                    "経口 1日1回と併用（ReBalance、FDA NADA 141-240）、90-270日間、"
                    "給餌1時間前に投与。臨床反応と検査所見の改善基準を満たすまで継続。"
                ),
                "notes": (
                    "Monitor CBC monthly (folate-antagonist anemia/leukopenia). Do "
                    "NOT supplement folic acid in pregnant mares on this protocol — "
                    "congenital defects have been reported with concurrent folic "
                    "acid; withdraw treatment or use alternatives (ponazuril, "
                    "diclazuril) in pregnancy."
                ),
                "notes_ja": (
                    "月1回CBCを監視（葉酸拮抗による貧血・白血球減少）。本プロトコル中の"
                    "妊娠馬に葉酸を補充しないこと — 葉酸併用下で先天異常が報告されている。"
                    "妊娠馬では休薬または代替薬（ポナズリル、ジクラズリル）を選択。"
                ),
            },
            "dog": {
                "safe": True,
                "dosage": (
                    "Neosporosis/toxoplasmosis adjunct: 1 mg/kg PO q24h combined "
                    "with a sulfonamide, typically 2-4 weeks."
                ),
                "dosage_ja": (
                    "ネオスポラ症/トキソプラズマ症の補助療法：1 mg/kg 経口 1日1回をスルホンアミドと併用、通常2-4週間。"
                ),
                "notes": "Clindamycin is first-line; add pyrimethamine for refractory neurologic cases. Folinic acid 1 mg/kg/day mitigates myelosuppression.",
                "notes_ja": "第一選択はクリンダマイシン。難治性の神経型に本剤を追加。ホリナート 1 mg/kg/日で骨髄抑制を軽減。",
            },
            "cat": {
                "safe": True,
                "dosage": (
                    "Toxoplasmosis (rarely needed): 0.5-1 mg/kg PO q24h with a "
                    "sulfonamide; clindamycin monotherapy is strongly preferred."
                ),
                "dosage_ja": (
                    "トキソプラズマ症（必要例は稀）：0.5-1 mg/kg 経口 1日1回をスルホンアミド"
                    "と併用。クリンダマイシン単剤が強く推奨される。"
                ),
                "notes": "Cats are sensitive to folate antagonism — anorexia, depression, cytopenias; give folinic acid and keep courses short.",
                "notes_ja": "猫は葉酸拮抗に感受性が高い — 食欲不振・沈鬱・血球減少。ホリナートを併用し投与期間は短く。",
            },
            "bird": {
                "safe": True,
                "dosage": (
                    "Toxoplasmosis/atoxoplasmosis/Sarcocystis: 0.5 mg/kg PO q12h "
                    "with trimethoprim-sulfonamide, 14-30 days (Carpenter's "
                    "Exotic Animal Formulary)."
                ),
                "dosage_ja": (
                    "トキソプラズマ症/アトキソプラズマ症/サルコシスティス症："
                    "0.5 mg/kg 経口 12時間毎をST合剤と併用、14-30日"
                    "（Carpenter's Exotic Animal Formulary）。"
                ),
                "notes": "Important for sarcocystosis outbreaks in outdoor aviaries (opossum exposure, Americas).",
                "notes_ja": "屋外飼育鳥のサルコシスティス症集団発生（米大陸のオポッサム暴露）で重要。",
            },
        },
        "side_effects": (
            "Dose-dependent bone marrow suppression (anemia, leukopenia, "
            "thrombocytopenia), anorexia, vomiting, depression. In horses on "
            "long EPM courses: mild anemia is the most common finding."
        ),
        "side_effects_ja": (
            "用量依存性の骨髄抑制（貧血・白血球減少・血小板減少）、食欲不振、嘔吐、沈鬱。"
            "長期EPM治療中の馬では軽度貧血が最も多い所見。"
        ),
        "contraindications": (
            "Pre-existing significant cytopenias; pregnancy (teratogenic folate "
            "antagonist — especially avoid in pregnant mares); severe hepatic "
            "disease."
        ),
        "contraindications_ja": (
            "既存の高度血球減少、妊娠（催奇形性のある葉酸拮抗薬 — 特に妊娠馬では回避）、重度肝疾患。"
        ),
        "drug_interactions": [
            {
                "drug": "trimethoprim_sulfa",
                "effect": "Additive folate antagonism — myelosuppression risk; monitor CBC when combined",
                "effect_ja": "葉酸拮抗作用が相加 — 骨髄抑制リスク。併用時はCBCを監視",
                "severity": "moderate",
            },
            {
                "drug": "Folic acid",
                "effect": "May antagonise antiprotozoal efficacy; in pregnant mares the combination has been associated with congenital defects",
                "effect_ja": "抗原虫効果を減弱させる可能性。妊娠馬では併用により先天異常の報告がある",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "emla_cream",
        "name": "EMLA Cream (Lidocaine/Prilocaine 2.5%/2.5%)",
        "name_ja": "EMLAクリーム（リドカイン・プリロカイン配合）",
        "category": "anesthetics",
        "mechanism": (
            "Eutectic mixture of local anesthetics: lidocaine 2.5% + prilocaine "
            "2.5% in a cream whose eutectic formulation lets the anesthetics "
            "penetrate intact skin. Blocks cutaneous sodium channels to a depth "
            "of a few millimetres, providing painless venipuncture and IV "
            "catheter placement — named in the rabbit anesthesia protocols for "
            "marginal ear vein catheterisation."
        ),
        "mechanism_ja": (
            "局所麻酔薬の共融混合物：リドカイン2.5%＋プリロカイン2.5%のクリームで、"
            "共融製剤により無傷の皮膚を透過する。皮膚のナトリウムチャネルを数mmの深さまで"
            "遮断し、無痛での採血・静脈カテーテル留置を可能にする — ウサギ麻酔プロトコル"
            "（耳介辺縁静脈カテーテル留置）で言及される製剤。"
        ),
        "species_info": {
            "rabbit": {
                "safe": True,
                "dosage": (
                    "Apply a thin layer to clipped skin over the marginal ear vein "
                    "(or cephalic/saphenous site), cover with an occlusive dressing, "
                    "wait 30-60 min before catheter placement; wipe off before "
                    "puncture."
                ),
                "dosage_ja": (
                    "耳介辺縁静脈（または橈側皮静脈・伏在静脈）上の剃毛部に薄く塗布し、"
                    "密封ドレッシングで被覆して30-60分待ってからカテーテル留置。"
                    "穿刺前に拭き取る。"
                ),
                "notes": "Standard-of-care for stress reduction in rabbit venous access (Flecknell, BSAVA Manual of Rabbit Medicine).",
                "notes_ja": "ウサギの静脈確保時のストレス軽減の標準手技（Flecknell, BSAVA Manual of Rabbit Medicine）。",
            },
            "dog": {
                "safe": True,
                "dosage": "Thin layer under occlusion 45-60 min before venipuncture/catheterisation.",
                "dosage_ja": "密封下で薄層塗布、採血・カテーテル留置の45-60分前。",
                "notes": "Prevent licking (Elizabethan collar or continuous supervision) — oral absorption causes toxicity.",
                "notes_ja": "舐め取りを防止（エリザベスカラーまたは常時監視）— 経口吸収で中毒を起こす。",
            },
            "cat": {
                "safe": True,
                "dosage": (
                    "Thin layer on a SMALL clipped area under occlusion, 30-60 min; remove completely before puncture."
                ),
                "dosage_ja": ("小面積の剃毛部にのみ密封下で薄層塗布、30-60分。穿刺前に完全に拭き取る。"),
                "notes": (
                    "Cats are susceptible to prilocaine-induced methemoglobinemia — "
                    "limit area and contact time, never apply to broken skin, and "
                    "prevent grooming/ingestion."
                ),
                "notes_ja": (
                    "猫はプリロカインによるメトヘモグロビン血症に感受性 — 塗布面積と時間を"
                    "制限し、損傷皮膚には使用せず、グルーミングによる摂取を防ぐ。"
                ),
            },
            "ferret": {
                "safe": True,
                "dosage": "As for cats: small area, occlusion, 30-45 min.",
                "dosage_ja": "猫と同様：小面積・密封・30-45分。",
                "notes": "Useful for jugular venipuncture in conscious ferrets.",
                "notes_ja": "覚醒フェレットの頸静脈採血で有用。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Small area under occlusion 30-45 min before venipuncture (small body mass — minimal amounts).",
                "dosage_ja": "採血30-45分前に小面積へ密封下塗布（体重が小さいためごく少量）。",
                "notes": "Also eases ear vein access in small rodents; watch total dose in very small patients.",
                "notes_ja": "小型げっ歯類の耳静脈確保にも有用。超小型個体では総量に注意。",
            },
        },
        "side_effects": (
            "Local blanching/erythema (transient), methemoglobinemia from "
            "prilocaine (cats, very small patients, or excessive area/time), "
            "systemic local-anesthetic toxicity if ingested or applied to "
            "broken skin."
        ),
        "side_effects_ja": (
            "一過性の局所蒼白/発赤、プリロカインによるメトヘモグロビン血症"
            "（猫・超小型動物・過大な面積/時間）、摂取や損傷皮膚への塗布による"
            "局所麻酔薬の全身中毒。"
        ),
        "contraindications": (
            "Broken or inflamed skin, congenital or acquired methemoglobinemia, "
            "concurrent methemoglobin-inducing drugs (e.g., benzocaine sprays). "
            "Not for application to mucous membranes or eyes."
        ),
        "contraindications_ja": (
            "損傷・炎症皮膚、先天性/後天性メトヘモグロビン血症、メトヘモグロビン誘発薬"
            "（ベンゾカインスプレー等）との併用。粘膜・眼への塗布は不可。"
        ),
        "drug_interactions": [
            {
                "drug": "lidocaine",
                "effect": "Additive systemic local-anesthetic exposure when combined with injectable lidocaine — count toward total lidocaine dose in small patients",
                "effect_ja": "注射用リドカインとの併用で局所麻酔薬の全身暴露が相加 — 小型動物ではリドカイン総投与量に算入する",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "niacinamide",
        "name": "Niacinamide (Nicotinamide)",
        "name_ja": "ニコチン酸アミド（ナイアシンアミド）",
        "category": "dermatological",
        "mechanism": (
            "Immunomodulator: inhibits antigen-IgE-induced histamine release, "
            "mast-cell degranulation and phosphodiesterases, and blocks "
            "leukocyte chemotaxis. Combined with tetracycline or doxycycline "
            "(which suppress in-vitro lymphocyte blastogenesis and complement "
            "activation), the pair is a steroid-sparing therapy for canine "
            "immune-mediated skin disease (White 1992)."
        ),
        "mechanism_ja": (
            "免疫調節薬：抗原-IgE誘発ヒスタミン放出、肥満細胞脱顆粒、ホスホジエステラーゼを"
            "阻害し、白血球走化性を抑制する。テトラサイクリンまたはドキシサイクリン"
            "（リンパ球幼若化・補体活性化を抑制）との併用で、犬の免疫介在性皮膚疾患に対する"
            "ステロイド温存療法となる（White 1992）。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Dogs >10 kg: niacinamide 500 mg PO q8h WITH tetracycline 500 mg "
                    "PO q8h (or doxycycline 5 mg/kg PO q12h). Dogs <10 kg: 250 mg of "
                    "each PO q8h. Clinical response takes 4-8 weeks; taper to q12h "
                    "then q24h after remission."
                ),
                "dosage_ja": (
                    "体重10 kg超の犬：ニコチン酸アミド 500 mg 経口 8時間毎をテトラサイクリン "
                    "500 mg 経口 8時間毎（またはドキシサイクリン 5 mg/kg 経口 12時間毎）と併用。"
                    "10 kg未満：各250 mg 経口 8時間毎。臨床反応まで4-8週。寛解後は12時間毎"
                    "→24時間毎へ漸減。"
                ),
                "notes": (
                    "Indications: discoid lupus erythematosus, symmetric lupoid "
                    "onychodystrophy, sterile granuloma/pyogranuloma, adjunct in "
                    "pemphigus foliaceus. Combine with sun avoidance/topical "
                    "therapy for nasal DLE."
                ),
                "notes_ja": (
                    "適応：円板状エリテマトーデス（DLE）、対称性狼瘡様爪異栄養症、"
                    "無菌性肉芽腫/化膿性肉芽腫、落葉状天疱瘡の補助。鼻部DLEでは"
                    "遮光と外用療法を併用する。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": "Limited data: 125-250 mg/cat PO q12h reported anecdotally with doxycycline for immune-mediated dermatoses.",
                "dosage_ja": "データ限定的：免疫介在性皮膚症に対しドキシサイクリン併用で125-250 mg/頭 経口 12時間毎の使用報告がある。",
                "notes": "Rarely used in cats; specialist guidance advised.",
                "notes_ja": "猫での使用は稀。専門医の指導が望ましい。",
            },
        },
        "side_effects": (
            "Uncommon: vomiting, anorexia, lethargy; rare hepatotoxicity "
            "(elevated liver enzymes) — discontinue if icterus or marked enzyme "
            "rise. (Distinct from niacin/nicotinic acid — niacinamide does not "
            "cause flushing.)"
        ),
        "side_effects_ja": (
            "少ない：嘔吐、食欲不振、元気消失。稀に肝毒性（肝酵素上昇）— 黄疸や著明な"
            "酵素上昇で中止。（ナイアシン/ニコチン酸とは異なり、ニコチン酸アミドは"
            "潮紅を起こさない。）"
        ),
        "contraindications": (
            "Significant hepatic disease; known hypersensitivity. When paired "
            "with tetracyclines, observe tetracycline contraindications "
            "(growing animals, pregnancy)."
        ),
        "contraindications_ja": (
            "重度肝疾患、過敏症の既往。テトラサイクリン系との併用時はテトラサイクリンの禁忌（成長期動物・妊娠）に従う。"
        ),
        "drug_interactions": [
            {
                "drug": "doxycycline",
                "effect": "Intended therapeutic combination for immune-mediated dermatoses (synergistic immunomodulation)",
                "effect_ja": "免疫介在性皮膚疾患に対する意図的な治療的併用（相乗的免疫調節）",
                "severity": "minor",
            },
        ],
    },
]
