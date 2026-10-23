"""Curate leishmaniasis prevention — 2026-10 第76弾.

Dog "Leishmaniasis"/"Leishmaniosis" and "Feline Leishmaniasis" carried the
generic parasite-prevention template ("puppies dewormed from 2-4 weeks, annual
heartworm prophylaxis, monthly flea/tick products") that never mentioned the
actual vector — phlebotomine sand flies. Leishmania infantum is prevented by
sand-fly repellent pyrethroids, indoor housing at dusk/dawn and, in endemic
areas, vaccination; heartworm and gut deworming are irrelevant. In cats,
deltamethrin/permethrin products are toxic, and the evidence is for the
imidacloprid/flumethrin collar.

Evidence: Solano-Gallego L et al. LeishVet guidelines for the practical
management of canine leishmaniosis. Parasit Vectors 2011;4:86. Miró G et al.
Novel areas for prevention and control of canine leishmaniosis. Trends
Parasitol 2017;33:718-730. Killick-Kendrick R et al. Protection of dogs from
bites of phlebotomine sandflies by deltamethrin collars. Med Vet Entomol
1997;11:105-111. Maroli M et al. Evidence for an impact on the incidence of
canine leishmaniasis by the mass use of deltamethrin-impregnated dog collars
in southern Italy. Med Vet Entomol 2001;15:358-363. Brianti E et al.
Prevention of feline leishmaniosis with an imidacloprid 10%/flumethrin 4.5%
polymer matrix collar. Parasit Vectors 2017;10:334. Pennisi MG et al.
LeishVet update and recommendations on feline leishmaniosis. Parasit Vectors
2015;8:302.

Usage: python3 -m scripts.template_elimination.fix_leishmaniasis_prevention [--apply]
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"

DOG = {
    "prevention_ja": (
        "リーシュマニア症はサシチョウバエ（Phlebotomus属）が媒介するため、予防の中心は吸血の防止。"
        "流行地（地中海沿岸・中南米・中東等）への滞在・渡航時は、サシチョウバエ忌避効果のあるピレスロイド製剤"
        "（デルタメトリン首輪、ペルメトリン配合スポットオン、イミダクロプリド/フルメトリン首輪）を流行期を通じて継続し、"
        "サシチョウバエが活動する夕方〜明け方は屋内で過ごさせる。流行地ではEU承認ワクチン（LetiFend等）や"
        "免疫調整（ドンペリドン）の併用が選択肢となる（LeishVet）。消化管の駆虫やフィラリア予防では予防できない。"
        "流行地からの輸入犬・帰国犬は血清検査でスクリーニングし、陽性犬は繁殖に用いない（経胎盤感染）。"
        "輸血ドナーも検査する。人獣共通感染症である。"
    ),
    "prevention": (
        "Leishmaniasis is transmitted by phlebotomine sand flies, so prevention centres on preventing bites. "
        "For dogs living in or travelling to endemic areas (Mediterranean, Latin America, Middle East), use a "
        "sand-fly-repellent pyrethroid throughout the transmission season (deltamethrin collar, permethrin-containing "
        "spot-on, or imidacloprid/flumethrin collar) and keep dogs indoors from dusk to dawn when sand flies are "
        "active. In endemic areas, an EU-licensed vaccine (e.g. LetiFend) or immunomodulation with domperidone can "
        "be added (LeishVet). Gut deworming and heartworm prophylaxis do not prevent it. Screen dogs imported from "
        "or returning from endemic areas serologically, do not breed seropositive dogs (transplacental "
        "transmission) and test blood donors. Leishmaniasis is zoonotic."
    ),
}

CAT = {
    "prevention_ja": (
        "猫リーシュマニア症もサシチョウバエが媒介する。流行地では夕方〜明け方の屋外活動を避け、"
        "猫で予防効果が示されたイミダクロプリド/フルメトリン首輪を使用する（Brianti 2017）。"
        "デルタメトリン・ペルメトリン製剤は猫に有毒なため使用しない。消化管の駆虫では予防できない。"
        "流行地由来の猫は血清/PCR検査でスクリーニングし、輸血ドナーも検査する。"
        "FIV・FeLV感染猫や免疫抑制下の猫は発症しやすい（LeishVet 2015）。"
    ),
    "prevention": (
        "Feline leishmaniasis is also transmitted by sand flies. In endemic areas keep cats indoors from dusk to "
        "dawn and use the imidacloprid/flumethrin collar, the only product shown to reduce infection in cats "
        "(Brianti 2017). Deltamethrin and permethrin products are toxic to cats and must not be used. Gut deworming "
        "does not prevent it. Screen cats from endemic areas by serology/PCR and test blood donors. FIV/FeLV-positive "
        "or immunosuppressed cats are more likely to develop disease (LeishVet 2015)."
    ),
}

# 治療文末尾の伝播対策（治療後も感染源となるため — LeishVet）。冪等に追記する。
DOG_TX_TAIL_JA = "治療中・治療後も犬はサシチョウバエへの感染源となるため、デルタメトリン首輪等の忌避剤を継続して他の犬・人への伝播を防ぐ（LeishVet）。"
DOG_TX_TAIL_EN = (
    " Treated dogs remain infectious to sand flies, so keep a repellent such as a deltamethrin collar on "
    "during and after treatment to prevent onward transmission (LeishVet)."
)

TARGETS = {
    ("Dog", "Leishmaniasis"): DOG,
    ("Dog", "Leishmaniosis"): DOG,
    ("Cat", "Feline Leishmaniasis"): CAT,
}


def main(apply: bool) -> int:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    hit = 0
    for r in data:
        fields = TARGETS.get((r.get("species"), r.get("name")))
        if fields:
            r.update(fields)
            if fields is DOG:
                if DOG_TX_TAIL_JA not in (r.get("treatment_ja") or ""):
                    r["treatment_ja"] = (r.get("treatment_ja") or "") + DOG_TX_TAIL_JA
                if DOG_TX_TAIL_EN.strip() not in (r.get("treatment") or ""):
                    r["treatment"] = (r.get("treatment") or "") + DOG_TX_TAIL_EN
            hit += 1
    print(f"JSON records updated: {hit}")
    if apply and hit:
        JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    return 0 if hit == len(TARGETS) else 1


if __name__ == "__main__":
    sys.exit(main("--apply" in sys.argv))
