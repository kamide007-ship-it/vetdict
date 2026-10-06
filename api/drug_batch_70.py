"""Drug batch 70 – 2026-10 session: gilvetmab (first canine checkpoint inhibitor).

GILVETMAB (Merck Animal Health) — the first USDA conditionally licensed
caninized anti-PD-1 monoclonal antibody in veterinary oncology, indicated
for dogs with mast cell tumors (stages I-III) and melanoma (stages II-III).
The dictionary already carried the other modern canine oncology
immunotherapies (Oncept DNA vaccine, Stelfonta intratumoral injection,
Tanovea) but no checkpoint inhibitor existed, leaving the melanoma/MCT
flagship entries without the newest systemic immunotherapy option.

Evidence:
  - Gilvetmab US conditional license label (Merck Animal Health) —
    10 mg/kg (0.5 mL/kg) IV over at least 30 minutes, every 2 weeks for
    up to 10 treatments.  Conditional license = "reasonable expectation
    of efficacy"; full efficacy/potency not yet demonstrated.
  - JVIM 2026 (PMID 42247661) efficacy/safety study: melanoma objective
    response rate 20% (median time-to-progression 56 days); MCT objective
    response rate 46% (median TTP not reached); serious adverse events
    (anaphylaxis, hypotension, tumor hemorrhage) in 5.9% of dogs;
    pseudoprogression (enlargement before regression) observed.
  - Label/FAQ: dogs must NOT be receiving glucocorticoids or other
    immunosuppressive medication concurrently (blunts PD-1 blockade).
  - Merck gilvetmab FAQ: pretreatment with diphenhydramine 2 mg/kg IM
    within 15-30 minutes of each infusion is recommended (or an oral
    dose prescribed beforehand by the oncologist), and dogs should be
    monitored for at least 1 hour after the infusion — infusion
    reactions including anaphylaxis are documented.
  - NOT licensed for lymphoma (insufficient monotherapy efficacy).
"""

