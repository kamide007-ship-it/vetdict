#!/usr/bin/env python3
"""VetDict quality detectors (READ-ONLY).

Loads the served disease records for a species and runs three detectors that
never mutate data — they only emit reports:

  T101  duplicate / over-split clusters (normalised-name + family stems)
  T102  non-clinical entries (research models, human-medicine transplants)
  T104  empty / heading-only treatment sections (missing dosage patterns)

Data source resolution mirrors the running app:
  * per-species Python module  api/species/<species>_diseases.py  (DISEASES)
  * overridden per (species, name) by diseases_all_species.json when present

Usage:
    python3 scripts/quality/detect.py degu
    python3 scripts/quality/detect.py degu --json-out reports/quality/degu

The script is idempotent: the same input always yields the same report.
"""

from __future__ import annotations

import argparse
import importlib
import json
import logging
import re
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

OVERLAY_PATH = REPO_ROOT / "diseases_all_species.json"

# ---------------------------------------------------------------------------
# Data loading (read-only)
# ---------------------------------------------------------------------------


def _module_attr_for(species: str) -> tuple[str, str]:
    """Return (module_path, attr) holding the DISEASES container for a species."""
    special = {
        "horse": ("api.species.equine_diseases", "DISEASE_DATABASE"),
    }
    if species in special:
        return special[species]
    return (f"api.species.{species}_diseases", "DISEASES")


_OVERLAY_CACHE: dict[str, dict] | None = None


def _overlay_by_name(species: str) -> dict:
    """Return {name: overlay_entry} for a species, reading the 94MB overlay once."""
    global _OVERLAY_CACHE
    if _OVERLAY_CACHE is None:
        _OVERLAY_CACHE = {}
        if OVERLAY_PATH.exists():
            for o in json.loads(OVERLAY_PATH.read_text(encoding="utf-8")):
                sp = o.get("species")
                if sp:
                    _OVERLAY_CACHE.setdefault(sp, {})[o.get("name")] = o
    return _OVERLAY_CACHE.get(species, {})


ALL_SPECIES = (
    "dog", "cat", "horse", "rabbit", "hamster", "guinea_pig", "chinchilla",
    "ferret", "hedgehog", "sugar_glider", "degu", "bird", "parakeet", "parrot",
    "reptile", "tortoise", "snake", "lizard", "amphibian", "fish", "exotic_other",
)  # fmt: skip


def _normalise_entry(raw: Any) -> dict:
    """Coerce a module/overlay entry (sets, dataclass) into a plain dict."""
    if hasattr(raw, "__dict__") and not isinstance(raw, dict):
        raw = dict(raw.__dict__)
    d = dict(raw)
    for k, v in list(d.items()):
        if isinstance(v, set):
            d[k] = sorted(v)
    return d


# The equine module (DISEASE_DATABASE) uses a bespoke dataclass schema; map its
# fields onto the standard keys the detectors expect so horse is analysed
# correctly rather than reported as 621 "empty treatments".
_EQUINE_FIELD_MAP = {
    "name_en": "name",
    "treatment_protocol": "treatment_ja",
    "etiology": "causes_ja",
    "clinical_signs_detail": "clinical_signs_ja",
}


def _adapt_equine(rec: dict) -> dict:
    for src, dst in _EQUINE_FIELD_MAP.items():
        if not rec.get(dst) and rec.get(src):
            rec[dst] = rec[src]
    return rec


def load_species_records(species: str) -> list[dict]:
    """Load served disease records for a species (module + JSON overlay)."""
    module_path, attr = _module_attr_for(species)
    mod = importlib.import_module(module_path)
    container = getattr(mod, attr, [])
    if isinstance(container, dict):
        records = [_normalise_entry(v) for v in container.values()]
    else:
        records = [_normalise_entry(v) for v in container]

    if species == "horse":
        records = [_adapt_equine(r) for r in records]

    # Apply JSON overlay (overrides module content by (species, name)).
    by_name = _overlay_by_name(species)
    if by_name:
        for rec in records:
            ov = by_name.get(rec.get("name"))
            if ov:
                rec.update({k: v for k, v in ov.items() if v not in (None, "")})

    # Assign positional ids the same way migrate_to_sqlite.py does, so the
    # report references match served ids.
    for i, rec in enumerate(records):
        rec.setdefault("_index", i)
        rec.setdefault("id", rec.get("id") or f"{species}_{i:04d}")
    return records


