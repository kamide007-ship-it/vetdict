"""Drug batch 46 – referenced-but-absent agents surfaced by the 2026-08 audit (15th sweep).

The emergency-protocol key-drug linkification audit (every key drug in the
救急タブ must resolve in the formulary) cross-checked against treatment-text
references found three agents that VetDict's own content instructs clinicians
to use — with explicit doses — yet were absent from the formulary:

  - ジアゾキシド (diazoxide, Proglycem): the ferret/canine insulinoma entries
    and the hypoglycemia emergency protocol cite "ジアゾキシド 5-30 mg/kg" —
    44 references across treatment texts — yet the standard second-line
    medical therapy for insulinoma was absent from the dictionary.
  - リバロキサバン (rivaroxaban, Xarelto): the feline aortic thromboembolism
    emergency protocol lists it as a key drug and ATE/thrombosis entries
    reference it, yet no direct oral factor Xa inhibitor existed (heparin,
    LMWHs and clopidogrel were the only antithrombotics).
  - マムシ抗毒素血清 (Gloydius blomhoffii antivenom, equine origin): the
    mamushi-envenomation emergency protocol lists it as a key drug and the
    snakebite disease entries reference it — the single most
    Japan-clinically-relevant antivenom, absent from the dictionary.
  - グルカゴン (glucagon): the hypoglycemia emergency protocol lists it as a
    key drug and 20 treatment references cite the CRI protocol for refractory
    hypoglycemia (insulinoma crisis, xylitol toxicosis) — absent from the
    dictionary.

References:
  - Quesenberry & Carpenter, Ferrets, Rabbits and Rodents 4th ed — ferret
    insulinoma: prednisolone first line, diazoxide 5-30 mg/kg PO q12h added
    when glucose control is lost.
  - Goutal CM et al. J Vet Emerg Crit Care 2012 — canine insulinoma review:
    diazoxide 5-30 mg/kg/day medical management.
  - Plumb's Veterinary Drug Handbook 10th ed — diazoxide adverse effects
    (GI signs, sodium/water retention, hyperglycemia), thiazide interaction.
  - Blais MC et al. J Vet Emerg Crit Care 2019 (CURATIVE consensus) —
    rivaroxaban dogs 1-2 mg/kg PO q24h, cats 0.5-1 mg/kg (2.5 mg/cat) PO
    q24h for thromboprophylaxis; bleeding is the principal adverse effect.
  - Dixon-Jimenez AC et al. J Vet Emerg Crit Care 2016 — rivaroxaban
    2.5 mg/cat PO q24h pharmacodynamics: predictable anti-Xa effect, well
    tolerated.
  - Yang VK et al. J Vet Cardiol 2016 — rivaroxaban pharmacokinetics in dogs.
  - Hifumi T et al. J Intensive Care 2015 — mamushi (Gloydius blomhoffii)
    envenomation: antivenom within 6 hours reduces severity progression
    (human data; the veterinary product is the same equine-origin serum).
  - Plumb's Veterinary Drug Handbook 10th ed — glucagon 50 ng/kg IV bolus
    then 5-40 ng/kg/min CRI for insulin-overdose / insulinoma-crisis
    hypoglycemia refractory to dextrose.
  - Fischer JR et al. JAVMA 2000;216:1073 — glucagon CRI for refractory
    hypoglycemia in a dog with insulinoma.
  - 日本臨床獣医学フォーラム・症例集積 — 犬マムシ咬傷は支持療法単独でも
    多くが生存するが、重度全身症状（急速進行性腫脹・凝固障害・溶血・
    急性腎障害リスク）では抗毒素血清の早期投与を考慮する。
"""

