"""Curated agent-specific treatments for toxicosis records carrying the generic
decontamination template.

Two boilerplate treatment templates from an old enrichment run were stamped on
~82 toxicosis records:

* JA — 「…迅速な除染と支持療法が必要である。…催吐…胃洗浄…活性炭…特異的
  解毒剤がある場合は投与する（例：抗凝固性殺鼠剤にビタミンK1、アセトアミノ
  フェンにN-アセチルシステイン）…」
* EN — "Treatment of toxicosis follows the principles of decontamination,
  supportive care, and specific antidote administration when available…"

This is clinically wrong in both directions: it recommends emesis / gastric
lavage / activated charcoal universally (contraindicated for corrosives,
volatile oils and seizing patients; absurd for a fish ammonia burn or a
constipated megacolon cat) and it names the *wrong* antidotes for most of the
affected agents (cat lily → fluids-before-anuria, ethylene glycol → fomepizole
within 3 h, ivermectin → intravenous lipid emulsion, bromethalin → no antidote
at all).

For records whose species module carries a curated treatment, the fix is the
template guard in ``migrate_to_sqlite`` / ``helpers`` (the template may never
replace informative text). For records where the template is the ONLY content
(module templated or absent), this library supplies an evidence-based,
agent- and species-specific protocol.

Resolution is by EXACT (species, English name) key — the affected set is a
closed list from the audit, so no substring matching (and none of its collision
risk) is involved.

References: Plumb's Veterinary Drug Handbook 10th ed; Peterson & Talcott,
Small Animal Toxicology 3rd ed; ASPCA Animal Poison Control Center;
Carpenter, Exotic Animal Formulary 6th ed; Mader, Reptile Medicine and Surgery
3rd ed; Ritchie & Harrison, Avian Medicine; Quesenberry & Carpenter, Ferrets,
Rabbits, and Rodents 4th ed; Connally et al. JAVMA 2010 (feline fomepizole);
Fitzgerald, Vet Clin North Am 2010 (lily); Gwaltney-Brant & Meadows,
Vet Clin North Am 2018 (intravenous lipid emulsion).
"""

from __future__ import annotations

# Fingerprints of the generic toxin-decontamination treatment template.
TOXIN_TREATMENT_JA_SIG = "特異的解毒剤がある場合は投与する（例：抗凝固性殺鼠剤にビタミンK1"
TOXIN_TREATMENT_EN_SIG = "Treatment of toxicosis follows the principles of decontamination"


def _t(ja: str, en: str) -> dict:
    return {"treatment_ja": ja, "treatment": en}


# ---------------------------------------------------------------- cat agents
_CAT_ACETAMINOPHEN = _t(
    "猫のアセトアミノフェン中毒は超緊急（治療域なし — 10 mg/kgでも中毒）。解毒の主軸はN-アセチルシステイン（NAC）: "
    "140 mg/kg PO/IV（希釈5%で緩徐静注）負荷→70 mg/kg q6h×7回以上。メトヘモグロビン血症にはアスコルビン酸 30 mg/kg PO/IV q6h併用、"
    "酸素供給、重度貧血・ハインツ小体性溶血には輸血。肝保護にSAMe 90 mg/頭 PO q24h。摂取2時間以内かつ無症状であれば催吐・活性炭 1-2 g/kg を先行。"
    "追加のアセトアミノフェン投与は絶対禁止。チョコレート色の粘膜・血液（メトヘモグロビン）、顔面・前肢浮腫が特徴的。"
    "48-72時間の入院モニタリング（PCV・メトヘモグロビン・肝酵素）。（Plumb's 10th ed; Peterson & Talcott 3rd ed）",
    "Feline acetaminophen toxicosis is a critical emergency (no safe dose — toxicity from 10 mg/kg). "
    "The mainstay is N-acetylcysteine: 140 mg/kg PO/IV (dilute to 5%, slow IV) loading, then 70 mg/kg q6h for at least 7 doses. "
    "For methemoglobinemia add ascorbic acid 30 mg/kg PO/IV q6h, provide oxygen, and transfuse for severe Heinz-body hemolytic anemia. "
    "Hepatoprotection with SAMe 90 mg/cat PO q24h. If within 2 h of ingestion and asymptomatic, induce emesis and give activated charcoal 1-2 g/kg first. "
    "Never give further acetaminophen. Monitor PCV, methemoglobin and liver enzymes in hospital for 48-72 h. (Plumb's 10th ed; Peterson & Talcott 3rd ed)",
)

_CAT_LILY = _t(
    "ユリ中毒は猫の最重要中毒緊急 — 全ての部位（花粉・葉・花瓶の水も）が腎毒性で、安全量はない。"
    "①除染: 摂取1-2時間以内なら催吐（デクスメデトミジン 7 μg/kg IM等）、活性炭 1-2 g/kg PO、被毛の花粉はシャンプーで除去。"
    "②輸液が予後を決める: 乏尿・無尿になる前に等張晶質液 2-3倍維持量（約4-6 mL/kg/h）IVを48-72時間 — 摂取後18時間以内の開始で予後良好（Fitzgerald 2010）。"
    "③モニタリング: クレアチニン・BUN・尿比重・尿量を q12-24h×72時間（腎数値は12-30時間で上昇開始）。"
    "④無尿に進行した場合は血液透析/腹膜透析のみが救命手段。摂取が疑わしいだけでも輸液入院が正当化される。（Fitzgerald JVECC 2010; Peterson & Talcott 3rd ed）",
    "Lily ingestion is the premier feline toxicologic emergency — every part of the plant (pollen, leaves, even vase water) is nephrotoxic with no safe dose. "
    "(1) Decontaminate: emesis within 1-2 h (dexmedetomidine 7 µg/kg IM), activated charcoal 1-2 g/kg PO, bathe pollen off the coat. "
    "(2) Fluids determine outcome: isotonic crystalloids at 2-3× maintenance (≈4-6 mL/kg/h) IV for 48-72 h started BEFORE oliguria — starting within 18 h of ingestion carries an excellent prognosis (Fitzgerald 2010). "
    "(3) Monitor creatinine, BUN, USG and urine output q12-24h for 72 h (renal values rise at 12-30 h). "
    "(4) Once anuric, hemodialysis/peritoneal dialysis is the only salvage. Suspected exposure alone justifies hospitalization on fluids. (Fitzgerald JVECC 2010; Peterson & Talcott 3rd ed)",
)

_CAT_EG = _t(
    "エチレングリコール中毒は分単位の救急 — 猫は犬より治療域が狭く、解毒開始は摂取後3時間以内が必須（Connally 2010）。"
    "①解毒: フォメピゾール猫用高用量プロトコル 125 mg/kg IV負荷→31.25 mg/kg を12・24・36時間後（犬用量では不十分）。"
    "入手不能時は20%エタノール 5 mL/kg IV q6h（鎮静深度に注意）。②代謝性アシドーシスに炭酸水素Na（不足量=0.3×BW×BE）。"
    "③輸液で利尿維持。④シュウ酸カルシウム結晶尿・高K・無尿は確立したAKIを示し、透析以外の救命は困難。"
    "診断は血清EG測定・浸透圧ギャップ・エコー（腎皮質高エコー）。予後は治療開始時間が全て。（Connally JAVMA 2010; Plumb's 10th ed）",
    "Ethylene glycol toxicosis is a minute-by-minute emergency — the feline treatment window closes 3 h post-ingestion (Connally 2010). "
    "(1) Antidote: feline high-dose fomepizole 125 mg/kg IV loading, then 31.25 mg/kg at 12, 24 and 36 h (canine dosing is insufficient in cats). "
    "If unavailable: 20% ethanol 5 mL/kg IV q6h (monitor sedation depth). (2) Sodium bicarbonate for metabolic acidosis (deficit = 0.3 × BW × base excess). "
    "(3) IV fluids to maintain diuresis. (4) Calcium oxalate crystalluria, hyperkalemia and anuria indicate established AKI — salvage then requires dialysis. "
    "Diagnosis: serum EG assay, osmolal gap, renal cortical hyperechogenicity. Time-to-treatment defines prognosis. (Connally JAVMA 2010; Plumb's 10th ed)",
)

_CAT_CHOCOLATE = _t(
    "猫のチョコレート（メチルキサンチン）中毒: 猫は犬より感受性が高いが嗜好性が低いため稀。"
    "①除染: 摂取2時間以内かつ無症状なら催吐（デクスメデトミジン 7 μg/kg IM）、活性炭 1-2 g/kg PO を腸肝循環対策に q8-12h 反復。"
    "②不整脈: 頻脈性→エスモロール 0.05-0.1 mg/kg 緩徐IV/プロプラノロール 0.02-0.06 mg/kg 緩徐IV、心室性→リドカイン（猫は神経毒性に注意し 0.25-0.5 mg/kg 緩徐IV）。"
    "③痙攣・振戦: ジアゼパム 0.5 mg/kg IV、無効時レベチラセタム。④輸液で排泄促進、尿カテーテル留置（膀胱壁からのメチルキサンチン再吸収防止）。"
    "半減期が長く24-72時間の心電図モニタリング。（Plumb's 10th ed; Peterson & Talcott 3rd ed）",
    "Feline chocolate (methylxanthine) toxicosis: cats are more sensitive than dogs but rarely ingest it. "
    "(1) Decontaminate: emesis within 2 h if asymptomatic (dexmedetomidine 7 µg/kg IM); activated charcoal 1-2 g/kg PO repeated q8-12h for enterohepatic recirculation. "
    "(2) Arrhythmias: tachyarrhythmia → esmolol 0.05-0.1 mg/kg slow IV or propranolol 0.02-0.06 mg/kg slow IV; ventricular → lidocaine with feline caution (0.25-0.5 mg/kg slow IV). "
    "(3) Seizures/tremors: diazepam 0.5 mg/kg IV, then levetiracetam if refractory. (4) IV fluids to promote excretion and an indwelling urinary catheter (prevents methylxanthine reabsorption across the bladder wall). "
    "ECG monitoring for 24-72 h. (Plumb's 10th ed; Peterson & Talcott 3rd ed)",
)

_CAT_IVERMECTIN = _t(
    "猫のイベルメクチン中毒に特異的解毒剤はない。第一選択の補助療法は静注脂肪乳剤（ILE 20%）: "
    "1.5 mL/kg IVボーラス→0.25 mL/kg/分×30-60分（親油性薬物を血中に隔離 — Gwaltney-Brant 2018）。"
    "重度昏迷・呼吸抑制には挿管・人工換気を含む集中支持療法（体温維持・眼保護・体位変換・栄養）を数日〜数週継続すれば回復可能。"
    "摂取直後なら活性炭 1-2 g/kg を反復（腸肝循環）。痙攣にはジアゼパム（GABA作動性増強の理論的懸念はあるが臨床上は第一選択）。"
    "以後のマクロサイクリックラクトン系は使用しない。（Plumb's 10th ed; Gwaltney-Brant & Meadows 2018）",
    "There is no specific antidote for feline ivermectin toxicosis. First-line adjunct is 20% intravenous lipid emulsion: "
    "1.5 mL/kg IV bolus then 0.25 mL/kg/min for 30-60 min (sequesters the lipophilic drug — Gwaltney-Brant 2018). "
    "Severe stupor/respiratory depression: intensive supportive care including intubation and ventilation, thermoregulation, eye lubrication, repositioning and nutrition — recovery over days to weeks is possible. "
    "Repeated activated charcoal 1-2 g/kg early (enterohepatic recirculation). Diazepam for seizures. "
    "Avoid all further macrocyclic lactones. (Plumb's 10th ed; Gwaltney-Brant & Meadows 2018)",
)

