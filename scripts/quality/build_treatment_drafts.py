"""Build the treatment-dosage DRAFT worklist for a species (T105).

SAFETY: This NEVER fabricates a dose. It produces a review worklist of diseases
whose treatment section lacks any dosage pattern, so a veterinarian can supply
cited doses. Each entry is created with ``review_status: "draft"`` and empty
``treatment_ja`` / ``sources`` — nothing is publishable until a human fills the
dose AND a source AND flips ``review_status`` to ``published`` (enforced by
``api/species/treatment_overrides.py``).

Sourcing policy (per SPEC failure condition): if a dose can be lifted verbatim
from the disease's existing in-repo English protocol (already vet-authored), it
is offered as ``en_reference`` for translation+verification (still a draft, not
published). If NO in-repo dose exists, the entry is marked ``needs_sourcing``.
If more than half of a batch needs external sourcing, the tool reports the stop
condition rather than proceeding to fabricate.

Idempotent: preserves any human edits to existing entries (only adds new gap
entries; never overwrites a non-draft entry). Backs up an existing file.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import scripts.quality.detect as detect
from api.species.canonical import apply_canonical_map

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "api" / "data" / "treatment_overrides"


def _slug(name: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")


# Authoritative dosing sources per species group (formularies are the real
# source of exotic clinical doses; PubMed exotic-dosing coverage is thin).
_FORMULARY_HINT = {
    "small_mammal": "Carpenter『Exotic Animal Formulary』6th ed / Plumb『Veterinary Drug Handbook』/ Quesenberry & Carpenter『Ferrets, Rabbits, and Rodents』4th ed",
    "bird": "Carpenter『Exotic Animal Formulary』6th ed / Harrison & Lightfoot『Clinical Avian Medicine』",
    "reptile": "Carpenter『Exotic Animal Formulary』6th ed / Mader『Reptile Medicine and Surgery』3rd ed",
    "amphibian_fish": "Carpenter『Exotic Animal Formulary』6th ed / Stoskopf『Fish Medicine』",
    "dog_cat": "Plumb『Veterinary Drug Handbook』/ BSAVA Formulary",
    "horse": "Plumb『Veterinary Drug Handbook』/ Bertone & Horspool『Equine Clinical Pharmacology』",
}
_SPECIES_GROUP = {
    "dog": "dog_cat", "cat": "dog_cat", "horse": "horse",
    "rabbit": "small_mammal", "ferret": "small_mammal", "hamster": "small_mammal",
    "guinea_pig": "small_mammal", "chinchilla": "small_mammal", "hedgehog": "small_mammal",
    "sugar_glider": "small_mammal", "degu": "small_mammal", "exotic_other": "small_mammal",
    "bird": "bird", "parakeet": "bird", "parrot": "bird",
    "reptile": "reptile", "tortoise": "reptile", "snake": "reptile", "lizard": "reptile",
    "amphibian": "amphibian_fish", "fish": "amphibian_fish",
}


def _sourcing_guidance(name_en: str, species: str) -> str:
    grp = _SPECIES_GROUP.get(species, "small_mammal")
    formulary = _FORMULARY_HINT.get(grp, _FORMULARY_HINT["small_mammal"])
    query = f"{name_en} {species} OR exotic OR rodent treatment".strip()
    return f"推奨情報源: {formulary}。PubMed候補検索: 「{query}」。"


def build(species: str) -> dict:
    records = apply_canonical_map(detect.load_species_records(species), species)
    et = detect.detect_empty_treatment(records)
    flagged = et["empty"] + et["heading_only"]
    by_id = {r["id"]: r for r in records}

    entries = []
    needs_sourcing = 0
    for f in flagged:
        r = by_id.get(f["id"], {})
        en_tx = r.get("treatment") or ""
        ja_tx = r.get("treatment_ja") or ""
        en_has = detect._has_dosage(en_tx)
        if en_has and not detect._has_dosage(ja_tx):
            source_kind = "en_reference"  # translate + verify existing EN dose
        else:
            source_kind = "needs_sourcing"  # no in-repo dose — external evidence required
            needs_sourcing += 1
        entries.append(
            {
                "slug": _slug(r.get("name") or r.get("name_en") or ""),
                "name": r.get("name"),
                "name_ja": r.get("name_ja"),
                "review_status": "draft",
                "source_kind": source_kind,
                "en_reference": en_tx if source_kind == "en_reference" else "",
                "current_treatment_ja": ja_tx,
                "treatment_ja": "",  # to be filled by veterinarian
                "sources": [],  # required before publish
                "sourcing_guidance": _sourcing_guidance(r.get("name") or r.get("name_en") or "", species),
            }
        )

    total = len(flagged)
    return {
        "species": species,
        "schema_version": 1,
        "note": "DRAFT worklist. Nothing here is served until review_status='published' AND sources present.",
        "counts": {
            "gap_diseases": total,
            "draftable_from_en": total - needs_sourcing,
            "needs_external_sourcing": needs_sourcing,
        },
        "stop_condition_triggered": total > 0 and needs_sourcing > total / 2,
        "entries": entries,
    }


def _merge_preserving_human_edits(existing: dict, fresh: dict) -> dict:
    """Keep any existing entry that a human has touched (non-draft or filled);
    only append newly-detected gap entries. Never overwrites human work."""
    if not existing:
        return fresh
    by_slug = {e["slug"]: e for e in existing.get("entries", [])}
    out_entries = []
    seen = set()
    for e in fresh["entries"]:
        prev = by_slug.get(e["slug"])
        if prev and (prev.get("review_status") != "draft" or prev.get("treatment_ja") or prev.get("sources")):
            out_entries.append(prev)  # preserve human edits
        else:
            out_entries.append(e)  # pristine draft -> take fresh (propagates new fields)
        seen.add(e["slug"])
    # keep any human entries no longer flagged (do not drop reviewed work)
    for slug, prev in by_slug.items():
        if slug not in seen and (prev.get("review_status") != "draft" or prev.get("treatment_ja")):
            out_entries.append(prev)
    fresh = dict(fresh)
    fresh["entries"] = out_entries
    return fresh


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("species", nargs="?", default="degu")
    ap.add_argument("--apply", action="store_true", help="write the worklist file")
    args = ap.parse_args()

    result = build(args.species)
    c = result["counts"]
    print(
        f"[{args.species}] gap_diseases={c['gap_diseases']} "
        f"draftable_from_en={c['draftable_from_en']} needs_sourcing={c['needs_external_sourcing']}"
    )
    if result["stop_condition_triggered"]:
        print(
            "  ⚠ STOP CONDITION: more than half of the batch has no in-repo dose to cite. "
            "Per SPEC, doses are NOT fabricated. This worklist is for veterinarian sourcing only."
        )

    if not args.apply:
        print("(dry-run — pass --apply to write the worklist)")
        return 0

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{args.species}.json"
    if out.exists():
        try:
            existing = json.loads(out.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            existing = None
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M")
        bak = ROOT / "backups" / stamp
        bak.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out, bak / out.name)
        result = _merge_preserving_human_edits(existing, result)
        print(f"backed up + preserved human edits -> {bak / out.name}")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
