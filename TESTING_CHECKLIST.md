# ✅ ShowDog UI Components - テスト実行チェックリスト

## 📋 テスト実施チェックリスト

このチェックリストを使用して、実装されたすべてのコンポーネントが正常に動作することを確認してください。

---

## 🧪 テスト 1: コンポーネントローディング

### 目的
スクリプトとスタイルが正しくロードされていることを確認

### テスト手順

1. **ブラウザのコンソール (F12) を開く**

2. **以下のコマンドを実行して、クラスが定義されているか確認**

```javascript
// 進捗トラッキングが利用可能
console.log(typeof AnalysisProgressTracker); // 'function' と表示されるべき

// 疾患カードが利用可能
console.log(typeof DiseaseCardRenderer); // 'function' と表示されるべき

// ケアガイドが利用可能
console.log(typeof TreatmentPlanDisplay); // 'function' と表示されるべき
```

### ✅ 確認項目

- [ ] AnalysisProgressTracker が 'function' として返される
- [ ] DiseaseCardRenderer が 'function' として返される
- [ ] TreatmentPlanDisplay が 'function' として返される
- [ ] コンソールにエラーが表示されない

### ❌ 失敗時のトラブルシューティング

```javascript
// スクリプトの読み込み状態を確認
const scripts = Array.from(document.querySelectorAll('script'));
scripts.forEach(s => {
    if (s.src.includes('analysis-progress') ||
        s.src.includes('diagnostic-cards') ||
        s.src.includes('treatment-plan')) {
        console.log('Script loaded:', s.src);
    }
});
```

**解決方法:**
- [ ] ハードリフレッシュ (Ctrl+Shift+R)
- [ ] ブラウザキャッシュをクリア
- [ ] /js ディレクトリのファイルが存在するか確認

---

## 🎬 テスト 2: 解析進捗アニメーション

### 目的
AnalysisProgressTracker が正常に動作すること

### テスト手順

1. **デモページにアクセス**
   ```
   http://localhost:5000/components-demo.html
   ```

2. **"1️⃣ 解析進捗アニメーション" セクションで "デモを実行" をクリック**

### ✅ 確認項目

#### ビジュアル確認
- [ ] 3つのステップが表示される
- [ ] 各ステップにアイコンが表示される
- [ ] プログレスバーが表示される
- [ ] テキストが日本語＋英語で表示される

#### 動作確認
- [ ] プログレスバーがスムーズに進行する
- [ ] ステップ完了時にアイコンが ⏳ → ✅ に変更される
- [ ] パーセンテージが 0% から 100% に更新される
- [ ] 3秒後にアラートが表示される

#### パフォーマンス
- [ ] アニメーションが滑らか（60 FPS）
- [ ] CPU 使用率が適切

### 🔍 詳細チェック

```javascript
// デモで実際にテスト
const tracker = new AnalysisProgressTracker('test-container');
tracker.addStep('step1', 'ステップ1', 'Step 1', '📏');
tracker.addStep('step2', 'ステップ2', 'Step 2', '🧼');

// 進捗更新
tracker.updateProgress('step1', 50);
console.log(tracker.getStatus()); // 状態確認

// 完了
tracker.completeStep('step1');
console.log(tracker.getStatus()); // 完了状態確認
```

---

## 🎨 テスト 3: 疾患カード

### 目的
DiseaseCardRenderer が正常に動作すること

### テスト手順

1. **デモページの "2️⃣ 疾患カード" セクションで "デモを実行" をクリック**

### ✅ ビジュアル確認

#### カード表示
- [ ] 2つの疾患カードが表示される
- [ ] 各カードに以下の情報が表示される：
  - [ ] 疾患名（日本語）
  - [ ] 疾患名（英語）
  - [ ] 重症度バッジ
  - [ ] 信頼度スコア（%）
  - [ ] プログレスバー

#### 色分けの確認
- [ ] 短頭種気道症候群: オレンジ（⚠️ 高）
- [ ] 心不全: 赤（🚨 緊急）

