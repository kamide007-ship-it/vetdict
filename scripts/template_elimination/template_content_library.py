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


# ============================================================================
# Pathogen-specific viral content (replaces "特異的抗ウイルス治療はない" templates)
# ============================================================================


def gen_viral_disease(species: str, name_ja: str) -> Optional[dict]:
    """Virus-specific treatment when a viral disease is named (not generic 'viral')."""
    nm = name_ja or ""
    species_ja = {
        "dog": "犬",
        "cat": "猫",
        "rabbit": "ウサギ",
        "ferret": "フェレット",
        "horse": "馬",
    }.get(species, species)

    # Canine parvovirus
    if "パルボウイルス" in nm and species == "dog":
        return {
            "treatment_ja": (
                "犬パルボウイルス感染症の治療（緊急）: "
                "① 入院・隔離（バリアナーシング）、輸液療法が治療の根幹—等張晶質液（生理食塩水・乳酸リンゲル）"
                "の脱水補正＋維持＋継続喪失分（嘔吐・下痢量）の合計を計算し IV または骨髄内投与。"
                "② 制吐剤: マロピタント 1 mg/kg IV/SC q24h（生後8週以上）、オンダンセトロン 0.5-1 mg/kg IV/PO q8-12h（重症例）。"
                "③ 二次性敗血症予防: アンピシリン/サルバクタム 22-30 mg/kg IV q8h、または セファゾリン 22 mg/kg IV q8h "
                "（好中球減少時はエンロフロキサシン 5 mg/kg IV q24h追加で広域カバー）。"
                "④ 鎮痛: ブプレノルフィン 0.01-0.02 mg/kg IV/IM q6-8h（嘔吐改善後、軽度オピオイド）。"
                "⑤ 早期経腸栄養: 嘔吐管理後24時間以内に少量から再開（生存率改善）—鼻食道チューブまたは小量PO。"
                "⑥ 重症例: 血漿輸血 6-10 mL/kg（低アルブミン血症・凝固障害）、組換え犬G-CSF 5 µg/kg SC q24h（重度好中球減少）、"
                "経口モノクローナル抗体（CPMA、Elanco）が早期投与で生存率向上。"
                "AAHA Canine Vaccination Guidelines 2022/ACVIM Consensus 2010参照。"
            ),
            "prognosis_ja": (
                "適切な集中治療で生存率80-95%。治療なしでは致死率70-91%。"
                "白血球減少の程度（WBC<1000/µL）、敗血症併発、播種性血管内凝固症候群（DIC）、低Albが予後不良因子。"
                "治療開始から3-5日が山場で、これを超えれば回復に向かう。"
            ),
        }
    # Canine distemper
    if ("ジステンパー" in nm or "distemper" in (name_ja or "").lower()) and species == "dog":
        return {
            "treatment_ja": (
                "犬ジステンパー（特異的抗ウイルス薬なし）: 集中支持療法と二次感染管理が中心。"
                "① 輸液療法: 等張晶質液 60-90 mL/kg/日 IV、脱水補正。"
                "② 二次性細菌感染（呼吸器・消化器）: ドキシサイクリン 5 mg/kg PO q12h、または "
                "アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h。"
                "③ 神経症状（ミオクローヌス・痙攣）: フェノバルビタール 2-4 mg/kg PO q12h、"
                "発作重積はジアゼパム 0.5 mg/kg IV、レベチラセタム 20-30 mg/kg PO/IV q8h。"
                "④ 喀痰排出促進: アセチルシステイン ネブライザー 10% × 10分 q8-12h。"
                "⑤ 栄養支持: 食欲不振時は経鼻食道チューブ給餌。"
                "⑥ アシクロビル 10-20 mg/kg IV q8h はin vitroで有効性報告あるが臨床効果は限定的。"
                "予防はワクチン（コアワクチン、DHPP）が最重要。AAHA Canine Vaccination Guidelines 2022参照。"
            ),
            "prognosis_ja": (
                "急性期生存率は支持療法で50-70%。神経症状発症例は予後不良で50%以上が安楽死または死亡。"
                "回復例も歯エナメル形成不全、ハードパッド（足蹠角化症）、慢性神経学的後遺症が残存することがある。"
            ),
        }
    # Feline calicivirus / herpesvirus (URI complex)
    if species == "cat" and ("カリシ" in nm or "ヘルペスウイルス" in nm or "FHV" in nm or "FCV" in nm):
        return {
            "treatment_ja": (
                "猫上部気道感染症（FHV-1/FCV）の治療: "
                "① 抗ウイルス薬（FHV-1）: ファムシクロビル 90 mg/kg PO q8-12h × 7-21日（最も推奨、ISFM 2018）、"
                "外用シドフォビル 0.5% 点眼 q12h（角膜潰瘍時）。"
                "② 二次性細菌感染（鼻汁・結膜炎）: ドキシサイクリン 10 mg/kg PO q24h × 21-28日（Bordetella/Mycoplasma "
                "/Chlamydia疑い時）、または アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h。"
                "③ 角膜潰瘍: オフロキサシン点眼 q4-6h、L-リジン 250-500 mg/cat PO q12h（FHV-1抑制、エビデンス限定）。"
                "④ ネブライザー（生食 q8h）で粘液排出促進。"
                "⑤ 食欲増進: ミルタザピン 1.88 mg/cat PO q48h、カプロモレリン 3 mg/kg PO q24h。"
                "⑥ 重症FCV変異株（virulent systemic FCV）は致死率最大67%—隔離・支持療法強化。"
                "ISFM Consensus Guidelines 2018 on Feline URTD参照。"
            ),
        }
    # Feline panleukopenia / FPV
    if species == "cat" and ("汎白血球減少" in nm or "panleukopenia" in (name_ja or "").lower()):
        return {
            "treatment_ja": (
                "猫汎白血球減少症（FPV）の治療（緊急、特に子猫）: "
                "① 入院・厳重な隔離（パルボウイルスは環境中で1年以上生存、漂白剤1:32必須）。"
                "② 積極的輸液療法: 等張晶質液で脱水補正（5-12%）+ 維持量 + 継続損失分。"
                "重度脱水ではコロイド（ヘタスターチ 5-10 mL/kg/日）併用。"
                "③ 制吐剤: マロピタント 1 mg/kg IV/SC q24h、オンダンセトロン 0.5 mg/kg IV q8-12h。"
                "④ 二次性敗血症予防: アンピシリン/サルバクタム 22 mg/kg IV q8h ± エンロフロキサシン "
                "5 mg/kg IV q24h（好中球減少時、ただし成長軟骨への影響に注意）。"
                "⑤ 低血糖補正: 50%デキストロース 0.5 mL/kg IV ボーラス、その後 2.5-5% デキストロース CRI。"
                "⑥ 重症例: 血漿輸血 6-10 mL/kg（凝固障害・低Alb）、組換え猫インターフェロンω "
                "（生存率改善エビデンス、入手可能な地域で）。"
                "⑦ 早期経腸栄養（嘔吐管理後24時間以内）。"
                "予防はFVRCPコアワクチンが最重要。AAFP Vaccination Guidelines 2020参照。"
            ),
            "prognosis_ja": (
                "未治療の致死率60-90%。積極的支持療法で生存率50-80%に改善。"
                "予後因子: WBC nadir（<1000/μL→不良）、低アルブミン血症、低体温、敗血症の併発。"
                "WBCが3-5日目に回復開始すれば予後良好。"
            ),
        }
    # Generic viral disease (fallback when virus is named but not specifically known)
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}における{nm}の治療: 特異的抗ウイルス薬は限定的—支持療法と二次感染予防が中心。"
                "① 輸液療法: 等張晶質液 60-80 mL/kg/日 IV（脱水補正＋維持）。重症は90 mL/kg初期ボーラス。"
                "② 制吐剤（消化器症状時）: マロピタント 1 mg/kg IV/SC q24h、オンダンセトロン 0.5 mg/kg IV q8h。"
                "③ 二次性細菌感染予防: アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h、または "
                "ドキシサイクリン 5-10 mg/kg PO q12h（呼吸器症状時）。"
                "④ 食欲増進: "
                + (
                    "ミルタザピン 1.88 mg/cat PO q48h、カプロモレリン 3 mg/kg PO q24h。"
                    if species == "cat"
                    else "カプロモレリン 3 mg/kg PO q24h、ミルタザピン 0.6 mg/kg PO q24h。"
                )
                + "⑤ 隔離（感染力が消失するまで）、ケージ消毒（次亜塩素酸1:32、エンベロープウイルスはエタノール70%でも可）。"
                "⑥ ワクチン未接種個体の同居動物にはコアワクチン接種を検討。"
                "AAHA/AAFP Vaccination Guidelines参照。"
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}における{nm}: 特異的抗ウイルス療法は限定的。"
                "① 隔離・バリアナーシング（多くの鳥ウイルスは飛沫・羽毛屑から伝播）。"
                "② 支持療法: 保温28-30℃、皮下/骨内輸液 50-100 mL/kg/日（温乳酸リンゲル）、強制給餌（Emeraid Omnivore 20-30 mL/kg q4-6h）。"
                "③ 二次性細菌・真菌感染予防: エンロフロキサシン 10-15 mg/kg PO/IM q12h、"
                "イトラコナゾール 5-10 mg/kg PO q24h（アスペルギルス予防、長期使用は肝酵素モニタ）。"
                "④ ウイルス特異的: PBFD/ポリオーマ→組換えαインターフェロン 1-10万IU/kg SC q24h（限定的エビデンス）。"
                "⑤ 群管理: 新規導入鳥は最低30-45日検疫、PCR陰性確認後合流。" + _avian_supportive(species)
            ),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}における{nm}: 特異的抗ウイルス療法は限定的。"
                "① 隔離・バリアナーシング、入院ケージは漂白剤1:32で消毒。"
                "② 支持療法: 輸液 80-100 mL/kg/日 SC/IV、保温26-28℃、シリンジ給餌（Critical Care）。"
                "③ 二次性細菌感染予防: エンロフロキサシン 5-10 mg/kg PO/SC q12-24h（草食種に経口β-ラクタムは禁忌）。"
                "④ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h。"
                + _small_mammal_supportive(species)
            ),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}における{nm}: 特異的抗ウイルス療法は限定的。"
                "① 隔離（パラミクソ・アデノ・アレナ等のウイルスは爬虫類群で集団発症のリスク）。"
                "② POTZ最適化（免疫機能回復の前提）、湿度・UVB調整。"
                "③ 支持療法: 輸液 25-30 mL/kg/日 SC/ICe、強制給餌（Carnivore Care）、栄養補給。"
                "④ 二次性細菌感染予防: セフタジジム 20 mg/kg IM q72h（嫌気性カバー要時）。"
                "⑤ 重症: αインターフェロン経験的使用報告あり（エビデンス限定）。" + _reptile_supportive(species)
            ),
        }
    if species == "horse":
        return {
            "treatment_ja": (
                f"{species_ja}における{nm}: 特異的抗ウイルス療法は症例選択的。"
                "① 隔離・バイオセキュリティ徹底（EIV/EHV-1等は群感染）、ウマ疾患届出対象は所管に連絡。"
                "② 支持療法: 等張電解質輸液 2-4 L/h IV、解熱（フルニキシン・メグルミン 1.1 mg/kg IV q12h）、栄養維持。"
                "③ 二次性細菌感染予防: ペニシリン G 22,000 IU/kg IM q12h ± ゲンタマイシン 6.6 mg/kg IV q24h。"
                "④ EHV-1神経型: アシクロビル 20 mg/kg PO q8h、バラシクロビル 27 mg/kg PO q12h、デキサメサゾン 0.05 mg/kg IV q24h。"
                "⑤ ワクチン: コアワクチン（EEE/WEE/西ナイル/破傷風）と疫学的に必要なリスクワクチン。"
                "AAEP Vaccination Guidelines参照。"
            ),
        }
    return None


# ============================================================================
# Pathogen-specific bacterial content (replaces "細菌感染症：培養感受性..." template)
# ============================================================================


def gen_bacterial_named(species: str, name_ja: str) -> Optional[dict]:
    """Pathogen-specific bacterial infection treatment when organism is named."""
    nm = name_ja or ""
    species_ja = _species_label_ja_local(species)

    if "サルモネラ" in nm:
        return {
            "treatment_ja": (
                f"{species_ja}におけるサルモネラ症の治療: "
                "① 健常成獣の無症候性キャリアは抗菌薬を控え自然排菌待ち（抗菌薬は耐性化・キャリア化リスク）。"
                "② 重症臨床例（敗血症・下血・脱水）には培養感受性後の抗菌薬: "
                "エンロフロキサシン 10-20 mg/kg PO/IM q12-24h（鳥類）/ 5-10 mg/kg PO q12-24h（小型哺乳類） "
                "× 14-21日、または トリメトプリム・スルファ 15-30 mg/kg PO q12h。"
                "③ 輸液療法 + 電解質補正、制吐・止瀉対症療法。"
                "④ ⚠人獣共通感染症—家族（特に小児・免疫不全者）の手洗い・接触予防徹底。"
                "⑤ 環境消毒は塩素系（次亜塩素酸 1:10）または過酢酸が有効。"
                "⑥ 群飼育では感染源（飼料・水・媒介動物）の検索と隔離。"
            ),
        }
    if "大腸菌" in nm or "E. coli" in nm or "コリバクテリア" in nm:
        return {
            "treatment_ja": (
                f"{species_ja}における大腸菌感染症: "
                "① 培養感受性試験必須（病原性株はβラクタマーゼ産生・キノロン耐性が増加）。"
                "② 経験的治療: アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h（小型哺乳類除く）、"
                "エンロフロキサシン 5-15 mg/kg PO/SC/IM q12-24h、または セフタジジム 20-30 mg/kg IM q12h（鳥類含む）。"
                "③ 敗血症・腸炎・尿路感染症の併発確認、それぞれに対する全身管理。"
                "④ 子犬・新生個体ではUmbilical infection/sepsisを疑い、ボディウォーマーで保温、ブドウ糖補正。"
                "⑤ 環境衛生: 給餌器・水ボトル・床面の毎日消毒（次亜塩素酸1:32）。"
                "⑥ プロバイオティクス（FortiFlora、Bene-Bac）併用で腸内細菌叢回復を促進。"
            ),
        }
    if "ブドウ球菌" in nm or "Staphylococc" in nm.lower() or "黄色ブドウ球" in nm:
        return {
            "treatment_ja": (
                f"{species_ja}におけるブドウ球菌感染症: "
                "① 必ず培養感受性試験を実施（MRSP/MRSA増加中）。"
                "② Methicillin感受性株: アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h、"
                "セファレキシン 22-30 mg/kg PO q8-12h、クリンダマイシン 5-10 mg/kg PO q12h。"
                "③ MRSP/MRSA陽性: ドキシサイクリン 5-10 mg/kg PO q12h、クロラムフェニコール 50 mg/kg PO q8h "
                "（再生不良性貧血リスクのため家族曝露注意）、アミカシン 15 mg/kg IM q24h（要TDM）。"
                "④ 膿瘍は外科的排膿＋局所洗浄が抗菌薬単独より有効。"
                "⑤ 皮膚病変はクロルヘキシジン 2-4% シャンプー q3-7日 + 抗菌軟膏。"
                "⑥ 再発例ではバイオフィルム形成と感染源（イヤホン・寝具・ハウス）の除去/消毒を見直す。"
            ),
        }
    if "クレブシエラ" in nm or "Klebsiella" in nm.lower():
        return {
            "treatment_ja": (
                f"{species_ja}におけるクレブシエラ感染症: "
                "① ESBL産生株が多くNon-CarbapenemとTrim/Sulf耐性多発。培養感受性必須。"
                "② 第一選択（感受性確認後）: エンロフロキサシン 10 mg/kg PO/IM q12-24h、"
                "アミカシン 15-20 mg/kg IM q24h（腎機能・TDM必須）、"
                "セフタジジム 20-30 mg/kg IM q12h、メロペネム 8-12 mg/kg IV q8h（ESBL/重症例）。"
                "③ 主に肺炎・尿路感染・敗血症—臓器別の支持療法を同時並行。"
                "④ ⚠院内感染源として重要—入院・在宅環境の徹底消毒（次亜塩素酸1:10、グルタラール2%）。"
                "⑤ 免疫不全動物（FIV・ステロイド長期）で重症化リスク。"
            ),
        }
    if "緑膿菌" in nm or "Pseudomonas" in nm:
        return {
            "treatment_ja": (
                f"{species_ja}における緑膿菌感染症: "
                "① β-ラクタマーゼ・効率排出ポンプによる耐性が多発—培養感受性必須。"
                "② 全身: シプロフロキサシン/エンロフロキサシン 10-20 mg/kg PO/IM q12h、"
                "セフタジジム 20-30 mg/kg IM q8-12h、アミカシン 15-20 mg/kg IM q24h（TDM）、"
                "ピペラシリン/タゾバクタム 50 mg/kg IV q6-8h（重症）。"
                "③ 外耳炎: 1% 酢酸 + ゲンタマイシン点耳 q12h、慢性例はTRIS-EDTA前処置で外膜浸透改善。"
                "④ 角膜潰瘍: シプロフロキサシン 0.3% 点眼 q1-2h（最初24h）、その後 q4-6h。"
                "⑤ ⚠院内感染源—環境消毒（次亜塩素酸1:10、加熱）、湿潤環境を避ける。"
            ),
        }
    if "クロストリジウム" in nm or "Clostridi" in nm:
        return {
            "treatment_ja": (
                f"{species_ja}におけるクロストリジウム感染症: "
                "① 第一選択: メトロニダゾール 15-25 mg/kg PO q12h × 5-10日 "
                "（神経毒性に注意、長期投与は避ける）、または アモキシシリン 11-22 mg/kg PO q12h（C. perfringens）。"
                "② C. difficile: バンコマイシン 10 mg/kg PO q8h × 7-10日（耐性例）。"
                "③ 重症腸毒血症: 抗毒素血清（入手可能な場合）、輸液・電解質補正、嫌気性ショック対応。"
                "④ 食事性管理: 高繊維食、急激な食変えを避け、プロバイオティクスで腸内細菌叢回復。"
                "⑤ 草食動物（ウサギ・モルモット）はC. difficile腸炎リスクが極めて高い—ペニシリン系・セファロスポリン系経口禁忌。"
                "⑥ 環境芽胞対策: 次亜塩素酸1:10で消毒、乾燥環境維持。"
            ),
        }
    if "パスツレラ" in nm or "Pasteurell" in nm.lower():
        return {
            "treatment_ja": (
                f"{species_ja}におけるパスツレラ症 (Pasteurella multocida): "
                "① 第一選択: エンロフロキサシン 5-15 mg/kg PO/SC q12-24h × 14-30日（ウサギの慢性例は3ヶ月以上）、"
                "ペニシリン G 40,000-60,000 IU/kg SC q24h（ウサギは経口β-ラクタム禁忌、SC/IMのみ）、"
                "トリメトプリム・スルファ 15-30 mg/kg PO q12h。"
                "② 鼻腔・上気道炎（snuffles）: ネブライザー（生食 + ゲンタマイシン 50 mg/4 mL）q8-12h。"
                "③ 皮下膿瘍は外科的切開・除去（マルセイン化）が再発予防に重要—単純な切開排膿は不十分。"
                "④ 中耳・内耳炎: 全身抗菌薬 + 鼓室洗浄、ステロイド使用は議論あり（短期低用量のみ）。"
                "⑤ 慢性キャリア・群飼育: 感染個体の隔離、新規導入時の鼻腔培養スクリーニング。"
                + _supportive_block(species)
            ),
        }
    return None


def _species_label_ja_local(species: str) -> str:
    """Local helper for species label (avoid circular import in fallback_generator)."""
    return {
        "dog": "犬",
        "cat": "猫",
        "rabbit": "ウサギ",
        "guinea_pig": "モルモット",
        "hamster": "ハムスター",
        "chinchilla": "チンチラ",
        "ferret": "フェレット",
        "hedgehog": "ハリネズミ",
        "sugar_glider": "フクロモモンガ",
        "degu": "デグー",
        "bird": "鳥",
        "parakeet": "インコ",
        "parrot": "オウム",
        "reptile": "爬虫類",
        "tortoise": "リクガメ",
        "snake": "ヘビ",
        "lizard": "トカゲ",
        "amphibian": "両生類",
        "horse": "馬",
        "fish": "魚",
        "exotic_other": "エキゾチック動物",
    }.get(species, species)


# ============================================================================
# Mycobacteriosis — species-specific (zoonotic risk varies dramatically)
# ============================================================================


def gen_mycobacteriosis(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    base_warning = (
        "⚠⚠ 人獣共通感染症: M. tuberculosis complex (M. bovis)、M. avium complex は免疫不全者に "
        "重大リスク。診断確定時は公衆衛生当局への報告と家族の医療相談を強く推奨。"
    )
    if species == "cat":
        return {
            "treatment_ja": (
                "猫マイコバクテリウム感染症: 多くはM. avium complex (MAC)、M. microti、M. bovis。"
                "① 診断: 抗酸染色 (Ziehl-Neelsen)、PCR、培養（4-12週要）、ITS-PCRで種同定。"
                "② 治療プロトコル（多剤併用、最低6-9ヶ月、感受性で個別）: "
                "リファンピシン 10-15 mg/kg PO q24h + クラリスロマイシン 5-7.5 mg/kg PO q12h + "
                "プラジカンテルではなく プラジコフロキサシン または ドキシサイクリン 10 mg/kg PO q12h。"
                "③ M. tuberculosis complex感染確定例は治療成功率低く、人獣共通リスクから安楽死を検討。"
                "④ 肝・腎機能・CBC を月1回モニタ（リファンピシンは肝毒性）。" + base_warning
            ),
            "prognosis_ja": (
                "MAC: 多剤併用6-12ヶ月で寛解率50-70%。播種性は予後不良。M. bovis/tuberculosis: 治療困難で予後不良。"
            ),
        }
    if species == "dog":
        return {
            "treatment_ja": (
                "犬マイコバクテリウム感染症: M. avium complex、M. bovis、M. tuberculosis、稀にM. fortuitum。"
                "① 多剤併用6-12ヶ月: リファンピシン 10-15 mg/kg PO q24h + アジスロマイシン 5-10 mg/kg PO q24h + "
                "クラリスロマイシン 5-15 mg/kg PO q12h（または エンロフロキサシン 5-10 mg/kg PO q24h）。"
                "② M. tuberculosis complex確定は安楽死推奨（人獣共通、Public Health優先）。"
                "③ 皮膚・皮下感染（M. fortuitum等）は外科的切除＋上記抗菌薬を6ヶ月以上。"
                "④ 肝・腎機能を月1回モニタ。" + base_warning
            ),
        }
    if species == "ferret":
        return {
            "treatment_ja": (
                "フェレットマイコバクテリウム感染症: M. avium complex、稀にM. tuberculosis、M. bovis。"
                "① 治療は試験的: リファンピシン 10-15 mg/kg PO q24h + クラリスロマイシン 15-20 mg/kg PO q12h + "
                "エンロフロキサシン 5-10 mg/kg PO q24h、6-12ヶ月。"
                "② M. tuberculosis complex確定は安楽死推奨（人獣共通リスク優先）。"
                "③ 体重・CBC・肝酵素を月1回モニタ。" + base_warning + _supportive_block(species)
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                "鳥類マイコバクテリウム症（鳥結核, M. avium）: 治療困難で再発が多い。"
                "① 治療プロトコル: アジスロマイシン 40-50 mg/kg PO q24h + リファンピシン 45 mg/kg PO q24h + "
                "エチオブトール 30 mg/kg PO q24h、最低6ヶ月（多くは12ヶ月以上）。"
                "② 飼養禁止：陽性個体は他鳥への感染源となるため隔離・治療または安楽死を検討。"
                "③ 環境消毒は3%ホルムアルデヒドまたはエタノール70%（芽胞耐性高い）。"
                "④ ⚠免疫不全者（HIV+、化学療法中）はM. avium感染リスク—家族曝露を確認。" + _avian_supportive(species)
            ),
            "prognosis_ja": "予後不良。長期治療でも再発率高く、群への感染拡大リスクから安楽死を検討する。",
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}マイコバクテリウム症（M. marinum, M. chelonae, M. fortuitum等の非結核性抗酸菌が多い）: "
                "① 治療は試験的で長期: リファンピシン 10-30 mg/kg PO q24h + クラリスロマイシン 30 mg/kg PO q24h + "
                "エンロフロキサシン 5-10 mg/kg PO q24h、6-12ヶ月以上。"
                "② 皮下・皮膚結節は外科的切除を推奨（抗菌薬の浸透性が悪い）。"
                "③ POTZ最適化（免疫機能の前提）。"
                "④ ⚠ M. marinum はヒト皮膚感染（fish tank granuloma）—飼養者の手洗い・防護必須。"
                + _reptile_supportive(species)
            ),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}マイコバクテリウム症: 主にM. avium complex（免疫不全個体で発症）。"
                "① 治療プロトコル: リファンピシン 10-20 mg/kg PO q24h + クラリスロマイシン 15-25 mg/kg PO q12h + "
                "エンロフロキサシン 5-10 mg/kg PO q24h、6-12ヶ月。"
                "② 多くの症例で完全治癒困難。重症例・人獣共通リスクは安楽死を検討。"
                "③ 月1回のCBC・肝酵素モニタ。" + base_warning + _small_mammal_supportive(species)
            ),
        }
    return None


# ============================================================================
# Vestibular disease — central vs peripheral, species-specific etiology
# ============================================================================


def gen_vestibular(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}前庭疾患: 末梢性（内耳・中耳由来、約85%）vs 中枢性（脳幹）の鑑別が治療方針を決定。"
                "① 神経学的検査: 末梢性=水平/回旋性眼振・同側Horner症候群・正常意識；"
                "中枢性=垂直/方向変換性眼振・固有受容覚欠損・意識変容→MRI/CT必須。"
                "② 末梢性の対症療法: メクリジン 12.5-25 mg/"
                + ("cat" if species == "cat" else "dog")
                + " PO q24h（鎮静・抗悪心）、"
                "マロピタント 1 mg/kg SC/PO q24h（嘔気強い時）、輸液 60 mL/kg/日 IV/SC。"
                "③ 原疾患治療: 細菌性中耳炎/内耳炎→培養に基づく抗菌薬3-6週（エンロフロキサシン 5-10 mg/kg PO q24h、"
                "アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h）、必要なら鼓室切開・bulla osteotomy。"
                "④ "
                + (
                    "特発性老齢性前庭疾患（idiopathic geriatric vestibular disease）"
                    if species == "dog"
                    else "特発性前庭症候群"
                )
                + "は通常3-7日で自然軽快、2-4週で頭部傾斜以外消失。"
                "⑤ 中枢性: ステロイド（プレドニゾロン 0.5-1 mg/kg PO q12h漸減）、抗てんかん薬、原因（腫瘍・梗塞・MUO）治療。"
                "⑥ 安全管理: 転倒予防、寝具を厚く、誤嚥防止のため食事は柔らかいフード・少量頻回。"
            ),
        }
    if species == "rabbit":
        return {
            "treatment_ja": (
                "ウサギ前庭疾患（斜頸、head tilt）: 主因はE. cuniculi（脳炎）とPasteurella内耳炎—培養・血清学で鑑別。"
                "① E. cuniculi疑い: ファンベンダゾール 20 mg/kg PO q24h × 28-90日、"
                "ステロイドは議論あり（短期 デキサメサゾン 0.2 mg/kg q24h × 3日）。"
                "② Pasteurella内耳炎: エンロフロキサシン 10-15 mg/kg PO q12-24h × 4-6週、"
                "重症例は鼓室洗浄・bulla osteotomy。"
                "③ 支持: メロキシカム 0.5-1 mg/kg PO q12-24h、輸液 80-100 mL/kg/日 SC、"
                "シリンジ給餌（Critical Care 50 mL/kg/日 q4-6h分割）、転倒・自傷防止のためパッド入りケージ。"
                "④ メクリジン 2-12 mg/kg PO q8-24h で前庭症状緩和。"
                "⑤ 予後: 早期治療で多くは改善、頭部傾斜は完全消失せず残ることが多い（QOL良好なら経過観察）。"
                "⚠経口β-ラクタムは禁忌（致死的腸内菌叢崩壊）。"
            ),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}前庭疾患: 鑑別—中耳炎/内耳炎、脳炎、外傷、腫瘍、特発性。"
                "① 診断: 神経学的検査、耳鏡、X線/CT（耳道・bulla）、CBC・血清化学・血液培養。"
                "② 細菌性中耳炎/内耳炎: 培養感受性に基づく全身抗菌薬3-6週（エンロフロキサシン 5-15 mg/kg PO q12-24h）、"
                "重症例は鼓室洗浄。"
                "③ 対症療法: メクリジン 2-12 mg/kg PO q8-24h、メロキシカム 0.5-1 mg/kg PO q12-24h、輸液 80 mL/kg/日 SC。"
                "④ 自傷・転倒防止のためパッド入りケージ、シリンジ給餌で栄養維持。"
                "⑤ 重症・進行性は脳腫瘍・脳症の鑑別にMRI/CT。" + _small_mammal_supportive(species)
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}前庭症候群: 中耳・内耳炎、脳炎、栄養性（ビタミンE/セレン欠乏）、外傷、毒物（鉛/亜鉛中毒）を鑑別。"
                "① 全血鉛/亜鉛濃度、X線（重金属影）、CBC・生化学・PCR（PMV、ボルナ等）。"
                "② 重金属中毒疑い: Ca-EDTA 35 mg/kg IM q12h × 5日 + 排泄促進（消化管洗浄）。"
                "③ 細菌性内耳炎: エンロフロキサシン 10-15 mg/kg PO/IM q12h × 4-6週、"
                "セフタジジム 20-30 mg/kg IM q8h（重症）。"
                "④ ビタミンE/セレン欠乏: ビタミンE 1 IU/30 g 体重 PO q24h、Se 0.05 mg/kg IM single dose。"
                "⑤ 支持: 保温、皮下輸液 50 mL/kg/日、強制給餌、自傷防止。" + _avian_supportive(species)
            ),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}前庭疾患: 中耳炎、脳炎（細菌・寄生虫）、外傷、栄養性（ビタミンB欠乏）、毒物を鑑別。"
                "① POTZ最適化（免疫機能基盤）、診断（CBC・生化学・X線・必要に応じMRI）。"
                "② 細菌性: 培養感受性、セフタジジム 20 mg/kg IM q72h、エンロフロキサシン 5-10 mg/kg PO/IM q24-48h × 4-6週。"
                "③ 寄生虫疑い: フェンベンダゾール 50 mg/kg PO q24h × 5日。"
                "④ ビタミンB1欠乏（魚食種）: チアミン 25-100 mg/kg PO/IM q24h × 7日。"
                "⑤ 支持: 輸液 25-30 mL/kg SC/ICe、強制給餌、自傷防止のため低位置の隠れ家。"
                + _reptile_supportive(species)
            ),
        }
    return None


# ============================================================================
# Encephalitis — etiology-specific (infectious vs immune vs toxic)
# ============================================================================


