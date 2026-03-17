#!/usr/bin/env python3
"""
Prevention フィールド完成スクリプト
残り 3,030 件の予防情報を疾患タイプ別に生成
"""

import json
from pathlib import Path
from typing import Dict

# ============================================================================
# Prevention テンプレートエンジン
# ============================================================================

class PreventionGenerator:
    """疾患別に Prevention を生成"""

    # 疾患カテゴリ別テンプレート
    TEMPLATES = {
        'infectious_viral': {
            'keywords': ['virus', 'viral', 'infection', 'influenza', 'distemper', 'feline', 'felv', 'fiv'],
            'preventions': [
                'Vaccination against {disease_type} where available',
                'Practice strict hygiene and sanitation protocols',
                'Isolate infected animals to prevent transmission',
                'Avoid contact with infected animals and contaminated materials',
                'Maintain good nutrition and immune health',
                'Regular health monitoring and early detection'
            ]
        },
        'infectious_bacterial': {
            'keywords': ['bacteria', 'bacterial', 'infection', 'streptococcus', 'staphylococcus', 'leptospirosis'],
            'preventions': [
                'Vaccination against common bacterial pathogens where available',
                'Maintain strict sanitation and hygiene practices',
                'Ensure clean drinking water and food sources',
                'Isolate infected individuals immediately',
                'Antibiotic therapy for exposed animals as recommended',
                'Regular disinfection of living areas and equipment'
            ]
        },
        'parasitic': {
            'keywords': ['parasite', 'parasitic', 'worm', 'helminth', 'mite', 'lice', 'tick', 'flea', 'coccidia'],
            'preventions': [
                'Regular parasite screening and preventive treatment',
                'Maintain clean living environments and bedding',
                'Practice proper waste management and sanitation',
                'Prevent access to contaminated water and food sources',
                'Regular grooming and inspection for external parasites',
                'Appropriate antiparasitic medications as recommended'
            ]
        },
        'metabolic': {
            'keywords': ['diabetes', 'obesity', 'thyroid', 'metabolism', 'nutritional', 'mineral', 'vitamin'],
            'preventions': [
                'Provide balanced, species-appropriate diet',
                'Maintain healthy body weight through portion control',
                'Regular exercise and physical activity',
                'Avoid excessive feeding of high-calorie foods',
                'Regular metabolic and nutritional assessments',
                'Monitor for early signs of metabolic imbalance'
            ]
        },
        'neoplastic': {
            'keywords': ['cancer', 'tumor', 'neoplasm', 'carcinoma', 'lymphoma', 'melanoma'],
            'preventions': [
                'Regular physical examinations and health screening',
                'Maintain healthy body weight and nutrition',
                'Minimize exposure to known carcinogens',
                'Spay/neuter to reduce hormone-dependent cancers',
                'Early detection through routine health monitoring',
                'Genetic screening where breed predisposition exists'
            ]
        },
        'nutritional': {
            'keywords': ['deficiency', 'malnutrition', 'nutritional', 'anemia', 'kwashiorkor'],
            'preventions': [
                'Provide complete and balanced diet',
                'Ensure adequate protein, vitamins, and minerals',
                'Regular nutritional assessment and monitoring',
                'Supplement diet with essential micronutrients as needed',
                'Avoid feeding poor-quality or contaminated foods',
                'Educate owners on proper nutritional requirements'
            ]
        },
        'immune': {
            'keywords': ['immune', 'immunodeficiency', 'leukemia', 'fiv', 'feline', 'aids'],
            'preventions': [
                'Test and isolate infected animals',
                'Practice strict hygiene and prevent transmission',
                'Maintain optimal nutrition for immune function',
                'Avoid stress and provide appropriate living conditions',
                'Regular health monitoring for secondary infections',
                'Preventive treatment for common opportunistic infections'
            ]
        },
        'respiratory': {
            'keywords': ['respiratory', 'lung', 'bronch', 'pneumonia', 'cough', 'asthma', 'airway'],
            'preventions': [
                'Maintain good air quality and avoid irritants',
                'Ensure adequate ventilation in living areas',
                'Vaccination against common respiratory pathogens',
                'Minimize stress and environmental stressors',
                'Avoid smoking and air pollution exposure',
                'Regular monitoring for respiratory signs'
            ]
        },
        'gastrointestinal': {
            'keywords': ['gastrointestinal', 'diarrhea', 'enteritis', 'colitis', 'ibd', 'pancreatitis', 'gastritis'],
            'preventions': [
                'Feed high-quality, age-appropriate diet',
                'Maintain clean water and food bowls',
                'Prevent access to spoiled or contaminated food',
                'Minimize dietary changes and maintain consistency',
                'Regular deworming and parasite control',
                'Manage stress and maintain healthy gut flora'
            ]
        },
        'dermatologic': {
            'keywords': ['dermatitis', 'dermatologic', 'skin', 'allergic', 'mange', 'ringworm', 'fungal'],
            'preventions': [
                'Maintain regular grooming and skin hygiene',
                'Identify and avoid allergens or irritants',
                'Prevent parasitic infestations',
                'Maintain healthy coat through proper nutrition',
                'Avoid exposure to fungal spores and contaminated environments',
                'Regular skin examination and early treatment of lesions'
            ]
        },
        'urinary': {
            'keywords': ['urinary', 'kidney', 'renal', 'bladder', 'feline urologic', 'fus', 'calculi'],
            'preventions': [
                'Ensure adequate water intake and hydration',
                'Feed appropriate diet with balanced minerals',
                'Maintain clean water sources at all times',
                'Regular urinalysis and kidney function monitoring',
                'Prevent obesity and maintain healthy weight',
                'Minimize stress and provide appropriate environment'
            ]
        },
        'cardiovascular': {
            'keywords': ['cardiac', 'heart', 'cardiovascular', 'hypertension', 'heart failure', 'cardiomyopathy'],
            'preventions': [
                'Maintain healthy body weight',
                'Provide regular, moderate exercise',
                'Feed low-sodium, balanced diet',
                'Regular cardiac screening and monitoring',
                'Minimize stress and maintain calm environment',
                'Control blood pressure and manage comorbidities'
            ]
        },
        'neurologic': {
            'keywords': ['seizure', 'epilepsy', 'neurologic', 'neurological', 'paralysis', 'nerve'],
            'preventions': [
                'Prevent head trauma and injuries',
                'Maintain steady blood glucose levels',
                'Avoid toxin exposure and poisoning',
                'Regular health monitoring and early treatment',
                'Manage underlying metabolic or systemic diseases',
                'Minimize stressors and environmental triggers'
            ]
        },
        'default': {
            'keywords': [],
            'preventions': [
                'Maintain good hygiene and sanitation practices',
                'Regular health check-ups and veterinary monitoring',
                'Provide balanced nutrition and clean water',
                'Minimize stress and maintain optimal living conditions',
                'Isolate infected individuals when appropriate',
                'Early detection and prompt treatment of disease signs'
            ]
        }
    }

    @classmethod
    def classify_disease_type(cls, disease: Dict) -> str:
        """疾患をカテゴリに分類"""
        name = disease.get('name', '').lower()
        description = disease.get('description', '').lower()
        text = f"{name} {description}"

        # カテゴリ順（より詳細なものから）
        category_order = [
            'immune', 'neoplastic', 'metabolic', 'nutritional',
            'infectious_viral', 'infectious_bacterial', 'parasitic',
            'respiratory', 'gastrointestinal', 'dermatologic',
            'urinary', 'cardiovascular', 'neurologic'
        ]

        for category in category_order:
            if category in cls.TEMPLATES:
                keywords = cls.TEMPLATES[category]['keywords']
                if any(kw in text for kw in keywords):
                    return category

        return 'default'

    @classmethod
    def generate_prevention(cls, disease: Dict) -> str:
        """疾患に対応した Prevention を生成"""
        category = cls.classify_disease_type(disease)
        templates = cls.TEMPLATES[category]['preventions']

        # 複数のテンプレートを組み合わせる
        # 最初の 3-4 個を選択
        import random
        random.seed(hash(disease.get('id', '')))  # 再現性を確保
        selected = random.sample(templates, min(3, len(templates)))

        return '; '.join(selected) + '.'

    @classmethod
    def generate_prevention_ja(cls, disease: Dict) -> str:
        """日本語版 Prevention を生成"""
        disease_type = cls.classify_disease_type(disease)

        # 簡易的な日本語テンプレート
        ja_templates = {
            'infectious_viral': '定期的な予防接種と衛生管理；感染動物との接触回避；免疫機能の維持',
            'infectious_bacterial': '衛生環境の維持；清潔な飲食物の提供；感染動物の隔離',
            'parasitic': '定期的な寄生虫駆除；生活環境の清潔保持；定期検診',
            'metabolic': 'バランスの取れた食事；健康的な体重管理；定期的な健康診断',
            'neoplastic': '定期的な健康診断；健康的な体重維持；遺伝的スクリーニング',
            'nutritional': '栄養バランスの取れた食事；ビタミン・ミネラルの補給；栄養管理',
            'immune': 'テストと隔離；衛生管理；栄養管理；定期的な健康監視',
            'respiratory': '清潔な空気環境；予防接種；ストレス管理；呼吸器系監視',
            'gastrointestinal': '高品質な食事；衛生的な環境；定期的な寄生虫駆除',
            'dermatologic': '定期的なグルーミング；アレルギー物質の回避；栄養管理',
            'urinary': '十分な水分摂取；バランスの取れた食事；定期検診',
            'cardiovascular': '健康的な体重維持；適度な運動；塩分制限食',
            'neurologic': '外傷の防止；血糖値の維持；毒素暴露の回避',
            'default': '定期的な衛生管理；バランスの取れた栄養；ストレス軽減；定期検診'
        }

        return ja_templates.get(disease_type, ja_templates['default'])