DRUGS_BATCH_46: list[dict] = [
    {
        "id": "diazoxide",
        "search_aliases": [
            "ジアゾキシド",
            "プログリセム",
            "Diazoxide",
            "Proglycem",
        ],
        "name": "Diazoxide (Proglycem)",
        "name_ja": "ジアゾキシド（プログリセム）",
        "category": "endocrine",
        "mechanism": "Benzothiadiazine that opens ATP-sensitive potassium channels on pancreatic beta cells, directly suppressing insulin secretion; also stimulates hepatic glycogenolysis/gluconeogenesis and reduces peripheral glucose uptake. The standard second-line medical therapy for insulinoma when glucocorticoids alone no longer control hypoglycemia.",
        "mechanism_ja": "膵β細胞のATP感受性カリウムチャネルを開口してインスリン分泌を直接抑制するベンゾチアジアジン系薬。肝グリコーゲン分解・糖新生の促進と末梢グルコース取り込みの抑制作用も持つ。グルココルチコイド単独で低血糖を管理できなくなったインスリノーマの標準的第二選択内科治療。",
        "species_info": {
            "ferret": {
                "safe": True,
                "dosage": "Insulinoma: start 5 mg/kg PO q12h with food, titrate to effect up to 30 mg/kg PO q12h (Quesenberry & Carpenter 4th ed). Add to prednisolone when steroids alone no longer maintain glucose >60-70 mg/dL; continue frequent small meals.",
                "dosage_ja": "インスリノーマ: 5 mg/kg 経口 12時間毎（食事と共に）から開始し、効果を見ながら最大30 mg/kg 12時間毎まで漸増（Quesenberry & Carpenter 4th ed）。プレドニゾロン単独で血糖>60-70 mg/dLを維持できなくなった時点で追加。頻回少量給餌は継続。",
                "notes": "Does not shrink the tumor — palliates hypoglycemia only. GI upset is the most common adverse effect; give with food. Surgical debulking remains the definitive option.",
                "notes_ja": "腫瘍自体は縮小させない（低血糖の緩和のみ）。最多の副作用は消化器症状 — 必ず食事と共に投与。根治的選択肢は外科的減容術。",
            },
            "dog": {
                "safe": True,
                "dosage": "Insulinoma (unresectable/recurrent): 5 mg/kg PO q12h with food, titrate up to 30 mg/kg/day divided q12h (Goutal 2012 JVECC; Plumb's 10th ed). Combine with prednisolone and frequent small low-simple-sugar meals.",
                "dosage_ja": "インスリノーマ（切除不能・再発例）: 5 mg/kg 経口 12時間毎（食事と共に）から開始し、最大30 mg/kg/日（12時間毎分割）まで漸増（Goutal 2012 JVECC; Plumb's 10th ed）。プレドニゾロン・頻回少量給餌（単純糖回避）と併用。",
                "notes": "Monitor for sodium/water retention (caution in cardiac disease), GI signs, and rarely bone marrow suppression/hepatotoxicity — periodic CBC/chemistry recommended.",
                "notes_ja": "ナトリウム・水分貯留（心疾患では注意）、消化器症状、まれに骨髄抑制・肝毒性をモニタリング — 定期的なCBC・生化学検査を推奨。",
            },
            "cat": {
                "safe": True,
                "dosage": "Insulinoma is rare in cats; anecdotal dosing 5-30 mg/kg/day PO divided q12h extrapolated from dogs (limited data).",
                "dosage_ja": "猫のインスリノーマは稀。犬からの外挿で5-30 mg/kg/日 経口 12時間毎分割（データ限定的）。",
                "notes": "Limited feline data — titrate cautiously with glucose monitoring.",
                "notes_ja": "猫でのデータは限定的 — 血糖モニタリング下で慎重に漸増。",
            },
        },
        "side_effects": "Anorexia, vomiting, diarrhea (give with food); sodium and water retention; hypertrichosis; hyperglycemia/DKA with overdose; rarely thrombocytopenia, hepatotoxicity",
        "side_effects_ja": "食欲不振・嘔吐・下痢（食事と共に投与で軽減）、ナトリウム・水分貯留、多毛、過量で高血糖/DKA、まれに血小板減少・肝毒性",
        "contraindications": "Hypersensitivity to thiazides/benzothiadiazines. Use with caution in congestive heart failure (fluid retention) and hepatic disease. Not a substitute for emergency IV dextrose in hypoglycemic crisis",
        "contraindications_ja": "チアジド/ベンゾチアジアジン過敏症。うっ血性心不全（体液貯留）・肝疾患では慎重投与。低血糖クリーゼの緊急対応は50%ブドウ糖静注であり本剤で代替しない",
        "drug_interactions": [
            {
                "drug": "Thiazide diuretics (hydrochlorothiazide)",
                "effect": "Potentiate the hyperglycemic effect — occasionally combined deliberately in refractory insulinoma, but the combination increases the risk of severe hyperglycemia and hypotension; use only with close monitoring",
                "effect_ja": "高血糖作用を増強 — 難治性インスリノーマで意図的に併用されることがあるが、重度高血糖・低血圧のリスクが増すため厳密なモニタリング下でのみ",
                "severity": "moderate",
            },
            {
                "drug": "Insulin / glucose-lowering agents",
                "effect": "Directly opposing pharmacology — concurrent use is irrational",
                "effect_ja": "薬理作用が真逆 — 併用は不合理",
                "severity": "info",
            },
        ],
    },
    {
        "id": "rivaroxaban",
        "search_aliases": [
            "リバロキサバン",
            "イグザレルト",
            "Rivaroxaban",
            "Xarelto",
        ],
        "name": "Rivaroxaban (Xarelto)",
        "name_ja": "リバロキサバン（イグザレルト）",
        "category": "anticoagulants",
        "mechanism": "Direct oral factor Xa inhibitor (DOAC). Selectively blocks free and clot-bound factor Xa, interrupting thrombin generation without requiring antithrombin. Predictable oral pharmacokinetics allow fixed once-daily dosing without routine coagulation monitoring — the practical advantage over unfractionated heparin and LMWH injections for outpatient thromboprophylaxis.",
        "mechanism_ja": "直接経口第Xa因子阻害薬（DOAC）。遊離型・血栓結合型双方のXa因子を選択的に阻害し、アンチトロンビン非依存的にトロンビン生成を遮断する。経口で薬物動態が予測可能なため、定期的な凝固モニタリングなしの固定用量1日1回投与が可能 — 外来血栓予防で未分画ヘパリン・LMWH注射に対する実用上の利点。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Aortic thromboembolism (ATE) treatment/secondary prevention: 0.5-1 mg/kg PO q24h — practical fixed dose 2.5 mg/cat PO q24h (Dixon-Jimenez 2016 JVECC; CURATIVE consensus Blais 2019). High-risk or recurrent ATE: may combine with clopidogrel 18.75 mg/cat q24h as dual therapy with bleeding-risk counselling.",
                "dosage_ja": "動脈血栓塞栓症（ATE）治療・二次予防: 0.5-1 mg/kg 経口 24時間毎 — 実用固定用量 2.5 mg/頭 経口 24時間毎（Dixon-Jimenez 2016 JVECC; CURATIVE合意 Blais 2019）。高リスク・再発ATEではクロピドグレル18.75 mg/頭 24時間毎との2剤併用も選択肢（出血リスク説明の上）。",
                "notes": "Clopidogrel remains the evidence-based first-line antithrombotic for feline ATE prevention (FATCAT 2015); rivaroxaban is the anticoagulant of choice when factor-Xa inhibition is added.",
                "notes_ja": "猫ATE予防のエビデンス上の第一選択は依然クロピドグレル（FATCAT 2015）。抗凝固を上乗せする場合のXa阻害薬として本剤が選択される。",
            },
            "dog": {
                "safe": True,
                "dosage": "Thromboprophylaxis (IMHA, PLE/PLN, hyperadrenocorticism, cardiac disease): 1-2 mg/kg PO q24h (CURATIVE consensus Blais 2019; Yang 2016 PK). Give consistently with or without food.",
                "dosage_ja": "血栓予防（IMHA・蛋白漏出性腸症/腎症・副腎皮質機能亢進症・心疾患）: 1-2 mg/kg 経口 24時間毎（CURATIVE合意 Blais 2019; Yang 2016 PK）。食事条件は一定にして投与。",
                "notes": "Discontinue 24-48h before invasive procedures. No practical reversal agent in veterinary medicine — bleeding is managed with drug withdrawal and supportive care/plasma.",
                "notes_ja": "侵襲的処置の24-48時間前に休薬。獣医療で実用的な拮抗薬はない — 出血時は休薬＋支持療法/血漿で管理。",
            },
        },
        "side_effects": "Bleeding (the principal adverse effect — gingival, GI, urinary, or at venipuncture sites); GI upset uncommon",
        "side_effects_ja": "出血（主要な副作用 — 歯肉・消化管・尿路・採血部位）。消化器症状はまれ",
        "contraindications": "Active clinically significant hemorrhage; severe hepatic dysfunction with coagulopathy; use with caution in significant renal impairment (reduced clearance). Discontinue before surgery",
        "contraindications_ja": "臨床的に重大な活動性出血、凝固障害を伴う重度肝機能不全。高度腎機能低下ではクリアランス低下に注意。手術前は休薬",
        "drug_interactions": [
            {
                "drug": "Clopidogrel / aspirin (antiplatelets)",
                "effect": "Additive bleeding risk — dual therapy is used deliberately in high-risk feline ATE but requires owner counselling and monitoring for hemorrhage",
                "effect_ja": "出血リスクが相加的 — 高リスク猫ATEでは意図的に2剤併用されるが、飼い主への説明と出血モニタリングが必須",
                "severity": "moderate",
            },
            {
                "drug": "NSAIDs",
                "effect": "Increased GI bleeding risk — avoid concurrent use where possible",
                "effect_ja": "消化管出血リスク増加 — 可能な限り併用を避ける",
                "severity": "moderate",
            },
            {
                "drug": "Ketoconazole/itraconazole (CYP3A/P-gp inhibitors)",
                "effect": "Increase rivaroxaban exposure and bleeding risk",
                "effect_ja": "リバロキサバンの血中濃度と出血リスクを上昇させる",
                "severity": "moderate",
            },
            {
                "drug": "Heparin / enoxaparin / warfarin",
                "effect": "Do not co-administer therapeutic anticoagulants — additive anticoagulation with major hemorrhage risk (sequential transition only)",
                "effect_ja": "治療量の抗凝固薬同士は併用しない — 抗凝固作用が相加し大出血リスク（切替時の逐次移行のみ）",
                "severity": "major",
            },
        ],
    },
    {
        "id": "glucagon",
        "search_aliases": [
            "グルカゴン",
            "Glucagon",
        ],
        "name": "Glucagon",
        "name_ja": "グルカゴン",
        "category": "endocrine",
        "mechanism": "Pancreatic alpha-cell counter-regulatory hormone. Activates hepatic glucagon receptors (Gs/cAMP) to drive glycogenolysis and gluconeogenesis, raising blood glucose independently of exogenous dextrose — the rescue option for hypoglycemia refractory to, or rebounding through, dextrose CRIs (insulinoma crisis stimulates further insulin release with each dextrose bolus; glucagon avoids that rebound loop).",
        "mechanism_ja": "膵α細胞の拮抗調節ホルモン。肝グルカゴン受容体（Gs/cAMP）を介してグリコーゲン分解・糖新生を駆動し、外因性ブドウ糖に依存せず血糖を上昇させる。デキストロースCRIに不応・反跳する低血糖のレスキュー選択肢（インスリノーマクリーゼではブドウ糖ボーラス毎にさらなるインスリン分泌が刺激される — グルカゴンはこの反跳ループを回避できる）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Refractory hypoglycemia (insulinoma crisis, insulin overdose, xylitol toxicosis): 50 ng/kg IV bolus, then CRI 5-40 ng/kg/min titrated to maintain glucose >60 mg/dL (Plumb's 10th ed; Fischer JAVMA 2000). Dilute 1 mg vial in 1 L 0.9% NaCl → 1,000 ng/mL working solution.",
                "dosage_ja": "難治性低血糖（インスリノーマクリーゼ・インスリン過量・キシリトール中毒）: 50 ng/kg 静注ボーラス後、CRI 5-40 ng/kg/分を血糖>60 mg/dL維持まで漸増（Plumb's 10th ed; Fischer JAVMA 2000）。1 mgバイアルを生理食塩水1 Lに希釈し1,000 ng/mL作業液とする。",
                "notes": "Adjunct to — not a replacement for — dextrose supplementation and frequent feeding. Wean the CRI gradually while monitoring glucose q1-2h; rebound hypoglycemia can follow abrupt discontinuation.",
                "notes_ja": "ブドウ糖補給・頻回給餌の代替ではなく補助。CRIは血糖を1-2時間毎にモニタリングしながら漸減 — 急な中止で反跳性低血糖が起こりうる。",
            },
            "cat": {
                "safe": True,
                "dosage": "Refractory hypoglycemia: 50 ng/kg IV bolus then CRI 5-40 ng/kg/min, extrapolated from canine dosing (limited feline data).",
                "dosage_ja": "難治性低血糖: 50 ng/kg 静注ボーラス後 CRI 5-40 ng/kg/分（犬からの外挿、猫のデータは限定的）。",
                "notes": "Same dilution and weaning cautions as dogs.",
                "notes_ja": "希釈法・漸減時の注意は犬と同様。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Insulinoma hypoglycemic crisis refractory to dextrose: CRI 5-40 ng/kg/min after 50 ng/kg IV bolus (extrapolated; Quesenberry & Carpenter 4th ed lists dextrose + glucocorticoids first).",
                "dosage_ja": "デキストロース不応のインスリノーマ低血糖クリーゼ: 50 ng/kg 静注ボーラス後 CRI 5-40 ng/kg/分（外挿。Quesenberry & Carpenter 4th ed はデキストロース＋グルココルチコイドを先行）。",
                "notes": "Reserve for crises not controlled by dextrose CRI + dexamethasone.",
                "notes_ja": "デキストロースCRI＋デキサメタゾンで管理できないクリーゼに温存。",
            },
        },
        "side_effects": "Vomiting/nausea (dose-dependent), tachycardia, rebound hypoglycemia after abrupt discontinuation, hypokalemia with prolonged infusion",
        "side_effects_ja": "嘔吐・悪心（用量依存性）、頻脈、急な中止後の反跳性低血糖、長時間投与での低カリウム血症",
        "contraindications": "Pheochromocytoma (catecholamine release → hypertensive crisis); insulinoma glucagon use is deliberate crisis management — expect it to stimulate some insulin co-release and monitor closely",
        "contraindications_ja": "褐色細胞腫（カテコールアミン放出→高血圧クリーゼ）。インスリノーマでの使用は意図的なクリーゼ管理 — インスリン共放出の刺激がありうるため厳密にモニタリング",
        "drug_interactions": [
            {
                "drug": "Insulin",
                "effect": "Direct pharmacological antagonists — glucagon is the rescue for insulin overdose",
                "effect_ja": "直接の薬理学的拮抗 — グルカゴンはインスリン過量投与のレスキュー薬",
                "severity": "info",
            },
        ],
    },
    {
        "id": "mamushi_antivenom",
        "search_aliases": [
            "マムシ抗毒素血清",
            "マムシ抗毒素",
            "抗マムシ血清",
            "Mamushi antivenin",
            "Mamushi antivenom",
        ],
        "name": "Mamushi Antivenom (Equine-Origin Serum)",
        "name_ja": "乾燥まむしウマ抗毒素（マムシ抗毒素血清）",
        "category": "biologics",
        "mechanism": "Equine-origin immunoglobulin (freeze-dried antitoxic serum) raised against Gloydius blomhoffii (Japanese mamushi) venom. Neutralizes circulating venom components — hemorrhagic metalloproteinases and phospholipase A2 — limiting progressive swelling, coagulopathy, hemolysis and venom-induced acute kidney injury. Efficacy is time-dependent: it neutralizes free venom, not established tissue damage.",
        "mechanism_ja": "ニホンマムシ（Gloydius blomhoffii）毒素に対するウマ由来免疫グロブリン（乾燥抗毒素血清）。血中の毒素成分（出血性メタロプロテアーゼ・ホスホリパーゼA2）を中和し、進行性腫脹・凝固障害・溶血・毒素性急性腎障害を抑制する。効果は時間依存性 — 遊離毒素を中和するもので、成立した組織障害は戻せない。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Severe/systemic mamushi envenomation: 1 vial (6,000 units) diluted in isotonic crystalloid, slow IV over 30-60 min, ideally within 4-6 hours of the bite (time-dependent efficacy — Hifumi 2015). Premedicate with an antihistamine ± glucocorticoid and have epinephrine drawn up (equine-origin serum — anaphylaxis risk).",
                "dosage_ja": "重度・全身性マムシ咬傷: 1バイアル（6,000単位）を等張晶質液に希釈し30-60分かけて緩徐静注。咬傷後4-6時間以内の投与が理想（効果は時間依存性 — Hifumi 2015）。ウマ由来血清のためアナフィラキシーリスク — 抗ヒスタミン薬±グルココルチコイドで前処置し、エピネフリンを準備した上で投与。",
                "notes": "Many canine mamushi bites recover with supportive care alone (fluids, analgesia, antibiotics for secondary infection) — reserve antivenom for severe envenomation: rapidly progressive swelling, coagulopathy, gross hemoglobinuria/hemolysis, or AKI risk. Watch for serum sickness 1-2 weeks post-administration.",
                "notes_ja": "犬のマムシ咬傷の多くは支持療法単独（輸液・鎮痛・二次感染への抗菌薬）で回復する — 抗毒素は重度咬傷（急速進行性腫脹・凝固障害・肉眼的ヘモグロビン尿/溶血・急性腎障害リスク）に温存。投与後1-2週の血清病に注意。",
            },
            "cat": {
                "safe": True,
                "dosage": "Severe envenomation: 1 vial (6,000 units) diluted, slow IV — same time window and anaphylaxis precautions as dogs (feline data are limited to case reports).",
                "dosage_ja": "重度咬傷: 1バイアル（6,000単位）希釈・緩徐静注 — 投与時間枠・アナフィラキシー対策は犬と同様（猫のデータは症例報告レベル）。",
                "notes": "Cats are bitten less often and frequently on the limbs/face; monitor renal values and PCV for hemolysis.",
                "notes_ja": "猫の咬傷は四肢・顔面が多い。腎数値と溶血（PCV）をモニタリング。",
            },
        },
        "side_effects": "Acute hypersensitivity/anaphylaxis (equine protein); delayed serum sickness (fever, urticaria, arthralgia) 1-2 weeks later",
        "side_effects_ja": "急性過敏反応/アナフィラキシー（ウマ蛋白）、投与1-2週間後の遅発性血清病（発熱・蕁麻疹・関節痛）",
        "contraindications": "Known hypersensitivity to equine serum products is a relative contraindication — in life-threatening envenomation, administer under intensive monitoring with epinephrine ready. Do not delay severe-case administration for skin testing",
        "contraindications_ja": "ウマ血清製剤への過敏症既往は相対的禁忌 — 生命に関わる咬傷ではエピネフリン準備・集中監視下で投与。重症例で皮内テストのために投与を遅らせない",
        "drug_interactions": [
            {
                "drug": "Epinephrine / diphenhydramine (premedication set)",
                "effect": "Not an interaction but a co-administration requirement — anaphylaxis rescue must be immediately available whenever equine-origin serum is infused",
                "effect_ja": "相互作用ではなく併用準備の要件 — ウマ由来血清の点滴中はアナフィラキシー救急薬を即座に使える状態にしておく",
                "severity": "info",
            },
        ],
    },
]
