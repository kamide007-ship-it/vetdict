"""Drug batch 42 – referenced-but-absent agents surfaced by the 2026-08 audit (10th sweep).

A katakana token sweep of disease treatment protocols, cross-checked with the
real text matcher (find_drugs_in_text), found two agents that VetDict's own
content instructs clinicians to use — with explicit doses — yet were absent
from the formulary:

  - 生理食塩水 (0.9% sodium chloride / normal saline): referenced ~293 times
    across treatment protocols (fluid of choice for hypercalcemia, saline
    nebulization q4-6h in pneumonia protocols, wound lavage, blood-product
    co-administration). The formulary carried LRS, Normosol-R/Plasma-Lyte A
    and 7.2% hypertonic saline, but not the isotonic 0.9% solution itself —
    a self-referential gap, and one worth closing explicitly so 0.9% and
    7.2% solutions are never conflated.
  - コレカルシフェロール (cholecalciferol / native vitamin D3): referenced
    ~96 times ("ビタミンD3（コレカルシフェロール）4,000-6,000 IU/kg/日 PO"
    in hypoparathyroidism/hypocalcemia protocols; oral D3 supplementation in
    reptile NSHP entries). Only the active metabolite calcitriol was carried.

References:
  - DiBartola SP. Fluid, Electrolyte, and Acid-Base Disorders in Small
    Animal Practice, 4th ed — 0.9% NaCl composition (Na 154 / Cl 154 mEq/L,
    308 mOsm/L), hyperchloremic (dilutional) acidosis with large volumes,
    fluid of choice for hypercalcemia and hypochloremic metabolic alkalosis.
  - Davis H et al. 2013 AAHA/AAFP Fluid Therapy Guidelines for Dogs and
    Cats — shock: dog up to 80-90 mL/kg/h given as 10-20 mL/kg titrated
    boluses; cat up to 40-60 mL/kg/h as 5-10 mL/kg boluses; reassess after
    each bolus.
  - Plumb's Veterinary Drug Handbook, 10th ed — sodium chloride 0.9%;
    vitamin D analog comparison (cholecalciferol vs calcitriol onset/offset).
  - Feldman EC, Nelson RW. Canine and Feline Endocrinology, 4th ed —
    primary hypoparathyroidism: calcitriol preferred (rapid onset, short
    half-life allows titration); native vitamin D 4,000-6,000 IU/kg/day PO
    initial as the historical alternative with prolonged-toxicity caveat.
  - Mader's Reptile and Amphibian Medicine and Surgery, 3rd ed — NSHP:
    correction of husbandry (UV-B, dietary Ca) is primary; oral vitamin D3
    200-400 IU/kg PO weekly as adjunct; parenteral vitamin D risks
    soft-tissue mineralization.
  - Rumbeiha WK. Cholecalciferol rodenticide toxicosis — narrow margin;
    hypercalcemia/hyperphosphatemia with renal injury; weeks-long tissue
    half-life.
"""