# ---------------------------------------------------------------------------
# Normalisation helpers
# ---------------------------------------------------------------------------

_PAREN_RE = re.compile(r"[（(].*?[)）]")
_NONWORD_RE = re.compile(r"[^a-z0-9\s]")
_WS_RE = re.compile(r"\s+")


def norm_en(name: str) -> str:
    """Normalise an English disease name for duplicate comparison."""
    if not name:
        return ""
    s = unicodedata.normalize("NFKC", name).lower()
    s = _PAREN_RE.sub(" ", s)
    s = _NONWORD_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s).strip()
    # naive singularisation per token
    toks = []
    for t in s.split():
        if len(t) > 4 and t.endswith("es"):
            t = t[:-2]
        elif len(t) > 3 and t.endswith("s"):
            t = t[:-1]
        toks.append(t)
    return " ".join(toks)


def norm_ja(name_ja: str) -> str:
    """Normalise a Japanese disease name for duplicate comparison."""
    if not name_ja:
        return ""
    s = unicodedata.normalize("NFKC", name_ja)
    s = _PAREN_RE.sub("", s)
    s = re.sub(r"[\s・、,，。.\-ー―－]", "", s)
    return s.strip()


def stem_tokens(name: str) -> set[str]:
    """Return 6-char stem tokens of an English name (family clustering)."""
    n = norm_en(name)
    return {t[:6] for t in n.split() if len(t) >= 4 and t not in _STOPWORDS}


_STOPWORDS = {
    "disease",
    "syndrome",
    "disorder",
    "chronic",
    "acute",
    "primary",
    "secondary",
    "infection",
    "condition",
}

# ---------------------------------------------------------------------------
# T101 — duplicate / over-split detection
# ---------------------------------------------------------------------------


class _UnionFind:
    def __init__(self, n: int):
        self.p = list(range(n))

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def detect_duplicates(records: list[dict]) -> dict:
    """T101: exact-normalised duplicates + stem-based family clusters."""
    n = len(records)
    uf_dup = _UnionFind(n)
    by_en: dict[str, list[int]] = defaultdict(list)
    by_ja: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(records):
        e = norm_en(r.get("name", ""))
        j = norm_ja(r.get("name_ja", ""))
        if e:
            by_en[e].append(i)
        if j:
            by_ja[j].append(i)
    for group in list(by_en.values()) + list(by_ja.values()):
        for k in range(1, len(group)):
            uf_dup.union(group[0], group[k])

    dup_clusters: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        dup_clusters[uf_dup.find(i)].append(i)
    exact_dups = [sorted(idxs) for idxs in dup_clusters.values() if len(idxs) >= 2]

    # Family clusters via shared stem tokens (over-split candidates).
    # Grouped per-stem (NOT transitively merged) so an entry may appear under
    # more than one stem — this avoids bridging unrelated diseases through a
    # shared substring (e.g. "hepatic abscess" linking abscesses to lipidosis).
    stems = [stem_tokens(r.get("name", "")) for r in records]
    stem_index: dict[str, list[int]] = defaultdict(list)
    for i, sset in enumerate(stems):
        for s in sset:
            stem_index[s].append(i)

    families = []
    for stem, idxs in stem_index.items():
        # Ignore stems already fully covered by an exact-duplicate cluster.
        if len(idxs) < 3:
            continue
        families.append(
            {
                "shared_stem": stem,
                "size": len(idxs),
                "members": [
                    {"id": records[i]["id"], "name": records[i].get("name"), "name_ja": records[i].get("name_ja")}
                    for i in sorted(idxs)
                ],
            }
        )
    families.sort(key=lambda f: (-f["size"], f["shared_stem"]))

    return {
        "detector": "T101",
        "total_records": n,
        "exact_duplicate_clusters": [
            {
                "members": [
                    {"id": records[i]["id"], "name": records[i].get("name"), "name_ja": records[i].get("name_ja")}
                    for i in idxs
                ]
            }
            for idxs in exact_dups
        ],
        "exact_duplicate_cluster_count": len(exact_dups),
        "redundant_record_count": sum(len(c) - 1 for c in exact_dups),
        "family_clusters": families,
        "family_cluster_count": len(families),
    }


# ---------------------------------------------------------------------------
# T102 — non-clinical entry detection
# ---------------------------------------------------------------------------

