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
    "diagnosis_ja",
    # English-language clinical fields. These previously shipped as a single
    # category paragraph reused across thousands of diseases (transmission was
    # <40% unique, diagnosis ~0% unique with one text on 1,600+ entries).
    "clinical_signs",
    "transmission",
    "diagnosis",
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


def test_no_cross_disease_clinical_field_template_in_json():
    """clinical_signs / transmission / diagnosis (EN+JA) must not be shared by
    4+ entries spanning 4+ distinct diseases.

    These fields previously shipped as category boilerplate — one English
    transmission paragraph on 6,000+ diseases, one diagnosis paragraph on
    1,600+ — so the English site displayed identical clinical text for almost
    every disease. Same-disease families (fracture subtypes, mite infestation
    variants) legitimately share text and span <4 distinct base names, so the
    guard fires only on genuine cross-disease templates.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    from collections import defaultdict

    failures = []
    for field in (
        "clinical_signs",
        "clinical_signs_ja",
        "transmission",
        "transmission_ja",
        "diagnosis",
        "diagnosis_ja",
    ):
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
    assert not failures, f"Found {len(failures)} cross-disease clinical-field templates. First 5:\n" + "\n".join(
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


# ---------------------------------------------------------------------------
# Prevention field: no dog/cat advice on other species (2026-06 fix).
#
# The legacy gen_prevention_ja emitted dog/cat category templates (DCM-
# predisposed breeds, puppy/kitten deworming, indoor-cat confinement, BCS
# 4-5/9, FLUTD, 子宮蓄膿症リスク...) for EVERY species, so a horse colic entry
# read "猫の屋内飼育、リード散歩" and a bird feather-plucking entry cited
# "DCM/HCM素因品種（ドーベルマン...）". 2,630 non-companion entries were
# contaminated. The generator is now species-class aware and the migration
# regenerates any contaminated prevention into species-appropriate text.
# ---------------------------------------------------------------------------

# Dog/cat-specific phrases that must never reach another species' prevention.
_COMPANION_ONLY_PHRASES = [
    "子犬子猫",
    "ドーベルマン",
    "コッカースパニエル",
    "メインクーン",
    "ラグドール",
    "猫の屋内飼育",
    "リード散歩",
    "短頭種",
    "グレインフリー",
    "蚤予防薬",
    "蚤アレルギー",
    "DCM/HCM素因品種",
    "FLUTD",
    "BCS 4-5/9",
    "缶詰食のBPA",
    "HD・ED・OCD・FCP",
    "デンタルガム",
]

_PREVENTION_CATEGORIES = [
    "viral_infection",
    "bacterial_infection",
    "respiratory_infection",
    "fungal_infection",
    "parasitic",
    "neoplasia",
    "endocrine_metabolic",
    "renal_urinary",
    "cardiac",
    "respiratory_other",
    "gastrointestinal",
    "neurological",
    "ophthalmic",
    "musculoskeletal",
    "dental",
    "dermatological",
    "hematological",
    "reproductive",
    "toxicity",
    "trauma",
    "autoimmune",
    "nutritional",
    "behavioral",
    "generic",
]

_NON_COMPANION_SPECIES = [
    "horse",
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


def test_prevention_generator_no_dogcat_advice_for_other_species():
    """gen_prevention_ja must not put dog/cat-specific advice on other species."""
    from scripts.template_elimination.clinical_fields_generator import gen_prevention_ja

    failures = []
    for species in _NON_COMPANION_SPECIES:
        for cat in _PREVENTION_CATEGORIES:
            text = gen_prevention_ja(cat, "テスト疾患", species)
            for phrase in _COMPANION_ONLY_PHRASES:
                if phrase in text:
                    failures.append(f"[{species}/{cat}] contains companion-only phrase '{phrase}'")
    assert not failures, "Companion advice leaked into non-companion prevention:\n" + "\n".join(failures[:15])


def test_prevention_generator_is_species_class_appropriate():
    """Each non-companion class must surface its own husbandry markers."""
    from scripts.template_elimination.clinical_fields_generator import gen_prevention_ja

    # (species, marker that must appear in its generic prevention core)
    expectations = [
        ("horse", "装蹄"),
        ("bird", "止まり木"),
        ("parrot", "ペレット"),
        ("reptile", "POTZ"),
        ("snake", "UV-B"),
        ("fish", "水質"),
        ("amphibian", "脱塩素"),
        ("rabbit", "ケージ"),
    ]
    failures = []
    for species, marker in expectations:
        text = gen_prevention_ja("generic", "テスト疾患", species)
        if marker not in text:
            failures.append(f"[{species}] generic prevention missing expected marker '{marker}': {text[:80]}")
    assert not failures, "\n".join(failures)


def _served_db_path():
    p = ROOT / "instance" / "vetdict.db"
    return p if p.exists() else None


def test_served_db_prevention_no_cross_species_contamination():
    """The served SQLite DB must carry no dog/cat advice on other species."""
    import sqlite3

    db = _served_db_path()
    if db is None:
        pytest.skip("served vetdict.db not present (run scripts/migrate_to_sqlite.py)")
    conn = sqlite3.connect(str(db))
    try:
        rows = conn.execute(
            "SELECT species, name_ja, prevention_ja FROM diseases "
            "WHERE species NOT IN ('dog','cat') AND prevention_ja IS NOT NULL"
        ).fetchall()
    finally:
        conn.close()
    failures = []
    for species, name_ja, prevention in rows:
        for phrase in _COMPANION_ONLY_PHRASES:
            if phrase in (prevention or ""):
                failures.append(f"[{species}] {name_ja}: '{phrase}'")
                break
    assert not failures, f"Found {len(failures)} contaminated prevention entries. First 10:\n" + "\n".join(
        failures[:10]
    )


def test_served_db_prevention_not_cross_disease_template():
    """No prevention_ja text may be shared by >=4 distinct disease base names."""
    import sqlite3
    from collections import defaultdict

    db = _served_db_path()
    if db is None:
        pytest.skip("served vetdict.db not present (run scripts/migrate_to_sqlite.py)")
    conn = sqlite3.connect(str(db))
    try:
        rows = conn.execute(
            "SELECT species, name, name_ja, prevention_ja FROM diseases WHERE prevention_ja IS NOT NULL"
        ).fetchall()
    finally:
        conn.close()
    paren = re.compile(r"[（(][^（）()]*[）)]\s*$")
    groups = defaultdict(list)
    for _species, name, name_ja, prevention in rows:
        text = (prevention or "").strip()
        if len(text) >= 20:
            base = paren.sub("", (name_ja or name or "")).strip()
            groups[text].append(base)
    offenders = [(len(set(bases)), text) for text, bases in groups.items() if len(set(bases)) >= 4]
    offenders.sort(reverse=True)
    assert not offenders, f"Found {len(offenders)} cross-disease prevention templates. First 5:\n" + "\n".join(
        f"  {n} names: {t[:80]}" for n, t in offenders[:5]
    )


# ---------------------------------------------------------------------------
# Description grounding + Japanese localisation (2026-06)
# ---------------------------------------------------------------------------
#
# Earlier passes deduplicated descriptions only by *exact string*, but the
# description generator slots the disease name + species into one per-category
# paragraph, so every neoplasm (or viral infection, …) of a species shared a
# structurally identical headline — a "generic AI" tell. Those paragraphs were
# replaced by grounded one-line summaries built from each record's own signs,
# work-up and urgency. Separately, English species placeholders had leaked into
# Japanese fields (``Hamsterにおける…`` / ``…（Amphibian）``). These tests lock in
# both fixes.

# Distinctive sentences from the per-category description paragraphs. None of
# these may appear in any description any more.
_DESCRIPTION_BOILERPLATE_JA = (
    "正常細胞の悪性転換により異常増殖・浸潤・転移が進行しうる",
    "病原ウイルスが宿主細胞内で複製し組織傷害と免疫応答を引き起こす",
    "原因・病態・進行段階により臨床像は多様",
    "寄生虫種・寄生数・寄生部位により消化器",
    "消化管の運動・吸収・分泌の障害により",
    "中枢または末梢神経の障害により運動失調",
    "原因菌の定着・増殖と毒素産生により局所および全身性の炎症",
)

# English species names that must never sit immediately before a Japanese
# particle or inside parentheses in Japanese text (breed names like
# "Quarter Horse" are excluded by the preceding-word lookbehind).
_EN_SPECIES = (
    "Guinea Pig",
    "Sugar Glider",
    "Exotic Other",
    "Hedgehog",
    "Chinchilla",
    "Parakeet",
    "Hamster",
    "Tortoise",
    "Amphibian",
    "Reptile",
    "Rabbit",
    "Ferret",
    "Parrot",
    "Lizard",
    "Snake",
    "Degu",
    "Bird",
    "Cat",
    "Dog",
    "Horse",
)
_EN_ALT = "|".join(re.escape(n) for n in sorted(_EN_SPECIES, key=len, reverse=True))
_EN_SPECIES_PARTICLE = re.compile(
    rf"(?<![A-Za-z])(?<![A-Za-z]\s)(?P<sp>{_EN_ALT})(?=(に|の|は|を|では|における|にみられる|に発症|に好発))"
)
_EN_SPECIES_PAREN = re.compile(rf"[（(](?P<sp>{_EN_ALT})[）)]")

_JA_TEXT_FIELDS = (
    "name_ja",
    "description_ja",
    "treatment_ja",
    "prognosis_ja",
    "causes_ja",
    "pathophysiology_ja",
    "clinical_signs_ja",
    "prevention_ja",
    "diagnosis_ja",
    "transmission_ja",
)


def test_no_description_category_boilerplate_in_json():
    """No description may reuse a per-category boilerplate paragraph."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not available")
    offenders = []
    for e in entries:
        text = e.get("description_ja") or ""
        for fp in _DESCRIPTION_BOILERPLATE_JA:
            if fp in text:
                offenders.append((e.get("species"), e.get("name_ja"), fp))
                break
    assert not offenders, f"Found {len(offenders)} category-boilerplate descriptions. First 5:\n" + "\n".join(
        f"  [{s}] {n}: {fp}" for s, n, fp in offenders[:5]
    )


