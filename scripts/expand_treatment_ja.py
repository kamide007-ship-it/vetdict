#!/usr/bin/env python3
"""
Expand treatment_ja entries that are 80-149 characters long.

For entries where the `treatment` (EN) field is longer than `treatment_ja`,
replace treatment_ja with treatment. The EN field often contains Japanese text
or more detailed clinical content that should be used.

Rules:
- Only modify entries where treatment_ja is 80-149 characters
- Only replace if treatment (EN) is a string and longer than treatment_ja
- Do NOT touch entries with treatment_ja >= 150 or < 80 characters
"""

import json
import os
import re
import sys

JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "diseases_all_species.json")
JSON_PATH = os.path.abspath(JSON_PATH)

# Japanese text must contain at least one hiragana, katakana, or kanji character
_JP_RE = re.compile(r"[\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]")


def main():
    print(f"Reading {JSON_PATH} ...")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    total = len(data)
    print(f"Total disease entries: {total}")

    # --- BEFORE counts ---
    before_under_80 = 0
    before_80_149 = 0
    before_150_plus = 0
    for d in data:
        tja_len = len(d.get("treatment_ja", ""))
        if tja_len < 80:
            before_under_80 += 1
        elif tja_len < 150:
            before_80_149 += 1
        else:
            before_150_plus += 1

    print("\n=== BEFORE ===")
    print(f"  treatment_ja < 80c:    {before_under_80}")
    print(f"  treatment_ja 80-149c:  {before_80_149}")
    print(f"  treatment_ja >= 150c:  {before_150_plus}")

    # --- Find qualifying entries and update ---
    updated_count = 0
    skipped_same_or_shorter = 0
    skipped_no_treatment = 0

    for d in data:
        tja = d.get("treatment_ja", "")
        tja_len = len(tja)

        # Only target 80-149 character range
        if tja_len < 80 or tja_len >= 150:
            continue

        treatment_en = d.get("treatment", "")

        if not treatment_en or not isinstance(treatment_en, str):
            skipped_no_treatment += 1
            continue

        if len(treatment_en) <= tja_len:
            skipped_same_or_shorter += 1
            continue

        # Only use source text that contains Japanese characters (P2 fix)
        if not _JP_RE.search(treatment_en):
            skipped_same_or_shorter += 1
            continue

        # Replace treatment_ja with the longer treatment field
        d["treatment_ja"] = treatment_en
        updated_count += 1

    print("\n=== UPDATE SUMMARY ===")
    print(f"  Qualifying entries (80-149c):        {before_80_149}")
    print(f"  Updated (EN longer → replaced):      {updated_count}")
    print(f"  Skipped (EN same/shorter length):     {skipped_same_or_shorter}")
    print(f"  Skipped (EN missing/non-string):      {skipped_no_treatment}")

    # --- AFTER counts ---
    after_under_80 = 0
    after_80_149 = 0
    after_150_plus = 0
    for d in data:
        tja_len = len(d.get("treatment_ja", ""))
        if tja_len < 80:
            after_under_80 += 1
        elif tja_len < 150:
            after_80_149 += 1
        else:
            after_150_plus += 1

    print("\n=== AFTER ===")
    print(f"  treatment_ja < 80c:    {after_under_80}")
    print(f"  treatment_ja 80-149c:  {after_80_149}")
    print(f"  treatment_ja >= 150c:  {after_150_plus}")

    delta_150 = after_150_plus - before_150_plus
    print(f"\n  Net entries moved to >= 150c: +{delta_150}")
    print(f"  Remaining in 80-149c range:   {after_80_149}")

    # --- Write back ---
    print(f"\nWriting updated data to {JSON_PATH} ...")
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Done.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
