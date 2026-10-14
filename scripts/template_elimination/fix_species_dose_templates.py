"""Fix species-inappropriate dose templates in disease treatment text.

2026-10 監査で、汎用テンプレートが種を問わず同一の用量文を埋め込んでいた2系統を検出:

1. 筋骨格系フォールバック: 「メロキシカム 0.2-0.5 mg/kg PO q24h（小型哺乳類）または
   0.1-0.2 mg/kg q24h（馬は1.7 mg/kg q24h）」— 猫（0.05→0.01-0.03 mg/kg）では約10倍の
   過量、馬のメロキシカムは 0.6 mg/kg（1.7 mg/kg は根拠のない値）。
   英語側の「【Small Mammal Arthritis/Spondylosis/...】」テンプレートも猫・爬虫類・鳥に誤適用。
2. 犬猫の支持療法ブロック「ショック時 90 mL/kg初期ボーラス」— 旧来の「全血液量」ボーラスで、
   現行は少量反復ボーラス＋再評価（AAHA/AAFP 2013）。猫は容量過負荷・胸水に脆弱。

Usage:
    python3 scripts/template_elimination/fix_species_dose_templates.py [--apply]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.fallback_generator import meloxicam_line_ja  # noqa: E402
from scripts.template_elimination.template_content_library import SHOCK_FLUID_JA  # noqa: E402

OLD_MELOX_JA = "鎮痛: メロキシカム 0.2-0.5 mg/kg PO q24h（小型哺乳類）または0.1-0.2 mg/kg q24h（馬は1.7 mg/kg q24h）。"
OLD_MELOX_HINT_JA = "具体的な薬剤目安: meloxicam 0.2-0.5 mg/kg PO。"
OLD_SHOCK_JA = "輸液（晶質液 60-80 mL/kg/日 IV、ショック時 90 mL/kg初期ボーラス）、"

SMALL_MAMMALS = {
    "rabbit",
    "guinea_pig",
    "chinchilla",
    "hamster",
    "degu",
    "ferret",
    "hedgehog",
    "sugar_glider",
    "exotic_other",
}

JSON_SPECIES = {
    "Dog": "dog",
    "Cat": "cat",
    "Horse": "horse",
    "Rabbit": "rabbit",
    "Guinea Pig": "guinea_pig",
    "Chinchilla": "chinchilla",
    "Hamster": "hamster",
    "Degu": "degu",
    "Ferret": "ferret",
    "Hedgehog": "hedgehog",
    "Sugar Glider": "sugar_glider",
    "Bird": "bird",
    "Parakeet": "parakeet",
    "Parrot": "parrot",
    "Reptile": "reptile",
    "Lizard": "lizard",
    "Snake": "snake",
    "Tortoise": "tortoise",
    "Amphibian": "amphibian",
    "Fish": "fish",
    "Exotic Other": "exotic_other",
}
MODULE_SPECIES = {"equine": "horse"}

MELOX_EN = {
    "cat": "meloxicam 0.05 mg/kg PO once, then 0.01-0.03 mg/kg PO q24h (lowest effective dose; monitor renal function and hydration — ISFM/AAFP 2010)",
    "dog": "meloxicam 0.2 mg/kg PO once, then 0.1 mg/kg PO q24h",
    "horse": "meloxicam 0.6 mg/kg PO q24h",
    "bird": "meloxicam 1.0-1.6 mg/kg PO q12-24h (Cole 2009; Carpenter 6th)",
    "reptile": "meloxicam 0.2-0.4 mg/kg PO/IM q24-48h (Carpenter 6th)",
    "amphibian": "meloxicam 0.2-0.4 mg/kg PO q24h (limited data — Carpenter 6th)",
}
_EN_GROUP = {"parakeet": "bird", "parrot": "bird", "lizard": "reptile", "snake": "reptile", "tortoise": "reptile"}
_EN_LABEL = {
    "cat": "Feline",
    "dog": "Canine",
    "horse": "Equine",
    "bird": "Avian",
    "parakeet": "Avian",
    "parrot": "Avian",
    "reptile": "Reptile",
    "lizard": "Reptile",
    "snake": "Reptile",
    "tortoise": "Chelonian",
    "amphibian": "Amphibian",
}
_MELOX_EN_RE = re.compile(r"meloxicam 0\.2-0\.5 mg/kg PO q24h")

# Curated replacement where the module itself has no usable text.
CURATED_EN = {
    ("cat", "Feline Struvite Urolithiasis"): (
        "Sterile struvite uroliths in cats are usually dissolvable: feed a calculolytic diet "
        "(therapeutic urinary dissolution diet) exclusively and recheck radiographs every 2-4 weeks — "
        "most dissolve within 2-4 weeks (ACVIM consensus, Lulich et al. JVIM 2016). Increase water "
        "intake (wet food, fountains). Antimicrobials only when urine culture confirms UTI. If urethral "
        "obstruction: emergency decompression, correct hyperkalemia, urethral catheterization; "
        "cystotomy only for non-dissolvable/obstructive uroliths. Prevent recurrence with a "
        "struvite-prevention diet and urine SG < 1.030."
    ),
}


def _en_species(sp: str) -> str:
    return _EN_GROUP.get(sp, sp)


def fix_ja(text: str, sp: str) -> str:
    if not text:
        return text
    out = text.replace(OLD_MELOX_JA, meloxicam_line_ja(sp))
    if sp not in SMALL_MAMMALS:
        out = out.replace(OLD_MELOX_HINT_JA + "\n", "").replace(OLD_MELOX_HINT_JA, "")
    if sp in SHOCK_FLUID_JA:
        out = out.replace(OLD_SHOCK_JA, SHOCK_FLUID_JA[sp])
    return out


def _strip_ecvn(text: str) -> str:
    return text.split("[ECVN:Block]")[0].rstrip()


def fix_en(text: str, sp: str, module_text: str | None, name: str) -> str:
    if not text or sp in SMALL_MAMMALS or not text.startswith("【Small Mammal"):
        return text
    if (sp, name) in CURATED_EN:
        return CURATED_EN[(sp, name)]
    if module_text:
        mt = _strip_ecvn(module_text)
        if len(mt) >= 80 and not mt.startswith("【Small Mammal"):
            return mt
    esp = _en_species(sp)
    out = text.replace("【Small Mammal", "【" + _EN_LABEL.get(sp, "Exotic"), 1)
    if esp in MELOX_EN:
        out = _MELOX_EN_RE.sub(MELOX_EN[esp], out)
    # Remove rabbit-specific asides that don't apply to the species.
    out = out.replace(" Rabbits→vertebral fracture common (low bone density).", "")
    return out


def _module_treatments() -> dict[tuple[str, str], str]:
    import importlib

    res: dict[tuple[str, str], str] = {}
    for f in sorted((ROOT / "api" / "species").glob("*_diseases.py")):
        stem = f.stem[: -len("_diseases")]
        sp = MODULE_SPECIES.get(stem, stem)
        try:
            mod = importlib.import_module(f"api.species.{f.stem}")
        except Exception:
            continue
        for d in getattr(mod, "DISEASES", []) or []:
            if isinstance(d, dict) and d.get("treatment"):
                res[(sp, d.get("name", ""))] = d["treatment"]
    return res


def main(apply: bool) -> None:
    path = ROOT / "diseases_all_species.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    mods = _module_treatments()
    n_ja = n_en = 0
    for x in data:
        sp = JSON_SPECIES.get(x.get("species", ""))
        if not sp:
            continue
        for fld in ("treatment_ja", "prognosis_ja", "prevention_ja"):
            new = fix_ja(x.get(fld) or "", sp)
            if new != (x.get(fld) or ""):
                x[fld] = new
                n_ja += 1
        new = fix_en(x.get("treatment") or "", sp, mods.get((sp, x.get("name", ""))), x.get("name", ""))
        if new != (x.get("treatment") or ""):
            x["treatment"] = new
            n_en += 1
    print(f"JSON: JA fields fixed={n_ja}, EN treatment fixed={n_en}")

    n_mod = 0
    for f in sorted((ROOT / "api" / "species").glob("*_diseases.py")):
        stem = f.stem[: -len("_diseases")]
        sp = MODULE_SPECIES.get(stem, stem)
        src = f.read_text(encoding="utf-8")
        new = src.replace(OLD_MELOX_JA, meloxicam_line_ja(sp))
        if sp not in SMALL_MAMMALS:
            new = new.replace(OLD_MELOX_HINT_JA + "\\n", "").replace(OLD_MELOX_HINT_JA, "")
        if sp in SHOCK_FLUID_JA:
            new = new.replace(OLD_SHOCK_JA, SHOCK_FLUID_JA[sp])
        if new != src:
            n_mod += 1
            if apply:
                f.write_text(new, encoding="utf-8")
    print(f"species modules changed: {n_mod}")

    supp = ROOT / "api" / "data" / "supplementary_diseases.json"
    if supp.exists():
        raw = supp.read_text(encoding="utf-8")
        hits = raw.count(OLD_MELOX_JA) + raw.count(OLD_SHOCK_JA)
        print(f"supplementary occurrences (species-agnostic, reported only): {hits}")

    if apply:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))


if __name__ == "__main__":
    main("--apply" in sys.argv)
