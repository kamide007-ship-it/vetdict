"""Drug batch 91 – 2026-10 第83弾.

Two referenced-but-absent agents: the curated disease content prescribes them
with a dose, yet the dictionary had no monograph, so the treatment chips and
the interaction checker could not resolve them.

* Clonazepam — canine distemper encephalitis / hardpad entries:
  "Myoclonus: clonazepam 0.5 mg/kg PO q8h". Long-acting oral benzodiazepine
  used as an adjunct for myoclonus and refractory seizures in dogs.
* Benznidazole — canine myocarditis entry: "Trypanosoma cruzi (Chagas):
  Benznidazole 5-10 mg/kg PO q12h (limited efficacy in chronic stage)".
  The only nitroimidazole trypanocide with canine data.

Evidence: Budde JA, McCluskey DM, eds. Plumb's Veterinary Drug Handbook.
10th ed. 2023; Podell M, et al. ACVIM small animal consensus statement on
seizure management in dogs. J Vet Intern Med 2016;30:477-490; Santos FM, et al.
Chagas cardiomyopathy: the potential effect of benznidazole treatment on
diastolic dysfunction and cardiac damage in dogs chronically infected with
Trypanosoma cruzi. Acta Trop 2016;161:44-54; Barr SC. Canine Chagas' disease
(American trypanosomiasis) in North America. Vet Clin North Am Small Anim
Pract 2009;39:1055-1064.
"""

