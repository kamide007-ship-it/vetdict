"""2026-10 第67弾: チャット精度第43弾・語内部部分一致による薬品誤チップの是正・新規承認薬2剤。"""

import warnings

import pytest

warnings.filterwarnings("ignore")


def _sp(phrase, species, n=5):
    from api.chat.disease_matcher import _match_species_symptoms_to_diseases
    from api.chat.symptom_extractor import _extract_species_symptoms

    ids = _extract_species_symptoms(phrase, species)
    res = _match_species_symptoms_to_diseases(list(ids), species, lang="ja")
    return set(ids), [r.get("name_ja") or "" for r in res[:n]]


def _dog(phrase, n=5):
    from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

    ids = extract_symptoms_from_text(phrase)
    return set(ids), [r.get("name_ja") or "" for r in match_symptoms_to_diseases(ids)[:n]]


def _horse(phrase, n=5):
    from api.diagnostic_chat import _extract_equine_symptoms, _match_equine_symptoms_to_diseases

    ids = _extract_equine_symptoms(phrase)
    return set(ids), [r.get("name_ja") or "" for r in _match_equine_symptoms_to_diseases(ids)[:n]]


class TestDrugMatcherWordInternalContainment:
    @pytest.mark.parametrize(
        "text,present,absent",
        [
            ("アポモルヒネ（0.04 mg/kg IV）で催吐", "apomorphine", "morphine"),
            ("apomorphine 0.03 mg/kg IV", "apomorphine", "morphine"),
            ("エンロフロキサシン 5 mg/kg PO q24h", "enrofloxacin", "ofloxacin_ophthalmic"),
            ("メデトミジン 10 μg/kg IM", "medetomidine", "detomidine"),
            ("ノルエピネフリン 0.1 μg/kg/min CRI", "norepinephrine", "epinephrine"),
            ("メチルプレドニゾロン", "methylprednisolone", "prednisolone"),
            ("メトロニダゾール 10 mg/kg", "metronidazole", "ronidazole"),
            ("オキシテトラサイクリン", "oxytetracycline", "tetracycline"),
            ("hypertonic saline 7.2%", "hypertonic_saline", "pancrelipase"),
        ],
    )
    def test_inner_substring_is_not_a_mention(self, text, present, absent):
        from api.drug_dictionary import find_drugs_in_text

        ids = [d["id"] for d in find_drugs_in_text(text)]
        assert present in ids and absent not in ids, ids

    def test_standalone_short_names_and_combinations_still_chip(self):
        from api.drug_dictionary import find_drugs_in_text

        def ids(t):
            return [d["id"] for d in find_drugs_in_text(t)]

        assert "morphine" in ids("モルヒネ 0.1 mg/kg IV")
        assert "detomidine" in ids("デトミジン 10 μg/kg IV（馬）")
        assert {"epinephrine", "norepinephrine"} <= set(ids("ノルエピネフリン CRI、エピネフリン 0.01 mg/kg"))
        assert {"amoxicillin", "amoxicillin_clavulanate"} <= set(ids("アモキシシリン・クラブラン酸"))

    def test_reverse_index_respects_containment_guard(self):
        from api.drug_dictionary import _inner_superstrings

        sup = _inner_superstrings()
        assert any(k2 == "enrofloxacin" for k2, _ in sup.get("ofloxacin", []))
        assert any(k2 == "apomorphine" for k2, _ in sup.get("morphine", []))
        # 合剤（先頭一致・区切りあり）はガード対象外
        assert not any("clavulanate" in k2 for k2, _ in sup.get("amoxicillin", []))


class TestBatch75:
    def _d(self, did):
        from api.drug_dictionary import DRUGS

        return next(d for d in DRUGS if d["id"] == did)

    def test_ropinirole_label_and_safety(self):
        d = self._d("ropinirole_ophthalmic")
        dog = d["species_info"]["dog"]
        assert "3.75 mg/m2" in dog["dosage"] and "15 minutes" in dog["dosage"]
        assert "3.75 mg/m²" in dog["dosage_ja"] and "15分" in dog["dosage_ja"]
        assert d["species_info"]["cat"]["safe"] is False
        assert "腐食性" in d["contraindications_ja"] and "corrosive" in d["contraindications"].lower()
        assert any("Maropitant" in i["drug"] for i in d["drug_interactions"])

    def test_enflicoxib_weekly_regimen(self):
        d = self._d("enflicoxib")
        dog = d["species_info"]["dog"]
        assert "8 mg/kg" in dog["dosage"] and "4 mg/kg" in dog["dosage"] and "weekly" in dog["dosage"]
        assert "週1回" in dog["dosage_ja"]
        assert d["species_info"]["cat"]["safe"] is False
        assert any(i["severity"] == "major" for i in d["drug_interactions"])

    def test_resolution_and_disease_links(self):
        from api.drug_dictionary import find_drugs_for_disease, resolve_drug_reference

        assert resolve_drug_reference("クレボー") == "ropinirole_ophthalmic"
        assert resolve_drug_reference("だくそこっくす") == "enflicoxib"
        for name in ("Chocolate Toxicosis", "Xylitol Poisoning", "Grape/Raisin Toxicosis"):
            ids = [x["id"] for x in find_drugs_for_disease("dog", name)]
            assert "ropinirole_ophthalmic" in ids and "apomorphine" in ids and "morphine" not in ids, (name, ids)
        assert "enflicoxib" in [x["id"] for x in find_drugs_for_disease("dog", "Osteoarthritis")]


