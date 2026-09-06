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


@pytest.mark.skipif(NODE is None, reason="node not available")
def test_vd_calc_iris_conversion_lean_weight_verified_by_node():
    """第36弾 additions: IRIS 2023 CKD staging boundaries, SI unit conversion
    factors, and the Laflamme BCS-9 ideal-weight estimate — run under node."""
    script = (
        _extract_vd_calc()
        + """
const out={
  iw8:VD_CALC.idealWeight(30,8),           // 30/(1+0.10*3) ≈ 23.0769
  iw5:VD_CALC.idealWeight(30,5),           // BCS≤5 → current weight
  iwBad:VD_CALC.idealWeight(30,0),         // invalid BCS → null
  glu:VD_CALC.convert("glucose",100,true), // 100 mg/dL → 5.55 mmol/L
  gluBack:VD_CALC.convert("glucose",5.55,false),
  creat:VD_CALC.convert("creatinine",2,true), // 176.8 µmol/L
  tempF:VD_CALC.convert("temp",103.1,true),   // ≈39.5 °C
  lb:VD_CALC.convert("weight_lb",10,true),    // 4.536 kg
  badKey:VD_CALC.convert("nope",1,true),      // null
  // IRIS 2023 creatinine boundaries (dog 1.4/2.9/5.0, cat 1.6/2.9/5.0 mg/dL)
  dC:[1.3,1.4,2.8,2.9,5.1].map(v=>VD_CALC.irisCreatStage("dog",v)),
  cC:[1.5,1.6].map(v=>VD_CALC.irisCreatStage("cat",v)),
  // IRIS 2023 SDMA bands (dog 18-35/36-54/>54, cat 18-25/26-38/>38 µg/dL)
  dS:[17,18,36,54,55].map(v=>VD_CALC.irisSdmaStage("dog",v)),
  cS:[25,26,38,39].map(v=>VD_CALC.irisSdmaStage("cat",v)),
  // UPC substage: borderline is inclusive of the upper bound (dog 0.5 / cat 0.4)
  upc:[VD_CALC.irisUpcSubstage("dog",0.1),VD_CALC.irisUpcSubstage("dog",0.5),
       VD_CALC.irisUpcSubstage("dog",0.51),VD_CALC.irisUpcSubstage("cat",0.41)],
  bp:[139,140,160,180].map(v=>VD_CALC.irisBpSubstage(v)),
};
console.log(JSON.stringify(out));
"""
    )
    res = subprocess.run([NODE, "-e", script], capture_output=True, text=True, timeout=30)
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert abs(out["iw8"] - 30 / 1.3) < 1e-9
    assert out["iw5"] == 30
    assert out["iwBad"] is None
    assert abs(out["glu"] - 5.55) < 1e-9
    assert abs(out["gluBack"] - 100) < 1e-6
    assert abs(out["creat"] - 176.8) < 1e-9
    assert abs(out["tempF"] - 39.5) < 0.01
    assert abs(out["lb"] - 4.536) < 1e-9
    assert out["badKey"] is None
    assert out["dC"] == [1, 2, 2, 3, 4]
    assert out["cC"] == [1, 2]
    assert out["dS"] == [1, 2, 3, 3, 4]
    assert out["cS"] == [2, 3, 3, 4]
    assert out["upc"] == ["NP", "BP", "P", "P"]
    assert out["bp"] == ["normo", "pre", "hyper", "severe"]


@pytest.mark.skipif(NODE is None, reason="node not available")
def test_parse_dose_range_rejects_cri_and_degenerate_doses():
    """parseDoseRange gates the per-drug prefill button. It must never treat a
    CRI/per-day dose (mg/kg/hr, mg/kg/day, mg/kg/min) as a single dose, must
    skip past a leading CRI to a genuine bolus in the same text, and must
    return null for degenerate (0 or inverted) parses — real rows: diltiazem
    horse '0.125 mg/kg/min IV CRI', colistin '2-5 mg/kg/day IV divided'."""
    m = re.search(r"function parseDoseRange\(doseText\)\{[\s\S]*?\n\}", APP_JS)
    assert m, "parseDoseRange missing"
    script = (
        m.group(0).replace("function parseDoseRange", "globalThis.parseDoseRange=function")
        + """
const cases=[
 ["0.125 mg/kg/min IV CRI", null],
 ["CMS: 2-5 mg/kg/day IV divided q8-12h", null],
 ["0.5-1 mg/kg IM/SC q4-6h; 0.1-0.3 mg/kg/hr CRI", {min:0.5,max:1,unit:"mg"}],
 ["1-2 mg/kg/day CRI; bolus 2 mg/kg", {min:2,max:2,unit:"mg"}],
 ["CRI: 5-40 \\u03bcg/kg/hr (load: 1-2 \\u03bcg/kg IV)", {min:1,max:2,unit:"\\u00b5g"}],
 ["2 mg/kg IV", {min:2,max:2,unit:"mg"}],
 ["5-10 \\u00b5g/kg IM", {min:5,max:10,unit:"\\u00b5g"}],
 ["10-5 mg/kg (inverted)", null],
 ["1,000 \\u00b5g/kg", null],
 ["12.5-25 mg/dog", null],
];
let bad=0;
for(const [t,exp] of cases){
 if(JSON.stringify(parseDoseRange(t))!==JSON.stringify(exp)){bad++;console.error("FAIL:",t,JSON.stringify(parseDoseRange(t)));}
}
console.log(JSON.stringify({bad}));
"""
    )
    res = subprocess.run([NODE, "-e", script], capture_output=True, text=True, timeout=30)
    assert res.returncode == 0, res.stderr
    assert json.loads(res.stdout.strip().splitlines()[-1])["bad"] == 0, res.stderr


