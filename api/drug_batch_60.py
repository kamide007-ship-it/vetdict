"""Drug batch 60 – referenced-but-absent agent surfaced by the 2026-09 audit (25th sweep).

A combined katakana + English drug-like-token sweep (dose-context filtered,
cross-checked against find_drugs_in_text on real context snippets) confirmed
the matcher is otherwise saturated and found one true monograph gap:

  - Methazolamide — the formulary's own glaucoma entries prescribe it by name
    with doses ("methazolamide 2-4 mg/kg PO q8-12h" in the canine glaucoma
    flagship, hedgehog glaucoma, and the small-mammal glaucoma guidance), and
    the canine entry even notes "fewer systemic side effects than
    acetazolamide" — yet only acetazolamide had a monograph. Methazolamide is
    the preferred systemic carbonic anhydrase inhibitor for canine glaucoma
    (Gelatt's Veterinary Ophthalmology; Plumb's 10th ed). Class-defining
    safety facts: no additive IOP benefit when combined with a topical CAI
    (dorzolamide/brinzolamide) — only additive toxicity; salicylate
    co-administration risks severe metabolic acidosis; contraindicated with
    significant hepatic disease (reduced ammonia excretion → hepatic
    encephalopathy risk).

References:
  - Plumb's Veterinary Drug Handbook 10th ed — methazolamide monograph
    (canine/feline dosing, interactions, contraindications).
  - Gelatt KN et al. Veterinary Ophthalmology 6th ed — systemic CAIs in
    canine glaucoma; methazolamide preferred over acetazolamide; lack of
    additive effect of systemic + topical CAI.
  - Carpenter's Exotic Animal Formulary 6th ed — small-mammal glaucoma
    therapy (systemic CAI extrapolation).
"""