_CAT_LEAD = _t(
    "猫の鉛中毒: ①鉛源の特定と除去が先決 — X線で消化管内金属片を確認し、残存すればキレート前に内視鏡/外科的に摘出（キレート中の吸収促進を防ぐ）。"
    "②キレーション: CaEDTA 25 mg/kg SC q6h（生食で2-4 mg/mLに希釈）×5日、または succimer（DMSA）10 mg/kg PO q8h×5日→q12h×2週（経口・腎毒性が少なく外来可）。"
    "③痙攣にはジアゼパム 0.5 mg/kg IV、脳浮腫にマンニトール。④治療前後の血中鉛値で効果判定、環境調査（塗料・カーテンウェイト・釣り錘）。"
    "（Plumb's 10th ed; Peterson & Talcott 3rd ed）",
    "Feline lead toxicosis: (1) identify and remove the source first — radiograph for GI metal and retrieve endoscopically/surgically BEFORE chelation (chelators enhance GI lead absorption). "
    "(2) Chelation: CaEDTA 25 mg/kg SC q6h (diluted to 2-4 mg/mL in saline) for 5 days, or succimer (DMSA) 10 mg/kg PO q8h ×5 d then q12h ×2 wk (oral, less nephrotoxic, outpatient-friendly). "
    "(3) Diazepam 0.5 mg/kg IV for seizures; mannitol for cerebral edema. (4) Pre/post blood lead levels and an environmental survey (paint, curtain weights, fishing sinkers). "
    "(Plumb's 10th ed; Peterson & Talcott 3rd ed)",
)

_CAT_MARIJUANA = _t(
    "猫の大麻（THC）中毒は支持療法で予後良好（死亡は稀）。摂取直後で無症状なら催吐、その後活性炭 1-2 g/kg（THCの腸肝循環対策に反復可）。"
    "神経抑制が主体: 保温・静かな暗い環境・転倒防止、徐脈は必要時アトロピン。重度昏迷・徐脈には静注脂肪乳剤（ILE 20%: 1.5 mL/kg ボーラス→0.25 mL/kg/分×30-60分）が回復を早める。"
    "輸液で循環維持。THC代謝物は脂溶性で症状は24-72時間持続しうる。特異的拮抗薬はない。合成カンナビノイドはより重篤化しやすい。"
    "（Plumb's 10th ed; Peterson & Talcott 3rd ed）",
    "Feline marijuana (THC) toxicosis carries a good prognosis with supportive care (death is rare). Emesis if immediately post-ingestion and asymptomatic, then activated charcoal 1-2 g/kg (repeatable — enterohepatic recirculation). "
    "CNS depression predominates: thermoregulation, a quiet dark environment, fall prevention; atropine for symptomatic bradycardia. For severe stupor, 20% intravenous lipid emulsion (1.5 mL/kg bolus then 0.25 mL/kg/min ×30-60 min) hastens recovery. "
    "IV fluids for perfusion. Signs may persist 24-72 h (lipophilic metabolites). No specific antagonist exists; synthetic cannabinoids cause more severe signs. "
    "(Plumb's 10th ed; Peterson & Talcott 3rd ed)",
)

_CAT_METALDEHYDE = _t(
    "猫のメタアルデヒド（ナメクジ駆除剤）中毒 — 「shake and bake」: 特異的解毒剤はなく、振戦・痙攣と高体温の制御が生死を分ける。"
    "①振戦・痙攣: メトカルバモール 55-220 mg/kg 緩徐IV（第一選択）、ジアゼパム 0.5 mg/kg IV、難治例はプロポフォールCRI/全身麻酔。"
    "②高体温: 41℃超は積極的冷却（濡れタオル+送風）、39.5℃で中止。③除染: 振戦発現後の催吐は誤嚥リスクで禁忌 — 麻酔下胃洗浄+活性炭 1-2 g/kg。"
    "④輸液・アシドーシス補正。肝障害が2-3日後に顕在化しうるため肝酵素を72時間モニタリング。（Plumb's 10th ed; Peterson & Talcott 3rd ed）",
    "Feline metaldehyde (slug bait) toxicosis — 'shake and bake': no antidote exists; controlling tremors/seizures and hyperthermia decides the outcome. "
    "(1) Tremors/seizures: methocarbamol 55-220 mg/kg slow IV (first line), diazepam 0.5 mg/kg IV, refractory → propofol CRI/general anesthesia. "
    "(2) Hyperthermia: active cooling above 41°C (wet towels + fan), stop at 39.5°C. (3) Decontamination: emesis is CONTRAINDICATED once tremoring — gastric lavage under anesthesia plus activated charcoal 1-2 g/kg. "
    "(4) Fluids and acid-base correction. Monitor liver enzymes 72 h (delayed hepatopathy). (Plumb's 10th ed; Peterson & Talcott 3rd ed)",
)

_CAT_ONION = _t(
    "猫のネギ属（タマネギ・ニンニク・ニラ）中毒: 猫は全動物種で最も感受性が高い（5 g/kgで溶血）。"
    "①除染: 摂取2時間以内なら催吐+活性炭 1-2 g/kg。②溶血は摂取後1-5日遅発 — PCV・ハインツ小体・血漿色を最低5-7日間連日モニタリング。"
    "③輸血: PCV<15%または急速低下で全血/濃厚赤血球。④輸液でヘモグロビン尿からの腎保護（尿量維持）。⑤酸素供給。"
    "加熱・乾燥でも毒性（有機硫黄化合物）は失活しない。特異的解毒剤はない。（Plumb's 10th ed; Cope 2005）",
    "Feline Allium (onion/garlic/chive) toxicosis: cats are the most sensitive of all species (hemolysis from 5 g/kg). "
    "(1) Decontaminate: emesis + activated charcoal 1-2 g/kg within 2 h. (2) Hemolysis is DELAYED 1-5 days — monitor PCV, Heinz bodies and plasma color daily for at least 5-7 days. "
    "(3) Transfuse whole blood/pRBC if PCV <15% or falling rapidly. (4) IV fluids to protect kidneys from hemoglobinuria. (5) Oxygen support. "
    "Cooking or drying does NOT inactivate the organosulfur toxins. No specific antidote. (Plumb's 10th ed; Cope 2005)",
)

_CAT_OP = _t(
    "猫の有機リン中毒（猫は特に感受性が高い — クロルピリホス等）: ①ムスカリン症状（流涎・縮瞳・徐脈・気道分泌）にアトロピン 0.2-0.5 mg/kg（1/4をIV、残りをIM/SC）を効果まで滴定。"
    "②ニコチン症状（振戦・筋力低下）にプラリドキシム（2-PAM）20 mg/kg IM q8-12h — エージング前の早期投与が有効。"
    "③痙攣にジアゼパム。④経皮曝露は食器用洗剤で全身洗浄（術者は手袋）。⑤フェノチアジン系・スキサメトニウムは禁忌。"
    "猫は数日〜数週後の遅発性ニューロパチー・慢性中間症候群にも注意。（Plumb's 10th ed; Peterson & Talcott 3rd ed）",
    "Feline organophosphate toxicosis (cats are notably sensitive — e.g. chlorpyrifos): (1) atropine 0.2-0.5 mg/kg (¼ IV, remainder IM/SC) titrated to effect for muscarinic signs (salivation, miosis, bradycardia, bronchial secretions). "
    "(2) Pralidoxime (2-PAM) 20 mg/kg IM q8-12h for nicotinic signs — effective when started before enzyme aging. "
    "(3) Diazepam for seizures. (4) Dermal exposure: bathe whole-body with dishwashing detergent (handler gloves). (5) Phenothiazines and succinylcholine are contraindicated. "
    "Watch for delayed neuropathy and intermediate syndrome over days-weeks. (Plumb's 10th ed; Peterson & Talcott 3rd ed)",
)

_CAT_SALT = _t(
    "猫の食塩中毒（高Na血症）: 治療原則は「急速に上がったNaは急速に、緩徐に上がったNaは緩徐に補正」。"
    "慢性（>24-48時間）または不明の場合、血清Na低下速度は0.5 mEq/L/h以下（10-12 mEq/L/日以下） — 速すぎる補正は脳浮腫を起こす。"
    "①血清Na・電解質を測定し、自由水欠乏量= 0.6×BW×(現在Na/目標Na − 1) を計算。②D5WまたはNaCl 0.45%を緩徐に投与し、Naをq2-4hで再測定。"
    "③意識レベル悪化（補正中の脳浮腫）にはマンニトール 0.5-1 g/kg IV。④経口摂取可能なら少量頻回の飲水。痙攣にはジアゼパム。"
    "（Plumb's 10th ed; DiBartola, Fluid Therapy 4th ed）",
    "Feline salt toxicosis (hypernatremia): correct at the rate it developed — rapidly acquired Na may be corrected quickly, chronic (>24-48 h) or unknown-duration hypernatremia no faster than 0.5 mEq/L/h (≤10-12 mEq/L/day); over-rapid correction causes cerebral edema. "
    "(1) Measure serum Na and calculate free-water deficit = 0.6 × BW × (current Na/target Na − 1). (2) Replace slowly with D5W or 0.45% NaCl, rechecking Na q2-4h. "
    "(3) Mannitol 0.5-1 g/kg IV for deteriorating mentation during correction. (4) Small frequent oral water if able; diazepam for seizures. "
    "(Plumb's 10th ed; DiBartola, Fluid Therapy 4th ed)",
)

_CAT_TEN = _t(
    "猫の中毒性表皮壊死症（TEN）は薬物有害反応であり中毒（毒物摂取）ではない — 除染は適応外。"
    "①最重要: 被疑薬（数週間以内に開始した抗菌薬・NSAIDs等すべて）の即時中止。②熱傷に準じた支持療法: 積極的輸液・膠質液、疼痛管理（ブプレノルフィン 0.02 mg/kg）、"
    "非固着性ドレッシングでの創傷管理、体温維持。③敗血症が確認された場合のみ抗菌薬（予防投与は避け培養に基づく）。"
    "④難治例にヒト免疫グロブリン（hIVIG）0.5-1.5 g/kg IV 単回。⑤食道炎回避と栄養に食道瘻チューブ。ステロイドの有効性は確立していない。"
    "死亡率は高く、皮膚剥離面積が予後指標。（Muller & Kirk 7th ed; Yager, Vet Dermatol 2014）",
    "Feline toxic epidermal necrolysis (TEN) is an adverse DRUG reaction, not a poisoning — decontamination has no role. "
    "(1) Most important: immediately withdraw every suspect drug started within recent weeks (antibiotics, NSAIDs etc.). "
    "(2) Burn-equivalent supportive care: aggressive fluids ± colloids, analgesia (buprenorphine 0.02 mg/kg), non-adherent wound dressings, thermoregulation. "
    "(3) Antibiotics only for documented sepsis (culture-guided, not prophylactic). (4) Refractory cases: hIVIG 0.5-1.5 g/kg IV once. "
    "(5) Esophagostomy tube for nutrition. Corticosteroid benefit is unproven. Mortality is high; detached skin area predicts outcome. "
    "(Muller & Kirk 7th ed; Yager, Vet Dermatol 2014)",
)