def gen_encephalitis(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    base = (
        "① 緊急処置: 痙攣→ジアゼパム 0.5-1.0 mg/kg IV/IN/直腸、重積はミダゾラム CRI 0.1-0.5 mg/kg/h、"
        "脳浮腫→マンニトール 0.5-1.0 g/kg IV over 20 min（10%以上希釈、心機能注意）。"
        "② 原因検索: 神経学的検査、MRI、CSF分析（細胞数・蛋白・培養・PCR）、血液PCR/血清学（病原体特異）。"
    )
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}脳炎の治療: 原因別治療＋脳浮腫管理が予後を分ける。"
                + base
                + "③ 感染性: 細菌→第3世代セフェム（セフトリアキソン 25 mg/kg IV q24h）+ メトロニダゾール 10 mg/kg IV q12h、"
                "ウイルス（ジステンパー等）→対症療法、原虫（トキソプラズマ・ネオスポラ）→クリンダマイシン "
                "10-25 mg/kg PO q8-12h × 4-8週、真菌（クリプトコッカス等）→フルコナゾール 5-10 mg/kg PO q12-24h、"
                "リケッチア（Ehrlichia等）→ドキシサイクリン 5-10 mg/kg PO q12h × 4週。"
                "④ 免疫介在性（MUO/GME/NME）: 高用量プレドニゾロン 2-4 mg/kg PO q24h で開始、"
                "シタラビン 50 mg/m² SC q12h × 2日 q3週 または シクロスポリン 5-7 mg/kg PO q12h を併用。"
                "⑤ 抗てんかん薬: フェノバルビタール 2-4 mg/kg PO q12h、レベチラセタム 20-30 mg/kg PO q8h。"
                "⑥ モニタ: 神経症状進行、CBC（骨髄抑制）、血中フェノバル濃度、肝酵素。"
                "ACVIM Consensus (2020) on MUO参照。"
            ),
        }
    if species == "rabbit":
        return {
            "treatment_ja": (
                "ウサギ脳炎: 最多原因はE. cuniculi（30-80%の保有率）、次いでPasteurella、外傷。"
                + base
                + "③ E. cuniculi: ファンベンダゾール 20 mg/kg PO q24h × 28日（重症は90日）、"
                "デキサメサゾン 0.2 mg/kg q24h × 3日（炎症抑制、長期は禁忌）。"
                "④ 細菌性: エンロフロキサシン 10-15 mg/kg PO/SC q12-24h × 4週以上、"
                "脳脊髄液移行性のため高用量推奨。"
                "⑤ 支持: メロキシカム 0.5-1 mg/kg PO q12-24h、シリンジ給餌（Critical Care）、輸液 80 mL/kg/日 SC、"
                "GI stasis予防にメトクロプラミド 0.5 mg/kg SC q8h。"
                "⚠ペニシリン系・セファロスポリン系の経口投与は禁忌。"
            ),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}脳炎: 細菌（Listeria、Streptococcus、Pasteurella）、ウイルス（LCMV、SDA virus、PHV）、"
                "寄生虫（Baylisascaris—齧歯類）、外傷、栄養性（ビタミンB1欠乏）を鑑別。"
                + base
                + "③ 細菌性: トリメトプリム・スルファ 15-30 mg/kg PO q12h、"
                "エンロフロキサシン 5-15 mg/kg PO/SC q12-24h × 4週、ChloramphenicolPalmitate 50 mg/kg PO q8h（CNS移行良好）。"
                "④ Baylisascaris疑い: アルベンダゾール 25-50 mg/kg PO q24h × 30日 + ステロイド（炎症抑制）。"
                "⑤ ビタミンB1欠乏: チアミン 25-50 mg/kg IM q24h × 7日。"
                "⑥ 支持療法重視—栄養・水分・体温管理。" + _small_mammal_supportive(species)
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}脳炎: 主因—ボルナウイルス（PDD）、PMV、West Nile、サルモネラ、クラミジア、重金属中毒（鉛/亜鉛）、"
                "Sarcocystis、Aspergillus髄膜脳炎。" + base + "③ 重金属中毒: Ca-EDTA 35 mg/kg IM q12h × 5日。"
                "④ 細菌性: エンロフロキサシン 10-15 mg/kg PO/IM q12h × 4-6週、ドキシサイクリン 25-50 mg/kg PO q24h（クラミジア）。"
                "⑤ 真菌性: イトラコナゾール 5-10 mg/kg PO q24h、ボリコナゾール 12.5 mg/kg PO q12h × 6-12週、肝酵素モニタ。"
                "⑥ Sarcocystis: トリメトプリム・スルファ 30 mg/kg PO q12h + ピリメサミン 0.5 mg/kg PO q24h × 30-60日。"
                "⑦ PDD（ボルナ）: メロキシカム 0.5-1 mg/kg PO q24h（症状軽減のみ）、塩化セレストデロン経験的。"
                + _avian_supportive(species)
            ),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}脳炎: 細菌（敗血症的播種）、ウイルス（パラミクソ、アデノ、IBD/ARENAVIRUS in pythons）、"
                "寄生虫、栄養性（ビタミンB1欠乏—魚食種）、毒物（重金属、農薬）を鑑別。"
                + base
                + "③ 細菌性: セフタジジム 20 mg/kg IM q72h、エンロフロキサシン 5-10 mg/kg PO/IM q24-48h × 4-6週、"
                "クロラムフェニコール 30-50 mg/kg PO q12h（CNS移行良好）。"
                "④ ビタミンB1欠乏: チアミン 25-50 mg/kg PO/IM q24h × 7日（特にgartersnakeの魚食種）。"
                "⑤ POTZ最適化が免疫機能回復の前提。"
                "⑥ IBD/Arenavirus: 確立した治療なし、隔離・支持療法・他蛇への感染予防。" + _reptile_supportive(species)
            ),
        }
    return None


# ============================================================================
# Peripheral neuropathy — etiology-specific
# ============================================================================


def gen_peripheral_neuropathy(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    return {
        "treatment_ja": (
            f"{species_ja}末梢神経障害: 代謝性（糖尿病、ビタミンB欠乏）、中毒性（鉛、有機リン、薬物）、外傷性、"
            "免疫介在性、腫瘍性、感染性、遺伝性などを鑑別。"
            "① 検査: CBC・生化学・血糖・甲状腺・ビタミンB12 と葉酸、重金属、X線/CT、必要に応じ筋電図・神経生検。"
            "② 代謝性: 原疾患治療（糖尿病コントロール、ビタミンB群高用量補充—ビタミンB1 25 mg/kg、B6 25 mg/kg、B12 50 µg/kg "
            "PO q24h × 6-8週）。"
            "③ 中毒性: 暴露源除去、対症療法、重金属はキレート療法（鉛—Ca-EDTA、ペニシラミン 8-15 mg/kg PO q8h）。"
            "④ 免疫介在性（多発性神経根炎、polyradiculoneuritis）: プレドニゾロン 1-2 mg/kg PO q12h × 4-6週漸減、"
            "重症はIVIg 0.5-1 g/kg IV、シクロスポリン 5-7 mg/kg PO q12h。"
            "⑤ 鎮痛: ガバペンチン 10-20 mg/kg PO q8-12h、プレガバリン 2-4 mg/kg PO q12h、トラマドール 2-5 mg/kg PO q8-12h。"
            "⑥ リハビリ: 受動的可動域訓練、水中歩行、神経筋電気刺激で機能回復促進。"
            "⑦ 環境調整: 滑り止めマット、低段差、自傷防止のために爪研磨など。" + _supportive_block(species)
        ),
    }


# ============================================================================
# Flagellate protozoan infections (Trichomonas, Hexamita, Spironucleus, Giardia)
# ============================================================================


def gen_flagellate(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}鞭毛原虫感染症（Trichomonas gallinae=トリコモナス症/canker、Giardia、Histomonas）: "
                "① 第一選択: メトロニダゾール 30-50 mg/kg PO q24h × 5-7日、または "
                "カルニダゾール 25 mg/kg PO single dose（薬剤耐性株あり）、"
                "ロニダゾール 10 mg/kg PO q24h × 5-7日（鳩で証拠多い）。"
                "② Histomonas: メトロニダゾール 30 mg/kg PO q24h × 7日。"
                "③ 口腔・咽喉の偽膜病変は除去（出血リスクあり、慎重に）、ぬるま湯洗浄。"
                "④ 群管理: 水入れの毎日洗浄、新規個体検疫、感染鳥の隔離（伝染力高）。"
                "⑤ 雛への直接給餌経路で母→雛感染が起きる—繁殖鳥のスクリーニング。" + _avian_supportive(species)
            ),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}鞭毛原虫感染症（Hexamita、Spironucleus、Trichomonas、Giardia）: "
                "① 第一選択: メトロニダゾール 20-25 mg/kg PO q24h × 5-7日（爬虫類） / 50 mg/kg PO q24h × 3-5日（陸亀）、"
                "リクガメではメトロニダゾールに感受性差あり。"
                "② 試験的代替: パロモマイシン 100 mg/kg PO q24h × 7日（メトロニダゾール耐性疑い）。"
                "③ Giardia: フェンベンダゾール 50 mg/kg PO q24h × 5日 + メトロニダゾール併用。"
                "④ POTZ最適化と環境消毒（次亜塩素酸1:32、紫外線）。"
                "⑤ ⚠群飼育・水浴び容器が感染源—頻繁な交換と消毒。" + _reptile_supportive(species)
            ),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}鞭毛原虫感染症（Giardia、Tritrichomonas、Spironucleus）: "
                "① 第一選択: メトロニダゾール 15-25 mg/kg PO q12h × 5-7日（神経毒性注意）、"
                "フェンベンダゾール 20-50 mg/kg PO q24h × 5日（Giardiaに有効）。"
                "② 環境消毒: 次亜塩素酸1:32、給水器・床面毎日洗浄。"
                "③ ⚠人獣共通感染症（Giardia）—家族の手洗い徹底。"
                "④ プロバイオティクスで腸内細菌叢回復。" + _small_mammal_supportive(species)
            ),
        }
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}鞭毛原虫感染症（Giardia、Tritrichomonas）: "
                "① Giardia: フェンベンダゾール 50 mg/kg PO q24h × 3-5日（再発時5日）、"
                "メトロニダゾール 15-25 mg/kg PO q12h × 5-7日、または併用。"
                "② Tritrichomonas（猫慢性下痢の重要原因）: ロニダゾール 30 mg/kg PO q24h × 14日（保険適用外、薬剤師調剤）。"
                "③ 沐浴で被毛のシスト除去、家族の手洗い徹底（人獣共通）。"
                "④ 環境消毒は塩素系（漂白剤1:32）、紫外線照射。"
                "⑤ 多頭飼育では全頭スクリーニング・治療を推奨。"
            ),
        }
    return None


# ============================================================================
# Hepatic disease (replaces 「肝疾患管理」 generic template) — type-specific
# ============================================================================


def gen_hepatic_disease(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    nm = name_ja or ""
    # Detect subtype from name
    is_bacterial = "細菌" in nm
    is_parasitic = "寄生虫" in nm
    is_fibrosis = "線維症" in nm
    is_lipidosis = "リピドーシス" in nm or "脂肪" in nm
    is_viral = "ウイルス" in nm
    common = (
        "① 検査: CBC・生化学（ALT/AST/ALP/GGT/T-Bil/Alb）、胆汁酸負荷試験、凝固系（PT/aPTT）、超音波、"
        "肝生検（細胞診/組織学/培養）。"
    )
    if is_bacterial:
        return {
            "treatment_ja": (
                f"{species_ja}肝細菌感染症（細菌性肝炎・胆管炎）: "
                + common
                + "② 培養感受性に基づく抗菌薬（経験的）: アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h "
                "（草食種は経口β-ラクタム禁忌のため除外）、エンロフロキサシン 5-15 mg/kg PO/IM q12-24h、"
                "メトロニダゾール 10-25 mg/kg PO q12h（嫌気性カバー）、最低4-6週投与。"
                "③ 肝庇護療法: ウルソデオキシコール酸 10-15 mg/kg PO q24h、SAMe 20 mg/kg PO q24h（空腹時）、"
                "シリマリン 4-15 mg/kg PO q24h、ビタミンE 10-15 IU/kg PO q24h。"
                "④ 支持: 輸液、栄養（肝不全用処方食、Hill's l/d）、ビタミンK1 補充（凝固障害時）。"
                "⑤ 重症・胆嚢炎合併は外科的胆嚢摘出。" + _supportive_block(species)
            ),
        }
    if is_parasitic:
        return {
            "treatment_ja": (
                f"{species_ja}肝寄生虫疾患: " + common + "② 寄生虫種特定（糞便検査、PCR、生検）後の駆虫: "
                "肝吸虫（Fasciola, Opisthorchis）→トリクラベンダゾール 10 mg/kg PO single または プラジカンテル 40 mg/kg PO q12h × 3日、"
                "線虫（Capillaria hepatica）→フェンベンダゾール 50 mg/kg PO q24h × 5日、"
                "原虫→種特異的（Leishmania→アンホテリシンB、Toxoplasma→クリンダマイシン）。"
                "③ 肝庇護: UDCA 10-15 mg/kg PO q24h、SAMe 20 mg/kg PO q24h、シリマリン。"
                "④ 環境管理: 中間宿主（巻貝、節足動物）の駆除、生餌・汚染水の回避。" + _supportive_block(species)
            ),
        }
    if is_fibrosis:
        return {
            "treatment_ja": (
                f"{species_ja}肝線維症: 進行性で根治困難—早期発見と原因除去、線維化進展抑制が中心。"
                + common
                + "② 原因治療: 慢性炎症（自己免疫→免疫抑制）、寄生虫→駆虫、毒物→暴露除去、銅蓄積→キレート（ペニシラミン）、"
                "薬剤性→中止。"
                "③ 抗線維化: ウルソデオキシコール酸 10-15 mg/kg PO q24h、SAMe 20 mg/kg PO q24h、"
                "シリマリン 4-15 mg/kg PO q24h、ビタミンE 10-15 IU/kg PO q24h。"
                "④ 門脈圧亢進管理: 利尿剤（スピロノラクトン 1-2 mg/kg PO q12h）、低塩食、腹水時はパラセンテシス。"
                "⑤ 肝性脳症: ラクツロース 0.5-1 mL/kg PO q8h（軟便目標）、低蛋白食、メトロニダゾール 7.5 mg/kg PO q12h。"
                "⑥ 凝固障害: ビタミンK1 1 mg/kg SC q12h × 3日。" + _supportive_block(species)
            ),
            "prognosis_ja": "代償性ではQOL維持可能。非代償性（腹水・肝性脳症・出血）は予後不良（6ヶ月以内死亡多い）。",
        }
    if is_lipidosis and species == "cat":
        return {
            "treatment_ja": (
                "猫肝リピドーシス（idiopathic hepatic lipidosis）: 猫の最も重要な肝疾患、致死率高い。"
                "① 早期・積極的経腸栄養が予後を決定—鼻食道チューブ、PEGチューブ、esophagostomyチューブで強制栄養。"
                "② 栄養目標: 高蛋白（30-40%）・高エネルギー処方食（Hill's a/d, Royal Canin Recovery）、"
                "1日RER（70 × BW^0.75 kcal）を4-6回分割、徐々に増量（リフィーディング症候群予防）。"
                "③ 制吐: マロピタント 1 mg/kg SC q24h、オンダンセトロン 0.5 mg/kg IV q8-12h。"
                "④ 食欲増進: ミルタザピン 1.88 mg/cat PO q48h、カプロモレリン 3 mg/kg PO q24h。"
                "⑤ 肝庇護: SAMe 20 mg/kg PO q24h、L-カルニチン 250 mg/cat PO q24h、ビタミンE 10 IU/kg PO q24h、"
                "ビタミンB12（コバラミン）250 µg/cat SC weekly × 6週。"
                "⑥ 凝固障害: ビタミンK1 0.5-1 mg/kg SC q12h × 3日（チューブ留置前必須）。"
                "⑦ 基礎疾患検索（膵炎、IBD、糖尿病、感染症）と並行治療。"
                "ISFM/AAFP Hepatic Lipidosis Consensus 2014参照。"
            ),
            "prognosis_ja": (
                "適切な栄養管理で生存率80-90%。診断遅れ・基礎疾患併発・低Albで予後悪化。"
                "完全回復には6-8週要し、その間チューブ栄養継続。"
            ),
        }
    if is_viral:
        return {
            "treatment_ja": (
                f"{species_ja}ウイルス性肝炎: 特異的抗ウイルス薬は限定的—支持療法と二次感染管理が中心。"
                + common
                + "② 支持療法: 輸液（晶質液 60-80 mL/kg/日 IV、肝不全時はラクテートを避けNoramosol-Rを選択）、"
                "栄養（高品質低蛋白食、肝性脳症時はさらに蛋白制限）。"
                "③ 肝庇護: ウルソデオキシコール酸 10-15 mg/kg PO q24h、SAMe 20 mg/kg PO q24h、シリマリン、ビタミンE。"
                "④ 二次性細菌感染予防: アンピシリン 22 mg/kg IV q8h、メトロニダゾール 10 mg/kg PO q12h（肝性脳症兼）。"
                "⑤ 凝固障害: ビタミンK1 1 mg/kg SC q12h、新鮮凍結血漿 6-10 mL/kg IV（出血時）。"
                "⑥ 肝性脳症: ラクツロース 0.5-1 mL/kg PO q8h（軟便目標）、低蛋白食。"
                "⑦ ワクチン（CAV-1犬伝染性肝炎等）が予防の主体。"
            ),
        }
    # generic hepatitis
    return {
        "treatment_ja": (
            f"{species_ja}{nm}: 原因（感染性・中毒・免疫介在性・腫瘍・代謝）特定が治療方針を決定。"
            + common
            + "② 原因別治療: 細菌→培養に基づく抗菌薬4-6週、寄生虫→駆虫、ウイルス→支持療法、"
            "免疫介在性→プレドニゾロン 1-2 mg/kg PO q12h漸減、薬剤性→暴露除去。"
            "③ 肝庇護: ウルソデオキシコール酸 10-15 mg/kg PO q24h、SAMe 20 mg/kg PO q24h（空腹時）、"
            "シリマリン 4-15 mg/kg PO q24h、ビタミンE 10-15 IU/kg PO q24h。"
            "④ 栄養: 高品質中等量蛋白、十分なカロリー（脂肪は耐容性で調整）、ビタミンK1補充。"
            "⑤ モニタ: 肝酵素 q2-4週、Alb・凝固系、必要なら肝生検でstaging。" + _supportive_block(species)
        ),
    }


# ============================================================================
# Dermatitis / skin disease — etiology-specific
# ============================================================================


def gen_dermatitis(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    nm = name_ja or ""
    is_alopecia = "脱毛" in nm
    is_abscess = "膿瘍" in nm
    is_pododermatitis = "足底" in nm or "バンブル" in nm or "Pododermatitis" in nm
    is_allergic = "アレルギ" in nm
    is_contact = "接触" in nm
    is_bacterial = "細菌" in nm
    is_parasitic = "寄生虫" in nm or "ダニ" in nm
    is_autoimmune = "自己免疫" in nm
    is_chronic = "慢性" in nm
    is_ulcer = "潰瘍" in nm

    if is_alopecia:
        return {
            "treatment_ja": (
                f"{species_ja}脱毛症の鑑別と治療: ① 原因鑑別—内分泌（甲状腺・副腎・性ホルモン）、"
                "感染性（細菌・真菌・寄生虫）、行動性（barbering、自傷）、アレルギー、栄養性、遺伝性、瘢痕性。"
                "② 検査: 被毛抜去試験、テープ採取、皮膚生検、皮膚培養（細菌・真菌）、内分泌（T4・コルチゾール）、CBC・生化学。"
                "③ 内分泌性: 原疾患治療（甲状腺機能低下→レボチロキシン、副腎皮質機能亢進→トリロスタン）。"
                "④ 真菌性（皮膚糸状菌）: イトラコナゾール 5-10 mg/kg PO q24h × 4-6週 + 局所2%ミコナゾール。"
                "⑤ 寄生虫: イベルメクチン 0.2-0.4 mg/kg SC q14d × 2-3回（チンチラ・ウサギ・Collie系は禁忌or慎重）、"
                "セラメクチン外用、フィプロニル（フェレット以外の小型哺乳類で慎重、チンチラ禁忌）。"
                "⑥ 行動性barbering: ストレス源同定（過密、騒音、退屈）、環境enrichment、必要時はベンゾジアゼピン。"
                "⑦ 栄養性: ω3/ω6脂肪酸補充、十分な蛋白質。" + _supportive_block(species)
            ),
        }
    if is_abscess:
        return {
            "treatment_ja": (
                f"{species_ja}皮膚膿瘍: ① 外科的処置が治療の根幹—切開・排膿・徹底的洗浄が抗菌薬単独より治癒率高い。"
                "② 麻酔下で十分な切開、内容物を除去し生理食塩水または0.05%クロルヘキシジンで洗浄、必要に応じドレーン留置。"
                "③ 培養感受性試験（深部組織から採取）後の全身抗菌薬: "
                "アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h（草食種除く）、"
                "セファレキシン 22 mg/kg PO q12h、エンロフロキサシン 5-15 mg/kg PO/IM q12-24h × 7-14日（再発時は4週）。"
                "④ 慢性・再発例ではマルセイン化（膿瘍嚢全摘）と組織培養を再評価—バイオフィルム形成菌を疑う。"
                "⑤ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO q24h、必要ならブプレノルフィン 0.01-0.05 mg/kg SC q8h。"
                "⑥ ⚠草食種（特にウサギ）の膿瘍は乾酪性（液体ではない）—完全摘出が再発予防に必須。"
                + _supportive_block(species)
            ),
        }
    if is_pododermatitis:
        return {
            "treatment_ja": (
                f"{species_ja}足底皮膚炎（バンブルフット/Pododermatitis）: 環境改善が治療の根幹。"
                "① 環境改善: 床材を柔らかいもの（タオル、Vetbed、人工芝）に変更、湿潤回避、止まり木の太さ・形状を見直す（鳥）。"
                "② 局所処置: ぬるま湯と0.05%クロルヘキシジン洗浄 q12h、外用シルバースルファジアジン or "
                "Manuka honey、患部包帯（鳥はballブートやテープシューズ）。"
                "③ 重症例（潰瘍・骨髄炎）: 培養感受性後の全身抗菌薬—エンロフロキサシン 10-15 mg/kg PO/IM q12-24h、"
                "アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h（鳥含む）、4-8週継続。"
                "④ 外科的デブリードマン（壊死組織除去）必要例あり。"
                "⑤ 鎮痛: メロキシカム "
                + ("0.5-1 mg/kg PO q12-24h" if species in SMALL_MAMMAL else "0.2-0.5 mg/kg PO q24h")
                + "。"
                "⑥ 肥満は最大のリスク因子—体重管理（特に飛ばない大型鳥、ウサギ、モルモット）。"
                "⑦ ビタミンA欠乏（鳥）も誘因—食事改善（種子食偏重を脱却）。" + _supportive_block(species)
            ),
        }
    if is_allergic or is_contact:
        cls = "接触性皮膚炎" if is_contact else "アレルギー性皮膚疾患"
        return {
            "treatment_ja": (
                f"{species_ja}{cls}: ① 原因物質の同定と除去が最重要—床材（杉材は禁忌、紙系/ペレット系へ）、"
                "ケージ素材（金属アレルギー）、食事、消毒剤、香料、装飾品。"
                "② 局所: 患部洗浄（ぬるま湯）、低刺激エメリエント、抗菌作用のあるシャンプー（クロルヘキシジン2%）q3-7日。"
                "③ 全身: 短期プレドニゾロン 0.5-1 mg/kg PO q24h × 5-7日で漸減（小型哺乳類はステロイド慎重）、"
                "セチリジン 5-10 mg/animal PO q12-24h、ジフェンヒドラミン 2-4 mg/kg PO q8h。"
                "④ 食物アレルギー疑い: 8週hydrolyzed protein食試験。"
                "⑤ アトピー性（犬）: シクロスポリン 5-7 mg/kg PO q24h、オクラシチニブ（Apoquel）0.4-0.6 mg/kg PO q12h × 14d→q24h。"
                "⑥ 二次性細菌感染: 培養感受性で抗菌薬。"
                "⑦ 自傷予防: エリザベスカラーまたは患部保護衣。" + _supportive_block(species)
            ),
        }
    if is_bacterial:
        return {
            "treatment_ja": (
                f"{species_ja}皮膚細菌感染: ① 培養感受性試験が治療の出発点—MRSP/MRSAスクリーニング推奨。"
                "② 局所（軽症）: クロルヘキシジン 2-4% シャンプー q3-7日、ムピロシン軟膏 q12h、"
                "ベンゾイル過酸化物（脂漏性に有効）。"
                "③ 全身（中等症-重症）: アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h（草食種除く）、"
                "セファレキシン 22-30 mg/kg PO q12h、クリンダマイシン 5-10 mg/kg PO q12h、"
                "エンロフロキサシン 5-15 mg/kg PO/SC q12-24h、最低3-4週（深在性は6-8週）。"
                "④ MRSP/MRSA: ドキシサイクリン 5-10 mg/kg PO q12h、クロラムフェニコール 50 mg/kg PO q8h（家族曝露注意）、"
                "アミカシン 15 mg/kg IM q24h（TDM）。"
                "⑤ 基礎疾患検索（アレルギー、内分泌、免疫不全）と並行治療が再発予防の鍵。" + _supportive_block(species)
            ),
        }
    if is_parasitic:
        return {
            "treatment_ja": (
                f"{species_ja}皮膚寄生虫症: ① 検体採取—スクラッピング（深部・浅部）、テープ採取、被毛抜去、皮膚生検。"
                "② Sarcoptes/Notoedres（疥癬）: イベルメクチン 0.2-0.4 mg/kg SC q14d × 2-3回（チンチラ・ウサギ慎重）、"
                "セラメクチン 6-12 mg/kg 外用 q14d × 3回、モキシデクチン経皮（一部種）。"
                "③ Demodex（毛包虫）: イソキサゾリン系（フルララネル、サロラネル、ロチラネル、アフォキソラネル）— "
                "犬猫で最も推奨、Brevicaul/canis/injai。"
                "④ Cheyletiella、Trombicula: 上記同様の駆虫＋環境消毒。"
                "⑤ シラミ（咬虫・吸虫）: フィプロニル外用（フェレット可、チンチラ禁忌）、イミダクロプリド。"
                "⑥ 二次性細菌・真菌感染の併発—培養後の抗菌薬・抗真菌薬。"
                "⑦ 環境: 寝具洗浄（60℃以上）、ケージ消毒、同居動物の同時治療。"
                "⑧ ⚠人獣共通感染症—家族の皮膚症状確認。" + _supportive_block(species)
            ),
        }
    if is_autoimmune:
        return {
            "treatment_ja": (
                f"{species_ja}皮膚自己免疫疾患（天疱瘡、紅斑性ループス、薬剤性等）: "
                "① 確定診断—皮膚生検（直接免疫蛍光、組織病理）、ANA、CBC・生化学・尿検査でSLE除外。"
                "② 免疫抑制療法（多くは長期）: プレドニゾロン 2-4 mg/kg PO q12h で開始、寛解後漸減 q4-8週、"
                "難治例にアザチオプリン 1-2 mg/kg PO q24-48h（猫は禁忌）、シクロスポリン 5-7 mg/kg PO q12h、"
                "マイコフェノール酸 10-15 mg/kg PO q12h。"
                "③ 局所: タクロリムス 0.1% 外用 q12h、トリアムシノロン点鼻/点眼。"
                "④ 二次性感染管理（免疫抑制中）: 培養感受性で抗菌薬、抗真菌薬。"
                "⑤ モニタ: CBC q2週（骨髄抑制）、肝酵素、血糖、感染症スクリーニング、QOL評価。"
                "⑥ 紫外線回避（紅斑性ループス）、ストレス軽減（再燃因子）。" + _supportive_block(species)
            ),
        }
    if is_ulcer:
        return {
            "treatment_ja": (
                f"{species_ja}潰瘍性皮膚炎: ① 原因鑑別—感染性、自己免疫、薬剤性、外傷、血管炎、悪性。"
                "② 検査: 培養感受性、生検（組織病理・直接免疫蛍光）、CBC・生化学。"
                "③ 局所処置: 壊死組織のデブリードマン、生食 or 0.05%クロルヘキシジン洗浄 q12h、"
                "湿潤治療材（hydrocolloid、hydrogel）、Manuka honey、抗菌軟膏（ムピロシン、シルバースルファジアジン）。"
                "④ 全身抗菌薬（深在感染時）: 培養感受性で選択、4-6週継続。"
                "⑤ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO q24h、必要ならガバペンチン 10-20 mg/kg PO q8-12h。"
                "⑥ 自傷防止: エリザベスカラー、ジャケット、低照度環境。"
                "⑦ 基礎疾患治療（糖尿病、副腎機能亢進、栄養不良）が並行重要。" + _supportive_block(species)
            ),
        }
    if is_chronic:
        return {
            "treatment_ja": (
                f"{species_ja}慢性皮膚炎: ① 慢性化＝原因未解決—再診で原因を再評価（アレルギー、感染、内分泌、寄生虫、自己免疫、栄養）。"
                "② 系統的アプローチ: 食事除去試験（hydrolyzed 8週）、皮膚生検、内分泌スクリーニング、"
                "培養（細菌・真菌）、被毛検査、環境アレルギー検査。"
                "③ 維持療法: クロルヘキシジン 2% シャンプー q3-7日（持続）、ω3脂肪酸 30-50 mg/kg/日、"
                "ペット用保湿剤・エメリエント外用 q12-24h。"
                "④ 症状コントロール: シクロスポリン 5-7 mg/kg PO q24h（犬猫）、オクラシチニブ（犬専用、長期投与可）、"
                "セチリジン 5-10 mg/animal PO q12-24h。"
                "⑤ 二次性感染の繰り返しに対し、間欠的抗菌シャンプー・短期抗菌薬・抗真菌薬。"
                "⑥ 長期管理: 3-6ヶ月毎の再評価、QOL・治療コスト・家族の負担を考慮した個別計画。"
                + _supportive_block(species)
            ),
        }
    # generic dermatitis
    return {
        "treatment_ja": (
            f"{species_ja}{nm}: 原因（感染・アレルギー・寄生虫・自己免疫・内分泌）特定が治療方針を決定。"
            "① 検査: 培養（細菌・真菌）、皮膚生検、寄生虫検査、内分泌・CBC・生化学。"
            "② 局所: 患部洗浄（0.05%クロルヘキシジン q12h）、外用抗菌・抗真菌軟膏、保護包帯。"
            "③ 全身抗菌薬（感染時）: 培養感受性で選択—エンロフロキサシン 5-15 mg/kg PO/IM q12-24h、"
            "アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h（草食種除く）、最低3-4週。"
            "④ 抗炎症: 短期プレドニゾロン 0.5-1 mg/kg PO q24h × 5-7日（必要時）、ω3脂肪酸補充。"
            "⑤ 自傷防止のエリザベスカラー、環境整備（湿度・清潔）、栄養改善。" + _supportive_block(species)
        ),
    }


# ============================================================================
# Fracture / orthopedic trauma — bone-specific
# ============================================================================


def gen_fracture(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    nm = name_ja or ""
    nm_lower = nm.lower()
    # Anatomical region tag + procedure-specific notes for each subtype.
    bone = ""
    subtype_note = ""
    if "翼" in nm or "wing" in nm_lower:
        bone = "翼"
        subtype_note = "翼骨折はFigure-8包帯（前腕・橈尺骨）またはbody wrap（上腕）、後遺症として羽根損傷リスクあり。"
    elif "脚" in nm or "leg" in nm_lower or "肢" in nm or "limb" in nm_lower:
        bone = "四肢"
        subtype_note = "四肢骨折は副木またはTape splint、長管骨は外科固定検討、関節を跨ぐ場合は早期可動域訓練。"
    elif "嘴" in nm or "beak" in nm_lower:
        bone = "嘴"
    elif "脊椎" in nm or "spine" in nm_lower or "spinal" in nm_lower or "脊柱" in nm:
        bone = "脊椎"
        subtype_note = (
            "脊椎骨折は厳格な ケージ制限・脊柱安定化、神経学的評価（運動・感覚・尿便）必須、損傷高位の特定で予後判断。"
        )
    elif "骨盤" in nm or "pelvi" in nm_lower:
        bone = "骨盤"
        subtype_note = (
            "骨盤骨折は多くは保存的（4-6週ケージ制限）、変位高度・骨盤腔狭窄は外科整復、難産・排便障害リスクの評価。"
        )
    elif "指" in nm or "digit" in nm_lower or "趾" in nm or "phalan" in nm_lower:
        bone = "指/趾"
        subtype_note = "指/趾骨折は単純例は副木・テーピング、複雑骨折・癒合不全は趾切断も検討。"
    elif "歯" in nm or "tooth" in nm_lower or "dental" in nm_lower or "切歯" in nm:
        bone = "歯"
        subtype_note = (
            "歯の骨折は歯髄露出・感染リスクで早期評価—断端トリミング、根管治療、抜歯のいずれか。栄養管理（軟食）併用。"
        )
    elif "飛膜" in nm or "patagium" in nm_lower:
        bone = "飛膜"
        subtype_note = "飛膜（patagium）損傷は皮膚縫合+創傷管理、二次感染予防、滑走運動回復まで活動制限。"
    elif "頭" in nm or "skull" in nm_lower or "cranial" in nm_lower:
        bone = "頭蓋"
        subtype_note = (
            "頭蓋骨折は神経症状・脳挫傷の評価（MRI・CT）、脳浮腫管理（マンニトール 0.5-1 g/kg IV）、痙攣管理。"
        )
    elif "肋骨" in nm or "rib" in nm_lower:
        bone = "肋骨"
        subtype_note = "肋骨骨折は呼吸モニタリング、フレイルチェスト・血気胸の評価、十分な鎮痛で呼吸抑制注意。"
    elif "尾" in nm or "tail" in nm_lower:
        bone = "尾"
        subtype_note = "尾骨折は保存的（4-6週）、開放性・神経損傷例は尾切断検討、排便・排尿機能評価。"

    if species in AVIAN:
        if bone == "嘴":
            return {
                "treatment_ja": (
                    f"{species_ja}嘴骨折/外傷: ① 嘴は採食・グルーミングに必須—早急対応が栄養維持と予後を決める。"
                    "② 出血止血: 加圧、止血剤（フェリック硫酸）、必要なら焼烙。"
                    "③ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg IM q6-12h。"
                    "④ 抗菌薬（培養感受性後）: エンロフロキサシン 10-15 mg/kg PO/IM q12h × 7-14日、"
                    "アモキシシリン/クラブラン酸 125 mg/kg PO q12h。"
                    "⑤ 嘴修復: アクリル樹脂（dental composite）でcomposite repair、断端を整える。"
                    "重度損失例ではprosthetic beak作製（複雑、専門医紹介）。"
                    "⑥ 栄養支持: 強制給餌（Emeraid Omnivore 20-30 mL/kg q4-6h）、修復が安定するまで継続。"
                    "⑦ 再発予防: ケージ内の鋭利物除去、他鳥との分離、適切な咀嚼物（ミネラルブロック）提供。"
                    + _avian_supportive(species)
                ),
            }
        return {
            "treatment_ja": (
                f"{species_ja}{bone or '骨'}折: ① 鳥類骨は中空気骨で骨折治癒に約4-6週要—種・年齢・骨により差。"
                f"{subtype_note}"
                "② 安定化: 翼骨折はFigure-8包帯（前腕・橈尺骨）または body wrap（上腕）、"
                "脚骨折は副木またはTape splint、重度・多発骨折は外固定（KE法）。"
                "③ 外科的固定（複雑骨折）: IM pin、cerclage wire、external skeletal fixator—専門医推奨。"
                "④ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg IM q6-12h、"
                "局所麻酔（リドカイン 4 mg/kg max、適応症）。"
                "⑤ 抗菌薬（開放骨折・術後）: エンロフロキサシン 10-15 mg/kg PO/IM q12h × 7-14日。"
                "⑥ ケージ調整: 止まり木低位置 or 取り外し、床面パッド、強制給餌。"
                "⑦ 経過観察: X線2-3週毎、固定材は癒合確認後（通常4-6週）に除去。"
                "⑧ リハビリ: 段階的flight再訓練、関節可動域訓練。" + _avian_supportive(species)
            ),
        }
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}{bone or '骨'}折の治療: ① 緊急安定化—ABCDE評価、ショック対応、輸液 60-90 mL/kg/h IV ボーラス、"
                f"外傷部位の出血止血。{subtype_note}"
                "② 鎮痛: メサドン 0.1-0.3 mg/kg IM、ブプレノルフィン 0.02 mg/kg IM、安定後にメロキシカム "
                "0.1-0.2 mg/kg PO/SC q24h（猫は短期）、ガバペンチン 10-20 mg/kg PO q8h。"
                "③ 画像評価（X線2方向、複雑なら CT）で骨折型分類（横骨折・斜骨折・らせん骨折・粉砕骨折）と判断。"
                "④ 固定法: 単純安定骨折→外固定（ギプス、副木）、"
                "複雑/長管骨→外科的固定（プレート・スクリュー、IM pin、external skeletal fixator）—専門医推奨。"
                "⑤ 開放骨折: 緊急の創洗浄・デブリードマン、培養感受性後の抗菌薬（cefazolin 22 mg/kg IV q8h、6週）。"
                "⑥ リハビリ: 受動的可動域訓練、水中歩行、CRI鎮痛で早期離床促進。"
                "⑦ 経過: X線4-6週毎、癒合確認まで活動制限。"
            ),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}{bone or '骨'}折: ① 小型・骨脆弱性が外科的固定を難しくする—保存的治療（副木）が多い。"
                f"{subtype_note}"
                "② 安定化: 副木（Robert Jones、軽量副木）またはケージ制限、4-6週で癒合。"
                "③ 重症・長管骨は外科的固定（mini IM pin、外固定）—専門医推奨。"
                "④ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h。"
                "⑤ 開放骨折: 培養感受性後の抗菌薬（草食種は経口β-ラクタム禁忌、エンロフロキサシン 5-10 mg/kg PO q12-24h）。"
                "⑥ ケージ制限: ステップ・ハンモック撤去、床に柔らかいパッド、シリンジ給餌で活動を最小化。"
                "⑦ 経過: X線3-4週毎、若齢は癒合早い（2-4週）。" + _small_mammal_supportive(species)
            ),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}{bone or '骨'}折: ① 骨折の多くは栄養性二次性副甲状腺機能亢進症（NSHP）に関連—血清Ca/P・X線で骨密度評価。"
                f"{subtype_note}"
                "② NSHP合併時はCa・VitD3補充（カルシウム グルコネート 100 mg/kg PO q24h × 2週）と"
                "UVB照射 (UVI 2-7、種別)、食事改善が並行必須。"
                "③ 安定化: 単純骨折は副木、複雑は外科的固定（mini plate, KE）—外骨格・甲羅は特殊接着剤（epoxy）。"
                "④ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h、ブプレノルフィン 0.01-0.05 mg/kg IM q12-24h、"
                "モルヒネ（亀 0.4-1 mg/kg、ヘビ無効—種差大）。"
                "⑤ 抗菌薬（開放骨折）: セフタジジム 20 mg/kg IM q72h、エンロフロキサシン 5-10 mg/kg PO/IM q24-48h。"
                "⑥ POTZ最適化（治癒の前提）、湿度管理、強制給餌。"
                "⑦ 経過: X線4-8週毎、爬虫類は癒合が遅い（最大6-12ヶ月）。" + _reptile_supportive(species)
            ),
        }
    return None


