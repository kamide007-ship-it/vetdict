"""fish_diseases.py – 観賞魚の代表的な疾患

淡水魚・海水魚（錦鯉、金魚、熱帯魚等）に発生する代表的な疾患を網羅的に
取り上げ、簡易的な鑑別診断を提供するモジュールです。情報は教育目的であり、
専門的な診断や治療は獣医師が行うべきです。
"""

from __future__ import annotations

from typing import Any, Dict, List

from . import prevalence_data
from .helpers import ADVICE, analyze_symptoms_generic, enrich_diseases

SYMPTOM_NAMES: Dict[str, Dict[str, str]] = {
    # 体表・外観
    "white_spots": {"ja": "白点（白い斑点）", "en": "White spots"},
    "cotton_like_growth": {"ja": "綿状の付着物", "en": "Cotton-like growth"},
    "fin_rot": {"ja": "鰭の溶解・崩壊", "en": "Fin rot / erosion"},
    "scale_loss": {"ja": "鱗の脱落", "en": "Scale loss"},
    "raised_scales": {"ja": "鱗の逆立ち（松かさ）", "en": "Raised scales (pinecone)"},
    "ulcers": {"ja": "潰瘍・ただれ", "en": "Ulcers / sores"},
    "redness_skin": {"ja": "体表の充血・発赤", "en": "Skin redness / hemorrhage"},
    "mucus_overproduction": {"ja": "粘液の過剰分泌", "en": "Excess mucus production"},
    "discoloration": {"ja": "体色の変化・退色", "en": "Color change / fading"},
    "dark_coloration": {"ja": "体色の黒化", "en": "Darkening of body color"},
    "white_film": {"ja": "白い膜状の付着", "en": "White film on body"},
    "gold_dust": {"ja": "金粉状の付着（コショウ病）", "en": "Gold dust appearance"},
    "lumps_nodules": {"ja": "しこり・結節", "en": "Lumps / nodules"},
    "worm_like_parasites": {"ja": "糸状の寄生虫が見える", "en": "Visible worm-like parasites"},
    "anchor_worm": {"ja": "イカリムシの付着", "en": "Anchor worm attached"},
    "spots_black": {"ja": "黒い斑点", "en": "Black spots"},
    # 鰭・尾
    "clamped_fins": {"ja": "鰭をたたんでいる", "en": "Clamped fins"},
    "frayed_fins": {"ja": "鰭がボロボロ", "en": "Frayed / ragged fins"},
    "fin_hemorrhage": {"ja": "鰭の充血", "en": "Fin hemorrhage"},
    # 眼
    "pop_eye": {"ja": "眼球突出（ポップアイ）", "en": "Pop-eye (exophthalmia)"},
    "cloudy_eye": {"ja": "目の白濁", "en": "Cloudy eye"},
    "sunken_eye": {"ja": "眼球陥没", "en": "Sunken eye"},
    # 鰓
    "gill_redness": {"ja": "鰓の充血", "en": "Gill redness"},
    "gill_paleness": {"ja": "鰓の退色・蒼白", "en": "Pale gills"},
    "gill_swelling": {"ja": "鰓の腫脹", "en": "Gill swelling"},
    "gill_mucus": {"ja": "鰓の粘液過多", "en": "Excess gill mucus"},
    "rapid_gill_movement": {"ja": "鰓蓋の速い動き", "en": "Rapid opercular movement"},
    # 行動
    "flashing": {"ja": "体を擦りつける（フラッシング）", "en": "Flashing / scratching"},
    "lethargy": {"ja": "活動低下・沈下", "en": "Lethargy / bottom sitting"},
    "loss_of_appetite": {"ja": "食欲不振", "en": "Loss of appetite"},
    "gasping_surface": {"ja": "水面でパクパク（鼻上げ）", "en": "Gasping at surface"},
    "erratic_swimming": {"ja": "異常遊泳（暴れる）", "en": "Erratic / darting swimming"},
    "loss_of_balance": {"ja": "平衡感覚の喪失", "en": "Loss of balance / listing"},
    "swimming_upside_down": {"ja": "転覆（逆さまに泳ぐ）", "en": "Swimming upside down"},
    "hiding": {"ja": "隠れて出てこない", "en": "Hiding behavior"},
    "isolation": {"ja": "群れから離れる", "en": "Isolation from group"},
    "head_shaking": {"ja": "頭を振る", "en": "Head shaking"},
    "spinning": {"ja": "旋回遊泳", "en": "Spinning / whirling"},
    # 腹部・体型
    "bloating": {"ja": "腹部膨満", "en": "Abdominal bloating / swelling"},
    "emaciation": {"ja": "痩せ（やつれ）", "en": "Emaciation / wasting"},
    "dropsy": {"ja": "腹水・浮腫", "en": "Dropsy / edema"},
    "bent_spine": {"ja": "脊椎の湾曲", "en": "Bent / curved spine"},
    # 排泄
    "white_stringy_feces": {"ja": "白い糸状の糞", "en": "White stringy feces"},
    "trailing_feces": {"ja": "糞がぶら下がる", "en": "Trailing feces"},
    # 呼吸
    "labored_breathing": {"ja": "呼吸困難", "en": "Labored breathing"},
    # 繁殖
    "egg_binding": {"ja": "過抱卵", "en": "Egg binding"},
    # 急変
    "sudden_death": {"ja": "突然死", "en": "Sudden death"},
    "mass_mortality": {"ja": "大量死", "en": "Mass mortality"},
}

