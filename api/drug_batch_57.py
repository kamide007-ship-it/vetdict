"""Drug batch 57 – referenced-but-absent agents surfaced by the 2026-09 audit (23rd sweep).

An English drug-like-token sweep (dose-context filtered, cross-checked against
find_drugs_in_text) — the first EN-side sweep after many katakana sweeps —
found two true monograph gaps:

  - Prednisone — 18 disease entries prescribe it by name with doses, and the
    formulary's own prednisolone entry warns "cats cannot efficiently convert
    prednisone" while the drug itself had no monograph (the same
    self-referential gap as neostigmine/aspirin/protamine). The defining
    species facts: dogs convert prednisone→prednisolone efficiently
    (interchangeable); cats achieve markedly lower plasma prednisolone from
    oral prednisone (Graham-Mize & Rosser, Vet Dermatol 2004 — use
    prednisolone); horses absorb/convert oral prednisone so poorly that it
    failed clinical trials for RAO (Peroni et al. 2002 — use prednisolone or
    dexamethasone).

  - Isotretinoin — canine sebaceous adenitis ("1-2 mg/kg PO q24h for severe
    cases"), epitheliotropic (cutaneous) lymphoma retinoid adjunct, and
    multiple keratoacanthoma entries reference it with doses, but no retinoid
    monograph existed. Human teratogen (iPLEDGE class): the handling warning
    for pregnant owners is the class-defining safety fact.

References:
  - Plumb's Veterinary Drug Handbook 10th ed — prednisone/prednisolone.
  - Graham-Mize CA, Rosser EJ. Bioavailability and activity of prednisone
    and prednisolone in the feline patient. Vet Dermatol 2004;15(s1):7.
  - Peroni DL et al. Prednisone per os is likely to have limited efficacy in
    horses. Equine Vet J 2002;34(3):283-287.
  - Muller & Kirk's Small Animal Dermatology 7th ed — retinoid therapy
    (sebaceous adenitis, keratinization disorders).
  - White SD et al. Sebaceous adenitis in dogs and results of treatment with
    isotretinoin and etretinate. JAVMA 1995;207(2):197-200.
  - Withrow & MacEwen's Small Animal Clinical Oncology 6th ed —
    epitheliotropic lymphoma (retinoids as adjunct).
"""

