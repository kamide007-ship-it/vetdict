"""Symptom extraction from natural language text.

Extracts symptom IDs from JP/EN text using longest-match-first strategy.
"""

from api.chat.species_data import get_species_data
from api.chat.symptom_aliases import SYMPTOM_ALIASES

# Cross-species ID mapping: dog aliases use "loss_of_appetite" but many
# species modules use "appetite_loss", "anorexia", etc. for the same concept.
# Hoisted to module scope so it can be reused by name-resolution helpers
# (e.g. follow-up question label localization).
ID_SYNONYMS: dict[str, list[str]] = {
    # Appetite
    "loss_of_appetite": ["appetite_loss", "anorexia", "poor_appetite", "decreased_appetite"],
    "appetite_loss": ["loss_of_appetite", "anorexia", "poor_appetite", "decreased_appetite"],
    "anorexia": ["loss_of_appetite", "appetite_loss", "poor_appetite"],
    "increased_appetite": ["appetite_increase", "polyphagia", "increased_hunger", "gen_increased_appetite"],
    "appetite_increase": ["increased_appetite", "polyphagia", "increased_hunger"],
    # General
    "lethargy": ["depression", "inactivity", "weakness", "listlessness", "muscle_wasting"],
    "weakness": ["lethargy", "depression", "inactivity", "muscle_weakness", "generalized_weakness"],
    "depression": ["lethargy", "inactivity", "weakness"],
    "fever": ["hyperthermia", "elevated_temperature"],
    "swollen_lymph_nodes": [
        "lymph_node_enlargement",
        "enlarged_lymph_nodes",
        "lymphadenopathy",
        "lymphadenomegaly",
        "lymph_node_swelling",
    ],
    # GI
    "regurgitation": ["vomiting", "emesis"],
    "diarrhea": ["loose_stool", "watery_stool", "soft_stool"],
    "vomiting": ["regurgitation", "emesis"],
    "constipation": [
        "reduced_fecal_output",
        "straining_to_defecate",
        "small_fecal_pellets",
        "decreased_fecal_output",
        # Birds/reptiles carry the tenesmus complaint as bare "straining"
        # ("いきんでいる" — egg binding, cloacal impaction); mammal species
        # resolve constipation directly so this fallback never fires there.
        "straining",
    ],
    "reduced_fecal_output": ["constipation", "small_fecal_pellets", "decreased_fecal_output"],
    "decreased_fecal_output": ["reduced_fecal_output", "constipation", "small_fecal_pellets"],
    "small_fecal_pellets": ["reduced_fecal_output", "constipation"],
    "teeth_grinding": ["bruxism", "dental_pain"],
    "abdominal_pain": ["abdominal_distension", "hunched_posture", "bloating", "bloated_abdomen"],
    "bloating": [
        "abdominal_distension",
        "abdominal_distention",
        "distended_abdomen",
        "bloated_abdomen",
        "abdominal_pain",
    ],
    "abdominal_distension": [
        "bloating",
        "abdominal_distention",
        "distended_abdomen",
        "bloated_abdomen",
        "abdominal_pain",
    ],
    # Neuro
    "seizures": ["convulsions", "fits", "epileptic_episodes"],
    "fainting": ["collapse", "syncope", "prostration", "recumbency"],
    "collapse": ["fainting", "syncope", "prostration", "recumbency"],
    "paralysis_or_paresis": [
        "paralysis",
        "paresis",
        "hind_limb_weakness",
        "hind_limb_paralysis",
        "posterior_paresis",
        "progressive_paralysis",
        "hindlimb_weakness",
        "hind_leg_weakness",
    ],
    "paralysis": ["paralysis_or_paresis", "paresis", "hind_limb_weakness", "hind_limb_paralysis"],
    "hind_leg_weakness": ["hind_limb_weakness", "hindlimb_weakness", "posterior_paresis"],
    "hind_limb_weakness": ["hind_leg_weakness", "hindlimb_weakness", "posterior_paresis", "progressive_paralysis"],
    "jaundice": ["icterus", "yellow_skin", "yellow_mucous_membranes"],
    # Weight / body
    "weight_loss": ["emaciation", "wasting", "cachexia", "rough_coat", "poor_growth"],
    "weight_gain": ["obesity", "overweight"],
    "emaciation": ["weight_loss", "wasting", "cachexia"],
    # Skin / coat
    "excessive_drooling": ["drooling", "hypersalivation", "ptyalism"],
    "drooling": ["excessive_drooling", "hypersalivation"],
    "bad_breath": ["halitosis", "oral_odor"],
    "oral_ulcers": ["mouth_lesions", "stomatitis", "gingivitis"],
    "excessive_licking": ["itching", "pruritus", "scratching", "overgrooming", "ear_scratching", "scratching_ears"],
    "pop_eye": [
        "exophthalmia",
        "exophthalmos",
        "eye_protrusion",
        "bulging_eye",
        "eye_swelling",
        "eye_bulging",
        "enlarged_eye",
    ],
    "eye_protrusion": [
        "pop_eye",
        "exophthalmia",
        "exophthalmos",
        "eye_bulging",
        "bulging_eye",
        "eye_swelling",
        "enlarged_eye",
        "proptosis",
    ],
    "eye_swelling": [
        "pop_eye",
        "exophthalmia",
        "exophthalmos",
        "periorbital_swelling",
        "swollen_eyes",
        "bulging_eye",
        "eye_swollen",
        "eye_bulging",
        "enlarged_eye",
        "eye_protrusion",
    ],
    "eye_bulging": [
        "pop_eye",
        "exophthalmia",
        "exophthalmos",
        "eye_protrusion",
        "eye_swelling",
        "bulging_eye",
        "enlarged_eye",
        "proptosis",
    ],
    "exophthalmos": [
        "pop_eye",
        "eye_protrusion",
        "eye_bulging",
        "eye_swelling",
        "bulging_eye",
        "enlarged_eye",
        "proptosis",
    ],
    "enlarged_eye": ["eye_bulging", "eye_swelling", "exophthalmos", "pop_eye", "eye_protrusion"],
    "ear_discharge": ["ear_infection", "ear_inflammation", "otitis", "ear_mites"],
    "blood_in_urine": ["hematuria", "bloody_urine", "uterine_bleeding", "blood_urine"],
    "blood_urine": ["blood_in_urine", "hematuria", "bloody_urine"],
    "blood_in_stool": ["melena", "hematochezia", "bloody_stool", "bleeding_gums"],
    "itching": [
        "pruritus",
        "scratching",
        "scratching_ears",
        "ear_scratching",
        "excessive_grooming",
        "excessive_licking",
        "overgrooming",
    ],
    "pruritus": ["itching", "scratching", "excessive_licking"],
    # 耳の痒み: 「耳が痒い/耳をかく」→ ear_scratching。猫等の語彙は
    # scratching_ears 表記のため双方向にブリッジ（外耳炎・耳ダニが正しくランク）
    "ear_scratching": ["scratching_ears", "itching"],
    "scratching_ears": ["ear_scratching", "itching"],
    # 耳血腫（耳介の波動性腫脹）— 犬レガシー/ウサギは ear_swelling を直接保有。
    # 猫語彙は ear_inflammation 表記のためブリッジで解決する。
    "ear_swelling": ["ear_inflammation", "ear_thickening", "facial_swelling", "swelling"],
    # ドライアイ — 犬レガシーは dry_eye を直接保有。他種は眼分泌物が最近接シグナル。
    "dry_eye": ["eye_discharge"],
    "lameness_or_limping": [
        "lameness",
        "limping",
        "joint_swelling",
        "joint_pain",
        "leg_swelling",
        "foot_swelling",
        "reluctance_to_move",
        # Dog checkbox vocabulary only carries per-leg limping IDs — resolve an
        # unspecified-leg complaint ("足を引きずる"/"limping") to the most common
        # canine presentation (hindlimb: CCL rupture, hip dysplasia); the
        # matcher's _SYN cross-leg expansion then credits any-leg diseases.
        "limping_rl",
        "limping_fl",
        "limping_rr",
        "limping_fr",
    ],
    "lumps_and_bumps": ["lumps_nodules", "skin_masses", "tumors", "skin_lumps", "lumps"],
    # Hair
    "hair_loss": [
        "alopecia",
        "fur_loss",
        "feather_loss",
        "bald_patches",
        "quill_loss",
        "severe_quill_loss",
        "scaling",
        "circular_hair_loss",
    ],
    "circular_hair_loss": ["hair_loss", "alopecia", "fur_loss", "bald_patches"],
    "alopecia": ["hair_loss", "fur_loss", "bald_patches", "circular_hair_loss"],
    "feather_loss": ["hair_loss", "feather_plucking", "alopecia"],
    "skin_lesions": [
        "scaling",
        "dermatitis",
        "skin_rash",
        "crusting",
        "thick_crusting",
        "flaky_skin",
        "dry_skin",
        "shell_discoloration",
        "shell_pitting",
        "skin_crusting",
    ],
    "scaly_skin": ["scaling", "dandruff", "skin_crusting", "dry_skin", "flaky_skin"],
    "skin_crusting": ["scaling", "scaly_skin", "dandruff", "crusting"],
    "scaling": ["skin_lesions", "dandruff", "scaly_skin", "skin_crusting"],
    "dandruff": ["scaling", "scaly_skin", "skin_crusting"],
    # Eyes
    "cloudiness_in_eyes": [
        "cloudy_eyes",
        "eye_cloudiness",
        "corneal_opacity",
        "cloudy_eye",
        "corneal_cloudiness",
        "cataracts",
    ],
    "cloudy_eyes": [
        "cloudiness_in_eyes",
        "eye_cloudiness",
        "corneal_opacity",
        "cloudy_eye",
        "corneal_cloudiness",
        "cataracts",
    ],
    "cloudy_eye": ["cloudy_eyes", "cloudiness_in_eyes", "eye_cloudiness", "corneal_cloudiness", "cataracts"],
    "corneal_opacity": ["corneal_cloudiness", "cloudy_eyes", "cloudy_eye", "cloudiness_in_eyes"],
    "corneal_cloudiness": ["corneal_opacity", "cloudy_eyes", "cloudy_eye", "cloudiness_in_eyes"],
    "redness_in_eyes": ["red_eyes", "conjunctivitis", "eye_redness"],
    "eye_discharge": ["ocular_discharge", "eye_secretion", "epiphora"],
    "squinting": ["blepharospasm", "eye_squinting"],
    "tearing": ["excessive_tearing", "epiphora", "eye_discharge"],
    "excessive_tearing": ["tearing", "epiphora", "eye_discharge"],
    "vision_loss": ["blindness", "cloudy_eye", "cloudy_eyes", "cataracts"],
    # 鼻出血: ウサギ語彙は epistaxis を正規IDに持つ。他種は鼻分泌物へフォールバック
    "epistaxis": ["nose_bleeding", "nasal_discharge"],
    # EPI hallmark の大量便: フェレット語彙は voluminous_stool を保有。他種は下痢へ
    "voluminous_stool": ["bulky_stool", "diarrhea"],
    # 猫DJDのジャンプ回避: 他種では動きたがらない・こわばりへフォールバック
    "reluctance_to_jump": ["reluctance_to_move", "stiffness"],
    # 過剰グルーミング: 語彙に無い種では舐め行動へフォールバック
    "excessive_grooming": ["overgrooming", "excessive_licking"],
    # Respiratory
    "labored_breathing": ["respiratory_distress", "dyspnea", "open_mouth_breathing", "difficulty_breathing"],
    "respiratory_distress": ["labored_breathing", "dyspnea", "open_mouth_breathing"],
    "open_mouth_breathing": ["labored_breathing", "respiratory_distress", "mouth_breathing"],
    "rapid_breathing": ["tachypnea", "panting", "labored_breathing"],
    "coughing": ["cough", "kennel_cough"],
    "wheezing": [
        "coughing",
        "labored_breathing",
        "respiratory_distress",
        "clicking_breathing_sounds",
        "breathing_difficulty",
        "difficulty_breathing",
    ],
    "sneezing": ["reverse_sneezing", "nasal_irritation", "nasal_discharge"],
    "nasal_discharge": ["runny_nose", "rhinorrhea", "nasal_secretion", "sneezing"],
    # Urinary
    "straining_to_urinate": [
        "dysuria",
        "urinary_straining",
        "difficulty_urinating",
        "stranguria",
        "straining_urinate",
    ],
    "straining_urinate": ["straining_to_urinate", "dysuria", "urinary_straining", "difficulty_urinating"],
    # pollakiuria (frequent small urinations) is an LUTD sign — resolve toward
    # straining before the polyuria-flavoured IDs so「おしっこの回数が多い」
    # ranks cystitis/urolithiasis rather than polyuric endocrinopathies.
    "frequent_urination": [
        "pollakiuria",
        "straining_to_urinate",
        "straining_urinate",
        "polyuria",
        "excessive_urination",
        "increased_urination",
    ],
    "excessive_urination": ["frequent_urination", "polyuria", "pollakiuria", "increased_urination"],
    "increased_urination": ["excessive_urination", "frequent_urination", "polyuria", "pollakiuria"],
    "cloudy_urine": ["turbid_urine", "murky_urine"],
    "foul_smelling_urine": ["malodorous_urine", "urine_odor"],
    "incontinence": ["urine_leakage", "urinary_incontinence"],
    "increased_thirst": ["excessive_thirst", "polydipsia"],
    "excessive_thirst": ["increased_thirst", "polydipsia"],
    "polydipsia": ["excessive_thirst", "increased_thirst"],
    "polyuria": ["excessive_urination", "frequent_urination", "increased_urination"],
    # Musculoskeletal
    "joint_pain_or_stiffness": ["joint_pain", "arthritis", "stiffness"],
    # Behavior
    "anxiety": ["restlessness", "pacing", "nervousness"],
    "self_mutilation": ["self_chewing", "self_harm", "overgrooming", "feather_plucking"],
    "self_chewing": ["self_mutilation", "self_harm"],
    "behavioral_change": ["behavioral_changes", "aggression", "depression", "restlessness"],
    "behavioral_changes": ["behavioral_change", "aggression", "depression"],
    # Head
    "head_tilt": ["vestibular_signs", "torticollis", "wry_neck", "nystagmus"],
    "nystagmus": ["head_tilt", "vestibular_signs", "rolling"],
    "ataxia": ["tremors", "incoordination", "wobbling", "unsteady_gait"],
    "tremors": ["shaking", "trembling", "muscle_tremors", "ataxia"],
    "wobbling": ["ataxia", "incoordination", "unsteady_gait", "stumbling"],
    # Reptile-specific
    "dysecdysis": ["abnormal_shedding", "retained_shed", "shedding_problems", "retained_skin"],
    "retained_shed": ["dysecdysis", "retained_skin", "shedding_problems"],
    "retained_skin": ["dysecdysis", "retained_shed", "shedding_problems"],
    "soft_bones": [
        "bone_weakness",
        "jaw_softening",
        "shell_soft_spots",
        "fractures",
        "bone_deformity",
        "shell_softening",
        "soft_shell",
    ],
    "bone_deformity": ["bone_swelling", "limb_deformity", "soft_bones", "shell_deformity", "fractures"],
    # 四肢の弯曲（爬虫類MBD/くる病の飼い主表現「脚が曲がってきた」）—
    # limb_deformity を持たない種（lizard等）では soft_bones/swollen_limbs に解決
    "limb_deformity": ["bone_deformity", "soft_bones", "swollen_limbs", "fractures"],
    "shell_softening": ["soft_shell", "soft_bones", "shell_soft_spots", "shell_deformity"],
    "soft_shell": ["shell_softening", "soft_bones", "shell_soft_spots", "shell_deformity"],
    "shell_deformity": ["bone_deformity", "soft_shell", "shell_softening"],
    "mouth_lesions": ["oral_lesions", "stomatitis", "mouth_rot"],
    "mucus_in_mouth": ["oral_mucus", "mouth_discharge"],
    # 直腸脱/クロアカ脱（「お尻から赤いものが出ている」）— 種ごとのID表記ゆれを吸収
    # 爬虫類（lizard等）は tissue_protruding_from_cloaca / tissue_prolapse /
    # cloacal_swelling 表記のため、そのIDにもフォールバック（2026-08 第11回スイープ:
    # トカゲ「お尻から何か出ている」が抽出後に解決不能だった）
    "rectal_prolapse": [
        "rectal_protrusion",
        "cloacal_prolapse",
        "prolapse",
        "tissue_protruding_from_cloaca",
        "tissue_prolapse",
        "cloacal_swelling",
    ],
    "rectal_protrusion": ["rectal_prolapse", "cloacal_prolapse"],
    "cloacal_prolapse": [
        "rectal_prolapse",
        "rectal_protrusion",
        "prolapse",
        "tissue_protruding_from_cloaca",
        "tissue_prolapse",
    ],
    # 2026-08 第11回スイープ: 条虫片節・回虫の飼い主主訴（「便に白い米粒」）と
    # 嘴過長・スペクタクル残留の種別ID表記ゆれ
    "worms_in_stool": ["visible_worms", "visible_parasites", "diarrhea"],
    "overgrown_beak": ["beak_deformity", "beak_overgrowth"],
    "retained_spectacle": ["dysecdysis", "cloudy_eyes", "eye_opacity"],
    # 2026-08 Round 13: フェレット低血糖の口掻き・チンチラ熱中症の耳充血・
    # 乳腺腫大の種別ID表記ゆれ（cat=mammary_masses）
    "pawing_at_mouth": ["pawing_at_face", "drooling", "difficulty_eating"],
    "red_ears": ["ear_redness"],
    "ear_redness": ["red_ears"],
    "mammary_swelling": ["mammary_masses", "mammary_enlargement", "lumps"],
    # Limbs / extremities
    "cold_limbs": ["cold_extremities", "poor_circulation"],
    "cold_extremities": ["cold_limbs", "poor_circulation"],
    # 2026-08 第9回精度スイープ: 心不全・頸部痛・鳥緑色便の主訴が解決不能だった
    "exercise_intolerance": ["resp_exercise_intolerance", "lethargy"],
    "cyanosis": [
        "blue_gums",
        "labored_breathing",
        "difficulty_breathing",
        "breathing_difficulty",
        "respiratory_distress",
    ],
    "neck_stiffness": ["neck_pain", "stiffness", "reluctance_to_move", "reluctance_move", "pain"],
    # 鳥の緑色便（ビリベルジン尿）— 種ごとの便ID表記ゆれを吸収し、
    # 該当IDを持たない哺乳類等では diarrhea にフォールバック
    "diarrhea_green": ["yellow_green_droppings", "diarrhea_yellow_green", "green_droppings", "diarrhea"],
    # 「皮膚に白いもの」— 両生類は白斑/綿状増殖、魚は白点に解決
    "white_patches_skin": ["white_patches", "cotton_like_growth", "white_spots"],
    # Bird-specific
    "fluffed_feathers": ["feather_fluffing", "puffed_up", "ruffled_feathers"],
    "feather_plucking": ["feather_loss", "self_mutilation", "feather_destructive_behavior"],
    "crop_swelling": ["crop_stasis", "ingluvitis", "crop_distension"],
    "crop_stasis": ["crop_swelling", "ingluvitis"],
    # Fish fin
    "frayed_fins": ["fin_rot", "fin_erosion", "ragged_fins"],
    "fin_rot": ["frayed_fins", "fin_erosion"],
    "redness_skin": ["skin_redness", "hemorrhage", "fin_hemorrhage", "bleeding"],
    "skin_redness": ["redness_skin", "hemorrhage", "red_legs", "red_ventrum"],
    "fin_hemorrhage": ["redness_skin", "hemorrhage"],
    # Hamster
    "wet_tail": ["diarrhea", "watery_diarrhea"],
    # Skin / coat additional
    "thinning_skin": ["skin_fragility", "thin_skin", "fragile_skin"],
    "poor_coat": ["dry_skin", "rough_coat", "dull_coat"],
    "rough_coat": ["poor_coat", "dry_skin", "dull_coat"],
    # Ferret reproductive
    "vulvar_swelling": ["vulvar_discharge", "genital_swelling"],
    "prostatic_enlargement": ["prostate_enlargement", "enlarged_prostate"],
    # Cardiac
    "bradycardia": ["slow_heart_rate"],
    # Cheek / oral
    "cheek_swelling": ["bloating", "cheek_pouch_prolapse", "facial_swelling"],
    "cheek_pouch_prolapse": ["cheek_swelling"],
    "jaw_swelling": ["facial_swelling", "swelling"],
    "abscess": ["discharge", "swelling"],
    "overgrown_teeth": [
        "dental_overgrowth",
        "incisor_overgrowth",
        "molar_overgrowth",
        "tooth_overgrowth",
        "malocclusion",
        "visible_tooth_overgrowth",
    ],
    "dental_overgrowth": [
        "overgrown_teeth",
        "incisor_overgrowth",
        "molar_overgrowth",
        "malocclusion",
        "visible_tooth_overgrowth",
    ],
    "visible_tooth_overgrowth": ["overgrown_teeth", "dental_overgrowth", "malocclusion"],
    "scaly_legs": ["leg_scales", "scaly_face"],
    "leg_scales": ["scaly_legs", "scaly_face"],
    # Pain
    "pain": ["lethargy", "vocalization"],
    # Oral
    "stomatitis": ["oral_ulcers", "bad_breath", "excessive_drooling"],
    # Perianal
    "perineal_swelling": ["perianal_irritation", "swelling"],
    # Guinea pig scurvy
    "bleeding_gums": ["swollen_gums", "oral_bleeding"],
    "swollen_joints": ["joint_swelling", "lameness_or_limping", "lameness"],
    # Fish
    "darkened_coloration": ["dark_coloration", "discoloration"],
    "dark_coloration": ["darkened_coloration", "discoloration"],
    # Amphibian
    "red_legs": ["red_ventrum", "skin_redness", "hemorrhage"],
    "red_ventrum": ["red_legs", "skin_redness", "hemorrhage"],
    "edema": ["swelling", "bloating", "ascites"],
    # Effusion / ascites (dogs/cats use "bloated_abdomen" / "abdominal_pain")
    "effusion": ["pleural_effusion", "abdominal_distension", "ascites", "bloated_abdomen"],
    "pleural_effusion": ["effusion", "labored_breathing"],
    "ascites": ["effusion", "abdominal_distension", "bloating", "dropsy", "bloated_abdomen", "abdominal_pain"],
    "dropsy": ["bloating", "edema", "ascites", "abdominal_distension", "bloated_abdomen", "abdominal_pain"],
    # NOTE: bloating / abdominal_distension keys defined earlier; bloated_abdomen added there
    # Swelling (generic)
    "swelling": ["facial_swelling", "eye_swelling", "edema"],
    # --- 2026-08 accuracy sweep round 6 ---
    # Plantar lesions: species-specific pododermatitis IDs, falling back to
    # lameness only where no foot vocabulary exists.
    "foot_sores": [
        "pododermatitis_signs",
        "foot_lesions",
        "foot_redness",
        "foot_swelling",
        "swollen_foot",
        "bumblefoot",
        "lameness_or_limping",
        "limping",
    ],
    # Non-productive retching gestures (ferret Helicobacter/gastric ulcer sign);
    # species without a retching ID fall back to vomiting for matching.
    "unproductive_retching": ["retching", "nausea", "vomiting"],
    # Falling off the perch: parakeet/parrot vocabularies carry perch deficits
    # under different IDs; neuro fallback for other avians.
    "falling_off_perch": ["inability_to_perch", "difficulty_perching", "ataxia", "incoordination"],
    # Reluctance to move (pain sign in small herbivores); fall back to
    # lameness/lethargy where the species lacks the dedicated ID.
    "reluctance_to_move": ["lameness_or_limping", "limping", "lethargy"],
    # Oral pain presenting as difficulty eating (dental/stomatitis complaints).
    "difficulty_eating": ["dropping_food", "dysphagia", "appetite_loss", "loss_of_appetite"],
    # Moist erosive skin lesions ("ジュクジュク"): hot_spots is the legacy dog
    # ID; other species fall back to their generic lesion vocabulary.
    "hot_spots": ["skin_lesions", "skin_rashes", "skin_ulcers", "moist_dermatitis"],
    # かさぶた ("かさぶたがある" alias resolves to crusting, which the dog
    # vocabulary lacks — bridge to the lesion IDs so crusting complaints reach
    # zinc-responsive dermatosis and pyoderma).
    "crusting": ["crusty_skin", "skin_crusting", "skin_lesions", "skin_rashes"],
    # Scaly-face mite (Knemidokoptes) complaints — parakeet carries the
    # specific IDs; bird/parrot fall back to their facial-lesion IDs.
    "crusty_beak": ["beak_deformity", "crusty_lesions_on_face", "crusting", "skin_lesions"],
    "scaly_face": ["crusty_lesions_on_face", "crusty_beak", "thickened_skin", "skin_lesions"],
    # 発疹/湿疹 resolve to the legacy skin_rashes ID; species vocabularies
    # carry rashes under their generic lesion IDs.
    "skin_rashes": ["skin_lesions", "skin_redness", "rash", "rashes"],
    # --- 2026-08 round-10 sweep bridges ---
    # ボルボリグミ（お腹がキュルキュル）: no species carries a dedicated
    # borborygmi ID — bridge to the nausea/gas vocabulary.
    "stomach_gurgling": ["nausea", "bloating", "abdominal_distension"],
    # 草を食べたがる (grass eating — owner-reported nausea proxy): species
    # vocabularies carry nausea only sporadically — fall back to vomiting.
    "nausea": ["vomiting", "retching", "drooling"],
    # 声がかすれる (bark/voice change — the GOLPP hallmark): cat and the legacy
    # dog vocabulary carry voice_change directly; others fall back to the
    # airway-noise IDs.
    "voice_change": ["vocalization_changes", "wheezing", "stridor"],
    # カサカサ (dry flaky skin): the cat vocabulary expresses it as scaling —
    # without this bridge the ear-tip mange complaint lost the sign entirely.
    "dry_skin": ["scaling", "flaky_skin", "skin_scaling", "skin_lesions"],
    # --- 2026-08 round-13 sweep bridges ---
    # あごが濡れている (slobbers/wet chin — the rabbit/rodent dental hallmark):
    # guinea pig and chinchilla carry wet_chin natively; the rabbit vocabulary
    # expresses ptyalism as drooling/salivation/dewlap_wetness.
    "wet_chin": ["drooling", "salivation", "dewlap_wetness", "facial_wetness"],
    # キーキー鳴く (screaming/vocal change): the cat vocabulary carries
    # vocalization_changes natively; ferret and most small mammals use bare
    # vocalization, birds use screaming/pain_vocalization.
    "vocalization_changes": [
        "vocalization",
        "screaming",
        "pain_vocalization",
        "distress_vocalizations",
    ],
    # 尿が茶色い (pigmenturia — haemoglobin/bilirubin): cat/rabbit/hedgehog
    # carry dark_urine natively; others express discoloured urine as
    # red_urine / blood_in_urine.
    "dark_urine": ["red_urine", "blood_in_urine"],
    # 止まり木を握れない (grip loss): bird carries inability_to_perch natively;
    # psittacine vocabularies vary — bridge to the perching/limb-weakness IDs.
    "inability_to_perch": ["difficulty_perching", "falling_off_perch", "leg_weakness"],
    # 口をくちゃくちゃ (jaw chattering — feline oral pain/FORL sign): only the
    # cat vocabulary carries it natively; bridge to eating-difficulty IDs.
    "jaw_chattering": ["difficulty_eating", "drooling", "mouth_pain"],
}

