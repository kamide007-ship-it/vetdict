#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# Amphibian Phase 2 (3件)
# ============================================================

ENRICHMENTS["amphibian_0102"] = {
    "treatment_ja": (
        "両生類の骨折。"
        "★両生類は骨が薄く脆弱で、MBD（代謝性骨疾患）による病的骨折が多い★。"
        "外傷（落下、ケージ蓋の挟み）も原因。"
        "■臨床症状: "
        "  四肢の腫脹、変形、使用回避。"
        "  病的骨折（MBD）: 下顎軟化（ラバージョー）、脊椎変形。"
        "■診断: X線（骨折、MBDの骨密度低下）。血液検査: Ca, P。"
        "■疼痛管理: "
        "  メロキシカム 0.1-0.2 mg/kg PO/ICe q24h。"
        "  ★両生類の薬物吸収は皮膚からも起こる — 投薬水に溶解して浸漬投与も可能★。"
        "  ブトルファノール 0.2-0.5 mg/kg ICe（急性疼痛）。"
        "■保存療法（小型種 — 大半の症例）: "
        "  テープスプリント or ボールバンデージ。"
        "  ★両生類の皮膚は非常にデリケート — 粘着テープの直接接触は皮膚損傷を起こす★。"
        "  → 薄いスポンジパッドで緩衝してからテープ固定。"
        "  ケージレスト 4-8週。浅い水（溺水防止）。"
        "■外科療法（大型カエル・サンショウウオ）: "
        "  髄内ピン（整形外科用ピン or 皮下注射針を代用）。"
        "  — 骨が非常に小さいため技術的に困難。"
        "■MBD是正: "
        "  UVB照射（昼行性種）。Ca補充（Caダスティング昆虫）。"
        "  ビタミンD3経口。"
        "■環境: 皮膚湿潤維持。適正温度（18-25℃、種による）。清潔な水。"
        "■予後: 単純骨折→良好。MBD+多発骨折→飼育環境改善が前提。"
        "参考文献: Wright & Whitaker (2001) Amphibian Medicine and Captive Husbandry; Divers & Stahl (2019)."
    ),
}

ENRICHMENTS["amphibian_0103"] = {
    "treatment_ja": (
        "両生類の骨折（甲羅/背甲）。"
        "★両生類には甲羅がないため、この項目は体壁損傷/外骨格損傷として扱う★。"
        "外傷（鋭利な基材、ケージ落下、同居個体間の咬傷）が原因。"
        "■臨床症状: "
        "  皮膚裂傷、出血、体腔臓器の露出（重度）。"
        "  ★両生類の皮膚は呼吸・水分調節に関与 — 損傷は全身に影響★。"
        "■初期安定化: "
        "  疼痛: メロキシカム 0.1-0.2 mg/kg ICe（背側リンパ嚢注射）。"
        "  輸液: 等張液（両生類用リンゲル or 0.6% NaCl）を浸漬 or SC。"
        "  ★両生類の体液はNaCl 0.6%（哺乳類の0.9%より低張）★。"
        "  皮膚湿潤維持（ガーゼ+生理食塩水で覆う）。"
        "■創傷管理: "
        "  洗浄: 希釈クロルヘキシジン（0.025% — 両生類は高濃度に感受性）。"
        "  小創傷: 組織接着剤（シアノアクリレート）で閉鎖。"
        "  大創傷: 吸収糸で縫合（5-0〜6-0）。"
        "  ★縫合糸は鱗がないため結紮部が皮膚を切断しやすい — マットレス縫合推奨★。"
        "■感染管理: "
        "  エンロフロキサシン 5 mg/kg ICe q24h。"
        "  水質管理: 清潔な水（Aeromonas, Pseudomonas等の水系病原体が二次感染の原因）。"
        "■環境: 清潔な湿潤環境。水浴可能だが深水禁止。適正温度維持。"
        "■予後: 小創傷→良好。体腔露出→不良。皮膚の再生能力は高い。"
        "参考文献: Wright & Whitaker (2001); Divers & Stahl (2019)."
    ),
}

ENRICHMENTS["amphibian_trauma___abrasions"] = {
    "treatment_ja": (
        "両生類の外傷/擦過傷。ケージ内の鋭利な表面、粗い基材、ハンドリング、同居個体の咬傷が原因。"
        "★両生類の皮膚は極めて薄く透過性が高い — 軽度の外傷でも全身への影響が大きい★。"
        "■臨床症状: "
        "  吻端損傷（ロストラルアブレージョン）: ケージ壁面への衝突。最多。"
        "  四肢・腹面の擦過傷。発赤、出血、潰瘍化。"
        "  重度: 二次感染（赤足病/レッドレッグ — Aeromonas hydrophila）。"
        "■創傷処置: "
        "  洗浄: 希釈クロルヘキシジン（0.025%）or 生理食塩水（0.6% NaCl）。"
        "  — ★ポビドンヨードは両生類の皮膚に毒性 → 使用回避★。"
        "  局所抗菌: シルバースルファジアジンクリーム（薄く塗布）。"
        "  小創傷: 組織接着剤（シアノアクリレート）。"
        "  ★粘着性テープ/バンデージは両生類の皮膚に直接貼付不可★。"
        "■全身感染の予防: "
        "  エンロフロキサシン 5 mg/kg ICe q24h（背側リンパ嚢注射）× 7-14日。"
        "  または薬浴: エンロフロキサシン 5 μg/mL水に6-8時間浸漬。"
        "  レッドレッグ進行時: 追加でアミカシン 2.5 mg/kg ICe q72h。"
        "■疼痛管理: メロキシカム 0.1-0.2 mg/kg ICe q24h。"
        "■環境改善（根本対策）: "
        "  吻端損傷: ケージ前面を不透明にする（ガラスへの衝突防止）。"
        "  基材: 湿潤スポンジ or ペーパータオル。砂利・鋭利な石を除去。"
        "  水質: 清潔。塩素除去。水温適正。"
        "  過密回避。"
        "■予後: 軽度擦過傷→良好（皮膚再生能力が高い）。レッドレッグ/敗血症→慎重〜不良。"
        "参考文献: Wright & Whitaker (2001); Pessier AP & Mendelson JR (2017) A Manual for Control of Infectious Diseases in Amphibian Survival Assurance Colonies."
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} amphibian entries")


if __name__ == "__main__":
    apply_enrichments()
