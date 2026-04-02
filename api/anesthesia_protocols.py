"""Anesthesia & sedation protocols for all 21 species.

Each species entry contains:
- premedication protocols
- induction protocols
- maintenance protocols
- local/regional anesthesia options
- monitoring guidelines
- recovery notes
- species-specific warnings
"""

ANESTHESIA_CATEGORIES = {
    "sedation": {"ja": "鎮静", "en": "Sedation"},
    "premedication": {"ja": "前投薬", "en": "Premedication"},
    "induction": {"ja": "導入", "en": "Induction"},
    "maintenance": {"ja": "維持", "en": "Maintenance"},
    "local_regional": {"ja": "局所・区域麻酔", "en": "Local/Regional"},
    "monitoring": {"ja": "モニタリング", "en": "Monitoring"},
    "recovery": {"ja": "覚醒", "en": "Recovery"},
    "emergency": {"ja": "緊急対応", "en": "Emergency"},
}

RISK_LEVELS = {
    "low": {"ja": "低リスク", "en": "Low Risk"},
    "moderate": {"ja": "中リスク", "en": "Moderate Risk"},
    "high": {"ja": "高リスク", "en": "High Risk"},
}

ASA_CLASSIFICATION = {
    "I": {
        "ja": "正常で健康な患者。基礎疾患なし。",
        "en": "Normal healthy patient. No underlying disease.",
        "risk": "low",
        "guidance_ja": "標準プロトコルで実施。特別な追加モニタリング不要。",
        "guidance_en": "Standard protocols. No additional monitoring required.",
    },
    "II": {
        "ja": "軽度の全身疾患を有する患者。肥満、高齢（合併症なし）、軽度心雑音等。",
        "en": "Patient with mild systemic disease. Obesity, geriatric (no comorbidities), mild heart murmur.",
        "risk": "low",
        "guidance_ja": "標準プロトコルで実施。術前血液検査推奨。輸液管理を確実に。",
        "guidance_en": "Standard protocols. Pre-anesthetic bloodwork recommended. Ensure IV fluid support.",
    },
    "III": {
        "ja": "重度の全身疾患を有する患者。代償性心疾患、中等度脱水、貧血、軽度の発熱等。",
        "en": "Patient with severe systemic disease. Compensated cardiac disease, moderate dehydration, anemia, mild fever.",
        "risk": "moderate",
        "guidance_ja": "用量を25-50%減量。侵襲的血圧モニタリング検討。術前安定化を実施。予備の緊急薬を準備。",
        "guidance_en": "Reduce doses by 25-50%. Consider invasive BP monitoring. Stabilize before anesthesia. Have emergency drugs drawn up.",
    },
    "IV": {
        "ja": "生命を脅かす重度の全身疾患。非代償性心不全、DIC、重度敗血症、ショック等。",
        "en": "Patient with severe systemic disease that is a constant threat to life. Decompensated heart failure, DIC, severe sepsis, shock.",
        "risk": "high",
        "guidance_ja": "最低用量で慎重に投与（titrate to effect）。侵襲的血圧・CVP必須。昇圧薬を準備。術前に可能な限り安定化。チーム全体で緊急対応の事前確認。",
        "guidance_en": "Use minimal doses (titrate to effect). Invasive BP and CVP mandatory. Vasopressors ready. Stabilize as much as possible pre-operatively. Brief entire team on emergency protocols.",
    },
    "V": {
        "ja": "手術なしでは24時間以内に死亡が予想される瀕死の患者。GDV、重度外傷、大量出血等。",
        "en": "Moribund patient not expected to survive 24 hours without surgery. GDV, severe trauma, massive hemorrhage.",
        "risk": "high",
        "guidance_ja": "最低限の薬物で意識消失を得る。術前輸液蘇生を並行。フェンタニル/ケタミンの微量投与で導入。揮発性麻酔薬は最低濃度。心肺蘇生の準備を常に。",
        "guidance_en": "Achieve unconsciousness with minimum drugs. Concurrent fluid resuscitation. Induce with microdoses of fentanyl/ketamine. Minimal volatile agent. CPR setup at all times.",
    },
    "E": {
        "ja": "緊急手術（上記いずれかのクラスに追加）。胃内容物の誤嚥リスク上昇。",
        "en": "Emergency surgery (appended to any class above). Increased aspiration risk from full stomach.",
        "risk": "high",
        "guidance_ja": "迅速導入（RSI）を検討。胃内容物の誤嚥に備え吸引器を準備。十分な前酸素化。絶食不十分を前提に対応。",
        "guidance_en": "Consider rapid sequence induction (RSI). Have suction ready for aspiration. Adequate preoxygenation. Assume full stomach.",
    },
}

ANESTHESIA_PROTOCOLS = {}

# ============================================================
# DOG
# ============================================================
ANESTHESIA_PROTOCOLS["dog"] = {
    "species_name": {"ja": "犬", "en": "Dog"},
    "overview": {
        "ja": "犬は麻酔に比較的耐性があるが、短頭種（ブルドッグ、パグ等）は上気道閉塞リスクが高い。大型犬はGDV（胃拡張捻転）リスクに注意。サイトハウンド（グレイハウンド等）はチオペンタール感受性が高い。",
        "en": "Dogs are relatively tolerant of anesthesia, but brachycephalic breeds (Bulldogs, Pugs) have high upper airway obstruction risk. Large breeds require GDV awareness. Sighthounds (Greyhounds) have increased thiopental sensitivity.",
    },
    "fasting": {
        "ja": "成犬: 6-8時間絶食、2-4時間絶水。子犬（<8週齢）: 2-4時間絶食（低血糖リスク）。",
        "en": "Adults: 6-8 hr food fast, 2-4 hr water fast. Puppies (<8 wk): 2-4 hr food fast (hypoglycemia risk).",
    },
    "protocols": [
        {
            "name": {"ja": "軽度鎮静（検査・処置用）", "en": "Light Sedation (Examination/Procedures)"},
            "category": "sedation",
            "risk_level": "low",
            "drugs": [
                {"name": "Acepromazine", "name_ja": "アセプロマジン", "dose": "0.01-0.05 mg/kg", "route": "IM/IV", "onset": "15-30 min (IM)", "duration": "3-4 hr",
                 "notes_ja": "低血圧に注意。ボクサーでは過感受性あり。てんかん歴のある犬には使用注意。", "notes": "Watch for hypotension. Boxers may be hypersensitive. Use caution in epileptic dogs."},
                {"name": "Dexmedetomidine", "name_ja": "デクスメデトミジン", "dose": "2-5 μg/kg", "route": "IM/IV", "onset": "5-15 min", "duration": "30-60 min",
                 "notes_ja": "徐脈・血圧変動に注意。アティパメゾールで拮抗可能。心疾患には禁忌。", "notes": "Monitor for bradycardia. Reversible with atipamezole. Contraindicated in cardiac disease."},
            ],
            "notes_ja": "軽度処置ではアセプロマジン単独またはデクスメデトミジン低用量で十分な鎮静が得られることが多い。",
            "notes": "Light procedures often achievable with acepromazine alone or low-dose dexmedetomidine.",
        },
        {
            "name": {"ja": "中等度鎮静（X線・超音波・創傷処置）", "en": "Moderate Sedation (Radiography/Ultrasound/Wound Care)"},
            "category": "sedation",
            "risk_level": "low",
            "drugs": [
                {"name": "Dexmedetomidine + Butorphanol", "name_ja": "デクスメデトミジン＋ブトルファノール", "dose": "5-10 μg/kg + 0.2-0.4 mg/kg", "route": "IM", "onset": "10-15 min", "duration": "30-60 min",
                 "notes_ja": "シナジー効果で確実な鎮静。拮抗: アティパメゾール（同容量IM）。", "notes": "Synergistic sedation. Reverse: atipamezole (equal volume IM)."},
                {"name": "Dexmedetomidine + Hydromorphone", "name_ja": "デクスメデトミジン＋ヒドロモルフォン", "dose": "5-10 μg/kg + 0.05-0.1 mg/kg", "route": "IM", "onset": "10-15 min", "duration": "45-90 min",
                 "notes_ja": "より深い鎮静・鎮痛。疼痛を伴う処置に適する。", "notes": "Deeper sedation/analgesia. Suitable for painful procedures."},
            ],
            "notes_ja": "α2作動薬＋オピオイドの併用は犬で最も信頼性の高い鎮静プロトコル。",
            "notes": "Alpha-2 agonist + opioid combination is the most reliable sedation protocol in dogs.",
        },
        {
            "name": {"ja": "前投薬（全身麻酔前）", "en": "Premedication (Before General Anesthesia)"},
            "category": "premedication",
            "risk_level": "low",
            "drugs": [
                {"name": "Acepromazine + Methadone", "name_ja": "アセプロマジン＋メサドン", "dose": "0.01-0.03 mg/kg + 0.2-0.5 mg/kg", "route": "IM", "onset": "15-20 min", "duration": "2-4 hr",
                 "notes_ja": "標準的な前投薬。健康な犬（ASA I-II）に推奨。", "notes": "Standard premedication. Recommended for healthy dogs (ASA I-II)."},
                {"name": "Dexmedetomidine + Methadone", "name_ja": "デクスメデトミジン＋メサドン", "dose": "3-5 μg/kg + 0.2-0.3 mg/kg", "route": "IM", "onset": "10-15 min", "duration": "30-60 min",
                 "notes_ja": "導入薬の必要量を大幅に減少。心疾患のある犬には減量。", "notes": "Significantly reduces induction agent requirement. Reduce dose in cardiac patients."},
                {"name": "Midazolam + Hydromorphone", "name_ja": "ミダゾラム＋ヒドロモルフォン", "dose": "0.2-0.3 mg/kg + 0.05-0.1 mg/kg", "route": "IM/IV", "onset": "5-10 min", "duration": "30-60 min",
                 "notes_ja": "高リスク患者（ASA III-V）に推奨。心血管系への影響が少ない。", "notes": "Recommended for high-risk patients (ASA III-V). Minimal cardiovascular effects."},
            ],
            "notes_ja": "前投薬は導入薬の必要量を30-50%削減し、よりスムーズな導入・覚醒をもたらす。",
            "notes": "Premedication reduces induction agent requirements by 30-50% and provides smoother induction/recovery.",
        },
        {
            "name": {"ja": "導入（全身麻酔）", "en": "Induction (General Anesthesia)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Propofol", "name_ja": "プロポフォール", "dose": "2-6 mg/kg", "route": "IV (slow, to effect)", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "最も一般的な導入薬。前投薬後は2-4 mg/kgで十分なことが多い。無呼吸に注意し、気管挿管の準備を。", "notes": "Most common induction agent. 2-4 mg/kg often sufficient after premedication. Watch for apnea; have ET tube ready."},
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "1-3 mg/kg", "route": "IV (slow, to effect)", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "プロポフォールの代替。心血管系への影響がやや少ない。IM投与も可（猫でより一般的）。", "notes": "Alternative to propofol. Slightly less cardiovascular depression. IM route possible (more common in cats)."},
                {"name": "Ketamine + Midazolam", "name_ja": "ケタミン＋ミダゾラム", "dose": "5-7 mg/kg + 0.2-0.3 mg/kg", "route": "IV", "onset": "1-2 min", "duration": "15-20 min",
                 "notes_ja": "ケタミン単独は犬では筋硬直を引き起こすため、必ずベンゾジアゼピンと併用。", "notes": "Ketamine alone causes muscle rigidity in dogs; always combine with benzodiazepine."},
            ],
            "notes_ja": "導入はtitration to effect（効果が得られるまで緩徐に投与）が原則。急速投与は無呼吸のリスクを増大させる。",
            "notes": "Always titrate to effect. Rapid administration increases apnea risk.",
        },
        {
            "name": {"ja": "維持（吸入麻酔）", "en": "Maintenance (Inhalation)"},
            "category": "maintenance",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Isoflurane", "name_ja": "イソフルラン", "dose": "MAC 1.28%（犬）", "route": "Inhalation", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "最も一般的な吸入麻酔薬。用量依存性の心血管抑制・低血圧に注意。", "notes": "Most common inhalant. Monitor for dose-dependent cardiovascular depression and hypotension."},
                {"name": "Sevoflurane", "name_ja": "セボフルラン", "dose": "MAC 2.36%（犬）", "route": "Inhalation", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "導入・覚醒がイソフルランより速い。マスク導入に適する。コストが高い。", "notes": "Faster induction/recovery than isoflurane. Suitable for mask induction. Higher cost."},
            ],
            "notes_ja": "術中は輸液（5-10 mL/kg/hr 晶質液）を維持。鎮痛はCRI（フェンタニル2-5 μg/kg/hr、リドカイン25-50 μg/kg/min、ケタミン2-10 μg/kg/min）を検討。",
            "notes": "Maintain IV fluids (5-10 mL/kg/hr crystalloids). Consider analgesic CRI (fentanyl 2-5 μg/kg/hr, lidocaine 25-50 μg/kg/min, ketamine 2-10 μg/kg/min).",
        },
        {
            "name": {"ja": "局所・区域麻酔", "en": "Local/Regional Anesthesia"},
            "category": "local_regional",
            "risk_level": "low",
            "drugs": [
                {"name": "Lidocaine", "name_ja": "リドカイン", "dose": "Max 6 mg/kg（犬）", "route": "Local infiltration / Nerve block", "onset": "5-10 min", "duration": "60-90 min",
                 "notes_ja": "最大用量を厳守。エピネフリン添加で作用延長・出血抑制。", "notes": "Do not exceed maximum dose. Epinephrine addition extends duration and reduces bleeding."},
                {"name": "Bupivacaine", "name_ja": "ブピバカイン", "dose": "Max 2 mg/kg（犬）", "route": "Local infiltration / Nerve block / Epidural", "onset": "15-20 min", "duration": "4-6 hr",
                 "notes_ja": "長時間作用型。術後鎮痛に有効。硬膜外投与: 0.5-1.0 mg/kg。", "notes": "Long-acting. Effective for postoperative analgesia. Epidural: 0.5-1.0 mg/kg."},
                {"name": "Epidural (Morphine + Bupivacaine)", "name_ja": "硬膜外麻酔（モルヒネ＋ブピバカイン）", "dose": "Morphine 0.1 mg/kg + Bupivacaine 0.5-1 mg/kg", "route": "Epidural (L7-S1)", "onset": "20-30 min", "duration": "12-24 hr (morphine)",
                 "notes_ja": "後肢・骨盤・腹腔手術に優れた鎮痛。無菌操作を徹底。", "notes": "Excellent analgesia for hindlimb, pelvic, and abdominal surgery. Strict aseptic technique required."},
            ],
            "notes_ja": "局所・区域麻酔は全身麻酔薬の必要量を減らし、術後鎮痛を改善する。マルチモーダル鎮痛の一環として積極的に活用。",
            "notes": "Local/regional anesthesia reduces general anesthetic requirements and improves postoperative analgesia. Use as part of multimodal analgesia.",
        },
        {
            "name": {"ja": "モニタリング", "en": "Monitoring Guidelines"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "SpO2", "target": ">95%", "notes_ja": "95%未満は低酸素血症。対応: 酸素流量増加、気道確認、PEEP検討。", "notes": "Below 95% indicates hypoxemia. Response: increase O2 flow, check airway, consider PEEP."},
                {"param": "ETCO2", "target": "35-45 mmHg", "notes_ja": "45超は換気不足（換気量/回数増加）。35未満は過換気。", "notes": "Above 45 indicates hypoventilation. Below 35 indicates hyperventilation."},
                {"param": "HR", "target": "60-140 bpm", "notes_ja": "徐脈（<60）: アトロピン0.02-0.04 mg/kg IV。頻脈（>160）: 麻酔深度・疼痛確認。", "notes": "Bradycardia (<60): atropine 0.02-0.04 mg/kg IV. Tachycardia (>160): check depth/pain."},
                {"param": "MAP", "target": "60-100 mmHg", "notes_ja": "MAP<60は臓器灌流不全。対応: 輸液負荷10-20 mL/kg、吸入濃度減少、昇圧剤検討。", "notes": "MAP<60 indicates organ hypoperfusion. Response: fluid bolus, reduce inhalant, consider vasopressors."},
                {"param": "Temperature", "target": "37.5-39.0°C", "notes_ja": "低体温は覚醒延長の主要因。加温パッド、温風ブランケット使用。", "notes": "Hypothermia is a major cause of prolonged recovery. Use warming pads and forced-air blankets."},
                {"param": "ECG", "target": "Normal sinus rhythm", "notes_ja": "不整脈出現時は麻酔深度・電解質・低酸素を確認。", "notes": "On arrhythmia, check depth, electrolytes, and oxygenation."},
            ],
            "notes_ja": "最低限: SpO2、ETCO2、HR、体温を5分毎に記録。MAP（侵襲的 or 非侵襲的血圧）は外科手術では必須。",
            "notes": "Minimum: record SpO2, ETCO2, HR, temperature q5min. MAP (invasive or non-invasive) is essential for surgical procedures.",
        },
        {
            "name": {"ja": "覚醒・回復", "en": "Recovery"},
            "category": "recovery",
            "risk_level": "low",
            "drugs": [
                {"name": "Atipamezole", "name_ja": "アティパメゾール", "dose": "Same volume as dexmedetomidine used", "route": "IM", "onset": "5-10 min", "duration": "",
                 "notes_ja": "デクスメデトミジンの拮抗薬。鎮痛も拮抗するため、他の鎮痛薬を確保してから投与。", "notes": "Reverses dexmedetomidine. Also reverses analgesia; ensure alternative analgesia before administering."},
                {"name": "Flumazenil", "name_ja": "フルマゼニル", "dose": "0.01-0.02 mg/kg", "route": "IV", "onset": "1-2 min", "duration": "30-60 min",
                 "notes_ja": "ベンゾジアゼピンの拮抗薬。ミダゾラム/ジアゼパムの過剰鎮静時に使用。", "notes": "Benzodiazepine reversal agent. Use for excessive midazolam/diazepam sedation."},
            ],
            "notes_ja": "覚醒時は静かで暖かい環境を確保。短頭種は完全覚醒まで気管チューブを抜管しない。抜管後は酸素補給を継続。",
            "notes": "Ensure quiet, warm environment. Do not extubate brachycephalic breeds until fully awake. Continue oxygen supplementation post-extubation.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Atropine", "name_ja": "アトロピン", "dose": "0.02-0.04 mg/kg", "route": "IV", "onset": "1-2 min", "duration": "15-30 min",
                 "notes_ja": "徐脈性不整脈に対する第一選択。", "notes": "First-line for bradyarrhythmias."},
                {"name": "Epinephrine", "name_ja": "エピネフリン（アドレナリン）", "dose": "0.01 mg/kg (low dose) / 0.1 mg/kg (high dose)", "route": "IV / IT", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "心肺停止時: low dose 0.01 mg/kg IV q3-5min。アナフィラキシー: 0.01 mg/kg IM。", "notes": "CPA: low dose 0.01 mg/kg IV q3-5min. Anaphylaxis: 0.01 mg/kg IM."},
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "1-2 mg/kg", "route": "IV", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸刺激薬。新生児の呼吸促進にも使用（舌下1-2滴）。", "notes": "Respiratory stimulant. Also used for neonatal resuscitation (1-2 drops sublingual)."},
            ],
            "notes_ja": "心肺蘇生（CPR）: 胸骨圧迫100-120回/分、2分毎に確認。エピネフリンは3-5分毎に反復投与。RECOVER CPRガイドラインに準拠。",
            "notes": "CPR: chest compressions 100-120/min, check q2min. Epinephrine q3-5min. Follow RECOVER CPR guidelines.",
        },
        {
            "name": {"ja": "CRI鎮痛（持続定量点滴）", "en": "CRI Analgesia (Constant Rate Infusion)"},
            "category": "maintenance",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Fentanyl CRI", "name_ja": "フェンタニルCRI", "dose": "2-5 µg/kg/hr (loading: 2-5 µg/kg IV slow)", "route": "IV CRI", "onset": "2-3 min", "duration": "Continuous",
                 "notes_ja": "最も一般的な術中CRI鎮痛。ボーラス後にCRI開始。徐脈に注意。μオピオイド作動薬。MAC削減30-50%。", "notes": "Most common intraoperative CRI analgesic. Start CRI after loading dose. Watch for bradycardia. µ-opioid agonist. MAC reduction 30-50%."},
                {"name": "Remifentanil CRI", "name_ja": "レミフェンタニルCRI", "dose": "5-20 µg/kg/hr (no loading dose needed)", "route": "IV CRI", "onset": "1-2 min", "duration": "Continuous (ultra-short acting)",
                 "notes_ja": "超短時間作用型。中止後3-5分で効果消失。術後鎮痛の移行計画が必須。用量調節が容易。", "notes": "Ultra-short acting. Effect gone within 3-5 min after stopping. Must plan transition to post-op analgesia. Easy dose titration."},
                {"name": "Ketamine CRI", "name_ja": "ケタミンCRI", "dose": "2-10 µg/kg/min (loading: 0.5 mg/kg IV)", "route": "IV CRI", "onset": "1-2 min", "duration": "Continuous",
                 "notes_ja": "NMDA受容体拮抗薬。中枢感作（ワインドアップ）を予防。オピオイドとの併用で相乗効果。サブ麻酔用量では交感神経刺激作用。", "notes": "NMDA antagonist. Prevents central sensitization (wind-up). Synergistic with opioids. Sub-anesthetic doses provide sympathetic stimulation."},
                {"name": "Lidocaine CRI", "name_ja": "リドカインCRI", "dose": "25-50 µg/kg/min (loading: 1-2 mg/kg IV over 10 min)", "route": "IV CRI", "onset": "5-10 min", "duration": "Continuous",
                 "notes_ja": "全身性鎮痛・抗不整脈・消化管運動促進。開腹術に特に有用。猫には禁忌（心毒性リスク高い）。ローディングは必ず緩徐に投与。", "notes": "Systemic analgesia, anti-arrhythmic, prokinetic. Especially useful for laparotomy. CONTRAINDICATED in cats (high cardiotoxicity risk). Loading dose must be given slowly."},
                {"name": "MLK (Morphine-Lidocaine-Ketamine)", "name_ja": "MLK（モルヒネ-リドカイン-ケタミン）", "dose": "Morphine 0.1 mg/kg/hr + Lidocaine 25-50 µg/kg/min + Ketamine 2-10 µg/kg/min", "route": "IV CRI (combined)", "onset": "5-10 min", "duration": "Continuous",
                 "notes_ja": "マルチモーダル鎮痛の代表的プロトコル。3剤を1バッグに混合して投与可能。各薬剤の副作用を低用量で回避しつつ相乗的鎮痛を実現。", "notes": "Gold standard multimodal analgesia CRI. Can combine all 3 in one bag. Synergistic analgesia at lower individual doses minimizes side effects."},
                {"name": "Dexmedetomidine CRI", "name_ja": "デクスメデトミジンCRI", "dose": "0.5-2 µg/kg/hr", "route": "IV CRI", "onset": "5-10 min", "duration": "Continuous",
                 "notes_ja": "α2作動薬。鎮静・鎮痛・MAC削減（30-50%）。徐脈・末梢血管収縮あり。心疾患には慎重投与。", "notes": "α2-agonist. Sedation, analgesia, MAC reduction 30-50%. Causes bradycardia and peripheral vasoconstriction. Use cautiously in cardiac patients."},
            ],
            "notes_ja": "CRI鎮痛はバランス麻酔の中核。揮発性麻酔薬のMAC削減により心血管系への影響を最小化。シリンジポンプ使用推奨。複数CRIの併用時は各薬剤の相互作用に注意。",
            "notes": "CRI analgesia is central to balanced anesthesia. MAC reduction minimizes cardiovascular effects of volatile agents. Syringe pump recommended. Monitor drug interactions when combining multiple CRIs.",
        },
        {
            "name": {"ja": "TIVA（全静脈麻酔）", "en": "TIVA (Total Intravenous Anesthesia)"},
            "category": "maintenance",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Propofol TIVA", "name_ja": "プロポフォールTIVA", "dose": "0.1-0.4 mg/kg/min (6-24 mg/kg/hr)", "route": "IV CRI", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "短時間処置（<30分）に最適。蓄積性あり、長時間投与では覚醒遅延。脂質含有のため長時間投与で高脂血症リスク。オピオイドCRI併用でプロポフォール減量可能。", "notes": "Best for short procedures (<30 min). Accumulates with prolonged infusion causing delayed recovery. Lipid emulsion may cause hypertriglyceridemia. Combine with opioid CRI to reduce propofol requirements."},
                {"name": "Alfaxalone TIVA", "name_ja": "アルファキサロンTIVA", "dose": "0.07-0.1 mg/kg/min (4-6 mg/kg/hr)", "route": "IV CRI", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "プロポフォールより蓄積が少ない。中時間処置に適する。神経系疾患の患者に有用（GABA-A作動薬、頭蓋内圧上昇なし）。", "notes": "Less accumulation than propofol. Suitable for medium-duration procedures. Useful in neurological patients (GABA-A agonist, no ICP elevation)."},
                {"name": "Propofol + Ketamine + Dexmedetomidine", "name_ja": "PKD（プロポフォール-ケタミン-デクスメデトミジン）", "dose": "Propofol 0.1-0.2 mg/kg/min + Ketamine 5-10 µg/kg/min + Dexmedetomidine 1-2 µg/kg/hr", "route": "IV CRI (combined)", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "バランスTIVAの代表例。各薬剤を低用量で併用し、安定した麻酔を維持。揮発性麻酔薬が使用できない環境（野外、MRI等）で有用。", "notes": "Representative balanced TIVA. Low doses of each drug maintain stable anesthesia. Useful when volatile agents unavailable (field, MRI)."},
            ],
            "monitoring_params": [
                {"param": "Jaw tone / Eye position", "target": "Ventromedial rotation = adequate depth", "notes_ja": "吸入麻酔と異なりETCO2以外の麻酔深度指標が重要。顎の弛緩度と眼球位置を継続評価。", "notes": "Unlike inhalant anesthesia, depth monitoring relies more on clinical signs. Continuously assess jaw tone and eye position."},
                {"param": "HR / BP", "target": "HR 60-120 bpm, MAP ≥60 mmHg", "notes_ja": "TIVAでは揮発性麻酔薬より血圧維持が容易だが、オーバードーズに注意。", "notes": "BP is often better maintained with TIVA vs inhalant, but watch for overdose."},
            ],
            "notes_ja": "TIVAは揮発性麻酔薬が使用できない環境（野外手術、MRI、気管・咽頭手術）で不可欠。シリンジポンプ2-3台が理想。酸素供給は別途確保（アンビューバッグ等）。長時間（>1時間）のTIVAでは薬物蓄積に注意。",
            "notes": "TIVA is essential when volatile agents cannot be used (field surgery, MRI, tracheal/pharyngeal surgery). Ideally use 2-3 syringe pumps. Ensure separate oxygen delivery (Ambu bag). Watch for drug accumulation in prolonged (>1 hr) TIVA.",
        },
    ],
    "breed_considerations": [
        {"breed_ja": "短頭種（ブルドッグ、パグ、フレンチブル等）", "breed": "Brachycephalic (Bulldog, Pug, French Bulldog)",
         "notes_ja": "上気道閉塞リスク極めて高い。前酸素化を十分に行い、導入後速やかに気管挿管。覚醒時も最後まで気管チューブを維持。抜管後ステロイド（デキサメタゾン0.1 mg/kg IV）検討。", "notes": "Very high upper airway obstruction risk. Preoxygenate well, intubate promptly after induction. Keep ET tube until fully awake. Consider post-extubation dexamethasone 0.1 mg/kg IV."},
        {"breed_ja": "サイトハウンド（グレイハウンド、ボルゾイ等）", "breed": "Sighthounds (Greyhound, Borzoi)",
         "notes_ja": "チオペンタール感受性（CYP450活性低下）。プロポフォールの覚醒も遅延する場合あり。体脂肪率が低いため脂溶性薬の分布容積が変化。", "notes": "Thiopental sensitivity (reduced CYP450 activity). Propofol recovery may also be prolonged. Low body fat alters distribution of lipid-soluble drugs."},
        {"breed_ja": "大型・超大型犬（グレートデーン、セントバーナード等）", "breed": "Giant breeds (Great Dane, St. Bernard)",
         "notes_ja": "GDV（胃拡張捻転）リスク。麻酔後は食事制限。拡張型心筋症の併存を考慮した心エコー事前評価推奨。", "notes": "GDV risk post-anesthesia. Restrict food after recovery. Pre-anesthetic echocardiography recommended to rule out dilated cardiomyopathy."},
        {"breed_ja": "ボクサー", "breed": "Boxer",
         "notes_ja": "アセプロマジン過感受性（重度低血圧）。代替: デクスメデトミジンまたはミダゾラム。不整脈原性右室心筋症（ARVC）に注意。", "notes": "Acepromazine hypersensitivity (severe hypotension). Use dexmedetomidine or midazolam instead. Watch for arrhythmogenic right ventricular cardiomyopathy (ARVC)."},
    ],
}

