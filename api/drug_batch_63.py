"""Drug batch 63 – referenced-but-absent agents surfaced by the 2026-09 audit (28th sweep).

A dose-context katakana + English drug-token sweep against the live text
matcher confirmed the katakana index is saturated (Normosol-R, lactated
Ringer's, ursodeoxycholic acid, mycophenolate mofetil, biotin, tiludronate,
ProZinc etc. all resolve from their real phrasings). Three true monograph gaps
remained, every one referenced by the formulary's own disease content with
explicit doses:

  - Physostigmine — the site's own toxicology entries prescribe it by name
    ("Physostigmine 0.02-0.06 mg/kg IV slowly" for avian anticholinergic
    toxicity; "フィゾスチグミン 0.06 mg/kg IV" for refractory ivermectin coma;
    rabbit nightshade toxicosis) yet the antidote itself was absent — the same
    self-referential antidote gap previously fixed for pralidoxime, protamine
    and dexrazoxane. Its defining property versus neostigmine (already listed)
    is that it is a TERTIARY amine that crosses the blood-brain barrier, which
    is the whole reason it can reverse central anticholinergic signs.

  - Tilmicosin — the exotic_other caprine/porcine mycoplasma entries dose it
    ("チルミコシン 10 mg/kg" with route caveats). One of the most
    safety-critical drugs in the veterinary formulary: IV administration is
    fatal in every species tested (including cattle), any parenteral route is
    fatal in swine, horses and primates, and accidental human self-injection
    has caused deaths (the US Micotil label carries a physician hotline).
    Documenting those hard gates is exactly what this dictionary is for.

  - Atorvastatin — the avian aortic rupture / thromboembolism entries dose it
    ("Atorvastatin 0.3-1 mg/kg PO q24h (extrapolated)"). Atherosclerosis is
    one of the most common necropsy findings in aged psittacines (Amazons,
    greys), and statin therapy is the referenced medical option. Honest
    framing required: parrot pharmacokinetic work shows low/variable plasma
    levels, so evidence is limited — plus a CYP3A4 interaction that matters
    daily in avian practice (itraconazole for aspergillosis raises statin
    exposure → myopathy risk).

References:
  - Plumb's Veterinary Drug Handbook 10th ed — physostigmine (anticholinergic
    toxicity antidote, cholinergic-crisis cautions), tilmicosin (species
    fatality profile, cattle/sheep SC single-dose labeling).
  - Peterson & Talcott, Small Animal Toxicology 3rd ed — anticholinergic plant
    toxicoses; physostigmine use and contraindications.
  - Micotil (tilmicosin) US label / Pulmotil (in-feed) labeling — injection
    fatality warnings, human safety hotline.
  - OIE Terrestrial Manual — contagious caprine pleuropneumonia therapy.
  - Beaufrère H, J Exot Pet Med / JAVMA 2013 — psittacine atherosclerosis
    review; statins as the referenced medical therapy.
  - Beaufrère H et al., AJVR 2015 — atorvastatin pharmacokinetics in
    Hispaniolan Amazon parrots (low/variable plasma concentrations).
"""

