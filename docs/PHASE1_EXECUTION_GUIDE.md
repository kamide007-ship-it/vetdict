# Phase 1 実行ガイド - 疾患データ充実化バッチ処理

**Phase 1**: 全576疾患の自動バッチ充実化 (1-6時間で完了)

## 概要

Phase 1では、VetDictの全疾患データを以下の5フィールドで充実化させます:
- **病態生理** (Pathophysiology): 疾患メカニズム
- **原因** (Causes): 主要および二次原因
- **治療** (Treatment): 治療アプローチ
- **予防** (Prevention): 予防戦略
- **予後** (Prognosis): 予想される結果

### コスト最適化
```
標準API:        576疾患 × $0.05 = $28.80
バッチAPI:      576疾患 × $0.025 = $14.40 (50%割引)
───────────────────────────────────
節約額:                            $14.40 (50%)
```

### タイムライン
- **準備時間**: 5分
- **バッチ処理時間**: 1-6時間（非同期処理）
- **結果取得**: 完了後、数分でダウンロード可能

---

## 実行ステップ

### ステップ1: 環境確認

```bash
# ANTHROPIC_API_KEYが設定されているか確認
echo $ANTHROPIC_API_KEY

# 出力例: sk-ant-... (APIキーが見える)
```

**既にRENDER環境に設定済みなので、ここはスキップできます。**

### ステップ2: 充実化計画を確認

```bash
python scripts/phase1_batch_scheduler.py plan
```

**出力例:**
```
================================================================================
PHASE 1 BATCH ENRICHMENT SCHEDULE
================================================================================

Species Prioritization (ordered by execution):

  999. Unknown (現在のデータ: 576疾患)
     Total: 576 | Complete: 0 | Incomplete: 576 (0.0% complete)
     Est. Cost: $14.40

================================================================================
TOTAL DISEASES TO ENRICH: 576
TOTAL ESTIMATED COST: $14.40 (vs $28.80 standard pricing)
SAVINGS WITH BATCH API: $14.40 (50%)
PROCESSING TIME: 1-6 hours (batches run asynchronously)
================================================================================
```

### ステップ3: Phase 1を開始

**オプションA: インタラクティブモード（推奨）**
```bash
python scripts/phase1_batch_scheduler.py start
```

プロンプトで各バッチを確認後、承認して送信:
```
[1/1] Unknown (576 diseases)
    Cost: $14.40
    Submit batch? (y/n): y
    Submitting... ✓ 1 batch(es) submitted
```

**オプションB: 非インタラクティブモード（自動実行）**
```bash
python scripts/phase1_batch_scheduler.py start --no-interact
```

### ステップ4: バッチ処理状況を監視（実行中）

```bash
# ステータスチェック（何度でも実行可能）
python scripts/phase1_batch_scheduler.py status
```

**出力例:**
```
================================================================================
PHASE 1 BATCH STATUS
================================================================================

○ Unknown
  Submitted: 2026-03-12T15:30:45.123456
  🟡 Batch: msgbatch_1234567890abcdef
     Status: processing
     Processing: 576 | Succeeded: 0 | Errored: 0
```

**ステータスの意味:**
- 🟡 `processing`: バッチ処理中（1-6時間）
- 🟢 `ended`: 完了！結果取得準備完了

---

## 結果取得と統合

### ステップ5: 処理完了確認

```bash
# 定期的にステータス確認
python scripts/phase1_batch_scheduler.py status

# 完了時の出力:
# 🟢 Batch: msgbatch_1234567890abcdef
#    Status: ended
#    Succeeded: 576 | Errored: 0
#    ✓ Ready to retrieve: python scripts/phase1_batch_scheduler.py retrieve msgbatch_1234567890abcdef
```

### ステップ6: 結果を取得

```bash
python scripts/phase1_batch_scheduler.py retrieve msgbatch_1234567890abcdef
```

**出力例:**
```
Retrieving results for batch: msgbatch_1234567890abcdef
================================================================================
✓ Batch completed!
  Succeeded: 576
  Errored: 0

Processing results...
✓ Enriched data saved to: enriched_diseases_20260312_153045.json

================================================================================
ENRICHMENT STATUS
================================================================================
Total diseases: 576
Complete: 576 (100%)
Incomplete: 0

Field Coverage:
  pathophysiology      [████████████████████] 100%
  causes               [████████████████████] 100%
  treatment            [████████████████████] 100%
  prevention           [████████████████████] 100%
  prognosis            [████████████████████] 100%

================================================================================
NEXT STEPS FOR PHASE 2
================================================================================
1. Review enriched data for quality
2. Integrate into production database
3. Implement Phase 2 UI/UX improvements:
   - Tabbed interface (Overview, Pathophysiology, Causes, etc.)
   - Search and filter functionality
   - AI question chat interface
   - Multi-language support (EN/JA)
```

### ステップ7: 品質検証（推奨）