# ============================================================
# CAT
# ============================================================
ANESTHESIA_PROTOCOLS["cat"] = {
    "species_name": {"ja": "猫", "en": "Cat"},
    "overview": {
        "ja": "猫は犬に比べ麻酔リスクが高い（喉頭痙攣、低体温、ストレス誘発性高体温）。IM注射による導入が一般的（静脈確保が困難な場合）。短頭種（ペルシャ等）は犬同様の上気道リスクあり。NSAIDsの代謝が犬より遅い（グルクロン酸抱合能力が低い）。",
        "en": "Cats have higher anesthesia risk than dogs (laryngospasm, hypothermia, stress-induced hyperthermia). IM induction is common when IV access is difficult. Brachycephalic breeds (Persian) carry similar airway risks. NSAIDs are metabolized more slowly (limited glucuronidation).",
    },
    "fasting": {
        "ja": "成猫: 6-8時間絶食、2時間絶水。子猫（<8週齢）: 2-4時間絶食。肥満猫の長時間絶食は肝リピドーシスリスク。",
        "en": "Adults: 6-8 hr food fast, 2 hr water fast. Kittens (<8 wk): 2-4 hr food fast. Prolonged fasting in obese cats risks hepatic lipidosis.",
    },
    "protocols": [
        {
            "name": {"ja": "軽度鎮静（検査・保定用）", "en": "Light Sedation (Examination/Restraint)"},
            "category": "sedation",
            "risk_level": "low",
            "drugs": [
                {"name": "Gabapentin (PO pre-visit)", "name_ja": "ガバペンチン（来院前経口）", "dose": "50-100 mg/cat (total dose)", "route": "PO", "onset": "1-2 hr", "duration": "8-12 hr",
                 "notes_ja": "来院1-2時間前に飼い主が投与。攻撃的な猫の検査をより安全に。液体製剤はキシリトール不含を確認。", "notes": "Owner administers 1-2 hr before visit. Makes examination of aggressive cats safer. Ensure liquid formulation is xylitol-free."},
                {"name": "Butorphanol", "name_ja": "ブトルファノール", "dose": "0.2-0.4 mg/kg", "route": "IM", "onset": "10-15 min", "duration": "1-2 hr",
                 "notes_ja": "軽度鎮静と鎮痛を提供。単独では信頼性が低い場合あり。", "notes": "Provides mild sedation and analgesia. May be unreliable as sole sedative."},
            ],
            "notes_ja": "恐怖・攻撃性の強い猫にはガバペンチンの事前投与が極めて有効。Cat-Friendly Practice推奨。",
            "notes": "Gabapentin pre-visit is highly effective for fearful/aggressive cats. Recommended by Cat-Friendly Practice guidelines.",
        },
        {
            "name": {"ja": "中等度鎮静（X線・超音波・軽処置）", "en": "Moderate Sedation (Radiography/Ultrasound/Minor Procedures)"},
            "category": "sedation",
            "risk_level": "low",
            "drugs": [
                {"name": "Dexmedetomidine + Butorphanol", "name_ja": "デクスメデトミジン＋ブトルファノール", "dose": "10-20 μg/kg + 0.2 mg/kg", "route": "IM", "onset": "10-15 min", "duration": "30-45 min",
                 "notes_ja": "猫の標準的な鎮静プロトコル。心疾患（特にHCM）には慎重に。拮抗: アティパメゾール同容量IM。", "notes": "Standard cat sedation protocol. Use cautiously in cardiac disease (especially HCM). Reverse: atipamezole equal volume IM."},
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "2-3 mg/kg", "route": "IM", "onset": "5-10 min", "duration": "20-40 min",
                 "notes_ja": "IM投与で確実な鎮静。注射量が多くなる（0.5 mL/kg程度）が、猫では広く使用される。", "notes": "Reliable sedation via IM. Injection volume is large (~0.5 mL/kg) but widely used in cats."},
            ],
            "notes_ja": "猫はストレスで体温上昇（>40°C）することがあり、真の発熱との鑑別が重要。",
            "notes": "Cats may develop stress-induced hyperthermia (>40°C); differentiate from true fever.",
        },
        {
            "name": {"ja": "前投薬（全身麻酔前）", "en": "Premedication (Before General Anesthesia)"},
            "category": "premedication",
            "risk_level": "low",
            "drugs": [
                {"name": "Dexmedetomidine + Buprenorphine", "name_ja": "デクスメデトミジン＋ブプレノルフィン", "dose": "5-10 μg/kg + 0.02 mg/kg", "route": "IM", "onset": "10-20 min", "duration": "4-6 hr (buprenorphine)",
                 "notes_ja": "猫の標準前投薬。ブプレノルフィンはOTM（口腔粘膜投与）も可能（0.02-0.03 mg/kg）。", "notes": "Standard cat premedication. Buprenorphine can also be given OTM (0.02-0.03 mg/kg)."},
                {"name": "Acepromazine + Methadone", "name_ja": "アセプロマジン＋メサドン", "dose": "0.01-0.05 mg/kg + 0.2-0.5 mg/kg", "route": "IM", "onset": "15-30 min", "duration": "2-4 hr",
                 "notes_ja": "HCM疑いの猫にはアセプロマジンが比較的安全（後負荷軽減）。", "notes": "Acepromazine is relatively safe in cats with suspected HCM (afterload reduction)."},
                {"name": "Midazolam + Buprenorphine", "name_ja": "ミダゾラム＋ブプレノルフィン", "dose": "0.2-0.3 mg/kg + 0.02 mg/kg", "route": "IM", "onset": "10-15 min", "duration": "1-2 hr",
                 "notes_ja": "高リスク患者（ASA III-V）。心血管系への影響最小。老齢猫にも安全。", "notes": "For high-risk patients (ASA III-V). Minimal cardiovascular effects. Safe in geriatric cats."},
            ],
            "notes_ja": "猫のHCM（肥大型心筋症）は無症状のことが多い。術前心エコーが理想的だが、最低限聴診でギャロップ・雑音を確認。",
            "notes": "Feline HCM is often asymptomatic. Pre-anesthetic echocardiography is ideal; at minimum, auscultate for gallop rhythm or murmur.",
        },
        {
            "name": {"ja": "導入（全身麻酔）", "en": "Induction (General Anesthesia)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Propofol", "name_ja": "プロポフォール", "dose": "2-6 mg/kg", "route": "IV (slow)", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "反復投与でハインツ小体貧血のリスク（3日以上の連続使用を避ける）。前投薬後は低用量で十分。", "notes": "Repeated use risks Heinz body anemia (avoid >3 consecutive days). Low dose sufficient after premedication."},
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "1-3 mg/kg IV / 2-5 mg/kg IM", "route": "IV/IM", "onset": "30-60 sec (IV)", "duration": "5-15 min",
                 "notes_ja": "IV確保が困難な場合にIM導入が可能（猫での大きな利点）。IM投与量は多めに必要。", "notes": "IM induction possible when IV access is difficult (major advantage in cats). Higher IM dose required."},
                {"name": "Ketamine + Midazolam", "name_ja": "ケタミン＋ミダゾラム", "dose": "5-7 mg/kg + 0.2 mg/kg", "route": "IM/IV", "onset": "2-5 min (IM)", "duration": "20-30 min",
                 "notes_ja": "IM導入が可能。野外や保定困難な猫に有用。HCM猫には注意（交感神経刺激）。", "notes": "IM induction possible. Useful for feral or difficult-to-restrain cats. Caution in HCM cats (sympathetic stimulation)."},
            ],
            "notes_ja": "猫の気管挿管は喉頭痙攣リスクが高い。リドカイン2%を喉頭にスプレー（0.1 mL）してから挿管。カフ圧は最小限に。",
            "notes": "Feline intubation carries high laryngospasm risk. Spray lidocaine 2% on larynx (0.1 mL) before intubation. Use minimal cuff pressure.",
        },
        {
            "name": {"ja": "維持（吸入麻酔）", "en": "Maintenance (Inhalation)"},
            "category": "maintenance",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Isoflurane", "name_ja": "イソフルラン", "dose": "MAC 1.63%（猫）", "route": "Inhalation", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "猫のMACは犬より高い。低体温で必要濃度が低下するため、濃度調節に注意。", "notes": "Cat MAC is higher than dogs. Hypothermia reduces MAC requirement; adjust concentration accordingly."},
                {"name": "Sevoflurane", "name_ja": "セボフルラン", "dose": "MAC 2.58%（猫）", "route": "Inhalation", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "マスク導入に適する（刺激臭が少ない）。覚醒が速い。", "notes": "Suitable for mask induction (less pungent). Faster recovery."},
            ],
            "notes_ja": "猫の維持輸液は3-5 mL/kg/hr。過剰輸液は肺水腫リスク（特にHCM猫）。体温管理を徹底（猫は低体温になりやすい）。",
            "notes": "Cat maintenance fluids: 3-5 mL/kg/hr. Fluid overload risks pulmonary edema (especially HCM cats). Aggressive temperature management essential.",
        },
        {
            "name": {"ja": "局所・区域麻酔", "en": "Local/Regional Anesthesia"},
            "category": "local_regional",
            "risk_level": "low",
            "drugs": [
                {"name": "Lidocaine", "name_ja": "リドカイン", "dose": "Max 4 mg/kg（猫）", "route": "Local infiltration / Nerve block", "onset": "5-10 min", "duration": "60-90 min",
                 "notes_ja": "猫の最大用量は犬（6 mg/kg）より低い。IV投与は心毒性リスクが高く避ける。", "notes": "Cat maximum dose is lower than dogs (6 mg/kg). Avoid IV administration due to high cardiotoxicity risk."},
                {"name": "Bupivacaine", "name_ja": "ブピバカイン", "dose": "Max 1-2 mg/kg（猫）", "route": "Local infiltration / Nerve block", "onset": "15-20 min", "duration": "4-6 hr",
                 "notes_ja": "OVH（卵巣子宮摘出）時の腹腔内投与（1 mg/kg生食で希釈）が有効。", "notes": "Intraperitoneal use (1 mg/kg diluted in saline) effective for OVH."},
            ],
            "notes_ja": "猫の去勢手術では精巣内ブロック（リドカイン1-2 mg/精巣）が簡便で有効。",
            "notes": "Intratesticular block (lidocaine 1-2 mg/testicle) is simple and effective for cat castration.",
        },
        {
            "name": {"ja": "モニタリング", "en": "Monitoring Guidelines"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "SpO2", "target": ">95%", "notes_ja": "猫の小さな舌ではプローブ装着が難しい場合あり。趾パッドも使用可。", "notes": "Probe placement on small cat tongues can be difficult. Toe pads are an alternative."},
                {"param": "ETCO2", "target": "35-45 mmHg", "notes_ja": "回路デッドスペースに注意（猫用小型コネクタ使用）。", "notes": "Watch for circuit dead space (use small feline connectors)."},
                {"param": "HR", "target": "120-200 bpm", "notes_ja": "猫は犬より高い心拍数が正常。100未満は要対応。", "notes": "Cats have higher normal HR than dogs. Below 100 requires intervention."},
                {"param": "MAP", "target": "60-100 mmHg", "notes_ja": "ドップラーが猫では使いやすい。", "notes": "Doppler is often easier in cats."},
                {"param": "Temperature", "target": "37.5-39.0°C", "notes_ja": "猫は低体温に非常になりやすい。積極的加温を。", "notes": "Cats are very prone to hypothermia. Active warming essential."},
            ],
            "notes_ja": "猫は犬よりも小さいため、輸液量・薬用量の計算は特に正確に。体重を必ず実測。",
            "notes": "Cats are smaller than dogs; calculate fluid and drug doses with particular precision. Always weigh the patient.",
        },
        {
            "name": {"ja": "覚醒・回復", "en": "Recovery"},
            "category": "recovery",
            "risk_level": "low",
            "drugs": [
                {"name": "Atipamezole", "name_ja": "アティパメゾール", "dose": "Same volume as dexmedetomidine", "route": "IM", "onset": "5-10 min", "duration": "",
                 "notes_ja": "鎮痛も拮抗するため、ブプレノルフィンOTMなどの鎮痛を先に確保。", "notes": "Also reverses analgesia; ensure buprenorphine OTM or other analgesia is in place first."},
            ],
            "notes_ja": "覚醒時の環境は静かに暗く。猫は覚醒時のストレスで高体温を呈することがある。攻撃的になる場合があるため、タオルで覆うなどの対応。",
            "notes": "Recovery area should be quiet and dim. Cats may become hyperthermic or aggressive during recovery. Cover with towel if needed.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Atropine", "name_ja": "アトロピン", "dose": "0.02-0.04 mg/kg", "route": "IV", "onset": "1-2 min", "duration": "15-30 min",
                 "notes_ja": "猫の徐脈に対する第一選択。", "notes": "First-line for feline bradycardia."},
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.01 mg/kg", "route": "IV / IT", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時: 0.01 mg/kg IV q3-5min。", "notes": "CPA: 0.01 mg/kg IV q3-5min."},
            ],
            "notes_ja": "猫のCPR: 胸骨圧迫100-120回/min。小型のため片手での圧迫が可能。新生猫: 鼻口を吸引後、軽い刺激と酸素投与。",
            "notes": "Cat CPR: chest compressions 100-120/min. Single-hand technique possible due to small size. Neonatal kittens: suction nose/mouth, gentle stimulation, and oxygen.",
        },
        {
            "name": {"ja": "CRI鎮痛（持続定量点滴）", "en": "CRI Analgesia (Constant Rate Infusion)"},
            "category": "maintenance",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Fentanyl CRI", "name_ja": "フェンタニルCRI", "dose": "2-5 µg/kg/hr (loading: 2 µg/kg IV slow)", "route": "IV CRI", "onset": "2-3 min", "duration": "Continuous",
                 "notes_ja": "猫の術中CRI鎮痛の第一選択。犬と同用量だが体格に合わせた正確な計算が必須。徐脈に注意。興奮（ユーフォリア）を呈する場合あり。", "notes": "First-line intraoperative CRI analgesic for cats. Same dose range as dogs but precise calculation essential for small body size. Watch for bradycardia. May cause euphoria/excitement."},
                {"name": "Remifentanil CRI", "name_ja": "レミフェンタニルCRI", "dose": "5-15 µg/kg/hr", "route": "IV CRI", "onset": "1-2 min", "duration": "Continuous (ultra-short acting)",
                 "notes_ja": "猫でも犬同様に安全に使用可能。中止後速やかに効果消失。術後のブプレノルフィンOTMへの移行を計画。", "notes": "Safe in cats as in dogs. Rapid offset after stopping. Plan transition to buprenorphine OTM for post-op analgesia."},
                {"name": "Ketamine CRI", "name_ja": "ケタミンCRI", "dose": "2-10 µg/kg/min (loading: 0.5 mg/kg IV)", "route": "IV CRI", "onset": "1-2 min", "duration": "Continuous",
                 "notes_ja": "NMDA受容体拮抗。猫のワインドアップ予防に有効。オピオイドとの併用が一般的。猫は覚醒時にケタミン後のディスフォリアを呈しやすいため低用量を維持。", "notes": "NMDA antagonist. Effective for wind-up prevention in cats. Commonly combined with opioids. Maintain low doses as cats are prone to ketamine-associated dysphoria during recovery."},
                {"name": "Dexmedetomidine CRI", "name_ja": "デクスメデトミジンCRI", "dose": "0.5-1 µg/kg/hr", "route": "IV CRI", "onset": "5-10 min", "duration": "Continuous",
                 "notes_ja": "猫では犬より低用量を使用。鎮静・鎮痛・MAC削減。徐脈・嘔吐に注意。心疾患（HCMなど）の猫には慎重投与。", "notes": "Use lower doses than dogs. Sedation, analgesia, MAC reduction. Watch for bradycardia and vomiting. Use cautiously in cats with cardiac disease (HCM)."},
            ],
            "notes_ja": "猫のCRI鎮痛ではリドカインCRIは禁忌（心毒性）。フェンタニル+ケタミンの組み合わせ（FK）が猫のマルチモーダルCRIの標準。シリンジポンプ必須（微量投与の精度確保）。",
            "notes": "Lidocaine CRI is CONTRAINDICATED in cats (cardiotoxicity). Fentanyl + Ketamine (FK) combination is the standard feline multimodal CRI. Syringe pump mandatory for dosing accuracy at small volumes.",
        },
        {
            "name": {"ja": "TIVA（全静脈麻酔）", "en": "TIVA (Total Intravenous Anesthesia)"},
            "category": "maintenance",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Propofol TIVA", "name_ja": "プロポフォールTIVA", "dose": "0.1-0.3 mg/kg/min (6-18 mg/kg/hr)", "route": "IV CRI", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "猫はプロポフォールの代謝が犬より遅い。連日投与は酸化的傷害（ハインツ小体貧血）のリスクあり。短時間処置に限定。", "notes": "Cats metabolize propofol more slowly than dogs. Repeated daily use risks oxidative damage (Heinz body anemia). Limit to short procedures."},
                {"name": "Alfaxalone TIVA", "name_ja": "アルファキサロンTIVA", "dose": "0.05-0.1 mg/kg/min (3-6 mg/kg/hr)", "route": "IV CRI", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "猫ではプロポフォールより安全なTIVA選択肢。蓄積性が低く、酸化的傷害のリスクなし。中時間処置にも適する。", "notes": "Safer TIVA option than propofol in cats. Less accumulation, no oxidative damage risk. Suitable for medium-duration procedures."},
                {"name": "Alfaxalone + Fentanyl + Ketamine", "name_ja": "AFK（アルファキサロン-フェンタニル-ケタミン）", "dose": "Alfaxalone 0.05-0.07 mg/kg/min + Fentanyl 3-5 µg/kg/hr + Ketamine 2-5 µg/kg/min", "route": "IV CRI (combined)", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "猫のバランスTIVAの推奨プロトコル。リドカインが使えない猫ではMLKの代替。各薬剤を低用量で併用し、安定した麻酔維持を実現。", "notes": "Recommended balanced TIVA protocol for cats. Alternative to MLK since lidocaine is contraindicated in cats. Low doses of each drug provide stable anesthesia."},
            ],
            "monitoring_params": [
                {"param": "Jaw tone / Eye position", "target": "Ventromedial rotation = adequate depth", "notes_ja": "猫の眼球は犬より小さく、位置判定がやや困難。瞬膜の位置も参考に。", "notes": "Cat eyes are smaller; position assessment can be harder. Third eyelid position is a useful additional indicator."},
                {"param": "HR / BP", "target": "HR 120-200 bpm, MAP ≥60 mmHg", "notes_ja": "猫は犬より高い心拍数が正常。ドップラーによる血圧測定が猫では容易。", "notes": "Cats have higher baseline HR. Doppler BP measurement is often easier in cats."},
            ],
            "notes_ja": "猫のTIVAではアルファキサロンがプロポフォールより推奨される（特に繰り返し使用時）。気管・咽頭手術時のTIVAでは、喉頭痙攣予防のためリドカインスプレー（喉頭に局所塗布、少量）を追加検討。",
            "notes": "Alfaxalone is preferred over propofol for feline TIVA (especially for repeated use). For tracheal/pharyngeal surgery TIVA, consider topical lidocaine spray on larynx (small amount) to prevent laryngospasm.",
        },
    ],
}

