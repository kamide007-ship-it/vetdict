"""Drug batch 9 – ISCAID guideline antimicrobials for urinary tract infections.

Adds 7 antimicrobials from the ISCAID 2019 guidelines (Weese et al.,
The Veterinary Journal 247: 8-25) that were missing from the database.
Also incorporates ADR data from Minouchi et al. (2024, Jpn J Vet Dermatol
30(1): 9-14) for fosfomycin.

WHO antimicrobial classification:
  CIA  = Critically Important Antimicrobial
  HP-CIA = Highest Priority CIA
  HIA  = Highly Important Antimicrobial

References:
  - Weese et al. 2019. ISCAID guidelines for bacterial UTI. Vet J 247: 8-25
  - Minouchi et al. 2024. ADR to CEX, MINO, FOM. Jpn J Vet Dermatol 30: 9-14
  - Plumb's Veterinary Drug Handbook, 10th ed.
  - BSAVA Small Animal Formulary, 10th ed.
"""

from __future__ import annotations

DRUGS_BATCH_9: list[dict] = [
    # ------------------------------------------------------------------
    # Fosfomycin (CIA) — WHO Critically Important Antimicrobial
    # ------------------------------------------------------------------
    {
        "id": "fosfomycin",
        "name": "Fosfomycin (Fosmicin)",
        "name_ja": "ホスホマイシン（ホスミシン）",
        "category": "antibiotics",
        "mechanism": "Phosphonic acid derivative that inhibits MurA (UDP-N-acetylglucosamine enolpyruvyl transferase), blocking the first step of peptidoglycan synthesis. Bactericidal. Broad-spectrum activity against Gram-positive and Gram-negative bacteria including ESBL-producing and multidrug-resistant strains.",
        "mechanism_ja": "ホスホン酸誘導体。MurA（UDP-N-アセチルグルコサミンエノールピルビルトランスフェラーゼ）を阻害し、ペプチドグリカン合成の最初のステップを遮断する殺菌性抗菌薬。ESBL産生菌・多剤耐性菌を含むグラム陽性菌・グラム陰性菌に広域スペクトル活性。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "UTI: 40 mg/kg PO q12h (with food); Pyelonephritis/Prostatitis: 40 mg/kg PO q8h; Pyoderma: 20 mg/kg PO q12h",
                "dosage_ja": "尿路感染症: 40 mg/kg 経口 12時間ごと（食事とともに）; 腎盂腎炎/前立腺炎: 40 mg/kg 経口 8時間ごと; 膿皮症: 20 mg/kg 経口 12時間ごと",
                "notes": "WHO CIA classification — reserve for multidrug-resistant infections only. ADR rate 16.3% (Minouchi 2024): diarrhea/soft stool 86.7%, vomiting 26.7%, anorexia 3.3%. 75% of ADRs occur within 1 week. All ADRs resolved after discontinuation. Administer with food to improve absorption. Effective against ESBL-producing E. coli and MRSP. For pyelonephritis/prostatitis, use q8h dosing.",
                "notes_ja": "WHO CIA分類 — 多剤耐性感染症にのみ使用すること。副作用発現率16.3%（箕内ら 2024）: 軟便・下痢86.7%、嘔吐26.7%、食欲不振3.3%。副作用の75%は1週間以内に発現。全例で休薬後に軽快。食事とともに投与し吸収を改善。ESBL産生大腸菌・MRSPに有効。腎盂腎炎/前立腺炎には8時間ごと投与。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not recommended",
                "dosage_ja": "推奨されない",
                "notes": "ISCAID 2019 guidelines: Do not use in cats. Insufficient safety and efficacy data in feline species.",
                "notes_ja": "ISCAID 2019ガイドライン: 猫には使用しないこと。猫における安全性・有効性データが不十分。",
            },
        },
        "side_effects": [
            "Diarrhea/soft stool (86.7% of ADR cases)",
            "Vomiting (26.7%)",
            "Anorexia (3.3%)",
        ],
        "side_effects_ja": [
            "軟便・下痢（副作用発現例の86.7%）",
            "嘔吐（26.7%）",
            "食欲不振（3.3%）",
        ],
        "contraindications": "Do not use in cats. Reserve for multidrug-resistant infections (WHO CIA). Not a first-line agent for routine UTI or pyoderma.",
        "contraindications_ja": "猫には使用不可。多剤耐性感染症に限定使用（WHO CIA）。通常の尿路感染症・膿皮症の第一選択薬ではない。",
    },
    # ------------------------------------------------------------------
    # Meropenem (CIA) — Carbapenem
    # ------------------------------------------------------------------
    {
        "id": "meropenem",
        "name": "Meropenem",
        "name_ja": "メロペネム",
        "category": "antibiotics",
        "mechanism": "Carbapenem beta-lactam antibiotic. Binds PBPs to inhibit cell wall synthesis. Ultra-broad spectrum: Gram-positive, Gram-negative (including ESBL-producing Enterobacteriaceae and Pseudomonas), and anaerobes. Resistant to most beta-lactamases.",
        "mechanism_ja": "カルバペネム系βラクタム抗菌薬。PBPに結合し細胞壁合成を阻害。超広域スペクトル: グラム陽性菌、グラム陰性菌（ESBL産生腸内細菌科・緑膿菌含む）、嫌気性菌。ほとんどのβラクタマーゼに安定。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "8.5 mg/kg SC q12h or IV q8h",
                "dosage_ja": "8.5 mg/kg 皮下 12時間ごと または 静注 8時間ごと",
                "notes": "Reserve for multidrug-resistant infections, especially ESBL-producing Enterobacteriaceae or Pseudomonas. Consult veterinary infectious disease specialist before use. Enterococcus faecium is inherently resistant.",
                "notes_ja": "多剤耐性菌感染症、特にESBL産生腸内細菌科・緑膿菌に限定。使用前に獣医感染症専門家に相談推奨。Enterococcus faeciumは本来耐性。",
            },
            "cat": {
                "safe": True,
                "dosage": "10 mg/kg IV/SC/IM q12h",
                "dosage_ja": "10 mg/kg 静注/皮下/筋注 12時間ごと",
                "notes": "Same indications as dogs. Reserve for confirmed multidrug-resistant infections only.",
                "notes_ja": "犬と同じ適応。確認された多剤耐性感染症にのみ使用。",
            },
        },
        "side_effects": [
            "Diarrhea",
            "Vomiting",
            "Pain at injection site (SC/IM)",
            "Seizures (rare, high doses or renal impairment)",
        ],
        "side_effects_ja": [
            "下痢",
            "嘔吐",
            "注射部位疼痛（皮下/筋注）",
            "痙攣（稀、高用量または腎機能障害時）",
        ],
        "contraindications": "Hypersensitivity to carbapenems or beta-lactams. Use with caution in renal impairment (dose adjust). WHO CIA — absolute last resort antimicrobial.",
        "contraindications_ja": "カルバペネム系・βラクタム系過敏症。腎機能障害時は用量調整が必要。WHO CIA — 最終手段の抗菌薬。",
    },
    # ------------------------------------------------------------------
    # Imipenem-Cilastatin (CIA) — Carbapenem
    # ------------------------------------------------------------------
    {
        "id": "imipenem_cilastatin",
        "name": "Imipenem-Cilastatin",
        "name_ja": "イミペネム・シラスタチン",
        "category": "antibiotics",
        "mechanism": "Carbapenem beta-lactam combined with cilastatin (renal dehydropeptidase-I inhibitor to prevent renal metabolism of imipenem). Ultra-broad spectrum including ESBL-producing organisms and Pseudomonas.",
        "mechanism_ja": "カルバペネム系βラクタム＋シラスタチン（腎デヒドロペプチダーゼI阻害薬、イミペネムの腎代謝を防止）。ESBL産生菌・緑膿菌を含む超広域スペクトル。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5 mg/kg IV/IM q6-8h",
                "dosage_ja": "5 mg/kg 静注/筋注 6-8時間ごと",
                "notes": "Reserve for multidrug-resistant infections, especially ESBL-producing Enterobacteriaceae or Pseudomonas. Consult veterinary infectious disease specialist before use. E. faecium is inherently resistant. IV infusion should be given slowly over 20-30 min.",
                "notes_ja": "多剤耐性菌感染症に限定。使用前に獣医感染症専門家に相談推奨。E. faeciumは本来耐性。静注は20-30分かけてゆっくり投与。",
            },
            "cat": {
                "safe": True,
                "dosage": "5 mg/kg IV/IM q6-8h",
                "dosage_ja": "5 mg/kg 静注/筋注 6-8時間ごと",
                "notes": "Same indications as dogs. Last-resort antimicrobial for confirmed MDR infections.",
                "notes_ja": "犬と同じ適応。確認された多剤耐性感染症の最終手段。",
            },
        },
        "side_effects": [
            "Nausea/vomiting (rapid IV infusion)",
            "Diarrhea",
            "Seizures (especially in renal impairment or CNS disease)",
            "Pain at IM injection site",
            "Thrombophlebitis (IV)",
        ],
        "side_effects_ja": [
            "悪心・嘔吐（急速静注時）",
            "下痢",
            "痙攣（特に腎機能障害・CNS疾患時）",
            "筋注部位疼痛",
            "血栓性静脈炎（静注）",
        ],
        "contraindications": "Hypersensitivity to carbapenems or beta-lactams. CNS disorders (increased seizure risk). Dose adjust in renal impairment. WHO CIA — absolute last resort.",
        "contraindications_ja": "カルバペネム系・βラクタム系過敏症。CNS障害（痙攣リスク増加）。腎機能障害時は用量調整。WHO CIA — 最終手段。",
    },
    # ------------------------------------------------------------------
    # Cefpodoxime Proxetil (HP-CIA) — 3rd gen Cephalosporin
    # ------------------------------------------------------------------
    {
        "id": "cefpodoxime",
        "name": "Cefpodoxime Proxetil",
        "name_ja": "セフポドキシムプロキセチル",
        "category": "antibiotics",
        "mechanism": "Third-generation oral cephalosporin (prodrug). Inhibits cell wall synthesis by binding PBP. Broader Gram-negative activity than first-gen cephalosporins (cephalexin). Resistant to many beta-lactamases.",
        "mechanism_ja": "第3世代経口セファロスポリン（プロドラッグ）。PBPに結合し細胞壁合成を阻害。第1世代（セファレキシン）より広いグラム陰性菌活性。多くのβラクタマーゼに安定。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q24h",
                "dosage_ja": "5-10 mg/kg 経口 24時間ごと",
                "notes": "HP-CIA classification. Higher activity against Enterobacteriaceae than cephalexin using the 2 mcg/mL breakpoint. Enterococcus spp. are resistant. Approved for canine skin infections in some regions.",
                "notes_ja": "HP-CIA分類。2 μg/mLブレイクポイント使用時、セファレキシンより腸内細菌科に対する活性が高い。エンテロコッカス属は耐性。一部地域で犬の皮膚感染症に承認。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not established",
                "dosage_ja": "用量未確立",
                "notes": "Feline dosing not established per ISCAID 2019 guidelines.",
                "notes_ja": "ISCAID 2019ガイドラインでは猫の用量は確立されていない。",
            },
        },
        "side_effects": [
            "Diarrhea",
            "Vomiting",
            "Decreased appetite",
        ],
        "side_effects_ja": [
            "下痢",
            "嘔吐",
            "食欲低下",
        ],
        "contraindications": "Hypersensitivity to cephalosporins or penicillins. HP-CIA — not first-line for routine infections where narrower-spectrum agents are effective.",
        "contraindications_ja": "セファロスポリン系・ペニシリン系過敏症。HP-CIA — 狭域スペクトル薬が有効な通常感染症の第一選択薬ではない。",
    },
    # ------------------------------------------------------------------
    # Orbifloxacin (HP-CIA) — Veterinary Fluoroquinolone
    # ------------------------------------------------------------------
    {
        "id": "orbifloxacin",
        "name": "Orbifloxacin",
        "name_ja": "オルビフロキサシン",
        "category": "antibiotics",
        "mechanism": "Third-generation veterinary fluoroquinolone. Inhibits DNA gyrase (topoisomerase II) and topoisomerase IV. Bactericidal, concentration-dependent killing. Primarily excreted in active form in urine.",
        "mechanism_ja": "第3世代動物用フルオロキノロン。DNAジャイレース（トポイソメラーゼII）およびトポイソメラーゼIVを阻害。殺菌性、濃度依存性。主に活性型のまま尿中排泄。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2.5-7.5 mg/kg PO q24h",
                "dosage_ja": "2.5-7.5 mg/kg 経口 24時間ごと",
                "notes": "HP-CIA. First-line for pyelonephritis. First-choice for prostate-involving infections due to good prostatic penetration. Not recommended for Enterococcus spp. Reserve for documented resistant infections or as empirical choice for pyelonephritis/prostatitis.",
                "notes_ja": "HP-CIA。腎盂腎炎の第一選択薬。良好な前立腺移行性のため前立腺感染症の第一選択。エンテロコッカス属には推奨されない。記録された耐性感染症または腎盂腎炎/前立腺炎の経験的選択に限定。",
            },
            "cat": {
                "safe": True,
                "dosage": "7.5 mg/kg PO q24h (suspension)",
                "dosage_ja": "7.5 mg/kg 経口 24時間ごと（懸濁液）",
                "notes": "Use with caution in cats. Monitor for retinopathy. Avoid doses exceeding recommended range.",
                "notes_ja": "猫では慎重に使用。網膜症に注意。推奨用量範囲を超えないこと。",
            },
        },
        "side_effects": [
            "GI upset (vomiting, diarrhea)",
            "CNS effects (rare: seizures in predisposed animals)",
            "Retinopathy (cats — dose-dependent)",
            "Cartilage damage in growing animals",
        ],
        "side_effects_ja": [
            "消化器症状（嘔吐、下痢）",
            "CNS症状（稀: 素因のある動物で痙攣）",
            "網膜症（猫 — 用量依存性）",
            "成長期動物の軟骨障害",
        ],
        "contraindications": "Growing animals (cartilage damage). Known seizure disorders. HP-CIA — reserve for documented resistant infections. Not for Enterococcus.",
        "contraindications_ja": "成長期動物（軟骨障害）。既知の痙攣性障害。HP-CIA — 記録された耐性感染症に限定。エンテロコッカスには無効。",
    },
    # ------------------------------------------------------------------
    # Levofloxacin (HP-CIA) — Human Fluoroquinolone
    # ------------------------------------------------------------------
    {
        "id": "levofloxacin",
        "name": "Levofloxacin",
        "name_ja": "レボフロキサシン",
        "category": "antibiotics",
        "mechanism": "Third-generation fluoroquinolone (L-isomer of ofloxacin). Inhibits DNA gyrase and topoisomerase IV. Bactericidal with concentration-dependent killing. Good oral bioavailability in dogs.",
        "mechanism_ja": "第3世代フルオロキノロン（オフロキサシンのL-異性体）。DNAジャイレースおよびトポイソメラーゼIVを阻害。濃度依存性の殺菌作用。犬では良好な経口バイオアベイラビリティ。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "25 mg/kg PO q24h",
                "dosage_ja": "25 mg/kg 経口 24時間ごと",
                "notes": "HP-CIA. Sometimes used as cheaper fluoroquinolone alternative. Approved veterinary fluoroquinolones (enrofloxacin, marbofloxacin, pradofloxacin) should be used preferentially when available. Good oral bioavailability in dogs.",
                "notes_ja": "HP-CIA。安価なフルオロキノロン代替として使用されることがある。承認済み動物用フルオロキノロン（エンロフロキサシン、マルボフロキサシン、プラドフロキサシン）を優先的に使用すべき。犬では良好な経口バイオアベイラビリティ。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not established",
                "dosage_ja": "用量未確立",
                "notes": "Feline dosing not established. Risk of retinal toxicity. Use approved veterinary fluoroquinolones instead.",
                "notes_ja": "猫の用量未確立。網膜毒性のリスク。承認済み動物用フルオロキノロンを使用すること。",
            },
        },
        "side_effects": [
            "GI upset (vomiting, diarrhea)",
            "CNS effects (dizziness, seizures — rare)",
            "Cartilage damage in growing animals",
            "Retinopathy (cats)",
        ],
        "side_effects_ja": [
            "消化器症状（嘔吐、下痢）",
            "CNS症状（めまい、痙攣 — 稀）",
            "成長期動物の軟骨障害",
            "網膜症（猫）",
        ],
        "contraindications": "Growing animals. Seizure disorders. Cats (retinal toxicity risk). HP-CIA — prefer approved veterinary fluoroquinolones.",
        "contraindications_ja": "成長期動物。痙攣性障害。猫（網膜毒性リスク）。HP-CIA — 承認済み動物用フルオロキノロンを優先。",
    },
    # ------------------------------------------------------------------
    # Ciprofloxacin (HP-CIA) — Human Fluoroquinolone
    # ------------------------------------------------------------------
    {
        "id": "ciprofloxacin",
        "name": "Ciprofloxacin",
        "name_ja": "シプロフロキサシン",
        "category": "antibiotics",
        "mechanism": "Second-generation fluoroquinolone. Inhibits DNA gyrase and topoisomerase IV. Bactericidal. Lower and more variable oral bioavailability in dogs than approved veterinary fluoroquinolones.",
        "mechanism_ja": "第2世代フルオロキノロン。DNAジャイレースおよびトポイソメラーゼIVを阻害。殺菌性。犬では承認済み動物用フルオロキノロンより経口バイオアベイラビリティが低くばらつきがある。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "25-30 mg/kg PO q24h",
                "dosage_ja": "25-30 mg/kg 経口 24時間ごと",
                "notes": "HP-CIA. Sometimes used as cheaper fluoroquinolone. Lower oral bioavailability than approved veterinary fluoroquinolones — use of approved drugs (enrofloxacin, marbofloxacin) is difficult to justify bypassing. CLSI recommends not using human breakpoints for canine isolates. Not recommended for prostatitis. Dosage recommendations are empirical and based on limited PK studies.",
                "notes_ja": "HP-CIA。安価なフルオロキノロンとして使用されることがある。承認済み動物用フルオロキノロンより経口バイオアベイラビリティが低い。CLSIは犬分離株にヒトのブレイクポイントを使用しないよう推奨。前立腺炎には推奨されない。投与推奨は経験的・限られたPK研究に基づく。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not recommended",
                "dosage_ja": "推奨されない",
                "notes": "Erratic oral absorption. Risk of retinal toxicity. Use approved veterinary fluoroquinolones.",
                "notes_ja": "経口吸収が不安定。網膜毒性のリスク。承認済み動物用フルオロキノロンを使用。",
            },
        },
        "side_effects": [
            "GI upset (vomiting, diarrhea, anorexia)",
            "CNS effects (rare: seizures, tremors)",
            "Cartilage damage in growing animals",
            "Crystalluria (alkaline urine)",
        ],
        "side_effects_ja": [
            "消化器症状（嘔吐、下痢、食欲不振）",
            "CNS症状（稀: 痙攣、振戦）",
            "成長期動物の軟骨障害",
            "結晶尿（アルカリ尿）",
        ],
        "contraindications": "Growing animals. Seizure disorders. Cats. HP-CIA — approved veterinary fluoroquinolones should be used preferentially. Not for prostatitis.",
        "contraindications_ja": "成長期動物。痙攣性障害。猫。HP-CIA — 承認済み動物用フルオロキノロンを優先使用。前立腺炎には不可。",
    },
    # ------------------------------------------------------------------
    # Minocycline (HIA) — Tetracycline for MRSP pyoderma
    # ------------------------------------------------------------------
    {
        "id": "minocycline",
        "name": "Minocycline",
        "name_ja": "ミノサイクリン",
        "category": "antibiotics",
        "mechanism": "Second-generation tetracycline. Binds 30S ribosomal subunit to inhibit protein synthesis. Bacteriostatic. More lipophilic than doxycycline — better tissue penetration including skin and prostate. Active against many MRSP (methicillin-resistant Staphylococcus pseudintermedius) strains.",
        "mechanism_ja": "第2世代テトラサイクリン。30Sリボソームサブユニットに結合しタンパク質合成を阻害。静菌性。ドキシサイクリンより脂溶性が高く、皮膚・前立腺への組織移行性が良好。多くのMRSP（メチシリン耐性スタフィロコッカス・シュードインターメディウス）株に有効。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Pyoderma: 5-10 mg/kg PO q12h; PK-PD optimal: 5 mg/kg PO q12h with food",
                "dosage_ja": "膿皮症: 5-10 mg/kg 経口 12時間ごと; PK-PD最適: 5 mg/kg 経口 12時間ごと 食事とともに",
                "notes": "Important for MRSP pyoderma treatment. ADR rate 21.0% (Minouchi 2024): vomiting 66.7%, soft stool/diarrhea 33.3%, anorexia 28.6%. Give with food to improve absorption and reduce GI upset. PK-PD data supports 5 mg/kg q12h (Maaland 2014). Higher oral bioavailability than doxycycline in dogs. Not high-concentration urinary excretion — not ideal for UTI.",
                "notes_ja": "MRSP膿皮症治療に重要。副作用発現率21.0%（箕内ら 2024）: 嘔吐66.7%、軟便・下痢33.3%、食欲不振28.6%。食事とともに投与し吸収改善・消化器症状軽減。PK-PDデータは5 mg/kg 12時間ごとを支持（Maaland 2014）。犬ではドキシサイクリンより経口バイオアベイラビリティが高い。高濃度で尿中排泄されないためUTIには不向き。",
            },
            "cat": {
                "safe": True,
                "dosage": "5-12.5 mg/kg PO q12h",
                "dosage_ja": "5-12.5 mg/kg 経口 12時間ごと",
                "notes": "Less esophageal stricture risk than doxycycline. Give with food. Limited feline-specific PK data.",
                "notes_ja": "ドキシサイクリンより食道狭窄リスクが低い。食事とともに投与。猫特異的PKデータは限定的。",
            },
        },
        "side_effects": [
            "Vomiting (66.7% of ADR cases — Minouchi 2024)",
            "Soft stool/diarrhea (33.3%)",
            "Anorexia (28.6%)",
            "Vestibular signs (rare)",
            "Tooth discoloration (young animals)",
        ],
        "side_effects_ja": [
            "嘔吐（副作用発現例の66.7% — 箕内ら 2024）",
            "軟便・下痢（33.3%）",
            "食欲不振（28.6%）",
            "前庭症状（稀）",
            "歯の変色（幼若動物）",
        ],
        "contraindications": "Pregnancy (teratogenic). Growing animals (tooth/bone discoloration). Hepatic insufficiency. Known tetracycline hypersensitivity.",
        "contraindications_ja": "妊娠（催奇形性）。成長期動物（歯・骨の変色）。肝機能不全。テトラサイクリン過敏症。",
    },
]

