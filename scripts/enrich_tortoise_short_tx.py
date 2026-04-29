#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# Tortoise Phase 2 (5件)
# ============================================================

# --- Batch 1: Shell Fracture, Limb Fracture, Shell/Carapace Fracture ---

ENRICHMENTS["tortoise_0004"] = {
    "treatment_ja": (
        "リクガメの甲羅骨折。犬咬傷・落下・踏みつけ・芝刈り機事故が主因。"
        "■初期安定化: "
        "  止血: 圧迫止血＋ゼラチンスポンジ。"
        "  疼痛管理: メロキシカム 0.1-0.2 mg/kg IM/PO q24-48h。"
        "  — カメの甲羅は皮骨（dermal bone）で神経が分布 → 疼痛を感じる。"
        "  ブトルファノール 0.4-1.0 mg/kg IM（急性疼痛の追加鎮痛）。"
        "  輸液: 乳酸リンゲル 10-20 mL/kg/day SC（大腿前窩）or 経口。"
        "■創傷処置: "
        "  0.05%クロルヘキシジン or 生理食塩水で洗浄。壊死組織デブリードマン。"
        "  湿潤療法維持。"
        "■甲羅修復: "
        "  骨片固定: ワイヤーサークラージュ or ケーブルタイ。"
        "  被覆: エポキシ樹脂＋ファイバーグラスパッチ。"
        "  定期的（2-4週毎）に被覆材を外して感染チェック。"
        "  完全治癒: 12-24ヶ月（甲羅の成長・再構築は非常に遅い）。"
        "■感染管理: "
        "  セフタジジム 20 mg/kg IM q72h（爬虫類の第一選択）。"
        "  嫌気性菌: メトロニダゾール 20 mg/kg PO q48h。"
        "■体腔露出: 緊急手術。腹腔洗浄。臓器損傷の評価。"
        "■環境: POTZ維持（25-32℃、種による）。UVB照射。清潔な基材（ペーパータオル）。"
        "■予後: 表層骨折→良好。体腔露出→慎重。脊椎損傷合併→不良。"
        "参考文献: McArthur et al. (2004) Medicine and Surgery of Tortoises and Turtles; Divers & Stahl (2019)."
    ),
}

ENRICHMENTS["tortoise_0094"] = {
    "treatment_ja": (
        "リクガメの四肢骨折。外傷（犬咬傷・落下）またはMBD（代謝性骨疾患）による病的骨折。"
        "■初期評価: "
        "  X線: 骨折型、MBDの有無（骨密度低下・皮質菲薄化）。"
        "  血液検査: Ca, P, ALP（MBDスクリーニング）。"
        "■疼痛管理: "
        "  メロキシカム 0.1-0.2 mg/kg PO/IM q24-48h。"
        "  トラマドール 5-10 mg/kg PO q48-72h（追加鎮痛）。"
        "  — 腎門脈系があるため後肢からの薬物投与は避ける。"
        "■保存療法（単純・安定骨折、小型種）: "
        "  テープスプリント or パッド付きバンデージ。6-12週固定。"
        "  ケージレスト。甲羅に脚を引き込む動作を制限（必要に応じ発泡材で制限）。"
        "■外科療法（不安定骨折、大型種）: "
        "  髄内ピン＋サークラージュワイヤー。創外固定器。"
        "  — 爬虫類の骨治癒は哺乳類の2-3倍遅い → 固定期間は6-12週以上。"
        "■MBDの是正（根本原因の場合）: "
        "  UVB照射: 10-12%ランプ、30-45cm距離、10-12h/日。6ヶ月毎交換。"
        "  Ca補充: 炭酸Ca粉末を食事に添加。Ca:P比2:1以上。"
        "  食事: コマツナ、チンゲン菜、タンポポ葉（高Ca葉野菜）。"
        "■感染予防（開放骨折）: セフタジジム 20 mg/kg IM q72h。"
        "■予後: 単純骨折＋MBD是正→良好。粉砕/MBD重度→截肢も選択肢（リクガメは3肢で歩行可能）。"
        "参考文献: Divers & Stahl (2019); McArthur et al. (2004); Mitchell & Tully (2016)."
    ),
}

ENRICHMENTS["tortoise_0095"] = {
    "treatment_ja": (
        "リクガメの甲羅/背甲骨折。犬咬傷・落下・交通事故が原因。"
        "背甲は骨性構造（皮骨＋肋骨癒合）で肺が直下にあり損傷リスクが高い。"
        "■初期安定化: "
        "  止血。体腔露出の有無を評価。"
        "  疼痛: メロキシカム 0.1-0.2 mg/kg IM q24-48h。"
        "  輸液: 乳酸リンゲル 10-20 mL/kg/day SC。"
        "  POTZ維持。"
        "■呼吸評価: "
        "  背甲損傷→肺損傷の可能性。X線で気胸/肺挫傷の評価。"
        "  呼吸促迫時: 酸素投与。"
        "■創傷処置: "
        "  洗浄: 0.05%クロルヘキシジン or 生理食塩水。"
        "  壊死組織デブリードマン。"
        "  ウジ虫症（myiasis）の確認・除去（屋外飼育個体）。"
        "■甲羅修復: "
        "  小欠損: 洗浄→湿潤療法→二次治癒（甲羅の自然再生）。"
        "  大欠損: ワイヤーサークラージュ＋エポキシ/ファイバーグラスブリッジ。"
        "  ★修復材下に膿瘍が形成されやすい → 定期チェック必須★。"
        "  完全修復: 12-24ヶ月。甲板は再生するが外観は不完全。"
        "■感染管理: "
        "  セフタジジム 20 mg/kg IM q72h。"
        "  メトロニダゾール 20 mg/kg PO q48h（嫌気性菌）。"
        "■環境: ペーパータオル基材（土砂禁忌 — 創傷汚染）。温浴q24-48h（清潔＋水分補給）。"
        "■予後: 表層→良好（数ヶ月-1年で修復）。肺損傷/体腔露出→慎重。"
        "参考文献: McArthur et al. (2004); Divers & Stahl (2019); Mader (2006)."
    ),
}

