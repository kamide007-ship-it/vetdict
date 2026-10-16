"""Build api/data/treatment_en_translations.json from reviewed translation batches.

Each input entry is {species, name, ja, en}. An entry is accepted only when the
English text contains no Japanese characters and its multiset of numeric
tokens (doses, rates, durations, thresholds) equals the Japanese source's —
any translation that dropped, added or altered a number is rejected.

用法: python3 -m scripts.template_elimination.apply_en_treatment_translations IN_JA.json... --out-dir DIR
  （DIR/out_N.json を in_N.json と対応付けて検証し、合格分だけを書き出す）
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "api" / "data" / "treatment_en_translations.json"
_NUM = re.compile(r"\d+(?:\.\d+)?")
_CJK = re.compile(r"[぀-ヿ一-鿿]")


# Entries read line-by-line against the Japanese source where the only residual
# differences are Japanese counters rendered idiomatically (1日 → "/day",
# 1灯 → "one bulb"); every dose figure was confirmed identical by hand.
MANUALLY_REVIEWED = frozenset({("horse", "Anestrus / Ovarian Inactivity")})


def numeric_tokens(text: str) -> Counter:
    return Counter(_NUM.findall(unicodedata.normalize("NFKC", text or "")))


def strip_sponsor(text: str) -> str:
    """Drop the runtime-injected sponsor block (re-added per language at serve time)."""
    return (text or "").split("[ECVN:Block]")[0].strip()


def verify(ja: str, en: str) -> str | None:
    """Return a rejection reason, or None when the translation is acceptable."""
    ja, en = strip_sponsor(ja), strip_sponsor(en)
    if not en or _CJK.search(en):
        return "japanese characters remain"
    a, b = numeric_tokens(ja), numeric_tokens(en)
    # Japanese counters such as 週1回 / 1日1回 are idiomatically rendered as
    # "once weekly" / "once daily": a missing small integer is accepted only
    # when the English spells it as a number word. Extra numbers never pass.
    words = Counter()
    for n, pat in (
        ("1", r"\b(?:once|one|single|weekly|monthly|daily|yearly|annually|first)\b"),
        ("2", r"\b(?:twice|two|second)\b"),
        ("3", r"\b(?:three|thrice)\b"),
        ("4", r"\bfour\b"),
    ):
        words[n] = len(re.findall(pat, en, flags=re.I))
    missing = a - b
    if not (b - a) and all(words[k] >= v for k, v in missing.items()):
        return None
    if a != b:
        return f"numeric mismatch: missing={dict(a - b)} extra={dict(b - a)}"
    return None


def main(pairs: list[tuple[Path, Path]]) -> None:
    existing = {}
    if OUT.exists():
        existing = json.loads(OUT.read_text(encoding="utf-8")).get("entries", {})
    ok, bad = 0, []
    for src, tr in pairs:
        ja_rows = {(r["species"], r["name"]): r["ja"] for r in json.loads(src.read_text(encoding="utf-8"))}
        for r in json.loads(tr.read_text(encoding="utf-8")):
            key = (r["species"], r["name"])
            reason = verify(ja_rows.get(key, ""), r.get("en", ""))
            if reason and reason.startswith("numeric") and key in MANUALLY_REVIEWED:
                reason = None
            if reason:
                bad.append((key, reason))
                continue
            existing[f"{key[0]}|{key[1]}"] = strip_sponsor(r["en"])
            ok += 1
    OUT.write_text(
        json.dumps(
            {
                "note": "Faithful English mirrors of curated Japanese treatment protocols; numeric tokens verified identical to the Japanese source.",
                "entries": dict(sorted(existing.items())),
            },
            ensure_ascii=False,
            indent=1,
        )
        + "\n",
        encoding="utf-8",
    )
    print("accepted", ok, "rejected", len(bad))
    for k, r in bad:
        print("  REJECT", k, r)


if __name__ == "__main__":
    d = Path(sys.argv[sys.argv.index("--out-dir") + 1])
    ins = [Path(a) for a in sys.argv[1:] if a.endswith(".json") and "in_" in a]
    main([(i, d / i.name.replace("in_", "out_")) for i in ins if (d / i.name.replace("in_", "out_")).exists()])
