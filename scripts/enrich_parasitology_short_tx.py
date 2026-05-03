#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# Phase 3: De-duplicate 150c parasitology template (24 entries)
# ============================================================

# --- Rabbit ---

ENRICHMENTS["rabbit_0032"] = {
    "treatment_ja": (
        "ウサギの蟯虫症（Passalurus ambiguus）。盲腸・結腸に寄生。"
        "最も一般的なウサギの消化管寄生虫。"
        "■臨床症状: 多くは無症状。重度: 肛門周囲の掻痒（尻を擦りつける）。"
        "  軽度の体重減少。稀に盲腸炎。"
        "■診断: 糞便浮遊法（虫卵）。セロハンテープ法（肛門周囲の虫卵）。"
        "  肉眼的に成虫（4-11mm白色線虫）を糞便中に確認。"
        "■治療: "
        "  フェンベンダゾール 20 mg/kg PO q24h × 5日。2週後に再投与。"
        "  イベルメクチン 0.2-0.4 mg/kg SC/PO、2週間隔で2回。"
        "  環境消毒: 虫卵は環境中に数週間残存 → ケージの熱水洗浄・消毒。"
        "■予後: 良好。環境対策なしでは再感染しやすい。"
        "参考文献: Harcourt-Brown F (2002); Quesenberry & Carpenter (2020)."
    ),
}

ENRICHMENTS["rabbit_0040"] = {
    "treatment_ja": (
        "ウサギの条虫症。Cittotaenia ctenoides（直接感染）、"
        "Mosgovoyia pectinata等。ウサギは中間宿主として犬条虫にも関与。"
        "■臨床症状: 多くは無症状。重度: 下痢、体重減少。"
        "  腸閉塞（大量寄生時 — 稀）。"
        "■診断: 糞便浮遊法（虫卵 or 片節）。片節の肉眼的確認。"
        "■治療: "
        "  プラジカンテル 5-10 mg/kg SC/PO、2週間隔で2回。"
        "  フェンベンダゾール 20 mg/kg PO q24h × 5日（一部条虫に有効）。"
        "  ★ウサギへのプラジカンテルは安全だが注射部位反応に注意★。"
        "■予後: 良好。"
        "参考文献: Harcourt-Brown F (2002); Quesenberry & Carpenter (2020)."
    ),
}

# --- Hamster ---

ENRICHMENTS["hamster_0041"] = {
    "treatment_ja": (
        "ハムスターの蟯虫症（Syphacia spp.）。盲腸・結腸に寄生。"
        "集団飼育で感染率が高い。"
        "■臨床症状: 多くは無症状。重度: 直腸脱（慢性テネスムス）。"
        "  肛門周囲の掻痒。体重減少。"
        "■診断: セロハンテープ法（肛門周囲虫卵）。糞便浮遊法。"
        "■治療: "
        "  フェンベンダゾール 20 mg/kg PO q24h × 5日。2週後に再投与。"
        "  イベルメクチン 0.2-0.4 mg/kg SC/PO、2週間隔で2回。"
        "  環境: ケージの完全洗浄・消毒。床材全交換。"
        "  同居個体の同時治療（全頭投与）。"
        "■予後: 良好。環境消毒が再感染予防の鍵。"
        "参考文献: Quesenberry & Carpenter (2020); Carpenter JW (2018)."
    ),
}

ENRICHMENTS["hamster_0042"] = {
    "treatment_ja": (
        "ハムスターの条虫症（Hymenolepis nana / H. diminuta）。"
        "★H. nanaは人獣共通感染症（ヒトにも感染）★。"
        "■臨床症状: 多くは無症状。重度: 下痢、体重減少。"
        "  腸閉塞（大量寄生 — 稀）。"
        "■診断: 糞便浮遊法（特徴的虫卵 — H. nanaは30-47μm）。"
        "■治療: "
        "  プラジカンテル 5-10 mg/kg SC/PO、2週間隔で2回。"
        "  ニクロサミド 100 mg/kg PO q24h × 7日（利用可能な場合）。"
        "  環境消毒: 虫卵の直接感染を防止。手洗い励行。"
        "  ★飼い主への衛生指導（ヒト感染リスク）★。"
        "■予後: 良好。H. nanaの自己感染サイクルに注意（再治療が必要な場合あり）。"
        "参考文献: Quesenberry & Carpenter (2020); Carpenter JW (2018)."
    ),
}

