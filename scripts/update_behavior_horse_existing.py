#!/usr/bin/env python3
"""Update horse behavioral diseases: 2 existing + 6 new stereotypic behaviors."""

import json

with open("diseases_all_species.json", "r") as f:
    data = json.load(f)

# --- Update existing 2 entries by name ---
NAME_UPDATES = {
    "Headshaking Syndrome": {
        "treatment_ja": (
            "【病態】三叉神経痛に起因する不随意の頭部振り運動。光過敏（photic headshaking）が約60%。"
            "季節性が多い（春〜夏に悪化）。"
            "【薬物療法】シプロヘプタジン 0.3 mg/kg PO q12h（抗ヒスタミン/抗セロトニン、第一選択）。"
            "カルバマゼピン 4-8 mg/kg PO q6-8h（抗てんかん薬、三叉神経痛に有効）。"
            "ガバペンチン 5-10 mg/kg PO q8-12h（神経障害性疼痛に）。"
            "フルフェナジン 0.04 mg/kg IM q3週間（フェノチアジン系、難治例に）。"
            "マグネシウム補充: MgO 10 g/日 PO（低マグネシウム血症の補正）。"
            "【光過敏性ヘッドシェイキング】UVカットフェイスマスク/ノーズネット装着（70%の症例で改善）。"
            "サングラス型アイカップ。暗い馬房での管理。夕方〜夜の騎乗にシフト。"
            "【外科療法】後篩骨神経切除術（posterior ethmoidal neurectomy）: 光過敏性の難治例に。"
            "成功率約50-70%、ただし再発リスクあり（1-3年で30%）。"
            "赤外線凝固術（infrared coagulation of posterior ethmoidal nerve）: 低侵襲代替。"
            "【鍼治療】顔面部の鍼治療が有効な症例報告あり。"
            "【環境管理】花粉・粉塵の暴露軽減。鼻腔内のアレルゲン刺激の最小化。"
            "【予後】季節性の症例は管理可能。通年性は難治。"
            "【参考文献】Madigan JE & Bell SA (2001) Owner survey of headshaking in horses. JAVMA; "
            "Roberts VLH et al. (2009) Caudal compression of infraorbital nerve for headshaking. Vet Surg; "
            "Newton SA et al. (2000) Idiopathic headshaking in horses. Vet Rec."
        ),
        "treatment": (
            "[Pathology] Involuntary head movements due to trigeminal neuralgia. "
            "Photic headshaking (~60% of cases). Often seasonal (worsens spring-summer). "
            "[Pharmacotherapy] Cyproheptadine 0.3 mg/kg PO q12h (antihistamine/antiserotonin, first-line). "
            "Carbamazepine 4-8 mg/kg PO q6-8h (anticonvulsant, effective for trigeminal neuralgia). "
            "Gabapentin 5-10 mg/kg PO q8-12h (neuropathic pain). "
            "Fluphenazine 0.04 mg/kg IM q3 weeks (phenothiazine, refractory cases). "
            "Magnesium supplementation: MgO 10 g/day PO (correct hypomagnesemia). "
            "[Photic Headshaking] UV-blocking face mask/nose net (improvement in ~70% of cases). "
            "Sunglass-type eye cups. Dark stable management. Shift riding to evening/night. "
            "[Surgical Therapy] Posterior ethmoidal neurectomy: refractory photic cases. "
            "Success rate ~50-70%, recurrence risk 30% at 1-3 years. "
            "Infrared coagulation of posterior ethmoidal nerve: minimally invasive alternative. "
            "[Acupuncture] Case reports of facial acupuncture efficacy. "
            "[Environmental Management] Reduce pollen/dust exposure. Minimize nasal allergen stimulation. "
            "[Prognosis] Seasonal cases manageable. Year-round cases are refractory. "
            "[References] Madigan JE & Bell SA (2001) JAVMA; "
            "Roberts VLH et al. (2009) Vet Surg; Newton SA et al. (2000) Vet Rec."
        ),
    },
    "Equine Self-Mutilation Syndrome": {
        "treatment_ja": (
            "【病態】自身の体（胸部、脇腹、肢端）を噛む・蹴る自傷行動。"
            "牡馬に多い（ホルモン関連）。ストレス、社会的隔離、退屈が誘因。"
            "【ホルモン療法】去勢手術（未去勢牡馬の場合、第一選択）。"
            "GnRHアゴニスト（デスロレリン4.7 mgインプラント SC）: 去勢済みでも残存行動がある場合。"
            "プロゲステロン製剤（アルトレノゲスト 0.044 mg/kg PO q24h）: 牡馬の攻撃性抑制に。"
            "【薬物療法】ナルトレキソン 0.04 mg/kg IV/IM（オピオイド拮抗薬、自傷行動の内因性オピオイド報酬系を遮断）。"
            "フルオキセチン 0.25-0.5 mg/kg PO q24h（SSRI、強迫性行動に）。"
            "ガバペンチン 5-10 mg/kg PO q8-12h（不安・疼痛管理）。"
            "ジフェンヒドラミン 1-2 mg/kg PO/IM q12h（軽度鎮静・抗掻痒）。"
            "【環境管理】社会的接触の確保（隣接馬房、放牧仲間）。"
            "十分な運動と放牧時間の確保。環境エンリッチメント（おもちゃ、干し草ネット）。"
            "馬房のサイズ拡大。自傷部位の保護（ネックカバー、ボディラップ）。"
            "【物理的保護】クレイドル（首の動きを制限）: 急性期の一時的使用のみ。"
            "長期使用はストレス増加→推奨しない。"
            "【皮膚損傷の治療】創傷洗浄 + 抗菌軟膏。二次感染防止。"
            "【参考文献】Dodman NH et al. (1994) Equine self-mutilation syndrome. J Vet Behav; "
            "Houpt KA (2011) Domestic Animal Behavior for Veterinarians and Animal Scientists 5th ed."
        ),
        "treatment": (
            "[Pathology] Self-biting/kicking of own body (chest, flanks, limbs). "
            "More common in stallions (hormone-related). Stress, social isolation, boredom as triggers. "
            "[Hormonal Therapy] Castration (first-line for intact stallions). "
            "GnRH agonist (deslorelin 4.7 mg implant SC): if residual behavior persists after castration. "
            "Progesterone (altrenogest 0.044 mg/kg PO q24h): stallion aggression suppression. "
            "[Pharmacotherapy] Naltrexone 0.04 mg/kg IV/IM (opioid antagonist, blocks endogenous opioid reward of self-mutilation). "
            "Fluoxetine 0.25-0.5 mg/kg PO q24h (SSRI, compulsive behavior). "
            "Gabapentin 5-10 mg/kg PO q8-12h (anxiety/pain management). "
            "Diphenhydramine 1-2 mg/kg PO/IM q12h (mild sedation/antipruritic). "
            "[Environmental Management] Ensure social contact (adjacent stalls, pasture companions). "
            "Adequate exercise and turnout time. Environmental enrichment (toys, hay nets). "
            "Increase stall size. Protect self-mutilation sites (neck covers, body wraps). "
            "[Physical Protection] Cradle (restrict neck movement): temporary acute use only. "
            "Long-term use increases stress → not recommended. "
            "[Wound Management] Wound lavage + antimicrobial ointment. Prevent secondary infection. "
            "[References] Dodman NH et al. (1994) J Vet Behav; "
            "Houpt KA (2011) Domestic Animal Behavior 5th ed."
        ),
    },
}

updated = 0
for entry in data:
    if entry.get("species") == "Horse" and entry.get("name") in NAME_UPDATES:
        upd = NAME_UPDATES[entry["name"]]
        entry["treatment"] = upd["treatment"]
        entry["treatment_ja"] = upd["treatment_ja"]
        updated += 1
        print(f"  Updated existing: {entry['name']}")

print(f"Updated {updated} existing entries")
with open("diseases_all_species.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("Saved.")