DISEASES: List[Dict[str, Any]] = [
    {
        "name": "Ichthyophthirius (White Spot Disease / Ich)",
        "name_ja": "白点病（イクチオフチリウス症）",
        "symptoms": {"white_spots", "flashing", "clamped_fins", "lethargy", "loss_of_appetite", "rapid_gill_movement"},
        "description": "Caused by the ciliate protozoan Ichthyophthirius multifiliis. One of the most common and recognizable freshwater fish diseases.",
        "description_ja": "繊毛虫イクチオフチリウス・ムルチフィリスによる感染症。淡水魚で最も一般的で認知度の高い疾患の一つ。",
        "urgency": "high",
        "recommended_tests": ["skin_scrape_microscopy", "water_quality_test"],
        "causes": "繊毛虫 Ichthyophthirius multifiliis の寄生。水温の急変、ストレス、免疫低下が発症を誘発。",
        "causes_ja": "繊毛虫 Ichthyophthirius multifiliis の寄生。水温の急変、ストレス、免疫低下が発症を誘発。",
        "treatment": "水温を28-30°Cに上昇させ生活環を加速。0.3-0.5%塩水浴、メチレンブルー、マラカイトグリーン、ホルマリン浴。遊走子ステージでのみ薬剤が有効。",
        "treatment_ja": "水温を28-30°Cに上昇させ生活環を加速。0.3-0.5%塩水浴、メチレンブルー、マラカイトグリーン、ホルマリン浴。遊走子ステージでのみ薬剤が有効。",
        "prevention": "新規導入魚の検疫（2-4週間）、水温の急変回避、適切な水質管理、過密飼育の回避。",
        "prevention_ja": "新規導入魚の検疫（2-4週間）、水温の急変回避、適切な水質管理、過密飼育の回避。",
        "prognosis": "早期発見・治療で予後良好。重症例や鰓への大量寄生は致死的。",
        "prognosis_ja": "早期発見・治療で予後良好。重症例や鰓への大量寄生は致死的。",
        "onset_pattern": {"acute", "subacute"},
    },
    {
        "name": "Columnaris Disease",
        "name_ja": "カラムナリス病（尾ぐされ病・口ぐされ病）",
        "symptoms": {"fin_rot", "frayed_fins", "ulcers", "white_film", "cotton_like_growth", "gill_redness", "lethargy", "loss_of_appetite"},
        "description": "Bacterial infection caused by Flavobacterium columnare. Affects skin, fins, and gills.",
        "description_ja": "Flavobacterium columnare による細菌感染症。皮膚、鰭、鰓に病変を形成。",
        "urgency": "high",
        "recommended_tests": ["skin_scrape_microscopy", "bacterial_culture", "water_quality_test"],
        "treatment": "抗菌薬浴（オキソリン酸、カナマイシン）、塩水浴、水質改善。重症例では薬餌投与。",
        "treatment_ja": "抗菌薬浴（オキソリン酸、カナマイシン）、塩水浴、水質改善。重症例では薬餌投与。",
        "prevention": "水質管理の徹底、過密飼育回避、ストレス軽減、外傷防止。",
        "prevention_ja": "水質管理の徹底、過密飼育回避、ストレス軽減、外傷防止。",
        "onset_pattern": {"acute", "subacute"},
    },
    {
        "name": "Aeromonas / Motile Aeromonad Septicemia",
        "name_ja": "エロモナス感染症（運動性エロモナス敗血症）",
        "symptoms": {"ulcers", "redness_skin", "raised_scales", "dropsy", "pop_eye", "fin_hemorrhage", "lethargy", "loss_of_appetite", "bloating"},
        "description": "Opportunistic bacterial infection by Aeromonas hydrophila and related species, often secondary to stress or poor water quality.",
        "description_ja": "Aeromonas hydrophila 等による日和見細菌感染。ストレスや水質悪化が発症の背景にあることが多い。",
        "urgency": "high",
        "recommended_tests": ["bacterial_culture", "water_quality_test", "blood_smear"],
        "treatment": "抗菌薬浴（オキソリン酸、エンロフロキサシン）、薬餌、水質改善。松かさ病や腹水を伴う重症例は治療困難。",
        "treatment_ja": "抗菌薬浴（オキソリン酸、エンロフロキサシン）、薬餌、水質改善。松かさ病や腹水を伴う重症例は治療困難。",
        "prevention": "水質管理、適正な飼育密度、栄養管理、ストレス軽減。",
        "prevention_ja": "水質管理、適正な飼育密度、栄養管理、ストレス軽減。",
        "onset_pattern": {"acute", "subacute", "chronic"},
    },
    {
        "name": "Saprolegnia (Water Mold / Cotton Wool Disease)",
        "name_ja": "水カビ病（サプロレグニア症）",
        "symptoms": {"cotton_like_growth", "white_film", "lethargy", "loss_of_appetite", "ulcers"},
        "description": "Fungal infection caused by Saprolegnia and related oomycetes. Often secondary to skin damage or immunosuppression.",
        "description_ja": "サプロレグニア等の卵菌類による真菌感染。皮膚損傷や免疫低下に続発することが多い。",
        "urgency": "moderate",
        "recommended_tests": ["skin_scrape_microscopy", "water_quality_test"],
        "treatment": "メチレンブルー浴、マラカイトグリーン浴、塩水浴（0.3-0.5%）。原因の除去（外傷治療、水質改善）。",
        "treatment_ja": "メチレンブルー浴、マラカイトグリーン浴、塩水浴（0.3-0.5%）。原因の除去（外傷治療、水質改善）。",
        "prevention": "外傷防止、水質管理、適正水温維持、過密飼育回避。",
        "prevention_ja": "外傷防止、水質管理、適正水温維持、過密飼育回避。",
        "onset_pattern": {"acute", "subacute"},
    },
    {
        "name": "Velvet Disease (Oodinium / Piscinoodinium)",
        "name_ja": "コショウ病（ウーディニウム症）",
        "symptoms": {"gold_dust", "flashing", "clamped_fins", "rapid_gill_movement", "lethargy", "loss_of_appetite", "labored_breathing"},
        "description": "Parasitic infection caused by Piscinoodinium (freshwater) or Amyloodinium (marine). Often mistaken for Ich but spots are finer.",
        "description_ja": "淡水では Piscinoodinium、海水では Amyloodinium による寄生虫感染。白点病に似るが斑点はより微細。",
        "urgency": "high",
        "recommended_tests": ["skin_scrape_microscopy", "water_quality_test"],
        "treatment": "銅イオン製剤（海水）、メチレンブルー・アクリフラビン（淡水）、遮光（光合成阻害）、水温上昇。",
        "treatment_ja": "銅イオン製剤（海水）、メチレンブルー・アクリフラビン（淡水）、遮光（光合成阻害）、水温上昇。",
        "onset_pattern": {"acute", "subacute"},
    },
    {
        "name": "Swim Bladder Disorder",
        "name_ja": "浮袋障害（転覆病）",
        "symptoms": {"loss_of_balance", "swimming_upside_down", "bloating", "loss_of_appetite", "lethargy"},
        "description": "Buoyancy disorder affecting the swim bladder. Common in fancy goldfish and bettas. May be caused by diet, infection, or congenital defects.",
        "description_ja": "浮袋の機能障害による浮力異常。琉金等の改良品種の金魚やベタに多い。食餌、感染、先天的異常が原因。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam", "xray", "water_quality_test"],
        "treatment": "3日間の絶食後、茹でた剥き餌（グリーンピース等）を給餌。水温を適正範囲に。細菌感染が疑われる場合は抗菌薬。",
        "treatment_ja": "3日間の絶食後、茹でた剥き餌（グリーンピース等）を給餌。水温を適正範囲に。細菌感染が疑われる場合は抗菌薬。",
        "onset_pattern": {"acute", "chronic"},
    },
    {
        "name": "Dropsy (Pinecone Disease)",
        "name_ja": "松かさ病（立鱗病・腹水症）",
        "symptoms": {"raised_scales", "bloating", "dropsy", "pop_eye", "lethargy", "loss_of_appetite", "redness_skin"},
        "description": "Symptom complex characterized by fluid accumulation and scale protrusion. Usually indicates severe organ failure (kidney/liver) or systemic infection.",
        "description_ja": "体液貯留と鱗の逆立ちを特徴とする症候群。通常、重度の臓器不全（腎/肝）または全身感染を示す。",
        "urgency": "high",
        "recommended_tests": ["bacterial_culture", "water_quality_test", "blood_chemistry"],
        "treatment": "エプソムソルト浴（硫酸マグネシウム）、抗菌薬浴・薬餌、水質改善。予後は一般に不良。",
        "treatment_ja": "エプソムソルト浴（硫酸マグネシウム）、抗菌薬浴・薬餌、水質改善。予後は一般に不良。",
        "prognosis": "一般に予後不良。早期の軽症例では回復の可能性があるが、重度の立鱗・腹水は治療困難。",
        "prognosis_ja": "一般に予後不良。早期の軽症例では回復の可能性があるが、重度の立鱗・腹水は治療困難。",
        "onset_pattern": {"subacute", "chronic"},
    },
    {
        "name": "Anchor Worm (Lernaea)",
        "name_ja": "イカリムシ症（レルネア症）",
        "symptoms": {"anchor_worm", "flashing", "redness_skin", "ulcers", "lethargy", "loss_of_appetite"},
        "description": "Parasitic copepod Lernaea that embeds in fish skin. Visible as thread-like protrusions from the body.",
        "description_ja": "寄生性カイアシ類レルネアが皮膚に突き刺さる。糸状の突起物として肉眼で確認可能。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam", "skin_scrape_microscopy"],
        "treatment": "ピンセットで成虫を除去後、傷口を消毒。トリクロルホン（ジプテレックス）浴、レバミゾール浴。幼虫対策も必要。",
        "treatment_ja": "ピンセットで成虫を除去後、傷口を消毒。トリクロルホン（ジプテレックス）浴、レバミゾール浴。幼虫対策も必要。",
        "onset_pattern": {"subacute", "chronic"},
    },
    {
        "name": "Fish Lice (Argulus)",
        "name_ja": "ウオジラミ症（アルグルス症）",
        "symptoms": {"flashing", "redness_skin", "ulcers", "worm_like_parasites", "lethargy", "erratic_swimming"},
        "description": "Parasitic crustacean Argulus that attaches to skin and feeds on blood. Visible as flat, disc-shaped parasites.",
        "description_ja": "寄生性甲殻類アルグルスが皮膚に付着し吸血。平らな円盤状の寄生虫として肉眼で確認可能。",
        "urgency": "moderate",
        "recommended_tests": ["physical_exam"],
        "treatment": "トリクロルホン浴、ピンセットによる除去、塩水浴。池では水の完全入れ替えも有効。",
        "treatment_ja": "トリクロルホン浴、ピンセットによる除去、塩水浴。池では水の完全入れ替えも有効。",
        "onset_pattern": {"subacute", "chronic"},
    },
    {
        "name": "Gill Flukes (Dactylogyrus)",
        "name_ja": "鰓吸虫症（ダクチロギルス症）",
        "symptoms": {"rapid_gill_movement", "gasping_surface", "gill_redness", "gill_mucus", "flashing", "lethargy", "loss_of_appetite"},
        "description": "Monogenean trematode parasites infecting the gills. Causes respiratory distress and secondary bacterial infections.",
        "description_ja": "鰓に寄生する単生吸虫。呼吸困難と二次的な細菌感染を引き起こす。",
        "urgency": "high",
        "recommended_tests": ["gill_biopsy_microscopy", "skin_scrape_microscopy"],
        "treatment": "プラジカンテル浴、ホルマリン浴、トリクロルホン浴。重症例では抗菌薬の併用。",
        "treatment_ja": "プラジカンテル浴、ホルマリン浴、トリクロルホン浴。重症例では抗菌薬の併用。",
        "onset_pattern": {"acute", "subacute"},
    },
]


def analyze_symptoms(
    symptoms: List[str],
    age_stage: str = "",
    breed: str = None,
    *,
    onset: str = None,
    age_years: float = None,
    species: str = None,
    lab_values: dict = None,
    gender: str = None,
    vaccines: list = None,
    vaccination_status: str = None,
) -> Dict[str, Any]:
    return analyze_symptoms_generic(
        symptoms,
        DISEASES,
        SYMPTOM_NAMES,
        ADVICE,
        onset=onset,
        age_years=age_years,
        breed=breed,
        species=species or "fish",
        lab_values=lab_values,
        gender=gender,
        vaccines=vaccines,
        vaccination_status=vaccination_status,
        prevalence_map=prevalence_data.SPECIES_PREVALENCE.get("fish", {}),
    )


DISEASES = enrich_diseases(DISEASES, "fish")