DRUGS_BATCH_57 = [
    {
        "id": "prednisone",
        "search_aliases": [
            "プレドニゾン",
            "prednisone",
        ],
        "name": "Prednisone",
        "name_ja": "プレドニゾン",
        "category": "corticosteroids",
        "mechanism": "Inactive prodrug glucocorticoid: hepatic 11β-hydroxysteroid dehydrogenase 1 converts it to the active prednisolone. Anti-inflammatory/immunosuppressive effects are therefore those of prednisolone — but only in species that convert it efficiently (dogs). Cats and horses convert/absorb it poorly, so prednisolone is the correct choice there.",
        "mechanism_ja": "不活性プロドラッグのグルココルチコイド: 肝の11β-HSD1で活性体プレドニゾロンに変換されて効果を発揮する。抗炎症・免疫抑制作用はプレドニゾロンそのものだが、効率よく変換できる種（犬）に限られる。猫と馬は変換/吸収が不良のため、プレドニゾロンを選択する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Interchangeable with prednisolone in dogs (efficient conversion). Anti-inflammatory: 0.5-1 mg/kg PO q24h then taper. Immunosuppressive (IMHA/ITP etc.): 2 mg/kg/day (or 50-60 mg/m² in large breeds to avoid overdosing) then taper to lowest effective q48h dose (Plumb's 10th ed).",
                "dosage_ja": "犬ではプレドニゾロンと同等に使用可（変換効率が良い）。抗炎症: 0.5-1 mg/kg PO q24h から漸減。免疫抑制（IMHA/ITP等）: 2 mg/kg/日（大型犬は過量回避のため50-60 mg/m²）から最小有効量の隔日投与へ漸減（Plumb's 10th ed）。",
                "notes": "Never stop long courses abruptly (iatrogenic adrenal suppression — taper). PU/PD/polyphagia and panting are expected class effects.",
                "notes_ja": "長期投与の突然中止は不可（医原性副腎抑制 — 漸減する）。多飲多尿・多食・パンティングはクラス共通の予測される作用。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not recommended — use prednisolone instead. Oral prednisone yields markedly lower plasma prednisolone levels in cats (poor conversion; Graham-Mize & Rosser 2004), risking treatment failure at 'equivalent' doses.",
                "dosage_ja": "非推奨 — 猫にはプレドニゾロンを使用する。猫では経口プレドニゾンからの血中プレドニゾロン濃度が著しく低く（変換不良; Graham-Mize & Rosser 2004）、「同等量」でも治療失敗のリスクがある。",
                "notes": "This is a treatment-failure gate, not a toxicity gate: asthma or IBD relapsing on 'prednisone' at textbook doses is a classic conversion-failure presentation — switch to prednisolone.",
                "notes_ja": "毒性ではなく治療失敗を防ぐためのゲート: 教科書用量の「プレドニゾン」で喘息やIBDが再燃するのは変換不良の典型像 — プレドニゾロンへ切り替える。",
            },
            "horse": {
                "safe": False,
                "dosage": "Not recommended — oral prednisone is poorly absorbed/converted in horses and failed to control RAO (heaves) in clinical study (Peroni 2002). Use oral prednisolone or dexamethasone.",
                "dosage_ja": "非推奨 — 馬では経口プレドニゾンの吸収/変換が不良で、RAO（馬喘息）の臨床試験でも効果を示せなかった（Peroni 2002）。経口プレドニゾロンまたはデキサメタゾンを使用する。",
                "notes": "Laminitis-risk counselling applies to any systemic glucocorticoid in horses (EMS/PPID patients especially).",
                "notes_ja": "馬の全身性グルココルチコイド共通の蹄葉炎リスク（特にEMS/PPID例）に留意。",
            },
        },
        "side_effects": "As prednisolone in converting species: PU/PD, polyphagia, panting, iatrogenic Cushing's with chronic use, GI ulceration (especially with NSAIDs), delayed healing, adrenal suppression on abrupt withdrawal",
        "side_effects_ja": "変換可能な種ではプレドニゾロンと同様: 多飲多尿・多食・パンティング・長期で医原性クッシング・消化管潰瘍（特にNSAIDs併用）・治癒遅延・突然中止で副腎抑制",
        "contraindications": "Cats and horses (poor conversion/absorption — use prednisolone). Systemic fungal infection, concurrent NSAIDs, GI ulceration. Do not vaccinate with live vaccines during immunosuppressive dosing.",
        "contraindications_ja": "猫・馬（変換/吸収不良 — プレドニゾロンを使用）。全身性真菌感染、NSAIDs併用、消化管潰瘍。免疫抑制量投与中の生ワクチン接種は避ける。",
        "drug_interactions": [
            {
                "drug": "NSAIDs (meloxicam, carprofen, etc.)",
                "effect": "Markedly increased GI ulceration/perforation risk — never combine; observe a washout when switching",
                "effect_ja": "消化管潰瘍・穿孔リスクが著増 — 併用禁止。切替時はウォッシュアウトを置く",
                "severity": "major",
            },
            {
                "drug": "Insulin",
                "effect": "Glucocorticoid-induced insulin resistance destabilises diabetic control",
                "effect_ja": "グルココルチコイドによるインスリン抵抗性で糖尿病管理が不安定化",
                "severity": "moderate",
            },
            {
                "drug": "Phenobarbital",
                "effect": "Hepatic enzyme induction accelerates glucocorticoid metabolism (reduced effect)",
                "effect_ja": "肝酵素誘導でグルココルチコイド代謝が亢進（効果減弱）",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "isotretinoin",
        "search_aliases": [
            "イソトレチノイン",
            "isotretinoin",
            "13-cis-レチノイン酸",
        ],
        "name": "Isotretinoin (Accutane)",
        "name_ja": "イソトレチノイン（アキュテイン）",
        "category": "dermatology",
        "mechanism": "Synthetic retinoid (13-cis-retinoic acid): binds nuclear retinoid receptors to normalise keratinocyte differentiation/proliferation and shrink sebaceous glands — the basis for its use in canine sebaceous adenitis, keratinization disorders, multiple keratoacanthomas and as a retinoid adjunct in epitheliotropic lymphoma.",
        "mechanism_ja": "合成レチノイド（13-cis-レチノイン酸）: 核内レチノイド受容体を介して角化細胞の分化・増殖を正常化し脂腺を縮小させる。犬の脂腺炎・角化異常症・多発性ケラトアカントーマ、および上皮向性リンパ腫のレチノイド補助療法の根拠となる機序。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Sebaceous adenitis (severe/refractory): 1-2 mg/kg PO q24h with food; expect 6+ weeks for response, then taper to lowest effective dose (White JAVMA 1995; Muller & Kirk 7th ed). Multiple keratoacanthomas: 1-2 mg/kg PO q24h. Epitheliotropic lymphoma (retinoid adjunct): 1-2 mg/kg PO q24h (Withrow & MacEwen 6th ed). Monitor tear production (Schirmer), triglycerides/cholesterol and liver enzymes q4-8wk.",
                "dosage_ja": "脂腺炎（重度/難治）: 1-2 mg/kg PO q24h 食事と共に。反応まで6週以上を見込み、その後最小有効量へ漸減（White JAVMA 1995; Muller & Kirk 7th ed）。多発性ケラトアカントーマ: 1-2 mg/kg PO q24h。上皮向性リンパ腫（レチノイド補助）: 1-2 mg/kg PO q24h（Withrow & MacEwen 6th ed）。涙液量（シルマー）・TG/コレステロール・肝酵素を4-8週毎にモニター。",
                "notes": "Standard-poodle/Akita sebaceous adenitis often also needs topical therapy (propylene-glycol soaks, keratolytic shampoos) and oral cyclosporine is the main alternative. Human prescription drug — availability/compounding varies.",
                "notes_ja": "スタンダードプードル/秋田犬の脂腺炎では外用（プロピレングリコール浸漬・角質溶解シャンプー）併用が多く、経口シクロスポリンが主要な代替。ヒト用処方薬のため入手性/調剤は要確認。",
            },
        },
        "side_effects": "KCS (dry eye — monitor Schirmer), hyperlipidemia, hepatotoxicity (raised enzymes), mucocutaneous dryness, joint stiffness, teratogenicity",
        "side_effects_ja": "乾性角結膜炎（ドライアイ — シルマー値監視）、高脂血症、肝毒性（酵素上昇）、皮膚粘膜の乾燥、関節のこわばり、催奇形性",
        "contraindications": "Pregnant animals (potent teratogen). Pregnant or possibly-pregnant owners must not handle broken/crushed capsules (human iPLEDGE-class teratogen). Pre-existing KCS or significant hepatopathy.",
        "contraindications_ja": "妊娠動物（強力な催奇形性）。妊娠中・妊娠の可能性のある飼い主は破損・粉砕カプセルに素手で触れないこと（ヒトでiPLEDGE管理の催奇形物質）。既存の乾性角結膜炎・重い肝障害。",
        "drug_interactions": [
            {
                "drug": "Vitamin A / retinol supplements",
                "effect": "Additive hypervitaminosis-A toxicity — do not combine",
                "effect_ja": "ビタミンA過剰症の毒性が相加 — 併用しない",
                "severity": "major",
            },
            {
                "drug": "Tetracyclines (doxycycline, minocycline)",
                "effect": "Combined class association with intracranial hypertension (pseudotumor cerebri) in humans — avoid concurrent use",
                "effect_ja": "ヒトで頭蓋内圧亢進（偽脳腫瘍）との関連が両クラスに報告 — 併用を避ける",
                "severity": "moderate",
            },
            {
                "drug": "Cyclosporine",
                "effect": "No adverse synergy documented; sequential rather than concurrent use is typical in sebaceous adenitis",
                "effect_ja": "有害な相乗作用の報告はないが、脂腺炎では併用より逐次切替が一般的",
                "severity": "minor",
            },
        ],
    },
]
