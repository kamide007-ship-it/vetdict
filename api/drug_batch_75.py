"""Drug batch 75 – 2026-10 session: two licensed canine products absent from
the dictionary although the toxicology/orthopaedic content they belong to
was present.

1. Ropinirole ophthalmic solution (CLEVOR, Orion/Vetoquinol) — dopamine
   D2-agonist eye drops that induce emesis in dogs (EMA 2018; FDA 2020,
   NADA 141-534). Target dose 3.75 mg/m2 (label volume by body weight); a
   second dose may be given if the dog has not vomited within 15 minutes.
   Pivotal EU RCT: Suokko M et al. Vet Rec 2019 — 95% of dogs vomited
   within 30 minutes. A needle-free alternative to apomorphine for gastric
   decontamination when emesis is indicated.
2. Enflicoxib (DAXOCOX, Ecuphar/Animalcare) — once-weekly oral coxib for
   canine osteoarthritis pain (EMA 2021). Loading dose 8 mg/kg on day 0,
   then 4 mg/kg once weekly with food (Salichs M et al. Vet Rec 2022 —
   non-inferior to mavacoxib/meloxicam in a 6-week blinded RCT).

Neither is approved in Japan at the time of entry.
"""

DRUGS_BATCH_75 = [
    {
        "id": "ropinirole_ophthalmic",
        "search_aliases": ["クレボー", "Clevor", "CLEVOR", "ロピニロール", "ロピニロール点眼", "ropinirole"],
        "name": "Ropinirole Ophthalmic Solution (Clevor)",
        "name_ja": "ロピニロール点眼液（クレボー）",
        "category": "miscellaneous",
        "mechanism": "Full dopamine D2-receptor agonist absorbed through the conjunctiva and nasal mucosa; stimulates the chemoreceptor trigger zone to induce emesis, typically within 10-15 minutes.",
        "mechanism_ja": "ドパミンD2受容体の完全作動薬。結膜・鼻粘膜から吸収され化学受容器引き金帯（CTZ）を刺激し、通常10-15分で嘔吐を誘発する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Target 3.75 mg/m2 (labelled dose range 2.7-5.4 mg/m2) instilled as 30 mg/mL eye drops — the number of drops is read from the label weight table (dogs >= 4.5 months and >= 1.8 kg). If the dog has not vomited within 15 minutes, the same dose may be given once more (CLEVOR US label, FDA 2020; EU SPC 2018).",
                "dosage_ja": "目標3.75 mg/m²（ラベル用量範囲 2.7-5.4 mg/m²）を30 mg/mL点眼液で投与 — 滴数はラベルの体重表に従う（4.5ヶ月齢以上・1.8 kg以上）。15分以内に嘔吐しなければ同量をもう1回投与可（CLEVOR 米国ラベル FDA 2020年／EU SPC 2018年）。",
                "notes": "Indication: emesis induction when gastric decontamination is appropriate (e.g., recent chocolate, grape/raisin, xylitol or drug ingestion within ~1-2 h). Pivotal RCT: 95% vomited within 30 minutes (Suokko 2019 Vet Rec). Transient ocular hyperaemia and mild tachycardia are common; protracted vomiting can be stopped with a dopamine antagonist (metoclopramide) — maropitant pre-treatment would block the effect. Wear gloves; avoid skin/eye contact for the person dosing. Not approved in Japan — apomorphine remains the domestic option.",
                "notes_ja": "適応: 胃内除染が適切な場合の催吐（チョコレート・ブドウ/レーズン・キシリトール・薬物等の摂取後おおむね1-2時間以内）。ピボタルRCT: 30分以内に95%が嘔吐（Suokko 2019 Vet Rec）。一過性の結膜充血・軽度頻脈が多い。遷延性嘔吐はドパミン拮抗薬（メトクロプラミド）で止められる — マロピタントの前投与は催吐効果を阻害する。投与者は手袋を着用し皮膚・眼への接触を避ける。国内未承認 — 国内ではアポモルヒネが選択肢。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not licensed for cats — dopamine agonists are unreliable emetics in cats.",
                "dosage_ja": "猫には未承認 — ドパミン作動薬は猫で催吐効果が不確実。",
                "notes": "In cats use an alpha-2 agonist (dexmedetomidine) for emesis induction, reversed with atipamezole.",
                "notes_ja": "猫の催吐にはα2作動薬（デクスメデトミジン）を用い、アチパメゾールで拮抗する。",
            },
        },
        "contraindications": "Ingestion of corrosives (acids/alkalis), hydrocarbons/volatile substances or sharp objects; CNS depression, seizures, reduced gag reflex or any condition with aspiration risk (brachycephalic dyspnoea, laryngeal paralysis); hypoxia; dogs < 4.5 months or < 1.8 kg.",
        "contraindications_ja": "腐食性物質（酸・アルカリ）・炭化水素/揮発性物質・鋭利な異物の摂取。中枢抑制・痙攣・咽頭反射低下など誤嚥リスクのある状態（短頭種の呼吸困難・喉頭麻痺）。低酸素症。4.5ヶ月齢未満または1.8 kg未満の犬。",
        "side_effects": [
            "Transient ocular hyperaemia, blepharospasm, ocular discharge",
            "Mild tachycardia, lethargy",
            "Protracted vomiting (reversible with metoclopramide)",
        ],
        "side_effects_ja": [
            "一過性の結膜充血・眼瞼痙攣・眼脂",
            "軽度の頻脈・元気消失",
            "遷延性嘔吐（メトクロプラミドで拮抗可能）",
        ],
        "drug_interactions": [
            {
                "drug": "Maropitant / other antiemetics",
                "effect": "Prior antiemetic administration prevents the emetic response — do not pre-medicate when emesis is the goal.",
                "effect_ja": "制吐薬の前投与は催吐反応を阻害する — 催吐目的の場合は前投与しない。",
                "severity": "moderate",
            },
            {
                "drug": "Metoclopramide / dopamine antagonists",
                "effect": "Antagonises ropinirole — used intentionally to stop protracted vomiting.",
                "effect_ja": "ロピニロールに拮抗する — 遷延性嘔吐を止める目的で意図的に使用する。",
                "severity": "minor",
            },
        ],
        "references": [
            "CLEVOR (ropinirole ophthalmic solution) US label — FDA NADA 141-534 (2020); EMA EPAR Clevor (2018)",
            "Suokko M, et al. Ropinirole eye drops induce vomiting effectively in dogs: a randomised, double-blind, placebo-controlled clinical study. Vet Rec 2019.",
        ],
    },
    {
        "id": "enflicoxib",
        "search_aliases": ["ダクソコックス", "Daxocox", "DAXOCOX", "エンフリコキシブ"],
        "name": "Enflicoxib (Daxocox)",
        "name_ja": "エンフリコキシブ（ダクソコックス）",
        "category": "nsaids",
        "mechanism": "COX-2-selective NSAID (coxib); its active pyrazoline metabolite has a long elimination half-life, allowing once-weekly oral dosing.",
        "mechanism_ja": "COX-2選択的NSAID（コキシブ系）。活性代謝物（ピラゾリン体）の消失半減期が長く、週1回の経口投与が可能。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Loading dose 8 mg/kg PO on day 0, then 4 mg/kg PO once weekly, given with food, for osteoarthritis pain (DAXOCOX EU SPC, EMA 2021; Salichs 2022 Vet Rec — non-inferior to reference NSAIDs over 6 weeks).",
                "dosage_ja": "変形性関節症の疼痛に初日8 mg/kg PO（負荷量）、以降4 mg/kg PO 週1回を食事と共に投与（DAXOCOX EU SPC、EMA 2021年／Salichs 2022 Vet Rec — 6週間で対照NSAIDに非劣性）。",
                "notes": "Weekly dosing aids compliance but cannot be stopped quickly if an adverse effect develops — screen renal/hepatic function and GI history before starting, recheck periodically, and allow a full washout per the SPC before switching to another NSAID or corticosteroid. Not approved in Japan.",
                "notes_ja": "週1回投与で服薬遵守が容易だが、副作用発現時に速やかに体内から消失させられない — 開始前に腎・肝機能と消化管疾患歴を確認し定期的に再評価、他のNSAIDやステロイドへ切り替える際はSPCに従い十分な休薬期間を置く。国内未承認。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not licensed for cats — no feline dose established.",
                "dosage_ja": "猫には未承認 — 猫の用量は確立していない。",
                "notes": "Use feline-licensed NSAIDs (meloxicam, robenacoxib) or frunevetmab for feline OA.",
                "notes_ja": "猫のOAには猫用承認NSAID（メロキシカム・ロベナコキシブ）またはフルネベトマブを用いる。",
            },
        },
        "contraindications": "Gastrointestinal ulceration or bleeding, renal or hepatic impairment, dehydration/hypovolaemia, coagulopathy, pregnancy/lactation, concurrent NSAID or corticosteroid use, known coxib hypersensitivity.",
        "contraindications_ja": "消化管潰瘍・出血、腎・肝機能障害、脱水・循環血液量減少、凝固障害、妊娠・授乳、他のNSAIDやステロイドとの併用、コキシブ系への過敏症。",
        "side_effects": [
            "Vomiting, diarrhoea, inappetence",
            "Gastrointestinal ulceration (rare)",
            "Renal or hepatic adverse effects (rare)",
        ],
        "side_effects_ja": [
            "嘔吐・下痢・食欲不振",
            "消化管潰瘍（稀）",
            "腎・肝の有害事象（稀）",
        ],
        "drug_interactions": [
            {
                "drug": "Other NSAIDs / corticosteroids",
                "effect": "Additive GI ulceration and renal risk — contraindicated; observe a full washout because of the long half-life.",
                "effect_ja": "消化管潰瘍・腎障害リスクの相加 — 併用禁忌。半減期が長いため十分な休薬期間を置く。",
                "severity": "major",
            },
            {
                "drug": "ACE inhibitors / diuretics",
                "effect": "Reduced renal perfusion — monitor renal function.",
                "effect_ja": "腎血流低下 — 腎機能を監視する。",
                "severity": "moderate",
            },
        ],
        "references": [
            "DAXOCOX (enflicoxib) EU Summary of Product Characteristics — EMA EPAR (2021)",
            "Salichs M, et al. Efficacy and safety of enflicoxib for treatment of canine osteoarthritis: a 6-week randomised, controlled, blind, multicentre clinical trial. Vet Rec 2022.",
        ],
    },
]
