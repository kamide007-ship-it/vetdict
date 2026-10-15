"""Curated treatments for ectoparasite / dermatophyte / heartworm entries that
carried the generic anthelmintic template (2026-10 第70弾).

The template — EN "Anti-parasitic therapy appropriate to the parasite
(fenbendazole, ivermectin, praziquantel, toltrazuril)..." / JA "同定された寄生虫に
応じた適切な駆虫薬が必要..." — was stamped on mite infestations (fenbendazole,
praziquantel and toltrazuril do not kill mites), dermatophytoses (fungal — no
antiparasitic is indicated), ferret heartworm and tarantula mites/nematodes
(macrocyclic lactones and other acaricides are lethal to arachnids).

Each value is (treatment_ja | None, treatment_en | None); None keeps the
existing (already curated) field. Doses: Carpenter's Exotic Animal Formulary
6th ed; Quesenberry & Carpenter 4th ed; Ritchie & Harrison; Mader 3rd ed;
Moriello 2017 Vet Dermatol consensus; Plumb's 10th ed; ESCCAP GL3.
"""

TEMPLATE_EN = "Anti-parasitic therapy appropriate to the parasite (fenbendazole"
TEMPLATE_JA = "同定された寄生虫に応じた適切な駆虫薬が必要"
# Coccidia/nematode/cestode workup template wrongly applied to mite entries
TEMPLATE_JA_ENDOPARASITE_WORKUP = "糞便PCR/直接鏡検/フローテーション法で原因虫種を特定してから駆虫薬を選択する"

_NO_FIPRONIL_JA = "⚠フィプロニルはウサギ・モルモット・チンチラ・デグーに禁忌（けいれん・死亡例）。"
_NO_FIPRONIL_EN = (
    "Fipronil is contraindicated in rabbits, guinea pigs, chinchillas and degus (seizures/deaths reported)."
)

