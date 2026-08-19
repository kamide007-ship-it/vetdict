"""Drug batch 40 – referenced-but-absent agents surfaced by the 2026-08 audit (8th sweep).

A katakana token-frequency sweep of the served disease treatment protocols,
resolved against the actual text→drug matcher, found two antibacterials that
VetDict's own content instructs clinicians to use — yet were absent from the
formulary:

  - エタンブトール (ethambutol): 13 disease entries — the avian/reptile/exotic
    mycobacteriosis (avian TB) multi-drug protocols name it explicitly
    ("リファンピシン + エタンブトール 15-30 mg/kg PO q24h × 6-12ヶ月"), and the
    dog/cat tuberculosis complex protocols in Greene list it as a companion
    drug. Five of those references were additionally garbled as
    "エチオブトール" (a non-existent drug name), fixed in the same session.
  - ジヒドロストレプトマイシン (dihydrostreptomycin/streptomycin): 9 disease
    entries — the classic canine brucellosis regimen the formulary's own
    disease pages cite (doxycycline + dihydrostreptomycin 10 mg/kg IM,
    weeks 1-3) had no formulary entry for the aminoglycoside half.

References:
  - Greene CE. Infectious Diseases of the Dog and Cat, 4th ed — canine/feline
    mycobacterial infections (rifampin + isoniazid + ethambutol 15 mg/kg PO
    q24h); canine brucellosis combination therapy.
  - Gunn-Moore DA. J Feline Med Surg 2013 — feline mycobacterial disease
    treatment; MTBC triple therapy and zoonotic handling guidance.
  - Carpenter JW. Exotic Animal Formulary, 6th ed — avian ethambutol
    20-30 mg/kg PO q12-24h in multi-drug mycobacteriosis protocols.
  - Wanke MM. Anim Reprod Sci 2004; Hollett RB. Theriogenology 2006 — canine
    brucellosis: doxycycline + dihydrostreptomycin (10 mg/kg IM) most
    effective published regimen; relapse common, lifelong monitoring.
  - Plumb's Veterinary Drug Handbook, 10th ed — aminoglycoside ototoxicity/
    nephrotoxicity; streptomycin is the most vestibulotoxic aminoglycoside.
"""

