"""Drug batch 53 – referenced-but-absent agents surfaced by the 2026-09 audit (19th sweep).

The dose-context token audit (treatment texts cross-checked against
find_drugs_in_text) found that systemic magnesium — an emergency
antiarrhythmic, an electrolyte-replacement therapy and the classic equine
osmotic laxative — was absent from the formulary. Only the fish-bath entry
"Epsom Salt (Magnesium Sulfate)" existed, whose single species row is a
prolonged-immersion bath for dropsy; none of the 41 systemic references
(MgSO4 ×18, MgO ×19, マグネシウム補充 ×4) resolved to any monograph:

  - Equine colic entries instruct "MgSO4" / "鉱油またはMgSO4" as the osmotic
    laxative alongside mineral oil (AAEP; Blikslager in Reed & Bayly 4th ed).
  - The equine headshaking and hypomagnesemia entries prescribe oral
    magnesium maintenance ("MgO 10-20 g/day PO") and slow-IV magnesium for
    grass tetany ("希釈して15-30分かけて投与。急速投与は心停止リスク").
  - The bird egg-binding entry uses "MgSO4 1-5 mg/kg ICe" for concurrent
    magnesium deficiency.
  - RECOVER (Fletcher et al. J Vet Emerg Crit Care 2012; 2024 update) lists
    magnesium sulfate for torsades de pointes / refractory ventricular
    fibrillation in dogs and cats.

References:
  - Plumb's Veterinary Drug Handbook 10th ed — magnesium sulfate: dog/cat
    ventricular arrhythmia bolus 30 mg/kg (0.15-0.3 mEq/kg) slow IV over
    5-15 min; hypomagnesemia CRI 0.75-1 mEq/kg/day.
  - RECOVER Initiative (Fletcher 2012; Burkitt-Creedon 2024, JVECC) —
    magnesium for torsades de pointes and refractory VF/pulseless VT.
  - Reed & Bayly, Equine Internal Medicine 4th ed — hypomagnesemic tetany:
    dilute slow IV magnesium with ECG monitoring; large-colon impaction:
    MgSO4 0.5-1 g/kg via NGT in water q24h ≤3 days.
  - Schott (AAEP proceedings) — magnesium sulfate laxative dosing and
    enteritis/magnesium-toxicity cautions with repeated dosing.
  - Pickar-Oliver / Madigan, headshaking reviews — oral magnesium (MgO)
    supplementation reduces trigeminal excitability in some horses.
"""

