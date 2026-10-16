"""Drug batch 79 – 2026-10 session (第71弾).

Otic (ear) combination products. Otitis externa is one of the most common
presenting problems in canine practice, yet the dictionary had no otic
products at all: the disease entries named Osurnia/Otomax/Posatex/Surolan
but none resolved, so a vet tapping the treatment had nowhere to land and
could not check label drop counts or the shared ear-drum warning.

All five are label-defined (dose = drops/tubes per ear, not mg/kg):
- Florfenicol + terbinafine + betamethasone acetate otic gel (Osurnia) —
  1 tube per ear, repeat once after 7 days (EU/US labels).
- Florfenicol + terbinafine + mometasone furoate otic solution (Claro;
  Neptra is the same three-ingredient class) — single 1 mL veterinarian-
  administered dose per ear, 30-day efficacy.
- Gentamicin + betamethasone valerate + clotrimazole otic ointment (Otomax)
  — 4 drops (<30 lb / ~13.6 kg) or 8 drops (>=30 lb) q12h x 7 days.
- Orbifloxacin + mometasone furoate + posaconazole otic suspension
  (Posatex) — 2 / 4 / 8 drops by weight band q24h x 7 days.
- Polymyxin B + miconazole + prednisolone acetate otic suspension
  (Surolan) — 5 drops q12h x 7 days; dogs and cats.

Shared class facts: confirm the tympanic membrane is intact before
instilling (aminoglycosides/chlorhexidine-type vehicles are ototoxic in the
middle ear); otitis has an underlying cause (atopy, food allergy,
endocrine, foreign body) that must be addressed; cytology guides the choice.

Evidence: product labels (DailyMed / EMA SPC); Paterson S. J Small Anim Pract 2016
(topical ear treatment); Nuttall T. Vet Rec 2016; Gotthelf LN. Small Animal
Ear Diseases 2nd ed.; Plumb's Veterinary Drug Handbook 10th ed.
"""

_TM_EN = (
    "Examine the ear canal and confirm the tympanic membrane is intact before use — "
    "do not use with a ruptured ear drum (risk of ototoxicity/vestibular signs). "
    "Use ear cytology to confirm cocci/rods/Malassezia, and address the primary cause "
    "(atopic dermatitis, food allergy, endocrine disease, foreign body) or recurrence is expected. "
)
_TM_JA = (
    "使用前に耳道を観察し鼓膜が正常であることを確認する — 鼓膜穿孔例には使用しない（耳毒性・前庭症状のリスク）。"
    "耳垢細胞診で球菌・桿菌・マラセチアを確認し、基礎疾患（アトピー性皮膚炎・食物アレルギー・内分泌疾患・異物）に"
    "対処しないと再発する。"
)


def _otic(id_, aliases, name, name_ja, mech, mech_ja, dog, cat, contra, contra_ja, se, se_ja, refs, ix=None):
    return {
        "id": id_,
        "search_aliases": aliases,
        "name": name,
        "name_ja": name_ja,
        "category": "dermatological",
        "no_component_index": True,
        "routes": ["otic"],
        "routes_ja": ["耳用（点耳）"],
        "mechanism": mech,
        "mechanism_ja": mech_ja,
        "species_info": {"dog": dog, "cat": cat},
        "contraindications": contra,
        "contraindications_ja": contra_ja,
        "side_effects": se,
        "side_effects_ja": se_ja,
        "drug_interactions": ix or [],
        "references": refs,
    }


_CAT_NOT_LABELED = {
    "safe": False,
    "dosage": "Not labelled for cats — use a feline-labelled otic product (e.g. polymyxin B/miconazole/prednisolone) or one chosen on cytology.",
    "dosage_ja": "猫には適応がない（犬用ラベル）— 猫に適応のある点耳薬（ポリミキシンB・ミコナゾール・プレドニゾロン配合等）か細胞診に基づく製剤を用いる。",
    "notes": "Feline ear canals and safety data differ; cats are also prone to Otodectes and polyps — examine before treating.",
    "notes_ja": "猫は耳道構造と安全性データが異なる。耳ダニ・炎症性ポリープも多いため治療前に診察する。",
}

