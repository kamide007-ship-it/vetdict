"""Drug batch 39 – referenced-but-absent agents surfaced by the 2026-08 audit (7th sweep).

A katakana token-frequency sweep of disease treatment protocols plus an
antidote/reversal cross-reference audit of the formulary's own entries found
three agents that VetDict's own content instructs clinicians to use — yet were
absent from the formulary:

  - プロタミン硫酸塩 (protamine sulfate): the heparin reversal agent. The
    formulary's own heparin (unfractionated), enoxaparin and dalteparin
    entries name protamine as the antidote ("プロタミン部分中和(~60%)"), yet
    the antidote itself was not carried — the same self-referential gap class
    as pralidoxime (organophosphates) and dexrazoxane (doxorubicin) fixed in
    earlier sweeps.
  - ヒドロコルチゾンコハク酸エステル (hydrocortisone sodium succinate): the
    standard glucocorticoid for the Addisonian (hypoadrenocortical) crisis and
    for CIRCI in septic shock; referenced in disease treatment texts but
    absent. Unlike dexamethasone it provides both glucocorticoid and
    mineralocorticoid activity and is the consensus choice once ACTH
    stimulation testing is complete (or when dexamethasone was used to bridge).
  - 高張食塩水 7.2-7.5% (hypertonic saline): named in shock / GDV / head
    trauma protocols for small-volume resuscitation; completes the fluid set
    started with LRS / Normosol-R (batch 34). Rapid intravascular volume
    expansion at ~4-5x the infused volume; first-line for intracranial
    hypertension alongside mannitol.

References:
  - Plumb's Veterinary Drug Handbook, 10th ed — protamine sulfate,
    hydrocortisone sodium succinate, hypertonic saline.
  - Silverstein DC, Hopper K. Small Animal Critical Care Medicine, 3rd ed —
    hypertonic saline resuscitation doses (dog 4-7 mL/kg, cat 2-4 mL/kg),
    traumatic brain injury use.
  - Lunsford KV, Mackin AJ. Vet Clin North Am 2007 — heparin/LMWH reversal;
    protamine neutralises UFH fully but LMWH anti-Xa activity only ~60%.
  - Church DB. Canine hypoadrenocorticism. In: Ettinger 8th ed —
    hydrocortisone CRI for Addisonian crisis.
  - Lathan P, Thompson AL. Vet Med (Auckl) 2018 — management of
    hypoadrenocorticism; hydrocortisone 0.5 mg/kg/h CRI.
  - Sharp CR et al. J Vet Emerg Crit Care 2018 — hydrocortisone for CIRCI in
    septic dogs.
  - DiBartola SP. Fluid, Electrolyte, and Acid-Base Disorders, 4th ed —
    hypertonic saline contraindications (dehydration, hypernatremia).
"""

