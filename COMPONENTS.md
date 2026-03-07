# 🎨 ShowDog UI Components ガイド

## 概要

ShowDog には、症状チェック表示用の3つの主要な UI コンポーネントが含まれています。

このドキュメントでは、各コンポーネントの使用方法を説明します。

---

## 📦 コンポーネント一覧

### 1. AnalysisProgressTracker

**ファイル:** `static/js/analysis-progress.js`

**用途:** 画像/動画解析時の段階的な進捗表示

#### インスタンス化

```javascript
const tracker = new AnalysisProgressTracker('container-id');
```

#### メソッド

##### `addStep(stepId, labelJa, labelEn, icon)`

ステップを追加します。

```javascript
tracker.addStep('body_measurement', '体型測定中', 'Body Measurement', '📏');
tracker.addStep('coat_analysis', '被毛状態確認中', 'Coat Analysis', '🧼');
tracker.addStep('gait_analysis', '歩様分析中', 'Gait Analysis', '🚶');
```

| パラメータ | 型 | 説明 |
|-----------|----|----|------|
| `stepId` | string | ステップの一意識別子 |
| `labelJa` | string | 日本語ラベル |
| `labelEn` | string | 英語ラベル |
| `icon` | string | emoji アイコン |

##### `updateProgress(stepId, percentage)`

ステップの進捗パーセンテージを更新します。

```javascript
tracker.updateProgress('body_measurement', 50);  // 50% 完了
tracker.updateProgress('body_measurement', 100); // 100% 完了
```

##### `completeStep(stepId)`

ステップを完了状態にします。

```javascript
tracker.completeStep('body_measurement');
// アイコンが ⏳ → ✅ に変更される
```

##### `failStep(stepId, errorMessage)`

ステップを失敗状態にします。

```javascript
tracker.failStep('coat_analysis', 'Image quality too low');
// アイコンが ⏳ → ❌ に変更される
```

##### `skipStep(stepId)`

ステップをスキップします。

```javascript
tracker.skipStep('gait_analysis');
```

##### `getStatus()`

現在の状態を取得します。

```javascript
const status = tracker.getStatus();
console.log(status);
// {
//   steps: [...],
//   allCompleted: false,
//   anyFailed: false,
//   completedCount: 2,
//   totalSteps: 3
// }
```

##### `reset()`

すべてのステップをリセットします。

```javascript
tracker.reset();
```

#### 使用例

```javascript
// 進捗トラッキングの初期化
const progressTracker = new AnalysisProgressTracker('analysisProgress');

// ステップを追加
progressTracker.addStep('extract', '症状抽出', 'Symptom Extraction', '🔍');
progressTracker.addStep('matching', '疾患マッチング', 'Disease Matching', '🔬');
progressTracker.addStep('reasoning', '判定根拠生成', 'Reasoning', '🧠');

// 進捗を更新（シミュレーション）
let progress = 0;
const interval = setInterval(() => {
    progress += 10;

    if (progress >= 100) {
        progressTracker.completeStep('extract');
        progressTracker.updateProgress('matching', 50);
    } else if (progress >= 200) {
        progressTracker.completeStep('matching');
        progressTracker.updateProgress('reasoning', 75);
    } else if (progress >= 300) {
        progressTracker.completeStep('reasoning');
        clearInterval(interval);
    }

    if (progress > 300) clearInterval(interval);
}, 500);
```

---

### 2. DiseaseCardRenderer

**ファイル:** `static/js/diagnostic-cards.js`

**用途:** 展開可能な疾患カードの表示と操作

#### インスタンス化

```javascript
const renderer = new DiseaseCardRenderer('container-id');
```

#### メソッド

##### `renderCards(diseases)`

疾患の配列からカードを生成して表示します。

```javascript
const diseases = [
    {
        disease_id: 'brachycephalic_airway_syndrome',
        name_ja: '短頭種気道症候群',
        name_en: 'Brachycephalic Airway Syndrome',
        severity: 'high',
        similarity_score: 0.85,
        confidence_level: '85%',
        // ... その他のフィールド
    },
    // ... 他の疾患
];

renderer.renderCards(diseases);
```

##### `toggleCard(cardElement)`

カードの展開/折り畳みをトグルします。

```javascript
const card = document.querySelector('.sd-disease-card');
renderer.toggleCard(card);
```

##### `handleAction(action, cardId)`

アクションボタンのイベントを処理します。

```javascript
document.addEventListener('diseaseCardAction', (e) => {
    const { action, cardId } = e.detail;

    if (action === 'compare') {
        // 類症鑑別を表示
    } else if (action === 'treatment-plan') {
        // ケアガイドを表示
    } else if (action === 'learn-more') {
        // 詳細情報を表示
    }
});
```

#### 使用例