DRUGS_BATCH_53: list[dict] = [
    {
        "id": "magnesium_sulfate",
        "search_aliases": [
            "硫酸マグネシウム",
            "マグネシウム硫酸塩",
            "MgSO4",
            "酸化マグネシウム",
            "マグネシウム補充",
            "Magnesium Sulfate",
            "Magnesium Oxide",
        ],
        "name": "Magnesium Sulfate (Systemic)",
        "name_ja": "硫酸マグネシウム（全身投与）",
        "category": "cardiovascular",
        "mechanism": "Essential intracellular cation and cofactor of Na+/K+-ATPase. Parenterally it stabilises cardiac cell membranes (antiarrhythmic of choice for torsades de pointes and refractory ventricular fibrillation — RECOVER), corrects hypomagnesemic tetany, and antagonises calcium at the neuromuscular junction. Orally (magnesium sulfate or magnesium oxide) it acts as a poorly-absorbed osmotic laxative drawing water into the intestinal lumen — the classic adjunct to mineral oil for equine large-colon impaction — and as maintenance magnesium supplementation.",
        "mechanism_ja": "細胞内主要陽イオンで Na+/K+-ATPase の補酵素。非経口では心筋細胞膜を安定化し（トルサード・ド・ポアント/難治性心室細動の第一選択 — RECOVER）、低Mg血症性テタニーを補正、神経筋接合部でカルシウムに拮抗する。経口（硫酸マグネシウム/酸化マグネシウム）では吸収されにくい浸透圧下剤として腸管内腔へ水分を引き込み（馬の大結腸便秘に対する鉱油と並ぶ古典的下剤）、維持的なマグネシウム補充にも用いる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Refractory ventricular arrhythmia / torsades de pointes: 30 mg/kg (0.15-0.3 mEq/kg) IV over 5-15 min (RECOVER; during CPR for refractory VF may be given over 1-2 min). Hypomagnesemia: 0.75-1 mEq/kg/day IV CRI in D5W, re-check serum Mg q12-24h.",
                "dosage_ja": "難治性心室性不整脈/トルサード・ド・ポアント: 30 mg/kg（0.15-0.3 mEq/kg）を5-15分かけて静注（RECOVER。CPR中の難治性心室細動では1-2分でも可）。低Mg血症: 0.75-1 mEq/kg/日 を5%ブドウ糖液に希釈してCRI、血清Mgを12-24時間毎に再検。",
                "notes": "Dilute for bolus use; rapid IV push in a perfusing patient causes hypotension, bradycardia and cardiac arrest. Monitor ECG during infusion. Reduce dose or avoid in renal failure (renally excreted).",
                "notes_ja": "ボーラスは希釈して投与。自己心拍のある患者への急速静注は低血圧・徐脈・心停止を起こす。投与中はECG監視。腎不全では減量または回避（腎排泄）。",
            },
            "cat": {
                "safe": True,
                "dosage": "Refractory ventricular arrhythmia / torsades: 0.15-0.3 mEq/kg (≈20-30 mg/kg) slow IV over 5-15 min. Hypomagnesemia (often with refractory hypokalemia): 0.75-1 mEq/kg/day IV CRI — correcting Mg is frequently required before potassium will normalise.",
                "dosage_ja": "難治性心室性不整脈/トルサード: 0.15-0.3 mEq/kg（約20-30 mg/kg）を5-15分かけて緩徐静注。低Mg血症（難治性低K血症の併発が多い）: 0.75-1 mEq/kg/日 CRI — Mgを補正しないとカリウムが正常化しないことが多い。",
                "notes": "Same ECG-monitored slow administration as dogs. Consider in DKA and refeeding cases with refractory hypokalemia.",
                "notes_ja": "犬と同様にECG監視下で緩徐投与。DKAやリフィーディングで低K血症が難治の際はMg欠乏を考慮。",
            },
            "horse": {
                "safe": True,
                "dosage": "Large-colon impaction (osmotic laxative): MgSO4 0.5-1 g/kg via nasogastric tube in 4-8 L water q24h, max 2-3 consecutive days (Reed & Bayly 4th ed) — confirm tube placement; do not combine with repeated doses if reflux present. Hypomagnesemic tetany: dilute magnesium solutions slow IV over 15-30 min to effect with ECG monitoring — rapid IV causes cardiac arrest. Headshaking / chronic supplementation: magnesium oxide (MgO) 10-20 g/horse/day PO in feed.",
                "dosage_ja": "大結腸便秘（浸透圧下剤）: 硫酸マグネシウム 0.5-1 g/kg を水4-8Lに溶解し経鼻胃チューブ投与 24時間毎、連続2-3日まで（Reed & Bayly 4th ed）— チューブ留置を必ず確認。胃逆流があれば反復投与しない。低Mg血症性テタニー: 希釈したMg溶液を15-30分かけてECG監視下で緩徐静注（急速静注は心停止）。ヘッドシェイキング/慢性補充: 酸化マグネシウム（MgO）10-20 g/頭/日 を飼料に混和。",
                "notes": "Repeated laxative dosing risks magnesium toxicity and enteritis — recheck before each dose. Oral MgO maintenance is the evidence-supported adjunct for trigeminal-mediated headshaking in some horses.",
                "notes_ja": "下剤の反復投与はMg中毒・腸炎のリスク — 毎回再評価してから投与。経口MgO維持は三叉神経介在性ヘッドシェイキングの一部の馬で有効性が支持される補助療法。",
            },
            "bird": {
                "safe": True,
                "dosage": "Concurrent magnesium deficiency (e.g. egg binding with hypocalcemia/hypomagnesemia): MgSO4 1-5 mg/kg ICe/IM once, with calcium and husbandry correction (Carpenter Exotic Animal Formulary).",
                "dosage_ja": "マグネシウム欠乏の併発時（低Ca/低Mgを伴う卵詰まり等）: 硫酸マグネシウム 1-5 mg/kg を体腔内/筋注で単回、カルシウム補正・飼育環境是正と併用（Carpenter Exotic Animal Formulary）。",
                "notes": "Adjunct only — calcium correction and husbandry remain primary for egg binding.",
                "notes_ja": "あくまで補助 — 卵詰まりの主治療はカルシウム補正と飼育環境の是正。",
            },
        },
        "side_effects": "Hypotension and bradycardia (IV, rate-dependent), flushing, loss of patellar reflexes → respiratory depression → cardiac arrest with overdose (hypermagnesemia), diarrhea (oral)",
        "side_effects_ja": "低血圧・徐脈（静注、速度依存性）、紅潮、過量で膝蓋腱反射消失→呼吸抑制→心停止（高Mg血症）、下痢（経口）",
        "contraindications": "Never give rapid IV push in a perfusing patient — dilute and give over 5-30 min with ECG monitoring. Renal failure: accumulates (renally excreted) — reduce dose or avoid. Antidote for magnesium toxicity is calcium gluconate slow IV. Do not run through the same line as calcium-containing fluids (calcium sulfate precipitation). Oral laxative use contraindicated with gastric reflux or suspected obstruction",
        "contraindications_ja": "自己心拍のある患者への急速静注は禁止 — 希釈し5-30分かけてECG監視下で投与。腎不全では蓄積（腎排泄）— 減量または回避。Mg中毒の解毒はグルコン酸カルシウム緩徐静注。カルシウム含有輸液と同一ラインで投与しない（硫酸カルシウム沈殿）。胃逆流・閉塞疑いでは経口下剤としての使用は禁忌",
        "drug_interactions": [
            {
                "drug": "Neuromuscular blockers (atracurium)",
                "effect": "Magnesium potentiates non-depolarizing neuromuscular blockade — prolonged paralysis; reduce blocker dose and monitor with a nerve stimulator",
                "effect_ja": "マグネシウムは非脱分極性神経筋遮断を増強 — 麻痺遷延。遮断薬を減量し神経刺激装置でモニタリング",
                "severity": "major",
            },
            {
                "drug": "Calcium-containing fluids (LRS, calcium gluconate)",
                "effect": "Physical incompatibility in the same line (calcium sulfate precipitate); pharmacologically calcium antagonises magnesium — used deliberately as the toxicity antidote",
                "effect_ja": "同一ラインで配合変化（硫酸カルシウム沈殿）。薬理学的にはカルシウムがマグネシウムに拮抗 — Mg中毒の解毒に意図的に利用",
                "severity": "moderate",
            },
            {
                "drug": "Aminoglycosides",
                "effect": "Additive neuromuscular blockade — respiratory weakness risk with high-dose magnesium",
                "effect_ja": "神経筋遮断の相加作用 — 高用量Mg併用で呼吸筋力低下のリスク",
                "severity": "moderate",
            },
            {
                "drug": "Digoxin",
                "effect": "Hypomagnesemia predisposes to digoxin toxicity; correct magnesium in digitalised patients with arrhythmias",
                "effect_ja": "低Mg血症はジゴキシン中毒の素因 — 不整脈のあるジギタリス投与患者ではMgを補正",
                "severity": "moderate",
            },
            {
                "drug": "CNS depressants / anesthetics",
                "effect": "Additive CNS and cardiovascular depression during magnesium infusion",
                "effect_ja": "Mg点滴中は中枢抑制・循環抑制が相加的に増強",
                "severity": "moderate",
            },
        ],
    },
]
