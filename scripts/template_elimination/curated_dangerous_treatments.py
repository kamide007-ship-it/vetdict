"""Curated replacements for clinically dangerous treatment miscategorisations.

A small number of disease records carry a *category* treatment template whose
category contradicts the disease — and, unlike the deworm/oncology cases handled
by ``fix_dangerous_treatment_in_served_db``, the disease resolves to the generic
``general`` class, so the fallback generator cannot produce a categorically
correct protocol on its own.

The two dangerous fingerprints handled here are:

* the **toxin-decontamination** template ("迅速な除染と支持療法…催吐…胃洗浄…
  活性炭") applied to non-toxicoses — e.g. cecal dysbiosis, haemolytic anaemia,
  proventricular ulceration, a gizzard foreign body. Recommending emesis /
  gastric lavage / activated charcoal for these is wrong and, for a herbivore
  with GI stasis, harmful.
* the **deworming** template ("同定された寄生虫に応じた適切な駆虫薬") applied to
  non-parasitic disease — e.g. a cerebral infarct, rectal prolapse, a fibrotic
  myopathy, neonatal conjunctivitis.

Rather than fall back to a generic ``general`` protocol, each affected disease is
given a concise, evidence-based, species-appropriate treatment written for that
specific condition. The correction is applied to the *served database* (so the
fix holds regardless of which source — JSON overlay or species module —
introduced the template) and is gated on BOTH a dangerous fingerprint AND a
curated entry matching the disease, so nothing else is ever touched.

References: Carpenter, *Exotic Animal Formulary* 6th ed; Quesenberry & Carpenter,
*Ferrets, Rabbits, and Rodents* 4th ed; Harrison & Lightfoot, *Clinical Avian
Medicine*; Ettinger, *Textbook of Veterinary Internal Medicine* 8th ed.
"""

from __future__ import annotations

# Dangerous treatment-template fingerprints. A record is a *candidate* for
# curated correction only if its treatment_ja contains one of these.
TOXIN_DECONTAM_SIG = "迅速な除染と支持療法"
DEWORM_SIG = "同定された寄生虫に応じた適切な駆虫薬"

DANGEROUS_TREATMENT_SIGS: tuple[str, ...] = (TOXIN_DECONTAM_SIG, DEWORM_SIG)


# Herbivore small mammals whose cecal fermentation makes dysbiosis / bloat a
# medical (not toxicological) emergency.
_HINDGUT_HERBIVORES = frozenset({"rabbit", "chinchilla", "guinea_pig", "degu", "exotic_other"})
_BIRDS = frozenset({"bird", "parakeet", "parrot"})


def _dysbiosis_tx(species: str) -> str:
    note = ""
    if species in ("guinea_pig", "chinchilla", "degu", "rabbit"):
        note = "（これらの草食動物では経口β-ラクタム/リンコサミド系抗菌薬は致死的腸内菌叢崩壊を招くため禁忌）"
    return (
        "盲腸内細菌叢の乱れには、まず高繊維食の是正が基本：良質チモシー乾草を無制限に給与し、"
        "高糖質・高デンプンのペレットやおやつを制限する。プロバイオティクス（例: Bene-Bac）と"
        "プレバイオティクスで正常細菌叢の再構築を図る。Clostridium属の異常増殖が疑われる中等度〜"
        "重度例ではメトロニダゾール 10-20 mg/kg PO q12h（5-7日）を選択し" + note + "、"
        "腸管毒素にはコレスチラミンで吸着する。鼓腸にはシメチコン、消化管運動低下例には十分な"
        "輸液と強制給餌（critical care formula 50-80 mL/kg/日 分割）を行う。誘因（不適切な抗菌薬"
        "投与・急激な食餌変更・低繊維食・ストレス）の除去が再発防止に必須。"
        "催吐・胃洗浄・活性炭投与は適応外である。"
    )


def _bloat_tx(species: str) -> str:
    return (
        "急性盲腸鼓腸は緊急疾患。まず腹部X線で胃拡張・捻転や閉塞を鑑別する。"
        "経鼻/経口胃カテーテルで減圧（脱気）し、シメチコンでガスを分散させる。"
        "閉塞を除外できれば消化管運動促進薬（メトクロプラミド 0.2-0.5 mg/kg SC q8-12h）を併用するが、"
        "完全閉塞・捻転が疑われる場合は禁忌で外科適応（盲腸切開・整復）となる。"
        "積極的な輸液、鎮痛（ブプレノルフィン 0.03 mg/kg）、保温、安定後の強制給餌で支持する。"
        "誘因（急激な食餌変更・低繊維食・dysbiosis・うっ滞）を是正する。"
        "催吐・胃洗浄・活性炭は適応外である。"
    )