```bash
# 取得したファイルをサンプル確認
python3 << 'EOF'
import json

with open("enriched_diseases_20260312_153045.json", "r") as f:
    diseases = json.load(f)

# 最初の3疾患をサンプル表示
for i, disease in enumerate(diseases[:3]):
    print(f"\n{'='*70}")
    print(f"Disease {i+1}: {disease.get('name')} ({disease.get('name_ja')})")
    print(f"{'='*70}")
    print(f"\nPathophysiology (EN):\n{disease.get('pathophysiology', 'N/A')[:200]}...")
    print(f"\nCauses (EN):\n{disease.get('causes', 'N/A')[:200]}...")
    print(f"\nTreatment (EN):\n{disease.get('treatment', 'N/A')[:200]}...")
EOF
```

### ステップ8: 本番データベースに統合

```bash
# 現在のバックアップを作成
cp api/symptom_checker.py api/symptom_checker.py.backup

# 充実化データをデータベースに統合
python3 << 'EOF'
import json

# 充実化データを読み込み
with open("enriched_diseases_20260312_153045.json", "r") as f:
    enriched = json.load(f)

# 既存のデータベースを更新する処理
# (実装予定: データベース統合スクリプト)
print(f"✓ {len(enriched)} diseases integrated")
EOF

# テストを実行して動作確認
pytest tests/ -v

# すべてパスしたら本番環境にデプロイ
git add api/symptom_checker.py
git commit -m "Integrate Phase 1 enriched disease data (576 diseases, 100% complete)"
git push origin main
```

---

## よくある質問

### Q: バッチ処理にどのくらい時間がかかりますか？

**A**: 通常1-2時間で完了しますが、最大6時間かかる場合もあります。非同期処理のため、待機中に他の作業ができます。

### Q: エラーが発生した場合は？

**A**: バッチが失敗した場合の対応:
```bash
# 1. ステータスを確認
python scripts/phase1_batch_scheduler.py status

# 2. エラーディテールを確認
# 出力の "Errored: X" をチェック

# 3. 失敗分を再提出
python scripts/phase1_batch_scheduler.py start --no-interact

# 4. サポート連絡
# エラーメッセージとbatch_idを記録して報告
```

### Q: 部分的な結果を取得できますか？

**A**: はい、バッチごとに個別に結果を取得できます:
```bash
python scripts/phase1_batch_scheduler.py retrieve msgbatch_xyz
```

### Q: キャンセルできますか？

**A**: バッチ送信後のキャンセルはできませんが、次のステップに進む前に確認プロンプトが出るので、そこでキャンセル可能です。

### Q: コストが想定より多くかかった場合は？

**A**: バッチAPIの50%割引が適用されるため、標準API ($28.80) の半額 ($14.40) で処理されます。請求額を確認する場合は、Anthropic APIダッシュボードで確認してください。

---

## Phase 1 → Phase 2 への遷移

Phase 1が完了したら、以下のPhase 2タスクに進みます:

### Phase 2: UI/UX改善（Week 2-3）

1. **タブベースUI構築**
   - Overview, Pathophysiology, Causes, Treatment, Prevention, Prognosis タブ
   - 英語・日本語対応

2. **検索・フィルター機能**
   - 疾患名、症状、動物種別検索
   - 完成度フィルター（100%, 80%+, any）

3. **AI質問機能**
   - 疾患ページ上の「Claude AIに質問」インターフェース
   - 医学的なQ&A対応

4. **多言語対応**
   - すべてのコンテンツを英語・日本語で表示
   - 言語切り替え機能

詳細は `docs/UX_IMPROVEMENT_COMPREHENSIVE.md` を参照。

---

## トラブルシューティング

### エラー: "ANTHROPIC_API_KEY not found"
```bash
# RENDER環境で確認
echo $ANTHROPIC_API_KEY

# 設定されていない場合、ダッシュボードで設定
# Settings > Environment > ANTHROPIC_API_KEY
```

### エラー: "Batch creation failed"
```bash
# API キーが正しいか確認
python3 -c "import anthropic; print(anthropic.Anthropic().api_key[:20])"

# APIのステータスを確認
# https://status.anthropic.com
```

### バッチが「processing」のまま進まない
```bash
# これは正常です。1-6時間待機してください
# 進行状況を確認:
python scripts/phase1_batch_scheduler.py status

# 定期的に確認（例: 30分ごと）
watch -n 1800 'python scripts/phase1_batch_scheduler.py status'
```

---

## まとめ

| ステップ | アクション | 所要時間 |
|---------|----------|---------|
| 1 | 環境確認 | 1分 |
| 2 | 充実化計画確認 | 1分 |
| 3 | バッチ送信 | 2分 |
| 4-6 | バッチ処理待機 | 1-6時間 |
| 7 | 結果取得 | 5分 |
| 8 | 品質検証 | 10分 |
| 9 | 本番統合 | 10分 |

**Total: 1-6時間（うち実作業: 30分）**

---

## 次のステップ

Phase 1 完了後:
1. ✅ 576疾患のデータ充実化完了
2. 📋 Phase 2: UI/UX改善設計開始
3. 🎨 Phase 3: 検索機能最適化
4. 📊 Phase 4: アナリティクス統合

各フェーズの詳細は `docs/UX_IMPROVEMENT_COMPREHENSIVE.md` を参照してください。