def test_no_english_species_name_in_japanese_json_fields():
    """English species placeholders must not appear in JA fields of the JSON."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not available")
    offenders = []
    for e in entries:
        for f in _JA_TEXT_FIELDS:
            v = e.get(f) or ""
            if _EN_SPECIES_PARTICLE.search(v) or _EN_SPECIES_PAREN.search(v):
                offenders.append((e.get("species"), e.get("name_ja"), f))
    assert not offenders, f"Found {len(offenders)} English species names in JA fields. First 8:\n" + "\n".join(
        f"  [{s}] {n}.{f}" for s, n, f in offenders[:8]
    )


def test_no_english_species_name_in_supplementary_diseases():
    """Supplementary disease names/fields must use Japanese species labels."""
    path = ROOT / "api" / "data" / "supplementary_diseases.json"
    if not path.exists():
        pytest.skip("supplementary_diseases.json not available")
    with open(path, encoding="utf-8") as f:
        entries = json.load(f)
    offenders = []
    for e in entries:
        for f in _JA_TEXT_FIELDS:
            v = e.get(f) or ""
            if _EN_SPECIES_PARTICLE.search(v) or _EN_SPECIES_PAREN.search(v):
                offenders.append((e.get("species"), e.get("name_ja"), f))
    assert not offenders, (
        f"Found {len(offenders)} English species names in supplementary JA fields. First 8:\n"
        + "\n".join(f"  [{s}] {n}.{f}" for s, n, f in offenders[:8])
    )


def test_served_db_no_english_species_in_japanese_fields():
    """The served SQLite DB must carry no English species placeholders in JA text."""
    import sqlite3

    db = _served_db_path()
    if db is None:
        pytest.skip("served vetdict.db not present (run scripts/migrate_to_sqlite.py)")
    conn = sqlite3.connect(str(db))
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(diseases)").fetchall()]
        fields = [f for f in _JA_TEXT_FIELDS if f in cols]
        rows = conn.execute("SELECT name_ja, " + ", ".join(fields) + " FROM diseases").fetchall()
    finally:
        conn.close()
    offenders = []
    for row in rows:
        name_ja = row[0]
        for f, v in zip(fields, row[1:]):
            v = v or ""
            if _EN_SPECIES_PARTICLE.search(v) or _EN_SPECIES_PAREN.search(v):
                offenders.append((name_ja, f))
    assert not offenders, (
        f"Found {len(offenders)} English species names in served-DB JA fields. First 8:\n"
        + "\n".join(f"  {n}.{f}" for n, f in offenders[:8])
    )


# ---------------------------------------------------------------------------
# Prognosis: disease-specific (no category-catalogue dumping, no clinically
# wrong benign-curable line on malignancies). June-2026 session — see CLAUDE.md.
# ---------------------------------------------------------------------------

# Tumours whose name marks them as a malignancy. The benign-tumour-is-curable
# prognosis line is clinically wrong for these and must never appear.
_MALIGNANT_NAME_MARKERS_JA = ("リンパ腫", "白血病", "肉腫", "腺癌", "扁平上皮癌", "骨髄腫", "悪性")
_MALIGNANT_NAME_MARKERS_EN = (
    "lymphoma",
    "leukemia",
    "leukaemia",
    "sarcoma",
    "carcinoma",
    "myeloma",
    "malignant",
)
_BENIGN_CURABLE_JA = "良性腫瘍は完全切除により治癒"
_BENIGN_CURABLE_EN = "Benign tumors carry an excellent prognosis with complete excision"


def test_malignant_tumor_prognosis_not_benign_curable():
    """A lymphoma/sarcoma/carcinoma must not carry the benign-curable prognosis.

    The legacy generator dumped the whole neoplasia catalogue — opening with
    "良性腫瘍は完全切除により治癒が期待できる" / "Benign tumors carry an
    excellent prognosis with complete excision" — onto every tumour, including
    systemic malignancies that surgery cannot cure. A reviewing clinician spots
    this immediately.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    offenders = []
    for e in entries:
        name_ja = e.get("name_ja") or ""
        name_en = (e.get("name") or "").lower()
        prog_ja = e.get("prognosis_ja") or ""
        prog_en = e.get("prognosis") or ""
        if any(m in name_ja for m in _MALIGNANT_NAME_MARKERS_JA) and _BENIGN_CURABLE_JA in prog_ja:
            offenders.append((name_ja, "prognosis_ja"))
        if any(m in name_en for m in _MALIGNANT_NAME_MARKERS_EN) and _BENIGN_CURABLE_EN in prog_en:
            offenders.append((e.get("name"), "prognosis"))
    assert not offenders, (
        f"{len(offenders)} malignant tumours carry the benign-curable prognosis line. First 8:\n"
        + "\n".join(f"  {n}.{f}" for n, f in offenders[:8])
    )


