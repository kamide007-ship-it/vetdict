"""Make oral antibiotic advice safe for hindgut-fermenting small mammals.

In rabbits, guinea pigs, chinchillas and degus, ORAL narrow-spectrum
beta-lactams (penicillins, amoxicillin ± clavulanate, ampicillin, oral
cephalosporins) and lincosamides/macrolides (clindamycin, lincomycin,
erythromycin) wipe out the Gram-positive caecal flora. *Clostridium spiroforme*
overgrows, produces iota toxin, and the animal dies of enterotoxaemia — this is
the classic, well-documented fatal drug reaction of the group
(Quesenberry & Carpenter, *Ferrets, Rabbits and Rodents*; Carpenter,
*Exotic Animal Formulary*).

The database nevertheless recommended exactly those drugs, by mouth and with a
dose, on 100+ hindgut-fermenter records. Most of the offending sentences came
from a shared empirical-therapy template that carries its own caveat —
"アモキシシリン・クラブラン酸 12.5-25 mg/kg PO q12h（小型哺乳類除く）" — i.e. the
sentence says "excluding small mammals" while sitting on the chinchilla page.
That is self-contradictory at best and lethal if the parenthesis is skimmed, so
the drug is removed from these species rather than merely annotated.

The transform is deliberately narrow:

* only the four hindgut-fermenting species are touched;
* only spans that *prescribe* (drug + oral route + mg/kg dose) are rewritten —
  a sentence that already warns against the drug is left exactly as it is;
* the unsafe drug is SUBSTITUTED with a safe equivalent rather than deleted
  (beta-lactams → trimethoprim-sulfa, lincosamides/macrolides → metronidazole,
  which is what the lincosamide was reaching for anaerobically). Deleting the
  clause outright left dangling conjunctive fragments such as
  "…は培養感受性試験を診療指針とし" and threw away the therapy the vet still
  needs, so substitution preserves both grammar and clinical usefulness;
* the substitute's DOSE is read per species from the drug dictionary — the
  vet-reviewed formulary this same site publishes on its drug tab — because the
  figures genuinely differ across the group: trimethoprim-sulfa is 30 mg/kg PO
  q12h in the rabbit and guinea pig but 15-30 mg/kg in the chinchilla and degu,
  and metronidazole is 20 mg/kg except in the chinchilla (10-20 mg/kg). A single
  hardcoded dose would have been wrong for half of them, and sourcing it from the
  dictionary means the treatment text and the drug tab cannot drift apart; and
* a single standard contraindication line is appended when the record does not
  already carry one.

Parenteral (SC/IM) penicillin G is *not* touched: it is used by exotic
clinicians for specific indications precisely because it bypasses the gut.
"""

from __future__ import annotations

import re

# Hindgut fermenters that die of antibiotic-associated enterotoxaemia.
HINDGUT_SPECIES = frozenset({"rabbit", "guinea_pig", "chinchilla", "degu"})

# Drugs that are lethal BY MOUTH in these species.
_DANGER_DRUG = (
    r"(?:アモキシシリン[・/]?クラブラン酸?|アモキシシリン/クラブラン酸|amoxicillin[\s/·・-]*clavulanate?"
    r"|アモキシシリン|amoxicillin|アンピシリン|ampicillin|クリンダマイシン|clindamycin"
    r"|リンコマイシン|lincomycin|セファレキシン|cephalexin|エリスロマイシン|erythromycin)"
)

# A prescribing clause: drug … dose … oral route (in any order within the clause).
_DOSE = r"\d+(?:\.\d+)?(?:\s*[-〜~]\s*\d+(?:\.\d+)?)?\s*mg/kg"
_ORAL = r"(?:\bPO\b|経口|内服)"

# A sentence that warns rather than prescribes must never be rewritten.
_WARNING = re.compile(r"(禁忌|致死|使用しない|投与しない|絶対に避け|避ける|contraindicat|fatal|avoid|never)", re.I)

_HAS_DANGER = re.compile(_DANGER_DRUG, re.I)
_HAS_DOSE = re.compile(_DOSE, re.I)
_HAS_ORAL = re.compile(_ORAL, re.I)

# The prescribing span to swap out: the drug name through its dose/route/caveat,
# stopping at the next clause boundary so neighbouring drugs are left intact.
_PRESCRIBING_SPAN = re.compile(
    _DANGER_DRUG + r"[^、,;；。．\n]*?" + _DOSE + r"[^、,;；。．\n]*",
    re.I,
)

# Safe oral substitutes in hindgut fermenters. Lincosamides/macrolides are
# replaced by metronidazole (the anaerobic cover they were reaching for);
# beta-lactams by trimethoprim-sulfa.
_LINCOSAMIDE = re.compile(
    r"(クリンダマイシン|clindamycin|リンコマイシン|lincomycin|エリスロマイシン|erythromycin)", re.I
)
# Ampicillin is contraindicated in these species whatever the route, so an
# "Ampicillin 20 mg/kg IV" line is no safer than an oral one.
_ANY_ROUTE_BANNED = re.compile(r"(アンピシリン|ampicillin)", re.I)