DRUGS_BATCH_39: list[dict] = [
    {
        "id": "protamine_sulfate",
        "search_aliases": [
            "プロタミン",
            "硫酸プロタミン",
            "Protamine",
        ],
        "name": "Protamine Sulfate",
        "name_ja": "プロタミン硫酸塩",
        "category": "miscellaneous",
        "mechanism": "Strongly basic (arginine-rich) protein that forms an inert ionic complex with strongly acidic heparin, immediately neutralising its anticoagulant effect. Fully reverses unfractionated heparin; neutralises only ~60% of LMWH (enoxaparin/dalteparin) anti-Xa activity. Excess protamine itself has weak anticoagulant activity, so dosing is titrated to the heparin given.",
        "mechanism_ja": "強塩基性（アルギニン豊富）蛋白で、強酸性のヘパリンとイオン複合体を形成し抗凝固作用を即時中和する。未分画ヘパリンは完全に、LMWH（エノキサパリン/ダルテパリン）の抗Xa活性は約60%のみ中和。プロタミン自体も過量で弱い抗凝固作用を持つため、投与ヘパリン量に合わせて滴定する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1 mg IV per 100 IU of heparin still active, by slow IV over 10+ min (max 50 mg). Reduce to 0.5 mg/100 IU if 30-60 min since heparin, 0.25 mg/100 IU if >2 h. LMWH: 1 mg per 1 mg (100 anti-Xa IU) enoxaparin — expect only partial (~60%) reversal.",
                "dosage_ja": "残存ヘパリン100 IUあたり1 mgを10分以上かけて緩徐静注（最大50 mg）。ヘパリン投与後30-60分なら0.5 mg/100 IU、2時間以降は0.25 mg/100 IUに減量。LMWH: エノキサパリン1 mg（抗Xa 100 IU）あたり1 mg — 中和は部分的（約60%）。",
                "notes": "Rapid injection causes hypotension, bradycardia and anaphylactoid reactions — always give slowly. Monitor aPTT/ACT to confirm reversal.",
                "notes_ja": "急速静注は低血圧・徐脈・アナフィラキシー様反応を起こす — 必ず緩徐投与。aPTT/ACTで中和を確認。",
            },
            "cat": {
                "safe": True,
                "dosage": "1 mg IV per 100 IU of heparin still active, slow IV over 10+ min; same time-decay reduction as dogs.",
                "dosage_ja": "残存ヘパリン100 IUあたり1 mgを10分以上かけて緩徐静注。犬と同様に経過時間で減量。",
                "notes": "Cats given protamine for ATE thrombolysis-associated bleeding: monitor closely for hypotension.",
                "notes_ja": "ATE治療関連出血への使用時は低血圧を厳重モニタリング。",
            },
            "horse": {
                "safe": True,
                "dosage": "1 mg IV per 100 IU heparin still active, very slow IV; titrate against ACT.",
                "dosage_ja": "残存ヘパリン100 IUあたり1 mgを極めて緩徐に静注。ACTで滴定。",
                "notes": "Rarely required; heparin's short half-life usually makes discontinuation sufficient.",
                "notes_ja": "必要となることは稀 — ヘパリンは半減期が短く中止のみで十分なことが多い。",
            },
        },
        "side_effects": "Hypotension, bradycardia, pulmonary hypertension and anaphylactoid reactions with rapid IV injection; rebound bleeding (heparin rebound) 2-8 h later; excess protamine is itself weakly anticoagulant",
        "side_effects_ja": "急速静注で低血圧・徐脈・肺高血圧・アナフィラキシー様反応。2-8時間後のヘパリンリバウンド出血。過量投与はプロタミン自体の弱い抗凝固作用",
        "contraindications": "Known protamine hypersensitivity. Use caution in animals previously exposed to protamine-containing insulin (PZI/NPH) — higher anaphylaxis risk.",
        "contraindications_ja": "プロタミン過敏症。プロタミン含有インスリン（PZI/NPH）使用歴のある動物はアナフィラキシーリスク上昇 — 慎重投与。",
        "drug_interactions": [
            {
                "drug": "Heparin (unfractionated)",
                "effect": "Intended antagonism — full neutralisation; dose by remaining active heparin",
                "severity": "info",
            },
            {
                "drug": "Enoxaparin",
                "effect": "Partial (~60%) neutralisation of anti-Xa activity only",
                "severity": "moderate",
            },
            {
                "drug": "Insulin PZI",
                "effect": "Prior exposure to protamine-containing insulin increases anaphylaxis risk on IV protamine",
                "severity": "moderate",
            },
        ],
    },
    {
        "id": "hydrocortisone_succinate",
        "search_aliases": [
            "ヒドロコルチゾン",
            "コハク酸ヒドロコルチゾン",
            "ソル・コーテフ",
            "Solu-Cortef",
        ],
        "name": "Hydrocortisone Sodium Succinate",
        "name_ja": "ヒドロコルチゾンコハク酸エステル（ソル・コーテフ）",
        "category": "corticosteroids",
        "mechanism": "Water-soluble ester of cortisol providing physiological glucocorticoid AND appreciable mineralocorticoid activity — the reason it is preferred over dexamethasone for ongoing Addisonian crisis management (dexamethasone has no mineralocorticoid effect but does not cross-react with the cortisol assay, so it is used only to bridge until ACTH stimulation testing is done). Also used at physiological doses for critical-illness-related corticosteroid insufficiency (CIRCI) in septic shock.",
        "mechanism_ja": "コルチゾールの水溶性エステルで、生理的グルココルチコイド作用に加え相応のミネラルコルチコイド作用を持つ — アジソンクリーゼの継続管理でデキサメタゾンより推奨される理由（デキサメタゾンはミネラルコルチコイド作用を欠くが、コルチゾール測定と交差しないためACTH刺激試験完了までのつなぎに用いる）。敗血症性ショックの相対的副腎皮質機能低下（CIRCI）にも生理量で使用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Addisonian crisis: 0.5 mg/kg/h IV CRI, or 2-4 mg/kg IV q6h, after fluid resuscitation; taper to oral replacement over 2-3 days. CIRCI in septic shock (vasopressor-refractory): 1 mg/kg/day CRI or divided q6h.",
                "dosage_ja": "アジソンクリーゼ: 輸液蘇生後に0.5 mg/kg/h 静脈内CRI、または2-4 mg/kg IV q6h。2-3日かけて経口補充へ漸減。敗血症性ショックのCIRCI（昇圧薬抵抗性）: 1 mg/kg/日 CRIまたはq6h分割。",
                "notes": "Cross-reacts with cortisol assays — draw the ACTH stimulation test BEFORE the first dose (use dexamethasone if steroid cover cannot wait). Continue IV fluids and monitor Na/K.",
                "notes_ja": "コルチゾール測定と交差する — 初回投与前にACTH刺激試験の採血を済ませること（待てない場合はデキサメタゾンでつなぐ）。輸液を継続しNa/Kをモニタリング。",
            },
            "cat": {
                "safe": True,
                "dosage": "Addisonian crisis (rare in cats): 0.5 mg/kg/h IV CRI or 2-4 mg/kg IV q6h after volume resuscitation.",
                "dosage_ja": "アジソンクリーゼ（猫では稀）: 容量蘇生後に0.5 mg/kg/h CRIまたは2-4 mg/kg IV q6h。",
                "notes": "Feline crises respond more slowly than canine — continue parenteral support 3-5 days.",
                "notes_ja": "猫のクリーゼは犬より反応が遅い — 非経口サポートを3-5日継続。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Hypoadrenocorticism after bilateral adrenalectomy: 1-2 mg/kg IV/IM initially, then oral glucocorticoid replacement.",
                "dosage_ja": "両側副腎摘出後の副腎皮質機能低下: 初回1-2 mg/kg IV/IM、以後経口グルココルチコイド補充へ。",
                "notes": "Anticipate crisis after bilateral adrenal surgery for ferret adrenal disease.",
                "notes_ja": "フェレット副腎疾患の両側摘出術後はクリーゼを予期して準備。",
            },
        },
        "side_effects": "PU/PD, polyphagia; GI ulceration at supraphysiological doses; hyperglycemia; immunosuppression with prolonged use; sodium retention (by design in Addisonian use)",
        "side_effects_ja": "多飲多尿・多食。超生理量で消化管潰瘍。高血糖。長期使用で免疫抑制。ナトリウム貯留（アジソン病治療では意図した作用）",
        "contraindications": "Systemic fungal infection without antifungal cover; do not use supraphysiological doses in septic shock (physiological CIRCI dosing only); GI ulceration/perforation",
        "contraindications_ja": "抗真菌薬併用のない全身性真菌感染。敗血症性ショックでの超生理量投与は不可（CIRCIは生理量のみ）。消化管潰瘍・穿孔",
        "drug_interactions": [
            {
                "drug": "NSAIDs",
                "effect": "Combined GI ulceration risk — do not co-administer",
                "severity": "major",
            },
            {
                "drug": "Insulin",
                "effect": "Glucocorticoid-induced insulin resistance raises insulin requirement",
                "severity": "moderate",
            },
            {
                "drug": "Desoxycorticosterone (DOCP)",
                "effect": "Complementary — DOCP provides long-term mineralocorticoid replacement once crisis is controlled",
                "severity": "info",
            },
        ],
    },
    {
        "id": "hypertonic_saline",
        "search_aliases": [
            "高張食塩水",
            "7.2%食塩水",
            "7.5%食塩水",
            "高張生理食塩水",
            "Hypertonic saline",
        ],
        "name": "Hypertonic Saline 7.2-7.5%",
        "name_ja": "高張食塩水（7.2-7.5%）",
        "category": "miscellaneous",
        "mechanism": "Small-volume resuscitation fluid: the steep osmotic gradient pulls interstitial and intracellular water into the vasculature, expanding intravascular volume by ~4-5x the infused volume within minutes. In traumatic brain injury it reduces intracranial pressure by osmotically shrinking brain parenchyma while — unlike mannitol — supporting arterial pressure. Effect is transient (30-60 min); follow with isotonic crystalloids.",
        "mechanism_ja": "少量蘇生輸液: 急峻な浸透圧勾配により間質・細胞内水分を血管内へ引き込み、数分で投与量の約4-5倍の血管内容量増加を得る。頭部外傷では脳実質を浸透圧的に縮小させ頭蓋内圧を下げつつ、マンニトールと異なり動脈圧を維持する。効果は一過性（30-60分）— 等張晶質液で後続する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Shock (incl. GDV pre-op): 4-7 mL/kg IV over 5-10 min, once. Traumatic brain injury / intracranial hypertension: 3-5 mL/kg IV over 10-15 min. Follow with isotonic crystalloids.",
                "dosage_ja": "ショック（GDV術前含む）: 4-7 mL/kg を5-10分かけて単回静注。頭部外傷・頭蓋内圧亢進: 3-5 mL/kg を10-15分かけて静注。等張晶質液で後続。",
                "notes": "Ideal when large-volume crystalloid is impractical (GDV: rapid pre-op stabilisation with small volume). Do not exceed 1 mL/kg/min (bradycardia/hypotension via vagal reflex).",
                "notes_ja": "大量晶質液投与が困難な場面（GDVの術前迅速安定化等）に最適。1 mL/kg/分を超えない（迷走神経反射による徐脈・低血圧）。",
            },
            "cat": {
                "safe": True,
                "dosage": "Shock: 2-4 mL/kg IV over 10 min. TBI: 2-4 mL/kg over 10-15 min.",
                "dosage_ja": "ショック: 2-4 mL/kg を10分かけて静注。頭部外傷: 2-4 mL/kg を10-15分。",
                "notes": "Cats are volume-sensitive — use the lower end and reassess before repeating.",
                "notes_ja": "猫は容量過負荷に敏感 — 低用量側を用い、再投与前に再評価。",
            },
            "horse": {
                "safe": True,
                "dosage": "Hypovolemic/endotoxemic shock: 2-4 mL/kg IV over 10-15 min (adult ~1-2 L of 7.2%), followed immediately by isotonic crystalloids at 2-4x the deficit.",
                "dosage_ja": "循環血液量減少・エンドトキシンショック: 2-4 mL/kg を10-15分で静注（成馬で7.2%液 約1-2 L）。直後から等張晶質液を欠乏量の2-4倍で後続。",
                "notes": "Standard field stabilisation for colic shock before referral — buys time when large-volume replacement is impossible in transit.",
                "notes_ja": "疝痛ショックの搬送前安定化の標準 — 搬送中の大量輸液が不可能な状況で時間を稼ぐ。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Shock: 3 mL/kg IV/IO over 10 min, followed by isotonic crystalloids.",
                "dosage_ja": "ショック: 3 mL/kg を10分かけてIV/IO投与し、等張晶質液で後続。",
                "notes": "Useful when IV volume loading is limited by small patient size.",
                "notes_ja": "小柄で大量輸液が難しい場合に有用。",
            },
        },
        "side_effects": "Transient hypernatremia/hyperchloremia; bradycardia and hypotension with rapid bolus (vagally mediated); phlebitis; rebound intracranial hypertension if used repeatedly without monitoring sodium",
        "side_effects_ja": "一過性の高Na・高Cl血症。急速ボーラスで迷走神経性の徐脈・低血圧。静脈炎。Na監視なしの反復投与でリバウンド性頭蓋内圧亢進",
        "contraindications": "Dehydration (interstitial water is the source of the volume effect — rehydrate first or concurrently), pre-existing hypernatremia, uncontrolled hemorrhage (relative — raises pressure before surgical control), cardiac disease with volume overload risk",
        "contraindications_ja": "脱水（容量効果の源は間質水分 — 先行/同時の補水が必須）、既存の高Na血症、未制御の出血（相対的 — 外科的止血前の昇圧）、容量過負荷リスクのある心疾患",
        "drug_interactions": [
            {
                "drug": "Mannitol",
                "effect": "Complementary osmotherapy for intracranial hypertension — hypertonic saline preferred when hypotensive",
                "severity": "info",
            },
            {
                "drug": "Lactated Ringer's Solution",
                "effect": "Required follow-on isotonic crystalloid after the transient volume effect",
                "severity": "info",
            },
        ],
    },
]
