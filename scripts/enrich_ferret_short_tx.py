#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# ============================================================
# Ferret Phase 2 (5件)
# ============================================================

# --- Batch 1: Canine Distemper, Aplastic Anemia, Gastric Foreign Body ---

ENRICHMENTS["ferret_0004"] = {
    "treatment_ja": (
        "フェレットの犬ジステンパーウイルス（CDV）感染。致死率ほぼ100%。"
        "■臨床症状: "
        "  初期: 発熱（40-41℃）、漿液性鼻汁・眼脂、食欲不振。"
        "  中期: 顎下・鼠径部の皮疹（丘疹→痂皮）、足底の角化亢進（ハードパッド）。"
        "  末期: 神経症状（振戦、痙攣、後肢不全麻痺）→死亡。"
        "■診断: 結膜スワブPCR。蛍光抗体法（FA）。血清CDV IgM抗体。"
        "■治療: "
        "  特異的抗ウイルス薬なし。"
        "  支持療法: 輸液（乳酸リンゲル SC/IV）、強制給餌、保温。"
        "  二次細菌感染: アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h。"
        "  痙攣: ジアゼパム 0.5-1.0 mg/kg IV/IM PRN。"
        "  ★安楽死が一般的に推奨される — 回復例は極めて稀★。"
        "■予防（最重要）: "
        "  フェレット用犬ジステンパーワクチン: Purevax Ferret Distemper（Merial）。"
        "  — 不活化カナリア痘ベクターワクチン（フェレットに安全）。"
        "  ★改変生犬用多価ワクチン（犬用DHPPi等）はフェレットで致死的 → 絶対禁忌★。"
        "  接種スケジュール: 8週齢、11週齢、14週齢（3回接種）→以後年1回ブースター。"
        "  接種後30分は院内観察（アナフィラキシーリスク — ジフェンヒドラミン2 mg/kg IM準備）。"
        "■予後: 極めて不良。神経症状出現後は致死的。"
        "参考文献: Quesenberry & Carpenter (2020) Ferrets, Rabbits, and Rodents 4th ed; Johnson-Delaney CA (2017)."
    ),
}

ENRICHMENTS["ferret_0010"] = {
    "treatment_ja": (
        "フェレットのエストロゲン中毒/再生不良性貧血。未避妊雌の持続発情（4週以上）で発症。"
        "エストロゲンが骨髄を抑制 → 汎血球減少（貧血＋血小板減少＋白血球減少）。"
        "■臨床症状: "
        "  外陰部腫大の持続、脱毛、粘膜蒼白、点状出血、メレナ。"
        "  重症: 出血傾向、敗血症、後肢不全麻痺。"
        "■診断: CBC（PCV低下、汎血球減少）。血清エストラジオール上昇。骨髄生検（低形成）。"
        "■緊急安定化: "
        "  輸血（PCV<15%）: ドナーフェレットから全血 6-12 mL/kg IV（緩徐）。"
        "  輸液: 乳酸リンゲル SC/IV。"
        "  広域抗菌薬（好中球減少に伴う敗血症予防）: "
        "    エンロフロキサシン 5 mg/kg PO/SC q12h + アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h。"
        "■骨髄刺激: "
        "  エリスロポエチン（EPO）: 50-150 IU/kg SC q48h（赤血球回復促進）。"
        "  — 抗EPO抗体形成に注意（長期使用）。"
        "  デルベポエチンアルファ: 0.6 μg/kg SC q7d（抗体形成リスクが低い）。"
        "■根本治療: "
        "  卵巣子宮摘出術（OHE）: 全身状態安定後に実施。"
        "  — PCV<15%では手術リスクが極めて高い → 輸血で安定化を先行。"
        "  応急処置: hCG 100 IU IM（排卵誘発で一時的にエストロゲン低下）。"
        "  GnRHアゴニスト: デスロレリン 4.7 mgインプラント（長期的発情抑制）。"
        "■予防: 早期避妊手術（6-8ヶ月齢）or デスロレリンインプラント。"
        "■予後: PCV>25%で手術→良好。PCV<15%→慎重〜不良（骨髄回復に数週-数ヶ月）。"
        "参考文献: Quesenberry & Carpenter (2020); Rosenthal KL (2004) JVIM; Swiderski JK et al. (2008)."
    ),
}

