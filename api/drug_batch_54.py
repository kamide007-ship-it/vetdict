"""Drug batch 54 – referenced-but-absent agents surfaced by the 2026-09 audit (20th sweep).

The dose-context token audit (treatment texts cross-checked against
find_drugs_in_text) found four agents that the site's own curated disease
content prescribes with explicit doses, yet no monograph existed:

  - Tiopronin (2-MPG) — the dog Cystinuria / Nephrolithiasis / Bladder
    Stones entries name "チオプロニン 15-20 mg/kg PO q12h" as the first-line
    dissolution agent for cystine uroliths (ACVIM consensus, Lulich et al.
    JVIM 2016; Hoppe & Denneberg JVIM 2001), yet only the alternative
    D-penicillamine was in the formulary.
  - Diclazuril (Protazil) — the equine EPM entries cite "ジクラズリル 1 mg/kg
    PO q24h × 28日間（Protazil®）" (FDA NADA 141-268) and the avian
    sarcocystosis entry uses 10 mg/kg PO q24h (Carpenter Exotic Animal
    Formulary), yet only ponazuril of the triazine anticoccidials existed.
  - Isoproterenol — the third-degree AV block entries for dog, cat AND
    horse all prescribe an isoproterenol CRI (0.04-0.08 μg/kg/min) as the
    pharmacologic bridge to pacemaker implantation (Plumb's 10th; Ettinger
    8th; Reed & Bayly 4th ed), yet no monograph existed.
  - Diminazene aceturate (ガナゼック) — the drug approved and most widely
    used in Japan for canine babesiosis; referenced (without dose) by the
    feline cytauxzoonosis/babesiosis entries and dosed explicitly by the
    equine dourine entry ("ジミナゼン3.5 mg/kg IM×2回"). Narrow safety
    margin in dogs (dose-dependent CNS haemorrhagic necrosis) is a
    defining safety fact that belongs in the formulary.

References:
  - Lulich JP et al. ACVIM Small Animal Consensus Recommendations on the
    Treatment and Prevention of Uroliths. J Vet Intern Med 2016.
  - Hoppe A, Denneberg T. Cystinuria in the dog: clinical studies during
    14 years of medical treatment. J Vet Intern Med 2001.
  - Protazil (1.56% diclazuril) FDA NADA 141-268; Reed SM et al. ACVIM
    consensus statement: EPM. J Vet Intern Med 2016.
  - Plumb's Veterinary Drug Handbook 10th ed — isoproterenol, diminazene.
  - Irwin PJ. Canine babesiosis: from molecular taxonomy to control.
    Parasit Vectors 2009 (diminazene regional standard; B. gibsoni relapse).
  - Carpenter Exotic Animal Formulary 6th ed — avian diclazuril.
"""

