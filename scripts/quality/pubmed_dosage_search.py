#!/usr/bin/env python3
"""Search PubMed for species-specific dosing evidence behind each dosage gap.

READ-ONLY with respect to drug data: this never writes a dose. It asks, for every
(drug, species) gap found by ``detect_dosage_gaps.py``, whether the published
literature even contains species-specific pharmacokinetic or dosing evidence, and
records the PMIDs so a vet can judge the source rather than trust a number that
appeared from nowhere.

The distinction matters because most of these gaps are in exotic species, where
dosing is carried by formularies (Plumb's, Carpenter) rather than by indexed
papers. Knowing *which* gaps PubMed can and cannot close is what decides whether
a gap is researchable at all or has to come off a formulary shelf.

Rate limited to NCBI's 3 requests/second guidance for unauthenticated use.

Usage:
    python3 scripts/quality/pubmed_dosage_search.py \
        --gaps reports/quality/_dosage_gaps.json \
        --out  reports/quality/_dosage_pubmed.json
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
ESUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

# PubMed indexes species by common and scientific name; a bare app species code
# ("guinea_pig", "degu") retrieves nothing useful on its own.
SPECIES_TERMS: dict[str, str] = {
    "dog": '"dogs"[MeSH] OR dog OR canine',
    "cat": '"cats"[MeSH] OR cat OR feline',
    "horse": '"horses"[MeSH] OR horse OR equine OR foal',
    "rabbit": '"rabbits"[MeSH] OR rabbit',
    "ferret": '"ferrets"[MeSH] OR ferret',
    "hamster": 'hamster OR "cricetinae"[MeSH]',
    "guinea_pig": '"guinea pigs"[MeSH] OR "guinea pig" OR cavia',
    "chinchilla": '"chinchilla"[MeSH] OR chinchilla',
    "degu": '"Octodon"[MeSH] OR "octodon degus" OR degu',
    "hedgehog": '"hedgehogs"[MeSH] OR hedgehog OR atelerix',
    "sugar_glider": '"sugar glider" OR petaurus',
    "bird": '"birds"[MeSH] OR avian OR bird',
    "parakeet": '"melopsittacus"[MeSH] OR budgerigar OR parakeet',
    "parrot": '"parrots"[MeSH] OR parrot OR psittacine',
    "reptile": '"reptiles"[MeSH] OR reptile',
    "snake": '"snakes"[MeSH] OR snake OR python OR boa',
    "lizard": '"lizards"[MeSH] OR lizard OR gecko OR iguana',
    "tortoise": '"turtles"[MeSH] OR tortoise OR chelonian',
    "amphibian": '"amphibians"[MeSH] OR amphibian OR frog OR salamander',
    "fish": '"fishes"[MeSH] OR fish OR teleost',
    "exotic_other": "exotic animal OR zoo animal",
}

DOSING = "pharmacokinetics OR pharmacokinetic OR dose OR dosage OR dosing OR administration OR plasma concentration"


def _drug_query_name(name: str) -> str:
    """Strip trade/formulation parentheticals: 'Ivermectin (Oral/Injectable)' → 'Ivermectin'."""
    base = name.split("(")[0].strip()
    return base or name.strip()


def _get(url: str, params: dict[str, str], retries: int = 3) -> dict[str, Any] | None:
    query = urllib.parse.urlencode(params)
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(f"{url}?{query}", timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            if attempt == retries - 1:
                return None
            time.sleep(1.5 * (attempt + 1))
    return None


def search_gap(drug: str, species: str, delay: float) -> dict[str, Any]:
    species_terms = SPECIES_TERMS.get(species, species.replace("_", " "))
    term = f"({_drug_query_name(drug)}) AND ({species_terms}) AND ({DOSING})"
    data = _get(ESEARCH, {"db": "pubmed", "term": term, "retmax": "5", "retmode": "json", "sort": "relevance"})
    time.sleep(delay)
    if not data:
        return {"drug": drug, "species": species, "error": "request failed", "hits": None, "pmids": []}
    result = data.get("esearchresult") or {}
    pmids = result.get("idlist") or []
    try:
        hits = int(result.get("count", 0))
    except (TypeError, ValueError):
        hits = 0
    return {"drug": drug, "species": species, "query": term, "hits": hits, "pmids": pmids}


# A raw hit count badly overstates what is usable. PubMed's exotic-species
# literature is dominated by two kinds of paper that must never become a dose:
# human medicine that merely shares the drug name (dexamethasone in COVID-19
# patients came back under "dexamethasone + avian"), and laboratory work using
# the species as a *model* for human disease (dexamethasone in hamsters for
# pulmonary pathology). Treating those as evidence is the same failure that put
# "Alzheimer-like disease" in the degu database. So results are tiered by whether
# the source looks veterinary AND the title talks about dosing at all.
VET_JOURNAL = re.compile(
    r"\bvet\b|veterinar|j zoo|zoo wildl|avian dis|avian med|j avian|exot|equine|poult|aquacult|dis aquat"
    r"|j fish dis|lab anim|comp med|am j vet|j am vet|can vet|aust vet|res vet sci|vet rec|j small anim"
    r"|j feline|j exot",
    re.I,
)
DOSE_LANGUAGE = re.compile(
    r"pharmacokinet|plasma concentration|serum concentration|dose|dosage|dosing|bioavailab|efficacy"
    r"|residue|withdrawal",
    re.I,
)


def classify(result: dict[str, Any]) -> str:
    """Tier one gap's search result by how likely it is to yield a usable dose."""
    if not (result.get("hits") or 0):
        return "not_indexed"
    titles = " ".join((result.get("titles") or {}).values())
    if not titles.strip():
        return "non_veterinary_noise"
    if not VET_JOURNAL.search(titles):
        return "non_veterinary_noise"
    return "veterinary_dosing_candidate" if DOSE_LANGUAGE.search(titles) else "veterinary_non_dosing"


