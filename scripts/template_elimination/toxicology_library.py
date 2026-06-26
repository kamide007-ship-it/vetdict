"""Curated, veterinary-accurate toxicology content (pathophysiology + etiology).

Background
----------
The disease database previously assigned **one generic paragraph per
*category*** to every clinical field.  For toxicoses this is not merely
cosmetic — it is clinically dangerous, because every poison received an
identical mechanism paragraph ("毒物は特異的標的に作用し…肝・腎は代謝・排泄の
主要臓器…") that is *wrong* for most agents:

* Chocolate (methylxanthine) acts on the heart/CNS, not via hepatorenal
  "toxic metabolites".
* Xylitol triggers insulin release → hypoglycaemia + hepatic necrosis (dogs).
* Grapes/raisins cause idiosyncratic proximal-tubular nephrosis.
* Ethylene glycol → oxalate-crystal nephropathy + severe acidosis.

Each toxic agent has a **distinct, textbook mechanism**.  This module curates
that mechanism per agent so the served database tells the truth.  The text is
established veterinary toxicology (Plumb's, the Merck/MSD Veterinary Manual,
Peterson & Talcott *Small Animal Toxicology* 3rd ed, ASPCA APCC), not
free-form generation, so it carries no fabrication risk.

Mechanism text is **species-independent** (the cellular target of theobromine
is the same in a dog and a parrot); species sensitivity differences are noted
inside the text where they matter clinically (e.g. cats and permethrin, the
MDR1/ABCB1 phenotype and ivermectin).  The caller supplies the localized
"<species>における<disease>の…" lead-in via the disease prefix.

Public API
----------
``resolve_toxic_agent(name_ja, name_en) -> str | None``
    Map a disease name to a canonical agent key, or ``None`` when the name is
    not a genuine, well-characterised toxicosis (so callers leave it alone
    rather than risk mis-applying a mechanism).

``AGENTS[key] -> {"patho_ja", "causes_ja", "patho_en", "causes_en"}``
    Curated body text for each canonical agent.
"""

from __future__ import annotations

from typing import Optional

# ---------------------------------------------------------------------------
# Canonical agent content
# ---------------------------------------------------------------------------
# Each value is the *body* of the field — a complete clinical statement that
# does not repeat the disease name.  Callers prepend the localized lead-in
# ("犬におけるチョコレート中毒の病態生理は、" / "In dogs, the pathophysiology of
# Chocolate Toxicosis involves ").

