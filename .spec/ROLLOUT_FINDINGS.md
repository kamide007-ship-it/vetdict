# 全21種 検出器 横展開レポート（read-only / フェーズ1完了）

実行: `python3 scripts/quality/rollout.py`
集計: `reports/quality/_rollout_summary.md` / 種別詳細: `reports/quality/<species>/detectors.{json,md}`

## 全体像（7,094疾患）
| 指標 | 合計 | 意味 |
|---|--:|---|
| 完全一致重複クラスタ | **546**（冗長 644件） | 論理統合(T103)の一次対象 |
| 疾患ファミリー候補 | 21種分（例: dog 119, horse 123, bird 97） | **統合候補ではなくレビュー対象**（骨折/肺炎/腫瘍の部位別は別疾患） |
| 非臨床エントリ | **4**（degu 3 + horse 1） | 研究モデル/ヒト医学移植。T103で archived 候補 |
| 投与量なし治療 | **954** | 治療ドラフト(T105)の一次対象 |
| 種不整合の薬品リンク | **2,139** | request-time マッチャに種ガードが無い（T108＝systemic bug 確認） |
| 犬猫論文の他種紐付け | **309** | `get_references_for_disease` に種ガード無し（出典v2=T110の対象） |
| 機械翻訳臭 | **39**（degu 17, guinea_pig 6, horse 5） | 置換辞書(T109)。egregious は degu に集中 |

## 失敗ガード（SPEC「10倍超で停止」）
読み取り専用のため停止せず surfacing のみ。超過2件:
- amphibian: drug_mismatch=220 / exotic_other: drug_mismatch=216（>200 ヒューリスティック上限）
- いずれも**データ異常ではなく systemic な薬品マッチャ・バグの反映**（薬品DBが犬猫中心 → 外来種の治療文中の薬品に種別用量が無い）。T108 の修正（`api/vetdict_api.py:1148` / `api/pubmed_references.py:333` に種ガード追加）で解消見込み。

## 根本原因（T108 調査で特定・request-time 実装）
| バグ | 位置 | 種ガード | 影響 |
|---|---|---|---|
| 関連薬品の substring 自動マッチ | `api/vetdict_api.py:1148-1162`（+ `_attach_mentioned_drugs` 2321-2369） | **無し** | エキゾ疾患に犬猫薬（例: degu にシプロフロキサシン/グリピジド）が付く |
| 参考文献の bidirectional substring | `api/pubmed_references.py:333-339` | **無し** | エキゾ疾患名が犬猫キーに一致 → 犬猫論文が付く（degu 糖尿病→犬猫 J Vet 論文） |

## 検出器カバレッジの注意
- **馬（equine）は独自スキーマ**（`name_en`/`treatment_protocol`/`etiology`）。`detect.py` に `_EQUINE_FIELD_MAP` アダプタを追加済み → 馬も正しく解析（当初 621件「空治療」の誤検出を解消）。
- T101 ファミリー候補は per-stem 非推移グルーピング。**統合可否は必ず獣医師レビュー**。
- T108 の drug_mismatch は「種別用量データが無い薬品リンク」を機械的に列挙したもの。一部は臨床的に妥当な外挿の可能性があるため、修正は「種ガード追加」＝マッチ自体の抑制で対応し、個別是正は不要。

## 次アクション（承認待ち）
1. フェーズ2（🟡）: `schema_migrations` + 不変ID付与（統合の前提）
2. T103（🔴）: degu 1種の統合バッチを**提示のみ**作成 → Kentaro 承認
3. T108修正（🟡→コード）: 2マッチャに種ガード追加（データ非改変・可逆）
