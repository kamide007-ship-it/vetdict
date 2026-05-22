"""Shared constants for the diagnostic chat system."""

import re

_GENERIC_SPECIES = [
    "dog",
    "cat",
    "rabbit",
    "hamster",
    "chinchilla",
    "guinea_pig",
    "ferret",
    "hedgehog",
    "sugar_glider",
    "degu",
    "bird",
    "parakeet",
    "parrot",
    "reptile",
    "tortoise",
    "snake",
    "lizard",
    "amphibian",
    "fish",
    "exotic_other",
]

SPECIES_LABELS = {
    "dog": {"ja": "犬", "en": "Dog"},
    "cat": {"ja": "猫", "en": "Cat"},
    "horse": {"ja": "馬", "en": "Horse"},
    "rabbit": {"ja": "ウサギ", "en": "Rabbit"},
    "hamster": {"ja": "ハムスター", "en": "Hamster"},
    "chinchilla": {"ja": "チンチラ", "en": "Chinchilla"},
    "guinea_pig": {"ja": "モルモット", "en": "Guinea Pig"},
    "ferret": {"ja": "フェレット", "en": "Ferret"},
    "hedgehog": {"ja": "ハリネズミ", "en": "Hedgehog"},
    "sugar_glider": {"ja": "フクロモモンガ", "en": "Sugar Glider"},
    "degu": {"ja": "デグー", "en": "Degu"},
    "bird": {"ja": "鳥", "en": "Bird"},
    "parakeet": {"ja": "インコ", "en": "Parakeet"},
    "parrot": {"ja": "オウム", "en": "Parrot"},
    "reptile": {"ja": "爬虫類", "en": "Reptile"},
    "tortoise": {"ja": "リクガメ", "en": "Tortoise"},
    "snake": {"ja": "ヘビ", "en": "Snake"},
    "lizard": {"ja": "トカゲ", "en": "Lizard"},
    "amphibian": {"ja": "両生類", "en": "Amphibian"},
    "fish": {"ja": "魚", "en": "Fish"},
    "exotic_other": {"ja": "その他エキゾチック", "en": "Other Exotic"},
}

# --- Species detection from free-text chat input -------------------------------
# Veterinarians type the species inline ("猫 多飲多尿 体重減少", "5yo dog PU/PD"),
# so the chat must infer the species from the message rather than silently
# defaulting to dog. Multi-character/specific terms are listed before single
# kanji so that an earlier, more specific match wins on ties.
_SPECIES_KEYWORDS_EN = [
    ("puppy", "dog"), ("canine", "dog"), ("doggy", "dog"), ("dog", "dog"),
    ("kitten", "cat"), ("feline", "cat"), ("kitty", "cat"), ("cat", "cat"),
    ("foal", "horse"), ("equine", "horse"), ("pony", "horse"), ("mare", "horse"),
    ("stallion", "horse"), ("gelding", "horse"), ("thoroughbred", "horse"), ("horse", "horse"),
    ("bunny", "rabbit"), ("rabbit", "rabbit"),
    ("hamster", "hamster"),
    ("guinea pig", "guinea_pig"), ("guinea-pig", "guinea_pig"),
    ("chinchilla", "chinchilla"),
    ("ferret", "ferret"),
    ("hedgehog", "hedgehog"),
    ("sugar glider", "sugar_glider"), ("sugar-glider", "sugar_glider"),
    ("degu", "degu"),
    ("budgerigar", "parakeet"), ("budgie", "parakeet"), ("parakeet", "parakeet"),
    ("cockatiel", "parrot"), ("macaw", "parrot"), ("cockatoo", "parrot"), ("parrot", "parrot"),
    ("tortoise", "tortoise"), ("turtle", "tortoise"),
    ("gecko", "lizard"), ("iguana", "lizard"), ("lizard", "lizard"),
    ("reptile", "reptile"),
    ("salamander", "amphibian"), ("newt", "amphibian"), ("frog", "amphibian"), ("amphibian", "amphibian"),
    ("goldfish", "fish"), ("betta", "fish"), ("guppy", "fish"), ("koi", "fish"), ("fish", "fish"),
    ("snake", "snake"),
    ("bird", "bird"),
]