class TestChatClinicalAccuracyAuditRound43:
    def test_skin_redness_does_not_become_bleeding(self):
        for sp in ("cat", "bird", "parrot"):
            ids, _ = _sp("皮膚が赤くなっています", sp)
            assert "bleeding" not in ids and "hemorrhage" not in ids, (sp, ids)

    def test_amphibian_skin_redness_native(self):
        ids, top = _sp("皮膚が赤くなって元気がないです", "amphibian")
        assert "skin_redness" in ids
        assert any("レッドレッグ" in t or "エロモナス" in t for t in top[:2]), top

    def test_dog_ear_redness_and_melena(self):
        ids, top = _dog("耳の中が赤くて臭いがします")
        assert ids and "外耳炎" in top[0], (ids, top)
        ids, _ = _dog("ウンチが黒っぽいです")
        assert "blood_in_stool" in ids

    def test_cat_litter_box_squatting(self):
        ids, top = _sp("トイレで何度もしゃがんでいます", "cat")
        assert "frequent_urination" in ids
        assert any(x in t for t in top for x in ("膀胱炎", "尿道", "FIC", "特発性")), top

    def test_coverage_bonus_counts_complaints_not_synonyms(self):
        _, top = _sp("羽を膨らませて寝てばかりいます", "bird")
        assert top[0] != "アボカド中毒", top

    @pytest.mark.parametrize(
        "phrase,species,expect",
        [
            ("片足をあげて歩きます", "dog", ("膝蓋骨", "十字", "肘")),
            ("食後にお腹がパンパンになって吐こうとします", "dog", ("胃拡張",)),
            ("目の色が変わってきました", "cat", ("虹彩", "ぶどう膜")),
            ("足の裏に傷があります", "rabbit", ("足底", "ソアホック")),
            ("便に血が混じっています", "bird", ("コクシジウム", "腸炎", "総排泄腔", "乳頭腫")),
            ("口が腫れて膿があります", "snake", ("口内炎",)),
            ("浮いて沈めません", "amphibian", ("浮", "水腫", "腹水")),
            ("体を岩にこすりつけています", "fish", ("白点", "寄生", "ウオジラミ", "トリコジナ", "吸虫")),
            ("尻尾が切れました", "degu", ("尾",)),
            ("羽の色が変わってきました", "parrot", ("PBFD", "羽", "栄養", "肝")),
        ],
    )
    def test_previously_unextractable_complaints(self, phrase, species, expect):
        if species == "dog":
            ids, top = _dog(phrase)
        else:
            ids, top = _sp(phrase, species)
        assert ids, phrase
        assert any(e in t for t in top for e in expect), (phrase, top)

    def test_rabbit_vulvar_bleeding_uterine_adenocarcinoma(self):
        ids, top = _sp("陰部から血が出ています", "rabbit")
        assert "vaginal_bleeding" in ids and top[0] == "子宮腺癌", top
        ids, top = _dog("陰部から血が出ています")
        assert "vulvar_discharge" in ids
        ids, _ = _sp("陰部から血が出ている", "cat")
        assert "bleeding" not in ids

    def test_polite_ichidan_negation(self):
        from api.chat.symptom_extractor import normalize_chat_text

        assert normalize_chat_text("沈めません") == "沈めない"
        assert normalize_chat_text("止めました") == "止めた"


class TestEquineRound43:
    def test_stocking_up_for_afebrile_limb_edema(self):
        ids, top = _horse("後ろ足がむくんでいます")
        assert ids == {"limb_filling"} and top[0] == "繋留性下肢浮腫(ストッキングアップ)", (ids, top)

    def test_febrile_limb_swelling_is_cellulitis_lymphangitis(self):
        _, top = _horse("後ろ足がむくんで熱があります")
        assert top[0] != "繋留性下肢浮腫(ストッキングアップ)"
        assert any("リンパ管炎" in t or "蜂窩織炎" in t for t in top[:3]), top

    def test_fever_cough_viral_respiratory(self):
        _, top = _horse("熱っぽくて咳をします")
        assert set(top[:2]) <= {"馬インフルエンザ", "馬ヘルペスウイルス4型感染症"}, top

    def test_exercise_cough_asthma_and_misc(self):
        _, top = _horse("運動すると咳が出ます")
        assert top[0] == "馬喘息 (IAD/RAO)", top
        _, top = _horse("皮膚にイボがあります")
        assert top[0] == "サルコイド"
        ids, top = _horse("ご飯を食べず元気がありません")
        assert "gen_poor_appetite" in ids

    def test_misassigned_limb_filling_removed(self):
        from api.species.equine_diseases import DISEASE_DATABASE

        by = {d.name_en: d for d in DISEASE_DATABASE}
        for name in ("Guttural Pouch Tympany", "Jugular Thrombophlebitis", "Orbital Cellulitis"):
            assert "limb_filling" not in by[name].associated_findings, name
        assert "resp_cough_at_exercise" in by["Equine Asthma (IAD/RAO)"].associated_findings
