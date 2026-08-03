"""Keep ivermectin off chelonian (tortoise/turtle) treatment plans.

Ivermectin is lethal in chelonians — flaccid paralysis and death are reported at
doses routinely used in snakes and lizards — which is why every formulary lists
it as contraindicated in the group (Mader, *Reptile Medicine and Surgery*;
Carpenter, *Exotic Animal Formulary*).

This site's own drug dictionary already says so: ``ivermectin`` carries
``safe=False``, ``dosage="N/A"`` and the note 「【禁忌】カメ類には致死的な可能性」
for ``tortoise``. The disease pages nevertheless prescribed it, with a dose, on
tortoise records — the drug tab and the treatment text contradicted each other on
a drug that kills the animal. Several of those records inherited a shared
ectoparasite template whose caveat warns about "Collie系・チンチラ・ウサギ" while
sitting on a tortoise page, i.e. it names every species except the one being
viewed.

One record was worse than a bare omission: 「⚠カメでの安全性は確立——用量注意」 is a
truncation of 「安全性は確立されていない」, so it asserted the *opposite* of the
truth — that ivermectin is established as safe in chelonians.

The rewrite replaces the drug with the right alternative for the parasite the
record is actually about, taking doses from the drug dictionary so the treatment
text and the published drug entry cannot disagree:

* nematodes / ascarids / pinworms  → fenbendazole
* cestodes / trematodes            → praziquantel
* mites, ticks, other ectoparasites → no drug is substituted. The dictionary
  carries no chelonian dose for a topical acaricide, and inventing one would be
  exactly the failure this module exists to fix, so the text directs the reader
  to manual removal, environmental decontamination and a vet-selected topical.
"""

from __future__ import annotations

import re

# Only the chelonian species key: every record under it is a tortoise/turtle.
CHELONIAN_SPECIES = frozenset({"tortoise"})

_IVERMECTIN = r"(?:イベルメクチン|ivermectin)"
_DOSE = r"\d+(?:\.\d+)?(?:\s*[-〜~]\s*\d+(?:\.\d+)?)?\s*(?:mg/kg|mcg/kg|μg/kg)"

# The prescribing span: the drug through its dose and any trailing schedule or
# parenthetical, stopping at the next clause boundary.
_PRESCRIBING_SPAN = re.compile(_IVERMECTIN + r"[^、,;；。．\n]*?" + _DOSE + r"[^。．\n]*", re.I)
# A bare mention with no dose ("ダニ寄生がある場合はイベルメクチン") is still an
# instruction to use it, so it is caught too.
_BARE_MENTION = re.compile(_IVERMECTIN + r"(?![^。．\n]*?" + _DOSE + r")", re.I)

_HAS_IVERMECTIN = re.compile(_IVERMECTIN, re.I)

# Text that already tells the reader not to use it in chelonians.
_CHELONIAN_WARNING = re.compile(r"カメ[^。]{0,24}(?:禁忌|致死|毒性|不可|避け|使用しない)|chelonian", re.I)

# The truncated line that reverses the meaning — "safety IS established".
_REVERSED_SAFETY = re.compile(r"[（(]?\s*⚠?\s*カメでの安全性は確立\s*[—－-]{0,3}\s*用量注意\s*[）)]?")

# Parasite class of the record, decided from its name + treatment text.
# Acanthocephalans are deliberately NOT grouped with cestodes: praziquantel is
# not reliable against them, and those records already list fenbendazole and
# levamisole, so ivermectin is dropped rather than swapped for a drug that would
# not work either.
_CESTODE = re.compile(r"条虫|吸虫|cestode|trematode|tapeworm|fluke", re.I)
_ECTO = re.compile(r"ダニ|マダニ|外部寄生虫|蝿蛆|ハエ|mite|tick|ectoparasit|myiasis|ophionyssus|trombicul", re.I)
_NEMATODE = re.compile(r"線虫|回虫|蟯虫|鉤虫|nematode|ascarid|pinworm|oxyurid|hookworm|strongyl", re.I)

_SUB_NEMATODE_ID = "fenbendazole"
_SUB_NEMATODE_JA = "フェンベンダゾール"
_SUB_CESTODE_ID = "praziquantel"
_SUB_CESTODE_JA = "プラジクアンテル"

# Used only when the dictionary cannot be read; mirrors Carpenter/Mader.
_FALLBACK_DOSE = {
    _SUB_NEMATODE_ID: "50-100 mg/kg PO",
    _SUB_CESTODE_ID: "5-8 mg/kg PO",
}

# No chelonian acaricide dose exists in the dictionary, so no dose is invented.
_ECTO_ADVICE = "外部寄生虫は物理的除去とケージ・シェルターの消毒を基本とし、外用駆虫薬は獣医師の選択・監督下で用いる"

_WARNING_LINE = (
    "⚠イベルメクチンはカメ類（リクガメ・ミズガメ）には禁忌——ヘビ・トカゲで常用される用量でも"
    "弛緩性麻痺・死亡の報告があり、本サイトの薬品辞書でも当該種は safe=False・用量 N/A として登録されている。"
    "線虫にはフェンベンダゾール、条虫・吸虫にはプラジクアンテルを用い、"
    "外部寄生虫は物理的除去と環境消毒を優先する。"
    "（Mader, Reptile Medicine and Surgery; Carpenter, Exotic Animal Formulary）"
)