DRUGS_BATCH_42: list[dict] = [
    {
        "id": "normal_saline",
        "search_aliases": [
            "生理食塩水",
            "生理食塩液",
            "生食",
            "0.9%食塩水",
            "0.9%塩化ナトリウム",
            "等張食塩水",
            "Normal saline",
            "0.9% NaCl",
            "Isotonic saline",
        ],
        "name": "Sodium Chloride 0.9% (Normal Saline)",
        "name_ja": "生理食塩水（0.9%塩化ナトリウム）",
        "category": "miscellaneous",
        "mechanism": "Isotonic non-buffered crystalloid (Na 154 / Cl 154 mEq/L, ~308 mOsm/L; no K, Ca or buffer). Expands extracellular volume; supraphysiologic chloride makes it mildly acidifying — large volumes cause dilutional hyperchloremic metabolic acidosis, so balanced crystalloids (LRS, Normosol-R) are preferred for most resuscitation. It is the fluid of choice when a calcium- and potassium-free, chloride-rich solution is wanted: hypercalcemia (saline diuresis promotes calciuresis), hypochloremic metabolic alkalosis (upper-GI obstruction/vomiting), hyperkalemia, and co-administration with blood products (no calcium to trigger citrate clotting, unlike LRS). Also the standard vehicle for saline nebulization and sterile wound lavage.",
        "mechanism_ja": "等張・無緩衝の晶質液（Na 154・Cl 154 mEq/L、約308 mOsm/L。K・Ca・緩衝剤を含まない）。細胞外液を増量する。塩素が生理値より高く軽度の酸性化作用があり、大量投与で希釈性の高Cl性代謝性アシドーシスを起こすため、一般的な蘇生には平衡型晶質液（乳酸リンゲル・ノルモソルR）が優先される。一方、Ca・Kを含まず塩素に富む輸液が望ましい場面では第一選択: 高カルシウム血症（生食利尿によるCa排泄促進）、低Cl性代謝性アルカローシス（上部消化管閉塞・嘔吐）、高カリウム血症、血液製剤との同一ライン投与（乳酸リンゲルと異なりクエン酸凝固を起こすCaを含まない）。ネブライゼーションの標準溶媒・滅菌創傷洗浄液でもある。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Shock: 10-20 mL/kg IV boluses titrated to effect (up to 80-90 mL/kg total; reassess perfusion after each bolus — AAHA/AAFP 2013). Rehydration: replace deficit over 6-24 h. Maintenance: 40-60 mL/kg/day. Hypercalcemia: 2-3x maintenance IV (saline diuresis). Nebulization: 0.9% sterile saline q4-6h.",
                "dosage_ja": "ショック: 10-20 mL/kg を効果を見ながらボーラス静注（総量80-90 mL/kgまで。各ボーラス後に灌流を再評価 — AAHA/AAFP 2013）。脱水補正: 欠乏量を6-24時間で補充。維持: 40-60 mL/kg/日。高カルシウム血症: 維持量の2-3倍で静注（生食利尿）。ネブライゼーション: 滅菌生理食塩水 4-6時間毎。",
                "notes": "Prefer balanced crystalloids for most resuscitation; choose 0.9% NaCl specifically for hypercalcemia, hyperkalemia, hypochloremic alkalosis, or when running blood products. Supplement K in maintenance use (solution is K-free).",
                "notes_ja": "一般的な蘇生は平衡型晶質液を優先。高カルシウム血症・高カリウム血症・低Cl性アルカローシス・血液製剤投与時にこそ0.9%塩化ナトリウムを選択する。維持輸液に使う場合はK補給を併用（K非含有のため）。",
            },
            "cat": {
                "safe": True,
                "dosage": "Shock: 5-10 mL/kg IV boluses titrated (up to 40-60 mL/kg total — AAHA/AAFP 2013). Maintenance: 40-60 mL/kg/day. Urethral obstruction: standard initial fluid alongside decompression; switch or supplement K once post-obstructive diuresis begins.",
                "dosage_ja": "ショック: 5-10 mL/kg を効果を見ながらボーラス静注（総量40-60 mL/kgまで — AAHA/AAFP 2013）。維持: 40-60 mL/kg/日。尿道閉塞: 減圧と並行する初期輸液の標準。閉塞解除後利尿が始まったらK補給に切替・追加。",
                "notes": "Cats are volume-overload prone — titrate in small boluses and auscultate for gallop/crackles between boluses.",
                "notes_ja": "猫は容量過負荷を起こしやすい — 少量ボーラスで漸増し、ボーラス間で奔馬調律・肺クラックルを聴診。",
            },
            "horse": {
                "safe": True,
                "dosage": "Shock: 10-20 mL/kg IV rapid bolus, reassess and repeat as needed (adult ~5-10 L per bolus). Rehydration/maintenance: 50-100 mL/kg/day. Hypercalcemia or blood-product co-administration: fluid of choice.",
                "dosage_ja": "ショック: 10-20 mL/kg を急速静注し再評価のうえ反復（成馬で1回約5-10 L）。脱水補正・維持: 50-100 mL/kg/日。高カルシウム血症・血液製剤との同時投与では第一選択。",
                "notes": "For most colic resuscitation balanced crystalloids are preferred; monitor chloride and acid-base with large volumes.",
                "notes_ja": "疝痛蘇生の多くは平衡型晶質液が優先。大量投与時はClと酸塩基をモニタリング。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Shock: 10 mL/kg IV/IO boluses titrated. SC rehydration: 60-100 mL/kg/day divided, warmed to body temperature.",
                "dosage_ja": "ショック: 10 mL/kg をIV/IOでボーラス漸増。皮下補液: 60-100 mL/kg/日を分割、体温程度に加温して投与。",
                "notes": "Warm all fluids for small mammals (hypothermia risk).",
                "notes_ja": "小型哺乳類では必ず輸液を加温（低体温リスク）。",
            },
            "bird": {
                "safe": True,
                "dosage": "Shock: 10 mL/kg IV/IO slow bolus. SC: 50-100 mL/kg/day divided (inguinal/interscapular web), warmed.",
                "dosage_ja": "ショック: 10 mL/kg をIV/IOで緩徐ボーラス。皮下: 50-100 mL/kg/日を分割（鼠径部・肩甲間膜）、加温して投与。",
                "notes": "Warmed fluids are critical in birds; combine with heat support.",
                "notes_ja": "鳥では輸液加温が必須。保温と併用する。",
            },
            "reptile": {
                "safe": True,
                "dosage": "10-25 mL/kg/day SC/intracoelomic/PO, warmed to the species' POTZ. Many clinicians dilute to ~0.6-0.8% ('reptile saline') for chronic dehydration.",
                "dosage_ja": "10-25 mL/kg/日 を皮下・体腔内・経口で、種のPOTZ温度に加温して投与。慢性脱水では約0.6-0.8%に希釈した低張液を用いる臨床家も多い。",
                "notes": "Administer at POTZ temperature; cold fluids depress reptile physiology.",
                "notes_ja": "POTZ温度で投与する。冷たい輸液は爬虫類の生理機能を抑制する。",
            },
        },
        "side_effects": "Dilutional hyperchloremic metabolic acidosis with large volumes; hypokalemia with prolonged K-free administration; volume overload (pulmonary edema) — especially cats and cardiac patients",
        "side_effects_ja": "大量投与で希釈性の高Cl性代謝性アシドーシス。K非含有のため長期投与で低カリウム血症。容量過負荷（肺水腫）— 特に猫・心疾患例",
        "contraindications": "Congestive heart failure / volume-overload states (relative). Chronic hyponatremia — correct slowly (≤0.5 mEq/L/h, ≤10-12 mEq/L/day; risk of osmotic demyelination). Not a maintenance fluid without K supplementation.",
        "contraindications_ja": "うっ血性心不全・容量過負荷状態（相対的）。慢性低ナトリウム血症では緩徐に補正（0.5 mEq/L/時以下、10-12 mEq/L/日以下 — 浸透圧性脱髄のリスク）。K補給なしの維持輸液には不適。",
        "drug_interactions": [
            {
                "drug": "Lactated Ringer's Solution",
                "effect": "Balanced alternative preferred for most resuscitation; 0.9% NaCl preferred for hypercalcemia, hyperkalemia and blood-product lines",
                "effect_ja": "一般的な蘇生では平衡型（乳酸リンゲル）が優先。高Ca血症・高K血症・血液製剤ラインでは0.9%塩化ナトリウムを優先",
                "severity": "info",
            },
            {
                "drug": "Hypertonic Saline 7.2-7.5%",
                "effect": "Do NOT confuse: 7.2-7.5% is a small-volume resuscitation fluid (mL/kg single doses) — never given at isotonic volumes",
                "effect_ja": "混同厳禁: 7.2-7.5%高張食塩水は少量蘇生用（mL/kg単回）であり、等張液の容量では決して投与しない",
                "severity": "major",
            },
        ],
    },
    {
        "id": "cholecalciferol",
        "search_aliases": [
            "コレカルシフェロール",
            "ビタミンD3",
            "ビタミンD3製剤",
            "Cholecalciferol",
            "Vitamin D3",
        ],
        "name": "Cholecalciferol (Vitamin D3)",
        "name_ja": "コレカルシフェロール（ビタミンD3）",
        "category": "miscellaneous",
        "mechanism": "Native vitamin D3. Requires hepatic 25-hydroxylation then renal 1α-hydroxylation to the active hormone calcitriol, so onset is slow (days-weeks) and tissue half-life very long (weeks) — toxicity, once produced, is prolonged. Increases intestinal calcium and phosphorus absorption and bone mobilization. For chronic hypocalcemia (hypoparathyroidism) calcitriol is preferred because its rapid onset and short half-life allow titration; cholecalciferol is the historical/alternative agent. In reptiles it supports NSHP correction when UV-B provision and dietary calcium — the primary treatment — are being restored.",
        "mechanism_ja": "天然型ビタミンD3。肝で25位水酸化、腎で1α位水酸化を受けて活性型（カルシトリオール）となるため、作用発現が遅く（数日〜数週）、組織半減期が極めて長い（数週間）— いったん生じた中毒は遷延する。腸管でのCa・P吸収と骨からの動員を増加させる。慢性低カルシウム血症（上皮小体機能低下症）では、作用発現が速く半減期が短いため用量調節しやすいカルシトリオールが優先され、コレカルシフェロールは歴史的・代替的選択。爬虫類ではUV-B照射と食餌Ca是正（NSHPの主治療）の回復を補助する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Hypoparathyroidism (alternative to calcitriol): 4,000-6,000 IU/kg PO q24h initially, tapered to the lowest dose maintaining low-normal serum calcium (often 1,000-2,000 IU/kg/day); recheck ionized Ca weekly during titration (Feldman & Nelson 4th ed). Calcitriol 20-30 ng/kg/day is preferred when available.",
                "dosage_ja": "上皮小体機能低下症（カルシトリオールの代替）: 初期 4,000-6,000 IU/kg 経口 24時間毎、血清Caを正常低値に保つ最小量（多くは1,000-2,000 IU/kg/日）まで漸減。調節期はイオン化Caを週1回再検（Feldman & Nelson 4th ed）。入手可能ならカルシトリオール 20-30 ng/kg/日を優先。",
                "notes": "Slow onset (5-21 days) and weeks-long washout — overshoot causes prolonged hypercalcemia. Target LOW-normal calcium to protect kidneys.",
                "notes_ja": "作用発現が遅く（5-21日）、消失にも数週間 — 過量は遷延性の高Ca血症となる。腎保護のため血清Caは正常低値を目標にする。",
            },
            "cat": {
                "safe": True,
                "dosage": "Hypoparathyroidism (alternative to calcitriol): 4,000-6,000 IU/kg PO q24h initially with taper as for dogs; ionized Ca monitoring weekly during titration.",
                "dosage_ja": "上皮小体機能低下症（カルシトリオールの代替）: 初期 4,000-6,000 IU/kg 経口 24時間毎、犬と同様に漸減。調節期はイオン化Caを週1回モニタリング。",
                "notes": "Post-thyroidectomy hypocalcemia is the classic feline indication; calcitriol preferred for titratability.",
                "notes_ja": "甲状腺摘出後の低Ca血症が猫の古典的適応。調節性の面でカルシトリオールが優先。",
            },
            "reptile": {
                "safe": True,
                "dosage": "NSHP adjunct: 200-400 IU/kg PO weekly while correcting UV-B and dietary calcium (Mader 3rd ed). Oral route preferred.",
                "dosage_ja": "NSHP補助: 200-400 IU/kg 経口 週1回（UV-B照射と食餌Caの是正と並行 — Mader 3rd ed）。経口投与を優先。",
                "notes": "Husbandry correction (UV-B, Ca:P ratio) is the primary treatment — vitamin D3 alone does not fix NSHP. Avoid repeated parenteral vitamin D (soft-tissue mineralization).",
                "notes_ja": "主治療は飼育環境の是正（UV-B、Ca:P比）— ビタミンD3単独ではNSHPは治らない。ビタミンDの反復非経口投与は避ける（軟部組織石灰化）。",
            },
            "bird": {
                "safe": True,
                "dosage": "Deficiency states: dietary correction (formulated diet) is primary; short-term supplementation 200-500 IU/kg PO weekly if needed.",
                "dosage_ja": "欠乏症: 食餌是正（ペレット化フード）が第一。必要時のみ短期補充 200-500 IU/kg 経口 週1回。",
                "notes": "Excess vitamin D3 in birds (especially macaws) causes renal mineralization — supplement conservatively.",
                "notes_ja": "鳥（特にコンゴウインコ類）のビタミンD3過剰は腎石灰化を起こす — 補充は控えめに。",
            },
        },
        "side_effects": "Hypercalcemia and hyperphosphatemia (anorexia, PU/PD, vomiting, weakness) progressing to soft-tissue/renal mineralization and renal failure — the same syndrome as cholecalciferol rodenticide toxicosis; prolonged because of weeks-long tissue half-life",
        "side_effects_ja": "高Ca血症・高P血症（食欲不振・多飲多尿・嘔吐・脱力）→ 軟部組織・腎石灰化、腎不全へ進行 — コレカルシフェロール系殺鼠剤中毒と同一の病態。組織半減期が長く遷延する",
        "contraindications": "Hypercalcemia, hyperphosphatemia, renal failure with Ca×P >60-70, nephrocalcinosis. Never exceed dosing — this molecule is also used as a rodenticide; narrow therapeutic margin.",
        "contraindications_ja": "高Ca血症、高P血症、Ca×P積>60-70の腎不全、腎石灰化。用量厳守 — 本分子は殺鼠剤成分でもあり治療域が狭い。",
        "drug_interactions": [
            {
                "drug": "Calcitriol",
                "effect": "Preferred alternative for chronic hypocalcemia (rapid onset, short half-life, titratable) — do not combine",
                "effect_ja": "慢性低Ca血症ではカルシトリオールが優先（発現が速く半減期が短く調節可能）— 併用しない",
                "severity": "info",
            },
            {
                "drug": "Calcium Gluconate",
                "effect": "Combined in acute-phase hypocalcemia management; monitor ionized Ca to avoid overshoot hypercalcemia",
                "effect_ja": "急性期の低Ca血症管理で併用。イオン化Caを監視し過剰補正（高Ca血症）を回避",
                "severity": "info",
            },
            {
                "drug": "Thiazide diuretics",
                "effect": "Reduce renal calcium excretion — increased hypercalcemia risk during vitamin D therapy",
                "effect_ja": "腎Ca排泄を低下させる — ビタミンD療法中の高Ca血症リスク増大",
                "severity": "moderate",
            },
        ],
    },
]