_CAT_ZINC = _t(
    "猫の亜鉛中毒: ①亜鉛源の除去が治療の中心 — X線で胃内金属異物（コイン・金具）を確認し内視鏡/外科的に摘出。"
    "摘出後は血中亜鉛が速やかに低下するためキレーションは通常不要（遷延例のみCaEDTA）。"
    "②胃酸抑制（酸性環境で亜鉛溶出が促進）: オメプラゾール 1 mg/kg PO/IV q24h。③溶血性貧血: PCVモニタリング、PCV<15%で輸血。"
    "④輸液でヘモグロビン尿からの腎保護。⑤膵炎併発の監視（亜鉛は膵毒性）。（Plumb's 10th ed; Peterson & Talcott 3rd ed）",
    "Feline zinc toxicosis: (1) source removal IS the treatment — radiograph for gastric metallic foreign bodies (coins, hardware) and retrieve endoscopically/surgically. "
    "Blood zinc falls rapidly after removal, so chelation is usually unnecessary (CaEDTA only for persistent cases). "
    "(2) Gastric acid suppression (acid accelerates zinc elution): omeprazole 1 mg/kg PO/IV q24h. (3) Hemolytic anemia: monitor PCV, transfuse below 15%. "
    "(4) IV fluids to protect kidneys from hemoglobinuria. (5) Watch for concurrent pancreatitis (zinc is pancreatotoxic). (Plumb's 10th ed; Peterson & Talcott 3rd ed)",
)

_CAT_BROMETHALIN = _t(
    "猫のブロメタリン（神経毒性殺鼠剤）中毒に解毒剤はない — 早期の積極的除染が唯一の有効介入。"
    "猫は最も感受性の高い動物種（最小致死量約0.24 mg/kg）。①摂取直後: 催吐+活性炭 1-2 g/kg を q8h×2-3日反復（顕著な腸肝循環）。"
    "②脳浮腫: マンニトール 0.5-1 g/kg IV 15-20分かけて、高張食塩水7.2% 2-4 mL/kg、頭部挙上30度。"
    "③痙攣: ジアゼパム→レベチラセタム→プロポフォールCRI。④支持療法（褥瘡予防・栄養・膀胱管理）。"
    "麻痺・痙攣に進行した場合の予後は不良だが、数週間の看護で回復した報告もある。（Plumb's 10th ed; Peterson & Talcott 3rd ed）",
    "No antidote exists for feline bromethalin (neurotoxic rodenticide) toxicosis — early aggressive decontamination is the only effective intervention. "
    "Cats are the most sensitive species (minimum lethal dose ≈0.24 mg/kg). (1) Immediately post-ingestion: emesis + activated charcoal 1-2 g/kg repeated q8h for 2-3 days (marked enterohepatic recirculation). "
    "(2) Cerebral edema: mannitol 0.5-1 g/kg IV over 15-20 min, 7.2% hypertonic saline 2-4 mL/kg, 30° head elevation. "
    "(3) Seizures: diazepam → levetiracetam → propofol CRI. (4) Nursing care (decubitus prevention, nutrition, bladder management). "
    "Prognosis is poor once paralysis/seizures develop, though recovery after weeks of care is reported. (Plumb's 10th ed; Peterson & Talcott 3rd ed)",
)

_CAT_NSAID = _t(
    "猫のNSAID中毒（猫はグルクロン酸抱合能が低く犬より遥かに感受性が高い）: "
    "①除染: 摂取2時間以内なら催吐、活性炭 1-2 g/kg（腸肝循環する薬物では q8h 反復）。"
    "②腎保護: 等張晶質液 2倍維持量 IV×48-72時間、腎数値（クレアチニン・SDMA）と尿量を72時間モニタリング。"
    "③消化管保護: オメプラゾール 1 mg/kg q24h + スクラルファート 250 mg/頭 PO q8-12h、ミソプロストール 2-5 μg/kg PO q8h。"
    "④消化管穿孔の徴候（急性腹症・敗血症）を監視。⑤追加のNSAIDs・ステロイドは絶対併用禁止。（Plumb's 10th ed; ISFM consensus 2010）",
    "Feline NSAID toxicosis (cats glucuronidate poorly and are far more sensitive than dogs): "
    "(1) Decontaminate: emesis within 2 h, activated charcoal 1-2 g/kg (repeat q8h for enterohepatically recirculated drugs). "
    "(2) Renal protection: isotonic crystalloids at 2× maintenance IV for 48-72 h; monitor creatinine/SDMA and urine output for 72 h. "
    "(3) GI protection: omeprazole 1 mg/kg q24h + sucralfate 250 mg/cat PO q8-12h + misoprostol 2-5 µg/kg PO q8h. "
    "(4) Watch for GI perforation (acute abdomen, sepsis). (5) Never combine with further NSAIDs or corticosteroids. (Plumb's 10th ed; ISFM consensus 2010)",
)

_CAT_ANTICOAG = _t(
    "猫の抗凝固性殺鼠剤中毒: 解毒剤はビタミンK1 — 3-5 mg/kg/日 PO 分2、脂肪を含む食事と共に（吸収向上）、第2世代製剤では4週間継続。"
    "①摂取4時間以内: 催吐+活性炭、その後「予防的K1を4週間」または「48-72時間後にPT測定し延長時のみ治療」のいずれかを選択。"
    "②活動性出血: ビタミンK1は効果発現に6-12時間かかるため、新鮮凍結血漿 10-20 mL/kg または全血輸血で凝固因子を直接補充。"
    "③K1静注はアナフィラキシー様反応のため避ける（PO/SC）。④投与終了48-72時間後にPT再検 — 延長していれば2週間延長。"
    "（Plumb's 10th ed; Peterson & Talcott 3rd ed）",
    "Feline anticoagulant rodenticide toxicosis: the antidote is vitamin K1 — 3-5 mg/kg/day PO divided q12h WITH a fatty meal (improves absorption), continued 4 weeks for second-generation agents. "
    "(1) Within 4 h of ingestion: emesis + charcoal, then either prophylactic K1 ×4 weeks or a PT check at 48-72 h treating only if prolonged. "
    "(2) Active bleeding: K1 takes 6-12 h to act — replace factors directly with fresh frozen plasma 10-20 mL/kg or whole blood. "
    "(3) Avoid IV K1 (anaphylactoid reactions) — use PO/SC. (4) Recheck PT 48-72 h after the last dose; extend 2 weeks if prolonged. "
    "(Plumb's 10th ed; Peterson & Talcott 3rd ed)",
)

_CAT_TEA_TREE = _t(
    "猫のティーツリーオイル（テルペン）中毒: 主経路は経皮＋グルーミング摂取。"
    "①催吐は禁忌 — 揮発性オイルの誤嚥性肺炎リスク。②皮膚除染が最優先: 食器用洗剤で繰り返し洗浄（低体温に注意し温水・保温）。"
    "③支持療法: 輸液、保温、振戦にはメトカルバモール 55-110 mg/kg 緩徐IV、痙攣にジアゼパム。"
    "④重度の神経抑制には静注脂肪乳剤（ILE 20%: 1.5 mL/kg→0.25 mL/kg/分×30-60分 — テルペンは高脂溶性）。"
    "⑤肝酵素を数日間モニタリング。「天然」でも猫に安全ではないことを飼い主に教育。（Khan JAVMA 2014; Plumb's 10th ed）",
    "Feline tea tree oil (terpene) toxicosis: exposure is dermal plus grooming ingestion. "
    "(1) Emesis is CONTRAINDICATED — volatile oil aspiration pneumonia risk. (2) Dermal decontamination first: repeated bathing with dishwashing detergent (warm water, prevent hypothermia). "
    "(3) Supportive: fluids, warmth, methocarbamol 55-110 mg/kg slow IV for tremors, diazepam for seizures. "
    "(4) Severe CNS depression: 20% intravenous lipid emulsion (1.5 mL/kg then 0.25 mL/kg/min ×30-60 min — terpenes are highly lipophilic). "
    "(5) Monitor liver enzymes for several days. Educate owners that 'natural' is not feline-safe. (Khan JAVMA 2014; Plumb's 10th ed)",
)

_CAT_MEGACOLON = _t(
    "猫の巨大結腸症/重度便秘の治療（中毒ではない — 催吐・活性炭は適応外）: "
    "①評価: X線（便塊量・骨盤狭窄の有無）、脱水・電解質（低K・脱水が腸運動をさらに低下）。"
    "②内科管理: 輸液で脱水補正、ラクツロース 0.5-1 mL/kg PO q8-12h、ポリエチレングリコール（MiraLAX）1/4-1 tsp PO q12h、"
    "シサプリド 0.5-1 mg/kg PO q8-12h（結腸運動促進）、缶詰ベースの可溶性繊維食または低残渣食。"
    "③宿便: 全身麻酔下で温水浣腸+用手摘便（複数回に分けて粘膜損傷を回避）。"
    "④慢性再発性巨大結腸症: 結腸亜全摘出術（奏効率85-90%）。（Washabau, Gastroenterology; AAFP）",
    "Treatment of feline megacolon/severe constipation (NOT a poisoning — emesis and charcoal have no role): "
    "(1) Assess: radiographs (fecal load, pelvic canal narrowing), hydration and electrolytes (hypokalemia and dehydration further impair motility). "
    "(2) Medical: rehydrate, lactulose 0.5-1 mL/kg PO q8-12h, polyethylene glycol (MiraLAX) ¼-1 tsp PO q12h, cisapride 0.5-1 mg/kg PO q8-12h (colonic prokinetic), canned soluble-fiber or low-residue diet. "
    "(3) Impaction: warm-water enemas plus manual evacuation under general anesthesia (staged to avoid mucosal trauma). "
    "(4) Chronic recurrent megacolon: subtotal colectomy (85-90% success). (Washabau; AAFP)",
)

# ---------------------------------------------------------- non-cat agents
_BIRD_LEAD = _t(
    "鳥の鉛中毒（慢性型含む）: ①キレーション: CaEDTA 30-35 mg/kg IM q12h×5日→3-4日休薬→症状消失まで反復、"
    "または外来管理向けに DMSA（サクシマー）25-35 mg/kg PO q12h×10日（安全域が狭く80 mg/kg超で死亡例 — Denver 2000）。"
    "②X線で筋胃内金属片を確認 — 残存例は嗉嚢/筋胃洗浄、内視鏡、グリットや psyllium・ピーナッツバター給餌で排出促進。"
    "③痙攣にはジアゼパム/ミダゾラム 0.5-1 mg/kg IM。④輸液・ガベージ給餌・保温の支持療法。"
    "⑤環境調査（塗料・カーテンウェイト・ステンドグラス・おもちゃ）。血中鉛>20 μg/dLで疑い、>50で確定的。"
    "（Carpenter 6th ed; Ritchie & Harrison; Denver JAVMA 2000）",
    "Avian lead toxicosis (including chronic form): (1) chelation — CaEDTA 30-35 mg/kg IM q12h ×5 d, rest 3-4 d, repeat until asymptomatic; "
    "or DMSA (succimer) 25-35 mg/kg PO q12h ×10 d for outpatients (narrow margin — deaths above 80 mg/kg, Denver 2000). "
    "(2) Radiograph for ventricular metal — persistent densities: crop/ventricular lavage, endoscopy, or grit/psyllium/peanut-butter feeding to promote passage. "
    "(3) Seizures: diazepam/midazolam 0.5-1 mg/kg IM. (4) Fluids, gavage feeding and warmth. "
    "(5) Environmental survey (paint, curtain weights, stained glass, toys). Blood lead >20 µg/dL suspicious, >50 diagnostic. "
    "(Carpenter 6th ed; Ritchie & Harrison; Denver JAVMA 2000)",
)