DRUGS_BATCH_91 = [
    {
        "id": "clonazepam",
        "search_aliases": ["クロナゼパム", "リボトリール", "ランドセン", "Klonopin", "Rivotril"],
        "name": "Clonazepam (Rivotril)",
        "name_ja": "クロナゼパム（リボトリール）",
        "category": "neurological",
        "mechanism": "Long-acting benzodiazepine: positive allosteric modulator of the GABA-A receptor, increasing chloride-channel opening frequency. Used as an oral adjunct for myoclonus (e.g. distemper myoclonus), cluster/refractory seizures and some anxiety disorders in dogs.",
        "mechanism_ja": "長時間作用型ベンゾジアゼピン: GABA-A受容体の正のアロステリック調節によりクロライドチャネルの開口頻度を高める。犬のミオクローヌス（ジステンパー後のミオクローヌス等）・群発/難治性発作の経口補助薬、一部の不安障害に用いる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Adjunct for myoclonus / refractory seizures: 0.5 mg/kg PO q8-12h (distemper myoclonus responds poorly to any drug). Anxiety (situational): 0.1-0.5 mg/kg PO q8-12h. Start low and titrate to effect; add-on to a maintenance antiepileptic, not a stand-alone maintenance drug (ACVIM 2016).",
                "dosage_ja": "ミオクローヌス・難治性発作の補助: 0.5 mg/kg PO q8-12h（ジステンパー後のミオクローヌスはどの薬にも反応しにくい）。状況性不安: 0.1-0.5 mg/kg PO q8-12h。低用量から開始し効果をみて調整する。維持抗てんかん薬への追加であり、単独の維持薬ではない（ACVIM 2016）。",
                "notes": "Tolerance to the anticonvulsant effect develops within weeks — reserve for adjunctive/short-term use. Never stop abruptly after chronic use (withdrawal seizures); taper over 2-4 weeks. Sedation, ataxia and paradoxical excitation can occur. Hepatic metabolism — reduce the dose in liver disease. Controlled substance (Japan: psychotropic class 3).",
                "notes_ja": "抗けいれん作用には数週間で耐性ができる — 補助・短期使用に留める。長期投与後の急な中止は離脱発作を起こすため、2-4週かけて漸減する。鎮静・運動失調・奇異性興奮がありうる。肝代謝のため肝疾患では減量する。向精神薬（日本: 第三種向精神薬）。",
            },
            "cat": {
                "safe": False,
                "dosage": "Dose not established — avoid. Oral benzodiazepines have caused idiosyncratic fulminant hepatic necrosis in cats (oral diazepam); use phenobarbital or levetiracetam instead.",
                "dosage_ja": "用量は確立されていない — 使用を避ける。経口ベンゾジアゼピン（経口ジアゼパム）で猫に特異体質性の劇症肝壊死が報告されているため、フェノバルビタールまたはレベチラセタムを用いる。",
                "notes": "Prefer phenobarbital/levetiracetam for feline seizures (ISFM).",
                "notes_ja": "猫の発作にはフェノバルビタール・レベチラセタムを優先する（ISFM）。",
            },
        },
        "contraindications": "Severe hepatic insufficiency; cats (oral benzodiazepine hepatotoxicity); abrupt discontinuation after chronic use.",
        "contraindications_ja": "重度の肝不全。猫（経口ベンゾジアゼピンの肝毒性）。長期投与後の急な中止。",
        "side_effects": [
            "Sedation",
            "Ataxia",
            "Paradoxical excitation",
            "Tolerance",
            "Withdrawal seizures on abrupt cessation",
        ],
        "side_effects_ja": ["鎮静", "運動失調", "奇異性興奮", "耐性", "急な中止での離脱発作"],
        "drug_interactions": [
            {
                "drug": "Phenobarbital",
                "effect": "CYP induction lowers clonazepam concentrations; additive CNS depression.",
                "effect_ja": "CYP誘導でクロナゼパム濃度が低下する一方、中枢抑制は相加する。",
                "severity": "moderate",
            },
            {
                "drug": "Opioids",
                "effect": "Additive CNS and respiratory depression.",
                "effect_ja": "中枢・呼吸抑制が相加する。",
                "severity": "major",
            },
        ],
        "references": [
            "Budde JA, McCluskey DM, eds. Plumb's Veterinary Drug Handbook. 10th ed. Wiley-Blackwell; 2023.",
            "Podell M, Volk HA, Berendt M, et al. 2015 ACVIM small animal consensus statement on seizure management in dogs. J Vet Intern Med 2016;30:477-490.",
            "Center SA, Elston TH, Rowland PH, et al. Fulminant hepatic failure associated with oral administration of diazepam in 11 cats. J Am Vet Med Assoc 1996;209:618-625.",
        ],
    },
    {
        "id": "benznidazole",
        "search_aliases": ["ベンズニダゾール", "Rochagan", "Radanil"],
        "name": "Benznidazole",
        "name_ja": "ベンズニダゾール",
        "category": "antiparasitics",
        "mechanism": "Nitroimidazole trypanocide: nitroreduction inside Trypanosoma cruzi generates reactive metabolites that damage parasite DNA, proteins and lipids. Active mainly against circulating trypomastigotes and intracellular amastigotes in the acute phase.",
        "mechanism_ja": "ニトロイミダゾール系抗トリパノソーマ薬: Trypanosoma cruzi 内での還元により生じる反応性代謝物が原虫のDNA・蛋白・脂質を傷害する。主に急性期の血中トリポマスチゴートと細胞内アマスチゴートに有効。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Chagas disease (American trypanosomiasis): 5-10 mg/kg PO q12h (commonly 7 mg/kg q12h) for 60 days, started in the acute phase. Efficacy is limited once chronic myocarditis/DCM is established (Barr 2009; Santos 2016) — combine with heart-failure and antiarrhythmic management.",
                "dosage_ja": "シャーガス病（アメリカトリパノソーマ症）: 5-10 mg/kg PO q12h（通常 7 mg/kg q12h）を60日間、急性期から開始する。慢性心筋炎・拡張型心筋症が成立した後は効果が限られる（Barr 2009; Santos 2016）— 心不全・抗不整脈治療と併用する。",
                "notes": "Monitor CBC and liver enzymes (bone-marrow suppression, hepatotoxicity) and watch for GI upset, dermatitis and peripheral neuropathy. T. cruzi is zoonotic (blood/tissue handling precautions). Not marketed for veterinary use; Chagas disease is not endemic in Japan — consider in dogs imported from the Americas.",
                "notes_ja": "CBC・肝酵素を監視する（骨髄抑制・肝毒性）。消化器症状・皮膚炎・末梢神経障害に注意する。T. cruzi は人獣共通感染症（血液・組織の取り扱いに注意）。動物用製剤はない。シャーガス病は日本では非流行 — 南北アメリカからの輸入犬で考慮する。",
            },
            "cat": {
                "safe": False,
                "dosage": "No feline data — not recommended.",
                "dosage_ja": "猫のデータはなく、推奨されない。",
                "notes": "",
                "notes_ja": "",
            },
        },
        "contraindications": "Pregnancy (genotoxic/teratogenic); pre-existing bone-marrow suppression or severe hepatic disease.",
        "contraindications_ja": "妊娠（遺伝毒性・催奇形性）。既存の骨髄抑制・重度肝疾患。",
        "side_effects": [
            "Vomiting / anorexia",
            "Hepatotoxicity",
            "Bone-marrow suppression",
            "Dermatitis",
            "Peripheral neuropathy",
        ],
        "side_effects_ja": ["嘔吐・食欲不振", "肝毒性", "骨髄抑制", "皮膚炎", "末梢神経障害"],
        "drug_interactions": [
            {
                "drug": "Metronidazole",
                "effect": "Both are nitroimidazoles — additive neurotoxicity and GI effects; avoid concurrent use.",
                "effect_ja": "いずれもニトロイミダゾール系 — 神経毒性・消化器症状が相加するため併用を避ける。",
                "severity": "major",
            },
        ],
        "references": [
            "Barr SC. Canine Chagas' disease (American trypanosomiasis) in North America. Vet Clin North Am Small Anim Pract 2009;39:1055-1064.",
            "Santos FM, Mazzeti AL, Caldas S, et al. Chagas cardiomyopathy: the potential effect of benznidazole treatment on diastolic dysfunction and cardiac damage in dogs chronically infected with Trypanosoma cruzi. Acta Trop 2016;161:44-54.",
            "Budde JA, McCluskey DM, eds. Plumb's Veterinary Drug Handbook. 10th ed. Wiley-Blackwell; 2023.",
        ],
    },
]
