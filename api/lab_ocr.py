"""Lab report OCR and text parser.

Extracts veterinary blood test values from either:
  - Uploaded images (Tesseract OCR + regex extraction)
  - Pasted text (regex extraction only)

Returns a dict {lab_id: float} compatible with the existing labValuesGrid
input format used throughout VetDict.

Supported lab IDs (must match those in templates/partials/_main_content.html
data-lab attributes):
  bun, creatinine, sdma, phosphorus, alt, alp, ggt, tbil, albumin,
  glucose, cholesterol, amylase, lipase, hct, wbc, platelets,
  sodium, potassium, calcium, t4, crp, usg
"""

from __future__ import annotations

import io
import logging
import re
from typing import Any

logger = logging.getLogger(__name__)


# Lab synonyms map: each lab ID → list of regex-friendly aliases (case-insensitive)
# Patterns must be specific enough to avoid false matches but flexible for OCR errors.
_LAB_PATTERNS: dict[str, list[str]] = {
    # Renal
    "bun": [r"\bBUN\b", r"血中尿素窒素", r"尿素窒素", r"Blood Urea Nitrogen", r"Urea Nitrogen"],
    "creatinine": [r"\bCRE\b", r"\bCr\b", r"クレアチニン", r"Creatinine", r"血清クレアチニン"],
    "sdma": [r"\bSDMA\b", r"対称性ジメチルアルギニン", r"Symmetric.*Dimethylarginine"],
    "phosphorus": [r"\bP\b", r"\bPhos\b", r"リン", r"無機リン", r"Phosphorus", r"Phosphate"],
    # Hepatic
    "alt": [r"\bALT\b", r"\bGPT\b", r"\bSGPT\b", r"アラニンアミノ基転移酵素", r"Alanine\s+aminotransferase"],
    "alp": [r"\bALP\b", r"\bALKP\b", r"アルカリホスファターゼ", r"アルカリフォスファターゼ", r"Alkaline\s+Phosphatase"],
    "ggt": [r"\bGGT\b", r"γ-GTP", r"γGTP", r"γ-GT", r"Gamma\s*Glutamyl"],
    "tbil": [r"T[-_]?Bil\b", r"\bTBIL\b", r"総ビリルビン", r"ビリルビン.*総量", r"Total\s+Bilirubin"],
    "albumin": [r"\bAlb\b", r"アルブミン", r"Albumin"],
    # Metabolic / pancreatic
    "glucose": [r"\bGLU\b", r"\bGlu\b", r"血糖", r"グルコース", r"Glucose", r"Blood\s+Sugar"],
    "cholesterol": [r"\bCHOL\b", r"\bChol\b", r"\bT[-_]?CHO\b", r"コレステロール", r"Cholesterol", r"総コレステロール"],
    "amylase": [r"\bAMY\b", r"アミラーゼ", r"Amylase"],
    "lipase": [r"\bLIP\b", r"リパーゼ", r"Lipase"],
    # Hematology
    "hct": [r"\bHCT\b", r"\bPCV\b", r"\bHt\b", r"ヘマトクリット", r"Hematocrit", r"Packed\s+Cell"],
    "wbc": [r"\bWBC\b", r"白血球(?:数)?", r"White\s+Blood\s+Cell"],
    "platelets": [r"\bPLT\b", r"\bPlat\b", r"血小板(?:数)?", r"Platelets?"],
    # Electrolytes
    "sodium": [r"\bNa\b", r"ナトリウム", r"Sodium"],
    "potassium": [r"\bK\b(?!\w)", r"カリウム", r"Potassium"],
    "calcium": [r"\bCa\b", r"カルシウム", r"Calcium"],
    # Endocrine / inflammation
    "t4": [r"\bT4\b", r"\btT4\b", r"サイロキシン", r"Thyroxine"],
    "crp": [r"\bCRP\b", r"C反応性タンパク", r"C-Reactive\s+Protein"],
    # Urine
    "usg": [r"\bUSG\b", r"\bSG\b(?:\s|=|:)", r"尿比重", r"Urine\s+Specific\s+Gravity"],
}


# Reasonable value range per lab to filter out obvious OCR errors (e.g. "ALT 1500" is plausible, "ALT 99999" is not).
# Used as a SANITY guard, not a clinical reference range.
_LAB_VALUE_BOUNDS: dict[str, tuple[float, float]] = {
    "bun": (0.5, 500.0),
    "creatinine": (0.01, 30.0),
    "sdma": (0.5, 200.0),
    "phosphorus": (0.5, 30.0),
    "alt": (1.0, 10000.0),
    "alp": (1.0, 10000.0),
    "ggt": (0.5, 2000.0),
    "tbil": (0.01, 50.0),
    "albumin": (0.1, 10.0),
    "glucose": (5.0, 1000.0),
    "cholesterol": (10.0, 2000.0),
    "amylase": (10.0, 10000.0),
    "lipase": (5.0, 10000.0),
    "hct": (5.0, 75.0),  # %
    "wbc": (0.1, 200.0),  # ×10³/μL
    "platelets": (1.0, 2000.0),  # ×10³/μL
    "sodium": (100.0, 200.0),
    "potassium": (1.0, 12.0),
    "calcium": (3.0, 25.0),
    "t4": (0.1, 50.0),
    "crp": (0.0, 500.0),
    "usg": (1.0, 1.06),
}