def _proventricular_ulcer_tx(species: str) -> str:
    return (
        "腺胃／前胃潰瘍では粘膜保護と胃酸抑制が中心：スクラルファート 25-30 mg/kg PO q8h（空腹時）、"
        "オメプラゾール 1 mg/kg PO q24h。原因の検索と治療が必須で、重金属（鉛・亜鉛）中毒では"
        "キレーション（CaEDTA 30-35 mg/kg IM q12h）、巨大前胃症（PDD/ボルナウイルス）・真菌"
        "（マクロラブダス）・細菌感染にはそれぞれの特異的治療を行う。NSAIDは中止する。"
        "出血例にはビタミンK1、貧血進行例には輸血を考慮する。経管栄養（流動食）で消化管を支持し、"
        "ストレス環境を是正する。催吐・胃洗浄・活性炭は適応外である。"
    )


def _gizzard_foreign_body_tx(species: str) -> str:
    return (
        "筋胃（砂嚢）異物はX線・内視鏡で同定・性状評価する。"
        "小さく非閉塞・非金属の異物は、食餌繊維の調整と砂粒（grit）管理で自然排出を促し経過観察する。"
        "金属異物は重金属中毒のリスクがあるためキレーション（CaEDTA）を併用のうえ、"
        "内視鏡的または外科的に摘出する。閉塞・穿孔徴候があれば開腹下に筋胃切開を行う。"
        "支持療法として輸液・保温・鎮痛・経管栄養を行う。催吐・胃洗浄は鳥類では適応外である。"
    )


def _haemolytic_anaemia_tx(species: str) -> str:
    return (
        "溶血性貧血では原因の鑑別が治療の鍵となる。免疫介在性溶血ではグルココルチコイド"
        "（プレドニゾロン 1-2 mg/kg PO q12-24h）で免疫抑制を行う。"
        "寄生性・微生物性（E. cuniculi、住血微生物）には対応する抗原虫薬・抗菌薬を、"
        "酸化的損傷を起こす毒物・有毒植物の摂取が関与する場合はその除去を行う。"
        "重度貧血（PCV<15-20%）では全血輸血を考慮する。"
        "支持療法として輸液・保温・強制給餌でGI stasisを予防する"
        "（ウサギは経口β-ラクタム系抗菌薬禁忌）。催吐・胃洗浄・活性炭は適応外である。"
    )


def _rectal_prolapse_tx(species: str) -> str:
    return (
        "直腸脱では、まず裏急後重をきたす基礎疾患（寄生虫・大腸炎・尿石・会陰ヘルニア・直腸腫瘤）"
        "の特定と治療が前提となる。急性・非壊死性の脱出：高張糖液（50%デキストロース）で浮腫を"
        "軽減してから用手整復し、巾着縫合を数日間留置する（排便用の開口部を確保）。"
        "再発例には結腸固定術（colopexy）が根治的である。壊死部位は切除＋端々吻合を行う。"
        "術後は軟便化（食物繊維・緩下剤）、鎮痛、原因疾患の治療を継続する。駆虫薬は寄生虫が"
        "証明された場合にのみ適応となる。"
    )


def _ischemic_encephalopathy_tx(species: str) -> str:
    return (
        "猫虚血性脳症（脳梗塞）に対する治療は支持療法が中心である。"
        "発作には抗痙攣薬（ジアゼパム 0.5 mg/kg IV 頓用、レベチラセタム 20 mg/kg PO q8h）、"
        "脳浮腫にはマンニトール 0.5-1 g/kg IV をゆっくり投与し、酸素化・正常血圧・正常血糖を維持する。"
        "基礎疾患（全身性高血圧、心疾患由来の血栓塞栓、まれにCuterebra幼虫の迷入）を検索・管理する。"
        "多くの症例は数週間で部分的に回復するため、栄養・水分管理と安全な療養環境の整備が予後を左右する。"
        "駆虫薬はCuterebra関与が確認された場合に限り適応となり、ルーチンの駆虫プロトコルは不要である。"
    )


def _fibrotic_myopathy_tx(species: str) -> str:
    return (
        "薄筋・半腱様筋ミオパチー（線維化性ミオパチー）は、筋の線維化による慢性・進行性の機械的"
        "跛行で、内科・外科いずれも再発率が高い難治性疾患である。保存療法として理学療法・"
        "ストレッチ・温熱療法・体重管理で可動域の維持を図る。外科的に線維化帯の切除や筋切離を"
        "行っても瘢痕の再形成による再発が多い。鎮痛（NSAID）を行いつつ、競技復帰よりも日常活動の"
        "維持という現実的なQOL目標を設定する。駆虫薬は無効である。"
    )


