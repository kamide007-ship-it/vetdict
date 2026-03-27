"""Drug batch 5 – Latest veterinary drugs (2023-2025).

Adds recent monoclonal antibodies, novel NSAIDs, appetite stimulants,
and other modern veterinary therapeutics with species-specific dosing.

References:
  - Plumb's Veterinary Drug Handbook, 10th ed.
  - BSAVA Small Animal Formulary, 10th ed.
  - Carpenter's Exotic Animal Formulary, 6th ed.
  - EMA/FDA product approval documents
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# New drugs (not in main dictionary or batches 1-4)
# ---------------------------------------------------------------------------
DRUGS_BATCH_5: list[dict] = [
    # ------------------------------------------------------------------
    # Erythropoiesis-stimulating agent
    # ------------------------------------------------------------------
    {
        "id": "darbepoetin",
        "name": "Darbepoetin Alfa (Aranesp)",
        "name_ja": "ダルベポエチンアルファ（アラネスプ）",
        "category": "endocrine",
        "mechanism": "Long-acting erythropoiesis-stimulating agent. Hyperglycosylated analog of erythropoietin with extended half-life. Lower immunogenicity than rHuEPO.",
        "mechanism_ja": "長時間作用型赤血球造血刺激薬。エリスロポエチンの超糖鎖付加アナログで半減期が延長。rHuEPOより免疫原性が低い。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "0.45-1.0 mcg/kg SC q1-3wk",
                "dosage_ja": "0.45-1.0 mcg/kg 皮下 1-3週毎",
                "notes": "Preferred over rHuEPO in cats — lower anti-drug antibody risk. For CKD non-regenerative anemia (PCV < 20%). Supplement iron. Monitor PCV weekly initially.",
                "notes_ja": "猫ではrHuEPOより好まれる — 抗薬物抗体リスクが低い。CKD非再生性貧血(PCV<20%)に。鉄を補充。初期は毎週PCV確認。",
            },
            "dog": {
                "safe": True,
                "dosage": "0.45-1.0 mcg/kg SC q1-3wk",
                "dosage_ja": "0.45-1.0 mcg/kg 皮下 1-3週毎",
                "notes": "Lower antibody formation risk than epoetin. For CKD anemia. Supplement iron. Target PCV 30-40%.",
                "notes_ja": "エポエチンより抗体形成リスクが低い。CKD貧血に。鉄を補充。目標PCV 30-40%。",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.45-1.0 mcg/kg SC q1-2wk",
                "dosage_ja": "0.45-1.0 mcg/kg 皮下 1-2週毎",
                "notes": "For aplastic anemia (estrogen toxicity in intact females)",
                "notes_ja": "再生不良性貧血（未避妊メスのエストロゲン中毒）に",
            },
        },
        "side_effects": ["hypertension", "iron deficiency", "anti-drug antibody formation (rare)", "pure red cell aplasia (rare)", "seizures"],
        "side_effects_ja": ["高血圧", "鉄欠乏", "抗薬物抗体形成（まれ）", "純赤芽球無形成症（まれ）", "痙攣"],
        "contraindications": "Uncontrolled hypertension. Adequate iron stores required before starting. Hypersensitivity.",
        "contraindications_ja": "コントロールされていない高血圧。開始前に十分な鉄貯蔵が必要。過敏症。",
    },
    # ------------------------------------------------------------------
    # Novel isoxazoline (cats)
    # ------------------------------------------------------------------
    {
        "id": "esafoxolaner",
        "name": "Esafoxolaner (NexGard Combo)",
        "name_ja": "エサフォキソラネル（ネクスガードコンボ）",
        "category": "antiparasitics",
        "mechanism": "Purified (S)-enantiomer of afoxolaner; isoxazoline ectoparasiticide. Combined with eprinomectin + praziquantel for broad-spectrum feline parasite protection.",
        "mechanism_ja": "アフォキソラネルの精製(S)-エナンチオマー。イソキサゾリン系外部寄生虫駆除薬。エプリノメクチン+プラジカンテルとの合剤で猫の広域寄生虫防御。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "1.44 mg/kg topical once monthly (spot-on)",
                "dosage_ja": "1.44 mg/kg 外用 月1回（スポットオン）",
                "notes": "EMA/FDA approved all-in-one for cats: fleas, ticks, heartworm, roundworms, hookworms, tapeworms. First isoxazoline spot-on for cats.",
                "notes_ja": "猫用オールインワンEMA/FDA承認：ノミ、マダニ、犬糸状虫、回虫、鉤虫、条虫。猫初のイソキサゾリン系スポットオン。",
            },
            "dog": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Cat-specific formulation; use NexGard for dogs",
                "notes_ja": "猫専用製剤。犬にはネクスガードを使用",
            },
        },
        "side_effects": ["skin irritation at application site", "vomiting", "diarrhea", "lethargy"],
        "side_effects_ja": ["塗布部位の皮膚刺激", "嘔吐", "下痢", "嗜眠"],
        "contraindications": "Cats < 8 weeks or < 0.8 kg. Not for dogs or rabbits.",
        "contraindications_ja": "8週齢未満または0.8kg未満の猫。犬やウサギには使用不可。",
    },
    # ------------------------------------------------------------------
    # Sedation combination
    # ------------------------------------------------------------------
    {
        "id": "medetomidine_vatinoxan",
        "name": "Medetomidine + Vatinoxan (Zenalpha)",
        "name_ja": "メデトミジン＋バチノキサン（ゼナルファ）",
        "category": "sedatives",
        "mechanism": "Medetomidine: alpha-2 adrenergic agonist (sedation/analgesia). Vatinoxan: peripheral alpha-2 antagonist that blocks cardiovascular side effects while preserving central sedation.",
        "mechanism_ja": "メデトミジン：α2アドレナリン作動薬（鎮静/鎮痛）。バチノキサン：末梢α2拮抗薬で心血管系副作用を遮断し中枢性鎮静は維持する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.01-0.04 mg/kg medetomidine + 0.1-0.4 mg/kg vatinoxan IM",
                "dosage_ja": "メデトミジン 0.01-0.04 mg/kg + バチノキサン 0.1-0.4 mg/kg 筋注",
                "notes": "FDA approved 2023. Maintains sedation quality with significantly less bradycardia, hypertension, and pale mucous membranes vs medetomidine alone.",
                "notes_ja": "2023年FDA承認。メデトミジン単独と比較して鎮静の質を維持しつつ徐脈・高血圧・粘膜蒼白を大幅に軽減。",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Currently approved for dogs only",
                "notes_ja": "現在は犬のみに承認",
            },
        },
        "side_effects": ["sedation (intended)", "bradycardia (reduced vs medetomidine alone)", "hypothermia", "emesis"],
        "side_effects_ja": ["鎮静（意図的作用）", "徐脈（メデトミジン単独より軽減）", "低体温", "催吐"],
        "contraindications": "Severe cardiovascular disease. Hepatic/renal impairment. Not for cats (unapproved).",
        "contraindications_ja": "重度の心血管疾患。肝/腎障害。猫には未承認。",
    },
]
# ---------------------------------------------------------------------------
# Species-specific dosage patches for existing drugs (batch 5)
# ---------------------------------------------------------------------------
SPECIES_INFO_PATCH_5: dict[str, dict[str, dict]] = {
    "meloxicam": {
        "hedgehog": {
            "safe": True,
            "dosage": "0.2 mg/kg PO/SC q24h",
            "dosage_ja": "0.2 mg/kg 経口/皮下 24時間毎",
            "notes": "NSAID of choice for hedgehogs; monitor for GI ulceration",
            "notes_ja": "ハリネズミに第一選択のNSAID。消化管潰瘍に注意",
        },
        "chinchilla": {
            "safe": True,
            "dosage": "0.1-0.2 mg/kg PO/SC q24h",
            "dosage_ja": "0.1-0.2 mg/kg 経口/皮下 24時間毎",
            "notes": "Use with caution; monitor for GI signs",
            "notes_ja": "慎重に使用。消化管症状に注意",
        },
        "sugar_glider": {
            "safe": True,
            "dosage": "0.1-0.2 mg/kg PO/SC q24h",
            "dosage_ja": "0.1-0.2 mg/kg 経口/皮下 24時間毎",
            "notes": "Short courses preferred",
            "notes_ja": "短期間の使用が望ましい",
        },
    },
    "tramadol": {
        "hedgehog": {
            "safe": True,
            "dosage": "5-10 mg/kg PO q8-12h",
            "dosage_ja": "5-10 mg/kg 経口 8-12時間毎",
            "notes": "For moderate pain; may cause sedation",
            "notes_ja": "中等度の疼痛に。鎮静を起こす可能性",
        },
        "guinea_pig": {
            "safe": True,
            "dosage": "5 mg/kg PO q12h",
            "dosage_ja": "5 mg/kg 経口 12時間毎",
            "notes": "Adjunctive analgesic; combine with NSAID for better effect",
            "notes_ja": "補助的鎮痛薬。NSAIDとの併用でより効果的",
        },
        "chinchilla": {
            "safe": True,
            "dosage": "5-10 mg/kg PO q12h",
            "dosage_ja": "5-10 mg/kg 経口 12時間毎",
            "notes": "For moderate pain",
            "notes_ja": "中等度の疼痛に",
        },
    },
    "gabapentin": {
        "hedgehog": {
            "safe": True,
            "dosage": "5 mg/kg PO q8-12h",
            "dosage_ja": "5 mg/kg 経口 8-12時間毎",
            "notes": "For neuropathic pain and WHS-related pain",
            "notes_ja": "神経障害性疼痛・WHS関連疼痛に",
        },
        "guinea_pig": {
            "safe": True,
            "dosage": "5-10 mg/kg PO q12h",
            "dosage_ja": "5-10 mg/kg 経口 12時間毎",
            "notes": "For neuropathic and chronic pain; may cause sedation",
            "notes_ja": "神経障害性疼痛・慢性疼痛に。鎮静を起こす可能性",
        },
        "chinchilla": {
            "safe": True,
            "dosage": "3-5 mg/kg PO q8-12h",
            "dosage_ja": "3-5 mg/kg 経口 8-12時間毎",
            "notes": "For neuropathic pain",
            "notes_ja": "神経障害性疼痛に",
        },
    },
    "furosemide": {
        "guinea_pig": {
            "safe": True,
            "dosage": "1-4 mg/kg PO/SC/IM q12h",
            "dosage_ja": "1-4 mg/kg 経口/皮下/筋注 12時間毎",
            "notes": "For pulmonary edema and heart failure",
            "notes_ja": "肺水腫・心不全に",
        },
        "hedgehog": {
            "safe": True,
            "dosage": "1-4 mg/kg PO/SC q12h",
            "dosage_ja": "1-4 mg/kg 経口/皮下 12時間毎",
            "notes": "For congestive heart failure; monitor hydration",
            "notes_ja": "うっ血性心不全に。水和状態をモニタリング",
        },
        "chinchilla": {
            "safe": True,
            "dosage": "1-4 mg/kg PO/SC/IM q12h",
            "dosage_ja": "1-4 mg/kg 経口/皮下/筋注 12時間毎",
            "notes": "For fluid overload",
            "notes_ja": "体液過剰に",
        },
    },
    "pimobendan": {
        "ferret": {
            "safe": True,
            "dosage": "0.5 mg/kg PO q12h",
            "dosage_ja": "0.5 mg/kg 経口 12時間毎",
            "notes": "For dilated cardiomyopathy; very common in ferrets",
            "notes_ja": "拡張型心筋症に。フェレットでは非常に一般的",
        },
        "hedgehog": {
            "safe": True,
            "dosage": "0.25-0.5 mg/kg PO q12h",
            "dosage_ja": "0.25-0.5 mg/kg 経口 12時間毎",
            "notes": "For DCM and heart failure; limited data",
            "notes_ja": "DCM・心不全に。データ限定的",
        },
    },
    "prednisolone": {
        "sugar_glider": {
            "safe": True,
            "dosage": "0.5-2 mg/kg PO q12-24h",
            "dosage_ja": "0.5-2 mg/kg 経口 12-24時間毎",
            "notes": "For inflammatory conditions; taper dose",
            "notes_ja": "炎症性疾患に。漸減投与",
        },
        "hedgehog": {
            "safe": True,
            "dosage": "0.5-2 mg/kg PO q12-24h",
            "dosage_ja": "0.5-2 mg/kg 経口 12-24時間毎",
            "notes": "For inflammatory/immune conditions; taper",
            "notes_ja": "炎症性/免疫性疾患に。漸減投与",
        },
    },
    "enrofloxacin": {
        "hedgehog": {
            "safe": True,
            "dosage": "5-10 mg/kg PO/SC q12h",
            "dosage_ja": "5-10 mg/kg 経口/皮下 12時間毎",
            "notes": "Broad-spectrum fluoroquinolone; avoid in young growing animals",
            "notes_ja": "広域スペクトルフルオロキノロン。成長期の若齢個体は避ける",
        },
        "sugar_glider": {
            "safe": True,
            "dosage": "5 mg/kg PO/IM q12h",
            "dosage_ja": "5 mg/kg 経口/筋注 12時間毎",
            "notes": "Fluoroquinolone; avoid in young animals",
            "notes_ja": "フルオロキノロン。若齢個体は避ける",
        },
        "chinchilla": {
            "safe": True,
            "dosage": "5-10 mg/kg PO/SC q12h",
            "dosage_ja": "5-10 mg/kg 経口/皮下 12時間毎",
            "notes": "Good for respiratory and urinary infections",
            "notes_ja": "呼吸器・尿路感染症に有効",
        },
    },
    "metronidazole": {
        "hedgehog": {
            "safe": True,
            "dosage": "20 mg/kg PO q12h",
            "dosage_ja": "20 mg/kg 経口 12時間毎",
            "notes": "For anaerobic infections and protozoal disease",
            "notes_ja": "嫌気性菌感染・原虫性疾患に",
        },
        "chinchilla": {
            "safe": True,
            "dosage": "20 mg/kg PO q12h",
            "dosage_ja": "20 mg/kg 経口 12時間毎",
            "notes": "For Giardia and anaerobic infections",
            "notes_ja": "ジアルジア・嫌気性菌感染に",
        },
        "sugar_glider": {
            "safe": True,
            "dosage": "25 mg/kg PO q12h",
            "dosage_ja": "25 mg/kg 経口 12時間毎",
            "notes": "For protozoal and anaerobic infections",
            "notes_ja": "原虫性・嫌気性菌感染に",
        },
    },
    "ivermectin": {
        "hedgehog": {
            "safe": True,
            "dosage": "0.2-0.4 mg/kg SC q10-14d (repeat 3x)",
            "dosage_ja": "0.2-0.4 mg/kg 皮下 10-14日毎（3回繰返し）",
            "notes": "For Caparinia mites (very common in hedgehogs); standard of care",
            "notes_ja": "カパリニアダニに（ハリネズミで非常に一般的）。標準治療",
        },
        "sugar_glider": {
            "safe": True,
            "dosage": "0.2 mg/kg SC/PO q14d",
            "dosage_ja": "0.2 mg/kg 皮下/経口 14日毎",
            "notes": "For external parasites",
            "notes_ja": "外部寄生虫に",
        },
    },
}