# ============================================================
# HORSE
# ============================================================
ANESTHESIA_PROTOCOLS["horse"] = {
    "species_name": {"ja": "馬", "en": "Horse"},
    "overview": {
        "ja": "馬の全身麻酔は他の種に比べ死亡率が高い（約1%、小動物の約10倍）。体格に起因する筋障害（ミオパチー）、低血圧、覚醒時の骨折リスクが主な合併症。可能な限り立位鎮静＋局所麻酔を選択する。",
        "en": "Equine general anesthesia has higher mortality (~1%, ~10x small animals). Major complications: myopathy from recumbency, hypotension, and recovery fractures. Standing sedation + local anesthesia is preferred whenever possible.",
    },
    "fasting": {
        "ja": "12時間絶食（可能なら）、2-4時間絶水。馬は嘔吐できないため誤嚥リスクは低いが、腸管ガス軽減のため絶食推奨。",
        "en": "12 hr food fast (if possible), 2-4 hr water fast. Horses cannot vomit so aspiration risk is low, but fasting reduces intestinal gas.",
    },
    "protocols": [
        {
            "name": {"ja": "立位鎮静（検査・歯科・小外科）", "en": "Standing Sedation (Examination/Dentistry/Minor Surgery)"},
            "category": "sedation",
            "risk_level": "low",
            "drugs": [
                {"name": "Xylazine", "name_ja": "キシラジン", "dose": "0.3-1.1 mg/kg", "route": "IV", "onset": "2-5 min", "duration": "20-40 min",
                 "notes_ja": "馬で最も一般的なα2作動薬。用量依存性の運動失調。ヨヒンビンで拮抗可能。", "notes": "Most common alpha-2 agonist in horses. Dose-dependent ataxia. Reversible with yohimbine."},
                {"name": "Detomidine", "name_ja": "デトミジン", "dose": "10-40 μg/kg", "route": "IV/IM", "onset": "2-5 min (IV)", "duration": "30-90 min",
                 "notes_ja": "キシラジンより強力で持続時間が長い。OTG（口腔粘膜ジェル）製剤あり（Dormosedan Gel）。", "notes": "More potent and longer-lasting than xylazine. OTG gel formulation available (Dormosedan Gel)."},
                {"name": "Romifidine", "name_ja": "ロミフィジン", "dose": "40-120 μg/kg", "route": "IV", "onset": "3-5 min", "duration": "40-100 min",
                 "notes_ja": "運動失調が最も少ないα2作動薬。立位手術に最適。", "notes": "Least ataxia among alpha-2 agonists. Best for standing procedures."},
            ],
            "notes_ja": "立位鎮静＋局所麻酔は全身麻酔に比べ安全性が格段に高い。創傷修復、歯科処置、去勢手術、眼科処置、上気道手術が可能。",
            "notes": "Standing sedation + local anesthesia is significantly safer than general anesthesia. Enables wound repair, dentistry, castration, ophthalmology, and upper airway surgery.",
        },
        {
            "name": {"ja": "立位鎮静＋鎮痛（疼痛性処置）", "en": "Standing Sedation + Analgesia (Painful Procedures)"},
            "category": "sedation",
            "risk_level": "low",
            "drugs": [
                {"name": "Detomidine + Butorphanol", "name_ja": "デトミジン＋ブトルファノール", "dose": "10-20 μg/kg + 0.01-0.04 mg/kg", "route": "IV", "onset": "3-5 min", "duration": "30-60 min",
                 "notes_ja": "立位手術の標準プロトコル。CRI: デトミジン6 μg/kg/hr + ブトルファノール13 μg/kg/hr。", "notes": "Standard standing surgery protocol. CRI: detomidine 6 μg/kg/hr + butorphanol 13 μg/kg/hr."},
                {"name": "Detomidine + Morphine", "name_ja": "デトミジン＋モルヒネ", "dose": "10-20 μg/kg + 0.05-0.1 mg/kg", "route": "IV", "onset": "3-5 min", "duration": "45-90 min",
                 "notes_ja": "より強い鎮痛。腸管運動抑制に注意（疝痛リスク）。", "notes": "Stronger analgesia. Monitor for GI motility reduction (colic risk)."},
            ],
            "notes_ja": "CRI（持続点滴）で安定した鎮静レベルを維持。Head standまたはスリングで頭部支持。",
            "notes": "CRI provides stable sedation level. Support head with head stand or sling.",
        },
        {
            "name": {"ja": "導入（全身麻酔）", "en": "Induction (General Anesthesia)"},
            "category": "induction",
            "risk_level": "high",
            "drugs": [
                {"name": "Ketamine + Midazolam/Diazepam", "name_ja": "ケタミン＋ミダゾラム/ジアゼパム", "dose": "2.2 mg/kg + 0.06 mg/kg", "route": "IV (rapid)", "onset": "30-60 sec", "duration": "15-20 min",
                 "notes_ja": "馬の標準導入法。α2前投薬後にケタミン＋ジアゼパムを急速IV。尾引き（Tail pull）で倒馬確認。", "notes": "Standard equine induction. After alpha-2 premedication, rapid IV ketamine + diazepam. Confirm recumbency with tail pull test."},
                {"name": "Thiopental", "name_ja": "チオペンタール", "dose": "4-6 mg/kg", "route": "IV (rapid)", "onset": "15-30 sec", "duration": "10-15 min",
                 "notes_ja": "ケタミンの代替。血管外漏出で組織壊死のリスク。確実なカテーテル留置を確認。", "notes": "Alternative to ketamine. Perivascular injection causes tissue necrosis. Ensure secure catheter placement."},
                {"name": "TIVA (Ketamine + Xylazine + GGE)", "name_ja": "TIVA（ケタミン＋キシラジン＋GGE）", "dose": "Triple drip", "route": "IV infusion", "onset": "5-10 min", "duration": "30-60 min",
                 "notes_ja": "野外麻酔（フィールドアネステジア）の標準。去勢、短時間手術に適する。GGE 50mg/mL + ケタミン1mg/mL + キシラジン0.5mg/mL、1-2 mL/kg/hr。", "notes": "Standard field anesthesia. Suitable for castration, short procedures. GGE 50mg/mL + ketamine 1mg/mL + xylazine 0.5mg/mL, 1-2 mL/kg/hr."},
            ],
            "notes_ja": "導入は十分にパッドのある部屋（倒馬用マット）で実施。尾を持ち、ゆっくり倒れるよう誘導。頭部を保護。",
            "notes": "Induction in well-padded room (knockdown mats). Hold tail and guide horse down gently. Protect head.",
        },
        {
            "name": {"ja": "維持（吸入麻酔）", "en": "Maintenance (Inhalation)"},
            "category": "maintenance",
            "risk_level": "high",
            "drugs": [
                {"name": "Isoflurane", "name_ja": "イソフルラン", "dose": "MAC 1.31%（馬）", "route": "Inhalation", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "低血圧が最大のリスク。MAP≥70 mmHgを維持目標。ドブタミン（1-5 μg/kg/min）で血圧サポート。", "notes": "Hypotension is the primary risk. Target MAP≥70 mmHg. Support with dobutamine (1-5 μg/kg/min)."},
                {"name": "Sevoflurane", "name_ja": "セボフルラン", "dose": "MAC 2.31%（馬）", "route": "Inhalation", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "覚醒がイソフルランより速い。覚醒の質への影響は議論あり。", "notes": "Faster recovery than isoflurane. Effect on recovery quality is debated."},
            ],
            "notes_ja": "馬の維持輸液: 5-10 mL/kg/hr（乳酸リンゲル）。体位変換（30分毎）でミオパチー予防。術中CRI（リドカイン50 μg/kg/min、ケタミン1.5 mg/kg/hr）で吸入濃度削減（MAC-sparing）。",
            "notes": "Maintenance fluids: 5-10 mL/kg/hr LRS. Reposition q30min to prevent myopathy. Intraoperative CRI (lidocaine 50 μg/kg/min, ketamine 1.5 mg/kg/hr) for MAC-sparing.",
        },
        {
            "name": {"ja": "局所・区域麻酔", "en": "Local/Regional Anesthesia"},
            "category": "local_regional",
            "risk_level": "low",
            "drugs": [
                {"name": "Lidocaine 2%", "name_ja": "リドカイン2%", "dose": "Max 5 mg/kg（馬）", "route": "Local infiltration / Nerve block", "onset": "5-10 min", "duration": "60-90 min",
                 "notes_ja": "皮膚切開の浸潤麻酔、歯科神経ブロック（下顎神経、眼窩下神経）、四肢神経ブロック（掌側神経、蹄踵神経）。", "notes": "Skin infiltration, dental nerve blocks (mandibular, infraorbital), limb nerve blocks (palmar, heel)."},
                {"name": "Mepivacaine 2%", "name_ja": "メピバカイン2%", "dose": "Max 5 mg/kg（馬）", "route": "Perineural / Intra-articular", "onset": "5-15 min", "duration": "90-120 min",
                 "notes_ja": "馬の診断的神経ブロックに最も使用される。関節内注射にも適する。組織刺激性がリドカインより低い。", "notes": "Most commonly used for diagnostic nerve blocks in horses. Also suitable for intra-articular injection. Less tissue irritation than lidocaine."},
                {"name": "Epidural (Xylazine + Lidocaine)", "name_ja": "硬膜外（キシラジン＋リドカイン）", "dose": "Xylazine 0.17 mg/kg + Lidocaine 0.22 mg/kg", "route": "Caudal epidural (Co1-Co2)", "onset": "10-15 min", "duration": "1-3 hr",
                 "notes_ja": "会陰部手術（Caslick修復、直腸脱等）に有効。後肢の運動機能は保持される（低用量）。", "notes": "Effective for perineal surgery (Caslick repair, rectal prolapse). Hindlimb motor function preserved at low doses."},
            ],
            "notes_ja": "馬では立位鎮静＋局所/区域麻酔の組み合わせが全身麻酔に代わる最も安全な選択肢。",
            "notes": "Standing sedation + local/regional anesthesia is the safest alternative to general anesthesia in horses.",
        },
        {
            "name": {"ja": "モニタリング", "en": "Monitoring Guidelines"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "MAP (arterial)", "target": "≥70 mmHg", "notes_ja": "顔面動脈 or 横尾動脈にカテーテル留置で直接測定。MAP<70で腎・筋灌流不全→ミオパチーリスク増大。ドブタミン1-5 μg/kg/minで対応。", "notes": "Direct measurement via facial or transverse facial artery catheter. MAP<70 risks renal/muscle hypoperfusion and myopathy. Treat with dobutamine 1-5 μg/kg/min."},
                {"param": "SpO2/PaO2", "target": "PaO2 >80 mmHg", "notes_ja": "馬は側臥位で換気血流ミスマッチが起こりやすい。PaO2<200 mmHg（FiO2 100%下）は注意。IPPV検討。", "notes": "Horses develop V/Q mismatch in lateral recumbency. PaO2<200 mmHg on 100% O2 is concerning. Consider IPPV."},
                {"param": "ETCO2", "target": "40-50 mmHg", "notes_ja": "馬は成人に比べ高めが許容される。>60で人工換気（IPPV）開始。", "notes": "Slightly higher levels acceptable in horses. Start IPPV if >60."},
                {"param": "Temperature", "target": "37.0-38.5°C", "notes_ja": "悪性高熱症は稀だが存在する。低体温は大型馬では稀（筋肉量で体温維持）。", "notes": "Malignant hyperthermia is rare but exists. Hypothermia rare in large horses (muscle mass maintains temperature)."},
            ],
            "notes_ja": "馬の全身麻酔では動脈血圧の直接モニタリングが必須。5分毎の血液ガス分析が理想的。",
            "notes": "Direct arterial blood pressure monitoring is essential for equine GA. Arterial blood gas analysis q5min is ideal.",
        },
        {
            "name": {"ja": "覚醒・回復", "en": "Recovery"},
            "category": "recovery",
            "risk_level": "high",
            "drugs": [],
            "notes_ja": "覚醒は馬の麻酔で最も危険なフェーズ。パッドのある回復室を使用。ヘッド＆テールロープで補助。鎮静延長（ロミフィジン0.01 mg/kg IV）やacceptable sedation recovery（意図的に鎮静下で覚醒）を検討。完全に立てるまで監視。回復失敗（骨折等）は安楽死に至ることがある。",
            "notes": "Recovery is the most dangerous phase of equine anesthesia. Use padded recovery room. Assist with head and tail ropes. Consider sedation prolongation (romifidine 0.01 mg/kg IV) or assisted recovery techniques. Monitor until standing. Failed recovery (fracture) may necessitate euthanasia.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Atropine", "name_ja": "アトロピン", "dose": "0.01-0.02 mg/kg", "route": "IV", "onset": "1-2 min", "duration": "30-60 min",
                 "notes_ja": "馬の徐脈には慎重に使用（腸管運動停止→疝痛リスク）。低用量から。", "notes": "Use cautiously in horses (GI stasis → colic risk). Start with low dose."},
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.01-0.02 mg/kg", "route": "IV", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。馬のCPRは体格的に困難（外的胸骨圧迫は効果限定的）。", "notes": "For CPA. Equine CPR is physically challenging (external chest compressions have limited efficacy)."},
                {"name": "Dobutamine", "name_ja": "ドブタミン", "dose": "1-5 μg/kg/min", "route": "IV CRI", "onset": "1-2 min", "duration": "Continuous",
                 "notes_ja": "術中低血圧の第一選択昇圧剤。MAP≥70 mmHg維持を目標。", "notes": "First-line vasopressor for intraoperative hypotension. Target MAP≥70 mmHg."},
            ],
            "notes_ja": "馬の術中心停止は予後不良。予防（適切な血圧管理、輸液、体位変換）が最重要。",
            "notes": "Intraoperative cardiac arrest in horses carries a very poor prognosis. Prevention (proper BP management, fluids, repositioning) is paramount.",
        },
    ],
}

