"""Curated antiprotozoal protocols for protozoal diseases mis-templated as helminth infections.

Forty protozoal disease records (babesiosis, toxoplasmosis, leishmaniosis,
hepatozoonosis, cytauxzoonosis, encephalitozoonosis, coccidiosis, sarcocystosis,
atoxoplasmosis, leucocytozoonosis, avian malaria) carry the generic *deworming*
treatment template:

    "…同定された寄生虫に応じた適切な駆虫薬が必要である。…全てのライフステージを
     排除するため複数回投与が必要…"

That template is clinically wrong for protozoa. Anthelmintics ("駆虫薬") do not
treat intra-erythrocytic, tissue, or intracellular protozoa — these require
*antiprotozoal* chemotherapy (imidocarb, atovaquone/azithromycin, clindamycin,
allopurinol + meglumine antimoniate / miltefosine, sulfadimethoxine, ponazuril /
toltrazuril, fenbendazole specifically for microsporidian *Encephalitozoon*).
Telling a clinician to give a dewormer for babesiosis or cytauxzoonosis is a
credibility-damaging error.

Each protozoal agent is given an evidence-based, species-aware treatment and a
pathogen-specific pathophysiology, in Japanese and English. The mechanism of the
drug is species-independent (imidocarb clears *Babesia* in any host), but the
host-specific realities (feline babesiosis responds poorly to imidocarb; small
vs. large *Babesia*; American vs. Old-World hepatozoonosis; *E. cuniculi*
needing the benzimidazole fenbendazole rather than an antiprotozoal) are written
into the text.

References: Solano-Gallego et al. *Parasit Vectors* 2016 (canine babesiosis,
ESCCAP); LeishVet guidelines (Solano-Gallego 2011); Dubey & Lappin, ACVIM
toxoplasmosis consensus; Baneth, *Vet Parasitol* (hepatozoonosis); Cohn & Birkenheuer
(cytauxzoonosis, *J Vet Intern Med* 2011); Künzel & Fisher *Vet Clin Exot* 2018
(E. cuniculi); Carpenter, *Exotic Animal Formulary* 6th ed; Greene, *Infectious
Diseases of the Dog and Cat* 4th ed.
"""

from __future__ import annotations

# Only records carrying this deworming fingerprint are candidates for correction.
DEWORM_SIG = "同定された寄生虫に応じた適切な駆虫薬"

# Non-curated pathophysiology stubs that may be overwritten with pathogen-specific
# prose. These supplement the category-template fingerprints and STUB_SIGNATURES:
# a generic "important disease caused by parasites" stub, the catch-all parasite
# list, and a renal-template fragment that was mis-applied to protozoal diseases
# (e.g. feline leishmaniosis given "progressive nephron loss"). Genuine curated
# pathophysiology (which names the pathogen — Babesia, Toxoplasma gondii,
# Cytauxzoon felis, Encephalitozoon cuniculi) contains none of these.
PATHO_JA_STUB_MARKS: tuple[str, ...] = (
    "臨床的に重要な疾患で",
    "寄生虫（線虫・条虫・吸虫・原虫",
    "ネフロンの進行性損傷",
)

# English parasite/stub pathophysiology markers (the EN overlay carries its own
# boilerplate, independent of the JA text).
PATHO_EN_STUB_MARKS: tuple[str, ...] = (
    "pathophysiology of parasitic diseases",
    "pathophysiology depends on the parasite",
    "is a clinically important",
    "progressive loss of functional nephrons",
)

# Species display names (Japanese) for weaving into prose.
_SPECIES_JA = {
    "dog": "犬",
    "cat": "猫",
    "horse": "馬",
    "rabbit": "ウサギ",
    "ferret": "フェレット",
    "guinea_pig": "モルモット",
    "chinchilla": "チンチラ",
    "degu": "デグー",
    "hamster": "ハムスター",
    "hedgehog": "ハリネズミ",
    "sugar_glider": "フクロモモンガ",
    "bird": "鳥",
    "parakeet": "インコ",
    "parrot": "オウム",
    "reptile": "爬虫類",
    "tortoise": "リクガメ",
    "snake": "ヘビ",
    "lizard": "トカゲ",
    "amphibian": "両生類",
    "fish": "魚",
    "exotic_other": "エキゾチックアニマル",
}

