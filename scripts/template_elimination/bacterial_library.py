"""Curated etiology / pathophysiology for named-pathogen bacterial diseases.

Companion to ``pathogen_library`` (viral). Bacterial diseases whose name
identifies the organism shipped the generic bacterial category template — JA
``「…の原因は特定の細菌病原体の感染である。病原性細菌が体内に侵入…」`` and English
``"Bacterial infection. Transmission via…"`` / ``"Infectious diseases are caused
by pathogenic organisms…"``. When the name names the genus (salmonellosis,
pasteurellosis, tetanus, strangles …) the aetiology is a textbook fact, so it is
curated with zero fabrication risk.

Each generator returns pathogen-specific ``causes`` and ``pathophysiology`` (JA +
EN), branching on the named organism/toxin where it matters clinically —
clostridial disease by toxin (C. tetani / C. botulinum / C. perfringens),
haemotropic vs respiratory mycoplasma, avian vs feline chlamydia, S. equi
strangles in the horse. Only category-template / stub fields are replaced, so
curated prose (flagship pasteurellosis, psittacosis, mycobacteriosis) is kept.

References: Greene, *Infectious Diseases of the Dog and Cat* 4th ed; Quinn et al.,
*Veterinary Microbiology and Microbial Disease* 2nd ed; Sellon & Long, *Equine
Infectious Diseases* 2nd ed; Carpenter, *Exotic Animal Formulary* 6th ed.
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


def _ja(sp: str) -> str:
    return SPECIES_JA.get(sp, sp)


def _en(sp: str) -> str:
    return SPECIES_EN.get(sp, sp)


def _nl(name_ja: str, name_en: str) -> str:
    return _neutralise_negations(f"{name_ja or ''} {name_en or ''}").lower()


# --------------------------------------------------------------------------- #
# Generators: (species, name_ja, name_en) -> (causes_ja, causes_en, patho_ja,  #
# patho_en). name is passed so a genus can branch on the specific disease.     #
# --------------------------------------------------------------------------- #
def _salmonella(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}のサルモネラ症はグラム陰性桿菌 Salmonella 属の感染による。汚染された飼料・水・環境や保菌動物の糞便を介した経口感染で伝播する人獣共通感染症。"
    cen = "Caused by Salmonella spp. (Gram-negative enteric bacilli), acquired by ingesting contaminated feed, water or the faeces of carrier animals; it is a zoonosis."
    pja = "サルモネラは腸上皮に侵入して腸炎を起こし、リポ多糖（内毒素）と全身播種により菌血症・敗血症・多臓器障害を招く。保菌動物は無症状でも間欠的に排菌する。"
    pen = "Salmonella invades intestinal epithelium causing enteritis, and via lipopolysaccharide endotoxin and systemic spread can produce bacteraemia, septicaemia and multi-organ injury; carriers shed intermittently while healthy."
    return cja, cen, pja, pen


def _ecoli(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}の大腸菌症はグラム陰性桿菌 Escherichia coli（病原性株）の感染による。糞口感染や不衛生な環境、移行免疫の不足が発症要因となる。"
    cen = "Caused by pathogenic strains of Escherichia coli (a Gram-negative bacillus), via the faecal-oral route; poor hygiene and inadequate passive immunity predispose."
    pja = "病原性大腸菌は付着因子で腸上皮に定着し、エンテロトキシンや志賀毒素、内毒素により分泌性下痢・腸傷害を起こす。全身播種すると敗血症・多臓器障害を招く（特に新生子）。"
    pen = "Pathogenic E. coli adheres to enterocytes via fimbrial adhesins and, through enterotoxins, Shiga toxins and endotoxin, causes secretory diarrhoea and mucosal injury; systemic spread produces septicaemia, especially in neonates."
    return cja, cen, pja, pen


def _staph(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}のブドウ球菌感染症はグラム陽性球菌 Staphylococcus 属（S. pseudintermedius・S. aureus 等）による。皮膚・粘膜の常在菌が、バリア破綻・免疫低下・基礎疾患を契機に日和見的に増殖して発症する。"
    cen = "Caused by Staphylococcus spp. (Gram-positive cocci, e.g. S. pseudintermedius, S. aureus); these skin/mucosal commensals overgrow opportunistically when the barrier is broken or immunity is impaired."
    pja = "ブドウ球菌は毛包・皮膚・創部で増殖し、コアグラーゼや各種毒素・酵素で組織を傷害して膿皮症・膿瘍・創傷感染を起こす。メチシリン耐性株（MRSP/MRSA）は治療を困難にする。"
    pen = "Staphylococci proliferate in follicles, skin and wounds, damaging tissue via coagulase, toxins and enzymes to cause pyoderma, abscessation and wound infection; meticillin-resistant strains (MRSP/MRSA) complicate therapy."
    return cja, cen, pja, pen


def _strep(sp, nj, ne):
    j = _ja(sp)
    name = _nl(nj, ne)
    if sp == "horse" and ("strangles" in name or "腺疫" in name or "equi" in name):
        cja = "馬の腺疫は Streptococcus equi subsp. equi の感染による。感染馬・保菌馬の鼻汁や膿を介した接触・飛沫、汚染された飼料桶・水・器具で急速に伝播する。"
        cen = "Caused by Streptococcus equi subsp. equi; it spreads rapidly by contact with nasal discharge/pus from infected or carrier horses and via contaminated troughs, water and equipment."
        pja = "S. equi は上部気道粘膜に定着後、所属リンパ節（顎下・咽後）に波及して化膿性リンパ節炎・膿瘍を形成する。膿瘍破裂で排膿し、稀に全身播種（bastard strangles）や免疫介在性紫斑病を合併する。"
        pen = "S. equi colonises the upper-airway mucosa then spreads to regional (submandibular/retropharyngeal) lymph nodes forming suppurative abscesses that rupture and drain; rare sequelae include metastatic 'bastard strangles' and immune-mediated purpura haemorrhagica."
        return cja, cen, pja, pen
    cja = f"{j}のレンサ球菌感染症はグラム陽性球菌 Streptococcus 属の感染による。常在菌の日和見的増殖や、創傷・咬傷・粘膜を介した侵入で発症する。"
    cen = "Caused by Streptococcus spp. (Gram-positive cocci), through opportunistic overgrowth of commensals or entry via wounds, bites and mucosal surfaces."
    pja = "レンサ球菌は化膿性の炎症を起こし、局所では膿瘍・蜂窩織炎・リンパ節炎を、全身播種では敗血症・関節炎・心内膜炎を招く。溶血毒素・莢膜が病原性に関与する。"
    pen = "Streptococci provoke suppurative inflammation — local abscessation, cellulitis and lymphadenitis, or, with systemic spread, septicaemia, arthritis and endocarditis; haemolysins and capsule contribute to virulence."
    return cja, cen, pja, pen


def _pseudomonas(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}の緑膿菌感染症はグラム陰性桿菌 Pseudomonas aeruginosa による。湿潤環境や水・器材に広く存在する日和見菌で、外耳道・創部・角膜・尿路などのバリア破綻部に感染する。"
    cen = "Caused by Pseudomonas aeruginosa (a Gram-negative bacillus), a ubiquitous water/environment opportunist that infects damaged barriers — ear canal, wounds, cornea and urinary tract."
    pja = "緑膿菌はバイオフィルムと多彩な毒素・蛋白分解酵素で組織を傷害し、難治性の外耳炎・角膜融解・創部感染を起こす。多剤耐性が高く治療に難渋する。"
    pen = "Pseudomonas damages tissue through biofilm formation and an array of toxins and proteases, causing refractory otitis, corneal melting and wound infection; extensive multidrug resistance makes it hard to treat."
    return cja, cen, pja, pen


def _clostridium(sp, nj, ne):
    j = _ja(sp)
    name = _nl(nj, ne)
    if "tetanus" in name or "破傷風" in name or "tetani" in name:
        cja = f"{j}の破傷風は Clostridium tetani の芽胞が創傷（特に深い嫌気的創）から侵入し、産生する神経毒テタノスパスミンによる。"
        cen = "Caused by Clostridium tetani spores entering through wounds (especially deep anaerobic wounds); disease is mediated by the neurotoxin tetanospasmin."
        pja = "テタノスパスミンは末梢神経を逆行性に上行し、抑制性介在ニューロン（GABA/グリシン）からの伝達物質放出を遮断する。その結果、持続的な筋強直・強直性痙攣・開口障害・第三眼瞼突出を生じる。"
        pen = "Tetanospasmin travels retrogradely up peripheral nerves and blocks neurotransmitter release from inhibitory (GABA/glycine) interneurons, producing sustained muscle rigidity, tetanic spasms, trismus and third-eyelid protrusion."
        return cja, cen, pja, pen
    if "botulism" in name or "ボツリヌス" in name or "botulinum" in name:
        cja = f"{j}のボツリヌス症は Clostridium botulinum が産生するボツリヌス毒素の摂取（腐敗物・汚染飼料）による毒素性疾患。"
        cen = "Caused by ingestion of botulinum toxin produced by Clostridium botulinum (from carrion or spoiled feed) — a toxaemia rather than an active infection."
        pja = "ボツリヌス毒素は神経筋接合部でアセチルコリン放出を阻害し、対称性の弛緩性麻痺・脱力・嚥下/呼吸筋麻痺を進行性に生じる。重症例は呼吸不全で死亡する。"
        pen = "Botulinum toxin blocks acetylcholine release at the neuromuscular junction, causing progressive symmetric flaccid paralysis, weakness and paralysis of swallowing and respiratory muscles; severe cases die of respiratory failure."
        return cja, cen, pja, pen
    if "perfringens" in name or "enterotox" in name or "腸毒血" in name or "エンテロトキセミア" in name:
        cja = f"{j}のクロストリジウム性腸疾患は Clostridium perfringens 等の腸管内異常増殖と毒素産生による。食餌変化・炭水化物過負荷・腸内細菌叢の乱れが誘因となる。"
        cen = "Caused by overgrowth of Clostridium perfringens (and related clostridia) in the gut with toxin production; dietary change, carbohydrate overload and dysbiosis are triggers."
        pja = "産生された腸毒素が腸上皮を傷害して壊死性・出血性腸炎を起こし、毒素吸収により腸毒血症・全身性ショックに至る。草食動物では特に重篤化しやすい。"
        pen = "Clostridial enterotoxins injure intestinal epithelium producing necrotising/haemorrhagic enteritis, and toxin absorption leads to enterotoxaemia and shock — often fulminant in herbivores."
        return cja, cen, pja, pen
    cja = f"{j}のクロストリジウム感染症は芽胞形成性嫌気性菌 Clostridium 属の感染・毒素産生による。芽胞は環境中に広く存在し、嫌気的条件下で発芽・増殖する。"
    cen = "Caused by spore-forming anaerobic Clostridium spp.; environmentally ubiquitous spores germinate and proliferate under anaerobic conditions and elaborate potent toxins."
    pja = "クロストリジウムは強力な外毒素により組織壊死・毒素血症を起こす。感染部位により壊死性筋炎（ガス壊疽）・腸炎・神経症状など多彩な病態を呈する。"
    pen = "Clostridia produce potent exotoxins causing tissue necrosis and toxaemia; depending on site this manifests as necrotising myositis (gas gangrene), enteritis or neurological disease."
    return cja, cen, pja, pen


def _pasteurella(sp, nj, ne):
    j = _ja(sp)
    name = _nl(nj, ne)
    if sp == "rabbit" or "snuffles" in name or "スナッフル" in name:
        cja = "ウサギのパスツレラ症（スナッフル）は Pasteurella multocida の感染による。多くの個体が鼻腔に保菌し、ストレス・過密・不衛生な換気（アンモニア）で発症・伝播する。"
        cen = "Caused by Pasteurella multocida; many rabbits are nasal carriers, and stress, crowding and poor ventilation (ammonia) precipitate clinical 'snuffles'."
        pja = "P. multocida は上部気道粘膜に定着し、鼻炎・副鼻腔炎から中耳炎（斜頸）・肺炎・膿瘍・結膜炎・子宮蓄膿へと波及する。慢性化・再発しやすい。"
        pen = "P. multocida colonises the upper-airway mucosa and extends to rhinitis/sinusitis, otitis media (head tilt), pneumonia, abscesses, conjunctivitis and pyometra, tending to become chronic and recurrent."
        return cja, cen, pja, pen
    cja = f"{j}のパスツレラ症はグラム陰性菌 Pasteurella multocida の感染による。口腔・上気道の常在菌で、咬傷や呼吸器を介して伝播する。"
    cen = "Caused by Pasteurella multocida (a Gram-negative coccobacillus), an oral/upper-airway commensal transmitted via bite wounds and the respiratory route."
    pja = "P. multocida は咬傷部で急速に増殖して蜂窩織炎・膿瘍を、呼吸器では鼻炎・肺炎を起こす。内毒素と莢膜が病原性に関与し、免疫低下個体で重症化する。"
    pen = "P. multocida proliferates rapidly in bite wounds causing cellulitis/abscessation and, in the airway, rhinitis and pneumonia; endotoxin and capsule drive virulence, with severe disease in immunocompromised hosts."
    return cja, cen, pja, pen


def _mycoplasma(sp, nj, ne):
    j = _ja(sp)
    name = _nl(nj, ne)
    if any(k in name for k in ("haemo", "hemo", "ヘモプラズマ", "血液", "haemofelis", "hemotropic", "感染性貧血")):
        cja = f"{j}のヘモプラズマ症（ヘモトロピック・マイコプラズマ）は Mycoplasma haemofelis 等の赤血球表面寄生菌による。ノミ・マダニ等の吸血節足動物や咬傷・輸血で伝播する。"
        cen = "Caused by haemotropic mycoplasmas (e.g. Mycoplasma haemofelis) that parasitise the red-cell surface, transmitted by blood-feeding arthropods (fleas/ticks), bites and transfusion."
        pja = "赤血球表面に付着した菌が免疫介在性・血管外溶血を誘発し、再生性貧血・黄疸・発熱を起こす。感染は再燃を繰り返し、キャリア化しやすい。"
        pen = "Surface attachment triggers immune-mediated, largely extravascular haemolysis producing regenerative anaemia, icterus and fever; infection tends to relapse and persist as a carrier state."
        return cja, cen, pja, pen
    cja = f"{j}のマイコプラズマ感染症は細胞壁を欠く細菌 Mycoplasma 属による。飛沫・接触で伝播し、密飼い・換気不良・他病原体との混合感染で顕在化する。"
    cen = "Caused by Mycoplasma spp. (cell-wall-deficient bacteria), spread by aerosol and contact; crowding, poor ventilation and co-infection precipitate disease."
    pja = "マイコプラズマは気道・関節・結膜の粘膜上皮に付着して線毛障害と慢性炎症を起こし、慢性呼吸器疾患・結膜炎・多発性関節炎を招く。細胞壁を欠くためβラクタム薬が無効。"
    pen = "Mycoplasmas adhere to respiratory, joint and conjunctival epithelium causing ciliary damage and chronic inflammation — chronic respiratory disease, conjunctivitis and polyarthritis; lacking a cell wall, they are unaffected by beta-lactams."
    return cja, cen, pja, pen


def _chlamydia(sp, nj, ne):
    j = _ja(sp)
    name = _nl(nj, ne)
    if sp in _BIRDS or "psittacosis" in name or "オウム病" in name or "psittaci" in name:
        cja = f"{j}のクラミジア症（オウム病）は偏性細胞内寄生菌 Chlamydia psittaci の感染による。乾燥した糞・気道分泌物・羽毛粉塵の吸入や経口摂取で伝播する人獣共通感染症。"
        cen = "Caused by Chlamydia psittaci (an obligate intracellular bacterium); transmission is by inhalation/ingestion of dried faeces, respiratory secretions and feather dust — a zoonosis (psittacosis)."
        pja = "C. psittaci は網内系・肝・脾・気嚢の細胞内で増殖し、肝脾腫・気嚢炎・結膜炎・多尿性下痢を起こす。不顕性キャリアがストレス時に排菌して感染源となる。"
        pen = "C. psittaci multiplies within reticuloendothelial, hepatic, splenic and air-sac cells, producing hepatosplenomegaly, airsacculitis, conjunctivitis and polyuric diarrhoea; subclinical carriers shed under stress."
        return cja, cen, pja, pen
    if sp == "cat" or "felis" in name:
        cja = "猫のクラミジア感染症は Chlamydia felis の感染による。感染猫の眼分泌物を介した直接接触で伝播し、若齢・多頭飼育で多い。"
        cen = "Caused by Chlamydia felis, spread by direct contact with ocular secretions of infected cats; most common in kittens and multi-cat households."
        pja = "C. felis は結膜上皮細胞内で増殖し、慢性・再発性の結膜炎（強い眼脂・結膜浮腫）を主徴とする。軽度の上部気道症状を伴うことがある。"
        pen = "C. felis replicates within conjunctival epithelial cells, causing chronic/recurrent conjunctivitis with marked ocular discharge and chemosis, sometimes with mild upper-respiratory signs."
        return cja, cen, pja, pen
    cja = f"{j}のクラミジア感染症は偏性細胞内寄生菌 Chlamydia 属による。分泌物・排泄物を介した接触・吸入で伝播する。"
    cen = "Caused by Chlamydia spp. (obligate intracellular bacteria), spread by contact with and inhalation of secretions and excretions."
    pja = "クラミジアは粘膜上皮細胞内で増殖し、結膜炎・呼吸器炎・全身性の炎症を起こす。細胞内寄生のためテトラサイクリン系等の細胞移行性薬剤を要する。"
    pen = "Chlamydiae replicate within mucosal epithelial cells producing conjunctivitis, respiratory disease and systemic inflammation; their intracellular niche requires cell-penetrating drugs such as tetracyclines."
    return cja, cen, pja, pen


def _bordetella(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}のボルデテラ感染症はグラム陰性菌 Bordetella bronchiseptica による。飛沫・接触で伝播し、密飼い・換気不良・ウイルスとの混合感染で顕在化する呼吸器病原体。"
    cen = "Caused by Bordetella bronchiseptica (a Gram-negative respiratory pathogen), spread by aerosol and contact; crowding, poor ventilation and viral co-infection precipitate disease."
    pja = "B. bronchiseptica は線毛付着因子で気道上皮に定着し、毒素で線毛運動と粘液クリアランスを障害する。気管気管支炎（ケンネルコフの一因）・肺炎を起こし、モルモット等では致死的となる。"
    pen = "B. bronchiseptica adheres to airway cilia and, via toxins, impairs ciliary function and mucus clearance, causing tracheobronchitis (a component of kennel cough) and pneumonia — often fatal in guinea pigs."
    return cja, cen, pja, pen


def _mycobacterium(sp, nj, ne):
    j = _ja(sp)
    name = _nl(nj, ne)
    if any(k in name for k in ("tuberculo", "結核", "bovis", "avium", "avian tb")):
        cja = f"{j}の結核（マイコバクテリア症）は抗酸菌 Mycobacterium 属（M. tuberculosis complex／M. bovis、鳥では M. avium）の感染による。経気道・経口感染で伝播し、人獣共通感染のリスクがある。"
        cen = "Caused by Mycobacterium of the tuberculosis complex (M. bovis; M. avium in birds), acquired by inhalation or ingestion; it carries a zoonotic risk."
        pja = "抗酸菌はマクロファージ内で生存・増殖し、細胞性免疫による肉芽腫（結節)を諸臓器（肺・肝・脾・腸）に形成する。緩徐に進行し、慢性消耗・臓器機能不全を招く。"
        pen = "Mycobacteria survive and multiply within macrophages, and the cell-mediated response forms granulomas (tubercles) in lung, liver, spleen and gut; disease progresses slowly with chronic wasting and organ dysfunction."
        return cja, cen, pja, pen
    if any(k in name for k in ("leprosy", "lepr", "ハンセン", "らい", "leproid")):
        cja = f"{j}のらい類似疾患（皮膚型マイコバクテリア症）は培養困難な抗酸菌（M. lepraemurium 等）の感染による。咬傷や外傷を介した接種で伝播すると考えられる。"
        cen = "Caused by fastidious, difficult-to-culture mycobacteria (e.g. M. lepraemurium); thought to be inoculated through bites and wounds (feline leprosy syndrome)."
        pja = "菌が真皮・皮下で肉芽腫性炎症を起こし、単発〜多発の結節・潰瘍を形成する。全身状態は比較的保たれるが、外科切除と長期の多剤併用を要する。"
        pen = "The organism drives granulomatous inflammation in dermis and subcutis forming single or multiple nodules and ulcers; animals stay relatively well but need excision plus prolonged multidrug therapy."
        return cja, cen, pja, pen
    cja = f"{j}の非結核性（非定型）マイコバクテリア症は環境中の抗酸菌（迅速発育菌等）による。土壌・水中の菌が創傷・皮下脂肪組織に感染して発症する。"
    cen = "Caused by environmental non-tuberculous (atypical/rapidly growing) mycobacteria; soil/water organisms infect wounds and subcutaneous fat."
    pja = "抗酸菌は皮下・脂肪組織で肉芽腫性・化膿性の慢性炎症を起こし、難治性の結節・瘻管・パニクリティスを形成する。菌の脂質壁のため長期の多剤併用を要する。"
    pen = "These mycobacteria cause chronic granulomatous/pyogranulomatous inflammation of subcutis and fat, forming refractory nodules, draining tracts and panniculitis; their lipid-rich wall demands prolonged multidrug therapy."
    return cja, cen, pja, pen


def _leptospira(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}のレプトスピラ症はスピロヘータ Leptospira 属の感染による。保菌動物（げっ歯類等）の尿で汚染された水・土壌との接触や粘膜・損傷皮膚からの侵入で伝播する人獣共通感染症。"
    cen = "Caused by spirochaetes of the genus Leptospira, acquired through contact with water/soil contaminated by the urine of reservoir hosts (e.g. rodents), entering via mucosa or broken skin — a zoonosis."
    pja = "レプトスピラは血流に侵入して菌血症を起こし、腎尿細管と肝に定着して急性腎障害・肝障害（黄疸）・血管炎・出血を招く。回復後も腎に保菌して排菌する。"
    pen = "Leptospires enter the bloodstream causing leptospiraemia, then localise in renal tubules and liver producing acute kidney injury, hepatopathy (icterus), vasculitis and haemorrhage; survivors shed from the kidney."
    return cja, cen, pja, pen


def _klebsiella(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}のクレブシエラ感染症はグラム陰性桿菌 Klebsiella pneumoniae 等による。腸管・環境由来の日和見菌で、免疫低下やバリア破綻を契機に呼吸器・尿路・生殖器・血流に感染する。"
    cen = "Caused by Klebsiella pneumoniae and related Gram-negative bacilli — enteric/environmental opportunists that infect the respiratory, urinary, genital tract or bloodstream when immunity or barriers fail."
    pja = "莢膜を持つクレブシエラは食菌に抵抗して増殖し、化膿性・壊死性の肺炎・膀胱炎・子宮感染・敗血症を起こす。多剤耐性（ESBL産生）株が問題となる。"
    pen = "Its antiphagocytic capsule lets Klebsiella proliferate, causing suppurative/necrotising pneumonia, cystitis, genital infection and septicaemia; multidrug-resistant (ESBL) strains are a concern."
    return cja, cen, pja, pen


def _listeria(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}のリステリア症はグラム陽性桿菌 Listeria monocytogenes の感染による。汚染飼料（不良サイレージ等）・環境からの経口摂取で伝播する人獣共通感染症。"
    cen = "Caused by Listeria monocytogenes (a Gram-positive bacillus), acquired by ingesting contaminated feed (e.g. spoiled silage) or environment — a zoonosis."
    pja = "L. monocytogenes は細胞内寄生し、三叉神経等を上行して脳幹に達し、片側性脳幹脳炎（旋回運動・顔面麻痺・嚥下障害）を起こす。妊娠動物では胎盤感染により流産を招く。"
    pen = "L. monocytogenes is intracellular and ascends cranial nerves to the brainstem, causing unilateral rhombencephalitis (circling, facial paralysis, dysphagia); in pregnancy, placental infection causes abortion."
    return cja, cen, pja, pen


def _abscess(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}の膿瘍は、咬傷・穿通性外傷・異物や隣接感染から侵入した化膿性細菌（好気性菌と嫌気性菌の混合が多い）の限局性感染による。"
    cen = "Caused by pyogenic bacteria (often a mixed aerobic-anaerobic flora) introduced by bite wounds, penetrating trauma, foreign bodies or extension from an adjacent infection — a localised infection."
    pja = "細菌の増殖に対する好中球の集積と組織融解により、膿（壊死組織・生菌・白血球）が被膜に囲まれて貯留する。緊満・疼痛・発熱を生じ、破裂・排膿するか全身播種すると敗血症に至る。"
    pen = "Neutrophil influx and tissue liquefaction in response to bacterial growth create a capsule-walled collection of pus (necrotic tissue, live bacteria, leukocytes); it becomes tense and painful and, if it ruptures or spreads, can cause sepsis."
    return cja, cen, pja, pen


def _lawsonia(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}の増殖性腸症は偏性細胞内寄生菌 Lawsonia intracellularis の感染による。糞口感染で伝播し、フェレット・幼齢個体で多い。"
    cen = "Caused by Lawsonia intracellularis (an obligate intracellular bacterium), transmitted faecal-orally; common in ferrets and young animals (proliferative enteropathy)."
    pja = "L. intracellularis は腸陰窩上皮細胞内で増殖し、未熟腸細胞の異常増殖による腸粘膜肥厚（増殖性腸症）を起こす。吸収不良・蛋白漏出性下痢・体重減少を招く。"
    pen = "L. intracellularis proliferates within crypt enterocytes driving hyperplasia of immature epithelium (proliferative enteropathy), with thickened mucosa causing malabsorption, protein-losing diarrhoea and weight loss."
    return cja, cen, pja, pen


def _helicobacter(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}のヘリコバクター感染症はらせん状グラム陰性菌 Helicobacter 属による。経口・糞口感染で伝播し、胃粘膜に定着する。"
    cen = "Caused by spiral Gram-negative Helicobacter spp., acquired oro-orally/faecal-orally and colonising the gastric mucosa."
    pja = "ヘリコバクターはウレアーゼで胃酸を中和して胃粘膜に定着し、慢性胃炎・リンパ濾胞過形成・嘔吐を起こす。一部は胃潰瘍やリンパ腫との関連が示唆される。"
    pen = "Using urease to neutralise gastric acid, Helicobacter colonises the mucosa causing chronic gastritis, lymphoid follicular hyperplasia and vomiting, with a suggested link to gastric ulceration and lymphoma."
    return cja, cen, pja, pen


def _campylobacter(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}のカンピロバクター症はらせん状グラム陰性菌 Campylobacter 属（C. jejuni 等）による。汚染された食物・水・糞便を介した経口感染で伝播する人獣共通感染症。"
    cen = "Caused by spiral Gram-negative Campylobacter spp. (e.g. C. jejuni), acquired by ingesting contaminated food, water or faeces — a zoonosis."
    pja = "カンピロバクターは腸上皮に侵入・付着して毒素を産生し、水様〜粘血性下痢・腸炎を起こす。若齢・免疫低下・混合感染で症状が増悪する。"
    pen = "Campylobacter invades and adheres to intestinal epithelium and elaborates toxins, producing watery to mucohaemorrhagic diarrhoea and enteritis, worse in the young, immunosuppressed or co-infected."
    return cja, cen, pja, pen


def _brucella(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}のブルセラ症はグラム陰性菌 Brucella 属（犬では B. canis）の感染による。交尾・流産分泌物・体液を介して伝播する人獣共通感染症。"
    cen = "Caused by Brucella spp. (B. canis in dogs), transmitted venereally and via aborted material and body fluids — a zoonosis."
    pja = "ブルセラは細胞内寄生し、生殖器（精巣上体・胎盤）や網内系に慢性感染して不妊・流産・精巣上体炎・椎間板脊椎炎・ブドウ膜炎を起こす。持続菌血症を呈し根治が難しい。"
    pen = "Brucella is intracellular and chronically infects the reproductive tract (epididymis, placenta) and reticuloendothelial system, causing infertility, abortion, epididymitis, discospondylitis and uveitis, with persistent bacteraemia that resists cure."
    return cja, cen, pja, pen


def _borrelia(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}のライム病はスピロヘータ Borrelia burgdorferi の感染による。マダニ（Ixodes 属）の吸血を介して伝播する。"
    cen = "Caused by the spirochaete Borrelia burgdorferi, transmitted by the bite of Ixodes ticks (Lyme borreliosis)."
    pja = "ボレリアはマダニ咬着後、皮膚から関節・腎・神経・心へ播種し、免疫介在性の機序も加わって遊走性の多発性関節炎・発熱・元気食欲低下、稀に致死的な糸球体腎炎を起こす。"
    pen = "After tick attachment, Borrelia disseminates from skin to joints, kidney, nerves and heart; combined with immune-mediated mechanisms it causes shifting-leg polyarthritis, fever and lethargy, and rarely a fatal glomerulonephritis."
    return cja, cen, pja, pen


def _actinomyces(sp, nj, ne):
    j = _ja(sp)
    cja = f"{j}の放線菌症／ノカルジア症はフィラメント状細菌 Actinomyces／Nocardia の感染による。口腔常在菌の創傷・咬傷からの侵入（放線菌）や、土壌由来菌の経気道・経皮感染（ノカルジア）で発症する。"
    cen = "Caused by filamentous bacteria Actinomyces or Nocardia — the former an oral commensal entering via wounds/bites, the latter a soil organism acquired by inhalation or through skin."
    pja = "これらの菌は膿瘍・肉芽腫・化膿性胸膜炎（膿胸）を形成し、硫黄顆粒を伴う排膿性の瘻管をつくる。緩徐に進行し、長期の抗菌薬治療を要する。"
    pen = "These organisms form abscesses, granulomas and pyothorax with draining tracts containing 'sulphur granules'; disease is indolent and requires prolonged antibacterial therapy."
    return cja, cen, pja, pen


# name-pattern -> generator. Order matters: specific/collision-safe keys first.
# NOTE substring collisions deliberately avoided: "大腸菌"/"escherichia"/"e. coli"
# (never bare "coli" — would hit colic/colitis); "listeria"/"listerio" (never
# bare "listeri" — would hit "blistering"); genus names spelled in full.
_AGENTS: tuple[tuple[tuple[str, ...], object], ...] = (
    (("破傷風", "tetanus", "tetani"), _clostridium),
    (("ボツリヌス", "botulism", "botulinum"), _clostridium),
    (("クロストリジウム", "clostrid", "腸毒血", "enterotoxaemia", "enterotoxemia"), _clostridium),
    (("腺疫", "strangles"), _strep),
    (("サルモネラ", "salmonell"), _salmonella),
    (("大腸菌", "escherichia", "e. coli", "colibacill"), _ecoli),
    (("ブドウ球菌", "staphylococc"), _staph),
    (("レンサ球菌", "連鎖球菌", "streptococc"), _strep),
    (("緑膿菌", "pseudomonas"), _pseudomonas),
    (("パスツレラ", "pasteurell", "スナッフル", "snuffles"), _pasteurella),
    (("ヘモプラズマ", "haemoplasm", "hemoplasm", "haemofelis", "マイコプラズマ", "mycoplasm"), _mycoplasma),
    (("クラミジア", "chlamyd", "オウム病", "psittacosis"), _chlamydia),
    (("ボルデテラ", "bordetell"), _bordetella),
    (("結核", "tuberculo", "マイコバクテリ", "mycobacter", "抗酸菌", "leproid", "leprosy", "ハンセン"), _mycobacterium),
    (("レプトスピラ", "leptospir"), _leptospira),
    (("クレブシエラ", "klebsiell"), _klebsiella),
    (("リステリア", "listeria", "listerio"), _listeria),
    (("ローソニア", "lawsonia", "増殖性腸", "proliferative enteropathy", "proliferative bowel"), _lawsonia),
    (("ヘリコバクター", "helicobacter"), _helicobacter),
    (("カンピロバクター", "campylobacter"), _campylobacter),
    (("ブルセラ", "brucell"), _brucella),
    (("ライム病", "borreli", "lyme"), _borrelia),
    (("放線菌", "actinomyc", "ノカルジア", "nocardia"), _actinomyces),
    (("膿瘍", "abscess"), _abscess),
)


def resolve_bacterial_agent(name_ja: str, name_en: str):
    """Return the generator for a named-pathogen bacterial disease, or None.

    Negated names are neutralised first so an explicitly non-bacterial disease is
    never matched."""
    name = _nl(name_ja, name_en)
    for keys, gen in _AGENTS:
        if any(k.lower() in name for k in keys):
            return gen
    return None


# The broad "abscess" generator must not claim a primary bacterial cause for an
# abscess that is secondary to a non-bacterial primary disease (hypovitaminosis A
# oral abscesses, neoplastic masses) or that names a specific organism whose
# route the generic mixed-flora text would misstate (Corynebacterium pigeon fever).
_ABSCESS_EXCLUSIONS = (
    "ビタミン",
    "vitamin",
    "欠乏",
    "deficiency",
    "腫瘍",
    "neoplas",
    "carcinoma",
    "腺癌",
    "腺腫",
    "鳩熱",
    "pigeon fever",
)


def bacterial_clinical_fields(species: str, name_ja: str, name_en: str) -> dict | None:
    """Curated causes / pathophysiology (JA+EN) for a named-pathogen bacterial
    disease, or None when the name does not resolve to a known organism."""
    gen = resolve_bacterial_agent(name_ja, name_en)
    if gen is None:
        return None
    if gen is _abscess:
        low = _nl(name_ja, name_en)
        if any(x in low for x in _ABSCESS_EXCLUSIONS):
            return None
    cja, cen, pja, pen = gen((species or "").lower(), name_ja or "", name_en or "")
    return {
        "causes_ja": cja,
        "causes": cen,
        "pathophysiology_ja": pja,
        "pathophysiology": pen,
    }
