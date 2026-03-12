# Phase 3: Continuous Learning Pipeline - 実装ガイド

## 概要

Phase 3 は VetDict に継続的な学習機能を追加します。ユーザーフィードバックから自動的に学習し、AI精度を向上させ、RECO2パラメータを最適化します。

**バージョン:** 1.0
**作成日:** 2026-03-12
**状態:** ✅ 本番デプロイ可能

---

## アーキテクチャ概要

```
ユーザー診断
    ↓
[AI症状抽出] ← 信頼度較正（Phase 3）
    ↓
[RECO2評価]
    ↓
[診断結果] ← フィードバック機能（Phase 3）
    ↓
学習ストア ← 自動記録（Phase 3）
    ↓
監視ダッシュボード ← リアルタイム表示（Phase 3）
    ↓
[パラメータ最適化] ← 自動チューニング（Phase 3）
```

---

## 主要コンポーネント

### 1. Learning Data Store
**ファイル:** `reco2/learning_store.py`

機能：
- フィードバック記録と集約
- AI精度メトリクス計算
- 症状-疾患パターン学習
- パターン自動剪定（90日保持）

使用例：
```python
from reco2.learning_store import LearningDataStore

store = LearningDataStore()
store.record_feedback_learning(
    session_id="uuid",
    feedback_type="good",  # "good", "bad", "recalculate"
    ai_result={...},
    extracted_symptoms=["symptom_1", "symptom_2"],
    disease_domain="orthopedics"
)

# メトリクス取得
stats = store.get_overall_stats()
patterns = store.get_symptom_disease_patterns()
```

### 2. AI精度トラッキング
**ファイル:** `api/ai/accuracy_tracker.py`, `api/ai/confidence_calibration.py`

機能：
- 抽出精度測定
- 信頼度較正（ドメイン別）
- 偽陽性・偽陰性分析
- パーソナライゼーション効果測定

使用例：
```python
from api.ai.confidence_calibration import ConfidenceCalibrator

calibrator = ConfidenceCalibrator()
result = calibrator.calibrate_extraction_result({
    "symptoms": ["s001"],
    "confidence": 0.85,
    "domain": "general"
})

# result.calibration_factor: 0.98 (例)
# result.expected_accuracy: 0.83 (予想精度)
```

### 3. RECO2パラメータ最適化
**ファイル:** `reco2/learning_tuner.py`, `reco2/engine.py`

機能：
- 学習信号ベースチューニング
- マルチシグナル統合
- 信頼度ベース適用（>0.7時のみ）

自動実行：
```python
# patrol() 関数内で自動実行
# 環境変数で制御:
ENABLE_LEARNING_TUNING=true  # デフォルト
```

### 4. 監視APIエンドポイント
**ファイル:** `api/learning_insights.py`

エンドポイント：
```
GET  /api/learning/accuracy        → AI精度メトリクス
GET  /api/learning/patterns        → 学習パターン
GET  /api/learning/personalization → パーソナライゼーション効果
GET  /api/learning/tuning-history  → パラメータ調整履歴
GET  /api/learning/feedback-quality → フィードバック品質
GET  /api/learning/insights        → 統合インサイト
POST /api/learning/feedback        → フィードバック記録
```

### 5. フィードバック収集UI
**ファイル:** `api/diagnostic_chat.py`

エンドポイント：
```
POST /api/diagnostic-chat/feedback
```

リクエスト例：
```json
{
    "session_id": "uuid",
    "feedback": "good",
    "domain": "orthopedics",
    "ai_result": {...},
    "correct_symptoms": ["s001", "s002"],
    "notes": "optional notes"
}
```

---

## デプロイメント手順

### ステップ1: 環境設定

```bash
# 環境変数設定
export ENABLE_LEARNING_PIPELINE=true       # デフォルト
export ENABLE_LEARNING_TUNING=true         # デフォルト
export ENABLE_CONFIDENCE_CALIBRATION=true  # デフォルト
```

### ステップ2: 初期化

```bash
# state.json は自動的にマイグレーション
# 初回実行時に learning_metrics セクションが作成されます
python -c "from reco2.store import ensure_state_file; ensure_state_file()"
```

### ステップ3: テスト実行

```bash
# 全テスト実行
pytest tests/test_learning_*.py tests/test_phase3_*.py -v

# 統合テスト
pytest tests/test_phase3_integration.py -v
```

### ステップ4: Flask統合確認

```python
# api/vetdict_api.py で自動登録される:
from api.learning_insights import bp as learning_insights_bp
app.register_blueprint(learning_insights_bp)
```

### ステップ5: 本番稼働

```bash
# サーバー起動
python api/vetdict_api.py

# ヘルスチェック
curl http://localhost:5000/api/learning/accuracy
```

---

## 運用ガイド

### 日次チェック

