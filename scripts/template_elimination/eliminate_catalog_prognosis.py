"""Replace category-*catalogue* prognosis text with disease-specific prognosis.

The legacy prognosis generator emitted, for every disease in a category, the
**whole category's** prognosis catalogue — e.g. every feline neoplasm (including
systemic lymphomas) carried a paragraph that opens with "良性腫瘍は完全切除に
より治癒が期待できる" and then enumerates benign/malignant/multimodal outcomes.
This is two defects at once:

1. **Clinically wrong** for many specific diseases. A renal/GI lymphoma is a
   systemic malignancy that is *not* cured by excision, yet the shared text
   leads with the benign-tumour-is-curable line. A reviewing clinician spots
   this immediately on launch.
2. **Generic-template UX.** The disease name is slotted into the paragraph, so
   the strings are technically unique (exact-match dedup misses them) while
   reading identically disease after disease.

``clinical_fields_generator.gen_prognosis_ja`` now returns a statement matched
to the *specific* disease — a tumour is classified into benign / lymphoid /
mast-cell / melanoma / carcinoma / sarcoma / unspecified and given the
appropriate prognosis, and each enumerated-catalogue category selects only the
clause whose keywords match the disease name. This pass detects the old
catalogue text (by fingerprint sentence + normalised cluster) and regenerates
it through that improved generator.

Run::

    python3 scripts/template_elimination/eliminate_catalog_prognosis.py --preview
    python3 scripts/template_elimination/eliminate_catalog_prognosis.py --apply

then rebuild the delivery DB with ``python3 scripts/migrate_to_sqlite.py``.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    gen_prognosis_en,
    gen_prognosis_ja,
    resolve_true_category,
)
from scripts.template_elimination.eliminate_generic_descriptions import _norm  # noqa: E402
from scripts.template_elimination.eliminate_templates import SPECIES_NORM  # noqa: E402

JSON_PATH = ROOT / "diseases_all_species.json"

# Distinctive sentences from the *old* category prognosis catalogues. Any
# prognosis containing one of these enumerates several unrelated sub-diseases
# and therefore is category-catalogue boilerplate, not a per-disease prognosis —
# regardless of how small its exact-duplicate cluster is.
_CATALOG_FINGERPRINTS: frozenset[str] = frozenset(
    {
        # neoplasia (the clinically wrong benign-curable lead)
        "良性腫瘍は完全切除により治癒が期待できる。",
        "集学的治療（外科＋化学療法＋放射線療法）により単独治療より生存期間延長が期待できる場合がある。",
        # endocrine_metabolic
        "クッシング症候群: トリロスタン・ミトタンによる症状制御で中央生存2年以上。",
        "甲状腺機能亢進症: I-131治療は治癒可能（猫95%以上）、メチマゾール内服も長期管理良好。",
        # renal_urinary
        "FLUTD/FIC: 自然寛解率約50%だが再発率も高い、ストレス管理で長期予後改善。",
        "早期CKD（ステージ2）: 適切な管理（腎臓食・降圧療法・低リン療法）で中央生存3年以上。",
        # cardiac
        "FATE（猫）: 急性期生存率約30-50%、再発予防が重要。",
        "DCM（ドーベルマン）は予後不良、HCM（猫）は症状発現後の中央生存約1.3年。",
        # respiratory_other
        "短頭種気道症候群: 外科的気道形成術（軟口蓋切除・鼻孔形成）で良好予後。",
        # gastrointestinal
        "GDV（犬）: 早期手術で生存率80%以上、診断遅延で予後悪化。",
        "消化器腫瘍: リンパ腫は化学療法で寛解可能だが、その他の腺癌・肉腫は予後不良。",
        # neurological
        "特発性てんかん: 抗痙攣薬で発作頻度低下、寿命に近い予後。",
        "椎間板疾患: 早期手術で良好回復、深部痛覚消失例は予後不良。",
        # ophthalmic
        "白内障: 外科的水晶体摘出術で視力回復可能。",
        "緑内障: 急性期治療で視覚温存可能、慢性期は視覚消失多く義眼または眼球摘出。",
        # musculoskeletal
        "靭帯損傷: TPLO・TTA・側方制動術で良好予後（犬の十字靭帯）。",
        # dental
        "歯周病: 早期スケーリング・適切な口腔ケアで進行抑制。",
        "口腔腫瘍: 良性は完全切除で治癒、悪性（扁平上皮癌）は予後不良。",
        # dermatological
        "皮膚糸状菌症: 抗真菌薬で治癒可能（4-12週）。",
        "慢性アトピー性皮膚炎: 長期管理（環境・薬物・免疫療法）で症状制御可能、根治は困難。",
        # hematological
        "IMTP: 適切な免疫抑制療法で多くは良好予後。",
        "非再生性貧血: 基礎疾患（FeLV・FIV・CKD等）の予後に依存。",
        # reproductive
        "子宮蓋膿症: 卵巣子宮全摘術で良好予後、早期診断が鍵。",
        # generic content-free filler
        "継続的なモニタリングと飼育環境管理が長期予後改善に重要である。",
    }
)


def _has_fingerprint(text: str) -> bool:
    return any(fp in text for fp in _CATALOG_FINGERPRINTS)


# The English ``prognosis`` field was emitted as a single category paragraph
# reused verbatim across thousands of diseases (no disease name embedded), so
# the neoplasia paragraph — including its "Benign tumors carry an excellent
# prognosis with complete excision" lead — sat on every malignant tumour too.
# A distinctive sentence per category paragraph identifies that boilerplate.
_CATALOG_FINGERPRINTS_EN: frozenset[str] = frozenset(
    {
        "Benign tumors carry an excellent prognosis with complete excision.",
        "Low-grade malignancies may be controlled for years with multimodal treatment.",
        "Early aggressive therapy significantly improves survival across all infectious disease categories.",
        "Diabetes mellitus has a fair to good prognosis",
        "IRIS stage",
        "Prognosis for parasitic",
        "Prognosis for nutritional",
        "Prognosis for toxic",
        "Prognosis for traumatic",
        "Prognosis for cardiac",
        "Prognosis for endocrine",
        "Prognosis for gastrointestinal",
        "Prognosis for musculoskeletal",
        "Prognosis for neurological",
        "Prognosis for ophthalmic",
        "Prognosis for dermatological",
        "Prognosis for hematological",
        "Prognosis for respiratory",
        "Prognosis for reproductive",
        "Prognosis for dental",
        "varies by underlying etiology and timing of intervention",
        "Early diagnosis and treatment improve outcomes in most cases",
    }
)


def _has_fingerprint_en(text: str) -> bool:
    return any(fp in text for fp in _CATALOG_FINGERPRINTS_EN)


def find_exact_templates(records: list[dict], field: str, min_cluster: int) -> set[str]:
    """Exact-duplicate detection for fields that do NOT embed the disease name."""
    counts: Counter[str] = Counter()
    for r in records:
        v = (r.get(field) or "").strip()
        if len(v) >= 40:
            counts[v] += 1
    return {v for v, c in counts.items() if c >= min_cluster}


def find_template_norms(records: list[dict], field: str, min_cluster: int) -> set[str]:
    counts: Counter[str] = Counter()
    for r in records:
        v = (r.get(field) or "").strip()
        if len(v) < 25:
            continue
        counts[_norm(v, r.get("name_ja") or r.get("name") or "", r.get("species"))] += 1
    return {n for n, c in counts.items() if c >= min_cluster}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes to JSON")
    ap.add_argument("--preview", action="store_true", help="show sample regenerations")
    ap.add_argument("--min-cluster", type=int, default=5)
    args = ap.parse_args()

    records = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    tmpl_norms = find_template_norms(records, "prognosis_ja", args.min_cluster)
    tmpl_en = find_exact_templates(records, "prognosis", args.min_cluster)
    print(f"structural-template clusters (prognosis_ja, >= {args.min_cluster}): {len(tmpl_norms)}")
    print(f"exact-duplicate templates (prognosis EN, >= {args.min_cluster}): {len(tmpl_en)}")

    changed = changed_en = 0
    by_species: Counter[str] = Counter()
    samples: list[tuple] = []

    for r in records:
        species = r.get("species")
        name_ja = r.get("name_ja") or ""
        name_en = r.get("name") or ""
        sp_norm = SPECIES_NORM.get(species, species)
        category = None

        cur = (r.get("prognosis_ja") or "").strip()
        if cur and (_has_fingerprint(cur) or _norm(cur, name_ja, species) in tmpl_norms):
            category = resolve_true_category(name_ja, name_en, r.get("category") or "")
            new = gen_prognosis_ja(category, name_ja, sp_norm)
            if new and new != cur:
                if args.apply:
                    r["prognosis_ja"] = new
                changed += 1
                by_species[species] += 1
                if len(samples) < 30:
                    samples.append((species, name_ja, cur, new))

        cur_en = (r.get("prognosis") or "").strip()
        if cur_en and (_has_fingerprint_en(cur_en) or cur_en in tmpl_en):
            if category is None:
                category = resolve_true_category(name_ja, name_en, r.get("category") or "")
            new_en = gen_prognosis_en(category, name_en, sp_norm)
            if new_en and new_en != cur_en:
                if args.apply:
                    r["prognosis"] = new_en
                changed_en += 1

    print(f"regenerated prognosis_ja: {changed}")
    print(f"regenerated prognosis (EN): {changed_en}")
    print("by species:", dict(by_species.most_common()))

    if args.preview:
        seen: set[str] = set()
        shown = 0
        for sp, nm, old, new in samples:
            if sp in seen and shown >= 10:
                continue
            seen.add(sp)
            print(f"\n===== {sp} | {nm}")
            print("OLD:", old[:120])
            print("NEW:", new[:160])
            shown += 1
            if shown >= 18:
                break

    if args.apply:
        JSON_PATH.write_text(json.dumps(records, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        # Verify residual
        residual_fp = sum(1 for r in records if _has_fingerprint((r.get("prognosis_ja") or "")))
        residual_cluster = find_template_norms(records, "prognosis_ja", args.min_cluster)
        print(f"post-apply: fingerprint residue={residual_fp}, structural clusters={len(residual_cluster)}")
        if residual_cluster:
            c2: dict[str, list] = defaultdict(list)
            for r in records:
                v = (r.get("prognosis_ja") or "").strip()
                if len(v) < 25:
                    continue
                n = _norm(v, r.get("name_ja") or r.get("name") or "", r.get("species"))
                if n in residual_cluster:
                    c2[n].append((r.get("species"), r.get("name_ja")))
            for n, items in sorted(c2.items(), key=lambda kv: -len(kv[1]))[:8]:
                print(f"    [{len(items)}x] {n[:90]}")
                # show the distinct names to judge if it is a legitimate variant family
                names = sorted({nm for _, nm in items})[:6]
                print(f"        names: {names}")

    _ = re  # keep import used if future regex needed
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
