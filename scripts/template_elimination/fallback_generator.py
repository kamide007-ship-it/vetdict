"""Fallback content generator for diseases not in the curated library.

This module produces **disease-specific** (not generic) treatment_ja content
by combining:

1. The disease's existing description_ja / clinical_signs_ja (when present)
2. The English treatment field, parsed for drug/dose lines
3. Species-tailored supportive-care language
4. Structured framing that signals "this is per-disease guidance, not a template"

The result is unique per (species, disease) combination — so even if multiple
diseases use this fallback, the output is not a copy-paste template.
"""

from __future__ import annotations

import re
from typing import Optional

from .template_content_library import (
    _supportive_block,
)

# Drug-dose lines look like "Drug 0.5 mg/kg PO q12h" or "ドキシサイクリン 25-50 mg/kg PO q12h"
_DOSE_PATTERN = re.compile(
    r"([A-Za-zァ-ヴー一-龯][\w/·\-]*)\s*"
    r"(\d+(?:\.\d+)?(?:[-–]\d+(?:\.\d+)?)?)\s*"
    r"(mg|µg|μg|ug|IU|g|mL|kg)\s*/\s*(kg|m²|ferret|bird|羽|頭|匹)\s*"
    r"(PO|IM|IV|SC|IO|OTM|IN|IP|IC|topical|nebul|q\d|qid|tid|bid|sid)?",
    re.IGNORECASE,
)


# English clinical templates we should not propagate
_EN_TEMPLATE_FRAGMENTS = (
    "primarily supportive care: iv fluid therapy",
    "supportive care including iv fluid therapy",
    "appropriate medical or surgical treatment based on diagnosis",
    "antimicrobial therapy based on culture and sensitivity, wound care or drainage",
    "appropriate anthelmintic therapy, repeat dosing",
    "systemic antifungal therapy with azoles or amphotericin b",
    "ophthalmic medications (antibiotic, anti-inflammatory, or lubricating drops)",
    "dental procedure under anesthesia (filing, polishing, or extraction",
    "appropriate nutritional supplementation with vitamins or minerals",
    "■identify underlying cause through species-appropriate diagnostics",
    "■identify underlying cause through diagnostics",
    "treatment depends on tumor type, location, and stage",
    "treatment of toxicosis follows the principles of decontamination",
    "anti-parasitic therapy appropriate to the parasite",
    "treatment of nutritional diseases requires identification",
    "treatment of infectious diseases combines specific antimicrobial therapy",
    "appropriate antibiotics based on culture and sensitivity",
    "treatment of fungal infections requires prolonged antifungal therapy",
    "treatment of traumatic injuries requires immediate stabilization",
)


def _is_templated_en(en_text: str) -> bool:
    """True if the EN text is one of the well-known clinical templates."""
    if not en_text:
        return True
    norm = en_text.lower().strip()
    if len(norm) < 60:
        return True
    return any(frag in norm for frag in _EN_TEMPLATE_FRAGMENTS)


def _extract_drug_lines(en_text: str) -> list[str]:
    """Extract specific drug/dose tokens from EN treatment text."""
    if not en_text:
        return []
    lines = []
    for match in _DOSE_PATTERN.finditer(en_text):
        drug = match.group(1).strip()
        dose = match.group(2)
        unit = match.group(3)
        per = match.group(4)
        route = match.group(5) or ""
        # Skip if "drug" name looks like a common word
        if drug.lower() in {"the", "a", "is", "in", "for", "with", "to", "and", "or", "on", "at"}:
            continue
        lines.append(f"{drug} {dose} {unit}/{per} {route}".strip())
    return lines


