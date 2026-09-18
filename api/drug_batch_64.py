"""Drug batch 64 – referenced-but-absent agents surfaced by the 2026-09 audit (30th sweep).

A dose-context katakana token sweep against the live text matcher confirmed
the index remains near-saturated. Two true monograph gaps and one alias gap
remained, every one referenced by the formulary's own disease content with
explicit doses:

  - Edrophonium — five of the site's own myasthenia gravis entries (dog focal
    MG, cat MG ×3 incl. the myasthenic-crisis protocol, ferret MG) prescribe
    the Tensilon test by name with doses ("エドロフォニウム試験 0.1-0.2 mg/kg
    IV", "0.25-0.5 mg/cat IV") yet the diagnostic agent itself was absent —
    the same self-referential gap previously fixed for pralidoxime, protamine,
    prednisone and tetanus antitoxin. Its defining property is the ultra-short
    (1-2 min) nicotinic response that makes it a bedside diagnostic rather
    than a therapeutic AChE inhibitor.

  - Riboflavin (vitamin B2) — the site's own avian nutrition entries dose it
    ("リボフラビン（B2）0.5-1 mg/kg PO q24h", "3-10 mg/kg 飼料" for curled-toe
    paralysis) and there are dedicated Riboflavin Deficiency disease entries
    in bird AND parakeet, plus the equine riboflavin-responsive MADD entry —
    but B2 itself was absent (B1/B7/B12 were all listed).

  - Hydroxyurea alias — the monograph exists (name_ja ヒドロキシウレア) but
    five exotic polycythemia protocols write it as the kanji compound
    「ヒドロキシ尿素 30 mg/kg PO q24h」, which never reached the keyword index.

References:
  - Shelton GD, Vet Clin North Am Small Anim Pract 2002 / JVIM — myasthenia
    gravis diagnosis; edrophonium response testing and its false positives.
  - Plumb's Veterinary Drug Handbook 10th ed — edrophonium dosing, atropine
    pretreatment/rescue; riboflavin nutritional dosing.
  - Carpenter's Exotic Animal Formulary 6th ed — avian riboflavin dosing.
  - Ritchie & Harrison, Avian Medicine — riboflavin (curled-toe paralysis in
    chicks; feed-level supplementation).
  - Valberg SJ et al. — equine multiple acyl-CoA dehydrogenase deficiency
    (riboflavin-responsive myopathy reports).
"""

