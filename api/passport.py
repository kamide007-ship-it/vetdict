"""
International Pet Passport & Health Report PDF Generator v1.0

Generates two types of professional A4 PDF documents:
  1. International Pet Passport — owner info, animal ID, vaccinations,
     deworming, clinical exam, travel info, veterinary oath
  2. Health Report — symptom analysis, matched diseases, diagnostic tests,
     genetic test recommendations

Blueprint: passport_bp  (url_prefix="/api/passport")
"""

import io
import logging
from datetime import datetime

from flask import Blueprint, jsonify, request, send_file

# ---------------------------------------------------------------------------
# reportlab imports
# ---------------------------------------------------------------------------
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

logger = logging.getLogger(__name__)

# =============================================================================
# CJK Font Registration
# =============================================================================
# Register CJK fonts so that Japanese / Chinese / Korean characters render
# correctly and do not produce mojibake.  HeiseiKakuGo-W5 (Gothic / sans-serif)
# is used for headings and HeiseiMin-W3 (Mincho / serif) for body text.
# These are built-in CID fonts shipped with reportlab — no external .ttf needed.

_CJK_FONTS_REGISTERED = False


def _register_cjk_fonts():
    """Register CJK CID fonts once (idempotent)."""
    global _CJK_FONTS_REGISTERED
    if _CJK_FONTS_REGISTERED:
        return
    try:
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
        pdfmetrics.registerFont(UnicodeCIDFont("HeiseiMin-W3"))
        _CJK_FONTS_REGISTERED = True
        logger.info("CJK CID fonts registered (HeiseiKakuGo-W5, HeiseiMin-W3)")
    except Exception as exc:
        logger.warning(f"CJK font registration failed: {exc}; "
                       "PDF output may show mojibake for CJK characters")


# =============================================================================
# Shared style helpers
# =============================================================================

# Font family names — fall back to Helvetica if CJK registration failed.
FONT_GOTHIC = "HeiseiKakuGo-W5"
FONT_MINCHO = "HeiseiMin-W3"
FONT_FALLBACK = "Helvetica"
FONT_FALLBACK_BOLD = "Helvetica-Bold"

PAGE_WIDTH, PAGE_HEIGHT = A4  # 595.27pt x 841.89pt (210mm x 297mm)
MARGIN = 18 * mm


def _safe_font(preferred: str) -> str:
    """Return *preferred* if registered, otherwise the latin fallback."""
    if _CJK_FONTS_REGISTERED:
        return preferred
    return FONT_FALLBACK


def _safe_font_bold() -> str:
    if _CJK_FONTS_REGISTERED:
        return FONT_GOTHIC
    return FONT_FALLBACK_BOLD


def _build_styles():
    """Build a dictionary of ParagraphStyle objects used across both PDFs."""
    base = getSampleStyleSheet()
    gothic = _safe_font(FONT_GOTHIC)
    mincho = _safe_font(FONT_MINCHO)
    bold = _safe_font_bold()

    styles = {
        "title": ParagraphStyle(
            "PassportTitle",
            parent=base["Title"],
            fontName=bold,
            fontSize=20,
            leading=26,
            alignment=TA_CENTER,
            spaceAfter=4 * mm,
            textColor=colors.HexColor("#1a237e"),
        ),
        "subtitle": ParagraphStyle(
            "PassportSubtitle",
            parent=base["Normal"],
            fontName=gothic,
            fontSize=11,
            leading=15,
            alignment=TA_CENTER,
            spaceAfter=6 * mm,
            textColor=colors.HexColor("#37474f"),
        ),
        "section_header": ParagraphStyle(
            "SectionHeader",
            parent=base["Heading2"],
            fontName=bold,
            fontSize=13,
            leading=17,
            spaceBefore=5 * mm,
            spaceAfter=2 * mm,
            textColor=colors.white,
        ),
        "field_label": ParagraphStyle(
            "FieldLabel",
            parent=base["Normal"],
            fontName=bold,
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#546e7a"),
        ),
        "field_value": ParagraphStyle(
            "FieldValue",
            parent=base["Normal"],
            fontName=mincho,
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#212121"),
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName=mincho,
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#212121"),
        ),
        "body_small": ParagraphStyle(
            "BodySmall",
            parent=base["Normal"],
            fontName=mincho,
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#616161"),
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=base["Normal"],
            fontName=bold,
            fontSize=8,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.white,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            parent=base["Normal"],
            fontName=mincho,
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#212121"),
        ),
        "table_cell_center": ParagraphStyle(
            "TableCellCenter",
            parent=base["Normal"],
            fontName=mincho,
            fontSize=8,
            leading=11,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#212121"),
        ),
        "disclaimer": ParagraphStyle(
            "Disclaimer",
            parent=base["Normal"],
            fontName=mincho,
            fontSize=7,
            leading=10,
            textColor=colors.HexColor("#9e9e9e"),
        ),
        "oath": ParagraphStyle(
            "Oath",
            parent=base["Normal"],
            fontName=mincho,
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#37474f"),
            alignment=TA_LEFT,
        ),
        "severity_high": ParagraphStyle(
            "SeverityHigh",
            parent=base["Normal"],
            fontName=bold,
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#c62828"),
        ),
        "severity_medium": ParagraphStyle(
            "SeverityMedium",
            parent=base["Normal"],
            fontName=bold,
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#ef6c00"),
        ),
        "severity_low": ParagraphStyle(
            "SeverityLow",
            parent=base["Normal"],
            fontName=bold,
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#2e7d32"),
        ),
    }
    return styles