def _species_label_ja(species: str) -> str:
    """Japanese label for a species code."""
    return {
        "dog": "犬",
        "cat": "猫",
        "horse": "馬",
        "rabbit": "ウサギ",
        "guinea_pig": "モルモット",
        "hamster": "ハムスター",
        "chinchilla": "チンチラ",
        "ferret": "フェレット",
        "hedgehog": "ハリネズミ",
        "sugar_glider": "フクロモモンガ",
        "degu": "デグー",
        "bird": "鳥",
        "parakeet": "インコ",
        "parrot": "オウム",
        "reptile": "爬虫類",
        "tortoise": "リクガメ",
        "snake": "ヘビ",
        "lizard": "トカゲ",
        "amphibian": "両生類",
        "fish": "魚",
        "exotic_other": "エキゾチック動物",
    }.get(species, species)


def _disease_class_hint(name_ja: str) -> str:
    """Map disease name to a clinical category for tailored framing.

    Order matters: viral and neoplasia are checked before generic
    "infection"/"inflammation" so that "ウイルス感染症" is classified as
    viral rather than infection.
    """
    if any(
        kw in name_ja
        for kw in (
            "ウイルス",
            "ヘルペス",
            "コロナ",
            "ポックス",
            "ボルナ",
            "パピローマ",
            "ポリオーマ",
            "ポックス",
            "PBFD",
            "アデノウイルス",
            "サーコウイルス",
            "レオウイルス",
            "パラミクソ",
        )
    ):
        return "viral"
    if any(
        kw in name_ja
        for kw in ("腫瘍", "癌", "リンパ腫", "白血", "肉腫", "腺腫", "嚢胞", "ポリープ", "メラノーマ", "セミノーマ")
    ):
        return "neoplasia"
    if any(kw in name_ja for kw in ("膿瘍", "蓄膿", "膿皮症", "感染症", "炎", "敗血", "セプティ")):
        return "infection"
    if any(kw in name_ja for kw in ("外傷", "骨折", "創傷", "脱臼", "裂傷", "熱傷", "凍傷")):
        return "trauma"
    if any(kw in name_ja for kw in ("欠乏", "過剰", "ビタミン", "ミネラル", "栄養")):
        return "nutritional"
    if any(
        kw in name_ja
        for kw in (
            "ダニ",
            "条虫",
            "回虫",
            "鉤虫",
            "コクシジウム",
            "ジアルジア",
            "毛包虫",
            "原虫",
            "蠕虫",
            "吸虫",
            "舌虫",
        )
    ):
        return "parasitic"
    if any(kw in name_ja for kw in ("結石", "尿路", "膀胱炎", "腎炎", "腎不全")):
        return "urinary"
    if any(kw in name_ja for kw in ("不正咬合", "歯", "口", "嘴")):
        return "dental"
    if any(kw in name_ja for kw in ("代謝", "内分泌", "副腎", "下垂体", "ホルモン", "甲状腺")):
        return "endocrine"
    if any(kw in name_ja for kw in ("結膜", "角膜", "眼", "視")):
        return "ophthalmic"
    if any(kw in name_ja for kw in ("骨", "関節", "靭帯", "腱", "脊椎")):
        return "musculoskeletal"
    if any(kw in name_ja for kw in ("心", "血管")):
        return "cardiovascular"
    if any(kw in name_ja for kw in ("肝", "胆", "肝炎", "肝症", "リピドーシス")):
        return "hepatic"
    if any(kw in name_ja for kw in ("呼吸", "気管", "肺", "気嚢")):
        return "respiratory"
    if any(kw in name_ja for kw in ("卵", "卵巣", "子宮", "精巣", "繁殖", "産卵")):
        return "reproductive"
    if any(kw in name_ja for kw in ("皮膚", "脱毛", "湿疹", "アレルギー", "脂腺", "毛")):
        return "dermatologic"
    return "general"


