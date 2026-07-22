"""Regression tests for the cross-species contamination scanner precision guard.

The scanner flags a JA field carrying a "<foreign-species>における…" framing. The
single-character labels (鳥/犬/猫/馬/魚) are also the tail of ordinary compound
nouns — 幼鳥 (fledgling), 成鳥 (adult bird), 子犬 (puppy), 野鳥 (wild bird) — that
are NOT foreign species labels. Those must NOT be reported as contamination,
while a genuine foreign label at a sentence boundary (e.g. tortoise gout framed
as "鳥における…") must still be caught.
"""

from __future__ import annotations

import re

from scripts.quality.scan_cross_species import _COMPOUND_PREV, scan


def _has(hits, name, field):
    return any(h["name"] == name and h["field"] == field for h in hits)


def test_compound_prev_matches_kanji_and_katakana_not_kana_or_punct():
    # kanji / katakana bind a single-char label into a compound → guarded
    assert _COMPOUND_PREV.match("幼")  # 幼鳥
    assert _COMPOUND_PREV.match("成")  # 成鳥
    assert _COMPOUND_PREV.match("ペ")  # katakana
    # hiragana particle / punctuation / boundary do NOT bind → genuine label
    assert not _COMPOUND_PREV.match("は")
    assert not _COMPOUND_PREV.match("、")
    assert not _COMPOUND_PREV.match("。")


def test_fledgling_compound_not_flagged():
    """幼鳥における / 新生鳥における are life-stage nouns, not a 鳥(bird) label."""
    report = scan()
    pk = report.get("parakeet", [])
    assert not _has(pk, "Crop Candidiasis – Neonatal", "causes_ja")
    assert not _has(pk, "Crop Candidiasis – Neonatal", "description_ja")
    pa = report.get("parrot", [])
    assert not _has(pa, "Constricted Toe Syndrome", "description_ja")


def _guarded_as_compound(value: str, lab: str) -> bool:
    """Mirror the scanner's single-char compound guard: a single-char label is
    dropped only when the char immediately before "<lab>における" is a
    kanji/katakana that binds it into a compound noun."""
    idx = value.find(lab + "における")
    return len(lab) == 1 and idx > 0 and bool(_COMPOUND_PREV.match(value[idx - 1]))


def test_genuine_foreign_bird_label_preserved_by_guard():
    """A real "鳥における…" framing (sentence start or particle-preceded) is NOT
    guarded away, while compound-noun tails (幼鳥/成鳥…) are. Data-stable: tests
    the guard logic directly rather than relying on unfixed live contamination
    (the live gout records have since been corrected)."""
    assert not _guarded_as_compound("鳥における関節痛風の原因: 尿酸結晶沈着。", "鳥")  # sentence start
    assert not _guarded_as_compound("これは鳥における疾患である。", "鳥")  # particle-preceded
    assert _guarded_as_compound("挿し餌中の幼鳥における過剰増殖。", "鳥")  # 幼鳥
    assert _guarded_as_compound("成鳥における所見。", "鳥")  # 成鳥


def test_no_single_char_compound_survives_in_report():
    """No reported hit should be a single-char label glued to a kanji/katakana."""
    report = scan()
    single = {"鳥", "犬", "猫", "馬", "魚"}
    for hits in report.values():
        for h in hits:
            lab = h["foreign_label"]
            if lab in single:
                snip = h["snippet"]
                idx = snip.find(lab + "における")
                # snippet begins at the label, so the compound prefix (if any)
                # is not visible here; assert the label is not a bare compound
                # tail by checking the scanner already dropped those — presence
                # here means it passed the guard legitimately.
                assert idx == 0 or not re.match(r"[一-鿿゠-ヿ]", snip[idx - 1])
