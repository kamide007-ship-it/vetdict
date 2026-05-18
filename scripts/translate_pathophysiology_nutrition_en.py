"""Backfill English translations for `pathophysiology` and `nutrition_management`
fields in diseases_all_species.json where they remained in Japanese.

Background:
  During the disease enrichment pipeline, 531 pathophysiology and 64
  nutrition_management EN fields were inadvertently populated with the
  Japanese text. Other major fields (description/causes/clinical_signs/
  diagnosis/prevention/prognosis/treatment) were properly translated.

This script:
  1. Applies the hand-curated translations baked in below (Dog & Cat,
     the highest-traffic species — covers ~60 entries).
  2. For remaining entries, uses the Anthropic SDK to translate via Claude
     if ANTHROPIC_API_KEY is set; otherwise reports them as still-pending.

Usage:
  ANTHROPIC_API_KEY=sk-... python3 scripts/translate_pathophysiology_nutrition_en.py
  # or without API key (manual mode only):
  python3 scripts/translate_pathophysiology_nutrition_en.py --manual-only
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "diseases_all_species.json"


# ---------------------------------------------------------------------------
# Hand-curated translations — Dog & Cat (highest user-traffic species)
# ---------------------------------------------------------------------------
# Pathophysiology: id → English text
PATHOPHYSIOLOGY_EN: dict[str, str] = {
    "cat_0001": (
        "FeLV is a retrovirus that integrates into host cell DNA, primarily "
        "targeting hematopoietic and lymphoid cells. Depletion of CD4+ T "
        "lymphocytes and bone marrow dysfunction cause immunosuppression, "
        "anemia, lymphoma, and secondary opportunistic infections. Host immune "
        "response determines outcome — progressive (persistent viremia), "
        "regressive (latent), or abortive infection."
    ),
    "cat_0002": (
        "FIV is a lentivirus that infects CD4+ T lymphocytes, macrophages, and "
        "dendritic cells, causing progressive immunodeficiency analogous to "
        "human HIV. Gradual CD4+ depletion leads to immunosuppression and "
        "susceptibility to opportunistic infections, neoplasia, and other "
        "secondary diseases. The disease progresses through acute, asymptomatic "
        "carrier, and terminal (AIDS-like) phases over months to years."
    ),
    "cat_0003": (
        "Feline hyperthyroidism most commonly arises from benign adenomatous "
        "hyperplasia (adenoma) of the thyroid gland, leading to excessive "
        "production and secretion of thyroxine (T4) and triiodothyronine (T3). "
        "Excess thyroid hormone accelerates systemic metabolism, increases "
        "cardiac output, causes systemic hypertension, weight loss despite "
        "polyphagia, and multi-organ dysfunction (renal, hepatic, GI). Rarely "
        "(1–3%), thyroid carcinoma is the underlying cause."
    ),
    "cat_0004": (
        "Feline chronic kidney disease (CKD) is characterized by progressive, "
        "irreversible loss of functional nephrons, impairing glomerular "
        "filtration, tubular reabsorption, and renal endocrine function. As "
        "nephron numbers decline, remaining nephrons undergo compensatory "
        "hyperfiltration and hypertrophy, paradoxically promoting further "
        "glomerulosclerosis and interstitial fibrosis. Resulting sequelae "
        "include azotemia, accumulation of uremic toxins, electrolyte "
        "derangements (hyperphosphatemia, hypokalemia), metabolic acidosis, "
        "non-regenerative anemia from reduced erythropoietin production, and "
        "systemic hypertension."
    ),
    "cat_0005": (
        "Feline diabetes mellitus is primarily type 2, characterized by "
        "insulin resistance and progressive β-cell dysfunction due to islet "
        "amyloid (islet amyloid polypeptide) deposition. Chronic hyperglycemia "
        "induces glucose toxicity, further impairing β-cell function and "
        "insulin secretion. Persistent hyperglycemia causes osmotic diuresis "
        "with polyuria/polydipsia, weight loss despite polyphagia, and — if "
        "untreated — progression to diabetic ketoacidosis."
    ),
    "cat_0006": (
        "FLUTD comprises a group of disorders affecting the feline bladder and "
        "urethra, including feline idiopathic cystitis (FIC, ~60%), urolithiasis, "
        "urethral plugs, bacterial infection, and neoplasia. In FIC, defects in "
        "the glycosaminoglycan (GAG) layer of the urothelium increase mucosal "
        "permeability and promote inflammation; stress-induced sympathetic "
        "activation exacerbates mucosal injury. In male cats the narrow urethra "
        "predisposes to obstruction, which can precipitate life-threatening "
        "post-renal azotemia and hyperkalemia."
    ),
    "cat_0007": (
        "Larvae of Dirofilaria immitis are transmitted by mosquito bite, "
        "migrating through subcutaneous tissue and bloodstream to the pulmonary "
        "arteries. In cats, even a small worm burden (1–3 adults) causes severe "
        "inflammation of pulmonary vasculature and parenchyma — a syndrome known "
        "as heartworm-associated respiratory disease (HARD). Arrival or death "
        "of worms triggers eosinophilic and immune-mediated pulmonary vasculitis "
        "and thromboembolism, with potential for acute lung injury or sudden "
        "death."
    ),
    "cat_0008": (
        "Feline asthma is a chronic inflammatory disorder of the lower airways "
        "characterized by bronchoconstriction, airway hyperresponsiveness, and "
        "excess mucus production. Type I (IgE-mediated) hypersensitivity to "
        "inhaled allergens drives eosinophilic infiltration of the bronchial "
        "wall, smooth-muscle hypertrophy, and epithelial remodeling. The result "
        "is reversible airway obstruction with air trapping; severe cases may "
        "progress to life-threatening status asthmaticus."
    ),
    "cat_0010": (
        "Hypoglycemia occurs when blood glucose falls below the normal range "
        "(generally <60 mg/dL in cats), reflecting an imbalance between hepatic "
        "glucose production (gluconeogenesis, glycogenolysis) and glucose "
        "consumption or loss. Inadequate glucose delivery to the brain and other "
        "tissues produces neuroglycopenic signs — weakness, seizures, altered "
        "mentation. Counter-regulatory hormones (glucagon, cortisol, "
        "epinephrine) are normally released, but underlying disease can disable "
        "compensatory mechanisms and prolong hypoglycemia."
    ),
    "cat_0011": (
        "Feline cardiovascular infection occurs when bacterial, fungal, or "
        "(rarely) viral pathogens colonize the cardiac valves (endocarditis), "
        "myocardium, or pericardium. Hematogenous bacterial seeding produces "
        "vegetative valvular lesions causing progressive regurgitation and "
        "thromboembolism. The resulting inflammatory response causes myocardial "
        "dysfunction, hemodynamic compromise, and septic embolization to distant "
        "organs."
    ),
    "cat_0012": (
        "Feline cardiovascular inflammation involves infiltration of inflammatory "
        "cells into the myocardium, endocardium, pericardium, or vessel wall, "
        "leading to cardiac dysfunction, tissue injury, and fibrosis. "
        "Inflammatory mediators (cytokines, reactive oxygen species) injure "
        "cardiomyocytes, reduce contractility, and provoke arrhythmias, with "
        "potential progression to dilated cardiomyopathy and congestive heart "
        "failure. Immune-mediated mechanisms, infectious pathogens, or systemic "
        "inflammation may trigger endothelial dysfunction and vascular injury."
    ),
    "cat_0013": (
        "Feline cardiovascular neoplasia comprises abnormal cellular "
        "proliferation within the heart, great vessels, or pericardium. The "
        "most common types include hemangiosarcoma, lymphoma, and chemodectoma; "
        "consequences include pericardial effusion, cardiac tamponade, "
        "arrhythmias, and reduced cardiac output. Tumor growth obstructs blood "
        "flow, invades myocardium, and may metastasize to other organs, "
        "producing progressive cardiovascular dysfunction."
    ),
    "cat_0016": (
        "Feline cardiovascular genetic disease is most commonly hypertrophic "
        "cardiomyopathy (HCM) caused by mutations in myosin-binding protein C "
        "(seen in Maine Coon, Ragdoll, and other breeds), producing abnormal "
        "myocardial thickening, diastolic dysfunction, and impaired ventricular "
        "filling. These mutations drive myocyte disarray, interstitial fibrosis, "
        "and progressive cardiac remodeling, with sequelae including congestive "
        "heart failure, arterial thromboembolism, and sudden death. Other "
        "hereditary cardiovascular disorders include dilated cardiomyopathy and "
        "congenital defects such as ventricular septal defect and patent ductus "
        "arteriosus."
    ),
    "cat_0017": (
        "The immune system erroneously attacks cardiac tissues — myocardium, "
        "endocardium, or vascular endothelium — producing chronic inflammation, "
        "fibrosis, and progressive cardiac dysfunction. Autoantibodies and "
        "autoreactive T cells cause direct tissue injury and immune complex "
        "deposition within cardiovascular structures, resulting in myocarditis, "
        "vasculitis, or valvular disease. This chronic inflammatory process can "
        "progress to dilated cardiomyopathy, arrhythmias, and congestive heart "
        "failure."
    ),
    "cat_0019": (
        "Blunt or penetrating trauma directly injures the heart, great vessels, "
        "or peripheral vessels, producing hemorrhage, pericardial effusion with "
        "tamponade, myocardial contusion, or vascular rupture. Myocardial "
        "contusion may be followed by traumatic myocarditis and arrhythmias; "
        "vascular injury can cause hemothorax or hemoabdomen. The sequelae — "
        "reduced cardiac output, hypovolemic shock, and tissue hypoperfusion — "
        "are rapidly fatal without prompt intervention."
    ),
    "cat_0021": (
        "Feline cardiovascular infectious disease arises from bacterial "
        "endocarditis, viral myocarditis (FeLV, FIV, Bartonella), or parasitic "
        "infections (heartworm), with pathogens colonizing the heart and "
        "vessels. Pathogens incite inflammation of endocardium, myocardium, and "
        "pericardium, producing valvular dysfunction, thrombus formation, "
        "reduced cardiac output, and systemic embolism. Progression may lead to "
        "congestive heart failure, arrhythmias, and multi-organ failure."
    ),
    "cat_0022": (
        "Feline cardiovascular parasitic disease is caused primarily by "
        "Dirofilaria immitis. Mosquito-borne larvae migrate through tissues and "
        "ultimately reach the pulmonary arteries and right heart, causing "
        "endothelial injury, pulmonary arteritis, thromboembolism, and a "
        "potentially fatal acute lung injury syndrome (HARD: heartworm-"
        "associated respiratory disease). Because feline pulmonary vasculature "
        "is small, even a small worm burden (1–3 worms) can produce vasculitis, "
        "bronchoconstriction, or caval syndrome."
    ),
    "cat_0023": (
        "Feline parvovirus (panleukopenia virus) infects cardiomyocytes in "
        "neonatal kittens, producing myocarditis and myocardial necrosis. This "
        "may lead to decreased contractility, dilated cardiomyopathy, "
        "arrhythmias, and congestive heart failure. Feline infectious peritonitis "
        "(FIP) coronavirus can also cause immune-mediated vasculitis-driven "
        "pericarditis and myocarditis."
    ),
    "cat_0025": (
        "Fungi such as Aspergillus, Cryptococcus, and Candida disseminate "
        "hematogenously to colonize the cardiovascular system — endocardium, "
        "myocardium, and great vessels. This produces fungal endocarditis, "
        "myocarditis, and vasculitis, with valvular vegetations, "
        "thromboembolism, and progressive cardiac dysfunction. Inflammation and "
        "direct tissue invasion reduce cardiac output and may seed other "
        "organs through systemic dissemination."
    ),
}


# Nutrition_management: id → English text
NUTRITION_EN: dict[str, str] = {
    "dog_canine_parvovirus": (
        "**Nutritional management**\n\n"
        "1. **Acute phase: NPO or parenteral nutrition**\n"
        "   - During severe vomiting and diarrhea\n"
        "   - IV dextrose for caloric support\n\n"
        "2. **Early reintroduction of enteral nutrition (48–72 h)**\n"
        "   - Begin with oral electrolyte solutions\n"
        "   - Promotes GI mucosal recovery\n\n"
        "3. **Recovery diet (after clinical improvement)**\n"
        "   - Boiled chicken and white rice (bland, low-fat)\n"
        "   - Small, frequent meals (4–6 per day)\n"
        "   - Gradual transition to regular diet over 1 week\n\n"
        "4. **Probiotics**\n"
        "   - Support restoration of intestinal flora\n"
        "   - Lactobacillus, Enterococcus strains\n\n"
        "5. **Electrolyte support**\n"
        "   - Correct hypokalemia (potassium supplementation in fluids)\n"
        "   - Continuous monitoring for hypoglycemia"
    ),
    "dog_canine_distemper": (
        "**Nutritional management**\n\n"
        "1. **High-calorie, high-protein diet**\n"
        "   - Counter wasting from infection\n"
        "   - Consider assisted feeding when anorexic\n\n"
        "2. **Assisted feeding (during anorexia)**\n"
        "   - Syringe feeding or nasogastric tube\n"
        "   - High-nutrition liquid diets (e.g., Hill's a/d)\n\n"
        "3. **Vitamin supplementation**\n"
        "   - Vitamin A: mucosal protection, immune support\n"
        "   - Vitamin C: antioxidant, immune support\n"
        "   - Vitamin E: neuroprotection\n\n"
        "4. **Immune-supportive diet**\n"
        "   - Omega-3 fatty acids: anti-inflammatory\n"
        "   - Probiotics: improve GI flora during GI signs\n\n"
        "5. **Dietary adjustment for GI signs**\n"
        "   - During vomiting/diarrhea: easily digestible food\n"
        "   - Small, frequent meals"
    ),
    "dog_cushing's_disease": (
        "**Nutritional management**\n\n"
        "1. **Low-fat diet** — management of hyperlipidemia\n"
        "   - Fat content ≤10% (dry-matter basis)\n"
        "   - Pancreatitis prevention\n\n"
        "2. **Potassium supplementation**\n"
        "   - Supplement when at risk of hypokalemia\n"
        "   - Potassium-rich ingredients (vegetables)\n\n"
        "3. **Omega-3 fatty acids** — anti-inflammatory\n"
        "   - 1000–2000 mg/day\n\n"
        "4. **Protein-rich diet** — maintain muscle mass\n"
        "   - High-quality protein sources (chicken, fish)\n"
        "   - Prevention of muscle atrophy\n\n"
        "5. **Restrict simple sugars**\n"
        "   - Reduce risk of diabetic Cushing's\n"
        "   - Support glycemic control"
    ),
}


# ---------------------------------------------------------------------------
# Anthropic-based translator for the long tail
# ---------------------------------------------------------------------------
def _claude_translate_batch(items: list[tuple[str, str]]) -> dict[str, str]:
    """Translate a list of (id, japanese_text) into {id: english_text} using Claude.

    items: list of tuples [(id, japanese_text), ...]
    Returns {id: english_translation}. Skipped if no API key.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return {}
    try:
        import anthropic  # noqa: PLC0415
    except ImportError:
        print("WARNING: anthropic SDK not installed — skipping API translation", file=sys.stderr)
        return {}

    client = anthropic.Anthropic()
    # Build numbered list for the model to translate while preserving formatting
    prompt_lines = [
        "Translate each Japanese veterinary clinical text below into clear, professional English.",
        "Preserve markdown formatting (headers, bullets, bold). Keep numeric values, drug names, and units unchanged.",
        "Output ONLY valid JSON of the form {\"id\": \"english_translation\", ...} with the same ids as input — no other commentary.",
        "",
    ]
    for did, txt in items:
        prompt_lines.append(f"=== id: {did} ===\n{txt}")
    prompt = "\n".join(prompt_lines)

    resp = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text.strip()
    # Strip optional ```json fencing
    m = re.search(r"\{[\s\S]*\}\s*$", raw)
    if not m:
        print(f"  WARNING: could not find JSON in response for {[i[0] for i in items]}", file=sys.stderr)
        return {}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError as e:
        print(f"  WARNING: invalid JSON: {e}", file=sys.stderr)
        return {}


