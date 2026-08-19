"""Drug batch 40 – referenced-but-absent agents surfaced by the 2026-08 audit (8th sweep).

A dose-context katakana/English token sweep of disease treatment protocols,
cross-checked with the real text matcher (find_drugs_in_text), found four
agents that VetDict's own content instructs clinicians to use — with explicit
doses — yet were absent from the formulary:

  - ミルテホシン (miltefosine): named with a dose (2 mg/kg PO q24h × 28日) in
    the canine leishmaniosis entries as one of the two LeishVet first-line
    anti-Leishmania drugs; absent.
  - メグルミンアンチモン酸塩 (meglumine antimoniate): the other LeishVet
    first-line drug, named with doses (SC q24h 4-8週) in the same entries;
    absent.
  - ヒト免疫グロブリン/hIVIG: referenced ~30-40 times ("ヒト免疫グロブリン
    （IVIG）0.5-1 g/kg IV") as the refractory-case rescue in IMHA / ITP /
    severe cutaneous drug reaction protocols; absent.
  - 組換えヒトインターフェロンα (human interferon-alpha): referenced ~33
    times ("組換えαインターフェロン 1-10万IU/kg SC q24h") in avian
    PBFD / polyomavirus protocols and feline retrovirus adjunct therapy;
    only feline interferon-omega was carried.

References:
  - Solano-Gallego L et al. LeishVet guidelines. Vet Parasitol 2009 /
    Parasit Vectors 2011;4:86 — canine leishmaniosis treatment: miltefosine
    2 mg/kg PO q24h ×28 d or meglumine antimoniate SC, each combined with
    allopurinol 10 mg/kg PO q12h long term.
  - Miró G et al. Vet Dermatol 2009 — randomized comparison
    miltefosine+allopurinol vs meglumine antimoniate+allopurinol: comparable
    clinical efficacy.
  - Pennisi MG et al. LeishVet feline leishmaniosis guidelines. Parasit
    Vectors 2015 — allopurinol first-line in cats; miltefosine 2 mg/kg PO
    q24h ×28 d as alternative (limited data).
  - Whelan MF et al. J Vet Emerg Crit Care 2009;19:617 — randomized
    placebo-controlled trial of hIVIG (0.5 g/kg IV) in canine ITP: faster
    platelet recovery and shorter hospitalization.
  - Spurlock NK, Prittie JE. J Vet Emerg Crit Care 2011;21:471 — review of
    hIVIG use in dogs (IMHA, ITP, cutaneous drug reactions): Fc-receptor
    blockade; thromboembolism and volume-overload cautions; single-dose use
    because of anti-human-protein sensitization.
  - Kellerman DL, Bruyette DS. J Vet Intern Med 1997;11:328 — hIVIG in
    canine IMHA.
  - Cummins JM et al. — oral low-dose human IFN-α (30 IU) in FeLV-infected
    cats; Weiss RC et al. J Am Vet Med Assoc 1991 — survival benefit in
    FeLV-associated disease (evidence mixed; McCaw 2001 found no benefit).
  - Stanford M. Vet Rec 2004 — interferon therapy for circovirus (PBFD)
    infection in psittacines (limited evidence; extrapolated dosing).
  - Plumb's Veterinary Drug Handbook, 10th ed — miltefosine, meglumine
    antimoniate, immunoglobulin (human), interferon-alfa.
"""