# ---------------------------------------------------------------------------
# UTI-specific notes patch for existing drugs (ISCAID 2019 Table 3)
# Appends UTI indication/dosing info to existing notes fields.
# ---------------------------------------------------------------------------
ISCAID_UTI_NOTES_PATCH: dict[str, dict[str, dict[str, str]]] = {
    "amoxicillin": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] First-line for sporadic bacterial cystitis. 11-15 mg/kg PO q8-12h. Primarily excreted in active form in urine. Klebsiella spp. are resistant. Not recommended for pyelonephritis or prostatitis. Treatment duration: 3-5 days.",
            "notes_ja_append": " [UTI/ISCAID 2019] 散発性細菌性膀胱炎の第一選択薬。11-15 mg/kg 経口 8-12時間ごと。主に活性型のまま尿中排泄。クレブシエラ属は耐性。腎盂腎炎・前立腺炎には推奨されない。治療期間: 3-5日。",
        },
        "cat": {
            "notes_append": " [UTI/ISCAID 2019] First-line when bacterial cystitis is confirmed by culture. Same dosing as dogs. Note: most cats with LUTS do NOT have bacterial cystitis (FIC is more common).",
            "notes_ja_append": " [UTI/ISCAID 2019] 細菌培養で膀胱炎が確認された場合の第一選択薬。犬と同じ用量。注意: LUTS猫の大多数は細菌性膀胱炎ではない（FICがより一般的）。",
        },
    },
    "amoxicillin_clavulanate": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] 12.5-25 mg/kg PO q12h (total product dose). Use when plain amoxicillin is unavailable or local susceptibility data shows high amoxicillin resistance with preserved amox/clav susceptibility. Not recommended for pyelonephritis or prostatitis.",
            "notes_ja_append": " [UTI/ISCAID 2019] 12.5-25 mg/kg 経口 12時間ごと（総製品用量）。アモキシシリン単剤が入手困難な場合、または地域の感受性データでアモキシシリン耐性率が高くアモキシシリン/クラブラン酸感受性が高い場合に使用。腎盂腎炎・前立腺炎には推奨されない。",
        },
        "cat": {
            "notes_append": " [UTI/ISCAID 2019] Same indications as amoxicillin for confirmed bacterial cystitis. Await culture results before initiating antibiotics in cats with LUTS.",
            "notes_ja_append": " [UTI/ISCAID 2019] 確認された細菌性膀胱炎にはアモキシシリンと同じ適応。LUTS猫では培養結果を待ってから抗菌薬開始。",
        },
    },
    "amikacin": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] 15-30 mg/kg IV/IM/SC q24h. Reserve for MDR infections. Potentially nephrotoxic — avoid in renal impairment. Caution with concurrent nephrotoxic drugs (NSAIDs). Low pH may reduce aminoglycoside activity.",
            "notes_ja_append": " [UTI/ISCAID 2019] 15-30 mg/kg IV/IM/SC 24時間ごと。多剤耐性感染症に限定。腎毒性の可能性 — 腎機能障害では避ける。腎毒性薬（NSAIDs等）との併用注意。低pHはアミノグリコシド活性を低下させうる。",
        },
        "cat": {
            "notes_append": " [UTI/ISCAID 2019] 10-14 mg/kg IV/IM/SC q24h. Same MDR-only indications. Cats more sensitive to nephrotoxicity.",
            "notes_ja_append": " [UTI/ISCAID 2019] 10-14 mg/kg IV/IM/SC 24時間ごと。多剤耐性感染症のみ。猫は腎毒性に対してより感受性が高い。",
        },
    },
    "cephalexin": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] 12-25 mg/kg PO q12h. Narrow activity spectrum. Enterococcus spp. are resistant. CLSI revised breakpoint to <16 mcg/mL (consistent with human medicine). [Pyoderma ADR/Minouchi 2024] ADR rate 8.5% (13/153 dogs): soft stool/diarrhea 53.8%, vomiting 46.2%, anorexia 7.7%. Lowest ADR rate among cephalexin, minocycline, fosfomycin.",
            "notes_ja_append": " [UTI/ISCAID 2019] 12-25 mg/kg 経口 12時間ごと。活性スペクトルは狭い。エンテロコッカス属は耐性。CLSIブレイクポイント16 μg/mL未満に修正。[膿皮症ADR/箕内ら 2024] 副作用発現率8.5%（13/153頭）: 軟便・下痢53.8%、嘔吐46.2%、食欲不振7.7%。CEX/MINO/FOM中最低の副作用率。",
        },
        "cat": {
            "notes_append": " [UTI/ISCAID 2019] Same dosing as dogs. For confirmed bacterial cystitis only.",
            "notes_ja_append": " [UTI/ISCAID 2019] 犬と同じ用量。確認された細菌性膀胱炎にのみ。",
        },
    },
    "cefovecin": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] 8 mg/kg SC single injection; may repeat once at 7-14 days. NOT recommended for routine use — duration and spectrum exceed typical needs. Use only when oral treatment is impossible. Enterococcus spp. are resistant. PK supports 14-day duration in dogs.",
            "notes_ja_append": " [UTI/ISCAID 2019] 8 mg/kg 皮下 単回注射; 7-14日後に1回反復可。常用は推奨されない — 持続時間・スペクトルが通常必要以上。経口投与不可能な場合のみ使用。エンテロコッカス属は耐性。犬でPKは14日間の投与期間を支持。",
        },
        "cat": {
            "notes_append": " [UTI/ISCAID 2019] Same dose as dogs. PK supports 21-day duration in cats. Reserve for situations where oral dosing is not possible.",
            "notes_ja_append": " [UTI/ISCAID 2019] 犬と同じ用量。猫のPKは21日間の投与期間を支持。経口投与不可能な場合に限定。",
        },
    },
    "ceftiofur": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] 2 mg/kg SC q12-24h. Approved for canine bacterial cystitis in some regions. Enterococcus spp. are resistant. HP-CIA classification.",
            "notes_ja_append": " [UTI/ISCAID 2019] 2 mg/kg 皮下 12-24時間ごと。一部地域で犬の細菌性膀胱炎に承認。エンテロコッカス属は耐性。HP-CIA分類。",
        },
    },
    "chloramphenicol": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] 40-50 mg/kg PO q8h. Reserve for MDR infections with no other options. Not first-line for pyelonephritis or prostatitis.",
            "notes_ja_append": " [UTI/ISCAID 2019] 40-50 mg/kg 経口 8時間ごと。他に選択肢がない多剤耐性感染症にのみ。腎盂腎炎・前立腺炎の第一選択ではない。",
        },
        "cat": {
            "notes_append": " [UTI/ISCAID 2019] 12.5-20 mg/kg PO q12h (max 50 mg/cat). Bone marrow suppression risk with prolonged use (>28 days). Idiosyncratic aplastic anemia risk to humans — avoid contact.",
            "notes_ja_append": " [UTI/ISCAID 2019] 12.5-20 mg/kg 経口 12時間ごと（最大50 mg/猫）。長期使用（28日超）で骨髄抑制リスク。ヒトへの特異体質性再生不良性貧血リスク — 接触を避ける。",
        },
    },
    "doxycycline": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] 5 mg/kg PO q12h. Not excreted in high concentrations in urine, but may reach effective levels against some pathogens. Reserve for infections where pathogens are resistant to drugs excreted in active form in urine.",
            "notes_ja_append": " [UTI/ISCAID 2019] 5 mg/kg 経口 12時間ごと。高濃度で尿中排泄されないが、一部の病原菌に対する有効濃度に達することがある。活性型のまま尿中排泄される薬剤に耐性の病原体による感染症に限定。",
        },
        "cat": {
            "notes_append": " [UTI/ISCAID 2019] Same dosing as dogs. Esophageal ulcer risk — follow dosing recommendations carefully (give with food/water, avoid dry pilling).",
            "notes_ja_append": " [UTI/ISCAID 2019] 犬と同じ用量。食道潰瘍リスク — 投与方法に注意（食事/水とともに、乾燥投与を避ける）。",
        },
    },
    "enrofloxacin": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] 5-20 mg/kg PO q24h. Primarily excreted in active form in urine. Reserve for documented resistant infections. First-line empirical choice for pyelonephritis and prostatitis (upper dose range). Not recommended for Enterococcus spp.",
            "notes_ja_append": " [UTI/ISCAID 2019] 5-20 mg/kg 経口 24時間ごと。主に活性型のまま尿中排泄。記録された耐性感染症に限定。腎盂腎炎・前立腺炎の経験的第一選択（高用量域）。エンテロコッカス属には推奨されない。",
        },
        "cat": {
            "notes_append": " [UTI/ISCAID 2019] 5 mg/kg PO q24h MAXIMUM. Retinopathy risk — avoid if possible. Use alternative fluoroquinolones or non-fluoroquinolone agents preferentially.",
            "notes_ja_append": " [UTI/ISCAID 2019] 5 mg/kg 経口 24時間ごと 最大。網膜症リスク — 可能なら避ける。代替フルオロキノロンまたは非フルオロキノロン薬を優先使用。",
        },
    },
    "marbofloxacin": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] 2.7-5.5 mg/kg PO q24h. Primarily excreted in active form in urine. First-line for pyelonephritis. First-choice for prostate-involving infections (excellent prostatic penetration). Not recommended for Enterococcus spp. HP-CIA classification.",
            "notes_ja_append": " [UTI/ISCAID 2019] 2.7-5.5 mg/kg 経口 24時間ごと。主に活性型のまま尿中排泄。腎盂腎炎の第一選択薬。前立腺感染症の第一選択（優れた前立腺移行性）。エンテロコッカス属には推奨されない。HP-CIA分類。",
        },
        "cat": {
            "notes_append": " [UTI/ISCAID 2019] Same dosing as dogs. Monitor for retinopathy (fluoroquinolone class effect in cats).",
            "notes_ja_append": " [UTI/ISCAID 2019] 犬と同じ用量。網膜症に注意（猫のフルオロキノロンクラスエフェクト）。",
        },
    },
    "pradofloxacin": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] 3-5 mg/kg PO q24h. Evidence-based for canine bacterial cystitis. Higher activity against some bacteria than conventional fluoroquinolones (enrofloxacin, marbofloxacin). Excellent first-line for pyelonephritis, especially in cats. Not for Enterococcus.",
            "notes_ja_append": " [UTI/ISCAID 2019] 3-5 mg/kg 経口 24時間ごと。犬の細菌性膀胱炎にエビデンスあり。従来のフルオロキノロン（エンロフロキサシン、マルボフロキサシン）より一部の細菌に対する活性が高い。特に猫の腎盂腎炎の第一選択薬として優れる。エンテロコッカスには無効。",
        },
        "cat": {
            "notes_append": " [UTI/ISCAID 2019] 3-5 mg/kg (tablets) or 5-7.5 mg/kg (suspension) PO q24h. Theoretically excellent first-line for feline pyelonephritis. Not for Enterococcus.",
            "notes_ja_append": " [UTI/ISCAID 2019] 3-5 mg/kg（錠剤）または 5-7.5 mg/kg（懸濁液）経口 24時間ごと。理論的に猫の腎盂腎炎の第一選択として優れる。エンテロコッカスには無効。",
        },
    },
    "trimethoprim_sulfa": {
        "dog": {
            "notes_append": " [UTI/ISCAID 2019] 15-30 mg/kg PO q12h (total product dose). Appropriate first-line or empirical choice for UTI. Prostatitis treatment option (good prostatic penetration via trimethoprim, though sulfadiazine levels low in prostatic tissue). Long-term use (>7 days): baseline Schirmer tear test + regular re-evaluation + owner monitoring for ocular discharge. Avoid in dogs prone to KCS, hepatic disease, hypersensitivity. Controversial activity against urinary Enterococcus — avoid.",
            "notes_ja_append": " [UTI/ISCAID 2019] 15-30 mg/kg 経口 12時間ごと（総製品用量）。UTIの適切な第一選択または経験的選択薬。前立腺炎の治療選択肢（トリメトプリムの良好な前立腺移行性、ただしスルファジアジンの前立腺組織濃度は低い）。長期使用（7日超）: ベースラインのシルマー涙液検査 + 定期再評価 + 飼い主による眼分泌物モニタリング。KCS傾向犬・肝疾患・過敏症では避ける。尿中エンテロコッカスに対する活性は議論あり — 避ける。",
        },
        "cat": {
            "notes_append": " [UTI/ISCAID 2019] Same dosing as dogs. Appropriate first-line for confirmed bacterial cystitis.",
            "notes_ja_append": " [UTI/ISCAID 2019] 犬と同じ用量。確認された細菌性膀胱炎の適切な第一選択。",
        },
    },
}
