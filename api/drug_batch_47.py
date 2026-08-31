"""Drug batch 47 – referenced-but-absent agents surfaced by the 2026-08 audit (16th sweep).

The dosage-context katakana token sweep (treatment texts citing an agent with an
explicit dose, cross-checked against find_drugs_in_text) found six agents that
VetDict's own disease content instructs clinicians to use — with doses — yet
were absent from the formulary:

  - ハロペリドール (haloperidol): 17 references — the classic pharmacologic
    option for refractory avian feather-destructive behavior / self-mutilation
    ("ハロペリドール0.1-0.2 mg/kg PO q12h短期使用").
  - アトバコン (atovaquone): 12 references — VetDict's own curated protocols for
    Babesia gibsoni (アトバコン+アジスロマイシン, Birkenheuer 2004) and
    Cytauxzoon felis (Cohn 2011) name it as first-line, yet it was absent.
  - プリマキン (primaquine): 20 references — avian malaria gametocyte/tissue
    phase clearance and the only established therapy for Babesia felis.
  - クロロキン (chloroquine): 20 references — avian malaria (Plasmodium)
    first-line erythrocytic-phase therapy, always paired with primaquine.
  - ナルトレキソン (naltrexone): 9 references — opioid antagonist for
    self-directed/compulsive behavior (canine acral lick, avian feather
    picking, equine self-mutilation).
  - ブチルスコポラミン (N-butylscopolammonium bromide, Buscopan): 10 references
    — the FDA-approved equine spasmolytic for spasmodic colic and esophageal
    obstruction; a first-reach drug in equine practice.

References:
  - Carpenter's Exotic Animal Formulary 6th ed — haloperidol 0.1-0.2 mg/kg PO
    q12-24h for psittacine feather-destructive behavior (cockatoos start low);
    naltrexone 1.5 mg/kg PO q12h for feather picking; avian malaria:
    chloroquine 25 mg/kg PO once then 15 mg/kg at 12/24/48h plus primaquine
    0.75-1 mg/kg PO q24h.
  - Iglauer F, Rasim R. J Small Anim Pract 1993 — haloperidol treatment of
    automutilation/feather plucking in psittacines.
  - Birkenheuer AJ et al. J Vet Intern Med 2004;18:494 — atovaquone
    13.3 mg/kg PO q8h with fatty food + azithromycin 10 mg/kg PO q24h ×10 days
    for Babesia gibsoni.
  - Cohn LA et al. J Vet Intern Med 2011;25:55 — atovaquone 15 mg/kg PO q8h +
    azithromycin 10 mg/kg PO q24h ×10 days for Cytauxzoon felis: 60% survival
    vs 26% with imidocarb.
  - Penzhorn BL et al. / Jacobson LS — Babesia felis: primaquine 0.5 mg/kg is
    the only consistently effective drug; the feline lethal dose (~1 mg/kg) is
    close to the therapeutic dose — the definitional safety fact for this
    agent in cats.
  - Grim KC et al. J Zoo Wildl Med 2004; Remple JD 2004 — chloroquine/
    primaquine protocols for avian malaria in penguins and raptors.
  - Dodman NH et al. JAVMA 1988; White SD. JAVMA 1990;196:1073 — naltrexone
    2.2 mg/kg PO for canine acral lick dermatitis; Dodman NH 1987 — opioid
    antagonists in equine self-mutilation/crib-biting.
  - Plumb's Veterinary Drug Handbook 10th ed; Reed & Bayly Equine Internal
    Medicine 4th ed — N-butylscopolammonium bromide 0.3 mg/kg slow IV for
    spasmodic colic / choke; transient tachycardia ~30 min masks the heart
    rate as a pain indicator — record HR before dosing.
"""

