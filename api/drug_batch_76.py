"""Drug batch 76 – 2026-10 session (第69弾).

Metamizole (dipyrone; JP: スルピリン) — a non-opioid, non-acidic pyrazolone
analgesic/antipyretic with weak peripheral COX activity and a spasmolytic
effect. It is FDA-approved for the control of pyrexia in horses (ZIMETA,
dipyrone injection, NADA 141-512, 2020), licensed for dogs/cats/horses in
much of Europe, and sold in Japan as veterinary sulpyrine injection for
livestock and horses. The dictionary had no pyrazolone at all, so the
frequently used equine antipyretic and the European multimodal analgesic
(often combined with an NSAID or opioid post-operatively) were missing.

Evidence: ZIMETA US label (FDA 2020); Plumb's Veterinary Drug Handbook
10th ed; Zanuzzo FS et al. Vet J 2015 (dipyrone 25 mg/kg IV in bitches after
ovariohysterectomy, analgesia comparable to meloxicam);
Lebkowska-Wieruszewska B et al. J Vet Pharmacol Ther 2018 (feline
pharmacokinetics — slow elimination supports once-daily dosing).
"""

DRUGS_BATCH_76 = [
    {
        "id": "metamizole",
        "search_aliases": [
            "メタミゾール",
            "ジピロン",
            "スルピリン",
            "dipyrone",
            "Dipyrone",
            "metamizole",
            "ジメタ",
            "Zimeta",
            "ZIMETA",
            "Novalgin",
            "ノバルジン",
        ],
        "name": "Metamizole (Dipyrone / Zimeta)",
        "name_ja": "メタミゾール（ジピロン・スルピリン）",
        "category": "analgesics",
        "mechanism": "Pyrazolone (non-acidic) analgesic-antipyretic: central COX inhibition with weak peripheral anti-inflammatory activity, plus a spasmolytic effect on smooth muscle; active metabolites (4-MAA, 4-AA) also act on cannabinoid/opioidergic descending pathways.",
        "mechanism_ja": "ピラゾロン系（非酸性）の鎮痛・解熱薬。中枢性COX阻害が主で末梢の抗炎症作用は弱く、平滑筋の鎮痙作用を併せ持つ。活性代謝物（4-MAA・4-AA）はカンナビノイド/オピオイド系の下行性抑制にも作用する。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Control of pyrexia: 30 mg/kg IV slowly, which may be repeated at 12-hour intervals for up to 3 days (ZIMETA label, FDA 2020). Visceral (spasmodic colic) analgesia has historically used 10-22 mg/kg IV.",
                "dosage_ja": "解熱（発熱の管理）: 30 mg/kg を緩徐に静注、12時間間隔で最長3日間反復可（ZIMETA ラベル、FDA 2020年）。痙攣性疝痛の内臓痛には従来 10-22 mg/kg IV が用いられてきた。",
                "notes": "Fever is a sign, not a diagnosis — investigate the cause (strangles, influenza/EHV, pneumonia, colitis) and do not let antipyresis mask a deteriorating infection. Inject slowly: rapid IV can cause hypotension/collapse. Avoid IM (painful). Do not combine with phenylbutazone or other NSAIDs without a clear rationale (additive GI/renal risk). Prohibited substance in competition (FEI) — observe detection times. Food-producing equids: follow local withdrawal rules (prohibited in food animals in the US). In Japan, licensed veterinary sulpyrine injection is the domestic product — follow its package insert.",
                "notes_ja": "発熱は所見であって診断ではない — 原因（腺疫・インフルエンザ/EHV・肺炎・大腸炎）を検索し、解熱で悪化する感染症をマスクしない。緩徐に静注する（急速静注で低血圧・虚脱）。筋注は疼痛のため避ける。フェニルブタゾン等のNSAIDとの併用は明確な理由がない限り避ける（消化管・腎リスクの相加）。競技馬では禁止物質（FEI）— 検出期間を守る。食用馬は各国の休薬規定に従う（米国では食用動物への使用禁止）。国内では動物用スルピリン注射液が流通 — 添付文書に従う。",
            },
            "dog": {
                "safe": True,
                "dosage": "25-35 mg/kg IV (slowly over >= 2-5 min) or PO q8h; often given as part of multimodal postoperative analgesia with an opioid (Zanuzzo 2015 Vet J: 25 mg/kg IV after ovariohysterectomy gave analgesia comparable to meloxicam). Antipyretic: 25 mg/kg.",
                "dosage_ja": "25-35 mg/kg を緩徐静注（2-5分以上かけて）または経口で8時間毎。オピオイドとの多角的術後鎮痛の一部として用いることが多い（Zanuzzo 2015 Vet J: 卵巣子宮摘出術後に 25 mg/kg IV でメロキシカムと同等の鎮痛）。解熱目的: 25 mg/kg。",
                "notes": "Useful when an NSAID should be avoided (renal compromise, GI ulceration, concurrent corticosteroid) because its renal/GI effects are milder — but it is not free of them. Rapid IV injection causes hypotension. Rare idiosyncratic agranulocytosis/blood dyscrasias: check CBC with repeated or prolonged use and stop if fever, mouth ulcers or infection appear. Not licensed in Japan for dogs (human/livestock products used off-label).",
                "notes_ja": "腎機能低下・消化管潰瘍・ステロイド併用などでNSAIDを避けたい症例の選択肢（腎・消化管への影響がNSAIDより軽い — ただし皆無ではない）。急速静注で低血圧。まれに特異体質性の無顆粒球症・血液障害 — 反復・長期使用時はCBCを確認し、発熱・口腔潰瘍・感染徴候が出たら中止。国内では犬用の承認なし（人用・家畜用製剤の適応外使用）。",
            },
            "cat": {
                "safe": True,
                "dosage": "25 mg/kg IV slowly or PO q12-24h (slow feline elimination — once daily is often sufficient; Lebkowska-Wieruszewska 2018 J Vet Pharmacol Ther).",
                "dosage_ja": "25 mg/kg を緩徐静注または経口で12-24時間毎（猫は消失が遅く1日1回で足りることが多い — Lebkowska-Wieruszewska 2018 J Vet Pharmacol Ther）。",
                "notes": "Bitter taste: oral solution causes marked hypersalivation and foaming — mix in food or use injectable. Use the lowest effective frequency in cats; monitor for vomiting and, with repeated dosing, CBC.",
                "notes_ja": "苦味が強く経口液では著しい流涎・泡沫を起こす — フードに混ぜるか注射剤を用いる。猫は最小有効頻度で使用し、嘔吐と（反復投与時は）CBCを監視する。",
            },
        },
        "contraindications": "Known pyrazolone hypersensitivity; pre-existing bone-marrow suppression or blood dyscrasia; hypotension/hypovolaemic shock (correct before giving IV); severe hepatic or renal failure; late pregnancy. Prohibited in food-producing animals in the US.",
        "contraindications_ja": "ピラゾロン系過敏症、既存の骨髄抑制・血液障害、低血圧・循環血液量減少性ショック（静注前に是正）、重度肝不全・腎不全、妊娠後期。米国では食用動物への使用禁止。",
        "side_effects": [
            "Hypotension / collapse with rapid IV injection",
            "Hypersalivation and vomiting (oral, especially cats)",
            "Rare idiosyncratic agranulocytosis / blood dyscrasias",
            "Injection-site pain (IM)",
        ],
        "side_effects_ja": [
            "急速静注による低血圧・虚脱",
            "流涎・嘔吐（経口、特に猫）",
            "まれな特異体質性無顆粒球症・血液障害",
            "注射部位の疼痛（筋注）",
        ],
        "drug_interactions": [
            {
                "drug": "Phenylbutazone / flunixin / other NSAIDs",
                "effect": "Additive gastrointestinal and renal risk; combine only with a defined multimodal rationale and monitoring.",
                "effect_ja": "消化管・腎リスクの相加 — 多角的鎮痛としての明確な理由とモニタリングがある場合のみ併用。",
                "severity": "moderate",
            },
            {
                "drug": "Chlorpromazine / phenothiazines (acepromazine)",
                "effect": "Severe hypothermia and additive hypotension reported.",
                "effect_ja": "重度の低体温と低血圧の相加が報告されている。",
                "severity": "major",
            },
            {
                "drug": "Methotrexate / other myelosuppressive drugs",
                "effect": "Additive haematological toxicity (agranulocytosis risk).",
                "effect_ja": "血液毒性の相加（無顆粒球症リスク）。",
                "severity": "major",
            },
        ],
        "references": [
            "ZIMETA (dipyrone injection) US label — FDA approval 2020 (control of pyrexia in horses)",
            "Plumb's Veterinary Drug Handbook, 10th ed. — Metamizole (Dipyrone)",
            "Zanuzzo FS et al. Analgesic and antihyperalgesic effects of dipyrone, meloxicam or a dipyrone-meloxicam combination in bitches undergoing ovariohysterectomy. Vet J 2015;205:33-37.",
            "Lebkowska-Wieruszewska B et al. Pharmacokinetics of metamizole (dipyrone) in cats. J Vet Pharmacol Ther 2018.",
        ],
    },
]