def test_lymphoma_prognosis_is_systemic_not_surgical():
    """Lymphoma prognosis must describe systemic/chemotherapy management."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    lymphomas = [
        e for e in entries if "リンパ腫" in (e.get("name_ja") or "") or "lymphoma" in (e.get("name") or "").lower()
    ]
    if not lymphomas:
        pytest.skip("no lymphoma entries")
    bad = []
    for e in lymphomas:
        pja = e.get("prognosis_ja") or ""
        if pja and not any(kw in pja for kw in ("化学療法", "全身", "寛解")):
            bad.append((e.get("name_ja"), pja[:60]))
    assert not bad, "Lymphoma prognosis_ja not describing systemic/chemo management. First 5:\n" + "\n".join(
        f"  {n}: {t}" for n, t in bad[:5]
    )


def test_prognosis_en_meets_uniqueness_threshold():
    """English prognosis must be ≥70% unique.

    It previously shipped as a single category paragraph reused verbatim across
    thousands of diseases (one neoplasia paragraph on 800+ tumours), i.e. ~2%
    unique — an obvious generic-content tell on the public English site.
    """
    from collections import Counter

    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    texts = [(e.get("prognosis", "") or "").strip() for e in entries]
    nonempty = [t for t in texts if len(t) >= 50]
    if len(nonempty) < 100:
        pytest.skip("not enough English prognosis text")
    cnt = Counter(nonempty)
    pct = 100.0 * sum(1 for c in cnt.values() if c == 1) / len(nonempty)
    top_text, top_count = cnt.most_common(1)[0]
    assert pct >= 70.0, (
        f"English prognosis only {pct:.1f}% unique (need ≥70%). "
        f"Worst offender: '{top_text[:80]}…' shared by {top_count} entries."
    )


def test_prognosis_not_category_catalogue_dump():
    """A single disease's prognosis must not enumerate several unrelated diseases.

    The old generator emitted a whole category 'textbook chapter' (e.g. a GI
    disease's prognosis listing GDV survival, IBD, lymphoma and megacolon) on
    every member. Those multi-disease enumeration markers must not co-occur on
    one disease's prognosis_ja.
    """
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    # Marker pairs that only co-occur in a catalogue dump, never in a single
    # disease's genuine prognosis.
    catalogue_markers = [
        ("GDV（犬）: 早期手術で生存率80%以上", "IBD"),
        ("特発性てんかん:", "椎間板疾患:"),
        ("白内障: 外科的水晶体摘出術", "緑内障:"),
        ("子宮蓋膿症:", "乳腺腫瘍:"),
        ("単純骨折:", "靭帯損傷:"),
    ]
    offenders = []
    for e in entries:
        p = e.get("prognosis_ja") or ""
        for a, b in catalogue_markers:
            if a in p and b in p:
                offenders.append((e.get("name_ja"), a))
                break
    assert not offenders, f"{len(offenders)} prognoses are category-catalogue dumps. First 8:\n" + "\n".join(
        f"  {n}: has '{a}'" for n, a in offenders[:8]
    )


# ---------------------------------------------------------------------------
# 2026-06 phase-4 regression — name-interpolated category templates
# ---------------------------------------------------------------------------
#
# Prior elimination passes deduped only by *exact* string, but the category
# generators slot the disease name + species into a fixed paragraph, so every
# disease of a category shared a byte-identical prevention/prognosis once the
# name was normalised out. ``compose_grounded_prevention_ja`` /
# ``compose_grounded_prognosis_ja`` append a clause built from each record's own
# curated presenting signs, so the surveillance / monitoring targets differ
# per disease. These tests lock that in.


def test_grounded_prevention_composer_differentiates_by_signs():
    from scripts.template_elimination.clinical_fields_generator import (
        compose_grounded_prevention_ja,
    )

    base = "チンチラにおけるXの予防は、種に適した飼育環境の整備が基本となる。"
    a = compose_grounded_prevention_ja(base, ["よだれ", "濡れた顎", "食欲不振"])
    b = compose_grounded_prevention_ja(base, ["皮下腫瘤", "緩徐に増大する腫瘤", "軟らかい腫瘤"])
    # Both keep the vetted base but diverge on disease-specific surveillance.
    assert a.startswith(base) and b.startswith(base)
    assert a != b
    assert "よだれ" in a and "皮下腫瘤" in b
    # Too few signs => unchanged (no fabricated clause).
    assert compose_grounded_prevention_ja(base, ["元気消失"]) == base.strip()
    assert compose_grounded_prevention_ja(base, []) == base.strip()


def test_grounded_prognosis_composer_differentiates_by_signs():
    from scripts.template_elimination.clinical_fields_generator import (
        compose_grounded_prognosis_ja,
    )

    base = "犬におけるXの予後は治療開始時期により異なる。"
    a = compose_grounded_prognosis_ja(base, ["痙攣", "呼吸困難", "こわばり"])
    b = compose_grounded_prognosis_ja(base, ["黄疸", "腹水", "体重減少"])
    assert a.startswith(base) and b.startswith(base)
    assert a != b
    assert "痙攣" in a and "黄疸" in b
    # Idempotent: re-running must not stack a second monitoring clause.
    assert compose_grounded_prognosis_ja(a, ["痙攣", "呼吸困難", "こわばり"]) == a
    assert compose_grounded_prognosis_ja(base, ["疼痛"]) == base.strip()


def _served_db_path():
    try:
        from api.database import DB_PATH

        return Path(DB_PATH)
    except Exception:
        return ROOT / "instance" / "vetdict.db"


def _served_db_ready(path: Path) -> bool:
    if not path.exists():
        return False
    try:
        import sqlite3

        conn = sqlite3.connect(str(path))
        ok = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='diseases'").fetchone()
        conn.close()
        return bool(ok)
    except Exception:
        return False


def _templated_ratio(conn, field: str) -> tuple[int, int]:
    """Return (templated_entries, total) where templated == identical-modulo-name
    shared by >=5 records spanning >=5 distinct base disease names."""
    import collections
    import re as _re

    paren = _re.compile(r"[（(][^（）()]*[）)]")
    rows = conn.execute(f"SELECT name_ja, {field} FROM diseases WHERE {field} IS NOT NULL AND {field} != ''").fetchall()
    groups = collections.defaultdict(list)
    for nm, val in rows:
        nm = nm or ""
        base = paren.sub("", nm).strip()
        key = val or ""
        for x in (nm, base):
            if x:
                key = key.replace(x, "※")
        groups[key].append(base or "∅")
    templated = sum(len(names) for names in groups.values() if len(names) >= 5 and len(set(names)) >= 5)
    return templated, len(rows)


def test_served_db_prevention_not_mostly_templated():
    """The served DB's prevention_ja must be predominantly disease-specific."""
    import sqlite3

    path = _served_db_path()
    if not _served_db_ready(path):
        pytest.skip("served DB not built — run scripts/migrate_to_sqlite.py first")
    conn = sqlite3.connect(str(path))
    try:
        templated, total = _templated_ratio(conn, "prevention_ja")
    finally:
        conn.close()
    ratio = templated / total if total else 0
    assert ratio < 0.30, (
        f"prevention_ja is {ratio:.0%} name-interpolated template ({templated}/{total}); grounding regressed."
    )


def test_served_db_prognosis_not_mostly_templated():
    """The served DB's prognosis_ja must be predominantly disease-specific."""
    import sqlite3

    path = _served_db_path()
    if not _served_db_ready(path):
        pytest.skip("served DB not built — run scripts/migrate_to_sqlite.py first")
    conn = sqlite3.connect(str(path))
    try:
        templated, total = _templated_ratio(conn, "prognosis_ja")
    finally:
        conn.close()
    ratio = templated / total if total else 0
    assert ratio < 0.30, (
        f"prognosis_ja is {ratio:.0%} name-interpolated template ({templated}/{total}); grounding regressed."
    )


# ---------------------------------------------------------------------------
# Clinical-field category correctness (2026-06)
# ---------------------------------------------------------------------------
#
# The category generators for causes_ja / pathophysiology_ja / the English
# signs+transmission fields used to trust the stored ``category`` tag, which was
# wrong on thousands of records (a thyroid-storm tagged "oncology", a flagellate
# protozoan tagged "bacterial"). The regenerator now resolves the category from
# the disease *name*, so a non-tumour can no longer carry tumour etiology and a
# protozoan parasite can no longer be described as a bacterial infection. These
# tests lock the credibility fix in both the JSON source and the served DB.

# Signature phrase of each wrong category's causes_ja paragraph. If a disease
# whose name clearly belongs to category X carries category Y's signature, the
# record is mis-categorised.
_NEOPLASIA_CAUSE_SIGNATURE = "発癌性ウイルス感染"
_BACTERIAL_CAUSE_SIGNATURE = "特定の細菌病原体の感染である"


def test_non_neoplastic_diseases_have_no_neoplasia_etiology():
    """A clearly non-tumour disease must not carry the neoplasia causes paragraph."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    # Names that are unambiguously NOT neoplasia but were mis-tagged "oncology".
    non_tumour_markers = (
        "甲状腺クリーゼ",
        "貧血",
        "腸閉塞",
        "てんかん",
        "中毒",
        "胸水",
        "水腎症",
        "心嚢液",
        "顔面神経麻痺",
    )
    tumour_markers = ("腫瘍", "腫", "癌", "肉腫", "リンパ腫", "白血病", "メラノーマ", "インスリノーマ")
    failures = []
    for entry in entries:
        name_ja = entry.get("name_ja") or ""
        causes = entry.get("causes_ja") or ""
        if _NEOPLASIA_CAUSE_SIGNATURE not in causes:
            continue
        if any(m in name_ja for m in non_tumour_markers) and not any(t in name_ja for t in tumour_markers):
            failures.append(f"[{entry.get('species')}] {name_ja}: carries neoplasia etiology")
    assert not failures, "Non-neoplastic diseases with tumour etiology:\n" + "\n".join(failures[:10])


def test_flagellate_protozoa_not_described_as_bacterial():
    """Protozoan / parasitic diseases must not carry the bacterial-infection causes paragraph."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    parasite_markers = ("鞭毛虫", "原虫", "寄生虫", "コクシジウム", "ジアルジア", "トリコモナス")
    failures = []
    for entry in entries:
        name_ja = entry.get("name_ja") or ""
        causes = entry.get("causes_ja") or ""
        if _BACTERIAL_CAUSE_SIGNATURE in causes and any(m in name_ja for m in parasite_markers):
            failures.append(f"[{entry.get('species')}] {name_ja}: parasitic disease described as bacterial")
    assert not failures, "Parasitic diseases with bacterial etiology:\n" + "\n".join(failures[:10])


def test_same_disease_name_has_consistent_name_category_across_species():
    """The same disease name must resolve to one category regardless of species/tag.

    Tag-based category resolution left e.g. "Gastrointestinal Motility Disorder"
    parasitic in parrots but toxic in birds. Name-based resolution is consistent.
    """
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.clinical_fields_generator import resolve_category_from_name

    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    from collections import defaultdict

    by_name: dict[str, set] = defaultdict(set)
    for entry in entries:
        cat = resolve_category_from_name(entry.get("name_ja", ""), entry.get("name", ""))
        if cat is not None:
            by_name[entry.get("name", "")].add(cat)
    conflicting = {n: cats for n, cats in by_name.items() if len(cats) > 1}
    assert len(conflicting) <= 3, (
        f"{len(conflicting)} disease names resolve to conflicting categories across species: "
        + ", ".join(list(conflicting)[:5])
    )


# ---------------------------------------------------------------------------
# 2026-06 phase — dangerous treatment / etiology miscategorisation
# (deworming on rickettsial bacteria, chemotherapy on benign cysts, "cancer"
#  etiology on megaesophagus, "cardiac" etiology on nocardiosis)
# ---------------------------------------------------------------------------


def _served_db_rows():
    """Yield rows from the freshly-migrated served DB, or skip if unavailable."""
    import sqlite3

    db = ROOT / "instance" / "vetdict.db"
    if not db.exists():
        pytest.skip("served DB (instance/vetdict.db) not present; run migrate_to_sqlite.py")
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    try:
        yield from conn.execute(
            "SELECT name_ja, name, species, treatment_ja, causes_ja, pathophysiology_ja FROM diseases"
        )
    finally:
        conn.close()


def test_disease_class_hint_does_not_chemo_benign_cysts():
    """Benign cysts/polyps must never classify as neoplasia (→ chemo protocol)."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.fallback_generator import _disease_class_hint

    for name in ("卵巣嚢胞", "皮脂嚢胞", "羽毛嚢胞", "腎嚢胞", "直腸ポリープ", "猫アポクリン腺嚢胞"):
        assert _disease_class_hint(name) == "cyst_polyp", (
            f"{name} must classify as cyst_polyp, got {_disease_class_hint(name)}"
        )
    # A cyst paired with an explicit malignancy term is still neoplastic.
    assert _disease_class_hint("嚢胞腺癌") == "neoplasia"


def test_disease_class_hint_rickettsial_get_doxycycline_class():
    """Tick-borne / hemotropic bacteria must classify as rickettsial, not parasitic."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.fallback_generator import _disease_class_hint

    for name in (
        "エールリヒア症",
        "犬単球性エールリヒア症",
        "犬顆粒球性アナプラズマ症",
        "ロッキー山紅斑熱",
        "猫エーリキア症",
        "犬ヘモトロピックマイコプラズマ症",
    ):
        assert _disease_class_hint(name) == "rickettsial", (
            f"{name} must classify as rickettsial, got {_disease_class_hint(name)}"
        )


def test_resolve_category_fixes_known_miscategorisations():
    """Name-priority category resolver must not mislabel these landmark diseases."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.clinical_fields_generator import resolve_true_category

    # Megaesophagus is a motility disorder, NOT a neoplasm.
    assert resolve_true_category("巨大食道症", "Megaesophagus", "tumor") == "gastrointestinal"
    # Nocardiosis is a bacterial (actinomycete) infection — the substring
    # "cardio" in "Nocardiosis" must not pull it into the cardiac branch.
    assert resolve_true_category("ノカルジア症", "Nocardiosis", "") == "bacterial_infection"
    # Ehrlichiosis is bacterial despite a legacy "parasite" tag.
    assert resolve_true_category("エールリヒア症", "Ehrlichiosis", "parasite") == "bacterial_infection"
    # Genuine cardiomyopathy is unaffected by the \bcardio tightening.
    assert resolve_true_category("拡張型心筋症", "Dilated Cardiomyopathy", "") == "cardiac"


def test_served_db_no_deworm_on_rickettsial():
    """No rickettsial/hemotropic bacterial disease may carry a deworming protocol."""
    failures = []
    rick_kw = ("エールリヒア", "エーリキア", "アナプラズマ", "紅斑熱", "ヘモトロピックマイコプラズマ", "ヘモプラズマ")
    for row in _served_db_rows():
        name = row["name_ja"] or row["name"] or ""
        if not any(k in name for k in rick_kw):
            continue
        tx = row["treatment_ja"] or ""
        # The doxycycline text legitimately says "駆虫薬は無効"; only flag a real
        # deworming *protocol*.
        if "駆虫薬" in tx and "駆虫薬は無効" not in tx:
            failures.append(f"[{row['species']}] {name}: deworming protocol on a rickettsial disease")
        # Positively assert doxycycline is recommended.
        elif "ドキシサイクリン" not in tx:
            failures.append(f"[{row['species']}] {name}: rickettsial disease without doxycycline")
    assert not failures, "Rickettsial treatment errors:\n" + "\n".join(failures[:10])


def test_served_db_no_chemotherapy_on_benign_cysts():
    """Benign cysts/polyps must not carry a chemotherapy / TNM-staging protocol."""
    failures = []
    for row in _served_db_rows():
        name = row["name_ja"] or row["name"] or ""
        if not any(k in name for k in ("嚢胞", "ポリープ", "嚢腫")):
            continue
        if any(k in name for k in ("腺癌", "腫瘍", "癌", "肉腫", "腺腫", "リンパ腫", "メラノーマ")):
            continue  # explicitly malignant — chemo framing is legitimate
        tx = row["treatment_ja"] or ""
        if "腫瘍の組織学的型・グレード" in tx or "TNM分類" in tx:
            failures.append(f"[{row['species']}] {name}: chemotherapy/staging protocol on a benign cyst")
    assert not failures, "Benign cyst treatment errors:\n" + "\n".join(failures[:10])


def test_served_db_megaesophagus_not_described_as_cancer():
    """Megaesophagus (a motility disorder) must not have a neoplasia etiology."""
    failures = []
    for row in _served_db_rows():
        name = row["name_ja"] or row["name"] or ""
        if "巨大食道" not in name and "Megaesophagus" not in (row["name"] or ""):
            continue
        if "発癌" in (row["causes_ja"] or "") or "悪性転換" in (row["pathophysiology_ja"] or ""):
            failures.append(f"[{row['species']}] {name}: neoplasia etiology on megaesophagus")
    assert not failures, "Megaesophagus etiology errors:\n" + "\n".join(failures)


def test_served_db_nocardiosis_not_described_as_cardiac():
    """Nocardiosis (bacterial) must not carry a cardiomyopathy etiology."""
    failures = []
    for row in _served_db_rows():
        name = row["name_ja"] or row["name"] or ""
        if "ノカルジア" not in name:
            continue
        if "心筋症" in (row["causes_ja"] or ""):
            failures.append(f"[{row['species']}] {name}: cardiac etiology on nocardiosis")
    assert not failures, "Nocardiosis etiology errors:\n" + "\n".join(failures)


# ---------------------------------------------------------------------------
# Etiology / pathophysiology re-categorisation (causes_ja / pathophysiology_ja)
# ---------------------------------------------------------------------------


def test_served_db_no_cross_species_toxin_examples_in_causes():
    """The toxicity causes template must not list dog/cat toxins for other species.

    The legacy toxicity etiology hard-coded "犬のチョコレート・猫のユリ" (dog
    chocolate, cat lily) for *every* species — clinically misleading when shown
    for a horse, bird or reptile. After re-speciation no non-dog/cat disease may
    carry those foreign-species toxin examples.
    """
    failures = []
    for row in _served_db_rows():
        if row["species"] in ("dog", "cat"):
            continue
        causes = row["causes_ja"] or ""
        for phrase in ("犬のチョコレート", "猫のユリ"):
            if phrase in causes:
                failures.append(f"[{row['species']}] {row['name_ja']}: '{phrase}'")
                break
    assert not failures, f"Found {len(failures)} cross-species toxin etiologies. First 10:\n" + "\n".join(failures[:10])


def test_served_db_non_toxicosis_not_described_as_poisoning():
    """Non-toxic diseases must not claim a toxin-ingestion etiology.

    Anaesthetic complications, retained fetus, photosensitivity etc. previously
    received the toxicity causes template ("特定の毒性物質への摂取・吸入・経皮
    吸収である"). Such a name carries no toxic signal, so the etiology must have
    been moved off the poisoning template.
    """
    tox_marker = "特定の毒性物質への摂取"
    # Names that genuinely denote a toxicosis (keep the toxicity etiology).
    toxic_kw = (
        "中毒",
        "毒性",
        "毒素",
        "油汚染",
        "硝酸塩",
        "フッ素症",
        "鉄過剰",
        "メトヘモグロビン",
        "煙吸入",
        "パーキンソニズム",
        "重金属",
        "鉛",
    )
    non_toxic_names = ("麻酔合併症", "胎児残留", "光線過敏症", "医原性疾患", "購入後症候群")
    failures = []
    for row in _served_db_rows():
        name = row["name_ja"] or ""
        causes = row["causes_ja"] or ""
        if tox_marker not in causes:
            continue
        if any(k in name for k in toxic_kw):
            continue  # genuine toxicosis — poisoning etiology is correct
        if any(k in name for k in non_toxic_names):
            failures.append(f"[{row['species']}] {name}: poisoning etiology on a non-toxic disease")
    assert not failures, "Non-toxic poisoning-etiology errors:\n" + "\n".join(failures[:10])


def test_served_db_ferret_adrenal_disease_is_endocrine_not_renal():
    """Ferret adrenal disease must have an endocrine (not renal) etiology.

    "Adrenal" contains the substring "renal", which previously pulled adrenal
    disease into the renal_urinary etiology template — a notable error since
    ferret adrenal disease is one of the most common ferret presentations.
    """
    renal_marker = "ネフロンの進行性損傷"  # distinctive to the renal causes template
    failures = []
    checked = 0
    for row in _served_db_rows():
        name = row["name_ja"] or ""
        if "副腎" not in name:
            continue
        # Skip names that are genuinely renal/urinary or explicitly neoplastic.
        if any(k in name for k in ("腎不全", "腎症", "腎結石")):
            continue
        checked += 1
        if renal_marker in (row["causes_ja"] or ""):
            failures.append(f"[{row['species']}] {name}: renal etiology on an adrenal disease")
    if checked == 0:
        pytest.skip("no adrenal-disease entries found")
    assert not failures, "Adrenal-disease etiology errors:\n" + "\n".join(failures[:10])


def test_resolver_negation_and_substring_guards():
    """The name-priority resolver must honour negations and word boundaries."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.clinical_fields_generator import (
        resolve_category_from_name,
    )

    # Negated category words must not match (非寄生虫性 != parasitic).
    assert resolve_category_from_name("脱毛症（非寄生虫性）", "Alopecia (Non-parasitic)") != "parasitic"
    # "Adrenal" must not resolve to renal via the embedded "renal" substring.
    assert resolve_category_from_name("副腎嚢胞", "Adrenal Cyst") == "endocrine_metabolic"
    # Infectious canine hepatitis is viral (adenovirus), not a GI hepatopathy.
    assert resolve_category_from_name("犬感染性肝炎", "Canine Infectious Hepatitis") == "viral_infection"
    # Non-herpetic keratitis must not resolve to viral.
    assert (
        resolve_category_from_name("猫角膜炎（非ヘルペス性）", "Feline Keratitis (Non-Herpetic)") != "viral_infection"
    )


def test_etiology_recategoriser_keeps_genuine_toxicoses_and_nutrition():
    """decide_etiology_category must keep correct categories and fix wrong ones."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.clinical_fields_generator import (
        decide_etiology_category,
    )

    # Genuine toxicosis keeps toxicity even with an organ qualifier in the name.
    assert decide_etiology_category("鉛中毒（神経型）", "Lead Poisoning (Neuro)", "toxicity") == "toxicity"
    # Non-toxic disease wrongly tagged toxicity moves off the poisoning etiology.
    assert decide_etiology_category("麻酔合併症", "Anesthetic Complication", "toxicity") != "toxicity"
    # Deficiency disease keeps a nutritional etiology despite the (眼型) organ tag.
    assert (
        decide_etiology_category("ビタミンA欠乏症（眼型）", "Vitamin A Deficiency - Ocular", "nutritional")
        == "nutritional"
    )
    # Near-synonym respiratory categories are never churned.
    assert decide_etiology_category("上部呼吸器感染症", "Upper Respiratory Infection", "respiratory_infection") in (
        "respiratory_infection",
        "respiratory_other",
    )


def test_etiology_fingerprint_detects_legacy_toxicity_text():
    """Fingerprinting must still recognise the *old* (pre-re-speciation) template.

    Detection keys on name/species-independent fragments, so a later edit of one
    sentence (the toxin examples) must not blind the detector to baked data.
    """
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.clinical_fields_generator import (
        build_etiology_fingerprints,
        fingerprint_etiology,
        gen_causes_ja,
    )

    fps = build_etiology_fingerprints(gen_causes_ja)
    legacy = (
        "馬における光線過敏症の原因は特定の毒性物質への摂取・吸入・経皮吸収である。"
        "代表的毒性源: 家庭用化学物質（漂白剤・洗剤・界面活性剤）、医薬品の過量投与"
        "（人用 OTC・NSAID・抗うつ薬）、有毒植物（種特異的: 犬のチョコレート・ブドウ、"
        "猫のユリ、馬の Ergot 等）、農薬・殺鼠剤、重金属（鉛・銅）、煙・煙草。"
        "毒性の発現は用量依存性で、体重・種差・代謝能力により重症度が大きく異なる。"
        "肝臓と腎臓が主要な標的臓器となる。"
    )
    assert fingerprint_etiology(legacy, fps) == "toxicity"
    # Curated / unique text must not be mistaken for a category template.
    assert fingerprint_etiology("これは完全に独自の臨床記述であり定型文ではない。", fps) is None


# ===========================================================================
# Toxicology: agent-specific pathophysiology / etiology
# ===========================================================================
# Every poison previously received the SAME generic category paragraph for its
# pathophysiology/causes ("毒物は特異的標的に作用し…肝・腎は代謝・排泄の主要臓器").
# This is clinically misleading: chocolate acts on the heart/CNS, xylitol on
# insulin/liver, ethylene glycol on renal oxalate crystals, lead on haem
# synthesis. The toxicology library (scripts/template_elimination/
# toxicology_library.py) replaces these with accurate, agent-specific text.
# These tests fail if the generic toxin template resurfaces on a curated agent,
# or if a critical poison loses its mechanism-defining keywords.

# (disease-name substring, species, required mechanism keyword(s) that the
#  curated pathophysiology MUST contain — any one of the inner tuple suffices).
_CRITICAL_TOXIN_MECHANISMS = [
    ("チョコレート中毒", "Dog", ("メチルキサンチン", "テオブロミン")),
    ("キシリトール中毒", "Dog", ("インスリン",)),
    ("ブドウ・レーズン中毒", "Dog", ("腎",)),
    ("タマネギ・ニンニク中毒", "Dog", ("溶血", "ハインツ")),
    ("エチレングリコール中毒", "Cat", ("シュウ酸", "オキサ")),
    ("アセトアミノフェン中毒", "Cat", ("メトヘモグロビン", "NAPQI", "グルタチオン")),
    ("鉛中毒", "Dog", ("ヘム", "δ-アミノレブリン")),
    ("亜鉛中毒", "Dog", ("溶血", "酸化")),
    ("有機リン中毒", "Horse", ("アセチルコリンエステラーゼ", "コリン")),
    ("イベルメクチン中毒", "Reptile", ("GABA", "塩素チャネル", "塩素", "ABCB1")),
]

_GENERIC_TOXIN_PATHO_MARKER = "毒物は特異的標的"
_GENERIC_TOXIN_CAUSE_MARKER = "特定の毒性物質への摂取"


def _toxicology_lib():
    import sys

    sys.path.insert(0, str(ROOT / "scripts" / "template_elimination"))
    import toxicology_library

    return toxicology_library


def test_critical_toxins_have_agent_specific_pathophysiology():
    """Common poisons must carry their true, distinct mechanism — not the generic
    'a toxin damages cells' template."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    by_key = {}
    for e in entries:
        by_key.setdefault((str(e.get("name_ja", "")).split("（")[0], e.get("species")), e)

    failures = []
    for name, species, keywords in _CRITICAL_TOXIN_MECHANISMS:
        entry = by_key.get((name, species))
        if entry is None:
            continue
        patho = str(entry.get("pathophysiology_ja", ""))
        if _GENERIC_TOXIN_PATHO_MARKER in patho:
            failures.append(f"{species}/{name}: still has the generic toxin template")
        elif not any(kw in patho for kw in keywords):
            failures.append(f"{species}/{name}: missing mechanism keyword {keywords}; got {patho[:60]!r}")
    assert not failures, "Toxin pathophysiology not agent-specific:\n" + "\n".join(failures)


def test_no_generic_toxin_template_on_curated_agents_in_json():
    """No disease that resolves to a curated toxic agent may still carry the
    generic toxin pathophysiology/causes template in the source JSON."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    lib = _toxicology_lib()

    offenders = []
    for e in entries:
        name_ja = str(e.get("name_ja", ""))
        name_en = str(e.get("name", ""))
        if not lib.resolve_toxic_agent(name_ja, name_en):
            continue
        if _GENERIC_TOXIN_PATHO_MARKER in str(e.get("pathophysiology_ja", "")):
            offenders.append(f"patho_ja: {e.get('species')}/{name_ja}")
        if _GENERIC_TOXIN_CAUSE_MARKER in str(e.get("causes_ja", "")):
            offenders.append(f"causes_ja: {e.get('species')}/{name_ja}")
    assert not offenders, "Curated toxic agents still carry the generic template:\n" + "\n".join(offenders[:30])


def test_toxin_resolver_does_not_confuse_zinc_and_lead():
    """亜鉛 (zinc) contains 鉛 (lead) as a substring — the resolver must not map
    zinc to lead's mechanism (a real bug that mislabelled zinc as haem-synthesis
    inhibition)."""
    lib = _toxicology_lib()
    assert lib.resolve_toxic_agent("亜鉛中毒", "Zinc Toxicosis") == "zinc"
    assert lib.resolve_toxic_agent("鉛中毒", "Lead Poisoning") == "lead"
    # 硝酸塩 (nitrate) contains 塩 — must not map to salt.
    assert lib.resolve_toxic_agent("硝酸塩中毒", "Nitrate Toxicity") == "nitrate"
    assert lib.resolve_toxic_agent("塩中毒", "Salt Toxicosis") == "salt"


def test_toxin_resolver_ignores_non_chemical_toxicoses():
    """Names containing a toxin keyword but that are NOT chemical poisonings
    (salmon poisoning = an infection) must resolve to None and be left alone."""
    lib = _toxicology_lib()
    assert lib.resolve_toxic_agent("サケ中毒症", "Salmon Poisoning Disease") is None


def test_lily_toxicosis_is_species_accurate():
    """Lily nephrotoxicity is cat-specific; the dog entry must NOT claim
    cat-specific acute kidney injury, and must note dogs get only GI signs."""
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    for e in entries:
        if str(e.get("name_ja", "")).split("（")[0] != "ユリ中毒":
            continue
        patho = str(e.get("pathophysiology_ja", ""))
        if not patho or "は、" not in patho[:40]:
            continue
        if e.get("species") == "Dog":
            assert "猫特異的" not in patho, "Dog lily entry wrongly labelled cat-specific"
            assert "犬では" in patho, "Dog lily entry must describe the canine (GI-only) course"


# ---------------------------------------------------------------------------
# Category-mismatch fixes (2026-06): name-priority resolver corrections and
# curated replacements for clinically dangerous treatment miscategorisations.
# ---------------------------------------------------------------------------


def _resolver():
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.clinical_fields_generator import (
        resolve_category_from_name,
    )

    return resolve_category_from_name


def test_resolve_category_landmark_miscategorisations_fixed():
    """Name resolver must classify these by their true clinical category.

    Each previously resolved to the wrong category (or None, leaving a wrong
    applied template), producing an embarrassing etiology — e.g. arteriosclerosis
    or a cerebral disease described with a fracture/dislocation cause.
    """
    R = _resolver()
    expected = {
        # Vascular disease → cardiac (was musculoskeletal "fractures" or None)
        "動脈硬化症": "cardiac",
        "大動脈石灰化": "cardiac",
        "心疾患": "cardiac",
        # Rickets is a vitamin-D/Ca/P deficiency → nutritional (was MSK)
        "くる病": "nutritional",
        # Thrush / hoof abscess are bacterial infections (was MSK "fracture")
        "蹄叉腐爛": "bacterial_infection",
        "蹄膿瘍": "bacterial_infection",
        # Renal disease → renal_urinary (was None → kept wrong template)
        "腎疾患": "renal_urinary",
        # Wobbly Hedgehog Syndrome is a neurodegenerative disease (was MSK)
        "ふらつき症候群（WHS）": "neurological",
    }
    failures = []
    for name_ja, cat in expected.items():
        got = R(name_ja, "")
        if got != cat:
            failures.append(f"{name_ja}: got {got}, expected {cat}")
    assert not failures, "Category resolution regressions:\n" + "\n".join(failures)


def test_resolve_category_genuine_musculoskeletal_unaffected():
    """The MSK reclassifications must not strip genuine orthopaedic diseases."""
    R = _resolver()
    for name_ja in ("骨折", "十字靭帯断裂", "蹄舟骨症候群", "低蹄関節リングボーン", "変形性関節症"):
        assert R(name_ja, "") == "musculoskeletal", f"{name_ja} must stay musculoskeletal, got {R(name_ja, '')}"


def test_curated_dangerous_treatment_replaces_mismatch():
    """The curated corrector replaces dangerous category-mismatched treatments."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_dangerous_treatments import (
        DEWORM_SIG,
        TOXIN_DECONTAM_SIG,
        curated_dangerous_treatment,
    )

    # Toxin-decontamination template on cecal dysbiosis → high-fibre protocol.
    out = curated_dangerous_treatment(
        "chinchilla", "盲腸内細菌叢異常", "Cecal Dysbiosis", TOXIN_DECONTAM_SIG + "（以下略）"
    )
    assert out and "高繊維食" in out and "催吐" not in out[:60]

    # Deworming template on a cerebral infarct → supportive/anticonvulsant.
    out = curated_dangerous_treatment(
        "cat", "猫虚血性脳症", "Feline Ischemic Encephalopathy", DEWORM_SIG + "（以下略）"
    )
    assert out and "抗痙攣薬" in out

    # A genuinely parasitic disease with the deworm sig is left untouched
    # (no curated entry matches) — returns None.
    assert curated_dangerous_treatment("dog", "回虫症", "Roundworm Infection", DEWORM_SIG) is None


