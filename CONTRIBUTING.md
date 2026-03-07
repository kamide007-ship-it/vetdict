# Contributing to ShowDog / コントリビューションガイド

ShowDog Analysis Platform へのコントリビューションに感謝します。

## 開発環境セットアップ

### Prerequisites
- Python 3.11+
- Node.js 18+ (optional, for frontend tooling)
- Git

### ローカル開発

```bash
# リポジトリのクローン
git clone https://github.com/kamide007-ship-it/showdog-app.git
cd showdog-app

# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 依存関係のインストール
pip install -r requirements.txt

# 環境変数の設定
cp .env.example .env
# .env を編集して必要なAPIキーを設定

# 開発サーバーの起動
python app.py
```

## ブランチ戦略

- `main` — 本番環境。直接プッシュ禁止
- `claude/*` — 機能開発ブランチ（CI/CD 自動マージ対応）
- `feature/*` — 手動機能開発ブランチ
- `fix/*` — バグ修正ブランチ

## コーディング規約

### Python
- **Linter**: Ruff (`ruff check .`)
- **Line length**: 120文字
- **Import order**: isort 準拠（ruff 自動整理）
- **Docstrings**: Google style
- **Type hints**: 推奨（必須ではない）

### Frontend (HTML/CSS/JS)
- **CSS**: BEM-like naming with `sd-` prefix (ShowDog Design System)
- **JavaScript**: Vanilla JS, no framework dependencies
- **i18n**: All user-facing text must use `data-i18n` attributes
- **Accessibility**: WCAG 2.2 AA compliance required

## テスト

```bash
# テストの実行
pytest tests/ -v

# 特定のテストファイル
pytest tests/test_engine.py -v
```

## プルリクエスト

1. 機能ブランチを作成: `git checkout -b feature/your-feature`
2. 変更をコミット: `git commit -m "Feat: describe your change"`
3. プッシュ: `git push -u origin feature/your-feature`
4. GitHub で PR を作成

### コミットメッセージ規約

```
<type>: <description>

Types:
  Feat:     新機能
  Fix:      バグ修正
  Refactor: リファクタリング
  Docs:     ドキュメント
  Test:     テスト
  Chore:    その他
```

### PR チェックリスト

- [ ] テストが通ること (`pytest tests/ -v`)
- [ ] Ruff でリントエラーがないこと (`ruff check .`)
- [ ] 新機能に対するテストを追加
- [ ] i18n 対応（日本語 + 英語）
- [ ] アクセシビリティ確認
- [ ] モバイル対応確認

## アルゴリズム変更ポリシー

スコアリングアルゴリズムの重み・軸・公式への変更は **厳格なガバナンスプロセス** に従います。
詳細は [docs/Model_Governance.md](docs/Model_Governance.md) を参照してください。

## セキュリティ

セキュリティの脆弱性を発見した場合は、public issue ではなく直接連絡してください。

## ライセンス

コントリビューションは本プロジェクトのライセンスに準じます。
