"""drug_batch_30.py — D2拮抗系の催乳（galactagogue）作用の収載

獣医師の指摘により追加:
  1. スルピリド（ドグマチール）が未収載だった。
  2. メトクロプラミド（プリンペラン）の催乳作用が機序・適応から欠落していた
     （消化管運動促進・制吐しか書かれていなかった）。

いずれもドパミンD2拮抗 → 下垂体前葉からのプロラクチン分泌を脱抑制、という同一機序。
ドンペリドンは既に lactation_support として収載済みで、本バッチはその同系統を揃えるもの。

**ヒト用量は載せない。** スルピリドはヒトでは胃潰瘍・うつ・統合失調症に 150〜1,200 mg/日
で使われるが、これは動物の用量ではない。ヒト用量を獣医DBに転記することは、本プロジェクトが
当初から排除してきた「ヒト医学の移植」そのもの（デグーの糖尿病性足潰瘍・網膜症と同種の誤り）。
ここに載せる用量はすべて当該動物種の一次文献から引いており、出典を notes に明記する。

**種カバレッジについて。** スルピリドの獣医領域のエビデンスは事実上ウマ（季節性無発情の
シクリシティ誘起・プロラクチン放出）に限られる。PubMed を全21種で横断検索したところ、
ウマ以外のヒットは受容体薬理・網膜・行動薬理などの基礎研究のみで、臨床用量は存在しない
（ハリネズミの1件は動物ではなく Sonic Hedgehog 遺伝子のヒットだった）。
したがって非ウマ種は「確立されていない」と正直に記載する。これが当該種における
エビデンスに基づいた記載であり、外挿用量をでっち上げないための線引き。
"""

# 未確立の種に入れる共通文言（用量を書かない＝✗表示のまま notes を読ませる）
_NOT_ESTABLISHED = {
    "dose": "Not established in this species 本種では確立されていない",
    "notes": (
        "No veterinary clinical dosing published for this species. PubMed hits are receptor-pharmacology "
        "or basic-science studies, not dosing evidence. Do not extrapolate from human psychiatric dosing."
    ),
    "notes_ja": (
        "本種の獣医臨床用量は報告されていない。PubMed のヒットは受容体薬理・基礎研究であり用量の根拠にならない。"
        "ヒトの精神科用量からの外挿は行わないこと。"
    ),
}


def _not_established(*species: str) -> dict[str, dict]:
    return {sp: dict(_NOT_ESTABLISHED) for sp in species}