_MAMMALS = frozenset(
    {
        "dog",
        "cat",
        "horse",
        "rabbit",
        "ferret",
        "guinea_pig",
        "chinchilla",
        "degu",
        "hamster",
        "hedgehog",
        "sugar_glider",
        "exotic_other",
    }
)
_BIRDS = frozenset({"bird", "parakeet", "parrot"})


def _sp_ja(species: str) -> str:
    return _SPECIES_JA.get(species, "本種")


# --- per-agent generators -------------------------------------------------
# Each returns (treatment_ja, treatment_en, patho_ja, patho_en).


def _babesia(species: str):
    sp = _sp_ja(species)
    if species == "cat":
        tx_ja = (
            f"{sp}のバベシア症（主にBabesia felis）は抗原虫薬で治療する。第一選択はプリマキンリン酸塩"
            "0.5 mg/kg PO/IM単回（治療域が狭く過量で致死的となるため厳密な用量管理が必須）。"
            "イミドカルブやジミナゼンは犬ほど有効でないことが多い。重度貧血には全血または濃厚赤血球輸血、"
            "等張晶質液による輸液、酸素化の維持を行う。再発・キャリア化が多いため治療後もPCR/塗抹で経過観察する。"
        )
        tx_en = (
            "Feline babesiosis (chiefly Babesia felis) requires antiprotozoal therapy. First-line is "
            "primaquine phosphate 0.5 mg/kg PO/IM once (narrow margin — overdose is fatal, so dose "
            "precisely); imidocarb and diminazene are often less effective than in dogs. Transfuse "
            "whole blood/pRBC for severe anaemia, give isotonic crystalloids, and monitor by smear/PCR "
            "for relapse and the carrier state."
        )
    else:
        tx_ja = (
            f"{sp}のバベシア症は原因種で治療が分かれる。大型バベシア（B. canis/vogeli）にはイミドカルブ"
            "ジプロピオン酸塩6.6 mg/kg IM/SCを2週間隔で2回投与（投与前にアトロピンでコリン作動性副作用を軽減）。"
            "小型バベシア（B. gibsoni）にはアトバコン13.3 mg/kg PO q8h＋アジスロマイシン10 mg/kg PO q24hを10日間。"
            "重度溶血性貧血には輸血、ショックには輸液、必要に応じ短期コルチコステロイド。"
            "治療後もPCRで原虫消失を確認し、マダニ予防を徹底する。"
        )
        tx_en = (
            "Treatment depends on the species. Large Babesia (B. canis/vogeli): imidocarb dipropionate "
            "6.6 mg/kg IM/SC, two doses 14 days apart (pre-treat with atropine for cholinergic effects). "
            "Small Babesia (B. gibsoni): atovaquone 13.3 mg/kg PO q8h + azithromycin 10 mg/kg PO q24h "
            "for 10 days. Transfuse for severe haemolytic anaemia, give fluids for shock, and confirm "
            "clearance by PCR; enforce tick prophylaxis."
        )
    patho_ja = (
        f"バベシアはマダニの吸血により{sp}の赤血球内に侵入・分裂増殖する原虫で、感染赤血球の破壊（血管内・"
        "血管外溶血）と免疫介在性赤血球破壊により再生性貧血・ヘモグロビン尿・黄疸を生じる。重症例では全身性"
        "炎症反応・低血圧・多臓器障害（急性腎障害、脳バベシア症）に進展する。"
    )
    patho_en = (
        "Babesia is a tick-transmitted intra-erythrocytic protozoan; parasitised red cells are destroyed "
        "by intra/extravascular and immune-mediated haemolysis, producing regenerative anaemia, "
        "haemoglobinuria and icterus, with SIRS, hypotension and multi-organ injury (AKI, cerebral "
        "babesiosis) in severe disease."
    )
    return tx_ja, tx_en, patho_ja, patho_en


