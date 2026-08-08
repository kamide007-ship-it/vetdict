"""Drug batch 32 – SGLT2 inhibitors for feline diabetes mellitus.

The cat Diabetes Mellitus disease entry explicitly recommends
"Bexagliflozin (Bexacat) and velagliflozin — SGLT2 inhibitors" (AAHA 2023
guidance) as first-line options for otherwise-healthy, insulin-naive diabetic
cats, but neither drug existed in the drug dictionary — a clinician reading the
treatment protocol had no formulary entry to consult for dose, monitoring or
the euglycemic-DKA safety warnings that make this class unusual. Both entries
carry the class-defining caution prominently: SGLT2 inhibitors can cause
euglycemic diabetic ketoacidosis (normal glucose does NOT rule out DKA — ketone
monitoring is mandatory), and they must not be used in cats that are, or have
been, on insulin.

References:
  - FDA NADA 141-568 (Bexacat, bexagliflozin) freedom-of-information summary, 2022.
  - Hadd MJ et al. JVIM 2023;37(3):915-924 — bexagliflozin field study, 84% success.
  - FDA NADA 141-576 (Senvelgo, velagliflozin oral solution) approval, 2023.
  - Niessen SJM et al. JVIM 2024;38(4):2099-2119 — velagliflozin vs insulin RCT
    (non-inferiority, 1 mg/kg PO q24h).
  - Behrend E et al. 2023 AAHA Selected Endocrinopathies of Dogs and Cats
    Guidelines — SGLT2 inhibitor positioning and eDKA monitoring.
  - Plumb's Veterinary Drug Handbook, 10th ed.
"""

from __future__ import annotations

