"""Curated etiology / pathophysiology for named-pathogen viral diseases.

The category generators emitted one generic aetiology for *every* viral disease
— Japanese ``「…の原因はウイルス感染である。特異的ウイルス病原体が宿主細胞に侵入し…」``
(245 records) and English ``"Viral infection. Transmission via direct contact
…"`` (200+ records). For a disease whose name *names the pathogen* (canine
parvovirus, feline herpesvirus, rabies …) that generic text is a wasted,
credibility-damaging placeholder: the aetiology is a textbook fact derivable
directly from the name, so it can be curated with zero fabrication risk.

Each generator returns pathogen-specific ``causes`` and ``pathophysiology`` in
Japanese and English. The mechanism of a virus family is host-independent, but
where the *named* virus is host-adapted (FHV-1 vs CHV-1 vs EHV-1; FPV vs CPV-2)
the species branch names the correct strain and its host-specific syndrome, so
the text is both accurate and disease-specific. Only records that currently
carry a recognised category template or vague stub are overwritten, so genuine
curated prose (e.g. the flagship PBFD / PDD entries) is never touched.

References: Greene, *Infectious Diseases of the Dog and Cat* 4th ed; Sykes,
*Canine and Feline Infectious Diseases*; MacLachlan & Dubovi, *Fenner's
Veterinary Virology* 5th ed; Ritchie, *Avian Viruses*; Reed & Bayly, *Equine
Internal Medicine*.
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

# Generic category-causes / pathophysiology template lead phrases. When a disease
# resolves to a *named* pathogen, ANY of these is a mislabel (the aetiology is the
# organism), so the field is safe to overwrite. Shared by the JSON pass and the
# served-DB safety net. Lowercased for case-insensitive substring matching.
GENERIC_CAUSES_JA_MARKS: tuple[str, ...] = (
    "の原因はウイルス感染である",
    "特異的ウイルス病原体が宿主細胞",
    "特定の細菌病原体の感染",
    "病原性細菌が体内に侵入",
)
GENERIC_CAUSES_EN_MARKS: tuple[str, ...] = (
    "viral infection. transmission via",
    "bacterial infection. transmission via",
    "infectious diseases are caused by pathogenic organisms",
    "multifactorial etiology depending on disease type",
    "neoplastic etiology, often unknown",
    "caused by physical trauma to musculoskeletal",
    "gastrointestinal etiology. may include",
    "caused by parasites infecting affected tissues",
    "caused by progressive deterioration of cardiovascular",
    "respiratory etiology. includes",
    "endocrine or metabolic dysfunction. may result",
    "caused by exposure to toxic substances",
    "caused by dietary deficiency or excess",
    "fungal infection. inhalation or contact",
    "nutritional diseases result from",
    "musculoskeletal etiology. includes",
    "reproductive etiology. includes",
    "neurological etiology. may include",
    "hepatic etiology. includes",
    "ophthalmic etiology. includes",
    "nutritional imbalance. caused by",
    "dermatological etiology. includes",
    "dental etiology. includes",
    "external parasite infestation",
    "cardiac etiology. may include",
    "toxicosis results from exposure",
    "neoplastic diseases arise from",
)
# All English category pathophysiology templates begin "The pathophysiology of …".
GENERIC_PATHO_EN_MARKS: tuple[str, ...] = ("the pathophysiology of ",)


def _ja(species: str) -> str:
    return SPECIES_JA.get(species, species)


def _en(species: str) -> str:
    return SPECIES_EN.get(species, species)


# --------------------------------------------------------------------------- #
# Viral pathogen generators. Each returns (causes_ja, causes_en, patho_ja,     #
# patho_en). Callers weave in the disease name for exact-uniqueness.           #
# --------------------------------------------------------------------------- #
def _herpesvirus(sp: str):
    j, e = _ja(sp), _en(sp)
    if sp == "cat":
        cja = "猫ヘルペスウイルス1型（FHV-1）の感染による。鼻汁・眼脂・唾液を介した直接接触や飛沫、汚染器材で伝播し、回復後も三叉神経節に潜伏してストレス時に再活性化・再排出する。"
        cen = "Caused by feline herpesvirus-1 (FHV-1), spread by direct contact with ocular/nasal/oral secretions, aerosol and fomites; the virus establishes lifelong latency in the trigeminal ganglion and reactivates under stress."
        pja = "FHV-1は上部気道・結膜・角膜上皮で複製し、上皮壊死と潰瘍形成を起こす。三叉神経節への潜伏感染が生涯持続し、ストレスやステロイド投与で再活性化して再発性鼻気管炎・角結膜炎・角膜潰瘍を生じる。"
        pen = "FHV-1 replicates in upper-respiratory, conjunctival and corneal epithelium causing epithelial necrosis and ulceration; latency in the trigeminal ganglion persists for life and reactivates under stress or corticosteroids, driving recurrent rhinotracheitis and keratoconjunctivitis."
    elif sp == "dog":
        cja = "犬ヘルペスウイルス1型（CHV-1）の感染による。経胎盤・産道感染や口鼻分泌物・交尾を介して伝播し、体温の低い新生子で急速に増殖する。"
        cen = "Caused by canine herpesvirus-1 (CHV-1), transmitted transplacentally, through the birth canal, oronasal secretions and venereally; it replicates best at the low body temperature of neonates."
        pja = "CHV-1は低体温の新生子で全身に播種し、血管内皮傷害と多臓器（腎・肝・肺）の巣状壊死・出血を起こして致死的となる。成犬では潜伏感染し、上部気道・生殖器の軽症にとどまることが多い。"
        pen = "In hypothermic neonates CHV-1 disseminates systemically, injuring vascular endothelium and producing multifocal necrosis and haemorrhage in kidney, liver and lung with high mortality; adults develop latent infection with mild respiratory or genital disease."
    elif sp == "horse":
        cja = "馬ヘルペスウイルス（EHV-1／EHV-4）の感染による。呼吸器飛沫・接触・流産胎子や胎盤を介して伝播し、感染馬は神経節に潜伏感染して再活性化する。"
        cen = "Caused by equine herpesvirus (EHV-1/EHV-4), spread by respiratory aerosol, contact and aborted fetal/placental material; infected horses harbour latent virus that can reactivate."
        pja = "EHVは呼吸器上皮で複製後、白血球関連ウイルス血症を介して妊娠子宮内膜や中枢神経の血管内皮に感染する。血管炎・血栓形成により流産・新生子死・馬ヘルペス脊髄脳症（EHM）を生じる。"
        pen = "EHV replicates in respiratory epithelium, then via leukocyte-associated viraemia infects endothelium of the pregnant endometrium and CNS; the resulting vasculitis and thrombosis cause abortion, neonatal death and equine herpesvirus myeloencephalopathy."
    elif sp in _BIRDS:
        cja = f"{j}に病原性を示すヘルペスウイルス（オウム目ではPacheco病を起こすサイタシドヘルペスウイルス等）の感染による。糞・呼吸器分泌物やキャリア鳥を介して伝播する。"
        cen = f"Caused by a host-adapted herpesvirus of {e} (in psittacines, the psittacid herpesvirus causing Pacheco's disease), spread via faeces, respiratory secretions and carrier birds."
        pja = "ヘルペスウイルスは肝・脾を主標的に急性壊死性病変を起こし、しばしば前駆症状を欠いて突然死する。回復鳥はキャリアとなりウイルスを排出し続ける。"
        pen = "The herpesvirus targets liver and spleen, producing acute necrotising lesions and frequently sudden death with few premonitory signs; survivors become carriers that continue to shed."
    else:
        cja = f"{j}に感染する宿主適応型ヘルペスウイルスによる。分泌物を介した直接接触で伝播し、感染後は神経節等に潜伏してストレス時に再活性化する。"
        cen = f"Caused by a host-adapted herpesvirus of {e}, spread by direct contact with secretions; the virus persists as a latent infection and reactivates under stress."
        pja = "ヘルペスウイルスは上皮で複製して局所の壊死・潰瘍を起こし、神経節への潜伏感染が生涯持続して再発の原因となる。"
        pen = "The herpesvirus replicates in epithelium causing local necrosis and ulceration, and establishes lifelong ganglionic latency that underlies recurrence."
    return cja, cen, pja, pen


def _parvovirus(sp: str):
    j, e = _ja(sp), _en(sp)
    name_l = ""  # host branch decides the strain
    if sp == "cat":
        cja = "猫パルボウイルス（猫汎白血球減少症ウイルス, FPV）の感染による。糞口感染および汚染環境・器材を介して伝播し、ウイルスは環境中で長期間安定に残存する。"
        cen = "Caused by feline parvovirus (feline panleukopenia virus, FPV), transmitted by the faecal-oral route and via contaminated environment and fomites; the virus is highly stable in the environment."
        pja = "FPVは分裂の盛んな細胞（腸陰窩上皮・骨髄前駆細胞・胎子/新生子の小脳）を破壊し、重度の腸炎・汎白血球減少・敗血症を、周産期感染では小脳低形成を引き起こす。"
        pen = "FPV destroys rapidly dividing cells — intestinal crypt epithelium, bone-marrow precursors and the fetal/neonatal cerebellum — causing severe enteritis, panleukopenia and sepsis, and cerebellar hypoplasia after perinatal infection."
    elif sp == "dog":
        cja = "犬パルボウイルス2型（CPV-2 およびその変異株 2a/2b/2c）の感染による。糞口感染・汚染環境で伝播し、環境抵抗性が高い。"
        cen = "Caused by canine parvovirus type 2 (CPV-2 and its variants 2a/2b/2c), transmitted faecal-orally and through a highly resistant contaminated environment."
        pja = "CPV-2は腸陰窩上皮と骨髄前駆細胞を標的に破壊し、出血性腸炎・好中球減少・細菌トランスロケーションによる敗血症を起こす。幼齢では心筋炎型もみられる。"
        pen = "CPV-2 targets and destroys intestinal crypt epithelium and bone-marrow precursors, producing haemorrhagic enteritis, neutropenia and sepsis from bacterial translocation; a myocarditic form occurs in very young pups."
    else:
        cja = f"{j}に感染するパルボウイルスによる。糞口感染・汚染環境を介して伝播し、環境中で安定に残存する。"
        cen = f"Caused by a parvovirus of {e}, transmitted faecal-orally and via a stable, resistant contaminated environment."
        pja = "パルボウイルスは分裂の盛んな腸陰窩上皮・骨髄前駆細胞を破壊し、腸炎と汎血球減少・免疫抑制を起こす。"
        pen = "The parvovirus destroys rapidly dividing intestinal crypt epithelium and bone-marrow precursors, causing enteritis with pancytopenia and immunosuppression."
    _ = name_l
    return cja, cen, pja, pen


def _distemper(sp: str):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のジステンパーは犬ジステンパーウイルス（CDV, モルビリウイルス属）の感染による。呼吸器エアロゾル・分泌物を介して伝播する。"
    cen = f"Caused by canine distemper virus (CDV, a morbillivirus), spread by respiratory aerosol and secretions among {e}."
    pja = "CDVはリンパ組織で複製して重度の免疫抑制を起こした後、上皮（呼吸器・消化器）と中枢神経に播種する。二次感染を伴う呼吸器・消化器症状、硬蹠症、脱髄性脳脊髄炎による神経症状を生じる。"
    pen = "CDV replicates in lymphoid tissue causing marked immunosuppression, then spreads to respiratory/gastrointestinal epithelium and the CNS, producing respiratory and enteric disease with secondary infection, hyperkeratosis of foot pads, and demyelinating encephalomyelitis."
    return cja, cen, pja, pen


def _calicivirus(sp: str):
    j, e = _ja(sp), _en(sp)
    if sp == "cat":
        cja = "猫カリシウイルス（FCV）の感染による。眼鼻口分泌物を介した直接接触・飛沫・汚染器材で伝播し、回復後も持続排出するキャリアが感染源となる。"
        cen = "Caused by feline calicivirus (FCV), spread by direct contact with oral/ocular/nasal secretions, aerosol and fomites; persistently shedding carriers maintain infection."
        pja = "FCVは口腔・上部気道上皮で複製し、特徴的な口腔潰瘍・上部気道炎を起こす。高病原性全身性株（VS-FCV）では血管炎により多臓器障害・顔面/四肢浮腫・高致死率を呈する。"
        pen = "FCV replicates in oral and upper-respiratory epithelium producing the characteristic oral ulceration and rhinitis; virulent systemic strains cause vasculitis with multi-organ involvement, facial/limb oedema and high mortality."
    elif sp == "rabbit":
        cja = "ウサギ出血病ウイルス（RHDV, カリシウイルス科ラゴウイルス属）の感染による。経口・経鼻・接触や汚染物・媒介昆虫を介して伝播し、極めて感染力が強い。"
        cen = "Caused by rabbit haemorrhagic disease virus (RHDV, a lagovirus in Caliciviridae), highly contagious via oral/nasal/contact routes, fomites and insect vectors."
        pja = "RHDVは肝細胞で急速に複製して大量のアポトーシス・肝壊死を起こし、播種性血管内凝固（DIC）と多臓器出血を招いて急死させる。"
        pen = "RHDV replicates rapidly in hepatocytes causing massive hepatocyte apoptosis and necrosis, triggering disseminated intravascular coagulation and fatal multi-organ haemorrhage."
    else:
        cja = f"{j}に感染するカリシウイルスによる。分泌物を介した接触・飛沫で伝播する。"
        cen = f"Caused by a calicivirus of {e}, spread by contact with secretions and aerosol."
        pja = "カリシウイルスは上皮で複製し、粘膜のびらん・潰瘍と局所炎症を起こす。"
        pen = "The calicivirus replicates in epithelium, producing mucosal erosion/ulceration and local inflammation."
    return cja, cen, pja, pen


def _coronavirus(sp: str):
    j, e = _ja(sp), _en(sp)
    if sp == "cat":
        cja = "猫コロナウイルス（FCoV）の感染による。糞口感染で伝播し、体内で強毒変異（FIPV）を生じると猫伝染性腹膜炎（FIP）に進展する。"
        cen = "Caused by feline coronavirus (FCoV), transmitted faecal-orally; an in-host virulent mutation (FIPV) leads to feline infectious peritonitis."
        pja = "FCoVは腸上皮で複製して軽度腸炎を起こす。変異株がマクロファージ指向性を獲得すると全身に播種し、免疫複合体・血管炎による滲出型（体腔液貯留）または肉芽腫型のFIPを生じる。"
        pen = "FCoV replicates in enterocytes causing mild enteritis; a mutant acquiring macrophage tropism disseminates systemically and, via immune-complex vasculitis, produces effusive (cavitary effusion) or granulomatous FIP."
    elif sp == "dog":
        cja = "犬腸コロナウイルス（CCoV）の感染による。糞口感染で伝播し、パルボウイルス等との混合感染で重症化する。"
        cen = "Caused by canine enteric coronavirus (CCoV), transmitted faecal-orally; disease is worse with co-infection (e.g. parvovirus)."
        pja = (
            "CCoVは小腸絨毛上皮で複製して絨毛萎縮と吸収不良性下痢を起こす。単独では軽症だが混合感染で腸傷害が増悪する。"
        )
        pen = "CCoV replicates in small-intestinal villous epithelium causing villous atrophy and malabsorptive diarrhoea; usually mild alone but exacerbated by co-infection."
    else:
        cja = f"{j}に感染するコロナウイルスによる。糞口感染・接触で伝播する。"
        cen = f"Caused by a coronavirus of {e}, transmitted faecal-orally and by contact."
        pja = "コロナウイルスは腸または呼吸器上皮で複製し、上皮傷害による下痢または呼吸器症状を起こす。"
        pen = "The coronavirus replicates in enteric or respiratory epithelium, causing diarrhoea or respiratory signs from epithelial injury."
    return cja, cen, pja, pen


def _influenza(sp: str):
    j, e = _ja(sp), _en(sp)
    if sp in _BIRDS:
        cja = "鳥インフルエンザウイルス（A型インフルエンザ）の感染による。感染鳥の分泌物・糞や汚染物を介して伝播し、水禽が自然宿主となる。高病原性株（HPAI, H5・H7）は届出対象。"
        cen = "Caused by avian influenza A virus, spread via secretions/faeces of infected birds and fomites, with waterfowl as the natural reservoir; highly pathogenic strains (HPAI H5/H7) are notifiable."
        pja = "低病原性株は呼吸器・消化器に限局するが、高病原性株は全身の血管内皮・実質臓器に播種して壊死・出血・多臓器不全を起こし、急死させる。"
        pen = "Low-pathogenicity strains stay in respiratory/enteric tissue, whereas HPAI disseminates to endothelium and parenchymal organs producing necrosis, haemorrhage, multi-organ failure and sudden death."
    elif sp == "horse":
        cja = "馬インフルエンザウイルス（A型, H3N8）の感染による。呼吸器エアロゾルで極めて速く伝播する。"
        cen = "Caused by equine influenza virus (influenza A, H3N8), spread extremely rapidly by respiratory aerosol."
        pja = "ウイルスは気道上皮の線毛細胞を破壊して粘液線毛クリアランスを障害し、乾性咳・発熱を起こす。上皮バリア破綻により二次性細菌性肺炎を招きやすい。"
        pen = "The virus destroys ciliated airway epithelium, impairing mucociliary clearance and causing dry cough and fever; loss of the epithelial barrier predisposes to secondary bacterial pneumonia."
    elif sp == "dog":
        cja = "犬インフルエンザウイルス（A型, H3N8／H3N2）の感染による。呼吸器分泌物・飛沫・接触で伝播する。"
        cen = "Caused by canine influenza virus (influenza A, H3N8/H3N2), spread by respiratory secretions, aerosol and contact."
        pja = "ウイルスは気道上皮で複製して線毛障害・気道炎を起こし、二次性細菌感染で肺炎に進展しうる。"
        pen = "The virus replicates in airway epithelium causing ciliary damage and airway inflammation, which can progress to pneumonia with secondary bacterial infection."
    else:
        cja = f"{j}に感染するA型インフルエンザウイルスによる。呼吸器飛沫・接触で伝播する。"
        cen = f"Caused by an influenza A virus of {e}, spread by respiratory aerosol and contact."
        pja = "ウイルスは気道上皮で複製し、線毛障害と気道炎を起こして二次感染を招きやすい。"
        pen = "The virus replicates in airway epithelium, causing ciliary damage and airway inflammation predisposing to secondary infection."
    return cja, cen, pja, pen


def _adenovirus(sp: str):
    j, e = _ja(sp), _en(sp)
    if sp == "dog":
        cja = "犬アデノウイルス（CAV-1＝伝染性肝炎、CAV-2＝呼吸器）の感染による。CAV-1は尿・分泌物を介した経口感染、CAV-2は呼吸器飛沫で伝播する。"
        cen = "Caused by canine adenovirus — CAV-1 (infectious hepatitis, via oronasal contact with urine/secretions) or CAV-2 (respiratory, via aerosol)."
        pja = "CAV-1は血管内皮・肝細胞・腎で複製し、肝壊死・出血傾向・回復期の角膜浮腫（blue eye）を起こす。CAV-2は気道上皮に限局し犬伝染性気管気管支炎の一因となる。"
        pen = "CAV-1 replicates in vascular endothelium, hepatocytes and kidney causing hepatic necrosis, a bleeding tendency and convalescent corneal oedema ('blue eye'); CAV-2 stays in airway epithelium and contributes to infectious tracheobronchitis."
    else:
        cja = f"{j}に感染するアデノウイルスによる。糞口・呼吸器を介して伝播する。"
        cen = f"Caused by an adenovirus of {e}, transmitted by faecal-oral and respiratory routes."
        pja = "アデノウイルスは呼吸器・消化器・肝の上皮で複製し、上皮壊死と炎症を起こす。免疫抑制個体で重症化しやすい。"
        pen = "The adenovirus replicates in respiratory, enteric and hepatic epithelium causing epithelial necrosis and inflammation, with more severe disease in immunosuppressed hosts."
    return cja, cen, pja, pen


def _papillomavirus(sp: str):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}に感染する宿主特異的パピローマウイルスによる。微小な皮膚・粘膜の損傷部から直接接触・汚染物を介して感染し、若齢や免疫抑制個体で発症しやすい。"
    cen = f"Caused by a host-specific papillomavirus of {e}, entering through minor skin/mucosal abrasions by direct contact or fomites; young or immunosuppressed animals are most susceptible."
    pja = "パピローマウイルスは基底層角化細胞に感染し、上皮の過形成を誘導して乳頭腫（疣）を形成する。多くは免疫獲得により自然退縮するが、一部は扁平上皮癌への進展リスクがある。"
    pen = "The papillomavirus infects basal keratinocytes and drives epithelial hyperplasia to form papillomas (warts); most regress once immunity develops, though a minority carry a risk of progression to squamous cell carcinoma."
    return cja, cen, pja, pen


def _poxvirus(sp: str):
    j, e = _ja(sp), _en(sp)
    if sp in _BIRDS:
        cja = "鳥痘ウイルス（アビポックスウイルス）の感染による。吸血昆虫（蚊）や皮膚の傷、汚染物を介して伝播する。"
        cen = "Caused by avipoxvirus (fowlpox), transmitted by biting insects (mosquitoes), skin wounds and fomites."
        pja = "ポックスウイルスは上皮で複製し、皮膚型では無羽部の増殖性結節（乾性痘）、ジフテリー型では口腔・気道粘膜の偽膜（湿性痘）を形成して摂食・呼吸を妨げる。"
        pen = "The poxvirus replicates in epithelium, producing proliferative nodules on unfeathered skin (dry form) or diphtheritic membranes of the oral/respiratory mucosa (wet form) that impair feeding and breathing."
    else:
        cja = f"{j}に感染するポックスウイルスによる。感染動物との接触や吸血昆虫、環境を介して伝播する。"
        cen = f"Caused by a poxvirus of {e}, transmitted by contact with infected animals, biting arthropods and the environment."
        pja = "ポックスウイルスは表皮角化細胞で複製し、増殖性・潰瘍性の皮膚病変を形成する。免疫抑制個体では全身播種しうる。"
        pen = "The poxvirus replicates in epidermal keratinocytes producing proliferative, ulcerative skin lesions, and can disseminate systemically in immunosuppressed hosts."
    return cja, cen, pja, pen


def _rabies(sp: str):
    j = _ja(sp)
    cja = f"{j}の狂犬病は狂犬病ウイルス（リッサウイルス属）の感染による。感染動物の咬傷を介して唾液中のウイルスが侵入する人獣共通感染症で、日本では届出対象。"
    cen = "Caused by rabies virus (genus Lyssavirus); the virus in saliva enters through the bite of an infected animal. It is a fatal zoonosis and a notifiable disease."
    pja = "ウイルスは咬傷部の筋・神経で複製後、末梢神経を逆行性に上行して中枢神経に達し、非化膿性脳脊髄炎を起こす。唾液腺へ遠心性に移行して咬傷伝播を可能にし、発症後はほぼ致死的である。"
    pen = "The virus replicates at the bite site, then travels retrogradely up peripheral nerves to the CNS causing non-suppurative encephalomyelitis; centrifugal spread to the salivary glands enables bite transmission, and disease is almost invariably fatal once signs appear."
    return cja, cen, pja, pen


def _rotavirus(sp: str):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}に感染するロタウイルスによる。糞口感染で伝播し、環境抵抗性が高く新生子・幼齢で集団発生しやすい。"
    cen = f"Caused by a rotavirus of {e}, transmitted faecal-orally; it is environmentally stable and causes outbreaks in neonates and the young."
    pja = "ロタウイルスは小腸絨毛先端の成熟腸上皮で複製して絨毛萎縮を起こし、二糖類分解酵素の低下による浸透圧性・吸収不良性下痢と脱水を招く。"
    pen = "Rotavirus replicates in mature enterocytes at the villous tips causing villous atrophy; the resulting loss of disaccharidases produces osmotic, malabsorptive diarrhoea and dehydration."
    return cja, cen, pja, pen


def _retrovirus_felv(sp: str):
    cja = "猫白血病ウイルス（FeLV, レトロウイルス科ガンマレトロウイルス属）の感染による。唾液を主とした密接接触（相互グルーミング・咬傷・食器共有）や母子感染で伝播する。"
    cen = "Caused by feline leukaemia virus (FeLV, a gammaretrovirus), spread mainly by saliva through close contact (mutual grooming, bites, shared bowls) and from queen to kittens."
    pja = "FeLVは逆転写により宿主ゲノムに組み込まれ、骨髄・リンパ組織に持続感染する。進行性感染では骨髄抑制（貧血・白血球減少）、免疫抑制、リンパ腫・白血病を引き起こす。"
    pen = "FeLV integrates into the host genome by reverse transcription and persists in bone marrow and lymphoid tissue; progressive infection causes myelosuppression (anaemia, leukopenia), immunosuppression and lymphoma/leukaemia."
    return cja, cen, pja, pen


def _retrovirus_fiv(sp: str):
    cja = "猫免疫不全ウイルス（FIV, レトロウイルス科レンチウイルス属）の感染による。主に咬傷を介した唾液感染で伝播し、放し飼いの雄で多い。"
    cen = "Caused by feline immunodeficiency virus (FIV, a lentivirus), transmitted chiefly by bite wounds (saliva), most often in free-roaming males."
    pja = "FIVはCD4陽性Tリンパ球等に感染し、逆転写でゲノムに組み込まれて生涯持続感染する。緩徐な進行でCD4/CD8比が低下し、後天性免疫不全により日和見感染・口内炎・腫瘍の素因となる。"
    pen = "FIV infects CD4+ T-lymphocytes and integrates into the genome for lifelong infection; a slow decline in the CD4/CD8 ratio produces acquired immunodeficiency that predisposes to opportunistic infections, stomatitis and neoplasia."
    return cja, cen, pja, pen


def _paramyxovirus(sp: str):
    j, e = _ja(sp), _en(sp)
    if sp in _BIRDS:
        cja = f"{j}のパラミクソウイルス感染症（ニューカッスル病＝鳥パラミクソウイルス1型が代表）による。感染鳥の分泌物・糞や汚染物を介した接触・吸入で伝播する。"
        cen = f"Caused by an avian paramyxovirus (Newcastle disease = avian paramyxovirus-1 being the archetype) in {e}, spread by contact with and inhalation of secretions, faeces and fomites."
        pja = "ウイルスは呼吸器・消化器上皮で複製後に全身・中枢神経へ播種し、呼吸器症状・緑色下痢・捻転斜頸や旋回などの神経症状を起こす。強毒株は高致死率で届出対象となる。"
        pen = "The virus replicates in respiratory/enteric epithelium then disseminates to viscera and CNS, causing respiratory signs, greenish diarrhoea and neurological disease (torticollis, circling); virulent strains are highly fatal and notifiable."
    else:
        cja = f"{j}のパラミクソウイルス感染症（げっ歯類ではセンダイウイルス等）による。呼吸器飛沫・接触で伝播し、密飼いで急速に広がる。"
        cen = f"Caused by a paramyxovirus of {e} (e.g. Sendai virus in rodents), spread by respiratory aerosol and contact and spreading rapidly in crowding."
        pja = "ウイルスは気道上皮で複製して線毛障害と間質性肺炎を起こし、二次性細菌感染で重症化する。幼若・免疫低下個体で致死的となりうる。"
        pen = "The virus replicates in airway epithelium causing ciliary damage and interstitial pneumonia, worsened by secondary bacterial infection and potentially fatal in the young or immunosuppressed."
    return cja, cen, pja, pen


def _iridovirus(sp: str):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のイリドウイルス感染症（ラナウイルス属等）による。水・接触・被食を介して伝播し、水生・両生・爬虫類で集団死を起こす。"
    cen = f"Caused by an iridovirus (e.g. Ranavirus) of {e}, transmitted via water, contact and ingestion, and causing mass mortality in aquatic, amphibian and reptile populations."
    pja = "イリドウイルスは造血組織・内皮・上皮で複製し、全身の壊死・出血・多臓器不全を起こす。皮膚潰瘍・浮腫・体腔液貯留を伴い、しばしば急速に致死的となる。"
    pen = "The iridovirus replicates in haematopoietic tissue, endothelium and epithelium causing systemic necrosis, haemorrhage and multi-organ failure with skin ulceration, oedema and effusion — often rapidly fatal."
    return cja, cen, pja, pen


def _circovirus(sp: str):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のサーコウイルス感染症による。糞・羽毛粉塵・分泌物を介して伝播する環境抵抗性の高い小型DNAウイルスで、若齢個体で発症しやすい。"
    cen = f"Caused by a circovirus of {e}, a small, environmentally stable DNA virus spread via faeces, feather dust and secretions, with young animals most susceptible."
    pja = "サーコウイルスはリンパ組織・分裂の盛んな上皮（羽包・腸・皮膚）で複製し、免疫抑制と発育中組織の傷害を起こす。鳥では羽毛・嘴の異常、豚では削痩・リンパ組織の消耗を招く。"
    pen = "The circovirus replicates in lymphoid tissue and rapidly dividing epithelium (feather follicles, gut, skin), causing immunosuppression and injury to developing tissues — feather/beak abnormalities in birds, wasting and lymphoid depletion in pigs."
    return cja, cen, pja, pen


def _polyomavirus(sp: str):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のポリオーマウイルス感染症による。糞・分泌物・羽毛粉塵を介して伝播する小型DNAウイルスで、幼若個体で急性・致死的な経過をとりやすい。"
    cen = f"Caused by a polyomavirus of {e}, a small DNA virus spread via faeces, secretions and feather dust, often acute and fatal in the very young."
    pja = "ポリオーマウイルスは複数臓器で複製して壊死・出血を起こし、幼鳥では羽毛形成不全・皮下出血・突然死を、慢性キャリアでは持続排出を生じる。"
    pen = "The polyomavirus replicates in multiple organs causing necrosis and haemorrhage — abnormal feathering, subcutaneous haemorrhage and sudden death in nestlings, with persistent shedding in chronic carriers."
    return cja, cen, pja, pen


def _reovirus(sp: str):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のレオウイルス感染症による。糞口・接触で伝播し、免疫抑制や他病原体との混合感染で顕在化する。"
    cen = f"Caused by a reovirus of {e}, transmitted faecal-orally and by contact, becoming clinical with immunosuppression or co-infection."
    pja = "レオウイルスは腱鞘・関節・消化器・肝で複製し、腱滑膜炎・関節炎（跛行）、腸炎、発育不良を起こす。若齢個体で影響が大きい。"
    pen = "The reovirus replicates in tendon sheaths, joints, gut and liver, causing tenosynovitis/arthritis (lameness), enteritis and stunting, with the greatest impact in the young."
    return cja, cen, pja, pen


def _bornavirus(sp: str):
    j, e = _ja(sp), _en(sp)
    if sp in _BIRDS:
        cja = f"{j}の鳥ボルナウイルス（ABV）感染による。腺胃拡張症（PDD）の原因ウイルスで、糞・分泌物を介して緩慢に伝播し、無症候キャリアも多い。"
        cen = f"Caused by avian bornavirus (ABV) in {e}, the agent of proventricular dilatation disease, spread slowly via faeces/secretions with many asymptomatic carriers."
        pja = "ABVは自律神経叢・中枢神経に感染し、免疫介在性の神経節神経炎を起こす。消化管運動の障害による腺胃拡張・未消化便・削痩と、運動失調・振戦などの神経症状を生じる。"
        pen = "ABV infects autonomic ganglia and CNS provoking immune-mediated ganglioneuritis; loss of gut motility causes proventricular dilatation, undigested droppings and wasting, alongside ataxia and tremors."
    else:
        cja = f"{j}のボルナ病はボルナ病ウイルスの感染による。神経向性ウイルスで、感染経路は完全には解明されていない。"
        cen = f"Caused by Borna disease virus in {e}, a neurotropic virus whose route of transmission is incompletely understood."
        pja = "ボルナ病ウイルスは中枢神経に持続感染し、免疫介在性の非化膿性脳脊髄炎を起こして行動異常・運動失調・麻痺などの神経症状を生じる。"
        pen = "Borna disease virus persistently infects the CNS causing immune-mediated non-suppurative meningoencephalitis with behavioural change, ataxia and paresis."
    return cja, cen, pja, pen


def _aleutian(sp: str):
    j = _ja(sp)
    cja = f"{j}のアリューシャン病はアリューシャン病ウイルス（アムドパルボウイルス）の感染による。糞・尿・唾液や汚染環境を介して伝播する。"
    cen = "Caused by Aleutian disease virus (an amdoparvovirus), spread via faeces, urine, saliva and a contaminated environment."
    pja = "本ウイルスは持続感染し、抗原過剰下で形成された免疫複合体が全身の血管・腎糸球体に沈着して、多クローン性高ガンマグロブリン血症・糸球体腎炎・血管炎・進行性削痩を起こす。"
    pen = "The virus persists and, under antigen excess, drives immune-complex deposition in vessels and renal glomeruli, producing polyclonal hypergammaglobulinaemia, glomerulonephritis, vasculitis and progressive wasting."
    return cja, cen, pja, pen


def _arenavirus_lcmv(sp: str):
    j = _ja(sp)
    cja = f"{j}のリンパ球性脈絡髄膜炎はLCMウイルス（アレナウイルス）の感染による。保菌げっ歯類の尿・糞・唾液を介して伝播する人獣共通感染症。"
    cen = "Caused by lymphocytic choriomeningitis virus (an arenavirus), transmitted via the urine, faeces and saliva of reservoir rodents — a zoonosis."
    pja = "LCMVは中枢神経の脈絡叢・髄膜で複製し、免疫介在性の髄膜炎・脈絡膜炎を起こす。周産期感染では持続感染・成長遅延を、宿主外感染では髄膜炎症状を生じる。"
    pen = "LCMV replicates in the choroid plexus and meninges provoking immune-mediated meningitis/choroiditis; perinatal infection leads to persistence and stunting, while later infection causes meningeal disease."
    return cja, cen, pja, pen


def _flavivirus(sp: str):
    j = _ja(sp)
    cja = f"{j}のフラビウイルス性脳炎（ウエストナイル熱・日本脳炎等）は蚊が媒介するフラビウイルスの感染による。鳥類が増幅動物となり、蚊の吸血で哺乳類・馬に伝播する人獣共通感染症。"
    cen = "Caused by a mosquito-borne flavivirus (West Nile, Japanese encephalitis); birds amplify the virus and mosquitoes transmit it to mammals and horses — a zoonosis."
    pja = "ウイルスは吸血で侵入後に増殖・ウイルス血症を経て中枢神経に到達し、神経細胞に感染して非化膿性脳脊髄炎を起こす。運動失調・筋振戦・麻痺・起立不能などの神経症状を生じる。"
    pen = "After a mosquito bite the virus amplifies, produces viraemia and reaches the CNS, infecting neurons to cause non-suppurative encephalomyelitis with ataxia, muscle tremors, paresis and recumbency."
    return cja, cen, pja, pen


def _eia(sp: str):
    cja = "馬伝染性貧血（EIA, スワンプフィーバー）はレンチウイルス（レトロウイルス科）の感染による。アブ等の吸血昆虫や汚染注射器・輸血を介して機械的に伝播する。日本では届出対象で根治療法はない。"
    cen = "Caused by equine infectious anaemia virus (a lentivirus); it is transmitted mechanically by biting flies (tabanids), contaminated needles and transfusion. It is reportable with no curative therapy."
    pja = "ウイルスはマクロファージに持続感染し、抗原変異を繰り返す。免疫介在性の赤血球破壊と血小板減少・血管炎により反復する発熱・貧血・浮腫・削痩を起こし、感染馬は生涯キャリアとなる。"
    pen = "The virus persistently infects macrophages and undergoes antigenic variation; immune-mediated red-cell destruction, thrombocytopenia and vasculitis produce recurrent fever, anaemia, oedema and wasting, and infected horses remain lifelong carriers."
    return cja, cen, pja, pen


def _eva(sp: str):
    cja = "馬ウイルス性動脈炎（EVA）はエクウイアルテリウイルス（アルテリウイルス）の感染による。呼吸器飛沫や、持続感染した種雄馬の精液を介した交配・人工授精で伝播する。"
    cen = "Caused by equine arteritis virus (an arterivirus), spread by respiratory aerosol and, importantly, via the semen of persistently infected stallions during breeding/AI."
    pja = "ウイルスは血管内皮・中膜平滑筋に感染して壊死性血管炎（動脈炎）を起こし、浮腫（四肢・陰嚢）・結膜炎・発熱を生じる。妊娠馬では胎盤血管障害により流産を招き、種雄馬は持続排出源となる。"
    pen = "The virus infects vascular endothelium and medial smooth muscle causing necrotising arteritis with oedema (limbs/scrotum), conjunctivitis and fever; in mares placental vascular injury causes abortion, and stallions become persistent shedders."
    return cja, cen, pja, pen


def _birnavirus(sp: str):
    j = _ja(sp)
    cja = f"{j}の伝染性ファブリキウス嚢病（ガンボロ病）は伝染性ファブリキウス嚢病ウイルス（ビルナウイルス）による。糞口感染で伝播し、環境抵抗性が極めて高い。"
    cen = "Caused by infectious bursal disease virus (a birnavirus); transmitted faecal-orally and extremely resistant in the environment (Gumboro disease)."
    pja = "ウイルスはファブリキウス嚢のBリンパ球を破壊して重度の免疫抑制を起こし、ワクチン不応・二次感染の素因となる。急性型では出血・脱水・腎障害を伴う。"
    pen = "The virus destroys B-lymphocytes in the bursa of Fabricius causing profound immunosuppression that impairs vaccine response and predisposes to secondary infection; the acute form adds haemorrhage, dehydration and renal injury."
    return cja, cen, pja, pen


def _henipavirus(sp: str):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のヘンドラ／ニパウイルス感染症はヘニパウイルス（パラミクソウイルス科）による。オオコウモリを自然宿主とし、その分泌物で汚染された飼料等を介して伝播する高病原性の人獣共通感染症。"
    cen = f"Caused by a henipavirus (Hendra/Nipah, family Paramyxoviridae) in {e}; fruit bats are the reservoir and infection follows contact with feed/environment contaminated by bat secretions — a highly lethal zoonosis."
    pja = "ウイルスは血管内皮に親和性を持ち、全身性の血管炎・血栓と、呼吸器・中枢神経の傷害を起こす。重度の呼吸器症状と脳炎を呈し致死率が高い。取扱いには厳重なバイオセーフティを要する。"
    pen = "The virus is endotheliotropic, causing systemic vasculitis and thrombosis with respiratory and CNS injury; severe respiratory disease and encephalitis carry high mortality, and handling demands strict biosafety."
    return cja, cen, pja, pen


def _hantavirus(sp: str):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のハンタウイルス感染症はハンタウイルス（ブニヤウイルス目）による。保菌げっ歯類の尿・糞・唾液のエアロゾル吸入で伝播する人獣共通感染症で、げっ歯類自身はほぼ無症状のキャリアとなる。"
    cen = f"Caused by a hantavirus (order Bunyavirales) in {e}, transmitted by inhaling aerosolised urine/faeces/saliva of reservoir rodents — a zoonosis in which the rodent host is a largely asymptomatic carrier."
    pja = "ハンタウイルスは血管内皮に感染して血管透過性亢進を起こす。げっ歯類では持続感染・排出が続き、ヒトでは腎症候性出血熱や肺症候群の原因となるため公衆衛生上重要。"
    pen = "Hantaviruses infect vascular endothelium increasing vascular permeability; rodents shed persistently while human infection causes haemorrhagic fever with renal syndrome or pulmonary syndrome, making it a public-health concern."
    return cja, cen, pja, pen


# name-pattern -> generator. Order matters: more specific keys first.
_AGENTS: tuple[tuple[tuple[str, ...], object], ...] = (
    (("白血病ウイルス", "leukemia virus", "leukaemia virus", "felv"), _retrovirus_felv),
    (("免疫不全ウイルス", "immunodeficiency virus", "fiv"), _retrovirus_fiv),
    (("馬伝染性貧血", "equine infectious an", "swamp fever"), _eia),
    (("馬ウイルス性動脈炎", "equine viral arteritis"), _eva),
    (("アリューシャン", "aleutian"), _aleutian),
    (("脈絡髄膜炎", "choriomeningitis", "lcmv"), _arenavirus_lcmv),
    (("ハンタウイルス", "hantavirus"), _hantavirus),
    (("ヘンドラ", "hendra", "ニパ", "nipah", "henipavirus"), _henipavirus),
    (("ウエストナイル", "west nile", "日本脳炎", "japanese encephalitis", "flavivirus"), _flavivirus),
    (("ファブリキウス嚢", "infectious bursal", "gumboro", "ガンボロ", "birnavirus"), _birnavirus),
    (("ボルナ", "borna"), _bornavirus),
    (
        (
            "イリドウイルス",
            "iridovirus",
            "ラナウイルス",
            "ranavirus",
            "カエルウイルス",
            "frog virus 3",
            "ambystoma tigrinum",
        ),
        _iridovirus,
    ),
    (("サーコウイルス", "circovirus", "嘴羽毛", "beak and feather", "pbfd"), _circovirus),
    (("ポリオーマ", "polyomavirus"), _polyomavirus),
    (("レオウイルス", "reovirus"), _reovirus),
    (
        (
            "ニューカッスル",
            "newcastle",
            "パラミクソ",
            "paramyxo",
            "センダイ",
            "sendai",
            "メタニューモ",
            "metapneumovirus",
        ),
        _paramyxovirus,
    ),
    (("マレック", "marek", "伝染性喉頭気管炎", "laryngotracheitis", "サイトメガロ", "cytomegalo"), _herpesvirus),
    # Parvovirus/panleukopenia BEFORE distemper: feline panleukopenia is named
    # "Feline Panleukopenia (Feline Distemper)" and must resolve to FPV, not CDV.
    (("パルボ", "parvo", "汎白血球減少", "panleukopenia"), _parvovirus),
    (("ジステンパー", "distemper"), _distemper),
    (("ヘルペス", "herpes", "鼻気管炎", "rhinotracheitis", "pacheco"), _herpesvirus),
    # "カリシウイルス"/"calicivirus" (not bare "カリシ"/"calici") so "カリシン過敏症"
    # (Culicoides hypersensitivity) is not miscaught.
    (
        (
            "カリシウイルス",
            "calicivirus",
            "ノロウイルス",
            "norovirus",
            "ウサギ出血",
            "rabbit haemorrhagic",
            "rabbit hemorrhagic",
            "rhdv",
        ),
        _calicivirus,
    ),
    (
        ("コロナ", "coronavirus", "伝染性腹膜炎", "infectious peritonitis", "伝染性気管支炎", "infectious bronchitis"),
        _coronavirus,
    ),
    (("インフルエンザ", "influenza"), _influenza),
    # "adenovirus" (not bare "adeno") so adenoma/adenocarcinoma are not miscaught.
    (("アデノ", "adenovirus", "伝染性肝炎", "infectious canine hepatitis"), _adenovirus),
    (("パピローマ", "papilloma", "乳頭腫ウイルス", "wart"), _papillomavirus),
    # "痘"/"poxvirus"/named pox (not bare "pox") so "hypoxia" is not miscaught.
    (("痘", "ポックス", "poxvirus", "fowlpox", "fowl pox", "cowpox"), _poxvirus),
    (("狂犬病", "rabies", "lyssa"), _rabies),
    (("ロタ", "rotavir"), _rotavirus),
)


def resolve_viral_agent(name_ja: str, name_en: str):
    """Return the generator for a named-pathogen viral disease, or None.

    Negated names (``"Feline Keratitis (Non-Herpetic)"`` / ``"非ヘルペス性"``) are
    neutralised first so an explicitly *non*-viral disease is never matched.
    """
    name = _neutralise_negations(f"{name_ja or ''} {name_en or ''}").lower()
    for keys, gen in _AGENTS:
        if any(k.lower() in name for k in keys):
            return gen
    return None


def viral_clinical_fields(species: str, name_ja: str, name_en: str) -> dict | None:
    """Curated causes / pathophysiology (JA+EN) for a named-pathogen viral
    disease, or None when the name does not resolve to a known virus."""
    gen = resolve_viral_agent(name_ja, name_en)
    if gen is None:
        return None
    species = (species or "").lower()
    # FeLV / FIV are feline-specific; do not stamp feline retrovirus prose onto a
    # non-cat lentivirus (e.g. simian immunodeficiency virus in an exotic entry).
    if gen in (_retrovirus_felv, _retrovirus_fiv) and species != "cat":
        return None
    cja, cen, pja, pen = gen(species)
    return {
        "causes_ja": cja,
        "causes": cen,
        "pathophysiology_ja": pja,
        "pathophysiology": pen,
    }