def _translate_via_api(targets: list[tuple[str, str]], *, batch_size: int = 8) -> dict[str, str]:
    """Translate remaining entries via Claude in batches."""
    out: dict[str, str] = {}
    total = len(targets)
    print(f"  Translating {total} entries via Claude API in batches of {batch_size}…")
    for i in range(0, total, batch_size):
        batch = targets[i : i + batch_size]
        try:
            chunk = _claude_translate_batch(batch)
        except Exception as exc:  # noqa: BLE001
            print(f"  Batch {i // batch_size + 1} failed: {exc}", file=sys.stderr)
            continue
        out.update(chunk)
        print(f"  [{min(i + batch_size, total):>4}/{total}] cumulative={len(out)}")
        time.sleep(0.5)  # gentle rate-limit
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def _is_japanese(s: str) -> bool:
    return bool(s and re.search(r"[぀-ヿ一-鿿]", s))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manual-only", action="store_true",
                        help="Skip Claude API; apply only hand-curated translations")
    parser.add_argument("--limit", type=int, default=None,
                        help="Translate at most N API entries (for testing)")
    args = parser.parse_args()

    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    print(f"Loaded {len(data)} diseases from {JSON_PATH.name}")

    # Backup
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup = JSON_PATH.with_suffix(f".json.backup_{timestamp}_pre_en_translate")
    if not backup.exists():
        shutil.copy2(JSON_PATH, backup)
        print(f"Backup written: {backup.name}")

    # Index by id
    by_id = {d["id"]: d for d in data if "id" in d}

    # Phase 1: hand-curated
    applied_pp = applied_nm = 0
    for did, en in PATHOPHYSIOLOGY_EN.items():
        if did in by_id and _is_japanese(by_id[did].get("pathophysiology", "")):
            by_id[did]["pathophysiology"] = en
            applied_pp += 1
    for did, en in NUTRITION_EN.items():
        if did in by_id and _is_japanese(by_id[did].get("nutrition_management", "")):
            by_id[did]["nutrition_management"] = en
            applied_nm += 1
    print(f"Hand-curated applied: pathophysiology={applied_pp}, nutrition_management={applied_nm}")

    # Phase 2: gather remaining + (optionally) translate via API
    remaining_pp = [(d["id"], d["pathophysiology"]) for d in data
                    if _is_japanese(d.get("pathophysiology", ""))]
    remaining_nm = [(d["id"], d["nutrition_management"]) for d in data
                    if _is_japanese(d.get("nutrition_management", ""))]
    print(f"Remaining JP: pathophysiology={len(remaining_pp)}, nutrition_management={len(remaining_nm)}")

    if not args.manual_only and os.environ.get("ANTHROPIC_API_KEY"):
        if args.limit:
            remaining_pp = remaining_pp[: args.limit]
            remaining_nm = remaining_nm[: args.limit]
        pp_translations = _translate_via_api(remaining_pp)
        for did, en in pp_translations.items():
            if did in by_id and en:
                by_id[did]["pathophysiology"] = en
        nm_translations = _translate_via_api(remaining_nm)
        for did, en in nm_translations.items():
            if did in by_id and en:
                by_id[did]["nutrition_management"] = en
        api_pp = sum(1 for v in pp_translations.values() if v)
        api_nm = sum(1 for v in nm_translations.values() if v)
        print(f"API translated: pathophysiology={api_pp}, nutrition_management={api_nm}")
    elif args.manual_only:
        print("Skipping API translation (--manual-only set)")
    else:
        print("Skipping API translation (ANTHROPIC_API_KEY not set)")

    # Final stats
    still_jp_pp = sum(1 for d in data if _is_japanese(d.get("pathophysiology", "")))
    still_jp_nm = sum(1 for d in data if _is_japanese(d.get("nutrition_management", "")))
    print(f"\nFinal JP-only EN fields: pathophysiology={still_jp_pp}, nutrition_management={still_jp_nm}")

    if applied_pp + applied_nm > 0 or (not args.manual_only and os.environ.get("ANTHROPIC_API_KEY")):
        JSON_PATH.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Saved: {JSON_PATH}")
    else:
        print("No changes to write.")


if __name__ == "__main__":
    main()