# --- Batch 2: Spinal Trauma, Intestinal Volvulus ---

ENRICHMENTS["tortoise_spinal_trauma___vertebral_fracture"] = {
    "treatment_ja": (
        "リクガメの脊椎外傷/椎骨骨折。犬咬傷・落下・圧迫事故が主因。"
        "甲羅が脊椎を保護するが、高所落下では衝撃が伝わる。"
        "■神経学的評価: "
        "  後肢反射（引込み反射）、総排泄腔反射、尾の筋緊張。"
        "  深部痛覚の有無が予後の最重要因子。"
        "  X線: 椎骨の骨折・脱臼・転位。CT/MRIが理想的。"
        "■急性期治療: "
        "  安静: 甲羅内に四肢を引き込めないよう発泡材で制限（評価のため）。"
        "  疼痛: メロキシカム 0.1-0.2 mg/kg IM q24-48h。"
        "  脊髄浮腫: デキサメタゾン 0.5-1.0 mg/kg IM（受傷後8時間以内）。"
        "  輸液: 乳酸リンゲル SC。"
        "■保存療法: "
        "  安定骨折/不完全麻痺: ケージレスト 8-12週。"
        "  膀胱管理: 排尿不能例は温浴＋用手圧迫。カテーテル留置は困難。"
        "■外科療法: "
        "  不安定骨折: 背甲の一部を除去して脊椎にアクセス（困難な手術）。"
        "  除圧＋椎体固定（ピン/PMMA）。"
        "  — リクガメの脊椎手術は高度専門施設でのみ実施可能。"
        "■リハビリ: 温浴（浮力利用）。緩やかな歩行促進。"
        "■後肢麻痺の長期管理: "
        "  車輪付き台車（カートタイプ）の装着例あり。"
        "  褥瘡予防: 柔らかい基材。定期的な体位変換。"
        "  排泄管理: 温浴で排泄促進。"
        "■予後: 深部痛覚あり→回復可能（数ヶ月）。深部痛覚なし→歩行回復困難（QOL管理へ移行）。"
        "参考文献: Divers & Stahl (2019); McArthur et al. (2004)."
    ),
}

ENRICHMENTS["tortoise_intestinal_volvulus"] = {
    "treatment_ja": (
        "リクガメの腸捻転。異物摂取・寄生虫・腫瘍・術後癒着が原因。稀だが致死的。"
        "■臨床症状: "
        "  急性食欲廃絶、排便停止、腹部膨満（甲羅の後方から軟部組織が膨隆）。"
        "  嗜眠、頭部を甲羅内に引き込む（疼痛サイン）。"
        "■診断: "
        "  X線: 腸管拡張、gas pattern異常。"
        "  超音波: 腸管壁肥厚、腹水。"
        "  造影X線: 通過遅延/停止。"
        "■初期安定化: "
        "  輸液: 乳酸リンゲル 20-25 mL/kg/day SC/ICe。"
        "  POTZ維持（免疫・代謝機能の最適化）。"
        "  疼痛: メロキシカム 0.1-0.2 mg/kg IM。ブトルファノール 0.4 mg/kg IM。"
        "  抗菌薬: セフタジジム 20 mg/kg IM + メトロニダゾール 20 mg/kg PO。"
        "■外科療法: "
        "  腹甲板切除（plastronotomy）でアクセス → 腸管の整復。"
        "  — リクガメでは腹甲を骨切りして体腔にアクセスする必要がある。"
        "  壊死腸管: 切除＋吻合（4-0〜5-0 PDS単層結節縫合）。"
        "  腹甲修復: ワイヤー＋エポキシ。治癒に数ヶ月。"
        "■術後管理: "
        "  絶食48-72h → 少量の葉野菜から再開。"
        "  輸液継続。POTZ維持。"
        "  温浴q24h（水分補給＋排泄促進）。"
        "■予後: 早期手術＋壊死なし→慎重〜良好。広範囲壊死/腹膜炎→不良。"
        "参考文献: McArthur et al. (2004); Divers & Stahl (2019); Mader (2006)."
    ),
}


def apply_enrichments() -> None:
    with open(JSON_PATH, encoding="utf-8") as f:
        data = json.load(f)

    updated = 0
    for entry in data:
        eid = entry.get("id")
        if eid in ENRICHMENTS:
            patch = ENRICHMENTS[eid]
            for k, v in patch.items():
                entry[k] = v
            updated += 1

    missing = set(ENRICHMENTS) - {e.get("id") for e in data}
    if missing:
        print(f"WARNING: {len(missing)} IDs in ENRICHMENTS not found in JSON:")
        for m in sorted(missing):
            print(f"  {m}")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Updated {updated}/{len(ENRICHMENTS)} tortoise entries")


if __name__ == "__main__":
    apply_enrichments()
