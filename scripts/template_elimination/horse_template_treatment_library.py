"""Curated equine treatment protocols replacing wrong-species templates — 2026-11 第83弾.

Twenty horse records still carried templates in their treatment fields:

* English: an exotic small-mammal template ("Pain management: meloxicam
  0.2-0.5 mg/kg q24-48h ... (Ref: Quesenberry & Carpenter 2012)") — a small-
  mammal dose (the equine meloxicam dose is 0.6 mg/kg) and an exotics textbook.
* Japanese dental entries: a small-animal dental template stating that equine
  dental work "requires general anaesthesia" (routine equine dentistry is done
  standing under sedation with a full-mouth speculum; GA is reserved for
  selected extractions/surgery).
* Japanese: the generic work-up template (PSSM, MFM, tumours, jaw
  malocclusions), an antibacterial template on a virus (Equine Pegivirus), and
  a small-animal endocrine template on equine hyperadrenocorticism (= PPID).

Evidence: Easley J, Dixon PM, Schumacher J (eds). Equine Dentistry 3rd ed
(2011). Dixon PM, Dacre I. A review of equine dental disorders. Vet J 2005;
169:165-187. Valberg SJ. Muscle conditions affecting sport horses. Vet Clin
Equine 2018;34:253-276. Williams ZJ et al. Dietary amino acid supplementation
in myofibrillar myopathy. Equine Vet J 2018. Reed SM, Bayly WM, Sellon DC.
Equine Internal Medicine 4th ed (2018). Knottenbelt DC. Pascoe's Principles
and Practice of Equine Dermatology 2nd ed (2009). Equine Endocrinology Group
PPID recommendations (2021). Tomlinson JE et al. Equine pegiviruses. Vet
Microbiol 2020. Southwood LL. Practical Guide to Equine Colic / urolithiasis
(Duesterdieck-Zellmer KF, Equine urolithiasis, Vet Clin Equine 2007;23:613-629).
"""

SEDATION_EN = (
    "standing sedation (detomidine 0.01-0.02 mg/kg IV + butorphanol 0.01-0.02 mg/kg IV) "
    "with a full-mouth speculum and head support"
)
SEDATION_JA = (
    "立位鎮静（デトミジン 0.01-0.02 mg/kg IV＋ブトルファノール 0.01-0.02 mg/kg IV）下で開口器を装着し頭部を支持して実施"
)
ANALGESIA_EN = "phenylbutazone 2.2-4.4 mg/kg PO q12-24h or flunixin 1.1 mg/kg PO/IV q24h for 1-3 days"
ANALGESIA_JA = "フェニルブタゾン 2.2-4.4 mg/kg PO 12-24時間毎またはフルニキシン 1.1 mg/kg PO/IV 24時間毎を1-3日"
DENT_REF = "(Easley, Dixon & Schumacher, Equine Dentistry 3rd ed 2011; Dixon & Dacre, Vet J 2005)"