# Backwards-compat alias (some older imports use the private name).
_ID_SYNONYMS = ID_SYNONYMS


# 否定表現ガード: 「咳はない」「嘔吐はしていない」「下痢なし」のように、症状語の直後に
# 否定が続く場合はその症状を抽出しない（従来は「咳はない」でも coughing が抽出され、
# 除外情報のつもりの入力が逆に鑑別を汚染していた）。
# 保守的設計: 症状語の直後（は/も + まだ/特に を許容）に否定語が続く場合のみ発火。
# 「食欲がない」「飲み込めない」のような否定形を内包するエイリアス自体は、マッチ範囲の
# 後ろを検査するため影響を受けない。
import re as _neg_re

_NEGATION_AFTER_RE = _neg_re.compile(
    r"^(?:は|も)?(?:まだ|特に|とくに)?"
    r"(?:ない|無い|なし|ありません|出ていない|出てない|でていない"
    r"|していない|してない|しません|見られない|みられない)"
)


def is_negated_mention(text: str, end: int) -> bool:
    """Return True if the symptom mention ending at ``end`` is directly negated."""
    return bool(_NEGATION_AFTER_RE.match(text[end : end + 12]))


def resolve_symptom_id(sid: str, symptom_names: dict) -> str | None:
    """Return the canonical symptom ID for a species, following synonyms.

    If ``sid`` is directly present in ``symptom_names``, returns it. Otherwise
    walks ``ID_SYNONYMS`` and returns the first alternate that exists.
    """
    if sid in symptom_names:
        return sid
    for alt in ID_SYNONYMS.get(sid, []):
        if alt in symptom_names:
            return alt
    return None


