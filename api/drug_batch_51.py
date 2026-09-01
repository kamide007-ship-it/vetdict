"""Drug batch 51 – referenced-but-absent agents surfaced by the 2026-09 audit (17th sweep).

The dosage-context katakana token audit (drug tokens with an explicit dose
within ~45 chars, cross-checked against find_drugs_in_text on the snippet)
found three agents that VetDict's own disease content instructs clinicians to
use — with explicit doses — yet were absent from the formulary:

  - カンナビジオール/CBD (cannabidiol): the single most-referenced absent agent
    (260 mentions). Behavioural, osteoarthritis and refractory-epilepsy
    entries cite "CBD 2 mg/kg PO q12h (McGrath 2019)" / "CBDオイル 0.5-2
    mg/kg PO q12h" across dogs, cats, horses and small mammals, yet the only
    CBD-containing entry was a sponsor supplement (not a neutral formulary
    monograph with evidence-based dosing and the CYP450/ALT safety facts).
  - L-トリプトファン (L-tryptophan): 49 references — behavioural entries cite
    "L-トリプトファン 20 mg/kg PO q24h（セロトニン前駆体）" while the sibling
    behavioural supplements (L-theanine, alpha-casozepine) are already listed.
  - hCG (human chorionic gonadotropin): 48 references — ovarian-cyst entries
    for rabbits/hamsters/guinea pigs cite "hCG 100 IU/kg IM" (ovulation
    induction / luteinisation of follicular cysts) and equine reproduction
    uses it for timed ovulation, yet no LH-activity gonadotropin existed.

References:
  - McGrath S et al. JAVMA 2019;254:1301 — randomised blinded trial: CBD
    2.5 mg/kg PO q12h as add-on in canine idiopathic epilepsy; significant
    seizure-frequency reduction vs placebo; dose-dependent ALP/ALT rise.
  - Gamble LJ et al. Front Vet Sci 2018;5:165 — CBD 2 mg/kg PO q12h in
    osteoarthritic dogs: decreased pain scores (CBPI), increased activity;
    transient ALP elevation.
  - Deabold KA et al. Animals 2019;9:832 — single-dose and chronic PK/safety
    in dogs and cats; cats show lower absorption and occasional head-shaking/
    licking; monitor ALT.
  - Vaughn D et al. Front Vet Sci 2020 — escalating-dose CBD safety in dogs.
  - DeNapoli JS et al. JAVMA 2000;217:504 — tryptophan supplementation with
    low-protein diet reduced territorial aggression scores in dogs.
  - Grimmett A, Sillence MN. Vet J 2005;170:24 — tryptophan in horses:
    calming evidence poor; low oral doses may cause mild excitement, and IV
    tryptophan causes haemolysis — oral only, adjunct only.
  - Quesenberry & Carpenter, Ferrets, Rabbits and Rodents 4th ed — hCG
    100 IU/kg IM for ovulation induction / cystic ovarian disease in small
    herbivores (functional follicular cysts; serous cysts respond poorly —
    ovariohysterectomy is definitive).
  - McCue PM, in Equine Reproduction 2nd ed — hCG 1,500-3,000 IU IV/IM to
    induce ovulation of a ≥35 mm follicle within 24-48 h in mares;
    anti-hCG antibodies with repeated cycles reduce efficacy.
  - Plumb's Veterinary Drug Handbook 10th ed — hCG: protein hormone,
    hypersensitivity/anaphylaxis possible with repeated injections.
"""

