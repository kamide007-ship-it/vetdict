"""drug_interactions.py - 薬品-薬品相互作用データベース

獣医臨床で重要な薬品相互作用を網羅。重症度3段階（contraindicated/major/moderate）。

参考文献:
- Plumb's Veterinary Drug Handbook 9th ed.
- BSAVA Small Animal Formulary 10th ed.
- Stockley's Drug Interactions
- Lexicomp Veterinary
"""

from __future__ import annotations

from typing import Any

# 重症度
SEVERITY_CONTRAINDICATED = "contraindicated"  # 禁忌（同時投与禁止）
SEVERITY_MAJOR = "major"  # 重大（特別な監視・用量調整必須）
SEVERITY_MODERATE = "moderate"  # 中等度（注意して使用）

# ---------------------------------------------------------------------------
# 相互作用テーブル
# 各エントリ: drug_a, drug_b は薬品ID（小文字スネークケース）
# ---------------------------------------------------------------------------
INTERACTIONS: list[dict[str, Any]] = [
    # ====== NSAID 関連 ======
    {
        "drug_a": "meloxicam",
        "drug_b": "carprofen",
        "severity": SEVERITY_CONTRAINDICATED,
        "mechanism": "COX阻害の重複",
        "effect_en": "Concurrent NSAIDs significantly increase risk of GI ulceration, perforation, and renal toxicity.",
        "effect_ja": "NSAIDsの併用により消化管潰瘍・穿孔・腎毒性のリスクが著しく増加。",
        "management_en": "Do not use concurrently. Wait at least 5-7 days washout when switching NSAIDs.",
        "management_ja": "併用禁忌。NSAID変更時は5-7日のウォッシュアウト期間を設ける。",
        "ref": "Plumb's 9th ed.",
    },
    {
        "drug_a": "meloxicam",
        "drug_b": "prednisolone",
        "severity": SEVERITY_CONTRAINDICATED,
        "mechanism": "胃腸粘膜保護の二重阻害",
        "effect_en": "NSAID + corticosteroid combination dramatically increases GI ulceration and bleeding risk.",
        "effect_ja": "NSAIDとコルチコステロイドの併用は消化管潰瘍・出血リスクを劇的に増加。",
        "management_en": "Do not combine. If steroid required, discontinue NSAID first with washout.",
        "management_ja": "併用禁忌。ステロイド必要時はNSAIDを中止しウォッシュアウト後に切替。",
        "ref": "AAHA 2020",
    },
    {
        "drug_a": "carprofen",
        "drug_b": "prednisolone",
        "severity": SEVERITY_CONTRAINDICATED,
        "mechanism": "胃腸粘膜保護の二重阻害",
        "effect_en": "NSAID + corticosteroid combination dramatically increases GI ulceration and bleeding risk.",
        "effect_ja": "NSAIDとコルチコステロイドの併用は消化管潰瘍・出血リスクを劇的に増加。",
        "management_en": "Do not combine.",
        "management_ja": "併用禁忌。",
        "ref": "AAHA 2020",
    },
    {
        "drug_a": "meloxicam",
        "drug_b": "furosemide",
        "severity": SEVERITY_MAJOR,
        "mechanism": "腎血流低下の相加作用",
        "effect_en": "NSAIDs reduce renal prostaglandin synthesis; combined with diuretic-induced volume depletion increases acute kidney injury risk.",
        "effect_ja": "NSAIDによる腎プロスタグランジン合成抑制と利尿薬の脱水で急性腎障害リスク増加。",
        "management_en": "Monitor BUN/creatinine, ensure hydration. Avoid in dehydrated/azotemic patients.",
        "management_ja": "BUN/クレアチニン監視、水和維持。脱水・高窒素血症患者では回避。",
        "ref": "Plumb's 9th ed.",
    },
    {
        "drug_a": "carprofen",
        "drug_b": "enalapril",
        "severity": SEVERITY_MAJOR,
        "mechanism": "ACE阻害薬の腎保護作用減弱",
        "effect_en": "NSAIDs blunt the antihypertensive and renoprotective effects of ACE inhibitors; risk of AKI in CHF/CKD.",
        "effect_ja": "NSAIDがACE阻害薬の降圧・腎保護作用を減弱。CHF/CKDで急性腎障害リスク。",
        "management_en": "Monitor renal function. Avoid in heart failure or chronic kidney disease.",
        "management_ja": "腎機能監視。心不全・慢性腎臓病では回避。",
        "ref": "ACVIM Cardiac Consensus 2019",
    },
    # ====== α2作動薬 関連 ======
    {
        "drug_a": "medetomidine",
        "drug_b": "atipamezole",
        "severity": SEVERITY_MODERATE,
        "mechanism": "α2拮抗（意図的逆転）",
        "effect_en": "Atipamezole reverses sedation and cardiovascular effects of α2 agonists. Intended interaction.",
        "effect_ja": "アチパメゾールはα2作動薬の鎮静・循環作用を拮抗。意図的相互作用（覚醒剤）。",
        "management_en": "Use as reversal agent. Equal volume IM to medetomidine dose given.",
        "management_ja": "拮抗薬として使用。投与したメデトミジンと同容量をIM。",
        "ref": "Lumb & Jones 5th ed.",
    },
    {
        "drug_a": "medetomidine",
        "drug_b": "epinephrine",
        "severity": SEVERITY_MAJOR,
        "mechanism": "α受容体への競合",
        "effect_en": "α2 agonist + epinephrine may cause severe vasoconstriction, hypertension, and ventricular arrhythmias.",
        "effect_ja": "α2作動薬とエピネフリン併用で重度血管収縮・高血圧・心室性不整脈の可能性。",
        "management_en": "Avoid combination. If epinephrine needed for anaphylaxis, use lowest effective dose.",
        "management_ja": "併用回避。アナフィラキシー時のエピネフリン投与は最小有効用量で。",
        "ref": "Lumb & Jones 5th ed.",
    },
    # ====== アミノグリコシド ======
    {
        "drug_a": "gentamicin",
        "drug_b": "furosemide",
        "severity": SEVERITY_MAJOR,
        "mechanism": "腎毒性・耳毒性の相加",
        "effect_en": "Loop diuretic + aminoglycoside synergistically increases nephrotoxicity and ototoxicity.",
        "effect_ja": "ループ利尿薬とアミノグリコシドの併用は相乗的に腎毒性・耳毒性を増加。",
        "management_en": "Avoid concurrent use. If unavoidable, monitor renal function and trough levels closely.",
        "management_ja": "併用回避。やむを得ない場合は腎機能とトラフ濃度を厳重監視。",
        "ref": "Plumb's 9th ed.",
    },
    {
        "drug_a": "amikacin",
        "drug_b": "furosemide",
        "severity": SEVERITY_MAJOR,
        "mechanism": "腎毒性・耳毒性の相加",
        "effect_en": "Loop diuretic + aminoglycoside synergistically increases nephrotoxicity and ototoxicity.",
        "effect_ja": "ループ利尿薬とアミノグリコシドの併用は相乗的に腎毒性・耳毒性を増加。",
        "management_en": "Avoid concurrent use.",
        "management_ja": "併用回避。",
        "ref": "Plumb's 9th ed.",
    },
    {
        "drug_a": "gentamicin",
        "drug_b": "cefazolin",
        "severity": SEVERITY_MODERATE,
        "mechanism": "シナジー（意図的併用）",
        "effect_en": "Synergistic gram-positive + gram-negative coverage. Common surgical prophylaxis combination.",
        "effect_ja": "グラム陽性+陰性の相乗的抗菌スペクトル。周術期予防の一般的併用。",
        "management_en": "Beneficial combination. Monitor renal function for prolonged courses.",
        "management_ja": "有益な併用。長期投与時は腎機能監視。",
        "ref": "BSAVA 10th ed.",
    },
    # ====== フッ化キノロン ======
    {
        "drug_a": "enrofloxacin",
        "drug_b": "theophylline",
        "severity": SEVERITY_MAJOR,
        "mechanism": "CYP1A2阻害によるテオフィリンクリアランス低下",
        "effect_en": "Fluoroquinolones inhibit theophylline metabolism, leading to elevated levels and toxicity (seizures, arrhythmias).",
        "effect_ja": "フルオロキノロンがテオフィリン代謝を阻害→中毒（痙攣、不整脈）。",
        "management_en": "Reduce theophylline dose by 50% or use alternative antibiotic.",
        "management_ja": "テオフィリン50%減量、または代替抗菌薬を使用。",
        "ref": "Plumb's 9th ed.",
    },
    {
        "drug_a": "enrofloxacin",
        "drug_b": "sucralfate",
        "severity": SEVERITY_MAJOR,
        "mechanism": "GI内でキレート形成",
        "effect_en": "Sucralfate (and antacids, dairy) chelates fluoroquinolones, reducing absorption by >50%.",
        "effect_ja": "スクラルファート（制酸薬・乳製品）がフルオロキノロンとキレート形成し吸収>50%低下。",
        "management_en": "Separate administration by at least 2 hours.",
        "management_ja": "投与間隔を2時間以上空ける。",
        "ref": "Plumb's 9th ed.",
    },
    # ====== トラマドール / セロトニン症候群 ======
    {
        "drug_a": "tramadol",
        "drug_b": "fluoxetine",
        "severity": SEVERITY_MAJOR,
        "mechanism": "セロトニン症候群リスク",
        "effect_en": "Both increase serotonergic activity; combination may cause serotonin syndrome (agitation, hyperthermia, seizures).",
        "effect_ja": "両薬剤がセロトニン作動性活性を増加→セロトニン症候群（興奮、高体温、痙攣）。",
        "management_en": "Avoid combination. If essential, monitor closely for serotonergic signs.",
        "management_ja": "併用回避。必須の場合はセロトニン症候群の徴候を厳重監視。",
        "ref": "Plumb's 9th ed.",
    },
    {
        "drug_a": "tramadol",
        "drug_b": "selegiline",
        "severity": SEVERITY_CONTRAINDICATED,
        "mechanism": "MAO-B阻害+セロトニン作動性",
        "effect_en": "MAOI + serotonergic agent → severe serotonin syndrome risk.",
        "effect_ja": "MAOIとセロトニン作動薬の併用で重度セロトニン症候群リスク。",
        "management_en": "Contraindicated. Allow 14-day washout when switching.",
        "management_ja": "併用禁忌。切替時は14日のウォッシュアウト期間。",
        "ref": "Plumb's 9th ed.",
    },
    # ====== オピオイド ======
    {
        "drug_a": "morphine",
        "drug_b": "acepromazine",
        "severity": SEVERITY_MODERATE,
        "mechanism": "鎮静・呼吸抑制の相加",
        "effect_en": "Common premedication combination. Synergistic sedation and analgesia, but increased respiratory depression risk.",
        "effect_ja": "一般的な前麻酔併用。鎮静・鎮痛は相乗的だが呼吸抑制リスク増加。",
        "management_en": "Useful combination at appropriate doses. Reduce individual doses 25-50%.",
        "management_ja": "適切な用量で有用。個々の用量を25-50%減量。",
        "ref": "Lumb & Jones 5th ed.",
    },
    # ====== 心臓薬 ======
    {
        "drug_a": "digoxin",
        "drug_b": "furosemide",
        "severity": SEVERITY_MAJOR,
        "mechanism": "低カリウム血症によるジゴキシン感受性増加",
        "effect_en": "Furosemide-induced hypokalemia increases digoxin toxicity risk (arrhythmias).",
        "effect_ja": "フロセミドによる低K血症がジゴキシン中毒リスクを増加（不整脈）。",
        "management_en": "Monitor serum potassium and digoxin levels regularly. Supplement K+ as needed.",
        "management_ja": "血清K+とジゴキシン濃度を定期監視。必要に応じKCl補給。",
        "ref": "ACVIM Cardiac Consensus 2019",
    },
    {
        "drug_a": "digoxin",
        "drug_b": "amiodarone",
        "severity": SEVERITY_MAJOR,
        "mechanism": "ジゴキシンクリアランス低下",
        "effect_en": "Amiodarone increases serum digoxin levels by 70-100%.",
        "effect_ja": "アミオダロンがジゴキシン血中濃度を70-100%上昇。",
        "management_en": "Reduce digoxin dose by 50%. Monitor levels.",
        "management_ja": "ジゴキシン50%減量。血中濃度監視。",
        "ref": "Plumb's 9th ed.",
    },
    # ====== 抗痙攣薬 ======
    {
        "drug_a": "phenobarbital",
        "drug_b": "chloramphenicol",
        "severity": SEVERITY_MAJOR,
        "mechanism": "CYP誘導 vs 阻害",
        "effect_en": "Chloramphenicol inhibits phenobarbital metabolism → toxicity. Phenobarbital induces metabolism of many drugs.",
        "effect_ja": "クロラムフェニコールがフェノバルビタール代謝を阻害→中毒。",
        "management_en": "Avoid combination. Monitor phenobarbital levels if essential.",
        "management_ja": "併用回避。必須の場合はフェノバルビタール血中濃度監視。",
        "ref": "Plumb's 9th ed.",
    },
    # ====== 鎮静拮抗 ======
    {
        "drug_a": "midazolam",
        "drug_b": "flumazenil",
        "severity": SEVERITY_MODERATE,
        "mechanism": "ベンゾジアゼピン拮抗（意図的）",
        "effect_en": "Flumazenil reverses benzodiazepine effects. Intended interaction.",
        "effect_ja": "フルマゼニルはベンゾジアゼピンを拮抗。意図的相互作用。",
        "management_en": "Use as reversal. Risk of resedation due to short half-life of flumazenil.",
        "management_ja": "拮抗薬として使用。フルマゼニル半減期短く再鎮静リスク。",
        "ref": "Lumb & Jones 5th ed.",
    },
    # ====== ステロイド長期 ======
    {
        "drug_a": "prednisolone",
        "drug_b": "ciclosporin",
        "severity": SEVERITY_MAJOR,
        "mechanism": "免疫抑制の相加",
        "effect_en": "Combined immunosuppression increases infection risk and may potentiate ciclosporin toxicity.",
        "effect_ja": "免疫抑制の相加で感染リスク増加、シクロスポリン毒性増強の可能性。",
        "management_en": "Use lowest effective doses. Monitor for infections, BUN/Cr.",
        "management_ja": "最小有効用量で使用。感染、BUN/Crを監視。",
        "ref": "BSAVA 10th ed.",
    },
    # ====== ペニシリン系（小型草食獣禁忌） ======
    {
        "drug_a": "amoxicillin",
        "drug_b": "_oral_route_rabbit",
        "severity": SEVERITY_CONTRAINDICATED,
        "mechanism": "腸内細菌叢破壊",
        "effect_en": "Oral penicillins/aminopenicillins kill gram-positive gut flora in rabbits/guinea pigs/chinchillas, causing fatal Clostridial enterotoxemia.",
        "effect_ja": "経口ペニシリン系はウサギ・モルモット・チンチラの腸内細菌叢を破壊し致死的クロストリジウム性エンテロトキセミアを引き起こす。",
        "management_en": "Do NOT use oral penicillins in lagomorphs/hindgut fermenters. Parenteral routes generally safer.",
        "management_ja": "ウサギ・後腸発酵動物に経口ペニシリン系禁忌。注射経路は概ね安全。",
        "ref": "BSAVA Manual of Rabbit Medicine 2014",
    },
    # ====== ワルファリン関連 ======
    {
        "drug_a": "warfarin",
        "drug_b": "meloxicam",
        "severity": SEVERITY_MAJOR,
        "mechanism": "蛋白結合競合 + 血小板機能阻害",
        "effect_en": "NSAIDs displace warfarin from protein binding and inhibit platelets → severe bleeding risk.",
        "effect_ja": "NSAIDがワルファリンを蛋白結合から遊離・血小板機能阻害→重度出血リスク。",
        "management_en": "Avoid combination. Monitor PT/INR closely if essential.",
        "management_ja": "併用回避。必須の場合はPT/INRを厳重監視。",
        "ref": "Plumb's 9th ed.",
    },
    {
        "drug_a": "warfarin",
        "drug_b": "metronidazole",
        "severity": SEVERITY_MAJOR,
        "mechanism": "CYP2C9阻害",
        "effect_en": "Metronidazole inhibits warfarin metabolism, increasing anticoagulant effect.",
        "effect_ja": "メトロニダゾールがワルファリン代謝を阻害し抗凝固作用を増強。",
        "management_en": "Reduce warfarin dose 30-50%. Monitor PT/INR.",
        "management_ja": "ワルファリン30-50%減量。PT/INR監視。",
        "ref": "Plumb's 9th ed.",
    },
    # ====== エキゾチックの致死的相互作用 ======
    {
        "drug_a": "fipronil",
        "drug_b": "_species_rabbit",
        "severity": SEVERITY_CONTRAINDICATED,
        "mechanism": "フィプロニル感受性",
        "effect_en": "Fipronil is fatal to rabbits even at standard topical doses (seizures, death).",
        "effect_ja": "フィプロニルは標準局所用量でもウサギに致死的（痙攣・死亡）。",
        "management_en": "NEVER use fipronil on rabbits. Use selamectin or imidacloprid instead.",
        "management_ja": "ウサギには絶対使用禁止。セラメクチンまたはイミダクロプリドを使用。",
        "ref": "BSAVA Manual of Rabbit Medicine 2014",
    },
    {
        "drug_a": "fipronil",
        "drug_b": "_species_chinchilla",
        "severity": SEVERITY_CONTRAINDICATED,
        "mechanism": "フィプロニル感受性",
        "effect_en": "Fipronil is fatal to chinchillas.",
        "effect_ja": "フィプロニルはチンチラに致死的。",
        "management_en": "NEVER use fipronil on chinchillas.",
        "management_ja": "チンチラには絶対使用禁止。",
        "ref": "Quesenberry & Carpenter 2012",
    },
    {
        "drug_a": "ivermectin",
        "drug_b": "_breed_collie",
        "severity": SEVERITY_CONTRAINDICATED,
        "mechanism": "MDR1/ABCB1変異による血液脳関門通過",
        "effect_en": "Collies/Australian Shepherds with MDR1 mutation: high-dose ivermectin causes neurotoxicity (ataxia, coma, death).",
        "effect_ja": "MDR1変異のあるコリー/オーストラリアンシェパード：高用量イベルメクチンで神経毒性（失調、昏睡、死亡）。",
        "management_en": "Test for MDR1 mutation. Avoid high-dose ivermectin in MDR1+/+ or +/-. Heartworm prevention dose is generally safe.",
        "management_ja": "MDR1変異検査。MDR1+/+ または +/- では高用量イベルメクチン回避。フィラリア予防用量は概ね安全。",
        "ref": "Mealey 2004 JAVMA",
    },
    # ====== その他臨床的に重要 ======
    {
        "drug_a": "metoclopramide",
        "drug_b": "ondansetron",
        "severity": SEVERITY_MODERATE,
        "mechanism": "セロトニン受容体作用の重複",
        "effect_en": "Both 5-HT3 effects; concurrent use generally not necessary and may increase QT prolongation.",
        "effect_ja": "両薬剤とも5-HT3作用。併用は通常不要、QT延長リスク増加の可能性。",
        "management_en": "Use one or the other; rarely beneficial in combination.",
        "management_ja": "どちらか一方を使用。併用は稀に有益。",
        "ref": "Plumb's 9th ed.",
    },
    {
        "drug_a": "doxycycline",
        "drug_b": "calcium",
        "severity": SEVERITY_MODERATE,
        "mechanism": "GI内でキレート形成",
        "effect_en": "Calcium (and Mg, Al, Fe) chelates doxycycline, reducing absorption.",
        "effect_ja": "カルシウム（Mg、Al、Feも）がドキシサイクリンとキレート形成し吸収低下。",
        "management_en": "Separate by 2-3 hours. Avoid dairy with doxycycline.",
        "management_ja": "投与間隔を2-3時間空ける。乳製品同時摂取回避。",
        "ref": "Plumb's 9th ed.",
    },
    {
        "drug_a": "ketoconazole",
        "drug_b": "ciclosporin",
        "severity": SEVERITY_MAJOR,
        "mechanism": "CYP3A4阻害（意図的併用あり）",
        "effect_en": "Ketoconazole inhibits ciclosporin metabolism. Often used intentionally to reduce ciclosporin dose/cost.",
        "effect_ja": "ケトコナゾールがシクロスポリン代謝を阻害。意図的併用でシクロスポリン用量・費用削減目的。",
        "management_en": "If intentional: reduce ciclosporin to 25-50%. Monitor levels. If unintentional: same dose adjustment needed.",
        "management_ja": "意図的併用：シクロスポリンを25-50%に減量し血中濃度監視。",
        "ref": "BSAVA 10th ed.",
    },
    {
        "drug_a": "trimethoprim_sulfa",
        "drug_b": "ciclosporin",
        "severity": SEVERITY_MAJOR,
        "mechanism": "腎毒性の相加",
        "effect_en": "TMS + ciclosporin synergistically increases nephrotoxicity.",
        "effect_ja": "TMSとシクロスポリン併用で相加的腎毒性。",
        "management_en": "Monitor BUN/Cr closely. Consider alternative antibiotic.",
        "management_ja": "BUN/Cr厳重監視。代替抗菌薬を検討。",
        "ref": "Plumb's 9th ed.",
    },
]