ENRICHMENTS["ferret_0011"] = {
    "treatment_ja": (
        "フェレットの胃内異物。ゴム、スポンジ、布、発泡素材、耳栓が好発。"
        "特に1歳未満の幼若フェレットに多い（探索的咀嚼行動）。"
        "■臨床症状: "
        "  急性: 嘔吐/吐出、ブラキシズム（歯ぎしり = 疼痛サイン）、よだれ。"
        "  亜急性: 食欲不振、体重減少、間欠的嘔吐。"
        "  完全閉塞: 急激な元気消失、脱水、ショック。"
        "■診断: "
        "  X線: 金属/石はX線不透過。ゴム/布は描出困難 → バリウム造影。"
        "  超音波: 異物のエコー＋音響陰影。"
        "■初期安定化: "
        "  輸液: 乳酸リンゲル SC/IV（脱水・電解質補正）。"
        "  疼痛管理: ブプレノルフィン 0.01-0.03 mg/kg SC q8-12h。"
        "  制吐: マロピタント 1 mg/kg SC q24h。"
        "■外科的除去（標準治療）: "
        "  胃切開術（gastrotomy）: 胃内の異物。"
        "  腸切開術（enterotomy）: 腸管に移動した異物。"
        "  腸切除＋吻合: 腸管壊死時。"
        "  ★催吐はフェレットでは不確実 — 外科的除去が推奨★。"
        "■術後管理: "
        "  絶食12-24時間 → Duck Soup等の流動食から開始 → 少量頻回給餌。"
        "  メロキシカム 0.2 mg/kg PO q24h × 3-5日（疼痛管理）。"
        "  抗菌薬: アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h × 5-7日。"
        "  異物の再摂取予防: 環境整備（ゴム製品、布の除去）。"
        "■予後: 早期手術→良好。腸管壊死/穿孔→慎重。"
        "参考文献: Quesenberry & Carpenter (2020); Johnson-Delaney CA (2017)."
    ),
}

# --- Batch 2: Intestinal Foreign Body, GI Foreign Body ---

ENRICHMENTS["ferret_0012"] = {
    "treatment_ja": (
        "フェレットの腸管異物。ゴム、スポンジ、布が好発。幼若フェレットに多い。"
        "■臨床症状: "
        "  部分閉塞: 間欠的食欲不振、下痢（粘液便/タール便）、体重減少。"
        "  完全閉塞: 急性嘔吐、元気消失、腹部疼痛（ブラキシズム）、脱水。"
        "  慢性例: 緩やかな削痩、間欠的な消化器症状。"
        "■診断: "
        "  X線: gas pattern異常、腸管拡張（閉塞より口側）。"
        "  バリウム造影: 通過遅延（正常2-3時間で大腸到達）。"
        "  超音波: 異物エコー、腸管壁肥厚。"
        "■初期安定化: "
        "  輸液: 乳酸リンゲル 10 mL/kg/hr IV（ショック時）→維持。"
        "  疼痛: ブプレノルフィン 0.01-0.03 mg/kg SC q8-12h。"
        "  制吐: マロピタント 1 mg/kg SC q24h。"
        "  低血糖（フェレットはインスリノーマ併発多い）: 血糖モニタリング。"
        "■外科治療: "
        "  探索的開腹術: 全消化管を触診（複数箇所の異物を見逃さない）。"
        "  腸切開術（enterotomy）: 異物の直近口側で切開。"
        "  腸切除吻合: 壊死・穿孔部位。4-0〜5-0 PDS単層結節縫合。"
        "  ★フェレットの腸管は薄く脆弱 — 丁寧な操作が必須★。"
        "■術後管理: "
        "  絶食12-24h → Duck Soup/a/d Diet少量頻回。"
        "  メロキシカム 0.2 mg/kg PO q24h × 3-5日。"
        "  アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h × 7日。"
        "  環境整備: ゴム製品、布、スポンジを生活環境から除去。"
        "■予後: 単純除去→良好。壊死/穿孔/腹膜炎→慎重〜不良。"
        "参考文献: Quesenberry & Carpenter (2020); Hoefer HL (1997) Vet Clin North Am Exot Anim Pract."
    ),
}

ENRICHMENTS["ferret_gi_foreign_body"] = {
    "treatment_ja": (
        "フェレットの消化管異物（胃〜腸管）。好発異物: ゴム（耳栓、靴底）、スポンジ、布、発泡ゴム。"
        "1歳未満に多いが、トリコベゾアール（毛球）は全年齢で発生。"
        "■臨床症状: "
        "  嘔吐/吐出、ブラキシズム（疼痛）、よだれ、食欲不振。"
        "  便の変化: 粘液便、細い便、タール便、排便停止。"
        "  前足で口を掻く動作（嘔気サイン）。"
        "■診断: "
        "  X線 + バリウム造影（フェレットの正常通過時間: 胃→大腸 2-3時間）。"
        "  超音波: 閉塞部位特定。"
        "■治療: "
        "  初期安定化: 輸液 + 電解質補正 + 疼痛管理（ブプレノルフィン 0.01-0.03 mg/kg SC q8-12h）。"
        "  血糖チェック: フェレットはインスリノーマ併発が多い → 低血糖に注意。"
        "  ★催吐はフェレットでは信頼性が低い → 外科的除去が標準★。"
        "  胃切開/腸切開術: 全身麻酔下。"
        "  壊死腸管: 切除＋吻合。"
        "■術後: "
        "  絶食12-24h。Duck Soup/a/d Diet少量頻回。"
        "  メロキシカム 0.2 mg/kg PO q24h（3-5日）。"
        "  抗菌薬: アモキシシリン/クラブラン酸 12.5-25 mg/kg PO q12h（5-7日）。"
        "  GI保護: ファモチジン 0.25-0.5 mg/kg PO q12h or スクラルファート 25-50 mg/kg PO q8h。"
        "■予防: 環境のフェレットプルーフ（ゴム製品除去）。換毛期のグルーミング。"
        "■予後: 早期→良好。穿孔/腹膜炎→不良。"
        "参考文献: Quesenberry & Carpenter (2020); Johnson-Delaney (2017)."
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} ferret entries")


if __name__ == "__main__":
    apply_enrichments()
