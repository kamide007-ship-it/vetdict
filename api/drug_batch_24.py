"""drug_batch_24.py - 獣医薬品辞書バッチ24

追加薬品: 皮膚科、抗真菌、呼吸器、消化器、腫瘍、エキゾチック専用薬。
600+薬品達成用バッチ。
"""

DRUGS_BATCH_24: list[dict] = [
    {
        "id": "hydrocodone_antitussive",
        "name": "Hydrocodone (Hycodan)",
        "name_ja": "ヒドロコドン",
        "category": "respiratory",
        "mechanism": "Opioid antitussive; suppresses cough reflex centrally",
        "mechanism_ja": "オピオイド鎮咳薬；中枢性に咳反射を抑制",
        "species_info": {
            "dog": {"dose": "0.22 mg/kg PO q6-12h", "notes": "For intractable non-productive cough (collapsing trachea, chronic bronchitis)", "notes_ja": "難治性非生産性咳嗽に（気管虚脱、慢性気管支炎）"}
        },
        "side_effects": "Sedation, constipation, respiratory depression",
        "side_effects_ja": "鎮静、便秘、呼吸抑制",
        "contraindications": "Head trauma, productive cough, hypothyroidism",
        "contraindications_ja": "頭部外傷、湿性咳嗽、甲状腺機能低下症",
        "drug_interactions": [
            {"drug": "CNS depressants", "effect": "Additive sedation", "severity": "major"},
            {"drug": "MAO inhibitors", "effect": "Serotonin syndrome risk", "severity": "major"}
        ]
    },
    {
        "id": "clenbuterol_equine",
        "name": "Clenbuterol (Ventipulmin)",
        "name_ja": "クレンブテロール（ベンチプルミン）",
        "category": "respiratory",
        "mechanism": "Beta-2 adrenergic agonist; bronchodilator for horses",
        "mechanism_ja": "β2アドレナリン受容体作動薬；馬用気管支拡張薬",
        "species_info": {
            "horse": {"dose": "0.8 μg/kg PO q12h; may increase to 3.2 μg/kg", "notes": "FDA-approved for RAO in horses; 21-day withdrawal for food animals", "notes_ja": "馬のRAOでFDA承認；食用動物では21日の休薬期間"}
        },
        "side_effects": "Sweating, tachycardia, muscle tremors, restlessness",
        "side_effects_ja": "発汗、頻脈、筋振戦、不穏",
        "contraindications": "Severe cardiac disease, last trimester of pregnancy",
        "contraindications_ja": "重度の心疾患、妊娠末期",
        "drug_interactions": [
            {"drug": "Beta-blockers", "effect": "Antagonizes bronchodilatory effect", "severity": "major"},
            {"drug": "Halothane", "effect": "Cardiac sensitization risk", "severity": "major"}
        ]
    },
    {
        "id": "fluticasone_inhaler",
        "name": "Fluticasone (Flovent HFA)",
        "name_ja": "フルチカゾン（フローベントHFA）",
        "category": "respiratory",
        "mechanism": "Inhaled corticosteroid; reduces airway inflammation with minimal systemic effects",
        "mechanism_ja": "吸入コルチコステロイド；全身作用を最小限に気道炎症を軽減",
        "species_info": {
            "cat": {"dose": "44-220 μg/puff via AeroKat spacer q12h", "notes": "Gold standard for feline asthma maintenance; AeroKat spacer required", "notes_ja": "猫喘息の維持療法のゴールドスタンダード；AeroKatスペーサー必須"},
            "dog": {"dose": "110-220 μg via spacer q12h", "notes": "For chronic bronchitis/eosinophilic bronchopneumopathy", "notes_ja": "慢性気管支炎/好酸球性気管支肺症に"},
            "horse": {"dose": "2000-3000 μg via equine spacer q12h", "notes": "For RAO maintenance; equine-specific spacer (Equine Haler)", "notes_ja": "RAO維持療法に；馬用スペーサー（エクインヘイラー）使用"}
        },
        "side_effects": "Oral candidiasis (rare), adrenal suppression at high doses",
        "side_effects_ja": "口腔カンジダ症（稀）、高用量で副腎抑制",
        "contraindications": "Active respiratory infection (relative)",
        "contraindications_ja": "活動性呼吸器感染（相対的禁忌）",
        "drug_interactions": [
            {"drug": "Ketoconazole", "effect": "Increases fluticasone systemic exposure via CYP3A4 inhibition", "severity": "moderate"}
        ]
    },
    {
        "id": "griseofulvin_oral",
        "name": "Griseofulvin",
        "name_ja": "グリセオフルビン",
        "category": "antifungals",
        "mechanism": "Disrupts fungal mitotic spindle; inhibits dermatophyte cell division",
        "mechanism_ja": "真菌の有糸分裂紡錘体を阻害；皮膚糸状菌の細胞分裂を抑制",
        "species_info": {
            "dog": {"dose": "25-50 mg/kg PO q12-24h with fatty meal", "notes": "For dermatophytosis; give with fatty food for absorption", "notes_ja": "皮膚糸状菌症に；脂肪食と同時投与で吸収促進"},
            "cat": {"dose": "25-50 mg/kg PO q12-24h with food", "notes": "6-8 week course typical; monitor CBC", "notes_ja": "通常6-8週間投与；CBC モニタリング"},
            "horse": {"dose": "10 mg/kg PO q24h", "notes": "For equine dermatophytosis (Trichophyton/Microsporum)", "notes_ja": "馬の皮膚糸状菌症に"}
        },
        "side_effects": "GI upset, bone marrow suppression (cats), teratogenic, hepatotoxicity",
        "side_effects_ja": "消化器症状、骨髄抑制（猫）、催奇形性、肝毒性",
        "contraindications": "Pregnancy (teratogenic), FIV+ cats, hepatic disease",
        "contraindications_ja": "妊娠（催奇形性）、FIV陽性猫、肝疾患",
        "drug_interactions": [
            {"drug": "Phenobarbital", "effect": "Reduced griseofulvin levels", "severity": "moderate"},
            {"drug": "Warfarin", "effect": "Decreased anticoagulant effect", "severity": "moderate"}
        ]
    },
    {
        "id": "lufenuron_oral",
        "name": "Lufenuron (Program)",
        "name_ja": "ルフェヌロン（プログラム）",
        "category": "antiparasitics",
        "mechanism": "Chitin synthesis inhibitor; prevents flea egg development",
        "mechanism_ja": "キチン合成阻害薬；ノミ卵の発育を阻止",
        "species_info": {
            "dog": {"dose": "10 mg/kg PO q30 days with food", "notes": "Insect growth regulator; does not kill adult fleas—combine with adulticide", "notes_ja": "昆虫成長調節剤；成虫は殺さない—殺成虫薬と併用"},
            "cat": {"dose": "30 mg/kg PO q30 days or 10 mg/kg SC q6mo", "notes": "Injectable form available for cats; also studied for dermatophytosis", "notes_ja": "猫用注射製剤あり；皮膚糸状菌症への研究もあり"}
        },
        "side_effects": "Very safe; rare GI upset",
        "side_effects_ja": "非常に安全；稀に消化器症状",
        "contraindications": "None significant",
        "contraindications_ja": "特に重大な禁忌なし",
        "drug_interactions": []
    },
    {
        "id": "nitenpyram_oral",
        "name": "Nitenpyram (Capstar)",
        "name_ja": "ニテンピラム（キャプスター）",
        "category": "antiparasitics",
        "mechanism": "Neonicotinoid; blocks insect nicotinic acetylcholine receptors; rapid flea kill",
        "mechanism_ja": "ネオニコチノイド系；昆虫のニコチン性アセチルコリン受容体を遮断；速効性ノミ駆除",
        "species_info": {
            "dog": {"dose": "1 mg/kg PO as needed (single dose)", "notes": "Kills adult fleas within 30 min; no residual—use with monthly preventive", "notes_ja": "30分以内に成虫を駆除；残効性なし—月次予防薬と併用"},
            "cat": {"dose": "1 mg/kg PO as needed (single dose)", "notes": "Safe from 4 weeks of age and 0.9 kg body weight", "notes_ja": "4週齢・体重0.9kgから安全"}
        },
        "side_effects": "Transient hyperactivity/scratching (dying fleas), rare GI upset",
        "side_effects_ja": "一過性の多動/掻痒（瀕死のノミ反応）、稀に消化器症状",
        "contraindications": "Under 4 weeks of age, under 0.9 kg",
        "contraindications_ja": "4週齢未満、体重0.9kg未満",
        "drug_interactions": []
    },
    {
        "id": "lotilaner_oral",
        "name": "Lotilaner (Credelio)",
        "name_ja": "ロチラネル（クレデリオ）",
        "category": "antiparasitics",
        "mechanism": "Isoxazoline; inhibits GABA and glutamate-gated chloride channels in arthropods",
        "mechanism_ja": "イソオキサゾリン系；節足動物のGABA/グルタミン酸依存性塩素チャネルを阻害",
        "species_info": {
            "dog": {"dose": "20 mg/kg PO q30 days with food", "notes": "Kills fleas and ticks; chewable tablet", "notes_ja": "ノミ・ダニ駆除；チュアブル錠"},
            "cat": {"dose": "6 mg/kg PO q30 days with food", "notes": "Feline formulation available; from 8 weeks and 0.5 kg", "notes_ja": "猫用製剤あり；8週齢・0.5kgから"}
        },
        "side_effects": "Vomiting, diarrhea, lethargy (uncommon)",
        "side_effects_ja": "嘔吐、下痢、嗜眠（稀）",
        "contraindications": "Seizure history (class caution for isoxazolines), under 8 weeks",
        "contraindications_ja": "痙攣歴（イソオキサゾリン系の注意）、8週齢未満",
        "drug_interactions": []
    },
    {
        "id": "sarolaner_oral",
        "name": "Sarolaner (Simparica)",
        "name_ja": "サロラネル（シンパリカ）",
        "category": "antiparasitics",
        "mechanism": "Isoxazoline; GABA/glutamate-gated chloride channel inhibitor in ectoparasites",
        "mechanism_ja": "イソオキサゾリン系；外部寄生虫のGABA/グルタミン酸塩素チャネル阻害",
        "species_info": {
            "dog": {"dose": "2 mg/kg PO q30 days", "notes": "Kills fleas, ticks, and Sarcoptes/Demodex mites", "notes_ja": "ノミ、ダニ、ヒゼンダニ/ニキビダニを駆除"}
        },
        "side_effects": "Vomiting, diarrhea, lethargy, tremors (rare)",
        "side_effects_ja": "嘔吐、下痢、嗜眠、振戦（稀）",
        "contraindications": "Seizure history (isoxazoline class caution), under 6 months",
        "contraindications_ja": "痙攣歴（イソオキサゾリン系注意）、6ヶ月齢未満",
        "drug_interactions": []
    },
    {
        "id": "emodepside_topical",
        "name": "Emodepside (Profender component)",
        "name_ja": "エモデプシド（プロフェンダー成分）",
        "category": "antiparasitics",
        "mechanism": "Cyclooctadepsipeptide; stimulates latrophilin receptors causing parasite paralysis",
        "mechanism_ja": "環状オクタデプシペプチド；ラトロフィリン受容体を刺激し寄生虫を麻痺",
        "species_info": {
            "cat": {"dose": "3 mg/kg topical (spot-on with praziquantel)", "notes": "Broad-spectrum dewormer; roundworms, hookworms, tapeworms", "notes_ja": "広域駆虫薬；回虫、鉤虫、条虫"},
            "ferret": {"dose": "Off-label topical at cat dose", "notes": "Used for roundworm and hookworm in ferrets", "notes_ja": "フェレットの回虫・鉤虫にオフラベル使用"}
        },
        "side_effects": "Transient salivation if licked, hair loss at application site",
        "side_effects_ja": "舐めた場合の一過性流涎、塗布部位の脱毛",
        "contraindications": "Kittens under 8 weeks or under 0.5 kg",
        "contraindications_ja": "8週齢未満または0.5kg未満の子猫",
        "drug_interactions": []
    },
    {
        "id": "maropitant_injectable_exotic",
        "name": "Maropitant (Cerenia) - Exotic Species",
        "name_ja": "マロピタント（セレニア）エキゾチック種用",
        "category": "antiemetics",
        "mechanism": "NK1 receptor antagonist; antiemetic with visceral analgesic properties",
        "mechanism_ja": "NK1受容体拮抗薬；制吐作用と内臓鎮痛特性",
        "species_info": {
            "rabbit": {"dose": "2 mg/kg SC q24h", "notes": "Anti-nausea for GI stasis; visceral analgesia", "notes_ja": "消化管うっ滞の制吐に；内臓鎮痛作用"},
            "ferret": {"dose": "1 mg/kg SC/PO q24h", "notes": "For nausea associated with GI disease or chemotherapy", "notes_ja": "消化管疾患または化学療法に伴う悪心に"},
            "guinea_pig": {"dose": "2 mg/kg SC q24h", "notes": "Limited data; extrapolated from rabbit studies", "notes_ja": "データ限定的；ウサギの研究から外挿"},
            "bird": {"dose": "2 mg/kg IM q24h", "notes": "For avian nausea/crop stasis", "notes_ja": "鳥の悪心/素嚢うっ滞に"},
            "hedgehog": {"dose": "1-2 mg/kg SC q24h", "notes": "For nausea associated with GI disease", "notes_ja": "消化管疾患に伴う悪心に"}
        },
        "side_effects": "Pain at SC injection site, transient lethargy",
        "side_effects_ja": "SC注射部位の疼痛、一過性の嗜眠",
        "contraindications": "GI obstruction (mask symptoms), under 16 weeks (dogs/cats)",
        "contraindications_ja": "消化管閉塞（症状をマスク）、16週齢未満（犬猫）",
        "drug_interactions": [
            {"drug": "Other highly protein-bound drugs", "effect": "Potential displacement", "severity": "minor"}
        ]
    },
    {
        "id": "cisapride_exotic",
        "name": "Cisapride (Exotic Species)",
        "name_ja": "シサプリド（エキゾチック種用）",
        "category": "gastrointestinal",
        "mechanism": "5-HT4 receptor agonist; promotes GI motility via acetylcholine release",
        "mechanism_ja": "5-HT4受容体作動薬；アセチルコリン放出を介して消化管運動を促進",
        "species_info": {
            "rabbit": {"dose": "0.5 mg/kg PO q8-12h", "notes": "Essential for GI stasis treatment; combine with metoclopramide", "notes_ja": "消化管うっ滞治療に不可欠；メトクロプラミドと併用"},
            "guinea_pig": {"dose": "0.5 mg/kg PO q8-12h", "notes": "For GI stasis and post-anesthetic ileus", "notes_ja": "消化管うっ滞および麻酔後イレウスに"},
            "chinchilla": {"dose": "0.5 mg/kg PO q8-12h", "notes": "For GI stasis; combine with syringe feeding", "notes_ja": "消化管うっ滞に；シリンジ給餌と併用"},
            "hedgehog": {"dose": "0.25-0.5 mg/kg PO q12h", "notes": "For GI motility disorders", "notes_ja": "消化管運動障害に"},
            "reptile": {"dose": "0.5-2 mg/kg PO q24-48h", "notes": "For post-brumation anorexia/ileus", "notes_ja": "冬眠後食欲不振/イレウスに"},
            "tortoise": {"dose": "0.5-1 mg/kg PO q24-48h", "notes": "For post-hibernation GI recovery", "notes_ja": "冬眠後消化管回復に"}
        },
        "side_effects": "Diarrhea, abdominal cramping",
        "side_effects_ja": "下痢、腹部痙攣",
        "contraindications": "GI obstruction, GI perforation, concurrent QT-prolonging drugs",
        "contraindications_ja": "消化管閉塞、消化管穿孔、QT延長薬併用",
        "drug_interactions": [
            {"drug": "Ketoconazole", "effect": "Increases cisapride levels; cardiac arrhythmia risk", "severity": "major"},
            {"drug": "Erythromycin", "effect": "QT prolongation risk", "severity": "major"}
        ]
    },
    {
        "id": "buprenorphine_exotic",
        "name": "Buprenorphine (Exotic Species)",
        "name_ja": "ブプレノルフィン（エキゾチック種用）",
        "category": "analgesic",
        "mechanism": "Partial mu-opioid agonist; provides analgesia without full respiratory depression",
        "mechanism_ja": "部分的μオピオイド作動薬；完全な呼吸抑制なく鎮痛を提供",
        "species_info": {
            "rabbit": {"dose": "0.02-0.05 mg/kg SC/IV q6-12h; OTM 0.1-0.2 mg/kg q8h", "notes": "OTM (oral transmucosal) route effective in rabbits", "notes_ja": "OTM（口腔粘膜経由）投与がウサギで有効"},
            "guinea_pig": {"dose": "0.05 mg/kg SC q8-12h", "notes": "Short duration in guinea pigs; frequent dosing needed", "notes_ja": "モルモットでは持続が短い；頻回投与が必要"},
            "hamster": {"dose": "0.05-0.1 mg/kg SC q8-12h", "notes": "Primary analgesic for hamsters", "notes_ja": "ハムスターの主要鎮痛薬"},
            "ferret": {"dose": "0.01-0.03 mg/kg SC/IM q8-12h", "notes": "Good for post-surgical pain in ferrets", "notes_ja": "フェレットの術後疼痛に良好"},
            "hedgehog": {"dose": "0.01-0.05 mg/kg SC q8-12h", "notes": "For post-surgical pain, trauma", "notes_ja": "術後疼痛、外傷に"},
            "bird": {"dose": "0.1-0.5 mg/kg IM q8-12h", "notes": "Variable efficacy across avian species", "notes_ja": "鳥種間で有効性にばらつき"},
            "reptile": {"dose": "0.02-0.1 mg/kg IM q24h", "notes": "Thermal-dependent metabolism; prolonged action", "notes_ja": "温度依存性代謝；作用が延長"}
        },
        "side_effects": "Mild sedation, respiratory depression (high doses), hypothermia (small species)",
        "side_effects_ja": "軽度鎮静、呼吸抑制（高用量）、低体温（小型種）",
        "contraindications": "Head trauma, severe respiratory compromise",
        "contraindications_ja": "頭部外傷、重度の呼吸不全",
        "drug_interactions": [
            {"drug": "Full mu-agonists (morphine)", "effect": "May reduce efficacy of full agonist", "severity": "moderate"},
            {"drug": "CNS depressants", "effect": "Additive sedation", "severity": "moderate"}
        ]
    },
    {
        "id": "piroxicam_transitional_cell",
        "name": "Piroxicam (TCC protocol)",
        "name_ja": "ピロキシカム（移行上皮癌プロトコル）",
        "category": "antineoplastic",
        "mechanism": "Non-selective COX inhibitor with antineoplastic properties; inhibits tumor angiogenesis",
        "mechanism_ja": "抗腫瘍特性を持つ非選択的COX阻害薬；腫瘍血管新生を阻害",
        "species_info": {
            "dog": {"dose": "0.3 mg/kg PO q24h", "notes": "First-line for canine TCC/bladder carcinoma; combine with misoprostol for GI protection", "notes_ja": "犬の移行上皮癌/膀胱癌の第一選択；GI保護にミソプロストールと併用"}
        },
        "side_effects": "GI ulceration (high risk), renal papillary necrosis, bleeding",
        "side_effects_ja": "消化管潰瘍（高リスク）、腎乳頭壊死、出血",
        "contraindications": "Renal disease, GI ulceration, concurrent corticosteroids or other NSAIDs",
        "contraindications_ja": "腎疾患、消化管潰瘍、コルチコステロイドまたは他のNSAIDsとの併用",
        "drug_interactions": [
            {"drug": "Other NSAIDs", "effect": "Dramatically increased GI ulceration risk", "severity": "major"},
            {"drug": "Corticosteroids", "effect": "Severely increased GI toxicity", "severity": "major"},
            {"drug": "ACE inhibitors", "effect": "Reduced antihypertensive effect", "severity": "moderate"}
        ]
    },
    {
        "id": "toceranib_phosphate",
        "name": "Toceranib Phosphate (Palladia)",
        "name_ja": "トセラニブリン酸塩（パラディア）",
        "category": "antineoplastic",
        "mechanism": "Multi-targeted receptor tyrosine kinase inhibitor (VEGFR, PDGFR, Kit, Flt-3)",
        "mechanism_ja": "多標的受容体チロシンキナーゼ阻害薬（VEGFR, PDGFR, Kit, Flt-3）",
        "species_info": {
            "dog": {"dose": "2.75 mg/kg PO q48h (MWF schedule common)", "notes": "FDA-approved for canine MCT; also used for anal sac adenocarcinoma, thyroid carcinoma", "notes_ja": "犬の肥満細胞腫でFDA承認；肛門嚢腺癌、甲状腺癌にも使用"},
            "cat": {"dose": "2.5 mg/kg PO q48h", "notes": "Off-label for feline oral SCC, intestinal lymphoma; monitor closely", "notes_ja": "猫の口腔扁平上皮癌、腸管リンパ腫にオフラベル使用；厳重なモニタリング"}
        },
        "side_effects": "GI toxicity (diarrhea, anorexia), neutropenia, proteinuria, hypertension, lameness",
        "side_effects_ja": "消化器毒性（下痢、食欲不振）、好中球減少、蛋白尿、高血圧、跛行",
        "contraindications": "Concurrent NSAIDs (GI risk), severe hepatic/renal disease",
        "contraindications_ja": "NSAIDs併用（GIリスク）、重度の肝腎疾患",
        "drug_interactions": [
            {"drug": "NSAIDs", "effect": "Dramatically increased GI toxicity risk", "severity": "major"},
            {"drug": "ACE inhibitors", "effect": "Additive hypotension; but may help proteinuria", "severity": "moderate"}
        ]
    },
    {
        "id": "mitotane_oral",
        "name": "Mitotane (Lysodren)",
        "name_ja": "ミトタン（リソドレン）",
        "category": "endocrine",
        "mechanism": "Adrenocorticolytic agent; selectively destroys zona fasciculata/reticularis of adrenal cortex",
        "mechanism_ja": "副腎皮質溶解薬；副腎皮質の束状帯/網状帯を選択的に破壊",
        "species_info": {
            "dog": {"dose": "Loading: 25-50 mg/kg/day PO divided × 7-14 days; Maintenance: 25-50 mg/kg/week PO", "notes": "For canine pituitary-dependent hyperadrenocorticism; monitor ACTH stim test", "notes_ja": "犬の下垂体性副腎皮質機能亢進症に；ACTH刺激試験でモニタリング"}
        },
        "side_effects": "Anorexia, vomiting, diarrhea, lethargy, hypoadrenocorticism (iatrogenic Addison's)",
        "side_effects_ja": "食欲不振、嘔吐、下痢、嗜眠、医原性副腎皮質機能低下症（アジソン病）",
        "contraindications": "Concurrent illness, hepatic disease, pregnancy",
        "contraindications_ja": "併存疾患、肝疾患、妊娠",
        "drug_interactions": [
            {"drug": "Phenobarbital", "effect": "Increases mitotane metabolism (may need higher dose)", "severity": "moderate"},
            {"drug": "Insulin", "effect": "Cortisol changes affect insulin requirements", "severity": "moderate"},
            {"drug": "Spironolactone", "effect": "May interfere with mitotane action", "severity": "moderate"}
        ]
    },
    {
        "id": "methocarbamol_exotic",
        "name": "Methocarbamol (Exotic/Equine)",
        "name_ja": "メトカルバモール（エキゾチック/馬用）",
        "category": "muscle_relaxants",
        "mechanism": "Centrally-acting muscle relaxant; reduces skeletal muscle spasm via CNS depression",
        "mechanism_ja": "中枢性筋弛緩薬；CNS抑制を介して骨格筋痙攣を軽減",
        "species_info": {
            "horse": {"dose": "5-25 mg/kg IV slow; may repeat q6-8h", "notes": "For exertional rhabdomyolysis (tying up); also tetanus adjunct", "notes_ja": "運動性横紋筋融解症（タイイングアップ）に；破傷風の補助にも"},
            "rabbit": {"dose": "Not commonly used", "notes": "Limited data in rabbits", "notes_ja": "ウサギでのデータ限定的"},
            "bird": {"dose": "Not recommended", "notes": "Insufficient safety data in avian species", "notes_ja": "鳥類での安全性データ不足"}
        },
        "side_effects": "Sedation, salivation, weakness, brown discoloration of urine",
        "side_effects_ja": "鎮静、流涎、脱力、尿の褐色変色",
        "contraindications": "Renal impairment (vehicle concerns), seizure disorders",
        "contraindications_ja": "腎機能障害（溶媒に関する懸念）、痙攣性疾患",
        "drug_interactions": [
            {"drug": "CNS depressants", "effect": "Additive sedation", "severity": "moderate"}
        ]
    },
]