```javascript
// カードレンダラーを初期化
const cardRenderer = new DiseaseCardRenderer('diseaseCardsContainer');

// API から疾患データを取得
const response = await fetch('/api/diagnostic-chat/chat', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
    },
    body: JSON.stringify({
        message: '咳が続いている'
    })
});

const data = await response.json();

// カードを表示
cardRenderer.renderCards(data.disease_candidates);

// アクションハンドリング
document.addEventListener('diseaseCardAction', (e) => {
    const { action, cardId } = e.detail;
    console.log(`Action: ${action} for card: ${cardId}`);
});
```

#### カード内のタブ機能

カードは3つのタブを持ちます：

- **Overview**: 疾患説明、症状マッチング、推奨検査
- **Reasoning**: 判定根拠、信頼度ファクター
- **Care Guide**: ケアガイド、サプリメント参考情報

タブはクリックで切り替え可能です。

---

### 3. TreatmentPlanDisplay

**ファイル:** `static/js/treatment-plan.js`

**用途:** 包括的なケアガイド情報の表示

#### インスタンス化

```javascript
const planner = new TreatmentPlanDisplay(diagnosis, dogInfo);
```

| パラメータ | 型 | 説明 |
|-----------|----|----|------|
| `diagnosis` | object | 疾患参考情報オブジェクト |
| `dogInfo` | object | 犬の情報（オプション） |

#### メソッド

##### `render(containerId)`

ケアガイドを指定されたコンテナに表示します。

```javascript
const diagnosis = {
    disease_id: 'brachycephalic_airway_syndrome',
    name_ja: '短頭種気道症候群',
    name_en: 'Brachycephalic Airway Syndrome',
    severity: 'high',
    treatment_recommendations: {
        primary_care_plan_ja: '...',
        supplements: [...],
        diagnostic_tests: [...]
    }
};

const planner = new TreatmentPlanDisplay(diagnosis);
planner.render('treatmentContainer');
```

##### `exportToPDF()`

ケアガイドを PDF にエクスポートします。

```javascript
planner.exportToPDF();
```

#### 表示内容

1. **直ちに行うべきこと**
   - 獣医師の診察が必須であることを強調

2. **参考検査項目**
   - 検査名、説明、優先度
   - チェックボックスで進捗追跡

3. **推奨サプリメント**
   - 用量、頻度、理由
   - リファレンスリンク

4. **ケアスケジュール**
   - タイムライン表示
   - 各段階でのフォーカスエリア

5. **経過観察チェックリスト**
   - 監視すべき項目
   - チェックボックスで追跡

6. **医師相談用メモ**
   - プリント可能な形式

#### 使用例

```javascript
// ケアガイド表示を初期化
async function showTreatmentPlan(diseaseId) {
    // ケアガイドを取得
    const response = await fetch('/api/diagnostic-chat/treatment-plan', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
            disease_id: diseaseId,
            breed_id: 'labrador_retriever',
            age_years: 3.5
        })
    });

    const plan = await response.json();

    // 表示
    const planner = new TreatmentPlanDisplay(plan);
    planner.render('treatmentContainer');

    // ユーザー操作
    document.querySelectorAll('.sd-test-check').forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            // 検査完了トラッキング
        });
    });
}
```

---

## 🔗 コンポーネント統合

### HTML にコンポーネントをロード

```html
<head>
    <!-- デザインシステムをロード -->
    <link rel="stylesheet" href="/design-system.css">

    <!-- コンポーネントスクリプトをロード -->
    <script src="/js/analysis-progress.js"></script>
    <script src="/js/diagnostic-cards.js"></script>
    <script src="/js/treatment-plan.js"></script>
</head>
```

### HTML コンテナを配置

```html
<body>
    <!-- 進捗トラッキング -->
    <div id="progressContainer"></div>

    <!-- 疾患カード -->
    <div id="diseaseCardsContainer"></div>

    <!-- ケアガイド -->
    <div id="treatmentContainer"></div>
</body>
```

### JavaScript で統合

```javascript
// ユーザーが症状を入力
async function handleSymptomInput(message) {
    // 進捗を表示
    const tracker = new AnalysisProgressTracker('progressContainer');
    tracker.addStep('extract', '症状抽出', 'Extracting symptoms', '🔍');
    tracker.addStep('match', 'マッチング', 'Matching diseases', '🔬');
    tracker.addStep('reason', '推論', 'Generating diagnosis', '🧠');

    // API を呼び出し
    tracker.updateProgress('extract', 100);
    tracker.completeStep('extract');

    const response = await fetch('/api/diagnostic-chat/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({ message })
    });

    tracker.updateProgress('match', 100);
    tracker.completeStep('match');

    const data = await response.json();

    tracker.updateProgress('reason', 100);
    tracker.completeStep('reason');

    // カード表示
    const cardRenderer = new DiseaseCardRenderer('diseaseCardsContainer');
    cardRenderer.renderCards(data.disease_candidates);

    // 最初の疾患を選択してケアガイドを表示
    if (data.disease_candidates.length > 0) {
        const planner = new TreatmentPlanDisplay(data.disease_candidates[0]);
        planner.render('treatmentContainer');
    }
}
```

