#!/usr/bin/env python3
"""Update bird behavioral disease treatments - batch 1 (10 entries)."""

import json

with open("diseases_all_species.json", "r") as f:
    data = json.load(f)

UPDATES = {
    "bird_0028": {  # Feather Destructive Behavior
        "treatment_ja": (
            "【診断的精査】医学的原因の除外が最優先: 皮膚掻爬検査（ダニ・真菌）、糞便検査、"
            "CBC/生化学、PBFD PCR、ABV（鳥ボルナウイルス）PCR、クラミジア検査。"
            "甲状腺機能検査（特にセキセイインコ）。皮膚生検（慢性例）。"
            "【環境エンリッチメント（最重要）】フォレイジング（採餌行動）の機会: フォレイジングトイ、"
            "紙に包んだおやつ、松ぼっくりにシードを詰める、段ボール箱の中に隠す。"
            "知育玩具のローテーション（2-3日毎に交換）。"
            "自然の枝（安全な樹種: ユーカリ、リンゴ、柳）を提供。"
            "水浴びの機会（霧吹き、浅い水皿、シャワー同伴）を毎日提供。"
            "日照管理: 12時間明/12時間暗の規則的サイクル。フルスペクトルUVBライト設置。"
            "【栄養管理】種子食からペレット食への転換（Harrison's, Zupreem, Roudybush等）。"
            "新鮮な野菜・果物の毎日提供。ビタミンA補充（欠乏が毛引きの一因になりうる）。"
            "omega-3脂肪酸サプリメント（亜麻仁油）。"
            "【社会的交流】1日最低2-3時間の飼い主との直接的交流。"
            "テレビ/ラジオは社会的交流の代替にはならない。"
            "トレーニングセッション（ターゲットトレーニング、トリック）で知的刺激を提供。"
            "【薬物療法（行動性が確認された場合）】ハロペリドール 0.1-0.2 mg/kg PO q12h"
            "（ブチロフェノン系、最もエビデンスが多い）。"
            "フルオキセチン 1-2 mg/kg PO q24h（SSRI）。"
            "クロミプラミン 1-3 mg/kg PO q12h（TCA、代替）。"
            "ナルトレキソン 1.5 mg/kg PO q12h（オピオイド拮抗薬、自傷の報酬系遮断）。"
            "ジアゼパム 0.5-1.0 mg/kg PO/IM PRN（急性不安時のみ、常用は依存リスク）。"
            "薬物療法は行動修正と併用。単独使用は推奨しない。効果判定に最低6-8週間。"
            "【エリザベスカラー】最終手段としてのみ使用。長期使用はストレス増加・二次的行動問題を引き起こす。"
            "使用する場合は必ず飲食・羽繕いが可能なサイズを選択。"
            "【参考文献】van Zeeland YRA et al. (2009) Feather damaging behaviour in parrots. Vet J; "
            "Jayson SL et al. (2014) Positive reinforcement training and feather-damaging behaviour. Zoo Biol; "
            "Seibert LM (2006) Feather-picking disorder in pet birds. In: Manual of Parrot Behavior."
        ),
        "treatment": (
            "[Diagnostic Workup] Ruling out medical causes is top priority: skin scraping (mites/fungal), "
            "fecal examination, CBC/chemistry, PBFD PCR, ABV (avian bornavirus) PCR, Chlamydia testing. "
            "Thyroid function (especially budgerigars). Skin biopsy (chronic cases). "
            "[Environmental Enrichment (Most Important)] Foraging opportunities: foraging toys, "
            "treats wrapped in paper, pine cones stuffed with seeds, hidden in cardboard boxes. "
            "Rotate puzzle toys every 2-3 days. "
            "Natural branches (safe species: eucalyptus, apple, willow). "
            "Daily bathing opportunities (misting, shallow water dish, shower). "
            "Light management: regular 12h light/12h dark cycle. Full-spectrum UVB lighting. "
            "[Nutritional Management] Convert from seed to pellet diet (Harrison's, Zupreem, Roudybush). "
            "Daily fresh vegetables/fruits. Vitamin A supplementation (deficiency can contribute). "
            "Omega-3 fatty acid supplement (flaxseed oil). "
            "[Social Interaction] Minimum 2-3 hours daily direct owner interaction. "
            "TV/radio is not a substitute for social interaction. "
            "Training sessions (target training, tricks) for mental stimulation. "
            "[Pharmacotherapy (confirmed behavioral)] Haloperidol 0.1-0.2 mg/kg PO q12h "
            "(butyrophenone, most evidence). "
            "Fluoxetine 1-2 mg/kg PO q24h (SSRI). "
            "Clomipramine 1-3 mg/kg PO q12h (TCA, alternative). "
            "Naltrexone 1.5 mg/kg PO q12h (opioid antagonist, blocks self-harm reward). "
            "Diazepam 0.5-1.0 mg/kg PO/IM PRN (acute anxiety only, dependency risk with chronic use). "
            "Combine with behavior modification; not standalone. Allow 6-8 weeks for assessment. "
            "[Elizabethan Collar] Last resort only. Long-term use increases stress and secondary behavioral issues. "
            "Ensure size allows eating, drinking, and preening. "
            "[References] van Zeeland YRA et al. (2009) Vet J; "
            "Jayson SL et al. (2014) Zoo Biol; Seibert LM (2006) Manual of Parrot Behavior."
        ),
    },
    "bird_0029": {  # Mate Aggression
        "treatment_ja": (
            "【緊急対応】攻撃を受けた鳥の即時分離と外傷評価。"
            "止血（出血部位にコーンスターチまたは止血パウダー）。"
            "重度の外傷: 創傷洗浄（温生理食塩水）+ 抗菌軟膏。深部損傷は縫合。"
            "鎮痛: メロキシカム 0.5-1.0 mg/kg PO q24h。感染予防: エンロフロキサシン 15 mg/kg PO q12h。"
            "【ホルモン管理】日照時間を10-12時間に制限（繁殖刺激の低減）。"
            "巣箱・巣材の完全除去。暗い隠れ場所（巣に見立てる場所）の排除。"
            "高脂肪・高カロリー食を避ける（繁殖刺激になる）。"
            "難治例: リュープロレリン（GnRHアゴニスト）100-800 μg/kg IM q2-4週"
            "（ホルモン性攻撃の一時的抑制）。"
            "【再導入プロトコル】最低2-4週間の分離期間。"
            "広いケージ（逃げ場のある十分なスペース）。"
            "視覚的遮蔽物（枝、おもちゃ）を複数設置。"
            "食器・水飲みを複数設置（資源独占を防ぐ）。"
            "監視下での短時間の接触から開始→段階的に延長。"
            "攻撃の兆候（追いかけ、嘴の威嚇、体の膨張）があれば即座に分離。"
            "【相性不良の場合】繰り返し攻撃するペアは永久分離を検討。"
            "無理にペアリングを継続しない（致死的外傷のリスク）。"
            "【参考文献】Speer BL (2016) Current Therapy in Avian Medicine and Surgery. Elsevier; "
            "Chitty J & Lierz M (2008) BSAVA Manual of Raptors, Pigeons and Passerine Birds."
        ),
        "treatment": (
            "[Emergency Response] Immediate separation and injury assessment of attacked bird. "
            "Hemostasis (cornstarch or styptic powder on bleeding sites). "
            "Severe injuries: wound lavage (warm saline) + antimicrobial ointment. Suture deep lacerations. "
            "Analgesia: meloxicam 0.5-1.0 mg/kg PO q24h. Infection prevention: enrofloxacin 15 mg/kg PO q12h. "
            "[Hormonal Management] Restrict photoperiod to 10-12 hours (reduce breeding stimulus). "
            "Complete removal of nest boxes and nesting materials. Eliminate dark hiding spots (perceived as nests). "
            "Avoid high-fat/high-calorie diets (breeding stimulus). "
            "Refractory: leuprolide (GnRH agonist) 100-800 μg/kg IM q2-4 weeks (temporary hormonal suppression). "
            "[Reintroduction Protocol] Minimum 2-4 weeks separation. "
            "Large cage with adequate escape space. Multiple visual barriers (branches, toys). "
            "Multiple food/water stations (prevent resource monopolization). "
            "Start with short supervised contact → gradually extend. "
            "Immediate separation if aggression signs (chasing, beak threats, body puffing). "
            "[Incompatible Pairs] Consider permanent separation for repeatedly aggressive pairs. "
            "Do not force continued pairing (risk of lethal injury). "
            "[References] Speer BL (2016) Current Therapy in Avian Medicine and Surgery; "
            "Chitty J & Lierz M (2008) BSAVA Manual."
        ),
    },
    "bird_0030": {  # Territorial Aggression
        "treatment_ja": (
            "【行動修正（第一選択）】ケージ外での交流時間を増加（ケージへの執着軽減）。"
            "ステップアップ訓練の再強化: 毎日5-10分のセッション、おやつで正の強化。"
            "咬む行動に対して: 叫ばない・叩かない（注目が報酬になる）→静かに手を引いて無視。"
            "ターゲットトレーニング: 棒の先端に触れる→おやつ、で攻撃以外の行動を強化。"
            "T字パーチ使用: ケージ内に手を入れずにステップアップ可能。"
            "【環境管理】日照時間を10-12時間に制限。"
            "ケージレイアウトを定期的に変更（縄張り意識のリセット）。"
            "ケージの位置変更（縄張りの固定化防止）。"
            "巣箱・巣材の除去。暗い囲われた空間の排除。"
            "ケージ上部のパーチを除去（高い位置=支配的→低い位置に移動）。"
            "【ホルモン性攻撃の管理】繁殖期の春〜夏に悪化することが多い。"
            "高脂肪食・甘い食べ物の制限。"
            "背中・翼下の撫でを避ける（性的刺激になる）→頭部・頸部のみ。"
            "難治例: リュープロレリン 100-800 μg/kg IM q2-4週。"
            "【薬物療法】フルオキセチン 1-2 mg/kg PO q24h（慢性的攻撃性に、最低6-8週間試行）。"
            "ハロペリドール 0.1-0.2 mg/kg PO q12h（重度の攻撃性に）。"
            "【参考文献】Luescher AU & Wilson L (2006) Aggressive behavior in pet birds. In: Manual of Parrot Behavior; "
            "Friedman SG (2009) What's wrong with this picture? Effectiveness is not enough. J Appl Companion Anim Behav."
        ),
        "treatment": (
            "[Behavior Modification (First-line)] Increase out-of-cage interaction time (reduce cage attachment). "
            "Reinforce step-up training: 5-10 min daily sessions with treat-based positive reinforcement. "
            "For biting: no screaming/hitting (attention becomes reward) → quietly withdraw hand and ignore. "
            "Target training: touch end of stick → treat, reinforcing non-aggressive behavior. "
            "T-perch: enables step-up without reaching into cage. "
            "[Environmental Management] Restrict photoperiod to 10-12 hours. "
            "Periodically rearrange cage layout (reset territorial perception). "
            "Relocate cage position (prevent territorial fixation). "
            "Remove nest boxes/materials. Eliminate dark enclosed spaces. "
            "Remove top perches (height = dominance → move to lower positions). "
            "[Hormonal Aggression Management] Often worsens during breeding season (spring-summer). "
            "Restrict high-fat foods and sweets. "
            "Avoid petting back/under-wings (sexual stimulation) → head/neck only. "
            "Refractory: leuprolide 100-800 μg/kg IM q2-4 weeks. "
            "[Pharmacotherapy] Fluoxetine 1-2 mg/kg PO q24h (chronic aggression, minimum 6-8 week trial). "
            "Haloperidol 0.1-0.2 mg/kg PO q12h (severe aggression). "
            "[References] Luescher AU & Wilson L (2006) Manual of Parrot Behavior; "
            "Friedman SG (2009) J Appl Companion Anim Behav."
        ),
    },
    "bird_0031": {  # Stress Bars (Feather)
        "treatment_ja": (
            "【病態】ストレスバーは羽軸を横断する透明な線（構造的弱化部位）。"
            "羽毛形成期のストレス（栄養不良、疾患、環境ストレス）を反映。"
            "ストレスバー自体は治療不要だが、原因の特定と改善が重要。"
            "【原因の特定と是正】栄養不良: 種子食中心→ペレット食への転換。"
            "ビタミンA・カルシウム・アミノ酸（特にメチオニン・リジン）の補充。"
            "感染症: PBFD、ABV、クラミジア、慢性細菌感染の検査と治療。"
            "環境ストレス: 騒音、温度変動、不規則な日照、睡眠不足の改善。"
            "社会的ストレス: 隔離、過密、ペア間の不和の解消。"
            "【栄養管理】高品質ペレット食（全食事の50-70%）。"
            "新鮮な野菜（濃緑色・オレンジ色: ビタミンA源）毎日提供。"
            "十分な蛋白質摂取（換羽期は特に重要）。"
            "カトルボーン（イカの甲）でカルシウム補充。"
            "【環境改善】12時間明/12時間暗の規則的サイクル。"
            "静かで安定した環境。適温の維持（20-28°C種による）。"
            "十分な睡眠（10-12時間の暗く静かな環境）。"
            "【モニタリング】次の換羽でストレスバーが改善するかを評価（改善指標）。"
            "【参考文献】Harcourt-Brown N & Chitty J (2005) BSAVA Manual of Psittacine Birds 2nd ed; "
            "Harrison GJ & Lightfoot TL (2006) Clinical Avian Medicine."
        ),
        "treatment": (
            "[Pathology] Stress bars are translucent lines crossing the feather shaft (structural weak points). "
            "Reflect stress during feather formation (malnutrition, disease, environmental stress). "
            "Bars themselves need no treatment; identifying and correcting the cause is key. "
            "[Identify and Correct Causes] Malnutrition: seed-based → pellet diet conversion. "
            "Supplement vitamin A, calcium, amino acids (especially methionine, lysine). "
            "Infections: test and treat PBFD, ABV, Chlamydia, chronic bacterial infections. "
            "Environmental stress: address noise, temperature fluctuations, irregular light, sleep deprivation. "
            "Social stress: resolve isolation, overcrowding, pair conflicts. "
            "[Nutritional Management] High-quality pellet diet (50-70% of total diet). "
            "Daily fresh vegetables (dark green/orange: vitamin A sources). "
            "Adequate protein intake (especially important during molt). "
            "Cuttlebone for calcium supplementation. "
            "[Environmental Improvement] Regular 12h light/12h dark cycle. "
            "Quiet, stable environment. Maintain appropriate temperature (20-28°C species-dependent). "
            "Adequate sleep (10-12 hours in dark, quiet environment). "
            "[Monitoring] Assess whether stress bars improve at next molt (indicator of improvement). "
            "[References] Harcourt-Brown N & Chitty J (2005) BSAVA Manual of Psittacine Birds 2nd ed; "
            "Harrison GJ & Lightfoot TL (2006) Clinical Avian Medicine."
        ),
    },
    "bird_0042": {  # Regurgitation Behavior
        "treatment_ja": (
            "【鑑別診断】感染性嘔吐の除外が最優先: そのう検査（カンジダ、トリコモナス、メガバクテリア）、"
            "糞便検査、CBC/生化学。腺胃拡張症（PDD/ABV）の除外。"
            "消化管異物のX線検査。重金属中毒（亜鉛・鉛）の血中濃度測定。"
            "【行動性吐き戻しの特徴】特定の対象（飼い主、おもちゃ、鏡）に向けて行う。"
            "頭を上下に振ってから吐き戻す。食欲・体重は正常。"
            "吐き戻した食物を再摂取することがある。"
            "【環境管理】吐き戻しの対象物の除去: 鏡、特定のおもちゃ、光る物体。"
            "日照時間を10-12時間に制限（ホルモン刺激の低減）。"
            "巣箱・巣材の除去。暗い隠れ場所の排除。"
            "飼い主への吐き戻しの場合: 反応せずに静かに離れる（正の強化を避ける）。"
            "背中・翼下を撫でない（性的刺激→吐き戻し誘発）。"
            "【栄養管理】高脂肪・高糖質食の制限。ペレット主体の食事。"
            "フォレイジングフィーダーで採食時間を延長（口腔行動の転位）。"
            "【ホルモン療法（重度）】リュープロレリン 100-800 μg/kg IM q2-4週（GnRHアゴニスト）。"
            "効果は一時的（2-4週間）。長期使用のリスク/ベネフィットを検討。"
            "【参考文献】Speer BL (2016) Current Therapy in Avian Medicine and Surgery; "
            "de Matos R & Morrisey JK (2005) Emergency and critical care of small psittacines and passerines. Vet Clin Exot Anim."
        ),
        "treatment": (
            "[Differential Diagnosis] Rule out infectious vomiting first: crop cytology (Candida, Trichomonas, "
            "megabacteria), fecal exam, CBC/chemistry. Rule out PDD/ABV (proventricular dilatation disease). "
            "Radiographs for GI foreign bodies. Heavy metal levels (zinc/lead). "
            "[Behavioral Regurgitation Characteristics] Directed at specific objects (owner, toy, mirror). "
            "Head bobbing before regurgitation. Normal appetite and weight. "
            "May re-ingest regurgitated food. "
            "[Environmental Management] Remove regurgitation targets: mirrors, specific toys, shiny objects. "
            "Restrict photoperiod to 10-12 hours (reduce hormonal stimulation). "
            "Remove nest boxes/materials. Eliminate dark hiding spots. "
            "If directed at owner: do not react, quietly move away (avoid positive reinforcement). "
            "Do not pet back/under-wings (sexual stimulation → triggers regurgitation). "
            "[Nutritional Management] Restrict high-fat/high-sugar diet. Pellet-based diet. "
            "Foraging feeders to extend foraging time (redirect oral behavior). "
            "[Hormonal Therapy (severe)] Leuprolide 100-800 μg/kg IM q2-4 weeks (GnRH agonist). "
            "Effect is temporary (2-4 weeks). Evaluate long-term risk/benefit. "
            "[References] Speer BL (2016) Current Therapy in Avian Medicine and Surgery; "
            "de Matos R & Morrisey JK (2005) Vet Clin Exot Anim."
        ),
    },
}

updated = 0
for entry in data:
    eid = entry.get("id", "")
    if eid in UPDATES:
        entry["treatment"] = UPDATES[eid]["treatment"]
        entry["treatment_ja"] = UPDATES[eid]["treatment_ja"]
        updated += 1
        print(f"  Updated: {eid} ({entry['name']})")

print(f"Total updated: {updated}")
with open("diseases_all_species.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
