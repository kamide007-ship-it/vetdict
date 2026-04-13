# VetDict 次セッション詳細計画書
**作成日**: 2026-04-13  
**対象セッション**: 次期実装フェーズ

## 現在の状態（2026-04-13確認）

### ✅ 完成済み項目
```
✓ Treatment フィールド (JA + EN): 100% (3,232/3,232)
  - Emergency: 617件 (全て治療内容あり)
  - High: 2,615件 (全て治療内容あり)

✓ 医学用語品質: 高
  - 種別特異的禁忌: 完全に記載（ウサギ/ハムスター/チンチラ等）
  - 用量・投与経路: 100% 詳細記載
  - 参考文献: 100+ citations

✓ テンプレート文: 完全削除
  - 「ウイルス感染症には特異的抗ウイルス薬がない」: 0件
  - 不正テンプレート: 0件 (2026-04-第3回で267件→0件に完全修正)

✓ Critical fields: 100% 埋まっている
  - Null fields: 0件
  - Empty fields: 0件

✓ データ整合性
  - Wrong species references: 降低中 (30→23件, セッション中修正予定)
  - 疾患数: 6,393 (全21動物種)
```

### 🟡 注意: 短いテキスト (129件)
**判定**: これらは「テンプレート不足」ではなく **「concise だが的確な記載」**  
**例**: 「脱出したチークポーチを生理食塩水で湿潤保持→糖溶液で浮腫軽減→用手的に整復。壊死組織がある場合は外科的切除」  
→ **拡充不要** (既に臨床的に適切)

---

## 次セッションの優先度別タスク

### 【Phase 1】CI/CD強化（1-2日）
**目的**: 自動品質保証の構築  
**難度**: 中  
**効果**: 開発速度向上 + バグ防止

#### Task 1-1: テストカバレッジ計測
```bash
# 現状
python3 -m pytest tests/ --cov=api --cov-fail-under=60

# CI統合 (.github/workflows/test.yml)
- name: Test with coverage
  run: |
    python3 -m pytest tests/ --cov=api --cov-fail-under=60 --cov-report=term-missing
```

**対象**: pytest 3,037件（既存テストスイート）  
**期待**: カバレッジ ~70% 達成

#### Task 1-2: ruff lint の厳格化
```toml
# pyproject.toml
[tool.ruff.lint]
select = ["E", "F", "W", "C90", "N", "D"]  # 拡張
fail-unexamined-exception-handlers = true   # 厳格化
```

**対象**: API, scripts, tests  
**期待**: lint score 100 達成

#### Task 1-3: pre-commit hooks の導入
```yaml
# .pre-commit-config.yaml (新規)
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest
        entry: bash -c 'python3 -m pytest -x --tb=short'
        language: system
        types: [python]
        stages: [commit]
```

**効果**: ローカル検証の自動化 → push直前にバグ検出

---

### 【Phase 2】データベース最適化（2-3日）
**目的**: パフォーマンス向上 + スケーラビリティ確保  
**難度**: 高  
**効果**: クエリ速度 10-100倍向上

#### Task 2-1: diseases_all_species.json → SQLite マイグレーション
```python
# scripts/migrate_diseases_to_sqlite.py (新規)
"""
Migrate 6,393 diseases from JSON to SQLite with proper indexing
"""

CREATE TABLE diseases (
    id TEXT PRIMARY KEY,
    name_ja TEXT NOT NULL,
    name TEXT NOT NULL,
    species TEXT NOT NULL,
    urgency TEXT,
    treatment_ja TEXT,
    treatment TEXT,
    diagnosis_ja TEXT,
    diagnosis TEXT,
    symptoms TEXT,  -- JSON array
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE INDEX idx_species ON diseases(species);
CREATE INDEX idx_urgency ON diseases(urgency);
CREATE INDEX idx_species_urgency ON diseases(species, urgency);
```

**現状**: JSON ファイル (1.2 MB)  
**目標**: SQLite + WAL + インデックス  
**期待効果**:
- 診断クエリ: 50ms → 5ms
- メモリ使用: 20 MB → 5 MB
- 同時接続対応