def _toxoplasma(species: str):
    sp = _sp_ja(species)
    if species in _BIRDS:
        tx_ja = (
            f"{sp}のトキソプラズマ症にはサルファ剤＋ピリメタミンの併用が用いられるが、鳥では中毒域が狭く"
            "支持療法が中心となる。脱水・削痩・神経症状に対する輸液・強制給餌・保温を行い、"
            "確定診断（血清抗体・PCR）に基づき治療する。"
        )
        tx_en = (
            "Avian toxoplasmosis is treated with potentiated sulfonamides plus pyrimethamine, but the "
            "narrow toxic margin in birds means supportive care predominates: fluids, assisted feeding "
            "and warmth, guided by serology/PCR."
        )
    else:
        tx_ja = (
            f"{sp}のトキソプラズマ症の第一選択はクリンダマイシン10-12.5 mg/kg PO q12hを4週間。"
            "代替としてトリメトプリム・サルファ15 mg/kg PO q12h±ピリメタミン。眼・神経・肺症状には"
            "対応する支持療法を併用する。妊娠動物・免疫抑制例では特に早期治療が重要。"
            "クリンダマイシンは下痢を起こしうるため草食動物では慎重に。"
        )
        tx_en = (
            "First-line is clindamycin 10-12.5 mg/kg PO q12h for 4 weeks; alternatives are "
            "trimethoprim-sulfa 15 mg/kg PO q12h +/- pyrimethamine. Add organ-directed supportive care "
            "for ocular, neurological or pulmonary involvement; treat pregnant or immunosuppressed "
            "animals early."
        )
    patho_ja = (
        f"トキソプラズマ・ゴンディは終宿主のネコ科で有性生殖し、オーシスト経口摂取または組織内シストの摂取で"
        f"{sp}に感染する。タキゾイトが細胞内で増殖し組織壊死（脳・肺・肝・眼・筋）を起こし、免疫により"
        "ブラディゾイトの組織シストとして潜伏する。免疫抑制で再活性化し全身性疾患を生じる。"
    )
    patho_en = (
        "Toxoplasma gondii reproduces sexually in felid definitive hosts; other hosts acquire it via "
        "oocysts or tissue cysts. Tachyzoites replicate intracellularly causing tissue necrosis (CNS, "
        "lung, liver, eye, muscle), then persist as bradyzoite cysts that reactivate under "
        "immunosuppression to cause systemic disease."
    )
    return tx_ja, tx_en, patho_ja, patho_en


def _leishmania(species: str):
    sp = _sp_ja(species)
    tx_ja = (
        f"{sp}のリーシュマニア症は根治が難しく長期管理を要する。標準はメグルミンアンチモン酸75-100 mg/kg "
        "SC q24h（4-8週）またはミルテホシン2 mg/kg PO q24h（28日）に、アロプリノール10 mg/kg PO q12hを"
        "数か月〜年単位で併用する。腎障害（蛋白漏出性腎症）の評価とモニタリングが必須で、"
        "重度腎症では予後が悪い。臨床的寛解は得られても寄生虫学的治癒は稀で再発に注意する。"
    )
    tx_en = (
        "Canine leishmaniosis is rarely cured and needs long-term management. Standard protocols pair "
        "meglumine antimoniate 75-100 mg/kg SC q24h (4-8 wk) or miltefosine 2 mg/kg PO q24h (28 d) "
        "with allopurinol 10 mg/kg PO q12h for months to years. Stage and monitor renal disease "
        "(protein-losing nephropathy); severe nephropathy carries a poor prognosis, and clinical "
        "remission seldom equals parasitological cure, so watch for relapse."
    )
    patho_ja = (
        f"リーシュマニアはサシチョウバエの吸血で{sp}に感染し、マクロファージ内でアマスティゴートとして増殖する"
        "細胞内原虫である。免疫応答の型（Th1で抑制、Th2で進行）が転帰を左右し、免疫複合体沈着による"
        "糸球体腎炎・多発性関節炎・ぶどう膜炎、皮膚潰瘍・鼻鏡脱色素・リンパ節腫大を生じる。"
    )
    patho_en = (
        "Leishmania is a sandfly-transmitted intracellular protozoan that multiplies as amastigotes "
        "within macrophages. Outcome hinges on the immune phenotype (Th1 controls, Th2 progresses); "
        "immune-complex deposition drives glomerulonephritis, polyarthritis and uveitis, with "
        "cutaneous ulceration, nasal depigmentation and lymphadenomegaly."
    )
    return tx_ja, tx_en, patho_ja, patho_en


