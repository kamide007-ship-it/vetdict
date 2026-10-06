"""2026-10 第63弾: 寄生虫「駆虫薬テンプレート」・小型哺乳類アレルギー床材テンプレートの是正.

配信監査で、英語 treatment は個別キュレート済みなのに日本語 treatment_ja だけが
汎用テンプレートのままの臨床的に重要なエントリを検出した:

- 「…同定された寄生虫に応じた適切な駆虫薬が必要である…」
  → 犬フィラリア症（AHS 3回メラルソミン法が要点なのに記載なし）、マダニ麻痺
  （治療の本体はダニ除去と呼吸管理で駆虫薬ではない）、ウマバエ幼虫症（幼虫を
  潰すとアナフィラキシー — イベルメクチン非推奨）、猫好酸球性肺炎（非寄生虫性の
  免疫疾患を含む）、ヤドカリ貝殻放棄症候群（飼育環境ストレス — 寄生虫ではない）等
- 「…床材（杉材は禁忌、紙系/ペレット系へ）、ケージ素材…」
  → 犬・猫・フェレットのノミアレルギー性皮膚炎に小型哺乳類の床材指導が混入

JA は既存のキュレート済み英語 treatment の忠実な日本語版（新規の医学的主張なし）。
フェレット大静脈症候群とヤドカリ貝殻放棄症候群は英語側も汎用文だったため日英とも
教科書準拠で記述する。

Usage:
    python3 scripts/template_elimination/fix_parasite_fad_treatment_ja.py --apply
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"

TEMPLATE_MARKS = (
    "同定された寄生虫に応じた適切な駆虫薬",
    "杉材は禁忌",
    "正確な臨床評価（病歴、身体検査、CBC・生化学、画像）から治療方針を決定",
)

# (species, name) -> {"treatment_ja": ..., optional "treatment": ...}
CURATED: dict[tuple[str, str], dict[str, str]] = {
    ("Dog", "Heartworm Disease"): {
        "treatment_ja": (
            "成虫駆除: メラルソミン（イミトサイド）2.5 mg/kg 腰部筋肉内深部注射 — 3回投与法（AHS推奨）: "
            "1回目 → 1ヶ月休止 → 2・3回目を24時間間隔で投与。前処置: ドキシサイクリン 10 mg/kg PO q12h を4週間"
            "（共生菌ボルバキアの除去）＋大環状ラクトン系予防薬を開始（未成熟虫の除去と新規感染防止）。"
            "プレドニゾン 0.5 mg/kg PO q12h から4週間かけて漸減（死滅虫体による肺血栓塞栓症の炎症軽減）。"
            "運動制限は最重要（駆除後6-8週間は厳格に安静 — 肺血栓塞栓症の主要予防策）。"
            "予防: イベルメクチン 6 μg/kg PO 月1回（またはミルベマイシン・モキシデクチン製剤）。"
            "重症（大静脈症候群）: 頸静脈からの外科的虫体摘出が唯一の救命手段。"
            "（American Heartworm Society ガイドライン 2024）"
        ),
    },
    ("Dog", "Tick Paralysis"): {
        "treatment_ja": (
            "治療の本体はマダニの除去（駆虫薬ではない）— 除去後通常24時間以内に回復が始まる。"
            "耳介・趾間・腋窩を含め全身を徹底的に検索し、追加のマダニを取り残さない。"
            "支持療法: 酸素補給、静脈輸液。呼吸不全では人工呼吸管理。"
            "モニタリング: 呼吸機能（ダニ除去後最初の24時間が最も危険 — 除去後も一時的に悪化しうる）。"
            "誤嚥の防止（巨大食道・喉頭機能低下を伴うことがある）。"
            "再発予防: イソキサゾリン系製剤による継続的なマダニ予防。"
            "（Ettinger 8th ed; Atwell 2001 Aust Vet J）"
        ),
    },
    ("Dog", "Cuterebra Infestation"): {
        "treatment_ja": (
            "幼虫の除去: 呼吸孔を拡大し、止血鉗子で幼虫を無傷のまま摘出する"
            "（**潰さない — 虫体破裂によるアナフィラキシーのリスク**）。"
            "創部を生理食塩水または希釈クロルヘキシジンで洗浄し、必要に応じデブリードメント。"
            "抗菌薬: アモキシシリン・クラブラン酸 12.5-25 mg/kg PO q12h × 7-10日。疼痛にNSAIDs。"
            "迷入幼虫移行（中枢神経・呼吸器）: コルチコステロイド（デキサメタゾン 0.1 mg/kg IV）＋支持療法。"
            "イベルメクチンは推奨しない（組織内で幼虫が死滅するとアナフィラキシー様反応の恐れ）。"
            "（Greene, Infectious Diseases of the Dog and Cat 4th ed）"
        ),
    },
    ("Cat", "Cuterebra Infestation"): {
        "treatment_ja": (
            "幼虫の除去: 呼吸孔を拡大し、止血鉗子で幼虫を無傷のまま摘出する"
            "（**潰さない — 虫体破裂によるアナフィラキシーのリスク**）。"
            "創部を生理食塩水または希釈クロルヘキシジンで洗浄し、必要に応じデブリードメント。"
            "抗菌薬: アモキシシリン・クラブラン酸 12.5-25 mg/kg PO q12h × 7-10日。疼痛管理にNSAIDs（猫は用量・期間に注意）。"
            "迷入幼虫移行（中枢神経 — 猫の脳ウマバエ幼虫症）: コルチコステロイド（デキサメタゾン 0.1 mg/kg IV）＋支持療法。"
            "イベルメクチンは推奨しない（組織内での幼虫死滅による反応の恐れ）。"
            "（Glass 1998 JAVMA; Greene 4th ed）"
        ),
    },
    ("Cat", "Feline Eosinophilic Pneumonia"): {
        "treatment_ja": (
            "コルチコステロイド: プレドニゾロン 1-2 mg/kg PO q12h × 2-4週間、その後2-3ヶ月かけて漸減。"
            "吸入フルチカゾン 110-220 μg q12h（AeroKat使用 — ステロイド節約・維持療法）。"
            "ステロイド抵抗性: シクロスポリン 7 mg/kg PO q24h。"
            "基礎原因への対応が必須: 犬糸状虫（HARD）、肺虫（Aelurostrongylus）・回虫（Toxocara）等の寄生虫、"
            "アレルゲン、薬物反応・過敏症 — 寄生虫が同定された場合のみ駆虫を行う。"
            "気管支拡張薬: テルブタリン 0.1-0.2 mg/kg SC、テオフィリン。"
            "（Little, The Cat; Reinero 2011 Vet J）"
        ),
    },
    ("Dog", "Thelazia Eye Worm"): {
        "treatment_ja": (
            "物理的除去: 点眼麻酔（プロパラカイン）下で結膜嚢から虫体を摘出し、生理食塩水で洗浄。"
            "全身: ミルベマイシンオキシム 0.5 mg/kg PO、またはモキシデクチンスポットオン。"
            "続発性結膜炎には抗菌点眼薬。媒介はショウジョウバエ類（Phortica属）— 媒介昆虫対策。"
            "予後: 完全除去で良好。（Otranto 2005）"
        ),
    },
    ("Dog", "Lungworm (Angiostrongylus vasorum)"): {
        "treatment_ja": (
            "フェンベンダゾール 25-50 mg/kg PO q24h × 20日（第一選択）。"
            "ミルベマイシンオキシム 0.5 mg/kg PO 週1回 × 4週。"
            "モキシデクチン（スポットオン、アドボケート）: 月1回（治療＋予防）。"
            "支持療法: 凝固障害 — ビタミンK1・新鮮凍結血漿・輸血。呼吸困難には酸素。"
            "コルチコステロイド: プレドニゾロン 1 mg/kg PO q24h × 1-2週（死滅幼虫による炎症の軽減）。"
            "モニタリング: 糞便検査（Baermann法）・凝固系。（Morgan & Shaw 2010; ESCCAP）"
        ),
    },
    ("Dog", "Flea Allergy Dermatitis"): {
        "treatment_ja": (
            "徹底したノミ駆除が最重要（ノミ1匹の咬傷でも反応が起こる）: イソキサゾリン系 — "
            "フルララネル（ブラベクト）PO 12週毎、アフォキソラネル（ネクスガード）またはサロラネル（シンパリカ）PO 月1回。"
            "投与忘れが問題になる家庭ではフルララネル徐放性注射剤（ブラベクト クオンタム、6ヶ月齢以上、12ヶ月持続）も選択肢。"
            "同居動物全頭を同時に治療する。環境対策: 環境用スプレー（IGR含有）・頻回の掃除機がけ。"
            "対症療法: オクラシチニブ 0.4-0.6 mg/kg PO q12h × 14日 → q24h。"
            "短期プレドニゾロン 0.5-1 mg/kg PO q24h × 5-7日。薬用シャンプー。"
            "二次性膿皮症には必要に応じ抗菌薬。予後: 厳格なノミ対策で良好だが生涯管理を要する。"
            "（Dryden 2009; Rust 2005）"
        ),
        "treatment_append": (
            " Compliance option: fluralaner extended-release injectable (Bravecto Quantum, dogs >=6 months) "
            "gives 12 months of flea control from one veterinarian-administered injection."
        ),
    },
    ("Cat", "Flea Allergy Dermatitis"): {
        "treatment_ja": (
            "徹底したノミ駆除: イソキサゾリン系（フルララネル/ブラベクト、サロラネル配合のレボリューションプラス — 猫用製剤）。"
            "セラメクチン（レボリューション）。イミダクロプリド・フルメトリン首輪（セレスト）。"
            "同居動物全頭を同時に治療する。環境対策: 室内の掃除機がけ・寝具の洗濯・環境用スプレー。"
            "**犬用ペルメトリン製品は猫に絶対使用しない（致死的中毒）**。"
            "止痒: プレドニゾロン 1-2 mg/kg PO q24h × 3-5日、その後漸減。オクラシチニブは猫に未承認。"
            "慢性例: シクロスポリン 7 mg/kg PO q24h。二次性膿皮症にはアモキシシリン・クラブラン酸。"
            "オメガ3脂肪酸。自己誘発性脱毛の分布: 腹側・大腿内側・脇腹。"
            "予後: 通年の厳格なノミ対策で良好。（Rust 2017; Miller 2013）"
        ),
    },
    ("Ferret", "Flea Allergy Dermatitis"): {
        "treatment_ja": (
            "ノミの駆除: セラメクチン 15-30 mg/kg 外用 30日毎＋環境対策。"
            "短期コルチコステロイド: プレドニゾロン 0.5-1 mg/kg PO q12h × 3-5日（掻痒）。"
            "抗ヒスタミン薬: ジフェンヒドラミン 1-2 mg/kg PO q8-12h。外用: オートミールシャンプー・カラミン。"
            "オメガ3脂肪酸。同居動物全頭を同時に治療する。予後: ノミの根絶で良好。"
            "（Quesenberry & Carpenter 2012）"
        ),
    },
    ("Ferret", "Heartworm Disease - Caval Syndrome"): {
        "treatment_ja": (
            "大静脈症候群は緊急: 少数の虫体でも右心・大静脈を閉塞しうる（フェレットは心臓が小さく、"
            "1-2隻の成虫で致死的）。可能であれば頸静脈切開による虫体摘出を検討するが、体格が小さく技術的に困難で予後は要注意〜不良。"
            "内科的管理: イベルメクチン 0.05 mg/kg SC 月1回を抗原検査陰性化まで継続（緩徐な成虫駆除）＋"
            "プレドニゾロン 0.5-1 mg/kg PO q24h（死滅虫体による血栓塞栓・炎症の軽減）。"
            "うっ血性心不全にはフロセミド 1-2 mg/kg PO/SC q8-12h、厳格な運動制限、酸素補給。"
            "メラルソミンはフェレットでの安全性データが限られ、急速な虫体死滅による血栓塞栓のリスクが高い。"
            "予防（流行地では通年）: イベルメクチン月1回等の大環状ラクトン系。"
            "（Quesenberry & Carpenter 4th ed; American Heartworm Society）"
        ),
        "treatment": (
            "Caval syndrome is an emergency: even a few worms can obstruct the right heart/vena cava "
            "(the small ferret heart — one or two adults can be fatal). Jugular venotomy worm extraction may be "
            "attempted but is technically difficult in such a small patient; prognosis guarded to poor. "
            "Medical management: ivermectin 0.05 mg/kg SC monthly until antigen-negative (slow adulticide) plus "
            "prednisolone 0.5-1 mg/kg PO q24h to limit thromboembolic/inflammatory reactions to dying worms. "
            "Congestive heart failure: furosemide 1-2 mg/kg PO/SC q8-12h, strict cage rest, oxygen. "
            "Melarsomine has limited safety data in ferrets and a high risk of thromboembolism from rapid worm kill. "
            "Prevention (year-round in endemic areas): monthly macrocyclic lactone (e.g., ivermectin). "
            "(Quesenberry & Carpenter, Ferrets, Rabbits, and Rodents 4th ed; American Heartworm Society)"
        ),
    },
    ("Exotic Other", "Shell Evacuation Syndrome (Hermit Crab)"): {
        "treatment_ja": (
            "貝殻放棄は寄生虫症ではなく、飼育環境ストレス・脱皮異常・不適切な貝殻のサインである。"
            "環境是正が治療の本体: 湿度70-80%・温度24-28°Cを維持、脱塩素した真水と海水の両方を用意、"
            "体格に合った替えの貝殻を複数（開口部の形状違いを含む）提供、脱皮に必要な深い床材（砂・ココナッツ繊維）を確保。"
            "裸の個体は暗く静かな隔離容器で保湿し、過度のハンドリングを避ける（脱皮前後は特に）。"
            "同居個体による貝殻の奪い合い・攻撃がないか確認する。"
            "（Quesenberry & Carpenter 2012; exotic invertebrate husbandry references）"
        ),
        "treatment": (
            "Shell evacuation is not a parasitic disease — it signals husbandry stress, a molting problem or "
            "unsuitable shells. Correcting the environment is the treatment: humidity 70-80%, temperature 24-28 °C, "
            "both dechlorinated fresh and salt water, several appropriately sized spare shells (varied aperture "
            "shapes), and deep substrate (sand/coconut fiber) for molting. House a shell-less crab in a dark, quiet, "
            "humid isolation container and minimize handling (especially around a molt). Check for shell fighting "
            "or aggression from tankmates. (Quesenberry & Carpenter 2012)"
        ),
    },
}


def apply(data: list[dict]) -> int:
    changed = 0
    for d in data:
        key = (d.get("species"), d.get("name"))
        spec = CURATED.get(key)
        if not spec:
            continue
        cur = d.get("treatment_ja") or ""
        if (not cur or any(m in cur for m in TEMPLATE_MARKS)) and cur != spec["treatment_ja"]:
            d["treatment_ja"] = spec["treatment_ja"]
            changed += 1
        en = d.get("treatment") or ""
        if "treatment" in spec and en != spec["treatment"]:
            d["treatment"] = spec["treatment"]
            changed += 1
        if "treatment_append" in spec and "Bravecto Quantum" not in en:
            d["treatment"] = en.rstrip() + spec["treatment_append"]
            changed += 1
    return changed


def main() -> None:
    raw = JSON_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    n = apply(data)
    print(f"fields changed: {n}")
    if "--apply" in sys.argv and n:
        compact = "\n" not in raw.strip()[:200]
        if compact:
            JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        else:
            JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