AGENTS: dict[str, dict[str, str]] = {
    # --- Food / household toxins -------------------------------------------
    "methylxanthine": {
        "patho_ja": (
            "カカオ・茶・コーヒーに含まれるメチルキサンチン（テオブロミン・カフェイン）による中毒である。"
            "メチルキサンチンはホスホジエステラーゼ阻害による細胞内 cAMP 上昇、アデノシン受容体の競合的拮抗、"
            "カテコールアミン遊離促進、細胞内カルシウム動員を介して、中枢神経興奮・心筋および骨格筋の興奮・平滑筋弛緩を引き起こす。"
            "テオブロミンは半減期が長く（犬で約17.5時間）腸肝循環するため作用が遷延・再燃しやすい。"
            "用量依存性に嘔吐・多飲多尿・落ち着きのなさ・頻脈性不整脈・高血圧・振戦・痙攣・高体温へ進行し、"
            "重症例では心室頻拍・心室細動・呼吸不全により死亡する。"
        ),
        "causes_ja": (
            "ダークチョコレート・ビターチョコレート・ココアパウダー・カカオマルチ（園芸用）など、"
            "テオブロミン濃度の高い製品の摂取が原因。ミルクチョコレートより製菓用・カカオ含量の高い製品ほど危険度が高い。"
            "カフェイン源（コーヒー豆・茶葉・エナジードリンク・カフェイン錠）でも同様の中毒を生じる。"
            "好奇心の強い若齢個体や大量摂取が可能な大型犬で発生が多い。"
        ),
        "patho_en": (
            "poisoning by methylxanthines (theobromine, caffeine) from cacao products. "
            "Methylxanthines inhibit phosphodiesterase (raising intracellular cAMP), competitively antagonise "
            "adenosine receptors, promote catecholamine release and mobilise intracellular calcium, producing CNS "
            "stimulation, cardiac and skeletal-muscle excitation and smooth-muscle relaxation. Theobromine has a long "
            "half-life (~17.5 h in dogs) and undergoes enterohepatic recirculation, so signs are prolonged and can "
            "relapse. Dose-dependent progression runs from vomiting, polydipsia and restlessness to tachyarrhythmia, "
            "tremor, seizures and hyperthermia, with death from ventricular tachycardia/fibrillation in severe cases."
        ),
        "causes_en": (
            "ingestion of theobromine-rich products — dark/baking chocolate, cocoa powder and cocoa-bean mulch — or "
            "caffeine sources (coffee, tea, energy drinks, caffeine tablets). Risk rises with cacao content; baking "
            "chocolate is far more dangerous than milk chocolate."
        ),
    },
    "xylitol": {
        "patho_ja": (
            "甘味料キシリトールによる中毒で、犬で特に重篤である。"
            "犬ではキシリトールが膵β細胞を強力に刺激してインスリンを過剰分泌させ、摂取後30〜60分で急性の低血糖を引き起こす。"
            "さらに高用量では用量依存性に肝細胞の ATP 枯渇・酸化的傷害を介した急性肝壊死を生じ、"
            "肝不全・凝固障害（DIC）に進展しうる。低血糖は虚脱・運動失調・痙攣を、肝傷害は黄疸・出血傾向をもたらす。"
            "なお猫におけるキシリトールのインスリン分泌刺激作用は犬ほど明確には確立されていない。"
        ),
        "causes_ja": (
            "キシリトール含有のシュガーレスガム・キャンディ・歯磨き剤・焼き菓子・一部の医薬品やサプリメント、"
            "ピーナッツバター製品の誤食が原因。少量（>0.1 g/kg で低血糖、>0.5 g/kg で肝傷害）でも中毒を起こすため、"
            "ガム数粒でも危険となりうる。"
        ),
        "patho_en": (
            "a poisoning that is especially severe in dogs, in which xylitol acts as a potent insulin secretagogue, "
            "causing acute hypoglycaemia 30–60 min after ingestion; higher doses cause dose-dependent acute hepatic "
            "necrosis through hepatocyte ATP depletion and oxidative injury, which can progress to liver failure and "
            "DIC. Hypoglycaemia produces collapse, ataxia and seizures; hepatic injury produces icterus and bleeding."
        ),
        "causes_en": (
            "ingestion of xylitol-sweetened sugar-free gum, candy, dental products, baked goods, some medications/"
            "supplements and certain peanut butters. Toxic at low doses (hypoglycaemia >0.1 g/kg, hepatotoxicity "
            ">0.5 g/kg), so even a few pieces of gum can be dangerous."
        ),
    },
    "grape_raisin": {
        "patho_ja": (
            "ブドウ・レーズン（および酒石酸を含む近縁果実）による特異体質性の急性腎傷害である。"
            "近年、原因毒性成分として酒石酸（tartaric acid）／酒石酸水素カリウムが有力視されており、近位尿細管上皮の壊死を引き起こす。"
            "感受性には個体差が大きく、摂取量と腎障害の相関は一定しない（少量でも発症例あり）。"
            "嘔吐・元気消失・乏尿/無尿性の急性腎不全に進行し、対応が遅れると不可逆性腎不全・死に至る。"
        ),
        "causes_ja": (
            "ブドウ・レーズン・カラント・サルタナ、およびそれらを含む食品（パン・菓子・グラノーラ等）の摂取が原因。"
            "品種・調理の有無を問わず中毒を起こしうる。個体感受性の差が大きいため、いかなる量も摂取量にかかわらず受診対象とする。"
        ),
        "patho_en": (
            "idiosyncratic acute kidney injury from grapes/raisins (and related tartaric-acid-containing fruit). "
            "Tartaric acid / potassium bitartrate is now the leading candidate toxic principle, causing proximal "
            "renal tubular necrosis. Susceptibility varies widely and dose correlates poorly with injury, so even "
            "small amounts may cause oligo-/anuric acute renal failure that can become irreversible."
        ),
        "causes_en": (
            "ingestion of grapes, raisins, currants or sultanas, or foods containing them. Any amount warrants "
            "evaluation because individual susceptibility is highly variable."
        ),
    },
    "allium": {
        "patho_ja": (
            "タマネギ・ニンニク・ニラ・ネギ（ネギ属）に含まれる有機チオ硫酸化合物（n-プロピルジスルフィド等）による酸化性溶血である。"
            "これらの化合物は赤血球内グルタチオンを枯渇させてヘモグロビンを酸化し、ハインツ小体形成と赤血球膜傷害を介して"
            "血管内・血管外溶血を引き起こす。猫は赤血球ヘモグロビンの構造（多数のスルフヒドリル基）により特に感受性が高い。"
            "摂取後数日で溶血性貧血・血色素尿・黄疸・元気消失・頻呼吸が顕在化する。加熱・粉末でも毒性は失われない。"
        ),
        "causes_ja": (
            "生・加熱・乾燥・粉末を問わず、タマネギ・ニンニク・長ネギ・ニラや、それらを含む食品"
            "（オニオンスープ・ガーリックパウダー・ベビーフード等）の摂取が原因。"
            "猫および犬で発生し、少量の反復摂取でも蓄積的に溶血を起こしうる。"
        ),
        "patho_en": (
            "oxidative haemolysis caused by organosulfur compounds (e.g. n-propyl disulfide) in Allium species "
            "(onion, garlic, chives, leek). These deplete erythrocyte glutathione and oxidise haemoglobin, producing "
            "Heinz bodies and membrane damage with intra- and extravascular haemolysis. Cats are especially "
            "susceptible owing to their sulfhydryl-rich haemoglobin. Haemolytic anaemia, haemoglobinuria and icterus "
            "appear over several days; cooking and powdering do not remove the toxicity."
        ),
        "causes_en": (
            "ingestion of onion, garlic, leek or chives — raw, cooked, dried or powdered — or foods containing them "
            "(onion soup, garlic powder, some baby foods). Repeated small amounts can be cumulatively haemolytic."
        ),
    },
    "macadamia": {
        "patho_ja": (
            "マカダミアナッツによる犬特有の中毒症候群で、機序は完全には解明されていない。"
            "摂取後12時間以内に後肢を中心とした筋力低下・起立困難・運動失調・振戦・高体温・嘔吐を呈する。"
            "症状は概ね一過性・自己限定性で、24〜48時間で回復することが多いが、高体温や脱水を伴う場合は支持療法を要する。"
        ),
        "causes_ja": (
            "マカダミアナッツ（生・ロースト・菓子に含まれるものを含む）の摂取が原因。"
            "犬で報告され、比較的少量（2〜3 g/kg 程度）でも症状を生じうる。チョコレートで被覆された製品では併発中毒に注意する。"
        ),
        "patho_en": (
            "a dog-specific syndrome from macadamia nuts whose mechanism is incompletely understood. Within 12 h "
            "ingestion causes weakness (especially of the hindlimbs), inability to stand, ataxia, tremor, hyperthermia "
            "and vomiting. Signs are usually transient and self-limiting, resolving in 24–48 h, though hyperthermia "
            "and dehydration may require supportive care."
        ),
        "causes_en": (
            "ingestion of macadamia nuts (raw, roasted or in confectionery). Reported in dogs; relatively small "
            "amounts (~2–3 g/kg) can cause signs. Watch for concurrent chocolate toxicosis with coated products."
        ),
    },
    "nsaid": {
        "patho_ja": (
            "非ステロイド性抗炎症薬（NSAID）の過量・誤食による中毒である。"
            "NSAID はシクロオキシゲナーゼ（COX-1/COX-2）を阻害してプロスタグランジン合成を抑制する。"
            "胃粘膜保護プロスタグランジン（PGE2）の喪失により胃・十二指腸潰瘍・穿孔・消化管出血を、"
            "腎血流維持プロスタグランジンの喪失により腎乳頭壊死・急性腎傷害を引き起こす。"
            "高用量では中枢神経症状（運動失調・痙攣）や肝傷害も生じる。犬・猫・フェレットは特に消化管・腎毒性に感受性が高い。"
        ),
        "causes_ja": (
            "人用 NSAID（イブプロフェン・ナプロキセン・アスピリン等）や動物用 NSAID の過量投与・誤食が原因。"
            "飼い主による自己判断での人用鎮痛薬の投与が重大な医原性中毒の原因となる。猫はグルクロン酸抱合能が低く特に危険。"
        ),
        "patho_en": (
            "overdose/ingestion of non-steroidal anti-inflammatory drugs. NSAIDs inhibit cyclo-oxygenase (COX-1/2) and "
            "prostaglandin synthesis. Loss of gastroprotective PGE2 causes gastroduodenal ulceration, perforation and "
            "GI haemorrhage; loss of renal-blood-flow prostaglandins causes renal papillary necrosis and acute kidney "
            "injury. High doses add CNS signs and hepatic injury. Dogs, cats and ferrets are especially susceptible."
        ),
        "causes_en": (
            "overdose or ingestion of human NSAIDs (ibuprofen, naproxen, aspirin) or veterinary NSAIDs. Owner "
            "administration of human analgesics is a major cause of iatrogenic poisoning; cats are at particular risk "
            "owing to limited glucuronidation."
        ),
    },
    "acetaminophen": {
        "patho_ja": (
            "アセトアミノフェン（パラセタモール）の中毒である。通常用量では肝でグルクロン酸・硫酸抱合により解毒されるが、"
            "過量では抱合経路が飽和し、CYP450 により反応性中間代謝物 NAPQI が過剰生成される。"
            "NAPQI はグルタチオンを枯渇させ、肝細胞蛋白と結合して中心静脈帯の肝壊死を引き起こす。"
            "猫はグルクロン酸抱合能が著しく低く極めて感受性が高い——猫ではメトヘモグロビン血症（チョコレート色の血液・チアノーゼ・顔面/前肢の浮腫）が主徴で、致死的となる。"
        ),
        "causes_ja": (
            "人用解熱鎮痛薬（アセトアミノフェン含有の市販感冒薬を含む）の誤食・飼い主による投与が原因。"
            "猫では1錠（325〜500 mg）でも致死的となりうるため、いかなる量の曝露も緊急対応を要する。犬では肝毒性が主体。"
        ),
        "patho_en": (
            "acetaminophen (paracetamol) poisoning. At therapeutic doses it is detoxified by hepatic glucuronidation/"
            "sulfation, but overdose saturates these pathways and CYP450 generates excess reactive NAPQI, which "
            "depletes glutathione and binds hepatocyte proteins, causing centrilobular hepatic necrosis. Cats have "
            "markedly deficient glucuronidation and are extremely sensitive — methaemoglobinaemia (chocolate-brown "
            "blood, cyanosis, facial/paw oedema) predominates in cats and is frequently fatal."
        ),
        "causes_en": (
            "ingestion of human antipyretic/analgesic products (including OTC cold remedies) or owner administration. "
            "A single tablet can be fatal to a cat, so any exposure is an emergency; hepatotoxicity predominates in dogs."
        ),
    },
    "lily": {
        "patho_ja": (
            "ユリ（Lilium 属・Hemerocallis 属＝ヤブカンゾウ/デイリリー）による中毒で、毒性は動物種により大きく異なる。"
            "毒性成分は未同定だが、猫では花・葉・茎・花粉・生けた水のいずれも腎近位尿細管上皮の壊死を引き起こす。"
            "猫では摂取後数時間で嘔吐・流涎・食欲不振を呈し、12〜72時間で多飲多尿に続く乏尿/無尿性の急性腎不全に進行する。"
            "対応が遅れると不可逆性腎不全・死に至るため、猫では曝露そのものが救急である。"
            "一方、犬では通常は一過性の消化器症状（嘔吐・流涎）にとどまり、猫のような重篤な腎毒性は生じない。"
        ),
        "causes_ja": (
            "テッポウユリ・オニユリ・スターゲイザー・デイリリー等の摂取・咀嚼、花粉のグルーミング、"
            "花を生けた水の摂取が原因。とくに猫ではごく少量（花弁1枚・花粉の舐め取り）でも致死的な腎傷害を起こしうる。"
        ),
        "patho_en": (
            "poisoning by true lilies (Lilium) and daylilies (Hemerocallis) whose toxicity differs markedly by species. "
            "The toxic principle is unidentified, but in cats any part — flower, leaf, stem, pollen or vase water — "
            "causes proximal renal tubular necrosis: vomiting and anorexia appear within hours, progressing over "
            "12–72 h to oligo-/anuric renal failure, so exposure itself is an emergency in cats. Dogs, by contrast, "
            "develop only transient GI upset (vomiting, hypersalivation) and not the severe nephrotoxicity."
        ),
        "causes_en": (
            "ingestion or chewing of Easter/tiger/stargazer lilies or daylilies, grooming pollen from the coat, or "
            "drinking vase water. Even a petal or a lick of pollen can poison a cat."
        ),
    },
    "ethylene_glycol": {
        "patho_ja": (
            "エチレングリコール（不凍液・冷却液）の中毒である。エチレングリコール自体の毒性は低いが、"
            "肝のアルコール脱水素酵素によりグリコールアルデヒド→グリコール酸→グリオキシル酸→シュウ酸へ代謝される。"
            "グリコール酸の蓄積が高アニオンギャップ性代謝性アシドーシスを、シュウ酸とカルシウムの結合がシュウ酸カルシウム結晶を生じ、"
            "腎尿細管に沈着して急性腎傷害（無尿）を引き起こす。第1相は酩酊様・多飲多尿、第2相は心肺症状、第3相（24〜72時間）は乏尿性腎不全。"
            "解毒（エタノール/ホメピゾール）は早期投与が必須で、遅れると致死的。"
        ),
        "causes_ja": (
            "自動車不凍液・冷却液・ブレーキ液・一部の融雪剤に含まれるエチレングリコールの摂取が原因。"
            "甘味があり犬・猫が好んで舐めるため、こぼれた不凍液や漏出した冷却液が主要曝露源となる。猫はごく少量で致死的。"
        ),
        "patho_en": (
            "ethylene glycol (antifreeze/coolant) poisoning. The parent compound is of low toxicity but hepatic alcohol "
            "dehydrogenase metabolises it to glycolaldehyde → glycolic acid → glyoxylic acid → oxalate. Glycolic acid "
            "produces severe high-anion-gap metabolic acidosis, and calcium oxalate crystals deposit in renal tubules "
            "causing anuric acute kidney injury. Stage 1 is inebriation/PU-PD, stage 2 cardiopulmonary, stage 3 "
            "(24–72 h) oliguric renal failure. Antidote (ethanol/fomepizole) must be given early."
        ),
        "causes_en": (
            "ingestion of automotive antifreeze/coolant, brake fluid or some de-icers. Its sweet taste attracts dogs "
            "and cats, so spilled coolant is the main source; cats are killed by tiny volumes."
        ),
    },
    # --- Metals -------------------------------------------------------------
    "lead": {
        "patho_ja": (
            "鉛はスルフヒドリル基に高親和性で結合し、ヘム合成酵素（δ-アミノレブリン酸脱水酵素・フェロケラターゼ）を阻害して"
            "貧血（好塩基性斑点を伴う有核赤血球の出現）を引き起こす。また血液脳関門を傷害して脳浮腫・毛細血管傷害による神経症状（発作・盲目・行動変化）を、"
            "消化管平滑筋・末梢神経への作用により疝痛・嘔吐・巨大食道を生じる。慢性曝露では腎近位尿細管傷害も来す。"
            "鳥では砂嚢内に停滞した金属片から持続的に吸収され重篤化しやすい。"
        ),
        "causes_ja": (
            "古い塗料の破片・釣りの錘・散弾・はんだ・鉛製品・一部の金属玩具やケージ部品の摂取が原因。"
            "鳥では装飾品・カーテンの錘・ステンドグラスのはんだ、放牧動物では古いバッテリー・塗料が主要曝露源となる。"
        ),
        "patho_en": (
            "lead poisoning. Lead binds avidly to sulfhydryl groups and inhibits the haem-synthesis enzymes "
            "δ-aminolevulinic acid dehydratase and ferrochelatase, producing anaemia with basophilic stippling and "
            "nucleated red cells. It also damages the blood–brain barrier (cerebral oedema, neurological signs: "
            "seizures, blindness, behaviour change) and affects GI smooth muscle and peripheral nerves (colic, "
            "vomiting, megaoesophagus). Chronic exposure injures the renal proximal tubule. In birds, metal retained "
            "in the gizzard is absorbed continuously."
        ),
        "causes_en": (
            "ingestion of old paint chips, fishing weights, gunshot, solder, lead objects, or some metal toys/cage "
            "parts. In birds, curtain weights and stained-glass solder are common; in grazing animals, old batteries "
            "and paint."
        ),
    },
    "zinc": {
        "patho_ja": (
            "胃酸により金属亜鉛からイオン化亜鉛が遊離し、強い酸化作用で赤血球膜を傷害して"
            "ハインツ小体性・血管内溶血を引き起こす（血色素尿・黄疸・重度貧血）。亜鉛は膵腺房細胞・腎尿細管・肝にも傷害を与え、"
            "膵炎・急性腎傷害・肝障害を生じうる。消化管では腐食性に作用して嘔吐・下痢を来す。"
            "胃内に停滞した亜鉛製異物（硬貨・ナット）から持続的に吸収されるため、異物除去が治療の要となる。"
        ),
        "causes_ja": (
            "1982年以降の米国1セント硬貨・亜鉛メッキ金属（ナット・ボルト・ケージ金具）・ジッパー・一部の玩具やクリームの摂取が原因。"
            "犬での硬貨誤食、鳥でのケージ金具齧りが代表的な曝露源。"
        ),
        "patho_en": (
            "zinc poisoning. Gastric acid liberates ionic zinc from metallic objects; its strong oxidant action damages "
            "erythrocyte membranes, causing Heinz-body intravascular haemolysis (haemoglobinuria, icterus, severe "
            "anaemia). Zinc also injures pancreatic acinar cells, renal tubules and liver (pancreatitis, AKI, hepatic "
            "injury) and is corrosive to the GI tract. Continuous absorption from a retained zinc foreign body makes "
            "removal central to treatment."
        ),
        "causes_en": (
            "ingestion of post-1982 US pennies, galvanised metal (nuts, bolts, cage hardware), zippers or some toys/"
            "creams. Coin ingestion in dogs and cage-hardware chewing in birds are typical sources."
        ),
    },
    "copper": {
        "patho_ja": (
            "過剰な銅が肝細胞のライソゾームに蓄積し、酸化的傷害により慢性肝障害・肝硬変を引き起こす。"
            "蓄積が閾値を超えると、貯蔵銅が血中へ急激に放出され、赤血球を酸化傷害して急性溶血性危機（ヘモグロビン尿・黄疸・突然死）を生じる。"
            "ヒツジで古典的だが、銅排泄の遺伝的欠陥を持つ犬種（ベドリントンテリア等）や、銅過剰飼料・環境曝露でも発生する。"
        ),
        "causes_ja": (
            "飼料・水・環境（銅製パイプ・殺真菌剤・補助飼料）からの慢性的な銅過剰摂取、または銅排泄障害を持つ素因が原因。"
            "反芻動物では飼料中銅:モリブデン比の不均衡が、犬では遺伝性銅蓄積症が主因となる。"
        ),
        "patho_en": (
            "copper poisoning. Excess copper accumulates in hepatocyte lysosomes, causing chronic oxidative hepatic "
            "injury and cirrhosis. Once a threshold is exceeded, stored copper is released abruptly into blood and "
            "oxidatively damages red cells, triggering an acute haemolytic crisis (haemoglobinuria, icterus, sudden "
            "death). Classic in sheep, but also in breeds with a hereditary copper-excretion defect (e.g. Bedlington "
            "terrier) and with dietary/environmental excess."
        ),
        "causes_en": (
            "chronic excess copper intake from feed, water or environment (copper piping, fungicides, supplements) or "
            "an inherited copper-excretion defect. In ruminants, an imbalanced dietary copper:molybdenum ratio is key."
        ),
    },
    "iron": {
        "patho_ja": (
            "過剰な遊離鉄は消化管粘膜に直接腐食性に作用して出血性胃腸炎を引き起こし、"
            "吸収された鉄はフリーラジカルを生成して肝細胞・心筋を傷害する。"
            "典型的には4相性の経過（消化管症状期→見かけの回復期→ショック・代謝性アシドーシス期→肝壊死期）をたどる。"
            "血清鉄が総鉄結合能を超えると遊離鉄毒性が顕在化する。"
        ),
        "causes_ja": (
            "鉄分サプリメント・鉄剤・妊婦用ビタミン・一部の除草剤や苔取り剤（硫酸鉄）・カイロ内容物の摂取が原因。"
            "甘くコーティングされた鉄錠剤を大量に誤食した小型犬で重症化しやすい。"
        ),
        "patho_en": (
            "iron poisoning. Excess free iron is directly corrosive to GI mucosa (haemorrhagic gastroenteritis), and "
            "absorbed iron generates free radicals that injure hepatocytes and myocardium. The classic course is "
            "four-phase: GI signs → apparent recovery → shock/metabolic acidosis → hepatic necrosis. Free-iron "
            "toxicity appears once serum iron exceeds total iron-binding capacity."
        ),
        "causes_en": (
            "ingestion of iron supplements, prenatal vitamins, some herbicides/moss killers (ferrous sulfate) or "
            "hand-warmer contents. Small dogs that eat many sweet-coated iron tablets are at greatest risk."
        ),
    },
    # --- Insecticides / drugs ----------------------------------------------
    "organophosphate": {
        "patho_ja": (
            "有機リン・カーバメート系殺虫剤による中毒である。これらはアセチルコリンエステラーゼを阻害し（有機リンは不可逆的・"
            "カーバメートは可逆的）、シナプスにアセチルコリンが過剰蓄積する。"
            "ムスカリン性過剰（流涎・流涙・縮瞳・気道分泌過多・徐脈・嘔吐下痢＝SLUDGE）、"
            "ニコチン性過剰（筋線維束攣縮・筋力低下・麻痺）、中枢性（不安・痙攣・呼吸中枢抑制）が混在する。"
            "死因は気道分泌・気管支攣縮・呼吸筋麻痺による呼吸不全である。"
        ),
        "causes_ja": (
            "有機リン・カーバメート系の殺虫剤・殺ダニ剤・ノミ駆除剤・殺鼠用に誤用された農薬の摂取・経皮/吸入曝露が原因。"
            "農地・家庭園芸での製剤、過量使用された外部寄生虫駆除剤が主要曝露源となる。"
        ),
        "patho_en": (
            "organophosphate/carbamate insecticide poisoning. These inhibit acetylcholinesterase (irreversibly for "
            "organophosphates, reversibly for carbamates), so acetylcholine accumulates at synapses. Muscarinic excess "
            "(salivation, lacrimation, miosis, bronchorrhoea, bradycardia, vomiting/diarrhoea — SLUDGE), nicotinic "
            "excess (fasciculations, weakness, paralysis) and central effects (anxiety, seizures, respiratory-centre "
            "depression) coexist. Death is from respiratory failure."
        ),
        "causes_en": (
            "ingestion, dermal or inhalational exposure to organophosphate/carbamate insecticides, acaricides, flea "
            "products or agrochemicals misused as rodenticides. Agricultural/garden products and overdosed ectoparasite "
            "treatments are common sources."
        ),
    },
    "pyrethroid": {
        "patho_ja": (
            "ピレスロイド・ピレトリン系殺虫剤による中毒である。これらは神経細胞の電位依存性ナトリウムチャネルの不活化を遅延させ、"
            "脱分極を遷延させて反復発火を起こし、振戦・筋攣縮・運動失調・流涎・痙攣・高体温を引き起こす。"
            "猫はグルクロン酸抱合能が低くピレスロイドの代謝が遅いため極めて感受性が高く、"
            "犬用高濃度ペルメトリン製剤の誤用が猫の重篤・致死的中毒の代表的原因となる。"
        ),
        "causes_ja": (
            "ペルメトリン・デルタメトリン等を含むノミ・ダニ駆除剤や家庭用殺虫剤への曝露が原因。"
            "とりわけ犬用の高濃度ペルメトリンスポットオン製剤を猫に誤用した場合、または同居犬への塗布後の接触で重篤化する。"
        ),
        "patho_en": (
            "pyrethroid/pyrethrin insecticide poisoning. These slow inactivation of voltage-gated sodium channels, "
            "prolonging depolarisation and causing repetitive firing — tremor, muscle fasciculation, ataxia, "
            "hypersalivation, seizures and hyperthermia. Cats metabolise pyrethroids slowly (low glucuronidation) and "
            "are extremely sensitive; misapplication of concentrated canine permethrin spot-ons to cats is the classic "
            "cause of severe, often fatal poisoning."
        ),
        "causes_en": (
            "exposure to permethrin/deltamethrin flea-tick products or household insecticides. Severe cases follow "
            "applying concentrated canine permethrin spot-ons to cats, or contact with a recently treated housemate dog."
        ),
    },
    "ivermectin": {
        "patho_ja": (
            "イベルメクチン等のマクロライド系（アベルメクチン/ミルベマイシン）駆虫薬による神経毒性である。"
            "これらは無脊椎動物のグルタミン酸作動性塩素チャネルを標的とするが、高用量では哺乳類中枢神経の GABA 作動性塩素チャネルにも作用し、"
            "中枢抑制・運動失調・散瞳・流涎・徐脈・昏睡・呼吸抑制を引き起こす。"
            "通常は血液脳関門の P-糖蛋白（ABCB1/MDR1）が脳内移行を防ぐが、ABCB1-1Δ 変異を持つ犬種（コリー系等）や高用量では中枢へ移行し重篤化する。"
        ),
        "causes_ja": (
            "イベルメクチン・モキシデクチン等の過量投与（大動物用製剤の小動物への誤用、馬用ペーストの摂取を含む）が原因。"
            "ABCB1（MDR1）遺伝子変異を持つ犬種では常用量でも中毒を起こしうる。爬虫類はイベルメクチンに極めて感受性が高く禁忌に近い。"
        ),
        "patho_en": (
            "neurotoxicity from macrocyclic-lactone (avermectin/milbemycin) antiparasitics such as ivermectin. They "
            "target invertebrate glutamate-gated chloride channels, but at high doses also act on mammalian CNS "
            "GABA-gated chloride channels, causing CNS depression, ataxia, mydriasis, hypersalivation, bradycardia, "
            "coma and respiratory depression. P-glycoprotein (ABCB1/MDR1) normally excludes them from the brain; dogs "
            "with the ABCB1-1Δ mutation (e.g. Collies) and high doses allow CNS entry and severe toxicity."
        ),
        "causes_en": (
            "overdose of ivermectin/moxidectin (large-animal formulations misused in small animals, or ingestion of "
            "equine paste). Breeds with the ABCB1 (MDR1) mutation can be poisoned at standard doses; reptiles are "
            "extremely sensitive and ivermectin is essentially contraindicated."
        ),
    },
    "metronidazole": {
        "patho_ja": (
            "メトロニダゾールの蓄積性神経毒性である。高用量・長期投与により中枢神経（特に前庭小脳系）に可逆性の傷害を生じ、"
            "前庭失調・眼振・運動失調・斜頸・振戦・発作を引き起こす。機序は神経細胞内 RNA 結合とフリーラジカル生成による軸索・小脳傷害と考えられる。"
            "総投与量・投与期間に依存し、投与中止と支持療法（ジアゼパムが回復を早めるとの報告）で多くは回復する。"
        ),
        "causes_ja": (
            "メトロニダゾールの高用量（>60 mg/kg/日）または長期投与が原因。"
            "肝機能低下例では代謝遅延により常用量でも蓄積し中毒を起こしうる。爬虫類など代謝の遅い種では特に慎重な用量設定を要する。"
        ),
        "patho_en": (
            "cumulative metronidazole neurotoxicity. High-dose or prolonged therapy causes reversible CNS injury, "
            "especially of the vestibulocerebellar system — vestibular ataxia, nystagmus, head tilt, tremor and "
            "seizures — thought to arise from neuronal RNA binding and free-radical axonal/cerebellar injury. It is "
            "dose- and duration-dependent and usually resolves on withdrawal and supportive care (diazepam reportedly "
            "speeds recovery)."
        ),
        "causes_en": (
            "high-dose (>60 mg/kg/day) or prolonged metronidazole therapy. Hepatic impairment slows metabolism so "
            "even standard doses can accumulate; slow-metabolising species (e.g. reptiles) need cautious dosing."
        ),
    },
    "cannabis": {
        "patho_ja": (
            "大麻（カンナビス）／Δ9-THC による中毒である。THC は中枢神経の CB1 カンナビノイド受容体に作用し、"
            "神経伝達を抑制して中枢抑制・運動失調・特徴的な「静止性運動失調（ふらつきながら立ち続ける）」・尿失禁・散瞳・"
            "驚愕反応亢進・徐脈・低体温を引き起こす。重症例では昏睡・呼吸抑制に至るが、致死例は比較的稀である。"
            "高濃度の食用大麻製品（バター・オイル・菓子）ではチョコレートやキシリトールの併発中毒に注意する。"
        ),
        "causes_ja": (
            "乾燥大麻・大麻オイル・食用大麻製品（ブラウニー等）・受動喫煙への曝露が原因。"
            "犬での誤食が最多で、廃棄物や飼い主の所持品からの摂取が典型的な曝露源となる。"
        ),
        "patho_en": (
            "cannabis / Δ9-THC poisoning. THC acts on CNS CB1 cannabinoid receptors, depressing neurotransmission to "
            "cause CNS depression, ataxia, the characteristic 'static ataxia' (swaying while standing), urinary "
            "incontinence, mydriasis, hyperaesthesia, bradycardia and hypothermia. Severe cases reach coma/respiratory "
            "depression, but death is relatively rare. Watch for concurrent chocolate/xylitol toxicosis with edibles."
        ),
        "causes_en": (
            "exposure to dried cannabis, cannabis oil, edibles (e.g. brownies) or second-hand smoke. Ingestion is most "
            "common in dogs, typically from discarded material or an owner's supply."
        ),
    },
    "mushroom": {
        "patho_ja": (
            "毒キノコによる中毒で、毒性は摂取したキノコの種類により大きく異なる。"
            "アマトキシン含有種（タマゴテングタケ等）は RNA ポリメラーゼ II を阻害して致死的な肝壊死・急性肝不全を引き起こす。"
            "ムスカリン含有種はコリン作動性症状（SLUDGE）を、イボテン酸/ムッシモール含有種は中枢症状（興奮・発作・昏睡）を、"
            "胃腸刺激性種は嘔吐下痢を生じる。種同定が困難なため、初期の消化管症状でも肝毒性種を想定した対応が重要である。"
        ),
        "causes_ja": (
            "野外・庭に自生する毒キノコの摂取が原因。雨後に発生したキノコを犬が拾い食いする事例が多い。"
            "摂取したキノコ・嘔吐物の保存が種同定と治療方針決定に役立つ。"
        ),
        "patho_en": (
            "mushroom poisoning, with toxicity varying greatly by species. Amatoxin-containing mushrooms (e.g. Amanita) "
            "inhibit RNA polymerase II, causing fatal hepatic necrosis and acute liver failure; muscarinic species "
            "cause cholinergic (SLUDGE) signs; ibotenic-acid/muscimol species cause CNS signs (agitation, seizures, "
            "coma); GI-irritant species cause vomiting/diarrhoea. Because identification is hard, even early GI signs "
            "should be managed as a possible hepatotoxic species."
        ),
        "causes_en": (
            "ingestion of wild mushrooms in yards or fields, often scavenged by dogs after rain. Saving the mushroom or "
            "vomitus aids species identification and treatment."
        ),
    },
    "metaldehyde": {
        "patho_ja": (
            "メタアルデヒド（ナメクジ・カタツムリ駆除剤）による中毒である。中枢神経の抑制性神経伝達物質（GABA・セロトニン・"
            "ノルアドレナリン）を減少させ、興奮性が亢進する。"
            "全身性の筋振戦・運動失調・痙攣・著明な高体温（いわゆる「shake and bake」）・頻呼吸・代謝性アシドーシスを引き起こし、"
            "持続する痙攣と高体温が横紋筋融解・DIC・肝傷害・死をもたらす。"
        ),
        "causes_ja": (
            "メタアルデヒドを含むナメクジ・カタツムリ用ペレット/顆粒の摂取が原因。"
            "ペレットが穀物様で誘引性が高いため、庭に散布された製剤を犬が摂取する事例が多い。"
        ),
        "patho_en": (
            "metaldehyde (slug/snail bait) poisoning. It lowers inhibitory CNS neurotransmitters (GABA, serotonin, "
            "noradrenaline), raising excitability to cause generalised tremor, ataxia, seizures and marked hyperthermia "
            "('shake and bake'), tachypnoea and metabolic acidosis. Sustained convulsions and hyperthermia lead to "
            "rhabdomyolysis, DIC, hepatic injury and death."
        ),
        "causes_en": (
            "ingestion of metaldehyde slug/snail pellets. The grain-like, palatable pellets are readily eaten by dogs "
            "from treated gardens."
        ),
    },
    "strychnine": {
        "patho_ja": (
            "ストリキニーネは脊髄・脳幹の抑制性神経伝達物質グリシンの受容体を競合的に拮抗し、"
            "運動ニューロンの脱抑制を引き起こす。その結果、外的刺激（音・光・接触）で誘発される全身性の強直性痙攣・"
            "伸筋優位の硬直（後弓反張）・「ノコギリ歯様」発作を呈する。意識は保たれることが多い。"
            "呼吸筋の持続的強直による換気不全・高体温が死因となる。"
        ),
        "causes_ja": (
            "ストリキニーネを含む殺鼠剤・モグラ駆除剤・有害動物駆除剤（違法・悪意ある毒餌を含む）の摂取が原因。"
            "悪意による毒殺で用いられることもある。"
        ),
        "patho_en": (
            "strychnine poisoning. Strychnine competitively antagonises glycine receptors in the spinal cord and "
            "brainstem, disinhibiting motor neurons. The result is stimulus-evoked (sound/light/touch) generalised "
            "tonic convulsions with extensor rigidity (opisthotonus) and 'sawhorse' posture, usually with retained "
            "consciousness. Death follows ventilatory failure and hyperthermia from sustained respiratory-muscle spasm."
        ),
        "causes_en": (
            "ingestion of strychnine-containing rodenticides, mole baits or pest baits (including illegal/malicious "
            "baits); also used in deliberate poisonings."
        ),
    },
    "bromethalin": {
        "patho_ja": (
            "ブロメタリン系殺鼠剤による中毒である。ブロメタリンの代謝物がミトコンドリアの酸化的リン酸化を脱共役させ、"
            "ATP 産生を障害する。ATP 依存性の Na/K ポンプ機能不全により中枢神経に液体が貯留し、脳浮腫・髄液圧上昇・髄鞘内浮腫を生じる。"
            "高用量では急性に痙攣・過敏・運動失調を、低用量では数日かけて進行する麻痺・運動失調・後肢不全麻痺・中枢抑制を呈する。"
            "抗凝固性殺鼠剤と異なりビタミンKは無効で、特異的解毒薬がない。"
        ),
        "causes_ja": (
            "ブロメタリンを有効成分とする殺鼠剤（第二世代抗凝固剤の代替として普及）の摂取が原因。"
            "抗凝固性殺鼠剤と外見が似るため、製品の有効成分確認が治療方針上きわめて重要である。"
        ),
        "patho_en": (
            "bromethalin rodenticide poisoning. Its metabolite uncouples mitochondrial oxidative phosphorylation, "
            "impairing ATP production; failure of ATP-dependent Na/K pumps causes fluid accumulation in the CNS with "
            "cerebral oedema, raised CSF pressure and intramyelinic oedema. High doses cause acute seizures and "
            "hyperexcitability; low doses cause paralysis, ataxia and CNS depression evolving over days. Unlike "
            "anticoagulant baits, vitamin K is useless and there is no specific antidote."
        ),
        "causes_en": (
            "ingestion of bromethalin-based rodenticide (now widely used in place of second-generation anticoagulants). "
            "It resembles anticoagulant baits, so confirming the active ingredient is critical to management."
        ),
    },
    "anticoagulant_rodenticide": {
        "patho_ja": (
            "抗凝固性殺鼠剤（ワルファリン・第二世代スーパーワルファリン）による中毒である。"
            "これらはビタミンK エポキシド還元酵素を阻害し、ビタミンK依存性凝固因子（II・VII・IX・X）の活性化を妨げる。"
            "既存の凝固因子が枯渇する2〜5日後に凝固障害が顕在化し、体腔内出血・血胸・血腹・皮下血腫・喀血・血尿・貧血を引き起こす。"
            "第二世代製剤は半減期が長く、ビタミンK1 の長期投与（3〜4週間）を要する。"
        ),
        "causes_ja": (
            "ワルファリン・ブロディファコウム・ジファシノン等を含む殺鼠剤の摂取（一次中毒）、"
            "または中毒した齧歯類を捕食したことによる二次中毒が原因。家庭・倉庫・農場での毒餌設置が主要曝露源。"
        ),
        "patho_en": (
            "anticoagulant rodenticide (warfarin / second-generation 'super-warfarin') poisoning. These inhibit "
            "vitamin K epoxide reductase, preventing activation of vitamin-K-dependent clotting factors (II, VII, IX, "
            "X). Coagulopathy appears 2–5 days later as existing factors are depleted, causing body-cavity haemorrhage "
            "(haemothorax, haemoabdomen), haematomas, haemoptysis, haematuria and anaemia. Second-generation products "
            "have long half-lives and need 3–4 weeks of vitamin K1."
        ),
        "causes_en": (
            "ingestion of warfarin/brodifacoum/diphacinone baits (primary poisoning), or eating poisoned rodents "
            "(secondary poisoning). Baits set in homes, sheds and farms are the main source."
        ),
    },
    # --- Salts / alcohols / vitamins ---------------------------------------
    "salt": {
        "patho_ja": (
            "過剰なナトリウム摂取または飲水制限による相対的高ナトリウム血症で、"
            "細胞外液の浸透圧が上昇し脳細胞から水が引き出されて神経細胞が脱水・収縮する。"
            "この状態で急速に水を与えると（または補正が速すぎると）脳細胞内へ水が急激に移動して脳浮腫・痙攣・昏睡を引き起こす。"
            "嘔吐・下痢・運動失調・振戦・発作・多飲を呈し、補正速度が予後を左右する。"
        ),
        "causes_ja": (
            "海水・岩塩・手作り粘土（塩生地）・大量の調味食品・誤った経口補水の摂取、または飲水不足/脱水が原因。"
            "鳥・小動物では給水切れ、犬では海水飲水や塩分の高い食品の誤食が典型的な曝露源となる。"
        ),
        "patho_en": (
            "salt (sodium) toxicosis / water deprivation. Excess sodium intake or restricted water causes "
            "hypernatraemia; rising extracellular osmolality draws water out of brain cells, dehydrating neurons. If "
            "water is then offered too quickly (or sodium corrected too fast), water shifts rapidly back into brain "
            "cells, causing cerebral oedema, seizures and coma. Vomiting, ataxia, tremor and PU-PD occur; correction "
            "rate determines outcome."
        ),
        "causes_en": (
            "ingestion of seawater, rock salt, homemade salt dough, heavily seasoned food or incorrect oral "
            "rehydration, or inadequate water/dehydration. Empty water sources in birds/small mammals and seawater "
            "drinking in dogs are typical."
        ),
    },
    "ethanol": {
        "patho_ja": (
            "エタノールは中枢神経を抑制し、運動失調・嗜眠・嘔吐・低体温・"
            "代謝性アシドーシス・低血糖を引き起こす。重症例では呼吸中枢抑制・昏睡・誤嚥に至る。"
            "発酵中のパン生地では、酵母が産生するエタノールに加え、生地の胃内膨張による胃拡張も合併する。"
        ),
        "causes_ja": (
            "アルコール飲料・未発酵のパン生地（イースト発酵）・消毒用アルコール・観賞用酒類・発酵果実の摂取が原因。"
            "体格の小さい犬・猫では少量でも重篤化する。"
        ),
        "patho_en": (
            "ethanol (alcohol) poisoning. Ethanol depresses the CNS, causing ataxia, lethargy, vomiting, hypothermia, "
            "metabolic acidosis and hypoglycaemia; severe cases reach respiratory depression, coma and aspiration. "
            "Rising bread dough adds yeast-generated ethanol plus gastric distension from dough expansion."
        ),
        "causes_en": (
            "ingestion of alcoholic drinks, unbaked yeast bread dough, rubbing alcohol, ornamental liquors or "
            "fermenting fruit. Small dogs and cats are severely affected by small amounts."
        ),
    },
    "vitamin_d": {
        "patho_ja": (
            "過剰なビタミンD は腸管からのカルシウム・リン吸収亢進、"
            "骨吸収促進、腎でのカルシウム再吸収増加を介して高カルシウム血症・高リン血症を引き起こす。"
            "カルシウム×リン積の上昇により、腎・血管・心筋・消化管・肺へ転移性の軟部組織石灰化が進行し、"
            "多飲多尿・嘔吐・食欲不振・急性腎傷害をもたらす。半減期が長く高カルシウム血症が遷延するため治療は長期化する。"
        ),
        "causes_ja": (
            "コレカルシフェロール系殺鼠剤・ビタミンD サプリメント/医薬品（乾癬用軟膏カルシポトリオールを含む）・"
            "ビタミンD強化食品・観賞用植物の摂取が原因。殺鼠剤と外用薬の誤食が代表的な曝露源となる。"
        ),
        "patho_en": (
            "vitamin D (cholecalciferol) poisoning. Excess vitamin D raises intestinal calcium/phosphorus absorption, "
            "bone resorption and renal calcium reabsorption, producing hypercalcaemia and hyperphosphataemia. The "
            "elevated calcium-phosphorus product drives metastatic soft-tissue mineralisation of kidney, vessels, "
            "myocardium, GI tract and lung, with PU-PD, vomiting, anorexia and acute kidney injury. Its long half-life "
            "makes hypercalcaemia persistent and treatment prolonged."
        ),
        "causes_en": (
            "ingestion of cholecalciferol rodenticide, vitamin D supplements/medications (including calcipotriene "
            "psoriasis cream), fortified foods or some ornamental plants. Rodenticide and topical-cream ingestion are "
            "typical sources."
        ),
    },
    "vitamin_a": {
        "patho_ja": (
            "脂溶性ビタミンA の慢性過剰摂取により、"
            "骨膜での異常な新生骨形成（外骨腫・椎体癒合）、関節硬直、頸部痛、肝細胞（伊東細胞）への蓄積による肝障害を引き起こす。"
            "成長板障害・骨折リスク増加も生じる。レバー中心の不適切な食餌を続けた猫の頸椎・四肢の変形性骨症が古典的である。"
        ),
        "causes_ja": (
            "レバー・肝臓を多給する不適切な食餌、またはビタミンA サプリメントの過剰投与が原因。"
            "とくに猫・フェレット等での長期のレバー偏重給餌が代表的な発症背景となる。"
        ),
        "patho_en": (
            "hypervitaminosis A. Chronic excess of fat-soluble vitamin A causes abnormal periosteal new-bone formation "
            "(exostoses, vertebral fusion), joint stiffness, cervical pain and hepatic injury from accumulation in "
            "hepatic stellate (Ito) cells, plus growth-plate damage and fracture risk. The classic picture is "
            "deforming cervical/limb osteopathy in cats fed a liver-heavy diet."
        ),
        "causes_en": (
            "an inappropriate liver-heavy diet or over-supplementation with vitamin A. Long-term liver feeding in cats "
            "and ferrets is the classic background."
        ),
    },
    # --- Plant / mycotoxin / specialty -------------------------------------
    "sago_cycad": {
        "patho_ja": (
            "ソテツ（Cycad）中毒である。全部位、特に種子に高濃度の毒素を含む。"
            "サイカシン（cycasin）は腸内細菌により発癌性・肝毒性のメチルアゾキシメタノールへ変換され、急性肝壊死・出血性胃腸炎を引き起こす。"
            "β-メチルアミノ-L-アラニン（BMAA）等のアミノ酸は神経毒性を示す。嘔吐・下痢・肝不全・黄疸・凝固障害・神経症状を呈し、致死率が高い。"
        ),
        "causes_ja": (
            "観賞用ソテツ（サゴヤシ）の葉・茎・特に種子の摂取が原因。屋内外の鉢植え・庭木が曝露源となり、"
            "種子は誘引性が高く少量でも重篤な肝障害を起こす。"
        ),
        "patho_en": (
            "sago palm (cycad) poisoning; all parts, especially the seeds, are highly toxic. Cycasin is converted by "
            "gut bacteria to carcinogenic/hepatotoxic methylazoxymethanol, causing acute hepatic necrosis and "
            "haemorrhagic gastroenteritis, while amino acids such as BMAA are neurotoxic. Vomiting, diarrhoea, liver "
            "failure, icterus, coagulopathy and neurological signs occur, with high mortality."
        ),
        "causes_en": (
            "ingestion of ornamental sago/cycad palm — leaves, stem and especially seeds. Indoor/outdoor plants are "
            "the source; the palatable seeds cause severe hepatic injury in small amounts."
        ),
    },
    "avocado": {
        "patho_ja": (
            "アボカドに含まれる毒素ペルシン（persin）による中毒で、種により影響が異なる。"
            "鳥（特にインコ・オウム類）では心筋壊死・肺水腫・呼吸困難・突然死を引き起こし極めて感受性が高い。"
            "馬・反芻動物・ウサギでは心筋傷害に加え非感染性乳腺炎・浮腫を生じる。果肉・種・葉・樹皮のいずれも毒性を持つ。"
        ),
        "causes_ja": (
            "アボカドの果実・種・葉・樹皮の摂取が原因。家庭での果実・観葉としてのアボカドが曝露源となり、"
            "鳥での誤食が最も危険である。"
        ),
        "patho_en": (
            "poisoning by persin in avocado, with species-dependent effects. Birds (especially psittacines) are highly "
            "sensitive, developing myocardial necrosis, pulmonary oedema, dyspnoea and sudden death. Horses, ruminants "
            "and rabbits develop myocardial injury plus non-infectious mastitis and oedema. Flesh, pit, leaves and bark "
            "are all toxic."
        ),
        "causes_en": (
            "ingestion of avocado fruit, pit, leaves or bark. Household fruit or ornamental avocado is the source; "
            "ingestion in birds is most dangerous."
        ),
    },
    "cyanobacteria": {
        "patho_ja": (
            "藍藻（シアノバクテリア）水華（アオコ）の毒素による中毒である。毒素は種により異なり、"
            "ミクロシスチン等の肝毒素は肝細胞骨格を破壊して大量肝出血・急性肝不全・ショックを引き起こし、"
            "アナトキシン-a 等の神経毒素はニコチン受容体作動性に筋振戦・流涎・痙攣・呼吸筋麻痺による急死を引き起こす。"
            "汚染水を飲んだ後、神経毒では数分〜数十分、肝毒では数時間で発症する。"
        ),
        "causes_ja": (
            "富栄養化した池・湖沼で夏季に発生したアオコ（藍藻水華）の汚染水の飲水・遊泳後のグルーミングが原因。"
            "犬・家畜・水鳥で発生し、温暖・無風・栄養豊富な条件で毒素産生が増す。"
        ),
        "patho_en": (
            "poisoning by toxins from cyanobacterial (blue-green algae) blooms. Hepatotoxins (e.g. microcystins) "
            "destroy the hepatocyte cytoskeleton, causing massive hepatic haemorrhage, acute liver failure and shock; "
            "neurotoxins (e.g. anatoxin-a) act on nicotinic receptors to cause tremor, hypersalivation, seizures and "
            "sudden death from respiratory paralysis. Onset is minutes (neurotoxins) to hours (hepatotoxins) after "
            "drinking contaminated water."
        ),
        "causes_en": (
            "drinking from, or grooming after swimming in, eutrophic ponds/lakes with summer blue-green algal blooms. "
            "Affects dogs, livestock and waterfowl; warm, calm, nutrient-rich conditions increase toxin production."
        ),
    },
    "aflatoxin": {
        "patho_ja": (
            "アフラトキシンをはじめとするマイコトキシン（カビ毒）による中毒である。"
            "Aspergillus flavus/parasiticus が産生するアフラトキシンB1 は肝で反応性エポキシドへ代謝され、DNA・蛋白と結合して"
            "肝細胞壊死・胆管増生・線維化を引き起こし、慢性曝露では肝腫瘍を誘発する。"
            "嘔吐・食欲不振・黄疸・出血傾向（凝固因子産生低下）・腹水・肝性脳症を呈する。フモニシン・スタキボトリス等は標的臓器が異なる。"
        ),
        "causes_ja": (
            "カビの生えた飼料・穀物・ペットフード・ナッツ・干し草の摂取が原因。"
            "湿潤環境で保管された飼料・穀物が主要汚染源となり、汚染ロットによる集団発生もみられる。"
        ),
        "patho_en": (
            "poisoning by aflatoxins and other mycotoxins. Aflatoxin B1 from Aspergillus flavus/parasiticus is "
            "metabolised to a reactive epoxide that binds DNA and protein, causing hepatocellular necrosis, bile-duct "
            "proliferation and fibrosis, and hepatic tumours with chronic exposure. Vomiting, anorexia, icterus, "
            "bleeding (reduced clotting-factor synthesis), ascites and hepatic encephalopathy occur. Other mycotoxins "
            "(fumonisin, Stachybotrys) target different organs."
        ),
        "causes_en": (
            "ingestion of mouldy feed, grain, pet food, nuts or hay. Feed/grain stored in damp conditions is the main "
            "source, and contaminated lots can cause outbreaks."
        ),
    },
    "essential_oil": {
        "patho_ja": (
            "エッセンシャルオイル（精油）・ティーツリーオイル等による中毒である。"
            "精油に含まれるフェノール類・モノテルペン（テルピネン-4-オール等）は経皮・経口・吸入で吸収され、"
            "中枢神経抑制・運動失調・振戦・流涎・低体温・肝傷害・皮膚刺激を引き起こす。"
            "猫はフェノール類のグルクロン酸抱合能が低く特に感受性が高く、少量・低濃度でも重篤化する。"
        ),
        "causes_ja": (
            "ティーツリー・ユーカリ・ペパーミント・シトラス・パイン等の精油の経皮塗布・舐取・アロマディフューザーからの吸入が原因。"
            "「天然・安全」と誤解した飼い主による猫への高濃度精油の使用が代表的な曝露源となる。"
        ),
        "patho_en": (
            "poisoning by essential oils such as tea tree oil. Phenols and monoterpenes (e.g. terpinen-4-ol) are "
            "absorbed dermally, orally or by inhalation, causing CNS depression, ataxia, tremor, hypersalivation, "
            "hypothermia, hepatic injury and skin irritation. Cats poorly glucuronidate phenols and are especially "
            "sensitive, with severe signs from small, dilute amounts."
        ),
        "causes_en": (
            "dermal application, licking or diffuser inhalation of tea tree, eucalyptus, peppermint, citrus or pine "
            "oils. Owners using concentrated oils on cats believing them 'natural and safe' is a common cause."
        ),
    },
    "ptfe": {
        "patho_ja": (
            "ポリテトラフルオロエチレン（PTFE／テフロン）熱分解ガスによる中毒で、鳥に特異的で致死的である。"
            "過熱された PTFE 加工面から放出される熱分解煙（フッ化物含有微粒子・ガス）が、"
            "鳥の精緻で効率的な気嚢・肺システムに急性の壊死性肺炎・肺出血・肺水腫を引き起こす。"
            "突然の呼吸困難・運動失調・虚脱の後、しばしば前駆症状なく急死する。"
        ),
        "causes_ja": (
            "PTFE（テフロン）加工の調理器具・ヒーター・電球・アイロン・ホットプレート等を空焚き/過熱した際に発生する煙が原因。"
            "台所近くで飼育される鳥が主に罹患し、換気不良で重篤化する。"
        ),
        "patho_en": (
            "polytetrafluoroethylene (PTFE/Teflon) pyrolysis-fume poisoning, which is specific to birds and frequently "
            "fatal. Fumes (fluoride-containing particulates/gases) released from overheated non-stick surfaces cause "
            "acute necrotising pneumonitis, pulmonary haemorrhage and oedema in the bird's highly efficient air-sac/"
            "lung system. Sudden dyspnoea, ataxia and collapse precede death, often without warning signs."
        ),
        "causes_en": (
            "fumes from overheated PTFE (Teflon)-coated cookware, heaters, bulbs, irons or hotplates. Birds kept near "
            "kitchens are mainly affected; poor ventilation worsens it."
        ),
    },
    "cyanide": {
        "patho_ja": (
            "シアン化物中毒である。シアンはミトコンドリア電子伝達系のチトクロムcオキシダーゼ（複合体IV）に結合してこれを阻害し、"
            "細胞が酸素を利用できない「組織性（細胞性）低酸素」を引き起こす。動脈血は酸素を保持するため鮮紅色を呈する。"
            "急速に虚脱・過呼吸・粘膜鮮紅色・痙攣・呼吸停止に至り、しばしば数分〜数十分で急死する。"
        ),
        "causes_ja": (
            "青酸配糖体を含む植物（萎れたサクラ・ウメ等バラ科の葉、ソルガム/スーダングラス、亜麻、青ウメの種）の摂取、"
            "または工業用シアン化物への曝露が原因。萎凋・霜・干ばつ後の植物で青酸濃度が上昇する。"
        ),
        "patho_en": (
            "cyanide poisoning. Cyanide binds and inhibits cytochrome c oxidase (complex IV) of the mitochondrial "
            "electron-transport chain, causing histotoxic (cellular) hypoxia in which cells cannot use oxygen; arterial "
            "blood stays oxygen-rich and bright red. Rapid collapse, hyperpnoea, bright-red mucous membranes, seizures "
            "and respiratory arrest follow, often with sudden death in minutes."
        ),
        "causes_en": (
            "ingestion of cyanogenic plants (wilted Prunus leaves — cherry/plum, sorghum/Sudan grass, flax, green plum "
            "pits) or industrial cyanide. Cyanide rises in wilted, frosted or drought-stressed plants."
        ),
    },
    "nitrate": {
        "patho_ja": (
            "硝酸塩・亜硝酸塩中毒である。摂取された硝酸塩は消化管内（反芻動物では第一胃）で亜硝酸塩に還元され、"
            "亜硝酸がヘモグロビンの2価鉄を3価鉄に酸化してメトヘモグロビンを形成する。"
            "メトヘモグロビンは酸素を運搬できないため機能的低酸素を生じ、チョコレート褐色の血液・粘膜のチアノーゼ/褐色化・"
            "呼吸困難・運動不耐・虚脱を引き起こす。妊娠動物では流産も生じる。"
        ),
        "causes_ja": (
            "硝酸塩を蓄積した飼料作物（施肥過多・干ばつ後）・汚染された飲水・硝酸塩肥料の摂取が原因。"
            "反芻動物で発生しやすく、霜害・干ばつ後の牧草で硝酸塩が蓄積する。"
        ),
        "patho_en": (
            "nitrate/nitrite poisoning. Ingested nitrate is reduced to nitrite in the gut (the rumen in ruminants); "
            "nitrite oxidises haemoglobin ferrous iron to ferric, forming methaemoglobin, which cannot carry oxygen. "
            "The resulting functional hypoxia produces chocolate-brown blood, brown/cyanotic mucous membranes, "
            "dyspnoea, exercise intolerance and collapse; abortion may occur in pregnant animals."
        ),
        "causes_en": (
            "ingestion of nitrate-accumulating forage (over-fertilised or drought-stressed), contaminated water or "
            "nitrate fertiliser. Ruminants are most affected; frost or drought raises forage nitrate."
        ),
    },
    "cardiac_glycoside": {
        "patho_ja": (
            "強心配糖体（キョウチクトウ・ジギタリス・スズラン・フクジュソウ等）による中毒である。"
            "強心配糖体は細胞膜の Na+/K+-ATPase を阻害し、細胞内ナトリウム・カルシウム蓄積と細胞外高カリウム血症を引き起こす。"
            "心筋では興奮性亢進と伝導障害により重篤な不整脈（徐脈・房室ブロック・心室性不整脈）を、消化管刺激により嘔吐下痢を生じる。"
            "高カリウム血症と致死的不整脈が死因となる。全部位が有毒で、乾燥しても毒性は残る。"
        ),
        "causes_ja": (
            "キョウチクトウ・ジギタリス（キツネノテブクロ）・スズラン・フクジュソウ等の植物、"
            "またはジゴキシン製剤の過量投与が原因。剪定枝・乾燥葉でも中毒を起こし、キョウチクトウは枝を燃やした煙でも危険。"
        ),
        "patho_en": (
            "cardiac glycoside poisoning (oleander, foxglove/digitalis, lily-of-the-valley, pheasant's eye). Cardiac "
            "glycosides inhibit membrane Na+/K+-ATPase, raising intracellular sodium/calcium and extracellular "
            "potassium. In myocardium this causes increased excitability and conduction block with severe arrhythmias "
            "(bradycardia, AV block, ventricular arrhythmias) and GI irritation (vomiting/diarrhoea). Hyperkalaemia and "
            "fatal arrhythmia cause death. All parts are toxic and remain so when dried."
        ),
        "causes_en": (
            "ingestion of oleander, foxglove, lily-of-the-valley or Adonis plants, or digoxin overdose. Dried leaves "
            "and prunings remain toxic; burning oleander produces toxic smoke."
        ),
    },
    "yew": {
        "patho_ja": (
            "イチイ（Taxus 属）中毒である。イチイの全部位（仮種皮を除く）に含まれるタキシンアルカロイドは、"
            "心筋細胞のナトリウム・カルシウムチャネルを阻害して心筋の脱分極・収縮を抑制する。"
            "重篤な徐脈・房室伝導障害・心室性不整脈を急速に引き起こし、しばしば前駆症状なく突然死をもたらす。"
            "極めて少量（体重の0.1〜0.5%相当の葉）でも致死的で、乾燥・剪定枝でも毒性が保たれる。"
        ),
        "causes_ja": (
            "庭木・生垣のイチイ（セイヨウイチイ・キャラボク）の葉・小枝・種の摂取が原因。"
            "放牧地への剪定枝の投棄や庭への侵入が馬・反芻動物での集団中毒の原因となる。"
        ),
        "patho_en": (
            "yew (Taxus) poisoning. Taxine alkaloids in all parts (except the aril) block cardiac sodium and calcium "
            "channels, suppressing myocardial depolarisation and contraction. They rapidly cause severe bradycardia, "
            "AV conduction block and ventricular arrhythmias, often with sudden death and no warning. Tiny amounts "
            "(0.1–0.5% of body weight as leaves) are lethal, and dried prunings remain toxic."
        ),
        "causes_en": (
            "ingestion of yew hedge/ornamental leaves, twigs or seeds. Discarded prunings reaching pasture, or garden "
            "access, cause outbreaks in horses and ruminants."
        ),
    },
    "red_maple": {
        "patho_ja": (
            "レッドメープル（アカカエデ）中毒で、馬に特異的な酸化性溶血である。"
            "萎れた・乾燥したアカカエデの葉に含まれる没食子酸等の酸化性物質が、赤血球内グルタチオンを枯渇させてヘモグロビンを酸化し、"
            "ハインツ小体形成とメトヘモグロビン血症を伴う重度の血管内・血管外溶血を引き起こす。"
            "急性の沈鬱・粘膜蒼白/黄疸・ヘモグロビン尿（赤褐色尿）・頻呼吸を呈し、致死率が高い。"
        ),
        "causes_ja": (
            "嵐・剪定・落葉で地面に落ちた、萎れた/乾燥したアカカエデ（およびシルバーメープル等近縁種）の葉の摂取が原因。"
            "新鮮な葉より萎凋した葉で毒性が高く、秋季の発生が多い。"
        ),
        "patho_en": (
            "red maple poisoning, a horse-specific oxidative haemolysis. Oxidant compounds (e.g. gallic acid) in "
            "wilted/dried red maple leaves deplete erythrocyte glutathione and oxidise haemoglobin, causing severe "
            "intra- and extravascular haemolysis with Heinz bodies and methaemoglobinaemia. Acute depression, pale or "
            "icteric mucous membranes, haemoglobinuria and tachypnoea occur, with high mortality."
        ),
        "causes_en": (
            "ingestion of wilted/dried red maple (and related silver maple) leaves fallen after storms, pruning or "
            "leaf-fall. Wilted leaves are more toxic than fresh; most cases occur in autumn."
        ),
    },
    "oak_acorn": {
        "patho_ja": (
            "ドングリ・オーク（カシ/ナラ）中毒である。若葉・芽・ドングリに多く含まれるタンニン（加水分解されガロタンニン・没食子酸となる）が、"
            "消化管粘膜を傷害して出血性胃腸炎・便秘/下痢を、腎尿細管を傷害して急性腎傷害を引き起こす。"
            "馬・反芻動物で発生し、元気消失・疝痛・血便/黒色便・乏尿・浮腫を呈する。大量・反復摂取で重篤化する。"
        ),
        "causes_ja": (
            "秋季に大量に落下したドングリ、または春の若葉・芽の摂取が原因。"
            "オーク（カシ・ナラ）の生える放牧地で、他に餌が乏しい時期に過食する事例が多い。"
        ),
        "patho_en": (
            "oak/acorn poisoning. Tannins (hydrolysed to gallotannins and gallic acid), concentrated in young leaves, "
            "buds and acorns, injure GI mucosa (haemorrhagic gastroenteritis, constipation/diarrhoea) and renal "
            "tubules (acute kidney injury). Affects horses and ruminants with depression, colic, melaena, oliguria and "
            "oedema; large or repeated intake worsens it."
        ),
        "causes_en": (
            "ingestion of fallen acorns in autumn or young leaves/buds in spring, typically over-grazing on oak pasture "
            "when other forage is scarce."
        ),
    },
    "fescue_ergot": {
        "patho_ja": (
            "麦角アルカロイド中毒（エンドファイト感染トールフェスク・麦角菌汚染穀物）である。"
            "内生菌（Neotyphodium）や麦角菌（Claviceps）が産生する麦角アルカロイドは、ドパミン作動性・アドレナリン作動性・"
            "セロトニン作動性受容体に作用して持続的な血管収縮とプロラクチン分泌抑制を引き起こす。"
            "妊娠馬では妊娠延長・難産・無乳・胎盤肥厚を、反芻動物では四肢末端・尾・耳の壊疽（壊疽型麦角中毒）や夏季の高体温（フェスクトキシコーシス）を生じる。"
        ),
        "causes_ja": (
            "エンドファイト感染トールフェスクの採食、または麦角菌に汚染された穀物・牧草の摂取が原因。"
            "妊娠後期の馬がエンドファイト陽性フェスク牧草で放牧されることが繁殖障害の主因となる。"
        ),
        "patho_en": (
            "ergot-alkaloid poisoning (endophyte-infected tall fescue, ergot-contaminated grain). Ergot alkaloids from "
            "Neotyphodium endophytes or Claviceps act on dopaminergic, adrenergic and serotonergic receptors, causing "
            "sustained vasoconstriction and suppressed prolactin. Pregnant mares show prolonged gestation, dystocia, "
            "agalactia and thickened placenta; ruminants develop gangrene of extremities/tail/ears (gangrenous ergotism) "
            "or summer hyperthermia (fescue toxicosis)."
        ),
        "causes_en": (
            "grazing endophyte-infected tall fescue or eating ergot-contaminated grain/hay. Late-gestation mares on "
            "endophyte-positive fescue are the classic cause of reproductive failure."
        ),
    },
    "bracken": {
        "patho_ja": (
            "ワラビ（Pteridium）中毒で、種により機序が異なる。"
            "馬ではワラビに含まれるチアミナーゼがビタミンB1（チアミン）を分解し、チアミン欠乏による神経症状（運動失調・起立不能・徐脈）を引き起こす。"
            "反芻動物では別成分プタキロサイドが骨髄抑制（汎血球減少・出血）や膀胱腫瘍（地方病性血尿）を引き起こす。慢性・累積的に発症する。"
        ),
        "causes_ja": (
            "ワラビの慢性的な採食（放牧地・干し草への混入）が原因。"
            "他に餌の乏しい荒廃地・夏季の放牧で過食され、数週間の累積摂取で発症する。"
        ),
        "patho_en": (
            "bracken fern (Pteridium) poisoning, with species-dependent mechanisms. In horses, bracken thiaminase "
            "degrades thiamine (vitamin B1), causing thiamine-deficiency neurological signs (ataxia, recumbency, "
            "bradycardia). In ruminants, ptaquiloside causes bone-marrow suppression (pancytopenia, haemorrhage) and "
            "bladder tumours (enzootic haematuria). Disease is chronic/cumulative."
        ),
        "causes_en": (
            "chronic grazing of bracken (or contaminated hay), typically over-grazing poor pasture in summer; signs "
            "follow weeks of cumulative intake."
        ),
    },
    "selenium": {
        "patho_ja": (
            "セレン中毒である。過剰なセレンは含硫アミノ酸の代謝に干渉し、ケラチン形成不全を引き起こす。"
            "慢性中毒（アルカリ病）では蹄の変形・輪状裂・脱蹄、たてがみ・尾毛の脱毛、跛行を生じる。"
            "急性中毒では呼吸困難・運動失調・「盲目性蹣跚（blind staggers）」・突然死を呈する。"
            "セレン集積植物の繁茂するセレン過剰土壌地域で発生する。"
        ),
        "causes_ja": (
            "セレン過剰土壌で育った飼料・セレン集積植物の採食、またはセレン補助剤/注射の過量が原因。"
            "土壌セレン濃度の高い地域での放牧・飼料給与が主要曝露源となる。"
        ),
        "patho_en": (
            "selenium poisoning. Excess selenium interferes with sulfur-amino-acid metabolism and impairs keratin "
            "formation. Chronic toxicosis (alkali disease) causes hoof deformity, coronary-band cracking, hoof "
            "sloughing, mane/tail hair loss and lameness; acute toxicosis causes dyspnoea, ataxia, 'blind staggers' and "
            "sudden death. It occurs in seleniferous-soil regions with selenium-accumulating plants."
        ),
        "causes_en": (
            "grazing forage/accumulator plants grown on seleniferous soil, or over-supplementation/injection. Grazing "
            "and feeding in high-soil-selenium regions are the main sources."
        ),
    },
    "ionophore": {
        "patho_ja": (
            "イオノフォア（モネンシン・ラサロシド・サリノマイシン等）中毒である。"
            "イオノフォアは細胞膜を通じて陽イオン（Na+・K+・Ca2+）の移動を促進し、細胞内イオン恒常性とミトコンドリア機能を破綻させる。"
            "エネルギー需要の高い心筋・骨格筋でミトコンドリア傷害・カルシウム過負荷による壊死を引き起こす。"
            "馬は全動物中で最も感受性が高く、食欲不振・発汗・疝痛・心不全・不整脈・運動不耐を呈し、生存例も心筋線維化により予後不良となる。"
        ),
        "causes_ja": (
            "家禽・牛用飼料添加物（抗コクシジウム剤・成長促進剤）であるイオノフォアが誤って馬用飼料に混入・給与されることが原因。"
            "種を超えた飼料の取り違え・製造時の交叉汚染が主要な発生背景となる。"
        ),
        "patho_en": (
            "ionophore (monensin, lasalocid, salinomycin) poisoning. Ionophores carry cations (Na+, K+, Ca2+) across "
            "membranes, disrupting intracellular ion homeostasis and mitochondrial function. In energy-demanding "
            "cardiac and skeletal muscle this causes mitochondrial injury and calcium-overload necrosis. Horses are the "
            "most sensitive of all species, showing anorexia, sweating, colic, heart failure, arrhythmia and exercise "
            "intolerance; survivors have a guarded prognosis from myocardial fibrosis."
        ),
        "causes_en": (
            "accidental feeding of poultry/cattle ionophore feed additives (anticoccidials/growth promoters) to horses. "
            "Cross-species feed mix-ups and manufacturing cross-contamination are the usual background."
        ),
    },
    "hemlock": {
        "patho_ja": (
            "ドクニンジン（poison hemlock, Conium）・ドクゼリ（water hemlock, Cicuta）中毒で、両者は機序が異なる。"
            "ドクニンジンのコニインはニコチン様作用を示し、初期刺激後に神経筋遮断による進行性麻痺・呼吸筋麻痺を引き起こす（催奇形性もある）。"
            "ドクゼリのシクトキシンは GABA 受容体を拮抗し、激しい全身性痙攣・流涎・てんかん重積を急速に引き起こす（最も毒性の強い植物の一つ）。"
        ),
        "causes_ja": (
            "湿地・水辺・道端に自生するドクニンジン・ドクゼリの摂取が原因。"
            "セリ科の食用植物と誤認した採食や、放牧地への侵入が曝露源となる。ドクゼリは根が特に猛毒。"
        ),
        "patho_en": (
            "poison hemlock (Conium) and water hemlock (Cicuta) poisoning, which differ mechanistically. Conium's "
            "coniine is nicotinic, causing initial stimulation then neuromuscular-blockade paralysis and respiratory "
            "failure (also teratogenic). Cicuta's cicutoxin antagonises GABA receptors, rapidly causing violent "
            "generalised seizures, hypersalivation and status epilepticus (one of the most toxic plants known)."
        ),
        "causes_en": (
            "ingestion of poison/water hemlock from wet ground, ditches and roadsides — mistaken grazing of these "
            "Apiaceae or pasture incursion. Water hemlock roots are especially lethal."
        ),
    },
    "pyrrolizidine": {
        "patho_ja": (
            "ピロリジジンアルカロイド（PA）中毒である。サワギク類・ハウンドストング・サルビアモドキ等が含む PA は、"
            "肝で反応性ピロール代謝物に変換され、肝細胞の有糸分裂を阻害して肝細胞巨大化（megalocytosis）・"
            "肝静脈閉塞・進行性線維化（巨細胞性肝症）を引き起こす。慢性・累積的に進行し、しばしば数週〜数ヶ月後に肝不全・"
            "肝性脳症・光線過敏として顕在化する。摂取量と発症に時間差があるのが特徴。"
        ),
        "causes_ja": (
            "ピロリジジンアルカロイドを含む雑草（サワギク/ラグワート等）の採食、またはこれらが混入した干し草・飼料の摂取が原因。"
            "生草は不味で避けられるが、干し草に混入すると識別できず累積摂取につながる。"
        ),
        "patho_en": (
            "pyrrolizidine alkaloid (PA) poisoning. PAs from ragwort/Senecio, houndstongue and related plants are "
            "converted in the liver to reactive pyrroles that block hepatocyte mitosis, causing megalocytosis, hepatic "
            "vein occlusion and progressive fibrosis. It is chronic and cumulative, often presenting weeks to months "
            "later as liver failure, hepatic encephalopathy or photosensitisation — with a characteristic delay "
            "between intake and signs."
        ),
        "causes_en": (
            "grazing PA-containing weeds (ragwort/Senecio) or eating contaminated hay/feed. Fresh plants are unpalatable "
            "and avoided, but baled in hay they are eaten unrecognised, causing cumulative intake."
        ),
    },
    "castor_ricin": {
        "patho_ja": (
            "トウゴマ（castor bean）中毒で、毒素リシン（ricin）による。リシンはリボソームを不可逆的に不活化する蛋白合成阻害毒素で、"
            "細胞の蛋白合成を停止させて細胞死を引き起こす。重度の出血性胃腸炎・腹痛・脱水・血便、"
            "続いて多臓器（肝・腎）傷害・痙攣・循環虚脱を生じる。少数の種子（よく咀嚼された場合）でも致死的となりうる。"
        ),
        "causes_ja": (
            "トウゴマ（ヒマ）の種子の摂取が原因。観賞用・採油用のヒマ、ヒマ粕（肥料/飼料）への混入が曝露源となる。"
            "種皮が無傷だと吸収されにくいが、咀嚼により毒性が顕在化する。"
        ),
        "patho_en": (
            "castor bean poisoning by the toxin ricin, a ribosome-inactivating protein-synthesis inhibitor that halts "
            "cellular protein synthesis and causes cell death. Severe haemorrhagic gastroenteritis, abdominal pain, "
            "dehydration and bloody diarrhoea are followed by multi-organ (hepatic/renal) injury, seizures and "
            "circulatory collapse. A few well-chewed seeds can be lethal."
        ),
        "causes_en": (
            "ingestion of castor bean (Ricinus) seeds — ornamental/oil plants or contamination of castor meal "
            "fertiliser/feed. Intact seed coats limit absorption, but chewing releases the toxicity."
        ),
    },
    "black_walnut": {
        "patho_ja": (
            "クロクルミ（black walnut）の削りくず（shavings）への接触による馬の蹄葉炎である。"
            "クロクルミ材を含む敷料に立つと、経皮的に作用する毒性成分により末梢血管の血行動態が変化し、"
            "数時間以内に四肢遠位の浮腫・蹄の熱感・蹄動脈拍動亢進・跛行を伴う急性蹄葉炎を引き起こす。"
            "敷料の除去で多くは改善するが、重症例では蹄葉炎が進行する。"
        ),
        "causes_ja": (
            "クロクルミ材を含む（しばしば誤って混入した）木屑敷料への起立・接触が原因。"
            "製材所由来の混合木屑が敷料に使われた際の集団発生が典型的である。"
        ),
        "patho_en": (
            "black walnut shaving exposure causing equine laminitis. Standing on bedding containing black walnut alters "
            "distal-limb vascular haemodynamics through a percutaneously acting toxic principle, producing acute "
            "laminitis with distal-limb oedema, hoof warmth, bounding digital pulses and lameness within hours. Removal "
            "of the bedding usually helps, but severe cases progress."
        ),
        "causes_en": (
            "standing on/contact with wood-shaving bedding containing (often accidentally mixed) black walnut. "
            "Sawmill-mixed shavings used as bedding are the classic cause of outbreaks."
        ),
    },
    "cantharidin": {
        "patho_ja": (
            "ツチハンミョウ（blister beetle）由来のカンタリジンによる二次中毒で、馬に多い。"
            "カンタリジンは強力な発疱性（vesicant）毒素で、接触・吸収した消化管・泌尿器の上皮を腐食して水疱・潰瘍・出血を引き起こす。"
            "重度の疝痛・口腔/消化管粘膜のびらん・頻回排尿・血尿に加え、特徴的に低カルシウム血症・低マグネシウム血症・心筋傷害を生じ、致死率が高い。"
        ),
        "causes_ja": (
            "ツチハンミョウ（特にアルファルファ乾草の収穫時に圧死して混入したもの）を含む干し草の摂取が原因。"
            "開花期アルファルファ乾草へのツチハンミョウ混入が代表的な曝露源となる。"
        ),
        "patho_en": (
            "secondary cantharidin poisoning from blister beetles, most common in horses. Cantharidin is a potent "
            "vesicant that corrodes the GI and urinary epithelium it contacts, causing blistering, ulceration and "
            "haemorrhage. Severe colic, oral/GI mucosal erosions, frequent urination and haematuria occur, with "
            "characteristic hypocalcaemia, hypomagnesaemia and myocardial injury and high mortality."
        ),
        "causes_en": (
            "ingestion of hay containing blister beetles (especially crushed into alfalfa hay at harvest). Beetle "
            "contamination of flowering alfalfa hay is the classic source."
        ),
    },
    # --- Inhalation / environmental ----------------------------------------
    "smoke_inhalation": {
        "patho_ja": (
            "煙・有毒ガス吸入による損傷である。熱と煙の粒子が気道粘膜を直接傷害して気道浮腫・気管支攣縮・化学性肺炎を引き起こし、"
            "一酸化炭素はヘモグロビンと強固に結合（カルボキシヘモグロビン）して酸素運搬を、シアン化水素は細胞呼吸を阻害する。"
            "低酸素・呼吸困難・咳・粘膜の異常色・神経症状を呈し、気道浮腫は曝露後数時間にわたり進行しうる。"
        ),
        "causes_ja": (
            "火災・調理時の過熱した加工面・暖房器具の不完全燃焼による煙・一酸化炭素・有毒ガスへの曝露が原因。"
            "閉鎖空間での火災や換気不良の環境が重篤化要因となる。"
        ),
        "patho_en": (
            "smoke/toxic-gas inhalation injury. Heat and smoke particles directly injure the airway mucosa (airway "
            "oedema, bronchospasm, chemical pneumonitis); carbon monoxide binds haemoglobin firmly (carboxyhaemoglobin) "
            "to impair oxygen carriage, and hydrogen cyanide blocks cellular respiration. Hypoxia, dyspnoea, cough, "
            "abnormal mucous-membrane colour and neurological signs occur, with airway oedema progressing for hours."
        ),
        "causes_en": (
            "exposure to smoke, carbon monoxide and toxic gases from fires, overheated cooking surfaces or faulty "
            "heaters. Closed-space fires and poor ventilation worsen severity."
        ),
    },
    "ammonia": {
        "patho_ja": (
            "アンモニア（および亜硝酸/硝酸）中毒で、特に水生・両生動物で重要である。"
            "未熟な生物濾過や過密・過給餌により水中アンモニア（NH3）が蓄積し、鰓・皮膚を刺激・傷害してガス交換を妨げ、"
            "中枢神経毒性により遊泳異常・体表充血・呼吸促迫・粘液過多を引き起こす。"
            "亜硝酸はヘモグロビン（魚ではメトヘモグロビン＝「ブラウンブラッド病」）を酸化して機能的低酸素を生じる。pH が高いほど NH3 毒性が増す。"
        ),
        "causes_ja": (
            "立ち上げ不十分な水槽（生物濾過の未確立）・過密飼育・過剰給餌・水換え不足による窒素化合物の蓄積が原因。"
            "新規水槽症候群や濾過槽の機能停止が主要な発生背景となる。"
        ),
        "patho_en": (
            "ammonia (and nitrite/nitrate) poisoning, important especially in aquatic/amphibian species. Immature "
            "biofiltration, overstocking or overfeeding lets aqueous ammonia (NH3) accumulate, irritating and damaging "
            "gills/skin, impairing gas exchange and causing CNS toxicity with abnormal swimming, surface hyperaemia, "
            "respiratory distress and excess mucus. Nitrite oxidises haemoglobin (methaemoglobin — 'brown blood "
            "disease' in fish) causing functional hypoxia. Higher pH increases NH3 toxicity."
        ),
        "causes_en": (
            "accumulation of nitrogenous waste from an under-cycled tank (immature biofilter), overstocking, "
            "overfeeding or infrequent water changes. New-tank syndrome and filter failure are the usual background."
        ),
    },
    "arsenic": {
        "patho_ja": (
            "無機ヒ素はスルフヒドリル基含有酵素（ピルビン酸脱水素酵素等）に結合して細胞呼吸を阻害し、"
            "毛細血管の内皮を傷害して透過性を亢進させる。その結果、重度の出血性胃腸炎・脱水・循環虚脱・"
            "腎尿細管壊死・肝傷害を急速に引き起こす。急性大量曝露では数時間で起立不能・ショック・死に至る。"
            "慢性曝種では削痩・粗剛な被毛・蹄/皮膚病変を呈する。"
        ),
        "causes_ja": (
            "ヒ素含有の除草剤・殺虫剤・防腐木材・鉱業/製錬副産物・汚染飼料/水への曝露が原因。"
            "古い農薬製剤や産業汚染地での放牧が主要曝露源となる。"
        ),
        "patho_en": (
            "arsenic poisoning. Inorganic arsenic binds sulfhydryl-containing enzymes (e.g. pyruvate dehydrogenase), "
            "blocking cellular respiration, and damages capillary endothelium, raising permeability. This rapidly "
            "causes severe haemorrhagic gastroenteritis, dehydration, circulatory collapse, renal tubular necrosis and "
            "hepatic injury; acute massive exposure brings recumbency, shock and death within hours. Chronic exposure "
            "causes wasting, a rough coat and hoof/skin lesions."
        ),
        "causes_en": (
            "exposure to arsenical herbicides/insecticides, treated wood preservatives, mining/smelting by-products or "
            "contaminated feed/water. Old agrochemicals and grazing on industrially contaminated land are typical."
        ),
    },
    "mercury": {
        "patho_ja": (
            "水銀（特に有機水銀）はスルフヒドリル基に結合して酵素機能を阻害し、"
            "中枢神経（運動失調・振戦・盲目・行動異常）と腎尿細管（蛋白尿・急性腎傷害）を主に傷害する。"
            "有機水銀は脂溶性が高く血液脳関門・胎盤を通過して神経・発生毒性を示し、無機水銀は腐食性消化管傷害と腎傷害が主体となる。慢性・累積的に進行する。"
        ),
        "causes_ja": (
            "有機水銀処理された種子穀物の摂取、水銀汚染された魚/飼料、産業排水汚染環境への曝露が原因。"
            "水銀処理穀物の誤給与や汚染水系での発生が代表的である。"
        ),
        "patho_en": (
            "mercury poisoning. Mercury (especially organic forms) binds sulfhydryl groups, inhibiting enzymes and "
            "injuring chiefly the CNS (ataxia, tremor, blindness, behaviour change) and renal tubules (proteinuria, "
            "acute kidney injury). Lipophilic organic mercury crosses the blood–brain barrier and placenta (neuro- and "
            "developmental toxicity); inorganic mercury is mainly corrosive-GI and nephrotoxic. Disease is chronic and "
            "cumulative."
        ),
        "causes_en": (
            "ingestion of organomercurial-treated seed grain, mercury-contaminated fish/feed, or industrial-effluent "
            "exposure. Mis-feeding treated grain and contaminated waterways are typical."
        ),
    },
    "aminoglycoside": {
        "patho_ja": (
            "アミノグリコシド系抗菌薬（ゲンタマイシン・アミカシン等）の腎毒性である。"
            "アミノグリコシドは腎近位尿細管上皮細胞に取り込まれてライソゾーム・ミトコンドリアに蓄積し、"
            "尿細管上皮の壊死を引き起こして急性腎傷害（非乏尿性〜乏尿性）を生じる。"
            "高用量・長期投与・脱水・既存腎疾患・併用腎毒性薬で危険が高まる。内耳毒性（前庭/聴覚障害）も生じうる。"
        ),
        "causes_ja": (
            "アミノグリコシド系抗菌薬の高用量・長期投与、脱水下や腎機能低下例での投与、他の腎毒性薬との併用が原因。"
            "適切な投与間隔（1日1回投与で蓄積を低減）・腎機能/水和状態のモニタリングで予防する。"
        ),
        "patho_en": (
            "aminoglycoside (gentamicin, amikacin) nephrotoxicity. Aminoglycosides are taken up by proximal renal "
            "tubular cells and accumulate in lysosomes/mitochondria, causing tubular necrosis and acute kidney injury "
            "(non-oliguric to oliguric). Risk rises with high doses, prolonged therapy, dehydration, pre-existing renal "
            "disease and concurrent nephrotoxins; ototoxicity (vestibular/auditory) can also occur."
        ),
        "causes_en": (
            "high-dose or prolonged aminoglycoside therapy, dosing in dehydrated or renally impaired patients, or "
            "combination with other nephrotoxins. Once-daily dosing and monitoring of renal function/hydration prevent it."
        ),
    },
    "black_locust": {
        "patho_ja": (
            "ニセアカシア（ハリエンジュ、black locust）中毒である。樹皮・葉・種子に含まれる毒性レクチン（ロビン）と"
            "配糖体（ロビチン）が消化管粘膜を傷害し、嘔吐・疝痛・下痢/血便を引き起こすとともに、"
            "吸収後は脱力・運動失調・頻脈/不整脈・散瞳・沈鬱などの全身症状を生じる。特に樹皮・新芽・種子の毒性が高い。"
        ),
        "causes_ja": (
            "ニセアカシアの樹皮・葉・新芽・種子の摂取が原因。樹皮剥ぎや剪定枝・落葉の採食、放牧地への植栽が曝露源となる。"
        ),
        "patho_en": (
            "black locust poisoning. Toxic lectin (robin) and glycoside (robitin) in bark, leaves and seeds injure the "
            "GI mucosa, causing vomiting, colic and bloody diarrhoea, and after absorption produce weakness, ataxia, "
            "tachycardia/arrhythmia, mydriasis and depression. Bark, shoots and seeds are most toxic."
        ),
        "causes_en": (
            "ingestion of black locust bark, leaves, shoots or seeds — bark-stripping, eating prunings/leaf-fall, or "
            "trees planted at pasture."
        ),
    },
    "pokeweed": {
        "patho_ja": (
            "ヨウシュヤマゴボウ（pokeweed）中毒である。全草、特に根に含まれるサポニン（フィトラッカトキシン）と"
            "レクチン（ポークウィードマイトジェン）が消化管粘膜を刺激・傷害し、流涎・嘔吐・激しい腹痛・出血性下痢を引き起こす。"
            "大量摂取では吸収後に脱力・痙攣・低血圧・徐脈を生じる。根が最も毒性が高い。"
        ),
        "causes_ja": (
            "ヨウシュヤマゴボウの根・葉・茎・未熟果実の摂取が原因。荒地・放牧地に侵入した本種の採食が曝露源となる。"
        ),
        "patho_en": (
            "pokeweed poisoning. Saponins (phytolaccatoxin) and lectin (pokeweed mitogen) throughout the plant — most "
            "in the root — irritate and injure the GI mucosa, causing hypersalivation, vomiting, severe abdominal pain "
            "and haemorrhagic diarrhoea; large amounts add weakness, convulsions, hypotension and bradycardia after "
            "absorption. The root is most toxic."
        ),
        "causes_en": (
            "ingestion of pokeweed root, leaves, stems or unripe berries — grazing the plant where it invades waste "
            "ground and pasture."
        ),
    },
    "locoweed": {
        "patho_ja": (
            "ロコ草（locoweed, Astragalus/Oxytropis）中毒で、毒素スウェインソニンによる。"
            "スウェインソニンはライソゾームのα-マンノシダーゼを阻害し、未消化のオリゴ糖が細胞内に蓄積する"
            "後天性のライソゾーム蓄積症を引き起こす。神経細胞の空胞変性により、間欠的な異常行動・運動失調・"
            "意図振戦・体重減少・繁殖障害（流産・新生子異常）を慢性的に生じる。神経症状は不可逆的なことが多い。"
        ),
        "causes_ja": (
            "ロコ草（ゲンゲ属/オヤマノエンドウ属）の慢性的な採食が原因。"
            "他に餌の乏しい乾燥地放牧で嗜癖的に過食され、数週間の累積摂取で発症する。"
        ),
        "patho_en": (
            "locoweed (Astragalus/Oxytropis) poisoning by the toxin swainsonine. Swainsonine inhibits lysosomal "
            "α-mannosidase, causing an acquired lysosomal storage disease in which undigested oligosaccharides "
            "accumulate; neuronal vacuolar degeneration produces chronic intermittent abnormal behaviour, ataxia, "
            "intention tremor, weight loss and reproductive failure (abortion, neonatal defects). Neurological signs are "
            "often irreversible."
        ),
        "causes_en": (
            "chronic grazing of locoweed (Astragalus/Oxytropis), often habitually over-eaten on sparse rangeland; signs "
            "follow weeks of cumulative intake."
        ),
    },
    "phalaris": {
        "patho_ja": (
            "ファラリス（Phalaris、カナリークサヨシ等）中毒である。本草が含むトリプタミン/β-カルボリンアルカロイドが"
            "中枢神経のセロトニン作動性伝達を撹乱し、神経型では運動失調・筋振戦・過敏・「ファラリスふらつき（staggers）」・"
            "突然死を引き起こす。別型（心臓型/急性死型）では急性の心不全様突然死を生じる。慢性曝露では神経細胞への色素沈着がみられる。"
        ),
        "causes_ja": (
            "ファラリス属牧草の採食が原因。新芽期・干ばつ後・霜害後にアルカロイド濃度が上昇し、"
            "コバルト欠乏下で神経型のリスクが高まる。反芻動物で多いが馬でも発生する。"
        ),
        "patho_en": (
            "Phalaris (canary grass) poisoning. Tryptamine/β-carboline alkaloids disturb central serotonergic "
            "transmission; the nervous form causes ataxia, muscle tremor, hyperaesthesia, 'Phalaris staggers' and "
            "sudden death, while a cardiac/sudden-death form causes acute heart-failure-like death. Chronic exposure "
            "leaves pigment deposition in neurons."
        ),
        "causes_en": (
            "grazing Phalaris pasture. Alkaloids rise in young growth and after drought/frost, and cobalt deficiency "
            "increases the nervous-form risk. Most common in ruminants but also seen in horses."
        ),
    },
    "horse_chestnut": {
        "patho_ja": (
            "トチノキ・セイヨウトチノキ（horse chestnut, Aesculus）中毒である。"
            "種子・新芽・若葉に含まれる配糖体エスクリン（aesculin）とサポニンが消化管を刺激し、"
            "吸収後は中枢神経を刺激/抑制して、嘔吐・疝痛・下痢に続き、筋れん縮・運動失調・興奮または沈鬱・散瞳・"
            "歩様異常を引き起こす。種子（コニカー）が最も毒性が高い。"
        ),
        "causes_ja": (
            "トチノキの種子・新芽・若葉の摂取が原因。秋季に落下した種子（コニカー）や春の新芽の採食が曝露源となる。"
        ),
        "patho_en": (
            "horse chestnut (Aesculus) poisoning. The glycoside aesculin and saponins in seeds, shoots and young leaves "
            "irritate the GI tract and, after absorption, stimulate/depress the CNS — vomiting, colic and diarrhoea "
            "followed by muscle twitching, ataxia, excitement or depression, mydriasis and abnormal gait. The seeds "
            "(conkers) are most toxic."
        ),
        "causes_en": (
            "ingestion of horse chestnut seeds, shoots or young leaves — fallen conkers in autumn or spring shoots."
        ),
    },
    "clover": {
        "patho_ja": (
            "クローバー（シャジクソウ属）関連中毒で、原因により病態が異なる。"
            "スイートクローバーがカビ（黒斑病）で傷むとジクマロールが生成され、ビタミンK拮抗による出血性疾患を引き起こす。"
            "アルサイククローバーは光線過敏症・肝障害（big liver syndrome）を、"
            "黒斑病菌（Rhizoctonia）に感染した赤クローバーはスラフラミンによる流涎症（slobbers）を引き起こす。"
        ),
        "causes_ja": (
            "カビ・黒斑病に侵されたスイートクローバー乾草、アルサイククローバー牧草、"
            "スラフラミン産生菌に感染した赤クローバーの採食が原因。湿潤条件で傷んだクローバー乾草が主要な発生背景となる。"
        ),
        "patho_en": (
            "clover (Trifolium/Melilotus)-associated toxicosis, varying by cause. Mouldy (black-patch) sweet clover "
            "generates dicoumarol, causing a vitamin-K-antagonist bleeding disorder; alsike clover causes "
            "photosensitisation and hepatic injury (big liver syndrome); red clover infected with Rhizoctonia "
            "(black-patch fungus) causes slaframine-induced slobbers."
        ),
        "causes_en": (
            "eating mouldy/black-patch sweet clover hay, alsike clover pasture, or slaframine-producing fungus-infected "
            "red clover. Spoiled clover hay made in damp conditions is the usual background."
        ),
    },
    "hoary_alyssum": {
        "patho_ja": (
            "ホーリーアリッサム（hoary alyssum）中毒で、馬に特異的である。"
            "本草（乾草に混入したものを含む）の摂取後12〜24時間で、四肢遠位の浮腫（「stocking up」）・発熱・"
            "硬く張った浮腫・跛行/蹄葉炎を引き起こす。重症例では下痢・血液濃縮・低容量性ショックを生じる。"
            "毒性成分は未同定だが、乾燥しても毒性が保たれるのが特徴である。"
        ),
        "causes_ja": (
            "ホーリーアリッサムが混入した乾草・牧草の採食が原因。"
            "本草が混入したアルファルファ/牧草乾草が主要曝露源で、生草より乾草混入による集団発生が多い。"
        ),
        "patho_en": (
            "hoary alyssum poisoning, specific to horses. Within 12–24 h of eating the plant (including hay "
            "contamination) horses develop distal-limb oedema ('stocking up'), fever, tight firm oedema and "
            "lameness/laminitis; severe cases add diarrhoea, haemoconcentration and hypovolaemic shock. The toxic "
            "principle is unidentified but survives drying."
        ),
        "causes_en": (
            "eating hay/pasture contaminated with hoary alyssum. Contaminated alfalfa/grass hay is the main source, "
            "with outbreaks more from baled hay than fresh pasture."
        ),
    },
    "cedar": {
        "patho_ja": (
            "杉・シダー材の削りくず（敷料）による中毒で、小型哺乳類・鳥で問題となる。"
            "軟材（杉・松）から揮発する芳香族炭化水素（フェノール類・プリカトン酸等のテルペン）が、"
            "気道粘膜を刺激して呼吸器症状を、経気道/経皮吸収後に肝の薬物代謝酵素を誘導して肝への負担を引き起こす。"
            "慢性曝露で呼吸器疾患感受性の上昇・流涙・くしゃみ・皮膚炎を生じうる。"
        ),
        "causes_ja": (
            "杉・シダー・松などの軟材チップを敷料に用いることによる慢性的な揮発成分曝露が原因。"
            "換気不良のケージ・水槽での飼育が増悪因子となる。広葉樹（アスペン）や紙系敷料への変更で予防する。"
        ),
        "patho_en": (
            "cedar/softwood shaving (bedding) toxicosis, relevant to small mammals and birds. Aromatic hydrocarbons "
            "(phenols and terpenes such as plicatic acid) volatilising from softwoods (cedar, pine) irritate the "
            "respiratory mucosa and, after inhalational/dermal absorption, induce hepatic drug-metabolising enzymes, "
            "stressing the liver. Chronic exposure increases respiratory-disease susceptibility, lacrimation, sneezing "
            "and dermatitis."
        ),
        "causes_en": (
            "chronic exposure to volatiles from softwood (cedar/pine) shaving bedding, worsened by poorly ventilated "
            "cages/enclosures. Prevented by switching to hardwood (aspen) or paper-based bedding."
        ),
    },
}