# ---------------------------------------------------------------------------
# Reusable drawing components
# ---------------------------------------------------------------------------

# Standard colours used in both PDFs
COLOR_PRIMARY = colors.HexColor("#1a237e")      # Deep indigo
COLOR_SECONDARY = colors.HexColor("#283593")     # Medium indigo
COLOR_ACCENT = colors.HexColor("#3949ab")        # Lighter indigo
COLOR_BG_LIGHT = colors.HexColor("#e8eaf6")      # Very light indigo
COLOR_BG_ROW = colors.HexColor("#f5f5f5")        # Alternating row grey
COLOR_BORDER = colors.HexColor("#bdbdbd")        # Table border grey
COLOR_WHITE = colors.white


def _section_banner(title: str, styles: dict) -> Table:
    """Return a coloured banner bar that acts as a section header."""
    para = Paragraph(title, styles["section_header"])
    tbl = Table([[para]], colWidths=[PAGE_WIDTH - 2 * MARGIN])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOR_SECONDARY),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [3, 3, 3, 3]),
    ]))
    return tbl


def _field_pair_table(pairs: list, styles: dict, col_count: int = 2) -> Table:
    """Build a two- or multi-column label/value grid.

    *pairs* is a flat list of (label, value) tuples.  They are laid out in
    *col_count* columns per row.
    """
    rows = []
    row = []
    for i, (label, value) in enumerate(pairs):
        row.append(Paragraph(f"<b>{label}</b>", styles["field_label"]))
        row.append(Paragraph(str(value) if value else "—", styles["field_value"]))
        if (i + 1) % col_count == 0:
            rows.append(row)
            row = []
    if row:
        # pad remaining cells
        while len(row) < col_count * 2:
            row.append(Paragraph("", styles["field_value"]))
        rows.append(row)

    if not rows:
        return Spacer(1, 0)

    available = PAGE_WIDTH - 2 * MARGIN
    label_w = 30 * mm
    value_w = (available - label_w * col_count) / col_count
    col_widths = []
    for _ in range(col_count):
        col_widths.extend([label_w, value_w])

    tbl = Table(rows, colWidths=col_widths)
    style_cmds = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, COLOR_BG_LIGHT),
    ]
    tbl.setStyle(TableStyle(style_cmds))
    return tbl


