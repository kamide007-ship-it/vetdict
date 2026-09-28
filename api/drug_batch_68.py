"""Drug batch 68 – 2026-09 audit (第55弾): molidustat (Varenzin-CA1).

Varenzin-CA1 (molidustat oral suspension) is the FIRST drug ever
FDA-approved (conditional approval, 2023) for control of nonregenerative
anemia associated with chronic kidney disease in cats — a flagship
problem area of this formulary (the cat CKD entries prescribe
darbepoetin, but carried no needle-free oral alternative and no
HIF-PH-inhibitor class at all).

Why it matters clinically:
  - First-in-class hypoxia-inducible factor prolyl hydroxylase (HIF-PH)
    inhibitor in veterinary medicine: stimulates the cat's OWN
    erythropoietin production instead of injecting a recombinant human
    ESA, so it avoids the anti-rhEPO antibody / pure red cell aplasia
    failure mode documented with epoetin (and much less so darbepoetin).
  - Once-daily ORAL suspension — an at-home option for cats that cannot
    return weekly for darbepoetin injections.

Honest evidence framing: conditional approval = reasonable expectation
of effectiveness while full effectiveness data are still being
collected; darbepoetin remains the conventional standard. The
label-defining safety facts are documented: 28-day treatment cycles
with a mandatory >=7-day pause, weekly PCV monitoring with a STOP
rule (erythrocytosis/thromboembolic risk from overshoot), vomiting as
the most common adverse event, and iron sufficiency as a prerequisite
for any erythropoiesis-stimulating strategy.

References:
  - VARENZIN-CA1 (molidustat oral suspension) US label (Elanco; FDA
    conditional approval 2023) — 5 mg/kg PO q24h up to 28 days,
    repeat cycles after >=7-day pause; monitor PCV.
  - Chalhoub S, Langston CE — anemia of CKD in cats: iron status and
    ESA therapy principles (J Feline Med Surg reviews).
  - Plumb's Veterinary Drug Handbook 10th ed — molidustat monograph.
"""