# ---------------------------------------------------------------------------
# Generic fall-backs for agents that are *genuinely* generic in the data
# ---------------------------------------------------------------------------
# A handful of disease names are deliberately non-specific ("植物中毒",
# "農薬中毒", "重金属中毒", "化学物質中毒").  These cannot name a single
# mechanism, but the previous template was still misleading (it described a
# hepatorenal "toxic metabolite" mechanism that does not apply to e.g. plant
# neurotoxins).  A short, honest "the mechanism depends on the specific agent"
# statement is more accurate than a falsely specific one.

GENERIC_AGENTS: dict[str, dict[str, str]] = {
    "plant_generic": {
        "patho_ja": (
            "有毒植物による中毒で、毒性は摂取した植物と含有毒素により大きく異なる。"
            "毒素クラスごとに標的が異なり、消化管刺激性成分（シュウ酸カルシウム結晶・サポニン）は口腔/消化管の刺激・嘔吐を、"
            "強心配糖体は不整脈を、アルカロイド・グリコアルカロイドは神経/消化器症状を、"
            "腎毒性・肝毒性成分は臓器傷害を引き起こす。原因植物の同定が治療と予後評価の鍵となる。"
        ),
        "causes_ja": (
            "観葉植物・庭木・野草・切り花など有毒植物の葉・茎・花・球根・種子の摂取が原因。"
            "退屈・好奇心からの齧り、餌不足時の採食、新規植物の導入が曝露の契機となる。可能なら原因植物を同定・保存する。"
        ),
        "patho_en": (
            "plant poisoning whose toxicity varies greatly with the plant and its toxic principle. Different toxin "
            "classes hit different targets: GI-irritant components (insoluble calcium-oxalate crystals, saponins) cause "
            "oral/GI irritation and vomiting; cardiac glycosides cause arrhythmias; alkaloids/glycoalkaloids cause "
            "neurological and GI signs; nephro-/hepatotoxic components cause organ injury. Identifying the plant is key "
            "to treatment and prognosis."
        ),
        "causes_en": (
            "ingestion of leaves, stems, flowers, bulbs or seeds of toxic houseplants, garden plants, weeds or cut "
            "flowers. Boredom chewing, scarce forage and newly introduced plants are common triggers; identify and "
            "save the plant where possible."
        ),
    },
    "pesticide_generic": {
        "patho_ja": (
            "農薬・殺虫剤への曝露による中毒で、機序は製剤の有効成分により異なる。"
            "有機リン・カーバメート系はアセチルコリンエステラーゼ阻害によるコリン作動性危機を、"
            "ピレスロイド系はナトリウムチャネル傷害による神経興奮を、有機塩素系は中枢神経刺激を引き起こす。"
            "曝露経路は経口・経皮・吸入があり、製品ラベル/有効成分の確認が解毒方針の決定に不可欠である。"
        ),
        "causes_ja": (
            "農地・家庭園芸・防疫で用いられる殺虫剤・殺ダニ剤・除草剤への摂取・経皮/吸入曝露が原因。"
            "散布直後の植生への接触、保管容器への接近、過量使用された外部寄生虫駆除剤が主要曝露源となる。"
        ),
        "patho_en": (
            "pesticide/insecticide exposure whose mechanism depends on the active ingredient: organophosphates/"
            "carbamates cause a cholinergic crisis via acetylcholinesterase inhibition; pyrethroids cause neural "
            "hyperexcitability via sodium-channel disruption; organochlorines cause CNS stimulation. Exposure may be "
            "oral, dermal or inhalational, so confirming the product's active ingredient is essential for antidotal "
            "management."
        ),
        "causes_en": (
            "oral, dermal or inhalational exposure to agricultural/garden/public-health insecticides, acaricides or "
            "herbicides — contact with freshly treated vegetation, access to storage containers, or overdosed "
            "ectoparasite products."
        ),
    },
    "heavy_metal_generic": {
        "patho_ja": (
            "重金属中毒で、原因金属により標的と機序が異なる。"
            "鉛はヘム合成阻害と神経傷害を、亜鉛は酸化性溶血と膵/腎傷害を、銅は肝蓄積と溶血危機を、"
            "鉄は腐食性消化管傷害とフリーラジカル性臓器傷害を引き起こす。"
            "多くは金属異物の消化管内停滞からの持続吸収によるため、画像診断での異物確認と除去、適切なキレート療法の選択が重要である。"
        ),
        "causes_ja": (
            "金属製異物（硬貨・釣り具・塗料片・ケージ金具・玩具・はんだ等）の摂取による原因金属の持続的吸収が主因。"
            "鳥でのケージ金具/装飾品齧り、犬での硬貨/釣り具誤食が代表的な曝露源となる。"
        ),
        "patho_en": (
            "heavy-metal poisoning whose target and mechanism depend on the metal: lead inhibits haem synthesis and "
            "injures nerves; zinc causes oxidative haemolysis and pancreatic/renal injury; copper accumulates in liver "
            "and triggers haemolytic crisis; iron causes corrosive GI and free-radical organ injury. Most result from "
            "continuous absorption of a retained metallic foreign body, so imaging, removal and the correct chelator "
            "are important."
        ),
        "causes_en": (
            "continuous absorption of an ingested metallic foreign body (coins, fishing tackle, paint chips, cage "
            "hardware, toys, solder). Cage-hardware chewing in birds and coin/tackle ingestion in dogs are typical."
        ),
    },
}