DRUGS_BATCH_30: list[dict] = [
    {
        "id": "sulpiride",
        "name": "Sulpiride",
        "name_ja": "スルピリド（ドグマチール）",
        "category": "lactation_support",
        "mechanism": (
            "Benzamide dopamine D2 receptor antagonist. Blocking D2 receptors on pituitary lactotrophs "
            "removes dopaminergic inhibition of prolactin secretion, raising serum prolactin. In the mare "
            "this is used to advance cyclicity in seasonal anoestrus and to support lactation."
        ),
        "mechanism_ja": (
            "ベンザミド系ドパミンD2受容体拮抗薬。下垂体ラクトトロープのD2受容体を遮断してプロラクチン分泌への"
            "ドパミン性抑制を解除し、血中プロラクチンを上昇させる。ウマでは季節性無発情のシクリシティ誘起および"
            "泌乳サポートに用いる。ヒトでは用量により胃薬・抗うつ・抗精神病薬として使われるが、"
            "それらのヒト用量は動物には適用しない。"
        ),
        "side_effects": "Extrapyramidal signs at high dose, sedation, behavioural change",
        "side_effects_ja": "高用量で錐体外路症状、鎮静、行動変化",
        "contraindications": (
            "Prolactinoma or other prolactin-dependent conditions; use with care alongside other D2 antagonists "
            "(metoclopramide, domperidone) — additive prolactin and extrapyramidal effects."
        ),
        "contraindications_ja": (
            "プロラクチン依存性病態。他のD2拮抗薬（メトクロプラミド、ドンペリドン）との併用は"
            "プロラクチン上昇・錐体外路症状が相加するため注意。"
        ),
        "drug_interactions": [
            {
                "drug": "Domperidone",
                "effect": "Both are D2 antagonists; additive hyperprolactinaemia",
                "severity": "moderate",
            },
            {
                "drug": "Metoclopramide",
                "effect": "Both are D2 antagonists; additive hyperprolactinaemia and extrapyramidal risk",
                "severity": "moderate",
            },
            {
                "drug": "Cabergoline",
                "effect": "Directly opposing action (D2 agonist suppresses prolactin) — do not combine",
                "severity": "major",
            },
        ],
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "1 mg/kg IM q24h (anovulatory mares); alternatively 200 mg/mare IM q24h until first ovulation",
                "dosage_ja": "1 mg/kg 筋注 24時間毎（無排卵牝馬）; または 200 mg/頭 筋注 24時間毎（初回排卵まで）",
                "notes": (
                    "Advances cyclicity in seasonally anoestrous mares; also raises prolactin (0.6 mg/kg produced "
                    "significant prolactin release in stallions). Sources: Theriogenology 2002;57(2):963-976 "
                    "(1 mg/kg IM daily); Theriogenology 1997;47(2):467-480 (200 mg/mare IM daily); "
                    "Reprod Domest Anim 2002;37(6):335-340, PMID 12464071 (0.6 mg/kg, prolactin release). "
                    "Response is seasonal — prolactin release is most pronounced in mid-winter."
                ),
                "notes_ja": (
                    "季節性無排卵牝馬のシクリシティを前進させる。プロラクチン上昇作用もあり（種牡馬で0.6 mg/kgが"
                    "有意なプロラクチン放出を誘導）。出典: Theriogenology 2002;57(2):963-976（1 mg/kg IM 連日）、"
                    "Theriogenology 1997;47(2):467-480（200 mg/頭 IM 連日）、"
                    "Reprod Domest Anim 2002;37(6):335-340, PMID 12464071（0.6 mg/kg・プロラクチン放出）。"
                    "反応には季節性があり、プロラクチン放出は冬季に最も顕著。"
                ),
                "evidence_grade": "A",
            },
            # 以下は「エビデンスが無い」ことがエビデンスに基づく回答。用量は書かない。
            **_not_established(
                "dog",
                "cat",
                "rabbit",
                "ferret",
                "hamster",
                "guinea_pig",
                "chinchilla",
                "degu",
                "hedgehog",
                "sugar_glider",
                "bird",
                "parakeet",
                "parrot",
                "reptile",
                "snake",
                "lizard",
                "tortoise",
                "amphibian",
                "fish",
                "exotic_other",
            ),
        },
    },
]

# メトクロプラミドの催乳作用（既存エントリに不足していた分を補う）
METOCLOPRAMIDE_LACTATION_PATCH_30: dict[str, dict] = {
    "metoclopramide": {
        "mechanism_ja": (
            "ドパミンD2拮抗薬。消化管運動促進・制吐作用に加え、下垂体D2遮断によりプロラクチン分泌を"
            "亢進させる（催乳作用）。犬の乳汁分泌不全への補助に用いられる。"
        ),
        "mechanism": (
            "Dopamine D2 antagonist. Prokinetic and antiemetic; additionally raises prolactin via pituitary D2 "
            "blockade (galactagogue effect), used as an adjunct for insufficient milk production in the bitch."
        ),
    }
}

# 犬の催乳用法（一次文献）— 既存の消化管用量は上書きせず notes に併記する形で補完
METOCLOPRAMIDE_DOG_LACTATION_NOTE = (
    "催乳（乳汁分泌不全）用法: 0.2 mg/kg 経口 6時間毎×6日間、分娩10-24時間後から開始"
    "（Am J Vet Res 2018;79(2):233-239, PMID 29359978）。血清プロラクチンの一過性上昇と乳汁乳糖の増加を認めたが、"
    "⚠️同試験では子犬の体重増加に有意差は出ていない。乳汁分泌不全例での有用性は示唆どまり。"
)
METOCLOPRAMIDE_DOG_LACTATION_NOTE_EN = (
    "Galactagogue use: 0.2 mg/kg PO q6h for 6 days starting 10-24 h after whelping "
    "(Am J Vet Res 2018;79(2):233-239, PMID 29359978). Raised serum prolactin transiently and increased milk "
    "lactose, but note puppy weight gain was NOT significantly affected in that study — benefit in true "
    "agalactia is suggested, not demonstrated."
)
