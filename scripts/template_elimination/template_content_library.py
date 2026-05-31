"""Clinical content library to replace generic template treatment_ja / treatment.

Each entry is keyed by a normalized disease-name pattern (Japanese substring match,
e.g. ``"クリプトスポリジウム"``) and returns a function that takes ``species``
and produces species-tailored, evidence-based clinical content for:

- treatment / treatment_ja
- causes_ja (optional)
- prognosis_ja (optional)

The goal is to **eliminate** generic copy-paste template text from the disease
database while preserving species-specific clinical accuracy. References are
embedded inline; expanded citation lists live in ``_references.html``.

Each generator returns ``{"treatment_ja": str, "treatment": str, ...}``.
A return of ``None`` means "no curated content; use fallback generator".
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Optional

# Species class buckets for tailoring content
AVIAN = frozenset({"bird", "parakeet", "parrot"})
SMALL_MAMMAL = frozenset(
    {
        "rabbit",
        "guinea_pig",
        "hamster",
        "chinchilla",
        "degu",
        "ferret",
        "hedgehog",
        "sugar_glider",
    }
)
REPTILE = frozenset({"reptile", "tortoise", "snake", "lizard"})
DOG_CAT = frozenset({"dog", "cat"})
LARGE_ANIMAL = frozenset({"horse"})


def _avian_supportive(species: str) -> str:
    """Standard avian supportive care text — disease-agnostic baseline."""
    return (
        "支持療法（鳥類）: 保温28-30℃（重症は30-32℃）、皮下/骨内輸液 50-100 mL/kg/日 "
        "（温乳酸リンゲルまたはノルモソルR）、強制給餌（Emeraid Omnivore/Carnivoreなど "
        "20-30 mL/kg q4-6h）、酸素分圧40%以下を維持しつつ呼吸補助。"
    )


def _small_mammal_supportive(species: str) -> str:
    """Small-mammal supportive care — emphasizes pro-motility and analgesia."""
    species_specific = ""
    if species == "rabbit":
        species_specific = " ペニシリン系・セファロスポリン系の経口投与は腸内細菌叢を破壊し致死的になるため禁忌。"
    elif species == "guinea_pig":
        species_specific = " 経口ペニシリン・アンピシリン・セファロスポリンは禁忌（Clostridium difficile腸炎を誘発）。"
    elif species == "chinchilla":
        species_specific = " フィプロニル禁忌（致死性）。経口β-ラクタムは禁忌。"
    return (
        "支持療法（小型哺乳類）: 等張輸液 80-100 mL/kg/日 SC/IV、保温（26-28℃）、"
        "シリンジ給餌（Critical Care/Recovery 50-90 mL/kg/日を3-4回分割）、"
        "メロキシカム 0.5-1.0 mg/kg PO q12-24h で疼痛・炎症管理。" + species_specific
    )


def _reptile_supportive(species: str) -> str:
    """Reptile supportive care — POTZ critical for immune recovery."""
    return (
        "支持療法（爬虫類）: 種別POTZ（preferred optimum temperature zone）維持が免疫機能回復の前提条件。"
        "輸液 25-30 mL/kg/日 SC/ICe（ノルモソルR、温熱）、強制給餌（Carnivore Care 等）、"
        "メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h（NSAID持続投与時は腎機能をモニタ）。"
    )


def _dogcat_supportive(species: str) -> str:
    base = "支持療法: 輸液（晶質液 60-80 mL/kg/日 IV、ショック時 90 mL/kg初期ボーラス）、酸素化、栄養管理、疼痛管理。"
    if species == "cat":
        base += "ブプレノルフィン 0.02-0.03 mg/kg IM/OTM q6-8h で疼痛管理（オピオイド過剰反応に注意）。"
    else:
        base += "メサドン 0.1-0.5 mg/kg IM/IV q4-6h またはブプレノルフィン 0.01-0.02 mg/kg IM q6-8h。"
    return base


def _horse_supportive(species: str) -> str:
    return (
        "支持療法（馬）: 等張電解質輸液（晶質液 2-4 L/h IV、循環不全時はボーラス 20-40 mL/kg/h）、"
        "フルニキシン・メグルミン 1.1 mg/kg IV q12h（疝痛・内毒素症）、潰瘍予防にオメプラゾール 4 mg/kg PO q24h。"
    )


def _supportive_block(species: str) -> str:
    if species in AVIAN:
        return _avian_supportive(species)
    if species in SMALL_MAMMAL:
        return _small_mammal_supportive(species)
    if species in REPTILE or species == "amphibian":
        return _reptile_supportive(species)
    if species in DOG_CAT:
        return _dogcat_supportive(species)
    if species in LARGE_ANIMAL:
        return _horse_supportive(species)
    return "支持療法: 種に適切な輸液・栄養管理・疼痛緩和を行う。"


# ----------------------------------------------------------------------------
# Disease-specific generators
# ----------------------------------------------------------------------------


def gen_diabetes(species: str, name_ja: str) -> dict:
    """Diabetes mellitus — species-specific. Common in cats/dogs/ferrets, rare in birds."""
    if species == "cat":
        return {
            "treatment_ja": (
                "猫糖尿病の治療: ① 食事療法を最優先：高蛋白・低炭水化物処方食"
                "（PurinaProPlan DM、Royal Canin Diabetic、Hill's m/d 等。乾質量カーボ <12%）。"
                "② インスリン療法：プロジンク（PZI）0.25-0.5 IU/kg SC q12hまたはグラルギン 0.25-0.5 IU/kg SC q12h "
                "を第一選択。低用量から開始し7日毎に再評価。③ 血糖曲線（在宅Freestyle Libre連続血糖測定を推奨）で12時間最低血糖120-180 mg/dL目標。"
                "④ 寛解率20-40%（早期食事介入＋グラルギン/PZIで最大化）。"
                "⑤ ベルガリフロジン（経口SGLT2阻害薬、AAHA 2023承認）は新規ケトーシスがない症例で代替選択肢。"
                "ストレス高血糖との鑑別にフルクトサミン（>400 µmol/L）またはHbA1c使用。"
                "DKA合併時は規ュラーインスリンCRI 0.05-0.1 IU/kg/h IV＋K補正＋輸液で集中治療。"
                "AAFP/ISFM 2022 ガイドライン参照。"
            ),
            "treatment": (
                "Feline diabetes mellitus: ① Diet first — low-carb/high-protein therapeutic diet "
                "(Purina ProPlan DM, Royal Canin Diabetic, Hill's m/d; <12% DM carbohydrate). "
                "② Insulin: PZI 0.25-0.5 IU/kg SC q12h or glargine 0.25-0.5 IU/kg SC q12h. "
                "Start low, recheck q7d. ③ At-home Freestyle Libre CGM strongly preferred to "
                "in-clinic blood glucose curves; target nadir 120-180 mg/dL. ④ Remission "
                "achievable in 20-40% with early dietary + glargine/PZI. ⑤ Bexagliflozin "
                "(oral SGLT2-i, AAHA 2023) is alternative for non-DKA cases. Differentiate "
                "stress hyperglycemia using fructosamine (>400 µmol/L). For DKA: regular "
                "insulin CRI 0.05-0.1 IU/kg/h IV + K supplementation + fluid resuscitation. "
                "Reference: AAFP/ISFM 2022 Diabetes Guidelines; Behrend et al. JAVMA 2018."
            ),
            "prognosis_ja": (
                "新規発症で早期適正治療を行えば寛解率20-40%。寛解しない場合でも適切な血糖管理で "
                "中央生存期間3年以上が期待できる。DKA合併、慢性経過、合併症（膵炎、慢性腎臓病、末端肥大症）の存在で予後悪化。"
            ),
        }
    if species == "dog":
        return {
            "treatment_ja": (
                "犬糖尿病の治療: ① ベテリナリーインスリンN（プロジンク等中間型）0.25-0.5 IU/kg SC q12h を第一選択。"
                "② 食事療法：低脂肪・高繊維処方食（Hill's w/d、Royal Canin Diabetic）。"
                "③ 雌は不妊化必須（プロゲステロン拮抗GH分泌が血糖管理を不能化）。"
                "④ 血糖曲線（CGMまたは2時間毎の点滴採血）で最低血糖80-150 mg/dLを目標、"
                "用量調整は1週間毎。⑤ DKA時は規ュラーインスリンCRI 0.05-0.1 IU/kg/h IV+ K補正。"
                "⑥ 白内障（4年以内60-70%で発症）：定期眼科検査と早期手術（IRIS/ACVIM 2018）。"
                "AAHA 2018 Diabetes Management Guidelines準拠。"
            ),
            "treatment": (
                "Canine diabetes mellitus: ① Lente/PZI insulin 0.25-0.5 IU/kg SC q12h. "
                "② Diet: low-fat/high-fiber prescription (Hill's w/d, RC Diabetic). "
                "③ Spay intact females (diestrus progesterone-driven GH antagonizes insulin). "
                "④ Curve target nadir 80-150 mg/dL; CGM preferred. ⑤ DKA: regular insulin CRI "
                "0.05-0.1 IU/kg/h IV + K supplementation. ⑥ 60-70% develop cataracts within 4 years — "
                "schedule baseline ophthalmology referral. Reference: AAHA 2018 Diabetes Management."
            ),
        }
    if species == "ferret":
        return {
            "treatment_ja": (
                "フェレット糖尿病はインスリノーマ術後の医原性が多く、原発性は稀。"
                "プロジンク 0.1-0.5 IU/フェレット SC q12h から開始し血糖60-200 mg/dL目標。"
                "膵切除後の一過性糖尿病は数週-数ヶ月で改善することが多い。"
                "高蛋白・低炭水化物・高脂肪食（Wysong Epigen、Carnivore Caine 等）。" + _supportive_block(species)
            ),
            "treatment": (
                "Ferret DM is most often iatrogenic following insulinoma surgery; primary DM is rare. "
                "PZI insulin 0.1-0.5 IU/ferret SC q12h titrated to BG 60-200 mg/dL. "
                "Post-pancreatectomy DM is often transient. High-protein, low-carb diet (Wysong Epigen)."
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                "鳥類糖尿病はオウム目（特にコザクラインコ、ボウシインコ）で稀に報告。"
                "病態はインスリン抵抗性主体でグルカゴン過剰の可能性。"
                "レギュラーインスリン 0.1-0.2 IU/羽 SC q12-24hから開始、血糖200-400 mg/dL目標（鳥の正常値200-400）。"
                "高血糖食回避（果物・穀物減量）、ペレット主体食。多飲多尿モニタ。"
                "予後は管理困難で要注意。" + _avian_supportive(species)
            ),
            "treatment": (
                "Avian DM is rare and reported mainly in Psittaciformes (cockatiels, Amazon parrots). "
                "Likely insulin-resistance + glucagon excess. Regular insulin 0.1-0.2 IU/bird SC q12-24h, "
                "titrate to BG 200-400 mg/dL (normal avian BG 200-400). Avoid high-sugar items; "
                "convert to pelleted diet. Guarded prognosis."
            ),
        }
    if species == "horse":
        return {
            "treatment_ja": (
                "馬の糖尿病はPPID（下垂体中葉機能障害）またはEMS（馬メタボリック症候群）に二次的なものが大半。"
                "原疾患治療：PPID→ペルゴリド 2 µg/kg PO q24h（プラスニル）から開始、ACTH測定で用量調整。"
                "EMS→食事療法（NSC <10%乾草、放牧制限）、レボチロキシン 0.1 mg/kg PO q24h（短期）、"
                "メトホルミン 15-30 mg/kg PO q8-12h（インスリン感受性改善）。蹄葉炎の早期発見が予後を左右する。"
                "ACVIM 2019 Consensus Statement on PPID and EMS。"
            ),
            "treatment": (
                "Equine DM is usually secondary to PPID or EMS. PPID: pergolide 2 µg/kg PO q24h, "
                "titrate by ACTH. EMS: low NSC forage (<10%), restricted pasture, levothyroxine "
                "0.1 mg/kg PO q24h (short term), metformin 15-30 mg/kg PO q8-12h. "
                "Laminitis surveillance critical. ACVIM 2019 Consensus."
            ),
        }
    # small mammals (rabbit, guinea pig, hamster, chinchilla, etc.)
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{name_ja or '糖尿病'}は{species}では非常に稀。報告例ではインスリン依存性で、"
                "プロジンク 0.5-1 IU/動物 SC q12h から開始、家庭での血糖モニタ（耳介穿刺、CGM試験的）と組み合わせる。"
                "低糖質・高繊維食。インスリン抵抗性をきたす副腎疾患・甲状腺疾患・肥満を除外。"
                + _small_mammal_supportive(species)
            ),
            "treatment": (
                f"DM is very rare in {species}. Reported cases were insulin-dependent: "
                "PZI 0.5-1 IU/animal SC q12h, home BG monitoring. Rule out adrenal/thyroid disease "
                "and obesity. Low-carb / high-fiber diet."
            ),
        }
    # reptiles
    if species in REPTILE:
        return {
            "treatment_ja": (
                "爬虫類の糖尿病は非常に稀。インスリン依存性の報告は陸亀（ヒョウモンガメ）、グリーンイグアナで散見される。"
                "プロタミン亜鉛インスリン 1-5 IU/kg IM q24-72h から開始。POTZ維持（種別）、低糖食。"
                "膵島腺腫の鑑別が必要。長期管理データは限定的で予後要注意。" + _reptile_supportive(species)
            ),
            "treatment": (
                "DM in reptiles is extremely rare; case reports in green iguanas and leopard tortoises. "
                "PZI 1-5 IU/kg IM q24-72h. Maintain species-specific POTZ. Differential: islet adenoma. "
                "Long-term management data limited; prognosis guarded."
            ),
        }
    return None


def gen_hyperthyroidism(species: str, name_ja: str) -> dict:
    """Hyperthyroidism — extremely common in cats, rare in dogs/exotics."""
    if species == "cat":
        return {
            "treatment_ja": (
                "猫甲状腺機能亢進症（最も一般的な高齢猫内分泌疾患、10歳以上で約10%）の治療: "
                "① **I-131放射性ヨウ素治療**（gold standard、95%治癒、副作用最少、ACVIM推奨）— 可能なら第一選択。"
                "② メチマゾール 1.25-2.5 mg PO q12h（経皮ゲル製剤も可）— 用量はT4で4週毎調整。"
                "③ ヒルズy/d低ヨウ素食（カーボイメージング不能のためI-131との比較で代替）。"
                "④ 甲状腺摘出（経験ある外科医、副甲状腺温存）。"
                "腎機能のマスキング効果を考慮し、治療前/後にSDMAとUSGをモニタ（IRIS分類）。"
                "心筋症併発時はアテノロール 6.25-12.5 mg PO q12-24h（HR<200目標）。"
                "ACVIM/AAFP/ISFM 2016 Guidelines for Hyperthyroidism準拠。"
            ),
            "treatment": (
                "Feline hyperthyroidism (most common feline endocrinopathy, ~10% of cats >10y): "
                "① I-131 radioiodine — gold standard (95% cure, minimal side effects); first choice when "
                "available. ② Methimazole 1.25-2.5 mg PO q12h (transdermal gel available); titrate by T4 "
                "q4w. ③ Hill's y/d limited-iodine diet. ④ Thyroidectomy with parathyroid preservation. "
                "Reassess renal function (SDMA, USG) pre/post treatment to unmask occult CKD. "
                "Comorbid HCM: atenolol 6.25-12.5 mg PO q12-24h (HR <200). "
                "Reference: ACVIM/AAFP/ISFM 2016 Guidelines."
            ),
            "prognosis_ja": (
                "I-131で95%が単回治癒。メチマゾール内服で5年生存率約50%（高齢開始のため）。"
                "未治療は心筋症・腎不全・血栓塞栓症で1年以内に多くが死亡。早期診断ほど予後良好。"
            ),
        }
    if species == "dog":
        return {
            "treatment_ja": (
                "犬甲状腺機能亢進症は稀で、ほぼ全例が甲状腺癌（多くは機能性、悪性）に伴う。"
                "外科切除＋放射線治療（cobalt-60または直線加速器）が第一選択。"
                "I-131も大型犬で使用可能（ヒトより高用量必要）。"
                "化学療法（メルファラン、ヒドロキシウレア）はサルベージ。"
                "未切除症例ではメチマゾールはほぼ無効（甲状腺癌のため）。"
                "局所浸潤、転移率35-40%。早期切除で1年生存率70-90%。"
            ),
            "treatment": (
                "Canine hyperthyroidism is rare and almost always due to functional thyroid carcinoma. "
                "Surgery + radiation (Co-60 or linear accelerator) first-line. I-131 possible (higher "
                "doses than humans). Chemotherapy (melphalan, hydroxyurea) as salvage. Methimazole "
                "rarely effective. Local invasion and 35-40% metastatic rate; early surgical control "
                "yields 70-90% 1-year survival."
            ),
        }
    if species in SMALL_MAMMAL:
        details = ""
        if species == "guinea_pig":
            details = (
                "モルモットの甲状腺機能亢進症は高齢で増加傾向（剖検率最大25%）。"
                "甲状腺腫瘤の触診、T4測定（正常域0.9-4.7 µg/dL、高い症例で6-10）、超音波で診断。"
                "メチマゾール 1-2 mg/kg PO q12h を第一選択（個体差大、T4で調整）。"
                "甲状腺摘出も選択肢だが副甲状腺温存技術が必要。"
                "I-131はモルモットへの応用報告あり（Mayer et al. 2010）。"
            )
        elif species == "chinchilla":
            details = (
                "チンチラの甲状腺機能亢進症は近年症例が増加。"
                "高齢で痩せ、多食、行動変化を呈する。T4>5 µg/dLで疑診、超音波で甲状腺腫評価。"
                "メチマゾール 1-2 mg/kg PO q12h から開始しT4で調整。"
            )
        else:
            details = f"{species}での甲状腺機能亢進症は稀。メチマゾール 1-2 mg/kg PO q12hを外挿で使用、T4で個別調整。"
        return {
            "treatment_ja": details + " " + _small_mammal_supportive(species),
            "treatment": (
                f"Hyperthyroidism in {species}: methimazole 1-2 mg/kg PO q12h titrated to T4. "
                "Imaging to assess thyroid mass. Thyroidectomy or I-131 in select centers."
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                "鳥類で稀に報告。コザクラインコ、セキセイインコの腺腫が時に機能性。"
                "メチマゾール 0.1-0.2 mg/kg PO q24hを試験的に使用するが、データ限定的。"
                "甲状腺超音波、T4（鳥種別基準）で評価。" + _avian_supportive(species)
            ),
            "treatment": (
                "Rare in birds; reported adenomas in budgerigars/lovebirds may be functional. "
                "Methimazole 0.1-0.2 mg/kg PO q24h experimental. Ultrasound + species-specific T4."
            ),
        }
    if species in REPTILE:
        return {
            "treatment_ja": (
                "爬虫類の甲状腺機能亢進症は稀。リクガメ、グリーンイグアナで腺腫/腺癌報告あり。"
                "甲状腺摘出が第一選択。メチマゾールは外挿で2-5 mg/kg PO q24hを試行（データ限定）。"
                "T4は種別基準値が不明確で診断には超音波と病理が中心。" + _reptile_supportive(species)
            ),
            "treatment": (
                "Rare in reptiles; reports in tortoises and green iguanas with thyroid adenoma/carcinoma. "
                "Thyroidectomy first-line. Methimazole extrapolation 2-5 mg/kg PO q24h with limited data."
            ),
        }
    return None


def gen_hypothyroidism(species: str, name_ja: str) -> dict:
    """Hypothyroidism — common in dogs, rare in others."""
    if species == "dog":
        return {
            "treatment_ja": (
                "犬甲状腺機能低下症: 「ゴールドスタンダード」レボチロキシン 0.02 mg/kg PO q12h（最大0.8 mg）。"
                "4-8週後にピーク濃度（投与4-6時間後）と低濃度（投与直前）でTT4測定、用量調整。"
                "目標：投与4-6時間後TT4 30-50 nmol/L（高め）、TSH正常化。"
                "心血管系合併症（HCM、副腎機能不全）合併時はq24h製剤から漸増。"
                "原発性（90%）vs続発性の鑑別。自己免疫性甲状腺炎の早期スクリーニングを犬種別に推奨。"
            ),
            "treatment": (
                "Canine hypothyroidism: levothyroxine 0.02 mg/kg PO q12h (max 0.8 mg). "
                "Recheck TT4 peak (4-6h post-dose) and trough (pre-dose) at 4-8 weeks. "
                "Target peak TT4 30-50 nmol/L, TSH normalized. Start lower in cardiac/adrenal "
                "comorbidity. Differentiate primary (~90%) vs secondary."
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                "鳥類の真の甲状腺機能低下症は稀。甲状腺腫（ヨウ素欠乏性、セキセイインコに多い）が圧倒的に多く、"
                "経口ヨウ素補給（Lugol液 1滴/30 mL水、2週間）で改善する。"
                "真の機能低下症診断時はレボチロキシン 0.02 mg/kg q12-24hを試用（鳥種別データ限定）。"
                + _avian_supportive(species)
            ),
            "treatment": (
                "True hypothyroidism is rare in birds; iodine-deficiency goiter (especially in "
                "budgerigars) is far more common — oral iodine (Lugol's, 1 drop/30 mL water × 2 wk) is "
                "diagnostic and therapeutic. True hypothyroidism: levothyroxine 0.02 mg/kg q12-24h "
                "(species-specific data limited)."
            ),
        }
    if species == "horse":
        return {
            "treatment_ja": (
                "馬の甲状腺機能低下症は稀で、過剰診断が問題。EMSのインスリン抵抗性が誤って甲状腺機能低下症と診断されることが多い。"
                "TSH刺激試験で確認後、レボチロキシンナトリウム 0.05-0.1 mg/kg PO q24h を投与。"
                "ヨウ素過剰/欠乏、フルニキシン等NSAID影響を除外。EMSが疑われる場合は短期Tx試行（前述）。"
            ),
            "treatment": (
                "Equine hypothyroidism is rare and overdiagnosed (EMS often mislabeled). Confirm with "
                "TSH stimulation. Levothyroxine sodium 0.05-0.1 mg/kg PO q24h. Rule out iodine "
                "imbalance and NSAID effects."
            ),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species}での甲状腺機能低下症は稀で診断は慎重に。低T4のみでは診断不確実"
                "（病気個体は普遍的にT4低下＝euthyroid sick syndrome）。"
                "TSH刺激試験で確認後、レボチロキシン 0.01-0.02 mg/kg PO q12-24h試用。"
                + _small_mammal_supportive(species)
            ),
            "treatment": (
                f"Hypothyroidism is rare in {species}. Confirm with TSH stim (low T4 alone is "
                "non-specific; euthyroid sick syndrome common). Levothyroxine 0.01-0.02 mg/kg PO q12-24h."
            ),
        }
    if species in REPTILE:
        return {
            "treatment_ja": (
                "爬虫類で真の甲状腺機能低下症は極めて稀。リクガメのヨウ素欠乏性甲状腺腫が稀に報告（甲状腺腫大、肥満、無気力）。"
                "ヨウ素補給（食事性ケルプ）と適切なPOTZ・UVBが第一選択。"
                "確定診断時は外挿でレボチロキシン 0.02 mg/kg PO q24-48h。" + _reptile_supportive(species)
            ),
            "treatment": (
                "True hypothyroidism extremely rare in reptiles; iodine-deficiency goiter in tortoises "
                "reported. Dietary iodine + appropriate UVB/POTZ. Levothyroxine 0.02 mg/kg PO q24-48h "
                "by extrapolation if needed."
            ),
        }
    return None


def gen_hypoglycemia(species: str, name_ja: str) -> dict:
    """Hypoglycemia — species-specific causes (insulinoma in ferret, sepsis in puppies, etc.)."""
    if species == "ferret":
        return {
            "treatment_ja": (
                "フェレット低血糖は**インスリノーマ**が最多原因（中年以上で約30%発症）。"
                "急性発作: ブドウ糖 50% 0.5-1 mL/ferret IV slow、または蜂蜜を歯肉に塗布。"
                "輸液（5%ブドウ糖加リンゲル 10-20 mL/h）、再発予防にプレドニゾロン 0.5-2 mg/kg PO q12h（漸増）。"
                "ジアゾキシド 5-30 mg/kg PO q12h（インスリン抑制）はオランダ製品入手困難。"
                "外科（膵部分切除＋結節摘出）で寛解期間中央値240-365日。"
                "頻回少量給餌（生肉ベース、糖質ゼロ）。AAHA Exotic Companion Mammal 2022参照。"
            ),
            "treatment": (
                "Ferret hypoglycemia is most often due to insulinoma (~30% of middle-aged ferrets). "
                "Acute crisis: 50% dextrose 0.5-1 mL/ferret slow IV or honey to gums. Maintain on 5% "
                "dextrose-LRS 10-20 mL/h. Prednisolone 0.5-2 mg/kg PO q12h titrated. Diazoxide "
                "5-30 mg/kg PO q12h where available. Partial pancreatectomy + nodulectomy: median "
                "remission 240-365 days. Frequent small carnivore meals. AAHA 2022."
            ),
        }
    if species == "dog":
        return {
            "treatment_ja": (
                "犬の低血糖の原因別治療: ① インスリノーマ→部分膵切除＋プレドニゾロン 0.5-2 mg/kg PO q12h、"
                "ジアゾキシド 10-30 mg/kg PO q12h、頻回給餌、ストレプトゾトシン化学療法（特殊例）。"
                "② 若齢小型犬の発作性低血糖→温糖水 1-2 mL/kg PO即時、5%ブドウ糖加リンゲルIV、保温、頻回少量給餌。"
                "③ 敗血症性→原疾患治療＋ブドウ糖補正。"
                "④ アジソン病→グルココルチコイド補充。"
                "急性発作: ブドウ糖 50% 0.5-1 mL/kg IV slow（希釈してから）。"
            ),
            "treatment": (
                "Canine hypoglycemia management depends on etiology: insulinoma (partial pancreatectomy + "
                "prednisolone 0.5-2 mg/kg PO q12h, diazoxide 10-30 mg/kg PO q12h, streptozocin in select "
                "cases); juvenile/toy-breed hypoglycemia (warm dextrose PO, 5% dextrose-LRS IV, "
                "frequent feeding); sepsis (treat primary disease); Addisonian crisis (glucocorticoid "
                "replacement). Acute: 50% dextrose 0.5-1 mL/kg slow IV diluted."
            ),
        }
    if species == "cat":
        return {
            "treatment_ja": (
                "猫の低血糖は犬より稀。インスリン過量投与（DM管理中）、敗血症、肝不全、新生子の飢餓が主因。"
                "急性発作: ブドウ糖 50% 1 mL/kg IV slow（希釈）。"
                "肝リピドーシス併発時は経腸栄養（食道瘻チューブ）が予後改善。"
                "原疾患検索（ACTH刺激試験、肝バイオプシー、血液培養）。"
            ),
            "treatment": (
                "Feline hypoglycemia is less common than canine. Causes: insulin overdose, sepsis, "
                "hepatic lipidosis, neonatal starvation. Acute: 50% dextrose 1 mL/kg slow IV diluted. "
                "Esophagostomy tube feeding improves outcome with lipidosis comorbidity."
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                "鳥の低血糖（正常血糖200-400 mg/dL、<150で症状）: 緊急時5%ブドウ糖SC 25-50 mL/kg、または、"
                "経口糖水（ガベージ）2-5 mL/kg。原因鑑別: 飢餓、敗血症、肝不全、雛の栄養不良、抱卵期ストレス。"
                "肝疾患併発時はラクツロース 0.3 mL/kg PO q8h、シリマリン 30-50 mg/kg PO q24h。"
                + _avian_supportive(species)
            ),
            "treatment": (
                "Avian hypoglycemia (normal BG 200-400 mg/dL): 5% dextrose 25-50 mL/kg SC or oral 2-5 mL/kg "
                "via gavage. Differentials: starvation, sepsis, hepatic failure, chick malnutrition, "
                "egg-laying stress. Hepatic: lactulose 0.3 mL/kg PO q8h, silymarin 30-50 mg/kg PO q24h."
            ),
        }
    if species in REPTILE:
        return {
            "treatment_ja": (
                "爬虫類の低血糖は肝不全、敗血症、長期飢餓、卵黄嚢吸収後の新生子で発生。"
                "5%ブドウ糖加リンゲル 10-30 mL/kg ICe/IV、POTZ加温で代謝復活。"
                "経口給餌は反応回復後（誤嚥防止）。原因検索（肝酵素、血液培養、超音波）。"
                + _reptile_supportive(species)
            ),
            "treatment": (
                "Reptilian hypoglycemia: hepatic failure, sepsis, prolonged anorexia, neonates with "
                "depleted yolk. 5% dextrose-LRS 10-30 mL/kg ICe/IV; warm to POTZ. Resume PO feeding "
                "only when alert. Investigate hepatic enzymes, blood cultures, ultrasound."
            ),
        }
    if species == "amphibian":
        return {
            "treatment_ja": (
                "両生類の低血糖（稀）: 5%ブドウ糖浴 15分（皮膚吸収）、POTZ範囲内に加温。"
                "原因（飢餓、肝不全、敗血症）の同定と治療。反応回復後に給餌再開。" + _reptile_supportive(species)
            ),
            "treatment": (
                "Amphibian hypoglycemia (rare): 5% dextrose bath × 15 min (cutaneous absorption); "
                "warm to POTZ. Investigate starvation, hepatic failure, sepsis."
            ),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species}の低血糖は飢餓（特に小型げっ歯類で容易に発症）、敗血症、肝不全、新生子で発生。"
                "5%ブドウ糖加リンゲル 50-100 mL/kg SC、保温、シリンジ給餌（Critical Care）。"
                "原因鑑別と原疾患治療が必須。" + _small_mammal_supportive(species)
            ),
            "treatment": (
                f"{species} hypoglycemia: 5% dextrose-LRS 50-100 mL/kg SC, warm, syringe-feed. "
                "Investigate starvation, sepsis, hepatic failure, neonatal causes."
            ),
        }
    return None


def gen_cryptosporidium(species: str, name_ja: str) -> dict:
    if species in REPTILE:
        return {
            "treatment_ja": (
                "爬虫類クリプトスポリジウム症（C. serpentis/varanii）に確実な治癒治療はない。"
                "パロモマイシン 300-800 mg/kg PO q24h × 10-14日が緩和に最も用いられる。"
                "ハイパーイミューンウシ初乳（HBC）パラメチルアミドール製剤の試験報告あり。"
                "感染個体は隔離し、長期的にはhumaneendpointを検討。"
                "⚠人獣共通の懸念は限定的（C. parvumとは別種が多い）。"
                "PCR/抗酸染色で診断。予後不良。"
            ),
            "treatment": (
                "Reptilian cryptosporidiosis (C. serpentis/varanii) has no curative therapy. "
                "Paromomycin 300-800 mg/kg PO q24h × 10-14 days is most commonly used for amelioration. "
                "Hyperimmune bovine colostrum trials underway. Isolate infected animals; consider "
                "humane endpoint long-term. Zoonotic risk is limited for these species (≠ C. parvum)."
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                "鳥類クリプトスポリジウム症（C. baileyi、C. galli等）: 確立された治療なし。"
                "パロモマイシン 100 mg/kg PO q12h × 7-14日が試みられる。アジスロマイシン 40 mg/kg PO q24h × 10-14日も選択肢。"
                "免疫不全鳥（PBFD合併等）で重症化。隔離、環境消毒（5%アンモニア、過酢酸）。"
                + _avian_supportive(species)
            ),
            "treatment": (
                "Avian cryptosporidiosis (C. baileyi, C. galli): paromomycin 100 mg/kg PO q12h × 7-14 d "
                "or azithromycin 40 mg/kg PO q24h × 10-14 d (limited efficacy). Severe in "
                "immunosuppressed (PBFD comorbidity). Isolate; disinfect with 5% ammonia."
            ),
        }
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                "犬猫クリプトスポリジウム症（C. canis/felis主体、まれにC. parvum）: 健常成獣は自限性が多い。"
                "持続性下痢：アジスロマイシン 10 mg/kg PO q24h × 7日、パロモマイシン 125-165 mg/kg PO q12h × 5日。"
                "免疫不全（FIV+、化学療法中）では遷延化、人獣共通感染リスクに注意。"
                "輸液・電解質管理、止瀉薬（適応症のみ）。"
            ),
            "treatment": (
                "Canine/feline cryptosporidiosis (C. canis, C. felis, rarely C. parvum): self-limiting "
                "in healthy adults. Persistent diarrhea: azithromycin 10 mg/kg PO q24h × 7d or "
                "paromomycin 125-165 mg/kg PO q12h × 5d. Zoonotic precautions in immunocompromised."
            ),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species}でのクリプトスポリジウム症（多くはC. parvumまたは宿主特異種）: 治療は補助的。"
                "パロモマイシン 100 mg/kg PO q12h × 7日が試行される。"
                "免疫不全個体（コルチコステロイド使用、リンパ腫など）で重症化。"
                "⚠人獣共通感染症（特にC. parvum）。" + _small_mammal_supportive(species)
            ),
            "treatment": (
                f"{species} cryptosporidiosis (often C. parvum or host-adapted species): supportive. "
                "Paromomycin 100 mg/kg PO q12h × 7d. Severe in immunocompromised. Zoonotic precautions."
            ),
        }
    if species == "amphibian":
        return {
            "treatment_ja": (
                "両生類クリプトスポリジウム症（C. fragile, C. serpentis亜種等）: 確立された治療なし。"
                "パロモマイシン 30-100 mg/kg PO q24hを試験的に使用。"
                "新興病原体として個体群モニタリング重要。バイオセキュリティ徹底。" + _reptile_supportive(species)
            ),
            "treatment": (
                "Amphibian cryptosporidiosis: no established therapy. Paromomycin 30-100 mg/kg PO q24h "
                "experimental. Emerging pathogen in amphibian populations; strict biosecurity."
            ),
        }
    return None


def gen_dermatophytosis(species: str, name_ja: str) -> dict:
    """Ringworm — common across species, treatment is similar with species-specific drug adjustments."""
    common_warning = ""
    if species == "rabbit":
        common_warning = " ⚠ウサギは経口β-ラクタムが禁忌のため抗真菌薬を選択する。"
    elif species == "chinchilla":
        common_warning = " ⚠フィプロニル禁忌（致死性）。長毛のため毛刈り併用。"
    if species in AVIAN:
        return {
            "treatment_ja": (
                "鳥類皮膚糸状菌症（稀、主にMicrosporum/Trichophyton）: 局所ミコナゾール2%軟膏/シャンプー q12h、"
                "全身ではイトラコナゾール 5-10 mg/kg PO q24h × 4-6週、TerbinafineFin 10-30 mg/kg PO q24h × 6-8週。"
                "肝酵素モニタリング必須。環境消毒（次亜塩素酸ナトリウム1:10）。⚠人獣共通。" + _avian_supportive(species)
            ),
            "treatment": (
                "Avian dermatophytosis (rare, Microsporum/Trichophyton): topical miconazole 2% q12h, "
                "systemic itraconazole 5-10 mg/kg PO q24h × 4-6 wk or terbinafine 10-30 mg/kg PO q24h × "
                "6-8 wk with LFT monitoring. Environmental sodium hypochlorite 1:10. Zoonotic."
            ),
        }
    if species in SMALL_MAMMAL:
        details = ""
        if species == "hedgehog":
            details = (
                "ハリネズミでは**Trichophyton erinacei**が病原。"
                "テルビナフィン 30-40 mg/kg PO q24h × 4-6週が第一選択。"
                "局所2%エナイル/ミコナゾール、棘部位は刺激最小化。"
                "⚠人獣共通：飼い主の手指白癬を確認。"
            )
        else:
            details = (
                f"{species}皮膚糸状菌症: 局所2%ミコナゾールクリーム q12h、"
                "全身でイトラコナゾール 5-10 mg/kg PO q24h × 4-6週またはテルビナフィン 20-40 mg/kg PO q24h × 4-6週。"
                "肝酵素q2週モニタ。長毛種は毛刈り。"
            )
        return {
            "treatment_ja": details
            + " 環境消毒（次亜塩素酸1:10）、寝床完全交換。⚠人獣共通感染症。"
            + common_warning
            + " "
            + _small_mammal_supportive(species),
            "treatment": (
                f"{species} dermatophytosis: topical 2% miconazole q12h, systemic itraconazole "
                "5-10 mg/kg PO q24h × 4-6 wk or terbinafine 20-40 mg/kg PO q24h × 4-6 wk. LFT q2w. "
                "Clip long fur. Environmental bleach 1:10. Zoonotic."
            ),
        }
    if species in REPTILE:
        return {
            "treatment_ja": (
                "爬虫類皮膚糸状菌症（Trichophyton, Microsporum, Nannizziopsis、CANV等）: "
                "イトラコナゾール 5 mg/kg PO q24h × 4-8週 + 局所2%クロルヘキシジン浴 q24h。"
                "ヘビではNannizziopsis（SFD）の確認が重要。"
                "POTZ最適化（免疫機能の基盤）、湿度管理、ケージ消毒（クロルヘキシジン2%）。"
                + _reptile_supportive(species)
            ),
            "treatment": (
                "Reptilian dermatophytosis (Trichophyton, Microsporum, Nannizziopsis/CANV): "
                "itraconazole 5 mg/kg PO q24h × 4-8 wk + topical 2% chlorhexidine baths q24h. "
                "Confirm Nannizziopsis (SFD) in snakes. Optimize POTZ and humidity; disinfect "
                "enclosure with 2% chlorhexidine."
            ),
        }
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species}皮膚糸状菌症（Microsporum canis主体）: ① 全身性治療**必須**："
                "イトラコナゾール 5 mg/kg PO q24h（猫はパルス療法 1週オン1週オフ可）または"
                "テルビナフィン 30-40 mg/kg PO q24h × 4-6週以上、PCR陰性化まで継続。"
                "② 局所：エナイルコナゾール（Imaverol）1:50浸漬 q3-4日 または "
                "ミコナゾール+クロルヘキシジンシャンプー q3-4日。"
                "③ 環境：徹底的清掃と次亜塩素酸1:10 適用、毛除去（HEPAクリーナー）。"
                "④ モニタリング：2週毎にPCR/培養、2回連続陰性で治癒判定。⚠人獣共通：免疫不全家族に注意。"
            ),
            "treatment": (
                f"{species} dermatophytosis (M. canis): MANDATORY systemic itraconazole 5 mg/kg PO q24h "
                "(cats: pulse therapy 1-on/1-off OK) or terbinafine 30-40 mg/kg PO q24h × ≥4-6 wk until "
                "PCR-negative. Topical: enilconazole 1:50 dip q3-4d OR miconazole-chlorhexidine "
                "shampoo q3-4d. Environmental decontamination critical (bleach 1:10, HEPA vacuum). "
                "Cure = 2 negative PCR/cultures. Zoonotic."
            ),
        }
    return None


# ----------------------------------------------------------------------------
# Lookup
# ----------------------------------------------------------------------------

# (substring pattern, generator function)
DISEASE_GENERATORS: list[tuple[str, Callable[[str, str], Optional[dict]]]] = [
    # Endocrine — cross-species cleanup
    ("糖尿病", gen_diabetes),
    ("甲状腺機能亢進症", gen_hyperthyroidism),
    ("甲状腺過形成", gen_hyperthyroidism),
    ("甲状腺腫", gen_hypothyroidism),  # most "甲状腺腫" in non-feline = goiter (hypothyroid spectrum)
    ("甲状腺機能低下症", gen_hypothyroidism),
    ("甲状腺疾患", gen_hypothyroidism),
    # Hypoglycemia
    ("低血糖", gen_hypoglycemia),
    # Cryptosporidium
    ("クリプトスポリジウム", gen_cryptosporidium),
    # Dermatophytosis
    ("皮膚糸状菌症", gen_dermatophytosis),
    ("白癬菌感染", gen_dermatophytosis),
    ("皮膚真菌感染", gen_dermatophytosis),
]


def lookup_disease_generator(name_ja: str) -> Optional[Callable[[str, str], Optional[dict]]]:
    """Find a generator function for a disease name. Returns None if not in library."""
    if not name_ja:
        return None
    for pattern, fn in DISEASE_GENERATORS:
        if pattern in name_ja:
            return fn
    return None


def generate_content(species: str, name_ja: str, name_en: str = "") -> Optional[dict]:
    """High-level entry point. Returns content dict or None."""
    fn = lookup_disease_generator(name_ja)
    if fn is None:
        return None
    try:
        return fn(species, name_ja)
    except Exception:
        return None
