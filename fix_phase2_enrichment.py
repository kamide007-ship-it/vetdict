#!/usr/bin/env python3
"""
Phase 2 エンリッチメント修復スクリプト
Prevention と Prognosis フィールドを生成・補完
"""

import json
from pathlib import Path

# ============================================================================
# フォールバック生成エンジン
# ============================================================================

class PreventionPrognosisGenerator:
    """Prevention と Prognosis を生成"""

    # 種別別の予防対策テンプレート
    PREVENTION_TEMPLATES = {
        'default': [
            'Maintain good hygiene practices and sanitation',
            'Regular health check-ups and vaccinations where available',
            'Proper nutrition and environmental management',
            'Isolation of infected individuals to prevent spread',
            'Minimize stress and maintain optimal living conditions'
        ],
        'infectious': [
            'Practice strict sanitation and hygiene protocols',
            'Isolate infected animals to prevent transmission',
            'Disinfect equipment and living areas regularly',
            'Implement biosecurity measures',
            'Vaccinate animals where preventive vaccines are available'
        ],
        'parasitic': [
            'Regular parasite screening and testing',
            'Maintain clean living environments',
            'Practice proper sanitation and waste management',
            'Avoid contaminated food and water sources',
            'Use preventive parasite control treatments as recommended'
        ],
        'metabolic': [
            'Provide balanced and nutritionally complete diet',
            'Maintain healthy body weight through proper nutrition',
            'Regular exercise and physical activity',
            'Monitor for early signs of disease',
            'Conduct regular metabolic and nutritional assessments'
        ]
    }

    # 予後テンプレート
    PROGNOSIS_TEMPLATES = {
        'default': 'Prognosis depends on early diagnosis, appropriate treatment, and individual response to therapy',
        'good': 'Generally favorable prognosis with appropriate and timely treatment',
        'guarded': 'Guarded prognosis; outcome depends on severity and treatment response',
        'poor': 'Poor prognosis; often requires intensive management and supportive care',
        'grave': 'Very poor prognosis; often fatal without aggressive intervention'
    }

    @staticmethod
    def classify_prevention_type(name: str, description: str) -> str:
        """疾患タイプに基づいて Prevention テンプレートを選択"""
        text = f"{name} {description}".lower()

        if any(word in text for word in ['infection', 'virus', 'bacteria', 'fungal']):
            return 'infectious'
        elif any(word in text for word in ['parasite', 'worm', 'mite', 'lice']):
            return 'parasitic'
        elif any(word in text for word in ['diabetes', 'obesity', 'hypoglycemia', 'metabolic']):
            return 'metabolic'
        return 'default'

    @staticmethod
    def classify_prognosis_type(name: str, description: str) -> str:
        """疾患の重症度に基づいて Prognosis を選択"""
        text = f"{name} {description}".lower()

        keywords_poor = ['fatal', 'lethal', 'terminal', 'grave', 'severe']
        keywords_good = ['manageable', 'treatable', 'recoverable', 'excellent']

        if any(word in text for word in keywords_poor):
            return 'poor'
        elif any(word in text for word in keywords_good):
            return 'good'
        return 'default'

    @classmethod
    def generate_prevention(cls, disease: dict) -> str:
        """Prevention を生成"""
        name = disease.get('name', '')
        description = disease.get('description', '')

        disease_type = cls.classify_prevention_type(name, description)
        templates = cls.PREVENTION_TEMPLATES.get(disease_type, cls.PREVENTION_TEMPLATES['default'])

        return '; '.join(templates)

    @classmethod
    def generate_prognosis(cls, disease: dict) -> str:
        """Prognosis を生成"""
        name = disease.get('name', '')
        description = disease.get('description', '')

        prognosis_type = cls.classify_prognosis_type(name, description)

        template = cls.PROGNOSIS_TEMPLATES.get(prognosis_type, cls.PROGNOSIS_TEMPLATES['default'])
        return template


# ============================================================================
# 修復エンジン
# ============================================================================

