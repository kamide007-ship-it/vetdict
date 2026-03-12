# 疾患コンテンツ充実化ガイド

VetDictの疾患データを充実させ、ユーザーエクスペリエンスを向上させるための実装ガイドです。

## 現状分析

- **総疾患数**: 576個
- **完全なデータ**: 33個（5.7%）
- **不足している情報フィールド**:
  - 病態生理 (pathophysiology)
  - 原因 (causes)
  - 治療 (treatment)
  - 予防 (prevention)
  - 予後 (prognosis)

## 戦略

### Phase 1: インベントリ作成（本ガイド）
1. 不完全な疾患を特定
2. Claude APIで医学的に正確な情報を生成
3. 品質チェックと検証
4. 段階的にデータベースに統合

### Phase 2: 継続的メンテナンス
1. 新規疾患追加時に自動充実化
2. ユーザーフィードバックに基づく改善
3. 医学文献との同期

## インプリメンテーション

### 1. リアルタイム充実化（単一疾患）

```python
from api.disease_content_enricher import DiseaseEnricher

enricher = DiseaseEnricher()

# 単一疾患の充実化
disease = {"name": "Hip Dysplasia", "name_ja": "股関節形成不全", ...}
enriched = enricher.enrich_single_disease(disease)

print(enriched['pathophysiology'])
print(enriched['causes'])
print(enriched['treatment'])
```

**使用場面**:
- 管理画面での手動編集
- API経由での個別リクエスト
- テストおよび品質検証

**コスト**: 1疾患あたり約$0.05

### 2. バッチ充実化（複数疾患・推奨）

```python
from api.disease_batch_enricher import DiseaseBatchEnricher
from api.symptom_checker import _DISEASE_DB

enricher = DiseaseBatchEnricher()

# 全疾患をバッチで充実化
result = enricher.enrich_diseases_batch(_DISEASE_DB, wait=True)

print(f"Status: {result['status']}")
print(f"Batch IDs: {result['batch_ids']}")
print(f"Results: {result['results']}")
```

**利点**:
- **50% コスト削減**: バッチAPI使用
- **効率的**: 最大100,000リクエスト/バッチ
- **スケーラブル**: 複数バッチを並列処理可能

**コスト**: 543疾患の充実化 ≈ $12-15（標準APIなら$24-30）

### 3. ステータス確認

```python
from api.disease_content_enricher import DiseaseEnricher
from api.symptom_checker import _DISEASE_DB

enricher = DiseaseEnricher()
status = enricher.get_enrichment_status(_DISEASE_DB)

print(f"完全: {status['complete']} ({status['complete_percentage']}%)")
print(f"フィールド別カバレッジ:")
for field, coverage in status['field_coverage'].items():
    print(f"  {field}: {coverage}%")
```

## セットアップ

### 環境変数

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### 依存関係

```bash
pip install anthropic>=0.7.0
```

## 実行計画

### Week 1: パイロット（100疾患）
```python
# test_enrichment.py
from api.disease_batch_enricher import DiseaseBatchEnricher
from api.symptom_checker import _DISEASE_DB

# 最初の100疾患でテスト
enricher = DiseaseBatchEnricher()
sample_diseases = _DISEASE_DB[:100]
result = enricher.enrich_diseases_batch(sample_diseases, wait=True)

# 品質チェック
for disease in sample_diseases:
    if disease.get('pathophysiology'):
        print(f"✓ {disease['name']}: pathophysiology OK")
```

**期間**: 1-2時間（バッチ処理時間）
**コスト**: 約$2-3

### Week 2: 完全実行（全543疾患）
```python
# full_enrichment.py
from api.disease_batch_enricher import DiseaseBatchEnricher
from api.symptom_checker import _DISEASE_DB

enricher = DiseaseBatchEnricher()
result = enricher.enrich_diseases_batch(_DISEASE_DB, wait=True)

# 結果を保存
import json
with open('enriched_diseases.json', 'w', encoding='utf-8') as f:
    json.dump(_DISEASE_DB, f, ensure_ascii=False, indent=2)
```

**期間**: 2-6時間（バッチ処理時間）
**コスト**: 約$12-15

### Week 3: 統合と検証
1. データの品質チェック
2. 医学的妥当性の確認
3. フロントエンドで表示テスト
4. ユーザーフィードバック収集

