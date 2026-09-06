"""Clinical calculator suite (2026-09, competitor-parity feature).

Plumb's ships BSA/lean-weight/conversion calculators and Vetcalculators/Vet Easy
are built around emergency-drug, CRI, fluid, calorie and chocolate-toxicity
calculators — VetDict had none of these beyond the weight×mg/kg row estimate.
The suite lives in app.js with the pure formulas isolated in the VD_CALC object
(no DOM) precisely so these tests can extract that block and verify the actual
arithmetic under node against textbook values:

  - RER = 70 × BW^0.75 (WSAVA Global Nutrition Guidelines 2011)
  - Fluid maintenance dog 132×BW^0.75 / cat 80×BW^0.75 mL/day (AAHA/AAFP 2013);
    deficit = BW × %dehydration × 10 (DiBartola 4th ed)
  - BSA m² = k × (BW g)^(2/3) × 1e-4, k = 10.1 dog / 10.0 cat (Withrow & Vail)
  - Transfusion mL = BW × blood volume (dog 90 / cat 60) × ΔPCV / donor PCV
  - Chocolate theobromine mg/g table (Merck Vet Manual / ASPCA APCC) with the
    20/40/60/100 mg/kg risk tiers
"""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
APP_JS = (ROOT / "static" / "js" / "app.js").read_text(encoding="utf-8")
MAIN_CSS = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
MAIN_HTML = (ROOT / "templates" / "partials" / "_main_content.html").read_text(encoding="utf-8")

NODE = shutil.which("node")


def _extract_vd_calc() -> str:
    m = re.search(r"(const VD_CALC=\{.*?\};)/\*VD_CALC_END\*/", APP_JS, re.S)
    assert m, "VD_CALC block (…};/*VD_CALC_END*/) missing from app.js"
    return m.group(1)


@pytest.mark.skipif(NODE is None, reason="node not available")
def test_vd_calc_formulas_verified_by_node():
    """Run the ACTUAL shipped formulas under node against textbook values."""
    script = (
        _extract_vd_calc()
        + """
const out={
  rer10:VD_CALC.rer(10),                       // 70*10^0.75 ≈ 393.6
  bsaDog10:VD_CALC.bsa(10,"dog"),              // 10.1*(10000)^(2/3)*1e-4 ≈ 0.469
  bsaCat4:VD_CALC.bsa(4,"cat"),                // 10.0*(4000)^(2/3)*1e-4 ≈ 0.252
  maintDog20:VD_CALC.fluidMaintenance("dog",20),   // 132*20^0.75 ≈ 1248.4
  maintCat4:VD_CALC.fluidMaintenance("cat",4),     // 80*4^0.75 ≈ 226.3
  maintOther:VD_CALC.fluidMaintenance("other",2,90), // 180
  deficit:VD_CALC.fluidDeficit(20,8),          // 20*8*10 = 1600
  doseMg:VD_CALC.doseMg(2.5,12),               // 30
  doseMl:VD_CALC.doseVolumeMl(30,15),          // 2
  criDobutamine:VD_CALC.criMlPerHr(VD_CALC.criMgPerHr(5,"ug_kg_min",20),0.5), // 6 mg/hr → 12 mL/hr
  criMgKgHr:VD_CALC.criMgPerHr(0.1,"mg_kg_hr",10),   // 1
  criMgKgDay:VD_CALC.criMgPerHr(24,"mg_kg_day",1),   // 1
  chocoDark:VD_CALC.chocoDoseMgPerKg("dark",50,10),  // 5.5*50/10 = 27.5
  chocoRiskLow:VD_CALC.chocoRisk(19.9),
  chocoRiskGi:VD_CALC.chocoRisk(20),
  chocoRiskCardiac:VD_CALC.chocoRisk(40),
  chocoRiskSeizure:VD_CALC.chocoRisk(60),
  chocoRiskLethal:VD_CALC.chocoRisk(100),
  transDog:VD_CALC.transfusionMl(25,"dog",12,20,40), // 25*90*8/40 = 450
  transCat:VD_CALC.transfusionMl(4,"cat",10,20,40),  // 4*60*10/40 = 60
  theobromine:VD_CALC.chocoTheobromine,
};
console.log(JSON.stringify(out));
"""
    )
    res = subprocess.run([NODE, "-e", script], capture_output=True, text=True, timeout=30)
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert abs(out["rer10"] - 70 * 10**0.75) < 0.01
    assert abs(out["bsaDog10"] - 0.4688) < 0.001
    assert abs(out["bsaCat4"] - 0.2520) < 0.001
    assert abs(out["maintDog20"] - 132 * 20**0.75) < 0.01
    assert abs(out["maintCat4"] - 80 * 4**0.75) < 0.01
    assert out["maintOther"] == 180
    assert out["deficit"] == 1600
    assert out["doseMg"] == 30
    assert out["doseMl"] == 2
    assert abs(out["criDobutamine"] - 12.0) < 1e-9
    assert abs(out["criMgKgHr"] - 1.0) < 1e-9
    assert abs(out["criMgKgDay"] - 1.0) < 1e-9
    assert abs(out["chocoDark"] - 27.5) < 1e-9
    # Risk tier boundaries are inclusive at each threshold (Merck/ASPCA tiers)
    assert out["chocoRiskLow"] == "low"
    assert out["chocoRiskGi"] == "gi"
    assert out["chocoRiskCardiac"] == "cardiac"
    assert out["chocoRiskSeizure"] == "seizure"
    assert out["chocoRiskLethal"] == "lethal"
    assert out["transDog"] == 450
    assert out["transCat"] == 60
    # Theobromine table (Merck Vet Manual / ASPCA APCC)
    assert out["theobromine"] == {"white": 0.01, "milk": 2.1, "dark": 5.5, "baking": 14, "cocoa": 26}


