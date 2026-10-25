"""2026-10 第78弾: 哺乳類に誤適用されていた栄養テンプレート治療文の是正。

犬/猫/ウサギのビタミンD中毒（高Ca血症の救急）が「4-8週の食事処方の見直し」、
馬の過剰歯（歯科）が栄養プロトコル、犬猫馬に小型エキゾチックの参考書が引用される
等の誤りを、``mammal_nutrition_treatment_library`` のキュレート文で置換する。
猫NSHPの英語オーバーレイ（甲状腺機能亢進症の治療文 — 副甲状腺/甲状腺の取り違え）と
小型哺乳類ビタミンA欠乏の英語文（鳥・爬虫類の記述）も同時に是正する。

用法: python3 -m scripts.template_elimination.fix_mammal_nutrition_treatments [--apply]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from scripts.template_elimination.mammal_nutrition_treatment_library import ENTRIES

ROOT = Path(__file__).resolve().parents[2]
_MODULE = {"horse": "equine_diseases"}


def _norm(sp: str) -> str:
    return (sp or "").lower().replace(" ", "_")


def fix_json(data: list) -> int:
    n = 0
    for d in data:
        e = ENTRIES.get((_norm(d.get("species")), d.get("name") or ""))
        if not e:
            continue
        for f, k in (("treatment_ja", "ja"), ("treatment", "en")):
            if k in e and d.get(f) != e[k]:
                d[f] = e[k]
                n += 1
    return n


def fix_module(src: str, name: str, entry: dict) -> tuple[str, int]:
    key = f'"name": "{name}",'
    if key not in src:
        return src, 0
    n = 0
    start = src.index(key)
    nxt = src.find('"name": "', start + len(key))
    end = nxt if nxt != -1 else len(src)
    block = src[start:end]
    for f, k in (("treatment_ja", "ja"), ("treatment", "en")):
        if k not in entry:
            continue
        m = re.search(r'^(\s*)"' + f + r'": "(?:[^"\\]|\\.)*",\s*$', block, re.M)
        if not m:
            continue
        new = f'{m.group(1)}"{f}": {json.dumps(entry[k], ensure_ascii=False)},'
        if block[m.start() : m.end()] != new:
            block = block[: m.start()] + new + block[m.end() :]
            n += 1
    return src[:start] + block + src[end:], n


def main(apply: bool) -> None:
    p = ROOT / "diseases_all_species.json"
    raw = p.read_text(encoding="utf-8")
    data = json.loads(raw)
    nj = fix_json(data)
    nm = 0
    changed = {}
    for (sp, name), e in ENTRIES.items():
        mp = ROOT / "api" / "species" / f"{_MODULE.get(sp, sp + '_diseases')}.py"
        if not mp.exists():
            continue
        src = changed.get(mp) or mp.read_text(encoding="utf-8")
        new, k = fix_module(src, name, e)
        nm += k
        changed[mp] = new
    print(("applied" if apply else "dry-run"), "json fields:", nj, "module fields:", nm)
    if apply:
        p.write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ("\n" if raw.endswith("\n") else ""),
            encoding="utf-8",
        )
        for mp, s in changed.items():
            mp.write_text(s, encoding="utf-8")


if __name__ == "__main__":
    main("--apply" in sys.argv)
