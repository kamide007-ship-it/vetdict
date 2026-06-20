"""Replace name-slotted *category-template* descriptions with grounded summaries.

Earlier elimination passes deduplicated descriptions only by **exact string**.
But the description generator slots the disease name + species into a
per-category paragraph, so the produced strings are technically unique while
remaining structurally identical: every feline neoplasm shares one headline,
every avian viral infection shares another, and so on. Normalising out the
disease name, the species name and digits exposes these clusters — and a
clinician opening the database sees the same generic paragraph under disease
after disease, an immediate "generic AI content" tell.

This pass rebuilds those descriptions from the data that is genuinely curated
*per record*: the disease's own presenting signs (``symptoms`` resolved to
localised names), its own recommended diagnostic work-up (``recommended_tests``)
and its triage ``urgency``. The result varies disease-to-disease and reads like
a real one-line clinical summary, while only restating facts already stored in
the record (no new, unverified medical claims).

Run with::

    python3 scripts/template_elimination/eliminate_generic_descriptions.py --preview
    python3 scripts/template_elimination/eliminate_generic_descriptions.py --apply

Then regenerate the delivery DB with ``python3 scripts/migrate_to_sqlite.py``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    _DESC_CATEGORY,
    compose_grounded_description,
    compose_grounded_description_ja,
    resolve_category_from_name,
)
from scripts.template_elimination.eliminate_templates import SPECIES_NORM  # noqa: E402

JSON_PATH = ROOT / "diseases_all_species.json"

# Distinctive sentences from the per-category description paragraphs. Any
# description containing one of these *is* category boilerplate regardless of how
# small its exact-duplicate cluster is (the name/species substitution makes the
# strings differ), so it is regenerated even below the cluster threshold.
# An older enrichment also produced a "systematic-approach" boilerplate
# paragraph (no per-category variation) that the category fingerprints below do
# not cover; list its distinctive sentences explicitly.
_LEGACY_FINGERPRINTS_JA: frozenset[str] = frozenset(
    {
        "病態生理の理解に基づいた系統的アプローチ",
        "に発症する疾患であり、適切な診断と治療介入が必要である",
        "正確な診断と効果的な治療計画の策定が可能となる",
        "個別化された治療戦略が最適な転帰をもたらす",
    }
)
_DESC_FINGERPRINTS_JA: frozenset[str] = _LEGACY_FINGERPRINTS_JA | frozenset(
    s.strip()
    for ja, _ in _DESC_CATEGORY.values()
    for s in ja.split("。")
    if len(s.strip()) >= 15 and "{n}" not in s and "{s}" not in s
)
_DESC_FINGERPRINTS_EN: frozenset[str] = frozenset(
    s.strip()
    for _, en in _DESC_CATEGORY.values()
    for s in en.split(". ")
    if len(s.strip()) >= 25 and "{n}" not in s and "{s}" not in s
)


def _has_fingerprint(text: str, fingerprints: frozenset[str]) -> bool:
    return any(fp in text for fp in fingerprints)


SPECIES_JA = {
    "Cat": "猫",
    "Dog": "犬",
    "Horse": "馬",
    "Rabbit": "ウサギ",
    "Hamster": "ハムスター",
    "Guinea Pig": "モルモット",
    "Chinchilla": "チンチラ",
    "Ferret": "フェレット",
    "Hedgehog": "ハリネズミ",
    "Sugar Glider": "フクロモモンガ",
    "Degu": "デグー",
    "Bird": "鳥",
    "Parakeet": "インコ",
    "Parrot": "オウム",
    "Reptile": "爬虫類",
    "Tortoise": "リクガメ",
    "Snake": "ヘビ",
    "Lizard": "トカゲ",
    "Amphibian": "両生類",
    "Exotic Other": "その他",
    "Fish": "魚",
}


# ---------------------------------------------------------------------------
# Structural-template detection (normalise out disease/species name + digits)
# ---------------------------------------------------------------------------
def _norm(text: str, name: str, species: str) -> str:
    base = re.sub(r"[（(].*", "", name or "").strip()
    out = text or ""
    if base:
        out = out.replace(base, "<D>")
    sp = SPECIES_JA.get(species)
    if sp:
        out = out.replace(sp, "<S>")
    return re.sub(r"[0-9]+", "#", out)


def find_template_norms(records: list[dict], field: str, min_cluster: int) -> set[str]:
    counts: Counter[str] = Counter()
    for r in records:
        v = (r.get(field) or "").strip()
        if len(v) < 25:
            continue
        counts[_norm(v, r.get("name_ja") or r.get("name") or "", r.get("species"))] += 1
    return {n for n, c in counts.items() if c >= min_cluster}


# ---------------------------------------------------------------------------
# Per-record signal extraction
# ---------------------------------------------------------------------------
_TEST_SPLIT = re.compile(r"^(?P<ja>[^(（]+?)\s*[（(](?P<en>[^)）]*)[)）]\s*$")


def parse_tests(recommended_tests) -> tuple[list[str], list[str]]:
    """Split ``recommended_tests`` of form ``"JA (EN)"`` into JA and EN lists."""
    ja, en = [], []
    for t in recommended_tests or []:
        if not isinstance(t, str):
            continue
        m = _TEST_SPLIT.match(t.strip())
        if m:
            ja.append(m.group("ja").strip())
            en.append(m.group("en").strip())
        else:
            ja.append(t.strip())
            en.append(t.strip())
    return ja, en


def build_symptom_maps() -> dict:
    from api.health_checker import _get_species_symptom_names

    maps = {}
    for disp, norm in SPECIES_NORM.items():
        try:
            maps[disp] = _get_species_symptom_names(norm)
        except Exception:
            maps[disp] = {}
    return maps


def resolve_signs(symptoms, name_map) -> tuple[list[str], list[str]]:
    ja, en = [], []
    for s in symptoms or []:
        info = name_map.get(s)
        if not info:
            continue
        j = (info.get("ja") or "").strip()
        e = (info.get("en") or "").strip()
        if j:
            ja.append(j)
        if e:
            en.append(e)
    return ja, en


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes to JSON")
    ap.add_argument("--preview", action="store_true", help="show sample regenerations")
    ap.add_argument("--min-cluster", type=int, default=5)
    args = ap.parse_args()

    records = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    tmpl_ja = find_template_norms(records, "description_ja", args.min_cluster)
    tmpl_en = find_template_norms(records, "description", args.min_cluster)
    print(f"structural-template clusters: description_ja={len(tmpl_ja)} description={len(tmpl_en)}")

    symptom_maps = build_symptom_maps()

    changed_ja = changed_en = 0
    by_species: Counter[str] = Counter()
    samples: list[tuple] = []

    for r in records:
        species = r.get("species")
        name_ja = r.get("name_ja") or ""
        name_en = r.get("name") or ""
        category = resolve_category_from_name(name_ja, name_en) or "generic"
        urgency = r.get("urgency") or ""
        test_ja, test_en = parse_tests(r.get("recommended_tests"))
        sign_ja, sign_en = resolve_signs(r.get("symptoms"), symptom_maps.get(species, {}))

        cur_ja = (r.get("description_ja") or "").strip()
        if cur_ja and (_norm(cur_ja, name_ja, species) in tmpl_ja or _has_fingerprint(cur_ja, _DESC_FINGERPRINTS_JA)):
            new_ja = compose_grounded_description_ja(
                name_ja, SPECIES_NORM.get(species, species), category, sign_ja, test_ja, urgency
            )
            if new_ja and new_ja != cur_ja:
                if args.apply:
                    r["description_ja"] = new_ja
                changed_ja += 1
                by_species[species] += 1
                if len(samples) < 24 and len(samples) % 1 == 0:
                    samples.append((species, name_ja, cur_ja, new_ja))

        cur_en = (r.get("description") or "").strip()
        if cur_en and (_norm(cur_en, name_en, species) in tmpl_en or _has_fingerprint(cur_en, _DESC_FINGERPRINTS_EN)):
            new_en = compose_grounded_description(
                name_en, SPECIES_NORM.get(species, species), category, sign_en, test_en, urgency
            )
            if new_en and new_en != cur_en:
                if args.apply:
                    r["description"] = new_en
                changed_en += 1

    print(f"regenerated: description_ja={changed_ja} description={changed_en}")
    print("by species (JA):", dict(by_species.most_common()))

    if args.preview:
        # diversify samples across species
        seen_sp: set[str] = set()
        shown = 0
        for sp, nm, old, new in samples:
            if sp in seen_sp and shown >= 12:
                continue
            seen_sp.add(sp)
            print("\n=====", sp, "|", nm)
            print("OLD:", old)
            print("NEW:", new)
            shown += 1
            if shown >= 20:
                break

    if args.apply:
        # Preserve the file's compact on-disk format (no indent, no trailing
        # newline) so the diff is limited to the changed values.
        JSON_PATH.write_text(
            json.dumps(records, ensure_ascii=False, separators=(",", ":")), encoding="utf-8"
        )
        # Verify no residual structural templates among regenerated descriptions
        residual_ja = find_template_norms(records, "description_ja", args.min_cluster)
        residual_en = find_template_norms(records, "description", args.min_cluster)
        print(f"post-apply structural clusters: description_ja={len(residual_ja)} description={len(residual_en)}")
        # report any remaining clusters with their entry counts
        for field, norms in (("description_ja", residual_ja), ("description", residual_en)):
            if not norms:
                continue
            c2: dict[str, list] = defaultdict(list)
            for r in records:
                v = (r.get(field) or "").strip()
                if len(v) < 25:
                    continue
                n = _norm(v, r.get("name_ja") or r.get("name") or "", r.get("species"))
                if n in norms:
                    c2[n].append((r.get("species"), r.get("name_ja")))
            print(f"  remaining {field} clusters:")
            for n, items in sorted(c2.items(), key=lambda kv: -len(kv[1]))[:10]:
                print(f"    [{len(items)}x] {n[:90]}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
