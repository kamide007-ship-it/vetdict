"""Drug batch 33 – referenced-but-absent drugs surfaced by the 2026-08 audit.

An is-referenced-but-absent sweep of (a) drug_interactions back-references,
(b) disease treatment protocols in the served DB and (c) anesthesia protocol
drug rows found 14 drugs that VetDict's own content tells clinicians to use
but the formulary did not carry:

  - Pyrimethamine   — 22 disease entries (EPM w/ sulfadiazine = FDA-approved
                      ReBalance regimen, toxoplasmosis, neosporosis, avian
                      atoxoplasmosis) reference it with no formulary entry.
  - Quinidine       — the gold-standard conversion drug for equine atrial
                      fibrillation (8 horse disease entries; digoxin's own
                      interaction list references it).
  - Valacyclovir    — equine EHV-1 myeloencephalopathy protocols reference it;
                      entry carries the critical safety flag: FATAL in cats.
  - Meclizine       — 11 species' vestibular-disease protocols reference it.
  - Colchicine      — avian/reptile gout and amyloidosis entries reference it
                      (plus canine Shar-Pei fever/renal amyloidosis use).
  - Leuprolide      — avian chronic egg laying + ferret adrenal disease
                      protocols reference it (7 species).
  - Niacinamide     — tetracycline+niacinamide combo for canine immune-mediated
                      dermatoses (DLE, pemphigus foliaceus, SLO) in 12 entries.
  - Dexrazoxane     — doxorubicin's entry names it as the extravasation
                      antidote; a clinician facing extravasation had no entry.
  - Methotrexate    — 10 interaction back-references (penicillins, sulfas,
                      PPIs, l-asparaginase, leflunomide) pointed at a
                      non-existent entry.
  - Thiamine (B1)   — 22 disease entries (feline thiamine deficiency,
                      thiaminase in frozen-fish diets for reptiles) reference it.
  - L-Carnitine     — canine DCM and feline hepatic lipidosis adjunct in 14
                      entries.
  - Paromomycin     — cryptosporidiosis protocols across 17 species; entry
                      carries the feline renal-failure/deafness warning.
  - EMLA cream      — rabbit and guinea-pig anesthesia protocols reference it
                      (pre-catheter topical anesthesia) with no entry; carries
                      the feline methemoglobinemia caution.
  - Dextrose 50%    — ferret insulinoma emergency protocol and 19 species'
                      hypoglycemia treatments reference it; entry carries the
                      mandatory peripheral-line dilution warning.

References:
  - Plumb's Veterinary Drug Handbook, 10th ed.
  - Carpenter's Exotic Animal Formulary, 6th ed.
  - Reed SM et al. JVIM 2016;30(2):491-502 — EPM ACVIM consensus (pyrimethamine/
    sulfadiazine 1 + 20 mg/kg PO q24h ≥ 90 days).
  - Reef VB et al. JVIM 2014;28(3):749-761 — ACVIM consensus, equine arrhythmias
    (quinidine sulfate 22 mg/kg via NGT q2h, QRS-prolongation stop rules).
  - Maxwell LK et al. J Vet Pharmacol Ther 2017 — valacyclovir loading regimen
    for EHV-1 (27 mg/kg q8h load → 18 mg/kg q12h).
  - Nasisse MP et al. AJVR 1997 — acyclovir/valacyclovir fatal toxicity in cats.
  - White SD et al. JAVMA 1992;200(10):1497-1500 — tetracycline & niacinamide
    for canine immune-mediated dermatoses.
  - Venable RO et al. JAVMA 2012;240(3):304-307 — dexrazoxane for doxorubicin
    extravasation in dogs.
  - Gookin JL et al. JAVMA 1999;215(12):1821-1823 — paromomycin-associated
    acute renal failure and deafness in cats.
  - Wagner RA et al. JAVMA 2005;227(8):1272-1274 — depot leuprolide for ferret
    adrenocortical disease.
  - Flecknell PA. Laboratory Animal Anaesthesia, 4th ed — EMLA for small-mammal
    venous access.
"""

from __future__ import annotations