HORSE_TREATMENTS: dict[str, tuple[str, str]] = {
    "Sharp Enamel Points": (
        f"Routine dental correction ('floating') under {SEDATION_EN}: reduce the buccal points of "
        "the maxillary and lingual points of the mandibular cheek teeth with hand rasps or a "
        "motorised burr, using intermittent contact and water cooling to avoid thermal pulp "
        "damage; remove only the sharp overgrowth, not occlusal surface. Treat buccal/lingual "
        "ulcers by removing the cause (they heal within about 1-2 weeks). Re-examine every "
        f"6-12 months (more often in young and aged horses). General anaesthesia is not required. {DENT_REF}",
        f"定期的な歯科矯正（フローティング）を{SEDATION_JA}。上顎臼歯の頬側・下顎臼歯の舌側の鋭利点を"
        "手用ラスプまたは電動バーで除去する（歯髄の熱損傷を避けるため断続的に当て、注水冷却する。咬合面は"
        "削りすぎず鋭利な過長部のみを除去）。頬粘膜・舌の潰瘍は原因除去で約1-2週で治癒する。6-12ヶ月毎に"
        "再検査（若齢馬・高齢馬はより頻回）。全身麻酔は不要。" + DENT_REF,
    ),
    "Wolf Teeth": (
        f"Extract when bit-related problems, displaced ('blind') or fractured wolf teeth are present. "
        f"Under {SEDATION_EN} plus local infiltration (mepivacaine), loosen the periodontal ligament "
        "with a wolf-tooth elevator and extract the whole tooth including the root; avoid the palatine "
        f"artery medially. Post-extraction analgesia: {ANALGESIA_EN}; no bit for about 1-2 weeks. "
        f"Normally erupted, non-problematic wolf teeth need not be removed. {DENT_REF}",
        "ハミ受けの問題・変位（埋伏・ブラインド）・破折がある狼歯は抜歯する。"
        f"{SEDATION_JA}し、局所浸潤麻酔（メピバカイン）を併用。狼歯用エレベーターで歯根膜を剥離し歯根ごと"
        f"抜去する（内側の口蓋動脈を損傷しない）。抜歯後の鎮痛: {ANALGESIA_JA}。約1-2週はハミを使用しない。"
        "正常に萌出し問題のない狼歯は必ずしも抜歯不要。" + DENT_REF,
    ),
    "Retained Deciduous Teeth (Caps)": (
        "Remove only caps that are loose, displaced or causing discomfort (typically at 2.5-4.5 "
        f"years of age), using cap extractors under {SEDATION_EN}. Do not remove firmly attached "
        "caps prematurely, as the immature permanent tooth beneath can be damaged. Retained caps can "
        "cause eruption cysts/bumps and delayed eruption; radiograph when a swelling persists. "
        f"{DENT_REF}",
        "ぐらつき・変位・不快感の原因となっている乳歯冠（キャップ、通常2.5-4.5歳）のみを、"
        f"{SEDATION_JA}してキャップ抜去鉗子で除去する。強固に付着したキャップを早期に外すと下の未成熟な"
        "永久歯を傷つけるため行わない。遺残キャップは萌出嚢胞（顎の膨隆）や萌出遅延の原因となるため、"
        "腫脹が持続する場合はX線撮影を行う。" + DENT_REF,
    ),
    "Overjet (Parrot Mouth)": (
        "Congenital mandibular brachygnathia: the incisors do not meet, and rostral hooks on the "
        "upper first cheek teeth (106/206) and caudal hooks on the lower last cheek teeth (311/411) "
        f"develop. Manage with corrective reduction of incisors and hooks every 3-6 months under "
        f"{SEDATION_EN}. In foals under about 6 months, orthodontic correction (tension-band wiring "
        "or an acrylic bite plate to slow premaxillary growth) can improve occlusion. The defect is "
        f"considered heritable — advise against breeding. {DENT_REF}",
        "先天性の下顎短小（下顎の後退）。切歯が咬合せず、上顎第一臼歯（106/206）の吻側フックと下顎"
        "最後臼歯（311/411）の尾側フックが形成される。3-6ヶ月毎に切歯とフックの矯正的削合を"
        f"{SEDATION_JA}する。約6ヶ月齢未満の子馬では歯科矯正（テンションバンドワイヤーやアクリル"
        "バイトプレートで切歯骨の成長を抑制）で咬合が改善しうる。遺伝性と考えられるため繁殖は勧めない。" + DENT_REF,
    ),
    "Prognathism (Parrot Mouth / Overshot Jaw)": (
        "Overshot jaw (relative mandibular shortening): manage as for parrot mouth — corrective "
        f"reduction of overgrown incisors and rostral/caudal cheek-teeth hooks every 3-6 months under "
        f"{SEDATION_EN}; orthodontic correction (tension-band wiring/acrylic bite plate) in foals "
        f"under about 6 months. Heritable — advise against breeding. {DENT_REF}",
        "上顎前突（相対的な下顎短小）。パロットマウスと同様に、過長切歯と臼歯の吻側・尾側フックの"
        f"矯正的削合を3-6ヶ月毎に{SEDATION_JA}する。約6ヶ月齢未満の子馬では歯科矯正（テンションバンド"
        "ワイヤー/アクリルバイトプレート）を検討。遺伝性のため繁殖は勧めない。" + DENT_REF,
    ),
    "Brachygnathism (Sow Mouth / Undershot Jaw)": (
        "Undershot jaw (sow mouth; relative maxillary shortening — the mandibular incisors lie rostral "
        "to the maxillary incisors): less common than parrot mouth. Correct the resulting overgrowths "
        f"(caudal maxillary and rostral mandibular cheek-teeth hooks, incisor overgrowth) every 3-6 "
        f"months under {SEDATION_EN}. Heritable — advise against breeding. {DENT_REF}",
        "下顎前突（サウマウス、相対的な上顎短小 — 下顎切歯が上顎切歯より吻側）。パロットマウスより少ない。"
        "生じる過長部（上顎臼歯の尾側フック・下顎臼歯の吻側フック・切歯の過長）を3-6ヶ月毎に"
        f"{SEDATION_JA}して矯正的に削合する。遺伝性のため繁殖は勧めない。" + DENT_REF,
    ),
    "Dental Caries": (
        "Grade the lesion clinically and radiographically (CT where available). Peripheral caries: "
        "reduce fermentable/acidic feeds (haylage, molasses), improve forage, and level the occlusal "
        "surface; mild lesions arrest. Infundibular caries of maxillary cheek teeth: monitor early "
        "grades; debride and restore (filling) advanced lesions; extract when the tooth is fractured "
        f"or has apical infection (sinusitis, facial swelling). Procedures under {SEDATION_EN}. {DENT_REF}",
        "臨床所見とX線（可能ならCT）で病変をグレード評価する。周辺性齲蝕: 発酵性・酸性飼料（ヘイレージ・"
        "糖蜜）を減らし粗飼料を見直し、咬合面を整える（軽度病変は進行が止まる）。上顎臼歯の漏斗部齲蝕: "
        "初期は経過観察、進行例は清掃・修復（充填）、歯の破折や根尖感染（副鼻腔炎・顔面腫脹）があれば"
        f"抜歯。処置は{SEDATION_JA}。" + DENT_REF,
    ),
    "Displaced / Malerupted Tooth": (
        "Image the arcade (radiography/CT) to define displacement and diastemata. Clean impacted feed "
        "from diastemata and periodontal pockets; reduce overgrowths that drive the displacement; "
        "widen valve diastemata with a burr where indicated; extract severely displaced teeth or those "
        f"with periapical infection. Procedures under {SEDATION_EN}; feed soaked/short-chop forage "
        f"to reduce impaction. {DENT_REF}",
        "X線/CTで歯列の変位と歯間離開（ジアステマ）を評価する。ジアステマと歯周ポケットに詰まった飼料を"
        "洗浄除去し、変位を助長する過長部を削合する。必要に応じてバーで弁状ジアステマを拡大し、高度に変位した"
        f"歯や根尖感染のある歯は抜歯する。処置は{SEDATION_JA}。飼料の詰まりを減らすため浸漬・短切の粗飼料を"
        "与える。" + DENT_REF,
    ),
    "Polysaccharide Storage Myopathy (PSSM)": (
        "PSSM1 (GYS1 mutation): diet and exercise are the treatment. Feed forage with <10% "
        "non-structural carbohydrate (NSC; soak hay if needed), eliminate grain and sweet feed, and add "
        "fat for calories (e.g. vegetable oil or rice bran, introduced gradually). Daily turnout and a "
        "gradually increasing exercise programme are essential — avoid stall confinement. Acute "
        "episode: stop exercise, give flunixin 1.1 mg/kg IV once hydrated, IV fluids if myoglobinuria, "
        "monitor CK/AST and renal values. (Valberg, Vet Clin Equine 2018)",
        "PSSM1型（GYS1変異）: 治療の中心は食事と運動。非構造性炭水化物（NSC）<10%の粗飼料（必要なら"
        "乾草を浸水）、穀類・スイートフィードを除去し、カロリーは脂肪（植物油・米ぬかを漸増）で補う。"
        "毎日の放牧と段階的に増やす運動プログラムが必須（馬房内拘束を避ける）。急性発作: 運動を中止し、"
        "脱水補正後にフルニキシン 1.1 mg/kg IV、ミオグロビン尿があれば静脈輸液、CK/AST と腎機能を監視。"
        "（Valberg, Vet Clin Equine 2018）",
    ),
    "Polysaccharide Storage Myopathy Type 2": (
        "PSSM2 is a histological diagnosis (abnormal polysaccharide without the GYS1 mutation). In "
        "Quarter Horse types manage as PSSM1 (NSC <10%, fat for calories, daily turnout and regular "
        "exercise). In Warmbloods/Arabians many cases are myofibrillar myopathy: feed a moderate-NSC "
        "diet with high-quality protein (amino-acid supplement rich in lysine and threonine) and "
        "vitamin E rather than high fat, with consistent daily exercise. Acute episodes: rest, flunixin "
        "1.1 mg/kg IV once hydrated, fluids if myoglobinuria. (Valberg, Vet Clin Equine 2018; "
        "Williams et al., Equine Vet J 2018)",
        "PSSM2型は組織学的診断（GYS1変異を伴わない異常多糖）。クォーターホース系はPSSM1型と同様に管理"
        "（NSC<10%、カロリーは脂肪、毎日の放牧と定期運動）。温血種・アラブ種の多くは筋線維性ミオパチー"
        "であり、高脂肪ではなく中等度NSCの食事に良質な蛋白質（リジン・スレオニンに富むアミノ酸サプリ）と"
        "ビタミンEを加え、毎日一定の運動を行う。急性発作: 安静、脱水補正後にフルニキシン 1.1 mg/kg IV、"
        "ミオグロビン尿があれば輸液。（Valberg, Vet Clin Equine 2018; Williams et al., Equine Vet J 2018）",
    ),
    "Myofibrillar Myopathy": (
        "Myofibrillar myopathy (Arabians, Warmbloods; exercise intolerance, poor performance): no "
        "specific cure. Feed a balanced diet with high-quality protein — an amino-acid supplement rich "
        "in lysine and threonine — plus vitamin E and other antioxidants; high-fat/very-low-starch "
        "diets are not specifically indicated. Maintain consistent daily exercise with adequate warm-up; "
        "avoid prolonged rest. Treat acute episodes like exertional rhabdomyolysis (rest, NSAID once "
        "hydrated, fluids). (Valberg, Vet Clin Equine 2018; Williams et al., Equine Vet J 2018)",
        "筋線維性ミオパチー（アラブ種・温血種、運動不耐性・パフォーマンス低下）: 特異的治療はない。"
        "良質な蛋白質（リジン・スレオニンに富むアミノ酸サプリ）とビタミンE等の抗酸化物質を含むバランス食を"
        "与える（高脂肪・極低澱粉食の特別な適応はない）。十分なウォームアップを伴う毎日一定の運動を維持し、"
        "長期の休養を避ける。急性発作は労作性横紋筋融解症に準じて治療（安静、脱水補正後のNSAID、輸液）。"
        "（Valberg, Vet Clin Equine 2018; Williams et al., Equine Vet J 2018）",
    ),
    "Hemangioma": (
        "Benign vascular tumour, most often in young horses (skin of the limbs, sometimes congenital). "
        "Biopsy to exclude hemangiosarcoma. Complete surgical excision is curative; cryotherapy or laser "
        "ablation for small or surgically difficult lesions. Recurrence follows incomplete excision. "
        "Haemorrhage can be brisk — plan haemostasis. (Knottenbelt, Pascoe's Principles and Practice "
        "of Equine Dermatology 2nd ed 2009)",
        "良性の血管腫瘍で若齢馬に多い（四肢の皮膚、先天性のこともある）。生検で血管肉腫を除外する。"
        "完全な外科的切除で治癒し、小型病変や切除困難例には凍結療法・レーザー焼灼を用いる。不完全切除では"
        "再発する。出血が多いことがあるため止血を準備する。（Knottenbelt, Pascoe's Principles and "
        "Practice of Equine Dermatology 2nd ed 2009）",
    ),
    "Neurofibroma": (
        "Peripheral nerve sheath tumour, typically on the eyelids/periocular skin of young horses. "
        "Confirm by biopsy (differentiate from sarcoid). Wide surgical excision, combined with "
        "cryotherapy or intralesional cisplatin for eyelid lesions where margins are limited; recurrence "
        "after excision is common, so monitor and re-treat early. Preserve eyelid function to protect "
        "the cornea. (Knottenbelt, Pascoe's Principles and Practice of Equine Dermatology 2nd ed 2009)",
        "末梢神経鞘腫瘍で、若齢馬の眼瞼・眼周囲皮膚に好発する。生検で確定（サルコイドとの鑑別）。"
        "広範な外科的切除を行い、切除縁を確保しにくい眼瞼病変には凍結療法またはシスプラチン腫瘍内投与を"
        "併用する。切除後の再発が多いため経過観察し早期に再治療する。角膜保護のため眼瞼機能を温存する。"
        "（Knottenbelt, Pascoe's Principles and Practice of Equine Dermatology 2nd ed 2009）",
    ),
    "Equine Pegivirus": (
        "Equine pegivirus is a common, persistent and apparently non-pathogenic infection; no antiviral "
        "or antibacterial treatment is indicated. It was formerly linked to Theiler's disease, which is "
        "now attributed to equine parvovirus-hepatitis — if liver disease is present, work up hepatitis "
        "(GGT, bile acids, ultrasound) and treat supportively. Reduce iatrogenic spread by avoiding "
        "biological products of equine origin from untested donors. (Tomlinson et al., Vet Microbiol "
        "2020; Reed, Bayly & Sellon, Equine Internal Medicine 4th ed)",
        "馬ペギウイルスは一般的で持続感染するが病原性は明らかでない感染症であり、抗ウイルス薬・抗菌薬の"
        "適応はない。かつてタイラー病との関連が指摘されたが、現在は馬パルボウイルス（肝炎型）が原因と"
        "されている — 肝疾患がある場合は肝炎の精査（GGT・胆汁酸・超音波）と支持療法を行う。未検査の供血馬"
        "由来の馬血清製剤を避け、医原性伝播を減らす。（Tomlinson et al., Vet Microbiol 2020; Reed, Bayly & "
        "Sellon, Equine Internal Medicine 4th ed）",
    ),
    "Hyperadrenocorticism": (
        "In horses, hyperadrenocorticism is almost always pituitary pars intermedia dysfunction (PPID) "
        "rather than an adrenal tumour. Treat with pergolide 2 µg/kg PO q24h, adjusting by clinical "
        "response and repeat basal ACTH 4-6 weeks after starting or changing the dose; manage concurrent "
        "insulin dysregulation (low-NSC diet), laminitis risk, regular clipping, dental care, parasite "
        "control and hoof care. Pergolide inappetence: start low and increase over days. Trilostane is "
        "not first-line in horses. (Equine Endocrinology Group PPID recommendations 2021)",
        "馬の副腎皮質機能亢進症はほぼ全てが副腎腫瘍ではなく下垂体中葉機能障害（PPID）である。ペルゴリド "
        "2 µg/kg PO 24時間毎で治療し、臨床反応と開始・用量変更の4-6週後の基礎ACTH再測定で調整する。"
        "併発するインスリン調節異常（低NSC食）・蹄葉炎リスク・定期的な毛刈り・歯科・寄生虫・蹄の管理を行う。"
        "ペルゴリドによる食欲低下は低用量から数日かけて増量して回避する。トリロスタンは馬の第一選択ではない。"
        "（Equine Endocrinology Group PPID recommendations 2021）",
    ),
    "Cystic Urolithiasis (Bladder Stones)": (
        "Equine uroliths are mostly calcium carbonate. Remove the stone surgically or by lithotripsy: "
        "standing laser or electrohydraulic lithotripsy via the urethra (mares, some geldings), "
        "perineal urethrotomy with fragmentation, or laparocystotomy for large stones. Treat secondary "
        "cystitis by urine culture and sensitivity (e.g. trimethoprim-sulfonamide 30 mg/kg PO q12h). "
        "Prevention: reduce dietary calcium (limit alfalfa), ensure water and salt intake, monitor "
        "recurrence by ultrasound. Rule out underlying renal disease and bladder paralysis. "
        "(Duesterdieck-Zellmer, Vet Clin Equine 2007)",
        "馬の尿石の大部分は炭酸カルシウム。結石は外科的に、または砕石術で除去する: 尿道経由の立位レーザー"
        "・電気水圧砕石術（雌馬・一部の騸馬）、会陰尿道切開と破砕、大型結石には開腹膀胱切開術。続発性膀胱炎は"
        "尿培養・感受性試験に基づき治療（例: トリメトプリム・サルファ剤 30 mg/kg PO 12時間毎）。予防: 食事中"
        "カルシウムを減らし（アルファルファを制限）、飲水と塩分摂取を確保し、超音波で再発を監視する。基礎的な"
        "腎疾患と膀胱麻痺を除外する。（Duesterdieck-Zellmer, Vet Clin Equine 2007）",
    ),
}

