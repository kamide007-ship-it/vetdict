"""Drug batch 75 – 2026-10 session (第67弾): three licensed veterinary
products absent from the dictionary although the toxicology / parasite /
osteoarthritis content they belong to was present.

1. Ropinirole ophthalmic solution (CLEVOR, Orion/Vetoquinol) — topical
   dopamine D2 agonist for induction of emesis in dogs. EU authorisation
   2018, FDA approval 2020 (NADA 141-534). Target dose 3.75 mg/m² BSA given
   as a weight-banded number of drops into the eye(s); a second dose may be
   given if the dog has not vomited within 15 minutes. Randomised,
   placebo-controlled trial: 95% of dogs vomited within 30 min (Suokko et
   al. Vet Rec 2020). The ocular route avoids the IV catheter that
   apomorphine needs. Emesis is not reliably induced in cats by dopamine
   agonists (alpha-2 agonists are used in cats).
2. Sarolaner + moxidectin + pyrantel (SIMPARICA TRIO, Zoetis) — monthly
   oral chewable: flea/tick (isoxazoline), heartworm prevention (macrocyclic
   lactone) and roundworm/hookworm treatment. Minimum label dose sarolaner
   1.2 mg/kg + moxidectin 24 µg/kg + pyrantel 5 mg/kg; dogs >= 8 weeks and
   >= 1.25 kg (FDA NADA 141-521, 2020; EU 2019). Marketed in Japan.
3. Enflicoxib (DAXOCOX, Ecuphar/Animalcare) — COX-2 preferential coxib
   given ONCE WEEKLY for canine osteoarthritis pain because of the long
   half-life of its active pyrazoline metabolite. EU authorisation 2021.
   Loading dose 8 mg/kg PO with food, then 4 mg/kg once weekly; randomised
   non-inferiority trial versus mavacoxib (Salichs et al. PLoS One 2022).
   Not approved in Japan or the US.
"""