def _tidy(text: str) -> str:
    """Clean up the punctuation left behind when a drug clause is removed."""
    text = re.sub(r"[、,;；]\s*(?=[、,;；])", "", text)
    text = re.sub(r"[、,;；]\s*(?=[。．])", "", text)
    text = re.sub(r"(?<=[。．])\s*[、,;；]\s*", "", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    # A removed clause can leave an empty sentence ("…再投与。。").
    text = re.sub(r"([。．])\s*\1+", r"\1", text)
    return text


# The corpus spells praziquantel both ways, so a duplicate check must see both.
_SPELLING_VARIANTS = {
    "プラジクアンテル": ("プラジクアンテル", "プラジカンテル"),
    "フェンベンダゾール": ("フェンベンダゾール",),
}


def _already_names(drug: str, text: str) -> bool:
    """True when ``text`` already prescribes ``drug`` under any known spelling."""
    return any(v in text for v in _SPELLING_VARIANTS.get(drug, (drug,)))


def _formulary_dose(drug_id: str, species: str) -> str:
    """Per-species dose from the drug dictionary, with a published fallback."""
    try:
        from api.drug_dictionary import get_drug_by_id

        entry = get_drug_by_id(drug_id) or {}
        info = (entry.get("species_info") or {}).get(species) or {}
        dose = str(info.get("dosage") or info.get("dosage_ja") or "").strip()
        if dose and "mg/kg" in dose:
            return dose
    except Exception:  # pragma: no cover - dictionary import is best-effort
        pass
    return _FALLBACK_DOSE[drug_id]


def replacement_for(name: str, treatment_ja: str, species: str) -> str:
    """The alternative appropriate to the parasite this record is about.

    The DISEASE NAME decides the class. The treatment text cannot: several of
    these records carry a shared template that lists every parasite class at
    once ("Nematodes: … Cestodes / Trematodes: … Ectoparasites: …"), so matching
    against it made a tick infestation look like a cestode case.
    """
    for text in (name, treatment_ja):
        # Ectoparasite records must not be handed an anthelmintic.
        if _ECTO.search(text) and not _NEMATODE.search(text):
            return _ECTO_ADVICE
        if _CESTODE.search(text):
            return f"{_SUB_CESTODE_JA} {_formulary_dose(_SUB_CESTODE_ID, species)}"
        if _NEMATODE.search(text):
            return f"{_SUB_NEMATODE_JA} {_formulary_dose(_SUB_NEMATODE_ID, species)}"
    return f"{_SUB_NEMATODE_JA} {_formulary_dose(_SUB_NEMATODE_ID, species)}"


def make_chelonian_antiparasitics_safe(species: str, name: str, name_ja: str, treatment_ja: str) -> str | None:
    """Return a chelonian-safe rewrite of ``treatment_ja``, else ``None``.

    ``None`` means the record needed no change (no ivermectin, or the text is
    already a contraindication statement rather than a prescription).
    """
    if species not in CHELONIAN_SPECIES or not treatment_ja:
        return None
    # The ivermectin-toxicosis record itself is *about* the poisoning; its
    # treatment text legitimately names the drug.
    if re.search(r"中毒|toxicos|poison", f"{name} {name_ja}", re.I):
        return None
    if not _HAS_IVERMECTIN.search(treatment_ja) and not _REVERSED_SAFETY.search(treatment_ja):
        return None

    replacement = replacement_for(f"{name} {name_ja}", treatment_ja, species)
    changed = False
    out: list[str] = []

    for sentence in re.split(r"(?<=[。．])", treatment_ja):
        # Repair the truncation that claims safety IS established, whatever else
        # the sentence does.
        if _REVERSED_SAFETY.search(sentence):
            sentence = _REVERSED_SAFETY.sub("（⚠カメ類には禁忌——安全性は確立されていない）", sentence)
            changed = True

        if not _HAS_IVERMECTIN.search(sentence):
            out.append(sentence)
            continue

        # A dosed prescription is removed even when a warning sits beside it:
        # annotating a lethal drug does not make ordering it safe, and leaving
        # both makes the sentence contradict itself.
        if _PRESCRIBING_SPAN.search(sentence):
            # Do not introduce a duplicate of a drug the record already names —
            # check the WHOLE text, since the existing mention is usually in an
            # earlier sentence ("フェンベンダゾール … 。イベルメクチン …").
            drug = replacement.split(" ")[0]
            sub = "" if drug and _already_names(drug, treatment_ja) else replacement
            rewritten = _PRESCRIBING_SPAN.sub(sub, sentence)
            if not sub:
                rewritten = _tidy(rewritten)
        elif _CHELONIAN_WARNING.search(sentence):
            # Warning-only sentence with no dose — that is exactly what we want.
            out.append(sentence)
            continue
        else:
            rewritten = _BARE_MENTION.sub(replacement, sentence)

        if rewritten != sentence:
            changed = True
        out.append(rewritten)

    text = _tidy("".join(out))
    if not changed:
        return None
    if "カメ類には禁忌" not in text:
        text = text.rstrip()
        if text and not text.endswith(("。", "．")):
            text += "。"
        text += _WARNING_LINE
    return text
