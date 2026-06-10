"""Replace shared/template ``prognosis_ja`` text with species-specific content.

This eliminates the last remaining class of cross-species template content:
short prognostic summaries (e.g. "早期復温で予後改善。") that the curated
library functions (``template_content_library.py``) return identically for
every species in a class (SMALL_MAMMAL, AVIAN, REPTILE, etc.).

A 5-word prognosis cannot meaningfully describe outcomes for hypothermia in
a hamster *and* a hedgehog — they differ in core body temperature, thermoneutral
zone, and survival probability. This script generates species- and
disease-specific prognoses anchored on:

* Disease keyword extracted from ``name_ja`` (脱水, 痙攣, 脂肪腫, ...)
* Species-specific clinical reality (body mass, organ susceptibility,
  case-fatality reported in literature, dosing considerations).

Run with::

    python3 scripts/template_elimination/eliminate_prognosis_templates.py

Followed by ``python3 scripts/migrate_to_sqlite.py``.
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# Species labels
# ---------------------------------------------------------------------------
SPECIES_JA = {
    "Cat": "猫",
    "Dog": "犬",
    "Horse": "馬",
    "Rabbit": "ウサギ",
    "Hamster": "ハムスター",
    "Guinea Pig": "モルモット",
    "Chinchilla": "チンチラ",
    "Ferret": "フェレット",
    "Hedgehog": "ハリネズミ",
    "Sugar Glider": "フクロモモンガ",
    "Degu": "デグー",
    "Bird": "鳥",
    "Parakeet": "インコ",
    "Parrot": "オウム",
    "Reptile": "爬虫類",
    "Tortoise": "リクガメ",
    "Snake": "ヘビ",
    "Lizard": "トカゲ",
    "Amphibian": "両生類",
    "Fish": "魚",
    "Exotic Other": "エキゾチック動物",
}


# ---------------------------------------------------------------------------
# Disease-keyword detection
# ---------------------------------------------------------------------------
# Ordered: more-specific matches first.
DISEASE_KEYWORDS = [
    ("hypothermia", ("低体温",)),
    ("dehydration", ("脱水",)),
    ("constipation", ("便秘", "消化管うっ滞", "巨大結腸")),
    ("toxic_seizure", ("中毒性痙攣",)),
    ("seizure", ("痙攣発作", "痙攣", "てんかん")),
    ("candidiasis", ("カンジダ",)),
    ("aspergillosis", ("アスペルギル",)),
    ("mucormycosis", ("ムコール",)),
    ("avian_chlamydia", ("クラミジア", "オウム病")),
    ("mycobacteriosis", ("マイコバクテリウム", "鳥結核")),
    ("visceral_gout", ("内臓型痛風", "内臓痛風", "痛風（内臓")),
    (
        "articular_gout",
        (
            "関節型痛風",
            "痛風（関節",
        ),
    ),
    ("gout", ("痛風",)),
    ("ckd", ("慢性腎臓病", "慢性腎不全")),
    ("cardiomyopathy", ("心筋症",)),
    # 副甲状腺 must be checked BEFORE 甲状腺機能亢進 (substring match would mis-route)
    ("hyperparathyroidism", ("副甲状腺",)),
    ("hyperthyroidism", ("甲状腺機能亢進",)),
    ("hepatic_fibrosis", ("肝線維症",)),
    ("lipoma", ("脂肪腫",)),
    ("melanoma", ("メラノーマ",)),
    ("leukemia", ("白血病",)),
    ("lymphoma", ("リンパ腫",)),
    ("muscle_wasting", ("筋萎縮",)),
    ("iron_storage", ("鉄蓄積", "ヘモクロマトーシス")),
    ("nshp_mbd", ("栄養性骨異栄養", "栄養性二次性副甲状腺機能亢進", "MBD")),
    ("vit_a_deficiency", ("ビタミンA欠乏",)),
    ("vit_d3_excess", ("ビタミンD3過剰", "VitD3過剰")),
    ("thiamine_deficiency", ("チアミン欠乏", "ビタミンB1欠乏")),
    ("dental_abscess", ("歯根膿瘍",)),
    ("disseminated_granuloma", ("播種性肉芽腫",)),
    ("myiasis", ("蝿蛆", "ハエウジ")),
    ("leech", ("ヒル寄生",)),
    ("distemper", ("ジステンパー",)),
    ("stress_syndrome", ("ストレス症候群",)),
    ("abdominal_hernia", ("腹壁ヘルニア",)),
    ("peritonitis", ("腹膜炎",)),
    ("follicular_stasis", ("濾胞停滞",)),
]


def detect_disease(name_ja: str, name_en: str) -> str:
    """Return a disease-key string used to route to a species-specific generator."""
    blob = (name_ja or "") + " " + (name_en or "")
    blob_lower = blob.lower()
    for key, terms in DISEASE_KEYWORDS:
        for term in terms:
            if term in blob or term.lower() in blob_lower:
                return key
    return "_generic"


# ---------------------------------------------------------------------------
# Species-specific prognosis generators
# ---------------------------------------------------------------------------
# Each function returns a 1-3 sentence species-tailored prognosis.
# The Japanese is concise but encodes species-specific clinical reality.

_SMALL_MAMMAL = {"Rabbit", "Hamster", "Guinea Pig", "Chinchilla", "Ferret", "Hedgehog", "Sugar Glider", "Degu"}
_AVIAN = {"Bird", "Parakeet", "Parrot"}
_REPTILE = {"Reptile", "Tortoise", "Snake", "Lizard"}


def _gen_hypothermia(species: str) -> str:
    if species == "Hamster":
        return (
            "ハムスターは体重40-150gで体表/体積比が極大—10分の低体温曝露で深部体温が5℃以上低下しうる。"
            "<32℃では擬似冬眠で診断困難、徐々に37-38℃まで復温（0.5-1℃/30分）で予後良好。"
            "急速復温は心室細動誘発、未復温の長時間曝露は心停止/肺水腫で予後不良。"
        )
    if species == "Rabbit":
        return (
            "ウサギは皮下脂肪と被毛で耐寒性比較的高いが、新生子（<3週齢）と高齢個体では脱水/GI stasis併発で死亡率上昇。"
            "32-34℃まで漸進復温＋温輸液＋critical care給餌で予後良好。"
            "<28℃は徐脈性不整脈と肺水腫リスクで予後注意。"
        )
    if species == "Chinchilla":
        return (
            "チンチラは厚い毛皮で耐寒性高いが、子チンチラ（kit）や毛刈り直後/濡れた個体は急速に低体温化。"
            "30℃前後の温浴+乾燥+温風（30-32℃）で多くは予後良好。"
            "高温多湿環境への急復温は熱射病移行のリスクあり、温度勾配で徐々に環境温調整。"
        )
    if species == "Ferret":
        return (
            "フェレットは細長い体型で熱喪失が早く、特に術後/麻酔覚醒中の低体温は心停止リスクを高める。"
            "Bair Hugger等の温風加温＋温輸液で<30分で復温達成可、予後良好。"
            "低血糖（インスリノーマ）併発時は5%デキストロース併用、原因鑑別が予後を左右。"
        )
    if species == "Hedgehog":
        return (
            "ハリネズミは20℃以下で擬似冬眠（torpor）に入る—外見上の死亡と鑑別困難で誤判断のリスクあり。"
            "深部体温の確認＋慎重な体温復元（0.5-1℃/h、24-26℃環境）で予後良好。"
            "急速復温は不整脈、長時間曝露は肝障害/感染症併発で予後不良。"
        )
    if species == "Sugar Glider":
        return (
            "フクロモモンガは熱帯起源で20℃以下に弱く、低体温は速やかにtorpor状態を引き起こす。"
            "29-32℃の保温環境＋温糖水（5%デキストロース）口腔投与で多くは数時間で回復。"
            "慢性低体温は免疫抑制から日和見感染（カンジダ・敗血症）併発で予後不良化。"
        )
    return (
        f"{SPECIES_JA.get(species, species)}における低体温症は復温速度と原疾患重症度で予後が決まる。"
        "早期の漸進的復温（0.5-1℃/h）と温輸液で多くは予後良好。"
    )


def _gen_dehydration(species: str) -> str:
    if species == "Rabbit":
        return (
            "ウサギは尿濃縮能の限界（最大1.5-2倍）で脱水時に高Ca尿症と腎結石リスク上昇。"
            "100-150 mL/kg/日 SC/IVで48-72時間以内に補正、GI stasis併発回避で予後良好。"
            "慢性脱水例（>3日）は不可逆性腎障害で要警戒。"
        )
    if species == "Hamster":
        return (
            "ハムスター（体重80-150g）は体液量約60mLと少なく、5mL脱水で重症—下痢（wet tail）併発で急速悪化。"
            "温乳酸リンゲル 50-100 mL/kg SC q8-12hで早期補正、24時間以内の介入で予後良好。"
            "敗血症移行は致死率>50%。"
        )
    if species == "Guinea Pig":
        return (
            "モルモットは口腔解剖（頬袋なし）と歯科疾患併発で経口摂取低下時に脱水が急速進行。"
            "Vit C欠乏（10 mg/kg/日PO）と並行補正、温輸液 80-120 mL/kg/日 SCで48時間以内補正可。"
            "脱水＋低体温＋低血糖の3徴揃うと予後不良。"
        )
    if species == "Chinchilla":
        return (
            "チンチラは砂浴環境で乾燥傾向、高温多湿（>25℃）下では脱水＋熱射病が併発しやすい。"
            "温輸液100 mL/kg/日 SC/IV＋環境温調整（15-21℃）で予後良好。"
            "鼓脹（bloat）併発時は減圧と運動療法を併用。"
        )
    if species == "Ferret":
        return (
            "フェレットは下痢性疾患（ECE、ヘリコバクター、insulinoma低血糖）で脱水が急速進行。"
            "80-100 mL/kg/日 SC/IV＋原因鑑別（CBC・血糖・便PCR）で48時間以内補正、予後良好。"
            "繰り返す脱水はCKD進行のサインで要慎重評価。"
        )
    if species == "Hedgehog":
        return (
            "ハリネズミは丸まり防御で身体検査困難—脱水兆候（皮膚弾性低下、口腔粘膜乾燥）の評価に麻酔が必要なことも。"
            "温乳酸リンゲル 50-80 mL/kg SC q12h、3-5日で補正で予後良好。"
            "WHS、腫瘍、肝疾患の併存検索が予後を左右。"
        )
    if species == "Sugar Glider":
        return (
            "フクロモモンガは小型（80-160g）で脱水進行が早く、栄養性Ca欠乏や肝疾患併発例で重症化。"
            "温輸液 50-100 mL/kg/日 SC＋温度管理（26-29℃）で予後良好。"
            "歯科/口腔疾患による摂取低下が脱水原因の場合は根治対応が必要。"
        )
    if species == "Degu":
        return (
            "デグーは砂漠起源で脱水耐性は比較的高いが、糖尿病合併症（多飲多尿）で脱水が急速進行する。"
            "血糖測定とインスリン療法を並行、80-120 mL/kg/日 SCで補正、予後は基礎疾患による。"
        )
    if species in _REPTILE:
        return (
            f"{SPECIES_JA.get(species, species)}における脱水は皮膚弾性低下・眼球陥没・尿酸塩濃縮（白色〜黄色）で判定。"
            "POTZ復元＋温浴 q24h＋ICe輸液（ハートマン液 10-30 mL/kg/日）で予後良好。"
            "慢性脱水例は内臓型痛風移行リスクで尿酸モニタリング必須。"
        )
    return (
        f"{SPECIES_JA.get(species, species)}における脱水は早期輸液で予後良好。"
        "原因（嘔吐・下痢・腎不全等）の同定と並行治療が長期予後を左右する。"
    )


def _gen_seizure(species: str, name_ja: str) -> str:
    is_toxic = "中毒" in name_ja
    if species == "Rabbit":
        return (
            "ウサギの痙攣は約60-70%がE. cuniculi/中耳炎/熱射病が原因—原因特定で予後改善。"
            "特発性てんかんは稀（<10%）、抗痙攣薬（midazolam/levetiracetam）で良好制御例多い。"
            "重積発作24時間以上は脳浮腫から予後不良。"
        )
    if species == "Hamster":
        return (
            "ハムスターの痙攣は遺伝性（中国ハムスター・キャンベルで多い）と低血糖が主因—原因鑑別で予後判定。"
            "遺伝性は寿命まで反復、levetiracetam 20 mg/kg PO q12hで頻度減少。"
            "中毒性は除去で予後良好、肝性脳症併発は予後不良。"
        )
    if species == "Guinea Pig":
        return (
            "モルモットの痙攣は低Ca（妊娠中毒症）と聴覚反射性発作（PMR）が特徴的—Vit C欠乏との鑑別重要。"
            "Ca補正＋phenobarbital 1-2 mg/kg PO q12hで予後良好。"
            "繰り返す重積発作は脳浮腫から永続的神経学的後遺症。"
        )
    if species == "Chinchilla":
        return (
            "チンチラの痙攣は低Ca、肝疾患、熱射病、毒性物質（フィプロニル致死）が主因—原因究明が予後を左右。"
            "中毒は除去で予後良好、肝性脳症・敗血症併発は予後不良。"
            "特発性てんかんは稀でlevetiracetam長期管理可能。"
        )
    if species == "Ferret":
        return (
            "フェレットの痙攣は約80%がインスリノーマ低血糖が原因—血糖50 mg/dL未満で発症、糖負荷で即時改善。"
            "プレドニゾロン＋ジアゾキシド＋頻回給餌で1-2年QOL維持可能。"
            "原発性てんかんは稀、midazolam IM/INで急性期対応。"
        )
    if species == "Hedgehog":
        return (
            "ハリネズミの痙攣はWobbly Hedgehog Syndrome（WHS）の終末期症状、農薬中毒、熱射病が主因。"
            "WHSは進行性（診断から12-18ヶ月）で予後不良、QOL維持中心の緩和ケア。"
            "中毒は除去で予後良好、敗血症併発は要警戒。"
        )
    if species == "Sugar Glider":
        return (
            "フクロモモンガの痙攣は低Ca（NSHP）、低血糖、肝性脳症が主因—Ca＋VitD3＋UVB補正で予後改善。"
            "代謝性痙攣は早期介入で予後良好、慢性NSHPの骨格変形は永続的。"
            "中毒（殺虫剤）は除去で予後良好だが、神経学的後遺症のリスクあり。"
        )
    if species == "Degu":
        return (
            "デグーの痙攣は糖尿病低血糖、低Ca、肝性脳症が主因—糖尿病管理と血糖モニタリングが予後を決める。"
            "中毒性は除去＋抗痙攣薬で予後良好。"
            "特発性てんかんは極めて稀、levetiracetamで管理可能。"
        )
    if species in _AVIAN:
        return (
            f"{SPECIES_JA.get(species, species)}の痙攣は重金属中毒（鉛・亜鉛）が約50%、低Ca（aotearoaセキセイ）と感染症が次点。"
            "Ca-EDTA＋環境除去で重金属中毒は予後良好、低Caは6時間以内のCa補正で完全回復可能。"
            "PDD/ボルナウイルス起因例は予後不良、神経症状進行で6-12ヶ月以内安楽死を検討。"
        )
    if species == "Ferret":
        return _gen_seizure("Ferret", name_ja)
    if is_toxic:
        return (
            f"{SPECIES_JA.get(species, species)}の中毒性痙攣は曝露物質除去と速やかな抗痙攣薬投与で予後改善。"
            "肝代謝・腎排泄能の種別差で回復速度異なる—肝性脳症併発は予後不良、24時間以上の重積発作は脳浮腫リスク。"
        )
    return (
        f"{SPECIES_JA.get(species, species)}の痙攣は原因により予後が大きく異なる。"
        "代謝性（低血糖・低Ca）は補正で速やかに回復、感染性・腫瘍性は基礎疾患の制御で予後が決まる。"
    )


def _gen_candidiasis(species: str) -> str:
    if species == "Rabbit":
        return (
            "ウサギの口腔カンジダ症は抗菌薬関連dysbiosisが約70-80%—原因抗菌薬の中止と腸内環境是正で予後良好。"
            "ナイスタチン100,000 IU/kg PO q12h × 5-10日で除菌、再発予防に高繊維食必須。"
            "GI stasis併発例は要警戒。"
        )
    if species == "Guinea Pig":
        return (
            "モルモットの口腔カンジダ症はVit C欠乏と免疫低下が背景—Vit C補給（10-30 mg/kg/日）と原因鑑別が必須。"
            "ナイスタチン口腔局所＋イトラコナゾール 5 mg/kg PO q24h（全身性）で2週以内改善。"
            "再発例は基礎免疫疾患検索。"
        )
    if species == "Ferret":
        return (
            "フェレットのカンジダ症は腸炎（ECE）/インスリノーマ/副腎疾患併発の指標—基礎疾患の評価が予後を決める。"
            "局所ナイスタチン＋フルコナゾール 10 mg/kg PO q24h × 14-21日で除菌。"
            "免疫不全状態が持続すれば再発を繰り返し慢性化。"
        )
    if species == "Hedgehog":
        return (
            "ハリネズミのカンジダ症は不適切食事/抗菌薬使用後に発症、皮膚・口腔・腸管型がある。"
            "イトラコナゾール 5 mg/kg PO q24h × 4週間＋局所ミコナゾール、栄養是正で予後良好。"
            "WHS等の基礎疾患併存例は予後注意。"
        )
    if species == "Sugar Glider":
        return (
            "フクロモモンガのカンジダ症（消化管/腸管型）は栄養性Ca欠乏や肝疾患の二次性が多い。"
            "ナイスタチン 100,000 IU/kg PO q12h × 7-10日＋食事改善で予後良好。"
            "再発例はprobiotics併用と基礎疾患スクリーニング。"
        )
    if species == "Degu":
        return (
            "デグーのカンジダ症は糖尿病による高血糖環境での真菌増殖が主因—血糖管理が予後を左右。"
            "フルコナゾール 5 mg/kg PO q24h × 2-3週＋糖尿病管理で予後改善。"
            "未治療の高血糖持続は再発を繰り返す。"
        )
    return (
        f"{SPECIES_JA.get(species, species)}のカンジダ症は局所感染例で予後良好、全身播種型では予後注意。"
        "基礎免疫不全/抗菌薬乱用/栄養不良の是正が長期予後を左右する。"
    )


def _gen_aspergillosis(species: str) -> str:
    if species == "Bird":
        return (
            "鳥類アスペルギルス症（A. fumigatus主）は気嚢炎で発見遅延、急性劇症型は3-7日以内死亡率>80%。"
            "イトラコナゾール 5-10 mg/kg PO q12h × 6-12週＋ボリコナゾール（重症例）で慢性型は60-70%生存。"
            "気嚢肉芽腫の内視鏡下除去で予後改善、抗真菌耐性株は予後不良。"
        )
    if species == "Parakeet":
        return (
            "セキセイインコ等小型インコのアスペルギルス症は乾燥種子食/換気不良環境が誘因—環境改善必須。"
            "イトラコナゾール 5 mg/kg PO q12h × 8-12週＋ネブライゼーション（クロトリマゾール）で急性型60%生存。"
            "気管型は手術リスク高く予後不良。"
        )
    if species == "Parrot":
        return (
            "オウム類（ヨウム・アマゾン等）のアスペルギルス症は慢性経過が多く、診断時には複数気嚢に病巣形成。"
            "ボリコナゾール 12-18 mg/kg PO q12h × 12週以上＋外科肉芽腫除去で50-70%生存可能。"
            "ヨウムの心血管型は予後不良。"
        )
    return (
        f"{SPECIES_JA.get(species, species)}におけるアスペルギルス症は気嚢病変の広がりで予後が決まる。"
        "早期診断＋長期抗真菌療法（イトラコナゾール/ボリコナゾール）で予後改善。"
    )


def _gen_lipoma(species: str) -> str:
    base = "境界明瞭な皮下脂肪腫は外科切除で再発<5%・予後良好。"
    if species == "Rabbit":
        return base + "ウサギは麻酔リスク考慮（呼吸抑制・GI stasis）、術後critical care給餌で予後良好。脂肪肉腫は稀。"
    if species == "Hamster":
        return (
            base
            + "ハムスターでは高齢個体（>1.5歳）の皮下脂肪腫が多く、麻酔リスクで術後数日の経過観察重要。腫瘍は緩徐進行。"
        )
    if species == "Guinea Pig":
        return (
            base
            + "モルモットは肥満動物が多く、脂肪腫頻度高—食事/運動管理で再発予防可能。麻酔は禁飼食回避（C型ボツリヌス毒素感受性）。"
        )
    if species == "Chinchilla":
        return base + "チンチラは皮膚剥離（fur slip）に注意した手術が必要、術後の自咬防止カラー使用。再発は稀。"
    if species == "Hedgehog":
        return base + "ハリネズミは丸まり防御で術前評価困難、麻酔下身体検査必須。腫瘍学的検索でWHS等の併存疾患鑑別。"
    if species == "Sugar Glider":
        return (
            base + "フクロモモンガは小型（80-160g）で麻酔リスク高、外科は専門医対応推奨。良性脂肪腫は完全切除で治癒。"
        )
    if species == "Degu":
        return (
            base
            + "デグーは糖尿病合併症の影響で麻酔リスク評価必須、血糖モニタリング下で外科。再発は飼育環境改善で予防可。"
        )
    if species == "Bird":
        return (
            base
            + "鳥類（特にセキセイインコ・コザクラインコ）は肥満と低栄養（高脂肪種子食）で多発、食事改善＋運動増加で再発予防。"
        )
    if species == "Parakeet":
        return (
            base
            + "セキセイインコの脂肪腫は中高齢メスに多く、ヨウ素不足の甲状腺腫との鑑別必要。低脂肪ペレット食＋飛翔運動で進展抑制。"
        )
    if species == "Parrot":
        return (
            base
            + "オウム類はアマゾン・ヨウム等で高頻度、肝脂肪症や心血管疾患併存例が多く術前評価必須。低脂肪食＋環境エンリッチメントで再発予防。"
        )
    if species == "Reptile":
        return (
            base
            + "爬虫類の脂肪腫はリクガメ・トカゲで報告、過給餌が背景—切除は止血困難（小血管多数）に注意、術後POTZ厳密管理で予後良好。"
        )
    if species == "Tortoise":
        return base + "リクガメの脂肪腫は中年以降（>10歳）に多く、過給餌が背景。甲羅下手術困難で外科適応は慎重判断。"
    if species == "Snake":
        return base + "ヘビの脂肪腫は皮下発生が多く比較的容易に切除可能、麻酔下の止血管理＋POTZ術後管理で予後良好。"
    if species == "Lizard":
        return (
            base
            + "トカゲ（特にヒョウモントカゲモドキ）で報告、過給餌＋カルシウム不足背景。外科切除＋食事改善で予後良好。"
        )
    if species == "Amphibian":
        return base + "両生類の脂肪腫は稀、皮膚バリア機能保持のため最小侵襲手術＋抗菌薬で予後良好。"
    return base


def _gen_melanoma(species: str) -> str:
    base = "早期完全切除（マージン2cm）で予後良好、深部浸潤・転移例は予後不良。"
    if species == "Rabbit":
        return "ウサギのメラノーマは高齢個体の皮膚/眼瞼に発生—" + base + "稀疾患のためエビデンス限定的。"
    if species == "Guinea Pig":
        return "モルモットメラノーマは極めて稀、ほとんどが皮膚良性—" + base + "悪性型は転移性で安楽死検討。"
    if species == "Chinchilla":
        return "チンチラのメラノーマは稀、皮膚良性病変との鑑別が重要—生検必須。" + base
    if species == "Hedgehog":
        return "ハリネズミは全腫瘍中第2位の発生頻度（口腔・棘部位）—" + base + "扁平上皮癌との鑑別で予後判定変わる。"
    if species == "Degu":
        return "デグーのメラノーマは稀、皮膚腫瘤は色素母斑等良性病変との鑑別が必要。" + base
    if species == "Reptile":
        return (
            "爬虫類のメラノーマは極めて稀、診断時には進行例が多い。"
            + base
            + "POTZ復元下の外科＋術後栄養管理で予後改善。"
        )
    if species == "Snake":
        return "ヘビのメラノーマは皮膚/口腔発生が報告、生検＋免疫染色（S100、Melan-A）で診断。" + base
    if species == "Lizard":
        return "トカゲのメラノーマは皮膚/口腔粘膜で報告例あり、悪性度は種により異なる。" + base
    return base


def _gen_leukemia(species: str) -> str:
    base = "種特異的データ限定的—多くは予後不良。"
    if species == "Rabbit":
        return (
            base
            + "ウサギの白血病は中高齢個体に多く、進行性で診断から数週〜数ヶ月の生存。プレドニゾロン緩和＋critical care給餌でQOL維持。"
        )
    if species == "Guinea Pig":
        return (
            base
            + "モルモットの白血病はリンパ性が多く、ウシ白血病ウイルス類似のレトロウイルス関与の報告も。緩和ケア中心。"
        )
    if species == "Chinchilla":
        return base + "チンチラの白血病は極めて稀、CBCで白血球>50,000/μLが診断指標。骨髄生検＋IHCで確定診断後QOL重視。"
    if species == "Hedgehog":
        return (
            base
            + "ハリネズミは全腫瘍中第3位の血液腫瘍—リンパ腫主体。化学療法（COP）で数週〜数ヶ月の延命可能だが、副作用で中止例多い。"
        )
    if species == "Degu":
        return base + "デグーの白血病は文献報告が極めて少なく、自然経過の理解も乏しい。緩和ケアでQOL維持が現実的目標。"
    return base


def _gen_cardiomyopathy(species: str) -> str:
    if species == "Bird":
        return (
            "鳥類心筋症は無症状進行—中央生存は症状出現から6-18ヶ月。"
            "拡張型心筋症はインコ/オウムで報告、ピモベンダン外挿で症状緩和可。"
            "心不全進行例は予後不良。"
        )
    if species == "Parakeet":
        return (
            "セキセイインコの心筋症はアテローム硬化症との鑑別重要—心エコーで診断。"
            "ピモベンダン 0.25 mg/kg PO q12h外挿で症状緩和、診断から平均生存12ヶ月。"
            "腹水・呼吸困難進行例は予後不良。"
        )
    if species == "Parrot":
        return (
            "オウム（特にヨウム・アマゾン）の心筋症はアテロームと併発、進行性で予後不良。"
            "ピモベンダン＋ベナゼプリル外挿で6-18ヶ月延命可能。"
            "失神・腹水発症後は数ヶ月。"
        )
    return f"{SPECIES_JA.get(species, species)}の心筋症は進行性—早期介入で延命可能だが治癒は困難。"


def _gen_ckd(species: str) -> str:
    if species == "Bird":
        return (
            "鳥類CKDは尿酸代謝障害から内臓型痛風移行で予後不良—早期発見＋輸液で進行抑制可能。"
            "アロプリノール 10-30 mg/kg PO q24hで尿酸抑制、症状出現後の中央生存6-12ヶ月。"
        )
    if species == "Parakeet":
        return (
            "セキセイインコCKDは高蛋白食/脱水/中毒（重金属）が主因、診断時には腎機能の50%以上喪失例多い。"
            "輸液+低蛋白食+アロプリノールで中央生存6-12ヶ月。"
        )
    if species == "Parrot":
        return (
            "オウムCKDは慢性脱水と高齢化が主因—症状出現時には進行例。"
            "輸液療法＋食事管理（低蛋白・低Ca）で中央生存6-18ヶ月。痛風移行は予後不良。"
        )
    if species == "Guinea Pig":
        return (
            "モルモットCKDは慢性Vit C欠乏や尿石症の終末像—早期介入で進行抑制可能だが治癒なし。"
            "皮下輸液 50-80 mL/kg/日＋食事制限で数ヶ月〜1年のQOL維持。"
        )
    if species == "Ferret":
        return (
            "フェレットCKDは中高齢（>4歳）の発生頻度高—副腎疾患/insulinoma併発で複雑化。"
            "皮下輸液80-100 mL/kg q48-72h＋低蛋白食＋ACE阻害薬（ベナゼプリル 0.25 mg/kg PO q24h）で中央生存6-18ヶ月。"
        )
    if species == "Hedgehog":
        return (
            "ハリネズミCKDは中高齢（>3歳）で多く、肝疾患/WHS併発で予後修飾。"
            "皮下輸液＋食事改善で進行抑制、診断後の中央生存6-12ヶ月。"
        )
    if species == "Sugar Glider":
        return (
            "フクロモモンガCKDは栄養性Ca欠乏や脱水の終末像で進行性、種特異的データ限定的。"
            "皮下輸液＋Ca/VitD3補正＋食事改善でQOL維持、診断から数ヶ月の生存例多い。"
        )
    if species == "Degu":
        return (
            "デグーCKDは糖尿病性腎症の併発が多い—血糖管理＋輸液で進行抑制が予後決定要因。"
            "未管理糖尿病例では診断から数ヶ月、管理良好例は1年以上のQOL維持可能。"
        )
    return (
        f"{SPECIES_JA.get(species, species)}のCKDは進行性—症状緩和とQOL維持が現実的目標。"
        "早期発見・脱水回避・食事管理で進行抑制可能。"
    )


def _gen_hepatic_fibrosis(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}の肝線維症は代償期は無症状で進行—肝酵素・胆汁酸モニタリングで早期発見が予後改善の鍵。"
        "腹水・肝性脳症・出血傾向（非代償期）出現後の中央生存は3-6ヶ月、UDCA＋抗酸化サプリ（SAMe・シリマリン）で進行遅延。"
    )


def _gen_muscle_wasting(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}における筋萎縮は原疾患（CKD・腫瘍・甲状腺機能異常・関節炎）で予後が決まる。"
        "原因除去後は数週〜数ヶ月で筋肉量回復可能、終末期では緩和ケア中心。"
    )


def _gen_visceral_gout(species: str) -> str:
    if species in _AVIAN:
        return (
            f"{SPECIES_JA.get(species, species)}の内臓型痛風は症状出現時には腎機能の80%以上喪失—予後不良。"
            "アロプリノール 10-30 mg/kg PO q24h＋積極的輸液で延命可能だが診断後の中央生存3-6ヶ月。"
            "生存例も生涯の脱水回避と低蛋白食管理が必要。"
        )
    return (
        f"{SPECIES_JA.get(species, species)}の内臓型痛風は腎不全進行例で予後不良。"
        "早期発見＋脱水管理＋アロプリノールで長期生存可能だが治癒は困難。"
    )


def _gen_articular_gout(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}の関節型痛風は慢性管理でQOL維持可能。"
        "再発予防と内臓型移行の早期発見（尿酸モニタリング）が長期予後を左右する。"
    )


def _gen_disseminated_granuloma(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}の播種性肉芽腫性疾患は予後不良—診断時には複数臓器に病変形成。"
        "早期診断・病原体特定（マイコバクテリア・真菌等）・長期治療で延命可能だが治癒は困難。"
        "免疫不全/栄養不良の併存で予後修飾。"
    )


def _gen_iron_storage(species: str) -> str:
    if species in _AVIAN:
        return (
            f"{SPECIES_JA.get(species, species)}の鉄蓄積症はオオハシ等果実食種で特に問題—診断時には肝障害進行例多い。"
            "瀉血（週1回、10 mL/kg）＋低鉄食（鉄<50 ppm）でフェリチン正常化、6-12ヶ月で予後改善。"
            "肝硬変進行例は予後不良。"
        )
    return f"{SPECIES_JA.get(species, species)}の鉄蓄積症は早期発見＋瀉血/低鉄食で予後良好、肝硬変進行例は予後不良。"


def _gen_constipation(species: str) -> str:
    if species == "Guinea Pig":
        return (
            "モルモットの消化管うっ滞は12-24時間以上の絶食で発症、48時間以上で肝リピドーシス併発リスク。"
            "シメチコン＋メトクロプラミド＋critical care給餌 80-100 mL/kg/日 syringeで早期介入で予後良好。"
            "盲腸鼓脹は予後注意。"
        )
    if species in _REPTILE:
        return (
            f"{SPECIES_JA.get(species, species)}の便秘は脱水/低温/栄養不良/異物が主因—POTZ復元＋温浴で多くは改善。"
            "原因除去で予後良好、慢性化例は腸閉塞や敗血症移行で予後不良。"
        )
    return f"{SPECIES_JA.get(species, species)}における便秘は原因除去（脱水補正・食事改善・運動増加）で予後良好。"


def _gen_dental_abscess(species: str) -> str:
    if species == "Horse":
        return (
            "馬の歯根膿瘍は罹患歯抜歯で治癒可能だが、術後の鼻洞性瘻孔・上顎洞炎合併例は予後注意。"
            "早期介入（症状出現2週以内）で良好予後、慢性瘻孔形成例は再手術リスク。"
            "高齢馬の臼歯抜歯後は対合歯のオーバーグロースで生涯歯科ケア必要。"
        )
    return f"{SPECIES_JA.get(species, species)}の歯根膿瘍は罹患歯抜歯＋抗菌薬で治癒可能、診断遅延例は予後注意。"


def _gen_distemper(species: str) -> str:
    return (
        "犬ジステンパー（特異的抗ウイルス薬なし）の予後はワクチン接種歴・年齢・神経症状の有無で大きく異なる。"
        "未接種子犬での全身性感染: 致死率50-80%、生存例も神経学的後遺症（hard pad、ミオクローヌス、慢性発作）高頻度。"
        "成犬不顕性〜軽症例: 良好予後。神経型（亜急性〜慢性）: 進行性で予後不良、安楽死選択も。"
    )


def _gen_vit_a_deficiency(species: str) -> str:
    if species == "Ferret":
        return (
            "フェレットのビタミンA欠乏は安価ドッグフード給餌で稀に発生—肉食ベース食事改善＋VitA補給（5000 IU/kg PO週1回×4週）で予後良好。"
            "症状進行（角膜潰瘍・呼吸器感染）例は数週で完全回復可能。"
        )
    if species == "Sugar Glider":
        return (
            "フクロモモンガのビタミンA欠乏は不適切食事（果実偏重）が主因—食事改善＋肝油補給で4-8週以内に改善。"
            "皮膚/視覚症状の永続的後遺症リスクあり早期介入が予後を左右。"
        )
    if species == "Degu":
        return (
            "デグーのビタミンA欠乏は飼育者の認識不足で進行例多い—食事改善＋低用量補給で予後良好。"
            "高用量補給は過剰症リスクで漸進的調整必要。"
        )
    if species == "Guinea Pig":
        return (
            "モルモットのビタミンA欠乏はVit C欠乏と併発しやすい—包括的栄養改善で4-6週以内に予後良好。"
            "再発防止に高品質ペレット＋緑黄色野菜の継続給餌が必要。"
        )
    return f"{SPECIES_JA.get(species, species)}のビタミンA欠乏症は食事矯正と漸進的補給で4-8週以内に予後良好、永続的視覚障害は稀。"


def _gen_vit_d3_excess(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}のビタミンD3過剰症による転移性石灰化は不可逆—予後要警戒。"
        "早期発見＋VitD3中止＋低Ca食＋輸液で進展抑制可能、慢性腎不全進行例は予後不良。"
    )


def _gen_thiamine_deficiency(species: str) -> str:
    return f"{SPECIES_JA.get(species, species)}のチアミン欠乏症はB1補給（10-50 mg/kg IM/PO）で数日以内に予後改善、診断遅延は永続的神経学的後遺症。"


def _gen_mycobacteriosis(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}のマイコバクテリウム症（鳥結核）は予後不良。"
        "長期多剤併用（azithromycin+rifampin+ethambutol 6-12ヶ月）でも再発率高く、群への感染拡大リスクから安楽死を検討する。"
        "人獣共通感染症リスクあり防護必須。"
    )


def _gen_myiasis(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}の蝿蛆症（ハエウジ症）は早期発見・蛆除去＋イベルメクチンで予後良好。"
        "深部組織浸潤・全身感染合併例は予後要警戒、脱水・敗血症で予後不良化。"
    )


def _gen_leech(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}のヒル寄生症は除去＋環境改善（清浄水）で予後優良。"
        "重度貧血合併例は輸血/輸液で支持治療必要、二次感染対応で予後良好。"
    )


def _gen_stress_syndrome(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}のストレス症候群は環境改善（温度・湿度・社会的環境）で予後良好。"
        "慢性放置は免疫抑制から日和見感染→致死的経過もある—早期介入が予後を左右。"
    )


def _gen_abdominal_hernia(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}の腹壁ヘルニアは早期外科修復で予後良好。"
        "嵌頓・絞扼例は緊急対応必要—診断遅延・敗血症進行で予後不良。"
    )


def _gen_peritonitis(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}の腹膜炎・体腔炎は早期外科治療＋抗菌薬で予後改善。"
        "診断遅延・敗血症進行例は予後不良、原因（穿孔/腫瘍/卵関連）で予後修飾。"
    )


def _gen_follicular_stasis(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}の濾胞停滞はGnRH/hCG＋環境改善で内科的に予後良好。"
        "難治例は卵巣摘出で根治、慢性化は卵関連体腔炎リスクで早期介入が予後を左右。"
    )


def _gen_avian_chlamydia(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}のクラミジア症（オウム病）はドキシサイクリン 25-50 mg/kg PO q24h × 45日で除菌、生存率>90%。"
        "人獣共通感染症—飼育者への警告と検査推奨。再感染リスクあり群管理が予後を左右。"
    )


def _gen_hyperthyroidism(species: str) -> str:
    if species == "Cat":
        return (
            "猫甲状腺機能亢進症の予後は治療法選択で大きく異なる。"
            "I-131治療: 治癒率>95%、中央生存4年以上。"
            "メチマゾール内服: 5年生存約70%（甲状腺癌でなければ）、副作用で10-15%が薬剤変更。"
            "甲状腺摘出: 治癒可能だが術後低Ca血症リスク。"
            "未治療例は心不全・腎不全・削痩で1-2年以内死亡、治療後CKD顕在化が15-25%で発生。"
        )
    return (
        f"{SPECIES_JA.get(species, species)}における甲状腺機能亢進症の予後は基礎病態（腺腫/癌/medication-induced）で異なる。"
        "適切な治療管理で5年以上の長期生存可能、未治療例は心不全・削痩で予後不良。"
    )


def _gen_hyperparathyroidism(species: str, name_ja: str) -> str:
    is_nutritional = "栄養性" in name_ja
    is_renal = "腎性" in name_ja
    is_primary = "原発性" in name_ja
    is_hypo = "機能低下" in name_ja
    sp_ja = SPECIES_JA.get(species, species)
    if is_hypo:
        return (
            f"{sp_ja}副甲状腺機能低下症の予後はCa/VitD補充療法で良好に管理可能。"
            "急性低Ca血症はグルコン酸Ca IV即時補正、慢性管理はカルシトリオール+Ca補給で生涯コントロール。"
            "原疾患（甲状腺手術後/自己免疫性/特発性）の鑑別で予後修飾、補充療法継続例は寿命に近い予後。"
        )
    if is_nutritional:
        return (
            f"{sp_ja}栄養性二次性副甲状腺機能亢進症（NSHP）は食事改善+Ca/VitD3補給で骨吸収停止、4-8週で予後良好。"
            "ただし既存の骨格変形は永続的—成長期罹患例は機能温存可能だが骨折リスク残存。"
            "再発防止には栄養バランス継続管理が必須。"
        )
    if is_renal:
        return (
            f"{sp_ja}腎性二次性副甲状腺機能亢進症の予後はCKDの進行度（IRISステージ）に従う。"
            "低リン食+リン吸着剤（Sevelamer/水酸化Al）+カルシトリオールでPTH抑制、CKD単独より生存期間短縮。"
            "皮膚石灰沈着・繊維性骨炎進行例は予後不良。"
        )
    if is_primary:
        return (
            f"{sp_ja}原発性副甲状腺機能亢進症は副甲状腺腺腫切除で治癒率>90%、中央生存5年以上の良好な予後。"
            "術後一過性低Ca血症（hungry bone syndrome）に注意—Ca/VitD3前処置で予防。"
            "未手術例は高Ca血症性腎症・尿石症で予後悪化。"
        )
    return (
        f"{sp_ja}における副甲状腺機能異常はPTH/Ca/P/VitDモニタリングで適切に管理することで予後良好。"
        "原疾患鑑別（原発性/栄養性/腎性）が治療選択と長期予後を左右する。"
    )


def _gen_lymphoma_cat(species: str) -> str:
    if species == "Cat":
        return (
            "猫リンパ腫は組織型で予後大きく異なる。"
            "縦隔型・多中心型: CHOP化学療法でMST 6-12ヶ月。"
            "皮膚型: 緩徐進行で長期生存例あり。"
            "鼻腔型: 放射線療法でMST 1.5-3年。"
            "消化器小細胞型: chlorambucil+prednisoloneで2-3年生存可能、大細胞型は予後不良（MST 3-6ヶ月）。"
        )
    return (
        f"{SPECIES_JA.get(species, species)}のリンパ腫は組織型と病期で予後が決まる。"
        "化学療法（CHOP/COP）で寛解可能、未治療例は急速進行。"
    )


def _gen_nshp_mbd(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}の栄養性骨異栄養症（MBD）は早期診断・食事矯正＋Ca/VitD3補給で予後良好。"
        "骨格変形は永続的だが機能温存可能、重度進行例は骨折リスクで要慎重ハンドリング。"
    )


def _gen_mucormycosis(species: str) -> str:
    return (
        f"{SPECIES_JA.get(species, species)}のムコール症（接合菌症）は侵襲性で予後不良。"
        "アゾール耐性のためアムホテリシンB＋早期外科切除＋環境改善が必要、診断遅延は予後不良。"
    )


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------
_GENERATORS = {
    "hypothermia": _gen_hypothermia,
    "dehydration": _gen_dehydration,
    "seizure": lambda sp, name: _gen_seizure(sp, name),
    "toxic_seizure": lambda sp, name: _gen_seizure(sp, name),
    "candidiasis": _gen_candidiasis,
    "aspergillosis": _gen_aspergillosis,
    "lipoma": _gen_lipoma,
    "melanoma": _gen_melanoma,
    "leukemia": _gen_leukemia,
    "lymphoma": _gen_lymphoma_cat,
    "cardiomyopathy": _gen_cardiomyopathy,
    "ckd": _gen_ckd,
    "hepatic_fibrosis": _gen_hepatic_fibrosis,
    "muscle_wasting": _gen_muscle_wasting,
    "visceral_gout": _gen_visceral_gout,
    "articular_gout": _gen_articular_gout,
    "disseminated_granuloma": _gen_disseminated_granuloma,
    "iron_storage": _gen_iron_storage,
    "constipation": _gen_constipation,
    "dental_abscess": _gen_dental_abscess,
    "distemper": _gen_distemper,
    "vit_a_deficiency": _gen_vit_a_deficiency,
    "vit_d3_excess": _gen_vit_d3_excess,
    "thiamine_deficiency": _gen_thiamine_deficiency,
    "mycobacteriosis": _gen_mycobacteriosis,
    "myiasis": _gen_myiasis,
    "leech": _gen_leech,
    "stress_syndrome": _gen_stress_syndrome,
    "abdominal_hernia": _gen_abdominal_hernia,
    "peritonitis": _gen_peritonitis,
    "follicular_stasis": _gen_follicular_stasis,
    "avian_chlamydia": _gen_avian_chlamydia,
    "hyperthyroidism": _gen_hyperthyroidism,
    "hyperparathyroidism": lambda sp, name: _gen_hyperparathyroidism(sp, name),
    "nshp_mbd": _gen_nshp_mbd,
    "mucormycosis": _gen_mucormycosis,
    "gout": _gen_visceral_gout,
}


def generate_species_prognosis(species: str, name_ja: str, name_en: str | None) -> str | None:
    """Generate species-specific prognosis_ja for the given entry.

    Returns None if no generator matches (caller should keep existing text).
    """
    disease = detect_disease(name_ja or "", name_en or "")
    if disease == "_generic":
        return None
    gen = _GENERATORS.get(disease)
    if not gen:
        return None
    try:
        if gen.__code__.co_argcount == 1:
            return gen(species)
        return gen(species, name_ja or "")
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Main: process the JSON
# ---------------------------------------------------------------------------
def main() -> None:
    json_path = ROOT / "diseases_all_species.json"
    if not json_path.exists():
        print(f"ERROR: {json_path} not found")
        sys.exit(1)

    print(f"Loading {json_path}...")
    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    # Detect shared prognosis_ja text (3+ species OR 3+ diseases)
    by_species_set: dict[str, set[str]] = defaultdict(set)
    by_diseases: dict[str, list[dict]] = defaultdict(list)
    for entry in data:
        p = (entry.get("prognosis_ja") or "").strip()
        sp = entry.get("species") or ""
        name = (entry.get("name_ja") or entry.get("name") or "").strip()
        if p and name and sp:
            by_species_set[p].add(sp)
            by_diseases[p].append(entry)

    template_progs = {p for p in by_species_set if len(by_species_set[p]) >= 3 or len(by_diseases[p]) >= 3}
    affected_entries = sum(len(by_diseases[p]) for p in template_progs)
    print(f"Detected {len(template_progs)} prognosis templates affecting {affected_entries} entries")

    replaced = 0
    skipped_no_generator: dict[str, int] = defaultdict(int)
    for entry in data:
        p = (entry.get("prognosis_ja") or "").strip()
        if p not in template_progs:
            continue
        new_p = generate_species_prognosis(
            entry.get("species") or "",
            entry.get("name_ja") or "",
            entry.get("name") or "",
        )
        if new_p and new_p != p:
            entry["prognosis_ja"] = new_p
            replaced += 1
        else:
            key = (entry.get("name_ja") or entry.get("name") or "")[:30]
            skipped_no_generator[key] += 1

    print(f"\nReplaced {replaced} entries")
    if skipped_no_generator:
        print(f"Skipped {sum(skipped_no_generator.values())} entries (no generator):")
        for name, n in sorted(skipped_no_generator.items(), key=lambda x: -x[1])[:10]:
            print(f"  {n}x: {name}")

    print(f"\nWriting {json_path}...")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))

    # Verify result
    print("\nVerifying...")
    by_species_set2: dict[str, set[str]] = defaultdict(set)
    by_diseases2: dict[str, list[dict]] = defaultdict(list)
    for entry in data:
        p = (entry.get("prognosis_ja") or "").strip()
        sp = entry.get("species") or ""
        name = (entry.get("name_ja") or entry.get("name") or "").strip()
        if p and name and sp:
            by_species_set2[p].add(sp)
            by_diseases2[p].append(entry)
    remaining = sum(1 for p in by_species_set2 if len(by_species_set2[p]) >= 3 or len(by_diseases2[p]) >= 3)
    print(f"  Remaining prognosis templates (3+ species or 3+ diseases): {remaining}")


if __name__ == "__main__":
    main()
