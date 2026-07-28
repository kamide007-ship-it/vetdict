"""Drug batch 16: Additional antibiotics, antifungals, antiparasitics & emergency drugs (24 drugs)."""

DRUGS_BATCH_16: list[dict] = [
    {
        "id": "pradofloxacin_oral",
        "name": "Pradofloxacin (Veraflox Oral)",
        "name_ja": "プラドフロキサシン（ベラフロックス経口）",
        "category": "antibiotics",
        "mechanism": "Third-generation veterinary fluoroquinolone; dual targeting of DNA gyrase and topoisomerase IV with potent anaerobic coverage. Uniquely effective against Bacteroides spp.",
        "mechanism_ja": "第三世代獣医用フルオロキノロン；DNAジャイレースとトポイソメラーゼIVの二重標的と強力な嫌気性菌カバレッジ。Bacteroides spp.に独自の効果",
        "species_info": {
            "dog": {
                "dose": "3-5 mg/kg PO q24h × 7-28d",
                "notes": "Skin wounds, deep pyoderma, abscesses with anaerobic component; FDA-approved for dogs",
                "notes_ja": "皮膚創傷、深在性膿皮症、嫌気性菌を含む膿瘍；犬でFDA承認",
            },
            "cat": {
                "dose": "5-10 mg/kg PO q24h × 7-14d (Veraflox oral suspension)",
                "notes": "Skin infections, wound infections; palatable oral suspension for cats. EMA/FDA approved",
                "notes_ja": "皮膚感染症、創傷感染；猫用経口懸濁液。EMA/FDA承認",
            },
        },
        "side_effects": [
            "GI upset",
            "Cartilage damage (growing animals)",
            "CNS stimulation",
            "Retinal degeneration (cats, high dose)",
        ],
        "side_effects_ja": ["消化器障害", "軟骨障害（成長期動物）", "CNS刺激", "網膜変性（猫、高用量）"],
        "contraindications": "Growing animals <8 months (large breeds <18 months), epilepsy, concurrent NSAIDs (seizure risk)",
        "contraindications_ja": "8ヶ月未満の成長期動物（大型犬18ヶ月未満）、てんかん、NSAID併用（痙攣リスク）",
        "drug_interactions": [
            {
                "drug": "NSAIDs",
                "severity": "moderate",
                "description": "Increased seizure risk through GABA antagonism",
                "description_ja": "GABA拮抗による痙攣リスク増加",
            },
            {
                "drug": "Sucralfate/antacids",
                "severity": "moderate",
                "description": "Chelation reduces FQ absorption; separate by 2h",
                "description_ja": "キレート化によりFQ吸収低下；2時間間隔",
            },
        ],
    },
    {
        "id": "tulathromycin",
        "name": "Tulathromycin (Draxxin)",
        "name_ja": "ツラスロマイシン（ドラキシン）",
        "category": "antibiotics",
        "mechanism": "Triamilide (novel macrolide subclass); concentrates in lung tissue at 60x plasma levels. Single injection provides 7-10 days therapeutic concentration due to extensive tissue distribution",
        "mechanism_ja": "トリアミライド（新規マクロライドサブクラス）；肺組織に血漿の60倍濃度で蓄積。広範な組織分布により単回注射で7-10日間の治療濃度を維持",
        "species_info": {
            "horse": {
                "dose": "2.5 mg/kg IM once (cattle dose; off-label equine)",
                "notes": "Rhodococcus equi pneumonia in foals (off-label); single injection convenience",
                "notes_ja": "子馬のロドコッカス肺炎（適応外）；単回注射の利便性",
            },
            "others": {
                "dose": "2.5 mg/kg SC/IM once (cattle/swine)",
                "notes": "BRD treatment/metaphylaxis; withdrawal periods apply for food animals",
                "notes_ja": "牛呼吸器病治療/メタフィラキシス；食用動物は休薬期間あり",
            },
        },
        "side_effects": ["Injection site reaction", "Transient pain", "Head pressing (rare, cattle)"],
        "side_effects_ja": ["注射部位反応", "一過性疼痛", "頭部圧迫行動（稀、牛）"],
        "contraindications": "Not approved for companion animals; caution in horses (fatal reactions reported)",
        "contraindications_ja": "コンパニオンアニマル未承認；馬では注意（致死的反応の報告あり）",
        "drug_interactions": [
            {
                "drug": "Other macrolides",
                "severity": "moderate",
                "description": "Do not combine macrolide classes",
                "description_ja": "マクロライド系の重複回避",
            }
        ],
    },
    {
        "id": "cefuroxime",
        "name": "Cefuroxime",
        "name_ja": "セフロキシム",
        "category": "antibiotics",
        "mechanism": "Second-generation cephalosporin; broader gram-negative coverage than first-gen while maintaining gram-positive activity. Beta-lactamase stable to most common enzymes",
        "mechanism_ja": "第二世代セファロスポリン；グラム陽性菌活性を維持しつつ第一世代より広いグラム陰性菌カバレッジ。大部分の一般的酵素に対しβ-ラクタマーゼ安定",
        "species_info": {
            "dog": {
                "dose": "10-25 mg/kg PO q8-12h; IV: 20-30 mg/kg q8h",
                "notes": "UTI, pneumonia, osteomyelitis; alternative to amoxicillin-clavulanate for resistant infections",
                "notes_ja": "UTI、肺炎、骨髄炎；耐性感染のアモキシシリン-クラブラン酸代替",
            },
            "cat": {
                "dose": "10-20 mg/kg PO q12h",
                "notes": "Respiratory infections, soft tissue infections",
                "notes_ja": "呼吸器感染症、軟部組織感染症",
            },
            "horse": {
                "dose": "20-30 mg/kg IV q8h",
                "notes": "Surgical prophylaxis, joint infections",
                "notes_ja": "手術予防、関節感染",
            },
            "rabbit": {
                "dose": "15-30 mg/kg PO/SC q12h",
                "notes": "Pasteurella, respiratory infections",
                "notes_ja": "パスツレラ、呼吸器感染",
            },
        },
        "side_effects": ["GI upset", "Allergic reaction", "Thrombophlebitis (IV)"],
        "side_effects_ja": ["消化器障害", "アレルギー反応", "血栓性静脈炎（IV）"],
        "contraindications": "Cephalosporin/penicillin allergy (10% cross-reactivity)",
        "contraindications_ja": "セファロスポリン/ペニシリンアレルギー（10%交差反応）",
        "drug_interactions": [
            {
                "drug": "Aminoglycosides",
                "severity": "moderate",
                "description": "Synergistic antibacterial but additive nephrotoxicity",
                "description_ja": "相乗的抗菌作用だが相加的腎毒性",
            },
            {
                "drug": "Probenecid",
                "severity": "mild",
                "description": "Delays cephalosporin excretion (higher levels)",
                "description_ja": "セファロスポリン排泄を遅延（高濃度）",
            },
        ],
    },
    {
        "id": "polymyxin_b_ophthalmic",
        "name": "Polymyxin B/Neomycin/Bacitracin Ophthalmic",
        "name_ja": "ポリミキシンB/ネオマイシン/バシトラシン眼軟膏",
        "category": "ophthalmology",
        "mechanism": "Triple antibiotic ophthalmic; combines membrane disruptor (polymyxin B), protein synthesis inhibitor (neomycin), and cell wall inhibitor (bacitracin) for broad-spectrum coverage",
        "mechanism_ja": "三重抗菌眼科用製剤；膜破壊薬（ポリミキシンB）、蛋白合成阻害薬（ネオマイシン）、細胞壁阻害薬（バシトラシン）の組合せで広域カバレッジ",
        "species_info": {
            "dog": {
                "dose": "Apply 1cm ribbon to affected eye q6-8h",
                "notes": "Bacterial conjunctivitis, corneal ulcer prophylaxis post-trauma; OTC availability",
                "notes_ja": "細菌性結膜炎、外傷後角膜潰瘍予防；OTCで入手可能",
            },
            "cat": {
                "dose": "Apply 0.5cm ribbon q6-8h",
                "notes": "Bacterial conjunctivitis adjunct; often combined with antiviral for herpes co-infection",
                "notes_ja": "細菌性結膜炎補助；ヘルペス混合感染に抗ウイルス薬併用が多い",
            },
            "horse": {
                "dose": "Apply q4-6h",
                "notes": "Corneal ulcer protection; inadequate for Pseudomonas (add fluoroquinolone)",
                "notes_ja": "角膜潰瘍保護；緑膿菌には不十分（フルオロキノロン追加）",
            },
            "rabbit": {
                "dose": "Apply q6-8h",
                "notes": "Conjunctivitis, dacryocystitis adjunct",
                "notes_ja": "結膜炎、涙嚢炎の補助",
            },
            "bird": {"dose": "Apply q8-12h", "notes": "Periorbital infections", "notes_ja": "眼窩周囲感染"},
        },
        "side_effects": [
            "Contact sensitization (neomycin)",
            "Corneal epithelial toxicity (prolonged use)",
            "Allergic conjunctivitis",
        ],
        "side_effects_ja": ["接触感作（ネオマイシン）", "角膜上皮毒性（長期使用）", "アレルギー性結膜炎"],
        "contraindications": "Aminoglycoside allergy, fungal/viral keratitis (without antifungal/antiviral)",
        "contraindications_ja": "アミノグリコシドアレルギー、真菌性/ウイルス性角膜炎（抗真菌/抗ウイルス薬なし）",
        "drug_interactions": [
            {
                "drug": "Topical corticosteroids",
                "severity": "mild",
                "description": "Common beneficial combination (e.g., neo-poly-dex); steroid masks infection signs",
                "description_ja": "一般的な有益組合せ（例：neo-poly-dex）；ステロイドが感染徴候をマスク",
            }
        ],
    },
    {
        "id": "posaconazole",
        "name": "Posaconazole",
        "name_ja": "ポサコナゾール",
        "category": "antifungals",
        "mechanism": "Extended-spectrum triazole antifungal; inhibits 14-alpha-demethylase (CYP51) with broader activity than itraconazole/fluconazole including Mucorales and resistant Aspergillus",
        "mechanism_ja": "拡張スペクトラムトリアゾール系抗真菌薬；イトラコナゾール/フルコナゾールより広い活性でムコール目や耐性アスペルギルスを含む14α-デメチラーゼ（CYP51）を阻害",
        "species_info": {
            "dog": {
                "dose": "5-10 mg/kg PO q12-24h (with fatty meal)",
                "notes": "Refractory aspergillosis, disseminated fungal infections; alternative when itraconazole fails",
                "notes_ja": "難治性アスペルギルス症、播種性真菌感染；イトラコナゾール無効時の代替",
            },
            "cat": {
                "dose": "5-10 mg/kg PO q12-24h",
                "notes": "Cryptococcosis, refractory dermatophytosis; better tolerated than itraconazole in some cats",
                "notes_ja": "クリプトコッカス症、難治性皮膚糸状菌症；一部の猫でイトラコナゾールより忍容性良好",
            },
            "horse": {
                "dose": "4-8 mg/kg PO q12-24h",
                "notes": "Guttural pouch mycosis, paranasal sinus aspergillosis",
                "notes_ja": "喉嚢真菌症、副鼻腔アスペルギルス症",
            },
            "bird": {
                "dose": "10-15 mg/kg PO q12h",
                "notes": "Avian aspergillosis (raptor, penguin); may be superior to itraconazole for pulmonary forms",
                "notes_ja": "鳥類アスペルギルス症（猛禽類・ペンギン）；肺型ではイトラコナゾールより優れる可能性",
            },
        },
        "side_effects": ["Hepatotoxicity", "GI upset", "QT prolongation", "Hypokalemia"],
        "side_effects_ja": ["肝毒性", "消化器障害", "QT延長", "低カリウム血症"],
        "contraindications": "Concurrent CYP3A4 substrates with narrow therapeutic index, severe hepatic disease, QT prolongation",
        "contraindications_ja": "治療域の狭いCYP3A4基質の併用、重度肝疾患、QT延長",
        "drug_interactions": [
            {
                "drug": "Cyclosporine",
                "severity": "major",
                "description": "Markedly increases cyclosporine levels; reduce dose 75%",
                "description_ja": "シクロスポリン濃度を著明に上昇；75%減量",
            },
            {
                "drug": "Rifampin",
                "severity": "major",
                "description": "Reduces posaconazole levels by 80%; contraindicated",
                "description_ja": "ポサコナゾール濃度を80%低下；禁忌",
            },
        ],
    },
    {
        "id": "micafungin",
        "name": "Micafungin",
        "name_ja": "ミカファンギン",
        "category": "antifungals",
        "mechanism": "Echinocandin antifungal; inhibits beta-1,3-D-glucan synthase disrupting fungal cell wall. Effective against Candida and Aspergillus. IV only formulation",
        "mechanism_ja": "エキノキャンディン系抗真菌薬；β-1,3-D-グルカン合成酵素を阻害し真菌細胞壁を破壊。カンジダとアスペルギルスに有効。注射専用製剤",
        "species_info": {
            "dog": {
                "dose": "1-4 mg/kg IV q24h",
                "notes": "Invasive candidiasis, refractory aspergillosis; very well tolerated IV",
                "notes_ja": "侵襲性カンジダ症、難治性アスペルギルス症；IV忍容性非常に良好",
            },
            "cat": {
                "dose": "1-3 mg/kg IV q24h",
                "notes": "Systemic candidiasis, concurrent immunosuppression",
                "notes_ja": "全身性カンジダ症、免疫抑制状態",
            },
            "bird": {
                "dose": "2-5 mg/kg IV q24h",
                "notes": "Avian aspergillosis rescue therapy when voriconazole/ampho-B fail",
                "notes_ja": "ボリコナゾール/アムホテリシンB無効時の鳥類アスペルギルス症レスキュー",
            },
        },
        "side_effects": ["Phlebitis", "Hepatotoxicity (rare)", "Hemolytic anemia (rare, high dose)"],
        "side_effects_ja": ["静脈炎", "肝毒性（稀）", "溶血性貧血（稀、高用量）"],
        "contraindications": "Known echinocandin hypersensitivity; not effective against Cryptococcus or Mucorales",
        "contraindications_ja": "エキノキャンディン過敏症既知；クリプトコッカスやムコール目には無効",
        "drug_interactions": [
            {
                "drug": "Cyclosporine",
                "severity": "mild",
                "description": "Slight increase in cyclosporine exposure (less than azoles)",
                "description_ja": "シクロスポリン曝露のわずかな増加（アゾール系より少ない）",
            },
            {
                "drug": "Amphotericin B",
                "severity": "mild",
                "description": "Potentially synergistic against Aspergillus (different targets)",
                "description_ja": "アスペルギルスに対し潜在的相乗効果（異なる標的）",
            },
        ],
    },
    {
        "id": "afoxolaner_milbemycin",
        "name": "Afoxolaner+Milbemycin (NexGard Spectra)",
        "name_ja": "アフォキソラネル+ミルベマイシン（ネクスガードスペクトラ）",
        "category": "antiparasitic",
        "mechanism": "Combination endectocide; afoxolaner (isoxazoline) kills fleas/ticks via GABA/GluCl inhibition + milbemycin oxime prevents heartworm and treats GI nematodes via glutamate-gated Cl channel potentiation",
        "mechanism_ja": "併用内外寄生虫駆除薬；アフォキソラネル（イソオキサゾリン）がGABA/GluCl阻害でノミ・ダニ駆除＋ミルベマイシンオキシムがグルタミン酸依存性Clチャネル増強でフィラリア予防・消化管線虫治療",
        "species_info": {
            "dog": {
                "dose": "2.5 mg/kg afoxolaner + 0.5 mg/kg milbemycin PO monthly",
                "notes": "All-in-one monthly: fleas, ticks, heartworm prevention, roundworm, hookworm; EMA/FDA approved",
                "notes_ja": "月1回オールインワン：ノミ・ダニ・フィラリア予防・回虫・鉤虫；EMA/FDA承認",
            }
        },
        "side_effects": ["Vomiting", "Diarrhea", "Lethargy", "Seizures (rare, predisposed)"],
        "side_effects_ja": ["嘔吐", "下痢", "嗜眠", "痙攣（稀、素因動物）"],
        "contraindications": "Seizure history (caution), <8 weeks/<2kg, cats (not approved), heartworm-positive dogs (test first)",
        "contraindications_ja": "痙攣既往（注意）、8週齢未満/2kg未満、猫（未承認）、フィラリア陽性犬（事前検査）",
        "drug_interactions": [
            {
                "drug": "P-glycoprotein inhibitors",
                "severity": "moderate",
                "description": "Increased milbemycin CNS levels in MDR1 dogs",
                "description_ja": "MDR1犬でミルベマイシンCNS濃度増加",
            }
        ],
    },
    {
        "id": "selamectin_sarolaner_combo",
        "name": "Selamectin+Sarolaner (Revolution Plus)",
        "name_ja": "セラメクチン+サロラネル（レボリューションプラス）",
        "category": "antiparasitic",
        "mechanism": "Topical combination for cats; selamectin (avermectin) prevents heartworm/ear mites/fleas + sarolaner (isoxazoline) adds tick kill and enhanced flea efficacy",
        "mechanism_ja": "猫用外用併用薬；セラメクチン（アベルメクチン）がフィラリア・耳ダニ・ノミ予防＋サロラネル（イソオキサゾリン）がダニ駆除と強化ノミ効果を追加",
        "species_info": {
            "cat": {
                "dose": "6 mg/kg selamectin + 1 mg/kg sarolaner topically monthly",
                "notes": "Comprehensive feline parasite prevention: fleas, ticks (Ixodes, Dermacentor), heartworm, ear mites, roundworms, hookworms; FDA approved",
                "notes_ja": "包括的猫寄生虫予防：ノミ・ダニ・フィラリア・耳ダニ・回虫・鉤虫；FDA承認",
            }
        },
        "side_effects": ["Hair loss at application site", "Lethargy", "Vomiting", "Seizures (very rare)"],
        "side_effects_ja": ["塗布部位の脱毛", "嗜眠", "嘔吐", "痙攣（非常に稀）"],
        "contraindications": "Kittens <8 weeks/<1.25 lb, sick/debilitated cats, dogs (not approved for dogs)",
        "contraindications_ja": "8週齢未満/0.56kg未満の子猫、病気/衰弱猫、犬（犬未承認）",
        "drug_interactions": [
            {
                "drug": "No significant interactions documented",
                "severity": "mild",
                "description": "Topical with minimal systemic absorption",
                "description_ja": "全身吸収最小限の外用薬",
            }
        ],
    },
    {
        "id": "imidacloprid_flumethrin",
        "name": "Imidacloprid+Flumethrin (Seresto)",
        "name_ja": "イミダクロプリド+フルメトリン（セレスト）",
        "category": "antiparasitic",
        "mechanism": "8-month slow-release collar; imidacloprid (neonicotinoid) kills fleas via nAChR agonism + flumethrin (pyrethroid) repels/kills ticks via sodium channel modulation. Released into lipid layer of skin/hair",
        "mechanism_ja": "8ヶ月徐放性カラー；イミダクロプリド（ネオニコチノイド）がnAChR作動でノミ駆除＋フルメトリン（ピレスロイド）がNaチャネル調節でダニ忌避・駆除。皮膚/被毛の脂質層に放出",
        "species_info": {
            "dog": {
                "dose": "Large collar (4.5g imidacloprid + 2.03g flumethrin) or small collar for <8kg dogs",
                "notes": "8-month flea/tick prevention; waterproof; also reduces Leishmania transmission via sandfly repellency",
                "notes_ja": "8ヶ月間ノミ・ダニ予防；防水；サシチョウバエ忌避によりリーシュマニア伝播も減少",
            },
            "cat": {
                "dose": "Cat collar (1.25g imidacloprid + 0.56g flumethrin)",
                "notes": "Cat-specific safety mechanism (breakaway); NO permethrin/flumethrin toxicity concern at collar dose",
                "notes_ja": "猫用安全機構（外れるバックル）；カラー用量ではペルメトリン/フルメトリン毒性の懸念なし",
            },
        },
        "side_effects": ["Local skin irritation", "Hair loss under collar", "Lethargy (first few days)"],
        "side_effects_ja": ["局所皮膚刺激", "カラー下の脱毛", "嗜眠（初期数日）"],
        "contraindications": "Puppies/kittens <7 weeks, sick/convalescent animals, known flea collar sensitivity",
        "contraindications_ja": "7週齢未満の子犬/子猫、病気/回復期動物、ノミ取りカラー過敏症既知",
        "drug_interactions": [
            {
                "drug": "Organophosphates",
                "severity": "moderate",
                "description": "Avoid combining with OP-based products",
                "description_ja": "有機リン系製品との併用回避",
            }
        ],
    },
    {
        "id": "milbemycin_lufenuron",
        "name": "Milbemycin+Lufenuron (Sentinel)",
        "name_ja": "ミルベマイシン+ルフェヌロン（センチネル）",
        "category": "antiparasitic",
        "mechanism": "Combination oral preventive; milbemycin oxime (macrocyclic lactone) prevents heartworm and treats GI nematodes + lufenuron (chitin synthesis inhibitor) prevents flea egg development",
        "mechanism_ja": "経口併用予防薬；ミルベマイシンオキシム（大環状ラクトン）がフィラリア予防・消化管線虫治療＋ルフェヌロン（キチン合成阻害薬）がノミ卵発生を阻害",
        "species_info": {
            "dog": {
                "dose": "0.5 mg/kg milbemycin + 10 mg/kg lufenuron PO monthly (with meal)",
                "notes": "Heartworm prevention + flea development control + deworming; does NOT kill adult fleas",
                "notes_ja": "フィラリア予防＋ノミ発生制御＋駆虫；成虫ノミは殺さない",
            },
            "cat": {
                "dose": "2 mg/kg milbemycin + 30 mg/kg lufenuron PO monthly",
                "notes": "Cat formulation (Sentinel for cats); prevents heartworm, controls flea populations",
                "notes_ja": "猫用製剤；フィラリア予防、ノミ個体群制御",
            },
        },
        "side_effects": ["Vomiting", "Diarrhea/soft stool", "Lethargy", "Hypersalivation"],
        "side_effects_ja": ["嘔吐", "下痢/軟便", "嗜眠", "流涎過多"],
        "contraindications": "Heartworm-positive (must test negative first), <4 weeks/<2lb",
        "contraindications_ja": "フィラリア陽性（事前に陰性確認必須）、4週齢未満/0.9kg未満",
        "drug_interactions": [
            {
                "drug": "P-glycoprotein inhibitors",
                "severity": "moderate",
                "description": "MDR1 mutant dogs may have increased milbemycin toxicity (standard doses usually safe)",
                "description_ja": "MDR1変異犬でミルベマイシン毒性増加の可能性（標準用量は通常安全）",
            }
        ],
    },
    {
        "id": "fluralaner_topical",
        "name": "Fluralaner Topical (Bravecto Spot-On)",
        "name_ja": "フルララネル外用（ブラベクトスポットオン）",
        "category": "antiparasitic",
        "mechanism": "Isoxazoline ectoparasiticide in topical formulation; inhibits arthropod GABA/GluCl channels. 12-week duration from single topical application for both dogs and cats",
        "mechanism_ja": "外用イソオキサゾリン系外部寄生虫駆除薬；節足動物GABA/GluClチャネルを阻害。犬猫とも単回外用で12週間持続",
        "species_info": {
            "dog": {
                "dose": "25-56 mg/kg topically q12 weeks",
                "notes": "12-week flea/tick prevention (longest duration); also treats Demodex, Sarcoptes",
                "notes_ja": "12週間ノミ・ダニ予防（最長持続期間）；ニキビダニ・疥癬ダニも治療",
            },
            "cat": {
                "dose": "40-94 mg/kg topically q12 weeks",
                "notes": "12-week duration for cats; treats Notoedres cati mange",
                "notes_ja": "猫用12週間持続；ネコショウセンコウヒゼンダニも治療",
            },
        },
        "side_effects": ["Vomiting", "Hair loss at site", "Diarrhea", "Lethargy", "Seizures (very rare)"],
        "side_effects_ja": ["嘔吐", "塗布部位脱毛", "下痢", "嗜眠", "痙攣（非常に稀）"],
        "contraindications": "Puppies/kittens <8 weeks/<2lb, seizure history (caution)",
        "contraindications_ja": "8週齢未満/0.9kg未満の子犬/子猫、痙攣既往（注意）",
        "drug_interactions": [
            {
                "drug": "Other isoxazolines",
                "severity": "moderate",
                "description": "Do not stack isoxazoline products",
                "description_ja": "イソオキサゾリン製品の重複回避",
            }
        ],
    },
    {
        "id": "doramectin",
        "name": "Doramectin",
        "name_ja": "ドラメクチン",
        "category": "antiparasitic",
        "mechanism": "Avermectin endectocide; potentiates GABA/GluCl channels in parasites. Long-acting IM formulation (2-3 weeks). Used in production animals and exotic species",
        "mechanism_ja": "アベルメクチン系内外寄生虫駆除薬；寄生虫のGABA/GluClチャネルを増強。長時間作用型IM製剤（2-3週間）。産業動物およびエキゾチック種で使用",
        "species_info": {
            "dog": {
                "dose": "0.2-0.6 mg/kg SC/PO q7-14d (Demodex protocol)",
                "notes": "Generalized demodicosis (off-label); AVOID in MDR1 breeds. Daily protocol also used",
                "notes_ja": "全身性ニキビダニ症（適応外）；MDR1犬種には禁忌。毎日投与プロトコルも使用",
            },
            "guinea_pig": {
                "dose": "0.2-0.4 mg/kg SC q7-14d",
                "notes": "Trixacarus caviae (sarcoptic mange); repeat 2-3 times",
                "notes_ja": "Trixacarus caviae（疥癬ダニ）；2-3回繰り返し",
            },
            "hedgehog": {
                "dose": "0.2-0.4 mg/kg SC q14d × 3",
                "notes": "Caparinia tripilis mites; preferred over ivermectin in some practitioners",
                "notes_ja": "Caparinia tripilusダニ；一部の臨床医ではイベルメクチンより推奨",
            },
            "bird": {
                "dose": "0.2 mg/kg IM once or topical",
                "notes": "Knemidocoptes (scaly face/leg mite)",
                "notes_ja": "疥癬ダニ（うろこ顔/脚ダニ）",
            },
            "reptile": {
                "dose": "0.2 mg/kg SC/IM, repeat in 14d",
                "notes": "Snake mites (Ophionyssus natricis); tortoises",
                "notes_ja": "ヘビダニ（Ophionyssus natricis）；リクガメ",
            },
        },
        "side_effects": ["CNS depression (MDR1)", "Ataxia", "Blindness (toxicity)", "Injection site reaction"],
        "side_effects_ja": ["CNS抑制（MDR1）", "運動失調", "失明（毒性）", "注射部位反応"],
        "contraindications": "MDR1 mutant breeds (Collie, Sheltie, Aussie), turtles/tortoises (some are sensitive), debilitated animals",
        "contraindications_ja": "MDR1変異犬種（コリー・シェルティー・オージー）、カメ（一部は感受性あり）、衰弱動物",
        "drug_interactions": [
            {
                "drug": "P-glycoprotein inhibitors (ketoconazole, spinosad)",
                "severity": "major",
                "description": "Increased avermectin CNS penetration; neurotoxicity risk",
                "description_ja": "アベルメクチンCNS移行増加；神経毒性リスク",
            }
        ],
    },
    {
        "id": "melarsomine",
        "name": "Melarsomine (Immiticide)",
        "name_ja": "メラルソミン（イミティサイド）",
        "category": "antiparasitic",
        "mechanism": "Organic arsenical adulticide; kills adult heartworms (Dirofilaria immitis) by disrupting metabolic pathways. Deep IM injection into epaxial lumbar muscles",
        "mechanism_ja": "有機ヒ素系成虫駆除薬；代謝経路を破壊し成虫フィラリア（犬糸状虫）を殺滅。腰部背軸筋への深部IM注射",
        "species_info": {
            "dog": {
                "dose": "Standard: 2.5 mg/kg deep IM × 1, then 30d rest, then 2.5 mg/kg × 2 (24h apart); AHS 3-injection protocol",
                "notes": "ONLY drug that kills adult heartworms; pre-treat with doxycycline + ivermectin × 60d. Strict exercise restriction critical",
                "notes_ja": "成虫フィラリアを殺す唯一の薬；ドキシサイクリン+イベルメクチン60日前処置。厳格な運動制限が重要",
            }
        },
        "side_effects": [
            "Injection site pain/swelling (common)",
            "Pulmonary thromboembolism (dying worms)",
            "Coughing",
            "Fever",
            "Hemoglobinuria",
        ],
        "side_effects_ja": ["注射部位痛/腫脹（高頻度）", "肺血栓塞栓症（死滅虫体）", "咳嗽", "発熱", "ヘモグロビン尿"],
        "contraindications": "Class IV heartworm (caval syndrome - surgical extraction needed), severe liver/kidney disease, cats (NEVER use in cats)",
        "contraindications_ja": "クラスIVフィラリア（大静脈症候群 - 外科的摘出が必要）、重度肝/腎疾患、猫（猫には絶対に使用しない）",
        "drug_interactions": [
            {
                "drug": "Ivermectin/Doxycycline",
                "severity": "mild",
                "description": "Part of standard pre-treatment protocol (slow-kill reduces emboli risk)",
                "description_ja": "標準前処置プロトコルの一部（スローキルで塞栓リスク低下）",
            }
        ],
    },
    {
        "id": "benazepril_heartworm",
        "name": "Benazepril (Heartworm-associated PH)",
        "name_ja": "ベナゼプリル（フィラリア関連肺高血圧症）",
        "category": "cardiovascular",
        "mechanism": "ACE inhibitor used specifically for heartworm-associated pulmonary hypertension and right-sided heart failure. Reduces pulmonary vascular resistance and improves RV function",
        "mechanism_ja": "フィラリア関連肺高血圧症と右心不全に特化して使用するACE阻害薬。肺血管抵抗を低下させ右心室機能を改善",
        "species_info": {
            "dog": {
                "dose": "0.5 mg/kg PO q12-24h",
                "notes": "Heartworm class III stabilization before melarsomine; reduces PH and RV afterload",
                "notes_ja": "メラルソミン前のフィラリアクラスIII安定化；肺高血圧と右心室後負荷を低下",
            }
        },
        "side_effects": ["Hypotension", "Azotemia", "Hyperkalemia"],
        "side_effects_ja": ["低血圧", "高窒素血症", "高カリウム血症"],
        "contraindications": "Dehydration, bilateral renal artery stenosis",
        "contraindications_ja": "脱水、両側腎動脈狭窄",
        "drug_interactions": [
            {
                "drug": "NSAIDs",
                "severity": "moderate",
                "description": "Reduced renal protection",
                "description_ja": "腎保護効果減弱",
            }
        ],
    },
    {
        "id": "ephedrine",
        "name": "Ephedrine",
        "name_ja": "エフェドリン",
        "category": "cardiovascular",
        "mechanism": "Mixed-acting sympathomimetic; directly and indirectly stimulates alpha and beta receptors. Increases blood pressure, heart rate, and bronchodilation. Also increases urethral sphincter tone",
        "mechanism_ja": "混合作用型交感神経刺激薬；直接的・間接的にα・β受容体を刺激。血圧・心拍数を上昇させ気管支拡張。尿道括約筋緊張も増加",
        "species_info": {
            "dog": {
                "dose": "Hypotension: 0.03-0.1 mg/kg IV bolus; Urethral incompetence: 1-4 mg/kg PO q8-12h",
                "notes": "Anesthetic hypotension (bolus), urethral sphincter incompetence (spayed females); tachyphylaxis develops",
                "notes_ja": "麻酔中低血圧（ボーラス）、尿道括約筋不全（避妊雌）；頻脈耐性が発現",
            },
            "cat": {
                "dose": "2-4 mg/cat PO q8-12h",
                "notes": "Urethral incompetence (less common in cats than dogs)",
                "notes_ja": "尿道括約筋不全（猫では犬より少ない）",
            },
            "horse": {
                "dose": "0.01-0.05 mg/kg IV",
                "notes": "Anesthetic hypotension bolus; short duration",
                "notes_ja": "麻酔中低血圧ボーラス；短時間作用",
            },
        },
        "side_effects": ["Tachycardia", "Hypertension", "Restlessness", "Urinary retention", "Tachyphylaxis"],
        "side_effects_ja": ["頻脈", "高血圧", "不穏", "尿閉", "頻脈耐性"],
        "contraindications": "Hypertension, tachyarrhythmias, closed-angle glaucoma, concurrent MAOIs",
        "contraindications_ja": "高血圧、頻脈性不整脈、閉塞隅角緑内障、MAOI併用",
        "drug_interactions": [
            {
                "drug": "MAO inhibitors",
                "severity": "major",
                "description": "Hypertensive crisis",
                "description_ja": "高血圧クリーゼ",
            },
            {
                "drug": "Halothane",
                "severity": "major",
                "description": "Sensitized myocardium to arrhythmias",
                "description_ja": "不整脈に対する心筋感受性増大",
            },
            {
                "drug": "Beta-blockers",
                "severity": "moderate",
                "description": "Unopposed alpha stimulation (hypertension)",
                "description_ja": "非拮抗α刺激（高血圧）",
            },
        ],
    },
    {
        "id": "phenylpropanolamine",
        "name": "Phenylpropanolamine (Proin)",
        "name_ja": "フェニルプロパノールアミン（プロイン）",
        "category": "cardiovascular",
        "mechanism": "Alpha-adrenergic agonist; increases urethral sphincter tone by stimulating smooth muscle alpha-1 receptors. First-line medical treatment for urethral sphincter mechanism incompetence (USMI)",
        "mechanism_ja": "α-アドレナリン作動薬；平滑筋α1受容体を刺激し尿道括約筋緊張を増加。尿道括約筋機能不全（USMI）の第一選択内科治療",
        "species_info": {
            "dog": {
                "dose": "1-2 mg/kg PO q8-12h (Proin ER: 2-4 mg/kg PO q24h)",
                "notes": "USMI in spayed females (50-65% effective); FDA-approved (Proin). May combine with estriol for refractory cases",
                "notes_ja": "避妊雌のUSMI（50-65%有効）；FDA承認（プロイン）。難治例ではエストリオール併用可",
            },
            "cat": {
                "dose": "1-1.5 mg/kg PO q8-12h",
                "notes": "Less commonly needed in cats; monitor for hypertension",
                "notes_ja": "猫では必要性が低い；高血圧モニタリング",
            },
        },
        "side_effects": ["Hypertension", "Restlessness/agitation", "Inappetence", "Urinary retention"],
        "side_effects_ja": ["高血圧", "不穏/興奮", "食欲不振", "尿閉"],
        "contraindications": "Hypertension, glaucoma, diabetes mellitus, cardiac disease, concurrent MAOIs",
        "contraindications_ja": "高血圧、緑内障、糖尿病、心疾患、MAOI併用",
        "drug_interactions": [
            {
                "drug": "MAO inhibitors",
                "severity": "major",
                "description": "Hypertensive crisis",
                "description_ja": "高血圧クリーゼ",
            },
            {
                "drug": "Tricyclic antidepressants",
                "severity": "moderate",
                "description": "Potentiated pressor effect",
                "description_ja": "昇圧効果増強",
            },
            {
                "drug": "NSAIDs",
                "severity": "mild",
                "description": "Additive renal vasoconstriction",
                "description_ja": "相加的腎血管収縮",
            },
        ],
    },
    {
        "id": "estriol",
        "name": "Estriol (Incurin)",
        "name_ja": "エストリオール（インキュリン）",
        "category": "endocrine",
        "mechanism": "Short-acting estrogen; selectively sensitizes urethral smooth muscle alpha-receptors and increases mucosal coaptation. Unlike estradiol, minimal bone marrow suppression risk",
        "mechanism_ja": "短時間作用型エストロゲン；尿道平滑筋α受容体を選択的に感作し粘膜密着を増加。エストラジオールと異なり骨髄抑制リスク最小限",
        "species_info": {
            "dog": {
                "dose": "1-2 mg/dog PO q24h (reduce to minimum effective dose after 2 weeks)",
                "notes": "USMI in spayed females (EMA-approved: Incurin); safer than DES. Can combine with PPA for refractory cases",
                "notes_ja": "避妊雌のUSMI（EMA承認：インキュリン）；DESより安全。難治例ではPPA併用可",
            }
        },
        "side_effects": [
            "Vulvar swelling",
            "Attracting males",
            "Mammary development",
            "Rare: bone marrow suppression (much less than DES)",
        ],
        "side_effects_ja": ["外陰部腫脹", "雄の誘引", "乳腺発達", "稀：骨髄抑制（DESよりはるかに少ない）"],
        "contraindications": "Estrogen-dependent tumors, intact females (endometrial hyperplasia), bone marrow suppression",
        "contraindications_ja": "エストロゲン依存性腫瘍、未避妊雌（子宮内膜過形成）、骨髄抑制",
        "drug_interactions": [
            {
                "drug": "Phenylpropanolamine",
                "severity": "mild",
                "description": "Synergistic for USMI (beneficial combination in refractory cases)",
                "description_ja": "USMIに相乗的（難治例で有益な組合せ）",
            },
            {
                "drug": "Corticosteroids",
                "severity": "moderate",
                "description": "May antagonize estrogenic effects on urethral tone",
                "description_ja": "尿道緊張へのエストロゲン効果を拮抗する可能性",
            },
        ],
    },
    {
        "id": "trilostane_feline",
        "name": "Trilostane (Feline Hyperaldosteronism)",
        "name_ja": "トリロスタン（猫高アルドステロン症）",
        "category": "endocrine",
        "mechanism": "3-beta-hydroxysteroid dehydrogenase inhibitor; blocks cortisol AND aldosterone synthesis. In cats, used for primary hyperaldosteronism (Conn's syndrome) which causes severe hypokalemia",
        "mechanism_ja": "3β-ヒドロキシステロイドデヒドロゲナーゼ阻害薬；コルチゾールとアルドステロン合成を遮断。猫では重度低カリウム血症を惹起する原発性高アルドステロン症（コン症候群）に使用",
        "species_info": {
            "cat": {
                "dose": "10-30 mg/cat PO q12-24h (start 10mg q24h, titrate based on K+ levels)",
                "notes": "Primary hyperaldosteronism (adrenal tumor/hyperplasia); monitor potassium and ACTH stimulation",
                "notes_ja": "原発性高アルドステロン症（副腎腫瘍/過形成）；カリウムとACTH刺激試験モニタリング",
            }
        },
        "side_effects": [
            "Hypoadrenocorticism (iatrogenic Addisonian crisis)",
            "Anorexia",
            "Lethargy",
            "Hyperkalemia (overcorrection)",
        ],
        "side_effects_ja": [
            "副腎皮質機能低下症（医原性アディソンクリーゼ）",
            "食欲不振",
            "嗜眠",
            "高カリウム血症（過剰是正）",
        ],
        "contraindications": "Primary hepatic disease, concurrent spironolactone (additive mineralocorticoid blockade)",
        "contraindications_ja": "原発性肝疾患、スピロノラクトン併用（相加的ミネラルコルチコイド遮断）",
        "drug_interactions": [
            {
                "drug": "Spironolactone",
                "severity": "major",
                "description": "Additive aldosterone blockade; potentially fatal hyperkalemia",
                "description_ja": "相加的アルドステロン遮断；致死的高カリウム血症の可能性",
            },
            {
                "drug": "ACE inhibitors",
                "severity": "moderate",
                "description": "Additive hyperkalemia risk",
                "description_ja": "相加的高カリウム血症リスク",
            },
        ],
    },
    {
        "id": "methimazole_transdermal",
        "name": "Methimazole Transdermal (PLO gel)",
        "name_ja": "メチマゾール経皮（PLOゲル）",
        "category": "endocrine",
        "mechanism": "Antithyroid drug in transdermal pluronic-lecithin organogel (PLO); absorbed through ear pinna skin avoiding GI side effects. Inhibits thyroid peroxidase blocking T3/T4 synthesis",
        "mechanism_ja": "経皮プルロニック-レシチンオルガノゲル（PLO）の抗甲状腺薬；耳介皮膚から吸収され消化器副作用を回避。甲状腺ペルオキシダーゼを阻害しT3/T4合成を遮断",
        "species_info": {
            "cat": {
                "dose": "2.5-5 mg/ear q12h (apply to inner pinna, alternate ears)",
                "notes": "Feline hyperthyroidism when oral dosing not feasible; slightly lower bioavailability than oral (may need higher dose)",
                "notes_ja": "経口投与困難な猫甲状腺機能亢進症；経口より生物学的利用能やや低い（高用量必要な場合あり）",
            }
        },
        "side_effects": [
            "Local skin irritation (ear)",
            "Facial pruritus",
            "Same systemic effects as oral (hepatotoxicity, blood dyscrasias) but less GI upset",
        ],
        "side_effects_ja": [
            "局所皮膚刺激（耳）",
            "顔面掻痒",
            "経口と同じ全身性副作用（肝毒性・血液異常）だが消化器障害は少ない",
        ],
        "contraindications": "Same as oral methimazole; known skin sensitivity to PLO base",
        "contraindications_ja": "経口メチマゾールと同じ；PLO基剤への皮膚感受性既知",
        "drug_interactions": [
            {
                "drug": "Same as oral methimazole",
                "severity": "moderate",
                "description": "Hepatotoxic drugs, bone marrow suppressants",
                "description_ja": "肝毒性薬、骨髄抑制薬",
            }
        ],
    },
    {
        "id": "firocoxib_equine",
        "name": "Firocoxib Equine (Equioxx)",
        "name_ja": "フィロコキシブ馬用（エクイオックス）",
        "category": "nsaids",
        "mechanism": "COX-2 selective NSAID; provides anti-inflammatory and analgesic effects with reduced GI/renal toxicity compared to non-selective NSAIDs. Paste and injectable formulations for horses",
        "mechanism_ja": "COX-2選択的NSAID；非選択的NSAIDsと比較し消化管/腎毒性を軽減しつつ抗炎症・鎮痛効果を提供。馬用ペーストおよび注射製剤",
        "species_info": {
            "horse": {
                "dose": "0.1 mg/kg PO q24h (Equioxx paste); 0.09 mg/kg IV once (Equioxx injection)",
                "notes": "Osteoarthritis, musculoskeletal pain; FDA-approved for horses. 14-day treatment maximum; lower RDC ulcer risk than phenylbutazone",
                "notes_ja": "変形性関節症、筋骨格系疼痛；馬でFDA承認。最大14日治療；フェニルブタゾンより右背側結腸潰瘍リスク低い",
            }
        },
        "side_effects": [
            "GI ulceration (less than bute)",
            "Renal papillary necrosis",
            "Oral mucosal erosion",
            "Right dorsal colitis",
        ],
        "side_effects_ja": ["消化管潰瘍（ブートより少ない）", "腎乳頭壊死", "口腔粘膜びらん", "右背側結腸炎"],
        "contraindications": "Dehydration, concurrent NSAIDs/corticosteroids, renal/hepatic disease, foals <1 year",
        "contraindications_ja": "脱水、NSAIDs/コルチコステロイド併用、腎/肝疾患、1歳未満の子馬",
        "drug_interactions": [
            {
                "drug": "Other NSAIDs",
                "severity": "major",
                "description": "Never combine NSAIDs (phenylbutazone + firocoxib = severe GI ulceration)",
                "description_ja": "NSAIDsの併用禁止（フェニルブタゾン+フィロコキシブ=重度消化管潰瘍）",
            },
            {
                "drug": "Corticosteroids",
                "severity": "major",
                "description": "Markedly increased GI ulceration risk",
                "description_ja": "消化管潰瘍リスクの著明な増加",
            },
        ],
    },
    {
        "id": "omeprazole_equine",
        "name": "Omeprazole Equine (GastroGard)",
        "name_ja": "オメプラゾール馬用（ガストロガード）",
        "category": "gastrointestinal",
        "mechanism": "Proton pump inhibitor specifically formulated for horses; inhibits H+/K+-ATPase in gastric parietal cells. Requires enteric protection for equine gastric acid environment",
        "mechanism_ja": "馬用に特別に製剤化されたプロトンポンプ阻害薬；胃壁細胞のH+/K+-ATPaseを阻害。馬の胃酸環境に対する腸溶性保護が必要",
        "species_info": {
            "horse": {
                "dose": "Treatment: 4 mg/kg PO q24h × 28d; Prevention: 1-2 mg/kg PO q24h",
                "notes": "EGUS gold standard treatment (87% healing rate at 28d). Give on empty stomach 30-60min before feed. GastroGard paste",
                "notes_ja": "EGUSゴールドスタンダード治療（28日で87%治癒率）。食前30-60分に空腹投与。ガストロガードペースト",
            }
        },
        "side_effects": [
            "Very well tolerated",
            "Rebound acid hypersecretion on discontinuation",
            "Theoretical B12/Ca malabsorption (long-term)",
        ],
        "side_effects_ja": ["忍容性非常に良好", "中止時のリバウンド酸過分泌", "理論的B12/Ca吸収不良（長期）"],
        "contraindications": "None significant; foal safety established",
        "contraindications_ja": "特記すべき禁忌なし；子馬での安全性確立済み",
        "drug_interactions": [
            {
                "drug": "Ketoconazole",
                "severity": "moderate",
                "description": "Reduced ketoconazole absorption (needs acid)",
                "description_ja": "ケトコナゾール吸収低下（酸が必要）",
            },
            {
                "drug": "Clopidogrel",
                "severity": "moderate",
                "description": "CYP2C19 inhibition may reduce clopidogrel activation",
                "description_ja": "CYP2C19阻害がクロピドグレル活性化を減弱する可能性",
            },
        ],
    },
    {
        "id": "succinylcholine_equine",
        "name": "Succinylcholine (Equine Emergency)",
        "name_ja": "サクシニルコリン（馬緊急）",
        "category": "anesthetics",
        "mechanism": "Depolarizing neuromuscular blocker; mimics acetylcholine causing persistent depolarization and phase II block. Ultra-rapid onset (30-60s), ultra-short duration (5-10 min in horses)",
        "mechanism_ja": "脱分極性神経筋遮断薬；アセチルコリンを模倣し持続的脱分極と第II相ブロックを惹起。超速効性（30-60秒）、超短時間作用（馬で5-10分）",
        "species_info": {
            "horse": {
                "dose": "0.1 mg/kg IV (rapid recumbency for emergency procedures)",
                "notes": "Chemical casting for field emergencies only; no analgesia/sedation (MUST combine with sedation). Ethical concerns limit use",
                "notes_ja": "フィールド緊急時のケミカルキャスティングのみ；鎮痛/鎮静なし（鎮静と必ず併用）。倫理的懸念から使用制限",
            }
        },
        "side_effects": [
            "Malignant hyperthermia (susceptible horses)",
            "Hyperkalemia",
            "Muscle fasciculations",
            "Masseter spasm",
            "Cardiac arrhythmias",
        ],
        "side_effects_ja": ["悪性高熱症（感受性馬）", "高カリウム血症", "筋線維束攣縮", "咬筋痙攣", "心不整脈"],
        "contraindications": "MH susceptibility, hyperkalemia, burns/crush injuries (K+ release), denervation atrophy, myopathies",
        "contraindications_ja": "悪性高熱症感受性、高カリウム血症、熱傷/圧挫傷（K+放出）、除神経萎縮、ミオパチー",
        "drug_interactions": [
            {
                "drug": "Anticholinesterases",
                "severity": "major",
                "description": "Prolongs phase I block (paradoxical with depolarizing agents)",
                "description_ja": "第I相ブロックを延長（脱分極薬との矛盾的作用）",
            },
            {
                "drug": "Aminoglycosides",
                "severity": "moderate",
                "description": "Potentiated neuromuscular block",
                "description_ja": "神経筋遮断増強",
            },
        ],
    },
    {
        "id": "detomidine_gel",
        "name": "Detomidine Oromucosal Gel (Dormosedan Gel)",
        "name_ja": "デトミジン口腔粘膜ゲル（ドルモセダンゲル）",
        "category": "sedatives",
        "mechanism": "Alpha-2 adrenergic agonist in sublingual gel; absorbed through oral mucosa for standing sedation without injection. Owner-applied sedation for minor procedures",
        "mechanism_ja": "舌下ゲルのα2アドレナリン作動薬；注射なしの立位鎮静のため口腔粘膜から吸収。軽微処置のための飼い主投与型鎮静",
        "species_info": {
            "horse": {
                "dose": "0.04 mg/kg sublingually (apply under tongue, do NOT swallow)",
                "notes": "Standing sedation for farrier, clipping, minor wound care; owner can administer. FDA-approved. 40 min onset, 2-3h duration",
                "notes_ja": "装蹄、クリッピング、軽微創傷処置の立位鎮静；飼い主が投与可能。FDA承認。発現40分、持続2-3時間",
            }
        },
        "side_effects": ["Ataxia", "Sweating", "Bradycardia", "Penile prolapse (geldings)", "Reduced GI motility"],
        "side_effects_ja": ["運動失調", "発汗", "徐脈", "陰茎脱出（せん馬）", "消化管運動低下"],
        "contraindications": "Severe cardiovascular disease, endotoxemia, horses intended for food (withdrawal period)",
        "contraindications_ja": "重度心血管疾患、エンドトキセミア、食用馬（休薬期間）",
        "drug_interactions": [
            {
                "drug": "Other alpha-2 agonists",
                "severity": "major",
                "description": "Profound cardiovascular depression; do not combine",
                "description_ja": "重度心血管抑制；併用不可",
            },
            {
                "drug": "Potentiated sulfonamides (IV)",
                "severity": "major",
                "description": "Fatal cardiac arrhythmias reported in horses",
                "description_ja": "馬で致死的心不整脈の報告",
            },
        ],
    },
    {
        "id": "pergolide_equine",
        "name": "Pergolide (Prascend)",
        "name_ja": "ペルゴリド（プラセンド）",
        "category": "endocrine",
        "mechanism": "D1/D2 dopamine receptor agonist; restores dopaminergic inhibition of pars intermedia melanotrophs in PPID. Reduces ACTH hypersecretion from dysfunctional pituitary",
        "mechanism_ja": "D1/D2ドパミン受容体作動薬；PPIDの中間葉メラノトロフへのドパミン抑制を回復。機能不全下垂体からのACTH過分泌を減少",
        "species_info": {
            "horse": {
                "dose": "2 μg/kg PO q24h (start 0.5 mg/horse); titrate based on ACTH levels",
                "notes": "PPID (Equine Cushing's) — FDA-approved (Prascend). Lifelong treatment; monitor ACTH q4-6 months. Seasonal ACTH rise (autumn) may need dose increase",
                "notes_ja": "PPID（馬クッシング病）— FDA承認（プラセンド）。生涯治療；ACTH 4-6ヶ月毎モニタリング。季節性ACTH上昇（秋）で増量必要な場合あり",
            }
        },
        "side_effects": [
            "Anorexia (first 2-3 days)",
            "Lethargy",
            "Diarrhea",
            "Sweating",
            "Laminitis exacerbation (rare, usually from inadequate control)",
        ],
        "side_effects_ja": [
            "食欲不振（初期2-3日）",
            "嗜眠",
            "下痢",
            "発汗",
            "蹄葉炎悪化（稀、通常はコントロール不十分による）",
        ],
        "contraindications": "Hypersensitivity to ergot derivatives; caution in horses with severe laminitis (optimize pain management first)",
        "contraindications_ja": "麦角誘導体過敏症；重度蹄葉炎の馬では注意（まず疼痛管理を最適化）",
        "drug_interactions": [
            {
                "drug": "Dopamine antagonists (metoclopramide, phenothiazines)",
                "severity": "major",
                "description": "Directly antagonizes pergolide effect; avoid concurrent use",
                "description_ja": "ペルゴリド効果を直接拮抗；併用回避",
            },
            {
                "drug": "Erythromycin",
                "severity": "moderate",
                "description": "Increases pergolide levels (CYP3A4 inhibition)",
                "description_ja": "ペルゴリド濃度上昇（CYP3A4阻害）",
            },
        ],
    },
]