# ============================================================
# RABBIT
# ============================================================
ANESTHESIA_PROTOCOLS["rabbit"] = {
    "species_name": {"ja": "うさぎ", "en": "Rabbit"},
    "overview": {
        "ja": "ウサギの麻酔死亡率は犬猫に比べ高い（健康個体で約1.4%、疾患個体で約7.4%）。気管挿管が困難（盲目挿管 or V-gel使用）。呼吸停止しやすく、覚醒が遅い。必ず術前の完全な身体検査（特に呼吸器状態）を実施。",
        "en": "Rabbit anesthetic mortality is higher than dogs/cats (~1.4% healthy, ~7.4% sick). Intubation is difficult (blind technique or V-gel). Prone to respiratory arrest and prolonged recovery. Always perform complete pre-anesthetic examination (especially respiratory status).",
    },
    "fasting": {
        "ja": "絶食不要（ウサギは嘔吐できない）。ただし、口腔内の食物を除去。絶水も不要。長時間絶食はGI stasisリスク。",
        "en": "No fasting required (rabbits cannot vomit). Remove food from oral cavity. No water restriction. Prolonged fasting risks GI stasis.",
    },
    "protocols": [
        {
            "name": {"ja": "鎮静（検査・軽処置）", "en": "Sedation (Examination/Minor Procedures)"},
            "category": "sedation",
            "risk_level": "low",
            "drugs": [
                {"name": "Midazolam + Butorphanol", "name_ja": "ミダゾラム＋ブトルファノール", "dose": "0.5-1.0 mg/kg + 0.3-0.5 mg/kg", "route": "IM/SC/IN", "onset": "5-15 min", "duration": "30-60 min",
                 "notes_ja": "安全性が高い。鼻腔内（IN）投与も有効（ストレス軽減）。拮抗可能。", "notes": "High safety margin. Intranasal (IN) route effective (reduces stress). Reversible."},
                {"name": "Dexmedetomidine + Midazolam", "name_ja": "デクスメデトミジン＋ミダゾラム", "dose": "50-100 μg/kg + 0.5 mg/kg", "route": "IM/SC", "onset": "10-15 min", "duration": "30-60 min",
                 "notes_ja": "より深い鎮静。徐脈に注意。アティパメゾールで拮抗可能。", "notes": "Deeper sedation. Watch for bradycardia. Reversible with atipamezole."},
            ],
            "notes_ja": "ウサギは保定ストレスで死亡することがある。優しく扱い、後肢を必ずサポート。仰臥位（トランス状態）は呼吸抑制リスクあり。",
            "notes": "Rabbits can die from restraint stress. Handle gently, always support hindquarters. Dorsal recumbency (trance) carries respiratory depression risk.",
        },
        {
            "name": {"ja": "前投薬＋導入", "en": "Premedication + Induction"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Ketamine + Medetomidine + Butorphanol", "name_ja": "ケタミン＋メデトミジン＋ブトルファノール", "dose": "15 mg/kg + 0.25 mg/kg + 0.3 mg/kg", "route": "IM/SC", "onset": "10-15 min", "duration": "30-60 min",
                 "notes_ja": "IM投与で導入可能。気管挿管を行い吸入麻酔に移行。アティパメゾールで部分拮抗可。", "notes": "IM induction possible. Intubate and transition to inhalation. Partially reversible with atipamezole."},
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "2-3 mg/kg IV / 3-5 mg/kg IM", "route": "IV/IM", "onset": "1-3 min (IV)", "duration": "10-20 min",
                 "notes_ja": "IM投与可能で静脈確保困難なウサギに便利。注射量がやや多い。", "notes": "IM route convenient for rabbits with difficult IV access. Injection volume somewhat large."},
                {"name": "Propofol", "name_ja": "プロポフォール", "dose": "3-6 mg/kg", "route": "IV (耳静脈)", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "耳介辺縁静脈からのIV投与。EMLAクリーム事前塗布で穿刺を容易に。", "notes": "IV via marginal ear vein. Pre-apply EMLA cream to facilitate venipuncture."},
            ],
            "notes_ja": "気管挿管はサイズ2.0-4.0 ETチューブ。盲目挿管（呼吸音聴取）、V-gel（声門上気道デバイス）、内視鏡ガイドが選択肢。V-gelはウサギ用に設計されており推奨。",
            "notes": "Intubation with 2.0-4.0 ET tube. Options: blind technique (listen for breath sounds), V-gel (supraglottic airway device), endoscope-guided. V-gel is specifically designed for rabbits and recommended.",
        },
        {
            "name": {"ja": "維持（吸入麻酔）", "en": "Maintenance (Inhalation)"},
            "category": "maintenance",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Isoflurane", "name_ja": "イソフルラン", "dose": "MAC 2.05%（ウサギ）", "route": "Inhalation", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "ウサギのMACは犬猫より高い。呼吸抑制に注意（無呼吸になりやすい）。IPPV準備。", "notes": "Rabbit MAC is higher than dogs/cats. Watch for respiratory depression (prone to apnea). Have IPPV ready."},
                {"name": "Sevoflurane", "name_ja": "セボフルラン", "dose": "MAC 3.7%（ウサギ）", "route": "Inhalation", "onset": "Immediate", "duration": "Continuous",
                 "notes_ja": "覚醒が速い。マスク導入にも使用可能。", "notes": "Faster recovery. Can be used for mask induction."},
            ],
            "notes_ja": "ウサギの維持輸液: 5-10 mL/kg/hr。低体温防止を徹底（加温パッド、温風ブランケット必須）。呼吸数のモニタリングが重要。",
            "notes": "Maintenance fluids: 5-10 mL/kg/hr. Prevent hypothermia aggressively (warming pad, forced-air blanket essential). Respiratory rate monitoring is critical.",
        },
        {
            "name": {"ja": "局所麻酔", "en": "Local Anesthesia"},
            "category": "local_regional",
            "risk_level": "low",
            "drugs": [
                {"name": "Lidocaine", "name_ja": "リドカイン", "dose": "Max 3 mg/kg", "route": "Local infiltration", "onset": "5-10 min", "duration": "60-90 min",
                 "notes_ja": "最大用量は犬猫より低い。皮膚縫合、去勢時の精巣内ブロック。", "notes": "Maximum dose lower than dogs/cats. Skin suturing, intratesticular block for castration."},
                {"name": "Bupivacaine", "name_ja": "ブピバカイン", "dose": "Max 1 mg/kg", "route": "Local infiltration", "onset": "15-20 min", "duration": "4-6 hr",
                 "notes_ja": "術後鎮痛に有効。切開部位への浸潤。", "notes": "Effective for postoperative analgesia. Infiltration at incision site."},
                {"name": "EMLA cream", "name_ja": "EMLAクリーム", "dose": "Apply 30-60 min before", "route": "Topical (ears)", "onset": "30-60 min", "duration": "1-2 hr",
                 "notes_ja": "耳静脈穿刺前に耳介に塗布。カテーテル留置を容易にする。", "notes": "Apply to ear pinnae before marginal ear vein catheterization. Facilitates IV access."},
            ],
            "notes_ja": "局所麻酔は全身麻酔薬の使用量を減らし、ウサギの安全性を向上させる。",
            "notes": "Local anesthesia reduces general anesthetic requirements and improves safety in rabbits.",
        },
        {
            "name": {"ja": "モニタリング", "en": "Monitoring Guidelines"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "SpO2", "target": ">95%", "notes_ja": "プローブは耳・趾に装着。呼吸停止は急に起こる。", "notes": "Place probe on ear or digit. Respiratory arrest can occur suddenly."},
                {"param": "ETCO2", "target": "30-40 mmHg", "notes_ja": "V-gel使用時でも測定可能。呼吸数と併せて評価。", "notes": "Measurable even with V-gel. Evaluate alongside respiratory rate."},
                {"param": "HR", "target": "130-325 bpm", "notes_ja": "心拍数が非常に速い。ドップラーで聴取。150未満は低すぎる。", "notes": "Very fast heart rate. Use Doppler. Below 150 is too low."},
                {"param": "RR", "target": "30-60 /min", "notes_ja": "呼吸抑制は最も危険な合併症。胸郭の動きを常に監視。", "notes": "Respiratory depression is the most dangerous complication. Monitor chest wall movement continuously."},
                {"param": "Temperature", "target": "38.5-40.0°C", "notes_ja": "ウサギは非常に低体温になりやすい。加温を全例で実施。", "notes": "Rabbits are extremely prone to hypothermia. Active warming in all cases."},
            ],
            "notes_ja": "ウサギの眼球は閉じたままでも角膜乾燥しやすい。眼軟膏を必ず塗布。眼球の位置は麻酔深度の指標にはならない。",
            "notes": "Rabbit corneas dry easily even with lids closed. Always apply eye lubricant. Eye position is NOT a reliable depth indicator in rabbits.",
        },
        {
            "name": {"ja": "覚醒・回復", "en": "Recovery"},
            "category": "recovery",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Atipamezole", "name_ja": "アティパメゾール", "dose": "1 mg/kg", "route": "IM/SC", "onset": "5-10 min", "duration": "",
                 "notes_ja": "メデトミジン/デクスメデトミジンの拮抗。投与後の覚醒促進。", "notes": "Reverses medetomidine/dexmedetomidine. Promotes faster recovery."},
            ],
            "notes_ja": "覚醒後すぐに乾草・水を提供（GI stasis予防）。術後鎮痛: メロキシカム0.3-0.5 mg/kg SC/PO q24h。腸管運動促進を確認。覚醒に時間がかかる場合は体温チェック。",
            "notes": "Offer hay and water immediately after recovery (GI stasis prevention). Post-op analgesia: meloxicam 0.3-0.5 mg/kg SC/PO q24h. Confirm GI motility. If slow recovery, check temperature.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Atropine", "name_ja": "アトロピン", "dose": "0.05 mg/kg", "route": "IV/IM", "onset": "1-2 min", "duration": "15-30 min",
                 "notes_ja": "約30%のウサギはアトロピナーゼを持ち、効果が減弱。効果不十分ならグリコピロレート使用。", "notes": "~30% of rabbits have atropinase, reducing effectiveness. Use glycopyrrolate if inadequate response."},
                {"name": "Glycopyrrolate", "name_ja": "グリコピロレート", "dose": "0.01-0.02 mg/kg", "route": "IV/IM", "onset": "2-3 min", "duration": "30-60 min",
                 "notes_ja": "アトロピナーゼ陽性のウサギにはグリコピロレートが推奨。", "notes": "Recommended for rabbits with atropinase."},
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.01 mg/kg", "route": "IV/IO", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。骨髄内（IO: 脛骨近位端）投与も検討。", "notes": "For CPA. Consider intraosseous (IO: proximal tibia) route."},
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "2-5 mg/kg", "route": "IV", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時の呼吸刺激。即効性。", "notes": "Respiratory stimulant for apnea. Rapid onset."},
            ],
            "notes_ja": "ウサギの心停止時はまず100% O2投与＋胸骨圧迫。エピネフリンは3-5分毎。体温が下がっている場合は積極的加温。",
            "notes": "For rabbit CPA: 100% O2 + chest compressions first. Epinephrine q3-5min. Active warming if hypothermic.",
        },
    ],
}

# ============================================================
# HAMSTER
# ============================================================
ANESTHESIA_PROTOCOLS["hamster"] = {
    "species_name": {"ja": "ハムスター", "en": "Hamster"},
    "overview": {
        "ja": "ハムスターは非常に小さく（30-150g）、麻酔リスクが高い。低体温、低血糖、呼吸抑制が主な合併症。頬袋に食物が残っていることがあり、気道閉塞の原因となる。短い処置はイソフルラン吸入のみで可能。",
        "en": "Hamsters are very small (30-150g) with high anesthetic risk. Major complications: hypothermia, hypoglycemia, respiratory depression. Check cheek pouches for food (aspiration risk). Short procedures can be done with isoflurane inhalation alone.",
    },
    "fasting": {
        "ja": "絶食不要（低血糖リスク）。頬袋の食物を除去。",
        "en": "No fasting required (hypoglycemia risk). Empty cheek pouches.",
    },
    "protocols": [
        {
            "name": {"ja": "吸入麻酔（短時間処置）", "en": "Inhalation Anesthesia (Short Procedures)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Isoflurane (chamber + mask)", "name_ja": "イソフルラン（チャンバー＋マスク）", "dose": "Induction: 3-4%, Maintenance: 1-2.5%", "route": "Inhalation", "onset": "2-3 min", "duration": "Continuous",
                 "notes_ja": "小型齧歯類に最も安全。麻酔チャンバーで導入後、マスク維持。呼吸停止に注意。", "notes": "Safest for small rodents. Induce in chamber, maintain with mask. Watch for apnea."},
                {"name": "Sevoflurane (chamber + mask)", "name_ja": "セボフルラン（チャンバー＋マスク）", "dose": "Induction: 6-8%, Maintenance: 3-4%", "route": "Inhalation", "onset": "1-2 min", "duration": "Continuous",
                 "notes_ja": "イソフルランより導入・覚醒が速い。", "notes": "Faster induction and recovery than isoflurane."},
            ],
            "notes_ja": "チャンバー導入は酸素流量を十分に確保し、過剰暴露に注意。目が閉じ、正向反射消失で導入完了。",
            "notes": "Ensure adequate oxygen flow during chamber induction. Watch for excessive exposure. Induction complete when eyes close and righting reflex is lost.",
        },
        {
            "name": {"ja": "注射麻酔（中等度処置）", "en": "Injectable Anesthesia (Moderate Procedures)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Ketamine + Xylazine", "name_ja": "ケタミン＋キシラジン", "dose": "100-200 mg/kg + 5-10 mg/kg", "route": "IP", "onset": "5-10 min", "duration": "30-60 min",
                 "notes_ja": "腹腔内（IP）投与。呼吸・心機能抑制に注意。アティパメゾールで部分拮抗可。", "notes": "Intraperitoneal (IP) injection. Monitor cardiorespiratory depression. Partially reversible with atipamezole."},
                {"name": "Ketamine + Medetomidine", "name_ja": "ケタミン＋メデトミジン", "dose": "100 mg/kg + 0.25 mg/kg", "route": "IP", "onset": "5-10 min", "duration": "30-60 min",
                 "notes_ja": "メデトミジンはアティパメゾールで拮抗可能（覚醒促進）。", "notes": "Medetomidine reversible with atipamezole (promotes faster recovery)."},
            ],
            "notes_ja": "IP投与は臓器穿刺を避けるため右下腹部に注射。26-28Gの針を使用。",
            "notes": "IP injection in right lower abdomen to avoid organ puncture. Use 26-28G needle.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "RR", "target": "35-135 /min", "notes_ja": "胸郭の動きを目視。呼吸停止時はドキサプラム（IP 10 mg/kg）または指で軽く胸郭を圧迫。", "notes": "Visual chest movement. For apnea: doxapram (IP 10 mg/kg) or gentle chest compression with fingers."},
                {"param": "HR", "target": "250-600 bpm", "notes_ja": "超音波ドップラーで確認。触診困難。", "notes": "Confirm with ultrasonic Doppler. Palpation difficult."},
                {"param": "Temperature", "target": "36.5-38.5°C", "notes_ja": "低体温は最大のリスク。加温パッド必須。直腸温計は小型のものを使用。", "notes": "Hypothermia is the greatest risk. Warming pad essential. Use small rectal thermometer."},
            ],
            "notes_ja": "覚醒後は暖かい環境（28-30°C）で回復させる。食事と水を早期に提供。覚醒に時間がかかる場合は体温をまず確認。",
            "notes": "Recover in warm environment (28-30°C). Offer food and water early. If slow recovery, check temperature first.",
        },
        {
            "name": {"ja": "緊急対応・回復", "en": "Emergency & Recovery"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "5-10 mg/kg", "route": "IP/SC", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時の第一選択。舌下1-2滴でも有効。", "notes": "First-line for apnea. 1-2 drops sublingual also effective."},
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.003-0.01 mg/kg", "route": "IP/IO", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "心停止時。IO（脛骨近位端）投与も検討。用量は非常に少量（希釈して使用）。", "notes": "For cardiac arrest. IO (proximal tibia) route an option. Very small doses (dilute before use)."},
                {"name": "Atropine", "name_ja": "アトロピン", "dose": "0.05 mg/kg", "route": "IP/SC", "onset": "1-2 min", "duration": "15-30 min",
                 "notes_ja": "徐脈時に使用。", "notes": "For bradycardia."},
            ],
            "notes_ja": "CPR: 指先で胸骨圧迫（100-120回/min）。呼気ガス吹き込み（マスク or 細チューブ）。覚醒後は28-30°Cの暖かい環境で、食事と水を速やかに提供。低血糖予防のため50%デキストロースを舌に塗布。",
            "notes": "CPR: fingertip chest compressions (100-120/min). Ventilate via mask or small tube. After recovery, maintain at 28-30°C, offer food/water promptly. Apply 50% dextrose to tongue for hypoglycemia prevention.",
        },
    ],
}

# ============================================================
# GUINEA PIG
# ============================================================
ANESTHESIA_PROTOCOLS["guinea_pig"] = {
    "species_name": {"ja": "モルモット", "en": "Guinea Pig"},
    "overview": {
        "ja": "モルモットは気管挿管が極めて困難（口腔が小さく、口蓋帆が大きい）。声門上気道デバイス（V-gel）が推奨される。チオペンタールは致死的心停止を起こすため禁忌。ビタミンC欠乏に注意（周術期にビタミンC 50-100 mg/kg SC補充を検討）。",
        "en": "Guinea pig intubation is extremely difficult (small oral cavity, large palatal ostium). Supraglottic airway devices (V-gel) recommended. Thiopental is contraindicated (causes fatal cardiac arrest). Watch for vitamin C deficiency (consider perioperative supplementation 50-100 mg/kg SC).",
    },
    "fasting": {
        "ja": "絶食不要（嘔吐できない）。",
        "en": "No fasting required (cannot vomit).",
    },
    "protocols": [
        {
            "name": {"ja": "鎮静（検査・軽処置）", "en": "Sedation (Examination/Minor Procedures)"},
            "category": "sedation",
            "risk_level": "low",
            "drugs": [
                {"name": "Midazolam + Butorphanol", "name_ja": "ミダゾラム＋ブトルファノール", "dose": "0.5-1.0 mg/kg + 0.4-0.8 mg/kg", "route": "IM/SC", "onset": "10-15 min", "duration": "30-60 min",
                 "notes_ja": "安全性が高い。軽度の鎮静に適する。", "notes": "High safety margin. Suitable for mild sedation."},
            ],
            "notes_ja": "モルモットはストレスに弱い。静かな環境で、同居個体の匂いがついたタオルを使用すると安心。",
            "notes": "Guinea pigs are stress-sensitive. Use towels with cage-mate scent in quiet environment.",
        },
        {
            "name": {"ja": "注射麻酔＋吸入維持", "en": "Injectable Induction + Inhalation Maintenance"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Ketamine + Medetomidine", "name_ja": "ケタミン＋メデトミジン", "dose": "40 mg/kg + 0.3 mg/kg", "route": "IP/IM", "onset": "5-10 min", "duration": "30-60 min",
                 "notes_ja": "アティパメゾールで拮抗可。吸入麻酔への移行を推奨。", "notes": "Reversible with atipamezole. Transition to inhalation recommended."},
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "5-10 mg/kg", "route": "IM/IP", "onset": "5-10 min", "duration": "15-30 min",
                 "notes_ja": "注射量が多いがIM投与可。覚醒時に興奮することがある。", "notes": "Large injection volume but IM route possible. May cause excitement during recovery."},
                {"name": "Isoflurane (mask/chamber)", "name_ja": "イソフルラン（マスク/チャンバー）", "dose": "Induction: 3-4%, Maintenance: 1.5-3%", "route": "Inhalation", "onset": "2-3 min", "duration": "Continuous",
                 "notes_ja": "モルモットは息止め（breath holding）をするため、チャンバー導入に時間がかかることがある。", "notes": "Guinea pigs may breath-hold, making chamber induction take longer."},
            ],
            "notes_ja": "気管挿管が困難なため、V-gel（モルモット用）の使用を推奨。気管挿管を試みる場合は14-16G IV catheterをETチューブ代わりに使用。",
            "notes": "Due to difficult intubation, V-gel (guinea pig size) is recommended. If attempting intubation, use 14-16G IV catheter as ET tube.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "RR", "target": "40-100 /min", "notes_ja": "呼吸停止時はドキサプラム2-5 mg/kg IV/IP。胸壁の動きを常時監視。", "notes": "For apnea: doxapram 2-5 mg/kg IV/IP. Monitor chest wall movement continuously."},
                {"param": "HR", "target": "230-380 bpm", "notes_ja": "ドップラーで確認。食道聴診器も有効。", "notes": "Confirm with Doppler. Esophageal stethoscope also effective."},
                {"param": "Temperature", "target": "37.2-39.5°C", "notes_ja": "低体温になりやすい。加温パッド使用。", "notes": "Prone to hypothermia. Use warming pad."},
            ],
            "notes_ja": "覚醒後すぐに乾草と水を提供。術後鎮痛: メロキシカム0.5-1.0 mg/kg PO/SC q24h。ビタミンC 50 mg/kg SC/PO。同居個体と早期に戻す（社会的動物）。",
            "notes": "Offer hay and water immediately after recovery. Post-op analgesia: meloxicam 0.5-1.0 mg/kg PO/SC q24h. Vitamin C 50 mg/kg SC/PO. Return to cage-mates early (social animals).",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "2-5 mg/kg", "route": "IV/IP", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時の第一選択。", "notes": "First-line for apnea."},
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.003-0.01 mg/kg", "route": "IP/IO", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。チオペンタールは絶対禁忌（致死的心停止）。", "notes": "For CPA. Thiopental is absolutely contraindicated (fatal cardiac arrest)."},
                {"name": "Glycopyrrolate", "name_ja": "グリコピロレート", "dose": "0.01-0.02 mg/kg", "route": "SC/IM", "onset": "2-3 min", "duration": "30-60 min",
                 "notes_ja": "徐脈時。アトロピンより副作用が少ない。", "notes": "For bradycardia. Fewer side effects than atropine."},
            ],
            "notes_ja": "モルモットのCPR: 胸骨を指先で圧迫（100-120/min）。100% O2でバッグバルブマスク換気。気管挿管困難なためマスク換気が現実的。",
            "notes": "Guinea pig CPR: fingertip sternal compressions (100-120/min). Bag-valve-mask ventilation with 100% O2. Mask ventilation is practical as intubation is very difficult.",
        },
    ],
}