CURATED = {
    # ---------------- dogs / cats: JA mirror of curated English ----------------
    ("Dog", "Mange (Demodex/Sarcoptes)"): (
        "毛包虫症: イソキサゾリン系が第一選択 — フルララネル（ブラベクト）25-56 mg/kg PO 単回（12週毎）、またはアフォキソラネル（ネクスガード）2.7 mg/kg PO 月1回。"
        "イベルメクチン 0.3-0.6 mg/kg PO q24h は代替（MDR1/ABCB1変異犬種では使用しない）。限局型は若齢犬で自然治癒が多い。全身型は1ヶ月間隔の皮膚掻爬で2回連続陰性まで治療を継続。"
        "疥癬（Sarcoptes）: イソキサゾリン系の単回投与で治癒することが多い。セラメクチン（レボリューション）外用 2週毎×3回。同居動物も同時治療し環境（寝具）を洗浄。"
        "予後: 限局型毛包虫症は約90%が自然消退、全身型はイソキサゾリンで80-90%治癒、疥癬は極めて良好。（Mueller 2020 Vet Dermatol; Perego 2019）",
        None,
    ),
    ("Dog", "Ear Mite Infestation (Otodectes)"): (
        "イソキサゾリン系（フルララネル・サロラネル）の単回投与で治癒することが多い。セラメクチン（レボリューション）外用 2週毎×3回。"
        "イベルメクチン 0.2-0.4 mg/kg SC/PO、14日後に反復（MDR1変異犬種では使用しない）。ミルベマイシン含有点耳薬も選択肢。治療前に耳道洗浄で耳垢を除去。"
        "同居の犬猫すべてを同時治療（猫が感染源のことが多い）。ダニは宿主外で長く生存しないため環境処理は通常不要。予後: 極めて良好。（Shanks 2000; Six 2000）",
        None,
    ),
    ("Dog", "Sarcoptic Mange (Scabies)"): (
        "イソキサゾリン系が第一選択（フルララネル単回、またはサロラネル/アフォキソラネル月1回）。セラメクチン外用 2週毎×3回。"
        "イベルメクチン 0.2-0.4 mg/kg SC/PO q7-14日×4回（MDR1変異犬種では禁忌）。石灰硫黄合剤 1:16 週1回×6回（全犬種に安全）。"
        "同居動物を同時治療、寝具は熱湯洗浄。駆虫中の掻痒緩和にプレドニゾロン 0.5-1 mg/kg PO 3-5日。人獣共通（ヒトでは一過性の自然消退性皮疹）。"
        "予後: 極めて良好。（Mueller 2020; Perego 2019）",
        None,
    ),
    ("Cat", "Ear Mite Infestation (Otodectes cynotis)"): (
        "セラメクチン（レボリューション）外用を1回、30日後に反復（全身作用で第一選択）。イベルメクチン 0.2-0.3 mg/kg SC/PO、2-3週後に反復。"
        "フルララネル（ブラベクト）スポットオン、サロラネル・セラメクチン配合（レボリューションプラス）も有効。ミルベマイシン点耳薬。黒褐色の耳垢をやさしく洗浄。"
        "伝染力が強いため同居の猫・犬すべてを治療。二次性細菌・マラセチア性外耳炎は外用抗菌・抗真菌薬で並行治療。猫の外耳炎の50%以上の原因。"
        "予後: 同居全頭の全身治療で極めて良好。（Miller 2013; ESCCAP）",
        None,
    ),
    ("Cat", "Flea Infestation"): (
        "イソキサゾリン系: フルララネル（ブラベクト）スポットオン 12週毎、サロラネル・セラメクチン配合（レボリューションプラス）月1回。セラメクチン（レボリューション）月1回、フィプロニル スポットオン月1回。"
        "海外ではチゴラネル・エモデプシド・プラジカンテル配合スポットオン（フェルプレバ、EU 2021承認・国内未承認）が1回で最長13週のノミ・マダニ予防と内部寄生虫駆除を兼ねる。"
        "同居ペット全頭を治療。環境: 徹底的な掃除機がけ、寝具の60°C洗浄、環境用スプレー（ペルメトリン系は猫の体に絶対使用しない）。蛹は環境中で数ヶ月生存するため通年予防を推奨。"
        "**犬用ペルメトリン製剤は猫に致死的**。重度寄生の子猫はノミ性貧血で輸血が必要な場合あり。瓜実条虫の同時駆除（プラジカンテル）も考慮。"
        "予後: 全頭への継続的な月1回治療で極めて良好。（Rust 2017; ESCCAP GL3）",
        "Isoxazoline: fluralaner (Bravecto) spot-on q12 weeks; sarolaner/selamectin (Revolution Plus) monthly. Selamectin (Revolution) monthly; fipronil spot-on monthly. "
        "Overseas, tigolaner/emodepside/praziquantel spot-on (Felpreva, EU 2021; not approved in Japan) provides up to 13 weeks of flea/tick control plus endoparasite treatment in one application. "
        "Treat ALL pets in the household. Environment: vacuum extensively, wash bedding at 60°C, premise spray (permethrin-based — never apply to cats). Pupae survive months — year-round prevention. "
        "NEVER use canine permethrin products on cats (fatal). Severe infestation in kittens may cause flea anemia requiring transfusion. Consider concurrent Dipylidium treatment (praziquantel). "
        "Prognosis: excellent with consistent treatment of all animals. (Rust 2017; ESCCAP GL3)",
    ),
    ("Cat", "Notoedric Mange (Feline Scabies)"): (
        "セラメクチン（レボリューション）外用 2週毎×3回（第一選択）。イベルメクチン 0.2-0.3 mg/kg SC 14日毎×3回。石灰硫黄合剤 1:16 7日毎×6-8週。"
        "フルララネル（ブラベクト）スポットオン（エビデンス蓄積中）。同居猫すべてを治療。Notoedres cati は伝染力が強く強い掻痒、頭部・耳介・顔面の痂皮が典型。"
        "皮膚掻爬でダニは多数検出されやすい（疥癬より容易）。軽度の人獣共通（一過性）。宿主外で長く生存しないため環境処理は限定的でよい。予後: 治療で極めて良好。（Miller 2013; Leone 2013）",
        None,
    ),
    ("Cat", "Feline Trombiculiasis (Chigger Mite)"): (
        "外用: フィプロニルスプレー、フルララネル（ブラベクト）スポットオン、セラメクチン（レボリューション）。石灰硫黄合剤 1:16 週1回×2-3回。やさしい洗浄でダニを物理的に除去。"
        "止痒: プレドニゾロン 0.5-1 mg/kg PO q24h×5-7日、狭い範囲はヒドロコルチゾン外用。二次細菌感染にアモキシシリン・クラブラン酸。"
        "ツツガムシ（秋ダニ）は幼虫期のみ寄生し成虫は自由生活。夏〜秋の季節性で外出猫に多く、頭部・耳介・肢端・腹部に病変。ダニが離脱すれば自然消退。"
        "予防: 流行期の外出制限。予後: 極めて良好。（Miller 2013; Shanks 2000）",
        None,
    ),
    # ---------------- rabbits / birds / hamster: EN for curated JA ----------------
    ("Rabbit", "Ear Mites (Psoroptes cuniculi)"): (
        None,
        "Psoroptes cuniculi. Ivermectin 0.2-0.4 mg/kg SC q10-14 days × 3-4 (first-line) or selamectin 6-18 mg/kg topically q30 days. "
        "Do NOT forcibly remove crusts (very painful, bleeds) — they soften and shed once mites die. Meloxicam 0.3-0.5 mg/kg PO q24h for analgesia; "
        "enrofloxacin 5-10 mg/kg PO q12h for secondary otitis. Clean the hutch; treat in-contact rabbits. Oral penicillins/amoxicillin are fatal (enterotoxemia). "
        + _NO_FIPRONIL_EN
        + " (Carpenter 6th ed; Quesenberry & Carpenter 4th ed)",
    ),
    ("Rabbit", "Cheyletiella Mange (Fur Mites)"): (
        None,
        "Cheyletiella parasitovorax ('walking dandruff' — heavy dorsal scaling). Ivermectin 0.2-0.4 mg/kg SC q10-14 days × 3-4 (first-line); "
        "selamectin 6-18 mg/kg topically q30 days × 3. Environmental cleaning is essential (mites survive ~10 days off the host); treat in-contact animals. "
        "Mildly zoonotic (pruritic papules in owners). Oral penicillins are fatal in rabbits. "
        + _NO_FIPRONIL_EN
        + " (Carpenter 6th ed)",
    ),
    ("Hamster", "Acariasis (Mite Infestation)"): (
        None,
        "Identify the mite by skin scraping. Ivermectin 0.2-0.4 mg/kg SC q10-14 days × 3-4 (effective against Demodex, Sarcoptes and Notoedres); "
        "selamectin 6-15 mg/kg topically q30 days as an alternative. Enrofloxacin 5-10 mg/kg PO q12h for secondary pyoderma. Clean the cage; "
        "investigate immunosuppression (age, neoplasia, hyperadrenocorticism), especially in demodicosis. (Carpenter 6th ed)",
    ),
    ("Hamster", "Dermatophytosis (Ringworm)"): (
        None,
        "Fungal — antiparasitics are not indicated. Trichophyton mentagrophytes most common; zoonotic. Topical miconazole/clotrimazole q12h × 4-6 weeks; "
        "systemic terbinafine 20 mg/kg PO q24h × 4-6 weeks for widespread/refractory cases (griseofulvin 25 mg/kg is teratogenic — not in pregnancy). "
        "Lime-sulfur dips weekly. Replace all bedding, disinfect the cage (sodium hypochlorite 1:10) — spores persist >18 months. "
        "Continue until two consecutive negative cultures. Wear gloves; owners may develop lesions. (Moriello 2017 Vet Dermatol consensus; Carpenter 6th ed)",
    ),
    ("Hamster", "Ringworm (Trichophyton)"): (
        None,
        "Same disease as dermatophytosis (T. mentagrophytes) — antifungal, not antiparasitic. Topical miconazole/clotrimazole q12h × 4-6 weeks; "
        "terbinafine 20 mg/kg PO q24h × 4-6 weeks (itraconazole 5-10 mg/kg PO q24h alternative). Replace bedding and disinfect with hypochlorite 1:10; "
        "isolate affected animals; treat until culture-negative. Zoonotic. (Moriello 2017; Carpenter 6th ed)",
    ),
    ("Guinea Pig", "Dermatophytosis (Ringworm)"): (
        None,
        "Fungal (T. mentagrophytes most common) — antiparasitics are not indicated. Topical miconazole/clotrimazole q12h × 4-6 weeks; "
        "terbinafine 20-40 mg/kg PO q24h × 4-6 weeks is safe and preferred systemically; itraconazole 5 mg/kg PO q24h × 6 weeks alternative. "
        "Griseofulvin is not recommended (hepatotoxicity). Disinfect the environment with dilute bleach; zoonotic. Ensure vitamin C supplementation. (Carpenter 6th ed)",
    ),
    ("Bird", "Dermatophytosis (Ringworm)"): (
        None,
        "Fungal — antiparasitics are not indicated. Itraconazole 5-10 mg/kg PO q12h × 4-6 weeks is the systemic first choice, with topical miconazole/clotrimazole q12h. "
        "CAUTION: African grey parrots are particularly sensitive to itraconazole (anorexia, depression, hepatotoxicity) — prefer voriconazole or terbinafine. "
        "Disinfect cage, perches and nest box (hypochlorite 1:10); isolate until culture-negative (two consecutive negative cultures). Zoonotic. (Carpenter 6th ed; Ritchie & Harrison)",
    ),
    ("Bird", "Cnemidocoptes pilae (Scaly Leg Mite)"): (
        None,
        "Ivermectin 0.2 mg/kg PO or applied to bare skin, q7-10 days × 3-4 (first-line, high cure rate); moxidectin 0.2 mg/kg topical spot-on alternative. "
        "Always dilute and measure precisely in small birds — never drip undiluted product. Do not pick off crusts (bleeding, infection); soften with warm soaks and let them shed. "
        "Trim severely deformed beaks. Examine/treat in-contact birds and clean perches. (Ritchie & Harrison; Carpenter 6th ed)",
    ),
    ("Bird", "Tracheal Mite (Sternostoma)"): (
        None,
        "Sternostoma tracheacolum — canaries and finches predisposed. Ivermectin 0.2-0.4 mg/kg PO/topical weekly × 2-3 (dilute accurately); moxidectin 1 mg/kg PO weekly × 2-3. "
        "Dying mites can obstruct small airways — have oxygen available and treat severe dyspnea first. Adjuncts: saline nebulization q12h, enrofloxacin 15 mg/kg PO q12h for secondary infection, warmth and humidity. "
        "Diagnosis by tracheal transillumination. Treat the whole aviary. (Carpenter 6th ed; Ritchie & Harrison)",
    ),
    ("Bird", "Air Sac Mite"): (
        None,
        "Ivermectin 0.2 mg/kg PO or on the skin of the neck, q10-14 days × 3 (standard); selamectin 6 mg/kg topically is also effective. "
        "Severe dyspnea: oxygen and bronchodilator (terbutaline 0.01 mg/kg IM). Disinfect the environment and treat all in-contact birds simultaneously; recheck for reinfection. "
        "Dilute ivermectin accurately for small birds. (Carpenter 6th ed)",
    ),
    ("Bird", "Red Mite (Dermanyssus)"): (
        None,
        "Environmental control is the priority — Dermanyssus hides in cage crevices and feeds at night: deep-clean the cage, replace wooden perches/nest boxes, spray crevices with a bird-safe pyrethrin product (remove the bird during spraying) and repeat for 2-3 weeks to cover the life cycle. "
        "Bird: ivermectin 0.2 mg/kg PO, repeat in 7 days. Severe anemia (PCV <30%): fluids, iron, transfusion if needed. Avoid organophosphate/carbamate products on birds. (Ritchie & Harrison; Carpenter 6th ed)",
    ),
    ("Horse", "Coccidioidomycosis"): (
        None,
        "Fungal (Coccidioides immitis/posadasii; endemic to the US Southwest) — antiparasitics are not indicated. Itraconazole 5 mg/kg PO q24h or fluconazole 5 mg/kg PO q24h "
        "(good CNS penetration) for months; disseminated disease: amphotericin B 0.3-0.5 mg/kg IV q48h with renal monitoring. NSAIDs for inflammation. "
        "Prognosis depends on the extent of dissemination (guarded to poor when disseminated). (Reed & Bayly 4th ed)",
    ),
    ("Exotic Other", "Dermatophytosis (Ringworm)"): (
        "真菌感染であり駆虫薬は適応外。皮膚掻爬・鏡検、真菌培養（DTM）またはPCRで確定。局所: ミコナゾール/クロトリマゾール q12h、または石灰硫黄合剤 週1-2回。"
        "広範囲・難治例は全身性抗真菌薬（テルビナフィン 20-30 mg/kg PO q24h が小型哺乳類で比較的安全、イトラコナゾール 5-10 mg/kg PO q24h は種の感受性を確認）を4-6週以上、培養2回連続陰性まで継続。"
        "床材の全交換と次亜塩素酸ナトリウム（1:10）による環境消毒（胞子は1年以上生存）、感染個体の隔離。人獣共通感染症のため手袋着用。（Moriello 2017 Vet Dermatol; Carpenter 6th ed）",
        "Fungal — antiparasitics are not indicated. Confirm by skin scraping/microscopy, fungal culture (DTM) or PCR. Topical miconazole/clotrimazole q12h or lime-sulfur dips 1-2×/week. "
        "Widespread/refractory: systemic antifungal (terbinafine 20-30 mg/kg PO q24h is relatively safe in small mammals; itraconazole 5-10 mg/kg PO q24h — check species sensitivity) for ≥4-6 weeks until two consecutive negative cultures. "
        "Replace all bedding and disinfect with hypochlorite 1:10 (spores survive >1 year); isolate affected animals. Zoonotic — wear gloves. (Moriello 2017; Carpenter 6th ed)",
    ),
    ("Exotic Other", "Hedgehog Ringworm (Trichophyton)"): (
        "ハリネズミの皮膚糸状菌症（主にTrichophyton erinacei、ヒトにも感染）。真菌感染であり駆虫薬は適応外。針の脱落・痂皮・鱗屑。ダニ（Caparinia）との混合感染が多いため皮膚掻爬も同時に実施。"
        "テルビナフィン 10-30 mg/kg PO q24h、またはイトラコナゾール 5-10 mg/kg PO q24h を4-6週以上、培養陰性まで。局所にエニルコナゾール 0.2% 浸漬・石灰硫黄合剤も選択肢。"
        "床材の交換・環境消毒、多頭飼育では同居個体の検査。人獣共通感染症（飼い主の皮疹）。（Carpenter 6th ed; Quesenberry & Carpenter 4th ed）",
        "Hedgehog dermatophytosis (mainly Trichophyton erinacei; zoonotic). Fungal — antiparasitics are not indicated. Quill loss, crusting and scaling; mixed infection with Caparinia mites is common, so perform skin scrapings too. "
        "Terbinafine 10-30 mg/kg PO q24h or itraconazole 5-10 mg/kg PO q24h for ≥4-6 weeks until culture-negative; topical enilconazole 0.2% dips or lime sulfur are options. "
        "Replace bedding and disinfect; check in-contact hedgehogs. Zoonotic. (Carpenter 6th ed; Quesenberry & Carpenter 4th ed)",
    ),
    # ---------------- both languages ----------------
    ("Hamster", "Fur Mites (Demodex criceti)"): (
        "ハムスターの毛包虫症（Demodex criceti/aurati）。皮膚掻爬で確定。イベルメクチン 0.3-0.5 mg/kg PO q24h を皮膚掻爬2回連続陰性まで（または 0.2-0.4 mg/kg SC q7-14日×3回以上）、セラメクチン 6-15 mg/kg 外用 q14-30日も選択肢。"
        "アミトラズ薬浴は低体温・中毒リスクがあり小型種では推奨しない。全身性毛包虫症は免疫低下の徴候のため、加齢・腫瘍・副腎皮質機能亢進症などの基礎疾患を精査する。二次膿皮症にエンロフロキサシン。（Carpenter 6th ed; Quesenberry & Carpenter 4th ed）",
        "Hamster demodicosis (Demodex criceti/aurati), confirmed by skin scraping. Ivermectin 0.3-0.5 mg/kg PO q24h until two consecutive negative scrapings (or 0.2-0.4 mg/kg SC q7-14 days × ≥3); selamectin 6-15 mg/kg topically q14-30 days is an alternative. "
        "Amitraz dips carry hypothermia/toxicity risk in small rodents. Generalized demodicosis signals immunosuppression — investigate age, neoplasia and hyperadrenocorticism. Enrofloxacin for secondary pyoderma. (Carpenter 6th ed)",
    ),
    ("Guinea Pig", "Demodex Mites"): (
        "モルモットの毛包虫症は稀で、免疫低下・妊娠・ストレスが背景にあることが多い。皮膚掻爬で確定。イベルメクチン 0.2-0.4 mg/kg SC q7-10日×3-4回、またはセラメクチン 15 mg/kg 外用 2週毎。"
        "皮膚掻爬2回連続陰性まで継続し、ビタミンC欠乏・妊娠・併発疾患を是正。二次感染は培養に基づく抗菌薬（経口ペニシリン系・セファロスポリンは禁忌）。"
        + _NO_FIPRONIL_JA
        + "（Carpenter 6th ed）",
        "Demodicosis is rare in guinea pigs and usually reflects immunosuppression, pregnancy or stress. Confirm by skin scraping. Ivermectin 0.2-0.4 mg/kg SC q7-10 days × 3-4, or selamectin 15 mg/kg topically q2 weeks, until two negative scrapings; "
        "correct vitamin C deficiency and concurrent disease. Culture-based antibiotics for secondary infection (oral penicillins/cephalosporins are contraindicated). "
        + _NO_FIPRONIL_EN
        + " (Carpenter 6th ed)",
    ),
    ("Guinea Pig", "Fur Mites - Heavy Infestation"): (
        "モルモットの毛ダニ（Chirodiscoides caviae）重度寄生、または疥癬（Trixacarus caviae）との鑑別が重要。セラメクチン 15 mg/kg 外用を10日間隔で2回、またはイベルメクチン 0.4-0.5 mg/kg SC 7-10日毎×3回（Eshar 2012 JAVMA: 両者とも有効、セラメクチンは注射不要で取り扱いストレスが少ない）。"
        "強い掻痒による発作様症状がある場合は鎮静・抗けいれん（ミダゾラム 0.5-1 mg/kg IM）とメロキシカム 0.3-0.5 mg/kg PO q24h。同居全頭を治療、床材交換・ケージ洗浄。ビタミンCを補給。"
        + _NO_FIPRONIL_JA,
        "Heavy fur-mite (Chirodiscoides caviae) burden — differentiate from Trixacarus caviae mange. Selamectin 15 mg/kg topically twice 10 days apart, or ivermectin 0.4-0.5 mg/kg SC q7-10 days × 3 (Eshar 2012 JAVMA: both effective; selamectin avoids injections). "
        "Pruritic seizure-like episodes: sedation/anticonvulsant (midazolam 0.5-1 mg/kg IM) and meloxicam 0.3-0.5 mg/kg PO q24h. Treat all in-contact guinea pigs, replace bedding, clean the cage, supplement vitamin C. "
        + _NO_FIPRONIL_EN,
    ),
    ("Guinea Pig", "Chirodiscoides caviae Mite"): (
        "モルモットの毛ダニ（Chirodiscoides caviae）は被毛に付着し、軽度寄生は無症状、重度では掻痒・脱毛（腰背部・脇腹）。被毛のセロハンテープ検査・抜毛鏡検で確定（糞便検査では検出できない）。"
        "セラメクチン 15 mg/kg 外用を10-14日間隔で2回、またはイベルメクチン 0.2-0.4 mg/kg SC 7-10日毎×3回。同居全頭を同時治療し床材を交換。駆虫薬のフェンベンダゾール・プラジカンテル・トルトラズリルはダニに無効。"
        + _NO_FIPRONIL_JA
        + "（Carpenter 6th ed）",
        "Chirodiscoides caviae clings to hair shafts: light burdens are asymptomatic, heavy burdens cause pruritus and alopecia (lumbar/flanks). Diagnose by tape impression or trichogram (fecal tests do not detect it). "
        "Selamectin 15 mg/kg topically twice 10-14 days apart, or ivermectin 0.2-0.4 mg/kg SC q7-10 days × 3. Treat all in-contact guinea pigs and replace bedding. Fenbendazole, praziquantel and toltrazuril do not kill mites. "
        + _NO_FIPRONIL_EN
        + " (Carpenter 6th ed)",
    ),
    ("Guinea Pig", "Ear Mite Infestation"): (
        "モルモットの耳ダニは稀（主にウサギの Psoroptes cuniculi・猫の Otodectes の伝播）。耳垢の鏡検で確定。セラメクチン 15 mg/kg 外用 2週毎×2回、またはイベルメクチン 0.2-0.4 mg/kg SC 10-14日毎×3回。"
        "痂皮は無理に剥がさない（出血・疼痛）。鎮痛にメロキシカム 0.3-0.5 mg/kg PO q24h。同居動物（ウサギ・猫）も治療。中耳炎・斜頸の併発に注意。"
        + _NO_FIPRONIL_JA,
        "Ear mites are uncommon in guinea pigs (usually Psoroptes from rabbits or Otodectes from cats). Confirm by microscopy of ear debris. Selamectin 15 mg/kg topically q2 weeks × 2, or ivermectin 0.2-0.4 mg/kg SC q10-14 days × 3. "
        "Do not pick crusts (bleeding, pain); meloxicam 0.3-0.5 mg/kg PO q24h for analgesia. Treat in-contact rabbits/cats; watch for otitis media/head tilt. "
        + _NO_FIPRONIL_EN,
    ),
    ("Chinchilla", "Fur Mites"): (
        "チンチラの毛ダニは稀（密な被毛のため外部寄生虫は少ない）— まず毛噛み（バーバリング）・皮膚糸状菌症を鑑別。皮膚掻爬・テープ検査で確定後、セラメクチン 15 mg/kg 外用 q30日、またはイベルメクチン 0.2-0.4 mg/kg SC 14日毎×3-4回。"
        "砂浴び用の砂と木製・布製床材は廃棄し、ケージを洗浄。人獣共通（一過性の皮疹）のため手袋着用。"
        + _NO_FIPRONIL_JA
        + "（Quesenberry & Carpenter 4th ed）",
        "Fur mites are rare in chinchillas (very dense coat) — first rule out fur chewing (barbering) and dermatophytosis. Once confirmed by scraping/tape test: selamectin 15 mg/kg topically q30 days or ivermectin 0.2-0.4 mg/kg SC q14 days × 3-4. "
        "Discard dust-bath sand and wood/fabric bedding; clean the cage. Mildly zoonotic — wear gloves. "
        + _NO_FIPRONIL_EN
        + " (Quesenberry & Carpenter 4th ed)",
    ),
    ("Degu", "Fur Mites (Demodex / Notoedres)"): (
        "デグーの毛包虫・疥癬（Notoedres）。皮膚掻爬で確定。イベルメクチン 0.2-0.4 mg/kg SC 7-14日毎×3-4回、またはセラメクチン 15 mg/kg 外用 q14-30日を、皮膚掻爬2回連続陰性まで。"
        "同居個体を同時治療し床材を交換。毛包虫症は免疫低下（加齢・糖尿病・ストレス）を精査。"
        + _NO_FIPRONIL_JA
        + "（Carpenter 6th ed）",
        "Degu demodicosis/notoedric mange, confirmed by skin scraping. Ivermectin 0.2-0.4 mg/kg SC q7-14 days × 3-4, or selamectin 15 mg/kg topically q14-30 days, until two negative scrapings. "
        "Treat cage mates, replace bedding; investigate immunosuppression (age, diabetes, stress) in demodicosis. "
        + _NO_FIPRONIL_EN
        + " (Carpenter 6th ed)",
    ),
    ("Degu", "Sarcoptic Mange"): (
        "デグーの疥癬。イベルメクチン 0.2-0.4 mg/kg SC 7-14日毎×3-4回（第一選択）、またはセラメクチン 15 mg/kg 外用 q30日。床材・ケージを清掃し同居個体を治療。強い掻痒にメロキシカム。人獣共通（一過性）のため手袋着用。"
        + _NO_FIPRONIL_JA
        + "（Quesenberry & Carpenter 2012）",
        None,
    ),
    ("Guinea Pig", "Trixacarus caviae (Sarcoptic Mange) - Severe"): (
        "【重症 — 強い掻痒から発作を起こしうる】イベルメクチン 0.2-0.5 mg/kg SC 7-14日毎×3-4回（第一選択）、またはセラメクチン 15-30 mg/kg 外用 q30日（Eshar 2012 JAVMA: セラメクチン2回投与も同等に有効）。"
        "掻痒性発作にはミダゾラム 0.5-1 mg/kg IM、鎮痛にメロキシカム 0.3-0.5 mg/kg q24h。床材をすべて廃棄しケージを漂白剤で洗浄、同居全頭を治療。人獣共通（一過性の丘疹）。"
        "ビタミンC補給とストレス軽減。"
        + _NO_FIPRONIL_JA
        + "予後: 治療で良好だが重度例は致死的になりうる。（Quesenberry & Carpenter 2012）",
        None,
    ),
    ("Hedgehog", "Ear Mites"): (
        "ハリネズミの耳ダニ（Notoedres cati・Otodectes 等）。耳介辺縁の痂皮・掻痒。セラメクチン 6-18 mg/kg 外用 q21-30日×2-3回、またはイベルメクチン 0.2-0.4 mg/kg SC 10-14日毎×3回。"
        "フルララネル 15 mg/kg PO 単回が Caparinia を含むハリネズミのダニに有効と報告（Romero 2017 Vet Dermatol）。痂皮は軟化させて自然脱落を待つ。同居個体の治療と床材交換。（Carpenter 6th ed）",
        "Hedgehog ear mites (Notoedres cati, Otodectes, etc.): crusting of the pinnal margins and pruritus. Selamectin 6-18 mg/kg topically q21-30 days × 2-3, or ivermectin 0.2-0.4 mg/kg SC q10-14 days × 3. "
        "A single oral dose of fluralaner 15 mg/kg has been reported effective against hedgehog mites (Romero 2017 Vet Dermatol). Let crusts soften and shed; treat cage mates and replace bedding. (Carpenter 6th ed)",
    ),
    ("Hedgehog", "Quill Mites (Chorioptes)"): (
        "ハリネズミのダニ症（Caparinia tripilis が最多、Chorioptes も）は針の脱落・鱗屑・痂皮の最多原因。皮膚掻爬・テープ検査で確定し、皮膚糸状菌症の混合感染も検査。"
        "セラメクチン 6-18 mg/kg 外用 q21-30日×2-3回、イベルメクチン 0.2-0.4 mg/kg SC 10-14日毎×3-5回、またはフルララネル 15 mg/kg PO 単回（Romero 2017 Vet Dermatol）。"
        "床材をすべて交換・ケージ洗浄、同居個体を同時治療。針の再生には数ヶ月。（Carpenter 6th ed; Quesenberry & Carpenter 4th ed）",
        "Hedgehog mange (Caparinia tripilis most common; also Chorioptes) is the leading cause of quill loss, scaling and crusting. Confirm by skin scraping/tape test and check for concurrent dermatophytosis. "
        "Selamectin 6-18 mg/kg topically q21-30 days × 2-3, ivermectin 0.2-0.4 mg/kg SC q10-14 days × 3-5, or fluralaner 15 mg/kg PO once (Romero 2017 Vet Dermatol). "
        "Replace all bedding, clean the cage and treat cage mates; quills take months to regrow. (Carpenter 6th ed)",
    ),
    ("Exotic Other", "Hedgehog Skin Mites (Caparinia tripilis)"): (
        "Caparinia tripilis はハリネズミの針の脱落・鱗屑の最多原因。皮膚掻爬・テープ検査で確定し、皮膚糸状菌症の混合感染も検査。"
        "セラメクチン 6-18 mg/kg 外用 q21-30日×2-3回、イベルメクチン 0.2-0.4 mg/kg SC 10-14日毎×3-5回、またはフルララネル 15 mg/kg PO 単回（Romero 2017 Vet Dermatol）。床材交換・同居個体の同時治療。（Carpenter 6th ed）",
        "Caparinia tripilis is the leading cause of quill loss and scaling in hedgehogs. Confirm by scraping/tape test and check for concurrent dermatophytosis. "
        "Selamectin 6-18 mg/kg topically q21-30 days × 2-3, ivermectin 0.2-0.4 mg/kg SC q10-14 days × 3-5, or fluralaner 15 mg/kg PO once (Romero 2017 Vet Dermatol). Replace bedding; treat cage mates. (Carpenter 6th ed)",
    ),
    ("Parakeet", "Scaly Leg Mites"): (
        "セキセイインコの疥癬（Knemidocoptes pilae — 嘴・ろう膜・脚の多孔性痂皮）。イベルメクチン 0.2 mg/kg PO または頸部無毛皮膚への局所塗布、10-14日毎に最低3回（必ず希釈して正確に計量し、原液を滴下しない）。"
        "モキシデクチン スポットオンも代替。痂皮は無理に剥がさず、ミネラルオイル/ワセリンで軟化させ自然脱落を待つ。嘴の変形が進んだら整形。木製止まり木を交換し同居鳥も治療。"
        "重度寄生は免疫低下（PBFD・栄養不良）を示唆するため基礎疾患を精査。（Ritchie & Harrison; Carpenter 6th ed）",
        "Budgerigar Knemidocoptes pilae (porous crusts on beak, cere and legs). Ivermectin 0.2 mg/kg PO or applied to bare neck skin, q10-14 days × ≥3 — always dilute and measure accurately; never drip undiluted product. "
        "Moxidectin spot-on is an alternative. Do not pick crusts; soften with mineral oil/petrolatum and let them shed. Trim deformed beaks. Replace wooden perches and treat in-contact birds. "
        "Heavy infestations suggest immunosuppression (PBFD, malnutrition) — investigate. (Ritchie & Harrison; Carpenter 6th ed)",
    ),
    ("Parakeet", "Air Sac Mite – Chronic Infestation"): (
        None,
        "Ivermectin 0.2 mg/kg PO or on bare skin, q10-14 days for at least 4-6 doses (established air-sac colonies need an extended course). Oxygen for severe dyspnea; sterile saline nebulization q12h; "
        "meloxicam 0.5-1 mg/kg PO q12-24h for airway inflammation; culture-based enrofloxacin 15 mg/kg PO q12h for secondary tracheitis/air sacculitis. "
        "Chronic Sternostoma infestation can cause irreversible tracheal/air-sac fibrosis — clicking and exercise intolerance may persist after eradication. Supplemental heat 28-30°C; weigh weekly; treat in-contact birds. (Carpenter 6th ed)",
    ),
    ("Parakeet", "Mite Infestation – Feather Mites"): (
        None,
        "Feather mites (Proctophyllodes, Dubininia) are usually of low pathogenicity compared with Knemidocoptes or Sternostoma. Ivermectin 0.2 mg/kg PO or topically (diluted, on bare neck skin), "
        "repeated q10-14 days × 3 to cover the life cycle; moxidectin spot-on alternative. Disinfect cage, perches and nest box (F10 or 1:10 bleach); discard wooden perches and natural-fibre toys; "
        "treat all in-contact birds simultaneously to prevent ping-pong reinfection. Rule out feather-destructive behaviour and PBFD when feather damage is marked. (Ritchie & Harrison)",
    ),
    ("Reptile", "Snake Mite Infestation (Ophionyssus natricis) - Severe"): (
        "ヘビダニ（Ophionyssus natricis）重度寄生。動物: 温水浸漬で体表のダニを溺死させ、イベルメクチン 0.2 mg/kg SC/PO を10-14日後に反復（**カメ類には致死的のため絶対禁忌**、インディゴスネーク等一部種も注意）、またはフィプロニルスプレーを布に取り体表を拭く（目・口を避ける）。"
        "環境: 床材をすべて廃棄して新聞紙等に替え、ケージを熱湯＋消毒剤で洗浄、隙間にダニが潜むため2週間後に反復。捕食性ダニ（Taurrus/Hypoaspis）による生物的防除も有効。"
        "重度寄生では貧血・脱水に輸液・栄養支持。ダニは封入体病（IBD）・Aeromonas の媒介者となるため隔離と新規導入個体の検疫を徹底。（Mader 3rd ed; Carpenter 6th ed）",
        "Severe Ophionyssus natricis infestation. Animal: warm-water soaks to drown surface mites; ivermectin 0.2 mg/kg SC/PO repeated in 10-14 days (**fatal to chelonians — never use in tortoises/turtles**; caution in some species such as indigo snakes), "
        "or fipronil spray applied with a cloth (avoid eyes/mouth). Environment: discard all substrate (use newspaper), clean the enclosure with hot water and disinfectant, repeat after 2 weeks (mites hide in crevices); predatory mites (Taurrus/Hypoaspis) are useful biological control. "
        "Fluid and nutritional support for anemia/dehydration. Mites can vector inclusion body disease and Aeromonas — isolate and quarantine new arrivals. (Mader 3rd ed; Carpenter 6th ed)",
    ),
    ("Exotic Other", "External Parasites (Mites/Fleas/Ticks)"): (
        "外部寄生虫の治療は動物分類群で安全な薬剤が大きく異なる — 種を確認してから選択する。"
        "小型哺乳類・フェレット: セラメクチン 6-18 mg/kg 外用、またはイベルメクチン 0.2-0.4 mg/kg SC 10-14日毎（フィプロニルはウサギ・モルモット・チンチラ・デグーに禁忌）。"
        "ヘビ・トカゲ: イベルメクチン 0.2 mg/kg（**カメ類には致死的で禁忌**）。鳥: 希釈イベルメクチン 0.2 mg/kg、環境中のワクモ対策。"
        "**節足動物（クモ・昆虫・甲殻類）にはイベルメクチン等の殺ダニ剤・殺虫剤を絶対に使用しない（致死的）**。マダニは基部をつまんで用手除去。全例で床材交換・環境清掃と同居個体の治療。（Carpenter 6th ed）",
        "Safe drugs differ sharply between taxa — identify the species first. Small mammals/ferrets: selamectin 6-18 mg/kg topically or ivermectin 0.2-0.4 mg/kg SC q10-14 days (fipronil is contraindicated in rabbits, guinea pigs, chinchillas and degus). "
        "Snakes/lizards: ivermectin 0.2 mg/kg (**fatal to chelonians**). Birds: diluted ivermectin 0.2 mg/kg plus environmental control of red mites. "
        "**Never use ivermectin or other acaricides/insecticides on arthropods (spiders, insects, crustaceans) — lethal.** Remove ticks manually by grasping at the mouthparts. In every case replace bedding, clean the enclosure and treat cage mates. (Carpenter 6th ed)",
    ),
    ("Exotic Other", "Mite Infestation (Tarantula)"): (
        "**タランチュラ（クモ類）にはイベルメクチン等の殺ダニ剤・殺虫剤を絶対に使用しない — ダニと同じクモ綱のため致死的**。"
        "多くのダニは湿った床材・食べ残しで増える腐食性の無害な土壌ダニ — 床材を交換し、食べ残しを毎日除去し、湿度を適正化する。"
        "体表のダニは湿らせた綿棒・柔らかい筆でやさしく除去（書肺・口器周囲を優先）。捕食性ダニ（Hypoaspis）による生物的防除も可。新規導入個体は隔離・検疫。（Pellett 2015 Vet Clin Exot Anim; Carpenter 6th ed）",
        "**Never use ivermectin or any acaricide/insecticide on tarantulas — as arachnids they are killed by the same drugs as mites.** "
        "Most mites are harmless detritivorous soil mites thriving on damp substrate and food remains: replace the substrate, remove uneaten prey daily and correct humidity. "
        "Remove mites from the body with a damp cotton swab or soft brush (prioritize book lungs and mouthparts). Predatory mites (Hypoaspis) can be used as biological control; quarantine new arrivals. (Pellett 2015 Vet Clin Exot Anim; Carpenter 6th ed)",
    ),
    ("Exotic Other", "Oral Nematodes (Tarantula)"): (
        "タランチュラの口器線虫症（Panagrolaimidae 科）— 口器周囲の白い粘液状物、拒食、うずくまり。**有効な治療法は確立されておらず、イベルメクチン等の駆虫薬はクモに致死的で使用しない**。"
        "罹患個体は直ちに隔離し、器具を共有しない（伝播防止）。口器周囲の物理的清拭は症状緩和にとどまる。予後は不良で、苦痛が強い場合は人道的安楽死を検討。予防は床材・餌昆虫の衛生管理と新規個体の検疫。（Pellett 2015 Vet Clin Exot Anim）",
        "Tarantula oral nematodes (Panagrolaimidae): white mucoid material around the mouthparts, anorexia, hunched posture. **No effective treatment is established; anthelmintics such as ivermectin are lethal to spiders.** "
        "Isolate affected animals immediately and do not share equipment. Cleaning the mouthparts is palliative only. Prognosis is poor — consider humane euthanasia for suffering animals. Prevent with substrate/feeder hygiene and quarantine. (Pellett 2015 Vet Clin Exot Anim)",
    ),
    ("Ferret", "Heartworm Disease"): (
        "フェレットのフィラリア症は少数寄生でも重篤（心臓が小さいため1-2隻で発症）。抗原検査は偽陰性が多く心エコーで虫体を確認。"
        "犬の3回メラルソミン法は虫体死滅時の血栓塞栓で死亡率が高く、一般に推奨されない。イベルメクチン 0.05 mg/kg SC/PO 月1回＋プレドニゾロン 0.5-1 mg/kg PO q24h（虫体死滅時の炎症抑制）を抗原陰性化まで継続するスローキル法が一般的。"
        "うっ血性心不全にはフロセミド 1-4 mg/kg q8-12h、厳重な運動制限。予防: 蚊の季節は月1回の予防（セラメクチン 18 mg/kg 外用 または イベルメクチン）。（Quesenberry & Carpenter 4th ed; American Heartworm Society）",
        "Ferret heartworm disease is severe even with 1-2 worms (small heart). Antigen tests are often falsely negative — confirm worms by echocardiography. "
        "The canine 3-dose melarsomine protocol carries high mortality from thromboembolism and is generally not recommended. The usual approach is slow-kill: ivermectin 0.05 mg/kg SC/PO monthly plus prednisolone 0.5-1 mg/kg PO q24h until antigen-negative. "
        "CHF: furosemide 1-4 mg/kg q8-12h and strict cage rest. Prevention: monthly preventive during mosquito season (selamectin 18 mg/kg topically or ivermectin). (Quesenberry & Carpenter 4th ed; American Heartworm Society)",
    ),
    ("Ferret", "Heartworm (Dirofilaria)"): (
        "フェレットのフィラリア症（Dirofilaria immitis）は1-2隻の寄生で右心不全・突然死を起こしうる。抗原検査は偽陰性が多く心エコーで確認。"
        "メラルソミン法は血栓塞栓による死亡率が高く一般に推奨されない — イベルメクチン 0.05 mg/kg 月1回＋プレドニゾロン 0.5-1 mg/kg q24h のスローキル法を抗原陰性化まで。"
        "胸水・腹水・心不全にはフロセミド 1-4 mg/kg q8-12h、厳重な安静。予防が最重要: 蚊の季節は月1回（セラメクチン 18 mg/kg 外用 または イベルメクチン）。（Quesenberry & Carpenter 4th ed; AHS）",
        "Dirofilaria immitis in ferrets: 1-2 worms can cause right heart failure or sudden death. Antigen tests are often falsely negative — confirm by echocardiography. "
        "Melarsomine carries high thromboembolic mortality and is generally not recommended — use slow-kill ivermectin 0.05 mg/kg monthly plus prednisolone 0.5-1 mg/kg q24h until antigen-negative. "
        "Effusions/CHF: furosemide 1-4 mg/kg q8-12h and strict rest. Prevention is paramount: monthly preventive during mosquito season (selamectin 18 mg/kg topically or ivermectin). (Quesenberry & Carpenter 4th ed; AHS)",
    ),
}


def is_replaceable(text: str | None) -> bool:
    t = text or ""
    return (
        not t.strip()
        or TEMPLATE_EN in t
        or TEMPLATE_JA in t
        or TEMPLATE_JA_ENDOPARASITE_WORKUP in t
        or ("正確な臨床評価（病歴、身体検査、CBC・生化学、画像）から治療方針を決定" in t)
        or ("皮膚生検（パンチまたはincisional）" in t and "皮膚糸状菌症（エキゾチック動物）" in t)
    )


def curated_treatment(species: str, name: str):
    return CURATED.get((species, name))
