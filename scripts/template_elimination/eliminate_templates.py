"""Eliminate generic template content from the disease database.

This script:
1. Scans ``diseases_all_species.json`` and ``api/species/*_diseases.py`` for
   known generic templates in ``treatment_ja`` and ``treatment`` fields.
2. For each template instance, generates **disease-specific, species-tailored**
   replacement content using the curated content library
   (``template_content_library.py``) or the structured fallback generator
   (``fallback_generator.py``).
3. Writes the updated JSON in-place and patches the Python species modules
   in-place (preserving formatting, just swapping the templated strings).

Run with::

    python3 scripts/template_elimination/eliminate_templates.py

Followed by ``python3 scripts/migrate_to_sqlite.py`` to refresh the SQLite DB.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.fallback_generator import generate_fallback_content  # noqa: E402
from scripts.template_elimination.template_content_library import generate_content  # noqa: E402

# Japanese template strings to eliminate
TEMPLATES_JA: list[str] = [
    # generic_metabolic
    "種適切な診断で原因同定。診断に基づく治療。支持療法：種に適切な温度・水分・栄養維持。疼痛管理。治療反応モニタリング。診断次第で予後決定。",
    # general_med_surg
    "診断に基づく適切な内科的または外科的治療、輸液療法を含む支持療法、疼痛管理、栄養サポート、治療反応の定期的モニタリング。",
    # bacterial_infection
    "培養感受性試験に基づく適切な抗菌薬療法、必要に応じた外科的排膿またはデブリードマン、輸液療法、疼痛管理、治療反応のモニタリング。",
    # parasitic
    "適切な駆虫薬の投与、全ライフサイクルステージをカバーするための反復投薬、環境消毒、脱水・栄養不良に対する支持療法。",
    # viral
    "支持療法を中心に、輸液療法、制吐薬、栄養サポート、二次感染予防の抗菌薬投与。抗ウイルス薬の使用（利用可能な場合）。",
    # cross-species errors (these will be regenerated with proper content)
    "オウム目では稀。インスリン0.05-0.1 IU/羽 q12-24h。低糖・高繊維食。血糖モニタリング。管理困難、予後要注意。",
    "爬虫類では稀。メチマゾール（外挿）。腫瘍は甲状腺摘出。T4モニタリング。予後まずまず。",
    "ブドウ糖浴：5%液×15分（皮膚吸収）。POTZに加温。原因同定。反応回復後に給餌。原因矯正で予後良好。",
    "メトロニダゾール20-25 mg/kg q12h×5-7日。ケージ清掃。予後良好。",
    "確実な治療法なし。アジスロマイシン/パロモマイシン。⚠人獣共通。予後要注意。",
    # other repeats
    "全身性抗真菌薬療法（アゾール系またはアムホテリシンB）、局所抗真菌剤、環境消毒、長期治療中の肝機能モニタリング。",
    "点眼薬（抗菌薬、抗炎症薬、潤滑剤）、疼痛管理、自傷防止、合併症のモニタリング。",
    "麻酔下での歯科処置（トリミング、研磨、必要に応じた抜歯）、疼痛管理、高繊維食への食事変更、定期的な歯科検診。",
    "適切な栄養補助（ビタミン・ミネラルの補充）、食事の見直し、UVBライトの適正化（必要な種）、臨床改善のモニタリング。",
    # short cross-species mismatches
    "ナイスタチン q12h。フルコナゾール（全身性）。飼育管理矯正。予後良好。",
    "局所ミコナゾール。全身イトラコナゾール×4-6週。環境消毒。予後良好。",
    "ビタミンE 10-20 IU/kg q24h。セレン（治療域狭い）。新鮮飼料。予後良好。",
    "鑷子除去。イベルメクチン0.2 mg/kg（14日後反復）。PCV（貧血）モニタリング。予後優良。",
    "餌のガットロードでビオチン補給。B群ビタミン。生卵白回避（アビジン）。皮膚病変。予後良好。",
    "ビタミンK1 2.5-5 mg/kg IM×3-5日。原因同定：殺鼠剤、肝疾患。PTモニタリング。予後良好。",
    "VitD中止。輸液。フロセミド。低Ca食。⚠転移性石灰化。予後要注意。",
    "VitA中止。輸液。中止で回復。予後良好。",
    "レボチロキシン0.02 mg/kg q12-24h。T4モニタリング。予後良好。",
    "瀉血。デフェロキサミン。低鉄食、VitC制限。予後要注意。",
    "Ca+VitD3+UV-B矯正。バランスペレット。変形は永続的（美容的）。予防で予後良好。",
]

TEMPLATES_JA_SET = set(TEMPLATES_JA)


# Template patterns that detect a generic SUFFIX bolted onto otherwise good content.
# These are stripped (not replaced) because the content before them is usually fine.
TEMPLATE_SUFFIXES: list[str] = [
    "代謝・内分泌疾患の治療はホルモン補充療法または過剰ホルモン抑制療法が基本となる。定期的な血中ホルモン濃度測定と臨床症状の評価に基づき投与量を調整する。食事管理、適度な運動、体重管理を併用し、合併症の予防と早期発見のための定期的なモニタリングを継続する。",
]


# Whole-text template patterns matched with regex (more flexible than exact match).
# The pattern is anchored to the disease name + "における" + "の治療は基礎となる..."
# which is mis-applied to many non-endocrine diseases.
TEMPLATE_REGEX_PATTERNS: list[re.Pattern] = [
    # "Xにおける(disease)の治療は基礎となるホルモン・代謝異常を標的とする..." (mis-applied to non-endocrine)
    re.compile(
        r"^[^。]{1,40}における[^。]{1,80}の治療は基礎となるホルモン・代謝異常を標的とする。"
        r"ホルモン補充療法または抑制療法により生理的バランスを回復する。"
        r"食事療法で代謝疾患の栄養面に対処する。"
        r"ホルモンレベル、血糖、電解質、臓器機能マーカーの定期的モニタリングにより用量調整を行う。"
        r"二次的合併症（臓器障害、感染）の併行管理が不可欠である。"
        r"長期または生涯にわたる治療が必要な場合がある。$",
        re.DOTALL,
    ),
    # Variant: "診断による原因同定。診断に基づく種適切な治療..."
    re.compile(
        r"^診断による原因同定。診断に基づく種適切な治療。"
        r"支持療法：適切な温度・水分・栄養維持。"
        r"疼痛管理：メロキシカム0\.2-0\.5 mg/kg q24-48h。"
        r"治療反応モニタリング。"
        r"診断と重症度次第で予後決定。$",
        re.DOTALL,
    ),
    # Neoplasia template (472 instances): "Xにおける(disease)の治療は腫瘍の種類、部位、病期に依存する..."
    re.compile(
        r"^[^。]{1,40}における[^。]{1,80}の治療は腫瘍の種類、部位、病期に依存する。"
        r"アクセス可能な固形腫瘍には十分なマージンを確保した外科的切除が第一選択である。"
        r"全身性腫瘍、不完全切除、転移性疾患には化学療法が適応となりうる。"
        r"放射線療法は局所的な腫瘍制御を提供できる。"
        r"根治療法が困難な場合は疼痛管理、栄養サポート、QOL維持に焦点を当てた緩和ケアを行う。$",
        re.DOTALL,
    ),
    # Nutritional template (57 instances): "Xにおける(disease)の治療は栄養バランスの是正が中心となる..."
    re.compile(
        r"^[^。]{1,40}における[^。]{1,80}の治療は栄養バランスの是正が中心となる。"
        r"欠乏状態では食事の改善または治療的サプリメンテーションにより特定の栄養素を補充する。"
        r"過剰状態では食事制限と臓器障害に対する支持療法を行う。"
        r"栄養不良動物ではリフィーディング症候群予防のため段階的に是正する。"
        r"種特異的な食事要求に基づく長期栄養計画を立案する。"
        r"過不足のない摂取を確保するため定期的に再評価する。$",
        re.DOTALL,
    ),
]

SPECIES_NORM = {
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


def _replacement_for(
    species: str, name_ja: str, name_en: str, en_treatment: str | None, description_ja: str | None
) -> dict:
    """Get the best replacement content. Library first, fallback otherwise."""
    species_norm = SPECIES_NORM.get(species, species)
    # Try curated library
    content = generate_content(species_norm, name_ja, name_en)
    if content:
        return content
    # Use fallback
    return generate_fallback_content(species_norm, name_ja, name_en, en_treatment, description_ja)


def _strip_suffix_templates(text: str) -> tuple[str, bool]:
    """Remove generic suffix templates from text. Returns (new_text, changed)."""
    changed = False
    for suffix in TEMPLATE_SUFFIXES:
        if suffix in text:
            text = text.replace(suffix, "").rstrip()
            # Also strip trailing newlines/whitespace left behind
            text = text.rstrip("\n ")
            changed = True
    return text, changed


def _matches_regex_template(text: str) -> bool:
    """True if the whole text is one of the regex template patterns."""
    if not text:
        return False
    return any(pattern.match(text.strip()) for pattern in TEMPLATE_REGEX_PATTERNS)


def update_json(json_path: Path) -> tuple[int, int, int]:
    """Update diseases_all_species.json in-place. Returns (replaced, suffix_stripped, unchanged)."""
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)
    replaced = 0
    suffix_stripped = 0
    unchanged = 0
    for entry in data:
        tx_ja = entry.get("treatment_ja", "")
        is_exact_template = tx_ja in TEMPLATES_JA_SET
        is_regex_template = _matches_regex_template(tx_ja)
        if is_exact_template or is_regex_template:
            species = entry.get("species", "")
            name = entry.get("name", "")
            name_ja = entry.get("name_ja", "")
            en_tx = entry.get("treatment", "")
            desc_ja = entry.get("description_ja", "")
            replacement = _replacement_for(species, name_ja, name, en_tx, desc_ja)
            entry["treatment_ja"] = replacement["treatment_ja"]
            if replacement.get("treatment") and en_tx != replacement["treatment"]:
                entry["treatment"] = replacement["treatment"]
            if replacement.get("prognosis_ja"):
                entry["prognosis_ja"] = replacement["prognosis_ja"]
            if replacement.get("causes_ja"):
                entry["causes_ja"] = replacement["causes_ja"]
            replaced += 1
        else:
            # Strip suffix templates from otherwise-good content
            new_tx, changed = _strip_suffix_templates(tx_ja)
            if changed:
                entry["treatment_ja"] = new_tx
                suffix_stripped += 1
            else:
                unchanged += 1
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return replaced, suffix_stripped, unchanged


_NAME_BLOCK_RE = re.compile(r'"name":\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.S)
_NAME_JA_BLOCK_RE = re.compile(r'"name_ja":\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.S)
_DESC_JA_BLOCK_RE = re.compile(r'"description_ja":\s*"([^"\\]*(?:\\.[^"\\]*)*)"', re.S)


def _find_entry_metadata(content: str, idx: int) -> dict:
    """Walk backward from a template-treatment match to find the disease metadata."""
    preceding = content[:idx]
    # Find the most recent name field
    names = list(_NAME_BLOCK_RE.finditer(preceding))
    name = names[-1].group(1) if names else ""
    names_ja = list(_NAME_JA_BLOCK_RE.finditer(preceding))
    name_ja = names_ja[-1].group(1) if names_ja else ""
    desc_ja_matches = list(_DESC_JA_BLOCK_RE.finditer(preceding))
    desc_ja = desc_ja_matches[-1].group(1) if desc_ja_matches else ""
    # Find the most recent treatment field (English) for the same entry
    # Look back at most 4 KB to stay in the same entry block
    window = preceding[-4000:]
    tx_match = list(re.finditer(r'"treatment":\s*"([^"\\]*(?:\\.[^"\\]*)*)"', window))
    en_tx = tx_match[-1].group(1) if tx_match else ""

    # Decode \n and \" inside extracted strings
    def _unesc(s: str) -> str:
        return s.encode("utf-8").decode("unicode_escape", errors="replace") if "\\" in s else s

    return {
        "name": _unesc(name),
        "name_ja": _unesc(name_ja),
        "description_ja": _unesc(desc_ja),
        "treatment": _unesc(en_tx),
    }


def _escape_for_python_string(s: str) -> str:
    """Escape a Python string for inclusion inside a Python string literal."""
    # Escape backslashes first, then quotes, then convert real newlines to \n
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def update_python_module(path: Path) -> tuple[int, int]:
    """Update one species *.py module. Returns (replaced, file_changed_bytes_delta)."""
    species_norm = path.stem.replace("_diseases", "")
    text = path.read_text(encoding="utf-8")
    original_len = len(text)
    replaced = 0

    # Process templates in order; replace one at a time to maintain index validity
    for tmpl in TEMPLATES_JA:
        # Build a regex that matches "treatment_ja": "<tmpl>"
        # We need to escape the template for regex
        tmpl_re = re.escape(tmpl)
        pattern = re.compile(r'"treatment_ja":\s*"(' + tmpl_re + r')"')
        while True:
            m = pattern.search(text)
            if not m:
                break
            meta = _find_entry_metadata(text, m.start())
            replacement = _replacement_for(
                species_norm,
                meta["name_ja"],
                meta["name"],
                meta["treatment"],
                meta["description_ja"],
            )
            new_tx_ja = replacement["treatment_ja"]
            new_field = f'"treatment_ja": "{_escape_for_python_string(new_tx_ja)}"'
            text = text[: m.start()] + new_field + text[m.end() :]
            replaced += 1

    # Strip suffix templates from any treatment_ja containing them
    for suffix in TEMPLATE_SUFFIXES:
        escaped = _escape_for_python_string(suffix)
        if escaped in text:
            count = text.count(escaped)
            text = text.replace(escaped, "")
            replaced += count

    # Handle whole-text regex templates by checking ALL "treatment_ja" fields
    # against TEMPLATE_REGEX_PATTERNS. This covers "における...治療は基礎となる",
    # "における...治療は腫瘍の種類", "における...治療は栄養バランス", and
    # "診断による原因同定" — all in one pass.
    treatment_ja_field = re.compile(r'"treatment_ja":\s*"((?:[^"\\]|\\.)*)"')
    # We accumulate edits and apply them in reverse to keep indices valid.
    edits: list[tuple[int, int, str]] = []
    for m in treatment_ja_field.finditer(text):
        body = m.group(1)
        # Python source uses literal UTF-8 strings. Only decode embedded
        # backslash escapes (e.g. \n, \", \\) — DO NOT use unicode_escape on
        # multi-byte UTF-8 bytes (that corrupts Japanese characters).
        if "\\" in body:
            # Manually handle common JSON-style escapes
            decoded = body.replace('\\"', '"').replace("\\n", "\n").replace("\\t", "\t").replace("\\\\", "\\")
        else:
            decoded = body
        if not any(p.match(decoded.strip()) for p in TEMPLATE_REGEX_PATTERNS):
            continue
        meta = _find_entry_metadata(text, m.start())
        replacement = _replacement_for(
            species_norm,
            meta["name_ja"],
            meta["name"],
            meta["treatment"],
            meta["description_ja"],
        )
        new_field = f'"treatment_ja": "{_escape_for_python_string(replacement["treatment_ja"])}"'
        edits.append((m.start(), m.end(), new_field))
    # Apply edits in reverse
    for start, end, new_field in reversed(edits):
        text = text[:start] + new_field + text[end:]
        replaced += 1

    if replaced > 0:
        path.write_text(text, encoding="utf-8")
    return replaced, len(text) - original_len


def main() -> int:
    print("=" * 70)
    print("Template elimination — eradicating generic disease content")
    print("=" * 70)

    json_path = ROOT / "diseases_all_species.json"
    if json_path.exists():
        print(f"\n[1/2] Updating {json_path.name}…")
        replaced, suffix_stripped, unchanged = update_json(json_path)
        print(f"  Replaced: {replaced}  |  Suffix-stripped: {suffix_stripped}  |  Unchanged: {unchanged}")

    print("\n[2/2] Updating Python species modules…")
    total = 0
    species_dir = ROOT / "api" / "species"
    for path in sorted(species_dir.glob("*_diseases.py")):
        replaced, delta = update_python_module(path)
        if replaced > 0:
            print(f"  {path.name}: {replaced} replaced ({delta:+,} bytes)")
        total += replaced
    print(f"  Total Python replacements: {total}")

    print("\nDone. Re-run `python3 scripts/migrate_to_sqlite.py` to refresh SQLite.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
