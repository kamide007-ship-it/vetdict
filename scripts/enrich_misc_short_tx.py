#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# Guinea Pig (1件) + Sugar Glider (1件)
# ============================================================

ENRICHMENTS["guinea_pig_bladder_sludge"] = {
    "treatment_ja": (
        "モルモットの膀胱スラッジ（膀胱砂）。炭酸カルシウム結晶の膀胱内蓄積。"
        "モルモットはCa代謝が特殊（腸管でのCa吸収が非選択的 → 高Ca食で尿中Ca排泄↑）。"
        "■臨床症状: "
        "  血尿、排尿困難（しぶり）、頻尿。"
        "  排尿時の発声（疼痛サイン）。会陰部の尿灼け。"
        "  重度: 尿道閉塞（♂に多い — 尿道が細く長い）。"
        "■診断: "
        "  X線: 膀胱内の放射線不透過性沈殿物（砂状〜スラッジ状）。"
        "  超音波: 膀胱内の高エコー沈殿物。"
        "  尿検査: 結晶（炭酸Ca）、血尿、細菌（二次UTI）。"
        "■治療: "
        "  膀胱洗浄（標準治療）: "
        "    全身麻酔下（イソフルラン/セボフルラン — ★ケタミン使用可★）。"
        "    カテーテルを尿道経由で膀胱に挿入。"
        "    温生理食塩水で繰り返し洗浄（注入→吸引）。"
        "    — ♂のカテーテル挿入は解剖学的に困難（J字型尿道）。"
        "  尿道閉塞: 緊急カテーテル挿入。不可能→膀胱穿刺（cystocentesis）。"
        "  膀胱切開（cystotomy）: 大型結石 or 洗浄不能なスラッジ。"
        "  疼痛管理: メロキシカム 0.3-0.5 mg/kg PO q24h。"
        "  UTI合併: "
        "    トリメトプリム/スルファメトキサゾール 30 mg/kg PO q12h × 14日。"
        "    または エンロフロキサシン 5-10 mg/kg PO q12h。"
        "    ★ペニシリン系/セファロスポリン系の経口投与は致死的 → 絶対禁忌★。"
        "■食事改善（再発予防の鍵）: "
        "  アルファルファヘイ → チモシーヘイに変更（Ca含量が低い）。"
        "  高Caペレットを制限（Ca 0.8%以下のペレットに）。"
        "  高Ca野菜を制限（パセリ、ケールを減量）。"
        "  ★ビタミンC: 50-100 mg/day PO（モルモットは体内合成不可 — Ca制限時も維持必須）★。"
        "  飲水増加: 新鮮な水を常時提供。給水ボトルの位置・数の確認。シリンジで補助給水。"
        "■定期モニタリング: 3-6ヶ月毎のX線で再発チェック。"
        "■予後: 食事改善＋飲水増加で管理可能。再発率が高い（生涯管理）。尿道閉塞は緊急。"
        "参考文献: Quesenberry & Carpenter (2020); Hawkins MG & Bishop CR (2012) JVIM; Harcourt-Brown (2002)."
    ),
}

ENRICHMENTS["sugar_glider_nutritional_secondary_hyperparathyroidism_nshp"] = {
    "treatment_ja": (
        "フクロモモンガの栄養性二次性上皮小体機能亢進症（NSHP/MBD）。"
        "Ca欠乏・Ca:P比の不均衡・ビタミンD3不足が原因。非常に多い疾患。"
        "■臨床症状: "
        "  後肢不全麻痺/麻痺（最も一般的な主訴）、骨折（病的）。"
        "  震え、痙攣（低Ca血症性テタニー）。食欲不振、嗜眠。"
        "  進行例: 下顎軟化、脊椎変形、寝たきり。"
        "■診断: "
        "  X線: 全身性骨密度低下、病的骨折。"
        "  血液検査: 低Ca、高P（採血量が限られるため困難なことがある）。"
        "■急性期治療（低Ca痙攣/テタニー）: "
        "  グルコン酸カルシウム10%: 10-20 mg/kg IM/SC（緩徐）。"
        "  — 心拍モニタリング（徐脈に注意）。"
        "  保温: 28-30℃。"
        "  酸素投与（呼吸困難時）。"
        "■維持療法: "
        "  カルシウム補充: グルコン酸Ca シロップ 10-20 mg/kg PO q12h × 2-4週。"
        "  ビタミンD3: 経口補充（Rep-Cal等のD3含有Caサプリメント）。"
        "  ★過剰投与は高Ca血症のリスク → 定期的な血液検査でモニタリング★。"
        "■食事改善（最重要 — 根本治療）: "
        "  推奨食: BML（Bourbon's Modified Leadbeater's）ダイエット or TPGダイエット。"
        "  — Ca:P比 1.5-2:1を維持。"
        "  問題食: 果物のみ（Ca不足/P過剰）、ミルワーム主体（高P）、ペレットのみ。"
        "  昆虫: Caダスティング済みコオロギ（週3-4回）。ミルワームは制限。"
        "  果物/野菜: Ca豊富な種類（パパイヤ、イチジク）。"
        "  ★蜂蜜/果汁の過剰はNG — 肥満＋Ca不足を助長★。"
        "■骨折管理: 小型のためスプリント困難。ケージレスト（高い場所を撤去）4-8週。"
        "■環境: 登攀物を低い位置に制限（落下骨折予防）。UVBの必要性は議論あり。"
        "■予後: 早期（後肢不全麻痺段階）→食事改善で2-4週以内に改善。"
        "  重度の骨変形/多発骨折→回復に数ヶ月。完全麻痺→回復困難。"
        "参考文献: Quesenberry & Carpenter (2020); Johnson-Delaney CA (2006) J Exotic Pet Med; Dierenfeld ES (2009)."
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} misc entries")


if __name__ == "__main__":
    apply_enrichments()
