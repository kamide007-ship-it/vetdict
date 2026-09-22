"""Drug batch 67 – 2026-09 audit (第54弾): sirolimus (Felycin-CA1).

Felycin-CA1 (sirolimus delayed-release tablets) is the FIRST drug ever
FDA-approved (conditional approval, 2025) for a feline cardiac indication:
management of ventricular hypertrophy in cats with subclinical hypertrophic
cardiomyopathy (HCM) — the most common feline heart disease (up to ~1 in 7
cats). The formulary carried no mTOR inhibitor at all, and the feline HCM
flagship entries had no disease-modifying option to point at (atenolol/
diltiazem are symptomatic; clopidogrel is thromboprophylaxis).

Honest evidence framing: conditional approval means a *reasonable
expectation* of effectiveness (RAPACAT randomized controlled trial —
delayed-release rapamycin attenuated progression of LV wall thickening
at 6 months; Kaplan et al. 2023) with full effectiveness data still being
collected. The label-defining safety facts are documented: diabetes
mellitus and pre-existing liver disease contraindications, the
swallow-whole delayed-release formulation, CYP3A4/P-glycoprotein
interaction surface (azoles, calcium channel blockers, amiodarone,
cyclosporine; P-gp substrates eprinomectin/emodepside), and live-vaccine
caution.

References:
  - FELYCIN-CA1 (sirolimus delayed-release tablets) US label (DailyMed);
    FDA conditional approval 2025 — target dose 0.3 mg/kg PO once weekly
    with food; weight-band tablet table; cats <2.5 kg cannot be dosed.
  - Kaplan JL et al. — RAPACAT trial: once-weekly delayed-release
    rapamycin in cats with subclinical HCM (basis of conditional approval).
  - Plumb's Veterinary Drug Handbook 10th ed — sirolimus (mTOR inhibitor)
    pharmacology and interaction profile.
"""