DRUGS_BATCH_51: list[dict] = [
    {
        "id": "cannabidiol",
        # "CBD" 単独は3文字Latinのためテキスト索引には載らないが、相互作用チェッカー等の
        # 完全一致解決（resolve_drug_reference）では有効
        "search_aliases": ["カンナビジオール", "CBDオイル", "CBD oil", "CBD", "Cannabidiol", "カンナビジオールオイル"],
        "name": "Cannabidiol (CBD)",
        "name_ja": "カンナビジオール（CBD）",
        "category": "supplements",
        "mechanism": "Non-intoxicating phytocannabinoid; modulates the endocannabinoid system (weak CB1/CB2 affinity), TRPV1, 5-HT1A and adenosine signalling — anxiolytic, analgesic-adjunct and anticonvulsant-adjunct effects.",
        "mechanism_ja": "非陶酔性フィトカンナビノイド。エンドカンナビノイド系（CB1/CB2への弱い親和性）、TRPV1、5-HT1A、アデノシン系を修飾し、抗不安・鎮痛補助・抗痙攣補助作用を示す。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Osteoarthritis adjunct: 2 mg/kg PO q12h (Gamble 2018). Refractory idiopathic epilepsy adjunct: 2.5 mg/kg PO q12h with conventional anticonvulsants (McGrath 2019). Behavioural anxiety adjunct: 1-2 mg/kg PO q12h. Use THC-free, third-party-assayed products only.",
                "dosage_ja": "変形性関節症の補助: 2 mg/kg 経口 12時間毎（Gamble 2018）。難治性特発性てんかんの補助: 既存抗痙攣薬に追加で 2.5 mg/kg 経口 12時間毎（McGrath 2019）。不安の補助: 1-2 mg/kg 経口 12時間毎。THCフリーで含量分析済みの製品のみ使用。",
                "notes": "Adjunct, never sole therapy for epilepsy or pain. Dose-dependent ALP/ALT elevation — check liver enzymes at baseline and q4-8 weeks. Inhibits hepatic CYP450: may raise levels of phenobarbital and other hepatically metabolised drugs.",
                "notes_ja": "てんかん・疼痛の単独治療にはしない（補助のみ）。用量依存性のALP/ALT上昇 — 開始前と4-8週毎に肝酵素を確認。肝CYP450阻害によりフェノバルビタール等の肝代謝薬の血中濃度を上昇させうる。",
            },
            "cat": {
                "safe": True,
                "dosage": "Limited data: 0.5-2 mg/kg PO q12h (Deabold 2019 PK/safety). Lower oral absorption than dogs; start low and titrate.",
                "dosage_ja": "データ限定的: 0.5-2 mg/kg 経口 12時間毎（Deabold 2019 薬物動態/安全性）。犬より経口吸収が低い — 低用量から漸増。",
                "notes": "Occasional head-shaking/excessive licking at dosing; monitor ALT. THC-containing products are toxic — THC-free only.",
                "notes_ja": "投与時に頭振り・過剰な舐め行動がまれにみられる。ALTをモニタリング。THC含有製品は中毒性 — THCフリーのみ。",
            },
            "horse": {
                "safe": True,
                "dosage": "Limited safety data: 0.5-2 mg/kg PO q12h reported for chronic pain/anxiety adjunct under veterinary supervision.",
                "dosage_ja": "安全性データ限定的: 慢性疼痛・不安の補助として獣医師監督下で 0.5-2 mg/kg 経口 12時間毎の報告。",
                "notes": "Prohibited substance in competition (FEI/racing) — withdraw well before events.",
                "notes_ja": "競技会では禁止物質（FEI・競馬）— 出走前に十分な休薬を。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Anecdotal only: 0.5-1 mg/kg PO q12h as palliative/anxiety adjunct; no controlled safety data.",
                "dosage_ja": "逸話的報告のみ: 緩和ケア・不安の補助として 0.5-1 mg/kg 経口 12時間毎。対照試験による安全性データなし。",
                "notes": "Use only when conventional options are exhausted; monitor appetite and GI motility.",
                "notes_ja": "標準治療で不十分な場合に限り使用。食欲・消化管運動をモニタリング。",
            },
            "bird": {
                "safe": False,
                "dosage": "Not recommended — no safety or efficacy data in avian species.",
                "dosage_ja": "非推奨 — 鳥類での安全性・有効性データなし。",
                "notes": "VetDict behavioural content explicitly excludes birds/reptiles/amphibians/fish from CBD use.",
                "notes_ja": "鳥類・爬虫類・両生類・魚類にはCBDを推奨しない（安全性データ欠如）。",
            },
            "reptile": {
                "safe": False,
                "dosage": "Not recommended — no safety or efficacy data in reptiles.",
                "dosage_ja": "非推奨 — 爬虫類での安全性・有効性データなし。",
                "notes": "No pharmacokinetic data; ectotherm metabolism unpredictable.",
                "notes_ja": "薬物動態データなし。変温動物の代謝は予測不能。",
            },
        },
        "side_effects": [
            "Dose-dependent ALP/ALT elevation",
            "Sedation/somnolence",
            "GI upset (soft stool, hypersalivation)",
        ],
        "side_effects_ja": ["用量依存性のALP/ALT上昇", "鎮静・傾眠", "消化器症状（軟便・流涎）"],
        "contraindications": "Significant hepatic disease (monitor closely if unavoidable); THC-containing products (canine THC toxicosis); birds/reptiles/amphibians/fish (no data).",
        "contraindications_ja": "重度肝疾患（やむを得ない場合は厳重モニタリング）。THC含有製品（犬のTHC中毒）。鳥類・爬虫類・両生類・魚類（データなし）。",
        "drug_interactions": [
            {
                "drug": "Phenobarbital",
                "severity": "moderate",
                "description": "CYP450 inhibition may raise phenobarbital levels — recheck serum levels 2-4 weeks after starting CBD",
                "description_ja": "CYP450阻害でフェノバルビタール血中濃度が上昇しうる — CBD開始2-4週後に血中濃度を再測定",
            },
            {
                "drug": "Ketoconazole/itraconazole",
                "severity": "moderate",
                "description": "Azoles inhibit CBD metabolism — additive hepatic load, monitor liver enzymes",
                "description_ja": "アゾール系がCBD代謝を阻害 — 肝負荷が相加、肝酵素をモニタリング",
            },
        ],
        "evidence": "McGrath 2019 JAVMA (epilepsy RCT); Gamble 2018 Front Vet Sci (OA); Deabold 2019 Animals (dog/cat PK & safety); Vaughn 2020 Front Vet Sci.",
        "evidence_ja": "McGrath 2019 JAVMA（てんかんRCT）、Gamble 2018 Front Vet Sci（変形性関節症）、Deabold 2019 Animals（犬猫の薬物動態・安全性）、Vaughn 2020 Front Vet Sci。",
    },
    {
        "id": "l_tryptophan",
        "search_aliases": ["トリプトファン", "L-トリプトファン", "L-tryptophan"],
        "name": "L-Tryptophan",
        "name_ja": "L-トリプトファン",
        "category": "supplements",
        "mechanism": "Essential amino acid and serotonin precursor; supplementation (especially with lower-protein diets that reduce competing large neutral amino acids) increases CNS serotonin synthesis — anxiolytic/anti-aggression adjunct.",
        "mechanism_ja": "必須アミノ酸でセロトニンの前駆体。補充（特に競合する大型中性アミノ酸を減らす低蛋白食との併用）で中枢セロトニン合成が増加 — 抗不安・攻撃行動軽減の補助。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Behavioural adjunct: 10-20 mg/kg PO q24h (or divided q12h), ideally combined with behaviour modification and, for territorial aggression, a moderately protein-restricted diet (DeNapoli 2000 JAVMA).",
                "dosage_ja": "行動学的補助: 10-20 mg/kg 経口 24時間毎（12時間毎分割も可）。行動修正療法と併用し、縄張り性攻撃行動では中等度蛋白制限食との併用が理想（DeNapoli 2000 JAVMA）。",
                "notes": "Adjunct only — never a substitute for behaviour modification or, where indicated, SSRIs/TCAs. Effect size is modest.",
                "notes_ja": "補助のみ — 行動修正療法や適応があればSSRI/TCAの代替にはならない。効果量は控えめ。",
            },
            "cat": {
                "safe": True,
                "dosage": "Anxiety/urine-marking adjunct: 10-20 mg/kg PO q24h; commercial calming diets combine tryptophan with alpha-casozepine.",
                "dosage_ja": "不安・スプレー行動の補助: 10-20 mg/kg 経口 24時間毎。市販の行動ケア食はトリプトファンとαカソゼピンを配合。",
                "notes": "Combine with environmental enrichment (litter management, vertical space, pheromones).",
                "notes_ja": "環境エンリッチメント（トイレ管理・垂直空間・フェロモン製剤）と併用。",
            },
            "chinchilla": {
                "safe": True,
                "dosage": "Stress-related disorders (fur chewing) adjunct: 20 mg/kg PO q24h.",
                "dosage_ja": "ストレス関連疾患（毛噛み）の補助: 20 mg/kg 経口 24時間毎。",
                "notes": "Address husbandry stressors first (dust bath, hiding places, cool dry environment).",
                "notes_ja": "まず飼育環境のストレス要因を是正（砂浴び・隠れ家・涼しく乾燥した環境）。",
            },
            "horse": {
                "safe": True,
                "dosage": "Oral calming-supplement doses only (evidence poor); typical products supply 1-3 g/500 kg/day. Do not exceed labelled doses.",
                "dosage_ja": "経口の鎮静サプリメント用量のみ（エビデンス乏しい）。市販製品は1-3 g/500 kg/日程度。表示用量を超えない。",
                "notes": "Low oral doses may paradoxically cause mild excitement; IV tryptophan causes haemolysis — never inject (Grimmett & Sillence 2005). Competition rules may restrict use.",
                "notes_ja": "低用量経口では逆に軽度の興奮を起こしうる。静注は溶血を起こすため絶対に注射しない（Grimmett & Sillence 2005）。競技規則で制限されうる。",
            },
        },
        "side_effects": [
            "GI upset (rare)",
            "Drowsiness at high doses",
            "Paradoxical mild excitement (horses, low doses)",
        ],
        "side_effects_ja": ["消化器症状（まれ）", "高用量での眠気", "逆説的な軽度興奮（馬・低用量）"],
        "contraindications": "Concurrent MAO inhibitors (selegiline) — serotonin syndrome risk; use caution with SSRIs/TCAs/tramadol (additive serotonergic load). Never IV in any species.",
        "contraindications_ja": "MAO阻害薬（セレギリン）併用 — セロトニン症候群リスク。SSRI/TCA/トラマドールとの併用は慎重に（セロトニン作動性負荷が相加）。全種で静注禁止。",
        "drug_interactions": [
            {
                "drug": "Selegiline",
                "severity": "major",
                "description": "MAO-B inhibitor + serotonin precursor — serotonin syndrome risk; avoid combination",
                "description_ja": "MAO-B阻害薬＋セロトニン前駆体 — セロトニン症候群リスク。併用回避",
            },
            {
                "drug": "Fluoxetine",
                "severity": "moderate",
                "description": "Additive serotonergic effect — monitor for agitation, tremor, hyperthermia",
                "description_ja": "セロトニン作動性が相加 — 興奮・振戦・高体温をモニタリング",
            },
            {
                "drug": "Tramadol",
                "severity": "moderate",
                "description": "Additive serotonergic effect — monitor for serotonin syndrome signs",
                "description_ja": "セロトニン作動性が相加 — セロトニン症候群の徴候をモニタリング",
            },
        ],
        "evidence": "DeNapoli 2000 JAVMA (canine aggression); Grimmett & Sillence 2005 Vet J (equine review).",
        "evidence_ja": "DeNapoli 2000 JAVMA（犬の攻撃行動）、Grimmett & Sillence 2005 Vet J（馬の総説）。",
    },
    {
        "id": "hcg",
        # NOTE: bare「ゴナドトロピン」は GnRH（ゴナドトロピン放出ホルモン）の部分文字列で
        # 誤マッチするため使用しない
        "search_aliases": ["ヒト絨毛性ゴナドトロピン", "コリオゴナドトロピン"],
        "name": "hCG (Human Chorionic Gonadotropin)",
        "name_ja": "hCG（ヒト絨毛性ゴナドトロピン）",
        "category": "reproductive_hormones",
        "mechanism": "LH-like glycoprotein hormone: binds LH receptors on follicles/interstitial cells, inducing ovulation or luteinisation of mature/persistent follicles and testosterone secretion from Leydig cells (diagnostic use for cryptorchidism).",
        "mechanism_ja": "LH様糖蛋白ホルモン。卵胞・間質細胞のLH受容体に結合し、成熟卵胞・遺残卵胞の排卵/黄体化を誘導。ライディッヒ細胞からのテストステロン分泌も刺激（潜在精巣の診断的使用）。",
        "species_info": {
            "guinea_pig": {
                "safe": True,
                "dosage": "Cystic ovarian disease (functional follicular cysts): 100 IU/kg (or 1,000 IU/animal) IM, repeat in 7-14 days if needed (Quesenberry & Carpenter 4th ed).",
                "dosage_ja": "卵巣嚢胞（機能性濾胞嚢胞）: 100 IU/kg（または1,000 IU/頭）筋注、必要なら7-14日後に再投与（Quesenberry & Carpenter 4th ed）。",
                "notes": "Serous (non-functional) cysts — the most common type — respond poorly; ovariohysterectomy is definitive. hCG is palliative/temporising.",
                "notes_ja": "最多の漿液性（非機能性）嚢胞には反応不良 — 卵巣子宮摘出術が根治的。hCGは一時的緩和。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Ovarian cyst / ovulation induction: 100 IU/kg IM single dose.",
                "dosage_ja": "卵巣嚢胞・排卵誘起: 100 IU/kg 筋注 単回。",
                "notes": "Temporary relief only — recurrence common; ovariohysterectomy definitive. Rabbits are induced ovulators.",
                "notes_ja": "効果は一時的 — 再発が多く、卵巣子宮摘出術が根治的。ウサギは交尾排卵動物。",
            },
            "hamster": {
                "safe": True,
                "dosage": "Ovarian cyst: 100 IU/kg IM single dose; reassess by ultrasound in 2 weeks.",
                "dosage_ja": "卵巣嚢胞: 100 IU/kg 筋注 単回。2週間後に超音波で再評価。",
                "notes": "Surgical ovariohysterectomy preferred in stable patients.",
                "notes_ja": "状態が安定していれば卵巣子宮摘出術を優先。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Persistent estrus / estrogen toxicity (induced ovulator): 100 IU/animal IM single dose; vulvar swelling should regress within 72 h — repeat once in 7 days if incomplete (Quesenberry & Carpenter 4th ed).",
                "dosage_ja": "発情持続・エストロジェン中毒（交尾排卵動物）: 100 IU/頭 筋注 単回。外陰膨大は72時間以内に退縮 — 不十分なら7日後に1回反復（Quesenberry & Carpenter 4th ed）。",
                "notes": "Early intervention can allow bone-marrow recovery in estrogen-induced aplastic anemia; established pancytopenia needs transfusion support. Spay (or deslorelin implant) prevents recurrence.",
                "notes_ja": "エストロジェン性再生不良性貧血は早期介入で骨髄回復の可能性。汎血球減少が確立した例は輸血支持が必要。避妊手術（またはデスロレリンインプラント）で再発予防。",
            },
            "horse": {
                "safe": True,
                "dosage": "Timed ovulation induction: 1,500-3,000 IU IV/IM when a ≥35 mm follicle with endometrial oedema is present — ovulation within 24-48 h (McCue, Equine Reproduction 2nd ed).",
                "dosage_ja": "排卵時期の調整: 子宮内膜浮腫を伴う35 mm以上の卵胞がある時点で1,500-3,000 IU 静注/筋注 — 24-48時間以内に排卵（McCue, Equine Reproduction 2nd ed）。",
                "notes": "Anti-hCG antibody formation with repeated cycles (≥2-3/season) blunts response — consider deslorelin instead for repeat inductions.",
                "notes_ja": "繁殖シーズン内の反復投与（2-3回以上）で抗hCG抗体が形成され反応が鈍化 — 反復誘起にはデスロレリンを検討。",
            },
            "dog": {
                "safe": True,
                "dosage": "Ovulation induction in prolonged proestrus / follicular cysts: 22 IU/kg IM q24-48h ×1-3. Cryptorchidism diagnosis (testosterone stimulation test): 44 IU/kg IM with pre/post testosterone.",
                "dosage_ja": "発情前期遷延・卵胞嚢胞の排卵誘起: 22 IU/kg 筋注 24-48時間毎 1-3回。潜在精巣の診断（テストステロン刺激試験）: 44 IU/kg 筋注、前後でテストステロン測定。",
                "notes": "Medical management of follicular cysts often fails — ovariohysterectomy definitive.",
                "notes_ja": "卵胞嚢胞の内科管理は不成功が多い — 卵巣子宮摘出術が根治的。",
            },
        },
        "side_effects": [
            "Hypersensitivity/anaphylaxis (protein hormone, repeated injections)",
            "Injection-site pain",
            "Antibody formation reducing efficacy",
        ],
        "side_effects_ja": [
            "過敏症・アナフィラキシー（蛋白ホルモン、反復注射で）",
            "注射部位痛",
            "抗体形成による効果減弱",
        ],
        "contraindications": "Prior hypersensitivity reaction; hormone-responsive neoplasia (mammary/ovarian tumours); pregnancy.",
        "contraindications_ja": "過去の過敏症反応。ホルモン反応性腫瘍（乳腺・卵巣腫瘍）。妊娠中。",
        "drug_interactions": [],
        "evidence": "Quesenberry & Carpenter 4th ed (small herbivore ovarian cysts); McCue, Equine Reproduction 2nd ed (mare ovulation induction); Plumb's 10th ed.",
        "evidence_ja": "Quesenberry & Carpenter 4th ed（小型草食獣の卵巣嚢胞）、McCue, Equine Reproduction 2nd ed（馬の排卵誘起）、Plumb's 10th ed。",
    },
]
