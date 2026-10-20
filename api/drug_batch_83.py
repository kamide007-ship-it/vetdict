"""Drug batch 83 – 2026-10 第74弾.

1. Izenivetmab (Lenivia, Zoetis) — a long-acting caninised anti-NGF
   monoclonal antibody for osteoarthritis pain in dogs, given SC once every
   three months (Health Canada 2025; EU 2025/2026; GB VMD May 2026). The
   dictionary carried only the monthly anti-NGF bedinvetmab (Librela) for
   dogs, while cats already had both the monthly (frunevetmab) and the
   3-monthly (relfovetmab) options. Not authorised in Japan.

Evidence:
  - Lenivia (izenivetmab) Summary of Product Characteristics, VMD GB,
    issued May 2026 (AN 00027/2025): 0.05-0.1 mg/kg SC every 3 months by
    vial-strength weight bands; <5 kg 0.1 mL/kg from a 0.5 mg vial; do not
    use <12 months, in breeding, pregnant or lactating dogs; ADA in 3.46%;
    pivotal EU trial treatment success 37.3% vs 22.6% placebo at day 90,
    onset from day 7.
  - Zoetis press releases (Health Canada approval Oct 2025; GB approval 2026).
"""

DRUGS_BATCH_83 = [
    {
        "id": "izenivetmab",
        "search_aliases": [
            "イゼニベトマブ",
            "いぜにべとまぶ",
            "レニビア",
            "Lenivia",
            "izenivetmab",
        ],
        "name": "Izenivetmab (Lenivia)",
        "name_ja": "イゼニベトマブ（レニビア）",
        "category": "biologics",
        "mechanism": "Caninised monoclonal antibody that binds nerve growth factor (NGF), preventing NGF-TrkA signalling that drives peripheral sensitisation and osteoarthritis pain. Engineered for a long half-life so one SC injection covers about three months. Cleared by normal protein catabolism (no hepatic/renal CYP metabolism).",
        "mechanism_ja": "神経成長因子（NGF）に結合する犬化モノクローナル抗体で、末梢感作と変形性関節症の疼痛を駆動するNGF-TrkAシグナルを遮断する。長い半減期を持つよう設計され、1回の皮下注射で約3ヶ月作用する。通常の蛋白異化で消失し、肝CYP代謝・腎排泄に依存しない。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.05-0.1 mg/kg SC once every 3 months, dosed by vial strength (entire 1 mL vial): 5.0-10.0 kg 0.5 mg; 10.1-20.0 kg 1.0 mg; 20.1-30.0 kg 1.5 mg; 30.1-40.0 kg 2.0 mg; 40.1-60.0 kg 3.0 mg; >60 kg combine vials in one syringe per the label chart. <5.0 kg: 0.1 mL/kg drawn from a 0.5 mg vial (discard the remainder). Dogs ≥12 months only.",
                "dosage_ja": "0.05-0.1 mg/kg SC 3ヶ月に1回。バイアル規格（1 mL全量）で体重帯投与: 5.0-10.0 kg 0.5 mg、10.1-20.0 kg 1.0 mg、20.1-30.0 kg 1.5 mg、30.1-40.0 kg 2.0 mg、40.1-60.0 kg 3.0 mg、60 kg超はラベル表に従い複数バイアルを1本のシリンジに合算。5.0 kg未満は0.5 mgバイアルから0.1 mL/kgを採取（残液は廃棄）。12ヶ月齢以上のみ。",
                "notes": "Pivotal EU trial: treatment success (CBPI) 37.3% vs 22.6% placebo at day 90, onset from day 7; some waning of effect near the end of each interval — if response is absent or limited, change treatment. Anti-drug antibodies in 3.46% (lower exposure, sometimes lack of efficacy). Not studied in dogs previously given other monoclonal antibodies (e.g. bedinvetmab). Increase exercise gradually over a few weeks once pain is controlled. Caution with pre-existing IMHA/ITP. No safety data for concurrent long-term NSAIDs (human anti-NGF rapidly progressive OA risk rose with >90-day NSAID co-use; no canine equivalent reported). Give vaccines at a different site. Accidental self-injection: anaphylaxis risk; pregnant women must avoid self-injection (NGF is essential for fetal neurodevelopment). Not authorised in Japan.",
                "notes_ja": "ピボタル試験（EU）: 90日目の治療成功率（CBPI）37.3% vs プラセボ22.6%、効果発現は7日目から。投与間隔の終盤に効果減弱がみられることがあり、無効・効果不十分なら他の治療に変更する。抗薬物抗体3.46%（血中濃度低下・一部で効果消失）。他のモノクローナル抗体（ベジンベトマブ等）の投与歴がある犬では未検討。疼痛が抑えられたら運動量は数週間かけて段階的に増やす。IMHA・ITPの既往では慎重に。NSAIDsの長期併用の安全性データはない（ヒトの抗NGF抗体では90日超のNSAID併用で急速進行性OAが増加 — 犬で同等の報告はない）。ワクチンは別部位に接種。誤自己注射でアナフィラキシーの恐れ、妊婦は自己注射を厳に避ける（NGFは胎児の神経発生に必須）。国内未承認。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not for cats (caninised antibody) — use frunevetmab (Solensia, monthly) or relfovetmab (Portela, 3-monthly).",
                "dosage_ja": "猫には使用しない（犬化抗体）— フルネベトマブ（ソレンシア、月1回）またはレルフォベトマブ（ポルテラ、3ヶ月毎）を使用。",
                "notes": "Species-specific antibody framework.",
                "notes_ja": "抗体のフレームワークが種特異的。",
            },
        },
        "contraindications": "Dogs under 12 months; dogs intended for breeding; pregnant or lactating dogs; hypersensitivity to izenivetmab.",
        "contraindications_ja": "12ヶ月齢未満、繁殖予定の犬、妊娠・授乳中の犬、イゼニベトマブ過敏症。",
        "side_effects": [
            "Injection-site reactions",
            "Anti-drug antibodies (3.46%) with loss of efficacy",
            "Hypersensitivity (rare)",
        ],
        "side_effects_ja": ["注射部位反応", "抗薬物抗体（3.46%）による効果減弱", "過敏反応（まれ）"],
        "drug_interactions": [
            {
                "drug": "Bedinvetmab (Librela)",
                "effect": "Duplicate anti-NGF antibody therapy; safety after prior monoclonal antibodies not studied.",
                "effect_ja": "抗NGF抗体療法の重複。他の抗体製剤の投与歴がある犬での安全性は未検討。",
                "severity": "major",
            },
            {
                "drug": "NSAIDs (long-term concurrent use)",
                "effect": "No canine safety data for long-term co-administration; in humans >90-day NSAID co-use with anti-NGF raised rapidly progressive OA risk.",
                "effect_ja": "犬での長期併用の安全性データなし。ヒトでは抗NGF抗体と90日超のNSAID併用で急速進行性OAが増加。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Lenivia (izenivetmab) Summary of Product Characteristics, Veterinary Medicines Directorate (GB), issued May 2026, Zoetis.",
            "Zoetis. Health Canada approval of Lenivia (izenivetmab injection) for osteoarthritis pain in dogs. Press release, Oct 2025.",
        ],
    },
]
