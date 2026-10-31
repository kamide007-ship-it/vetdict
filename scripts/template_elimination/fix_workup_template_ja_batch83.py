"""2026-10 第83弾: 英語治療文はキュレート済みなのに日本語治療文が汎用ワークアップ・
テンプレート（「…正確な臨床評価（病歴、身体検査、CBC・生化学、画像）から治療方針を決定」
＋輸液・メサドンの定型支持療法）のままだった高頻度疾患の是正。

日本語は既存の英語キュレート文の忠実な訳（用量・期間・閾値は英語と同一 — 数値トークンを
自動照合）。馬 PSSM は英語側も汎用テンプレート（小型哺乳類の参考書・馬に不適切な
メロキシカム用量）だったため、日英とも教科書準拠で記述（Valberg 2018 Vet Clin North Am
Equine Pract; Ribeiro 2004; Firshman 2003; McCue 2008）。

使い方: python3 -m scripts.template_elimination.fix_workup_template_ja_batch83 --apply
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"
TEMPLATE_MARK = "から治療方針を決定"

JA: dict[tuple[str, str], str] = {
    ("Dog", "Benign Prostatic Hyperplasia (BPH)"): (
        "去勢: 第一選択（3ヶ月以内に95%が消退）。内科療法（繁殖に用いる未去勢犬）: "
        "デスロレリン（スプレソリン）4.7 mg SCインプラント（GnRHアゴニスト）、フィナステリド 0.1-0.5 mg/kg "
        "PO q24h（5α-還元酵素阻害薬）、酢酸オサテロン 0.25-0.5 mg/kg PO q24h×7日。併発症の治療: 尿路感染症、"
        "前立腺膿瘍（ドレナージ＋抗菌薬）。モニタリング: 超音波による前立腺サイズ、尿検査。予後: 去勢で極めて良好。"
        "内科療法は有効だが一時的。（Brendler 1983, Johnston 2001）"
    ),
    ("Dog", "Cataracts"): (
        "外科: 超音波水晶体乳化吸引術＋眼内レンズ（IOL）挿入がゴールドスタンダード。術前: ERG（網膜機能の確認）、"
        "眼球超音波検査、ぶどう膜炎・糖尿病のコントロール。術後: 1%酢酸プレドニゾロン点眼 q6h を数ヶ月かけて漸減、"
        "抗菌薬点眼 q6-8h、経口NSAIDs。エリザベスカラー 2-4週。内科: 水晶体起因性ぶどう膜炎の抗炎症管理"
        "（NSAIDs点眼、プレドニゾロン）。糖尿病性白内障にはアルドース還元酵素阻害薬（Kinostat、予防目的）。"
        "予後: 乳化吸引術の成功率85-95%。糖尿病性白内障はやや低い。手術しない場合は水晶体起因性ぶどう膜炎・"
        "緑内障のリスク。（Gelatt 2013, Williams 2004）"
    ),
    ("Dog", "Central Diabetes Insipidus"): (
        "デスモプレシン（DDAVP）: 1-4滴（1.5-4 μg）を点鼻または結膜嚢内に q12-24h。経口: 0.05-0.2 mg PO q12h。"
        "水制限試験: 診断的（DDAVPに反応すれば中枢性で腎性と鑑別）。常に自由飲水させる。原因: 特発性、外傷、"
        "下垂体腫瘍、術後。MRI: 下垂体領域の評価。クロロチアジド 20-40 mg/kg PO q12h（軽症例 — 逆説的抗利尿作用）。"
        "モニタリング: 尿比重、血清ナトリウム、飲水量・尿量。予後: 特発性でDDAVP使用 — 極めて良好（正常寿命）。"
        "腫瘍関連 — 腫瘍による。（Feldman 2015）"
    ),
    ("Dog", "Diabetes Insipidus"): (
        "中枢性尿崩症: デスモプレシン（DDAVP）0.1-0.2 mL 点鼻 q12h、または 0.05-0.2 mg PO q12h、または "
        "1-4 μg SC q12-24h。飲水量と尿濃縮に基づき用量調整。腎性尿崩症: サイアザイド系利尿薬 — "
        "ヒドロクロロチアジド 2-4 mg/kg PO q12h（逆説的抗利尿作用）。低ナトリウム食。自由飲水（極めて重要）。"
        "基礎疾患の治療: 下垂体腫瘍（中枢性）、腎疾患、高カルシウム血症（腎性）。水制限試験: 診断目的（監視下で実施）。"
        "モニタリング: 尿比重、飲水量、血清Na。予後: 中枢性でDDAVP使用 — 極めて良好。腎性 — 原因による。"
        "（Harb 1996, Nichols 2001）"
    ),
    ("Cat", "Hypokalemia"): (
        "補充: KCl 静注（輸液中 20-40 mEq/L — 速度は重症度による）。静注は決して 0.5 mEq/kg/h を超えない"
        "（不整脈リスク）。経口: グルコン酸カリウム 2-4 mEq/頭 PO q12h（慢性）。クエン酸カリウム: 代謝性アシドーシス"
        "併発時。腎性カリウム喪失: 慢性腎臓病（猫で最多の原因）、閉塞解除後利尿。食事: 腎臓病用療法食（カリウム添加）。"
        "その他の原因: 糖尿病性ケトアシドーシス、ループ利尿薬、嘔吐、下痢、低マグネシウム血症。臨床徴候: 筋力低下、"
        "頸部腹側屈曲（猫の古典的徴候）、イレウス。モニタリング: 血清K+、心電図。予後: 適切な補充で良好。"
        "基礎疾患に対処する。（DiBartola 2006, Theisen 1997）"
    ),
    ("Cat", "Eclampsia (Puerperal Hypocalcemia)"): (
        "緊急疾患。10%グルコン酸カルシウム: 0.5-1 mL/kg を10-20分かけて緩徐に静注（心電図を監視 — 徐脈・不整脈で"
        "中止）。その後 SC 維持: 希釈したグルコン酸カルシウムを SC q6-8h。経口カルシウム: 炭酸カルシウム "
        "50-100 mg/kg/日 PO（維持）。カルシトリオール 20-30 ng/kg PO q24h。子猫を離す: 人工哺育または補助哺乳"
        "（授乳負荷の軽減）。可能なら授乳を減らす（3-4週齢から補助給餌）。周産期（妊娠後期または授乳初期）に発症。"
        "徴候: 振戦、テタニー、痙攣、高体温。モニタリング: イオン化カルシウム、心電図。予後: 迅速なカルシウム投与で"
        "極めて良好。未治療では致死的。（Drobatz 2000, Feldman 2015）"
    ),
    ("Dog", "Myxomatous Mitral Valve Degeneration (Early Stage)"): (
        "ACVIM ステージB1（心雑音あり・心拡大なし）: 心臓薬の適応なし。年1回の心エコー＋胸部X線で経過観察。"
        "適正体重と適度な運動を維持。ACVIM ステージB2（心拡大あり・前臨床期）: ピモベンダン 0.25-0.3 mg/kg PO q12h"
        "（EPIC試験でうっ血性心不全の発症を15ヶ月遅延）。心エコー q6ヶ月、LA:Ao比と LVIDDN を監視。"
        "食事: 中等度のナトリウム制限、オメガ3脂肪酸。自宅での安静時呼吸数のモニタリングを飼い主指導"
        "（睡眠時の正常は30回/分未満）。好発犬種: キャバリア・キング・チャールズ・スパニエル、ダックスフンド、チワワ。"
    ),
    ("Cat", "Cryptococcosis"): (
        "フルコナゾール 50-100 mg/頭 PO q12h（鼻腔型・皮膚型の第一選択）。イトラコナゾール 5-10 mg/kg PO q12h"
        "（代替 — 中枢移行は劣る）。中枢神経病変: フルコナゾールを優先（中枢移行が最良）＋アムホテリシンB脂質複合体 "
        "1 mg/kg IV q48h（導入）。重症・中枢型はフルコナゾール＋アムホテリシンBの併用。期間: 抗原価陰性化後さらに"
        "1-2ヶ月（総計6-18ヶ月となることが多い）。鼻腔肉芽腫: 外科的減量が必要な場合がある。モニタリング: 血清"
        "クリプトコッカス抗原価を q2-3ヶ月（治療期間の目安）。アムホテリシンB使用時は腎機能。猫で最も多い全身性真菌症。"
        "予後: 鼻腔型 — 良好（70-80%治癒）。中枢型 — 慎重。（Trivedi 2011, Sykes 2014）"
    ),
    ("Dog", "Cryptococcosis"): (
        "フルコナゾール 5-10 mg/kg PO q12h（第一選択、中枢移行が良好）。イトラコナゾール 5 mg/kg PO q12h（代替）。"
        "アムホテリシンB脂質複合体 1 mg/kg IV q48h（重症例・初期安定化）。重症例は初期にアムホテリシン＋"
        "フルコナゾールを併用。期間: 最低6-12ヶ月。鼻腔型: 長期のアゾール療法が必要な場合がある。中枢型: "
        "フルコナゾール（中枢移行が最良）＋初期にアムホテリシン。モニタリング: クリプトコッカス抗原価（目標は4倍の低下）、"
        "肝酵素。抗原価が陰性化または低値で安定するまで治療。予後: 鼻腔型 — 良好（80%以上）。中枢型 — 慎重。"
        "（Sykes 2010, O'Brien 2006）"
    ),
}

# 馬 PSSM: 英語側も汎用テンプレートだったため日英とも記述
PSSM_EN = (
    "■Management is dietary and exercise-based (lifelong; no curative drug). ■Diet: low starch/sugar "
    "(NSC <10-12% of ration — replace grain and sweet feed with forage-based concentrate) with fat as the "
    "calorie source (vegetable oil or rice bran, introduced gradually; overweight horses — weight loss with "
    "low-NSC hay first, fat only as needed). ■Exercise: daily turnout and consistent daily exercise with a "
    "gradual return over weeks after an episode; avoid stall confinement and irregular rest days. ■Acute "
    "episode: stop exercise, treat as exertional rhabdomyolysis (IV fluids if myoglobinuria — renal "
    "protection; flunixin 1.1 mg/kg IV; acepromazine 0.02-0.04 mg/kg if well hydrated). ■Diagnosis guides "
    "the plan: GYS1 genetic test (PSSM1); muscle biopsy for PSSM2/MFM. ■Check vitamin E/selenium status "
    "and correct deficiency. ■Prognosis: most horses (>70-90%) improve markedly with combined diet and "
    "exercise management; signs recur when either lapses. (Valberg 2018; Firshman 2003; Ribeiro 2004; "
    "McCue 2008)"
)
PSSM_JA = (
    "■管理の中心は食事と運動（生涯管理 — 根治薬はない）。■食事: 低デンプン・低糖（NSC が飼料の10-12%未満 — "
    "穀物・スイートフィードを粗飼料ベースの濃厚飼料に置換）とし、カロリー源は脂肪（植物油・米ぬかを徐々に導入。"
    "過体重馬はまず低NSCの乾草で減量し、脂肪は必要時のみ）。■運動: 毎日の放牧と規則的な毎日の運動。発症後は"
    "数週かけて段階的に復帰。馬房での閉じ込め・不規則な休養日は避ける。■急性発作: 運動を中止し労作性横紋筋融解症"
    "として治療（ミオグロビン尿があれば腎保護のため輸液静注、フルニキシン 1.1 mg/kg IV、十分に水和していれば"
    "アセプロマジン 0.02-0.04 mg/kg）。■診断が方針を決める: GYS1 遺伝子検査（PSSM1）、PSSM2/MFM は筋生検。"
    "■ビタミンE・セレン状態を確認し欠乏を是正。■予後: 食事と運動の併用で大半（70-90%超）が著明に改善するが、"
    "どちらかが途切れると再発する。（Valberg 2018; Firshman 2003; Ribeiro 2004; McCue 2008）"
)

_NUM = re.compile(r"\d+(?:[.,]\d+)?")


# 日本語の頻度語（「年1回」= Annual）は英語側に数字を持たないため照合から除外
_JA_COUNT_WORDS = ("年1回",)


def _numbers(text: str) -> list[str]:
    for w in _JA_COUNT_WORDS:
        text = text.replace(w, "")
    return sorted(_NUM.findall(text.replace(",", "")))


def main(apply: bool) -> int:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    by = {(x.get("species"), x.get("name")): x for x in data}
    changed = 0
    for key, ja in JA.items():
        e = by.get(key)
        if e is None:
            print("missing", key)
            continue
        if TEMPLATE_MARK not in (e.get("treatment_ja") or ""):
            continue
        en_nums, ja_nums = _numbers(e.get("treatment") or ""), _numbers(ja)
        if en_nums != ja_nums:
            raise SystemExit(f"number mismatch {key}: {en_nums} vs {ja_nums}")
        e["treatment_ja"] = ja
        changed += 1
    # 鳥ワクモ: Bird の日本語キュレート文は英語（3種共通）の忠実な訳 — インコ・オウムへ複製
    bird = by.get(("Bird", "Red Mite (Dermanyssus)"))
    for sp in ("Parakeet", "Parrot"):
        e = by.get((sp, "Red Mite (Dermanyssus)"))
        if (
            e
            and bird
            and TEMPLATE_MARK in (e.get("treatment_ja") or "")
            and (e.get("treatment") or "") == (bird.get("treatment") or "")
        ):
            e["treatment_ja"] = bird["treatment_ja"]
            changed += 1
    pssm = by.get(("Horse", "Polysaccharide Storage Myopathy (PSSM)"))
    if pssm and TEMPLATE_MARK in (pssm.get("treatment_ja") or ""):
        pssm["treatment"], pssm["treatment_ja"] = PSSM_EN, PSSM_JA
        changed += 1
    print("changed", changed)
    if apply and changed:
        JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