### ✅ 操作確認

#### カード展開
- [ ] カードをクリックすると展開する
- [ ] 展開時にスムーズなアニメーション（0.3s）
- [ ] 再度クリックで折り畳まれる
- [ ] 同時に1つだけ展開（他は折り畳まれる）

#### タブ操作
展開時に以下のタブが表示される：

**Overview タブ:**
- [ ] 疾患説明が表示される
- [ ] 症状マッチング情報
- [ ] 推奨検査リスト

**Reasoning タブ:**
- [ ] 判定根拠（日本語）
- [ ] 判定根拠（英語）
- [ ] 信頼度ファクターのグラフ
- [ ] パーセンテージが正確

**Treatment タブ:**
- [ ] ケアガイド
- [ ] サプリメント情報
- [ ] 用量と頻度

### 🔍 詳細チェック

```javascript
// カード情報を確認
const renderer = new DiseaseCardRenderer('test-container');
const mockDiseases = [
    {
        disease_id: 'test',
        name_ja: 'テスト疾患',
        name_en: 'Test Disease',
        severity: 'high',
        similarity_score: 0.85,
        // ... その他のフィールド
    }
];

renderer.renderCards(mockDiseases);

// アクションイベントを確認
document.addEventListener('diseaseCardAction', (e) => {
    console.log('Action:', e.detail); // { action: '...', cardId: '...' }
});
```

---

## 💊 テスト 4: ケアガイド表示

### 目的
TreatmentPlanDisplay が正常に動作すること

### テスト手順

1. **デモページの "3️⃣ ケアガイド表示" セクションで "デモを実行" をクリック**

### ✅ ビジュアル確認

#### セクション表示
以下のセクションがすべて表示されること：

- [ ] ヘッダー（🏥 ケアガイド）
- [ ] 直ちに行うべきこと
- [ ] 参考検査項目
- [ ] 推奨サプリメント
- [ ] ケアスケジュール（タイムライン）
- [ ] 経過観察チェックリスト
- [ ] 医師相談用メモ

#### コンテンツ確認

**参考検査:**
- [ ] 検査名が表示される
- [ ] 優先度が表示される（優先度1, 2, 3）
- [ ] 説明が表示される
- [ ] チェックボックスが操作可能

**サプリメント:**
- [ ] 名前（日本語＋英語）
- [ ] 用量
- [ ] 頻度
- [ ] 理由
- [ ] 参考リンク

**スケジュール:**
- [ ] タイムラインが表示される
- [ ] 本日、2週間後、2ヶ月後の段階
- [ ] 各段階の説明

**経過観察:**
- [ ] チェックリスト項目
- [ ] チェックボックス機能
- [ ] 警告メッセージ

### ✅ 機能確認

#### インタラクション
- [ ] 検査チェックボックスをクリック可能
- [ ] サプリメントチェックボックスをクリック可能
- [ ] 経過観察チェックボックスをクリック可能
- [ ] プリントボタンが機能

#### プリント機能
1. ページ右下の **🖨️ プリント** をクリック
2. プリント設定ダイアログが表示される
3. [ ] 医師相談用メモが印刷可能な形式

### 🔍 詳細チェック

```javascript
// ケアガイドをテスト
const diagnosis = {
    name_ja: 'テスト疾患',
    severity: 'high',
    treatment_recommendations: {
        supplements: [
            {
                name_ja: 'テストサプリ',
                dosage: '100mg',
                frequency: '毎日'
            }
        ]
    }
};

const planner = new TreatmentPlanDisplay(diagnosis);
planner.render('test-container');

// チェックボックス操作テスト
document.querySelectorAll('.sd-test-check').forEach(cb => {
    console.log('Test checkbox:', cb);
    cb.click();
    console.log('Checked:', cb.checked);
});
```

---

## 🔗 テスト 5: 実装統合テスト

