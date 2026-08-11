"""Drug batch 34 – referenced-but-absent agents surfaced by the 2026-08 audit (2nd sweep).

An is-referenced-but-absent sweep of (a) disease treatment protocols in
diseases_all_species.json, (b) drug_interactions back-references and (c) the
anesthesia/emergency content found 11 agents that VetDict's own content tells
clinicians to use but the formulary did not carry:

  - Vinblastine        — 408 disease entries reference it (mast cell tumor
                         standard of care: vinblastine + prednisolone), yet only
                         vincristine was in the formulary. Vesicant + nadir info.
  - Lactated Ringer's  — 710 treatment entries name 乳酸リンゲル; fluid therapy is
                         the single most-referenced intervention in the DB with
                         no crystalloid entry at all (only colloids/lipid).
  - Normosol-R /       — 1,059 treatment entries name ノルモソル; acetate-buffered
    Plasma-Lyte A        calcium-free balanced crystalloid (blood-compatible).
  - L-theanine         — 41 behavioral-disease entries (Anxitane).
  - Alpha-casozepine   — 33 behavioral-disease entries (Zylkene).
  - Povidone-iodine    — 48 entries (wound/shell-rot antisepsis); chlorhexidine
                         was present but the iodophor alternative was not.
  - Folic acid         — pyrimethamine/sulfadiazine EPM regimen and chronic
                         enteropathy entries reference folate supplementation;
                         carries the pregnant-mare warning (Toribio 1998).
  - DMSO               — 49 entries (equine neuro/laminitis adjunct, doxorubicin
                         extravasation topical); dexrazoxane's entry references it.
  - Mineral oil        — 35 entries (equine large-colon impaction via NGT);
                         vitamin K1's interaction list references it. Carries the
                         mandatory aspiration/lipoid-pneumonia warning.
  - Lugol's iodine     — 48 entries (budgerigar goiter/thyroid hyperplasia
                         drinking-water iodine, matches the DB's 1 drop/250 mL).
  - Fluorescein        — 132 entries (corneal ulcer detection, Jones test, TFBUT);
                         the single most-referenced ophthalmic diagnostic.

References:
  - Plumb's Veterinary Drug Handbook, 10th ed.
  - Carpenter's Exotic Animal Formulary, 6th ed.
  - Thamm DH et al. Vet Comp Oncol 2006;4(1):8-15 — vinblastine/prednisolone for
    canine mast cell tumor (2 mg/m² IV protocol).
  - Davis H et al. J Am Anim Hosp Assoc 2013;49(3):149-159 — AAHA/AAFP fluid
    therapy guidelines (shock bolus / maintenance rates).
  - DiBartola SP. Fluid, Electrolyte, and Acid-Base Disorders in Small Animal
    Practice, 4th ed — crystalloid composition and selection.
  - Beata C et al. J Vet Behav 2007;2(2):40-46 — alpha-casozepine vs selegiline
    for canine anxiety (15 mg/kg PO q24h).
  - Berteselli GV, Michelazzi M. J Vet Behav 2007;2(3):101 — L-theanine in dogs.
  - Dramard V et al. Vet Rec Open 2018;5(1) — L-theanine in cats (25 mg q12h).
  - Reed SM et al. JVIM 2016;30(2):491-502 — EPM ACVIM consensus (folate
    monitoring under pyrimethamine/sulfonamide therapy).
  - Toribio RE et al. JAVMA 1998;212(5):697-701 — congenital defects in foals of
    mares on pyrimethamine/sulfa given oral folic acid supplementation.
  - Samour J. Avian Medicine, 3rd ed / Carpenter 6th ed — Lugol's iodine
    drinking-water protocol for budgerigar thyroid hyperplasia.
  - Featherstone HJ, Heinrich CL. Veterinary Ophthalmology, 6th ed (Gelatt) —
    fluorescein staining, Jones test, tear-film breakup time.
"""

from __future__ import annotations