def _page_border(canvas, doc):
    """Draw a professional double-line border and footer on every page."""
    canvas.saveState()

    # Outer border
    canvas.setStrokeColor(COLOR_PRIMARY)
    canvas.setLineWidth(2)
    canvas.rect(
        MARGIN - 4 * mm, MARGIN - 4 * mm,
        PAGE_WIDTH - 2 * MARGIN + 8 * mm,
        PAGE_HEIGHT - 2 * MARGIN + 8 * mm,
    )

    # Inner border
    canvas.setStrokeColor(COLOR_ACCENT)
    canvas.setLineWidth(0.5)
    canvas.rect(
        MARGIN - 2 * mm, MARGIN - 2 * mm,
        PAGE_WIDTH - 2 * MARGIN + 4 * mm,
        PAGE_HEIGHT - 2 * MARGIN + 4 * mm,
    )

    # Footer
    canvas.setFont(_safe_font(FONT_MINCHO), 7)
    canvas.setFillColor(colors.HexColor("#9e9e9e"))
    footer_y = MARGIN - 2 * mm - 2
    canvas.drawCentredString(
        PAGE_WIDTH / 2, footer_y,
        f"Page {doc.page}  |  Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  ShowDog Analysis Platform"
    )
    canvas.restoreState()


# =============================================================================
# Blueprint
# =============================================================================

passport_bp = Blueprint("passport", __name__, url_prefix="/api/passport")


# =============================================================================
# Endpoint 1 — International Pet Passport PDF
# =============================================================================

@passport_bp.route("/generate", methods=["POST"])
def generate_passport():
    """POST /api/passport/generate

    Accept JSON with all pet passport data, return a professionally
    formatted A4 PDF (Content-Type: application/pdf).

    Expected JSON fields (all optional — missing fields produce "—"):
        owner:  {name, address, phone, email}
        animal: {species, breed, name, sex, date_of_birth, color,
                 microchip_number}
        vaccinations: [{vaccine_name, date, batch_number, valid_until,
                        vet_name}, ...]
        deworming: [{product, date, vet}, ...]
        clinical_exam: {date, findings, vet}
        travel: {destination, departure_date, entry_permit_number}
        issued_date: str  (defaults to today)
        passport_number: str
    """
    _register_cjk_fonts()
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    try:
        pdf_bytes = _build_passport_pdf(data)
    except Exception as exc:
        logger.error(f"Passport PDF generation failed: {exc}", exc_info=True)
        return jsonify({"error": f"PDF generation failed: {str(exc)}"}), 500

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"pet_passport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    )