# ============================================================
# CHINCHILLA
# ============================================================
ANESTHESIA_PROTOCOLS["chinchilla"] = {
    "species_name": {"ja": "チンチラ", "en": "Chinchilla"},
    "overview": {
        "ja": "チンチラは密な毛皮のため体温管理が重要（高体温に弱い）。気管挿管はモルモット同様困難。ストレスに非常に敏感で、捕獲時に毛が抜ける（ファースリップ）。",
        "en": "Chinchillas have dense fur making temperature management critical (heat-intolerant). Intubation is as difficult as guinea pigs. Extremely stress-sensitive; fur slip can occur during capture.",
    },
    "fasting": {
        "ja": "絶食不要（嘔吐できない）。口腔内の食物確認。",
        "en": "No fasting required (cannot vomit). Check oral cavity for food.",
    },
    "protocols": [
        {
            "name": {"ja": "鎮静（検査・軽処置）", "en": "Sedation (Examination/Minor Procedures)"},
            "category": "sedation",
            "risk_level": "low",
            "drugs": [
                {"name": "Midazolam + Butorphanol", "name_ja": "ミダゾラム＋ブトルファノール", "dose": "0.5-1.0 mg/kg + 0.2-0.5 mg/kg", "route": "IM/SC", "onset": "10-15 min", "duration": "30-60 min",
                 "notes_ja": "安全で拮抗可能。", "notes": "Safe and reversible."},
            ],
            "notes_ja": "チンチラは高温（>25°C）に弱い。麻酔中の環境温度管理に注意（冷却と加温のバランス）。",
            "notes": "Chinchillas are heat-intolerant (>25°C). Balance cooling and warming during anesthesia.",
        },
        {
            "name": {"ja": "全身麻酔", "en": "General Anesthesia"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Ketamine + Medetomidine", "name_ja": "ケタミン＋メデトミジン", "dose": "40 mg/kg + 0.3 mg/kg", "route": "IM/IP", "onset": "5-10 min", "duration": "30-60 min",
                 "notes_ja": "アティパメゾールで部分拮抗可。吸入麻酔移行推奨。", "notes": "Partially reversible with atipamezole. Transition to inhalation recommended."},
                {"name": "Isoflurane (chamber + mask)", "name_ja": "イソフルラン（チャンバー＋マスク）", "dose": "Induction: 3-4%, Maintenance: 1-2.5%", "route": "Inhalation", "onset": "2-3 min", "duration": "Continuous",
                 "notes_ja": "短時間処置に適する。マスク維持。", "notes": "Suitable for short procedures. Maintain with mask."},
            ],
            "notes_ja": "術後鎮痛: メロキシカム0.3-0.5 mg/kg PO/SC q24h。フィプロニルは致死的であり絶対に使用しない。",
            "notes": "Post-op analgesia: meloxicam 0.3-0.5 mg/kg PO/SC q24h. Fipronil is LETHAL to chinchillas — never use.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "200-350 bpm", "notes_ja": "ドップラーで確認。", "notes": "Confirm with Doppler."},
                {"param": "RR", "target": "40-80 /min", "notes_ja": "呼吸停止に注意。", "notes": "Watch for apnea."},
                {"param": "Temperature", "target": "36.1-37.8°C", "notes_ja": "正常体温が低め。高体温（>38.5°C）は致死的。低体温にも注意。", "notes": "Normal temperature is relatively low. Hyperthermia (>38.5°C) is fatal. Also watch for hypothermia."},
            ],
            "notes_ja": "覚醒は静かで涼しい（20-22°C）環境で。乾草と水を早期に提供。砂浴びは創傷治癒まで中止。",
            "notes": "Recover in quiet, cool (20-22°C) environment. Offer hay and water early. Suspend dust baths until wound healing.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "2-5 mg/kg", "route": "IP/IV", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時の第一選択。", "notes": "First-line for apnea."},
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.003-0.01 mg/kg", "route": "IP/IO", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。用量は希釈して正確に計測。", "notes": "For CPA. Dilute for accurate dosing."},
            ],
            "notes_ja": "チンチラは高温（>28°C）に極めて弱い。緊急時も環境温度に注意。覚醒環境は20-22°C。フィプロニルは致死的であり絶対に使用しない。",
            "notes": "Chinchillas are extremely heat-sensitive (>28°C). Monitor environmental temperature even during emergencies. Recovery environment at 20-22°C. Fipronil is LETHAL — never use.",
        },
    ],
}

# ============================================================
# FERRET
# ============================================================
ANESTHESIA_PROTOCOLS["ferret"] = {
    "species_name": {"ja": "フェレット", "en": "Ferret"},
    "overview": {
        "ja": "フェレットは犬猫に近い麻酔管理が可能。気管挿管は比較的容易（2.5-3.5 ETチューブ）。インスリノーマ（低血糖）の併存が多く、術前血糖チェック必須。副腎疾患も多い。3-4時間の絶食で低血糖リスクあり。",
        "en": "Ferrets can be managed similarly to small dogs/cats. Intubation is relatively easy (2.5-3.5 ET tube). High incidence of insulinoma (hypoglycemia) — pre-anesthetic glucose check essential. Adrenal disease also common. 3-4 hr fasting may cause hypoglycemia.",
    },
    "fasting": {
        "ja": "3-4時間絶食のみ（消化管通過が速い）。インスリノーマの場合は絶食時間を最短に。術中血糖モニタリング。",
        "en": "3-4 hr food fast only (rapid GI transit). Minimize fasting time with insulinoma. Monitor intraoperative glucose.",
    },
    "protocols": [
        {
            "name": {"ja": "鎮静（検査・処置）", "en": "Sedation (Examination/Procedures)"},
            "category": "sedation",
            "risk_level": "low",
            "drugs": [
                {"name": "Dexmedetomidine + Butorphanol", "name_ja": "デクスメデトミジン＋ブトルファノール", "dose": "10-20 μg/kg + 0.2 mg/kg", "route": "IM", "onset": "10-15 min", "duration": "30-45 min",
                 "notes_ja": "確実な鎮静。拮抗可能。低血糖に注意。", "notes": "Reliable sedation. Reversible. Watch for hypoglycemia."},
                {"name": "Midazolam + Butorphanol", "name_ja": "ミダゾラム＋ブトルファノール", "dose": "0.25-0.5 mg/kg + 0.2 mg/kg", "route": "IM", "onset": "10-15 min", "duration": "30-60 min",
                 "notes_ja": "心疾患のあるフェレットにより安全。", "notes": "Safer for ferrets with cardiac disease."},
            ],
            "notes_ja": "フェレットは比較的麻酔に耐性がある。マスク導入も可能（イソフルラン3-5%）だが、興奮・息止めに注意。",
            "notes": "Ferrets are relatively tolerant of anesthesia. Mask induction possible (isoflurane 3-5%) but watch for excitement/breath-holding.",
        },
        {
            "name": {"ja": "全身麻酔", "en": "General Anesthesia"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Propofol", "name_ja": "プロポフォール", "dose": "2-5 mg/kg", "route": "IV (cephalic vein)", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "頭側静脈からのIV投与。スムーズな導入。", "notes": "IV via cephalic vein. Smooth induction."},
                {"name": "Isoflurane (mask/chamber)", "name_ja": "イソフルラン（マスク/チャンバー）", "dose": "Induction: 3-5%, Maintenance: 1.5-3%", "route": "Inhalation", "onset": "2-5 min", "duration": "Continuous",
                 "notes_ja": "マスク導入は一般的。導入後気管挿管。", "notes": "Mask induction is common. Intubate after induction."},
                {"name": "Ketamine + Midazolam", "name_ja": "ケタミン＋ミダゾラム", "dose": "5-8 mg/kg + 0.3 mg/kg", "route": "IM", "onset": "5-10 min", "duration": "20-30 min",
                 "notes_ja": "IM導入が可能。吸入麻酔に移行。", "notes": "IM induction possible. Transition to inhalation."},
            ],
            "notes_ja": "気管挿管: 2.5-3.5 ETチューブ。喉頭鏡（Miller 0-1ブレード）使用。フェレットの気管は長い。",
            "notes": "Intubation: 2.5-3.5 ET tube. Use laryngoscope (Miller 0-1 blade). Ferret tracheas are long.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "200-400 bpm", "notes_ja": "ドップラーまたは食道聴診器で確認。", "notes": "Confirm with Doppler or esophageal stethoscope."},
                {"param": "RR", "target": "33-36 /min", "notes_ja": "呼吸抑制に注意。", "notes": "Watch for respiratory depression."},
                {"param": "Blood Glucose", "target": ">60 mg/dL", "notes_ja": "インスリノーマがあれば30分毎にチェック。低血糖時: デキストロース0.5-1 mL/kg IV（50%溶液を希釈）。", "notes": "Check q30min if insulinoma present. Hypoglycemia: dextrose 0.5-1 mL/kg IV (dilute 50% solution)."},
                {"param": "Temperature", "target": "37.8-40.0°C", "notes_ja": "低体温に注意。加温パッド使用。", "notes": "Watch for hypothermia. Use warming pad."},
            ],
            "notes_ja": "覚醒後すぐに少量の高カロリー食を提供（低血糖予防）。術後鎮痛: メロキシカム0.2 mg/kg PO/SC q24h。",
            "notes": "Offer small amounts of high-calorie food immediately after recovery (prevent hypoglycemia). Post-op analgesia: meloxicam 0.2 mg/kg PO/SC q24h.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Atropine", "name_ja": "アトロピン", "dose": "0.02-0.04 mg/kg", "route": "IV/IM", "onset": "1-2 min", "duration": "15-30 min",
                 "notes_ja": "徐脈に対する第一選択。", "notes": "First-line for bradycardia."},
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.01 mg/kg", "route": "IV/IO/IT", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。フェレットは犬猫に近い管理が可能。", "notes": "For CPA. Ferrets can be managed similarly to small dogs/cats."},
                {"name": "50% Dextrose", "name_ja": "50%デキストロース", "dose": "0.5-1 mL/kg (diluted 1:4)", "route": "IV slow", "onset": "1-2 min", "duration": "",
                 "notes_ja": "インスリノーマによる低血糖発作時の第一選択。必ず希釈して投与。", "notes": "First-line for insulinoma-related hypoglycemic seizures. Always dilute before administration."},
            ],
            "notes_ja": "フェレットのCPR: 犬猫に準じる。胸骨圧迫100-120/min。低血糖が疑われる場合はまずデキストロース投与。インスリノーマ手術時は血糖値を30分毎にモニタリング。",
            "notes": "Ferret CPR: follow small dog/cat protocols. Chest compressions 100-120/min. If hypoglycemia suspected, administer dextrose first. Monitor glucose q30min during insulinoma surgery.",
        },
    ],
}

# ============================================================
# HEDGEHOG
# ============================================================
ANESTHESIA_PROTOCOLS["hedgehog"] = {
    "species_name": {"ja": "ハリネズミ", "en": "Hedgehog"},
    "overview": {
        "ja": "ハリネズミは防御姿勢（丸まる）のため、検査にも鎮静が必要なことが多い。体重300-600g。イソフルラン吸入で導入が最も一般的。丸まった状態でもマスクを近づければ吸入可能。肥満個体が多い。",
        "en": "Hedgehogs often require sedation even for examination due to defensive curling. Weight 300-600g. Isoflurane inhalation induction is most common. Mask can be applied even when curled. Obesity is common.",
    },
    "fasting": {
        "ja": "絶食不要（低血糖リスク）。",
        "en": "No fasting required (hypoglycemia risk).",
    },
    "protocols": [
        {
            "name": {"ja": "吸入鎮静・麻酔（最も一般的）", "en": "Inhalation Sedation/Anesthesia (Most Common)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Isoflurane (chamber + mask)", "name_ja": "イソフルラン（チャンバー＋マスク）", "dose": "Induction: 3-5%, Maintenance: 1-3%", "route": "Inhalation", "onset": "3-5 min", "duration": "Continuous",
                 "notes_ja": "丸まった状態でチャンバーに入れ、広がるまで待つ。広がったらマスクに移行。呼吸停止に注意。", "notes": "Place curled hedgehog in chamber, wait until uncurling. Switch to mask once relaxed. Watch for apnea."},
                {"name": "Sevoflurane (chamber + mask)", "name_ja": "セボフルラン（チャンバー＋マスク）", "dose": "Induction: 6-8%, Maintenance: 3-4%", "route": "Inhalation", "onset": "2-3 min", "duration": "Continuous",
                 "notes_ja": "導入・覚醒が速い。", "notes": "Faster induction and recovery."},
            ],
            "notes_ja": "ハリネズミの検査ではイソフルラン短時間吸入（2-3分）で十分な場合が多い。針（棘）を通して注射が困難なため、吸入麻酔が推奨される。",
            "notes": "Short isoflurane exposure (2-3 min) often sufficient for examination. Injection through quills is difficult, making inhalation preferred.",
        },
        {
            "name": {"ja": "注射麻酔（手術用）", "en": "Injectable Anesthesia (For Surgery)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Ketamine + Medetomidine", "name_ja": "ケタミン＋メデトミジン", "dose": "5-10 mg/kg + 0.05-0.1 mg/kg", "route": "IM/SC (ventral abdomen)", "onset": "10-15 min", "duration": "30-60 min",
                 "notes_ja": "腹部腹側の棘のない部分に注射。アティパメゾールで部分拮抗。", "notes": "Inject in quill-free ventral abdominal skin. Partially reversible with atipamezole."},
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "3-5 mg/kg", "route": "IM/SC", "onset": "5-10 min", "duration": "15-30 min",
                 "notes_ja": "吸入麻酔への移行に適する。", "notes": "Suitable for transition to inhalation anesthesia."},
            ],
            "notes_ja": "IV確保は困難（頭側静脈 or 外側伏在静脈を使用、26-28G）。IO（脛骨、大腿骨）が緊急時の代替。",
            "notes": "IV access is difficult (cephalic or lateral saphenous vein, 26-28G). IO (tibial, femoral) as emergency alternative.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "180-280 bpm", "notes_ja": "ドップラーで確認。棘が邪魔する場合は腹側から。", "notes": "Confirm with Doppler. If quills interfere, monitor from ventral surface."},
                {"param": "RR", "target": "25-50 /min", "notes_ja": "呼吸停止時はドキサプラムまたは穏やかな胸部圧迫。", "notes": "For apnea: doxapram or gentle thoracic compression."},
                {"param": "Temperature", "target": "35.1-37.2°C", "notes_ja": "正常体温が低め。36°C以下は加温必須。冬眠様状態（トルポール）に注意。", "notes": "Normal temperature is relatively low. Below 36°C requires active warming. Watch for torpor-like state."},
            ],
            "notes_ja": "覚醒後は暖かい環境（25-27°C）で回復。ミルワーム等の好物で食欲を確認。術後鎮痛: メロキシカム0.2-0.5 mg/kg PO/SC q24h。",
            "notes": "Recover in warm (25-27°C) environment. Check appetite with mealworms or favorite food. Post-op analgesia: meloxicam 0.2-0.5 mg/kg PO/SC q24h.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "2-5 mg/kg", "route": "SC/IP", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時の第一選択。棘のない腹側から注射。", "notes": "First-line for apnea. Inject into quill-free ventral skin."},
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.003-0.01 mg/kg", "route": "IP/IO", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。IO: 脛骨近位端。", "notes": "For CPA. IO: proximal tibia."},
            ],
            "notes_ja": "ハリネズミのCPR: 棘があるため胸骨圧迫は腹側から。指先で100-120/min。トルポール（低体温休眠）と死亡の鑑別に注意（加温で覚醒するかを確認）。覚醒後25-27°Cの環境で。",
            "notes": "Hedgehog CPR: quills make dorsal access difficult; compress from ventral side. Fingertip compressions 100-120/min. Differentiate torpor from death (warm and check for arousal). Recover at 25-27°C.",
        },
    ],
}

# ============================================================
# SUGAR GLIDER
# ============================================================
ANESTHESIA_PROTOCOLS["sugar_glider"] = {
    "species_name": {"ja": "フクロモモンガ", "en": "Sugar Glider"},
    "overview": {
        "ja": "フクロモモンガは非常に小型（80-160g）で麻酔リスクが高い。低体温・低血糖が主な合併症。有袋類のため薬物代謝が胎盤哺乳類と異なる可能性がある。イソフルラン吸入が最も安全。ストレスに非常に弱く、自咬症のリスクあり。",
        "en": "Sugar gliders are very small (80-160g) with high anesthetic risk. Major complications: hypothermia, hypoglycemia. As marsupials, drug metabolism may differ from placental mammals. Isoflurane inhalation is safest. Extremely stress-sensitive with self-mutilation risk.",
    },
    "fasting": {
        "ja": "2-4時間絶食のみ（低血糖リスク）。",
        "en": "2-4 hr food fast only (hypoglycemia risk).",
    },
    "protocols": [
        {
            "name": {"ja": "吸入麻酔（推奨）", "en": "Inhalation Anesthesia (Recommended)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Isoflurane (chamber + mask)", "name_ja": "イソフルラン（チャンバー＋マスク）", "dose": "Induction: 3-5%, Maintenance: 1-3%", "route": "Inhalation", "onset": "2-3 min", "duration": "Continuous",
                 "notes_ja": "最も推奨される方法。小型チャンバーで導入後、マスク維持。", "notes": "Most recommended method. Induce in small chamber, maintain with mask."},
            ],
            "notes_ja": "フクロモモンガは皮膚が薄く、IVアクセスは外側尾静脈（lateral tail vein）。IOアクセス（脛骨）が代替。",
            "notes": "Sugar gliders have thin skin. IV access via lateral tail vein. IO access (tibial) as alternative.",
        },
        {
            "name": {"ja": "注射麻酔（IV確保困難時）", "en": "Injectable Anesthesia (When IV Access Unavailable)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Ketamine + Medetomidine", "name_ja": "ケタミン＋メデトミジン", "dose": "10-20 mg/kg + 0.05-0.1 mg/kg", "route": "IM/SC", "onset": "5-10 min", "duration": "30-60 min",
                 "notes_ja": "アティパメゾールで拮抗。筋肉量が少ないためSCが安全。", "notes": "Reversible with atipamezole. SC safer due to limited muscle mass."},
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "5-10 mg/kg", "route": "IM/SC", "onset": "5-10 min", "duration": "15-30 min",
                 "notes_ja": "IM投与可。吸入への移行を推奨。", "notes": "IM route possible. Transition to inhalation recommended."},
            ],
            "notes_ja": "術後の自咬症予防のためエリザベスカラー（小型）を装着。ストレス軽減のためポーチ（袋）を回復環境に提供。",
            "notes": "Apply small Elizabethan collar to prevent self-mutilation. Provide pouch in recovery environment for stress reduction.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "200-300 bpm", "notes_ja": "ドップラーで確認。非常に小型のため触診困難。", "notes": "Confirm with Doppler. Palpation difficult due to very small size."},
                {"param": "RR", "target": "16-40 /min", "notes_ja": "呼吸停止に注意。", "notes": "Watch for apnea."},
                {"param": "Temperature", "target": "36.3-36.9°C", "notes_ja": "正常体温が低い。トルポール（低体温休眠）との鑑別に注意。加温パッド必須。", "notes": "Normal temperature is low. Differentiate from torpor. Warming pad essential."},
            ],
            "notes_ja": "覚醒後は暗く暖かいポーチに入れ、蜂蜜水を提供（低血糖予防）。術後鎮痛: メロキシカム0.2-0.5 mg/kg PO/SC q24h。",
            "notes": "Place in dark, warm pouch after recovery. Offer honey water (prevent hypoglycemia). Post-op analgesia: meloxicam 0.2-0.5 mg/kg PO/SC q24h.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "5-10 mg/kg", "route": "SC/IP", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時の第一選択。", "notes": "First-line for apnea."},
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.003-0.01 mg/kg", "route": "IP/IO", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。有袋類特有の薬物代謝差を考慮。", "notes": "For CPA. Consider marsupial-specific differences in drug metabolism."},
            ],
            "notes_ja": "フクロモモンガのCPR: 非常に小型のため指先で穏やかに胸骨圧迫。トルポール（低体温休眠）と死亡の鑑別が重要（加温＋刺激で反応確認）。覚醒後は自咬症予防のためエリザベスカラー装着。暗いポーチで回復。",
            "notes": "Sugar glider CPR: very small; gentle fingertip sternal compressions. Differentiate torpor from death (warm + stimulate to check response). Apply Elizabethan collar after recovery to prevent self-mutilation. Recover in dark pouch.",
        },
    ],
}

