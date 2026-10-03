#!/usr/bin/env python3
"""哺乳類エントリに混入した鳥・雌用生殖器治療テンプレートのキュレート置換（一回限り）。

fallback_generator の reproductive テンプレートは卵停滞・卵管脱・OHE 中心の
雌・産卵動物向け定型文で、雄性疾患（犬・猫の停留精巣）や哺乳類の雌性疾患にも
そのままスタンプされていた（鳥用量「1-3 IU/羽」含む）。英語 treatment は
疾患固有のキュレート済みプロトコルが存在するため、その内容を日本語でミラーする。
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"

CURATED_TREATMENT_JA = {
    ("dog", "Cryptorchidism"): (
        "【犬における停留精巣（陰睾）】\n"
        "外科: 停留側・下降側の両精巣摘出（去勢）を推奨 — 停留精巣は腫瘍化リスクが高い"
        "（セルトリ細胞腫・セミノーマ・間質細胞腫）。\n"
        "腹腔内停留: 開腹または腹腔鏡（補助下）で精巣を検索・摘出（膀胱背側〜鼠径輪の範囲）。\n"
        "鼠径部・皮下停留: 鼠径アプローチで摘出。\n"
        "ホルモン療法（GnRH・hCG による下降促進）: 有効性は限定的で推奨されない。\n"
        "繁殖: 遺伝形質（多因子性）のため罹患犬の繁殖は禁止。\n"
        "未去勢で経過観察する場合: 腫瘍化・精巣捻転の早期発見のため定期的な触診・超音波検査。\n"
        "予後: 両側精巣摘出により極めて良好（Cox 1986; Yates 2003）。"
    ),
    ("cat", "Cryptorchidism"): (
        "【猫における停留精巣】\n"
        "外科: 去勢時に停留精巣の検索・摘出が必須。鼠径部停留（最多）は鼠径アプローチ、"
        "腹腔内停留は開腹または腹腔鏡補助下で摘出。\n"
        "停留精巣は腫瘍化（セルトリ細胞腫・セミノーマ）・捻転リスクが上昇するため摘出で排除する。\n"
        "実施時期: 通常の去勢適齢で実施。両側停留（少数派）は特に見逃しに注意。\n"
        "繁殖: 遺伝性（多因子性と推定）のため罹患猫の繁殖は禁止。\n"
        "予後: 手術により極めて良好。去勢で腫瘍化リスクは排除される（Yates 2003; Romagnoli 2017）。"
    ),
    ("hamster", "Uterine Leiomyoma"): (
        "【ハムスターにおける子宮平滑筋腫】\n"
        "卵巣子宮全摘出（OVH）が根治的治療。通常は良性の平滑筋腫瘍。\n"
        "術後管理: メロキシカム 0.3 mg/kg PO q24h、強制給餌（シリンジフィーディング）、保温。\n"
        "摘出組織は病理組織検査で確定し、平滑筋肉腫（悪性）と鑑別する。\n"
        "予後: OVH により極めて良好（Reavill & Lennox 2012）。"
    ),
    ("ferret", "Ovarian Remnant Syndrome"): (
        "【フェレットにおける卵巣遺残症候群】\n"
        "遺残卵巣組織の完全な外科的摘出が根治的治療（避妊手術後の発情徴候の持続・再発が手がかり）。\n"
        "卵巣嚢胞: GnRH アゴニスト等のホルモン療法または外科。卵巣腫瘍: 外科摘出＋病理組織検査。\n"
        "術前管理: 輸液、鎮痛（メロキシカム 0.2 mg/kg PO/SC q24h）。\n"
        "持続発情による高エストロジェン血症（骨髄抑制・貧血）が疑われる場合は CBC で評価し、"
        "必要に応じ輸血等の支持療法を行う。"
    ),
    ("hedgehog", "Ovarian Granulosa Cell Tumor"): (
        "【ハリネズミにおける卵巣顆粒膜細胞腫】\n"
        "卵巣子宮全摘出（OVH）が第一選択。ホルモン産生性のことがあり、外陰部腫大・脱毛・"
        "貧血（エストロジェン性骨髄抑制）を伴いうる。\n"
        "術前評価: CBC（貧血・血小板減少の有無）、超音波・X線で腹腔内腫瘤と転移を評価。\n"
        "摘出組織は病理組織検査で確定。骨髄抑制の合併例は輸血等の支持療法。\n"
        "予後: 転移前の摘出で良好（Reavill & Lennox 2012 — ハリネズミの生殖器腫瘍は雌で高頻度）。"
    ),
}


def main(apply: bool) -> None:
    items = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    fixed = 0
    for entry in items:
        key = ((entry.get("species") or "").lower(), entry.get("name"))
        curated = CURATED_TREATMENT_JA.get(key)
        if curated is None:
            continue
        current = entry.get("treatment_ja") or ""
        # 既にキュレート済み（卵停滞テンプレートでない）なら触らない
        if "卵停滞" not in current and "IU/羽" not in current:
            continue
        entry["treatment_ja"] = curated
        fixed += 1
        print(f"fixed treatment_ja: {key}")
    print(f"total fixed: {fixed}")
    if apply and fixed:
        with JSON_PATH.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, separators=(",", ":"))
        print(f"written: {JSON_PATH}")


if __name__ == "__main__":
    import sys

    main(apply="--apply" in sys.argv)
