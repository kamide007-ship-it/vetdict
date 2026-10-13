"""2026-10 第70弾: 外部寄生虫症（ダニ・ノミ）の治療テンプレート撲滅.

配信監査で、外部寄生虫症31エントリの治療欄が内部寄生虫用の汎用テンプレートだった:

- JA「…同定された寄生虫に応じた適切な駆虫薬が必要…全てのライフステージを排除…」
- EN "Anti-parasitic therapy appropriate to the parasite (fenbendazole, ivermectin,
  praziquantel, toltrazuril)…"

フェンベンダゾール・プラジカンテル・トルトラズリルは蠕虫・原虫の薬でダニには無効
であり、さらに **タランチュラのダニにイベルメクチン（節足動物＝クモ類に致死的）**、
リクガメ等への誤用リスクを含む臨床的に危険な記述だった。

- 英語がキュレート済みの16件: JA を英語の忠実な日本語版に（新規の医学的主張なし）
- 日英とも汎用文だった15件: 教科書準拠で日英とも記述
  （Quesenberry & Carpenter 4th ed; Carpenter Exotic Animal Formulary 6th ed;
  Mader Reptile Medicine 3rd ed; Ritchie & Harrison; Mueller 2020 Vet Dermatol;
  Romero 2017 Vet Dermatol（ハリネズミのフルララネル））

Usage:
    python3 scripts/template_elimination/fix_ectoparasite_treatments.py --apply
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"

TEMPLATE_MARKS_JA = ("同定された寄生虫に応じた適切な駆虫薬", "糞便PCR/直接鏡検/フローテーション法で原因虫種を特定")
TEMPLATE_MARK_EN = (
    "Anti-parasitic therapy appropriate to the parasite (fenbendazole, ivermectin, praziquantel, toltrazuril)"
)

C: dict[tuple[str, str], dict[str, str]] = {}

# ---- (a) EN curated → JA faithful translation ----
C[("Dog", "Mange (Demodex/Sarcoptes)")] = {
    "treatment_ja": (
        "ニキビダニ症: イソキサゾリン系が第一選択 — フルララネル（ブラベクト）25-56 mg/kg PO 単回、またはアフォキソラネル"
        "（ネクスガード）2.7 mg/kg PO 月1回。イベルメクチン 0.3-0.6 mg/kg PO q24h（MDR1変異犬種には使用しない）。"
        "限局型: 若齢犬では自然治癒することが多い。全身型: 1ヶ月間隔の皮膚掻爬で2回連続陰性になるまで治療。"
        "疥癬（サルコプテス）: イソキサゾリン系（単回で治癒することが多い）。セラメクチン（レボリューション）外用 2週毎×3回。"
        "同居動物も全頭治療し、環境対策を行う。予後: 限局型ニキビダニ症は約90%が治癒、全身型はイソキサゾリン系で80-90%治癒、"
        "疥癬は良好。（Mueller 2020; Perego 2019）"
    )
}
C[("Dog", "Ear Mite Infestation (Otodectes)")] = {
    "treatment_ja": (
        "イソキサゾリン系: フルララネル（ブラベクト）またはサロラネル — 単回で治癒することが多い。セラメクチン（レボリューション）"
        "外用 2週毎×3回。イベルメクチン 0.2-0.4 mg/kg SC/PO、14日後に再投与（MDR1変異犬種を除く）。点耳: ミルベマイシン含有点耳薬。"
        "治療前に耳道洗浄。同居の猫・犬も全頭治療。ミミヒゼンダニは宿主外で長く生存しないため環境処理は通常不要。"
        "予後: 極めて良好。（Shanks 2000; Six 2000）"
    )
}
C[("Dog", "Sarcoptic Mange (Scabies)")] = {
    "treatment_ja": (
        "イソキサゾリン系（第一選択）: フルララネル（ブラベクト）PO 単回、またはサロラネル/アフォキソラネル月1回。"
        "セラメクチン（レボリューション）外用 2週毎×3回。イベルメクチン 0.2-0.4 mg/kg SC/PO 7-14日毎×4回（MDR1犬種は避ける）。"
        "石灰硫黄合剤 1:16 浸漬 週1回×6回（全犬種で安全）。同居動物も全頭治療。環境: 寝具を熱湯洗浄。"
        "掻痒の緩和にプレドニゾロン 0.5-1 mg/kg PO 3-5日（ダニの死滅を待つ間）。"
        "人獣共通: ヒトに一過性の皮疹（自然治癒）。予後: 極めて良好。（Mueller 2020; Perego 2019）"
    )
}
C[("Dog", "Cheyletiellosis (Walking Dandruff)")] = {
    "treatment_ja": (
        "イソキサゾリン系: フルララネルまたはサロラネル — 高い有効性。セラメクチン外用 2週毎×3回。フィプロニルスプレー。"
        "イベルメクチン 0.2-0.3 mg/kg SC 7-14日毎×3-4回（MDR1犬種は避ける）。石灰硫黄合剤浸漬 週1回×6-8回。"
        "同居動物を全頭治療。環境: 徹底清掃・寝具の洗浄（ツメダニは宿主外で約10日生存）。"
        "人獣共通: ヒトに一過性の丘疹性皮膚炎。予後: 全頭治療＋環境対策で極めて良好。（Paradis 1998）"
    )
}
C[("Cat", "Demodicosis")] = {
    "treatment_ja": (
        "猫では稀 — 基礎にある免疫抑制（FIV・FeLV・糖尿病・腫瘍・医原性ステロイド）を検索する。"
        "Demodex cati（毛包型）: 石灰硫黄合剤 1:16 浸漬 7日毎×4-6週。イベルメクチン 0.2-0.3 mg/kg PO q24h×4-8週。"
        "ドラメクチン 0.6 mg/kg SC 7日毎×4-6週。フルララネル（ブラベクト）外用 単回（エビデンス集積中）。"
        "Demodex gatoi（伝染性・表在型）: 石灰硫黄合剤浸漬 7日毎×6-8週、同居猫を全頭治療。"
        "診断: 皮膚掻爬（D. cati）、表在掻爬・セロハンテープ（D. gatoi）。予後: 基礎疾患に対処すれば良好。"
        "（Mueller 2020; Short & Gram 2016）"
    )
}
C[("Cat", "Ear Mite Infestation (Otodectes cynotis)")] = {
    "treatment_ja": (
        "セラメクチン（レボリューション）外用 単回、30日後に再投与（第一選択 — 全身作用）。イベルメクチン 0.2-0.3 mg/kg SC/PO、"
        "2-3週後に再投与。フルララネル（ブラベクト）スポットオン。サロラネル・セラメクチン（レボリューションプラス）。"
        "点耳: ミルベマイシン点耳薬。耳道洗浄: 黒褐色の耳垢をやさしく除去。同居の猫・犬を全頭治療（伝染性が強い）。"
        "二次性の細菌/酵母性外耳炎は同時に治療（局所抗菌薬/抗真菌薬）。猫の外耳炎の50%以上の原因。"
        "予後: 同居動物全頭の全身治療で極めて良好。（Miller 2013; ESCCAP）"
    )
}
C[("Cat", "Flea Infestation")] = {
    "treatment_ja": (
        "イソキサゾリン系: フルララネル（ブラベクト）外用 12週毎。サロラネル・セラメクチン（レボリューションプラス）月1回。"
        "フルララネル・モキシデクチン（ブラベクトプラス）外用 2ヶ月毎 — フィラリア予防・回虫/鉤虫も同時にカバー。"
        "セラメクチン（レボリューション）月1回。フィプロニル スポットオン月1回。同居動物を全頭治療。"
        "環境: 徹底的な掃除機がけ、寝具の60°C洗浄、環境スプレー（ペルメトリン系 — 猫には絶対に塗布しない）。"
        "蛹は数ヶ月生存するため通年の予防を推奨。**犬用ペルメトリン製剤を猫に使用しない（致死的）**。"
        "重度寄生の子猫はノミ性貧血で輸血が必要になることがある。予後: 全頭の継続的治療で極めて良好。（Rust 2017; ESCCAP）"
    ),
    "treatment_append": " Fluralaner/moxidectin (Bravecto Plus) topical every 2 months adds heartworm prevention and roundworm/hookworm treatment.",
}
C[("Cat", "Notoedric Mange (Feline Scabies)")] = {
    "treatment_ja": (
        "セラメクチン（レボリューション）外用 2週毎×3回（第一選択）。イベルメクチン 0.2-0.3 mg/kg SC 14日毎×3回。"
        "石灰硫黄合剤 1:16 浸漬 7日毎×6-8週。フルララネル（ブラベクト）外用（エビデンス集積中）。同居猫を全頭治療。"
        "ネコショウセンコウヒゼンダニは伝染性が強く激しい掻痒、頭部・耳介・顔面の痂皮が典型。皮膚掻爬でダニは多数検出されやすい"
        "（疥癬より見つけやすい）。ヒトへの軽度・一過性の感染あり。宿主外で長く生存しないため環境処理は限定的でよい。"
        "予後: 治療で極めて良好。（Miller 2013; Leone 2013）"
    )
}
C[("Cat", "Feline Cheyletiellosis (Walking Dandruff)")] = {
    "treatment_ja": (
        "セラメクチン（レボリューション）外用 14-30日毎×3回（第一選択）。フルララネル（ブラベクト）外用 単回。"
        "サロラネル・セラメクチン（レボリューションプラス）。イベルメクチン 0.2-0.3 mg/kg SC 14日毎×3回。"
        "石灰硫黄合剤 1:16 浸漬 7日毎×4-6週。同居動物を全頭治療（伝染性が強い）。"
        "Cheyletiella blakei（猫）・C. yasguri（犬）・C. parasitovorax（ウサギ）。環境: 掃除機がけ・寝具洗浄（宿主外で10日以上生存）。"
        "ヒトに一過性の掻痒性皮膚炎。診断: セロハンテープ・表在掻爬（大型のダニで視認可能）。予後: 極めて良好。"
        "（Saevik 2004; Miller 2013）"
    )
}
C[("Cat", "Feline Trombiculiasis (Chigger Mite)")] = {
    "treatment_ja": (
        "外用: フィプロニルスプレー、フルララネル（ブラベクト）外用、セラメクチン（レボリューション）。"
        "石灰硫黄合剤 1:16 浸漬 週1回×2-3回。ダニの除去（やさしい洗浄）。"
        "掻痒の緩和: プレドニゾロン 0.5-1 mg/kg PO q24h×5-7日、狭い範囲はヒドロコルチゾン外用。"
        "二次性細菌感染にはアモキシシリン・クラブラン酸。ツツガムシ（秋ダニ）は幼虫期のみ寄生し成虫は自由生活。"
        "夏〜秋に多く外出猫に好発、頭部・耳介・肢端・腹部に病変。ダニが脱落すれば自然軽快。"
        "予防: 流行期の外出制限。予後: 極めて良好。（Miller 2013; Shanks 2000）"
    )
}
C[("Rabbit", "Demodex Mange")] = {
    "treatment_ja": (
        "■イベルメクチン 0.2-0.4 mg/kg SC 14日毎×3-4回。■セラメクチン（レボリューション）6-18 mg/kg 外用 30日毎。"
        "■基礎の免疫抑制（E. cuniculi・ストレス・コルチコステロイド）に対処。■診断は皮膚掻爬。"
        "■予後: 治療で良好。重度例は免疫抑制を検索する。**フィプロニルはウサギに致死的 — 使用しない**。"
        "（Harcourt-Brown 2002）"
    )
}
C[("Hamster", "Demodex Mange - Generalized")] = {
    "treatment_ja": (
        "■イベルメクチン 0.2-0.4 mg/kg SC 14日毎×3-4回（第一選択）。■アミトラズ 0.025% 浸漬 14日毎×3回"
        "（小型哺乳類では毒性リスクがあり慎重に）。■基礎の免疫抑制を検索: 副腎皮質機能亢進症（ハムスターに多い）・慢性疾患・加齢。"
        "■予後: 要注意 — 基礎疾患の存在を示すことが多いので原疾患を治療する。（Harkness & Wagner 2010）"
    )
}
C[("Guinea Pig", "Trixacarus caviae (Sarcoptic Mange) - Severe")] = {
    "treatment_ja": (
        "【重度 — 激しい掻痒により痙攣を起こしうる】■イベルメクチン 0.2-0.5 mg/kg SC 7-14日毎×3-4回（第一選択）。"
        "■セラメクチン 15-30 mg/kg 外用 30日毎。■環境: 床材は全て廃棄し、ケージを次亜塩素酸で消毒。"
        "■⚠ 重度の疥癬は激しい掻痒→掻破に伴う痙攣発作→致死的となりうる。■同居個体も治療。"
        "■鎮痛: メロキシカム 0.3-0.5 mg/kg q24h。■⚠ 人獣共通 — ヒトに一過性の丘疹。"
        "■予後: イベルメクチンで良好。飼育群全体で対応する。（Quesenberry & Carpenter 2012）"
    )
}
C[("Sugar Glider", "Sarcoptic Mange (Severe)")] = {
    "treatment_ja": (
        "■イベルメクチン 0.2 mg/kg SC 14日毎×3-4回。■セラメクチン 6-18 mg/kg 外用 30日毎。■環境: ケージを徹底清掃。"
        "■支持療法: 衰弱例は輸液・栄養補給。■自咬に注意（エリザベスカラー）。■⚠ 人獣共通。■予後: 治療で良好。"
        "（Carpenter 6th ed）"
    )
}
C[("Degu", "Sarcoptic Mange")] = {
    "treatment_ja": (
        "■イベルメクチン 0.2-0.4 mg/kg SC 14日毎×3-4回。■セラメクチン（レボリューション）15 mg/kg 外用 30日毎。"
        "■環境: ケージを清掃し、木製・布製の床材は廃棄。■⚠ 人獣共通 — ヒトに一過性の病変、手袋を着用。"
        "■予後: 治療で良好。（Quesenberry & Carpenter 2012）"
    )
}
C[("Parakeet", "Knemidocoptic Mange – Severe")] = {
    "treatment_ja": (
        "■トリヒゼンダニ症と同様 — イベルメクチン 0.2 mg/kg 14日毎×3-4回。重度: 痂皮病変の二次感染には全身抗菌薬。"
        "イベルメクチンの効果発現後に痂皮をやさしく除去する。■予後: 良好。進行した嘴・脚の変形は残ることがある。"
        "（Chitty & Lierz 2008）"
    )
}

# ---- (b) both fields templated → curated JA + EN ----
_IVM_SMALL = (
    "イベルメクチン 0.2-0.4 mg/kg SC/PO 7-14日毎×3-4回、またはセラメクチン 6-18 mg/kg 外用 2-4週毎×2-3回",
    "ivermectin 0.2-0.4 mg/kg SC/PO q7-14d × 3-4, or selamectin 6-18 mg/kg topically q2-4 weeks × 2-3",
)
C[("Hamster", "Fur Mites (Demodex criceti)")] = {
    "treatment_ja": f"■{_IVM_SMALL[0]}。皮膚掻爬・セロハンテープで2回連続陰性まで継続。■高齢・副腎皮質機能亢進症・慢性疾患など基礎の免疫抑制を検索（ハムスターのニキビダニ症は基礎疾患の徴候であることが多い）。■床材交換・ケージ清掃、同居個体も確認。■フィプロニル・アミトラズ等の外用殺虫剤は小型齧歯類で毒性リスク — 避ける。（Quesenberry & Carpenter 4th ed; Carpenter 6th ed）",
    "treatment": f"■{_IVM_SMALL[1]}; continue until 2 consecutive negative scrapings/tape preps. ■Search for underlying immunosuppression (old age, hyperadrenocorticism, chronic disease) — hamster demodicosis is often a marker of systemic disease. ■Change bedding, clean the cage, check cage-mates. ■Avoid fipronil/amitraz-type topical insecticides (toxicity risk in small rodents). (Quesenberry & Carpenter 4th ed; Carpenter 6th ed)",
}
C[("Guinea Pig", "Demodex Mites")] = {
    "treatment_ja": "■Demodex caviae は稀 — 壊血病（ビタミンC欠乏）・ストレス・妊娠・ステロイドなど基礎の免疫抑制を検索。■イベルメクチン 0.2-0.5 mg/kg SC 7-10日毎、皮膚掻爬で2回連続陰性まで。■ビタミンC 10-30 mg/kg/日（治療中は50 mg/kg/日まで増量可）。■アミトラズは毒性リスクのため避ける。（Quesenberry & Carpenter 4th ed）",
    "treatment": "■Demodex caviae is uncommon — look for an immunosuppressive driver (scurvy/vitamin C deficiency, stress, pregnancy, corticosteroids). ■Ivermectin 0.2-0.5 mg/kg SC q7-10d until 2 consecutive negative scrapings. ■Vitamin C 10-30 mg/kg/day (up to 50 mg/kg/day while ill). ■Avoid amitraz (toxicity). (Quesenberry & Carpenter 4th ed)",
}
C[("Guinea Pig", "Fur Mites - Heavy Infestation")] = {
    "treatment_ja": "■Chirodiscoides caviae（被毛ダニ）: イベルメクチン 0.2-0.5 mg/kg SC 7-14日毎×3回、またはセラメクチン 15 mg/kg 外用 2-4週毎×2-3回。■同居個体も全頭治療、床材交換とケージ清掃。■重度寄生ではストレス・壊血病など基礎要因を確認しビタミンCを補給。■激しい掻痒を伴う場合は疥癬（Trixacarus caviae）を皮膚掻爬で除外する。（Quesenberry & Carpenter 4th ed）",
    "treatment": "■Chirodiscoides caviae (fur mite): ivermectin 0.2-0.5 mg/kg SC q7-14d × 3, or selamectin 15 mg/kg topically q2-4 weeks × 2-3. ■Treat all in-contact guinea pigs; change bedding and clean the cage. ■Heavy burdens suggest stress/scurvy — check husbandry and supplement vitamin C. ■If pruritus is intense, rule out Trixacarus caviae (sarcoptic mange) by skin scraping. (Quesenberry & Carpenter 4th ed)",
}
C[("Chinchilla", "Fur Mites")] = {
    "treatment_ja": "■チンチラの被毛ダニ（主にツメダニ類）は稀 — 皮膚糸状菌症・毛噛みを鑑別（セロハンテープ・毛検査・培養）。■セラメクチン 15 mg/kg 外用 30日毎×2-3回、またはイベルメクチン 0.2-0.4 mg/kg SC 7-14日毎×3回。■砂浴びの砂を交換し、ケージ・床材を清掃。■**フィプロニルは致死的 — 使用しない**。シャンプー・水浴は禁止（密な被毛が乾かず低体温・皮膚炎）。（Quesenberry & Carpenter 4th ed）",
    "treatment": "■Fur mites (mainly Cheyletiella-type) are uncommon in chinchillas — rule out dermatophytosis and fur-chewing (tape prep, trichogram, fungal culture). ■Selamectin 15 mg/kg topically q30d × 2-3, or ivermectin 0.2-0.4 mg/kg SC q7-14d × 3. ■Replace dust-bath material and clean cage/bedding. ■**Fipronil is fatal — never use.** Do not bathe or shampoo (the dense coat stays wet → hypothermia/dermatitis). (Quesenberry & Carpenter 4th ed)",
}
_HH = (
    "■イベルメクチン 0.2-0.4 mg/kg SC 14日毎×3回、またはセラメクチン 6-18 mg/kg 外用 2-4週毎×2-3回。フルララネル 15 mg/kg PO 単回の有効性報告あり（Romero 2017 Vet Dermatol）。",
    "■Ivermectin 0.2-0.4 mg/kg SC q14d × 3, or selamectin 6-18 mg/kg topically q2-4 weeks × 2-3. Single-dose fluralaner 15 mg/kg PO has been reported effective (Romero 2017 Vet Dermatol). ",
)
C[("Hedgehog", "Quill Mites (Chorioptes)")] = {
    "treatment_ja": _HH[0]
    + "■同居個体も治療、床材を全交換しケージを清掃。■痂皮・フケ・針の脱落が改善するまで2-4週毎に皮膚掻爬で再評価。■二次性の細菌・真菌感染（皮膚糸状菌症）を併発しやすい — 培養で確認。（Carpenter 6th ed; Quesenberry & Carpenter 4th ed）",
    "treatment": _HH[1]
    + "■Treat cage-mates, replace all bedding and clean the enclosure. ■Re-scrape every 2-4 weeks until crusting, scaling and quill loss resolve. ■Secondary bacterial or dermatophyte infection is common — confirm by culture. (Carpenter 6th ed; Quesenberry & Carpenter 4th ed)",
}
C[("Exotic Other", "Hedgehog Skin Mites (Caparinia tripilis)")] = {
    "treatment_ja": "■Caparinia tripilis はハリネズミで最も多い外部寄生虫（針の脱落・フケ・痂皮）。"
    + _HH[0]
    + "■同居個体も治療、床材を全交換。■2-4週毎の皮膚掻爬で陰性化を確認。二次性皮膚糸状菌症の併発に注意。（Carpenter 6th ed; Romero 2017）",
    "treatment": "■Caparinia tripilis is the most common hedgehog ectoparasite (quill loss, scaling, crusts). "
    + _HH[1]
    + "■Treat cage-mates and replace bedding. ■Confirm clearance by scraping every 2-4 weeks; watch for secondary dermatophytosis. (Carpenter 6th ed; Romero 2017)",
}
C[("Hedgehog", "Ear Mites")] = {
    "treatment_ja": "■耳介・耳道の痂皮と耳垢（Notoedres・Otodectes 等）: セラメクチン 6-18 mg/kg 外用 2-4週毎×2-3回、またはイベルメクチン 0.2-0.4 mg/kg SC 14日毎×3回。■耳道の痂皮・耳垢をやさしく洗浄。二次性の細菌・酵母性外耳炎は細胞診に基づき局所治療。■同居個体も治療。（Carpenter 6th ed）",
    "treatment": "■Pinnal/aural crusting and debris (Notoedres, Otodectes and others): selamectin 6-18 mg/kg topically q2-4 weeks × 2-3, or ivermectin 0.2-0.4 mg/kg SC q14d × 3. ■Gently clean crusts/debris; treat secondary bacterial/yeast otitis topically based on cytology. ■Treat cage-mates. (Carpenter 6th ed)",
}
C[("Degu", "Fur Mites (Demodex / Notoedres)")] = {
    "treatment_ja": f"■{_IVM_SMALL[0]}。皮膚掻爬で陰性化まで継続。■同居個体も治療、床材交換とケージ清掃。■ニキビダニの重度寄生は基礎の免疫抑制（糖尿病・ストレス）を検索。■フィプロニル等の外用殺虫剤は避ける。（Quesenberry & Carpenter 4th ed）",
    "treatment": f"■{_IVM_SMALL[1]}; continue until scrapings are negative. ■Treat cage-mates, change bedding, clean the cage. ■Heavy Demodex burdens warrant a search for immunosuppression (diabetes, stress). ■Avoid fipronil-type topical insecticides. (Quesenberry & Carpenter 4th ed)",
}
C[("Parakeet", "Scaly Leg Mites")] = {
    "treatment_ja": "■トリヒゼンダニ（Knemidokoptes）: イベルメクチン 0.2 mg/kg を頸部皮膚に滴下（または PO/IM）14日毎×3回。モキシデクチン外用も有効。■痂皮は効果発現後にやさしく除去（無理に剥がさない）。■止まり木を交換・清掃、同居鳥も確認。■重度・難治例は免疫抑制や栄養状態を評価。進行した脚・嘴の変形は残ることがある。（Ritchie & Harrison; Carpenter 6th ed）",
    "treatment": "■Knemidokoptes: ivermectin 0.2 mg/kg applied to the skin of the neck (or PO/IM) q14d × 3; topical moxidectin is also effective. ■Remove crusts gently once treatment takes effect (do not tear them off). ■Replace/clean perches and check flock-mates. ■Severe/refractory cases warrant assessment of immune and nutritional status; advanced leg/beak deformity may persist. (Ritchie & Harrison; Carpenter 6th ed)",
}
C[("Parakeet", "Air Sac Mite – Chronic Infestation")] = {
    "treatment_ja": "■気嚢ダニ（Sternostoma tracheacolum）: イベルメクチン 0.2 mg/kg 皮膚滴下/PO 14日毎×3回、またはモキシデクチン外用。■⚠ 重度寄生では駆除後に死滅したダニが気道を閉塞し急変することがある — 呼吸困難例は酸素室で安定化し、必要に応じ低用量から開始し投与後を監視。■二次性の細菌性気嚢炎は培養に基づき抗菌薬。■同居鳥も同時に治療。（Ritchie & Harrison; Carpenter 6th ed）",
    "treatment": "■Sternostoma tracheacolum: ivermectin 0.2 mg/kg spot-on/PO q14d × 3, or topical moxidectin. ■⚠ In heavy burdens dying mites can obstruct the airway after treatment — stabilise dyspnoeic birds in oxygen, consider starting low, and monitor after dosing. ■Treat secondary bacterial airsacculitis per culture. ■Treat all flock-mates at the same time. (Ritchie & Harrison; Carpenter 6th ed)",
}
C[("Parakeet", "Mite Infestation – Feather Mites")] = {
    "treatment_ja": "■羽ダニの多くは非病原性 — まず毛引き・PBFD・栄養性羽毛異常を鑑別。■ワクモ（Dermanyssus）は夜間に吸血し日中はケージの隙間に潜む — 夜間の観察で確認し、治療の主体はケージ・止まり木・巣箱の徹底清掃と交換（鳥体ではなく環境を処理）。■鳥体: イベルメクチン 0.2 mg/kg 皮膚滴下 14日毎×2-3回。■重度吸血による貧血の雛・小型鳥は支持療法。■ピレスロイド系の環境用スプレーは鳥を退避させて使用し、鳥体には噴霧しない。（Ritchie & Harrison; Carpenter 6th ed）",
    "treatment": "■Most feather mites are non-pathogenic — first rule out feather-destructive behaviour, PBFD and nutritional feather disease. ■Red mites (Dermanyssus) feed at night and hide in cage crevices by day — confirm by night inspection; treatment centres on thoroughly cleaning/replacing the cage, perches and nest box (treat the environment, not just the bird). ■Bird: ivermectin 0.2 mg/kg spot-on q14d × 2-3. ■Supportive care for anaemic chicks/small birds after heavy feeding. ■Use pyrethroid environmental sprays only with the bird removed — never spray the bird. (Ritchie & Harrison; Carpenter 6th ed)",
}
C[("Reptile", "Snake Mite Infestation (Ophionyssus natricis) - Severe")] = {
    "treatment_ja": "■ヘビダニ（Ophionyssus natricis）: 個体と飼育環境の同時治療が必須（ダニの大半は環境中）。■個体: イベルメクチン 0.2 mg/kg SC/PO 14日毎×2-3回（**リクガメ・ミズガメには禁忌、インディゴスネーク・一部のトカゲは感受性に注意**）。フィプロニルスプレーを布に含ませて体表を拭く方法も用いられる。■環境: 床材・レイアウトを全廃棄し、ケージを清掃・消毒、イベルメクチン希釈液（約5-10 mg/L）の噴霧。捕食性ダニ（Hypoaspis 等）の導入も選択肢。■重度例の貧血・脱水に輸液・支持療法。■ヘビダニはIBD・エロモナス感染の媒介となるため新規個体は検疫。（Mader 3rd ed; Carpenter 6th ed）",
    "treatment": "■Ophionyssus natricis: the animal and the enclosure must be treated together (most mites are off-host). ■Animal: ivermectin 0.2 mg/kg SC/PO q14d × 2-3 (**contraindicated in chelonians; use caution in indigo snakes and some lizards**); wiping the body with a cloth moistened with fipronil spray is also used. ■Enclosure: discard all substrate/furnishings, clean and disinfect, spray dilute ivermectin (~5-10 mg/L); predatory mites (Hypoaspis spp.) are an option. ■Fluids/supportive care for anaemia and dehydration in heavy infestations. ■Snake mites can transmit IBD and Aeromonas — quarantine new animals. (Mader 3rd ed; Carpenter 6th ed)",
}
C[("Exotic Other", "External Parasites (Mites/Fleas/Ticks)")] = {
    "treatment_ja": "■寄生虫の同定（セロハンテープ・皮膚掻爬・ダニの形態）と種の同定に基づいて薬剤を選ぶ — 外部寄生虫に駆虫薬（フェンベンダゾール・プラジクアンテル等の蠕虫用薬）は無効。■一般的な選択肢: セラメクチン外用、イベルメクチン 0.2-0.4 mg/kg（種による）。■種特異的な禁忌: **ウサギ・チンチラ等にフィプロニル（致死的）、リクガメ等のカメ類にイベルメクチン（致死的）、クモ・昆虫など無脊椎動物にイベルメクチン・殺ダニ剤全般（致死的）、猫・魚にペルメトリン**。■同居個体と飼育環境（床材・ケージ）を同時に処理。（Carpenter 6th ed）",
    "treatment": "■Choose the drug from the identified parasite (tape prep, skin scraping, mite morphology) and the host species — anthelmintics (fenbendazole, praziquantel) do nothing against ectoparasites. ■Common options: topical selamectin; ivermectin 0.2-0.4 mg/kg (species-dependent). ■Species-specific contraindications: **fipronil in rabbits/chinchillas (fatal), ivermectin in chelonians (fatal), ivermectin and any acaricide in invertebrates such as spiders/insects (fatal), permethrin in cats and fish.** ■Treat in-contact animals and the environment (substrate, cage) at the same time. (Carpenter 6th ed)",
}
C[("Exotic Other", "Mite Infestation (Tarantula)")] = {
    "treatment_ja": "■**イベルメクチン・フィプロニル・ピレスロイド等の殺ダニ剤・殺虫剤はクモ（節足動物）に致死的 — 絶対に使用しない**。■多くは床材由来の腐食性ダニ（宿主を直接害さない）で、過湿・食べ残しが増殖の原因 — 床材を全交換し、食べ残しを除去、湿度を種に適した範囲に下げる。■体表・口器周囲のダニは湿らせた綿棒・柔らかい筆で物理的に除去。■捕食性ダニ（Hypoaspis miles 等）を床材に導入する方法もある。■口器周囲の白い付着物は線虫（Panagrolaimidae）感染の可能性 — 鑑別する（予後不良）。（Pellett 2015; Carpenter 6th ed）",
    "treatment": "■**Ivermectin, fipronil, pyrethroids and other acaricides/insecticides are lethal to spiders (arthropods) — never use them.** ■Most are substrate-derived scavenger mites (not directly parasitic) that bloom with excess humidity and leftover prey — replace all substrate, remove food remains and lower humidity to the species-appropriate range. ■Remove mites from the body/mouthparts physically with a damp cotton swab or soft brush. ■Predatory mites (e.g. Hypoaspis miles) can be added to the substrate. ■White material around the mouthparts may instead be nematode (Panagrolaimidae) infection — differentiate (poor prognosis). (Pellett 2015; Carpenter 6th ed)",
}

# ---- (c) EN template on entries whose JA is already curated → EN translation ----
_BIRD_TAIL_EN = " Fipronil must not be used in birds (deaths reported); avoid organophosphate/carbamate insecticides and any spraying or fogging near the bird; dilute ivermectin for accurate dosing in very small birds. (Ritchie & Harrison; Carpenter 6th ed)"
_RODENT_TAIL_EN = " Fipronil (Frontline) is contraindicated in rabbits, guinea pigs, chinchillas and degus (convulsions and deaths reported) — never use dog/cat spot-ons. Oral penicillins/ampicillin/cephalosporins are contraindicated (fatal clostridial enterotoxaemia). (Quesenberry & Carpenter 4th ed; Carpenter 6th ed)"
C[("Bird", "Cnemidocoptes pilae (Scaly Leg Mite)")] = {
    "treatment": "Ivermectin 0.2 mg/kg PO or topically, every 7-10 days for 3-4 doses, is first-line and highly effective; topical moxidectin 0.2 mg/kg spot-on is an alternative. Never pick crusts off forcibly (bleeding, secondary infection) — soften with warm water and let them shed. Trim progressive beak deformity with a rotary tool. Examine and treat in-contact birds and clean/disinfect cage and perches."
    + _BIRD_TAIL_EN
}
C[("Bird", "Tracheal Mite (Sternostoma)")] = {
    "treatment": "Sternostoma tracheacolum (canaries/finches especially). Ivermectin 0.2-0.4 mg/kg PO or spot-on weekly × 2-3, or moxidectin 1 mg/kg PO weekly × 2-3 (longer acting); safe in canaries/finches, use care in psittacines. Supportive: enrofloxacin 15 mg/kg PO q12h × 7-10 days for secondary infection, saline nebulisation, humidity, warmth, assisted feeding and fluids. Diagnosis: transillumination of the trachea (small birds), tracheal wash. Treat all flock-mates, steam/hot-water clean cages, quarantine new birds. Prognosis good with early treatment; poor with airway obstruction."
    + _BIRD_TAIL_EN
}
C[("Bird", "Air Sac Mite")] = {
    "treatment": "Ivermectin 0.2 mg/kg PO or dorsal-neck spot-on every 10-14 days × 3 is standard; selamectin 6 mg/kg topically is also effective. For severe dyspnoea give oxygen and a bronchodilator (terbutaline 0.01 mg/kg IM) — dying mites can transiently worsen airway signs. Disinfect the environment and treat all flock-mates at once. Common in budgerigars and Java sparrows; recheck for reinfection."
    + _BIRD_TAIL_EN
}
C[("Bird", "Red Mite (Dermanyssus)")] = {
    "treatment": "Environmental control is the core: red mites feed at night and hide in cage crevices — strip and clean the cage, apply a pyrethrin-based spray to crevices with the bird removed, and scald perches/nest boxes; continue for 2-3 weeks to cover the life cycle. Bird: ivermectin 0.2 mg/kg PO, 2 doses 7 days apart. Severe anaemia (PCV <30%): fluids, iron, transfusion if needed."
    + _BIRD_TAIL_EN,
    "ja_replace": ("カルバリル5%パウダーの体表散布。", "（カーバメート系のカルバリル等を鳥体に散布しない — 毒性）"),
}
C[("Hamster", "Acariasis (Mite Infestation)")] = {
    "treatment": "Hamster acariasis (various ectoparasites). Ivermectin 0.2-0.4 mg/kg SC q10-14d × 3-4 is first-line and covers Demodex, Sarcoptes and Notoedres; selamectin 6-15 mg/kg topically q30d is an alternative. Identify the mite by skin scraping. Enrofloxacin 5-10 mg/kg PO q12h for secondary bacterial infection. Clean the environment and investigate underlying immunosuppression (e.g. hyperadrenocorticism, age). Avoid fipronil/amitraz-type insecticides. (Quesenberry & Carpenter 4th ed)"
}
C[("Rabbit", "Ear Mites (Psoroptes cuniculi)")] = {
    "treatment": "Psoroptes cuniculi. Ivermectin 0.2-0.4 mg/kg SC q10-14d × 3-4 is first-line; selamectin 6-18 mg/kg topically q30d is an alternative. Do NOT remove crusts forcibly (bleeding, severe pain) — let them soften and shed. Enrofloxacin 5-10 mg/kg PO q12h for secondary infection; meloxicam 0.3-0.5 mg/kg PO q24h for pain. Clean the environment."
    + _RODENT_TAIL_EN
}
C[("Rabbit", "Cheyletiella Mange (Fur Mites)")] = {
    "treatment": "Cheyletiella parasitovorax ('walking dandruff', heavy scaling). Ivermectin 0.2-0.4 mg/kg SC q10-14d × 3-4 is first-line; selamectin (Revolution) 6-18 mg/kg topically q30d × 3 is an alternative. Environmental cleaning matters (mites survive ~10 days off the host); treat in-contact animals at the same time; enrofloxacin for secondary infection. Zoonotic (transient pruritic papules in people)."
    + _RODENT_TAIL_EN
}
_GP_MITE_JA_TAIL = "■⚠ フィプロニル（フロントライン®）はモルモットに禁忌（けいれん・死亡例）— 犬猫用スポットオンを流用しない。経口ペニシリン・アンピシリン・セファロスポリンも禁忌（致死的腸炎）。（Quesenberry & Carpenter 4th ed; Carpenter 6th ed）"
C[("Guinea Pig", "Chirodiscoides caviae Mite")] = {
    "treatment_ja": "■Chirodiscoides caviae（被毛ダニ）: 体幹後部の被毛に付着し、軽度の掻痒・脱毛・フケ（無症状のことも多い）。セロハンテープ・被毛検査で診断。■イベルメクチン 0.2-0.5 mg/kg SC 7-14日毎×3回、またはセラメクチン 15 mg/kg 外用 2-4週毎×2-3回。■同居個体を全頭治療、床材交換・ケージ清掃。■激しい掻痒は疥癬（Trixacarus caviae）を皮膚掻爬で除外。■ストレス・壊血病を確認しビタミンCを補給。"
    + _GP_MITE_JA_TAIL,
    "treatment": "■Chirodiscoides caviae (fur mite): clings to hairs over the caudal trunk; mild pruritus, alopecia and scaling (often subclinical). Diagnose by tape prep/trichogram. ■Ivermectin 0.2-0.5 mg/kg SC q7-14d × 3, or selamectin 15 mg/kg topically q2-4 weeks × 2-3. ■Treat all in-contact guinea pigs; change bedding and clean the cage. ■Intense pruritus → rule out Trixacarus caviae by skin scraping. ■Check for stress/scurvy and supplement vitamin C."
    + _RODENT_TAIL_EN,
}
C[("Guinea Pig", "Ear Mite Infestation")] = {
    "treatment_ja": "■耳介・耳道の痂皮と耳垢（モルモットでは Trixacarus 等の疥癬ダニの耳介病変や、同居ウサギ由来の Psoroptes を含む）: 耳垢の鏡検・皮膚掻爬で同定。■イベルメクチン 0.2-0.5 mg/kg SC 7-14日毎×3回、またはセラメクチン 15 mg/kg 外用 2-4週毎×2-3回。■痂皮は無理に剥がさない（出血・疼痛）。耳道はやさしく洗浄し、二次性外耳炎は細胞診に基づき局所治療。■斜頸・眼振を伴えば中耳炎・内耳炎を評価（X線・CT）。■同居個体も治療。"
    + _GP_MITE_JA_TAIL,
    "treatment": "■Pinnal/aural crusting and debris (in guinea pigs often Trixacarus or other mange mites on the pinnae, or Psoroptes from in-contact rabbits): identify by otic cytology/scraping. ■Ivermectin 0.2-0.5 mg/kg SC q7-14d × 3, or selamectin 15 mg/kg topically q2-4 weeks × 2-3. ■Do not pull crusts off (bleeding, pain); clean the canal gently and treat secondary otitis topically per cytology. ■Head tilt/nystagmus → evaluate for otitis media/interna (radiographs/CT). ■Treat in-contact animals."
    + _RODENT_TAIL_EN,
}

# ---- (d) species-mismatched ectoparasite templates (2nd wave) ----
# EN "Ectoparasite treatment: Ivermectin 0.2-0.4 mg/kg SC… Moxidectin/imidacloprid
# (Advocate)…" is a mammal template that was also stamped on birds, reptiles and
# **tortoises (ivermectin is fatal in chelonians)**; JA「…糞便PCR/直接鏡検/フローテ
# ーション法…Coccidia: トルトラズリル…」 is an endoparasite work-up on mite/tick entries.
FORCE_EN_MARKS = ("Ectoparasite treatment: Ivermectin 0.2-0.4 mg/kg SC", "Individual deworming—fipronil spray")

_AIRSAC = C[("Parakeet", "Air Sac Mite – Chronic Infestation")]
_FEATHER = C[("Parakeet", "Mite Infestation – Feather Mites")]
_SNAKE_MITE = C[("Reptile", "Snake Mite Infestation (Ophionyssus natricis) - Severe")]
for sp in ("Parakeet", "Parrot"):
    C[(sp, "Tracheal Mite (Sternostoma)")] = dict(_AIRSAC)
    C[(sp, "Air Sac Mite")] = dict(_AIRSAC)
    C[(sp, "Feather Mites")] = dict(_FEATHER)
for sp in ("Reptile", "Snake", "Lizard"):
    C[(sp, "Mite Infestation (Ophionyssus)")] = dict(_SNAKE_MITE)
C[("Snake", "Snake Mite (Ophionyssus natricis)")] = dict(_SNAKE_MITE)

C[("Tortoise", "Mite Infestation (Ophionyssus)")] = {
    "treatment_ja": "■**イベルメクチンはリクガメ・ミズガメ（カメ類）に禁忌 — 弛緩性麻痺・死亡**。■ダニ・マダニは鉗子・湿らせた綿棒で物理的に除去し、甲羅の継ぎ目・四肢の付け根・頸部のひだを丁寧に確認。■飼育環境の処理が主体: 床材・シェルターを全交換し、ケージを熱湯・蒸気で清掃（ダニの大半は環境中）。■外用殺ダニ剤（フィプロニル等）を用いる場合は獣医師の判断で少量を局所に、吸入・経口曝露を避ける。■重度寄生の貧血・脱水には輸液と適温（POTZ）での支持療法。■新規導入個体は検疫。（Mader 3rd ed; Carpenter 6th ed）",
    "treatment": "■**Ivermectin is contraindicated in tortoises and turtles (chelonians) — flaccid paralysis and death.** ■Remove mites/ticks physically with forceps or a damp cotton swab, checking scute seams, limb pockets and neck folds. ■Environmental treatment is the core: replace all substrate and hides and steam/hot-water clean the enclosure (most mites are off-host). ■If a topical acaricide (e.g. fipronil) is used, apply sparingly to a small area at the veterinarian's discretion, avoiding inhalation/ingestion. ■Fluids and supportive care at the preferred optimum temperature zone (POTZ) for anaemic/dehydrated animals. ■Quarantine new animals. (Mader 3rd ed; Carpenter 6th ed)",
}
C[("Tortoise", "Tick Infestation")] = {
    "treatment_ja": "■**イベルメクチンはカメ類に禁忌（致死的）**。■マダニは口器ごと鉗子でゆっくり垂直に引き抜く（口器を残すと肉芽腫・感染）。甲羅の継ぎ目・四肢・総排泄腔周囲を確認。■創部はクロルヘキシジン希釈液で消毒し、二次感染があれば抗菌薬。■輸入・野外採集個体のマダニ（Amblyomma 等）はハートウォーター（Ehrlichia ruminantium）等の家畜伝染病の媒介となりうる — 除去したマダニは廃棄し、検疫・行政相談を考慮。■床材交換と環境清掃。（Mader 3rd ed; Carpenter 6th ed）",
    "treatment": "■**Ivermectin is contraindicated in chelonians (fatal).** ■Remove ticks slowly and perpendicularly with forceps, mouthparts included (retained mouthparts cause granulomas/infection); check scute seams, limbs and the vent. ■Disinfect bite sites with dilute chlorhexidine; antibiotics only for secondary infection. ■Ticks on imported/wild-caught tortoises (e.g. Amblyomma) can carry livestock pathogens such as heartwater (Ehrlichia ruminantium) — destroy removed ticks, quarantine and consider regulatory advice. ■Replace substrate and clean the enclosure. (Mader 3rd ed; Carpenter 6th ed)",
}
_REPT_TICK = {
    "treatment_ja": "■マダニは口器ごと鉗子でゆっくり垂直に引き抜く（口器を残すと肉芽腫・感染）。鱗の間・眼の周囲・総排泄腔周囲を確認。■多数寄生では個体にイベルメクチン 0.2 mg/kg SC/PO 14日毎×2回（インディゴスネーク・一部のトカゲは感受性に注意、**カメ類には禁忌**）。■床材交換と環境清掃、新規導入個体は検疫（マダニはヘモグレガリン等の血液寄生虫の媒介）。■二次感染は創部消毒と必要時の抗菌薬。（Mader 3rd ed; Carpenter 6th ed）",
    "treatment": "■Remove ticks slowly and perpendicularly with forceps, mouthparts included; check between scales, around the eyes and the vent. ■Heavy burdens: ivermectin 0.2 mg/kg SC/PO q14d × 2 (caution in indigo snakes and some lizards; **contraindicated in chelonians**). ■Replace substrate, clean the enclosure and quarantine new animals (ticks transmit haemogregarines and other blood parasites). ■Clean bite wounds; antibiotics only for secondary infection. (Mader 3rd ed; Carpenter 6th ed)",
}
for sp in ("Reptile", "Snake", "Lizard"):
    C[(sp, "Tick Infestation")] = dict(_REPT_TICK)
C[("Amphibian", "Tick Infestation")] = {
    "treatment_ja": "■マダニ・ダニは鉗子で物理的に除去する。■両生類の皮膚は透過性が高く外用殺虫剤・殺ダニ剤（フィプロニル・ピレスロイド等）は経皮吸収で中毒の危険 — 原則使用しない。■除去部位は清潔な脱塩素水で洗浄し、二次感染（エロモナス等）を監視。■水質・床材を改善し、野外採集個体は検疫。（Wright & Whitaker, Amphibian Medicine; Carpenter 6th ed）",
    "treatment": "■Remove ticks/mites physically with forceps. ■Amphibian skin is highly permeable — topical insecticides/acaricides (fipronil, pyrethroids) risk toxic absorption and are generally avoided. ■Rinse sites with clean dechlorinated water and watch for secondary infection (e.g. Aeromonas). ■Improve water quality/substrate and quarantine wild-caught animals. (Wright & Whitaker, Amphibian Medicine; Carpenter 6th ed)",
}
C[("Parrot", "Tick Infestation")] = {
    "treatment_ja": "■マダニは口器ごと鉗子で除去（屋外禽舎の鳥に多い）。■多数寄生にはイベルメクチン 0.2 mg/kg 皮膚滴下/PO 14日毎×2回。■**フィプロニルは鳥に使用しない**。ピレスロイド系の環境スプレーは鳥を退避させて使用。■重度吸血による貧血には支持療法。■禽舎周囲の草刈り・野生動物の侵入防止。（Ritchie & Harrison; Carpenter 6th ed）",
    "treatment": "■Remove ticks with forceps, mouthparts included (mostly birds in outdoor aviaries). ■Heavy burdens: ivermectin 0.2 mg/kg spot-on/PO q14d × 2. ■**Do not use fipronil in birds**; use pyrethroid environmental sprays only with birds removed. ■Supportive care for anaemia. ■Mow around aviaries and exclude wildlife. (Ritchie & Harrison; Carpenter 6th ed)",
}
_MAMMAL_TAIL_JA = "■同居動物も治療し、床材交換・ケージ清掃。■フィプロニル・アミトラズ等の外用殺虫剤は小型哺乳類で毒性リスク — 避ける。（Carpenter 6th ed; Quesenberry & Carpenter 4th ed）"
_MAMMAL_TAIL_EN = " ■Treat in-contact animals; change bedding and clean the cage. ■Avoid fipronil/amitraz-type topical insecticides (toxicity risk in small mammals). (Carpenter 6th ed; Quesenberry & Carpenter 4th ed)"
C[("Ferret", "Ear Mites (Otodectes)")] = {
    "treatment_ja": "■ミミヒゼンダニ（Otodectes cynotis）: セラメクチン 6-18 mg/kg 外用 30日毎×2-3回、またはイベルメクチン 0.2-0.4 mg/kg SC 14日毎×3回。■黒褐色の耳垢をやさしく洗浄し、二次性外耳炎は細胞診に基づき局所治療。■**同居の猫・犬も全頭治療**（伝染源となる）。■フィプロニルは避ける。（Quesenberry & Carpenter 4th ed; Carpenter 6th ed）",
    "treatment": "■Otodectes cynotis: selamectin 6-18 mg/kg topically q30d × 2-3, or ivermectin 0.2-0.4 mg/kg SC q14d × 3. ■Gently clean the dark brown debris; treat secondary otitis topically per cytology. ■**Treat all in-contact cats and dogs** (reservoir). ■Avoid fipronil. (Quesenberry & Carpenter 4th ed; Carpenter 6th ed)",
}
C[("Hedgehog", "Ear Mite Infestation")] = dict(C[("Hedgehog", "Ear Mites")])
C[("Hedgehog", "Caparinia Mange (Severe)")] = {
    "treatment_ja": "■Caparinia tripilis の重度寄生（広範な針の脱落・痂皮・体重減少）。"
    + _HH[0]
    + "■衰弱例は輸液・保温・強制給餌。■二次性の細菌感染・皮膚糸状菌症を培養で確認し治療。■2-4週毎の皮膚掻爬で陰性化を確認。"
    + _MAMMAL_TAIL_JA,
    "treatment": "■Severe Caparinia tripilis infestation (extensive quill loss, crusting, weight loss). "
    + _HH[1]
    + "■Fluids, warmth and assisted feeding for debilitated animals. ■Culture for and treat secondary bacterial infection/dermatophytosis. ■Re-scrape every 2-4 weeks until negative."
    + _MAMMAL_TAIL_EN,
}
C[("Hedgehog", "Demodex Mange")] = {
    "treatment_ja": "■ニキビダニ症はハリネズミでは稀 — 基礎の免疫抑制（腫瘍・慢性疾患・加齢・ステロイド）を検索。■イベルメクチン 0.2-0.4 mg/kg SC 7-14日毎、またはセラメクチン 6-18 mg/kg 外用 2-4週毎、皮膚掻爬で2回連続陰性まで。■アミトラズは毒性リスクのため避ける。"
    + _MAMMAL_TAIL_JA,
    "treatment": "■Demodicosis is uncommon in hedgehogs — search for immunosuppression (neoplasia, chronic disease, age, corticosteroids). ■Ivermectin 0.2-0.4 mg/kg SC q7-14d or selamectin 6-18 mg/kg topically q2-4 weeks until 2 consecutive negative scrapings. ■Avoid amitraz (toxicity)."
    + _MAMMAL_TAIL_EN,
}
C[("Hedgehog", "Tick Infestation")] = {
    "treatment_ja": "■マダニは口器ごと鉗子で除去（針の間・耳介・顔面を確認）。■多数寄生にはイベルメクチン 0.2-0.4 mg/kg SC 14日毎×2回、またはセラメクチン 6-18 mg/kg 外用。■屋外で保護した個体はマダニ媒介性疾患（人獣共通を含む）に注意し、手袋を着用。■貧血・衰弱には支持療法。"
    + _MAMMAL_TAIL_JA,
    "treatment": "■Remove ticks with forceps, mouthparts included (check between spines, pinnae and face). ■Heavy burdens: ivermectin 0.2-0.4 mg/kg SC q14d × 2, or selamectin 6-18 mg/kg topically. ■Rescued wild hedgehogs can carry tick-borne (including zoonotic) pathogens — wear gloves. ■Supportive care for anaemia/debility."
    + _MAMMAL_TAIL_EN,
}
# Bird EN-only fixes (JA already curated): bird-specific EN for the mammal template
for sp in ("Parakeet", "Parrot"):
    C[(sp, "Red Mite (Dermanyssus)")] = {"treatment": C[("Bird", "Red Mite (Dermanyssus)")]["treatment"]}
    C[(sp, "Knemidocoptes Mange (Scaly Face)")] = {
        "treatment": C[("Bird", "Cnemidocoptes pilae (Scaly Leg Mite)")]["treatment"]
    }
C[("Parakeet", "Scaly Face Mite (Knemidocoptes)")] = {
    "treatment": C[("Bird", "Cnemidocoptes pilae (Scaly Leg Mite)")]["treatment"]
}

# ---- (e) tortoise EN text that still recommends ivermectin (fatal in chelonians) ----
_NO_IVM = "Ivermectin is contraindicated in chelonians (flaccid paralysis/death) — do not use. "
CHELONIAN_EN_REPLACE = (
    ("Ivermectin 0.2 mg/kg SC/PO (residual larvae). ", _NO_IVM),
    ("Ivermectin 0.2 mg/kg SC/PO single dose, repeat 14d (limited efficacy for acanthocephalans). ", _NO_IVM),
    (
        "Ivermectin 0.2 mg/kg SC/PO every 14 days for 2-3 treatments (CAUTION: safety established in chelonians — dose carefully). ",
        "Levamisole 10 mg/kg SC/ICe, repeat in 14 days, is an alternative. " + _NO_IVM,
    ),
    (
        "Pharmacotherapy: Ivermectin 0.2 mg/kg SC/PO every 14 days for 3 treatments (limited efficacy). ",
        "Pharmacotherapy (limited efficacy): " + _NO_IVM,
    ),
    ("Ivermectin 0.2 mg/kg PO/SC q14 days×3 (use cautiously in chelonians—adverse reports). ", _NO_IVM),
)
CHELONIAN_SPECIES = ("Tortoise",)

# ---- (f) module-only entries (no JSON overlay row): patch api/species/*.py ----
SPECIES_DIR = ROOT / "api" / "species"
_HANNEMANIA = {
    "treatment_ja": "■Hannemania はツツガムシ科の幼虫が皮下に被嚢し、赤〜橙色の小結節を形成する（カエル・サンショウウオ、野外採集個体・土壌由来）。■多くは病原性が低く経過観察でよいが、多数・炎症・二次感染例は麻酔下で結節を切開し幼虫を摘出、創部を清潔に保つ。■両生類の皮膚は透過性が高く、外用殺ダニ剤・殺虫剤は中毒の危険 — 原則使用しない。■床材（野外土壌）を交換し、新規個体は検疫。（Wright & Whitaker, Amphibian Medicine; Carpenter 6th ed）",
    "treatment": "■Hannemania are trombiculid larvae that encyst under the skin, forming red-orange nodules (frogs/salamanders; wild-caught animals, outdoor soil). ■Most are of low pathogenicity and can be monitored; with many nodules, inflammation or secondary infection, incise and remove larvae under anaesthesia and keep wounds clean. ■Amphibian skin is highly permeable — topical acaricides/insecticides risk toxicity and are generally avoided. ■Replace soil substrate and quarantine new animals. (Wright & Whitaker, Amphibian Medicine; Carpenter 6th ed)",
}
_HAM_NOTO = {
    "treatment_ja": "■Notoedres（耳介・鼻・陰部の痂皮と掻痒）: イベルメクチン 0.2-0.4 mg/kg SC 7-14日毎×3回、またはセラメクチン 6-15 mg/kg 外用 30日毎×2-3回。■皮膚掻爬で診断し、陰性化を確認。■高齢・副腎皮質機能亢進症など基礎の免疫抑制を検索。"
    + _MAMMAL_TAIL_JA,
    "treatment": "■Notoedres (crusting and pruritus of pinnae, nose and genitals): ivermectin 0.2-0.4 mg/kg SC q7-14d × 3, or selamectin 6-15 mg/kg topically q30d × 2-3. ■Diagnose and confirm clearance by skin scraping. ■Look for immunosuppression (age, hyperadrenocorticism)."
    + _MAMMAL_TAIL_EN,
}
MODULE_PATCH: dict[tuple[str, str], dict[str, str]] = {
    ("amphibian", "Mite Infestation (Hannemania)"): _HANNEMANIA,
    ("bird", "Air Sac Mites (Sternostoma tracheacolum)"): _AIRSAC,
    ("bird", "Tracheal Mites (Sternostoma – Non-Finch Species)"): _AIRSAC,
    ("parakeet", "Air Sac Mites (Sternostoma) - Parakeet"): _AIRSAC,
    ("bird", "Knemidocoptes (Scaly Face/Leg Mites)"): C[("Parakeet", "Scaly Leg Mites")],
    ("parrot", "Knemidocoptes Mite Infestation (Scaly Face/Leg)"): C[("Parakeet", "Scaly Leg Mites")],
    ("ferret", "Ear Mites (Otodectes cynotis)"): C[("Ferret", "Ear Mites (Otodectes)")],
    ("guinea_pig", "Fur Mites (Chirodiscoides caviae)"): C[("Guinea Pig", "Chirodiscoides caviae Mite")],
    ("guinea_pig", "Sarcoptic Mange (Trixacarus caviae)"): {
        "treatment_ja": C[("Guinea Pig", "Trixacarus caviae (Sarcoptic Mange) - Severe")]["treatment_ja"]
    },
    ("hamster", "Ear Mites (Notoedres)"): _HAM_NOTO,
    ("lizard", "Mite Infestation (Ectoparasites)"): _SNAKE_MITE,
    ("snake", "Snake Mites (Ophionyssus natricis)"): _SNAKE_MITE,
    ("bird", "Red Mites (Dermanyssus gallinae)"): {
        "treatment": C[("Bird", "Red Mite (Dermanyssus)")]["treatment"],
        "treatment_ja": "■ワクモ（Dermanyssus gallinae）は夜間に吸血し、日中はケージの隙間・止まり木・巣箱に潜む — 治療の主体は環境: ケージを分解清掃し、鳥を退避させて隙間にピレスリン系スプレー、止まり木・巣箱は熱湯消毒または交換。2-3週間継続して生活環をカバー。■鳥体: イベルメクチン 0.2 mg/kg PO または皮膚滴下、7日間隔で2回。■重度貧血（PCV<30%）は輸液・鉄補給、必要に応じ輸血。■フィプロニル・有機リン系・カーバメート系は鳥に使用しない。（Ritchie & Harrison; Carpenter 6th ed）",
    },
}
_GENERIC_MOD_JA = "糞便PCR/直接鏡検/フローテーション法で原因虫種を特定"
_GENERIC_MOD_EN = (
    "Appropriate antiparasitic medication, environmental cleaning",
    "Species-appropriate antiparasitic medication, repeated treatments",
)


def patch_modules(write: bool) -> int:
    changed = 0
    by_file: dict[str, list] = {}
    for (sp, name), spec in MODULE_PATCH.items():
        by_file.setdefault(sp, []).append((name, spec))
    for sp, items in by_file.items():
        path = SPECIES_DIR / f"{sp}_diseases.py"
        lines = path.read_text(encoding="utf-8").split("\n")
        for name, spec in items:
            start = next(
                i for i, ln in enumerate(lines) if ln.strip() == f'"name": {json.dumps(name, ensure_ascii=False)},'
            )
            end = next((i for i in range(start + 1, len(lines)) if lines[i].strip().startswith('"name": ')), len(lines))
            for i in range(start, end):
                st = lines[i].strip()
                indent = lines[i][: len(lines[i]) - len(lines[i].lstrip())]
                if st.startswith('"treatment": ') and "treatment" in spec and any(m in st for m in _GENERIC_MOD_EN):
                    lines[i] = indent + '"treatment": ' + json.dumps(spec["treatment"], ensure_ascii=False) + ","
                    changed += 1
                elif st.startswith('"treatment_ja": ') and "treatment_ja" in spec and _GENERIC_MOD_JA in st:
                    lines[i] = indent + '"treatment_ja": ' + json.dumps(spec["treatment_ja"], ensure_ascii=False) + ","
                    changed += 1
        if write:
            path.write_text("\n".join(lines), encoding="utf-8")
    return changed


def apply(data: list[dict]) -> int:
    changed = 0
    for d in data:
        if d.get("species") in CHELONIAN_SPECIES:
            en = d.get("treatment") or ""
            for old, new in CHELONIAN_EN_REPLACE:
                if old in en:
                    en = en.replace(old, new)
            if en != (d.get("treatment") or ""):
                d["treatment"] = en
                changed += 1
        spec = C.get((d.get("species"), d.get("name")))
        if not spec:
            continue
        cur = d.get("treatment_ja") or ""
        if "ja_replace" in spec and spec["ja_replace"][0] in cur:
            d["treatment_ja"] = cur = cur.replace(*spec["ja_replace"])
            changed += 1
        if (
            "treatment_ja" in spec
            and (not cur or any(m in cur for m in TEMPLATE_MARKS_JA))
            and cur != spec["treatment_ja"]
        ):
            d["treatment_ja"] = spec["treatment_ja"]
            changed += 1
        en = d.get("treatment") or ""
        if (
            "treatment" in spec
            and (not en or TEMPLATE_MARK_EN in en or any(m in en for m in FORCE_EN_MARKS))
            and en != spec["treatment"]
        ):
            d["treatment"] = spec["treatment"]
            changed += 1
        if "treatment_append" in spec and "Bravecto Plus" not in en:
            d["treatment"] = en.rstrip() + spec["treatment_append"]
            changed += 1
    return changed


def main() -> None:
    raw = JSON_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    found = {(d.get("species"), d.get("name")) for d in data}
    missing = [k for k in C if k not in found]
    if missing:
        raise SystemExit(f"missing keys: {missing}")
    n = apply(data)
    m = patch_modules("--apply" in sys.argv)
    print(f"fields changed: {n} (json) + {m} (modules)")
    if "--apply" in sys.argv and n:
        JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    main()