DRUGS_BATCH_70 = [
    {
        "id": "gilvetmab",
        "search_aliases": [
            "ギルベトマブ",
            "抗PD-1抗体",
            "チェックポイント阻害薬",
        ],
        "name": "Gilvetmab (anti-PD-1 mAb)",
        "name_ja": "ギルベトマブ（抗PD-1モノクローナル抗体）",
        "category": "antineoplastics",
        "mechanism": "Caninized IgG monoclonal antibody against PD-1 (programmed cell death protein 1) — the first immune checkpoint inhibitor conditionally licensed for dogs (USDA). Blocks the PD-1/PD-L1 inhibitory axis that tumors exploit to silence cytotoxic T cells, restoring anti-tumor T-cell activity. Because the drug works by re-enabling the patient's own immune response, concurrent immunosuppression (glucocorticoids, cyclosporine) defeats its mechanism, and immune-mediated adverse events are the class-defining toxicity.",
        "mechanism_ja": "PD-1（プログラム細胞死タンパク質1）に対する犬化IgGモノクローナル抗体 — 犬でUSDA条件付きライセンスを取得した初の免疫チェックポイント阻害薬。腫瘍が細胞傷害性T細胞を抑え込むために利用するPD-1/PD-L1抑制経路を遮断し、抗腫瘍T細胞活性を回復させる。患者自身の免疫応答を再起動させる機序のため、免疫抑制薬（グルココルチコイド・シクロスポリン）の併用は作用機序そのものを打ち消し、免疫介在性有害事象がクラス定義的毒性となる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10 mg/kg (0.5 mL/kg) IV infusion over AT LEAST 30 minutes, every 2 weeks, for up to 10 treatments (US conditional license label). REQUIRED PREMEDICATION: diphenhydramine 2 mg/kg IM within 15-30 minutes before each infusion (or an oral dose prescribed beforehand by the oncologist) — infusion reactions including anaphylaxis are documented. Monitor the dog for at least 1 hour after each infusion. Indications: mast cell tumor stages I-III and melanoma stages II-III, as an aid in reducing solid tumor burden.",
                "dosage_ja": "10 mg/kg（0.5 mL/kg）を30分以上かけて緩徐に静脈内点滴、2週毎、最大10回（米国条件付きライセンスのラベル用法）。前投薬必須: 各点滴の15-30分前にジフェンヒドラミン 2 mg/kg IM（腫瘍科医が事前に経口投与を処方した場合はそれでも可）— アナフィラキシーを含むインフュージョンリアクションが報告されているため。点滴終了後も最低1時間は院内でモニタリング。適応: 肥満細胞腫 ステージI-III、メラノーマ ステージII-III（固形腫瘍量減少の補助）。",
                "notes": "Conditional license = 'reasonable expectation of efficacy' (JVIM 2026: melanoma ORR 20%, median TTP 56 days; MCT ORR 46%, median TTP not reached). Serious AEs (anaphylaxis, hypotension, tumor hemorrhage) in 5.9% — hence the diphenhydramine 2 mg/kg IM premedication 15-30 min before each infusion and >=1 hour post-infusion monitoring (Merck FAQ). Pseudoprogression (tumor enlargement before regression) can occur — do not abandon therapy on early size increase alone. NOT licensed for lymphoma (insufficient monotherapy efficacy). Combination options: Oncept vaccine (melanoma), Stelfonta (cutaneous MCT), surgery/RT per oncologist.",
                "notes_ja": "条件付きライセンス（有効性への合理的期待の段階 — JVIM 2026: メラノーマ奏効率20%・進行までの期間中央値56日、肥満細胞腫 奏効率46%・進行中央値未到達）。重篤な有害事象（アナフィラキシー・低血圧・腫瘍出血）が5.9% — このため各点滴の15-30分前のジフェンヒドラミン 2 mg/kg IM 前投薬と、点滴後1時間以上のモニタリングがMerck FAQで推奨される。偽性進行（縮小前の一過性増大）がありうるため、早期のサイズ増大のみで治療を中断しない。リンパ腫には非適応（単剤での有効性不十分）。メラノーマではOnceptワクチン、皮膚型MCTではステルフォンタ等との役割分担を腫瘍科医と検討。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not for use in cats — caninized antibody (anti-canine PD-1); no feline safety or efficacy data.",
                "dosage_ja": "猫には使用しない — 犬化抗体（犬PD-1特異的）であり、猫での安全性・有効性データは存在しない。",
                "notes": "A caninized mAb given to cats would be a foreign protein with sensitization/anaphylaxis risk and no expected target binding.",
                "notes_ja": "犬化抗体を猫に投与すると異種蛋白として感作・アナフィラキシーのリスクがあり、標的結合も期待できない。",
            },
        },
        "contraindications": "Do NOT use in dogs currently receiving glucocorticoids or other immunosuppressive medication (defeats PD-1 blockade and the label excludes concurrent use). Prior severe infusion reaction to gilvetmab. Use caution in dogs with pre-existing immune-mediated disease (checkpoint blockade can unmask/worsen it).",
        "contraindications_ja": "グルココルチコイドその他の免疫抑制薬を投与中の犬には使用しない（PD-1遮断の機序を打ち消し、ラベルも併用を除外）。本剤への重度のインフュージョンリアクション既往。免疫介在性疾患の既往犬では慎重に（チェックポイント遮断が顕在化・増悪させうる）。",
        "side_effects": [
            "Lethargy/fatigue (24% in melanoma dogs)",
            "Decreased appetite (16%)",
            "Vomiting (16%)",
            "Weight loss (16%)",
            "Serious: anaphylaxis, hypotension, tumor hemorrhage (5.9%)",
            "Immune-mediated adverse events (class effect)",
        ],
        "side_effects_ja": [
            "嗜眠・易疲労（メラノーマ犬で24%）",
            "食欲低下（16%）",
            "嘔吐（16%）",
            "体重減少（16%）",
            "重篤: アナフィラキシー・低血圧・腫瘍出血（5.9%）",
            "免疫介在性有害事象（クラス効果）",
        ],
        "drug_interactions": [
            {
                "drug": "Prednisolone / glucocorticoids",
                "effect": "Concurrent glucocorticoids suppress the T-cell response that gilvetmab works by restoring — label excludes concurrent immunosuppressive use.",
                "effect_ja": "グルココルチコイドの併用はギルベトマブが回復させるT細胞応答自体を抑制する — ラベルは免疫抑制薬の併用を除外。",
                "severity": "major",
            },
            {
                "drug": "Cyclosporine / other immunosuppressants",
                "effect": "Same mechanism conflict — checkpoint blockade requires a functional T-cell compartment.",
                "effect_ja": "同じ機序的矛盾 — チェックポイント遮断は機能するT細胞が前提。",
                "severity": "major",
            },
        ],
        "references": [
            "Gilvetmab US conditional license label / FAQ (Merck Animal Health)",
            "Efficacy and safety evaluation of gilvetmab in dogs with melanoma and mast cell tumor. J Vet Intern Med 2026 (PMID 42247661)",
            "AAHA Oncology Guidelines for Dogs and Cats 2026 — immunotherapy section",
        ],
    },
]