def _build_passport_pdf(data: dict) -> bytes:
    """Compose the full International Pet Passport and return raw PDF bytes."""
    styles = _build_styles()
    buf = io.BytesIO()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + 2 * mm,
        bottomMargin=MARGIN + 2 * mm,
        title="International Pet Passport",
        author="ShowDog Analysis Platform",
    )

    story = []

    # ---- Title block ----
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("INTERNATIONAL PET PASSPORT", styles["title"]))
    passport_number = data.get("passport_number", "")
    issued = data.get("issued_date", datetime.now().strftime("%Y-%m-%d"))
    story.append(Paragraph(
        f"Passport No: {passport_number or '—'}  |  Date of Issue: {issued}",
        styles["subtitle"],
    ))
    story.append(HRFlowable(
        width="100%", thickness=1, color=COLOR_PRIMARY,
        spaceAfter=4 * mm, spaceBefore=1 * mm,
    ))

    # ---- Section 1: Owner Information ----
    owner = data.get("owner", {})
    story.append(_section_banner("I.  OWNER INFORMATION", styles))
    story.append(Spacer(1, 2 * mm))
    story.append(_field_pair_table([
        ("Name", owner.get("name")),
        ("Phone", owner.get("phone")),
        ("Address", owner.get("address")),
        ("Email", owner.get("email")),
    ], styles, col_count=2))
    story.append(Spacer(1, 3 * mm))

    # ---- Section 2: Animal Identification ----
    animal = data.get("animal", {})
    story.append(_section_banner("II.  ANIMAL IDENTIFICATION", styles))
    story.append(Spacer(1, 2 * mm))
    story.append(_field_pair_table([
        ("Species", animal.get("species")),
        ("Breed", animal.get("breed")),
        ("Name", animal.get("name")),
        ("Sex", animal.get("sex")),
        ("Date of Birth", animal.get("date_of_birth")),
        ("Color / Markings", animal.get("color")),
        ("Microchip No.", animal.get("microchip_number")),
    ], styles, col_count=2))
    story.append(Spacer(1, 3 * mm))

    # ---- Section 3: Vaccination Records ----
    vaccinations = data.get("vaccinations", [])
    story.append(_section_banner("III.  VACCINATION RECORDS", styles))
    story.append(Spacer(1, 2 * mm))

    if vaccinations:
        header_row = [
            Paragraph("Vaccine", styles["table_header"]),
            Paragraph("Date", styles["table_header"]),
            Paragraph("Batch No.", styles["table_header"]),
            Paragraph("Valid Until", styles["table_header"]),
            Paragraph("Veterinarian", styles["table_header"]),
        ]
        table_data = [header_row]
        for v in vaccinations:
            table_data.append([
                Paragraph(str(v.get("vaccine_name", "—")), styles["table_cell"]),
                Paragraph(str(v.get("date", "—")), styles["table_cell_center"]),
                Paragraph(str(v.get("batch_number", "—")), styles["table_cell_center"]),
                Paragraph(str(v.get("valid_until", "—")), styles["table_cell_center"]),
                Paragraph(str(v.get("vet_name", "—")), styles["table_cell"]),
            ])

        avail = PAGE_WIDTH - 2 * MARGIN
        col_ws = [avail * 0.25, avail * 0.15, avail * 0.18, avail * 0.17, avail * 0.25]
        vax_table = Table(table_data, colWidths=col_ws, repeatRows=1)
        vax_style = [
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_SECONDARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_WHITE),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_WHITE, COLOR_BG_ROW]),
        ]
        vax_table.setStyle(TableStyle(vax_style))
        story.append(vax_table)
    else:
        story.append(Paragraph("No vaccination records provided.", styles["body_small"]))

    story.append(Spacer(1, 3 * mm))

    # ---- Section 4: Deworming / Parasite Treatment ----
    deworming = data.get("deworming", [])
    story.append(_section_banner("IV.  DEWORMING / PARASITE TREATMENT", styles))
    story.append(Spacer(1, 2 * mm))

    if deworming:
        dw_header = [
            Paragraph("Product", styles["table_header"]),
            Paragraph("Date", styles["table_header"]),
            Paragraph("Veterinarian", styles["table_header"]),
        ]
        dw_data = [dw_header]
        for d in deworming:
            dw_data.append([
                Paragraph(str(d.get("product", "—")), styles["table_cell"]),
                Paragraph(str(d.get("date", "—")), styles["table_cell_center"]),
                Paragraph(str(d.get("vet", "—")), styles["table_cell"]),
            ])

        avail = PAGE_WIDTH - 2 * MARGIN
        dw_col_ws = [avail * 0.40, avail * 0.25, avail * 0.35]
        dw_table = Table(dw_data, colWidths=dw_col_ws, repeatRows=1)
        dw_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_SECONDARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_WHITE),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_WHITE, COLOR_BG_ROW]),
        ]))
        story.append(dw_table)
    else:
        story.append(Paragraph("No deworming records provided.", styles["body_small"]))

    story.append(Spacer(1, 3 * mm))

    # ---- Section 5: Clinical Examination ----
    exam = data.get("clinical_exam", {})
    story.append(_section_banner("V.  CLINICAL EXAMINATION", styles))
    story.append(Spacer(1, 2 * mm))
    story.append(_field_pair_table([
        ("Examination Date", exam.get("date")),
        ("Veterinarian", exam.get("vet")),
    ], styles, col_count=2))
    story.append(Spacer(1, 1 * mm))
    findings_text = exam.get("findings", "No findings recorded.")
    story.append(Paragraph(f"<b>Findings:</b>  {findings_text}", styles["body"]))
    story.append(Spacer(1, 3 * mm))

    # ---- Section 6: Travel Information ----
    travel = data.get("travel", {})
    story.append(_section_banner("VI.  TRAVEL INFORMATION", styles))
    story.append(Spacer(1, 2 * mm))
    story.append(_field_pair_table([
        ("Destination", travel.get("destination")),
        ("Departure Date", travel.get("departure_date")),
        ("Entry Permit No.", travel.get("entry_permit_number")),
    ], styles, col_count=2))
    story.append(Spacer(1, 5 * mm))

    # ---- Section 7: Veterinary Oath / Certification ----
    story.append(_section_banner("VII.  VETERINARY CERTIFICATION", styles))
    story.append(Spacer(1, 3 * mm))

    oath_text = (
        "I, the undersigned veterinarian, hereby certify that I have examined "
        "the animal described above and that the information recorded in this "
        "passport is accurate and complete to the best of my professional "
        "knowledge.  The animal is, in my opinion, fit for travel and free "
        "from clinical signs of infectious or contagious disease."
    )
    story.append(Paragraph(oath_text, styles["oath"]))
    story.append(Spacer(1, 8 * mm))

    # Signature / stamp area
    sig_data = [
        [
            Paragraph("Veterinarian Signature", styles["field_label"]),
            Paragraph("", styles["body"]),
            Paragraph("Official Stamp", styles["field_label"]),
            Paragraph("", styles["body"]),
        ],
        [
            Paragraph("", styles["body"]),
            Paragraph("", styles["body"]),
            Paragraph("", styles["body"]),
            Paragraph("", styles["body"]),
        ],
        [
            Paragraph("Name (print)", styles["field_label"]),
            Paragraph("", styles["body"]),
            Paragraph("Date", styles["field_label"]),
            Paragraph("", styles["body"]),
        ],
    ]
    avail = PAGE_WIDTH - 2 * MARGIN
    sig_table = Table(sig_data, colWidths=[28 * mm, avail * 0.35 - 28 * mm,
                                            28 * mm, avail * 0.65 - 28 * mm])
    sig_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        # Signature line
        ("LINEBELOW", (1, 1), (1, 1), 0.8, colors.black),
        # Stamp box
        ("BOX", (3, 0), (3, 1), 1, COLOR_BORDER),
        ("BACKGROUND", (3, 0), (3, 1), COLOR_BG_LIGHT),
        # Name / Date lines
        ("LINEBELOW", (1, 2), (1, 2), 0.5, colors.black),
        ("LINEBELOW", (3, 2), (3, 2), 0.5, colors.black),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 5 * mm))

    # Disclaimer
    story.append(HRFlowable(
        width="100%", thickness=0.5, color=COLOR_BORDER,
        spaceAfter=2 * mm, spaceBefore=2 * mm,
    ))
    story.append(Paragraph(
        "This document is generated by ShowDog Analysis Platform for informational "
        "purposes.  It should be validated and signed by a licensed veterinarian "
        "before being used for official travel or regulatory submissions.",
        styles["disclaimer"],
    ))

    # Build
    doc.build(story, onFirstPage=_page_border, onLaterPages=_page_border)
    return buf.getvalue()