_SPECIES_KEYWORDS_JA = [
    ("フクロモモンガ", "sugar_glider"), ("モモンガ", "sugar_glider"),
    ("ハリネズミ", "hedgehog"), ("ハムスター", "hamster"),
    ("モルモット", "guinea_pig"), ("ギニアピッグ", "guinea_pig"),
    ("チンチラ", "chinchilla"), ("フェレット", "ferret"), ("デグー", "degu"),
    ("セキセイインコ", "parakeet"), ("インコ", "parakeet"), ("オウム", "parrot"),
    ("リクガメ", "tortoise"),
    ("両生類", "amphibian"), ("爬虫類", "reptile"),
    ("ヤモリ", "lizard"), ("イグアナ", "lizard"), ("トカゲ", "lizard"),
    ("イモリ", "amphibian"), ("カエル", "amphibian"),
    ("サラブレッド", "horse"), ("競走馬", "horse"), ("仔馬", "horse"), ("子馬", "horse"),
    ("熱帯魚", "fish"), ("金魚", "fish"), ("メダカ", "fish"), ("グッピー", "fish"), ("ベタ", "fish"),
    ("文鳥", "bird"), ("小鳥", "bird"),
    ("ラビット", "rabbit"), ("うさぎ", "rabbit"), ("ウサギ", "rabbit"),
    ("仔犬", "dog"), ("子犬", "dog"), ("わんちゃん", "dog"), ("ワンちゃん", "dog"),
    ("仔猫", "cat"), ("子猫", "cat"), ("にゃんこ", "cat"),
    ("ねこ", "cat"), ("ネコ", "cat"), ("いぬ", "dog"), ("イヌ", "dog"),
    ("うま", "horse"), ("ウマ", "horse"), ("ヘビ", "snake"), ("へび", "snake"),
    ("猫", "cat"), ("犬", "dog"), ("馬", "horse"), ("兎", "rabbit"),
    ("鳥", "bird"), ("亀", "tortoise"), ("蛇", "snake"), ("鯉", "fish"), ("魚", "fish"),
]

# Compounds where a species kanji is part of an unrelated word (false positives).
_JA_BLOCKED_COMPOUNDS = ("猫背", "犬歯", "海馬", "河馬", "馬鹿", "馬力", "鳥肌", "魚の目", "魚鱗癬")

_EN_KEYWORD_PATTERNS = [(re.compile(r"\b" + re.escape(kw) + r"\b"), sp) for kw, sp in _SPECIES_KEYWORDS_EN]


def detect_species_from_text(message):
    """Infer the patient species from free-text chat input.

    Returns a supported species id (e.g. "cat", "horse") or ``None`` when no
    species keyword is present. The earliest match in the message wins so that
    a leading species token ("猫 …", "dog …") takes precedence; kanji that are
    part of unrelated compounds (e.g. 犬歯 = canine tooth) are ignored.
    """
    if not message or not isinstance(message, str):
        return None
    lower = message.lower()

    blocked_ranges = []
    for compound in _JA_BLOCKED_COMPOUNDS:
        start = 0
        while True:
            j = message.find(compound, start)
            if j == -1:
                break
            blocked_ranges.append((j, j + len(compound)))
            start = j + 1

    def _is_blocked(pos, length):
        return any(a <= pos and pos + length <= b for a, b in blocked_ranges)

    best = None  # (position, -length, species)
    for pattern, sp in _EN_KEYWORD_PATTERNS:
        m = pattern.search(lower)
        if m:
            cand = (m.start(), -(m.end() - m.start()), sp)
            if best is None or cand < best:
                best = cand
    for kw, sp in _SPECIES_KEYWORDS_JA:
        start = 0
        while True:
            idx = message.find(kw, start)
            if idx == -1:
                break
            if not _is_blocked(idx, len(kw)):
                cand = (idx, -len(kw), sp)
                if best is None or cand < best:
                    best = cand
                break
            start = idx + 1

    return best[2] if best else None
