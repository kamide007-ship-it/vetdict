"""Fix the dermatology fallback template that leaked canine drugs and
category-inappropriate work-ups into other species and non-skin diseases.

2026-10 監査（第67弾）で、皮膚科フォールバック生成器の定型ブロック
（「皮膚生検（パンチまたはincisional）…アレルギー性: … シクロスポリン 5-7 mg/kg PO q24h、
オクラシチニブ（犬専用）。外用ケア: 抗菌・抗真菌シャンプー q3-7日」）が 32 エントリの
treatment_ja に残存していた。問題は2系統:

1. 皮膚疾患ではない疾患への誤適用（臨床的に誤り）: 爬虫類・両生類の鞭毛虫感染（消化管原虫）、
   モルモット毛球症、フェレット胃毛球閉塞、チンチラ陰茎毛輪、フクロモモンガ尾部皮膚剥離、
   各種皮膚腫瘍（組織球腫・肥満細胞腫・毛包腫）等 — 疾患固有の治療に全置換する。
2. 皮膚疾患でも種に不適切な行: 犬専用の JAK 阻害薬・犬猫用シクロスポリン用量を鳥・爬虫類・
   小型哺乳類・馬に提示、鳥・爬虫類・両生類へのシャンプー推奨 — 種別の行に置換する。

加えて馬の汎用皮膚テンプレート末尾（「…アレルギー性にはステロイド、アポキル、サイトポイント等を
使用する…」）を馬・デグーから除去する（いずれも犬専用製剤）。

Usage:
    python3 scripts/template_elimination/fix_derm_template_cross_species.py [--apply]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

DERM_MARKER = "皮膚生検（パンチまたはincisional）"
OLD_ALLERGY = (
    "アレルギー性: 食物アレルギー除外食試験（8週hydrolyzed蛋白食）、環境アレルゲン特異IgE。"
    "シクロスポリン 5-7 mg/kg PO q24h、オクラシチニブ（犬専用）。"
)
OLD_TOPICAL = "外用ケア: 抗菌・抗真菌シャンプー q3-7日、湿潤環境改善。"
DOG_SUFFIX = (
    "皮膚疾患の治療は基礎疾患の特定と原因除去が最も重要である。感染性皮膚疾患には感受性試験に基づく"
    "抗菌薬・抗真菌薬を投与し、アレルギー性にはステロイド、アポキル、サイトポイント等を使用する。"
    "局所療法としてシャンプー療法、外用薬を併用し、再発予防のためのスキンケアプログラムを策定する。"
)

SMALL_MAMMALS = {
    "rabbit",
    "guinea_pig",
    "chinchilla",
    "hamster",
    "degu",
    "ferret",
    "hedgehog",
    "sugar_glider",
    "exotic_other",
}
BIRDS = {"bird", "parakeet", "parrot"}
REPTILES = {"reptile", "lizard", "snake", "tortoise"}

ALLERGY_LINE = {
    "cat": "アレルギー性: 食物アレルギー除外食試験（8週加水分解蛋白食）、ノミ対策の徹底。シクロスポリン 7 mg/kg PO q24h（猫ラベル用量）。",
    "horse": "アレルギー性: 原因アレルゲンの回避（Culicoides対策・飼料変更）、短期のプレドニゾロン/デキサメタゾン、抗ヒスタミン薬（セチリジン 0.2-0.4 mg/kg PO q12h）、アレルゲン特異的免疫療法。犬用のオクラシチニブ・ロキベトマブは馬では適応外。",
    "small": "アレルギー性（まれ）: 寄生虫・感染・床材や環境刺激の除外を優先。犬猫用の免疫抑制薬・JAK阻害薬（シクロスポリン・オクラシチニブ）は本種で用量未確立のため用いない。",
    "bird": "アレルギー性（除外診断）: 鳥では皮膚アレルギーの確証は乏しく、感染・寄生虫・栄養（ビタミンA）・環境（乾燥・喫煙・エアロゾル）・行動要因の除外を優先する。犬猫用の免疫抑制薬・JAK阻害薬は用いない。",
    "reptile": "爬虫類ではアレルギー性皮膚疾患はほぼ報告がない — 飼育環境（温度勾配・湿度・床材・UV-B）の是正と感染症の治療を優先する。",
    "amphibian": "両生類ではアレルギー性皮膚疾患はほぼ報告がない — 水質（アンモニア・亜硝酸・塩素）と温度・湿度の是正、感染症の治療を優先する。",
}
TOPICAL_LINE = {
    "bird": "外用ケア: シャンプーは用いない（羽毛の防水性・保温性を損なう）。病変部のみ希釈クロルヘキシジン/ポビドンヨードで局所洗浄。",
    "reptile": "外用ケア: 希釈ポビドンヨード/クロルヘキシジン浴、乾燥した清潔な床材（新聞紙・ペットシーツ）と適切な湿度管理。",
    "amphibian": "外用ケア: シャンプー・消毒薬の原液は禁忌（皮膚呼吸・経皮吸収）。脱塩素水で清潔を保ち、薬浴は両生類用量で行う。",
}


def _group(sp: str) -> str:
    if sp in BIRDS:
        return "bird"
    if sp in REPTILES:
        return "reptile"
    if sp == "amphibian":
        return "amphibian"
    if sp in SMALL_MAMMALS:
        return "small"
    return sp


def _flagellate_ja(label: str, amphibian: bool) -> str:
    dose = (
        "メトロニダゾール 10 mg/kg PO q24h × 5-10日、または 50 mg/L 薬浴（最長24時間）（Wright & Whitaker; Carpenter 6th）"
        if amphibian
        else "メトロニダゾール 25-50 mg/kg PO（q14日 × 3回、または q24-48h で2-3回投与後に便再検）。"
        "キングヘビ・ミルクヘビ・インディゴヘビは高感受性のため 40 mg/kg 単回を上限とする（Carpenter 6th）"
    )
    env = "脱塩素水の頻回交換と水温の是正" if amphibian else "至適温度（POTZ）の維持と温浴・輸液による脱水補正"
    return (
        f"【{label}】消化管の鞭毛虫（Hexamita/Spironucleus/Trichomonas）感染。確定: 新鮮便の加温生理食塩水"
        f"直接塗抹で運動性栄養型を確認（少数は健常個体にも常在 — 臨床徴候と虫体数で判断）。治療: {dose}。"
        f"支持療法: {env}、強制給餌。ケージ・水入れの消毒と糞便の頻回除去で再感染を防ぎ、治療2-4週後の"
        "便検査で陰性を確認する。"
    )


def _tumor_ja(label: str, extra: str = "") -> str:
    return (
        f"【{label}】皮膚腫瘤は細胞診で円形細胞腫瘍（肥満細胞腫）等と鑑別し、外科的切除と病理組織検査で"
        f"確定する（多くは良性で完全切除により根治）。{extra}切除不能・高齢で麻酔リスクが高い場合は"
        "経過観察し、増大・潰瘍化で再評価する。疼痛管理と創部保護（自咬防止）を行う。"
    )


CURATED: dict[tuple[str, str], tuple[str, str | None]] = {
    **{
        (sp, "Flagellate Protozoan Infection"): (_flagellate_ja(lbl, sp == "amphibian"), None)
        for sp, lbl in (
            ("amphibian", "両生類の鞭毛虫感染"),
            ("lizard", "トカゲの鞭毛虫感染"),
            ("reptile", "爬虫類の鞭毛虫感染"),
            ("snake", "ヘビの鞭毛虫感染"),
            ("tortoise", "リクガメの鞭毛虫感染"),
        )
    },
    ("chinchilla", "Fur Ring"): (
        "【チンチラの陰茎毛輪（ファーリング）】軽い鎮静下で包皮を反転し、潤滑剤（水溶性ゼリー/ミネラルオイル）を"
        "用いて陰茎に絡んだ被毛の輪を慎重に巻き戻して除去する。嵌頓包茎・陰茎の腫脹が強ければ冷却と"
        "潤滑で整復し、壊死があれば外科処置を検討。鎮痛（メロキシカム 0.5-1 mg/kg PO q24h）。"
        "繁殖期の未去勢雄は月1-2回の定期チェックを飼い主に指導する（Quesenberry & Carpenter 4th）。",
        None,
    ),
    ("ferret", "Gastric Hairball Obstruction"): (
        "【フェレットの胃毛球閉塞】完全閉塞（持続嘔吐・吐出・腹部痛・虚脱）は緊急: 輸液で安定化後に胃切開で"
        "除去する。部分閉塞は輸液・制吐（マロピタント 1 mg/kg SC q24h）・毛球除去剤（石油系緩下剤 1-2 mL PO"
        " q12h）で内科管理し、改善がなければ手術へ。腸閉塞を伴う場合はプロキネティクスを用いない。"
        "インスリノーマ併発例は絶食中の低血糖に注意。予防: 換毛期のブラッシングと毛球除去剤"
        "（Quesenberry & Carpenter 4th）。",
        None,
    ),
    ("guinea_pig", "Trichobezoar"): (
        "【モルモットの毛球症】多くは消化管うっ滞の一表現。輸液（等張液 80-100 mL/kg/日 SC）・保温・"
        "シリンジ給餌（Critical Care 50-80 mL/kg/日を分割）・鎮痛（メロキシカム 0.5 mg/kg PO q24h）で"
        "腸管運動を回復させ、閉塞がないことを画像で確認してから運動促進薬（メトクロプラミド 0.2-0.5 mg/kg"
        " q12h）を用いる。完全閉塞は外科的摘出。牧草主体の食事とビタミンC補給、グルーミング過多（毛噛み）"
        "の原因対策で再発を防ぐ。",
        "Usually a manifestation of GI stasis. Fluids (80-100 mL/kg/day SC), warmth, syringe feeding "
        "(Critical Care 50-80 mL/kg/day divided), analgesia (meloxicam 0.5 mg/kg PO q24h); confirm the absence "
        "of obstruction on imaging before prokinetics (metoclopramide 0.2-0.5 mg/kg q12h). Complete obstruction "
        "requires surgical removal. Prevent recurrence with a hay-based diet, vitamin C supplementation and "
        "management of barbering (Quesenberry & Carpenter 4th ed).",
    ),
    ("sugar_glider", "Tail Degloving"): (
        "【フクロモモンガの尾部皮膚剥離】露出した尾椎は皮膚が再生しないため、麻酔下での尾部断尾"
        "（健常皮膚で被覆できる位置）が標準治療。周術期鎮痛（ブプレノルフィン 0.01-0.03 mg/kg SC q8h、"
        "メロキシカム 0.2 mg/kg PO q24h）、自咬防止のカラー、術後抗菌薬は汚染創のみ。ケージ内の"
        "引っかかり（ワイヤー・回し車の隙間）を除去し、ストレス・自咬症の原因を評価する"
        "（Johnson-Delaney; Quesenberry & Carpenter 4th）。",
        "Exposed coccygeal vertebrae cannot re-epithelialise: amputate the tail under anaesthesia at a level "
        "where healthy skin can close the wound. Perioperative analgesia (buprenorphine 0.01-0.03 mg/kg SC q8h, "
        "meloxicam 0.2 mg/kg PO q24h), a collar against self-mutilation, antimicrobials only for contaminated "
        "wounds. Remove cage hazards (wire gaps, wheels) and assess stress/self-mutilation triggers "
        "(Johnson-Delaney; Quesenberry & Carpenter 4th ed).",
    ),
    ("dog", "Cutaneous Histiocytoma"): (
        "【犬皮膚組織球腫】若齢犬（多くは3歳未満）の良性腫瘍で、多くは1-3ヶ月で自然退縮する（治療不要）。"
        "細胞診で肥満細胞腫など他の円形細胞腫瘍を除外することが必須。3ヶ月以上退縮しない・急速増大・"
        "潰瘍化して不快な場合は外科的切除（または小病変の凍結手術）と病理検査。予後優良"
        "（Withrow & MacEwen 6th）。",
        None,
    ),
    ("dog", "Calcinosis Cutis"): (
        "【犬皮膚石灰沈着症】基礎疾患の治療が中心: 医原性クッシング（ステロイドの漸減中止）、自然発生性"
        "クッシング（トリロスタン）、慢性腎臓病（リン制限・リン吸着剤）。局所: DMSO 50%外用 q12h で沈着の"
        "溶解を促進しうる。二次感染は培養に基づく抗菌薬、病変は易感染・潰瘍化するため丁寧な創傷管理。"
        "大きな限局病変は外科切除。基礎疾患が是正されれば数ヶ月で退縮（Gross 2005; Miller 2013）。",
        None,
    ),
    ("cat", "Mast Cell Tumor (Cutaneous)"): (
        "【猫皮膚肥満細胞腫】多くは高分化型で良性の挙動: 1-2 cmマージンでの外科切除と病理組織検査（頭頸部に"
        "好発）。多形型・多発例・非典型組織像は腹部超音波・リンパ節・CBCで病期分類し、内臓型（脾臓）を除外。"
        "不完全切除には放射線療法を検討。抗ヒスタミン薬・プレドニゾロンは脱顆粒関連症状の管理に。"
        "単発の高分化型は切除で90%以上根治（Litster & Sorenmo 2006; Withrow & MacEwen 6th）。",
        None,
    ),
    ("cat", "Feline Acquired Cutaneous Fragility Syndrome"): (
        "【猫後天性皮膚脆弱症候群】特異的治療はなく基礎疾患の同定と治療が必須: 副腎皮質機能亢進症"
        "（トリロスタン）、医原性（ステロイド・酢酸メゲストロール等プロゲスチンの中止）、肝リピドーシス"
        "（食道チューブによる栄養管理）、糖尿病、FIP、膵癌、慢性腎臓病。創傷は希釈クロルヘキシジン洗浄と"
        "非固着性ドレッシングで管理し、粘着テープは使わない（剥離時に裂傷）。極めて愛護的な保定・柔らかい"
        "床、エリザベスカラー、鎮痛（ブプレノルフィン 0.01-0.02 mg/kg OTM q8-12h）。予後は基礎疾患に依存し"
        "多くは要注意。",
        None,
    ),
    ("parrot", "Feather Destructive Behavior (Feather Plucking)"): (
        "【オウムの羽毛破壊行動（毛引き症）】まず医学的原因を除外: 全身疾患（肝・腎・生殖器・重金属中毒）、"
        "皮膚感染・寄生虫、栄養（ビタミンA欠乏・種子食）、PBFD。医学的原因が否定されれば行動・環境管理が"
        "治療の中心: フォージング等の採餌エンリッチメント、10-12時間の暗く静かな睡眠、ペレット主体への"
        "食事転換、日光浴/UV照明・水浴び、社会的関わりの適正化、発情（性ホルモン）関連はGnRHアゴニスト"
        "（デスロレリン/リュープロレリン）を検討。カラーは自咬創がある場合の一時使用に限る。難治例の"
        "向精神薬（ハロペリドール等）は行動療法と併用する（Ritchie & Harrison; van Zeeland 2009）。",
        "First rule out medical causes: systemic disease (liver, kidney, reproductive, heavy-metal toxicosis), "
        "skin infection/parasites, nutrition (hypovitaminosis A, seed diet) and PBFD. Once excluded, behaviour and "
        "environment are the treatment: foraging enrichment, 10-12 h of dark quiet sleep, conversion to a pelleted "
        "diet, natural/UV light and bathing, appropriate social interaction, and GnRH agonists (deslorelin/"
        "leuprolide) for sex-hormone-driven plucking. Collars only temporarily for self-inflicted wounds; "
        "psychoactive drugs (e.g. haloperidol) only alongside behaviour therapy (Ritchie & Harrison; van Zeeland 2009).",
    ),
    ("guinea_pig", "Grease Gland Infection"): (
        "【モルモットの脂腺感染】臀部背側（尾腺）の皮脂を温かい石鹸水またはココナッツオイルで軟化させ丁寧に"
        "除去し、クロルヘキシジン0.05%で1日2回洗浄、細菌感染にはムピロシン軟膏。蜂窩織炎を伴う場合は"
        "エンロフロキサシン 5-10 mg/kg PO q12h（経口ペニシリン・アンピシリン・セファロスポリンは禁忌）。"
        "雄で目立ち、去勢で皮脂腺活動が低下する。1-2週毎の定期清拭を飼い主に指導（Quesenberry & Carpenter 4th）。",
        None,
    ),
    ("horse", "Food Allergies"): (
        "【馬の食物アレルギー】まれな疾患で除外診断: 蕁麻疹・掻痒を示す馬では昆虫過敏症（Culicoides）・"
        "接触性・薬物性を先に除外する。診断は8-12週間の除去食試験（単一の粗飼料と新規の穀類のみ）と再負荷"
        "試験（血清IgE検査は食物アレルギーの診断に推奨されない）。急性期はデキサメタゾン 0.04-0.1 mg/kg IV/IM"
        " 単回、抗ヒスタミン薬（セチリジン 0.2-0.4 mg/kg PO q12h、ヒドロキシジン 1-1.5 mg/kg PO q8-12h）。"
        "原因飼料の恒久的除去で予後良好（Scott & Miller, Equine Dermatology 2nd）。",
        "Rare and a diagnosis of exclusion: rule out insect (Culicoides) hypersensitivity, contact and drug "
        "reactions first. Diagnose with an 8-12-week elimination diet (single forage plus a novel grain) and "
        "re-challenge — serum IgE testing is not recommended for food allergy. Acute flares: dexamethasone "
        "0.04-0.1 mg/kg IV/IM once; antihistamines (cetirizine 0.2-0.4 mg/kg PO q12h, hydroxyzine 1-1.5 mg/kg "
        "PO q8-12h). Good prognosis once the offending feed is permanently removed (Scott & Miller, Equine "
        "Dermatology 2nd ed).",
    ),
    ("guinea_pig", "Trichofolliculoma"): (_tumor_ja("モルモットの毛包腫"), None),
    ("guinea_pig", "Trichofolliculoma (Basal Cell Tumor)"): (
        _tumor_ja("モルモットの毛包腫（基底細胞腫）", "モルモットで最も多い皮膚腫瘍で、腰背部に好発する。"),
        None,
    ),
    ("guinea_pig", "Trichoepithelioma"): (_tumor_ja("モルモットの毛包上皮腫"), None),
    ("rabbit", "Trichoblastoma"): (
        _tumor_ja("ウサギの毛芽腫", "ウサギで最も多い皮膚腫瘍の一つで、頭頸部・体幹に好発する。"),
        None,
    ),
}


def fix_text(text: str, sp: str, name: str) -> str:
    if not text:
        return text
    out = text
    if sp in ("horse", "degu") and DOG_SUFFIX in out:
        out = out.replace(DOG_SUFFIX, "").rstrip()
    if DERM_MARKER in out and (sp, name) in CURATED:
        return CURATED[(sp, name)][0]
    g = _group(sp)
    if sp != "dog" and OLD_ALLERGY in out:
        out = out.replace(OLD_ALLERGY, ALLERGY_LINE.get(g, ALLERGY_LINE["small"]))
    if g in TOPICAL_LINE and OLD_TOPICAL in out:
        out = out.replace(OLD_TOPICAL, TOPICAL_LINE[g])
    return out


def _generic_en(text: str) -> bool:
    return (
        text.startswith("■Identify underlying cause through species-appropriate")
        or text.startswith("Appropriate treatment based on specific diagnosis")
        or text.startswith("Dermatological disease: Skin scraping")
    )


JSON_SPECIES = {
    "Dog": "dog", "Cat": "cat", "Horse": "horse", "Rabbit": "rabbit", "Guinea Pig": "guinea_pig",
    "Chinchilla": "chinchilla", "Hamster": "hamster", "Degu": "degu", "Ferret": "ferret",
    "Hedgehog": "hedgehog", "Sugar Glider": "sugar_glider", "Bird": "bird", "Parakeet": "parakeet",
    "Parrot": "parrot", "Reptile": "reptile", "Lizard": "lizard", "Snake": "snake", "Tortoise": "tortoise",
    "Amphibian": "amphibian", "Fish": "fish", "Exotic Other": "exotic_other",
}  # fmt: skip
MODULE_SPECIES = {"equine": "horse"}


def main(apply: bool) -> None:
    path = ROOT / "diseases_all_species.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    n = 0
    for x in data:
        sp = JSON_SPECIES.get(x.get("species", ""))
        if not sp:
            continue
        name = x.get("name", "")
        new = fix_text(x.get("treatment_ja") or "", sp, name)
        if new != (x.get("treatment_ja") or ""):
            x["treatment_ja"] = new
            n += 1
        if (sp, name) in CURATED and CURATED[(sp, name)][1] and _generic_en(x.get("treatment") or ""):
            x["treatment"] = CURATED[(sp, name)][1]
            n += 1
    print(f"JSON fields fixed: {n}")
    if apply:
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, separators=(",", ":"))

    import importlib

    n_mod = 0
    for f in sorted((ROOT / "api" / "species").glob("*_diseases.py")):
        stem = f.stem[: -len("_diseases")]
        sp = MODULE_SPECIES.get(stem, stem)
        src = f.read_text(encoding="utf-8")
        new_src = src
        mod = importlib.import_module(f"api.species.{f.stem}")
        for d in getattr(mod, "DISEASES", []) or []:
            if not isinstance(d, dict):
                continue
            name = d.get("name", "")
            for fld in ("treatment_ja", "treatment"):
                old = d.get(fld) or ""
                if not old:
                    continue
                if fld == "treatment_ja":
                    new = fix_text(old, sp, name)
                else:
                    cur = CURATED.get((sp, name))
                    new = cur[1] if cur and cur[1] and _generic_en(old) else old
                if new != old:
                    lit_old = json.dumps(old, ensure_ascii=False)
                    lit_new = json.dumps(new, ensure_ascii=False)
                    # 同一の汎用文が同ファイルの他疾患にもあるため、当該疾患の
                    # "name" 位置以降の最初の出現のみを置換する
                    anchor = new_src.find('"name": ' + json.dumps(name, ensure_ascii=False))
                    pos = new_src.find(lit_old, anchor) if anchor >= 0 else -1
                    if pos >= 0:
                        new_src = new_src[:pos] + lit_new + new_src[pos + len(lit_old) :]
        if new_src != src:
            n_mod += 1
            if apply:
                f.write_text(new_src, encoding="utf-8")
    print(f"species modules changed: {n_mod}")

    supp = ROOT / "api" / "data" / "supplementary_diseases.json"
    if supp.exists():
        sdata = json.loads(supp.read_text(encoding="utf-8"))
        ns = 0
        items = (
            sdata
            if isinstance(sdata, list)
            else [v for vs in sdata.values() for v in (vs if isinstance(vs, list) else [])]
        )
        for x in items:
            if not isinstance(x, dict):
                continue
            sp = JSON_SPECIES.get(x.get("species", ""), str(x.get("species", "")).lower().replace(" ", "_"))
            new = fix_text(x.get("treatment_ja") or "", sp, x.get("name", ""))
            if new != (x.get("treatment_ja") or ""):
                x["treatment_ja"] = new
                ns += 1
        print(f"supplementary fixed: {ns}")
        if apply and ns:
            supp.write_text(json.dumps(sdata, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    main("--apply" in sys.argv)