_SMALL_MAMMAL_ZINC = _t(
    "小型哺乳類（デグー等）の亜鉛中毒: ①亜鉛源（亜鉛メッキのケージ金網・ボルト・コイン）の特定と除去が治療の中心 — X線で消化管内金属を確認。"
    "②異物残存例のみキレーション: CaEDTA 30 mg/kg SC q12h（希釈）を摘出まで。③支持療法: 輸液、強制給餌（草食種は critical care formula）、保温。"
    "④溶血性貧血のモニタリング（PCV）。⑤ケージ・給水器の亜鉛メッキ部品を全てステンレスに交換（新しい亜鉛メッキ金網「new wire disease」が典型的原因）。"
    "（Carpenter 6th ed; Quesenberry & Carpenter 4th ed）",
    "Small-mammal (degu etc.) zinc toxicosis: (1) identifying and removing the source (galvanized cage wire, bolts, coins) IS the treatment — radiograph for GI metal. "
    "(2) Chelation only while a foreign body persists: CaEDTA 30 mg/kg SC q12h (diluted) until retrieval. (3) Supportive: fluids, syringe feeding (critical care formula for herbivores), warmth. "
    "(4) Monitor PCV for hemolytic anemia. (5) Replace all galvanized cage/waterer parts with stainless steel ('new wire disease' is the classic cause). "
    "(Carpenter 6th ed; Quesenberry & Carpenter 4th ed)",
)

_FISH_AMMONIA = _t(
    "魚のアンモニア中毒/鰓焼けの治療は水質管理そのもの（催吐・活性炭という概念は存在しない）: "
    "①即時30-50%換水（温度・pH合わせ）を毒性値が下がるまで連日。②アンモニア無害化剤（Prime等のコンディショナー）投与。"
    "③エアレーション強化（鰓障害による低酸素対策）。④給餌を数日間中止/大幅減（アンモニア産生源）。"
    "⑤原因究明: 生物濾過の破綻（新規立ち上げ・薬浴後・過密・濾材洗いすぎ）を是正し、亜硝酸→硝酸への硝化サイクル回復を試験紙で確認。"
    "⑥pHが高いほど毒性の高いNH3比率が増える — pH>8では緊急性が高い。二次的な細菌感染・鰓障害を経過観察。"
    "（Noga, Fish Disease 2nd ed; Roberts, Fish Pathology）",
    "Treating fish ammonia toxicity/gill burn IS water-quality management (emesis and charcoal do not exist here): "
    "(1) immediate 30-50% water changes (temperature/pH-matched) daily until levels fall. (2) Ammonia-detoxifying conditioner (e.g. Prime). "
    "(3) Increase aeration (gill damage causes hypoxia). (4) Stop/greatly reduce feeding for several days (the ammonia source). "
    "(5) Fix the cause: a crashed biofilter (new tank, post-medication, overstocking, over-cleaned media) — verify the nitrification cycle recovers with test strips. "
    "(6) Toxic NH3 fraction rises with pH — pH >8 is more urgent. Monitor for secondary bacterial/gill disease. "
    "(Noga, Fish Disease 2nd ed; Roberts, Fish Pathology)",
)

_PIG_SALT = _t(
    "ブタ（ミニブタ）の食塩中毒・水分欠乏症: 治療の核心は「ゆっくり戻す」 — 自由飲水の一括再開は脳浮腫を悪化させ致死的。"
    "①少量頻回の給水: 体重の0.5%量を1時間毎（例: 20 kgで100 mL）から開始し徐々に増量。"
    "②重症・飲水不能例: 血清Naを測定し、低下速度0.5 mEq/L/h以下でD5W/0.45% NaClを緩徐IV。"
    "③脳浮腫の徴候（発作・皮質盲・旋回）にはマンニトール 1 g/kg IVまたはデキサメタゾン。④痙攣にジアゼパム。"
    "⑤再発防止: 常時新鮮水へのアクセス確保（給水器の凍結・故障が典型的誘因）。回復しても神経後遺症が残ることがある。"
    "（Pugh, Sheep, Goat & Cervid Medicine; Swine Medicine texts）",
    "Porcine (mini-pig) salt poisoning / water deprivation: the core of treatment is SLOW reintroduction — unrestricted water access worsens cerebral edema and can be fatal. "
    "(1) Small frequent water: start at 0.5% of body weight hourly (e.g. 100 mL for 20 kg) and increase gradually. "
    "(2) Severe/unable to drink: measure serum Na and infuse D5W/0.45% NaCl no faster than a 0.5 mEq/L/h decrease. "
    "(3) Cerebral edema signs (seizures, cortical blindness, circling): mannitol 1 g/kg IV or dexamethasone. (4) Diazepam for seizures. "
    "(5) Prevention: guarantee constant fresh-water access (frozen/failed waterers are the classic trigger). Neurologic deficits may persist. "
    "(Pugh; standard swine medicine references)",
)

_GLIDER_AFLA = _t(
    "フクロモモンガのアフラトキシン中毒: ①汚染源（カビたトウモロコシ系飼料・ピーナッツ・汚染コオロギの腸内容）を即時全撤去し、新鮮で保存状態の良い食餌に交換。"
    "②肝保護: シリマリン 20-50 mg/kg PO q24h、SAMe 30 mg/kg PO q24h。③凝固障害（アフラトキシンは凝固因子合成を阻害）にビタミンK1 2.5 mg/kg SC q24h。"
    "④低血糖に経口/皮下ブドウ糖、脱水に加温輸液（SC 20-40 mL/kg/日 分割）、強制給餌。"
    "⑤特異的解毒剤はなく、肝壊死が進行した例の予後は不良。同居個体の食餌も点検。"
    "（Carpenter 6th ed; Booth, Sugar Glider medicine references）",
    "Sugar glider aflatoxicosis: (1) immediately remove ALL contaminated feed (moldy corn-based diets, peanuts, gut-loaded crickets) and replace with fresh, well-stored food. "
    "(2) Hepatoprotection: silymarin 20-50 mg/kg PO q24h, SAMe 30 mg/kg PO q24h. (3) Vitamin K1 2.5 mg/kg SC q24h for the coagulopathy (aflatoxin impairs clotting-factor synthesis). "
    "(4) Oral/SC dextrose for hypoglycemia, warmed SC fluids 20-40 mL/kg/day divided, syringe feeding. "
    "(5) No specific antidote exists; prognosis is poor once hepatic necrosis is established. Check cage-mates' diet too. "
    "(Carpenter 6th ed)",
)

_FERRET_IBUPROFEN = _t(
    "フェレットのイブプロフェン中毒（フェレットは犬より遥かに感受性が高く、神経徴候〔昏迷・昏睡〕が急速に出る）: "
    "①除染: 1時間以内なら催吐、活性炭 1-2 g/kg PO（症状発現後の催吐は誤嚥リスクで避ける）。"
    "②腎保護: 晶質液 2倍維持量 IV×48時間、腎数値と尿量を72時間モニタリング。"
    "③消化管保護: オメプラゾール 4 mg/kg PO q24h、スクラルファート 25 mg/kg PO q8h、ミソプロストール 1-5 μg/kg PO q8h。"
    "④神経抑制には気道確保を含む支持療法、重度昏迷に静注脂肪乳剤（ILE 20%）を考慮。"
    "⑤メレナ・穿孔徴候の監視。（Quesenberry & Carpenter 4th ed; Richardson, Exotic DVM）",
    "Ferret ibuprofen toxicosis (ferrets are far more sensitive than dogs, with rapid CNS signs — stupor, coma): "
    "(1) Decontaminate: emesis within 1 h, activated charcoal 1-2 g/kg PO (avoid emesis once symptomatic — aspiration risk). "
    "(2) Renal protection: crystalloids at 2× maintenance IV ×48 h; monitor renal values and urine output for 72 h. "
    "(3) GI protection: omeprazole 4 mg/kg PO q24h, sucralfate 25 mg/kg PO q8h, misoprostol 1-5 µg/kg PO q8h. "
    "(4) Airway-protective supportive care for CNS depression; consider 20% intravenous lipid emulsion for severe stupor. "
    "(5) Watch for melena/perforation. (Quesenberry & Carpenter 4th ed)",
)


def _reptile_ivermectin(sp_ja: str, sp_en: str, chelonian: bool) -> dict:
    chel_ja = (
        "カメ類（リクガメ含む）ではイベルメクチンはいかなる用量でも絶対禁忌（致死的弛緩性麻痺）であり、"
        "本症の発生自体が投薬過誤を意味する。"
        if chelonian
        else ""
    )
    chel_en = (
        "In chelonians ivermectin is absolutely contraindicated at ANY dose (fatal flaccid paralysis) — "
        "occurrence of this toxicosis implies a medication error. "
        if chelonian
        else ""
    )
    return _t(
        f"{sp_ja}のイベルメクチン中毒に解毒剤はない。{chel_ja}"
        "治療は長期の集中支持療法: ①呼吸抑制・無呼吸には挿管+間欠的陽圧換気（爬虫類は低代謝のため数日間の換気補助でも回復例あり）。"
        "②適温域（POTZ）上限での維持（代謝・薬物排泄を促進）。③輸液（10-20 mL/kg/日 SC/ICe）、経管栄養。"
        "④回復は数日〜数週かかるため安楽死判断を急がない。⑤以後のマクロサイクリックラクトン使用禁止 — 外部寄生虫は接触殺虫剤や環境対策で管理。"
        "（Mader 3rd ed; Carpenter 6th ed）",
        f"There is no antidote for ivermectin toxicosis in {sp_en}. {chel_en}"
        "Treatment is prolonged intensive support: (1) intubation + intermittent positive-pressure ventilation for respiratory depression/apnea "
        "(reptiles' low metabolic rate means recovery is possible even after days of ventilatory support). "
        "(2) Maintain at the upper preferred optimal temperature zone (POTZ) to promote metabolism and drug elimination. "
        "(3) Fluids 10-20 mL/kg/day SC/intracoelomic and tube feeding. (4) Recovery takes days to weeks — do not rush euthanasia decisions. "
        "(5) Never use macrocyclic lactones again; manage ectoparasites with contact acaricides and husbandry. (Mader 3rd ed; Carpenter 6th ed)",
    )


