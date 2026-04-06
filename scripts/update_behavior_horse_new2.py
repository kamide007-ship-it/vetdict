#!/usr/bin/env python3
"""Add 3 more horse behavioral entries: wood chewing, coprophagy, equine anxiety."""
import json

with open("diseases_all_species.json", "r") as f:
    data = json.load(f)

NEW_ENTRIES = [
    {
        "id": "horse_0029",
        "name": "Wood Chewing",
        "name_ja": "木かじり（ウッドチューイング）",
        "species": "Horse",
        "description": "Chewing on wooden surfaces (fences, stalls, trees) without the neck arching and air swallowing seen in crib-biting. Distinct from crib-biting.",
        "description_ja": "柵・馬房・樹木などの木材表面を噛む行動。さく癖（クリビング）とは異なり、首のアーチと空気嚥下を伴わない。",
        "pathophysiology": "Primarily a redirected foraging behavior rather than a true stereotypy. Occurs when natural foraging motivation is frustrated by insufficient fiber intake. May also be related to trace mineral deficiencies.",
        "pathophysiology_ja": "真の常同行動ではなく、主に転位採食行動。粗飼料不足による自然な採食動機の欲求不満が原因。微量ミネラル欠乏も関与しうる。",
        "causes": "Insufficient dietary fiber/forage, low roughage diet, boredom, trace mineral deficiency (copper, zinc), restricted grazing access.",
        "causes_ja": "食物繊維/粗飼料不足、低繊維食、退屈、微量ミネラル欠乏（銅、亜鉛）、放牧制限。",
        "treatment_ja": (
            "【飼養管理改善（第一選択）】粗飼料の増量が最も効果的。"
            "乾草の自由採食化またはスローフィーダー使用。"
            "放牧時間の増加。飼料中の繊維量を体重の1.5-2%/日に増加。"
            "【栄養補正】微量ミネラルの血液検査（銅、亜鉛、セレン）。"
            "不足があれば適切なミネラルサプリメントで補正。"
            "塩ブロック・ミネラルブロックの常設。"
            "【環境エンリッチメント】噛める安全な素材の提供（枝、丸太）。"
            "馬房内の干し草ネット複数設置。"
            "社会的接触と十分な運動。"
            "【物理的対策】木材表面へのホットソース/苦味剤塗布（一時的対策）。"
            "金属キャッピングやプラスチックカバーで木材保護。"
            "電気柵（動物福祉への配慮が必要）。"
            "【消化器合併症】木片の摂取による腸閉塞リスク（稀だが重篤）。"
            "歯牙摩耗。口腔内損傷。"
            "【参考文献】Redbo I et al. (1998) Factors affecting behavioural disturbances in race-horses. Anim Sci; "
            "Willard JG et al. (1977) Effect of diet on cecal pH and feeding behavior of horses. J Anim Sci."
        ),
        "treatment": (
            "[Management Improvement (First-line)] Increasing forage is most effective. "
            "Ad libitum hay access or slow feeders. Increase turnout time. "
            "Increase dietary fiber to 1.5-2% body weight/day. "
            "[Nutritional Correction] Blood test for trace minerals (copper, zinc, selenium). "
            "Supplement if deficient. Permanent salt/mineral blocks. "
            "[Environmental Enrichment] Provide safe chewable materials (branches, logs). "
            "Multiple hay nets in stall. Social contact and adequate exercise. "
            "[Physical Deterrents] Hot sauce/bitter agents on wood surfaces (temporary). "
            "Metal capping or plastic covers. Electric fencing (welfare considerations). "
            "[GI Complications] Risk of intestinal obstruction from ingested wood chips (rare but serious). "
            "Dental wear. Oral injuries. "
            "[References] Redbo I et al. (1998) Anim Sci; "
            "Willard JG et al. (1977) J Anim Sci."
        ),
        "prevention": "十分な粗飼料給与。適切なミネラル補給。放牧時間の確保。",
        "prevention_ja": "十分な粗飼料給与。適切なミネラル補給。放牧時間の確保。",
        "prognosis": "Excellent with dietary management. Usually resolves when adequate forage is provided.",
        "prognosis_ja": "食事管理で予後良好。十分な粗飼料が提供されれば通常改善。",
        "clinical_signs": "chewing wooden fences, stalls, trees; wood damage; possible dental wear; wood chips in feces",
        "clinical_signs_ja": "柵・馬房・樹木の木材を噛む、木材の損傷、歯牙摩耗の可能性、糞中に木片。",
        "diagnosis": "Behavioral observation. Distinguish from crib-biting (no neck arch/air swallowing). Nutritional assessment. Trace mineral blood panel.",
        "diagnosis_ja": "行動観察。さく癖との鑑別（首のアーチ・空気嚥下なし）。栄養評価。微量ミネラル血液検査。",
        "urgency": "low",
        "category": "misc",
        "transmission": "Not transmissible.",
        "transmission_ja": "伝播しない。",
        "recommended_tests": ["血液生化学検査 (Blood Chemistry Panel)", "微量ミネラル検査 (Trace Mineral Panel)", "歯科検査 (Dental Examination)"],
        "symptoms": ["behavioral_changes", "dental_abnormalities"],
        "differential_diagnosis": "Crib-biting (distinct: involves neck arching and air swallowing), pica, nutritional deficiency.",
        "severity_score": 1,
        "estimated_cost_level": "low",
        "hospitalization_likelihood": "low",
        "monitoring_frequency": "monthly",
        "treatment_duration_weeks": 12,
    },
    {
        "id": "horse_0030",
        "name": "Coprophagy (Foal and Adult)",
        "name_ja": "食糞症（子馬および成馬）",
        "species": "Horse",
        "description": "Ingestion of feces. Normal in foals (1-8 weeks, establishing gut microbiome) but abnormal in adults. Adult coprophagy may indicate nutritional deficiency or behavioral disorder.",
        "description_ja": "糞便の摂取。子馬では正常（生後1-8週、腸内細菌叢の確立）だが成馬では異常。成馬の食糞は栄養欠乏または行動障害を示唆。",
        "pathophysiology": "In foals: normal developmental behavior for establishing hindgut microbiome (coprophagy of dam's feces). In adults: may indicate fiber deficiency, protein deficiency, B vitamin deficiency, boredom, or chronic stress.",
        "pathophysiology_ja": "子馬: 後腸微生物叢確立のための正常な発達行動（母馬の糞を摂取）。成馬: 繊維欠乏、蛋白質欠乏、ビタミンB群欠乏、退屈、慢性ストレスを示唆。",
        "causes": "Foals: normal behavior. Adults: fiber/protein deficiency, B vitamin deficiency, boredom, social deprivation, restricted foraging.",
        "causes_ja": "子馬: 正常行動。成馬: 繊維/蛋白質欠乏、ビタミンB群欠乏、退屈、社会的隔離、採食制限。",
        "treatment_ja": (
            "【子馬の食糞】生後1-8週間は正常行動（母馬の糞から腸内細菌叢を獲得）。"
            "介入不要。8週齢以降も継続する場合は栄養評価。"
            "【成馬の食糞 — 栄養評価】飼料分析: 繊維含量、蛋白質含量、ビタミン/ミネラルプロファイル。"
            "粗飼料を体重の1.5-2%/日に増量。蛋白質摂取量の確認と補正。"
            "ビタミンB群サプリメント（酵母培養物含有飼料添加剤）。"
            "【飼養管理改善】粗飼料の自由採食化またはスローフィーダー。"
            "放牧時間の増加。環境エンリッチメント。社会的接触。"
            "【寄生虫管理】成馬の食糞は寄生虫再感染リスクを増大。"
            "定期的な糞便検査（FEC: 糞便虫卵数）と適切な駆虫プログラム。"
            "放牧地の糞便除去を徹底。"
            "【衛生管理】馬房の清潔維持（頻回な糞便除去）。"
            "放牧地のローテーション。"
            "【参考文献】Crowell-Davis SL & Houpt KA (1985) Coprophagy by foals: recognition of maternal feces. Appl Anim Behav Sci; "
            "McGreevy PD (2004) Equine Behavior: A Guide for Veterinarians and Equine Scientists."
        ),
        "treatment": (
            "[Foal Coprophagy] Normal behavior from 1-8 weeks of age (acquiring gut microbiome from dam's feces). "
            "No intervention needed. If persisting beyond 8 weeks, nutritional evaluation indicated. "
            "[Adult Coprophagy — Nutritional Assessment] Feed analysis: fiber content, protein content, vitamin/mineral profile. "
            "Increase forage to 1.5-2% body weight/day. Verify and correct protein intake. "
            "B vitamin supplementation (yeast culture-containing feed additives). "
            "[Management Improvement] Ad libitum forage or slow feeders. "
            "Increase turnout time. Environmental enrichment. Social contact. "
            "[Parasite Management] Adult coprophagy increases reinfection risk. "
            "Regular fecal egg counts (FEC) and appropriate deworming program. "
            "Thorough pasture fecal removal. "
            "[Hygiene] Maintain stall cleanliness (frequent manure removal). Pasture rotation. "
            "[References] Crowell-Davis SL & Houpt KA (1985) Appl Anim Behav Sci; "
            "McGreevy PD (2004) Equine Behavior."
        ),
        "prevention": "十分な粗飼料給与。適切な栄養バランス。放牧地の衛生管理。",
        "prevention_ja": "十分な粗飼料給与。適切な栄養バランス。放牧地の衛生管理。",
        "prognosis": "Foal: self-resolving. Adult: usually resolves with dietary correction. If behavioral, may persist but can be managed.",
        "prognosis_ja": "子馬: 自然消退。成馬: 食事補正で通常改善。行動性の場合は持続しうるが管理可能。",
        "clinical_signs": "eating feces; may be associated with poor body condition; dull coat; signs of nutritional deficiency",
        "clinical_signs_ja": "糞便の摂取。ボディコンディション低下、被毛の光沢低下、栄養欠乏徴候を伴うことあり。",
        "diagnosis": "Behavioral observation. Nutritional assessment. Fecal egg count. Blood work (protein, B vitamins, trace minerals).",
        "diagnosis_ja": "行動観察。栄養評価。糞便虫卵数。血液検査（蛋白質、ビタミンB群、微量ミネラル）。",
        "urgency": "low",
        "category": "misc",
        "transmission": "Not transmissible as a behavior. However, coprophagy facilitates parasite transmission.",
        "transmission_ja": "行動としては伝播しない。ただし食糞により寄生虫の伝播が促進される。",
        "recommended_tests": ["糞便虫卵検査 (Fecal Egg Count)", "血液生化学検査 (Blood Chemistry Panel)", "飼料分析 (Feed Analysis)"],
        "symptoms": ["behavioral_changes", "poor_body_condition", "weight_loss"],
        "differential_diagnosis": "Nutritional deficiency, pica, boredom-related behavior, GI disease.",
        "severity_score": 1,
        "estimated_cost_level": "low",
        "hospitalization_likelihood": "low",
        "monitoring_frequency": "monthly",
        "treatment_duration_weeks": 8,
    },
    {
        "id": "horse_0031",
        "name": "Equine Anxiety / Barn Sour / Buddy Sour",
        "name_ja": "馬の不安障害 / 馬房依存症 / 仲間依存症",
        "species": "Horse",
        "description": "Anxiety disorders in horses including separation anxiety from companion horses (buddy sour) or reluctance to leave the stable environment (barn sour/nappy behavior).",
        "description_ja": "仲間馬からの分離不安（バディサワー）や馬房環境から離れることへの拒否（バーンサワー/ナッピー行動）を含む馬の不安障害。",
        "pathophysiology": "Horses are obligate social species with strong affiliative bonds. Separation from bonded companions or familiar environments triggers HPA axis activation, elevated cortisol, and sympathetic nervous system arousal.",
        "pathophysiology_ja": "馬は社会性が高く強い親和的絆を形成する。絆のある仲間や慣れた環境からの分離はHPA軸の活性化、コルチゾール上昇、交感神経系の興奮を引き起こす。",
        "causes": "Inadequate socialization during development, over-bonding with single companion, lack of confidence-building training, sudden environmental changes.",
        "causes_ja": "発達期の不十分な社会化、単一の仲間への過度な執着、自信構築トレーニングの不足、急激な環境変化。",
        "treatment_ja": (
            "【バディサワー（仲間依存症）】段階的分離トレーニング: 短時間・短距離の分離から開始し徐々に延長。"
            "分離時に報酬（おやつ、粗飼料）を提供。"
            "複数の馬との社会化（単一の仲間への過度な依存を防ぐ）。"
            "分離中も視覚的・聴覚的接触を維持しつつ段階的に距離を拡大。"
            "騎乗中: 仲間から離れた時にリラックスした状態を強化（ポジティブ強化）。"
            "【バーンサワー（馬房依存症）】馬房から離れる距離を段階的に延長。"
            "馬房から離れた場所で正の経験（おやつ、放牧、リラックスした歩行）を提供。"
            "自信構築のためのグラウンドワーク（地上でのトレーニング）。"
            "トレイルライディング: 経験馬との同行から開始。"
            "【薬物療法（補助的）】トラゾドン 4 mg/kg PO（イベント60-90分前）。"
            "マグネシウム補充: 酸化マグネシウム 10-20 g/日 PO。"
            "トリプトファン 20 mg/kg PO q24h。"
            "重度: アセプロマジン 0.02-0.04 mg/kg IV/IM（輸送時等の一時的使用のみ）。"
            "注意: 薬物療法は行動修正の補助であり、単独使用は推奨しない。"
            "【環境管理】安定した群れ構成の維持。急激な仲間の変更を避ける。"
            "新しい環境への段階的な慣らし。"
            "【参考文献】Houpt KA (2011) Domestic Animal Behavior 5th ed; "
            "Hartmann E et al. (2012) Keeping horses in groups: A review. Appl Anim Behav Sci; "
            "McDonnell SM (2003) The Equid Ethogram: A Practical Field Guide to Horse Behavior."
        ),
        "treatment": (
            "[Buddy Sour (Separation Anxiety)] Gradual separation training: start with short duration/distance, "
            "progressively extend. Provide rewards (treats, forage) during separation. "
            "Socialize with multiple horses (prevent over-bonding with single companion). "
            "Maintain visual/auditory contact during separation, gradually increase distance. "
            "Under saddle: reinforce relaxed state away from companion (positive reinforcement). "
            "[Barn Sour (Stable Dependency)] Gradually extend distance from stable. "
            "Provide positive experiences away from barn (treats, grazing, relaxed walking). "
            "Groundwork for confidence building. Trail riding: start with experienced companion horse. "
            "[Pharmacotherapy (adjunctive)] Trazodone 4 mg/kg PO (60-90 min before event). "
            "Magnesium supplementation: MgO 10-20 g/day PO. "
            "Tryptophan 20 mg/kg PO q24h. "
            "Severe: acepromazine 0.02-0.04 mg/kg IV/IM (temporary use only, e.g., transport). "
            "Note: pharmacotherapy is adjunctive to behavior modification, not standalone. "
            "[Environmental Management] Maintain stable group composition. Avoid abrupt companion changes. "
            "Gradual acclimation to new environments. "
            "[References] Houpt KA (2011) Domestic Animal Behavior 5th ed; "
            "Hartmann E et al. (2012) Appl Anim Behav Sci; "
            "McDonnell SM (2003) The Equid Ethogram."
        ),
        "prevention": "子馬期からの適切な社会化。複数の馬との交流。段階的な環境変化への暴露。",
        "prevention_ja": "子馬期からの適切な社会化。複数の馬との交流。段階的な環境変化への暴露。",
        "prognosis": "Good with consistent training program. Gradual improvement over weeks to months. Young horses respond better than older horses with long-established patterns.",
        "prognosis_ja": "一貫したトレーニングプログラムで予後良好。数週間〜数ヶ月で段階的に改善。若馬は長期間パターンが固定した高齢馬より反応が良い。",
        "clinical_signs": "calling/whinnying when separated; pawing; sweating; pacing; refusal to move away from barn or companion; bolting toward barn/companion; elevated heart rate; trembling",
        "clinical_signs_ja": "分離時のいななき、前掻き、発汗、歩き回り、馬房/仲間から離れることの拒否、馬房/仲間方向への暴走、心拍数上昇、震え。",
        "diagnosis": "Behavioral assessment. Rule out pain as underlying cause of reluctance. Assess training history and social environment.",
        "diagnosis_ja": "行動評価。拒否の根底にある疼痛の除外。トレーニング歴と社会環境の評価。",
        "urgency": "low",
        "category": "misc",
        "transmission": "Not transmissible.",
        "transmission_ja": "伝播しない。",
        "recommended_tests": ["行動評価 (Behavioral Assessment)", "歩様検査 (Lameness Examination)", "血液生化学検査 (Blood Chemistry Panel)"],
        "symptoms": ["behavioral_changes", "sweating", "vocalization"],
        "differential_diagnosis": "Pain-related reluctance, musculoskeletal injury, visual impairment, neurological conditions.",
        "severity_score": 2,
        "estimated_cost_level": "low",
        "hospitalization_likelihood": "low",
        "monitoring_frequency": "weekly",
        "treatment_duration_weeks": 12,
    },
]

data.extend(NEW_ENTRIES)
print(f"Added {len(NEW_ENTRIES)} new horse entries (wood chewing, coprophagy, anxiety)")
print(f"Total entries now: {len(data)}")

with open("diseases_all_species.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