# English mirrors of already-curated Japanese protocols (JA kept as is).
HORSE_EN_ONLY: dict[str, str] = {
    "Fire Ant Bites": (
        "[Local care] Wash the ants off with running water (do not rub). Dexamethasone 0.05 mg/kg IV "
        "(severe swelling or systemic reaction). Flunixin 1.1 mg/kg IV/PO (pain, inflammation). "
        "Antihistamine: diphenhydramine 0.5 mg/kg IM (to reduce pruritus). Topical corticosteroid cream "
        "(hydrocortisone 1%). Do not burst the pustules (prevents secondary infection). [Coronary-band "
        "stings] Coronary swelling and lameness: protective bandage, flunixin; in severe cases soak in "
        "warm Epsom-salt water. [Anaphylaxis (rare)] Epinephrine 0.01 mg/kg IV + dexamethasone 0.2 "
        "mg/kg IV + rapid IV fluids. [Nest control] Eliminate mounds on the premises with an "
        "abamectin- or hydramethylnon-based fire-ant bait to prevent recurrence."
    ),
    "Stocking Up": (
        "[Core treatment: exercise is most effective] Walking/trotting for 20-30 minutes promotes "
        "lymphatic return and produces marked improvement within hours; turnout (free exercise) is the "
        "definitive solution — establish a daily exercise routine. [Bandaging] Standing wraps from the "
        "cannon to above the fetlock overnight, removed the next morning; avoid over-tight wraps (skin "
        "necrosis, pressure on the periosteum). [Cold hosing] Cold-water hosing for 5-10 minutes "
        "temporarily reduces oedema. [Massage] Distal-to-proximal compressive massage (lymphatic "
        "drainage). [Severe or persistent cases] If not improved by exercise, rule out other causes: "
        "lymphangitis, cardiac disease (right heart failure), hypoproteinaemia (albumin <2.0 g/dL), "
        "venous thrombosis. [Long-term] Improve confinement (pasture, larger stall, paddock) and manage "
        "dietary salt and water (high-salt feeds worsen oedema)."
    ),
    "Insect Bite Hypersensitivity": (
        "[Acute flare (intense pruritus)] Dexamethasone 0.05-0.1 mg/kg IV/PO for 5-7 days, then taper; "
        "prednisolone 1.0-2.0 mg/kg PO once daily (SID; moderate cases). Antihistamine: cetirizine 0.4 mg/kg PO "
        "twice daily (BID; about 10 times the human dose is needed; risk of QTc prolongation). Topical fluocinolone "
        "spray or triamcinolone cream; protective dressings over excoriated areas. [Long-term "
        "management — prevention is central] Vector control: permethrin-containing repellent sprays "
        "over the whole body q12-24h; full fly sheets/body covers (Culicoides cannot reach covered "
        "skin); stable the horse at dusk and dawn (Culicoides are crepuscular/nocturnal); fans "
        "(Culicoides are weak fliers and cannot fly in wind >3 m/s); fine-mesh insect netting. "
        "[Immunotherapy] Allergen-specific immunotherapy with Culicoides extract by incremental "
        "subcutaneous injection for at least 1 year; onset takes 3-6 months and long-term continuation "
        "is needed (improvement in about 60%). [Secondary (2°) infection] Bacterial pyoderma: penicillin G + "
        "TMP-SMX. [Adjuncts] Omega-3 fatty acids (DHA/EPA), vitamin E and zinc supplementation."
    ),
    "Equine Nodular Necrosis": (
        "[Treatment usually unnecessary (benign course)] Observation is the first choice; most nodules "
        "are asymptomatic and painless and do not affect performance. [When cosmetic or saddle/tack "
        "friction is a problem] Surgical excision under local anaesthesia with complete removal and "
        "margins; electrocautery for small single lesions; intralesional triamcinolone 10-20 mg (shrinks "
        "and softens nodules; recurrence possible). [After excision] Penicillin G for 5 days to prevent "
        "secondary infection. [Monitoring] Rapid enlargement, ulceration or inflammation warrants "
        "biopsy to differentiate malignancy (e.g. sarcoma)."
    ),
}