def normalize_drug_id(drug_id: str) -> str:
    """薬品IDを正規化（小文字・スネークケース）"""
    return (drug_id or "").lower().strip().replace("-", "_").replace(" ", "_")


def find_interactions(drug_ids: list[str]) -> list[dict[str, Any]]:
    """
    与えられた薬品IDリストから相互作用を全て検出する。
    重症度順（contraindicated → major → moderate）でソートして返す。
    """
    if not drug_ids or len(drug_ids) < 1:
        return []

    normalized = {normalize_drug_id(d) for d in drug_ids}
    matches: list[dict[str, Any]] = []
    seen_pairs: set[tuple[str, str]] = set()

    for ix in INTERACTIONS:
        a = normalize_drug_id(ix["drug_a"])
        b = normalize_drug_id(ix["drug_b"])
        # 両方とも入力リストに含まれる場合のみ
        if a in normalized and b in normalized:
            pair = tuple(sorted([a, b]))
            if pair not in seen_pairs:
                seen_pairs.add(pair)
                matches.append({**ix, "drug_a": a, "drug_b": b})

    # 重症度順
    severity_order = {SEVERITY_CONTRAINDICATED: 0, SEVERITY_MAJOR: 1, SEVERITY_MODERATE: 2}
    matches.sort(key=lambda x: severity_order.get(x.get("severity", ""), 99))
    return matches


