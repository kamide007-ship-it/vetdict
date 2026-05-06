"""Drug batch 15: Oncology, Antiparasitic, Reproductive & Misc drugs (30 drugs)."""

DRUGS_BATCH_15: list[dict] = [
    {
        "id": "carboplatin",
        "name": "Carboplatin",
        "name_ja": "カルボプラチン",
        "category": "antineoplastic",
        "mechanism": "Platinum-based alkylating agent; forms DNA crosslinks inhibiting replication and transcription. Less nephrotoxic than cisplatin, preferred for veterinary oncology",
        "mechanism_ja": "白金系アルキル化剤；DNA架橋を形成し複製と転写を阻害。シスプラチンより腎毒性が少なく、獣医腫瘍学で推奨",
        "species_info": {
            "dog": {"dose": "300 mg/m² IV q21d (or area-under-curve dosing)", "notes": "Osteosarcoma adjuvant, melanoma, carcinomas, mesothelioma; CBC day 10-14 for nadir", "notes_ja": "骨肉腫アジュバント、メラノーマ、癌腫、中皮腫；CBC10-14日目にナディア確認"},
            "cat": {"dose": "200-240 mg/m² IV q21d", "notes": "SCC, vaccine-associated sarcoma, mammary carcinoma; cats more myelosuppression-sensitive", "notes_ja": "SCC、ワクチン関連肉腫、乳腺癌；猫は骨髄抑制に感受性が高い"},
            "bird": {"dose": "5 mg/kg IV q28d or intralesional", "notes": "SCC in psittacines; intralesional for accessible tumors", "notes_ja": "オウム目のSCC；到達可能な腫瘍には腫瘍内投与"},
            "ferret": {"dose": "50 mg/m² IV q21d", "notes": "Lymphoma protocol component", "notes_ja": "リンパ腫プロトコルの一成分"}
        },
        "side_effects": ["Myelosuppression (dose-limiting)", "GI upset", "Nephrotoxicity (less than cisplatin)", "Ototoxicity"],
        "side_effects_ja": ["骨髄抑制（用量制限毒性）", "消化器障害", "腎毒性（シスプラチンより少ない）", "聴覚毒性"],
        "contraindications": "Severe myelosuppression, severe renal impairment, cats with FeLV (poor marrow reserve)",
        "contraindications_ja": "重度骨髄抑制、重度腎障害、FeLV猫（骨髄予備能低下）",
        "drug_interactions": [
            {"drug": "Aminoglycosides", "severity": "major", "description": "Additive nephro/ototoxicity", "description_ja": "相加的腎/聴覚毒性"},
            {"drug": "NSAIDs", "severity": "moderate", "description": "Increased nephrotoxicity risk; ensure hydration", "description_ja": "腎毒性リスク増加；水和確保"},
            {"drug": "Phenobarbital", "severity": "moderate", "description": "May increase carboplatin clearance reducing efficacy", "description_ja": "カルボプラチンクリアランス増加で効果減弱の可能性"}
        ]
    },
    {
        "id": "mitoxantrone",
        "name": "Mitoxantrone",
        "name_ja": "ミトキサントロン",
        "category": "antineoplastic",
        "mechanism": "Anthracenedione; intercalates DNA and inhibits topoisomerase II. Less cardiotoxic than doxorubicin, making it preferred when cardiac risk is a concern",
        "mechanism_ja": "アントラセンジオン；DNAにインターカレートしトポイソメラーゼIIを阻害。ドキソルビシンより心毒性が少なく、心リスク懸念時に推奨",
        "species_info": {
            "dog": {"dose": "5-6 mg/m² IV q21d", "notes": "Lymphoma (rescue), TCC/transitional cell carcinoma, hemangiosarcoma; less alopecia than doxorubicin", "notes_ja": "リンパ腫（レスキュー）、移行上皮癌、血管肉腫；ドキソルビシンより脱毛少ない"},
            "cat": {"dose": "6-6.5 mg/m² IV q21d", "notes": "Lymphoma, mammary carcinoma; well tolerated in cats", "notes_ja": "リンパ腫、乳腺癌；猫での忍容性良好"}
        },
        "side_effects": ["Myelosuppression", "GI upset (milder than doxorubicin)", "Blue-green discoloration of urine/sclera", "Cardiotoxicity (cumulative, less than doxorubicin)"],
        "side_effects_ja": ["骨髄抑制", "消化器障害（ドキソルビシンより軽度）", "尿/強膜の青緑色変色", "心毒性（累積性、ドキソルビシンより少ない）"],
        "contraindications": "Pre-existing myelosuppression, prior cumulative doxorubicin at max dose",
        "contraindications_ja": "既存の骨髄抑制、ドキソルビシン最大累積量の既投与",
        "drug_interactions": [
            {"drug": "Other myelosuppressive agents", "severity": "major", "description": "Additive bone marrow suppression", "description_ja": "相加的骨髄抑制"},
            {"drug": "Live vaccines", "severity": "major", "description": "Risk of disseminated infection in immunosuppressed patient", "description_ja": "免疫抑制患者での播種性感染リスク"}
        ]
    },
    {
        "id": "melphalan",
        "name": "Melphalan",
        "name_ja": "メルファラン",
        "category": "antineoplastic",
        "mechanism": "Nitrogen mustard alkylating agent; forms DNA crosslinks disrupting replication. Well-absorbed orally, used in chronic low-dose protocols",
        "mechanism_ja": "ナイトロジェンマスタード系アルキル化剤；DNA架橋を形成し複製を障害。経口吸収良好で慢性低用量プロトコルに使用",
        "species_info": {
            "dog": {"dose": "0.1 mg/kg PO q24h × 10d then rest 10d (pulse); or 7 mg/m² PO q24h × 5d q21d", "notes": "Multiple myeloma (with prednisolone), hemangiosarcoma adjunct", "notes_ja": "多発性骨髄腫（プレドニゾロン併用）、血管肉腫補助"},
            "cat": {"dose": "0.1-0.2 mg/kg PO q24h × 10d rest 10d; or 2 mg/cat q48h", "notes": "Multiple myeloma, mast cell tumor (oral protocol)", "notes_ja": "多発性骨髄腫、肥満細胞腫（経口プロトコル）"}
        },
        "side_effects": ["Myelosuppression (delayed, cumulative)", "GI upset", "Secondary leukemia (long-term)"],
        "side_effects_ja": ["骨髄抑制（遅発性、累積性）", "消化器障害", "二次性白血病（長期）"],
        "contraindications": "Severe pre-existing myelosuppression, prior extensive radiation",
        "contraindications_ja": "重度の既存骨髄抑制、広範な既往放射線照射",
        "drug_interactions": [
            {"drug": "Other alkylating agents", "severity": "major", "description": "Cumulative myelotoxicity", "description_ja": "累積性骨髄毒性"},
            {"drug": "Cyclosporine", "severity": "moderate", "description": "Increased nephrotoxicity risk", "description_ja": "腎毒性リスク増加"}
        ]
    },
    {
        "id": "palladia",
        "name": "Masitinib (Masivet/Kinavet)",
        "name_ja": "マシチニブ（マシベット）",
        "category": "antineoplastic",
        "mechanism": "Tyrosine kinase inhibitor targeting c-Kit, PDGFR, FGFR3; inhibits mast cell proliferation and tumor angiogenesis. Oral targeted therapy for non-resectable mast cell tumors",
        "mechanism_ja": "c-Kit・PDGFR・FGFR3を標的とするチロシンキナーゼ阻害薬；肥満細胞増殖と腫瘍血管新生を阻害。切除不能肥満細胞腫の経口分子標的療法",
        "species_info": {
            "dog": {"dose": "12.5 mg/kg PO q24h (with food)", "notes": "Non-resectable Grade II/III mast cell tumors with confirmed c-Kit mutation; EMA-approved", "notes_ja": "c-Kit変異確認済み切除不能Grade II/III肥満細胞腫；EMA承認"},
            "cat": {"dose": "50 mg/cat PO q24h (off-label)", "notes": "Feline mast cell tumors; very limited data", "notes_ja": "猫肥満細胞腫；データ非常に限定的"}
        },
        "side_effects": ["Diarrhea", "Vomiting", "Neutropenia", "Protein-losing nephropathy", "Edema", "Hemolytic anemia (rare)"],
        "side_effects_ja": ["下痢", "嘔吐", "好中球減少症", "蛋白漏出性腎症", "浮腫", "溶血性貧血（稀）"],
        "contraindications": "Hepatic impairment (ALT >3x ULN), severe renal disease, concurrent NSAID (GI bleeding risk), anemia",
        "contraindications_ja": "肝障害（ALT>正常上限3倍）、重度腎疾患、NSAID併用（消化管出血リスク）、貧血",
        "drug_interactions": [
            {"drug": "NSAIDs", "severity": "major", "description": "Increased GI ulceration and bleeding risk", "description_ja": "消化管潰瘍・出血リスク増加"},
            {"drug": "CYP3A4 inhibitors", "severity": "moderate", "description": "May increase masitinib levels", "description_ja": "マシチニブ濃度上昇の可能性"}
        ]
    },
    {
        "id": "l_asparaginase",
        "name": "L-Asparaginase",
        "name_ja": "L-アスパラギナーゼ",
        "category": "antineoplastic",
        "mechanism": "Enzyme that depletes asparagine; lymphoid tumor cells lack asparagine synthetase and cannot survive without exogenous asparagine. Selectively starves lymphoblasts",
        "mechanism_ja": "アスパラギンを枯渇させる酵素；リンパ系腫瘍細胞はアスパラギン合成酵素を欠き、外因性アスパラギンなしで生存できない。リンパ芽球を選択的に飢餓させる",
        "species_info": {
            "dog": {"dose": "400 IU/kg IM or 10,000-20,000 IU/m² IM (never IV first dose)", "notes": "Lymphoma induction (CHOP week 1); anaphylaxis risk increases with repeat doses", "notes_ja": "リンパ腫導入（CHOP第1週）；反復投与でアナフィラキシーリスク増加"},
            "cat": {"dose": "400 IU/kg IM", "notes": "Feline lymphoma (especially GI lymphoma induction); same anaphylaxis precautions", "notes_ja": "猫リンパ腫（特にGIリンパ腫導入）；同様のアナフィラキシー予防策"},
            "ferret": {"dose": "400 IU/kg IM", "notes": "Ferret lymphoma protocol", "notes_ja": "フェレットリンパ腫プロトコル"}
        },
        "side_effects": ["Anaphylaxis (5-30% on re-exposure)", "Pancreatitis", "Coagulopathy (DIC)", "Hepatotoxicity", "Hyperglycemia"],
        "side_effects_ja": ["アナフィラキシー（再投与で5-30%）", "膵炎", "凝固障害（DIC）", "肝毒性", "高血糖"],
        "contraindications": "Previous anaphylaxis to L-asparaginase, active pancreatitis, severe hepatic disease, active thrombosis/DIC",
        "contraindications_ja": "L-アスパラギナーゼへの既往アナフィラキシー、活動性膵炎、重度肝疾患、活動性血栓症/DIC",
        "drug_interactions": [
            {"drug": "Vincristine", "severity": "moderate", "description": "Give vincristine before L-asparaginase (increased vincristine neurotoxicity if reversed)", "description_ja": "ビンクリスチンをL-アスパラギナーゼの前に投与（順序逆だとビンクリスチン神経毒性増加）"},
            {"drug": "Methotrexate", "severity": "major", "description": "Antagonizes methotrexate effect; cells need to be dividing for MTX to work", "description_ja": "メトトレキサート効果を拮抗；MTXは細胞分裂中に作用"}
        ]
    },
    {
        "id": "chlorambucil_low_dose",
        "name": "Chlorambucil (Metronomic)",
        "name_ja": "クロラムブシル（メトロノミック）",
        "category": "antineoplastic",
        "mechanism": "Nitrogen mustard alkylating agent at low continuous dose; anti-angiogenic and immunomodulatory metronomic effect rather than direct cytotoxicity. Targets tumor vasculature",
        "mechanism_ja": "低用量持続投与のナイトロジェンマスタード系アルキル化剤；直接的細胞毒性ではなく抗血管新生・免疫調節性メトロノミック効果。腫瘍血管系を標的",
        "species_info": {
            "dog": {"dose": "4-6 mg/m² PO q24h (metronomic); or pulse 20 mg/m² q14d (CLL)", "notes": "Small cell lymphoma, CLL, metronomic anti-angiogenic protocol; monitor CBC q2-4wk", "notes_ja": "小細胞型リンパ腫、CLL、メトロノミック抗血管新生プロトコル；CBC 2-4週毎モニタリング"},
            "cat": {"dose": "2 mg/cat PO q48-72h (CLL/low-grade lymphoma); 15 mg/m² pulse q14d", "notes": "Feline small-cell GI lymphoma (with prednisolone), CLL; very well tolerated long-term in cats", "notes_ja": "猫小細胞GIリンパ腫（プレドニゾロン併用）、CLL；猫で長期忍容性非常に良好"}
        },
        "side_effects": ["Myelosuppression (mild at metronomic doses)", "GI upset (rare)", "Secondary leukemia (very long-term)"],
        "side_effects_ja": ["骨髄抑制（メトロノミック用量では軽度）", "消化器障害（稀）", "二次性白血病（超長期）"],
        "contraindications": "Severe pre-existing cytopenias, active infection without antibiotic coverage",
        "contraindications_ja": "重度の既存血球減少症、抗菌薬カバーなしの活動性感染",
        "drug_interactions": [
            {"drug": "Other myelosuppressives", "severity": "moderate", "description": "Additive bone marrow suppression", "description_ja": "相加的骨髄抑制"},
            {"drug": "Live vaccines", "severity": "major", "description": "Disseminated infection risk", "description_ja": "播種性感染リスク"}
        ]
    },
    {
        "id": "epofolaner",
        "name": "Epofolaner (Zenrelia)",
        "name_ja": "エポフォラネル（ゼンレリア）",
        "category": "antiparasitic",
        "mechanism": "Novel isoxazoline ectoparasiticide; inhibits GABA-gated and glutamate-gated chloride channels in arthropod nervous system. Monthly oral flea/tick preventive for dogs",
        "mechanism_ja": "新規イソオキサゾリン系外部寄生虫駆除薬；節足動物神経系のGABA依存性・グルタミン酸依存性塩素チャネルを阻害。犬用月1回経口ノミ・ダニ予防薬",
        "species_info": {
            "dog": {"dose": "0.5 mg/kg PO monthly (chewable tablet)", "notes": "Flea and tick prevention; safe for MDR1 mutant dogs (no P-gp substrate concern); FDA 2024 approval", "notes_ja": "ノミ・ダニ予防；MDR1変異犬で安全（P-gp基質の懸念なし）；2024年FDA承認"},
            "cat": {"dose": "Not approved for cats", "notes": "Feline safety not established", "notes_ja": "猫の安全性未確立"}
        },
        "side_effects": ["Vomiting", "Diarrhea", "Lethargy", "Seizures (very rare, predisposed animals)"],
        "side_effects_ja": ["嘔吐", "下痢", "嗜眠", "痙攣（非常に稀、素因動物）"],
        "contraindications": "History of seizures (use with caution), severe hepatic disease, puppies <8 weeks",
        "contraindications_ja": "痙攣既往（慎重使用）、重度肝疾患、8週齢未満の子犬",
        "drug_interactions": [
            {"drug": "Other isoxazolines", "severity": "moderate", "description": "Do not combine different isoxazoline products", "description_ja": "異なるイソオキサゾリン製品を併用しない"},
            {"drug": "Seizure threshold-lowering drugs", "severity": "mild", "description": "Theoretical additive seizure risk in predisposed animals", "description_ja": "素因動物での理論的な相加的痙攣リスク"}
        ]
    },
    {
        "id": "lotilaner",
        "name": "Lotilaner (Credelio)",
        "name_ja": "ロチラネル（クレデリオ）",
        "category": "antiparasitic",
        "mechanism": "Isoxazoline ectoparasiticide; selectively inhibits arthropod GABA-gated chloride channels causing uncontrolled neurotransmission and parasite death. Rapid flea kill (<6h)",
        "mechanism_ja": "イソオキサゾリン系外部寄生虫駆除薬；節足動物のGABA依存性塩素チャネルを選択的に阻害し神経伝達制御不能と寄生虫死を惹起。速効性ノミ駆除（<6時間）",
        "species_info": {
            "dog": {"dose": "20-43 mg/kg PO monthly (chewable, give with food)", "notes": "Fleas, ticks (Ixodes, Dermacentor, Rhipicephalus, Amblyomma); very palatable beef-flavored", "notes_ja": "ノミ、ダニ（マダニ4属）；牛肉フレーバーで嗜好性良好"},
            "cat": {"dose": "6-24 mg/kg PO monthly (Credelio Cat)", "notes": "Feline flea/tick; one of few oral isoxazolines approved for cats", "notes_ja": "猫のノミ/ダニ；猫に承認された数少ない経口イソオキサゾリンの一つ"}
        },
        "side_effects": ["Vomiting", "Diarrhea", "Lethargy", "Weight loss (rare)", "Seizures (very rare)"],
        "side_effects_ja": ["嘔吐", "下痢", "嗜眠", "体重減少（稀）", "痙攣（非常に稀）"],
        "contraindications": "Seizure history (caution), <8 weeks or <2lb (dogs), <8 weeks or <2lb (cats)",
        "contraindications_ja": "痙攣既往（注意）、8週齢未満または体重0.9kg未満",
        "drug_interactions": [
            {"drug": "Other ectoparasiticides", "severity": "mild", "description": "Avoid stacking multiple isoxazoline-class products", "description_ja": "複数のイソオキサゾリン系製品の重複回避"}
        ]
    },
    {
        "id": "moxidectin_injectable",
        "name": "Moxidectin Injectable (ProHeart)",
        "name_ja": "モキシデクチン注射（プロハート）",
        "category": "antiparasitic",
        "mechanism": "Milbemycin class macrocyclic lactone in sustained-release microsphere formulation; prevents heartworm by eliminating L3/L4 larvae. Single injection provides 6 or 12 months protection",
        "mechanism_ja": "徐放性マイクロスフェア製剤のミルベマイシン系大環状ラクトン；L3/L4幼虫を駆除しフィラリアを予防。1回注射で6または12ヶ月間の防御",
        "species_info": {
            "dog": {"dose": "ProHeart 6: 0.17 mg/kg SC q6months; ProHeart 12: 0.5 mg/kg SC q12months", "notes": "Heartworm prevention (compliance guarantee); also treats hookworms. Must be administered by veterinarian", "notes_ja": "フィラリア予防（コンプライアンス保証）；鉤虫も治療。獣医師が投与必須"},
            "cat": {"dose": "Not approved for cats", "notes": "No feline sustained-release formulation; use topical moxidectin for cats", "notes_ja": "猫用徐放製剤なし；猫にはモキシデクチン外用薬を使用"}
        },
        "side_effects": ["Injection site reactions", "Vomiting", "Lethargy", "Anaphylaxis (rare)", "Diarrhea"],
        "side_effects_ja": ["注射部位反応", "嘔吐", "嗜眠", "アナフィラキシー（稀）", "下痢"],
        "contraindications": "Dogs <6 months, sick/debilitated/underweight dogs, known moxidectin hypersensitivity, heartworm-positive (must test negative first)",
        "contraindications_ja": "6ヶ月齢未満の犬、病気/衰弱/低体重犬、モキシデクチン過敏症既知、フィラリア陽性（事前に陰性確認必須）",
        "drug_interactions": [
            {"drug": "P-glycoprotein inhibitors", "severity": "major", "description": "May increase moxidectin CNS levels in MDR1 dogs; use ivermectin-sensitivity screening", "description_ja": "MDR1犬でモキシデクチンCNS濃度上昇の可能性；イベルメクチン感受性スクリーニング実施"}
        ]
    },
    {
        "id": "ponazuril",
        "name": "Ponazuril",
        "name_ja": "ポナズリル",
        "category": "antiparasitic",
        "mechanism": "Triazine antiprotozoal; inhibits apicoplast function and mitochondrial electron transport in Apicomplexa. Active metabolite of diclazuril. Coccidiostatic/coccidiocidal",
        "mechanism_ja": "トリアジン系抗原虫薬；アピコンプレックスのアピコプラスト機能とミトコンドリア電子伝達を阻害。ジクラズリルの活性代謝物。コクシジウム静止/殺滅作用",
        "species_info": {
            "dog": {"dose": "20-50 mg/kg PO q24h × 5-28d", "notes": "Neospora caninum, Toxoplasma, Hepatozoon, coccidiosis (Isospora)", "notes_ja": "ネオスポラ、トキソプラズマ、ヘパトゾーン、コクシジウム症"},
            "cat": {"dose": "20-50 mg/kg PO q24h × 5-28d", "notes": "Toxoplasma gondii (preferred over clindamycin for active infection), coccidiosis", "notes_ja": "トキソプラズマ（活動性感染にはクリンダマイシンより推奨）、コクシジウム症"},
            "horse": {"dose": "5-10 mg/kg PO q24h × 28d (or 15 mg/kg q24h × 7d loading)", "notes": "EPM (Sarcocystis neurona) — FDA-approved for horses (Marquis)", "notes_ja": "EPM（Sarcocystis neurona）— 馬でFDA承認（マーキス）"},
            "rabbit": {"dose": "20 mg/kg PO q24h × 14-28d", "notes": "E. cuniculi treatment (superior to fenbendazole in acute phase)", "notes_ja": "E. cuniculi治療（急性期ではフェンベンダゾールより優れる）"},
            "bird": {"dose": "30-50 mg/kg PO q24h × 3-5d", "notes": "Avian coccidiosis (Eimeria/Isospora)", "notes_ja": "鳥類コクシジウム症（アイメリア/イソスポラ）"},
            "reptile": {"dose": "30 mg/kg PO, repeat in 7d", "notes": "Coccidia in tortoises and lizards", "notes_ja": "リクガメとトカゲのコクシジウム"},
            "guinea_pig": {"dose": "20-30 mg/kg PO q24h × 5d", "notes": "Hepatic coccidiosis", "notes_ja": "肝コクシジウム症"}
        },
        "side_effects": ["Generally very well tolerated", "Loose stool (transient)", "Anorexia (rare)"],
        "side_effects_ja": ["一般に忍容性非常に良好", "軟便（一過性）", "食欲不振（稀）"],
        "contraindications": "None significant; not established safe in pregnant mares",
        "contraindications_ja": "特記すべき禁忌なし；妊娠馬での安全性未確立",
        "drug_interactions": [
            {"drug": "No significant interactions known", "severity": "mild", "description": "Very safe drug interaction profile", "description_ja": "薬物相互作用プロファイルは非常に安全"}
        ]
    },
    {
        "id": "eprinomectin",
        "name": "Eprinomectin",
        "name_ja": "エプリノメクチン",
        "category": "antiparasitic",
        "mechanism": "Avermectin endectocide; potentiates GABA/glutamate-gated chloride channels in nematodes and arthropods. Unique zero-milk withdrawal making it safe during lactation",
        "mechanism_ja": "アベルメクチン系内外寄生虫駆除薬；線虫と節足動物のGABA/グルタミン酸依存性塩素チャネルを増強。ミルク休薬期間ゼロのユニークな特性で泌乳期も安全",
        "species_info": {
            "dog": {"dose": "Not commonly used in dogs (other options preferred)", "notes": "Broadline (cat topical) contains eprinomectin; not standard for dogs alone", "notes_ja": "犬では一般に使用されない（他の選択肢推奨）；Broadline（猫外用）にエプリノメクチン含有"},
            "cat": {"dose": "0.5 mg/kg topical (as component of Broadline)", "notes": "GI nematodes (roundworm, hookworm) + heartworm prevention in combination product", "notes_ja": "消化管線虫（回虫・鉤虫）＋フィラリア予防を併用製品として"},
            "horse": {"dose": "0.2 mg/kg topical pour-on", "notes": "Equine GI nematodes; zero-milk withdrawal for lactating mares", "notes_ja": "馬消化管線虫；泌乳馬でミルク休薬期間ゼロ"}
        },
        "side_effects": ["Very well tolerated", "Local irritation at pour-on site", "Ataxia/depression (overdose)"],
        "side_effects_ja": ["忍容性非常に良好", "外用部位の局所刺激", "運動失調/沈鬱（過量）"],
        "contraindications": "MDR1 mutant dogs (same class concerns as ivermectin)",
        "contraindications_ja": "MDR1変異犬（イベルメクチンと同系統の懸念）",
        "drug_interactions": [
            {"drug": "P-glycoprotein inhibitors", "severity": "moderate", "description": "Increased CNS levels in MDR1 animals", "description_ja": "MDR1動物でCNS濃度増加"}
        ]
    },
    {
        "id": "monepantel",
        "name": "Monepantel (Zolvix)",
        "name_ja": "モネパンテル（ゾルビックス）",
        "category": "antiparasitic",
        "mechanism": "Amino-acetonitrile derivative (AAD); novel class of anthelmintic acting on nematode-specific nicotinic acetylcholine receptor subunit (DEG-3/DES-2). Effective against multi-drug resistant GI nematodes",
        "mechanism_ja": "アミノアセトニトリル誘導体（AAD）；線虫特異的ニコチン性アセチルコリン受容体サブユニット（DEG-3/DES-2）に作用する新規クラスの駆虫薬。多剤耐性消化管線虫に有効",
        "species_info": {
            "dog": {"dose": "Not approved for companion animals", "notes": "Livestock anthelmintic; no established canine dose", "notes_ja": "畜産用駆虫薬；犬の用量未確立"},
            "horse": {"dose": "Not approved for horses (sheep/goat product)", "notes": "Research use only in equines for resistant cyathostomins", "notes_ja": "馬では研究使用のみ（耐性小円虫）"},
            "others": {"dose": "2.5 mg/kg PO (sheep); 3.75 mg/kg PO (goat)", "notes": "Multi-drug resistant Haemonchus, Teladorsagia, Trichostrongylus; novel MOA against BZ/LEV/ML-resistant worms", "notes_ja": "多剤耐性ヘモンクス・テラドルサジア・トリコストロンジルス；BZ/LEV/ML耐性虫に新規作用機序"}
        },
        "side_effects": ["Very well tolerated in target species", "Transient soft feces"],
        "side_effects_ja": ["標的種での忍容性非常に良好", "一過性軟便"],
        "contraindications": "Not for use in companion animals without veterinary guidance; not for cats",
        "contraindications_ja": "獣医師の指導なしでのコンパニオンアニマル使用不可；猫には使用不可",
        "drug_interactions": [
            {"drug": "No significant interactions documented", "severity": "mild", "description": "Novel MOA with minimal interaction potential", "description_ja": "新規作用機序で相互作用ポテンシャル最小"}
        ]
    },
    {
        "id": "aglepristone",
        "name": "Aglepristone (Alizin)",
        "name_ja": "アグレプリストン（アリジン）",
        "category": "reproductive",
        "mechanism": "Progesterone receptor antagonist; competitively blocks progesterone receptors with 3x affinity of progesterone. Terminates pregnancy, opens cervix in pyometra, induces parturition",
        "mechanism_ja": "プロゲステロン受容体拮抗薬；プロゲステロンの3倍の親和性で受容体を競合的に遮断。妊娠中絶、子宮蓄膿症の子宮頸管開口、分娩誘発",
        "species_info": {
            "dog": {"dose": "10 mg/kg SC on days 1, 2 (and day 8 if needed)", "notes": "Pyometra medical management (open/closed), mismating, pregnancy termination (before day 45)", "notes_ja": "子宮蓄膿症の内科的管理（開放型/閉鎖型）、交配事故、妊娠中絶（45日以前）"},
            "cat": {"dose": "10 mg/kg SC on days 1, 2 (repeat day 7 if needed)", "notes": "Pyometra, pregnancy termination; effective up to day 25 in queens", "notes_ja": "子宮蓄膿症、妊娠中絶；雌猫で25日目まで有効"},
            "rabbit": {"dose": "10 mg/kg SC days 1, 2", "notes": "Pyometra (common in intact does >3 years); very effective", "notes_ja": "子宮蓄膿症（3歳以上の未避妊雌で多い）；非常に有効"},
            "ferret": {"dose": "10 mg/kg SC days 1, 2", "notes": "Hyperadrenocorticism-associated endometrial hyperplasia", "notes_ja": "副腎皮質機能亢進症関連子宮内膜過形成"}
        },
        "side_effects": ["Injection site pain/swelling", "Transient anorexia", "Vaginal discharge (expected)", "Lethargy"],
        "side_effects_ja": ["注射部位痛/腫脹", "一過性食欲不振", "膣分泌物（予想される反応）", "嗜眠"],
        "contraindications": "Not available in USA (EU/Japan/Australia); species with non-progesterone-dependent pregnancy maintenance past certain stages",
        "contraindications_ja": "米国では未承認（EU/日本/豪州で使用可能）；特定段階以降にプロゲステロン非依存性の妊娠維持をする種",
        "drug_interactions": [
            {"drug": "Progesterone/progestins", "severity": "major", "description": "Direct pharmacological antagonism; counteracts aglepristone", "description_ja": "直接的薬理学的拮抗；アグレプリストンを打ち消す"},
            {"drug": "PGF2α (cloprostenol)", "severity": "mild", "description": "Synergistic for pyometra evacuation (often combined)", "description_ja": "子宮蓄膿症排出に相乗的（しばしば併用）"}
        ]
    },
    {
        "id": "dinoprost",
        "name": "Dinoprost (PGF2α)",
        "name_ja": "ジノプロスト（PGF2α）",
        "category": "reproductive",
        "mechanism": "Natural prostaglandin F2-alpha; causes luteolysis (destroys corpus luteum reducing progesterone), myometrial contraction, and cervical relaxation. Used for pregnancy termination and pyometra",
        "mechanism_ja": "天然プロスタグランジンF2α；黄体融解（黄体破壊によるプロゲステロン低下）、子宮筋収縮、子宮頸管弛緩を惹起。妊娠中絶と子宮蓄膿症に使用",
        "species_info": {
            "dog": {"dose": "0.1-0.25 mg/kg SC q12-24h × 3-5 days (start at low end)", "notes": "Open pyometra (with aglepristone), pregnancy termination >day 30; expect transient side effects", "notes_ja": "開放型子宮蓄膿症（アグレプリストン併用）、30日以降の妊娠中絶；一過性副作用を予想"},
            "cat": {"dose": "0.1-0.25 mg/kg SC q12-24h", "notes": "Pyometra (cats very sensitive - start 0.1 mg/kg); pregnancy termination", "notes_ja": "子宮蓄膿症（猫は感受性高い - 0.1mg/kgから開始）；妊娠中絶"},
            "horse": {"dose": "5-10 mg IM once (mare)", "notes": "Luteolysis for estrus synchronization, persistent CL, pyometra; single injection effective in mares", "notes_ja": "発情同期化の黄体融解、遺残黄体、子宮蓄膿症；馬では単回注射で有効"},
            "rabbit": {"dose": "0.1-0.2 mg/kg SC", "notes": "Pyometra, pseudopregnancy termination", "notes_ja": "子宮蓄膿症、偽妊娠中絶"}
        },
        "side_effects": ["Vomiting/salivation/diarrhea (immediate, transient 20-30 min)", "Panting", "Restlessness", "Abdominal pain", "Fever"],
        "side_effects_ja": ["嘔吐/流涎/下痢（即時性、20-30分で一過性）", "パンティング", "不穏", "腹痛", "発熱"],
        "contraindications": "Closed-cervix pyometra (without aglepristone - uterine rupture risk), cardiovascular disease, respiratory disease, pregnant animals (if pregnancy desired)",
        "contraindications_ja": "閉鎖型子宮蓄膿症（アグレプリストンなし - 子宮破裂リスク）、心血管疾患、呼吸器疾患、妊娠動物（妊娠継続希望時）",
        "drug_interactions": [
            {"drug": "Oxytocin", "severity": "moderate", "description": "Synergistic uterine contraction; risk of uterine rupture", "description_ja": "相乗的子宮収縮；子宮破裂リスク"},
            {"drug": "NSAIDs", "severity": "moderate", "description": "May antagonize prostaglandin effects through COX inhibition", "description_ja": "COX阻害によりプロスタグランジン効果を拮抗する可能性"}
        ]
    },
    {
        "id": "capromorelin",
        "name": "Capromorelin (Entyce/Elura)",
        "name_ja": "カプロモレリン（エンタイス/エルラ）",
        "category": "miscellaneous",
        "mechanism": "Ghrelin receptor agonist; mimics hunger hormone ghrelin to stimulate appetite via hypothalamic feeding centers. Also stimulates GH and IGF-1 release providing anabolic effects",
        "mechanism_ja": "グレリン受容体作動薬；視床下部摂食中枢を介して空腹ホルモン・グレリンを模倣し食欲を刺激。GH・IGF-1放出も刺激し同化作用を発揮",
        "species_info": {
            "dog": {"dose": "3 mg/kg PO q24h (Entyce, oral solution)", "notes": "Appetite stimulation in any disease causing inappetence; FDA-approved for dogs. Give 1h before meal", "notes_ja": "食欲不振を惹起する全疾患の食欲刺激；犬でFDA承認。食事1時間前に投与"},
            "cat": {"dose": "2 mg/kg PO q24h (Elura, oral solution)", "notes": "CKD-associated weight loss in cats; FDA-approved for feline CKD. Long-term use safe in studies", "notes_ja": "猫CKD関連体重減少；猫CKDでFDA承認。試験で長期使用安全"}
        },
        "side_effects": ["Diarrhea", "Vomiting", "Polydipsia", "Hypersalivation", "Elevated BUN (cats)"],
        "side_effects_ja": ["下痢", "嘔吐", "多飲", "流涎過多", "BUN上昇（猫）"],
        "contraindications": "None absolute; use with caution in GH-sensitive tumors (theoretical), hepatic disease (reduced clearance)",
        "contraindications_ja": "絶対的禁忌なし；GH感受性腫瘍（理論的）、肝疾患（クリアランス低下）では注意",
        "drug_interactions": [
            {"drug": "Insulin", "severity": "moderate", "description": "GH release may cause insulin resistance; monitor glucose in diabetic patients", "description_ja": "GH放出がインスリン抵抗性を惹起する可能性；糖尿病患者で血糖モニタリング"},
            {"drug": "CYP3A4 inhibitors", "severity": "mild", "description": "May increase capromorelin exposure", "description_ja": "カプロモレリン曝露量増加の可能性"}
        ]
    },
    {
        "id": "maropitant_injectable",
        "name": "Maropitant Injectable (Cerenia IV/SC)",
        "name_ja": "マロピタント注射（セレニアIV/SC）",
        "category": "gastrointestinal",
        "mechanism": "NK1 receptor antagonist (injectable); blocks substance P at vomiting center and vagal afferents. Also provides visceral analgesia. Injectable form for patients unable to take oral medication",
        "mechanism_ja": "NK1受容体拮抗薬（注射）；嘔吐中枢と迷走神経求心路のサブスタンスPを遮断。内臓痛覚抑制も提供。経口不可患者への注射製剤",
        "species_info": {
            "dog": {"dose": "1 mg/kg SC/IV q24h (up to 5 consecutive days)", "notes": "Perioperative nausea (give pre-op), parvoviral enteritis, chemotherapy-induced emesis, motion sickness", "notes_ja": "周術期悪心（術前投与）、パルボ腸炎、化学療法誘発嘔吐、動揺病"},
            "cat": {"dose": "1 mg/kg SC/IV q24h (up to 5 days)", "notes": "Post-operative nausea, CKD nausea, pancreatitis; IV stings (dilute with saline)", "notes_ja": "術後悪心、CKD悪心、膵炎；IV投与時に刺激感（生食で希釈）"},
            "ferret": {"dose": "1 mg/kg SC q24h", "notes": "Nausea/vomiting from various causes", "notes_ja": "各種原因による悪心/嘔吐"}
        },
        "side_effects": ["Pain at injection site (SC)", "Diarrhea", "Hypotension (rapid IV)", "Lethargy"],
        "side_effects_ja": ["注射部位痛（SC）", "下痢", "低血圧（急速IV）", "嗜眠"],
        "contraindications": "None absolute; caution <16 weeks (bone marrow suppression in young animals at high doses in safety studies)",
        "contraindications_ja": "絶対的禁忌なし；16週齢未満では注意（安全性試験で高用量にて若齢動物の骨髄抑制）",
        "drug_interactions": [
            {"drug": "CYP2D6 substrates", "severity": "mild", "description": "Maropitant inhibits CYP2D6; may increase levels of substrates", "description_ja": "マロピタントはCYP2D6を阻害；基質の濃度上昇の可能性"},
            {"drug": "Highly protein-bound drugs", "severity": "mild", "description": "Maropitant is >99% protein bound; displacement interactions possible", "description_ja": "マロピタントは99%以上蛋白結合；置換相互作用の可能性"}
        ]
    },
    {
        "id": "aluminum_hydroxide_oral",
        "name": "Aluminum Hydroxide (Phosphate Binder)",
        "name_ja": "水酸化アルミニウム（リン吸着薬）",
        "category": "gastrointestinal",
        "mechanism": "Phosphate binder; forms insoluble aluminum phosphate in GI tract preventing dietary phosphorus absorption. Reduces hyperphosphatemia in CKD. Also antacid (neutralizes gastric acid)",
        "mechanism_ja": "リン吸着薬；消化管内で不溶性リン酸アルミニウムを形成し食事性リンの吸収を阻害。CKDの高リン血症を軽減。制酸薬（胃酸中和）としても作用",
        "species_info": {
            "dog": {"dose": "30-90 mg/kg/day PO divided with meals", "notes": "CKD hyperphosphatemia (IRIS Stage 3-4); must mix with food for phosphate binding", "notes_ja": "CKD高リン血症（IRISステージ3-4）；リン結合のため食事に混合必須"},
            "cat": {"dose": "30-90 mg/kg/day PO divided with meals", "notes": "CKD phosphorus management; palatability can be challenging - mix with wet food", "notes_ja": "CKDリン管理；嗜好性に課題あり - ウェットフードに混合"},
            "rabbit": {"dose": "30 mg/kg PO with meals", "notes": "Renal disease phosphorus control", "notes_ja": "腎疾患のリン管理"},
            "bird": {"dose": "25-50 mg/kg PO with food", "notes": "Renal disease (common in older budgies/cockatiels)", "notes_ja": "腎疾患（高齢セキセイインコ・オカメインコで多い）"},
            "reptile": {"dose": "30-50 mg/kg PO with meals", "notes": "Chronic renal disease phosphorus management", "notes_ja": "慢性腎疾患のリン管理"}
        },
        "side_effects": ["Constipation", "Aluminum toxicity (long-term/renal failure)", "Hypophosphatemia (overdose)", "Anorexia (palatability)"],
        "side_effects_ja": ["便秘", "アルミニウム毒性（長期/腎不全）", "低リン血症（過量）", "食欲不振（嗜好性）"],
        "contraindications": "Severe constipation/GI obstruction, dialysis patients (aluminum accumulation)",
        "contraindications_ja": "重度便秘/消化管閉塞、透析患者（アルミニウム蓄積）",
        "drug_interactions": [
            {"drug": "Fluoroquinolones", "severity": "major", "description": "Chelates fluoroquinolones reducing absorption by >90%; separate by 2-4h", "description_ja": "フルオロキノロンをキレートし吸収90%以上低下；2-4時間間隔"},
            {"drug": "Tetracyclines", "severity": "major", "description": "Forms insoluble chelates; separate administration", "description_ja": "不溶性キレート形成；投与を分離"},
            {"drug": "Levothyroxine", "severity": "moderate", "description": "Reduced thyroid hormone absorption", "description_ja": "甲状腺ホルモン吸収低下"}
        ]
    },
    {
        "id": "lanthanum_carbonate",
        "name": "Lanthanum Carbonate (Renalzin)",
        "name_ja": "炭酸ランタン（レナルジン）",
        "category": "gastrointestinal",
        "mechanism": "Non-aluminum, non-calcium phosphate binder; rare earth metal that binds dietary phosphate in GI tract forming insoluble lanthanum phosphate. Not systemically absorbed (safer than aluminum long-term)",
        "mechanism_ja": "非アルミニウム・非カルシウム系リン吸着薬；希土類金属が消化管内で食事性リンと結合し不溶性リン酸ランタンを形成。全身吸収されない（長期的にアルミニウムより安全）",
        "species_info": {
            "dog": {"dose": "25-50 mg/kg PO divided with meals (Renalzin)", "notes": "CKD hyperphosphatemia; no aluminum toxicity risk with long-term use", "notes_ja": "CKD高リン血症；長期使用でアルミニウム毒性リスクなし"},
            "cat": {"dose": "200 mg/cat/meal (Renalzin paste) or 25-50 mg/kg/day", "notes": "CKD cats; flavored paste formulation (Renalzin) designed for feline palatability. Licensed for cats in EU", "notes_ja": "CKD猫；猫の嗜好性に設計されたフレーバーペースト製剤（レナルジン）。EUで猫に承認"}
        },
        "side_effects": ["Vomiting", "Diarrhea", "Very low systemic absorption (safety advantage)"],
        "side_effects_ja": ["嘔吐", "下痢", "全身吸収非常に低い（安全性上の利点）"],
        "contraindications": "Hypophosphatemia, GI obstruction",
        "contraindications_ja": "低リン血症、消化管閉塞",
        "drug_interactions": [
            {"drug": "Fluoroquinolones/Tetracyclines", "severity": "moderate", "description": "May chelate antibiotics; separate by 2h", "description_ja": "抗菌薬をキレートする可能性；2時間間隔"},
            {"drug": "Levothyroxine", "severity": "moderate", "description": "Potential reduced absorption; separate dosing", "description_ja": "吸収低下の可能性；投与を分離"}
        ]
    },
    {
        "id": "benazepril_feline",
        "name": "Benazepril (Feline CKD)",
        "name_ja": "ベナゼプリル（猫CKD）",
        "category": "cardiovascular",
        "mechanism": "ACE inhibitor; reduces glomerular capillary pressure by preferentially dilating efferent arteriole. In cats, uniquely dual-eliminated (50% hepatic), making it safer in renal impairment than enalapril",
        "mechanism_ja": "ACE阻害薬；輸出細動脈を優先的に拡張し糸球体毛細管圧を低下。猫では50%が肝排泄のユニークな二重排泄で、エナラプリルより腎障害時に安全",
        "species_info": {
            "dog": {"dose": "0.25-0.5 mg/kg PO q12-24h", "notes": "CHF (MMVD, DCM), proteinuric CKD; BENCH study evidence", "notes_ja": "心不全（MMVD、DCM）、蛋白尿性CKD；BENCH試験エビデンス"},
            "cat": {"dose": "0.5-1 mg/kg PO q24h (Fortekor)", "notes": "CKD IRIS Stage 2-4 with proteinuria (UPC>0.4); BENRIC study showed reduced proteinuria. Dual elimination advantage in cats", "notes_ja": "蛋白尿（UPC>0.4）を伴うCKD IRISステージ2-4；BENRIC試験で蛋白尿減少。猫での二重排泄の利点"},
            "rabbit": {"dose": "0.25-0.5 mg/kg PO q24h", "notes": "CKD, heart disease; limited but growing rabbit data", "notes_ja": "CKD、心疾患；限定的だが増加中のウサギデータ"},
            "guinea_pig": {"dose": "0.25-0.5 mg/kg PO q24h", "notes": "Cardiac disease (extrapolated)", "notes_ja": "心疾患（外挿データ）"},
            "ferret": {"dose": "0.25-0.5 mg/kg PO q24h", "notes": "Cardiomyopathy, renal disease", "notes_ja": "心筋症、腎疾患"}
        },
        "side_effects": ["Hypotension", "Azotemia (monitor creatinine)", "Hyperkalemia", "Inappetence"],
        "side_effects_ja": ["低血圧", "高窒素血症（クレアチニンモニタリング）", "高カリウム血症", "食欲不振"],
        "contraindications": "Bilateral renal artery stenosis, dehydration, severe hypotension, pregnancy",
        "contraindications_ja": "両側腎動脈狭窄、脱水、重度低血圧、妊娠",
        "drug_interactions": [
            {"drug": "NSAIDs", "severity": "moderate", "description": "Reduced renoprotective effect; avoid if possible in CKD patients", "description_ja": "腎保護効果減弱；CKD患者では可能なら回避"},
            {"drug": "Spironolactone", "severity": "moderate", "description": "Hyperkalemia risk", "description_ja": "高カリウム血症リスク"},
            {"drug": "Amlodipine", "severity": "mild", "description": "Beneficial combination for CKD hypertension in cats", "description_ja": "猫CKD高血圧に有益な組合せ"}
        ]
    },
    {
        "id": "gabapentin_pain",
        "name": "Gabapentin (Chronic Pain)",
        "name_ja": "ガバペンチン（慢性疼痛）",
        "category": "analgesic",
        "mechanism": "Binds alpha-2-delta subunit of voltage-gated calcium channels reducing excitatory neurotransmitter release. Effective for neuropathic, chronic, and osteoarthritis pain. Also anxiolytic for veterinary visits",
        "mechanism_ja": "電位依存性カルシウムチャネルのα2δサブユニットに結合し興奮性神経伝達物質放出を減少。神経障害性・慢性・変形性関節症疼痛に有効。動物病院訪問時の抗不安薬としても有用",
        "species_info": {
            "dog": {"dose": "Pain: 5-10 mg/kg PO q8h; Neuropathic: 10-20 mg/kg PO q8h", "notes": "Multimodal analgesia (OA, IVDD, neuropathic), post-amputation phantom pain; titrate up over 1-2 weeks", "notes_ja": "マルチモーダル鎮痛（OA・IVDD・神経障害性）、切断後幻肢痛；1-2週かけて漸増"},
            "cat": {"dose": "Pain: 5-10 mg/kg PO q8-12h; Anxiolysis (vet visit): 50-100 mg/cat PO 2h before", "notes": "Feline OA pain (AAHA 2022), pre-visit anxiolysis (Fear Free); liquid compound (no xylitol)", "notes_ja": "猫OA疼痛（AAHA 2022）、来院前抗不安（Fear Free）；液体調剤（キシリトールなし）"},
            "horse": {"dose": "5-20 mg/kg PO q8-12h", "notes": "Neuropathic pain (shivers, headshaking), laminitis chronic pain adjunct", "notes_ja": "神経障害性疼痛（シバーズ、ヘッドシェーキング）、慢性蹄葉炎疼痛補助"},
            "rabbit": {"dose": "5-20 mg/kg PO q8-12h", "notes": "Chronic pain (spondylosis, dental); well tolerated long-term", "notes_ja": "慢性疼痛（変形性脊椎症、歯科）；長期忍容性良好"},
            "bird": {"dose": "10-25 mg/kg PO q8-12h", "notes": "Neuropathic/chronic pain; bumblefoot, beak injuries", "notes_ja": "神経障害性/慢性疼痛；趾瘤症、嘴損傷"},
            "reptile": {"dose": "5-10 mg/kg PO q24-72h", "notes": "Chronic pain adjunct; very slow metabolism in reptiles", "notes_ja": "慢性疼痛補助；爬虫類では代謝非常に遅い"},
            "ferret": {"dose": "3-5 mg/kg PO q8-12h", "notes": "OA, post-surgical pain; combine with meloxicam for multimodal approach", "notes_ja": "OA、術後疼痛；マルチモーダルアプローチにメロキシカム併用"}
        },
        "side_effects": ["Sedation (dose-dependent, usually transient)", "Ataxia", "Weight gain (chronic)", "Withdrawal seizures (abrupt discontinuation)"],
        "side_effects_ja": ["鎮静（用量依存性、通常一過性）", "運動失調", "体重増加（慢性）", "離脱痙攣（急な中止）"],
        "contraindications": "Severe renal impairment (reduce dose/frequency), products containing xylitol (dogs/cats/ferrets)",
        "contraindications_ja": "重度腎障害（用量/頻度減量）、キシリトール含有製品（犬/猫/フェレット）",
        "drug_interactions": [
            {"drug": "Other CNS depressants", "severity": "moderate", "description": "Additive sedation; reduce doses when combining", "description_ja": "相加的鎮静；併用時は減量"},
            {"drug": "Antacids (aluminum)", "severity": "mild", "description": "Reduced gabapentin absorption by ~20%; separate by 2h", "description_ja": "ガバペンチン吸収約20%低下；2時間間隔"},
            {"drug": "Opioids", "severity": "moderate", "description": "Synergistic analgesia but also additive respiratory depression at high doses", "description_ja": "相乗的鎮痛だが高用量で相加的呼吸抑制も"}
        ]
    },
    {
        "id": "frunevetmab_extended",
        "name": "Frunevetmab (Solensia) Extended Protocol",
        "name_ja": "フルネベトマブ（ソレンシア）拡張プロトコル",
        "category": "analgesic",
        "mechanism": "Felinized anti-NGF monoclonal antibody; neutralizes nerve growth factor preventing pain signal amplification. Monthly SC injection provides 4 weeks of OA pain relief without daily medication",
        "mechanism_ja": "フェライン化抗NGFモノクローナル抗体；神経成長因子を中和し疼痛シグナル増幅を阻害。月1回SC注射で4週間のOA疼痛緩和を日常投薬なしで提供",
        "species_info": {
            "cat": {"dose": "1-2.8 mg/kg SC q28d (minimum 1 mg/kg)", "notes": "OA pain first-line (FDA/EMA approved); >77% owner-reported improvement. No renal/hepatic monitoring needed. Can extend to q5-6wk in stable patients", "notes_ja": "OA疼痛の第一選択（FDA/EMA承認）；飼い主報告77%以上改善。腎/肝モニタリング不要。安定患者では5-6週間隔に延長可能"}
        },
        "side_effects": ["Injection site reactions (mild)", "Dermatitis (rare)", "Worsened renal values (rare, monitor CKD cats closely)"],
        "side_effects_ja": ["注射部位反応（軽度）", "皮膚炎（稀）", "腎値悪化（稀、CKD猫は綿密にモニタリング）"],
        "contraindications": "None absolute; monitor closely in CKD IRIS Stage 4, known hypersensitivity",
        "contraindications_ja": "絶対的禁忌なし；CKD IRISステージ4では綿密にモニタリング、過敏症既知",
        "drug_interactions": [
            {"drug": "NSAIDs", "severity": "mild", "description": "Can be combined safely; often used as transition from chronic NSAID therapy", "description_ja": "安全に併用可能；慢性NSAID療法からの移行にしばしば使用"},
            {"drug": "Corticosteroids", "severity": "mild", "description": "No known interaction; may combine for multimodal approach", "description_ja": "既知の相互作用なし；マルチモーダルアプローチに併用可能"}
        ]
    },
    {
        "id": "librela_extended",
        "name": "Bedinvetmab (Librela) Extended Protocol",
        "name_ja": "ベジンベトマブ（リブレラ）拡張プロトコル",
        "category": "analgesic",
        "mechanism": "Caninized anti-NGF monoclonal antibody; binds and neutralizes canine NGF preventing chronic pain sensitization. Monthly SC injection for OA pain management without daily oral medications",
        "mechanism_ja": "カニナイズ化抗NGFモノクローナル抗体；犬NGFに結合・中和し慢性疼痛感作を阻害。日常経口投薬なしのOA疼痛管理のための月1回SC注射",
        "species_info": {
            "dog": {"dose": "0.5-1 mg/kg SC q28d", "notes": "OA pain (FDA/EMA approved); significant improvement in mobility scores. May extend to q5wk in well-controlled dogs. Onset 1-2 weeks for full effect", "notes_ja": "OA疼痛（FDA/EMA承認）；運動性スコアの有意な改善。安定した犬では5週間隔に延長可能。全効果まで1-2週間"}
        },
        "side_effects": ["Injection site reactions", "Urinary tract infections (higher incidence in studies)", "Dermatitis", "Atopic dermatitis exacerbation (rare)"],
        "side_effects_ja": ["注射部位反応", "尿路感染症（試験で高頻度）", "皮膚炎", "アトピー性皮膚炎悪化（稀）"],
        "contraindications": "None absolute; not for use in breeding/pregnant/lactating dogs",
        "contraindications_ja": "絶対的禁忌なし；繁殖/妊娠/泌乳犬には使用不可",
        "drug_interactions": [
            {"drug": "NSAIDs", "severity": "mild", "description": "Safe to combine; useful during transition period", "description_ja": "安全に併用可能；移行期間中に有用"},
            {"drug": "Gabapentin", "severity": "mild", "description": "Multimodal combination frequently used for moderate-severe OA", "description_ja": "中等度-重度OAに頻繁に使用されるマルチモーダル併用"}
        ]
    },
    {
        "id": "tranexamic_acid_topical",
        "name": "Tranexamic Acid (Topical/Wound)",
        "name_ja": "トラネキサム酸（外用/創傷）",
        "category": "miscellaneous",
        "mechanism": "Antifibrinolytic; inhibits plasminogen activation to plasmin by blocking lysine binding sites. Topical application for wound hemostasis without systemic effects",
        "mechanism_ja": "抗線溶薬；リジン結合部位を遮断しプラスミノーゲンからプラスミンへの活性化を阻害。全身作用なしの創傷止血に外用",
        "species_info": {
            "dog": {"dose": "Topical: soak gauze with 100 mg/mL solution; Systemic: 10-25 mg/kg IV/PO q8h", "notes": "Epistaxis (topical), post-surgical hemorrhage, DIC adjunct, von Willebrand disease bleeding episodes", "notes_ja": "鼻出血（外用）、術後出血、DIC補助、フォンヴィレブランド病出血エピソード"},
            "cat": {"dose": "10-25 mg/kg IV/PO q8h", "notes": "Hemorrhage control, DIC adjunct", "notes_ja": "出血制御、DIC補助"},
            "horse": {"dose": "10-25 mg/kg IV q8h; topical for wounds", "notes": "Exercise-induced pulmonary hemorrhage (EIPH) adjunct, post-surgical hemostasis", "notes_ja": "運動誘発性肺出血（EIPH）補助、術後止血"},
            "bird": {"dose": "Topical application to bleeding wounds/feathers", "notes": "Blood feather hemorrhage, beak injuries; topical preferred in small birds", "notes_ja": "血管羽からの出血、嘴損傷；小型鳥では外用を推奨"}
        },
        "side_effects": ["GI upset (oral)", "Thrombosis risk (systemic, rare)", "Seizures (very high doses)"],
        "side_effects_ja": ["消化器障害（経口）", "血栓症リスク（全身、稀）", "痙攣（超高用量）"],
        "contraindications": "Active intravascular clotting/DIC (systemic use), upper urinary tract bleeding (clot obstruction risk), severe renal impairment",
        "contraindications_ja": "活動性血管内凝固/DIC（全身使用）、上部尿路出血（凝血塊閉塞リスク）、重度腎障害",
        "drug_interactions": [
            {"drug": "Factor IX complex", "severity": "major", "description": "Increased thrombotic risk when combined with coagulation factor concentrates", "description_ja": "凝固因子濃縮製剤との併用で血栓リスク増加"},
            {"drug": "Estrogens", "severity": "moderate", "description": "Additive thrombotic risk", "description_ja": "相加的血栓リスク"}
        ]
    },
]