def _extract_species_symptoms(text: str, species: str) -> list[str]:
    """Extract symptom IDs from text using species-specific SYMPTOM_NAMES.

    Uses longest-match-first strategy and Japanese particle splitting
    for maximum extraction accuracy across all species.
    """
    sp_data = get_species_data(species)
    if not sp_data:
        return []

    text_lower = text.lower()
    matched: set[str] = set()
    symptom_names = sp_data["symptom_names"]

    def _resolve_id(sid: str) -> str | None:
        return resolve_symptom_id(sid, symptom_names)

    # Phase 1: Longest-match-first alias matching (aliases → species symptom IDs)
    # Track consumed character positions to avoid substring double-matching
    # (e.g. "外陰部が腫れてる" should not also match "腫れてる")
    _sorted_aliases = sorted(SYMPTOM_ALIASES.keys(), key=len, reverse=True)
    _consumed: set[int] = set()
    for alias in _sorted_aliases:
        pos = text_lower.find(alias)
        if pos >= 0:
            alias_range = set(range(pos, pos + len(alias)))
            if alias_range & _consumed:
                continue
            if is_negated_mention(text_lower, pos + len(alias)):
                # 「嘔吐はしていない」等 — 否定された言及は抽出せず、範囲だけ消費して
                # 短いサブストリングの再マッチも防ぐ
                _consumed |= alias_range
                continue
            symptom_id = SYMPTOM_ALIASES[alias]
            resolved = _resolve_id(symptom_id)
            if resolved:
                matched.add(resolved)
                _consumed |= alias_range

    # Phase 2: Direct symptom name matches (ja/en)
    for sym_id, names in symptom_names.items():
        ja = names.get("ja", "").lower()
        en = names.get("en", "").lower()
        ja_pos = text_lower.find(ja) if ja else -1
        en_pos = text_lower.find(en) if en else -1
        if (ja_pos >= 0 and not is_negated_mention(text_lower, ja_pos + len(ja))) or (
            en_pos >= 0 and not is_negated_mention(text_lower, en_pos + len(en))
        ):
            matched.add(sym_id)

    # Phase 3: Fragment splitting for compound Japanese phrases
    if not matched:
        import re as _re

        fragments = _re.split(r"[、。,.と！!？?\s]+", text_lower)
        fragments = [f.strip() for f in fragments if len(f.strip()) >= 1]
        for frag in fragments:
            for alias in _sorted_aliases:
                if alias in frag:
                    sid = SYMPTOM_ALIASES[alias]
                    if sid in symptom_names:
                        matched.add(sid)
                        break
            for sym_id, names in symptom_names.items():
                ja = names.get("ja", "").lower()
                en = names.get("en", "").lower()
                if (ja and ja in frag) or (en and en in frag):
                    matched.add(sym_id)

    return list(matched)