def test_calculator_input_hardening_in_source():
    """Edge-case guards from the 第36弾 error audit stay in place:
    negative typed values are treated as empty (all calculator quantities are
    non-negative), an inverted dose range is normalised instead of rendering
    '5–2 mg', and a language re-render preserves typed values and the active
    tab instead of wiping the form."""
    assert "isNaN(v)||v<0?null:v" in APP_JS
    assert "Math.max(hiRaw,lo)" in APP_JS
    # language re-render snapshot/restore + silent tab restore
    assert "prevVals" in APP_JS
    assert "_calcSwitchTab(prevTab,true)" in APP_JS
    # analytics stays silent on programmatic tab restore
    assert 'if(!silent)trackEvent("calculator_tab"' in APP_JS
    # duplicate print function cleanup must not regress (merge artifact removed)
    assert APP_JS.count("function printAnesthesiaChecklist(") == 1


def test_iris_and_conversion_panels_wired():
    """New IRIS / unit-conversion tabs and the BCS lean-weight row are wired,
    including the direction-select rebuild and the AKI/dehydration guard note."""
    for panel in ("iris", "conv"):
        assert f'data-calc-panel="{panel}"' in APP_JS, panel
    for el_id in (
        "calcIrisSpecies",
        "calcIrisCreat",
        "calcIrisCreatUnit",
        "calcIrisSdma",
        "calcIrisUpc",
        "calcIrisSbp",
        "calcConvKey",
        "calcConvDir",
        "calcConvVal",
        "calcEnergyBcs",
    ):
        # number inputs are built via the num() helper, selects inline — either
        # way the element id appears as a quoted string in the template source
        assert f'"{el_id}"' in APP_JS, el_id
    # conversion direction select rebuilds when the measurement changes
    assert 'if(e.target.id==="calcConvKey")_calcPopulateConvDir()' in APP_JS
    # IRIS staging is only valid on stable CKD — the guard note must ship
    assert "AKI・脱水・静脈輸液中の値では判定しない" in APP_JS
    # discordant creatinine/SDMA guidance (IRIS 2023) is surfaced
    assert "クレアチニンとSDMAのステージが乖離" in APP_JS
    # weight-loss factors are marked so BCS switches the basis to ideal weight
    assert '"1.0_wl"' in APP_JS and '"0.8_wl"' in APP_JS
    assert 'fv.indexOf("_wl")>=0' in APP_JS
    # chocolate risk tiers are canine data — the species caveat must ship
    assert "リスク閾値は犬のデータ" in APP_JS


def test_owner_handout_is_wired_and_omits_dosing():
    """Owner handout print (Plumb's/Vetlexicon parity): reachable from the
    disease-DB detail via delegation, and the generated sheet deliberately
    prints NO treatment_protocol text (no drug doses reach owners — the vet
    writes individual instructions into the blank memo area)."""
    assert "function printOwnerHandout(" in APP_JS
    assert APP_JS.count("owner-handout-btn") >= 2  # template button + delegated route
    idx = APP_JS.index('e.target.closest(".owner-handout-btn")')
    assert idx < APP_JS.index('e.target.closest(".disease-detail.open")', idx), (
        "handout route must run before the open-detail guard swallows the click"
    )
    body = APP_JS[APP_JS.index("function printOwnerHandout(") :]
    body = body[: body.index("/* ===== Shared helpers ===== */")]
    # The handout must not embed the clinical treatment fields
    assert "treatment_ja" not in body and "d.treatment" not in body
    assert "notes-area" in body  # vet's hand-written instruction area
    assert "獣医師の指示どおり" in body
    assert 'trackEvent("owner_handout_print"' in APP_JS
    assert ".owner-handout-btn" in MAIN_CSS


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