# ---------------------------------------------------------------------------
# Disease-name -> canonical agent resolver
# ---------------------------------------------------------------------------
# Order matters: the most specific keyword must come first so that, e.g.,
# "ピレスリン/ペルメトリン中毒" resolves to pyrethroid before any broad match.
# Each entry is (canonical_key, [keyword, ...]); a name matches when ANY of its
# keywords is a substring of "<name_ja> <name_en>".

_AGENT_KEYWORDS: list[tuple[str, list[str]]] = [
    ("xylitol", ["キシリトール", "xylitol"]),
    ("grape_raisin", ["ブドウ・レーズン", "ブドウ／レーズン", "レーズン", "grape", "raisin"]),
    ("allium", ["タマネギ", "ねぎ", "ネギ", "ニンニク", "にんにく", "ニラ", "allium", "onion", "garlic"]),
    ("macadamia", ["マカダミア", "macadamia"]),
    ("acetaminophen", ["アセトアミノフェン", "パラセタモール", "acetaminophen", "paracetamol"]),
    ("nsaid", ["nsaid", "イブプロフェン", "ibuprofen", "naproxen", "ナプロキセン", "鎮痛剤", "鎮痛薬"]),
    ("lily", ["ユリ", "ゆり", "lily", "lilies"]),
    ("ethylene_glycol", ["エチレングリコール", "不凍液", "ethylene glycol", "antifreeze"]),
    # methylxanthine: chocolate + caffeine
    (
        "methylxanthine",
        ["チョコレート", "ココア", "カカオ", "カフェイン", "chocolate", "cocoa", "caffeine", "methylxanthine"],
    ),
    # metals.  Order matters:
    #  * heavy_metal_generic first so "混合重金属中毒（鉛・亜鉛）" stays generic
    #    rather than matching the single-metal "亜鉛"/"鉛" keywords.
    #  * zinc ("亜鉛") before lead ("鉛") because 亜鉛 contains 鉛.
    ("heavy_metal_generic", ["重金属", "混合重金属", "heavy metal"]),
    ("zinc", ["亜鉛", "zinc"]),
    ("lead", ["鉛", "lead"]),
    ("copper", ["銅", "copper"]),
    ("iron", ["鉄中毒", "鉄過剰", "iron tox", "iron poison"]),
    # insecticides / drugs
    (
        "pyrethroid",
        ["ペルメトリン", "ピレスロイド", "ピレスリン", "ピレトリン", "permethrin", "pyrethr", "deltamethrin"],
    ),
    (
        "organophosphate",
        ["有機リン", "カーバメート", "カルバメート", "organophosphate", "carbamate", "コリンエステラーゼ"],
    ),
    (
        "ivermectin",
        [
            "イベルメクチン",
            "モキシデクチン",
            "マクロライド系駆虫",
            "ivermectin",
            "moxidectin",
            "avermectin",
            "milbemycin",
            "ミルベマイシン",
        ],
    ),
    ("metronidazole", ["メトロニダゾール", "metronidazole"]),
    ("cannabis", ["大麻", "カンナビス", "マリファナ", "cannabis", "marijuana", "thc"]),
    ("mushroom", ["キノコ", "きのこ", "茸", "mushroom", "amanita", "アマニタ"]),
    ("metaldehyde", ["メタアルデヒド", "ナメクジ", "カタツムリ", "metaldehyde", "slug", "snail bait"]),
    ("strychnine", ["ストリキニーネ", "strychnine"]),
    ("bromethalin", ["ブロメタリン", "bromethalin"]),
    (
        "anticoagulant_rodenticide",
        [
            "殺鼠剤",
            "ワルファリン",
            "ブロディファコウム",
            "抗凝固性殺鼠",
            "warfarin",
            "anticoagulant rodenticide",
            "brodifacoum",
            "rodenticide",
        ],
    ),
    # salts / alcohols / vitamins
    # nitrate MUST precede salt because "硝酸塩中毒" contains "塩中毒".
    ("nitrate", ["硝酸塩", "亜硝酸", "nitrate", "nitrite", "メトヘモグロビン血症"]),
    ("salt", ["塩中毒", "塩分中毒", "食塩", "塩化ナトリウム", "salt tox", "sodium tox", "hypernatr", "salt poison"]),
    (
        "ethanol",
        ["エタノール", "アルコール中毒", "ethanol", "alcohol tox", "alcohol poison", "パン生地", "bread dough"],
    ),
    (
        "vitamin_d",
        [
            "ビタミンd中毒",
            "ビタミンd過剰",
            "コレカルシフェロール",
            "vitamin d tox",
            "cholecalciferol",
            "ブロメタリン以外",
        ],
    ),
    ("vitamin_a", ["ビタミンa中毒", "ビタミンa過剰", "vitamin a tox", "hypervitaminosis a", "レチノール過剰"]),
    # plants / mycotoxins / specialty
    ("sago_cycad", ["ソテツ", "サゴ", "サイカシン", "cycad", "sago", "cycas"]),
    ("avocado", ["アボカド", "avocado", "persin", "ペルシン"]),
    ("cyanobacteria", ["藍藻", "アオコ", "シアノバクテリア", "blue-green", "cyanobacter", "microcystin", "anatoxin"]),
    (
        "aflatoxin",
        [
            "アフラトキシン",
            "マイコトキシン",
            "カビ毒",
            "フモニシン",
            "スタキボトリス",
            "aflatoxin",
            "mycotoxin",
            "fumonisin",
            "stachybotrys",
        ],
    ),
    ("essential_oil", ["エッセンシャルオイル", "精油", "ティーツリー", "essential oil", "tea tree", "メラルーカ"]),
    ("ptfe", ["ptfe", "テフロン", "ポリテトラフルオロエチレン", "teflon", "polytetrafluoro"]),
    ("cyanide", ["シアン化物", "青酸", "cyanide", "青酸配糖体", "シアン中毒"]),
    (
        "cardiac_glycoside",
        [
            "キョウチクトウ",
            "強心配糖体",
            "ジギタリス",
            "スズラン",
            "フクジュソウ",
            "oleander",
            "cardiac glycoside",
            "foxglove",
            "digitalis",
        ],
    ),
    ("yew", ["イチイ", "キャラボク", "yew", "taxus", "taxine", "タキシン"]),
    ("red_maple", ["レッドメープル", "アカカエデ", "red maple", "メープル中毒"]),
    ("oak_acorn", ["ドングリ", "どんぐり", "オーク", "ナラ中毒", "acorn", "oak", "tannin"]),
    ("fescue_ergot", ["フェスク", "麦角", "エンドファイト", "fescue", "ergot", "claviceps", "endophyte"]),
    ("bracken", ["ワラビ", "わらび", "bracken", "pteridium"]),
    ("selenium", ["セレン", "selenium", "アルカリ病"]),
    ("ionophore", ["モネンシン", "イオノフォア", "ラサロシド", "サリノマイシン", "monensin", "ionophore", "lasalocid"]),
    ("arsenic", ["ヒ素", "砒素", "arsenic"]),
    ("mercury", ["水銀", "mercury"]),
    (
        "aminoglycoside",
        ["アミノグリコシド", "ゲンタマイシン", "アミカシン", "aminoglycoside", "gentamicin", "amikacin"],
    ),
    ("black_locust", ["ニセアカシア", "ハリエンジュ", "black locust", "robinia"]),
    ("pokeweed", ["ヨウシュヤマゴボウ", "ヤマゴボウ", "pokeweed", "phytolacca"]),
    ("locoweed", ["ロコ草", "ロコイズム", "locoweed", "locoism", "swainsonine", "スウェインソニン"]),
    ("phalaris", ["ファラリス", "カナリークサヨシ", "phalaris", "canary grass"]),
    ("horse_chestnut", ["トチノキ", "セイヨウトチノキ", "horse chestnut", "aesculus", "buckeye"]),
    ("clover", ["クローバー", "スイートクローバー", "アルサイク", "clover", "trifolium", "melilotus"]),
    ("hoary_alyssum", ["ホーリーアリッサム", "hoary alyssum", "berteroa"]),
    ("cedar", ["杉チップ", "シダーチップ", "杉材", "シダー材", "cedar chip", "cedar shaving", "softwood bedding"]),
    ("hemlock", ["ドクニンジン", "ドクゼリ", "hemlock", "conium", "cicuta", "シクトキシン"]),
    ("pyrrolizidine", ["ピロリジジン", "サワギク", "ラグワート", "pyrrolizidine", "ragwort", "senecio"]),
    ("castor_ricin", ["トウゴマ", "ヒマ中毒", "リシン", "ヒマシ", "castor", "ricin"]),
    ("black_walnut", ["ブラックウォールナット", "クロクルミ", "black walnut", "黒クルミ"]),
    ("cantharidin", ["ツチハンミョウ", "カンタリジン", "cantharidin", "blister beetle"]),
    ("smoke_inhalation", ["煙吸入", "煙・ガス", "ガス吸入", "smoke inhalation", "一酸化炭素", "carbon monoxide"]),
    # ammonia: aquatic/amphibian water-quality toxicosis only.  Chlorine /
    # chloramine has a different mechanism and is deliberately NOT mapped here.
    ("ammonia", ["アンモニア中毒", "ammonia", "ブラウンブラッド", "brown blood"]),
    # generic buckets — placed LAST so specific agents win
    ("plant_generic", ["植物中毒", "有毒植物", "plant tox", "plant poison", "toxic plant"]),
    ("pesticide_generic", ["農薬", "殺虫剤", "除草剤", "pesticide", "insecticide", "herbicide"]),
]