ENRICHMENTS["hamster_0131"] = {
    "treatment_ja": (
        "ハムスターの消化管寄生虫症（一般）。蟯虫、条虫、原虫（ジアルジア等）。"
        "■臨床症状: 無症状〜下痢、体重減少、脱水。被毛粗剛。"
        "■診断: 糞便浮遊法（虫卵）。直接塗抹法（原虫栄養体）。"
        "■治療: "
        "  線虫（蟯虫等）: フェンベンダゾール 20 mg/kg PO q24h × 5日。"
        "  条虫: プラジカンテル 5-10 mg/kg SC/PO × 2回。"
        "  ジアルジア: メトロニダゾール 20-40 mg/kg PO q12h × 5-7日。"
        "  コクシジウム: トルトラズリル 10 mg/kg PO q24h × 3日。"
        "  環境: ケージ洗浄、床材交換。同居個体の同時治療。"
        "■予後: 良好（適切な駆虫 + 環境対策）。"
        "参考文献: Quesenberry & Carpenter (2020); Carpenter JW (2018)."
    ),
}

# --- Chinchilla ---

ENRICHMENTS["chinchilla_0131"] = {
    "treatment_ja": (
        "チンチラの蟯虫症。Syphacia obvelata等。集団飼育で蔓延しやすい。"
        "■臨床症状: 多くは無症状。重度: 肛門周囲掻痒、直腸脱。"
        "■診断: セロハンテープ法。糞便浮遊法。"
        "■治療: "
        "  フェンベンダゾール 20 mg/kg PO q24h × 5日。2週後再投与。"
        "  イベルメクチン 0.2-0.4 mg/kg SC/PO × 2回（2週間隔）。"
        "  環境消毒: ケージ・砂浴び容器の洗浄。床材全交換。"
        "  ★チンチラにフィプロニルは致死的 — 外部寄生虫治療時に誤用しないこと★。"
        "■予後: 良好。"
        "参考文献: Quesenberry & Carpenter (2020); Carpenter JW (2018)."
    ),
}

# --- Reptile (generic) ---

ENRICHMENTS["reptile_0034"] = {
    "treatment_ja": (
        "爬虫類の線虫症。回虫（Ophidascaris等）、鉤虫、蟯虫。"
        "飼育下では糞口感染サイクルで蔓延。"
        "■臨床症状: 軽度: 無症状。重度: 体重減少、吐出、下痢。"
        "  回虫大量寄生: 腸閉塞。肺幼虫移行: 呼吸器症状。"
        "■診断: 糞便浮遊法（虫卵形態で種同定）。直接塗抹法。"
        "■治療: "
        "  フェンベンダゾール 50-100 mg/kg PO、2週間隔で3回。"
        "  レバミゾール 5-10 mg/kg PO/SC/ICe（吸虫にも一部有効）。"
        "  ★イベルメクチンはカメには慎重投与（毒性報告あり）★。"
        "  ヘビ・トカゲ: イベルメクチン 0.2 mg/kg SC/PO（ダニ兼用）。"
        "  環境: POTZ管理（適正温度 — 免疫機能維持）。糞便の速やかな除去。"
        "■予後: 適切な駆虫で良好。"
        "参考文献: Divers SJ & Stahl SJ (2019); Jacobson ER (2007)."
    ),
}

ENRICHMENTS["reptile_0036"] = {
    "treatment_ja": (
        "爬虫類の吸虫症（Trematoda）。水棲・半水棲種に多い。"
        "中間宿主（貝類）を介する間接生活環。"
        "■臨床症状: 腎吸虫（Spirorchidae — カメ）: 腎障害、浮腫。"
        "  血管内吸虫: 卵塞栓による多臓器障害。肝吸虫: 肝腫大。"
        "  肺吸虫: 呼吸困難。"
        "■診断: 糞便沈殿法（虫卵 — 蓋付き虫卵が特徴）。剖検。"
        "■治療: "
        "  プラジカンテル 5-8 mg/kg SC/PO/ICe、2週間隔で2-3回。"
        "  ★重度の血管内吸虫症は駆虫後に卵塞栓による急性症状悪化あり★。"
        "  支持療法: 輸液、POTZ管理。"
        "  環境: 中間宿主（巻貝）の排除。"
        "■予後: 軽度→良好。血管内吸虫大量寄生→慎重。"
        "参考文献: Divers SJ & Stahl SJ (2019); Jacobson ER (2007)."
    ),
}

