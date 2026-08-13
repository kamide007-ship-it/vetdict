"""Drug batch 35 – referenced-but-absent agents surfaced by the 2026-08 audit (3rd sweep).

A katakana/English token-frequency sweep of disease treatment protocols in
diseases_all_species.json plus the antidote cross-reference audit found 15
agents that VetDict's own content instructs clinicians to use — with explicit
doses — but the formulary did not carry:

  - Pralidoxime (2-PAM)   — 184 treatment references (organophosphate toxicosis
                            standard antidote alongside atropine), absent.
  - Regular insulin       — 16 references with doses (DKA CRI protocols,
                            hyperkalemia shifting in blocked cats/AKI/Addisonian
                            crisis) yet only the long/intermediate-acting
                            insulins were carried.
  - Triamcinolone         — 31 references (equine intra-articular standard,
                            intralesional derm use).
  - Imidocarb dipropionate— 22 references (large-Babesia standard of care,
                            equine piroplasmosis, Hepatozoon canis).
  - Succimer (DMSA)       — 12 references (oral chelation for avian/ferret lead
                            and zinc toxicosis); only CaEDTA was carried.
  - Cidofovir 0.5% oph.   — 11 references (FHV-1 q12h topical antiviral).
  - Albendazole           — 9 references (E. cuniculi alternative, giardiasis);
                            carries myelosuppression/teratogenicity warnings.
  - Triclabenzadole       — 8 references (Fasciola drug of choice incl.
                            immature flukes).
  - Enilconazole          — 5 references (Imaverol topical dermatophytosis
                            rinse for dogs/horses; feline grooming-ingestion
                            caution).
  - Flurbiprofen 0.03%    — 5 references (topical ophthalmic NSAID, uveitis).
  - Oseltamivir           — 4 references (ferret influenza; canine parvo use
                            explicitly flagged as lacking evidence).
  - Esmolol               — 3 references (ultra-short beta-1 blocker for SVT
                            diagnosis/rate control, avian methylxanthine
                            toxicosis).
  - Idoxuridine 0.1% oph. — 3 references (FHV-1 topical antiviral, compounded).
  - Dimercaprol (BAL)     — 2 references (arsenic/mercury chelation) —
                            completes the heavy-metal antidote set (CaEDTA,
                            succimer, penicillamine, BAL).
  - Celecoxib             — the documented empirical COX-2 inhibitor for avian
                            bornavirus / PDD (Dahlhausen 2002); referenced by
                            the corrected encephalitis/PDD protocols.

References:
  - Plumb's Veterinary Drug Handbook, 10th ed.
  - Carpenter's Exotic Animal Formulary, 6th ed.
  - Peterson ME, Talcott PA. Small Animal Toxicology, 3rd ed — pralidoxime,
    dimercaprol, succimer protocols.
  - Macintire DK. JAVMA 1993;202(8):1266-1272 — low-dose IM/IV regular insulin
    protocols for canine DKA.
  - Nelson RW, Couto CG. Small Animal Internal Medicine, 6th ed — DKA regular
    insulin CRI 0.05-0.1 U/kg/h, hyperkalemia insulin/dextrose shifting.
  - McKenzie HC. Vet Clin North Am Equine Pract 2011;27(1):59-72 — equine
    hyperlipemia insulin therapy.
  - Baneth G. Vet Parasitol 2011;181(1):3-11 — imidocarb for canine babesiosis
    and Hepatozoon canis.
  - Wise LN et al. JVIM 2013;27(6):1334-1346 — equine piroplasmosis (imidocarb
    2.2 mg/kg B. caballi / 4 mg/kg q72h x4 T. equi; donkey sensitivity).
  - Fontenelle JP et al. AJVR 2008;69(2):289-293 — topical cidofovir 0.5% q12h
    for experimental FHV-1 (reduced shedding and clinical disease).
  - Denver MC et al. JAVMA 2000;216(6):879-882 — succimer in cockatiels
    (lead toxicosis).
  - Frick TW et al. / Villar D et al. Vet Hum Toxicol 1996 — methylxanthine
    (caffeine/theobromine) toxicosis beta-blocker management.
  - McCluskey MJ, Kavenagh PB. Equine intra-articular triamcinolone use
    (Equine Vet J 2004;36(1)) and Ferris DJ et al. AAEP proceedings —
    IA corticosteroid practice patterns.
  - Savigny MR, Macintire DK. J Vet Emerg Crit Care 2010;20(1):132-142 —
    oseltamivir in canine parvoviral enteritis (limited/inconclusive benefit).
  - Gelatt KN. Veterinary Ophthalmology, 6th ed — flurbiprofen/idoxuridine
    topical protocols.
"""

from __future__ import annotations