@pytest.mark.skipif(NODE is None, reason="node not available")
def test_mgcs_verified_by_node_and_wired():
    """第37弾: Modified Glasgow Coma Scale (Platt 2001 JVIM). Band boundaries
    3-8 grave / 9-14 guarded / 15-18 good are run under node against the
    shipped code, and the tab ships with the stabilise-first / never-prognose-
    on-a-single-score caveats."""
    script = (
        _extract_vd_calc()
        + """
const out={
  total:VD_CALC.mgcsTotal(6,6,6),
  min:VD_CALC.mgcsTotal(1,1,1),
  nan:VD_CALC.mgcsTotal(NaN,3,3),
  range:VD_CALC.mgcsTotal(7,3,3),
  bands:[3,8,9,14,15,18].map(v=>VD_CALC.mgcsBand(v)),
  oob:[VD_CALC.mgcsBand(2),VD_CALC.mgcsBand(19)],
};
console.log(JSON.stringify(out));
"""
    )
    res = subprocess.run([NODE, "-e", script], capture_output=True, text=True, timeout=30)
    assert res.returncode == 0, res.stderr
    out = json.loads(res.stdout)
    assert out["total"] == 18 and out["min"] == 3
    assert out["nan"] is None and out["range"] is None
    assert out["bands"] == ["grave", "grave", "guarded", "guarded", "good", "good"]
    assert out["oob"] == [None, None]
    # UI wiring: tab, three category selects, dog-validation + caveat text
    assert 'data-calc-panel="mgcs"' in APP_JS
    for el_id in ("calcMgcsMotor", "calcMgcsBrainstem", "calcMgcsConsciousness"):
        assert f'"{el_id}"' in APP_JS, el_id
    assert "Platt 2001" in APP_JS
    assert "スコア単独で予後を断定しない" in APP_JS


@pytest.mark.skipif(NODE is None, reason="node not available")
def test_owner_handout_tips_curated_and_resolvable():
    """第37弾: per-disease home-care tips for the owner handout. Every entry
    must be bilingual with a reference, contain ZERO dosing language (the
    handout's core safety contract), and every match-pattern set must resolve
    to at least one real disease name in its gated species in the served DB
    (mirror test — renames/dedupe that orphan a tip fail CI)."""
    m = re.search(r"const OWNER_HANDOUT_TIPS=\[[\s\S]*?\n\];", APP_JS)
    assert m, "OWNER_HANDOUT_TIPS registry missing"
    script = (
        m.group(0).replace("const OWNER_HANDOUT_TIPS", "globalThis.T")
        + """
console.log(JSON.stringify(T.map(t=>({match:t.match,sp:t.sp||null,ja:t.ja,en:t.en,ref:t.ref||""}))));
"""
    )
    res = subprocess.run([NODE, "-e", script], capture_output=True, text=True, timeout=30)
    assert res.returncode == 0, res.stderr
    tips = json.loads(res.stdout)
    assert len(tips) >= 25
    dose_re = re.compile(r"(mg/kg|mcg|µg/|\bIU\b|q\d+h|mg/|mL/kg|単位/)")
    for t in tips:
        assert t["ja"] and t["en"] and t["ref"], t["match"]
        for s in t["ja"] + t["en"]:
            assert not dose_re.search(s), f"dosing language in owner tip: {s[:60]}"
    # Handout integration: resolver + section title + ref line
    assert "function _ownerTipsFor(" in APP_JS
    assert "_ownerTipsFor(d)" in APP_JS
    assert "ご家庭でのケアのポイント" in APP_JS
    # Mirror check against the served DB (skip when DB not built locally)
    db = ROOT / "instance" / "vetdict.db"
    if not db.exists() or db.stat().st_size < 1_000_000:
        pytest.skip("served DB not built")
    import sqlite3

    conn = sqlite3.connect(db)
    rows = conn.execute("select species, name, name_ja from diseases").fetchall()
    conn.close()

    def base(s):
        return re.sub(r"（[^）]*）|\([^)]*\)", "", (s or "")).strip().lower()

    by_sp = {}
    for sp, n, nj in rows:
        by_sp.setdefault(sp, []).append((base(n), base(nj)))
    for t in tips:
        sps = t["sp"] or list(by_sp.keys())
        hit = any(
            any((mm.lower() in ne) or (mm.lower() in nj) for mm in t["match"])
            for sp in sps
            for ne, nj in by_sp.get(sp, [])
        )
        assert hit, f"owner tip pattern resolves to no served disease: {t['match']}"