def _reptile_lead(sp_ja: str, sp_en: str) -> dict:
    return _t(
        f"{sp_ja}の鉛中毒: ①X線で消化管内金属片（釣り錘・散弾・塗料片）を確認し、可能なら内視鏡/外科的に摘出。"
        "②キレーション: CaEDTA 10-40 mg/kg IM q12h（水和を維持し腎障害に注意）を血中鉛低下まで。"
        "③POTZ上限での飼育、輸液（10-20 mL/kg/日）、強制給餌。④痙攣にはミダゾラム 1-2 mg/kg IM。"
        "⑤基質・ケージ環境の鉛源（古い塗料・おもり）を除去。（Mader 3rd ed; Carpenter 6th ed）",
        f"Lead toxicosis in {sp_en}: (1) radiograph for GI metal (sinkers, shot, paint chips) and retrieve endoscopically/surgically when possible. "
        "(2) Chelation: CaEDTA 10-40 mg/kg IM q12h (keep hydrated, watch renal function) until blood lead falls. "
        "(3) Husbandry at the upper POTZ, fluids 10-20 mL/kg/day, assisted feeding. (4) Midazolam 1-2 mg/kg IM for seizures. "
        "(5) Remove environmental lead sources (old paint, weights). (Mader 3rd ed; Carpenter 6th ed)",
    )


def _reptile_metronidazole(sp_ja: str, sp_en: str) -> dict:
    return _t(
        f"{sp_ja}のメトロニダゾール中毒（神経毒性 — 失調・斜頸・後弓反張）: ①即時投薬中止が治療の中心。"
        "②支持療法: POTZ維持、輸液（10-20 mL/kg/日 SC/ICe）、転倒・外傷防止の単純なケージ、経管栄養。"
        "③神経徴候は蓄積した薬物の消失に伴い1-2週間（時に数週）で通常可逆。④再投与する場合は総用量を制限"
        "（一般種<100 mg/kg、インディゴヘビ・キングスネーク等の感受性種は40 mg/kg以下）。"
        "（Mader 3rd ed; Carpenter 6th ed）",
        f"Metronidazole toxicosis in {sp_en} (neurotoxicity — ataxia, head tilt, opisthotonus): (1) immediate drug withdrawal IS the treatment. "
        "(2) Support: POTZ maintenance, fluids 10-20 mL/kg/day SC/intracoelomic, a simple padded enclosure to prevent trauma, tube feeding. "
        "(3) Neurologic signs are usually reversible over 1-2 weeks (occasionally longer) as the accumulated drug clears. "
        "(4) If ever re-dosed, cap total dose (<100 mg/kg in general; ≤40 mg/kg in sensitive species such as indigo snakes and kingsnakes). "
        "(Mader 3rd ed; Carpenter 6th ed)",
    )


def _reptile_plant_pesticide(sp_ja: str, sp_en: str) -> dict:
    return _t(
        f"{sp_ja}の植物毒・農薬曝露: ①曝露源の除去 — 経皮/環境曝露（有機リン系殺虫剤・除草剤）は微温湯と希釈中性洗剤で洗浄し、"
        "汚染基質・植物をケージから撤去。②有機リン徴候（流涎・振戦・徐脈）にはアトロピン 0.02-0.04 mg/kg IM。"
        "③支持療法: POTZ維持、輸液（10-20 mL/kg/日）、強制給餌。④草食種の毒草摂取では催吐は不可能/危険であり、"
        "胃管での希釈・活性炭 1 g/kg 投与を検討。⑤痙攣にミダゾラム。回復まで数日〜数週。安全な餌植物リストの飼い主教育。"
        "（Mader 3rd ed; Carpenter 6th ed）",
        f"Plant/pesticide exposure in {sp_en}: (1) remove the source — wash dermal/environmental exposure (organophosphate insecticides, herbicides) "
        "with tepid water and dilute mild detergent; strip contaminated substrate/plants from the enclosure. "
        "(2) Atropine 0.02-0.04 mg/kg IM for organophosphate signs (salivation, tremors, bradycardia). "
        "(3) Support: POTZ, fluids 10-20 mL/kg/day, assisted feeding. (4) Emesis is not feasible/safe in reptiles — consider gastric tube dilution and activated charcoal 1 g/kg. "
        "(5) Midazolam for seizures. Recovery takes days-weeks. Educate owners on safe food-plant lists. (Mader 3rd ed; Carpenter 6th ed)",
    )


_PARROT_CHOCOLATE = _t(
    "鳥（オウム類）のチョコレート（メチルキサンチン）中毒: 鳥は体重あたりの感受性が非常に高く少量でも危険。"
    "①除染: 早期なら嗉嚢洗浄（ガベージチューブで微温生食を注入・回収）、活性炭 1-3 g/kg 嗉嚢内投与。"
    "②不整脈・頻脈: 心電図/聴診モニタリング、頻脈性不整脈にプロプラノロール 0.2 mg/kg 緩徐IV/IM。"
    "③痙攣にミダゾラム 0.5-1 mg/kg IM。④輸液（ボーラス10 mL/kg IV/IO→維持）で排泄促進。"
    "⑤保温・低刺激の酸素ケージ。チョコレート・アボカド・カフェインは鳥に絶対に与えないことを飼い主教育。"
    "（Carpenter 6th ed; Ritchie & Harrison）",
    "Avian (psittacine) chocolate/methylxanthine toxicosis: birds are extremely sensitive per body weight — small amounts are dangerous. "
    "(1) Decontaminate early: crop lavage (warm saline via gavage tube, instill and retrieve), activated charcoal 1-3 g/kg into the crop. "
    "(2) Arrhythmias/tachycardia: ECG/auscultation monitoring, propranolol 0.2 mg/kg slow IV/IM for tachyarrhythmias. "
    "(3) Midazolam 0.5-1 mg/kg IM for seizures. (4) Fluids (10 mL/kg IV/IO bolus then maintenance) to promote excretion. "
    "(5) Warm, low-stimulation oxygen cage. Educate owners: never chocolate, avocado or caffeine for birds. (Carpenter 6th ed; Ritchie & Harrison)",
)

_BIRD_AVOCADO = _t(
    "鳥のアボカド（ペルシン）中毒に解毒剤はない — 心筋壊死・肺水腫が主病態で、治療は早期除染と心肺支持。"
    "①摂取直後: 嗉嚢洗浄+活性炭 1-3 g/kg。②肺水腫・呼吸促迫: 酸素ケージ、フロセミド 1-2 mg/kg IM q6-12h。"
    "③ハンドリングを最小限にし保温（心筋障害下のストレス性突然死を防ぐ）。④輸液は肺水腫を悪化させない量で慎重に。"
    "⑤摂取後24-48時間の心電図/呼吸数モニタリング。予後は摂取量依存で guarded。"
    "セキセイ・オカメは特に感受性が高い。（Carpenter 6th ed; Hargis 1989; Ritchie & Harrison）",
    "There is no antidote for avian avocado (persin) toxicosis — myocardial necrosis and pulmonary edema dominate; treatment is early decontamination and cardiopulmonary support. "
    "(1) Immediately post-ingestion: crop lavage + activated charcoal 1-3 g/kg. (2) Pulmonary edema/tachypnea: oxygen cage, furosemide 1-2 mg/kg IM q6-12h. "
    "(3) Minimal handling and warmth (prevents stress-induced sudden death on a damaged myocardium). (4) Cautious fluid volumes (avoid worsening edema). "
    "(5) ECG/respiratory monitoring for 24-48 h. Prognosis is dose-dependent and guarded. Budgerigars and cockatiels are especially sensitive. "
    "(Carpenter 6th ed; Hargis JAVMA 1989; Ritchie & Harrison)",
)

_BIRD_ESSENTIAL_OIL = _t(
    "鳥のエッセンシャルオイル中毒（ディフューザー・アロマ）: ①即時に新鮮空気へ移動し、発生源を撤去・部屋を換気。"
    "②吸入曝露が主: 加湿酸素ケージ、呼吸促迫にはミダゾラムでストレス軽減、気道炎症にメロキシカム 1 mg/kg PO/IM q24h。"
    "③羽毛・皮膚への付着: 微温湯+希釈食器用洗剤で優しく洗浄（低体温防止に保温を徹底）。催吐は不可能（鳥）。"
    "④二次的細菌感染の監視。⑤飼い主教育: 鳥のいる部屋でのディフューザー・アロマキャンドル・テフロン調理は避ける"
    "（鳥の気嚢系は揮発性物質に極めて敏感）。（Carpenter 6th ed; Ritchie & Harrison）",
    "Avian essential-oil toxicosis (diffusers/aromatherapy): (1) move to fresh air immediately, remove the source and ventilate the room. "
    "(2) Inhalation dominates: humidified oxygen cage, midazolam to reduce stress dyspnea, meloxicam 1 mg/kg PO/IM q24h for airway inflammation. "
    "(3) Feather/skin contamination: gently bathe with tepid water and dilute dish detergent (guard against hypothermia). Emesis is not possible in birds. "
    "(4) Monitor for secondary bacterial infection. (5) Owner education: no diffusers, scented candles or overheated PTFE cookware in the bird's room "
    "(the avian air-sac system is exquisitely sensitive to volatiles). (Carpenter 6th ed; Ritchie & Harrison)",
)

_BIRD_PLANT = _t(
    "鳥の植物中毒: ①種同定が最優先（アボカド→心毒性、ナス科→アトロピン様、キョウチクトウ→ジギタリス様と対処が異なる）。"
    "摂取植物の写真・現物を持参してもらう。②早期除染: 嗉嚢洗浄+活性炭 1-3 g/kg 嗉嚢内投与。"
    "③輸液（10 mL/kg ボーラス→維持）・保温・ガベージ給餌の支持療法。④強心配糖体植物では不整脈モニタリング、"
    "痙攣にはミダゾラム 0.5-1 mg/kg IM。⑤ケージ周囲の観葉植物を安全種のみに（飼い主教育）。"
    "（Carpenter 6th ed; Ritchie & Harrison; Gardner & LaFage 植物毒性リスト）",
    "Avian plant toxicosis: (1) plant identification first — management differs radically (avocado → cardiotoxic, nightshades → atropinic, oleander → digitalis-like); have owners bring a photo/sample. "
    "(2) Early decontamination: crop lavage + activated charcoal 1-3 g/kg into the crop. "
    "(3) Support: fluids (10 mL/kg bolus then maintenance), warmth, gavage feeding. (4) Arrhythmia monitoring for cardiac-glycoside plants; midazolam 0.5-1 mg/kg IM for seizures. "
    "(5) Restrict houseplants around the cage to known-safe species (owner education). (Carpenter 6th ed; Ritchie & Harrison)",
)

_BIRD_RODENTICIDE = _t(
    "鳥の抗凝固性殺鼠剤中毒: 解毒剤はビタミンK1 — 2.5-5 mg/kg PO/SC q12h を第2世代製剤では4週間継続（餌に混ぜた経口投与が実用的）。"
    "①摂取直後: 嗉嚢洗浄+活性炭 1-3 g/kg。②出血例: ハンドリング最小化、保温酸素ケージ、重度貧血には同種鳥全血輸血（PCV<20%）。"
    "③治療終了48-72時間後にPT相当（鳥では観察ベース）で再評価し、出血傾向再発なら延長。"
    "④ブロメタリン系（非抗凝固）はK1無効 — 製品確認が必須。⑤げっ歯類駆除は鳥のアクセス不能な方法に変更。"
    "（Carpenter 6th ed; Ritchie & Harrison）",
    "Avian anticoagulant rodenticide toxicosis: the antidote is vitamin K1 — 2.5-5 mg/kg PO/SC q12h, continued 4 weeks for second-generation agents (oral in food is practical). "
    "(1) Immediately post-ingestion: crop lavage + activated charcoal 1-3 g/kg. (2) Bleeding birds: minimal handling, warm oxygen cage, homologous whole-blood transfusion for severe anemia (PCV <20%). "
    "(3) Re-evaluate 48-72 h after the last dose; extend if bleeding recurs. "
    "(4) Bromethalin (non-anticoagulant) products do NOT respond to K1 — verify the product. (5) Switch rodent control to bird-inaccessible methods. "
    "(Carpenter 6th ed; Ritchie & Harrison)",
)

