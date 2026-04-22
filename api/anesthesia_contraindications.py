"""Anesthesia drug-disease contraindication and interaction rules.

Clinical contraindication data for anesthesia drug selection based on
patient comorbidities, breed, and species-specific considerations.
"""

# Severity levels for contraindication warnings
SEVERITY_CONTRAINDICATED = "contraindicated"  # Absolute contraindication
SEVERITY_CAUTION = "caution"  # Use with caution, dose adjustment needed
SEVERITY_MONITOR = "monitor"  # Extra monitoring required

# Drug-disease interaction rules
# Each rule: drug pattern → condition → severity + message (ja/en)
DRUG_CONTRAINDICATIONS = [
    # === Cardiovascular ===
    {
        "drug_patterns": ["dexmedetomidine", "medetomidine", "デクスメデトミジン", "メデトミジン"],
        "conditions": [
            "cardiac_disease",
            "heart_failure",
            "cardiomyopathy",
            "aortic_stenosis",
            "pulmonic_stenosis",
            "bradycardia",
        ],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "α2作動薬は心疾患に禁忌。徐脈・高度房室ブロック・心拍出量低下のリスク。代替: ブトルファノール/ミダゾラム",
        "message_en": "Alpha-2 agonists contraindicated in cardiac disease. Risk of bradycardia, AV block, decreased cardiac output. Alternative: butorphanol/midazolam",
    },
    {
        "drug_patterns": ["xylazine", "キシラジン"],
        "conditions": ["cardiac_disease", "heart_failure", "cardiomyopathy", "bradycardia"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "キシラジンは心疾患に禁忌。重度の徐脈・房室ブロックを引き起こす。代替: ブトルファノール",
        "message_en": "Xylazine contraindicated in cardiac disease. Causes severe bradycardia and AV block. Alternative: butorphanol",
    },
    {
        "drug_patterns": ["thiopental", "チオペンタール"],
        "conditions": ["cardiac_disease", "heart_failure", "hypovolemia", "shock"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "チオペンタールは心機能低下・循環血液量減少に禁忌。心筋抑制が強い。代替: プロポフォール（低用量）/アルファキサロン",
        "message_en": "Thiopental contraindicated in cardiac dysfunction/hypovolemia. Strong myocardial depression. Alternative: propofol (low dose)/alfaxalone",
    },
    # === GI / Hepatic ===
    {
        "drug_patterns": [
            "nsaid",
            "meloxicam",
            "carprofen",
            "firocoxib",
            "メロキシカム",
            "カルプロフェン",
            "フィロコキシブ",
        ],
        "conditions": ["renal_disease", "kidney_failure", "ckd", "aki"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "NSAIDsは腎疾患に禁忌。腎血流低下による急性腎障害のリスク。代替: オピオイド（ブトルファノール、ブプレノルフィン）",
        "message_en": "NSAIDs contraindicated in renal disease. Risk of acute kidney injury from decreased renal blood flow. Alternative: opioids (butorphanol, buprenorphine)",
    },
    {
        "drug_patterns": [
            "nsaid",
            "meloxicam",
            "carprofen",
            "firocoxib",
            "メロキシカム",
            "カルプロフェン",
            "フィロコキシブ",
        ],
        "conditions": ["gi_ulcer", "gi_bleeding", "gastric_ulcer", "inflammatory_bowel_disease"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "NSAIDsは消化管潰瘍・出血に禁忌。消化管出血悪化のリスク。代替: オピオイド鎮痛",
        "message_en": "NSAIDs contraindicated in GI ulceration/bleeding. Risk of worsening GI hemorrhage. Alternative: opioid analgesia",
    },
    {
        "drug_patterns": ["nsaid", "meloxicam", "carprofen", "メロキシカム", "カルプロフェン"],
        "conditions": ["hepatic_disease", "liver_failure", "hepatic_lipidosis"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "NSAIDsは肝疾患で慎重投与。肝代謝低下により薬物蓄積のリスク。用量減量を検討",
        "message_en": "NSAIDs: use with caution in hepatic disease. Risk of drug accumulation due to decreased hepatic metabolism. Consider dose reduction",
    },
    # === Respiratory ===
    {
        "drug_patterns": ["morphine", "モルヒネ"],
        "conditions": ["respiratory_disease", "upper_airway_obstruction", "brachycephalic", "laryngeal_paralysis"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "モルヒネは呼吸器疾患で慎重投与。呼吸抑制・ヒスタミン遊離リスク。低用量から開始し呼吸モニタリング必須",
        "message_en": "Morphine: use with caution in respiratory disease. Risk of respiratory depression and histamine release. Start low dose, monitor respiration closely",
    },
    {
        "drug_patterns": ["acepromazine", "アセプロマジン"],
        "conditions": ["brachycephalic", "upper_airway_obstruction"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "アセプロマジンは短頭種で慎重投与。上気道弛緩による閉塞リスク。低用量使用し気道確保準備",
        "message_en": "Acepromazine: use with caution in brachycephalic breeds. Risk of upper airway relaxation and obstruction. Use low dose, prepare for airway management",
    },
    # === Breed-specific ===
    {
        "drug_patterns": ["thiopental", "チオペンタール"],
        "conditions": ["sighthound", "greyhound", "サイトハウンド", "グレイハウンド"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "チオペンタールはサイトハウンドに禁忌。体脂肪率が低く覚醒遅延・重篤化。代替: プロポフォール/アルファキサロン",
        "message_en": "Thiopental contraindicated in sighthounds. Low body fat causes prolonged recovery and toxicity. Alternative: propofol/alfaxalone",
    },
    {
        "drug_patterns": ["acepromazine", "アセプロマジン"],
        "conditions": ["boxer", "ボクサー"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "アセプロマジンはボクサー犬で慎重投与。低血圧・失神のリスクが他犬種より高い。用量を50%減量",
        "message_en": "Acepromazine: use with caution in Boxers. Higher risk of hypotension and syncope. Reduce dose by 50%",
    },
    {
        "drug_patterns": ["acepromazine", "アセプロマジン"],
        "conditions": ["giant_breed", "大型犬"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "アセプロマジンは大型犬で低血圧リスクが高い。最大用量を超えない（体重あたりの用量を低く設定）",
        "message_en": "Acepromazine: higher risk of hypotension in giant breeds. Do not exceed maximum dose, use lower end of dose range",
    },
    # === Species-specific ===
    {
        "drug_patterns": ["ketamine", "ケタミン"],
        "conditions": ["cat_hcm", "hypertrophic_cardiomyopathy"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "ケタミンは猫の肥大型心筋症（HCM）で慎重投与。交感神経刺激による心拍数増加が有害。低用量使用",
        "message_en": "Ketamine: use with caution in feline HCM. Sympathetic stimulation increases heart rate, potentially harmful. Use low dose",
    },
    {
        "drug_patterns": ["dexmedetomidine", "medetomidine", "デクスメデトミジン", "メデトミジン"],
        "conditions": ["rabbit", "ウサギ"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "α2作動薬はウサギで慎重投与。30%のウサギがアトロピナーゼ陽性（アトロピンによる拮抗が効かない）。徐脈時はグリコピロレート使用",
        "message_en": "Alpha-2 agonists: use with caution in rabbits. 30% are atropinase-positive (atropine antagonism ineffective). Use glycopyrrolate for bradycardia",
    },
    {
        "drug_patterns": ["fipronil", "フィプロニル"],
        "conditions": ["rabbit", "ウサギ"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "フィプロニルはウサギに致死的。絶対禁忌",
        "message_en": "Fipronil is lethal in rabbits. Absolutely contraindicated",
    },
    {
        "drug_patterns": ["fipronil", "フィプロニル"],
        "conditions": ["chinchilla", "チンチラ"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "フィプロニルはチンチラに致死的。絶対禁忌",
        "message_en": "Fipronil is lethal in chinchillas. Absolutely contraindicated",
    },
    # === Endocrine / Metabolic ===
    {
        "drug_patterns": [
            "dexmedetomidine",
            "medetomidine",
            "xylazine",
            "デクスメデトミジン",
            "メデトミジン",
            "キシラジン",
        ],
        "conditions": ["diabetes", "diabetic_ketoacidosis", "糖尿病"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "α2作動薬は糖尿病で慎重投与。インスリン分泌抑制により高血糖を悪化させるリスク。血糖モニタリング必須",
        "message_en": "Alpha-2 agonists: use with caution in diabetes. Risk of worsening hyperglycemia via insulin suppression. Monitor blood glucose",
    },
    {
        "drug_patterns": [
            "dexmedetomidine",
            "medetomidine",
            "xylazine",
            "デクスメデトミジン",
            "メデトミジン",
            "キシラジン",
        ],
        "conditions": ["insulinoma", "インスリノーマ"],
        "severity": SEVERITY_MONITOR,
        "message_ja": "α2作動薬はインスリノーマで血糖変動を引き起こす可能性。術中の血糖モニタリング（30分毎）を推奨",
        "message_en": "Alpha-2 agonists may cause blood glucose fluctuations with insulinoma. Recommend intraoperative glucose monitoring every 30 min",
    },
    # === Seizure disorders ===
    {
        "drug_patterns": ["acepromazine", "アセプロマジン"],
        "conditions": ["seizure", "epilepsy", "てんかん"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "アセプロマジンはてんかん患者に禁忌。痙攣閾値を低下させる。代替: ミダゾラム/ブトルファノール",
        "message_en": "Acepromazine contraindicated in epileptic patients. Lowers seizure threshold. Alternative: midazolam/butorphanol",
    },
    # === Coagulopathy ===
    {
        "drug_patterns": ["nsaid", "meloxicam", "carprofen", "メロキシカム", "カルプロフェン"],
        "conditions": ["coagulopathy", "thrombocytopenia", "dic", "凝固障害", "血小板減少症"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "NSAIDsは凝固障害・血小板減少症に禁忌。出血リスク増大。代替: オピオイド鎮痛",
        "message_en": "NSAIDs contraindicated in coagulopathy/thrombocytopenia. Increased bleeding risk. Alternative: opioid analgesia",
    },
    # === GDV (Gastric Dilatation-Volvulus) ===
    {
        "drug_patterns": ["thiopental", "チオペンタール"],
        "conditions": ["gdv", "gastric_dilatation_volvulus", "胃拡張捻転"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "チオペンタールはGDVに禁忌。循環不全患者での心筋抑制が致死的。代替: フェンタニル/リドカイン/ケタミン",
        "message_en": "Thiopental contraindicated in GDV. Myocardial depression in hemodynamically compromised patients is lethal. Alternative: fentanyl/lidocaine/ketamine",
    },
    # === Pregnancy ===
    {
        "drug_patterns": ["nsaid", "meloxicam", "メロキシカム"],
        "conditions": ["pregnancy", "妊娠"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "NSAIDsは妊娠動物に禁忌。胎児の動脈管早期閉鎖・腎障害のリスク。代替: オピオイド鎮痛",
        "message_en": "NSAIDs contraindicated in pregnant animals. Risk of premature ductus arteriosus closure and fetal renal damage. Alternative: opioid analgesia",
    },
    # === Equine-specific ===
    {
        "drug_patterns": ["halothane", "ハロタン"],
        "conditions": ["horse", "馬"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "ハロタンは馬の悪性高熱症リスク。可能であればイソフルラン/セボフルランを使用。ダントロレン準備",
        "message_en": "Halothane: malignant hyperthermia risk in horses. Use isoflurane/sevoflurane if possible. Have dantrolene available",
    },
    # === Reptile-specific ===
    {
        "drug_patterns": ["ketamine", "ケタミン"],
        "conditions": ["reptile_renal", "reptile", "爬虫類"],
        "severity": SEVERITY_MONITOR,
        "message_ja": "ケタミンは爬虫類で腎排泄。腎門脈系を考慮し後肢注射を避ける（前肢に投与）。腎疾患時は用量減量。参考: Divers & Stahl (2019)",
        "message_en": "Ketamine is renally excreted in reptiles. Avoid hind limb injection due to renal portal system (use forelimb). Reduce dose in renal disease. Ref: Divers & Stahl (2019)",
    },
    # === Additional clinical rules ===
    {
        "drug_patterns": ["propofol", "プロポフォール"],
        "conditions": ["cat_repeated", "cat", "猫"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "プロポフォールは猫で反復投与時にハインツ小体性貧血のリスク。連日使用を避ける。単回使用は安全。参考: Grimm et al. (2015)",
        "message_en": "Propofol: risk of Heinz body anemia with repeated use in cats. Avoid consecutive daily use. Single use is safe. Ref: Grimm et al. (2015)",
    },
    {
        "drug_patterns": ["ketamine", "ケタミン"],
        "conditions": ["renal_disease", "kidney_failure", "ckd", "aki"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "ケタミンは腎排泄型。腎機能低下時は作用延長・蓄積リスク。用量を50%減量するか代替薬（プロポフォール/アルファキサロン）を検討。参考: Grimm et al. (2015)",
        "message_en": "Ketamine is renally excreted. Risk of prolonged action and accumulation in renal failure. Reduce dose by 50% or use alternatives (propofol/alfaxalone). Ref: Grimm et al. (2015)",
    },
    {
        "drug_patterns": ["atropine", "アトロピン"],
        "conditions": ["glaucoma", "緑内障"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "アトロピンは緑内障に禁忌。散瞳により眼圧上昇を悪化。代替: グリコピロレート（眼への影響が少ない）。参考: Grimm et al. (2015)",
        "message_en": "Atropine contraindicated in glaucoma. Mydriasis worsens intraocular pressure. Alternative: glycopyrrolate (less ocular effect). Ref: Grimm et al. (2015)",
    },
    {
        "drug_patterns": ["succinylcholine", "スキサメトニウム", "サクシニルコリン"],
        "conditions": ["hyperkalemia", "高カリウム血症", "renal_disease", "urinary_obstruction"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "スキサメトニウムは高カリウム血症に禁忌。カリウム遊離により致死的不整脈のリスク。代替: 非脱分極性筋弛緩薬。参考: Grimm et al. (2015)",
        "message_en": "Succinylcholine contraindicated in hyperkalemia. Risk of fatal arrhythmia from potassium release. Alternative: non-depolarizing muscle relaxants. Ref: Grimm et al. (2015)",
    },
    {
        "drug_patterns": ["dexmedetomidine", "medetomidine", "デクスメデトミジン", "メデトミジン"],
        "conditions": ["pheochromocytoma", "褐色細胞腫", "adrenal_tumor"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "α2作動薬は褐色細胞腫に禁忌。カテコラミン放出を誘発し高血圧クリーゼのリスク。参考: Grimm et al. (2015)",
        "message_en": "Alpha-2 agonists contraindicated in pheochromocytoma. Risk of catecholamine release and hypertensive crisis. Ref: Grimm et al. (2015)",
    },
    {
        "drug_patterns": ["tiletamine", "チレタミン", "telazol", "テラゾール"],
        "conditions": ["cat", "猫"],
        "severity": SEVERITY_CAUTION,
        "message_ja": "チレタミン/ゾラゼパム（テラゾール）は猫で腎排泄が遅く覚醒延長。腎疾患猫では禁忌に近い。犬より低用量で使用。参考: Carpenter (2018)",
        "message_en": "Tiletamine/zolazepam (Telazol): slow renal excretion in cats causes prolonged recovery. Near-contraindicated in cats with renal disease. Use lower dose than dogs. Ref: Carpenter (2018)",
    },
    {
        "drug_patterns": ["penicillin", "ペニシリン", "amoxicillin", "アモキシシリン", "ampicillin", "アンピシリン"],
        "conditions": ["guinea_pig", "モルモット"],
        "severity": SEVERITY_CONTRAINDICATED,
        "message_ja": "ペニシリン系抗菌薬はモルモットに禁忌。致死性の腸内細菌叢破壊（dysbiosis）を引き起こす。代替: エンロフロキサシン、TMS。参考: Quesenberry & Carpenter (2020)",
        "message_en": "Penicillin antibiotics are contraindicated in guinea pigs. Causes lethal dysbiosis. Alternatives: enrofloxacin, TMS. Ref: Quesenberry & Carpenter (2020)",
    },
]


def check_contraindications(drug_name, conditions=None, species=None, breed=None):
    """Check drug against known contraindication rules.

    Args:
        drug_name: Name of the drug to check (English or Japanese)
        conditions: List of condition tags (e.g. ["cardiac_disease", "renal_disease"])
        species: Species identifier (e.g. "rabbit", "horse")
        breed: Breed name (e.g. "greyhound", "boxer")

    Returns:
        List of matching contraindication warnings, each with severity and message.
    """
    if not drug_name:
        return []

    drug_lower = drug_name.lower()
    all_tags = set()
    if conditions:
        all_tags.update(c.lower() for c in conditions)
    if species:
        all_tags.add(species.lower())
    if breed:
        all_tags.add(breed.lower())

    warnings = []
    for rule in DRUG_CONTRAINDICATIONS:
        # Check if drug matches any pattern
        drug_match = any(p.lower() in drug_lower for p in rule["drug_patterns"])
        if not drug_match:
            continue
        # Check if any condition matches
        cond_match = any(c.lower() in all_tags for c in rule["conditions"])
        if not cond_match:
            continue
        warnings.append(
            {
                "severity": rule["severity"],
                "message_ja": rule["message_ja"],
                "message_en": rule["message_en"],
            }
        )

    return warnings


def get_all_contraindications():
    """Return all contraindication rules for frontend display."""
    return DRUG_CONTRAINDICATIONS