DRUGS_BATCH_40: list[dict] = [
    {
        "id": "ethambutol",
        "search_aliases": [
            "エサンブトール",
            "EB",
            "Ethambutol",
        ],
        "name": "Ethambutol",
        "name_ja": "エタンブトール",
        "category": "antibiotics",
        "mechanism": "Inhibits mycobacterial arabinosyl transferases (embB), blocking arabinogalactan synthesis in the mycobacterial cell wall. Bacteriostatic and active only against mycobacteria; always used within multi-drug protocols to prevent resistance.",
        "mechanism_ja": "抗酸菌のアラビノシルトランスフェラーゼ（embB）を阻害し、細胞壁アラビノガラクタン合成を遮断する。静菌的で抗酸菌にのみ有効。耐性化防止のため必ず多剤併用プロトコル内で使用する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "15 mg/kg PO q24h, always combined with rifampin ± isoniazid or a macrolide, for 6-12+ months (M. tuberculosis complex / disseminated mycobacteriosis).",
                "dosage_ja": "15 mg/kg PO q24h。必ずリファンピン±イソニアジドまたはマクロライドと併用し、6-12ヶ月以上（結核菌群/播種性抗酸菌症）。",
                "notes": "M. tuberculosis complex in pets is a zoonotic/public-health issue — consult authorities before treating; euthanasia is often advised for confirmed M. tuberculosis. Monitor liver values monthly.",
                "notes_ja": "ペットの結核菌群感染は人獣共通感染症（公衆衛生上の問題）— 治療前に行政機関へ相談。M. tuberculosis確定例は安楽死が推奨されることも多い。肝酵素を毎月モニタリング。",
            },
            "cat": {
                "safe": True,
                "dosage": "10-25 mg/kg PO q24h (typically 15 mg/kg), within triple therapy (rifampicin + fluoroquinolone/macrolide + ethambutol) for 6+ months.",
                "dosage_ja": "10-25 mg/kg PO q24h（通常15 mg/kg）。3剤併用（リファンピシン＋フルオロキノロン/マクロライド＋エタンブトール）で6ヶ月以上。",
                "notes": "Feline leprosy/NTM often managed with rifampicin + clarithromycin + pradofloxacin instead; ethambutol reserved for MTBC (Gunn-Moore 2013). Zoonotic precautions for owners.",
                "notes_ja": "猫らい/非結核性抗酸菌症はリファンピシン＋クラリスロマイシン＋プラドフロキサシンで管理されることが多く、エタンブトールは結核菌群（MTBC）向け（Gunn-Moore 2013）。飼い主への人獣共通感染症対策を指導。",
            },
            "bird": {
                "safe": True,
                "dosage": "20-30 mg/kg PO q12-24h, within multi-drug protocols (clarithromycin/azithromycin + rifampin/rifabutin + ethambutol) for a minimum of 6 months, often 12+ (avian mycobacteriosis, M. avium/M. genavense).",
                "dosage_ja": "20-30 mg/kg PO q12-24h。多剤併用（クラリスロマイシン/アジスロマイシン＋リファンピン/リファブチン＋エタンブトール）で最低6ヶ月、多くは12ヶ月以上（鳥抗酸菌症、M. avium/M. genavense）。",
                "notes": "Treatment is controversial: M. avium is an opportunistic zoonosis for immunocompromised humans — screen the household before electing therapy. Isolate positive birds from the collection.",
                "notes_ja": "治療の是非は議論あり: M. aviumは免疫不全者への日和見人獣共通感染症 — 治療選択前に同居者のリスクを評価。陽性個体は群から隔離。",
            },
            "reptile": {
                "safe": True,
                "dosage": "15 mg/kg PO q24h (extrapolated), within multi-drug protocols; monitor hepatic values (disseminated granulomatous disease/mycobacteriosis).",
                "dosage_ja": "15 mg/kg PO q24h（外挿値）。多剤併用プロトコル内で使用し、肝数値をモニタリング（播種性肉芽腫性疾患/抗酸菌症）。",
                "notes": "Doses extrapolated from mammals; euthanasia is often recommended for confirmed reptile mycobacteriosis on public-health grounds.",
                "notes_ja": "用量は哺乳類からの外挿。爬虫類の抗酸菌症確定例は公衆衛生上、安楽死が推奨されることも多い。",
            },
        },
        "side_effects": "Dose-dependent optic neuritis/retrobulbar neuritis (well documented in humans — vision changes hard to detect in animals), GI upset, hepatotoxicity, rare peripheral neuropathy",
        "side_effects_ja": "用量依存性の視神経炎・球後視神経炎（ヒトで著明 — 動物では視覚変化の検出が困難）、消化器症状、肝毒性、稀に末梢神経障害",
        "contraindications": "Known optic neuritis; severe hepatic failure; never use as monotherapy (rapid resistance)",
        "contraindications_ja": "既知の視神経炎、重度肝不全。単剤使用は禁止（急速に耐性化）",
        "drug_interactions": "Aluminium-containing antacids reduce absorption (separate by 4 h); additive hepatotoxicity with rifampin/isoniazid — monitor liver values",
        "drug_interactions_ja": "アルミニウム含有制酸薬は吸収を低下（4時間以上あける）。リファンピン/イソニアジドと肝毒性が相加的 — 肝数値モニタリング",
    },
    {
        "id": "dihydrostreptomycin",
        "search_aliases": [
            "ストレプトマイシン",
            "硫酸ストレプトマイシン",
            "Streptomycin",
            "DSM",
        ],
        "name": "Dihydrostreptomycin (Streptomycin)",
        "name_ja": "ジヒドロストレプトマイシン（ストレプトマイシン）",
        "category": "antibiotics",
        "mechanism": "Aminoglycoside binding the 30S ribosomal subunit, causing mistranslation and bactericidal activity against aerobic gram-negatives, Brucella, Leptospira, Francisella (tularemia) and Yersinia pestis (plague). Not absorbed orally; concentration-dependent killing.",
        "mechanism_ja": "アミノグリコシド系。30Sリボソームサブユニットに結合して翻訳エラーを誘発し、好気性グラム陰性菌・ブルセラ・レプトスピラ・野兎病菌・ペスト菌に殺菌的に作用。経口では吸収されない。濃度依存性殺菌。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Brucellosis: 10 mg/kg IM q24h (or divided q12h) during weeks 1-3, combined with doxycycline 5 mg/kg PO q12h × 8+ weeks — the most effective published regimen. Leptospiral carrier state (historical): 10-15 mg/kg IM q24h × 5-7 days.",
                "dosage_ja": "ブルセラ症: 10 mg/kg IM q24h（またはq12h分割）を第1-3週に、ドキシサイクリン5 mg/kg PO q12h×8週以上と併用 — 最も有効性が報告されたレジメン。レプトスピラ保菌状態（歴史的）: 10-15 mg/kg IM q24h×5-7日。",
                "notes": "B. canis is never reliably eradicated — relapse common; neuter, retest q3mo, lifelong monitoring. Zoonotic: counsel owners. Where dihydrostreptomycin is unavailable, gentamicin (5 mg/kg IM/IV q24h weeks 1+4) with doxycycline is the usual substitute.",
                "notes_ja": "B. canisの完全除菌は困難 — 再発が多い。避妊去勢、3ヶ月毎の再検査、生涯モニタリング。人獣共通感染症であり飼い主への指導必須。ジヒドロストレプトマイシン入手不能時はゲンタマイシン（5 mg/kg IM/IV q24h、第1・4週）＋ドキシサイクリンで代替。",
            },
            "cat": {
                "safe": True,
                "dosage": "Rarely indicated; tularemia/plague: 10 mg/kg IM q12h × 7-10 days (gentamicin now preferred).",
                "dosage_ja": "適応は稀。野兎病/ペスト: 10 mg/kg IM q12h×7-10日（現在はゲンタマイシンが優先される）。",
                "notes": "Handle suspected plague/tularemia cats with strict zoonotic precautions.",
                "notes_ja": "ペスト/野兎病疑い猫は厳重な人獣共通感染症対策下で取り扱う。",
            },
            "horse": {
                "safe": True,
                "dosage": "Historical: 10 mg/kg IM q12h with procaine penicillin G ('pen-strep'); largely superseded by gentamicin-based combinations.",
                "dosage_ja": "歴史的: 10 mg/kg IM q12h をプロカインペニシリンGと併用（ペニシリン・ストレプトマイシン合剤）。現在はゲンタマイシン併用にほぼ置き換え。",
                "notes": "Observe regulatory withdrawal rules in food-producing contexts.",
                "notes_ja": "食用供用の可能性がある場合は休薬期間の規制を遵守。",
            },
        },
        "side_effects": "Ototoxicity — streptomycin is the most vestibulotoxic aminoglycoside (ataxia, nystagmus, deafness may be irreversible); nephrotoxicity (monitor urine sediment/creatinine); neuromuscular blockade at high doses",
        "side_effects_ja": "耳毒性 — アミノグリコシドの中で最も前庭毒性が強い（運動失調・眼振・難聴は不可逆のことがある）。腎毒性（尿沈渣・クレアチニンをモニタリング）。高用量で神経筋遮断",
        "contraindications": "Renal failure; pre-existing vestibular/hearing deficits; myasthenia gravis; concurrent other ototoxic/nephrotoxic drugs; pregnancy (fetal ototoxicity)",
        "contraindications_ja": "腎不全、既存の前庭・聴覚障害、重症筋無力症、他の耳毒性・腎毒性薬との併用、妊娠（胎子耳毒性）",
        "drug_interactions": "Additive nephrotoxicity with NSAIDs, amphotericin B, cisplatin; additive neuromuscular blockade with anesthetics/muscle relaxants (atracurium); loop diuretics (furosemide) potentiate ototoxicity",
        "drug_interactions_ja": "NSAIDs・アムホテリシンB・シスプラチンと腎毒性が相加的。麻酔薬・筋弛緩薬（アトラクリウム）と神経筋遮断が相加的。ループ利尿薬（フロセミド）は耳毒性を増強",
    },
]
