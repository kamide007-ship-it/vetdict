"""Drug batch 65 – referenced-but-absent agents surfaced by the 2026-09 audit (32nd sweep).

A dose-context katakana/English token sweep against the live text matcher
confirmed the index remains near-saturated. The three true monograph gaps
were all product-class agents the formulary's own disease content names
hundreds of times:

  - Sodium hypochlorite (diluted household bleach) — the single largest
    unresolved reference in the corpus (1,200+ mentions: 「次亜塩素酸1:32」
    cage disinfection for parvo/FeLV/calici, 「漂白剤1:32」 in rabbit rotavirus
    barrier nursing, 1:10 for dermatophyte spores). Chlorhexidine and
    povidone-iodine were listed but the environmental disinfectant the site
    itself prescribes was absent. The monograph documents the class-defining
    facts: dilution table, 10-min contact time, inactivation by organic
    matter, the never-mix-with-ammonia rule, and the pathogens it does NOT
    kill (Tyzzer spores, coccidia/Cryptosporidium oocysts).

  - Feliway (synthetic feline F3 facial pheromone) — the flagship FIC/FLUTD
    entries prescribe it by name as part of the MEMO multimodal environmental
    modification protocol (53 references) yet no monograph existed. Evidence
    is presented honestly: modest/mixed in systematic review (Frank 2010
    JAVMA), strongest for urine spraying (Mills & Mills 2001) and as an
    adjunct within MEMO (Buffington 2006).

  - Adaptil (dog appeasing pheromone, DAP) — 42 references across the canine
    behavioural entries (noise phobia, separation anxiety, CDS). Same honest
    evidence framing (Mills 2006 firework study; Frank 2010 review).

References:
  - Greene CE, Infectious Diseases of the Dog and Cat 4th ed — environmental
    disinfection tables (parvovirus 1:32 bleach, contact time, organic-matter
    inactivation; agents resistant to hypochlorite).
  - Moriello KA et al., Vet Dermatol 2017 (dermatophytosis consensus) —
    1:10-1:32 bleach for environmental M. canis spore decontamination.
  - Mills DS & Mills CB, Vet Rec 2001 — F3 fraction and feline urine spraying.
  - Gunn-Moore DA & Cameron ME, JFMS 2004 — Feliway pilot in feline idiopathic
    cystitis.
  - Buffington CAT et al., JFMS 2006 — MEMO for indoor cats with FIC.
  - Mills DS et al., Appl Anim Behav Sci 2006 — DAP and firework fears.
  - Frank D et al., JAVMA 2010 — systematic review of veterinary pheromone
    efficacy (honest limitation framing for both products).
"""

