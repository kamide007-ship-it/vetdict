"""Drug batch 56 – referenced-but-absent agent surfaced by the 2026-09 audit (22nd sweep).

The dose-context token audit (treatment texts cross-checked against
find_drugs_in_text) found the matcher near-saturated; the single true
monograph gap was:

  - Propylene glycol — 14 disease entries prescribe it with explicit doses:
    the classic oral glucogenic for pregnancy toxemia / ketosis in rabbits
    ("1 mL PO q12h"), hamsters ("0.5-1 mL PO q12h"), guinea pigs
    ("1-2 mL PO q12h", pre-/post-partum entries), degus ("1 mL/kg PO q12h")
    and goats, plus the topical 50-75% keratolytic for canine sebaceous
    adenitis / nasal hyperkeratosis / distemper hardpad. The cat entries
    reference it only as a TOXIN (Heinz-body methemoglobinemia; paintball
    ingredient) — that species gate is the defining safety fact and belongs
    in the formulary (FDA banned propylene glycol in cat foods; Christopher
    et al. JAVMA 1989).

The same sweep found the medical-manuka-honey monograph (id=silver_honey)
unreachable from its 70+ wound-care references — fixed via search aliases in
drug_dictionary.py, not a duplicate entry.

References:
  - Quesenberry & Carpenter, Ferrets, Rabbits and Rodents 4th ed —
    pregnancy toxemia / ketosis management in rabbits and rodents.
  - Christopher MM et al. Propylene glycol ingestion causes D-lactic
    acidosis and Heinz body formation in cats. JAVMA 1989.
  - Plumb's Veterinary Drug Handbook 10th ed — propylene glycol (ruminant
    ketosis glucogenic).
  - Muller & Kirk's Small Animal Dermatology 7th ed — topical keratolytics
    (sebaceous adenitis skin-care protocols).
  - Pugh & Baird, Sheep and Goat Medicine 2nd ed — caprine pregnancy
    toxemia (propylene glycol 30-60 mL PO q12h).
"""

