"""Drug batch 47 – referenced-but-absent agents surfaced by the 2026-08 audit (16th sweep).

The dosage-context katakana token audit (drug-suffix tokens with an explicit
dose within 60 chars, cross-checked against find_drugs_in_text) found four
agents that VetDict's own disease content instructs clinicians to use — with
explicit doses — yet were absent from the formulary:

  - メマンチン (memantine): canine compulsive-disorder / cognitive-dysfunction
    entries cite "メマンチン 0.3-0.5 mg/kg PO q12h — NMDA拮抗薬" as the
    add-on when SSRIs/TCAs alone fail, yet no NMDA antagonist existed.
  - プロカルバジン (procarbazine): the MUO/GME rescue protocols cite
    "プロカルバジン 25-50 mg/m² PO q24h" — one of the few cytotoxics with
    good blood-brain-barrier penetration — absent from the dictionary.
  - フェニトイン (phenytoin): the digoxin-toxicity entries cite
    "フェニトイン 5-10 mg/kg IV slow" for digitalis-induced ventricular
    arrhythmias (the classic indication where lidocaine fails), absent.
  - ビオチン (biotin): avian feather/skin entries cite "ビオチン
    0.5-1.0 mg/kg PO q24h" and equine hoof-quality management is one of the
    few nutraceutical uses with controlled-trial evidence — absent.

References:
  - Schneider BM, Dodman NH, Maranda L. J Vet Behav 2009;4:118 — memantine
    open-label trial in canine compulsive disorder: 11/11 dogs improved at
    0.3-1 mg/kg/day as fluoxetine add-on or monotherapy.
  - Overall KL. Manual of Clinical Behavioral Medicine 2013 — NMDA
    antagonists in compulsive disorder; memantine dosing 0.3-0.5 mg/kg q12h.
  - Coates JR, Jeffery ND. Vet Clin North Am 2014 — MUO therapy review:
    procarbazine 25-50 mg/m² PO q24h as steroid-sparing rescue.
  - Cantile C et al. / MOPP rescue protocols (Northrup NC et al. J Vet
    Intern Med 2009) — procarbazine as the "P" of MOPP for relapsed canine
    lymphoma, 50 mg/m² PO q24h ×14 days per 28-day cycle.
  - Plumb's Veterinary Drug Handbook 10th ed — phenytoin: dogs 5-10 mg/kg
    slow IV for digitalis-induced ventricular arrhythmia; oral
    anticonvulsant use obsolete in dogs (rapid elimination); cats: severely
    prolonged half-life with hepatotoxicity/thrombocytopenia — avoid.
  - Josseck H, Zenker W, Geyer H. Equine Vet J 1995;27:175 — biotin
    15-20 mg/day PO improved hoof horn quality in Lipizzaners over
    long-term supplementation (controlled trial).
  - Carpenter's Exotic Animal Formulary 6th ed — avian biotin
    supplementation for feather/beak keratin disorders.
"""