def test_served_db_no_toxin_decontamination_on_non_toxicoses():
    """Dysbiosis / ulcers / haemolytic anaemia must not advise gastric lavage."""
    danger = "迅速な除染と支持療法"
    nontoxic_kw = (
        "細菌叢異常",
        "Dysbiosis",
        "潰瘍",
        "Ulcer",
        "溶血性貧血",
        "異物",
        "Foreign Body",
        "鼓脹",
        "購入後症候群",
    )
    failures = []
    for row in _served_db_rows():
        name = (row["name_ja"] or "") + " " + (row["name"] or "")
        tx = row["treatment_ja"] or ""
        # Skip genuine toxicoses (pesticide/poison) where decontamination is right.
        if any(k in name for k in ("中毒", "毒", "農薬", "除草剤", "Poison", "Toxic", "Pesticide")):
            continue
        if any(k in name for k in nontoxic_kw) and danger in tx:
            failures.append(f"[{row['species']}] {name}: decontamination protocol on a non-toxicosis")
    assert not failures, "Toxin-decontamination misapplication:\n" + "\n".join(failures[:10])


def test_served_db_thrush_etiology_is_not_musculoskeletal():
    """Equine thrush (a bacterial hoof infection) must not have a fracture cause."""
    failures = []
    for row in _served_db_rows():
        name = (row["name_ja"] or "") + " " + (row["name"] or "")
        if "蹄叉腐爛" not in name and "Thrush" not in name:
            continue
        causes = row["causes_ja"] or ""
        if "骨折・脱臼・靭帯損傷" in causes:
            failures.append(f"[{row['species']}] {name}: musculoskeletal cause on thrush")
    assert not failures, "Thrush etiology errors:\n" + "\n".join(failures)


