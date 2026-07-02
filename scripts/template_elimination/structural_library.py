"""Curated etiology / pathophysiology for structural & mechanical diseases.

Companion to the pathogen / nutrient / flagship libraries. A large group of
purely *mechanical / structural* conditions — bladder stones, organ prolapse,
crop stasis, gastrointestinal impaction and foreign bodies, visceral torsion,
gland impaction, dystocia / egg binding, beak & hoof overgrowth — shipped an
**incorrect infection / toxicosis / parasite category template** in ``causes``
and ``pathophysiology`` (e.g. dog *Bladder Stones* described as "caused by a
bacterial pathogen invading the body"). These conditions are not infectious;
their mechanism is a textbook, largely species-general fact (a stone is a
concretion, a prolapse is a protrusion, an impaction is an obstruction), so it
is curated here with zero fabrication risk.

Generators return mechanism-specific ``causes`` + ``pathophysiology`` (JA + EN),
species name interpolated and species-specific caveats added where clinically
important (rabbit GI stasis → hepatic lipidosis risk, reptile uroliths →
dehydration / husbandry, herbivore ileus → fibre). Only category-template / stub
fields are overwritten by the caller (``fix_named_pathogens`` / the served-DB
safety net), so any genuinely curated prose (e.g. the rabbit hepatic-lobe-torsion
pathophysiology) is preserved.

References: Ettinger & Feldman, *Textbook of Veterinary Internal Medicine* 8th
ed; Quesenberry & Carpenter, *Ferrets, Rabbits and Rodents* 4th ed; Carpenter,
*Exotic Animal Formulary* 6th ed; Mader, *Reptile Medicine and Surgery* 3rd ed;
Harrison & Lightfoot, *Clinical Avian Medicine*.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    SPECIES_EN,
    SPECIES_JA,
)

_HERBIVORE = {"rabbit", "chinchilla", "guinea_pig", "degu"}
_BIRD = {"bird", "parakeet", "parrot"}
_REPTILE = {"reptile", "tortoise", "snake", "lizard"}


def _ja(sp: str) -> str:
    return SPECIES_JA.get(sp, sp)


def _en(sp: str) -> str:
    return SPECIES_EN.get(sp, sp)


def _en_name(name_en: str, fallback: str) -> str:
    """English display name for use inside English prose. Falls back to a generic
    label when the record's English name is empty or actually holds Japanese
    (some newly-added entries have a CJK ``name``), so English sentences never
    embed Japanese."""
    n = (name_en or "").strip()
    if not n or any("　" <= c <= "鿿" for c in n):
        return fallback
    return n


def _strip_species_suffix(name: str, sp: str) -> str:
    """Drop a trailing parenthetical that merely repeats the species name
    (e.g. "膀胱結石（トカゲ）" → "膀胱結石") so interpolated prose does not read
    "トカゲの膀胱結石（トカゲ）は…"; keeps informative parentheticals."""
    if not name:
        return name
    sp_ja = SPECIES_JA.get(sp, "")
    sp_en = (SPECIES_EN.get(sp, "") or "").rstrip("s")
    import re

    for open_p, close_p in (("（", "）"), ("(", ")")):
        m = re.search(rf"\s*{re.escape(open_p)}([^{re.escape(close_p)}]*){re.escape(close_p)}\s*$", name)
        if m:
            inner = m.group(1).strip().lower()
            if inner in {sp_ja.lower(), sp_en.lower()} or (sp_ja and sp_ja in m.group(1)):
                return name[: m.start()].rstrip()
    return name


# --- Urolithiasis ---------------------------------------------------------- #
def _urolithiasis(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    name = f"{nj or ''} {ne or ''}".lower()
    kidney = any(k in name for k in ("nephro", "腎", "kidney"))
    cloacal = any(k in name for k in ("cloacal", "総排泄腔"))
    if kidney:
        cja = (
            f"{j}の腎結石は上部尿路（腎盂・腎実質）にミネラルが析出・凝集して形成される。"
            "尿の過飽和（脱水・飲水不足）、尿pHの偏り、慢性尿路感染、代謝異常（高カルシウム尿症）、"
            "食餌のミネラルバランス不良が主因。"
        )
        cen = (
            f"Nephroliths form when urinary minerals supersaturate and crystallise in the renal "
            f"pelvis/parenchyma of {e}. Drivers include dehydration/low water intake, abnormal urine "
            "pH, chronic urinary infection, metabolic disorders (hypercalciuria) and dietary mineral imbalance."
        )
        pja = (
            "結石が腎盂を占拠すると尿流の閉塞・水腎症・腎実質の圧排性萎縮を招き、進行性の腎機能低下を"
            "きたす。感染性結石（ストルバイト）では細菌が結石内に温存され難治性となる。"
        )
        pen = (
            "Stones occupying the renal pelvis obstruct urine flow, causing hydronephrosis and "
            "compressive parenchymal atrophy with progressive renal impairment; infection-induced "
            "(struvite) stones harbour bacteria within the matrix and are difficult to clear."
        )
        return cja, cen, pja, pen
    site_ja = "総排泄腔・膀胱" if cloacal else "膀胱・尿道"
    site_en = "cloaca/bladder" if cloacal else "bladder and urethra"
    extra_ja = ""
    extra_en = ""
    if sp in _REPTILE:
        extra_ja = "爬虫類では慢性脱水・不適切な温度勾配・シュウ酸塩の多い食餌が強い素因となる。"
        extra_en = " In reptiles chronic dehydration, poor thermal gradients and oxalate-rich diets are major predisposing factors."
    elif sp in _HERBIVORE:
        extra_ja = "草食動物ではカルシウム代謝の特性（過剰カルシウムを尿中排泄）とカルシウム過剰食が炭酸カルシウム結石を招きやすい。"
        extra_en = " Herbivores excrete excess calcium in urine and readily form calcium-carbonate stones on high-calcium diets."
    cja = (
        f"{j}の{nj or '尿石症'}は尿中ミネラルが過飽和して{site_ja}に結石（ストルバイト・シュウ酸カルシウム・"
        f"尿酸塩等）を形成する。飲水不足・脱水、尿pHの偏り、尿路感染、食餌のミネラル過剰、尿停滞が原因。{extra_ja}"
    )
    cen = (
        f"Urolithiasis in {e} arises when urinary minerals supersaturate and precipitate as calculi "
        f"(struvite, calcium oxalate, urate) in the {site_en}. Causes include inadequate water intake/"
        f"dehydration, abnormal urine pH, urinary infection, dietary mineral excess and urine stasis.{extra_en}"
    )
    pja = (
        "結石が尿路粘膜を機械的に刺激して血尿・排尿痛・頻尿を起こし、尿道に嵌頓すると尿路閉塞・水腎症・"
        "急性腎後性腎不全から死に至る緊急事態となる。二次的な細菌性膀胱炎を伴いやすい。"
    )
    pen = (
        "Calculi mechanically irritate the urothelium (haematuria, dysuria, pollakiuria); a stone "
        "lodged in the urethra causes obstruction, hydronephrosis and life-threatening post-renal "
        "azotaemia, and secondary bacterial cystitis is common."
    )
    return cja, cen, pja, pen


# --- Rectal / cloacal / intestinal prolapse -------------------------------- #
def _gi_prolapse(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    name = f"{nj or ''} {ne or ''}".lower()
    cloacal = any(k in name for k in ("cloac", "総排泄腔"))
    organ_ja = "総排泄腔（直腸・排泄腔組織）" if cloacal else "直腸"
    organ_en = "cloaca (rectum/cloacal tissue)" if cloacal else "rectum"
    cja = (
        f"{j}の{nj or '脱出'}は持続的な努責・腹圧上昇により{organ_ja}が肛門/総排泄腔から外反・脱出する病態。"
        "重度の下痢・便秘・しぶり、腸内寄生虫、消化管閉塞・異物、難産、泌尿生殖器疾患、直腸腫瘤が誘因となる。"
    )
    cen = (
        f"{_en_name(ne, 'Prolapse')} in {e} is eversion of the {organ_en} through the anus/vent driven by "
        "sustained straining and raised intra-abdominal pressure — from severe diarrhoea, constipation "
        "or tenesmus, enteric parasites, GI obstruction/foreign body, dystocia, urogenital disease or a rectal mass."
    )
    pja = (
        "反復する努責が直腸を支持する組織（骨盤隔膜・筋膜）を弛緩させ、粘膜または全層が脱出する。脱出部は"
        "浮腫・うっ血・乾燥・潰瘍化し、放置すると絞扼・壊死に至るため早期整復が必要。"
    )
    pen = (
        "Repeated straining weakens the pelvic supporting tissues, allowing mucosal or full-thickness "
        "protrusion; the exposed segment becomes oedematous, congested and ulcerated and, untreated, "
        "strangulates and necroses — early reduction is required."
    )
    return cja, cen, pja, pen


# --- Reproductive (uterine / vaginal / oviductal) prolapse ----------------- #
def _repro_prolapse(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    name = f"{nj or ''} {ne or ''}".lower()
    oviduct = any(k in name for k in ("oviduct", "卵管", "reproductive tract")) and sp in (_BIRD | _REPTILE)
    if oviduct:
        cja = (
            f"{j}の生殖器脱は産卵に伴う卵管（輸卵管）の過度な努責・弛緩により卵管が総排泄腔から脱出する病態。"
            "難産（卵塞）、慢性の過剰産卵、低カルシウム血症による子宮/卵管筋の収縮不全、卵管炎が誘因。"
        )
        cen = (
            f"Oviductal/reproductive-tract prolapse in {e} is protrusion of the oviduct through the vent "
            "from excessive straining during egg-laying — dystocia (egg binding), chronic over-production, "
            "hypocalcaemia impairing oviductal muscle tone, or salpingitis."
        )
        pja = (
            "産卵時の強い怒責で卵管が反転・脱出し、脱出組織は急速に浮腫・乾燥・壊死する。総排泄腔からの持続的"
            "脱出は自咬・感染・ショックを招く緊急疾患。"
        )
        pen = (
            "Violent egg-laying effort everts the oviduct; the prolapsed tissue rapidly becomes oedematous, "
            "desiccated and necrotic, and persistent protrusion invites self-trauma, infection and shock — an emergency."
        )
        return cja, cen, pja, pen
    cja = (
        f"{j}の{nj or '子宮/膣脱'}は分娩・出産に伴う過度の努責と生殖器支持組織の弛緩により、子宮または膣壁が"
        "陰部から反転・脱出する病態。難産、遷延分娩、低カルシウム血症、多胎が主な誘因。"
    )
    cen = (
        f"{_en_name(ne, 'Uterine/vaginal prolapse')} in {e} is eversion of the uterus or vaginal wall through "
        "the vulva after parturition, from excessive straining and lax reproductive support — dystocia, "
        "prolonged labour, hypocalcaemia and large litters."
    )
    pja = (
        "産褥期の子宮/膣が怒責で外反・脱出し、脱出組織のうっ血・浮腫・乾燥・裂傷が進む。子宮動脈の断裂による"
        "出血やショック、二次感染のリスクが高く、緊急整復・処置を要する。"
    )
    pen = (
        "The post-partum uterus/vagina everts under straining and the exposed tissue becomes congested, "
        "oedematous and lacerated; rupture of uterine vessels causes haemorrhage and shock with high risk "
        "of secondary infection, demanding emergency reduction."
    )
    return cja, cen, pja, pen


def _penile_prolapse(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    cja = (
        f"{j}の陰茎/半陰茎脱は交尾・排泄時の逸脱後に、腫脹・乾燥・筋の疲弊により陰茎（爬虫類では半陰茎）が"
        "退縮できず露出したままとなる病態。感染・外傷・便秘/結石による努責、神経障害が誘因。"
    )
    cen = (
        f"Penile/hemipenal prolapse in {e} is failure of the penis (hemipenis in reptiles) to retract "
        "after protrusion, from swelling, desiccation and muscular exhaustion; infection, trauma, straining "
        "(constipation/calculi) and neurological deficits predispose."
    )
    pja = (
        "露出した勃起組織は速やかに浮腫・乾燥・裂傷・壊死を起こし、尿道閉塞や自咬を伴う。整復不能例では"
        "部分切除（爬虫類の半陰茎は片側切除可）が必要。"
    )
    pen = (
        "The exposed erectile tissue rapidly swells, dries, lacerates and necroses, with urethral "
        "obstruction and self-trauma; irreducible cases require amputation (a single reptile hemipenis "
        "can be removed)."
    )
    return cja, cen, pja, pen


def _organ_prolapse_generic(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    cja = (
        f"{j}の臓器脱（胃・腸・総排泄腔）は総排泄腔から胃腸管や排泄腔組織が脱出する病態で、重度の努責・"
        "腹圧上昇（消化管閉塞・便秘・寄生虫・産卵困難・環境ストレス）により生じる。"
    )
    cen = (
        f"Organ prolapse (gastric/intestinal/cloacal) in {e} is protrusion of GI or cloacal tissue "
        "through the vent, driven by severe straining and raised intra-abdominal pressure (GI obstruction, "
        "constipation, parasites, dystocia, environmental stress)."
    )
    pja = (
        "脱出した臓器は浮腫・うっ血・乾燥・壊死へ進行し、脱出源の鑑別（直腸か胃腸重積か）が治療方針を決める。"
        "早期の整復・支持療法が予後を左右する。"
    )
    pen = (
        "Prolapsed viscera progress to oedema, congestion, desiccation and necrosis; identifying the "
        "prolapsed origin (rectum vs intussuscepted gut) guides therapy, and early reduction with "
        "supportive care determines outcome."
    )
    return cja, cen, pja, pen


# --- Foreign body ---------------------------------------------------------- #
def _foreign_body(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    name = f"{nj or ''} {ne or ''}".lower()
    if "nasal" in name or "鼻" in name:
        cja = (
            f"{j}の鼻腔異物は草片・種子・牧草片などが鼻腔に迷入し、機械的刺激と二次感染を起こす。くしゃみ・"
            "片側性鼻汁・鼻出血・前肢での鼻擦りが特徴。"
        )
        cen = (
            f"A nasal foreign body in {e} — grass awn, seed or hay fragment lodged in the nasal cavity — "
            "causes mechanical irritation and secondary infection, with sneezing, unilateral nasal "
            "discharge, epistaxis and pawing at the nose."
        )
        pja = "異物が鼻粘膜を刺激して炎症・化膿性鼻汁を生じ、遺残すると慢性鼻炎・鼻道破壊に至る。"
        pen = (
            "The object irritates the nasal mucosa producing inflammation and mucopurulent discharge; if "
            "retained it causes chronic rhinitis and turbinate destruction."
        )
        return cja, cen, pja, pen
    if "foot" in name or "sole" in name or "蹄" in name:
        cja = (
            f"{j}の趾/蹄異物は釘・木片・石などが蹄底・蹄叉から刺入し、深部組織（蹄真皮・滑液包・遠位指骨）を"
            "損傷して膿瘍・敗血症性滑液包炎を起こす穿通性外傷。"
        )
        cen = (
            f"A penetrating foot foreign body in {e} — nail, wood or stone driven through the sole/frog — "
            "damages deep structures (corium, bursa, distal phalanx), causing abscessation and septic bursitis."
        )
        pja = (
            "刺入路に沿って細菌が深部組織へ持ち込まれ、化膿・跛行・骨/滑液包感染を招く。刺入物の深達度が予後を決める。"
        )
        pen = (
            "Bacteria are carried along the tract into deep tissue, causing suppuration, lameness and "
            "bone/bursal infection; the depth of penetration determines prognosis."
        )
        return cja, cen, pja, pen
    if any(k in name for k in ("gizzard", "ventricular", "砂嚢", "筋胃")):
        cja = (
            f"{j}の筋胃（砂嚢）異物は金属片・ワイヤー・砂利などを摂取し、筋胃に貯留して機械的閉塞や重金属中毒"
            "（鉛・亜鉛）を起こす。放し飼い・退屈・栄養欠乏による異食が誘因。"
        )
        cen = (
            f"A ventricular (gizzard) foreign body in {e} — swallowed metal, wire or grit retained in the "
            "gizzard — causes mechanical obstruction and heavy-metal toxicosis (lead, zinc); free-ranging, "
            "boredom and nutritional pica predispose."
        )
        pja = "異物が筋胃を占拠・穿孔し、通過障害と粘膜損傷を起こす。金属異物は溶出して鉛/亜鉛中毒を併発しうる。"
        pen = (
            "The object occupies or perforates the gizzard, obstructing transit and damaging mucosa; "
            "metallic items leach to cause concurrent lead/zinc toxicosis."
        )
        return cja, cen, pja, pen
    cja = (
        f"{j}の消化管異物は消化できない物体（玩具・布・骨・植物繊維・毛球）を摂取し、胃・腸管に停滞または"
        "閉塞を起こす。異食・退屈・食餌管理不良が誘因。線状異物は腸重積・穿孔のリスクが高い。"
    )
    cen = (
        f"A gastrointestinal foreign body in {e} is ingestion of indigestible material (toys, fabric, "
        "bone, plant fibre, hair) that lodges or obstructs the stomach/intestine; pica, boredom and poor "
        "husbandry predispose, and linear foreign bodies risk plication and perforation."
    )
    pja = (
        "異物が管腔を閉塞すると口側の拡張・嘔吐・脱水・電解質異常を招き、圧迫壊死や線状異物の切創で腸穿孔・"
        "腹膜炎に至る外科的緊急疾患。"
    )
    pen = (
        "Luminal obstruction causes oral-side distension, vomiting, dehydration and electrolyte "
        "derangement; pressure necrosis or a linear foreign body sawing through the wall leads to "
        "perforation and peritonitis — a surgical emergency."
    )
    return cja, cen, pja, pen


# --- Crop stasis / impaction (birds) --------------------------------------- #
def _crop_disorder(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    name = f"{nj or ''} {ne or ''}".lower()
    proventric = any(k in name for k in ("proventric", "前胃", "腺胃"))
    sour = any(k in name for k in ("sour", "サワー"))
    site_ja = "前胃（腺胃）" if proventric else "そ嚢"
    site_en = "proventriculus" if proventric else "crop"
    cja = (
        f"{j}の{nj or 'そ嚢停滞'}は{site_ja}の運動低下・排出遅延により内容物が停滞・貯留する病態。"
        "低温・不適切な給餌（過度に濃厚/低温の流動食）、脱水、異物・繊維の過食、基礎疾患（感染・全身疾患）、"
        "神経筋障害が誘因。"
    )
    cen = (
        f"{_en_name(ne, 'Crop stasis')} in {e} is delayed emptying of the {site_en} with retention of contents, "
        "from hypothermia, improper hand-feeding (over-thick/cold formula), dehydration, ingested foreign "
        "material/coarse fibre, underlying infection/systemic disease or neuromuscular dysfunction."
    )
    if sour:
        pja = (
            "停滞した内容が発酵し、二次的な酵母（カンジダ）・細菌の異常増殖（サワークロップ）を招く。ガス産生・"
            "悪臭・逆流を伴い、放置すると誤嚥・敗血症へ進行する。停滞は原因であって一次感染ではない。"
        )
        pen = (
            "Retained ingesta ferments, driving secondary yeast (Candida) and bacterial overgrowth (sour "
            "crop) with gas, malodour and regurgitation; untreated it progresses to aspiration and sepsis. "
            "Stasis is the primary event, not a primary infection."
        )
    else:
        pja = (
            "運動低下により内容が停滞・脱水固化し、伸展した壁の血流障害・二次的な微生物異常増殖を生じる。"
            "重度では通過障害・誤嚥・栄養不良に至り、雛では成長停止を招く。"
        )
        pen = (
            "Reduced motility lets contents stagnate and desiccate, compromising the distended wall and "
            "allowing secondary microbial overgrowth; severe cases obstruct, aspirate and starve, and "
            "nestlings fail to thrive."
        )
    return cja, cen, pja, pen


# --- Cheek pouch impaction (hamster) --------------------------------------- #
def _cheek_pouch(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    cja = (
        f"{j}の頬袋閉塞は頬袋に食物・敷材が過剰に詰まり排出できなくなる機械的疾患。粘着性の餌、鋭利/繊維状の"
        "敷材、頬袋膿瘍・腫瘍・脱出が誘因となる。"
    )
    cen = (
        f"Cheek pouch impaction in {e} is a mechanical accumulation of food/bedding that cannot be emptied; "
        "sticky feeds, sharp or fibrous bedding, and pouch abscess, neoplasia or eversion predispose."
    )
    pja = "貯留内容が頬袋を伸展・圧迫して粘膜損傷・二次感染を起こし、摂食障害・削痩を招く。用手排出と原因除去が必要。"
    pen = (
        "Retained material distends and compresses the pouch, causing mucosal injury, secondary infection "
        "and inappetence/wasting; manual emptying and removing the cause are required."
    )
    return cja, cen, pja, pen


# --- Cecal impaction ------------------------------------------------------- #
def _cecal_impaction(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    cja = (
        f"{j}の盲腸停滞は盲腸内容が脱水・固化して通過障害を起こす病態。低繊維/高炭水化物食、飲水不足・脱水、"
        "運動不足、疼痛や基礎疾患による盲腸運動低下が原因。"
    )
    cen = (
        f"Cecal impaction in {e} is dehydration and inspissation of cecal contents with impaired transit, "
        "from low-fibre/high-carbohydrate diets, inadequate water/dehydration, inactivity and reduced "
        "cecal motility due to pain or underlying disease."
    )
    pja = "固化した内容が盲腸を拡張・閉塞し、鼓脹・腹痛・食欲廃絶・脱水を招く。草食動物では消化管うっ滞・盲腸鼓脹へ進行しうる。"
    pen = (
        "Inspissated contents distend and obstruct the cecum with bloat, abdominal pain, anorexia and "
        "dehydration; in herbivores it progresses to GI stasis and cecal tympany."
    )
    return cja, cen, pja, pen


# --- GI stasis / ileus ----------------------------------------------------- #
def _gi_stasis(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    herb = sp in _HERBIVORE
    cja = f"{j}の{nj or '消化管うっ滞'}は消化管運動が低下・停止して内容が停滞する機能性疾患。" + (
        "繊維不足・不適切な食餌、脱水、疼痛（歯科疾患・尿路結石等）、ストレス、運動不足が主因。"
        if herb
        else "食欲不振を伴う基礎疾患、疼痛、脱水、電解質異常、術後・環境ストレスが誘因。"
    )
    cen = (
        f"{_en_name(ne, 'GI stasis')} in {e} is a functional slowing/arrest of gut motility with stagnation of "
        "contents"
        + (
            ", driven by insufficient fibre, inappropriate diet, dehydration, pain (dental disease, "
            "urolithiasis), stress and inactivity."
            if herb
            else ", triggered by any anorexia-inducing disease, pain, dehydration, electrolyte imbalance and "
            "post-operative or environmental stress."
        )
    )
    if herb:
        pja = (
            "運動低下により内容が脱水・固化し、腸内細菌叢の異常発酵でガスが貯留、痛みがさらに運動を抑制する"
            "悪循環に陥る。摂食停止は肝リピドーシスを誘発し、放置すると致死的。真の緊急疾患。"
        )
        pen = (
            "Slowed motility lets contents dehydrate and impact while dysbiotic fermentation produces gas; "
            "pain further suppresses motility in a vicious cycle. Anorexia precipitates hepatic lipidosis "
            "and, untreated, is fatal — a true emergency."
        )
    else:
        pja = "運動低下で内容が停滞・脱水し、細菌異常増殖・ガス貯留・毒素吸収を招く。摂食停止と脱水が全身状態を急速に悪化させる。"
        pen = (
            "Stagnant, dehydrating contents allow bacterial overgrowth, gas accumulation and toxin "
            "absorption; anorexia and dehydration rapidly worsen the systemic state."
        )
    return cja, cen, pja, pen


# --- Trichobezoar / hairball ----------------------------------------------- #
def _trichobezoar(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    cja = (
        f"{j}の毛球症は嚥下した被毛が胃内に貯留・凝集して毛球を形成する病態。過剰グルーミング（皮膚疾患・"
        "ストレス・繊維不足）、消化管運動低下、脱水が誘因。草食動物では消化管うっ滞の一徴候として現れる。"
    )
    cen = (
        f"Trichobezoar (hairball) in {e} is retention and matting of swallowed hair into a gastric mass; "
        "over-grooming (skin disease, stress, low fibre), reduced GI motility and dehydration predispose, "
        "and in herbivores it is a sign of GI stasis rather than a primary blockage."
    )
    pja = (
        "毛球が胃内容の通過を妨げ、食欲不振・削痩・嘔吐（可能な種）を招く。運動低下と脱水により毛球が固化し、"
        "重度では胃/幽門閉塞に至る。うっ滞への対処が治療の中心。"
    )
    pen = (
        "The hair mass impedes gastric outflow with inappetence, wasting and vomiting (in species that "
        "vomit); reduced motility and dehydration harden the bezoar, occasionally obstructing the stomach/"
        "pylorus — treating the underlying stasis is central."
    )
    return cja, cen, pja, pen


# --- Visceral torsion ------------------------------------------------------ #
def _visceral_torsion(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    name = f"{nj or ''} {ne or ''}".lower()
    if "uter" in name or "子宮" in name:
        cja = (
            f"{j}の子宮捻転は妊娠子宮（または蓄膿・腫大子宮）が長軸を軸に捻転し、子宮血流を遮断する急性腹症。"
            "妊娠末期の子宮重量・胎動、運動、子宮筋の張力異常が誘因。"
        )
        cen = (
            f"Uterine torsion in {e} is rotation of the gravid (or pyometra/enlarged) uterus about its long "
            "axis, occluding uterine blood flow — an acute abdomen precipitated by late-gestation uterine "
            "weight, fetal movement, activity and abnormal myometrial tone."
        )
        pja = "捻転により子宮のうっ血・虚血・壊死が進み、胎子死・ショック・敗血症に至る。緊急の外科的整復/卵巣子宮摘出を要する。"
        pen = (
            "Torsion causes uterine congestion, ischaemia and necrosis with fetal death, shock and sepsis; "
            "emergency surgical correction/ovariohysterectomy is required."
        )
        return cja, cen, pja, pen
    cja = (
        f"{j}の{nj or '臓器捻転'}は臓器がその血管茎を軸に捻転して血流を遮断する稀だが致死的な急性腹症。"
        "多くは特発性で、臓器の可動性・支持靭帯の弛緩、隣接臓器の膨満による腹腔内圧変動が素因。"
    )
    cen = (
        f"{_en_name(ne, 'Visceral torsion')} in {e} is rotation of an organ about its vascular pedicle occluding "
        "blood supply — a rare but lethal acute abdomen, usually idiopathic, predisposed by organ mobility, "
        "lax supporting ligaments and pressure shifts from adjacent distension."
    )
    pja = "捻転→静脈還流障害→うっ血性壊死→腹腔内出血・ショックの流れで急速に悪化する。早期の外科的整復/切除が唯一の救命手段。"
    pen = (
        "Torsion obstructs venous return, causing congestive necrosis, intra-abdominal haemorrhage and "
        "shock with rapid deterioration; early surgical correction/resection is the only life-saving option."
    )
    return cja, cen, pja, pen


# --- Gland / pore impaction ------------------------------------------------ #
def _gland_impaction(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    name = f"{nj or ''} {ne or ''}".lower()
    if any(k in name for k in ("femoral", "大腿孔", "大腿腺")):
        cja = (
            f"{j}の大腿孔閉塞は雄トカゲの大腿孔から分泌される蝋様物質が過剰に貯留・硬化して栓子を形成する病態。"
            "低湿度・不適切な基質・繁殖期の分泌亢進が誘因で、二次的に細菌感染（大腿孔炎）を合併しうる。"
        )
        cen = (
            f"Femoral pore impaction in {e} is accumulation and hardening of the waxy secretion from the "
            "femoral pores of male lizards into a plug; low humidity, inappropriate substrate and breeding-"
            "season secretion predispose, with secondary bacterial pore infection possible."
        )
        pja = "硬化した栓子が孔を拡張・圧迫して局所炎症・膿瘍・跛行を起こす。用手除去と環境（湿度）改善が治療。"
        pen = (
            "The hardened plug distends and compresses the pore, causing local inflammation, abscessation "
            "and lameness; manual removal and correcting humidity/husbandry are curative."
        )
        return cja, cen, pja, pen
    gland_ja = "臭腺" if ("scent" in name or "臭腺" in name) else "肛門腺"
    gland_en = "scent gland" if ("scent" in name or "臭腺" in name) else "anal gland"
    cja = (
        f"{j}の{gland_ja}貯留は分泌物が排出されず腺内に貯留・濃縮する機械的疾患。分泌物の粘稠化、開口部の"
        "狭窄・炎症、肥満・軟便による自然排出不全が誘因で、二次感染で膿瘍化しうる。"
    )
    cen = (
        f"{gland_en.capitalize()} impaction in {e} is failure to express secretion, which retains and "
        "inspissates within the gland; thickened secretion, a narrowed/inflamed duct opening, obesity and "
        "soft stool impair natural emptying, and secondary infection may abscessate."
    )
    pja = (
        "貯留物が腺を拡張して不快感・患部の舐性/擦過を起こし、閉塞が続くと炎症・膿瘍・破裂に至る。用手排出が基本治療。"
    )
    pen = (
        "Retained material distends the gland causing discomfort and licking/scooting; persistent blockage "
        "leads to inflammation, abscessation and rupture — manual expression is the mainstay."
    )
    return cja, cen, pja, pen


# --- Beak overgrowth / malocclusion (birds) -------------------------------- #
def _beak_overgrowth(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    cja = (
        f"{j}の嘴不正咬合（シザービーク・側方偏位）は上下嘴の噛み合わせ異常により嘴が正常に摩耗せず過長・変形する"
        "病態。雛期の給餌不良・外傷、栄養障害（Ca/VitD/VitA）、疥癬（Knemidokoptes）、肝疾患が誘因。"
    )
    cen = (
        f"Beak malocclusion (scissor beak/lateral deviation) in {e} is misalignment of the upper and lower "
        "beak so it fails to wear normally and overgrows/deforms; hand-rearing errors or trauma in the "
        "nestling, nutritional disease (Ca/vitamin D/A), Knemidokoptes mange and liver disease predispose."
    )
    pja = "咬合異常で自然摩耗が失われ嘴が過長・偏位し、採食障害・削痩を招く。放置すると変形が固定化するため早期矯正が必要。"
    pen = (
        "Malalignment abolishes normal attrition so the beak overgrows and deviates, impairing prehension "
        "and causing wasting; deformity becomes fixed if untreated, so early correction is needed."
    )
    return cja, cen, pja, pen


# --- Hoof overgrowth ------------------------------------------------------- #
def _hoof_overgrowth(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    cja = (
        f"{j}の蹄過長・亀裂は蹄の伸長が摩耗を上回って過長・変形し、亀裂を生じる病態。運動不足・軟らかい床・"
        "削蹄不足、栄養（ビオチン/亜鉛/銅）不足、慢性の蹄葉炎素因が誘因。"
    )
    cen = (
        f"Hoof overgrowth/cracks in {e} occur when horn growth outpaces wear, producing overgrown, deformed "
        "and fissured hooves; inactivity, soft flooring, infrequent trimming, nutritional deficiency "
        "(biotin/zinc/copper) and chronic laminitic predisposition contribute."
    )
    pja = (
        "過長蹄は肢軸・体重負重の異常を招き、亀裂から感染・跛行・蹄葉炎を生じる。定期的な削蹄と床・栄養管理が予防の要。"
    )
    pen = (
        "Overgrown hooves distort limb axis and weight-bearing, and cracks admit infection with lameness "
        "and laminitis; regular trimming, flooring and nutrition are the mainstays of prevention."
    )
    return cja, cen, pja, pen


# --- Dystocia / egg binding / follicular stasis ---------------------------- #
def _egg_binding(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    name = f"{nj or ''} {ne or ''}".lower()
    follicular = any(
        k in name for k in ("follicular", "卵胞", "reproductive stasis", "生殖停滞", "egg retention", "卵停滞")
    )
    if follicular:
        cja = (
            f"{j}の卵胞/生殖停滞は卵胞が発育・排卵・吸収されずに卵巣に停滞、または排卵後の卵が卵管/総排泄腔に"
            "停滞する病態。不適切な温度・光周期・営巣環境、栄養（Ca/VitA/VitD）不足、肥満、産卵刺激の欠如が誘因。"
        )
        cen = (
            f"Follicular/reproductive stasis in {e} is arrest of follicles that neither ovulate nor "
            "resorb, or retention of post-ovulatory eggs in the oviduct/cloaca; inappropriate temperature/"
            "photoperiod/nesting, nutritional deficiency (Ca/vitamin A/D), obesity and lack of laying "
            "stimulus predispose."
        )
        pja = (
            "停滞卵胞・卵が腹腔を占拠して圧迫・卵黄性体腔炎・二次感染を招き、慢性化すると衰弱・食欲不振・呼吸困難"
            "に至る。内科的管理不応例では卵巣卵管摘出を要する。"
        )
        pen = (
            "Retained follicles/eggs occupy the coelom with compression, yolk coelomitis and secondary "
            "infection; chronic cases waste, become anorexic and dyspnoeic, and refractory cases need "
            "salpingohysterectomy."
        )
        return cja, cen, pja, pen
    cja = (
        f"{j}の卵塞（難産）は形成された卵が正常時間内に産出されない病態。低カルシウム血症による子宮/卵管収縮"
        "不全、過大卵・奇形卵、肥満・運動不足、不適切な営巣環境、栄養（Ca/VitD/VitA）不足、卵管疾患が誘因。"
    )
    cen = (
        f"Egg binding (dystocia) in {e} is failure to pass a formed egg within the normal interval, from "
        "hypocalcaemia impairing uterine/oviductal contraction, oversized/malformed eggs, obesity/"
        "inactivity, inadequate nesting, nutritional deficiency (Ca/vitamin D/A) and oviductal disease."
    )
    pja = (
        "停滞卵が総排泄腔・尿路・血管を圧迫し、努責・排泄障害・虚脱を招く。長期停滞は卵管壊死・卵管破裂・卵黄性"
        "体腔炎に至る緊急疾患で、内科（カルシウム・オキシトシン・保温補液）不応例では外科的摘出を要する。"
    )
    pen = (
        "The retained egg compresses the cloaca, urinary tract and vessels, causing straining, obstruction "
        "and collapse; prolonged retention leads to oviductal necrosis, rupture and yolk coelomitis — an "
        "emergency, with surgery when medical management (calcium, oxytocin, warmth, fluids) fails."
    )
    return cja, cen, pja, pen


# --- Arytenoid chondritis (horse) ------------------------------------------ #
def _arytenoid_chondritis(sp, nj, ne):
    j, e = _ja(sp), _en(sp)
    cja = (
        f"{j}の披裂軟骨炎は喉頭の披裂軟骨の慢性炎症・化膿・肉芽形成により軟骨が肥厚・変形し、気道を狭窄させる"
        "病態。粘膜潰瘍からの細菌侵入、挿管・異物・手術による外傷、慢性上気道感染が契機となる。"
    )
    cen = (
        f"Arytenoid chondritis in {e} is chronic inflammation, suppuration and granulation of the laryngeal "
        "arytenoid cartilage that thickens and deforms it, narrowing the airway; mucosal ulceration with "
        "bacterial invasion, intubation/foreign-body/surgical trauma and chronic upper-airway infection initiate it."
    )
    pja = (
        "炎症により軟骨が壊死・肥厚し、披裂軟骨の可動性が失われて吸気性喘鳴・運動不耐・重度では上気道閉塞を"
        "きたす。慢性・進行性で、内科不応例では披裂軟骨切除を要する。"
    )
    pen = (
        "Inflammation leads to cartilage necrosis and thickening with loss of arytenoid mobility, producing "
        "inspiratory stridor, exercise intolerance and, when severe, upper-airway obstruction; it is chronic "
        "and progressive, needing arytenoidectomy in refractory cases."
    )
    return cja, cen, pja, pen


# name-keyword → generator (checked in order; specific before general).
# Keys carry the MECHANISM qualifier (…閉塞 / …stasis / …prolapse) — never a bare
# anatomical word — so neoplasia / abscess / infection / necrosis variants of the
# same organ (Anal Gland Carcinoma, Cheek Pouch Abscess, Beak Rot, Crop
# Candidiasis, Penile Necrosis) do NOT resolve here.
_AGENTS = (
    (("披裂軟骨炎", "arytenoid chondritis"), _arytenoid_chondritis),
    (("頬袋閉塞", "頬袋停滞", "cheek pouch impaction"), _cheek_pouch),
    (("盲腸停滞", "盲腸うっ滞", "盲腸嵌頓", "盲腸閉塞", "cecal impaction", "caecal impaction"), _cecal_impaction),
    (
        (
            "そ嚢停滞",
            "そ嚢うっ滞",
            "そ嚢閉塞",
            "嗉嚢停滞",
            "嗉嚢うっ滞",
            "嗉嚢閉塞",
            "crop stasis",
            "crop impaction",
            "crop slowdown",
            "sour crop",
            "slow crop",
            "proventricular impaction",
            "前胃うっ滞",
            "腺胃うっ滞",
        ),
        _crop_disorder,
    ),
    (("砂嚢異物", "gizzard foreign body", "ventricular foreign body", "筋胃異物"), _foreign_body),
    (
        (
            "卵胞停滞",
            "follicular stasis",
            "卵停滞",
            "reproductive stasis",
            "生殖停滞",
            "egg retention",
            "egg binding",
            "dystocia",
            "卵塞",
            "卵詰",
        ),
        _egg_binding,
    ),
    (
        (
            "陰茎脱",
            "半陰茎脱",
            "penile prolapse",
            "hemipenal prolapse",
            "hemipenile prolapse",
            "penile/hemipenal prolapse",
            "phallus prolapse",
        ),
        _penile_prolapse,
    ),
    (
        (
            "子宮脱",
            "膣脱",
            "uterine prolapse",
            "vaginal prolapse",
            "卵管脱",
            "oviduct prolapse",
            "reproductive tract prolapse",
            "生殖器脱",
        ),
        _repro_prolapse,
    ),
    (
        (
            "子宮捻転",
            "uterine torsion",
            "肝葉捻転",
            "hepatic lobe torsion",
            "splenic torsion",
            "mesenteric torsion",
            "臓器捻転",
        ),
        _visceral_torsion,
    ),
    (("直腸脱", "総排泄腔脱", "rectal prolapse", "cloacal prolapse", "腸脱", "intestinal prolapse"), _gi_prolapse),
    (("臓器脱", "organ prolapse", "prolapse (gastric"), _organ_prolapse_generic),
    (
        (
            "肛門腺貯留",
            "肛門腺閉塞",
            "anal gland impaction",
            "臭腺詰まり",
            "臭腺閉塞",
            "scent gland impaction",
            "大腿孔閉塞",
            "大腿腺閉塞",
            "femoral pore impaction",
        ),
        _gland_impaction,
    ),
    (("毛球", "trichobezoar", "hairball", "trichobezoard"), _trichobezoar),
    (
        (
            "消化管うっ滞",
            "gi stasis",
            "gastrointestinal stasis",
            "gut stasis",
            "ileus",
            "腸閉塞",
            "intestinal obstruction",
        ),
        _gi_stasis,
    ),
    (("異物", "foreign body", "鼻腔異物", "foreign body in foot"), _foreign_body),
    (("嘴不正咬合", "嘴の不正咬合", "beak malocclusion", "scissor beak", "シザービーク"), _beak_overgrowth),
    (("蹄過長", "hoof overgrowth", "蹄亀裂", "hoof crack"), _hoof_overgrowth),
    (
        (
            "結石",
            "尿石",
            "腎結石",
            "尿路結石",
            "総排泄腔結石",
            "膀胱結石",
            "urolith",
            "bladder stone",
            "kidney stone",
            "urinary stone",
            "cystic calcul",
            "cloacal calcul",
            "nephrolith",
            "urethral obstruction",
            "尿道閉塞",
        ),
        _urolithiasis,
    ),
)

# Names that look structural but are genuinely neoplastic / infectious / necrotic /
# dysbiotic — never treat with the mechanical mechanism.
_EXCLUSIONS = (
    "sibo",
    "small intestinal bacterial overgrowth",
    "ciliate",
    "protozoal overgrowth",
    "繊毛虫",
    "dysbios",
    "菌叢",
    "abscess",
    "膿瘍",
    "carcinoma",
    "adenocarcinoma",
    "sarcoma",
    "腫瘍",
    "腺癌",
    "腺腫",
    "adenoma",
    "lymphoma",
    "リンパ腫",
    "neoplas",
    "tumor",
    "tumour",
    "necrosis",
    "壊死",
    "mycosis",
    "candidias",
    "真菌",
    "rot ",
    "burn",
    "熱傷",
    "火傷",
    "fistula",
    "瘻",
    "cholelith",
    "gallstone",
    "胆石",
    "胆管結石",
    "唾石",
    "歯石",
    "salivary",
    "vomit stone",
)


def resolve_structural_agent(name_ja: str, name_en: str):
    """Return the generator for a structural/mechanical disease, or None."""
    name = f"{name_ja or ''} {name_en or ''}".lower()
    if any(x in name for x in _EXCLUSIONS):
        return None
    for keys, gen in _AGENTS:
        if any(k.lower() in name for k in keys):
            return gen
    return None


def structural_clinical_fields(species: str, name_ja: str, name_en: str) -> dict | None:
    """Curated causes / pathophysiology (JA+EN) for a structural/mechanical
    disease, or None when the name does not resolve to a known mechanism."""
    gen = resolve_structural_agent(name_ja, name_en)
    if gen is None:
        return None
    sp = (species or "").lower()
    disp_ja = _strip_species_suffix(name_ja, sp)
    disp_en = _strip_species_suffix(name_en, sp)
    cja, cen, pja, pen = gen(sp, disp_ja, disp_en)
    return {
        "causes_ja": cja,
        "causes": cen,
        "pathophysiology_ja": pja,
        "pathophysiology": pen,
    }