DRUGS_BATCH_34: list[dict] = [
    {
        "id": "vinblastine",
        "name": "Vinblastine",
        "name_ja": "ビンブラスチン",
        "category": "antineoplastics",
        "mechanism": (
            "Vinca alkaloid. Binds tubulin and blocks microtubule polymerisation, "
            "arresting mitosis in metaphase. Compared with vincristine it is more "
            "myelosuppressive but less neurotoxic and causes less ileus, which is why "
            "it is the vinca of choice in canine mast cell tumor protocols "
            "(vinblastine + prednisolone)."
        ),
        "mechanism_ja": (
            "ビンカアルカロイド。チューブリンに結合して微小管重合を阻害し、分裂中期で細胞分裂を停止させる。"
            "ビンクリスチンと比べ骨髄抑制は強いが神経毒性・イレウスは少なく、"
            "犬肥満細胞腫プロトコル（ビンブラスチン＋プレドニゾロン）で選択されるビンカ系薬剤。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "2 mg/m² IV bolus once weekly x 4, then every 2 weeks x 4 with "
                    "prednisolone for mast cell tumor (Thamm 2006). CBC before each "
                    "dose; delay if neutrophils < 3,000/uL."
                ),
                "dosage_ja": (
                    "2 mg/m² 静注ボーラス 週1回×4回、その後2週毎×4回（肥満細胞腫にプレドニゾロン併用、"
                    "Thamm 2006）。毎回投与前にCBC。好中球 < 3,000/μL なら延期。"
                ),
                "notes": (
                    "STRICT vesicant — administer through a first-stick, freely running "
                    "IV catheter. If extravasated: stop, aspirate, WARM compress "
                    "(vinca alkaloids; cold is for doxorubicin) ± hyaluronidase. "
                    "Myelosuppression nadir day 4-7, recovery by day 14."
                ),
                "notes_ja": (
                    "強い壊死起因性（vesicant）— 一発で確保した確実に開通した静脈カテーテルから投与。"
                    "血管外漏出時: 中止・吸引し温罨法（ビンカ系は温罨法。冷罨法はドキソルビシン用）"
                    "±ヒアルロニダーゼ。骨髄抑制の最下点は4-7日目、14日目までに回復。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": "1.5-2 mg/m² IV every 1-2 weeks (mast cell tumor, lymphoma rescue).",
                "dosage_ja": "1.5-2 mg/m² 静注 1-2週毎（肥満細胞腫、リンパ腫レスキュー）。",
                "notes": "Same vesicant precautions as dogs. Monitor CBC.",
                "notes_ja": "犬と同じ血管外漏出対策を徹底。CBCモニタリング。",
            },
        },
        "side_effects": (
            "Myelosuppression (neutropenia nadir day 4-7), GI upset (milder than "
            "vincristine), perivascular necrosis if extravasated, alopecia in "
            "non-shedding breeds."
        ),
        "side_effects_ja": (
            "骨髄抑制（好中球減少の最下点4-7日目）、消化器症状（ビンクリスチンより軽度）、"
            "血管外漏出時の血管周囲壊死、非換毛犬種での脱毛。"
        ),
        "contraindications": (
            "Severe pre-existing myelosuppression, active infection. Do not "
            "substitute 1:1 for vincristine (different doses and toxicity profiles)."
        ),
        "contraindications_ja": (
            "重度の既存骨髄抑制、活動性感染。ビンクリスチンと1:1で置き換え不可（用量・毒性プロファイルが異なる）。"
        ),
        "drug_interactions": [
            {
                "drug": "Other myelosuppressive drugs",
                "effect": "Additive bone-marrow suppression",
                "effect_ja": "骨髄抑制が相加的",
            },
            {
                "drug": "ketoconazole",
                "effect": "CYP3A4/P-gp inhibition raises vinblastine exposure and toxicity",
                "effect_ja": "CYP3A4/P-糖蛋白阻害によりビンブラスチン曝露・毒性が増加",
            },
            {
                "drug": "cyclosporine",
                "effect": "P-gp inhibition increases vinblastine toxicity",
                "effect_ja": "P-糖蛋白阻害によりビンブラスチン毒性増加",
            },
        ],
    },
    {
        "id": "lactated_ringers",
        "name": "Lactated Ringer's Solution (LRS)",
        "name_ja": "乳酸リンゲル液",
        "category": "miscellaneous",
        "mechanism": (
            "Isotonic balanced replacement crystalloid (Na 130, K 4, Ca 3, Cl 109 "
            "mEq/L, lactate 28 mEq/L; ~273 mOsm/L). Hepatic metabolism of lactate "
            "yields bicarbonate, giving a mild alkalinising effect. First-line fluid "
            "for shock resuscitation, dehydration replacement and maintenance in "
            "most species."
        ),
        "mechanism_ja": (
            "等張性の平衡型補充輸液（Na 130・K 4・Ca 3・Cl 109 mEq/L、乳酸28 mEq/L、約273 mOsm/L）。"
            "乳酸は肝で代謝され重炭酸となり軽度のアルカリ化作用を示す。"
            "多くの種でショック蘇生・脱水補正・維持輸液の第一選択。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Shock: 10-20 mL/kg IV over 15-20 min, reassess and repeat to "
                    "effect (up to 80-90 mL/kg total). Dehydration: deficit (%) x BW "
                    "(kg) x 10 = mL, replace over 12-24 h + ongoing losses. "
                    "Maintenance: 40-60 mL/kg/day (AAHA/AAFP 2013)."
                ),
                "dosage_ja": (
                    "ショック: 10-20 mL/kg 静注 15-20分、再評価しながら反復（合計80-90 mL/kgまで）。"
                    "脱水補正: 脱水率(%)×体重(kg)×10 = mL を12-24時間で＋進行中喪失分。"
                    "維持: 40-60 mL/kg/日（AAHA/AAFP 2013）。"
                ),
                "notes": (
                    "Reassess perfusion (HR, pulses, lactate, BP) after each bolus — "
                    "titrate, don't run the full shock dose blind."
                ),
                "notes_ja": (
                    "ボーラス毎に灌流指標（心拍・脈圧・乳酸・血圧）を再評価 — ショック総量を盲目的に入れず滴定する。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": (
                    "Shock: 5-10 mL/kg IV over 15-20 min, reassess (total 40-60 "
                    "mL/kg). Maintenance: 40-60 mL/kg/day (~2-3 mL/kg/h)."
                ),
                "dosage_ja": (
                    "ショック: 5-10 mL/kg 静注 15-20分で再評価（合計40-60 mL/kg）。"
                    "維持: 40-60 mL/kg/日（約2-3 mL/kg/時）。"
                ),
                "notes": (
                    "Cats are volume-overload prone (occult cardiomyopathy) — use "
                    "smaller boluses and auscultate/monitor respiratory rate."
                ),
                "notes_ja": (
                    "猫は容量過負荷を起こしやすい（潜在性心筋症）— 少量ボーラスで、聴診と呼吸数モニタリングを併行。"
                ),
            },
            "horse": {
                "safe": True,
                "dosage": (
                    "Shock/colic resuscitation: 10-20 mL/kg rapid IV bolus, reassess "
                    "and repeat. Maintenance: 50-60 mL/kg/day."
                ),
                "dosage_ja": ("ショック・疝痛蘇生: 10-20 mL/kg 急速静注ボーラス、再評価し反復。維持: 50-60 mL/kg/日。"),
                "notes": "Large-bore catheter(s); monitor PCV/TS during large-volume replacement.",
                "notes_ja": "太径カテーテル（必要なら複数）。大量輸液中はPCV/TSをモニタリング。",
            },
            "rabbit": {
                "safe": True,
                "dosage": (
                    "Maintenance 80-100 mL/kg/day; mild-moderate dehydration: warmed "
                    "SC in divided doses. Shock: 10-15 mL/kg IV/IO bolus, reassess."
                ),
                "dosage_ja": (
                    "維持 80-100 mL/kg/日。軽-中等度脱水は加温してSC分割投与。"
                    "ショック: 10-15 mL/kg IV/IO ボーラスで再評価。"
                ),
                "notes": "Warm fluids (small mammals chill quickly).",
                "notes_ja": "輸液は加温する（小型哺乳類は容易に低体温になる）。",
            },
            "bird": {
                "safe": True,
                "dosage": (
                    "Bolus 10-25 mL/kg IV/IO slowly; SC 50-100 mL/kg/day divided for "
                    "maintenance/mild dehydration (warmed)."
                ),
                "dosage_ja": ("ボーラス 10-25 mL/kg IV/IO 緩徐に。維持・軽度脱水は加温してSC 50-100 mL/kg/日 分割。"),
                "notes": "Medial metatarsal/jugular IV or IO catheter for critical patients.",
                "notes_ja": "重症例は内側中足静脈・頸静脈IVまたはIOカテーテル。",
            },
            "reptile": {
                "safe": True,
                "dosage": (
                    "15-25 mL/kg/day SC/intracoelomic/soaking at POTZ; replace "
                    "deficits over 48-72 h (slower metabolism)."
                ),
                "dosage_ja": (
                    "15-25 mL/kg/日 SC・体腔内・温浴（POTZで）。欠乏補正は48-72時間かけて（代謝が遅いため緩徐に）。"
                ),
                "notes": "Warm to POTZ before administration.",
                "notes_ja": "投与前にPOTZまで加温。",
            },
        },
        "side_effects": (
            "Volume overload (pulmonary edema — especially cats and small exotics), "
            "dilutional effects with large volumes, interstitial edema in "
            "hypoproteinemia."
        ),
        "side_effects_ja": (
            "容量過負荷（肺水腫 — 特に猫・小型エキゾチック）、大量投与時の希釈性変化、低蛋白血症での間質浮腫。"
        ),
        "contraindications": (
            "Do not run through the same line as blood products (calcium chelates "
            "citrate anticoagulant and triggers clotting). Caution in congestive "
            "heart failure, anuric renal failure, severe liver failure (impaired "
            "lactate metabolism) and head trauma (slightly hypotonic)."
        ),
        "contraindications_ja": (
            "血液製剤と同一ラインで投与しない（カルシウムがクエン酸抗凝固剤と反応し凝固）。"
            "うっ血性心不全・無尿性腎不全・重度肝不全（乳酸代謝低下）・頭部外傷（軽度低張）では慎重に。"
        ),
        "drug_interactions": [
            {
                "drug": "Blood products (same line)",
                "effect": "Calcium content clots citrated blood — use a separate line or 0.9% saline",
                "effect_ja": "カルシウム含有のためクエン酸血液が凝固 — 別ライン or 生理食塩液を使用",
            },
            {
                "drug": "ceftriaxone",
                "effect": "Calcium-ceftriaxone precipitation — do not co-administer in the same line",
                "effect_ja": "カルシウム-セフトリアキソン沈殿 — 同一ラインで併用しない",
            },
        ],
    },
    {
        "id": "normosol_r",
        "name": "Normosol-R / Plasma-Lyte A",
        "name_ja": "ノルモソルR／プラズマライトA",
        "category": "miscellaneous",
        "mechanism": (
            "Isotonic balanced crystalloid buffered with acetate/gluconate (Na 140, "
            "K 5, Mg 3, Cl 98 mEq/L; pH 7.4; ~294 mOsm/L). Calcium-free, so it is "
            "compatible with blood products; acetate is metabolised in muscle "
            "(not liver), making it the preferred balanced fluid in hepatic failure."
        ),
        "mechanism_ja": (
            "酢酸/グルコン酸緩衝の等張平衡型輸液（Na 140・K 5・Mg 3・Cl 98 mEq/L、pH 7.4、約294 mOsm/L）。"
            "カルシウム非含有で血液製剤と同一ライン投与が可能。酢酸は筋で代謝されるため（肝でなく）、"
            "肝不全時に選択される平衡型輸液。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Same rates as LRS: shock 10-20 mL/kg IV over 15-20 min to effect "
                    "(up to 80-90 mL/kg); maintenance 40-60 mL/kg/day."
                ),
                "dosage_ja": (
                    "乳酸リンゲルと同じ流量: ショック 10-20 mL/kg 静注 15-20分で滴定"
                    "（80-90 mL/kgまで）。維持 40-60 mL/kg/日。"
                ),
                "notes": ("Very rapid large boluses can cause transient vasodilation (acetate) — titrate in shock."),
                "notes_ja": "超急速大量ボーラスは一過性血管拡張（酢酸）を起こしうる — ショックでは滴定。",
            },
            "cat": {
                "safe": True,
                "dosage": "Shock 5-10 mL/kg IV boluses to effect (total 40-60 mL/kg); maintenance 40-60 mL/kg/day.",
                "dosage_ja": "ショック 5-10 mL/kg ボーラスを滴定（合計40-60 mL/kg）。維持 40-60 mL/kg/日。",
                "notes": "Volume-overload caution as with any crystalloid in cats.",
                "notes_ja": "他の晶質液同様、猫では容量過負荷に注意。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Maintenance 80-100 mL/kg/day warmed SC divided; shock 10-15 mL/kg IV/IO.",
                "dosage_ja": "維持 80-100 mL/kg/日 加温SC分割。ショック 10-15 mL/kg IV/IO。",
                "notes": "Commonly used warmed SC in small exotic mammals.",
                "notes_ja": "小型エキゾチック哺乳類では加温SC投与が一般的。",
            },
            "hamster": {
                "safe": True,
                "dosage": "80-100 mL/kg/day warmed SC divided (dehydration support).",
                "dosage_ja": "80-100 mL/kg/日 加温SC分割（脱水の支持療法）。",
                "notes": "Small volumes per site; warm to body temperature.",
                "notes_ja": "1部位あたり少量ずつ。体温程度に加温。",
            },
            "bird": {
                "safe": True,
                "dosage": "Bolus 10-25 mL/kg IV/IO; 50-100 mL/kg/day SC divided (warmed).",
                "dosage_ja": "ボーラス 10-25 mL/kg IV/IO。加温してSC 50-100 mL/kg/日 分割。",
                "notes": "Calcium-free — preferred when co-administering with transfusions.",
                "notes_ja": "カルシウム非含有 — 輸血併用時に選択される。",
            },
        },
        "side_effects": (
            "Volume overload; transient vasodilation/hypotension with very rapid "
            "infusion (acetate); magnesium accumulation possible in severe renal "
            "failure."
        ),
        "side_effects_ja": (
            "容量過負荷。超急速投与での一過性血管拡張・低血圧（酢酸）。重度腎不全ではマグネシウム蓄積の可能性。"
        ),
        "contraindications": (
            "Caution in congestive heart failure and oliguric/anuric renal failure "
            "(K and Mg content). No calcium — safe with blood products."
        ),
        "contraindications_ja": (
            "うっ血性心不全、乏尿・無尿性腎不全では慎重に（K・Mg含有）。カルシウム非含有のため血液製剤とは併用可。"
        ),
        "drug_interactions": [
            {
                "drug": "No significant drug interactions",
                "effect": "Compatible with blood products (calcium-free), unlike LRS",
                "effect_ja": "カルシウム非含有のため血液製剤と適合（乳酸リンゲルと異なる）",
            },
        ],
    },
    {
        "id": "l_theanine",
        "name": "L-Theanine (Anxitane)",
        "name_ja": "L-テアニン（アンキシタン）",
        "category": "behavioral",
        "mechanism": (
            "Green-tea amino acid that crosses the blood-brain barrier, increases "
            "brain GABA, serotonin and dopamine and weakly antagonises glutamate "
            "binding. Non-sedating anxiolytic nutraceutical used as an adjunct to "
            "behaviour modification for noise/storm anxiety and mild situational "
            "anxiety."
        ),
        "mechanism_ja": (
            "緑茶由来アミノ酸。血液脳関門を通過し脳内GABA・セロトニン・ドパミンを増加させ、"
            "グルタミン酸結合を弱く拮抗する。鎮静を伴わない抗不安ニュートラシューティカルで、"
            "騒音・雷不安や軽度の状況性不安に対し行動修正の補助として使用。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "~2.5-5 mg/kg PO q12h. Anxitane tablets: 50 mg q12h (< 10 kg), "
                    "100 mg q12h (>= 10 kg). Give >= 30-60 min before a predictable "
                    "stressor (Berteselli 2007)."
                ),
                "dosage_ja": (
                    "約2.5-5 mg/kg 経口 1日2回。アンキシタン錠: 50 mg q12h（10 kg未満）、"
                    "100 mg q12h（10 kg以上）。予測可能なストレッサーの30-60分以上前に投与（Berteselli 2007）。"
                ),
                "notes": (
                    "Nutraceutical adjunct — combine with behaviour modification; not "
                    "a substitute for SSRIs/TCAs in severe anxiety disorders."
                ),
                "notes_ja": (
                    "ニュートラシューティカルの補助 — 行動修正と併用。重度不安症でのSSRI/三環系の代替にはならない。"
                ),
            },
            "cat": {
                "safe": True,
                "dosage": "25 mg/cat PO q12h (Dramard 2018).",
                "dosage_ja": "25 mg/頭 経口 1日2回（Dramard 2018）。",
                "notes": "Improved undesirable stress-related behaviours in an open-label trial.",
                "notes_ja": "オープンラベル試験でストレス関連問題行動の改善が報告されている。",
            },
        },
        "side_effects": "Very well tolerated; occasional mild GI upset.",
        "side_effects_ja": "忍容性は非常に良好。まれに軽度の消化器症状。",
        "contraindications": "None established. Not evaluated in pregnancy.",
        "contraindications_ja": "確立された禁忌なし。妊娠中の評価はされていない。",
        "drug_interactions": [
            {
                "drug": "No significant drug interactions",
                "effect": "May be combined with behavioural drugs (fluoxetine, trazodone) under supervision",
                "effect_ja": "獣医師管理下で行動治療薬（フルオキセチン・トラゾドン）と併用可",
            },
        ],
    },
    {
        "id": "alpha_casozepine",
        "name": "Alpha-Casozepine (Zylkene)",
        "name_ja": "αカソゼピン（ジルケーン）",
        "category": "behavioral",
        "mechanism": (
            "Tryptic hydrolysate decapeptide of bovine alpha-s1 casein with affinity "
            "for the GABA-A receptor benzodiazepine site, producing anxiolysis "
            "without sedation, ataxia or dependence. Used for situational and "
            "chronic mild anxiety in dogs and cats."
        ),
        "mechanism_ja": (
            "牛αs1カゼインのトリプシン加水分解デカペプチド。GABA-A受容体ベンゾジアゼピン部位に親和性を持ち、"
            "鎮静・失調・依存を伴わない抗不安作用を示す。犬猫の状況性・慢性の軽度不安に使用。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "15 mg/kg PO q24h (Beata 2007 — comparable efficacy to selegiline "
                    "for anxiety disorders). Start 1-2 days before a predictable "
                    "stressor; continue 1-2 months for chronic anxiety."
                ),
                "dosage_ja": (
                    "15 mg/kg 経口 1日1回（Beata 2007 — 不安障害でセレギリンと同等の有効性）。"
                    "予測可能なストレッサーの1-2日前から開始。慢性不安には1-2ヶ月継続。"
                ),
                "notes": "Nutraceutical adjunct to behaviour modification.",
                "notes_ja": "行動修正の補助となるニュートラシューティカル。",
            },
            "cat": {
                "safe": True,
                "dosage": "15 mg/kg PO q24h (capsule content may be mixed with food).",
                "dosage_ja": "15 mg/kg 経口 1日1回（カプセル内容物はフードに混ぜてよい）。",
                "notes": "Useful for vet-visit/boarding/moving stress; start several days ahead.",
                "notes_ja": "通院・ペットホテル・引越しストレスに有用。数日前から開始する。",
            },
        },
        "side_effects": "Very well tolerated; no sedation at recommended doses.",
        "side_effects_ja": "忍容性は非常に良好。推奨用量で鎮静なし。",
        "contraindications": "Milk-protein hypersensitivity.",
        "contraindications_ja": "乳蛋白過敏症。",
        "drug_interactions": [
            {
                "drug": "No significant drug interactions",
                "effect": "May be combined with behavioural drugs under supervision",
                "effect_ja": "獣医師管理下で行動治療薬と併用可",
            },
        ],
    },
    {
        "id": "povidone_iodine",
        "name": "Povidone-Iodine",
        "name_ja": "ポビドンヨード",
        "category": "antiseptics",
        "mechanism": (
            "Iodophor that slowly releases free iodine, oxidising microbial "
            "proteins, nucleotides and membranes. Broad-spectrum bactericidal, "
            "virucidal, fungicidal and protozoacidal. Working strength matters: "
            "concentrations above ~1% are cytotoxic to fibroblasts and delay wound "
            "healing — dilute for open wounds."
        ),
        "mechanism_ja": (
            "ヨードフォア。遊離ヨウ素を徐放し微生物の蛋白・核酸・膜を酸化する。"
            "広域の殺菌・殺ウイルス・殺真菌・殺原虫作用。使用濃度が重要: 約1%超は線維芽細胞に"
            "細胞毒性を示し創傷治癒を遅延させる — 開放創には希釈して使用。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Surgical prep: 7.5% scrub then 10% solution. Open-wound lavage: "
                    "dilute to 0.1-1% (1:10 to 1:100 of 10% stock) — 'weak tea' colour."
                ),
                "dosage_ja": (
                    "術野消毒: 7.5%スクラブ後に10%液。開放創洗浄: 0.1-1%に希釈"
                    "（10%原液の1:10〜1:100）— 「薄い紅茶色」を目安に。"
                ),
                "notes": "Inactivated by organic debris — lavage gross contamination first.",
                "notes_ja": "有機物で失活する — まず肉眼的汚染を洗浄除去してから使用。",
            },
            "cat": {
                "safe": True,
                "dosage": "Same dilutions as dogs (0.1-1% for wounds).",
                "dosage_ja": "犬と同じ希釈（創傷には0.1-1%）。",
                "notes": "Avoid extensive repeated application (iodine absorption, thyroid effects).",
                "notes_ja": "広範囲・反復の使用は避ける（ヨウ素吸収・甲状腺への影響）。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Dilute 0.1-1% for wound/pododermatitis care.",
                "dosage_ja": "創傷・足底皮膚炎ケアに0.1-1%希釈で。",
                "notes": "Do not let small mammals become hypothermic from wet dressings.",
                "notes_ja": "湿潤処置による小型哺乳類の低体温に注意。",
            },
            "reptile": {
                "safe": True,
                "dosage": (
                    "Shell rot/wounds: after debridement, apply dilute (1:10) solution "
                    "topically or as short soaks q12-24h, then keep dry-docked as "
                    "directed."
                ),
                "dosage_ja": (
                    "甲羅腐敗症・創傷: デブリードマン後に1:10希釈液を塗布または短時間浸漬 q12-24h、"
                    "その後は指示に従いドライドック管理。"
                ),
                "notes": "Combine with husbandry correction (water quality, basking, UV-B).",
                "notes_ja": "飼育環境の是正（水質・バスキング・UV-B）と必ず併行。",
            },
            "bird": {
                "safe": True,
                "dosage": "Dilute 0.5-1% for wound antisepsis; small areas only.",
                "dosage_ja": "創傷消毒に0.5-1%希釈。小範囲のみに使用。",
                "notes": "Avoid soaking large body areas (hypothermia, iodine absorption).",
                "notes_ja": "広範囲の湿潤は避ける（低体温・ヨウ素吸収）。",
            },
        },
        "side_effects": (
            "Cytotoxicity to healing tissue at > 1%, contact irritation, iodine "
            "absorption with large-area/repeated use (thyroid interference), "
            "staining."
        ),
        "side_effects_ja": (
            "1%超での治癒組織への細胞毒性、接触刺激、広範囲・反復使用でのヨウ素吸収（甲状腺機能への干渉）、着色。"
        ),
        "contraindications": (
            "Known iodine hypersensitivity; use with care in patients with thyroid "
            "disease and in neonates; not for use in the ear canal with a ruptured "
            "tympanum."
        ),
        "contraindications_ja": ("ヨウ素過敏症。甲状腺疾患患者・新生子では慎重に。鼓膜穿孔例の耳道内には使用しない。"),
        "drug_interactions": [
            {
                "drug": "Enzymatic debriding agents",
                "effect": "Iodine inactivates enzymatic debriders — do not combine",
                "effect_ja": "ヨウ素は酵素的デブリードマン剤を失活させる — 併用しない",
            },
            {
                "drug": "chlorhexidine",
                "effect": "No benefit combining antiseptics; choose one per site",
                "effect_ja": "消毒薬の併用に利点なし。部位ごとにどちらか一方を選択",
            },
        ],
    },
    {
        "id": "folic_acid",
        "name": "Folic Acid",
        "name_ja": "葉酸",
        "category": "vitamins_minerals",
        "mechanism": (
            "Vitamin B9. Reduced to tetrahydrofolate, the one-carbon donor required "
            "for purine/thymidylate synthesis and erythropoiesis. Supplemented when "
            "serum folate is low (proximal small-intestinal disease, chronic "
            "enteropathy) and during long antifolate therapy (sulfonamides)."
        ),
        "mechanism_ja": (
            "ビタミンB9。テトラヒドロ葉酸に還元され、プリン・チミジル酸合成と造血に必須の一炭素供与体となる。"
            "血清葉酸低値（近位小腸疾患・慢性腸症）や長期の抗葉酸薬（サルファ薬）治療中に補給する。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "0.5-1 mg/dog PO q24h for documented low serum folate (chronic "
                    "enteropathy); recheck folate after 4 weeks."
                ),
                "dosage_ja": (
                    "血清葉酸低値が確認された症例（慢性腸症）に 0.5-1 mg/頭 経口 1日1回。4週間後に葉酸を再測定。"
                ),
                "notes": "Treat the underlying enteropathy; folate is an adjunct.",
                "notes_ja": "基礎にある腸症の治療が主体。葉酸補給は補助。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.25-0.5 mg/cat PO q24h for low serum folate; recheck in 4 weeks.",
                "dosage_ja": "血清葉酸低値に 0.25-0.5 mg/頭 経口 1日1回。4週間後に再測定。",
                "notes": "Often combined with cobalamin (B12) in chronic enteropathy work-ups.",
                "notes_ja": "慢性腸症ではコバラミン（B12）補給と併用されることが多い。",
            },
            "horse": {
                "safe": True,
                "dosage": (
                    "Monitor folate status during prolonged pyrimethamine/sulfonamide "
                    "(EPM) therapy. Do NOT give oral folic acid to PREGNANT mares on "
                    "pyrimethamine/sulfa — congenital defects reported in their foals "
                    "(Toribio 1998); avoid treating pregnant mares with the "
                    "combination where possible."
                ),
                "dosage_ja": (
                    "ピリメタミン/サルファ薬（EPM）長期治療中は葉酸状態をモニタリング。"
                    "妊娠馬でピリメタミン/サルファ治療中の経口葉酸投与は行わない — "
                    "子馬の先天奇形が報告されている（Toribio 1998）。妊娠馬への同併用療法自体を可能な限り避ける。"
                ),
                "notes": (
                    "Oral folic acid is poorly absorbed in horses and does not "
                    "reliably correct antifolate-induced deficiency; folinic acid is "
                    "the rescue form used in other species."
                ),
                "notes_ja": (
                    "馬では経口葉酸の吸収が乏しく、抗葉酸薬による欠乏を確実には補正できない。"
                    "他種でのレスキューにはフォリン酸（ホリナート）が用いられる。"
                ),
            },
        },
        "side_effects": "Essentially non-toxic at supplementation doses.",
        "side_effects_ja": "補給用量では実質的に無毒。",
        "contraindications": (
            "Pregnant mares receiving pyrimethamine/sulfonamides (paradoxical fetal "
            "harm — see horse notes). Folic acid does not reverse methotrexate "
            "toxicity (use folinic acid/leucovorin)."
        ),
        "contraindications_ja": (
            "ピリメタミン/サルファ薬治療中の妊娠馬（逆説的な胎子障害 — 馬の項参照）。"
            "メトトレキサート中毒の拮抗には無効（フォリン酸/ロイコボリンを使用）。"
        ),
        "drug_interactions": [
            {
                "drug": "pyrimethamine",
                "effect": "Antifolate depletes folate; see pregnant-mare warning before supplementing",
                "effect_ja": "抗葉酸薬により葉酸が枯渇。補給前に妊娠馬の警告を参照",
            },
            {
                "drug": "Potentiated sulfonamides",
                "effect": "Prolonged therapy can lower folate — monitor CBC/folate",
                "effect_ja": "長期投与で葉酸低下の可能性 — CBC・葉酸をモニタリング",
            },
            {
                "drug": "methotrexate",
                "effect": "Folic acid does not rescue toxicity; folinic acid is required",
                "effect_ja": "葉酸では毒性を拮抗できない。フォリン酸が必要",
            },
        ],
    },
    {
        "id": "dmso",
        "name": "DMSO (Dimethyl Sulfoxide)",
        "name_ja": "DMSO（ジメチルスルホキシド）",
        "category": "miscellaneous",
        "mechanism": (
            "Hydroxyl-radical scavenger with anti-inflammatory, anti-edema and "
            "membrane-penetrant carrier properties. Used IV (diluted) as an adjunct "
            "for equine CNS inflammation/endotoxemia (evidence mixed) and topically "
            "for musculoskeletal inflammation and doxorubicin extravasation."
        ),
        "mechanism_ja": (
            "ヒドロキシルラジカルスカベンジャー。抗炎症・抗浮腫作用と、膜透過キャリア特性を持つ。"
            "馬の中枢神経炎症・エンドトキセミアの補助として希釈静注（エビデンスは混在）、"
            "筋骨格系炎症やドキソルビシン血管外漏出に局所塗布で使用。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": (
                    "0.5-1 g/kg IV as a <= 10% solution in isotonic fluids q12-24h, "
                    "up to 3 days (cerebral/spinal edema, adjunct). Topical: 90% gel "
                    "to affected area q8-12h with gloves."
                ),
                "dosage_ja": (
                    "0.5-1 g/kg を等張輸液で10%以下に希釈し静注 q12-24h、最長3日"
                    "（脳・脊髄浮腫の補助）。局所: 90%ゲルを患部に q8-12h、手袋着用で塗布。"
                ),
                "notes": (
                    "Concentrations > 10% IV cause intravascular hemolysis and "
                    "hemoglobinuria. Garlic-like breath odour is expected."
                ),
                "notes_ja": ("10%超の静注は血管内溶血・ヘモグロビン尿を起こす。ニンニク様の呼気臭は正常反応。"),
            },
            "dog": {
                "safe": True,
                "dosage": (
                    "Topical 90% solution/gel sparingly to localised inflammation or "
                    "doxorubicin extravasation sites q8h (with dexrazoxane IV for "
                    "extravasation)."
                ),
                "dosage_ja": (
                    "局所炎症やドキソルビシン血管外漏出部位に90%液/ゲルを少量 q8h"
                    "（漏出時はデクスラゾキサン静注と併用）。"
                ),
                "notes": "Carrier effect: whatever is on the skin goes through — apply to clean, dry skin.",
                "notes_ja": "キャリア作用: 皮膚上の物質を透過させる — 清潔で乾いた皮膚に塗布。",
            },
            "cat": {
                "safe": True,
                "dosage": (
                    "Limited topical use only (small areas). Intravesical 10% DMSO "
                    "has been described for refractory feline idiopathic cystitis by "
                    "specialists."
                ),
                "dosage_ja": (
                    "局所の限定的使用のみ（小範囲）。難治性特発性膀胱炎への10%膀胱内注入が専門医により報告されている。"
                ),
                "notes": "Cats are sensitive to many solvents — use sparingly and monitor.",
                "notes_ja": "猫は溶媒感受性が高い — 少量使用とモニタリングを徹底。",
            },
        },
        "side_effects": (
            "Hemolysis/hemoglobinuria (IV > 10%), garlic breath odour, local skin "
            "irritation/dryness, transient tremor with rapid IV."
        ),
        "side_effects_ja": (
            "溶血・ヘモグロビン尿（10%超の静注）、ニンニク様呼気臭、局所皮膚刺激・乾燥、急速静注での一過性振戦。"
        ),
        "contraindications": (
            "Dehydration/shock before volume replacement; pregnancy (teratogenic "
            "potential); handlers must wear gloves — pregnant staff should avoid "
            "handling. Never apply over toxic residues (carrier effect)."
        ),
        "contraindications_ja": (
            "容量補正前の脱水・ショック。妊娠（催奇形性の可能性）。取扱者は手袋必須 — "
            "妊娠中のスタッフは取り扱いを避ける。毒性残留物の上には絶対に塗布しない（キャリア作用）。"
        ),
        "drug_interactions": [
            {
                "drug": "Topical drugs/chemicals on the same skin",
                "effect": "DMSO carries them systemically — apply only to clean skin",
                "effect_ja": "DMSOが全身循環へ透過させる — 清潔な皮膚のみに塗布",
            },
            {
                "drug": "Organophosphates / cholinesterase inhibitors",
                "effect": "Enhanced percutaneous absorption and toxicity",
                "effect_ja": "経皮吸収・毒性を増強",
            },
        ],
    },
    {
        "id": "mineral_oil",
        "name": "Mineral Oil (Liquid Paraffin)",
        "name_ja": "ミネラルオイル（流動パラフィン）",
        "category": "gi_drugs",
        "mechanism": (
            "Non-absorbable intestinal lubricant laxative. Coats ingesta and mucosa "
            "to soften and ease passage of impacted material. Mainstay for equine "
            "large-colon impaction via nasogastric tube; largely superseded by "
            "lactulose/PEG in small animals."
        ),
        "mechanism_ja": (
            "非吸収性の腸管潤滑性下剤。内容物と粘膜をコーティングし、宿便の軟化・通過を促す。"
            "馬の大結腸便秘に経鼻胃チューブで投与するのが主用途。小動物ではラクツロース/PEGが主流。"
        ),
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": (
                    "2-4 L/500 kg (approx. 5-10 mL/kg) via nasogastric tube with "
                    "water, once; may repeat q12-24h for large-colon impaction. "
                    "CONFIRM tube placement before administration."
                ),
                "dosage_ja": (
                    "2-4 L/500 kg（約5-10 mL/kg）を水とともに経鼻胃チューブで単回投与。"
                    "大結腸便秘では q12-24h で反復可。投与前にチューブの胃内留置を必ず確認。"
                ),
                "notes": (
                    "Aspiration causes fatal lipoid pneumonia. Do not administer with "
                    "nasogastric reflux or suspected small-intestinal obstruction. "
                    "Oil at the anus in 12-24 h confirms transit."
                ),
                "notes_ja": (
                    "誤嚥は致死的な脂質性肺炎を起こす。胃逆流や小腸閉塞疑いでは投与しない。"
                    "12-24時間後の肛門からのオイル排出で通過を確認。"
                ),
            },
            "dog": {
                "safe": True,
                "dosage": (
                    "5-30 mL/dog PO mixed IN FOOD q12-24h short-term for constipation. "
                    "Never syringe directly (tasteless — high aspiration risk)."
                ),
                "dosage_ja": (
                    "5-30 mL/頭 をフードに混ぜて q12-24h 短期使用（便秘）。"
                    "直接シリンジで経口投与しない（無味で誤嚥リスクが高い）。"
                ),
                "notes": "Lactulose or PEG 3350 preferred for ongoing management.",
                "notes_ja": "継続管理にはラクツロースやPEG 3350が望ましい。",
            },
            "cat": {
                "safe": True,
                "dosage": "2-10 mL/cat PO mixed in food q12-24h short-term; never syringe directly.",
                "dosage_ja": "2-10 mL/頭 をフードに混ぜて q12-24h 短期使用。直接シリンジ投与は絶対にしない。",
                "notes": "Aspiration of tasteless oil is silent — food admixture only.",
                "notes_ja": "無味のオイルの誤嚥は気付かれにくい — 必ずフード混和で。",
            },
            "rabbit": {
                "safe": True,
                "dosage": (
                    "Historically 1-2 mL/kg PO for trichobezoar; current management "
                    "prioritises rehydration, fibre and prokinetics instead."
                ),
                "dosage_ja": ("毛球症に対し歴史的に1-2 mL/kg 経口。現在は輸液・繊維・消化管運動促進薬が優先される。"),
                "notes": "Does not address the underlying GI stasis — adjunct at most.",
                "notes_ja": "基礎にある消化管うっ滞を治療するものではない — あくまで補助。",
            },
        },
        "side_effects": (
            "Lipoid (aspiration) pneumonia if inhaled, interference with "
            "fat-soluble vitamin (A/D/E/K) absorption with chronic use, anal "
            "leakage/seepage."
        ),
        "side_effects_ja": ("誤嚥による脂質性肺炎、慢性使用での脂溶性ビタミン（A/D/E/K）吸収阻害、肛門からの漏出。"),
        "contraindications": (
            "Suspected GI obstruction or perforation, nasogastric reflux (horses), "
            "dysphagia/megaesophagus (aspiration risk). Do not use chronically."
        ),
        "contraindications_ja": (
            "消化管閉塞・穿孔の疑い、胃逆流（馬）、嚥下障害・巨大食道症（誤嚥リスク）。慢性使用は避ける。"
        ),
        "drug_interactions": [
            {
                "drug": "vitamin_k1",
                "effect": "Chronic mineral oil reduces fat-soluble vitamin (K) absorption",
                "effect_ja": "慢性使用で脂溶性ビタミン（K）の吸収を低下させる",
            },
            {
                "drug": "docusate",
                "effect": "Docusate enhances mineral-oil absorption — do not combine",
                "effect_ja": "ドキュセートがミネラルオイルの吸収を促進する — 併用しない",
            },
        ],
    },
    {
        "id": "lugols_iodine",
        "name": "Lugol's Iodine",
        "name_ja": "ルゴール液",
        "category": "vitamins_minerals",
        "mechanism": (
            "Aqueous iodine/potassium-iodide solution. Supplies the iodine required "
            "for thyroid hormone synthesis; reverses dietary iodine-deficiency "
            "goiter (thyroid hyperplasia), classically in seed-fed budgerigars in "
            "which the enlarged gland compresses the trachea/syrinx."
        ),
        "mechanism_ja": (
            "ヨウ素・ヨウ化カリウム水溶液。甲状腺ホルモン合成に必要なヨウ素を補給し、"
            "食餌性ヨウ素欠乏による甲状腺腫（過形成）を改善する。シード主体食のセキセイインコで"
            "腫大腺が気管・鳴管を圧迫する古典的疾患に用いる。"
        ),
        "species_info": {
            "bird": {
                "safe": True,
                "dosage": (
                    "Dilute stock: 2 mL Lugol's in 30 mL water. Add 1 drop of stock "
                    "per 250 mL drinking water daily until improved (usually days), "
                    "then 2-3x weekly maintenance (Carpenter 6th ed; budgerigar "
                    "goiter)."
                ),
                "dosage_ja": (
                    "希釈ストック: ルゴール原液2 mLを水30 mLで希釈。ストック1滴を飲水250 mLに"
                    "添加し毎日（通常数日で改善）、以後は週2-3回の維持投与"
                    "（Carpenter第6版。セキセイインコ甲状腺腫）。"
                ),
                "notes": (
                    "Convert to an iodine-adequate diet (pellets, iodine block) for "
                    "prevention. Severe dyspnea may need oxygen and parenteral iodine "
                    "first."
                ),
                "notes_ja": (
                    "予防にはヨウ素を含む食餌（ペレット・ヨードブロック）へ変更。"
                    "重度呼吸困難例はまず酸素と非経口ヨウ素製剤を考慮。"
                ),
            },
            "tortoise": {
                "safe": True,
                "dosage": (
                    "Dietary iodine correction for goiter from goitrogenic plants "
                    "(brassicas): reduce goitrogens; iodine supplementation per "
                    "exotic formulary guidance."
                ),
                "dosage_ja": (
                    "ゴイトロゲン植物（アブラナ科）過剰による甲状腺腫には食餌是正を優先。"
                    "ヨウ素補給はエキゾチックフォーミュラリーの指針に従う。"
                ),
                "notes": "Chronic brassica-heavy diets are the usual cause in chelonians.",
                "notes_ja": "カメ類ではアブラナ科偏重の食餌が主因。",
            },
        },
        "side_effects": (
            "Iodine excess can itself suppress thyroid function (Wolff-Chaikoff "
            "effect) — do not exceed recommended dilution or duration."
        ),
        "side_effects_ja": (
            "ヨウ素過剰はそれ自体が甲状腺機能を抑制しうる（Wolff-Chaikoff効果）— 推奨希釈・期間を超えない。"
        ),
        "contraindications": (
            "Hyperthyroidism; concurrent methimazole (opposing/complex thyroid effects) without specialist guidance."
        ),
        "contraindications_ja": ("甲状腺機能亢進症。専門的管理なしのメチマゾール併用（甲状腺への複雑な相互作用）。"),
        "drug_interactions": [
            {
                "drug": "methimazole",
                "effect": "Iodine loading alters antithyroid drug response",
                "effect_ja": "ヨウ素負荷は抗甲状腺薬への反応を変化させる",
            },
        ],
    },
    {
        "id": "fluorescein",
        "name": "Fluorescein Sodium (Ophthalmic Stain)",
        "name_ja": "フルオレセイン（眼科染色）",
        "category": "ophthalmic",
        "mechanism": (
            "Hydrophilic diagnostic dye. Does not stain intact lipophilic corneal "
            "epithelium but binds exposed hydrophilic stroma, outlining corneal "
            "ulcers under cobalt-blue light. Also used for the Jones test "
            "(nasolacrimal patency) and tear-film breakup time (TFBUT)."
        ),
        "mechanism_ja": (
            "親水性の診断用色素。脂溶性の正常角膜上皮には染着せず、露出した親水性実質に結合し、"
            "コバルトブルー光下で角膜潰瘍を描出する。ジョーンズ試験（鼻涙管開通性）や"
            "涙液層破壊時間（TFBUT）にも使用。"
        ),
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": (
                    "Moisten a sterile fluorescein strip with eyewash, touch the "
                    "bulbar conjunctiva (or instil a drop), irrigate excess, examine "
                    "with cobalt-blue light. Jones test: dye at the nares within "
                    "~5 min indicates a patent nasolacrimal duct (unreliable in "
                    "brachycephalics — dye may exit the nasopharynx)."
                ),
                "dosage_ja": (
                    "滅菌フルオレセイン試験紙を点眼液で湿らせ眼球結膜に接触（または1滴点眼）、"
                    "余剰を洗い流しコバルトブルー光で観察。ジョーンズ試験: 約5分以内の外鼻孔への色素到達で"
                    "鼻涙管開通（短頭種では鼻咽頭へ抜けるため信頼性低い）。"
                ),
                "notes": (
                    "A deep ulcer with a non-staining centre = descemetocele "
                    "(Descemet's membrane does not stain) — surgical emergency."
                ),
                "notes_ja": ("中心部が染まらない深い潰瘍＝デスメ膜瘤（デスメ膜は染色されない）— 外科的緊急疾患。"),
            },
            "cat": {
                "safe": True,
                "dosage": "Same technique as dogs; stain every red/painful eye before applying steroids.",
                "dosage_ja": "手技は犬と同じ。ステロイド点眼の前に、赤い眼・痛い眼は必ず染色検査。",
                "notes": "Dendritic (branching) ulcers are pathognomonic for FHV-1 keratitis.",
                "notes_ja": "樹枝状潰瘍はFHV-1角膜炎に特徴的。",
            },
            "horse": {
                "safe": True,
                "dosage": "Same technique; stain all painful eyes (ulcerative vs immune-mediated keratitis).",
                "dosage_ja": "手技は同じ。有痛眼は全例染色（潰瘍性か免疫介在性角膜炎かの鑑別）。",
                "notes": "Never apply topical steroids to a fluorescein-positive equine eye.",
                "notes_ja": "フルオレセイン陽性の馬の眼にはステロイド点眼を絶対に使用しない。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Same strip technique; useful for E. cuniculi-associated and traumatic ulcers.",
                "dosage_ja": "試験紙法は同じ。E. cuniculi関連や外傷性潰瘍の評価に有用。",
                "notes": "Also stains for dacryocystitis work-ups (patency).",
                "notes_ja": "涙嚢炎の検査（開通性評価）にも使用。",
            },
            "bird": {
                "safe": True,
                "dosage": "Diluted drop or moistened strip; small volumes in small eyes.",
                "dosage_ja": "希釈点眼または湿らせた試験紙。小さな眼にはごく少量で。",
                "notes": "Corneal ulcers are common after trauma/fights.",
                "notes_ja": "外傷・闘争後の角膜潰瘍は多い。",
            },
            "reptile": {
                "safe": True,
                "dosage": "Strip technique; note the spectacle in snakes/some geckos prevents corneal staining.",
                "dosage_ja": "試験紙法。ヘビ・一部ヤモリのスペクタクル（眼鏡板）があると角膜染色は不可。",
                "notes": "Evaluate subspectacular space separately in snakes.",
                "notes_ja": "ヘビではスペクタクル下腔を別途評価。",
            },
        },
        "side_effects": (
            "Transient yellow staining of periocular fur/feathers; rare "
            "hypersensitivity. Soft contact-lens staining in humans handling it."
        ),
        "side_effects_ja": ("眼周囲の被毛・羽毛の一過性黄染。まれに過敏反応。取扱者のソフトコンタクトレンズ着色。"),
        "contraindications": (
            "None clinically significant for topical diagnostic use. Do not confuse with IV angiography formulations."
        ),
        "contraindications_ja": ("局所診断用途で臨床的に重要な禁忌なし。静注造影用製剤と混同しない。"),
        "drug_interactions": [
            {
                "drug": "No significant drug interactions",
                "effect": "Topical diagnostic agent",
                "effect_ja": "局所診断薬のため臨床的相互作用なし",
            },
        ],
    },
]
