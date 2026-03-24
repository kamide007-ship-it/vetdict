"""Drug species_info expansion – batch 3.

Adds dosage data for under-represented species (guinea_pig, hamster,
hedgehog, chinchilla, snake, tortoise, reptile, horse).

References:
  - Carpenter's Exotic Animal Formulary, 6th ed.
  - Plumb's Veterinary Drug Handbook, 9th ed.
  - BSAVA Manual of Exotic Pets, 5th ed.

The dict maps drug_id -> species -> species_info entry.
Merged at import time in drug_dictionary.py.
"""

from __future__ import annotations

SPECIES_INFO_PATCH: dict[str, dict[str, dict]] = {
    # ==================================================================
    # Guinea pig (モルモット) — ~50 drugs
    # ==================================================================
    "cephalexin": {
        "guinea_pig": {"safe": False, "dosage": "N/A", "dosage_ja": "使用不可", "notes": "Oral cephalosporins cause fatal dysbiosis in guinea pigs", "notes_ja": "経口セファロスポリンはモルモットに致死的な腸内細菌叢の破壊を起こす"},
    },
    "chloramphenicol": {
        "guinea_pig": {"safe": True, "dosage": "30-50 mg/kg PO q12h", "dosage_ja": "30-50 mg/kg 経口 12時間毎", "notes": "Useful broad-spectrum option safe for guinea pigs", "notes_ja": "モルモットに安全な広域スペクトル抗菌薬"},
    },
    "gentamicin": {
        "guinea_pig": {"safe": True, "dosage": "5-8 mg/kg SC/IM q24h", "dosage_ja": "5-8 mg/kg 皮下/筋注 24時間毎", "notes": "Monitor for nephrotoxicity and ototoxicity; ensure adequate hydration", "notes_ja": "腎毒性・聴器毒性に注意。十分な水和を確保"},
    },
    "marbofloxacin": {
        "guinea_pig": {"safe": True, "dosage": "5 mg/kg PO q24h", "dosage_ja": "5 mg/kg 経口 24時間毎", "notes": "Fluoroquinolone; use with caution in young growing animals", "notes_ja": "フルオロキノロン系。成長期の若齢個体には慎重投与"},
    },
    "tylosin": {
        "guinea_pig": {"safe": True, "dosage": "10 mg/kg PO q12h", "dosage_ja": "10 mg/kg 経口 12時間毎", "notes": "Macrolide; useful for respiratory infections", "notes_ja": "マクロライド系。呼吸器感染症に有用"},
    },
    "florfenicol": {
        "guinea_pig": {"safe": True, "dosage": "25 mg/kg SC q24-48h", "dosage_ja": "25 mg/kg 皮下 24-48時間毎", "notes": "Alternative when chloramphenicol unavailable", "notes_ja": "クロラムフェニコール入手不可時の代替"},
    },
    "penicillin_g": {
        "guinea_pig": {"safe": True, "dosage": "22,000-44,000 IU/kg SC/IM q24h", "dosage_ja": "22,000-44,000 IU/kg 皮下/筋注 24時間毎", "notes": "Injectable penicillin is safe; NEVER give oral penicillin to guinea pigs", "notes_ja": "注射用ペニシリンは安全。経口ペニシリンは絶対に投与しない"},
    },
    "oxytetracycline": {
        "guinea_pig": {"safe": True, "dosage": "50 mg/kg PO q12h", "dosage_ja": "50 mg/kg 経口 12時間毎", "notes": "Long-acting injectable: 60 mg/kg SC q72h also used", "notes_ja": "長時間作用型注射：60 mg/kg 皮下 72時間毎も使用"},
    },
    "itraconazole": {
        "guinea_pig": {"safe": True, "dosage": "5-10 mg/kg PO q24h", "dosage_ja": "5-10 mg/kg 経口 24時間毎", "notes": "First-line for dermatophytosis; give with food for better absorption", "notes_ja": "皮膚糸状菌症の第一選択。食事と共に投与で吸収向上"},
    },
    "fluconazole": {
        "guinea_pig": {"safe": True, "dosage": "5-16 mg/kg PO q24h", "dosage_ja": "5-16 mg/kg 経口 24時間毎", "notes": "Alternative antifungal; good CNS penetration", "notes_ja": "代替抗真菌薬。CNS移行性良好"},
    },
    "terbinafine": {
        "guinea_pig": {"safe": True, "dosage": "10-30 mg/kg PO q24h", "dosage_ja": "10-30 mg/kg 経口 24時間毎", "notes": "Effective for Trichophyton; 4-6 week course typically needed", "notes_ja": "トリコフィトンに有効。通常4-6週間の投与が必要"},
    },
    "griseofulvin": {
        "guinea_pig": {"safe": True, "dosage": "15-25 mg/kg PO q24h for 4-6 weeks", "dosage_ja": "15-25 mg/kg 経口 24時間毎 4-6週間", "notes": "Teratogenic; do not use in pregnant animals", "notes_ja": "催奇形性あり。妊娠個体には使用しない"},
    },
    "praziquantel": {
        "guinea_pig": {"safe": True, "dosage": "5-10 mg/kg PO/SC, repeat in 10-14 days", "dosage_ja": "5-10 mg/kg 経口/皮下 10-14日後に再投与", "notes": "For cestode infections", "notes_ja": "条虫感染に使用"},
    },
    "fipronil": {
        "guinea_pig": {"safe": False, "dosage": "N/A", "dosage_ja": "使用不可", "notes": "TOXIC to guinea pigs — can cause fatal seizures", "notes_ja": "モルモットに有毒 — 致死的痙攣を引き起こす可能性"},
    },
    "fluralaner": {
        "guinea_pig": {"safe": True, "dosage": "8-12 mg/kg PO once; repeat in 8-12 weeks", "dosage_ja": "8-12 mg/kg 経口 単回; 8-12週後に再投与", "notes": "Effective for Trixacarus mites; emerging use in exotics", "notes_ja": "疥癬ダニに有効。エキゾチック動物での使用が増加中"},
    },
    "toltrazuril": {
        "guinea_pig": {"safe": True, "dosage": "10 mg/kg PO q24h for 3 days", "dosage_ja": "10 mg/kg 経口 24時間毎 3日間", "notes": "For coccidiosis (Eimeria caviae)", "notes_ja": "コクシジウム症（Eimeria caviae）に使用"},
    },
    "carprofen": {
        "guinea_pig": {"safe": True, "dosage": "4 mg/kg SC q24h", "dosage_ja": "4 mg/kg 皮下 24時間毎", "notes": "NSAID; use short-term; monitor for GI side effects", "notes_ja": "NSAID。短期使用。消化器副作用に注意"},
    },
    "tramadol": {
        "guinea_pig": {"safe": True, "dosage": "5-10 mg/kg PO q12h", "dosage_ja": "5-10 mg/kg 経口 12時間毎", "notes": "Moderate pain relief; often combined with NSAID", "notes_ja": "中等度の鎮痛。NSAIDとの併用が多い"},
    },
    "gabapentin": {
        "guinea_pig": {"safe": True, "dosage": "5-10 mg/kg PO q8-12h", "dosage_ja": "5-10 mg/kg 経口 8-12時間毎", "notes": "Neuropathic pain; may cause mild sedation", "notes_ja": "神経障害性疼痛に使用。軽度の鎮静が生じうる"},
    },
    "buprenorphine": {
        "guinea_pig": {"safe": True, "dosage": "0.05-0.1 mg/kg SC/IM q8-12h", "dosage_ja": "0.05-0.1 mg/kg 皮下/筋注 8-12時間毎", "notes": "Good perioperative analgesia", "notes_ja": "周術期の良好な鎮痛効果"},
    },
    "butorphanol": {
        "guinea_pig": {"safe": True, "dosage": "0.5-2 mg/kg SC/IM q4-6h", "dosage_ja": "0.5-2 mg/kg 皮下/筋注 4-6時間毎", "notes": "Short-acting; useful for procedural sedation/analgesia", "notes_ja": "短時間作用型。処置時の鎮静・鎮痛に有用"},
    },
    "ketamine": {
        "guinea_pig": {"safe": True, "dosage": "20-40 mg/kg IM (with xylazine 5 mg/kg)", "dosage_ja": "20-40 mg/kg 筋注（キシラジン5 mg/kgと併用）", "notes": "Always combine with sedative/analgesic for adequate anesthesia", "notes_ja": "十分な麻酔のため必ず鎮静薬/鎮痛薬と併用"},
    },
    "propofol": {
        "guinea_pig": {"safe": True, "dosage": "3-5 mg/kg IV slowly to effect", "dosage_ja": "3-5 mg/kg 緩徐静注 効果発現まで", "notes": "IV access challenging; often use after IM premedication", "notes_ja": "静脈確保が困難。IM前投薬後に使用することが多い"},
    },
    "alfaxalone": {
        "guinea_pig": {"safe": True, "dosage": "5-10 mg/kg IM for sedation; 3-5 mg/kg IV for induction", "dosage_ja": "鎮静: 5-10 mg/kg 筋注; 導入: 3-5 mg/kg 静注", "notes": "Preferred induction agent; smoother recovery than ketamine", "notes_ja": "推奨される導入薬。ケタミンより回復が良好"},
    },
    "prednisolone": {
        "guinea_pig": {"safe": True, "dosage": "0.5-1 mg/kg PO/IM q12-24h", "dosage_ja": "0.5-1 mg/kg 経口/筋注 12-24時間毎", "notes": "Use cautiously; guinea pigs are sensitive to immunosuppression", "notes_ja": "慎重投与。モルモットは免疫抑制に敏感"},
    },
    "dexamethasone": {
        "guinea_pig": {"safe": True, "dosage": "0.2-0.6 mg/kg IM/IV once", "dosage_ja": "0.2-0.6 mg/kg 筋注/静注 単回", "notes": "Short-term anti-inflammatory/shock; avoid chronic use", "notes_ja": "短期間の抗炎症/ショック治療。長期使用は避ける"},
    },
    "omeprazole": {
        "guinea_pig": {"safe": True, "dosage": "4 mg/kg PO q24h", "dosage_ja": "4 mg/kg 経口 24時間毎", "notes": "For gastric ulceration, commonly seen with NSAIDs or stress", "notes_ja": "胃潰瘍に使用。NSAID投与時やストレス時に多い"},
    },
    "famotidine": {
        "guinea_pig": {"safe": True, "dosage": "0.5-1 mg/kg PO/SC q12-24h", "dosage_ja": "0.5-1 mg/kg 経口/皮下 12-24時間毎", "notes": "H2 blocker; gastric acid reduction", "notes_ja": "H2ブロッカー。胃酸分泌抑制"},
    },
    "metoclopramide": {
        "guinea_pig": {"safe": True, "dosage": "0.5-1 mg/kg PO/SC q8-12h", "dosage_ja": "0.5-1 mg/kg 経口/皮下 8-12時間毎", "notes": "Prokinetic; useful for GI stasis", "notes_ja": "消化管運動促進薬。消化管うっ滞に有用"},
    },
    "lactulose": {
        "guinea_pig": {"safe": True, "dosage": "0.5 mL/kg PO q8-12h", "dosage_ja": "0.5 mL/kg 経口 8-12時間毎", "notes": "Osmotic laxative; adjust dose to stool consistency", "notes_ja": "浸透圧性緩下剤。便の硬さに応じて用量調整"},
    },
    "furosemide": {
        "guinea_pig": {"safe": True, "dosage": "1-4 mg/kg PO/SC/IM q12h", "dosage_ja": "1-4 mg/kg 経口/皮下/筋注 12時間毎", "notes": "For pulmonary edema or pleural effusion", "notes_ja": "肺水腫・胸水に使用"},
    },
    "benazepril": {
        "guinea_pig": {"safe": True, "dosage": "0.25-0.5 mg/kg PO q24h", "dosage_ja": "0.25-0.5 mg/kg 経口 24時間毎", "notes": "ACE inhibitor for cardiac disease", "notes_ja": "心疾患に対するACE阻害薬"},
    },
    "amlodipine": {
        "guinea_pig": {"safe": True, "dosage": "0.1-0.25 mg/kg PO q24h", "dosage_ja": "0.1-0.25 mg/kg 経口 24時間毎", "notes": "Calcium channel blocker for hypertension", "notes_ja": "高血圧に対するカルシウム拮抗薬"},
    },
    "midazolam": {
        "guinea_pig": {"safe": True, "dosage": "0.5-2 mg/kg IM/IN", "dosage_ja": "0.5-2 mg/kg 筋注/経鼻", "notes": "Sedation/premedication; intranasal route effective", "notes_ja": "鎮静/前投薬。経鼻投与も有効"},
    },
    "diazepam": {
        "guinea_pig": {"safe": True, "dosage": "0.5-3 mg/kg IM/IV", "dosage_ja": "0.5-3 mg/kg 筋注/静注", "notes": "Seizure control; sedation; IM absorption unreliable", "notes_ja": "痙攣管理・鎮静。IM吸収は不安定"},
    },
    "vitamin_k1": {
        "guinea_pig": {"safe": True, "dosage": "1-10 mg/kg SC/IM q24h", "dosage_ja": "1-10 mg/kg 皮下/筋注 24時間毎", "notes": "For anticoagulant rodenticide toxicity", "notes_ja": "抗凝固性殺鼠剤中毒に使用"},
    },
    "vitamin_b12": {
        "guinea_pig": {"safe": True, "dosage": "0.02 mg/kg SC/IM q7d", "dosage_ja": "0.02 mg/kg 皮下/筋注 週1回", "notes": "Supportive care for anorexia and weight loss", "notes_ja": "食欲不振・体重減少の支持療法"},
    },
    "sucralfate": {
        "guinea_pig": {"safe": True, "dosage": "25-50 mg/kg PO q8-12h", "dosage_ja": "25-50 mg/kg 経口 8-12時間毎", "notes": "Gastric ulcer protection; give 1h before other meds", "notes_ja": "胃潰瘍保護。他の薬剤の1時間前に投与"},
    },
    "maropitant": {
        "guinea_pig": {"safe": True, "dosage": "1-2 mg/kg SC q24h", "dosage_ja": "1-2 mg/kg 皮下 24時間毎", "notes": "Antiemetic; limited data in guinea pigs but used clinically", "notes_ja": "制吐薬。モルモットでのデータは限られるが臨床使用あり"},
    },
    "isoflurane": {
        "guinea_pig": {"safe": True, "dosage": "Induction 3-5%, maintenance 1.5-3%", "dosage_ja": "導入 3-5%, 維持 1.5-3%", "notes": "Standard inhalant anesthetic; mask or chamber induction", "notes_ja": "標準的吸入麻酔薬。マスクまたはチャンバーで導入"},
    },
    "sevoflurane": {
        "guinea_pig": {"safe": True, "dosage": "Induction 6-8%, maintenance 3-4.5%", "dosage_ja": "導入 6-8%, 維持 3-4.5%", "notes": "Faster induction and recovery than isoflurane", "notes_ja": "イソフルランより導入・回復が速い"},
    },
    "moxidectin": {
        "guinea_pig": {"safe": True, "dosage": "0.2-0.5 mg/kg PO/topical once; repeat in 10-14 days", "dosage_ja": "0.2-0.5 mg/kg 経口/外用 単回; 10-14日後に再投与", "notes": "For mite infestations (Trixacarus)", "notes_ja": "ダニ寄生（Trixacarus）に使用"},
    },
    "rifampin": {
        "guinea_pig": {"safe": True, "dosage": "10-20 mg/kg PO q24h", "dosage_ja": "10-20 mg/kg 経口 24時間毎", "notes": "For mycobacterial or resistant infections; turns urine orange", "notes_ja": "抗酸菌・耐性菌感染に使用。尿がオレンジ色になる"},
    },
    "iron_dextran": {
        "guinea_pig": {"safe": True, "dosage": "10 mg/kg IM once; repeat in 7-10 days if needed", "dosage_ja": "10 mg/kg 筋注 単回; 必要時7-10日後に再投与", "notes": "For iron deficiency anemia in neonates/weanlings", "notes_ja": "新生仔/離乳仔の鉄欠乏性貧血に使用"},
    },
    "n_acetylcysteine": {
        "guinea_pig": {"safe": True, "dosage": "70 mg/kg PO/IV q6-8h", "dosage_ja": "70 mg/kg 経口/静注 6-8時間毎", "notes": "Mucolytic and antioxidant; used for hepatic support", "notes_ja": "粘液溶解薬・抗酸化剤。肝保護に使用"},
    },
    "mannitol": {
        "guinea_pig": {"safe": True, "dosage": "0.5-1 g/kg IV over 20 min", "dosage_ja": "0.5-1 g/kg 20分かけて静注", "notes": "For cerebral edema/raised ICP; ensure IV access", "notes_ja": "脳浮腫/頭蓋内圧亢進に使用。静脈路確保が必要"},
    },
    "atropine": {
        "guinea_pig": {"safe": True, "dosage": "0.05-0.1 mg/kg SC/IM", "dosage_ja": "0.05-0.1 mg/kg 皮下/筋注", "notes": "Many guinea pigs carry atropinase; higher doses may be needed", "notes_ja": "多くのモルモットはアトロピナーゼを持つ。高用量が必要な場合がある"},
    },
    "glycopyrrolate": {
        "guinea_pig": {"safe": True, "dosage": "0.01-0.02 mg/kg SC/IM", "dosage_ja": "0.01-0.02 mg/kg 皮下/筋注", "notes": "Preferred anticholinergic; not affected by atropinase", "notes_ja": "推奨される抗コリン薬。アトロピナーゼの影響を受けない"},
    },
}