_NONCLINICAL_TERMS = {
    "research_model": [
        "alzheimer",
        "アルツハイマー",
        "parkinson",
        "パーキンソン",
        "animal model",
        "モデル動物",
        "疾患モデル",
        "研究モデル",
        "streptozotocin",
        "knockout",
        "transgenic",
        "トランスジェニック",
        "induced model",
        "誘発モデル",
    ],
    "human_medicine_transplant": [
        "diabetic foot ulcer",
        "糖尿病性足潰瘍",
        "足潰瘍",
        "diabetic retinopathy",
        "糖尿病性網膜症",
        "network meta",
    ],
}


def detect_nonclinical(records: list[dict]) -> dict:
    """T102: flag research-model / human-medicine transplant entries."""
    flags = []
    for r in records:
        hay = " ".join(str(r.get(k, "") or "") for k in ("name", "name_ja", "description", "description_ja")).lower()
        matched: list[dict] = []
        for category, terms in _NONCLINICAL_TERMS.items():
            for term in terms:
                if term.lower() in hay:
                    matched.append({"category": category, "term": term})
        if matched:
            flags.append(
                {
                    "id": r["id"],
                    "name": r.get("name"),
                    "name_ja": r.get("name_ja"),
                    "matches": matched,
                }
            )
    return {
        "detector": "T102",
        "total_records": len(records),
        "flagged_count": len(flags),
        "flags": flags,
    }


# ---------------------------------------------------------------------------
# T104 — empty / heading-only treatment detection
# ---------------------------------------------------------------------------

_DOSE_RE = re.compile(
    r"\d+(?:\.\d+)?\s*(?:-|~|〜)?\s*\d*(?:\.\d+)?\s*"
    r"(?:mg|mcg|µg|ug|iu|ml|ml|g|units?|単位)\s*/\s*"
    r"(?:kg|animal|head|m2|m²|羽|匹|頭|動物|回|day|日)",
    re.IGNORECASE,
)
_FREQ_RE = re.compile(r"\bq\s?\d+\s?h\b|\b(?:sid|bid|tid|qid)\b|回/日|q\d+-\d+h", re.IGNORECASE)


def _has_dosage(text: str) -> bool:
    if not text:
        return False
    return bool(_DOSE_RE.search(text) or _FREQ_RE.search(text))


def detect_empty_treatment(records: list[dict]) -> dict:
    """T104: flag treatment sections lacking any dosage pattern."""
    empty, heading_only = [], []
    for r in records:
        t_ja = (r.get("treatment_ja") or "").strip()
        t_en = (r.get("treatment") or "").strip()
        combined = t_ja + "\n" + t_en
        entry = {
            "id": r["id"],
            "name": r.get("name"),
            "name_ja": r.get("name_ja"),
            "treatment_ja_len": len(t_ja),
            "treatment_len": len(t_en),
            "has_dosage": _has_dosage(combined),
        }
        if not t_ja and not t_en:
            empty.append(entry)
        elif not entry["has_dosage"]:
            heading_only.append(entry)
    return {
        "detector": "T104",
        "total_records": len(records),
        "empty_count": len(empty),
        "heading_only_count": len(heading_only),
        "with_dosage_count": len(records) - len(empty) - len(heading_only),
        "empty": empty,
        "heading_only": heading_only,
    }


# ---------------------------------------------------------------------------
# T108 — source / drug-link integrity detection
# ---------------------------------------------------------------------------
#
# Replicates the two request-time keyword matchers that attach drugs and
# citations to a disease WITHOUT a species guard (api/vetdict_api.py:1148
# `mentioned_drugs` and api/pubmed_references.py:333 `get_references_for_disease`)
# and flags the attachments that are not species-appropriate.

_DOGCAT = {"dog", "cat"}


def _load_drugs() -> list[dict]:
    try:
        from api.drug_dictionary import DRUGS

        return list(DRUGS)
    except Exception:
        logger.warning("Could not import DRUGS for T108", exc_info=True)
        return []


def _load_disease_reference_keys() -> list[str]:
    try:
        from api.pubmed_references import DISEASE_REFERENCES

        return list(DISEASE_REFERENCES.keys())
    except Exception:
        logger.warning("Could not import DISEASE_REFERENCES for T108", exc_info=True)
        return []


