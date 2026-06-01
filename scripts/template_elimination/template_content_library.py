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
    bone = ""
    if "翼" in nm or "wing" in nm.lower():
        bone = "翼"
    elif "脚" in nm or "leg" in nm.lower():
        bone = "脚"
    elif "嘴" in nm or "beak" in nm.lower():
        bone = "嘴"
    elif "頭" in nm:
        bone = "頭蓋"

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
                "外傷部位の出血止血。"
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