ENRICHMENTS["reptile_0038"] = {
    "treatment_ja": (
        "爬虫類のコクシジウム症。Isospora, Eimeria, Cryptosporidium等。"
        "飼育下で糞口感染サイクルが成立。"
        "■臨床症状: 水様〜粘液性下痢、体重減少、脱水。"
        "  Cryptosporidium（ヘビ）: 胃粘膜肥厚、慢性吐出、致死的。"
        "■診断: 糞便浮遊法（オーシスト）。抗酸菌染色（Cryptosporidium）。PCR。"
        "■治療: "
        "  Isospora/Eimeria: トルトラズリル 5-15 mg/kg PO q24h × 3日、7日後再投与。"
        "    ポナズリル 10-30 mg/kg PO q24h × 14日（代替）。"
        "    スルファジメトキシン 50 mg/kg PO初日 → 25 mg/kg q24h × 5日。"
        "  Cryptosporidium: ★有効な治療法なし★。"
        "    パロモマイシン 100 mg/kg PO q24h × 14日（排オーシスト減少のみ）。"
        "    ★特にヘビのCryptosporidium serpentisは致死的 — 安楽死検討★。"
        "  環境: 熱水消毒（オーシストは一般消毒剤に抵抗性）。"
        "  POTZ管理（免疫機能維持）。"
        "■予後: Isospora/Eimeria→良好。Cryptosporidium→不良。"
        "参考文献: Divers SJ & Stahl SJ (2019); Jacobson ER (2007)."
    ),
}

ENRICHMENTS["reptile_0139"] = {
    "treatment_ja": (
        "爬虫類の消化管寄生虫症（一般）。線虫、条虫、吸虫、原虫の混合感染も多い。"
        "■診断: 糞便浮遊法 + 沈殿法 + 直接塗抹法（3法併用推奨）。"
        "■治療: "
        "  線虫: フェンベンダゾール 50-100 mg/kg PO × 3回（2週間隔）。"
        "  条虫: プラジカンテル 5-8 mg/kg SC/PO × 2回。"
        "  コクシジウム: トルトラズリル 5-15 mg/kg PO q24h × 3日。"
        "  原虫（アメーバ等）: メトロニダゾール 25-50 mg/kg PO q24h × 5-7日。"
        "  環境: POTZ管理。糞便除去。清潔な水。"
        "  定期検便: 3-6ヶ月毎（飼育下）。"
        "■予後: 良好（定期的な駆虫と環境管理）。"
        "参考文献: Divers SJ & Stahl SJ (2019)."
    ),
}

# --- Tortoise ---

ENRICHMENTS["tortoise_0041"] = {
    "treatment_ja": (
        "リクガメの線虫症。Angusticaecum, Alaeuris等。回虫・蟯虫。"
        "■臨床症状: 軽度: 無症状。重度: 食欲不振、軟便、体重減少。"
        "  大量寄生: 腸閉塞（特に小型種）。"
        "■診断: 糞便浮遊法。"
        "■治療: "
        "  フェンベンダゾール 50-100 mg/kg PO、2週間隔で3回。"
        "  ★カメへのイベルメクチンは毒性報告あり — フェンベンダゾールが第一選択★。"
        "  環境: 飼育スペースの清掃。糞便の速やかな除去。POTZ管理。"
        "  定期検便（3-6ヶ月毎）。"
        "■予後: 良好。"
        "参考文献: McArthur S et al. (2004); Divers SJ & Stahl SJ (2019)."
    ),
}