def test_calculator_ui_is_wired():
    """Accordion, tabs, prefill buttons, emergency link and language re-render
    are all present — the suite must be reachable from the drugs tab, the
    emergency tab, and every parseable per-drug dose row."""
    # HTML: accordion in the drugs panel + jump link in the emergency panel
    assert 'id="clinicalCalculators"' in MAIN_HTML
    assert 'id="calcBody"' in MAIN_HTML
    assert 'id="emergencyCalcLink"' in MAIN_HTML
    # i18n keys exist in BOTH dictionaries
    assert APP_JS.count("calcTitle:") >= 2
    assert APP_JS.count("emergencyCalcLink:") >= 2
    # Renderer + all seven panels
    assert "function renderCalculators(" in APP_JS
    for panel in ("dose", "cri", "fluid", "energy", "choco", "transfusion", "bsa"):
        assert f'data-calc-panel="{panel}"' in APP_JS, panel
    # Open-from-anywhere navigation helper with dose prefill
    assert "function openClinicalCalculators(" in APP_JS
    assert 'trackEvent("calc_from_emergency"' in APP_JS
    assert 'trackEvent("calc_from_drug"' in APP_JS
    # Per-drug prefill buttons ride the parsed dose (never a re-parse guess) and
    # are routed by the shared DB-list delegation
    assert APP_JS.count("drug-calc-open") >= 3  # list row + species card + delegated route
    idx = APP_JS.index('e.target.closest(".drug-calc-open")')
    assert idx < APP_JS.index('e.target.closest(".disease-detail.open")', idx), (
        "calc route must run before the open-detail guard swallows the click"
    )
    # Emergency-tab link is wired once (dataset guard) and lands on the CRI tab
    assert 'calcLink.dataset.wired="1"' in APP_JS
    assert 'openClinicalCalculators({tab:"cri"})' in APP_JS
    # Language switch re-renders an already-rendered calculator body
    assert "cb.dataset.rendered&&cb.dataset.rendered!==currentLang" in APP_JS
    # Shared weight persists through the SAME key the drug-list calc uses, so
    # the two features stay in sync
    assert APP_JS.count('"vetdict-drug-weight"') >= 3
    # CSS: tabs, result, risk tiers and the two entry buttons
    for cls in (
        ".calc-tab-btn",
        ".calc-result",
        ".calc-risk-lethal",
        ".drug-calc-open",
        ".emergency-calc-link",
        ".calc-disclaimer",
    ):
        assert cls in MAIN_CSS, cls


def test_calculator_safety_rails_in_source():
    """The clinically load-bearing guardrails must be present in the UI text:
    the always-verify disclaimer, the source-text echo on prefill, the shock
    bolus exclusion, and the chocolate emesis window + disease-entry pivot."""
    assert "計算結果は入力値に依存します" in APP_JS
    assert "必ず原文の用量・経路・頻度を確認" in APP_JS
    assert "ショック蘇生ボーラスは本計算の対象外" in APP_JS
    assert "催吐は摂取後2-4時間以内" in APP_JS
    # Chocolate pivot lands on the real dog module entry name (exact-match nav)
    assert 'openDiseaseAcrossSpecies("Chocolate Toxicosis","dog")' in APP_JS
    # Prefill buttons only render for parseable doses on safe rows — the
    # species-card variant must gate on info.safe
    assert "info.safe?parseDoseRange(" in APP_JS