_BIRD_SMOKE = _t(
    "鳥の煙・ガス吸入中毒（PTFE/テフロン過熱・調理煙・火災）: 鳥の気嚢系は揮発性毒に極めて敏感で、PTFE熱分解ガスはしばしば致死的。"
    "①即時に新鮮空気へ — 発生源の部屋から退避。②加湿酸素ケージ（40-50%酸素）で最小ハンドリング。"
    "③気道炎症・肺水腫: メロキシカム 1 mg/kg IM q24h、フロセミド 1-2 mg/kg IM q6-12h、重度の呼吸困難にはミダゾラムでストレス軽減。"
    "④二次的細菌性肺炎の予防的監視（発熱・白血球）。⑤輸液・保温・強制給餌。"
    "⑥予後: PTFE曝露は急性死が多いが、24時間生存例は回復が期待できる。台所と鳥の部屋の分離を飼い主教育。"
    "（Carpenter 6th ed; Ritchie & Harrison; Wells 1983）",
    "Avian smoke/fume inhalation (overheated PTFE/Teflon, cooking fumes, fires): the air-sac system is exquisitely sensitive; PTFE pyrolysis gas is often fatal. "
    "(1) Fresh air immediately — evacuate the room. (2) Humidified 40-50% oxygen cage with minimal handling. "
    "(3) Airway inflammation/pulmonary edema: meloxicam 1 mg/kg IM q24h, furosemide 1-2 mg/kg IM q6-12h, midazolam to relieve stress dyspnea. "
    "(4) Monitor for secondary bacterial pneumonia. (5) Fluids, warmth, gavage feeding. "
    "(6) Prognosis: PTFE exposure kills acutely, but birds surviving 24 h usually recover. Educate owners to separate kitchens and bird rooms. "
    "(Carpenter 6th ed; Ritchie & Harrison; Wells JAVMA 1983)",
)


# ------------------------------------------------------------ exact-name map
# (db_species, exact English name) -> fields dict
CURATED_TOXICOSIS_TREATMENTS: dict[tuple[str, str], dict] = {
    ("cat", "Acetaminophen (Paracetamol) Toxicosis"): _CAT_ACETAMINOPHEN,
    ("cat", "Acetaminophen Toxicosis (Acute)"): _CAT_ACETAMINOPHEN,
    ("cat", "Ethylene Glycol (Antifreeze) Poisoning"): _CAT_EG,
    ("cat", "Feline Bromethalin Toxicosis"): _CAT_BROMETHALIN,
    ("cat", "Feline Chocolate Toxicosis"): _CAT_CHOCOLATE,
    ("cat", "Feline Ivermectin Toxicosis"): _CAT_IVERMECTIN,
    ("cat", "Feline Lead Toxicosis"): _CAT_LEAD,
    ("cat", "Feline Marijuana Toxicosis"): _CAT_MARIJUANA,
    ("cat", "Feline Metaldehyde Toxicosis (Slug Bait)"): _CAT_METALDEHYDE,
    ("cat", "Feline Onion/Garlic Toxicosis"): _CAT_ONION,
    ("cat", "Feline Organophosphate Toxicosis"): _CAT_OP,
    ("cat", "Feline Salt Toxicosis"): _CAT_SALT,
    ("cat", "Feline Toxic Epidermal Necrolysis"): _CAT_TEN,
    ("cat", "Feline Toxic Megacolon"): _CAT_MEGACOLON,
    ("cat", "Feline Zinc Toxicosis"): _CAT_ZINC,
    ("cat", "Lily Nephrotoxicosis (Acute)"): _CAT_LILY,
    ("cat", "Lily Toxicosis"): _CAT_LILY,
    ("cat", "NSAID Toxicosis"): _CAT_NSAID,
    ("cat", "Rodenticide Poisoning (Anticoagulant)"): _CAT_ANTICOAG,
    ("cat", "Tea Tree Oil Toxicosis"): _CAT_TEA_TREE,
    ("bird", "Lead Toxicosis – Chronic"): _BIRD_LEAD,
    ("degu", "Zinc Toxicosis"): _SMALL_MAMMAL_ZINC,
    ("exotic_other", "Ammonia Burns / Poisoning (Fish)"): _FISH_AMMONIA,
    ("exotic_other", "Salt Poisoning / Water Deprivation (Porcine)"): _PIG_SALT,
    ("exotic_other", "Sugar Glider Aflatoxicosis"): _GLIDER_AFLA,
    ("ferret", "Ibuprofen Toxicosis"): _FERRET_IBUPROFEN,
    ("lizard", "Ivermectin Toxicosis"): _reptile_ivermectin("トカゲ", "lizards", chelonian=False),
    ("lizard", "Lead Toxicosis"): _reptile_lead("トカゲ", "lizards"),
    ("lizard", "Metronidazole Toxicosis"): _reptile_metronidazole("トカゲ", "lizards"),
    ("reptile", "Ivermectin Toxicosis"): _reptile_ivermectin("爬虫類", "reptiles", chelonian=True),
    ("reptile", "Lead Toxicosis"): _reptile_lead("爬虫類", "reptiles"),
    ("reptile", "Metronidazole Toxicosis"): _reptile_metronidazole("爬虫類", "reptiles"),
    ("snake", "Ivermectin Toxicosis"): _reptile_ivermectin("ヘビ", "snakes", chelonian=False),
    ("snake", "Lead Toxicosis"): _reptile_lead("ヘビ", "snakes"),
    ("snake", "Metronidazole Toxicosis"): _reptile_metronidazole("ヘビ", "snakes"),
    ("tortoise", "Ivermectin Toxicosis"): _reptile_ivermectin("リクガメ", "tortoises", chelonian=True),
    ("tortoise", "Lead Toxicosis"): _reptile_lead("リクガメ", "tortoises"),
    ("tortoise", "Metronidazole Toxicosis"): _reptile_metronidazole("リクガメ", "tortoises"),
    ("tortoise", "Pesticide / Herbicide Exposure"): _reptile_plant_pesticide("リクガメ", "tortoises"),
    ("tortoise", "Plant Toxicity"): _reptile_plant_pesticide("リクガメ", "tortoises"),
    ("parakeet", "Avocado Toxicosis (Parakeet)"): _BIRD_AVOCADO,
    ("parakeet", "Essential Oil Toxicity"): _BIRD_ESSENTIAL_OIL,
    ("parakeet", "Lead Toxicosis"): _BIRD_LEAD,
    ("parakeet", "Plant Toxicity"): _BIRD_PLANT,
    ("parakeet", "Rodenticide Poisoning"): _BIRD_RODENTICIDE,
    ("parrot", "Chocolate Toxicity"): _PARROT_CHOCOLATE,
    ("parrot", "Essential Oil Toxicity"): _BIRD_ESSENTIAL_OIL,
    ("parrot", "Plant Toxicity"): _BIRD_PLANT,
    ("parrot", "Rodenticide Poisoning"): _BIRD_RODENTICIDE,
    ("parrot", "Smoke/Fume Inhalation Toxicosis"): _BIRD_SMOKE,
}


def curated_toxicosis_treatment(species: str, name_en: str) -> dict | None:
    """Return curated treatment fields for an exact (species, name) key, or None."""
    return CURATED_TOXICOSIS_TREATMENTS.get(((species or "").lower(), name_en or ""))


# --------------------------------------------------------------------------
# EN back-fill: records whose JA treatment is informative but whose EN carries
# the toxin template. The EN text below is a faithful English rendering of the
# existing curated JA content (same drugs, doses and caveats), so no new
# medical claims are introduced.
_EN = lambda en: {"treatment": en}  # noqa: E731

