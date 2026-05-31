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