ENRICHMENTS["tortoise_0043"] = {
    "treatment_ja": (
        "リクガメの吸虫症。淡水カメで多い（半水棲種）。"
        "Spirorchidae（血管内吸虫 — ウミガメで重要）。"
        "■臨床症状: 肝腫大、腹水。腎障害。呼吸困難（肺吸虫）。"
        "  血管内吸虫: 卵塞栓→多臓器炎症。"
        "■診断: 糞便沈殿法。血液中のmicrofilariae検索。"
        "■治療: "
        "  プラジカンテル 5-8 mg/kg SC/PO/ICe × 2-3回（2週間隔）。"
        "  ★リクガメは水棲種ほど吸虫症のリスクは低い★。"
        "  支持療法: 輸液（温浴 + SC）。POTZ管理。"
        "■予後: 軽度→良好。血管内吸虫大量寄生→慎重。"
        "参考文献: McArthur S et al. (2004); Divers SJ & Stahl SJ (2019)."
    ),
}

ENRICHMENTS["tortoise_0045"] = {
    "treatment_ja": (
        "リクガメのコクシジウム症。Isospora, Eimeria等。"
        "過密飼育・ストレス・免疫低下で発症。"
        "■臨床症状: 水様〜粘液性下痢、食欲不振、脱水、体重減少。"
        "  幼体で重症化しやすい。"
        "■診断: 糞便浮遊法（オーシスト）。"
        "■治療: "
        "  トルトラズリル 5-15 mg/kg PO q24h × 3日。7日後に再投与。"
        "  スルファジメトキシン 50 mg/kg PO初日 → 25 mg/kg q24h × 5日。"
        "  輸液: 温浴（30分 — 経クロアカ吸水）+ SC。"
        "  環境: POTZ管理。飼育スペース消毒（熱水）。"
        "■予後: 良好（適切な治療 + 環境改善）。"
        "参考文献: McArthur S et al. (2004); Divers SJ & Stahl SJ (2019)."
    ),
}

ENRICHMENTS["tortoise_0145"] = {
    "treatment_ja": (
        "リクガメの消化管寄生虫症（一般）。"
        "■治療: "
        "  線虫: フェンベンダゾール 50-100 mg/kg PO × 3回（2週間隔）。"
        "  条虫: プラジカンテル 5-8 mg/kg SC/PO × 2回。"
        "  コクシジウム: トルトラズリル 5-15 mg/kg PO q24h × 3日。"
        "  ★イベルメクチンはカメに禁忌（毒性リスク）★。フェンベンダゾール使用。"
        "  環境: POTZ管理。清掃。定期検便。"
        "■予後: 良好。"
        "参考文献: McArthur S et al. (2004); Divers SJ & Stahl SJ (2019)."
    ),
}

# --- Snake ---

ENRICHMENTS["snake_0040"] = {
    "treatment_ja": (
        "ヘビの線虫症。Ophidascaris（回虫）、Kalicephalus（鉤虫）、"
        "Rhabdias（肺虫）等。WC個体で高感染率。"
        "■臨床症状: 吐出（回虫大量寄生）、体重減少。"
        "  肺虫: 呼吸困難、開口呼吸。消化管出血（鉤虫）。"
        "■診断: 糞便浮遊法。気管洗浄液（肺虫）。"
        "■治療: "
        "  フェンベンダゾール 50-100 mg/kg PO、2週間隔で3回。"
        "  イベルメクチン 0.2 mg/kg SC/PO（線虫 + ダニ兼用）。"
        "  レバミゾール 5-10 mg/kg SC/ICe（肺虫に有効）。"
        "  POTZ管理。環境消毒。"
        "■予後: 良好（定期駆虫）。肺虫重度→慎重。"
        "参考文献: Divers SJ & Stahl SJ (2019); Jacobson ER (2007)."
    ),
}

ENRICHMENTS["snake_0042"] = {
    "treatment_ja": (
        "ヘビの吸虫症。Stomatrema（口腔吸虫）、Ochetosoma（胆管吸虫）等。"
        "野生捕獲個体に多い。中間宿主を介する。"
        "■臨床症状: 口腔吸虫: 口内炎（stomatitis随伴）。"
        "  胆管吸虫: 肝腫大、黄疸。肺吸虫: 呼吸困難。"
        "■診断: 糞便沈殿法（蓋付き虫卵）。口腔内の虫体肉眼的確認。"
        "■治療: "
        "  プラジカンテル 5-8 mg/kg SC/PO × 2-3回（2週間隔）。"
        "  口腔吸虫: 物理的除去 + プラジカンテル。口腔消毒。"
        "  支持療法: POTZ管理。"
        "■予後: 良好。CB個体では稀。"
        "参考文献: Divers SJ & Stahl SJ (2019); Jacobson ER (2007)."
    ),
}