def _hepatozoon(species: str):
    sp = _sp_ja(species)
    tx_ja = (
        f"{sp}のヘパトゾーン症は原因種で治療が異なる。H. canis感染にはイミドカルブジプロピオン酸塩5-6 mg/kg "
        "IM/SCを2週間隔で原虫血症が消失するまで反復。アメリカ型（H. americanum）にはTMS＋クリンダマイシン＋"
        "ピリメタミンの三剤併用（TCP）を14日、続いてデコキネート10-20 mg/kg PO q12hを長期投与し再発を抑制する。"
        "疼痛・発熱・削痩に対する支持療法とマダニ駆除を併用する。"
    )
    tx_en = (
        "Treatment depends on the species. H. canis: imidocarb dipropionate 5-6 mg/kg IM/SC every 14 "
        "days until parasitaemia clears. American canine hepatozoonosis (H. americanum): the TCP combo "
        "(trimethoprim-sulfa + clindamycin + pyrimethamine) for 14 days, then long-term decoquinate "
        "10-20 mg/kg PO q12h to suppress relapse, plus analgesia, supportive care and tick control."
    )
    patho_ja = (
        f"ヘパトゾーンは感染マダニの捕食・摂取で{sp}に感染する原虫で、腸管から実質臓器・筋・骨に播種する。"
        "H. americanumは筋・骨膜に重度の化膿性肉芽腫性炎症を起こし、激しい疼痛・歩様異常・骨膜増殖・"
        "好中球増多をきたす。H. canisは脾・骨髄・リンパ節を侵し貧血・削痩を生じる。"
    )
    patho_en = (
        "Hepatozoon is acquired by ingesting infected ticks; it disseminates from the gut to parenchymal "
        "organs, muscle and bone. H. americanum incites severe pyogranulomatous myositis/periostitis with "
        "intense pain, gait abnormality, periosteal proliferation and marked neutrophilia; H. canis "
        "targets spleen, marrow and nodes, causing anaemia and wasting."
    )
    return tx_ja, tx_en, patho_ja, patho_en


def _cytauxzoon(species: str):
    sp = _sp_ja(species)
    tx_ja = (
        f"{sp}のサイトークスゾーン症（Cytauxzoon felis）は致死率が高く、迅速な抗原虫薬と集中支持療法を要する。"
        "アトバコン15 mg/kg PO q8h＋アジスロマイシン10 mg/kg PO q24hを10日間（最も生存率が高い）。"
        "積極的な静脈内輸液、ヘパリンによる血栓予防、貧血には輸血、疼痛管理、栄養補給を行う。"
        "ジミナゼン/イミダカルブも用いられるが有効性は限定的。マダニ予防が最重要。"
    )
    tx_en = (
        "Cytauxzoonosis (Cytauxzoon felis) is highly lethal and needs prompt antiprotozoal therapy plus "
        "intensive support. Atovaquone 15 mg/kg PO q8h + azithromycin 10 mg/kg PO q24h for 10 days gives "
        "the best survival. Provide aggressive IV fluids, heparin for thrombosis, transfusion for "
        "anaemia, analgesia and nutritional support; imidocarb/diminazene are less effective. Tick "
        "prevention is paramount."
    )
    patho_ja = (
        f"Cytauxzoon felisはマダニ媒介で{sp}に感染し、シゾント期にマクロファージが血管内で巨大化・増殖して"
        "全身の血管を閉塞（特に肺・肝・脾・リンパ節）し、続いて赤血球内ピロプラズム期で溶血を起こす。"
        "高熱・呼吸困難・黄疸・DIC・ショックへ急速に進展する。"
    )
    patho_en = (
        "Cytauxzoon felis is tick-transmitted; the schizogenous phase fills and enlarges macrophages that "
        "occlude vessels throughout the body (lung, liver, spleen, nodes), followed by an erythrocytic "
        "piroplasm phase causing haemolysis, with rapid progression to high fever, dyspnoea, icterus, "
        "DIC and shock."
    )
    return tx_ja, tx_en, patho_ja, patho_en


