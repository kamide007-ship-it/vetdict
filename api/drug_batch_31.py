"""Drug batch 31 – anaesthetic agents referenced by the anaesthesia protocols
but previously missing from the drug dictionary.

Every agent here is named in `api/anesthesia_protocols.py` (protocol drug rows,
premedication combinations or the equine "triple drip"), so a clinician tapping
the drug in the anaesthesia table should land on a real formulary entry rather
than an empty search. Detomidine additionally *mis-resolved* to Medetomidine via
a naive substring match before this entry existed.

References:
  - Plumb's Veterinary Drug Handbook, 10th ed.
  - Lumb & Jones' Veterinary Anesthesia and Analgesia, 5th ed. (Grimm et al.)
  - Muir & Hubbell, Equine Anesthesia: Monitoring and Emergency Therapy, 2nd ed.
  - Carpenter, Exotic Animal Formulary, 6th ed. (fish immersion agents).
  - BSAVA Manual of Canine and Feline Anaesthesia and Analgesia, 3rd ed.
"""

from __future__ import annotations

DRUGS_BATCH_31: list[dict] = [
    {
        "id": "thiopental",
        "name": "Thiopental (Sodium Thiopental)",
        "name_ja": "チオペンタール（チオペンタールナトリウム）",
        "category": "anesthetics",
        "mechanism": (
            "Ultra-short-acting thiobarbiturate. Potentiates GABA-A chloride "
            "conductance producing rapid, smooth IV induction; anaesthesia ends "
            "by redistribution from brain to muscle and fat rather than by "
            "metabolism. Largely superseded by propofol and alfaxalone but still "
            "referenced for induction where those are unavailable."
        ),
        "mechanism_ja": (
            "超短時間作用型チオバルビツール酸。GABA-A受容体のクロライドコンダクタンスを"
            "増強し、円滑で速やかな静脈内導入をもたらす。麻酔からの覚醒は代謝ではなく脳から"
            "筋・脂肪への再分布による。プロポフォール・アルファキサロンにほぼ置換されたが、"
            "それらが利用できない場合の導入薬として参照される。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-20 mg/kg IV to effect (unpremedicated); 4-8 mg/kg after premedication. Give slowly via catheter.",
                "dosage_ja": "10-20 mg/kg 静注 効果発現まで（無前投薬時）。前投薬後は4-8 mg/kg。カテーテルから緩徐に投与。",
                "notes": "Strictly IV via a secure catheter — perivascular injection causes tissue necrosis. Transient apnoea and biphasic (bigeminal) arrhythmias are common. Avoid in cardiovascular compromise.",
                "notes_ja": "確実なカテーテルから厳密に静注（血管外漏出は組織壊死を起こす）。一過性無呼吸・二連脈性不整脈が多い。循環不全では回避。",
            },
            "cat": {
                "safe": True,
                "dosage": "5-10 mg/kg IV to effect",
                "dosage_ja": "5-10 mg/kg 静注 効果発現まで",
                "notes": "Titrate slowly. Prolonged recovery in debilitated or hypoproteinaemic cats (increased free fraction).",
                "notes_ja": "緩徐に調節。衰弱・低蛋白血症の猫では遊離型増加により覚醒遷延。",
            },
            "horse": {
                "safe": True,
                "dosage": "6-12 mg/kg IV to effect, following alpha-2 sedation (often with guaifenesin)",
                "dosage_ja": "6-12 mg/kg 静注 効果発現まで。α2鎮静後（多くはグアイフェネシン併用）に投与。",
                "notes": "Give after adequate sedation to ensure a controlled induction and recumbency.",
                "notes_ja": "十分な鎮静後に投与し、制御された導入・横臥を得る。",
            },
        },
        "side_effects": "Dose-dependent respiratory depression/apnoea, ventricular bigeminy, hypotension, laryngospasm, perivascular tissue necrosis (highly alkaline).",
        "side_effects_ja": "用量依存性の呼吸抑制・無呼吸、心室性二連脈、低血圧、喉頭痙攣、血管外漏出時の組織壊死（強アルカリ性）。",
        "contraindications": "Sighthounds (very slow recovery — low body fat, slow redistribution); severe cardiovascular or hepatic disease; caesarean section (crosses placenta). Do not give perivascularly or intra-arterially.",
        "contraindications_ja": "サイトハウンド（低体脂肪・再分布緩徐で覚醒著しく遷延）、重度の心血管・肝疾患、帝王切開（胎盤通過）。血管外・動脈内投与は禁止。",
        "drug_interactions": [
            {
                "drug": "acepromazine",
                "effect": "Additive cardiovascular and respiratory depression; enhanced hypotension",
                "effect_ja": "心血管・呼吸抑制が相加的に増強、低血圧が助長される",
            },
            {
                "drug": "opioids",
                "effect": "Potentiated respiratory depression; lower induction dose required",
                "effect_ja": "呼吸抑制が増強、必要導入量が減少",
            },
        ],
    },
    {
        "id": "guaifenesin",
        "name": "Guaifenesin (GGE, Glyceryl Guaiacolate)",
        "name_ja": "グアイフェネシン（GGE、グリセリルグアヤコレート）",
        "category": "muscle_relaxants",
        "mechanism": (
            "Centrally acting muscle relaxant that depresses internuncial "
            "transmission in the spinal cord and brainstem, producing skeletal "
            "muscle relaxation with minimal effect on the diaphragm. Not an "
            "anaesthetic or analgesic on its own; the muscle-relaxant carrier of "
            "the equine 'triple drip' (guaifenesin + ketamine + alpha-2 agonist) "
            "for total intravenous anaesthesia."
        ),
        "mechanism_ja": (
            "中枢性筋弛緩薬。脊髄・脳幹の介在ニューロン伝達を抑制し、横隔膜への影響を"
            "最小限に骨格筋を弛緩させる。単独では麻酔・鎮痛作用はない。馬のTIVA用"
            "「トリプルドリップ」（グアイフェネシン＋ケタミン＋α2作動薬）の筋弛緩基剤。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "5% solution, 50-100 mg/kg IV to effect (recumbency); do not exceed ~150 mg/kg",
                "dosage_ja": "5%液を50-100 mg/kg 静注 効果発現（横臥）まで。約150 mg/kgを超えない。",
                "notes": "Carrier of the 'triple drip' TIVA (typically 50 mg/mL guaifenesin + 1-2 mg/mL ketamine + xylazine/detomidine). Concentrations >10% cause haemolysis; perivascular injection causes thrombophlebitis/necrosis.",
                "notes_ja": "「トリプルドリップ」TIVAの基剤（通常グアイフェネシン50 mg/mL＋ケタミン1-2 mg/mL＋キシラジン/デトミジン）。10%超で溶血、血管外漏出で血栓性静脈炎・壊死。",
            },
            "cattle": {
                "safe": True,
                "dosage": "5% solution, 50-100 mg/kg IV to effect",
                "dosage_ja": "5%液を50-100 mg/kg 静注 効果発現まで",
                "notes": "Ruminants are more sensitive than horses; titrate. Component of GKX ('triple drip').",
                "notes_ja": "反芻獣は馬より感受性が高く、調節投与。GKX（トリプルドリップ）の構成成分。",
            },
        },
        "side_effects": "Recumbency, transient hypotension and tachypnoea at induction; haemolysis and haemoglobinuria at concentrations >10%; thrombophlebitis if given perivascularly.",
        "side_effects_ja": "横臥、導入時の一過性低血圧・頻呼吸、10%超濃度での溶血・ヘモグロビン尿、血管外投与時の血栓性静脈炎。",
        "contraindications": "Do not use solutions >10% (haemolysis). Avoid perivascular injection. No analgesia — must be combined with ketamine/alpha-2 agonist for surgical procedures.",
        "contraindications_ja": "10%超の溶液は使用しない（溶血）。血管外投与を避ける。鎮痛作用はなく、外科手技にはケタミン/α2作動薬との併用が必須。",
        "drug_interactions": [
            {
                "drug": "ketamine",
                "effect": "Standard 'triple drip' combination — guaifenesin provides relaxation, ketamine provides anaesthesia/analgesia",
                "effect_ja": "標準的な「トリプルドリップ」併用—グアイフェネシンが弛緩、ケタミンが麻酔・鎮痛を担う",
            },
            {
                "drug": "xylazine",
                "effect": "Standard 'triple drip' combination for equine/ruminant TIVA",
                "effect_ja": "馬・反芻獣TIVA用の標準的「トリプルドリップ」併用",
            },
        ],
    },
    {
        "id": "detomidine",
        "name": "Detomidine (Dormosedan)",
        "name_ja": "デトミジン（ドルモセダン）",
        "category": "sedatives",
        "mechanism": (
            "Potent alpha-2 adrenergic agonist producing dose-dependent sedation, "
            "analgesia and muscle relaxation, primarily in horses and cattle. More "
            "potent and longer-acting than xylazine. Distinct from medetomidine — "
            "do not confuse the two. Reversible with atipamezole or yohimbine."
        ),
        "mechanism_ja": (
            "強力なα2アドレナリン作動薬。主に馬・牛で用量依存性の鎮静・鎮痛・筋弛緩を"
            "もたらす。キシラジンより強力かつ作用時間が長い。メデトミジンとは別薬剤で"
            "混同しないこと。アティパメゾールまたはヨヒンビンで拮抗可能。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "10-40 μg/kg IV or IM for standing sedation; sublingual gel 0.04 mg/kg (Dormosedan Gel)",
                "dosage_ja": "10-40 μg/kg 静注または筋注で立位鎮静。舌下ゲル0.04 mg/kg（ドルモセダンゲル）。",
                "notes": "Often combined with butorphanol or morphine for standing procedures/CRI. Expect bradycardia, AV block, ataxia, sweating, diuresis and transient hyperglycaemia.",
                "notes_ja": "立位処置・CRIではブトルファノールやモルヒネと併用することが多い。徐脈・房室ブロック・運動失調・発汗・利尿・一過性高血糖に注意。",
            },
            "cattle": {
                "safe": True,
                "dosage": "10-30 μg/kg IV/IM",
                "dosage_ja": "10-30 μg/kg 静注/筋注",
                "notes": "Ruminants are highly sensitive to alpha-2 agonists; use the low end. Salivation and ruminal atony.",
                "notes_ja": "反芻獣はα2作動薬に高感受性で低用量を用いる。流涎・ルーメン運動停止。",
            },
        },
        "side_effects": "Bradycardia, first/second-degree AV block, transient hypertension then hypotension, ataxia, sweating (horse), diuresis, transient hyperglycaemia, reduced GI motility.",
        "side_effects_ja": "徐脈、第1/2度房室ブロック、一過性高血圧に続く低血圧、運動失調、発汗（馬）、利尿、一過性高血糖、消化管運動低下。",
        "contraindications": "Advanced cardiac disease/AV block, shock, severe respiratory disease. Use with caution in the last trimester of pregnancy (may increase uterine tone). Reverse excessive effect with atipamezole.",
        "contraindications_ja": "進行した心疾患・房室ブロック、ショック、重度呼吸器疾患。妊娠末期は慎重投与（子宮筋緊張が高まる可能性）。過度の作用はアティパメゾールで拮抗。",
        "drug_interactions": [
            {
                "drug": "atipamezole",
                "effect": "Specific alpha-2 antagonist — reverses sedation/cardiovascular effects",
                "effect_ja": "特異的α2拮抗薬—鎮静・循環作用を拮抗",
            },
            {
                "drug": "butorphanol",
                "effect": "Synergistic sedation/analgesia for standing procedures (common equine combination)",
                "effect_ja": "立位処置での鎮静・鎮痛が相乗（一般的な馬の併用）",
            },
        ],
    },
    {
        "id": "mepivacaine",
        "name": "Mepivacaine (Carbocaine) 2%",
        "name_ja": "メピバカイン（カルボカイン）2%",
        "category": "anesthetics",
        "mechanism": (
            "Intermediate-acting amide local anaesthetic. Blocks voltage-gated "
            "sodium channels to prevent nerve impulse conduction. Causes less "
            "tissue irritation and less vasodilation than lidocaine, which makes "
            "it the preferred agent for equine diagnostic perineural and "
            "intra-articular blocks."
        ),
        "mechanism_ja": (
            "中時間作用型アミド型局所麻酔薬。電位依存性ナトリウムチャネルを遮断し神経"
            "インパルス伝導を阻止する。リドカインより組織刺激・血管拡張が少なく、馬の"
            "診断的神経周囲ブロック・関節内ブロックの第一選択となる。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "2% solution for perineural/intra-articular blocks; volume per site (e.g. 2-5 mL palmar digital nerve block). Onset ~10 min, duration 1.5-2 hr.",
                "dosage_ja": "2%液を神経周囲・関節内ブロックに使用。部位ごとの容量（例：掌側指神経ブロック2-5 mL）。発現約10分、持続1.5-2時間。",
                "notes": "Preferred over lidocaine for lameness work-ups — less pain on injection and less tissue reaction.",
                "notes_ja": "跛行診断ではリドカインより好まれる—注射時痛・組織反応が少ない。",
            },
            "dog": {
                "safe": True,
                "dosage": "Local infiltration/nerve blocks; maximum ~4-6 mg/kg total",
                "dosage_ja": "局所浸潤・神経ブロック。総量最大約4-6 mg/kg。",
                "notes": "Respect the total mg/kg ceiling to avoid systemic (CNS/cardiac) toxicity.",
                "notes_ja": "全身毒性（中枢/心）回避のため総mg/kg上限を厳守。",
            },
            "cat": {
                "safe": True,
                "dosage": "Local infiltration/nerve blocks; maximum ~2-3 mg/kg total (cats are more sensitive)",
                "dosage_ja": "局所浸潤・神経ブロック。総量最大約2-3 mg/kg（猫は高感受性）。",
                "notes": "Cats are more susceptible to local-anaesthetic toxicity — use the lowest effective dose.",
                "notes_ja": "猫は局所麻酔薬毒性に感受性が高く、最小有効量を用いる。",
            },
        },
        "side_effects": "Dose-related CNS signs (tremors, seizures) then cardiovascular depression if the mg/kg ceiling is exceeded or on inadvertent IV injection; rare local tissue reaction.",
        "side_effects_ja": "用量依存性の中枢症状（振戦・痙攣）に続く心血管抑制（mg/kg上限超過・誤静注時）、まれに局所組織反応。",
        "contraindications": "Do not inject intravascularly (aspirate before injecting). Do not exceed the species mg/kg maximum. Avoid infiltration into infected tissue.",
        "contraindications_ja": "血管内注入は禁止（注入前に吸引確認）。種ごとのmg/kg上限を超えない。感染組織への浸潤は避ける。",
        "drug_interactions": [
            {
                "drug": "bupivacaine",
                "effect": "Additive local-anaesthetic systemic toxicity if combined — count total mg/kg across agents",
                "effect_ja": "併用時は局所麻酔薬全身毒性が相加的—薬剤横断で総mg/kgを計算する",
            }
        ],
    },
    {
        "id": "phenoxyethanol",
        "name": "2-Phenoxyethanol",
        "name_ja": "2-フェノキシエタノール",
        "category": "anesthetics",
        "mechanism": (
            "Aromatic-alcohol immersion anaesthetic for fish. Absorbed across the "
            "gills to depress the CNS, giving rapid induction and recovery. Also "
            "bactericidal/fungicidal. An alternative to MS-222 where buffering of "
            "tricaine is impractical."
        ),
        "mechanism_ja": (
            "魚類用の芳香族アルコール浸漬麻酔薬。鰓から吸収され中枢神経を抑制し、速やかな"
            "導入・覚醒をもたらす。殺菌・殺真菌作用もある。トリカインの緩衝が困難な場面での"
            "MS-222の代替。"
        ),
        "species_info": {
            "fish": {
                "safe": True,
                "dosage": "0.1-0.5 mL/L (≈100-500 mg/L) immersion; sedation at low end, surgical anaesthesia ~0.3-0.5 mL/L. Induction 2-3 min.",
                "dosage_ja": "0.1-0.5 mL/L（≈100-500 mg/L）浸漬。低濃度で鎮静、外科麻酔は約0.3-0.5 mL/L。導入2-3分。",
                "notes": "Oily liquid — pre-dissolve/emulsify in a small volume of water before adding to the bath. Narrow safety margin: monitor opercular (gill) rate continuously and have fresh recovery water ready. Not for food fish (no established withdrawal).",
                "notes_ja": "油性液体—少量の水に予め溶解・乳化してから薬浴に加える。安全域が狭く、鰓蓋運動を連続監視し覚醒用の新鮮水を準備。食用魚には不可（休薬期間未設定）。",
            },
        },
        "side_effects": "Respiratory depression and death if overdosed or exposure prolonged; gill irritation; delayed recovery in cold water.",
        "side_effects_ja": "過量・曝露延長で呼吸抑制・死亡、鰓刺激、低水温での覚醒遅延。",
        "contraindications": "Food fish (no established withdrawal period). Narrow margin — do not leave fish unmonitored in the bath. Ensure well-oxygenated recovery water.",
        "contraindications_ja": "食用魚（休薬期間未設定）。安全域が狭く、薬浴中の魚を無監視にしない。十分に酸素化した覚醒水を確保。",
        "drug_interactions": [],
    },
    {
        "id": "yohimbine",
        "name": "Yohimbine (Yobine)",
        "name_ja": "ヨヒンビン（ヨビン）",
        "category": "sedatives",
        "mechanism": (
            "Alpha-2 adrenergic antagonist used to reverse xylazine (and other "
            "alpha-2 agonist) sedation, and as an antidote for amitraz toxicosis. "
            "Atipamezole is now the more selective reversal agent, but yohimbine "
            "remains widely used, particularly for xylazine in large animals and "
            "wildlife."
        ),
        "mechanism_ja": (
            "α2アドレナリン拮抗薬。キシラジン（および他のα2作動薬）鎮静の拮抗、"
            "アミトラズ中毒の解毒に用いる。より選択的な拮抗薬はアティパメゾールに移行"
            "したが、特に大動物・野生動物のキシラジン拮抗でヨヒンビンは広く使われている。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.11 mg/kg IV slowly (xylazine reversal / amitraz toxicosis)",
                "dosage_ja": "0.11 mg/kg 緩徐に静注（キシラジン拮抗/アミトラズ中毒）",
                "notes": "Give slowly IV — rapid injection causes excitement, tremors, and transient hypertension. Effect may be shorter than the alpha-2 agonist, so re-sedation is possible.",
                "notes_ja": "緩徐に静注—急速投与で興奮・振戦・一過性高血圧。作用がα2作動薬より短く再鎮静が起こりうる。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.5 mg/kg IV slowly",
                "dosage_ja": "0.5 mg/kg 緩徐に静注",
                "notes": "Xylazine reversal. Monitor for re-sedation.",
                "notes_ja": "キシラジン拮抗。再鎮静に注意。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.075-0.12 mg/kg IV slowly (xylazine/detomidine reversal)",
                "dosage_ja": "0.075-0.12 mg/kg 緩徐に静注（キシラジン/デトミジン拮抗）",
                "notes": "Slow IV to avoid CNS excitement. Used in large-animal and cervid work.",
                "notes_ja": "中枢興奮回避のため緩徐に静注。大動物・シカ類で使用。",
            },
        },
        "side_effects": "Excitement, muscle tremors, transient hypertension then hypotension, tachycardia, salivation, seizures on rapid IV injection.",
        "side_effects_ja": "興奮、筋振戦、一過性高血圧に続く低血圧、頻脈、流涎、急速静注時の痙攣。",
        "contraindications": "Rapid IV injection; seizure disorders; use caution with cardiovascular disease. Effect may wane before the agonist, allowing re-sedation.",
        "contraindications_ja": "急速静注、痙攣性疾患は禁忌/慎重。心血管疾患では注意。作用が作動薬より先に消退し再鎮静を許すことがある。",
        "drug_interactions": [
            {
                "drug": "xylazine",
                "effect": "Antagonises sedation/analgesia — classic reversal pairing",
                "effect_ja": "鎮静・鎮痛を拮抗—古典的な拮抗の組み合わせ",
            }
        ],
    },
]
