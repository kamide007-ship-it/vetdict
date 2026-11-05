"""Curate Feline Squamous Cell Carcinoma (Nasal Planum) — 2026-11 第83弾.

The UV-induced nasal-planum carcinoma of white-faced cats carried the generic
oncology template in most explanatory fields: prevention told vets that early
spay/neuter reduces "hormone-dependent tumours (mammary, prostate, testicular,
uterine, anal-gland)" and transmission/causes cited oncogenic viruses (FeLV) —
none of which applies to an actinic (solar) carcinoma, whose only modifiable
risk is sun exposure. Clinical signs were the generic "progressive mass, weight
loss, anaemia" list instead of the crusting/erosion that does not heal.
Replaced in the JSON overlay and the cat module with disease-specific text.

Evidence: Lana SE et al. Feline cutaneous squamous cell carcinoma of the nasal
planum and the pinnae: 61 cases. JAAHA 1997;33:329-332. Hammond GM et al.
Treatment of superficial squamous cell carcinoma of the nasal planum in cats
with strontium-90 plesiotherapy: 49 cases. J Feline Med Surg 2007;9:211-217.
Murphy S. Cutaneous squamous cell carcinoma in the cat: current understanding
and treatment approaches. J Feline Med Surg 2013;15:401-407. Withrow &
MacEwen's Small Animal Clinical Oncology 6th ed (2020), ch. 18.

Usage: python3 -m scripts.template_elimination.fix_feline_nasal_planum_scc [--apply]
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"
MODULE_PATH = ROOT / "api" / "species" / "cat_diseases.py"
NAME = "Feline Squamous Cell Carcinoma (Nasal Planum)"

FIELDS = {
    "causes": (
        "Chronic ultraviolet (UV-B) exposure of poorly pigmented, sparsely haired skin is the "
        "principal cause: white or white-faced cats that sunbathe (outdoor access, windowsills) "
        "are predisposed, and the nasal planum, pinnae and eyelids are the classic sites. UV "
        "induces p53 mutation in keratinocytes. Lesions progress over months to years from "
        "actinic (solar) dermatitis/keratosis through carcinoma in situ to invasive carcinoma. "
        "It is not infectious and is unrelated to sex hormones."
    ),
    "causes_ja": (
        "主因は色素の乏しい無毛〜薄毛部の皮膚への慢性的な紫外線（UV-B）曝露。日光浴をする"
        "白猫・白顔の猫（屋外飼育・窓辺）に好発し、鼻平面・耳介・眼瞼が典型部位。紫外線が"
        "角化細胞の p53 変異を誘発し、数ヶ月〜数年かけて日光性皮膚炎（日光角化症）→"
        "上皮内癌→浸潤癌へ進行する。感染性ではなく、性ホルモンとも無関係。"
    ),
    "pathophysiology": (
        "UV-induced DNA damage (cyclobutane pyrimidine dimers, p53 mutation) in epidermal "
        "keratinocytes of unpigmented skin leads to actinic keratosis, then carcinoma in situ "
        "confined above the basement membrane, then invasive squamous cell carcinoma that "
        "destroys the nasal planum and can extend into the nasal cavity and premaxilla. The "
        "tumour is locally aggressive but metastasises late and infrequently (regional lymph "
        "nodes, rarely lungs), so local control determines outcome."
    ),
    "pathophysiology_ja": (
        "無色素部の表皮角化細胞に紫外線による DNA 損傷（シクロブタン型ピリミジン二量体・"
        "p53 変異）が蓄積し、日光角化症→基底膜を越えない上皮内癌→浸潤性扁平上皮癌へと"
        "進行する。浸潤癌は鼻平面を破壊し、鼻腔・切歯骨へ進展しうる。局所浸潤性は強いが"
        "転移は遅く頻度も低い（所属リンパ節、まれに肺）ため、予後は局所制御で決まる。"
    ),
    "clinical_signs": (
        "Early: erythema, scaling and superficial crusting of the nasal planum that bleeds "
        "when the crust is removed and fails to heal (often mistaken for a scratch or sunburn); "
        "similar changes on the pinna tips or eyelids. Advanced: deep ulceration and erosion "
        "that deforms the nose, intermittent bleeding, sneezing and nasal discharge or "
        "epistaxis when the nasal cavity is invaded."
    ),
    "clinical_signs_ja": (
        "初期: 鼻平面の紅斑・鱗屑・表在性の痂皮。痂皮が剥がれると出血し治らない"
        "（ひっかき傷や日焼けと誤認されやすい）。耳介先端・眼瞼にも同様の変化。進行例: 深い"
        "潰瘍・びらんで鼻の形が変形し、断続的な出血、鼻腔浸潤時はくしゃみ・鼻汁・鼻出血。"
    ),
    "prevention": (
        "Limit sun exposure in white or white-faced cats: keep indoors during peak UV hours "
        "(roughly 10:00-16:00), apply UV-blocking film to sunny windows, and provide shade. "
        "Sunscreens are poorly tolerated and licked off; never use zinc-oxide products, which "
        "are toxic if ingested. Biopsy any nasal planum or pinnal crust that has not healed "
        "within a few weeks, because carcinoma in situ is curable with minimally invasive "
        "treatment."
    ),
    "prevention_ja": (
        "白猫・白顔の猫は日光曝露を制限する: 紫外線の強い時間帯（おおむね10〜16時）は室内に"
        "置き、日の当たる窓に紫外線カットフィルムを貼り、日陰を用意する。日焼け止めは舐め"
        "取られやすく効果が乏しい。酸化亜鉛を含む製品は誤食で中毒を起こすため使用しない。"
        "数週間で治らない鼻平面・耳介の痂皮は早期に生検する（上皮内癌の段階なら低侵襲治療で"
        "根治可能）。"
    ),
    "prognosis": (
        "Good when treated early and with adequate local control. Superficial lesions treated "
        "with strontium-90 plesiotherapy show high complete-response rates with long "
        "progression-free intervals (Hammond 2007); nasal planectomy for invasive tumours gives "
        "durable local control in most cats (Lana 1997). Prognosis worsens with deep invasion "
        "into the nasal cavity, incomplete margins or untreated progression; new lesions may "
        "arise at other sun-exposed sites, so lifelong UV avoidance and rechecks are needed."
    ),
    "prognosis_ja": (
        "早期に十分な局所制御を行えば予後は良好。表在性病変へのストロンチウム90接触照射は"
        "完全奏効率が高く無増悪期間も長い（Hammond 2007）。浸潤例への鼻平面切除術でも多くの"
        "猫で長期の局所制御が得られる（Lana 1997）。鼻腔への深部浸潤・不完全切除・未治療の"
        "進行では予後は悪化する。他の日光曝露部位に新病変が生じうるため、生涯の紫外線対策と"
        "定期検診が必要。"
    ),
    "transmission": (
        "Not contagious. Housemates are not at risk; other white cats in the same household "
        "share the same sun-exposure risk and should be protected and checked."
    ),
    "transmission_ja": (
        "伝染性はなく同居動物への感染はない。ただし同じ環境の白猫は同じ日光曝露リスクを"
        "持つため、同様の対策と観察が必要。"
    ),
}

NEW_SYMPTOM = "nasal_planum_lesion"


def _patch_json() -> int:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    hit = 0
    for r in data:
        if r.get("name") == NAME and r.get("species") == "Cat":
            r.update(FIELDS)
            syms = list(r.get("symptoms") or [])
            if NEW_SYMPTOM not in syms:
                syms.append(NEW_SYMPTOM)
            for s in ("crusting", "non_healing_wound"):
                if s not in syms:
                    syms.append(s)
            r["symptoms"] = syms
            hit += 1
    return hit, data


def _patch_module(src: str) -> tuple[str, int]:
    start = src.index(f'"name": "{NAME}"')
    end = src.index("\n    },", start)
    block = src[start:end]
    n = 0
    for k, v in FIELDS.items():
        pat = re.compile(r'^(\s*)"' + re.escape(k) + r'": ".*",$', re.M)
        new, c = pat.subn(lambda m, v=v, k=k: f'{m.group(1)}"{k}": {json.dumps(v, ensure_ascii=False)},', block)
        block, n = new, n + c
    block = block.replace(
        '"symptoms": {"non_healing_wound", "crusting", "bleeding", "nasal_discharge", "facial_swelling"}',
        '"symptoms": {"nasal_planum_lesion", "non_healing_wound", "crusting", "bleeding", "nasal_discharge", "facial_swelling"}',
    )
    return src[:start] + block + src[end:], n


def main(apply: bool) -> int:
    hit, data = _patch_json()
    src = MODULE_PATH.read_text(encoding="utf-8")
    new_src, n = _patch_module(src)
    print(f"JSON records updated: {hit}; module fields replaced: {n}")
    if apply and hit:
        JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        MODULE_PATH.write_text(new_src, encoding="utf-8")
    return 0 if hit else 1


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
