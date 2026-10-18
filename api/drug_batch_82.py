"""Drug batch 82 – 2026-10 第73弾.

1. Ciclesonide inhalation spray (Aservo EquiHaler) — the first inhaled
   corticosteroid licensed for horses (FDA 2020; EU/UK authorised), for the
   management of severe equine asthma. The equine asthma entries cited
   "Aservo EquiHaler" but as *inhaled dexamethasone* at "2 puffs q12h", an
   incorrect active ingredient and regimen — corrected in the disease text
   in the same batch (label: 343 µg/actuation; days 1-5 eight actuations
   q12h, days 6-10 twelve actuations q24h).

Evidence:
  - Aservo EquiHaler (ciclesonide inhalation spray) US label / EU SPC,
    Boehringer Ingelheim Animal Health.
  - Lavoie JP et al. Efficacy of inhaled ciclesonide for treatment of severe
    equine asthma. J Vet Intern Med 2019;33:1059-1066 (placebo-controlled).
  - Couetil LL et al. ACVIM Consensus Statement: Inflammatory airway
    disease of horses — revised consensus. J Vet Intern Med 2016;30:503-515.
"""

DRUGS_BATCH_82 = [
    {
        "id": "ciclesonide_inhaled",
        "search_aliases": [
            "シクレソニド",
            "しくれそにど",
            "アセルボ",
            "Aservo",
            "Aservo EquiHaler",
            "EquiHaler",
            "ciclesonide",
        ],
        "name": "Ciclesonide Inhalation Spray (Aservo EquiHaler)",
        "name_ja": "シクレソニド吸入スプレー（アセルボ エクイヘイラー）",
        "category": "respiratory",
        "mechanism": "Inhaled prodrug corticosteroid activated by airway esterases to des-ciclesonide, a potent glucocorticoid-receptor agonist that suppresses neutrophilic airway inflammation and bronchial hyperreactivity. Local activation, high plasma-protein binding and rapid hepatic clearance keep systemic glucocorticoid exposure low compared with systemic dexamethasone/prednisolone.",
        "mechanism_ja": "気道のエステラーゼで活性体デスシクレソニドに変換される吸入プロドラッグ型ステロイド。強力なグルココルチコイド受容体作動により好中球性気道炎症・気道過敏性を抑制する。局所活性化・高い血漿蛋白結合・速やかな肝クリアランスにより、全身投与のデキサメタゾン/プレドニゾロンより全身性ステロイド曝露が少ない。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "Label regimen (343 µg ciclesonide per actuation, delivered through the EquiHaler nostril device): days 1-5 — 8 actuations q12h; days 6-10 — 12 actuations q24h (10-day course). Severe equine asthma; give alongside low-dust environmental management (soaked/steamed hay, non-straw bedding, maximal turnout).",
                "dosage_ja": "ラベル用法（1噴霧あたりシクレソニド343 µg、専用の鼻孔デバイスEquiHalerで投与）: 1-5日目 8噴霧 q12h、6-10日目 12噴霧 q24h（計10日間）。重度馬喘息に、低粉塵の環境管理（乾草の浸水/スチーム処理・藁以外の敷料・放牧時間の最大化）と併用する。",
                "notes": "Placebo-controlled efficacy in severe equine asthma (Lavoie 2019 JVIM). Transient, mild serum cortisol suppression can occur; as with any corticosteroid, weigh laminitis risk in EMS/PPID horses. For acute crises with marked respiratory distress, systemic dexamethasone plus inhaled bronchodilator remains the rescue — the inhaler is not a bronchodilator. Check competition medication rules (FEI). Not authorised in Japan.",
                "notes_ja": "重度馬喘息でプラセボ対照試験により有効性が示されている（Lavoie 2019 JVIM）。一過性・軽度の血清コルチゾール抑制がありうる。他のステロイドと同様、EMS/PPIDの馬では蹄葉炎リスクを考慮。著明な呼吸困難を伴う急性増悪のレスキューは全身デキサメタゾン＋吸入気管支拡張薬 — 本剤は気管支拡張薬ではない。競技規則（FEI）を確認。国内未承認。",
            },
            "dog": {
                "safe": False,
                "dosage": "Not licensed or established for dogs — use fluticasone via a spacer/mask for canine chronic bronchitis.",
                "dosage_ja": "犬には未承認・用量未確立 — 犬の慢性気管支炎にはスペーサー/マスク経由のフルチカゾンを使用。",
                "notes": "The EquiHaler device is designed for the equine nostril.",
                "notes_ja": "EquiHalerデバイスは馬の鼻孔専用に設計されている。",
            },
            "cat": {
                "safe": False,
                "dosage": "Not licensed or established for cats — use fluticasone via a spacer (e.g. AeroKat) for feline asthma.",
                "dosage_ja": "猫には未承認・用量未確立 — 猫喘息にはスペーサー（AeroKat等）経由のフルチカゾンを使用。",
                "notes": "Equine-specific device and dose.",
                "notes_ja": "馬専用のデバイス・用量。",
            },
        },
        "contraindications": "Hypersensitivity to ciclesonide; not a rescue bronchodilator for acute respiratory crisis. Caution in horses at high laminitis risk (EMS, PPID, history of laminitis).",
        "contraindications_ja": "シクレソニド過敏症。急性呼吸困難のレスキュー用気管支拡張薬ではない。蹄葉炎の高リスク馬（EMS・PPID・蹄葉炎既往）では慎重に。",
        "side_effects": [
            "Transient mild cortisol suppression",
            "Nasal irritation / head shaking during actuation",
        ],
        "side_effects_ja": ["一過性・軽度のコルチゾール抑制", "噴霧時の鼻刺激・頭振り"],
        "drug_interactions": [
            {
                "drug": "Dexamethasone / Prednisolone (systemic)",
                "effect": "Additive glucocorticoid effect — when bridging from systemic steroids, account for the combined steroid load (laminitis risk).",
                "effect_ja": "グルココルチコイド作用の相加 — 全身ステロイドから切り替える期間は合算のステロイド負荷（蹄葉炎リスク）を考慮。",
                "severity": "moderate",
            },
            {
                "drug": "Albuterol / Salmeterol (inhaled)",
                "effect": "Complementary: bronchodilator for symptom relief alongside the anti-inflammatory inhaler.",
                "effect_ja": "相補的: 抗炎症の吸入ステロイドに加え症状緩和の気管支拡張薬として併用。",
                "severity": "minor",
            },
        ],
        "references": [
            "Aservo EquiHaler (ciclesonide inhalation spray) US label / EU SPC, Boehringer Ingelheim Animal Health.",
            "Lavoie JP et al. Efficacy of inhaled ciclesonide for treatment of severe equine asthma. J Vet Intern Med 2019;33:1059-1066.",
            "Couetil LL et al. ACVIM Consensus Statement: Inflammatory airway disease of horses — revised consensus statement. J Vet Intern Med 2016;30:503-515.",
        ],
    },
]