DRUGS_BATCH_75 = [
    {
        "id": "ropinirole_ophthalmic",
        "search_aliases": ["クレボー", "クレヴォー", "Clevor", "CLEVOR", "ロピニロール点眼", "ロピニロール"],
        "name": "Ropinirole Ophthalmic Solution (Clevor)",
        "name_ja": "ロピニロール点眼液（クレボー）",
        "category": "miscellaneous",
        "mechanism": "Dopamine D2-receptor agonist absorbed through the conjunctiva and nasolacrimal mucosa that stimulates the chemoreceptor trigger zone — induces emesis in dogs without intravenous access.",
        "mechanism_ja": "結膜・鼻涙管粘膜から吸収されるドパミンD2受容体作動薬で、化学受容器引金帯（CTZ）を刺激して催吐する。静脈確保不要で犬の催吐が可能。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Target 3.75 mg/m² body surface area (label range 2.7-5.4 mg/m²) given as the weight-banded number of drops (30 mg/mL solution) from the label table into one or both eyes. If the dog has not vomited within 15 minutes, the same dose may be repeated once. Emesis typically occurs within 10-15 minutes (CLEVOR label, FDA 2020; Suokko 2020 Vet Rec: 95% vomited within 30 min).",
                "dosage_ja": "目標 3.75 mg/m²（体表面積、ラベル範囲 2.7-5.4 mg/m²）を、ラベルの体重帯表に従った滴数（30 mg/mL製剤）として片眼または両眼に点眼。15分以内に嘔吐しない場合は同量を1回だけ再投与できる。通常10-15分で嘔吐（CLEVOR ラベル、FDA 2020年；Suokko 2020 Vet Rec: 95%が30分以内に嘔吐）。",
                "notes": "Decide that emesis is indicated before dosing: most useful within 1-2 h of ingesting a toxin such as chocolate, grapes/raisins, xylitol or NSAIDs. Wear gloves; avoid human skin/eye contact. Transient conjunctival hyperaemia, protruding third eyelid, lacrimation and tachycardia are common. Protracted vomiting or marked tachycardia can be reversed with the D2 antagonist metoclopramide (0.5 mg/kg IV/IM/SC per label). Maropitant given BEFORE ropinirole blocks emesis — give it afterwards to stop vomiting. Not approved in Japan (apomorphine remains the domestic standard).",
                "notes_ja": "投与前に催吐の適応を判断する: チョコレート・ブドウ/レーズン・キシリトール・NSAIDs 等の摂取後1-2時間以内が最も有用。手袋を着用し、人の皮膚・眼への接触を避ける。一過性の結膜充血・瞬膜突出・流涙・頻脈が多い。遷延性嘔吐や著明な頻脈はD2拮抗薬メトクロプラミド（ラベル 0.5 mg/kg IV/IM/SC）で拮抗できる。マロピタントを先に投与すると催吐が阻害される — 嘔吐を止める目的で催吐後に投与する。国内未承認（国内ではアポモルヒネが標準）。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not used — dopamine agonists do not reliably induce emesis in cats (feline emesis is induced with an alpha-2 agonist such as dexmedetomidine).",
                "dosage_ja": "使用しない — 猫ではドパミン作動薬で確実な催吐が得られない（猫の催吐はデクスメデトミジン等のα2作動薬で行う）。",
                "notes": "Cats: use an alpha-2 agonist protocol for emesis induction and reverse with atipamezole.",
                "notes_ja": "猫の催吐はα2作動薬プロトコルで行い、アチパメゾールで拮抗する。",
            },
        },
        "contraindications": "Emesis contraindicated: CNS depression, seizures or reduced gag reflex (aspiration risk); ingestion of corrosives, hydrocarbons/petroleum products or sharp objects; dyspnoea/hypoxia; recent abdominal surgery; brachycephalic dogs with upper-airway compromise (use caution). Corneal injury or ocular disease in the eye to be dosed. Hypersensitivity to ropinirole.",
        "contraindications_ja": "催吐禁忌の状態: 意識低下・痙攣・咽頭反射低下（誤嚥リスク）、腐食性物質・炭化水素/石油製品・鋭利な異物の摂取、呼吸困難/低酸素、最近の腹部手術、上気道障害のある短頭種（慎重に）。点眼する眼の角膜損傷・眼疾患。ロピニロール過敏症。",
        "side_effects": [
            "Transient conjunctival hyperaemia, third-eyelid protrusion, lacrimation, blepharospasm",
            "Tachycardia, lethargy",
            "Protracted vomiting (reverse with metoclopramide)",
        ],
        "side_effects_ja": [
            "一過性の結膜充血・瞬膜突出・流涙・眼瞼痙攣",
            "頻脈・元気消失",
            "遷延性嘔吐（メトクロプラミドで拮抗）",
        ],
        "drug_interactions": [
            {
                "drug": "Metoclopramide / other dopamine antagonists (acepromazine)",
                "effect": "Antagonise the D2-mediated emetic effect — given beforehand they prevent emesis; metoclopramide is used afterwards to reverse protracted vomiting.",
                "effect_ja": "D2を介した催吐作用に拮抗する — 事前投与で催吐を妨げる。遷延性嘔吐の拮抗にはメトクロプラミドを事後投与する。",
                "severity": "moderate",
            },
            {
                "drug": "Maropitant / other antiemetics",
                "effect": "Prior administration blocks the induced emesis.",
                "effect_ja": "事前投与で催吐が得られなくなる。",
                "severity": "moderate",
            },
        ],
        "references": [
            "CLEVOR (ropinirole ophthalmic solution) US label — FDA NADA 141-534 (2020); EMA EPAR Clevor (2018)",
            "Suokko M et al. Ropinirole eye drops induce vomiting effectively in dogs: a randomised, double-blind, placebo-controlled clinical study. Vet Rec 2020;186:283.",
        ],
    },
    {
        "id": "sarolaner_moxidectin_pyrantel",
        "search_aliases": ["シンパリカトリオ", "シンパリカ トリオ", "Simparica Trio", "SIMPARICA TRIO"],
        "name": "Sarolaner + Moxidectin + Pyrantel (Simparica Trio)",
        "name_ja": "サロラネル＋モキシデクチン＋ピランテル（シンパリカトリオ）",
        "category": "antiparasitics",
        "mechanism": "Sarolaner (isoxazoline: GABA-/glutamate-gated chloride channel blocker in arthropods) + moxidectin (macrocyclic lactone: kills D. immitis L3/L4 larvae) + pyrantel pamoate (nicotinic agonist: spastic paralysis of roundworms/hookworms) in one monthly chewable.",
        "mechanism_ja": "サロラネル（イソキサゾリン系: 節足動物のGABA/グルタミン酸作動性Clチャネル遮断）＋モキシデクチン（大環状ラクトン: 犬糸状虫L3/L4幼虫を殺滅）＋パモ酸ピランテル（ニコチン受容体作動: 回虫・鉤虫の痙性麻痺）を配合した月1回のチュアブル錠。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Minimum 1.2 mg/kg sarolaner + 24 µg/kg moxidectin + 5 mg/kg pyrantel (as pamoate) PO once monthly, given as the weight-banded chewable (label range 1.2-2.4 mg/kg sarolaner). Dogs >= 8 weeks of age and >= 1.25 kg. Give year-round (or from 1 month before to 1 month after the mosquito season) for heartworm prevention (Simparica Trio label, FDA 2020).",
                "dosage_ja": "最低用量 サロラネル 1.2 mg/kg＋モキシデクチン 24 µg/kg＋ピランテル（パモ酸塩として）5 mg/kg を月1回経口、体重帯別のチュアブル錠で投与（ラベル範囲 サロラネル 1.2-2.4 mg/kg）。8週齢以上・1.25 kg以上。フィラリア予防は通年（または蚊の発生1ヶ月前から終息1ヶ月後まで）（シンパリカトリオ ラベル、FDA 2020年）。",
                "notes": "Confirm a negative heartworm antigen test before starting (macrocyclic lactone in an infected dog can cause a reaction to dying microfilariae and does not treat adult worms). Isoxazoline class warning: neurologic adverse reactions (tremor, ataxia, seizures) have been reported — use with caution in dogs with a history of seizures. Moxidectin at this dose is safe in MDR1 (ABCB1) mutant dogs. Does not cover tapeworms (add praziquantel/epsiprantel when indicated). Marketed in Japan.",
                "notes_ja": "開始前にフィラリア抗原検査陰性を確認する（感染犬への大環状ラクトン投与はミクロフィラリア死滅反応のリスクがあり、成虫は駆除しない）。イソキサゾリン系のクラス警告: 神経系副作用（振戦・運動失調・痙攣）の報告あり — 痙攣の既往がある犬では慎重に。本用量のモキシデクチンはMDR1（ABCB1）変異犬でも安全。条虫には無効（必要時プラジカンテル/エプシプランテルを追加）。国内でも販売されている。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not for cats — use a feline-labelled product (e.g. selamectin + sarolaner topical).",
                "dosage_ja": "猫には使用しない — 猫用製剤（セラメクチン＋サロラネル外用等）を用いる。",
                "notes": "Canine-only chewable.",
                "notes_ja": "犬専用チュアブル錠。",
            },
        },
        "contraindications": "Dogs < 8 weeks or < 1.25 kg. Heartworm-positive dogs (test first). Use with caution in dogs with a history of seizures or neurologic disorders (isoxazoline class).",
        "contraindications_ja": "8週齢未満・1.25 kg未満。フィラリア陽性犬（事前検査必須）。痙攣・神経疾患の既往がある犬では慎重に（イソキサゾリン系）。",
        "side_effects": [
            "Vomiting, diarrhoea, lethargy, anorexia (uncommon)",
            "Neurologic signs: tremor, ataxia, seizures (isoxazoline class, rare)",
        ],
        "side_effects_ja": [
            "嘔吐・下痢・元気消失・食欲不振（まれ）",
            "神経症状: 振戦・運動失調・痙攣（イソキサゾリン系、まれ）",
        ],
        "drug_interactions": [
            {
                "drug": "Other isoxazolines (fluralaner, afoxolaner, lotilaner)",
                "effect": "Duplicate class exposure with no added benefit — do not combine.",
                "effect_ja": "同系統の重複曝露で上乗せ効果なし — 併用しない。",
                "severity": "moderate",
            },
            {
                "drug": "Other macrocyclic lactones (ivermectin, milbemycin, selamectin)",
                "effect": "Duplicate heartworm preventive exposure; additive neurotoxicity risk at high doses (MDR1 dogs).",
                "effect_ja": "フィラリア予防薬の重複。高用量ではMDR1変異犬で神経毒性が相加しうる。",
                "severity": "moderate",
            },
        ],
        "references": [
            "SIMPARICA TRIO (sarolaner, moxidectin, pyrantel chewable tablets) US label, Zoetis — FDA NADA 141-521 (2020); EMA EPAR (2019)",
            "Becskei C et al. Efficacy of a novel oral chewable tablet containing sarolaner, moxidectin and pyrantel (Simparica Trio) against induced hookworm, roundworm and heartworm infections in dogs. Parasit Vectors 2020;13:70.",
        ],
    },
    {
        "id": "enflicoxib",
        "search_aliases": ["ダクソコックス", "Daxocox", "DAXOCOX", "エンフリコキシブ"],
        "name": "Enflicoxib (Daxocox)",
        "name_ja": "エンフリコキシブ（ダクソコックス）",
        "category": "nsaids",
        "mechanism": "COX-2-preferential coxib NSAID. Its active pyrazoline metabolite has a very long elimination half-life, allowing ONCE-WEEKLY oral dosing for chronic osteoarthritis pain.",
        "mechanism_ja": "COX-2選択的（コキシブ系）NSAID。活性代謝物（ピラゾリン体）の消失半減期が非常に長く、慢性変形性関節症の疼痛に週1回の経口投与が可能。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Loading dose 8 mg/kg PO with food on day 0, then 4 mg/kg PO with food once WEEKLY (EU SPC, 2021). Give with a meal — fasting reduces absorption. Reassess pain control and renal/hepatic parameters periodically during long-term use.",
                "dosage_ja": "初回 8 mg/kg を食事と共に経口投与し、以降 4 mg/kg を食事と共に週1回経口投与（EU製品概要、2021年）。空腹時は吸収が低下するため必ず食事と共に。長期使用中は疼痛管理効果と腎・肝パラメータを定期的に再評価する。",
                "notes": "Weekly dosing improves compliance but means an adverse effect cannot be stopped quickly — the drug persists for weeks after the last dose. Allow a washout (at least one week after the last weekly dose, longer if clinically indicated) before switching to another NSAID or a corticosteroid. Non-inferior to mavacoxib in a randomised multicentre OA trial (Salichs 2022 PLoS One). Not approved in Japan or the US.",
                "notes_ja": "週1回投与はコンプライアンスを高めるが、副作用発現時にすぐ中止できない（最終投与後も数週間体内に残る）。他のNSAIDs・ステロイドへの切替時は休薬期間を置く（最終週投与から最低1週間、臨床的に必要ならさらに長く）。多施設無作為化OA試験でマバコキシブに非劣性（Salichs 2022 PLoS One）。国内・米国未承認。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not used — no feline data; long-acting NSAID exposure is unsafe in cats.",
                "dosage_ja": "使用しない — 猫のデータなし。長時間作用型NSAIDの曝露は猫で安全でない。",
                "notes": "Cats: meloxicam/robenacoxib at feline doses or frunevetmab.",
                "notes_ja": "猫はメロキシカム/ロベナコキシブの猫用量、またはフルネベトマブを用いる。",
            },
        },
        "contraindications": "Gastrointestinal ulceration or bleeding, renal or hepatic impairment, bleeding disorders, dehydration/hypovolaemia/hypotension, pregnancy/lactation/breeding animals, dogs under 1 year, concurrent NSAIDs or corticosteroids.",
        "contraindications_ja": "消化管潰瘍・出血、腎・肝機能障害、出血性疾患、脱水・循環血液量減少・低血圧、妊娠・授乳・繁殖動物、1歳未満、他のNSAIDs・ステロイドとの併用。",
        "side_effects": [
            "Vomiting, diarrhoea, anorexia",
            "GI ulceration (NSAID class)",
            "Renal/hepatic adverse effects (NSAID class)",
        ],
        "side_effects_ja": ["嘔吐・下痢・食欲不振", "消化管潰瘍（NSAIDsクラス）", "腎・肝の有害事象（NSAIDsクラス）"],
        "drug_interactions": [
            {
                "drug": "Other NSAIDs / corticosteroids",
                "effect": "Additive GI ulceration and nephrotoxicity — contraindicated; the long half-life requires a washout before switching.",
                "effect_ja": "消化管潰瘍・腎毒性の相加 — 併用禁忌。長い半減期のため切替時は休薬期間が必要。",
                "severity": "major",
            },
            {
                "drug": "ACE inhibitors / diuretics",
                "effect": "Reduced renal perfusion — monitor renal values.",
                "effect_ja": "腎灌流低下 — 腎パラメータを監視。",
                "severity": "moderate",
            },
        ],
        "references": [
            "DAXOCOX (enflicoxib) EMA EPAR / Summary of Product Characteristics (2021)",
            "Salichs M et al. Enflicoxib for canine osteoarthritis: a randomized, blind, multicentre, non-inferiority clinical trial compared to mavacoxib. PLoS One 2022;17:e0274800.",
        ],
    },
]
