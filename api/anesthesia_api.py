"""Anesthesia & sedation protocols API Blueprint."""

import logging

from flask import Blueprint, jsonify, request

from api.anesthesia_contraindications import (
    check_contraindications,
    get_all_contraindications,
)
from api.anesthesia_protocols import (
    ANESTHESIA_CATEGORIES,
    ANESTHESIA_PROTOCOLS,
    ASA_CLASSIFICATION,
    RISK_LEVELS,
    get_all_species_ids,
    get_protocols_for_species,
    search_protocols,
)

logger = logging.getLogger(__name__)

anesthesia_bp = Blueprint("anesthesia", __name__)

# ---------------------------------------------------------------------------
# Contraindication drug_patterns → drug-dictionary resolution.
# The frontend renders each rule's drug names; annotating which patterns
# resolve to a formulary entry lets it link those names for one-tap dosage
# lookup while leaving class terms ("NSAIDs") and discontinued agents
# ("halothane") as plain text. Built lazily on first request.
# ---------------------------------------------------------------------------
_PATTERN_DRUG_INDEX: dict[str, dict] | None = None


def _build_pattern_drug_index() -> dict[str, dict]:
    import re

    from api.drug_dictionary import DRUGS

    index: dict[str, dict] = {}

    def register(key: str, drug: dict) -> None:
        k = (key or "").strip().lower()
        if len(k) >= 3 and k not in index:
            index[k] = drug

    for d in DRUGS:
        register(d.get("id", ""), d)
        for raw in (d.get("name", ""), d.get("name_ja", "")):
            if not raw:
                continue
            # "Tiletamine/Zolazepam (Telazol/Zoletil)" → base + paren parts,
            # each split on slash / interpunct so every alias resolves.
            m = re.match(r"^([^（(]*)[（(]?([^）)]*)", raw)
            base, paren = (m.group(1), m.group(2)) if m else (raw, "")
            for chunk in (base, paren):
                for part in re.split(r"[／/・,、]", chunk):
                    register(part, d)
    return index


def _pattern_drug_links(patterns: list[str]) -> list[dict]:
    """Resolve contraindication drug patterns to formulary entries."""
    global _PATTERN_DRUG_INDEX
    if _PATTERN_DRUG_INDEX is None:
        _PATTERN_DRUG_INDEX = _build_pattern_drug_index()
    links = []
    seen: set[str] = set()
    for p in patterns:
        d = _PATTERN_DRUG_INDEX.get((p or "").strip().lower())
        if d and d["id"] not in seen:
            seen.add(d["id"])
            links.append(
                {
                    "pattern": p,
                    "id": d["id"],
                    "name": d.get("name", ""),
                    "name_ja": d.get("name_ja", ""),
                }
            )
    return links


@anesthesia_bp.route("/api/anesthesia/protocols", methods=["GET"])
def api_anesthesia_protocols():
    """Return anesthesia protocols, optionally filtered by species/category/query."""
    species = request.args.get("species", "")
    category = request.args.get("category", "")
    query = request.args.get("search", "")

    if species:
        data = get_protocols_for_species(species)
        if not data:
            return jsonify({"error": "Species not found", "species": species}), 404
        # Apply category/query filter
        protocols = data.get("protocols", [])
        if category:
            protocols = [p for p in protocols if p.get("category") == category]
        if query:
            q = query.lower()
            filtered = []
            for p in protocols:
                searchable = " ".join(
                    [
                        p.get("name", {}).get("ja", ""),
                        p.get("name", {}).get("en", ""),
                        p.get("notes_ja", ""),
                        p.get("notes", ""),
                    ]
                    + [d.get("name", "") + " " + d.get("name_ja", "") for d in p.get("drugs", [])]
                ).lower()
                if q in searchable:
                    filtered.append(p)
            protocols = filtered

        return jsonify(
            {
                "species": species,
                "species_name": data.get("species_name", {}),
                "overview": data.get("overview", {}),
                "fasting": data.get("fasting", {}),
                "protocols": protocols,
                "breed_considerations": data.get("breed_considerations", []),
                "references": data.get("references", []),
                "categories": ANESTHESIA_CATEGORIES,
                "risk_levels": RISK_LEVELS,
            }
        )

    # No species specified — return summary for all species
    results = search_protocols(query=query, category=category)
    return jsonify(
        {
            "results": results,
            "total": len(results),
            "categories": ANESTHESIA_CATEGORIES,
            "risk_levels": RISK_LEVELS,
        }
    )


@anesthesia_bp.route("/api/anesthesia/species", methods=["GET"])
def api_anesthesia_species():
    """Return list of species with available anesthesia protocols."""
    species_list = []
    for sp_id in get_all_species_ids():
        sp_data = ANESTHESIA_PROTOCOLS.get(sp_id, {})
        species_list.append(
            {
                "id": sp_id,
                "name": sp_data.get("species_name", {}),
                "protocol_count": len(sp_data.get("protocols", [])),
            }
        )
    return jsonify({"species": species_list, "total": len(species_list)})


@anesthesia_bp.route("/api/anesthesia/categories", methods=["GET"])
def api_anesthesia_categories():
    """Return list of anesthesia categories."""
    return jsonify(
        {
            "categories": ANESTHESIA_CATEGORIES,
            "risk_levels": RISK_LEVELS,
            "asa_classification": ASA_CLASSIFICATION,
        }
    )


@anesthesia_bp.route("/api/anesthesia/contraindications", methods=["GET"])
def api_anesthesia_contraindications():
    """Check drug-disease contraindications.

    Query params:
        drug: Drug name to check
        conditions: Comma-separated condition tags
        species: Species identifier
        breed: Breed name
        all: If "true", return all contraindication rules
    """
    if request.args.get("all") == "true":
        rules = get_all_contraindications()
        return jsonify(
            {
                "rules": [
                    {
                        "drug_patterns": r["drug_patterns"],
                        "conditions": r["conditions"],
                        "severity": r["severity"],
                        "message_ja": r["message_ja"],
                        "message_en": r["message_en"],
                        "drug_links": _pattern_drug_links(r["drug_patterns"]),
                    }
                    for r in rules
                ],
                "total": len(rules),
            }
        )

    drug = request.args.get("drug", "")
    conditions = [c.strip() for c in request.args.get("conditions", "").split(",") if c.strip()]
    species = request.args.get("species", "")
    breed = request.args.get("breed", "")

    warnings = check_contraindications(drug, conditions, species, breed)
    return jsonify({"drug": drug, "warnings": warnings, "count": len(warnings)})