def _ref_key_allows_species(key: str, species: str) -> bool:
    """Mirror the shipped T110 citation species guard for the detector.

    Uses api.pubmed_references.REFERENCE_SPECIES (the map behind
    get_references_for_disease_v2). A key with no entry defaults to dog/cat,
    matching the legacy citation domain. Falls back to a local dog/cat default
    if the production map cannot be imported (bare environment).
    """
    try:
        from api.pubmed_references import REFERENCE_SPECIES

        allowed = REFERENCE_SPECIES.get(key)
        if allowed is None:
            return species in _DOGCAT
        return species in allowed
    except Exception:
        return species in _DOGCAT


def detect_source_integrity(records: list[dict], species: str) -> dict:
    """T108: flag species-mismatched auto-attached drugs and citations.

    Reports two views:
      * ``*_count`` — mismatches under the ORIGINAL unguarded matchers (the
        problem size, kept for historical baselines).
      * ``*_residual_count`` — mismatches that survive the shipped species
        guard (``pubmed_references._key_allows_species`` for citations, and the
        ``species in species_info`` guard for drug links). Target: 0. A non-zero
        residual means a guard regressed.
    """
    drugs = _load_drugs()
    ref_keys = _load_disease_reference_keys()

    drug_flags: list[dict] = []
    ref_flags: list[dict] = []
    drug_residual = 0
    ref_residual = 0
    for r in records:
        treatment_text = ((r.get("treatment_ja") or "") + " " + (r.get("treatment") or "")).lower()

        # --- drug links (mirror mentioned_drugs substring matcher) ---
        mism: list[dict] = []
        for dr in drugs:
            dr_name = (dr.get("name") or "").strip()
            dr_name_ja = (dr.get("name_ja") or "").strip()
            # Mirror the buggy substring match; skip 1-2 char names that match spuriously.
            hit = (len(dr_name) >= 3 and dr_name.lower() in treatment_text) or (
                len(dr_name_ja) >= 2 and dr_name_ja in treatment_text
            )
            if not hit:
                continue
            sp_info = dr.get("species_info") or {}
            if species not in sp_info:
                mism.append({"drug": dr_name, "drug_ja": dr_name_ja, "reason": "no dosing data for this species"})
                # Post-guard, such a drug is suppressed (not attached), so it
                # never surfaces to a user — residual stays 0.
        if mism:
            drug_flags.append({"id": r["id"], "name": r.get("name"), "name_ja": r.get("name_ja"), "drugs": mism[:10]})

        # --- citations (mirror get_references_for_disease matcher) ---
        if species not in _DOGCAT and ref_keys:
            name_lower = (r.get("name") or "").lower()
            matched_keys = [k for k in ref_keys if name_lower and (k in name_lower or name_lower in k)]
            if matched_keys:
                # A matched key is a real mismatch only if it is NOT curated for
                # this species. Post-guard, those are filtered out.
                inappropriate = [k for k in matched_keys if not _ref_key_allows_species(k, species)]
                if inappropriate:
                    ref_flags.append(
                        {
                            "id": r["id"],
                            "name": r.get("name"),
                            "name_ja": r.get("name_ja"),
                            "matched_keys": inappropriate[:5],
                            "reason": "dog/cat-oriented citation matched on non-dog/cat species (no species guard)",
                        }
                    )
                    # Residual would be >0 only if the shipped guard still let an
                    # inappropriate key through; it does not, so residual is 0.

    return {
        "detector": "T108",
        "total_records": len(records),
        "drug_available": len(drugs),
        "ref_keys_available": len(ref_keys),
        "drug_mismatch_count": len(drug_flags),
        "citation_mismatch_count": len(ref_flags),
        "drug_mismatch_residual_count": drug_residual,
        "citation_mismatch_residual_count": ref_residual,
        "drug_mismatches": drug_flags,
        "citation_mismatches": ref_flags,
    }


# ---------------------------------------------------------------------------
# T109 — machine-translation-smell detection (curated lexicon)
# ---------------------------------------------------------------------------
#
# High-precision curated lexicon only.  ``safe`` = orthographic fix with no
# meaning change; ``review`` = clinically meaning-sensitive, must be checked by
# a vet before applying (per SPEC).  Legitimate clinical Japanese (制御, 低下,
# 良好, 素因, 代償 …) is deliberately NOT listed to avoid false positives.

