"""Drug batch 43 – referenced-but-absent agents surfaced by the 2026-08 audit (11th sweep).

A context-aware katakana token sweep of disease treatment protocols,
cross-checked with the real text matcher (find_drugs_in_text), found two
agents that VetDict's own content instructs clinicians to use — with explicit
doses — yet were absent from the formulary (a third hit, ミコフェノール酸
モフェチル/MMF with 48 references, turned out to be present already under id
"mycophenolate" — only its bare-stem spelling "ミコフェノール酸" failed to
resolve, fixed via _KATAKANA_VARIANT_ALIASES instead):

  - シタラビン (cytarabine, Ara-C): referenced 8 times. The standard
    steroid-adjunct for meningoencephalitis of unknown origin (MUO/GME/NME/
    NLE) — "50 mg/m² SC q12h × 2日間、4週毎" appears verbatim in the dog and
    cat neurology entries.
  - イミキモド (imiquimod 5% cream): referenced 5 times, all with dosing —
    equine sarcoid and aural plaques ("イミキモド5%クリーム外用q48h"),
    feline SCC in situ ("週3回 × 4-16週、奏効率40-70%"). Directly relevant
    to the developer's equine caseload (sarcoid is the most common equine
    tumour).

References:
  - Plumb's Veterinary Drug Handbook, 10th ed — cytarabine handling and
    myelosuppression nadir.
  - Zarfoss M et al. 2006 JSAP; Lowrie M et al. 2013 Vet Rec —
    cytarabine 50 mg/m² SC q12h × 2 days repeated q3-4 weeks (or 200 mg/m²
    CRI over 8-24 h) with prednisolone for MUO; crosses the blood-brain
    barrier, unlike most cytotoxics.
  - Nogueira SAF et al. 2006 Vet Dermatol — imiquimod 5% cream 3×/week for
    equine sarcoid: >75% reduction in 80% of treated tumours; marked local
    inflammation expected.
  - Torres SMF et al. 2010 Vet Dermatol — imiquimod for equine aural
    plaques: effective but application is painful; sedation often required.
  - Gill VL et al. 2008 Vet Dermatol — imiquimod 5% cream in cats with
    Bowenoid in situ carcinoma: partial/complete responses in most cats;
    monitor for local irritation and prevent grooming ingestion.
"""