def _neonatal_sticky_eye_tx(species: str) -> str:
    return (
        "粘着眼（新生児眼炎）は開瞼前の新生子の眼瞼裏に膿性分泌物が貯留する状態である。"
        "閉じた眼瞼を温湿布で軟化させ、愛護的に開瞼して貯留物を滅菌生理食塩水で洗浄・排膿する。"
        "細菌感染に対しては抗菌点眼（例: オフロキサシン眼軟膏、または1%クロラムフェニコール）を"
        "1日数回、数日間塗布する。母体および巣箱の衛生を改善して再発を予防する。"
        "駆虫薬は適応外である。"
    )


def _post_purchase_syndrome_tx(species: str) -> str:
    return (
        "入手後症候群（ヤドカリ）は輸送・乾燥・不適切な環境による衰弱・脱殻不全・四肢脱落の"
        "症候群で、特異的な薬物治療よりも飼育環境の是正が中心となる。"
        "適切な温度（24-27℃）・湿度（70-80%）、塩水と淡水の両方の水皿、十分な深さの砂と隠れ家、"
        "清浄な空気を整える。脱水には浅い塩水浴を行う。二次感染が疑われる外傷部位は局所消毒する。"
        "新規個体は隔離して観察する。催吐・胃洗浄・解毒（活性炭）は適応外である。"
    )


# Each entry: (species_set_or_None, name_substrings, dangerous_sig, generator).
# A record matches when its species is in the set (or set is None), ANY name
# substring is present, and its treatment_ja carries the named dangerous sig.
_CURATED: tuple[tuple[frozenset | None, tuple[str, ...], str, object], ...] = (
    (
        _HINDGUT_HERBIVORES,
        ("盲腸細菌叢異常", "盲腸内細菌叢異常", "腸内細菌叢異常", "Dysbiosis", "Cecal Dysbiosis"),
        TOXIN_DECONTAM_SIG,
        _dysbiosis_tx,
    ),
    (
        frozenset({"chinchilla", "guinea_pig", "degu", "rabbit"}),
        ("鼓脹", "盲腸鼓腸", "Bloat", "Tympany"),
        TOXIN_DECONTAM_SIG,
        _bloat_tx,
    ),
    (_BIRDS, ("腺胃潰瘍", "前胃潰瘍", "Proventricular Ulcer"), TOXIN_DECONTAM_SIG, _proventricular_ulcer_tx),
    (
        _BIRDS,
        ("筋胃異物", "砂嚢異物", "Gizzard", "Ventricular Foreign Body"),
        TOXIN_DECONTAM_SIG,
        _gizzard_foreign_body_tx,
    ),
    (None, ("溶血性貧血", "Haemolytic Anaemia", "Hemolytic Anemia"), TOXIN_DECONTAM_SIG, _haemolytic_anaemia_tx),
    (
        frozenset({"exotic_other"}),
        ("購入後症候群", "Post-Purchase Syndrome", "ヤドカリ", "Hermit Crab"),
        TOXIN_DECONTAM_SIG,
        _post_purchase_syndrome_tx,
    ),
    (None, ("直腸脱", "Rectal Prolapse"), DEWORM_SIG, _rectal_prolapse_tx),
    (
        frozenset({"cat"}),
        ("虚血性脳症", "Ischemic Encephalopathy", "Ischaemic Encephalopathy"),
        DEWORM_SIG,
        _ischemic_encephalopathy_tx,
    ),
    (frozenset({"dog"}), ("薄筋・半腱様筋ミオパチー", "Gracilis", "Semitendinosus"), DEWORM_SIG, _fibrotic_myopathy_tx),
    (None, ("粘着眼", "Sticky Eye"), DEWORM_SIG, _neonatal_sticky_eye_tx),
)


def curated_dangerous_treatment(species: str, name_ja: str, name_en: str, treatment_ja: str) -> str | None:
    """Return a curated treatment when ``treatment_ja`` is a dangerous mismatch.

    Returns None when no dangerous fingerprint is present or no curated entry
    matches — so callers may treat ``None`` as "leave untouched".
    """
    if not treatment_ja:
        return None
    species = (species or "").lower()
    name = f"{name_ja or ''} {name_en or ''}"
    for species_set, name_subs, sig, gen in _CURATED:
        if sig not in treatment_ja:
            continue
        if species_set is not None and species not in species_set:
            continue
        if not any(sub in name for sub in name_subs):
            continue
        new = gen(species)
        if new and new != treatment_ja:
            return new
    return None