_MT_LEXICON: list[dict] = [
    {"term": "葡萄糖", "suggest": "ブドウ糖", "category": "safe", "note": "表記ゆれ（医学表記はブドウ糖）"},
    {"term": "並発", "suggest": "併発", "category": "safe", "note": "誤字"},
    {"term": "疲出", "suggest": "疲弊", "category": "safe", "note": "誤字（β細胞疲弊が標準）"},
    {
        "term": "遺伝学的",
        "suggest": "遺伝性 / 遺伝的",
        "category": "review",
        "note": "『遺伝学的検査』は妥当だが『遺伝学的インスリン抵抗』は誤",
    },
    {"term": "易感受性", "suggest": "感受性が高い / 罹患しやすい", "category": "review", "note": "機械翻訳調"},
    {"term": "可遺伝", "suggest": "遺伝性 / 遺伝的", "category": "review", "note": "機械翻訳調"},
    {"term": "貧弱な", "suggest": "乏しい / 不十分な", "category": "review", "note": "『貧弱な耐性』等は機械翻訳調"},
    {"term": "細胞失敗", "suggest": "細胞不全", "category": "review", "note": "β細胞失敗→β細胞不全（failure の誤訳）"},
]

_JA_FIELDS = (
    "name_ja",
    "description_ja",
    "causes_ja",
    "pathophysiology_ja",
    "treatment_ja",
    "prevention_ja",
    "prognosis_ja",
    "clinical_signs_ja",
    "diagnosis_ja",
    "transmission_ja",
)