# ============================================================
# DEGU
# ============================================================
ANESTHESIA_PROTOCOLS["degu"] = {
    "species_name": {"ja": "デグー", "en": "Degu"},
    "overview": {
        "ja": "デグーは小型齧歯類（170-300g）でハムスター・モルモットと類似した麻酔管理。糖尿病が非常に多いため、術前血糖チェック必須。尾は脱グローブ（皮膚剥離）しやすいため絶対に尾で保定しない。",
        "en": "Degus are small rodents (170-300g) with anesthetic management similar to hamsters/guinea pigs. Very high incidence of diabetes — pre-anesthetic glucose check essential. Tail degloving risk is very high — never restrain by tail.",
    },
    "fasting": {
        "ja": "絶食不要（低血糖リスク、特に糖尿病個体）。",
        "en": "No fasting required (hypoglycemia risk, especially diabetic individuals).",
    },
    "protocols": [
        {
            "name": {"ja": "吸入麻酔（推奨）", "en": "Inhalation Anesthesia (Recommended)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Isoflurane (chamber + mask)", "name_ja": "イソフルラン（チャンバー＋マスク）", "dose": "Induction: 3-4%, Maintenance: 1.5-2.5%", "route": "Inhalation", "onset": "2-3 min", "duration": "Continuous",
                 "notes_ja": "小型齧歯類の標準。チャンバー導入後マスク維持。", "notes": "Standard for small rodents. Chamber induction, mask maintenance."},
            ],
            "notes_ja": "デグーは社会的動物。複数飼育の場合、同居個体の匂いがついた環境で覚醒させるとストレス軽減。",
            "notes": "Degus are social animals. When group-housed, recover with cage-mate scent for stress reduction.",
        },
        {
            "name": {"ja": "注射麻酔", "en": "Injectable Anesthesia"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Ketamine + Xylazine", "name_ja": "ケタミン＋キシラジン", "dose": "60-80 mg/kg + 5-8 mg/kg", "route": "IP", "onset": "5-10 min", "duration": "30-45 min",
                 "notes_ja": "IP投与。糖尿病個体では血糖変動に特に注意。", "notes": "IP injection. Monitor blood glucose closely in diabetic individuals."},
                {"name": "Ketamine + Medetomidine", "name_ja": "ケタミン＋メデトミジン", "dose": "50-75 mg/kg + 0.25 mg/kg", "route": "IP", "onset": "5-10 min", "duration": "30-60 min",
                 "notes_ja": "アティパメゾールで部分拮抗可。", "notes": "Partially reversible with atipamezole."},
            ],
            "notes_ja": "血糖モニタリング: 術中30分毎。低血糖（<60 mg/dL）時は5%デキストロース点滴。糖分の多い食事は禁忌（糖尿病悪化）。",
            "notes": "Blood glucose monitoring q30min intraoperatively. Hypoglycemia (<60 mg/dL): 5% dextrose infusion. High-sugar diet is contraindicated (worsens diabetes).",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "200-350 bpm", "notes_ja": "ドップラーで確認。", "notes": "Confirm with Doppler."},
                {"param": "RR", "target": "50-100 /min", "notes_ja": "呼吸停止に注意。", "notes": "Watch for apnea."},
                {"param": "Blood Glucose", "target": "60-120 mg/dL", "notes_ja": "糖尿病個体では高血糖にも注意。インスリン投与は周術期には行わない。", "notes": "Watch for hyperglycemia in diabetic individuals. Do not administer insulin perioperatively."},
                {"param": "Temperature", "target": "37.0-38.0°C", "notes_ja": "低体温に注意。加温パッド使用。", "notes": "Watch for hypothermia. Use warming pad."},
            ],
            "notes_ja": "覚醒後は乾草と水を提供。糖分の高い果物は厳禁。術後鎮痛: メロキシカム0.3-0.5 mg/kg PO/SC q24h。",
            "notes": "Offer hay and water after recovery. High-sugar fruits are strictly prohibited. Post-op analgesia: meloxicam 0.3-0.5 mg/kg PO/SC q24h.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "5-10 mg/kg", "route": "IP", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時の第一選択。", "notes": "First-line for apnea."},
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.003-0.01 mg/kg", "route": "IP/IO", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。", "notes": "For CPA."},
                {"name": "5% Dextrose", "name_ja": "5%デキストロース", "dose": "1-2 mL bolus", "route": "IP/IV", "onset": "1-2 min", "duration": "",
                 "notes_ja": "低血糖時。糖尿病個体でも急性低血糖はまず補正。", "notes": "For hypoglycemia. Even in diabetic individuals, correct acute hypoglycemia first."},
            ],
            "notes_ja": "デグーのCPR: 指先で胸骨圧迫（100-120/min）。尾の脱グローブに注意（尾を掴まない）。覚醒後は糖分を含まない食事を提供（糖尿病悪化予防）。血糖値を確認。",
            "notes": "Degu CPR: fingertip sternal compressions (100-120/min). Avoid tail (degloving risk — never grab tail). Offer sugar-free food after recovery (prevent diabetes worsening). Check blood glucose.",
        },
    ],
}

# ============================================================
# BIRD (General)
# ============================================================
ANESTHESIA_PROTOCOLS["bird"] = {
    "species_name": {"ja": "鳥", "en": "Bird"},
    "overview": {
        "ja": "鳥類は独特な呼吸器系（気嚢システム）を持ち、麻酔管理が哺乳類と大きく異なる。横隔膜がないため陽圧換気の概念が異なる。吸入麻酔（イソフルラン）がゴールドスタンダード。体重に比べ代謝率が高く、薬物の効果が速い。保定ストレスで急死するリスクがある。",
        "en": "Birds have a unique respiratory system (air sac system) making anesthetic management very different from mammals. No diaphragm, so positive pressure ventilation concepts differ. Isoflurane inhalation is the gold standard. High metabolic rate relative to body weight leads to rapid drug effects. Restraint stress can cause sudden death.",
    },
    "fasting": {
        "ja": "小型鳥（<100g）: 1-2時間。中型鳥（100-500g）: 2-4時間。大型鳥（>500g）: 6-12時間。そのう（crop）の食物を確認し、嘔吐・誤嚥リスクを評価。",
        "en": "Small birds (<100g): 1-2 hr. Medium (100-500g): 2-4 hr. Large (>500g): 6-12 hr. Check crop contents; assess regurgitation/aspiration risk.",
    },
    "protocols": [
        {
            "name": {"ja": "吸入麻酔（ゴールドスタンダード）", "en": "Inhalation Anesthesia (Gold Standard)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Isoflurane", "name_ja": "イソフルラン", "dose": "Induction: 3-5%, Maintenance: 1-3%", "route": "Mask / ET tube / Air sac tube", "onset": "30-90 sec", "duration": "Continuous",
                 "notes_ja": "鳥類での第一選択。マスク導入が最も一般的。導入が非常に速い（30-90秒）。呼吸停止のリスクが高いため、常にIPPV準備。", "notes": "First choice in birds. Mask induction most common. Very rapid induction (30-90 sec). High apnea risk; always have IPPV ready."},
                {"name": "Sevoflurane", "name_ja": "セボフルラン", "dose": "Induction: 6-8%, Maintenance: 3-5%", "route": "Mask / ET tube", "onset": "30-60 sec", "duration": "Continuous",
                 "notes_ja": "導入・覚醒がイソフルランよりさらに速い。コストが高い。", "notes": "Even faster induction/recovery than isoflurane. Higher cost."},
            ],
            "notes_ja": "鳥の気管挿管: 非カフ付きETチューブ（鳥の気管は完全軟骨輪で壊死リスク）。サイズは体重で選択。鳥の声門は開放状態で可視。",
            "notes": "Avian intubation: UNCUFFED ET tubes (bird trachea has complete rings, cuff causes necrosis). Size by body weight. Glottis is open and visible in birds.",
        },
        {
            "name": {"ja": "注射麻酔（補助的使用）", "en": "Injectable Anesthesia (Adjunctive Use)"},
            "category": "premedication",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Midazolam", "name_ja": "ミダゾラム", "dose": "0.5-2.0 mg/kg", "route": "IM/IN", "onset": "5-10 min", "duration": "30-60 min",
                 "notes_ja": "鎮静・筋弛緩に使用。フルマゼニルで拮抗可能。鼻腔内（IN）投与がストレス軽減に有効。", "notes": "Used for sedation/muscle relaxation. Reversible with flumazenil. Intranasal (IN) route reduces stress."},
                {"name": "Butorphanol", "name_ja": "ブトルファノール", "dose": "1-4 mg/kg", "route": "IM", "onset": "10-15 min", "duration": "2-4 hr",
                 "notes_ja": "鳥での鎮痛の第一選択オピオイド。用量が哺乳類より高い。", "notes": "First-choice opioid analgesic in birds. Doses are higher than in mammals."},
                {"name": "Ketamine + Midazolam", "name_ja": "ケタミン＋ミダゾラム", "dose": "10-30 mg/kg + 0.5-1.0 mg/kg", "route": "IM", "onset": "3-5 min", "duration": "15-30 min",
                 "notes_ja": "野生鳥の捕獲後導入や、マスク導入が困難な場合に使用。覚醒が粗いことがある。", "notes": "Used for wild bird capture or when mask induction is difficult. Recovery may be rough."},
            ],
            "notes_ja": "鳥類ではα2作動薬（キシラジン、デクスメデトミジン）は心血管抑制が強く、一般的には推奨されない。",
            "notes": "Alpha-2 agonists (xylazine, dexmedetomidine) are generally NOT recommended in birds due to severe cardiovascular depression.",
        },
        {
            "name": {"ja": "モニタリング", "en": "Monitoring Guidelines"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "RR", "target": "Species-dependent (15-80/min)", "notes_ja": "小型鳥は速い。呼吸パターンの変化に注意。無呼吸は即座にIPPV。", "notes": "Small birds are faster. Watch for pattern changes. Apnea requires immediate IPPV."},
                {"param": "HR", "target": "Species-dependent (150-600 bpm)", "notes_ja": "食道聴診器またはドップラー。ECGも可能。", "notes": "Esophageal stethoscope or Doppler. ECG also possible."},
                {"param": "ETCO2", "target": "30-45 mmHg", "notes_ja": "気嚢システムのため哺乳類と異なる値を示すことがある。", "notes": "Air sac system may produce values different from mammals."},
                {"param": "SpO2", "target": ">90%", "notes_ja": "プローブは趾に装着。鳥類の正常値は哺乳類より低いことがある。", "notes": "Place probe on digit. Normal values may be lower than mammals."},
                {"param": "Temperature", "target": "40.0-42.0°C", "notes_ja": "鳥の正常体温は哺乳類より高い。38°C以下は低体温。", "notes": "Normal avian temperature is higher than mammals. Below 38°C indicates hypothermia."},
                {"param": "Reflex", "target": "Pedal withdrawal, palpebral", "notes_ja": "趾引っ込め反射、眼瞼反射で麻酔深度を評価。翼の緊張度も参考。", "notes": "Evaluate depth with pedal withdrawal and palpebral reflexes. Wing tone also informative."},
            ],
            "notes_ja": "鳥の麻酔深度評価: 浅い→翼トーン維持、趾反射(+)。適切→翼弛緩、趾反射(-)、眼瞼反射(+)。深すぎ→眼瞼反射(-)、瞳孔散大。",
            "notes": "Avian depth assessment: Light→wing tone present, pedal reflex(+). Adequate→wing relaxed, pedal(-), palpebral(+). Too deep→palpebral(-), dilated pupils.",
        },
        {
            "name": {"ja": "覚醒・回復", "en": "Recovery"},
            "category": "recovery",
            "risk_level": "moderate",
            "drugs": [],
            "notes_ja": "覚醒は非常に速い（1-3分）。暗い暖かい環境（インキュベーター28-32°C）で回復。覚醒時のばたつきによる外傷を防ぐため、パッドで覆う。食事は覚醒後1-2時間以降に提供。強制給餌が必要な場合はそのうチューブで。",
            "notes": "Recovery is very rapid (1-3 min). Recover in dark, warm environment (incubator 28-32°C). Pad surroundings to prevent flapping injuries. Offer food 1-2 hr post-recovery. Crop tube feeding if needed.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Atropine", "name_ja": "アトロピン", "dose": "0.02-0.05 mg/kg", "route": "IV/IM/IO", "onset": "1-2 min", "duration": "15-30 min",
                 "notes_ja": "徐脈に使用。IO（脛足根骨、上腕骨）経路も有効。", "notes": "For bradycardia. IO route (tibiotarsus, humerus) also effective."},
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.01-0.1 mg/kg", "route": "IV/IO/IT", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。IOまたは気管内投与。鳥のCPRは胸骨圧迫（竜骨を挟む）。", "notes": "For CPA. IO or intratracheal. Avian CPR: compress keel (sternal compressions)."},
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "5-10 mg/kg", "route": "IV/IO", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時の第一選択。", "notes": "First-line for respiratory arrest."},
            ],
            "notes_ja": "鳥のCPR: 竜骨（keel）を親指と人差し指で挟んで圧迫。1-2秒/回。100% O2でIPPV。エピネフリンは気管内投与も可能。",
            "notes": "Avian CPR: compress keel between thumb and forefinger. 1-2 compressions/sec. IPPV with 100% O2. Epinephrine can be given intratracheally.",
        },
    ],
}

# ============================================================
# PARAKEET
# ============================================================
ANESTHESIA_PROTOCOLS["parakeet"] = {
    "species_name": {"ja": "インコ", "en": "Parakeet"},
    "overview": {
        "ja": "インコ（セキセイインコ、オカメインコ等）は小型鳥類の中でも特に小さく（30-100g）、麻酔リスクが高い。代謝率が極めて高く、低体温・低血糖が急速に進行する。イソフルラン吸入が唯一の現実的な方法。保定だけで死亡するリスクがある。",
        "en": "Parakeets (budgerigars, cockatiels) are among the smallest birds (30-100g) with very high anesthetic risk. Extremely high metabolic rate; hypothermia and hypoglycemia progress rapidly. Isoflurane inhalation is the only practical method. Restraint alone can be fatal.",
    },
    "fasting": {
        "ja": "1-2時間のみ（低血糖リスク極めて高い）。そのうを確認。",
        "en": "1-2 hr only (extremely high hypoglycemia risk). Check crop.",
    },
    "protocols": [
        {
            "name": {"ja": "吸入麻酔", "en": "Inhalation Anesthesia"},
            "category": "induction",
            "risk_level": "high",
            "drugs": [
                {"name": "Isoflurane (mask)", "name_ja": "イソフルラン（マスク）", "dose": "Induction: 3-5%, Maintenance: 1-3%", "route": "Mask", "onset": "30-60 sec", "duration": "Continuous",
                 "notes_ja": "マスクで導入。チャンバーは過剰暴露リスクがあるため注意。非常に迅速な導入（30秒程度）。呼吸停止を起こしやすい。", "notes": "Mask induction. Chamber carries overdose risk. Very rapid induction (~30 sec). Prone to respiratory arrest."},
            ],
            "notes_ja": "セキセイインコ（30-40g）は気管挿管がほぼ不可能。マスク維持が標準。オカメインコ（80-100g）は1.5-2.0mm非カフETチューブが可能な場合あり。",
            "notes": "Budgerigars (30-40g): intubation nearly impossible. Mask maintenance is standard. Cockatiels (80-100g): 1.5-2.0mm uncuffed ET tube may be possible.",
        },
        {
            "name": {"ja": "鎮痛", "en": "Analgesia"},
            "category": "premedication",
            "risk_level": "low",
            "drugs": [
                {"name": "Butorphanol", "name_ja": "ブトルファノール", "dose": "1-2 mg/kg", "route": "IM", "onset": "5-10 min", "duration": "2-4 hr",
                 "notes_ja": "術前または術後に投与。胸筋への注射。", "notes": "Pre- or post-operative. Inject into pectoral muscle."},
                {"name": "Meloxicam", "name_ja": "メロキシカム", "dose": "0.5-1.0 mg/kg", "route": "PO/IM", "onset": "30 min", "duration": "12-24 hr",
                 "notes_ja": "術後鎮痛。腎機能に注意。", "notes": "Post-operative analgesia. Monitor renal function."},
            ],
            "notes_ja": "小型インコへの注射は26-30Gのツベルクリン用シリンジで。投与量は0.01-0.1 mL単位の精密さが必要。",
            "notes": "Use 26-30G tuberculin syringe for small parakeets. Dosing requires precision to 0.01-0.1 mL.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "350-600 bpm", "notes_ja": "食道聴診器が最も信頼性が高い。", "notes": "Esophageal stethoscope is most reliable."},
                {"param": "RR", "target": "40-80 /min", "notes_ja": "胸壁・尾羽の動きを観察。", "notes": "Observe chest wall and tail feather movement."},
                {"param": "Temperature", "target": "40.0-42.0°C", "notes_ja": "低体温は急速に進行。インキュベーター必須。38°C以下は危険。", "notes": "Hypothermia progresses rapidly. Incubator essential. Below 38°C is dangerous."},
            ],
            "notes_ja": "覚醒は30秒-2分。インキュベーター（30-32°C）で回復。覚醒時のばたつきによる骨折に注意（タオルで軽く包む）。食事は覚醒後早期に。",
            "notes": "Recovery in 30 sec-2 min. Use incubator (30-32°C). Watch for fractures from flapping during recovery (wrap loosely in towel). Offer food early after recovery.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.01-0.1 mg/kg", "route": "IV/IO/IT", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。IO: 脛足根骨（尺骨は含気骨のため避ける）。気管内投与も有効。", "notes": "For CPA. IO: tibiotarsus (avoid ulna — pneumatic bone). Intratracheal also effective."},
                {"name": "Atropine", "name_ja": "アトロピン", "dose": "0.02-0.05 mg/kg", "route": "IV/IO/IM", "onset": "1-2 min", "duration": "15-30 min",
                 "notes_ja": "徐脈時。", "notes": "For bradycardia."},
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "5-10 mg/kg", "route": "IV/IO", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時の第一選択。", "notes": "First-line for apnea."},
            ],
            "notes_ja": "小型インコ（30-40g）のCPR: 竜骨を親指と人差し指で挟んで圧迫（1-2回/sec）。100% O2でIPPV。低体温が疑われる場合はまず加温。IOアクセスは脛足根骨から（25-28G針）。",
            "notes": "Small parakeet (30-40g) CPR: compress keel between thumb and forefinger (1-2/sec). IPPV with 100% O2. If hypothermia suspected, warm first. IO access via tibiotarsus (25-28G needle).",
        },
    ],
}