def _encephalitozoon(species: str):
    sp = _sp_ja(species)
    tx_ja = (
        f"{sp}のエンセファリトゾーン症（Encephalitozoon cuniculi）にはベンズイミダゾール系のフェンベンダゾール"
        "20 mg/kg PO q24hを28日間投与する（胞子形成を抑制し再発を減らす）。前庭症状・炎症には"
        "メロキシカム0.3-0.5 mg/kg PO q24hなどの抗炎症薬、斜頸・眼振による摂食低下には強制給餌・輸液・"
        "保温・パッド付き環境を提供する。腎型・眼型では各臓器の支持療法を併用する。"
    )
    tx_en = (
        "Encephalitozoon cuniculi is treated with the benzimidazole fenbendazole 20 mg/kg PO q24h for "
        "28 days (suppresses spore formation, reduces relapse). Add anti-inflammatories (meloxicam "
        "0.3-0.5 mg/kg PO q24h) for vestibular inflammation, and supportive care — assisted feeding, "
        "fluids, warmth and padded housing — for head tilt/nystagmus; treat the renal or ocular forms "
        "with organ-directed support."
    )
    patho_ja = (
        f"E. cuniculiは偏性細胞内の微胞子虫で、経口・経胎盤感染後に胞子が腎・脳・水晶体に播種する。"
        f"{sp}では肉芽腫性脳炎（斜頸・眼振・運動失調）、肉芽腫性間質性腎炎、水晶体破裂による白内障性ぶどう膜炎"
        "を生じる。宿主免疫が低下すると潜伏感染が再活性化する。"
    )
    patho_en = (
        "E. cuniculi is an obligate intracellular microsporidian; after oral/transplacental infection, "
        "spores disseminate to kidney, brain and lens, producing granulomatous encephalitis (head tilt, "
        "nystagmus, ataxia), granulomatous interstitial nephritis, and phacoclastic uveitis from lens "
        "rupture, with reactivation when host immunity wanes."
    )
    return tx_ja, tx_en, patho_ja, patho_en


def _coccidia(species: str):
    sp = _sp_ja(species)
    rabbit_note = ""
    if species == "rabbit":
        rabbit_note = (
            "肝コクシジウム（Eimeria stiedae）は胆管上皮を侵し肝腫大・黄疸を起こすため、サルファ剤による"
            "早期治療と衛生管理が重要。"
        )
    tx_ja = (
        f"{sp}のコクシジウム症（Isospora/Eimeria）にはサルファ系のサルファジメトキシン50 mg/kg PO初日、"
        "以後25 mg/kg q24hを5-20日、またはポナズリル20-50 mg/kg PO q24h（1-3日）、トルトラズリルを用いる。"
        "下痢・脱水には輸液と整腸、重複感染の管理を行う。"
        + rabbit_note
        + "オーシストは環境抵抗性が高いため、糞便除去・乾燥・熱湯/蒸気消毒による環境衛生で再感染を防ぐ。"
    )
    tx_en = (
        "Coccidiosis (Isospora/Eimeria) is treated with sulfadimethoxine 50 mg/kg PO day 1 then "
        "25 mg/kg q24h for 5-20 days, or a coccidiocidal triazinone (ponazuril 20-50 mg/kg PO q24h for "
        "1-3 days, or toltrazuril). Give fluids and gut support for diarrhoea/dehydration. "
        + (
            "Hepatic coccidiosis (Eimeria stiedae) damages biliary epithelium causing hepatomegaly and "
            "icterus — treat early with sulfonamides. "
            if species == "rabbit"
            else ""
        )
        + "Oocysts are environmentally resistant, so faecal removal, drying and steam/scald sanitation "
        "are essential to prevent re-infection."
    )
    patho_ja = (
        f"コクシジウムは{sp}の腸上皮細胞内で無性生殖（メロゴニー）と有性生殖を繰り返し、上皮を破壊して"
        "吸収不良・蛋白漏出・出血性下痢を起こす。幼若・過密・ストレス下で発症しやすく、"
        "重度感染では脱水・体重減少・二次感染を招く。"
    )
    patho_en = (
        "Coccidia cycle through asexual merogony and sexual stages inside intestinal epithelial cells, "
        "destroying the mucosa to cause malabsorption, protein loss and haemorrhagic diarrhoea. Disease "
        "is precipitated by youth, crowding and stress, with dehydration, weight loss and secondary "
        "infection in heavy burdens."
    )
    return tx_ja, tx_en, patho_ja, patho_en


