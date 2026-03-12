# VetDict 包括的UX改善計画

全疾患4,806の詳細情報を充実化させ、ユーザー体験を大幅に向上させるための実装ロードマップ。

## 🎯 目標

- **完全性**: 全4,806疾患に対して、5つの重要フィールド（病態生理・原因・治療・予防・予後）を100%充実化
- **アクセス性**: ユーザーが簡単に疾患情報を検索・理解できるUI
- **信頼性**: 医学的に正確で実用的な情報

---

## 📈 現状分析

### 疾患分布
```
Total Diseases: 4,806
Species:       20

High Priority (>200):
  ウマ:    736 ████████████████ 15.3%
  犬:     576 ███████████      12.0%
  猫:     516 ██████████       10.7%
  鳥:     308 ██████           6.4%
  ウサギ:  271 █████            5.6%

Total (>100): 4,806 疾患（全て）
```

### データ充実度（現在）
- **完全データ**: 約33個（0.7%）
- **不完全**: 約4,773個（99.3%）
- **不足フィールド**: 病態生理、原因、治療、予防、予後

---

## 🚀 実装ロードマップ

### Phase 1: 大規模バッチ充実化（Week 1-2）
**目標**: 4,806疾患すべてを充実化

#### Step 1.1: 動物種別バッチスケジューリング
```python
# 処理順序（効率性 + インパクト）
batches = [
    ("Dog", 576),           # Week 1-Mon: ~$14.40
    ("Cat", 516),           # Week 1-Tue: ~$12.90
    ("Horse", 736),         # Week 1-Wed: ~$18.40
    ("Bird", 308),          # Week 1-Thu: ~$7.70
    ("Rabbit", 271),        # Week 1-Fri: ~$6.78
    ("Parakeet", 251),      # Week 2-Mon: ~$6.28
    ("Others-Batch1", 1200),# Week 2-Tue/Wed: ~$30.00
    ("Others-Batch2", 1148),# Week 2-Thu/Fri: ~$28.70
]

# Total Cost: ~$125 (vs $240 standard pricing)
# Savings: 50% = $125 saved!
```

#### Step 1.2: バッチスケジューラー実装
```python
# api/disease_batch_scheduler.py (新規作成)
class DiseaseEnrichmentScheduler:
    def schedule_all_species(self):
        """全動物種のバッチスケジュール"""
        species_list = self.get_all_species()
        batch_schedule = self.create_batch_schedule(species_list)
        return batch_schedule

    def submit_scheduled_batches(self):
        """スケジュール済みバッチを順序通り送信"""
        for species, batch_id in self.batch_schedule.items():
            self.submit_batch_for_species(species)
            # Wait for completion before next
            self.wait_for_completion(batch_id)
```

#### Step 1.3: GitHub Actions 自動化
```yaml
# .github/workflows/enrichment-all-species.yml
schedule:
  - cron: '0 0 * * *'  # Daily checks
jobs:
  enrichment-pipeline:
    - submit_dog_batch
    - wait_for_dog
    - retrieve_dog_results
    - submit_cat_batch
    - ... (続く)
```

---

### Phase 2: UI/UX改善（Week 2-3）

#### 2.1 検索＆フィルター強化
```javascript
// 疾患検索の高度化
{
  searchBy: ['disease_name', 'symptom', 'species'],
  filters: {
    species: ['dog', 'cat', 'horse', ...],
    urgency: ['high', 'moderate', 'low'],
    dataCompletion: ['100%', '80%+', 'any'],
    category: ['infectious', 'genetic', 'metabolic', ...]
  },
  sort: ['relevance', 'alphabetical', 'completeness']
}
```

