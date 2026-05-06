"""Drug batch 19 — dermatology, wound care, supplements, nutraceuticals, additional antiparasitics (33 drugs)."""

DRUGS_BATCH_19 = [
    {
        "id": "oclacitinib",
        "name": "Oclacitinib (Apoquel)",
        "name_ja": "オクラシチニブ（アポキル）",
        "category": "dermatology",
        "mechanism": "Janus kinase (JAK1) inhibitor; selectively blocks IL-31, IL-4, IL-13 signaling (pruritus and inflammation)",
        "mechanism_ja": "ヤヌスキナーゼ（JAK1）阻害薬。IL-31/IL-4/IL-13シグナルを選択的に遮断（掻痒・炎症）",
        "species_info": {
            "dog": {"dose": "0.4-0.6 mg/kg PO q12h×14日、以後q24h", "notes_ja": "犬アトピー性皮膚炎の第一選択。即効性（4時間以内）。12ヶ月齢以上", "notes": "First-line canine atopic dermatitis. Rapid onset (<4h). Dogs ≥12 months old"}
        },
        "side_effects": "Diarrhea, vomiting, decreased WBC, increased susceptibility to infections/neoplasia",
        "side_effects_ja": "下痢、嘔吐、白血球減少、感染・腫瘍感受性増加",
        "contraindications": "Dogs <12 months, serious infections, history of neoplasia (relative)",
        "contraindications_ja": "12ヶ月齢未満、重度感染症、腫瘍既往（相対的）",
        "drug_interactions": [
            {"drug": "ciclosporin", "severity": "moderate", "description_ja": "免疫抑制の相加。併用エビデンス限定", "description": "Additive immunosuppression. Limited combination data"},
            {"drug": "corticosteroids", "severity": "moderate", "description_ja": "免疫抑制増強。短期併用のみ", "description": "Enhanced immunosuppression. Short-term overlap only"}
        ]
    },
    {
        "id": "ciclosporin_oral",
        "name": "Ciclosporin (Modified Oral)",
        "name_ja": "シクロスポリン（改良型経口・アトピカ）",
        "category": "immunosuppressive",
        "mechanism": "Calcineurin inhibitor; blocks T-cell activation and IL-2 transcription",
        "mechanism_ja": "カルシニューリン阻害薬。T細胞活性化とIL-2転写を遮断",
        "species_info": {
            "dog": {"dose": "5 mg/kg PO q24h（空腹時）; 4-6週で効果判定", "notes_ja": "アトピー性皮膚炎・肛門周囲瘻・IMHA/ITP（プレドニゾロン併用）", "notes": "Atopic dermatitis, perianal fistula, IMHA/ITP (with prednisolone)"},
            "cat": {"dose": "7 mg/kg PO q24h", "notes_ja": "猫のアレルギー性皮膚炎・好酸球性肉芽腫症候群・IBD", "notes": "Feline allergic dermatitis, eosinophilic granuloma complex, IBD"},
            "horse": {"dose": "2-5 mg/kg PO q12-24h", "notes_ja": "免疫介在性角膜炎", "notes": "Immune-mediated keratitis"},
            "rabbit": {"dose": "データ限定", "notes_ja": "使用データ限定的", "notes": "Limited data"}
        },
        "side_effects": "GI upset, gingival hyperplasia, hirsutism, papillomatosis, immunosuppression",
        "side_effects_ja": "消化器症状、歯肉肥厚、多毛症、乳頭腫症、免疫抑制",
        "contraindications": "Neoplasia history (relative), FeLV/FIV+ cats, <6 months age",
        "contraindications_ja": "腫瘍既往（相対的）、FeLV/FIV陽性猫、6ヶ月齢未満",
        "drug_interactions": [
            {"drug": "ketoconazole", "severity": "major", "description_ja": "シクロスポリン血中濃度上昇（意図的に用量削減に利用可）", "description": "Increased CsA levels (intentionally used for dose reduction)"},
            {"drug": "nsaids", "severity": "moderate", "description_ja": "腎毒性リスク増加", "description": "Increased nephrotoxicity risk"}
        ]
    },
    {
        "id": "cephalexin",
        "name": "Cephalexin",
        "name_ja": "セファレキシン",
        "category": "antibiotics",
        "mechanism": "First-generation cephalosporin; inhibits cell wall synthesis (PBP binding). Gram-positive focused",
        "mechanism_ja": "第一世代セファロスポリン。細胞壁合成阻害（PBP結合）。グラム陽性菌中心",
        "species_info": {
            "dog": {"dose": "22-30 mg/kg PO q12h", "notes_ja": "膿皮症第一選択。UTI・軟部組織感染。3-4週間（深在性膿皮症は6-8週）", "notes": "First-line pyoderma. UTI, soft tissue infections. 3-4 weeks (deep: 6-8 weeks)"},
            "cat": {"dose": "15-25 mg/kg PO q12h", "notes_ja": "皮膚感染・UTI。猫は味を嫌がる場合あり", "notes": "Skin infections, UTI. Cats may dislike taste"},
            "horse": {"dose": "30 mg/kg PO q8h", "notes_ja": "軟部組織感染。経口バイオアベイラビリティ低い", "notes": "Soft tissue infections. Low oral bioavailability"},
            "rabbit": {"dose": "15-25 mg/kg PO q8-12h", "notes_ja": "皮膚感染。腸内細菌叢への影響は少ない", "notes": "Skin infections. Less GI microbiome disruption"},
            "guinea_pig": {"dose": "25 mg/kg PO q12h", "notes_ja": "皮膚感染。ペニシリン系より安全", "notes": "Skin infections. Safer than penicillins"},
            "ferret": {"dose": "15-25 mg/kg PO q8-12h", "notes_ja": "皮膚・軟部組織感染", "notes": "Skin/soft tissue infections"},
            "bird": {"dose": "35-50 mg/kg PO q6-8h", "notes_ja": "グラム陽性菌感染", "notes": "Gram-positive infections"}
        },
        "side_effects": "GI upset, allergic reaction (cross-reactivity with penicillins ~5%)",
        "side_effects_ja": "消化器症状、アレルギー反応（ペニシリンとの交差反応約5%）",
        "contraindications": "Known cephalosporin/penicillin allergy",
        "contraindications_ja": "セファロスポリン/ペニシリン アレルギー既往",
        "drug_interactions": [
            {"drug": "aminoglycosides", "severity": "moderate", "description_ja": "腎毒性の相加リスク", "description": "Additive nephrotoxicity risk"}
        ]
    },
    {
        "id": "cefovecin",
        "name": "Cefovecin (Convenia)",
        "name_ja": "セフォベシン（コンベニア）",
        "category": "antibiotics",
        "mechanism": "Third-generation cephalosporin; ultra-long-acting (14 days) due to high protein binding",
        "mechanism_ja": "第三世代セファロスポリン。高タンパク結合により超長時間作用（14日間）",
        "species_info": {
            "dog": {"dose": "8 mg/kg SC 1回（効果14日間）", "notes_ja": "膿皮症・UTI・創傷感染。経口投与困難な場合。注射後14日間撤回不可", "notes": "Pyoderma, UTI, wound infections. When oral dosing difficult. Cannot withdraw after injection"},
            "cat": {"dose": "8 mg/kg SC 1回（効果14日間）", "notes_ja": "猫の皮膚感染・UTI。投薬困難な猫に有用。腎排泄→腎不全で半減期延長", "notes": "Feline skin infections, UTI. Useful for difficult-to-medicate cats. Renal excretion"},
            "rabbit": {"dose": "8 mg/kg SC（14日間効果）", "notes_ja": "投薬困難なウサギに有用", "notes": "Useful for difficult-to-medicate rabbits"},
            "guinea_pig": {"dose": "8 mg/kg SC", "notes_ja": "皮膚感染", "notes": "Skin infections"},
            "ferret": {"dose": "8 mg/kg SC", "notes_ja": "フェレットの皮膚感染", "notes": "Ferret skin infections"}
        },
        "side_effects": "Injection site swelling, GI upset, allergic reaction",
        "side_effects_ja": "注射部位腫脹、消化器症状、アレルギー反応",
        "contraindications": "Renal failure (prolonged half-life), penicillin allergy",
        "contraindications_ja": "腎不全（半減期延長）、ペニシリンアレルギー",
        "drug_interactions": []
    },
    {
        "id": "mupirocin",
        "name": "Mupirocin 2% Ointment",
        "name_ja": "ムピロシン2%軟膏（バクトロバン）",
        "category": "dermatology",
        "mechanism": "Inhibits bacterial isoleucyl-tRNA synthetase; bacteriostatic/bactericidal against Staphylococcus",
        "mechanism_ja": "細菌イソロイシルtRNA合成酵素を阻害。ブドウ球菌に対して静菌/殺菌的",
        "species_info": {
            "dog": {"dose": "患部に薄く塗布 q8-12h × 7-14日", "notes_ja": "表在性膿皮症・MRSA局所感染・皮膚創傷感染", "notes": "Surface pyoderma, localized MRSA, wound infections"},
            "cat": {"dose": "患部に薄く塗布 q8-12h", "notes_ja": "猫の局所皮膚感染。PEG含有製剤は猫で経口毒性→舐めさせない", "notes": "Localized skin infections. PEG-containing formulations toxic if ingested by cats"}
        },
        "side_effects": "Local irritation, rarely contact dermatitis",
        "side_effects_ja": "局所刺激、稀に接触性皮膚炎",
        "contraindications": "Large open wounds (systemic PEG absorption), cat ingestion",
        "contraindications_ja": "広範囲開放創（PEG全身吸収）、猫の舐め取り",
        "drug_interactions": []
    },
    {
        "id": "silver_sulfadiazine_topical",
        "name": "Silver Sulfadiazine 1% Cream",
        "name_ja": "スルファジアジン銀1%クリーム",
        "category": "dermatology",
        "mechanism": "Silver ions disrupt bacterial cell membrane; sulfadiazine inhibits folate synthesis. Broad spectrum",
        "mechanism_ja": "銀イオンが細菌細胞膜を破壊、スルファジアジンが葉酸合成を阻害。広域抗菌",
        "species_info": {
            "dog": {"dose": "患部に1-2mm厚で塗布 q12-24h", "notes_ja": "熱傷・広範囲創傷・皮膚移植部位", "notes": "Burns, extensive wounds, skin graft sites"},
            "cat": {"dose": "患部に塗布 q12-24h", "notes_ja": "熱傷・創傷。舐め防止にカラー装着", "notes": "Burns, wounds. E-collar to prevent licking"},
            "horse": {"dose": "患部に塗布 q12-24h", "notes_ja": "広範囲創傷・熱傷", "notes": "Extensive wounds, burns"},
            "bird": {"dose": "患部に薄く塗布 q12-24h", "notes_ja": "熱傷・脚部創傷", "notes": "Burns, foot wounds"},
            "reptile": {"dose": "患部に塗布 q24h", "notes_ja": "爬虫類の火傷・皮膚感染", "notes": "Reptilian burns, skin infections"}
        },
        "side_effects": "Transient leukopenia (large areas), argyria (chronic use), delayed eschar separation",
        "side_effects_ja": "一過性白血球減少（広範囲）、銀沈着症（長期使用）、痂皮分離遅延",
        "contraindications": "Sulfonamide allergy, pregnancy (teratogenic), hepatic/renal failure",
        "contraindications_ja": "サルファ剤アレルギー、妊娠（催奇形性）、肝/腎不全",
        "drug_interactions": []
    },
    {
        "id": "chlorhexidine_topical",
        "name": "Chlorhexidine Solution/Shampoo",
        "name_ja": "クロルヘキシジン溶液/シャンプー",
        "category": "dermatology",
        "mechanism": "Disrupts bacterial cell membrane; bactericidal with residual activity for 24-48h",
        "mechanism_ja": "細菌細胞膜を破壊。殺菌的で24-48時間の残存活性",
        "species_info": {
            "dog": {"dose": "2-4%シャンプー: 週2-3回; 0.05%溶液: 洗浄用", "notes_ja": "膿皮症・マラセチア皮膚炎の局所療法。2%+ミコナゾール2%併用シャンプーが効果的", "notes": "Pyoderma, Malassezia dermatitis. 2% + miconazole 2% combination shampoo effective"},
            "cat": {"dose": "2%シャンプー/溶液", "notes_ja": "皮膚感染の局所療法。猫は4%で口腔刺激性あり→2%推奨", "notes": "Topical for skin infections. Cats: use 2% (4% causes oral irritation)"},
            "horse": {"dose": "2-4%溶液/スクラブ", "notes_ja": "術前皮膚消毒・創傷洗浄", "notes": "Preoperative skin antisepsis, wound irrigation"},
            "rabbit": {"dose": "0.05-2%溶液", "notes_ja": "創傷洗浄・皮膚感染", "notes": "Wound irrigation, skin infections"},
            "bird": {"dose": "0.05%希釈溶液", "notes_ja": "創傷洗浄。高濃度は毒性あり", "notes": "Wound irrigation. High concentrations toxic"},
            "reptile": {"dose": "0.05-0.5%溶液", "notes_ja": "創傷洗浄・シェルロット", "notes": "Wound irrigation, shell rot"}
        },
        "side_effects": "Contact dermatitis (high concentration), ototoxicity (do not use in ears with ruptured TM)",
        "side_effects_ja": "接触性皮膚炎（高濃度）、耳毒性（鼓膜穿孔時は使用禁忌）",
        "contraindications": "Middle/inner ear (ototoxic), eyes, CNS tissue",
        "contraindications_ja": "中耳/内耳（耳毒性）、眼、CNS組織",
        "drug_interactions": []
    },
    {
        "id": "miconazole_topical",
        "name": "Miconazole (Topical)",
        "name_ja": "ミコナゾール（外用）",
        "category": "antifungals",
        "mechanism": "Imidazole antifungal; inhibits ergosterol synthesis in fungal cell membrane",
        "mechanism_ja": "イミダゾール系抗真菌薬。真菌細胞膜のエルゴステロール合成を阻害",
        "species_info": {
            "dog": {"dose": "2%シャンプー/クリーム/ローション q12-24h", "notes_ja": "マラセチア皮膚炎・皮膚糸状菌症の局所治療。クロルヘキシジンとの併用が効果的", "notes": "Malassezia dermatitis, dermatophytosis topical. Effective with chlorhexidine"},
            "cat": {"dose": "2%クリーム/ローション q12-24h", "notes_ja": "猫の皮膚糸状菌症局所治療", "notes": "Feline dermatophytosis topical"},
            "guinea_pig": {"dose": "2%クリーム q12-24h", "notes_ja": "皮膚糸状菌症", "notes": "Dermatophytosis"},
            "rabbit": {"dose": "2%クリーム q12h", "notes_ja": "皮膚糸状菌症", "notes": "Dermatophytosis"},
            "hamster": {"dose": "2%クリーム q12h", "notes_ja": "皮膚糸状菌症", "notes": "Dermatophytosis"},
            "hedgehog": {"dose": "2%クリーム q12h", "notes_ja": "皮膚糸状菌症", "notes": "Dermatophytosis"}
        },
        "side_effects": "Local irritation, rarely contact dermatitis",
        "side_effects_ja": "局所刺激、稀に接触性皮膚炎",
        "contraindications": "Known azole hypersensitivity",
        "contraindications_ja": "アゾール系過敏症",
        "drug_interactions": []
    },
    {
        "id": "omega_3_fatty_acids",
        "name": "Omega-3 Fatty Acids (EPA/DHA)",
        "name_ja": "オメガ3脂肪酸（EPA/DHA）",
        "category": "dermatology",
        "mechanism": "Competes with arachidonic acid in inflammatory pathways; anti-inflammatory eicosanoid production",
        "mechanism_ja": "炎症経路でアラキドン酸と競合。抗炎症性エイコサノイド産生を促進",
        "species_info": {
            "dog": {"dose": "EPA 40-70 mg/kg/day + DHA 25-45 mg/kg/day", "notes_ja": "アトピー性皮膚炎補助・OA・CKD・心疾患。効果発現に6-8週", "notes": "Atopic dermatitis adjunct, OA, CKD, cardiac disease. 6-8 weeks for effect"},
            "cat": {"dose": "EPA 30-40 mg/kg/day + DHA 20-25 mg/kg/day", "notes_ja": "CKD（IRIS推奨）・アトピー・OA。魚油カプセルで投与", "notes": "CKD (IRIS recommended), atopy, OA. Fish oil capsules"},
            "horse": {"dose": "フラキシードオイル 100-200 mL/day", "notes_ja": "皮膚の健康維持・炎症性疾患補助", "notes": "Skin health, inflammatory disease adjunct"},
            "bird": {"dose": "フラキシードオイル 0.1-0.5 mL/kg/day", "notes_ja": "羽毛の健康維持・皮膚疾患", "notes": "Feather health, skin disease"}
        },
        "side_effects": "Diarrhea (high dose), fishy breath, delayed wound healing (theoretical)",
        "side_effects_ja": "下痢（高用量）、魚臭い口臭、創傷治癒遅延（理論的）",
        "contraindications": "Acute pancreatitis (high fat), coagulation disorders (theoretical)",
        "contraindications_ja": "急性膵炎（高脂肪）、凝固障害（理論的）",
        "drug_interactions": [
            {"drug": "warfarin", "severity": "minor", "description_ja": "出血リスクの軽度増加", "description": "Mildly increased bleeding risk"}
        ]
    },
    {
        "id": "glucosamine_chondroitin",
        "name": "Glucosamine/Chondroitin Sulfate",
        "name_ja": "グルコサミン/コンドロイチン硫酸",
        "category": "musculoskeletal",
        "mechanism": "Provides building blocks for cartilage proteoglycan synthesis; inhibits cartilage-degrading enzymes",
        "mechanism_ja": "軟骨プロテオグリカン合成の構成要素を提供。軟骨分解酵素を阻害",
        "species_info": {
            "dog": {"dose": "グルコサミン 20 mg/kg/day + コンドロイチン 15 mg/kg/day", "notes_ja": "OA補助療法。NSAIDsとの併用で相乗効果。効果発現に4-8週", "notes": "OA adjunct. Synergistic with NSAIDs. 4-8 weeks for effect"},
            "cat": {"dose": "グルコサミン 125-250 mg/cat/day", "notes_ja": "猫のOA補助。FISS猫では軟骨保護の報告", "notes": "Feline OA adjunct"},
            "horse": {"dose": "グルコサミン 10-20 mg/kg/day PO", "notes_ja": "OA・関節軟骨保護", "notes": "OA, articular cartilage protection"},
            "rabbit": {"dose": "グルコサミン 20 mg/kg/day", "notes_ja": "スナッフル後の関節炎", "notes": "Post-snuffles arthritis"}
        },
        "side_effects": "GI upset (rare), allergic reaction (shellfish-derived products)",
        "side_effects_ja": "消化器症状（稀）、アレルギー反応（甲殻類由来製品）",
        "contraindications": "Shellfish allergy (shellfish-derived glucosamine)",
        "contraindications_ja": "甲殻類アレルギー（甲殻類由来グルコサミン）",
        "drug_interactions": []
    },
    {
        "id": "probiotics_vet",
        "name": "Probiotics (Veterinary)",
        "name_ja": "プロバイオティクス（獣医用）",
        "category": "gastrointestinal",
        "mechanism": "Live beneficial microorganisms that restore intestinal microbiome balance and compete with pathogens",
        "mechanism_ja": "腸内細菌叢バランスを回復し病原体と競合する生きた有益微生物",
        "species_info": {
            "dog": {"dose": "製品に依存; E. faecium SF68: 1×10^8 CFU/day", "notes_ja": "急性胃腸炎・抗生物質関連下痢・IBD補助。Enterococcus faecium SF68に最もエビデンスあり", "notes": "Acute GI, antibiotic-associated diarrhea, IBD adjunct. Best evidence for E. faecium SF68"},
            "cat": {"dose": "製品に依存; E. faecium SF68: 1×10^8 CFU/day", "notes_ja": "急性胃腸炎・ストレス関連下痢。猫用製品を使用", "notes": "Acute GI, stress-related diarrhea. Use feline-specific products"},
            "horse": {"dose": "Saccharomyces boulardii 10-25 g/day", "notes_ja": "抗生物質関連下痢・子馬の下痢", "notes": "Antibiotic-associated diarrhea, foal diarrhea"},
            "rabbit": {"dose": "S. boulardii, E. faecium; 製品に依存", "notes_ja": "GI stasis後・抗生物質後の腸内環境回復", "notes": "Post-GI stasis, post-antibiotic microbiome restoration"},
            "guinea_pig": {"dose": "製品に依存", "notes_ja": "抗生物質後の腸内環境回復", "notes": "Post-antibiotic recovery"},
            "chinchilla": {"dose": "製品に依存", "notes_ja": "抗生物質後", "notes": "Post-antibiotic"},
            "bird": {"dose": "Lactobacillus spp.; 飲水添加", "notes_ja": "抗生物質後・ストレス後", "notes": "Post-antibiotic, post-stress"}
        },
        "side_effects": "None significant; rarely bloating",
        "side_effects_ja": "特になし。稀に膨満感",
        "contraindications": "Severely immunocompromised animals (theoretical translocation risk)",
        "contraindications_ja": "重度免疫不全動物（理論的な菌血症リスク）",
        "drug_interactions": []
    },
    {
        "id": "cobalamin_injection",
        "name": "Cobalamin (Vitamin B12) Injectable",
        "name_ja": "コバラミン（ビタミンB12）注射",
        "category": "miscellaneous",
        "mechanism": "Essential cofactor for methionine synthase and methylmalonyl-CoA mutase; required for DNA synthesis",
        "mechanism_ja": "メチオニン合成酵素とメチルマロニルCoAムターゼの必須補因子。DNA合成に必要",
        "species_info": {
            "dog": {"dose": "250-1500 μg SC/IM q7日×6週、以後月1回", "notes_ja": "EPI・IBD・慢性腸疾患でのB12欠乏。血清コバラミン<300 ng/Lで補充", "notes": "EPI, IBD, chronic enteropathy B12 deficiency. Supplement if serum <300 ng/L"},
            "cat": {"dose": "250 μg SC q7日×6週、以後月1回", "notes_ja": "猫の慢性腸疾患・三臓器炎でのB12欠乏。予後因子としても重要", "notes": "Chronic enteropathy, triaditis B12 deficiency. Also prognostic marker"},
            "rabbit": {"dose": "250 μg SC q7日", "notes_ja": "慢性GI疾患", "notes": "Chronic GI disease"},
            "ferret": {"dose": "250 μg SC q7日", "notes_ja": "IBDに伴うB12欠乏", "notes": "IBD-associated B12 deficiency"}
        },
        "side_effects": "None significant; rare injection site reaction",
        "side_effects_ja": "特になし。稀に注射部位反応",
        "contraindications": "Known cobalamin allergy (extremely rare)",
        "contraindications_ja": "コバラミンアレルギー（極めて稀）",
        "drug_interactions": []
    },
    {
        "id": "vitamin_d3",
        "name": "Calcitriol (1,25-Dihydroxyvitamin D3)",
        "name_ja": "カルシトリオール（活性型ビタミンD3）",
        "category": "endocrine",
        "mechanism": "Active form of vitamin D; increases intestinal calcium absorption, promotes bone mineralization",
        "mechanism_ja": "ビタミンDの活性型。腸管カルシウム吸収を増加、骨石灰化を促進",
        "species_info": {
            "dog": {"dose": "1.5-3.5 ng/kg PO q24h", "notes_ja": "CKDステージ3-4の二次性上皮小体機能亢進症。iCa・リン・PTHモニタリング必須", "notes": "CKD stage 3-4 secondary hyperparathyroidism. Monitor iCa, phosphorus, PTH"},
            "cat": {"dose": "1.5-3.5 ng/kg PO q24h", "notes_ja": "猫のCKDに伴う二次性副甲状腺機能亢進症", "notes": "CKD secondary hyperparathyroidism"},
            "reptile": {"dose": "データ限定的; UVB照射が第一選択", "notes_ja": "MBDにはUVB照射が優先。カルシトリオールは補助", "notes": "UVB lighting preferred for MBD. Calcitriol is adjunctive"},
            "bird": {"dose": "データ限定的", "notes_ja": "代謝性骨疾患の補助", "notes": "Metabolic bone disease adjunct"}
        },
        "side_effects": "Hypercalcemia, hyperphosphatemia, soft tissue mineralization",
        "side_effects_ja": "高カルシウム血症、高リン血症、軟部組織石灰化",
        "contraindications": "Hypercalcemia, hyperphosphatemia (correct first), vitamin D toxicity",
        "contraindications_ja": "高カルシウム血症、高リン血症（先に補正）、ビタミンD中毒",
        "drug_interactions": [
            {"drug": "thiazide_diuretics", "severity": "moderate", "description_ja": "高カルシウム血症リスク", "description": "Hypercalcemia risk"}
        ]
    },
    {
        "id": "eprinomectin_topical",
        "name": "Eprinomectin (Pour-on)",
        "name_ja": "エプリノメクチン（経皮投与）",
        "category": "antiparasitic",
        "mechanism": "Macrocyclic lactone; binds glutamate-gated chloride channels causing parasite paralysis",
        "mechanism_ja": "大環状ラクトン系。グルタミン酸作動性塩素イオンチャネルに結合し寄生虫を麻痺",
        "species_info": {
            "cat": {"dose": "0.5 mg/kg 局所（スポットオン）; ブロードライン配合", "notes_ja": "猫のフィラリア予防・消化管寄生虫・外部寄生虫。ブロードライン（fipronil+S-methoprene+eprinomectin+praziquantel）配合", "notes": "Feline heartworm prevention, GI parasites, ectoparasites. Component of Broadline"},
            "horse": {"dose": "0.5 mg/kg 経皮投与（背線上）", "notes_ja": "牛用製品。馬でのオフラベル使用報告あり", "notes": "Cattle product. Off-label equine use reported"}
        },
        "side_effects": "Rare; transient local irritation",
        "side_effects_ja": "稀。一過性の局所刺激",
        "contraindications": "Ivermectin-sensitive breeds (MDR1/ABCB1 mutation — theoretical cross-sensitivity)",
        "contraindications_ja": "イベルメクチン感受性品種（MDR1/ABCB1変異 — 理論的交差感受性）",
        "drug_interactions": []
    },
    {
        "id": "praziquantel",
        "name": "Praziquantel",
        "name_ja": "プラジカンテル（ドロンタール配合）",
        "category": "antiparasitic",
        "mechanism": "Increases cestode/trematode cell membrane permeability to calcium, causing contraction and paralysis",
        "mechanism_ja": "条虫/吸虫の細胞膜カルシウム透過性を増加し、収縮・麻痺を引き起こす",
        "species_info": {
            "dog": {"dose": "5-10 mg/kg PO/SC 1回; エキノコックス: 5 mg/kg PO q24h×3日", "notes_ja": "条虫（瓜実条虫・エキノコックス）。ドロンタール配合（+ピランテル）", "notes": "Cestodes (Dipylidium, Echinococcus). Drontal combination (+pyrantel)"},
            "cat": {"dose": "5 mg/kg PO/SC 1回", "notes_ja": "条虫駆除。ドロンタール猫用（+ピランテル）", "notes": "Cestode treatment. Drontal for cats (+pyrantel)"},
            "horse": {"dose": "1-1.5 mg/kg PO 1回", "notes_ja": "馬の条虫（Anoplocephala perfoliata）", "notes": "Equine tapeworm (A. perfoliata)"},
            "rabbit": {"dose": "5-10 mg/kg PO/SC 1回; 14日後繰返し", "notes_ja": "ウサギの条虫", "notes": "Rabbit cestodes"},
            "bird": {"dose": "5-10 mg/kg PO 1回", "notes_ja": "鳥類の条虫", "notes": "Avian cestodes"},
            "reptile": {"dose": "5-8 mg/kg PO 1回; 14日後繰返し", "notes_ja": "爬虫類の条虫", "notes": "Reptilian cestodes"},
            "fish": {"dose": "2-10 mg/L 浴水 3-24h; PO 50 mg/kg 1回", "notes_ja": "魚の吸虫（ギロダクチルス・ダクチロギルス）", "notes": "Fish trematodes (Gyrodactylus, Dactylogyrus)"},
            "ferret": {"dose": "5 mg/kg PO 1回", "notes_ja": "フェレットの条虫", "notes": "Ferret cestodes"},
            "hamster": {"dose": "5-10 mg/kg PO 1回", "notes_ja": "条虫", "notes": "Cestodes"},
            "guinea_pig": {"dose": "5-10 mg/kg PO 1回", "notes_ja": "条虫", "notes": "Cestodes"}
        },
        "side_effects": "Transient GI upset, drooling (cats, bitter taste), pain on injection (SC)",
        "side_effects_ja": "一過性消化器症状、流涎（猫、苦味）、注射時疼痛（SC）",
        "contraindications": "Puppies/kittens <4 weeks, debilitated animals",
        "contraindications_ja": "4週齢未満の子犬/子猫、衰弱動物",
        "drug_interactions": []
    },
    {
        "id": "pyrantel_pamoate",
        "name": "Pyrantel Pamoate",
        "name_ja": "ピランテルパモ酸塩",
        "category": "antiparasitic",
        "mechanism": "Depolarizing neuromuscular blocker in nematodes; causes spastic paralysis and expulsion",
        "mechanism_ja": "線虫の脱分極性神経筋遮断薬。痙性麻痺を引き起こし排出",
        "species_info": {
            "dog": {"dose": "5-10 mg/kg PO 1回; 子犬: 2週齢から2週間隔で投与", "notes_ja": "回虫・鉤虫。子犬の定期駆虫（2/4/6/8週齢）。安全性高い", "notes": "Roundworms, hookworms. Puppy deworming schedule (2/4/6/8 weeks). Very safe"},
            "cat": {"dose": "5-10 mg/kg PO 1回", "notes_ja": "回虫・鉤虫。子猫の定期駆虫", "notes": "Roundworms, hookworms. Kitten deworming"},
            "horse": {"dose": "6.6 mg/kg PO 1回", "notes_ja": "大型円虫・小型円虫。子馬の駆虫プログラム", "notes": "Large/small strongyles. Foal deworming program"},
            "rabbit": {"dose": "5-10 mg/kg PO 1回; 14日後繰返し", "notes_ja": "蟯虫（Passalurus ambiguus）", "notes": "Pinworm (Passalurus ambiguus)"},
            "bird": {"dose": "4.5 mg/kg PO 1回; 14日後繰返し", "notes_ja": "回虫", "notes": "Roundworms"},
            "ferret": {"dose": "4.4 mg/kg PO 1回", "notes_ja": "回虫", "notes": "Roundworms"},
            "hamster": {"dose": "5 mg/kg PO 1回", "notes_ja": "蟯虫", "notes": "Pinworm"},
            "guinea_pig": {"dose": "5 mg/kg PO 1回", "notes_ja": "蟯虫", "notes": "Pinworm"},
            "reptile": {"dose": "5 mg/kg PO 1回; 14日後繰返し", "notes_ja": "線虫", "notes": "Nematodes"}
        },
        "side_effects": "Minimal; rare GI upset, vomiting",
        "side_effects_ja": "最小限。稀に消化器症状・嘔吐",
        "contraindications": "Concurrent levamisole or morantel (same mechanism)",
        "contraindications_ja": "レバミゾール/モランテル併用（同一機序）",
        "drug_interactions": [
            {"drug": "levamisole", "severity": "major", "description_ja": "毒性増強（同一作用点）", "description": "Enhanced toxicity (same site of action)"},
            {"drug": "piperazine", "severity": "major", "description_ja": "拮抗作用", "description": "Antagonistic effects"}
        ]
    },
    {
        "id": "fenbendazole",
        "name": "Fenbendazole",
        "name_ja": "フェンベンダゾール（パナクール）",
        "category": "antiparasitic",
        "mechanism": "Benzimidazole; binds β-tubulin inhibiting microtubule polymerization in parasites",
        "mechanism_ja": "ベンズイミダゾール系。β-チューブリンに結合し寄生虫の微小管重合を阻害",
        "species_info": {
            "dog": {"dose": "50 mg/kg PO q24h × 3-5日; ジアルジア: 50 mg/kg × 5日", "notes_ja": "回虫・鉤虫・鞭虫・ジアルジア・肺虫（Oslerus/Crenosoma）。安全マージン広い", "notes": "Roundworms, hookworms, whipworms, Giardia, lungworms. Wide safety margin"},
            "cat": {"dose": "50 mg/kg PO q24h × 3-5日", "notes_ja": "回虫・鉤虫・ジアルジア・肺虫（Aelurostrongylus）", "notes": "Roundworms, hookworms, Giardia, lungworm (Aelurostrongylus)"},
            "horse": {"dose": "5-10 mg/kg PO 1回; 子馬: 50 mg/kg（回虫）", "notes_ja": "小型円虫・回虫。子馬は高用量で回虫駆除", "notes": "Small strongyles, ascarids. Higher dose for foal ascarids"},
            "rabbit": {"dose": "20-50 mg/kg PO q24h × 5日", "notes_ja": "蟯虫・E. cuniculi（20 mg/kg × 28日）", "notes": "Pinworm, E. cuniculi (20 mg/kg × 28 days)"},
            "guinea_pig": {"dose": "20-50 mg/kg PO q24h × 5日", "notes_ja": "消化管寄生虫", "notes": "GI parasites"},
            "chinchilla": {"dose": "20-50 mg/kg PO q24h × 5日", "notes_ja": "消化管寄生虫・ジアルジア", "notes": "GI parasites, Giardia"},
            "hamster": {"dose": "20-50 mg/kg PO q24h × 5日", "notes_ja": "蟯虫", "notes": "Pinworm"},
            "hedgehog": {"dose": "20-50 mg/kg PO q24h × 5日", "notes_ja": "消化管寄生虫・肺虫", "notes": "GI parasites, lungworms"},
            "ferret": {"dose": "20-50 mg/kg PO q24h × 5日", "notes_ja": "消化管寄生虫", "notes": "GI parasites"},
            "bird": {"dose": "20-50 mg/kg PO q24h × 3-5日", "notes_ja": "回虫・毛細線虫", "notes": "Roundworms, Capillaria"},
            "reptile": {"dose": "50-100 mg/kg PO 1回; 14日後繰返し", "notes_ja": "線虫。原虫には効果なし", "notes": "Nematodes. Ineffective against protozoa"},
            "fish": {"dose": "2-5 mg/L 浴水 24-48h; PO 25-50 mg/kg", "notes_ja": "内部寄生虫（カマラヌス等）", "notes": "Internal parasites (Camallanus etc.)"},
            "sugar_glider": {"dose": "20-50 mg/kg PO q24h × 5日", "notes_ja": "消化管寄生虫", "notes": "GI parasites"},
            "degu": {"dose": "20-50 mg/kg PO q24h × 5日", "notes_ja": "蟯虫・ジアルジア", "notes": "Pinworm, Giardia"}
        },
        "side_effects": "Minimal; rare GI upset, bone marrow suppression at extreme doses",
        "side_effects_ja": "最小限。稀に消化器症状、極端な高用量で骨髄抑制",
        "contraindications": "First trimester pregnancy (teratogenic in some species at high doses)",
        "contraindications_ja": "妊娠初期（一部動物種で高用量催奇形性）",
        "drug_interactions": []
    },
    {
        "id": "metronidazole",
        "name": "Metronidazole",
        "name_ja": "メトロニダゾール（フラジール）",
        "category": "antibiotics",
        "mechanism": "Nitroimidazole; reduced form damages DNA of anaerobic bacteria and protozoa",
        "mechanism_ja": "ニトロイミダゾール系。還元型がDNAを損傷（嫌気性菌・原虫に有効）",
        "species_info": {
            "dog": {"dose": "10-15 mg/kg PO q12h; IBD: 10 mg/kg PO q12h", "notes_ja": "嫌気性菌感染・ジアルジア・IBD（免疫調節作用）。15 mg/kg超で神経毒性リスク", "notes": "Anaerobes, Giardia, IBD (immunomodulatory). Neurotoxicity risk >15 mg/kg"},
            "cat": {"dose": "10-15 mg/kg PO q12h", "notes_ja": "ジアルジア・IBD・嫌気性菌感染。苦味→投薬困難な場合あり", "notes": "Giardia, IBD, anaerobic infections. Bitter taste, compounding may help"},
            "horse": {"dose": "15-25 mg/kg PO q6-8h", "notes_ja": "嫌気性菌感染・クロストリジウム腸炎", "notes": "Anaerobic infections, clostridial enteritis"},
            "rabbit": {"dose": "20 mg/kg PO q12h", "notes_ja": "ジアルジア・嫌気性菌感染。腸内細菌叢への影響注意", "notes": "Giardia, anaerobic infections. Monitor GI flora"},
            "guinea_pig": {"dose": "20-40 mg/kg PO q12h", "notes_ja": "ジアルジア・嫌気性菌感染", "notes": "Giardia, anaerobic infections"},
            "chinchilla": {"dose": "10-20 mg/kg PO q12h", "notes_ja": "ジアルジア", "notes": "Giardia"},
            "ferret": {"dose": "15-20 mg/kg PO q12h", "notes_ja": "ヘリコバクター（3剤併用）・ジアルジア", "notes": "Helicobacter (triple therapy), Giardia"},
            "bird": {"dose": "20-50 mg/kg PO q12h", "notes_ja": "トリコモナス（カナリア口病）", "notes": "Trichomoniasis (canker)"},
            "reptile": {"dose": "20-40 mg/kg PO q48h", "notes_ja": "アメーバ症・嫌気性菌感染。48時間間隔", "notes": "Amebiasis, anaerobic infections. 48h interval"},
            "fish": {"dose": "5-10 mg/L 浴水 24h; PO 25-50 mg/kg", "notes_ja": "ヘキサミタ・スピロヌクレウス", "notes": "Hexamita, Spironucleus"},
            "hedgehog": {"dose": "20-25 mg/kg PO q12h", "notes_ja": "ジアルジア・嫌気性菌", "notes": "Giardia, anaerobes"},
            "hamster": {"dose": "20-40 mg/kg PO q12h", "notes_ja": "ジアルジア", "notes": "Giardia"}
        },
        "side_effects": "Neurotoxicity (ataxia, seizures, nystagmus at high doses), GI upset, hepatotoxicity",
        "side_effects_ja": "神経毒性（運動失調・痙攣・眼振、高用量時）、消化器症状、肝毒性",
        "contraindications": "CNS disease, hepatic failure, pregnancy (teratogenic)",
        "contraindications_ja": "CNS疾患、肝不全、妊娠（催奇形性）",
        "drug_interactions": [
            {"drug": "phenobarbital", "severity": "moderate", "description_ja": "メトロニダゾール代謝促進→効果減弱", "description": "Increased metronidazole metabolism"},
            {"drug": "warfarin", "severity": "moderate", "description_ja": "抗凝固効果増強", "description": "Enhanced anticoagulant effect"}
        ]
    },
    {
        "id": "clindamycin",
        "name": "Clindamycin",
        "name_ja": "クリンダマイシン（アンチローブ）",
        "category": "antibiotics",
        "mechanism": "Binds 50S ribosomal subunit; bacteriostatic (bactericidal at high concentrations). Good bone penetration",
        "mechanism_ja": "50Sリボソームサブユニットに結合。静菌的（高濃度で殺菌的）。骨移行性良好",
        "species_info": {
            "dog": {"dose": "5.5-11 mg/kg PO q12h; 深部感染: 11 mg/kg q12h", "notes_ja": "口腔感染・骨髄炎・膿皮症・トキソプラズマ。骨組織への移行性良好", "notes": "Dental infections, osteomyelitis, pyoderma, toxoplasmosis. Good bone penetration"},
            "cat": {"dose": "5.5-11 mg/kg PO q12h; トキソプラズマ: 12.5 mg/kg q12h", "notes_ja": "トキソプラズマ症・口腔感染・膿皮症。食道狭窄予防にwater chaser", "notes": "Toxoplasmosis, dental infections. Give with water to prevent esophageal stricture"},
            "rabbit": {"dose": "使用注意（致死性腸炎リスク）", "notes_ja": "ウサギではClostridium関連腸炎リスク→経口投与は原則避ける", "notes": "CAUTION: Risk of fatal Clostridium enteritis in rabbits. Avoid oral use"},
            "ferret": {"dose": "5.5-11 mg/kg PO q12h", "notes_ja": "骨感染・口腔感染", "notes": "Bone infections, dental infections"},
            "bird": {"dose": "25-50 mg/kg PO q8-12h", "notes_ja": "嫌気性菌感染", "notes": "Anaerobic infections"}
        },
        "side_effects": "GI upset, esophageal stricture (cats, dry capsules), pseudomembranous colitis (rare)",
        "side_effects_ja": "消化器症状、食道狭窄（猫、乾燥カプセル）、偽膜性大腸炎（稀）",
        "contraindications": "Rabbits/hamsters/guinea pigs (oral - fatal enteritis risk), neonates",
        "contraindications_ja": "ウサギ/ハムスター/モルモット（経口 — 致死性腸炎リスク）、新生仔",
        "drug_interactions": [
            {"drug": "erythromycin", "severity": "major", "description_ja": "同一結合部位で拮抗", "description": "Antagonism at same binding site"},
            {"drug": "neuromuscular_blockers", "severity": "moderate", "description_ja": "神経筋遮断増強", "description": "Enhanced neuromuscular blockade"}
        ]
    },
    {
        "id": "enrofloxacin",
        "name": "Enrofloxacin (Baytril)",
        "name_ja": "エンロフロキサシン（バイトリル）",
        "category": "antibiotics",
        "mechanism": "Fluoroquinolone; inhibits DNA gyrase and topoisomerase IV. Concentration-dependent bactericidal",
        "mechanism_ja": "フルオロキノロン系。DNAジャイレースとトポイソメラーゼIVを阻害。濃度依存性殺菌",
        "species_info": {
            "dog": {"dose": "5-20 mg/kg PO/IM q24h", "notes_ja": "UTI・呼吸器・皮膚・骨感染。成長期の犬では関節軟骨障害リスク", "notes": "UTI, respiratory, skin, bone infections. Cartilage damage risk in growing dogs"},
            "cat": {"dose": "5 mg/kg PO q24h（5mg/kg超は禁忌→網膜毒性）", "notes_ja": "猫は5mg/kg/dayを超えない！急性網膜変性・失明リスク", "notes": "NEVER exceed 5 mg/kg/day in cats! Acute retinal degeneration/blindness risk"},
            "horse": {"dose": "5-7.5 mg/kg PO/IV q24h", "notes_ja": "呼吸器感染・胸膜肺炎。子馬は関節軟骨障害→成長期は避ける", "notes": "Respiratory infections, pleuropneumonia. Avoid in growing foals (cartilage)"},
            "rabbit": {"dose": "5-20 mg/kg PO/SC q12-24h", "notes_ja": "パスツレラ・UTI・呼吸器感染", "notes": "Pasteurella, UTI, respiratory infections"},
            "guinea_pig": {"dose": "5-10 mg/kg PO/SC q12h", "notes_ja": "UTI・呼吸器感染", "notes": "UTI, respiratory infections"},
            "ferret": {"dose": "5-10 mg/kg PO q12h", "notes_ja": "UTI・呼吸器感染", "notes": "UTI, respiratory infections"},
            "bird": {"dose": "15-30 mg/kg PO/IM q12h", "notes_ja": "グラム陰性菌感染・慢性感染。飲水投与可", "notes": "Gram-negative, chronic infections. Can add to drinking water"},
            "reptile": {"dose": "5-10 mg/kg PO/IM q24h", "notes_ja": "細菌感染。POTZ内で投与", "notes": "Bacterial infections. Dose within POTZ"},
            "hedgehog": {"dose": "5-10 mg/kg PO q12h", "notes_ja": "UTI・呼吸器感染", "notes": "UTI, respiratory infections"},
            "hamster": {"dose": "5-10 mg/kg PO q12h", "notes_ja": "細菌感染", "notes": "Bacterial infections"},
            "chinchilla": {"dose": "5-15 mg/kg PO q12h", "notes_ja": "細菌感染", "notes": "Bacterial infections"},
            "fish": {"dose": "5-10 mg/kg PO/IM q24h", "notes_ja": "細菌感染", "notes": "Bacterial infections"}
        },
        "side_effects": "Cartilage erosion (growing animals), retinal degeneration (cats), GI upset, CNS excitation",
        "side_effects_ja": "関節軟骨びらん（成長期動物）、網膜変性（猫）、消化器症状、CNS興奮",
        "contraindications": "Growing animals <1 year (large breed dogs), cats >5 mg/kg/day, seizure disorders",
        "contraindications_ja": "1歳未満の成長期動物（大型犬）、猫で5mg/kg/day超、てんかん",
        "drug_interactions": [
            {"drug": "sucralfate", "severity": "major", "description_ja": "エンロフロキサシン吸収を著明に低下（2時間空ける）", "description": "Markedly decreased absorption (separate by 2h)"},
            {"drug": "theophylline", "severity": "moderate", "description_ja": "テオフィリン血中濃度上昇", "description": "Increased theophylline levels"},
            {"drug": "nsaids", "severity": "moderate", "description_ja": "CNS刺激増強→痙攣リスク", "description": "Enhanced CNS stimulation, seizure risk"}
        ]
    },
    {
        "id": "amoxicillin_clavulanate",
        "name": "Amoxicillin/Clavulanic Acid",
        "name_ja": "アモキシシリン/クラブラン酸（クラバモックス）",
        "category": "antibiotics",
        "mechanism": "Amoxicillin (cell wall synthesis inhibitor) + clavulanate (β-lactamase inhibitor). Broadens amoxicillin spectrum",
        "mechanism_ja": "アモキシシリン（細胞壁合成阻害）＋クラブラン酸（βラクタマーゼ阻害）。アモキシシリンのスペクトルを拡大",
        "species_info": {
            "dog": {"dose": "12.5-25 mg/kg PO q12h", "notes_ja": "UTI・皮膚感染・口腔感染・呼吸器感染。βラクタマーゼ産生菌に有効", "notes": "UTI, skin, dental, respiratory infections. Effective against β-lactamase producers"},
            "cat": {"dose": "12.5-25 mg/kg PO q12h", "notes_ja": "上部呼吸器感染・UTI・口内炎", "notes": "URI, UTI, stomatitis"},
            "rabbit": {"dose": "12.5-20 mg/kg PO q12h", "notes_ja": "パスツレラ・UTI。経口βラクタムはウサギで比較的安全", "notes": "Pasteurella, UTI. Oral β-lactams relatively safe in rabbits"},
            "guinea_pig": {"dose": "12.5-25 mg/kg PO q12h", "notes_ja": "UTI・呼吸器感染。ペニシリン注射は禁忌だが経口は比較的安全", "notes": "UTI, respiratory. Injectable penicillin contraindicated but oral relatively safe"},
            "ferret": {"dose": "12.5-25 mg/kg PO q12h", "notes_ja": "ヘリコバクター（3剤併用）・呼吸器感染", "notes": "Helicobacter (triple therapy), respiratory infections"},
            "bird": {"dose": "125 mg/kg PO q12h", "notes_ja": "グラム陽性・陰性菌感染", "notes": "Gram-positive and negative infections"},
            "hedgehog": {"dose": "12.5-25 mg/kg PO q12h", "notes_ja": "呼吸器・皮膚感染", "notes": "Respiratory, skin infections"},
            "hamster": {"dose": "20 mg/kg PO q12h", "notes_ja": "細菌感染。注意：注射は腸炎リスク", "notes": "Bacterial infections. CAUTION: injectable may cause enteritis"},
            "reptile": {"dose": "データ限定", "notes_ja": "使用データ限定的", "notes": "Limited data"}
        },
        "side_effects": "GI upset (diarrhea, vomiting), allergic reaction, dysbiosis",
        "side_effects_ja": "消化器症状（下痢・嘔吐）、アレルギー反応、ディスバイオシス",
        "contraindications": "Penicillin allergy, hamsters/guinea pigs (injectable form)",
        "contraindications_ja": "ペニシリンアレルギー、ハムスター/モルモット（注射剤）",
        "drug_interactions": [
            {"drug": "methotrexate", "severity": "moderate", "description_ja": "メトトレキサート排泄遅延", "description": "Delayed methotrexate excretion"}
        ]
    },
    {
        "id": "doxycycline",
        "name": "Doxycycline",
        "name_ja": "ドキシサイクリン（ビブラマイシン）",
        "category": "antibiotics",
        "mechanism": "Tetracycline; inhibits 30S ribosomal subunit. Good intracellular penetration",
        "mechanism_ja": "テトラサイクリン系。30Sリボソームサブユニットを阻害。細胞内移行性良好",
        "species_info": {
            "dog": {"dose": "5-10 mg/kg PO q12h", "notes_ja": "リケッチア（エーリキア・アナプラズマ）・ボレリア・ブルセラ・呼吸器感染・歯周病", "notes": "Rickettsial (Ehrlichia, Anaplasma), Borrelia, Brucella, respiratory, periodontal"},
            "cat": {"dose": "5-10 mg/kg PO q12h; ヘモプラズマ: 10 mg/kg q12h × 28日", "notes_ja": "ヘモプラズマ・クラミジア・バルトネラ・上部呼吸器感染。水で流して食道狭窄予防", "notes": "Hemoplasma, Chlamydia, Bartonella, URI. Follow with water to prevent esophageal stricture"},
            "horse": {"dose": "10 mg/kg PO q12h", "notes_ja": "子馬のR. equi（+アジスロマイシン）・ピロプラズマ・EPM補助", "notes": "Foal R. equi (+azithromycin), piroplasmosis, EPM adjunct"},
            "rabbit": {"dose": "2.5-5 mg/kg PO q12h", "notes_ja": "パスツレラ・呼吸器感染", "notes": "Pasteurella, respiratory infections"},
            "guinea_pig": {"dose": "2.5-5 mg/kg PO q12h", "notes_ja": "呼吸器感染", "notes": "Respiratory infections"},
            "bird": {"dose": "25-50 mg/kg PO q12h", "notes_ja": "クラミジア症（オウム病）第一選択。45日間", "notes": "Chlamydiosis (psittacosis) first-line. 45 days treatment"},
            "reptile": {"dose": "2.5-10 mg/kg PO q24-48h", "notes_ja": "マイコプラズマ・呼吸器感染", "notes": "Mycoplasma, respiratory infections"},
            "ferret": {"dose": "5-10 mg/kg PO q12h", "notes_ja": "ヘリコバクター併用・呼吸器感染", "notes": "Helicobacter combination, respiratory infections"},
            "hedgehog": {"dose": "2.5-5 mg/kg PO q12h", "notes_ja": "呼吸器感染", "notes": "Respiratory infections"},
            "hamster": {"dose": "2.5-5 mg/kg PO q12h", "notes_ja": "呼吸器感染", "notes": "Respiratory infections"},
            "chinchilla": {"dose": "2.5-5 mg/kg PO q12h", "notes_ja": "呼吸器感染", "notes": "Respiratory infections"},
            "fish": {"dose": "2.5-5 mg/L 浴水 5-7日", "notes_ja": "細菌感染", "notes": "Bacterial infections"}
        },
        "side_effects": "GI upset, esophageal stricture (cats), photosensitivity, tooth discoloration (neonates)",
        "side_effects_ja": "消化器症状、食道狭窄（猫）、光過敏、歯牙変色（新生仔）",
        "contraindications": "Pregnancy (tooth/bone effects), neonates, severe hepatic disease",
        "contraindications_ja": "妊娠（歯/骨への影響）、新生仔、重度肝疾患",
        "drug_interactions": [
            {"drug": "antacids", "severity": "major", "description_ja": "吸収を著明に低下（2時間空ける）", "description": "Markedly decreased absorption (separate by 2h)"},
            {"drug": "phenobarbital", "severity": "moderate", "description_ja": "ドキシサイクリン代謝促進", "description": "Increased doxycycline metabolism"},
            {"drug": "sucralfate", "severity": "major", "description_ja": "吸収低下", "description": "Decreased absorption"}
        ]
    },
    {
        "id": "azithromycin",
        "name": "Azithromycin",
        "name_ja": "アジスロマイシン（ジスロマック）",
        "category": "antibiotics",
        "mechanism": "Azalide (macrolide subclass); binds 50S ribosomal subunit. Excellent tissue penetration, long half-life",
        "mechanism_ja": "アザライド系（マクロライドのサブクラス）。50Sリボソームに結合。組織移行性良好、半減期長い",
        "species_info": {
            "dog": {"dose": "5-10 mg/kg PO q24h × 3日、以後q48-72h", "notes_ja": "バベシア（+アトバコン）・呼吸器感染・パピローマ。長い組織半減期", "notes": "Babesia (+atovaquone), respiratory, papilloma. Long tissue half-life"},
            "cat": {"dose": "5-10 mg/kg PO q24h × 3日、以後q48-72h", "notes_ja": "バルトネラ・上部呼吸器感染複合・トキソプラズマ代替", "notes": "Bartonella, URI complex, toxoplasmosis alternative"},
            "horse": {"dose": "10 mg/kg PO q24h × 5日、以後q48h", "notes_ja": "子馬のR. equi肺炎（+リファンピシン）", "notes": "Foal R. equi pneumonia (+rifampin)"},
            "rabbit": {"dose": "15-30 mg/kg PO q24h", "notes_ja": "パスツレラ・呼吸器感染", "notes": "Pasteurella, respiratory infections"},
            "bird": {"dose": "40-50 mg/kg PO q24h", "notes_ja": "クラミジア症の代替（ドキシサイクリンが第一選択）", "notes": "Chlamydiosis alternative (doxycycline is first-line)"},
            "reptile": {"dose": "10 mg/kg PO q48-72h", "notes_ja": "呼吸器感染・マイコバクテリア", "notes": "Respiratory infections, mycobacteria"},
            "guinea_pig": {"dose": "15-25 mg/kg PO q24h", "notes_ja": "呼吸器感染", "notes": "Respiratory infections"},
            "ferret": {"dose": "5-10 mg/kg PO q24h", "notes_ja": "呼吸器感染", "notes": "Respiratory infections"},
            "hedgehog": {"dose": "5-10 mg/kg PO q24h", "notes_ja": "呼吸器感染", "notes": "Respiratory infections"}
        },
        "side_effects": "GI upset, hepatotoxicity (rare), ototoxicity (rare)",
        "side_effects_ja": "消化器症状、肝毒性（稀）、耳毒性（稀）",
        "contraindications": "Macrolide allergy, severe hepatic disease",
        "contraindications_ja": "マクロライドアレルギー、重度肝疾患",
        "drug_interactions": [
            {"drug": "ciclosporin", "severity": "moderate", "description_ja": "シクロスポリン血中濃度上昇", "description": "Increased ciclosporin levels"}
        ]
    },
    {
        "id": "acepromazine",
        "name": "Acepromazine",
        "name_ja": "アセプロマジン（ベトランキル）",
        "category": "anesthetics",
        "mechanism": "Phenothiazine; D2 dopamine receptor antagonist. Tranquilizer (not analgesic)",
        "mechanism_ja": "フェノチアジン系。D2ドパミン受容体拮抗薬。トランキライザー（鎮痛作用なし）",
        "species_info": {
            "dog": {"dose": "0.01-0.05 mg/kg IV/IM; 最大用量3mg（体重不問）", "notes_ja": "前投薬・鎮静。低用量で十分。用量反応プラトーあり。短頭種は減量", "notes": "Premedication, sedation. Low doses sufficient. Dose-response plateau. Reduce in brachycephalics"},
            "cat": {"dose": "0.01-0.05 mg/kg IV/IM", "notes_ja": "猫の鎮静。低用量で十分", "notes": "Feline sedation. Low doses sufficient"},
            "horse": {"dose": "0.02-0.05 mg/kg IV/IM", "notes_ja": "鎮静。陰茎脱出リスク（種牡馬で注意）", "notes": "Sedation. Penile prolapse risk (caution in stallions)"},
            "ferret": {"dose": "0.1-0.25 mg/kg IM", "notes_ja": "フェレットの鎮静前投薬", "notes": "Ferret sedation premedication"}
        },
        "side_effects": "Hypotension, hypothermia, penile prolapse (horses), seizure threshold lowering",
        "side_effects_ja": "低血圧、低体温、陰茎脱出（馬）、痙攣閾値低下",
        "contraindications": "Epilepsy, hypovolemia/shock, Boxers (breed sensitivity), MDR1 mutant breeds",
        "contraindications_ja": "てんかん、循環血液量減少/ショック、ボクサー（品種感受性）、MDR1変異品種",
        "drug_interactions": [
            {"drug": "epinephrine", "severity": "moderate", "description_ja": "α遮断作用により逆説的低血圧（epinephrine reversal）", "description": "Paradoxical hypotension due to alpha blockade (epinephrine reversal)"},
            {"drug": "opioids", "severity": "moderate", "description_ja": "鎮静・呼吸抑制の相加", "description": "Additive sedation and respiratory depression"}
        ]
    },
    {
        "id": "diazepam",
        "name": "Diazepam (Valium)",
        "name_ja": "ジアゼパム（セルシン）",
        "category": "anesthetics",
        "mechanism": "Benzodiazepine; enhances GABA-A receptor activity. Anxiolytic, muscle relaxant, anticonvulsant",
        "mechanism_ja": "ベンゾジアゼピン系。GABA-A受容体活性を増強。抗不安・筋弛緩・抗痙攣",
        "species_info": {
            "dog": {"dose": "てんかん重積: 0.5-1 mg/kg IV; 鎮静前投薬: 0.2-0.5 mg/kg IV", "notes_ja": "てんかん重積の第一選択。麻酔導入時のco-induction。筋弛緩", "notes": "First-line status epilepticus. Co-induction agent. Muscle relaxation"},
            "cat": {"dose": "てんかん重積: 0.5-1 mg/kg IV; 食欲刺激: 0.05-0.15 mg/kg IV", "notes_ja": "てんかん重積・食欲刺激（IV）。経口投与は肝壊死リスク→経口ならオキサゼパム", "notes": "Status epilepticus, appetite stimulation (IV). Oral use risks hepatic necrosis → use oxazepam PO"},
            "horse": {"dose": "0.02-0.1 mg/kg IV", "notes_ja": "新生子馬の痙攣。成馬は倒れるリスク→通常α2と併用", "notes": "Neonatal seizures. Adults may recumbent → usually with α2 agonist"},
            "rabbit": {"dose": "1-3 mg/kg IV/IM/IN", "notes_ja": "痙攣管理・鎮静補助", "notes": "Seizure management, sedation adjunct"},
            "bird": {"dose": "0.5-1 mg/kg IM/IV", "notes_ja": "痙攣管理", "notes": "Seizure management"},
            "reptile": {"dose": "0.5-1 mg/kg IM", "notes_ja": "痙攣管理・筋弛緩", "notes": "Seizure management, muscle relaxation"}
        },
        "side_effects": "Sedation, paradoxical excitation (cats, dogs), hepatic necrosis (cats PO), respiratory depression",
        "side_effects_ja": "鎮静、奇異性興奮（猫・犬）、肝壊死（猫経口）、呼吸抑制",
        "contraindications": "Hepatic disease (cats especially), neonates, respiratory depression",
        "contraindications_ja": "肝疾患（特に猫）、新生仔、呼吸抑制",
        "drug_interactions": [
            {"drug": "opioids", "severity": "moderate", "description_ja": "呼吸抑制の相加", "description": "Additive respiratory depression"},
            {"drug": "cimetidine", "severity": "moderate", "description_ja": "ジアゼパム代謝遅延", "description": "Delayed diazepam metabolism"}
        ]
    },
    {
        "id": "meloxicam",
        "name": "Meloxicam (Metacam)",
        "name_ja": "メロキシカム（メタカム）",
        "category": "nsaids",
        "mechanism": "Preferential COX-2 inhibitor; anti-inflammatory, analgesic, antipyretic",
        "mechanism_ja": "COX-2優先的阻害薬。抗炎症・鎮痛・解熱",
        "species_info": {
            "dog": {"dose": "初回0.2 mg/kg PO/SC, 以後0.1 mg/kg PO q24h", "notes_ja": "OA・術後疼痛・炎症。消化管保護のため食事と一緒に投与", "notes": "OA, post-op pain, inflammation. Give with food for GI protection"},
            "cat": {"dose": "初回0.1 mg/kg SC, 以後0.05 mg/kg PO q24h", "notes_ja": "猫のOA疼痛に長期低用量が認可（一部の国）。腎機能モニタリング必須", "notes": "Long-term low-dose approved for feline OA in some countries. Monitor renal function"},
            "horse": {"dose": "0.6 mg/kg IV/PO q24h", "notes_ja": "筋骨格疼痛・軟部組織炎症", "notes": "Musculoskeletal pain, soft tissue inflammation"},
            "rabbit": {"dose": "0.3-0.6 mg/kg PO/SC q24h", "notes_ja": "術後疼痛・慢性疼痛", "notes": "Post-op pain, chronic pain"},
            "guinea_pig": {"dose": "0.2-0.5 mg/kg PO q24h", "notes_ja": "術後疼痛", "notes": "Post-op pain"},
            "ferret": {"dose": "0.2 mg/kg PO/SC q24h", "notes_ja": "疼痛・炎症", "notes": "Pain, inflammation"},
            "bird": {"dose": "0.5-1 mg/kg PO/IM q12-24h", "notes_ja": "鳥類の疼痛管理", "notes": "Avian pain management"},
            "reptile": {"dose": "0.1-0.3 mg/kg PO/IM q24-48h", "notes_ja": "爬虫類の疼痛管理", "notes": "Reptilian pain management"},
            "hedgehog": {"dose": "0.2-0.5 mg/kg PO q24h", "notes_ja": "疼痛管理", "notes": "Pain management"},
            "hamster": {"dose": "0.2-0.5 mg/kg PO q24h", "notes_ja": "術後疼痛", "notes": "Post-op pain"},
            "chinchilla": {"dose": "0.2-0.5 mg/kg PO q24h", "notes_ja": "疼痛管理", "notes": "Pain management"},
            "sugar_glider": {"dose": "0.2 mg/kg PO q24h", "notes_ja": "疼痛管理", "notes": "Pain management"},
            "degu": {"dose": "0.2-0.5 mg/kg PO q24h", "notes_ja": "疼痛管理", "notes": "Pain management"}
        },
        "side_effects": "GI ulceration, renal injury, hepatotoxicity, decreased platelet function",
        "side_effects_ja": "消化管潰瘍、腎障害、肝毒性、血小板機能低下",
        "contraindications": "Dehydration, renal disease, GI ulceration, concurrent corticosteroids/other NSAIDs",
        "contraindications_ja": "脱水、腎疾患、消化管潰瘍、コルチコステロイド/他のNSAID併用",
        "drug_interactions": [
            {"drug": "corticosteroids", "severity": "major", "description_ja": "消化管潰瘍リスクの著明な増加", "description": "Markedly increased GI ulceration risk"},
            {"drug": "ace_inhibitors", "severity": "moderate", "description_ja": "降圧効果減弱・腎機能悪化", "description": "Attenuated antihypertensive effect, worsened renal function"},
            {"drug": "furosemide", "severity": "moderate", "description_ja": "利尿効果減弱", "description": "Attenuated diuretic effect"}
        ]
    }
]
