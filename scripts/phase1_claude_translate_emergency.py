#!/usr/bin/env python3
"""
Phase 1: Emergency 617件の treatment_en を Claude API で翻訳

仕様:
- batch size: 10件 (API効率 + 品質バランス)
- context: 医学用語辞書 + 種別特異的注意事項
- output: diseases_all_species.json 更新 + 翻訳ログ
"""

import json
import os
import sys
import time
from pathlib import Path
from anthropic import Anthropic

def load_data():
    """Load disease database"""
    db_path = Path(__file__).parent.parent / 'diseases_all_species.json'
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_emergency_to_translate(diseases):
    """Extract emergency cases without EN treatment"""
    to_translate = []
    for i, disease_data in enumerate(diseases):
        if disease_data.get('urgency') == 'emergency':
            treatment_en = disease_data.get('treatment_en')
            if not treatment_en or not treatment_en.strip():
                to_translate.append((i, disease_data))
    return to_translate

def build_translation_prompt(batch_cases):
    """Build prompt for batch translation"""
    cases_text = ""
    for idx, (db_idx, disease_data) in enumerate(batch_cases, 1):
        cases_text += f"""
【Case {idx}】
Species: {disease_data['species']}
Disease: {disease_data['name_ja']}  (EN: {disease_data.get('name_en', '')})
Urgency: emergency
Treatment (JA):
{disease_data['treatment_ja']}

---
"""

    return f"""You are a veterinary medical translator specializing in emergency treatment protocols.

Translate the following Japanese emergency treatment protocols into professional English medical language.

IMPORTANT INSTRUCTIONS:
1. Maintain medical accuracy and terminology (use standard veterinary nomenclature)
2. Preserve all specific dosages, routes, and durations exactly
3. Keep species-specific information and contraindications (e.g., "Penicillin contraindicated in guinea pigs")
4. Use passive voice where appropriate for medical context
5. Ensure emergency protocols are clear and actionable
6. Output ONLY the translations in JSON format, no explanation

Medical terminology reference:
- Route: IV (intravenous), IM (intramuscular), PO (oral), SC (subcutaneous), IP (intraperitoneal)
- Units: mg/kg, μg/kg, mg/kg/hr, mL/kg
- Common emergency drugs: epinephrine, atropine, fluids, medications

{cases_text}

Output format (JSON array):
[
  {{"case": 1, "treatment_en": "..."}},
  {{"case": 2, "treatment_en": "..."}},
  ...
]
"""

def translate_batch(client, batch_cases, batch_num, total_batches):
    """Translate a batch using Claude API"""
    prompt = build_translation_prompt(batch_cases)

    print(f"\n[Batch {batch_num}/{total_batches}] Translating {len(batch_cases)} cases...")

    try:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        response_text = message.content[0].text
        # Parse JSON response
        try:
            translations = json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                translations = json.loads(json_match.group())
            else:
                print(f"  ⚠ Failed to parse JSON from batch {batch_num}")
                return []

        print(f"  ✓ Batch {batch_num} completed ({len(translations)} translations)")
        return translations

    except Exception as e:
        print(f"  ✗ Error in batch {batch_num}: {e}")
        return []

def apply_translations(diseases, to_translate, translations_by_batch):
    """Apply translations back to database"""
    updated_count = 0
    failed_count = 0

    # Flatten batch translations
    all_translations = {}
    for batch_translations in translations_by_batch:
        for trans in batch_translations:
            case_num = trans.get('case')
            if case_num:
                all_translations[case_num] = trans.get('treatment_en', '')

    for case_num, (db_idx, disease_data) in enumerate(to_translate, 1):
        if case_num in all_translations:
            diseases[db_idx]['treatment_en'] = all_translations[case_num]
            updated_count += 1
        else:
            failed_count += 1

    return updated_count, failed_count

def main():
    # Load data
    print("🔄 Loading disease database...")
    diseases = load_data()
    to_translate = extract_emergency_to_translate(diseases)
    print(f"✓ Found {len(to_translate)} emergency cases without EN treatment")

    if not to_translate:
        print("✓ No cases to translate")
        return

    # Initialize Claude client
    client = Anthropic()

    # Process in batches
    batch_size = 10
    batches = [to_translate[i:i+batch_size] for i in range(0, len(to_translate), batch_size)]
    translations_by_batch = []

    print(f"\n📋 Processing {len(batches)} batches...")
    for batch_num, batch in enumerate(batches, 1):
        translations = translate_batch(client, batch, batch_num, len(batches))
        translations_by_batch.append(translations)
        time.sleep(1)  # Rate limiting

    # Apply translations
    print("\n🔄 Applying translations...")
    updated, failed = apply_translations(diseases, to_translate, translations_by_batch)
    print(f"  ✓ Updated: {updated} cases")
    print(f"  ✗ Failed: {failed} cases")

    # Save updated database
    db_path = Path(__file__).parent.parent / 'diseases_all_species.json'
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(diseases, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Database updated: {db_path}")

    # Log results
    log_path = Path(__file__).parent.parent / 'translation_phase1_log.json'
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump({
            'phase': 'Phase 1: Emergency',
            'total_cases': len(to_translate),
            'batch_size': batch_size,
            'batches_processed': len(batches),
            'updated': updated,
            'failed': failed,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }, f, ensure_ascii=False, indent=2)
    print(f"✓ Log saved: {log_path}")

if __name__ == '__main__':
    main()
