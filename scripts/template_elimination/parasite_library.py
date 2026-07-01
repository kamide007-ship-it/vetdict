"""Curated etiology / pathophysiology for named-parasite diseases.

Fourth companion to the pathogen libraries (viral / bacterial / fungal). Parasitic
diseases whose name identifies the parasite shipped the generic parasite category
template — JA ``「…の原因は寄生虫（蠕虫・原虫・節足動物）の感染である…」`` and English
``"Caused by parasites infecting affected tissues…"`` / ``"External parasite
infestation…"``. When the name names the parasite (roundworm, tapeworm,
heartworm, sarcoptic mange, coccidiosis …) the aetiology is a textbook fact,
curated with zero fabrication risk.

Generators return parasite-specific ``causes`` + ``pathophysiology`` (JA + EN).
Only category-template / stub fields are overwritten (curated flagship prose is
preserved). Intestinal protozoa (coccidia, giardia, trichomonas) are covered for
the *causes/pathophysiology* fields here; their *treatment* is handled separately
by ``antiprotozoal_library``.

References: Bowman, *Georgis' Parasitology for Veterinarians* 11th ed; ESCCAP
guidelines; Carpenter, *Exotic Animal Formulary* 6th ed; Noga, *Fish Disease*
2nd ed.
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


def _ja(sp: str) -> str:
    return SPECIES_JA.get(sp, sp)


def _en(sp: str) -> str:
    return SPECIES_EN.get(sp, sp)


# --- Nematodes (roundworms) ------------------------------------------------ #
def _ascarid(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の回虫症は消化管内寄生線虫（イヌ回虫 Toxocara canis／ネコ回虫 T. cati／馬回虫 Parascaris 等）による。虫卵の経口摂取、経乳・経胎盤感染、待機宿主の捕食で感染する。"
    cen = f"Caused by ascarid roundworms of {e} (Toxocara canis/cati, Parascaris in horses), acquired by ingesting embryonated eggs, transmammary/transplacental passage, or eating paratenic hosts."
    pja = "幼虫は体内移行（肝・肺）を経て小腸で成虫となり、栄養を奪って発育不良・腹部膨満・削痩・下痢を起こす。多数寄生では腸閉塞・腸穿孔を招き、幼虫移行はヒトの内臓幼虫移行症の原因ともなる。"
    pen = "Larvae migrate through liver and lung before maturing in the small intestine, competing for nutrients to cause poor growth, pot-belly, wasting and diarrhoea; heavy burdens obstruct or perforate the gut, and larval migration causes human visceral larva migrans."
    return cja, cen, pja, pen


def _hookworm(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の鉤虫症は吸血性線虫（Ancylostoma／Uncinaria）による。感染幼虫の経皮・経口侵入、経乳感染で伝播する。"
    cen = f"Caused by blood-feeding hookworms (Ancylostoma, Uncinaria) of {e}, via skin penetration or ingestion of infective larvae and transmammary passage."
    pja = "成虫が小腸粘膜に咬着して吸血し、失血性（再生性→非再生性）貧血・低蛋白血症・黒色タール便を起こす。幼虫の経皮侵入部では皮膚炎を、肺移行では咳を生じる。"
    pen = "Adults attach to the small-intestinal mucosa and suck blood, causing blood-loss anaemia (regenerative then non-regenerative), hypoproteinaemia and melaena; skin penetration causes dermatitis and lung migration causes cough."
    return cja, cen, pja, pen


def _whipworm(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の鞭虫症は大腸に寄生する線虫 Trichuris による。土壌中で長期間感染性を保つ虫卵の経口摂取で感染する。"
    cen = f"Caused by the large-intestinal whipworm Trichuris in {e}, acquired by ingesting eggs that remain infective in soil for years."
    pja = "成虫が盲腸・結腸粘膜に頭部を穿入して炎症・出血を起こし、粘血便・裏急後重・体重減少を生じる。重度感染では低ナトリウム・高カリウム血症（偽アジソン様）を呈することがある。"
    pen = "Adults thread their heads into the caecal/colonic mucosa causing inflammation and bleeding with mucohaemorrhagic diarrhoea, tenesmus and weight loss; heavy infection can cause a pseudo-Addisonian hyponatraemia/hyperkalaemia."
    return cja, cen, pja, pen


def _pinworm(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の蟯虫症は大腸に寄生する線虫（Oxyuris equi＝馬蟯虫、齧歯類では Syphacia／Aspiculuris 等）による。虫卵の経口摂取で感染する。"
    cen = f"Caused by pinworms (Oxyuris equi in horses; Syphacia/Aspiculuris in rodents) in {e}, acquired by ingesting eggs."
    pja = "雌成虫が肛門周囲に産卵する際の刺激で強い肛門掻痒を起こし、擦れによる尾根部の脱毛・皮膚炎（rat tail）を生じる。多くは病原性が低いが不快感と二次性皮膚炎が問題となる。"
    pen = "Females depositing eggs around the anus provoke intense perianal pruritus, leading to tail-base rubbing, alopecia and dermatitis ('rat tail'); pathogenicity is usually low but discomfort and secondary dermatitis are the main issues."
    return cja, cen, pja, pen


def _strongyle(sp):
    j = _ja(sp)
    cja = f"{j}の円虫症（ストロンギルス症）は大腸に寄生する線虫（大円虫 Strongylus、小円虫＝シアソストミン）による。虫卵で汚染された放牧地の草を介した経口感染で伝播する。"
    cen = f"Caused by strongyles (large Strongylus, small strongyles/cyathostomins) in {_en(sp)}, acquired by grazing pasture contaminated with infective larvae."
    pja = "大円虫幼虫は腸間膜動脈を移行して血栓・疝痛を、小円虫の被嚢幼虫は一斉出嚢時に重度の腸炎・低蛋白血症・削痩（幼若円虫症）を起こす。慢性の体重減少・被毛不良・疝痛の主要因となる。"
    pen = "Large-strongyle larvae migrate in the mesenteric arteries causing thrombosis and colic, while mass emergence of encysted small strongyles causes severe colitis, hypoproteinaemia and wasting (larval cyathostominosis) — a major cause of chronic weight loss and colic."
    return cja, cen, pja, pen


def _lungworm(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の肺虫症は気道・肺血管に寄生する線虫（Aelurostrongylus／Angiostrongylus／Oslerus 等）による。中間宿主（軟体動物）や待機宿主の摂取で感染する。"
    cen = f"Caused by lungworms (Aelurostrongylus, Angiostrongylus, Oslerus) of {e}, acquired by ingesting molluscan intermediate or paratenic hosts."
    pja = "成虫・幼虫が細気管支・肺実質・肺動脈に寄生して肉芽腫性・好酸球性の炎症を起こし、慢性咳・呼吸困難・運動不耐を生じる。Angiostrongylus では出血傾向・肺高血圧を伴うことがある。"
    pen = "Adults and larvae in bronchioles, lung parenchyma and pulmonary arteries provoke granulomatous/eosinophilic inflammation causing chronic cough, dyspnoea and exercise intolerance; Angiostrongylus can add coagulopathy and pulmonary hypertension."
    return cja, cen, pja, pen


def _capillaria(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の毛細線虫症（カピラリア症）は細長い線虫 Capillaria 属による。寄生部位により消化管型・呼吸器型・膀胱型があり、虫卵の経口摂取（一部ミミズを介する）で感染する。"
    cen = f"Caused by the fine threadworm Capillaria in {e}; depending on site it is enteric, respiratory or urinary, acquired by ingesting eggs (sometimes via earthworm hosts)."
    pja = "虫体が粘膜（腸・気道・膀胱上皮）に穿入して炎症を起こし、部位に応じて下痢・削痩、慢性咳・鼻汁、血尿・膀胱炎を生じる。鳥では上部消化管型が発育不良の原因となる。"
    pen = "The worms embed in mucosa (gut, airway or bladder epithelium) causing inflammation and, by site, diarrhoea/wasting, chronic cough/nasal discharge, or haematuria/cystitis; the upper-GI form stunts birds."
    return cja, cen, pja, pen


def _heartworm(sp):
    j = _ja(sp)
    if sp == "cat":
        cja = "猫の犬糸状虫症（フィラリア症）は Dirofilaria immitis の感染による。蚊の吸血で幼虫が伝播するが、猫は非好適宿主のため少数寄生でも重篤化する。"
        cen = "Caused by Dirofilaria immitis in cats, transmitted by mosquitoes; cats are non-permissive hosts, so even a few worms cause severe disease."
        pja = "未成熟虫・成虫が肺動脈・細動脈に到達し、強い血管・気道反応（HARD：heartworm-associated respiratory disease）を起こす。虫体死滅時に急性肺傷害・突然死を招くことがある。"
        pen = "Immature and adult worms reaching the pulmonary arteries provoke intense vascular and airway reactions (heartworm-associated respiratory disease); worm death can trigger acute lung injury and sudden death."
    else:
        cja = f"{j}の犬糸状虫症（フィラリア症）は Dirofilaria immitis の感染による。蚊の吸血により感染幼虫が体内に入り、成長して右心・肺動脈に寄生する。"
        cen = f"Caused by Dirofilaria immitis in {_en(sp)}, transmitted by mosquitoes; infective larvae mature and lodge in the right heart and pulmonary arteries."
        pja = "成虫が肺動脈・右心に寄生して肺動脈内膜の増殖・肺高血圧・右心不全を起こす。多数寄生では大静脈症候群（急性溶血・虚脱）を、虫体死滅時には肺血栓塞栓症を招く。"
        pen = "Adults in the pulmonary arteries and right heart cause proliferative endarteritis, pulmonary hypertension and right-sided heart failure; heavy burdens cause caval syndrome (acute haemolysis, collapse) and worm death causes pulmonary thromboembolism."
    return cja, cen, pja, pen


# --- Cestodes / acanthocephalans ------------------------------------------ #
def _tapeworm(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の条虫症は消化管内寄生の条虫（Dipylidium・Taenia・Echinococcus・Anoplocephala 等）による。中間宿主（ノミ・小哺乳類・ダニ）の摂取で感染する。"
    cen = f"Caused by tapeworms (Dipylidium, Taenia, Echinococcus, Anoplocephala) of {e}, acquired by ingesting the intermediate host (fleas, small mammals, forage mites)."
    pja = "成虫が小腸粘膜に付着して栄養を奪い、片節排出による肛門掻痒・軽度消化器症状を起こす。馬 Anoplocephala は回盲部で疝痛・腸重積を、Echinococcus は中間宿主で致死的な包虫症（人獣共通）を招く。"
    pen = "Adults attach to the small-intestinal mucosa and compete for nutrients, causing proglottid-related perianal irritation and mild GI signs; equine Anoplocephala causes ileocaecal colic/intussusception, and Echinococcus causes fatal hydatid disease in intermediate hosts (a zoonosis)."
    return cja, cen, pja, pen


def _acanthocephala(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の鉤頭虫症は腸に寄生する鉤頭虫（Acanthocephala）による。中間宿主（節足動物）の摂取で感染する。"
    cen = f"Caused by thorny-headed worms (Acanthocephala) in {e}, acquired by ingesting arthropod intermediate hosts."
    pja = "虫体が吻の鉤で腸壁に深く穿入して局所の炎症・肉芽腫・穿孔を起こし、腸炎・体重減少・腹膜炎を生じる。深部穿入のため治療抵抗性のことがある。"
    pen = "The worm anchors its hooked proboscis deep in the intestinal wall causing focal inflammation, granuloma and perforation with enteritis, weight loss and peritonitis; deep attachment can make it refractory to treatment."
    return cja, cen, pja, pen


# --- Trematodes ------------------------------------------------------------ #
def _fluke(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の吸虫症（肝蛭症等）は扁形動物の吸虫（Fasciola・Platynosomum・Paragonimus・Schistosoma 等）による。中間宿主の巻貝を経た被嚢幼虫を、水草・生の魚介・甲殻類等とともに摂取して感染する。"
    cen = f"Caused by trematode flukes (Fasciola, Platynosomum, Paragonimus, Schistosoma) in {e}, acquired by ingesting encysted metacercariae on vegetation or in raw fish/crustaceans after a snail intermediate host."
    pja = "寄生部位（肝・胆管・肺・門脈）で虫体が慢性炎症・線維化・胆管閉塞を起こし、黄疸・肝障害・慢性咳・削痩を生じる。肝蛭では胆管肥厚・胆管炎を、住血吸虫では門脈系の肉芽腫性病変を招く。"
    pen = "At their site (liver, bile ducts, lung, portal veins) the flukes cause chronic inflammation, fibrosis and biliary obstruction with icterus, hepatopathy, chronic cough and wasting; Fasciola thickens bile ducts (cholangitis) and Schistosoma causes portal granulomas."
    return cja, cen, pja, pen


# --- Intestinal protozoa (causes/pathophysiology only) --------------------- #
def _coccidia(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のコクシジウム症は腸上皮に寄生する原虫（Cystoisospora／Eimeria 等）による。糞便中のオーシストの経口摂取で感染し、過密・不衛生・ストレス・幼齢で発症しやすい。"
    cen = f"Caused by intestinal coccidian protozoa (Cystoisospora, Eimeria) in {e}, acquired by ingesting sporulated oocysts in faeces; crowding, poor hygiene, stress and young age predispose."
    pja = "原虫が腸上皮細胞内で無性・有性生殖を繰り返して上皮を破壊し、水様〜血様下痢・脱水・発育不良を起こす。免疫が未熟な幼若動物で重症化し、二次感染を伴う。"
    pen = "The protozoa undergo asexual and sexual reproduction within enterocytes, destroying the epithelium to cause watery to bloody diarrhoea, dehydration and poor growth; disease is most severe in immunologically naïve young animals with secondary infection."
    return cja, cen, pja, pen


def _giardia(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のジアルジア症は鞭毛虫 Giardia の栄養型・シストによる。糞口感染（汚染された水・環境のシスト摂取）で伝播し、多頭飼育・幼若で多い人獣共通感染症。"
    cen = f"Caused by the flagellate Giardia (trophozoites and cysts) in {e}, transmitted faecal-orally via cysts in contaminated water/environment — a zoonosis common in the young and in group housing."
    pja = "栄養型が小腸微絨毛に付着して吸収面を障害し、微絨毛の萎縮・二糖類分解酵素低下により吸収不良性・脂肪性の慢性〜間欠性下痢を起こす。全身状態は比較的保たれることが多い。"
    pen = "Trophozoites carpet the small-intestinal microvilli impairing the absorptive surface; microvillous atrophy and reduced disaccharidases produce malabsorptive, fatty, chronic-intermittent diarrhoea, usually with a preserved general condition."
    return cja, cen, pja, pen


def _trichomonas(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のトリコモナス症は鞭毛虫 Trichomonas／Tritrichomonas による。鳥では上部消化管（そ嚢・口腔）、猫・牛では腸管・生殖器に寄生し、直接接触・共有の水/餌を介して伝播する。"
    cen = f"Caused by the flagellates Trichomonas/Tritrichomonas in {e}; in birds it colonises the upper GI tract (crop, oropharynx), in cats/cattle the intestine or reproductive tract, spread by direct contact and shared food/water."
    pja = "原虫が粘膜表面で増殖して炎症・壊死を起こす。鳥では口腔・そ嚢に乾酪様の黄色プラーク（canker/frounce）を形成して摂食困難を、猫では大腸炎による難治性下痢を生じる。"
    pen = "The protozoa proliferate on the mucosal surface causing inflammation and necrosis — caseous yellow plaques in the avian mouth/crop (canker/frounce) that impede feeding, and a refractory large-bowel diarrhoea in cats."
    return cja, cen, pja, pen


# --- Ectoparasites --------------------------------------------------------- #
def _mite(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のダニ症（疥癬・毛包虫症等）は皮膚に寄生するダニ（Sarcoptes・Notoedres・Demodex・Otodectes・Cheyletiella・Psoroptes・Trixacarus 等）による。多くは直接接触で伝播する。"
    cen = f"Caused by parasitic mites of {e} (Sarcoptes, Notoedres, Demodex, Otodectes, Cheyletiella, Psoroptes, Trixacarus); most spread by direct contact (mange/acariasis)."
    pja = "疥癬類は表皮内に穿孔してアレルギー性の激しい掻痒・痂皮・脱毛を、毛包虫は毛包内で増殖して膿皮症を伴う脱毛を、耳ダニは外耳道で耳垢増生・外耳炎を起こす。掻破による二次感染を伴いやすい。"
    pen = "Burrowing mites (Sarcoptes/Notoedres) provoke intense allergic pruritus, crusting and alopecia; Demodex proliferates in follicles causing alopecia with secondary pyoderma; ear mites (Otodectes) cause ceruminous otitis — all prone to self-trauma and secondary infection."
    return cja, cen, pja, pen


def _tick(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のマダニ寄生症は吸血性の外部寄生虫マダニ（Ixodes・Rhipicephalus・Haemaphysalis・Dermacentor 等）による。草むら等で宿主に付着して吸血する。"
    cen = f"Caused by blood-feeding ixodid ticks (Ixodes, Rhipicephalus, Haemaphysalis, Dermacentor) attaching to {e} from vegetation."
    pja = "吸血による局所の炎症・貧血に加え、唾液毒素による上行性弛緩性麻痺（tick paralysis）を起こしうる。さらに多数の病原体（バベシア・エールリヒア・ライム病・ヘパトゾーン等）を媒介する点が重要。"
    pen = "Beyond local inflammation and blood-loss anaemia, salivary toxins can cause ascending flaccid paralysis (tick paralysis); crucially, ticks vector numerous pathogens (Babesia, Ehrlichia, Borrelia, Hepatozoon)."
    return cja, cen, pja, pen


def _flea(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のノミ寄生症は吸血性昆虫ノミ（Ctenocephalides felis 等）による。環境中の幼虫・蛹から成虫が宿主に飛び移って寄生する。"
    cen = f"Caused by blood-feeding fleas (chiefly Ctenocephalides felis) infesting {e}, adults emerging from environmental larvae/pupae onto the host."
    pja = "吸血による掻痒に加え、唾液抗原に対する過敏反応でノミアレルギー性皮膚炎（腰背部・尾根部の脱毛・湿疹）を起こす。多数寄生の幼若・小型動物では失血性貧血を、瓜実条虫の媒介源ともなる。"
    pen = "Beyond bite pruritus, hypersensitivity to flea salivary antigen causes flea-allergy dermatitis (dorsolumbar/tail-base alopecia and dermatitis); heavy burdens cause blood-loss anaemia in small/young animals, and fleas transmit Dipylidium tapeworm."
    return cja, cen, pja, pen


def _louse(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のシラミ・羽虫寄生症（ペディクロシス）は宿主特異的な吸血シラミまたは咬毛（羽）虫による。直接接触で伝播し、密飼い・不衛生・衰弱個体で増える。"
    cen = f"Caused by host-specific sucking lice or chewing (biting) lice/feather lice on {e}, spread by direct contact and increasing with crowding, poor hygiene and debilitation."
    pja = "吸血シラミは掻痒・失血性貧血を、咬毛虫は皮膚・羽毛の損傷と掻痒を起こし、擦れによる脱毛・被毛/羽毛不良・不穏を生じる。全生活史を宿主上で完結するため接触で容易に広がる。"
    pen = "Sucking lice cause pruritus and blood-loss anaemia while chewing lice damage skin, hair and feathers; rubbing causes alopecia, poor coat/plumage and restlessness, and because the whole life cycle is on the host, infestation spreads readily by contact."
    return cja, cen, pja, pen


def _myiasis(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のハエ幼虫症（蠅蛆症・myiasis）はハエの幼虫（ウジ）が生体組織に寄生することによる。汚れた被毛・創傷・下痢による皮膚汚染にハエが産卵して発生する。"
    cen = f"Caused by fly larvae (maggots) infesting the living tissue of {e}; flies oviposit on skin soiled by wounds, diarrhoea or matted coat (myiasis)."
    pja = "孵化した幼虫が組織を融解・摂食して急速に拡大する潰瘍・壊死を作り、毒素吸収と二次感染により全身状態が急速に悪化してショック・死に至ることがある。衰弱・不潔・被毛の長い個体で好発する。"
    pen = "Hatched larvae liquefy and consume tissue creating rapidly enlarging ulcers and necrosis; toxin absorption and secondary infection can cause rapid deterioration, shock and death, especially in debilitated, soiled or long-coated animals."
    return cja, cen, pja, pen


# --- Fish/aquatic parasites ------------------------------------------------ #
def _ich(sp):
    j = _ja(sp)
    cja = f"{j}の白点病は繊毛虫（淡水 Ichthyophthirius multifiliis／海水 Cryptocaryon irritans）による。水中の遊走子（セロント）が魚体表・鰓に侵入して発症し、水質悪化・低水温・過密で多発する。"
    cen = f"Caused by ciliate protozoa (freshwater Ichthyophthirius multifiliis / marine Cryptocaryon irritans) in {_en(sp)}; free-swimming theronts invade the skin and gills, favoured by poor water quality, low temperature and crowding."
    pja = "虫体が上皮下に侵入・被嚢して特徴的な白点を形成し、上皮・鰓を破壊して浸透圧調節障害・呼吸障害を起こす。鰓障害は致死的で、増殖が速いため水槽全体に急速に蔓延する。"
    pen = "The parasite burrows under the epithelium and encysts forming the characteristic white spots, destroying skin and gills to cause osmoregulatory and respiratory failure; gill involvement is lethal and the fast life cycle spreads it rapidly through a tank."
    return cja, cen, pja, pen


def _monogenean(sp):
    j = _ja(sp)
    cja = f"{j}の単生虫症（ギロダクチルス・ダクチロギルス症）は体表・鰓に寄生する単生類吸虫による。直接生活史で中間宿主を要さず、過密・水質悪化の水槽で急増する。"
    cen = f"Caused by monogenean flukes (Gyrodactylus on skin, Dactylogyrus on gills) in {_en(sp)}; with a direct life cycle needing no intermediate host, they multiply rapidly in crowded, poor-quality water."
    pja = "固着器の鉤で体表・鰓上皮に付着・摂食して過剰な粘液分泌・上皮増生・出血を起こし、体表の擦り付け行動・鰓の呼吸障害・二次感染を招く。"
    pen = "Anchoring by opisthaptor hooks, they feed on skin and gill epithelium causing excess mucus, epithelial hyperplasia and haemorrhage, with flashing behaviour, gill respiratory compromise and secondary infection."
    return cja, cen, pja, pen


def _crustacean_parasite(sp):
    j = _ja(sp)
    cja = f"{j}の甲殻類寄生症（イカリムシ症・ウオジラミ症）は寄生性甲殻類（Lernaea＝イカリムシ／Argulus＝ウオジラミ）による。導入魚や水を介して持ち込まれる。"
    cen = f"Caused by parasitic crustaceans (Lernaea anchor worm / Argulus fish louse) in {_en(sp)}, introduced with new fish or water."
    pja = "イカリムシは頭部を筋肉に埋入して潰瘍・二次感染を、ウオジラミは体表に付着・吸血して刺傷・炎症・擦り付けを起こす。刺傷部が細菌・真菌の侵入門戸となる。"
    pen = "Lernaea embeds its head in muscle causing ulcers and secondary infection, while Argulus attaches and feeds on the surface causing puncture wounds, inflammation and flashing; the wounds are portals for bacterial and fungal invasion."
    return cja, cen, pja, pen


# name-pattern -> generator. Order: specific first. Collision notes inline.
_AGENTS: tuple[tuple[tuple[str, ...], object], ...] = (
    # Fish "white spot": full names only — never bare "ich" (would hit itch/which).
    (("ichthyophthirius", "cryptocaryon", "白点病", "white spot"), _ich),
    (("gyrodactylus", "dactylogyrus", "ギロダクチルス", "ダクチロギルス", "単生虫", "monogene"), _monogenean),
    (("lernaea", "イカリムシ", "argulus", "ウオジラミ", "anchor worm", "fish louse"), _crustacean_parasite),
    (("heartworm", "dirofilaria", "フィラリア", "犬糸状虫"), _heartworm),
    (("回虫", "roundworm", "ascari", "toxocar", "parascaris"), _ascarid),
    (("鉤虫", "hookworm", "ancylostoma", "uncinaria"), _hookworm),
    (("鞭虫", "whipworm", "trichuris"), _whipworm),
    (("蟯虫", "pinworm", "oxyuris", "syphacia", "aspiculuris"), _pinworm),
    (("円虫", "strongyle", "strongylus", "cyathostom"), _strongyle),
    (("肺虫", "lungworm", "aelurostrongylus", "angiostrongylus", "oslerus"), _lungworm),
    (("毛細線虫", "カピラリア", "capillaria"), _capillaria),
    # "エキノコックス"/"hydatid"/"echinococc" — never bare "包虫" (would hit
    # 毛包虫症 = demodicosis, a mite disease).
    (
        (
            "条虫",
            "tapeworm",
            "cestode",
            "dipylidium",
            "taenia",
            "echinococc",
            "エキノコックス",
            "hydatid",
            "anoplocephala",
        ),
        _tapeworm,
    ),
    (("鉤頭虫", "acanthocephal"), _acanthocephala),
    (("吸虫", "肝蛭", "fluke", "trematode", "fasciola", "paragonimus", "schistosom", "platynosomum"), _fluke),
    (("コクシジウム", "球虫", "coccidiosis", "eimeria", "isospora", "cystoisospora"), _coccidia),
    (("ジアルジア", "giardia", "ランブル鞭毛虫"), _giardia),
    (("トリコモナス", "trichomonas", "canker", "frounce"), _trichomonas),
    # Ectoparasites. "疥癬"/"mange"/named genera — bare "mite"/"ダニ" last so a
    # specific parasite matches first; "mite" is safe under the template gate.
    (
        (
            "疥癬",
            "毛包虫",
            "ニキビダニ",
            "ミミヒゼンダニ",
            "耳ダニ",
            "mange",
            "sarcopt",
            "notoedres",
            "demodex",
            "demodicosis",
            "otodectes",
            "cheyletiella",
            "psoropt",
            "trixacarus",
            "ダニ症",
            "mite",
            "acariasis",
        ),
        _mite,
    ),
    (
        ("マダニ", "ixodes", "rhipicephalus", "haemaphysalis", "dermacentor", "tick infestation", "tick paralysis"),
        _tick,
    ),
    (("ノミ", "flea", "ctenocephalides"), _flea),
    # "louse"/"pediculosis"/JA — never bare "lice" (would hit police/slice).
    (("シラミ", "羽虫", "louse", "pediculosis", "mallophaga", "trichodectes"), _louse),
    (("ハエ幼虫", "蠅蛆", "ウジ", "myiasis", "screwworm", "botfly", "cuterebra", "maggot"), _myiasis),
)


def resolve_parasite_agent(name_ja: str, name_en: str):
    """Return the generator for a named-parasite disease, or None.

    Negated names are neutralised first."""
    name = _neutralise_negations(f"{name_ja or ''} {name_en or ''}").lower()
    for keys, gen in _AGENTS:
        if any(k.lower() in name for k in keys):
            return gen
    return None


def parasite_clinical_fields(species: str, name_ja: str, name_en: str) -> dict | None:
    """Curated causes / pathophysiology (JA+EN) for a named-parasite disease, or
    None when the name does not resolve to a known parasite."""
    gen = resolve_parasite_agent(name_ja, name_en)
    if gen is None:
        return None
    cja, cen, pja, pen = gen((species or "").lower())
    return {
        "causes_ja": cja,
        "causes": cen,
        "pathophysiology_ja": pja,
        "pathophysiology": pen,
    }