# ============================================================
# PARROT
# ============================================================
ANESTHESIA_PROTOCOLS["parrot"] = {
    "species_name": {"ja": "オウム", "en": "Parrot"},
    "overview": {
        "ja": "オウム類（コンゴウインコ、ヨウム、キバタン等）は中〜大型鳥類（200g-1.5kg）。噛む力が非常に強く、保定に注意。イソフルラン吸入が標準。気管挿管は中大型種では可能。アフリカングレイ（ヨウム）はカルシウム代謝異常と呼吸器感染症が多い。",
        "en": "Parrots (macaws, African greys, cockatoos) are medium-large birds (200g-1.5kg). Very strong bite force; careful restraint needed. Isoflurane inhalation is standard. Intubation possible in medium-large species. African greys (Psittacus erithacus) prone to calcium deficiency and respiratory infections.",
    },
    "fasting": {
        "ja": "中型（200-500g）: 2-4時間。大型（>500g）: 4-6時間。そのう確認。",
        "en": "Medium (200-500g): 2-4 hr. Large (>500g): 4-6 hr. Check crop.",
    },
    "protocols": [
        {
            "name": {"ja": "吸入麻酔", "en": "Inhalation Anesthesia"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Isoflurane", "name_ja": "イソフルラン", "dose": "Induction: 3-5%, Maintenance: 1.5-3%", "route": "Mask → ET tube", "onset": "30-90 sec", "duration": "Continuous",
                 "notes_ja": "マスクで導入後、非カフETチューブで挿管（中大型種）。コンゴウインコ: 5-6mm、ヨウム: 4-5mm、オカメインコ: 2.5-3mm。", "notes": "Mask induction, then uncuffed ET tube (medium-large species). Macaw: 5-6mm, African grey: 4-5mm, cockatiel: 2.5-3mm."},
            ],
            "notes_ja": "大型オウムの保定は厚手の手袋を使用。嘴による重度の咬傷リスクあり。頸部を圧迫しないよう注意（気管の圧迫で窒息）。",
            "notes": "Use thick gloves for large parrot restraint. Risk of severe bite injuries. Avoid cervical compression (tracheal obstruction causes asphyxia).",
        },
        {
            "name": {"ja": "注射麻酔（補助的）", "en": "Injectable Anesthesia (Adjunctive)"},
            "category": "premedication",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Midazolam + Butorphanol", "name_ja": "ミダゾラム＋ブトルファノール", "dose": "0.5-1.0 mg/kg + 1-2 mg/kg", "route": "IM", "onset": "5-10 min", "duration": "30-60 min",
                 "notes_ja": "前投薬として使用。吸入麻酔薬の必要量を削減。", "notes": "Used as premedication. Reduces inhalant requirement."},
                {"name": "Ketamine + Midazolam", "name_ja": "ケタミン＋ミダゾラム", "dose": "10-20 mg/kg + 0.5-1.0 mg/kg", "route": "IM", "onset": "3-5 min", "duration": "15-30 min",
                 "notes_ja": "攻撃的で保定困難な場合に使用。覚醒が粗い場合あり。", "notes": "For aggressive birds difficult to restrain. Recovery may be rough."},
            ],
            "notes_ja": "IM注射は胸筋に26-27G針で。上腕骨は鳥類で含気骨（空気で満たされた骨）のため、上腕部への深い注射は骨折リスクがある。",
            "notes": "IM injection into pectoral muscle with 26-27G needle. Humerus is pneumatic (air-filled bone) in birds; deep upper arm injection risks fracture.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "150-350 bpm", "notes_ja": "食道聴診器またはドップラー。ECGも可能。", "notes": "Esophageal stethoscope or Doppler. ECG possible."},
                {"param": "RR", "target": "15-40 /min", "notes_ja": "呼吸パターンの変化に注意。呼吸停止はIPPV即開始。", "notes": "Watch for pattern changes. Apnea requires immediate IPPV."},
                {"param": "Temperature", "target": "40.0-42.0°C", "notes_ja": "低体温に注意。加温ランプまたはインキュベーター使用。", "notes": "Watch for hypothermia. Use heat lamp or incubator."},
                {"param": "Capnography", "target": "ETCO2 30-45 mmHg", "notes_ja": "非カフETチューブではリークがあるため値が低く出ることがある。", "notes": "Values may read low due to leak around uncuffed ET tube."},
            ],
            "notes_ja": "覚醒は速い（2-5分）。暗い静かな環境（インキュベーター30-32°C）で。大型オウムは覚醒時に暴れることがあるため、止まり木を除去しパッドで保護。",
            "notes": "Recovery is rapid (2-5 min). Dark, quiet environment (incubator 30-32°C). Large parrots may thrash during recovery; remove perches and pad surroundings.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.01-0.1 mg/kg", "route": "IV/IO/IT", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。IO: 脛足根骨または上腕骨遠位端。大型オウムでは血管アクセスが容易。", "notes": "For CPA. IO: tibiotarsus or distal humerus. Vascular access easier in large parrots."},
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "5-10 mg/kg", "route": "IV/IO", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時。", "notes": "For apnea."},
                {"name": "Atropine", "name_ja": "アトロピン", "dose": "0.02-0.05 mg/kg", "route": "IV/IO/IM", "onset": "1-2 min", "duration": "15-30 min",
                 "notes_ja": "徐脈時。", "notes": "For bradycardia."},
            ],
            "notes_ja": "大型オウムのCPR: 竜骨を圧迫（1-2回/sec）。気管挿管してIPPV（100% O2）。ヨウム（アフリカングレイ）はカルシウム低下による心停止リスクがあり、10%グルコン酸カルシウム50-100 mg/kg IV slowを検討。",
            "notes": "Large parrot CPR: keel compressions (1-2/sec). Intubate and IPPV (100% O2). African greys are at risk of cardiac arrest from hypocalcemia; consider calcium gluconate 10% 50-100 mg/kg IV slow.",
        },
    ],
}

# ============================================================
# REPTILE (General)
# ============================================================
ANESTHESIA_PROTOCOLS["reptile"] = {
    "species_name": {"ja": "爬虫類", "en": "Reptile"},
    "overview": {
        "ja": "爬虫類は変温動物のため、体温が薬物代謝に直接影響する。至適体温範囲（POTZ: Preferred Optimum Temperature Zone）を維持することが麻酔管理の鍵。心臓が3室（不完全な心室中隔）のため右左シャントが起こりうる。吸入麻酔の導入・覚醒が哺乳類より遅い（息止め可能）。",
        "en": "Reptiles are ectothermic; body temperature directly affects drug metabolism. Maintaining POTZ (Preferred Optimum Temperature Zone) is key to anesthetic management. Three-chambered heart (incomplete ventricular septum) allows right-to-left shunting. Inhalation induction/recovery is slower than mammals (breath-holding possible).",
    },
    "fasting": {
        "ja": "小型爬虫類: 12-24時間。大型爬虫類: 24-48時間。消化管通過が遅いため長めの絶食が必要。",
        "en": "Small reptiles: 12-24 hr. Large reptiles: 24-48 hr. Longer fasting needed due to slow GI transit.",
    },
    "protocols": [
        {
            "name": {"ja": "注射麻酔（推奨）", "en": "Injectable Anesthesia (Recommended)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "5-15 mg/kg", "route": "IV/IM/SC", "onset": "5-15 min (IM)", "duration": "30-90 min",
                 "notes_ja": "爬虫類で最も推奨される注射麻酔薬。IV投与は腹側尾静脈から。IM投与も有効。", "notes": "Most recommended injectable anesthetic for reptiles. IV via ventral tail vein. IM also effective."},
                {"name": "Ketamine + Midazolam", "name_ja": "ケタミン＋ミダゾラム", "dose": "5-30 mg/kg + 0.5-2 mg/kg", "route": "IM", "onset": "10-30 min", "duration": "30-120 min",
                 "notes_ja": "効果発現が遅い。覚醒も遅延する。", "notes": "Slow onset. Recovery also prolonged."},
                {"name": "Dexmedetomidine + Ketamine + Midazolam", "name_ja": "デクスメデトミジン＋ケタミン＋ミダゾラム", "dose": "50-100 μg/kg + 5-10 mg/kg + 0.5-1 mg/kg", "route": "IM", "onset": "10-20 min", "duration": "60-120 min",
                 "notes_ja": "深い鎮静。アティパメゾール＋フルマゼニルで部分拮抗。", "notes": "Deep sedation. Partially reversible with atipamezole + flumazenil."},
            ],
            "notes_ja": "爬虫類への注射は前肢または前半身に行う（腎門脈系を避ける）。後肢への注射は薬物が腎臓で初回通過代謝を受ける可能性がある。",
            "notes": "Inject in forelimbs or cranial body (avoid renal portal system). Hindlimb injection may result in first-pass metabolism through kidneys.",
        },
        {
            "name": {"ja": "吸入麻酔", "en": "Inhalation Anesthesia"},
            "category": "maintenance",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Isoflurane", "name_ja": "イソフルラン", "dose": "Induction: 3-5%, Maintenance: 1-3%", "route": "Mask / ET tube / Air sac", "onset": "10-30 min", "duration": "Continuous",
                 "notes_ja": "導入が遅い（息止めのため）。注射麻酔で導入後、気管挿管して吸入維持が推奨。爬虫類は長時間無呼吸が可能。", "notes": "Slow induction (breath-holding). Injectable induction followed by intubation and inhalation maintenance recommended. Reptiles can sustain prolonged apnea."},
                {"name": "Sevoflurane", "name_ja": "セボフルラン", "dose": "Induction: 6-8%, Maintenance: 3-5%", "route": "Mask / ET tube", "onset": "10-20 min", "duration": "Continuous",
                 "notes_ja": "イソフルランよりやや速い導入。", "notes": "Slightly faster induction than isoflurane."},
            ],
            "notes_ja": "爬虫類の気管挿管: 声門は舌の付け根に位置。非カフETチューブを使用。IPPV（4-6回/min）での換気が必要なことが多い。",
            "notes": "Reptile intubation: glottis at base of tongue. Use uncuffed ET tube. IPPV (4-6 breaths/min) often necessary.",
        },
        {
            "name": {"ja": "局所麻酔", "en": "Local Anesthesia"},
            "category": "local_regional",
            "risk_level": "low",
            "drugs": [
                {"name": "Lidocaine", "name_ja": "リドカイン", "dose": "Max 5 mg/kg", "route": "Local infiltration", "onset": "5-15 min", "duration": "30-60 min",
                 "notes_ja": "創傷修復、小腫瘤切除に使用。効果発現が哺乳類より遅い場合がある。", "notes": "For wound repair, small mass removal. Onset may be slower than in mammals."},
            ],
            "notes_ja": "爬虫類の疼痛評価は困難だが、鎮痛は必須。メロキシカム0.2-0.4 mg/kg IM/SC q24-48h。",
            "notes": "Reptile pain assessment is challenging, but analgesia is essential. Meloxicam 0.2-0.4 mg/kg IM/SC q24-48h.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "Species-dependent", "notes_ja": "ドップラーで確認。爬虫類の正常心拍数は種と体温に依存。ECGも可能。", "notes": "Confirm with Doppler. Normal HR depends on species and body temperature. ECG possible."},
                {"param": "RR", "target": "2-10 /min (depends on species)", "notes_ja": "呼吸数は非常に少ない。IPPV（4-6回/min）で管理。", "notes": "Very low respiratory rate. Manage with IPPV (4-6 breaths/min)."},
                {"param": "SpO2", "target": ">90%", "notes_ja": "プローブは舌、総排泄腔、または趾に装着。値の解釈に注意（爬虫類用のキャリブレーションではない）。", "notes": "Probe on tongue, cloaca, or digit. Interpret cautiously (not calibrated for reptiles)."},
                {"param": "Temperature", "target": "POTZ (species-specific)", "notes_ja": "体温管理が最重要。術中はPOTZの低い方で管理（代謝抑制）。覚醒時はPOTZの高い方に加温。", "notes": "Temperature management is paramount. Maintain at low POTZ during surgery (metabolic suppression). Warm to high POTZ for recovery."},
            ],
            "notes_ja": "覚醒は非常に遅い（数時間〜24時間）。POTZ上限に加温して代謝を促進。覚醒まで気管チューブを維持し、定期的にIPPVを実施。正向反射の回復で覚醒を確認。",
            "notes": "Recovery is very slow (hours to 24 hr). Warm to upper POTZ to promote metabolism. Maintain ET tube and provide periodic IPPV until recovery. Confirm recovery with righting reflex.",
        },
    ],
}

# ============================================================
# TORTOISE
# ============================================================
ANESTHESIA_PROTOCOLS["tortoise"] = {
    "species_name": {"ja": "リクガメ", "en": "Tortoise"},
    "overview": {
        "ja": "リクガメは甲羅のため心臓の聴診・モニタリングが困難。肺が甲羅の背側に位置するため、腹臥位で圧迫されない。注射は前肢の皮下または筋肉内。覚醒が非常に遅い（6-24時間）。",
        "en": "Tortoises: shell makes cardiac auscultation/monitoring difficult. Lungs are dorsal within shell, not compressed in sternal recumbency. Inject into forelimb SC/IM. Recovery is very slow (6-24 hr).",
    },
    "fasting": {
        "ja": "24-48時間絶食（消化管通過が極めて遅い）。",
        "en": "24-48 hr fast (very slow GI transit).",
    },
    "protocols": [
        {
            "name": {"ja": "鎮静・麻酔", "en": "Sedation/Anesthesia"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "10-15 mg/kg", "route": "IM (forelimb) / IV (jugular)", "onset": "10-30 min (IM)", "duration": "30-90 min",
                 "notes_ja": "前肢筋肉内注射。頸静脈からのIVも可能だが確保困難。効果発現まで忍耐が必要。", "notes": "IM into forelimb. IV via jugular possible but access is difficult. Patience needed for onset."},
                {"name": "Ketamine + Medetomidine", "name_ja": "ケタミン＋メデトミジン", "dose": "10-20 mg/kg + 0.1-0.15 mg/kg", "route": "IM", "onset": "15-30 min", "duration": "60-120 min",
                 "notes_ja": "深い鎮静。アティパメゾールで部分拮抗。四肢を甲羅から引き出すのに十分な筋弛緩。", "notes": "Deep sedation. Partially reversible with atipamezole. Sufficient muscle relaxation to extend limbs from shell."},
                {"name": "Isoflurane (maintenance)", "name_ja": "イソフルラン（維持）", "dose": "1-3%", "route": "ET tube", "onset": "", "duration": "Continuous",
                 "notes_ja": "注射麻酔で導入後、気管挿管して吸入維持。リクガメの声門は舌の付け根。", "notes": "After injectable induction, intubate and maintain with inhalation. Tortoise glottis at tongue base."},
            ],
            "notes_ja": "リクガメの頭を甲羅から引き出すのが導入の指標。完全に四肢が弛緩するまで待つ。POTZ: 26-32°C（種による）。",
            "notes": "Head extending from shell indicates onset. Wait for complete limb relaxation. POTZ: 26-32°C (species-dependent).",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "15-40 bpm (species/temp dependent)", "notes_ja": "ドップラー（頸部、前肢動脈に当てる）で確認。甲羅を通しての聴診は困難。", "notes": "Doppler (cervical area, forelimb artery). Auscultation through shell is difficult."},
                {"param": "RR", "target": "2-6 /min", "notes_ja": "IPPV 2-4回/min。呼吸数は非常に低い。", "notes": "IPPV 2-4/min. Respiratory rate is very low."},
                {"param": "Temperature", "target": "26-32°C (POTZ)", "notes_ja": "術中はPOTZ低い方。覚醒はPOTZ上限。", "notes": "Low POTZ during surgery. Upper POTZ for recovery."},
            ],
            "notes_ja": "覚醒は6-24時間かかる。POTZ上限に加温。気管チューブは覚醒まで維持。四肢引っ込め反射、頭部引っ込め反射で覚醒判定。",
            "notes": "Recovery takes 6-24 hr. Warm to upper POTZ. Maintain ET tube until recovery. Assess with limb/head withdrawal reflexes.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.1-0.5 mg/kg", "route": "IC/IV", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。心臓内（IC）投与が最も効果的。爬虫類の心臓は3室。", "notes": "For CPA. Intracardiac (IC) most effective. Reptile heart is 3-chambered."},
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "5-10 mg/kg", "route": "IV/IM", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時。爬虫類は長時間無呼吸が可能なため、真の呼吸停止かの判断が重要。", "notes": "For apnea. Reptiles can sustain prolonged apnea; determining true respiratory arrest is important."},
            ],
            "notes_ja": "爬虫類のCPR: IPPV（2-4回/min）が最重要。心臓マッサージは腹腔側から。低体温の個体はPOTZ上限まで加温してから判断（低体温で死亡に見えても回復することがある）。",
            "notes": "Reptile CPR: IPPV (2-4/min) is most critical. Cardiac massage from ventral approach. Warm hypothermic individuals to upper POTZ before pronouncing death (may recover from apparent death when hypothermic).",
        },
    ],
}

# ============================================================
# SNAKE
# ============================================================
ANESTHESIA_PROTOCOLS["snake"] = {
    "species_name": {"ja": "ヘビ", "en": "Snake"},
    "overview": {
        "ja": "ヘビは片肺（右肺が主、左肺は退化）。気管挿管は容易（声門が大きく開口する）。長時間の無呼吸が可能。体温管理が最重要。大型ヘビの保定には複数人が必要。毒蛇の麻酔は専門的知識が必要。",
        "en": "Snakes have a single functional lung (right; left is vestigial). Intubation is easy (large, visible glottis). Can sustain prolonged apnea. Temperature management is critical. Large snakes require multiple handlers. Venomous snake anesthesia requires specialized knowledge.",
    },
    "fasting": {
        "ja": "最後の給餌から7-14日後が理想（消化完了後）。",
        "en": "Ideally 7-14 days after last feeding (after digestion complete).",
    },
    "protocols": [
        {
            "name": {"ja": "鎮静・麻酔", "en": "Sedation/Anesthesia"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "5-15 mg/kg", "route": "IV (ventral tail vein) / IM", "onset": "5-15 min", "duration": "30-90 min",
                 "notes_ja": "腹側尾静脈からIV。IM投与は前半身の筋肉に。", "notes": "IV via ventral tail vein. IM into cranial body musculature."},
                {"name": "Ketamine + Midazolam", "name_ja": "ケタミン＋ミダゾラム", "dose": "10-20 mg/kg + 1-2 mg/kg", "route": "IM", "onset": "15-30 min", "duration": "60-120 min",
                 "notes_ja": "IM注射は前1/3の体幹筋に。", "notes": "IM injection into cranial 1/3 of body musculature."},
                {"name": "Isoflurane", "name_ja": "イソフルラン", "dose": "Maintenance: 1-3%", "route": "ET tube", "onset": "", "duration": "Continuous",
                 "notes_ja": "気管挿管は容易。非カフETチューブ使用。IPPV 2-4回/min。", "notes": "Intubation is easy. Uncuffed ET tube. IPPV 2-4/min."},
            ],
            "notes_ja": "ヘビは息止めで吸入麻酔の導入が非常に遅いため、注射麻酔で導入し吸入に移行するのが推奨。IV確保: 腹側尾静脈（心臓から尾側1/3の位置）。POTZ: 25-32°C。",
            "notes": "Breath-holding makes inhalation induction very slow in snakes. Injectable induction transitioning to inhalation is recommended. IV access: ventral tail vein (1/3 from tail tip). POTZ: 25-32°C.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "20-60 bpm", "notes_ja": "ドップラー（心臓直上）。ヘビの心臓は体長の1/4-1/3の位置。", "notes": "Doppler (directly over heart). Snake heart located at 1/4-1/3 body length."},
                {"param": "RR", "target": "2-8 /min", "notes_ja": "IPPV管理。自発呼吸の回復が覚醒の指標。", "notes": "IPPV management. Return of spontaneous breathing indicates recovery."},
            ],
            "notes_ja": "覚醒は遅い（数時間〜24時間）。POTZ上限に加温。舌のフリッキング（ちらつかせ）の回復が覚醒の指標。毒蛇は完全覚醒を確認するまで取り扱いに注意。",
            "notes": "Recovery is slow (hours to 24 hr). Warm to upper POTZ. Return of tongue flicking indicates recovery. Handle venomous snakes with extreme caution until fully recovered.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.1-0.5 mg/kg", "route": "IC/IV", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。心臓は体長の1/4-1/3の位置（体の前方寄り）。心臓内投与が有効。", "notes": "For CPA. Heart at 1/4-1/3 body length. Intracardiac injection effective."},
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "5-10 mg/kg", "route": "IV/IM", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時。", "notes": "For apnea."},
            ],
            "notes_ja": "ヘビのCPR: IPPV（2-4回/min、ETチューブ経由）が最優先。心臓マッサージは体前方1/4の腹側から。低体温個体はPOTZ上限に加温してから評価。毒蛇は防護手袋着用。",
            "notes": "Snake CPR: IPPV (2-4/min via ET tube) is top priority. Cardiac massage from ventral side at cranial 1/4 of body. Warm hypothermic individuals to upper POTZ before assessment. Use protective gloves for venomous species.",
        },
    ],
}