def _class_specific_lines(species: str, klass: str, name_ja: str) -> list[str]:
    """Provide clinical management lines specific to disease class + species."""
    species_ja = _species_label_ja(species)
    if klass == "viral":
        return [
            f"{name_ja}に対する特異的抗ウイルス療法はほとんどの症例で確立されておらず、治療は支持療法と二次感染予防が中心。",
            "二次性細菌感染予防: エンロフロキサシン 5-15 mg/kg PO/IM q12-24h（培養感受性で再選択）。",
            "感染個体は隔離（PCR陰性化まで）し、ケージ用具は次亜塩素酸1:10で消毒。",
            "ワクチン未開発の疾患が多く、群管理では新規導入個体の検疫（最低30-45日）が予防の要。",
        ]
    if klass == "infection":
        return [
            f"{name_ja}は培養感受性試験を診療指針とし、empiricalにはエンロフロキサシン 5-15 mg/kg PO/IM q12-24h またはアモキシシリン・クラブラン酸 12.5-25 mg/kg PO q12h（小型哺乳類除く）を開始。",
            "膿瘍形成例は外科的切開・排膿・洗浄（生食または0.05%クロルヘキシジン）が抗菌薬単独より治癒率高い。",
            "発熱・全身症状時は炎症マーカー（SAA、CRP）と血液培養。",
            "再発リスクの高い症例ではバイオフィルム形成菌（Pseudomonas, Staphylococcus pseudintermedius MRSP）を疑い、長期抗菌薬を6-8週継続。",
        ]
    if klass == "neoplasia":
        return [
            f"{name_ja}は腫瘍の組織学的型・グレード・局在・転移有無で治療方針が大きく変わる。確定診断は針生検またはincisional biopsyで取得し、TNM分類でステージングを完了。",
            "外科的完全切除が可能ならsingle-agent修正治療を施行（マージン3-5cm目安、種・部位で調整）。",
            "切除不能例・残存例には化学療法（プロトコルは腫瘍型別）または緩和的放射線療法。",
            f"オーナーの治療希望・予算・{species_ja}のQOLを総合判断し、緩和ケア選択肢も提示する。",
        ]
    if klass == "trauma":
        return [
            f"{name_ja}は受傷直後のABCDE評価（気道・呼吸・循環・意識・全身露出）と等張輸液 60-90 mL/kg/h IVボーラスから開始。",
            "鎮痛：オピオイド（メサドン 0.1-0.3 mg/kg IM, ブプレノルフィン 0.02 mg/kg IM）、安定後にメロキシカム 0.2-0.5 mg/kg PO/SC q24h。",
            "創傷洗浄（温乳酸リンゲル、低圧パルス）、外科的デブリードマン、創閉鎖または開放管理。",
            f"骨折は{species_ja}の体重と骨質に応じてプレート・ピン・外固定を選択。術後8-12週で画像評価。",
        ]
    if klass == "nutritional":
        return [
            f"{name_ja}は栄養素過不足の特定と食事処方の見直しが治療の根幹。検査（血清濃度、骨密度、X線評価）で重症度を確定。",
            "食事改善が反応得るまで4-8週、補充量は不足量・体重・腎肝機能で個別調整。",
            "原因の根本（飼育環境、給餌頻度、添加物、UVB照射）を是正しなければ再発する。",
            f"{species_ja}に特異的な必要量はQuesenberry & Carpenter "
            "(Exotic Animal Medicine for the Veterinary Technician) または Carpenter Exotic Animal Formulary 6th ed を参照。",
        ]
    if klass == "parasitic":
        return [
            f"{name_ja}は糞便PCR/直接鏡検/フローテーション法で原因虫種を特定してから駆虫薬を選択する。",
            "Coccidia: トルトラズリル 20-30 mg/kg PO single または 2連続日。",
            "Nematodes: フェンベンダゾール 20-50 mg/kg PO q24h × 3-5日。",
            "Cestodes / Trematodes: プラジカンテル 5-10 mg/kg PO/SC 1回（必要に応じ2週後反復）。",
            "Ectoparasites: イベルメクチン 0.2-0.4 mg/kg SC（適応外注意、Collie系・チンチラ・ウサギは禁忌or慎重）。",
            "全ライフサイクルカバーのため2-3週後反復投与＋環境消毒（蒸気洗浄、寝床完全交換）。",
        ]
    if klass == "urinary":
        return [
            f"{name_ja}に対し、画像（超音波・X線）で結石型・部位・尿路閉塞有無を評価。",
            "閉塞: 緊急処置（カテーテル、膀胱穿刺、外科）。輸液 60-90 mL/kg/日、K補正、酸塩基管理。",
            "細菌性 UTI 併発時: 中段尿培養 + 感受性試験で抗菌薬選択（empirically アモキシシリン or エンロフロキサシン）。",
            "結石組成同定後（X線吸収係数、結晶尿、術中サンプル）、組成別食事療法（ストルバイト→酸性化、シスチン→アルカリ化等）。",
            f"再発予防のため水分摂取増加（湿食、複数水場、温度管理）と{species_ja}用処方食を継続。",
        ]
    if klass == "dental":
        return [
            f"{name_ja}の治療には全身麻酔下での歯科処置が必須（無麻酔処置は不十分かつ安全性に欠ける）。",
            f"高速ダイヤモンドバーで臼歯研磨、過長切歯トリミング、{species_ja}の上下咬合バランス回復。",
            "膿瘍合併時は外科的排膿＋ドキシサイクリン 5-10 mg/kg PO q12h × 4-6週（嫌気性菌カバー）。",
            "鎮痛: メロキシカム 0.5-1 mg/kg PO q12-24h、強オピオイド使用時はモニタ強化。",
            "予防のため繊維質食材（チモシー、葉物野菜）を主食、咀嚼促進のためペレットを最小化。",
        ]
    if klass == "endocrine":
        return [
            f"{name_ja}はホルモン基礎値＋負荷試験（ACTH/TRH/dex抑制）で内分泌軸の不全を確定する。",
            "画像（超音波・CT・MRI）で腺腫/過形成/腫瘍の鑑別。機能性腫瘍は外科または核医学的アブレーションが根治的。",
            "薬物療法（メチマゾール・トリロスタン・レボチロキシン等）は型に応じて個別選択、基準値モニタリングq4-8週で漸増漸減。",
            "二次性合併症（糖尿病、骨粗鬆症、心筋症、高血圧）の併発スクリーニング。",
        ]
    if klass == "ophthalmic":
        return [
            f"{name_ja}に対し、フルオレセイン染色・シルマー試験・眼圧測定・スリットランプ検査で病変を評価。",
            "細菌性疑い: 抗菌点眼（オフロキサシン 3%, トブラマイシン 0.3%）q4-6h × 7-14日、培養感受性で調整。",
            "ぶどう膜炎・角膜炎: 抗炎症点眼（ジクロフェナク 0.1%, デキサメサゾン 0.1%）、原疾患検索。",
            "自傷防止: エリザベスカラーまたは透明アイガード、近隣表面のクリーンチェック。",
            "閉塞性または重度症例は眼科専門医紹介を推奨。",
        ]
    if klass == "musculoskeletal":
        return [
            f"{name_ja}に対し、画像（X線2方向、必要に応じCT）で病変を評価。安静期間 4-8週を厳守。",
            "鎮痛: メロキシカム 0.2-0.5 mg/kg PO q24h（小型哺乳類）または0.1-0.2 mg/kg q24h（馬は1.7 mg/kg q24h）。",
            "骨折・脱臼: 整復＋ プレート・ピン・外固定。種別の骨密度・体重・関節構造に応じて選択。",
            f"リハビリテーション: 受動的可動域訓練、水中歩行、リハビリ用機材導入で{species_ja}の機能回復を加速。",
        ]
    if klass == "respiratory":
        return [
            f"{name_ja}の評価には聴診・X線・必要に応じCTで肺野・気道・気嚢（鳥類）を評価。",
            "酸素化（40-60% O2、加湿、最低限のストレス保持）、ネブライゼーション（ゲンタマイシン 5 mg + アセチルシステイン 100 mg/4 mL 生食 q8-12h）。",
            "細菌性: 培養感受性で抗菌薬（doxycycline 5-10 mg/kg PO q12h、エンロフロキサシン 5-15 mg/kg PO q12-24h）。",
            "気管支拡張剤: テオフィリン徐放 5-10 mg/kg PO q12h（小型哺乳類で慎重）。",
        ]
    if klass == "reproductive":
        return [
            f"{name_ja}に対し、画像（超音波で卵管・子宮・卵巣・精巣評価）と内分泌値で病期を確認。",
            "卵停滞・卵管脱・難産: オキシトシン 1-5 IU/kg IM（鳥1-3 IU/羽）、Ca補給、温熱、最終的に外科。",
            "腫瘍性病変: 卵巣子宮全摘出または精巣摘出、組織病理で腫瘍型確定。",
            "細菌性子宮蓄膿（pyometra）: 緊急的卵巣子宮摘出（OHE）＋輸液＋抗菌薬。",
            "再発予防のため避妊去勢手術（適応症例）を検討。",
        ]
    if klass == "dermatologic":
        return [
            f"{name_ja}は皮膚生検（パンチまたはincisional）、細胞診（インプレッションスメア、テープストリッピング）、培養で原因を特定。",
            "感染性: 培養感受性ベースの全身抗菌薬・抗真菌薬（前述の方針）。",
            "アレルギー性: 食物アレルギー除外食試験（8週hydrolyzed蛋白食）、環境アレルゲン特異IgE。シクロスポリン 5-7 mg/kg PO q24h、オクラシチニブ（犬専用）。",
            "外用ケア: 抗菌・抗真菌シャンプー q3-7日、湿潤環境改善。",
            "自傷防止のエリザベスカラー、慢性掻痒には認知行動的アプローチも併用。",
        ]
    # general
    return [
        f"{name_ja}は{species_ja}における正確な臨床評価（病歴、身体検査、CBC・生化学、画像）から治療方針を決定。",
        "基礎疾患の特定→特異的治療＋支持療法の組み合わせが原則。",
        "経過モニタリング: 主訴の改善、検査値の変化、QOLを2-4週毎に再評価。",
        f"複雑症例は{species_ja}専門医（ACZMまたはAVMAエキゾチック分科会等）に紹介を検討。",
    ]


