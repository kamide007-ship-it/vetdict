#!/usr/bin/env python3
"""Update cat behavioral disease treatments - batch 1 (6 entries)."""
import json

with open("diseases_all_species.json", "r") as f:
    data = json.load(f)

UPDATES = {
    "cat_feline_anxiety_disorder": {
        "treatment_ja": (
            "【薬物療法】第一選択: フルオキセチン 0.5-1.0 mg/kg PO q24h（効果発現まで4-6週間）。"
            "短期的不安軽減: ガバペンチン 50-100 mg/cat PO q8-12h（来院前投与にも有用: 来院60-90分前に100 mg/cat）。"
            "トラゾドン 50 mg/cat PO q12-24h（イベント性不安に）。"
            "クロミプラミン 0.25-0.5 mg/kg PO q24h（フルオキセチン無効例に）。"
            "ブスピロン 0.5-1.0 mg/kg PO q12h（社会的不安に特に有効）。"
            "【環境療法】フェリウェイ（合成F3フェイシャルフェロモン）ディフューザー設置。"
            "隠れ場所（箱、高い棚）・垂直空間の確保。安全な退避場所を各部屋に設置。"
            "多頭飼育の場合: トイレ数=猫数+1、食器・水飲みの分散配置。"
            "【行動修正】系統的脱感作（恐怖刺激を低強度から段階的に提示）。"
            "逆条件付け（恐怖刺激＋おやつ/遊び）。予測可能な日課の確立。"
            "罰は禁忌（不安を悪化させる）。"
            "【参考文献】Crowell-Davis SL et al. (2011) JAVMA; AAFP/ISFM Feline Environmental Needs Guidelines (2013); "
            "Overall KL. Clinical Behavioral Medicine for Small Animals (1997)."
        ),
        "treatment": (
            "[Pharmacotherapy] First-line: fluoxetine 0.5-1.0 mg/kg PO q24h (onset 4-6 weeks). "
            "Short-term anxiolysis: gabapentin 50-100 mg/cat PO q8-12h (also useful pre-visit: 100 mg/cat 60-90 min before). "
            "Trazodone 50 mg/cat PO q12-24h (event-based anxiety). "
            "Clomipramine 0.25-0.5 mg/kg PO q24h (if fluoxetine ineffective). "
            "Buspirone 0.5-1.0 mg/kg PO q12h (particularly effective for social anxiety). "
            "[Environmental Therapy] Feliway (synthetic F3 facial pheromone) diffuser placement. "
            "Provide hiding spots (boxes, high shelves) and vertical space. Safe retreat areas in each room. "
            "Multi-cat households: litter boxes = cats + 1, distributed food/water stations. "
            "[Behavior Modification] Systematic desensitization (gradual exposure to fear stimuli at low intensity). "
            "Counter-conditioning (fear stimulus + treats/play). Establish predictable daily routines. "
            "Punishment is contraindicated (worsens anxiety). "
            "[References] Crowell-Davis SL et al. (2011) JAVMA; AAFP/ISFM Feline Environmental Needs Guidelines (2013); "
            "Overall KL. Clinical Behavioral Medicine for Small Animals (1997)."
        ),
    },
    "cat_feline_cognitive_dysfunction_syndrome": {
        "treatment_ja": (
            "【評価】DISHAAL評価（見当識障害Disorientation・社会的交流変化Interactions・睡眠覚醒サイクル変化Sleep-wake・"
            "不適切排泄Housesoiling・活動レベル変化Activity・不安Anxiety・学習記憶低下Learning）で重症度を評価。"
            "【薬物療法】SAMe（S-アデノシルメチオニン）90 mg/cat PO q24h 空腹時（神経保護・抗酸化）。"
            "omega-3 DHA/EPA（EPA 40 mg/kg + DHA 25 mg/kg PO q24h）。"
            "夜間徘徊・過剰発声: トラゾドン 25-50 mg/cat PO q12-24h、またはガバペンチン 25-50 mg/cat PO q12h。"
            "メラトニン 1.5-6 mg/cat PO 就寝前（睡眠サイクル正常化）。"
            "セレギリン 0.5-1.0 mg/kg PO q24h（MAO-B阻害薬、ドーパミン増強）。"
            "【栄養療法】Hill's b/d（抗酸化栄養素・ビタミンE/C・L-カルニチン・DHA配合）。"
            "Purina Pro Plan Bright Mind（MCTオイル配合）。"
            "【環境管理】規則正しい生活リズムの維持。夜間用ナイトライト設置（見当識障害軽減）。"
            "トイレ・食器・寝床の位置を変更しない。段差の低いトイレに変更。"
            "環境エンリッチメント（穏やかな遊び、パズルフィーダー）。"
            "【参考文献】Gunn-Moore D et al. (2007) JFMS; Landsberg GM et al. (2012) Behavior Problems of the Dog and Cat 3rd ed; "
            "AAHA Senior Care Guidelines (2023)."
        ),
        "treatment": (
            "[Assessment] DISHAAL scoring (Disorientation, Interactions, Sleep-wake cycle, Housesoiling, "
            "Activity, Anxiety, Learning/memory) to evaluate severity. "
            "[Pharmacotherapy] SAMe (S-adenosylmethionine) 90 mg/cat PO q24h on empty stomach (neuroprotective/antioxidant). "
            "Omega-3 DHA/EPA (EPA 40 mg/kg + DHA 25 mg/kg PO q24h). "
            "Nighttime wandering/vocalization: trazodone 25-50 mg/cat PO q12-24h, or gabapentin 25-50 mg/cat PO q12h. "
            "Melatonin 1.5-6 mg/cat PO at bedtime (sleep cycle normalization). "
            "Selegiline 0.5-1.0 mg/kg PO q24h (MAO-B inhibitor, dopamine enhancement). "
            "[Nutritional Therapy] Hill's b/d (antioxidant nutrients, vitamin E/C, L-carnitine, DHA). "
            "Purina Pro Plan Bright Mind (MCT oil formula). "
            "[Environmental Management] Maintain consistent daily routines. Install nightlights (reduce disorientation). "
            "Do not relocate litter boxes, food bowls, or beds. Switch to low-sided litter boxes. "
            "Environmental enrichment (gentle play, puzzle feeders). "
            "[References] Gunn-Moore D et al. (2007) JFMS; Landsberg GM et al. (2012) Behavior Problems of the Dog and Cat 3rd ed; "
            "AAHA Senior Care Guidelines (2023)."
        ),
    },
    "cat_feline_compulsive_disorder": {
        "treatment_ja": (
            "【薬物療法】第一選択: フルオキセチン 0.5-1.0 mg/kg PO q24h（SSRI、効果発現4-6週間）。"
            "代替: クロミプラミン 0.25-0.5 mg/kg PO q24h（TCA）。"
            "過剰グルーミング（心因性脱毛）: フルオキセチン + ガバペンチン 5-10 mg/kg PO q8-12h（神経障害性疼痛の除外後）。"
            "ウールサッキング（毛織物吸引）: フルオキセチン + 食物繊維増量（Metamucil等）。"
            "テイルチェイシング（尾追い行動）: フルオキセチン + 環境エンリッチメント。"
            "【行動修正】トリガーの特定と回避・軽減。"
            "強迫行動中に罰を与えない（ストレス増加→悪化）。"
            "代替行動の強化（強迫行動の代わりに遊び・おやつで注意をそらす）。"
            "【環境療法】フェリウェイ拡散器。隠れ場所・高い場所の確保。"
            "予測可能な日課。定期的な遊び時間（1日15-30分×2-3回）。"
            "フォレイジングフィーダーで食事時間を延長。"
            "【鑑別診断の除外】皮膚疾患（真菌・アレルギー・外部寄生虫）、疼痛、神経疾患を除外後に行動学的診断。"
            "【参考文献】Luescher AU (2003) Compulsive behavior in companion animals. In: Recent Advances in Companion Animal Behavior Problems; "
            "Overall KL (2013) Manual of Clinical Behavioral Medicine for Dogs and Cats."
        ),
        "treatment": (
            "[Pharmacotherapy] First-line: fluoxetine 0.5-1.0 mg/kg PO q24h (SSRI, onset 4-6 weeks). "
            "Alternative: clomipramine 0.25-0.5 mg/kg PO q24h (TCA). "
            "Psychogenic alopecia (over-grooming): fluoxetine + gabapentin 5-10 mg/kg PO q8-12h (after ruling out neuropathic pain). "
            "Wool sucking: fluoxetine + dietary fiber supplementation (e.g., Metamucil). "
            "Tail chasing: fluoxetine + environmental enrichment. "
            "[Behavior Modification] Identify and avoid/reduce triggers. "
            "Never punish during compulsive episodes (increases stress → worsens condition). "
            "Reinforce alternative behaviors (redirect with play/treats instead of compulsive behavior). "
            "[Environmental Therapy] Feliway diffuser. Provide hiding spots and elevated spaces. "
            "Predictable routines. Regular play sessions (15-30 min × 2-3 times daily). "
            "Foraging feeders to extend mealtimes. "
            "[Differential Diagnosis Exclusion] Rule out dermatologic (fungal, allergic, ectoparasites), pain, "
            "and neurologic conditions before behavioral diagnosis. "
            "[References] Luescher AU (2003) Compulsive behavior in companion animals; "
            "Overall KL (2013) Manual of Clinical Behavioral Medicine for Dogs and Cats."
        ),
    },
    "cat_redirected_aggression": {
        "treatment_ja": (
            "【急性期管理】攻撃が起きたら即座に猫を隔離（別室）。刺激が残っている間は接触しない。"
            "興奮が収まるまで最低24-48時間の冷却期間（猫によっては数日必要）。"
            "無理に抱き上げない（二次的攻撃リスク）。厚手の手袋・毛布で保護して移動。"
            "【行動修正】トリガーの特定: 窓の外の猫・動物、大きな音、痛み、他の猫との喧嘩の目撃。"
            "窓フィルム・カーテンで外の刺激を遮断。"
            "再導入: 別室からドア越しのにおい交換→フィーディングステーションを徐々に接近→視覚的接触→監視下の直接接触。"
            "各段階で両猫がリラックスしていることを確認してから次に進む。"
            "【薬物療法】フルオキセチン 0.5-1.0 mg/kg PO q24h（慢性的な攻撃性に）。"
            "ガバペンチン 50-100 mg/cat PO q8-12h（急性期の不安軽減）。"
            "フェリウェイ（各部屋に拡散器設置）。"
            "【予防】トリガーへの暴露を最小化。各猫に独立した資源（トイレ、食器、寝床）を確保。"
            "【参考文献】Levine ED (2008) Feline fear and anxiety. Vet Clin North Am Small Anim Pract; "
            "Overall KL (1997) Clinical Behavioral Medicine for Small Animals."
        ),
        "treatment": (
            "[Acute Management] Immediately isolate the cat (separate room) when aggression occurs. "
            "No contact while stimulus persists. Minimum 24-48 hour cooling period (some cats need several days). "
            "Do not attempt to pick up (risk of secondary attack). Use thick gloves/blankets for safe transport. "
            "[Behavior Modification] Identify triggers: outdoor cats/animals, loud noises, pain, witnessing other cat fights. "
            "Block outdoor stimuli with window film/curtains. "
            "Reintroduction: scent exchange through closed door → gradually approach feeding stations → "
            "visual contact → supervised direct contact. Confirm both cats relaxed before advancing. "
            "[Pharmacotherapy] Fluoxetine 0.5-1.0 mg/kg PO q24h (chronic aggression). "
            "Gabapentin 50-100 mg/cat PO q8-12h (acute anxiety reduction). "
            "Feliway diffuser in each room. "
            "[Prevention] Minimize trigger exposure. Provide independent resources for each cat (litter box, food, bed). "
            "[References] Levine ED (2008) Feline fear and anxiety. Vet Clin North Am Small Anim Pract; "
            "Overall KL (1997) Clinical Behavioral Medicine for Small Animals."
        ),
    },
    "cat_territorial_marking___urine_spraying": {
        "treatment_ja": (
            "【医学的原因の除外】尿検査・尿培養で下部尿路疾患（FLUTD/FIC）を除外。"
            "血液検査で甲状腺機能亢進症・糖尿病・腎疾患を除外。"
            "【避妊・去勢】未去勢雄の90%、未避妊雌の95%がスプレー行動を示す→去勢/避妊で約90%が改善。"
            "ただし長期間の習慣化がある場合は去勢後も30%が継続。"
            "【環境管理】トイレ数=猫数+1。トイレの清潔維持（1日1-2回清掃）。"
            "スプレー箇所を酵素クリーナーで完全消臭（アンモニア系洗剤は逆効果）。"
            "スプレー箇所に食器を置く（摂食場所ではスプレーしにくい）。"
            "フェリウェイ（F3フェロモン）拡散器をスプレー多発エリアに設置。"
            "多頭飼育のストレス軽減: 各猫の独立した資源と空間を確保。"
            "外猫の視覚刺激を遮断（窓フィルム、カーテン）。"
            "【薬物療法】フルオキセチン 0.5-1.0 mg/kg PO q24h（最もエビデンスが豊富）。"
            "クロミプラミン 0.25-0.5 mg/kg PO q24h（代替）。"
            "ブスピロン 0.5-1.0 mg/kg PO q12h（多頭飼育の社会的ストレスに有効）。"
            "最低8-12週間の投薬継続後に段階的減量。"
            "【参考文献】Mills DS et al. (2011) Stress and Pheromonatherapy in Small Animal Clinical Behaviour; "
            "Pryor PA et al. (2001) Causes of urine marking in cats. JAVMA; "
            "Hart BL & Cooper L (1984) Factors relating to urine spraying and fighting in prepubertally gonadectomized cats. JAVMA."
        ),
        "treatment": (
            "[Rule Out Medical Causes] Urinalysis and urine culture to exclude FLUTD/FIC. "
            "Blood work to exclude hyperthyroidism, diabetes, renal disease. "
            "[Spay/Neuter] 90% of intact males and 95% of intact females spray → spay/neuter resolves ~90%. "
            "However, 30% may continue if long-established habit. "
            "[Environmental Management] Litter boxes = cats + 1. Maintain clean litter (1-2x daily scooping). "
            "Enzymatic cleaner on spray sites (ammonia-based cleaners are counterproductive). "
            "Place food bowls at spray sites (cats avoid spraying near feeding areas). "
            "Feliway (F3 pheromone) diffusers in high-spray areas. "
            "Multi-cat stress reduction: independent resources and space for each cat. "
            "Block visual stimuli from outdoor cats (window film, curtains). "
            "[Pharmacotherapy] Fluoxetine 0.5-1.0 mg/kg PO q24h (most evidence-based). "
            "Clomipramine 0.25-0.5 mg/kg PO q24h (alternative). "
            "Buspirone 0.5-1.0 mg/kg PO q12h (effective for multi-cat social stress). "
            "Minimum 8-12 weeks of treatment before gradual tapering. "
            "[References] Mills DS et al. (2011) Stress and Pheromonatherapy in Small Animal Clinical Behaviour; "
            "Pryor PA et al. (2001) Causes of urine marking in cats. JAVMA; "
            "Hart BL & Cooper L (1984) JAVMA."
        ),
    },
    "cat_pica": {
        "treatment_ja": (
            "【鑑別診断】消化器疾患（IBD、リンパ腫、膵炎）、栄養欠乏（鉄欠乏性貧血）、"
            "甲状腺機能亢進症、FIP、ポルフィリン症を除外。血液検査・腹部エコー・内視鏡検査を検討。"
            "【異物摂取の急性管理】消化管閉塞の疑い: 腹部X線/エコーで確認。閉塞あれば外科的摘出。"
            "線状異物（糸・紐）: 口腔内確認→舌下に係留されていれば切断せず外科紹介。"
            "【品種素因】シャム猫・ビルマ猫・東洋系品種にウールサッキング/異食症が多い（遺伝的素因）。"
            "【環境管理】異食対象物の徹底的な除去・アクセス制限。"
            "食物繊維の増量: 猫草（小麦草）の提供、高繊維食への変更。"
            "フォレイジングフィーダーで食事時間を延長。"
            "環境エンリッチメント: 噛めるおもちゃ、知育玩具、遊び時間の確保。"
            "【薬物療法】フルオキセチン 0.5-1.0 mg/kg PO q24h（強迫的異食に）。"
            "ガバペンチン 5-10 mg/kg PO q8-12h（不安軽減）。"
            "苦味スプレー（Bitter Apple等）を対象物に塗布。"
            "【参考文献】Bradshaw JWS (2006) The evolutionary basis for the feeding behavior of domestic dogs and cats. J Nutr; "
            "Bamberger M & Houpt KA (2006) Signalment factors, comorbidity, and trends in behavior diagnoses in cats. JAVMA."
        ),
        "treatment": (
            "[Differential Diagnosis] Rule out GI disease (IBD, lymphoma, pancreatitis), nutritional deficiency "
            "(iron deficiency anemia), hyperthyroidism, FIP, porphyria. Consider blood work, abdominal ultrasound, endoscopy. "
            "[Acute Foreign Body Management] Suspect GI obstruction: confirm with abdominal radiographs/ultrasound. "
            "Surgical removal if obstructed. Linear foreign bodies (string/thread): check oral cavity → "
            "if anchored under tongue, do not cut, refer for surgery. "
            "[Breed Predisposition] Siamese, Burmese, and Oriental breeds predisposed to wool sucking/pica (genetic component). "
            "[Environmental Management] Thorough removal/access restriction of target objects. "
            "Increase dietary fiber: provide cat grass (wheatgrass), switch to high-fiber diet. "
            "Foraging feeders to extend mealtimes. "
            "Environmental enrichment: chew toys, puzzle toys, dedicated play time. "
            "[Pharmacotherapy] Fluoxetine 0.5-1.0 mg/kg PO q24h (compulsive pica). "
            "Gabapentin 5-10 mg/kg PO q8-12h (anxiety reduction). "
            "Bitter spray (e.g., Bitter Apple) on target objects. "
            "[References] Bradshaw JWS (2006) J Nutr; "
            "Bamberger M & Houpt KA (2006) JAVMA."
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

print(f"Updated {updated} entries")

with open("diseases_all_species.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved.")