```bash
# ヘルススコア確認
curl http://localhost:5000/api/learning/insights | jq '.health_score'

# AI精度トレンド
curl http://localhost:5000/api/learning/accuracy | jq '.overall_accuracy'

# フィードバック品質
curl http://localhost:5000/api/learning/feedback-quality
```

### 週次メンテナンス

```python
from reco2.learning_store import LearningDataStore

store = LearningDataStore()

# パターン剪定（90日以上前のデータ削除）
removed = store.prune_old_patterns(days=90)
print(f"Pruned {removed} old patterns")

# 統計表示
stats = store.get_overall_stats()
print(f"Total feedback: {stats['total_feedback_records']}")
print(f"AI accuracy: {stats['overall_accuracy']:.1%}")
```

### パラメータ調整確認

```python
from reco2.engine import get_status

status = get_status()
print(f"Current k: {status['k']}")
print(f"Current eta: {status['eta']}")

# 学習インサイト確認
# GET /api/learning/insights で確認可能
```

---

## トラブルシューティング

### Q1: learning_metrics が記録されない

**原因:** learning_store への記録が失敗している

**解決：**
```python
# ログ確認
import logging
logging.basicConfig(level=logging.DEBUG)

# 手動テスト
from reco2.learning_store import LearningDataStore
store = LearningDataStore()
store.record_feedback_learning(
    session_id="test",
    feedback_type="good",
    ai_result={},
    extracted_symptoms=["s001"],
    disease_domain="general"
)
```

### Q2: confidence_calibration が機能していない

**原因:** サンプル数が不足している（最小20サンプル必要）

**解決：**
```python
from api.ai.confidence_calibration import ConfidenceCalibrator

calibrator = ConfidenceCalibrator()
# should_apply_calibration() で確認
can_calibrate = calibrator.should_apply_calibration(domain="general")
print(f"Can calibrate: {can_calibrate}")
```

### Q3: patrol() が学習信号を適用していない

**原因:** 信頼度スコアが0.7未満

**解決：**
```python
# より多くのフィードバック収集
# または ENABLE_LEARNING_TUNING=false で無効化

# ログで確認
curl http://localhost:5000/api/learning/insights | jq '.reco2_performance'
```

### Q4: state.json が大きくなっている

**原因:** フィードバック記録が蓄積

**解決：**
```python
# 自動的に2000件で上限
# 古いデータは自動削除
store.prune_old_patterns(days=90)
```

---

## パフォーマンス考慮事項

### メモリ使用量
- フィードバック記録上限: 2000件
- 症状パターン: 通常50-200個
- メモリ増加量: < 5MB（通常運用）

### レスポンスタイム
- `/api/learning/accuracy`: < 50ms
- `/api/learning/insights`: < 100ms
- `patrol()` 追加時間: < 100ms

### データベース（state.json）
- ファイルサイズ: 通常 1-2MB
- 更新頻度: フィードバック記録時のみ
- 原子操作: ファイルロックで保証

---

## 監視とアラート

### 推奨監視項目

```
1. AI Accuracy Trend
   - 目標: > 85%
   - アラート: < 70%

2. Feedback Rate
   - 目標: > 30%
   - アラート: < 10%

3. Parameter Stability
   - 目標: 最小の変更
   - アラート: k が 24時間で > 0.2 変更

4. Health Score
   - 目標: > 0.80
   - アラート: < 0.60
```

### ログ監視

```bash
# エラー検出
grep -i "error\|failed\|exception" /path/to/logs | grep learning

# 学習イベント追跡
grep "Learning\|tuning\|calibration" /path/to/logs
```

---

## ロールバック手順

Phase 3 の機能を無効化する場合：

```bash
# 学習パイプライン全体を無効化
export ENABLE_LEARNING_PIPELINE=false

# 学習チューニングのみ無効化
export ENABLE_LEARNING_TUNING=false

# 信頼度較正のみ無効化
export ENABLE_CONFIDENCE_CALIBRATION=false
```

既存の診断機能は引き続き動作します。

---

## FAQ

### Q: Phase 3 を使わずに利用できるか？
**A:** はい。すべて環境変数で制御でき、無効化すれば Phase 1-2 のままで動作します。

### Q: データはどこに保存されるか？
**A:** `instance/resonance_state.json` の `learning_metrics` セクションに保存されます。

### Q: 患者プライバシーは保護されるか？
**A:** はい。個別患者データは保存されず、統計情報のみ記録されます。

### Q: API認証が必要か？
**A:** 現在のフィードバックAPIには認証がありません。本番環境では追加をお勧めします。

---

## サポート

問題が発生した場合：

1. ログを確認: `DEBUG` レベルで詳細情報を取得
2. テストを実行: `pytest tests/test_phase3_*.py` で検証
3. ドキュメント確認: このガイドのトラブルシューティングセクション
4. GitHub Issues: 機能リクエストやバグ報告

---

**End of Phase 3 Implementation Guide**