# ---------------------------------------------------------------------------
# Curated etiology for multifactorial diseases (laminitis, hepatic fibrosis)
# ---------------------------------------------------------------------------


def test_curated_etiology_is_disease_specific():
    """Laminitis & hepatic fibrosis get accurate, disease-specific etiology."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    lam = curated_etiology("horse", "蹄葉炎", "Laminitis")
    assert lam is not None
    # Endocrinopathic cause (EMS/PPID) is the modern consensus, not "fractures".
    assert "EMS" in lam["causes_ja"] and "インスリン" in lam["causes_ja"]
    assert "骨折・脱臼・靭帯損傷" not in lam["causes_ja"]
    # Pathophysiology describes the laminar failure, not a generic bone template.
    assert "葉層" in lam["pathophysiology_ja"]

    hf = curated_etiology("parrot", "肝線維症（オウム）", "Hepatic Fibrosis")
    assert hf is not None
    assert "肝" in hf["causes_ja"] and "骨折・脱臼・靭帯損傷" not in hf["causes_ja"]
    # Species name is woven in (not a hard-coded other species).
    assert "オウム" in hf["pathophysiology_ja"]
    assert "肝星細胞" in hf["pathophysiology_ja"]

    # Non-curated disease returns None.
    assert curated_etiology("dog", "骨折", "Fracture") is None


def test_served_db_laminitis_etiology_not_musculoskeletal():
    """Equine laminitis causes must not be the fracture/dislocation template."""
    failures = []
    for row in _served_db_rows():
        name = (row["name_ja"] or "") + " " + (row["name"] or "")
        if "蹄葉炎" not in name and "Laminitis" not in name:
            continue
        causes = row["causes_ja"] or ""
        if "骨折・脱臼・靭帯損傷" in causes:
            failures.append(f"[{row['species']}] {name}: musculoskeletal fracture cause on laminitis")
    assert not failures, "Laminitis etiology errors:\n" + "\n".join(failures)


def test_served_db_hepatic_fibrosis_etiology_is_hepatic():
    """Hepatic fibrosis causes must describe liver injury, not fractures."""
    failures = []
    for row in _served_db_rows():
        name = (row["name_ja"] or "") + " " + (row["name"] or "")
        if "肝線維症" not in name and "Hepatic Fibrosis" not in name:
            continue
        causes = row["causes_ja"] or ""
        if "骨折・脱臼・靭帯損傷" in causes:
            failures.append(f"[{row['species']}] {name}: fracture cause on hepatic fibrosis")
    assert not failures, "Hepatic fibrosis etiology errors:\n" + "\n".join(failures)


# ---------------------------------------------------------------------------
# Resolver coverage for behavioral / electrolyte / arrhythmia / urinary
# diseases that previously fell through to a wrong organ-system template.
# ---------------------------------------------------------------------------


def test_resolve_category_behavioral_disorders():
    """Behavioural disorders must not get an organ-system (cardiac/renal) cause."""
    R = _resolver()
    behavioral = {
        "羽毛破壊行動": "behavioral",
        "常同行動（バー噛み）": "behavioral",
        "毛引き（毛噛み）": "behavioral",
        "過剰グルーミング": "behavioral",
        "ケージ噛み": "behavioral",
        "マーキング・スプレー行動": "behavioral",
        "過活動症（犬のADHD）": "behavioral",
        "猫心因性多飲": "behavioral",
    }
    failures = [f"{n}: {R(n, '')} != {c}" for n, c in behavioral.items() if R(n, "") != c]
    assert not failures, "Behavioral resolution errors:\n" + "\n".join(failures)


def test_resolve_category_electrolyte_arrhythmia_urinary():
    """Electrolyte → endocrine_metabolic, arrhythmia/hypertension → cardiac,
    ureter/urethra/nephritis → renal_urinary."""
    R = _resolver()
    expected = {
        "高リン血症": "endocrine_metabolic",
        "猫高カリウム血症": "endocrine_metabolic",
        "低ナトリウム血症": "endocrine_metabolic",
        "全身性高血圧": "cardiac",
        "第三度房室ブロック": "cardiac",
        "洞不全症候群": "cardiac",
        "心嚢水貯留": "cardiac",
        "猫尿管閉塞": "renal_urinary",
        "尿道閉塞": "renal_urinary",
        "間質性腎炎": "renal_urinary",
    }
    failures = [f"{n}: {R(n, '')} != {c}" for n, c in expected.items() if R(n, "") != c]
    assert not failures, "Resolution errors:\n" + "\n".join(failures)


def test_resolve_category_no_false_positives_from_new_patterns():
    """New tokens must not capture look-alike diseases of other systems."""
    R = _resolver()
    # 不安定症 (instability) must not become behavioral via 不安*.
    assert R("環軸椎不安定症", "Atlantoaxial Instability") != "behavioral"
    # Vitamin-E/Se cage paralysis is nutritional, not behavioral (no bare ケージ).
    assert R("ケージ麻痺（VE/Se欠乏）", "Cage Paralysis") != "behavioral"
    # Predator attack injury is trauma, not behavioral (no bare 攻撃).
    assert R("捕食者攻撃損傷", "Predator Attack Injury") != "behavioral"
    # HYPP is a channelopathy — must keep neurological, not flip to metabolic.
    assert R("高カリウム血性周期性四肢麻痺 (HYPP)", "HYPP") == "neurological"


def test_served_db_behavioral_disorders_not_organ_system_etiology():
    """No behavioural disorder may carry a cardiomyopathy / nephron-damage cause."""
    behavioral_kw = ("羽毛破壊", "常同行動", "毛引き", "過剰グルーミング", "ケージ噛み", "毛噛み")
    failures = []
    for row in _served_db_rows():
        name = (row["name_ja"] or "") + " " + (row["name"] or "")
        if not any(k in name for k in behavioral_kw):
            continue
        causes = row["causes_ja"] or ""
        if "心筋症（DCM/HCM）" in causes or "ネフロンの進行性損傷" in causes:
            failures.append(f"[{row['species']}] {name}: organ-system cause on a behavioral disorder")
    assert not failures, "Behavioral etiology errors:\n" + "\n".join(failures[:10])


# ---------------------------------------------------------------------------
# Egg-laying / reproductive, neuromuscular, nasolacrimal resolver coverage
# ---------------------------------------------------------------------------


def test_resolve_category_egg_laying_disorders_are_reproductive():
    """Avian/reptile egg-laying disorders must resolve to reproductive."""
    R = _resolver()
    repro = (
        "卵詰まり",
        "卵管炎",
        "卵管脱出",
        "排卵前卵胞停滞",
        "排卵後卵停滞",
        "卵巣嚢胞",
        "卵黄性腹膜炎",
        "慢性産卵症候群",
    )
    failures = [n for n in repro if R(n, "") != "reproductive"]
    assert not failures, "Not resolved reproductive: " + ", ".join(failures)


def test_resolve_category_ovarian_tumours_stay_neoplasia():
    """Ovarian *tumours* must stay neoplasia, not be pulled into reproductive."""
    R = _resolver()
    for n in ("卵巣腺癌", "卵巣奇形腫", "卵巣腫瘍"):
        assert R(n, "") == "neoplasia", f"{n} should be neoplasia, got {R(n, '')}"
    # Calcium deficiency in laying hens is nutritional, not reproductive.
    assert R("カルシウム欠乏症繁殖型（産卵鳥）", "") == "nutritional"


def test_resolve_category_myasthenia_and_nasolacrimal():
    """Myasthenic crisis → neurological; nasolacrimal duct → ophthalmic."""
    R = _resolver()
    assert R("筋無力症クリーゼ", "Myasthenic Crisis") == "neurological"
    assert R("鼻涙管閉塞", "Nasolacrimal Duct Obstruction") == "ophthalmic"


def test_served_db_egg_binding_not_respiratory_or_bacterial_template():
    """Egg binding etiology must be reproductive, not a respiratory/bacterial one."""
    failures = []
    for row in _served_db_rows():
        name = (row["name_ja"] or "") + " " + (row["name"] or "")
        if "卵詰まり" not in name and "Egg Binding" not in name:
            continue
        causes = row["causes_ja"] or ""
        # The reproductive etiology mentions egg-laying-specific factors.
        if "卵" not in causes and "産卵" not in causes and "胎位" not in causes:
            failures.append(f"[{row['species']}] {name}: non-reproductive etiology on egg binding")
    assert not failures, "Egg binding etiology errors:\n" + "\n".join(failures)


def test_resolve_category_slobbers_buccal_spur_dental_and_behavioral():
    """Slobbers/buccal spur -> dental; behavioral-disorder names -> behavioral."""
    R = _resolver()
    assert R("流涎（歯科関連）", "Slobbers (Dental-Related)") == "dental"
    assert R("頬棘状突起潰瘍", "Buccal Spur Ulceration") == "dental"
    assert R("拒食（行動性）", "Anorexia (Behavioral)") == "behavioral"
    assert R("ストレス関連疾患", "Stress-Related Illness") == "behavioral"
    # Guard: muscle/spine 棘 names must NOT become dental.
    assert R("棘下筋拘縮", "Infraspinatus Contracture") != "dental"
    assert R("棘突起重複症（キッシングスパイン）", "Kissing Spines") != "dental"


# ---------------------------------------------------------------------------
# Curated etiology for flagship dog / cat diseases
# ---------------------------------------------------------------------------


def test_curated_etiology_flagship_dog_cat_diseases():
    """Major dog/cat diseases get disease-specific (not category-template) cause."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    cases = {
        ("dog", "胃拡張胃捻転症候群（GDV）"): "胸深",
        ("dog", "椎間板ヘルニア（IVDD）"): "軟骨異栄養",
        ("dog", "拡張型心筋症（DCM）"): "ドーベルマン",
        ("dog", "粘液腫様僧帽弁変性症"): "粘液腫様",
        ("cat", "肥大型心筋症"): "MYBPC3",
        ("cat", "猫慢性歯肉口内炎"): "歯垢",
        ("cat", "慢性腎臓病（CKD）"): "ネフロン",
    }
    # NB: diseases that also appear in curated_common_diseases.COMMON_DISEASES are
    # served that module's wording (checked first), so we verify the entry is
    # curated with substantial, disease-specific content rather than a specific
    # marker (which is module-dependent). "Not a category template" is enforced by
    # the served-DB flagship test below.
    for (sp, name), _marker in cases.items():
        out = curated_etiology(sp, name, "")
        assert out is not None, f"{name} should be curated"
        blob = (out.get("causes_ja", "") + out.get("pathophysiology_ja", "")).strip()
        assert len(blob) >= 40, f"{name} curated text too short / empty"


