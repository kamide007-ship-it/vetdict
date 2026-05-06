"""drug_batch_28.py - 動物種カバレッジ拡張パッチ

既存薬品にエキゾチック動物種の投与量情報を追加。
Carpenter's Exotic Animal Formulary 6th ed. / BSAVA Manual of Exotic Pets 参照。
"""

SPECIES_INFO_PATCH_28: dict[str, dict[str, dict]] = {
    "gabapentin_oral": {
        "rabbit": {"dose": "5-20 mg/kg PO q8-12h", "notes": "For neuropathic pain and adjunctive seizure control", "notes_ja": "神経障害性疼痛および補助的な発作コントロールに"},
        "guinea_pig": {"dose": "5-10 mg/kg PO q12h", "notes": "For pain management; musculoskeletal conditions", "notes_ja": "疼痛管理に；筋骨格系疾患"},
        "ferret": {"dose": "3-5 mg/kg PO q8-12h", "notes": "For neuropathic pain; insulinoma-associated neuropathy", "notes_ja": "神経障害性疼痛に；インスリノーマ関連神経障害"},
        "bird": {"dose": "10-25 mg/kg PO q8-12h", "notes": "For chronic pain in avian species", "notes_ja": "鳥類の慢性疼痛に"},
        "reptile": {"dose": "5-10 mg/kg PO q24-72h", "notes": "Limited data; temperature-dependent pharmacokinetics", "notes_ja": "データ限定的；温度依存性の薬物動態"}
    },
    "metoclopramide": {
        "rabbit": {"dose": "0.5-1 mg/kg PO/SC q8-12h", "notes": "For GI stasis; combine with cisapride for better motility", "notes_ja": "消化管うっ滞に；シサプリドと併用でより良い消化管運動促進"},
        "guinea_pig": {"dose": "0.5 mg/kg PO/SC q8h", "notes": "For post-anesthetic ileus and GI stasis", "notes_ja": "麻酔後イレウスおよび消化管うっ滞に"},
        "ferret": {"dose": "0.2-1 mg/kg PO/SC q6-8h", "notes": "For nausea and gastric motility disorders", "notes_ja": "悪心および胃運動障害に"},
        "bird": {"dose": "0.5-1 mg/kg PO/IM q8-12h", "notes": "For crop stasis and vomiting in psittacines", "notes_ja": "オウム目の素嚢うっ滞および嘔吐に"},
        "hedgehog": {"dose": "0.5-1 mg/kg PO/SC q8h", "notes": "For GI motility support", "notes_ja": "消化管運動支持に"}
    },
    "famotidine": {
        "rabbit": {"dose": "0.5-1 mg/kg PO/SC q12-24h", "notes": "For gastric ulcer prevention; safer than omeprazole in rabbits", "notes_ja": "胃潰瘍予防に；ウサギではオメプラゾールより安全"},
        "guinea_pig": {"dose": "0.5 mg/kg PO/SC q12h", "notes": "For gastric ulcer prevention during NSAID therapy", "notes_ja": "NSAID療法中の胃潰瘍予防に"},
        "ferret": {"dose": "0.25-0.5 mg/kg PO/SC/IV q12-24h", "notes": "For Helicobacter-associated gastritis", "notes_ja": "ヘリコバクター関連胃炎に"},
        "chinchilla": {"dose": "0.5 mg/kg PO q12h", "notes": "For stress-related GI ulceration", "notes_ja": "ストレス関連消化管潰瘍に"},
        "hedgehog": {"dose": "0.5 mg/kg PO q12-24h", "notes": "For suspected gastric ulceration", "notes_ja": "胃潰瘍疑い例に"}
    },
    "sucralfate": {
        "rabbit": {"dose": "25-100 mg/kg PO q8-12h", "notes": "For gastric ulcer treatment; give 1h before other medications", "notes_ja": "胃潰瘍治療に；他の薬の1時間前に投与"},
        "guinea_pig": {"dose": "25-50 mg/kg PO q8-12h", "notes": "GI mucosal protectant", "notes_ja": "消化管粘膜保護薬"},
        "ferret": {"dose": "25 mg/kg PO q8h", "notes": "For Helicobacter gastritis and GI ulcers", "notes_ja": "ヘリコバクター胃炎および消化管潰瘍に"},
        "bird": {"dose": "25 mg/kg PO q8h", "notes": "For proventricular/ventricular ulceration", "notes_ja": "前胃/筋胃潰瘍に"},
        "hedgehog": {"dose": "25-50 mg/kg PO q8h", "notes": "For suspected GI ulceration", "notes_ja": "消化管潰瘍疑い例に"}
    },
    "enrofloxacin": {
        "rabbit": {"dose": "5-20 mg/kg PO/SC/IM q12-24h", "notes": "Safe fluoroquinolone for rabbits; first-line for Pasteurella", "notes_ja": "ウサギに安全なフルオロキノロン；パスツレラの第一選択"},
        "guinea_pig": {"dose": "5-10 mg/kg PO/SC q12h", "notes": "For respiratory and urinary infections", "notes_ja": "呼吸器・泌尿器感染に"},
        "chinchilla": {"dose": "5-15 mg/kg PO/SC q12h", "notes": "For respiratory infections", "notes_ja": "呼吸器感染に"},
        "ferret": {"dose": "5-10 mg/kg PO/IM q12h", "notes": "Broad-spectrum; avoid in young ferrets", "notes_ja": "広域スペクトル；若齢フェレットには避ける"},
        "hedgehog": {"dose": "5-10 mg/kg PO/SC q12h", "notes": "For skin and respiratory infections", "notes_ja": "皮膚・呼吸器感染に"},
        "bird": {"dose": "15-30 mg/kg PO/IM q12h", "notes": "Higher dose required in avians; avoid in young growing birds", "notes_ja": "鳥類では高用量必要；成長期の幼鳥には避ける"},
        "reptile": {"dose": "5-10 mg/kg PO/IM q24-48h", "notes": "Temperature-dependent; maintain in POTZ", "notes_ja": "温度依存性；POTZを維持"},
        "tortoise": {"dose": "5-10 mg/kg IM q48h", "notes": "Excellent for respiratory infections in chelonians", "notes_ja": "カメ類の呼吸器感染に優れている"},
        "snake": {"dose": "5-10 mg/kg PO/IM q48h", "notes": "For pneumonia and stomatitis", "notes_ja": "肺炎および口内炎に"},
        "amphibian": {"dose": "5-10 mg/kg PO/IM q24h or bath 5 mg/L × 6h", "notes": "Systemic or bath administration", "notes_ja": "全身投与または薬浴"}
    },
    "metronidazole": {
        "rabbit": {"dose": "20-40 mg/kg PO q12h", "notes": "For anaerobic infections and giardia; avoid prolonged use (neurotoxicity)", "notes_ja": "嫌気性感染およびジアルジアに；長期使用は避ける（神経毒性）"},
        "guinea_pig": {"dose": "20-25 mg/kg PO q12h", "notes": "For anaerobic infections and protozoal enteritis", "notes_ja": "嫌気性感染および原虫性腸炎に"},
        "chinchilla": {"dose": "20-25 mg/kg PO q12h", "notes": "For giardia and anaerobic infections", "notes_ja": "ジアルジアおよび嫌気性感染に"},
        "ferret": {"dose": "15-20 mg/kg PO q12h", "notes": "For Helicobacter (with amoxicillin+bismuth) and IBD", "notes_ja": "ヘリコバクター（アモキシシリン+ビスマスと）およびIBDに"},
        "hedgehog": {"dose": "20-25 mg/kg PO q12h", "notes": "For protozoal and anaerobic infections", "notes_ja": "原虫および嫌気性感染に"},
        "bird": {"dose": "25-50 mg/kg PO q12h", "notes": "For trichomonas and anaerobic infections", "notes_ja": "トリコモナスおよび嫌気性感染に"},
        "reptile": {"dose": "20-50 mg/kg PO q24-48h", "notes": "For flagellate protozoal infections; adjust for temperature", "notes_ja": "鞭毛虫感染に；温度に応じて調整"}
    },
    "doxycycline": {
        "rabbit": {"dose": "2.5-5 mg/kg PO q12h", "notes": "For Pasteurella and Mycoplasma; well-tolerated in rabbits", "notes_ja": "パスツレラおよびマイコプラズマに；ウサギで忍容性良好"},
        "guinea_pig": {"dose": "2.5-5 mg/kg PO q12h", "notes": "For respiratory infections; antibiotic of choice with enrofloxacin", "notes_ja": "呼吸器感染に；エンロフロキサシンとともに第一選択"},
        "ferret": {"dose": "5-10 mg/kg PO q12h", "notes": "For respiratory and rickettsial infections", "notes_ja": "呼吸器およびリケッチア感染に"},
        "hedgehog": {"dose": "5-10 mg/kg PO q12h", "notes": "For skin and respiratory infections", "notes_ja": "皮膚・呼吸器感染に"},
        "bird": {"dose": "25-50 mg/kg PO q12-24h", "notes": "Drug of choice for Chlamydia psittaci (psittacosis); 45-day course", "notes_ja": "クラミジア・シッタシ（オウム病）の第一選択薬；45日間投与"},
        "reptile": {"dose": "5-10 mg/kg PO q24-48h", "notes": "For Mycoplasma and respiratory infections", "notes_ja": "マイコプラズマおよび呼吸器感染に"}
    },
    "amoxicillin_clavulanate": {
        "rabbit": {"dose": "12.5-25 mg/kg PO q12h (ORAL ONLY—never inject penicillins in rabbits)", "notes": "CAUTION: Only use if no safer alternative; risk of dysbiosis", "notes_ja": "注意: より安全な代替薬がない場合のみ使用；腸内細菌叢障害のリスク"},
        "guinea_pig": {"dose": "12.5-25 mg/kg PO q12h", "notes": "CAUTION: Penicillins risky in guinea pigs; monitor for dysbiosis", "notes_ja": "注意: モルモットではペニシリン系リスクあり；腸内細菌叢障害を監視"},
        "ferret": {"dose": "12.5-25 mg/kg PO q12h", "notes": "Safe in ferrets; for skin, dental, and GI infections", "notes_ja": "フェレットでは安全；皮膚、歯科、消化管感染に"},
        "bird": {"dose": "125 mg/kg PO q12h", "notes": "For gram-positive and mixed infections in psittacines", "notes_ja": "オウム目のグラム陽性菌および混合感染に"}
    },
    "azithromycin": {
        "rabbit": {"dose": "15-30 mg/kg PO q24h", "notes": "Safe macrolide for rabbits (unlike erythromycin); for Pasteurella", "notes_ja": "ウサギに安全なマクロライド（エリスロマイシンとは異なり）；パスツレラに"},
        "guinea_pig": {"dose": "15-30 mg/kg PO q24h", "notes": "For Bordetella and upper respiratory infections", "notes_ja": "ボルデテラおよび上部気道感染に"},
        "ferret": {"dose": "5-10 mg/kg PO q24h", "notes": "For respiratory infections and Helicobacter", "notes_ja": "呼吸器感染およびヘリコバクターに"},
        "hedgehog": {"dose": "10-15 mg/kg PO q24h", "notes": "For respiratory and skin infections", "notes_ja": "呼吸器・皮膚感染に"},
        "bird": {"dose": "40-50 mg/kg PO q24h", "notes": "For Chlamydia (alternative to doxycycline) and Mycobacterium", "notes_ja": "クラミジア（ドキシサイクリンの代替）およびマイコバクテリウムに"},
        "reptile": {"dose": "10 mg/kg PO q48-72h", "notes": "Long tissue half-life; good for respiratory infections", "notes_ja": "組織半減期が長い；呼吸器感染に良好"}
    },
    "itraconazole_oral": {
        "rabbit": {"dose": "5-10 mg/kg PO q24h", "notes": "For dermatophytosis and systemic mycoses", "notes_ja": "皮膚糸状菌症および全身性真菌症に"},
        "guinea_pig": {"dose": "5-10 mg/kg PO q24h", "notes": "For dermatophytosis (Trichophyton mentagrophytes)", "notes_ja": "皮膚糸状菌症（T. mentagrophytes）に"},
        "ferret": {"dose": "5-10 mg/kg PO q24h", "notes": "For systemic mycoses", "notes_ja": "全身性真菌症に"},
        "bird": {"dose": "5-10 mg/kg PO q12-24h", "notes": "Drug of choice for aspergillosis in birds", "notes_ja": "鳥のアスペルギルス症の第一選択薬"},
        "reptile": {"dose": "5-10 mg/kg PO q24-48h", "notes": "For CANV and other systemic mycoses; long courses needed", "notes_ja": "CANVおよびその他の全身性真菌症に；長期投与が必要"}
    },
    "fluconazole_oral": {
        "rabbit": {"dose": "5-14 mg/kg PO q24h", "notes": "For systemic candidiasis and CNS fungal infections (good CSF penetration)", "notes_ja": "全身性カンジダ症およびCNS真菌感染に（良好なCSF移行性）"},
        "guinea_pig": {"dose": "5-10 mg/kg PO q24h", "notes": "For yeast infections and dermatophytosis adjunct", "notes_ja": "酵母感染および皮膚糸状菌症の補助療法に"},
        "bird": {"dose": "5-15 mg/kg PO q24h", "notes": "For candidiasis and macrorhabdus (megabacteria); water-soluble", "notes_ja": "カンジダ症およびマクロラブダス（メガバクテリア）に；水溶性"},
        "reptile": {"dose": "5-10 mg/kg PO q48-72h", "notes": "For systemic mycoses in reptiles", "notes_ja": "爬虫類の全身性真菌症に"}
    },
    "prednisolone": {
        "rabbit": {"dose": "0.5-2 mg/kg PO/IM q12-24h (short course only)", "notes": "Use with extreme caution in rabbits; immunosuppression risk high", "notes_ja": "ウサギでは極めて慎重に使用；免疫抑制リスクが高い"},
        "guinea_pig": {"dose": "0.5-1 mg/kg PO/IM q12-24h", "notes": "Short courses only; GI dysbiosis risk with immunosuppression", "notes_ja": "短期投与のみ；免疫抑制による腸内細菌叢障害リスク"},
        "ferret": {"dose": "0.5-2.5 mg/kg PO q12-24h", "notes": "For insulinoma management and lymphoma; may worsen adrenal disease", "notes_ja": "インスリノーマ管理およびリンパ腫に；副腎疾患を悪化させる可能性"},
        "bird": {"dose": "0.5-1 mg/kg PO/IM q12h (short course)", "notes": "Immunosuppression dangerous in birds; use short courses only", "notes_ja": "鳥では免疫抑制が危険；短期投与のみ"},
        "reptile": {"dose": "2-5 mg/kg IM once, then 1-2 mg/kg q24-48h", "notes": "Limited use in reptiles; for severe inflammation only", "notes_ja": "爬虫類での使用は限定的；重度の炎症にのみ"}
    },
    "furosemide_injectable": {
        "rabbit": {"dose": "1-4 mg/kg IV/IM/SC q4-12h", "notes": "For pulmonary edema and ascites", "notes_ja": "肺水腫および腹水に"},
        "guinea_pig": {"dose": "1-4 mg/kg SC/IM q12h", "notes": "For congestive heart failure and fluid overload", "notes_ja": "うっ血性心不全および体液過負荷に"},
        "ferret": {"dose": "1-4 mg/kg PO/SC/IM/IV q8-12h", "notes": "For cardiomyopathy-related CHF", "notes_ja": "心筋症関連うっ血性心不全に"},
        "bird": {"dose": "0.15-2 mg/kg IM q12-24h", "notes": "For avian CHF and ascites; use cautiously (dehydration risk)", "notes_ja": "鳥のうっ血性心不全および腹水に；慎重に使用（脱水リスク）"},
        "reptile": {"dose": "2-5 mg/kg IM/SC q12-24h", "notes": "For edema and coelomic effusion", "notes_ja": "浮腫および体腔液貯留に"}
    },
    "phenobarbital_oral": {
        "rabbit": {"dose": "1-2 mg/kg PO q12h", "notes": "For seizure management in rabbits (E. cuniculi-related)", "notes_ja": "ウサギの痙攣管理に（E.クニクリ関連）"},
        "ferret": {"dose": "1-2 mg/kg PO q12h", "notes": "For seizures; monitor liver values", "notes_ja": "痙攣に；肝機能値をモニタリング"}
    },
    "diazepam": {
        "rabbit": {"dose": "1-3 mg/kg IV/IM; 0.5-2 mg/kg intranasal", "notes": "For seizure emergencies and sedation; intranasal effective", "notes_ja": "痙攣緊急時および鎮静に；経鼻投与が有効"},
        "guinea_pig": {"dose": "0.5-3 mg/kg IM", "notes": "For seizures and as muscle relaxant", "notes_ja": "痙攣および筋弛緩薬として"},
        "ferret": {"dose": "0.5-1 mg/kg IV/IM", "notes": "For seizure emergencies", "notes_ja": "痙攣緊急時に"},
        "bird": {"dose": "0.5-1 mg/kg IM/IV", "notes": "For seizures in birds; short-acting", "notes_ja": "鳥の痙攣に；短時間作用型"},
        "reptile": {"dose": "0.5-2.5 mg/kg IM/IV", "notes": "For seizures; slow onset in ectotherms", "notes_ja": "痙攣に；変温動物では発現が遅い"}
    },
    "acepromazine": {
        "rabbit": {"dose": "0.25-1 mg/kg SC/IM", "notes": "For pre-anesthetic sedation; avoid in hypotensive patients", "notes_ja": "麻酔前鎮静に；低血圧の患者では避ける"},
        "guinea_pig": {"dose": "0.5-1 mg/kg IM", "notes": "For mild sedation; rarely used alone", "notes_ja": "軽度鎮静に；単独使用は稀"},
        "ferret": {"dose": "0.1-0.25 mg/kg IM/SC", "notes": "For sedation; combine with opioid for procedures", "notes_ja": "鎮静に；処置時はオピオイドと併用"},
        "bird": {"dose": "Not recommended", "notes": "Unpredictable in avian species; severe hypotension risk", "notes_ja": "鳥類では効果が予測不能；重度の低血圧リスク"}
    },
    "omeprazole_oral": {
        "rabbit": {"dose": "0.5-1 mg/kg PO q24h", "notes": "For gastric ulcers; less data than famotidine in rabbits", "notes_ja": "胃潰瘍に；ウサギではファモチジンよりデータが少ない"},
        "ferret": {"dose": "1-4 mg/kg PO q24h", "notes": "For Helicobacter gastritis (triple therapy component)", "notes_ja": "ヘリコバクター胃炎に（3剤併用療法の構成薬）"}
    },
    "pimobendan_oral": {
        "ferret": {"dose": "0.5-1.25 mg/kg PO q12h", "notes": "For dilated cardiomyopathy in ferrets", "notes_ja": "フェレットの拡張型心筋症に"},
        "rabbit": {"dose": "0.1-0.3 mg/kg PO q12h", "notes": "Limited data; for congestive heart failure", "notes_ja": "データ限定的；うっ血性心不全に"}
    },
}
