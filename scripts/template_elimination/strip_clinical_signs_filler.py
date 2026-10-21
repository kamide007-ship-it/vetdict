"""Strip the boilerplate tail from English clinical_signs (2026-10 第75弾).

An early enrichment pass appended a fixed string of non-informative clauses to
~2,200 English clinical_signs texts, e.g.

    "... include: Dehydration, Vomiting, Lethargy.; typical viral etiology
     presentation; variable severity depending on disease stage; behavioral
     changes often observed; symptom timeline varies by individual; response to
     treatment helps confirm diagnosis"

The first clause class is clinically wrong for most records ("typical viral
etiology presentation" on Addison's disease, pyometra, IMHA; "bacterial" /
"parasitic" / "progressive mass growth" variants likewise stamped by category),
and the remaining clauses carry no disease-specific information. The tail is
removed only when *every* clause after the signs list belongs to the known
filler vocabulary, so curated clauses are never touched.

Usage: python3 -m scripts.template_elimination.strip_clinical_signs_filler [--apply]
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"

_FILLER_CLAUSE = re.compile(
    r"^(?:typical [a-z ]+ presentation"
    r"|variable severity depending on disease stage"
    r"|potentially severe systemic effects"
    r"|behavioral changes often observed"
    r"|symptom timeline varies by individual"
    r"|gradual symptom development over weeks to months"
    r"|rapid symptom onset and progression"
    r"|mild to moderate severity typical"
    r"|production losses common in livestock"
    r"|response to treatment helps confirm diagnosis)$"
)


def strip_filler(text: str) -> str:
    """Return text with trailing boilerplate clauses removed (unchanged otherwise).

    Clauses are ";"-separated; filler clauses are popped from the end while they
    match the known vocabulary. At least one (non-filler) clause is kept.
    """
    if not text or ";" not in text:
        return text
    parts = text.split(";")
    while len(parts) > 1 and _FILLER_CLAUSE.match(parts[-1].strip()):
        parts.pop()
    if len(parts) == len(text.split(";")):
        return text
    head = ";".join(parts).rstrip()
    if not head.endswith("."):
        head += "."
    return head


def main(apply: bool) -> int:
    raw = JSON_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    recs = data if isinstance(data, list) else data["diseases"]
    changed = 0
    for r in recs:
        old = r.get("clinical_signs")
        if isinstance(old, str):
            new = strip_filler(old)
            if new != old:
                r["clinical_signs"] = new
                changed += 1
    print(f"clinical_signs filler tails stripped: {changed}")
    if apply and changed:
        compact = "\n" not in raw.strip()
        JSON_PATH.write_text(
            json.dumps(
                data, ensure_ascii=False, separators=(",", ":") if compact else None, indent=None if compact else 2
            ),
            encoding="utf-8",
        )
    return 0


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