# Disease names that contain a toxin keyword but are NOT a chemical toxicosis
# we should rewrite (e.g. salmon poisoning disease is an infection; "中毒症"
# alone is too vague).  Resolving these to None leaves them untouched.
_NOT_TOXICOSIS: tuple[str, ...] = (
    "サケ中毒症",  # salmon poisoning disease — Neorickettsia, infectious
    "ボツリヌス",  # botulism — bacterial toxin, handled as infection elsewhere
    "破傷風",  # tetanus
)


def _all_agent_keys() -> set[str]:
    return set(AGENTS) | set(GENERIC_AGENTS)


def resolve_toxic_agent(name_ja: str, name_en: str) -> Optional[str]:
    """Map a disease name to a canonical toxic-agent key, or None.

    Returns None when the name is not a genuine, well-characterised toxicosis
    that we have curated content for, so the caller leaves the text alone
    rather than risk applying the wrong mechanism.
    """
    name = f"{name_ja or ''} {name_en or ''}".lower()
    if any(bad.lower() in name for bad in _NOT_TOXICOSIS):
        return None
    for key, keywords in _AGENT_KEYWORDS:
        if any(kw.lower() in name for kw in keywords):
            return key
    return None


def agent_content(agent: str) -> Optional[dict[str, str]]:
    """Return the curated field bodies for a canonical agent key."""
    if agent in AGENTS:
        return AGENTS[agent]
    if agent in GENERIC_AGENTS:
        return GENERIC_AGENTS[agent]
    return None