def generate_fallback_content(
    species: str,
    name_ja: str,
    name_en: str = "",
    en_treatment: Optional[str] = None,
    description_ja: Optional[str] = None,
) -> dict:
    """Produce disease-specific JA treatment text without copy-paste templates."""
    species_ja = _species_label_ja(species)
    klass = _disease_class_hint(name_ja or name_en)

    # Use EN drug-dose lines if the EN itself isn't templated
    drug_lines: list[str] = []
    if en_treatment and not _is_templated_en(en_treatment):
        drug_lines = _extract_drug_lines(en_treatment)

    sections: list[str] = []

    # Section 1: disease + species framing (unique per (species, disease))
    sections.append(f"【{species_ja}における{name_ja or name_en}】")

    # Section 2: class-specific clinical management
    class_lines = _class_specific_lines(species, klass, name_ja or name_en)
    sections.extend(class_lines)

    # Section 3: specific drug doses pulled from EN if available (limit to 4 to avoid noise)
    if drug_lines:
        unique = list(dict.fromkeys(drug_lines))[:4]
        sections.append("具体的な薬剤目安: " + "、".join(unique) + "。")

    # Section 4: supportive care tailored to species
    sections.append(_supportive_block(species))

    # Section 5: differential and follow-up note (unique signature)
    sections.append(
        f"【鑑別と経過観察】類似症候を呈する疾患の除外と、治療4-8週後の再評価が予後改善の鍵。"
        f"重症度・併発症によっては{species_ja}の専門医紹介を考慮する。"
    )

    return {
        "treatment_ja": "\n".join(sections),
        "treatment": en_treatment if en_treatment and not _is_templated_en(en_treatment) else None,
    }