DRUGS_BATCH_56 = [
    {
        "id": "propylene_glycol",
        "search_aliases": [
            "プロピレングリコール",
            "propylene glycol",
            "グルコース前駆体",
        ],
        "name": "Propylene Glycol",
        "name_ja": "プロピレングリコール",
        "category": "endocrine",
        "mechanism": "Oral glucogenic precursor: absorbed intact and hepatically metabolised via lactaldehyde/lactate to pyruvate, feeding gluconeogenesis — raises blood glucose and suppresses ketogenesis in pregnancy toxemia / hepatic lipidosis-spectrum ketosis of rabbits, rodents and small ruminants. Topically a humectant/keratolytic (50-75% solution) that hydrates and loosens adherent scale in sebaceous adenitis and nasal/footpad hyperkeratosis.",
        "mechanism_ja": "経口グルコース前駆体: 吸収後に肝でラクトアルデヒド/乳酸を経てピルビン酸となり糖新生に入り、ウサギ・げっ歯類・小型反芻獣の妊娠中毒症/ケトーシスで血糖を上げケトン生成を抑制する。外用では保湿・角質溶解剤（50-75%溶液）として脂腺炎や鼻鏡・肉球の角化亢進で固着鱗屑を軟化させる。",
        "species_info": {
            "rabbit": {
                "safe": True,
                "dosage": "Pregnancy toxemia (adjunct): 1 mL PO q12h alongside the mainstays — IV dextrose, calcium gluconate as indicated, aggressive fluids and syringe feeding (Quesenberry & Carpenter 4th ed).",
                "dosage_ja": "妊娠中毒症（補助）: 1 mL PO q12h。主軸は静注ブドウ糖・（必要時）グルコン酸カルシウム・積極的輸液・強制給餌であり、その併用として（Quesenberry & Carpenter 4th ed）。",
                "notes": "Glucogenic adjunct only — never a substitute for dextrose IV and nutritional support in an anorexic doe.",
                "notes_ja": "糖新生の補助のみ — 食欲廃絶した雌の静注ブドウ糖・栄養サポートの代替にはならない。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Pregnancy toxemia (pre-/post-partum ketosis): 1-2 mL PO q12h (limited evidence — adjunct to IV dextrose, calcium and syringe feeding). Prevention (obesity control, late-gestation stress reduction) matters more than any drug.",
                "dosage_ja": "妊娠中毒症（分娩前後のケトーシス）: 1-2 mL PO q12h（エビデンス限定的 — 静注ブドウ糖・カルシウム・強制給餌の補助）。肥満回避・妊娠後期のストレス軽減という予防が薬物より重要。",
                "notes": "Mortality of established toxemia is high (50-80%) despite treatment — treat aggressively and early.",
                "notes_ja": "発症後の致死率は治療しても高い（50-80%）— 早期から積極的に治療する。",
            },
            "hamster": {
                "safe": True,
                "dosage": "Pregnancy toxemia: 0.5-1 mL PO q12h with syringe feeding + oral/parenteral glucose.",
                "dosage_ja": "妊娠中毒症: 0.5-1 mL PO q12h。強制給餌と経口/非経口ブドウ糖を併用。",
                "notes": "Obese late-gestation females are the at-risk group.",
                "notes_ja": "肥満の妊娠後期雌がリスク群。",
            },
            "degu": {
                "safe": True,
                "dosage": "Pregnancy toxemia: 1 mL/kg PO q12h (adjunct to 5% dextrose IV + calcium gluconate).",
                "dosage_ja": "妊娠中毒症: 1 mL/kg PO q12h（5%ブドウ糖静注＋グルコン酸カルシウムの補助）。",
                "notes": "Use sugar-free recovery diets for syringe feeding in this diabetes-prone species.",
                "notes_ja": "糖尿病になりやすい種のため、強制給餌には無糖の回復食を用いる。",
            },
            "dog": {
                "safe": True,
                "dosage": "Topical keratolytic: 50-75% aqueous solution sprayed/applied q12-24h (sebaceous adenitis, nasal hyperkeratosis, distemper hardpad), or 50:50 with mineral oil as a 2-4 h soak before medicated shampoo (Muller & Kirk 7th ed).",
                "dosage_ja": "外用角質溶解: 50-75%水溶液を q12-24h で塗布/スプレー（脂腺炎・鼻鏡角化症・ジステンパー硬蹠症）、または鉱物油と50:50で2-4時間浸漬後に薬用シャンプー（Muller & Kirk 7th ed）。",
                "notes": "Systemic glucogenic use is not standard in dogs; the referenced canine uses are topical.",
                "notes_ja": "犬では全身の糖新生目的の使用は標準的でなく、参照される犬の用途は外用。",
            },
            "cat": {
                "safe": False,
                "dosage": "Contraindicated — do not use orally or in repeated topical applications.",
                "dosage_ja": "禁忌 — 経口投与・反復外用とも使用しない。",
                "notes": "Cats are uniquely sensitive: propylene glycol causes oxidative erythrocyte injury with Heinz-body formation and reduced RBC survival (Christopher JAVMA 1989); the FDA banned it from cat foods. Paintballs (propylene glycol + salt) are a recognised feline toxicosis source.",
                "notes_ja": "猫は特異的に感受性が高い: プロピレングリコールは赤血球の酸化障害を起こしハインツ小体形成・赤血球寿命短縮を招く（Christopher JAVMA 1989）。FDAはキャットフードへの使用を禁止。ペイントボール（プロピレングリコール＋塩）は猫の中毒源として知られる。",
            },
            "exotic_other": {
                "safe": True,
                "dosage": "Goat pregnancy toxemia (ketosis): 30-60 mL PO q12h until appetite returns, with IV dextrose in recumbent does (Pugh & Baird, Sheep and Goat Medicine 2nd ed).",
                "dosage_ja": "ヤギ妊娠中毒症（ケトーシス）: 30-60 mL PO q12h を食欲回復まで。起立不能例は静注ブドウ糖を併用（Pugh & Baird, Sheep and Goat Medicine 2nd ed）。",
                "notes": "Overdose causes CNS depression and D-lactic acidosis — do not exceed recommended volumes.",
                "notes_ja": "過量はCNS抑制・D-乳酸アシドーシスを起こす — 推奨量を超えない。",
            },
        },
        "side_effects": "CNS depression, ataxia and D-lactic acidosis with overdose; osmotic diarrhea (oral); local irritation at high topical concentrations",
        "side_effects_ja": "過量でCNS抑制・失調・D-乳酸アシドーシス、経口で浸透圧性下痢、高濃度外用で局所刺激",
        "contraindications": "Cats (Heinz-body hemolytic anemia — FDA-banned in cat foods). Not a substitute for IV dextrose in collapsed/hypoglycemic patients.",
        "contraindications_ja": "猫（ハインツ小体性溶血性貧血 — FDAがキャットフードへの使用を禁止）。虚脱・低血糖例では静注ブドウ糖の代替にならない。",
        "drug_interactions": [
            {
                "drug": "Oxidant drugs in Heinz-body-prone species (e.g. acetaminophen, benzocaine)",
                "effect": "Additive oxidative erythrocyte injury — avoid combining, and avoid the drug entirely in cats",
                "effect_ja": "酸化的赤血球障害が相加 — 併用を避け、猫では本剤自体を使用しない",
                "severity": "moderate",
            },
        ],
    },
]
