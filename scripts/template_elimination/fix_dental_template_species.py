"""2026-11 第83弾: 常生歯用の歯科テンプレートを非常生歯の種から撲滅する。

歯科カテゴリのフォールバックは全種に「高速ダイヤモンドバーで臼歯研磨、過長切歯トリミング」
「メロキシカム 0.5-1 mg/kg PO q12-24h」「チモシー主食」を出力しており、犬猫（メロキシカムは
5-10倍量）・馬・フェレット・ハリネズミ・トカゲ・鳥/リクガメの嘴疾患に誤適用されていた。

- 犬猫の3疾患は英語キュレート治療の忠実な日本語版に全置換
- その他は旧テンプレートの4行を種別の行（fallback_generator.dental_body_lines_ja）に置換

使い方: python3 -m scripts.template_elimination.fix_dental_template_species [--apply]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from scripts.template_elimination.fallback_generator import (
    ELODONT_SPECIES,
    LEGACY_DENTAL_TEMPLATE_LINES,
    dental_body_lines_ja,
)

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"
MODULE_DIR = ROOT / "api" / "species"

_SPECIES_FILE = {
    "bird": "bird_diseases.py",
    "parakeet": "parakeet_diseases.py",
    "parrot": "parrot_diseases.py",
    "tortoise": "tortoise_diseases.py",
    "lizard": "lizard_diseases.py",
    "ferret": "ferret_diseases.py",
    "hedgehog": "hedgehog_diseases.py",
}

# 犬猫: 英語キュレート治療の日本語版（新規の臨床内容なし）
CURATED_JA = {
    ("cat", "Oral Mass / Epulis"): (
        "【猫における口腔腫瘤・エプリス】\n"
        "まず生検で良性・悪性を鑑別する（必須）。\n"
        "線維腫性エプリス（周辺性歯原性線維腫）: 保存的切除で再発は少ない。\n"
        "棘細胞性エナメル上皮腫: 局所浸潤性のため顎骨部分切除（下顎骨/上顎骨切除）でマージンを確保。\n"
        "扁平上皮癌・線維肉腫: 広範切除±放射線療法（扁平上皮癌は猫で最多の口腔悪性腫瘍で予後不良）。\n"
        "術後はX線で再発をモニタリング。予後: 良性は良好、扁平上皮癌は不良。\n"
        "鎮痛: ブプレノルフィン 0.02-0.03 mg/kg OTM q8h、局所麻酔ブロックを併用。\n"
        "（Withrow & Vail 6th ed 2019; Verstraete 2012）"
    ),
    ("cat", "Feline Oral Eosinophilic Granuloma"): (
        "【猫における猫口腔好酸球性肉芽腫】\n"
        "グルココルチコイドが第一選択: 酢酸メチルプレドニゾロン（デポメドロール）4 mg/kg SC/IM 2週毎×3回、"
        "または プレドニゾロン 1-2 mg/kg PO q12h × 2-3週→漸減、トリアムシノロン 0.25-0.5 mg/kg PO q12-24h。\n"
        "難治例・ステロイド節約: シクロスポリン 5-7 mg/kg PO q24h。\n"
        "二次感染時（または試験的に）: アモキシシリン・クラブラン酸 12.5-25 mg/kg PO q12h × 14-21日（抗菌薬に反応する例がある）。\n"
        "誘因の特定と除去: 除去食試験（加水分解/新奇蛋白食 8-12週）、厳格なノミ対策（イソキサゾリン系）、FHV-1・FIV/FeLVの除外。\n"
        "生検で扁平上皮癌を除外する。難治病変はCO2レーザー切除。好発部位: 上唇（いわゆるrodent ulcer）、舌、硬口蓋。\n"
        "予後: 治療により良好だが、基礎原因が特定できないと再発が多い。（Bloom 2006; Buckley 2012）"
    ),
    ("dog", "Oral Papillomatosis"): (
        "【犬における口腔乳頭腫症】\n"
        "通常1-3ヶ月で自然退縮するため、嚥下障害・流涎・出血がある場合のみ治療する。\n"
        "アジスロマイシン 10 mg/kg PO q24h × 10日（退縮を早める可能性）。\n"
        "閉塞を起こす病変は外科的切除・減量、個々の病変には凍結療法またはCO2レーザー焼灼。\n"
        "難治例は自家ワクチン、重度・持続例はインターフェロンα。\n"
        "2歳未満の若齢犬に多い。免疫不全犬では扁平上皮癌への悪性転化のリスクが高い。\n"
        "他の犬に伝染するが、ヒトや猫には伝染しない。"
    ),
}


def _norm(sp: str) -> str:
    return sp.strip().lower().replace(" ", "_")


def _rewrite(text: str, species: str) -> str:
    if not text or LEGACY_DENTAL_TEMPLATE_LINES[0] not in text:
        return text
    lines = text.split("\n")
    out: list[str] = []
    inserted = False
    for ln in lines:
        if any(ln.startswith(t) or ln == t for t in LEGACY_DENTAL_TEMPLATE_LINES):
            if not inserted:
                out.extend(dental_body_lines_ja(species))
                inserted = True
            continue
        out.append(ln)
    return "\n".join(out)


def fix_json(apply: bool) -> int:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    n = 0
    for e in data:
        sp = _norm(e.get("species", ""))
        if sp in ELODONT_SPECIES:
            continue
        cur = e.get("treatment_ja") or ""
        key = (sp, e.get("name"))
        new = CURATED_JA.get(key) if LEGACY_DENTAL_TEMPLATE_LINES[0] in cur else None
        if new is None:
            new = _rewrite(cur, sp)
        if new != cur:
            e["treatment_ja"] = new
            n += 1
    if apply and n:
        JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return n


def fix_modules(apply: bool) -> int:
    n = 0
    for sp, fname in _SPECIES_FILE.items():
        path = MODULE_DIR / fname
        if not path.exists():
            continue
        src = path.read_text(encoding="utf-8")

        def repl(m: re.Match, sp: str = sp) -> str:
            raw = json.loads('"' + m.group(1) + '"')
            new = _rewrite(raw, sp)
            if new == raw:
                return m.group(0)
            return '"treatment_ja": ' + json.dumps(new, ensure_ascii=False)

        out, cnt = re.subn(r'"treatment_ja": "((?:[^"\\]|\\.)*)"', repl, src)
        changed = sum(1 for _ in re.finditer(re.escape(LEGACY_DENTAL_TEMPLATE_LINES[0]), src)) - sum(
            1 for _ in re.finditer(re.escape(LEGACY_DENTAL_TEMPLATE_LINES[0]), out)
        )
        if changed:
            n += changed
            if apply:
                path.write_text(out, encoding="utf-8")
    return n


if __name__ == "__main__":
    apply = "--apply" in sys.argv
    print("json:", fix_json(apply), "modules:", fix_modules(apply), "(applied)" if apply else "(dry-run)")