#### Task 2-2: 検索インデックスの追加
```python
# Full-text search index
CREATE VIRTUAL TABLE diseases_fts USING fts5(
    name_ja,
    name,
    symptoms_ja,
    treatment_ja,
    content=diseases
);
```

**効果**: フリーテキスト検索が 1秒以下で応答

#### Task 2-3: キャッシュ戦略の実装
```python
# app.py
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'simple',
    'CACHE_DEFAULT_TIMEOUT': 3600
})

@app.route('/api/disease/<disease_id>')
@cache.cached(timeout=3600)
def get_disease(disease_id):
    ...
```

**効果**: 診断結果の応答速度を 50% 削減

---

### 【Phase 3】診断精度の体系的検証（3-5日）
**目的**: TRIPOD準拠の検証フレームワーク構築  
**難度**: 最高  
**効果**: 臨床信頼性の科学的根拠化

#### Task 3-1: 検証プロトコルの策定
**参考**: TRIPOD (Transparent Reporting of Evaluations with Nonrandomized Designs)

```python
# scripts/validate_diagnostic_accuracy.py
"""
Diagnostic accuracy validation framework

Metrics:
- Sensitivity: TP / (TP + FN)
- Specificity: TN / (TN + FP)
- PPV (Positive Predictive Value): TP / (TP + FP)
- NPV (Negative Predictive Value): TN / (TN + FN)
- F1-score: 2 * (Precision * Recall) / (Precision + Recall)
"""

# Gold standard: 100+ケースの臨床専門家評価
# Test set: 26テストケース → 100+ケースに拡張

# Subgroup analysis:
# - Species: 犬 vs 猫 vs ウサギ vs 鳥 vs 爬虫類
# - Urgency: emergency vs high vs normal
# - Symptom count: 1-2 vs 3-5 vs 6+
```

**期待結果**:
```
Overall sensitivity: 85-92%
Overall specificity: 88-95%
Emergency cases sensitivity: 90-95%
High-urgency sensitivity: 85-90%
```

#### Task 3-2: 診断精度改善の優先度付け
```python
# 現在の課題疾患
failing_cases = [
    ('Hamster eyeball protrusion', 43.2%, 'rank1達成だが信頼度低'),
    ('Fish dropsy', 58.9%, '症状マッチ限界'),
    ('Rabbit stasis', 95.0%, '✓OK'),
]

# 改善戦略
# 1. SYMPTOM_ALIASES 拡張 (口語表現 500→1000)
# 2. _SYN 辞書 拡張 (シノニムマッピング)
# 3. 有病率補正の都市化 (日本固有の疾患分布)
# 4. 多言語対応 (EN/JA/中文)
```

#### Task 3-3: 科学文献に基づく検証
```
参考文献戦略:
1. JAMA AI: ML in clinical diagnosis (Rajkomar 2018, Esteva 2019)
2. Veterinary Surgery: equine anesthesia mortality (Bidstrup 2013)
3. AAHA/AVMA Guidelines: species-specific protocols
4. WSAVA: global standardization

期待: 20-30 citations の新規追加
```

---

### 【Phase 4】機能拡張（オプション）
**目的**: ユーザー体験と臨床価値の向上  
**難度**: 中～高  
**優先度**: 低～中（Phase 1-3 完了後）

#### 4-1: 多言語対応の拡張
```
Current: JA + EN
Candidate:
- Chinese (Simplified): veterinary education市場（中国）
- Korean: 韓国の動物病院
- German: European veterinary standards
- Spanish: Latin American market
```

#### 4-2: データネイティブ検証
```python
# AI enrichment の臨床レビュー文書化
# api/review_logs.py (新規)
"""
Document clinical review of AI-enriched content

Fields:
- enriched_text: AI生成テキスト
- reviewer_id: 獣医師ID
- review_date: レビュー日時
- approved: Yes/No
- comments: 修正履歴
- confidence_level: 実装確度 (high/medium/low)
"""
```

#### 4-3: 機械学習ベースの改善
```python
# future/ml_ranking.py (将来用)
"""
Train on historical diagnosis patterns

Model:
- Input: symptoms + species + prevalence
- Output: disease ranking + confidence scores
- Training: 3,000+ historical cases

Tech: scikit-learn or TensorFlow
"""
```

---

## 実装優先度（推奨）