#### 2.2 疾患詳細ページの改善
```html
<!-- 現在の構造 -->
<div class="disease-detail">
  <h2>Disease Name / 日本語名</h2>
  <section>説明</section>
  <section>病態生理</section>
  <section>原因</section>
  <section>治療</section>
  <section>予防</section>
  <section>予後</section>
</div>

<!-- 改善案：インタラクティブ設計 -->
<div class="disease-detail-enhanced">
  <header>
    <h1>{Disease Name}</h1>
    <badges>
      <span class="urgency">Urgency: High</span>
      <span class="completeness">Completeness: 100%</span>
      <span class="species">Species: Dog, Cat</span>
    </badges>
    <quick-actions>
      <btn>Ask AI</btn>
      <btn>Share</btn>
      <btn>Print</btn>
    </quick-actions>
  </header>

  <tabs>
    <tab name="Overview">
      <div class="grid-2">
        <card title="概説">説明</card>
        <card title="重症度">重要度インジケータ</card>
      </div>
    </tab>

    <tab name="Pathophysiology">
      <card title="病態生理（医学的メカニズム）">
        <content>EN: {pathophysiology}</content>
        <content>JA: {pathophysiology_ja}</content>
      </card>
    </tab>

    <tab name="Etiology">
      <card title="原因と危険因子">
        <content>EN: {causes}</content>
        <content>JA: {causes_ja}</content>
        <risk-factors>主要なリスク因子</risk-factors>
      </card>
    </tab>

    <tab name="Management">
      <card title="治療法">
        <content>EN: {treatment}</content>
        <content>JA: {treatment_ja}</content>
        <protocol-timeline>段階的治療プロトコル</protocol-timeline>
      </card>
    </tab>

    <tab name="Prevention">
      <card title="予防戦略">
        <content>EN: {prevention}</content>
        <content>JA: {prevention_ja}</content>
        <checklist>予防チェックリスト</checklist>
      </card>
    </tab>

    <tab name="Prognosis">
      <card title="予後">
        <content>EN: {prognosis}</content>
        <content>JA: {prognosis_ja}</content>
        <survival-chart>生存率チャート</survival-chart>
      </card>
    </tab>

    <tab name="References">
      <card title="参考文献と引用">
        <references>医学文献へのリンク</references>
        <citations>信頼できるソース</citations>
      </card>
    </tab>
  </tabs>

  <ai-assistant>
    <textarea placeholder="この疾患について質問してください..."></textarea>
    <button>Ask Claude AI</button>
  </ai-assistant>
</div>
```

#### 2.3 比較機能（複数疾患）
```javascript
// 疾患間比較UI
{
  compare: ['disease1', 'disease2', 'disease3'],
  comparisonTable: {
    columns: ['症状', '原因', '治療', '予後'],
    rows: [disease1, disease2, disease3]
  }
}
```

---

### Phase 3: 検索最適化（Week 3）

#### 3.1 症状→疾患マッピング
```python
# Elasticsearch/Algolia統合
{
  "symptom_disease_map": {
    "cough": [
      "Pneumonia (肺炎)",
      "Bronchitis (気管支炎)",
      "Kennel Cough (ケンネルコフ)"
    ],
    "fever": [
      "Infection",
      "Inflammation",
      "Cancer"
    ]
  }
}
```

#### 3.2 多言語サポート（英語・日本語）
```javascript
{
  i18n: {
    languages: ['en', 'ja'],
    content: {
      pathophysiology: { en: '...', ja: '...' },
      causes: { en: '...', ja: '...' },
      // etc
    }
  }
}
```

---

### Phase 4: 分析＆最適化（Week 4）

#### 4.1 ユーザー行動分析
```javascript
// トラッキング
{
  events: {
    disease_view: "疾患ページ閲覧",
    field_click: "フィールドクリック",
    search_query: "検索クエリ",
    ai_question: "AI質問"
  }
}
```

#### 4.2 品質フィードバック
```javascript
// 疾患ページ上のフィードバック
<div class="feedback">
  <q>この情報は役に立ちましたか？</q>
  <buttons>
    <btn>👍 Helpful</btn>
    <btn>👎 Not helpful</btn>
    <btn>🐛 Report error</btn>
  </buttons>
</div>
```

---

## 📊 コスト見積もり

