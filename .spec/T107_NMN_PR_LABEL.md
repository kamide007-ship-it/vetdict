# T107 — NMN/ECVN ブロックを「自社製品・PR」として分離

Branch: `claude/vibrant-newton-np00um`

## 目的
自社（Equine & Canine Vet Nutrition, caninevet.jp）の栄養補助製品ブロックを**残置**しつつ、
**エビデンスに基づく標準治療と誤認されない**よう「自社製品・PR（広告）」として明確に分離。

## 実装（残置・可逆）
- **データヘッダー**（`api/data/sponsor_adjuncts.py`）: ブロック見出しを
  `【PR・自社製品｜標準治療ではありません — …(caninevet.jp)】` に変更（英語版も同様）。
  ブロックは実行時注入（JSONに焼き込まれていない）ため即時反映。
- **SPA**（`static/js/app.js` `renderTreatmentWithAdjunct`）:
  - データ見出し行を除去し、UI 側で **「PR」バッジ + 「PR・自社製品」ラベル + ベンダーリンク**、
    および**免責文**「以下は自社製品の紹介（広告）です。標準治療・エビデンスに基づく治療ではありません。」を表示。
  - `role="complementary"` / `aria-label="自社製品の広告（PR）"`。日英対応。
- **サーバー描画**（`api/vetdict_api.py` `_render_treatment_adjunct_html` + `disease_detail.html`）:
  - SEO 疾患詳細ページでも同じ PR ブロックを描画。`[ECVN:Block]` マーカーがユーザーに漏れない。
  - `markupsafe` でエスケープ、治療本文と分離。
- **CSS**（`static/css/main.css`）: 緑（エビデンス治療）とは別系統の**アンバー（広告）配色**の
  `.ecvn-adjunct-block` / `.ecvn-adjunct-label` / `.ecvn-pr-badge` / `.ecvn-adjunct-disclaimer`。
- **ServiceWorker**: `CACHE_NAME` v87 → **v88**。

## テスト
- `tests/test_ecvn_pr_label.py` 4件: データヘッダーPR化、サーバー描画でマーカー非漏洩＋PRバッジ＋免責＋治療本文保持＋ベンダーリンク、エスケープ、非ECVN治療にPRブロック無し。
- SEO/API/diagnostic 回帰 402件 pass。ruff 通過。

## 効果
- 製品ブロックは**残す**が、視覚（アンバー広告配色）・ラベル（PRバッジ）・免責文・ARIA で
  標準治療から**明確に分離**。誤読（＝標準治療と誤認）を防止。
