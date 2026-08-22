"""Drug batch 44 – referenced-but-absent agents surfaced by the 2026-08 audit (12th sweep).

A context-aware katakana token sweep of disease treatment protocols,
cross-checked with the real text matcher (find_drugs_in_text), found three
agents that VetDict's own content instructs clinicians to use — with explicit
doses — yet were absent from the formulary (a fourth hit, DOCP with 4
references, turned out to be present already under id "desoxycorticosterone" —
only the bare acronym failed to resolve, fixed via _KATAKANA_VARIANT_ALIASES):

  - シメチコン (simethicone): referenced 37 times across 6 herbivore /
    small-mammal species — the GI stasis / bloat protocols cite
    "シメチコン40-50mg/kg PO q6-8h" verbatim (rabbit, guinea pig, chinchilla,
    degu, hamster, exotic_other). A luminal anti-foaming surfactant that is
    part of the standard small-herbivore stasis bundle.
  - トリエンチン (trientine): the named second-line copper chelator in the
    canine copper-associated hepatopathy entries ("トリエンチン 10-15 mg/kg
    PO q12h") for dogs that cannot tolerate D-penicillamine.
  - オロパタジン (olopatadine 0.1% ophthalmic): cited with dosing in the
    allergic-conjunctivitis protocol ("オロパタジン0.1%点眼 q12h（抗ヒスタ
    ミン+マスト細胞安定化）") — a standard veterinary-adopted human ophthalmic
    in Japan (パタノール).

References:
  - Carpenter's Exotic Animal Formulary, 6th ed — simethicone 65-130 mg/kg PO
    for rabbits and small herbivores (paediatric drops); luminal action only.
  - Oglesbee BL, Blackwell's Five-Minute Veterinary Consult: Small Mammal,
    3rd ed — simethicone as adjunct in rabbit gastrointestinal stasis/bloat;
    emphasises it does not replace fluids, analgesia and refeeding.
  - Plumb's Veterinary Drug Handbook, 10th ed — simethicone small-animal
    dosing (25-200 mg/dog PO); trientine 10-15 mg/kg PO q12h for
    copper-associated hepatopathy when penicillamine is not tolerated.
  - Webster CRL et al. 2019 ACVIM consensus statement on canine chronic
    hepatitis — chelation (D-penicillamine first line; trientine as the
    alternative chelator) for copper-associated hepatopathy.
  - Maggs DJ, Slatter's Fundamentals of Veterinary Ophthalmology, 6th ed —
    topical antihistamine/mast-cell stabilisers (olopatadine) for allergic
    conjunctivitis in dogs and cats.
"""

