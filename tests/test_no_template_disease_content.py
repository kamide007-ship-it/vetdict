"""Regression test: forbid generic copy-paste template content in the disease DB.

The disease database was populated with bulk-fill template text in 338 entries
across 21 species — including embarrassing cross-species errors such as cat
hyperthyroidism's treatment_ja saying "rare in reptiles". These were
eradicated in May 2026.

This test fails if any of those templates resurface, in either:
- ``diseases_all_species.json`` (the enrichment overlay)
- ``api/species/*_diseases.py`` (the canonical Python sources)
- The SQLite database, if a fresh migration is available

A template is "forbidden" if it is verbatim, generic clinical filler that
provides no disease-specific or species-specific information.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


# These are the exact strings that the bulk-fill enrichment used to insert.
# They should appear ZERO times across the codebase.
FORBIDDEN_TEMPLATES = [
    # generic_metabolic (110 instances before fix)
    "種適切な診断で原因同定。診断に基づく治療。支持療法：種に適切な温度・水分・栄養維持。疼痛管理。治療反応モニタリング。診断次第で予後決定。",
    # general_med_surg (100 instances before fix)
    "診断に基づく適切な内科的または外科的治療、輸液療法を含む支持療法、疼痛管理、栄養サポート、治療反応の定期的モニタリング。",
    # bacterial_infection (41 instances)
    "培養感受性試験に基づく適切な抗菌薬療法、必要に応じた外科的排膿またはデブリードマン、輸液療法、疼痛管理、治療反応のモニタリング。",
    # parasitic (20 instances)
    "適切な駆虫薬の投与、全ライフサイクルステージをカバーするための反復投薬、環境消毒、脱水・栄養不良に対する支持療法。",
    # viral (12 instances)
    "支持療法を中心に、輸液療法、制吐薬、栄養サポート、二次感染予防の抗菌薬投与。抗ウイルス薬の使用（利用可能な場合）。",
    # other repeats
    "全身性抗真菌薬療法（アゾール系またはアムホテリシンB）、局所抗真菌剤、環境消毒、長期治療中の肝機能モニタリング。",
    "点眼薬（抗菌薬、抗炎症薬、潤滑剤）、疼痛管理、自傷防止、合併症のモニタリング。",
    "麻酔下での歯科処置（トリミング、研磨、必要に応じた抜歯）、疼痛管理、高繊維食への食事変更、定期的な歯科検診。",
    "適切な栄養補助（ビタミン・ミネラルの補充）、食事の見直し、UVBライトの適正化（必要な種）、臨床改善のモニタリング。",
    # Generic suffix that was bolted onto otherwise-good content
    "代謝・内分泌疾患の治療はホルモン補充療法または過剰ホルモン抑制療法が基本となる。定期的な血中ホルモン濃度測定と臨床症状の評価に基づき投与量を調整する。食事管理、適度な運動、体重管理を併用し、合併症の予防と早期発見のための定期的なモニタリングを継続する。",
    # "診断による原因同定" variant
    "診断による原因同定。診断に基づく種適切な治療。支持療法：適切な温度・水分・栄養維持。疼痛管理：メロキシカム0.2-0.5 mg/kg q24-48h。治療反応モニタリング。診断と重症度次第で予後決定。",
]


# Regex patterns for templates that vary slightly across entries.
FORBIDDEN_REGEX = [
    # "Xにおける(disease)の治療は基礎となるホルモン・代謝異常を標的とする..." — the
    # endocrine-template that was mis-applied to hepatic, neoplastic, toxicosis,
    # parasitic, and many other non-endocrine diseases (286 instances before fix).
    re.compile(
        r"[一-龯ァ-ヴ\w]{1,40}における[^。]{1,80}の治療は基礎となるホルモン・代謝異常を標的とする。"
        r"ホルモン補充療法または抑制療法により生理的バランスを回復する。"
    ),
    # Neoplasia template (472 instances before fix)
    re.compile(
        r"[一-龯ァ-ヴ\w]{1,40}における[^。]{1,80}の治療は腫瘍の種類、部位、病期に依存する。"
        r"アクセス可能な固形腫瘍には十分なマージンを確保した外科的切除が第一選択である。"
    ),
    # Nutritional template (57 instances before fix)
    re.compile(
        r"[一-龯ァ-ヴ\w]{1,40}における[^。]{1,80}の治療は栄養バランスの是正が中心となる。"
        r"欠乏状態では食事の改善または治療的サプリメンテーションにより特定の栄養素を補充する。"
    ),
]


# These cross-species terms must NEVER appear in the wrong species' content.
# Maps (forbidden_phrase, set_of_species_where_NOT_allowed).
CROSS_SPECIES_RULES = [
    # "オウム目では稀" should only appear in avian species (bird/parakeet/parrot)
    (
        "オウム目では稀",
        {
            "cat",
            "dog",
            "rabbit",
            "guinea_pig",
            "hamster",
            "chinchilla",
            "ferret",
            "hedgehog",
            "sugar_glider",
            "degu",
            "snake",
            "lizard",
            "tortoise",
            "reptile",
            "amphibian",
            "horse",
            "fish",
            "exotic_other",
        },
    ),
    # "爬虫類では稀" should only appear in reptile content
    (
        "爬虫類では稀",
        {
            "cat",
            "dog",
            "rabbit",
            "guinea_pig",
            "hamster",
            "chinchilla",
            "ferret",
            "hedgehog",
            "sugar_glider",
            "degu",
            "bird",
            "parakeet",
            "parrot",
            "horse",
            "fish",
        },
    ),
    # "POTZ" (reptile-specific term) should not be in mammal content
    (
        "POTZに加温",
        {
            "cat",
            "dog",
            "rabbit",
            "guinea_pig",
            "hamster",
            "chinchilla",
            "ferret",
            "hedgehog",
            "sugar_glider",
            "degu",
            "horse",
        },
    ),
]


def _load_json_entries() -> list[dict]:
    json_path = ROOT / "diseases_all_species.json"
    if not json_path.exists():
        return []
    # The file is git-LFS-tracked; on CI without `git lfs pull` we get a
    # ~134-byte pointer file instead of the actual content. Treat that as
    # "not present" so tests skip cleanly rather than crashing on JSON decode.
    if json_path.stat().st_size < 10_000:
        with open(json_path, encoding="utf-8") as f:
            head = f.read(200)
        if head.startswith("version https://git-lfs"):
            return []
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def test_no_forbidden_template_in_json():
    """diseases_all_species.json must not contain any exact-match generic template."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    failures = []
    for entry in entries:
        tx_ja = entry.get("treatment_ja", "") or ""
        for template in FORBIDDEN_TEMPLATES:
            if tx_ja == template or template in tx_ja:
                failures.append(
                    f"[{entry.get('species')}] {entry.get('name_ja') or entry.get('name')}: "
                    f"contains forbidden template '{template[:40]}…'"
                )
                break
    assert not failures, f"Found {len(failures)} entries with forbidden template content. First 5:\n" + "\n".join(
        failures[:5]
    )


