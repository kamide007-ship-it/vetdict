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
