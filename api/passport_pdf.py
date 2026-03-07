"""
International Pet Passport and Veterinary Health Report PDF Generator.

Generates professional A4 PDF documents for:
  - International Veterinary Certificates (pet passports)
  - Veterinary Health Assessment Reports

Uses the reportlab library for PDF generation.
All outputs are returned as in-memory bytes (BytesIO).
"""

import json
import logging
import uuid
from datetime import datetime
from io import BytesIO

from api.errors import DataCorruptionError

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.platypus.flowables import Image as RLImage

try:
    from io import BytesIO as _QRBuf

    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PAGE_WIDTH, PAGE_HEIGHT = A4  # 595.27, 841.89 points

COLOUR_HEADER_BG = colors.HexColor("#f0f0f0")
COLOUR_ACCENT = colors.HexColor("#1a3c6e")
COLOUR_LIGHT_BLUE = colors.HexColor("#e8f0fe")
COLOUR_RABIES_HIGHLIGHT = colors.HexColor("#fff3cd")
COLOUR_BORDER = colors.HexColor("#cccccc")
COLOUR_BLACK = colors.black
COLOUR_WHITE = colors.white
COLOUR_DARK_GRAY = colors.HexColor("#333333")
COLOUR_MEDIUM_GRAY = colors.HexColor("#666666")

VALID_DAYS_DEFAULT = 10


# ---------------------------------------------------------------------------
# Helper: certificate number
# ---------------------------------------------------------------------------

def generate_certificate_number() -> str:
    """Return a unique certificate number based on UUID-4.

    Format: ``PET-XXXXXXXX`` where X is an uppercase hex segment derived
    from a UUID so that the number is both unique and compact.
    """
    raw = uuid.uuid4().hex.upper()
    return f"PET-{raw[:4]}-{raw[4:8]}-{raw[8:12]}"


# ---------------------------------------------------------------------------
# Internal: shared style helpers
# ---------------------------------------------------------------------------

def _get_styles():
    """Build and return a dictionary of ``ParagraphStyle`` objects used
    throughout both PDF generators."""

    base = getSampleStyleSheet()

    styles = {
        "Title": ParagraphStyle(
            "PDFTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=20,
            alignment=TA_CENTER,
            spaceAfter=2 * mm,
            textColor=COLOUR_ACCENT,
        ),
        "Subtitle": ParagraphStyle(
            "PDFSubtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            spaceAfter=4 * mm,
            textColor=COLOUR_MEDIUM_GRAY,
        ),
        "SectionHeader": ParagraphStyle(
            "SectionHeader",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            spaceBefore=5 * mm,
            spaceAfter=2 * mm,
            textColor=COLOUR_ACCENT,
            borderPadding=(2 * mm, 2 * mm, 1 * mm, 2 * mm),
        ),
        "Normal": ParagraphStyle(
            "PDFNormal",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=COLOUR_DARK_GRAY,
        ),
        "NormalBold": ParagraphStyle(
            "PDFNormalBold",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=COLOUR_DARK_GRAY,
        ),
        "Small": ParagraphStyle(
            "PDFSmall",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=COLOUR_MEDIUM_GRAY,
        ),
        "SmallBold": ParagraphStyle(
            "PDFSmallBold",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=COLOUR_DARK_GRAY,
        ),
        "CellNormal": ParagraphStyle(
            "CellNormal",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=COLOUR_DARK_GRAY,
        ),
        "CellBold": ParagraphStyle(
            "CellBold",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=COLOUR_DARK_GRAY,
        ),
        "CellHeader": ParagraphStyle(
            "CellHeader",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=COLOUR_WHITE,
        ),
        "Justified": ParagraphStyle(
            "PDFJustified",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            alignment=TA_JUSTIFY,
            textColor=COLOUR_DARK_GRAY,
        ),
        "Footer": ParagraphStyle(
            "PDFFooter",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            alignment=TA_CENTER,
            textColor=COLOUR_MEDIUM_GRAY,
        ),
        "CheckItem": ParagraphStyle(
            "CheckItem",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            leftIndent=6 * mm,
            textColor=COLOUR_DARK_GRAY,
        ),
    }
    return styles


def _safe(data: dict, key: str, default: str = "N/A") -> str:
    """Return ``data[key]`` if present and truthy, else *default*.

    Handles ``None`` values and missing keys gracefully so that the PDF
    never displays ``None`` or crashes on absent data.
    """
    val = data.get(key)
    if val is None or (isinstance(val, str) and val.strip() == ""):
        return default
    return str(val)


def _safe_list(data: dict, key: str) -> list:
    """Return ``data[key]`` if it is a list, otherwise an empty list."""
    val = data.get(key)
    if isinstance(val, list):
        return val
    return []


def _format_date(value, default="N/A"):
    """Attempt to present a date string nicely; return *default* on failure."""
    if not value:
        return default
    if isinstance(value, datetime):
        return value.strftime("%d %B %Y")
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(str(value), fmt).strftime("%d %B %Y")
        except (ValueError, TypeError):
            continue
    return str(value)


# ---------------------------------------------------------------------------
# Internal: page number callback
# ---------------------------------------------------------------------------

def _add_page_number(canvas, doc):
    """Draw page number at the bottom-centre of every page."""
    canvas.saveState()
    canvas.setFont("Helvetica", 7)
    canvas.setFillColor(COLOUR_MEDIUM_GRAY)
    page_num_text = f"Page {doc.page}"
    canvas.drawCentredString(PAGE_WIDTH / 2, 12 * mm, page_num_text)
    canvas.restoreState()


def _add_passport_header_footer(canvas, doc):
    """Draw page number and a thin top rule for the passport PDF."""
    _add_page_number(canvas, doc)
    canvas.saveState()
    # thin accent line at top
    canvas.setStrokeColor(COLOUR_ACCENT)
    canvas.setLineWidth(1.5)
    canvas.line(
        doc.leftMargin,
        PAGE_HEIGHT - 12 * mm,
        PAGE_WIDTH - doc.rightMargin,
        PAGE_HEIGHT - 12 * mm,
    )
    # thin accent line at bottom
    canvas.setLineWidth(0.5)
    canvas.line(
        doc.leftMargin,
        16 * mm,
        PAGE_WIDTH - doc.rightMargin,
        16 * mm,
    )
    canvas.restoreState()


def _add_report_header_footer(canvas, doc):
    """Draw page number and a thin top rule for the health report PDF."""
    _add_page_number(canvas, doc)
    canvas.saveState()
    canvas.setStrokeColor(COLOUR_ACCENT)
    canvas.setLineWidth(1.5)
    canvas.line(
        doc.leftMargin,
        PAGE_HEIGHT - 12 * mm,
        PAGE_WIDTH - doc.rightMargin,
        PAGE_HEIGHT - 12 * mm,
    )
    canvas.setLineWidth(0.5)
    canvas.line(
        doc.leftMargin,
        16 * mm,
        PAGE_WIDTH - doc.rightMargin,
        16 * mm,
    )
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Internal: table builders
# ---------------------------------------------------------------------------

def _section_heading(text: str, styles: dict) -> list:
    """Return flowable elements for a coloured section heading bar."""
    heading_data = [[Paragraph(text, styles["SectionHeader"])]]
    heading_table = Table(heading_data, colWidths=[PAGE_WIDTH - 40 * mm])
    heading_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), COLOUR_HEADER_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return [heading_table, Spacer(1, 1 * mm)]