# The substitute's dose is read from the drug dictionary (api/drug_dictionary.py),
# which carries the vet-reviewed, per-species figures shown on the drug tab, so a
# rewritten treatment can never contradict the formulary the same site publishes.
# The doses genuinely differ by species — trimethoprim-sulfa is 30 mg/kg PO q12h
# in the rabbit and guinea pig but 15-30 mg/kg in the chinchilla and degu, and
# metronidazole is 20 mg/kg except in the chinchilla (10-20 mg/kg) — so a single
# hardcoded figure would have been wrong for half of them.
_SUB_BETA_LACTAM_ID = "trimethoprim_sulfa"
_SUB_BETA_LACTAM_JA = "トリメトプリム・スルファ"
_SUB_ANAEROBE_ID = "metronidazole"
_SUB_ANAEROBE_JA = "メトロニダゾール"

# Used only if the dictionary cannot be imported (it is the single source of
# truth; these mirror Carpenter, Exotic Animal Formulary for the widest species).
_FALLBACK_DOSE = {
    _SUB_BETA_LACTAM_ID: "15-30 mg/kg PO q12h",
    _SUB_ANAEROBE_ID: "10-20 mg/kg PO q12h",
}

_SPECIES_JA = {
    "rabbit": "ウサギ",
    "guinea_pig": "モルモット",
    "chinchilla": "チンチラ",
    "degu": "デグー",
}


def _formulary_dose(drug_id: str, species: str) -> str:
    """Return the curated oral dose for ``drug_id`` in ``species``.

    Falls back to the conservative published range when the dictionary is
    unavailable or the entry carries no dose for this species.
    """
    try:
        from api.drug_dictionary import get_drug_by_id

        entry = get_drug_by_id(drug_id) or {}
        info = (entry.get("species_info") or {}).get(species) or {}
        # Prefer the "30 mg/kg PO q12h" form over the localised
        # "30 mg/kg 経口 12時間毎": the surrounding prescribing text uses the
        # PO/q12h convention, so the substitute must read the same way.
        dose = str(info.get("dosage") or info.get("dosage_ja") or "").strip()
        if dose and "mg/kg" in dose:
            return dose
    except Exception:  # pragma: no cover - dictionary import is best-effort
        pass
    return _FALLBACK_DOSE[drug_id]


def substitute_for(species: str, anaerobic: bool) -> str:
    """The species-appropriate replacement drug + dose, straight from the formulary."""
    if anaerobic:
        return f"{_SUB_ANAEROBE_JA} {_formulary_dose(_SUB_ANAEROBE_ID, species)}"
    return f"{_SUB_BETA_LACTAM_JA} {_formulary_dose(_SUB_BETA_LACTAM_ID, species)}"


_WARNING_LINE = (
    "⚠{sp}では経口のペニシリン系・アモキシシリン（±クラブラン酸）・アンピシリン・経口セファロスポリン系・"
    "リンコマイシン系（クリンダマイシン等）・エリスロマイシンは禁忌——盲腸内のグラム陽性菌叢を破壊し "
    "Clostridium spiroforme の異常増殖とイオタ毒素による致死的腸性毒血症を招く。"
    "経口投与が必要な場合はエンロフロキサシン、トリメトプリム・スルファ、クロラムフェニコール、"
    "メトロニダゾール（嫌気性菌）、ドキシサイクリンから培養感受性に基づいて選択する。"
    "（Quesenberry & Carpenter, Ferrets, Rabbits and Rodents; Carpenter, Exotic Animal Formulary）"
)


def _rewrite_sentence(sentence: str, species: str) -> str | None:
    """Substitute unsafe prescribing spans; ``None`` when nothing changed."""
    if _WARNING.search(sentence):
        return None
    if not (_HAS_DANGER.search(sentence) and _HAS_DOSE.search(sentence)):
        return None
    if not (_HAS_ORAL.search(sentence) or _ANY_ROUTE_BANNED.search(sentence)):
        return None

    def _substitute(match: re.Match[str]) -> str:
        span = match.group(0)
        # Ampicillin is contraindicated in these species by ANY route —
        # parenteral dosing does not rescue it — so it is swapped even without
        # an oral marker. Penicillin G IM/SC is left alone: it bypasses the gut
        # and is used clinically.
        if not _HAS_ORAL.search(span) and not _ANY_ROUTE_BANNED.search(span):
            return span
        return substitute_for(species, anaerobic=bool(_LINCOSAMIDE.search(span)))

    rewritten = _PRESCRIBING_SPAN.sub(_substitute, sentence)
    if rewritten == sentence:
        return None
    # Collapse a duplicate that appears when two unsafe drugs sat side by side.
    for sub in (substitute_for(species, False), substitute_for(species, True)):
        dup = re.escape(sub) + r"(?:\s*[、,]\s*" + re.escape(sub) + r")+"
        rewritten = re.sub(dup, sub, rewritten)
    return rewritten


def make_oral_antibiotics_safe(species: str, treatment_ja: str) -> str | None:
    """Return a safe rewrite of ``treatment_ja``, or ``None`` if already safe.

    Only rabbits, guinea pigs, chinchillas and degus are considered.
    """
    if species not in HINDGUT_SPECIES or not treatment_ja:
        return None

    sentences = re.split(r"(?<=[。．])", treatment_ja)
    changed = False
    out: list[str] = []
    for s in sentences:
        rewritten = _rewrite_sentence(s, species)
        if rewritten is not None:
            out.append(rewritten)
            changed = True
        else:
            out.append(s)
    text = "".join(out)

    if not changed:
        return None

    # Guarantee the reader is told why, once per record.
    warning = _WARNING_LINE.format(sp=_SPECIES_JA.get(species, "本種"))
    if "Clostridium spiroforme" not in text:
        text = text.rstrip()
        if text and not text.endswith(("。", "．")):
            text += "。"
        text = f"{text}{warning}"
    return text