### 🔴 最優先（次セッション実施）
1. **Phase 1-1**: テストカバレッジ計測（1-2時間）
   - ROI: テスト品質の見える化
   - Risk: 低
   
2. **Phase 1-2**: ruff lint 厳格化（30分）
   - ROI: コード品質向上
   - Risk: 既存テスト修正の可能性

### 🟠 高優先（次々セッション）
3. **Phase 2-1**: SQLiteマイグレーション（2-3日）
   - ROI: パフォーマンス 10-100倍向上
   - Risk: 中（バックアップ必須）

4. **Phase 3-1**: 検証プロトコル策定（1日）
   - ROI: 臨床信頼性の科学的根拠化
   - Risk: 低（実装なし、設計のみ）

### 🟡 中優先（季節ごと）
5. **Phase 3-2**: 診断精度改善（3-5日）
   - ROI: 診断精度 +5-10%
   - Risk: 中

6. **Phase 4**: 機能拡張（優先度ベース）
   - ROI: マーケット拡大（中国・韓国市場）
   - Risk: 高（翻訳品質管理）

---

## テスト戦略

### 各 Phase のテスト計画

#### Phase 1: CI/CD強化
```bash
# Coverage report
pytest tests/ --cov=api --cov-report=html
# 期待: 60% → 70% (500+ lines covered)

# Lint check
ruff check api/ scripts/ tests/
# 期待: 0 errors, 0 warnings
```

#### Phase 2: データベース最適化
```python
# Migration verification
- Record count: 6,393件 == 6,393件 ✓
- Fields integrity: 全フィールドマッピング確認 ✓
- Performance: query latency < 10ms ✓

# Backward compatibility
- JSON API: 互換性維持 ✓
-診断エンジン: 精度変わらず ✓
```

#### Phase 3: 診断精度検証
```python
# Gold standard validation
- 100+ expert-annotated cases
- Confusion matrix: TP/TN/FP/FN 集計
- Species-level breakdown: 全21種対応確認

# Regression test
- 既存の26テストケース: 精度変わらず
```

---

## 依存関係と制約

### 技術的制約
- **Python**: 3.11+ (現行環境)
- **DB**: SQLite (Render対応)
- **API**: Flask + Gunicorn (現行環境)
- **Test**: pytest 3,037件 (既存スイート)

### 時間・リソース
- **開発環境**: Claude Code + local git
- **CI/CD**: GitHub Actions (現行)
- **デプロイ**: Render (15分無操作スリープ既知)

### リスク緩和
- **バックアップ**: `diseases_all_species.json.backup_*` 複数世代保持
- **版管理**: git branching per phase
- **ロールバック**: tag-based復旧計画

---

## 成功基準

| Phase | 成功指標 |
|-------|---------|
| 1 | テストカバレッジ ≥60%, lint score 100 |
| 2 | クエリ < 10ms, メモリ < 5MB |
| 3 | 感度 ≥85%, 特異度 ≥88%, PPV ≥90% |
| 4 | NPS ≥70 (多言語市場) |

---

## 参考情報

### 既存テストスイート
```
tests/test_vetdict_api.py          — API エンドポイント (500+)
tests/test_diagnostic_chat.py      — 診断エンジン (100+)
tests/test_drug_dictionary.py      — 薬品DB (50+)
tests/test_disease_store.py        — 疾患ストア (100+)
tests/test_anesthesia_*.py         — 麻酔プロトコル (237)
--- 計 3,037 件
```

### ドメイン知識
```
臨床意思決定支援: 診断精度の定量化が必須
獣医教育: 初学者向けの説明冗長性が必要
多言語化: 医学用語の正確性がコスト（翻訳品質管理）
```

---

## 次セッション開始時のチェックリスト
```
□ ブランチ確認: claude/* (feature branch)
□ テスト実行: pytest tests/ -x -q (全テスト合格)
□ git log確認: 最新コミットが分かる状態
□ backup確認: diseases_all_species.json.backup_* が存在
□ CLAUDE.md更新: 次セッション欄に本計画書をコミット
```

---

**計画書 version**: 1.0  
**最終更新**: 2026-04-13 (Claude Code session)  
**状態**: Ready for next phase implementation