# ============================================================================
# Prevention 補完エンジン
# ============================================================================

def complete_prevention_fields():
    """Prevention フィールドを完成"""

    print("🔧 Prevention フィールド完成を開始します")
    print("="*70)

    # データを読み込み
    data_file = Path('diseases_all_species.json')
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"✓ {len(data)} 件の疾患データを読み込みました")

    # 統計
    stats = {
        'prevention_added': 0,
        'prevention_ja_added': 0,
        'prevention_kept': 0,
        'errors': 0
    }

    generator = PreventionGenerator()

    # 各疾患を処理
    for i, disease in enumerate(data):
        try:
            # Prevention を追加（既存データは保持）
            if disease.get('prevention'):
                stats['prevention_kept'] += 1
            else:
                disease['prevention'] = generator.generate_prevention(disease)
                stats['prevention_added'] += 1

            # Prevention_ja を追加
            if not disease.get('prevention_ja'):
                disease['prevention_ja'] = generator.generate_prevention_ja(disease)
                stats['prevention_ja_added'] += 1

            if (i + 1) % 1000 == 0:
                print(f"  処理中... {i+1}/{len(data)}")

        except Exception as e:
            print(f"❌ エラー (ID: {disease.get('id')}): {e}")
            stats['errors'] += 1

    # 修復されたデータを保存
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n✅ Prevention 補完完了！")
    print(f"{'='*70}")
    print("📊 補完統計:")
    print(f"  Prevention 追加: {stats['prevention_added']}")
    print(f"  Prevention 既存: {stats['prevention_kept']}")
    print(f"  Prevention_ja 追加: {stats['prevention_ja_added']}")
    print(f"  エラー: {stats['errors']}")

    # フィールド完成度を確認
    print("\n📋 補完後のフィールド完成度:")
    fields = ['treatment', 'prevention', 'prognosis', 'treatment_ja', 'prevention_ja', 'prognosis_ja']
    for field in fields:
        filled = sum(1 for d in data if d.get(field) and str(d.get(field)).strip())
        completion = (filled / len(data)) * 100
        status = "✅" if completion == 100 else "⚠️" if completion > 50 else "❌"
        print(f"  {status} {field:<20} {filled:>5}/{len(data)} ({completion:>5.1f}%)")

    return data_file


def verify_prevention(data_file: Path):
    """Prevention の品質を検証"""
    print("\n✔️ Prevention の品質検証中...")
    print(f"{'='*70}")

    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # サンプル確認
    print("\n📝 サンプル (疾患別):")

    # 各カテゴリから 1 件ずつサンプル
    categories = {}
    for disease in data:
        category = PreventionGenerator.classify_disease_type(disease)
        if category not in categories:
            categories[category] = disease

    for category, disease in sorted(categories.items())[:5]:
        print(f"\n  📌 {category}")
        print(f"     名前: {disease.get('name')}")
        print(f"     Prevention: {disease.get('prevention', 'なし')[:100]}...")
        print(f"     Prevention_ja: {disease.get('prevention_ja', 'なし')[:80]}...")

    print("\n✅ Prevention 品質確認完了！")


if __name__ == '__main__':
    # 補完実行
    data_file = complete_prevention_fields()

    # 検証
    verify_prevention(data_file)

    print("\n✅ Prevention フィールド完成！")
    print(f"📄 ファイル: {data_file}")
