"""Drug batch 37 – referenced-but-absent agents surfaced by the 2026-08 audit (5th sweep).

A katakana token-frequency sweep of disease treatment protocols found three
agents that VetDict's own content instructs clinicians to use — with explicit
doses — yet were absent from the formulary:

  - タウリン (taurine): 768 treatment-text references. The definitive therapy
    for feline taurine-deficiency dilated cardiomyopathy and a standard
    adjunct for canine (diet-associated) DCM, ferret and guinea-pig
    cardiomyopathy — all cited with doses in VetDict disease entries.
  - カルシトニン (salmon calcitonin): cited with doses in rabbit/bird/parakeet
    hypervitaminosis-D entries (4-6 IU/kg SC) and relevant to cholecalciferol
    rodenticide toxicosis and reptile NSHP.
  - アンピシリン・スルバクタム (ampicillin-sulbactam, Unasyn): the empirical
    sepsis antibiotic named in VetDict's parvovirus/panleukopenia and
    pneumonia protocols ("アンピシリン・スルバクタム 22-30 mg/kg IV q8h");
    only plain ampicillin was carried.

References:
  - Pion PD et al. Science 1987;237:764-768 — taurine deficiency as the cause
    of feline DCM; myocardial failure reversible with supplementation.
  - Kittleson MD et al. J Vet Intern Med 1997;11:204-211 (MUST trial) —
    taurine + carnitine responsive DCM in American Cocker Spaniels.
  - Freeman LM et al. JAVMA 2018;253:1390-1394 — diet-associated DCM in dogs.
  - Plumb's Veterinary Drug Handbook, 10th ed — taurine, calcitonin salmon,
    ampicillin-sulbactam dosing.
  - Carpenter's Exotic Animal Formulary, 6th ed — avian/rabbit calcitonin.
  - Mader's Reptile and Amphibian Medicine and Surgery, 3rd ed — calcitonin
    in NSHP only after normocalcemia is established.
"""

