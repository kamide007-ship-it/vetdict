#!/usr/bin/env python3
"""Update cat behavioral disease treatments - batch 2 (6 entries)."""
import json

with open("diseases_all_species.json", "r") as f:
    data = json.load(f)

UPDATES = {
    "cat_separation_anxiety": {
        "treatment_ja": (
            "【診断】他の疾患（FLUTD、認知機能不全、甲状腺機能亢進症）の除外。"
            "留守中のビデオ録画で不在時の行動パターンを確認（過剰発声、不適切排泄、破壊行動、過剰グルーミング）。"
            "【行動修正】出発・帰宅の儀式を最小化（興奮させない）。"
            "系統的脱感作: 出発の合図（鍵を持つ、靴を履く等）を繰り返し提示して脱感作。"
            "短時間の不在から段階的に延長。帰宅後すぐに猫に反応しない（落ち着いてから対応）。"
            "独立した遊びを強化: パズルフィーダー、フォレイジングトイ、タイマー付き自動給餌器。"
            "【環境療法】フェリウェイ拡散器。窓辺にキャットツリー設置（外の観察で退屈軽減）。"
            "留守中のBGM（クラシック音楽、猫用音楽: Through a Cat's Ear等）。"
            "安全な隠れ場所を複数確保。"
            "【薬物療法】フルオキセチン 0.5-1.0 mg/kg PO q24h（第一選択、4-6週間で効果発現）。"
            "クロミプラミン 0.25-0.5 mg/kg PO q24h。"
            "短期的: トラゾドン 50 mg/cat PO（長時間の留守前に）。"
            "ガバペンチン 50-100 mg/cat PO q8-12h。"
            "アルファカソジン（Zylkene）75 mg/cat PO q24h（カゼイン由来ペプチド、軽度不安に）。"
            "【参考文献】Schwartz S (2002) Separation anxiety syndrome in cats. JAVMA; "
            "de Souza Machado D et al. (2020) Identification of separation-related problems in domestic cats. PLoS ONE."
        ),
        "treatment": (
            "[Diagnosis] Rule out other conditions (FLUTD, cognitive dysfunction, hyperthyroidism). "
            "Video recording during absence to confirm behavior patterns (excessive vocalization, inappropriate elimination, "
            "destructive behavior, over-grooming). "
            "[Behavior Modification] Minimize departure/arrival rituals (avoid exciting the cat). "
            "Systematic desensitization: repeatedly present departure cues (picking up keys, putting on shoes) to desensitize. "
            "Gradually extend absence duration from short periods. Don't react to cat immediately on return (respond after calm). "
            "Reinforce independent play: puzzle feeders, foraging toys, timed automatic feeders. "
            "[Environmental Therapy] Feliway diffuser. Cat tree by window (reduce boredom through outdoor observation). "
            "Background music during absence (classical, cat-specific: Through a Cat's Ear). "
            "Multiple safe hiding spots. "
            "[Pharmacotherapy] Fluoxetine 0.5-1.0 mg/kg PO q24h (first-line, onset 4-6 weeks). "
            "Clomipramine 0.25-0.5 mg/kg PO q24h. "
            "Short-term: trazodone 50 mg/cat PO (before extended absences). "
            "Gabapentin 50-100 mg/cat PO q8-12h. "
            "Alpha-casozepine (Zylkene) 75 mg/cat PO q24h (casein-derived peptide, for mild anxiety). "
            "[References] Schwartz S (2002) JAVMA; "
            "de Souza Machado D et al. (2020) PLoS ONE."
        ),
    },
    "cat_feline_idiopathic_aggression": {
        "treatment_ja": (
            "【注意】特発性攻撃行動は他の全ての攻撃タイプ（疼痛性、恐怖性、転嫁性、縄張り性、遊び性、"
            "母性、てんかん関連）を除外した上での除外診断。予測不能な攻撃は飼い主の安全リスクが高い。"
            "【医学的精査】神経学的検査（部分発作の可能性）。甲状腺機能検査。"
            "頭部MRI/CT（腫瘍・構造的病変の除外）。血液検査一般。"
            "疼痛評価（口腔内・関節・腹部）。"
            "【安全管理】攻撃の前兆パターンを記録（瞳孔散大、耳伏せ、尾の膨大、皮膚の波打ち）。"
            "飼い主への安全指導: 前兆を認めたら即座に離れる。追い詰めない。"
            "子供や高齢者がいる家庭では安全な分離空間を確保。"
            "【薬物療法】フルオキセチン 0.5-1.0 mg/kg PO q24h（第一選択）。"
            "ガバペンチン 50-100 mg/cat PO q8-12h（特に疼痛関連の可能性がある場合）。"
            "フェリウェイ拡散器。"
            "重度の場合: フルオキセチン + ガバペンチンの併用。"
            "効果不十分時: ブスピロン 0.5-1.0 mg/kg PO q12hへの変更を検討。"
            "【行動修正】罰は絶対禁忌（悪化する）。トリガーの回避。"
            "正の強化による基本トレーニング（おやつで穏やかな行動を報酬）。"
            "予測可能な日課の確立。"
            "【予後】特発性攻撃行動は薬物療法への反応が限定的な場合があり、慎重な予後告知が必要。"
            "安楽死を含む全選択肢について飼い主と率直に議論。"
            "【参考文献】Beaver BV (2003) Feline Behavior: A Guide for Veterinarians 2nd ed; "
            "Amat M et al. (2009) Aggressive behavior in the English cocker spaniel. J Vet Behav."
        ),
        "treatment": (
            "[Caution] Idiopathic aggression is a diagnosis of exclusion after ruling out all other aggression types "
            "(pain-induced, fear, redirected, territorial, play, maternal, seizure-related). "
            "Unpredictable aggression poses high safety risk to owners. "
            "[Medical Workup] Neurological examination (partial seizure potential). Thyroid function tests. "
            "Head MRI/CT (rule out tumors/structural lesions). General blood work. "
            "Pain assessment (oral, articular, abdominal). "
            "[Safety Management] Record pre-attack patterns (pupil dilation, ear flattening, tail puffing, skin rippling). "
            "Owner safety counseling: disengage immediately upon seeing precursors. Never corner the cat. "
            "Ensure safe separation spaces in households with children or elderly. "
            "[Pharmacotherapy] Fluoxetine 0.5-1.0 mg/kg PO q24h (first-line). "
            "Gabapentin 50-100 mg/cat PO q8-12h (especially if pain component suspected). "
            "Feliway diffuser. "
            "Severe cases: fluoxetine + gabapentin combination. "
            "If inadequate response: consider switching to buspirone 0.5-1.0 mg/kg PO q12h. "
            "[Behavior Modification] Punishment absolutely contraindicated (worsens condition). Trigger avoidance. "
            "Positive reinforcement training (reward calm behavior with treats). "
            "Establish predictable routines. "
            "[Prognosis] Idiopathic aggression may have limited response to pharmacotherapy; guarded prognosis warranted. "
            "Discuss all options including euthanasia frankly with owners. "
            "[References] Beaver BV (2003) Feline Behavior 2nd ed; "
            "Amat M et al. (2009) J Vet Behav."
        ),
    },
    "cat_feline_noise_phobia": {
        "treatment_ja": (
            "【急性期管理】安全な退避場所（クローゼット内、ベッド下、キャリーの中等）へのアクセスを確保。"
            "無理に隠れ場所から出さない。窓・カーテンを閉めて音と光を遮断。"
            "BGM/ホワイトノイズで環境音をマスキング。飼い主は平常通りに振る舞う（過度の慰めは不安を強化しうる）。"
            "【薬物療法（イベント性）】ガバペンチン 50-100 mg/cat PO（恐怖イベントの60-90分前に投与）。"
            "トラゾドン 50 mg/cat PO（イベント前）。併用も可。"
            "【薬物療法（慢性/予防）】フルオキセチン 0.5-1.0 mg/kg PO q24h（花火シーズン等の前から開始、4-6週間前投与開始）。"
            "ガバペンチン 25-50 mg/cat PO q8-12h（日常的に恐怖が高い猫に）。"
            "フェリウェイ拡散器（常時使用）。"
            "【行動修正】系統的脱感作: 恐怖音の録音を非常に小さい音量から再生→おやつ/遊び→段階的に音量上昇。"
            "1セッション5-10分、週3-5回、数週間かけて実施。"
            "逆条件付け: 恐怖音＝おやつの連合学習。"
            "サンダーシャツ（圧迫ベスト）: エビデンスは限定的だが一部の猫に有効。"
            "【参考文献】Crowell-Davis SL et al. (2003) Veterinary psychopharmacology. Blackwell; "
            "Overall KL (2013) Manual of Clinical Behavioral Medicine for Dogs and Cats."
        ),
        "treatment": (
            "[Acute Management] Ensure access to safe retreat (closet, under bed, inside carrier). "
            "Never force cat out of hiding. Close windows/curtains to block sound and light. "
            "Mask environmental sounds with background music/white noise. "
            "Owner should behave normally (excessive comforting may reinforce anxiety). "
            "[Event-Based Pharmacotherapy] Gabapentin 50-100 mg/cat PO (60-90 min before fear event). "
            "Trazodone 50 mg/cat PO (before event). Combination acceptable. "
            "[Chronic/Preventive Pharmacotherapy] Fluoxetine 0.5-1.0 mg/kg PO q24h "
            "(start 4-6 weeks before firework season etc.). "
            "Gabapentin 25-50 mg/cat PO q8-12h (for cats with chronically elevated fear). "
            "Feliway diffuser (continuous use). "
            "[Behavior Modification] Systematic desensitization: play recorded fear sounds at very low volume → "
            "treats/play → gradually increase volume. "
            "Sessions 5-10 min, 3-5x/week, over several weeks. "
            "Counter-conditioning: fear sound = treat association. "
            "ThunderShirt (compression vest): limited evidence but effective in some cats. "
            "[References] Crowell-Davis SL et al. (2003) Veterinary psychopharmacology; "
            "Overall KL (2013) Manual of Clinical Behavioral Medicine for Dogs and Cats."
        ),
    },
    "cat_feline_pyrethroid_toxicosis_topical": {
        # This is not behavioral - keep improved but mark as non-behavioral
        "treatment_ja": (
            "【緊急対応】ピレスロイド含有製品を直ちに除去。ぬるま湯と食器用洗剤（Dawn等）で全身を洗浄。"
            "猫用でない犬用ピレスロイド製品（ペルメトリン等）の誤用が最も多い原因。"
            "【振戦管理】メトカルバモール 55-220 mg/kg IV（緩徐投与、330 mg/kg/日を超えない）。"
            "メトカルバモールが利用不能な場合: ジアゼパム 0.5-1.0 mg/kg IV PRN。"
            "重度の振戦にはプロポフォール 1-4 mg/kg IV（CRI 0.1-0.4 mg/kg/min）。"
            "【痙攣管理】ジアゼパム 0.5-1.0 mg/kg IV。レベチラセタム 20-60 mg/kg IV。"
            "【支持療法】静脈輸液（脱水補正、薬物排泄促進）。"
            "体温モニタリング（振戦による高体温→冷却）。"
            "ILE（脂肪乳剤）療法 20%イントラリピッド 1.5 mL/kg IV ボーラス→0.25 mL/kg/min CRI 60分（重症例）。"
            "【予後】早期の適切な治療で予後良好（回復率>95%）。通常24-72時間で回復。"
            "【予防】猫に犬用ピレスロイド製品を絶対使用しない。犬と猫が同居の場合、犬への塗布後も猫への接触を制限。"
            "【参考文献】Richardson JA (2000) Permethrin spot-on toxicoses in cats. J Vet Emerg Crit Care; "
            "Haworth MD & Smart L (2012) Use of intravenous lipid therapy in three cases of feline permethrin toxicosis. J Vet Emerg Crit Care."
        ),
        "treatment": (
            "[Emergency Response] Immediately remove pyrethroid-containing product. "
            "Bathe entire body with lukewarm water and dish soap (e.g., Dawn). "
            "Most common cause: accidental application of canine pyrethroid products (permethrin) to cats. "
            "[Tremor Management] Methocarbamol 55-220 mg/kg IV (slow administration, max 330 mg/kg/day). "
            "If methocarbamol unavailable: diazepam 0.5-1.0 mg/kg IV PRN. "
            "Severe tremors: propofol 1-4 mg/kg IV (CRI 0.1-0.4 mg/kg/min). "
            "[Seizure Management] Diazepam 0.5-1.0 mg/kg IV. Levetiracetam 20-60 mg/kg IV. "
            "[Supportive Care] IV fluids (rehydration, promote drug excretion). "
            "Temperature monitoring (tremor-induced hyperthermia → active cooling). "
            "ILE (Intralipid) therapy 20% Intralipid 1.5 mL/kg IV bolus → 0.25 mL/kg/min CRI 60 min (severe cases). "
            "[Prognosis] Good with early appropriate treatment (recovery rate >95%). Usually recovers in 24-72 hours. "
            "[Prevention] NEVER use canine pyrethroid products on cats. "
            "Restrict cat contact with treated dogs after application. "
            "[References] Richardson JA (2000) J Vet Emerg Crit Care; "
            "Haworth MD & Smart L (2012) J Vet Emerg Crit Care."
        ),
    },
    # Cardiovascular Behavioral Disorder is likely a data artifact, but let's check
}