DRUGS_BATCH_40: list[dict] = [
    {
        "id": "miltefosine",
        "search_aliases": ["ミルテホシン", "ミルテフォラン", "Milteforan"],
        "name": "Miltefosine",
        "name_ja": "ミルテホシン（ミルテフォラン）",
        "category": "antiparasitics",
        "mechanism": "Alkylphosphocholine that disrupts Leishmania membrane phospholipid metabolism and mitochondrial function, causing apoptosis-like death of amastigotes; also modulates macrophage activation. One of the two LeishVet first-line anti-Leishmania drugs (with meglumine antimoniate), always combined with allopurinol.",
        "mechanism_ja": "アルキルホスホコリン系抗リーシュマニア薬。リーシュマニア原虫の膜リン脂質代謝とミトコンドリア機能を障害しアマスティゴートをアポトーシス様死に導く。マクロファージ活性化の調節作用もある。LeishVetガイドラインの第一選択2剤の一つ（もう一方はメグルミンアンチモン酸塩）で、常にアロプリノールと併用する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2 mg/kg PO q24h × 28 days, given with food, combined with allopurinol 10 mg/kg PO q12h for ≥6-12 months (LeishVet; Solano-Gallego 2011). Complete the full 28-day course — do not skip or reduce doses (resistance risk).",
                "dosage_ja": "2 mg/kg 経口 24時間毎 × 28日間（食餌と同時投与）。アロプリノール 10 mg/kg 経口 12時間毎（6-12ヶ月以上）と併用（LeishVet; Solano-Gallego 2011）。28日間を完遂すること — 減量・中断は耐性リスク（スキップ不可）。",
                "notes": "Efficacy comparable to meglumine antimoniate when combined with allopurinol (Miró 2009). Oral route avoids injection-site reactions; preferred when renal compromise makes antimonials risky. Vomiting/diarrhea in ~10-15% — usually transient; give with food. Monitor renal values and urine protein:creatinine during therapy. Clinical cure ≠ parasitological cure — monitor serology/PCR for relapse.",
                "notes_ja": "アロプリノール併用でメグルミンアンチモン酸塩と同等の臨床効果（Miró 2009）。経口投与のため注射部位反応がなく、腎機能低下例でアンチモン製剤が使いにくい場合に優先される。約10-15%で嘔吐・下痢（通常一過性、食餌と同時投与で軽減）。治療中は腎数値と尿蛋白/クレアチニン比をモニタリング。臨床的治癒≠寄生虫学的治癒 — 血清抗体価/PCRで再発を監視。",
            },
            "cat": {
                "safe": True,
                "dosage": "2 mg/kg PO q24h × 28 days (LeishVet feline guidelines 2015; limited data). Allopurinol 10 mg/kg PO q12h is the feline first-line; miltefosine is an alternative/adjunct.",
                "dosage_ja": "2 mg/kg 経口 24時間毎 × 28日間（LeishVet猫ガイドライン2015、データ限定的）。猫の第一選択はアロプリノール 10 mg/kg 経口 12時間毎で、ミルテホシンは代替・補助。",
                "notes": "Feline leishmaniosis is uncommon; screen for FIV/FeLV co-infection which worsens prognosis.",
                "notes_ja": "猫のリーシュマニア症は稀。予後を悪化させるFIV/FeLV共感染をスクリーニングする。",
            },
        },
        "side_effects": "Vomiting, diarrhea, inappetence (usually transient); teratogenic",
        "side_effects_ja": "嘔吐・下痢・食欲不振（通常一過性）。催奇形性",
        "contraindications": "Pregnancy/lactation (teratogenic — also advise pregnant owners to wear gloves when handling). Severe hepatic/renal failure. Do not use as monotherapy without allopurinol (resistance).",
        "contraindications_ja": "妊娠・授乳中（催奇形性 — 妊娠中の飼い主には手袋着用を指導）。重度の肝・腎不全。アロプリノール非併用の単剤使用は不可（耐性リスク）。",
        "drug_interactions": [
            {
                "drug": "Allopurinol",
                "effect": "Standard combination for leishmaniosis — additive anti-Leishmania effect (LeishVet first-line protocol)",
                "effect_ja": "リーシュマニア症の標準併用 — 抗リーシュマニア作用が相加的（LeishVet第一選択プロトコル）",
            },
        ],
    },
    {
        "id": "meglumine_antimoniate",
        "search_aliases": [
            "メグルミンアンチモン酸塩",
            "メグルミンアンチモン酸",
            "アンチモン酸メグルミン",
            "グルカンチーム",
            "Glucantime",
        ],
        "name": "Meglumine Antimoniate",
        "name_ja": "メグルミンアンチモン酸塩（グルカンチーム）",
        "category": "antiparasitics",
        "mechanism": "Pentavalent antimonial: reduced intracellularly to trivalent antimony, which inhibits Leishmania glycolysis and fatty-acid β-oxidation, depleting amastigote ATP. One of the two LeishVet first-line anti-Leishmania drugs, always combined with allopurinol.",
        "mechanism_ja": "5価アンチモン製剤。細胞内で3価アンチモンに還元され、リーシュマニア原虫の解糖系と脂肪酸β酸化を阻害してアマスティゴートのATPを枯渇させる。LeishVetガイドラインの第一選択2剤の一つで、常にアロプリノールと併用する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "75-100 mg/kg SC q24h (or 40-75 mg/kg SC q12h) × 4-8 weeks, combined with allopurinol 10 mg/kg PO q12h for ≥6-12 months (LeishVet; Solano-Gallego 2011).",
                "dosage_ja": "75-100 mg/kg 皮下 24時間毎（または 40-75 mg/kg 皮下 12時間毎）× 4-8週間。アロプリノール 10 mg/kg 経口 12時間毎（6-12ヶ月以上）と併用（LeishVet; Solano-Gallego 2011）。",
                "notes": "Assess renal function BEFORE starting — nephrotoxicity potential; in dogs with significant renal disease (IRIS ≥2 with proteinuria) prefer allopurinol alone or miltefosine. Injection-site reactions (pain, swelling, abscessation) are common — rotate sites. Monitor renal values weekly during induction. Clinical cure ≠ parasitological cure — long-term serology/PCR monitoring for relapse.",
                "notes_ja": "投与前に必ず腎機能を評価 — 腎毒性の可能性があり、有意な腎疾患（蛋白尿を伴うIRIS≥2）ではアロプリノール単独またはミルテホシンを優先。注射部位反応（疼痛・腫脹・膿瘍化）が多い — 部位をローテーション。導入期は週1回腎数値をモニタリング。臨床的治癒≠寄生虫学的治癒 — 血清抗体価/PCRで長期的に再発を監視。",
            },
            "cat": {
                "safe": True,
                "dosage": "Not well established; allopurinol 10 mg/kg PO q12h is the feline first-line (LeishVet feline guidelines 2015). Antimonials reserved for refractory cases (5-50 mg/kg SC q24h reported).",
                "dosage_ja": "確立された用量なし。猫の第一選択はアロプリノール 10 mg/kg 経口 12時間毎（LeishVet猫ガイドライン2015）。アンチモン製剤は難治例に限定（5-50 mg/kg 皮下 24時間毎の報告あり）。",
                "notes": "Limited feline data; monitor renal function closely.",
                "notes_ja": "猫でのデータは限定的。腎機能を厳重にモニタリング。",
            },
        },
        "side_effects": "Nephrotoxicity, injection-site pain/swelling/abscess, GI upset, lethargy; rare pancreatitis and cardiotoxicity (high cumulative doses)",
        "side_effects_ja": "腎毒性、注射部位の疼痛・腫脹・膿瘍、消化器症状、元気消失。稀に膵炎・心毒性（高累積用量）",
        "contraindications": "Significant renal insufficiency (use allopurinol alone or miltefosine instead), severe hepatic failure, pregnancy.",
        "contraindications_ja": "有意な腎機能不全（アロプリノール単独またはミルテホシンを選択）、重度肝不全、妊娠。",
        "drug_interactions": [
            {
                "drug": "Allopurinol",
                "effect": "Standard combination for leishmaniosis — additive anti-Leishmania effect (LeishVet first-line protocol)",
                "effect_ja": "リーシュマニア症の標準併用 — 抗リーシュマニア作用が相加的（LeishVet第一選択プロトコル）",
            },
            {
                "drug": "Aminoglycosides",
                "effect": "Additive nephrotoxicity — avoid concurrent use",
                "effect_ja": "腎毒性が相加的 — 併用を避ける",
            },
        ],
    },
    {
        "id": "human_ivig",
        "search_aliases": [
            "ヒト免疫グロブリン",
            "免疫グロブリン製剤",
            "IVIG",
            "hIVIG",
            "静注用免疫グロブリン",
        ],
        "name": "Human Intravenous Immunoglobulin (hIVIG)",
        "name_ja": "ヒト免疫グロブリン（IVIG）",
        "category": "immunosuppressives",
        "mechanism": "Pooled human IgG that blockades Fcγ receptors on mononuclear phagocytes, interrupting antibody-mediated destruction of erythrocytes/platelets; additional immune-complex clearance modulation and anti-idiotype effects. Provides rapid (24-72 h) interruption of immune-mediated cytopenias while conventional immunosuppression takes effect.",
        "mechanism_ja": "プール化ヒトIgG製剤。単核貪食細胞系のFcγ受容体をブロックし、抗体を介した赤血球・血小板破壊を中断する。免疫複合体クリアランスの調節・抗イディオタイプ作用もある。従来の免疫抑制薬が効果を発揮するまでの間、免疫介在性血球減少を迅速（24-72時間）に中断する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1.5 g/kg IV over 6-12 h as a SINGLE infusion (refractory ITP: Whelan 2009 used 0.5 g/kg; IMHA rescue: 0.5-1.5 g/kg — Kellerman 1997, Spurlock 2011). Also reported for severe cutaneous drug reactions (SJS/TEN, 0.5-1 g/kg).",
                "dosage_ja": "0.5-1.5 g/kg を6-12時間かけて緩徐に静注（単回）。難治性ITP: Whelan 2009は0.5 g/kgを使用。IMHAレスキュー: 0.5-1.5 g/kg（Kellerman 1997, Spurlock 2011）。重症皮膚薬物反応（SJS/TEN、0.5-1 g/kg）の報告もある。",
                "notes": "Rescue therapy for IMHA/ITP refractory to glucocorticoids ± second-line immunosuppressants — NOT first-line. Single use only: anti-human-protein antibodies form after exposure, so repeat administration risks anaphylaxis. IMHA patients are already hypercoagulable — hIVIG may further increase thromboembolic risk; give concurrent thromboprophylaxis (clopidogrel/heparin). Monitor for volume overload (colloid osmotic load) and infusion reactions (slow/stop infusion, antihistamine).",
                "notes_ja": "グルココルチコイド±第二選択免疫抑制薬に反応しないIMHA/ITPのレスキュー療法 — 第一選択ではない。単回使用に限る: 投与後に抗ヒト蛋白抗体が形成されるため、再投与はアナフィラキシーリスク。IMHA患者は既に過凝固状態 — hIVIGは血栓塞栓リスクをさらに高めうるため、抗血栓療法（クロピドグレル/ヘパリン）を併用。容量過負荷（膠質浸透圧負荷）と輸注反応をモニタリング（発現時は減速・中断、抗ヒスタミン薬）。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.5-1 g/kg IV over 6-8 h single infusion (limited case reports — pure red cell aplasia, refractory IMHA).",
                "dosage_ja": "0.5-1 g/kg を6-8時間かけて静注（単回）。症例報告レベル（赤芽球癆・難治性IMHA）。",
                "notes": "Feline evidence is anecdotal; reserve for refractory immune-mediated cytopenias after standard immunosuppression fails.",
                "notes_ja": "猫でのエビデンスは逸話的。標準的免疫抑制が無効の難治性免疫介在性血球減少に限定する。",
            },
        },
        "side_effects": "Infusion reactions (facial swelling, urticaria, vomiting), thromboembolism (especially IMHA), volume overload, rare acute renal injury (sucrose-stabilized products)",
        "side_effects_ja": "輸注反応（顔面腫脹・蕁麻疹・嘔吐）、血栓塞栓症（特にIMHA）、容量過負荷。稀に急性腎障害（ショ糖安定化製剤）",
        "contraindications": "Prior hIVIG exposure (anti-human-protein sensitization — anaphylaxis risk on re-exposure). Uncontrolled hypercoagulable state without thromboprophylaxis. Volume-intolerant cardiac patients (slow infusion, reduce volume).",
        "contraindications_ja": "hIVIG投与歴（抗ヒト蛋白感作 — 再投与でアナフィラキシーリスク）。抗血栓療法なしの制御不能な過凝固状態。容量負荷に耐えられない心疾患例（緩徐投与・減量）。",
        "drug_interactions": [
            {
                "drug": "Prednisolone",
                "effect": "Standard concurrent therapy — hIVIG bridges the 1-2 week lag of glucocorticoid immunosuppression",
                "effect_ja": "標準的な併用 — グルココルチコイド免疫抑制の効果発現（1-2週）までをhIVIGが橋渡しする",
            },
            {
                "drug": "Clopidogrel",
                "effect": "Recommended thromboprophylaxis when hIVIG is used in hypercoagulable IMHA patients",
                "effect_ja": "過凝固状態のIMHA患者へのhIVIG使用時に推奨される血栓予防",
            },
        ],
    },
    {
        "id": "interferon_alpha",
        "search_aliases": [
            "インターフェロンアルファ",
            "インターフェロンα",
            "αインターフェロン",
            "組換えαインターフェロン",
            "ヒトインターフェロン",
            "IFN-α",
        ],
        "name": "Interferon Alpha (Human Recombinant)",
        "name_ja": "インターフェロンα（組換えヒト）",
        "category": "antivirals",
        "mechanism": "Type I interferon: binds the IFNAR receptor and induces antiviral effector proteins (2'5'-oligoadenylate synthetase, PKR) that degrade viral RNA and block viral protein synthesis; also enhances NK-cell and macrophage activity. Oral low-dose protocols act via oropharyngeal lymphoid immunomodulation rather than systemic antiviral levels.",
        "mechanism_ja": "I型インターフェロン。IFNAR受容体に結合し抗ウイルスエフェクター蛋白（2'5'-オリゴアデニル酸合成酵素・PKR）を誘導してウイルスRNA分解・蛋白合成阻害を起こす。NK細胞・マクロファージ活性の増強作用もある。経口低用量プロトコルは全身の抗ウイルス濃度ではなく口腔咽頭リンパ組織の免疫調節を介して作用する。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Oral low-dose: 30 IU/cat PO q24h on alternating weekly cycles (7 days on / 7 days off) as adjunct for FeLV/FIV-associated disease (Cummins 1988; Weiss 1991 — evidence mixed, McCaw 2001 found no benefit). High-dose SC (10⁴-10⁶ IU/kg) is limited by neutralizing antibody formation after 3-7 weeks.",
                "dosage_ja": "経口低用量: 30 IU/頭 経口 24時間毎を週交代サイクル（7日投与/7日休薬）で、FeLV/FIV関連疾患の補助療法として（Cummins 1988; Weiss 1991 — エビデンスは賛否あり、McCaw 2001は効果を認めず）。高用量皮下投与（10⁴-10⁶ IU/kg）は3-7週で中和抗体が形成され効果が減弱する。",
                "notes": "Feline interferon-omega (licensed in Japan/EU) is preferred where available — homologous protein, no neutralizing antibody problem. Human IFN-α is an economical adjunct when omega is unavailable. Supportive care and secondary-infection control remain the mainstay of retrovirus management.",
                "notes_ja": "入手可能ならネコインターフェロンω（日本/EUで承認済み）を優先 — 同種蛋白のため中和抗体の問題がない。ヒトIFN-αはω入手不能時の安価な補助選択肢。レトロウイルス管理の主体は支持療法と二次感染対策であることに変わりはない。",
            },
            "bird": {
                "safe": True,
                "dosage": "10,000-100,000 IU/kg SC q24h (limited evidence; extrapolated) as adjunct for circovirus (PBFD) / polyomavirus infection (Stanford 2004 — interferon therapy for psittacine circovirus).",
                "dosage_ja": "1-10万 IU/kg 皮下 24時間毎（限定的エビデンス・外挿）。サーコウイルス（PBFD）/ポリオーマウイルス感染の補助療法として（Stanford 2004 — オウム類サーコウイルスへのインターフェロン療法）。",
                "notes": "No specific antiviral cures PBFD — therapy is supportive (nutrition, warmth, secondary-infection control, strict isolation/hygiene to protect the flock). Interferon is adjunctive with limited evidence; discuss euthanasia ethics for progressive PBFD in highly susceptible species.",
                "notes_ja": "PBFDを治癒させる特異的抗ウイルス薬はない — 治療は支持療法（栄養・保温・二次感染対策・群を守る厳格な隔離/衛生管理）が主体。インターフェロンは限定的エビデンスの補助療法。感受性の高い種で進行性のPBFDでは安楽死の倫理的検討も説明する。",
            },
        },
        "side_effects": "High-dose parenteral: fever, lethargy, myelosuppression (monitor CBC); neutralizing antibody formation (3-7 weeks) abolishes efficacy. Oral low-dose: minimal.",
        "side_effects_ja": "高用量非経口投与: 発熱・元気消失・骨髄抑制（CBCモニタリング）。3-7週で中和抗体が形成され効果消失。経口低用量: ほぼなし",
        "contraindications": "None significant at oral low dose. Avoid prolonged high-dose parenteral courses (antibody formation, myelosuppression).",
        "contraindications_ja": "経口低用量では重大な禁忌なし。高用量非経口の長期投与は避ける（中和抗体形成・骨髄抑制）。",
        "drug_interactions": [],
    },
]
