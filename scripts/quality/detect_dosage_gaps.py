#!/usr/bin/env python3
"""Find drug/species entries whose dosing is missing a dose, route or frequency.

READ-ONLY. Never mutates drug data — it writes a report so a vet can fill the
gaps from a formulary.

Why this is not a plain "is the field empty" check
--------------------------------------------------
A naive scan calls 22% of entries "missing a route" and 46% "missing a
frequency", which is wrong and would send someone chasing hundreds of
non-problems. Several drug classes are *correctly* written without an mg/kg +
qNh pattern:

* inhalant anaesthetics are dosed as a MAC percentage, not mg/kg;
* topicals, eye and ear preparations are applied, not dosed per kilo;
* local anaesthetics are single infiltrations;
* induction, premedication and emergency drugs (ketamine, midazolam, atropine,
  adrenaline …) are single doses given to effect, so no repeat interval exists;
* the sponsor's own supplements legitimately say "refer to the product label";
* antiparasitics express their schedule as "repeat in 14 days" rather than qNh.

The detector therefore classifies before it counts, and reports the excluded
buckets so the exclusions stay auditable rather than hidden. Entries that
honestly say "not well established" are counted separately: those are truthful
blanks, not defects, and filling them needs real evidence.

Usage:
    python3 scripts/quality/detect_dosage_gaps.py            # summary
    python3 scripts/quality/detect_dosage_gaps.py --json OUT  # full worklist
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

ROUTE = re.compile(
    r"\b(PO|IV|IM|SC|SQ|IO|IP|PR|IN|TD|transderm|topical|inhal|nebuli|ophthalmic|otic|oral|bath|dip"
    r"|immersion|in\s*water|in\s*feed|per\s*os|epidural|intraarticular|intralesional|intranasal"
    # A dispensed "drop" is an ophthalmic/otic route; an ointment/patch/strip that
    # is "applied" is topical; a rate-per-minute/hour (CRI) is by definition an
    # intravenous infusion. Without these, ~75 eye-drop/topical/CRI entries that
    # ARE complete were mis-flagged as "missing route".
    r"|drops?|ointment|applied|apply|patch|strip|pinna|CRI|to\s*effect)\b"
    r"|[/⁄]\s*kg\s*[/⁄]\s*(min|hr|hrs|hour|hours)"
    r"|経口|静脈|筋肉|筋注|皮下|局所|外用|点眼|点耳|吸入|噴霧|薬浴|浸漬|経鼻|直腸|腹腔|飼料|飲水|塗布|経皮|硬膜外|軟膏|貼付|パッチ|滴",
    re.I,
)
FREQUENCY = re.compile(
    r"\bq\s*\d+(\s*-\s*\d+)?\s*(h|hr|hrs|hours?|d|days?|wk|weeks?|min)\b"
    r"|\b(SID|BID|TID|QID|EOD|PRN|once|single|daily|weekly|monthly|continuous|CRI|to effect"
    r"|as needed|induction|bolus)\b"
    r"|for\s+\d+(\s*-\s*\d+)?\s*(days?|weeks?|hours?)|repeat\s+(in|after|every)|then\s+repeat|may\s+repeat"
    r"|毎|時間毎|日\d回|回/日|週\d|単回|1日\d回|隔日|連日|持続|効果発現まで|導入|日間|時間ごと|再投与|後に反復|反復投与",
    re.I,
)
# "no dose" is the correct content here, not a gap.
NOT_APPLICABLE = re.compile(r"使用不可|禁忌|contraindicated|do not use|^\s*(N/?A|-|なし)\s*$", re.I)
# An honest "we don't know / we don't use this here" — a truthful blank that
# reflects a clinical judgement, not a missing-data bug. "Not commonly used",
# "rarely used" and "not established" are the same honest signal as "not well
# established" and belong in this bucket, not on a vet's worklist.
UNESTABLISHED = re.compile(
    r"not (well )?established|not commonly (needed|used|supplemented|indicated)"
    r"|(rarely|seldom) used|十分に確立されていない|not commonly needed|一般的には使用されない"
    r"|通常は(不要|補充不要)|ほとんど使用しない|unknown|不明|データなし|no data",
    re.I,
)
LABEL_DIRECTED = re.compile(r"refer to product label|製品ラベル|product label", re.I)
# Dosing that is complete by pointing at another species' entry ("same protocol
# as cats"). The route and frequency live in the referenced entry, so this is
# not a defect to fill.
CROSS_REFERENCED = re.compile(
    r"same (protocol )?as (cats?|dogs?|above|for)|as (per|for) (cats?|dogs?)|に準じ|と同(じ|様)のプロトコル", re.I
)
# Classes whose dosing is not written as mg/kg + qNh.
NON_WEIGHT_CLASS = re.compile(
    r"isoflurane|sevoflurane|desflurane|nitrous|halothane|chlorhexidine|ophthalmic|otic|shampoo|cream"
    r"|ointment|topical|spray|povidone|silver sulfadiazine|artificial tear|lubricant|bupivacaine|lidocaine"
    r"|mepivacaine|ropivacaine|proparacaine|EMLA|prilocaine",
    re.I,
)
# Single-dose agents: a repeat interval is not expected once a route is given.
SINGLE_DOSE_CLASS = re.compile(
    r"ketamine|diazepam|midazolam|alfaxalone|propofol|etomidate|thiopental|atropine|glycopyrrolate|mannitol"
    r"|epinephrine|adrenaline|naloxone|flumazenil|atipamezole|yohimbine|neostigmine|succinylcholine|rocuronium"
    r"|vecuronium|tiletamine|medetomidine|dexmedetomidine|xylazine|acepromazine|butorphanol|buprenorphine"
    r"|morphine|fentanyl|hydromorphone|methadone|oxytocin|vitamin k1|calcium gluconate|dextrose|doxapram",
    re.I,
)


def scan() -> dict[str, Any]:
    from api.drug_dictionary import DRUGS

    gaps: list[dict[str, Any]] = []
    excluded: Counter[str] = Counter()
    unestablished: list[dict[str, str]] = []

    for drug in DRUGS:
        name = str(drug.get("name") or "")
        for species, info in (drug.get("species_info") or {}).items():
            if not isinstance(info, dict) or info.get("safe") is False:
                continue
            text = " ".join(str(info.get(k, "") or "") for k in ("dosage", "dosage_ja")).strip()
            if not text or NOT_APPLICABLE.search(text):
                continue
            has_route = bool(ROUTE.search(text))
            has_freq = bool(FREQUENCY.search(text))
            # Completeness wins over every other label: an entry that carries both
            # a route and a frequency is usable even when it is prefaced with a
            # caveat like "Not established; empirical 10-30 mg/kg PO q24-48h". Test
            # this first so those honest-but-usable doses are not mislabelled.
            if has_route and has_freq:
                continue
            if UNESTABLISHED.search(text):
                unestablished.append({"drug": name, "species": species, "text": text[:120]})
                continue
            if CROSS_REFERENCED.search(text):
                excluded["cross-referenced to another species"] += 1
                continue
            if LABEL_DIRECTED.search(text):
                excluded["supplement (label-directed)"] += 1
                continue
            if NON_WEIGHT_CLASS.search(name):
                excluded["inhalant / topical / local anaesthetic"] += 1
                continue
            if SINGLE_DOSE_CLASS.search(name) and has_route:
                excluded["single-dose agent (route given)"] += 1
                continue
            gaps.append(
                {
                    "drug_id": drug.get("id"),
                    "drug": name,
                    "species": species,
                    "dosage": text[:160],
                    "missing_route": not has_route,
                    "missing_frequency": not has_freq,
                }
            )

    return {
        "total_gaps": len(gaps),
        "missing_route": sum(1 for g in gaps if g["missing_route"]),
        "missing_frequency": sum(1 for g in gaps if g["missing_frequency"]),
        "excluded_by_class": dict(excluded),
        "unestablished_count": len(unestablished),
        "unestablished": unestablished,
        "gaps": gaps,
        "by_drug": Counter(g["drug"] for g in gaps).most_common(),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Detect missing dose/route/frequency in the drug dictionary")
    ap.add_argument("--json", help="write the full worklist to this path")
    args = ap.parse_args()

    report = scan()
    print(f"genuine gaps           : {report['total_gaps']}")
    print(f"  missing route        : {report['missing_route']}")
    print(f"  missing frequency    : {report['missing_frequency']}")
    print(f"explicitly unestablished: {report['unestablished_count']} (honest blanks, need evidence)")
    print("excluded as correct-by-class:")
    for bucket, count in report["excluded_by_class"].items():
        print(f"  {bucket:38} {count}")
    print("\ntop drugs by gap count:")
    for drug, count in report["by_drug"][:15]:
        print(f"  {drug[:46]:48} {count}")

    if args.json:
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nworklist -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