DRUGS_BATCH_60 = [
    {
        "id": "methazolamide",
        "search_aliases": [
            "メタゾールアミド",
            "methazolamide",
        ],
        "name": "Methazolamide",
        "name_ja": "メタゾラミド",
        "category": "ophthalmic",
        "mechanism": "Systemic carbonic anhydrase inhibitor (CAI). Inhibits carbonic anhydrase in the ciliary body epithelium, reducing bicarbonate formation and thus aqueous humour production, lowering intraocular pressure. Better lipid solubility and CNS/ocular penetration than acetazolamide with less renal CA inhibition — hence fewer systemic side effects at antiglaucoma doses (Gelatt's Veterinary Ophthalmology 6th ed).",
        "mechanism_ja": "全身性炭酸脱水酵素阻害薬（CAI）。毛様体上皮の炭酸脱水酵素を阻害して房水産生を減らし、眼圧を低下させる。アセタゾラミドより脂溶性・眼内移行性が高く腎の炭酸脱水酵素阻害が少ないため、抗緑内障用量での全身性副作用が少ない（Gelatt's Veterinary Ophthalmology 6th ed）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Glaucoma: 2-4 mg/kg PO q8-12h (Plumb's 10th ed; Gelatt's 6th ed). Preferred systemic CAI in dogs — fewer systemic side effects than acetazolamide. Usually combined with topical prostaglandin (latanoprost) ± emergency mannitol for acute congestive glaucoma; monitor potassium and acid-base status on chronic therapy.",
                "dosage_ja": "緑内障: 2-4 mg/kg PO q8-12h（Plumb's 10th ed; Gelatt's 6th ed）。犬の全身性CAIとして第一選択 — アセタゾラミドより全身性副作用が少ない。通常は点眼プロスタグランジン（ラタノプロスト）と併用し、急性うっ血性緑内障ではマンニトールを併用。長期投与ではカリウム・酸塩基平衡をモニタリング。",
                "notes": "Do NOT add to a topical CAI (dorzolamide/brinzolamide): combining systemic and topical CAIs gives no additional IOP reduction, only additive toxicity — choose one route (Gelatt's 6th ed). Medical therapy is bridging/adjunctive: primary glaucoma ultimately requires surgery (laser cyclophotocoagulation, gonioimplant) or enucleation for blind painful eyes.",
                "notes_ja": "点眼CAI（ドルゾラミド/ブリンゾラミド）への上乗せは禁物: 全身性CAIと点眼CAIの併用は眼圧下降の追加効果がなく毒性のみ相加する — どちらか一方の経路を選択（Gelatt's 6th ed）。内科療法はブリッジ/補助であり、原発緑内障は最終的に手術（レーザー毛様体光凝固・ゴニオインプラント）または失明疼痛眼の眼球摘出が必要。",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q8-12h (Plumb's 10th ed) — use the low end and reassess: cats are more prone to CAI-induced hypokalemia and metabolic acidosis than dogs. Topical dorzolamide is generally preferred in cats; reserve systemic CAI for refractory cases.",
                "dosage_ja": "1-2 mg/kg PO q8-12h（Plumb's 10th ed）— 低用量から開始し再評価: 猫は犬よりCAIによる低カリウム血症・代謝性アシドーシスを起こしやすい。猫では点眼ドルゾラミドが一般に優先され、全身性CAIは難治例に温存する。",
                "notes": "Feline glaucoma is usually secondary (uveitis, lens luxation, neoplasia) — treat the underlying cause; monitor potassium on therapy.",
                "notes_ja": "猫の緑内障は続発性（ぶどう膜炎・水晶体脱臼・腫瘍）が大半 — 基礎疾患の治療が本体。投与中はカリウムをモニタリング。",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "2-4 mg/kg PO q8-12h (extrapolated from small-animal dosing; Carpenter 6th ed small-mammal glaucoma guidance). Monitor for metabolic acidosis and GI upset; enucleation is often the definitive welfare option for advanced exophthalmos/glaucoma in hedgehogs.",
                "dosage_ja": "2-4 mg/kg PO q8-12h（小動物用量からの外挿; Carpenter 6th ed の小型哺乳類緑内障ガイダンス）。代謝性アシドーシス・消化器症状をモニタリング。ハリネズミの進行した眼球突出/緑内障では眼球摘出が福祉的に確実な選択肢となることが多い。",
                "notes": "Referenced in this formulary's hedgehog glaucoma entry; small-mammal data are extrapolated — titrate to effect.",
                "notes_ja": "本辞書のハリネズミ緑内障エントリが参照する用量。小型哺乳類データは外挿のため効果をみながら漸増。",
            },
        },
        "side_effects": "Metabolic acidosis, hypokalemia, GI upset (vomiting, anorexia), lethargy, panting; rarely blood dyscrasias (sulfonamide derivative)",
        "side_effects_ja": "代謝性アシドーシス、低カリウム血症、消化器症状（嘔吐・食欲不振）、元気消失、パンティング。稀に血液異常（スルホンアミド誘導体）",
        "contraindications": "Significant hepatic disease (reduced ammonia excretion — hepatic encephalopathy risk), severe renal insufficiency, uncorrected hypokalemia/hyponatremia or metabolic acidosis, sulfonamide hypersensitivity. Do not combine with another carbonic anhydrase inhibitor (topical or systemic).",
        "contraindications_ja": "重度の肝疾患（アンモニア排泄低下 — 肝性脳症リスク）、重度の腎機能不全、未補正の低カリウム/低ナトリウム血症・代謝性アシドーシス、スルホンアミド過敏症。他の炭酸脱水酵素阻害薬（点眼・全身とも）との併用は不可。",
        "drug_interactions": [
            {
                "drug": "Dorzolamide/brinzolamide (topical CAI)",
                "effect": "No additive IOP reduction — additive systemic toxicity only; do not combine CAI routes",
                "effect_ja": "眼圧下降の追加効果なし — 全身毒性のみ相加。CAIの経路併用は不可",
                "severity": "moderate",
            },
            {
                "drug": "Aspirin (salicylates)",
                "effect": "Salicylates displace CAI from protein binding and reduce excretion — severe metabolic acidosis and CNS toxicity",
                "effect_ja": "サリチル酸がCAIの蛋白結合を置換し排泄を低下 — 重度の代謝性アシドーシス・中枢神経毒性",
                "severity": "major",
            },
            {
                "drug": "Furosemide (potassium-depleting diuretics)",
                "effect": "Additive hypokalemia — monitor potassium closely",
                "effect_ja": "低カリウム血症が相加 — カリウムを厳重モニタリング",
                "severity": "moderate",
            },
        ],
    },
]