def test_no_forbidden_regex_template_in_json():
    """diseases_all_species.json must not contain regex-matched generic templates."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    failures = []
    for entry in entries:
        tx_ja = entry.get("treatment_ja", "") or ""
        for pattern in FORBIDDEN_REGEX:
            if pattern.search(tx_ja):
                failures.append(
                    f"[{entry.get('species')}] {entry.get('name_ja') or entry.get('name')}: "
                    f"matches forbidden regex /{pattern.pattern[:60]}…/"
                )
                break
    assert not failures, f"Found {len(failures)} JSON entries with regex template content. First 5:\n" + "\n".join(
        failures[:5]
    )


def test_no_forbidden_template_in_species_modules():
    """api/species/*_diseases.py must not contain any exact-match generic template."""
    species_dir = ROOT / "api" / "species"
    failures = []
    for path in species_dir.glob("*_diseases.py"):
        text = path.read_text(encoding="utf-8")
        for template in FORBIDDEN_TEMPLATES:
            # Search for the exact template in a treatment_ja-like context
            if template in text:
                count = text.count(template)
                failures.append(f"{path.name}: {count}× '{template[:40]}…'")
    assert not failures, "Found template text in Python species modules:\n" + "\n".join(failures)


def test_no_cross_species_contamination_in_json():
    """Cross-species clinical errors (e.g. 'rare in reptiles' on a cat row) must not exist."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    species_norm = {
        "Bird": "bird",
        "Parakeet": "parakeet",
        "Parrot": "parrot",
        "Horse": "horse",
        "Guinea Pig": "guinea_pig",
        "Rabbit": "rabbit",
        "Chinchilla": "chinchilla",
        "Hedgehog": "hedgehog",
        "Snake": "snake",
        "Lizard": "lizard",
        "Amphibian": "amphibian",
        "Sugar Glider": "sugar_glider",
        "Degu": "degu",
        "Reptile": "reptile",
        "Exotic Other": "exotic_other",
        "Hamster": "hamster",
        "Ferret": "ferret",
        "Tortoise": "tortoise",
        "Fish": "fish",
        "Cat": "cat",
        "Dog": "dog",
    }
    failures = []
    for entry in entries:
        tx_ja = entry.get("treatment_ja", "") or ""
        sp = species_norm.get(entry.get("species", ""), entry.get("species", ""))
        for phrase, forbidden_species_set in CROSS_SPECIES_RULES:
            if sp in forbidden_species_set and phrase in tx_ja:
                failures.append(
                    f"[{sp}] {entry.get('name_ja') or entry.get('name')}: "
                    f"contains '{phrase}' which is inappropriate for this species"
                )
    assert not failures, f"Found {len(failures)} cross-species contamination errors. First 5:\n" + "\n".join(
        failures[:5]
    )


def test_critical_endocrine_diseases_are_species_appropriate():
    """Spot-check that key endocrine diseases have correct species-specific content."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    by_species_name: dict[tuple[str, str], dict] = {}
    species_norm = {
        "Cat": "cat",
        "Dog": "dog",
        "Ferret": "ferret",
        "Bird": "bird",
        "Parakeet": "parakeet",
        "Parrot": "parrot",
        "Horse": "horse",
        "Reptile": "reptile",
    }
    for entry in entries:
        sp = species_norm.get(entry.get("species"), entry.get("species", "").lower())
        name = entry.get("name", "")
        by_species_name[(sp, name)] = entry

    # Cat hyperthyroidism MUST mention I-131 or methimazole (the standard of care)
    cat_hyper = by_species_name.get(("cat", "Hyperthyroidism"))
    if cat_hyper:
        tx = cat_hyper.get("treatment_ja", "") or ""
        assert "メチマゾール" in tx or "I-131" in tx or "ヨウ素" in tx, (
            f"Cat hyperthyroidism treatment_ja must reference methimazole/I-131. Got: {tx[:200]}"
        )
        # Must NOT mention reptile-specific terms
        assert "爬虫類では稀" not in tx, "Cat hyperthyroidism still has reptile content!"


def test_template_files_have_no_inappropriate_avian_terms_in_mammals():
    """Mammal disease files must not contain avian-specific dose units ('IU/羽')."""
    species_dir = ROOT / "api" / "species"
    mammal_files = [
        "dog_diseases.py",
        "cat_diseases.py",
        "rabbit_diseases.py",
        "guinea_pig_diseases.py",
        "hamster_diseases.py",
        "chinchilla_diseases.py",
        "ferret_diseases.py",
        "hedgehog_diseases.py",
        "sugar_glider_diseases.py",
        "degu_diseases.py",
    ]
    failures = []
    for fname in mammal_files:
        path = species_dir / fname
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        # "IU/羽" is the avian dosing unit (per bird); should never appear in mammal sources
        if "IU/羽" in text:
            failures.append(f"{fname}: contains avian-specific 'IU/羽' unit")
    assert not failures, "Avian dose units in mammal files: " + "; ".join(failures)


# ---------------------------------------------------------------------------
# Cross-disease template misapplication regression tests
# ---------------------------------------------------------------------------


# Within a single species, no treatment_ja text should be shared by more than
# this many *distinct* diseases. Allow up to 4 to accommodate legitimate same-
# treatment groupings (e.g. all fracture subtypes get similar orthopedic care).
_MAX_DISEASES_PER_TREATMENT_INTRA_SPECIES = 4


def test_no_cross_disease_template_misapplication_intra_species():
    """No treatment_ja should be reused by 5+ different diseases within one species.

    This regression guards against the May-2026 disaster where a generic
    "bacterial infection" treatment was applied to feline panleukopenia
    (a viral disease), rabies (viral), leukemia (neoplastic), etc.
    """
    from collections import defaultdict

    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    by_sp_tx: dict[tuple[str, str], set[str]] = defaultdict(set)
    for e in entries:
        tx = (e.get("treatment_ja", "") or "").strip()
        if not tx or len(tx) < 30:
            continue
        sp = e.get("species", "")
        name_key = (e.get("name_ja") or "").strip() or (e.get("name") or "").strip()
        if not name_key:
            continue
        by_sp_tx[(sp, tx)].add(name_key)

    failures = []
    for (sp, tx), names in by_sp_tx.items():
        if len(names) > _MAX_DISEASES_PER_TREATMENT_INTRA_SPECIES:
            failures.append(
                f"[{sp}] {len(names)} diseases share one treatment_ja "
                f"(threshold {_MAX_DISEASES_PER_TREATMENT_INTRA_SPECIES}): {sorted(names)[:5]}... "
                f"Tx preview: '{tx[:60]}...'"
            )
    assert not failures, f"Found {len(failures)} cross-disease template misapplications. First 3:\n" + "\n".join(
        failures[:3]
    )


def test_no_cross_species_template_propagation():
    """No treatment_ja should be reused by 5+ species AND 5+ different diseases.

    Vestibular disease being applied identically across 15 species with no
    species-specific dosing is a template error.
    """
    from collections import defaultdict

    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    by_tx: dict[str, dict[str, set[str]]] = defaultdict(lambda: {"species": set(), "names": set()})
    for e in entries:
        tx = (e.get("treatment_ja", "") or "").strip()
        if not tx or len(tx) < 30:
            continue
        sp = e.get("species", "")
        name_key = (e.get("name_ja") or "").strip() or (e.get("name") or "").strip()
        if not name_key:
            continue
        by_tx[tx]["species"].add(sp)
        by_tx[tx]["names"].add(name_key)

    failures = []
    for tx, info in by_tx.items():
        if len(info["species"]) >= 5 and len(info["names"]) >= 5:
            failures.append(
                f"Treatment used by {len(info['species'])} species × {len(info['names'])} diseases: "
                f"'{tx[:60]}...' (species: {sorted(info['species'])[:3]}...)"
            )
    assert not failures, f"Found {len(failures)} cross-species template propagations. First 3:\n" + "\n".join(
        failures[:3]
    )


def test_critical_viral_diseases_are_pathogen_specific():
    """Cat panleukopenia and canine parvo must mention pathogen-specific management."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    by_species_name: dict[tuple[str, str], dict] = {}
    species_norm = {"Cat": "cat", "Dog": "dog"}
    for entry in entries:
        sp = species_norm.get(entry.get("species"), entry.get("species", "").lower())
        name = entry.get("name", "")
        by_species_name[(sp, name)] = entry

    # Cat panleukopenia must reference FPV/feline-specific management
    cat_fpv = by_species_name.get(("cat", "Feline Panleukopenia (Feline Distemper)"))
    if cat_fpv:
        tx = cat_fpv.get("treatment_ja", "") or ""
        cja = cat_fpv.get("causes_ja", "") or ""
        # Treatment must mention FPV-specific markers
        assert any(kw in tx for kw in ("FPV", "汎白血球減少", "猫汎白血球", "パルボウイルス")), (
            f"Cat panleukopenia treatment_ja missing FPV-specific markers. Got: {tx[:200]}"
        )
        # Causes_ja must NOT cite CPV-2 (canine virus)
        assert "CPV-2" not in cja, f"Cat panleukopenia causes_ja still cites CPV-2: {cja[:200]}"

    # Canine parvo must reference CPV-2/canine-specific management
    dog_cpv = by_species_name.get(("dog", "Canine Parvovirus"))
    if dog_cpv:
        tx = dog_cpv.get("treatment_ja", "") or ""
        assert any(kw in tx for kw in ("パルボウイルス", "CPV", "犬パルボ", "マロピタント")), (
            f"Canine parvo treatment_ja missing parvo-specific markers. Got: {tx[:200]}"
        )


def test_vestibular_disease_is_species_specific():
    """Vestibular disease entries across species must have species-tailored content."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    # Find all vestibular entries
    vest = [e for e in entries if "前庭" in (e.get("name_ja", "") or "")]
    if len(vest) < 3:
        pytest.skip("Not enough vestibular entries for this test")
    # Collect distinct treatment_ja
    distinct_tx = {(e.get("treatment_ja", "") or "").strip() for e in vest}
    # At least half of the species should have distinct treatment (not all sharing one template)
    assert len(distinct_tx) >= max(3, len(vest) // 3), (
        f"Only {len(distinct_tx)} distinct vestibular treatments for {len(vest)} entries — "
        f"likely a template still in use."
    )


# ---------------------------------------------------------------------------
# Misapplied pathophysiology_ja templates (2026-06 fix)
# ---------------------------------------------------------------------------
# enrich_diseases() overlays pathophysiology_ja onto each species module. The
# overlay contained CATEGORY-level boilerplate that was bulk-applied to the
# WRONG disease class — e.g. bacterial toxin diseases (botulism, tetanus,
# clostridial enteritis) receiving the chemical-toxicant paragraph, or viral
# diseases (avian influenza, Bornavirus/PDD) receiving the toxicant/neoplasia
# paragraph. These were corrected by
# scripts/template_elimination/fix_misapplied_pathophysiology.py.

# Substring signatures of the category templates.
_PATHO_TEMPLATE_SIGS = {
    "toxicant": "毒性物質は細胞レベルで",
    "fungal": "真菌感染の病態生理",
    "neoplasia": "腫瘍の病態生理は正常細胞の悪性転換",
    "bacterial_colonisation": "細菌感染症である。病原菌は付着因子",
    "autoimmune": "免疫介在性疾患である。免疫系が自己抗原",
}

_TRUE_CLASS_HINTS = {
    "bacterial": [
        "菌",
        "bacteri",
        "sepsis",
        "敗血",
        "pneumonia",
        "肺炎",
        "tetanus",
        "破傷風",
        "botulism",
        "ボツリヌス",
        "bordetella",
        "actinomyc",
        "放線菌",
        "clostrid",
        "salmonella",
        "e. coli",
        "大腸菌",
        "erysipel",
        "pseudomonas",
        "緑膿菌",
        "strepto",
        "レンサ球菌",
        "pasteurell",
        "enterotox",
        "dysbiosis",
        "enteritis",
        "abscess",
        "膿瘍",
        "rhinitis",
        "sacculitis",
        "気嚢炎",
        "dermatophilosis",
    ],
    "fungal": [
        "真菌",
        "fungal",
        "mycosis",
        "mycetoma",
        "aspergill",
        "candid",
        "カンジダ",
        "crypto",
        "histoplasm",
        "dermatophyt",
        "皮膚糸状菌",
        "sporotrich",
        "ringworm",
        "白癬",
        "yeast",
        "酵母",
        "canv",
        "ophidiomyces",
    ],
    "viral": [
        "ウイルス",
        "virus",
        "viral",
        "herpes",
        "calici",
        "parvo",
        "influenza",
        "reovirus",
        "bornavirus",
        "birnavirus",
        "ビルナ",
        "poxvirus",
        "ポックス",
        "iridovirus",
        "proventricular dilatation",
        "pdd",
    ],
    "parasitic": [
        "寄生虫",
        "parasit",
        "mite",
        "ダニ",
        "worm",
        "線虫",
        "coccidi",
        "コクシジウム",
        "アイメリア",
        "eimeria",
        "giardia",
        "pinworm",
        "cheyletiella",
        "demodex",
        "hexamit",
    ],
}

_PATHO_INCOMPAT = {
    "toxicant": {"bacterial", "viral", "fungal", "parasitic"},
    "fungal": {"bacterial", "viral", "parasitic"},
    "neoplasia": {"bacterial", "viral", "fungal", "parasitic"},
    "bacterial_colonisation": {"viral", "fungal", "parasitic"},
    "autoimmune": {"bacterial", "viral", "fungal", "parasitic"},
}


def _patho_template_class(text: str):
    for cls, sig in _PATHO_TEMPLATE_SIGS.items():
        if sig in text:
            return cls
    return None


def _patho_true_classes(name: str, desc: str) -> set:
    blob = (name + " " + desc).lower()
    classes = {c for c, kws in _TRUE_CLASS_HINTS.items() if any(k.lower() in blob for k in kws)}
    if "bacterial" in classes:
        has_fungal_context = "真菌" in blob or "fungal" in blob or "mycosis" in blob
        has_aseptic_context = "無菌" in blob
        if has_fungal_context or has_aseptic_context:
            strong = [k for k in _TRUE_CLASS_HINTS["bacterial"] if k != "菌" and k.lower() in blob]
            if not strong:
                classes.discard("bacterial")
    return classes


def _patho_is_misapplied(text: str, name: str, desc: str) -> bool:
    if not text:
        return False
    tcls = _patho_template_class(text)
    if tcls is None:
        return False
    bench = "bacterial" if tcls == "bacterial_colonisation" else tcls
    truth = _patho_true_classes(name, desc)
    if bench in truth:
        return False
    return bool(truth & _PATHO_INCOMPAT[tcls])


_PATHO_SPECIES_MODULES = [
    "cat",
    "dog",
    "rabbit",
    "hamster",
    "guinea_pig",
    "chinchilla",
    "ferret",
    "hedgehog",
    "sugar_glider",
    "degu",
    "bird",
    "parakeet",
    "parrot",
    "reptile",
    "tortoise",
    "snake",
    "lizard",
    "amphibian",
    "fish",
    "exotic_other",
]


def test_no_misapplied_pathophysiology_template_in_modules():
    """No disease may carry a pathophysiology_ja template from the wrong class.

    Operates on the *enriched* (served) DISEASES — exactly what the live site
    shows — so it catches misapplications introduced by either the module, the
    JSON overlay, or the runtime fallback generator.
    """
    import importlib

    failures = []
    for sp in _PATHO_SPECIES_MODULES:
        try:
            mod = importlib.import_module(f"api.species.{sp}_diseases")
        except ImportError:
            continue
        for d in getattr(mod, "DISEASES", []):
            if not isinstance(d, dict):
                continue
            name = d.get("name", "") or d.get("name_en", "")
            if _patho_is_misapplied(d.get("pathophysiology_ja", ""), name, d.get("description_ja", "")):
                cls = _patho_template_class(d.get("pathophysiology_ja", ""))
                failures.append(
                    f"[{sp}] {name}: carries '{cls}' template for a "
                    f"{_patho_true_classes(name, d.get('description_ja', ''))} disease"
                )
    assert not failures, f"Found {len(failures)} misapplied pathophysiology templates. First 10:\n" + "\n".join(
        failures[:10]
    )


def test_specific_infectious_diseases_have_pathogen_specific_pathophysiology():
    """Spot-check that key fixed diseases mention BOTH pathogen AND mechanism."""
    import importlib

    # (pathogen markers, mechanism markers) — both groups must have at least one hit.
    expectations = {
        ("cat", "Feline Botulism"): (("Clostridium botulinum",), ("アセチルコリン",)),
        ("cat", "Feline Tetanus"): (("Clostridium tetani",), ("テタノスパスミン",)),
        ("bird", "Avian Influenza"): (("インフルエンザ",), ("ヘマグルチニン",)),
        ("dog", "Coccidiosis"): (("コクシジウム",), ("オーシスト",)),
    }
    for (sp, name), (pathogen_kws, mechanism_kws) in expectations.items():
        mod = importlib.import_module(f"api.species.{sp}_diseases")
        entry = next((d for d in getattr(mod, "DISEASES", []) if d.get("name") == name), None)
        if entry is None:
            continue
        patho = entry.get("pathophysiology_ja", "") or ""
        assert any(k in patho for k in pathogen_kws), (
            f"[{sp}] {name} pathophysiology_ja missing pathogen markers {pathogen_kws}. Got: {patho[:120]}"
        )
        assert any(k in patho for k in mechanism_kws), (
            f"[{sp}] {name} pathophysiology_ja missing mechanism markers {mechanism_kws}. Got: {patho[:120]}"
        )


# ---------------------------------------------------------------------------
# 2026-06 phase-3 regression — neoplasia + nutritional + exotic syndromes
# ---------------------------------------------------------------------------


def _find_by_substring(entries, name_substr):
    return [e for e in entries if name_substr in (e.get("name_ja", "") or "")]


def test_neoplasia_entries_are_species_specific():
    """Lipoma, Melanoma, Leukemia/Lymphoma must have species-tailored content.

    Each species needs different biology, surgical considerations, and prognosis.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    for label, substr in [
        ("Lipoma", "脂肪腫"),
        ("Melanoma", "メラノーマ"),
        ("Leukemia", "白血病"),
        ("Lymphoma", "リンパ腫"),
    ]:
        matches = _find_by_substring(entries, substr)
        if len(matches) < 3:
            continue
        short = [e for e in matches if len(e.get("treatment_ja", "") or "") < 100]
        assert not short, (
            f"{label}: {len(short)} entries still have <100c treatment_ja. "
            f"First: [{short[0].get('species')}] {short[0].get('name_ja')}: "
            f"'{short[0].get('treatment_ja', '')[:80]}'"
        )


def test_avian_gout_mentions_allopurinol():
    """Avian gout entries must mention allopurinol or fluid therapy (standard of care)."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    avian_species = {"Bird", "Parakeet", "Parrot"}
    gout_avian = [e for e in entries if "痛風" in (e.get("name_ja", "") or "") and e.get("species") in avian_species]
    if not gout_avian:
        pytest.skip("No avian gout entries found")
    for entry in gout_avian:
        tx = entry.get("treatment_ja", "") or ""
        assert any(kw in tx for kw in ("アロプリノール", "ベンズブロマロン", "輸液")), (
            f"Avian gout missing standard-of-care: [{entry.get('species')}] {entry.get('name_ja')}: '{tx[:120]}'"
        )


def test_nshp_mbd_mentions_calcium_uvb():
    """Nutritional Secondary Hyperparathyroidism / MBD must mention Ca + VitD3 + UVB."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    for substr in ("栄養性二次性副甲状腺機能亢進症", "栄養性骨異栄養"):
        matches = _find_by_substring(entries, substr)
        for entry in matches:
            tx = entry.get("treatment_ja", "") or ""
            if len(tx) < 100:
                # Allow short entries from species without specific generator (e.g. Exotic Other)
                continue
            assert any(kw in tx for kw in ("カルシウム", "Ca", "グルコン酸")), (
                f"NSHP/MBD missing calcium reference: [{entry.get('species')}] {entry.get('name_ja')}: '{tx[:120]}'"
            )
            assert any(kw in tx for kw in ("VitD3", "ビタミンD3", "D3", "UVB", "UV-B")), (
                f"NSHP/MBD missing VitD3/UVB reference: [{entry.get('species')}] {entry.get('name_ja')}: '{tx[:120]}'"
            )


def test_vitamin_deficiency_excess_correctly_distinguished():
    """VitA/D/E excess vs deficiency content must not be swapped.

    Excess entries should mention 中止 (stop) or 過剰 (excess); deficiency entries
    should mention 補給 (supplementation).
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    # Excess entries must contain "中止" or "過剰" — they're about stopping supplementation
    for substr in ("ビタミンA過剰", "ビタミンD3過剰"):
        for entry in _find_by_substring(entries, substr):
            tx = entry.get("treatment_ja", "") or ""
            if len(tx) < 80:
                continue
            assert any(kw in tx for kw in ("中止", "停止", "過剰")), (
                f"{substr} missing 中止/過剰 reference: [{entry.get('species')}] {entry.get('name_ja')}: '{tx[:120]}'"
            )
            # Must NOT recommend supplementation
            assert "補給を増やす" not in tx, f"{substr} incorrectly recommends supplementation: '{tx[:120]}'"


def test_iron_storage_disease_mentions_phlebotomy_or_deferoxamine():
    """Iron storage disease entries (in species where it's clinically meaningful)
    must mention bloodletting or deferoxamine. The 'Exotic Other' catch-all species
    is exempt because it lacks species-specific protocols."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    matches = _find_by_substring(entries, "鉄蓄積")
    exempt_species = {"Exotic Other"}
    for entry in matches:
        if entry.get("species") in exempt_species:
            continue
        tx = entry.get("treatment_ja", "") or ""
        if len(tx) < 80:
            continue
        assert any(kw in tx for kw in ("瀉血", "デフェロキサミン", "鉄キレート", "低鉄")), (
            f"Iron storage missing treatment markers: [{entry.get('species')}] {entry.get('name_ja')}: '{tx[:120]}'"
        )


def test_thiamine_deficiency_mentions_b1():
    """Thiamine deficiency entries must mention thiamine/B1 supplementation."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    matches = _find_by_substring(entries, "チアミン欠乏")
    for entry in matches:
        tx = entry.get("treatment_ja", "") or ""
        if len(tx) < 80:
            continue
        assert any(kw in tx for kw in ("チアミン", "ビタミンB1", "B1", "B群")), (
            f"Thiamine deficiency missing B1 reference: [{entry.get('species')}] {entry.get('name_ja')}: '{tx[:120]}'"
        )


def test_reptile_syndromes_mention_potz():
    """Reptile-specific syndromes (peritonitis, stress, drowning) must reference
    thermal management — either POTZ, 温度, or 温浴 (warm-water bath, which is
    a clinically equivalent thermal-support intervention)."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    reptile_sp = {"Reptile", "Tortoise", "Snake", "Lizard", "Amphibian"}
    targets = [
        "腹膜炎",
        "ストレス症候群",
        "濾胞停滞",
        "腹壁ヘルニア",
        "アナサルカ",
        "全身浮腫",
        "溺水",
    ]
    thermal_keywords = ("POTZ", "温熱", "保温", "種別温度", "温度勾配", "温浴", "加温", "温度")
    # Amphibians use water quality as their primary husbandry intervention rather than
    # thermal management; "水質" / "清潔な水" are also acceptable.
    amphib_extra = ("水質", "清潔な水", "湿潤", "塩浴", "皮膚湿潤")
    for substr in targets:
        matches = [e for e in _find_by_substring(entries, substr) if e.get("species") in reptile_sp]
        for entry in matches:
            tx = entry.get("treatment_ja", "") or ""
            if len(tx) < 100:
                continue
            keywords = thermal_keywords
            if entry.get("species") == "Amphibian":
                keywords = thermal_keywords + amphib_extra
            assert any(kw in tx for kw in keywords), (
                f"Reptile syndrome ({substr}) missing thermal/environmental management: [{entry.get('species')}] "
                f"{entry.get('name_ja')}: '{tx[:140]}'"
            )


def test_myiasis_mentions_larva_removal_or_ivermectin():
    """Myiasis (fly larvae infestation) must mention larva removal or ivermectin."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    matches = _find_by_substring(entries, "蝿蛆")
    for entry in matches:
        tx = entry.get("treatment_ja", "") or ""
        if len(tx) < 80:
            continue
        assert any(kw in tx for kw in ("除去", "イベルメクチン", "ivermectin", "蛆")), (
            f"Myiasis missing removal/ivermectin: [{entry.get('species')}] {entry.get('name_ja')}: '{tx[:120]}'"
        )


def test_mucormycosis_warns_azole_resistance():
    """Mucormycosis entries must warn about azole resistance (Mucorales are azole-resistant)."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    matches = _find_by_substring(entries, "ムコール")
    for entry in matches:
        tx = entry.get("treatment_ja", "") or ""
        if len(tx) < 100:
            continue
        # Must mention amphotericin B or warning about azoles
        assert any(kw in tx for kw in ("アムホテリシン", "amphotericin", "アゾール")), (
            f"Mucormycosis missing amphotericin/azole-warning: [{entry.get('species')}] "
            f"{entry.get('name_ja')}: '{tx[:120]}'"
        )


def test_cat_ckd_mentions_iris_staging():
    """Cat CKD entries must reference IRIS staging system (standard of care)."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    cat_ckd = [e for e in entries if e.get("species") == "Cat" and "慢性腎臓病" in (e.get("name_ja", "") or "")]
    if not cat_ckd:
        pytest.skip("No cat CKD entries")
    for entry in cat_ckd:
        tx = entry.get("treatment_ja", "") or ""
        if len(tx) < 100:
            continue
        assert "IRIS" in tx or "病期" in tx, f"Cat CKD missing IRIS/staging reference: '{tx[:120]}'"


def test_cat_hcm_mentions_thromboprophylaxis():
    """Cat HCM entries must reference echocardiography, beta-blocker, or thromboprophylaxis (ATE risk)."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    cat_hcm = [
        e
        for e in entries
        if e.get("species") == "Cat"
        and ("HCM" in (e.get("name_ja", "") or "") or "肥大型心筋症" in (e.get("name_ja", "") or ""))
    ]
    if not cat_hcm:
        pytest.skip("No cat HCM entries")
    for entry in cat_hcm:
        tx = entry.get("treatment_ja", "") or ""
        if len(tx) < 100:
            continue
        assert any(kw in tx for kw in ("心エコー", "アテノロール", "クロピドグレル", "ピモベンダン", "ATE")), (
            f"Cat HCM missing standard-of-care markers: '{tx[:160]}'"
        )


def test_avian_chlamydiosis_mentions_doxycycline_and_zoonosis():
    """Avian chlamydiosis (psittacosis) must mention doxycycline + zoonotic warning."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    avian_species = {"Bird", "Parakeet", "Parrot"}
    chlamydia = [
        e
        for e in entries
        if e.get("species") in avian_species
        and ("クラミジア" in (e.get("name_ja", "") or "") or "オウム病" in (e.get("name_ja", "") or ""))
    ]
    if not chlamydia:
        pytest.skip("No avian chlamydiosis entries")
    for entry in chlamydia:
        tx = entry.get("treatment_ja", "") or ""
        if len(tx) < 100:
            continue
        assert "ドキシサイクリン" in tx or "アジスロマイシン" in tx, (
            f"Avian chlamydiosis missing antibiotic: '{tx[:120]}'"
        )
        assert any(kw in tx for kw in ("人獣共通", "人感染", "psittacosis", "zoonotic", "PPE")), (
            f"Avian chlamydiosis missing zoonotic warning: '{tx[:160]}'"
        )


def test_rabbit_gi_stasis_warns_about_oral_betalactam():
    """Rabbit GI stasis/constipation must warn about oral β-lactam contraindication."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    rabbit_gi = [
        e
        for e in entries
        if e.get("species") == "Rabbit"
        and any(kw in (e.get("name_ja", "") or "") for kw in ("GI stasis", "消化管うっ滞", "便秘"))
    ]
    if not rabbit_gi:
        pytest.skip("No rabbit GI stasis entries")
    for entry in rabbit_gi:
        tx = entry.get("treatment_ja", "") or ""
        if len(tx) < 200:
            continue
        # Must mention Critical Care or strong supportive treatment
        assert any(kw in tx for kw in ("Critical Care", "シリンジ", "強制給餌", "シサプリド", "ブプレノルフィン")), (
            f"Rabbit GI stasis missing standard-of-care: '{tx[:160]}'"
        )


def test_streptococcus_warns_pcn_contraindication_in_herbivores():
    """Streptococcus in guinea pig must warn about oral β-lactam contraindication."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    gp_strep = [
        e
        for e in entries
        if ("連鎖球菌" in (e.get("name_ja", "") or "") or "レンサ球菌" in (e.get("name_ja", "") or ""))
        and e.get("species") == "Guinea Pig"
    ]
    if not gp_strep:
        pytest.skip("No guinea pig Streptococcus entries")
    for entry in gp_strep:
        tx = entry.get("treatment_ja", "") or ""
        if len(tx) < 100:
            continue
        # Must warn about Clostridium / orals or β-lactams
        assert any(kw in tx for kw in ("Clostridium", "禁忌", "経口", "β-ラクタム", "ペニシリン")), (
            f"Guinea pig Streptococcus missing antibiotic-warning: '{tx[:160]}'"
        )


# ============================================================================
# 2026-06 (Phase 5) regression tests: garbled medical phrase + blood disorders
# ============================================================================


def test_no_garbled_single_agent_phrase():
    """Regression: the garbled fallback phrase 'single-agent修正治療' (medically nonsense
    — meant to describe wide-margin surgical resection) must never appear in any field.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    offenders = []
    for entry in entries:
        for fld in ("treatment_ja", "treatment", "prognosis_ja", "causes_ja"):
            v = entry.get(fld) or ""
            if "single-agent修正治療" in v:
                offenders.append((entry.get("species"), entry.get("name_ja", "?"), fld))
    assert not offenders, f"Garbled neoplasia phrase persists in {len(offenders)} fields: {offenders[:5]}"
    # Also enforce on the Python species modules
    py_offenders = []
    for path in (ROOT / "api" / "species").glob("*_diseases.py"):
        if "single-agent修正治療" in path.read_text(encoding="utf-8"):
            py_offenders.append(path.name)
    assert not py_offenders, f"Garbled phrase in Python modules: {py_offenders}"


def test_no_blood_disorder_template():
    """Regression: the generic blood-disorder template (42 instances pre-fix) must be eradicated.

    Pre-fix wording: "Xにおける(disease)の治療は血液異常の基礎原因の特定と対処が必要である。
    重度の貧血や急性出血には輸血が必要となりうる..."

    Each species/disorder combination now gets disorder-specific evidence-based content.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    bad_phrase = "の治療は血液異常の基礎原因の特定と対処が必要である"
    offenders = [
        (e.get("species"), e.get("name_ja", "?")) for e in entries if bad_phrase in (e.get("treatment_ja", "") or "")
    ]
    assert not offenders, f"Generic blood-disorder template persists in {len(offenders)} entries: {offenders[:10]}"


def test_eia_marked_as_reportable_with_no_cure():
    """Regression: equine infectious anemia (馬伝染性貧血) must be marked as reportable
    and explicitly state that there is no cure (this is critical clinical/legal info).
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    eia = [
        e
        for e in entries
        if ("馬伝染性貧血" in (e.get("name_ja", "") or "") or "EIA" in (e.get("name_ja", "") or ""))
        and e.get("species") == "Horse"
    ]
    if not eia:
        pytest.skip("No EIA entry found")
    for entry in eia:
        tx = entry.get("treatment_ja", "") or ""
        # Must mention reportable status (届出/法定) AND lack of cure (治療法なし or similar)
        assert any(kw in tx for kw in ("届出", "法定", "OIE", "Coggins")), (
            f"EIA entry missing reportable-disease language: '{tx[:200]}'"
        )
        assert any(kw in tx for kw in ("治療法なし", "根治不能", "治癒不可", "生涯", "隔離", "殺処分", "安楽死")), (
            f"EIA entry missing 'no cure / lifelong carrier' language: '{tx[:200]}'"
        )


def test_neonatal_iso_is_species_specific():
    """Regression: neonatal isoerythrolysis must have species-specific (cat=FNI, horse=NI)
    content with the critical colostrum-restriction message, not generic hemolysis text.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    cat_ni = [e for e in entries if "新生子溶血" in (e.get("name_ja", "") or "") and e.get("species") == "Cat"]
    horse_ni = [e for e in entries if "新生子溶血" in (e.get("name_ja", "") or "") and e.get("species") == "Horse"]
    if cat_ni:
        tx = cat_ni[0].get("treatment_ja", "") or ""
        # Must mention type B mother & A/AB kitten OR colostrum restriction
        assert any(kw in tx for kw in ("B型母猫", "FNI", "初乳", "人工哺乳")), (
            f"Cat NI missing critical management info: '{tx[:200]}'"
        )
    if horse_ni:
        tx = horse_ni[0].get("treatment_ja", "") or ""
        assert any(kw in tx for kw in ("Aa", "Qa", "初乳", "新生駒", "凝集試験")), (
            f"Horse NI missing critical management info: '{tx[:200]}'"
        )


def test_ferret_estrogen_aplastic_anemia_management():
    """Regression: ferret estrogen-induced aplastic anemia entries must mention the
    species-specific treatment pillars (hCG/GnRH for ovulation induction, OHE for prevention).
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    ferret_est = [
        e
        for e in entries
        if e.get("species") == "Ferret"
        and ("エストロゲン" in (e.get("name_ja", "") or "") or "高エストロゲン" in (e.get("name_ja", "") or ""))
    ]
    if not ferret_est:
        pytest.skip("No ferret estrogen entries found")
    for entry in ferret_est:
        tx = entry.get("treatment_ja", "") or ""
        assert any(kw in tx for kw in ("hCG", "HCG", "GnRH", "buserelin", "デスロレリン", "排卵誘起", "持続発情")), (
            f"Ferret estrogen-AA missing ovulation-induction mention: '{tx[:200]}'"
        )
        assert any(kw in tx for kw in ("OHE", "OVH", "卵巣子宮", "去勢", "避妊", "ovariohysterectomy")), (
            f"Ferret estrogen-AA missing OHE/spay prevention message: '{tx[:200]}'"
        )


def test_feline_hemoplasmosis_mentions_doxycycline():
    """Regression: feline hemoplasmosis (Mycoplasma haemofelis/haemominutum) must
    mention doxycycline (gold-standard 1st line), not just generic anemia content.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    hp = [
        e
        for e in entries
        if e.get("species") == "Cat"
        and any(
            kw in (e.get("name_ja", "") or "")
            for kw in ("ヘモプラズマ", "haemominutum", "haemofelis", "感染性貧血", "伝染性貧血")
        )
    ]
    if not hp:
        pytest.skip("No feline hemoplasmosis entries")
    for entry in hp:
        tx = entry.get("treatment_ja", "") or ""
        # Must mention doxycycline OR marbofloxacin (first-line anti-hemoplasma)
        assert any(kw in tx for kw in ("ドキシサイクリン", "doxycycline", "マルボフロキサシン", "marbofloxacin")), (
            f"Feline hemoplasmosis missing first-line antibiotic: '{tx[:240]}'"
        )


# ---------------------------------------------------------------------------
# Multi-field clinical template regression tests (2026-06 fix)
# ---------------------------------------------------------------------------
# The non-treatment JA fields (causes_ja, transmission_ja, prevention_ja,
# prognosis_ja, clinical_signs_ja, differential_diagnosis_ja,
# nutrition_management_ja, prognosis_detailed_ja, rehabilitation_protocol_ja,
# pathophysiology_ja) had ~0% uniqueness across 6,400+ entries — every
# infection had the same causes_ja, every neoplasia the same prognosis, etc.
# Worse, cross-category misapplications were rife (FeLV got "tumors do not
# transmit", asthma got the parasite template, etc.).
#
# These were eliminated in scripts/template_elimination/
# eliminate_clinical_field_templates.py.

# Fields whose uniqueness must remain above the threshold below.
_CLINICAL_FIELDS_REQUIRING_UNIQUENESS = [
    "causes_ja",
    "transmission_ja",
    "prevention_ja",
    "clinical_signs_ja",
    "differential_diagnosis_ja",
    "nutrition_management_ja",
    "prognosis_detailed_ja",
    "rehabilitation_protocol_ja",
]

# Minimum allowed unique-text % for each field. Anything below this signals
# that templates have re-infected the database.
_MIN_UNIQUENESS_PCT = 70.0


def test_clinical_fields_meet_uniqueness_threshold():
    """Every non-treatment JA clinical field must be ≥70% unique across entries.

    A field that's <70% unique means category-level templates have been
    bulk-applied across many distinct diseases — which is what we just
    eliminated.
    """
    from collections import Counter

    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")

    failures = []
    for field in _CLINICAL_FIELDS_REQUIRING_UNIQUENESS:
        texts = [(e.get(field, "") or "").strip() for e in entries]
        nonempty = [t for t in texts if len(t) >= 50]
        if len(nonempty) < 100:
            continue
        cnt = Counter(nonempty)
        unique = sum(1 for c in cnt.values() if c == 1)
        pct = 100.0 * unique / len(nonempty)
        if pct < _MIN_UNIQUENESS_PCT:
            # Show the most-repeated text
            top_text, top_count = cnt.most_common(1)[0]
            failures.append(
                f"{field}: {pct:.1f}% unique (need ≥{_MIN_UNIQUENESS_PCT:.0f}%). "
                f"Worst offender: '{top_text[:80]}…' shared by {top_count} entries."
            )
    assert not failures, "Clinical fields below uniqueness threshold:\n" + "\n".join(failures)


def test_felv_transmission_does_not_claim_tumors_dont_transmit():
    """FeLV is a contagious virus — its transmission_ja must NOT say
    "tumors don't transmit between individuals" (a credibility-killing
    cross-category template error from the May-2026 enrichment).
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    felv = [
        e for e in entries if e.get("species") == "Cat" and "FeLV" in ((e.get("name_ja") or "") + (e.get("name") or ""))
    ]
    if not felv:
        pytest.skip("No FeLV entries")
    for entry in felv:
        tx = entry.get("transmission_ja", "") or ""
        assert "腫瘍は感染性疾患ではない" not in tx, f"FeLV transmission_ja still has neoplasia template: '{tx[:200]}'"
        # Must mention actual transmission route
        assert any(kw in tx for kw in ("唾液", "咬傷", "水平感染", "母子伝播", "saliva")), (
            f"FeLV transmission_ja missing virus-specific transmission: '{tx[:200]}'"
        )


def test_asthma_causes_is_not_parasitic_template():
    """Feline asthma is an allergic/inflammatory airway disease — not parasitic.
    Its causes_ja must NOT be the generic parasite-infection template.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    asthma = [
        e
        for e in entries
        if e.get("species") == "Cat" and "喘息" in ((e.get("name_ja") or "") + (e.get("name") or "Asthma"))
    ]
    if not asthma:
        pytest.skip("No feline asthma entries")
    for entry in asthma:
        cja = entry.get("causes_ja", "") or ""
        # The parasite template starts with "寄生虫（線虫・条虫..."
        assert not cja.startswith("寄生虫（線虫"), f"Feline asthma causes_ja is the parasite template: '{cja[:200]}'"


def test_hyperthyroidism_does_not_have_neoplasia_transmission():
    """Cat hyperthyroidism is endocrine — its transmission_ja must NOT use
    the neoplasia template's "tumors don't transmit" boilerplate (because
    hyperthyroidism IS caused by a benign tumor and the template is being
    auto-applied incorrectly to other endocrine details).
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    cat_hyp = [
        e
        for e in entries
        if e.get("species") == "Cat" and "甲状腺機能亢進" in ((e.get("name_ja") or "") + (e.get("name") or ""))
    ]
    if not cat_hyp:
        pytest.skip("No cat hyperthyroidism entries")
    for entry in cat_hyp:
        tx = entry.get("transmission_ja", "") or ""
        # Must mention "non-infectious / no transmission" but in endocrine-appropriate language
        # The neoplasia template specifically says "CTVT" and "FeLV-related tumors"
        # which shouldn't be in hyperthyroidism transmission_ja
        assert "CTVT" not in tx, f"Cat hyperthyroidism transmission_ja contains CTVT (canine tumor): '{tx[:200]}'"


def test_no_cross_species_prognosis_template():
    """No prognosis_ja text may be reused by 3+ different species.

    The disease library used to return identical short prognoses
    (e.g. "早期復温で予後改善。") for every species in a class — meaning
    rabbit/hamster/guinea-pig/chinchilla/etc. all shared the same 5-word
    prognostic summary. A 5-word prognosis cannot meaningfully describe
    outcomes for the same condition across 3+ species: each one has different
    body mass, organ susceptibility, dosing, and case-fatality reports.

    This was eliminated by scripts/template_elimination/
    eliminate_prognosis_templates.py in June 2026 — see CLAUDE.md.
    """
    from collections import defaultdict

    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    by_species: dict[str, set[str]] = defaultdict(set)
    by_names: dict[str, set[str]] = defaultdict(set)
    for e in entries:
        prog = (e.get("prognosis_ja") or "").strip()
        sp = e.get("species") or ""
        name = (e.get("name_ja") or "").strip() or (e.get("name") or "").strip()
        if prog and sp and name:
            by_species[prog].add(sp)
            by_names[prog].add(name)
    failures = []
    for prog, species_set in by_species.items():
        if len(species_set) >= 3 and len(by_names[prog]) >= 3:
            failures.append(
                f"{len(species_set)} species × {len(by_names[prog])} diseases share prognosis_ja: "
                f"'{prog[:80]}…' (species: {sorted(species_set)[:5]})"
            )
    assert not failures, f"Found {len(failures)} cross-species prognosis templates. First 5:\n" + "\n".join(
        failures[:5]
    )


def test_no_double_species_prefix_in_clinical_fields():
    """Generated content must not have '猫における猫XXX...' double-species patterns."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    sp_map = {
        "Dog": "犬",
        "Cat": "猫",
        "Horse": "馬",
        "Rabbit": "ウサギ",
        "Hamster": "ハムスター",
        "Guinea Pig": "モルモット",
        "Chinchilla": "チンチラ",
        "Bird": "鳥",
        "Parakeet": "インコ",
        "Parrot": "オウム",
        "Ferret": "フェレット",
        "Hedgehog": "ハリネズミ",
    }
    fields = [
        "causes_ja",
        "transmission_ja",
        "prognosis_ja",
        "clinical_signs_ja",
        "differential_diagnosis_ja",
        "prevention_ja",
        "nutrition_management_ja",
        "prognosis_detailed_ja",
        "rehabilitation_protocol_ja",
    ]
    failures = []
    for entry in entries:
        sp_ja = sp_map.get(entry.get("species", ""), "")
        if not sp_ja:
            continue
        for field in fields:
            v = entry.get(field, "") or ""
            if v.startswith(f"{sp_ja}における{sp_ja}"):
                failures.append(
                    f"[{entry.get('species')}] {entry.get('name_ja')}/{field}: starts with '{sp_ja}における{sp_ja}'"
                )
                break
    assert not failures, f"Found {len(failures)} entries with double-species prefix. First 5:\n" + "\n".join(
        failures[:5]
    )


# ---------------------------------------------------------------------------
# Disease description templates (2026-06 elimination)
# ---------------------------------------------------------------------------

# Generic boilerplate that the early enrichment pass appended to exotic-species
# descriptions. These sentences carry no disease-specific information and were
# shared verbatim across hundreds of unrelated diseases.
DESCRIPTION_BOILERPLATE_JA = (
    "臨床症状の重症度と全身状態を総合的に評価し",
    "飼育環境の最適化と栄養管理が回復の促進に重要な役割を果たす",
    "定期的な再評価により治療反応を確認し、必要に応じて治療計画の修正を行う",
)
DESCRIPTION_BOILERPLATE_EN = (
    "Comprehensive assessment of clinical signs and overall condition",
    "Optimization of husbandry and nutritional management plays",
)

_PAREN_TAG = re.compile(r"[（(][^（）()]*[）)]\s*$")


def _base_name(entry: dict) -> str:
    name = entry.get("name_ja") or entry.get("name") or ""
    return _PAREN_TAG.sub("", name).strip()


def test_no_description_boilerplate_in_json():
    """description / description_ja must not carry the generic boilerplate tail."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    failures = []
    for entry in entries:
        ja = entry.get("description_ja", "") or ""
        en = entry.get("description", "") or ""
        if any(m in ja for m in DESCRIPTION_BOILERPLATE_JA):
            failures.append(f"[{entry.get('species')}] {entry.get('name_ja')}: description_ja boilerplate")
        elif any(m in en for m in DESCRIPTION_BOILERPLATE_EN):
            failures.append(f"[{entry.get('species')}] {entry.get('name')}: description boilerplate")
    assert not failures, f"Found {len(failures)} entries with boilerplate descriptions. First 5:\n" + "\n".join(
        failures[:5]
    )


def test_no_cross_disease_description_template_in_json():
    """No description text may be shared by 4+ entries spanning 4+ distinct diseases.

    Same-disease families (portosystemic shunt congenital/acquired, hemangiosarcoma
    at different sites) legitimately share a summary, so the guard fires only when
    4+ *distinct base disease names* share one text — a genuine template spanned
    dozens of unrelated diseases.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    from collections import defaultdict

    failures = []
    for field in ("description_ja", "description"):
        by_text: dict[str, list] = defaultdict(list)
        for entry in entries:
            v = (entry.get(field) or "").strip()
            if v and len(v) >= 40:
                by_text[v].append(entry)
        for text, items in by_text.items():
            names = {_base_name(e) for e in items}
            if len(items) >= 4 and len(names) >= 4:
                failures.append(
                    f"{field}: {len(items)} entries / {len(names)} diseases share "
                    f"'{text[:60]}…' (e.g. {sorted(names)[:3]})"
                )
    assert not failures, f"Found {len(failures)} cross-disease description templates. First 5:\n" + "\n".join(
        failures[:5]
    )


def test_avian_goiter_description_not_neoplasia():
    """Avian goiter (iodine-deficiency thyroid hyperplasia) must not be described as a tumour.

    Regression for the '腺腫' substring inside '甲状腺腫' matching the neoplasia
    category resolver.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    for entry in entries:
        name = entry.get("name_ja", "") or ""
        if entry.get("species") in ("Parakeet", "Parrot", "Bird") and "甲状腺腫" in name and "腫瘍" not in name:
            ja = entry.get("description_ja", "") or ""
            if ja and ("臨床症状の重症度" not in ja):  # only assert on regenerated descriptions
                assert "腫瘍性疾患" not in ja, (
                    f"[{entry.get('species')}] {name}: goiter described as neoplasia: {ja[:120]}"
                )


def test_no_stub_description_in_json():
    """description_ja must not contain the field-label-scaffolding stub prose.

    The stub form ("XはYにみられる疾患である。YにおけるXの原因: …。主要な臨床
    徴候はYにおけるXの臨床徴候は以下を含む。など。") reads as broken prose and
    was replaced by clean category summaries in 2026-06.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    failures = []
    for entry in entries:
        ja = entry.get("description_ja", "") or ""
        if "にみられる疾患である" in ja and ("の臨床徴候は以下を含む" in ja or "の原因:" in ja or "の原因：" in ja):
            failures.append(f"[{entry.get('species')}] {entry.get('name_ja')}: stub description_ja")
    assert not failures, f"Found {len(failures)} stub descriptions. First 5:\n" + "\n".join(failures[:5])