DRUGS_BATCH_43: list[dict] = [
    {
        "id": "cytarabine",
        "search_aliases": [
            "シタラビン",
            "Ara-C",
            "アラシー",
            "キロサイド",
            "Cytarabine",
            "Cytosine arabinoside",
        ],
        "name": "Cytarabine (Ara-C)",
        "name_ja": "シタラビン（Ara-C）",
        "category": "antineoplastics",
        "mechanism": "Pyrimidine nucleoside analog. Intracellularly phosphorylated to ara-CTP, which inhibits DNA polymerase and is incorporated into DNA, arresting S-phase cells. Crosses the blood-brain barrier — the property that makes it the standard cytotoxic adjunct for meningoencephalitis of unknown origin (MUO/GME/NME/NLE) and CNS lymphoma, unlike most chemotherapeutics.",
        "mechanism_ja": "ピリミジンヌクレオシドアナログ。細胞内でリン酸化されてara-CTPとなり、DNAポリメラーゼを阻害しDNAに取り込まれてS期細胞を停止させる。血液脳関門を通過する — この特性により、多くの抗がん薬と異なり、原因不明性髄膜脳炎（MUO/GME/NME/NLE）およびCNSリンパ腫に対する標準的な細胞傷害性補助薬となっている。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "MUO (GME/NME/NLE), with prednisolone: 50 mg/m² SC q12h × 2 days (4 doses = 200 mg/m²/cycle), repeat q3-4 weeks with gradual interval extension on response (Zarfoss 2006). Alternative: 200 mg/m² IV CRI over 8-24 h per cycle (Lowrie 2013). CNS lymphoma: same cycle as adjunct to CHOP.",
                "dosage_ja": "MUO（GME/NME/NLE）にプレドニゾロン併用: 50 mg/m² 皮下 12時間毎 × 2日間（4回=200 mg/m²/サイクル）、3-4週毎に反復し反応に応じて間隔を漸延（Zarfoss 2006）。代替: 200 mg/m² を8-24時間かけて静脈内CRI（Lowrie 2013）。CNSリンパ腫: CHOPへの上乗せとして同サイクル。",
                "notes": "Myelosuppression nadir 5-7 days after dosing — CBC before each cycle (defer if neutrophils <2,500/µL). Cytotoxic: wear gloves, dedicated sharps disposal.",
                "notes_ja": "骨髄抑制の最下点は投与5-7日後 — 各サイクル前にCBC（好中球<2,500/µLなら延期）。細胞傷害性薬: 手袋着用・専用廃棄。",
            },
            "cat": {
                "safe": True,
                "dosage": "Steroid-refractory meningoencephalitis / polyneuropathy: 50 mg/m² SC q12h × 2 days, repeat q3-4 weeks. CNS lymphoma: 50-100 mg/m² SC per cycle as adjunct.",
                "dosage_ja": "ステロイド不応性髄膜脳炎・多発性神経障害: 50 mg/m² 皮下 12時間毎 × 2日間、3-4週毎に反復。CNSリンパ腫: 補助として1サイクル 50-100 mg/m² 皮下。",
                "notes": "CBC before each cycle; feline marrow reserve is smaller — monitor closely.",
                "notes_ja": "各サイクル前にCBC。猫は骨髄予備能が小さい — 慎重にモニタリング。",
            },
        },
        "side_effects": "Myelosuppression (neutropenia nadir 5-7 days), GI upset (vomiting/diarrhea), local irritation at SC sites; rarely fever after administration",
        "side_effects_ja": "骨髄抑制（好中球最下点は5-7日後）、消化器症状（嘔吐・下痢）、皮下投与部位の局所刺激。まれに投与後発熱",
        "contraindications": "Pre-existing severe myelosuppression; active serious infection; pregnancy. Cytotoxic — safe-handling precautions mandatory (gloves; pregnant staff should not handle)",
        "contraindications_ja": "既存の重度骨髄抑制、重篤な活動性感染症、妊娠。細胞傷害性薬 — 安全取扱い必須（手袋着用。妊娠中のスタッフは取り扱わない）",
        "drug_interactions": [
            {
                "drug": "Prednisolone",
                "effect": "Standard MUO combination — cytarabine cycles allow steroid taper and improve survival vs steroid alone",
                "effect_ja": "MUOの標準併用 — シタラビンのサイクル投与でステロイド漸減が可能となり、単独より生存期間が改善",
                "severity": "info",
            },
            {
                "drug": "Other myelosuppressive chemotherapy",
                "effect": "Additive marrow toxicity — stagger nadirs and monitor CBC",
                "effect_ja": "骨髄毒性が相加的 — 最下点をずらしCBCを監視",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "imiquimod",
        "search_aliases": [
            "イミキモド",
            "イミキモド5%クリーム",
            "ベセルナ",
            "アルダラ",
            "Imiquimod",
            "Aldara",
        ],
        "name": "Imiquimod 5% Cream",
        "name_ja": "イミキモド5%クリーム",
        "category": "dermatological",
        "mechanism": "Topical toll-like receptor 7 (TLR7) agonist. Induces local interferon-α, TNF-α and other proinflammatory cytokines, recruiting an innate and cell-mediated immune response against virally infected and neoplastic cells — an immune response modifier rather than a direct cytotoxic. Used off-label in veterinary dermatology/oncology for papillomavirus-associated lesions (equine sarcoid, aural plaques) and superficial carcinoma in situ.",
        "mechanism_ja": "外用トル様受容体7（TLR7）アゴニスト。局所でインターフェロンα・TNF-α等の炎症性サイトカインを誘導し、ウイルス感染細胞・腫瘍細胞に対する自然免疫・細胞性免疫応答を動員する — 直接的な細胞傷害薬ではなく免疫応答調節薬。獣医領域ではパピローマウイルス関連病変（馬サルコイド・耳介プラーク）や表在性上皮内癌に適応外使用される。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Sarcoid (small/flat lesions or post-debulking): thin film 3×/week (or q48h) until resolution, typically 2-4 months — >75% reduction in 80% of tumours (Nogueira 2006). Aural plaques: q48h × 4-8 weeks; application is painful — sedation often required (Torres 2010).",
                "dosage_ja": "サルコイド（小型・扁平病変または減量術後）: 薄く週3回（または48時間毎）塗布、消退まで通常2-4ヶ月 — 80%の腫瘤で75%超の縮小（Nogueira 2006）。耳介プラーク: 48時間毎 × 4-8週。塗布時疼痛が強く鎮静を要することが多い（Torres 2010）。",
                "notes": "Marked local inflammation/erosion is expected and part of the mechanism — warn owners. Wear gloves for application. Do not use on large ulcerated masses.",
                "notes_ja": "顕著な局所炎症・びらんは想定内で作用機序の一部 — 飼い主に事前説明。塗布時は手袋着用。大型の潰瘍化腫瘤には用いない。",
            },
            "cat": {
                "safe": True,
                "dosage": "Bowenoid (SCC) in situ / actinic keratosis: thin film 3×/week × 4-16 weeks (response rate 40-70%, Gill 2008). Elizabethan collar until dry — prevent grooming ingestion.",
                "dosage_ja": "ボーエン様上皮内癌（SCC in situ）・日光角化症: 薄く週3回 × 4-16週（奏効率40-70%、Gill 2008）。乾くまでエリザベスカラー — グルーミングによる経口摂取を防ぐ。",
                "notes": "Local erythema/crusting common; withhold applications until settled if severe. Systemic signs (inappetence, neutropenia) reported with excessive use — apply thinly to limited areas.",
                "notes_ja": "局所紅斑・痂皮は高頻度。重度なら鎮静化まで休薬。過量塗布で全身徴候（食欲低下・好中球減少）の報告 — 限局部位に薄く塗布。",
            },
            "dog": {
                "safe": True,
                "dosage": "Viral papilloma / pigmented plaques (off-label, refractory cases): thin film 3×/week to limited lesions; prevent licking (collar).",
                "dosage_ja": "ウイルス性乳頭腫・色素性プラーク（適応外・難治例）: 限局病変に薄く週3回。舐め防止（カラー装着）。",
                "notes": "Evidence anecdotal in dogs; most papillomas regress spontaneously — reserve for persistent lesions.",
                "notes_ja": "犬でのエビデンスは逸話的。乳頭腫の多くは自然消退する — 遷延例に限って使用。",
            },
        },
        "side_effects": "Local erythema, erosion, crusting and pruritus at application site (expected); systemic flu-like signs, inappetence or neutropenia with over-application or ingestion",
        "side_effects_ja": "塗布部の紅斑・びらん・痂皮・掻痒（想定内の反応）。過量塗布や経口摂取で全身症状（倦怠・食欲低下・好中球減少）",
        "contraindications": "Do not apply to large ulcerated surfaces or mucous membranes; prevent ingestion (grooming) — Elizabethan collar in small animals; handler should wear gloves",
        "contraindications_ja": "大きな潰瘍面・粘膜には塗布しない。経口摂取（グルーミング）を防止 — 小動物ではエリザベスカラー。取り扱い者は手袋着用",
        "drug_interactions": [
            {
                "drug": "Topical corticosteroids",
                "effect": "Antagonize the intended local immune activation — avoid concurrent use on the same lesion",
                "effect_ja": "目的とする局所免疫活性化に拮抗 — 同一病変への併用は避ける",
                "severity": "moderate",
            },
        ],
    },
]
