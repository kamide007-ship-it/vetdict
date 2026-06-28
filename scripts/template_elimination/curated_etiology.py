"""Curated causes_ja / pathophysiology_ja for diseases that resist single-category
templating.

Some diseases are multifactorial and do not map cleanly onto any one of the
``NAME_CATEGORY_PATTERNS`` buckets, so the category-recategorisation pass can only
swap one imperfect template for another. Equine **laminitis** (predominantly
endocrinopathic/inflammatory/mechanical, not orthopaedic) and **hepatic fibrosis**
(the fibrotic end-stage of chronic liver injury, with no dedicated hepatic
etiology bucket) are the two flagged in the previous session.

Rather than force them into a marginal category, this module supplies concise,
textbook-accurate, disease-specific etiology and pathophysiology. The text encodes
established veterinary knowledge (not per-record generation), so it carries no
fabrication risk; it is applied ONLY to fields that are currently a recognised
category template or vague stub, so genuinely curated content (e.g. the existing
disease-specific laminitis pathophysiology) is never overwritten.

References: Belknap & Geor, *Equine Laminitis* (2017); AAEP/ECEIM laminitis
consensus; Stashak, *Adams' Lameness in Horses* 6th ed; Carpenter, *Exotic Animal
Formulary* 6th ed; Harrison & Lightfoot, *Clinical Avian Medicine* (hepatic
disease); Cullen & Stalker, *Jubb, Kennedy & Palmer's Pathology of Domestic
Animals* (liver).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.clinical_fields_generator import SPECIES_JA  # noqa: E402

# A field is replaceable (safe to overwrite with curated text) when it is empty,
# carries a category template (detected by the caller via fingerprint), or is one
# of these vague generic stubs.
STUB_SIGNATURES: tuple[str, ...] = (
    "正確な病因は症例により異なる",
    "病因は症例により異なる",
)


def _laminitis_causes(species_ja: str) -> str:
    return (
        f"{species_ja}における蹄葉炎の原因は多くが全身性で、現在は内分泌性が最多とされる。"
        "(1) 内分泌性（インスリン調節異常）: 馬代謝症候群（EMS）や下垂体中葉機能不全（PPID/クッシング）に伴う"
        "高インスリン血症が葉層を傷害する（最も一般的）。"
        "(2) 炎症性・敗血症性（SIRS）: 穀物過食（炭水化物過負荷）、大腸炎、子宮内膜炎・胎盤停滞、"
        "重度感染症などの全身性炎症。"
        "(3) 過重負重性（supporting-limb）: 対側肢の重度疼痛・非負重による患肢への持続的荷重。"
        "(4) その他: 硬地での過度な運動（road founder）、コルチコステロイド誘発。"
        "肥満・過肥、ポニーや特定品種、過去の蹄葉炎既往が主要なリスク因子である。"
    )


def _laminitis_patho(species_ja: str) -> str:
    return (
        f"{species_ja}の蹄葉炎は、蹄骨と蹄壁をつなぐ葉状層（葉層）の機能不全により蹄骨の回転・沈下が生じる病態である。"
        "発症機序は原因により異なる: 内分泌性では高インスリン血症がIGF-1受容体等を介して葉層上皮を伸長・脆弱化させる。"
        "敗血症・炎症性では循環中のサイトカイン・エンドトキシンが葉層の微小循環障害（血管収縮・血栓・虚血再灌流）と"
        "基質メタロプロテアーゼ（MMP-2/9）の活性化を引き起こし、基底膜の酵素的分解を招く。"
        "過重負重性では持続的な機械的ストレスと灌流低下が関与する。"
        "葉層結合の破綻により蹄骨が深指屈腱の牽引と体重で回転・沈下し、重症例では蹄底穿孔に至る。"
        "急性期は強い疼痛と拍動性の指動脈拍動、慢性期は蹄輪の乖離（founder lines）・白帯の開大・蹄骨変位を呈する。"
    )


def _hepatic_fibrosis_causes(species_ja: str) -> str:
    return (
        f"{species_ja}における肝線維症は、慢性的な肝傷害が持続した結果として肝実質が線維性結合組織へ置換される終末像であり、"
        "原因は基礎となる慢性肝疾患に依存する。"
        "慢性胆管肝炎・胆管閉塞（胆汁うっ滞）、栄養性（肝リピドーシス関連、ビタミン・ミネラル不均衡、肥満や高脂肪の種子食）、"
        "毒性（アフラトキシン等のカビ毒、重金属、薬剤性、植物毒）、感染性（細菌・ウイルス・寄生虫による慢性肝炎）、"
        "鉄過剰症（一部の鳥類・果実食種でのヘモクロマトーシス）、慢性うっ血（右心不全）が主な誘因である。"
        "多くは長期にわたる不適切な飼育・栄養管理を背景とする。"
    )


def _hepatic_fibrosis_patho(species_ja: str) -> str:
    return (
        f"{species_ja}の肝線維症は、持続的な肝細胞傷害に対する創傷治癒反応の結果として進行する。"
        "傷害により活性化された肝星細胞（伊東細胞）が筋線維芽細胞へ形質転換し、"
        "I型・III型コラーゲンなどの細胞外基質を過剰に産生・沈着させる。"
        "基質の産生と分解の均衡が崩れることで類洞周囲から門脈域に線維性隔壁が形成され、肝小葉構造が改変される。"
        "進行すると肝内血流抵抗の上昇（門脈圧亢進）と肝細胞機能の低下（低アルブミン血症・凝固異常・胆汁うっ滞・高アンモニア血症）を招き、"
        "不可逆的な肝硬変・肝不全へ至る。早期は無症状だが、食欲不振・体重減少・黄疸・腹水・出血傾向として顕在化する。"
    )


# ---------------------------------------------------------------------------
# Flagship dog / cat diseases — the most common, most-searched conditions.
# Each pair of strings is textbook etiology + mechanism (Ettinger & Feldman,
# *Textbook of Veterinary Internal Medicine* 8th ed; Nelson & Couto, *Small
# Animal Internal Medicine* 6th ed; ACVIM consensus statements). The species is
# fixed per entry, so the species name is written directly into the text.
# ---------------------------------------------------------------------------


def _f(causes: str, patho: str):
    """Build a (species_ja-ignoring) field-generator dict for fixed JA text."""
    return {"causes_ja": lambda _sp, _c=causes: _c, "pathophysiology_ja": lambda _sp, _p=patho: _p}


_GDV = _f(
    "胃拡張胃捻転症候群（GDV）の最大の要因は大型・胸深長犬種（グレート・デーン、セッター、ワイマラナー、"
    "スタンダードプードル、ジャーマン・シェパード等）の解剖学的素因である。リスク因子として一度の大量給餌・"
    "早食い・高い位置からの給餌、食後すぐの運動、ストレス、加齢、痩せ型体型、不安気質、第一度近親のGDV既往が挙げられる。"
    "胃を固定する靭帯の弛緩や胃排出遅延が捻転を許容する。",
    "胃内にガス・液体・食物が貯留して拡張し、胃が間膜軸を中心に捻転（多くは時計回りに200-360°）する。"
    "噴門と幽門が閉塞してガスが逃げられず胃壁が急速に膨満し、胃壁静脈還流障害から胃壁の虚血・壊死を生じる。"
    "膨満胃が門脈・後大静脈を圧迫して静脈還流が低下し、心拍出量減少による閉塞性ショックに陥る。"
    "脾臓のうっ血・捻転を伴い、エンドトキシン血症・再灌流障害・心室性不整脈・DICへ進展する致死的緊急疾患である。",
)

_PANCREATITIS_DOG = _f(
    "犬の膵炎の多くは特発性だが、高脂肪食の暴食や脂肪分の多い人の食事、高脂血症（ミニチュア・シュナウザー）、"
    "肥満、内分泌疾患（クッシング症候群・糖尿病・甲状腺機能低下症）、薬剤（臭化カリウム、フェノバルビタール、"
    "L-アスパラギナーゼ、アザチオプリン）、胆管・膵管閉塞、腹部外傷・手術、膵虚血が誘因となる。"
    "中高齢・雌・特定犬種（ミニチュア・シュナウザー、テリア種）に好発する。",
    "何らかの傷害により膵腺房細胞内で消化酵素（トリプシノーゲン）が早期活性化し、膵の自己消化が始まる。"
    "活性化トリプシンがホスホリパーゼ・エラスターゼ等を連鎖的に活性化し、膵実質の浮腫・出血・壊死と周囲脂肪壊死を生じる。"
    "炎症性サイトカインの全身放出によりSIRS・急性腎障害・急性肺傷害・DIC・多臓器不全へ進展しうる。"
    "慢性化すると線維化と腺房・膵島の脱落により外分泌不全（EPI）や糖尿病を併発する。",
)

_HYPOTHYROID_DOG = _f(
    "犬の甲状腺機能低下症は90%以上が後天性原発性で、リンパ球性甲状腺炎（自己免疫性、遺伝的素因）と"
    "特発性甲状腺萎縮が二大原因である。まれに甲状腺腫瘍による破壊、医原性、先天性（クレチン症）、"
    "下垂体性（二次性）がある。中高齢の中〜大型犬（ゴールデン・レトリーバー、ドーベルマン、ダックスフント等）に好発する。",
    "甲状腺濾胞の進行性破壊により甲状腺ホルモン（T4・T3）産生が低下する。"
    "ホルモン欠乏は全身の基礎代謝を低下させ、エネルギー産生・タンパク合成・体温調節を抑制する。"
    "粘液多糖類の皮膚沈着（粘液水腫）、脂質代謝異常（高コレステロール血症・動脈硬化）、徐脈、神経伝導遅延、"
    "生殖機能低下を生じる。原発性ではネガティブフィードバックの解除によりTSHが上昇する。",
)

_CUSHING_DOG = _f(
    "犬のクッシング症候群（副腎皮質機能亢進症）の自然発生例は、80-85%が下垂体性（PDH：ACTH産生下垂体腺腫による"
    "両側副腎過形成）、15-20%が副腎腫瘍（機能性腺腫・腺癌）である。残りは医原性（長期グルココルチコイド投与）。"
    "中高齢の小型犬（プードル、ダックスフント、各種テリア）に好発する。",
    "慢性的なコルチゾール過剰が全身に作用する。糖新生亢進とインスリン拮抗（高血糖・糖尿病誘発）、タンパク異化"
    "（筋萎縮・腹部膨満）、脂肪再分布、コラーゲン分解（皮膚菲薄・石灰沈着症）、免疫抑制（易感染性）、"
    "多飲多尿、全身性高血圧、肺血栓塞栓症リスク上昇を生じる。下垂体性では巨大腺腫が神経症状を起こすことがある。",
)

_CKD_DOG = _f(
    "犬の慢性腎臓病（CKD）は加齢性・特発性の尿細管間質性腎炎や糸球体腎症が多い。"
    "原因として慢性腎盂腎炎、免疫複合体性糸球体腎炎、アミロイドーシス、遺伝性腎症（シーズー、"
    "ソフトコーテッド・ウィートン・テリア等）、腎毒性物質、レプトスピラ感染後、尿路閉塞後、"
    "先天性腎異形成（若齢例）がある。高齢犬で有病率が高い。",
    "ネフロンの不可逆的・進行性の喪失により、残存ネフロンが代償性に過剰濾過・肥大するが、"
    "これが糸球体高血圧と硬化を招きさらにネフロンを失う悪循環となる。"
    "GFR低下により尿毒素（BUN・クレアチニン・SDMA）が蓄積し、濃縮能低下で多尿・代償性多飲、"
    "エリスロポエチン低下で非再生性貧血、リン貯留とカルシトリオール低下で腎性二次性副甲状腺機能亢進症、"
    "代謝性アシドーシス、全身性高血圧を生じる。IRISステージに沿って進行する。",
)

_CAD_DOG = _f(
    "犬アトピー性皮膚炎（CAD）は遺伝的素因を背景に、環境アレルゲン（ハウスダストマイト、花粉、カビ等）への"
    "経皮感作で発症するアレルギー性皮膚疾患である。好発犬種（柴犬、フレンチ・ブルドッグ、ウエスト・ハイランド・"
    "ホワイト・テリア、ゴールデン／ラブラドール・レトリーバー等）があり、皮膚バリア機能（フィラグリン・セラミド）の"
    "低下、食物アレルギーの併発、季節・環境要因が関与する。多くは3歳齢までに発症する。",
    "皮膚バリア機能の低下によりアレルゲンが経皮侵入し、ランゲルハンス細胞を介してTh2優位の免疫応答が誘導される。"
    "IL-4・IL-13・IL-31などのサイトカイン、IgE産生、肥満細胞の脱顆粒により掻痒と炎症が生じる。"
    "掻破による自己傷害とバリア破壊、二次的なブドウ球菌・マラセチアの過剰増殖が炎症を増悪させる悪循環を形成する。"
    "IL-31は掻痒シグナル伝達の中心的メディエーターである。",
)

_OA_DOG = _f(
    "犬の変形性関節症は原発性（加齢性）と続発性に分かれ、続発性の原因として股関節・肘関節形成不全、"
    "前十字靭帯断裂、膝蓋骨脱臼、離断性骨軟骨症（OCD）、関節内骨折・外傷、肥満、過度の運動が挙げられる。"
    "大型犬・肥満・高齢でリスクが上昇する。",
    "関節軟骨の摩耗・変性が中心病態である。軟骨細胞の代謝異常とプロテオグリカン・II型コラーゲンの分解"
    "（MMP・アグリカナーゼ）により軟骨基質が崩壊し、軟骨下骨の硬化、骨棘（osteophyte）形成、滑膜炎、"
    "関節包の線維化が進行する。炎症性メディエーター（IL-1・TNF-α・PGE2）が疼痛と軟骨破壊を増幅し、"
    "慢性疼痛と可動域制限の悪循環をきたす。",
)

_IVDD_DOG = _f(
    "犬の椎間板ヘルニア（IVDD）は、軟骨異栄養性犬種（ダックスフント、ビーグル、ウェルシュ・コーギー、"
    "シー・ズー等）での髄核の早期軟骨化生・石灰化による急性逸脱（Hansen I型）と、非軟骨異栄養性犬種での"
    "線維輪の慢性変性・膨隆（Hansen II型）に大別される。肥満、跳躍・階段昇降などの機械的負荷、加齢が誘因となる。",
    "変性した椎間板髄核（I型）が線維輪を破って脊柱管内へ急性に逸脱、または線維輪（II型）が慢性的に膨隆して"
    "脊髄を圧迫する。圧迫による直接的機械的損傷に加え、血管損傷・虚血、浮腫、グルタミン酸興奮毒性・"
    "フリーラジカルによる二次的脊髄損傷が進行する。重症度はグレードで分類され、深部痛覚消失例は予後不良で、"
    "急性重度例では進行性脊髄軟化症のリスクがある。",
)

_EPILEPSY_DOG = _f(
    "犬の特発性てんかんは、構造的脳病変や代謝異常を伴わない反復性発作で、遺伝性・素因性が背景にある"
    "（ボーダー・コリー、ラブラドール・レトリーバー、ベルジアン・シェパード等）除外診断である。"
    "多くは生後6か月〜6歳で初発し、睡眠不足・ストレス・ホルモン変動などが発作の誘因となりうる。",
    "大脳神経細胞の過剰な同期性放電により発作が生じる。興奮性（グルタミン酸）と抑制性（GABA）神経伝達の"
    "バランス破綻やイオンチャネル機能異常が発作閾値を低下させる。反復する発作はキンドリング現象により"
    "発作を起こしやすい神経回路を強化する。てんかん重積（status epilepticus）は神経細胞傷害・高体温・"
    "脳浮腫を招く緊急事態である。",
)

_DCM_DOG = _f(
    "犬の拡張型心筋症（DCM）は主に遺伝性で、大型犬種（ドーベルマン、グレート・デーン、ボクサー、"
    "アイリッシュ・ウルフハウンド等）に好発する。タウリン／カルニチン欠乏（アメリカン・コッカー・スパニエルや"
    "一部のグレインフリー食関連が報告）、感染後、中毒性（ドキソルビシン）も原因となる。中〜高齢の大型犬に多い。",
    "心筋収縮力の進行性低下により左室（しばしば両室）が拡張・菲薄化する。心拍出量低下に対する神経体液性代償"
    "（RAAS・交感神経の活性化）が容量負荷と心筋リモデリングをかえって悪化させる。進行すると左心不全（肺水腫）・"
    "両心不全（腹水・胸水）、心房細動や心室性不整脈による失神・突然死を生じる。"
    "ドーベルマン・ボクサーでは不整脈死が多く、無症状の潜在期（オカルト期）が長い。",
)

_MMVD_DOG = _f(
    "犬の粘液腫様僧帽弁変性症（MMVD）は犬で最も多い後天性心疾患で、加齢性の弁の粘液腫様変性による。"
    "小型〜中型犬（キャバリア・キング・チャールズ・スパニエル、マルチーズ、ダックスフント、チワワ等）に好発し、"
    "キャバリアでは若齢発症の強い遺伝的素因がある。雄でやや多い。",
    "僧帽弁尖と腱索のグリコサミノグリカン蓄積・コラーゲン変性により弁が肥厚・逸脱し、閉鎖不全（逆流）を生じる。"
    "左房への逆流が左房容量負荷・拡大を招き、進行すると左房圧上昇から肺静脈うっ血・肺水腫（左心不全）に至る。"
    "代償性の神経体液性活性化（RAAS）が容量負荷を悪化させる。腱索断裂は急性増悪を、重度左房拡大は心房細動を起こす。",
)

# Cat
_HCM_CAT = _f(
    "猫の肥大型心筋症（HCM）は猫で最も多い心疾患で、多くは遺伝性である（メインクーン・ラグドールで"
    "MYBPC3遺伝子変異が同定され、雑種猫にも多い）。診断には続発性肥大の原因（甲状腺機能亢進症・"
    "全身性高血圧・先端巨大症）の除外が必要である。中年の雄に好発する。",
    "左室心筋の求心性肥大により心室内腔が狭小化し、硬くなった心室の拡張機能障害（充満障害）が主病態となる。"
    "左房圧上昇から左房拡大、うっ血性心不全（肺水腫・胸水）に至る。左房内の血流うっ滞は血栓形成を促し、"
    "動脈血栓塞栓症（ATE：サドル血栓）の重大なリスクとなる。心筋虚血・線維化、流出路狭窄（SAM/閉塞性HCM）、"
    "致死性不整脈による突然死もみられる。",
)

_PANCREATITIS_CAT = _f(
    "猫の膵炎の多くは特発性で、犬より慢性型が多い。胆管炎・炎症性腸疾患との併発（三臓器炎 triaditis）、"
    "トキソプラズマ症、猫伝染性腹膜炎（FIP）、腹部外傷、胆管閉塞が関与しうる。"
    "犬のような明確な高脂肪食の誘因は乏しい。",
    "腺房細胞内での消化酵素の早期活性化により膵の自己消化が起こり、炎症・浮腫・壊死を生じる。"
    "猫では胆管と膵管が十二指腸に共通開口するため、胆道・腸管病変と相互に波及して triaditis を形成しやすい。"
    "慢性炎症は線維化と腺房脱落を招き、外分泌不全・糖尿病を併発する。"
    "重症例ではSIRS・脂肪織炎・低カルシウム血症を伴う。",
)

_IBD_CAT = _f(
    "猫の炎症性腸疾患（IBD）は単一原因がなく、遺伝的素因・腸内細菌叢の異常（dysbiosis）・食物抗原・"
    "粘膜免疫の調節異常の相互作用による慢性特発性腸炎症である。最も多いのはリンパ球形質細胞性腸炎で、"
    "食物アレルギーや低悪性度消化器型リンパ腫との連続性が議論される。中〜高齢猫に多い。",
    "腸管粘膜のバリア機能と免疫寛容の破綻により、管腔内抗原（食事・細菌）に対する持続的な炎症細胞浸潤"
    "（リンパ球・形質細胞・好酸球）が生じる。慢性炎症は絨毛萎縮・粘膜肥厚・吸収不良を招き、慢性嘔吐・下痢・"
    "体重減少・低アルブミン血症をきたす。猫では胆管炎・膵炎を伴う triaditis が多く、"
    "低悪性度リンパ腫への移行が臨床上問題となる。",
)

_ASTHMA_CAT = _f(
    "猫喘息は、吸入アレルゲン（ハウスダスト、花粉、タバコ煙、猫砂の粉塵、芳香スプレー等）に対する"
    "I型過敏症（アレルギー性気道炎症）である。シャム猫での好発が報告され、若〜中年猫に多い。",
    "アレルゲン感作によりTh2優位の好酸球性気道炎症が生じ、気道平滑筋の攣縮、気道壁の浮腫・炎症、"
    "過剰な粘液分泌により可逆性の気道狭窄を起こす。慢性化すると気道リモデリング（平滑筋肥厚・線維化・"
    "気管支拡張症）が進行する。急性増悪では呼気性努力呼吸・開口呼吸を伴う重度の呼吸困難をきたし、"
    "致死的となりうる。",
)

_CKD_CAT = _f(
    "猫の慢性腎臓病（CKD）は高齢猫で最も一般的な疾患の一つで、多くは特発性の慢性尿細管間質性腎炎である。"
    "原因・増悪因子として加齢、慢性腎盂腎炎、糸球体腎炎、多発性嚢胞腎（PKD：ペルシャ系の常染色体優性遺伝）、"
    "腎リンパ腫、尿路閉塞後、腎毒性物質（ユリ・アミノグリコシド・NSAID）、全身性高血圧、慢性脱水がある。",
    "ネフロンの不可逆的・進行性の喪失により残存ネフロンが代償性に過剰濾過を行うが、糸球体高血圧と"
    "尿細管間質の線維化が進行しさらにネフロンを失う。GFR低下で尿毒素（BUN・クレアチニン・SDMA）が蓄積し、"
    "濃縮能低下で多尿・多飲、エリスロポエチン低下で貧血、リン貯留とカルシトリオール低下で"
    "腎性二次性副甲状腺機能亢進症、代謝性アシドーシス、全身性高血圧、低カリウム血症を生じる。"
    "IRISステージで重症度を評価する。",
)

_FCGS_CAT = _f(
    "猫慢性歯肉口内炎（FCGS）の病因は多因子・免疫介在性で、歯垢（プラーク）細菌抗原への過剰な口腔粘膜"
    "免疫応答が中心である。猫カリシウイルス（FCV）の関与が強く示唆され、FIV／FeLV、Bartonella、"
    "慢性歯周病が増悪因子となる。明確な単一原因はない。",
    "歯垢バイオフィルム抗原に対する過剰な免疫・炎症応答により、口腔粘膜（特に臼歯後部・口峡部）に"
    "リンパ球形質細胞性の重度炎症・潰瘍・増殖性病変を生じる。慢性の疼痛により摂食困難・流涎・体重減少をきたす。"
    "多くは内科治療抵抗性で、病態の主因である歯垢付着面を除去する抜歯（臼歯または全顎）の奏効率が高い。",
)


# (species_set_or_None, name_substrings, exclude_substrings, {field: generator})
_CURATED: tuple[tuple[frozenset | None, tuple[str, ...], tuple[str, ...], dict], ...] = (
    (
        frozenset({"horse"}),
        ("蹄葉炎", "Laminitis"),
        (),
        {"causes_ja": _laminitis_causes, "pathophysiology_ja": _laminitis_patho},
    ),
    (
        None,
        ("肝線維症", "肝繊維症", "Hepatic Fibrosis"),
        (),
        {"causes_ja": _hepatic_fibrosis_causes, "pathophysiology_ja": _hepatic_fibrosis_patho},
    ),
    # --- Dog flagship diseases ---
    (frozenset({"dog"}), ("胃拡張",), (), _GDV),
    (frozenset({"dog"}), ("膵炎",), (), _PANCREATITIS_DOG),
    (frozenset({"dog"}), ("甲状腺機能低下",), ("副甲状腺",), _HYPOTHYROID_DOG),
    (frozenset({"dog"}), ("クッシング", "副腎皮質機能亢進"), (), _CUSHING_DOG),
    (frozenset({"dog"}), ("慢性腎臓病", "慢性腎不全"), (), _CKD_DOG),
    (frozenset({"dog"}), ("アトピー性皮膚炎",), (), _CAD_DOG),
    (frozenset({"dog"}), ("変形性関節症",), (), _OA_DOG),
    (frozenset({"dog"}), ("椎間板ヘルニア",), (), _IVDD_DOG),
    (frozenset({"dog"}), ("特発性てんかん", "若年性てんかん"), (), _EPILEPSY_DOG),
    (frozenset({"dog"}), ("拡張型心筋症",), (), _DCM_DOG),
    (
        frozenset({"dog"}),
        ("粘液腫様僧帽弁", "僧帽弁閉鎖不全", "僧帽弁逆流", "僧帽弁変性", "早期発症僧帽弁"),
        ("形成不全",),
        _MMVD_DOG,
    ),
    # --- Cat flagship diseases ---
    (frozenset({"cat"}), ("肥大型心筋症",), (), _HCM_CAT),
    (frozenset({"cat"}), ("膵炎",), (), _PANCREATITIS_CAT),
    (frozenset({"cat"}), ("炎症性腸疾患",), (), _IBD_CAT),
    (frozenset({"cat"}), ("喘息",), (), _ASTHMA_CAT),
    (frozenset({"cat"}), ("慢性腎臓病", "慢性腎不全"), (), _CKD_CAT),
    (frozenset({"cat"}), ("歯肉口内炎", "慢性口内炎"), (), _FCGS_CAT),
)


def curated_etiology(species: str, name_ja: str, name_en: str) -> dict | None:
    """Return {field: curated_text} for a curated disease, or None.

    The caller decides per-field whether the existing value is replaceable (a
    template / stub / empty); this function only supplies the correct text.
    """
    species = (species or "").lower()
    name = f"{name_ja or ''} {name_en or ''}"
    species_ja = SPECIES_JA.get(species, species)
    for species_set, name_subs, exclude_subs, fields in _CURATED:
        if species_set is not None and species not in species_set:
            continue
        if not any(sub in name for sub in name_subs):
            continue
        if any(bad in name for bad in exclude_subs):
            continue
        return {field: gen(species_ja) for field, gen in fields.items()}
    return None