# ============================================================================
# Neoplasia — species-tailored (Lipoma, Melanoma, Leukemia, Lymphoma)
# ============================================================================


def gen_lipoma(species: str, name_ja: str) -> Optional[dict]:
    """Lipoma — benign adipose tumor. Species-specific surgical risk + dietary context."""
    species_ja = _species_label_ja_local(species)
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}脂肪腫（xanthoma を含む）: ① 好発: バジェリガー・コザクラ等の高脂肪種子食給餌例、肥満個体—"
                "腹部・胸部・翼基部の柔軟皮下腫瘤。"
                "② 内科管理（小型・成長緩慢例）: L-カルニチン 1,000 mg/kg 餌、レボチロキシン 0.02 mg/kg PO q12h（甲状腺低下併発時）、"
                "低脂肪ペレット食への漸進的切替（種子4週で20%以下）、運動増加（飛翔促進）。"
                "③ 外科切除: 急速増大・潰瘍化・歩行/飛翔障害をきたす腫瘤に適応。"
                "病理組織で脂肪肉腫（liposarcoma）—境界不明瞭で再発しやすい—との鑑別必須。"
                "④ 周術期: 絶食3-6時間（短時間）、術前体重評価、温熱維持28-30℃、出血最小化（凝固障害合併が多い）。"
                "⑤ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h、術後3-5日継続。"
                "⑥ 切開部閉鎖は単層連続縫合（PDS 4-0/5-0）、テンション軽減。"
                "⑦ 黄色腫（xanthoma）合併例は皮膚再構成（advancement flap）を検討。" + _avian_supportive(species)
            ),
            "prognosis_ja": (
                "切除可能腫瘤は予後良好。再発例・脂肪肉腫は要警戒。食事・体重管理で発生・再発を予防できる。"
            ),
        }
    if species in SMALL_MAMMAL:
        ferret_note = ""
        if species == "ferret":
            ferret_note = (
                "フェレットでは皮下脂肪腫は稀—多くは皮下インスリノーマ転移巣・副腎関連腫瘤・リンパ腫の鑑別が優先。"
            )
        guinea_note = ""
        if species == "guinea_pig":
            guinea_note = "モルモットでは皮下腫瘤の最多原因は皮下膿瘍（Streptococcus zooepidemicus）—FNAで鑑別。"
        rabbit_note = ""
        if species == "rabbit":
            rabbit_note = "ウサギでは胸腺リンパ腫・線維肉腫の鑑別、頚部腫瘤は胸腺腫を除外。"
        return {
            "treatment_ja": (
                f"{species_ja}脂肪腫: ① 多くは老齢肥満個体に発生する良性皮下腫瘤。{ferret_note}{guinea_note}{rabbit_note}"
                "② 確定診断: 細胞診（FNA）で脂肪細胞確認、急速増大例は針生検または切除生検で脂肪肉腫/腺癌/膿瘍を除外。"
                "③ 手術適応: 機能障害（歩行・摂食・排泄阻害）、皮膚潰瘍、急速増大、整容的要請。"
                "④ 切除: 局所麻酔 + 軽鎮静で対応可能な小型腫瘤、全身麻酔が必要な深部・大型は周術期低体温・絶食管理を厳格に。"
                "⑤ 鎮痛: メロキシカム 0.5-1.5 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h、術後5-7日継続。"
                "⑥ 食事/体重管理: 高繊維低脂肪（チモシー主体、ペレット制限）、運動空間の確保、四半期毎の体重トレンド評価。"
                "⑦ 浸潤性脂肪腫（infiltrative lipoma）—筋層に浸潤、不完全切除で再発—に注意。"
                + _small_mammal_supportive(species)
            ),
            "prognosis_ja": (
                "境界明瞭な単純脂肪腫は外科切除で予後良好。浸潤性・脂肪肉腫疑い例は再発リスクあり経過観察が必要。"
            ),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}脂肪腫: ① 爬虫類・両生類の脂肪腫は飼育下肥満個体（特にヒョウモントカゲモドキ・フトアゴ・水生ガメ）で報告。"
                "② 体腔内脂肪（celomic fat body）の過形成と真の脂肪腫の鑑別が必要—超音波・CTで評価。"
                "③ 外科切除: 機能障害（呼吸・産卵・歩行）または急速増大時に適応。"
                "④ 周術期: 種別POTZ維持（前後72時間）、絶食24-72時間（種別代謝速度に応じる）、術前体重評価。"
                "⑤ 麻酔: アルファキサロン 5-15 mg/kg IM/IV、イソフルラン維持、IPPV準備。"
                "⑥ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h × 5-7日、ブプレノルフィン 0.01-0.05 mg/kg IM q12-24h。"
                "⑦ 食事・飼育是正: 給餌頻度減量（成体トカゲは2-3日毎）、高繊維野菜中心、UVB適正化、運動空間拡大。"
                "⑧ 組織学で脂肪肉腫を除外（爬虫類の脂肪肉腫は稀だが報告あり）。" + _reptile_supportive(species)
            ),
            "prognosis_ja": ("外科切除で予後良好。飼育・食事の是正がなければ再発・他部位発症リスク。"),
        }
    if species in DOG_CAT:
        if species == "dog":
            return {
                "treatment_ja": (
                    "犬脂肪腫の治療: ① 高齢中-大型犬（ラブラドール、ダックスフント、ドーベルマン）の最多軟部腫瘍。"
                    "② FNA細胞診で脂肪細胞確認、急速増大・固着例は脂肪肉腫または浸潤性脂肪腫の除外で生検必須。"
                    "③ 経過観察可: 境界明瞭・成長緩慢・機能無障害な小型腫瘤は3-6ヶ月毎の測定で対応。"
                    "④ 外科切除適応: 急速増大、機能障害（歩行・摂食阻害）、潰瘍化、整容的問題。"
                    "⑤ 鎮痛: メロキシカム 0.1-0.2 mg/kg PO q24h（術後5-7日）、トラマドール 2-5 mg/kg PO q8-12h（補助）。"
                    "⑥ 浸潤性脂肪腫（infiltrative lipoma）—筋層浸潤性で再発率高い—は広範囲切除＋術後放射線療法を考慮。"
                    "⑦ 体重・運動管理で発生抑制（肥満は危険因子）。"
                    "AAHA Oncology Guidelines 2016 参照。"
                ),
                "prognosis_ja": (
                    "単純脂肪腫は完全切除で予後極めて良好（再発<5%）。"
                    "浸潤性脂肪腫は局所再発率30-50%、脂肪肉腫は転移リスクあり MST 1-2年。"
                ),
            }
        return {  # cat
            "treatment_ja": (
                "猫脂肪腫の治療: ① 猫では犬より稀—皮下腫瘤の最多原因は注射部位肉腫（FISS）、リンパ腫、線維肉腫の鑑別が優先。"
                "② FNA細胞診を全症例で実施—Vaccine-associated sarcoma除外が最重要。"
                "③ 2-3 cm以上・3ヶ月以上残存・術後再発の腫瘤は incisional biopsy で確定診断（VAFSTF 2-3-1 ルール）。"
                "④ 単純脂肪腫が確定したら経過観察または機能障害時に切除。"
                "⑤ 周術期鎮痛: ブプレノルフィン 0.02-0.03 mg/kg IM/OTM q6-8h、ロベナコキシブ 1-2 mg/kg PO q24h（短期）。"
                "⑥ 老齢猫・甲状腺機能亢進症・糖尿病合併は周術期管理を厳格に。"
                "AAFP Practice Guidelines 参照。"
            ),
            "prognosis_ja": ("単純脂肪腫は予後良好。FISS や他の悪性腫瘍を見逃さなければ良好な経過。"),
        }
    return None


def gen_melanoma(species: str, name_ja: str) -> Optional[dict]:
    """Melanoma — biology + prognosis varies dramatically by species + anatomic site."""
    species_ja = _species_label_ja_local(species)
    if species == "dog":
        return {
            "treatment_ja": (
                "犬メラノーマの治療: ① 部位別生物学が異なる—口腔/粘膜型（攻撃的、転移率80%）、指端/爪床型（局所浸潤・遠隔転移）、"
                "皮膚型（多くは良性）、眼内型（中等度）。"
                "② 確定: 切除生検＋IHC（Melan-A、PNL2、TRP-1/2、S-100）—amelanotic例で重要。"
                "③ 病期診断: 局所LN生検（細胞診/組織検査）、胸部X線3方向、腹部超音波、CT（口腔・指端）。"
                "④ 外科治療: 口腔型は片側下顎/上顎切除術＋同側LN摘出（2cmマージン）、指端型は趾切断（中手骨/中足骨レベル）。"
                "⑤ 放射線療法: 切除不能・術後マイクロ残存に hypofractionated（6-9 Gy × 4-6回）—局所制御率70-80%。"
                "⑥ 免疫療法: Oncept（USDA承認、米国・カナダ）—stage II-III口腔メラノーマで MST 改善（>15ヶ月）。"
                "⑦ 化学療法: カルボプラチン 250-300 mg/m² IV q3週 × 4-6サイクル（限定的エビデンス）。"
                "AAHA Oncology Guidelines、Bergman et al. Vaccine 2006 (Oncept)。"
            ),
            "prognosis_ja": (
                "口腔: MST stage I 17-18ヶ月、stage II 6-9ヶ月、stage III 3-5ヶ月（外科+免疫療法併用で改善）。"
                "指端: MST 12-18ヶ月。皮膚良性型: 完全切除で治癒。眼内: 早期摘出で治癒可能。"
            ),
        }
    if species == "cat":
        return {
            "treatment_ja": (
                "猫メラノーマの治療: ① 猫ではメラノーマは犬より稀—虹彩色素沈着（FDIM: feline diffuse iris melanoma）が最多。"
                "② FDIM早期: 観察＋眼内圧モニタ（緑内障併発高率）、瞳孔形状/虹彩色変化を撮影記録。"
                "③ FDIM進行（眼内圧上昇、形状変化、ぶどう膜炎）: 早期眼球摘出術（enucleation）が転移予防に最も有効—"
                "晩期摘出は全身転移率増大（>60%）。"
                "④ 病理: 高度浸潤・有糸分裂高値はリンパ節・肝・肺転移リスク高い。"
                "⑤ 口腔・皮膚型: 広範切除（2-3 cmマージン）＋病期診断（LN/胸部画像）、化学療法（カルボプラチン）の補助は限定的エビデンス。"
                "⑥ 鎮痛: ブプレノルフィン 0.02-0.03 mg/kg OTM q6-8h、ロベナコキシブ 1-2 mg/kg PO q24h（短期）。"
                "Kalishman et al. Vet Comp Oncol 1998、Patnaik & Mooney JVIM 1988。"
            ),
            "prognosis_ja": (
                "FDIM早期摘出: MST >5年。進行例: MST 1.5-3年。口腔型: 攻撃的でMST 6-12ヶ月。皮膚型: 完全切除で予後良好。"
            ),
        }
    if species == "horse":
        return {
            "treatment_ja": (
                "馬メラノーマの治療: ① 灰色馬（特に8歳以上の灰色アラブ・サラブレッド）の80%が生涯発症する—多くは緩徐進行性。"
                "② 好発部位: 尾下・会陰部・包皮・耳介・眼瞼周囲—皮下硬結節として進行。"
                "③ 経過観察: 小型・成長緩慢・無症状例は3-6ヶ月毎の測定とX線/超音波で経過観察可。"
                "④ 外科切除: 急速増大、潰瘍化、機能障害、4-5 cm超に達した腫瘤に適応—2 cmマージン。"
                "⑤ 内科治療: シメチジン 2.5 mg/kg PO q8h × 90日（一部例で縮小報告）—エビデンス限定的。"
                "⑥ 細胞内化学療法: シスプラチン局所注入（1 mg/cm³ × 4-6セッション q14日）—大型・切除不能腫瘤に有効。"
                "⑦ 電気化学療法（electrochemotherapy）: シスプラチン+電気パルス、限定例で奏効率70%超の報告。"
                "⑧ 免疫療法: BCG・ヒトメラノーマDNAワクチン（Oncept—種特異性により馬では非承認）試験的。"
                "Smith et al. Equine Vet J 2002、Théon et al. JAVMA 2007。"
            ),
            "prognosis_ja": (
                "緩徐進行型: 多年無症状経過、生涯QoL良好。急速進行型・転移性（肺・肝・腹腔リンパ節）は予後不良MST 1-2年。"
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}メラノーマ: ① 鳥類メラノーマは稀—嘴基部・脚・羽毛根・口腔粘膜に色素性結節として発生。"
                "② 確定: 切除生検＋HE染色＋Fontana-Masson染色（メラニン）、amelanotic例はIHC（Melan-A）併用。"
                "③ 病期診断: 体腔X線（肝・肺）、CT（局所浸潤）、CBC・生化学（多くは正常）。"
                "④ 外科切除: 広範囲切除（実現可能なら 0.5-1 cm マージン）。嘴・脚部は機能温存とのバランス。"
                "⑤ 麻酔: イソフルラン、保温30-32℃、IPPV準備、絶食3時間。"
                "⑥ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h × 5-7日、ブプレノルフィン 0.01-0.05 mg/kg IM q6-12h。"
                "⑦ 化学療法: 限定的エビデンス—Oncept外挿例の報告（カナリア等）あり。"
                "⑧ 切除不能例: 緩和ケア（疼痛管理、栄養支持、QOL維持）。" + _avian_supportive(species)
            ),
            "prognosis_ja": ("早期局所切除で予後良好。転移例・切除不能例は予後不良で緩和ケア中心。"),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}メラノーマ: ① エキゾチック小型哺乳類のメラノーマは稀—皮膚・口腔粘膜・眼内に発生報告。"
                "② 確定: 切除生検＋HE+メラニン染色＋IHC（Melan-A・S-100）。amelanotic 例で IHC が必須。"
                "③ 病期診断: 全身画像（X線・超音波）、局所LN細胞診、CBC・生化学。"
                "④ 外科切除: 0.5-2 cmマージンの広範囲切除（解剖学的に可能な限り）。"
                "⑤ 麻酔: アルファキサロン IM/IV、イソフルラン維持、低体温対策（保温パッド・温輸液）。"
                "⑥ 鎮痛: メロキシカム 0.5-1.5 mg/kg PO q12-24h × 5-7日、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h。"
                "⑦ 化学療法: 種特異的データほぼなし—個別判断、緩和的役割中心。"
                "⑧ 切除不能・転移例: 緩和ケア（疼痛・栄養・QOL）。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": ("早期完全切除で予後良好。深部浸潤・転移例は予後不良。"),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}メラノーマ: ① 爬虫類・両生類のメラノーマは多くが皮膚または口腔粘膜の色素性結節として発生—"
                "局所浸潤性、転移率は哺乳類より低いが報告あり。"
                "② 確定: 切除生検＋HE＋メラニン染色、深部浸潤評価にCT/MRI。"
                "③ 外科治療: 広範囲切除（1-2 cmマージン）、口腔病変は片側顎切除も検討。"
                "④ 周術期: 種別POTZ前後72時間、絶食24-72時間（種別）、保温維持。"
                "⑤ 麻酔: アルファキサロン 10-15 mg/kg IM/IV、イソフルラン、IPPV準備。"
                "⑥ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h × 5-7日、ブプレノルフィン 0.01-0.05 mg/kg IM q12-24h、"
                "モルヒネ（亀のみ有効、ヘビ・トカゲでは無効）。"
                "⑦ 化学療法・放射線療法: 爬虫類でのデータ極めて限定的—個別検討。"
                "⑧ 切除不能例: 緩和ケア（栄養支持・POTZ最適化・疼痛緩和）。" + _reptile_supportive(species)
            ),
            "prognosis_ja": ("早期完全切除で予後良好。再発例・深部浸潤例は経過観察が必要。"),
        }
    return None


def gen_leukemia_lymphoma(species: str, name_ja: str) -> Optional[dict]:
    """Leukemia / lymphoid neoplasia — species-specific protocols (FeLV-associated in cats, etc.)"""
    species_ja = _species_label_ja_local(species)
    if species == "cat":
        return {
            "treatment_ja": (
                "猫白血病/リンパ系腫瘍の治療: ① 病型分類—消化管型（最多）、縦隔型（若齢、FeLV関連多い）、"
                "腎型、皮膚型、中枢神経型、白血病（急性ALL/AML、慢性CLL/CML）。"
                "② 確定: 病変部FNA/コア生検＋IHC（CD3 T細胞、CD20/Pax5 B細胞）、フローサイトメトリー、PARR（クローナリティ評価）。"
                "③ ウイルス検査: FeLV ELISA/PCR・FIV ELISA—予後因子。"
                "④ COP療法（中等度奏効・低毒性）: シクロホスファミド 200-300 mg/m² PO q3週、"
                "ビンクリスチン 0.5-0.7 mg/m² IV q週 × 4回、プレドニゾロン 2 mg/kg PO q24h漸減。"
                "⑤ CHOP療法（高奏効）: ドキソルビシン 25 mg/m² IV q3週（ピーク腎毒性—事前BUN/Cr確認）+ COP。19週プロトコル。"
                "⑥ 救援療法: ロムスチン 50-60 mg/m² PO q3-6週、L-asparaginase 400 IU/kg SC（再発時）。"
                "⑦ 支持療法: メトクロプラミド/マロピタント、栄養管理（高蛋白）、輸液、感染症管理（好中球減少期）。"
                "Vail et al. JVIM、Withrow & Vail Small Animal Clinical Oncology 6th ed。"
            ),
            "prognosis_ja": (
                "リンパ腫: COP応答 MST 6-9ヶ月、CHOP完全寛解で MST 12-18ヶ月。"
                "ALL: MST 1-3ヶ月。CLL: MST 1-2年。FeLV陽性は予後悪化（MST短縮）。"
            ),
        }
    if species == "dog":
        return {
            "treatment_ja": (
                "犬リンパ系腫瘍/白血病の治療: ① 病型分類—多中心型（最多80%）、消化管型、縦隔型、皮膚型、中枢神経型、"
                "白血病（ALL/AML、CLL/CML）。"
                "② 確定: リンパ節FNA/コア生検＋IHC（CD3/CD20/Pax5）、フローサイトメトリー、PARR。"
                "③ 病期診断: CBC・生化学・尿検査、胸腹部X線・超音波、骨髄穿刺（白血病疑い）。"
                "④ CHOP-25週プロトコル（標準）: ビンクリスチン → シクロホスファミド → ドキソルビシン → メトトレキセート/プレドニゾロン、"
                "8週後に維持—完全寛解率80-90%。"
                "⑤ COP療法（低リソース環境）: シクロホスファミド + ビンクリスチン + プレドニゾロン、"
                "完全寛解率70%、MST 6-7ヶ月。"
                "⑥ 救援療法: MOPP、ロムスチン、L-asparaginase、ダカルバジン。"
                "⑦ B細胞型は予後良好、T細胞型（特に CD4-CD8- ALL）は予後悪化。"
                "⑧ 支持療法: 制吐薬、輸液、好中球減少期の感染管理（抗菌薬予防投与）。"
                "Vail et al. JVIM、AAHA Oncology Guidelines 2016。"
            ),
            "prognosis_ja": (
                "B細胞リンパ腫CHOP: 完全寛解80-90%、MST 12-14ヶ月。"
                "T細胞リンパ腫: MST 6-8ヶ月。ALL: MST 1-3ヶ月。CLL: 緩徐、MST 12-24ヶ月。"
            ),
        }
    if species == "ferret":
        return {
            "treatment_ja": (
                "フェレットリンパ腫/白血病の治療: ① フェレットの最多悪性腫瘍の一つ—若齢型（リンパ芽球型、急性）と"
                "高齢型（リンパ球型、緩徐）。"
                "② 確定: リンパ節FNA/生検＋IHC、CBC（リンパ球数）、骨髄穿刺、超音波（脾臓・肝臓）。"
                "③ ALDH（Brown et al.）プロトコル: プレドニゾロン 1-2 mg/kg PO q24h、ビンクリスチン 0.07 mg/kg IV q週 × 4-8回、"
                "シクロホスファミド 10 mg/kg PO q週、ドキソルビシン 1 mg/kg IV q3週—完全寛解50-70%。"
                "④ 単剤プレドニゾロン: 緩和的—寛解率は低いがQOL改善。"
                "⑤ ロムスチン 10-50 mg/m² PO q3-6週: 救援療法。"
                "⑥ 支持療法: 高蛋白食、輸液 20-30 mL/kg/日 SC、ファムリディン 0.5 mg/kg PO q12h（消化管潰瘍予防）。"
                "Antinoff et al. J Avian Med Surg、Hutson et al. JAVMA。"
            ),
            "prognosis_ja": (
                "若齢急性型: MST 2-6ヶ月。高齢緩徐型: MST 12-18ヶ月（プレドニゾロン単剤でも長期生存例あり）。"
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}白血病/リンパ系腫瘍: ① 鳥類のリンパ系腫瘍はMD（Marek's Disease、ニワトリ）、LL（リンパ性白血病、Avian leukosis virus）、"
                "REV（網内皮症ウイルス）関連が知られる—コンパニオン鳥での原発性は稀。"
                "② 確定: 末梢血スメア、CBC（リンパ球増多）、内臓画像（X線・超音波）、組織生検＋IHC、ウイルス検査（PCR）。"
                "③ 化学療法（限定的データ）: クロラムブシル 2 mg/m² PO q24h、L-asparaginase 400 IU/kg IM、"
                "シクロホスファミド 5 mg/kg PO q24h × 4日 q3週、プレドニゾロン 1-2 mg/kg PO q12h。"
                "④ ドキソルビシン: 鳥での薬物動態データ限定—1 mg/kg IV q3週（試験的）。"
                "⑤ 支持療法: 強制給餌（Emeraid Carnivore）、輸液、保温30-32℃、肝補助（SAMe、シリマリン）。"
                "⑥ ウイルス性原因のスクリーニングと飼育環境改善、群飼育例は他鳥の検査。" + _avian_supportive(species)
            ),
            "prognosis_ja": (
                "鳥類の白血病/リンパ腫は化学療法エビデンス限定的—多くは予後不良で緩和ケア中心。"
                "孤立性結節型は外科切除＋補助化学療法で延命可能。"
            ),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}白血病/リンパ腫: ① エキゾチック小型哺乳類でのリンパ系腫瘍は症例報告レベル—フェレット以外では治療プロトコル未確立。"
                "② 確定: リンパ節/腫瘤FNA・生検＋IHC、CBC（リンパ球数、白血球分画）、画像診断（超音波・X線）、骨髄穿刺。"
                "③ 緩和的化学療法: プレドニゾロン 1-2 mg/kg PO q24h（多くで第一選択、QOL改善）、"
                "クロラムブシル 0.1-0.2 mg/kg PO q24-48h、L-asparaginase 10,000 IU/m² IM/SC q週（試験的）。"
                "④ 外科切除: 孤立性腫瘤型に限定的—多発性・全身性は化学療法。"
                "⑤ 支持療法: シリンジ給餌（Critical Care 50-90 mL/kg/日）、輸液 80-100 mL/kg/日 SC、温熱管理、"
                "メロキシカム 0.5-1.5 mg/kg PO q12-24h（疼痛・炎症）。"
                "⑥ 個別意思決定—QOL中心の緩和ケアを優先する場合が多い。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": (
                "種特異的データ限定的—多くは予後不良。プレドニゾロン緩和で数週-数ヶ月の QOL維持が現実的目標。"
            ),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}白血病/リンパ系腫瘍: ① 爬虫類・両生類でリンパ系腫瘍報告例は稀—多くは剖検時診断。"
                "② 生前確定: CBC（リンパ球異常）、超音波・CT、針生検／切除生検＋IHC。"
                "③ 治療プロトコル未確立—プレドニゾロン 0.5-1 mg/kg PO q24h（緩和的、慢性投与で免疫抑制注意）。"
                "④ 外科切除: 孤立性腫瘤に限定。"
                "⑤ 支持療法: POTZ最適化（治癒の前提）、強制給餌、温熱輸液 25-30 mL/kg/日 SC/ICe、"
                "メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h。"
                "⑥ QOL中心の緩和ケアが現実的選択肢となる場合が多い。" + _reptile_supportive(species)
            ),
            "prognosis_ja": ("症例報告レベルで予後データ限定的。多くで予後不良、緩和ケアが中心。"),
        }
    if species == "horse":
        return {
            "treatment_ja": (
                "馬リンパ系腫瘍/白血病: ① 馬の最多血液腫瘍—多中心型・縦隔型・皮膚型・腸管型。"
                "② 確定: リンパ節/腫瘤生検＋IHC、CBC・生化学、超音波（胸腔・腹腔）、胸水/腹水細胞診（縦隔型）。"
                "③ 化学療法: COP プロトコル（シクロホスファミド 200-300 mg/m² IV、ビンクリスチン 0.5 mg/m² IV、"
                "プレドニゾロン 1-2 mg/kg PO）—奏効率変動。"
                "④ 高用量プレドニゾロン単剤も緩和選択肢—蹄葉炎リスク監視。"
                "⑤ 外科切除: 孤立性皮膚リンパ腫に限定。"
                "⑥ 支持療法: 輸液、栄養管理（高蛋白）、潰瘍予防（オメプラゾール 4 mg/kg PO q24h）、感染症管理。"
                "Reef et al. Equine Internal Medicine。"
            ),
            "prognosis_ja": ("縦隔型・多中心型: MST 数週-数ヶ月。皮膚型: 緩徐進行で長期生存例あり。"),
        }
    return None


# ============================================================================
# Gout — avian/reptilian metabolic crystallopathy (visceral vs articular)
# ============================================================================