DRUGS_BATCH_32: list[dict] = [
    {
        "id": "bexagliflozin",
        "name": "Bexagliflozin (Bexacat)",
        "name_ja": "ベキサグリフロジン（ベキサキャット）",
        "category": "endocrine",
        "mechanism": (
            "Sodium-glucose cotransporter-2 (SGLT2) inhibitor. Blocks glucose "
            "reabsorption in the renal proximal tubule, producing therapeutic "
            "glucosuria that lowers blood glucose independently of insulin. "
            "First oral once-daily tablet approved for feline diabetes mellitus "
            "(FDA 2022) in otherwise healthy, insulin-naive cats."
        ),
        "mechanism_ja": (
            "ナトリウム・グルコース共輸送体2（SGLT2）阻害薬。腎近位尿細管でのグルコース"
            "再吸収を阻害し、治療的糖尿によりインスリン非依存的に血糖を低下させる。"
            "インスリン未治療で他は健康な糖尿病猫を適応とする、猫糖尿病初の経口1日1回"
            "投与錠（FDA 2022年承認）。"
        ),
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": (
                    "15 mg/cat PO q24h (fixed-dose tablet; cats ≥ 3.0 kg, ≥ 1 year). "
                    "Insulin-naive cats only. Baseline: rule out ketonuria/ketonemia, "
                    "hepatic disease and pancreatitis before starting."
                ),
                "dosage_ja": (
                    "15 mg/頭 経口 1日1回（固定用量錠。体重3.0 kg以上・1歳以上）。"
                    "インスリン未治療の猫のみ。開始前にケトン尿/ケトン血症・肝疾患・"
                    "膵炎の除外を行う。"
                ),
                "notes": (
                    "Monitor beta-hydroxybutyrate/urine ketones — euglycemic DKA can occur "
                    "with NORMAL blood glucose; any inappetence, vomiting or lethargy in a "
                    "treated cat warrants ketone testing. 84% treatment success at day 56 "
                    "(Hadd 2023). Do not transition insulin-treated cats onto this drug."
                ),
                "notes_ja": (
                    "β-ヒドロキシ酪酸/尿ケトンを監視 — 血糖が正常でも正常血糖DKAが起こりうる。"
                    "投与中の猫の食欲不振・嘔吐・元気消失は直ちにケトン検査の適応。"
                    "56日時点の治療成功率84%（Hadd 2023）。インスリン治療中の猫の"
                    "本剤への切替は不可。"
                ),
            },
            "dog": {
                "safe": False,
                "dosage": "Not established",
                "dosage_ja": "用量未確立",
                "notes": "Not approved in dogs; canine diabetes is insulin-dependent (type 1-like) — SGLT2 monotherapy risks DKA.",
                "notes_ja": "犬では未承認。犬の糖尿病はインスリン依存性（1型類似）でSGLT2単剤はDKAリスクがあるため適応外。",
            },
        },
        "side_effects": (
            "Euglycemic diabetic ketoacidosis (most serious — can be fatal; glucose may be "
            "normal), vomiting, diarrhoea, anorexia, dehydration, polyuria (osmotic), "
            "urinary tract infection. Hypoglycaemia is rare (insulin-independent mechanism)."
        ),
        "side_effects_ja": (
            "正常血糖糖尿病性ケトアシドーシス（最重要 — 致死的になりうる。血糖は正常のことがある）、"
            "嘔吐、下痢、食欲不振、脱水、浸透圧性多尿、尿路感染症。低血糖は稀"
            "（インスリン非依存機序のため）。"
        ),
        "contraindications": (
            "Cats currently or previously treated with insulin; ketonuria/ketonemia at "
            "baseline; hepatic disease; reduced renal function; pancreatitis (current or "
            "historical — increases eDKA risk); anorexic, dehydrated or debilitated cats."
        ),
        "contraindications_ja": (
            "インスリン投与中または投与歴のある猫、開始時にケトン尿/ケトン血症のある猫、"
            "肝疾患、腎機能低下、膵炎（現病歴・既往歴ともeDKAリスクを上げる）、"
            "食欲不振・脱水・衰弱状態の猫。"
        ),
        "drug_interactions": [
            {
                "drug": "insulin",
                "effect": "Contraindicated combination — concurrent or prior insulin therapy markedly raises euglycemic DKA risk on SGLT2 inhibitors",
                "effect_ja": "併用禁忌 — インスリンの併用・使用歴はSGLT2阻害薬での正常血糖DKAリスクを著しく高める",
            },
            {
                "drug": "corticosteroids",
                "effect": "Induce insulin resistance and promote ketogenesis; avoid — destabilises glycaemic control and raises DKA risk",
                "effect_ja": "インスリン抵抗性を誘導しケトン産生を促進。血糖コントロールを不安定化しDKAリスクを上げるため回避",
            },
            {
                "drug": "furosemide",
                "effect": "Additive volume depletion with osmotic diuresis; monitor hydration",
                "effect_ja": "浸透圧利尿と相加的な循環血液量減少。水和状態を監視",
            },
        ],
    },
    {
        "id": "velagliflozin",
        "name": "Velagliflozin (Senvelgo)",
        "name_ja": "ベラグリフロジン（センベルゴ）",
        "category": "endocrine",
        "mechanism": (
            "Sodium-glucose cotransporter-2 (SGLT2) inhibitor formulated as a "
            "once-daily oral solution (first liquid SGLT2i for cats, FDA 2023). "
            "Induces renal glucosuria to lower blood glucose without insulin; "
            "weight-based dosing suits cats across the size range. Non-inferior "
            "to insulin glargine in the SENSATION randomised trial (Niessen 2024)."
        ),
        "mechanism_ja": (
            "1日1回の経口液剤として製剤化されたナトリウム・グルコース共輸送体2（SGLT2）"
            "阻害薬（猫初の液剤SGLT2i、FDA 2023年承認）。腎性糖尿を誘導しインスリン"
            "非依存的に血糖を低下。体重換算投与のため体格を問わず投与しやすい。"
            "ランダム化試験でインスリングラルギンに非劣性（Niessen 2024）。"
        ),
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": (
                    "1 mg/kg PO q24h (oral solution, with or without food). "
                    "Insulin-naive cats only. Rule out ketonuria/ketonemia before starting."
                ),
                "dosage_ja": (
                    "1 mg/kg 経口 1日1回（液剤。食事の有無を問わない）。"
                    "インスリン未治療の猫のみ。開始前にケトン尿/ケトン血症を除外。"
                ),
                "notes": (
                    "Same class warning as bexagliflozin: monitor ketones — euglycemic DKA "
                    "can develop with normal glucose, most often in the first weeks. "
                    "Check ketones promptly if appetite drops or vomiting/lethargy appears."
                ),
                "notes_ja": (
                    "ベキサグリフロジンと同じクラス警告: ケトンを監視 — 血糖正常でも"
                    "正常血糖DKAが特に投与初期数週間に発生しうる。食欲低下・嘔吐・"
                    "元気消失があれば直ちにケトン検査。"
                ),
            },
            "dog": {
                "safe": False,
                "dosage": "Not established",
                "dosage_ja": "用量未確立",
                "notes": "Not approved in dogs; canine diabetes is insulin-dependent — SGLT2 monotherapy risks DKA.",
                "notes_ja": "犬では未承認。犬の糖尿病はインスリン依存性でSGLT2単剤はDKAリスクがあるため適応外。",
            },
        },
        "side_effects": (
            "Euglycemic diabetic ketoacidosis (monitor ketones — glucose may be normal), "
            "loose stool/diarrhoea (most common), vomiting, polyuria, dehydration, "
            "urinary tract infection. Hypoglycaemia rare."
        ),
        "side_effects_ja": (
            "正常血糖糖尿病性ケトアシドーシス（ケトン監視 — 血糖は正常のことがある）、"
            "軟便/下痢（最多）、嘔吐、多尿、脱水、尿路感染症。低血糖は稀。"
        ),
        "contraindications": (
            "Cats currently or previously treated with insulin; ketonuria/ketonemia at "
            "baseline; hepatic or significant renal disease; pancreatitis; anorexic, "
            "dehydrated or debilitated cats."
        ),
        "contraindications_ja": (
            "インスリン投与中または投与歴のある猫、開始時にケトン尿/ケトン血症のある猫、"
            "肝疾患・高度の腎機能低下、膵炎、食欲不振・脱水・衰弱状態の猫。"
        ),
        "drug_interactions": [
            {
                "drug": "insulin",
                "effect": "Contraindicated combination — concurrent or prior insulin therapy markedly raises euglycemic DKA risk on SGLT2 inhibitors",
                "effect_ja": "併用禁忌 — インスリンの併用・使用歴はSGLT2阻害薬での正常血糖DKAリスクを著しく高める",
            },
            {
                "drug": "corticosteroids",
                "effect": "Induce insulin resistance and promote ketogenesis; avoid — destabilises glycaemic control and raises DKA risk",
                "effect_ja": "インスリン抵抗性を誘導しケトン産生を促進。血糖コントロールを不安定化しDKAリスクを上げるため回避",
            },
        ],
    },
]
