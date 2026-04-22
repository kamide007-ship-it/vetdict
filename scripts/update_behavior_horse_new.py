#!/usr/bin/env python3
"""Add 6 new horse stereotypic behavior entries."""

import json

with open("diseases_all_species.json", "r") as f:
    data = json.load(f)

NEW_ENTRIES = [
    {
        "id": "horse_0026",
        "name": "Crib-Biting / Wind Sucking (Aerophagia)",
        "name_ja": "さく癖（クリビング）/ 空気嚥下症",
        "species": "Horse",
        "description": "A stereotypic behavior where the horse grasps a fixed object with its incisors, arches its neck, and swallows air. Wind sucking is the same behavior without grasping an object.",
        "description_ja": "馬が前歯で固定物を噛み、首をアーチ状にして空気を嚥下する常同行動。ウィンドサッキングは物を噛まずに同様の動作を行う。",
        "pathophysiology": "Considered an oral stereotypy linked to dopaminergic system dysregulation in the basal ganglia. Associated with chronic stress, restricted forage access, and social isolation. Not caused by observational learning from other horses (myth).",
        "pathophysiology_ja": "大脳基底核のドーパミン系調節障害に関連する口腔常同行動。慢性ストレス、粗飼料制限、社会的隔離が誘因。他の馬を見て学習するという説はエビデンスで否定されている。",
        "causes": "Restricted forage access, high-concentrate/low-forage diet, early weaning (especially abrupt), social isolation, confinement, chronic stress.",
        "causes_ja": "粗飼料制限、高濃厚飼料/低粗飼料食、早期離乳（特に急激な離乳）、社会的隔離、拘束飼育、慢性ストレス。",
        "treatment_ja": (
            "【基本原則】さく癖は常同行動であり「悪癖」ではない。罰や物理的抑制のみでは解決せず、福祉上も問題。"
            "根本的なストレス要因の改善が最重要。"
            "【飼養管理改善（第一選択）】粗飼料（乾草）の自由採食化またはスローフィーダー使用で採食時間延長。"
            "濃厚飼料の減量、給与回数の増加（1日3-4回以上に分割）。"
            "放牧時間の最大化（最低4-6時間/日）。社会的接触の確保（仲間馬との放牧）。"
            "馬房の拡大、環境エンリッチメント（おもちゃ、干し草ネット、塩ブロック）。"
            "【薬物療法】ナルトレキソン 0.04 mg/kg IV（オピオイド拮抗薬、短期的に行動頻度を50%以上減少させるエビデンスあり）。"
            "フルオキセチン 0.25-0.5 mg/kg PO q24h（SSRI、難治例に）。"
            "制酸剤: オメプラゾール 1-4 mg/kg PO q24h（胃潰瘍併発例に）。"
            "【消化器合併症】胃潰瘍（有病率が高い: さく癖馬の約50-68%に潰瘍）→胃内視鏡検査を推奨。"
            "疝痛リスク: 腸重積のリスクが一般集団より高い。"
            "前歯の摩耗→定期的な歯科検診。"
            "【物理的抑制（推奨しない）】クリビングストラップ: 福祉上の懸念が大きい。コルチゾール上昇のエビデンスあり。"
            "電気柵での抑制: 動物福祉法に抵触する可能性。"
            "馬房の表面をカバー: 一時的対症療法のみ。"
            "【外科療法（最終手段）】Forsell's手術（胸骨舌骨筋/胸骨甲状筋の部分切除）: 成功率60-70%。"
            "術後合併症リスクあり。再発率が高い。倫理的議論あり。"
            "【参考文献】McGreevy PD et al. (1995) Management factors associated with stereotypic behaviour in the Thoroughbred horse. Equine Vet J; "
            "Wickens CL & Heleski CR (2010) Crib-biting behavior in horses: A review. Appl Anim Behav Sci; "
            "Archer DC et al. (2008) Association between cribbing and entrapment colic. Vet Rec."
        ),
        "treatment": (
            "[Fundamental Principle] Crib-biting is a stereotypic behavior, not a 'vice.' Punishment or physical restraint alone "
            "does not resolve it and raises welfare concerns. Addressing root stressors is paramount. "
            "[Management Improvement (First-line)] Ad libitum forage (hay) access or slow feeders to extend foraging time. "
            "Reduce concentrates, increase feeding frequency (3-4+ times/day). "
            "Maximize turnout time (minimum 4-6 hours/day). Ensure social contact (pasture companions). "
            "Increase stall size, environmental enrichment (toys, hay nets, salt blocks). "
            "[Pharmacotherapy] Naltrexone 0.04 mg/kg IV (opioid antagonist, evidence of >50% behavior reduction short-term). "
            "Fluoxetine 0.25-0.5 mg/kg PO q24h (SSRI, refractory cases). "
            "Antacids: omeprazole 1-4 mg/kg PO q24h (concurrent gastric ulcers). "
            "[GI Complications] Gastric ulcers (high prevalence: ~50-68% of cribbers) → gastroscopy recommended. "
            "Colic risk: higher intussusception risk than general population. "
            "Incisor wear → regular dental examinations. "
            "[Physical Restraint (NOT recommended)] Cribbing strap: significant welfare concerns. Evidence of cortisol elevation. "
            "[Surgical Therapy (last resort)] Forssell's procedure (partial myectomy of sternohyoideus/sternothyroideus): "
            "60-70% success rate. Complication risk. High recurrence. Ethical debate. "
            "[References] McGreevy PD et al. (1995) Equine Vet J; "
            "Wickens CL & Heleski CR (2010) Appl Anim Behav Sci; Archer DC et al. (2008) Vet Rec."
        ),
        "prevention": "早期離乳の回避（漸進的離乳）。十分な粗飼料給与。社会的接触と放牧時間の確保。ストレスの最小化。",
        "prevention_ja": "早期離乳の回避（漸進的離乳）。十分な粗飼料給与。社会的接触と放牧時間の確保。ストレスの最小化。",
        "prognosis": "Once established, crib-biting is rarely completely eliminated but frequency can be significantly reduced with appropriate management changes. Early intervention yields better outcomes.",
        "prognosis_ja": "一旦確立したさく癖を完全に消失させることは困難だが、適切な飼養管理改善で頻度を大幅に減少可能。早期介入で予後が改善。",
        "clinical_signs": "grasping fixed objects with incisors; arching neck; gulping air; excessive salivation; worn incisors; weight loss; poor body condition; gastric ulcer signs",
        "clinical_signs_ja": "前歯で固定物を噛む、首をアーチ状に曲げる、空気の嚥下、過剰な流涎、前歯の摩耗、体重減少、ボディコンディション低下、胃潰瘍徴候。",
        "diagnosis": "Direct behavioral observation. Gastroscopy for concurrent gastric ulcers. Dental examination for incisor wear. Rule out GI pain as primary cause.",
        "diagnosis_ja": "行動観察による直接診断。胃内視鏡検査で併発胃潰瘍を確認。歯科検査で前歯摩耗を評価。消化器疼痛を一次原因として除外。",
        "urgency": "low",
        "category": "misc",
        "transmission": "Not transmissible. Despite common belief, observational learning of crib-biting from other horses has been disproven by controlled studies.",
        "transmission_ja": "伝播しない。他の馬を見て学習するという一般的な通説は対照研究で否定されている。",
        "recommended_tests": [
            "胃内視鏡検査 (Gastroscopy)",
            "歯科検査 (Dental Examination)",
            "血液生化学検査 (Blood Chemistry Panel)",
        ],
        "symptoms": ["behavioral_changes", "weight_loss", "poor_body_condition", "dental_abnormalities"],
        "differential_diagnosis": "Rule out gastric ulcers, dental pain, GI discomfort as primary causes triggering the behavior.",
        "severity_score": 2,
        "estimated_cost_level": "moderate",
        "hospitalization_likelihood": "low",
        "monitoring_frequency": "monthly",
        "treatment_duration_weeks": 52,
    },
    {
        "id": "horse_0027",
        "name": "Weaving",
        "name_ja": "熊癖（ウィービング）",
        "species": "Horse",
        "description": "A locomotor stereotypy characterized by repetitive lateral swaying of the head, neck, and forequarters, typically performed while standing at the stall door.",
        "description_ja": "馬房の扉付近で頭部・頸部・前躯を左右に反復的に振る運動性常同行動。",
        "pathophysiology": "Locomotor stereotypy associated with dopaminergic dysregulation in the basal ganglia. Develops as a coping mechanism for chronic frustration of locomotor motivation in confined environments.",
        "pathophysiology_ja": "大脳基底核のドーパミン系調節障害に関連する運動性常同行動。拘束環境における運動動機の慢性的欲求不満への対処機制として発達。",
        "causes": "Prolonged confinement, insufficient turnout/exercise, social isolation, restricted visual contact with other horses, monotonous environment.",
        "causes_ja": "長時間の拘束飼育、不十分な放牧/運動、社会的隔離、他馬との視覚的接触の制限、単調な環境。",
        "treatment_ja": (
            "【飼養管理改善（第一選択）】放牧時間の最大化が最も有効な治療。"
            "最低限: 1日6時間以上の放牧（理想は終日放牧）。"
            "仲間馬との社会的接触（放牧仲間、隣接馬房での視覚・嗅覚接触）。"
            "馬房に窓・開口部を設けて視野を広げる。"
            "【馬房環境の改善】馬房サイズの拡大（最低3.6m×3.6m、理想は4m×4m以上）。"
            "ミラー設置: 馬房内の鏡が熊癖頻度を減少させるエビデンスあり（McAfee et al. 2002）。"
            "干し草ネット・スローフィーダーで採食時間を延長。"
            "環境エンリッチメント（馬用おもちゃ、塩ブロック、枝）。"
            "馬房の扉を開放型（上部開放）にして外部への視野を確保。"
            "【運動プログラム】定期的な運動（騎乗、調馬索、ウォーカー）。"
            "運動パターンのバリエーションを増やす。"
            "【薬物療法（補助的）】ナルトレキソン 0.04 mg/kg IV（研究レベル）。"
            "重度の場合: フルオキセチン 0.25-0.5 mg/kg PO q24h。"
            "トリプトファン補充 20 mg/kg PO q24h（セロトニン前駆体、軽度の効果報告あり）。"
            "【物理的抑制（非推奨）】Vバー（扉にV字型金具設置）: 動物福祉上の問題。行動を抑制するが原因を解決しない。"
            "ストレスホルモン（コルチゾール）上昇のエビデンスあり。"
            "【整形外科的合併症】慢性的な熊癖は前肢の腱・靭帯への負荷増大、蹄の不均等な摩耗、"
            "体重減少・筋肉疲労を引き起こしうる。定期的な装蹄を推奨。"
            "【参考文献】Cooper JJ et al. (2000) The effect of increasing visual horizons on stereotypic weaving. Appl Anim Behav Sci; "
            "McAfee LM et al. (2002) The use of mirrors to reduce weaving in stabled horses. Appl Anim Behav Sci; "
            "Mills DS & Riezebos M (2005) The role of exteroceptive and interoceptive cues in stereotypic weaving. Appl Anim Behav Sci."
        ),
        "treatment": (
            "[Management Improvement (First-line)] Maximizing turnout is the most effective treatment. "
            "Minimum: 6+ hours/day turnout (ideal: full-day turnout). "
            "Social contact with companion horses (pasture mates, visual/olfactory contact in adjacent stalls). "
            "Provide windows/openings in stalls to broaden visual field. "
            "[Stall Environment] Increase stall size (minimum 3.6m×3.6m, ideal 4m×4m+). "
            "Mirror installation: evidence that stable mirrors reduce weaving frequency (McAfee et al. 2002). "
            "Hay nets/slow feeders to extend foraging time. "
            "Environmental enrichment (horse toys, salt blocks, branches). "
            "Open-top stall doors for external visual access. "
            "[Exercise Program] Regular exercise (riding, lunging, walker). Vary exercise patterns. "
            "[Pharmacotherapy (adjunctive)] Naltrexone 0.04 mg/kg IV (research level). "
            "Severe cases: fluoxetine 0.25-0.5 mg/kg PO q24h. "
            "Tryptophan supplementation 20 mg/kg PO q24h (serotonin precursor, mild effect reported). "
            "[Physical Restraint (NOT recommended)] V-bars (V-shaped fixtures on door): animal welfare concern. "
            "Suppresses behavior without addressing cause. Evidence of cortisol elevation. "
            "[Orthopedic Complications] Chronic weaving can increase forelimb tendon/ligament strain, "
            "uneven hoof wear, weight loss, and muscle fatigue. Regular farriery recommended. "
            "[References] Cooper JJ et al. (2000) Appl Anim Behav Sci; "
            "McAfee LM et al. (2002) Appl Anim Behav Sci; Mills DS & Riezebos M (2005) Appl Anim Behav Sci."
        ),
        "prevention": "十分な放牧時間。社会的接触。広い馬房。環境エンリッチメント。子馬期の適切な離乳管理。",
        "prevention_ja": "十分な放牧時間。社会的接触。広い馬房。環境エンリッチメント。子馬期の適切な離乳管理。",
        "prognosis": "Difficult to eliminate once established. Can be significantly reduced with management changes. Prognosis for reduction is good with adequate turnout and social contact.",
        "prognosis_ja": "確立後の完全消失は困難。飼養管理改善で大幅な減少が可能。十分な放牧と社会的接触があれば軽減の予後は良好。",
        "clinical_signs": "repetitive lateral swaying of head and forequarters at stall door; weight shifting between forelimbs; may progress to involve entire forebody",
        "clinical_signs_ja": "馬房の扉で頭部・前躯を反復的に左右に揺らす。前肢間での体重移動。進行すると前躯全体が関与。",
        "diagnosis": "Direct behavioral observation. Rule out neurological conditions. Assess stable management and social environment.",
        "diagnosis_ja": "行動観察による直接診断。神経疾患の除外。飼養管理・社会環境の評価。",
        "urgency": "low",
        "category": "misc",
        "transmission": "Not transmissible. Social facilitation has not been demonstrated in controlled studies.",
        "transmission_ja": "伝播しない。対照研究で社会的促進は実証されていない。",
        "recommended_tests": [
            "行動観察 (Behavioral Assessment)",
            "神経学的検査 (Neurological Examination)",
            "装蹄評価 (Farrier Assessment)",
        ],
        "symptoms": ["behavioral_changes", "weight_loss", "lameness"],
        "differential_diagnosis": "Neurological conditions (EPM, wobblers), vestibular disease, pain-related shifting.",
        "severity_score": 2,
        "estimated_cost_level": "low",
        "hospitalization_likelihood": "low",
        "monitoring_frequency": "monthly",
        "treatment_duration_weeks": 52,
    },
    {
        "id": "horse_0028",
        "name": "Stall Walking / Box Walking",
        "name_ja": "旋回癖（ストールウォーキング）",
        "species": "Horse",
        "description": "A locomotor stereotypy characterized by repetitive circling or pacing within the stall.",
        "description_ja": "馬房内で反復的に旋回または歩き回る運動性常同行動。",
        "pathophysiology": "Locomotor stereotypy arising from frustration of movement motivation in confined environments. Related to basal ganglia dopaminergic dysregulation.",
        "pathophysiology_ja": "拘束環境における運動動機の欲求不満から生じる運動性常同行動。大脳基底核のドーパミン系調節障害に関連。",
        "causes": "Prolonged confinement, insufficient exercise, social isolation, pre-feeding anticipation, anxiety.",
        "causes_ja": "長時間の拘束飼育、不十分な運動、社会的隔離、給餌前の予期的興奮、不安。",
        "treatment_ja": (
            "【飼養管理改善（第一選択）】放牧時間の最大化（最低6時間/日以上）。"
            "仲間馬との社会的接触。馬房サイズの拡大。"
            "給餌スケジュールの規則化と予測可能性の向上（給餌前の旋回が誘発される場合）。"
            "粗飼料の自由採食または頻回給与。"
            "【環境エンリッチメント】ミラー設置。干し草ネット・スローフィーダー。"
            "馬房の窓・開口部の確保。おもちゃ・塩ブロック。"
            "馬房の床材を深くして歩行コストを上げる試みもあるが、福祉面で議論あり。"
            "【運動プログラム】十分な運動量の確保。ウォーカー・調馬索・騎乗。"
            "運動パターンのバリエーション。"
            "【薬物療法（補助的）】トリプトファン 20 mg/kg PO q24h。"
            "重度: フルオキセチン 0.25-0.5 mg/kg PO q24h。"
            "マグネシウム補充（低Mg血症の補正）。"
            "【合併症】不均等な蹄摩耗、蹄葉炎リスク、筋疲労、体重減少。"
            "定期的な装蹄が重要。"
            "【参考文献】Houpt KA (1986) Stable vices and trailer problems. Vet Clin North Am Equine Pract; "
            "Cooper JJ & Albentosa MJ (2005) Behavioural adaptation in the domestic horse. Equine Vet J."
        ),
        "treatment": (
            "[Management Improvement (First-line)] Maximize turnout (minimum 6+ hours/day). "
            "Social contact with companion horses. Increase stall size. "
            "Regularize feeding schedule (if pre-feeding pacing is trigger). "
            "Ad libitum or frequent forage feeding. "
            "[Environmental Enrichment] Mirror installation. Hay nets/slow feeders. "
            "Stall windows/openings. Toys, salt blocks. "
            "[Exercise Program] Ensure adequate exercise. Walker, lunging, riding. Vary exercise patterns. "
            "[Pharmacotherapy (adjunctive)] Tryptophan 20 mg/kg PO q24h. "
            "Severe: fluoxetine 0.25-0.5 mg/kg PO q24h. "
            "Magnesium supplementation (correct hypomagnesemia). "
            "[Complications] Uneven hoof wear, laminitis risk, muscle fatigue, weight loss. "
            "Regular farriery essential. "
            "[References] Houpt KA (1986) Vet Clin North Am Equine Pract; "
            "Cooper JJ & Albentosa MJ (2005) Equine Vet J."
        ),
        "prevention": "十分な放牧。社会的接触。広い馬房。規則的な給餌スケジュール。",
        "prevention_ja": "十分な放牧。社会的接触。広い馬房。規則的な給餌スケジュール。",
        "prognosis": "Management changes can significantly reduce frequency. Complete cessation is difficult once established.",
        "prognosis_ja": "飼養管理改善で頻度を大幅に減少可能。確立後の完全消失は困難。",
        "clinical_signs": "repetitive circling or pacing in stall; worn track in bedding; weight loss; uneven hoof wear",
        "clinical_signs_ja": "馬房内での反復的旋回・歩行。敷料に円形の踏跡。体重減少。蹄の不均等摩耗。",
        "diagnosis": "Direct behavioral observation. Rule out pain, neurological conditions, colic.",
        "diagnosis_ja": "行動観察による直接診断。疼痛、神経疾患、疝痛の除外。",
        "urgency": "low",
        "category": "misc",
        "transmission": "Not transmissible.",
        "transmission_ja": "伝播しない。",
        "recommended_tests": [
            "行動観察 (Behavioral Assessment)",
            "歩様検査 (Lameness Examination)",
            "装蹄評価 (Farrier Assessment)",
        ],
        "symptoms": ["behavioral_changes", "weight_loss", "lameness"],
        "differential_diagnosis": "Colic, neurological disease, pain, vestibular dysfunction.",
        "severity_score": 2,
        "estimated_cost_level": "low",
        "hospitalization_likelihood": "low",
        "monitoring_frequency": "monthly",
        "treatment_duration_weeks": 52,
    },
]

data.extend(NEW_ENTRIES)
print(f"Added {len(NEW_ENTRIES)} new horse entries (cribbing, weaving, stall walking)")
print(f"Total entries now: {len(data)}")

with open("diseases_all_species.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