ENRICHMENTS["snake_0044"] = {
    "treatment_ja": (
        "ヘビのコクシジウム症。Isospora等。"
        "★Cryptosporidium serpentisはヘビで特に致死的★。"
        "■臨床症状: "
        "  Isospora: 水様下痢、体重減少。"
        "  C. serpentis: 慢性吐出、胃粘膜肥厚（X線で確認）、"
        "    進行性削痩 → 致死。★コレクションに壊滅的★。"
        "■診断: 糞便浮遊法。抗酸菌染色（Crypto）。PCR。"
        "■治療: "
        "  Isospora: トルトラズリル 5-15 mg/kg PO q24h × 3日。"
        "  C. serpentis: ★有効な治療法なし★。"
        "    パロモマイシン 100 mg/kg PO q24h × 14日（排オーシスト減少のみ）。"
        "    ★陽性個体は隔離。安楽死を検討（コレクション保護）★。"
        "  POTZ管理。環境熱水消毒。"
        "■予後: Isospora→良好。C. serpentis→不良（致死的）。"
        "参考文献: Divers SJ & Stahl SJ (2019); Jacobson ER (2007)."
    ),
}

# --- Lizard ---

ENRICHMENTS["lizard_0041"] = {
    "treatment_ja": (
        "トカゲの線虫症。回虫、蟯虫（Oxyuridae — 草食トカゲで多い）。"
        "蟯虫は草食トカゲの盲腸に共生的に存在する場合がある。"
        "■臨床症状: 蟯虫: 多くは無症状（過剰寄生時のみ問題）。"
        "  回虫: 体重減少、下痢。大量寄生で腸閉塞。"
        "■診断: 糞便浮遊法。"
        "■治療: "
        "  フェンベンダゾール 50-100 mg/kg PO、2週間隔で3回。"
        "  イベルメクチン 0.2 mg/kg SC/PO。"
        "  ★蟯虫の少数寄生は治療不要の場合あり（草食トカゲの共生菌叢に寄与）★。"
        "  環境: POTZ管理。糞便除去。"
        "■予後: 良好。"
        "参考文献: Divers SJ & Stahl SJ (2019); Jacobson ER (2007)."
    ),
}

ENRICHMENTS["lizard_0043"] = {
    "treatment_ja": (
        "トカゲの吸虫症。野生捕獲個体に多い。"
        "■臨床症状: 肝吸虫: 肝腫大。肺吸虫: 呼吸困難。多くは軽度。"
        "■診断: 糞便沈殿法。"
        "■治療: "
        "  プラジカンテル 5-8 mg/kg SC/PO × 2-3回（2週間隔）。"
        "  POTZ管理。CB個体では稀。"
        "■予後: 良好。"
        "参考文献: Divers SJ & Stahl SJ (2019)."
    ),
}

ENRICHMENTS["lizard_0045"] = {
    "treatment_ja": (
        "トカゲのコクシジウム症。Isospora, Eimeria。"
        "特にヒョウモントカゲモドキ（Eublepharis macularius）で臨床的に重要。"
        "■臨床症状: 下痢（粘液性〜血性）、体重減少、脱水。"
        "  幼体: 急速に重症化。"
        "  ★Cryptosporidium varanaeはトカゲで致死的な場合あり★。"
        "■診断: 糞便浮遊法。抗酸菌染色（Crypto）。PCR。"
        "■治療: "
        "  トルトラズリル 5-15 mg/kg PO q24h × 3日。7日後再投与。"
        "  ポナズリル 10-30 mg/kg PO q24h × 14日。"
        "  Cryptosporidium: 有効な治療法なし。パロモマイシン（試験的）。"
        "  輸液。POTZ管理。衛生管理。"
        "■予後: Isospora/Eimeria→良好。Cryptosporidium→不良。"
        "参考文献: Divers SJ & Stahl SJ (2019); Jacobson ER (2007)."
    ),
}

# --- Amphibian ---