def _sarcocystis(species: str):
    sp = _sp_ja(species)
    tx_ja = (
        f"{sp}のサルコシスティス症にはトリメトプリム・サルファ＋ピリメタミンの併用、または"
        "クリンダマイシンを用いる。鳥（特にオウム目のS. falcatula肺型）では支持療法（酸素・輸液）を併用し、"
        "予防的にピリメタミンを投与する。神経・筋症状には対症療法を行う。"
    )
    tx_en = (
        "Sarcocystosis is treated with trimethoprim-sulfa plus pyrimethamine, or clindamycin. In birds "
        "(notably pulmonary S. falcatula in psittacines) combine supportive oxygen and fluids with "
        "pyrimethamine prophylaxis, and treat neuromuscular signs symptomatically."
    )
    patho_ja = (
        f"サルコシスティスは終宿主（肉食獣・猛禽）と中間宿主の間で生活環を持つ原虫で、{sp}では"
        "筋肉内シスト形成や、急性期の内皮・肺胞での裂体増殖により出血性肺炎・脳炎・筋炎を生じる。"
    )
    patho_en = (
        "Sarcocystis cycles between carnivore/raptor definitive hosts and intermediate hosts; in this "
        "host it forms intramuscular cysts and, in the acute phase, undergoes schizogony in endothelium "
        "and alveoli, producing haemorrhagic pneumonia, encephalitis and myositis."
    )
    return tx_ja, tx_en, patho_ja, patho_en


def _atoxoplasma(species: str):
    sp = _sp_ja(species)
    tx_ja = (
        f"{sp}のアトキソプラズマ症（Atoxoplasma/Isospora serini）は根治が難しく、サルファ剤やトルトラズリルの"
        "投与と、群飼育における衛生・密度管理が中心となる。罹患幼鳥には保温・強制給餌などの支持療法を行う。"
    )
    tx_en = (
        "Atoxoplasmosis (Atoxoplasma/Isospora serini) is hard to cure; management centres on sulfonamides "
        "or toltrazuril plus flock hygiene and stocking-density control, with warmth and assisted feeding "
        "for affected fledglings."
    )
    patho_ja = (
        f"アトキソプラズマは{sp}（特に幼鳥）の単核球内で増殖する原虫で、肝・脾の腫大（'big liver disease'）と"
        "腸管感染を起こし、削痩・元気消失・突然死をきたす。"
    )
    patho_en = (
        "Atoxoplasma replicates within mononuclear cells of (mostly juvenile) birds, causing "
        "hepatosplenomegaly ('big liver disease') and enteric infection with wasting, depression and "
        "sudden death."
    )
    return tx_ja, tx_en, patho_ja, patho_en


def _leucocytozoon(species: str):
    sp = _sp_ja(species)
    tx_ja = (
        f"{sp}のロイコチトゾーン症に確実な治療薬はなく、サルファ剤（スルファジメトキシン/スルファキノキサリン）や"
        "クロピドール、ピリメタミンが用いられる。貧血・衰弱には支持療法を行い、媒介昆虫（ブユ・ヌカカ）の"
        "防除が最も重要である。"
    )
    tx_en = (
        "No reliably curative drug exists for leucocytozoonosis; sulfonamides "
        "(sulfadimethoxine/sulfaquinoxaline), clopidol or pyrimethamine are used. Support anaemia and "
        "debility, and prioritise vector control (blackflies, midges)."
    )
    patho_ja = (
        f"ロイコチトゾーンはブユ・ヌカカ媒介の原虫で、{sp}の白血球・赤血球および肝・脾・心・脳などの"
        "実質臓器でメロゴニーを行い、貧血・臓器のメガロシゾント形成・衰弱・突然死を生じる。"
    )
    patho_en = (
        "Leucocytozoon is transmitted by blackflies/midges; it undergoes merogony in leukocytes, "
        "erythrocytes and parenchymal organs (liver, spleen, heart, brain), causing anaemia, "
        "megaloschizont formation, debility and sudden death."
    )
    return tx_ja, tx_en, patho_ja, patho_en