DRUGS_BATCH_64 = [
    {
        "id": "edrophonium",
        "search_aliases": [
            "エドロフォニウム",
            "edrophonium",
            "テンシロン",
            "tensilon",
        ],
        "name": "Edrophonium",
        "name_ja": "エドロフォニウム（テンシロン）",
        "category": "muscle_relaxants",
        "mechanism": "Ultra-short-acting reversible acetylcholinesterase inhibitor (onset <1 min, duration 1-2 min after IV). The transient rise in synaptic acetylcholine briefly overcomes the receptor deficit of myasthenia gravis, producing a visible but fleeting return of muscle strength — the basis of the Tensilon diagnostic test. Too short-acting for therapy; treatment uses pyridostigmine.",
        "mechanism_ja": "超短時間作用型の可逆的アセチルコリンエステラーゼ阻害薬（静注後1分未満で発現、持続1-2分）。シナプス内アセチルコリンの一過性上昇が重症筋無力症の受容体不足を一時的に代償し、目に見える短時間の筋力回復を生じる — これがテンシロン診断試験の原理。作用が短すぎるため治療には用いず、治療はピリドスチグミンで行う。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Tensilon test for suspected myasthenia gravis: 0.1-0.2 mg/kg IV (small dogs start at the low end); a dramatic 1-2 min improvement in gait/strength supports MG (Shelton; Plumb's 10th ed). Videotape the response. Definitive diagnosis remains the AChR-antibody titer — a negative test does not exclude MG (false negatives in focal/chronic disease), and transient improvement can rarely occur in other neuromuscular diseases.",
                "dosage_ja": "重症筋無力症疑いのテンシロン試験: 0.1-0.2 mg/kg IV（小型犬は低用量側から）。1-2分間の劇的な歩様・筋力改善はMGを支持する（Shelton; Plumb's 10th ed）。反応は動画で記録する。確定診断はあくまで抗AChR抗体価 — 陰性でもMGは除外できず（限局型・慢性例で偽陰性）、他の神経筋疾患でも稀に一過性改善が起こりうる。",
                "notes": "Draw up atropine (0.02-0.04 mg/kg) BEFORE injecting — bradycardia, salivation, dyspnea or collapse (cholinergic crisis) is treated immediately with atropine. Availability is limited in some markets (brand Tensilon discontinued); a neostigmine response test (0.02-0.04 mg/kg IM) is the published alternative when edrophonium cannot be sourced.",
                "notes_ja": "投与前にアトロピン（0.02-0.04 mg/kg）を必ず準備 — 徐脈・流涎・呼吸困難・虚脱（コリン作動性クリーゼ）は直ちにアトロピンで拮抗する。一部市場では入手性が限られる（先発テンシロンは販売中止）— 入手不能時はネオスチグミン反応試験（0.02-0.04 mg/kg IM）が文献上の代替。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.25-0.5 mg TOTAL per cat IV (the formulary's own myasthenic-crisis protocol) — cats are given a fixed low total dose, not a full mg/kg calculation, because they are prone to cholinergic side effects. Transient improvement in ventroflexion/gait supports MG; confirm with AChR-antibody titer.",
                "dosage_ja": "0.25-0.5 mg/頭（総量）IV（本辞書の筋無力症クリーゼプロトコル参照）— 猫はコリン作動性副作用が出やすいため、mg/kg計算ではなく低い固定総量で行う。頸部腹側屈曲・歩様の一過性改善はMGを支持。確定は抗AChR抗体価で行う。",
                "notes": "Atropine drawn up before the test. SLUDGE signs (salivation, lacrimation, urination, defecation, GI cramping, emesis) or bradycardia → atropine immediately.",
                "notes_ja": "試験前にアトロピンを準備。SLUDGE症状（流涎・流涙・排尿・排便・消化管痙攣・嘔吐）や徐脈が出たら直ちにアトロピン。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Suspected myasthenia gravis: 0.1-0.2 mg/kg IV with a transient strength response supporting the diagnosis (the formulary's ferret MG entry; Quesenberry & Carpenter 4th ed — MG is rare but documented in ferrets).",
                "dosage_ja": "重症筋無力症疑い: 0.1-0.2 mg/kg IV で一過性の筋力改善があれば診断を支持（本辞書のフェレットMGエントリ; Quesenberry & Carpenter 4th ed — フェレットのMGは稀だが報告がある）。",
            },
        },
        "contraindications": "Mechanical urinary or GI obstruction (cholinergic stimulation against an obstruction). Asthmatic/bronchospastic patients (bronchoconstriction). Do not use in organophosphate/carbamate toxicosis. This is a DIAGNOSTIC agent only — its 1-2 min duration makes it useless and hazardous as maintenance therapy; chronic treatment is pyridostigmine.",
        "contraindications_ja": "尿路・消化管の機械的閉塞（閉塞に対するコリン作動性刺激）。喘息・気管支攣縮素因（気管支収縮）。有機リン・カーバメート中毒には使用しない。本剤は診断専用 — 作用持続1-2分のため維持療法には無意味かつ危険であり、慢性治療はピリドスチグミンで行う。",
        "drug_interactions": [
            {
                "drug": "Atropine",
                "effect": "Antagonist and rescue — keep drawn up during every Tensilon test",
                "effect_ja": "拮抗薬かつレスキュー — テンシロン試験では必ず準備しておく",
                "severity": "moderate",
            },
            {
                "drug": "Succinylcholine (depolarizing NMBA)",
                "effect": "Prolonged depolarizing blockade (AChE inhibition slows succinylcholine breakdown)",
                "effect_ja": "脱分極性遮断の延長（AChE阻害によりサクシニルコリン分解が遅延）",
                "severity": "major",
            },
            {
                "drug": "Pyridostigmine / neostigmine",
                "effect": "Additive cholinergic effects — testing a patient already on anticholinesterase therapy raises the cholinergic-crisis risk and blunts test interpretation",
                "effect_ja": "コリン作動性作用の相加 — 既に抗コリンエステラーゼ治療中の患者への試験はクリーゼリスクを高め、判定も困難にする",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "riboflavin_b2",
        "search_aliases": [
            "リボフラビン",
            "riboflavin",
            "ビタミンB2",
            "vitamin b2",
        ],
        "name": "Riboflavin (Vitamin B2)",
        "name_ja": "リボフラビン（ビタミンB2）",
        "category": "vitamins_minerals",
        "mechanism": "Water-soluble B vitamin; precursor of the flavin coenzymes FAD and FMN, essential cofactors of mitochondrial fatty-acid β-oxidation (acyl-CoA dehydrogenases) and the electron-transport chain. Deficiency in growing birds causes demyelination of peripheral nerves — the classic curled-toe paralysis of chicks.",
        "mechanism_ja": "水溶性ビタミンB群。フラビン補酵素FAD・FMNの前駆体で、ミトコンドリア脂肪酸β酸化（アシルCoA脱水素酵素群）と電子伝達系の必須補因子。成長期の鳥の欠乏は末梢神経の脱髄を起こす — 雛の古典的な巻き趾麻痺（curled-toe paralysis）。",
        "species_info": {
            "bird": {
                "safe": True,
                "dosage": "Riboflavin deficiency (curled-toe paralysis in chicks, dermatitis, poor growth): 0.5-1 mg/kg PO q24h until resolved (the formulary's own deficiency entries; Carpenter 6th ed). Flock/feed correction: 3-10 mg/kg of feed. Response to supplementation is rapid, but curled-toe deformity becomes permanent if treatment is delayed — treat on suspicion. Convert to a balanced pelleted diet as the definitive fix.",
                "dosage_ja": "リボフラビン欠乏症（雛の巻き趾麻痺・皮膚炎・成長不良）: 0.5-1 mg/kg PO q24h を改善まで（本辞書の欠乏症エントリ; Carpenter 6th ed）。群・飼料での是正: 飼料1 kgあたり3-10 mg。補給への反応は迅速だが、巻き趾変形は治療が遅れると永続化するため疑い時点で治療する。根本治療はバランスペレット食への移行。",
                "notes": "Usually given as part of a B-complex preparation; riboflavin is heat- and light-labile, so feed stored poorly or overcooked loses activity. Harmless yellow discoloration of urates/droppings during supplementation is expected.",
                "notes_ja": "通常はビタミンB複合体製剤の一部として投与。リボフラビンは熱・光に不安定で、保存不良・過加熱の飼料は力価が失われる。補給中の尿酸塩・糞の無害な黄色着色は正常。",
            },
            "horse": {
                "safe": True,
                "dosage": "Riboflavin-responsive multiple acyl-CoA dehydrogenase deficiency (MADD/atypical myopathy spectrum): supplementation has produced partial improvement in reported cases; no validated equine dose is established — B-complex-based riboflavin supplementation is used empirically alongside the disease protocol's low-fat/high-carbohydrate diet and L-carnitine 50-100 mg/kg PO q24h (the formulary's MADD entry).",
                "dosage_ja": "リボフラビン反応性の多種アシルCoA脱水素酵素欠損症（MADD/非典型ミオパチー系）: 補充で一部改善の報告があるが、検証された馬の用量は確立されていない — B複合体ベースのリボフラビン補充を、本辞書MADDエントリの低脂肪・高炭水化物食＋L-カルニチン 50-100 mg/kg PO q24h と併用して経験的に用いる。",
            },
        },
        "contraindications": "Essentially non-toxic (water-soluble; excess is renally excreted and colors urine yellow). The only real failure mode is treating the wrong disease — curled-toe-like signs in chicks also occur with vitamin E/selenium deficiency and avian encephalomyelitis, which do not respond to riboflavin.",
        "contraindications_ja": "実質的に無毒（水溶性で過剰分は腎排泄され尿を黄色に着色する）。唯一の実害は誤った疾患への投与 — 雛の巻き趾様症状はビタミンE/セレン欠乏や鳥脳脊髄炎でも起こり、これらはリボフラビンに反応しない。",
        "drug_interactions": [],
    },
]
