"""Tests for lab report text/OCR parser (api/lab_ocr.py).

Image OCR (Tesseract) is exercised only when the binary is available;
text parsing is always exercised because it has no external deps.
"""

from __future__ import annotations

import pytest

from api.lab_ocr import parse_lab_text


# ---------------------------------------------------------------------------
# Text parsing — Japanese
# ---------------------------------------------------------------------------
def test_parse_japanese_lab_report():
    text = """
    BUN  45 mg/dL
    クレアチニン  3.2 mg/dL
    ALT  220 U/L
    ALP  450 U/L
    総ビリルビン  0.8 mg/dL
    アルブミン  2.4 g/dL
    血糖  180 mg/dL
    ナトリウム  148 mEq/L
    カリウム  5.6 mEq/L
    ヘマトクリット  28 %
    """
    labs = parse_lab_text(text)
    assert labs["bun"]["value"] == 45
    assert labs["creatinine"]["value"] == 3.2
    assert labs["alt"]["value"] == 220
    assert labs["alp"]["value"] == 450
    assert labs["tbil"]["value"] == 0.8
    assert labs["albumin"]["value"] == 2.4
    assert labs["glucose"]["value"] == 180
    assert labs["sodium"]["value"] == 148
    assert labs["potassium"]["value"] == 5.6
    assert labs["hct"]["value"] == 28


def test_parse_english_lab_report():
    text = """
    Creatinine 4.5 mg/dL
    BUN 80 mg/dL
    Phosphorus 7.2 mg/dL
    Total Bilirubin 1.2 mg/dL
    Glucose 95 mg/dL
    """
    labs = parse_lab_text(text)
    assert labs["creatinine"]["value"] == 4.5
    assert labs["bun"]["value"] == 80
    assert labs["phosphorus"]["value"] == 7.2
    assert labs["tbil"]["value"] == 1.2
    assert labs["glucose"]["value"] == 95


def test_empty_and_garbage_input():
    assert parse_lab_text("") == {}
    assert parse_lab_text("no labs here") == {}
    # Numbers without a recognized label should be ignored
    assert parse_lab_text("42 99 100") == {}


def test_value_sanity_bounds_reject_garbage():
    # ALT of 999999 is clearly OCR garbage — should be rejected
    labs = parse_lab_text("ALT 999999 U/L\nBUN 50 mg/dL")
    assert "alt" not in labs
    assert labs["bun"]["value"] == 50


def test_unit_capture():
    labs = parse_lab_text("BUN 45 mg/dL\nALT 220 U/L")
    assert labs["bun"]["unit"] == "mg/dL"
    assert labs["alt"]["unit"] == "U/L"


def test_first_occurrence_wins():
    # If a lab appears twice, the first valid value is taken
    labs = parse_lab_text("BUN 25 mg/dL\nBUN 200 mg/dL")
    assert labs["bun"]["value"] == 25


def test_thousands_separator_stripped():
    # Commas are treated as thousands separators (US/JP convention).
    # "1,200" → 1200; "1.8" decimal point preserved.
    labs = parse_lab_text("Cholesterol 1,200 mg/dL\nCreatinine 1.8 mg/dL")
    assert labs["cholesterol"]["value"] == 1200
    assert labs["creatinine"]["value"] == 1.8


# ---------------------------------------------------------------------------
# Image OCR — skipped if Tesseract binary unavailable
# ---------------------------------------------------------------------------
def _tesseract_available() -> bool:
    try:
        import pytesseract  # noqa: PLC0415

        pytesseract.get_tesseract_version()
        return True
    except Exception:  # noqa: BLE001
        return False


@pytest.mark.skipif(not _tesseract_available(), reason="Tesseract not installed")
def test_extract_labs_from_synthetic_image():
    """Render a simple lab report as PNG, then OCR it back."""
    from io import BytesIO

    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", (700, 400), "white")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
    except OSError:
        font = ImageFont.load_default()
    lines = [
        "BUN     45  mg/dL",
        "Cr       3.2 mg/dL",
        "ALT     220 U/L",
        "Glucose 180 mg/dL",
    ]
    for i, line in enumerate(lines):
        d.text((30, 30 + i * 50), line, fill="black", font=font)
    buf = BytesIO()
    img.save(buf, format="PNG")

    from api.lab_ocr import extract_labs_from_image

    result = extract_labs_from_image(buf.getvalue(), lang="eng")
    labs = result["labs"]
    # We expect at least 3 of the 4 to come back (OCR tolerance)
    found = sum(1 for k in ("bun", "creatinine", "alt", "glucose") if k in labs)
    assert found >= 3, f"OCR only extracted {found}/4 labs: {list(labs)}"


# ---------------------------------------------------------------------------
# Flask endpoints
# ---------------------------------------------------------------------------
def test_api_lab_parse_text_endpoint():
    from api.vetdict_api import app

    client = app.test_client()
    r = client.post("/api/lab-ocr/text", json={"text": "BUN 45 mg/dL\nALT 220 U/L"})
    assert r.status_code == 200
    body = r.get_json()
    assert body["count"] >= 2
    assert body["labs"]["bun"]["value"] == 45


def test_api_lab_parse_text_rejects_missing_text():
    from api.vetdict_api import app

    client = app.test_client()
    r = client.post("/api/lab-ocr/text", json={})
    assert r.status_code == 400


def test_api_lab_parse_image_requires_payload():
    from api.vetdict_api import app

    client = app.test_client()
    r = client.post("/api/lab-ocr/image", json={})
    assert r.status_code == 400