def _info_table(rows: list, styles: dict, col_widths=None):
    """Build a two-column label/value table.

    *rows* is a list of ``(label, value)`` tuples.  Labels are rendered bold.
    """
    table_data = []
    for label, value in rows:
        table_data.append([
            Paragraph(f"<b>{label}:</b>", styles["CellNormal"]),
            Paragraph(str(value), styles["CellNormal"]),
        ])

    if col_widths is None:
        col_widths = [45 * mm, PAGE_WIDTH - 85 * mm]

    t = Table(table_data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, COLOUR_BORDER),
        ("BACKGROUND", (0, 0), (0, -1), COLOUR_LIGHT_BLUE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


def _data_table_with_header(headers: list, rows: list, styles: dict,
                            col_widths=None, highlight_rows=None):
    """Build a full-width table with a dark header row.

    *highlight_rows* is an optional set/list of 0-based row indices (of the
    data rows, not including the header) that should receive a yellow
    highlight (used for rabies vaccines, etc.).
    """
    highlight_rows = set(highlight_rows or [])

    header_cells = [Paragraph(h, styles["CellHeader"]) for h in headers]
    data_cells = []
    for row in rows:
        data_cells.append(
            [Paragraph(str(cell), styles["CellNormal"]) for cell in row]
        )

    table_data = [header_cells] + data_cells

    avail = PAGE_WIDTH - 40 * mm
    if col_widths is None:
        n = len(headers)
        col_widths = [avail / n] * n

    t = Table(table_data, colWidths=col_widths, repeatRows=1)

    style_commands = [
        ("BACKGROUND", (0, 0), (-1, 0), COLOUR_ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLOUR_WHITE),
        ("GRID", (0, 0), (-1, -1), 0.4, COLOUR_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 8.5),
    ]

    # alternate row shading for readability
    for i in range(len(rows)):
        row_idx = i + 1  # +1 because header is row 0
        if i in highlight_rows:
            style_commands.append(
                ("BACKGROUND", (0, row_idx), (-1, row_idx), COLOUR_RABIES_HIGHLIGHT)
            )
        elif i % 2 == 1:
            style_commands.append(
                ("BACKGROUND", (0, row_idx), (-1, row_idx), colors.HexColor("#fafafa"))
            )

    t.setStyle(TableStyle(style_commands))
    return t


# ---------------------------------------------------------------------------
# Public: generate_passport_pdf
# ---------------------------------------------------------------------------

def generate_passport_pdf(data: dict) -> BytesIO:
    """Generate an International Veterinary Certificate (pet passport) as an
    A4 PDF and return the result as a ``BytesIO`` object containing the raw
    PDF bytes.

    Parameters
    ----------
    data : dict
        Dictionary containing the following top-level keys (all optional
        except where noted):

        - ``owner_name``, ``owner_address``, ``owner_phone``,
          ``owner_email``, ``emergency_contact``
        - ``pet_name``, ``species`` (defaults to *Dog*), ``breed``,
          ``sex``, ``date_of_birth``, ``color_markings``
        - ``microchip_number``, ``microchip_date``, ``microchip_location``
        - ``vaccinations`` -- list of dicts with keys ``vaccine``,
          ``date``, ``manufacturer``, ``lot_number``, ``expiry``,
          ``veterinarian``
        - ``parasite_treatments`` -- list of dicts with keys ``type``,
          ``date``, ``product``, ``administered_by``
        - ``exam_date``, ``weight``, ``temperature``, ``heart_rate``,
          ``respiratory_rate``, ``bcs`` (body condition score)
        - ``organ_systems`` -- list of dicts with ``system``, ``status``
          (*Normal* / *Abnormal*), ``notes``
        - ``health_statement``
        - ``destination``, ``departure_date``, ``return_date``,
          ``travel_purpose``
        - ``vet_name``, ``vet_license``, ``vet_clinic``, ``vet_date``
        - ``valid_days`` -- integer, defaults to 10
        - ``certificate_number`` -- if omitted, one is auto-generated

    Returns
    -------
    BytesIO
        In-memory buffer positioned at 0, containing the PDF bytes.
    """

    if data is None:
        logging.getLogger(__name__).warning(
            "generate_passport_pdf called with data=None; "
            "producing PDF with empty fields"
        )
        data = {}

    buf = BytesIO()
    styles = _get_styles()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=18 * mm,
        bottomMargin=22 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        title="International Veterinary Certificate for Dogs",
        author="ShowDog Platform",
    )

    elements: list = []
    cert_number = data.get("certificate_number") or generate_certificate_number()
    issue_date = _format_date(data.get("issue_date"), datetime.now().strftime("%d %B %Y"))

    # ------------------------------------------------------------------
    # PAGE 1
    # ------------------------------------------------------------------

    # Title block
    elements.append(Spacer(1, 2 * mm))
    elements.append(Paragraph(
        "INTERNATIONAL VETERINARY CERTIFICATE FOR DOGS",
        styles["Title"],
    ))
    elements.append(Paragraph(
        "Health Certificate for International Travel",
        styles["Subtitle"],
    ))

    # Certificate number / date row
    meta_data = [
        [
            Paragraph(f"<b>Certificate No:</b> {cert_number}", styles["CellNormal"]),
            Paragraph(f"<b>Date of Issue:</b> {issue_date}", styles["CellNormal"]),
        ]
    ]
    avail_width = PAGE_WIDTH - 40 * mm
    meta_table = Table(meta_data, colWidths=[avail_width * 0.55, avail_width * 0.45])
    meta_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_ACCENT),
        ("BACKGROUND", (0, 0), (-1, -1), COLOUR_LIGHT_BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(meta_table)
    elements.append(Spacer(1, 4 * mm))

    # --- Section A: Owner Information ---
    elements.extend(_section_heading("Section A: Owner Information", styles))
    owner_rows = [
        ("Name", _safe(data, "owner_name")),
        ("Address", _safe(data, "owner_address")),
        ("Phone", _safe(data, "owner_phone")),
        ("Email", _safe(data, "owner_email")),
        ("Emergency Contact", _safe(data, "emergency_contact")),
    ]
    elements.append(_info_table(owner_rows, styles))
    elements.append(Spacer(1, 2 * mm))

    # --- Section B: Animal Identification ---
    elements.extend(_section_heading("Section B: Animal Identification", styles))
    species = _safe(data, "species", "Dog")
    call_name = _safe(data, "call_name", "")
    animal_rows = [
        ("Registered Name", _safe(data, "pet_name")),
    ]
    if call_name:
        animal_rows.append(("Call Name", call_name))
    animal_rows.extend([
        ("Species", species),
        ("Breed", _safe(data, "breed")),
        ("Sex", _safe(data, "sex")),
        ("Date of Birth", _format_date(data.get("date_of_birth"))),
        ("Color / Markings", _safe(data, "color_markings")),
    ])
    elements.append(_info_table(animal_rows, styles))
    elements.append(Spacer(1, 1 * mm))

    # Microchip sub-table (bold microchip number)
    chip_number = _safe(data, "microchip_number")
    chip_rows = [
        [
            Paragraph("<b>Microchip Number:</b>", styles["CellNormal"]),
            Paragraph(
                f'<font size="11"><b>{chip_number}</b></font>',
                styles["CellBold"],
            ),
        ],
        [
            Paragraph("<b>Microchip Date:</b>", styles["CellNormal"]),
            Paragraph(_format_date(data.get("microchip_date")), styles["CellNormal"]),
        ],
        [
            Paragraph("<b>Microchip Location:</b>", styles["CellNormal"]),
            Paragraph(_safe(data, "microchip_location"), styles["CellNormal"]),
        ],
    ]
    chip_table = Table(chip_rows, colWidths=[45 * mm, avail_width - 45 * mm])
    chip_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, COLOUR_BORDER),
        ("BACKGROUND", (0, 0), (0, -1), COLOUR_LIGHT_BLUE),
        ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#e6ffe6")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(chip_table)
    elements.append(Spacer(1, 2 * mm))

    # --- Section C: Vaccination Record ---
    elements.extend(_section_heading("Section C: Vaccination Record", styles))
    vaccinations = _safe_list(data, "vaccinations")
    vax_headers = ["Vaccine", "Date", "Manufacturer", "Lot No.", "Expiry", "Veterinarian"]
    vax_rows = []
    rabies_indices = []
    for idx, v in enumerate(vaccinations):
        vaccine_name = _safe(v, "vaccine")
        vax_rows.append([
            vaccine_name,
            _format_date(v.get("date")),
            _safe(v, "manufacturer"),
            _safe(v, "lot_number"),
            _format_date(v.get("expiry")),
            _safe(v, "veterinarian"),
        ])
        if "rabies" in vaccine_name.lower():
            rabies_indices.append(idx)

    if vax_rows:
        vax_col_w = [
            avail_width * 0.17,
            avail_width * 0.14,
            avail_width * 0.18,
            avail_width * 0.14,
            avail_width * 0.14,
            avail_width * 0.23,
        ]
        elements.append(_data_table_with_header(
            vax_headers, vax_rows, styles,
            col_widths=vax_col_w,
            highlight_rows=rabies_indices,
        ))
    else:
        elements.append(Paragraph(
            "<i>No vaccination records provided.</i>",
            styles["Small"],
        ))
    elements.append(Spacer(1, 2 * mm))

    # --- Section D: Parasite Treatment ---
    elements.extend(_section_heading("Section D: Parasite Treatment", styles))
    treatments = _safe_list(data, "parasite_treatments")
    pt_headers = ["Treatment Type", "Date", "Product", "Administered by"]
    pt_rows = []
    for t in treatments:
        pt_rows.append([
            _safe(t, "type"),
            _format_date(t.get("date")),
            _safe(t, "product"),
            _safe(t, "administered_by"),
        ])

    if pt_rows:
        pt_col_w = [
            avail_width * 0.22,
            avail_width * 0.20,
            avail_width * 0.30,
            avail_width * 0.28,
        ]
        elements.append(_data_table_with_header(
            pt_headers, pt_rows, styles, col_widths=pt_col_w,
        ))
    else:
        elements.append(Paragraph(
            "<i>No parasite treatment records provided.</i>",
            styles["Small"],
        ))
    elements.append(Spacer(1, 2 * mm))

    # --- Section E: Clinical Examination ---
    elements.extend(_section_heading("Section E: Clinical Examination", styles))
    exam_rows = [
        ("Examination Date", _format_date(data.get("exam_date"))),
        ("Weight", _safe(data, "weight")),
        ("Temperature", _safe(data, "temperature")),
        ("Heart Rate", _safe(data, "heart_rate")),
        ("Respiratory Rate", _safe(data, "respiratory_rate")),
        ("Body Condition Score (BCS)", _safe(data, "bcs")),
    ]
    elements.append(_info_table(exam_rows, styles))
    elements.append(Spacer(1, 2 * mm))

    # Organ systems checklist
    organ_systems = _safe_list(data, "organ_systems")
    if organ_systems:
        os_headers = ["Organ System", "Status", "Notes"]
        os_rows = []
        for osys in organ_systems:
            status = _safe(osys, "status", "Normal")
            display_status = status
            display_status = "Normal" if status.lower() == "normal" else '<font color="red"><b>Abnormal</b></font>'
            os_rows.append([
                _safe(osys, "system"),
                display_status,
                _safe(osys, "notes", "-"),
            ])
        os_col_w = [avail_width * 0.30, avail_width * 0.20, avail_width * 0.50]
        elements.append(_data_table_with_header(
            os_headers, os_rows, styles, col_widths=os_col_w,
        ))
    else:
        # Default organ system list when none supplied
        default_systems = [
            "Cardiovascular", "Respiratory", "Gastrointestinal",
            "Musculoskeletal", "Integumentary (Skin/Coat)",
            "Neurological", "Eyes", "Ears", "Urogenital",
            "Lymph Nodes",
        ]
        os_headers = ["Organ System", "Status", "Notes"]
        os_rows = [[s, "Normal", "-"] for s in default_systems]
        os_col_w = [avail_width * 0.30, avail_width * 0.20, avail_width * 0.50]
        elements.append(_data_table_with_header(
            os_headers, os_rows, styles, col_widths=os_col_w,
        ))

    elements.append(Spacer(1, 2 * mm))

    # General health statement
    health_stmt = _safe(
        data, "health_statement",
        "The animal described above has been examined and found to be "
        "clinically healthy and fit for international travel.",
    )
    elements.append(Paragraph(
        f"<b>General Health Statement:</b> {health_stmt}",
        styles["Justified"],
    ))
    elements.append(Spacer(1, 2 * mm))

    # --- Section F: Travel Information ---
    elements.extend(_section_heading("Section F: Travel Information", styles))
    travel_rows = [
        ("Destination Country", _safe(data, "destination")),
        ("Departure Date", _format_date(data.get("departure_date"))),
        ("Expected Return Date", _format_date(data.get("return_date"))),
        ("Purpose of Travel", _safe(data, "travel_purpose")),
    ]
    elements.append(_info_table(travel_rows, styles))

    # ------------------------------------------------------------------
    # PAGE 2: Declarations
    # ------------------------------------------------------------------
    elements.append(PageBreak())

    elements.append(Paragraph(
        "DECLARATIONS AND CERTIFICATIONS",
        styles["Title"],
    ))
    elements.append(Spacer(1, 4 * mm))

    # --- Veterinarian Declaration ---
    elements.extend(_section_heading("Veterinarian Declaration", styles))

    exam_date_display = _format_date(
        data.get("exam_date"),
        datetime.now().strftime("%d %B %Y"),
    )
    vet_decl_text = (
        f"I, the undersigned veterinarian, certify that I have examined the "
        f"animal described above on <b>{exam_date_display}</b> and found it to be:"
    )
    elements.append(Paragraph(vet_decl_text, styles["Justified"]))
    elements.append(Spacer(1, 3 * mm))

    # Checkbox items
    checkbox_items = [
        "Clinically healthy and fit for travel",
        "Free from signs of infectious or contagious disease",
        "Vaccinated against rabies with a valid vaccination",
    ]
    for item in checkbox_items:
        # Unicode ballot box character
        elements.append(Paragraph(
            f"\u2610&nbsp;&nbsp;{item}",
            styles["CheckItem"],
        ))
    elements.append(Spacer(1, 5 * mm))

    # Signature block
    sig_line = "_______________________________________________"
    vet_name = _safe(data, "vet_name")
    vet_license = _safe(data, "vet_license")
    vet_clinic = _safe(data, "vet_clinic")
    vet_date = _format_date(
        data.get("vet_date"),
        datetime.now().strftime("%d %B %Y"),
    )

    sig_data = [
        [Paragraph(f"Signature: {sig_line}", styles["Normal"]), ""],
        [
            Paragraph(f"<b>Name:</b> {vet_name}", styles["Normal"]),
            Paragraph(f"<b>License No.:</b> {vet_license}", styles["Normal"]),
        ],
        [
            Paragraph(f"<b>Clinic / Hospital:</b> {vet_clinic}", styles["Normal"]),
            Paragraph(f"<b>Date:</b> {vet_date}", styles["Normal"]),
        ],
    ]
    sig_table = Table(sig_data, colWidths=[avail_width * 0.55, avail_width * 0.45])
    sig_table.setStyle(TableStyle([
        ("SPAN", (0, 0), (1, 0)),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(sig_table)
    elements.append(Spacer(1, 3 * mm))

    # Official stamp box
    elements.append(Paragraph("<b>Official Stamp:</b>", styles["Normal"]))
    elements.append(Spacer(1, 1 * mm))
    stamp_data = [
        [Paragraph(
            "&nbsp;<br/><br/><br/><br/><br/>",
            styles["Small"],
        )]
    ]
    stamp_table = Table(stamp_data, colWidths=[55 * mm], rowHeights=[35 * mm])
    stamp_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, COLOUR_ACCENT),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fafafa")),
    ]))
    elements.append(stamp_table)
    elements.append(Spacer(1, 6 * mm))

    # --- Owner Declaration ---
    elements.extend(_section_heading("Owner Declaration", styles))
    owner_decl_text = (
        "I, the undersigned owner/authorized agent, declare that the "
        "information provided in this certificate is true and accurate to "
        "the best of my knowledge. I understand that providing false or "
        "misleading information may result in penalties under applicable "
        "laws and regulations. I accept full responsibility for the animal "
        "described in this certificate during its international transport."
    )
    elements.append(Paragraph(owner_decl_text, styles["Justified"]))
    elements.append(Spacer(1, 5 * mm))

    owner_sig_data = [
        [
            Paragraph(f"Owner Signature: {sig_line}", styles["Normal"]),
        ],
        [
            Paragraph(
                f"<b>Name:</b> {_safe(data, 'owner_name')}"
                f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                f"<b>Date:</b> {vet_date}",
                styles["Normal"],
            ),
        ],
    ]
    owner_sig_table = Table(owner_sig_data, colWidths=[avail_width])
    owner_sig_table.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(owner_sig_table)
    elements.append(Spacer(1, 8 * mm))

    # --- Important Notes ---
    elements.extend(_section_heading("Important Notes", styles))
    valid_days = data.get("valid_days", VALID_DAYS_DEFAULT)
    try:
        valid_days = int(valid_days)
    except (ValueError, TypeError):
        valid_days = VALID_DAYS_DEFAULT

    notes = [
        f"This certificate is valid for <b>{valid_days} days</b> from the "
        f"date of clinical examination.",
        "Entry requirements may vary by destination country. It is the "
        "owner's responsibility to verify all import regulations, "
        "quarantine requirements, and necessary documentation before travel.",
        "Some countries require this certificate to be endorsed by the "
        "competent authority of the exporting country.",
        "The microchip must be ISO 11784/11785 compliant. If a non-standard "
        "microchip is used, the owner must provide a compatible reader.",
    ]
    for i, note in enumerate(notes, 1):
        elements.append(Paragraph(
            f"{i}. {note}",
            styles["Justified"],
        ))
        elements.append(Spacer(1, 1.5 * mm))

    elements.append(Spacer(1, 5 * mm))

    # QR Code - contains certificate verification data
    elements.append(Paragraph("<b>Verification QR Code:</b>", styles["Normal"]))
    elements.append(Spacer(1, 1 * mm))
    if QR_AVAILABLE:
        qr_payload = json.dumps({
            "cert": cert_number,
            "pet": data.get("pet_name", ""),
            "breed": data.get("breed", ""),
            "chip": data.get("microchip_number", ""),
            "issued": issue_date,
        }, ensure_ascii=False)
        qr_img = qrcode.make(qr_payload, box_size=4, border=2)
        qr_buf = _QRBuf()
        qr_img.save(qr_buf, format="PNG")
        qr_buf.seek(0)
        elements.append(RLImage(qr_buf, width=35 * mm, height=35 * mm))
    else:
        qr_data = [[Paragraph(
            '<font color="#999999">[ QR Code - qrcode library required ]</font>',
            ParagraphStyle(
                "QRFallback",
                fontName="Helvetica",
                fontSize=9,
                alignment=TA_CENTER,
                textColor=COLOUR_MEDIUM_GRAY,
            ),
        )]]
        qr_table = Table(qr_data, colWidths=[35 * mm], rowHeights=[35 * mm])
        qr_table.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 0.8, COLOUR_BORDER),
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fafafa")),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        elements.append(qr_table)

    # Build
    doc.build(
        elements,
        onFirstPage=_add_passport_header_footer,
        onLaterPages=_add_passport_header_footer,
    )
    buf.seek(0)
    return buf