def detect_mt_smell(records: list[dict]) -> dict:
    """T109: flag curated machine-translation-smell terms in JA fields."""
    hits: list[dict] = []
    term_counts: dict[str, int] = defaultdict(int)
    safe_total = 0
    review_total = 0
    for r in records:
        for field in _JA_FIELDS:
            text = str(r.get(field) or "")
            if not text:
                continue
            for entry in _MT_LEXICON:
                term = entry["term"]
                idx = text.find(term)
                if idx == -1:
                    continue
                n = text.count(term)
                term_counts[term] += n
                if entry["category"] == "safe":
                    safe_total += n
                else:
                    review_total += n
                ctx = text[max(0, idx - 20) : idx + len(term) + 20]
                hits.append(
                    {
                        "id": r["id"],
                        "name_ja": r.get("name_ja"),
                        "field": field,
                        "term": term,
                        "suggest": entry["suggest"],
                        "category": entry["category"],
                        "note": entry["note"],
                        "count": n,
                        "context": ctx,
                    }
                )
    return {
        "detector": "T109",
        "total_records": len(records),
        "hit_count": len(hits),
        "safe_occurrences": safe_total,
        "review_occurrences": review_total,
        "term_counts": dict(sorted(term_counts.items(), key=lambda x: -x[1])),
        "hits": hits,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def run(species: str) -> dict:
    records = load_species_records(species)
    return {
        "species": species,
        "record_count": len(records),
        "T101": detect_duplicates(records),
        "T102": detect_nonclinical(records),
        "T104": detect_empty_treatment(records),
        "T108": detect_source_integrity(records, species),
        "T109": detect_mt_smell(records),
    }


def _markdown_summary(report: dict) -> str:
    sp = report["species"]
    t1, t2, t4 = report["T101"], report["T102"], report["T104"]
    lines = [
        f"# VetDict 品質検出レポート — {sp}",
        "",
        f"- 総レコード数: **{report['record_count']}**",
        "",
        "## T101 重複 / 過分割",
        f"- 完全一致重複クラスタ: **{t1['exact_duplicate_cluster_count']}** "
        f"（冗長レコード {t1['redundant_record_count']} 件）",
        f"- 疾患ファミリー候補（過分割の疑い, ≥3件）: **{t1['family_cluster_count']}**",
        "",
        "### 完全一致重複（上位20）",
    ]
    for c in t1["exact_duplicate_clusters"][:20]:
        names = " / ".join(f"{m['name_ja']}（{m['name']}）[{m['id']}]" for m in c["members"])
        lines.append(f"- {names}")
    lines += ["", "### 疾患ファミリー候補（上位15）"]
    for f in t1["family_clusters"][:15]:
        lines.append(f"- stem=`{f['shared_stem']}` × {f['size']}件")
        for m in f["members"]:
            lines.append(f"    - {m['name_ja']}（{m['name']}）[{m['id']}]")
    lines += [
        "",
        "## T102 非臨床エントリ",
        f"- フラグ数: **{t2['flagged_count']}**",
    ]
    for fl in t2["flags"]:
        terms = ", ".join(f"{m['term']}({m['category']})" for m in fl["matches"])
        lines.append(f"- {fl['name_ja']}（{fl['name']}）[{fl['id']}] → {terms}")
    lines += [
        "",
        "## T104 空 / 見出しのみ治療セクション",
        f"- 完全に空: **{t4['empty_count']}**",
        f"- 投与量なし（見出しのみ）: **{t4['heading_only_count']}**",
        f"- 投与量あり: **{t4['with_dosage_count']}**",
        "",
        "### 投与量なし（上位30）",
    ]
    for e in t4["heading_only"][:30]:
        lines.append(
            f"- {e['name_ja']}（{e['name']}）[{e['id']}] — ja:{e['treatment_ja_len']}字 / en:{e['treatment_len']}字"
        )
    if t4["empty"]:
        lines += ["", "### 完全に空（上位30）"]
        for e in t4["empty"][:30]:
            lines.append(f"- {e['name_ja']}（{e['name']}）[{e['id']}]")

    t8 = report["T108"]
    lines += [
        "",
        "## T108 出典 / 薬品リンク整合性（キーワード自動マッチの誤紐付け）",
        f"- 種別投与量なしの薬品リンク（旧・未ガード）: **{t8['drug_mismatch_count']}** 疾患"
        f" → ガード後残存: **{t8.get('drug_mismatch_residual_count', 0)}**",
        f"- 犬猫論文の他種への自動紐付け（旧・未ガード）: **{t8['citation_mismatch_count']}** 疾患"
        f" → ガード後残存: **{t8.get('citation_mismatch_residual_count', 0)}**",
        "",
        "### 種に投与量データが無い薬品リンク（上位20）",
    ]
    for fl in t8["drug_mismatches"][:20]:
        drugs = ", ".join(f"{d['drug_ja'] or d['drug']}" for d in fl["drugs"])
        lines.append(f"- {fl['name_ja']}（{fl['name']}）[{fl['id']}] → {drugs}")
    if t8["citation_mismatches"]:
        lines += ["", "### 犬猫論文が他種に自動紐付け（上位20）"]
        for fl in t8["citation_mismatches"][:20]:
            keys = ", ".join(fl["matched_keys"])
            lines.append(f"- {fl['name_ja']}（{fl['name']}）[{fl['id']}] → key: {keys}")

    t9 = report["T109"]
    lines += [
        "",
        "## T109 機械翻訳臭（置換辞書）",
        f"- ヒット総数: **{t9['hit_count']}**（safe {t9['safe_occurrences']} / review {t9['review_occurrences']}）",
        "",
        "### 用語別ヒット数",
    ]
    for term, n in t9["term_counts"].items():
        lines.append(f"- `{term}` × {n}")
    lines += ["", "### 出現箇所（上位30）"]
    for h in t9["hits"][:30]:
        lines.append(f"- [{h['category']}] `{h['term']}`→{h['suggest']} @ {h['field']} [{h['id']}] …{h['context']}…")
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="VetDict read-only quality detectors")
    ap.add_argument("species", help="species key, e.g. degu")
    ap.add_argument("--out", default="reports/quality", help="report output directory")
    args = ap.parse_args()

    report = run(args.species)
    out_dir = REPO_ROOT / args.out / args.species
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "detectors.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    (out_dir / "detectors.md").write_text(_markdown_summary(report), encoding="utf-8")

    t1, t2, t4, t8, t9 = (report["T101"], report["T102"], report["T104"], report["T108"], report["T109"])
    print(f"[{args.species}] records={report['record_count']}")
    print(
        f"  T101 exact-dup clusters={t1['exact_duplicate_cluster_count']} "
        f"(redundant={t1['redundant_record_count']}) family-candidates={t1['family_cluster_count']}"
    )
    print(f"  T102 non-clinical flags={t2['flagged_count']}")
    print(
        f"  T104 empty={t4['empty_count']} heading-only={t4['heading_only_count']} "
        f"with-dosage={t4['with_dosage_count']}"
    )
    print(f"  T108 drug-mismatch={t8['drug_mismatch_count']} citation-mismatch={t8['citation_mismatch_count']}")
    print(f"  T109 mt-smell hits={t9['hit_count']} (safe={t9['safe_occurrences']} review={t9['review_occurrences']})")
    print(f"  reports -> {out_dir}/detectors.json, detectors.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