DRUGS_BATCH_79 = [
    _otic(
        "florfenicol_terbinafine_betamethasone_otic",
        ["オスルニア", "Osurnia", "osurnia", "フロルフェニコール・テルビナフィン・ベタメタゾン"],
        "Florfenicol / Terbinafine / Betamethasone acetate otic gel (Osurnia)",
        "フロルフェニコール・テルビナフィン・ベタメタゾン酢酸エステル点耳ゲル（オスルニア）",
        "Florfenicol (bacteriostatic amphenicol: staphylococci) + terbinafine (allylamine antifungal: Malassezia) + betamethasone acetate (anti-inflammatory). The gel coats the canal and releases drug for about a week, so only two clinic-applied doses are needed.",
        "フロルフェニコール（静菌性アンフェニコール系: ブドウ球菌）＋テルビナフィン（アリルアミン系抗真菌薬: マラセチア）＋ベタメタゾン酢酸エステル（抗炎症）。ゲルが耳道を覆い約1週間薬剤を放出するため、院内での2回投与で治療が完了する。",
        {
            "safe": True,
            "dosage": "Clean and dry the ear, then instil 1 tube (1 mL) per affected ear; repeat once after 7 days (2 doses total). Dogs only.",
            "dosage_ja": "耳を洗浄・乾燥させた後、患耳1つにつきチューブ1本（1 mL）を注入し、7日後に1回再投与する（計2回）。犬のみ。",
            "notes": _TM_EN
            + "Avoid ear cleaning during the treatment period so the gel is not removed (follow the label). Avoid contact with the eyes — keratoconjunctivitis sicca and corneal ulcers have been reported. Head shaking right after application is common. Low owner burden makes it useful where twice-daily drops fail.",
            "notes_ja": _TM_JA
            + "治療期間中はゲルを除去しないよう耳洗浄を控える（ラベルに従う）。眼への付着を避ける（乾性角結膜炎・角膜潰瘍の報告あり）。投与直後の頭振りはよくみられる。飼い主の投薬負担が少なく、1日2回の点耳が続かない症例に有用。",
        },
        _CAT_NOT_LABELED,
        "Ruptured tympanic membrane; hypersensitivity to ingredients; demodicosis or generalised infection where corticosteroid is undesirable; not for breeding dogs (safety not established).",
        "鼓膜穿孔、成分過敏症、副腎皮質ステロイドが望ましくない毛包虫症・全身感染、繁殖犬（安全性未確立）。",
        [
            "Head shaking after application",
            "Ocular disorders if gel reaches the eye (KCS, corneal ulcer)",
            "Hearing loss / vestibular signs (rare)",
        ],
        ["投与後の頭振り", "眼への付着による眼障害（乾性角結膜炎・角膜潰瘍）", "聴覚低下・前庭症状（まれ）"],
        [
            "Osurnia (florfenicol/terbinafine/betamethasone acetate) otic gel — EMA SPC / US label",
            "Paterson S. Topical ear treatment — options, indications and limitations of current therapy. J Small Anim Pract 2016.",
        ],
    ),
    _otic(
        "florfenicol_terbinafine_mometasone_otic",
        ["クラロ", "Claro", "claro", "ネプトラ", "Neptra", "neptra", "フロルフェニコール・テルビナフィン・モメタゾン"],
        "Florfenicol / Terbinafine / Mometasone furoate otic solution (Claro, Neptra)",
        "フロルフェニコール・テルビナフィン・モメタゾン点耳液（クラロ／ネプトラ）",
        "Same antibacterial/antifungal pair as Osurnia with mometasone furoate as the glucocorticoid; formulated as a single veterinarian-administered dose that persists in the canal for about 30 days.",
        "オスルニアと同じ抗菌・抗真菌の組み合わせに副腎皮質ステロイドとしてモメタゾンフランカルボン酸エステルを配合。獣医師が1回投与し、耳道内に約30日間持続する製剤。",
        {
            "safe": True,
            "dosage": "Single dose: 1 mL (one dropperette) per affected ear, administered by the veterinarian after cleaning and drying. Efficacy assessed at 30 days. Dogs only.",
            "dosage_ja": "単回投与: 患耳1つにつき1 mL（1本）を、洗浄・乾燥後に獣医師が投与する。効果判定は30日後。犬のみ。",
            "notes": _TM_EN
            + "Post-marketing reports include hearing loss and vestibular signs — counsel owners and avoid in dogs with suspected TM rupture. Do not clean the ears for the duration of action unless directed. Ideal when daily medication is impossible.",
            "notes_ja": _TM_JA
            + "市販後に聴覚低下・前庭症状の報告があり、飼い主へ説明し鼓膜穿孔が疑われる犬には使用しない。指示がない限り作用期間中は耳洗浄を行わない。毎日の投薬が困難な症例に適する。",
        },
        _CAT_NOT_LABELED,
        "Ruptured tympanic membrane; hypersensitivity to ingredients; breeding, pregnant or lactating dogs (not evaluated).",
        "鼓膜穿孔、成分過敏症、繁殖・妊娠・授乳中の犬（評価されていない）。",
        [
            "Hearing loss / deafness (post-marketing reports)",
            "Vestibular signs (head tilt, ataxia)",
            "Head shaking, vomiting",
        ],
        ["聴覚低下・難聴（市販後報告）", "前庭症状（斜頸・運動失調）", "頭振り・嘔吐"],
        [
            "Claro (florfenicol, terbinafine, mometasone furoate) otic solution — US label",
            "Neptra (florfenicol, terbinafine hydrochloride, mometasone furoate) otic solution — US label / EMA SPC",
            "Nuttall T. Successful management of otitis externa. In Practice 2016.",
        ],
    ),
    _otic(
        "gentamicin_betamethasone_clotrimazole_otic",
        [
            "オトマックス",
            "Otomax",
            "otomax",
            "モメタマックス",
            "Mometamax",
            "mometamax",
            "ゲンタマイシン・ベタメタゾン・クロトリマゾール点耳",
        ],
        "Gentamicin / Betamethasone valerate / Clotrimazole otic ointment (Otomax)",
        "ゲンタマイシン・ベタメタゾン・クロトリマゾール点耳軟膏（オトマックス）",
        "Gentamicin (aminoglycoside: staphylococci and many Pseudomonas) + clotrimazole (imidazole antifungal: Malassezia) + betamethasone valerate. The mometasone variant (Mometamax) uses the same gentamicin/clotrimazole pair with once-daily dosing.",
        "ゲンタマイシン（アミノグリコシド系: ブドウ球菌・多くの緑膿菌）＋クロトリマゾール（イミダゾール系抗真菌薬: マラセチア）＋ベタメタゾン吉草酸エステル。モメタゾン配合品（モメタマックス）は同じ組み合わせで1日1回投与。",
        {
            "safe": True,
            "dosage": "Otomax: dogs < 30 lb (~13.6 kg) 4 drops, >= 30 lb 8 drops into the ear canal q12h for 7 days. Mometamax variant: same drop counts q24h for 7 days.",
            "dosage_ja": "オトマックス: 体重30ポンド（約13.6 kg）未満は4滴、それ以上は8滴を耳道に1日2回・7日間。モメタマックス（モメタゾン配合）は同じ滴数を1日1回・7日間。",
            "notes": _TM_EN
            + "Aminoglycoside: ototoxic if the drum is ruptured — this is the classic product to avoid with otitis media. Pseudomonas otitis often needs culture-guided therapy and a Tris-EDTA flush. Massage the base of the ear after instillation.",
            "notes_ja": _TM_JA
            + "アミノグリコシド系のため鼓膜穿孔時は耳毒性 — 中耳炎で避けるべき代表的製剤。緑膿菌性外耳炎は培養に基づく治療とTris-EDTA洗浄を要することが多い。点耳後に耳の付け根をマッサージする。",
        },
        _CAT_NOT_LABELED,
        "Ruptured tympanic membrane / otitis media; hypersensitivity to ingredients; pregnancy and breeding dogs (corticosteroid).",
        "鼓膜穿孔・中耳炎、成分過敏症、妊娠犬・繁殖犬（副腎皮質ステロイド）。",
        [
            "Ototoxicity / hearing loss (with ruptured drum)",
            "Local irritation",
            "Systemic corticosteroid effects with prolonged use",
        ],
        ["耳毒性・聴覚低下（鼓膜穿孔時）", "局所刺激", "長期使用時の全身性ステロイド作用"],
        [
            "Otomax (gentamicin sulfate, betamethasone valerate, clotrimazole) otic ointment — US label",
            "Mometamax (gentamicin, mometasone furoate, clotrimazole) otic suspension — US label",
            "Gotthelf LN. Small Animal Ear Diseases, 2nd ed. Elsevier.",
        ],
        [
            {
                "drug": "Other ototoxic drugs (aminoglycosides, loop diuretics)",
                "effect": "Additive ototoxicity if absorbed through a ruptured drum",
                "effect_ja": "鼓膜穿孔から吸収された場合に耳毒性が相加",
                "severity": "moderate",
            }
        ],
    ),
    _otic(
        "orbifloxacin_mometasone_posaconazole_otic",
        ["ポサテックス", "Posatex", "posatex", "オルビフロキサシン・モメタゾン・ポサコナゾール"],
        "Orbifloxacin / Mometasone furoate / Posaconazole otic suspension (Posatex)",
        "オルビフロキサシン・モメタゾン・ポサコナゾール点耳懸濁液（ポサテックス）",
        "Orbifloxacin (fluoroquinolone: staphylococci, Pseudomonas) + posaconazole (triazole: Malassezia) + mometasone furoate.",
        "オルビフロキサシン（フルオロキノロン系: ブドウ球菌・緑膿菌）＋ポサコナゾール（トリアゾール系: マラセチア）＋モメタゾンフランカルボン酸エステル。",
        {
            "safe": True,
            "dosage": "Once daily for 7 days: dogs < 2 kg 2 drops, 2-15 kg 4 drops, >= 15 kg 8 drops per affected ear.",
            "dosage_ja": "1日1回・7日間: 体重2 kg未満は2滴、2-15 kgは4滴、15 kg以上は8滴を患耳に点耳。",
            "notes": _TM_EN
            + "Reserve fluoroquinolone otics for rods/Pseudomonas on cytology rather than first-line cocci infections (antimicrobial stewardship).",
            "notes_ja": _TM_JA
            + "抗菌薬適正使用の観点から、フルオロキノロン系点耳薬は細胞診で桿菌・緑膿菌が見られる症例に温存し、球菌性の初回治療には用いない。",
        },
        _CAT_NOT_LABELED,
        "Ruptured tympanic membrane; hypersensitivity to ingredients; pregnant or breeding dogs.",
        "鼓膜穿孔、成分過敏症、妊娠犬・繁殖犬。",
        ["Local irritation, head shaking", "Hearing impairment (rare)"],
        ["局所刺激・頭振り", "聴覚障害（まれ）"],
        [
            "Posatex (orbifloxacin, mometasone furoate, posaconazole) otic suspension — EMA SPC / US label",
            "Paterson S. J Small Anim Pract 2016 (topical ear therapy; reserving fluoroquinolones).",
        ],
    ),
    _otic(
        "polymyxin_miconazole_prednisolone_otic",
        [
            "スロラン",
            "Surolan",
            "surolan",
            "ポリミキシンB・ミコナゾール・プレドニゾロン",
            "ポリミキシン・ミコナゾール・プレドニゾロン配合点耳",
        ],
        "Polymyxin B / Miconazole / Prednisolone acetate otic suspension (Surolan)",
        "ポリミキシンB・ミコナゾール・プレドニゾロン配合点耳液（スロラン）",
        "Polymyxin B (Gram-negative incl. Pseudomonas) + miconazole (Malassezia; also some anti-staphylococcal activity) + prednisolone acetate. Also acaricidal by suffocation against Otodectes.",
        "ポリミキシンB（緑膿菌を含むグラム陰性菌）＋ミコナゾール（マラセチア、一部の抗ブドウ球菌作用）＋プレドニゾロン酢酸エステル。耳ダニ（ミミヒゼンダニ）にも物理的な殺ダニ作用がある。",
        {
            "safe": True,
            "dosage": "5 drops into the affected ear q12h for 7 days (shake well).",
            "dosage_ja": "よく振ってから患耳に5滴を1日2回・7日間点耳。",
            "notes": _TM_EN + "Polymyxin B is ototoxic in the middle ear.",
            "notes_ja": _TM_JA + "ポリミキシンBは中耳に入ると耳毒性がある。",
        },
        {
            "safe": True,
            "dosage": "5 drops into the affected ear q12h for 7 days (shake well).",
            "dosage_ja": "よく振ってから患耳に5滴を1日2回・7日間点耳。",
            "notes": "Labelled for cats. In cats, examine for Otodectes and inflammatory polyps first; for ear mites a systemic/spot-on acaricide (selamectin, isoxazoline) treats all in-contact animals. "
            + "Confirm the ear drum is intact.",
            "notes_ja": "猫に適応がある。猫ではまず耳ダニと炎症性ポリープを確認し、耳ダニには同居動物全頭へスポットオン/全身性駆除薬（セラメクチン・イソキサゾリン系）を用いる。鼓膜が正常であることを確認する。",
        },
        "Ruptured tympanic membrane; hypersensitivity to ingredients.",
        "鼓膜穿孔、成分過敏症。",
        ["Ototoxicity (with ruptured drum)", "Local irritation"],
        ["耳毒性（鼓膜穿孔時）", "局所刺激"],
        [
            "Surolan (miconazole nitrate, polymyxin B sulfate, prednisolone acetate) — EMA SPC (dogs and cats)",
            "Paterson S. Topical ear treatment. J Small Anim Pract 2016.",
        ],
    ),
]
