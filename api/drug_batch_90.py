"""Drug batch 90 – 2026-10 第82弾.

Pimobendan solution for injection (Vetmedin 0.75 mg/mL solution for injection
for dogs, Boehringer Ingelheim; authorised in the EU/UK). The canine acute
cardiogenic pulmonary-oedema protocol tells the reader to give
"furosemide + pimobendan IV/PO", but the dictionary only carried the oral
monograph, so the single-dose IV regimen (and the hand-over to oral dosing)
could not be looked up. Kept as a separate monograph from oral pimobendan so
the injection dose (0.15 mg/kg once) can never be confused with the oral
maintenance dose (0.25-0.3 mg/kg q12h).
Evidence: Vetmedin 0.75 mg/ml solution for injection for dogs — Summary of
Product Characteristics (UK VMD / EU national authorisation);
Keene BW, Atkins CE, Bonagura JD, et al. ACVIM consensus guidelines for the
diagnosis and treatment of myxomatous mitral valve disease in dogs. J Vet
Intern Med 2019;33:1127-1140; Plumb's Veterinary Drug Handbook 10th ed.
"""

DRUGS_BATCH_90 = [
    {
        "id": "pimobendan_injection",
        # Name stem is deliberately "ピモベンダン注射液" so the bare word
        # 「ピモベンダン」 in oral protocols keeps resolving to the oral monograph.
        "no_component_index": True,
        "search_aliases": [
            "ピモベンダン注射液",
            "ピモベンダン注",
            "ベトメディン注射液",
            "Vetmedin injection",
            "pimobendan injection",
            "pimobendan IV",
        ],
        "name": "Pimobendan Solution for Injection (Vetmedin injection)",
        "name_ja": "ピモベンダン注射液（ベトメディン注射液）",
        "category": "cardiovascular",
        "mechanism": "Inodilator: calcium sensitiser of cardiac troponin C plus phosphodiesterase-III inhibition, increasing contractility and producing arterial and venous vasodilation without raising myocardial oxygen demand as much as catecholamines. The IV formulation gives an immediate onset when oral absorption cannot be relied on (dyspnoeic, vomiting or anorexic dogs).",
        "mechanism_ja": "強心血管拡張薬（イノダイレーター）: 心筋トロポニンCのカルシウム感受性増強とホスホジエステラーゼIII阻害により収縮力を高め、動静脈を拡張する（カテコールアミンほど心筋酸素需要を増やさない）。静注製剤は呼吸困難・嘔吐・食欲廃絶で経口吸収に頼れない犬で即効性を得るために使う。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Initiation of treatment of congestive heart failure (decompensated MMVD/valvular insufficiency or DCM): a SINGLE IV injection of 0.15 mg/kg (= 0.2 mL/kg of the 0.75 mg/mL solution). Continue with ORAL pimobendan 0.25 mg/kg q12h, the first oral dose 12 hours after the injection (product SPC). Give together with furosemide and oxygen for acute pulmonary oedema (ACVIM 2019 stage C).",
                "dosage_ja": "うっ血性心不全の治療開始（非代償性の僧帽弁閉鎖不全症・弁膜疾患または拡張型心筋症）: 0.15 mg/kg を1回のみ静注（0.75 mg/mL 液で 0.2 mL/kg）。12時間後から経口ピモベンダン 0.25 mg/kg q12h に切り替えて継続する（添付文書）。急性肺水腫ではフロセミド・酸素と併用する（ACVIM 2019 ステージC）。",
                "notes": "Single dose only — the injection is NOT a substitute for repeated IV dosing; maintenance is oral. Do not confuse the injection dose (0.15 mg/kg once) with the oral dose (0.25-0.3 mg/kg q12h). Monitor heart rate/rhythm and blood pressure after injection (vasodilation can cause hypotension, PDE-III inhibition can increase ventricular ectopy). Authorised in the EU/UK; not marketed in Japan or the USA — in those markets the oral product is used (via nasogastric tube if needed).",
                "notes_ja": "単回投与のみ — 反復静注の代わりではなく、維持は経口で行う。注射用量（0.15 mg/kg 単回）と経口用量（0.25-0.3 mg/kg q12h）を混同しないこと。投与後は心拍数・調律・血圧を監視する（血管拡張による低血圧、PDE-III阻害による心室性期外収縮の増加の可能性）。EU・英国で承認。日本・米国では未発売のため、経口製剤（必要なら経鼻胃チューブ）を用いる。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not authorised for cats — no validated injectable dose. Oral pimobendan is used off-label in cats only after LVOT obstruction has been excluded by echocardiography.",
                "dosage_ja": "猫には承認されておらず、検証された注射用量はない。猫では心エコーで左室流出路閉塞を除外したうえで経口ピモベンダンを適応外使用する。",
                "notes": "Avoid in obstructive hypertrophic cardiomyopathy (HOCM).",
                "notes_ja": "閉塞性肥大型心筋症（HOCM）では使用を避ける。",
            },
        },
        "contraindications": "Hypertrophic cardiomyopathy; conditions in which an increase in cardiac output is not possible for functional or anatomical reasons (e.g. aortic or pulmonic stenosis). Not for repeated dosing.",
        "contraindications_ja": "肥大型心筋症。機能的・解剖学的理由で心拍出量の増加が見込めない病態（大動脈弁狭窄・肺動脈弁狭窄など）。反復投与には使わない。",
        "side_effects": [
            "Transient increase in heart rate",
            "Hypotension (vasodilation)",
            "Ventricular arrhythmias (PDE-III inhibition)",
            "Vomiting",
        ],
        "side_effects_ja": [
            "一過性の心拍数増加",
            "低血圧（血管拡張）",
            "心室性不整脈（PDE-III阻害）",
            "嘔吐",
        ],
        "drug_interactions": [
            {
                "drug": "Pimobendan",
                "effect": "Same active substance — the injection starts therapy and oral pimobendan continues it 12 hours later; do not give both at full dose at the same time.",
                "effect_ja": "同一成分 — 注射で治療を開始し12時間後から経口ピモベンダンで継続する。同時に両方を全量投与しない。",
                "severity": "major",
            },
            {
                "drug": "Verapamil",
                "effect": "Calcium-channel blockers can blunt the positive inotropic effect.",
                "effect_ja": "カルシウム拮抗薬は陽性変力作用を減弱させうる。",
                "severity": "moderate",
            },
            {
                "drug": "Atenolol",
                "effect": "Beta-blockers can blunt the positive inotropic effect.",
                "effect_ja": "β遮断薬は陽性変力作用を減弱させうる。",
                "severity": "moderate",
            },
        ],
        "references": [
            "Vetmedin 0.75 mg/ml solution for injection for dogs — Summary of Product Characteristics (Boehringer Ingelheim; UK VMD / EU national authorisation).",
            "Keene BW, Atkins CE, Bonagura JD, et al. ACVIM consensus guidelines for the diagnosis and treatment of myxomatous mitral valve disease in dogs. J Vet Intern Med 2019;33:1127-1140.",
            "Budde JA, McCluskey DM, eds. Plumb's Veterinary Drug Handbook. 10th ed. Wiley-Blackwell; 2023.",
        ],
    },
]
