"""Bring the English ``causes`` field up to Japanese parity.

Across many prior sessions the Japanese ``causes_ja`` field was resolved to the
correct clinical category (``gen_causes_ja`` — a vet-reviewed, category-aware
generator) or curated per disease. The **English** ``causes`` field, however,
never had an equivalent category generator: hundreds of diseases shipped a single
*contentless* catch-all — "Multifactorial etiology depending on disease type." —
regardless of what the disease actually is, and the remainder carried English
category templates that were out of sync with the (correct) Japanese category.

For a bilingual clinical tool aiming at public release this is a visible quality
gap: an English reader opens *Heart Disease* and sees "Multifactorial etiology
depending on disease type" while the Japanese reader sees a proper cardiac
aetiology. This module closes the gap.

Strategy (safe — no new medical claims):

* Detect diseases whose English ``causes`` is one of the recognised *generic
  category* templates (``GENERIC_CATEGORY_CAUSES_EN_MARKS``).
* Skip any disease that resolves to a **named agent** (virus, bacterium, fungus,
  parasite, nutrient, structural mechanism, non-infectious flagship): those are
  owned by ``fix_named_pathogens`` / ``regenerate_named_pathogen_etiology`` and
  must not be clobbered with a generic category paragraph.
* For the rest, determine the category by *fingerprinting the already-reviewed
  Japanese ``causes_ja``* (falling back to name-based resolution when the JA text
  is curated), then render ``gen_causes`` (EN) for that category. The English
  text now states exactly the same category-level aetiology the Japanese already
  conveys — English/Japanese parity, resolved to the correct category.

Used by both the JSON pass (``eliminate_generic_english_causes.py``) and the
served-DB safety net (``ground_english_causes_to_category`` in
``migrate_to_sqlite.py``).
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.bacterial_library import (  # noqa: E402
    bacterial_clinical_fields,
)
from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    build_etiology_fingerprints,
    fingerprint_etiology,
    gen_causes,
    gen_causes_ja,
    resolve_true_category,
)
from scripts.template_elimination.flagship_noninfectious_library import (  # noqa: E402
    flagship_clinical_fields,
)
from scripts.template_elimination.fungal_library import (  # noqa: E402
    fungal_clinical_fields,
)
from scripts.template_elimination.nutritional_library import (  # noqa: E402
    nutrient_clinical_fields,
)
from scripts.template_elimination.parasite_library import (  # noqa: E402
    parasite_clinical_fields,
)
from scripts.template_elimination.pathogen_library import (  # noqa: E402
    viral_clinical_fields,
)
from scripts.template_elimination.structural_library import (  # noqa: E402
    structural_clinical_fields,
)

# Generic *category* aetiology templates carried by the English ``causes`` field.
# These say nothing disease-specific — they are the category-level (or, in the
# case of "Multifactorial etiology depending on disease type", contentless)
# boilerplate that must be resolved to the correct category. Lowercased for
# case-insensitive substring matching. Named-agent aetiologies (Salmonella,
# Mycobacterium, "Caused by parasitic mites of …", rabies virus …) and
# disease-specific mechanistic aetiologies (Urolithiasis causes:, "Protrusion of
# organ …", "Pancreatic inflammation." …) are deliberately excluded — they are
# already specific and must be left untouched.
GENERIC_CATEGORY_CAUSES_EN_MARKS: tuple[str, ...] = (
    # contentless catch-all
    "multifactorial etiology depending on disease type",
    "multifactorial etiology including infectious, environmental, immune",
    "the underlying causes of this condition involve a complex interplay",
    # "<system> etiology. includes/may include …" family
    "respiratory etiology. includes",
    "gastrointestinal etiology. may include",
    "endocrine or metabolic dysfunction. may result",
    "musculoskeletal etiology. includes",
    "neurological etiology. may include",
    "hepatic etiology. includes",
    "ophthalmic etiology. includes",
    "reproductive etiology. includes",
    "traumatic etiology. caused by",
    "dermatological etiology. includes",
    "renal etiology. includes",
    "behavioral etiology. multifactorial",
    "cardiac etiology. may include",
    "dental etiology. includes",
    "genetic or congenital etiology. inherited",
    # "<Category> diseases result from …" family
    "nutritional diseases result from",
    "neoplastic diseases arise from",
    "autoimmune diseases result from",
    "cardiac diseases result from",
    "respiratory diseases result from",
    "metabolic and endocrine diseases result from",
    "congenital and hereditary conditions result from",
    "traumatic injuries result from external mechanical",
    "dermatological conditions result from",
    "renal and urinary tract diseases result from",
    # "Caused by …" category family (not naming a specific agent)
    "caused by physical trauma to musculoskeletal",
    "caused by exposure to toxic substances",
    "caused by dietary deficiency or excess",
    "caused by progressive deterioration of cardiovascular",
    "caused by progressive deterioration of musculoskeletal",
    "caused by progressive deterioration of nervous system",
    "caused by progressive deterioration of ocular",
    "caused by progressive deterioration of dental",
    "caused by progressive deterioration of renal",
    "caused by progressive deterioration of respiratory",
    # generic infection / neoplasia / parasite category boilerplate
    "infectious diseases are caused by pathogenic organisms",
    "neoplastic etiology, often unknown",
    "fungal infections are caused by pathogenic or opportunistic fungi",
    "fungal infection. inhalation or contact",
    "nutritional imbalance. caused by",
    "bacterial infection. transmission via",
    "viral infection. transmission via",
    "parasitic diseases are caused by infection with",
    "caused by parasites infecting affected tissues",
    "external parasite infestation.",
    "endoparasitic infection.",
    "toxicosis results from exposure",
)

_CAUSES_FPS = build_etiology_fingerprints(gen_causes_ja)


def is_generic_category_causes_en(text: str) -> bool:
    """True if the English causes text is a recognised generic category template."""
    if not text:
        return False
    low = text.lower()
    return any(mark in low for mark in GENERIC_CATEGORY_CAUSES_EN_MARKS)


def _resolves_to_named_agent(species: str, name_ja: str, name_en: str) -> bool:
    """True if the disease name identifies a named agent / curated mechanism.

    Those diseases are owned by the named-pathogen / structural / flagship
    pipelines and must not be overwritten with a generic category paragraph.
    """
    return (
        viral_clinical_fields(species, name_ja, name_en)
        or bacterial_clinical_fields(species, name_ja, name_en)
        or fungal_clinical_fields(species, name_ja, name_en)
        or parasite_clinical_fields(species, name_ja, name_en)
        or nutrient_clinical_fields(species, name_ja, name_en)
        or flagship_clinical_fields(species, name_ja, name_en)
        or structural_clinical_fields(species, name_ja, name_en)
    ) is not None


def upgrade_english_causes(
    species: str,
    name_ja: str,
    name_en: str,
    causes_ja: str,
    causes_en: str,
    tagged_category: str = "",
) -> Optional[str]:
    """Return category-resolved English causes, or None to leave the field as-is.

    None is returned when the English text is not a generic category template,
    when the disease resolves to a named agent (owned by another pass), or when
    the regenerated text would be identical to the current value.
    """
    if not is_generic_category_causes_en(causes_en or ""):
        return None
    if _resolves_to_named_agent(species, name_ja or "", name_en or ""):
        return None
    # Prefer the category the (reviewed) Japanese aetiology already uses, so the
    # English text ends up in exactly the same category — true bilingual parity.
    cat = fingerprint_etiology(causes_ja or "", _CAUSES_FPS)
    if cat is None:
        cat = resolve_true_category(name_ja or "", name_en or "", tagged_category or "")
    new = gen_causes(cat, name_en or "", species)
    if new == (causes_en or ""):
        return None
    return new
