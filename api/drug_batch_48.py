"""Drug batch 48 – referenced-but-absent agents surfaced by the 2026-08 audit (17th sweep).

(Authored in parallel with batch 47 — the sibling session claimed the 47 slot
on main first, so this session's three agents ship as batch 48.)

The dose-context katakana token audit (treatment texts cross-checked against the
live find_drugs_in_text matcher) found three agents that VetDict's own disease
content instructs clinicians to use — with explicit doses — yet were absent
from the formulary:

  - イソクスプリン (isoxsuprine): both equine navicular entries cite
    "イソクスプリン 0.6 mg/kg PO q12h（末梢血管拡張）" as a named medical
    option, yet the classic (if evidence-limited) navicular vasodilator was
    absent from the dictionary.
  - 次サリチル酸ビスマス (bismuth subsalicylate): the ferret/hamster
    Helicobacter triple-therapy entries cite "ビスマス次サリチル酸
    17.5 mg/kg PO q8h ×14日" — 7 references — yet the third leg of the
    classic H. mustelae regimen was absent.
  - ビオチン (biotin): 28 references — the equine navicular/hoof-quality
    supplement ("バイオチン 15-25 mg/日"), the reptile biotin-deficiency
    entry (raw egg-white avidin), and multiple dermatology coat-quality
    mentions — with no formulary entry.

References:
  - Rose RJ et al. Equine Vet J 1983;15:238 — isoxsuprine 0.6 mg/kg PO q12h
    improved lameness scores in navicular disease (original controlled trial).
  - Erkert RS & MacAllister CG. Equine Vet J 2002 — oral isoxsuprine has poor
    bioavailability in horses; efficacy is debated. FEI/racing prohibited
    substance — meaningful withdrawal period required before competition.
  - Quesenberry & Carpenter, Ferrets, Rabbits and Rodents 4th ed — ferret
    Helicobacter mustelae triple therapy: amoxicillin + metronidazole +
    bismuth subsalicylate 17.5 mg/kg PO q8h × 14 days.
  - Marini RP et al. Am J Vet Res 1999 — eradication of H. mustelae in
    ferrets with triple therapy including bismuth subsalicylate.
  - Plumb's Veterinary Drug Handbook 10th ed — bismuth subsalicylate: avoid
    or use single-dose only in cats (salicylate; slow glucuronidation);
    darkens stools (may mimic melena) and is radiopaque.
  - Josseck H et al. Equine Vet J 1995;27:175 — biotin 20 mg/day PO improved
    hoof horn quality in Lipizzaners over 9-19 months.
  - Zenker W et al. Equine Vet J 1995;27:183 — histological/physical hoof
    horn improvement under long-term biotin supplementation.
  - Mader's Reptile and Amphibian Medicine 3rd ed — biotin deficiency in
    egg-eating reptiles (avidin in raw egg white); dietary correction and
    multivitamin supplementation.
"""