---

## 🎯 イベント処理

### 疾患カードアクション

```javascript
document.addEventListener('diseaseCardAction', (e) => {
    const { action, cardId } = e.detail;

    switch (action) {
        case 'compare':
            // 類症鑑別を表示
            showDifferentialAnalysis(cardId);
            break;
        case 'treatment-plan':
            // ケアガイドを表示
            showTreatmentPlan(cardId);
            break;
        case 'learn-more':
            // 詳細情報を表示
            showDetailedInfo(cardId);
            break;
    }
});

async function showDifferentialAnalysis(cardId) {
    const response = await fetch('/api/diagnostic-chat/differential-analysis', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
        },
        body: JSON.stringify({
            disease_id_1: cardId,
            disease_id_2: 'heart_failure', // 比較対象
            symptoms: accumulatedSymptoms
        })
    });

    const comparison = await response.json();
    displayComparison(comparison);
}
```

---

## 🎨 スタイルカスタマイズ

### CSS 変数

コンポーネントは CSS 変数を使用しており、テーマをカスタマイズできます。

```css
:root {
    --purple: #7C3AED;        /* プライマリーカラー */
    --teal: #319795;          /* セカンダリーカラー */
    --red: #EF4444;           /* エラー/緊急 */
    --orange: #F59E0B;        /* 警告 */
    --green: #10B981;         /* 成功 */
    --text: #1F2937;          /* テキスト色 */
    --text-secondary: #6B7280;/* セカンダリーテキスト */
    --border: #E5E7EB;        /* ボーダー */
    --bg: #F9FAFB;            /* 背景 */
}
```

### コンポーネント固有の CSS クラス

```css
/* 進捗コンテナ */
.sd-progress-container { }
.sd-progress-step { }
.sd-progress-fill { }

/* 疾患カード */
.sd-disease-card { }
.sd-disease-card-emergency { }
.sd-disease-card-high { }
.sd-disease-card-moderate { }
.sd-disease-card-low { }

/* ケアガイド */
.sd-treatment-plan-container { }
.sd-treatment-section { }
.sd-supplement-card { }
.sd-timeline-item { }
```

---

## 📊 レスポンシブデザイン

すべてのコンポーネントはレスポンシブです。

| デバイス | ブレークポイント | レイアウト |
|---------|-----------------|----------|
| デスクトップ | 1200px+ | 最適表示 |
| タブレット | 768px - 1200px | 2列/1列 |
| モバイル | 〜768px | 1列スタック |

---

## ⚡ パフォーマンス

### 最適化のコツ

1. **遅延ロード**
   ```javascript
   // 必要なときだけ初期化
   if (userSelected === 'treatment') {
       const planner = new TreatmentPlanDisplay(diagnosis);
       planner.render('container');
   }
   ```

2. **キャッシング**
   ```javascript
   const diagnosisCache = new Map();
   async function getDiagnosis(id) {
       if (diagnosisCache.has(id)) {
           return diagnosisCache.get(id);
       }
       const data = await fetch(...);
       diagnosisCache.set(id, data);
       return data;
   }
   ```

3. **イベントデリゲーション**
   ```javascript
   // ❌ 避ける
   cards.forEach(card => card.addEventListener('click', handler));

   // ✅ 推奨
   container.addEventListener('click', (e) => {
       if (e.target.closest('.sd-card-action')) {
           handleAction(e);
       }
   });
   ```

---

## 🔍 デバッグ

### コンソール出力

```javascript
// コンポーネントの状態を確認
console.log(tracker.getStatus());

// カード情報を確認
console.log(cardRenderer);

// イベントリスニング確認
document.addEventListener('diseaseCardAction', (e) => {
    console.log('Action received:', e.detail);
});
```

### 一般的な問題

**問題:** コンポーネントが表示されない
```javascript
// コンテナの存在確認
console.assert(
    document.getElementById('container'),
    'Container not found!'
);
```

**問題:** スタイルが反映されない
```javascript
// CSS 読み込み確認
const link = document.querySelector('link[href*="design-system"]');
console.log(link); // null でないことを確認
```

---

## 📚 関連リソース

- [API リファレンス](./API_REFERENCE.md)
- [テストガイド](./TEST_GUIDE.md)
- [実装詳細](./IMPLEMENTATION.md)

---

**Components Guide - 2026年2月17日版**