DRUGS_BATCH_54 = [
    {
        "id": "tiopronin",
        "search_aliases": [
            "2-MPG",
            "チオラ",
            "Thiola",
            "メルカプトプロピオニルグリシン",
            "Tiopronin",
        ],
        "name": "Tiopronin (2-MPG)",
        "name_ja": "チオプロニン（2-MPG）",
        "category": "urinary",
        "mechanism": "Thiol donor that undergoes thiol-disulfide exchange with cystine, forming a mixed tiopronin-cysteine disulfide that is up to 50 times more water-soluble than cystine. Reduces urinary cystine concentration below the solubility threshold, dissolving existing cystine uroliths and preventing recurrence in cystinuric dogs. First-line medical dissolution agent (better tolerated than D-penicillamine).",
        "mechanism_ja": "チオール供与体。シスチンとチオール-ジスルフィド交換反応を起こし、シスチンの最大50倍水溶性の高いチオプロニン・システイン混合ジスルフィドを形成する。尿中シスチン濃度を溶解閾値以下に低下させ、シスチン結石の内科的溶解と再発予防を可能にする。D-ペニシラミンより忍容性が高く、溶解療法の第一選択。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Dissolution: 15-20 mg/kg PO q12h with an alkalinising low-protein diet (target urine pH ≥7.5); recheck urinalysis + imaging q4-6 weeks — median dissolution 1-3 months. Prevention after dissolution/surgery: 10-15 mg/kg PO q12h long term (ACVIM consensus, Lulich 2016; Hoppe & Denneberg 2001).",
                "dosage_ja": "溶解療法: 15-20 mg/kg PO q12h をアルカリ化低蛋白食（目標尿pH≥7.5）と併用。4-6週毎に尿検査+画像で再評価 — 溶解期間の中央値は1-3ヶ月。溶解/摘出後の再発予防: 10-15 mg/kg PO q12h を長期継続（ACVIMコンセンサス Lulich 2016; Hoppe & Denneberg 2001）。",
                "notes": "Intact male dogs with androgen-dependent cystinuria (e.g. Mastiff-type): castration alone markedly reduces cystine excretion — evaluate before lifelong drug therapy. Monitor CBC and urine protein q3-6 months (proteinuria, rare thrombocytopenia/myopathy).",
                "notes_ja": "アンドロゲン依存性シスチン尿症の未去勢雄（マスティフ系等）は去勢のみで尿中シスチン排泄が著減する — 生涯投薬の前に評価。CBCと尿蛋白を3-6ヶ月毎にモニタリング（蛋白尿、稀に血小板減少・ミオパチー）。",
            },
        },
        "side_effects": "Vomiting/inappetence (sulfur taste), proteinuria, rarely myopathy, thrombocytopenia, aggressive behaviour change reported in some dogs",
        "side_effects_ja": "嘔吐・食欲不振（硫黄味）、蛋白尿、稀にミオパチー・血小板減少、一部の犬で攻撃的な行動変化の報告",
        "contraindications": "History of tiopronin/penicillamine hypersensitivity or blood dyscrasia. Not a substitute for dietary management — always combine with alkalinising low-protein diet and increased water intake. Reduce dose if proteinuria develops",
        "contraindications_ja": "チオプロニン/ペニシラミン過敏症・血液異常の既往。食事療法の代替ではない — 必ずアルカリ化低蛋白食と飲水量増加を併用。蛋白尿が出現したら減量",
        "drug_interactions": [],
    },
    {
        "id": "diclazuril",
        "search_aliases": ["Protazil", "プロタジル", "Diclazuril"],
        "name": "Diclazuril",
        "name_ja": "ジクラズリル",
        "category": "antiparasitics",
        "mechanism": "Benzeneacetonitrile triazine antiprotozoal. Targets the apicoplast of apicomplexan protozoa (Sarcocystis neurona, Eimeria spp.), disrupting merozoite division. FDA-approved (Protazil, alfalfa-based pellet top-dress) for equine protozoal myeloencephalitis; also used for avian coccidiosis/sarcocystosis.",
        "mechanism_ja": "ベンゼンアセトニトリル系トリアジン抗原虫薬。アピコンプレクサ原虫（Sarcocystis neurona、Eimeria属）のアピコプラストを標的としメロゾイト分裂を阻害する。馬原虫性脊髄脳炎（EPM）に対しFDA承認（Protazil、アルファルファペレット飼料混和）。鳥のコクシジウム症/サルコシスティス症にも使用。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "EPM: 1 mg/kg PO q24h × 28 days (Protazil 1.56% pellets as top-dress; FDA NADA 141-268). Alternative to ponazuril — comparable CNS penetration of active triazine metabolites (Reed et al. ACVIM consensus JVIM 2016).",
                "dosage_ja": "EPM: 1 mg/kg PO q24h × 28日間（Protazil 1.56%ペレットを飼料に混和。FDA NADA 141-268）。ポナズリルの代替 — 活性トリアジン代謝物のCNS移行性は同等（Reed et al. ACVIMコンセンサス JVIM 2016）。",
                "notes": "Re-evaluate neurologic grade at 28 days; extended courses used in relapsing EPM. Combine with vitamin E antioxidant support.",
                "notes_ja": "28日時点で神経学的グレードを再評価。再発性EPMでは投与期間延長も。ビタミンE抗酸化サポートを併用。",
            },
            "bird": {
                "safe": True,
                "dosage": "Sarcocystosis / refractory coccidiosis: 5-10 mg/kg PO q24h × 5-7 days (Carpenter Exotic Animal Formulary 6th ed).",
                "dosage_ja": "サルコシスティス症/難治性コクシジウム症: 5-10 mg/kg PO q24h × 5-7日（Carpenter Exotic Animal Formulary 6th ed）。",
                "notes": "Toltrazuril/ponazuril are alternatives; supportive fluid therapy for acute sarcocystosis.",
                "notes_ja": "トルトラズリル/ポナズリルが代替。急性サルコシスティス症では輸液による支持療法を併用。",
            },
        },
        "side_effects": "Well tolerated at label doses; soft feces reported occasionally in horses",
        "side_effects_ja": "承認用量では忍容性良好。馬で軟便が時に報告される",
        "contraindications": "Safety in breeding/pregnant horses not fully established — use only when benefit outweighs risk",
        "contraindications_ja": "繁殖馬・妊娠馬での安全性は十分に確立されていない — 有益性がリスクを上回る場合のみ使用",
        "drug_interactions": [],
    },
    {
        "id": "isoproterenol",
        "search_aliases": ["イソプレナリン", "Isoprenaline", "Isoproterenol"],
        "name": "Isoproterenol",
        "name_ja": "イソプロテレノール",
        "category": "cardiovascular",
        "mechanism": "Non-selective β1/β2-adrenergic agonist. β1 stimulation increases sinus rate, AV nodal conduction and ventricular escape-rhythm rate — the pharmacologic bridge for symptomatic high-grade (third-degree) AV block until pacemaker implantation. β2 stimulation causes vasodilation and bronchodilation, so blood pressure may fall despite the chronotropic effect.",
        "mechanism_ja": "非選択的β1/β2アドレナリン作動薬。β1刺激により洞調律・房室伝導・心室補充調律のレートを上げる — 症候性の高度（第3度）房室ブロックに対するペースメーカー植込みまでの薬理学的ブリッジ。β2刺激は血管拡張・気管支拡張を起こすため、心拍数増加にもかかわらず血圧は低下しうる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Symptomatic third-degree AV block (bridge to pacing): 0.04-0.08 μg/kg/min IV CRI, titrate to a stable escape rate; often only partially effective (Plumb's 10th; Ettinger 8th ed). Atropine response test should precede (vagally mediated block excluded).",
                "dosage_ja": "症候性第3度房室ブロック（ペーシングまでのブリッジ）: 0.04-0.08 μg/kg/分 IV CRI、安定した補充調律レートまで漸増。効果は部分的なことが多い（Plumb's 10th; Ettinger 8th ed）。先にアトロピン反応試験を実施（迷走神経性ブロックの除外）。",
                "notes": "Definitive therapy is pacemaker implantation — isoproterenol is a temporary bridge only. Monitor ECG continuously for ventricular ectopy.",
                "notes_ja": "根治療法はペースメーカー植込み — イソプロテレノールは一時的ブリッジに限る。心室性期外収縮の出現をECGで持続監視。",
            },
            "cat": {
                "safe": True,
                "dosage": "Third-degree AV block: 0.04-0.08 μg/kg/min IV CRI (Plumb's 10th). Investigate underlying myocardial disease (HCM, myocarditis, infiltrative lymphoma).",
                "dosage_ja": "第3度房室ブロック: 0.04-0.08 μg/kg/分 IV CRI（Plumb's 10th）。基礎心筋疾患（HCM、心筋炎、浸潤性リンパ腫）を精査。",
                "notes": "Many cats with third-degree AV block have adequate escape rates and are managed without pacing — reserve CRI for syncopal/low-output patients.",
                "notes_ja": "第3度房室ブロックの猫は補充調律が十分でペーシング不要のことも多い — CRIは失神・低心拍出例に限定。",
            },
            "horse": {
                "safe": True,
                "dosage": "Complete AV block (emergency rate support): 0.05-0.4 μg/kg/min IV CRI titrated to effect (Reed & Bayly 4th ed). Atropine 0.01-0.02 mg/kg IV first to assess vagal component.",
                "dosage_ja": "完全房室ブロック（応急的心拍数維持）: 0.05-0.4 μg/kg/分 IV CRI を効果に合わせ漸増（Reed & Bayly 4th ed）。先にアトロピン 0.01-0.02 mg/kg IV で迷走神経性要素を評価。",
                "notes": "Enforce strict rest (no exercise) until definitive management; transvenous pacing where available.",
                "notes_ja": "根治的管理まで運動は行わせない（厳重な休養）。可能な施設では経静脈ペーシングを実施。",
            },
        },
        "side_effects": "Ventricular tachyarrhythmias (dose-dependent), hypotension (β2 vasodilation), tremor, increased myocardial oxygen demand",
        "side_effects_ja": "心室性頻脈性不整脈（用量依存性）、低血圧（β2血管拡張）、振戦、心筋酸素需要の増大",
        "contraindications": "Tachyarrhythmias — especially digitalis-induced (risk of ventricular fibrillation). Not for cardiac arrest (RECOVER uses epinephrine). Use lowest effective rate; myocardial ischemia risk with prolonged high-dose infusion",
        "contraindications_ja": "頻脈性不整脈 — 特にジギタリス中毒性（心室細動リスク）。心停止には使用しない（RECOVERはエピネフリンを使用）。最低有効量で使用。高用量持続投与は心筋虚血リスク",
        "drug_interactions": [
            {
                "drug": "Digoxin",
                "effect": "Digitalis-sensitised myocardium + β-agonist markedly increases risk of ventricular tachycardia/fibrillation",
                "effect_ja": "ジギタリスで感作された心筋にβ作動薬を併用すると心室頻拍/細動のリスクが著増",
                "severity": "major",
            },
            {
                "drug": "Propranolol (β-blockers)",
                "effect": "Pharmacologic antagonism — β-blockade abolishes the chronotropic effect",
                "effect_ja": "薬理学的拮抗 — β遮断により陽性変時作用が消失",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "diminazene",
        "search_aliases": [
            "ガナゼック",
            "ベレニル",
            "Ganaseg",
            "Berenil",
            "ジミナゼンアセチュレート",
            "Diminazene",
        ],
        "name": "Diminazene Aceturate",
        "name_ja": "ジミナゼン",
        "category": "antiparasitics",
        "mechanism": "Aromatic diamidine antiprotozoal. Binds kinetoplast DNA of Babesia and Trypanosoma spp., inhibiting kinetoplast replication. The drug approved and most widely used in Japan for canine babesiosis (ガナゼック); also the classic treatment for trypanosomiasis (dourine, surra). Narrow safety margin — dose-dependent CNS haemorrhagic necrosis in dogs.",
        "mechanism_ja": "芳香族ジアミジン系抗原虫薬。バベシア・トリパノソーマのキネトプラストDNAに結合し複製を阻害する。日本で犬バベシア症に承認され最も広く使われる薬剤（ガナゼック）。トリパノソーマ症（媾疫・スーラ病）の古典的治療薬でもある。安全域が狭く、犬では用量依存性のCNS出血性壊死を起こす。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Large Babesia (B. canis/vogeli, incl. Japanese field cases): 3.5 mg/kg IM once (Japan-approved ガナゼック; Plumb's 10th). B. gibsoni: parasitemia reduction only — relapse is common; atovaquone 13.3 mg/kg PO q8h + azithromycin 10 mg/kg PO q24h × 10 days is the evidence-based first line (Birkenheuer 2004; Irwin 2009).",
                "dosage_ja": "大型バベシア（B. canis/vogeli、国内症例含む）: 3.5 mg/kg IM 単回（日本承認ガナゼック; Plumb's 10th）。B. gibsoni: 原虫血症の減少にとどまり再発が多い — アトバコン 13.3 mg/kg PO q8h＋アジスロマイシン 10 mg/kg PO q24h × 10日がエビデンス上の第一選択（Birkenheuer 2004; Irwin 2009）。",
                "notes": "NARROW SAFETY MARGIN: doses ≥7 mg/kg or repeated dosing within days cause haemorrhagic necrosis of the midbrain/cerebellum (ataxia, opisthotonus, seizures, death). Do not exceed 3.5 mg/kg and do not repeat within 24-48 h. Post-treatment PCR to confirm clearance.",
                "notes_ja": "安全域が狭い: 7 mg/kg以上または数日内の反復投与で中脳・小脳の出血性壊死（失調、後弓反張、痙攣、死亡）。3.5 mg/kgを超えない・24-48時間以内に再投与しない。治療後はPCRで原虫消失を確認。",
            },
            "cat": {
                "safe": True,
                "dosage": "Feline babesiosis / cytauxzoonosis (salvage only): 3 mg/kg IM once — efficacy is distinctly lower than in dogs; atovaquone 15 mg/kg PO q8h + azithromycin 10 mg/kg PO q24h is the treatment of choice for Cytauxzoon felis (Cohn 2011).",
                "dosage_ja": "猫バベシア症/サイトークスゾーン症（サルベージのみ）: 3 mg/kg IM 単回 — 有効性は犬より明らかに低い。Cytauxzoon felis はアトバコン 15 mg/kg PO q8h＋アジスロマイシン 10 mg/kg PO q24h が第一選択（Cohn 2011）。",
                "notes": "Limited feline safety data — reserve for cases where atovaquone-based therapy is unavailable.",
                "notes_ja": "猫での安全性データは限定的 — アトバコンベース治療が入手不能な場合に限定。",
            },
            "horse": {
                "safe": True,
                "dosage": "Dourine / surra (Trypanosoma equiperdum/evansi): 3.5 mg/kg IM, repeat once after 24-48 h; treatment effect is inconsistent and relapse occurs. Equine piroplasmosis: imidocarb is the drug of choice — diminazene is an alternative for Babesia caballi (11 mg/kg IM ×2, 24 h apart), less effective for Theileria equi.",
                "dosage_ja": "媾疫/スーラ病（Trypanosoma equiperdum/evansi）: 3.5 mg/kg IM、24-48時間後に1回反復。治療効果は不確実で再発あり。馬ピロプラズマ症: 第一選択はイミドカルブ — ジミナゼンは B. caballi の代替（11 mg/kg IM×2回、24時間間隔）で、Theileria equi には効果が劣る。",
                "notes": "Dourine/surra are notifiable diseases — report to authorities; test-and-slaughter policies apply in many regions.",
                "notes_ja": "媾疫・スーラ病は届出伝染病 — 当局へ報告。多くの地域で摘発淘汰の対象。",
            },
        },
        "side_effects": "Pain/swelling at IM injection site, vomiting, hypotension; dose-dependent neurotoxicity in dogs (ataxia, nystagmus, opisthotonus, seizures — CNS haemorrhagic necrosis)",
        "side_effects_ja": "筋注部位の疼痛・腫脹、嘔吐、低血圧。犬で用量依存性神経毒性（失調、眼振、後弓反張、痙攣 — CNS出血性壊死）",
        "contraindications": "Do not exceed 3.5 mg/kg in dogs or repeat within 24-48 h (neurotoxicity). Severe hepatic/renal impairment: use with caution. Camelids are exquisitely sensitive — avoid",
        "contraindications_ja": "犬で3.5 mg/kg超・24-48時間以内の反復投与は禁止（神経毒性）。重度の肝・腎障害では慎重投与。ラクダ類は極めて感受性が高く回避",
        "drug_interactions": [],
    },
]