def find_species_specific_warnings(drug_id: str, species: str) -> list[dict[str, Any]]:
    """
    薬品IDと動物種から、種特異的な禁忌・警告を検出する。
    (e.g., fipronil + rabbit, oral amoxicillin + rabbit)
    """
    drug_n = normalize_drug_id(drug_id)
    species_n = normalize_drug_id(species)
    matches: list[dict[str, Any]] = []

    for ix in INTERACTIONS:
        a = normalize_drug_id(ix["drug_a"])
        b = normalize_drug_id(ix["drug_b"])
        # 種特異的マーカー（_species_xxx, _oral_route_xxx, _breed_xxx）
        if a == drug_n and (b.startswith("_species_") or b.startswith("_oral_route_") or b.startswith("_breed_")):
            target = b.replace("_species_", "").replace("_oral_route_", "").replace("_breed_", "")
            if target == species_n:
                matches.append(ix)
        elif b == drug_n and (a.startswith("_species_") or a.startswith("_oral_route_") or a.startswith("_breed_")):
            target = a.replace("_species_", "").replace("_oral_route_", "").replace("_breed_", "")
            if target == species_n:
                matches.append(ix)

    return matches


def get_all_interactions_for_drug(drug_id: str) -> list[dict[str, Any]]:
    """単一薬品に関わる全相互作用を返す（参考表示用）"""
    drug_n = normalize_drug_id(drug_id)
    matches = []
    for ix in INTERACTIONS:
        a = normalize_drug_id(ix["drug_a"])
        b = normalize_drug_id(ix["drug_b"])
        if a == drug_n or b == drug_n:
            matches.append(ix)

    severity_order = {SEVERITY_CONTRAINDICATED: 0, SEVERITY_MAJOR: 1, SEVERITY_MODERATE: 2}
    matches.sort(key=lambda x: severity_order.get(x.get("severity", ""), 99))
    return matches
