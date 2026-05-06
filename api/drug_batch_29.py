"""drug_batch_29.py - エキゾチック種カバレッジ拡張パッチ（第2弾）

デグー、インコ、オウム、トカゲ、両生類、フクロモモンガ、ヘビ、リクガメ等の
投与量情報を既存薬品に追加。
Carpenter's Exotic Animal Formulary 6th ed. 参照。
"""

SPECIES_INFO_PATCH_29: dict[str, dict[str, dict]] = {
    "enrofloxacin": {
        "degu": {
            "dose": "5-10 mg/kg PO/SC q12h",
            "notes": "For respiratory and urinary infections",
            "notes_ja": "呼吸器・泌尿器感染に",
        },
        "lizard": {
            "dose": "5-10 mg/kg PO/IM q24-48h",
            "notes": "Temperature-dependent PK; maintain in POTZ",
            "notes_ja": "温度依存性の薬物動態；POTZを維持",
        },
        "parakeet": {
            "dose": "15-30 mg/kg PO/IM q12h",
            "notes": "For gram-negative infections; avoid in young growing birds",
            "notes_ja": "グラム陰性菌感染に；成長期の幼鳥には避ける",
        },
        "parrot": {
            "dose": "15-30 mg/kg PO/IM q12h",
            "notes": "For gram-negative infections; excellent tissue penetration",
            "notes_ja": "グラム陰性菌感染に；優れた組織移行性",
        },
    },
    "metronidazole": {
        "amphibian": {
            "dose": "50 mg/kg PO q14 days or 10 mg/L bath × 6h",
            "notes": "For flagellate protozoa; bath administration preferred for small species",
            "notes_ja": "鞭毛虫に；小型種では薬浴投与が望ましい",
        },
        "degu": {
            "dose": "20 mg/kg PO q12h",
            "notes": "For anaerobic and protozoal infections",
            "notes_ja": "嫌気性菌・原虫感染に",
        },
        "lizard": {
            "dose": "20-50 mg/kg PO q24-48h",
            "notes": "For flagellate protozoa (Entamoeba, Hexamita)",
            "notes_ja": "鞭毛虫（エンタメーバ、ヘキサミタ）に",
        },
        "parakeet": {
            "dose": "25-50 mg/kg PO q12h",
            "notes": "For trichomonas and anaerobic infections",
            "notes_ja": "トリコモナスおよび嫌気性感染に",
        },
        "parrot": {
            "dose": "25-50 mg/kg PO q12h",
            "notes": "For trichomonas and anaerobic infections",
            "notes_ja": "トリコモナスおよび嫌気性感染に",
        },
    },
    "doxycycline": {
        "amphibian": {
            "dose": "5 mg/kg PO q24h or 5 mg/L bath × 6h",
            "notes": "For bacterial skin infections; maintain skin moisture",
            "notes_ja": "細菌性皮膚感染に；皮膚の湿潤を維持",
        },
        "degu": {
            "dose": "2.5-5 mg/kg PO q12h",
            "notes": "For respiratory infections",
            "notes_ja": "呼吸器感染に",
        },
        "lizard": {
            "dose": "5-10 mg/kg PO q24-48h",
            "notes": "For Mycoplasma and respiratory infections",
            "notes_ja": "マイコプラズマおよび呼吸器感染に",
        },
        "parakeet": {
            "dose": "25-50 mg/kg PO q24h",
            "notes": "Drug of choice for Chlamydia psittaci (psittacosis); 45-day course",
            "notes_ja": "クラミジア・シッタシ（オウム病）の第一選択薬；45日間投与",
        },
        "parrot": {
            "dose": "25-50 mg/kg PO q24h",
            "notes": "Drug of choice for Chlamydia psittaci; 45-day course; injectable available",
            "notes_ja": "クラミジア・シッタシの第一選択薬；45日間投与；注射製剤あり",
        },
    },
    "azithromycin": {
        "degu": {
            "dose": "10-15 mg/kg PO q24h",
            "notes": "For respiratory infections; long tissue half-life",
            "notes_ja": "呼吸器感染に；組織半減期が長い",
        },
        "parakeet": {
            "dose": "40-50 mg/kg PO q24h",
            "notes": "Alternative for Chlamydia; good for Mycobacterium",
            "notes_ja": "クラミジアの代替薬；マイコバクテリウムに有効",
        },
        "parrot": {
            "dose": "40-50 mg/kg PO q24h",
            "notes": "For Chlamydia (alternative to doxycycline) and Mycobacterium",
            "notes_ja": "クラミジア（ドキシサイクリンの代替）およびマイコバクテリウムに",
        },
        "snake": {
            "dose": "10 mg/kg PO q48-72h",
            "notes": "For Mycoplasma and upper respiratory infections",
            "notes_ja": "マイコプラズマおよび上部気道感染に",
        },
        "sugar_glider": {
            "dose": "10-15 mg/kg PO q24h",
            "notes": "For respiratory infections; safer than erythromycin",
            "notes_ja": "呼吸器感染に；エリスロマイシンより安全",
        },
        "tortoise": {
            "dose": "10 mg/kg PO q48-72h",
            "notes": "For Mycoplasma (URTD) in tortoises; long half-life allows infrequent dosing",
            "notes_ja": "リクガメのマイコプラズマ（URTD）に；長い半減期で投与間隔を延長可能",
        },
    },
    "amoxicillin_clavulanate": {
        "degu": {
            "dose": "12.5-25 mg/kg PO q12h",
            "notes": "CAUTION: Risk of dysbiosis in hindgut fermenters; monitor closely",
            "notes_ja": "注意: 後腸発酵動物で腸内細菌叢障害リスク；厳重にモニタリング",
        },
        "parakeet": {
            "dose": "125 mg/kg PO q12h",
            "notes": "For gram-positive and mixed infections",
            "notes_ja": "グラム陽性菌および混合感染に",
        },
        "parrot": {
            "dose": "125 mg/kg PO q12h",
            "notes": "For gram-positive and mixed infections in psittacines",
            "notes_ja": "オウム目のグラム陽性菌および混合感染に",
        },
    },
    "itraconazole_oral": {
        "amphibian": {
            "dose": "0.01% bath (10 mg/L) × 5 min q24h × 11 days",
            "notes": "For Batrachochytrium dendrobatidis (chytrid); Bd treatment protocol",
            "notes_ja": "カエルツボカビ（Bd）に；Bd治療プロトコル",
        },
        "degu": {
            "dose": "5-10 mg/kg PO q24h",
            "notes": "For dermatophytosis (Trichophyton)",
            "notes_ja": "皮膚糸状菌症（トリコフィトン）に",
        },
        "lizard": {
            "dose": "5-10 mg/kg PO q24-48h",
            "notes": "For CANV (Chrysosporium anamorph of Nannizziopsis vriesii) and systemic mycoses",
            "notes_ja": "CANV（イエローファンガス病）および全身性真菌症に",
        },
        "parakeet": {
            "dose": "5-10 mg/kg PO q12-24h",
            "notes": "Drug of choice for aspergillosis; long treatment courses",
            "notes_ja": "アスペルギルス症の第一選択薬；長期治療コース",
        },
        "parrot": {
            "dose": "5-10 mg/kg PO q12-24h",
            "notes": "For aspergillosis; African greys especially susceptible",
            "notes_ja": "アスペルギルス症に；ヨウムが特に感受性が高い",
        },
        "snake": {
            "dose": "5-10 mg/kg PO q24-48h",
            "notes": "For CANV (Ophidiomyces ophiodiicola) and other mycoses",
            "notes_ja": "CANV（ヘビ真菌症）およびその他の真菌症に",
        },
        "sugar_glider": {
            "dose": "5-10 mg/kg PO q24h",
            "notes": "For dermatophytosis and systemic mycoses",
            "notes_ja": "皮膚糸状菌症および全身性真菌症に",
        },
        "tortoise": {
            "dose": "5-10 mg/kg PO q24-48h",
            "notes": "For shell mycoses and systemic fungal infections",
            "notes_ja": "甲羅の真菌症および全身性真菌感染に",
        },
    },
    "fluconazole_oral": {
        "lizard": {
            "dose": "5-10 mg/kg PO q48-72h",
            "notes": "For systemic fungal infections; good CNS penetration",
            "notes_ja": "全身性真菌感染に；良好なCNS移行性",
        },
        "parakeet": {
            "dose": "5-15 mg/kg PO q24h",
            "notes": "For candidiasis and macrorhabdus (megabacteria)",
            "notes_ja": "カンジダ症およびマクロラブダス（メガバクテリア）に",
        },
        "parrot": {
            "dose": "5-15 mg/kg PO q24h",
            "notes": "For candidiasis; water-soluble for easier administration",
            "notes_ja": "カンジダ症に；水溶性で投与が容易",
        },
        "tortoise": {
            "dose": "5-10 mg/kg PO q48-72h",
            "notes": "For systemic fungal infections; good tissue penetration",
            "notes_ja": "全身性真菌感染に；良好な組織移行性",
        },
    },
    "fenbendazole": {
        "amphibian": {
            "dose": "50-100 mg/kg PO, repeat in 14 days",
            "notes": "For nematode infections (Rhabdias spp.)",
            "notes_ja": "線虫感染（ラブジアス属）に",
        },
        "degu": {
            "dose": "20-50 mg/kg PO q24h × 3-5 days",
            "notes": "For pinworms (Syphacia/Aspiculuris) and other nematodes",
            "notes_ja": "蟯虫（Syphacia/Aspiculuris）およびその他の線虫に",
        },
        "lizard": {
            "dose": "50-100 mg/kg PO, repeat in 14 days",
            "notes": "For nematodes (Oxyuridae common in herbivorous lizards)",
            "notes_ja": "線虫に（草食性トカゲで蟯虫が一般的）",
        },
        "parakeet": {
            "dose": "20-50 mg/kg PO q24h × 3-5 days",
            "notes": "For Ascaridia, Capillaria, and other nematodes",
            "notes_ja": "回虫、毛細線虫およびその他の線虫に",
        },
        "parrot": {
            "dose": "20-50 mg/kg PO q24h × 3-5 days",
            "notes": "For nematodes; repeat in 14 days",
            "notes_ja": "線虫に；14日後に反復投与",
        },
        "sugar_glider": {
            "dose": "20-50 mg/kg PO q24h × 3-5 days",
            "notes": "For nematode infections",
            "notes_ja": "線虫感染に",
        },
    },
    "ivermectin_oral": {
        "degu": {
            "dose": "0.2-0.4 mg/kg SC, repeat in 10-14 days",
            "notes": "For ectoparasites (fur mites)",
            "notes_ja": "外部寄生虫（毛ダニ）に",
        },
    },
    "praziquantel": {
        "amphibian": {
            "dose": "8-24 mg/kg PO/ICe or 10 mg/L bath × 3h",
            "notes": "For trematodes and cestodes; bath for small species",
            "notes_ja": "吸虫および条虫に；小型種では薬浴",
        },
        "lizard": {
            "dose": "5-8 mg/kg PO/IM/SC, repeat in 14 days",
            "notes": "For cestodes and trematodes",
            "notes_ja": "条虫および吸虫に",
        },
        "parakeet": {
            "dose": "5-10 mg/kg PO/IM, repeat in 14 days",
            "notes": "For tapeworms (cestodes)",
            "notes_ja": "条虫（サナダムシ）に",
        },
        "parrot": {
            "dose": "5-10 mg/kg PO/IM, repeat in 14 days",
            "notes": "For cestodes; single dose usually effective",
            "notes_ja": "条虫に；通常1回投与で有効",
        },
    },
    "meloxicam_exotic": {
        "lizard": {
            "dose": "0.1-0.2 mg/kg PO/IM q24-48h",
            "notes": "For pain management; temperature-dependent metabolism",
            "notes_ja": "疼痛管理に；温度依存性の代謝",
        },
        "parakeet": {
            "dose": "0.5-1 mg/kg PO/IM q12-24h",
            "notes": "First-line NSAID for budgerigars and small psittacines",
            "notes_ja": "セキセイインコおよび小型オウム目の第一選択NSAID",
        },
        "parrot": {
            "dose": "0.5-1 mg/kg PO/IM q12-24h",
            "notes": "Well-studied in psittacines; first-line analgesic/anti-inflammatory",
            "notes_ja": "オウム目でよく研究されている；第一選択鎮痛・抗炎症薬",
        },
        "snake": {
            "dose": "0.1-0.2 mg/kg PO/IM q24-48h",
            "notes": "For pain; temperature-dependent metabolism",
            "notes_ja": "疼痛に；温度依存性の代謝",
        },
        "tortoise": {
            "dose": "0.1-0.2 mg/kg PO/IM q24-48h",
            "notes": "For shell injuries, arthritis, post-surgical pain",
            "notes_ja": "甲羅損傷、関節炎、術後疼痛に",
        },
    },
    "tramadol_exotic": {
        "degu": {
            "dose": "5-10 mg/kg PO q12h",
            "notes": "For post-surgical and dental pain",
            "notes_ja": "術後・歯科疼痛に",
        },
        "lizard": {
            "dose": "5-11 mg/kg PO q24-72h",
            "notes": "Variable efficacy; thermal-dependent metabolism",
            "notes_ja": "効果にばらつき；温度依存性の代謝",
        },
        "parakeet": {
            "dose": "10-30 mg/kg PO q8-12h",
            "notes": "For moderate pain; variable efficacy in small birds",
            "notes_ja": "中等度の疼痛に；小型鳥では効果にばらつき",
        },
        "parrot": {
            "dose": "10-30 mg/kg PO q8-12h",
            "notes": "For moderate pain; higher dose in larger parrots",
            "notes_ja": "中等度の疼痛に；大型オウムでは高用量",
        },
        "snake": {
            "dose": "5-10 mg/kg PO q24-72h",
            "notes": "Limited data; variable efficacy across species",
            "notes_ja": "データ限定的；種間で効果にばらつき",
        },
    },
    "buprenorphine_exotic": {
        "degu": {
            "dose": "0.05-0.1 mg/kg SC q8-12h",
            "notes": "Primary analgesic for degus; post-surgical pain",
            "notes_ja": "デグーの主要鎮痛薬；術後疼痛に",
        },
        "parakeet": {
            "dose": "0.1-0.5 mg/kg IM q8-12h",
            "notes": "For post-surgical pain in small psittacines",
            "notes_ja": "小型オウム目の術後疼痛に",
        },
        "parrot": {
            "dose": "0.1-0.5 mg/kg IM q8-12h",
            "notes": "For moderate to severe pain",
            "notes_ja": "中等度〜重度の疼痛に",
        },
    },
    "gabapentin_oral": {
        "parakeet": {
            "dose": "10-25 mg/kg PO q8-12h",
            "notes": "For neuropathic pain and self-mutilation (feather plucking)",
            "notes_ja": "神経障害性疼痛および自傷行為（毛引き）に",
        },
        "parrot": {
            "dose": "10-25 mg/kg PO q8-12h",
            "notes": "For chronic pain, neuropathic pain, and feather destructive behavior",
            "notes_ja": "慢性疼痛、神経障害性疼痛、および破壊的羽毛行動に",
        },
        "sugar_glider": {
            "dose": "3-5 mg/kg PO q8-12h",
            "notes": "For neuropathic pain and self-mutilation pain management",
            "notes_ja": "神経障害性疼痛および自傷行為の疼痛管理に",
        },
    },
    "prednisolone": {
        "amphibian": {
            "dose": "1-2 mg/kg IM/ICe single dose",
            "notes": "Emergency use only; for severe inflammation or anaphylaxis",
            "notes_ja": "緊急時のみ；重度の炎症またはアナフィラキシーに",
        },
        "degu": {
            "dose": "0.5-1 mg/kg PO/IM q24h (short course only)",
            "notes": "CAUTION: Degus prone to diabetes; steroids worsen hyperglycemia",
            "notes_ja": "注意: デグーは糖尿病になりやすい；ステロイドは高血糖を悪化",
        },
        "lizard": {
            "dose": "2-5 mg/kg IM once, then 1-2 mg/kg q24-48h",
            "notes": "Very limited use; for severe inflammation or shock only",
            "notes_ja": "使用は非常に限定的；重度の炎症またはショックにのみ",
        },
        "parakeet": {
            "dose": "0.5-1 mg/kg PO/IM q12h (short course)",
            "notes": "Immunosuppression dangerous in birds; use very short courses only",
            "notes_ja": "鳥では免疫抑制が危険；極短期使用のみ",
        },
        "parrot": {
            "dose": "0.5-1 mg/kg PO/IM q12h (short course)",
            "notes": "Immunosuppression dangerous; use only for severe inflammation",
            "notes_ja": "免疫抑制が危険；重度の炎症にのみ使用",
        },
    },
    "diazepam": {
        "amphibian": {
            "dose": "Bath: 5-10 mg/L until effect",
            "notes": "For seizures; bath administration for absorption through skin",
            "notes_ja": "痙攣に；皮膚からの吸収のため薬浴投与",
        },
        "degu": {
            "dose": "0.5-2 mg/kg IM/IV",
            "notes": "For seizures; diabetes-related hypoglycemic seizures common in degus",
            "notes_ja": "痙攣に；デグーでは糖尿病関連の低血糖性痙攣が多い",
        },
        "lizard": {
            "dose": "0.5-2.5 mg/kg IM/IV",
            "notes": "For seizures; slow onset in ectotherms",
            "notes_ja": "痙攣に；変温動物では発現が遅い",
        },
        "parakeet": {
            "dose": "0.5-1 mg/kg IM/IV",
            "notes": "For seizures; short-acting",
            "notes_ja": "痙攣に；短時間作用型",
        },
        "parrot": {
            "dose": "0.5-1 mg/kg IM/IV",
            "notes": "For seizure emergencies; calcium and lead levels should also be checked",
            "notes_ja": "痙攣緊急時に；カルシウムおよび鉛濃度も確認すべき",
        },
        "sugar_glider": {
            "dose": "0.5-1 mg/kg IM/IV",
            "notes": "For seizures and severe self-mutilation episodes",
            "notes_ja": "痙攣および重度の自傷行為エピソードに",
        },
        "tortoise": {
            "dose": "0.5-2.5 mg/kg IM",
            "notes": "For seizures; slow onset—allow adequate time before redosing",
            "notes_ja": "痙攣に；発現が遅い—再投与前に十分な時間をおく",
        },
    },
    "acepromazine": {
        "degu": {
            "dose": "0.5-1 mg/kg IM",
            "notes": "For sedation; combine with opioid for procedures",
            "notes_ja": "鎮静に；処置時はオピオイドと併用",
        },
    },
    "furosemide_injectable": {
        "degu": {
            "dose": "1-4 mg/kg SC/IM q12h",
            "notes": "For pulmonary edema and CHF",
            "notes_ja": "肺水腫およびうっ血性心不全に",
        },
        "lizard": {
            "dose": "2-5 mg/kg IM/SC q12-24h",
            "notes": "For edema and coelomic effusion",
            "notes_ja": "浮腫および体腔液貯留に",
        },
        "parakeet": {
            "dose": "0.15-2 mg/kg IM q12-24h",
            "notes": "For avian CHF and ascites; dehydration risk high",
            "notes_ja": "鳥のうっ血性心不全および腹水に；脱水リスク高い",
        },
        "parrot": {
            "dose": "0.15-2 mg/kg IM q12-24h",
            "notes": "For congestive heart failure; monitor hydration closely",
            "notes_ja": "うっ血性心不全に；水和状態を厳重にモニタリング",
        },
        "sugar_glider": {
            "dose": "1-2 mg/kg SC/IM q12h",
            "notes": "For pulmonary edema and fluid overload",
            "notes_ja": "肺水腫および体液過負荷に",
        },
    },
    "famotidine": {
        "amphibian": {
            "dose": "0.5 mg/kg PO/IM q24h",
            "notes": "Limited data; for suspected GI ulceration",
            "notes_ja": "データ限定的；消化管潰瘍疑い例に",
        },
        "degu": {
            "dose": "0.5 mg/kg PO q12-24h",
            "notes": "For gastric ulcer prevention",
            "notes_ja": "胃潰瘍予防に",
        },
        "sugar_glider": {
            "dose": "0.5 mg/kg PO q12-24h",
            "notes": "For stress-related GI ulceration",
            "notes_ja": "ストレス関連消化管潰瘍に",
        },
    },
    "sucralfate": {
        "degu": {
            "dose": "25-50 mg/kg PO q8-12h",
            "notes": "For gastric ulceration; stress-related GI disease",
            "notes_ja": "胃潰瘍に；ストレス関連消化管疾患",
        },
        "lizard": {
            "dose": "25-50 mg/kg PO q8-12h",
            "notes": "For GI ulceration",
            "notes_ja": "消化管潰瘍に",
        },
        "parakeet": {
            "dose": "25 mg/kg PO q8h",
            "notes": "For proventricular/ventricular ulceration",
            "notes_ja": "前胃/筋胃潰瘍に",
        },
        "parrot": {
            "dose": "25 mg/kg PO q8h",
            "notes": "For proventricular/ventricular ulceration; PDD-associated lesions",
            "notes_ja": "前胃/筋胃潰瘍に；PDD関連病変",
        },
    },
    "metoclopramide": {
        "degu": {
            "dose": "0.5 mg/kg PO/SC q8-12h",
            "notes": "For GI motility disorders",
            "notes_ja": "消化管運動障害に",
        },
        "parakeet": {
            "dose": "0.5-1 mg/kg PO/IM q8-12h",
            "notes": "For crop stasis and vomiting",
            "notes_ja": "素嚢うっ滞および嘔吐に",
        },
        "parrot": {
            "dose": "0.5-1 mg/kg PO/IM q8-12h",
            "notes": "For crop stasis and regurgitation",
            "notes_ja": "素嚢うっ滞および吐き戻しに",
        },
    },
    "lactulose": {
        "degu": {
            "dose": "0.5 mL/kg PO q12h",
            "notes": "For hepatic disease support",
            "notes_ja": "肝疾患サポートに",
        },
    },
    "silver_sulfadiazine_cream": {
        "amphibian": {
            "dose": "Apply thin layer to wounds (keep moist)",
            "notes": "For bacterial dermatitis and red leg syndrome lesions",
            "notes_ja": "細菌性皮膚炎およびレッドレッグ症候群の病変に",
        },
        "lizard": {
            "dose": "Apply to wounds/burns q24h",
            "notes": "For thermal burns and bite wounds",
            "notes_ja": "熱傷および咬傷に",
        },
        "snake": {
            "dose": "Apply to wounds/burns q24h",
            "notes": "For thermal burns and scale rot lesions",
            "notes_ja": "熱傷およびスケールロット（鱗腐り）病変に",
        },
    },
}