DRUGS_BATCH_63 = [
    {
        "id": "physostigmine",
        "search_aliases": [
            "フィゾスチグミン",
            "physostigmine",
            "エゼリン",
            "eserine",
        ],
        "name": "Physostigmine",
        "name_ja": "フィゾスチグミン",
        "category": "miscellaneous",
        "mechanism": "Reversible acetylcholinesterase inhibitor that is a TERTIARY amine — unlike neostigmine (quaternary) it crosses the blood-brain barrier, so it reverses both central and peripheral antimuscarinic effects. This CNS penetration is the entire rationale for its use as the antidote for anticholinergic toxicity.",
        "mechanism_ja": "可逆的アセチルコリンエステラーゼ阻害薬。第三級アミンであるため（第四級アミンのネオスチグミンと異なり）血液脳関門を通過し、中枢・末梢両方の抗ムスカリン作用を拮抗する。このCNS移行性こそが抗コリン中毒の解毒薬として使われる根拠である。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Anticholinergic toxicity (Datura/belladonna-type plant alkaloids, antihistamine or atropine overdose with severe CNS signs): 0.02-0.06 mg/kg IV given SLOWLY over ≥5 min; effect lasts only 30-60 min, repeat as needed (Plumb's 10th ed; Peterson & Talcott 3rd ed). Refractory ivermectin/ML coma: 0.06 mg/kg IV produces transient arousal — controversial, high adverse-effect rate, reserve for ILE-refractory cases.",
                "dosage_ja": "抗コリン中毒（チョウセンアサガオ・ベラドンナ系植物アルカロイド、抗ヒスタミン薬・アトロピン過量で重度CNS症状がある場合）: 0.02-0.06 mg/kg を5分以上かけて緩徐静注。作用持続はわずか30-60分のため必要に応じ反復（Plumb's 10th ed; Peterson & Talcott 3rd ed）。難治性イベルメクチン/ML系昏睡: 0.06 mg/kg IV で一過性の覚醒 — 議論があり副作用率も高く、脂肪乳剤（ILE）不応の重症例に限定。",
                "notes": "Diagnostic-therapeutic trial: rapid (minutes) reversal of CNS depression strongly supports anticholinergic toxicosis. Have atropine drawn up before injecting — treats iatrogenic cholinergic crisis.",
                "notes_ja": "診断的治療トライアル: 投与後数分でのCNS抑制の改善は抗コリン中毒を強く支持する。医原性コリン作動性クリーゼに備え、投与前にアトロピンを準備しておくこと。",
            },
            "cat": {
                "safe": True,
                "dosage": "Anticholinergic toxicity with severe CNS signs: 0.02 mg/kg IV slowly over ≥5 min; repeat cautiously (short duration of action). Use the lowest effective dose — cats are prone to cholinergic adverse effects (salivation, bradycardia).",
                "dosage_ja": "重度CNS症状を伴う抗コリン中毒: 0.02 mg/kg を5分以上かけて緩徐静注。作用時間が短いため慎重に反復。猫はコリン作動性副作用（流涎・徐脈）が出やすく、最小有効量を用いる。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Nightshade (Solanaceae) plant toxicosis with atropine-like signs — rarely required: 0.02-0.06 mg/kg IV slowly, only when severe central signs are present; otherwise supportive care alone (the formulary's own rabbit plant-toxicosis protocol).",
                "dosage_ja": "アトロピン様症状を示すナス科植物中毒 — 必要となるのは稀: 重度の中枢症状がある場合に限り 0.02-0.06 mg/kg 緩徐静注。それ以外は支持療法のみ（本辞書のウサギ植物中毒プロトコル参照）。",
            },
            "bird": {
                "safe": True,
                "dosage": "Anticholinergic plant/drug toxicity with seizure-like CNS excitation or profound depression: 0.02-0.06 mg/kg IV slowly with careful monitoring (the formulary's avian toxin-induced seizure protocol). NOT for organophosphate/carbamate cases.",
                "dosage_ja": "痙攣様のCNS興奮または高度の抑制を伴う抗コリン性の植物・薬物中毒: 0.02-0.06 mg/kg を監視下で緩徐静注（本辞書の鳥中毒性痙攣プロトコル参照）。有機リン・カーバメート中毒には使用しない。",
            },
        },
        "contraindications": "Organophosphate or carbamate toxicosis — adding an AChE inhibitor to an AChE-poisoned patient precipitates cholinergic crisis (these cases get atropine ± pralidoxime instead). Rapid IV bolus (bradycardia, bronchospasm, seizures). Use with extreme caution in suspected TCA overdose (asystole reported in human medicine). Airway obstruction/asthmatic bronchospasm.",
        "contraindications_ja": "有機リン・カーバメート中毒 — AChEが既に阻害された患者へのAChE阻害薬追加はコリン作動性クリーゼを誘発する（これらはアトロピン±プラリドキシムの適応）。急速静注（徐脈・気管支攣縮・痙攣）。三環系抗うつ薬過量摂取疑いでは極めて慎重に（ヒト医療で心静止の報告）。気道閉塞・喘息性気管支攣縮。",
        "drug_interactions": [
            {
                "drug": "Atropine / glycopyrrolate",
                "effect": "Mutual antagonism — atropine is the rescue for physostigmine-induced cholinergic crisis; keep it drawn up",
                "effect_ja": "相互拮抗 — アトロピンはフィゾスチグミン誘発性コリン作動性クリーゼのレスキュー薬。必ず準備しておく",
                "severity": "moderate",
            },
            {
                "drug": "Succinylcholine (depolarizing NMBA)",
                "effect": "Markedly prolonged neuromuscular blockade (AChE inhibition slows succinylcholine breakdown)",
                "effect_ja": "神経筋遮断の著明な延長（AChE阻害によりサクシニルコリン分解が遅延）",
                "severity": "major",
            },
            {
                "drug": "Organophosphates / carbamates",
                "effect": "Additive AChE inhibition → cholinergic crisis — contraindicated combination",
                "effect_ja": "AChE阻害の相加 → コリン作動性クリーゼ — 禁忌の組み合わせ",
                "severity": "major",
            },
        ],
    },
    {
        "id": "tilmicosin",
        "search_aliases": [
            "チルミコシン",
            "tilmicosin",
            "ミコチル",
            "micotil",
            "プルモチル",
            "pulmotil",
        ],
        "name": "Tilmicosin",
        "name_ja": "チルミコシン（ミコチル/プルモチル）",
        "category": "antibiotics",
        "mechanism": "16-membered macrolide (tylosin derivative) binding the 50S ribosomal subunit; concentrates in lung tissue and phagocytes with days-long pulmonary persistence after a single dose — the basis of one-shot respiratory therapy in ruminants. Its cardiotoxicity (calcium-channel effects → tachycardia + negative inotropy) is what makes injection fatal in susceptible species.",
        "mechanism_ja": "16員環マクロライド（タイロシン誘導体）。50Sリボソームに結合。肺組織と貪食細胞に高濃度集積し、単回投与後も肺内に数日間残留する — 反芻類の単回注射呼吸器治療の根拠。心毒性（カルシウムチャネル作用 → 頻脈＋陰性変力作用）が感受性種での注射致死性の本体である。",
        "species_info": {
            "exotic_other": {
                "safe": True,
                "dosage": "Goats — respiratory mycoplasmosis incl. contagious caprine pleuropneumonia (adjunct to oxytetracycline; OIE-notifiable): 10 mg/kg SC as a SINGLE dose, repeat no sooner than 72 h if needed. Never IV (fatal in all species). Narrow margin in goats — do not exceed 10 mg/kg. Swine — enzootic (Mycoplasma) pneumonia: ORAL ONLY (in-feed/water, Pulmotil labeling; ~10 mg/kg/day); ANY injection is fatal in swine.",
                "dosage_ja": "ヤギ — 呼吸器マイコプラズマ症・山羊伝染性胸膜肺炎の補助（オキシテトラサイクリンと併用。OIE届出疾病）: 10 mg/kg SC 単回。再投与は最短でも72時間空ける。静注は絶対不可（全種で致死的）。ヤギは安全域が狭く10 mg/kgを超えないこと。ブタ — 豚マイコプラズマ肺炎: 経口のみ（飼料/飲水添加、プルモチル製剤。約10 mg/kg/日）。ブタへの注射は経路を問わず致死的。",
                "notes": "Cattle/sheep (reference): Micotil label = 10 mg/kg SC once. HUMAN SAFETY: accidental self-injection has killed people — never carry a loaded uncapped syringe, never use in automatically powered syringes; the US label carries an emergency physician hotline.",
                "notes_ja": "牛・羊（参考）: ミコチルのラベル用量 = 10 mg/kg SC 単回。ヒトの安全: 誤自己注射による死亡例がある — 針キャップなしの充填シリンジ携行禁止・自動注射器使用禁止。米国ラベルには緊急医師ホットラインが記載されている。",
            },
            "horse": {
                "safe": False,
                "dosage": "CONTRAINDICATED — fatal in horses by any parenteral route (acute cardiotoxicity). Do not use.",
                "dosage_ja": "禁忌 — 馬では注射経路を問わず致死的（急性心毒性）。使用しないこと。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not used in companion carnivores — no established safe dose; cardiotoxic class risk. Choose another macrolide (e.g., azithromycin) or doxycycline.",
                "dosage_ja": "伴侶肉食動物では使用しない — 安全用量が確立されておらず、クラスとして心毒性リスクがある。他のマクロライド（アジスロマイシン等）またはドキシサイクリンを選択。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not used — no established safe dose; cardiotoxic class risk.",
                "dosage_ja": "使用しない — 安全用量が確立されておらず心毒性リスクがある。",
            },
        },
        "contraindications": "IV administration in ANY species — fatal, including cattle. Any injection in swine, horses and primates — fatal. Goats: never exceed 10 mg/kg SC. Do not use in lactating dairy animals producing milk for human consumption per local regulations. Human operator risk: self-injection can be lethal.",
        "contraindications_ja": "全種における静脈内投与 — 牛を含め致死的。ブタ・馬・霊長類へのあらゆる注射 — 致死的。ヤギ: 10 mg/kg SC を超えないこと。泌乳中の乳用動物への使用は各国の規制に従い回避。ヒト（術者）リスク: 誤自己注射は致死的となりうる。",
        "drug_interactions": [
            {
                "drug": "Epinephrine (adrenaline)",
                "effect": "In swine, epinephrine INCREASES tilmicosin lethality — it is not a rescue for tilmicosin cardiotoxicity",
                "effect_ja": "ブタではアドレナリンがチルミコシンの致死性を増強する — 心毒性のレスキュー薬にはならない",
                "severity": "major",
            },
            {
                "drug": "Other macrolides / cardioactive drugs (beta blockers, calcium channel blockers)",
                "effect": "Additive negative inotropy/chronotropy risk with the drug's intrinsic cardiotoxicity",
                "effect_ja": "本剤固有の心毒性に対する陰性変力/変時作用の相加リスク",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "atorvastatin",
        "search_aliases": [
            "アトルバスタチン",
            "atorvastatin",
            "リピトール",
            "lipitor",
        ],
        "name": "Atorvastatin",
        "name_ja": "アトルバスタチン（リピトール）",
        "category": "cardiovascular",
        "mechanism": "HMG-CoA reductase inhibitor (statin): blocks the rate-limiting step of hepatic cholesterol synthesis, upregulating LDL-receptor expression and lowering circulating cholesterol; pleiotropic anti-inflammatory/plaque-stabilizing effects. Metabolized by CYP3A4 — the source of its clinically important azole interaction.",
        "mechanism_ja": "HMG-CoA還元酵素阻害薬（スタチン）: 肝コレステロール合成の律速段階を阻害し、LDL受容体発現を増加させて血中コレステロールを低下させる。抗炎症・プラーク安定化の多面的効果も持つ。CYP3A4で代謝され、これが臨床的に重要なアゾール系との相互作用の原因となる。",
        "species_info": {
            "bird": {
                "safe": True,
                "dosage": "Psittacine atherosclerosis (one of the most common necropsy findings in aged Amazons/greys — Beaufrère 2013) — adjunct to diet conversion, weight control and encouraged exercise/flight: 0.3-1 mg/kg PO q24h as used in the formulary's aortic rupture/thromboembolism protocols (extrapolated dosing). Evidence is limited: parrot PK work (Beaufrère 2015, Hispaniolan Amazons) showed low/variable plasma levels, so some clinicians use higher doses (10-20 mg/kg) — titrate to cholesterol/triglyceride response and re-check a lipid panel after 4-8 weeks.",
                "dosage_ja": "オウム類のアテローム性動脈硬化症（高齢アマゾン・ヨウムの剖検で最多クラスの所見 — Beaufrère 2013）— 食事転換・体重管理・運動/飛翔の奨励への補助として: 本辞書の大動脈破裂/血栓塞栓症プロトコルで用いる 0.3-1 mg/kg PO q24h（外挿用量）。エビデンスは限定的: オウムのPK研究（Beaufrère 2015、アマゾン）では血中濃度が低く変動が大きいため、より高用量（10-20 mg/kg）を用いる臨床家もいる — コレステロール/中性脂肪の反応で漸増し、4-8週後に脂質パネルを再検する。",
                "notes": "Statins do not reverse established plaques; the goal is progression control and thromboembolism risk reduction. Address the diet (seed→formulated pellets + vegetables) first — it is the single highest-yield intervention.",
                "notes_ja": "スタチンは既成プラークを消退させない。目標は進行抑制と血栓塞栓リスクの低減である。まず食事（シード食→ペレット＋野菜）を是正すること — 単独で最も効果の大きい介入である。",
            },
            "dog": {
                "safe": True,
                "dosage": "Rarely indicated: canine hyperlipidemia is usually hypertriglyceridemia (fibrates first — bezafibrate; see that monograph). Reserve statins for documented refractory hypercholesterolemia after excluding secondary causes (hypothyroidism, Cushing's, diabetes): atorvastatin 1-3 mg/kg PO q24h reported anecdotally; monitor CK and liver enzymes.",
                "dosage_ja": "適応は稀: 犬の高脂血症は通常は高トリグリセリド血症であり、第一選択はフィブラート系（ベザフィブラート — 当該モノグラフ参照）。続発性原因（甲状腺機能低下・クッシング・糖尿病）除外後の難治性高コレステロール血症に限定: アトルバスタチン 1-3 mg/kg PO q24h の使用報告がある。CKと肝酵素をモニタリング。",
            },
        },
        "contraindications": "Active hepatic disease (transaminase elevation is the class hepatotoxicity signal). Pregnancy. Myopathy/CK elevation — stop if muscle pain/weakness with CK rise (class effect, dose- and interaction-dependent).",
        "contraindications_ja": "活動性肝疾患（トランスアミナーゼ上昇はクラス共通の肝毒性シグナル）。妊娠。ミオパチー/CK上昇 — 筋痛・脱力とCK上昇があれば中止（クラス効果。用量・相互作用依存性）。",
        "drug_interactions": [
            {
                "drug": "Itraconazole / ketoconazole (azole antifungals)",
                "effect": "CYP3A4 inhibition raises statin exposure → myopathy/rhabdomyolysis risk — directly relevant in birds on itraconazole for aspergillosis; pause or reduce the statin during azole courses",
                "effect_ja": "CYP3A4阻害でスタチン曝露が上昇 → ミオパチー/横紋筋融解リスク — アスペルギルス症でイトラコナゾール投与中の鳥ではまさに現実的な併用。アゾール投与期間中はスタチンを休薬または減量",
                "severity": "major",
            },
            {
                "drug": "Cyclosporine",
                "effect": "Markedly increased statin levels (OATP1B1/CYP3A4 inhibition) → myopathy risk",
                "effect_ja": "スタチン血中濃度の著明な上昇（OATP1B1/CYP3A4阻害）→ ミオパチーリスク",
                "severity": "major",
            },
            {
                "drug": "Fibrates (bezafibrate, gemfibrozil)",
                "effect": "Additive myopathy risk when combined — combine only with monitoring and clear indication",
                "effect_ja": "併用でミオパチーリスクが相加 — 明確な適応とモニタリング下でのみ併用",
                "severity": "moderate",
            },
        ],
    },
]