ENRICHMENTS["amphibian_0008"] = {
    "treatment_ja": (
        "両生類のRhabdias感染（肺虫）。直接生活環（自由生活世代あり）。"
        "■臨床症状: 呼吸困難、開口呼吸。慢性削痩。"
        "  肺の炎症・出血。二次細菌性肺炎。"
        "■診断: 糞便浮遊法（幼虫）。気管洗浄液。"
        "■治療: "
        "  レバミゾール 5-10 mg/kg ICe or 浸漬（10 mg/L × 24h）。"
        "  フェンベンダゾール 50-100 mg/kg PO × 2回（2週間隔）。"
        "  ★両生類は皮膚透過性が高い — 薬浴/浸漬投与が実用的★。"
        "  イベルメクチン 0.2 mg/kg 経皮（背部 — 希釈して適用）。"
        "  環境: 基質の完全交換（自由生活期幼虫の除去）。"
        "■予後: 適切な駆虫で良好。"
        "参考文献: Wright KM & Whitaker BR (2001); Densmore CL & Green DE (2007)."
    ),
}

ENRICHMENTS["amphibian_0009"] = {
    "treatment_ja": (
        "両生類の吸虫症。中間宿主（巻貝）を介する。"
        "■臨床症状: 腎吸虫: 腎腫大、浮腫、腹水。"
        "  メタセルカリアのシスト: 皮下結節。"
        "  肺吸虫: 呼吸困難。"
        "■診断: 糞便沈殿法。皮膚のシスト視診。"
        "■治療: "
        "  プラジカンテル 5-10 mg/kg ICe or 浸漬（10 mg/L × 3h）。"
        "    2週間隔で2-3回。"
        "  環境: 中間宿主（巻貝）の排除。"
        "  ★薬浴は皮膚から吸収される — 濃度に注意★。"
        "■予後: 軽度→良好。腎吸虫大量寄生→慎重。"
        "参考文献: Wright KM & Whitaker BR (2001)."
    ),
}

ENRICHMENTS["amphibian_0049"] = {
    "treatment_ja": (
        "両生類の線虫症（一般）。回虫、蟯虫、肺虫（Rhabdias）等。"
        "■臨床症状: 体重減少、食欲不振。肺虫: 呼吸困難。"
        "■診断: 糞便浮遊法。"
        "■治療: "
        "  フェンベンダゾール 50-100 mg/kg PO × 2-3回（2週間隔）。"
        "  レバミゾール 5-10 mg/kg ICe or 浸漬（肺虫に有効）。"
        "  イベルメクチン 0.2 mg/kg 経皮（希釈 — 種による感受性の差に注意）。"
        "  環境: 基質交換。POTZ管理。"
        "■予後: 良好。"
        "参考文献: Wright KM & Whitaker BR (2001)."
    ),
}

ENRICHMENTS["amphibian_0052"] = {
    "treatment_ja": (
        "両生類のコクシジウム症。Isospora, Eimeria等。"
        "■臨床症状: 下痢、体重減少、脱水。"
        "  Cryptosporidium: 慢性消耗 → 予後不良。"
        "■診断: 糞便浮遊法。抗酸菌染色。"
        "■治療: "
        "  トルトラズリル 5-15 mg/kg PO q24h × 3日。"
        "    浸漬法: 10 mg/L × 24h。"
        "  スルファジメトキシン 50 mg/kg PO初日 → 25 mg/kg × 5日。"
        "  Cryptosporidium: 有効な治療法なし。"
        "  輸液: 浸漬（両生類用リンゲル液）。POTZ管理。"
        "■予後: Isospora→良好。Cryptosporidium→不良。"
        "参考文献: Wright KM & Whitaker BR (2001); Densmore CL & Green DE (2007)."
    ),
}


def apply_enrichments() -> None:
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for entry in data:
        eid = entry.get("id")
        if eid in ENRICHMENTS:
            patch = ENRICHMENTS[eid]
            for k, v in patch.items():
                entry[k] = v
            updated += 1

    missing = set(ENRICHMENTS) - {e.get("id") for e in data}
    if missing:
        print(f"WARNING: {len(missing)} IDs not found: {sorted(missing)}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated}/{len(ENRICHMENTS)} parasitology entries")


if __name__ == "__main__":
    apply_enrichments()