### 目的
diagnostic-chat.html での実装統合を確認

### テスト手順

1. **ブラウザで `/diagnostic-chat.html` にアクセス**

2. **チャットボックスに症状を入力**
   ```
   例：「咳が続いている、呼吸が苦しい、いびきをかいている」
   ```

3. **送信ボタンをクリック**

### ✅ 確認項目

#### UI 表示
- [ ] AIメッセージが表示される
- [ ] 抽出された症状がサイドパネルに表示される
- [ ] 関連疾患（参考）がリスト表示される

#### コンポーネント表示
- [ ] `diseaseCardsContainer` が表示される
- [ ] 展開可能な疾患カードが表示される
- [ ] `treatmentContainer` が表示される
- [ ] ケアガイドが表示される

#### インタラクション
- [ ] 関連疾患（参考）をクリック可能
- [ ] カードが展開/折り畳み可能
- [ ] タブが切り替え可能
- [ ] スクロールで全コンテンツが見える

### 🔍 API レスポンス確認

1. **Network タブを開く (F12 → Network)**

2. **症状を入力して送信**

3. `/api/diagnostic-chat/chat` リクエストを確認

4. **レスポンスに以下フィールドが含まれているか確認：**
   - [ ] `disease_candidates`
   - [ ] `reasoning`（各候補に）
   - [ ] `confidence_level`
   - [ ] `treatment_recommendations`
   - [ ] `analysis_steps`

```json
// 確認するレスポンス構造
{
  "disease_candidates": [
    {
      "confidence_level": "85%",
      "reasoning": {
        "why_this_condition_ja": "...",
        "confidence_factors": [...]
      },
      "treatment_recommendations": {
        "supplements": [...],
        "diagnostic_tests": [...]
      }
    }
  ]
}
```

---

## 📱 テスト 6: レスポンシブデザイン

### 目的
すべてのデバイスサイズで正しくレイアウトされることを確認

### テスト手順

各デバイスサイズで `/diagnostic-chat.html` をテスト

#### デスクトップ (1920px)
- [ ] 3列レイアウト（チャット＋疾患情報＋サイドパネル）
- [ ] すべての要素が表示される
- [ ] スクロール不要で全コンテンツ見える

#### タブレット (768px)
- [ ] 2列 or 1列レイアウト
- [ ] 読みやすいテキストサイズ
- [ ] タッチフレンドリーなボタンサイズ

#### モバイル (375px)
- [ ] 1列レイアウト（垂直スタック）
- [ ] テキストが自動折り返される
- [ ] ボタンが押しやすい大きさ（最小 44x44px）

### ✅ 確認項目

- [ ] オーバーフロー（横スクロール）なし
- [ ] テキストが切れていない
- [ ] 画像が適切にスケール
- [ ] ボタンが操作可能
- [ ] アニメーションが滑らか

---

## 🔧 テスト 7: ブラウザ互換性

### テスト手順

各ブラウザで `/components-demo.html` と `/diagnostic-chat.html` をテスト

#### Chrome/Chromium
- [ ] すべての機能が動作
- [ ] アニメーションが滑らか
- [ ] コンソールエラーなし

#### Firefox
- [ ] すべての機能が動作
- [ ] CSSが正しく適用
- [ ] コンソールエラーなし

#### Safari (Mac/iOS)
- [ ] すべての機能が動作
- [ ] フォントが正しく表示
- [ ] コンソールエラーなし

#### Edge
- [ ] すべての機能が動作
- [ ] 互換性モード不要
- [ ] コンソールエラーなし

### ✅ 確認項目

- [ ] JavaScript エラーなし
- [ ] CSS 適用エラーなし
- [ ] アニメーション対応
- [ ] フォント表示正常

---

## 🎯 テスト 8: パフォーマンス

### テスト手順

1. **DevTools → Performance タブを開く**

2. **症状チェック チャット操作をレコード**
   - 症状入力
   - 送信
   - カード展開
   - タブ切り替え

