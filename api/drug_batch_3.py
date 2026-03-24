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
    # ==================================================================
    # Hamster (ハムスター) — ~45 drugs
    # ==================================================================
    "amoxicillin_clavulanate": {
        "hamster": {"safe": False, "dosage": "N/A", "dosage_ja": "使用不可", "notes": "Oral penicillins/cephalosporins cause fatal enterotoxemia in hamsters", "notes_ja": "経口ペニシリン/セファロスポリンはハムスターに致死的腸毒素血症を起こす"},
    },
    "metronidazole": {
        "hamster": {"safe": True, "dosage": "20 mg/kg PO q12h", "dosage_ja": "20 mg/kg 経口 12時間毎", "notes": "For anaerobic infections and protozoal disease", "notes_ja": "嫌気性菌感染・原虫疾患に使用"},
    },
    "cephalexin": {
        "hamster": {"safe": False, "dosage": "N/A", "dosage_ja": "使用不可", "notes": "Oral cephalosporins cause fatal dysbiosis in hamsters", "notes_ja": "経口セファロスポリンはハムスターに致死的な腸内細菌叢の破壊を起こす"},
    },
    "marbofloxacin": {
        "hamster": {"safe": True, "dosage": "5 mg/kg PO q24h", "dosage_ja": "5 mg/kg 経口 24時間毎", "notes": "Fluoroquinolone; avoid in young growing animals", "notes_ja": "フルオロキノロン系。成長期の若齢個体は避ける"},
    },
    "azithromycin": {
        "hamster": {"safe": True, "dosage": "10-30 mg/kg PO q24h", "dosage_ja": "10-30 mg/kg 経口 24時間毎", "notes": "Macrolide; useful for respiratory infections", "notes_ja": "マクロライド系。呼吸器感染症に有用"},
    },
    "trimethoprim_sulfa": {
        "hamster": {"safe": True, "dosage": "15-30 mg/kg PO q12h", "dosage_ja": "15-30 mg/kg 経口 12時間毎", "notes": "Broad-spectrum; well-tolerated in hamsters", "notes_ja": "広域スペクトル。ハムスターに忍容性良好"},
    },
    "chloramphenicol": {
        "hamster": {"safe": True, "dosage": "50 mg/kg PO q12h", "dosage_ja": "50 mg/kg 経口 12時間毎", "notes": "Safe broad-spectrum alternative to penicillins", "notes_ja": "ペニシリンの代替となる安全な広域スペクトル抗菌薬"},
    },
    "gentamicin": {
        "hamster": {"safe": True, "dosage": "5 mg/kg SC/IM q24h", "dosage_ja": "5 mg/kg 皮下/筋注 24時間毎", "notes": "Monitor for nephrotoxicity; maintain hydration", "notes_ja": "腎毒性に注意。水和を維持"},
    },
    "tylosin": {
        "hamster": {"safe": True, "dosage": "10 mg/kg PO q12h", "dosage_ja": "10 mg/kg 経口 12時間毎", "notes": "May be added to water (0.5 mg/mL); for proliferative ileitis", "notes_ja": "飲水に添加可能（0.5 mg/mL）。増殖性回腸炎に使用"},
    },
    "penicillin_g": {
        "hamster": {"safe": True, "dosage": "22,000 IU/kg SC/IM q24h", "dosage_ja": "22,000 IU/kg 皮下/筋注 24時間毎", "notes": "Injectable penicillin is safe; NEVER give oral penicillin", "notes_ja": "注射用ペニシリンは安全。経口投与は絶対に不可"},
    },
    "itraconazole": {
        "hamster": {"safe": True, "dosage": "5-10 mg/kg PO q24h", "dosage_ja": "5-10 mg/kg 経口 24時間毎", "notes": "For dermatophytosis; give with fatty food", "notes_ja": "皮膚糸状菌症に使用。脂肪分の多い食事と投与"},
    },
    "fluconazole": {
        "hamster": {"safe": True, "dosage": "5-10 mg/kg PO q24h", "dosage_ja": "5-10 mg/kg 経口 24時間毎", "notes": "Good oral bioavailability; alternative to itraconazole", "notes_ja": "経口バイオアベイラビリティ良好。イトラコナゾールの代替"},
    },
    "terbinafine": {
        "hamster": {"safe": True, "dosage": "10-30 mg/kg PO q24h", "dosage_ja": "10-30 mg/kg 経口 24時間毎", "notes": "For dermatophytosis", "notes_ja": "皮膚糸状菌症に使用"},
    },
    "selamectin": {
        "hamster": {"safe": True, "dosage": "15-30 mg/kg topical once; repeat in 14-28 days", "dosage_ja": "15-30 mg/kg 外用 単回; 14-28日後に再投与", "notes": "For mites (Demodex, Notoedres); apply between shoulder blades", "notes_ja": "ダニ類（ニキビダニ, ノトエドレス）に使用。肩甲骨間に塗布"},
    },
    "fenbendazole": {
        "hamster": {"safe": True, "dosage": "20-50 mg/kg PO q24h for 5 days", "dosage_ja": "20-50 mg/kg 経口 24時間毎 5日間", "notes": "For pinworms (Syphacia) and other helminths", "notes_ja": "蟯虫（シファシア）等の蠕虫に使用"},
    },
    "praziquantel": {
        "hamster": {"safe": True, "dosage": "5-10 mg/kg PO/SC; repeat in 14 days", "dosage_ja": "5-10 mg/kg 経口/皮下; 14日後に再投与", "notes": "For cestode infections (Hymenolepis)", "notes_ja": "条虫感染（小形条虫）に使用"},
    },
    "fipronil": {
        "hamster": {"safe": False, "dosage": "N/A", "dosage_ja": "使用不可", "notes": "TOXIC to hamsters — can cause fatal neurological signs", "notes_ja": "ハムスターに有毒 — 致死的神経症状を引き起こす可能性"},
    },
    "moxidectin": {
        "hamster": {"safe": True, "dosage": "0.2-0.5 mg/kg PO/topical; repeat in 10-14 days", "dosage_ja": "0.2-0.5 mg/kg 経口/外用; 10-14日後に再投与", "notes": "For Demodex mites", "notes_ja": "ニキビダニに使用"},
    },
    "toltrazuril": {
        "hamster": {"safe": True, "dosage": "10 mg/kg PO q24h for 3 days", "dosage_ja": "10 mg/kg 経口 24時間毎 3日間", "notes": "For coccidiosis", "notes_ja": "コクシジウム症に使用"},
    },
    "carprofen": {
        "hamster": {"safe": True, "dosage": "5 mg/kg SC q24h", "dosage_ja": "5 mg/kg 皮下 24時間毎", "notes": "NSAID; short-term use for post-operative pain", "notes_ja": "NSAID。術後疼痛の短期使用"},
    },
    "tramadol": {
        "hamster": {"safe": True, "dosage": "5-10 mg/kg PO q12h", "dosage_ja": "5-10 mg/kg 経口 12時間毎", "notes": "Moderate analgesia", "notes_ja": "中等度の鎮痛"},
    },
    "gabapentin": {
        "hamster": {"safe": True, "dosage": "5-10 mg/kg PO q8-12h", "dosage_ja": "5-10 mg/kg 経口 8-12時間毎", "notes": "Neuropathic pain; causes mild sedation", "notes_ja": "神経障害性疼痛。軽度の鎮静を生じうる"},
    },
    "buprenorphine": {
        "hamster": {"safe": True, "dosage": "0.05-0.1 mg/kg SC q8-12h", "dosage_ja": "0.05-0.1 mg/kg 皮下 8-12時間毎", "notes": "Perioperative analgesia; may reduce food intake", "notes_ja": "周術期鎮痛。摂食量が減少する場合がある"},
    },
    "butorphanol": {
        "hamster": {"safe": True, "dosage": "1-5 mg/kg SC q4h", "dosage_ja": "1-5 mg/kg 皮下 4時間毎", "notes": "Short-acting opioid", "notes_ja": "短時間作用型オピオイド"},
    },
    "ketamine": {
        "hamster": {"safe": True, "dosage": "50-200 mg/kg IP (with xylazine 10 mg/kg)", "dosage_ja": "50-200 mg/kg 腹腔内（キシラジン10 mg/kgと併用）", "notes": "Wide dose range; always combine with sedative", "notes_ja": "用量幅が広い。必ず鎮静薬と併用"},
    },
    "alfaxalone": {
        "hamster": {"safe": True, "dosage": "5-10 mg/kg IP/IM", "dosage_ja": "5-10 mg/kg 腹腔内/筋注", "notes": "Smoother recovery than ketamine combinations", "notes_ja": "ケタミン併用より回復が良好"},
    },
    "prednisolone": {
        "hamster": {"safe": True, "dosage": "0.5-2 mg/kg PO/SC q12-24h", "dosage_ja": "0.5-2 mg/kg 経口/皮下 12-24時間毎", "notes": "Anti-inflammatory/immunosuppressive; use cautiously", "notes_ja": "抗炎症/免疫抑制。慎重投与"},
    },
    "dexamethasone": {
        "hamster": {"safe": True, "dosage": "0.5-2 mg/kg IM/SC", "dosage_ja": "0.5-2 mg/kg 筋注/皮下", "notes": "Emergency anti-inflammatory; avoid chronic use", "notes_ja": "緊急の抗炎症。長期使用は避ける"},
    },
    "famotidine": {
        "hamster": {"safe": True, "dosage": "0.5 mg/kg PO/SC q24h", "dosage_ja": "0.5 mg/kg 経口/皮下 24時間毎", "notes": "H2 blocker for gastric protection", "notes_ja": "胃保護のH2ブロッカー"},
    },
    "furosemide": {
        "hamster": {"safe": True, "dosage": "1-4 mg/kg SC/IM q12h", "dosage_ja": "1-4 mg/kg 皮下/筋注 12時間毎", "notes": "For congestive heart failure; common in aged hamsters", "notes_ja": "うっ血性心不全に使用。高齢ハムスターに多い"},
    },
    "isoflurane": {
        "hamster": {"safe": True, "dosage": "Induction 3-4%, maintenance 1-2.5%", "dosage_ja": "導入 3-4%, 維持 1-2.5%", "notes": "Standard inhalant; chamber induction recommended", "notes_ja": "標準的吸入麻酔。チャンバー導入を推奨"},
    },
    "sevoflurane": {
        "hamster": {"safe": True, "dosage": "Induction 6-8%, maintenance 3-4%", "dosage_ja": "導入 6-8%, 維持 3-4%", "notes": "Faster induction and recovery than isoflurane", "notes_ja": "イソフルランより導入・回復が速い"},
    },
    "midazolam": {
        "hamster": {"safe": True, "dosage": "1-2 mg/kg IM/IP", "dosage_ja": "1-2 mg/kg 筋注/腹腔内", "notes": "Premedication/sedation; often combined with opioid", "notes_ja": "前投薬/鎮静。オピオイドとの併用が多い"},
    },
    "diazepam": {
        "hamster": {"safe": True, "dosage": "0.5-3 mg/kg IM/IP", "dosage_ja": "0.5-3 mg/kg 筋注/腹腔内", "notes": "Seizure control", "notes_ja": "痙攣管理"},
    },
    "atropine": {
        "hamster": {"safe": True, "dosage": "0.05 mg/kg SC/IM", "dosage_ja": "0.05 mg/kg 皮下/筋注", "notes": "Preanesthetic anticholinergic", "notes_ja": "麻酔前投薬の抗コリン薬"},
    },
    "vitamin_b12": {
        "hamster": {"safe": True, "dosage": "0.02 mg/kg SC/IM q7d", "dosage_ja": "0.02 mg/kg 皮下/筋注 週1回", "notes": "Supportive care", "notes_ja": "支持療法"},
    },
    "vitamin_k1": {
        "hamster": {"safe": True, "dosage": "1-10 mg/kg SC/IM q24h", "dosage_ja": "1-10 mg/kg 皮下/筋注 24時間毎", "notes": "For rodenticide toxicity", "notes_ja": "殺鼠剤中毒に使用"},
    },
    "sucralfate": {
        "hamster": {"safe": True, "dosage": "25-50 mg/kg PO q8-12h", "dosage_ja": "25-50 mg/kg 経口 8-12時間毎", "notes": "Gastric ulcer protection", "notes_ja": "胃潰瘍保護"},
    },
    "metoclopramide": {
        "hamster": {"safe": True, "dosage": "0.5 mg/kg PO/SC q12h", "dosage_ja": "0.5 mg/kg 経口/皮下 12時間毎", "notes": "Prokinetic for GI stasis", "notes_ja": "消化管うっ滞の運動促進薬"},
    },
    "mannitol": {
        "hamster": {"safe": True, "dosage": "0.5-1 g/kg IV over 20 min", "dosage_ja": "0.5-1 g/kg 20分かけて静注", "notes": "For cerebral edema; IV access very challenging", "notes_ja": "脳浮腫に使用。静脈確保が非常に困難"},
    },
    "n_acetylcysteine": {
        "hamster": {"safe": True, "dosage": "70 mg/kg PO/SC q8h", "dosage_ja": "70 mg/kg 経口/皮下 8時間毎", "notes": "Mucolytic; hepatoprotective", "notes_ja": "粘液溶解・肝保護"},
    },
    "iron_dextran": {
        "hamster": {"safe": True, "dosage": "10 mg/kg IM once", "dosage_ja": "10 mg/kg 筋注 単回", "notes": "For iron deficiency anemia", "notes_ja": "鉄欠乏性貧血に使用"},
    },
    "fluralaner": {
        "hamster": {"safe": True, "dosage": "10 mg/kg PO once; repeat in 8-12 weeks", "dosage_ja": "10 mg/kg 経口 単回; 8-12週後に再投与", "notes": "Emerging use for Demodex; limited data", "notes_ja": "ニキビダニへの使用が増加中。データは限られる"},
    },
    "glycopyrrolate": {
        "hamster": {"safe": True, "dosage": "0.01-0.02 mg/kg SC/IM", "dosage_ja": "0.01-0.02 mg/kg 皮下/筋注", "notes": "Preanesthetic anticholinergic", "notes_ja": "麻酔前投薬の抗コリン薬"},
    },
    # ==================================================================
    # Hedgehog (ハリネズミ) — ~45 drugs
    # ==================================================================
    "amoxicillin": {
        "hedgehog": {"safe": True, "dosage": "15-30 mg/kg PO q12h", "dosage_ja": "15-30 mg/kg 経口 12時間毎", "notes": "Broad-spectrum; well-tolerated in hedgehogs", "notes_ja": "広域スペクトル。ハリネズミに忍容性良好"},
    },
    "amoxicillin_clavulanate": {
        "hedgehog": {"safe": True, "dosage": "12.5-25 mg/kg PO q12h", "dosage_ja": "12.5-25 mg/kg 経口 12時間毎", "notes": "For resistant infections", "notes_ja": "耐性菌感染に使用"},
    },
    "doxycycline": {
        "hedgehog": {"safe": True, "dosage": "5-10 mg/kg PO q12-24h", "dosage_ja": "5-10 mg/kg 経口 12-24時間毎", "notes": "Good for respiratory and skin infections", "notes_ja": "呼吸器・皮膚感染症に有効"},
    },
    "metronidazole": {
        "hedgehog": {"safe": True, "dosage": "20 mg/kg PO q12h", "dosage_ja": "20 mg/kg 経口 12時間毎", "notes": "For anaerobic infections and GI protozoal disease", "notes_ja": "嫌気性菌感染・消化管原虫疾患に使用"},
    },
    "cephalexin": {
        "hedgehog": {"safe": True, "dosage": "25 mg/kg PO q12h", "dosage_ja": "25 mg/kg 経口 12時間毎", "notes": "First-generation cephalosporin; safe in hedgehogs", "notes_ja": "第一世代セファロスポリン。ハリネズミに安全"},
    },
    "clindamycin": {
        "hedgehog": {"safe": True, "dosage": "5.5-10 mg/kg PO q12h", "dosage_ja": "5.5-10 mg/kg 経口 12時間毎", "notes": "Good bone and dental penetration", "notes_ja": "骨・歯への移行性良好"},
    },
    "azithromycin": {
        "hedgehog": {"safe": True, "dosage": "10-30 mg/kg PO q24-48h", "dosage_ja": "10-30 mg/kg 経口 24-48時間毎", "notes": "Long half-life allows less frequent dosing", "notes_ja": "半減期が長く投与頻度を減らせる"},
    },
    "trimethoprim_sulfa": {
        "hedgehog": {"safe": True, "dosage": "30 mg/kg PO q12h", "dosage_ja": "30 mg/kg 経口 12時間毎", "notes": "Broad-spectrum; useful for UTI", "notes_ja": "広域スペクトル。尿路感染症に有用"},
    },
    "chloramphenicol": {
        "hedgehog": {"safe": True, "dosage": "50 mg/kg PO q12h", "dosage_ja": "50 mg/kg 経口 12時間毎", "notes": "Broad-spectrum alternative", "notes_ja": "広域スペクトルの代替薬"},
    },
    "gentamicin": {
        "hedgehog": {"safe": True, "dosage": "5 mg/kg SC/IM q24h", "dosage_ja": "5 mg/kg 皮下/筋注 24時間毎", "notes": "Ensure hydration; nephrotoxic", "notes_ja": "水和を確保。腎毒性あり"},
    },
    "itraconazole": {
        "hedgehog": {"safe": True, "dosage": "5-10 mg/kg PO q24h", "dosage_ja": "5-10 mg/kg 経口 24時間毎", "notes": "For dermatophytosis (Trichophyton erinacei); give with food", "notes_ja": "皮膚糸状菌症（T. erinacei）に使用。食事と投与"},
    },
    "fluconazole": {
        "hedgehog": {"safe": True, "dosage": "5-10 mg/kg PO q24h", "dosage_ja": "5-10 mg/kg 経口 24時間毎", "notes": "Alternative antifungal; good CNS penetration", "notes_ja": "代替抗真菌薬。CNS移行性良好"},
    },
    "terbinafine": {
        "hedgehog": {"safe": True, "dosage": "10-30 mg/kg PO q24h", "dosage_ja": "10-30 mg/kg 経口 24時間毎", "notes": "Very effective for hedgehog dermatophytosis", "notes_ja": "ハリネズミの皮膚糸状菌症に非常に有効"},
    },
    "ivermectin": {
        "hedgehog": {"safe": True, "dosage": "0.2-0.4 mg/kg SC; repeat in 14 days", "dosage_ja": "0.2-0.4 mg/kg 皮下; 14日後に再投与", "notes": "For Caparinia mites and other ectoparasites; 3 treatments typical", "notes_ja": "カパリニアダニ等の外部寄生虫に使用。通常3回投与"},
    },
    "fenbendazole": {
        "hedgehog": {"safe": True, "dosage": "20-50 mg/kg PO q24h for 5 days", "dosage_ja": "20-50 mg/kg 経口 24時間毎 5日間", "notes": "For intestinal helminths (Crenosoma, Capillaria)", "notes_ja": "腸管蠕虫（クレノソーマ、キャピラリア）に使用"},
    },
    "selamectin": {
        "hedgehog": {"safe": True, "dosage": "6-18 mg/kg topical once; repeat in 21-28 days", "dosage_ja": "6-18 mg/kg 外用 単回; 21-28日後に再投与", "notes": "Apply to skin between quills; effective for mites and fleas", "notes_ja": "針の間の皮膚に塗布。ダニ・ノミに有効"},
    },
    "praziquantel": {
        "hedgehog": {"safe": True, "dosage": "5-10 mg/kg PO/SC; repeat in 14 days", "dosage_ja": "5-10 mg/kg 経口/皮下; 14日後に再投与", "notes": "For cestode infections", "notes_ja": "条虫感染に使用"},
    },
    "fipronil": {
        "hedgehog": {"safe": False, "dosage": "N/A", "dosage_ja": "使用不可", "notes": "Potential toxicity in hedgehogs; avoid use", "notes_ja": "ハリネズミに毒性の可能性。使用を避ける"},
    },
    "fluralaner": {
        "hedgehog": {"safe": True, "dosage": "10-15 mg/kg PO once; repeat in 8-12 weeks", "dosage_ja": "10-15 mg/kg 経口 単回; 8-12週後に再投与", "notes": "Emerging treatment for Caparinia mites", "notes_ja": "カパリニアダニの新しい治療法"},
    },
    "carprofen": {
        "hedgehog": {"safe": True, "dosage": "1-2 mg/kg PO/SC q12-24h", "dosage_ja": "1-2 mg/kg 経口/皮下 12-24時間毎", "notes": "NSAID for post-operative and chronic pain", "notes_ja": "術後・慢性疼痛のNSAID"},
    },
    "tramadol": {
        "hedgehog": {"safe": True, "dosage": "5-10 mg/kg PO q12h", "dosage_ja": "5-10 mg/kg 経口 12時間毎", "notes": "Moderate analgesia; can be mixed with food", "notes_ja": "中等度の鎮痛。食事に混ぜて投与可能"},
    },
    "gabapentin": {
        "hedgehog": {"safe": True, "dosage": "3-5 mg/kg PO q8-12h", "dosage_ja": "3-5 mg/kg 経口 8-12時間毎", "notes": "For neuropathic pain and Wobbly Hedgehog Syndrome", "notes_ja": "神経障害性疼痛とふらつきハリネズミ症候群に使用"},
    },
    "buprenorphine": {
        "hedgehog": {"safe": True, "dosage": "0.01-0.05 mg/kg SC/IM q8-12h", "dosage_ja": "0.01-0.05 mg/kg 皮下/筋注 8-12時間毎", "notes": "Perioperative analgesia", "notes_ja": "周術期鎮痛"},
    },
    "butorphanol": {
        "hedgehog": {"safe": True, "dosage": "0.2-1 mg/kg SC/IM q4-6h", "dosage_ja": "0.2-1 mg/kg 皮下/筋注 4-6時間毎", "notes": "Short-acting opioid", "notes_ja": "短時間作用型オピオイド"},
    },
    "ketamine": {
        "hedgehog": {"safe": True, "dosage": "5-20 mg/kg IM (with medetomidine 0.05-0.1 mg/kg)", "dosage_ja": "5-20 mg/kg 筋注（メデトミジン0.05-0.1 mg/kgと併用）", "notes": "Must combine with sedative; mask induction with isoflurane often preferred", "notes_ja": "鎮静薬との併用が必須。イソフルランマスク導入が好まれることが多い"},
    },
    "alfaxalone": {
        "hedgehog": {"safe": True, "dosage": "1-3 mg/kg IM/IV", "dosage_ja": "1-3 mg/kg 筋注/静注", "notes": "Preferred injectable anesthetic for hedgehogs", "notes_ja": "ハリネズミに推奨される注射麻酔薬"},
    },
    "prednisolone": {
        "hedgehog": {"safe": True, "dosage": "0.5-2 mg/kg PO q12-24h", "dosage_ja": "0.5-2 mg/kg 経口 12-24時間毎", "notes": "Anti-inflammatory; immunosuppression risk", "notes_ja": "抗炎症。免疫抑制のリスクあり"},
    },
    "dexamethasone": {
        "hedgehog": {"safe": True, "dosage": "0.2-2 mg/kg IM/IV", "dosage_ja": "0.2-2 mg/kg 筋注/静注", "notes": "Emergency anti-inflammatory/shock therapy", "notes_ja": "緊急の抗炎症/ショック治療"},
    },
    "furosemide": {
        "hedgehog": {"safe": True, "dosage": "1-4 mg/kg PO/SC/IM q12h", "dosage_ja": "1-4 mg/kg 経口/皮下/筋注 12時間毎", "notes": "For cardiac disease and pulmonary edema", "notes_ja": "心疾患・肺水腫に使用"},
    },
    "famotidine": {
        "hedgehog": {"safe": True, "dosage": "0.5-1 mg/kg PO/SC q24h", "dosage_ja": "0.5-1 mg/kg 経口/皮下 24時間毎", "notes": "Gastric acid reduction", "notes_ja": "胃酸分泌抑制"},
    },
    "isoflurane": {
        "hedgehog": {"safe": True, "dosage": "Induction 3-5%, maintenance 1.5-3%", "dosage_ja": "導入 3-5%, 維持 1.5-3%", "notes": "Preferred method of anesthesia; chamber or mask induction", "notes_ja": "推奨される麻酔法。チャンバーまたはマスクで導入"},
    },
    "sevoflurane": {
        "hedgehog": {"safe": True, "dosage": "Induction 6-8%, maintenance 3-4.5%", "dosage_ja": "導入 6-8%, 維持 3-4.5%", "notes": "Faster recovery than isoflurane", "notes_ja": "イソフルランより回復が速い"},
    },
    "midazolam": {
        "hedgehog": {"safe": True, "dosage": "0.5-2 mg/kg IM/IN", "dosage_ja": "0.5-2 mg/kg 筋注/経鼻", "notes": "Sedation/premedication; intranasal effective for uncooperative patients", "notes_ja": "鎮静/前投薬。非協力的な患者に経鼻投与が有効"},
    },
    "diazepam": {
        "hedgehog": {"safe": True, "dosage": "0.5-2 mg/kg IM", "dosage_ja": "0.5-2 mg/kg 筋注", "notes": "Seizure control; IM absorption unreliable", "notes_ja": "痙攣管理。IM吸収は不安定"},
    },
    "atropine": {
        "hedgehog": {"safe": True, "dosage": "0.01-0.04 mg/kg SC/IM", "dosage_ja": "0.01-0.04 mg/kg 皮下/筋注", "notes": "Preanesthetic; reduce respiratory secretions", "notes_ja": "麻酔前投薬。気道分泌物の減少"},
    },
    "glycopyrrolate": {
        "hedgehog": {"safe": True, "dosage": "0.01-0.02 mg/kg SC/IM", "dosage_ja": "0.01-0.02 mg/kg 皮下/筋注", "notes": "Preferred anticholinergic for premedication", "notes_ja": "前投薬に推奨される抗コリン薬"},
    },
    "vitamin_b12": {
        "hedgehog": {"safe": True, "dosage": "0.02 mg/kg SC/IM q7d", "dosage_ja": "0.02 mg/kg 皮下/筋注 週1回", "notes": "Supportive care", "notes_ja": "支持療法"},
    },
    "vitamin_k1": {
        "hedgehog": {"safe": True, "dosage": "1-5 mg/kg SC/IM q24h", "dosage_ja": "1-5 mg/kg 皮下/筋注 24時間毎", "notes": "For coagulopathy", "notes_ja": "凝固障害に使用"},
    },
    "sucralfate": {
        "hedgehog": {"safe": True, "dosage": "25-50 mg/kg PO q8-12h", "dosage_ja": "25-50 mg/kg 経口 8-12時間毎", "notes": "Gastric protection", "notes_ja": "胃保護"},
    },
    "omeprazole": {
        "hedgehog": {"safe": True, "dosage": "4 mg/kg PO q24h", "dosage_ja": "4 mg/kg 経口 24時間毎", "notes": "Proton pump inhibitor for gastric ulcers", "notes_ja": "胃潰瘍に対するプロトンポンプ阻害薬"},
    },
    "lactulose": {
        "hedgehog": {"safe": True, "dosage": "0.5 mL/kg PO q8-12h", "dosage_ja": "0.5 mL/kg 経口 8-12時間毎", "notes": "For hepatic encephalopathy or constipation", "notes_ja": "肝性脳症または便秘に使用"},
    },
    "iron_dextran": {
        "hedgehog": {"safe": True, "dosage": "10 mg/kg IM once", "dosage_ja": "10 mg/kg 筋注 単回", "notes": "For iron deficiency anemia", "notes_ja": "鉄欠乏性貧血に使用"},
    },
    # ==================================================================
    # Chinchilla (チンチラ) — ~45 drugs
    # ==================================================================
    "amoxicillin_clavulanate": {
        "chinchilla": {"safe": False, "dosage": "N/A", "dosage_ja": "使用不可", "notes": "Oral penicillins/cephalosporins cause fatal dysbiosis in chinchillas", "notes_ja": "経口ペニシリン/セファロスポリンはチンチラに致死的な腸内細菌叢の破壊を起こす"},
    },
    "doxycycline": {
        "chinchilla": {"safe": True, "dosage": "5-10 mg/kg PO q12h", "dosage_ja": "5-10 mg/kg 経口 12時間毎", "notes": "Safe broad-spectrum option for chinchillas", "notes_ja": "チンチラに安全な広域スペクトル抗菌薬"},
    },
    "metronidazole": {
        "chinchilla": {"safe": True, "dosage": "10-20 mg/kg PO q12h", "dosage_ja": "10-20 mg/kg 経口 12時間毎", "notes": "For anaerobic infections and Giardia", "notes_ja": "嫌気性菌感染・ジアルジアに使用"},
    },
    "cephalexin": {
        "chinchilla": {"safe": False, "dosage": "N/A", "dosage_ja": "使用不可", "notes": "Oral cephalosporins cause fatal dysbiosis", "notes_ja": "経口セファロスポリンは致死的な腸内細菌叢の破壊を起こす"},
    },
    "marbofloxacin": {
        "chinchilla": {"safe": True, "dosage": "5 mg/kg PO q24h", "dosage_ja": "5 mg/kg 経口 24時間毎", "notes": "Fluoroquinolone; safe for chinchillas", "notes_ja": "フルオロキノロン系。チンチラに安全"},
    },
    "clindamycin": {
        "chinchilla": {"safe": False, "dosage": "N/A", "dosage_ja": "使用不可", "notes": "Risk of fatal dysbiosis; avoid in chinchillas", "notes_ja": "致死的な腸内細菌叢破壊のリスク。チンチラには使用しない"},
    },
    "azithromycin": {
        "chinchilla": {"safe": True, "dosage": "15-30 mg/kg PO q24h", "dosage_ja": "15-30 mg/kg 経口 24時間毎", "notes": "Safe macrolide for respiratory infections", "notes_ja": "呼吸器感染症に安全なマクロライド"},
    },
    "trimethoprim_sulfa": {
        "chinchilla": {"safe": True, "dosage": "15-30 mg/kg PO q12h", "dosage_ja": "15-30 mg/kg 経口 12時間毎", "notes": "Well-tolerated broad-spectrum option", "notes_ja": "忍容性の良い広域スペクトル抗菌薬"},
    },
    "chloramphenicol": {
        "chinchilla": {"safe": True, "dosage": "30-50 mg/kg PO q12h", "dosage_ja": "30-50 mg/kg 経口 12時間毎", "notes": "Broad-spectrum; safe alternative to penicillins", "notes_ja": "広域スペクトル。ペニシリンの安全な代替"},
    },
    "gentamicin": {
        "chinchilla": {"safe": True, "dosage": "5 mg/kg SC/IM q24h", "dosage_ja": "5 mg/kg 皮下/筋注 24時間毎", "notes": "Monitor for nephrotoxicity", "notes_ja": "腎毒性に注意"},
    },
    "penicillin_g": {
        "chinchilla": {"safe": True, "dosage": "22,000-44,000 IU/kg SC/IM q24h", "dosage_ja": "22,000-44,000 IU/kg 皮下/筋注 24時間毎", "notes": "Injectable penicillin is safe; NEVER give oral penicillin", "notes_ja": "注射用ペニシリンは安全。経口ペニシリンは絶対に投与しない"},
    },
    "itraconazole": {
        "chinchilla": {"safe": True, "dosage": "5-10 mg/kg PO q24h", "dosage_ja": "5-10 mg/kg 経口 24時間毎", "notes": "For dermatophytosis; give with food", "notes_ja": "皮膚糸状菌症に使用。食事と投与"},
    },
    "fluconazole": {
        "chinchilla": {"safe": True, "dosage": "5-10 mg/kg PO q24h", "dosage_ja": "5-10 mg/kg 経口 24時間毎", "notes": "Alternative antifungal", "notes_ja": "代替抗真菌薬"},
    },
    "terbinafine": {
        "chinchilla": {"safe": True, "dosage": "10-30 mg/kg PO q24h", "dosage_ja": "10-30 mg/kg 経口 24時間毎", "notes": "Effective for Trichophyton mentagrophytes", "notes_ja": "トリコフィトン・メンタグロフィテスに有効"},
    },
    "griseofulvin": {
        "chinchilla": {"safe": True, "dosage": "25 mg/kg PO q24h for 6-8 weeks", "dosage_ja": "25 mg/kg 経口 24時間毎 6-8週間", "notes": "Teratogenic; do not use in pregnant animals", "notes_ja": "催奇形性あり。妊娠個体には使用しない"},
    },
    "ivermectin": {
        "chinchilla": {"safe": True, "dosage": "0.2-0.4 mg/kg SC; repeat in 14 days", "dosage_ja": "0.2-0.4 mg/kg 皮下; 14日後に再投与", "notes": "For fur mites and other ectoparasites", "notes_ja": "毛ダニ等の外部寄生虫に使用"},
    },
    "selamectin": {
        "chinchilla": {"safe": True, "dosage": "15-30 mg/kg topical; repeat in 21-28 days", "dosage_ja": "15-30 mg/kg 外用; 21-28日後に再投与", "notes": "Apply to skin on dorsal neck area", "notes_ja": "背部頸部の皮膚に塗布"},
    },
    "fenbendazole": {
        "chinchilla": {"safe": True, "dosage": "20-50 mg/kg PO q24h for 5 days", "dosage_ja": "20-50 mg/kg 経口 24時間毎 5日間", "notes": "For Giardia and intestinal helminths", "notes_ja": "ジアルジア・腸管蠕虫に使用"},
    },
    "praziquantel": {
        "chinchilla": {"safe": True, "dosage": "5-10 mg/kg PO/SC; repeat in 14 days", "dosage_ja": "5-10 mg/kg 経口/皮下; 14日後に再投与", "notes": "For cestode infections", "notes_ja": "条虫感染に使用"},
    },
    "carprofen": {
        "chinchilla": {"safe": True, "dosage": "4 mg/kg SC q24h", "dosage_ja": "4 mg/kg 皮下 24時間毎", "notes": "NSAID; short-term use", "notes_ja": "NSAID。短期使用"},
    },
    "tramadol": {
        "chinchilla": {"safe": True, "dosage": "5-10 mg/kg PO q12h", "dosage_ja": "5-10 mg/kg 経口 12時間毎", "notes": "Moderate analgesia", "notes_ja": "中等度の鎮痛"},
    },
    "gabapentin": {
        "chinchilla": {"safe": True, "dosage": "3-5 mg/kg PO q8-12h", "dosage_ja": "3-5 mg/kg 経口 8-12時間毎", "notes": "Neuropathic pain; may cause sedation", "notes_ja": "神経障害性疼痛。鎮静を生じうる"},
    },
    "buprenorphine": {
        "chinchilla": {"safe": True, "dosage": "0.05 mg/kg SC q8-12h", "dosage_ja": "0.05 mg/kg 皮下 8-12時間毎", "notes": "Perioperative analgesia", "notes_ja": "周術期鎮痛"},
    },
    "butorphanol": {
        "chinchilla": {"safe": True, "dosage": "0.5-2 mg/kg SC q4-6h", "dosage_ja": "0.5-2 mg/kg 皮下 4-6時間毎", "notes": "Short-acting opioid", "notes_ja": "短時間作用型オピオイド"},
    },
    "ketamine": {
        "chinchilla": {"safe": True, "dosage": "20-40 mg/kg IM (with xylazine 2-5 mg/kg)", "dosage_ja": "20-40 mg/kg 筋注（キシラジン2-5 mg/kgと併用）", "notes": "Combine with sedative for adequate depth", "notes_ja": "十分な深度のため鎮静薬と併用"},
    },
    "alfaxalone": {
        "chinchilla": {"safe": True, "dosage": "5-8 mg/kg IM", "dosage_ja": "5-8 mg/kg 筋注", "notes": "Smoother recovery vs ketamine combos", "notes_ja": "ケタミン併用より回復が良好"},
    },
    "prednisolone": {
        "chinchilla": {"safe": True, "dosage": "0.5-2 mg/kg PO q12-24h", "dosage_ja": "0.5-2 mg/kg 経口 12-24時間毎", "notes": "Anti-inflammatory; use cautiously", "notes_ja": "抗炎症。慎重投与"},
    },
    "dexamethasone": {
        "chinchilla": {"safe": True, "dosage": "0.5-2 mg/kg IM/SC", "dosage_ja": "0.5-2 mg/kg 筋注/皮下", "notes": "Emergency anti-inflammatory", "notes_ja": "緊急の抗炎症"},
    },
    "furosemide": {
        "chinchilla": {"safe": True, "dosage": "1-4 mg/kg PO/SC/IM q12h", "dosage_ja": "1-4 mg/kg 経口/皮下/筋注 12時間毎", "notes": "For cardiac disease and edema", "notes_ja": "心疾患・浮腫に使用"},
    },
    "famotidine": {
        "chinchilla": {"safe": True, "dosage": "0.5-1 mg/kg PO q24h", "dosage_ja": "0.5-1 mg/kg 経口 24時間毎", "notes": "Gastric acid reduction", "notes_ja": "胃酸分泌抑制"},
    },
    "metoclopramide": {
        "chinchilla": {"safe": True, "dosage": "0.5 mg/kg PO/SC q8-12h", "dosage_ja": "0.5 mg/kg 経口/皮下 8-12時間毎", "notes": "Prokinetic for GI stasis", "notes_ja": "消化管うっ滞の運動促進薬"},
    },
    "lactulose": {
        "chinchilla": {"safe": True, "dosage": "0.5 mL/kg PO q8-12h", "dosage_ja": "0.5 mL/kg 経口 8-12時間毎", "notes": "For constipation; adjust to stool consistency", "notes_ja": "便秘に使用。便の硬さに応じて調整"},
    },
    "isoflurane": {
        "chinchilla": {"safe": True, "dosage": "Induction 3-5%, maintenance 1.5-3%", "dosage_ja": "導入 3-5%, 維持 1.5-3%", "notes": "Standard inhalant anesthetic; mask induction", "notes_ja": "標準的吸入麻酔薬。マスクで導入"},
    },
    "sevoflurane": {
        "chinchilla": {"safe": True, "dosage": "Induction 6-8%, maintenance 3-4.5%", "dosage_ja": "導入 6-8%, 維持 3-4.5%", "notes": "Faster recovery than isoflurane", "notes_ja": "イソフルランより回復が速い"},
    },
    "midazolam": {
        "chinchilla": {"safe": True, "dosage": "0.5-2 mg/kg IM/IN", "dosage_ja": "0.5-2 mg/kg 筋注/経鼻", "notes": "Sedation/premedication", "notes_ja": "鎮静/前投薬"},
    },
    "diazepam": {
        "chinchilla": {"safe": True, "dosage": "0.5-3 mg/kg IM", "dosage_ja": "0.5-3 mg/kg 筋注", "notes": "Seizure control", "notes_ja": "痙攣管理"},
    },
    "atropine": {
        "chinchilla": {"safe": True, "dosage": "0.05 mg/kg SC/IM", "dosage_ja": "0.05 mg/kg 皮下/筋注", "notes": "Preanesthetic anticholinergic", "notes_ja": "麻酔前投薬の抗コリン薬"},
    },
    "glycopyrrolate": {
        "chinchilla": {"safe": True, "dosage": "0.01-0.02 mg/kg SC/IM", "dosage_ja": "0.01-0.02 mg/kg 皮下/筋注", "notes": "Preferred anticholinergic", "notes_ja": "推奨される抗コリン薬"},
    },
    "sucralfate": {
        "chinchilla": {"safe": True, "dosage": "25-50 mg/kg PO q8-12h", "dosage_ja": "25-50 mg/kg 経口 8-12時間毎", "notes": "Gastric protection", "notes_ja": "胃保護"},
    },
    "vitamin_b12": {
        "chinchilla": {"safe": True, "dosage": "0.02 mg/kg SC/IM q7d", "dosage_ja": "0.02 mg/kg 皮下/筋注 週1回", "notes": "Supportive care", "notes_ja": "支持療法"},
    },
    "vitamin_k1": {
        "chinchilla": {"safe": True, "dosage": "1-10 mg/kg SC/IM q24h", "dosage_ja": "1-10 mg/kg 皮下/筋注 24時間毎", "notes": "For coagulopathy/rodenticide toxicity", "notes_ja": "凝固障害/殺鼠剤中毒に使用"},
    },
}