def gen_gout(species: str, name_ja: str) -> Optional[dict]:
    """Gout — uric acid deposition. Bird/reptile predominant; pathophysiology = dehydration + renal disease."""
    species_ja = _species_label_ja_local(species)
    nm = name_ja or ""
    is_visceral = "内臓" in nm or "visceral" in nm.lower()
    is_articular = "関節" in nm or "articular" in nm.lower()
    if species in AVIAN:
        if is_visceral:
            return {
                "treatment_ja": (
                    f"{species_ja}内臓型痛風: ① 病態—腎不全に伴う高尿酸血症で心嚢膜・肝・脾・腎実質に尿酸塩沈着。"
                    "症状出現時には進行例で予後不良。"
                    "② 確定: 血漿尿酸 >15 mg/dL（種別正常上限差あり）、X線・超音波で内臓白濁、"
                    "致死症例の剖検で確定。"
                    "③ 緊急的初期: 温輸液（5%デキストロース加リンゲル 50-100 mL/kg/日 SC/IO）—腎還流・尿酸排泄促進。"
                    "保温30-32℃、強制給餌（Emeraid Omnivore）。"
                    "④ 尿酸降下: アロプリノール 10-30 mg/kg PO q12-24h（⚠オウム目では一部毒性報告、Galah は要注意）、"
                    "代替: ベンズブロマロン 5 mg/kg PO q24h（試験的）。"
                    "⑤ コルヒチン 0.04 mg/kg PO q24h（炎症抑制、長期使用は注意）。"
                    "⑥ 食事: 低タンパク食（蛋白 12-14%）、水分供給（果物・野菜中心）、ビタミンA過剰回避。"
                    "⑦ 原因検索: 慢性脱水、高タンパク食、ビタミンA欠乏、腎毒性薬剤（aminoglycoside）、感染性腎症。"
                    + _avian_supportive(species)
                ),
                "prognosis_ja": "内臓型は症状出現時には腎機能の大部分が喪失—予後不良。生存例も生涯管理が必要。",
            }
        if is_articular:
            return {
                "treatment_ja": (
                    f"{species_ja}関節型痛風: ① 病態—関節・腱鞘・皮下に尿酸塩結節（tophi）—跛行・関節腫脹・破行。"
                    "② 確定: 結節穿刺で尿酸塩結晶確認（偏光顕微鏡で複屈折）、X線（関節周囲軟部陰影）、血漿尿酸測定。"
                    "③ 急性疼痛管理: メロキシカム 0.5-1.0 mg/kg PO/IM q12-24h、ブプレノルフィン 0.01-0.05 mg/kg IM q6-12h。"
                    "④ 尿酸降下: アロプリノール 10-30 mg/kg PO q12-24h、ベンズブロマロン 5 mg/kg PO q24h。"
                    "⑤ コルヒチン 0.04 mg/kg PO q24h—長期投与で再発予防。"
                    "⑥ 結節切除: 機能障害例は外科除去（再発リスクあり）。"
                    "⑦ 食事是正: 低タンパク・水分豊富、果物・野菜中心、ビタミンC・Eで抗酸化。"
                    "⑧ 環境改善: 止まり木のクッション化、温度・湿度適正化、適度な運動促進。"
                    + _avian_supportive(species)
                ),
                "prognosis_ja": ("関節型は慢性管理で長期生存可能だが、内臓型へ進展する例もあり生涯モニタが必要。"),
            }
        return {
            "treatment_ja": (
                f"{species_ja}痛風（内臓型/関節型混合）: ① 病型鑑別—血液検査・X線・関節結節穿刺で内臓型/関節型を判別。"
                "② 内臓型は緊急脱水補正と腎還流改善が最優先（温輸液 50-100 mL/kg/日 SC/IO）、保温30-32℃。"
                "③ 関節型は鎮痛（メロキシカム 0.5-1.0 mg/kg PO q12-24h）と尿酸降下を併行。"
                "④ アロプリノール 10-30 mg/kg PO q12-24h（⚠Galahで毒性報告—種別投与量確認）、"
                "ベンズブロマロン 5 mg/kg PO q24h、コルヒチン 0.04 mg/kg PO q24h。"
                "⑤ 食事是正: 低タンパク（12-14%）、水分豊富、ビタミンA過剰回避。"
                "⑥ 原因疾患（慢性脱水、腎症、腎毒性薬剤、ビタミンA欠乏）の同定と除去。" + _avian_supportive(species)
            ),
            "prognosis_ja": ("内臓型は腎機能予備能で決まり、症状出現時は予後不良。関節型は慢性管理で長期生存可能。"),
        }
    if species in REPTILE:
        if is_visceral:
            return {
                "treatment_ja": (
                    f"{species_ja}内臓型痛風: ① 病態—爬虫類で最多代謝性疾患の一つ（特にヒョウモントカゲモドキ・"
                    "イグアナ・グリーンイグアナ・水生ガメ）、慢性脱水＋高タンパク食＋腎症が主因。"
                    "② 確定: 血漿尿酸 >10 mg/dL（草食種では低め）、超音波/CTで内臓白濁、生検（腎・心嚢）。"
                    "③ 緊急脱水補正: 温輸液（ノルモソルR） 25-30 mL/kg/日 SC/ICe、温浴 20分 q24h（種別温度）、"
                    "POTZ維持（治癒の前提条件）。"
                    "④ 尿酸降下: アロプリノール 10-20 mg/kg PO q24h × 慢性、ベンズブロマロン 5 mg/kg PO q24h。"
                    "⑤ 食事是正: 種別 protein 制限（草食種は野菜中心、肉食種は赤身肉・bone-in prey、"
                    "魚介過剰摂取回避）、水分豊富な餌（葉野菜、果物適量）。"
                    "⑥ 環境是正: 飲水器の常時清掃、湿度適正化（種別）、温度勾配確保。"
                    "⑦ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h。" + _reptile_supportive(species)
                ),
                "prognosis_ja": ("内臓型は腎不全進行例で予後不良。早期発見・脱水管理で長期生存可能だが要慎重。"),
            }
        if is_articular:
            return {
                "treatment_ja": (
                    f"{species_ja}関節型痛風: ① 病態—四肢関節（特に肘・膝・指関節）の尿酸塩結節—跛行・関節腫脹・拒食。"
                    "② 確定: 結節穿刺で尿酸塩結晶確認、X線（関節周囲軟部陰影・骨破壊）、血漿尿酸測定。"
                    "③ 急性疼痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h × 7-14日、"
                    "ブプレノルフィン 0.01-0.05 mg/kg IM q12-24h（補助）。"
                    "④ 尿酸降下: アロプリノール 10-20 mg/kg PO q24h × 慢性、"
                    "ベンズブロマロン 5 mg/kg PO q24h、コルヒチン 0.04 mg/kg PO q24-72h。"
                    "⑤ 結節除去: 機能障害例は外科切除（再発リスク高い）。"
                    "⑥ 環境是正: 温浴 q24h、水分摂取促進、温度勾配・湿度最適化、運動空間確保。"
                    "⑦ 食事是正: 低タンパク化（種別）、水分豊富な野菜・果物、"
                    "ビタミン過剰回避（ビタミンA・D3）。" + _reptile_supportive(species)
                ),
                "prognosis_ja": ("関節型は慢性管理で生活の質を維持できる。再発と内臓型進展に注意。"),
            }
        return {
            "treatment_ja": (
                f"{species_ja}痛風: ① 病型判別—内臓型は超音波/CTで臓器白濁、関節型は結節穿刺で結晶確認。"
                "② 緊急脱水補正: ノルモソルR 25-30 mL/kg/日 SC/ICe、温浴、POTZ維持。"
                "③ 尿酸降下: アロプリノール 10-20 mg/kg PO q24h × 慢性、ベンズブロマロン 5 mg/kg PO q24h。"
                "④ 食事是正: 種別タンパク制限、水分豊富な餌、ビタミン過剰回避。"
                "⑤ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h。"
                "⑥ 環境是正: 温浴、湿度・温度勾配、清潔な飲水器。" + _reptile_supportive(species)
            ),
            "prognosis_ja": ("内臓型は腎機能で決まり要警戒、関節型は慢性管理で予後良好。"),
        }
    return None


# ============================================================================
# Nutritional Secondary Hyperparathyroidism / MBD — Ca/P imbalance crisis
# ============================================================================


def gen_nshp_mbd(species: str, name_ja: str) -> Optional[dict]:
    """NSHP / MBD — Ca/P imbalance, predominantly exotic herbivores/insectivores."""
    species_ja = _species_label_ja_local(species)
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}栄養性二次性副甲状腺機能亢進症/MBD: ① 病態—Ca:P比 <1:1の食事＋UVB不足＋ビタミンD3欠乏→"
                "副甲状腺ホルモン↑→骨吸収→繊維性骨形成異栄養症（fibrous osteodystrophy）→"
                "ピラミッディング、ゴム顎、四肢変形、病的骨折、嗜眠、テタニー。"
                "② 確定: X線（皮質骨菲薄化、病的骨折）、血清Ca・P・PTH測定、CBC・生化学。"
                "③ 緊急Ca補正（テタニー時）: グルコン酸Ca 100 mg/kg slow IV/ICe、その後 50-100 mg/kg PO q12-24h × 2-4週。"
                "④ ビタミンD3: 200-1,000 IU/kg PO q週 × 4-8週（過剰投与で転移性石灰化—血清Ca・Pモニタ）。"
                "⑤ UVB照射—種別UVI（leopard gecko: 2-4, bearded dragon: 4-6, iguana: 6-7）"
                "12時間/日、ランプ交換 q6ヶ月。"
                "⑥ 食事改善: 草食種—Ca:P比 2:1の葉野菜（colard greens、mustard greens、dandelion等）、"
                "ペレット補助。昆虫食—Ca-dust（Repashy Calcium Plus等）、gut-load 24-48時間前。"
                "⑦ 環境: POTZ維持（活性D3代謝の前提）、湿度適正化、運動空間確保。"
                "⑧ 病的骨折は副木またはケージ制限、骨密度改善後に再評価。"
                "Mader 2019、Divers & Stahl 2019。" + _reptile_supportive(species)
            ),
            "prognosis_ja": (
                "早期診断・矯正で予後良好。骨変形・病的骨折は永続するが機能温存可能。"
                "重度進行例（脊椎変形・呼吸障害）は予後不良。"
            ),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}栄養性二次性副甲状腺機能亢進症/MBD: ① 病態—全種子食/低Ca・低D3食→Ca:P比悪化→PTH↑→骨吸収。"
                "若鳥（特にアフリカン・グレイ、エクレクトゥス）で多発。"
                "② 症状: 病的骨折（翼下垂・歩行困難）、テタニー（低Ca痙攣）、骨格変形、若鳥の発育不良。"
                "③ 確定: 血清イオン化Ca（総Ca参考程度）、X線（骨密度低下）、CBC・生化学。"
                "④ 緊急Ca補正: グルコン酸Ca 50-100 mg/kg slow IV/IO（テタニー時）、その後 25-50 mg/kg SC/PO q12-24h。"
                "⑤ ビタミンD3: 1,000-3,300 IU/kg IM q週 × 4-8週（過剰投与注意）、"
                "経口補給は Ca カーボネート粉 0.5-1% 食。"
                "⑥ UVB照射: 5.0/10.0 UVB（鳥用）12時間/日、ガラス越し不可。"
                "⑦ 食事改善: ペレット主体（Harrison's、ZuPreem 等）への漸進的切替（4週でseed→pellet）、"
                "緑黄色野菜、卵殻粉 1%添加。"
                "⑧ 環境: 自然光（適切な時間帯）、適度な運動促進。" + _avian_supportive(species)
            ),
            "prognosis_ja": ("早期診断と食事改善で予後良好。病的骨折は癒合に4-8週、骨格変形は永続的だが機能可能。"),
        }
    if species in SMALL_MAMMAL:
        species_detail = ""
        if species == "sugar_glider":
            species_detail = "フクロモモンガ—市販ペットフードのみ・果物中心給餌例で多発。Leadbeater's mixレシピ（卵・蜂蜜・市販フード）推奨。"
        elif species == "hedgehog":
            species_detail = "ハリネズミ—昆虫食偏重で発生、Repashy等のCa dustが必須。"
        elif species == "guinea_pig":
            species_detail = "モルモットでは「Mulberry heart」型と区別、Ca補給と共にビタミンC 25-50 mg/kg q24hの併用。"
        elif species == "chinchilla":
            species_detail = "チンチラでは白色歯の喪失（茶色歯化）が早期サイン—チモシー+良質ペレット必須。"
        elif species == "degu":
            species_detail = "デグーは糖代謝異常のため糖分制限—Ca補給は無糖サプリで。"
        return {
            "treatment_ja": (
                f"{species_ja}栄養性二次性副甲状腺機能亢進症: ① 病態—Ca:P比不適切な食事→PTH↑→骨吸収→病的骨折・"
                f"歯歪み・テタニー。{species_detail}"
                "② 確定: 血清Ca・P、X線（骨密度低下、病的骨折）、CBC・生化学、栄養履歴聴取。"
                "③ Ca補正: グルコン酸Ca 50-100 mg/kg PO q12h × 2-4週（軽症）、グルコン酸Ca 100 mg/kg slow IV/SC（テタニー時）。"
                "④ ビタミンD3: 100-500 IU/kg PO q週 × 4-8週（過剰投与回避—血清Ca・Pモニタ）。"
                "⑤ 食事改善: チモシー牧草主体（草食種）、適量ペレット（Ca 0.5-1.0%）、Ca:P比 1.5-2:1、"
                "Caダスト昆虫（昆虫食種）、緑黄色野菜。"
                "⑥ 環境: 適度な日光浴または UVB（必要種—デグー・モルモット・ハリネズミは検討）、運動空間。"
                "⑦ 病的骨折は副木またはケージ制限、骨密度改善後に再評価（メロキシカム 0.5-1.0 mg/kg PO q12-24h）。"
                + _small_mammal_supportive(species)
            ),
            "prognosis_ja": ("早期診断・食事矯正で予後良好。骨格変形は永続的だが機能温存可能。"),
        }
    return None


def gen_hypervitaminosis_a(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}ビタミンA過剰症: ① 病態—注射VitA過量投与（医原性が最多原因）、過剰サプリメント。"
                "症状: 皮膚剥離・脱落（特にカメ頭頸部・両生類腹部）、肝障害、骨形成異常、二次感染。"
                "② 確定: 投薬・栄養履歴聴取、臨床症状、肝酵素↑、皮膚生検。"
                "③ 緊急停止: ビタミンA含有製剤の即時中止、混合ビタミン製剤の評価。"
                "④ 支持療法: 創傷管理（クロルヘキシジン0.05%）、SSD（silver sulfadiazine）局所、二次感染予防"
                "（エンロフロキサシン 5-10 mg/kg IM q24h）。"
                "⑤ 輸液（25-30 mL/kg/日 SC/ICe）、栄養支持、POTZ維持。"
                "⑥ 肝保護: SAMe 20 mg/kg PO q24h、シリマリン 10-15 mg/kg PO q12-24h。"
                "⑦ 注射VitA投与は禁忌—ベータカロテン経口で代替（種別量）。" + _reptile_supportive(species)
            ),
            "prognosis_ja": ("原因薬剤中止で皮膚は4-8週で再生—予後良好。重度二次感染合併例は要警戒。"),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}ビタミンA過剰症: ① 病態—ビタミンサプリメント過剰（特に注射剤・粉末混合）、肝臓給餌過多。"
                "② 症状: 食欲不振、皮膚病変、関節痛、嘴・骨格変形（若鳥）、肝障害。"
                "③ 緊急中止: ビタミン製剤、肝給餌の即時停止。"
                "④ 食事是正: 高ビタミンA食品制限、新鮮緑葉野菜中心、適切ペレット。"
                "⑤ 支持療法: 輸液 50-100 mL/kg/日 SC、栄養支持、肝保護（SAMe、シリマリン）。"
                "⑥ 確定: 血清VitA濃度、投薬・栄養履歴。" + _avian_supportive(species)
            ),
            "prognosis_ja": "原因停止で予後良好、慢性骨変形は永続することあり。",
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}ビタミンA過剰症: ① ハムスター・モルモット等ではビタミンドロップ過剰投与例で報告。"
                "② 症状: 皮膚剥離、肝障害、骨変形、食欲不振。"
                "③ ビタミン製剤即時中止、肝給餌制限。"
                "④ 支持療法: 創傷管理、輸液、SAMe 20 mg/kg PO q24h、シリマリン 10-15 mg/kg PO q12-24h。"
                "⑤ 食事矯正: バランス食（草食種—チモシー、適量ペレット）、過剰サプリ回避。"
                + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "原因停止で予後良好。",
        }
    return None


def gen_hypervitaminosis_d3(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}ビタミンD3過剰症: ① 病態—経口D3製剤過剰投与＋UVB過剰照射併用例で報告。"
                "高Ca血症→転移性石灰化（血管・腎・心嚢・消化管）—不可逆性。"
                "② 確定: 血清Ca（>15 mg/dLで重度）、リン、25(OH)D3、X線（軟部組織石灰化）、組織生検。"
                "③ 緊急対応: ビタミンD3製剤の即時停止、UVB照射の一時減量または中止。"
                "④ Ca降下: 等張輸液（ノルモソルR 25-30 mL/kg/日 SC/ICe）で希釈、フロセミド 5 mg/kg IM/IV q12h × 短期。"
                "⑤ 低Ca食: 草食種は Caが低めの野菜、肉食種は低リン餌（liver回避）。"
                "⑥ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h、ガバペンチン 5-10 mg/kg PO q12h（補助）。"
                "⑦ POTZ維持、栄養支持。" + _reptile_supportive(species)
            ),
            "prognosis_ja": ("転移性石灰化は不可逆—予後要警戒。早期発見・原因除去で進展抑制可能。"),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}ビタミンD3過剰症: ① 病態—ビタミン製剤過剰投与で発生。腎・血管・心臓に転移性石灰化。"
                "② 確定: 血清Ca・25(OH)D3測定、X線（血管・腎石灰化）。"
                "③ 緊急停止: D3製剤の即時中止、UVB照射の調整。"
                "④ Ca降下: 輸液 50-100 mL/kg/日 SC、フロセミド 1-2 mg/kg IM q12h（短期、脱水注意）。"
                "⑤ 食事是正: ペレット・サプリメントの再評価、新鮮野菜・果物中心へ。" + _avian_supportive(species)
            ),
            "prognosis_ja": "石灰化は不可逆—予後要警戒。",
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}ビタミンD3過剰症: ① 過剰サプリ・ビタミンミックス事故等で発生。"
                "② 確定: 血清Ca↑、X線（軟部石灰化）。"
                "③ 緊急中止、輸液で希釈、フロセミド 1-2 mg/kg IM/PO q12h（短期）、低Ca食。"
                "④ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "石灰化は不可逆—予後要警戒。",
        }
    return None


# ============================================================================
# Vitamin deficiencies — species-specific (A, E, Thiamine)
# ============================================================================


def gen_vitamin_a_deficiency(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in REPTILE or species == "amphibian":
        chelonian_note = ""
        if species in {"tortoise", "reptile"}:
            chelonian_note = "（リクガメ・水生ガメで最多代謝疾患）"
        return {
            "treatment_ja": (
                f"{species_ja}ビタミンA欠乏症{chelonian_note}: ① 病態—全粒食/イモムシ偏食/植物食偏重で発症—"
                "上皮の扁平上皮化生→眼瞼浮腫、結膜炎、口腔/総排泄腔粘膜病変、呼吸器症状、皮膚剥離、繁殖障害。"
                "② 確定: 病歴聴取、臨床症状、組織生検（扁平上皮化生）、血清VitA測定。"
                "③ ビタミンA投与: 2,000-5,000 IU/kg IM 1回、1-2週後再投与（過剰投与でVitA中毒に注意）。"
                "経口製剤も使用可（β-カロテン経口は安全マージン広い）。"
                "④ 食事改善: カロチン豊富な濃緑色野菜（dandelion、collard greens、mustard greens、squash）、"
                "肉食種は内臓肉適量、昆虫食種は gut-load 野菜豊富。"
                "⑤ 眼科支持: 人工涙液 q4-6h、抗菌点眼（ofloxacin等）、眼瞼浮腫は温湿布。"
                "⑥ 二次感染予防: エンロフロキサシン 5-10 mg/kg PO/IM q24-48h（呼吸器・眼科症状時）。"
                "⑦ POTZ維持、湿度適正化（種別）。" + _reptile_supportive(species)
            ),
            "prognosis_ja": ("早期発見・食事矯正で予後良好。眼瞼変形・繁殖障害は遷延することあり。"),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}ビタミンA欠乏症: ① 病態—全種子食給餌（オウム目で典型）→ビタミンA欠乏→"
                "扁平上皮化生→眼瞼/結膜浮腫、副鼻腔炎、舌下/口腔膿瘍、皮膚過角化、繁殖障害。"
                "② 確定: 病歴（種子主体）、臨床症状、舌下生検（扁平上皮化生）、血清VitA。"
                "③ ビタミンA: 10,000-25,000 IU/kg IM 1回、1-2週後再投与（過剰投与回避）、"
                "経口 1,000-2,000 IU/羽 q週 × 4-8週。"
                "④ 食事是正: ペレット主体（Harrison's、ZuPreem等）への漸進切替（4-6週でseed→pellet）、"
                "緑黄色野菜（ニンジン、カボチャ、葉野菜）、果物（マンゴー、パパイヤ）添加。"
                "⑤ 副鼻腔・口腔病変: 局所洗浄、抗菌薬（エンロフロキサシン 10-15 mg/kg PO/IM q12h）。"
                "⑥ 眼科支持: 人工涙液、抗菌点眼。" + _avian_supportive(species)
            ),
            "prognosis_ja": ("食事完全切替＋VitA補給で予後良好。慢性副鼻腔病変は遷延可能性あり。"),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}ビタミンA欠乏症: ① 適切な市販食給餌では稀—不適切な手作り食・古い飼料で発生。"
                "② 症状: 皮膚過角化、眼乾燥、繁殖障害、若齢の発育遅延。"
                "③ ビタミンA: 500-2,000 IU/kg PO q24h × 7-14日（過剰投与回避）、β-カロテン経口は安全。"
                "④ 食事是正: 緑黄色野菜（種別適量）、新鮮市販フード、バランス食。"
                "⑤ 二次感染予防: 角化部位の細菌感染—エンロフロキサシン 5-10 mg/kg PO q12h（必要時）。"
                + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "食事矯正で予後良好。",
        }
    return None


def gen_vitamin_e_deficiency(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species == "ferret":
        return {
            "treatment_ja": (
                "フェレットビタミンE欠乏症: ① 病態—魚ベース食/酸化したPUFAを多く含む不適切な食事→"
                "脂肪組織の褐色変性（黄色脂肪病、yellow fat disease/steatitis）→"
                "皮下硬結節、疼痛、食欲不振、発熱、嗜眠。"
                "② 確定: 病歴（魚・古い脂肪食）、皮下結節触診、生検（脂肪織炎、ceroid沈着）、血清VitE/PUFA測定。"
                "③ VitE補給: α-トコフェロール 10-50 IU/kg PO q24h × 2-4週、その後維持 5-20 IU/kg q24h。"
                "④ セレン補給（協同抗酸化）: 0.05-0.1 mg/kg PO q24h（過剰投与に注意—治療域狭い）。"
                "⑤ 食事改善: 新鮮高品質肉食フード（Wysong Epigen、Carnivore Care、ferret用ペレット）、"
                "魚ベース食・古い脂肪食回避。"
                "⑥ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO q24h × 7-14日、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h（重度時）。"
                "⑦ 支持療法: シリンジ給餌、輸液、温熱管理。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": ("原因食除去＋VitE補給で予後良好。皮下結節は数週-数ヶ月で吸収。"),
        }
    if species == "sugar_glider":
        return {
            "treatment_ja": (
                "フクロモモンガビタミンE欠乏症: ① 病態—不適切な果物中心食/Leadbeater's mix未提供で発症。"
                "症状: 筋力低下、痙攣、繁殖障害、脂肪織炎。"
                "② VitE 10-50 IU/kg PO q24h × 2-4週、セレン補給（要注意）。"
                "③ 食事改善: Leadbeater's mixレシピ（卵・蜂蜜・市販フード・ベビーセリアル）、"
                "新鮮昆虫（Ca dust+gut-load）、適量果物、ペレット補助。"
                "④ 支持療法: シリンジ給餌、温熱管理、輸液。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "食事改善で予後良好。",
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}ビタミンE欠乏症: ① 病態—魚食肉食種（特に水生ガメ、魚食ヘビ、ワニ）で"
                "PUFA酸化食提供で発症—steatitis（脂肪織炎）、筋ジストロフィー、白筋病。"
                "② 確定: 病歴（魚食・酸化食）、皮下/筋脂肪触診、生検、血清VitE。"
                "③ VitE: 10-100 IU/kg IM/PO q週 × 4週、その後維持。"
                "④ セレン: 0.05-0.1 mg/kg PO q24h（治療域狭い—過剰禁）。"
                "⑤ 食事改善: 新鮮魚（古い・冷凍劣化魚回避）、多様食、適切gut-load。"
                "⑥ POTZ維持、支持療法。" + _reptile_supportive(species)
            ),
            "prognosis_ja": "食事是正と補給で予後良好。",
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}ビタミンE欠乏症: ① 病態—PUFA酸化食/不適切種子食で発生。"
                "症状: 脳軟化症（脳卒中様症状）、筋ジストロフィー、繁殖障害。"
                "② VitE: 10-100 IU/kg IM/PO q週 × 4週。"
                "③ セレン補給は治療域狭く要注意。"
                "④ 食事改善: 新鮮ペレット、緑葉野菜、種子は新鮮で適量。" + _avian_supportive(species)
            ),
            "prognosis_ja": "脳軟化症進行例は予後不良、初期治療で改善可能。",
        }
    return None


def gen_thiamine_deficiency(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species == "ferret":
        return {
            "treatment_ja": (
                "フェレットチアミン欠乏症: ① 病態—生淡水魚（コイ、ニシン等チアミナーゼ含有）給餌、"
                "硫酸塩過剰水で発症—神経症状、後弓反張、痙攣、嗜眠。"
                "② 確定: 病歴、神経症状、血清チアミン測定、治療反応性。"
                "③ チアミン: 25-50 mg/kg IM q24h × 3-5日、その後経口 10-25 mg/kg PO q24h × 1-2週。"
                "④ B群ビタミン補給併用。"
                "⑤ 食事改善: 加熱魚または新鮮chicken/turkeyベースの肉食フード、生淡水魚回避。"
                "⑥ 支持療法: 温熱、輸液、痙攣管理（ジアゼパム 0.5-1 mg/kg IV）。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "早期治療で予後良好—24-48時間で改善。",
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}チアミン欠乏症: ① 病態—魚食ヘビ・ワニ・水生種で冷凍金魚・古いコイ給餌で発症—"
                "opisthotonus、痙攣、虚脱、神経症状。"
                "② チアミン: 25-100 mg/kg IM q24h × 3-5日（重症は IM/SC）、その後経口 25 mg/kg PO q24-48h × 1-2週。"
                "③ B群ビタミン併用。"
                "④ 食事改善: 加熱魚（チアミナーゼ不活化）、多様な魚種、適切gut-load。"
                "⑤ POTZ維持、輸液、痙攣管理（ジアゼパム 0.5-1 mg/kg IM）。" + _reptile_supportive(species)
            ),
            "prognosis_ja": "早期治療で予後優良。",
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}チアミン欠乏症: ① 病態—精白米・古い穀物中心食、生魚給餌（魚食鳥）で発生。"
                "症状: opisthotonus（star-gazing）、痙攣、麻痺、跛行。"
                "② チアミン: 1-3 mg/kg IM q24h × 3-5日、経口 1 mg/kg PO q24h × 1-2週。"
                "③ B群ビタミン併用。"
                "④ 食事是正: バランスペレット、新鮮多様穀物、生魚回避（or 加熱）。" + _avian_supportive(species)
            ),
            "prognosis_ja": "迅速治療で予後優良—数時間で神経症状改善。",
        }
    if species == "sugar_glider":
        return {
            "treatment_ja": (
                "フクロモモンガチアミン欠乏症: ① 不適切食事で稀に発生—神経症状、痙攣。"
                "② チアミン 1-3 mg/kg IM q24h × 3-5日、B群併用。"
                "③ Leadbeater's mix導入、多様食。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "早期治療で予後良好。",
        }
    return None


# ============================================================================
# Iron Storage Disease (Hemochromatosis) — avian-predominant
# ============================================================================


def gen_iron_storage_disease(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}鉄蓄積症（ヘモクロマトーシス）: ① 病態—鉄感受性種（ミナミハコス・"
                "オオハシ・ハチドリ・フルーツバット・タンザニア起源種）で高鉄食/補給で肝・心・脾に鉄沈着→"
                "肝不全、腹水、呼吸困難。"
                "② 確定: 肝生検（鉄染色—プルシアンブルー）、血清フェリチン↑、肝酵素↑、超音波（肝腫大）。"
                "③ 瀉血治療: 体重1%/週（小型1-2 mL、中型2-5 mL）× 4-8回、Hb・PCV モニタ。"
                "④ デフェロキサミン（鉄キレート）: 100 mg/kg IM q24h × 5-7日、その後 IM q週 × 慢性。"
                "⑤ 食事改善: 低鉄ペレット（鉄 <100 ppm、Harrison's Low-Iron など）、"
                "鉄豊富な食品（赤身肉、緑葉野菜）制限。"
                "⑥ ビタミンC制限: 鉄吸収促進→VitC含有サプリ・果物（オレンジ・トマト）回避。"
                "⑦ 肝保護: SAMe 20 mg/kg PO q24h、シリマリン 10-15 mg/kg PO q12-24h、ウルソデオキシコール酸 10-15 mg/kg PO q12h。"
                "⑧ 腹水: フロセミド 1-2 mg/kg IM q12-24h、腹腔穿刺（呼吸障害時）。" + _avian_supportive(species)
            ),
            "prognosis_ja": ("早期発見・瀉血+食事改善で予後良好。肝硬変進行例は予後不良。"),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}鉄蓄積症: ① エキゾチック小型哺乳類でも報告（特にハムスター・チンチラ・ハリネズミ）—"
                "高鉄食・遺伝的素因で発症。肝不全、嗜眠、被毛不良。"
                "② 確定: 肝生検（プルシアンブルー鉄染色）、血清フェリチン、肝酵素、超音波。"
                "③ 瀉血: サイズによっては困難—代替的にデフェロキサミン 100 mg/kg IM q24h × 5-7日。"
                "④ 食事改善: 低鉄ペレット、緑葉野菜・赤身肉制限、VitC含有サプリ制限。"
                "⑤ 肝保護: SAMe 20 mg/kg PO q24h、シリマリン 10-15 mg/kg PO q12-24h。"
                + _small_mammal_supportive(species)
            ),
            "prognosis_ja": ("肝硬変が進む前の早期発見・管理で予後改善。"),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}鉄蓄積症（ヘモクロマトーシス）: ① 爬虫類・両生類での報告は稀—主に飼育下肉食種で慢性高鉄食給餌例。"
                "肝・脾・腎に鉄沈着→肝不全、腹水、嗜眠。"
                "② 確定: 肝生検（プルシアンブルー鉄染色）、血清フェリチン、肝酵素↑、超音波（肝腫大）。"
                "③ 瀉血: 体サイズによっては困難—デフェロキサミン（鉄キレート） 100 mg/kg IM/SC q24h × 5-7日が代替。"
                "④ 食事改善: 低鉄食（赤身肉・内臓肉制限）、ビタミンC制限（鉄吸収促進のため）、種別バランス食。"
                "⑤ 肝保護: SAMe 20 mg/kg PO q24h、シリマリン 10-15 mg/kg PO q12-24h、ウルソデオキシコール酸 10-15 mg/kg PO q12h。"
                "⑥ POTZ維持、輸液（ノルモソルR 25-30 mL/kg/日 SC/ICe）、強制給餌。"
                "⑦ 腹水: フロセミド 2-5 mg/kg IM q12-24h（短期、脱水モニタ）、必要なら体腔穿刺。"
                + _reptile_supportive(species)
            ),
            "prognosis_ja": ("肝硬変進行例は予後不良。早期発見・食事改善・キレート療法で改善可能。"),
        }
    return None


# ============================================================================
# Myiasis — fly larvae infestation, species-specific topical concerns
# ============================================================================