3. **パフォーマンス結果を確認**

### ✅ 確認項目

#### フレームレート
- [ ] 60 FPS 以上を維持
- [ ] ジャンク（フレーム遅延）なし
- [ ] スクロールが滑らか

#### 読み込み時間
- [ ] `/components-demo.html` < 2秒
- [ ] `/diagnostic-chat.html` < 2秒
- [ ] API レスポンス < 1秒

#### メモリ使用量
- [ ] 初期: < 50MB
- [ ] 複数カード展開後: < 100MB
- [ ] メモリリークなし

### 🔍 詳細確認

```javascript
// コンソール実行
console.time('renderCards');
const renderer = new DiseaseCardRenderer('container');
renderer.renderCards(largeArray);
console.timeEnd('renderCards');

// 結果が < 500ms であること
```

---

## 📊 テスト結果レポート

### テスト実施日時

**日時:** ___年___月___日 ___:___

**実施者:** _________________

### テスト環境

| 項目 | 値 |
|------|-----|
| ブラウザ | ☐ Chrome ☐ Firefox ☐ Safari ☐ Edge |
| OS | ☐ Windows ☐ Mac ☐ Linux |
| デバイス | ☐ デスクトップ ☐ タブレット ☐ モバイル |
| ネットワーク | ☐ WiFi ☐ 有線 ☐ 4G |

### テスト結果

| テスト | 状態 | メモ |
|--------|------|------|
| 1. コンポーネントローディング | ☐ 合格 ☐ 失敗 | |
| 2. 解析進捗アニメーション | ☐ 合格 ☐ 失敗 | |
| 3. 疾患カード | ☐ 合格 ☐ 失敗 | |
| 4. ケアガイド表示 | ☐ 合格 ☐ 失敗 | |
| 5. 実装統合 | ☐ 合格 ☐ 失敗 | |
| 6. レスポンシブ | ☐ 合格 ☐ 失敗 | |
| 7. ブラウザ互換性 | ☐ 合格 ☐ 失敗 | |
| 8. パフォーマンス | ☐ 合格 ☐ 失敗 | |

### 発見された問題

#### 問題 1
- **タイトル:** _________________
- **重大度:** ☐ 低 ☐ 中 ☐ 高 ☐ 致命的
- **説明:** _________________
- **再現手順:** _________________
- **期待される動作:** _________________
- **実際の動作:** _________________

#### 問題 2
- **タイトル:** _________________
- （以下同様）

### 総合評価

**合格:** ☐

**条件付き合格:** ☐
（修正すべき項目: ________________）

**不合格:** ☐
（理由: ________________）

### コメント

_________________________________

_________________________________

---

## 📞 問題発生時のサポート

### よくある問題と解決方法

1. **"ReferenceError: AnalysisProgressTracker is not defined"**
   ```
   解決: スクリプトが読み込まれているか確認
   ハードリフレッシュ (Ctrl+Shift+R)
   ```

2. **"Container element not found"**
   ```
   解決: HTML コンテナの ID が正確か確認
   console.log(document.getElementById('container-id'));
   ```

3. **"Styling not applied"**
   ```
   解決: design-system.css が読み込まれているか確認
   link[href*="design-system"]
   ```

### デバッグ方法

```javascript
// コンソールでデバッグ
const tracker = new AnalysisProgressTracker('container');
console.log(tracker);  // オブジェクトが表示されるか確認

// メソッドが存在するか確認
console.log(typeof tracker.addStep); // 'function' であるべき

// 状態確認
console.log(tracker.getStatus());
```

---

## ✅ テスト完了チェック

すべてのテストが完了したら、以下をチェック：

- [ ] すべてのテストリストを確認
- [ ] 問題がある場合は報告
- [ ] テスト結果レポートを記入
- [ ] 承認者に報告

---

**ShowDog UI Components - テスト実行チェックリスト**

最後更新: 2026年2月17日