# ============================================================
# LIZARD
# ============================================================
ANESTHESIA_PROTOCOLS["lizard"] = {
    "species_name": {"ja": "トカゲ", "en": "Lizard"},
    "overview": {
        "ja": "トカゲは種による体格差が大きい（ヤモリ数g〜イグアナ数kg）。多くの種で自切（尾の自切）が起こるため尾での保定を避ける。フトアゴヒゲトカゲ、ヒョウモントカゲモドキは一般的な飼育種。気管挿管は小型種以外で可能。",
        "en": "Lizards vary greatly in size (geckos few grams to iguanas several kg). Many species have tail autotomy — avoid tail restraint. Bearded dragons and leopard geckos are common pet species. Intubation possible in all but smallest species.",
    },
    "fasting": {
        "ja": "12-24時間絶食。",
        "en": "12-24 hr fast.",
    },
    "protocols": [
        {
            "name": {"ja": "鎮静・麻酔", "en": "Sedation/Anesthesia"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "5-15 mg/kg", "route": "IV/IM", "onset": "5-15 min (IM)", "duration": "30-60 min",
                 "notes_ja": "IV: 腹側尾静脈。IM: 前肢。爬虫類で最も推奨。", "notes": "IV: ventral tail vein. IM: forelimb. Most recommended for reptiles."},
                {"name": "Ketamine + Medetomidine", "name_ja": "ケタミン＋メデトミジン", "dose": "10-20 mg/kg + 0.1-0.15 mg/kg", "route": "IM", "onset": "10-20 min", "duration": "60-120 min",
                 "notes_ja": "部分拮抗可。前肢に注射。", "notes": "Partially reversible. Inject into forelimb."},
                {"name": "Isoflurane", "name_ja": "イソフルラン", "dose": "Maintenance: 1-3%", "route": "Mask / ET tube", "onset": "", "duration": "Continuous",
                 "notes_ja": "注射導入後の維持に。小型種はマスク維持も可。", "notes": "For maintenance after injectable induction. Mask maintenance possible for small species."},
            ],
            "notes_ja": "フトアゴヒゲトカゲ: 前肢筋肉内にアルファキサロン10 mg/kg IMが標準。POTZ: 25-35°C（種による）。ヒョウモントカゲモドキは小型のためマスク吸入が主。",
            "notes": "Bearded dragon: alfaxalone 10 mg/kg IM into forelimb is standard. POTZ: 25-35°C (species-dependent). Leopard gecko: mask inhalation is primary due to small size.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "30-80 bpm (species/temp)", "notes_ja": "ドップラーで確認。", "notes": "Confirm with Doppler."},
                {"param": "RR", "target": "2-10 /min", "notes_ja": "IPPV 4-6回/min。", "notes": "IPPV 4-6/min."},
                {"param": "Temperature", "target": "POTZ (25-35°C)", "notes_ja": "体温管理が最重要。", "notes": "Temperature management is paramount."},
            ],
            "notes_ja": "覚醒は数時間〜24時間。正向反射の回復で覚醒を判定。覚醒後はPOTZ上限の環境に。術後鎮痛: メロキシカム0.2-0.4 mg/kg IM/SC q24-48h。",
            "notes": "Recovery: hours to 24 hr. Righting reflex return indicates recovery. Place in upper POTZ environment after recovery. Post-op analgesia: meloxicam 0.2-0.4 mg/kg IM/SC q24-48h.",
        },
        {
            "name": {"ja": "緊急対応", "en": "Emergency Protocols"},
            "category": "emergency",
            "risk_level": "high",
            "drugs": [
                {"name": "Epinephrine", "name_ja": "エピネフリン", "dose": "0.1-0.5 mg/kg", "route": "IC/IV", "onset": "Immediate", "duration": "3-5 min",
                 "notes_ja": "CPA時。心臓内注射。フトアゴヒゲトカゲの心臓は胸骨直後の腹側。", "notes": "For CPA. Intracardiac injection. Bearded dragon heart is ventral, just caudal to sternum."},
                {"name": "Doxapram", "name_ja": "ドキサプラム", "dose": "5-10 mg/kg", "route": "IV/IM", "onset": "30-60 sec", "duration": "5-10 min",
                 "notes_ja": "呼吸停止時。", "notes": "For apnea."},
            ],
            "notes_ja": "トカゲのCPR: IPPV（4-6回/min）+ 心臓マッサージ（腹側から）。尾の自切を起こさないよう取り扱い注意。低体温個体はPOTZ上限に加温してから評価。",
            "notes": "Lizard CPR: IPPV (4-6/min) + cardiac massage (ventral approach). Handle carefully to avoid tail autotomy. Warm hypothermic individuals to upper POTZ before assessment.",
        },
    ],
}

# ============================================================
# AMPHIBIAN
# ============================================================
ANESTHESIA_PROTOCOLS["amphibian"] = {
    "species_name": {"ja": "両生類", "en": "Amphibian"},
    "overview": {
        "ja": "両生類（カエル、イモリ、サンショウウオ等）は皮膚呼吸を行い、経皮的に薬物を吸収する。麻酔は水中浸漬法（MS-222等）が標準。皮膚を乾燥させない。手袋は粉なしを使用（皮膚毒性）。体温管理は水温で行う。",
        "en": "Amphibians (frogs, newts, salamanders) perform cutaneous respiration and absorb drugs transcutaneously. Immersion anesthesia (MS-222 etc.) is standard. Never let skin dry. Use powder-free gloves (skin toxicity). Temperature management via water temperature.",
    },
    "fasting": {
        "ja": "24-48時間絶食（消化管内容物の排出促進のため）。",
        "en": "24-48 hr fast (to promote GI emptying).",
    },
    "protocols": [
        {
            "name": {"ja": "浸漬麻酔（標準法）", "en": "Immersion Anesthesia (Standard)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "MS-222 (Tricaine)", "name_ja": "MS-222（トリカイン）", "dose": "1-3 g/L (buffered to pH 7.0)", "route": "Immersion", "onset": "5-15 min", "duration": "Until removed from solution",
                 "notes_ja": "最も広く使用される両生類麻酔薬。重炭酸ナトリウムでpH 7.0にバッファー（未バッファーは組織障害）。深さは外刺激への反応消失で判定。", "notes": "Most widely used amphibian anesthetic. Buffer to pH 7.0 with sodium bicarbonate (unbuffered causes tissue damage). Depth assessed by loss of response to stimuli."},
                {"name": "Eugenol (Clove oil)", "name_ja": "オイゲノール（クローブオイル）", "dose": "50-100 mg/L", "route": "Immersion", "onset": "5-15 min", "duration": "Until removed",
                 "notes_ja": "MS-222の代替。安価。pH調整不要。", "notes": "Alternative to MS-222. Inexpensive. No pH adjustment needed."},
                {"name": "Isoflurane (topical/immersion)", "name_ja": "イソフルラン（局所/浸漬）", "dose": "0.5-1 mL/L water", "route": "Topical / Immersion", "onset": "5-10 min", "duration": "Until removed",
                 "notes_ja": "皮膚からの吸収で麻酔。小型両生類に有効。", "notes": "Absorbed through skin. Effective for small amphibians."},
            ],
            "notes_ja": "浸漬麻酔中は定期的に（5分毎）体位変換し、皮膚の乾燥を防ぐ。脱塩素水（カルキ抜き）を使用。麻酔深度は正向反射消失→外刺激反応消失→角膜反射消失の順に深くなる。",
            "notes": "Reposition q5min during immersion. Use dechlorinated water. Depth progression: loss of righting reflex → loss of response to stimuli → loss of corneal reflex.",
        },
        {
            "name": {"ja": "注射麻酔（大型種・浸漬困難時）", "en": "Injectable Anesthesia (Large Species/When Immersion Difficult)"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "10-20 mg/kg", "route": "SC (dorsal lymph sac) / IM", "onset": "10-20 min", "duration": "30-90 min",
                 "notes_ja": "背側リンパ嚢への皮下注射が一般的。IM投与も可能。", "notes": "SC injection into dorsal lymph sac is common. IM also possible."},
                {"name": "Ketamine", "name_ja": "ケタミン", "dose": "50-150 mg/kg", "route": "SC / IM / dorsal lymph sac", "onset": "10-30 min", "duration": "30-120 min",
                 "notes_ja": "用量が高い。覚醒が遅延する場合あり。", "notes": "High doses required. Recovery may be prolonged."},
            ],
            "notes_ja": "両生類は皮膚が非常にデリケート。常に湿潤状態を維持し、直接手で触れる場合は手を水で濡らす。",
            "notes": "Amphibian skin is extremely delicate. Maintain moisture at all times. Wet hands before direct contact.",
        },
        {
            "name": {"ja": "モニタリング・回復", "en": "Monitoring & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "20-60 bpm (species/temp)", "notes_ja": "ドップラーで心拍確認。視認できる場合は胸壁/喉の動きで判断。", "notes": "Doppler for heart rate. If visible, chest/throat movement can be used."},
                {"param": "Depth", "target": "Loss of righting reflex", "notes_ja": "正向反射消失=外科的麻酔平面。角膜反射消失は深すぎ。", "notes": "Loss of righting reflex = surgical plane. Loss of corneal reflex = too deep."},
                {"param": "Skin moisture", "target": "Continuously moist", "notes_ja": "皮膚乾燥は致死的。定期的に脱塩素水をスプレー。", "notes": "Skin desiccation is lethal. Spray with dechlorinated water regularly."},
            ],
            "notes_ja": "回復: 新鮮な脱塩素水に移す。正向反射の回復を確認。低酸素耐性は高いが、長時間の浸漬は肺水腫リスク。完全回復まで浅い水で監視。",
            "notes": "Recovery: transfer to fresh dechlorinated water. Confirm righting reflex return. High hypoxia tolerance but prolonged immersion risks pulmonary edema. Monitor in shallow water until full recovery.",
        },
    ],
}

# ============================================================
# FISH
# ============================================================
ANESTHESIA_PROTOCOLS["fish"] = {
    "species_name": {"ja": "魚", "en": "Fish"},
    "overview": {
        "ja": "魚の麻酔は水中浸漬法で行う。MS-222（トリカイン）が最も一般的。麻酔深度は4段階（Stage I-IV）で評価。水温・pH・種によって効果が異なる。観賞魚では手術（腫瘤切除、浮袋手術等）が増加している。",
        "en": "Fish anesthesia is performed via immersion. MS-222 (tricaine) is most common. Depth assessed in 4 stages (I-IV). Effects vary with water temperature, pH, and species. Surgical procedures (mass removal, swim bladder surgery) are increasing in pet fish.",
    },
    "fasting": {
        "ja": "24-48時間絶食（水質維持と消化管排出のため）。",
        "en": "24-48 hr fast (for water quality and GI emptying).",
    },
    "protocols": [
        {
            "name": {"ja": "浸漬麻酔", "en": "Immersion Anesthesia"},
            "category": "induction",
            "risk_level": "moderate",
            "drugs": [
                {"name": "MS-222 (Tricaine)", "name_ja": "MS-222（トリカイン）", "dose": "50-150 mg/L (buffered)", "route": "Immersion", "onset": "3-10 min", "duration": "Until removed",
                 "notes_ja": "重炭酸ナトリウムでバッファー（pH 7.0-7.5）。鎮静: 50 mg/L、外科麻酔: 100-150 mg/L。水温が高いほど効果増大（用量減）。", "notes": "Buffer with sodium bicarbonate (pH 7.0-7.5). Sedation: 50 mg/L, surgical: 100-150 mg/L. Higher water temp increases effect (reduce dose)."},
                {"name": "Eugenol (Clove oil)", "name_ja": "オイゲノール（クローブオイル）", "dose": "40-100 mg/L", "route": "Immersion", "onset": "3-10 min", "duration": "Until removed",
                 "notes_ja": "エタノールに溶解して使用。安価で入手しやすい。鎮静: 40 mg/L、外科: 60-100 mg/L。", "notes": "Dissolve in ethanol before use. Inexpensive and accessible. Sedation: 40 mg/L, surgical: 60-100 mg/L."},
                {"name": "2-Phenoxyethanol", "name_ja": "2-フェノキシエタノール", "dose": "0.2-0.5 mL/L", "route": "Immersion", "onset": "3-5 min", "duration": "Until removed",
                 "notes_ja": "MS-222の代替。一部の種で有効性が高い。", "notes": "Alternative to MS-222. More effective in some species."},
            ],
            "notes_ja": "麻酔水は飼育水と同じ水温・pHを使用。酸素供給のためエアレーション。鰓蓋の動き（opercular movement）で麻酔深度を評価。",
            "notes": "Use anesthetic water at same temperature/pH as housing water. Aerate for oxygen. Assess depth by opercular (gill cover) movement.",
        },
        {
            "name": {"ja": "手術中の管理", "en": "Intraoperative Management"},
            "category": "maintenance",
            "risk_level": "moderate",
            "drugs": [],
            "notes_ja": "手術は魚を水から出して実施（濡れたスポンジの上に置く）。鰓に麻酔水を灌流するリサーキュレーションシステム（ポンプ＋チューブ→口→鰓→回収）を使用。手術部位以外は濡れたガーゼで覆う。手術時間は可能な限り短く。",
            "notes": "Surgery performed out of water (on wet sponge). Use recirculation system (pump + tubing → mouth → gills → collection) to irrigate gills with anesthetic water. Cover body with wet gauze except surgical site. Minimize surgical time.",
        },
        {
            "name": {"ja": "麻酔深度・回復", "en": "Depth Assessment & Recovery"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "Stage I (Sedation)", "target": "Reduced swimming, responsive", "notes_ja": "遊泳活動低下、色調変化、刺激に反応あり。輸送・軽処置用。", "notes": "Reduced swimming, color change, responds to stimuli. For transport/minor procedures."},
                {"param": "Stage II (Light anesthesia)", "target": "Loss of equilibrium", "notes_ja": "平衡感覚喪失、鰓蓋運動は規則的。外科的刺激にまだ反応。", "notes": "Loss of equilibrium, opercular movement regular. Still responds to surgical stimuli."},
                {"param": "Stage III (Surgical)", "target": "No response to stimuli", "notes_ja": "外科的刺激に無反応。鰓蓋運動は減少するが持続。手術可能。", "notes": "No response to stimuli. Opercular movement reduced but present. Surgery possible."},
                {"param": "Stage IV (Overdose)", "target": "Opercular movement stops", "notes_ja": "鰓蓋運動停止。直ちに新鮮水に移す。死亡リスク。", "notes": "Opercular movement stops. Immediately transfer to fresh water. Risk of death."},
            ],
            "notes_ja": "回復: 新鮮な（麻酔薬を含まない）エアレーション水に移す。口を開けて水流を当て、鰓を灌流。正常遊泳の回復まで監視。回復には3-15分。",
            "notes": "Recovery: transfer to fresh (anesthetic-free) aerated water. Direct water flow into mouth to irrigate gills. Monitor until normal swimming resumes. Recovery takes 3-15 min.",
        },
    ],
}

# ============================================================
# EXOTIC OTHER
# ============================================================
ANESTHESIA_PROTOCOLS["exotic_other"] = {
    "species_name": {"ja": "その他エキゾチック", "en": "Exotic Other"},
    "overview": {
        "ja": "その他のエキゾチック動物（チンチラ以外の齧歯類、有袋類、小型霊長類、ミニブタ等）は種ごとに大きく異なる。共通原則: 体温管理、正確な体重測定、低血糖予防、最小限のストレス。種特異的な文献を参照。",
        "en": "Other exotic animals (non-chinchilla rodents, marsupials, small primates, mini-pigs, etc.) vary greatly by species. Common principles: temperature management, accurate weighing, hypoglycemia prevention, minimal stress. Consult species-specific literature.",
    },
    "fasting": {
        "ja": "小型種: 絶食不要〜2時間。中型種: 4-6時間。種による。",
        "en": "Small species: no fasting to 2 hr. Medium species: 4-6 hr. Species-dependent.",
    },
    "protocols": [
        {
            "name": {"ja": "一般原則", "en": "General Principles"},
            "category": "sedation",
            "risk_level": "moderate",
            "drugs": [
                {"name": "Isoflurane (chamber/mask)", "name_ja": "イソフルラン（チャンバー/マスク）", "dose": "Species-dependent", "route": "Inhalation", "onset": "Variable", "duration": "Continuous",
                 "notes_ja": "ほぼ全てのエキゾチック種で安全に使用可能。小型種では最も推奨。", "notes": "Can be used safely in nearly all exotic species. Most recommended for small species."},
                {"name": "Alfaxalone", "name_ja": "アルファキサロン", "dose": "Species-dependent (3-15 mg/kg)", "route": "IM/IV/SC", "onset": "5-30 min", "duration": "15-90 min",
                 "notes_ja": "多くのエキゾチック種で安全性が高い。用量は種と体重で調整。", "notes": "High safety margin in many exotic species. Adjust dose by species and body weight."},
                {"name": "Ketamine + Midazolam", "name_ja": "ケタミン＋ミダゾラム", "dose": "Species-dependent", "route": "IM/IP", "onset": "5-30 min", "duration": "20-60 min",
                 "notes_ja": "多くの種で使用実績あり。用量は文献参照。", "notes": "Established use in many species. Consult literature for dosing."},
            ],
            "notes_ja": "未知の種に対する麻酔は、最も近縁な既知種のプロトコルを参考に、低用量から開始し、効果を確認しながら追加投与（titrate to effect）。",
            "notes": "For unfamiliar species, use protocols from most closely related known species. Start at low dose and titrate to effect.",
        },
        {
            "name": {"ja": "共通モニタリング指針", "en": "Common Monitoring Guidelines"},
            "category": "monitoring",
            "risk_level": "low",
            "drugs": [],
            "monitoring_params": [
                {"param": "HR", "target": "Species-dependent", "notes_ja": "ドップラーが最も汎用的。体重10g以上であれば使用可能。", "notes": "Doppler is most versatile. Usable for animals >10g."},
                {"param": "RR", "target": "Species-dependent", "notes_ja": "胸壁の動きを目視。呼吸停止はドキサプラムまたはIPPV。", "notes": "Visual chest wall movement. Apnea: doxapram or IPPV."},
                {"param": "Temperature", "target": "Species-dependent", "notes_ja": "ほぼ全ての小型動物で低体温が最大リスク。加温パッド必須。", "notes": "Hypothermia is the greatest risk in nearly all small animals. Warming pad essential."},
                {"param": "Reflexes", "target": "Toe pinch / Palpebral", "notes_ja": "趾反射と眼瞼反射で深度評価。", "notes": "Assess depth with toe pinch and palpebral reflex."},
            ],
            "notes_ja": "全エキゾチック種共通: (1)正確な体重測定、(2)体温管理、(3)低血糖予防、(4)最小限のストレス。術後鎮痛はメロキシカム（種による用量調整）が第一選択。",
            "notes": "Common to all exotics: (1) accurate weighing, (2) temperature management, (3) hypoglycemia prevention, (4) minimal stress. Meloxicam (dose per species) is first-line post-op analgesic.",
        },
    ],
}


def get_protocols_for_species(species_id):
    """Return anesthesia protocols for a given species."""
    return ANESTHESIA_PROTOCOLS.get(species_id)


def get_all_species_ids():
    """Return list of species IDs with anesthesia protocols."""
    return list(ANESTHESIA_PROTOCOLS.keys())


def search_protocols(query="", species="", category=""):
    """Search protocols by query string, species, and/or category."""
    results = []
    species_list = [species] if species else list(ANESTHESIA_PROTOCOLS.keys())

    for sp in species_list:
        sp_data = ANESTHESIA_PROTOCOLS.get(sp)
        if not sp_data:
            continue

        for protocol in sp_data.get("protocols", []):
            # Filter by category
            if category and protocol.get("category") != category:
                continue

            # Filter by query
            if query:
                q = query.lower()
                searchable = " ".join([
                    protocol.get("name", {}).get("ja", ""),
                    protocol.get("name", {}).get("en", ""),
                    protocol.get("notes_ja", ""),
                    protocol.get("notes", ""),
                ] + [
                    d.get("name", "") + " " + d.get("name_ja", "")
                    for d in protocol.get("drugs", [])
                ]).lower()
                if q not in searchable:
                    continue

            results.append({
                "species": sp,
                "species_name": sp_data["species_name"],
                "protocol": protocol,
            })

    return results
