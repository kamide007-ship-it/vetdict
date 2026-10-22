"""Curate Feline Tooth Resorption (FORL) — 2026-10 第75弾.

The commonest feline dental disease carried the generic dental/oral category
template in most fields: treatment_ja told vets that "malocclusion requires tooth
trimming, burring or extraction depending on species" (rodent/rabbit elodont
teeth), causes listed overgrown herbivore teeth, prevention_ja listed hay for
rabbits and cuttlebone for birds, and the clinical signs described herbivore
malocclusion. Replaced in both the JSON overlay and the cat module with
FORL-specific text.

Evidence: Reiter AM, Mendoza KA. Feline odontoclastic resorptive lesions — an
unsolved enigma in veterinary dentistry. Vet Clin North Am Small Anim Pract
2002;32:791-837. Lommer MJ, Verstraete FJM. Prevalence of odontoclastic
resorption lesions and periapical radiographic lucencies in cats: 265 cases
(1995-1998). JAVMA 2000;217:1866-1869. Ingham KE et al. Prevalence of
odontoclastic resorptive lesions in a population of clinically healthy cats.
J Small Anim Pract 2001;42:439-443. DuPont GA, DeBowes LJ. Comparison of
periodontitis and root replacement in cat teeth with resorptive lesions.
J Vet Dent 2002;19:71-75. AVDC nomenclature (tooth resorption stages 1-5,
types 1-3). Bellows J et al. 2019 AAHA Dental Care Guidelines for Dogs and
Cats. JAAHA 2019;55:49-69.

Usage: python3 -m scripts.template_elimination.fix_feline_tooth_resorption [--apply]
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"
NAME = "Feline Tooth Resorption (FORL)"

FIELDS = {
    "causes": (
        "The cause of feline tooth resorption is unknown. Resorption is carried out by the cat's own odontoclasts, "
        "which are activated at the cementoenamel junction (type 1, associated with periodontal inflammation) or "
        "along the root surface without inflammation (type 2, replacement resorption with ankylosis). Proposed "
        "contributing factors include chronic gingival inflammation, excess dietary vitamin D, and age; prevalence "
        "rises with age and is reported in about 29-67% of cats depending on the population studied. It is not "
        "caused by caries (true dental caries are extremely rare in cats)."
    ),
    "causes_ja": (
        "猫の歯の吸収病変の原因は不明。猫自身の破歯細胞が活性化して歯質を吸収する。セメント-エナメル境で歯周炎症を伴って"
        "起こるもの（タイプ1）と、炎症を伴わず歯根表面が骨に置換されるもの（タイプ2、置換性吸収・骨性癒着）がある。"
        "関与が考えられている因子は慢性歯肉炎、ビタミンDの過剰摂取、加齢で、有病率は加齢とともに上昇し、"
        "調査対象により約29〜67%と報告されている。虫歯（う蝕）ではない（猫の真のう蝕は極めてまれ）。"
    ),
    "pathophysiology": (
        "Odontoclasts resorb cementum and dentin, usually starting at or below the gingival margin and progressing "
        "into the crown, where the defect fills with inflamed granulation tissue that bleeds on probing. Once dentin "
        "is exposed to the oral cavity the lesion is painful. Type 1 lesions keep a normal periodontal ligament space "
        "and root canal on radiographs; in type 2 the periodontal ligament space disappears and the root is "
        "progressively replaced by bone (ankylosis); type 3 has features of both on the same tooth. The crown "
        "eventually weakens and fractures, leaving root remnants under the gingiva."
    ),
    "pathophysiology_ja": (
        "破歯細胞がセメント質と象牙質を吸収する。多くは歯肉縁またはその直下から始まり歯冠へ進行し、欠損部は炎症性の"
        "肉芽組織で満たされプローブで出血する。象牙質が口腔に露出すると疼痛を生じる。X線でタイプ1は歯根膜腔と根管が"
        "正常に保たれ、タイプ2では歯根膜腔が消失して歯根が徐々に骨に置き換わる（骨性癒着）。タイプ3は同一歯に両方の"
        "特徴をもつ。最終的に歯冠が脆弱化して破折し、歯肉下に残根が残る。"
    ),
    "clinical_signs": (
        "Many cats show no obvious signs despite painful lesions. Signs include jaw chattering or a twitching mouth "
        "when eating or when the lesion is touched, dropping food, chewing on one side, preferring soft food, reduced "
        "appetite, drooling and occasionally oral bleeding. On examination, a red granulation tissue defect at the "
        "gingival margin (most often the mandibular third premolars) and a missing or fractured crown are typical."
    ),
    "clinical_signs_ja": (
        "疼痛性の病変があっても多くの猫は目立った症状を示さない。症状として、食事中や病変に触れた際の顎のチャタリング"
        "（口のピクつき）、食べこぼし、片側での咀嚼、柔らかい食事を好む、食欲低下、流涎、まれに口腔出血がある。"
        "検査では歯肉縁の赤い肉芽組織を伴う欠損（下顎第3前臼歯に最も多い）や、歯冠の欠損・破折が典型的。"
    ),
    "treatment_ja": (
        "治療は全身麻酔下で全顎の歯科X線を撮影し、病型を決めてから行う（X線なしの治療計画は不可）。"
        "タイプ1（歯根膜腔・根管が保たれる）：外科的抜歯で歯根まで完全に除去する。"
        "タイプ2（歯根が骨に置換されている）：歯冠切断術（意図的に歯根を残す）を選択できる。"
        "ただし歯周炎・根尖病変・歯内病変・口内炎・FeLV/FIV陽性の猫では適応外で、抜歯とする（AVDC）。"
        "修復（充填）は再吸収が進むため推奨されない。"
        "鎮痛：ブプレノルフィン 0.02 mg/kg 口腔粘膜投与 8時間毎、腎機能に問題がなければメロキシカムを短期併用。"
        "術後は数日間柔らかい食事とし、他の歯に新たな病変が出るため6〜12ヶ月毎の麻酔下歯科検診とX線で経過を追う。"
    ),
    "prevention": (
        "No proven prevention exists. Annual oral examination (and full-mouth radiographs under anaesthesia when "
        "lesions are suspected) allows early detection; daily tooth brushing and periodontal care reduce the "
        "inflammation associated with type 1 lesions. Avoid excess dietary vitamin D supplementation."
    ),
    "prevention_ja": (
        "確立された予防法はない。年1回の口腔検査（病変が疑われる場合は麻酔下の全顎歯科X線）で早期に発見する。"
        "毎日の歯磨きと歯周ケアはタイプ1病変に関連する炎症を減らす。ビタミンDの過剰な補給は避ける。"
        "早期発見には顎のチャタリング・食べこぼし・片側咀嚼・流涎などの変化を見逃さないことが重要。"
    ),
    "prognosis_ja": (
        "罹患歯を抜歯（タイプ2では歯冠切断）すれば疼痛は解消し予後は良好。ただし病変の進行を止める内科治療はなく、"
        "他の歯に新たな病変が生じることが多いため、生涯にわたる定期的な歯科検診が必要。多くの歯を抜歯しても、"
        "猫は通常のフードを食べられることが多い。"
    ),
    "transmission": ("Not infectious and not transmitted between cats."),
    "transmission_ja": "感染性はなく、猫同士で伝播しない。",
}

MODULE_FIELDS = (
    "causes",
    "causes_ja",
    "pathophysiology",
    "pathophysiology_ja",
    "treatment_ja",
    "prevention",
    "prevention_ja",
)


def main(apply: bool) -> int:
    raw = JSON_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    hit = 0
    for r in data:
        if r.get("name") == NAME and r.get("species") == "Cat":
            for k, v in FIELDS.items():
                r[k] = v
            hit += 1
    print(f"JSON records updated: {hit}")
    if apply and hit:
        JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return 0 if hit else 1


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