DRUGS_BATCH_68 = [
    {
        "id": "molidustat",
        "search_aliases": [
            "モリデュスタット",
            "バレンジン",
            "varenzin",
            "HIF-PH阻害薬",
        ],
        "name": "Molidustat (Varenzin-CA1)",
        "name_ja": "モリデュスタット（バレンジン-CA1）",
        "category": "endocrine",
        "mechanism": "Hypoxia-inducible factor prolyl hydroxylase (HIF-PH) inhibitor — first of its class in veterinary medicine. Stabilizes HIF-alpha, which up-regulates the cat's endogenous erythropoietin production and iron-handling genes, stimulating erythropoiesis without administering a recombinant human ESA (avoids the anti-rhEPO antibody / pure red cell aplasia failure mode of epoetin). FDA conditional approval 2023 — the first drug ever approved for control of nonregenerative anemia associated with CKD in cats; conditional approval = reasonable expectation of effectiveness with full data still accumulating.",
        "mechanism_ja": "低酸素誘導因子プロリル水酸化酵素（HIF-PH）阻害薬 — 獣医療で初のクラス。HIF-αを安定化して猫自身の内因性エリスロポエチン産生と鉄利用関連遺伝子を上方制御し、組換えヒトESAを投与せずに赤血球造血を刺激する（エポエチンで問題となる抗rhEPO抗体→赤芽球癆という失敗様式を回避できる）。2023年FDA条件付き承認 — 猫CKD関連の非再生性貧血の管理に対して史上初めて承認された薬剤。条件付き承認＝有効性は「合理的期待」段階で完全なデータは収集継続中。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "5 mg/kg PO once daily for up to 28 days (oral suspension, with or without food). If anemia recurs, the 28-day cycle may be REPEATED only after a pause of at least 7 days. Monitor PCV/HCT weekly during each cycle and STOP dosing once PCV reaches the individual target/normal range — do not dose past target (erythrocytosis risk). Confirm iron sufficiency before/during therapy (iron-deficient cats cannot respond; supplement as needed).",
                "dosage_ja": "5 mg/kg PO 1日1回・最長28日間（経口懸濁液、食事の有無は不問）。貧血が再燃する場合、28日サイクルの再開は**最低7日間の休薬後**のみ可。各サイクル中は**PCV/HCTを週1回監視**し、目標域（正常域）に達したら投与を中止 — 目標を超えて漫然と投与しない（多血症リスク）。治療前・治療中に鉄充足を確認（鉄欠乏では反応できない — 必要に応じ鉄補充）。",
                "notes": "Indication: control of NONregenerative anemia associated with CKD (conditional approval — darbepoetin remains the conventional standard; molidustat is the needle-free oral alternative and avoids anti-rhEPO antibody risk). Most common adverse event: vomiting. Overshoot erythrocytosis raises hyperviscosity/thromboembolic concern — the weekly PCV stop-rule is the core safety control. Work up and treat GI bleeding/iron deficiency as contributing causes of the anemia in parallel.",
                "notes_ja": "適応: CKDに伴う**非再生性**貧血の管理（条件付き承認 — 従来標準はダルベポエチンで、本剤は毎週の通院注射が難しい猫への経口・自宅投与の代替。抗rhEPO抗体リスクを回避できる）。最多の有害事象は嘔吐。過剰造血（多血症）は過粘稠・血栓塞栓の懸念となるため、週1回PCVの中止ルールが安全管理の中核。消化管出血・鉄欠乏など貧血の併存原因の精査・治療を並行する。",
            },
            "dog": {
                "safe": False,
                "dosage": "No approved indication or validated dose in dogs",
                "dosage_ja": "犬では承認適応・検証済み用量なし",
                "notes": "Feline-only conditional approval; canine use is not established — do not extrapolate",
                "notes_ja": "猫限定の条件付き承認。犬での使用は未確立 — 外挿しない",
            },
        },
        "side_effects": [
            "Vomiting (most common)",
            "Erythrocytosis/polycythemia if dosed past target PCV (hyperviscosity, thromboembolic risk)",
            "Hypertension possible with rising red cell mass — recheck blood pressure",
            "Inappetence, lethargy, diarrhea",
        ],
        "side_effects_ja": [
            "嘔吐（最多）",
            "目標PCVを超えた投与による多血症（過粘稠・血栓塞栓リスク）",
            "赤血球量増加に伴う血圧上昇の可能性 — 血圧再評価",
            "食欲不振・元気消失・下痢",
        ],
        "contraindications": "Do not continue dosing once PCV reaches target (stop rule); not for regenerative or non-CKD anemias without a diagnosis (work up blood loss/hemolysis first); iron deficiency must be corrected for the drug to work; safety not established in breeding, pregnant or lactating cats",
        "contraindications_ja": "PCVが目標域に達したら投与継続不可（中止ルール）；診断のつかない再生性貧血・非CKD性貧血には用いない（失血・溶血の精査が先）；鉄欠乏は先に補正しないと効果が出ない；繁殖・妊娠・授乳中の猫での安全性は未確立",
        "drug_interactions": [
            {
                "drug": "Darbepoetin / epoetin (ESAs)",
                "effect": "Do not combine erythropoiesis-stimulating strategies — additive erythrocytosis risk; choose one and monitor PCV",
                "effect_ja": "造血刺激療法同士は併用しない — 多血症リスクが相加。どちらか一方を選択しPCVを監視",
                "severity": "major",
            },
            {
                "drug": "Iron supplements (ferrous sulfate, iron dextran)",
                "effect": "Intentional, often necessary co-therapy — erythropoiesis consumes iron; verify iron status rather than avoiding the combination",
                "effect_ja": "意図的かつしばしば必要な併用 — 造血は鉄を消費するため、併用回避ではなく鉄状態の確認を行う",
                "severity": "moderate",
            },
        ],
    },
]