DRUGS_BATCH_33: list[dict] = [
    {
        "id": "pyrimethamine",
        "name": "Pyrimethamine",
        "name_ja": "ピリメタミン",
        "category": "antiparasitics",
        "mechanism": (
            "Dihydrofolate reductase inhibitor with high affinity for the protozoal "
            "enzyme. Blocks folate-dependent nucleic acid synthesis in apicomplexan "
            "protozoa (Sarcocystis neurona, Toxoplasma gondii, Neospora caninum, "
            "Hepatozoon, avian Atoxoplasma). Synergistic with sulfonamides, which "
            "block the upstream step (dihydropteroate synthase) of the same pathway."
        ),
        "mechanism_ja": (
            "ジヒドロ葉酸還元酵素阻害薬。原虫の同酵素への親和性が高く、アピコンプレクサ門原虫"
            "（Sarcocystis neurona・Toxoplasma gondii・Neospora caninum・Hepatozoon・"
            "鳥のAtoxoplasma）の葉酸依存性核酸合成を阻害する。同経路の上流"
            "（ジヒドロプテロイン酸合成酵素）を阻害するサルファ剤と相乗的に作用する。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": (
                    "EPM: pyrimethamine 1 mg/kg + sulfadiazine 20 mg/kg PO q24h for "
                    "at least 90-120 days (FDA-approved ReBalance regimen; ACVIM "
                    "consensus, Reed 2016). Give 1 h before feeding hay."
                ),
                "dosage_ja": (
                    "EPM（馬原虫性脊髄脳炎）: ピリメタミン 1 mg/kg＋スルファジアジン 20 mg/kg "
                    "経口 1日1回、最低90-120日間（FDA承認ReBalanceレジメン。ACVIMコンセンサス "
                    "Reed 2016）。乾草給餌の1時間前に投与。"
                ),
                "notes": (
                    "Monitor CBC every 4 weeks — folate-antagonist marrow suppression "
                    "(anemia, leukopenia) is the dose-limiting toxicity. Avoid in pregnant "
                    "mares (congenital defects reported, worsened by concurrent high-dose "
                    "folic acid supplementation)."
                ),
                "notes_ja": (
                    "4週毎にCBCを監視 — 葉酸拮抗による骨髄抑制（貧血・白血球減少）が用量制限毒性。"
                    "妊娠馬では回避（先天異常の報告あり。高用量葉酸の併用でむしろ悪化するため"
                    "安易な葉酸大量補給も行わない）。"
                ),
            },
            "dog": {
                "safe": True,
                "dosage": (
                    "Toxoplasmosis/neosporosis: 1 mg/kg PO q24h for 14-28 days combined "
                    "with a sulfonamide. Hepatozoon americanum (TCP protocol): 0.25 mg/kg "
                    "PO q24h × 14 days with trimethoprim-sulfa + clindamycin, then "
                    "long-term decoquinate."
                ),
                "dosage_ja": (
                    "トキソプラズマ症/ネオスポラ症: 1 mg/kg 経口 1日1回 14-28日間、サルファ剤と併用。"
                    "Hepatozoon americanum（TCPプロトコル）: 0.25 mg/kg 経口 1日1回 14日間"
                    "（トリメトプリム・サルファ＋クリンダマイシン併用）、以後デコキネート長期投与。"
                ),
                "notes": (
                    "Supplement folinic acid (not folic acid) if cytopenias develop; "
                    "monitor CBC weekly on prolonged courses."
                ),
                "notes_ja": (
                    "血球減少が出た場合はホリン酸（葉酸ではなくフォリン酸）を補給。長期投与ではCBCを週1回監視。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": (
                    "Rarely used — clindamycin is first-line for feline toxoplasmosis. "
                    "If used: 0.25-0.5 mg/kg PO q12h with a sulfonamide, short course."
                ),
                "dosage_ja": (
                    "使用は稀 — 猫トキソプラズマ症の第一選択はクリンダマイシン。"
                    "使用する場合: 0.25-0.5 mg/kg 経口 12時間毎、サルファ剤併用で短期間。"
                ),
                "notes": "Cats are sensitive to folate-antagonist marrow suppression; monitor CBC.",
                "notes_ja": "猫は葉酸拮抗性骨髄抑制に感受性が高い。CBCを監視。",
            },
            "bird": {
                "safe": True,
                "dosage": (
                    "Atoxoplasmosis/Leucocytozoon adjunct: 0.5 mg/kg PO q12h × 14-28 "
                    "days, usually with a sulfonamide (Carpenter 6th ed)."
                ),
                "dosage_ja": (
                    "アトキソプラズマ症/ロイコチトゾーン症の補助: 0.5 mg/kg 経口 12時間毎 "
                    "14-28日間。通常サルファ剤と併用（Carpenter第6版）。"
                ),
                "notes": "Marrow suppression on prolonged courses; monitor droppings and weight.",
                "notes_ja": "長期投与で骨髄抑制。糞便と体重を監視。",
            },
        },
        "side_effects": (
            "Bone marrow suppression (anemia, leukopenia, thrombocytopenia — "
            "folate antagonism), anorexia, vomiting/diarrhoea, depression. In "
            "horses: transient worsening of neurologic signs early in EPM "
            "treatment ('treatment crisis') can occur."
        ),
        "side_effects_ja": (
            "骨髄抑制（貧血・白血球減少・血小板減少 — 葉酸拮抗による）、食欲不振、嘔吐/下痢、"
            "沈うつ。馬ではEPM治療初期に神経症状の一過性悪化（治療クリーゼ）が起こりうる。"
        ),
        "contraindications": (
            "Pregnancy (teratogenic — folate antagonist), pre-existing bone marrow "
            "suppression, severe hepatic disease. Use with caution in anemic animals."
        ),
        "contraindications_ja": ("妊娠（葉酸拮抗による催奇形性）、既存の骨髄抑制、重度肝疾患。貧血動物では慎重投与。"),
        "drug_interactions": [
            {
                "drug": "trimethoprim_sulfa",
                "effect": "Additive folate antagonism — increased marrow-suppression risk; monitor CBC when combined (intentional synergy in EPM/TCP protocols)",
                "effect_ja": "葉酸拮抗が相加的 — 骨髄抑制リスク増加。併用時（EPM/TCPプロトコルでは意図的な相乗）はCBC監視",
            },
            {
                "drug": "sulfadiazine",
                "effect": "Intentional synergistic combination (sequential folate-pathway blockade) — the standard EPM regimen",
                "effect_ja": "意図的な相乗的併用（葉酸経路の逐次阻害）— EPM標準レジメン",
            },
            {
                "drug": "Folic acid (high dose)",
                "effect": "High-dose folic acid does not protect and may worsen congenital defects in pregnant mares on pyrimethamine; use folinic acid for rescue instead",
                "effect_ja": "高用量葉酸は保護的でなく、妊娠馬では先天異常をむしろ悪化させうる。レスキューにはフォリン酸を使用",
            },
        ],
    },
    {
        "id": "quinidine",
        "name": "Quinidine Sulfate",
        "name_ja": "キニジン硫酸塩",
        "category": "antiarrhythmics",
        "mechanism": (
            "Class IA antiarrhythmic. Blocks fast sodium channels (slows phase-0 "
            "depolarisation) and potassium channels (prolongs refractory period), "
            "with vagolytic effects. The classic drug for pharmacologic conversion "
            "of atrial fibrillation in horses (ACVIM consensus, Reef 2014)."
        ),
        "mechanism_ja": (
            "クラスIA抗不整脈薬。速いナトリウムチャネルを遮断（第0相脱分極を減速）し、"
            "カリウムチャネル遮断により不応期を延長。迷走神経遮断作用ももつ。"
            "馬の心房細動の薬理学的洞調律復帰における古典的第一選択薬"
            "（ACVIMコンセンサス Reef 2014）。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": (
                    "Atrial fibrillation conversion: quinidine sulfate 22 mg/kg via "
                    "nasogastric tube q2h until conversion, adverse effects, or 4-6 "
                    "doses; then q6h if continuing. Continuous ECG monitoring is "
                    "mandatory. STOP if QRS widens > 25% of pre-treatment duration."
                ),
                "dosage_ja": (
                    "心房細動の洞調律復帰: キニジン硫酸塩 22 mg/kg 経鼻胃管投与 2時間毎、"
                    "復帰・副作用出現・4-6回投与のいずれかまで。継続する場合は以後6時間毎。"
                    "持続心電図監視が必須。QRS幅が治療前の25%超に延長したら投与中止。"
                ),
                "notes": (
                    "Best success in AF < 3 months' duration with no significant "
                    "structural disease. Toxicity: colic, diarrhoea, paraphimosis, "
                    "urticaria, nasal edema, hypotension, ataxia, rapid SVT "
                    "(vagolytic AV acceleration), torsades de pointes. Transvenous "
                    "electrical cardioversion (TVEC) is the referral alternative."
                ),
                "notes_ja": (
                    "罹患期間3ヶ月未満・重大な器質的心疾患のないAFで成功率が最も高い。"
                    "毒性: 疝痛、下痢、持続勃起（包皮脱出）、蕁麻疹、鼻粘膜浮腫、低血圧、"
                    "運動失調、迷走神経遮断によるAV伝導促進で頻脈性上室性頻拍、"
                    "torsades de pointes。経静脈電気的除細動（TVEC）が紹介施設での代替法。"
                ),
            },
            "dog": {
                "safe": True,
                "dosage": (
                    "6-16 mg/kg PO q6-8h (rarely used — largely superseded by other "
                    "antiarrhythmics; consider only where alternatives unavailable)."
                ),
                "dosage_ja": (
                    "6-16 mg/kg 経口 6-8時間毎（使用は稀 — 他の抗不整脈薬にほぼ置き換えられており、"
                    "代替薬がない場合のみ考慮）。"
                ),
                "notes": "GI upset common; monitor ECG for QRS/QT prolongation.",
                "notes_ja": "消化器症状が多い。QRS/QT延長を心電図で監視。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not recommended",
                "dosage_ja": "推奨されない",
                "notes": "Safer alternatives exist for feline arrhythmias; quinidine not used clinically in cats.",
                "notes_ja": "猫の不整脈にはより安全な代替薬があり、キニジンは臨床使用されない。",
            },
        },
        "side_effects": (
            "Horses: colic, diarrhoea, paraphimosis, urticaria/wheals, nasal mucosal "
            "swelling (upper airway obstruction risk), hypotension, ataxia, "
            "supraventricular tachycardia, QRS/QT prolongation, torsades de pointes, "
            "sudden death (rare). Dogs: vomiting, diarrhoea, weakness, hypotension."
        ),
        "side_effects_ja": (
            "馬: 疝痛、下痢、持続勃起・包皮脱出、蕁麻疹/膨疹、鼻粘膜腫脹（上気道閉塞リスク）、"
            "低血圧、運動失調、上室性頻拍、QRS/QT延長、torsades de pointes、突然死（稀）。"
            "犬: 嘔吐、下痢、脱力、低血圧。"
        ),
        "contraindications": (
            "Complete AV block, congestive heart failure, significant structural "
            "heart disease (equine AF with CHF should be rate-controlled, not "
            "converted), digoxin toxicity, myasthenia gravis."
        ),
        "contraindications_ja": (
            "完全房室ブロック、うっ血性心不全、重大な器質的心疾患"
            "（CHFを伴う馬のAFは洞調律復帰でなく心拍数コントロールの適応）、"
            "ジゴキシン中毒、重症筋無力症。"
        ),
        "drug_interactions": [
            {
                "drug": "digoxin",
                "effect": "Quinidine displaces digoxin from tissue binding and reduces its clearance — plasma digoxin roughly doubles; halve digoxin dose and monitor levels",
                "effect_ja": "キニジンはジゴキシンを組織結合から遊離させクリアランスを低下 — 血中ジゴキシン濃度が約2倍化。ジゴキシンを半量に減量し血中濃度を監視",
            },
            {
                "drug": "Potassium-altering drugs",
                "effect": "Hypokalemia potentiates torsades de pointes on quinidine; correct potassium before and during treatment",
                "effect_ja": "低カリウム血症はキニジンによるtorsades de pointesを増強。治療前・治療中はカリウムを補正",
            },
            {
                "drug": "cimetidine",
                "effect": "Inhibits hepatic quinidine metabolism — increased plasma levels and toxicity risk",
                "effect_ja": "肝でのキニジン代謝を阻害 — 血中濃度上昇・毒性リスク増加",
            },
        ],
    },
    {
        "id": "valacyclovir",
        "name": "Valacyclovir",
        "name_ja": "バラシクロビル",
        "category": "antivirals",
        "mechanism": (
            "L-valyl ester prodrug of acyclovir with much higher oral bioavailability "
            "(~ 3-4× in horses). Converted to acyclovir, which is phosphorylated by "
            "viral thymidine kinase and inhibits herpesviral DNA polymerase. Used in "
            "horses for EHV-1, including reduction of viremia in equine herpesvirus "
            "myeloencephalopathy (EHM) outbreaks."
        ),
        "mechanism_ja": (
            "アシクロビルのL-バリルエステル型プロドラッグで、経口バイオアベイラビリティが"
            "大幅に高い（馬で約3-4倍）。体内でアシクロビルに変換され、ウイルスの"
            "チミジンキナーゼによりリン酸化されてヘルペスウイルスDNAポリメラーゼを阻害。"
            "馬のEHV-1感染（馬ヘルペスウイルス脊髄脳症/EHMアウトブレイク時のウイルス血症"
            "低減を含む）に使用される。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": (
                    "EHV-1/EHM: loading 27 mg/kg PO q8h × 2 days, then 18 mg/kg PO "
                    "q12h × 7-14 days (Maxwell 2017 pharmacokinetic regimen). Start "
                    "as early as possible — greatest benefit before neurologic signs."
                ),
                "dosage_ja": (
                    "EHV-1/EHM: 負荷投与 27 mg/kg 経口 8時間毎 2日間、以後 18 mg/kg 経口 "
                    "12時間毎 7-14日間（Maxwell 2017の薬物動態ベースレジメン）。"
                    "可能な限り早期に開始 — 神経症状発現前の投与が最も有効。"
                ),
                "notes": (
                    "Ensure hydration (acyclovir crystalluria at high doses). Expensive "
                    "in adult horses; weigh cost-benefit in outbreak prophylaxis."
                ),
                "notes_ja": (
                    "水和の維持（高用量でアシクロビル結晶尿のリスク）。成馬では高コストのため、"
                    "アウトブレイク予防投与では費用対効果を検討。"
                ),
            },
            "cat": {
                "safe": False,
                "dosage": "NEVER use in cats — fatal",
                "dosage_ja": "猫には絶対に使用しない — 致死的",
                "notes": (
                    "FATAL in cats: causes fulminant hepatic and renal tubular necrosis "
                    "and bone marrow suppression at herpes-therapeutic doses (Nasisse "
                    "1997). Famciclovir is the safe and effective anti-FHV-1 drug in cats."
                ),
                "notes_ja": (
                    "猫では致死的: ヘルペス治療用量で劇症肝壊死・腎尿細管壊死・骨髄抑制を"
                    "引き起こす（Nasisse 1997）。猫のFHV-1にはファムシクロビルが安全かつ有効。"
                ),
            },
            "dog": {
                "safe": False,
                "dosage": "Not used",
                "dosage_ja": "使用しない",
                "notes": "No established indication; canine herpesvirus disease is managed supportively.",
                "notes_ja": "確立された適応なし。犬ヘルペスウイルス感染症は支持療法で管理。",
            },
        },
        "side_effects": (
            "Horses: soft feces, mild colic (uncommon), crystalluria with dehydration. "
            "Cats: DO NOT USE — hepatic/renal necrosis and marrow suppression, fatal."
        ),
        "side_effects_ja": (
            "馬: 軟便、軽度疝痛（稀）、脱水時の結晶尿。猫: 使用禁止 — 肝壊死・腎壊死・骨髄抑制により致死的。"
        ),
        "contraindications": (
            "Cats (absolute contraindication — fatal). Significant renal impairment "
            "without dose adjustment; maintain hydration."
        ),
        "contraindications_ja": ("猫（絶対禁忌 — 致死的）。用量調整なしの高度腎機能低下。水和を維持すること。"),
        "drug_interactions": [
            {
                "drug": "Nephrotoxic drugs",
                "effect": "Additive renal risk (acyclovir crystalluria) — avoid concurrent aminoglycosides/NSAIDs in dehydrated horses",
                "effect_ja": "腎リスクが相加的（アシクロビル結晶尿）— 脱水馬でのアミノグリコシドやNSAIDsとの併用を回避",
            },
            {
                "drug": "Probenecid",
                "effect": "Reduces renal tubular secretion of acyclovir — increased plasma levels",
                "effect_ja": "アシクロビルの腎尿細管分泌を抑制 — 血中濃度上昇",
            },
        ],
    },
    {
        "id": "meclizine",
        "name": "Meclizine",
        "name_ja": "メクリジン",
        "category": "antihistamines",
        "mechanism": (
            "First-generation H1 antihistamine with central antiemetic and "
            "anti-motion-sickness action on the vestibular apparatus and "
            "chemoreceptor trigger zone. Used for symptomatic relief of nausea in "
            "vestibular disease and motion sickness."
        ),
        "mechanism_ja": (
            "第一世代H1抗ヒスタミン薬。前庭器と化学受容器引金帯（CTZ）に作用する中枢性の"
            "制吐・抗動揺病作用をもつ。前庭疾患や乗り物酔いに伴う悪心の対症療法に使用。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "25 mg/dog PO q24h (12.5 mg for small dogs; ~ 4 mg/kg) for "
                    "vestibular-disease nausea or motion sickness."
                ),
                "dosage_ja": ("25 mg/頭 経口 1日1回（小型犬は12.5 mg。約4 mg/kg）。前庭疾患の悪心・乗り物酔いに。"),
                "notes": "Give 30-60 min before travel for motion sickness. Sedation is the main side effect.",
                "notes_ja": "乗り物酔いには乗車30-60分前に投与。主な副作用は鎮静。",
            },
            "cat": {
                "safe": True,
                "dosage": "12.5 mg/cat PO q24h.",
                "dosage_ja": "12.5 mg/頭 経口 1日1回。",
                "notes": "Maropitant is often preferred for vestibular nausea in cats; meclizine is an OTC alternative.",
                "notes_ja": "猫の前庭性悪心にはマロピタントが選ばれることが多い。メクリジンはOTCの代替選択肢。",
            },
            "rabbit": {
                "safe": True,
                "dosage": (
                    "2-12 mg/kg PO q24h as supportive care for head tilt "
                    "(E. cuniculi/otitis vestibular disease; Carpenter 6th ed)."
                ),
                "dosage_ja": (
                    "2-12 mg/kg 経口 1日1回。斜頸（E. cuniculi・中耳炎による前庭疾患）の"
                    "支持療法として（Carpenter第6版）。"
                ),
                "notes": "Adjunct only — treat the underlying cause (fenbendazole ± antibiotics).",
                "notes_ja": "あくまで補助 — 基礎疾患の治療（フェンベンダゾール±抗菌薬）を併行。",
            },
            "ferret": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q24h (Carpenter 6th ed).",
                "dosage_ja": "1-2 mg/kg 経口 1日1回（Carpenter第6版）。",
                "notes": "Sedation possible.",
                "notes_ja": "鎮静が起こりうる。",
            },
        },
        "side_effects": (
            "Sedation (most common), dry mouth/eyes and urinary retention "
            "(anticholinergic), paradoxical excitement (rare)."
        ),
        "side_effects_ja": ("鎮静（最多）、口腔・眼の乾燥や尿貯留（抗コリン作用）、逆説的興奮（稀）。"),
        "contraindications": (
            "Glaucoma, urinary obstruction/prostatic disease, severe cardiac disease "
            "(anticholinergic effects); use cautiously with other CNS depressants."
        ),
        "contraindications_ja": (
            "緑内障、尿路閉塞・前立腺疾患、重度心疾患（抗コリン作用のため）。他の中枢抑制薬との併用は慎重に。"
        ),
        "drug_interactions": [
            {
                "drug": "Other CNS depressants",
                "effect": "Additive sedation",
                "effect_ja": "鎮静作用が相加的",
            },
            {
                "drug": "Anticholinergics",
                "effect": "Additive antimuscarinic effects (ileus, urinary retention)",
                "effect_ja": "抗ムスカリン作用が相加的（イレウス・尿貯留）",
            },
        ],
    },
    {
        "id": "colchicine",
        "name": "Colchicine",
        "name_ja": "コルヒチン",
        "category": "miscellaneous",
        "mechanism": (
            "Binds tubulin and blocks microtubule polymerisation — inhibits "
            "neutrophil migration and degranulation (anti-inflammatory in gout and "
            "familial-fever syndromes) and reduces amyloid A deposition and hepatic "
            "collagen formation. Veterinary uses: Shar-Pei autoinflammatory disease "
            "and renal amyloidosis, hepatic fibrosis, avian/reptile articular gout "
            "adjunct."
        ),
        "mechanism_ja": (
            "チューブリンに結合し微小管重合を阻害 — 好中球の遊走・脱顆粒を抑制"
            "（痛風や家族性発熱症候群での抗炎症作用）し、アミロイドA沈着と肝コラーゲン形成を"
            "低減する。獣医学的用途: シャーペイ自己炎症性疾患・腎アミロイドーシス、肝線維症、"
            "鳥・爬虫類の関節痛風の補助治療。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Shar-Pei fever / renal amyloidosis prophylaxis: 0.01-0.03 mg/kg "
                    "PO q24h. Hepatic fibrosis: 0.03 mg/kg PO q24h."
                ),
                "dosage_ja": (
                    "シャーペイ熱/腎アミロイドーシス予防: 0.01-0.03 mg/kg 経口 1日1回。"
                    "肝線維症: 0.03 mg/kg 経口 1日1回。"
                ),
                "notes": (
                    "Narrow therapeutic margin — GI upset (vomiting/diarrhoea) is "
                    "dose-limiting; reduce dose or give with food. Monitor CBC on "
                    "long-term use (rare marrow suppression)."
                ),
                "notes_ja": (
                    "治療域が狭い — 消化器症状（嘔吐/下痢）が用量制限。減量または食事と共に投与。"
                    "長期投与ではCBC監視（稀に骨髄抑制）。"
                ),
            },
            "cat": {
                "safe": False,
                "dosage": "Generally avoided (limited safety data)",
                "dosage_ja": "原則回避（安全性データが乏しい）",
                "notes": "Little clinical evidence in cats; GI toxicity concern.",
                "notes_ja": "猫での臨床エビデンスは乏しく、消化器毒性が懸念される。",
            },
            "bird": {
                "safe": True,
                "dosage": (
                    "Articular gout adjunct: 0.04 mg/kg PO q12-24h (Carpenter 6th "
                    "ed) with dietary purine/protein reduction and hydration."
                ),
                "dosage_ja": (
                    "関節痛風の補助: 0.04 mg/kg 経口 12-24時間毎（Carpenter第6版）。"
                    "低プリン/低蛋白食への変更と水和管理を併行。"
                ),
                "notes": "Allopurinol and hydration remain the mainstay; monitor uric acid.",
                "notes_ja": "アロプリノールと水和管理が治療の中心。尿酸値を監視。",
            },
            "reptile": {
                "safe": True,
                "dosage": "Gout adjunct: 0.04 mg/kg PO q24-72h with aggressive hydration and husbandry correction.",
                "dosage_ja": "痛風の補助: 0.04 mg/kg 経口 24-72時間毎。積極的な水和と飼育環境是正を併行。",
                "notes": "Correct chronic dehydration and dietary protein excess — the underlying causes.",
                "notes_ja": "基礎原因である慢性脱水と食餌性蛋白過剰を是正すること。",
            },
        },
        "side_effects": (
            "Vomiting, diarrhoea, abdominal discomfort (dose-limiting), bone marrow "
            "suppression (rare, chronic use), myopathy/neuropathy (rare)."
        ),
        "side_effects_ja": (
            "嘔吐、下痢、腹部不快感（用量制限毒性）、骨髄抑制（稀・慢性投与時）、ミオパチー/ニューロパチー（稀）。"
        ),
        "contraindications": (
            "Severe renal or hepatic failure (reduced clearance — accumulation), "
            "pre-existing marrow suppression, pregnancy."
        ),
        "contraindications_ja": ("重度の腎不全・肝不全（クリアランス低下による蓄積）、既存の骨髄抑制、妊娠。"),
        "drug_interactions": [
            {
                "drug": "Macrolides / azole antifungals",
                "effect": "CYP3A4/P-glycoprotein inhibition raises colchicine levels — potentially severe toxicity; avoid or reduce dose",
                "effect_ja": "CYP3A4/P糖蛋白阻害によりコルヒチン濃度上昇 — 重度毒性のおそれ。併用回避または減量",
            },
            {
                "drug": "cyclosporine",
                "effect": "P-glycoprotein competition increases colchicine exposure and myotoxicity risk",
                "effect_ja": "P糖蛋白の競合によりコルヒチン曝露とミオパチーリスクが増加",
            },
        ],
    },
    {
        "id": "leuprolide",
        "name": "Leuprolide Acetate (Lupron Depot)",
        "name_ja": "リュープロレリン酢酸塩（リュープロリド/ルプロンデポ）",
        "category": "reproductive_hormones",
        "mechanism": (
            "Long-acting GnRH agonist. Continuous receptor stimulation "
            "down-regulates pituitary GnRH receptors, suppressing LH/FSH and "
            "gonadal/adrenal sex-steroid output after an initial flare. Mainstays: "
            "avian chronic egg laying and reproductive disease; ferret "
            "adrenocortical disease (suppresses LH-driven adrenal sex-hormone "
            "secretion)."
        ),
        "mechanism_ja": (
            "持続性GnRHアゴニスト。持続的な受容体刺激により下垂体GnRH受容体が"
            "ダウンレギュレーションされ、初期フレアの後にLH/FSHと性腺・副腎性ステロイド分泌を"
            "抑制する。主用途: 鳥の慢性産卵・生殖器疾患、フェレット副腎疾患"
            "（LH駆動性の副腎性ホルモン分泌を抑制）。"
        ),
        "species_info": {
            "bird": {
                "safe": True,
                "dosage": (
                    "Chronic egg laying / reproductive disease: 700-800 μg/kg IM "
                    "(depot formulation) q2-3 weeks until behavioural/reproductive "
                    "quiescence (Carpenter 6th ed; small birds may need the higher "
                    "end)."
                ),
                "dosage_ja": (
                    "慢性産卵/生殖器疾患: 700-800 μg/kg 筋注（デポ製剤）2-3週毎、"
                    "産卵・発情行動が沈静化するまで（Carpenter第6版。小型鳥は高用量側）。"
                ),
                "notes": (
                    "Combine with husbandry change (light cycle ≤ 10-12 h, remove "
                    "nest sites/mirrors, diet correction). Deslorelin implant is the "
                    "longer-acting alternative."
                ),
                "notes_ja": (
                    "飼育環境の是正（明期10-12時間以下、巣材・鏡の除去、食餌是正）を必ず併行。"
                    "より長期作用のデスロレリンインプラントが代替。"
                ),
            },
            "ferret": {
                "safe": True,
                "dosage": (
                    "Adrenocortical disease: 100-250 μg/kg IM (30-day depot) q4 "
                    "weeks; signs (pruritus, alopecia, vulvar swelling) typically "
                    "improve within 2-4 weeks (Wagner 2005)."
                ),
                "dosage_ja": (
                    "副腎疾患: 100-250 μg/kg 筋注（30日デポ製剤）4週毎。"
                    "臨床徴候（掻痒・脱毛・外陰部腫大）は通常2-4週間で改善（Wagner 2005）。"
                ),
                "notes": (
                    "Palliative — does not shrink adrenal tumours; adrenalectomy is "
                    "curative for unilateral disease. Deslorelin implant is the "
                    "longer-acting alternative."
                ),
                "notes_ja": (
                    "対症的 — 副腎腫瘍自体は縮小しない。片側性なら副腎摘出が根治的。"
                    "デスロレリンインプラントがより長期作用の代替。"
                ),
            },
            "reptile": {
                "safe": True,
                "dosage": (
                    "Follicular stasis adjunct (lizards): 400-800 μg/kg IM q2-4 "
                    "weeks — efficacy evidence limited; husbandry correction and "
                    "surgery remain primary."
                ),
                "dosage_ja": (
                    "卵胞停滞の補助（トカゲ類）: 400-800 μg/kg 筋注 2-4週毎 — "
                    "有効性のエビデンスは限定的。飼育環境是正と外科が主体。"
                ),
                "notes": "Response variable across reptile taxa.",
                "notes_ja": "爬虫類の分類群により反応は不定。",
            },
        },
        "side_effects": (
            "Transient flare of reproductive behaviour after first dose, "
            "injection-site soreness, lethargy (transient). Rare hypersensitivity."
        ),
        "side_effects_ja": ("初回投与後の一過性の発情/生殖行動フレア、注射部位痛、一過性の元気消失。稀に過敏症。"),
        "contraindications": (
            "Pregnancy (induces luteolysis/abortion risk). Not a substitute for "
            "surgery in egg-yolk coelomitis or adrenal carcinoma with invasion."
        ),
        "contraindications_ja": (
            "妊娠（黄体退行・流産リスク）。卵黄性腹膜炎や浸潤性副腎癌に対する外科の代替にはならない。"
        ),
        "drug_interactions": [
            {
                "drug": "deslorelin",
                "effect": "Same class (GnRH agonist) — do not stack; choose one agent",
                "effect_ja": "同一クラス（GnRHアゴニスト）— 重複投与しない。どちらか一方を選択",
            },
        ],
    },
    {
        "id": "niacinamide",
        "name": "Niacinamide (Nicotinamide)",
        "name_ja": "ナイアシンアミド（ニコチン酸アミド）",
        "category": "dermatological",
        "mechanism": (
            "Amide form of vitamin B3 with immunomodulatory action: inhibits "
            "antigen-IgE-induced histamine release and phosphodiesterase, and "
            "protects against photodamage. Combined with tetracycline or "
            "doxycycline as a steroid-sparing regimen for canine immune-mediated "
            "skin diseases (discoid lupus erythematosus, pemphigus foliaceus "
            "adjunct, symmetric lupoid onychodystrophy, cutaneous vasculitis; "
            "White 1992)."
        ),
        "mechanism_ja": (
            "ビタミンB3のアミド型で免疫調整作用をもつ: 抗原-IgE誘発性ヒスタミン遊離と"
            "ホスホジエステラーゼを阻害し、光障害から保護する。テトラサイクリンまたは"
            "ドキシサイクリンとの併用で、犬の免疫介在性皮膚疾患（円板状エリテマトーデス、"
            "落葉状天疱瘡の補助、対称性狼瘡様爪異栄養症、皮膚血管炎）のステロイド節約"
            "レジメンとして用いる（White 1992）。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Dogs > 10 kg: 500 mg PO q8h; dogs ≤ 10 kg: 250 mg PO q8h — "
                    "always combined with tetracycline (same mg dose) or doxycycline "
                    "5 mg/kg q12h. Expect 1-2 months for full effect; taper to q12h "
                    "after remission."
                ),
                "dosage_ja": (
                    "体重10 kg超: 500 mg 経口 8時間毎。10 kg以下: 250 mg 経口 8時間毎 — "
                    "常にテトラサイクリン（同mg量）またはドキシサイクリン5 mg/kg 12時間毎と併用。"
                    "効果発現まで1-2ヶ月。寛解後は12時間毎に漸減。"
                ),
                "notes": (
                    "Steroid-sparing option for mild-to-moderate disease or as "
                    "maintenance after prednisolone induction. Add sunscreen/UV "
                    "avoidance for nasal DLE."
                ),
                "notes_ja": (
                    "軽度〜中等度病変のステロイド節約選択肢、またはプレドニゾロン導入後の維持療法。"
                    "鼻鏡DLEでは遮光・UV回避を併行。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": "Rarely used; 250 mg/cat PO q8-12h reported anecdotally with doxycycline.",
                "dosage_ja": "使用は稀。ドキシサイクリン併用で250 mg/頭 経口 8-12時間毎の報告（逸話的）。",
                "notes": "Evidence in cats is weak; consider other immunomodulators first.",
                "notes_ja": "猫でのエビデンスは弱い。他の免疫調整薬を優先的に検討。",
            },
        },
        "side_effects": (
            "Vomiting, anorexia, lethargy; rarely increased liver enzymes or "
            "(with the tetracycline partner) seizures reported in small dogs."
        ),
        "side_effects_ja": (
            "嘔吐、食欲不振、元気消失。稀に肝酵素上昇、（併用するテトラサイクリン側の影響で）小型犬での痙攣の報告。"
        ),
        "contraindications": (
            "Hepatic disease (monitor enzymes), known hypersensitivity. Do not "
            "substitute niacin (nicotinic acid) — flushing/hepatotoxicity risk."
        ),
        "contraindications_ja": (
            "肝疾患（肝酵素監視）、過敏症の既往。ナイアシン（ニコチン酸）で代用しないこと — "
            "紅潮・肝毒性のリスクがある。"
        ),
        "drug_interactions": [
            {
                "drug": "tetracycline",
                "effect": "Intentional therapeutic combination for immune-mediated dermatoses (White 1992)",
                "effect_ja": "免疫介在性皮膚疾患に対する意図的な治療的併用（White 1992）",
            },
            {
                "drug": "doxycycline",
                "effect": "Preferred modern partner drug (dosed 5 mg/kg q12h) in the same combination regimen",
                "effect_ja": "同レジメンで現在好まれる併用薬（5 mg/kg 12時間毎）",
            },
            {
                "drug": "Anticonvulsants",
                "effect": "High-dose nicotinamide may potentiate sedation with phenobarbital",
                "effect_ja": "高用量ニコチン酸アミドはフェノバルビタールの鎮静を増強しうる",
            },
        ],
    },
    {
        "id": "dexrazoxane",
        "name": "Dexrazoxane (Zinecard)",
        "name_ja": "デクスラゾキサン（ジネカード）",
        "category": "antineoplastics",
        "mechanism": (
            "EDTA-analogue iron chelator and topoisomerase II inhibitor. Chelates "
            "intracellular iron, preventing anthracycline-iron free-radical "
            "formation — the antidote of choice for doxorubicin extravasation and "
            "a cardioprotectant against cumulative doxorubicin cardiotoxicity."
        ),
        "mechanism_ja": (
            "EDTA類縁の鉄キレート薬かつトポイソメラーゼII阻害薬。細胞内鉄をキレートし、"
            "アントラサイクリン-鉄フリーラジカル形成を防ぐ — ドキソルビシン血管外漏出の"
            "第一選択の解毒薬であり、累積投与による心毒性に対する心保護薬。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Doxorubicin extravasation: 10× the extravasated doxorubicin dose "
                    "IV (in a DIFFERENT limb) within 6 h, repeated at 24 h and 48 h "
                    "(3 doses total; Venable 2012). Cardioprotection: 10:1 "
                    "dexrazoxane:doxorubicin IV immediately before doxorubicin in "
                    "high-cumulative-dose patients."
                ),
                "dosage_ja": (
                    "ドキソルビシン血管外漏出: 漏出したドキソルビシン量の10倍量を6時間以内に"
                    "静注（漏出肢と別の肢から）、24時間後・48時間後にも反復（計3回。Venable 2012）。"
                    "心保護: 累積高用量患者でドキソルビシン直前にデクスラゾキサン:ドキソルビシン"
                    "＝10:1で静注。"
                ),
                "notes": (
                    "Extravasation of doxorubicin causes progressive tissue necrosis "
                    "over weeks — early dexrazoxane markedly reduces surgical "
                    "debridement need. Do NOT apply DMSO concurrently with "
                    "dexrazoxane (reduces efficacy). Cold-compress the site."
                ),
                "notes_ja": (
                    "ドキソルビシン漏出は数週間かけて進行性の組織壊死を起こす — 早期の"
                    "デクスラゾキサン投与で外科的デブリードマンの必要性が大幅に減少。"
                    "DMSOの同時局所塗布はデクスラゾキサンの効果を減弱するため行わない。"
                    "患部は冷罨法。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": "Same protocol as dogs (10× extravasated dose IV, repeat 24/48 h) — limited feline reports.",
                "dosage_ja": "犬と同プロトコル（漏出量の10倍を静注、24/48時間後に反復）— 猫での報告は限られる。",
                "notes": "Feline doxorubicin doses are lower (1 mg/kg); scale accordingly.",
                "notes_ja": "猫のドキソルビシン用量は低い（1 mg/kg）ため相応にスケーリング。",
            },
        },
        "side_effects": ("Myelosuppression (additive with chemotherapy — monitor CBC), vomiting, injection-site pain."),
        "side_effects_ja": ("骨髄抑制（化学療法と相加的 — CBC監視）、嘔吐、注射部位痛。"),
        "contraindications": (
            "Severe pre-existing myelosuppression. Not for non-anthracycline "
            "vesicant extravasation (e.g. vincristine — different management)."
        ),
        "contraindications_ja": (
            "重度の既存骨髄抑制。アントラサイクリン以外の起壊死性抗癌薬"
            "（ビンクリスチン等 — 対処法が異なる）の漏出には非適応。"
        ),
        "drug_interactions": [
            {
                "drug": "doxorubicin",
                "effect": "Intended pairing: extravasation antidote and cardioprotectant; may modestly add to myelosuppression",
                "effect_ja": "意図された組み合わせ: 血管外漏出の解毒薬・心保護薬。骨髄抑制がやや相加的になりうる",
            },
            {
                "drug": "DMSO (topical)",
                "effect": "Concurrent topical DMSO reduces dexrazoxane efficacy for extravasation — do not combine",
                "effect_ja": "DMSO局所塗布の併用は漏出に対するデクスラゾキサンの効果を減弱 — 併用しない",
            },
        ],
    },
    {
        "id": "methotrexate",
        "name": "Methotrexate",
        "name_ja": "メトトレキサート",
        "category": "immunosuppressives",
        "mechanism": (
            "Folate-antagonist antimetabolite: inhibits dihydrofolate reductase, "
            "blocking thymidylate and purine synthesis in rapidly dividing cells. "
            "Veterinary uses: adjunct in multi-agent lymphoma protocols "
            "(historic LMP maintenance), immune-mediated diseases (refractory "
            "polyarthritis, IBD) at low anti-inflammatory doses."
        ),
        "mechanism_ja": (
            "葉酸拮抗性代謝拮抗薬: ジヒドロ葉酸還元酵素を阻害し、分裂の速い細胞での"
            "チミジル酸・プリン合成を遮断する。獣医学的用途: 多剤併用リンパ腫プロトコルの"
            "補助（旧LMP維持療法）、低用量での免疫介在性疾患（難治性多発性関節炎・IBD）。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Immune-mediated disease: 2.5 mg/m² PO 2-3×/week (or 0.06-0.08 "
                    "mg/kg). Lymphoma maintenance (historic protocols): 2.5-5 mg/m² "
                    "PO q48h. Monitor CBC every 1-2 weeks initially."
                ),
                "dosage_ja": (
                    "免疫介在性疾患: 2.5 mg/m² 経口 週2-3回（または0.06-0.08 mg/kg）。"
                    "リンパ腫維持（旧プロトコル）: 2.5-5 mg/m² 経口 48時間毎。"
                    "開始初期は1-2週毎にCBC監視。"
                ),
                "notes": (
                    "Give folic acid on non-methotrexate days to reduce GI/marrow "
                    "toxicity. Leucovorin (folinic acid) is the overdose rescue."
                ),
                "notes_ja": (
                    "非投与日に葉酸を補給し消化器/骨髄毒性を軽減。過量投与のレスキューはロイコボリン（フォリン酸）。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": "2.5 mg/m² PO 2-3×/week (e.g. chronic progressive polyarthritis) — use with caution and CBC monitoring.",
                "dosage_ja": "2.5 mg/m² 経口 週2-3回（例: 慢性進行性多発性関節炎）— 慎重投与・CBC監視下で。",
                "notes": "Cats are prone to GI upset; dose-escalate slowly.",
                "notes_ja": "猫は消化器症状を起こしやすい。緩徐に増量。",
            },
        },
        "side_effects": (
            "Myelosuppression, GI upset (vomiting, diarrhoea, mucosal ulceration), "
            "hepatotoxicity (chronic), nephrotoxicity at high doses, alopecia (rare)."
        ),
        "side_effects_ja": (
            "骨髄抑制、消化器症状（嘔吐・下痢・粘膜潰瘍）、肝毒性（慢性投与）、高用量での腎毒性、脱毛（稀）。"
        ),
        "contraindications": (
            "Pre-existing marrow suppression, significant hepatic or renal "
            "impairment, pregnancy (teratogenic), concurrent serious infection."
        ),
        "contraindications_ja": ("既存の骨髄抑制、高度の肝・腎機能障害、妊娠（催奇形性）、重篤な感染症の併存。"),
        "drug_interactions": [
            {
                "drug": "NSAIDs",
                "effect": "Reduce renal clearance and displace protein binding — increased methotrexate toxicity; avoid concurrent use",
                "effect_ja": "腎クリアランス低下と蛋白結合置換 — メトトレキサート毒性増加。併用回避",
            },
            {
                "drug": "trimethoprim_sulfa",
                "effect": "Additive folate antagonism — marked marrow-suppression risk; avoid",
                "effect_ja": "葉酸拮抗が相加的 — 顕著な骨髄抑制リスク。併用回避",
            },
            {
                "drug": "Penicillins",
                "effect": "Compete for renal tubular secretion — reduced methotrexate clearance and increased toxicity",
                "effect_ja": "腎尿細管分泌で競合 — メトトレキサートのクリアランス低下・毒性増加",
            },
            {
                "drug": "Proton pump inhibitors",
                "effect": "Reduce renal elimination of methotrexate — increased exposure",
                "effect_ja": "メトトレキサートの腎排泄を低下 — 曝露増加",
            },
        ],
    },
    {
        "id": "thiamine_b1",
        "name": "Thiamine (Vitamin B1)",
        "name_ja": "チアミン（ビタミンB1）",
        "category": "vitamins_minerals",
        "mechanism": (
            "Essential cofactor (as thiamine pyrophosphate) for pyruvate "
            "dehydrogenase and transketolase — critical for neuronal glucose "
            "metabolism. Deficiency (all-fish thiaminase diets in cats and "
            "frozen-fish-fed reptiles/birds, prolonged anorexia, cooked meat "
            "diets) causes reversible encephalopathy if treated early."
        ),
        "mechanism_ja": (
            "ピルビン酸脱水素酵素とトランスケトラーゼの必須補酵素（チアミンピロリン酸として）— "
            "神経細胞のグルコース代謝に不可欠。欠乏（猫の魚中心食・冷凍魚給餌の爬虫類/鳥での"
            "チアミナーゼ、遷延性食欲不振、加熱肉食）は早期治療で可逆的な脳症を起こす。"
        ),
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": (
                    "Deficiency: 25-50 mg/cat IM or SC q24h × 3-5 days, then oral "
                    "supplementation until diet corrected. Classic signs: cervical "
                    "ventroflexion, mydriasis, vestibular ataxia, seizures."
                ),
                "dosage_ja": (
                    "欠乏症: 25-50 mg/頭 筋注または皮下 1日1回 3-5日間、以後は食餌是正まで"
                    "経口補給。典型徴候: 頸部腹側屈曲、散瞳、前庭性運動失調、痙攣。"
                ),
                "notes": "Neurologic signs are reversible if treated within days of onset. Correct the diet (no raw-fish-only feeding).",
                "notes_ja": "神経徴候は発症数日以内の治療で可逆的。食餌を是正（生魚のみの給餌をやめる）。",
            },
            "dog": {
                "safe": True,
                "dosage": "Deficiency: 50-100 mg/dog IM/SC q24h × 3-5 days, then oral.",
                "dosage_ja": "欠乏症: 50-100 mg/頭 筋注/皮下 1日1回 3-5日間、以後経口。",
                "notes": "Also used as adjunct in lead toxicosis and ethylene-glycol metabolic support.",
                "notes_ja": "鉛中毒の補助、エチレングリコール中毒の代謝サポートとしても使用。",
            },
            "horse": {
                "safe": True,
                "dosage": (
                    "Bracken fern / thiaminase toxicosis: 0.5-5 mg/kg slow IV or IM q12-24h until signs resolve."
                ),
                "dosage_ja": (
                    "ワラビ中毒/チアミナーゼ中毒: 0.5-5 mg/kg 緩徐静注または筋注 12-24時間毎、徴候消失まで。"
                ),
                "notes": "Rapid IV bolus can cause transient hypotension — give slowly.",
                "notes_ja": "急速静注は一過性低血圧を起こしうる — 緩徐に投与。",
            },
            "reptile": {
                "safe": True,
                "dosage": (
                    "Deficiency (frozen-fish-fed species): 25-30 mg/kg IM q24h until "
                    "response; prevention: supplement 30 mg thiamine per kg of "
                    "frozen fish fed."
                ),
                "dosage_ja": (
                    "欠乏症（冷凍魚給餌種）: 25-30 mg/kg 筋注 1日1回、反応が出るまで。"
                    "予防: 給餌する冷凍魚1 kgあたりチアミン30 mgを補給。"
                ),
                "notes": "Thaw-and-feed frozen fish destroys thiamine via thiaminase — routine supplementation needed (garter snakes, crocodilians, piscivorous turtles).",
                "notes_ja": "冷凍魚は解凍過程でチアミナーゼによりチアミンが破壊される — 恒常的補給が必要（ガーターヘビ・ワニ類・魚食性カメ）。",
            },
            "bird": {
                "safe": True,
                "dosage": "Deficiency (fish-eating birds, seed-only diets): 1-3 mg/kg IM q24h, then dietary correction.",
                "dosage_ja": "欠乏症（魚食性鳥類・種子偏重食）: 1-3 mg/kg 筋注 1日1回、以後食餌是正。",
                "notes": "Signs: opisthotonos ('stargazing'), leg paralysis — dramatic response to injection supports diagnosis.",
                "notes_ja": "徴候: 後弓反張（スターゲイジング）、脚麻痺 — 注射への劇的な反応が診断を支持。",
            },
        },
        "side_effects": (
            "Very safe (water-soluble). Rare hypersensitivity to rapid IV "
            "injection; transient hypotension with fast IV boluses."
        ),
        "side_effects_ja": ("非常に安全（水溶性）。急速静注への過敏反応は稀。急速静注で一過性低血圧。"),
        "contraindications": "Known hypersensitivity (rare).",
        "contraindications_ja": "過敏症の既往（稀）。",
        "drug_interactions": [
            {
                "drug": "Neuromuscular blockers",
                "effect": "High-dose thiamine may theoretically enhance blockade — clinical significance low",
                "effect_ja": "高用量チアミンは理論上遮断を増強しうる — 臨床的意義は低い",
            },
        ],
    },
    {
        "id": "l_carnitine",
        "name": "L-Carnitine",
        "name_ja": "L-カルニチン",
        "category": "supplements",
        "mechanism": (
            "Quaternary amine that shuttles long-chain fatty acids into "
            "mitochondria for beta-oxidation — essential for myocardial energy "
            "metabolism. Supplemented in carnitine-responsive dilated "
            "cardiomyopathy (notably Boxers, American Cocker Spaniels with "
            "taurine) and as hepatic-support in feline hepatic lipidosis."
        ),
        "mechanism_ja": (
            "長鎖脂肪酸をミトコンドリア内へ輸送しβ酸化に供する第四級アミン — 心筋の"
            "エネルギー代謝に必須。カルニチン反応性拡張型心筋症（特にボクサー、"
            "タウリン併用のアメリカン・コッカー・スパニエル）や猫の肝リピドーシスの"
            "肝サポートとして補給する。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "DCM adjunct: 50-100 mg/kg PO q8-12h (Boxer protocol ~ 1 g PO "
                    "q8h for medium dogs; combine with taurine 500-1000 mg q12h in "
                    "Cocker Spaniels)."
                ),
                "dosage_ja": (
                    "DCM補助: 50-100 mg/kg 経口 8-12時間毎（ボクサーのプロトコルは中型犬で"
                    "約1 g 経口 8時間毎。コッカー・スパニエルではタウリン500-1000 mg "
                    "12時間毎と併用）。"
                ),
                "notes": (
                    "Echo recheck at 3-6 months to document response; only a subset "
                    "of DCM is carnitine-responsive. Screen diet history "
                    "(grain-free/legume-rich diet-associated DCM — diet change is "
                    "primary)."
                ),
                "notes_ja": (
                    "反応評価のため3-6ヶ月後に心エコー再検。カルニチン反応性はDCMの一部のみ。"
                    "食餌歴を確認（グレインフリー/豆類主体食関連DCMでは食餌変更が第一）。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": "Hepatic lipidosis adjunct: 250-500 mg/cat PO q24h alongside enteral nutrition.",
                "dosage_ja": "肝リピドーシス補助: 250-500 mg/頭 経口 1日1回。経腸栄養と併行。",
                "notes": "Nutrition (esophagostomy-tube feeding) is the primary therapy; carnitine supports fatty-acid oxidation.",
                "notes_ja": "主治療は栄養（食道瘻チューブ給餌）。カルニチンは脂肪酸酸化を支援する補助。",
            },
        },
        "side_effects": ("Very safe; GI upset (diarrhoea, nausea) and fishy body odor at high doses."),
        "side_effects_ja": ("非常に安全。高用量で消化器症状（下痢・悪心）や魚様体臭。"),
        "contraindications": "None significant at clinical doses.",
        "contraindications_ja": "臨床用量で重大なものはなし。",
        "drug_interactions": [
            {
                "drug": "No significant drug interactions",
                "effect": "Nutraceutical with wide safety margin",
                "effect_ja": "安全域の広い栄養補助剤",
            },
        ],
    },
    {
        "id": "paromomycin",
        "name": "Paromomycin",
        "name_ja": "パロモマイシン",
        "category": "antiparasitics",
        "mechanism": (
            "Non-absorbed oral aminoglycoside with luminal activity against "
            "Cryptosporidium, Giardia, Entamoeba and Leishmania. Because it is "
            "normally not absorbed, systemic aminoglycoside toxicity is rare — "
            "EXCEPT when intestinal mucosa is compromised (see feline warning)."
        ),
        "mechanism_ja": (
            "腸管から吸収されない経口アミノグリコシドで、Cryptosporidium・Giardia・"
            "Entamoeba・Leishmaniaに管腔内活性を示す。通常は吸収されないため全身性"
            "アミノグリコシド毒性は稀 — ただし腸粘膜が障害されている場合は例外"
            "（猫の警告参照）。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Cryptosporidiosis/giardiasis (refractory): 150 mg/kg PO q24h × 5 days.",
                "dosage_ja": "クリプトスポリジウム症/ジアルジア症（難治例）: 150 mg/kg 経口 1日1回 5日間。",
                "notes": "Ensure hydration; avoid in animals with severe hemorrhagic diarrhoea (absorption risk).",
                "notes_ja": "水和を維持。重度の出血性下痢では吸収リスクがあるため回避。",
            },
            "cat": {
                "safe": False,
                "dosage": "Use with extreme caution — 125-165 mg/kg PO q12h × 5 days ONLY if benefits outweigh risks",
                "dosage_ja": "使用は極めて慎重に — 利益がリスクを上回る場合のみ 125-165 mg/kg 経口 12時間毎 5日間",
                "notes": (
                    "Acute renal failure, deafness and cataracts reported in cats "
                    "treated for cryptosporidiosis — the damaged intestinal mucosa "
                    "absorbs the aminoglycoside systemically (Gookin 1999). "
                    "Consider azithromycin or tylosin first."
                ),
                "notes_ja": (
                    "クリプトスポリジウム症の猫で急性腎不全・難聴・白内障の報告 — 障害された"
                    "腸粘膜からアミノグリコシドが全身吸収されるため（Gookin 1999）。"
                    "アジスロマイシンやタイロシンを先に検討。"
                ),
            },
            "reptile": {
                "safe": True,
                "dosage": (
                    "Cryptosporidium serpentis (snakes): 300-800 mg/kg PO q48h "
                    "long-term (suppressive, not curative; Carpenter 6th ed)."
                ),
                "dosage_ja": (
                    "Cryptosporidium serpentis（ヘビ）: 300-800 mg/kg 経口 48時間毎 長期"
                    "（抑制的であり根治的でない。Carpenter第6版）。"
                ),
                "notes": "Snake cryptosporidiosis is rarely eliminated — combine with strict hygiene/quarantine.",
                "notes_ja": "ヘビのクリプトスポリジウム症の排除は困難 — 厳格な衛生・検疫と併行。",
            },
            "bird": {
                "safe": True,
                "dosage": "Cryptosporidiosis: 100 mg/kg PO q12h × 7 days.",
                "dosage_ja": "クリプトスポリジウム症: 100 mg/kg 経口 12時間毎 7日間。",
                "notes": "Supportive care and hygiene are essential adjuncts.",
                "notes_ja": "支持療法と衛生管理が必須の補助。",
            },
        },
        "side_effects": (
            "Diarrhoea, soft stool (luminal dysbiosis). If systemically absorbed "
            "through damaged mucosa: nephrotoxicity, ototoxicity (deafness), "
            "cataracts (cats)."
        ),
        "side_effects_ja": (
            "下痢・軟便（管腔内ディスバイオシス）。障害粘膜から全身吸収された場合: "
            "腎毒性、聴器毒性（難聴）、白内障（猫）。"
        ),
        "contraindications": (
            "Intestinal obstruction; severe ulcerative/hemorrhagic enteritis "
            "(systemic absorption); pre-existing renal disease (especially cats)."
        ),
        "contraindications_ja": ("腸閉塞、重度の潰瘍性/出血性腸炎（全身吸収のリスク）、既存の腎疾患（特に猫）。"),
        "drug_interactions": [
            {
                "drug": "Other aminoglycosides",
                "effect": "Additive nephro/ototoxicity if systemic absorption occurs — do not combine",
                "effect_ja": "全身吸収が起これば腎毒性・聴器毒性が相加的 — 併用しない",
            },
            {
                "drug": "furosemide",
                "effect": "Loop diuretics potentiate aminoglycoside ototoxicity",
                "effect_ja": "ループ利尿薬はアミノグリコシドの聴器毒性を増強",
            },
        ],
    },
    {
        "id": "emla_cream",
        "name": "EMLA Cream (Lidocaine 2.5% / Prilocaine 2.5%)",
        "name_ja": "EMLAクリーム（リドカイン2.5%/プリロカイン2.5%）",
        "category": "anesthetics",
        "mechanism": (
            "Eutectic mixture of local anesthetics — lidocaine and prilocaine "
            "penetrate intact skin and block dermal nociceptor sodium channels. "
            "Standard for painless venous catheter placement in rabbits, guinea "
            "pigs and other small exotics (Flecknell), and for needle-phobic "
            "dogs/cats."
        ),
        "mechanism_ja": (
            "局所麻酔薬の共融混合物 — リドカインとプリロカインが健常皮膚に浸透し、"
            "真皮の侵害受容器ナトリウムチャネルを遮断する。ウサギ・モルモット等の"
            "小型エキゾチックの無痛的静脈カテーテル留置の標準（Flecknell）で、"
            "犬猫の穿刺嫌悪例にも使用。"
        ),
        "species_info": {
            "rabbit": {
                "safe": True,
                "dosage": (
                    "Apply a thin layer to clipped skin over the vein (marginal ear "
                    "vein, cephalic), cover with occlusive dressing, wait 30-60 min "
                    "before venipuncture/catheter placement."
                ),
                "dosage_ja": (
                    "静脈上（耳介辺縁静脈・橈側皮静脈）の剃毛部に薄く塗布し、密封被覆材で覆い、"
                    "穿刺/カテーテル留置の30-60分前から作用させる。"
                ),
                "notes": "Prevent ingestion (Elizabethan collar or wipe residue before recovery). Small areas only.",
                "notes_ja": "舐取を防止（エリザベスカラーまたは覚醒前に残薬を拭き取り）。塗布は小範囲のみ。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "As for rabbits: thin layer + occlusion, 30-60 min contact time before catheter placement.",
                "dosage_ja": "ウサギと同様: 薄く塗布＋密封、カテーテル留置の30-60分前から接触。",
                "notes": "Useful before saphenous/cephalic catheterisation in anesthesia protocols.",
                "notes_ja": "麻酔プロトコルでの伏在/橈側皮静脈カテーテル留置前に有用。",
            },
            "dog": {
                "safe": True,
                "dosage": "Thin layer on clipped skin, occlude 30-60 min; small areas only.",
                "dosage_ja": "剃毛部に薄く塗布し30-60分密封。小範囲のみ。",
                "notes": "Wipe off completely before puncture; avoid broken skin.",
                "notes_ja": "穿刺前に完全に拭き取り。損傷皮膚には使用しない。",
            },
            "cat": {
                "safe": True,
                "dosage": ("Small areas only (≤ 1-2 cm²), occlude 30-60 min, wipe off thoroughly and prevent licking."),
                "dosage_ja": ("ごく小範囲のみ（1-2 cm²以下）、30-60分密封し、徹底的に拭き取り、舐取を防止する。"),
                "notes": (
                    "Cats are susceptible to prilocaine-induced methemoglobinemia — "
                    "restrict area/contact time strictly and never apply to broken "
                    "skin or mucosa."
                ),
                "notes_ja": (
                    "猫はプリロカインによるメトヘモグロビン血症に感受性 — 塗布範囲・接触時間を"
                    "厳格に制限し、損傷皮膚・粘膜には絶対に塗布しない。"
                ),
            },
        },
        "side_effects": (
            "Local blanching/erythema (transient), methemoglobinemia (prilocaine — "
            "cats and small patients with large application areas), systemic local "
            "anesthetic toxicity if ingested."
        ),
        "side_effects_ja": (
            "局所の蒼白/紅斑（一過性）、メトヘモグロビン血症（プリロカインによる — "
            "猫や広範囲塗布の小型患者）、舐取時の局所麻酔薬全身毒性。"
        ),
        "contraindications": (
            "Broken skin or mucosal application, methemoglobinemia risk states "
            "(concurrent oxidant drugs), very small patients with large "
            "application areas."
        ),
        "contraindications_ja": (
            "損傷皮膚・粘膜への塗布、メトヘモグロビン血症リスク状態（酸化剤併用）、"
            "体格に対し広範囲の塗布となる超小型患者。"
        ),
        "drug_interactions": [
            {
                "drug": "acetaminophen",
                "effect": "Additive methemoglobinemia/oxidative injury risk (especially cats) — avoid concurrent oxidant drugs",
                "effect_ja": "メトヘモグロビン血症/酸化障害リスクが相加的（特に猫）— 酸化剤との併用回避",
            },
            {
                "drug": "lidocaine",
                "effect": "Counts toward total local-anesthetic dose — factor in when combining with infiltration/systemic lidocaine",
                "effect_ja": "局所麻酔薬総投与量に加算される — 浸潤麻酔や全身リドカインとの併用時は総量を考慮",
            },
        ],
    },
    {
        "id": "dextrose_50",
        "name": "Dextrose 50% (Hypertonic Glucose)",
        "name_ja": "50%ブドウ糖（デキストロース）注射液",
        "category": "miscellaneous",
        "mechanism": (
            "Hypertonic glucose solution (500 mg/mL) for emergency correction of "
            "hypoglycemia (insulinoma crisis, neonatal/juvenile hypoglycemia, "
            "xylitol toxicosis, sepsis, hepatic failure) and as a CRI substrate "
            "after dilution."
        ),
        "mechanism_ja": (
            "高張ブドウ糖液（500 mg/mL）。低血糖の救急補正（インスリノーマクリーゼ、"
            "新生子/若齢低血糖、キシリトール中毒、敗血症、肝不全）および希釈後のCRI基質として"
            "使用する。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Hypoglycemic crisis: 0.5-1 mL/kg of 50% dextrose IV, DILUTED "
                    "1:2 to 1:4 with saline (final ≤ 25%, ideally ≤ 12.5% for "
                    "peripheral veins), given slowly over 5-10 min. Follow with "
                    "2.5-5% dextrose CRI."
                ),
                "dosage_ja": (
                    "低血糖クリーゼ: 50%ブドウ糖 0.5-1 mL/kg を生理食塩液で1:2〜1:4に希釈"
                    "（最終濃度25%以下、末梢静脈では12.5%以下が望ましい）し、5-10分かけて"
                    "緩徐に静注。以後2.5-5%ブドウ糖CRIで維持。"
                ),
                "notes": (
                    "NEVER give undiluted 50% through a peripheral vein — severe "
                    "phlebitis and tissue necrosis on extravasation. Recheck glucose "
                    "every 1-2 h."
                ),
                "notes_ja": (
                    "50%原液を末梢静脈から投与しないこと — 重度の静脈炎、血管外漏出時は"
                    "組織壊死を起こす。血糖は1-2時間毎に再検。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": "As for dogs: 0.5-1 mL/kg diluted 1:2-1:4, slow IV; then 2.5-5% CRI.",
                "dosage_ja": "犬と同様: 0.5-1 mL/kg を1:2〜1:4希釈で緩徐静注。以後2.5-5% CRI。",
                "notes": "Buccal rubbing of glucose syrup is a stop-gap when no IV access (avoid aspiration).",
                "notes_ja": "静脈路がない場合は糖シロップの頬粘膜塗布が応急処置（誤嚥に注意）。",
            },
            "ferret": {
                "safe": True,
                "dosage": (
                    "Insulinoma crisis: 0.25-0.5 mL/kg of 50% dextrose diluted 1:2-1:4, "
                    "slow IV bolus ONLY if seizing; otherwise titrate a 2.5-5% CRI."
                ),
                "dosage_ja": (
                    "インスリノーマクリーゼ: 50%ブドウ糖 0.25-0.5 mL/kg を1:2〜1:4希釈し、"
                    "痙攣時のみ緩徐静注ボーラス。それ以外は2.5-5% CRIで漸増調整。"
                ),
                "notes": (
                    "In insulinoma, boluses trigger rebound insulin release and "
                    "recurrent hypoglycemia — feed small frequent meals and use the "
                    "lowest effective CRI; start prednisolone ± diazoxide for "
                    "chronic control."
                ),
                "notes_ja": (
                    "インスリノーマではボーラス投与が反跳性インスリン分泌と低血糖再発を誘発 — "
                    "頻回少量給餌と最小有効量CRIを用い、慢性管理はプレドニゾロン±ジアゾキシドを開始。"
                ),
            },
            "horse": {
                "safe": True,
                "dosage": (
                    "Neonatal foal hypoglycemia: bolus 1 mL/kg of 10% dextrose "
                    "(dilute 50% stock 1:4), then 4-8 mg/kg/min CRI titrated to "
                    "glucose."
                ),
                "dosage_ja": (
                    "新生子馬の低血糖: 10%ブドウ糖1 mL/kgをボーラス（50%原液を1:4希釈）、"
                    "以後4-8 mg/kg/分のCRIで血糖に合わせ調整。"
                ),
                "notes": "Avoid hyperglycemia in septic foals — titrate against serial glucose.",
                "notes_ja": "敗血症子馬では高血糖を回避 — 血糖の連続測定に合わせて調整。",
            },
        },
        "side_effects": (
            "Phlebitis (hypertonic — dilute for peripheral use), tissue necrosis on "
            "extravasation of concentrated solution, rebound hypoglycemia "
            "(insulinoma), hyperglycemia/osmotic diuresis with overdose."
        ),
        "side_effects_ja": (
            "静脈炎（高張のため末梢投与時は希釈必須）、濃厚液の血管外漏出による組織壊死、"
            "反跳性低血糖（インスリノーマ）、過量による高血糖・浸透圧利尿。"
        ),
        "contraindications": (
            "Undiluted peripheral administration; intracranial hemorrhage "
            "(worsens cerebral edema if overdosed); use glucose-monitored titration "
            "in septic patients."
        ),
        "contraindications_ja": (
            "原液のままの末梢静脈投与。頭蓋内出血（過量で脳浮腫を悪化）。敗血症患者では血糖監視下の漸増投与。"
        ),
        "drug_interactions": [
            {
                "drug": "insulin",
                "effect": "Physiologic antagonism — used together deliberately in hyperkalemia protocols (insulin + dextrose)",
                "effect_ja": "生理的拮抗 — 高カリウム血症プロトコルでは意図的に併用（インスリン＋ブドウ糖）",
            },
        ],
    },
]