DRUGS_BATCH_44: list[dict] = [
    {
        "id": "simethicone",
        "search_aliases": [
            "シメチコン",
            "ジメチコン",
            "ガスコン",
            "Simethicone",
            "Gas-X",
        ],
        "name": "Simethicone",
        "name_ja": "シメチコン（ガスコン）",
        "category": "gi_drugs",
        "mechanism": "Anti-foaming surfactant. Lowers the surface tension of gas bubbles trapped in ingesta and mucus, causing them to coalesce into larger bubbles that are passed more easily. Acts entirely within the gut lumen — it is not absorbed systemically, which is why it is considered extremely safe even in debilitated small herbivores.",
        "mechanism_ja": "消泡性界面活性剤。消化管内容物・粘液中に閉じ込められたガス気泡の表面張力を低下させ、気泡を合一化させて排出しやすくする。作用は完全に消化管腔内に限局し全身吸収されない — 衰弱した小型草食動物でも極めて安全とされる理由である。",
        "species_info": {
            "rabbit": {
                "safe": True,
                "dosage": "GI stasis / gas bloat adjunct: 65-130 mg/kg PO q1h for 2-3 doses initially, then q6-8h as needed (paediatric simethicone drops; Carpenter 6th ed). VetDict stasis protocols use 40-50 mg/kg PO q6-8h.",
                "dosage_ja": "消化管うっ滞・ガス性鼓脹の補助: 初期は 65-130 mg/kg 経口 1時間毎 × 2-3回、以後必要に応じ 6-8時間毎（小児用シメチコン内用液; Carpenter 6th ed）。本データベースのうっ滞プロトコルでは 40-50 mg/kg 経口 6-8時間毎。",
                "notes": "Adjunct only — never a substitute for fluids, analgesia, syringe feeding and motility support. Rule out obstructive ileus before adding prokinetics to the bundle.",
                "notes_ja": "あくまで補助 — 輸液・鎮痛・強制給餌・消化管運動サポートの代替にはならない。閉塞性イレウスを除外してから運動促進薬を併用すること。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Gas bloat / GI stasis adjunct: 40-65 mg/kg PO q6-8h (paediatric drops via syringe).",
                "dosage_ja": "鼓脹・消化管うっ滞の補助: 40-65 mg/kg 経口 6-8時間毎（小児用内用液をシリンジ投与）。",
                "notes": "Acute gastric dilation in guinea pigs can be surgical — simethicone is supportive, not definitive therapy.",
                "notes_ja": "モルモットの急性胃拡張は外科適応となりうる — シメチコンは支持療法であり根治治療ではない。",
            },
            "chinchilla": {
                "safe": True,
                "dosage": "GI stasis gas relief: 40-50 mg/kg PO q6-8h until normal fecal output resumes.",
                "dosage_ja": "消化管うっ滞のガス軽減: 40-50 mg/kg 経口 6-8時間毎、正常な便産生の再開まで。",
            },
            "hamster": {
                "safe": True,
                "dosage": "Gas/bloat adjunct: 40-65 mg/kg PO q6-8h (paediatric drops).",
                "dosage_ja": "ガス・鼓脹の補助: 40-65 mg/kg 経口 6-8時間毎（小児用内用液）。",
            },
            "dog": {
                "safe": True,
                "dosage": "Flatulence / gas colic adjunct: 25-200 mg/dog PO q6-12h (Plumb's).",
                "dosage_ja": "鼓腸・ガス性疝痛の補助: 25-200 mg/頭 経口 6-12時間毎（Plumb's）。",
                "notes": "Does not reduce gas production — only aids passage. In suspected GDV do not delay decompression/surgery for oral medication.",
                "notes_ja": "ガス産生自体は減らさず排出を助けるのみ。GDV疑い例では経口投与のために減圧・手術を遅らせないこと。",
            },
            "cat": {
                "safe": True,
                "dosage": "Flatulence adjunct: 25-50 mg/cat PO q8-12h.",
                "dosage_ja": "鼓腸の補助: 25-50 mg/頭 経口 8-12時間毎。",
            },
        },
        "side_effects": "Essentially none at clinical doses (not absorbed); rare loose stool from vehicle",
        "side_effects_ja": "臨床用量では実質的になし（吸収されない）。まれに基剤による軟便",
        "contraindications": "Suspected complete GI obstruction or GDV — gas relief must not delay decompression/surgical management; simethicone will not resolve an obstruction",
        "contraindications_ja": "完全消化管閉塞・GDVの疑い — ガス軽減のために減圧・外科的管理を遅らせてはならない。シメチコンで閉塞は解除できない",
        "drug_interactions": [
            {
                "drug": "Metoclopramide/cisapride (prokinetics)",
                "effect": "Standard stasis-bundle combination once obstruction is excluded — simethicone coalesces gas while prokinetics restore transit",
                "effect_ja": "閉塞除外後のうっ滞バンドル標準併用 — シメチコンがガスを合一化し、運動促進薬が輸送能を回復させる",
                "severity": "info",
            },
        ],
    },
    {
        "id": "trientine",
        "search_aliases": [
            "トリエンチン",
            "トリエンチン塩酸塩",
            "メタライト",
            "Trientine",
            "Syprine",
        ],
        "name": "Trientine (Triethylenetetramine)",
        "name_ja": "トリエンチン（トリエチレンテトラミン）",
        "category": "miscellaneous",
        "mechanism": "Oral copper chelator. Forms a stable complex with copper in the gut and circulation, promoting urinary copper excretion and reducing hepatic copper accumulation. Second-line to D-penicillamine for canine copper-associated hepatopathy — chosen when penicillamine causes intractable vomiting or hypersensitivity.",
        "mechanism_ja": "経口銅キレート剤。消化管内および循環中の銅と安定な複合体を形成し、尿中銅排泄を促進して肝銅蓄積を減少させる。犬の銅関連性肝障害ではD-ペニシラミンの第二選択 — ペニシラミンで難治性嘔吐や過敏症が出た症例に選択する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Copper-associated hepatopathy (penicillamine-intolerant): 10-15 mg/kg PO q12h on an empty stomach (1 h before or 2 h after food). Continue until hepatic copper is controlled (recheck biopsy quantification); often months. Combine with a low-copper diet ± zinc maintenance after de-coppering (Plumb's; ACVIM 2019 chronic hepatitis consensus).",
                "dosage_ja": "銅関連性肝障害（ペニシラミン不耐例）: 10-15 mg/kg 経口 12時間毎、空腹時投与（食前1時間または食後2時間）。肝銅コントロールまで継続（肝生検の銅定量で再評価）、多くは数ヶ月単位。低銅食と併用し、脱銅後は亜鉛維持療法を検討（Plumb's; ACVIM 2019 慢性肝炎コンセンサス）。",
                "notes": "Better GI tolerance than D-penicillamine. Do not give with food, mineral supplements or zinc at the same time (chelates dietary metals and loses efficacy). Monitor CBC and iron status on prolonged therapy.",
                "notes_ja": "D-ペニシラミンより消化器忍容性が高い。食事・ミネラルサプリ・亜鉛と同時投与しない（食餌中金属をキレートし効果が落ちる）。長期投与ではCBCと鉄状態をモニタリング。",
            },
        },
        "side_effects": "Occasional nausea/vomiting (less than penicillamine); iron deficiency anemia with prolonged use; rare cutaneous reactions",
        "side_effects_ja": "時に悪心・嘔吐（ペニシラミンより少ない）。長期投与で鉄欠乏性貧血。まれに皮膚反応",
        "contraindications": "Do not combine with D-penicillamine (no added benefit, additive metal depletion). Caution in pregnancy and pre-existing iron-deficiency anemia",
        "contraindications_ja": "D-ペニシラミンとの併用不可（上乗せ効果なく金属枯渇が相加）。妊娠中・既存の鉄欠乏性貧血では慎重投与",
        "drug_interactions": [
            {
                "drug": "Zinc supplements / mineral-containing antacids",
                "effect": "Mutual chelation in the gut — separate administration by at least 2 hours; zinc maintenance is started only after active chelation ends",
                "effect_ja": "消化管内で相互にキレート — 最低2時間あけて投与。亜鉛維持療法は活動性キレート終了後に開始する",
                "severity": "moderate",
            },
            {
                "drug": "D-penicillamine",
                "effect": "Alternative chelators — use one at a time; trientine replaces penicillamine on intolerance",
                "effect_ja": "代替キレート剤同士 — 同時併用せずどちらか一方を使用。トリエンチンは不耐時のペニシラミン代替",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "olopatadine_ophthalmic",
        "search_aliases": [
            "オロパタジン",
            "オロパタジン点眼",
            "パタノール",
            "Olopatadine",
            "Patanol",
        ],
        "name": "Olopatadine 0.1% Ophthalmic",
        "name_ja": "オロパタジン0.1%点眼（パタノール）",
        "category": "ophthalmic",
        "mechanism": "Dual-action topical anti-allergic: selective H1-receptor antagonist plus mast-cell stabiliser. Blocks histamine-mediated itching/hyperemia and prevents further mast-cell degranulation on the ocular surface — used for allergic conjunctivitis in dogs and cats (veterinary-adopted human ophthalmic).",
        "mechanism_ja": "二重作用の抗アレルギー点眼薬: 選択的H1受容体拮抗＋マスト細胞安定化。ヒスタミン介在性の掻痒・充血を遮断し、眼表面のマスト細胞脱顆粒の進行を防ぐ — 犬猫のアレルギー性結膜炎に用いる（獣医転用が定着したヒト用点眼薬）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Allergic conjunctivitis: 1 drop per affected eye q12h. Reassess at 1-2 weeks; continue seasonally for atopic dogs with ocular signs.",
                "dosage_ja": "アレルギー性結膜炎: 患眼に1滴 12時間毎。1-2週で再評価。眼症状を伴うアトピー犬では季節性に継続。",
                "notes": "Symptomatic therapy — pursue the underlying allergy (atopy, ASIT, flea control). Exclude infectious/ulcerative causes (fluorescein) before chronic anti-allergic therapy.",
                "notes_ja": "対症療法 — 基礎のアレルギー（アトピー、減感作療法、ノミ対策）へのアプローチを並行する。慢性投与の前にフルオレセインで感染性・潰瘍性の原因を除外。",
            },
            "cat": {
                "safe": True,
                "dosage": "Allergic/eosinophilic conjunctivitis adjunct: 1 drop per affected eye q12h.",
                "dosage_ja": "アレルギー性・好酸球性結膜炎の補助: 患眼に1滴 12時間毎。",
                "notes": "In cats always consider herpetic disease first — FHV-1 keratoconjunctivitis needs antivirals, not antihistamines.",
                "notes_ja": "猫ではまずヘルペス性疾患を考慮 — FHV-1角結膜炎には抗ヒスタミンではなく抗ウイルス薬が必要。",
            },
        },
        "side_effects": "Transient stinging on instillation; rare local irritation/blepharitis",
        "side_effects_ja": "点眼時の一過性刺激感。まれに局所刺激・眼瞼炎",
        "contraindications": "Not for infectious conjunctivitis as sole therapy; do not use to mask undiagnosed red eye — rule out ulcer, glaucoma and uveitis first",
        "contraindications_ja": "感染性結膜炎への単独使用は不可。未診断の赤目の隠蔽に使わない — 潰瘍・緑内障・ぶどう膜炎をまず除外",
        "drug_interactions": [
            {
                "drug": "Other ophthalmic drops",
                "effect": "Separate different eye drops by at least 5 minutes to avoid washout",
                "effect_ja": "他の点眼薬とは5分以上間隔をあけて洗い流しを防ぐ",
                "severity": "info",
            },
        ],
    },
]