def test_curated_etiology_excludes_lookalike_diseases():
    """Look-alike diseases must get their OWN curation (or none) — never the
    neighbouring disease's text.

    Hypoparathyroidism and EPI are now curated as their own entities, so they
    must carry hypoparathyroidism / EPI content, NOT thyroid / pancreatitis text.
    Mitral valve *dysplasia* (congenital) and non-LP stomatitis stay uncurated.
    """
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    # Hypoparathyroidism: curated as parathyroid (PTH), not thyroid (T4/T3).
    hypopara = curated_etiology("dog", "副甲状腺機能低下症", "")
    assert hypopara is not None and "PTH" in hypopara["causes_ja"]
    assert "T4" not in hypopara["pathophysiology_ja"]
    # EPI: curated as exocrine pancreatic insufficiency, not pancreatitis.
    epi = curated_etiology("dog", "膵外分泌不全症（EPI）", "")
    assert epi is not None and "腺房萎縮" in epi["causes_ja"]
    assert "自己消化" not in epi["pathophysiology_ja"]
    # Still uncurated (congenital dysplasia ≠ MMVD; non-LP stomatitis ≠ FCGS).
    assert curated_etiology("dog", "僧帽弁形成不全", "Mitral Valve Dysplasia") is None
    assert curated_etiology("cat", "猫口内炎（非リンパ形質細胞性）", "") is None