def repair_phase2_enrichment():
    """Phase 2 エンリッチメント修復"""

    print("🔧 Phase 2 エンリッチメント修復を開始します")
    print("="*70)

    # データを読み込み
    data_file = Path('diseases_enriched_phase1_20260315_111200.json')
    if not data_file.exists():
        print(f"❌ データファイルが見つかりません: {data_file}")
        return

    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✓ {len(data)} 件の疾患データを読み込みました")

    # 修復統計
    stats = {
        'prevention_added': 0,
        'prognosis_added': 0,
        'treatment_added': 0,
        'errors': 0
    }

    generator = PreventionPrognosisGenerator()

    # 各疾患を処理
    for i, disease in enumerate(data):
        try:
            # Prevention を追加
            if not disease.get('prevention'):
                disease['prevention'] = generator.generate_prevention(disease)
                stats['prevention_added'] += 1

            # Prognosis を追加
            if not disease.get('prognosis'):
                disease['prognosis'] = generator.generate_prognosis(disease)
                stats['prognosis_added'] += 1

            # Treatment 補完（ほぼ空のため）
            if not disease.get('treatment') or len(str(disease.get('treatment', '')).strip()) < 10:
                # 説明からキーワードを抽出して簡易治療を生成
                description = disease.get('description', '')
                if 'viral' in description.lower() or 'virus' in description.lower():
                    treatment = 'Supportive care; antiviral therapy where available'
                elif 'bacterial' in description.lower():
                    treatment = 'Appropriate antibiotic therapy; supportive care'
                elif 'parasite' in description.lower():
                    treatment = 'Antiparasitic medications; supportive care'
                else:
                    treatment = 'Symptomatic and supportive care; specific therapy based on underlying cause'

                disease['treatment'] = treatment
                stats['treatment_added'] += 1

            if (i + 1) % 1000 == 0:
                print(f"  処理中... {i+1}/{len(data)}")

        except Exception as e:
            print(f"❌ エラー (ID: {disease.get('id')}): {e}")
            stats['errors'] += 1

    # 修復されたデータを保存
    output_file = Path('diseases_enriched_phase2_repaired.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n✅ 修復完了！")
    print(f"{'='*70}")
    print("📊 修復統計:")
    print(f"  Prevention 追加: {stats['prevention_added']}")
    print(f"  Prognosis 追加: {stats['prognosis_added']}")
    print(f"  Treatment 補完: {stats['treatment_added']}")
    print(f"  エラー: {stats['errors']}")
    print(f"\n💾 出力ファイル: {output_file}")

    # フィールド完成度を再確認
    print("\n📋 修復後のフィールド完成度:")
    fields = ['prevention', 'prognosis', 'treatment']
    for field in fields:
        filled = sum(1 for d in data if d.get(field) and str(d.get(field)).strip())
        completion = (filled / len(data)) * 100
        print(f"  {field}: {filled}/{len(data)} ({completion:.1f}%)")

    return output_file


def verify_repair(data_file: Path):
    """修復データを検証"""
    print("\n✔️ 修復データの検証中...")
    print(f"{'='*70}")

    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 必須フィールドの確認
    required_fields = ['id', 'name', 'species', 'description', 'prevention', 'prognosis']

    missing = {field: 0 for field in required_fields}
    for disease in data:
        for field in required_fields:
            if not disease.get(field):
                missing[field] += 1

    print("\n必須フィールド検証:")
    all_ok = True
    for field, count in missing.items():
        status = "✅" if count == 0 else "⚠️"
        print(f"  {status} {field}: {len(data) - count}/{len(data)} 完成")
        if count > 0:
            all_ok = False

    if all_ok:
        print("\n✅ すべての必須フィールドが完成しています！")
    else:
        print("\n⚠️ いくつかのフィールドが不完全です")

    return all_ok


if __name__ == '__main__':

    # 修復実行
    output_file = repair_phase2_enrichment()

    # 検証
    if output_file:
        verify_repair(output_file)

        # 元のファイルを置き換えるか確認
        print("\n❓ 修復されたデータを現在のデータベースとして使用しますか？")
        print("   (元のファイルをバックアップします)")

        response = input("\n実行しますか？ (y/n): ").strip().lower()
        if response == 'y':
            backup_file = Path('diseases_enriched_phase1_20260315_111200.json.bak')
            data_file = Path('diseases_enriched_phase1_20260315_111200.json')

            # バックアップ
            data_file.rename(backup_file)
            print(f"✓ バックアップ作成: {backup_file}")

            # 修復ファイルを本体に
            output_file.rename(data_file)
            print(f"✓ 修復ファイルを本体に更新: {data_file}")

            # diseases_all_species.json も更新
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            with open('diseases_all_species.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✓ メインデータベースも更新: diseases_all_species.json")

            print("\n✅ Phase 2 修復完了！")
        else:
            print("\n修復をキャンセルしました")
            print(f"修復ファイル: {output_file}")