DRUGS_BATCH_67 = [
    {
        "id": "sirolimus",
        "search_aliases": [
            "シロリムス",
            "ラパマイシン",
            "フェリシン",
            "felycin",
            "rapamycin",
        ],
        "name": "Sirolimus Delayed-Release (Felycin-CA1)",
        "name_ja": "シロリムス徐放錠（フェリシン-CA1）",
        "category": "cardiovascular",
        "mechanism": "mTOR (mTORC1) inhibitor. Pathologic cardiomyocyte hypertrophy is driven in part by chronic mTORC1 activation; intermittent low-dose inhibition attenuates hypertrophic signaling. First drug FDA-approved (conditional, 2025) for a feline cardiac indication: management of ventricular hypertrophy in subclinical HCM. Conditional approval = reasonable expectation of effectiveness based on the randomized RAPACAT trial (attenuated LV wall-thickness progression at 6 months, Kaplan JAVMA 2023); definitive effectiveness data are still accumulating.",
        "mechanism_ja": "mTOR（mTORC1）阻害薬。病的心筋肥大の一部は慢性的なmTORC1活性化により駆動され、間欠的低用量阻害が肥大シグナルを減弱させる。猫の心疾患に対して史上初めてFDAが承認（2025年条件付き承認）した薬剤で、適応は無症候性肥大型心筋症（HCM）の心室肥大管理。条件付き承認＝有効性は無作為化RAPACAT試験（週1回投与で6ヶ月時点の左室壁厚進行を抑制 — Kaplan JAVMA 2023）に基づく「合理的期待」段階であり、完全な有効性データは収集継続中。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Target 0.3 mg/kg PO once WEEKLY, with food (label). Delayed-release tablets (0.4 / 1.2 / 2.4 mg) must be swallowed whole — never split, crush or chew. Weight bands: 2.5-3.2 kg = 2x0.4 mg; 3.3-4.8 kg = 1.2 mg; 4.9-6.4 kg = 0.4+1.2 mg; 6.5-9.6 kg = 2.4 mg; >9.6 kg = 1.2+2.4 mg. Cats <2.5 kg cannot be accurately dosed. Indication: subclinical HCM (end-diastolic LV wall >=6 mm) WITHOUT congestive heart failure, systemic hypertension or severe LVOT obstruction.",
                "dosage_ja": "目標用量 0.3 mg/kg PO **週1回**・食事と共に（ラベル）。徐放錠（0.4/1.2/2.4 mg）は必ず丸ごと嚥下 — 分割・粉砕・咀嚼不可（徐放性が失われる）。体重帯: 2.5-3.2 kg=0.4 mg×2錠、3.3-4.8 kg=1.2 mg、4.9-6.4 kg=0.4+1.2 mg、6.5-9.6 kg=2.4 mg、9.6 kg超=1.2+2.4 mg。**2.5 kg未満の猫は正確に投与できない**。適応: 無症候性HCM（拡張末期左室壁厚≥6 mm）で、うっ血性心不全・全身性高血圧・重度LVOT閉塞の無い症例。",
                "notes": "Screen FIRST: biochemistry to rule out liver disease, glucose/history to rule out diabetes (both contraindicated), echo to confirm subclinical status. Monitor ALT/AST every 1-2 months initially, then every 6-12 months; discontinue immediately if diabetes mellitus develops (one trial cat progressed to fatal DKA). May blunt response to LIVE vaccines (killed rabies response was adequate).",
                "notes_ja": "投与前スクリーニング必須: 生化学検査で肝疾患を除外・血糖/病歴で糖尿病を除外（いずれも禁忌）、心エコーで無症候性ステージを確認。ALT/AST は開始後1-2ヶ月毎→安定後6-12ヶ月毎に監視。治療中に糖尿病を発症したら直ちに中止（治験中1例が致死的DKAへ進行）。生ワクチンへの免疫応答を減弱させうる（不活化狂犬病ワクチンの応答は保たれた）。",
            },
            "dog": {
                "safe": False,
                "dosage": "No approved indication or validated dose in dogs",
                "dosage_ja": "犬では承認適応・検証済み用量なし",
                "notes": "Canine use remains investigational (aging/oncology trials); do not extrapolate the feline cardiac label",
                "notes_ja": "犬での使用は臨床試験段階（老化・腫瘍学領域）。猫の心臓ラベルを外挿しない",
            },
        },
        "side_effects": [
            "Hepatic transaminase elevation (ALT/AST)",
            "Diabetes mellitus (discontinue immediately; DKA reported)",
            "Lethargy, vomiting, diarrhea, inappetence",
            "Cardiac events reported in trial population (arrhythmia, CHF, syncope, pericardial effusion)",
        ],
        "side_effects_ja": [
            "肝酵素上昇（ALT/AST）",
            "糖尿病（発症時は直ちに中止 — DKA進行例の報告）",
            "元気消失・嘔吐・下痢・食欲不振",
            "治験集団で心イベントの報告（不整脈・CHF・失神・心膜液貯留）",
        ],
        "contraindications": "Diabetes mellitus; pre-existing liver disease; cats <2.5 kg (cannot be dosed); cats with CHF, systemic hypertension or severe LVOT obstruction (outside the label population); pregnant/breastfeeding handlers should avoid contact",
        "contraindications_ja": "糖尿病；既存の肝疾患；2.5 kg未満の猫（正確な投与不可）；うっ血性心不全・全身性高血圧・重度LVOT閉塞例（ラベル対象外集団）；妊娠中・授乳中の取扱者は接触を避ける",
        "drug_interactions": [
            {
                "drug": "Azole antifungals (ketoconazole/itraconazole)",
                "effect": "CYP3A4/P-gp inhibition markedly raises sirolimus exposure — avoid or use extreme caution",
                "effect_ja": "CYP3A4/P糖蛋白阻害でシロリムス曝露が大幅に上昇 — 併用回避または最大限慎重に",
                "severity": "major",
            },
            {
                "drug": "Calcium channel blockers (diltiazem/amlodipine), amiodarone",
                "effect": "CYP3A4/P-gp inhibition raises sirolimus exposure (note: diltiazem is a common HCM co-medication — reassess before combining)",
                "effect_ja": "CYP3A4/P糖蛋白阻害でシロリムス曝露上昇（ジルチアゼムはHCM併用薬の定番 — 併用前に再評価）",
                "severity": "major",
            },
            {
                "drug": "Cyclosporine",
                "effect": "Shared CYP3A4/P-gp pathway raises exposure of both immunosuppressants",
                "effect_ja": "CYP3A4/P糖蛋白経路の競合で両免疫抑制薬の曝露が上昇",
                "severity": "major",
            },
            {
                "drug": "Eprinomectin / emodepside (P-gp substrates)",
                "effect": "P-gp competition — use caution, especially with MDR1-type sensitivity",
                "effect_ja": "P糖蛋白競合 — 併用注意（MDR1型感受性ではさらに慎重に）",
                "severity": "moderate",
            },
            {
                "drug": "Live (modified-live) vaccines",
                "effect": "Immunosuppression may blunt vaccine response — prefer killed vaccines during treatment",
                "effect_ja": "免疫抑制により生ワクチン応答が減弱しうる — 治療中は不活化ワクチンを優先",
                "severity": "moderate",
            },
        ],
    },
]