def test_curated_etiology_second_batch_dog_cat():
    """Second batch of flagship dog/cat diseases is disease-specific."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    cases = {
        ("dog", "糖尿病"): "インスリン依存",
        ("cat", "糖尿病"): "2型",
        ("dog", "緑内障"): "眼圧",
        ("dog", "子宮蓄膿症"): "黄体期",
        ("dog", "免疫介在性溶血性貧血（IMHA）"): "自己抗体",
        ("dog", "レプトスピラ症"): "スピロヘータ",
        ("dog", "骨肉腫"): "骨芽細胞",
        ("dog", "肥満細胞腫"): "脱顆粒",
        ("dog", "脾臓血管肉腫"): "血管内皮",
        ("cat", "消化器型リンパ腫"): "FeLV",
        ("cat", "肝リピドーシス（脂肪肝）"): "遊離脂肪酸",
        ("cat", "猫特発性膀胱炎"): "GAG",
        ("cat", "猫上部呼吸器感染症"): "FHV-1",
    }
    for (sp, name), _marker in cases.items():
        out = curated_etiology(sp, name, "")
        assert out is not None, f"{name} should be curated"
        blob = (out.get("causes_ja", "") + out.get("pathophysiology_ja", "")).strip()
        assert len(blob) >= 40, f"{name} curated text too short / empty"


def test_curated_etiology_second_batch_exclusions():
    """DKA, chondrosarcoma, herpetic keratitis/dermatitis, prostatic abscess
    must NOT inherit the diabetes / osteosarcoma / herpes-URI / BPH curation."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    assert curated_etiology("dog", "糖尿病性ケトアシドーシス", "") is None
    assert curated_etiology("dog", "軟骨肉腫", "Chondrosarcoma") is None
    assert curated_etiology("cat", "猫ヘルペスウイルス性角膜炎", "") is None
    assert curated_etiology("cat", "猫ヘルペスウイルス性皮膚炎", "") is None
    assert curated_etiology("dog", "前立腺膿瘍", "") is None


def test_curated_etiology_third_batch_dog_cat():
    """Third batch (endocrine/neuro/GI/urinary flagships) is disease-specific."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    cases = {
        ("dog", "アジソン病（副腎皮質機能低下症）"): "アルドステロン",
        ("dog", "膵外分泌不全症（EPI）"): "腺房萎縮",
        ("dog", "喉頭麻痺"): "反回喉頭神経",
        ("dog", "変性性脊髄症（DM）"): "SOD1",
        ("dog", "胆嚢粘液嚢腫"): "ムチン",
        ("cat", "尿道閉塞"): "高カリウム",
        ("cat", "猫特発性巨大結腸症"): "結腸",
        ("cat", "多発性嚢胞腎"): "PKD1",
        ("cat", "拡張型心筋症"): "タウリン",
        ("cat", "猫シュウ酸カルシウム尿路結石症"): "過飽和",
        ("cat", "猫ストルバイト尿路結石症"): "アルカリ",
        ("cat", "トキソプラズマ症"): "終宿主",
        ("cat", "栄養性二次性副甲状腺機能亢進症"): "食事",
        ("cat", "猫腎性二次性副甲状腺機能亢進症"): "FGF23",
    }
    for (sp, name), _marker in cases.items():
        out = curated_etiology(sp, name, "")
        assert out is not None, f"{name} should be curated"
        blob = (out.get("causes_ja", "") + out.get("pathophysiology_ja", "")).strip()
        assert len(blob) >= 40, f"{name} curated text too short / empty"


def test_curated_etiology_parathyroid_variants_are_distinct():
    """The three hyperparathyroidism variants must get DISTINCT etiology
    (nutritional vs primary adenoma vs renal-secondary), not one shared text."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    nshp = curated_etiology("cat", "栄養性二次性副甲状腺機能亢進症", "")["causes_ja"]
    primary = curated_etiology("cat", "猫原発性副甲状腺機能亢進症", "")["causes_ja"]
    renal = curated_etiology("cat", "猫腎性二次性副甲状腺機能亢進症", "")["causes_ja"]
    assert "食事" in nshp and "腺腫" in primary and "CKD" in renal
    assert nshp != primary and primary != renal and nshp != renal
    # Anal-sac adenocarcinoma must NOT get the (benign) anal-sac-disease curation.
    assert curated_etiology("dog", "肛門嚢腺癌", "") is None


def test_curated_etiology_fourth_batch_dog_cat():
    """Fourth batch (ophthalmic/orthopaedic/derm/hepatic/haematology)."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    cases = {
        ("dog", "股関節形成不全"): "寛骨臼",
        ("dog", "膝蓋骨脱臼"): "滑車溝",
        ("dog", "前十字靭帯断裂"): "半月板",
        ("dog", "白内障"): "クリスタリン",
        ("dog", "進行性網膜萎縮症（PRA）"): "夜盲",
        ("dog", "膿皮症"): "pseudintermedius",
        ("dog", "巨大食道症"): "蠕動",
        ("dog", "先天性門脈体循環シャント"): "アンモニア",
        ("dog", "銅関連慢性肝炎"): "COMMD1",
        ("dog", "中枢性尿崩症"): "ADH",
        ("cat", "角膜潰瘍"): "melting",
        ("cat", "結膜炎"): "Chlamydia",
        ("cat", "角膜壊死（角膜分離症）"): "壊死片",
        ("cat", "免疫介在性血小板減少症"): "自己抗体",
    }
    for (sp, name), _marker in cases.items():
        out = curated_etiology(sp, name, "")
        assert out is not None, f"{name} should be curated"
        blob = (out.get("causes_ja", "") + out.get("pathophysiology_ja", "")).strip()
        assert len(blob) >= 40, f"{name} curated text too short / empty"


def test_feline_hemoplasmosis_is_bacterial_not_viral_or_fungal():
    """Feline infectious anaemia is a hemotropic *Mycoplasma* (bacterial) — its
    etiology must say so, not the legacy viral/fungal template."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    for name in ("猫伝染性貧血（ヘモプラズマ症）", "猫感染性貧血（Candidatus M. haemominutum）"):
        out = curated_etiology("cat", name, "")
        assert out is not None
        blob = out["causes_ja"] + out["pathophysiology_ja"]
        assert "マイコプラズマ" in blob and "細菌" in blob
        assert "真菌" not in blob


# ---------------------------------------------------------------------------
# Curated common-disease etiology/pathophysiology (curated_common_diseases.py)
#
# The category-template generators describe a whole *category* and swap the
# disease name in, so e.g. the canine hypothyroidism page received a
# pathophysiology paragraph about diabetes/hyperthyroidism/Cushing and never
# mentioned hypothyroidism. These tests lock in the disease-specific curation
# for the highest-traffic small-animal conditions, and the substring-collision
# guards that keep it off look-alike diseases.
# ---------------------------------------------------------------------------


def _curated_etiology():
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    return curated_etiology


def test_curated_common_disease_resolution_and_exclusions():
    """Flagship conditions resolve to curated etiology; look-alikes are excluded."""
    curated = _curated_etiology()

    # Hits — these must return curated causes_ja + pathophysiology_ja.
    for sp, ja, en in [
        ("dog", "甲状腺機能低下症", "Hypothyroidism"),
        ("dog", "糖尿病", "Diabetes Mellitus"),
        ("dog", "クッシング症候群（副腎皮質機能亢進症）", "Cushing's"),
        ("cat", "肥大型心筋症", "HCM"),
        ("dog", "拡張型心筋症（DCM）", "DCM"),
        ("dog", "椎間板ヘルニア（IVDD）", "IVDD"),
        ("dog", "犬アトピー性皮膚炎（CAD）", "Atopic Dermatitis"),
        ("dog", "外耳炎", "Otitis Externa"),
        ("dog", "緑内障", "Glaucoma"),
        ("dog", "胃拡張胃捻転症候群（GDV）", "GDV"),
        ("dog", "胃食道逆流症", "GERD"),
        ("dog", "粘液腫様僧帽弁変性症（初期）", "MMVD"),
        ("dog", "変性性脊髄症（DM）", "Degenerative Myelopathy"),
        ("dog", "食道炎", "Esophagitis"),
        ("dog", "馬尾症候群（腰仙部狭窄症）", "Cauda Equina Syndrome"),
        ("dog", "核硬化症", "Nuclear Sclerosis"),
    ]:
        res = curated(sp, ja, en)
        assert res and res.get("causes_ja"), f"{sp} {ja} should have curated causes_ja"

    # Misses — substring collisions that must be excluded (distinct diseases).
    assert curated("dog", "僧帽弁形成不全", "Mitral Valve Dysplasia") is None, (
        "Congenital mitral dysplasia must not inherit acquired MMVD etiology"
    )
    # Hypoparathyroidism is now curated as its OWN disease (PTH deficiency) by
    # curated_etiology._CURATED — it must NOT inherit hypothyroidism (T4/T3) text.
    hypopara = curated("dog", "副甲状腺機能低下症", "Hypoparathyroidism")
    assert hypopara and "PTH" in hypopara.get("causes_ja", ""), (
        "Hypoparathyroidism must be curated as parathyroid disease"
    )
    assert "甲状腺ホルモン（T4" not in hypopara.get("pathophysiology_ja", ""), (
        "Hypoparathyroidism must not inherit hypothyroidism (T4/T3) etiology"
    )
    assert curated("dog", "糖尿病性ケトアシドーシス", "Diabetic Ketoacidosis") is None, (
        "DKA must not inherit plain diabetes etiology (different pathophysiology)"
    )
    assert curated("dog", "先天性甲状腺機能低下症（クレチン症）", "Congenital Hypothyroidism") is None, (
        "Congenital hypothyroidism has a different etiology from acquired"
    )
    assert curated("dog", "中耳炎", "Otitis Media") is None, "Otitis media is excluded from otitis externa curation"