## 品質基準

各フィールドは以下を満たす必要があります:

- **病態生理**: 疾患メカニズムを説明（2-3文）
- **原因**: 主要および二次原因を列挙（2-3文）
- **治療**: 治療アプローチを説明（2-3文）
- **予防**: 予防戦略を説明（2-3文）
- **予後**: 予想される結果を説明（2-3文）

### 検証チェックリスト

```python
def validate_enriched_disease(disease):
    """疾患充実化の品質チェック"""
    issues = []

    # フィールド存在チェック
    fields = ['pathophysiology', 'causes', 'treatment', 'prevention', 'prognosis']
    for field in fields:
        if not disease.get(field) or len(disease[field]) < 50:
            issues.append(f"{field}: too short")
        if not disease.get(f"{field}_ja") or len(disease[f"{field}_ja"]) < 50:
            issues.append(f"{field}_ja: missing or too short")

    # 翻訳品質チェック
    for field in fields:
        en = disease.get(field, '')
        ja = disease.get(f"{field}_ja", '')
        # 同じ長さの概算で翻訳がなされているか確認
        if len(en) > 0 and len(ja) == 0:
            issues.append(f"{field}_ja: not translated")

    return issues
```

## フロントエンド統合

既存のUIは既に完全に実装されています：

### disease_detail.html表示例
```
疾患名: Hip Dysplasia / 股関節形成不全
説明: ...

病態生理: [充実化されたコンテンツ表示]
原因: [充実化されたコンテンツ表示]
予防: [充実化されたコンテンツ表示]
治療: [充実化されたコンテンツ表示]
予後: [充実化されたコンテンツ表示]
```

## トラブルシューティング

### APIエラー: 401 Unauthorized
```
解決策: ANTHROPIC_API_KEYが正しく設定されているか確認
export ANTHROPIC_API_KEY="your-actual-api-key"
```

### JSONパースエラー
```
原因: ClaudeがJSON以外の形式で応答した可能性
対策: max_tokensを増やすか、より明確なプロンプトを使用
```

### バッチが遅い
```
通常動作です：バッチAPIは非同期処理のため1-6時間かかることがあります
リアルタイム処理が必要な場合は DiseaseEnricher を使用してください（コスト2倍）
```

## 今後の拡張

### 1. 他の動物種への対応
```python
# 猫、ウマ、ウサギなどのデータも充実化可能
from api.species.cat_diseases import DISEASES as CAT_DISEASES
enricher.enrich_diseases_batch(CAT_DISEASES)
```

### 2. 医学文献との同期
```python
# 信頼できるソースからの引用を追加
enriched_disease['evidence_sources'] = [
    {'name': 'AAHA Guidelines', 'url': '...'},
    {'name': 'Veterinary Medicine Journal', 'url': '...'}
]
```

### 3. 自動更新パイプライン
```
毎月：
1. 新規疾患の追加を検出
2. 自動充実化バッチを実行
3. 品質チェック
4. 本番環境に自動デプロイ
```

## コスト最適化

| 方式 | コスト | 処理時間 | 用途 |
|------|--------|---------|------|
| リアルタイム (Enricher) | $0.05/疾患 | 数秒 | テスト・手動編集 |
| バッチ (BatchEnricher) | $0.025/疾患 | 1-6時間 | 一括処理・本運用 |

**推奨**:
- パイロット: Enricher (100疾患 ≈ $5)
- 本運用: BatchEnricher (全疾患 ≈ $12-15)

## セキュリティ考慮事項

- **APIキー管理**: 環境変数経由でのみ
- **データ保護**: 本番環境では医学データの機密性を確保
- **監査ログ**: どの疾患がいつ充実化されたかを記録

## 参考資料

- Claude API ドキュメント: https://platform.claude.com/docs
- バッチAPI: https://platform.claude.com/docs/en/build-with-claude/batch-processing
- 料金情報: https://platform.claude.com/docs/en/pricing

## 次のステップ

1. `test_enrichment.py` を実行してパイロットテスト
2. 100疾患のパイロット結果を医学的に検証
3. フロントエンドで表示確認
4. 本番実行（全543疾患）
5. 継続的メンテナンスプロセスを構築