def gen_myiasis(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species == "rabbit":
        return {
            "treatment_ja": (
                "ウサギ蝿蛆症（Cuterebra・flystrike）の治療: ① ⚠緊急—肛門周囲・湿潤被毛部のCuterebra/blowfly感染で"
                "急性毒性ショック→数時間で死亡することあり。夏期屋外飼育例で多発。"
                "② 全蛆虫の手動除去（細鑷子、麻酔下が望ましい）、Cuterebra warbleは皮膚切開で慎重に摘出—"
                "破砕すると過敏症ショック。"
                "③ 創傷管理: 温生理食塩水/クロルヘキシジン 0.05% 洗浄、壊死組織デブリードマン。"
                "④ 抗菌薬（培養感受性後）: エンロフロキサシン 10-15 mg/kg PO/SC q12h × 7-14日、"
                "⚠経口β-ラクタム（ペニシリン、アモキシシリン）は腸内細菌叢破壊で禁忌。"
                "⑤ イベルメクチン 0.2-0.4 mg/kg SC q14日 × 2-3回（外部残存幼虫対策）。"
                "⑥ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h × 5-7日、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h。"
                "⑦ 支持療法: 輸液、シリンジ給餌（Critical Care）、温熱管理（重度ショックは体温低下注意）。"
                "⑧ 予防: 屋外飼育時のflyscreen、被毛清掃、肥満・関節炎の予防（肛門周囲清掃能力維持）。"
            ),
            "prognosis_ja": ("早期発見で予後良好（72時間以内）。重度感染・ショック合併例は予後不良（死亡率30-50%）。"),
        }
    if species in REPTILE or species == "amphibian":
        amphib_note = ""
        if species == "amphibian":
            amphib_note = (
                "⚠両生類は皮膚吸収性高い—イベルメクチン全身投与は神経毒性で禁忌。背側リンパ嚢への局所投与のみ。"
            )
        return {
            "treatment_ja": (
                f"{species_ja}蝿蛆症: ① 屋外飼育・湿潤環境・外傷部位での発生。"
                "② 全蛆虫の手動除去（細鑷子）、麻酔下が望ましい（イソフルラン）。"
                "③ 創傷洗浄: 温生理食塩水・希釈クロルヘキシジン 0.05%、壊死組織デブリードマン。"
                "④ 局所: SSD（silver sulfadiazine）1% クリーム、マヌカハニー（創傷治癒促進）。"
                "⑤ 抗菌薬: エンロフロキサシン 5-10 mg/kg PO/IM q24-48h × 10-14日、"
                "セフタジジム 20 mg/kg IM q72h（グラム陰性菌対応）。"
                f"⑥ イベルメクチン（爬虫類のみ）: 0.2 mg/kg IM/SC q14日 × 2回。"
                "⚠カメ類（chelonian）はイベルメクチン感受性高い—禁忌または極低用量。"
                f"{amphib_note}"
                "⑦ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h × 5-7日。"
                "⑧ 環境: POTZ維持、湿度適正化、ハエ網設置、外傷源除去。" + _reptile_supportive(species)
            ),
            "prognosis_ja": ("早期発見・除去で予後良好。深部組織浸潤・全身感染合併例は予後要警戒。"),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}蝿蛆症: ① 屋外飼育・外傷部位・羽毛汚染部位での発生。"
                "② 全蛆虫の鑷子除去（必要に応じて麻酔下）。"
                "③ 創傷洗浄: 温生理食塩水・希釈クロルヘキシジン、壊死組織除去。"
                "④ 局所: SSD クリーム、マヌカハニー。"
                "⑤ 抗菌薬: エンロフロキサシン 10-15 mg/kg PO/IM q12h × 7-10日、"
                "アモキシシリン/クラブラン酸 125 mg/kg PO q12h（培養感受性後調整）。"
                "⑥ イベルメクチン 0.2 mg/kg SC/PO q14日 × 2回（残存幼虫対策）。"
                "⑦ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h × 5-7日。"
                "⑧ 環境: ハエ網、ケージ清掃、外傷源除去。" + _avian_supportive(species)
            ),
            "prognosis_ja": "早期治療で予後良好。",
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}蝿蛆症: ① 屋外/汚れた環境・肛門周囲湿潤・外傷部位で発生。"
                "② 全蛆虫の鑷子除去（麻酔下が望ましい）、Cuterebra warbleは慎重に摘出。"
                "③ 創傷管理: 温生理食塩水/クロルヘキシジン、デブリードマン。"
                "④ 抗菌薬: エンロフロキサシン 5-10 mg/kg PO/SC q12-24h、"
                "⚠草食種は経口β-ラクタム禁忌。"
                "⑤ イベルメクチン 0.2-0.4 mg/kg SC q14日 × 2回。"
                "⑥ 鎮痛: メロキシカム 0.5-1.0 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h。"
                "⑦ 環境管理、ハエ網、定期的清掃。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "早期治療で予後良好、重度ショック例は予後要警戒。",
        }
    return None


# ============================================================================
# Mucormycosis (Zygomycosis) — invasive fungal infection
# ============================================================================


def gen_mucormycosis(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    base = (
        "① 病態—Mucorales目（Rhizopus、Mucor、Lichtheimia）による侵襲性真菌感染—"
        "免疫抑制・糖尿病・慢性疾患で日和見感染。皮膚・呼吸器・全身。"
        "⚠ アゾール系（フルコナゾール、イトラコナゾール）はムコラレスに無効。"
        "② 確定: 病変部生検＋GMS/PAS染色（広い非中隔菌糸）、培養（4-7日）、PCR。"
        "③ 外科的デブリードマン（大型病変は治療の根幹）。"
        "④ 第一選択薬: アムホテリシンB（リポソーマル形式 5-10 mg/kg IV q24h × 4-6週、"
        "従来型 0.5-1.0 mg/kg IV q24-48h—腎毒性モニタ）。"
        "⑤ 第二選択: ポサコナゾール 5 mg/kg PO q12h × 慢性（in vitro感受性確認後）。"
        "⑥ 免疫機能改善: 糖尿病管理、ステロイド減量、栄養支持。"
    )
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}ムコール症: {base}"
                "⑦ 鳥類では呼吸器感染（気嚢炎）が多い—気管支鏡下デブリードマン+局所アムホテリシンB噴霧。"
                + _avian_supportive(species)
            ),
            "prognosis_ja": "侵襲性で予後不良。早期外科切除+抗真菌薬併用で改善可能。",
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}ムコール症: {base}"
                "⑦ 爬虫類・両生類では皮膚・口腔粘膜の侵襲性感染が多い—デブリードマン+局所アムホテリシンB浴 1 mg/mL × 5分/日"
                "（⚠腎毒性—長期使用注意）。POTZ維持、清潔環境必須。" + _reptile_supportive(species)
            ),
            "prognosis_ja": "侵襲性で予後不良。早期外科切除+抗真菌薬+環境改善で改善可能。",
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}ムコール症: {base}"
                "⑦ 免疫抑制状態（ステロイド、糖尿病、慢性疾患）の評価と是正。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "侵襲性で予後不良—早期外科+抗真菌薬で改善可能。",
        }
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}ムコール症: {base}"
                "⑦ 鼻腔・副鼻腔・皮膚・消化管に発生—免疫抑制基礎疾患の評価必須。"
                "AAHA Infectious Disease Guidelines、Wiebe et al. JAVMA 2009。"
            ),
            "prognosis_ja": "侵襲性で予後不良、早期治療で改善可能。",
        }
    return None


# ============================================================================
# Muscle Wasting / Cachexia — species-specific supportive care
# ============================================================================


def gen_muscle_wasting(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}筋萎縮/悪液質: ① 病態—原発疾患（腫瘍、慢性腎症、心疾患、慢性感染、歯科疾患、関節炎）に伴う"
                "筋蛋白分解・食欲不振→筋萎縮、体重減少、虚弱。"
                "② 確定: 詳細な身体検査（BCS<3/9、MCS<2/3）、CBC・生化学・尿検査、画像（X線・超音波）、"
                "歯科検査（草食種は必須—臼歯不正咬合スクリーニング）、心電図（必要時）。"
                "③ 原発疾患治療: 慢性腎症→輸液・リン制限、腫瘍→外科/化学療法、歯科疾患→歯冠調整、"
                "心疾患→循環管理。"
                "④ 栄養支持: シリンジ給餌（Critical Care、Recovery）50-90 mL/kg/日 × 3-4分割、"
                "高蛋白（草食種は良質チモシー+ペレット、肉食種は良質肉食フード）。"
                "⑤ 食欲刺激: ミルタザピン 0.5-1 mg/kg PO q24-48h（草食種では効果限定的）、"
                "シプロヘプタジン 0.1-0.5 mg/kg PO q12-24h。"
                "⑥ 鎮痛（疼痛性筋萎縮）: メロキシカム 0.5-1.0 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h。"
                "⑦ リハビリ: 適度な運動空間、抵抗運動（坂・斜面）、温熱療法。"
                "⑧ 体重トレンドのモニタリング（毎週測定）、写真記録で進行評価。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": ("原発疾患による—早期発見・治療で予後改善。慢性腎症・腫瘍進行例は緩和ケア中心。"),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}悪液質/筋萎縮: ① 病態—慢性疾患（鉄蓄積、感染症、腫瘍、PDD等）、不適切食事、社会的ストレスで進行。"
                "② 確定: 胸筋スコア（keel score 1-5）、体重、CBC・生化学、画像（X線・超音波）、感染症スクリーニング。"
                "③ 原発疾患治療: 鉄蓄積→瀉血、感染症→抗菌薬、PDD→セレコキシブ、腫瘍→外科/緩和。"
                "④ 栄養支持: 強制給餌（Emeraid Carnivore/Omnivore 20-30 mL/kg q4-6h）、保温30-32℃。"
                "⑤ 食欲刺激: 嗜好性高い食材（果物、種子）、ペレット浸漬で柔軟化。"
                "⑥ 環境改善: ストレス除去、適度な飛翔空間、社会的相互作用。" + _avian_supportive(species)
            ),
            "prognosis_ja": ("原発疾患による—早期介入で予後改善。"),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}筋萎縮: ① 病態—慢性疾患（NSHP、腫瘍、寄生虫、不適切POTZ）、不適切食事で進行。"
                "② 確定: 体重トレンド、X線（骨密度）、CBC・生化学、寄生虫検査、POTZ・UVB評価。"
                "③ 原発疾患治療: NSHP→Ca・VitD3・UVB、寄生虫→駆虫、感染→抗菌薬。"
                "④ 栄養支持: 強制給餌（Carnivore Care、Critical Care、肉食種は適切な獲物サイズ）、POTZ最適化。"
                "⑤ 環境改善: POTZ確保（治癒・代謝の前提）、UVB照射、適度な運動空間。" + _reptile_supportive(species)
            ),
            "prognosis_ja": ("原発疾患による—早期発見・矯正で予後改善。"),
        }
    return None


# ============================================================================
# Reptile/amphibian cross-species exotic syndromes — species-tailored details
# ============================================================================


def gen_reptile_coelomitis(species: str, name_ja: str) -> Optional[dict]:
    """Peritonitis / coelomitis in reptiles — egg-related or septic."""
    species_ja = _species_label_ja_local(species)
    if species not in REPTILE and species != "amphibian":
        return None
    is_egg = "卵" in (name_ja or "")
    extra = ""
    if species == "tortoise":
        extra = "リクガメは甲羅切開（plastronotomy）が必要で麻酔・術後管理が複雑。"
    elif species == "snake":
        extra = "ヘビは細長い体腔と多数の臓器（卵管×2）—切開部位は腹側鱗の正中線、術中の臓器同定が重要。"
    elif species == "lizard":
        extra = "トカゲは腹側皮膚切開で体腔アクセス、保温と低体温対策を厳格に。"
    elif species == "amphibian":
        extra = "両生類は皮膚透過性が高く、術中の脱水・電解質損失に注意—温浴で支持。"
    return {
        "treatment_ja": (
            f"{species_ja}腹膜炎/体腔炎: ① ⚠緊急。"
            f"{'卵関連体腔炎' if is_egg else '感染性/非感染性体腔炎'}—"
            "卵管破裂、消化管穿孔、卵黄性腹膜炎、または血行性敗血症が主因。"
            "② 確定: 体腔穿刺（細胞診・培養）、超音波/CT、CBC・生化学。"
            "③ 緊急安定化: 温輸液（ノルモソルR 25-30 mL/kg/日 SC/ICe、ショック時はボーラス 10-20 mL/kg IV/IO）、"
            "POTZ維持（前後72時間）、酸素投与（必要時）。"
            "④ 抗菌薬（広域→培養後調整）: エンロフロキサシン 5-10 mg/kg IM q24h + セフタジジム 20 mg/kg IM q72h、"
            "嫌気性菌カバー必要時はメトロニダゾール 20 mg/kg PO q24-48h。"
            "⑤ 外科治療: 探索的体腔切開→原因特定（消化管穿孔修復、卵管摘出、卵黄洗浄）、体腔洗浄（温生理食塩水）。"
            f"{extra}"
            "⑥ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h、ブプレノルフィン 0.01-0.05 mg/kg IM q12-24h、"
            "モルヒネ（亀のみ有効）0.4-1 mg/kg IM。"
            "⑦ 栄養支持: 術後はシリンジ給餌（Carnivore Care）、強制給餌は腸蠕動回復後。"
            "Mader 2019, Divers & Stahl 2019。" + _reptile_supportive(species)
        ),
        "prognosis_ja": ("早期外科治療で予後改善—診断遅延・敗血症進行例は予後不良。"),
    }


def gen_disseminated_granuloma(species: str, name_ja: str) -> Optional[dict]:
    """Disseminated granulomatous disease — multi-organ infection, predominantly reptile/amphibian."""
    species_ja = _species_label_ja_local(species)
    if species not in REPTILE and species != "amphibian":
        return None
    return {
        "treatment_ja": (
            f"{species_ja}播種性肉芽腫性疾患: ① ⚠予後不良の全身性疾患—Mycobacterium、真菌（Nannizziopsis、CANV、Chrysosporium）、"
            "寄生虫（Cryptosporidium）、Devriesea agamarum 等が原因。"
            "② 確定診断: 病変部生検＋培養（AFB染色、真菌培養、PCR）、剖検が確定的なことも多い。"
            "③ Mycobacterium疑い: ⚠人獣共通—取り扱い注意。"
            "多剤併用 6-9ヶ月: クラリスロマイシン 15 mg/kg PO q24h + リファンピシン 10 mg/kg PO q24h + "
            "エタンブトール 15 mg/kg PO q24h（爬虫類での用量は外挿、肝毒性モニタ）。"
            "感染源は安楽死も検討（公衆衛生）。"
            "④ 真菌性（Nannizziopsis/CANV）: ボリコナゾール 10 mg/kg PO q24h × 8-12週、"
            "テルビナフィン 25 mg/kg PO q24h（補助）、外科的デブリードマン併用。"
            "⑤ 支持療法: POTZ維持、栄養支持、肝保護（SAMe 20 mg/kg PO q24h、シリマリン 10 mg/kg PO q12-24h）、"
            "鎮痛（メロキシカム 0.2-0.5 mg/kg PO q24-48h）。"
            "⑥ 環境衛生: 飼育環境完全消毒（クロルヘキシジン、塩素系）、感染個体の隔離、群飼育例のスクリーニング。"
            "⑦ Mader 2019, Divers & Stahl 2019。" + _reptile_supportive(species)
        ),
        "prognosis_ja": ("播種性は予後不良—早期診断・原因特定・治療で延命可能だが治癒は困難。"),
    }


def gen_streptococcus(species: str, name_ja: str) -> Optional[dict]:
    """Streptococcal infection — common septic disease, especially Streptococcus zooepidemicus in guinea pigs."""
    species_ja = _species_label_ja_local(species)
    if species == "guinea_pig":
        return {
            "treatment_ja": (
                "モルモット連鎖球菌感染症（Streptococcus zooepidemicus 主）: ① モルモット最多細菌感染—"
                "頚部リンパ節膿瘍（lumps）、肺炎、敗血症、髄膜炎、子宮内膜炎。"
                "② 確定: 培養感受性試験、CBC（好中球増加・左方移動）、X線（肺炎時）、超音波（膿瘍評価）。"
                "③ 抗菌薬（培養感受性後）: ⚠経口ペニシリン・アンピシリン・セファロスポリン禁忌（Clostridium difficile腸炎）。"
                "推奨: トリメトプリム-スルファ 30 mg/kg PO q12h × 10-14日、エンロフロキサシン 5-10 mg/kg PO q12h、"
                "クロラムフェニコール 30-50 mg/kg PO q12h（中枢移行良）。"
                "④ 注射ペニシリン（procaine penicillin G） 22,000 IU/kg SC q24h は使用可（経口は禁忌）。"
                "⑤ 膿瘍治療: 外科的完全切除（被膜ごと）+ 病巣洗浄、抗菌薬全身投与併用。"
                "⑥ 支持療法: シリンジ給餌（Critical Care）、輸液 80-100 mL/kg/日 SC、"
                "プロバイオティクス（Lactobacillus）、ビタミンC 25-50 mg/kg q24h。"
                "⑦ 鎮痛: メロキシカム 0.5-1.5 mg/kg PO q12-24h、ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h。"
                "Quesenberry & Carpenter 2020。"
            ),
            "prognosis_ja": "リンパ節膿瘍は外科切除で予後良好、敗血症・髄膜炎合併例は予後要警戒。",
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}レンサ球菌感染症: ① 多くは S. zooepidemicus、S. pyogenes、S. agalactiae 等—"
                "リンパ節膿瘍、皮膚感染、肺炎、敗血症。"
                "② 確定: 培養感受性試験、CBC、画像診断。"
                "③ 抗菌薬: ⚠草食種は経口β-ラクタム禁忌。"
                "推奨: トリメトプリム-スルファ 30 mg/kg PO q12h × 10-14日、"
                "エンロフロキサシン 5-10 mg/kg PO/SC q12h、注射PCN（24h SC）使用可。"
                "④ 膿瘍は外科切除+全身抗菌薬。"
                "⑤ 支持療法、鎮痛、栄養補助。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "外科+抗菌薬で予後良好、敗血症は要警戒。",
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}連鎖球菌感染症: ① 鳥類—Streptococcus属（特にS. gallolyticus）—"
                "敗血症、心内膜炎、副鼻腔炎、関節炎。"
                "② 抗菌薬: アモキシシリン/クラブラン酸 125 mg/kg PO q12h、エンロフロキサシン 10-15 mg/kg PO/IM q12h、"
                "クリンダマイシン 25 mg/kg PO q12h（嫌気性カバー時）。"
                "③ 培養感受性試験で個別調整。"
                "④ 支持療法、鎮痛、栄養補助。" + _avian_supportive(species)
            ),
            "prognosis_ja": "心内膜炎・敗血症は予後不良、早期治療で改善可能。",
        }
    return None


def gen_ciliate_infection(species: str, name_ja: str) -> Optional[dict]:
    """Ciliate protozoal infection — Balantidium/Nyctotherus, often commensal in reptiles/amphibians."""
    species_ja = _species_label_ja_local(species)
    if species not in REPTILE and species != "amphibian":
        return None
    return {
        "treatment_ja": (
            f"{species_ja}繊毛虫感染症（Balantidium・Nyctotherus等）: ① 病態—大腸の常在繊毛虫が"
            "ストレス・免疫低下時に過増殖→粘液性下痢、血便、体重減少。"
            "② 確定: 新鮮糞便直接塗抹で大型繊毛虫栄養体確認、Lugol染色、PCR（種同定）。"
            "③ 治療適応: 臨床症状ある過増殖例のみ（無症状常在は治療不要）。"
            "④ 第一選択: メトロニダゾール 25-50 mg/kg PO q24-48h × 5-7日"
            "（種別代謝差大—リクガメ・トカゲ・ヘビで投与量差）。"
            "⑤ 補助: 適切な水分・温度（POTZ）、ストレス除去、清潔な飼育環境。"
            "⑥ 支持療法: 輸液（温浴+SC/ICe）、プロバイオティクス（爬虫類用、限定的）、栄養支持。"
            "⑦ 環境消毒: ケージ・水容器の徹底洗浄、糞便除去頻度増加。"
            "⑧ 群飼育例のスクリーニング、感染源確認。" + _reptile_supportive(species)
        ),
        "prognosis_ja": ("過増殖の原因（ストレス・環境不良・免疫抑制）を除去すれば予後良好。"),
    }


def gen_cloacal_calculi(species: str, name_ja: str) -> Optional[dict]:
    """Cloacal calculi — uric acid/calcium oxalate stones in reptile cloaca."""
    species_ja = _species_label_ja_local(species)
    if species not in REPTILE and species != "amphibian":
        return None
    return {
        "treatment_ja": (
            f"{species_ja}総排泄腔結石: ① 病態—脱水、高タンパク食、低Ca食、Ca補給不足、慢性腎症→"
            "総排泄腔内の尿酸塩/シュウ酸Ca結石→排便/排卵障害、テネスムス、嗜眠。"
            "② 確定: 触診、X線（不透過性）、超音波、内視鏡。"
            "③ 内科治療: 温浴 q24h × 30分（種別温度）で結石の自然排出促進、"
            "輸液療法（ノルモソルR 25-30 mL/kg/日 SC/ICe）で尿酸塩結石溶解。"
            "④ 用手摘出（小結石）: 麻酔下で潤滑剤＋鉗子/スプーン鉗子で摘出。"
            "⑤ 外科除去（大型結石）: 総排泄腔切開術（cloacotomy）—麻酔下、術後縫合・抗菌薬・POTZ維持。"
            "⑥ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h × 5-7日、"
            "ブプレノルフィン 0.01-0.05 mg/kg IM q12-24h。"
            "⑦ 食事・環境改善: 適切なタンパク量、Ca・水分豊富、温度勾配、清潔な飲水器。"
            "⑧ 基礎疾患スクリーニング: 慢性腎症、痛風、NSHP。"
            "Mader 2019, Divers & Stahl 2019。" + _reptile_supportive(species)
        ),
        "prognosis_ja": ("結石除去で予後良好、基礎疾患の管理で再発予防。"),
    }


def gen_follicular_stasis(species: str, name_ja: str) -> Optional[dict]:
    """Follicular stasis — chronic ovarian follicular retention in reptiles."""
    species_ja = _species_label_ja_local(species)
    if species not in REPTILE and species != "amphibian":
        return None
    return {
        "treatment_ja": (
            f"{species_ja}慢性濾胞停滞: ① 病態—雌爬虫類で発生する不適切な営巣条件・温度・光周期に伴う"
            "卵巣濾胞の慢性停滞→卵黄性腹膜炎・体腔炎のリスク、嗜眠、食欲不振、腹部膨満。"
            "② 確定: 超音波（多発卵胞、サイズ計測）、X線、CBC・生化学。"
            "③ 内科治療（早期・小型）: GnRHアゴニスト—ロイプロリド 100-200 μg/kg IM q14日 × 3回、"
            "デスロレリンインプラント 4.7 mg SC。hCG 50-100 IU/kg IM（卵胞排出促進）。"
            "④ 環境刺激: POTZ上限維持、光周期 12-14時間、営巣場所提供（暖湿った基質）、"
            "雄との一時的接触（種別）。"
            "⑤ 外科治療（内科無効・慢性化・体腔炎リスク）: 卵巣卵管摘出術（OE/OVH）—根治療法、"
            "麻酔下で慎重に。"
            "⑥ 周術期: 輸液、抗菌薬（セフタジジム 20 mg/kg IM q72h）、鎮痛（メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h）、"
            "POTZ維持。"
            "⑦ 術後: カルシウム補充、栄養支持、活動制限。"
            "⑧ 慢性化は卵黄性腹膜炎リスクで予後悪化。"
            "Mader 2019, Divers & Stahl 2019。" + _reptile_supportive(species)
        ),
        "prognosis_ja": ("早期外科治療で予後良好。慢性化・体腔炎合併例は予後要警戒。"),
    }


def gen_anasarca(species: str, name_ja: str) -> Optional[dict]:
    """Generalized edema — multi-cause."""
    species_ja = _species_label_ja_local(species)
    if species not in REPTILE and species != "amphibian":
        return None
    return {
        "treatment_ja": (
            f"{species_ja}全身浮腫（アナサルカ）: ① 病態—多臓器機能不全（心不全、肝不全、腎不全、低蛋白血症、敗血症）"
            "に伴う全身浮腫—予後不良サイン。"
            "② 確定原因: CBC・生化学（蛋白、ALT、BUN）、心エコー（心不全）、超音波（肝・腎）、"
            "体腔穿刺（細胞診・蛋白）、X線。"
            "③ 緊急安定化: POTZ維持、酸素（呼吸障害時）、温輸液（少量ずつ、過剰禁）。"
            "④ 利尿薬: フロセミド 2-5 mg/kg IM q12-24h（一時的、脱水・電解質モニタ）。"
            "⑤ 基礎疾患治療: 心不全→慎重な循環管理、肝不全→肝保護、腎不全→輸液管理、"
            "敗血症→広域抗菌薬（エンロフロキサシン 5-10 mg/kg IM + セフタジジム 20 mg/kg IM）。"
            "⑥ 蛋白補充: 高蛋白食、栄養支持（強制給餌）、低蛋白血症重度時はHES/アルブミンを検討。"
            "⑦ 体腔液貯留時の排液（呼吸困難時）—infection control厳重に。"
            "⑧ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h。" + _reptile_supportive(species)
        ),
        "prognosis_ja": ("多臓器不全を反映—多くで予後不良、基礎疾患の重症度で決まる。"),
    }


def gen_stress_syndrome(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species not in REPTILE and species != "amphibian":
        return None
    return {
        "treatment_ja": (
            f"{species_ja}ストレス症候群: ① 病態—不適切な飼育環境（温度・湿度・光周期・基質・隠れ家不足・過密・同居ストレス）"
            "→慢性ストレス→免疫抑制→日和見感染で致死的になりうる。"
            "② 確定: 飼育環境評価（温度勾配、UVB、湿度、ケージサイズ、エンリッチメント）、ストレス指標"
            "（体重トレンド、食欲、行動パターン、隠れ過剰）。"
            "③ 原因除去（必須）: POTZ確保（種別温度勾配、ベーシングスポット）、UVB照射"
            "（種別UVI、ランプ交換 q6ヶ月）、湿度適正化、隠れ家設置（複数）、基質改善、"
            "同居個体の見直し（攻撃的同居除去）。"
            "④ 免疫サポート: POTZ上限管理、ビタミン補給（VitC・E）、抗酸化食品。"
            "⑤ 二次感染予防: 環境衛生（毎日清掃、週次総消毒）、栄養改善。"
            "⑥ ストレス指標モニタリング: 体重 q週、食欲記録、行動観察。"
            "⑦ 慢性ストレス放置は免疫抑制→日和見感染で致死的—早期介入が鍵。"
            "Mader 2019。" + _reptile_supportive(species)
        ),
        "prognosis_ja": ("環境改善で予後良好。慢性放置は免疫抑制で日和見感染→致死的。"),
    }


def gen_abdominal_hernia(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species not in REPTILE and species != "amphibian":
        return None
    return {
        "treatment_ja": (
            f"{species_ja}腹壁ヘルニア: ① 病態—外傷、卵管/腸管脱出、先天性弱化により腹壁筋層の欠損—"
            "皮下に内臓脱出。"
            "② 確定: 触診、超音波（脱出臓器同定）、X線。"
            "③ 外科治療: ヘルニア整復＋腹壁修復（全身麻酔下、PDS 4-0/5-0で層別縫合）—"
            "緊急性は嵌頓・血流障害の有無で判断。"
            "④ 周術期: 絶食24-72時間（種別）、POTZ維持、温輸液 25-30 mL/kg/日。"
            "⑤ 麻酔: アルファキサロン 5-15 mg/kg IM/IV + イソフルラン、IPPV準備。"
            "⑥ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h × 5-7日、"
            "ブプレノルフィン 0.01-0.05 mg/kg IM q12-24h（補助）。"
            "⑦ 抗菌薬予防: エンロフロキサシン 5-10 mg/kg IM q24h × 7-10日、"
            "セフタジジム 20 mg/kg IM q72h（汚染創時）。"
            "⑧ 術後: 活動制限、創部清潔保持（POTZ・湿度管理）、栄養支持。"
            "Mader 2019。" + _reptile_supportive(species)
        ),
        "prognosis_ja": ("外科修復で予後良好—緊急嵌頓例は予後要警戒。"),
    }


def gen_drowning(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species not in REPTILE and species != "amphibian":
        return None
    return {
        "treatment_ja": (
            f"{species_ja}溺水/準溺水: ① ⚠緊急。"
            "② 初期対応: 頭部下位傾斜で口腔・気道からの水排出、気道確保、必要なら気管内挿管。"
            "③ 呼吸管理: 100%酸素投与、必要なら人工呼吸（圧迫式 1-2回/分、ヘビ/トカゲは胸郭圧迫、"
            "カメは前肢-後肢の交互圧迫）。"
            "④ 保温（必須）: POTZ維持（低体温は代謝低下→回復遅延、致死リスク）—温風器・温水パッド使用。"
            "⑤ 輸液: 等張晶質液 SC/ICe（過剰輸液は肺水腫悪化のため少量から）。"
            "⑥ 抗菌薬（誤嚥性肺炎予防）: エンロフロキサシン 5-10 mg/kg IM q24h × 7-10日、"
            "セフタジジム 20 mg/kg IM q72h（追加）。"
            "⑦ 利尿薬（肺水腫時）: フロセミド 2-5 mg/kg IM q12-24h（短期）。"
            "⑧ モニタリング: 24-48時間集中観察、呼吸音、酸素飽和度（鳥用パルスオキシメータ）。"
            "⑨ ⚠遅発性肺水腫リスク—回復後72時間は厳重観察。"
            "Mader 2019。" + _reptile_supportive(species)
        ),
        "prognosis_ja": ("軽度は回復可能、長時間水没・重度低酸素・肺水腫合併例は予後不良。"),
    }


def gen_leech_infestation(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species not in REPTILE and species != "amphibian":
        return None
    amphib_note = ""
    if species == "amphibian":
        amphib_note = "両生類は皮膚透過性高—希釈塩水浴で慎重に（過剰塩は致死）、希釈クロルヘキシジン使用。"
    return {
        "treatment_ja": (
            f"{species_ja}ヒル寄生症: ① 野外採取個体・池環境飼育例で発生—吸血により貧血、皮膚潰瘍。"
            "② 除去: 鑷子で1個体ずつ慎重に除去、または塩を局所適用（ヒルが自発離脱）。"
            "⚠強引な引き剥がしは口器残存→感染リスク。"
            "③ 創傷管理: 除去後にクロルヘキシジン 0.05%/povidone iodine 1%で洗浄、"
            "SSD（silver sulfadiazine）1% クリーム局所塗布。"
            f"④ {amphib_note}"
            "⑤ 重度寄生は PCV/Hb 確認（貧血評価）、輸液（25-30 mL/kg/日 SC/ICe）、栄養支持。"
            "⑥ 抗菌薬（感染合併）: エンロフロキサシン 5-10 mg/kg PO/IM q24h × 7-10日。"
            "⑦ 環境改善: 水源・池の清掃・消毒、新規個体の隔離・スクリーニング。"
            "⑧ 鎮痛: メロキシカム 0.2-0.5 mg/kg PO/IM q24-48h（必要時）。" + _reptile_supportive(species)
        ),
        "prognosis_ja": ("除去+環境改善で予後優良—重度貧血合併例は要支持治療。"),
    }


# ============================================================================
# Common emergency/chronic conditions — high-frequency fallback replacement
# ============================================================================


def gen_dehydration(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}脱水症の治療: ① 脱水度評価—皮膚弾力、粘膜湿潤、CRT、眼球陥凹、PCV/TS、BUN。"
                "軽度<5%、中等度5-8%、重度8-12%、ショック>12%。"
                "② 輸液製剤選択: 等張晶質液（乳酸リンゲル、ノルモソルR）が第一選択。"
                "Na異常時は0.9% NaClまたは0.45% NaCl/2.5%dextrose。"
                "③ 投与経路: 軽度はSC（30-50 mL/kg）、中等度以上はIV（推奨）またはIO。"
                "④ 用量計算: 維持量 40-60 mL/kg/日 + 不足量（体重×脱水%）+ 進行性損失。"
                "ショック時はボーラス 30-90 mL/kg IV q15-30分（再評価しつつ）。"
                "⑤ K補正: <3.5 mEq/L で20-40 mEq/L KCl添加（投与速度0.5 mEq/kg/h以下）。"
                "⑥ モニタリング: PCV/TS、尿量（>1-2 mL/kg/h目標）、体重q12-24h、肺音（過剰負荷の聴取）。"
                "⑦ 原因治療を並行: 嘔吐・下痢・多尿・高体温の制御。"
                "AAHA Fluid Therapy Guidelines 2013参照。"
            ),
            "prognosis_ja": "原疾患による。早期適切な輸液で多くは予後良好。",
        }
    if species == "horse":
        return {
            "treatment_ja": (
                "馬脱水症の治療: ① 急性疝痛・下痢・敗血症で急速進行—緊急対応。"
                "② 輸液: 等張晶質液（乳酸リンゲル）2-10 L/h IV—大型動物は短時間で大量必要。"
                "ショック時20-40 mL/kg/h、維持60-80 mL/kg/日。"
                "③ 経鼻胃管経腸液（warm isotonic electrolyte solution、3-5 L/h）は重度脱水＋IV併用で有効。"
                "④ 電解質補正: K、Na、Ca、Cl、HCO3 のモニタと補正。"
                "⑤ コロイド（ボルベン、ヘタスターチ）は重度低蛋白血症時に検討。"
                "⑥ モニタリング: PCV/TS、CVP、尿量、心拍数、血圧、乳酸。"
                "⑦ 原因治療: 疝痛は外科適応評価、下痢はC. difficile/Salmonella培養、感染症は抗菌薬。"
                + _horse_supportive(species)
            ),
            "prognosis_ja": "原因による—急性大量輸液で多くは予後改善。",
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}脱水症の治療: ① 鳥類脱水評価困難—体重、皮膚弾力、眼球陥凹、PCV/TPで判断。"
                "② 輸液製剤: 温乳酸リンゲルまたはノルモソルR、温度38-40℃。"
                "③ 投与経路: 軽度はSC（鼠径部 50-100 mL/kg/日 分割）、"
                "中等度以上はIO（脛骨近位または尺骨遠位 10-20 mL/kg q4-6h）または IV（静脈確保困難な場合多い）。"
                "④ ボーラス（ショック時）: 10 mL/kg IV/IO q5-10分まで × 3回まで。"
                "⑤ 経口は意識ある安定例のみ—シリンジまたは経口胃管。"
                "⑥ 保温30-32℃、温度勾配確保—低体温防止が代謝・吸収の前提。"
                "⑦ K補正は注意深く、Ca補正（テタニー時）50 mg/kg slow IV/IO。" + _avian_supportive(species)
            ),
            "prognosis_ja": "早期輸液+保温で予後改善。原疾患重症度で決まる。",
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}脱水症の治療: ① 評価—皮膚弾力（小型では限定的）、体重トレンド、PCV/TS、粘膜湿潤。"
                "② 輸液製剤: 温乳酸リンゲルまたはノルモソルR。"
                "③ 投与経路: 軽-中等度はSC（背中皮下 80-100 mL/kg/日 分割）、"
                "重度・ショックはIO（脛骨近位 10-20 mL/kg q4-6h）または小型でもIV試行。"
                "④ 保温（26-28℃）が吸収・代謝に必須。"
                "⑤ シリンジ給餌（Critical Care 50-90 mL/kg/日）併用で経口水分も補給。"
                "⑥ K補正注意深く、Ca補正（Hypocalcemia時）50-100 mg/kg PO/IV。"
                "⑦ 原疾患治療: 草食種のGI stasis、肉食種の嘔吐/下痢、高体温の制御。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "早期輸液+原因治療で予後改善。",
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}脱水症の治療: ① 評価—皮膚張り、眼球陥凹、PCV/TS、体重、尿量（尿酸塩濃度）。"
                "爬虫類は慢性脱水多い—代謝性疾患（痛風・腎症）合併に注意。"
                "② 輸液製剤: 温ノルモソルR、温乳酸リンゲル（38-40℃）。"
                "③ 投与経路: 軽-中等度はSC（軸下・鼡径部 25-30 mL/kg/日）、"
                "重度はICe（腹腔内、亀は前肢窩、ヘビ・トカゲは尾側1/3腹腔 25-30 mL/kg q24h）、"
                "またはIO（脛骨近位・甲羅gular bridge 10-20 mL/kg q4-6h）。"
                "④ 温浴 q24h × 20-30分（種別温度）—皮膚吸収も期待でき特に両生類で有効。"
                "⑤ POTZ維持（前後72時間以上）—吸収・代謝の前提。"
                "⑥ 経口は意識・嚥下反射ある例のみ—シリンジまたは胃管。" + _reptile_supportive(species)
            ),
            "prognosis_ja": "POTZ＋輸液で予後改善。慢性化・腎症合併例は要警戒。",
        }
    return None