# Built lazily on first use
_COMPILED_PATTERNS: dict[str, re.Pattern] = {}


def _compile_patterns() -> None:
    """Compile each lab ID's regex once."""
    if _COMPILED_PATTERNS:
        return
    for lab_id, aliases in _LAB_PATTERNS.items():
        combined = "|".join(f"(?:{a})" for a in aliases)
        _COMPILED_PATTERNS[lab_id] = re.compile(combined, re.IGNORECASE)


# Value pattern: number with optional decimal, sometimes followed by ↑/↓/H/L flags
_VALUE_PATTERN = re.compile(
    r"(?P<value>\d+(?:[.,]\d+)?)\s*(?:[↑↓HhLl*†‡]?)\s*(?P<unit>mg/dL|U/L|IU/L|mmol/L|mEq/L|µg/dL|μg/dL|ug/dL|g/dL|×?10[³^3]/µL|×?10[³^3]/μL|×?10[³^3]/uL|/μL|/uL|/[mu]L|%|ng/mL|pg/mL)?",
)


def parse_lab_text(text: str) -> dict[str, dict[str, Any]]:
    """Parse free-form lab report text → {lab_id: {value, unit, raw}}.

    For each line / segment in the text, finds the closest number after a
    lab name keyword. The number is sanity-checked against typical clinical
    ranges to reject OCR garbage.
    """
    if not text:
        return {}
    _compile_patterns()
    results: dict[str, dict[str, Any]] = {}
    # Normalize: split on newlines first (lab reports are line-oriented)
    # and on common delimiters within lines.
    lines = re.split(r"[\r\n]+", text)
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # For each lab ID, check if any of its aliases appears in this line
        for lab_id, pat in _COMPILED_PATTERNS.items():
            if lab_id in results:
                continue  # already found
            m = pat.search(line)
            if not m:
                continue
            # Look for a number IMMEDIATELY AFTER the matched alias
            tail = line[m.end() :]
            vm = _VALUE_PATTERN.search(tail)
            if not vm:
                continue
            raw_value = vm.group("value").replace(",", "")
            try:
                value = float(raw_value)
            except ValueError:
                continue
            # Sanity bounds check
            lo, hi = _LAB_VALUE_BOUNDS.get(lab_id, (0.0, 1e9))
            if not (lo <= value <= hi):
                continue
            results[lab_id] = {
                "value": value,
                "unit": (vm.group("unit") or "").strip(),
                "raw_line": line[:200],
            }
    return results


def ocr_image_to_text(image_bytes: bytes, *, lang: str = "jpn+eng") -> tuple[str, dict[str, Any]]:
    """Run Tesseract OCR on an image. Returns (text, meta).

    If pytesseract or tesseract binary is unavailable, raises RuntimeError.
    """
    try:
        import pytesseract  # noqa: PLC0415
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(f"OCR dependencies missing: {exc}") from exc

    try:
        img = Image.open(io.BytesIO(image_bytes))
        # Convert to grayscale to improve OCR
        if img.mode != "L":
            img = img.convert("L")
        # Resize tiny images for better OCR (target ~1500px on longest side)
        max_dim = max(img.size)
        if max_dim < 1200:
            scale = 1500 / max_dim
            new_size = (int(img.size[0] * scale), int(img.size[1] * scale))
            img = img.resize(new_size, Image.LANCZOS)
        text = pytesseract.image_to_string(img, lang=lang, config="--psm 6")
    except pytesseract.TesseractNotFoundError as exc:
        raise RuntimeError("Tesseract binary not installed on server") from exc
    except Exception as exc:  # noqa: BLE001 — surface OCR failure
        raise RuntimeError(f"OCR failed: {exc}") from exc

    meta = {
        "image_size": img.size if "img" in locals() else None,
        "text_length": len(text),
        "ocr_lang": lang,
    }
    return text, meta


def extract_labs_from_image(image_bytes: bytes, *, lang: str = "jpn+eng") -> dict[str, Any]:
    """End-to-end: image → OCR → parsed lab values.

    Returns:
        {
          "labs": {lab_id: {value, unit, raw_line}},
          "ocr_text": str,
          "meta": {image_size, text_length, ocr_lang, count},
        }
    """
    text, meta = ocr_image_to_text(image_bytes, lang=lang)
    labs = parse_lab_text(text)
    meta["count"] = len(labs)
    return {"labs": labs, "ocr_text": text, "meta": meta}
