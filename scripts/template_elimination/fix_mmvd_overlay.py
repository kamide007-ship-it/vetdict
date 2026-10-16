"""2026-10 第71弾: 犬 MMVD（犬の後天性心疾患の75%超）のJSONオーバーレイ是正。

diseases_all_species.json の「Mitral Valve Disease (MMVD)」は日本語9フィールドが
同一の汎用段落（「…病態生理の理解に基づいた系統的アプローチにより…」）で、英語の
treatment/causes/prevention も循環器カテゴリ・テンプレートだった。配信DBの
オーバーレイがキュレート済みモジュール（ACVIM 2019 / EPIC / QUEST 準拠）を
上書きしていたため、最頻の犬心疾患の治療欄がテンプレートになっていた。

- 治療・病因・予防・予後・病態生理（日英）: モジュールのキュレート文を採用
- 臨床徴候・診断・伝播（日本語）: 英語版に対応する疾患固有文を収載
- 英語の臨床徴候に混入していた猫ATEの一文（異種混入）を除去

用法: python3 -m scripts.template_elimination.fix_mmvd_overlay [--apply]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAME = "Mitral Valve Disease (MMVD)"
TEMPLATE = "病態生理の理解に基づいた系統的アプローチにより"
CAT_ATE = " In cats, feline aortic thromboembolism may present acutely with hindlimb paresis, cold limbs, pain and absent pulses."

CLINICAL_SIGNS_JA = (
    "病期（ACVIM Stage）に沿って進行する。Stage B1/B2（無症状期）: 左心尖部の収縮期逆流性雑音のみで、"
    "飼い主は異常に気づかないことが多い（雑音Grade 3/6以上は心拡大リスク上昇）。"
    "Stage C（うっ血性心不全）: 安静時・睡眠時呼吸数の増加（≥40回/分 — 最も早期の家庭での警告徴候）、"
    "運動不耐性、夜間〜明け方の咳（左房拡大による左主気管支圧排 — 気管虚脱との鑑別が重要）、"
    "呼吸困難・起座呼吸、食欲低下・体重減少（心臓悪液質）。"
    "重症・合併症: 失神（不整脈・肺高血圧）、チアノーゼ、腹水（肺高血圧に伴う右心不全）、"
    "腱索断裂による急性肺水腫（突然の重度呼吸困難・ピンク色泡沫状喀痰）。"
)
DIAGNOSIS_JA = (
    "(1) 聴診: 左心尖部の収縮期逆流性雑音（Grade I-VI/VI）、頻脈・不整の有無。"
    "(2) 胸部X線: VHS >10.5・VLAS ≥2.3 で心拡大、肺静脈うっ血・肺門部〜尾背側の間質/肺胞パターン（肺水腫）。"
    "(3) 心エコー（確定・病期分類の中心）: LA/Ao ≥1.6 かつ LVIDDN ≥1.7 で Stage B2、弁尖肥厚・逸脱・腱索断裂、"
    "逆流ジェット、三尖弁逆流速度による肺高血圧評価。"
    "(4) NT-proBNP: >1500 pmol/L は心原性呼吸困難を示唆（呼吸器疾患との鑑別補助）。"
    "(5) 心電図（心房細動・期外収縮）、血圧測定、CBC・生化学・電解質（利尿薬開始前の腎機能ベースライン）。"
    "(6) 家庭での安静時呼吸数記録（Stage B2以降は毎日）。（ACVIM 2019 — Keene et al. JVIM 2019）"
)
TRANSMISSION_JA = (
    "感染性ではなく、動物間で伝播しない。粘液腫様弁変性には強い遺伝的素因があり（CKCSでは常染色体優性遺伝が"
    "疑われる多因子遺伝）、罹患個体の繁殖制限（CKCSでは2.5歳未満で雑音のある個体を繁殖に用いない）が"
    "集団レベルの予防策となる。"
)

FIELDS_FROM_MODULE = (
    "treatment",
    "treatment_ja",
    "causes",
    "causes_ja",
    "prevention",
    "prevention_ja",
    "prognosis",
    "prognosis_ja",
    "pathophysiology",
    "pathophysiology_ja",
)


def _module_entry() -> dict:
    from api.species.dog_diseases import DISEASES

    return next(d for d in DISEASES if d["name"] == NAME)


def fix_json(data: list) -> int:
    mod = _module_entry()
    n = 0
    for d in data:
        if d.get("species") not in ("Dog", "dog") or d.get("name") != NAME:
            continue
        for f in FIELDS_FROM_MODULE:
            if mod.get(f) and d.get(f) != mod[f]:
                d[f] = mod[f]
                n += 1
        for f, v in (
            ("clinical_signs_ja", CLINICAL_SIGNS_JA),
            ("diagnosis_ja", DIAGNOSIS_JA),
            ("transmission_ja", TRANSMISSION_JA),
        ):
            if d.get(f) != v:
                d[f] = v
                n += 1
        if CAT_ATE in (d.get("clinical_signs") or ""):
            d["clinical_signs"] = d["clinical_signs"].replace(CAT_ATE, "")
            n += 1
    return n


def fix_module(src: str) -> str:
    """Replace the template JA paragraph inside the MMVD module entry only."""
    start = src.index(f'"name": "{NAME}"')
    end = src.index('"urgency"', start)
    block = src[start:end]
    import re

    para = re.search(r'"[^"]*' + TEMPLATE + r'[^"]*"', block)
    if not para:
        return src
    tmpl = para.group(0)
    for key, val in (
        ("clinical_signs_ja", CLINICAL_SIGNS_JA),
        ("diagnosis_ja", DIAGNOSIS_JA),
        ("transmission_ja", TRANSMISSION_JA),
    ):
        block = block.replace(f'"{key}": {tmpl}', f'"{key}": {json.dumps(val, ensure_ascii=False)}')
    block = block.replace(CAT_ATE, "")
    return src[:start] + block + src[end:]


def main(apply: bool) -> None:
    p = ROOT / "diseases_all_species.json"
    raw = p.read_text(encoding="utf-8")
    data = json.loads(raw)
    n = fix_json(data)
    mp = ROOT / "api" / "species" / "dog_diseases.py"
    msrc = mp.read_text(encoding="utf-8")
    new_m = fix_module(msrc)
    print(("applied" if apply else "dry-run"), "json fields:", n, "module changed:", new_m != msrc)
    if apply:
        p.write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ("\n" if raw.endswith("\n") else ""),
            encoding="utf-8",
        )
        mp.write_text(new_m, encoding="utf-8")


if __name__ == "__main__":
    main("--apply" in sys.argv)
