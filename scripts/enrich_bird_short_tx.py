#!/usr/bin/env python3
import json
import os

JSON_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "diseases_all_species.json",
)

ENRICHMENTS: dict[str, dict[str, str]] = {}

# --- Batch 1: 総排泄腔乳頭腫, フレンチモルト, 多尿多飲, レオウイルス, アデノウイルス ---

ENRICHMENTS["bird_0024"] = {
    "treatment_ja": (
        "総排泄腔乳頭腫。パピローマウイルス関連。オウム目（特にアマゾン、コンゴウインコ）に好発。"
        "治療: "
        "  外科的切除: 電気焼灼/レーザー焼灼（CO2レーザー — 最も推奨）。"
        "  硝酸銀焼灼: 小病変に（化学的焼灼）。"
        "  凍結外科: 液体窒素。"
        "  — 再発率が高い（ウイルス潜伏感染）→ 複数回の処置が必要なことが多い。"
        "抗ウイルス薬（補助的）: "
        "  シドフォビル局所塗布（1%溶液 — 切除後に再発予防）。"
        "  インターフェロン（効果不明確）。"
        "自己免疫ワクチン: autogenous vaccine（自家ワクチン — 一部施設で試みあり）。"
        "合併症: 総排泄腔狭窄 → 排便/排尿障害。悪性転化（稀にSCC）。"
        "  内部乳頭腫: 胆管、膵管に発生 → 膵炎/胆管閉塞。"
        "予後: 管理可能だが根治困難（ウイルス潜伏）。再発は一般的。"
    ),
}

ENRICHMENTS["bird_0032"] = {
    "treatment_ja": (
        "フレンチモルト。APV（Avian Polyomavirus）感染。セキセイインコに好発。"
        "治療: 根治療法なし（ウイルス感染 — 支持療法のみ）。"
        "  栄養管理: 高栄養食。ビタミン・ミネラル補充。"
        "  保温: 適温（28-30°C）。"
        "  二次感染予防: 必要時のみ抗菌薬。"
        "  換羽促進: 栄養管理が最も重要（新しい羽毛の成長を支援）。"
        "臨床症状: 幼鳥（巣立ち期）の飛翔羽/尾羽の異常脱落 → 飛翔不能。"
        "  重症型: 多臓器障害（肝壊死、腎障害）→ 致死的。"
        "  軽症型: 羽毛異常のみ → 次の換羽で正常化することもある。"
        "予防: APVワクチン（不活化ワクチン — 海外で利用可能）。"
        "  繁殖管理: 感染鳥の隔離。巣箱の消毒。"
        "  PCRスクリーニング: 繁殖鳥のAPV検査。"
        "鑑別: PBFD（BFDVウイルス）、栄養性羽毛障害、甲状腺機能低下症。"
        "予後: 軽症型は良好（回復あり）。重症型は不良。"
    ),
}

ENRICHMENTS["bird_0033"] = {
    "treatment_ja": (
        "多尿多飲（PU/PD）。鳥では多尿（polyuria）と水様便（watery droppings）の区別が重要。"
        "原因別治療: "
        "  腎疾患: 輸液（皮下/骨髄内）。腎臓食（低蛋白）。アロプリノール（痛風合併時）。"
        "  糖尿病: インスリン療法（鳥では管理困難）。食事管理。"
        "  肝疾患: UDCA、SAMe、シリマリン。原因治療。"
        "  高Ca血症: 輸液（生食 — Ca排泄促進）。フロセミド。カルシトニン。"
        "  心因性多飲: 環境エンリッチメント。飲水制限（慎重に）。"
        "  中毒: 重金属（鉛/亜鉛）→ キレート療法（CaEDTA/DMSA）。"
        "  感染性: 細菌性/真菌性腎炎 → 適切な抗微生物薬。"
        "診断: 排泄物検査（糞便と尿/尿酸の比率）。CBC/BCP。UA。"
        "  鳥では尿と便が混合して排泄 → 尿量の正確な測定は困難。"
        "  体重あたりの飲水量測定が実用的。"
        "鑑別: 正常な多尿（果物摂取後、興奮時、産卵期）を除外。"
        "予後: 原因依存。腎疾患/肝疾患は進行性で予後不良。"
    ),
}

ENRICHMENTS["bird_0046"] = {
    "treatment_ja": (
        "レオウイルス感染。鶏/七面鳥に多い。ペットの鳥では稀だが家禽では重要。"
        "治療: 根治療法なし（ウイルス — 支持療法）。"
        "  輸液: 皮下輸液/骨髄内輸液（脱水補正）。"
        "  保温: 28-30°C。"
        "  強制給餌: 食欲低下時。"
        "  二次感染予防: 抗菌薬（エンロフロキサシン15-30 mg/kg PO q12h）。"
        "  抗真菌薬: アスペルギルス等の日和見感染予防。"
        "臨床症状: "
        "  関節炎/腱鞘炎（tenosynovitis — 鶏で最も一般的な症状）。"
        "  肝壊死、脾臓壊死。吸収不良症候群。"
        "  幼鳥での死亡率が高い。"
        "予防: ワクチン（家禽産業 — 生ワクチン+不活化ワクチン）。"
        "  消毒: レオウイルスは環境中で安定 → 徹底的な消毒。"
        "鑑別: マイコプラズマ関節炎、痛風、Staphylococcus関節炎。"
        "予後: 幼鳥は不良。成鳥は回復する場合あり。"
    ),
}

ENRICHMENTS["bird_0047"] = {
    "treatment_ja": (
        "アデノウイルス感染。家禽（鶏/七面鳥/ハト）および猛禽類に発生。"
        "治療: 根治療法なし（ウイルス — 支持療法）。"
        "  輸液: 皮下/骨髄内輸液。"
        "  保温: 28-30°C。酸素療法（呼吸困難時）。"
        "  強制給餌: 食欲低下時。"
        "  肝保護: SAMe/シリマリン（肝炎型で）。"
        "  二次感染予防: エンロフロキサシン15-30 mg/kg PO q12h。"
        "臨床症候群: "
        "  封入体肝炎（IBH — 鶏/猛禽類）: 急性肝壊死。高致死率。"
        "  鶏卵下落症候群（EDS — ガチョウ型）: 産卵率低下。"
        "  出血性腸炎（七面鳥）。"
        "  アデノウイルス性肝炎（ハト）。"
        "予防: ワクチン（家禽 — 不活化ワクチン）。"
        "  衛生管理: ケージ消毒。感染鳥の隔離。"
        "鑑別: ヘルペスウイルス肝炎、細菌性肝炎、クラミジア。"
        "予後: 幼鳥/免疫低下鳥で不良。成鳥は回復の可能性あり。"
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

    print(f"Updated {updated}/{len(ENRICHMENTS)} bird disease entries")


if __name__ == "__main__":
    apply_enrichments()
