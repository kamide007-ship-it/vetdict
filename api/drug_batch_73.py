"""Drug batch 73 – 2026-10 session: two newly licensed veterinary biologic /
targeted drugs that were absent from the dictionary.

1. Atinvicitinib (NUMELVI, Merck/MSD Animal Health) — the first
   second-generation, JAK1-selective inhibitor for canine allergic pruritus.
   EU marketing authorisation 2025, FDA approval Feb 2026, UK VMD 2026.
   Label: 0.8-1.2 mg/kg PO once daily at or around mealtime from the first
   dose (no twice-daily induction phase), dogs >= 6 months; tablets 4.8 /
   7.2 / 21.6 / 31.6 mg (scored). Not for dogs < 2 kg (tablet strengths
   do not allow accurate dosing).
2. Relfovetmab (PORTELA, Zoetis) — a felinised anti-NGF monoclonal antibody
   with a THREE-MONTH dosing interval for feline osteoarthritis pain
   (EU authorisation Oct 2025, Health Canada Dec 2025, GB VMD 2026; not
   FDA-approved at time of entry). SC injection every 3 months; strengths
   2.5 mg and 6.4 mg per 1 mL vial dosed by weight band (pivotal study dose
   range 0.5-1.25 mg/kg). Contraindicated < 12 months, breeding /
   pregnant / lactating cats; immunogenicity (anti-drug antibodies)
   possible; no data beyond 9 months of treatment.

Sources: Merck Animal Health NUMELVI US label & dosing chart; VMD SPC
3179257/3179301; European Commission Union Product Register (Portela 2.5 mg
and 6.4 mg SmPC); Zoetis press releases (EC Oct 2025, Health Canada Dec 2025,
VMD 2026).
"""