EN_BACKFILL_TREATMENTS: dict[tuple[str, str], dict] = {
    ("amphibian", "Iridovirus (Ranavirus)"): _EN(
        "Amphibian ranavirus (Iridoviridae) infection is highly lethal and has no specific therapy. "
        "Supportive care: amphibian Ringer's solution baths, optimal water temperature, nutritional support. "
        "Enrofloxacin 5-10 mg/kg bath/topical for secondary bacterial infection; meloxicam 0.2 mg/kg topical for analgesia. "
        "Watch for Bd/Bsal (chytrid) co-infection. Strict isolation of affected animals and environmental disinfection with 1% sodium hypochlorite. "
        "A disease of conservation significance."
    ),
    ("bird", "Renal Failure (Acute)"): _EN(
        "Restore renal perfusion with emergency fluids (25 mL/kg SC/IO bolus, then ~10 mL/kg/h maintenance). "
        "Stop all nephrotoxic drugs immediately. Allopurinol 10 mg/kg PO q12h to reduce urate production; furosemide 2 mg/kg IM for oliguria. "
        "Warmth and nutritional support. Identify and treat the cause (e.g. heavy-metal chelation). Early intervention can be rewarding."
    ),
    ("bird", "Teflon/PTFE Toxicosis"): _EN(
        "Move to fresh air immediately after exposure. Oxygen therapy (40-60%). "
        "Dexamethasone 2 mg/kg IM may be attempted for pulmonary edema; bronchodilator (terbutaline 0.01 mg/kg IM). "
        "Severe exposure often fails to respond and carries a grave prognosis — prevention is paramount "
        "(remove PTFE cookware or keep birds entirely out of kitchens; toxic fumes are released above ~260°C)."
    ),
    ("bird", "Hepatic Fibrosis"): _EN(
        "Avian hepatic fibrosis is progressive and rarely curable — management centers on early detection, removing the cause and slowing fibrogenesis. "
        "(1) Work-up: CBC/chemistry, bile-acid testing, coagulation times, ultrasound, liver biopsy. "
        "(2) Cause-directed therapy: immunosuppression for immune-mediated disease, deworming, toxin removal, copper chelation (penicillamine), drug withdrawal. "
        "(3) Antifibrotics/hepatoprotection: ursodiol 10-15 mg/kg PO q24h, SAMe 20 mg/kg PO q24h, silymarin 4-15 mg/kg PO q24h, vitamin E 10-15 IU/kg PO q24h. "
        "(4) Portal hypertension: spironolactone 1-2 mg/kg PO q12h, low-salt diet, paracentesis for ascites. "
        "(5) Hepatic encephalopathy: lactulose 0.5-1 mL/kg PO q8h."
    ),
    ("degu", "Lead Poisoning"): _EN(
        "Degu lead toxicosis: CaEDTA 25-30 mg/kg SC q12h for 5 days; remove metallic foreign material. "
        "Diazepam 1-2 mg/kg IM for seizures. Supportive SC fluids, warmth, timothy hay and pellets. "
        "Degus are diabetes-prone — avoid high-sugar syringe feeds. Prognosis good with early treatment. (Quesenberry & Carpenter 2020)"
    ),
    ("degu", "Plant Toxicosis"): _EN(
        "Degu plant toxicosis: oral lavage for calcium-oxalate plants; activated charcoal 1-2 g/kg PO for systemically toxic plants. "
        "Supportive SC fluids, warmth, timothy-based feeding; nephrotoxic plants (Liliaceae) warrant aggressive fluids for 48-72 h. "
        "Avoid sugar-containing syrups (diabetes risk). Prognosis good for oral irritation alone, poor after large nephrotoxic ingestions. (Quesenberry & Carpenter 2020)"
    ),
    ("degu", "Antibiotic Toxicity"): _EN(
        "Degu antibiotic-associated enterotoxemia (oral penicillins/cephalosporins/lincosamides disrupt cecal flora): "
        "stop the offending drug immediately. SC fluids (3-5 mL/dose q12h), metronidazole 20 mg/kg PO q12h ×5 d for clostridial overgrowth, "
        "probiotics/cecotroph transfaunation from a healthy degu, and syringe feeding with a sugar-free timothy-pellet slurry. "
        "Prognosis fair when mild, guarded with severe enteritis. (Quesenberry & Carpenter 2020)"
    ),
    ("exotic_other", "Anemia"): _EN(
        "Exotic-companion anemia: classify first — blood loss (trauma, parasites, GI bleeding), hemolysis (immune-mediated, infectious, oxidative) "
        "or non-regenerative (chronic disease, renal, marrow suppression). Work-up: CBC with reticulocytes, blood smear, chemistry, Coombs, urinalysis, imaging. "
        "Acute blood loss: control the source; consider transfusion below PCV 15% (carnivores)/20% (herbivores) with species-matched, crossmatched donors. "
        "Chronic loss: treat the cause plus iron (iron dextran 10-20 mg/kg IM once, or ferrous sulfate 4-6 mg/kg PO q24h). "
        "Immune-mediated hemolysis: prednisolone 1-2 mg/kg."
    ),
    ("exotic_other", "Dermatological Viral Infection"): _EN(
        "Cutaneous viral disease in exotic companions: papilloma/pox-like lesions — surgical excision (solitary, enlarging), cryotherapy for small lesions, "
        "or await spontaneous regression in immunocompetent animals (weeks-months). Poxvirus: supportive nutrition, antibiotics for secondary infection, "
        "topical antisepsis/silver sulfadiazine, let crusts detach naturally (avian pox: dry cutaneous form fair, wet oropharyngeal form poor). "
        "Herpesvirus: acyclovir 80 mg/kg PO q8h reported in chelonians/birds. Isolate, disinfect and quarantine new animals."
    ),
    ("guinea_pig", "Lead Poisoning"): _EN(
        "Guinea-pig lead toxicosis: CaEDTA 30 mg/kg SC q12h ×5 d, repeat course after a 5-day rest if needed; retrieve retained GI metal. "
        "Seizures: diazepam 1-3 mg/kg IM or midazolam 0.5-1 mg/kg IN. Supportive SC fluids (20-30 mL/dose), vitamin C 50-100 mg/kg PO q24h. "
        "Never give oral penicillins/cephalosporins (fatal dysbiosis). Prognosis good with early treatment. (Quesenberry & Carpenter 2020)"
    ),
    ("guinea_pig", "Plant Toxicosis"): _EN(
        "Guinea-pig plant toxicosis: oral lavage for calcium-oxalate plants (pothos, philodendron); activated charcoal 1-2 g/kg PO for systemic toxins. "
        "Supportive SC fluids, syringe feeding with a timothy-pellet slurry plus vitamin C 50-100 mg/kg PO q24h, warmth. "
        "Anorexia beyond 24 h risks hepatic lipidosis — assisted feeding is mandatory. Block access to toxic plants. (Quesenberry & Carpenter 2020)"
    ),
    ("guinea_pig", "Antibiotic Toxicity"): _EN(
        "Guinea-pig antibiotic-associated enterotoxemia — CRITICAL: oral penicillins, cephalosporins, lincosamides and macrolides cause "
        "fatal clostridial dysbiosis (mortality 60-100%). Stop the drug immediately. Aggressive fluids (LRS 50-100 mL/kg/day SC/IP), "
        "metronidazole 20 mg/kg PO q12h for C. difficile, cholestyramine to bind enterotoxin, cecotroph transfaunation from a healthy guinea pig, "
        "syringe feeding (timothy slurry + vitamin C), warmth. (Quesenberry & Carpenter 2020)"
    ),
    ("guinea_pig", "Thrombocytopenia"): _EN(
        "Guinea-pig thrombocytopenia: classify the cause — immune-mediated, infectious, drug-induced, consumptive (DIC) or productive failure. "
        "Work-up: CBC with smear (exclude clumping), chemistry, coagulation times, infectious PCR, marrow evaluation, abdominal ultrasound. "
        "Severe bleeding below 30,000/µL: fresh whole-blood transfusion 5-10 mL/kg slowly (species-matched healthy donor, ≤1% of donor body weight). "
        "Immune-mediated disease: corticosteroids; otherwise treat the underlying cause."
    ),
    ("guinea_pig", "Polycythemia"): _EN(
        "Guinea-pig polycythemia: distinguish relative (dehydration) from absolute (primary polycythemia vera vs secondary to chronic hypoxemia or "
        "EPO-producing tumors) using CBC, serum EPO, imaging and blood gas. Relative: isotonic fluids until HCT normalizes. "
        "Secondary: treat the underlying cardiac/pulmonary disease. Polycythemia vera: therapeutic phlebotomy 10-20 mL/kg with equal-volume fluid "
        "replacement q2-4 wk, plus hydroxyurea for maintenance."
    ),
    ("guinea_pig", "Zinc Toxicosis"): _EN(
        "Guinea-pig zinc toxicosis: CaEDTA 30 mg/kg SC q12h ×5 d and removal of the metallic source (galvanized cage parts). "
        "Supportive SC fluids, vitamin C 50-100 mg/kg PO q24h, syringe feeding; manage hemolytic anemia (iron, transfusion if severe). "
        "Prevention: stainless-steel/powder-coated caging, no galvanized products. (Quesenberry & Carpenter 2020)"
    ),
    ("parakeet", "Hepatitis"): _EN(
        "Psittacine hepatitis: identifying the cause (infectious, toxic, immune-mediated, neoplastic, metabolic) directs therapy. "
        "(1) Work-up: CBC/chemistry, bile acids, coagulation, ultrasound, liver biopsy. (2) Cause-directed: culture-guided antibiotics 4-6 wk, deworming, "
        "supportive care for viral disease, tapering prednisolone for immune-mediated disease, drug withdrawal. "
        "(3) Hepatoprotection: ursodiol 10-15 mg/kg PO q24h, SAMe 20 mg/kg PO q24h, silymarin 4-15 mg/kg PO q24h, vitamin E 10-15 IU/kg PO q24h. "
        "(4) Nutrition with vitamin K1 supplementation. (5) Recheck liver enzymes q2-4 wk."
    ),
    ("parakeet", "Hepatic Fibrosis"): _EN(
        "Psittacine hepatic fibrosis is progressive — early detection, cause removal and slowing of fibrogenesis are the goals. "
        "Work-up: CBC/chemistry, bile acids, coagulation, ultrasound, liver biopsy. Cause-directed therapy (immunosuppression, deworming, toxin removal, "
        "copper chelation with penicillamine, drug withdrawal). Antifibrotics: ursodiol 10-15 mg/kg PO q24h, SAMe 20 mg/kg q24h, silymarin 4-15 mg/kg q24h, "
        "vitamin E 10-15 IU/kg q24h. Portal hypertension: spironolactone 1-2 mg/kg PO q12h, paracentesis for ascites. "
        "Hepatic encephalopathy: lactulose 0.5-1 mL/kg PO q8h."
    ),
    ("parakeet", "Systemic Toxic Exposure"): _EN(
        "Systemic toxic exposure in parakeets (metals, PTFE, plant toxins, insecticides, aerosols — birds are exquisitely sensitive to inhaled agents): "
        "source removal and decontamination first, move to fresh air. Oral toxins: activated charcoal 1-3 g/kg PO. Inhaled: oxygen and bronchodilators. "
        "Dermal: warm-water feather bathing (guard against chilling). Heavy metals: CaEDTA 35-50 mg/kg IM q12h ×5 d. "
        "Supportive SC fluids, warmth (28-30°C), gavage feeding; silymarin for hepatoprotection. Prognosis depends on the agent — PTFE grave, metals good if treated early."
    ),
    ("parrot", "Hepatitis"): _EN(
        "Psittacine hepatitis: identifying the cause (infectious, toxic, immune-mediated, neoplastic, metabolic) directs therapy. "
        "(1) Work-up: CBC/chemistry, bile acids, coagulation, ultrasound, liver biopsy. (2) Cause-directed: culture-guided antibiotics 4-6 wk, deworming, "
        "supportive care for viral disease, tapering prednisolone for immune-mediated disease, drug withdrawal. "
        "(3) Hepatoprotection: ursodiol 10-15 mg/kg PO q24h, SAMe 20 mg/kg PO q24h, silymarin 4-15 mg/kg PO q24h, vitamin E 10-15 IU/kg PO q24h. "
        "(4) Nutrition with vitamin K1 supplementation. (5) Recheck liver enzymes q2-4 wk."
    ),
    ("reptile", "Renal Failure"): _EN(
        "Reptile renal failure (dehydration, gout, nephrotoxic drugs, poor husbandry): fluids are paramount — warmed lactated Ringer's 10-30 mL/kg "
        "SC/IO/intracoelomic q24h plus warm-water soaking baths (transcutaneous uptake is reptile-specific). "
        "Allopurinol 10-20 mg/kg PO q24h when gout is present; aluminium hydroxide in food as a phosphate binder; avoid aminoglycosides absolutely. "
        "Husbandry: POTZ maintenance, appropriate humidity, constant fresh water, UV-B provision; low-protein diet to reduce urate production. "
        "Visceral gout carries a poor prognosis."
    ),
    ("sugar_glider", "Hepatitis"): _EN(
        "Sugar-glider hepatitis: identify the cause (infectious, toxic, immune-mediated, neoplastic, metabolic). "
        "Work-up: CBC/chemistry, bile acids, coagulation, ultrasound, liver biopsy where feasible. Cause-directed therapy plus hepatoprotection: "
        "ursodiol 10-15 mg/kg PO q24h, SAMe 20 mg/kg PO q24h, silymarin 4-15 mg/kg PO q24h, vitamin E 10-15 IU/kg PO q24h. "
        "Nutrition with vitamin K1 supplementation; recheck liver enzymes q2-4 wk."
    ),
    ("sugar_glider", "Thrombocytopenia"): _EN(
        "Sugar-glider thrombocytopenia: classify the cause — immune-mediated, infectious, drug-induced, consumptive (DIC) or productive failure. "
        "Work-up: CBC with smear (exclude clumping), chemistry, coagulation times, infectious screening, abdominal ultrasound. "
        "Severe bleeding: fresh whole-blood transfusion from a species-matched healthy donor, given slowly. "
        "Immune-mediated disease: corticosteroids; otherwise treat the underlying cause."
    ),
}