DRUGS_BATCH_35: list[dict] = [
    {
        "id": "pralidoxime",
        "search_aliases": ["2-PAM", "プラリドキシム"],
        "name": "Pralidoxime Chloride (2-PAM)",
        "name_ja": "プラリドキシム（2-PAM、パム）",
        "category": "miscellaneous",
        "mechanism": (
            "Oxime cholinesterase reactivator. Removes the organophosphate moiety "
            "from phosphorylated acetylcholinesterase, restoring enzyme activity "
            "at nicotinic and muscarinic synapses. Must be given before the "
            "enzyme-OP bond 'ages' (becomes irreversible), so it is most effective "
            "within 24-48 h of exposure. Treats the nicotinic signs (tremors, "
            "weakness) that atropine cannot reverse."
        ),
        "mechanism_ja": (
            "オキシム系コリンエステラーゼ再賦活薬。有機リンによりリン酸化された"
            "アセチルコリンエステラーゼからリン酸基を除去し酵素活性を回復させる。"
            "酵素-有機リン結合が「エージング」（不可逆化）する前の投与が必須で、"
            "曝露後24-48時間以内が最も有効。アトロピンでは拮抗できない"
            "ニコチン様症状（振戦・脱力）に有効。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "20 mg/kg IM or slow IV (over 15-30 min) q8-12h, with atropine "
                    "(0.1-0.2 mg/kg, ¼ IV rest IM/SC) for muscarinic signs. Continue "
                    "until nicotinic signs resolve; discontinue if no response after "
                    "24-36 h (aged enzyme)."
                ),
                "dosage_ja": (
                    "20 mg/kg 筋注または緩徐静注（15-30分かけて）q8-12h。ムスカリン様症状には"
                    "アトロピン（0.1-0.2 mg/kg、¼を静注・残りを筋注/皮下）併用。"
                    "ニコチン様症状の消失まで継続。24-36時間で無反応なら中止（酵素エージング）。"
                ),
                "notes": (
                    "Give as early as possible — efficacy falls sharply once the "
                    "AChE-OP complex ages. Not a substitute for atropine; the two are "
                    "complementary (atropine = muscarinic, 2-PAM = nicotinic)."
                ),
                "notes_ja": (
                    "可及的早期に投与 — AChE-有機リン複合体のエージング後は効果が急減する。"
                    "アトロピンの代替ではなく相補的併用（アトロピン=ムスカリン様、2-PAM=ニコチン様）。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": "20 mg/kg IM or slow IV q8-12h with atropine, as for dogs.",
                "dosage_ja": "20 mg/kg 筋注または緩徐静注 q8-12h（犬と同様にアトロピン併用）。",
                "notes": (
                    "Cats are prone to chlorpyrifos toxicosis with delayed/chronic "
                    "signs; 2-PAM courses may need to be longer."
                ),
                "notes_ja": (
                    "猫はクロルピリホス中毒で遅発性・慢性経過を取りやすく、2-PAM投与期間が長くなることがある。"
                ),
            },
            "horse": {
                "safe": True,
                "dosage": "20 mg/kg slow IV q8-12h (dilute; give over 15-30 min) with atropine.",
                "dosage_ja": "20 mg/kg 緩徐静注 q8-12h（希釈し15-30分かけて投与、アトロピン併用）。",
                "notes": "Rapid IV bolus causes tachycardia, muscle rigidity, transient weakness.",
                "notes_ja": "急速静注は頻脈・筋硬直・一過性脱力を起こすため禁止。",
            },
            "bird": {
                "safe": True,
                "dosage": "10-20 mg/kg IM q8-12h (Carpenter) with atropine 0.2-0.5 mg/kg.",
                "dosage_ja": "10-20 mg/kg 筋注 q8-12h（Carpenter準拠）、アトロピン 0.2-0.5 mg/kg 併用。",
                "notes": "Raptors and waterfowl with OP exposure from treated fields/carcasses.",
                "notes_ja": "農薬処理圃場・汚染死骸経由の猛禽・水禽の有機リン曝露に使用。",
            },
        },
        "side_effects": (
            "Rapid IV: tachycardia, laryngospasm, muscle rigidity, transient "
            "neuromuscular blockade. Pain at IM injection site."
        ),
        "side_effects_ja": ("急速静注で頻脈・喉頭痙攣・筋硬直・一過性神経筋遮断。筋注部位の疼痛。"),
        "contraindications": (
            "Carbamate toxicosis is a relative contraindication (reactivation is "
            "unnecessary — carbamate-AChE binding is spontaneously reversible — and "
            "2-PAM is reported to worsen carbaryl toxicosis). Do not use without "
            "atropine coverage in symptomatic patients."
        ),
        "contraindications_ja": (
            "カーバメート中毒は相対的禁忌（カーバメート-AChE結合は自然可逆性で再賦活不要。"
            "カルバリル中毒では悪化の報告あり）。症状のある患者ではアトロピン併用なしで使用しない。"
        ),
        "drug_interactions": [
            {
                "drug": "Atropine",
                "effect": (
                    "Intended combination for organophosphate toxicosis — atropine "
                    "controls muscarinic signs while 2-PAM reactivates AChE."
                ),
                "effect_ja": (
                    "有機リン中毒での意図的併用 — アトロピンがムスカリン様症状を抑え、2-PAMがAChEを再賦活する。"
                ),
            },
            {
                "drug": "Morphine",
                "effect": "Avoid in OP toxicosis; respiratory depression is additive.",
                "effect_ja": "有機リン中毒では回避 — 呼吸抑制が相加的。",
            },
        ],
    },
    {
        "id": "insulin_regular",
        "search_aliases": ["速効型インスリン", "ヒューマリンR"],
        "name": "Regular Insulin (Humulin R / Novolin R)",
        "name_ja": "レギュラーインスリン（速効型、ヒューマリンR/ノボリンR）",
        "category": "endocrine",
        "mechanism": (
            "Short-acting soluble (neutral) insulin. The only insulin suitable for "
            "IV use: onset within minutes IV, duration 1-4 h. Drives cellular "
            "glucose uptake and shifts potassium intracellularly (with glucose), "
            "which is why it is the emergency insulin for diabetic ketoacidosis "
            "CRIs and for hyperkalemia (urethral obstruction, AKI, Addisonian "
            "crisis)."
        ),
        "mechanism_ja": (
            "速効型（中性可溶性）インスリン。静脈内投与が可能な唯一のインスリンで、"
            "静注では数分で作用発現、持続1-4時間。細胞内グルコース取込を促進し、"
            "グルコースと共にカリウムを細胞内へ移動させる。このため糖尿病性ケトアシドーシス（DKA）の"
            "CRIおよび高カリウム血症（尿道閉塞・急性腎障害・アジソンクリーゼ）の救急用インスリンとなる。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "DKA CRI: 0.05-0.1 U/kg/h IV (commonly 2.2 U/kg/day in 250 mL "
                    "0.9% NaCl, run through 50 mL of tubing first — insulin adsorbs "
                    "to plastic); adjust to drop glucose 50-75 mg/dL/h; add dextrose "
                    "when glucose < 250 mg/dL. IM alternative (Macintire): 0.2 U/kg "
                    "IM initially, then 0.1 U/kg IM q1h. Hyperkalemia: 0.25-0.5 U/kg "
                    "IV once + dextrose 1-2 g per unit of insulin IV, then dextrose "
                    "CRI to prevent hypoglycemia."
                ),
                "dosage_ja": (
                    "DKAのCRI: 0.05-0.1 U/kg/時 静注（一般に2.2 U/kg/日を0.9%生食250 mLに希釈。"
                    "インスリンは輸液チューブに吸着するため先にチューブへ50 mL流して飽和させる）。"
                    "血糖降下速度 50-75 mg/dL/時を目標に調整し、血糖 < 250 mg/dLでブドウ糖を追加。"
                    "筋注法（Macintire）: 初回 0.2 U/kg 筋注、以後 0.1 U/kg 筋注 q1h。"
                    "高カリウム血症: 0.25-0.5 U/kg 静注 単回＋インスリン1単位あたりブドウ糖 1-2 g 静注、"
                    "その後は低血糖予防にブドウ糖CRI。"
                ),
                "notes": (
                    "Check glucose q1-2h and potassium/phosphorus q4-6h during DKA "
                    "CRI — insulin shifts K and P intracellularly; supplement both. "
                    "Do not start insulin until perfusion deficits and severe "
                    "hypokalemia (< 3.5 mEq/L) are being corrected."
                ),
                "notes_ja": (
                    "DKAのCRI中は血糖を1-2時間毎、カリウム・リンを4-6時間毎に測定 — "
                    "インスリンはKとPを細胞内へ移動させるため両方を補給。"
                    "灌流障害と重度低カリウム血症（< 3.5 mEq/L）の是正開始前にインスリンを開始しない。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": (
                    "DKA CRI: 0.05-0.1 U/kg/h IV as for dogs (commonly 1.1 U/kg/day "
                    "in 250 mL 0.9% NaCl). Hyperkalemia (blocked cat, AKI): 0.25-0.5 "
                    "U/kg IV + 50% dextrose 1-2 mL/kg IV (diluted), then dextrose "
                    "CRI 2.5-5% for 4-6 h."
                ),
                "dosage_ja": (
                    "DKAのCRI: 0.05-0.1 U/kg/時 静注（犬と同様。一般に1.1 U/kg/日を0.9%生食250 mLに希釈）。"
                    "高カリウム血症（尿道閉塞・AKI）: 0.25-0.5 U/kg 静注＋50%ブドウ糖 1-2 mL/kg 静注（希釈）、"
                    "その後2.5-5%ブドウ糖CRIを4-6時間継続。"
                ),
                "notes": (
                    "Calcium gluconate protects the myocardium immediately but does "
                    "not lower K — insulin/dextrose does the shifting. Monitor for "
                    "rebound hypoglycemia for at least 4-6 h after a shifting dose."
                ),
                "notes_ja": (
                    "グルコン酸カルシウムは心筋を即時保護するがKは下げない — "
                    "K降下はインスリン/ブドウ糖が担う。シフト用量投与後は最低4-6時間、"
                    "反跳性低血糖をモニタリング。"
                ),
            },
            "horse": {
                "safe": True,
                "dosage": (
                    "Hyperlipemia (ponies, miniature horses, donkeys): 0.05-0.1 "
                    "IU/kg/h IV CRI with dextrose (or 0.1-0.3 IU/kg SC q12-24h with "
                    "oral/IV glucose), titrated to triglycerides and glucose "
                    "(McKenzie 2011). Hyperkalemia (HYPP crisis adjunct): dextrose "
                    "± insulin under glucose monitoring."
                ),
                "dosage_ja": (
                    "高脂血症（ポニー・ミニチュアホース・ロバ）: 0.05-0.1 IU/kg/時 静注CRI＋ブドウ糖併用"
                    "（または 0.1-0.3 IU/kg 皮下 q12-24h＋経口/静注グルコース）。"
                    "トリグリセリドと血糖で用量調整（McKenzie 2011）。"
                    "高カリウム血症（HYPPクリーゼの補助）: 血糖監視下でブドウ糖±インスリン。"
                ),
                "notes": "Always co-administer a glucose source; monitor glucose q1-2h.",
                "notes_ja": "必ずグルコース源を併用し、血糖を1-2時間毎に測定。",
            },
            "ferret": {
                "safe": True,
                "dosage": (
                    "DKA (rare): 0.05 U/kg/h IV CRI with q1-2h glucose checks. NOT "
                    "for insulinoma patients (already hypoglycemic)."
                ),
                "dosage_ja": (
                    "DKA（稀）: 0.05 U/kg/時 静注CRI、血糖を1-2時間毎に測定。"
                    "インスリノーマ患者（既に低血糖）には使用しない。"
                ),
            },
        },
        "side_effects": (
            "Hypoglycemia (weakness, seizures), hypokalemia, hypophosphatemia "
            "(hemolysis in severe cases). Adsorption to IV tubing reduces delivered "
            "dose unless tubing is pre-saturated."
        ),
        "side_effects_ja": (
            "低血糖（脱力・痙攣）、低カリウム血症、低リン血症（重度では溶血）。"
            "輸液チューブへの吸着により、チューブを事前飽和しないと実投与量が低下する。"
        ),
        "contraindications": (
            "Hypoglycemia; insulinoma. Do not begin DKA insulin before addressing "
            "severe hypokalemia — insulin will drop potassium further and can cause "
            "fatal arrhythmias or respiratory muscle weakness."
        ),
        "contraindications_ja": (
            "低血糖、インスリノーマ。重度低カリウム血症の是正開始前にDKAのインスリンを開始しない — "
            "インスリンはカリウムをさらに低下させ、致死性不整脈や呼吸筋麻痺を起こしうる。"
        ),
        "drug_interactions": [
            {
                "drug": "Corticosteroids",
                "effect": "Antagonize insulin action (insulin resistance); higher doses needed.",
                "effect_ja": "インスリン作用に拮抗（インスリン抵抗性）。必要用量が増加。",
            },
            {
                "drug": "Beta-blockers",
                "effect": "May mask tachycardia of hypoglycemia and delay glucose recovery.",
                "effect_ja": "低血糖時の頻脈をマスクし、血糖回復を遅延させることがある。",
            },
            {
                "drug": "Potassium supplements",
                "effect": (
                    "Intended combination in DKA — insulin shifts K intracellularly, "
                    "so supplementation guided by q4-6h electrolytes is standard."
                ),
                "effect_ja": (
                    "DKAでの意図的併用 — インスリンがKを細胞内へ移動させるため、"
                    "4-6時間毎の電解質測定に基づく補給が標準。"
                ),
            },
        ],
    },
    {
        "id": "triamcinolone",
        "search_aliases": ["トリアムシノロン", "ケナコルト"],
        "name": "Triamcinolone Acetonide (Vetalog / Kenalog)",
        "name_ja": "トリアムシノロンアセトニド（ボアラ/ケナコルト）",
        "category": "corticosteroids",
        "mechanism": (
            "Intermediate-acting synthetic glucocorticoid (~5x hydrocortisone "
            "potency, negligible mineralocorticoid activity). The acetonide ester "
            "is poorly water-soluble, giving a depot effect after intra-articular "
            "or intralesional injection — the basis of its equine joint-therapy "
            "role."
        ),
        "mechanism_ja": (
            "中間作用型合成糖質コルチコイド（力価はヒドロコルチゾンの約5倍、"
            "鉱質コルチコイド活性はほぼなし）。アセトニドエステルは水に難溶で、"
            "関節内・病変内注射後にデポー効果を示す — 馬の関節治療での役割の基盤。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": (
                    "Intra-articular: 6-18 mg per joint (many clinicians cap the "
                    "total body dose at 18-20 mg per session); high-motion joints "
                    "(fetlock, carpus, coffin) and navicular bursa. Systemic: "
                    "0.02-0.04 mg/kg IM."
                ),
                "dosage_ja": (
                    "関節内: 1関節あたり 6-18 mg（1回の総投与量を18-20 mgまでに制限する"
                    "臨床医が多い）。高可動性関節（球節・腕節・蹄関節）およびナビキュラー包に使用。"
                    "全身投与: 0.02-0.04 mg/kg 筋注。"
                ),
                "notes": (
                    "Historical laminitis association is dose-dependent and debated; "
                    "avoid high total doses in ponies, EMS/PPID and previously "
                    "laminitic horses. Strict asepsis for IA injection; rest the "
                    "joint 1-2 weeks. Withdraw per competition rules (detectable "
                    "in synovial fluid/plasma for weeks)."
                ),
                "notes_ja": (
                    "蹄葉炎との関連は用量依存的で議論があるが、ポニー・EMS/PPID・蹄葉炎既往馬では"
                    "高総用量を回避。関節内注射は厳密な無菌操作で行い、注射後1-2週間は運動制限。"
                    "競技会規則に従った休薬期間を設定（滑液・血漿中に数週間検出される）。"
                ),
            },
            "dog": {
                "safe": True,
                "dosage": (
                    "0.1-0.2 mg/kg IM/SC (anti-inflammatory, ~7-15 day duration); "
                    "intralesional 1.2-1.8 mg per lesion (acral lick granuloma, "
                    "localized granulomas); topical 0.015% spray (Genesis) for "
                    "pruritus."
                ),
                "dosage_ja": (
                    "0.1-0.2 mg/kg 筋注/皮下（抗炎症、効果は約7-15日持続）。"
                    "病変内注射 1病変あたり1.2-1.8 mg（舐性肉芽腫・限局性肉芽腫）。"
                    "外用 0.015%スプレー（瘙痒）。"
                ),
                "notes": (
                    "Depot steroid — cannot be withdrawn once injected; prefer "
                    "shorter-acting oral steroids when daily titration is needed. "
                    "PU/PD, polyphagia and iatrogenic Cushing's with repeated use."
                ),
                "notes_ja": (
                    "デポーステロイドのため注射後の中止・回収は不可能 — 日々の用量調整が必要な場合は"
                    "短時間作用型経口ステロイドを優先。反復使用で多飲多尿・多食・医原性クッシング。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": (
                    "0.1-0.2 mg/kg IM/SC; intralesional for eosinophilic granuloma "
                    "complex refractory to systemic therapy."
                ),
                "dosage_ja": ("0.1-0.2 mg/kg 筋注/皮下。全身療法に不応の好酸球性肉芽腫群には病変内注射。"),
                "notes": (
                    "Cats tolerate glucocorticoids better than dogs but repeated depot "
                    "steroid injections are a diabetes mellitus risk factor."
                ),
                "notes_ja": ("猫は犬よりステロイド耐性が高いが、デポーステロイドの反復注射は糖尿病の危険因子。"),
            },
        },
        "side_effects": (
            "PU/PD, polyphagia, iatrogenic hyperadrenocorticism, GI ulceration, "
            "delayed wound healing, laminitis (horses, dose-dependent), diabetes "
            "mellitus (cats, repeated use), post-injection flare or septic "
            "arthritis (IA route)."
        ),
        "side_effects_ja": (
            "多飲多尿・多食、医原性副腎皮質機能亢進症、消化管潰瘍、創傷治癒遅延、"
            "蹄葉炎（馬、用量依存）、糖尿病（猫、反復使用）、関節内投与では"
            "注射後フレアや化膿性関節炎。"
        ),
        "contraindications": (
            "Septic joint (absolute for IA use), systemic fungal infection, GI "
            "ulceration, concurrent NSAID use without gastroprotection, diabetes "
            "mellitus, late pregnancy (abortion risk in mares)."
        ),
        "contraindications_ja": (
            "感染関節（関節内投与の絶対禁忌）、全身性真菌感染、消化管潰瘍、"
            "胃保護なしのNSAIDs併用、糖尿病、妊娠後期（馬では流産リスク）。"
        ),
        "drug_interactions": [
            {
                "drug": "NSAIDs",
                "effect": "Additive GI ulceration risk — avoid concurrent systemic use.",
                "effect_ja": "消化管潰瘍リスクが相加的 — 全身投与の併用は回避。",
            },
            {
                "drug": "Insulin",
                "effect": "Glucocorticoids antagonize insulin; diabetic patients destabilize.",
                "effect_ja": "糖質コルチコイドはインスリンに拮抗し、糖尿病患者の血糖コントロールを乱す。",
            },
            {
                "drug": "Amphotericin B",
                "effect": "Additive potassium wasting.",
                "effect_ja": "カリウム喪失が相加的。",
            },
        ],
    },
    {
        "id": "imidocarb",
        "search_aliases": ["イミドカルブ", "イミゾール"],
        "name": "Imidocarb Dipropionate (Imizol)",
        "name_ja": "イミドカルブジプロピオン酸塩（イミゾール）",
        "category": "antiparasitics",
        "mechanism": (
            "Aromatic diamidine antiprotozoal. Interferes with piroplasm nucleic "
            "acid metabolism and polyamine synthesis, clearing intraerythrocytic "
            "Babesia (large forms) and tissue stages of Hepatozoon canis. Also has "
            "anticholinesterase activity, which produces the characteristic "
            "cholinergic injection reaction."
        ),
        "mechanism_ja": (
            "芳香族ジアミジン系抗原虫薬。ピロプラズマの核酸代謝とポリアミン合成を阻害し、"
            "赤血球内のバベシア（大型種）と Hepatozoon canis の組織ステージを駆除する。"
            "抗コリンエステラーゼ活性も持ち、特徴的なコリン作動性の注射反応を起こす。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Large Babesia (B. canis/vogeli/rossi): 6.6 mg/kg IM or SC, "
                    "repeat once in 14 days. Hepatozoon canis: 5-6 mg/kg IM q14d "
                    "until gamonts clear. Small Babesia (B. gibsoni) responds poorly "
                    "— use atovaquone + azithromycin instead."
                ),
                "dosage_ja": (
                    "大型バベシア（B. canis/vogeli/rossi）: 6.6 mg/kg 筋注または皮下、14日後に再投与（計2回）。"
                    "Hepatozoon canis: 5-6 mg/kg 筋注 q14日、ガモント消失まで。"
                    "小型バベシア（B. gibsoni）には効果不良 — アトバコン＋アジスロマイシンを使用。"
                ),
                "notes": (
                    "Premedicate with atropine 0.02-0.04 mg/kg SC (or glycopyrrolate) "
                    "30 min before to blunt cholinergic signs (salivation, vomiting, "
                    "diarrhea, tremors). Painful IM injection — split large volumes."
                ),
                "notes_ja": (
                    "投与30分前にアトロピン 0.02-0.04 mg/kg 皮下（またはグリコピロレート）で前処置し、"
                    "コリン作動性症状（流涎・嘔吐・下痢・振戦）を軽減。"
                    "筋注は疼痛が強く、大容量は分割して注射。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": (
                    "Cytauxzoon felis (historical): 5 mg/kg IM, repeat in 14 days — "
                    "atovaquone 15 mg/kg q8h + azithromycin 10 mg/kg q24h x 10 d now "
                    "gives superior survival and is preferred. Feline babesiosis "
                    "(B. felis, southern Africa): primaquine is the drug of choice."
                ),
                "dosage_ja": (
                    "サイトークスゾーン症（歴史的治療）: 5 mg/kg 筋注、14日後に再投与 — "
                    "現在はアトバコン 15 mg/kg q8h＋アジスロマイシン 10 mg/kg q24h×10日の方が"
                    "生存率が高く第一選択。猫バベシア症（B. felis、南部アフリカ）はプリマキンが第一選択。"
                ),
                "notes": "Cholinergic premedication as for dogs.",
                "notes_ja": "犬と同様にコリン作動性症状の前処置を行う。",
            },
            "horse": {
                "safe": True,
                "dosage": (
                    "Babesia caballi: 2.2 mg/kg IM q24h x 2. Theileria equi "
                    "(clearance protocol): 4 mg/kg IM q72h x 4 doses (Wise 2013, "
                    "USDA protocol) — expect marked cholinergic signs at this dose."
                ),
                "dosage_ja": (
                    "Babesia caballi: 2.2 mg/kg 筋注 q24h×2回。Theileria equi（クリアランスプロトコル）: "
                    "4 mg/kg 筋注 q72h×4回（Wise 2013、USDAプロトコル） — "
                    "この用量では顕著なコリン作動性症状を想定しておく。"
                ),
                "notes": (
                    "DONKEYS AND MULES ARE HIGHLY SENSITIVE — the T. equi clearance "
                    "dose can be fatal in donkeys; use reduced doses and intensive "
                    "monitoring. Equine piroplasmosis is reportable in many countries."
                ),
                "notes_ja": (
                    "ロバ・ラバは高感受性 — T. equi クリアランス用量はロバで致死的となりうるため、"
                    "減量と集中モニタリングが必須。馬ピロプラズマ症は多くの国で届出伝染病。"
                ),
            },
        },
        "side_effects": (
            "Cholinergic signs (hypersalivation, lacrimation, vomiting, diarrhea, "
            "tremors) within minutes of injection; injection-site pain/swelling; "
            "hepatotoxicity and renal tubular injury at high/repeated doses."
        ),
        "side_effects_ja": (
            "注射後数分以内のコリン作動性症状（流涎・流涙・嘔吐・下痢・振戦）、"
            "注射部位の疼痛・腫脹、高用量・反復投与での肝毒性と腎尿細管障害。"
        ),
        "contraindications": (
            "Concurrent exposure to cholinesterase-inhibiting insecticides or drugs "
            "(organophosphates, carbamates) — additive anticholinesterase toxicity. "
            "Severe hepatic or renal failure. Donkey/mule dose reduction mandatory."
        ),
        "contraindications_ja": (
            "コリンエステラーゼ阻害性の殺虫剤・薬剤（有機リン・カーバメート）との併用 — "
            "抗コリンエステラーゼ毒性が相加的。重度の肝・腎不全。ロバ・ラバでは減量必須。"
        ),
        "drug_interactions": [
            {
                "drug": "Organophosphates",
                "effect": (
                    "Additive anticholinesterase toxicity — do not use imidocarb in "
                    "animals recently treated with OP/carbamate insecticides."
                ),
                "effect_ja": (
                    "抗コリンエステラーゼ毒性が相加的 — 有機リン/カーバメート系殺虫剤の"
                    "最近の使用歴がある動物には投与しない。"
                ),
            },
            {
                "drug": "Atropine",
                "effect": "Intended premedication to blunt cholinergic injection reactions.",
                "effect_ja": "コリン作動性注射反応を軽減するための意図的な前処置薬。",
            },
        ],
    },
    {
        "id": "succimer",
        "search_aliases": ["DMSA"],
        "name": "Succimer (DMSA, Chemet)",
        "name_ja": "サクシマー（DMSA、ケメット）",
        "category": "miscellaneous",
        "mechanism": (
            "Water-soluble dimercaptosuccinic acid chelator. Binds lead (and zinc, "
            "arsenic, mercury) into a stable complex excreted in urine. Orally "
            "bioavailable, does not significantly deplete essential minerals, and — "
            "unlike CaEDTA — does not enhance GI absorption of lead still present "
            "in the gut, so it can be started before all metal is removed."
        ),
        "mechanism_ja": (
            "水溶性のジメルカプトコハク酸キレート剤。鉛（および亜鉛・ヒ素・水銀）と安定な複合体を形成し"
            "尿中排泄させる。経口投与が可能で必須ミネラルの喪失が少なく、CaEDTAと異なり"
            "消化管内に残存する鉛の吸収を促進しないため、金属片の完全除去前でも開始できる。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10 mg/kg PO q8h x 5 days, then 10 mg/kg PO q12h x 2 weeks (lead).",
                "dosage_ja": "10 mg/kg 経口 q8h×5日、その後 10 mg/kg 経口 q12h×2週間（鉛中毒）。",
                "notes": (
                    "Confirm exposure source removed; recheck blood lead 2 weeks "
                    "after finishing the course (redistribution rebound)."
                ),
                "notes_ja": ("曝露源の除去を確認。投与終了2週間後に血中鉛を再検（再分布によるリバウンド）。"),
            },
            "cat": {
                "safe": True,
                "dosage": "10 mg/kg PO q8h x 5 days, then q12h x 2 weeks (lead).",
                "dosage_ja": "10 mg/kg 経口 q8h×5日、その後 q12h×2週間（鉛中毒）。",
            },
            "bird": {
                "safe": True,
                "dosage": (
                    "25-35 mg/kg PO q12h x 5 days per week, for 3-5 weeks or until "
                    "blood lead < 20 µg/dL (Denver 2000, cockatiels). Also effective "
                    "for zinc toxicosis."
                ),
                "dosage_ja": (
                    "25-35 mg/kg 経口 q12h、週5日投与を3-5週間、または血中鉛 < 20 µg/dLまで"
                    "（Denver 2000、オカメインコ）。亜鉛中毒にも有効。"
                ),
                "notes": (
                    "Narrow margin in birds — doses ≥ 80 mg/kg have caused deaths in "
                    "cockatiels; do not exceed the published range. Combine with "
                    "radiographic monitoring of metal densities and endoscopic/"
                    "surgical removal of particles."
                ),
                "notes_ja": (
                    "鳥では安全域が狭い — オカメインコで80 mg/kg以上の投与による死亡報告があり、"
                    "推奨用量域を超えないこと。X線での金属片モニタリングと内視鏡/外科的除去を併用。"
                ),
            },
            "ferret": {
                "safe": True,
                "dosage": "30 mg/kg PO q12h x 10 days (oral alternative/follow-on to CaEDTA).",
                "dosage_ja": "30 mg/kg 経口 q12h×10日（CaEDTAの経口代替/後続コース）。",
            },
        },
        "side_effects": (
            "GI upset (vomiting, anorexia), transient elevation of liver enzymes, "
            "sulfur odor. Deaths in birds at supratherapeutic doses."
        ),
        "side_effects_ja": (
            "消化器症状（嘔吐・食欲不振）、一過性の肝酵素上昇、硫黄臭。鳥では治療域超過用量での死亡報告。"
        ),
        "contraindications": (
            "Severe hepatic insufficiency (monitor enzymes). Not a substitute for "
            "removing the metallic foreign body — chelation without source removal "
            "leads to relapse."
        ),
        "contraindications_ja": (
            "重度の肝機能不全（肝酵素をモニタリング）。金属異物の除去の代替にはならない — "
            "曝露源を除去しないキレート療法は再発する。"
        ),
        "drug_interactions": [
            {
                "drug": "Calcium EDTA (CaNa2EDTA)",
                "effect": (
                    "Sequential use is common (parenteral CaEDTA acutely, oral DMSA "
                    "follow-on); concurrent use adds no benefit."
                ),
                "effect_ja": ("逐次使用が一般的（急性期は注射CaEDTA、後続コースは経口DMSA）。同時併用の利益はない。"),
            },
            {
                "drug": "Zinc supplements",
                "effect": "DMSA chelates zinc; separate supplementation from dosing.",
                "effect_ja": "DMSAは亜鉛もキレートするため、亜鉛補給とは投与時間を分ける。",
            },
        ],
    },
    {
        "id": "cidofovir_ophthalmic",
        "search_aliases": ["シドフォビル"],
        "name": "Cidofovir 0.5% Ophthalmic (compounded)",
        "name_ja": "シドフォビル0.5%点眼（院内調剤）",
        "category": "ophthalmic",
        "mechanism": (
            "Acyclic nucleotide phosphonate antiviral. Already monophosphorylated, "
            "so unlike acyclovir-class drugs it does not depend on viral thymidine "
            "kinase; its diphosphate inhibits viral DNA polymerase. Long "
            "intracellular half-life allows twice-daily topical dosing for feline "
            "herpesvirus-1 — the practical advantage over idoxuridine (q4-6h)."
        ),
        "mechanism_ja": (
            "非環状ヌクレオチドホスホネート系抗ウイルス薬。既にモノリン酸化されているため"
            "アシクロビル系と異なりウイルスのチミジンキナーゼに依存せず、"
            "二リン酸体がウイルスDNAポリメラーゼを阻害する。細胞内半減期が長く、"
            "猫ヘルペスウイルス1型に対し1日2回の点眼で足りる — イドクスウリジン（q4-6h）に対する実用上の利点。"
        ),
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": (
                    "1 drop of 0.5% solution in affected eye q12h for 10-21 days "
                    "(FHV-1 conjunctivitis/keratitis; Fontenelle 2008 — reduced viral "
                    "shedding and clinical scores in experimental infection)."
                ),
                "dosage_ja": (
                    "0.5%液を患眼に1滴 q12h、10-21日間（FHV-1結膜炎/角膜炎。Fontenelle 2008 — "
                    "実験感染でウイルス排出と臨床スコアの減少を確認）。"
                ),
                "notes": (
                    "Compounded preparation (no commercial veterinary ophthalmic). "
                    "Oral famciclovir is the systemic partner for severe disease. "
                    "Topical only — systemic cidofovir is nephrotoxic."
                ),
                "notes_ja": (
                    "院内調剤製剤（獣医用の市販点眼はない）。重症例では経口ファムシクロビルを全身併用。"
                    "点眼専用 — 全身投与のシドフォビルは腎毒性がある。"
                ),
            },
            "bird": {
                "safe": True,
                "dosage": (
                    "Topical on cutaneous/periocular poxvirus and papillomatous "
                    "lesions q12h (anecdotal/experimental; supportive care remains "
                    "primary for avian pox)."
                ),
                "dosage_ja": (
                    "皮膚・眼周囲のポックスウイルス病変や乳頭腫様病変に局所塗布 q12h"
                    "（逸話的/実験的報告。鳥ポックスの主体は依然として支持療法）。"
                ),
            },
        },
        "side_effects": (
            "Mild conjunctival irritation; rare punctal/nasolacrimal stenosis with prolonged use (reported in humans)."
        ),
        "side_effects_ja": ("軽度の結膜刺激。長期使用で稀に涙点/鼻涙管狭窄（ヒトで報告）。"),
        "contraindications": (
            "Do not administer systemically (nephrotoxic). Discontinue if corneal epithelial toxicity develops."
        ),
        "contraindications_ja": ("全身投与禁止（腎毒性）。角膜上皮毒性が出現したら中止。"),
        "drug_interactions": [
            {
                "drug": "Famciclovir",
                "effect": (
                    "Complementary — topical cidofovir + oral famciclovir is a "
                    "rational combination for severe FHV-1 ocular disease."
                ),
                "effect_ja": ("相補的 — 重症FHV-1眼疾患ではシドフォビル点眼＋ファムシクロビル経口の併用が合理的。"),
            }
        ],
    },
    {
        "id": "albendazole",
        "name": "Albendazole (Valbazen)",
        "name_ja": "アルベンダゾール（バルバゼン）",
        "category": "antiparasitics",
        "mechanism": (
            "Benzimidazole anthelmintic. Binds nematode/protozoal beta-tubulin, "
            "blocking microtubule polymerisation and glucose uptake. Broader "
            "anti-protozoal reach than fenbendazole (Giardia, microsporidia "
            "including Encephalitozoon), but also the most myelotoxic "
            "benzimidazole in companion animals."
        ),
        "mechanism_ja": (
            "ベンズイミダゾール系駆虫薬。線虫・原虫のβチューブリンに結合して微小管重合と"
            "グルコース取込を阻害する。フェンベンダゾールより抗原虫スペクトラムが広い"
            "（ジアルジア、Encephalitozoon を含む微胞子虫）が、伴侶動物では"
            "ベンズイミダゾール系の中で最も骨髄毒性が強い。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Giardia: 25 mg/kg PO q12h x 2-4 days. Filaroides/Paragonimus: "
                    "25-50 mg/kg q12h x 10-21 days (monitor CBC weekly on long "
                    "courses)."
                ),
                "dosage_ja": (
                    "ジアルジア: 25 mg/kg 経口 q12h×2-4日。フィラロイデス/肺吸虫: "
                    "25-50 mg/kg q12h×10-21日（長期コースでは週1回CBCモニタリング）。"
                ),
                "notes": (
                    "Fenbendazole is preferred for routine use — albendazole has "
                    "caused aplastic anemia in dogs. Reserve for infections where the "
                    "broader spectrum is needed."
                ),
                "notes_ja": (
                    "通常はフェンベンダゾールを優先 — アルベンダゾールは犬で再生不良性貧血の報告がある。"
                    "広域スペクトラムが必要な感染に限定して使用。"
                ),
            },
            "cat": {
                "safe": False,
                "dosage": (
                    "Not recommended for routine use — aplastic anemia/pancytopenia "
                    "reported (Platynosomum courses at 50 mg/kg q24h caused "
                    "myelotoxicity); use fenbendazole or praziquantel instead."
                ),
                "dosage_ja": (
                    "通常使用は非推奨 — 再生不良性貧血/汎血球減少の報告あり"
                    "（Platynosomum 治療の50 mg/kg q24hで骨髄毒性）。"
                    "フェンベンダゾールまたはプラジカンテルを使用。"
                ),
                "notes": "If used at all: strict CBC monitoring q5-7 days.",
                "notes_ja": "やむを得ず使用する場合は5-7日毎の厳密なCBCモニタリング。",
            },
            "rabbit": {
                "safe": True,
                "dosage": (
                    "Encephalitozoon cuniculi (alternative): 20-30 mg/kg PO q24h x "
                    "7-14 days — fenbendazole 20 mg/kg q24h x 28 days remains first "
                    "line (Suter 2001). Monitor CBC; bone marrow suppression "
                    "reported in rabbits."
                ),
                "dosage_ja": (
                    "エンセファリトゾーン症（代替薬）: 20-30 mg/kg 経口 q24h×7-14日 — "
                    "第一選択は引き続きフェンベンダゾール 20 mg/kg q24h×28日（Suter 2001）。"
                    "CBCモニタリング必須。ウサギで骨髄抑制の報告あり。"
                ),
            },
            "bird": {
                "safe": True,
                "dosage": (
                    "5-10 mg/kg PO q24h x 3-5 days (ascarids, Capillaria); flagellates "
                    "10 mg/kg q12h x 5 days. Do not exceed — myelotoxicity and deaths "
                    "reported in columbiformes/psittacines at high doses."
                ),
                "dosage_ja": (
                    "5-10 mg/kg 経口 q24h×3-5日（回虫・毛細線虫）。鞭毛虫は 10 mg/kg q12h×5日。"
                    "増量禁止 — ハト目・オウム目で高用量による骨髄毒性・死亡の報告あり。"
                ),
            },
        },
        "side_effects": (
            "Bone marrow suppression (aplastic anemia, pancytopenia — dogs, cats, "
            "rabbits, birds), GI upset, hepatopathy. Teratogenic in early pregnancy."
        ),
        "side_effects_ja": (
            "骨髄抑制（再生不良性貧血・汎血球減少 — 犬・猫・ウサギ・鳥）、消化器症状、肝障害。妊娠初期には催奇形性。"
        ),
        "contraindications": (
            "Pregnancy (teratogenic), pre-existing cytopenias, hepatic failure. Cats: avoid for routine indications."
        ),
        "contraindications_ja": ("妊娠（催奇形性）、既存の血球減少、肝不全。猫では通常適応での使用を回避。"),
        "drug_interactions": [
            {
                "drug": "Dexamethasone",
                "effect": "May increase albendazole sulfoxide levels (human data).",
                "effect_ja": "アルベンダゾールスルホキシド濃度を上昇させることがある（ヒトデータ）。",
            },
            {
                "drug": "Praziquantel",
                "effect": "Increases albendazole metabolite exposure (human data); monitor on combined fluke protocols.",
                "effect_ja": "アルベンダゾール代謝物の曝露を増加（ヒトデータ）。吸虫併用プロトコルではモニタリング。",
            },
        ],
    },
    {
        "id": "enilconazole",
        "name": "Enilconazole (Imaverol) Topical",
        "name_ja": "エニルコナゾール（イマベロール）外用",
        "category": "antifungals",
        "mechanism": (
            "Topical imidazole antifungal. Inhibits fungal lanosterol "
            "14α-demethylase, depleting ergosterol. Also active as a vapor, which "
            "makes it useful for environmental decontamination. One of the few "
            "topicals with proven efficacy against dermatophytes in controlled "
            "studies (alongside lime sulfur and miconazole/chlorhexidine)."
        ),
        "mechanism_ja": (
            "外用イミダゾール系抗真菌薬。真菌のラノステロール14α-脱メチル化酵素を阻害し"
            "エルゴステロールを枯渇させる。蒸気としても活性があり環境除染にも有用。"
            "対照研究で皮膚糸状菌への有効性が証明された数少ない外用薬の一つ"
            "（石灰硫黄合剤、ミコナゾール/クロルヘキシジンと並ぶ）。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "0.2% emulsion (dilute 10% concentrate 1:50) — sponge over the "
                    "entire body q3-4 days x 4 applications (dermatophytosis). Do "
                    "not rinse off; allow to air dry."
                ),
                "dosage_ja": (
                    "0.2%乳剤（10%濃縮液を1:50希釈）— 全身にスポンジ塗布 q3-4日×4回（皮膚糸状菌症）。"
                    "すすがず自然乾燥させる。"
                ),
            },
            "cat": {
                "safe": False,
                "dosage": (
                    "Not licensed for cats. Grooming ingestion has caused "
                    "hypersalivation, muscle weakness and elevated liver enzymes — "
                    "use lime sulfur or miconazole/chlorhexidine rinses instead. If "
                    "used off-label: Elizabethan collar until coat is fully dry."
                ),
                "dosage_ja": (
                    "猫には未承認。グルーミングによる経口摂取で流涎・筋力低下・肝酵素上昇の報告 — "
                    "石灰硫黄合剤またはミコナゾール/クロルヘキシジンリンスを使用。"
                    "適応外使用時は被毛が完全に乾くまでエリザベスカラー装着。"
                ),
            },
            "horse": {
                "safe": True,
                "dosage": (
                    "0.2% wash q3-4 days x 4 (Trichophyton equinum, Microsporum "
                    "gypseum); include tack/grooming-kit disinfection."
                ),
                "dosage_ja": (
                    "0.2%洗浄 q3-4日×4回（Trichophyton equinum・Microsporum gypseum）。"
                    "馬具・手入れ用具の消毒も併せて実施。"
                ),
            },
            "bird": {
                "safe": True,
                "dosage": (
                    "Environmental/hatchery aspergillosis control (Clinafarm "
                    "fogging/surface); topical use on birds themselves is limited — "
                    "systemic azoles preferred for clinical aspergillosis."
                ),
                "dosage_ja": (
                    "環境・孵卵場のアスペルギルス対策（クリナファーム燻蒸/表面処理）。"
                    "鳥体への直接塗布は限定的 — 臨床的アスペルギルス症には全身アゾールを優先。"
                ),
            },
        },
        "side_effects": (
            "Local irritation (uncommon); hypersalivation/weakness if groomed off "
            "(cats). Low systemic absorption through intact skin."
        ),
        "side_effects_ja": ("局所刺激（稀）。猫が舐め取った場合は流涎・脱力。健常皮膚からの全身吸収は少ない。"),
        "contraindications": (
            "Cats (relative — see above). Do not use in food-producing animals "
            "outside label. Avoid eyes and mucous membranes."
        ),
        "contraindications_ja": ("猫（相対的禁忌 — 上記参照）。食用動物にはラベル外使用不可。眼・粘膜への使用回避。"),
        "drug_interactions": [
            {
                "drug": "No significant systemic interactions",
                "effect": "Topical use; negligible systemic absorption through intact skin.",
                "effect_ja": "外用薬であり健常皮膚からの全身吸収はごくわずか。",
            }
        ],
    },
    {
        "id": "esmolol",
        "name": "Esmolol (Brevibloc)",
        "name_ja": "エスモロール（ブレビブロック）",
        "category": "antiarrhythmics",
        "mechanism": (
            "Ultra-short-acting selective beta-1 blocker, hydrolysed by red-cell "
            "esterases (elimination half-life ~10 min in dogs). Slows sinus and AV "
            "nodal conduction. The rapid on/off kinetics make it the diagnostic and "
            "titration beta-blocker of choice for supraventricular tachycardia and "
            "for catecholamine-driven tachyarrhythmias (methylxanthine toxicosis, "
            "pheochromocytoma, thyrotoxicosis)."
        ),
        "mechanism_ja": (
            "超短時間作用型選択的β1遮断薬。赤血球エステラーゼで加水分解される"
            "（犬での消失半減期は約10分）。洞結節・房室結節伝導を抑制する。"
            "迅速なオン/オフ動態により、上室頻拍の診断的治療や、カテコラミン起因性の頻脈性不整脈"
            "（メチルキサンチン中毒・褐色細胞腫・甲状腺中毒症）の滴定用β遮断薬として第一選択。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "0.05-0.1 mg/kg IV slowly over 1-2 min (may repeat up to a total "
                    "of 0.5 mg/kg) for SVT diagnosis/conversion; CRI 25-200 "
                    "µg/kg/min titrated to heart rate/blood pressure."
                ),
                "dosage_ja": (
                    "0.05-0.1 mg/kg を1-2分かけて緩徐静注（総量 0.5 mg/kgまで反復可）— "
                    "上室頻拍の診断/停止用。CRI 25-200 µg/kg/分を心拍数・血圧で滴定。"
                ),
                "notes": (
                    "Effect dissipates within ~10-20 min of stopping the CRI — useful "
                    "when a beta-blocker trial is needed but negative inotropy is a "
                    "concern."
                ),
                "notes_ja": (
                    "CRI中止後は約10-20分で効果消失 — 陰性変力作用が懸念される症例でのβ遮断薬トライアルに有用。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": (
                    "0.05-0.1 mg/kg IV slow bolus; CRI 25-100 µg/kg/min (SVT, "
                    "thyrotoxic or HCM-associated tachycardia when rapid control "
                    "and reversibility are needed)."
                ),
                "dosage_ja": (
                    "0.05-0.1 mg/kg 緩徐静注。CRI 25-100 µg/kg/分（上室頻拍、"
                    "甲状腺中毒性・HCM関連頻脈で迅速なコントロールと可逆性が必要な場合）。"
                ),
            },
            "bird": {
                "safe": True,
                "dosage": (
                    "0.5 mg/kg slow IV (limited data) for severe methylxanthine "
                    "(caffeine/chocolate) tachyarrhythmia unresponsive to fluids and "
                    "sedation."
                ),
                "dosage_ja": (
                    "0.5 mg/kg 緩徐静注（限定的データ）— 輸液・鎮静に反応しない重度の"
                    "メチルキサンチン（カフェイン/チョコレート）性頻脈性不整脈に。"
                ),
            },
        },
        "side_effects": (
            "Hypotension, bradycardia, negative inotropy (transient given the short "
            "half-life), bronchospasm at high doses (beta-1 selectivity is "
            "dose-dependent)."
        ),
        "side_effects_ja": (
            "低血圧、徐脈、陰性変力作用（短半減期のため一過性）、"
            "高用量では気管支攣縮（β1選択性は用量依存的に失われる）。"
        ),
        "contraindications": (
            "Uncompensated congestive heart failure, bradyarrhythmias, high-grade AV block, cardiogenic shock."
        ),
        "contraindications_ja": ("非代償性うっ血性心不全、徐脈性不整脈、高度房室ブロック、心原性ショック。"),
        "drug_interactions": [
            {
                "drug": "Diltiazem",
                "effect": ("Additive AV nodal suppression and hypotension — combine with caution and continuous ECG."),
                "effect_ja": "房室結節抑制と低血圧が相加的 — 併用時は持続心電図下で慎重に。",
            },
            {
                "drug": "Dexmedetomidine",
                "effect": "Additive bradycardia.",
                "effect_ja": "徐脈が相加的。",
            },
        ],
    },
    {
        "id": "oseltamivir",
        "name": "Oseltamivir (Tamiflu)",
        "name_ja": "オセルタミビル（タミフル）",
        "category": "antivirals",
        "mechanism": (
            "Neuraminidase inhibitor prodrug. Blocks influenza A/B neuraminidase, "
            "preventing release of new virions from infected respiratory "
            "epithelium. Only useful early in infection (first 48 h). Ferrets are "
            "naturally susceptible to human influenza strains and are the main "
            "veterinary indication."
        ),
        "mechanism_ja": (
            "ノイラミニダーゼ阻害薬のプロドラッグ。インフルエンザA/B型ウイルスの"
            "ノイラミニダーゼを阻害し、感染呼吸上皮からの新規ウイルス放出を防ぐ。"
            "感染初期（48時間以内）のみ有効。フェレットはヒトインフルエンザ株に自然感受性があり、"
            "獣医領域での主適応となる。"
        ),
        "species_info": {
            "ferret": {
                "safe": True,
                "dosage": (
                    "5 mg/kg PO q12h x 5 days, started within 48 h of onset "
                    "(influenza acquired from infected humans). Supportive care — "
                    "fluids, nutrition, antipyresis — remains the mainstay."
                ),
                "dosage_ja": (
                    "5 mg/kg 経口 q12h×5日、発症48時間以内に開始（感染したヒトからうつった"
                    "インフルエンザ）。主体は支持療法 — 輸液・栄養・解熱。"
                ),
                "notes": (
                    "Ferret influenza is usually self-limiting in adults; reserve "
                    "antivirals for severe cases, kits and geriatric/comorbid "
                    "ferrets. Zoonotic in both directions — isolate from sick owners."
                ),
                "notes_ja": (
                    "成体フェレットのインフルエンザは通常自然治癒する。抗ウイルス薬は重症例・"
                    "幼体・高齢/併存疾患例に限定。双方向の人獣共通感染 — 発症した飼い主から隔離。"
                ),
            },
            "dog": {
                "safe": False,
                "dosage": (
                    "Not recommended for canine parvovirus — the proposed rationale "
                    "(bacterial neuraminidase inhibition) is unproven and the single "
                    "controlled trial (Savigny 2010) showed no significant outcome "
                    "benefit. Canine influenza is managed with supportive care."
                ),
                "dosage_ja": (
                    "犬パルボウイルスへの使用は非推奨 — 提唱された機序（細菌性ノイラミニダーゼ阻害）は"
                    "未証明で、唯一の対照試験（Savigny 2010）でも有意な転帰改善なし。"
                    "犬インフルエンザは支持療法で管理する。"
                ),
            },
        },
        "side_effects": "GI upset (vomiting, inappetence).",
        "side_effects_ja": "消化器症状（嘔吐・食欲低下）。",
        "contraindications": (
            "Renal failure (dose adjustment required — renally excreted). Not a "
            "substitute for isolation and supportive care."
        ),
        "contraindications_ja": ("腎不全（腎排泄のため用量調整が必要）。隔離と支持療法の代替にはならない。"),
        "drug_interactions": [
            {
                "drug": "Probenecid",
                "effect": "Doubles oseltamivir carboxylate exposure (human data).",
                "effect_ja": "オセルタミビル活性体の曝露を約2倍に増加（ヒトデータ）。",
            }
        ],
    },
    {
        "id": "flurbiprofen_ophthalmic",
        "search_aliases": ["フルルビプロフェン"],
        "name": "Flurbiprofen 0.03% Ophthalmic",
        "name_ja": "フルルビプロフェン0.03%点眼",
        "category": "ophthalmic",
        "mechanism": (
            "Topical ophthalmic NSAID (COX inhibitor). Suppresses prostaglandin-"
            "mediated anterior uveitis, intraoperative miosis and blood-aqueous "
            "barrier breakdown. Steroid-sparing option when corneal healing status "
            "or infection makes topical steroids risky — but it still slows "
            "epithelial healing."
        ),
        "mechanism_ja": (
            "点眼NSAID（COX阻害薬）。プロスタグランジン介在性の前部ぶどう膜炎・術中縮瞳・"
            "血液房水関門破綻を抑制する。角膜治癒状態や感染で点眼ステロイドが使いにくい場合の"
            "ステロイド代替となるが、上皮治癒はやはり遅延させる。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "1 drop in affected eye q6-12h (anterior uveitis, pre-/post-"
                    "cataract surgery, lens-induced uveitis)."
                ),
                "dosage_ja": ("患眼に1滴 q6-12h（前部ぶどう膜炎、白内障手術前後、水晶体起因性ぶどう膜炎）。"),
            },
            "cat": {
                "safe": True,
                "dosage": "1 drop q12-24h (anterior uveitis) — use the lowest effective frequency.",
                "dosage_ja": "1滴 q12-24h（前部ぶどう膜炎）— 有効最低頻度で使用。",
            },
            "horse": {
                "safe": True,
                "dosage": ("1 drop q6-12h (equine recurrent uveitis flare adjunct, post-surgical inflammation)."),
                "dosage_ja": "1滴 q6-12h（馬再発性ぶどう膜炎の増悪時補助、術後炎症）。",
            },
            "bird": {
                "safe": True,
                "dosage": "1 drop q8-12h, short courses (cataract/uveitis; limited data).",
                "dosage_ja": "1滴 q8-12h、短期間（白内障/ぶどう膜炎。限定的データ）。",
            },
        },
        "side_effects": (
            "Delayed corneal epithelial healing, local stinging, rare keratomalacia "
            "with prolonged use on compromised corneas; may blunt latanoprost's "
            "IOP-lowering effect."
        ),
        "side_effects_ja": (
            "角膜上皮治癒の遅延、点眼時刺激感、脆弱角膜への長期使用で稀に角膜融解。"
            "ラタノプロストの眼圧下降作用を減弱させることがある。"
        ),
        "contraindications": (
            "Infected or melting corneal ulcers (relative — never without "
            "concurrent antimicrobial cover and close monitoring), coagulopathy "
            "with hyphema."
        ),
        "contraindications_ja": (
            "感染性・融解性角膜潰瘍（相対的禁忌 — 抗菌カバーと厳密なモニタリングなしでは使用しない）、"
            "前房出血を伴う凝固障害。"
        ),
        "drug_interactions": [
            {
                "drug": "Latanoprost",
                "effect": "Topical NSAIDs may reduce prostaglandin-analog IOP lowering.",
                "effect_ja": "点眼NSAIDsはプロスタグランジン誘導体の眼圧下降作用を減弱させることがある。",
            },
            {
                "drug": "Topical corticosteroids",
                "effect": "Additive corneal healing delay when combined.",
                "effect_ja": "併用で角膜治癒遅延が相加的。",
            },
        ],
    },
    {
        "id": "idoxuridine_ophthalmic",
        "search_aliases": ["イドクスウリジン"],
        "name": "Idoxuridine 0.1% Ophthalmic (compounded)",
        "name_ja": "イドクスウリジン0.1%点眼（院内調剤）",
        "category": "ophthalmic",
        "mechanism": (
            "Thymidine analog antiviral. Incorporated into viral DNA in place of "
            "thymidine, producing fragile, nonfunctional genomes. Non-selective "
            "(host cells also affected), so it is topical-only. Virostatic against "
            "FHV-1; requires frequent dosing."
        ),
        "mechanism_ja": (
            "チミジンアナログ系抗ウイルス薬。チミジンの代わりにウイルスDNAへ取り込まれ、"
            "脆弱で機能しないゲノムを作らせる。選択性がない（宿主細胞にも影響）ため点眼専用。"
            "FHV-1に対して静ウイルス的で、頻回投与が必要。"
        ),
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": (
                    "1 drop of 0.1% solution q4-6h for 14-21 days (FHV-1 "
                    "conjunctivitis/dendritic keratitis); continue 1 week beyond "
                    "clinical resolution."
                ),
                "dosage_ja": ("0.1%液を1滴 q4-6h、14-21日間（FHV-1結膜炎/樹枝状角膜炎）。臨床的治癒後も1週間継続。"),
                "notes": (
                    "Compounded (no commercial product). Generally well tolerated in "
                    "cats; if the q4-6h frequency is impractical, cidofovir 0.5% "
                    "q12h is the alternative."
                ),
                "notes_ja": (
                    "院内調剤（市販品なし）。猫では概ね忍容性良好。q4-6hの頻回点眼が"
                    "実行困難な場合はシドフォビル0.5% q12hが代替。"
                ),
            },
        },
        "side_effects": ("Local irritation, punctate epithelial toxicity with prolonged use."),
        "side_effects_ja": "局所刺激、長期使用で点状上皮毒性。",
        "contraindications": (
            "Do not use systemically. Deep stromal ulceration warrants specialist "
            "referral rather than prolonged topical antivirals alone."
        ),
        "contraindications_ja": ("全身投与禁止。深部実質潰瘍は点眼抗ウイルス薬単独の長期継続ではなく専門医紹介を。"),
        "drug_interactions": [
            {
                "drug": "No significant drug interactions",
                "effect": "Topical antiviral; negligible systemic absorption.",
                "effect_ja": "点眼抗ウイルス薬であり全身吸収はごくわずか。",
            }
        ],
    },
    {
        "id": "triclabendazole",
        "name": "Triclabendazole (Fasinex)",
        "name_ja": "トリクラベンダゾール（ファシネックス）",
        "category": "antiparasitics",
        "mechanism": (
            "Benzimidazole-derivative flukicide. Uniquely active against BOTH "
            "immature (from ~1-2 weeks old) and adult Fasciola hepatica — other "
            "flukicides only kill adults. Narrow spectrum: essentially no "
            "nematode/cestode activity."
        ),
        "mechanism_ja": (
            "ベンズイミダゾール誘導体の吸虫駆除薬。未成熟虫（約1-2週齢以降）と成虫の両方の"
            "肝蛭（Fasciola hepatica）に有効な点が独特 — 他の吸虫駆除薬は成虫のみに効く。"
            "スペクトラムは狭く、線虫・条虫にはほぼ無効。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "12 mg/kg PO single dose (Fasciola hepatica; repeat per fecal sedimentation results).",
                "dosage_ja": "12 mg/kg 経口 単回（肝蛭。糞便沈殿法の結果に応じて再投与）。",
                "notes": "Off-label in horses; confirm diagnosis by fecal sedimentation/serology.",
                "notes_ja": "馬では適応外使用。糞便沈殿法・血清学で診断確定してから投与。",
            },
            "bird": {
                "safe": True,
                "dosage": (
                    "10 mg/kg PO single dose (hepatic trematodes — Fasciola, "
                    "Opisthorchis; waterfowl and zoo birds; limited data)."
                ),
                "dosage_ja": (
                    "10 mg/kg 経口 単回（肝吸虫 — Fasciola・Opisthorchis。水禽・動物園鳥類。限定的データ）。"
                ),
            },
            "rabbit": {
                "safe": True,
                "dosage": "10 mg/kg PO single dose (Fasciola; pasture/greens-fed rabbits).",
                "dosage_ja": "10 mg/kg 経口 単回（肝蛭。野草・牧草給餌のウサギ）。",
            },
        },
        "side_effects": (
            "Well tolerated at label doses; transient inappetence. Dying flukes can transiently elevate liver enzymes."
        ),
        "side_effects_ja": ("推奨用量では忍容性良好。一過性の食欲低下。虫体死滅に伴う一過性の肝酵素上昇。"),
        "contraindications": (
            "Not for lactating dairy animals supplying milk for consumption "
            "(residue rules). Resistance in livestock Fasciola is emerging — "
            "confirm efficacy with post-treatment fecal checks."
        ),
        "contraindications_ja": (
            "食用乳を供する泌乳動物には使用不可（残留規制）。家畜の肝蛭で耐性が出現しつつあるため、"
            "投与後の糞便検査で効果を確認。"
        ),
        "drug_interactions": [
            {
                "drug": "No significant drug interactions",
                "effect": "Short single-dose exposure; no clinically relevant interactions documented.",
                "effect_ja": "単回投与であり臨床的に重要な相互作用の報告はない。",
            }
        ],
    },
    {
        "id": "dimercaprol",
        "name": "Dimercaprol (BAL in Oil)",
        "name_ja": "ジメルカプロール（BAL）",
        "category": "miscellaneous",
        "mechanism": (
            "Dithiol chelator (British Anti-Lewisite). Its two sulfhydryl groups "
            "compete with tissue thiols for arsenic, mercury and (with CaEDTA) "
            "lead, forming excretable complexes. The classic antidote for "
            "arsenical toxicosis; formulated in peanut oil for deep IM injection."
        ),
        "mechanism_ja": (
            "ジチオール系キレート剤（British Anti-Lewisite）。2つのSH基が組織チオールと競合して"
            "ヒ素・水銀・（CaEDTA併用で）鉛と結合し、排泄可能な複合体を形成する。"
            "ヒ素中毒の古典的解毒薬。ピーナッツ油基剤で深部筋注する。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Arsenic: 2.5-5 mg/kg deep IM q4h for the first 24 h (use 5 "
                    "mg/kg only in acute severe cases, first day), then 2.5 mg/kg "
                    "q6-12h until recovery (usually 3-5 days total)."
                ),
                "dosage_ja": (
                    "ヒ素中毒: 最初の24時間は 2.5-5 mg/kg 深部筋注 q4h（5 mg/kgは急性重症例の初日のみ）、"
                    "その後 2.5 mg/kg q6-12h を回復まで（通常計3-5日）。"
                ),
                "notes": (
                    "Painful injection. Maintain hydration and monitor renal values — "
                    "the metal-BAL complex dissociates in acidic urine; alkalinize if "
                    "needed."
                ),
                "notes_ja": (
                    "注射は疼痛が強い。輸液で水和を維持し腎数値をモニタリング — "
                    "金属-BAL複合体は酸性尿中で解離するため、必要に応じて尿アルカリ化。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": "2.5-5 mg/kg deep IM q4h first day, then 2.5 mg/kg q6-12h (arsenic).",
                "dosage_ja": "初日 2.5-5 mg/kg 深部筋注 q4h、以後 2.5 mg/kg q6-12h（ヒ素中毒）。",
            },
            "horse": {
                "safe": True,
                "dosage": (
                    "3 mg/kg deep IM q4h x 2 days, then q6h day 3, then q12h until "
                    "recovery (arsenic; combine with aggressive IV fluids)."
                ),
                "dosage_ja": (
                    "3 mg/kg 深部筋注 q4h×2日、3日目は q6h、以後回復まで q12h（ヒ素中毒。積極的な静脈内輸液と併用）。"
                ),
            },
        },
        "side_effects": (
            "Injection-site pain and sterile abscesses, vomiting, tremors, "
            "tachycardia, transient hypertension; nephrotoxicity at high doses."
        ),
        "side_effects_ja": ("注射部位の疼痛・無菌性膿瘍、嘔吐、振戦、頻脈、一過性高血圧。高用量で腎毒性。"),
        "contraindications": (
            "Iron, cadmium or selenium toxicosis (the BAL-metal complexes are MORE "
            "toxic than the metals alone), hepatic failure (except acute arsenical "
            "hepatitis). Do not give iron supplements during BAL therapy."
        ),
        "contraindications_ja": (
            "鉄・カドミウム・セレン中毒（BAL-金属複合体は金属単独より毒性が強い）、"
            "肝不全（急性ヒ素性肝炎を除く）。BAL治療中は鉄剤を投与しない。"
        ),
        "drug_interactions": [
            {
                "drug": "Iron Dextran",
                "effect": ("BAL-iron complex is nephrotoxic — never supplement iron during dimercaprol therapy."),
                "effect_ja": "BAL-鉄複合体は腎毒性 — ジメルカプロール治療中の鉄剤投与は禁止。",
            },
            {
                "drug": "Calcium EDTA (CaNa2EDTA)",
                "effect": ("Intended combination for severe lead toxicosis with CNS signs (BAL first, then CaEDTA)."),
                "effect_ja": "中枢神経症状を伴う重度鉛中毒での意図的併用（BAL先行→CaEDTA）。",
            },
        ],
    },
    {
        "id": "celecoxib",
        "name": "Celecoxib (Celebrex)",
        "name_ja": "セレコキシブ（セレコックス/セレブレックス）",
        "category": "nsaids",
        "mechanism": (
            "Selective COX-2 inhibitor NSAID. In avian medicine it is the "
            "best-documented empirical anti-inflammatory for proventricular "
            "dilatation disease (avian bornavirus ganglioneuritis): COX-2 "
            "blockade dampens the lymphoplasmacytic ganglion inflammation that "
            "drives GI dysmotility (Dahlhausen 2002)."
        ),
        "mechanism_ja": (
            "選択的COX-2阻害NSAID。鳥類医療では腺胃拡張症（PDD、鳥ボルナウイルス性"
            "神経節炎）に対する経験的抗炎症療法として最も文献的裏付けのある薬剤で、"
            "COX-2阻害により消化管運動障害の原因となるリンパ形質細胞性神経節炎症を"
            "抑制する（Dahlhausen 2002）。"
        ),
        "species_info": {
            "bird": {
                "safe": True,
                "dosage": (
                    "PDD (empirical): 10-20 mg/kg PO q24h long-term (Dahlhausen "
                    "2002 — clinical improvement in a majority of treated "
                    "psittacines; not curative, virus persists). Give with food; "
                    "compounded suspension for accurate small-bird dosing."
                ),
                "dosage_ja": (
                    "PDD（経験的治療）: 10-20 mg/kg 経口 q24h 長期（Dahlhausen 2002 — "
                    "治療オウム類の過半数で臨床的改善。治癒はせずウイルスは残存）。"
                    "食餌と共に投与。小型鳥では正確な用量調整のため調剤懸濁液を使用。"
                ),
                "notes": (
                    "Monitor droppings/weight; combine with small frequent "
                    "easily-digestible meals and gastric prokinetics as indicated. "
                    "Meloxicam is the alternative when celecoxib is unavailable."
                ),
                "notes_ja": (
                    "排泄物と体重をモニタリング。少量頻回の易消化食や消化管運動促進薬と"
                    "適宜併用。セレコキシブが入手できない場合はメロキシカムが代替。"
                ),
            },
            "dog": {
                "safe": True,
                "dosage": (
                    "Rarely indicated — licensed veterinary coxibs (deracoxib, "
                    "firocoxib, robenacoxib) are preferred; human celecoxib PK in "
                    "dogs is polymorphic (fast/slow metabolisers)."
                ),
                "dosage_ja": (
                    "適応は稀 — 動物用承認コキシブ（デラコキシブ・フィロコキシブ・"
                    "ロベナコキシブ）を優先。ヒト用セレコキシブの犬での薬物動態は"
                    "多型性（速い/遅い代謝群）がある。"
                ),
            },
        },
        "side_effects": (
            "GI upset/ulceration, renal injury in hypovolemia, hepatopathy "
            "(idiosyncratic). Avian long-term safety data limited."
        ),
        "side_effects_ja": (
            "消化器症状・潰瘍、循環血液量減少時の腎障害、特異体質性肝障害。鳥類での長期安全性データは限定的。"
        ),
        "contraindications": (
            "Dehydration/hypovolemia, renal or hepatic failure, GI ulceration, "
            "concurrent corticosteroids or other NSAIDs."
        ),
        "contraindications_ja": (
            "脱水・循環血液量減少、腎不全・肝不全、消化管潰瘍、コルチコステロイドまたは他のNSAIDsとの併用。"
        ),
        "drug_interactions": [
            {
                "drug": "Corticosteroids",
                "effect": "Additive GI ulceration — do not combine.",
                "effect_ja": "消化管潰瘍リスクが相加的 — 併用しない。",
            },
            {
                "drug": "Furosemide",
                "effect": "NSAIDs blunt diuretic response and increase renal risk.",
                "effect_ja": "NSAIDsは利尿反応を減弱させ腎リスクを増加させる。",
            },
        ],
    },
]