DRUGS_BATCH_47: list[dict] = [
    {
        "id": "memantine",
        "search_aliases": ["メマンチン", "Memantine", "メマリー"],
        "name": "Memantine",
        "name_ja": "メマンチン",
        "category": "behavioral",
        "mechanism": "Uncompetitive NMDA-receptor antagonist; dampens pathological glutamatergic signalling implicated in compulsive behaviours and cognitive dysfunction while sparing normal synaptic transmission.",
        "mechanism_ja": "非競合的NMDA受容体拮抗薬。常同・強迫行動や認知機能不全に関与する病的グルタミン酸シグナルを抑制しつつ、正常なシナプス伝達は温存する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Compulsive disorder (adjunct to fluoxetine/clomipramine or monotherapy): 0.3-0.5 mg/kg PO q12h; up to 1 mg/kg/day (Schneider 2009 J Vet Behav). Cognitive dysfunction adjunct at the same dose. Allow 2-4 weeks to judge response.",
                "dosage_ja": "強迫性障害（フルオキセチン/クロミプラミンへの追加または単独）: 0.3-0.5 mg/kg 経口 12時間毎、最大1 mg/kg/日（Schneider 2009 J Vet Behav）。認知機能不全症候群の補助にも同用量。効果判定には2-4週間。",
                "notes": "Behavioural modification remains the foundation — memantine is an adjunct, not a substitute. Well tolerated in the published series; sedation/GI upset occasionally reported.",
                "notes_ja": "行動修正療法が治療の基盤 — メマンチンは補助であり代替ではない。公表シリーズでは忍容性良好。まれに鎮静・消化器症状。",
            },
            "cat": {
                "safe": True,
                "dosage": "Limited data; extrapolated 0.3-0.5 mg/kg PO q12-24h for refractory psychogenic alopecia/compulsive disorders after excluding medical causes.",
                "dosage_ja": "データ限定的。器質的疾患を除外した難治性心因性脱毛症・強迫性障害に外挿で 0.3-0.5 mg/kg 経口 12-24時間毎。",
                "notes": "Rule out dermatologic/pain causes before treating grooming disorders as behavioural.",
                "notes_ja": "グルーミング障害を行動学的に治療する前に皮膚科的・疼痛性の原因を必ず除外。",
            },
        },
        "side_effects": ["Sedation", "GI upset (vomiting, inappetence)", "Agitation (rare)"],
        "side_effects_ja": ["鎮静", "消化器症状（嘔吐・食欲低下）", "興奮（まれ）"],
        "contraindications": "Severe renal impairment (renally excreted — reduce dose); concurrent other NMDA antagonists (amantadine, ketamine) without dose review.",
        "contraindications_ja": "重度腎機能障害（腎排泄のため減量）。他のNMDA拮抗薬（アマンタジン・ケタミン）との無調整併用。",
        "drug_interactions": [
            {
                "drug": "Amantadine",
                "severity": "moderate",
                "description": "Additive NMDA antagonism — avoid stacking or reduce doses",
                "description_ja": "NMDA拮抗作用が相加 — 重複投与を避けるか減量",
            },
            {
                "drug": "Fluoxetine",
                "severity": "minor",
                "description": "Intentional combination in compulsive disorder; monitor for additive sedation",
                "description_ja": "強迫性障害では意図的な併用 — 相加的鎮静をモニタリング",
            },
        ],
    },
    {
        "id": "procarbazine",
        "search_aliases": ["プロカルバジン", "Procarbazine", "塩酸プロカルバジン"],
        "name": "Procarbazine",
        "name_ja": "プロカルバジン",
        "category": "antineoplastics",
        "mechanism": "Alkylating-like cytotoxic (methylhydrazine derivative) that crosses the blood-brain barrier — the basis for its use in CNS inflammatory disease (MUO/GME rescue) and as the 'P' of MOPP rescue for relapsed lymphoma. Also a weak MAO inhibitor.",
        "mechanism_ja": "血液脳関門を通過するアルキル化様細胞傷害薬（メチルヒドラジン誘導体）。CNS炎症性疾患（MUO/GMEレスキュー）とリンパ腫再発時MOPPプロトコルの「P」としての使用根拠。弱いMAO阻害作用も持つ。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "MUO/GME (steroid-sparing rescue): 25-50 mg/m² PO q24h, taper with clinical/MRI response (Coates & Jeffery 2014). MOPP rescue for relapsed lymphoma: 50 mg/m² PO q24h days 1-14 of a 28-day cycle (Northrup 2009 JVIM).",
                "dosage_ja": "MUO/GME（ステロイド減量レスキュー）: 25-50 mg/m² 経口 24時間毎、臨床・MRI反応で漸減（Coates & Jeffery 2014）。リンパ腫再発MOPP: 28日サイクルの第1-14日に 50 mg/m² 経口 24時間毎（Northrup 2009 JVIM）。",
                "notes": "Myelosuppression (nadir 2-3 weeks) and hemorrhagic gastroenteritis are dose-limiting — CBC before each cycle. Cytotoxic handling precautions; capsules must not be split at home.",
                "notes_ja": "用量制限毒性は骨髄抑制（ナディア2-3週）と出血性胃腸炎 — 各サイクル前にCBC。細胞傷害性薬剤の取扱注意。カプセルの家庭での分割は不可。",
            },
            "cat": {
                "safe": True,
                "dosage": "Limited data; MOPP-type rescue 50 mg/m² PO q24h ×14 days per cycle with vigilant CBC monitoring.",
                "dosage_ja": "データ限定的。MOPP型レスキューとして 50 mg/m² 経口 24時間毎 ×14日/サイクル。CBCを厳重にモニタリング。",
                "notes": "Use only under oncology guidance.",
                "notes_ja": "腫瘍科の指導下でのみ使用。",
            },
        },
        "side_effects": [
            "Myelosuppression (neutropenia, thrombocytopenia)",
            "Hemorrhagic gastroenteritis",
            "Vomiting/anorexia",
            "Hepatotoxicity (rare)",
        ],
        "side_effects_ja": ["骨髄抑制（好中球減少・血小板減少）", "出血性胃腸炎", "嘔吐・食欲不振", "肝毒性（まれ）"],
        "contraindications": "Pre-existing severe myelosuppression; concurrent MAO-inhibitor-interacting drugs without review; pregnancy.",
        "contraindications_ja": "既存の重度骨髄抑制。MAO阻害相互作用薬との無調整併用。妊娠動物。",
        "drug_interactions": [
            {
                "drug": "Selegiline",
                "severity": "major",
                "description": "Additive MAO inhibition — avoid combination",
                "description_ja": "MAO阻害作用が相加 — 併用回避",
            },
            {
                "drug": "Cyclophosphamide",
                "severity": "moderate",
                "description": "Additive myelosuppression in multi-agent protocols — stagger CBC monitoring",
                "description_ja": "多剤プロトコルで骨髄抑制が相加 — CBCモニタリングを強化",
            },
        ],
    },
    {
        "id": "phenytoin",
        "search_aliases": ["フェニトイン", "Phenytoin", "ジフェニルヒダントイン", "アレビアチン"],
        "name": "Phenytoin",
        "name_ja": "フェニトイン",
        "category": "cardiovascular",
        "mechanism": "Class IB sodium-channel blocker. In veterinary practice its niche is digitalis-induced ventricular arrhythmia: it suppresses digoxin-triggered automaticity while improving AV conduction — the arrhythmia setting where lidocaine may fail. Oral anticonvulsant use is obsolete in dogs (elimination too rapid) and dangerous in cats.",
        "mechanism_ja": "クラスIBナトリウムチャネル遮断薬。獣医領域でのニッチはジギタリス中毒性心室性不整脈 — ジゴキシン誘発性の異常自動能を抑制しつつ房室伝導は改善する（リドカイン不応例で考慮）。犬での経口抗てんかん薬用途は消失半減期が短すぎ廃用。猫では危険。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Digitalis-induced ventricular arrhythmia: 5-10 mg/kg slow IV (over 5+ min, ECG monitoring); may repeat to effect. Oral maintenance not practical (t½ 3-4 h).",
                "dosage_ja": "ジギタリス中毒性心室性不整脈: 5-10 mg/kg 緩徐静注（5分以上かけECG監視下）。効果を見て反復可。経口維持は半減期3-4時間のため非実用的。",
                "notes": "Stop digoxin first; correct hypokalemia. Rapid IV injection causes hypotension/bradycardia (propylene glycol vehicle).",
                "notes_ja": "まずジゴキシン中止・低カリウム血症を補正。急速静注は溶媒（プロピレングリコール）による低血圧・徐脈を起こす。",
            },
            "cat": {
                "safe": False,
                "dosage": "Avoid — half-life 24-108 h with cumulative hepatotoxicity and thrombocytopenia.",
                "dosage_ja": "使用回避 — 半減期24-108時間で蓄積し、肝毒性・血小板減少症を起こす。",
                "notes": "Cats eliminate phenytoin extremely slowly; safer antiarrhythmics (lidocaine low-dose, beta-blockers) exist.",
                "notes_ja": "猫はフェニトインの消失が極めて遅い。より安全な抗不整脈薬（低用量リドカイン・β遮断薬）を選択。",
            },
        },
        "side_effects": [
            "Hypotension/bradycardia with rapid IV",
            "Sedation, ataxia",
            "Gingival hyperplasia (chronic use)",
            "Hepatotoxicity (cats, chronic dogs)",
        ],
        "side_effects_ja": [
            "急速静注での低血圧・徐脈",
            "鎮静・運動失調",
            "歯肉増殖（慢性投与）",
            "肝毒性（猫・犬の慢性投与）",
        ],
        "contraindications": "Cats (chronic use), severe bradycardia, 2nd/3rd-degree AV block, severe hepatic disease.",
        "contraindications_ja": "猫（慢性投与）、重度徐脈、II/III度房室ブロック、重度肝疾患。",
        "drug_interactions": [
            {
                "drug": "Digoxin",
                "severity": "moderate",
                "description": "Therapeutic pairing in digitalis toxicity, but phenytoin induces hepatic enzymes and can lower digoxin levels on chronic co-use",
                "description_ja": "ジギタリス中毒では治療的併用だが、フェニトインは肝酵素誘導により慢性併用でジゴキシン濃度を低下させうる",
            },
            {
                "drug": "Chloramphenicol",
                "severity": "major",
                "description": "Inhibits phenytoin metabolism — toxicity risk",
                "description_ja": "フェニトイン代謝を阻害 — 中毒リスク",
            },
        ],
    },
    {
        "id": "biotin",
        "search_aliases": ["ビオチン", "Biotin", "ビタミンB7", "ビタミンH"],
        "name": "Biotin (Vitamin B7)",
        "name_ja": "ビオチン（ビタミンB7）",
        "category": "supplements",
        "mechanism": "Water-soluble B vitamin; essential cofactor for carboxylases in fatty-acid synthesis and keratin formation. Deficiency (raw egg-white avidin, prolonged antibiotics, malnutrition) causes scaling dermatitis, brittle keratin and poor feather/hoof horn quality.",
        "mechanism_ja": "水溶性ビタミンB群。脂肪酸合成・ケラチン形成に必須のカルボキシラーゼ補酵素。欠乏（生卵白アビジン・長期抗菌薬・栄養失調）で鱗屑性皮膚炎、脆弱な角質、羽毛・蹄角質の質低下を起こす。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Hoof horn quality: 15-20 mg/head PO q24h long term — improvement requires 6-9+ months of continuous supplementation as new horn grows down (Josseck 1995 Equine Vet J).",
                "dosage_ja": "蹄角質の質改善: 15-20 mg/頭 経口 24時間毎を長期継続 — 新生角質が伸びるまで6-9ヶ月以上の継続で効果（Josseck 1995 Equine Vet J）。",
                "notes": "Adjunct to farriery and dietary balance — not a substitute for trimming/shoeing correction.",
                "notes_ja": "装蹄管理・飼料バランスの補助 — 削蹄・装蹄の是正の代替ではない。",
            },
            "bird": {
                "safe": True,
                "dosage": "Feather/beak keratin disorders, biotin-responsive dermatitis: 0.5-1.0 mg/kg PO q24h ×2-4 weeks; eliminate raw egg white from diet (avidin binds biotin; cooked egg is safe).",
                "dosage_ja": "羽毛・嘴の角質障害、ビオチン反応性皮膚炎: 0.5-1.0 mg/kg 経口 24時間毎 ×2-4週。食餌から生卵白を排除（アビジンがビオチンを結合。加熱卵は安全）。",
                "notes": "Deficiency is rare on formulated diets — investigate underlying malnutrition/malabsorption.",
                "notes_ja": "配合飼料では欠乏はまれ — 基礎にある栄養失調・吸収不良を精査。",
            },
            "dog": {
                "safe": True,
                "dosage": "Adjunct for dull coat/scaling dermatosis: 2.5-5 mg/head PO q24h (often combined with zinc and omega fatty acids).",
                "dosage_ja": "被毛光沢低下・鱗屑性皮膚症の補助: 2.5-5 mg/頭 経口 24時間毎（亜鉛・オメガ脂肪酸としばしば併用）。",
                "notes": "Water-soluble — excess is renally excreted; toxicity essentially unreported.",
                "notes_ja": "水溶性で過剰分は腎排泄 — 中毒は事実上報告なし。",
            },
        },
        "side_effects": ["Essentially none at recommended doses (water-soluble)"],
        "side_effects_ja": ["推奨用量では実質的になし（水溶性）"],
        "contraindications": "None significant.",
        "contraindications_ja": "特記すべき禁忌なし。",
        "drug_interactions": [
            {
                "drug": "Long-term antibiotics",
                "severity": "minor",
                "description": "Gut flora suppression reduces endogenous biotin synthesis — supplementation rationale, not a hazard",
                "description_ja": "腸内細菌叢の抑制で内因性ビオチン合成が低下 — 補給の根拠であり危険な相互作用ではない",
            }
        ],
    },
]
