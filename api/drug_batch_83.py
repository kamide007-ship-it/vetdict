"""Drug batch 83 – 2026-10 第74弾.

1. Izenivetmab (Lenivia) — the first long-acting caninised anti-NGF
   monoclonal antibody for canine osteoarthritis pain, given once every three
   months (Health Canada 2025; EU 2025; UK VMD 29 May 2026). The existing
   anti-NGF entry, bedinvetmab (Librela), is monthly.

Evidence (label figures copied from the UK package leaflet, Vm 42058/5196,
issued May 2026):
  - Dose 0.05-0.1 mg/kg SC once every three months; 1 mL vials of 0.5 / 1.0 /
    1.5 / 2.0 / 3.0 mg by body-weight band (5-10, 10.1-20, 20.1-30, 30.1-40,
    40.1-60 kg; 60.1-80 kg two 2.0 mg vials; 80.1-100 kg 2.0 + 3.0 mg;
    100.1-120 kg two 3.0 mg vials). <5 kg: 0.1 mL/kg from a 0.5 mg vial.
  - Contraindicated <12 months of age, breeding, pregnant or lactating dogs.
  - Anti-drug antibodies in 3.46% of dogs (9-month repeat-dose trial);
    waning of effect towards the end of each interval; caution in IMHA/IMTP;
    no long-term NSAID co-administration safety data.
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
        "mechanism": "Caninised monoclonal antibody against canine nerve growth factor (NGF). Binding NGF prevents its interaction with TrkA/p75 receptors on nociceptors and immune cells, reducing peripheral sensitisation and OA pain. Degraded like endogenous protein (not metabolised by cytochrome P450). Engineered for a three-month dosing interval, compared with the monthly bedinvetmab (Librela).",
        "mechanism_ja": "犬神経成長因子（NGF）に対する犬化モノクローナル抗体。NGFに結合して侵害受容器・免疫細胞上のTrkA/p75受容体との相互作用を阻止し、末梢性感作と変形性関節症（OA）の疼痛を軽減する。内因性蛋白と同様に分解され、CYP450では代謝されない。月1回のベジンベトマブ（リブレラ）に対し、3ヶ月間隔の投与を想定して設計されている。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.05-0.1 mg/kg SC once every 3 months (label). Give the entire 1 mL vial by body weight: 5-10 kg 0.5 mg; 10.1-20 kg 1.0 mg; 20.1-30 kg 1.5 mg; 30.1-40 kg 2.0 mg; 40.1-60 kg 3.0 mg; 60.1-80 kg two 2.0 mg vials; 80.1-100 kg 2.0 mg + 3.0 mg; 100.1-120 kg two 3.0 mg vials (combined into one syringe, single SC injection). Dogs <5 kg: withdraw 0.1 mL/kg from one 0.5 mg vial and discard the rest. Dogs ≥12 months only.",
                "dosage_ja": "0.05〜0.1 mg/kg 皮下投与 3ヶ月に1回（ラベル）。体重帯ごとに1 mLバイアルを全量投与: 5〜10 kg 0.5 mg、10.1〜20 kg 1.0 mg、20.1〜30 kg 1.5 mg、30.1〜40 kg 2.0 mg、40.1〜60 kg 3.0 mg、60.1〜80 kg 2.0 mgを2本、80.1〜100 kg 2.0 mg＋3.0 mg、100.1〜120 kg 3.0 mgを2本（同一シリンジに合わせ1回の皮下注射）。5 kg未満: 0.5 mgバイアルから0.1 mL/kgを採取し残りは廃棄。12ヶ月齢以上のみ。",
                "notes": "Effect may wane towards the end of each three-month interval (pivotal trial); not all dogs respond — use alternative analgesia if response is absent or limited. Anti-drug antibodies developed in 3.46% of dogs and were associated with lower drug levels and lack of efficacy in some. Not studied in dogs previously given other monoclonal antibodies. Reintroduce exercise gradually over a few weeks after pain relief. Caution in dogs with pre-existing immune-mediated haemolytic anaemia or thrombocytopenia (very rare post-marketing reports). Not authorised in Japan.",
                "notes_ja": "各3ヶ月間隔の終盤に効果が減弱しうる（承認試験）。全例が反応するわけではなく、反応がない・乏しい場合は他の鎮痛法へ切り替える。抗薬物抗体が3.46%で生じ、一部で血中濃度低下・効果不十分と関連した。他のモノクローナル抗体の投与歴がある犬では未検討。疼痛が軽減したら運動量は数週間かけて徐々に増やす。免疫介在性溶血性貧血・血小板減少症の既往がある犬では慎重に（市販後の非常にまれな報告）。国内未承認。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not for cats (caninised antibody) — use frunevetmab (Solensia) or relfovetmab (Portela).",
                "dosage_ja": "猫には使用しない（犬化抗体） — フルネベトマブ（ソレンシア）またはレルフォベトマブ（ポルテラ）を使用。",
                "notes": "Species-specific antibody.",
                "notes_ja": "動物種特異的な抗体製剤。",
            },
        },
        "contraindications": "Hypersensitivity to izenivetmab or excipients; dogs under 12 months of age; breeding dogs; pregnant or lactating dogs (anti-NGF antibodies are teratogenic/foetotoxic in primates). Do not mix with other products in the syringe.",
        "contraindications_ja": "イゼニベトマブまたは添加物への過敏症、12ヶ月齢未満、繁殖犬、妊娠・授乳中の犬（抗NGF抗体は霊長類で催奇形性・胎子毒性）。他剤とシリンジ内で混合しない。",
        "side_effects": [
            "Pain at injection (common)",
            "Ataxia, polydipsia, polyuria (uncommon)",
            "Anorexia, lethargy (rare)",
            "Hypersensitivity (facial swelling), immune-mediated haemolytic anaemia, immune-mediated thrombocytopenia (very rare)",
        ],
        "side_effects_ja": [
            "注射時の疼痛（よくみられる）",
            "運動失調・多飲・多尿（まれ）",
            "食欲不振・元気消失（まれ）",
            "過敏反応（顔面腫脹）・免疫介在性溶血性貧血・免疫介在性血小板減少症（非常にまれ）",
        ],
        "drug_interactions": [
            {
                "drug": "Bedinvetmab (Librela)",
                "effect": "Duplicate anti-NGF antibody therapy — never combine; switch only after the previous product's dosing interval has elapsed.",
                "effect_ja": "抗NGF抗体療法の重複 — 併用しない。前製剤の投与間隔が経過してから切り替える。",
                "severity": "major",
            },
            {
                "drug": "NSAIDs (long-term)",
                "effect": "No safety data for concurrent long-term NSAID use in dogs; rapidly progressive OA was reported in humans given anti-NGF antibodies with >90 days of NSAIDs (no canine equivalent reported).",
                "effect_ja": "犬でのNSAIDs長期併用の安全性データはない。ヒトでは抗NGF抗体と90日超のNSAIDs併用で急速進行性OAが報告されている（犬では同等の報告なし）。",
                "severity": "moderate",
            },
            {
                "drug": "Vaccines",
                "effect": "If given on the same day, inject vaccines at a different site.",
                "effect_ja": "同日に接種する場合はワクチンを別部位に投与する。",
                "severity": "minor",
            },
        ],
        "references": [
            "Lenivia (izenivetmab) solution for injection for dogs, UK package leaflet, Vm 42058/5196, Zoetis UK, issued May 2026.",
            "Zoetis. Health Canada approval of Lenivia (izenivetmab) for alleviation of osteoarthritis pain in dogs, October 2025.",
            "Enomoto M et al. Anti-nerve growth factor monoclonal antibodies for the control of pain in dogs and cats. Vet Rec 2019;184:23.",
        ],
    },
]
