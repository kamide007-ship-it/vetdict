"""Drug batch 8 – Reproductive medicine & lactation support drugs

Specialized therapeutics for breeding soundness, infertility management,
lactation support, and periparturient complications across 21 species.

References:
  - Hafez & Hafez: Reproduction in Farm Animals (9th ed, 2018)
  - McKinnon et al.: Equine Reproduction (3rd ed, 2011)
  - Verstegen et al.: Handbook of Small Animal Theriogenology (2009)
  - Carpenter's Exotic Animal Formulary (6th ed, 2023)
  - Plumb's Veterinary Drug Handbook (12th ed, 2024)
"""

from __future__ import annotations

from typing import Any, Dict, List

DRUGS_BATCH_8: List[Dict[str, Any]] = [
    {
        "id": "domperidone",
        "name": "Domperidone",
        "name_ja": "ドンペリドン",
        "category": "lactation_support",
        "mechanism": "Dopamine D2 receptor antagonist that increases prolactin secretion by blocking dopamine's inhibitory effect on lactotroph cells. Peripheral action (doesn't cross BBB) minimizes CNS side effects.",
        "mechanism_ja": "ドーパミンD2受容体拮抗薬。ドーパミンのラクトトロープ細胞への抑制作用を遮断してプロラクチン分泌を増加。末梢作用（BBB非通過）でCNS副作用を最小化",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "25-30 mg PO BID-TID",
                "dosage_ja": "25-30 mg 経口 1日2-3回",
                "notes": "First-line therapy for mare lactation failure. Onset 2-7 days. Monitor serum prolactin levels (target >10 ng/mL). Efficacy 70-80% in clinical trials.",
                "notes_ja": "牝馬の乳汁分泌不全に第1選択。発現2-7日。血清プロラクチン値をモニタリング（目標>10 ng/mL）。臨床試験での有効率70-80%",
            },
            "dog": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO BID-TID",
                "dosage_ja": "0.5-1 mg/kg 経口 1日2-3回",
                "notes": "Used for pseudopregnancy/false pregnancy and to support lactation in nursing bitches. Duration 2-4 weeks.",
                "notes_ja": "偽妊娠・偽妊娠および授乳母犬の乳汁分泌サポート。期間2-4週間",
            },
            "cat": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO TID",
                "dosage_ja": "0.5-1 mg/kg 経口 1日3回",
                "notes": "Support lactation in nursing queens. Off-label use but well-tolerated.",
                "notes_ja": "授乳母猫の乳汁分泌サポート。適応外使用だが忍容性良好",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1-2 mg/kg PO BID-TID",
                "dosage_ja": "1-2 mg/kg 経口 1日2-3回",
                "notes": "Supports doe lactation. Monitor intake carefully.",
                "notes_ja": "母ウサギの乳汁分泌サポート。摂取を綿密にモニタリング",
            },
        },
        "side_effects": ["Transient anorexia", "Mild agitation (rare)", "Increased estrous activity (prolonged use)"],
        "side_effects_ja": ["一過性食欲不振", "軽度の興奮性（稀）", "発情活動の亢進（長期使用）"],
        "contraindications": "Contraindicated in animals with dopamine-dependent critical functions (rare). Use caution in prolactinomas. Not for use in animals requiring dopamine agonist therapy.",
        "contraindications_ja": "ドーパミン依存性の重篤な機能障害がある動物では禁忌（稀）。プロラクチノーマ使用時は慎重。ドーパミン作動薬治療を必要とする動物には使用不可",
    },
    {
        "id": "oxytocin_reproductive",
        "name": "Oxytocin (Reproductive Use)",
        "name_ja": "オキシトシン（生殖医学用）",
        "category": "reproductive_hormones",
        "mechanism": "Nonapeptide hormone that stimulates uterine myometrial contractions and facilitates milk letdown reflex. Acts on oxytocin receptors on smooth muscle.",
        "mechanism_ja": "九ペプチド製ホルモン。子宮筋層の収縮を刺激し乳汁放出反射を促進。平滑筋のオキシトシン受容体に作用",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "10-20 IU IM/IV q30min (max 3-4 doses)",
                "dosage_ja": "10-20 IU 筋注/静注 30分毎（最大3-4回）",
                "notes": "For retained fetal membranes (RFM). Must combine with IV fluid therapy and progestin support. Do NOT use in early labor (<1 hour post-foaling). Monitor for excessive uterine contraction (risk of uterine rupture if dose >40 IU).",
                "notes_ja": "胎盤停滞（RFM）に使用。輸液療法とプロゲスチン補充と併用必須。分娩初期（分娩後1時間以内）には使用禁止。過剰な子宮収縮をモニタリング（40IU以上で子宮破裂リスク）",
            },
            "dog": {
                "safe": True,
                "dosage": "5-20 IU IM (max 2-3 doses, 15-30 min apart)",
                "dosage_ja": "5-20 IU 筋注（最大2-3回、15-30分間隔）",
                "notes": "For uterine inertia (weak labor/failure to progress). Use only in confirmed stage 2 labor with >2 hours of unproductive straining. Do NOT use for primary inertia without veterinary evaluation.",
                "notes_ja": "子宮無力症（陣痛微弱・分娩進行不全）に使用。確認された第2段陣痛で2時間以上無結果の怒責のみ。獣医師評価なしに原発性無力症には使用禁止",
            },
            "cat": {
                "safe": True,
                "dosage": "2.5-5 IU IM (max 2 doses, 20 min apart)",
                "dosage_ja": "2.5-5 IU 筋注（最大2回、20分間隔）",
                "notes": "For feline dystocia/uterine inertia. Cats are more sensitive; use lowest effective dose. Risk of uterine atony if overused.",
                "notes_ja": "猫の難産・子宮無力症に使用。猫は感受性が高い。最小有効用量を使用。過剰使用で子宮弛緩のリスク",
            },
        },
        "side_effects": [
            "Excessive uterine contraction",
            "Uterine rupture (overdose)",
            "Abdominal pain",
            "Systemic hypotension (IV use)",
        ],
        "side_effects_ja": ["過剰な子宮収縮", "子宮破裂（過剰用量）", "腹部痛", "全身性低血圧（IV使用）"],
        "contraindications": "Absolute contraindication: dystocia from malpresentation or obstruction (can rupture uterus). Not before cervical dilation confirmed. Not if fetus dead/compromised.",
        "contraindications_ja": "絶対禁忌：胎位異常・機械的閉塞による難産（子宮破裂の危険）。子宮頸部開大確認前に使用禁止。胎仔死亡・障害がある場合は禁止",
    },
    {
        "id": "cloprostenol",
        "name": "Cloprostenol (Estrumate)",
        "name_ja": "クロプロステノール（エストルメート）",
        "category": "reproductive_hormones",
        "mechanism": "Synthetic prostaglandin F2α analog that induces luteolysis by binding to FP receptors on corpus luteum cells, causing progesterone withdrawal and estrus induction/cycling.",
        "mechanism_ja": "合成プロスタグランジンF2αアナログ。黄体のFP受容体に結合して黄体溶解を誘発。プロゲステロン消失と発情誘発・周期化を引き起こす",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "250 μg IM q6-8h (typically 2-3 doses during estrous cycle)",
                "dosage_ja": "250 μg 筋注 6-8時間毎（通常発情周期中に2-3回）",
                "notes": "For retained corpus luteum, cycling mares to promote estrus, and assisting with retained fetal membranes when combined with oxytocin. NEVER use in pregnant mares (induces abortion). Maximum cumulative dose 500-750 μg per treatment cycle.",
                "notes_ja": "黄体保留、発情周期馬の発情促進、オキシトシン併用時の胎盤停滞治療に使用。妊娠牝馬には絶対使用禁止（流産誘発）。治療周期あたり最大累積用量500-750 μg",
            },
            "dog": {
                "safe": True,
                "dosage": "1-5 μg/kg IM q24h",
                "dosage_ja": "1-5 μg/kg 筋注 24時間毎",
                "notes": "For terminating unwanted pregnancy (most effective <45 days). Also promotes estrus in cycling bitches. Side effects: restlessness, salivation, defecation within 30 min of injection.",
                "notes_ja": "望まない妊娠の中断（45日以内が最も有効）。また発情周期中の母犬の発情促進に使用。副作用：注射後30分以内に落ち着きなさ、流涎、排便",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2.5 μg/kg IM",
                "dosage_ja": "1-2.5 μg/kg 筋注",
                "notes": "For unwanted pregnancy termination in cats (single dose often sufficient). Induces estrus in cycling queens. Less predictable than in dogs.",
                "notes_ja": "猫の望まない妊娠中断（単回投与がしばしば十分）。発情周期中の母猫の発情誘発。犬より予測不能",
            },
        },
        "side_effects": ["Salivation", "Defecation", "Urination", "Restlessness", "Panting", "Sweating (horse)"],
        "side_effects_ja": ["流涎", "排便", "排尿", "落ち着きなさ", "喘息", "発汗（馬）"],
        "contraindications": "ABSOLUTE: Not in pregnant animals (induces abortion). Not in animals with hypersensitivity to prostaglandins. Use caution in renal disease, asthma, GI ulcers.",
        "contraindications_ja": "絶対禁忌：妊娠動物（流産誘発）。プロスタグランジン過敏症のある動物に不可。腎疾患・喘息・消化性潰瘍のある動物では慎重",
    },
    {
        "id": "tramadol_lactation",
        "name": "Tramadol (Reproductive Use: Lactation Support)",
        "name_ja": "トラマドール（生殖医学用：乳汁分泌サポート）",
        "category": "analgesics_lactation",
        "mechanism": "Dual mechanism: (1) μ-opioid agonist for pain relief; (2) μ-receptor stimulation increases prolactin secretion via TRH stimulation. Alternative when domperidone unavailable.",
        "mechanism_ja": "二重作用機序：(1)μオピオイド作動薬として鎮痛；(2)μ受容体刺激でTRH刺激によるプロラクチン分泌増加。ドメペリドン入手困難時の代替",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "5-6 mg/kg PO TID (15 mg/kg total daily)",
                "dosage_ja": "5-6 mg/kg 経口 1日3回（総1日量15 mg/kg）",
                "notes": "Alternative to domperidone for lactation failure when domperidone unavailable (e.g., Japan). Combines analgesia (postpartum pain relief) + prolactin stimulation. Efficacy ~70%. Can combine with domperidone for synergistic effect. Monitor for GI upset.",
                "notes_ja": "ドメペリドン入手困難時の乳汁分泌不全の代替（例：日本）。鎮痛（産後疼痛緩和）＋プロラクチン刺激を組み合わせ。有効率~70%。ドメペリドンとの併用で相乗効果。GI障害をモニタリング",
            },
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q6-8h",
                "dosage_ja": "5-10 mg/kg 経口 6-8時間毎",
                "notes": "For postpartum pain in dams + lactation support. Can use alongside domperidone. Monitor for CNS side effects (mild sedation, panting).",
                "notes_ja": "母犬の産後疼痛＋乳汁分泌サポート。ドメペリドン併用可能。CNS副作用（軽度鎮静、喘息）をモニタリング",
            },
        },
        "side_effects": ["Sedation", "Panting", "GI upset (mild)", "Dizziness (rare)"],
        "side_effects_ja": ["鎮静", "喘息", "GI障害（軽度）", "めまい（稀）"],
        "contraindications": "Avoid in seizure history. Not in animals receiving MAOIs or tramadol-like drugs. Use caution in respiratory depression.",
        "contraindications_ja": "けいれん既往歴のある動物では避ける。MAOI投与中または同様の薬剤投与中は禁止。呼吸抑制のある動物では慎重",
    },
    {
        "id": "heparin_laminitis",
        "name": "Heparin (Laminitis Prevention in Periparturient Mares)",
        "name_ja": "ヘパリン（産褥期牝馬の蹄葉炎予防）",
        "category": "anticoagulants",
        "mechanism": "Unfractionated heparin potentiates antithrombin III action to prevent thrombosis and endotoxemia-induced DIC. Also has anti-inflammatory properties and may preserve hoof lamellae perfusion during periparturient stress.",
        "mechanism_ja": "未分画ヘパリン。アンチトロンビンIII作用を増強して血栓症とエンドトキシン誘発DICを予防。また抗炎症特性を持ち、産褥期ストレス時の蹄葉灌流を保持する可能性",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "40-100 IU/kg IV SID × 5-7 days",
                "dosage_ja": "40-100 IU/kg 静注 1日1回 5-7日間",
                "notes": "Gold standard for laminitis prevention in mares with retained placenta, severe colic, or sepsis. Start within 24 hours of risk event. Target aPTT 1.5-2.0× control. ALTERNATIVE: Low-molecular-weight heparin (enoxaparin) 150 IU/kg SC BID for 5-7 days if unfractionated heparin unavailable.",
                "notes_ja": "胎盤停滞・重度疝痛・敗血症のある牝馬の蹄葉炎予防の標準。リスク事象から24時間以内に開始。目標aPTT 1.5-2.0×対照。代替：未分画ヘパリン入手困難時は低分子ヘパリン（エノキサパリン）150 IU/kg 皮下 1日2回 5-7日間",
            },
        },
        "side_effects": [
            "Hemorrhage (rare, if aPTT excessive)",
            "Thrombocytopenia (rare)",
            "Heparin-induced thrombosis (very rare)",
        ],
        "side_effects_ja": ["出血（稀、aPTT過剰時）", "血小板減少症（稀）", "ヘパリン誘発性血栓症（極稀）"],
        "contraindications": "Avoid in active hemorrhage. Use caution in thrombocytopenia (<100k/μL). Monitor aPTT q24-48h.",
        "contraindications_ja": "活動性出血のある動物では避ける。血小板減少症（<100k/μL）で慎重。aPTTを24-48時間毎にモニタリング",
    },
    {
        "id": "selenium_vitamin_e",
        "name": "Selenium + Vitamin E (Periparturient Supplement)",
        "name_ja": "セレニウム＋ビタミンE（産褥期補充）",
        "category": "vitamins_minerals",
        "mechanism": "Selenium (component of glutathione peroxidase) + Vitamin E (lipid-soluble antioxidant) together combat oxidative stress and support immune function in periparturient period. Deficiency linked to weak labor, retained placenta, and low milk quality.",
        "mechanism_ja": "セレニウム（グルタチオンペルオキシダーゼ成分）＋ビタミンE（脂溶性抗酸化）が酸化ストレスに対抗し産褥期の免疫機能をサポート。欠乏は陣痛微弱・胎盤停滞・低品質乳汁と関連",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Se 3-5 mg/day IV/IM starting 2-3 weeks pre-foaling, continue 5-7 days post-foaling; Vitamin E 2000-3000 IU/day PO",
                "dosage_ja": "Se 3-5 mg/日 静注/筋注（分娩2-3週間前から開始、分娩後5-7日間継続）；ビタミンE 2000-3000 IU/日 経口",
                "notes": "Prophylaxis for RFM, lactation failure, and laminitis in high-risk mares. Serum Se target >0.15 μg/mL. Vitamin C 1-2 g IV also recommended perioperatively. Combined antioxidant effect prevents endotoxemia cascade.",
                "notes_ja": "RFM・乳汁分泌不全・蹄葉炎リスク牝馬の予防。血清Se目標>0.15 μg/mL。ビタミンC 1-2g静注も術周期に推奨。組み合わせた抗酸化効果がエンドトキシミアカスケードを予防",
            },
            "dog": {
                "safe": True,
                "dosage": "Se 0.1-0.3 mg/day PO; Vitamin E 200-400 IU/day PO",
                "dosage_ja": "Se 0.1-0.3 mg/日 経口；ビタミンE 200-400 IU/日 経口",
                "notes": "Periparturient supplementation (last 3-4 weeks before whelping + 2-3 weeks after). Supports immune function and milk quality. Especially important in borderline deficiency regions.",
                "notes_ja": "産褥期補充（分娩前3-4週間＋分娩後2-3週間）。免疫機能と乳汁品質をサポート。欠乏境界線地域で特に重要",
            },
            "cat": {
                "safe": True,
                "dosage": "Se 0.05-0.1 mg/day PO; Vitamin E 50-100 IU/day PO",
                "dosage_ja": "Se 0.05-0.1 mg/日 経口；ビタミンE 50-100 IU/日 経口",
                "notes": "Supportive therapy during pregnancy + lactation. Cats are sensitive to Se toxicity at high doses (>1 mg/kg); use minimal effective dose.",
                "notes_ja": "妊娠＋授乳期の支持療法。猫は高用量Se毒性（>1 mg/kg）に敏感。最小有効用量を使用",
            },
        },
        "side_effects": [
            "Selenium toxicity (garlic odor breath, hair loss, hooves brittle) if overdosed",
            "Vitamin E: rare GI upset at high doses",
        ],
        "side_effects_ja": [
            "セレニウム毒性（過剰投与時：ニンニク臭の呼気、脱毛、蹄ろう質化）",
            "ビタミンE：高用量時の稀なGI障害",
        ],
        "contraindications": "Avoid excessive Se dosing (narrow margin between deficiency and toxicity). Do not combine with other Se supplements without dose adjustment.",
        "contraindications_ja": "過剰Se投与を避ける（欠乏と毒性の間の間隔が狭い）。他のSe補充との併用時は用量調整が必須",
    },
    {
        "id": "deslorelin_reproductive",
        "name": "Deslorelin (Suprelorin, GnRH Agonist Implant)",
        "name_ja": "デスロレリン（スプレソリン、GnRHアゴニストインプラント）",
        "category": "reproductive_hormones",
        "mechanism": "GnRH agonist that causes initial GnRH receptor stimulation (flare), followed by downregulation and suppression of FSH/LH. Used for estrus induction or suppression depending on timing and species.",
        "mechanism_ja": "GnRHアゴニスト。初期GnRH受容体刺激（フレア）の後、downregulation と FSH/LH抑制。タイミングと動物種に応じて発情誘発または抑制に使用",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "2.1 mg SC implant (single, lasts ~4 weeks) or 4.7 mg (lasts ~12 weeks)",
                "dosage_ja": "2.1 mg 皮下インプラント（単回、効果4週間）または4.7 mg（効果12週間）",
                "notes": "For ovulation induction (flare phase, 24-48h post-implant) in mares during spring transition or to synchronize estrus cycles for breeding management. Suprapituitary GnRH agonist effect overcomes seasonal anestrus. Also used to suppress estrus in high-performance mares during training season.",
                "notes_ja": "牝馬の排卵誘発（フレア期、インプラント後24-48時間）。春の転換期または繁殖管理のための発情周期同期化に使用。下垂体上GnRHアゴニスト効果が季節性発情停止を克服。訓練期間中に高パフォーマンス牝馬の発情を抑制するのにも使用",
            },
            "dog": {
                "safe": True,
                "dosage": "4.7 mg SC implant",
                "dosage_ja": "4.7 mg 皮下インプラント",
                "notes": "For control of estrus in intact females during show season or to suppress unwanted mating behavior in males. Reversible chemical castration. Lasts 6-12 months depending on dose.",
                "notes_ja": "ショーシーズン中の未去勢メスの発情抑制または未去勢オスの不適切な交配行動抑制。可逆的な化学的去勢。用量に応じて6-12ヶ月持続",
            },
        },
        "side_effects": [
            "Initial flare-up (increased estrous signs for 24-48h)",
            "Injection site reaction (mild)",
            "Temporary behavior changes",
        ],
        "side_effects_ja": ["初期フレア（24-48時間の発情徴候増加）", "注射部位反応（軽度）", "一時的な行動変化"],
        "contraindications": "Not for use if estrus is undesirable (initial flare will worsen signs). Avoid in pregnancy. Requires veterinary placement.",
        "contraindications_ja": "発情が望ましくない場合は使用禁止（初期フレアが徴候を悪化）。妊娠中は避ける。獣医師による設置が必須",
    },
]
