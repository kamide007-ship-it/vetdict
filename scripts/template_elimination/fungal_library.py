"""Curated etiology / pathophysiology for named-pathogen fungal diseases.

Companion to ``pathogen_library`` (viral) and ``bacterial_library``. Mycoses
whose name identifies the fungus shipped the generic fungal category template —
JA ``「…の原因は真菌感染である…」`` and English ``"Fungal infection. Inhalation or
contact with environmental spores…"`` / ``"Fungal infections are caused by
pathogenic or opportunistic fungi…"``. When the name names the organism
(dermatophytosis, aspergillosis, cryptococcosis …) the aetiology is a textbook
fact, curated with zero fabrication risk.

Generators return pathogen-specific ``causes`` + ``pathophysiology`` (JA + EN),
host-aware where the presentation differs (Microsporum canis in cats vs
Trichophyton in rodents; avian air-sac vs canine nasal vs equine guttural-pouch
aspergillosis; feline nasal/CNS cryptococcosis; Saprolegnia water-mould in fish).

References: Greene, *Infectious Diseases of the Dog and Cat* 4th ed; Sykes,
*Canine and Feline Infectious Diseases*; Carpenter, *Exotic Animal Formulary*
6th ed; Noga, *Fish Disease* 2nd ed.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    SPECIES_EN,
    SPECIES_JA,
    _neutralise_negations,
)

_BIRDS = {"bird", "parakeet", "parrot"}
_AQUATIC = {"fish", "amphibian"}


def _ja(sp: str) -> str:
    return SPECIES_JA.get(sp, sp)


def _en(sp: str) -> str:
    return SPECIES_EN.get(sp, sp)


def _dermatophyte(sp):
    j, e = _ja(sp), _en(sp)
    if sp in ("cat", "dog"):
        cja = f"{j}の皮膚糸状菌症（白癬）は主に Microsporum canis（一部 Trichophyton・M. gypseum）の感染による。感染動物・被毛・鱗屑や汚染環境との接触で伝播する人獣共通感染症。"
        cen = "Caused chiefly by Microsporum canis (also Trichophyton, M. gypseum), spread by contact with infected animals, hair/scale and a contaminated environment — a zoonosis (ringworm)."
    else:
        cja = f"{j}の皮膚糸状菌症（白癬）は主に Trichophyton mentagrophytes 等の感染による。汚染された敷料・環境や保菌個体との接触で伝播する人獣共通感染症。"
        cen = f"Caused chiefly by Trichophyton mentagrophytes and related dermatophytes in {e}, spread via contaminated bedding/environment and carrier animals — a zoonosis (ringworm)."
    pja = "角質好性の糸状菌が被毛・角層・爪などの角化組織に侵入・増殖し、毛包炎・脱毛・鱗屑・痂皮を生じる。胞子は環境中で長期間感染性を保ち再感染源となる。"
    pen = "Keratinophilic fungi invade and proliferate in keratinised tissue (hair shafts, stratum corneum, claws) causing folliculitis, alopecia, scaling and crusting; spores remain infective in the environment for months, driving re-infection."
    return cja, cen, pja, pen


def _aspergillus(sp):
    j, e = _ja(sp), _en(sp)
    if sp in _BIRDS:
        cja = "鳥のアスペルギルス症は環境中の Aspergillus fumigatus 等の分生子（胞子）吸入による日和見感染。換気不良・高湿度・汚染敷料・栄養不良・免疫抑制が発症要因となる。"
        cen = "Caused by inhalation of Aspergillus fumigatus conidia; an opportunist favoured by poor ventilation, high humidity, soiled bedding, malnutrition and immunosuppression."
        pja = "吸入された分生子が気嚢・肺で発芽し、肉芽腫性の気嚢炎・肺炎（真菌プラーク・菌塊）を形成する。慢性進行性で、毒素産生と血管侵襲により全身へ波及しうる。"
        pen = "Inhaled conidia germinate in the air sacs and lungs forming granulomatous airsacculitis/pneumonia (fungal plaques and mycelial masses); disease is chronic-progressive and can disseminate via toxins and angioinvasion."
    elif sp == "dog":
        cja = "犬のアスペルギルス症は Aspergillus fumigatus 等の吸入による。鼻腔型が多く、播種型（A. terreus 等）はジャーマン・シェパードで報告される。"
        cen = "Caused by inhaled Aspergillus fumigatus (nasal form) or, in disseminated disease (often A. terreus, German Shepherds), by systemic spread."
        pja = "鼻腔型では鼻甲介粘膜に真菌プラークを形成し、酵素・毒素で骨・鼻甲介を破壊して破壊性鼻炎・鼻出血・鼻梁疼痛を起こす。播種型では椎体・腎などに血行性に病巣を作る。"
        pen = "In the nasal form fungal plaques on the turbinate mucosa release enzymes/toxins that destroy bone and turbinates, causing destructive rhinitis, epistaxis and facial pain; the disseminated form seeds vertebrae and kidneys haematogenously."
    elif sp == "horse":
        cja = "馬の喉嚢真菌症は Aspergillus 等が喉嚢内壁に真菌プラークを形成する日和見感染で、内頸動脈等の血管上に好発する。"
        cen = "Caused by Aspergillus forming a fungal plaque on the guttural-pouch lining, characteristically overlying the internal carotid artery."
        pja = "真菌プラーク下の血管壁が侵食されて動脈破綻を起こし、致死的な鼻出血（喉嚢からの出血）を生じる。近接する脳神経の障害で嚥下障害・喉頭麻痺・ホルネル症候群を伴う。"
        pen = "Vascular erosion beneath the plaque leads to arterial rupture and life-threatening epistaxis, while damage to adjacent cranial nerves causes dysphagia, laryngeal paralysis and Horner's syndrome."
    else:
        cja = f"{j}のアスペルギルス症は環境中の Aspergillus 属分生子の吸入による日和見真菌感染で、免疫抑制・不衛生環境が発症要因となる。"
        cen = f"Caused by inhalation of environmental Aspergillus conidia in {e}, an opportunist favoured by immunosuppression and unhygienic conditions."
        pja = "分生子が呼吸器で発芽し、肉芽腫性の炎症と血管侵襲による組織壊死を起こす。慢性進行性で全身播種しうる。"
        pen = "Conidia germinate in the respiratory tract causing granulomatous inflammation and angioinvasive tissue necrosis, chronic-progressive and potentially disseminating."
    return cja, cen, pja, pen


def _candida(sp):
    j, e = _ja(sp), _en(sp)
    if sp in _BIRDS:
        cja = "鳥のカンジダ症（そ嚢真菌症）は常在酵母 Candida albicans の日和見的過増殖による消化管感染で、若齢（挿し餌雛）・長期抗菌薬・免疫低下・ビタミンA欠乏が誘因となる。"
        cen = "Caused by opportunistic overgrowth of the commensal yeast Candida albicans (crop mycosis), precipitated in hand-fed chicks, by prolonged antibiotics, immunosuppression and vitamin-A deficiency."
    else:
        cja = f"{j}のカンジダ症は常在酵母 Candida albicans の日和見的過増殖による。免疫抑制・長期抗菌薬・粘膜バリア破綻・湿潤環境が発症要因となる。"
        cen = f"Caused by opportunistic overgrowth of the commensal yeast Candida albicans in {e}, favoured by immunosuppression, prolonged antibiotics, mucosal barrier disruption and moisture."
    pja = "酵母・仮性菌糸が粘膜表面で過増殖して白色の偽膜・プラークを形成し、粘膜炎症・びらん・消化吸収障害を起こす。基礎的な免疫低下があると深部・全身へ波及しうる。"
    pen = "Yeast and pseudohyphae overgrow the mucosal surface forming white pseudomembranes/plaques with mucosal inflammation, erosion and impaired digestion; with underlying immunosuppression it can extend to deep or systemic disease."
    return cja, cen, pja, pen


def _cryptococcus(sp):
    j = _ja(sp)
    if sp == "cat":
        cja = "猫のクリプトコッカス症は莢膜を持つ酵母 Cryptococcus neoformans／gattii の吸入による。ハト糞やユーカリ等で汚染された環境が感染源で、猫で最も多い全身性真菌症。"
        cen = "Caused by inhalation of the encapsulated yeast Cryptococcus neoformans/gattii from environments contaminated by pigeon droppings or eucalyptus — the most common systemic mycosis of cats."
    else:
        cja = f"{j}のクリプトコッカス症は莢膜酵母 Cryptococcus neoformans／gattii の吸入による。環境由来の日和見感染で、鼻腔から中枢神経・眼・皮膚へ波及する。"
        cen = f"Caused by inhalation of the encapsulated yeast Cryptococcus neoformans/gattii in {_en(sp)}, an environmental opportunist spreading from the nasal cavity to CNS, eyes and skin."
    pja = "厚い多糖莢膜が食菌・免疫を回避し、鼻腔で増殖して腫瘤（ローマ鼻）を形成後、篩板を越えて中枢神経・眼に波及し、ゼラチン様の肉芽腫性病変を作る。"
    pen = "Its thick polysaccharide capsule evades phagocytosis; the yeast proliferates in the nasal cavity forming masses ('Roman nose'), then crosses the cribriform plate to the CNS and eyes, producing gelatinous granulomatous lesions."
    return cja, cen, pja, pen


def _malassezia(sp):
    j = _ja(sp)
    cja = f"{j}のマラセチア症は常在脂好性酵母 Malassezia pachydermatis の過増殖による。アレルギー性皮膚炎・脂漏・湿潤・免疫低下などの基礎要因を背景に発症する。"
    cen = f"Caused by overgrowth of the commensal lipophilic yeast Malassezia pachydermatis in {_en(sp)}, on a background of allergic dermatitis, seborrhoea, moisture or immunosuppression."
    pja = "脂好性酵母が皮膚・外耳道で過増殖し、その代謝産物と過敏反応により脂漏性皮膚炎・外耳炎（紅斑・悪臭・掻痒・苔癬化）を起こす。基礎疾患の管理が再発防止に重要。"
    pen = "The lipophilic yeast overgrows in skin and ear canals; its metabolites and host hypersensitivity drive seborrhoeic dermatitis and otitis (erythema, malodour, pruritus, lichenification), so control of the underlying disease is key to preventing relapse."
    return cja, cen, pja, pen


def _histoplasma(sp):
    j = _ja(sp)
    cja = f"{j}のヒストプラズマ症は二形性真菌 Histoplasma capsulatum の分生子吸入による。鳥・コウモリの糞で富栄養化した土壌が感染源となる。"
    cen = f"Caused by inhaling conidia of the dimorphic fungus Histoplasma capsulatum in {_en(sp)}, from soil enriched with bird or bat droppings."
    pja = "吸入後に酵母型へ転換し、マクロファージ内で増殖して細網内皮系（肺・消化管・肝脾・骨髄）に播種する。肉芽腫性炎症により慢性の消耗・下痢・呼吸器症状・汎血球減少を起こす。"
    pen = "After inhalation it converts to the yeast form and multiplies within macrophages, disseminating through the reticuloendothelial system (lung, gut, liver/spleen, marrow); granulomatous inflammation causes chronic wasting, diarrhoea, respiratory signs and cytopenias."
    return cja, cen, pja, pen


def _blastomyces(sp):
    j = _ja(sp)
    cja = f"{j}のブラストミセス症は二形性真菌 Blastomyces dermatitidis の分生子吸入による。水辺・湿潤な土壌が感染源で、若齢大型犬に多い。"
    cen = f"Caused by inhaling conidia of the dimorphic fungus Blastomyces dermatitidis in {_en(sp)}, from moist soil near water; young large-breed dogs are over-represented."
    pja = "肺で酵母型に転換して化膿性肉芽腫性肺炎を起こし、血行性に皮膚・骨・眼・リンパ節へ播種する。広基性出芽酵母が特徴で、眼病変やドレナージする皮膚結節を生じる。"
    pen = "In the lung it converts to the yeast form causing pyogranulomatous pneumonia and disseminates haematogenously to skin, bone, eyes and lymph nodes; the broad-based budding yeast produces ocular lesions and draining skin nodules."
    return cja, cen, pja, pen


def _coccidioides(sp):
    j = _ja(sp)
    cja = f"{j}のコクシジオイデス症（渓谷熱）は二形性真菌 Coccidioides immitis／posadasii の分節分生子吸入による。乾燥した砂漠地帯（米国南西部等）の土壌が感染源。"
    cen = f"Caused by inhaling arthroconidia of the dimorphic fungus Coccidioides immitis/posadasii in {_en(sp)} (Valley Fever), from arid desert soils (e.g. south-western USA)."
    pja = "肺で球状体（spherule）を形成して肉芽腫性肺炎・肺門リンパ節腫大を起こし、播種型では骨・関節・皮膚・中枢神経に波及して難治性の慢性経過をとる。"
    pen = "In the lung it forms spherules causing granulomatous pneumonia and hilar lymphadenopathy; the disseminated form involves bone, joints, skin and CNS with a refractory chronic course."
    return cja, cen, pja, pen


def _sporothrix(sp):
    j = _ja(sp)
    cja = f"{j}のスポロトリックス症は二形性真菌 Sporothrix schenckii の創傷・咬掻傷からの接種による。猫では病変中に大量の菌を含み、ヒト・動物への感染力が強い重要な人獣共通感染症。"
    cen = f"Caused by inoculation of the dimorphic fungus Sporothrix schenckii through wounds/scratches in {_en(sp)}; feline lesions teem with organisms, making it a highly transmissible zoonosis."
    pja = "接種部位で酵母型に転換し、皮膚・皮下に結節・潰瘍を形成してリンパ管に沿って上行拡大（リンパ皮膚型）する。免疫低下では播種しうる。"
    pen = "At the inoculation site it converts to the yeast form producing cutaneous/subcutaneous nodules and ulcers that ascend along lymphatics (lymphocutaneous form), and may disseminate in immunosuppressed hosts."
    return cja, cen, pja, pen


def _mucor(sp):
    j = _ja(sp)
    cja = f"{j}の接合菌症（ムコール症）は Rhizopus・Mucor 等の接合菌の感染による。免疫抑制・糖尿病・アシドーシス・重度の基礎疾患を背景に発症する日和見感染。"
    cen = f"Caused by zygomycetes (Rhizopus, Mucor) in {_en(sp)}, an opportunist arising with immunosuppression, diabetes/acidosis or severe underlying disease."
    pja = "幅広で隔壁の乏しい菌糸が血管に侵入（血管侵襲性）して血栓・梗塞・広範な組織壊死を急速に起こす。進行が速く予後不良のことが多い。"
    pen = "Broad, sparsely septate hyphae invade blood vessels (angioinvasion) causing thrombosis, infarction and rapid extensive tissue necrosis; progression is fast and the prognosis often poor."
    return cja, cen, pja, pen


def _pythium(sp):
    j = _ja(sp)
    cja = f"{j}のピシウム症は卵菌類 Pythium insidiosum の感染による。暖かい淡水環境で遊走子が損傷皮膚や消化管に侵入して発症する。"
    cen = f"Caused by the oomycete Pythium insidiosum in {_en(sp)}; motile zoospores in warm freshwater invade damaged skin or the gastrointestinal tract."
    pja = "菌糸様構造が組織に侵入して好酸球性の肉芽腫性炎症を起こし、消化管型では著明な腸壁肥厚と閉塞を、皮膚型では難治性の潰瘍・瘻管を形成する。"
    pen = "Hypha-like elements invade tissue provoking eosinophilic pyogranulomatous inflammation — marked intestinal-wall thickening and obstruction in the GI form, and refractory ulcers with draining tracts in the cutaneous form."
    return cja, cen, pja, pen


def _saprolegnia(sp):
    j = _ja(sp)
    cja = f"{j}の水生菌症（サプロレグニア症・綿かぶり病）は卵菌類 Saprolegnia 等の日和見感染による。外傷・低水温・不良水質・ストレスで損傷した皮膚・鰓・卵に定着する。"
    cen = f"Caused by opportunistic water moulds (Saprolegnia) in {_en(sp)}; they colonise skin, gills or eggs damaged by trauma, low temperature, poor water quality or stress (cotton-wool disease)."
    pja = "菌糸が損傷表皮に綿毛状に増殖して表皮・鰓を破壊し、浸透圧調節障害と二次感染を招く。広範に及ぶと呼吸・体液平衡の破綻により致死的となる。"
    pen = "Hyphae grow as cotton-wool tufts over damaged epidermis, destroying skin and gills and causing osmoregulatory failure and secondary infection; extensive involvement is fatal through respiratory and fluid-balance collapse."
    return cja, cen, pja, pen


def _macrorhabdus(sp):
    j = _ja(sp)
    cja = f"{j}のマクロラブダス症（旧称メガバクテリア症・鳥胃酵母症）は酵母様真菌 Macrorhabdus ornithogaster の感染による。糞口感染で伝播し、セキセイインコ・フィンチで多い。"
    cen = f"Caused by the yeast-like fungus Macrorhabdus ornithogaster in {_en(sp)} (avian gastric yeast, formerly 'megabacteria'), transmitted faecal-orally and common in budgerigars and finches."
    pja = "菌が腺胃と筋胃の移行部（峡部）に定着して胃酸分泌と消化を障害し、慢性の体重減少・未消化便・嘔吐（「go light」症候群）を起こす。ストレス・免疫低下で顕在化する。"
    pen = "The organism colonises the isthmus between proventriculus and ventriculus, impairing acid secretion and digestion to cause chronic weight loss, undigested droppings and regurgitation ('going light'); it becomes clinical under stress or immunosuppression."
    return cja, cen, pja, pen


def _fungal_shell_disease(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の真菌性甲羅疾患は環境中の日和見真菌（Fusarium・Paecilomyces等）が甲羅の角質層・下床骨に感染することによる。外傷・不衛生な基質・過湿環境・免疫低下が誘因となる。"
    cen = f"Caused by opportunistic environmental fungi (Fusarium, Paecilomyces) infecting the keratinised shell layer and underlying bone in {e}; trauma, unsanitary substrate, excessive dampness and immunosuppression predispose."
    pja = "菌糸が損傷した角質層から侵入して角質下に壊死性病変を形成し、進行すると骨組織に達して深部の骨融解・敗血症を招く。細菌性の甲羅腐敗症より進行が緩徐だが、より深部に浸潤しやすく難治性となりやすい。"
    pen = "Hyphae invade through breached keratin, producing necrotic lesions beneath the shell surface; advanced disease reaches bone causing deep osteolysis and can progress to septicaemia. Progression is typically slower than bacterial shell rot but the fungus penetrates more deeply, making it more refractory to treatment."
    return cja, cen, pja, pen


def _pneumocystis(sp):
    j = _ja(sp)
    cja = f"{j}のニューモシスチス肺炎は真菌 Pneumocystis の感染による。基礎的な免疫不全（原発性免疫不全・免疫抑制療法）を背景に発症する日和見感染。"
    cen = f"Caused by the fungus Pneumocystis in {_en(sp)}, an opportunist that arises on a background of immunodeficiency (primary immune defects or immunosuppressive therapy)."
    pja = "菌が肺胞腔で増殖して泡沫状の滲出物を満たし、ガス交換を障害して進行性の呼吸困難・低酸素血症を起こす。免疫能の回復が治療の鍵となる。"
    pen = "The organism proliferates in alveolar spaces filling them with foamy exudate that impairs gas exchange, causing progressive dyspnoea and hypoxaemia; restoring immune competence is central to treatment."
    return cja, cen, pja, pen


# name-pattern -> generator. Collision-safe keys (see comments):
_AGENTS: tuple[tuple[tuple[str, ...], object], ...] = (
    # "coccidioidomyc"/"coccidioides" (never bare "coccidio" — protozoal coccidiosis).
    (("coccidioidomyc", "coccidioides", "コクシジオイデス", "渓谷熱", "valley fever"), _coccidioides),
    # "microsporum" (full — never "microspor", which hits microsporidia).
    (("皮膚糸状菌", "白癬", "dermatophyt", "ringworm", "microsporum", "trichophyton"), _dermatophyte),
    (("アスペルギル", "aspergill", "喉嚢真菌", "guttural pouch myco"), _aspergillus),
    (("カンジダ", "candid", "そ嚢真菌"), _candida),
    (("クリプトコッカス", "cryptococc"), _cryptococcus),
    (("マラセチア", "malassezia"), _malassezia),
    (("ヒストプラズマ", "histoplasm"), _histoplasma),
    (("ブラストミセス", "blastomyc"), _blastomyces),
    (("スポロトリックス", "スポロトリコーシス", "sporotri"), _sporothrix),
    (("接合菌", "ムコール", "mucor", "zygomyc", "rhizopus"), _mucor),
    (("ピシウム", "pythi"), _pythium),
    (("サプロレグニア", "水カビ", "綿かぶり", "saprolegni", "water mould", "water mold"), _saprolegnia),
    (("マクロラブダス", "メガバクテリア", "macrorhabdus", "avian gastric yeast"), _macrorhabdus),
    (("ニューモシスチス", "pneumocystis"), _pneumocystis),
    (("真菌性甲羅疾患", "fungal shell disease"), _fungal_shell_disease),
)


def resolve_fungal_agent(name_ja: str, name_en: str):
    """Return the generator for a named-pathogen fungal disease, or None.

    Negated names are neutralised first."""
    name = _neutralise_negations(f"{name_ja or ''} {name_en or ''}").lower()
    for keys, gen in _AGENTS:
        if any(k.lower() in name for k in keys):
            return gen
    return None


def fungal_clinical_fields(species: str, name_ja: str, name_en: str) -> dict | None:
    """Curated causes / pathophysiology (JA+EN) for a named-pathogen fungal
    disease, or None when the name does not resolve to a known fungus."""
    gen = resolve_fungal_agent(name_ja, name_en)
    if gen is None:
        return None
    cja, cen, pja, pen = gen((species or "").lower())
    return {
        "causes_ja": cja,
        "causes": cen,
        "pathophysiology_ja": pja,
        "pathophysiology": pen,
    }