def _avian_malaria(species: str):
    sp = _sp_ja(species)
    tx_ja = (
        f"{sp}の鳥マラリア（Plasmodium属）にはクロロキン＋プリマキンの併用、またはメフロキンを用いる。"
        "急性溶血・呼吸困難に対する酸素・輸液・輸血などの支持療法を併行し、蚊の防除を徹底する。"
    )
    tx_en = (
        "Avian malaria (Plasmodium spp.) is treated with chloroquine plus primaquine, or mefloquine, "
        "alongside supportive oxygen, fluids and transfusion for acute haemolysis/dyspnoea, with rigorous "
        "mosquito control."
    )
    patho_ja = (
        f"鳥マラリア原虫は蚊媒介で{sp}に感染し、赤血球内で分裂増殖して溶血性貧血を起こすとともに、"
        "組織内裂体増殖（外赤血球期）が肺・脳・肝などを侵し、急性期に高い死亡率を示す。"
    )
    patho_en = (
        "Avian Plasmodium is mosquito-transmitted; erythrocytic schizogony causes haemolytic anaemia "
        "while exo-erythrocytic schizogony in lung, brain and liver drives high acute-phase mortality."
    )
    return tx_ja, tx_en, patho_ja, patho_en


# Resolution order matters: more specific keys first so substrings do not collide
# (e.g. "Encephalitozoon" and "Hepatozoon" both end in "zoon" but have distinct
# prefixes; "Cytauxzoon" variants are matched before the generic terms).
_AGENTS: tuple[tuple[tuple[str, ...], object], ...] = (
    (("サイトークスゾーン", "サイトウクスゾーン", "シタウクソーン", "cytauxzoon"), _cytauxzoon),
    (("エンセファリトゾーン", "encephalitozoon"), _encephalitozoon),
    (("ヘパトゾーン", "hepatozoon"), _hepatozoon),
    (("バベシア", "babesi", "ピロプラズマ", "piroplasm"), _babesia),
    (("リーシュマニア", "leishman"), _leishmania),
    (("トキソプラズマ", "toxoplasm"), _toxoplasma),
    (("アトキソプラズマ", "atoxoplasm"), _atoxoplasma),
    (("ロイコチトゾーン", "leucocytozoon", "leukocytozoon"), _leucocytozoon),
    (("鳥マラリア", "avian malaria", "マラリア", "malaria"), _avian_malaria),
    (("サルコシスティス", "sarcocyst"), _sarcocystis),
    (("コクシジウム", "コクシジア", "coccidi"), _coccidia),
)


def resolve_protozoal_agent(name_ja: str, name_en: str):
    """Return the generator for a protozoal disease, or None if not protozoal."""
    name = f"{name_ja or ''} {name_en or ''}".lower()
    for keys, gen in _AGENTS:
        if any(k.lower() in name for k in keys):
            return gen
    return None


def protozoal_clinical_fields(species: str, name_ja: str, name_en: str, treatment_ja: str) -> dict | None:
    """Return curated antiprotozoal fields when ``treatment_ja`` is the deworming
    template AND the disease resolves to a protozoal agent. None otherwise, so
    callers may treat None as "leave untouched".

    Always returns ``treatment_ja``/``treatment`` (the clinically dangerous field)
    and ``pathophysiology_ja``/``pathophysiology`` (pathogen-specific mechanism).
    """
    if not treatment_ja or DEWORM_SIG not in treatment_ja:
        return None
    gen = resolve_protozoal_agent(name_ja, name_en)
    if gen is None:
        return None
    species = (species or "").lower()
    tx_ja, tx_en, patho_ja, patho_en = gen(species)
    return {
        "treatment_ja": tx_ja,
        "treatment": tx_en,
        "pathophysiology_ja": patho_ja,
        "pathophysiology": patho_en,
    }