# ---------------------------------------------------------------------------
# Public: generate_health_report_pdf
# ---------------------------------------------------------------------------

def generate_health_report_pdf(data: dict, analysis_results: dict) -> BytesIO:
    """Generate a Veterinary Health Assessment Report as an A4 PDF and return
    the result as a ``BytesIO`` object.

    Parameters
    ----------
    data : dict
        Dictionary with pet/owner information and reported symptoms.

        Expected keys:
        - ``pet_name``, ``breed``, ``age``, ``weight``, ``sex``
        - ``date_of_birth``
        - ``owner_name``
        - ``symptoms`` -- list of dicts, each with ``category`` and
          ``name`` (or simply a list of strings)

    analysis_results : dict
        Dictionary with the AI / rule-based analysis output.

        Expected keys:
        - ``suspected_conditions`` -- list of dicts with ``name``,
          ``description``, ``likelihood`` (e.g. *High*, *Medium*, *Low*)
        - ``recommended_tests`` -- list of dicts with ``name``,
          ``purpose``, ``priority`` (e.g. *Urgent*, *Recommended*,
          *Optional*)
        - ``notes`` -- optional string with additional notes

    Returns
    -------
    BytesIO
        In-memory buffer positioned at 0, containing the PDF bytes.
    """

    _logger = logging.getLogger(__name__)
    if data is None:
        _logger.warning(
            "generate_health_report_pdf called with data=None; "
            "producing PDF with empty fields"
        )
        data = {}
    if analysis_results is None:
        _logger.warning(
            "generate_health_report_pdf called with analysis_results=None; "
            "health report will have no analysis data"
        )
        analysis_results = {}

    buf = BytesIO()
    styles = _get_styles()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=18 * mm,
        bottomMargin=22 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        title="Veterinary Health Assessment Report",
        author="ShowDog Platform",
    )

    elements: list = []
    avail_width = PAGE_WIDTH - 40 * mm
    report_date = datetime.now().strftime("%d %B %Y")

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------
    elements.append(Spacer(1, 2 * mm))
    elements.append(Paragraph(
        "VETERINARY HEALTH ASSESSMENT REPORT",
        styles["Title"],
    ))
    elements.append(Paragraph(
        "Preliminary Symptom-Based Evaluation",
        styles["Subtitle"],
    ))

    # Pet summary row
    pet_name = _safe(data, "pet_name", "Unknown")
    breed = _safe(data, "breed")
    age = _safe(data, "age")
    weight = _safe(data, "weight")
    sex = _safe(data, "sex")

    summary_data = [
        [
            Paragraph(f"<b>Patient:</b> {pet_name}", styles["CellNormal"]),
            Paragraph(f"<b>Breed:</b> {breed}", styles["CellNormal"]),
            Paragraph(f"<b>Age:</b> {age}", styles["CellNormal"]),
        ],
        [
            Paragraph(f"<b>Weight:</b> {weight}", styles["CellNormal"]),
            Paragraph(f"<b>Sex:</b> {sex}", styles["CellNormal"]),
            Paragraph(f"<b>Date:</b> {report_date}", styles["CellNormal"]),
        ],
    ]
    summary_table = Table(
        summary_data,
        colWidths=[avail_width * 0.38, avail_width * 0.32, avail_width * 0.30],
    )
    summary_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_ACCENT),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, COLOUR_BORDER),
        ("BACKGROUND", (0, 0), (-1, -1), COLOUR_LIGHT_BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 4 * mm))

    # ------------------------------------------------------------------
    # Reported Symptoms
    # ------------------------------------------------------------------
    elements.extend(_section_heading("Reported Symptoms", styles))

    symptoms = _safe_list(data, "symptoms")
    if symptoms:
        # Group by category if dicts
        if symptoms and isinstance(symptoms[0], dict):
            categories: dict = {}
            for s in symptoms:
                cat = _safe(s, "category", "General")
                name = _safe(s, "name", str(s))
                categories.setdefault(cat, []).append(name)

            for cat, items in categories.items():
                elements.append(Paragraph(
                    f"<b>{cat}</b>",
                    styles["NormalBold"],
                ))
                elements.append(Spacer(1, 1 * mm))
                for item in items:
                    # Unicode checkmark
                    elements.append(Paragraph(
                        f"&nbsp;&nbsp;&nbsp;\u2713&nbsp;&nbsp;{item}",
                        styles["Normal"],
                    ))
                elements.append(Spacer(1, 2 * mm))
        else:
            # Simple list of strings
            for item in symptoms:
                elements.append(Paragraph(
                    f"&nbsp;&nbsp;&nbsp;\u2713&nbsp;&nbsp;{str(item)}",
                    styles["Normal"],
                ))
            elements.append(Spacer(1, 2 * mm))
    else:
        elements.append(Paragraph(
            "<i>No symptoms were reported.</i>",
            styles["Small"],
        ))
        elements.append(Spacer(1, 2 * mm))

    # ------------------------------------------------------------------
    # Suspected Conditions
    # ------------------------------------------------------------------
    elements.extend(_section_heading("Suspected Conditions", styles))

    conditions = _safe_list(analysis_results, "suspected_conditions")
    if conditions:
        for idx, cond in enumerate(conditions, 1):
            cond_name = _safe(cond, "name", "Unknown Condition")
            description = _safe(cond, "description", "No description available.")
            likelihood = _safe(cond, "likelihood", "Unknown")

            # Colour-code the likelihood
            likelihood_lower = likelihood.lower()
            if "high" in likelihood_lower:
                lk_colour = "#dc3545"
                lk_label = "HIGH"
            elif "medium" in likelihood_lower or "moderate" in likelihood_lower:
                lk_colour = "#fd7e14"
                lk_label = "MEDIUM"
            elif "low" in likelihood_lower:
                lk_colour = "#28a745"
                lk_label = "LOW"
            else:
                lk_colour = "#6c757d"
                lk_label = likelihood.upper()

            cond_data = [
                [
                    Paragraph(
                        f"<b>{idx}. {cond_name}</b>",
                        styles["CellBold"],
                    ),
                    Paragraph(
                        f'<font color="{lk_colour}"><b>Likelihood: {lk_label}</b></font>',
                        styles["CellNormal"],
                    ),
                ],
                [
                    Paragraph(description, styles["CellNormal"]),
                    "",
                ],
            ]
            cond_table = Table(
                cond_data,
                colWidths=[avail_width * 0.68, avail_width * 0.32],
            )
            cond_table.setStyle(TableStyle([
                ("SPAN", (0, 1), (1, 1)),
                ("BOX", (0, 0), (-1, -1), 0.4, COLOUR_BORDER),
                ("LINEBELOW", (0, 0), (-1, 0), 0.3, COLOUR_BORDER),
                ("BACKGROUND", (0, 0), (-1, 0), COLOUR_HEADER_BG),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            elements.append(cond_table)
            elements.append(Spacer(1, 2 * mm))
    else:
        elements.append(Paragraph(
            "<i>No suspected conditions identified based on the reported symptoms.</i>",
            styles["Small"],
        ))
        elements.append(Spacer(1, 2 * mm))

    # ------------------------------------------------------------------
    # Recommended Diagnostic Tests
    # ------------------------------------------------------------------
    elements.extend(_section_heading("Recommended Diagnostic Tests", styles))

    tests = _safe_list(analysis_results, "recommended_tests")
    if tests:
        test_headers = ["#", "Test Name", "Purpose", "Priority"]
        test_rows = []
        for idx, t in enumerate(tests, 1):
            test_name = _safe(t, "name", "Unknown Test")
            purpose = _safe(t, "purpose", "-")
            priority = _safe(t, "priority", "Recommended")

            # Colour-code the priority
            priority_lower = priority.lower()
            if "urgent" in priority_lower:
                priority_display = '<font color="#dc3545"><b>URGENT</b></font>'
            elif "recommended" in priority_lower:
                priority_display = '<font color="#fd7e14"><b>RECOMMENDED</b></font>'
            elif "optional" in priority_lower:
                priority_display = '<font color="#28a745">Optional</font>'
            else:
                priority_display = priority

            test_rows.append([
                str(idx),
                test_name,
                purpose,
                priority_display,
            ])

        test_col_w = [
            avail_width * 0.06,
            avail_width * 0.25,
            avail_width * 0.49,
            avail_width * 0.20,
        ]
        elements.append(_data_table_with_header(
            test_headers, test_rows, styles, col_widths=test_col_w,
        ))
    else:
        elements.append(Paragraph(
            "<i>No specific diagnostic tests recommended at this time.</i>",
            styles["Small"],
        ))
    elements.append(Spacer(1, 4 * mm))

    # ------------------------------------------------------------------
    # Notes for Veterinarian
    # ------------------------------------------------------------------
    elements.extend(_section_heading("Notes for Veterinarian", styles))

    disclaimer = (
        "This report is generated based on owner-reported symptoms and is "
        "intended as a preliminary guide for veterinary consultation. It "
        "does not constitute a veterinary diagnosis. A thorough physical "
        "examination and appropriate diagnostic testing by a licensed "
        "veterinarian are recommended to confirm or rule out any suspected "
        "conditions. Disease data (symptoms, risk factors, frequency, "
        "treatment, prognosis, prevention) is presented as general reference "
        "information within the scope permitted by the Veterinary Practice Act. "
        "Supervised by Kentaro Kaimide, DVM / Minamisoma Veterinary Clinic "
        "(https://www.minamisoma-vet.com/)."
    )
    elements.append(Paragraph(disclaimer, styles["Justified"]))
    elements.append(Spacer(1, 2 * mm))

    additional_notes = analysis_results.get("notes")
    if additional_notes and str(additional_notes).strip():
        elements.append(Paragraph(
            f"<b>Additional Notes:</b> {additional_notes}",
            styles["Justified"],
        ))
        elements.append(Spacer(1, 2 * mm))

    elements.append(Spacer(1, 6 * mm))

    # Veterinarian signature block
    elements.append(HRFlowable(
        width="60%", thickness=0.5, color=COLOUR_BORDER,
        spaceAfter=2 * mm, spaceBefore=2 * mm,
    ))
    sig_line = "_______________________________________________"
    vet_sig_data = [
        [Paragraph(f"Veterinarian Signature: {sig_line}", styles["Normal"])],
        [Paragraph(f"Name: {sig_line}", styles["Normal"])],
        [Paragraph(f"License No.: {sig_line}", styles["Normal"])],
        [Paragraph(f"Date: {sig_line}", styles["Normal"])],
    ]
    vet_sig_table = Table(vet_sig_data, colWidths=[avail_width])
    vet_sig_table.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(vet_sig_table)

    # Build
    doc.build(
        elements,
        onFirstPage=_add_report_header_footer,
        onLaterPages=_add_report_header_footer,
    )
    buf.seek(0)
    return buf


# =============================================================================
# MAFF Export Inspection Application Form (別記様式第１号)
# =============================================================================

def generate_maff_export_pdf(data: dict) -> BytesIO:
    """Generate the official MAFF dog export inspection application form.

    Reproduces 別記様式第１号:
    狂犬病予防法及び家畜伝染病予防法に基づく犬の輸出検査申請書
    APPLICATION FOR EXPORT INSPECTION OF DOG

    Parameters
    ----------
    data : dict
        Keys (all optional):
        - applicant_name, applicant_address, applicant_phone, applicant_org
        - species (defaults to "犬 Dog"), quantity (defaults to 1)
        - pet_name, breed, color, sex, use
        - date_of_birth, age
        - destination_country
        - length_cm, height_cm, weight_kg
        - embarkation_date, embarkation_place
        - vessel_or_flight
        - consignor_name, consignor_address
        - consignee_name, consignee_address
        - keeping_place, purchase_date, reentry_date
        - microchip_type, microchip_number, microchip_date,
          microchip_location, microchip_reader_type
        - rabies_vaccinations: list of dicts with vaccine_date, expiry_date,
          vaccine_kind, vaccine_product
        - other_vaccinations: list of dicts (same keys)
        - rabies_test_date, antibody_titer, lab_name, lab_address
        - remarks
    """
    if data is None:
        logging.getLogger(__name__).warning(
            "generate_maff_export_pdf called with data=None; "
            "producing PDF with empty fields"
        )
        data = {}

    buf = BytesIO()

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=12 * mm,
        bottomMargin=10 * mm,
        leftMargin=14 * mm,
        rightMargin=14 * mm,
        title="犬の輸出検査申請書",
        author="ShowDog Platform",
    )

    styles = getSampleStyleSheet()

    # Custom styles for the form
    styles.add(ParagraphStyle(
        "FormTitle", parent=styles["Normal"],
        fontSize=10, fontName="Helvetica-Bold",
        alignment=TA_CENTER, spaceBefore=2, spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        "FormTitleJP", parent=styles["Normal"],
        fontSize=7, alignment=TA_CENTER,
        spaceBefore=0, spaceAfter=1,
    ))
    styles.add(ParagraphStyle(
        "CellLabel", parent=styles["Normal"],
        fontSize=6.5, leading=8,
    ))
    styles.add(ParagraphStyle(
        "CellValue", parent=styles["Normal"],
        fontSize=8, leading=10,
    ))
    styles.add(ParagraphStyle(
        "CellLabelSmall", parent=styles["Normal"],
        fontSize=5.5, leading=7, textColor=COLOUR_MEDIUM_GRAY,
    ))

    elements = []
    avail_width = PAGE_WIDTH - 28 * mm

    def _v(key, default=""):
        val = data.get(key)
        if val is None or str(val).strip() == "":
            return default
        return str(val).strip()

    def _label_value(label_jp, label_en, value, label_style="CellLabel", value_style="CellValue"):
        """Create a cell with bilingual label and value."""
        return Paragraph(
            f'<font size="6">{label_jp}</font><br/>'
            f'<font size="5" color="#666666">{label_en}</font><br/>'
            f'<font size="8"><b>{value}</b></font>',
            styles["CellValue"],
        )

    # --- Header ---
    elements.append(Paragraph(
        '<font size="6">別記様式第１号</font>',
        ParagraphStyle("FormNo", parent=styles["Normal"], fontSize=6, alignment=TA_RIGHT),
    ))

    elements.append(Paragraph(
        "狂犬病予防法及び家畜伝染病予防法に基づく犬の輸出検査申請書",
        styles["FormTitle"],
    ))
    elements.append(Paragraph(
        "APPLICATION FOR EXPORT INSPECTION OF DOG<br/>"
        "UNDER THE RABIES PREVENTION LAW AND THE DOMESTIC ANIMAL INFECTIOUS DISEASES CONTROL LAW",
        styles["FormTitleJP"],
    ))
    elements.append(Spacer(1, 2 * mm))

    # To / Date / Applicant row
    app_date = _v("application_date", datetime.now().strftime("%Y年 %m月 %d日"))
    top_data = [
        [
            Paragraph('<font size="6">動物検疫所長 殿<br/>To the chief of Animal Quarantine Service</font>', styles["CellLabel"]),
            Paragraph(f'<font size="7">{app_date}</font>', styles["CellValue"]),
        ],
        [
            Paragraph(
                '<font size="6">下記の動物の輸出検査を申請いたします。</font><br/>'
                '<font size="5" color="#666">I hereby apply for the export quarantine inspection of the undermentioned animal(s).</font>',
                styles["CellLabel"],
            ),
            Paragraph("", styles["CellLabel"]),
        ],
    ]
    top_table = Table(top_data, colWidths=[avail_width * 0.6, avail_width * 0.4])
    top_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(top_table)
    elements.append(Spacer(1, 1 * mm))

    # --- Applicant Section ---
    applicant_data = [
        [
            Paragraph('<font size="6.5"><b>申請者住所氏名及び連絡先</b></font><br/>'
                       '<font size="5" color="#666">Name and address of applicant</font>',
                       styles["CellLabel"]),
        ],
        [
            Paragraph(
                f'<font size="7">氏名 Name: <b>{_v("applicant_name")}</b></font><br/>'
                f'<font size="7">住所 Address: <b>{_v("applicant_address")}</b></font><br/>'
                f'<font size="7">電話番号 Telephone: <b>{_v("applicant_phone")}</b></font>'
                + (f'<br/><font size="6">法人: {_v("applicant_org")}</font>' if _v("applicant_org") else ""),
                styles["CellValue"],
            ),
        ],
    ]
    app_table = Table(applicant_data, colWidths=[avail_width])
    app_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_BLACK),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, COLOUR_BORDER),
        ("BACKGROUND", (0, 0), (0, 0), COLOUR_LIGHT_BLUE),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(app_table)
    elements.append(Spacer(1, 2 * mm))

    # --- Animal Information ---
    species = _v("species", "犬 Dog")
    quantity = _v("quantity", "1")
    pet_name = _v("pet_name")
    breed = _v("breed")
    color = _v("color")
    sex = _v("sex")
    use = _v("use")
    dob = _v("date_of_birth")
    age = _v("age")
    dob_age = f"{dob}" + (f" ({age})" if age else "")
    destination = _v("destination_country")

    animal_rows = [
        [
            _label_value("動物の種類", "Species", species),
            _label_value("頭数", "Quantity", quantity),
            _label_value("名称", "Name of animal(s)", pet_name),
        ],
        [
            _label_value("品種", "Breed", breed),
            _label_value("毛色", "Color", color),
            _label_value("性別", "Sex", sex),
        ],
        [
            _label_value("用途", "Use", use),
            _label_value("生年月日（年齢）", "Date of birth (Age)", dob_age),
            _label_value("仕向国名", "Country of destination", destination),
        ],
    ]
    w3 = avail_width / 3
    animal_table = Table(animal_rows, colWidths=[w3, w3, w3])
    animal_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_BLACK),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, COLOUR_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(animal_table)
    elements.append(Spacer(1, 1 * mm))

    # Body measurements
    body_rows = [[
        _label_value("体長", "Length", f'{_v("length_cm")} cm'),
        _label_value("体高", "Height", f'{_v("height_cm")} cm'),
        _label_value("体重", "Weight", f'{_v("weight_kg")} kg'),
    ]]
    body_table = Table(body_rows, colWidths=[w3, w3, w3])
    body_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_BLACK),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, COLOUR_BORDER),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(body_table)
    elements.append(Spacer(1, 1 * mm))

    # Transport & shipping info
    w2 = avail_width / 2
    transport_rows = [
        [
            _label_value("搭載年月日及び搭載地", "Date and place of embarkation",
                         f'{_v("embarkation_date")}  {_v("embarkation_place")}'),
            _label_value("搭載船舶（航空機）名", "Name of vessel (or flight No.)",
                         _v("vessel_or_flight")),
        ],
        [
            _label_value("荷送人住所氏名", "Name and address of consignor",
                         f'{_v("consignor_name")}  {_v("consignor_address")}'),
            _label_value("荷受人住所氏名", "Name and address of consignee",
                         f'{_v("consignee_name")}  {_v("consignee_address")}'),
        ],
        [
            _label_value("飼養場所（購入場所）", "Name of keeping place (or purchase)",
                         _v("keeping_place")),
            Paragraph(
                f'<font size="6">購入年月日 Date of purchase: <b>{_v("purchase_date")}</b></font><br/>'
                f'<font size="6">帰国予定年月日 Scheduled re-entry: <b>{_v("reentry_date")}</b></font>',
                styles["CellValue"],
            ),
        ],
    ]
    transport_table = Table(transport_rows, colWidths=[w2, w2])
    transport_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_BLACK),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, COLOUR_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(transport_table)
    elements.append(Spacer(1, 1 * mm))

    # --- Microchip / Identification ---
    micro_rows = [
        [
            _label_value("個体識別方法", "Means for identification", _v("microchip_type", "マイクロチップ Microchip")),
            _label_value("個体識別番号", "Identification number/Mark", _v("microchip_number")),
        ],
        [
            _label_value("標識年月日", "Date of identification", _v("microchip_date")),
            _label_value("標識部位", "Location of identification", _v("microchip_location", "左頸部 Left neck")),
        ],
        [
            Paragraph(
                f'<font size="6">マイクロチップ（リーダー）の種類<br/>Type of microchip (reader): '
                f'<b>{_v("microchip_reader_type", "ISO 11784/11785")}</b></font>',
                styles["CellValue"],
            ),
            Paragraph("", styles["CellLabel"]),
        ],
    ]
    micro_table = Table(micro_rows, colWidths=[w2, w2])
    micro_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_BLACK),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, COLOUR_BORDER),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(micro_table)
    elements.append(Spacer(1, 2 * mm))

    # --- Rabies Vaccination ---
    rabies_header = [
        Paragraph(
            '<font size="6.5"><b>狂犬病予防接種 Rabies vaccination</b></font>',
            styles["CellLabel"],
        ),
        Paragraph('<font size="6">接種年月日<br/>Date of vaccination</font>', styles["CellLabelSmall"]),
        Paragraph('<font size="6">有効期限<br/>Date of expiry</font>', styles["CellLabelSmall"]),
        Paragraph('<font size="6">予防液の種類<br/>Kind of vaccine</font>', styles["CellLabelSmall"]),
        Paragraph('<font size="6">予防液の製品名及び製造会社<br/>Name of product &amp; manufacturer</font>', styles["CellLabelSmall"]),
    ]

    rabies_vacs = data.get("rabies_vaccinations", [])
    rabies_rows = [rabies_header]
    for i in range(max(len(rabies_vacs), 2)):
        vac = rabies_vacs[i] if i < len(rabies_vacs) else {}
        rabies_rows.append([
            Paragraph(f'<font size="7">{i+1}</font>', styles["CellValue"]),
            Paragraph(f'<font size="7">{_safe(vac, "vaccine_date")}</font>', styles["CellValue"]),
            Paragraph(f'<font size="7">{_safe(vac, "expiry_date")}</font>', styles["CellValue"]),
            Paragraph(f'<font size="7">{_safe(vac, "vaccine_kind")}</font>', styles["CellValue"]),
            Paragraph(f'<font size="7">{_safe(vac, "vaccine_product")}</font>', styles["CellValue"]),
        ])

    vac_widths = [avail_width * 0.08, avail_width * 0.18, avail_width * 0.18,
                  avail_width * 0.22, avail_width * 0.34]
    rabies_table = Table(rabies_rows, colWidths=vac_widths)
    rabies_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_BLACK),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, COLOUR_BORDER),
        ("BACKGROUND", (0, 0), (-1, 0), COLOUR_RABIES_HIGHLIGHT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(rabies_table)
    elements.append(Spacer(1, 1 * mm))

    # --- Other Vaccinations ---
    other_header = [
        Paragraph(
            '<font size="6.5"><b>その他の予防接種 Other vaccination</b></font>',
            styles["CellLabel"],
        ),
        Paragraph('<font size="6">接種年月日<br/>Date of vaccination</font>', styles["CellLabelSmall"]),
        Paragraph('<font size="6">有効期限<br/>Date of expiry</font>', styles["CellLabelSmall"]),
        Paragraph('<font size="6">予防液の種類<br/>Kind of vaccine</font>', styles["CellLabelSmall"]),
        Paragraph('<font size="6">予防液の製品名及び製造会社<br/>Name of product &amp; manufacturer</font>', styles["CellLabelSmall"]),
    ]

    other_vacs = data.get("other_vaccinations", [])
    other_rows = [other_header]
    for i in range(max(len(other_vacs), 2)):
        vac = other_vacs[i] if i < len(other_vacs) else {}
        other_rows.append([
            Paragraph(f'<font size="7">{i+1}</font>', styles["CellValue"]),
            Paragraph(f'<font size="7">{_safe(vac, "vaccine_date")}</font>', styles["CellValue"]),
            Paragraph(f'<font size="7">{_safe(vac, "expiry_date")}</font>', styles["CellValue"]),
            Paragraph(f'<font size="7">{_safe(vac, "vaccine_kind")}</font>', styles["CellValue"]),
            Paragraph(f'<font size="7">{_safe(vac, "vaccine_product")}</font>', styles["CellValue"]),
        ])

    other_table = Table(other_rows, colWidths=vac_widths)
    other_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_BLACK),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, COLOUR_BORDER),
        ("BACKGROUND", (0, 0), (-1, 0), COLOUR_LIGHT_BLUE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(other_table)
    elements.append(Spacer(1, 1 * mm))

    # --- Rabies Serological Test ---
    test_rows = [
        [
            Paragraph(
                '<font size="6.5"><b>狂犬病抗体検査 Rabies serological test</b></font>',
                styles["CellLabel"],
            ),
            Paragraph("", styles["CellLabel"]),
            Paragraph("", styles["CellLabel"]),
        ],
        [
            _label_value("血液採取年月日", "Blood sampling date", _v("rabies_test_date")),
            _label_value("抗体価", "Antibody titer", f'{_v("antibody_titer")} IU/ml'),
            Paragraph("", styles["CellLabel"]),
        ],
        [
            Paragraph(
                f'<font size="6">検査機関名及び住所 Name and address of the designated laboratory:</font><br/>'
                f'<font size="8"><b>{_v("lab_name")}  {_v("lab_address")}</b></font>',
                styles["CellValue"],
            ),
            Paragraph("", styles["CellLabel"]),
            Paragraph("", styles["CellLabel"]),
        ],
    ]
    test_table = Table(test_rows, colWidths=[w3, w3, w3])
    test_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_BLACK),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, COLOUR_BORDER),
        ("BACKGROUND", (0, 0), (-1, 0), COLOUR_RABIES_HIGHLIGHT),
        ("SPAN", (0, 0), (2, 0)),
        ("SPAN", (0, 2), (2, 2)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(test_table)
    elements.append(Spacer(1, 1 * mm))

    # --- Remarks ---
    remarks_rows = [[
        Paragraph(
            f'<font size="6.5"><b>備考 Remarks</b></font><br/>'
            f'<font size="8">{_v("remarks")}</font>',
            styles["CellValue"],
        ),
    ]]
    remarks_table = Table(remarks_rows, colWidths=[avail_width], rowHeights=[20 * mm])
    remarks_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, COLOUR_BLACK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(remarks_table)

    # --- Footer note ---
    elements.append(Spacer(1, 3 * mm))
    elements.append(Paragraph(
        '<font size="5.5" color="#999">Generated by ShowDog Analysis Platform | '
        'This form follows 別記様式第１号 (MAFF)</font>',
        ParagraphStyle("FooterNote", parent=styles["Normal"], fontSize=5.5, alignment=TA_CENTER),
    ))

    # Build PDF
    doc.build(elements)
    buf.seek(0)
    return buf


# ---------------------------------------------------------------------------
# Veterinary Visit Report PDF
# ---------------------------------------------------------------------------

# Category display labels (Japanese)
_VISIT_CAT_LABELS = {
    "general": "全般状態",
    "appetite": "食欲・飲水",
    "digestive": "消化器症状",
    "respiratory": "呼吸器症状",
    "urinary": "泌尿器症状",
    "skin": "皮膚症状",
    "eyes_ears": "眼・耳・鼻症状",
    "musculoskeletal": "運動器症状",
    "neurological": "神経症状",
    "other": "その他",
}

# Alert keywords for red highlighting
_ALERT_KEYWORDS = [
    "嘔吐", "血便", "黒色便", "呼吸困難", "開口呼吸", "血尿", "尿が出ない",
    "けいれん", "意識障害", "麻痺", "発作", "出血", "痛がる", "異物誤飲",
    "立てない", "ぐったり", "鼻血", "発熱",
]


def _is_alert(item: str) -> bool:
    """Check if a health check item is an alert-level symptom."""
    return any(kw in item for kw in _ALERT_KEYWORDS)


def generate_visit_pdf(visit_data: dict) -> BytesIO:
    """Generate a Veterinary Visit Report PDF.

    Parameters
    ----------
    visit_data : dict
        Visit record from database, including:
        - visit_date, visit_time, chief_complaint
        - health_checks (dict of category -> items list)
        - body_weight_kg, body_temperature, heart_rate, respiratory_rate
        - detailed_memo
        - diagnosis, treatment, prescription, next_visit_date
        - analysis_result (dict with suspected_diseases, recommended_tests, severity)
        - dog_name, dog_breed (optional, for header)

    Returns
    -------
    BytesIO
        In-memory PDF buffer positioned at 0.
    """
    if visit_data is None:
        logging.getLogger(__name__).warning(
            "generate_visit_pdf called with visit_data=None; "
            "producing PDF with empty fields"
        )
        visit_data = {}

    buf = BytesIO()
    styles = _get_styles()

    # Add a smaller style for visit items
    visit_item_style = ParagraphStyle(
        "VisitItem",
        parent=styles["Small"],
        fontSize=8,
        leading=10,
        spaceBefore=1,
        spaceAfter=1,
    )
    visit_item_alert = ParagraphStyle(
        "VisitItemAlert",
        parent=visit_item_style,
        textColor=colors.HexColor("#c53030"),
    )

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=18 * mm,
        bottomMargin=22 * mm,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        title="Veterinary Visit Report",
        author="ShowDog Platform",
    )

    elements: list = []
    avail_width = PAGE_WIDTH - 40 * mm
    report_date = datetime.now().strftime("%d %B %Y")

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------
    elements.append(Spacer(1, 2 * mm))

    # ShowDog branded header
    header_data = [[
        Paragraph(
            '<font size="14"><b>ShowDog v4.0 - 診察記録</b></font>'
            '<br/><font size="9" color="#666666">Veterinary Visit Report</font>',
            styles["Title"],
        ),
        Paragraph(
            f'<font size="8" color="#999999">Report Date: {report_date}</font>',
            ParagraphStyle("RightAlign", parent=styles["Small"], alignment=TA_RIGHT),
        ),
    ]]
    header_table = Table(header_data, colWidths=[avail_width * 0.7, avail_width * 0.3])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#667eea")),
        ("TEXTCOLOR", (0, 0), (0, 0), COLOUR_WHITE),
        ("TEXTCOLOR", (1, 0), (1, 0), colors.HexColor("#c4d4ff")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#5a6fd6")),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 4 * mm))

    # ------------------------------------------------------------------
    # Visit Information
    # ------------------------------------------------------------------
    elements.extend(_section_heading("来院情報 / Visit Information", styles))

    info_rows = [
        ("来院日 / Date", _safe(visit_data, "visit_date", "-")),
    ]
    if visit_data.get("visit_time"):
        info_rows.append(("来院時間 / Time", visit_data["visit_time"]))
    if visit_data.get("dog_name"):
        dog_str = visit_data["dog_name"]
        if visit_data.get("dog_breed"):
            dog_str += f" ({visit_data['dog_breed']})"
        info_rows.append(("犬 / Dog", dog_str))
    info_rows.append(("主訴 / Chief Complaint", _safe(visit_data, "chief_complaint", "-")))

    elements.append(_info_table(info_rows, styles))
    elements.append(Spacer(1, 3 * mm))

    # ------------------------------------------------------------------
    # Vitals
    # ------------------------------------------------------------------
    vitals_parts = []
    if visit_data.get("body_weight_kg"):
        vitals_parts.append(f"体重: {visit_data['body_weight_kg']} kg")
    if visit_data.get("body_temperature"):
        vitals_parts.append(f"体温: {visit_data['body_temperature']} °C")
    if visit_data.get("heart_rate"):
        vitals_parts.append(f"心拍数: {visit_data['heart_rate']} bpm")
    if visit_data.get("respiratory_rate"):
        vitals_parts.append(f"呼吸数: {visit_data['respiratory_rate']} /min")

    if vitals_parts:
        elements.extend(_section_heading("バイタルサイン / Vitals", styles))
        vitals_data = [[Paragraph(
            " &nbsp; | &nbsp; ".join(f"<b>{v}</b>" for v in vitals_parts),
            styles["CellNormal"],
        )]]
        vitals_table = Table(vitals_data, colWidths=[avail_width])
        vitals_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), COLOUR_LIGHT_BLUE),
            ("BOX", (0, 0), (-1, -1), 0.4, COLOUR_BORDER),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ]))
        elements.append(vitals_table)
        elements.append(Spacer(1, 3 * mm))

    # ------------------------------------------------------------------
    # Health Checks
    # ------------------------------------------------------------------
    health_checks = visit_data.get("health_checks", {})
    if isinstance(health_checks, str):
        import json as _json
        try:
            health_checks = _json.loads(health_checks)
        except Exception as e:
            raise DataCorruptionError(
                f"health_checks JSON is corrupt and cannot be included in PDF: {e}"
            ) from e

    if health_checks:
        elements.extend(_section_heading("体調チェック / Health Check Items", styles))

        for cat_key, items in health_checks.items():
            if not items:
                continue
            cat_label = _VISIT_CAT_LABELS.get(cat_key, cat_key)

            # Category heading
            elements.append(Paragraph(
                f'<font size="9"><b>【{cat_label}】</b></font>',
                styles["CellNormal"],
            ))

            # Items as bullet list
            for item in items:
                is_alert = _is_alert(item)
                style = visit_item_alert if is_alert else visit_item_style
                prefix = "⚠ " if is_alert else "• "
                elements.append(Paragraph(
                    f"&nbsp;&nbsp;&nbsp;{prefix}{item}",
                    style,
                ))
            elements.append(Spacer(1, 2 * mm))

        elements.append(Spacer(1, 1 * mm))

    # ------------------------------------------------------------------
    # Detailed Memo
    # ------------------------------------------------------------------
    memo = visit_data.get("detailed_memo", "")
    if memo:
        elements.extend(_section_heading("詳細メモ / Detailed Notes", styles))
        elements.append(Paragraph(
            memo.replace("\n", "<br/>"),
            styles["Small"],
        ))
        elements.append(Spacer(1, 3 * mm))

    # ------------------------------------------------------------------
    # AI Analysis Results
    # ------------------------------------------------------------------
    analysis = visit_data.get("analysis_result", {})
    if isinstance(analysis, str):
        import json as _json
        try:
            analysis = _json.loads(analysis)
        except Exception as e:
            raise DataCorruptionError(
                f"analysis_result JSON is corrupt and cannot be included in PDF: {e}"
            ) from e

    diseases = analysis.get("suspected_diseases", [])
    if diseases:
        elements.extend(_section_heading("AI分析結果 - 疑われる疾患 / Suspected Conditions", styles))

        for d in diseases:
            likelihood = (d.get("likelihood") or "").lower()
            lk_color = (
                colors.HexColor("#e53e3e") if likelihood == "high"
                else colors.HexColor("#dd6b20") if likelihood == "moderate"
                else colors.HexColor("#38a169")
            )
            name_str = d.get("name", "")
            if d.get("name_ja"):
                name_str += f" ({d['name_ja']})"
            desc = d.get("description", "")

            cond_data = [
                [
                    Paragraph(f"<b>{name_str}</b>", styles["CellNormal"]),
                    Paragraph(
                        f'<font color="{lk_color.hexval()}">'
                        f'<b>{d.get("likelihood", "N/A")}</b></font>',
                        ParagraphStyle("LkCell", parent=styles["CellNormal"], alignment=TA_RIGHT),
                    ),
                ],
            ]
            if desc:
                cond_data.append([
                    Paragraph(f"<i>{desc}</i>", styles["Small"]),
                    Paragraph("", styles["Small"]),
                ])

            cond_table = Table(cond_data, colWidths=[avail_width * 0.72, avail_width * 0.28])
            cond_table.setStyle(TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.4, COLOUR_BORDER),
                ("LINEBELOW", (0, 0), (-1, 0), 0.3, COLOUR_BORDER),
                ("BACKGROUND", (0, 0), (-1, 0), COLOUR_HEADER_BG),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]))
            if desc:
                cond_table.setStyle(TableStyle([
                    ("SPAN", (0, 1), (1, 1)),
                ]))
            elements.append(cond_table)
            elements.append(Spacer(1, 2 * mm))

    # Recommended Tests
    tests = analysis.get("recommended_tests", [])
    if tests:
        elements.extend(_section_heading("推奨検査 / Recommended Tests", styles))
        for t in tests:
            t_name = t.get("name", str(t)) if isinstance(t, dict) else str(t)
            if isinstance(t, dict) and t.get("name_ja"):
                t_name += f" ({t['name_ja']})"
            priority = t.get("priority", "") if isinstance(t, dict) else ""
            purpose = t.get("purpose", "") if isinstance(t, dict) else ""
            line = f"• <b>{t_name}</b>"
            if priority:
                p_color = "#e53e3e" if priority == "urgent" else "#dd6b20" if priority == "recommended" else "#718096"
                line += f' <font color="{p_color}">[{priority}]</font>'
            if purpose:
                line += f" — {purpose}"
            elements.append(Paragraph(line, styles["Small"]))
        elements.append(Spacer(1, 3 * mm))

    # Severity
    severity = analysis.get("severity")
    if severity:
        sev_labels = {"emergency": "緊急 (EMERGENCY)", "high": "高 (HIGH)", "moderate": "中 (MODERATE)", "low": "低 (LOW)"}
        sev_colors = {"emergency": "#c53030", "high": "#e53e3e", "moderate": "#dd6b20", "low": "#38a169"}
        sev_color = sev_colors.get(severity, "#718096")
        sev_label = sev_labels.get(severity, severity)
        elements.extend(_section_heading("総合判定 / Overall Assessment", styles))
        elements.append(Paragraph(
            f'<font color="{sev_color}" size="11"><b>{sev_label}</b></font>',
            styles["CellNormal"],
        ))
        advice = analysis.get("general_advice_ja") or analysis.get("general_advice", "")
        if advice:
            elements.append(Paragraph(advice, styles["Small"]))
        elements.append(Spacer(1, 3 * mm))

    # ------------------------------------------------------------------
    # Veterinarian Notes
    # ------------------------------------------------------------------
    vet_notes = []
    if visit_data.get("diagnosis"):
        vet_notes.append(("獣医師の所見 / Veterinary Findings", visit_data["diagnosis"]))
    if visit_data.get("treatment"):
        vet_notes.append(("獣医師による処置 / Veterinary Care", visit_data["treatment"]))
    if visit_data.get("prescription"):
        vet_notes.append(("処方 / Prescription", visit_data["prescription"]))
    if visit_data.get("next_visit_date"):
        vet_notes.append(("次回来院 / Next Visit", visit_data["next_visit_date"]))

    if vet_notes:
        elements.extend(_section_heading("獣医師記入欄 / Veterinarian Notes", styles))
        elements.append(_info_table(vet_notes, styles))
        elements.append(Spacer(1, 3 * mm))

    # ------------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------------
    elements.append(Spacer(1, 5 * mm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=COLOUR_BORDER))
    elements.append(Spacer(1, 2 * mm))
    elements.append(Paragraph(
        '<font size="7" color="#999999">'
        f'Generated by ShowDog Analysis Platform v4.0 on {report_date}. '
        'Supervised by Kentaro Kaimide, DVM (Minamisoma Vet Clinic). '
        'This document is for veterinary reference only.'
        '</font>',
        ParagraphStyle("VisitFooter", parent=styles["Small"], alignment=TA_CENTER),
    ))

    # Build PDF
    doc.build(elements)
    buf.seek(0)
    return buf