DRUGS_BATCH_47: list[dict] = [
    {
        "id": "haloperidol",
        "search_aliases": [
            "ハロペリドール",
            "セレネース",
            "Haloperidol",
            "Haldol",
        ],
        "name": "Haloperidol (Haldol)",
        "name_ja": "ハロペリドール（セレネース）",
        "category": "behavioral",
        "mechanism": "Butyrophenone antipsychotic — central dopamine D2 receptor antagonist. In birds it damps the compulsive/stereotypic drive underlying refractory feather-destructive behavior and self-mutilation when environmental/behavioral modification and first-line agents have failed.",
        "mechanism_ja": "ブチロフェノン系抗精神病薬 — 中枢ドーパミンD2受容体拮抗薬。鳥では環境・行動修正と第一選択薬が無効な難治性の羽毛破壊行動・自咬症の背景にある強迫・常同的衝動を抑制する。",
        "species_info": {
            "bird": {
                "safe": True,
                "dosage": "Refractory feather-destructive behavior / self-mutilation: 0.1-0.2 mg/kg PO q12-24h, start at the low end (Carpenter 6th ed; Iglauer & Rasim 1993). Cockatoos are sensitive — start 0.1 mg/kg q24h. Long-acting decanoate 1-2 mg/kg IM q2-3 weeks has been used when oral dosing is impractical.",
                "dosage_ja": "難治性の羽毛破壊行動・自咬症: 0.1-0.2 mg/kg 経口 12-24時間毎、低用量から開始（Carpenter 6th ed; Iglauer & Rasim 1993）。オウム類（特にバタン）は感受性が高く0.1 mg/kg 24時間毎から。経口投与が困難な場合はデカン酸エステル持効型 1-2 mg/kg 筋注 2-3週毎の使用報告あり。",
                "notes": "Short-term adjunct only — environmental enrichment, foraging opportunity and behavioral modification remain the foundation. Monitor for anorexia, sedation, agitation and extrapyramidal signs; discontinue if they appear.",
                "notes_ja": "短期の補助療法に限る — 環境エンリッチメント・採餌機会・行動修正が治療の基盤。食欲不振・鎮静・興奮・錐体外路症状をモニタリングし、出現時は中止。",
            },
            "parrot": {
                "safe": True,
                "dosage": "0.1-0.2 mg/kg PO q12-24h, start low (Carpenter 6th ed). Cockatoos: 0.1 mg/kg q24h initially.",
                "dosage_ja": "0.1-0.2 mg/kg 経口 12-24時間毎、低用量から開始（Carpenter 6th ed）。バタン類は0.1 mg/kg 24時間毎から。",
                "notes": "Reserve for cases refractory to behavioral therapy and first-line agents (SSRIs/TCAs).",
                "notes_ja": "行動療法と第一選択薬（SSRI/TCA）が無効な症例に限って使用。",
            },
            "parakeet": {
                "safe": True,
                "dosage": "0.1-0.2 mg/kg PO q12-24h, start low (Carpenter 6th ed).",
                "dosage_ja": "0.1-0.2 mg/kg 経口 12-24時間毎、低用量から開始（Carpenter 6th ed）。",
                "notes": "Small-bird dosing requires accurate weighing and compounded dilution.",
                "notes_ja": "小型鳥では正確な体重測定と調剤希釈が必須。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not recommended — modern behavioral pharmacotherapy (fluoxetine, clomipramine) is preferred for compulsive disorders.",
                "dosage_ja": "非推奨 — 犬の強迫性障害には現行の行動薬物療法（フルオキセチン・クロミプラミン）が優先される。",
                "notes": "Extrapyramidal effects and sedation without addressing the underlying behavior; no established indication in current canine behavioral medicine.",
                "notes_ja": "錐体外路症状・鎮静のみで根本の行動問題に作用しない。現行の犬行動学に確立された適応なし。",
            },
        },
        "side_effects": "Anorexia, sedation, paradoxical agitation, extrapyramidal signs (tremor, rigidity); hepatic metabolism — monitor liver values on prolonged use",
        "side_effects_ja": "食欲不振・鎮静・逆説的興奮・錐体外路症状（振戦・固縮）。肝代謝 — 長期使用時は肝酵素をモニタリング",
        "contraindications": "CNS depression, hepatic failure. Not a substitute for environmental/behavioral modification",
        "contraindications_ja": "CNS抑制状態・肝不全。環境・行動修正の代替にはならない",
        "drug_interactions": [
            {
                "drug": "CNS depressants (opioids, benzodiazepines)",
                "effect": "Additive sedation",
                "effect_ja": "鎮静作用の相加",
                "severity": "moderate",
            },
            {
                "drug": "Metoclopramide",
                "effect": "Both are dopamine antagonists — additive extrapyramidal risk",
                "effect_ja": "共にドーパミン拮抗薬 — 錐体外路症状リスクが相加",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "atovaquone",
        "search_aliases": [
            "アトバコン",
            "メプロン",
            "Atovaquone",
            "Mepron",
        ],
        "name": "Atovaquone (Mepron)",
        "name_ja": "アトバコン（メプロン）",
        "category": "antiparasitics",
        "mechanism": "Hydroxynaphthoquinone antiprotozoal — inhibits the parasite mitochondrial cytochrome bc1 complex, collapsing the membrane potential. Combined with azithromycin it is the evidence-based first-line therapy for small Babesia (B. gibsoni) in dogs and Cytauxzoon felis in cats — the piroplasms that respond poorly to imidocarb.",
        "mechanism_ja": "ヒドロキシナフトキノン系抗原虫薬 — 原虫ミトコンドリアのチトクロムbc1複合体を阻害し膜電位を消失させる。アジスロマイシンとの併用で、イミドカルブが効きにくい小型ピロプラズマ（犬のBabesia gibsoni、猫のCytauxzoon felis）に対するエビデンスに基づく第一選択。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Babesia gibsoni: 13.3 mg/kg PO q8h WITH a fatty meal ×10 days + azithromycin 10 mg/kg PO q24h (Birkenheuer 2004 JVIM). Fatty food increases absorption several-fold — administration on an empty stomach is a common cause of treatment failure.",
                "dosage_ja": "Babesia gibsoni: 13.3 mg/kg 経口 8時間毎を**脂肪を含む食事と共に** 10日間 + アジスロマイシン 10 mg/kg 経口 24時間毎（Birkenheuer 2004 JVIM）。脂肪食で吸収が数倍に増加 — 空腹時投与は治療失敗の代表的原因。",
                "notes": "M121I cytochrome b mutants confer atovaquone resistance — relapse after initial response warrants PCR re-testing and a switch (clindamycin combination protocols). Clearance (PCR-negative) rather than clinical cure is the treatment goal.",
                "notes_ja": "チトクロムb M121I変異株はアトバコン耐性 — 初期反応後の再燃はPCR再検査とプロトコル変更（クリンダマイシン併用等）を検討。治療目標は臨床的改善ではなくPCR陰性化。",
            },
            "cat": {
                "safe": True,
                "dosage": "Cytauxzoon felis: 15 mg/kg PO q8h ×10 days + azithromycin 10 mg/kg PO q24h (Cohn 2011 JVIM — 60% survival vs 26% with imidocarb) alongside intensive supportive care (fluids, heparin, oxygen, nutrition). Babesia felis-group infections: reported adjunct where primaquine is unavailable.",
                "dosage_ja": "サイトークスゾーン症: 15 mg/kg 経口 8時間毎 10日間 + アジスロマイシン 10 mg/kg 経口 24時間毎（Cohn 2011 JVIM — 生存率60% vs イミドカルブ26%）。集中支持療法（輸液・ヘパリン・酸素・栄養）と必ず併用。猫バベシアではプリマキン入手不能時の補助としての報告あり。",
                "notes": "Give with food. Minimal-restraint nursing is part of the protocol — stress precipitates decompensation in cytauxzoonosis.",
                "notes_ja": "食事と共に投与。サイトークスゾーン症ではストレスが急変を誘発するため最小限の保定・看護がプロトコルの一部。",
            },
        },
        "side_effects": "Generally well tolerated; GI signs (vomiting, diarrhea, inappetence) most common",
        "side_effects_ja": "概して忍容性良好。最多は消化器症状（嘔吐・下痢・食欲不振）",
        "contraindications": "Hypersensitivity. Absorption is unreliable in anorexic patients — address nutrition first or use assisted feeding",
        "contraindications_ja": "過敏症。食欲廃絶例では吸収が不安定 — 先に栄養補給・強制給餌を確立して投与",
        "drug_interactions": [
            {
                "drug": "Azithromycin",
                "effect": "Intended synergistic combination — the standard protocol for B. gibsoni and C. felis",
                "effect_ja": "意図的な相乗併用 — B. gibsoni・C. felis の標準プロトコル",
                "severity": "info",
            },
            {
                "drug": "Metoclopramide",
                "effect": "Reduces atovaquone plasma concentrations (human data) — prefer maropitant for antiemesis during therapy",
                "effect_ja": "アトバコン血中濃度を低下させる（ヒトデータ） — 治療中の制吐はマロピタントを優先",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "primaquine",
        "search_aliases": [
            "プリマキン",
            "Primaquine",
        ],
        "name": "Primaquine",
        "name_ja": "プリマキン",
        "category": "antiparasitics",
        "mechanism": "8-aminoquinoline antimalarial — the only class active against exoerythrocytic (tissue) stages and gametocytes of Plasmodium, and the only consistently effective drug for Babesia felis. Paired with chloroquine (which clears erythrocytic stages) in avian malaria to prevent relapse and block transmission.",
        "mechanism_ja": "8-アミノキノリン系抗マラリア薬 — Plasmodiumの赤外型（組織型）とガメトサイトに有効な唯一のクラスで、Babesia felisに安定して有効な唯一の薬剤。鳥マラリアでは赤内型を除去するクロロキンと組み合わせ、再燃防止と伝播遮断を担う。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Babesia felis: 0.5 mg/kg PO or IM once, repeat after 24h if parasitemia persists (Penzhorn/Jacobson). DO NOT exceed 0.5 mg/kg per dose — the feline lethal dose (~1 mg/kg) is only twice the therapeutic dose.",
                "dosage_ja": "猫バベシア（Babesia felis）: 0.5 mg/kg 経口または筋注 単回、原虫血症持続時は24時間後に再投与（Penzhorn/Jacobson）。**1回0.5 mg/kgを超えないこと** — 猫の致死量（約1 mg/kg）は治療量のわずか2倍。",
                "notes": "The narrowest therapeutic margin in the feline antiprotozoal formulary — double-check the calculation and use an accurate scale. Monitor for hemolysis and methemoglobinemia.",
                "notes_ja": "猫の抗原虫薬で最も治療域が狭い薬剤 — 用量計算のダブルチェックと正確な体重測定が必須。溶血・メトヘモグロビン血症をモニタリング。",
            },
            "bird": {
                "safe": True,
                "dosage": "Avian malaria (Plasmodium): 0.75-1 mg/kg PO q24h ×3-10 days, combined with chloroquine loading (Carpenter 6th ed; Grim 2004 penguins). Prophylaxis in high-risk aviary/penguin collections during vector season: 1 mg/kg PO q24h.",
                "dosage_ja": "鳥マラリア（Plasmodium）: 0.75-1 mg/kg 経口 24時間毎 3-10日間、クロロキン初期投与と併用（Carpenter 6th ed; Grim 2004 ペンギン）。媒介蚊シーズンの高リスク飼育群（ペンギン等）の予防: 1 mg/kg 経口 24時間毎。",
                "notes": "Always paired with chloroquine — primaquine alone does not clear the erythrocytic stage. Vector (mosquito) control is part of the protocol.",
                "notes_ja": "必ずクロロキンと併用 — プリマキン単独では赤内型を除去できない。媒介蚊対策もプロトコルの一部。",
            },
            "parakeet": {
                "safe": True,
                "dosage": "0.75-1 mg/kg PO q24h ×3-10 days with chloroquine (Carpenter 6th ed).",
                "dosage_ja": "0.75-1 mg/kg 経口 24時間毎 3-10日間、クロロキンと併用（Carpenter 6th ed）。",
                "notes": "Accurate microdosing required in small psittacines.",
                "notes_ja": "小型インコでは正確な微量投与が必須。",
            },
            "parrot": {
                "safe": True,
                "dosage": "0.75-1 mg/kg PO q24h ×3-10 days with chloroquine (Carpenter 6th ed).",
                "dosage_ja": "0.75-1 mg/kg 経口 24時間毎 3-10日間、クロロキンと併用（Carpenter 6th ed）。",
                "notes": "Haemoproteus is often an incidental finding — reserve therapy for genuine Plasmodium disease.",
                "notes_ja": "Haemoproteusは偶発所見のことが多い — 治療は真のPlasmodium感染症に限る。",
            },
        },
        "side_effects": "Dose-dependent oxidative hemolysis and methemoglobinemia (8-aminoquinoline class effect); GI upset",
        "side_effects_ja": "用量依存性の酸化的溶血・メトヘモグロビン血症（8-アミノキノリン系のクラス作用）、消化器症状",
        "contraindications": "Cats: never exceed 0.5 mg/kg per dose — lethal at ~1 mg/kg. Severe anemia (correct first / transfuse). Not for Haemoproteus incidental parasitemia",
        "contraindications_ja": "猫: 1回0.5 mg/kg厳守 — 約1 mg/kgで致死的。重度貧血（先に輸血・補正）。Haemoproteusの偶発的寄生血症は治療対象外",
        "drug_interactions": [
            {
                "drug": "Chloroquine",
                "effect": "Intended combination for avian malaria (erythrocytic + tissue phase coverage)",
                "effect_ja": "鳥マラリアでの意図的併用（赤内型＋組織型を同時カバー）",
                "severity": "info",
            },
            {
                "drug": "Oxidant drugs (sulfonamides, benzocaine)",
                "effect": "Additive oxidative RBC injury — heightened hemolysis/methemoglobinemia risk",
                "effect_ja": "酸化的赤血球傷害が相加 — 溶血・メトヘモグロビン血症リスク増大",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "chloroquine",
        "search_aliases": [
            "クロロキン",
            "Chloroquine",
        ],
        "name": "Chloroquine",
        "name_ja": "クロロキン",
        "category": "antiparasitics",
        "mechanism": "4-aminoquinoline antimalarial — concentrates in the parasite food vacuole and blocks heme detoxification, killing erythrocytic-stage Plasmodium. The first-line erythrocytic-phase drug for avian malaria, always combined with primaquine for tissue-stage/gametocyte clearance.",
        "mechanism_ja": "4-アミノキノリン系抗マラリア薬 — 原虫の食胞に濃縮しヘム無毒化を阻害して赤内型Plasmodiumを殺滅。鳥マラリアの赤内型に対する第一選択で、組織型・ガメトサイト除去のため必ずプリマキンと併用する。",
        "species_info": {
            "bird": {
                "safe": True,
                "dosage": "Avian malaria (Plasmodium): 25 mg/kg PO initial dose, then 15 mg/kg at 12, 24 and 48h, combined with primaquine 0.75-1 mg/kg PO q24h (Carpenter 6th ed; Remple 2004 raptors; Grim 2004 penguins).",
                "dosage_ja": "鳥マラリア（Plasmodium）: 初回 25 mg/kg 経口、以後 15 mg/kg を12・24・48時間後に投与。プリマキン 0.75-1 mg/kg 経口 24時間毎と併用（Carpenter 6th ed; Remple 2004 猛禽; Grim 2004 ペンギン）。",
                "notes": "Institute during acute hemolytic crisis with supportive care (fluids, oxygen); severe anemia may need transfusion. Screen collections and control mosquitoes in endemic seasons.",
                "notes_ja": "急性溶血クリーゼでは支持療法（輸液・酸素）と共に開始。重度貧血は輸血を考慮。流行期は飼育群スクリーニングと蚊対策を併施。",
            },
            "parakeet": {
                "safe": True,
                "dosage": "25 mg/kg PO once, then 15 mg/kg at 12/24/48h + primaquine (Carpenter 6th ed).",
                "dosage_ja": "初回 25 mg/kg 経口、以後 15 mg/kg を12/24/48時間後 + プリマキン併用（Carpenter 6th ed）。",
                "notes": "Accurate microdosing in small birds.",
                "notes_ja": "小型鳥では正確な微量投与が必須。",
            },
            "parrot": {
                "safe": True,
                "dosage": "25 mg/kg PO once, then 15 mg/kg at 12/24/48h + primaquine (Carpenter 6th ed).",
                "dosage_ja": "初回 25 mg/kg 経口、以後 15 mg/kg を12/24/48時間後 + プリマキン併用（Carpenter 6th ed）。",
                "notes": "Confirm Plasmodium (blood smear/PCR) before committing to the full course.",
                "notes_ja": "全コース開始前に血液塗抹/PCRでPlasmodiumを確認。",
            },
        },
        "side_effects": "Retinal toxicity with chronic use (class effect); GI upset; overdose causes cardiotoxicity",
        "side_effects_ja": "長期使用で網膜毒性（クラス作用）、消化器症状。過量で心毒性",
        "contraindications": "Pre-existing retinal disease for prolonged courses; severe hepatic impairment",
        "contraindications_ja": "長期投与では既存網膜疾患に注意。重度肝障害",
        "drug_interactions": [
            {
                "drug": "Primaquine",
                "effect": "Intended combination for avian malaria",
                "effect_ja": "鳥マラリアでの意図的併用",
                "severity": "info",
            },
        ],
    },
    {
        "id": "naltrexone",
        "search_aliases": [
            "ナルトレキソン",
            "Naltrexone",
        ],
        "name": "Naltrexone",
        "name_ja": "ナルトレキソン",
        "category": "behavioral",
        "mechanism": "Long-acting oral opioid receptor antagonist. Self-directed behaviors (acral licking, feather picking, flank biting) can be maintained by endogenous opioid release — blocking the reward loop reduces the behavior in a subset of patients.",
        "mechanism_ja": "長時間作用型の経口オピオイド受容体拮抗薬。自己指向性行動（肢端舐性、毛引き、脇腹咬み）は内因性オピオイド放出により強化されることがあり、その報酬ループを遮断して一部の症例で行動を減少させる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Acral lick dermatitis / self-mutilation adjunct: 1-2.2 mg/kg PO q12-24h (White 1990 JAVMA; Dodman 1988). Trial 4-6 weeks; continue only in responders.",
                "dosage_ja": "肢端舐性皮膚炎・自傷行動の補助: 1-2.2 mg/kg 経口 12-24時間毎（White 1990 JAVMA; Dodman 1988）。4-6週間試験投与し、反応例のみ継続。",
                "notes": "Adjunct to behavioral modification and treatment of underlying pruritus/pain — not a standalone therapy. SSRIs/TCAs are the usual first-line pharmacotherapy.",
                "notes_ja": "行動修正と基礎の掻痒・疼痛治療への補助であり単独療法ではない。薬物療法の第一選択は通常SSRI/TCA。",
            },
            "bird": {
                "safe": True,
                "dosage": "Feather-destructive behavior: 1.5 mg/kg PO q12h (Carpenter 6th ed; Turner 1993).",
                "dosage_ja": "羽毛破壊行動: 1.5 mg/kg 経口 12時間毎（Carpenter 6th ed; Turner 1993）。",
                "notes": "Response is individual — reassess at 4 weeks alongside enrichment and medical workup for pruritic causes.",
                "notes_ja": "反応は個体差が大きい — エンリッチメントと掻痒原因の医学的精査を併行し4週で再評価。",
            },
            "parrot": {
                "safe": True,
                "dosage": "1.5 mg/kg PO q12h (Carpenter 6th ed).",
                "dosage_ja": "1.5 mg/kg 経口 12時間毎（Carpenter 6th ed）。",
                "notes": "Rule out medical causes of plucking (PBFD, giardiasis, dermatitis) first.",
                "notes_ja": "先に毛引きの医学的原因（PBFD・ジアルジア・皮膚炎）を除外。",
            },
            "horse": {
                "safe": True,
                "dosage": "Self-mutilation / flank-biting adjunct: 0.4-1 mg/kg PO q24h reported (Dodman 1987 — opioid antagonism reduced stereotypic behavior).",
                "dosage_ja": "自傷・脇腹咬み行動の補助: 0.4-1 mg/kg 経口 24時間毎の報告（Dodman 1987 — オピオイド拮抗で常同行動が減少）。",
                "notes": "Address management factors (turnout, social contact, ulcer pain) first; pharmacotherapy is adjunctive.",
                "notes_ja": "先に管理要因（放牧・社会的接触・胃潰瘍性疼痛）を是正。薬物療法は補助。",
            },
        },
        "side_effects": "GI upset; lethargy at high doses; hepatic metabolism — monitor liver values on prolonged use",
        "side_effects_ja": "消化器症状、高用量で元気消失。肝代謝 — 長期使用時は肝酵素をモニタリング",
        "contraindications": "Blocks opioid analgesics — discontinue before procedures requiring opioid analgesia; acute hepatitis/liver failure",
        "contraindications_ja": "オピオイド鎮痛薬を無効化する — オピオイド鎮痛が必要な処置の前に休薬。急性肝炎・肝不全",
        "drug_interactions": [
            {
                "drug": "Opioid analgesics (morphine, buprenorphine, tramadol)",
                "effect": "Antagonizes analgesia — opioids will not work while naltrexone is on board; plan perioperative analgesia with non-opioid agents or wash out first",
                "effect_ja": "鎮痛作用を拮抗 — 本剤投与中はオピオイドが効かない。周術期は非オピオイド鎮痛で計画するか先に休薬",
                "severity": "major",
            },
        ],
    },
    {
        "id": "butylscopolamine",
        "search_aliases": [
            "ブチルスコポラミン",
            "ブスコパン",
            "臭化ブチルスコポラミン",
            "N-ブチルスコポラミン",
            "Butylscopolamine",
            "Buscopan",
            "N-butylscopolammonium",
        ],
        "name": "N-Butylscopolammonium Bromide (Buscopan)",
        "name_ja": "ブチルスコポラミン臭化物（ブスコパン）",
        "category": "gastrointestinal",
        "mechanism": "Quaternary ammonium anticholinergic (antimuscarinic) spasmolytic — relaxes gastrointestinal smooth muscle without crossing the blood-brain barrier. The FDA-approved equine spasmolytic: rapidly relieves spasmodic colic pain and relaxes the esophagus in choke, and facilitates rectal palpation.",
        "mechanism_ja": "第四級アンモニウム型の抗コリン（抗ムスカリン）鎮痙薬 — 血液脳関門を通過せずに消化管平滑筋を弛緩させる。馬でFDA承認された鎮痙薬: 痙攣性疝痛の疼痛を速やかに緩和し、食道梗塞（チョーク）では食道を弛緩、直腸検査の弛緩にも用いる。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Spasmodic colic / esophageal obstruction (choke) / rectal relaxation: 0.3 mg/kg slow IV once (Plumb's 10th ed; Reed & Bayly 4th ed). Effect within minutes; duration ~20-30 min.",
                "dosage_ja": "痙攣性疝痛・食道梗塞（チョーク）・直腸弛緩: 0.3 mg/kg 緩徐静注 単回（Plumb's 10th ed; Reed & Bayly 4th ed）。数分で効果発現、持続約20-30分。",
                "notes": "Causes transient tachycardia (~30 min) — RECORD THE HEART RATE BEFORE DOSING, because HR is the key colic-severity indicator and is uninterpretable afterward. Pain returning after the spasmolytic wears off suggests a surgical lesion — re-evaluate rather than re-dose repeatedly.",
                "notes_ja": "一過性頻脈（約30分）を起こす — **投与前に必ず心拍数を記録**（心拍数は疝痛重症度の主要指標であり投与後は評価不能になる）。効果消失後の疼痛再燃は外科的病変を示唆 — 反復投与でごまかさず再評価する。",
            },
            "dog": {
                "safe": True,
                "dosage": "GI/urinary tract spasm adjunct: 0.2-0.3 mg/kg IV/IM/SC q8-12h (Plumb's). In Japan often as combination products with metamizole (Buscopan compositum).",
                "dosage_ja": "消化管・尿路の痙攣性疼痛の補助: 0.2-0.3 mg/kg 静注/筋注/皮下 8-12時間毎（Plumb's）。日本ではメタミゾール配合剤（ブスコパン・コンポジタム等）としての使用も多い。",
                "notes": "Symptomatic adjunct — identify and treat the underlying cause.",
                "notes_ja": "対症的補助 — 基礎原因の診断・治療を並行する。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.2-0.3 mg/kg IV/IM/SC q8-12h (extrapolated; limited feline data).",
                "dosage_ja": "0.2-0.3 mg/kg 静注/筋注/皮下 8-12時間毎（外挿、猫のデータは限定的）。",
                "notes": "Use anticholinergics cautiously in cats with cardiac disease (tachycardia).",
                "notes_ja": "心疾患のある猫では抗コリン薬による頻脈に注意。",
            },
        },
        "side_effects": "Transient tachycardia, decreased GI motility/borborygmi, mydriasis (minimal CNS effect — quaternary structure)",
        "side_effects_ja": "一過性頻脈、消化管運動性・腸音の低下、散瞳（第四級構造のためCNS作用は最小）",
        "contraindications": "Ileus and impaction/obstruction (further reduces motility); glaucoma; tachyarrhythmia. Masks heart rate as a pain indicator in colic — record HR first",
        "contraindications_ja": "イレウス・便秘疝/閉塞（運動性をさらに低下させる）、緑内障、頻脈性不整脈。疝痛では心拍数指標をマスクする — 投与前の心拍数記録が必須",
        "drug_interactions": [
            {
                "drug": "Metoclopramide / cisapride / prokinetics",
                "effect": "Directly opposing pharmacology — anticholinergic spasmolysis antagonizes prokinetic effect",
                "effect_ja": "薬理作用が真逆 — 抗コリン性鎮痙は消化管運動促進薬の効果を拮抗する",
                "severity": "moderate",
            },
            {
                "drug": "Other anticholinergics (atropine, glycopyrrolate)",
                "effect": "Additive tachycardia and ileus risk",
                "effect_ja": "頻脈・イレウスリスクが相加",
                "severity": "moderate",
            },
        ],
    },
]