# =============================================================================
# Endpoint 2 — Health Report PDF
# =============================================================================

@passport_bp.route("/health-report", methods=["POST"])
def generate_health_report():
    """POST /api/passport/health-report

    Accept JSON with health analysis results and return a professional
    A4 PDF (Content-Type: application/pdf).

    Expected JSON fields:
        dog: {name, breed, age, sex, weight, microchip_number}
        symptoms: [str, ...]
        symptom_analysis: {summary, duration, onset}
        matched_diseases: [{name, probability, severity, description,
                            common_symptoms}, ...]
        diagnostic_tests: [{test_name, reason, urgency}, ...]
        genetic_tests: [{test_name, relevant_breed, description}, ...]
        notes: str
        report_date: str  (defaults to today)
    """
    _register_cjk_fonts()
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    try:
        pdf_bytes = _build_health_report_pdf(data)
    except Exception as exc:
        logger.error(f"Health report PDF generation failed: {exc}", exc_info=True)
        return jsonify({"error": f"PDF generation failed: {str(exc)}"}), 500

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
    )


def _build_health_report_pdf(data: dict) -> bytes:
    """Compose the Health Report PDF and return raw bytes."""
    styles = _build_styles()
    buf = io.BytesIO()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN + 2 * mm,
        bottomMargin=MARGIN + 2 * mm,
        title="Pet Health Report",
        author="ShowDog Analysis Platform",
    )

    story = []
    report_date = data.get("report_date", datetime.now().strftime("%Y-%m-%d"))

    # ---- Title ----
    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("PET HEALTH REPORT", styles["title"]))
    story.append(Paragraph(
        f"Report Date: {report_date}  |  ShowDog Analysis Platform",
        styles["subtitle"],
    ))
    story.append(HRFlowable(
        width="100%", thickness=1, color=COLOR_PRIMARY,
        spaceAfter=4 * mm, spaceBefore=1 * mm,
    ))

    # ---- Section 1: Dog Information ----
    dog = data.get("dog", {})
    story.append(_section_banner("1.  DOG INFORMATION", styles))
    story.append(Spacer(1, 2 * mm))
    story.append(_field_pair_table([
        ("Name", dog.get("name")),
        ("Breed", dog.get("breed")),
        ("Age", dog.get("age")),
        ("Sex", dog.get("sex")),
        ("Weight", dog.get("weight")),
        ("Microchip No.", dog.get("microchip_number")),
    ], styles, col_count=2))
    story.append(Spacer(1, 3 * mm))

    # ---- Section 2: Reported Symptoms ----
    symptoms = data.get("symptoms", [])
    analysis = data.get("symptom_analysis", {})
    story.append(_section_banner("2.  SYMPTOM ANALYSIS", styles))
    story.append(Spacer(1, 2 * mm))

    if symptoms:
        symptom_bullets = "  /  ".join(str(s) for s in symptoms)
        story.append(Paragraph(
            f"<b>Reported Symptoms:</b>  {symptom_bullets}",
            styles["body"],
        ))
        story.append(Spacer(1, 1 * mm))

    if analysis.get("summary"):
        story.append(Paragraph(
            f"<b>Summary:</b>  {analysis['summary']}", styles["body"],
        ))
    if analysis.get("duration"):
        story.append(Paragraph(
            f"<b>Duration:</b>  {analysis['duration']}", styles["body"],
        ))
    if analysis.get("onset"):
        story.append(Paragraph(
            f"<b>Onset:</b>  {analysis['onset']}", styles["body"],
        ))

    if not symptoms and not analysis:
        story.append(Paragraph("No symptom data provided.", styles["body_small"]))

    story.append(Spacer(1, 3 * mm))

    # ---- Section 3: Matched Diseases ----
    diseases = data.get("matched_diseases", [])
    story.append(_section_banner("3.  POSSIBLE CONDITIONS", styles))
    story.append(Spacer(1, 2 * mm))

    if diseases:
        avail = PAGE_WIDTH - 2 * MARGIN

        # Table header
        disease_header = [
            Paragraph("Condition", styles["table_header"]),
            Paragraph("Probability", styles["table_header"]),
            Paragraph("Severity", styles["table_header"]),
            Paragraph("Description", styles["table_header"]),
        ]
        disease_rows = [disease_header]

        for d in diseases:
            severity_raw = str(d.get("severity", "unknown")).lower()
            if severity_raw in ("high", "severe", "critical"):
                sev_style = styles["severity_high"]
                sev_label = "HIGH"
            elif severity_raw in ("medium", "moderate"):
                sev_style = styles["severity_medium"]
                sev_label = "MEDIUM"
            else:
                sev_style = styles["severity_low"]
                sev_label = "LOW"

            prob_val = d.get("probability", "—")
            prob_str = f"{prob_val:.0f}%" if isinstance(prob_val, (int, float)) else str(prob_val)

            disease_rows.append([
                Paragraph(str(d.get("name", "—")), styles["table_cell"]),
                Paragraph(prob_str, styles["table_cell_center"]),
                Paragraph(sev_label, sev_style),
                Paragraph(str(d.get("description", "—")), styles["table_cell"]),
            ])

        d_col_ws = [avail * 0.22, avail * 0.13, avail * 0.12, avail * 0.53]
        d_table = Table(disease_rows, colWidths=d_col_ws, repeatRows=1)
        d_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_SECONDARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_WHITE),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_WHITE, COLOR_BG_ROW]),
        ]))
        story.append(d_table)
    else:
        story.append(Paragraph("No conditions matched.", styles["body_small"]))

    story.append(Spacer(1, 3 * mm))

    # ---- Section 4: Recommended Diagnostic Tests ----
    diag_tests = data.get("diagnostic_tests", [])
    story.append(_section_banner("4.  RECOMMENDED DIAGNOSTIC TESTS", styles))
    story.append(Spacer(1, 2 * mm))

    if diag_tests:
        avail = PAGE_WIDTH - 2 * MARGIN
        dt_header = [
            Paragraph("Test", styles["table_header"]),
            Paragraph("Reason", styles["table_header"]),
            Paragraph("Urgency", styles["table_header"]),
        ]
        dt_rows = [dt_header]
        for t in diag_tests:
            urgency_raw = str(t.get("urgency", "routine")).lower()
            if urgency_raw in ("urgent", "immediate", "emergency"):
                urg_style = styles["severity_high"]
            elif urgency_raw in ("soon", "recommended"):
                urg_style = styles["severity_medium"]
            else:
                urg_style = styles["severity_low"]

            dt_rows.append([
                Paragraph(str(t.get("test_name", "—")), styles["table_cell"]),
                Paragraph(str(t.get("reason", "—")), styles["table_cell"]),
                Paragraph(str(t.get("urgency", "Routine")).capitalize(), urg_style),
            ])

        dt_col_ws = [avail * 0.28, avail * 0.52, avail * 0.20]
        dt_table = Table(dt_rows, colWidths=dt_col_ws, repeatRows=1)
        dt_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_SECONDARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_WHITE),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_WHITE, COLOR_BG_ROW]),
        ]))
        story.append(dt_table)
    else:
        story.append(Paragraph("No diagnostic tests recommended.", styles["body_small"]))

    story.append(Spacer(1, 3 * mm))

    # ---- Section 5: Genetic Test Recommendations ----
    gen_tests = data.get("genetic_tests", [])
    story.append(_section_banner("5.  GENETIC TEST RECOMMENDATIONS", styles))
    story.append(Spacer(1, 2 * mm))

    if gen_tests:
        avail = PAGE_WIDTH - 2 * MARGIN
        gt_header = [
            Paragraph("Test", styles["table_header"]),
            Paragraph("Relevant Breed", styles["table_header"]),
            Paragraph("Description", styles["table_header"]),
        ]
        gt_rows = [gt_header]
        for g in gen_tests:
            gt_rows.append([
                Paragraph(str(g.get("test_name", "—")), styles["table_cell"]),
                Paragraph(str(g.get("relevant_breed", "—")), styles["table_cell"]),
                Paragraph(str(g.get("description", "—")), styles["table_cell"]),
            ])

        gt_col_ws = [avail * 0.28, avail * 0.22, avail * 0.50]
        gt_table = Table(gt_rows, colWidths=gt_col_ws, repeatRows=1)
        gt_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), COLOR_SECONDARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), COLOR_WHITE),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("GRID", (0, 0), (-1, -1), 0.5, COLOR_BORDER),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLOR_WHITE, COLOR_BG_ROW]),
        ]))
        story.append(gt_table)
    else:
        story.append(Paragraph("No genetic tests recommended.", styles["body_small"]))

    story.append(Spacer(1, 3 * mm))

    # ---- Notes ----
    notes = data.get("notes")
    if notes:
        story.append(_section_banner("6.  ADDITIONAL NOTES", styles))
        story.append(Spacer(1, 2 * mm))
        story.append(Paragraph(str(notes), styles["body"]))
        story.append(Spacer(1, 3 * mm))

    # ---- Disclaimer ----
    story.append(Spacer(1, 4 * mm))
    story.append(HRFlowable(
        width="100%", thickness=0.5, color=COLOR_BORDER,
        spaceAfter=2 * mm, spaceBefore=2 * mm,
    ))
    disclaimer_text = (
        "DISCLAIMER: This health report is generated by an automated analysis "
        "system and is intended for informational purposes only.  It does NOT "
        "constitute a veterinary diagnosis.  The conditions listed are "
        "possibilities based on the reported symptoms and should be confirmed "
        "by a licensed veterinarian through proper clinical examination and "
        "diagnostic testing.  Always consult a qualified veterinary "
        "professional before making any treatment decisions."
    )
    story.append(Paragraph(disclaimer_text, styles["disclaimer"]))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph(
        f"Report generated on {report_date} by ShowDog Analysis Platform.",
        styles["disclaimer"],
    ))

    doc.build(story, onFirstPage=_page_border, onLaterPages=_page_border)
    return buf.getvalue()