DRUGS_BATCH_73 = [
    {
        "id": "atinvicitinib",
        "search_aliases": [
            "ヌメルビ",
            "ニュメルヴィ",
            "Numelvi",
            "NUMELVI",
            "アチンビシチニブ",
        ],
        "name": "Atinvicitinib (Numelvi)",
        "name_ja": "アチンビシチニブ（ヌメルビ）",
        "category": "dermatology",
        "mechanism": "Second-generation, JAK1-selective Janus kinase inhibitor. Blocks JAK1-dependent signalling of pruritogenic and pro-inflammatory cytokines (IL-31, IL-4, IL-13, IL-2, IL-6) while sparing JAK2/JAK3/TYK2 more than first-generation pan-JAK inhibitors — the design rationale is less interference with haematopoiesis (JAK2) and immune surveillance.",
        "mechanism_ja": "第二世代のJAK1選択的ヤヌスキナーゼ阻害薬。掻痒・炎症性サイトカイン（IL-31・IL-4・IL-13・IL-2・IL-6）のJAK1依存性シグナルを遮断し、第一世代の汎JAK阻害薬よりJAK2/JAK3/TYK2への作用を抑えた設計（造血=JAK2・免疫監視への干渉を減らす意図）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.8-1.2 mg/kg PO once daily at or around mealtime — once daily from the first dose (no twice-daily induction phase, unlike oclacitinib). Dose by the label weight-band table (scored tablets 4.8 / 7.2 / 21.6 / 31.6 mg; tablets may be halved along the score). Dogs >= 6 months of age; not for dogs < 2 kg (tablet strengths do not allow accurate dosing) (NUMELVI US label; VMD SPC).",
                "dosage_ja": "0.8-1.2 mg/kg PO q24h、食事時またはその前後に投与 — 初回から1日1回（オクラシチニブのような1日2回の導入期なし）。ラベルの体重帯表で投与（割線入り錠 4.8 / 7.2 / 21.6 / 31.6 mg、割線で半錠可）。6ヶ月齢以上。2 kg未満の犬は錠剤規格上正確な投与ができないため対象外（NUMELVI 米国ラベル・英国VMD SPC）。",
                "notes": "Indication: control of pruritus associated with allergic dermatitis and control of atopic dermatitis in dogs. Symptomatic — investigate and manage the underlying allergy (flea control, elimination diet, ASIT). Do not stack JAK inhibitors (oclacitinib, ilunocitinib). As with other JAK inhibitors: may increase susceptibility to infection and demodicosis and exacerbate neoplasia — not for dogs with serious infection or evidence of malignancy; monitor CBC/biochemistry with long-term use. Vaccination timing: follow the label's guidance. Not approved in Japan as of this entry — overseas (EU/US/UK) product.",
                "notes_ja": "適応: アレルギー性皮膚炎に伴う掻痒の制御、および犬アトピー性皮膚炎の制御。対症薬であり、基礎アレルギーの管理（ノミ対策・除去食試験・減感作療法）を並行する。JAK阻害薬同士（オクラシチニブ・イルノシチニブ）を重ねない。JAK阻害薬共通の注意: 感染症・毛包虫症の易感染性、腫瘍の増悪の可能性 — 重篤な感染症や悪性腫瘍のある犬には使用しない。長期投与ではCBC・血液化学を定期監視。ワクチン接種のタイミングはラベルに従う。本収載時点で国内未承認の海外（EU・米国・英国）製品。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not licensed for cats — no feline dose established.",
                "dosage_ja": "猫には未承認 — 猫の用量は確立していない。",
                "notes": "Feline allergic dermatitis: glucocorticoids / ciclosporin remain first line.",
                "notes_ja": "猫のアレルギー性皮膚炎はグルココルチコイド・シクロスポリンが第一選択。",
            },
        },
        "contraindications": "Dogs < 6 months or < 2 kg. Serious infection, active demodicosis or evidence of neoplasia. Breeding, pregnant or lactating dogs (safety not established). Concurrent use of another JAK inhibitor.",
        "contraindications_ja": "6ヶ月齢未満・2 kg未満の犬。重篤な感染症・活動性毛包虫症・悪性腫瘍の所見がある犬。繁殖・妊娠・授乳中の犬（安全性未確立）。他のJAK阻害薬との併用。",
        "side_effects": [
            "Vomiting, diarrhea (usually mild and transient)",
            "Lethargy, decreased appetite",
            "Increased susceptibility to infections / demodicosis (JAK-inhibitor class)",
        ],
        "side_effects_ja": [
            "嘔吐・下痢（通常は軽度・一過性）",
            "嗜眠・食欲低下",
            "感染症・毛包虫症への易感染性（JAK阻害薬クラス共通）",
        ],
        "drug_interactions": [
            {
                "drug": "Oclacitinib / Ilunocitinib (other JAK inhibitors)",
                "effect": "Duplicate JAK inhibition — no added antipruritic benefit, additive immunosuppression.",
                "effect_ja": "JAK阻害の重複 — 止痒効果は上乗せされず免疫抑制が相加。",
                "severity": "major",
            },
            {
                "drug": "Ciclosporin / systemic glucocorticoids",
                "effect": "Additive immunosuppression — combined use not evaluated on the label; reserve for specialist-supervised cases.",
                "effect_ja": "免疫抑制の相加 — ラベル上併用は未評価。専門医管理下の症例に限る。",
                "severity": "moderate",
            },
        ],
        "references": [
            "NUMELVI (atinvicitinib tablets) US product label and dosing chart, Merck Animal Health (FDA approval Feb 2026)",
            "VMD Summary of Product Characteristics, NUMELVI tablets for dogs (SPC 3179257 / 3179301)",
            "European Commission marketing authorisation, NUMELVI (2025)",
        ],
    },
    {
        "id": "relfovetmab",
        "search_aliases": [
            "ポルテラ",
            "Portela",
            "レルフォベトマブ",
        ],
        "name": "Relfovetmab (Portela)",
        "name_ja": "レルフォベトマブ（ポルテラ）",
        "category": "biologics",
        "mechanism": "Felinised anti-nerve growth factor (NGF) monoclonal antibody. Binds NGF and prevents its interaction with TrkA/p75 receptors, interrupting peripheral and central sensitisation in osteoarthritis pain — same target as frunevetmab (Solensia) but engineered for a three-month (rather than monthly) dosing interval.",
        "mechanism_ja": "猫化抗神経成長因子（NGF）モノクローナル抗体。NGFに結合しTrkA/p75受容体との結合を阻害して、変形性関節症の痛みにおける末梢性・中枢性感作を遮断する。標的はフルネベトマブ（ソレンシア）と同じだが、投与間隔を月1回ではなく3ヶ月に1回に延ばした長時間作用型。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "SC injection once every 3 months, dosed by the label weight-band table using the 2.5 mg/mL or 6.4 mg/mL vial (pivotal-study dose range 0.5-1.25 mg/kg). Cats >= 12 months of age. Do not use the monthly frunevetmab (Solensia) volume or interval interchangeably (EU SmPC; Health Canada / VMD authorisation).",
                "dosage_ja": "3ヶ月に1回の皮下注射。ラベルの体重帯表に従い 2.5 mg/mL または 6.4 mg/mL バイアルで投与（ピボタル試験の用量範囲 0.5-1.25 mg/kg）。12ヶ月齢以上。月1回製剤フルネベトマブ（ソレンシア）と液量・間隔を互換的に扱わない（EU SmPC・カナダ/英国承認）。",
                "notes": "Indication: alleviation of pain associated with osteoarthritis in cats. The 3-month interval is the main practical advantage for cats that are difficult to bring in monthly. Assess response after the first dose; continue only in responders. Immunogenicity: anti-drug (including neutralising) antibodies may develop — loss of effect can reflect this. No safety data beyond 9 months of treatment. Not FDA-approved and not approved in Japan at time of entry (EU/Canada/GB product). Concurrent NSAIDs: not evaluated — avoid routine combination (anti-NGF class caution about joint adverse events).",
                "notes_ja": "適応: 猫の変形性関節症に伴う痛みの緩和。3ヶ月間隔が最大の実用上の利点（毎月の通院が難しい猫）。初回投与後に効果を評価し、反応例のみ継続する。免疫原性: 抗薬物抗体（中和抗体を含む）が生じうる — 効果減弱の原因となりうる。9ヶ月を超える投与期間の安全性データはない。本収載時点でFDA未承認・国内未承認（EU・カナダ・英国の製品）。NSAIDs併用は未評価 — 抗NGF抗体クラスの関節有害事象への注意から日常的な併用は避ける。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not for dogs — felinised antibody (use the canine anti-NGF bedinvetmab / Librela).",
                "dosage_ja": "犬には使用しない — 猫化抗体（犬にはベジンベトマブ（リブレラ）を使用）。",
                "notes": "Species-specific antibody; immunogenic in other species.",
                "notes_ja": "種特異的抗体であり他種では免疫原性を示す。",
            },
        },
        "contraindications": "Cats < 12 months of age. Breeding, pregnant or lactating cats (NGF is involved in fetal neural development). Known hypersensitivity to relfovetmab or excipients.",
        "contraindications_ja": "12ヶ月齢未満の猫。繁殖・妊娠・授乳中の猫（NGFは胎子の神経発達に関与）。レルフォベトマブまたは添加物への過敏症。",
        "side_effects": [
            "Injection-site reactions (pain, swelling)",
            "Skin reactions (pruritus, dermatitis, alopecia) — reported with feline anti-NGF antibodies",
            "Vomiting / diarrhoea (uncommon)",
        ],
        "side_effects_ja": [
            "注射部位反応（疼痛・腫脹）",
            "皮膚反応（掻痒・皮膚炎・脱毛）— 猫の抗NGF抗体で報告",
            "嘔吐・下痢（まれ）",
        ],
        "drug_interactions": [
            {
                "drug": "Frunevetmab (Solensia)",
                "effect": "Duplicate anti-NGF therapy — never combine; switch only after the dosing interval of the previous product has elapsed.",
                "effect_ja": "抗NGF療法の重複 — 併用しない。切り替えは前製剤の投与間隔経過後に行う。",
                "severity": "major",
            },
            {
                "drug": "NSAIDs (meloxicam, robenacoxib)",
                "effect": "Combination not evaluated; anti-NGF + NSAID co-administration has been associated with accelerated joint pathology in other species — avoid routine combination.",
                "effect_ja": "併用は未評価。他種では抗NGF抗体とNSAIDsの併用で関節病変の進行加速が報告 — 日常的な併用は避ける。",
                "severity": "moderate",
            },
        ],
        "references": [
            "European Commission Union Product Register: Portela 2.5 mg / 6.4 mg solution for injection for cats — SmPC (authorised Oct 2025)",
            "Zoetis: Health Canada approval of Portela (Dec 2025); VMD (Great Britain) approval (2026)",
        ],
    },
]
