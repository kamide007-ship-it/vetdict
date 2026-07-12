# 検出器の「生ソース」ビュー vs「配信」ビュー（read-only）

品質検出器（`scripts/quality/detect.py` / `rollout.py`）は 2 つのビューでレポートを出せる。
どちらも **完全に読み取り専用**（疾患データを一切改変しない）。

| ビュー | 生成コマンド | 出力 | 意味 |
|---|---|---|---|
| **raw（生ソース）** | `python3 scripts/quality/rollout.py` | `reports/quality/_rollout_summary.md` | Python モジュール＋JSON オーバーレイの**元データ**。統合前＝問題の**元規模**。基準線。 |
| **served（配信）** | `python3 scripts/quality/rollout.py --served` | `reports/quality/_rollout_summary_served.md` | 上に本番の **dedup + canonical map（T103）** を適用した、**サイトが実際に配信する状態**。統合の**実効果＝残作業**。 |

単一種は `python3 scripts/quality/detect.py degu [--served]`
（→ `reports/quality/degu/detectors[_served].{json,md}`）。

## なぜ 2 ビューか
検出器はこれまで生ソースだけを読んでいたため、T103 の論理統合（degu/rabbit/cat/horse
＋16種の auto-canonical）を適用しても `_rollout_summary.md` の数字は変わらず、**進捗が見えなかった**。
served ビューは serve-time の実関数（`api.species.helpers.dedupe_disease_list` +
`api.species.canonical.apply_canonical_map`）を**そのまま再利用**するので、数字はサイトの配信内容と一致する。

## served ビューが示す統合の実効果（2026-07 時点）
| 指標 | raw | served | 差 |
|---|--:|--:|--:|
| 総疾患 | 7,094 | **6,836** | −258（論理統合で非表示化） |
| 完全重複クラスタ | 545 | **338** | −207 |
| ├ horse | 23 | 2 | curated 統合21 |
| ├ rabbit | 42 | 13 | 統合31 |
| ├ dog | 35 | 23 | auto dedup |
| └ degu | 17 | 8 | 統合＋アーカイブ |
| 非臨床エントリ | 4 | **1** | degu ヒト医学移植3件を archived（horse 1件が残） |

## 注意
- **物理削除ゼロ**: served ビューで「消える」エントリは canonical サイドカーで hide/merge/archive
  されているだけ。旧 URL は 301 リダイレクト。サイドカーを消せば raw に戻る。
- **T108（薬品誤リンク・論文誤紐付け）** は served/raw でほぼ不変。これは request-time マッチャの
  systemic バグで、出荷済みの種ガードで残存 0（本番で非表示）。served の数字は「未ガード時の規模」。
- served ビューはフルの `api.*` インポートを要する（T108 は `flask`＋`DRUGS`）。CI/開発環境で実行のこと。
- 生ベースライン（`_rollout_summary.md`）は温存。served は別ファイルなので両方を並べて追える。