def gen_seizures(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}痙攣の治療: ① 緊急安定化（active seizure）—気道確保、酸素、輸液確保、体温管理。"
                "② 初期発作中: ジアゼパム 0.5-1 mg/kg IV/IR（直腸）q5-10分まで × 3回、"
                "midazolam 0.2-0.5 mg/kg IM/IN（鼻腔内、静脈確保前に有効）。"
                "③ 持続発作（status epilepticus）: ジアゼパムCRI 0.5-2 mg/kg/h IV、"
                "phenobarbital 4-16 mg/kg IV slow（負荷量）、levetiracetam 30-60 mg/kg IV。"
                "④ 難治性: プロポフォール CRI 0.1-0.6 mg/kg/min（人工呼吸準備）、"
                "ketamine CRI 0.5-2 mg/kg/h（強直性発作）。"
                "⑤ 原因検索: 血糖、Ca、Na、肝酵素、毒物、CT/MRI、脳脊髄液検査。"
                "⑥ 慢性管理: phenobarbital 2-3 mg/kg PO q12h（血中濃度 25-35 µg/mL目標、肝酵素モニタ）、"
                "levetiracetam 20-30 mg/kg PO q8h、zonisamide 5-10 mg/kg PO q12h、"
                "bromide 20-30 mg/kg PO q24h（猫禁忌—呼吸器症状）。"
                "⑦ 高体温（>40.5℃）はクーリング+鎮静。"
                "AAHA 2015 Seizure Guidelines。"
            ),
            "prognosis_ja": ("原因による—特発性は薬物療法でコントロール可能。脳腫瘍・代謝性は原疾患による。"),
        }
    if species == "horse":
        return {
            "treatment_ja": (
                "馬痙攣の治療: ① 馬の痙攣は稀—多くは新生子（neonatal）、低Ca/低Mg、肝性脳症、頭部外傷、毒物。"
                "② 緊急: ジアゼパム 0.05-0.2 mg/kg IV slow（成馬）、0.1-0.5 mg/kg IV（仔馬）。"
                "③ 持続: midazolam 0.04-0.1 mg/kg/h CRI IV、phenobarbital 5-15 mg/kg IV slow。"
                "④ Ca補正: グルコン酸Ca 23% 250-500 mL IV slow（成馬、心電図モニタ）。"
                "⑤ 原因検索: 血糖、電解質、肝酵素、毒物、脳脊髄液。"
                "⑥ 安全確保: 厩房に詰物、観察、外傷予防。" + _horse_supportive(species)
            ),
            "prognosis_ja": "原因による—早期治療で予後改善。",
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}痙攣の治療: ① 鳥類の痙攣は重大サイン—重金属中毒（鉛・亜鉛）、低Ca、低血糖、感染（PDD、ボルナ、PCV）、頭部外傷が主因。"
                "② 緊急安定化: 保温30-32℃、酸素、安全な静置（外傷防止）。"
                "③ 抗痙攣: ジアゼパム 0.5-1 mg/kg IM、midazolam 0.2-0.5 mg/kg IM/IN、"
                "phenobarbital 1-7 mg/kg IM（血中濃度モニタ）。"
                "④ 原因治療: 鉛中毒はCa-EDTA 35 mg/kg IM q12h × 5-7日、亜鉛同様、"
                "低Caはグルコン酸Ca 50-100 mg/kg slow IV/IO、低血糖は5%デキストロース 0.25-0.5 mL/羽 IV/IO。"
                "⑤ 検査: 血液鉛・亜鉛、Ca、血糖、X線（金属異物）、PCV/TS、ボルナPCR、PDD組織生検。"
                + _avian_supportive(species)
            ),
            "prognosis_ja": "原因による—重金属・低Caは早期治療で予後良好、神経感染症は予後不良。",
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}痙攣の治療: ① 原因鑑別重要—低血糖、低Ca、肝性脳症、感染（E. cuniculi、リステリア）、頭部外傷、毒物。"
                "② 緊急: ジアゼパム 0.5-2 mg/kg IM/IV、midazolam 0.2-0.5 mg/kg IM/IN。"
                "③ 持続: phenobarbital 2-5 mg/kg IM/IV、levetiracetam 20-30 mg/kg PO/SC q8h。"
                "④ 原因治療: 低血糖は5%デキストロース slow IV、低Caはグルコン酸Ca 50-100 mg/kg slow IV、"
                "E. cuniculi疑いはfenbendazole 20 mg/kg PO q24h × 28日（ウサギ）、"
                "肝性脳症はラクツロース、Hill's l/d、ジアゼパム回避（GABA作動性悪化）。"
                "⑤ 検査: 血糖、Ca、ALT、BUN、E. cuniculi抗体、MRI。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "原因による—代謝性は治療反応良好、感染性・腫瘍性は要警戒。",
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}痙攣の治療: ① 原因鑑別—NSHP（低Ca）、低血糖、敗血症、毒物（殺虫剤、植物）、頭部外傷、感染症。"
                "② 緊急: midazolam 0.2-1 mg/kg IM、ジアゼパム 0.5-2 mg/kg IM/IV。"
                "③ Ca補正: グルコン酸Ca 100 mg/kg slow IV/ICe（NSHP痙攣で第一選択）。"
                "④ 低血糖: 5%デキストロース 10-30 mL/kg ICe/IV。"
                "⑤ 持続: phenobarbital 5-10 mg/kg IM（代謝差大、血中濃度モニタ困難）、levetiracetam 20-30 mg/kg PO。"
                "⑥ 原因検索: 血清Ca・P、血糖、肝酵素、X線（NSHP）、感染症スクリーニング、毒物履歴。"
                + _reptile_supportive(species)
            ),
            "prognosis_ja": "NSHP・低血糖は早期治療で予後良好、感染・毒物は重症度による。",
        }
    return None


def gen_hypothermia(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}低体温症の治療: ① 重症度評価—軽度32-36℃、中等度28-32℃、重度<28℃。"
                "② 加温法選択: 軽度は受動的（毛布、温暖環境）、中等度は能動的体表加温（温風器、温水パッド、Bair Hugger）、"
                "重度は能動的中心加温（温輸液 40-42℃ IV、温乳酸リンゲル胃管／温浴洗浄、温潅注）。"
                "③ 急速加温は不整脈リスク—0.5-1℃/h で漸進加温（after-drop注意）。"
                "④ 輸液: 温乳酸リンゲル 60-90 mL/kg/h IV（重度脱水例）、加温した輸液のみ。"
                "⑤ モニタリング: 心電図（心室細動・徐脈）、血糖（低血糖併発）、PCV/TS、電解質、酸塩基。"
                "⑥ 原因対処: 麻酔覚醒中、shock、敗血症、内分泌（甲状腺機能低下）、長時間屋外曝露。"
                "⑦ ⚠重度<28℃の蘇生はAHA推奨'not dead until warm and dead'—心停止例も復温まで蘇生継続。"
            ),
            "prognosis_ja": ("復温速度・原疾患・合併症で決まる。早期適切な復温で多くは予後良好。"),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}低体温症の治療: ① 鳥類は体表/体積比大—急速に低体温化、急速復温必須。"
                "正常体温39-42℃、<37℃で緊急。"
                "② 加温: ICU/インキュベーター30-32℃（重度は32-34℃）、温水パッド、温風器。"
                "③ 温輸液: 温乳酸リンゲル38-40℃ IV/IO/SC 50-100 mL/kg/日。"
                "④ 経口給餌は意識・嚥下反射回復後（誤嚥防止）。"
                "⑤ 5%デキストロース併用（低血糖併発）—10-30 mg/kg slow IV/IO。"
                "⑥ モニタリング: 体温q15-30分、呼吸、心拍、酸素飽和度。" + _avian_supportive(species)
            ),
            "prognosis_ja": "早期復温で多くは予後良好—重度遷延例は要警戒。",
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}低体温症の治療: ① 小型・体表/体積比大—急速低体温化。正常体温は種別（37-39℃）。"
                "② 加温: ICU/温風器26-30℃、温水パッド、温毛布。"
                "③ 温輸液: 温乳酸リンゲル 80-100 mL/kg/日 SC/IV、低血糖時は5%デキストロース併用。"
                "④ 急速加温は心電図異常リスク—0.5-1℃/h 漸進的に。"
                "⑤ 経口給餌は意識・嚥下反射回復後（シリンジ Critical Care 少量）。"
                "⑥ 原因検索: 麻酔覚醒中、ショック、敗血症、低栄養、長時間屋外曝露。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "早期復温で予後改善。",
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}低体温症の治療: ① 爬虫類・両生類は外温性—環境温度低下で低体温→代謝停止→免疫低下。"
                "種別POTZの最適温度に復温が必須。"
                "② 加温: 種別POTZ温度勾配で復温（急速復温は代謝過負荷で禁忌）—4-12時間かけて。"
                "③ 温浴 q24h × 20-30分（種別温度）—皮膚吸収＋復温。"
                "④ 輸液（IV/ICe）: 温度はPOTZと同等以上。"
                "⑤ POTZ復元: ベーシング温度、エアアンビエント温度、湿度、UVBの再評価。"
                "⑥ 原因対処: 加熱機器故障、停電、誤った種別温度設定。" + _reptile_supportive(species)
            ),
            "prognosis_ja": "POTZ復元で多くは予後良好—長時間低体温で免疫抑制・日和見感染に注意。",
        }
    return None


def gen_constipation(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species == "rabbit":
        return {
            "treatment_ja": (
                "ウサギ便秘/GI stasis: ① ⚠緊急—ウサギの便秘は多くがGI stasisで致死的になりうる。"
                "② 確定: 触診（盲腸の硬結・小ペレット）、X線（gas pattern）、腹部超音波。"
                "③ 鎮痛（最優先）: ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h、メロキシカム 0.5-1.5 mg/kg PO q12-24h。"
                "④ 輸液療法（必須）: 80-100 mL/kg/日 SC、重度脱水時はIV。"
                "⑤ 強制給餌: Critical Care/Recovery 50-90 mL/kg/日 を3-4分割—腸蠕動の最強の刺激。"
                "⑥ 蠕動促進薬: メトクロプラミド 0.5 mg/kg SC/PO q6-8h、シサプリド 0.5 mg/kg PO q8-12h（H2拮抗・腸蠕動促進）。"
                "⑦ 経腸誘導: ラクツロース 0.5-1 mL/kg PO q12h（柔らかい便促進）、または0.9% NaCl温胃管。"
                "⑧ ⚠経口β-ラクタム禁忌（腸内細菌叢破壊）、シメチコン使用可（ガス管理）。"
                "⑨ ケージ運動促進、新鮮チモシー牧草の常時提供、新鮮葉野菜励行、ペレット制限。"
                "Carpenter Exotic Animal Formulary 6th ed、Quesenberry 2020。"
            ),
            "prognosis_ja": ("早期介入で予後良好（72時間以内）。肝リピドーシス・敗血症合併例は予後不良。"),
        }
    if species == "guinea_pig":
        return {
            "treatment_ja": (
                "モルモット便秘/GI stasis: ① ⚠緊急—ウサギと同様に致死的。"
                "② 鎮痛: ブプレノルフィン 0.01-0.05 mg/kg SC q8-12h、メロキシカム 0.5-1.5 mg/kg PO q12-24h。"
                "③ 輸液: 80-100 mL/kg/日 SC。"
                "④ 強制給餌: Critical Care 50-90 mL/kg/日 分割、ビタミンC 25-50 mg/kg PO q24h併用。"
                "⑤ 蠕動促進: メトクロプラミド 0.5 mg/kg SC q6-8h、シサプリド 0.5 mg/kg PO q8-12h。"
                "⑥ ⚠経口ペニシリン・アンピシリン・セファロスポリン禁忌（Clostridium difficile腸炎）。"
                "⑦ 食事改善: 新鮮チモシー、葉野菜（パセリ・コリアンダー）、ペレット制限。"
                + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "早期介入で予後良好。",
        }
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}便秘/巨大結腸症の治療: ① 評価—X線（便塊量・分布）、超音波、CBC・生化学・電解質。"
                "猫は巨大結腸症（megacolon）合併多い。"
                "② 軽度: 食物繊維増量（缶ピューレ、Hill's w/d）、水分摂取促進、適度運動。"
                "③ 緩下薬: ラクツロース 0.5-1 mL/kg PO q8-12h、シサプリド 0.5 mg/kg PO q8h（猫megacolon）、"
                "MiraLAX（ポリエチレングリコール）1/4-1 tsp PO q12h。"
                "④ 浣腸: 温水浣腸（4-10 mL/kg）、無菌生理食塩水。"
                "⑤ 重度（fecal impaction）: 全身麻酔下用手摘出+多量浣腸+輸液療法。"
                "⑥ 慢性megacolon（猫）: subtotal colectomy（保存的治療無効例）—85-90%奏効率。"
                "⑦ 鎮痛: ブプレノルフィン、ガバペンチン 10-20 mg/kg PO q8-12h。"
                "AAFP 2014 Constipation Consensus。"
            ),
            "prognosis_ja": "軽度は食事・薬物で管理良好、慢性megacolonは外科で改善。",
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}便秘の治療: ① 原因鑑別—脱水、不適切食事（低繊維・基質飲み込み）、POTZ不足、腸内寄生虫、NSHP、卵管圧迫。"
                "② 確定: 触診、X線（便塊・異物）、超音波。"
                "③ 温浴: q24h × 20-30分（種別温度）—自然排便促進。"
                "④ 輸液: ノルモソルR 25-30 mL/kg/日 SC/ICe（脱水補正）。"
                "⑤ 緩下: ラクツロース 0.5 mL/kg PO q24h、ミネラルオイル 0.5-1 mL/kg PO（基質誤食時）。"
                "⑥ 蠕動促進: メトクロプラミド 0.5 mg/kg PO/IM q24h。"
                "⑦ 重度・異物: 用手摘出（鎮静下）または外科的除去。"
                "⑧ 環境改善: POTZ最適化、湿度、基質変更（吸湿性のないもの）、適切な飲水器。"
                + _reptile_supportive(species)
            ),
            "prognosis_ja": "原因除去で予後良好。",
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}便秘/総排泄腔停滞: ① 原因—脱水、骨盤腔狭窄（NSHP、卵詰まり）、腫瘍、神経損傷。"
                "② 確定: 触診、X線、超音波、CBC・生化学。"
                "③ 輸液: 温乳酸リンゲル 50-100 mL/kg/日 SC/IO。"
                "④ 用手援助: 鎮静下総排泄腔潤滑+用手摘出（ガード鉗子）。"
                "⑤ 蠕動促進: メトクロプラミド 0.5 mg/kg IM/PO q12h。"
                "⑥ 卵詰まり合併時はGnRHアゴニスト・温浴・カルシウム補正。" + _avian_supportive(species)
            ),
            "prognosis_ja": "原因除去で予後良好—腫瘍・神経損傷例は予後要警戒。",
        }
    return None


def gen_chronic_kidney_disease(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species == "cat":
        return {
            "treatment_ja": (
                "猫慢性腎臓病（CKD）の治療: ① 病期分類—IRIS stage 1-4（血清クレアチニン・SDMA・蛋白尿・血圧で評価）。"
                "② 食事療法: 低リン・適量蛋白・高EPA/DHA処方食（Hill's k/d、Royal Canin Renal、Purina NF）—最重要。"
                "③ リン制限: SDMA上昇・高P血症時にPバインダー（aluminum hydroxide 30-100 mg/kg PO q12h、"
                "lanthanum carbonate）追加—血清P 2-5 mg/dL目標。"
                "④ 高血圧管理: 収縮期>160 mmHgでアムロジピン 0.625-1.25 mg/cat PO q24h、目標<140 mmHg。"
                "⑤ 蛋白尿管理: UPC>0.4で benazepril 0.25-0.5 mg/kg PO q24h または telmisartan 1 mg/kg PO q24h。"
                "⑥ 貧血管理: HCT<20% でダルベポエチンα 0.45-1 μg/kg SC q週、鉄補給。"
                "⑦ 輸液（脱水・高窒素血症）: 乳酸リンゲルSC 100-150 mL/cat 1-7日毎（在宅可）。"
                "⑧ 制吐: マロピタント 1 mg/kg PO/SC q24h、ondansetron 0.5-1 mg/kg PO q12h。"
                "⑨ K補給: 低K血症時 potassium gluconate 2-4 mEq/cat PO q12h。"
                "⑩ ⚠ NSAIDs回避、感染症スクリーニング、定期再評価 q1-3ヶ月。"
                "IRIS 2023 Staging Guidelines, ISFM 2016 CKD Consensus。"
            ),
            "prognosis_ja": (
                "IRIS stage 1-2: MST 数年。Stage 3: MST 1-2年。Stage 4: MST 数ヶ月。早期診断・適切な管理で生存延長。"
            ),
        }
    if species == "dog":
        return {
            "treatment_ja": (
                "犬慢性腎臓病の治療: ① IRIS病期分類（SDMA・クレアチニン・蛋白尿・血圧）。"
                "② 食事療法: 低リン・適量蛋白・高EPA/DHA（Hill's k/d、Royal Canin Renal、Purina NF）。"
                "③ Pバインダー: aluminum hydroxide 30-100 mg/kg PO q12h、目標 P 2.5-4.5 mg/dL。"
                "④ 高血圧: アムロジピン 0.1-0.4 mg/kg PO q24h、目標<160 mmHg。"
                "⑤ 蛋白尿: ベナゼプリル 0.25-0.5 mg/kg PO q24h、telmisartan 1 mg/kg PO q24h。"
                "⑥ 貧血: ダルベポエチンα 0.45 μg/kg SC q週、鉄補給。"
                "⑦ 輸液: 在宅SCまたは入院IV、症状による。"
                "⑧ 制吐: マロピタント 1-2 mg/kg PO/SC q24h、ondansetron 0.5-1 mg/kg PO q12h。"
                "⑨ 定期再評価 q1-3ヶ月。"
                "IRIS 2023 Staging, AAHA 2013 CKD Guidelines。"
            ),
            "prognosis_ja": ("IRIS病期で決まる。早期介入で生存延長—stage 4は緩和ケア中心。"),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}慢性腎臓病の治療: ① 評価—BUN・クレアチニン・SDMA・尿比重・尿蛋白、超音波（腎構造）。"
                "② 食事療法: 低タンパク・低リン処方食（種別、入手可能性で）、新鮮野菜中心（草食種）。"
                "③ Pバインダー: aluminum hydroxide 30-100 mg/kg PO q12h（必要時）。"
                "④ 輸液: SC 80-100 mL/kg/日（脱水時）—在宅維持輸液有効。"
                "⑤ 高血圧（測定困難だが）: アムロジピン 0.1-0.2 mg/kg PO q24h。"
                "⑥ 蛋白尿: ベナゼプリル 0.1-0.25 mg/kg PO q24h（種別データ限定的）。"
                "⑦ 制吐: メトクロプラミド 0.5 mg/kg SC/PO q6-8h、マロピタント（試験的）。"
                "⑧ ⚠ NSAIDs回避、定期モニタ q1-3ヶ月。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "進行性—症状軽減・QOL維持が目標。",
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}慢性腎臓病の治療: ① 鳥類腎症は痛風合併が多い—評価は尿酸・血漿生化学・腎超音波。"
                "② 輸液: 50-100 mL/kg/日 SC/IO—脱水補正＋尿酸排泄促進。"
                "③ 食事: 低タンパク（12-14%）、水分豊富（果物・野菜）、ペレット主体。"
                "④ アロプリノール（痛風合併時）10-30 mg/kg PO q12-24h（種別注意）。"
                "⑤ Pバインダー: aluminum hydroxide 30-100 mg/kg PO q12h（必要時）。"
                "⑥ ⚠ ビタミンA過剰、腎毒性薬剤（aminoglycoside、NSAIDs長期）回避。" + _avian_supportive(species)
            ),
            "prognosis_ja": "進行性—早期介入で延命可能。",
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}慢性腎症の治療: ① 爬虫類腎症は脱水・高タンパク食・痛風と関連—血漿尿酸・BUN・超音波で評価。"
                "② 輸液: ノルモソルR 25-30 mL/kg/日 SC/ICe（脱水補正・尿酸排泄）、温浴 q24h。"
                "③ 食事: 低タンパク化（草食種は野菜中心、肉食種は低リン）、水分豊富。"
                "④ アロプリノール 10-20 mg/kg PO q24h（痛風合併時）。"
                "⑤ POTZ維持、湿度適正化。"
                "⑥ ⚠ NSAIDs長期回避（腎毒性）、aminoglycoside慎重投与。" + _reptile_supportive(species)
            ),
            "prognosis_ja": "進行性—早期発見・脱水管理で予後改善。",
        }
    return None


def gen_chlamydiosis(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}クラミジア症（オウム病、Chlamydia psittaci）: ① ⚠人獣共通—取扱注意（人psittacosis原因）。"
                "② 確定: PCR（咽頭・総排泄腔スワブ）、IFA、ELISA、培養（困難）。"
                "③ 第一選択: ドキシサイクリン 25-35 mg/kg PO q24h × 45日—長期治療必須。"
                "経口困難例はdoxycycline hyclate IM 75-100 mg/kg q5-7日 × 6-7回。"
                "④ 代替: アジスロマイシン 40 mg/kg PO q48h × 45日、エンロフロキサシン 15 mg/kg PO q12h × 21日（軽症）。"
                "⑤ 支持療法: 強制給餌（Emeraid Carnivore/Omnivore）、輸液 50-100 mL/kg/日 SC、保温30-32℃。"
                "⑥ 環境消毒: 1:1000ベンザルコニウム塩化、3%ホルマリン、quaternary ammonium、5%漂白剤。"
                "⑦ 隔離: 治療中・治療後2ヶ月は他鳥との接触回避。"
                "⑧ 飼主教育: 人感染リスク（インフルエンザ様症状で受診時にpsittacosis申告）、PPE使用。"
                "⑨ 都道府県保健所への届出（家畜伝染病予防法）。"
                "Compendium of Measures to Control C. psittaci, CDC/NASPHV 2017。" + _avian_supportive(species)
            ),
            "prognosis_ja": (
                "適切な抗菌薬治療（45日）で予後良好。"
                "重度感染（敗血症・肝障害）は要警戒。再発リスクあり、ストレス回避必須。"
            ),
        }
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}クラミジア感染症: ① 病原体—C. felis（猫）、C. abortus（人獣共通リスク）。"
                "② 主に結膜炎（猫）、流産（C. abortus妊娠犬）として発症。"
                "③ 確定: 結膜PCR、IFA、ELISA、培養。"
                "④ 第一選択: ドキシサイクリン 5-10 mg/kg PO q24h × 21-28日（猫の結膜炎は最低14日）、"
                "結膜病変は局所抗菌点眼（オフロキサシン）。"
                "⑤ 代替: アジスロマイシン 5-10 mg/kg PO q24h（パルス療法も可）。"
                "⑥ 妊娠犬: テトラサイクリン系は催奇性—erythromycin 10-20 mg/kg PO q8h × 14日に変更。"
                "⑦ ⚠人獣共通—特にC. abortus（妊婦の流産リスク）、衛生管理徹底。"
                "ABCD 2015 Chlamydiosis Guidelines（猫）。"
            ),
            "prognosis_ja": "早期治療で予後良好。慢性再発例は長期管理が必要。",
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}クラミジア症: ① モルモット・ウサギ・ハムスター等で結膜炎・呼吸器症状—Chlamydia psittaci/caviae。"
                "② 確定: 結膜・呼吸器スワブPCR、IFA。"
                "③ 抗菌薬: ドキシサイクリン 2.5-5 mg/kg PO q12h × 14-21日"
                "（ウサギは消化器副作用注意、enrofloxacin 5-10 mg/kg PO q12h 代替）。"
                "④ 結膜局所: ofloxacin/tetracycline点眼 q6h。"
                "⑤ ⚠人獣共通—衛生管理徹底。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "早期治療で予後良好。",
        }
    return None


def gen_aspergillosis(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}アスペルギルス症: ① 病原体—Aspergillus fumigatus（最多）、A. flavus、A. niger等の侵襲性真菌感染。"
                "免疫抑制・大気質悪化（カビ含むハウスダスト・基質）・ストレスで発症。"
                "② 確定: 内視鏡＋気嚢病変生検（gold standard）、X線/CT（肉芽腫陰影）、"
                "PCR、IgY ELISA、galactomannan ELISA（補助的）。"
                "③ 抗真菌薬（長期治療4-12ヶ月）: イトラコナゾール 5-10 mg/kg PO q12-24h（最も使用）、"
                "voriconazole 12-18 mg/kg PO q12h（重症例、種別差大—African Grayは要注意）、"
                "terbinafine 10-15 mg/kg PO q12-24h（補助）、"
                "amphotericin B 1-1.5 mg/kg IV/IT q24h（重症例）。"
                "④ 局所治療: 気管内ネブライザー（amphotericin B 1 mg/mL × 15分 q24h × 7日）、"
                "内視鏡下病変直接注入。"
                "⑤ 環境管理: HEPAフィルター、基質変更（カビ含むウッドチップ回避、紙系基質推奨）、"
                "湿度・換気適正化、定期的清掃消毒。"
                "⑥ 免疫サポート: 栄養改善（ペレット・新鮮野菜・果物）、ストレス除去、ビタミンA補給。"
                "⑦ ⚠肝酵素モニタ必須（アゾール系の肝毒性）—q4-6週。"
                "Carpenter Exotic Formulary 6th ed、Avian Medicine Principles & Application。"
                + _avian_supportive(species)
            ),
            "prognosis_ja": ("早期発見＋長期抗真菌治療で予後改善。重度気嚢病変・全身性は予後不良（>50%死亡）。"),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}アスペルギルス症: ① 不適切な飼育環境（高湿度・換気不良・カビ基質）で発症—呼吸器・皮膚感染。"
                "② 確定: 病変生検＋培養＋PCR、X線/CT。"
                "③ 抗真菌薬: イトラコナゾール 5 mg/kg PO q24h × 4-8週、"
                "voriconazole 10 mg/kg PO q24h、"
                "terbinafine 25 mg/kg PO q24h（補助）。"
                "④ 局所: 病変外科切除/デブリードマン、外用クロトリマゾール。"
                "⑤ 環境管理: 換気・湿度適正化、基質変更、清掃。"
                "⑥ 肝酵素モニタ。" + _reptile_supportive(species)
            ),
            "prognosis_ja": "早期治療で予後改善。",
        }
    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}アスペルギルス症: ① 病型—鼻腔型（最多、ドリコセファリック種好発）、"
                "播種型（免疫抑制例、A. terreus）。"
                "② 確定: 鼻腔内視鏡＋鼻腔粘膜生検＋培養、PCR、galactomannan ELISA、CT/MRI。"
                "③ 鼻腔型治療: 経鼻クロトリマゾール 1% 50-60 mL × 60分 注入（全身麻酔下）、"
                "1-2回で奏効率70-80%。"
                "④ 全身治療: イトラコナゾール 5-10 mg/kg PO q12-24h × 4-12週、"
                "voriconazole 4-5 mg/kg PO q12h（耐性例）、肝酵素モニタ。"
                "⑤ 播種型（重症）: amphotericin B+ posaconazole 経口、長期治療、予後不良。"
                "⑥ 鼻孔潰瘍管理、二次感染予防。"
                "AAHA Infectious Disease Guidelines。"
            ),
            "prognosis_ja": "鼻腔型は局所治療で予後良好。播種型は予後不良。",
        }
    return None


def gen_cardiomyopathy(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    if species == "cat":
        return {
            "treatment_ja": (
                "猫心筋症の治療: ① 病型—HCM（最多 14.7%、Ragdoll/MCO好発）、RCM、DCM、ARVC、unclassified。"
                "② 確定: 心エコー（左室壁厚>6mm でHCM）、NT-proBNP（>270 pmol/L 心疾患示唆）、Tn-I。"
                "③ 無症候期: 経過観察＋6-12ヶ月毎心エコー。"
                "④ 心不全症状（うっ血性心不全）: フロセミド 1-4 mg/kg PO/IM/SC q8-12h（個別調整）、"
                "ピモベンダン 0.5-1 mg/kg PO q12h（収縮機能低下時）、ベナゼプリル 0.25-0.5 mg/kg PO q24h。"
                "⑤ 血栓予防（左房拡張>15-16mm、SEC、ATE既往）: クロピドグレル 18.75 mg/cat PO q24h"
                "（FATCAT試験で有効）、リバロキサバン 2.5 mg/cat PO q24h（補助）。"
                "⑥ HCMの不整脈/頻脈: アテノロール 6.25-12.5 mg/cat PO q12-24h、ジルチアゼム 7.5 mg/cat PO q8h。"
                "⑦ ATE（大動脈血栓塞栓症）: 緊急疼痛管理（ブプレノルフィン）、抗凝固（dalteparin 100-150 IU/kg SC q12h）、"
                "tPA は限定的—温熱保護、リハビリ。"
                "ACVIM 2020 HCM Consensus、AAFP 2024。"
            ),
            "prognosis_ja": (
                "無症候HCM: MST 5+年。心不全発症: MST 9-18ヶ月。ATE発症: MST 2-12ヶ月。"
                "早期発見・薬物療法・血栓予防で生存延長。"
            ),
        }
    if species == "dog":
        return {
            "treatment_ja": (
                "犬心筋症（DCM主）の治療: ① 病型—DCM（ドーベルマン・大型犬好発）、"
                "拡張型ARVC（ボクサー）、栄養関連（grain-free食、タウリン欠乏）。"
                "② 確定: 心エコー（拡張+収縮機能低下）、NT-proBNP、Tn-I、ホルター心電図。"
                "③ Occult期: ピモベンダン 0.25-0.5 mg/kg PO q12h（PROTECT試験）、ベナゼプリル 0.25-0.5 mg/kg PO q24h。"
                "④ うっ血性心不全: ピモベンダン+フロセミド 1-4 mg/kg PO q8-12h+ベナゼプリル、"
                "スピロノラクトン 1-2 mg/kg PO q12h（補助）。"
                "⑤ 心房細動: ジルチアゼム 1.5-3 mg/kg PO q8h、ジゴキシン 0.003-0.005 mg/kg PO q12h（血中濃度0.5-1 ng/mL）。"
                "⑥ 心室性不整脈: ソタロール 1-3 mg/kg PO q12h、メキシレチン 5-8 mg/kg PO q8h。"
                "⑦ 栄養性DCM: タウリン補給 500-1000 mg PO q12h、L-カルニチン 50-100 mg/kg PO q8h、"
                "grain-free食の中止。"
                "ACVIM 2009 DCM Consensus、Adin 2018 grain-free。"
            ),
            "prognosis_ja": ("Occult期: MST 2-3年。CHF発症: MST 6-12ヶ月。栄養性で食事改善+タウリン補給は予後改善。"),
        }
    if species == "ferret":
        return {
            "treatment_ja": (
                "フェレット心筋症の治療: ① 病型—DCM（最多、中-高齢）、HCM稀。"
                "② 確定: 心エコー、CBC・生化学、X線（肺水腫評価）、心電図。"
                "③ うっ血性心不全: フロセミド 1-4 mg/kg PO q12h、ピモベンダン 0.25-0.5 mg/kg PO q12h、"
                "ベナゼプリル 0.25-0.5 mg/kg PO q24h。"
                "④ タウリン補給 250 mg PO q12-24h（栄養性疑い）。"
                "⑤ 高血圧管理: アムロジピン 0.625-1.25 mg PO q24h。"
                "⑥ モニタリング: 体重、呼吸数、エネルギー、食欲、定期心エコー q3-6ヶ月。"
                + _small_mammal_supportive(species)
            ),
            "prognosis_ja": "DCMは進行性—薬物療法で延命可能、MST 6-12ヶ月。",
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}心筋症: ① 鳥類—アテローム性心臓病・DCM・心嚢液貯留が多い。"
                "好発: アフリカン・グレイ、Amazon、コザクラ等。"
                "② 確定: 心エコー（経胸壁または経静脈）、X線（心拡大）、ECG、生化学（Tn-I）。"
                "③ 治療: フロセミド 1-2 mg/kg PO/IM q12h、エナラプリル 1.25-2.5 mg/kg PO q24h、"
                "ピモベンダン 0.25 mg/kg PO q12h（試験的—鳥種別データ限定）。"
                "④ アテローム関連: 低脂肪食、L-カルニチン、運動増加、ストレス除去。"
                "⑤ 心嚢液貯留: 超音波ガイド穿刺、原因治療。" + _avian_supportive(species)
            ),
            "prognosis_ja": "進行性—早期介入で延命可能。",
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}心筋症: ① 爬虫類の心筋症は稀—多くは慢性脱水・寄生虫・腫瘍性の二次性。"
                "② 確定: 心エコー、X線、CBC・生化学。"
                "③ 治療: フロセミド 2-5 mg/kg IM q12-24h（短期）、エナラプリル 0.25-0.5 mg/kg PO q24h（試験的）。"
                "④ POTZ維持、ストレス除去、栄養支持。" + _reptile_supportive(species)
            ),
            "prognosis_ja": "進行性—緩和ケア中心が現実的。",
        }
    if species == "horse":
        return {
            "treatment_ja": (
                "馬心筋症の治療: ① 病型—idiopathic（稀）、毒物（fumonisin、白カビ、ライグラス）、"
                "感染（EHV、ボルナ）、ビタミンE/セレン欠乏。"
                "② 確定: 心エコー、Tn-I、ECG、運動負荷検査、心臓MRI。"
                "③ 心不全: フロセミド 1-3 mg/kg IV/PO q12h、ジゴキシン 0.0022-0.0044 mg/kg PO q12h（モニタ）、"
                "エナラプリル 0.5 mg/kg PO q12-24h。"
                "④ ビタミンE/セレン補給（欠乏例）: VitE 5000 IU PO q24h、Se 0.06 mg/kg。"
                "⑤ 不整脈管理: キニジン（心房細動）、リドカイン（心室性）。"
                "⑥ 運動制限、ストレス除去。" + _horse_supportive(species)
            ),
            "prognosis_ja": "原因による—栄養性は治療可能、特発性は予後不良。",
        }
    return None