### Phase 1: 充実化バッチ処理
```
計算式: 疾患数 × $0.025 (バッチ50%割引)

Dog:       576 × $0.025 = $14.40
Cat:       516 × $0.025 = $12.90
Horse:     736 × $0.025 = $18.40
Bird:      308 × $0.025 = $7.70
Rabbit:    271 × $0.025 = $6.78
Parakeet:  251 × $0.025 = $6.28
Others:  2,148 × $0.025 = $53.70
────────────────────────────
Total (4,806):           $120.16

vs Standard Pricing:     $240.30
Savings (50%):           $120.14
```

### Phase 2-4: UI/UX開発
```
Frontend Development:      24-40 hours
Backend Integration:       16-24 hours
Testing & QA:              16-24 hours
Deployment:                 4-8 hours
────────────────────────────
Total:                   60-96 hours
Cost (at $50/hr):      $3,000-4,800
```

---

## 🎯 期待される成果

### Before
```
✗ 99.3% 疾患データ不完全
✗ シンプルな疾患一覧表示
✗ 詳細情報が見つけづらい
✗ ユーザーが手動で追加調査が必要
```

### After
```
✓ 100% 疾患データ完全充実化
✓ インタラクティブな詳細ページ
✓ 直感的な検索・フィルター
✓ AI質問機能で即座に回答
✓ 複数疾患の比較機能
✓ 完全な医学的情報
```

---

## 📋 実装チェックリスト

### Phase 1
- [ ] 全20動物種のバッチスケジュール作成
- [ ] バッチスケジューラーモジュール実装
- [ ] GitHub Actions 自動化パイプライン設定
- [ ] バッチ送信・監視・結果取得の自動化
- [ ] データ品質検証スクリプト

### Phase 2
- [ ] 検索UI コンポーネント開発
- [ ] フィルター機能実装
- [ ] タブベースUIの構築
- [ ] 多言語サポート統合

### Phase 3
- [ ] Elasticsearch/Algolia統合
- [ ] 症状→疾患マッピング構築
- [ ] 検索インデックス作成

### Phase 4
- [ ] アナリティクス統合
- [ ] ユーザーフィードバック機能
- [ ] 品質スコアリング

---

## 🚀 実行タイムライン

```
Week 1:  Phase 1 (バッチ充実化)
         Mon: Dog (576)
         Tue: Cat (516)
         Wed: Horse (736)
         Thu: Bird (308)
         Fri: Rabbit (271)

Week 2:  Phase 1 (続き) + Phase 2 開始
         Mon: Parakeet (251) + UI設計
         Tue-Fri: Others (2,148) + UI開発

Week 3:  Phase 2 (UI/UX) + Phase 3 開始
         完全UI実装
         検索最適化

Week 4:  Phase 4 (分析・最適化)
         テスト・デプロイ準備
```

---

## 🎨 UI改善のビジュアル例

### 現在
```
Disease Name
Description
(5つのフィールド：説明、病態生理、原因、治療、予防、予後)
```

### 改善後
```
┌─ Disease Name / 日本語名 ─────────────────┐
│ [🔴 Urgency: High] [📊 100% Complete]      │
├────────────────────────────────────────────┤
│ ○ Overview  ○ Pathophysiology  ○ Causes   │
│ ○ Treatment ○ Prevention        ○ Prognosis│
├────────────────────────────────────────────┤
│ [Selected Tab Content]                     │
│                                            │
│ English: ....                              │
│ 日本語:  ....                              │
│                                            │
│ 🔗 References | 📄 Print | 📤 Share       │
├────────────────────────────────────────────┤
│ 💬 Ask AI: "How to diagnose this?"        │
│ [Ask]                                      │
└────────────────────────────────────────────┘
```

---

## 🔗 関連リソース

- `api/disease_batch_enricher.py` - バッチ処理モジュール
- `docs/DISEASE_CONTENT_ENRICHMENT.md` - 充実化ガイド
- `scripts/run_disease_enrichment.py` - 実行スクリプト

---

## 📞 次のステップ

1. ✅ Phase 1 バッチ充実化を開始
2. 📋 Phase 2 UI設計レビュー
3. 🎨 Phase 3 検索機能設計
4. 📊 Phase 4 アナリティクス統合

このロードマップに従い、段階的に全疾患4,806の完全充実化とUX改善を実現します！