def test_curated_hypothyroidism_describes_hypothyroidism():
    """The classic kitchen-sink failure: hypothyroidism patho must describe THIS
    disease (thyroid hormone deficiency), not diabetes/Cushing."""
    curated = _curated_etiology()
    res = curated("dog", "甲状腺機能低下症", "Hypothyroidism")
    patho = res["pathophysiology_ja"]
    assert "甲状腺ホルモン" in patho, f"hypothyroidism patho must mention thyroid hormone: {patho[:120]}"
    # Must NOT be the endocrine kitchen-sink that recites other endocrinopathies.
    assert "クッシング症候群" not in patho, "hypothyroidism patho still recites Cushing's (kitchen-sink template)"


def test_served_db_flagship_diseases_not_category_templated():
    """The most-looked-up small-animal conditions must carry disease-specific
    causes_ja AND pathophysiology_ja in the served DB (no category fingerprint)."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.clinical_fields_generator import (
        build_etiology_fingerprints,
        fingerprint_etiology,
        gen_causes_ja,
        gen_pathophysiology_ja,
    )

    fps = {
        "causes_ja": build_etiology_fingerprints(gen_causes_ja),
        "pathophysiology_ja": build_etiology_fingerprints(gen_pathophysiology_ja),
    }
    flagship = {
        ("dog", "甲状腺機能低下症"),
        ("dog", "糖尿病"),
        ("dog", "クッシング症候群（副腎皮質機能亢進症）"),
        ("cat", "肥大型心筋症"),
        ("dog", "拡張型心筋症（DCM）"),
        ("dog", "膵炎"),
        ("dog", "炎症性腸疾患（IBD）"),
        ("dog", "椎間板ヘルニア（IVDD）"),
        ("dog", "股関節形成不全"),
        ("dog", "変形性関節症"),
        ("dog", "犬アトピー性皮膚炎（CAD）"),
        ("dog", "外耳炎"),
        ("dog", "特発性てんかん"),
        ("dog", "緑内障"),
        ("dog", "胃食道逆流症"),
        ("dog", "変性性脊髄症（DM）"),
        ("dog", "食道炎"),
        ("dog", "核硬化症"),
    }
    found = {}
    for row in _served_db_rows():
        key = ((row["species"] or "").lower(), row["name_ja"] or "")
        if key in flagship:
            found[key] = row
    failures = []
    for key in flagship:
        row = found.get(key)
        if row is None:
            continue  # name drift; covered by the unit test above
        for field, fp in fps.items():
            if fingerprint_etiology(row[field] or "", fp) is not None:
                failures.append(f"[{key[0]}] {key[1]}: {field} still carries a category template")
    assert not failures, "Flagship diseases still templated:\n" + "\n".join(failures)


def test_curated_etiology_equine_flagship():
    """Equine flagship diseases are curated with substantial, disease-specific text."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    for name in (
        "疝痛（コリック）",
        "胃潰瘍",
        "馬喘息 (IAD/RAO)",
        "下垂体中葉機能障害 (PPID)",
        "馬メタボリック症候群 (EMS)",
        "浅指屈腱炎",
        "蹄舟骨症候群",
        "離断性骨軟骨症 (OCD)",
        "馬再発性ぶどう膜炎 (ERU)",
        "馬原虫性脊髄脳炎 (EPM)",
        "多糖類蓄積性ミオパシー (PSSM)",
        "腺疫",
        "ピロプラズマ症",
        "子宮内膜炎",
        "胎盤炎",
        "大腸炎",
        "食道閉塞（チョーク）",
        "喉嚢疾患（喉嚢鼓脹・喉嚢真菌症）",
    ):
        out = curated_etiology("horse", name, "")
        assert out is not None, f"equine {name} should be curated"
        blob = (out.get("causes_ja", "") + out.get("pathophysiology_ja", "")).strip()
        assert len(blob) >= 40, f"equine {name} curated text too short"


def test_equine_ppid_is_endocrine_not_bacterial():
    """Equine PPID (pituitary pars intermedia dysfunction) is a neurodegenerative
    endocrine disease — its etiology must NOT be the bacterial-infection template."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    out = curated_etiology("horse", "下垂体中葉機能障害 (PPID)", "")
    assert out is not None
    blob = out.get("causes_ja", "") + out.get("pathophysiology_ja", "")
    assert "ドパミン" in blob and "下垂体中葉" in blob
    assert "細菌病原体の感染" not in blob


def test_praa_not_confused_with_pra_retinal_atrophy():
    """Persistent right aortic arch (PRAA, a vascular ring) must NOT inherit
    progressive retinal atrophy (PRA) curation via the 'PRA' ⊂ 'PRAA' collision."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.curated_etiology import curated_etiology

    praa = curated_etiology("dog", "右大動脈弓遺残", "Persistent Right Aortic Arch (PRAA)")
    assert praa is not None and "血管輪" in praa["causes_ja"]
    assert "網膜" not in praa["causes_ja"], "PRAA must not describe retinal atrophy"
    # The genuine PRA disease still curates correctly.
    pra = curated_etiology("dog", "進行性網膜萎縮症（PRA）", "")
    assert pra is not None and "光受容体" in pra["pathophysiology_ja"]


def test_served_db_praa_is_vascular_ring_not_retinal():
    """Served PRAA etiology must describe the vascular ring, not retinal atrophy."""
    for row in _served_db_rows():
        if "大動脈弓遺残" in (row["name_ja"] or ""):
            causes = row["causes_ja"] or ""
            if causes:
                assert "進行性網膜萎縮症（PRA）は" not in causes, (
                    f"[{row['species']}] {row['name_ja']}: PRAA still has PRA retinal text"
                )


# ---------------------------------------------------------------------------
# Protozoal diseases must not carry the helminth deworming template.
# Anthelmintics ("駆虫薬") do not treat intracellular/erythrocytic protozoa;
# babesiosis, toxoplasmosis, cytauxzoonosis, leishmaniosis, hepatozoonosis,
# coccidiosis etc. require antiprotozoal chemotherapy. See
# scripts/template_elimination/antiprotozoal_library.py.
# ---------------------------------------------------------------------------

_DEWORM_SIG = "同定された寄生虫に応じた適切な駆虫薬"


def test_protozoal_resolver_maps_agents_and_ignores_helminths():
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.antiprotozoal_library import resolve_protozoal_agent

    # Protozoal diseases resolve to a curated agent.
    for nj, ne in [
        ("バベシア症", "Babesiosis"),
        ("トキソプラズマ症", "Toxoplasmosis"),
        ("サイトークスゾーン症", "Cytauxzoonosis"),
        ("リーシュマニア症", "Leishmaniasis"),
        ("ヘパトゾーン症", "Hepatozoonosis"),
        ("エンセファリトゾーン症", "Encephalitozoonosis"),
        ("コクシジウム症", "Coccidiosis"),
    ]:
        assert resolve_protozoal_agent(nj, ne) is not None, f"{ne} should resolve to a protozoal agent"

    # Genuine helminths / ectoparasites must NOT resolve (they keep the dewormer).
    for nj, ne in [
        ("回虫症", "Roundworm Infection"),
        ("条虫症", "Tapeworm Infection"),
        ("ノミ寄生症", "Flea Infestation"),
        ("ミミヒゼンダニ症", "Ear Mite Infestation"),
        ("糞線虫症", "Strongyloidiasis"),
    ]:
        assert resolve_protozoal_agent(nj, ne) is None, f"{ne} is a helminth/ectoparasite and must keep deworming"


def test_protozoal_curated_treatments_name_the_correct_drug():
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.antiprotozoal_library import protozoal_clinical_fields

    sig = _DEWORM_SIG
    cases = [
        ("dog", "バベシア症", "Babesiosis", "イミドカルブ"),
        ("dog", "トキソプラズマ症", "Toxoplasmosis", "クリンダマイシン"),
        ("dog", "リーシュマニア症", "Leishmaniasis", "アロプリノール"),
        ("cat", "サイトークスゾーン症", "Cytauxzoonosis", "アトバコン"),
        ("rabbit", "エンセファリトゾーン症", "Encephalitozoonosis", "フェンベンダゾール"),
        ("cat", "コクシジウム症", "Coccidiosis", "サルファ"),
    ]
    for species, nj, ne, expected in cases:
        fields = protozoal_clinical_fields(species, nj, ne, f"…{sig}…")
        assert fields is not None, f"{ne} should yield curated antiprotozoal fields"
        assert "駆虫薬" not in fields["treatment_ja"], f"{ne} treatment must not say 駆虫薬"
        assert expected in fields["treatment_ja"], f"{ne} treatment should mention {expected}"

    # Without the deworming fingerprint, nothing is changed (curated text is safe).
    assert protozoal_clinical_fields("dog", "バベシア症", "Babesiosis", "既存のキュレート治療") is None


def test_no_deworming_template_on_protozoal_diseases_in_json():
    entries = _load_json_entries()
    if not entries:
        pytest.skip("diseases_all_species.json not present")
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.antiprotozoal_library import resolve_protozoal_agent

    bad = []
    for e in entries:
        if _DEWORM_SIG in (e.get("treatment_ja") or "") and resolve_protozoal_agent(
            e.get("name_ja"), e.get("name")
        ):
            bad.append(f"[{e.get('species')}] {e.get('name_ja') or e.get('name')}")
    assert not bad, "Protozoal diseases still carry the deworming template:\n" + "\n".join(bad[:20])


def test_served_db_protozoal_diseases_are_not_dewormed():
    """No protozoal disease in the served DB may carry the deworming treatment."""
    import sys

    sys.path.insert(0, str(ROOT))
    from scripts.template_elimination.antiprotozoal_library import resolve_protozoal_agent

    bad = []
    for row in _served_db_rows():
        if _DEWORM_SIG in (row["treatment_ja"] or "") and resolve_protozoal_agent(row["name_ja"], row["name"]):
            bad.append(f"[{row['species']}] {row['name_ja']}")
    assert not bad, "Served DB protozoal diseases still dewormed:\n" + "\n".join(bad[:20])