DRUGS_BATCH_65 = [
    {
        "id": "sodium_hypochlorite",
        "search_aliases": [
            "次亜塩素酸",
            "次亜塩素酸ナトリウム",
            "sodium hypochlorite",
            "ハイポクロライト",
        ],
        "name": "Sodium Hypochlorite (Diluted Bleach)",
        "name_ja": "次亜塩素酸ナトリウム（希釈漂白剤）",
        "category": "antiseptics",
        "mechanism": "Broad-spectrum oxidising disinfectant. Hypochlorous acid oxidises microbial proteins, lipids and nucleic acids, giving rapid activity against enveloped AND most non-enveloped viruses (including parvovirus and calicivirus, which survive many other disinfectants), bacteria and dermatophyte spores. It is an ENVIRONMENTAL disinfectant, not a skin antiseptic — activity is destroyed by organic matter, so surfaces must be cleaned of faeces/blood/bedding first.",
        "mechanism_ja": "広域酸化系消毒薬。次亜塩素酸が微生物の蛋白・脂質・核酸を酸化し、エンベロープウイルスに加えて多くのノンエンベロープウイルス（他の消毒薬に抵抗するパルボウイルス・カリシウイルスを含む）・細菌・皮膚糸状菌の分節分生子に迅速に作用する。皮膚用ではなく環境用の消毒薬であり、有機物（糞便・血液・敷料）で失活するため、消毒の前に必ず清掃を行う。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Environmental disinfection (kennels, floors, bowls, non-porous surfaces): 1:32 dilution of 5-6% household bleach (≈0.16%) with ≥10 min contact time — the standard for canine parvovirus, distemper and kennel-cough agents (Greene 4th ed). Dermatophyte (ringworm) environments: 1:10-1:32 with mechanical cleaning ×2 passes (Moriello 2017 consensus). Clean organic matter off FIRST, apply, keep wet 10 min, rinse and dry before the dog returns.",
                "dosage_ja": "環境消毒（ケージ・床・食器・非多孔質面）: 家庭用漂白剤（5-6%）を1:32希釈（約0.16%）し接触時間10分以上 — 犬パルボウイルス・ジステンパー・ケンネルコフ病原体の標準（Greene 4th ed）。皮膚糸状菌（リングワーム）環境: 1:10〜1:32希釈＋機械的清掃を2回（Moriello 2017 コンセンサス）。先に有機物を除去→塗布→10分間湿潤維持→すすいで乾燥させてから犬を戻す。",
                "notes": "Not a wound/skin antiseptic at these concentrations — use chlorhexidine 0.05% or povidone-iodine 0.1-1% on tissue instead. Solutions lose potency: dilute fresh daily and store away from light.",
                "notes_ja": "この濃度は創傷・皮膚用ではない — 組織にはクロルヘキシジン0.05%やポビドンヨード0.1-1%を用いる。希釈液は失活が早いため毎日新しく調製し、遮光保存する。",
            },
            "cat": {
                "safe": True,
                "dosage": "1:32 dilution, ≥10 min contact for feline panleukopenia (parvovirus), calicivirus and FeLV cage disinfection — bleach is one of the few agents reliably effective against unenveloped panleukopenia/calicivirus (quaternary ammoniums are unreliable). Ringworm (M. canis) environment: 1:10-1:32 after mechanical removal of hair (Moriello 2017).",
                "dosage_ja": "1:32希釈・接触10分以上 — 猫汎白血球減少症（パルボ）・カリシウイルス・FeLVのケージ消毒。ノンエンベロープの汎白血球減少症ウイルス・カリシウイルスに確実に有効な数少ない消毒薬（第四級アンモニウムは信頼性が低い）。皮膚糸状菌（M. canis）環境: 被毛の機械的除去後に1:10〜1:32（Moriello 2017）。",
                "notes": "Rinse food/water bowls and litter boxes thoroughly — cats groom residues off paws. Ventilate; remove cats from the room during application.",
                "notes_ja": "食器・トイレは十分にすすぐ — 猫は足裏の残留物をグルーミングで摂取する。換気し、散布中は猫を部屋から出す。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1:32 dilution ≥10 min for RHDV, rotavirus and general cage disinfection (the formulary's own rabbit enteritis entries: 「漂白剤1:32で消毒」). RHDV is highly environment-stable — combine with disposal of porous items.",
                "dosage_ja": "RHDV・ロタウイルス・一般ケージ消毒に1:32希釈・10分以上（本辞書のウサギ腸炎エントリ「漂白剤1:32で消毒」参照）。RHDVは環境中で極めて安定 — 多孔質物品の廃棄と併用する。",
                "notes": "NOT reliable against Clostridium piliforme (Tyzzer's disease) spores — the formulary's own Tyzzer entry notes spores resist hypochlorite; use prolonged contact with 0.3% peracetic acid or discard/incinerate bedding instead.",
                "notes_ja": "ティザー病（Clostridium piliforme）の芽胞には信頼できない — 本辞書のティザー病エントリの通り芽胞は次亜塩素酸に抵抗する。過酢酸0.3%の長時間接触、または敷料の廃棄・焼却で対応する。",
            },
            "bird": {
                "safe": True,
                "dosage": "1:32 dilution for cage/aviary surface disinfection (psittacosis, polyomavirus, circovirus environments) with ≥10 min contact, then rinse thoroughly and DRY before birds return.",
                "dosage_ja": "ケージ・禽舎表面の消毒（オウム病・ポリオーマ・サーコウイルス環境）に1:32希釈・接触10分以上。その後十分にすすぎ、完全に乾燥させてから鳥を戻す。",
                "notes": "Birds are exquisitely sensitive to aerosolised chlorine fumes — always remove birds from the room, ventilate well, and never fog or spray near them.",
                "notes_ja": "鳥は塩素ガスの吸入に極めて敏感 — 散布時は必ず鳥を部屋から出し、十分に換気し、鳥の近くでの噴霧は絶対に行わない。",
            },
            "reptile": {
                "safe": True,
                "dosage": "1:32 dilution for vivarium hard surfaces and equipment (Salmonella, ranavirus, mite-environment control); rinse thoroughly and dry before reintroducing the animal.",
                "dosage_ja": "ビバリウムの硬質面・器具の消毒（サルモネラ・ラナウイルス・ダニ環境対策）に1:32希釈。十分にすすいで乾燥させてから個体を戻す。",
                "notes": "NOT effective against coccidia or Cryptosporidium oocysts (a major reptile pathogen) — oocysts resist bleach; use >5% ammonia solution, steam, or discard contaminated furnishings.",
                "notes_ja": "コクシジウム・クリプトスポリジウム（爬虫類の重要病原体）のオーシストには無効 — オーシストは漂白剤に抵抗する。5%超アンモニア水・スチーム・汚染物品の廃棄で対応する。",
            },
            "fish": {
                "safe": False,
                "dosage": "Equipment/tank disinfection ONLY (200 ppm, empty systems). Never add to water containing fish — chlorine destroys gill epithelium at a fraction of disinfectant concentrations.",
                "dosage_ja": "器具・空水槽の消毒のみ（200 ppm、魚のいない状態）。魚のいる水への添加は絶対不可 — 塩素は消毒濃度の数十分の一でも鰓上皮を破壊する。",
                "notes": "After disinfection, rinse and fully dechlorinate (sodium thiosulfate) before restocking; verify zero residual chlorine.",
                "notes_ja": "消毒後はすすぎ、チオ硫酸ナトリウムで完全に脱塩素してから再導入する。残留塩素ゼロを確認すること。",
            },
        },
        "contraindications": "Never apply undiluted or at disinfectant strength to skin, wounds or mucous membranes (corrosive). Never mix with ammonia, acids or other cleaners — chlorine gas release is potentially lethal to staff and animals. Inactivated by organic matter (clean first, then disinfect). Do NOT rely on it for Clostridium piliforme (Tyzzer) spores or coccidia/Cryptosporidium oocysts. Ingestion of concentrated bleach is a caustic emergency: do NOT induce emesis — dilute with milk/water and treat as oesophageal burn.",
        "contraindications_ja": "原液・消毒濃度のまま皮膚・創傷・粘膜に使用しない（腐食性）。アンモニア・酸・他の洗浄剤と絶対に混合しない — 発生する塩素ガスはスタッフ・動物に致死的となりうる。有機物で失活する（先に清掃、その後消毒）。ティザー病（Clostridium piliforme）芽胞・コクシジウム/クリプトスポリジウムのオーシストには頼らない。濃厚漂白剤の誤飲は腐食性救急: 催吐禁忌 — 牛乳/水で希釈し食道熱傷として治療する。",
        "side_effects": "Respiratory irritation from fumes (birds and small mammals most sensitive), dermal/ocular irritation on contact, corrosion of metals with repeated use.",
        "side_effects_ja": "ガスによる気道刺激（鳥・小型哺乳類が最も敏感）、接触による皮膚・眼刺激、反復使用による金属腐食。",
        "drug_interactions": [
            {
                "drug": "Ammonia / ammonium-based cleaners",
                "effect": "Chloramine/chlorine gas release — potentially lethal; never combine or use sequentially without rinsing",
                "effect_ja": "クロラミン・塩素ガスが発生し致死的となりうる — 併用・すすぎなしの連続使用は絶対不可",
                "severity": "major",
            },
            {
                "drug": "Chlorhexidine",
                "effect": "Chemical incompatibility — rinse surfaces between agents; combining inactivates both and can form irritant residues",
                "effect_ja": "化学的配合禁忌 — 切り替え時は表面をすすぐ。混合は両剤を失活させ刺激性残渣を生じうる",
                "severity": "moderate",
            },
        ],
        "references": [
            "Greene CE, Infectious Diseases of the Dog and Cat 4th ed (environmental disinfection tables)",
            "Moriello KA et al., Vet Dermatol 2017 — dermatophytosis clinical consensus guidelines",
        ],
    },
    {
        "id": "feliway_f3",
        "search_aliases": [
            "フェリウェイ",
            "feliway",
            "F3フェロモン",
            "フェイシャルフェロモン",
        ],
        "name": "Feline Facial Pheromone F3 (Feliway)",
        "name_ja": "猫顔面フェロモンF3製剤（フェリウェイ）",
        "category": "behavioral",
        "mechanism": "Synthetic analogue of the F3 fraction of feline facial pheromone — the mark cats deposit by cheek-rubbing on 'safe' objects. Environmental diffusion is thought to signal familiarity/security and reduce arousal-driven behaviours (urine marking, stress-associated lower urinary signs). It modifies the cat's perception of the environment; it is not sedating and has no systemic pharmacology.",
        "mechanism_ja": "猫が頬こすりで「安全」な対象に付けるフェイシャルフェロモンF3分画の合成アナログ。環境中への拡散が親密・安心のシグナルとなり、覚醒亢進に由来する行動（尿マーキング、ストレス関連下部尿路徴候）を減らすと考えられる。環境の知覚を変える製剤であり、鎮静作用や全身薬理作用はない。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "Diffuser: 1 unit per ~50-70 m² room where the cat spends most time, run CONTINUOUSLY (not intermittently); replace vial ~monthly and the diffuser unit ~6-monthly. Spray: 1 spray on carrier/bedding corners 15 min before use (allow alcohol carrier to evaporate); reapply q4-5h. Indications with published support: urine spraying (Mills & Mills 2001), adjunct within MEMO multimodal environmental modification for idiopathic cystitis/FLUTD (Gunn-Moore & Cameron 2004 JFMS pilot; Buffington 2006), transport/hospitalisation stress. Multi-cat conflict uses the cat-appeasing-pheromone product (Feliway Friends/Multicat), not classic F3.",
                "dosage_ja": "ディフューザー: 猫が最も長く過ごす部屋（約50-70 m²）に1台を連続稼働（間欠使用は不可）。リフィルは約1ヶ月、本体は約6ヶ月で交換。スプレー: 使用15分前にキャリー・寝具の角に1プッシュ（アルコール基剤の揮発を待つ）、効果は4-5時間で再適用。エビデンスのある適応: 尿スプレー（Mills & Mills 2001）、特発性膀胱炎/FLUTDのMEMO多面的環境修正の補助（Gunn-Moore & Cameron 2004 JFMS パイロット; Buffington 2006）、移動・入院ストレス。多頭飼育の猫間対立には古典的F3ではなく猫用アピージングフェロモン製剤（フェリウェイ マルチキャット）を用いる。",
                "notes": "Evidence is modest and mixed in systematic review (Frank 2010 JAVMA) — position it as an ADJUNCT to litter box optimisation, resource multiplication and play (MEMO), never as sole therapy for FIC or marking. Never spray directly at a cat; never spray inside a carrier immediately before loading (alcohol odour is aversive until evaporated).",
                "notes_ja": "エビデンスはシステマティックレビューでは限定的・混在（Frank 2010 JAVMA）— トイレ最適化・資源の複数化・遊び（MEMO）の補助と位置づけ、FICやマーキングの単独治療にしない。猫に直接噴霧しない。キャリー内への噴霧直後の収容は不可（揮発前のアルコール臭は忌避的）。",
            },
        },
        "contraindications": "None systemic (no absorption). Species-specific signal — no effect in dogs or other species. Do not rely on it to replace analgesia, environmental modification or treatment of medical causes (a marking/periuria workup must still exclude FLUTD, pain and litter aversion).",
        "contraindications_ja": "全身性の禁忌なし（吸収されない）。種特異的シグナルのため犬・他種には無効。鎮痛・環境修正・医学的原因の治療の代替にしない（マーキング/不適切排尿では FLUTD・疼痛・トイレ嫌悪の除外が先）。",
        "side_effects": "None reported at recommended use; diffuser plug-in should be kept clear of curtains/furniture per fire-safety labelling.",
        "side_effects_ja": "推奨使用での副作用報告なし。ディフューザーは防火表示に従いカーテン・家具から離して設置する。",
        "drug_interactions": [],
        "references": [
            "Mills DS & Mills CB, Vet Rec 2001 — F3 and urine spraying",
            "Gunn-Moore DA & Cameron ME, JFMS 2004 — Feliway in feline idiopathic cystitis",
            "Buffington CAT et al., JFMS 2006 — MEMO in indoor cats",
            "Frank D et al., JAVMA 2010 — systematic review of pheromone efficacy",
        ],
    },
    {
        "id": "adaptil_dap",
        "search_aliases": [
            "アダプティル",
            "adaptil",
            "DAPフェロモン",
            "犬用フェロモン",
        ],
        "name": "Dog Appeasing Pheromone (Adaptil / DAP)",
        "name_ja": "犬アピージングフェロモン（アダプティル/DAP）",
        "category": "behavioral",
        "mechanism": "Synthetic analogue of the appeasing pheromone secreted by the intermammary sebaceous glands of lactating bitches, which signals safety to puppies. In adults it is thought to reduce fear/arousal responses to stressors (noise, novelty, separation). Environmental/collar delivery; no systemic pharmacology and no sedation.",
        "mechanism_ja": "泌乳中の母犬の乳腺間皮脂腺から分泌され、子犬に安全を伝えるアピージング（安心）フェロモンの合成アナログ。成犬でもストレッサー（騒音・新奇環境・分離）への恐怖・覚醒反応を減らすと考えられる。環境拡散またはカラーで投与し、全身薬理作用・鎮静作用はない。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Collar: fitted snugly (body heat drives release), replace ~monthly — best evidence for ongoing/unpredictable stressors (thunderstorm season: Landsberg 2015). Diffuser: 1 per ~50-70 m², run continuously, start 24-48 h BEFORE a predicted stressor (fireworks: Mills 2006; adaptation of newly adopted puppies: Gaultier 2005). Spray: on bandana/bedding/car 15 min before exposure, lasts ~4-5 h. Indications in the formulary's own entries: noise phobia, storm anxiety, separation anxiety and CDS night-time restlessness — always combined with behaviour modification (desensitisation/counter-conditioning) ± anxiolytics for severe cases.",
                "dosage_ja": "カラー: 体温で揮発するため皮膚に密着装着し約1ヶ月で交換 — 持続的・予測不能なストレッサーに最もエビデンスがある（雷雨シーズン: Landsberg 2015）。ディフューザー: 約50-70 m²に1台を連続稼働し、予測されるストレッサー（花火: Mills 2006、新規導入子犬の順応: Gaultier 2005）の24-48時間前から開始。スプレー: 暴露15分前にバンダナ・寝具・車内へ（効果約4-5時間）。本辞書の適応: 音響恐怖症・雷雨不安・分離不安・CDSの夜間不穏 — 常に行動修正（系統的脱感作・拮抗条件づけ）と併用し、重症例は抗不安薬を追加する。",
                "notes": "Evidence is modest in systematic review (Frank 2010 JAVMA) — an adjunct, never sole therapy for severe noise phobia or separation anxiety (those need behaviour modification ± medication). Odourless to humans. Do not expect effect in cats or other species (species-specific signal).",
                "notes_ja": "エビデンスはシステマティックレビューでは限定的（Frank 2010 JAVMA）— 補助療法であり、重度の音響恐怖症・分離不安の単独治療にしない（行動修正±薬物療法が必要）。ヒトには無臭。種特異的シグナルのため猫・他種への効果は期待しない。",
            },
        },
        "contraindications": "None systemic. Not a restraint or sedation substitute — a panicking dog still needs anxiolytic medication and management. Check collar fit weekly in growing puppies (embedding risk as with any collar).",
        "contraindications_ja": "全身性の禁忌なし。保定・鎮静の代替ではない — パニック状態の犬には抗不安薬と管理が依然必要。成長期の子犬はカラーの締まり具合を週1回確認する（食い込みリスクは通常のカラーと同様）。",
        "side_effects": "None reported at recommended use.",
        "side_effects_ja": "推奨使用での副作用報告なし。",
        "drug_interactions": [],
        "references": [
            "Mills DS et al., Appl Anim Behav Sci 2006 — DAP and firework fears",
            "Gaultier E et al., Vet Rec 2005 — DAP in newly adopted puppies",
            "Landsberg GM et al., 2015 — DAP collar and thunderstorm response",
            "Frank D et al., JAVMA 2010 — systematic review of pheromone efficacy",
        ],
    },
]