DRUGS_BATCH_48: list[dict] = [
    {
        "id": "isoxsuprine",
        "search_aliases": [
            "イソクスプリン",
            "Isoxsuprine",
            "イソキスプリン",
        ],
        "name": "Isoxsuprine",
        "name_ja": "イソクスプリン",
        "category": "cardiovascular",
        "mechanism": "Beta-adrenergic agonist with alpha-blocking activity producing peripheral vasodilation; historically used to improve digital blood flow in equine navicular syndrome and laminitis. Oral bioavailability in horses is poor and clinical efficacy is debated — an adjunct, never a substitute for corrective farriery and analgesia.",
        "mechanism_ja": "β作動性＋α遮断作用による末梢血管拡張薬。馬の蹄舟骨症候群・蹄葉炎で趾血流改善を目的に古くから使用される。馬での経口バイオアベイラビリティは低く臨床効果には議論がある — 装蹄矯正と鎮痛の代替ではなく補助と位置づける。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Navicular syndrome (adjunct): 0.6-1.2 mg/kg PO q12h (Rose 1983 EVJ). Reassess lameness after 3-6 weeks; discontinue if no response. Evidence is limited (poor oral bioavailability — Erkert 2002); corrective shoeing and NSAIDs remain first line.",
                "dosage_ja": "蹄舟骨症候群（補助療法）: 0.6-1.2 mg/kg 経口 12時間毎（Rose 1983 EVJ）。3-6週間で跛行を再評価し、無反応なら中止。エビデンスは限定的（経口吸収不良 — Erkert 2002）。装蹄矯正とNSAIDsが第一選択であることに変わりはない。",
                "notes": "FEI/racing prohibited substance — meaningful withdrawal before competition. Adverse effects uncommon at oral doses; IV use causes hypotension/tachycardia and is not recommended.",
                "notes_ja": "FEI・競馬の禁止薬物 — 競技前に十分な休薬期間が必要。経口用量での副作用は稀。静注は低血圧・頻脈を起こすため推奨されない。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not used in routine small-animal practice — no established indication or dose.",
                "dosage_ja": "小動物臨床では通常使用されない — 確立された適応・用量なし。",
                "notes": "Historic human peripheral vasodilator; veterinary use is essentially confined to equine podiatry.",
                "notes_ja": "ヒトの末梢血管拡張薬に由来し、獣医領域での使用は実質的に馬の蹄疾患に限られる。",
            },
        },
        "drug_interactions": [
            {
                "drug": "Antihypertensives / vasodilators (acepromazine)",
                "drug_ja": "降圧薬・血管拡張薬（アセプロマジン等）",
                "severity": "moderate",
                "effect": "Additive hypotension when combined with other vasodilating agents.",
                "effect_ja": "他の血管拡張作用を持つ薬剤との併用で低血圧が相加的に増強する。",
            },
        ],
    },
    {
        "id": "bismuth_subsalicylate",
        "search_aliases": [
            "次サリチル酸ビスマス",
            "ビスマス次サリチル酸",
            "ビスマス次サリチル酸塩",
            "サリチル酸ビスマス",
            "ビスマス",
            "ペプトビスモル",
            "Bismuth subsalicylate",
            "Pepto-Bismol",
        ],
        "name": "Bismuth Subsalicylate (Pepto-Bismol)",
        "name_ja": "次サリチル酸ビスマス（ペプトビスモル）",
        "category": "gi_drugs",
        "mechanism": "Dissociates in the gut into bismuth (direct antibacterial action against Helicobacter, mucosal coating/protection) and salicylate (antisecretory, anti-inflammatory via prostaglandin inhibition). The classic third leg of Helicobacter mustelae triple therapy in ferrets and an adjunct antidiarrheal in dogs.",
        "mechanism_ja": "消化管内でビスマス（Helicobacterへの直接抗菌作用・粘膜保護）とサリチル酸（プロスタグランジン阻害による分泌抑制・抗炎症）に解離する。フェレットのHelicobacter mustelae三剤併用療法の古典的な第三の柱であり、犬では止瀉補助薬。",
        "species_info": {
            "ferret": {
                "safe": True,
                "dosage": "Helicobacter mustelae triple therapy: 17.5 mg/kg PO q8h × 14 days combined with amoxicillin (10-20 mg/kg PO q12h) and metronidazole (20 mg/kg PO q12h) (Quesenberry & Carpenter 4th ed; Marini 1999 AJVR).",
                "dosage_ja": "Helicobacter mustelae三剤併用療法: 17.5 mg/kg 経口 8時間毎 × 14日間 — アモキシシリン（10-20 mg/kg 経口 12時間毎）＋メトロニダゾール（20 mg/kg 経口 12時間毎）と併用（Quesenberry & Carpenter 4th ed; Marini 1999 AJVR）。",
                "notes": "Bitter taste — syringe-feed slowly or follow with a treat. Darkens stools (do not mistake for melena).",
                "notes_ja": "苦味が強い — ゆっくりシリンジ投与するか、投与後におやつを与える。糞便が黒色化する（メレナと誤認しないこと）。",
            },
            "dog": {
                "safe": True,
                "dosage": "Adjunct for acute nonspecific diarrhea/gastritis: 10-30 mg/kg (0.5-1 mL/kg of standard 17.5 mg/mL suspension) PO q8-12h for no more than 5 days (Plumb's 10th ed).",
                "dosage_ja": "急性非特異性下痢・胃炎の補助: 10-30 mg/kg（標準17.5 mg/mL懸濁液で0.5-1 mL/kg）経口 8-12時間毎、最長5日間（Plumb's 10th ed）。",
                "notes": "Contains salicylate — avoid with NSAIDs/corticosteroids or in GI bleeding. Blackens stools (mimics melena) and is radiopaque (visible on abdominal radiographs).",
                "notes_ja": "サリチル酸を含む — NSAIDs・ステロイド併用中や消化管出血例では回避。糞便黒色化（メレナと紛らわしい）とX線不透過性（腹部X線に写る）に注意。",
            },
            "cat": {
                "safe": False,
                "dosage": "Avoid — cats deficiently glucuronidate salicylates; repeated dosing risks salicylate toxicosis. If ever used, single low dose only under veterinary direction (Plumb's 10th ed).",
                "dosage_ja": "回避 — 猫はサリチル酸のグルクロン酸抱合能が低く、反復投与でサリチル酸中毒のリスク。使用する場合も獣医師管理下の単回低用量に限る（Plumb's 10th ed）。",
                "notes": "Same salicylate-accumulation mechanism as aspirin toxicity in cats. Safer alternatives (kaolin-pectin, probiotics, diet) exist for feline diarrhea.",
                "notes_ja": "猫のアスピリン中毒と同一のサリチル酸蓄積機序。猫の下痢にはより安全な代替（カオリン・ペクチン、プロバイオティクス、食事療法）がある。",
            },
        },
        "drug_interactions": [
            {
                "drug": "Aspirin / NSAIDs",
                "drug_ja": "アスピリン・NSAIDs",
                "severity": "moderate",
                "effect": "Additive salicylate load and GI mucosal injury risk; avoid concurrent use.",
                "effect_ja": "サリチル酸負荷と消化管粘膜傷害リスクが相加的に増加 — 併用を避ける。",
            },
            {
                "drug": "Tetracyclines / fluoroquinolones",
                "drug_ja": "テトラサイクリン系・フルオロキノロン系",
                "severity": "moderate",
                "effect": "Bismuth chelates and markedly reduces oral absorption of these antibiotics — separate administration by at least 2 hours.",
                "effect_ja": "ビスマスがキレート形成しこれら抗菌薬の経口吸収を著しく低下させる — 投与間隔を2時間以上空ける。",
            },
        ],
    },
    {
        "id": "biotin",
        "search_aliases": [
            "ビオチン",
            "バイオチン",
            "ビタミンB7",
            "ビタミンH",
            "Biotin",
        ],
        "name": "Biotin (Vitamin B7)",
        "name_ja": "ビオチン（ビタミンB7）",
        "category": "supplements",
        "mechanism": "Water-soluble B vitamin serving as a cofactor for carboxylases in fatty-acid synthesis and keratin formation. Long-term supplementation improves hoof horn quality in horses and supports coat/claw quality in small animals; corrects deficiency caused by raw egg-white avidin in egg-fed reptiles.",
        "mechanism_ja": "脂肪酸合成・ケラチン形成に関与するカルボキシラーゼの補酵素となる水溶性ビタミンB群。長期補給で馬の蹄角質の質を改善し、小動物の被毛・爪の質をサポートする。卵食性爬虫類では生卵白アビジンによる欠乏症を是正する。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Hoof horn quality (thin/crumbling walls, navicular adjunct): 15-25 mg/horse/day PO (Josseck 1995; Zenker 1995 Equine Vet J). Effect requires 6-9+ months of continuous supplementation — hoof wall grows down from the coronet.",
                "dosage_ja": "蹄角質の質改善（薄い・脆い蹄壁、蹄舟骨症候群の補助）: 15-25 mg/頭/日 経口（Josseck 1995; Zenker 1995 Equine Vet J）。蹄壁は蹄冠から伸びるため効果発現には6-9ヶ月以上の継続投与が必要。",
                "notes": "Water-soluble — excess is excreted; toxicity is not reported at supplemental doses.",
                "notes_ja": "水溶性のため過剰分は排泄され、補給量での毒性報告はない。",
            },
            "dog": {
                "safe": True,
                "dosage": "Coat/claw quality adjunct (hypothyroidism, follicular dysplasia, brittle claws): 2.5-5 mg/day PO with food; often combined with omega-3/6 fatty acids and zinc.",
                "dosage_ja": "被毛・爪の質改善の補助（甲状腺機能低下症、毛包形成異常、脆弱爪）: 2.5-5 mg/日 経口（食事と共に）。ω-3/6脂肪酸・亜鉛としばしば併用。",
                "notes": "Supplement — treats the coat consequence, not the underlying endocrine/dermatologic disease.",
                "notes_ja": "サプリメント — 被毛の結果を補助するのみで、基礎にある内分泌・皮膚疾患自体の治療にはならない。",
            },
            "reptile": {
                "safe": True,
                "dosage": "Biotin deficiency (egg-fed monitors/snakes): remove raw egg white from the diet (avidin binds biotin) and supplement with a reptile multivitamin containing biotin per label; feed whole prey instead (Mader 3rd ed).",
                "dosage_ja": "ビオチン欠乏症（生卵給餌のオオトカゲ・ヘビ）: 生卵白を食餌から除去し（アビジンがビオチンと結合）、ビオチン含有の爬虫類用総合ビタミン剤をラベル用量で補給。丸ごとの餌動物への切替が根本対策（Mader 3rd ed）。",
                "notes": "Cooked egg denatures avidin; whole-prey diets prevent recurrence.",
                "notes_ja": "加熱卵はアビジンが変性するため安全。丸ごとの餌動物への切替で再発を予防。",
            },
        },
        "drug_interactions": [],
    },
]
