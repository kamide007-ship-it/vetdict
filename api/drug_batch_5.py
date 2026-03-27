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
    "cyclosporine": {
        "rabbit": {
            "safe": True,
            "dosage": "1-2 mg/kg PO q12-24h",
            "dosage_ja": "1-2 mg/kg 経口 12-24時間毎",
            "notes": "For immune-mediated conditions; limited data",
            "notes_ja": "免疫介在性疾患に。データ限定的",
        },
        "guinea_pig": {
            "safe": True,
            "dosage": "1-2 mg/kg PO q12h",
            "dosage_ja": "1-2 mg/kg 経口 12時間毎",
            "notes": "Off-label for immune-mediated disease",
            "notes_ja": "免疫介在性疾患に適応外使用",
        },
        "ferret": {
            "safe": True,
            "dosage": "1-2 mg/kg PO q12h",
            "dosage_ja": "1-2 mg/kg 経口 12時間毎",
            "notes": "For immune-mediated conditions",
            "notes_ja": "免疫介在性疾患に",
        },
    },
    "phenobarbital": {
        "rabbit": {
            "safe": True,
            "dosage": "1-2 mg/kg PO q12h",
            "dosage_ja": "1-2 mg/kg 経口 12時間毎",
            "notes": "For seizure management; monitor liver values",
            "notes_ja": "痙攣管理に。肝機能値をモニタリング",
        },
        "ferret": {
            "safe": True,
            "dosage": "1-2 mg/kg PO q12h",
            "dosage_ja": "1-2 mg/kg 経口 12時間毎",
            "notes": "For seizures; less common in ferrets",
            "notes_ja": "痙攣に。フェレットではまれ",
        },
        "guinea_pig": {
            "safe": True,
            "dosage": "1-2 mg/kg PO q12h",
            "dosage_ja": "1-2 mg/kg 経口 12時間毎",
            "notes": "For seizure disorders; limited data",
            "notes_ja": "痙攣性疾患に。データ限定的",
        },
    },
    "levothyroxine": {
        "rabbit": {
            "safe": True,
            "dosage": "Not commonly needed",
            "dosage_ja": "通常は不要",
            "notes": "Hypothyroidism is rare in rabbits",
            "notes_ja": "ウサギでは甲状腺機能低下症はまれ",
        },
        "ferret": {
            "safe": True,
            "dosage": "50-100 mcg/ferret PO q12-24h",
            "dosage_ja": "50-100 mcg/匹 経口 12-24時間毎",
            "notes": "For hypothyroidism (rare in ferrets)",
            "notes_ja": "甲状腺機能低下症に（フェレットではまれ）",
        },
    },
    "atenolol": {
        "rabbit": {
            "safe": True,
            "dosage": "0.5-2 mg/kg PO q12-24h",
            "dosage_ja": "0.5-2 mg/kg 経口 12-24時間毎",
            "notes": "For tachyarrhythmias; limited data",
            "notes_ja": "頻脈性不整脈に。データ限定的",
        },
        "guinea_pig": {
            "safe": True,
            "dosage": "0.5-2 mg/kg PO q12-24h",
            "dosage_ja": "0.5-2 mg/kg 経口 12-24時間毎",
            "notes": "For tachyarrhythmias",
            "notes_ja": "頻脈性不整脈に",
        },
    },
    "spironolactone": {
        "rabbit": {
            "safe": True,
            "dosage": "1-2 mg/kg PO q12h",
            "dosage_ja": "1-2 mg/kg 経口 12時間毎",
            "notes": "For heart failure adjunct; potassium-sparing diuretic",
            "notes_ja": "心不全の補助療法。カリウム保持性利尿薬",
        },
        "guinea_pig": {
            "safe": True,
            "dosage": "1-2 mg/kg PO q12h",
            "dosage_ja": "1-2 mg/kg 経口 12時間毎",
            "notes": "For cardiac disease adjunct",
            "notes_ja": "心疾患の補助療法",
        },
    },
    "cefovecin": {
        "guinea_pig": {
            "safe": False,
            "dosage": "N/A",
            "dosage_ja": "使用不可",
            "notes": "Injectable cephalosporin — risk of dysbiosis in guinea pigs",
            "notes_ja": "注射用セファロスポリン — モルモットでは腸内細菌叢破壊のリスク",
        },
        "ferret": {
            "safe": True,
            "dosage": "8 mg/kg SC once (lasts 14 days)",
            "dosage_ja": "8 mg/kg 皮下 1回（14日間持続）",
            "notes": "Long-acting injectable; useful for compliance issues",
            "notes_ja": "長時間作用型注射薬。コンプライアンス問題に有用",
        },
        "bird": {
            "safe": True,
            "dosage": "10 mg/kg SC/IM (duration varies by species)",
            "dosage_ja": "10 mg/kg 皮下/筋注（持続時間は種により異なる）",
            "notes": "Off-label; limited pharmacokinetic data in avians",
            "notes_ja": "適応外使用。鳥類での薬物動態データは限定的",
        },
    },
    "budesonide": {
        "ferret": {
            "safe": True,
            "dosage": "0.5-1 mg/ferret PO q24h",
            "dosage_ja": "0.5-1 mg/匹 経口 24時間毎",
            "notes": "For IBD; locally-acting corticosteroid with less systemic effect",
            "notes_ja": "IBDに。全身作用の少ない局所作用型コルチコステロイド",
        },
    },
    "same": {
        "ferret": {
            "safe": True,
            "dosage": "30-50 mg/ferret PO q24h on empty stomach",
            "dosage_ja": "30-50 mg/匹 経口 24時間毎 空腹時",
            "notes": "Hepatoprotective supplement; for liver disease",
            "notes_ja": "肝保護サプリメント。肝疾患に",
        },
        "horse": {
            "safe": True,
            "dosage": "10-20 mg/kg PO q24h",
            "dosage_ja": "10-20 mg/kg 経口 24時間毎",
            "notes": "For hepatic support",
            "notes_ja": "肝臓サポートに",
        },
    },
    "glucosamine": {
        "rabbit": {
            "safe": True,
            "dosage": "20 mg/kg PO q24h",
            "dosage_ja": "20 mg/kg 経口 24時間毎",
            "notes": "For articular cartilage support; limited evidence",
            "notes_ja": "関節軟骨サポートに。エビデンス限定的",
        },
        "ferret": {
            "safe": True,
            "dosage": "25 mg/ferret PO q24h",
            "dosage_ja": "25 mg/匹 経口 24時間毎",
            "notes": "Joint supplement; limited data",
            "notes_ja": "関節サプリメント。データ限定的",
        },
    },
    "doxycycline": {
        "hedgehog": {
            "safe": True,
            "dosage": "5-10 mg/kg PO q12h",
            "dosage_ja": "5-10 mg/kg 経口 12時間毎",
            "notes": "Broad-spectrum tetracycline; well tolerated in hedgehogs",
            "notes_ja": "広域スペクトルテトラサイクリン。ハリネズミに忍容性良好",
        },
        "sugar_glider": {
            "safe": True,
            "dosage": "2.5-5 mg/kg PO q12h",
            "dosage_ja": "2.5-5 mg/kg 経口 12時間毎",
            "notes": "For respiratory and soft tissue infections",
            "notes_ja": "呼吸器・軟部組織感染症に",
        },
        "chinchilla": {
            "safe": True,
            "dosage": "5-10 mg/kg PO q12h",
            "dosage_ja": "5-10 mg/kg 経口 12時間毎",
            "notes": "Good for respiratory infections; safe for hindgut fermenters",
            "notes_ja": "呼吸器感染症に有効。後腸発酵動物に安全",
        },
    },
    "amoxicillin_clavulanate": {
        "hedgehog": {
            "safe": True,
            "dosage": "12.5-25 mg/kg PO q12h",
            "dosage_ja": "12.5-25 mg/kg 経口 12時間毎",
            "notes": "Broad-spectrum; first-line for many infections in hedgehogs",
            "notes_ja": "広域スペクトル。ハリネズミの多くの感染症に第一選択",
        },
        "sugar_glider": {
            "safe": True,
            "dosage": "12.5-25 mg/kg PO q12h",
            "dosage_ja": "12.5-25 mg/kg 経口 12時間毎",
            "notes": "First-line broad-spectrum antibiotic",
            "notes_ja": "第一選択の広域スペクトル抗菌薬",
        },
    },
    "selamectin": {
        "hedgehog": {
            "safe": True,
            "dosage": "6-18 mg/kg topical once, repeat in 2-4 weeks",
            "dosage_ja": "6-18 mg/kg 外用 1回、2-4週後に繰返し",
            "notes": "Alternative to ivermectin for mites; easier application (Revolution/Stronghold)",
            "notes_ja": "ダニに対するイベルメクチンの代替。塗布が容易（レボリューション/ストロングホールド）",
        },
        "sugar_glider": {
            "safe": True,
            "dosage": "6 mg/kg topical once, repeat in 30 days",
            "dosage_ja": "6 mg/kg 外用 1回、30日後に繰返し",
            "notes": "For external parasites",
            "notes_ja": "外部寄生虫に",
        },
        "chinchilla": {
            "safe": True,
            "dosage": "6-18 mg/kg topical once, repeat in 30 days",
            "dosage_ja": "6-18 mg/kg 外用 1回、30日後に繰返し",
            "notes": "For fur mites; safe topical option",
            "notes_ja": "毛皮ダニに。安全な外用の選択肢",
        },
    },
    # ------------------------------------------------------------------
    # Pradofloxacin – expand beyond dog/cat
    # ------------------------------------------------------------------
    "pradofloxacin": {
        "rabbit": {
            "safe": True,
            "dosage": "5-7.5 mg/kg PO q24h",
            "dosage_ja": "5-7.5 mg/kg 経口 24時間毎",
            "notes": "Broad-spectrum fluoroquinolone; useful for Pasteurella and anaerobic infections",
            "notes_ja": "広域フルオロキノロン。パスツレラや嫌気性菌感染に有用",
        },
        "ferret": {
            "safe": True,
            "dosage": "5-7.5 mg/kg PO q24h",
            "dosage_ja": "5-7.5 mg/kg 経口 24時間毎",
            "notes": "Good oral bioavailability; covers atypicals",
            "notes_ja": "良好な経口吸収率。非定型菌にも有効",
        },
        "reptile": {
            "safe": True,
            "dosage": "5 mg/kg PO q24h",
            "dosage_ja": "5 mg/kg 経口 24時間毎",
            "notes": "Adjust interval in cold environments; good gram-negative activity",
            "notes_ja": "低温環境では投与間隔を調整。グラム陰性菌に良好な活性",
        },
    },
    # ------------------------------------------------------------------
    # Robenacoxib – expand beyond dog/cat
    # ------------------------------------------------------------------
    "robenacoxib": {
        "rabbit": {
            "safe": True,
            "dosage": "1-2 mg/kg SC/PO q24h (short-term)",
            "dosage_ja": "1-2 mg/kg 皮下/経口 24時間毎（短期使用）",
            "notes": "COX-2 selective NSAID; limited data in rabbits, use short-term perioperatively",
            "notes_ja": "COX-2選択的NSAID。ウサギでのデータ限定、周術期短期使用",
        },
        "guinea_pig": {
            "safe": True,
            "dosage": "1-2 mg/kg SC q24h (short-term)",
            "dosage_ja": "1-2 mg/kg 皮下 24時間毎（短期使用）",
            "notes": "COX-2 selectivity may reduce GI risk; perioperative analgesia",
            "notes_ja": "COX-2選択性によりGIリスク軽減の可能性。周術期鎮痛",
        },
    },
    # ------------------------------------------------------------------
    # Methimazole – expand beyond cat/dog
    # ------------------------------------------------------------------
    "methimazole": {
        "ferret": {
            "safe": True,
            "dosage": "0.5-1 mg/ferret PO q12h",
            "dosage_ja": "0.5-1 mg/匹 経口 12時間毎",
            "notes": "Rare thyroid disease in ferrets; start low and titrate based on T4",
            "notes_ja": "フェレットの甲状腺疾患は稀。低用量から開始しT4でモニター",
        },
        "guinea_pig": {
            "safe": True,
            "dosage": "1-2.5 mg/kg PO q12h",
            "dosage_ja": "1-2.5 mg/kg 経口 12時間毎",
            "notes": "Limited reports of hyperthyroidism; dose extrapolated from cat",
            "notes_ja": "甲状腺機能亢進症の報告は限定的。猫からの用量外挿",
        },
    },
    # ------------------------------------------------------------------
    # Trilostane – expand beyond dog/ferret
    # ------------------------------------------------------------------
    "trilostane": {
        "horse": {
            "safe": True,
            "dosage": "0.5-1 mg/kg PO q24h",
            "dosage_ja": "0.5-1 mg/kg 経口 24時間毎",
            "notes": "For pituitary pars intermedia dysfunction (PPID/Cushing's); monitor ACTH",
            "notes_ja": "下垂体中間部機能障害（PPID/クッシング）に。ACTHをモニター",
        },
        "cat": {
            "safe": True,
            "dosage": "1-2 mg/kg PO q24h",
            "dosage_ja": "1-2 mg/kg 経口 24時間毎",
            "notes": "Feline hyperadrenocorticism is rare; monitor electrolytes closely",
            "notes_ja": "猫の副腎皮質機能亢進症は稀。電解質を厳密にモニター",
        },
    },
    # ------------------------------------------------------------------
    # Chlorambucil – expand beyond dog/cat
    # ------------------------------------------------------------------
    "chlorambucil": {
        "ferret": {
            "safe": True,
            "dosage": "2 mg/ferret PO q48-72h",
            "dosage_ja": "2 mg/匹 経口 48-72時間毎",
            "notes": "For lymphoma; combine with prednisolone. Monitor CBC closely",
            "notes_ja": "リンパ腫に。プレドニゾロンと併用。CBC厳密にモニター",
        },
        "rabbit": {
            "safe": True,
            "dosage": "2 mg/rabbit PO q48h",
            "dosage_ja": "2 mg/匹 経口 48時間毎",
            "notes": "For thymoma and lymphoma; use with corticosteroids",
            "notes_ja": "胸腺腫・リンパ腫に。コルチコステロイドと併用",
        },
    },
    # ------------------------------------------------------------------
    # Amphotericin B – expand beyond dog/cat/bird
    # ------------------------------------------------------------------
    "amphotericin_b": {
        "horse": {
            "safe": True,
            "dosage": "0.3-0.5 mg/kg IV q48h (cumulative dose ≤6 mg/kg)",
            "dosage_ja": "0.3-0.5 mg/kg 静注 48時間毎（累積投与量 ≤6 mg/kg）",
            "notes": "For systemic mycoses; highly nephrotoxic, pre-hydrate with saline. Monitor BUN/creatinine",
            "notes_ja": "全身性真菌症に。腎毒性が高く生理食塩水で前水和。BUN/クレアチニンをモニター",
        },
        "reptile": {
            "safe": True,
            "dosage": "1 mg/kg IT/ICe q24h for 14-28 days, or 1 mg/kg SC diluted q72h",
            "dosage_ja": "1 mg/kg 気管内/体腔内 24時間毎 14-28日、または1 mg/kg 皮下希釈 72時間毎",
            "notes": "For systemic fungal infections; less nephrotoxic in reptiles but monitor closely",
            "notes_ja": "全身性真菌症に。爬虫類では腎毒性が低いが慎重にモニター",
        },
        "ferret": {
            "safe": True,
            "dosage": "0.15-0.5 mg/kg IV q24-48h (cumulative ≤7-25 mg)",
            "dosage_ja": "0.15-0.5 mg/kg 静注 24-48時間毎（累積 ≤7-25 mg）",
            "notes": "For systemic mycoses (blastomycosis, histoplasmosis). Pre-hydrate; stop if azotemia develops",
            "notes_ja": "全身性真菌症に。前水和。高窒素血症が出たら中止",
        },
    },
    # ------------------------------------------------------------------
    # Phenylbutazone – expand beyond horse/dog/cat
    # ------------------------------------------------------------------
    "phenylbutazone": {
        "rabbit": {
            "safe": True,
            "dosage": "10-20 mg/kg PO q8-12h (short-term only)",
            "dosage_ja": "10-20 mg/kg 経口 8-12時間毎（短期使用のみ）",
            "notes": "Non-selective NSAID; use only short-term. Risk of GI ulceration",
            "notes_ja": "非選択的NSAID。短期使用のみ。消化管潰瘍のリスクあり",
        },
        "guinea_pig": {
            "safe": True,
            "dosage": "10-20 mg/kg PO q12h",
            "dosage_ja": "10-20 mg/kg 経口 12時間毎",
            "notes": "Short-term analgesic; GI risk with prolonged use",
            "notes_ja": "短期鎮痛薬。長期使用では消化管リスクあり",
        },
    },
    # ------------------------------------------------------------------
    # Flunixin meglumine – expand beyond horse/dog/cat
    # ------------------------------------------------------------------
    "flunixin": {
        "rabbit": {
            "safe": True,
            "dosage": "1.1 mg/kg SC/IM q12-24h (1-3 days max)",
            "dosage_ja": "1.1 mg/kg 皮下/筋注 12-24時間毎（最大1-3日）",
            "notes": "Potent NSAID for visceral pain; limit to 3 days to avoid GI/renal toxicity",
            "notes_ja": "内臓痛に有効なNSAID。GI/腎毒性回避のため3日以内に制限",
        },
        "bird": {
            "safe": True,
            "dosage": "1-10 mg/kg IM q12-24h",
            "dosage_ja": "1-10 mg/kg 筋注 12-24時間毎",
            "notes": "Wide dose range across avian species; effective for visceral and musculoskeletal pain",
            "notes_ja": "鳥種により用量範囲が広い。内臓・筋骨格系痛に有効",
        },
        "reptile": {
            "safe": True,
            "dosage": "0.1-0.5 mg/kg IM q24-48h",
            "dosage_ja": "0.1-0.5 mg/kg 筋注 24-48時間毎",
            "notes": "Limited PK data; adjust interval based on ambient temperature",
            "notes_ja": "薬物動態データ限定。環境温度に応じて投与間隔を調整",
        },
        "ferret": {
            "safe": True,
            "dosage": "0.5-2 mg/kg SC/IM q12-24h (short-term)",
            "dosage_ja": "0.5-2 mg/kg 皮下/筋注 12-24時間毎（短期使用）",
            "notes": "For acute pain/inflammation; avoid prolonged use",
            "notes_ja": "急性疼痛・炎症に。長期使用は避ける",
        },
    },
    # ------------------------------------------------------------------
    # Oclacitinib – expand beyond dog/cat (limited evidence)
    # ------------------------------------------------------------------
    "oclacitinib": {
        "ferret": {
            "safe": True,
            "dosage": "0.4-0.6 mg/kg PO q12h x14d then q24h",
            "dosage_ja": "0.4-0.6 mg/kg 経口 12時間毎×14日後、24時間毎",
            "notes": "JAK inhibitor; anecdotal use for pruritic dermatitis in ferrets. Monitor CBC",
            "notes_ja": "JAK阻害薬。フェレットの瘙痒性皮膚炎に経験的使用。CBCモニター",
        },
    },
}
