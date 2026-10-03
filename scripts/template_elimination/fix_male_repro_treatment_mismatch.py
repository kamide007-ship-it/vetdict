#!/usr/bin/env python3
"""哺乳類エントリに混入した鳥・雌用生殖器テンプレートのキュレート置換（一回限り・冪等）。

第1弾: fallback_generator の reproductive テンプレート（卵停滞・卵管脱・OHE・鳥1-3 IU/羽）が
雄性疾患（犬・猫の停留精巣）や哺乳類の雌性疾患の treatment_ja にスタンプされていた5件を置換。

第2弾（利用者要望「しっかりと記載」）: 犬・猫の停留精巣の残りのテンプレート/スタブ
フィールドを教科書準拠の疾患固有記載（日英）に全面置換。clinical_signs は
「子宮蓄膿症・乳腺炎・難産・妊娠中毒症の徴候」という雌用カテゴリ文が雄疾患に
付いており、EN の causes/pathophysiology/prevention も感染症/腫瘍ボイラープレートだった。
出典: Ettinger 8th ed; Nelson & Couto 6th; Yates 2003 JSAP; Hayes 1985; Romagnoli 2017。
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"

CURATED_TREATMENT_JA = {
    ("dog", "Cryptorchidism"): (
        "【犬における停留精巣（陰睾）】\n"
        "外科: 停留側・下降側の両精巣摘出（去勢）を推奨 — 停留精巣は腫瘍化リスクが高い"
        "（セルトリ細胞腫・セミノーマ・間質細胞腫）。\n"
        "腹腔内停留: 開腹または腹腔鏡（補助下）で精巣を検索・摘出（膀胱背側〜鼠径輪の範囲）。\n"
        "鼠径部・皮下停留: 鼠径アプローチで摘出。\n"
        "ホルモン療法（GnRH・hCG による下降促進）: 有効性は限定的で推奨されない。\n"
        "繁殖: 遺伝形質（多因子性）のため罹患犬の繁殖は禁止。\n"
        "未去勢で経過観察する場合: 腫瘍化・精巣捻転の早期発見のため定期的な触診・超音波検査。\n"
        "予後: 両側精巣摘出により極めて良好（Cox 1986; Yates 2003）。"
    ),
    ("cat", "Cryptorchidism"): (
        "【猫における停留精巣】\n"
        "外科: 去勢時に停留精巣の検索・摘出が必須。鼠径部停留（最多）は鼠径アプローチ、"
        "腹腔内停留は開腹または腹腔鏡補助下で摘出。\n"
        "停留精巣は腫瘍化（セルトリ細胞腫・セミノーマ）・捻転リスクが上昇するため摘出で排除する。\n"
        "実施時期: 通常の去勢適齢で実施。両側停留（少数派）は特に見逃しに注意。\n"
        "繁殖: 遺伝性（多因子性と推定）のため罹患猫の繁殖は禁止。\n"
        "予後: 手術により極めて良好。去勢で腫瘍化リスクは排除される（Yates 2003; Romagnoli 2017）。"
    ),
    ("hamster", "Uterine Leiomyoma"): (
        "【ハムスターにおける子宮平滑筋腫】\n"
        "卵巣子宮全摘出（OVH）が根治的治療。通常は良性の平滑筋腫瘍。\n"
        "術後管理: メロキシカム 0.3 mg/kg PO q24h、強制給餌（シリンジフィーディング）、保温。\n"
        "摘出組織は病理組織検査で確定し、平滑筋肉腫（悪性）と鑑別する。\n"
        "予後: OVH により極めて良好（Reavill & Lennox 2012）。"
    ),
    ("ferret", "Ovarian Remnant Syndrome"): (
        "【フェレットにおける卵巣遺残症候群】\n"
        "遺残卵巣組織の完全な外科的摘出が根治的治療（避妊手術後の発情徴候の持続・再発が手がかり）。\n"
        "卵巣嚢胞: GnRH アゴニスト等のホルモン療法または外科。卵巣腫瘍: 外科摘出＋病理組織検査。\n"
        "術前管理: 輸液、鎮痛（メロキシカム 0.2 mg/kg PO/SC q24h）。\n"
        "持続発情による高エストロジェン血症（骨髄抑制・貧血）が疑われる場合は CBC で評価し、"
        "必要に応じ輸血等の支持療法を行う。"
    ),
    ("hedgehog", "Ovarian Granulosa Cell Tumor"): (
        "【ハリネズミにおける卵巣顆粒膜細胞腫】\n"
        "卵巣子宮全摘出（OVH）が第一選択。ホルモン産生性のことがあり、外陰部腫大・脱毛・"
        "貧血（エストロジェン性骨髄抑制）を伴いうる。\n"
        "術前評価: CBC（貧血・血小板減少の有無）、超音波・X線で腹腔内腫瘤と転移を評価。\n"
        "摘出組織は病理組織検査で確定。骨髄抑制の合併例は輸血等の支持療法。\n"
        "予後: 転移前の摘出で良好（Reavill & Lennox 2012 — ハリネズミの生殖器腫瘍は雌で高頻度）。"
    ),
}

# 第2弾: 犬・猫の停留精巣の全面キュレート（テンプレート/スタブだった残りフィールド）。
# 無条件に設定する（既存値は clinical_signs=雌用カテゴリ文・EN=腫瘍/感染ボイラープレート
# であることを監査済み。再実行は同一値の上書きで冪等）。
CURATED_FIELDS: dict[tuple[str, str], dict[str, str]] = {
    ("dog", "Cryptorchidism"): {
        "description": (
            "Failure of one or both testes to descend into the scrotum by 8 weeks of age "
            "(definitive diagnosis by 6 months). The most common congenital reproductive defect "
            "of male dogs, most frequent in toy breeds; retained testes carry a markedly "
            "increased risk of testicular tumours and torsion."
        ),
        "description_ja": (
            "片側または両側の精巣が生後8週（確定判断は6ヶ月齢）までに陰嚢へ下降しない、"
            "雄犬で最も多い先天性生殖器異常。トイ種に好発し、停留精巣は腫瘍化（約10〜13倍）と"
            "精巣捻転のリスクが大きく上昇する。"
        ),
        "causes": (
            "Heritable, multifactorial congenital defect (sex-limited autosomal recessive "
            "inheritance suspected — dams and sires transmit the trait) affecting gubernaculum "
            "development and the INSL3/androgen-dependent phases of testicular descent. "
            "Predisposed breeds: Chihuahua, Pomeranian, Yorkshire Terrier, Toy Poodle, "
            "Dachshund, Boxer. Unilateral retention (right side more often) is about three "
            "times more common than bilateral."
        ),
        "causes_ja": (
            "遺伝性・多因子性の先天異常（限性の常染色体劣性遺伝が疑われ、雌も保因者になりうる）。"
            "精巣導帯（gubernaculum）の発生と、INSL3・アンドロジェン依存性の精巣下降過程の障害による。"
            "チワワ・ポメラニアン・ヨークシャーテリア・トイプードル・ダックスフンド・ボクサー等に好発。"
            "片側性（右側に多い）が両側性の約3倍。生後8週までに下降しなければ疑い、"
            "6ヶ月齢までに下降しなければ停留と判断する。"
        ),
        "pathophysiology": (
            "Testicular descent has an intra-abdominal (INSL3-dependent) phase and an "
            "inguinoscrotal (androgen-dependent) phase; failure leaves the testis in the abdomen "
            "or inguinal canal. Core body temperature (2-4°C above scrotal) degenerates the "
            "germinal epithelium — bilateral cryptorchids are sterile, while Leydig-cell "
            "testosterone secretion persists so male behaviour and secondary sex characteristics "
            "are preserved. Chronic thermal stress raises testicular tumour risk roughly 10-13× "
            "(Sertoli cell tumour, seminoma); oestrogen-secreting Sertoli cell tumours cause "
            "feminization and potentially fatal bone-marrow suppression. Poor gubernacular "
            "fixation also predisposes the retained testis to torsion."
        ),
        "pathophysiology_ja": (
            "精巣下降は腹腔内相（INSL3依存）と鼠径陰嚢相（アンドロジェン依存）の2段階で、"
            "その障害により精巣が腹腔内または鼠径管に停留する。腹腔内は陰嚢より2〜4℃高温のため"
            "精細管上皮が変性し、両側停留では不妊となる（ライディッヒ細胞のテストステロン分泌は"
            "保たれ、雄行動・第二次性徴は維持される）。慢性熱ストレスにより腫瘍化リスクが"
            "約10〜13倍に上昇（セルトリ細胞腫・セミノーマ）。エストロジェン産生性セルトリ細胞腫は"
            "雌性化症候群（左右対称性脱毛・乳腺発達・対側精巣萎縮）と致死的な骨髄抑制"
            "（汎血球減少）を起こしうる。精巣導帯の固定が弱いため精巣捻転の素因にもなる。"
        ),
        "clinical_signs": (
            "Often an incidental finding: one or both testes absent from the scrotum on "
            "examination (check at 8-16 weeks; definitive by 6 months). An inguinal retained "
            "testis may be palpable as a mobile subcutaneous swelling. Bilateral cryptorchids "
            "are infertile but show normal male behaviour. Complication signs: abdominal "
            "mass/distension from neoplastic transformation of an intra-abdominal testis; "
            "feminization syndrome with Sertoli cell tumour (symmetrical alopecia, gynecomastia, "
            "pendulous prepuce, contralateral testicular atrophy, anaemia/bleeding from marrow "
            "suppression); acute abdomen and collapse with testicular torsion."
        ),
        "clinical_signs_ja": (
            "多くは無症候で、健診時に陰嚢内の精巣が1個のみ/両側欠如として発見される"
            "（8〜16週齢で確認、6ヶ月齢で確定）。鼠径部停留は皮下の可動性腫瘤として触知される"
            "ことがある。両側停留は不妊だが雄行動は正常。合併症の徴候: 腹腔内精巣の腫瘍化による"
            "腹部腫瘤・腹囲膨満、セルトリ細胞腫による雌性化症候群（左右対称性脱毛・乳腺発達・"
            "包皮下垂・対側精巣萎縮、骨髄抑制による貧血・出血傾向）、精巣捻転による急性腹症・虚脱。"
        ),
        "prevention": (
            "Castration (removal of both retained and scrotal testes) eliminates tumour and "
            "torsion risk — recommended at 6-12 months. Do not breed affected dogs or their "
            "parents (heritable trait). If left intact, schedule regular palpation and "
            "ultrasound for early detection of neoplasia. Verify both testes at puppy "
            "examinations (8-16 weeks)."
        ),
        "prevention_ja": (
            "停留精巣犬の去勢手術（停留側＋下降側の両側摘出）が必須 — 腫瘍化・捻転リスクを"
            "排除でき、6〜12ヶ月齢での実施が推奨される。遺伝形質のため罹患犬およびその両親の"
            "繁殖使用は避ける。未去勢で維持する場合は腫瘍化の早期発見のため定期的な触診・"
            "超音波検査を行う。子犬健診（8〜16週齢）で両精巣の陰嚢内下降を確認する。"
        ),
        "diagnosis": (
            "Palpation: one or no testes in the scrotum; palpate the inguinal canal for a "
            "subcutaneous retained testis. Abdominal ultrasound: locate an intra-abdominal "
            "testis (search from the caudal pole of the kidney to the inguinal ring — "
            "hypoechoic ovoid structure). hCG or GnRH stimulation test, or AMH assay, to "
            "distinguish a cryptorchid from a castrated dog (a post-stimulation rise in serum "
            "testosterone indicates functional testicular tissue). CT for difficult "
            "intra-abdominal cases. Verify both testes at puppy visits (8-16 weeks); "
            "diagnosis is definitive if not descended by 6 months."
        ),
    },
    ("cat", "Cryptorchidism"): {
        "description": (
            "Failure of one or both testes to descend into the scrotum (inguinal retention is "
            "most common in cats). An important differential for apparently castrated cats with "
            "persistent male behaviour; retained testes carry increased tumour and torsion risk."
        ),
        "description_ja": (
            "片側または両側の精巣が陰嚢へ下降しない先天異常（猫では鼠径部停留が最多）。"
            "去勢済みに見えて雄行動が残る猫の重要な鑑別で、停留精巣は腫瘍化・捻転のリスクが上昇する。"
        ),
        "causes": (
            "Failure of one or both testes to descend into the scrotum due to an inherited "
            "defect in gubernacular development (autosomal recessive, likely polygenic). "
            "Retained testes carry an increased risk of Sertoli cell tumour and seminoma."
        ),
        "causes_ja": (
            "精巣導帯（gubernaculum）の発生異常により片側または両側の精巣が陰嚢へ下降しない"
            "先天異常。遺伝性（劣性形質と推定）のため罹患猫の繁殖は避ける。"
            "停留精巣はセルトリ細胞腫・セミノーマの発生リスクが上昇する。"
        ),
        "pathophysiology": (
            "Failure of one or both testes to descend through the inguinal canal into the "
            "scrotum; the retained testis is exposed to core body temperature, which degenerates "
            "the seminiferous epithelium (bilateral retention causes sterility) while "
            "Leydig-cell testosterone secretion persists — so male behaviour and penile spines "
            "remain. Chronic thermal stress increases the risk of Sertoli cell tumour and "
            "seminoma, and poor fixation predisposes to torsion."
        ),
        "pathophysiology_ja": (
            "片側または両側の精巣が鼠径管を経て陰嚢へ下降せず、鼠径部または腹腔内に停留する"
            "発生異常。腹腔内の高温環境により精細管上皮が障害され（両側停留では不妊）、"
            "慢性熱ストレスによりセルトリ細胞腫・セミノーマの発生リスクが上昇する。"
            "停留精巣は固定が弱く精巣捻転のリスクも高い。雄性ホルモン分泌は保たれるため、"
            "去勢済みに見えて雄行動（尿スプレー・雄猫臭）が残る猫では停留精巣を疑う。"
        ),
        "clinical_signs": (
            "Usually asymptomatic. Suspect a retained testis in any 'castrated' cat with "
            "persistent urine spraying, tomcat urine odour, penile spines or male behaviour "
            "(testosterone secretion is preserved). Findings: one or both testes absent from "
            "the scrotum, occasionally a palpable inguinal subcutaneous mass. Complications "
            "(less frequent than in dogs): neoplastic transformation (Sertoli cell tumour, "
            "seminoma) and testicular torsion with acute abdomen."
        ),
        "clinical_signs_ja": (
            "多くは無症候。去勢済みのはずの猫で尿スプレー・雄猫臭・陰茎棘・雄行動が持続する場合は"
            "停留精巣（または遺残精巣組織）を疑う（テストステロン分泌は保たれるため）。"
            "所見: 陰嚢内精巣の片側欠如/両側欠如、まれに鼠径部の皮下腫瘤として触知。"
            "合併症（犬より頻度は低い）: 腫瘍化（セルトリ細胞腫・セミノーマ）、精巣捻転による急性腹症。"
        ),
        "prevention": (
            "Castration with retrieval of the retained testis eliminates neoplasia and torsion "
            "risk; verify both testes at routine neutering. Do not breed cryptorchid cats "
            "(heritable). Persistent penile spines after apparent castration indicate "
            "circulating testosterone and warrant a search for retained testicular tissue."
        ),
        "prevention_ja": (
            "去勢時に停留精巣を必ず検索・摘出することで腫瘍化・捻転リスクを排除できる。"
            "遺伝性のため罹患猫は繁殖に使用しない。去勢済みのはずで陰茎棘・雄行動が残る猫は"
            "テストステロン分泌源（遺残精巣組織）の検索を行う。"
        ),
        "prognosis": (
            "Excellent with castration including retrieval of the retained testis; neoplasia "
            "and torsion risk are eliminated by surgery. Untreated, the risk of Sertoli cell "
            "tumour, seminoma and torsion persists (lower incidence than in dogs)."
        ),
        "prognosis_ja": (
            "停留精巣の摘出を含む去勢により予後は極めて良好で、腫瘍化・捻転リスクは手術で"
            "排除される。放置した場合はセルトリ細胞腫・セミノーマ・捻転のリスクが残る"
            "（猫では犬より頻度は低い）。"
        ),
        "diagnosis": (
            "Begins with absence of one or both testes on scrotal palpation; palpate the "
            "inguinal region for a subcutaneous retained testis. Abdominal ultrasound to "
            "locate an intra-abdominal testis. hCG/GnRH stimulation test confirms functional "
            "testicular tissue in an apparently castrated cat (post-stimulation rise in serum "
            "testosterone; baseline >0.1 ng/mL suggests retained tissue); AMH assay is a "
            "single-sample alternative. Persistent penile spines indicate circulating "
            "testosterone and support the diagnosis."
        ),
    },
}


def main(apply: bool) -> None:
    items = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    fixed = 0
    for entry in items:
        key = ((entry.get("species") or "").lower(), entry.get("name"))
        curated = CURATED_TREATMENT_JA.get(key)
        if curated is not None:
            current = entry.get("treatment_ja") or ""
            # 既にキュレート済み（卵停滞テンプレートでない）なら触らない
            if "卵停滞" in current or "IU/羽" in current:
                entry["treatment_ja"] = curated
                fixed += 1
                print(f"fixed treatment_ja: {key}")
        fields = CURATED_FIELDS.get(key)
        if fields:
            changed = [f for f, v in fields.items() if entry.get(f) != v]
            entry.update(fields)
            if changed:
                fixed += 1
                print(f"curated fields: {key} -> {changed}")
    print(f"total fixed: {fixed}")
    if apply and fixed:
        with JSON_PATH.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, separators=(",", ":"))
        print(f"written: {JSON_PATH}")


if __name__ == "__main__":
    import sys

    main(apply="--apply" in sys.argv)