def fetch_titles(pmids: list[str], delay: float) -> dict[str, str]:
    if not pmids:
        return {}
    data = _get(ESUMMARY, {"db": "pubmed", "id": ",".join(pmids), "retmode": "json"})
    time.sleep(delay)
    if not data:
        return {}
    out: dict[str, str] = {}
    for pmid, rec in (data.get("result") or {}).items():
        if pmid == "uids" or not isinstance(rec, dict):
            continue
        out[pmid] = f"{rec.get('title', '')} — {rec.get('source', '')} {rec.get('pubdate', '')}".strip()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="PubMed evidence search for dosage gaps")
    ap.add_argument("--gaps", default="reports/quality/_dosage_gaps.json")
    ap.add_argument("--out", default="reports/quality/_dosage_pubmed.json")
    ap.add_argument("--delay", type=float, default=0.36, help="seconds between requests (NCBI: 3/sec)")
    ap.add_argument("--limit", type=int, default=0, help="only process the first N gaps (0 = all)")
    args = ap.parse_args()

    gaps = json.loads(Path(args.gaps).read_text(encoding="utf-8"))["gaps"]
    if args.limit:
        gaps = gaps[: args.limit]

    results: list[dict[str, Any]] = []
    for i, gap in enumerate(gaps, 1):
        res = search_gap(gap["drug"], gap["species"], args.delay)
        res["missing_route"] = gap["missing_route"]
        res["missing_frequency"] = gap["missing_frequency"]
        res["current_dosage"] = gap["dosage"]
        results.append(res)
        if i % 25 == 0 or i == len(gaps):
            print(f"  {i}/{len(gaps)} searched", flush=True)

    # Titles only for gaps that actually returned something, to keep call volume down.
    with_hits = [r for r in results if (r.get("hits") or 0) > 0]
    for i, res in enumerate(with_hits, 1):
        res["titles"] = fetch_titles(res["pmids"][:3], args.delay)
        if i % 25 == 0 or i == len(with_hits):
            print(f"  {i}/{len(with_hits)} titles fetched", flush=True)

    for res in results:
        res["tier"] = classify(res)
    tiers = Counter(r["tier"] for r in results)

    none_found = [r for r in results if (r.get("hits") or 0) == 0]
    errors = [r for r in results if r.get("error")]
    needs_formulary = len(results) - tiers["veterinary_dosing_candidate"]
    report = {
        "total_gaps_searched": len(results),
        "with_candidate_evidence": len(with_hits),
        "no_evidence_found": len(none_found),
        "request_errors": len(errors),
        "tiers": dict(tiers),
        "needs_formulary": needs_formulary,
        "results": results,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nsearched {len(results)} gaps")
    print(f"  raw hits           : {len(with_hits)}  (a hit is not yet evidence)")
    print(f"  nothing indexed    : {len(none_found)}")
    print(f"  request errors     : {len(errors)}")
    print("  tiers:")
    for tier, count in tiers.most_common():
        print(f"    {tier:30} {count}")
    print(f"  -> needs a formulary: {needs_formulary} of {len(results)}")
    print(f"report -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
