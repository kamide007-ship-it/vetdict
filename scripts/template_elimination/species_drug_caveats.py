"""Apply species drug caveats the corpus states in some records but not others.

Both facts below are already written into this database — just inconsistently, so
whether a vet is warned depends on which page they happen to open. That is worse
than a uniform omission: the reader has no way to know the caveat exists.

**Atropine in rabbits (and other hystricomorphs).** Roughly 30-40% of rabbits
carry serum atropinesterase, which hydrolyses atropine so fast that a normal dose
may do nothing. Glycopyrrolate is not a substrate and is preferred; for mydriasis
tropicamide is used instead. Five records say so (「約30%にアトロピナーゼ」,
「アトロピンではなくトロピカミドを使用」); ten others prescribe atropine with no hint
— including the bradycardia/AV-block lines, where a drug silently failing is an
emergency, not an inconvenience.

**Itraconazole in African grey parrots.** Greys (Psittacus erithacus) are
distinctly sensitive: anorexia, depression and hepatotoxicity occur at doses other
psittacines tolerate, so voriconazole or terbinafine is preferred in that species.
Nine avian records carry the caveat and sixty-eight do not, even though
itraconazole is correctly first-line for aspergillosis in birds generally — this
adds the species nuance rather than removing the drug.

Neither caveat withdraws a drug: both are appended as a note, and records that
already carry the point are left untouched.
"""

from __future__ import annotations

import re

# Hystricomorphs/lagomorphs where atropinesterase matters. Guinea pigs are
# included because the corpus already applies the caveat to one of their records.
_ATROPINE_SPECIES = frozenset({"rabbit", "guinea_pig", "chinchilla", "degu"})
_AVIAN_SPECIES = frozenset({"bird", "parakeet", "parrot"})

_ATROPINE = re.compile(r"アトロピン|atropine", re.I)
_ITRACONAZOLE = re.compile(r"イトラコナゾール|itraconazole", re.I)

# The record already makes the point — in any of the phrasings the corpus uses.
_HAS_ATROPINE_CAVEAT = re.compile(r"アトロピナーゼ|グリコピロレート|トロピカミド|atropinesterase|glycopyrrolate", re.I)
_HAS_GREY_CAVEAT = re.compile(r"ヨウム|african\s*gr[ae]y|アフリカ", re.I)

_ATROPINE_NOTE = (
    "※{sp}の約30-40%は血清アトロピナーゼ（アトロピンエステラーゼ）を保有し、"
    "アトロピンが急速に加水分解されて無効となることがある。"
    "徐脈への抗コリン薬が必要な場合は基質とならないグリコピロレート 0.01-0.02 mg/kg SC/IM/IV を優先し、"
    "散瞳目的ではトロピカミド点眼を用いる。"
    "（Quesenberry & Carpenter, Ferrets, Rabbits and Rodents; Carpenter, Exotic Animal Formulary）"
)

_GREY_NOTE = (
    "※ヨウム（African grey, Psittacus erithacus）はイトラコナゾールに特に感受性が高く、"
    "他のオウム目が忍容する用量でも食欲不振・元気消失・肝毒性を生じうる。"
    "本種ではボリコナゾールまたはテルビナフィンを優先し、"
    "やむを得ず使用する場合は減量と肝酵素モニタリングを行う。"
    "（Mader/Carpenter 系エキゾチック処方集、Orosz, Avian Antifungal Therapeutics）"
)

_SPECIES_JA = {
    "rabbit": "ウサギ",
    "guinea_pig": "モルモット",
    "chinchilla": "チンチラ",
    "degu": "デグー",
}


def _append(text: str, note: str) -> str:
    text = text.rstrip()
    if text and not re.search(r"[。．]$", text):
        text += "。"
    return f"{text}{note}"


def species_drug_caveat(species: str, name: str, name_ja: str, treatment_ja: str) -> str | None:
    """Return ``treatment_ja`` with the missing caveat appended, else ``None``.

    ``None`` means the record does not name the drug, or already makes the point.
    """
    if not treatment_ja:
        return None
    # A record about the poisoning itself does not need a prescribing caveat.
    if re.search(r"中毒|toxicos|poison", f"{name} {name_ja}", re.I):
        return None

    if (
        species in _ATROPINE_SPECIES
        and _ATROPINE.search(treatment_ja)
        and not _HAS_ATROPINE_CAVEAT.search(treatment_ja)
    ):
        return _append(treatment_ja, _ATROPINE_NOTE.format(sp=_SPECIES_JA.get(species, "本種")))

    if species in _AVIAN_SPECIES and _ITRACONAZOLE.search(treatment_ja) and not _HAS_GREY_CAVEAT.search(treatment_ja):
        return _append(treatment_ja, _GREY_NOTE)

    return None
