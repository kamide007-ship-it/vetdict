"""Drug batch 7 – Chinchilla species-specific dosing patches.

Chinchillas are hindgut fermenters with sensitive gut flora, similar to
rabbits and guinea pigs. Oral beta-lactams, lincosamides, and macrolides
carry a HIGH RISK of fatal dysbiosis and are generally contraindicated.

Safe first-line antibiotics: Enrofloxacin, TMS, Chloramphenicol (already
in batch 3). This batch covers the remaining commonly used drugs.

References:
  - Carpenter's Exotic Animal Formulary, 6th ed. (2023)
  - Quesenberry & Carpenter: Ferrets, Rabbits, and Rodents, 4th ed.
  - BSAVA Manual of Exotic Pets, 5th ed.
  - Plumb's Veterinary Drug Handbook, 10th ed.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Chinchilla species_info patches for existing drugs
# ---------------------------------------------------------------------------
CHINCHILLA_SPECIES_PATCH: dict[str, dict[str, dict]] = {
    # ── Antibiotics ──────────────────────────────────────────────────
    "ampicillin": {
        "chinchilla": {
            "safe": False, "dosage": "N/A", "dosage_ja": "使用不可",
            "notes": "CONTRAINDICATED. Oral beta-lactams cause fatal dysbiosis in chinchillas.",
            "notes_ja": "【禁忌】経口ベータラクタム系は致死的な腸内細菌叢破壊を引き起こす。注射剤も推奨しない。",
        },
    },
    "cefovecin": {
        "chinchilla": {
            "safe": False, "dosage": "N/A", "dosage_ja": "使用不可",
            "notes": "CONTRAINDICATED. Long-acting cephalosporin; high dysbiosis risk.",
            "notes_ja": "【禁忌】長時間作用型セファロスポリン。腸内細菌叢破壊のリスクが高い。",
        },
    },
    "lincomycin": {
        "chinchilla": {
            "safe": False, "dosage": "N/A", "dosage_ja": "使用不可",
            "notes": "CONTRAINDICATED. Lincosamides cause fatal enterotoxemia.",
            "notes_ja": "【禁忌】リンコサミド系は致死的な腸管毒素症を引き起こす。",
        },
    },
    "erythromycin": {
        "chinchilla": {
            "safe": False, "dosage": "N/A", "dosage_ja": "使用不可",
            "notes": "CONTRAINDICATED. Macrolides cause fatal dysbiosis in chinchillas.",
            "notes_ja": "【禁忌】マクロライド系は致死的な腸内細菌叢破壊を引き起こす。",
        },
    },
    "tylosin": {
        "chinchilla": {
            "safe": False, "dosage": "N/A", "dosage_ja": "原則使用不可",
            "notes": "Generally contraindicated. Macrolide antibiotic; high dysbiosis risk.",
            "notes_ja": "原則禁忌。マクロライド系抗菌薬。腸内細菌叢破壊のリスクが高い。",
        },
    },
    "pradofloxacin": {
        "chinchilla": {
            "safe": True, "dosage": "5-7.5 mg/kg PO q24h", "dosage_ja": "5-7.5 mg/kg 経口 24時間毎",
            "notes": "Third-generation fluoroquinolone; safe for chinchillas. Avoid in growing animals.",
            "notes_ja": "第三世代フルオロキノロン系。チンチラに安全。成長期の若齢個体には慎重投与。",
        },
    },
    "oxytetracycline": {
        "chinchilla": {
            "safe": True, "dosage": "50 mg/kg PO q12h", "dosage_ja": "50 mg/kg 経口 12時間毎",
            "notes": "Tetracycline; generally safe. May cause GI upset at high doses.",
            "notes_ja": "テトラサイクリン系。一般的に安全。高用量で消化器障害の可能性。",
        },
    },
    "amikacin": {
        "chinchilla": {
            "safe": True, "dosage": "8-16 mg/kg SC/IM q24h", "dosage_ja": "8-16 mg/kg 皮下/筋注 24時間毎",
            "notes": "Aminoglycoside; nephrotoxic/ototoxic. Ensure hydration. Monitor renal values.",
            "notes_ja": "アミノグリコシド系。腎毒性・聴器毒性あり。十分な水和と腎機能モニタリングが必要。",
        },
    },
    "cefazolin": {
        "chinchilla": {
            "safe": True, "dosage": "20-40 mg/kg SC/IM q8-12h", "dosage_ja": "20-40 mg/kg 皮下/筋注 8-12時間毎",
            "notes": "Injectable cephalosporin only; NEVER give orally. Perioperative use.",
            "notes_ja": "注射剤のみ使用可。経口投与は絶対不可。周術期に限定使用。",
        },
    },
    "ceftriaxone": {
        "chinchilla": {
            "safe": True, "dosage": "20-40 mg/kg SC/IM q12-24h", "dosage_ja": "20-40 mg/kg 皮下/筋注 12-24時間毎",
            "notes": "Injectable cephalosporin only; NEVER give orally. For severe infections.",
            "notes_ja": "注射剤のみ使用可。経口投与は絶対不可。重篤な感染症に使用。",
        },
    },
    # ── Antiparasitics ───────────────────────────────────────────────
    "fipronil": {
        "chinchilla": {
            "safe": False, "dosage": "N/A", "dosage_ja": "使用不可",
            "notes": "CONTRAINDICATED. Reported fatalities in chinchillas. Use selamectin instead.",
            "notes_ja": "【禁忌】チンチラでの死亡例が報告されている。代わりにセラメクチンを使用。",
        },
    },
    "permethrin": {
        "chinchilla": {
            "safe": False, "dosage": "N/A", "dosage_ja": "使用不可",
            "notes": "CONTRAINDICATED. Pyrethroid toxicity risk. Use selamectin or ivermectin.",
            "notes_ja": "【禁忌】ピレスロイド中毒のリスク。セラメクチンまたはイベルメクチンを使用。",
        },
    },
    "fluralaner": {
        "chinchilla": {
            "safe": True, "dosage": "25 mg/kg PO once (off-label)", "dosage_ja": "25 mg/kg 経口 単回（適応外使用）",
            "notes": "Isoxazoline; emerging evidence for use in chinchillas. Monitor for neurological side effects.",
            "notes_ja": "イソキサゾリン系。チンチラでの使用は新知見段階。神経症状の副作用に注意。",
        },
    },
    "toltrazuril": {
        "chinchilla": {
            "safe": True, "dosage": "10 mg/kg PO q24h × 3 days", "dosage_ja": "10 mg/kg 経口 24時間毎 × 3日",
            "notes": "Anticoccidial. Effective for coccidiosis in chinchillas.",
            "notes_ja": "抗コクシジウム薬。チンチラのコクシジウム症に有効。",
        },
    },
    # ── Analgesics / Sedatives ────────────────────────────────────────
    "fentanyl": {
        "chinchilla": {
            "safe": True, "dosage": "0.02-0.05 mg/kg SC/IM", "dosage_ja": "0.02-0.05 mg/kg 皮下/筋注",
            "notes": "Potent opioid analgesic for perioperative pain. Short duration.",
            "notes_ja": "強力なオピオイド鎮痛薬。周術期疼痛に使用。作用時間が短い。",
        },
    },
    "morphine": {
        "chinchilla": {
            "safe": True, "dosage": "2-5 mg/kg SC/IM q4h", "dosage_ja": "2-5 mg/kg 皮下/筋注 4時間毎",
            "notes": "Opioid analgesic. May cause GI stasis at high doses; monitor fecal output.",
            "notes_ja": "オピオイド鎮痛薬。高用量で消化管うっ滞の可能性。糞便量のモニタリングが必要。",
        },
    },
    "dexmedetomidine": {
        "chinchilla": {
            "safe": True, "dosage": "0.01-0.04 mg/kg SC/IM", "dosage_ja": "0.01-0.04 mg/kg 皮下/筋注",
            "notes": "Alpha-2 agonist sedative. Use with atipamezole reversal available. Bradycardia expected.",
            "notes_ja": "アルファ2作動薬鎮静剤。アチパメゾール（拮抗薬）を必ず準備。徐脈が生じる。",
        },
    },
    "atipamezole": {
        "chinchilla": {
            "safe": True, "dosage": "Equal volume to dexmedetomidine, IM", "dosage_ja": "デクスメデトミジンと等量 筋注",
            "notes": "Alpha-2 antagonist; reverses medetomidine/dexmedetomidine sedation.",
            "notes_ja": "アルファ2拮抗薬。メデトミジン/デクスメデトミジンの鎮静を拮抗。",
        },
    },
    "acepromazine": {
        "chinchilla": {
            "safe": True, "dosage": "0.5-1.0 mg/kg SC/IM", "dosage_ja": "0.5-1.0 mg/kg 皮下/筋注",
            "notes": "Phenothiazine tranquilizer. Causes hypotension; avoid in debilitated animals.",
            "notes_ja": "フェノチアジン系鎮静薬。低血圧を引き起こす。衰弱動物には使用不可。",
        },
    },
    "propofol": {
        "chinchilla": {
            "safe": True, "dosage": "5-10 mg/kg IV to effect", "dosage_ja": "5-10 mg/kg 緩徐静注（効果発現まで）",
            "notes": "IV anesthetic induction agent. Rapid recovery. Apnea risk; intubation recommended.",
            "notes_ja": "静脈麻酔導入薬。覚醒が速い。無呼吸のリスクがあるため気管挿管推奨。",
        },
    },
    # ── GI / Hepatic ──────────────────────────────────────────────────
    "omeprazole": {
        "chinchilla": {
            "safe": True, "dosage": "0.5-1 mg/kg PO q24h", "dosage_ja": "0.5-1 mg/kg 経口 24時間毎",
            "notes": "Proton pump inhibitor for gastric ulcers.",
            "notes_ja": "プロトンポンプ阻害薬。胃潰瘍に使用。",
        },
    },
    "cisapride": {
        "chinchilla": {
            "safe": True, "dosage": "0.5 mg/kg PO q8-12h", "dosage_ja": "0.5 mg/kg 経口 8-12時間毎",
            "notes": "GI prokinetic; useful for ileus/GI stasis. Compound pharmacy required.",
            "notes_ja": "消化管運動促進薬。腸管うっ滞に有効。調剤薬局での調製が必要。",
        },
    },
    "maropitant": {
        "chinchilla": {
            "safe": True, "dosage": "1 mg/kg SC q24h", "dosage_ja": "1 mg/kg 皮下 24時間毎",
            "notes": "NK1 receptor antagonist antiemetic. Also provides visceral analgesia.",
            "notes_ja": "NK1受容体拮抗薬制吐薬。内臓鎮痛作用もある。",
        },
    },
    "ursodiol": {
        "chinchilla": {
            "safe": True, "dosage": "15-20 mg/kg PO q24h", "dosage_ja": "15-20 mg/kg 経口 24時間毎",
            "notes": "Hepatoprotectant; for hepatic lipidosis and cholestatic disease.",
            "notes_ja": "肝保護薬。肝リピドーシスや胆汁うっ滞に使用。",
        },
    },
    # ── Cardiac ────────────────────────────────────────────────────────
    "amlodipine": {
        "chinchilla": {
            "safe": True, "dosage": "0.1-0.2 mg/kg PO q24h", "dosage_ja": "0.1-0.2 mg/kg 経口 24時間毎",
            "notes": "Calcium channel blocker; for systemic hypertension.",
            "notes_ja": "カルシウムチャネル遮断薬。全身性高血圧に使用。",
        },
    },
    # ── Endocrine ──────────────────────────────────────────────────────
    "insulin": {
        "chinchilla": {
            "safe": True, "dosage": "0.5-2 IU/kg SC q12-24h (start low)", "dosage_ja": "0.5-2 IU/kg 皮下 12-24時間毎（低用量で開始）",
            "notes": "For diabetes mellitus. Monitor blood glucose closely. Dietary management essential (eliminate sugar/fruit).",
            "notes_ja": "糖尿病に使用。血糖値を厳密にモニタリング。食事管理（砂糖・果物の除去）が不可欠。",
        },
    },
    "calcium_gluconate": {
        "chinchilla": {
            "safe": True, "dosage": "50-100 mg/kg IV slow or SC diluted", "dosage_ja": "50-100 mg/kg 緩徐静注 または 皮下（希釈）",
            "notes": "For hypocalcemia/eclampsia. Monitor heart during IV administration.",
            "notes_ja": "低カルシウム血症・子癇に使用。静注時は心拍モニタリングが必要。",
        },
    },
    # ── Ophthalmic ─────────────────────────────────────────────────────
    "tobramycin_ophthalmic": {
        "chinchilla": {
            "safe": True, "dosage": "1 drop affected eye q6-8h", "dosage_ja": "患眼に1滴 6-8時間毎",
            "notes": "Topical aminoglycoside; for bacterial conjunctivitis/corneal ulcers.",
            "notes_ja": "局所アミノグリコシド系。細菌性結膜炎・角膜潰瘍に使用。",
        },
    },
    # ── Antifungals ────────────────────────────────────────────────────
    "ketoconazole": {
        "chinchilla": {
            "safe": True, "dosage": "10-15 mg/kg PO q24h × 4-6 weeks", "dosage_ja": "10-15 mg/kg 経口 24時間毎 × 4-6週間",
            "notes": "Azole antifungal for dermatophytosis. Monitor liver values. Terbinafine preferred.",
            "notes_ja": "アゾール系抗真菌薬。皮膚糸状菌症に使用。肝機能モニタリングが必要。テルビナフィンが第一選択。",
        },
    },
    "nystatin": {
        "chinchilla": {
            "safe": True, "dosage": "100,000 IU/kg PO q8-12h", "dosage_ja": "100,000 IU/kg 経口 8-12時間毎",
            "notes": "For GI candidiasis. Not absorbed systemically.",
            "notes_ja": "消化管カンジダ症に使用。全身吸収されない。",
        },
    },
    # ── Neurological ───────────────────────────────────────────────────
    "levetiracetam": {
        "chinchilla": {
            "safe": True, "dosage": "20-40 mg/kg PO q8-12h", "dosage_ja": "20-40 mg/kg 経口 8-12時間毎",
            "notes": "Anticonvulsant; first-line for seizure management in chinchillas. Minimal hepatic metabolism.",
            "notes_ja": "抗けいれん薬。チンチラの発作管理の第一選択。肝代謝が少なく安全性が高い。",
        },
    },
    "phenobarbital": {
        "chinchilla": {
            "safe": True, "dosage": "2-5 mg/kg PO q12h", "dosage_ja": "2-5 mg/kg 経口 12時間毎",
            "notes": "Anticonvulsant; monitor liver values long-term. Levetiracetam preferred.",
            "notes_ja": "抗けいれん薬。長期使用時は肝機能モニタリングが必要。レベチラセタムが第一選択。",
        },
    },
    # ── Supplements / Other ────────────────────────────────────────────
    "chlorhexidine": {
        "chinchilla": {
            "safe": True, "dosage": "0.05% solution topical", "dosage_ja": "0.05%溶液 局所使用",
            "notes": "Antiseptic for wound cleaning. Dilute well; concentrated solution is irritating.",
            "notes_ja": "創傷洗浄用消毒薬。十分に希釈して使用。高濃度では皮膚刺激性あり。",
        },
    },
    "oxytocin": {
        "chinchilla": {
            "safe": True, "dosage": "0.5-3 IU/kg SC/IM", "dosage_ja": "0.5-3 IU/kg 皮下/筋注",
            "notes": "For dystocia (after verifying no mechanical obstruction). Use with calcium supplementation.",
            "notes_ja": "難産に使用（機械的閉塞がないことを確認後）。カルシウム補充と併用。",
        },
    },
    "aluminum_hydroxide": {
        "chinchilla": {
            "safe": True, "dosage": "30 mg/kg PO q8h with food", "dosage_ja": "30 mg/kg 経口 8時間毎（食事と共に）",
            "notes": "Phosphate binder for renal disease/hyperphosphatemia.",
            "notes_ja": "リン吸着薬。腎疾患・高リン血症に使用。",
        },
    },
}