# ============================================================================
# Endocrine "Others" multi-species placeholder (replaces 「種特異的治療が必要」 template)
# ============================================================================


def gen_candidiasis(species: str, name_ja: str) -> Optional[dict]:
    """Candida infections — distinct from dermatophytes; nystatin/fluconazole based.
    Common sites: oral (thrush), GI, urinary, systemic in immunocompromised.
    """
    species_ja = _species_label_ja_local(species)
    nm = name_ja or ""

    is_oral = "口腔" in nm or "Oral" in nm or "thrush" in nm.lower()
    is_systemic = "全身" in nm or "敗血" in nm or "播種" in nm
    is_gi = "胃腸" in nm or "腸" in nm or "GI" in nm or "腸炎" in nm or "嘔吐" in nm or "下痢" in nm

    # Determine clinical context block
    if is_oral:
        context = "口腔カンジダ症（thrush）—白斑性プラーク・グラム陰性炎症性肉芽腫を伴う。"
    elif is_systemic:
        context = "全身性カンジダ症—免疫不全・長期抗菌薬・カテーテル留置で発症、致死率高い。"
    elif is_gi:
        context = "消化管カンジダ症—下痢・嘔吐・体重減少、特に幼若・免疫抑制動物。"
    else:
        context = f"{species_ja}カンジダ症—皮膚・粘膜・全身に発症、免疫低下が誘因。"

    if species in DOG_CAT:
        return {
            "treatment_ja": (
                f"{species_ja}カンジダ症の治療: ① {context}"
                "② 確定: 培養（Sabouraud寒天）、組織生検（PAS染色で偽菌糸・菌体）、"
                "PCR、KOH直接鏡検、CBC・生化学（基礎免疫不全評価）。"
                "③ 局所治療: ニスタチン経口懸濁液 100,000 IU/mL を 0.25-1.0 mL PO q6-8h × 7-14日"
                "（経口・GI カンジダで第一選択、吸収されないので全身副作用少）、"
                "またはクロトリマゾール1%軟膏 q12h（皮膚・外陰）、"
                "ミコナゾール2%軟膏 q12h（皮膚）。"
                "④ 全身治療: フルコナゾール 5-10 mg/kg PO q24h × 4-6週（GI・全身・尿路）、"
                "イトラコナゾール 5 mg/kg PO q24h × 4-6週（代替）、"
                "アムホテリシンB 0.5 mg/kg IV q48h（重症全身、腎毒性モニタ必須）。"
                "⑤ 基礎免疫不全治療: 糖尿病管理、ステロイド減量、長期抗菌薬の見直し。"
                "⑥ 環境: 哺乳瓶・食器・ケージの煮沸消毒、新鮮水給水。"
                "⑦ モニタ: 肝酵素 q2-4週（アゾール療法中）、改善まで臨床評価 q1-2週。"
            ),
            "prognosis_ja": (
                "局所感染は適切治療で予後良好、全身性カンジダ症は致死率20-50%—早期診断・"
                "高用量抗真菌薬・基礎免疫不全治療が予後を決定する。"
            ),
        }
    if species in SMALL_MAMMAL:
        return {
            "treatment_ja": (
                f"{species_ja}カンジダ症の治療: ① {context}"
                "幼若個体・抗菌薬使用後・免疫抑制で発症しやすい。"
                "② 確定: 口腔・皮膚スワブKOH/培養、糞便培養（GI型）、CBC・生化学。"
                "③ 局所治療: ニスタチン経口懸濁液 50,000-100,000 IU/動物 PO q8h × 7-14日（経口・GI）、"
                "クロトリマゾール1%軟膏 q12h（皮膚・粘膜）。"
                "④ 全身治療: フルコナゾール 10-20 mg/kg PO q24h × 4-6週（全身性のみ）、"
                "草食種ではアゾール系の長期投与で食欲低下に注意（プロバイオ併用）。"
                "⑤ 基礎管理: 不適切抗菌薬使用の見直し、ストレス除去、栄養改善。" + _small_mammal_supportive(species)
            ),
            "prognosis_ja": ("局所感染は予後良好、全身型は予後注意。基礎免疫不全の管理が成功の鍵。"),
        }
    if species in AVIAN:
        return {
            "treatment_ja": (
                f"{species_ja}カンジダ症（thrush、moniliasis）の治療: ① そ嚢・口腔・GI でC. albicans感染、"
                "幼鳥（雛）に多い—そ嚢内白斑・粘液性そ嚢液、食滞、嘔吐、消化不良。"
                "成鳥は免疫抑制（PBFD、PDD、長期抗菌薬、不適切栄養）で発症。"
                "② 確定: そ嚢洗浄液KOH/グラム染色（出芽酵母・偽菌糸）、培養（Sabouraud）、PCR。"
                "③ 局所治療: ニスタチン経口懸濁液 100,000 IU/羽 PO q8h × 7-14日（第一選択）、"
                "投与は強制給餌チューブで直接そ嚢へ。"
                "④ 全身治療（重症・難治性）: フルコナゾール 10-15 mg/kg PO q24h × 14-21日、"
                "ケトコナゾール 30 mg/kg PO q12h（代替）。"
                "⑤ そ嚢洗浄: 重症例は鎮静下で滅菌生食でそ嚢洗浄・残留物除去。"
                "⑥ 食事改善: ペレット食への切替、新鮮水（毎日交換）、ヨーグルト/プロバイオ。"
                "⑦ 環境: 哺乳器具消毒（次亜塩素酸1:32）、繁殖期は親鳥のスクリーニング。"
                "Harrison & Lightfoot Clinical Avian Medicine 2006; Speer Current Avian Therapy 4th ed。"
                + _avian_supportive(species)
            ),
            "prognosis_ja": (
                "雛のそ嚢カンジダ症は適切治療で予後良好、全身性・PBFD/PDD合併例は予後ガード、基礎免疫不全の管理が必要。"
            ),
        }
    if species in REPTILE or species == "amphibian":
        return {
            "treatment_ja": (
                f"{species_ja}カンジダ症の治療: ① 稀だが免疫抑制・不適切POTZ・抗菌薬使用で発症—"
                "口腔・皮膚・GI感染、両生類では皮膚浅表性。"
                "② 確定: 病変スワブKOH/培養、組織生検（PAS染色）、PCR。"
                "③ 局所治療: ニスタチン経口懸濁液 100,000 IU/kg PO q12h × 14日、"
                "ミコナゾール/クロトリマゾール局所 q12h（皮膚）。"
                "④ 全身治療: イトラコナゾール 5 mg/kg PO q24h × 4-6週、"
                "フルコナゾール 5-10 mg/kg PO q24h（代替）。"
                "⑤ 環境改善: POTZ最適化（免疫機能の基盤）、清浄度向上、湿度適正化。" + _reptile_supportive(species)
            ),
            "prognosis_ja": ("原因除去（POTZ・栄養）で予後良好、全身性・免疫不全合併は予後注意。"),
        }
    return None


def gen_sporotrichosis(species: str, name_ja: str) -> Optional[dict]:
    """Sporotrichosis — dimorphic fungus (Sporothrix schenckii complex), zoonotic.
    Cats are the most affected mammal and zoonotic source.
    """
    if species == "cat":
        return {
            "treatment_ja": (
                "猫スポロトリックス症（Sporothrix schenckii complex）: ⚠**人獣共通感染症**—"
                "猫は最も感染しやすく、人への感染源として最重要（特にS. brasiliensis）。"
                "獣医師・飼い主の手指感染を防ぐため、診察時手袋・予防衣着用必須。"
                "① 病態—外傷からの感染（多くは喧嘩・ひっかき傷）、皮膚結節・潰瘍・リンパ管性散布、"
                "全身型では肺・骨・中枢神経に進展、未治療では致死的。"
                "② 確定: 病変からの細胞診（酵母様・葉巻型菌体）、培養（Sabouraud、25-30℃でカビ相、35-37℃で酵母相）、"
                "組織生検（GMS染色）、PCR、被嚢菌型確認。"
                "③ 第一選択: イトラコナゾール 10 mg/kg PO q24h（食後）× 病変消失後+1ヶ月（通常3-6ヶ月）、"
                "肝酵素 q4週モニタリング、奏効率60-90%。"
                "④ 第二選択: ヨウ化カリウム飽和液（SSKI）20 mg/kg PO q12h（食事と共に）— "
                "胃刺激・甲状腺機能低下・流涎・嘔吐が副作用、忍容性で減量。"
                "⑤ 重症・全身型: アムホテリシンB 0.25-0.5 mg/kg IV q48h（リポソーマル製剤推奨、腎毒性監視）、"
                "ヨウ化カリウムとの併用も。"
                "⑥ 局所外科: 限局性病変の切除、温熱療法（40-42℃、Sporothrix熱感受性）。"
                "⑦ 隔離: 治療中・治癒判定（培養2回連続陰性）まで他猫・人との接触制限。"
                "AAFP/ISFM 2018; Larsson Vet Microbiol 2020 (Brazilian epidemic)。"
            ),
            "prognosis_ja": (
                "皮膚限局型は治療6-12ヶ月で60-90%治癒、全身型・骨・中枢神経合併は予後不良。"
                "治療中断で再発、感染源として人獣共通リスクが続く。"
            ),
        }
    if species == "dog":
        return {
            "treatment_ja": (
                "犬スポロトリックス症: 猫より稀、皮膚・皮下結節・リンパ管型が主。"
                "① 確定: 細胞診・培養・組織生検・PCR。"
                "② 第一選択: イトラコナゾール 5-10 mg/kg PO q24h × 病変消失後+1ヶ月、"
                "ヨウ化カリウム 40 mg/kg PO q24h（食事と共に、犬では忍容性比較的良好）。"
                "③ 局所: 温熱療法、限局病変の外科切除。"
                "④ ⚠人獣共通—診察時の感染予防（手袋・予防衣）。"
                "Lecuyer et al. Vet Dermatol 2018。"
            ),
            "prognosis_ja": ("適切治療で予後良好、全身型は予後ガード。"),
        }
    if species == "horse":
        return {
            "treatment_ja": (
                "馬スポロトリックス症: リンパ管型が多い（皮膚結節の鎖状連結）。"
                "① 第一選択: ヨウ化ナトリウム 20-40 mg/kg IV週1-2回 × 4-6週、"
                "またはヨウ化カリウム 1-2 g PO q24h × 4-8週。"
                "② 代替: イトラコナゾール 3-5 mg/kg PO q24h × 4-6週。"
                "③ 切除可能病変は外科的切除。"
                "④ ⚠人獣共通—診察時の感染予防。" + _horse_supportive(species)
            ),
            "prognosis_ja": ("限局型は適切治療で予後良好。"),
        }
    return None


def gen_blood_disorder(species: str, name_ja: str) -> Optional[dict]:
    """Hematology disorders: anemia, thrombocytopenia, DIC, hemolysis, polycythemia, splenomegaly,
    hemorrhagic syndromes. Replaces the cross-species "血液異常の基礎原因の特定と対処" template
    with disorder-specific evidence-based guidance per species.
    """
    species_ja = _species_label_ja_local(species)
    nm = name_ja or ""

    # Determine which blood disorder this is — specific subtypes first
    if "新生子溶血" in nm or "新生児溶血" in nm or "neonatal iso" in nm.lower():
        disorder = "neonatal_iso"
    elif "エストロゲン" in nm or "高エストロゲン" in nm:
        disorder = "estrogen_aplastic"
    elif "馬伝染性貧血" in nm or "EIA" in nm:
        disorder = "eia"
    elif "ヘモプラズマ" in nm or "haemominutum" in nm or "haemofelis" in nm or "伝染性貧血" in nm or "感染性貧血" in nm:
        disorder = "hemoplasmosis"
    elif "溶血性尿毒症" in nm or "HUS" in nm:
        disorder = "hus"
    elif "鉄欠乏" in nm:
        disorder = "iron_deficiency"
    elif "コニュア" in nm and "出血" in nm:
        disorder = "conure_hemorrhagic"
    elif any(kw in nm for kw in ("DIC", "播種性血管内凝固")):
        disorder = "dic"
    elif "溶血" in nm:
        disorder = "hemolysis"
    elif "血小板減少" in nm:
        disorder = "thrombocytopenia"
    elif "赤血球増加" in nm or "多血" in nm:
        disorder = "polycythemia"
    elif "脾腫" in nm or "脾臓腫大" in nm:
        disorder = "splenomegaly"
    elif "出血" in nm:
        disorder = "hemorrhage"
    elif "貧血" in nm or "Anemia" in nm or "anemia" in nm:
        disorder = "anemia"
    elif "血液疾患" in nm:
        disorder = "anemia"  # treat generic "blood disease" as workup-driven approach
    else:
        return None

    # Species-class specific supportive care
    if species in SMALL_MAMMAL:
        support = _small_mammal_supportive(species)
        transfuse_note = (
            "輸血: 同種輸血が理想（事前クロスマッチ）—ウサギ・モルモットでは少量（5-10 mL/kg, 10 mL/kg/h）"
            "を緩徐に。ドナーは同種・同居の健常個体から採血（最大体重の1%）。"
        )
    elif species in DOG_CAT:
        support = _dogcat_supportive(species)
        if species == "cat":
            transfuse_note = (
                "輸血: 全血または濃厚赤血球 10-20 mL/kg IV（4-6時間かけて）。"
                "猫は必ず血液型判定（A/B/AB）—不適合輸血は致死的（特にB型レシピエント）。"
                "DEA・血液型サイドカード使用、クロスマッチ推奨。"
            )
        else:
            transfuse_note = (
                "輸血: 濃厚赤血球 6-10 mL/kg または全血 10-20 mL/kg IV（4-6時間）。"
                "初回輸血はクロスマッチ陰性なら血液型判定なしで可能だが、2回目以降は必須（DEA 1.1）。"
            )
    elif species in AVIAN:
        support = _avian_supportive(species)
        transfuse_note = (
            "輸血: 鳥類は赤血球寿命短く（28-35日）輸血効果は限定的（数日のみ）。"
            "緊急時に同種全血 10-20 mL/kg IO/IV を 4-6時間かけて。ドナーは健常個体から最大体重の1%採血。"
        )
    elif species in REPTILE or species == "amphibian":
        support = _reptile_supportive(species)
        transfuse_note = (
            "輸血: 爬虫類では輸血の臨床的エビデンス限定的。重度貧血では同種全血を試みる場合あり"
            "（5-10 mL/kg IO/IV）が、POTZ最適化・原因除去を優先。"
        )
    else:
        support = "支持療法: 種に適切な輸液・栄養・酸素化・温度管理を行う。"
        transfuse_note = "輸血: 種特異的なドナー選択とクロスマッチを行う。"

    if disorder == "estrogen_aplastic":
        return {
            "treatment_ja": (
                f"{species_ja}エストロゲン誘発性再生不良性貧血: ① 病態—未去勢雌フェレットの持続発情で"
                "高エストロゲンが骨髄を非可逆的に抑制—汎血球減少、致死的。"
                "発情が10日以上持続する個体はリスク高。"
                "② 確定: 病歴（未去勢・発情持続・外陰膨大）、CBC（汎血球減少: PCV <15%、血小板 <50,000、好中球減少）、"
                "塗抹（網赤血球低値）、エストラジオール上昇、骨髄穿刺（骨髄低形成・脂肪置換）。"
                "③ 排卵誘起（早期介入で骨髄回復可能性あり）: hCG 100 IU IM 単回（外陰膨大が72時間以内に消失することを確認、"
                "効果不十分なら7日後反復）、または GnRH（buserelin）1.5 µg/動物 IM 単回—排卵させエストロゲンを下げる。"
                "④ 持続発情予防の根本治療: 卵巣子宮全摘出（OHE）—骨髄回復後（または準緊急で）に施行。"
                "デスロレリン徐放インプラント（4.7 mg SC）は薬学的去勢として有効、6-12ヶ月作用。"
                "⑤ 重度汎血球減少: 新鮮全血輸血 6-12 mL/kg IV/IO（同種ドナーフェレット、血液型判定不要だがクロスマッチ望ましい）、"
                "重度好中球減少（<500/µL）には予防的広域抗菌薬。"
                "⑥ サポートとしてエリスロポエチン製剤（ダーベポエチン 1 µg/kg SC q週）試行可。"
                "⑦ モニタ: CBC q3-7日、骨髄回復には4-12週要、PCV >25%回復を目標。"
                "Quesenberry & Carpenter Ferrets 3rd ed; Lewington 2007。" + support
            ),
            "prognosis_ja": (
                "PCV >25%なら骨髄回復可能性高い、PCV <15%（特に <10%）は予後極めて不良"
                "（死亡率50-90%）。早期介入と速やかなOHEが救命の鍵。発症予防には繁殖計画外の雌は早期OHE。"
            ),
        }

    if disorder == "neonatal_iso":
        if species == "cat":
            return {
                "treatment_ja": (
                    "猫新生子溶血性疾患（FNI、新生子赤血球溶解症）: ① 病態—B型母猫のA/AB型新生子が"
                    "初乳中の抗A抗体（自然抗体）を吸収して溶血—生後12-72時間で発症。"
                    "Type B多発品種: ブリティッシュショートヘア、デボンレックス、コーニッシュレックス、トルコバン、ペルシャ。"
                    "② 予防が最重要—妊娠/分娩前に母猫の血液型判定（A/B/AB）。B型母猫×A型雄の場合、生まれた子猫は全て"
                    "出生から24時間は隔離・人工哺乳（初乳禁、KMR等の代替）、24時間後から通常授乳。"
                    "③ 発症した子猫の救命: 母乳離脱（直ちに）、保温（30-32℃）、適切な人工哺乳（KMR 1 mL/30 g BW q2-4h）、"
                    "重症（PCV <15%、ヘモグロビン尿、虚脱）には洗浄赤血球輸血（同型A型ドナーまたはO型代替）2-5 mL IO/IV。"
                    "④ 軽症は支持療法とモニタで自然回復可能、重症は1-3日で死亡することが多い。"
                    "⑤ 母猫の管理: 次回交配前に雄を再選定（A型雄に変更）。"
                    "AAFP Feline Blood Type Guidelines; Casal 2008 J Feline Med Surg。"
                ),
                "prognosis_ja": (
                    "予防（出生24時間人工哺乳）で罹患回避可能。発症例は重症度による—軽症は回復、"
                    "重症（虚脱・尿黒色化・PCV <10%）は致死率50-90%。"
                ),
            }
        if species == "horse":
            return {
                "treatment_ja": (
                    "馬新生子溶血性疾患（NI、新生駒赤血球溶解症）: ① 病態—Aa/Qa血液型不一致の繁殖で、"
                    "母馬が前産・輸血で感作され、初乳中の抗体が新生駒を溶血。生後12-48時間で発症。"
                    "経産母馬・輸血歴のある母馬・ロバ×馬交配（ミュール）でリスク高。"
                    "② 予防: 妊娠280-300日に母馬血清と父馬赤血球で凝集試験 → 陽性なら出産前準備。"
                    "代替初乳（他のNI陰性母馬または市販Equicolostrum）給与、または出生直後母乳禁止＋免疫グロブリン代替。"
                    "③ 発症した新生駒の救命: 直ちに授乳停止、初乳代替（バンクされた他母馬初乳または"
                    "市販製品 1-2 L PO q4h × 24h）、生後24時間後は通常授乳再開可能。"
                    "重症例（PCV <15%、虚脱、ヘモグロビン尿、黄疸）には洗浄赤血球輸血（父馬以外のドナー、"
                    "母馬血清と非凝集ドナー）8-12 mL/kg IV、または濃厚赤血球。"
                    "④ 支持療法: 等張輸液 4-6 mL/kg/h IV、保温、IgG確認（>800 mg/dL）、"
                    "腎機能保護（ヘモグロビン尿による尿細管障害予防）。"
                    "⑤ 次産での予防: 父馬変更または代替初乳プロトコル準備。"
                    "MacLeay 2001 Equine Vet J; Becht 1985 JAVMA。" + _horse_supportive(species)
                ),
                "prognosis_ja": (
                    "早期発見・初乳遮断と適切な輸血で予後改善（生存率60-80%）、"
                    "発見遅延・重度溶血では致死率高い。次産では予防プロトコル必須。"
                ),
            }
        # Other species fallback: route to generic hemolysis section
        disorder = "hemolysis"

    if disorder == "eia":
        return {
            "treatment_ja": (
                "馬伝染性貧血（EIA、Equine Infectious Anemia）: ⚠**国内法定届出伝染病**—診断確定で即時届出。"
                "① 病態—EIAウイルス（レトロウイルス科Lentivirus）による生涯持続感染、"
                "アブ・サシバエの機械的伝播、子宮内伝播、輸血感染。"
                "急性期（発熱・血小板減少・貧血）→慢性期（再燃性発熱・体重減少）→不顕性キャリア。"
                "② 確定診断: Coggins試験（AGID、世界基準）—国際輸送・販売時必須。"
                "ELISA（迅速、感度高い）と確認試験の併用が現在は標準。"
                "急性期はPCR陽性、抗体は感染後14-45日で陽転。"
                "③ ⚠**治療法なし**—感染馬は生涯ウイルス保有、感染源として隔離または安楽死が原則。"
                "農林水産省告示に従い、確定例は届出後、隔離（200 m以上他馬から、虫除けスクリーニング）または殺処分。"
                "④ 群管理: 同居馬の検査（Coggins陰性確認）、消毒（吸血昆虫対策）、ピレスロイド系塗布。"
                "感染馬の使用器具・針は専用化し、共有禁止。"
                "⑤ 国際馬輸送: 出発前30-180日のCoggins陰性証明必須。"
                "MAFF 馬伝染性貧血対策要綱; OIE Terrestrial Manual; Sellon Equine Infectious Diseases 2nd ed。"
                + _horse_supportive(species)
            ),
            "prognosis_ja": (
                "治癒不可能。生涯キャリア（不顕性または再燃性）として隔離管理または淘汰。"
                "急性期重症例は致死的、慢性期は数年以上生存可能だが感染源となる。"
            ),
        }

    if disorder == "hemoplasmosis":
        if species == "cat":
            return {
                "treatment_ja": (
                    "猫ヘモプラズマ症（Mycoplasma haemofelis, Candidatus M. haemominutum, M. turicensis）: "
                    "① 病態—赤血球膜に付着する細胞壁欠損細菌、ノミ・吸血昆虫・輸血媒介、FeLV/FIV合併で重症化。"
                    "M. haemofelis が最病原性（重度溶血性貧血）、他2種は軽度。"
                    "② 確定: PCR（種別同定、最も感度・特異度高い）、塗抹（Wright-Giemsa染色で赤血球辺縁の"
                    "リング/コンマ状菌体—感度低）、Coombs試験（しばしば陽性）、FeLV/FIVスクリーニング併行。"
                    "③ 第一選択抗菌薬: ドキシサイクリン 10 mg/kg PO q24h × 21-28日（水と共に投与—食道狭窄予防）、"
                    "またはマルボフロキサシン 2.75 mg/kg PO q24h × 14日（迅速効果、ドキシ不耐例）。"
                    "プラジカンテルは無効。"
                    "④ 重度貧血（PCV <15%、虚脱）: 全血輸血 10-20 mL/kg IV（血液型判定とクロスマッチ必須）。"
                    "⑤ 免疫介在性溶血合併: プレドニゾロン 1-2 mg/kg PO q12h（Coombs陽性または改善鈍化時）。"
                    "⑥ 重症例には酸素化、輸液、栄養管理。"
                    "⑦ 治療後もPCR陽性が持続（不顕性キャリア化）—臨床改善で十分、再燃時に再治療。"
                    "ABCD 2018 Guidelines; AAFP 2020 Feline Retrovirus Guidelines。"
                ),
                "prognosis_ja": (
                    "M. haemofelis急性期は適切治療で生存率70-90%、無治療は致死率高い。"
                    "他種は軽症で予後良好。FeLV/FIV併発は予後悪化。"
                ),
            }
        # Other species fallback
        disorder = "hemolysis"

    if disorder == "hus":
        species_specific = ""
        if species == "dog":
            species_specific = (
                "犬HUS（Greyhound急性皮膚血管症 CRGV/'Alabama rot'）: シガ毒素産生大腸菌（STEC）誘発、"
                "皮膚潰瘍＋急性腎不全＋微小血管症性溶血性貧血。"
            )
        elif species == "horse":
            species_specific = "馬HUS: 大腸菌・サルモネラ感染や黒くるみ中毒で発症—溶血＋急性腎不全＋血小板減少。"
        return {
            "treatment_ja": (
                f"{species_ja}溶血性尿毒症症候群（HUS）の治療: ① 病態—志賀毒素産生細菌（STEC O157:H7, Stx2）または"
                "他の血管内皮損傷で微小血管症性溶血性貧血（MAHA）＋急性腎不全＋血小板減少の三徴。"
                f"{species_specific}"
                "② 確定: 塗抹で破砕赤血球（schistocyte >10%）、CBC（PCV低下、血小板 <100,000）、"
                "生化学（BUN/Cre上昇、LDH上昇、ハプトグロビン低下）、糞便培養（STEC PCR・Stx）、"
                "Coombs陰性、補体（C3, CH50）測定（aHUS鑑別）。"
                "③ 集中支持療法: 等張輸液で循環維持（過剰輸液回避—腎不全悪化）、"
                "電解質・酸塩基管理、利尿不全には透析（腹膜透析または血液透析、可能な施設で）。"
                "④ 輸血: 重度貧血には洗浄赤血球（PRBC 6-10 mL/kg IV、ゆっくり投与）、血小板輸血は"
                "活動性出血時のみ（消費を促進するため通常は避ける）。"
                f"{transfuse_note} "
                "⑤ 抗菌薬: STEC感染では抗菌薬がStx放出を増加させHUS悪化させうるため慎重—培養感受性で個別判断、"
                "アジスロマイシンは比較的安全。"
                "⑥ 補体阻害薬（エクリズマブ）: 非典型HUS（aHUS）で人医エビデンスあり、獣医適応外使用は限定的。"
                "⑦ モニタ: 腎機能 q12-24h、血小板・PCV・LDH、尿量、血圧。" + support
            ),
            "prognosis_ja": (
                "犬CRGV（Alabama rot）は致死率70-90%と極めて不良、"
                "STEC合併症は早期透析支援で生存率改善（30-70%）。回復例も慢性腎症リスク残存。"
            ),
        }

    if disorder == "iron_deficiency":
        species_specific = ""
        if species == "horse":
            species_specific = "馬では稀（出血性原因が多い）—鉄欠乏よりも慢性失血や寄生虫を疑う。"
        elif species in SMALL_MAMMAL:
            species_specific = "小型哺乳類では子犬子猫期や繁殖期母体に多い—栄養性または寄生虫性。"
        return {
            "treatment_ja": (
                f"{species_ja}鉄欠乏性貧血の治療: ① 病態—慢性失血（GI出血・寄生虫・出血性腫瘍）、"
                "鉄摂取不足（離乳期・成長期）、鉄吸収障害が主因。"
                "小球性低色素性貧血（MCV低下、MCHC低下）が特徴。"
                f"{species_specific}"
                "② 確定: CBC（小球性低色素性貧血、網赤血球反応性）、血清鉄・TIBC（鉄飽和度 <20%）、"
                "フェリチン低値（鉄貯蔵枯渇）、糞便潜血、寄生虫検査、消化管検査（出血源同定）、"
                "塗抹（標的細胞、楕円赤血球、Heinz小体なし）。"
                "③ 原因除去: 出血源治療（GI腫瘍切除、寄生虫駆除—フェンベンダゾール 50 mg/kg PO q24h × 3日）。"
                "④ 鉄補充療法: 経口硫酸第一鉄 4-6 mg/kg PO q24h × 4-8週（食事と分けて空腹時投与—吸収↑）、"
                "重症例または経口不耐には鉄デキストラン 10-20 mg/kg IM 単回（アナフィラキシー注意、テストドーズ推奨）。"
                "⑤ 食事: 鉄豊富食（赤身肉、肝臓、貝類、緑黄色野菜）、ビタミンC併用で吸収促進、"
                "コーヒー・茶・カルシウム剤は同時投与回避（吸収阻害）。"
                "⑥ モニタ: 網赤血球 q2週（治療開始7-10日でピーク）、CBC q4週、フェリチン q3ヶ月。"
                "鉄補給は貯蔵鉄回復まで4-6ヶ月継続。" + support
            ),
            "prognosis_ja": (
                "原因除去と適切な鉄補給で予後良好—4-6週でPCV正常化、6ヶ月で完全回復。"
                "出血源が制御できない場合は反復治療要。"
            ),
        }

    if disorder == "conure_hemorrhagic":
        return {
            "treatment_ja": (
                "コニュア出血症候群（Conure Bleeding Syndrome、CBS）: "
                "① 病態—未解明、ビタミンK欠乏症またはカルシウム代謝異常が関連と推定—"
                "繰り返す自発性出血（皮下・口腔・腸管）、塗抹で形態異常の血小板。"
                "ナンデイコニュア、コガネメキシコインコ、ジャンデーコニュアで報告多。"
                "② 確定: 臨床所見（再発性出血エピソード、血腫）、CBC（軽度貧血、血小板可変）、"
                "凝固系（PT延長、aPTT正常）、生化学（Ca低下例あり）、"
                "鉛・亜鉛中毒除外（X線で重金属検出）、肝機能、糞便潜血。"
                "③ 治療: ビタミンK1 0.2-2.5 mg/kg IM/SC 急性期 q12h × 3日→PO維持 q24h、"
                "カルシウム補給（経口グルコン酸カルシウム 50-100 mg/kg q12h、注射用は重症時）、"
                "出血エピソードには局所止血（圧迫、フェリック硫酸）。"
                "④ 食事改善: ペレット食への切替（VK含有）、緑黄色野菜・小松菜・パセリ、"
                "種子主体を脱却。"
                "⑤ 環境: 紫外線ライト（D3合成・Ca代謝促進）、止まり木の高さ調整（出血時転落防止）。"
                "⑥ モニタ: 出血エピソード頻度、CBC・凝固系 q1-3ヶ月。"
                "Harrison & Lightfoot Clinical Avian Medicine 2006; Carpenter Exotic Animal Formulary 6th ed。"
                + _avian_supportive(species)
            ),
            "prognosis_ja": (
                "適切な食事改善・ビタミンK補給で多くは寛解、再発予防には終生の食事管理が必要。重症急性出血は致死的。"
            ),
        }

    if disorder == "anemia":
        return {
            "treatment_ja": (
                f"{species_ja}貧血の治療: ① 病因鑑別が最重要—失血性（外傷・寄生虫・GI出血）、"
                "溶血性（免疫介在性・感染・酸化障害）、非再生性（慢性疾患・腎性・骨髄抑制）の3型に分類。"
                "② 確定検査: CBC＋網赤血球数（再生性 vs 非再生性鑑別）、塗抹標本（球状赤血球・"
                "ハインツ小体・血液寄生虫）、生化学（BUN/Cre・肝酵素）、Coombs試験（IMHA疑い）、"
                "尿検査（ヘモグロビン尿）、超音波（脾腫・腹腔内出血）、感染症スクリーニング。"
                "③ 急性失血の場合: 出血源同定と止血（外科・圧迫・薬物）。"
                "PCV <15%（犬猫）/<20%（草食種）または症候性低血圧では輸血を検討。"
                f"{transfuse_note} "
                "④ 慢性失血（GI出血・寄生虫）: 原因治療＋鉄補給"
                "（鉄デキストラン 10-20 mg/kg IM 単回、または硫酸鉄 4-6 mg/kg PO q24h）。"
                "⑤ 溶血性: 免疫介在性疑いではプレドニゾロン 1-2 mg/kg PO q12h、改善後3-6ヶ月で漸減。"
                "感染性（バベシア・マイコプラズマ・ヘモプラズマ）には特異的抗微生物薬。"
                "⑥ 非再生性: 腎性貧血→エリスロポエチン製剤（ダーベポエチン 1 µg/kg SC q週、"
                "鉄補給併用）、骨髄抑制→原因薬剤中止・骨髄生検・支持療法。"
                "⑦ モニタ: 24-48時間ごとPCV、網赤血球、塗抹で治療反応評価。" + support
            ),
            "prognosis_ja": (
                "再生性貧血で原因除去可能なら予後良好。免疫介在性は適切治療で寛解可能だが再燃あり。"
                "非再生性（特に骨髄性）は予後ガード、慢性腎性貧血は基礎疾患のステージに依存。"
            ),
        }

    if disorder == "thrombocytopenia":
        return {
            "treatment_ja": (
                f"{species_ja}血小板減少症の治療: ① 病因鑑別—免疫介在性（ITP/IMTP）、感染性（"
                "エールリヒア・アナプラズマ・FeLV・FIV・RHDV2・敗血症）、薬剤性、消費性（DIC）、"
                "産生不全（骨髄抑制）、希釈性（大量輸液後）。"
                "② 確定検査: CBC＋塗抹（凝集除外、巨大血小板の有無）、生化学、凝固系（PT/aPTT、"
                "Dダイマー）、感染症PCR、抗血小板抗体（可能なら）、骨髄穿刺/生検（産生不全評価）、"
                "腹部超音波（脾腫・出血）。"
                "③ 緊急止血: 血小板<30,000/µLで重度出血時は新鮮全血または血小板濃厚液輸血"
                "（10 mL/kg IV、半減期5-7日）。"
                f"{transfuse_note} "
                "④ 免疫介在性: プレドニゾロン 2 mg/kg PO q12h（犬猫）/0.5-1 mg/kg q24h（馬は限定使用）、"
                "重症例ではビンクリスチン 0.02 mg/kg IV 単回 or ヒト免疫グロブリン（IVIG）0.5-1 g/kg IV、"
                "難治例はミコフェノール酸モフェチル 10 mg/kg PO q12h。"
                "⑤ 感染性: 特異的治療（ドキシサイクリン 5-10 mg/kg PO q12h × 28日 for エールリヒア/アナプラズマ）。"
                "⑥ 出血予防: 安静、外傷回避、IM注射・静脈穿刺最小限、ヘパリン/NSAIDs禁忌。"
                "⑦ モニタ: 血小板数 q24-48h、安定後は週1回。" + support
            ),
            "prognosis_ja": (
                "免疫介在性は寛解率70-85%（犬）、再燃あり生涯管理。"
                "感染性は原因除去で予後良好。骨髄性・腫瘍随伴は予後ガード。"
            ),
        }

    if disorder == "dic":
        return {
            "treatment_ja": (
                f"{species_ja}播種性血管内凝固（DIC）の治療: ① DICは独立した疾患ではなく、"
                "重症基礎疾患（敗血症・腫瘍・熱射病・膵炎・外傷・蛇咬傷）に続発する症候群—"
                "基礎疾患制御が最優先で、これなくしてDICは治癒しない。"
                "② 確定: 血小板減少＋PT/aPTT延長＋Dダイマー上昇＋フィブリノーゲン低下（または逆に高値=代償期）"
                "＋抗トロンビンIII低下、塗抹で破砕赤血球（schistocyte）。"
                "ISTH DICスコア≥5で診断（人医基準を獣医に応用）。"
                "③ 基礎疾患治療: 敗血症→感受性ベース広域抗菌薬・敗血症ガイドラインに沿った蘇生（"
                "晶質液 60-90 mL/kg/h、目標MAP>65、乳酸クリアランス）。腫瘍→外科・化学療法。"
                "膵炎→絶食・輸液・鎮痛。"
                "④ 凝固因子補充: 新鮮凍結血漿（FFP）10-20 mL/kg IV q6-12h で凝固因子・AT補充、"
                "重度血小板減少は血小板輸血または新鮮全血。"
                "⑤ 抗凝固療法: 低分子ヘパリン（エノキサパリン 0.8-1 mg/kg SC q12h、抗Xaモニタ）"
                "—出血傾向と血栓形成のバランスを慎重に判断、低凝固期は禁忌。"
                f"{transfuse_note} "
                "⑥ 支持療法: 輸液・酸素化・電解質補正・腎機能保護（dopamine 微量CRI、利尿薬）。"
                "⑦ モニタ: 4-6時間ごとPT/aPTT・血小板・乳酸・尿量、改善傾向で漸減。" + support
            ),
            "prognosis_ja": (
                "予後は基礎疾患制御の成否に依存—制御可能なら回復可能だが、"
                "進行例・敗血症性ショック合併では死亡率50-80%と高い。"
            ),
        }

    if disorder == "hemolysis":
        return {
            "treatment_ja": (
                f"{species_ja}溶血性疾患の治療: ① 病型鑑別が治療方針を決める—免疫介在性溶血性貧血（IMHA）、"
                "感染性（バベシア・マイコプラズマ・ヘモプラズマ・RHDV2/3 for rabbits）、"
                "酸化障害性（タマネギ・ニンニク・アセトアミノフェン・亜鉛中毒）、機械的（DIC・心血管疾患）、"
                "遺伝性（ピルビン酸キナーゼ欠損症等）。"
                "② 確定: CBC＋網赤血球増加、塗抹（球状赤血球・ハインツ小体・Howell-Jolly体・寄生虫体・破砕赤血球）、"
                "Coombs試験、感染症PCR、生化学（ビリルビン・LDH・ハプトグロビン）、尿（ヘモグロビン尿）。"
                "③ 緊急輸血: PCV <15%（犬）/<12%（猫）または症候性は輸血適応。"
                f"{transfuse_note} "
                "④ IMHA: プレドニゾロン 2 mg/kg PO q12h × 2-4週後漸減、難治例にミコフェノール酸モフェチル 10 mg/kg PO q12h、"
                "ヒト免疫グロブリン 0.5-1 g/kg IV、シクロスポリン 5 mg/kg PO q12h。"
                "血栓塞栓予防にクロピドグレル 1-2 mg/kg PO q24h（IMHAは血栓リスク高）。"
                "⑤ 感染性: バベシア→イミドカルブ 6.6 mg/kg IM 2回（14日間隔）、"
                "マイコプラズマ→ドキシサイクリン 5-10 mg/kg PO q12h × 4-6週。"
                "⑥ 酸化障害性: 原因物質除去、活性炭、N-アセチルシステイン 140 mg/kg IV 初回→70 mg/kg q6h（パラセタモール中毒時）。"
                "⑦ モニタ: PCV・網赤血球・ビリルビン q12-24h、安定後週1回。" + support
            ),
            "prognosis_ja": (
                "IMHA死亡率30-70%（最初の2週が最重症）、感染性は治療反応良好。"
                "中毒性は早期除染で予後良好、遺伝性は管理疾患として終生対応。"
            ),
        }

    if disorder == "polycythemia":
        return {
            "treatment_ja": (
                f"{species_ja}赤血球増加症（多血症）の治療: ① 病型鑑別—相対性（脱水）、絶対性原発性（真性多血症 PV）、"
                "絶対性二次性（慢性低酸素症—心疾患・肺疾患・高地、エリスロポエチン産生腫瘍—腎癌・肝癌）。"
                "② 確定: HCT >65%（犬）/>55%（猫）/種特異的高値、CBC、塗抹、血清EPO値（PVで低値、二次性で高値）、"
                "胸腔・腹腔の画像（心臓・肺・腎・肝の評価）、動脈血ガス（低酸素症評価）、骨髄生検（PV確診）。"
                "③ 脱水性（相対性）: 等張輸液で補正、HCT低下を確認。"
                "④ 二次性低酸素症: 基礎疾患治療（心疾患→ピモベンダン、肺疾患→気管支拡張薬・酸素）—"
                "代償性赤血球増加は完全には正常化しないが基礎疾患制御を優先。"
                "⑤ 真性多血症（PV）: 治療的瀉血（10-20 mL/kg、目標HCT <60%、等量輸液置換）q2-4週、"
                "ヒドロキシ尿素 30 mg/kg PO q24h × 7日 → 15 mg/kg PO q24h 維持で骨髄抑制、CBCモニタ。"
                "⑥ 過粘稠症候群（神経症状・血栓・出血）: 緊急瀉血、補液で粘度低下、低分子ヘパリン併用検討。"
                "⑦ モニタ: HCT q2-4週、肝腎機能、神経症状の有無。" + support
            ),
            "prognosis_ja": (
                "相対性（脱水）は補正で予後良好、二次性は基礎疾患による、PVは適切治療で中央生存期間2-5年（犬）。"
            ),
        }

    if disorder == "splenomegaly":
        return {
            "treatment_ja": (
                f"{species_ja}脾腫の治療: ① 脾腫は独立疾患ではなく、原因鑑別が必須—"
                "鬱血性（門脈圧亢進・心不全・脾捻転）、増殖性（リンパ腫・血管肉腫・MCT・髄外造血）、"
                "感染性（マイコプラズマ・エールリヒア・バベシア・FIV・FeLV・敗血症）、"
                "免疫介在性（IMHA・SLE・脾過誤腫）、薬剤性（バルビツール酸長期）。"
                "② 確定: 触診・超音波（びまん性 vs 結節性、血管系評価）、CBC・生化学・凝固系、"
                "塗抹（血液寄生虫・腫瘍細胞）、感染症PCR・抗体、"
                "脾穿刺/針生検（細胞診—リンパ腫・MCT・髄外造血鑑別）、CT（病期評価・血管造影）。"
                "③ 緊急脾捻転: 緊急脾摘出術—腹部膨満・低血圧・乳酸上昇・心不全合併で死亡率高い。"
                "④ 腫瘍性（血管肉腫・リンパ腫）: 脾摘出＋化学療法（血管肉腫はDoxorubicin、リンパ腫はCHOP）、"
                "破裂例は緊急輸血＋外科。"
                f"{transfuse_note} "
                "⑤ 感染性: ドキシサイクリン 5-10 mg/kg PO q12h × 28日（リケッチア・マイコプラズマ）、"
                "イミドカルブ（バベシア）。"
                "⑥ 鬱血性: 基礎疾患治療（心不全→ピモベンダン・利尿、門脈圧亢進→原因対処）。"
                "⑦ モニタ: 4-8週毎の超音波と血液検査、腫瘍例は転移評価。" + support
            ),
            "prognosis_ja": (
                "原因による—感染性・鬱血性は基礎疾患制御で改善、"
                "脾血管肉腫（犬）は中央生存3-6ヶ月と予後不良、リンパ腫は化学療法反応性で改善可能。"
            ),
        }

    if disorder == "hemorrhage":
        return {
            "treatment_ja": (
                f"{species_ja}出血症候群の治療: ① 病因鑑別—一次性止血障害（血小板減少・血小板機能不全・"
                "vWD）、二次性（凝固因子欠損—肝疾患・ビタミンK欠乏・抗凝固薬中毒・先天性血友病）、"
                "血管脆弱（外傷・血管炎・敗血症）。"
                "② 確定: CBC＋血小板、塗抹、凝固系（PT/aPTT・Dダイマー・フィブリノーゲン）、"
                "頬粘膜出血時間（BMBT、一次止血評価）、vWF測定、肝機能、毒物検査（殺鼠剤）。"
                "③ 緊急止血: 圧迫・止血剤（フェリック硫酸・ハイドロコロイド剤）、外科的結紮。"
                "ショック例には輸液＋輸血（重度出血で大量出血プロトコル）。"
                f"{transfuse_note} "
                "④ ビタミンK拮抗性殺鼠剤中毒: ビタミンK1 2.5-5 mg/kg PO/SC q12h × 14-42日"
                "（製剤により期間調整、PT正常化後さらに2週継続）、新鮮凍結血漿 10-20 mL/kg IV（PT延長時）。"
                "⑤ 肝性凝固障害: FFP補充、UDCA、肝保護薬、肝原疾患治療。"
                "⑥ 血友病: 反復FFP・濃厚血漿輸血で因子補充。先天性vWDではDDAVP 1 µg/kg SC（type 1）。"
                "⑦ 血小板機能不全: 抗血小板薬中止（クロピドグレル・アスピリン）、新鮮血小板輸血。"
                "⑧ モニタ: PT/aPTT・PCV・血小板 q6-12h（急性期）。" + support
            ),
            "prognosis_ja": (
                "ビタミンK拮抗中毒は早期治療で予後良好、肝性は基礎疾患による、先天性血友病は管理疾患として生涯対応。"
            ),
        }

    return None


