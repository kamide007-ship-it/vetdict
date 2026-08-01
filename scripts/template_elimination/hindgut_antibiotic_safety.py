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
  needs, so substitution preserves both grammar and clinical usefulness; and
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
_SUB_BETA_LACTAM = "トリメトプリム・スルファ 30 mg/kg PO q12h"
_SUB_ANAEROBE = "メトロニダゾール 20 mg/kg PO q12h"

_SPECIES_JA = {
    "rabbit": "ウサギ",
    "guinea_pig": "モルモット",
    "chinchilla": "チンチラ",
    "degu": "デグー",
}

_WARNING_LINE = (
    "⚠{sp}では経口のペニシリン系・アモキシシリン（±クラブラン酸）・アンピシリン・経口セファロスポリン系・"
    "リンコマイシン系（クリンダマイシン等）・エリスロマイシンは禁忌——盲腸内のグラム陽性菌叢を破壊し "
    "Clostridium spiroforme の異常増殖とイオタ毒素による致死的腸性毒血症を招く。"
    "経口投与が必要な場合はエンロフロキサシン、トリメトプリム・スルファ、クロラムフェニコール、"
    "メトロニダゾール（嫌気性菌）、ドキシサイクリンから培養感受性に基づいて選択する。"
    "（Quesenberry & Carpenter, Ferrets, Rabbits and Rodents; Carpenter, Exotic Animal Formulary）"
)


def _substitute(match: re.Match[str]) -> str:
    """Swap one prescribing span for its species-safe equivalent."""
    span = match.group(0)
    # Ampicillin is contraindicated in these species by ANY route — parenteral
    # dosing does not rescue it — so it is swapped even without an oral marker.
    if not _HAS_ORAL.search(span) and not _ANY_ROUTE_BANNED.search(span):
        # Parenteral-only span (e.g. penicillin G IM/SC) — clinically used, leave it.
        return span
    return _SUB_ANAEROBE if _LINCOSAMIDE.search(span) else _SUB_BETA_LACTAM


def _rewrite_sentence(sentence: str) -> str | None:
    """Substitute unsafe prescribing spans; ``None`` when nothing changed."""
    if _WARNING.search(sentence):
        return None
    if not (_HAS_DANGER.search(sentence) and _HAS_DOSE.search(sentence)):
        return None
    if not (_HAS_ORAL.search(sentence) or _ANY_ROUTE_BANNED.search(sentence)):
        return None
    rewritten = _PRESCRIBING_SPAN.sub(_substitute, sentence)
    if rewritten == sentence:
        return None
    # Collapse a duplicate that appears when two unsafe drugs sat side by side.
    for sub in (_SUB_BETA_LACTAM, _SUB_ANAEROBE):
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
        rewritten = _rewrite_sentence(s)
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
