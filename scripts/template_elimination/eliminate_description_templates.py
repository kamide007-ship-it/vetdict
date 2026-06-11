"""Replace template-shaped disease *descriptions* with disease-specific text.

The ``description`` (EN) and ``description_ja`` (JA) fields are the headline
summary shown directly under each disease name in the database browser, in
diagnostic-chat result cards, and in differential-diagnosis results. For the
exotic species these fields were filled by an early enrichment pass with
**category-level boilerplate** that:

* repeats verbatim across many unrelated diseases (e.g. one parasitic-disease
  paragraph shared by 12 different tortoise parasites), and
* is frequently **mis-categorised** — e.g. "cheek pouch impaction" described
  as an *infectious disease* — which is an immediate credibility killer for a
  clinical decision-support tool aimed at veterinarians.

This script detects those template descriptions and regenerates concise,
disease-specific, correctly-categorised replacements (both languages) using
``clinical_fields_generator``. The name-based category resolver also corrects
the mis-categorisations.

Run with::

    python3 scripts/template_elimination/eliminate_description_templates.py

Followed by ``python3 scripts/migrate_to_sqlite.py``.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    generate_clinical_fields,
)
from scripts.template_elimination.eliminate_templates import SPECIES_NORM  # noqa: E402

# Sentences that only ever appear in the auto-generated category boilerplate.
# Any description containing one of these is a template regardless of how its
# (species-substituted) lead sentence varies.
BOILERPLATE_MARKERS_JA = (
    "臨床症状の重症度と全身状態を総合的に評価し",
    "飼育環境の最適化と栄養管理が回復の促進に重要な役割を果たす",
    "定期的な再評価により治療反応を確認し、必要に応じて治療計画の修正を行う",
)
BOILERPLATE_MARKERS_EN = (
    "Comprehensive assessment of clinical signs and overall condition",
    "Optimization of husbandry and nutritional management plays",
    "Regular reassessment confirms treatment response",
)


def _is_stub_ja(text: str) -> bool:
    """Detect the field-label-scaffolding stub descriptions.

    e.g. "XはYにみられる疾患である。YにおけるXの原因: …。主要な臨床徴候は
    YにおけるXの臨床徴候は以下を含む。など。…" — these read as broken prose
    (a dangling "以下を含む。など。" lists nothing) and just restate field
    labels. The disease-specific detail they embed also lives in the dedicated
    causes_ja / clinical_signs_ja / treatment_ja fields, so the headline summary
    is better served by a clean category description.
    """
    if not text:
        return False
    if "にみられる疾患である" not in text:
        return False
    return "の臨床徴候は以下を含む" in text or "の原因:" in text or "の原因：" in text


# A description is also treated as a template if its exact text is shared by
# this many or more entries (catches any boilerplate without a known marker).
DUPLICATE_THRESHOLD = 3
MIN_TEXT_LEN = 40


def _exact_duplicate_texts(data: list[dict], field: str) -> set[str]:
    cnt: Counter = Counter()
    for entry in data:
        text = (entry.get(field) or "").strip()
        if text and len(text) >= MIN_TEXT_LEN:
            cnt[text] += 1
    return {t for t, c in cnt.items() if c >= DUPLICATE_THRESHOLD}


def _is_template(text: str, markers: tuple[str, ...], dup_texts: set[str]) -> bool:
    text = (text or "").strip()
    if not text:
        return False
    if any(m in text for m in markers):
        return True
    return text in dup_texts


def update_json(json_path: Path) -> tuple[int, dict[str, int]]:
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    dup_ja = _exact_duplicate_texts(data, "description_ja")
    dup_en = _exact_duplicate_texts(data, "description")

    counts = {"description": 0, "description_ja": 0}
    entries_modified = 0

    for entry in data:
        ja = entry.get("description_ja") or ""
        en = entry.get("description") or ""
        ja_tmpl = _is_template(ja, BOILERPLATE_MARKERS_JA, dup_ja) or _is_stub_ja(ja)
        en_tmpl = _is_template(en, BOILERPLATE_MARKERS_EN, dup_en)

        # Each language is regenerated independently iff its own description is a
        # template, so curated/unique descriptions in either language are kept.
        if not (ja_tmpl or en_tmpl):
            continue

        fields = []
        if ja_tmpl:
            fields.append("description_ja")
        if en_tmpl:
            fields.append("description")

        species = entry.get("species", "")
        species_norm = SPECIES_NORM.get(species, species).lower()
        new_content = generate_clinical_fields(
            species_norm,
            entry.get("name_ja", ""),
            entry.get("name", ""),
            entry.get("category", ""),
            fields,
        )

        changed = False
        for field, text in new_content.items():
            if text and text != entry.get(field, ""):
                entry[field] = text
                counts[field] += 1
                changed = True
        if changed:
            entries_modified += 1

    with open(json_path, "w", encoding="utf-8") as f:
        # Compact: pretty-printing would push the blob past GitHub's 100 MiB
        # limit; it is read at runtime, not edited by hand.
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    return entries_modified, counts


def main() -> None:
    json_path = ROOT / "diseases_all_species.json"
    if not json_path.exists():
        print(f"ERROR: {json_path} not found")
        sys.exit(1)

    print(f"Processing {json_path}...")
    modified, counts = update_json(json_path)
    print(f"\nEntries modified: {modified}")
    for field, n in counts.items():
        print(f"  {field}: {n}")


if __name__ == "__main__":
    main()