# Also find and update the Cardiovascular Behavioral Disorder entry
for entry in data:
    eid = entry.get("id", "")
    if eid == "cat_cardiovascular_behavioral_disorder_cat":
        UPDATES[eid] = {
            "treatment_ja": (
                "【注意】心血管系疾患に伴う行動変化は原発性行動疾患ではなく、基礎疾患の症状である。"
                "【基礎疾患の治療】肥大型心筋症（HCM）: アテノロール 6.25-12.5 mg/cat PO q12h。"
                "拡張型心筋症（DCM）: タウリン補充 250-500 mg/cat PO q12h、ピモベンダン 0.25 mg/kg PO q12h。"
                "うっ血性心不全: フロセミド 1-2 mg/kg PO/IV q8-12h、ベナゼプリル 0.5 mg/kg PO q24h。"
                "動脈血栓塞栓症（ATE）: 疼痛管理（ブプレノルフィン 0.02 mg/kg IV/IM q6-8h）+ クロピドグレル 18.75 mg/cat PO q24h。"
                "【行動変化の管理】低酸素血症による不安・興奮: 酸素療法。"
                "慢性心疾患に伴う活動性低下・隠れ行動: 環境調整（低い場所にベッド・食器配置）。"
                "【モニタリング】呼吸数モニタリング（安静時呼吸数>30回/分は心不全悪化の指標）。"
                "定期的心エコー検査（3-6ヶ月毎）。"
                "【参考文献】Luis Fuentes V et al. (2020) ACVIM consensus statement on classification of cardiomyopathies in cats. J Vet Intern Med."
            ),
            "treatment": (
                "[Note] Behavioral changes associated with cardiovascular disease are symptoms of underlying disease, "
                "not primary behavioral disorders. "
                "[Treat Underlying Disease] HCM: atenolol 6.25-12.5 mg/cat PO q12h. "
                "DCM: taurine supplementation 250-500 mg/cat PO q12h, pimobendan 0.25 mg/kg PO q12h. "
                "CHF: furosemide 1-2 mg/kg PO/IV q8-12h, benazepril 0.5 mg/kg PO q24h. "
                "ATE: pain management (buprenorphine 0.02 mg/kg IV/IM q6-8h) + clopidogrel 18.75 mg/cat PO q24h. "
                "[Behavioral Change Management] Hypoxemia-related anxiety/agitation: oxygen therapy. "
                "Chronic heart disease-related activity reduction/hiding: environmental adjustment (low placement of beds/bowls). "
                "[Monitoring] Resting respiratory rate monitoring (>30 breaths/min indicates CHF progression). "
                "Regular echocardiography (every 3-6 months). "
                "[References] Luis Fuentes V et al. (2020) ACVIM consensus statement. J Vet Intern Med."
            ),
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