# Orthopaedic records whose JA column carried the work-up template and whose EN
# column was the generic "Equine orthopedic disease" list.
HORSE_TREATMENTS.update(
    {
        "Angular Limb Deformities": (
            "Foals: first assess for incomplete ossification of the cuboidal bones (radiographs) — if "
            "present, restrict exercise and support the limb (splints/tube casts) until ossified. Mild "
            "physeal deviations: controlled exercise (small paddock), corrective hoof trimming and "
            "glue-on extensions; many correct spontaneously. Surgical correction must be done while the "
            "relevant physis is still active — early for the fetlock (distal MC3/MT3, within the first "
            "weeks to about 2 months of age) and later for the carpus/tarsus: growth acceleration "
            "(periosteal transection/elevation) or growth retardation (transphyseal screw or bridge), "
            "removing implants once the limb is straight to prevent overcorrection. (Auer & Stick, "
            "Equine Surgery 5th ed)",
            "子馬ではまずX線で立方骨の不完全骨化を評価し、あれば運動制限とスプリント/チューブキャストで骨化まで"
            "支持する。軽度の成長板性の偏位: 制限運動（小さなパドック）、矯正削蹄・接着式エクステンションで、"
            "多くは自然矯正される。外科的矯正は該当する成長板が活動中に行う必要がある — 球節（MC3/MT3"
            "遠位）は早期（生後数週〜約2ヶ月まで）、手根・足根はより遅くまで: 成長促進（骨膜切開・挙上）または"
            "成長抑制（経骨端板スクリュー・ブリッジ）。肢軸が真っすぐになったら過矯正を防ぐためインプラントを"
            "除去する。（Auer & Stick, Equine Surgery 5th ed）",
        ),
        "Capped Elbow": (
            "Olecranon (subcutaneous) bursitis, usually from trauma by the shoe heel while lying down. "
            "Remove the cause: shoe-boil roll (doughnut) around the pastern, shorten or roll the heel of "
            "the shoe, and provide deep bedding. Acute: cold therapy; aseptic aspiration followed by "
            "intrabursal corticosteroid with a pressure bandage. Chronic fibrotic or recurrent lesions: "
            "surgical excision of the bursa or drainage. Infected bursae: culture, lavage and systemic "
            "antimicrobials. (Auer & Stick, Equine Surgery 5th ed)",
            "肘頭の皮下滑液包炎で、横臥時の蹄鉄の鉄尾による外傷が主因。原因を除去する: 繋部にシューボイル"
            "ロール（ドーナツ）を装着し、蹄鉄の鉄尾を短く・丸め、深い敷料を用意する。急性期: 冷却療法、無菌的"
            "穿刺吸引後の滑液包内コルチコステロイド注入と圧迫包帯。慢性の線維化・再発例: 滑液包の外科的切除"
            "または排液。感染例: 培養・洗浄と全身抗菌薬。（Auer & Stick, Equine Surgery 5th ed）",
        ),
        "Fistulous Withers": (
            "Septic supraspinous bursitis. Test for Brucella abortus (serology) before handling — it is "
            "zoonotic, so wear protection and follow national reporting rules. Culture the drainage "
            "(Brucella, Actinomyces, Streptococcus). Definitive treatment is surgical: radical "
            "debridement or en bloc excision of the bursa and necrotic tissue (including affected "
            "dorsal spinous processes and nuchal ligament) with ventral drainage, then daily lavage. "
            "Systemic antimicrobials based on culture and continued for weeks; prolonged wound "
            "management and recurrence are common. (Auer & Stick, Equine Surgery 5th ed; Reed, Bayly & "
            "Sellon, Equine Internal Medicine 4th ed)",
            "化膿性の棘上滑液包炎。処置前にBrucella abortus（血清検査）を確認する — 人獣共通感染症のため防護"
            "具を着用し、国の届出規則に従う。排膿液を培養（Brucella・Actinomyces・Streptococcus）。根治は"
            "外科的: 滑液包と壊死組織（侵された胸椎棘突起・項靱帯を含む）の徹底的な郭清または一括切除と腹側排液、"
            "その後の毎日の洗浄。培養に基づく全身抗菌薬を数週間継続する。創傷管理は長期に及び再発も多い。"
            "（Auer & Stick, Equine Surgery 5th ed; Reed, Bayly & Sellon, Equine Internal Medicine 4th ed）",
        ),
    }
)