# --------------------------------------------------------------------------
# Records whose JA treatment ALSO carries a wrong-category template:
# * lizard "Femoral Pore Impaction" — generic work-up boilerplate.
# * parakeet/parrot "Renal Failure (Acute)" — a mammalian urolithiasis protocol
#   (struvite acidification, urinary catheter…) pasted onto birds, which have
#   no bladder and excrete urates. Replaced with proper avian AKI management.
_FEMORAL_PORE = _t(
    "トカゲの大腿腺閉塞（主に雄）: ①温浴（30-32℃、10-15分）で栓を軟化させ、愛護的に用手圧出（無理な圧出は腺損傷）。"
    "②炎症・感染例: 希釈クロルヘキシジン0.05%で局所洗浄、膿瘍化していれば切開排膿・デブリードマン+培養に基づく抗菌薬。"
    "③根本是正は飼育環境: 湿度不足・低温・ビタミンA欠乏が角栓形成を促進 — 種適正の湿度/POTZ、餌のビタミンA補正。"
    "④再発性・重度例は摘出も選択肢。爪やすり状の粗い基質はナチュラルな摩耗を助ける。（Mader 3rd ed; Carpenter 6th ed）",
    "Femoral pore impaction in lizards (mostly males): (1) warm soaks (30-32°C, 10-15 min) to soften the plugs, then gentle manual expression "
    "(forceful expression damages the glands). (2) Inflamed/infected pores: flush with dilute 0.05% chlorhexidine; incise, debride and give "
    "culture-guided antibiotics if abscessed. (3) The definitive fix is husbandry: low humidity, low temperature and hypovitaminosis A promote "
    "plug formation — correct species-appropriate humidity/POTZ and dietary vitamin A. (4) Recurrent severe cases may warrant gland excision; "
    "mildly abrasive natural substrate assists normal wear. (Mader 3rd ed; Carpenter 6th ed)",
)

_AVIAN_AKI = _t(
    "鳥（インコ・オウム）の急性腎不全: 鳥は膀胱を持たず尿酸を排泄するため、哺乳類の結石プロトコルは適用外。"
    "①緊急輸液で腎灌流回復: 25 mL/kg SC/IOボーラス→維持50-100 mL/kg/日（加温乳酸リンゲル/ノルモソルR）。"
    "②腎毒性薬剤（アミノグリコシド・NSAIDs）の即時中止。③高尿酸血症にアロプリノール 10 mg/kg PO q12h。"
    "④乏尿にフロセミド 2 mg/kg IM。⑤保温28-30℃、強制給餌（Emeraid等 20-30 mL/kg q4-6h）。"
    "⑥原因検索と治療: 重金属（血中鉛/亜鉛→キレーション）、脱水、ビタミンD過剰、腎毒性物質。"
    "早期介入で回復可能だが、内臓痛風に進行した例の予後は不良。（Carpenter 6th ed; Ritchie & Harrison; Echols, Avian nephrology）",
    "Avian (psittacine) acute renal failure: birds have no bladder and excrete urates — mammalian urolithiasis protocols do not apply. "
    "(1) Emergency fluids to restore renal perfusion: 25 mL/kg SC/IO bolus, then 50-100 mL/kg/day maintenance (warmed LRS/Normosol-R). "
    "(2) Immediately stop nephrotoxic drugs (aminoglycosides, NSAIDs). (3) Allopurinol 10 mg/kg PO q12h for hyperuricemia. "
    "(4) Furosemide 2 mg/kg IM for oliguria. (5) Warmth 28-30°C, gavage feeding (e.g. Emeraid 20-30 mL/kg q4-6h). "
    "(6) Find and treat the cause: heavy metals (blood lead/zinc → chelation), dehydration, hypervitaminosis D, nephrotoxins. "
    "Recovery is possible with early intervention; visceral gout carries a poor prognosis. (Carpenter 6th ed; Ritchie & Harrison)",
)


def _small_mammal_aki(sp_ja: str, sp_en: str, note_ja: str = "", note_en: str = "") -> dict:
    return _t(
        f"{sp_ja}の急性腎不全（AKI — 慢性腎臓病や結石症とは管理が異なる）: "
        "①原因の検索と除去が最優先 — 腎毒性薬剤（アミノグリコシド・NSAIDs）の即時中止、脱水/ショック・尿路閉塞（X線/超音波）・中毒の鑑別。"
        "②輸液蘇生: 脱水を6-8時間で補正後、維持量の1.5-2倍で利尿を維持（体重と尿量を1日2回モニタリング — 乏尿例の過剰輸液は肺水腫を招く）。"
        "乏尿にはフロセミド 1-2 mg/kg IV/IM。③高K血症・代謝性アシドーシスの補正。④閉塞例は減圧（カテーテル/膀胱穿刺/外科）。"
        f"⑤支持療法: 保温、消化管保護、強制給餌{note_ja}。回復の可否は原因と乏尿の可逆性に依存する。"
        "（Carpenter 6th ed; Quesenberry & Carpenter 4th ed）",
        f"Acute kidney injury in {sp_en} (managed differently from CKD and from urolithiasis): "
        "(1) find and remove the cause first — stop nephrotoxic drugs (aminoglycosides, NSAIDs), rule out dehydration/shock, urinary obstruction "
        "(radiographs/ultrasound) and toxins. (2) Fluid resuscitation: correct dehydration over 6-8 h, then maintain diuresis at 1.5-2× maintenance "
        "(weigh and monitor urine output twice daily — overhydrating an oliguric patient causes pulmonary edema). Furosemide 1-2 mg/kg IV/IM for oliguria. "
        "(3) Correct hyperkalemia and metabolic acidosis. (4) Decompress obstruction (catheter/cystocentesis/surgery). "
        f"(5) Support: warmth, GI protection, assisted feeding{note_en}. Recovery depends on the cause and reversibility of oliguria. "
        "(Carpenter 6th ed; Quesenberry & Carpenter 4th ed)",
    )


_AVIAN_UROLITH = _t(
    "鳥の尿石症（総排泄腔尿石・尿管尿酸塩結石 — 哺乳類の膀胱結石とは別病態）: "
    "①総排泄腔尿石: 麻酔下で潤滑・用手破砕・摘出（内視鏡補助）、粘膜損傷を避ける。"
    "②輸液利尿（50-100 mL/kg/日 SC/IO 加温）で尿酸排泄を促進、高尿酸血症にアロプリノール 10 mg/kg PO q12h。"
    "③原因是正: 脱水（飲水環境）、ビタミンA欠乏（総排泄腔上皮の角化）、高蛋白/高Ca食、産卵関連の総排泄腔うっ滞。"
    "④尿管結石による閉塞・内臓痛風への進行は予後不良（外科適応は限定的）。⑤再発予防: 水分摂取増加・食餌是正・定期尿酸値チェック。"
    "（Carpenter 6th ed; Ritchie & Harrison; Echols, Avian nephrology）",
    "Avian urolithiasis (cloacal uroliths and ureteral urate calculi — a different entity from mammalian bladder stones): "
    "(1) Cloacal uroliths: lubricate, manually fragment and extract under anesthesia (endoscope-assisted), sparing the mucosa. "
    "(2) Fluid diuresis (50-100 mL/kg/day SC/IO, warmed) to promote urate excretion; allopurinol 10 mg/kg PO q12h for hyperuricemia. "
    "(3) Correct the causes: dehydration (water access), hypovitaminosis A (cloacal epithelial keratinisation), high-protein/high-calcium diets, "
    "egg-laying-associated cloacal stasis. (4) Ureteral obstruction and progression to visceral gout carry a poor prognosis (surgery rarely feasible). "
    "(5) Prevention: increased water intake, dietary correction, periodic uric-acid checks. (Carpenter 6th ed; Ritchie & Harrison)",
)


# Wrong-template fingerprints that gate the replacements for these records.
WORKUP_TEMPLATE_JA_SIG = "正確な臨床評価（病歴、身体検査、CBC・生化学、画像）から治療方針を決定"
UROLITH_TEMPLATE_JA_SIG = "結石組成同定後（X線吸収係数、結晶尿、術中サンプル）"
CKD_ON_AKI_EN_SIG = "CKD management. Renal diet (phosphorus/protein restricted)"
SMALL_MAMMAL_UROLITH_EN_SIG = "【Small Mammal Urolithiasis】"

# (species, name) -> (JA gating fingerprint, EN gating fingerprint, fields).
# The JA/EN field is replaced only when its own gate matches, so curated prose
# in either language is never overwritten.
JA_MISTEMPLATE_FIXES: dict[tuple[str, str], tuple[str, str, dict]] = {
    ("lizard", "Femoral Pore Impaction"): (WORKUP_TEMPLATE_JA_SIG, TOXIN_TREATMENT_EN_SIG, _FEMORAL_PORE),
    ("parakeet", "Renal Failure (Acute)"): (UROLITH_TEMPLATE_JA_SIG, TOXIN_TREATMENT_EN_SIG, _AVIAN_AKI),
    ("parrot", "Renal Failure (Acute)"): (UROLITH_TEMPLATE_JA_SIG, TOXIN_TREATMENT_EN_SIG, _AVIAN_AKI),
    ("guinea_pig", "Acute Renal Failure"): (
        UROLITH_TEMPLATE_JA_SIG,
        CKD_ON_AKI_EN_SIG,
        _small_mammal_aki(
            "モルモット",
            "guinea pigs",
            "（草食スラリー＋ビタミンC 50-100 mg/kg/日）",
            " (herbivore slurry plus vitamin C 50-100 mg/kg/day)",
        ),
    ),
    ("degu", "Acute Renal Failure"): (
        UROLITH_TEMPLATE_JA_SIG,
        CKD_ON_AKI_EN_SIG,
        _small_mammal_aki("デグー", "degus", "（糖分を含まない草食スラリー）", " (sugar-free herbivore slurry)"),
    ),
    ("ferret", "Acute Renal Failure"): (
        UROLITH_TEMPLATE_JA_SIG,
        CKD_ON_AKI_EN_SIG,
        _small_mammal_aki(
            "フェレット", "ferrets", "（高蛋白の肉食用回復食）", " (high-protein carnivore recovery diet)"
        ),
    ),
    ("hedgehog", "Acute Renal Failure"): (
        UROLITH_TEMPLATE_JA_SIG,
        CKD_ON_AKI_EN_SIG,
        _small_mammal_aki(
            "ハリネズミ",
            "hedgehogs",
            "（ふやかしフード、環境温24-29℃で偽冬眠を防止）",
            " (softened food; 24-29°C ambient to prevent torpor)",
        ),
    ),
    ("sugar_glider", "Acute Renal Failure"): (
        UROLITH_TEMPLATE_JA_SIG,
        CKD_ON_AKI_EN_SIG,
        _small_mammal_aki(
            "フクロモモンガ", "sugar gliders", "（加温・少量頻回給餌）", " (warmth and small frequent feeds)"
        ),
    ),
    ("parakeet", "Urolithiasis"): (UROLITH_TEMPLATE_JA_SIG, SMALL_MAMMAL_UROLITH_EN_SIG, _AVIAN_UROLITH),
    ("parrot", "Urolithiasis"): (UROLITH_TEMPLATE_JA_SIG, SMALL_MAMMAL_UROLITH_EN_SIG, _AVIAN_UROLITH),
}


def en_backfill_treatment(species: str, name_en: str) -> dict | None:
    """Return the curated EN treatment for a JA-informative/EN-templated record."""
    return EN_BACKFILL_TREATMENTS.get(((species or "").lower(), name_en or ""))


def ja_mistemplate_fix(species: str, name_en: str) -> tuple[str, str, dict] | None:
    """Return (JA gate, EN gate, fields) for records with a wrong-category template."""
    return JA_MISTEMPLATE_FIXES.get(((species or "").lower(), name_en or ""))
