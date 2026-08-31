"""Regression tests for surfacing the clinical-signs / diagnosis fields.

The `clinical_signs` (臨床徴候) and `diagnosis` (診断) fields have long been
populated in the disease records but were never rendered in the SPA or SEO page,
and never even serialized by the /api/health-check/diseases endpoint. These tests
lock in that they are now:
  1. returned by the disease browser API,
  2. rendered on the server-side SEO detail page, and
  3. wired into the SPA (app.js) with proper i18n labels.

They also guard the data fix that split the two dog ophthalmology records whose
diagnostic work-up had been mis-filed into the treatment field.
"""

from pathlib import Path

from api.vetdict_api import app

PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_JS = (PROJECT_ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
SEO_TEMPLATE = (PROJECT_ROOT / "templates" / "disease_detail.html").read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# API: the disease browser endpoint now serializes the two fields
# ---------------------------------------------------------------------------


def test_api_diseases_include_clinical_signs_and_diagnosis():
    client = app.test_client()
    for species in ("dog", "cat", "reptile"):
        resp = client.get(f"/api/health-check/diseases?species={species}")
        assert resp.status_code == 200
        diseases = resp.get_json()["diseases"]
        # Every serialized record must carry the keys (may be empty for a few).
        assert all("clinical_signs_ja" in d and "diagnosis_ja" in d for d in diseases), species
        # And the large majority genuinely carry content.
        with_dx = sum(1 for d in diseases if (d.get("diagnosis_ja") or "").strip())
        with_cs = sum(1 for d in diseases if (d.get("clinical_signs_ja") or "").strip())
        assert with_dx > len(diseases) * 0.5, f"{species}: only {with_dx}/{len(diseases)} have diagnosis"
        assert with_cs > len(diseases) * 0.5, f"{species}: only {with_cs}/{len(diseases)} have clinical signs"


# ---------------------------------------------------------------------------
# Data fix: the two dog ophthalmology records no longer bury diagnosis in treatment
# ---------------------------------------------------------------------------


def test_misfiled_diagnosis_extracted_for_dog_eye_records():
    from api.species.dog_diseases import DISEASES

    targets = {
        "Persistent Pupillary Membrane (PPM)",
        "Persistent Hyperplastic Primary Vitreous (PHPV / PHTVL)",
    }
    seen = 0
    for d in DISEASES:
        if d.get("name") in targets:
            seen += 1
            assert (d.get("diagnosis_ja") or "").strip(), d["name"]
            assert (d.get("diagnosis") or "").strip(), d["name"]
            # The diagnosis header must no longer prefix the treatment field.
            assert not (d.get("treatment_ja") or "").lstrip().startswith("診断"), d["name"]
            assert not (d.get("treatment") or "").lstrip().upper().startswith("DIAGNOSIS"), d["name"]
    assert seen == 2


def test_no_dog_record_buries_diagnosis_in_treatment():
    """Guard against the mis-filing pattern reappearing in the dog module."""
    from api.species.dog_diseases import DISEASES

    offenders = [
        d.get("name")
        for d in DISEASES
        if not (d.get("diagnosis_ja") or "").strip() and (d.get("treatment_ja") or "").lstrip().startswith("診断")
    ]
    assert offenders == [], f"diagnosis mis-filed into treatment: {offenders}"


# ---------------------------------------------------------------------------
# SEO page: the two sections render server-side
# ---------------------------------------------------------------------------


def test_seo_detail_page_renders_clinical_signs_and_diagnosis():
    client = app.test_client()
    resp = client.get("/diseases/dog/canine-parvovirus")
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert "<h2>臨床徴候</h2>" in html
    assert "<h2>診断</h2>" in html


def test_seo_template_has_conditional_sections():
    assert "disease.clinical_signs_ja or disease.clinical_signs" in SEO_TEMPLATE
    assert "disease.diagnosis_ja or disease.diagnosis" in SEO_TEMPLATE
    assert "<h2>臨床徴候</h2>" in SEO_TEMPLATE
    assert "<h2>診断</h2>" in SEO_TEMPLATE


# ---------------------------------------------------------------------------
# SPA (app.js): i18n labels + rendering + related-disease click navigation
# ---------------------------------------------------------------------------


def test_app_js_defines_clinical_and_diagnosis_labels():
    # Both JA and EN i18n dictionaries must define the labels (not fall back to key).
    assert 'dtClinicalSigns:"臨床徴候"' in APP_JS
    assert 'dtDiagnosis:"診断"' in APP_JS
    assert 'dtClinicalSigns:"Clinical Signs"' in APP_JS
    assert 'dtDiagnosis:"Diagnosis"' in APP_JS


def test_app_js_renders_clinical_and_diagnosis_sections():
    # DB detail panel (<dl>) and differential result card both reference the fields.
    assert 't("dtClinicalSigns")' in APP_JS
    assert 't("dtDiagnosis")' in APP_JS
    assert "d.clinical_signs_ja" in APP_JS
    assert "d.diagnosis_ja" in APP_JS


def test_app_js_related_disease_navigation_present():
    # The click-to-navigate related-disease feature: compute + hydrate + click handler.
    assert "function computeRelatedDiseases" in APP_JS
    assert "function hydrateRelatedDiseases" in APP_JS
    assert "related-disease-chip" in APP_JS
    # Clicking a chip must route through navigateToDiseaseDb.
    assert 'e.target.closest(".related-disease-chip")' in APP_JS
    assert "hydrateRelatedDiseases(detail)" in APP_JS


# ---------------------------------------------------------------------------
# Read-time grounding: the fallback serving path must fill empty diagnosis /
# clinical-signs sections (the SQLite build already does; low-memory production
# serves the Python-module path, which previously left 733 records sectionless)
# ---------------------------------------------------------------------------


def test_api_diseases_diagnosis_grounded_at_read_time():
    client = app.test_client()
    for species in ("dog", "cat", "rabbit", "bird"):
        diseases = client.get(f"/api/health-check/diseases?species={species}").get_json()["diseases"]
        # Japanese diagnosis must be present wherever the record stores tests;
        # after grounding no mainstream-species record should ship it empty.
        no_dx_ja = [d["name"] for d in diseases if not (d.get("diagnosis_ja") or "").strip()]
        assert not no_dx_ja, f"{species}: diagnosis_ja empty for {no_dx_ja[:5]}"
        # Clinical signs: never empty in BOTH languages when the record has
        # its own symptom list to ground from.
        both_empty = [
            d["name"]
            for d in diseases
            if not (d.get("clinical_signs") or "").strip()
            and not (d.get("clinical_signs_ja") or "").strip()
            and (d.get("symptoms_display") or [])
        ]
        assert not both_empty, f"{species}: clinical_signs empty both languages for {both_empty[:5]}"


def test_api_diseases_grounding_never_overwrites_curated_prose():
    # A record with curated diagnosis prose must keep it verbatim (grounding
    # only fills blanks). FIP has long-standing curated content.
    client = app.test_client()
    diseases = client.get("/api/health-check/diseases?species=cat").get_json()["diseases"]
    fip = next((d for d in diseases if "Infectious Peritonitis" in (d.get("name") or "")), None)
    assert fip is not None
    # Curated text is substantive, not the short grounded template.
    assert (fip.get("diagnosis_ja") or "").strip()
    assert not (fip.get("diagnosis_ja") or "").startswith("診断は")


# ---------------------------------------------------------------------------
# SPA: cross-link navigation must land on the exactly-named row, not the first
# substring match ("Gastritis" must not open "Chronic Gastritis")
# ---------------------------------------------------------------------------


def test_app_js_navigation_lands_on_exact_match():
    # Shared exact-match picker exists…
    assert "function _pickListItemByName" in APP_JS
    # …and every cross-link navigation routes through it (disease chips,
    # cross-species results, drug links).
    assert APP_JS.count("_pickListItemByName(list,") >= 3
    # Disease rows must expose the names the picker matches against.
    assert 'class="disease-db-item" role="button" tabindex="0" aria-expanded="false" data-name=' in APP_JS
    # No navigation may blindly expand the first row of a filtered list.
    assert 'const first=list.querySelector(".disease-db-item")' not in APP_JS


def test_app_js_compound_interaction_refs_are_linkified():
    """Compound interaction references such as "Ketoconazole/itraconazole" name
    several real drugs in one cell but never resolve as a whole, so they used to
    render as dead text. The cell builder must split on "/" and link each
    component that exists in the manual (one tap from the warning to the drug)."""
    assert "function _interactionDrugCell" in APP_JS
    # The renderer must route through the shared cell builder.
    assert "_interactionDrugCell(ref)" in APP_JS
    # Split-and-resolve logic for compound refs.
    assert 'ref.split("/")' in APP_JS
    assert "interaction-drug-part" in APP_JS
    # EMLA (added to the formulary in batch 33) must be reachable from the
    # anesthesia protocol text via the drug linkifier.
    assert "EMLAクリーム" in APP_JS


def test_app_js_chat_cards_navigate_to_disease_db():
    """Chat candidate cards (free chat + guided consultation finals) must offer a
    click-through that lands on the disease's DB detail via the species-aware
    opener, and the chat containers must carry the delegated handler that makes
    both those buttons and the embedded drug links actually navigate (previously
    the dotted-underline drug links fell through to a bare #drugs hash jump)."""
    # Delegated handler is defined and attached to all three chat containers.
    assert "function _attachChatNavHandlers" in APP_JS
    assert '"chatMessages","landingChatMessages","guidedMessages"' in APP_JS
    # Handler routes drug links through navigateToDrug (exact-match landing)…
    handler = APP_JS.split("function _attachChatNavHandlers", 1)[1].split("\nfunction ", 1)[0]
    assert "navigateToDrug(" in handler
    # …and disease buttons through the species-aware opener (chat species can
    # differ from the DB's loaded species).
    assert "openDiseaseAcrossSpecies(" in handler
    # Both free-chat and guided final-result cards render the button with the
    # data the opener needs.
    assert APP_JS.count('class="chat-disease-open"') >= 2
    assert 'class="chat-disease-open" data-name=' in APP_JS


def test_app_js_related_chips_navigate_via_delegation():
    """Related-drug chips (disease detail / checker results) and drug→disease
    chips (drug detail) are ALSO rendered synchronously from cache on any
    second open — a path that attaches no per-node listeners, so their clicks
    used to fall through to a dead '#diseases' hash. Both chip classes must be
    handled by the delegated container handlers, the cross-species disease
    chip must route through the species-aware opener (which waits for the
    target species' list instead of racing it), and the per-node wiring that
    would double-fire against delegation must stay removed."""
    # Delegated handlers exist for both chip classes.
    assert 'closest(".treatment-drug-chip")' in APP_JS
    assert 'closest(".drug-disease-chip")' in APP_JS
    # The disease chip routes through the species-aware opener with the chip's
    # own species (the drug panel lists diseases of many species).
    assert "openDiseaseAcrossSpecies(dChip.dataset.disease" in APP_JS
    # Per-node listeners must not come back (they double-fire with delegation:
    # the second toggle would immediately close the just-opened panel).
    assert 'querySelectorAll(".drug-disease-chip").forEach' not in APP_JS
    assert 'querySelectorAll(".treatment-drug-chip").forEach' not in APP_JS
    # The fallback href must be a real view hash, not the dead '#diseases'.
    assert 'class="drug-disease-chip" href="#database"' in APP_JS
    assert 'href="#diseases"' not in APP_JS


def test_app_js_anesthesia_considerations_are_clickable():
    """The '🏥 この疾患の麻酔注意事項' box in checker results must (a) render
    server-annotated drug_links as one-tap links to the exact formulary entry,
    (b) offer a jump to the species-synced anesthesia tab, and (c) actually
    have its data: the contraindication rules used to load only when the
    anesthesia tab was opened first, so checker-first users never saw the box
    at all. The fetch-once helper must exist and fire when analysis starts."""
    # Fetch-once helper, wired into both the anesthesia tab and doAnalyze.
    assert "function ensureAnesthesiaContraRules" in APP_JS
    assert APP_JS.count("ensureAnesthesiaContraRules();") >= 2
    # Considerations renderer links resolvable drug patterns…
    renderer = APP_JS.split("function renderAnesthesiaConsiderations", 1)[1].split("\nfunction ", 1)[0]
    assert "drug_links" in renderer
    assert "anesthesia-contra-drug" in renderer
    assert "drug-nav-link" in renderer
    # …and carries the species-synced anesthesia-tab jump.
    assert "anesthesia-nav-link" in renderer
    # The checker-results delegated handler must route that jump (the DB list
    # handler already did; checker results previously dead-ended on the href).
    checker_handler = APP_JS.split('const dbLink=e.target.closest(".disease-db-nav-link")', 1)[1].split(
        "\nfunction ", 1
    )[0]
    assert 'closest(".anesthesia-nav-link")' in checker_handler


def test_app_js_disease_detail_has_differential_pivot():
    """Disease detail → symptom checker pivot: the detail panel's symptom list
    carries a one-tap button that pre-fills the checker with that disease's own
    signs and auto-runs the analysis ("what else presents like this?"), landing
    the reader on the ranked results instead of a bare text list."""
    # The button builder and the runner exist.
    assert "function _differentialCheckButton" in APP_JS
    assert "function runDifferentialFromDisease" in APP_JS
    # The detail template renders the button inside the symptoms definition.
    assert "_differentialCheckButton(d)" in APP_JS
    # The delegated DB-item handler routes the click (cache-rendered details
    # attach no per-node listeners, so delegation is mandatory).
    assert '.closest(".differential-check-btn")' in APP_JS
    assert "runDifferentialFromDisease(diffBtn.dataset.ids)" in APP_JS
    # IDs are validated against the loaded checker vocabulary, the checker view
    # is activated, and the analysis runs (its completion scrolls to results).
    assert "selectedSymptoms=new Set(usable)" in APP_JS
    assert 'switchView("checker")' in APP_JS


def test_app_js_low_confidence_banner_pivots_to_guided_consultation():
    """Checker results → guided consultation pivot: when the low-confidence
    banner fires (≤2 symptoms or top confidence <50%), it offers a one-tap
    button that switches to the chat view, starts the guided consultation with
    the checker's species carried over (guided flow reads currentSpecies), and
    scrolls the chat panel into view — the structured re-questioning is exactly
    the remedy the banner recommends."""
    # The banner renders the pivot button.
    assert 'class="guided-consult-link"' in APP_JS
    # The delegated results-area handler routes the click into guided mode.
    assert '.closest(".guided-consult-link")' in APP_JS
    handler = APP_JS[APP_JS.index('.closest(".guided-consult-link")') :]
    handler = handler[: handler.index("return;")]
    assert 'switchView("chat")' in handler
    assert 'switchChatMode("guided")' in handler
    # switchChatMode("guided") starts the consultation for currentSpecies.
    assert "startGuidedConsultation()" in APP_JS


def test_app_js_drug_detail_links_to_anesthesia_protocols():
    """Anesthesia→drug navigation has existed since the ANES_AGENTS linkifier,
    but the reverse was a dead end: a clinician reading midazolam in the drug
    dictionary had no path to the protocols that use it. The drug detail must
    render a drug→anesthesia jump for agents that appear in the protocol
    tables, and the delegated handler must pre-fill the anesthesia search so
    the landing list is already filtered to that drug."""
    # Reverse-lookup helper against the ANES_AGENTS registry.
    assert "function _anesQueryForDrug" in APP_JS
    # Rendered inside the drug detail panel.
    assert "drug-anes-protocols-link" in APP_JS
    assert "_anesQueryForDrug(d.name" in APP_JS
    # Delegated handler: switches view, pre-fills the search, re-renders when
    # already loaded, and lands scrolled to the list.
    handler = APP_JS.split('closest(".drug-anes-protocols-link")', 1)[1].split("\n    const diffBtn", 1)[0]
    assert 'switchView("anesthesia")' in handler
    assert "anesthesiaSearch" in handler
    assert "anesProto.dataset.anesQuery" in handler
    assert "renderAnesthesiaList()" in handler
    # Abbreviation aliases (e.g. "dex", "mdz") must not drive containment
    # matches — only en/ja aliases are consulted.
    helper = APP_JS.split("function _anesQueryForDrug", 1)[1].split("\nfunction ", 1)[0]
    assert "a.abbr" not in helper


def test_app_js_guided_final_results_pivot_to_checker():
    """Guided-consultation final results → checker pivot (reverse of the
    low-confidence-banner pivot): the interview's confirmed symptom set must be
    carried into the checkbox checker pre-selected and auto-analyzed, so the
    vet can fine-tune signs one checkbox at a time instead of restarting the
    interview. The pivot waits for the target species' checker vocabulary when
    the guided species differs from the loaded one."""
    # Final-results action row renders the pivot button and wires it.
    assert 'id="guidedToChecker"' in APP_JS
    assert "runCheckerFromGuided()" in APP_JS
    # The guided pivot delegates to the shared carry-over helper with its
    # confirmed symptom set (2026-08: refactored so the free-chat result can
    # reuse the same logic).
    fn = APP_JS[APP_JS.index("function runCheckerFromGuided()") :]
    fn = fn[: fn.index("\n}") + 2]
    assert "guidedState.selectedSymptoms" in fn
    assert "_runCheckerWithSymptoms" in fn
    # The shared helper carries the IDs into the checker and analyzes.
    helper = APP_JS[APP_JS.index("function _runCheckerWithSymptoms(") :]
    helper = helper[: helper.index("\n}") + 2]
    assert "selectSpecies(sp)" in helper  # species alignment before applying
    assert "selectedSymptoms=new Set(usable)" in helper
    assert 'switchView("checker")' in helper
    assert "doAnalyze()" in helper
    # Unmappable sets degrade to a toast, never a broken checker state.
    assert "showToast" in helper


def test_app_js_free_chat_results_pivot_to_checker():
    """Free-input chat results → checker pivot (2026-08 round 11): the guided
    mode had this pivot but the free-chat result did not, so adjusting one
    sign after a typed complaint meant re-typing the whole message. The chat
    card footer must render a refine button carrying the extracted symptom IDs
    and the chat species, and the delegated chat-container handler must route
    it through the same shared carry-over helper."""
    # Renderer emits the refine button with the extracted IDs + chat species.
    assert "chat-checker-refine" in APP_JS
    idx = APP_JS.index("chat-checker-refine")
    block = APP_JS[max(0, idx - 900) : idx + 900]
    assert "symptoms.map(s=>s.id)" in block
    assert "chatSpecies" in block
    # Delegated handler (survives innerHTML resets) routes to the shared helper.
    handler = APP_JS[APP_JS.index("function _attachChatNavHandlers(") :]
    handler = handler[: handler.index("\n}") + 2]
    assert ".chat-checker-refine" in handler
    assert "_runCheckerWithSymptoms" in handler
    assert "checker_from_chat" in handler
    # Styled with a visible tap affordance.
    with open("static/css/main.css", encoding="utf-8") as f:
        css = f.read()
    assert ".chat-checker-refine" in css


def test_app_js_free_chat_low_info_warning_pivots_to_guided_mode():
    """Free-chat results ← guided-mode pivot (2026-08 round 12): the free
    chat's low-info warning ('1-2 symptoms only') was text-only, unlike the
    checker's low-confidence banner which offers a one-tap pivot into the
    guided consultation. The warning box must now render a
    .chat-guided-pivot button and the delegated chat handler must route it
    into guided mode (opening the chat view first for the landing chat) and
    scroll the mode toggle into view."""
    # The warning box renders the pivot button (reuses the banner styling).
    assert "chat-guided-pivot" in APP_JS
    assert 'pivotBtn.className="guided-consult-link chat-guided-pivot"' in APP_JS
    # The delegated chat-container handler routes the click.
    assert '.closest(".chat-guided-pivot")' in APP_JS
    handler = APP_JS[APP_JS.index('.closest(".chat-guided-pivot")') :]
    handler = handler[: handler.index("return;")]
    assert 'switchView("chat")' in handler
    assert 'switchChatMode("guided")' in handler
    assert "guided_from_chat_low_info" in handler


def test_app_js_emergency_key_drugs_are_linkified():
    """Emergency-tab key drugs (2026-08 round 13): the key-drug list rendered
    plain text — no path from the highest-urgency view to the full formulary
    entry (dosing detail, contraindications). Rows the server resolved
    (link_name) must render as .drug-nav-link anchors routed by the existing
    emergencyList delegation; unresolved rows stay plain so no tap dead-ends."""
    idx = APP_JS.index("function renderEmergencyProtocol(")
    block = APP_JS[idx : idx + 3000]
    assert "emergency-drug-link" in block and "drug-nav-link" in block
    assert "d.link_name" in block
    # unresolved rows fall back to the plain <strong> label
    assert ":`<strong>" in block.replace(" ", "")
    with open("static/css/main.css", encoding="utf-8") as f:
        css = f.read()
    assert "a.emergency-drug-link" in css


def test_main_css_disables_mobile_font_inflation():
    """Mobile-reported bug (2026-08): differential-diagnosis text rendered far
    larger than authored on phones. The card styles are small (0.8rem bodies),
    but the stylesheet carried no text-size-adjust, so Android Chrome's font
    boosting / iOS Safari's auto text-sizing inflated the long unconstrained
    treatment/pathophysiology paragraphs in the result cards. The html rule
    must pin text-size-adjust to 100% (inflation off; user zoom and browser
    accessibility font settings are unaffected)."""
    css = (PROJECT_ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    html_rule = css[css.index("html{") : css.index("}", css.index("html{"))]
    assert "-webkit-text-size-adjust:100%" in html_rule
    assert "text-size-adjust:100%" in html_rule


def test_app_js_checker_zero_results_pivot_to_guided_and_chat():
    """Checker zero-result state pivots (2026-08 round 14): the 'no matching
    diseases found' empty state was a dead end — tips only, no actionable
    buttons. It must now offer one-tap pivots into the guided consultation and
    the free-text chat (whose 530+ colloquial aliases parse phrasings the
    checkbox vocabulary cannot express), carrying the selected symptom names
    into the chat input so the user rewords instead of starting over."""
    assert "results-empty-guided" in APP_JS
    assert "results-empty-chat" in APP_JS
    # both pivots land on the chat view
    guided = APP_JS[APP_JS.index("guided_from_checker_empty") :][:400]
    assert 'switchView("chat")' in guided and 'switchChatMode("guided")' in guided
    chat = APP_JS[APP_JS.index("chat_from_checker_empty") :][:400]
    assert 'switchView("chat")' in chat and 'switchChatMode("free")' in chat
    # the selected symptom names prefill the free-chat input
    assert "symptomWords" in APP_JS