DRUGS_BATCH_37: list[dict] = [
    {
        "id": "taurine",
        "search_aliases": ["タウリン補充", "タウリン補給"],
        "name": "Taurine",
        "name_ja": "タウリン",
        "category": "supplements",
        "mechanism": "Sulfur-containing β-amino acid essential in cats (minimal hepatic synthesis from cysteine). Required for myocardial calcium handling and contractility, retinal photoreceptor integrity, and bile-acid conjugation (cats conjugate bile acids exclusively with taurine). Deficiency causes reversible dilated cardiomyopathy and irreversible central retinal degeneration.",
        "mechanism_ja": "含硫β-アミノ酸。猫では肝でのシステインからの合成能が低く必須栄養素。心筋のカルシウム動態・収縮性、網膜光受容体の維持、胆汁酸抱合（猫はタウリン抱合のみ）に必須。欠乏は可逆性の拡張型心筋症と不可逆性の中心性網膜変性を引き起こす。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "250-500 mg/cat PO q12h. Continue at least 12-16 weeks; echocardiographic improvement of taurine-deficiency DCM typically appears within 3-6 months (Pion 1987).",
                "dosage_ja": "250-500 mg/頭 経口 12時間毎。最低12-16週継続。タウリン欠乏性DCMの心エコー改善は通常3-6ヶ月以内に現れる（Pion 1987）。",
                "notes": "Measure whole-blood taurine (<250 nmol/mL = deficient) before supplementation where possible. Deficiency is now rare on complete commercial diets — screen home-prepared, vegetarian and dog-food-fed cats.",
                "notes_ja": "可能なら投与前に全血タウリン濃度を測定（<250 nmol/mLで欠乏）。総合栄養食では欠乏は稀 — 手作り食・菜食・ドッグフード給餌の猫でスクリーニングを。",
            },
            "dog": {
                "safe": True,
                "dosage": "500-1000 mg PO q8-12h (dogs <25 kg: 500 mg; ≥25 kg: 1 g). Often combined with L-carnitine 50-100 mg/kg PO q8h in American Cocker Spaniel DCM (MUST trial).",
                "dosage_ja": "500-1000 mg 経口 8-12時間毎（25 kg未満: 500 mg、25 kg以上: 1 g）。アメリカン・コッカー・スパニエルのDCMではL-カルニチン 50-100 mg/kg 経口 8時間毎と併用（MUST試験）。",
                "notes": "Indicated in taurine-responsive DCM (Cocker Spaniel, Golden Retriever, Newfoundland) and diet-associated (grain-free/legume-rich) DCM — measure plasma/whole-blood taurine and change the diet as well (Freeman 2018).",
                "notes_ja": "タウリン反応性DCM（コッカー・スパニエル、ゴールデン・レトリーバー、ニューファンドランド）およびグレインフリー/豆類主体食関連DCMに適応。血漿/全血タウリン測定と食事変更を併行する（Freeman 2018）。",
            },
            "ferret": {
                "safe": True,
                "dosage": "250 mg/kg PO q24h (empirical) as adjunct in dilated cardiomyopathy.",
                "dosage_ja": "250 mg/kg 経口 24時間毎（経験的）。拡張型心筋症の補助療法として。",
                "notes": "Nutritional benefit unproven in ferrets but supplementation is low-risk; continue standard heart-failure therapy (pimobendan, furosemide).",
                "notes_ja": "フェレットでの有効性エビデンスは限定的だが低リスク。標準的心不全治療（ピモベンダン・フロセミド）を継続する。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "100 mg/kg PO q24h (empirical) as adjunct in dilated cardiomyopathy.",
                "dosage_ja": "100 mg/kg 経口 24時間毎（経験的）。拡張型心筋症の補助療法として。",
                "notes": "Empirical adjunct where taurine deficiency is suspected; correct concurrent vitamin C deficiency, which worsens myocardial disease.",
                "notes_ja": "タウリン欠乏疑い例での経験的補助。心筋障害を悪化させるビタミンC欠乏の併発を必ず是正する。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "100 mg/kg PO q24h (empirical, extrapolated).",
                "dosage_ja": "100 mg/kg 経口 24時間毎（経験的・外挿）。",
                "notes": "Rarely indicated; herbivore diets are not taurine-dependent. Use only as cardiologist-directed adjunct.",
                "notes_ja": "適応は稀（草食動物はタウリン要求性が低い）。循環器診療の補助としてのみ使用。",
            },
        },
        "side_effects": "Very well tolerated; occasional mild GI upset at high doses",
        "side_effects_ja": "忍容性は非常に高い。高用量で軽度の消化器症状が出ることがある",
        "contraindications": "None significant. Supplementation does not replace diet correction in diet-associated DCM.",
        "contraindications_ja": "重大な禁忌なし。食事関連DCMでは食事の是正を伴わない補充のみでは不十分。",
        "drug_interactions": [],
    },
    {
        "id": "calcitonin_salmon",
        "search_aliases": ["カルシトニン", "サケカルシトニン", "Calcitonin"],
        "name": "Calcitonin (Salmon)",
        "name_ja": "カルシトニン（サケ）",
        "category": "endocrine",
        "mechanism": "Polypeptide hormone that inhibits osteoclastic bone resorption and increases renal calcium excretion, lowering serum calcium. Salmon calcitonin is markedly more potent than mammalian calcitonin at mammalian receptors.",
        "mechanism_ja": "破骨細胞性骨吸収を抑制し腎からのCa排泄を促進して血清カルシウムを低下させるポリペプチドホルモン。サケ由来カルシトニンは哺乳類受容体に対し哺乳類型より高力価。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "4-6 IU/kg SC q8-12h for hypercalcemia of cholecalciferol (vitamin D3) rodenticide toxicosis, refractory to fluids/furosemide/steroids.",
                "dosage_ja": "4-6 IU/kg 皮下 8-12時間毎。コレカルシフェロール（ビタミンD3）系殺鼠剤中毒などの高Ca血症で、輸液・フロセミド・ステロイドに反応しない場合。",
                "notes": "Effect wanes with repeated dosing (receptor down-regulation); bisphosphonates (pamidronate) are now often preferred for sustained control. Monitor ionized calcium.",
                "notes_ja": "反復投与で効果が減弱（受容体ダウンレギュレーション）。持続的制御にはビスホスホネート（パミドロン酸）が現在は好まれることが多い。イオン化Caをモニタリング。",
            },
            "cat": {
                "safe": True,
                "dosage": "4-6 IU/kg SC q8-12h (hypercalcemia; limited feline data — extrapolated).",
                "dosage_ja": "4-6 IU/kg 皮下 8-12時間毎（高Ca血症。猫のデータは限定的・外挿）。",
                "notes": "Anorexia and vomiting are the main adverse effects; reassess need at each dose.",
                "notes_ja": "主な副作用は食欲不振と嘔吐。投与毎に必要性を再評価する。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "4-6 IU/kg SC q12h for severe hypercalcemia (vitamin D toxicosis).",
                "dosage_ja": "4-6 IU/kg 皮下 12時間毎。重度高Ca血症（ビタミンD中毒）時。",
                "notes": "Combine with saline diuresis and low-calcium diet; rabbits normally run high serum calcium — confirm true pathological hypercalcemia first.",
                "notes_ja": "生理食塩水利尿・低Ca食と併用。ウサギは生理的に血清Caが高いため、真の病的高Ca血症であることを先に確認する。",
            },
            "bird": {
                "safe": True,
                "dosage": "4 IU/kg IM q12h (hypercalcemia/hypervitaminosis D); regimens up to 50 IU/kg SC q24h × 3 days are also published (Carpenter 6th ed).",
                "dosage_ja": "4 IU/kg 筋注 12時間毎（高Ca血症・ビタミンD過剰症）。50 IU/kg 皮下 24時間毎×3日のレジメンも報告あり（Carpenter 6th ed）。",
                "notes": "Stop all vitamin D/calcium supplementation first; support renal perfusion with fluids — soft-tissue mineralization may be irreversible.",
                "notes_ja": "まず全てのビタミンD・Ca補給を中止。輸液で腎灌流を維持 — 軟部組織石灰化は不可逆のことがある。",
            },
            "reptile": {
                "safe": True,
                "dosage": "50 IU/kg IM once weekly × 2-3 doses for NSHP — ONLY after serum calcium is normalized with calcium ± vitamin D therapy.",
                "dosage_ja": "50 IU/kg 筋注 週1回×2-3回（NSHP/代謝性骨疾患）。カルシウム±ビタミンD療法で血清Caを正常化した後にのみ投与。",
                "notes": "Giving calcitonin to a still-hypocalcemic reptile precipitates fatal hypocalcemic tetany (Mader 3rd ed). Verify normocalcemia and provide UV-B/dietary correction concurrently.",
                "notes_ja": "低Ca血症のままの爬虫類への投与は致死的な低Caテタニーを誘発する（Mader 3rd ed）。正常Ca血症の確認が絶対条件。UV-B照射・食事是正を並行する。",
            },
        },
        "side_effects": "Anorexia, vomiting/nausea, hypersensitivity (foreign polypeptide), hypocalcemia with overdose",
        "side_effects_ja": "食欲不振、嘔吐・悪心、過敏反応（異種ポリペプチド）、過量で低Ca血症",
        "contraindications": "Hypocalcemia (absolute — especially reptile NSHP before calcium correction). Efficacy declines with repeated use.",
        "contraindications_ja": "低カルシウム血症（絶対禁忌 — 特にCa補正前の爬虫類NSHP）。反復投与で効果減弱。",
        "drug_interactions": [
            {
                "drug": "Vitamin D / calcium supplements",
                "effect": "Pharmacological antagonism — stop supplementation when treating hypercalcemia",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "ampicillin_sulbactam",
        "search_aliases": ["スルバクタム", "ユナシン", "Unasyn", "アンピシリンスルバクタム"],
        "name": "Ampicillin-Sulbactam (Unasyn)",
        "name_ja": "アンピシリン・スルバクタム（ユナシン）",
        "category": "antibiotics",
        "mechanism": "Aminopenicillin combined with the β-lactamase inhibitor sulbactam. Sulbactam irreversibly binds bacterial β-lactamases, restoring ampicillin activity against β-lactamase-producing Staphylococcus, E. coli, Klebsiella, Pasteurella and anaerobes — the empirical IV choice for sepsis with GI translocation (parvovirus, panleukopenia) and aspiration pneumonia.",
        "mechanism_ja": "アミノペニシリンとβ-ラクタマーゼ阻害薬スルバクタムの合剤。スルバクタムが細菌のβ-ラクタマーゼに不可逆結合し、産生株（ブドウ球菌・大腸菌・クレブシエラ・パスツレラ・嫌気性菌）へのアンピシリン活性を回復。消化管バクテリアルトランスロケーションを伴う敗血症（パルボ・汎白血球減少症）や誤嚥性肺炎の経験的静注第一選択。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "22-30 mg/kg (combined) IV q8h; sepsis/neutropenia: q6-8h. Often combined with enrofloxacin for gram-negative coverage in parvoviral sepsis.",
                "dosage_ja": "22-30 mg/kg（合剤量）静注 8時間毎。敗血症・好中球減少時は6-8時間毎。パルボ性敗血症ではエンロフロキサシン併用でグラム陰性カバーを追加。",
                "notes": "IV formulation only (oral sulbactam is not absorbed — use amoxicillin-clavulanate for oral step-down). Reduce frequency in severe renal failure.",
                "notes_ja": "静注製剤のみ（スルバクタムは経口吸収されない — 経口ステップダウンはアモキシシリン・クラブラン酸へ）。重度腎不全では投与間隔を延長。",
            },
            "cat": {
                "safe": True,
                "dosage": "22 mg/kg (combined) IV q8h (panleukopenia sepsis prophylaxis, pyothorax, bite-wound sepsis).",
                "dosage_ja": "22 mg/kg（合剤量）静注 8時間毎（汎白血球減少症の敗血症予防、膿胸、咬傷敗血症）。",
                "notes": "Good empirical choice for Pasteurella-dominated bite abscesses and anaerobic infections.",
                "notes_ja": "パスツレラ主体の咬傷膿瘍・嫌気性菌感染への経験的選択として良好。",
            },
            "horse": {
                "safe": True,
                "dosage": "Foal sepsis: 22-44 mg/kg (combined) IV q6-8h, usually with amikacin.",
                "dosage_ja": "子馬敗血症: 22-44 mg/kg（合剤量）静注 6-8時間毎。通常アミカシンと併用。",
                "notes": "Adult horses: use judiciously (broad-spectrum β-lactams and antimicrobial-associated colitis risk).",
                "notes_ja": "成馬では慎重に使用（広域β-ラクタムによる抗菌薬関連大腸炎リスク）。",
            },
            "rabbit": {
                "safe": False,
                "dosage": "Contraindicated.",
                "dosage_ja": "禁忌。",
                "notes": "Aminopenicillins cause fatal clostridial enterotoxemia (dysbiosis) in rabbits by any route.",
                "notes_ja": "アミノペニシリンは投与経路を問わずウサギに致死的なクロストリジウム性腸性毒血症（腸内細菌叢破綻）を起こす。",
            },
            "guinea_pig": {
                "safe": False,
                "dosage": "Contraindicated.",
                "dosage_ja": "禁忌。",
                "notes": "Penicillins are contraindicated in guinea pigs (fatal antibiotic-associated enterotoxemia).",
                "notes_ja": "モルモットにペニシリン系は禁忌（致死的な抗生物質関連腸性毒血症）。",
            },
            "hamster": {
                "safe": False,
                "dosage": "Contraindicated.",
                "dosage_ja": "禁忌。",
                "notes": "Penicillins precipitate fatal Clostridium difficile enterotoxemia in hamsters.",
                "notes_ja": "ハムスターではペニシリン系が致死的なClostridium difficile腸性毒血症を誘発する。",
            },
            "chinchilla": {
                "safe": False,
                "dosage": "Contraindicated.",
                "dosage_ja": "禁忌。",
                "notes": "Hindgut fermenter — penicillins cause fatal dysbiosis.",
                "notes_ja": "後腸発酵動物 — ペニシリン系は致死的な腸内細菌叢破綻を起こす。",
            },
        },
        "side_effects": "Hypersensitivity, injection-site pain/phlebitis, GI upset, antibiotic-associated diarrhea",
        "side_effects_ja": "過敏反応、注射部位疼痛・静脈炎、消化器症状、抗菌薬関連下痢",
        "contraindications": "β-lactam hypersensitivity. Contraindicated in rabbits, guinea pigs, hamsters and chinchillas (fatal enterotoxemia).",
        "contraindications_ja": "β-ラクタム過敏症。ウサギ・モルモット・ハムスター・チンチラには禁忌（致死的腸性毒血症）。",
        "drug_interactions": [
            {
                "drug": "Methotrexate",
                "effect": "Penicillins reduce renal MTX clearance — increased toxicity",
                "severity": "major",
            },
            {
                "drug": "Bacteriostatic antibiotics (tetracyclines, chloramphenicol)",
                "effect": "May antagonize β-lactam bactericidal activity",
                "severity": "minor",
            },
        ],
    },
]
