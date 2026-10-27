"""Drug batch 88 – 2026-10 第80弾.

Benazepril + spironolactone fixed-dose combination (Cardalis, Ceva) —
authorised in the EU/UK for congestive heart failure caused by chronic
degenerative (myxomatous) mitral valve disease in dogs. Both components were
in the dictionary, but the once-daily combination tablet that many clinics
use for MMVD stage C was not, so its label dose (and the fact that it already
contains an ACE inhibitor and an aldosterone antagonist) could not be looked
up or pair-checked.
Evidence: Cardalis SPC (EMA, EMEA/V/C/002780); Coffman M, Guillot E,
Blondel T, et al. Clinical efficacy of a benazepril and spironolactone
combination in dogs with congestive heart failure due to myxomatous mitral
valve disease: The BEnazepril Spironolactone STudy (BESST). J Vet Intern Med
2021;35:1673-1687; Bernay F, Bland JM, Häggström J, et al. Efficacy of
spironolactone on survival in dogs with naturally occurring mitral
regurgitation caused by myxomatous mitral valve disease. J Vet Intern Med
2010;24:331-341; Keene BW et al. ACVIM consensus guidelines for MMVD in dogs.
J Vet Intern Med 2019;33:1127-1140.
"""

DRUGS_BATCH_88 = [
    {
        "id": "benazepril_spironolactone",
        "search_aliases": [
            "カルダリス",
            "Cardalis",
            "ベナゼプリル・スピロノラクトン",
            "ベナゼプリル＋スピロノラクトン",
            "benazepril/spironolactone",
            "spironolactone/benazepril",
        ],
        "no_component_index": True,
        "name": "Benazepril + Spironolactone (Cardalis)",
        "name_ja": "ベナゼプリル・スピロノラクトン配合錠（カルダリス）",
        "category": "cardiovascular",
        "mechanism": "Fixed-dose combination of an ACE inhibitor (benazepril hydrochloride) and a mineralocorticoid-receptor (aldosterone) antagonist (spironolactone). Blocking both angiotensin II formation and the action of aldosterone that escapes ACE inhibition ('aldosterone breakthrough') reduces sodium/water retention and myocardial fibrosis in congestive heart failure.",
        "mechanism_ja": "ACE阻害薬（ベナゼプリル塩酸塩）と鉱質コルチコイド受容体（アルドステロン）拮抗薬（スピロノラクトン）の配合錠。アンジオテンシンIIの生成と、ACE阻害下でも再上昇するアルドステロン（アルドステロン・ブレイクスルー）の作用を同時に抑え、うっ血性心不全のナトリウム・水分貯留と心筋線維化を軽減する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Label dose: 0.25 mg/kg benazepril hydrochloride + 2 mg/kg spironolactone PO q24h with food (tablets 2.5/20 mg, 5/40 mg, 10/80 mg — choose the strength by body weight per the SPC). Used in ACVIM stage C/D MMVD alongside furosemide (± pimobendan) as needed. Check creatinine and potassium before starting and 1-2 weeks after starting or changing the dose, then at each recheck.",
                "dosage_ja": "ラベル用量: ベナゼプリル塩酸塩 0.25 mg/kg ＋ スピロノラクトン 2 mg/kg を1日1回、食事と共に経口投与（錠剤 2.5/20 mg・5/40 mg・10/80 mg — 体重に応じて添付文書の規格を選択）。ACVIM ステージC/Dの僧帽弁閉鎖不全症で、必要に応じてフロセミド（±ピモベンダン）と併用する。開始前と、開始・用量変更の1〜2週間後にクレアチニンとカリウムを測定し、以後は再診ごとに確認する。",
                "notes": "BESST (Coffman 2021 JVIM): in dogs with CHF from MMVD on standard therapy, the combination reduced the composite of cardiac death/euthanasia/worsening compared with benazepril alone. The tablet already contains an ACE inhibitor and an aldosterone antagonist — do not add separate benazepril, enalapril or spironolactone. Spironolactone is anti-androgenic: reversible prostatic atrophy in intact males. Not authorised for cats (spironolactone causes ulcerative facial dermatitis in some cats, notably Maine Coons). Not available in Japan as this combination — the two components can be prescribed separately at the same doses.",
                "notes_ja": "BESST試験（Coffman 2021 JVIM）: 標準治療中の僧帽弁閉鎖不全症によるうっ血性心不全の犬で、ベナゼプリル単剤と比べて心臓死・安楽死・悪化の複合転帰を減らした。本剤にはACE阻害薬とアルドステロン拮抗薬が既に含まれるため、ベナゼプリル・エナラプリル・スピロノラクトンを別に追加しない。スピロノラクトンは抗アンドロゲン作用があり、未去勢雄で可逆的な前立腺萎縮が起こる。猫には適応がない（一部の猫、特にメインクーンでスピロノラクトンによる潰瘍性顔面皮膚炎）。国内では配合錠としては流通していない — 2成分を同じ用量で別々に処方できる。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not authorised for cats.",
                "dosage_ja": "猫には適応がない。",
                "notes": "Spironolactone has caused ulcerative facial dermatitis in cats (notably Maine Coons) — use the individual components only if specifically indicated and monitored.",
                "notes_ja": "スピロノラクトンにより猫（特にメインクーン）で潰瘍性顔面皮膚炎が報告されている。個々の成分を使う場合も適応を慎重に判断し監視する。",
            },
        },
        "contraindications": "Breeding, pregnant or lactating dogs; hypoadrenocorticism; hyperkalaemia or hyponatraemia; hypotension; acute renal failure; aortic stenosis or other outflow obstruction; dogs already receiving a separate ACE inhibitor or aldosterone antagonist.",
        "contraindications_ja": "繁殖・妊娠・授乳中の犬、副腎皮質機能低下症、高カリウム血症・低ナトリウム血症、低血圧、急性腎不全、大動脈狭窄など流出路の閉塞、別にACE阻害薬またはアルドステロン拮抗薬を投与中の犬。",
        "side_effects": [
            "Hyperkalaemia (especially with renal impairment or potassium supplements)",
            "Azotaemia / decline in renal function",
            "Hypotension, lethargy, inappetence",
            "Reversible prostatic atrophy in intact males",
        ],
        "side_effects_ja": [
            "高カリウム血症（特に腎機能低下時・カリウム補充中）",
            "高窒素血症・腎機能の低下",
            "低血圧・元気消失・食欲低下",
            "未去勢雄の可逆的な前立腺萎縮",
        ],
        "drug_interactions": [
            {
                "drug": "Spironolactone",
                "effect": "Duplicate aldosterone antagonist — the combination tablet already contains spironolactone.",
                "effect_ja": "アルドステロン拮抗薬の重複 — 配合錠に既にスピロノラクトンが含まれる。",
                "severity": "major",
            },
            {
                "drug": "Benazepril",
                "effect": "Duplicate ACE inhibitor — the combination tablet already contains benazepril.",
                "effect_ja": "ACE阻害薬の重複 — 配合錠に既にベナゼプリルが含まれる。",
                "severity": "major",
            },
            {
                "drug": "Potassium gluconate",
                "effect": "Potassium supplements add to the potassium-retaining effect — risk of hyperkalaemia.",
                "effect_ja": "カリウム補充はカリウム保持作用に相加し、高カリウム血症のリスクとなる。",
                "severity": "major",
            },
            {
                "drug": "Meloxicam",
                "effect": "NSAIDs reduce the antihypertensive/natriuretic effect and increase the risk of renal impairment and hyperkalaemia.",
                "effect_ja": "NSAIDsは降圧・ナトリウム利尿作用を減弱し、腎機能低下と高カリウム血症のリスクを高める。",
                "severity": "moderate",
            },
            {
                "drug": "Trilostane",
                "effect": "Both raise serum potassium — monitor electrolytes closely.",
                "effect_ja": "いずれも血清カリウムを上昇させる。電解質を厳密に監視する。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Cardalis Summary of Product Characteristics (EMA, EMEA/V/C/002780).",
            "Coffman M, Guillot E, Blondel T, et al. Clinical efficacy of a benazepril and spironolactone combination in dogs with congestive heart failure due to myxomatous mitral valve disease: The BEnazepril Spironolactone STudy (BESST). J Vet Intern Med 2021;35:1673-1687.",
            "Bernay F, Bland JM, Häggström J, et al. Efficacy of spironolactone on survival in dogs with naturally occurring mitral regurgitation caused by myxomatous mitral valve disease. J Vet Intern Med 2010;24:331-341.",
            "Keene BW, Atkins CE, Bonagura JD, et al. ACVIM consensus guidelines for the diagnosis and treatment of myxomatous mitral valve disease in dogs. J Vet Intern Med 2019;33:1127-1140.",
        ],
    },
]