# ============================================================================
# Endocrine "Others" multi-species placeholder (replaces 「種特異的治療が必要」 template)
# ============================================================================


def gen_endocrine_others(species: str, name_ja: str) -> Optional[dict]:
    species_ja = _species_label_ja_local(species)
    nm = name_ja or ""
    # This is a generic "endocrine - other" placeholder; produce a unique signature
    return {
        "treatment_ja": (
            f"{species_ja}における{nm}: 内分泌軸の特定が治療方針を決める—基礎ホルモン値＋負荷試験（"
            "ACTH刺激、TRH刺激、dex抑制等）で機能評価。"
            "① 検査: CBC・生化学・尿検査、内分泌スクリーニング（甲状腺、副腎、性腺、下垂体）、"
            "画像（超音波・CT・MRI）で腺腫/過形成/腫瘍鑑別。"
            "② 機能性腫瘍は外科的切除または核医学的アブレーション（I-131等）が根治的選択。"
            "③ 薬物療法: 機能亢進→抑制（メチマゾール、トリロスタン、ミトタン）、機能低下→補充（レボチロキシン、コルチゾール、インスリン）—"
            "ホルモン値モニタで個別調整 q4-8週。"
            "④ 二次性合併症（糖尿病、骨粗鬆症、心筋症、高血圧、感染易罹患性）の併発スクリーニングと管理。"
            "⑤ 長期管理: 3-6ヶ月毎のホルモン値・全身状態評価、用量見直し。"
            "⑥ 種特異的考慮（フェレット副腎疾患、馬PPID/EMS、鳥甲状腺腫等）に注意。" + _supportive_block(species)
        ),
    }


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
    # === Phase 2 — new generators ===
    # Viral diseases (pathogen-specific)
    ("パルボウイルス", gen_viral_disease),
    ("汎白血球減少", gen_viral_disease),
    ("ジステンパー", gen_viral_disease),
    ("カリシ", gen_viral_disease),
    ("ヘルペスウイルス", gen_viral_disease),
    ("コロナウイルス", gen_viral_disease),
    ("ロタウイルス", gen_viral_disease),
    ("ポックス", gen_viral_disease),
    ("パピローマ", gen_viral_disease),
    ("アデノウイルス", gen_viral_disease),
    ("インフルエンザ", gen_viral_disease),
    ("パラインフルエンザ", gen_viral_disease),
    ("狂犬病", gen_viral_disease),
    ("ボルナ", gen_viral_disease),
    ("ノロウイルス", gen_viral_disease),
    ("ウイルス性疾患", gen_viral_disease),
    ("ウイルス感染", gen_viral_disease),
    ("VHD", gen_viral_disease),
    # Bacterial pathogens (organism-specific)
    ("サルモネラ", gen_bacterial_named),
    ("大腸菌", gen_bacterial_named),
    ("コリバクテリア", gen_bacterial_named),
    ("ブドウ球菌", gen_bacterial_named),
    ("クレブシエラ", gen_bacterial_named),
    ("緑膿菌", gen_bacterial_named),
    ("クロストリジウム", gen_bacterial_named),
    ("パスツレラ", gen_bacterial_named),
    # Mycobacteriosis
    ("マイコバクテリア症", gen_mycobacteriosis),
    ("マイコバクテリウム", gen_mycobacteriosis),
    ("結核", gen_mycobacteriosis),
    # Vestibular
    ("前庭疾患", gen_vestibular),
    ("前庭症候群", gen_vestibular),
    ("斜頸", gen_vestibular),
    # Encephalitis
    ("脳炎", gen_encephalitis),
    # Peripheral neuropathy
    ("末梢神経障害", gen_peripheral_neuropathy),
    ("ニューロパチー", gen_peripheral_neuropathy),
    ("多発性神経炎", gen_peripheral_neuropathy),
    # Flagellate
    ("鞭毛原虫", gen_flagellate),
    ("トリコモナス", gen_flagellate),
    ("ジアルジア", gen_flagellate),
    ("ヘキサミタ", gen_flagellate),
    # Hepatic disease (must come AFTER 肝リピドーシス since it's broader)
    ("肝リピドーシス", gen_hepatic_disease),
    ("肝細菌感染", gen_hepatic_disease),
    ("肝寄生虫", gen_hepatic_disease),
    ("肝線維症", gen_hepatic_disease),
    ("肝炎", gen_hepatic_disease),
    ("肝症", gen_hepatic_disease),
    # Dermatitis variants
    ("脱毛症", gen_dermatitis),
    ("ストレス性脱毛", gen_dermatitis),
    ("皮膚膿瘍", gen_dermatitis),
    ("バンブルフット", gen_dermatitis),
    ("足底皮膚炎", gen_dermatitis),
    ("Pododermatitis", gen_dermatitis),
    ("接触性皮膚炎", gen_dermatitis),
    ("アレルギー性皮膚", gen_dermatitis),
    ("皮膚アレルギー", gen_dermatitis),
    ("皮膚細菌感染", gen_dermatitis),
    ("皮膚寄生虫", gen_dermatitis),
    ("皮膚自己免疫", gen_dermatitis),
    ("慢性皮膚炎", gen_dermatitis),
    ("潰瘍性皮膚炎", gen_dermatitis),
    ("皮膚炎", gen_dermatitis),
    # Fractures
    ("骨折", gen_fracture),
    ("Fracture", gen_fracture),
    ("嘴外傷", gen_fracture),
    ("嘴損傷", gen_fracture),
    ("頭部外傷", gen_fracture),
    # Generic endocrine "Others"
    ("内分泌系", gen_endocrine_others),
    ("代謝性疾患（複数種）", gen_endocrine_others),
    # === Phase 5 — Blood/hematology disorders (Jun 2026) ===
    # These conditions previously shared a generic "血液異常の基礎原因の特定と対処" template;
    # gen_blood_disorder produces disorder-specific (anemia/DIC/IMHA/etc.) content per species.
    ("貧血", gen_blood_disorder),
    ("Anemia", gen_blood_disorder),
    ("血小板減少", gen_blood_disorder),
    ("Thrombocytopenia", gen_blood_disorder),
    ("播種性血管内凝固", gen_blood_disorder),
    ("DIC", gen_blood_disorder),
    ("溶血", gen_blood_disorder),
    ("Hemolytic", gen_blood_disorder),
    ("赤血球増加", gen_blood_disorder),
    ("多血", gen_blood_disorder),
    ("Polycythemia", gen_blood_disorder),
    ("脾腫", gen_blood_disorder),
    ("Splenomegaly", gen_blood_disorder),
    ("出血症候群", gen_blood_disorder),
    ("血液疾患", gen_blood_disorder),
    # Subtype routing (must be present so lookup matches names that don't include 貧血)
    ("ヘモプラズマ", gen_blood_disorder),
    ("haemofelis", gen_blood_disorder),
    ("haemominutum", gen_blood_disorder),
    ("Mycoplasma haem", gen_blood_disorder),
    ("猫感染性貧血", gen_blood_disorder),
    ("猫伝染性貧血", gen_blood_disorder),
    ("馬伝染性貧血", gen_blood_disorder),
    ("EIA", gen_blood_disorder),
    ("新生子溶血", gen_blood_disorder),
    ("新生児溶血", gen_blood_disorder),
    ("溶血性尿毒症", gen_blood_disorder),
    ("HUS", gen_blood_disorder),
    ("コニュア出血", gen_blood_disorder),
    ("エストロゲン中毒", gen_blood_disorder),
    ("高エストロゲン血症", gen_blood_disorder),
    # === Phase 3 — Neoplasia & nutritional & exotic syndromes ===
    # Neoplasia (must come before broader "腫瘍" matches if added)
    ("脂肪腫", gen_lipoma),
    ("Lipoma", gen_lipoma),
    ("メラノーマ", gen_melanoma),
    ("黒色腫", gen_melanoma),
    ("Melanoma", gen_melanoma),
    ("リンパ腫", gen_leukemia_lymphoma),
    ("白血病", gen_leukemia_lymphoma),
    ("Lymphoma", gen_leukemia_lymphoma),
    # Gout — avian/reptile
    ("痛風", gen_gout),
    ("Gout", gen_gout),
    # Nutritional Secondary Hyperparathyroidism / MBD
    ("栄養性二次性副甲状腺機能亢進症", gen_nshp_mbd),
    ("栄養性骨異栄養症", gen_nshp_mbd),
    ("代謝性骨疾患", gen_nshp_mbd),
    ("MBD", gen_nshp_mbd),
    # Hypervitaminoses
    ("ビタミンA過剰症", gen_hypervitaminosis_a),
    ("ビタミンA中毒", gen_hypervitaminosis_a),
    ("ビタミンD3過剰症", gen_hypervitaminosis_d3),
    ("ビタミンD過剰", gen_hypervitaminosis_d3),
    # Vitamin deficiencies (must come AFTER 過剰症 to avoid wrong match)
    ("ビタミンA欠乏症", gen_vitamin_a_deficiency),
    ("VitA欠乏", gen_vitamin_a_deficiency),
    ("ビタミンE欠乏症", gen_vitamin_e_deficiency),
    ("VitE欠乏", gen_vitamin_e_deficiency),
    ("チアミン欠乏症", gen_thiamine_deficiency),
    ("ビタミンB1欠乏", gen_thiamine_deficiency),
    # Iron Storage Disease
    ("鉄蓄積症", gen_iron_storage_disease),
    ("ヘモクロマトーシス", gen_iron_storage_disease),
    ("Iron Storage", gen_iron_storage_disease),
    # Myiasis
    ("蝿蛆症", gen_myiasis),
    ("ハエウジ症", gen_myiasis),
    ("Myiasis", gen_myiasis),
    # Mucormycosis (must NOT match general fungal)
    ("ムコール症", gen_mucormycosis),
    ("Mucormycosis", gen_mucormycosis),
    ("接合菌症", gen_mucormycosis),
    # Candidiasis — distinct from dermatophytes; needs nystatin/fluconazole content
    ("カンジダ", gen_candidiasis),
    ("Candida", gen_candidiasis),
    ("Candidiasis", gen_candidiasis),
    ("thrush", gen_candidiasis),
    ("カンジダ症", gen_candidiasis),
    # Sporotrichosis — zoonotic dimorphic fungus, cats are major source
    ("スポロトリックス", gen_sporotrichosis),
    ("スポロトリコ", gen_sporotrichosis),
    ("Sporothrix", gen_sporotrichosis),
    ("Sporotrichosis", gen_sporotrichosis),
    # Muscle wasting / cachexia
    ("筋萎縮", gen_muscle_wasting),
    ("悪液質", gen_muscle_wasting),
    ("Cachexia", gen_muscle_wasting),
    # Reptile/amphibian shared exotic syndromes (species-tailored details)
    ("腹膜炎・体腔炎", gen_reptile_coelomitis),
    ("卵関連体腔炎", gen_reptile_coelomitis),
    ("体腔炎", gen_reptile_coelomitis),
    ("播種性肉芽腫性疾患", gen_disseminated_granuloma),
    ("肉芽腫性疾患", gen_disseminated_granuloma),
    ("連鎖球菌感染症", gen_streptococcus),
    ("レンサ球菌感染症", gen_streptococcus),
    ("Streptococcus", gen_streptococcus),
    ("繊毛虫感染症", gen_ciliate_infection),
    ("繊毛虫過増殖症", gen_ciliate_infection),
    ("Balantidium", gen_ciliate_infection),
    ("総排泄腔結石", gen_cloacal_calculi),
    ("Cloacal calculi", gen_cloacal_calculi),
    ("慢性濾胞停滞", gen_follicular_stasis),
    ("濾胞停滞", gen_follicular_stasis),
    ("Follicular stasis", gen_follicular_stasis),
    ("全身浮腫", gen_anasarca),
    ("全身性浮腫", gen_anasarca),
    ("アナサルカ", gen_anasarca),
    ("ストレス症候群", gen_stress_syndrome),
    ("Stress syndrome", gen_stress_syndrome),
    ("腹壁ヘルニア", gen_abdominal_hernia),
    ("溺水", gen_drowning),
    ("Drowning", gen_drowning),
    ("ヒル寄生", gen_leech_infestation),
    ("Leech", gen_leech_infestation),
    # === Phase 4 — high-frequency common conditions ===
    # Dehydration (universal supportive care)
    ("脱水", gen_dehydration),
    ("Dehydration", gen_dehydration),
    # Seizures (emergency)
    ("痙攣", gen_seizures),
    ("発作", gen_seizures),
    ("てんかん", gen_seizures),
    ("Seizure", gen_seizures),
    # Hypothermia (emergency)
    ("低体温", gen_hypothermia),
    ("Hypothermia", gen_hypothermia),
    # Constipation / GI stasis
    ("便秘", gen_constipation),
    ("GI stasis", gen_constipation),
    ("消化管うっ滞", gen_constipation),
    ("Constipation", gen_constipation),
    ("巨大結腸", gen_constipation),
    # Chronic kidney disease
    ("慢性腎臓病", gen_chronic_kidney_disease),
    ("慢性腎症", gen_chronic_kidney_disease),
    ("CKD", gen_chronic_kidney_disease),
    ("Chronic Kidney", gen_chronic_kidney_disease),
    # Chlamydiosis
    ("クラミジア", gen_chlamydiosis),
    ("オウム病", gen_chlamydiosis),
    ("Chlamydia", gen_chlamydiosis),
    ("Psittacosis", gen_chlamydiosis),
    # Aspergillosis
    ("アスペルギルス", gen_aspergillosis),
    ("Aspergillus", gen_aspergillosis),
    # Cardiomyopathy
    ("心筋症", gen_cardiomyopathy),
    ("Cardiomyopathy", gen_cardiomyopathy),
    ("HCM", gen_cardiomyopathy),
    ("DCM", gen_cardiomyopathy),
]


# Anti-patterns: if any of these appear in name_ja, the corresponding generator
# must NOT be selected (prevents false-positive substring matches like
# "副甲状腺機能亢進症" matching the thyroid generator).
_GENERATOR_EXCLUSIONS: dict[str, list[str]] = {
    "甲状腺機能亢進症": ["副甲状腺", "Hyperparathyroid"],
    "甲状腺機能低下症": ["副甲状腺"],
    "甲状腺腫": ["副甲状腺"],
    "甲状腺疾患": ["副甲状腺"],
    "甲状腺過形成": ["副甲状腺"],
    "肝炎": ["伝染性肝炎"],  # canine infectious hepatitis is viral, handled by viral generator
    # Vitamin deficiency vs. excess must not cross-match
    "ビタミンA欠乏症": ["過剰", "中毒", "過敏"],
    "ビタミンA過剰症": ["欠乏"],
    "ビタミンE欠乏症": ["過剰", "中毒"],
    "ビタミンD3過剰症": ["欠乏"],
    "ビタミンD過剰": ["欠乏"],
    # NSHP — exclude primary hyperparathyroidism
    "栄養性二次性副甲状腺機能亢進症": ["原発性", "腺腫"],
    # Coelomitis — egg-related has its own dedicated entry, but both use same generator
    "体腔炎": [],
    # Myiasis — don't catch nephritis containing wrong substring
    # (no exclusion needed — "蝿蛆症" is highly specific)
    # Streptococcus — don't catch e.g. "Streptococcus equi" via 連鎖球菌 unless guinea-pig (handled inside)
    # (no exclusion — generic Streptococcus generator gracefully handles cross-species)
    # Lipoma — don't catch "脂肪肝" or "脂肪織炎"
    "脂肪腫": ["肝", "織炎", "腺", "壊死"],
    # Leukemia/Lymphoma must avoid lymphangitis, lymphadenitis (not neoplastic)
    "リンパ腫": [],  # exact match, no ambiguity
    "白血病": ["白血球減少", "白血球増多"],  # exclude leukopenia/leukocytosis (not neoplastic)
    # Melanoma generator should not fire for "メラニン色素沈着" etc.
    "メラノーマ": ["色素沈着", "色素脱失"],
    # Gout — don't trigger on "通風" (ventilation) etc.; specific kanji
    # (no exclusion — 痛風 is highly specific)
    # Mucormycosis — don't catch dermatomycosis etc.
    "ムコール症": [],
    # Stress syndrome — narrow context (reptile only inside generator)
    "ストレス症候群": ["心因性"],
    # Muscle wasting — don't fire for muscle hypertrophy
    "筋萎縮": ["筋肥大"],
    # Cachexia generic — narrow to wasting context
    "悪液質": [],
    # Constipation — don't fire on neoplasia/dysplasia (similar kanji)
    "便秘": [],
    "GI stasis": [],
    # Hypothermia must not catch "高体温" (hyperthermia)
    "低体温": ["高体温"],
    # Seizures — narrow context; don't catch "neuromuscular twitch" or epilepsy variants
    "痙攣": ["子宮"],  # uterine torsion uses 子宮 not 痙攣
    "発作": ["心房", "心室"],  # avoid atrial/ventricular tachycardia which use 発作
    # CKD must not catch acute kidney injury
    "慢性腎臓病": ["急性"],
    "慢性腎症": ["急性"],
    # Chlamydia generic
    "クラミジア": [],
    # Aspergillosis don't catch generic "fungal"
    "アスペルギルス": [],
    # Cardiomyopathy must not catch pericarditis/endocarditis (different diseases)
    "心筋症": ["心膜", "心内膜炎", "心筋炎"],
    # Dehydration - narrow to actual dehydration (not "脱水酵素" etc.)
    "脱水": ["酵素"],
    # Blood disorders: tight scoping to avoid clobbering specific conditions
    "貧血": [],  # 溶血性貧血 should match 貧血 — gen_blood_disorder routes internally
    "血小板減少": [],
    "播種性血管内凝固": [],
    "DIC": [],
    "溶血": [],
    "赤血球増加": [],
    "多血": [],
    "脾腫": [],
    "出血症候群": [],
    "血液疾患": [],
}


def lookup_disease_generator(name_ja: str) -> Optional[Callable[[str, str], Optional[dict]]]:
    """Find a generator function for a disease name. Returns None if not in library."""
    if not name_ja:
        return None
    for pattern, fn in DISEASE_GENERATORS:
        if pattern not in name_ja:
            continue
        # Check exclusion list for this pattern
        exclusions = _GENERATOR_EXCLUSIONS.get(pattern, [])
        if any(excl in name_ja for excl in exclusions):
            continue
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
