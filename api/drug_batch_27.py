"""drug_batch_27.py - 薬物相互作用パッチ（第3弾）

残り142品の薬物相互作用を追加。外用薬/サプリ/IGRには「相互作用最小限」を明示。
"""

DRUG_INTERACTIONS_PATCH_27: dict[str, list[dict]] = {
    "adequan_equine": [
        {"drug": "Anticoagulants", "effect": "Additive anticoagulant effect (polysulfated GAG has heparin-like activity)", "severity": "moderate"}
    ],
    "afoxolaner": [
        {"drug": "No significant drug interactions", "effect": "Isoxazoline; highly protein-bound but no clinically relevant CYP interactions", "severity": "minor"}
    ],
    "alfaprostol": [
        {"drug": "NSAIDs", "effect": "May antagonize prostaglandin-mediated effects", "severity": "moderate"},
        {"drug": "Oxytocin", "effect": "Additive uterotonic effect", "severity": "moderate"}
    ],
    "cefixime": [
        {"drug": "Probenecid", "effect": "Reduces renal clearance; increases cefixime levels", "severity": "minor"},
        {"drug": "Aminoglycosides", "effect": "Synergistic bactericidal activity", "severity": "minor"}
    ],
    "domperidone_equine": [
        {"drug": "Ketoconazole", "effect": "Increases domperidone levels (CYP3A4 inhibition)", "severity": "moderate"},
        {"drug": "Anticholinergics", "effect": "Antagonizes prokinetic effect", "severity": "moderate"}
    ],
    "flumazenil": [
        {"drug": "Benzodiazepines", "effect": "Specific reversal agent; may precipitate seizures in benzodiazepine-dependent animals", "severity": "moderate"},
        {"drug": "Tricyclic antidepressants", "effect": "Unmasking of TCA-induced seizures after BZD reversal", "severity": "major"}
    ],
    "glycopyrrolate": [
        {"drug": "Other anticholinergics", "effect": "Additive anticholinergic effects", "severity": "moderate"},
        {"drug": "Metoclopramide", "effect": "Antagonizes prokinetic GI effects", "severity": "moderate"},
        {"drug": "Potassium chloride (oral)", "effect": "Delayed GI transit increases KCl ulceration risk", "severity": "moderate"}
    ],
    "griseofulvin": [
        {"drug": "Phenobarbital", "effect": "Reduces griseofulvin levels (CYP induction)", "severity": "moderate"},
        {"drug": "Warfarin", "effect": "Reduces anticoagulant effect", "severity": "moderate"},
        {"drug": "Cyclosporine", "effect": "May reduce cyclosporine levels", "severity": "moderate"}
    ],
    "gs441524": [
        {"drug": "No well-documented drug interactions", "effect": "Novel antiviral nucleoside analog; limited pharmacokinetic data", "severity": "minor"}
    ],
    "hydrochlorothiazide": [
        {"drug": "NSAIDs", "effect": "Reduced diuretic efficacy", "severity": "moderate"},
        {"drug": "Digoxin", "effect": "Hypokalemia increases digoxin toxicity", "severity": "major"},
        {"drug": "ACE inhibitors", "effect": "Additive hypotension (first-dose effect)", "severity": "moderate"},
        {"drug": "Lithium", "effect": "Reduced lithium clearance; toxicity risk", "severity": "major"}
    ],
    "ibuprofen": [
        {"drug": "Other NSAIDs", "effect": "Dramatically increased GI ulceration", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Increased GI toxicity", "severity": "major"},
        {"drug": "Anticoagulants", "effect": "Increased bleeding risk", "severity": "major"},
        {"drug": "ACE inhibitors", "effect": "Reduced antihypertensive effect; renal risk", "severity": "moderate"}
    ],
    "interferon_omega": [
        {"drug": "Immunosuppressants", "effect": "May antagonize immunostimulatory effects of interferon", "severity": "moderate"}
    ],
    "latanoprost": [
        {"drug": "Atropine ophthalmic", "effect": "Opposing effects on pupil size", "severity": "minor"},
        {"drug": "NSAIDs ophthalmic", "effect": "May slightly reduce prostaglandin-mediated IOP reduction", "severity": "minor"}
    ],
    "levofloxacin": [
        {"drug": "Antacids (Al/Mg)", "effect": "Chelation dramatically reduces absorption", "severity": "major"},
        {"drug": "Theophylline", "effect": "Increases theophylline levels", "severity": "moderate"},
        {"drug": "NSAIDs", "effect": "Increased seizure risk", "severity": "moderate"},
        {"drug": "Warfarin", "effect": "May increase anticoagulant effect", "severity": "moderate"}
    ],
    "lokivetmab": [
        {"drug": "No significant drug interactions", "effect": "Anti-IL-31 monoclonal antibody; no CYP metabolism", "severity": "minor"}
    ],
    "librela": [
        {"drug": "No significant drug interactions", "effect": "Anti-NGF monoclonal antibody; no hepatic metabolism", "severity": "minor"},
        {"drug": "NSAIDs", "effect": "Can be used concurrently; may allow NSAID dose reduction", "severity": "minor"}
    ],
    "lomustine": [
        {"drug": "Other myelosuppressive drugs", "effect": "Additive/delayed bone marrow suppression (nadir 4-6 weeks)", "severity": "major"},
        {"drug": "Live vaccines", "effect": "Immunosuppression; vaccine-disease risk", "severity": "major"}
    ],
    "marbofloxacin": [
        {"drug": "Antacids/cations (Ca/Mg/Fe/Al)", "effect": "Chelation reduces absorption 50%+", "severity": "major"},
        {"drug": "Theophylline", "effect": "May increase theophylline levels", "severity": "moderate"},
        {"drug": "NSAIDs", "effect": "Increased seizure risk (fluoroquinolone class)", "severity": "moderate"}
    ],
    "maropitant": [
        {"drug": "Highly protein-bound drugs", "effect": "Theoretical displacement; clinically minimal", "severity": "minor"}
    ],
    "medetomidine_vatinoxan": [
        {"drug": "Opioids", "effect": "Additive sedation; reduces cardiovascular depression (vatinoxan component)", "severity": "moderate"},
        {"drug": "Atipamezole", "effect": "Specific alpha-2 reversal agent", "severity": "minor"}
    ],
    "milbemycin_oxime": [
        {"drug": "P-glycoprotein inhibitors (ketoconazole, spinosad)", "effect": "Increased avermectin CNS penetration in MDR1-mutant dogs", "severity": "moderate"}
    ],
    "minocycline": [
        {"drug": "Antacids/cations", "effect": "Chelation reduces absorption (less than older tetracyclines)", "severity": "moderate"},
        {"drug": "Retinoids", "effect": "Additive risk of pseudotumor cerebri", "severity": "moderate"},
        {"drug": "Warfarin", "effect": "May enhance anticoagulant effect", "severity": "moderate"}
    ],
    "misoprostol": [
        {"drug": "NSAIDs", "effect": "Gastroprotective; intended co-administration", "severity": "minor"},
        {"drug": "Oxytocin", "effect": "Synergistic uterotonic; avoid in pregnancy", "severity": "major"}
    ],
    "molnupiravir": [
        {"drug": "No well-documented veterinary interactions", "effect": "Limited veterinary pharmacokinetic data available", "severity": "minor"}
    ],
    "moxidectin": [
        {"drug": "P-glycoprotein inhibitors", "effect": "Increased CNS penetration in MDR1-mutant dogs; neurotoxicity risk", "severity": "major"},
        {"drug": "Spinosad", "effect": "Reports of increased avermectin toxicity risk", "severity": "moderate"}
    ],
    "neo_poly_dex_ophthalmic": [
        {"drug": "Other ophthalmic drugs", "effect": "Space 5 minutes between drops", "severity": "minor"}
    ],
    "nitenpyram_oral": [
        {"drug": "No significant drug interactions", "effect": "Rapid-kill adulticide with minimal systemic interactions", "severity": "minor"}
    ],
    "ondansetron": [
        {"drug": "Tramadol", "effect": "Reduces tramadol analgesic effect", "severity": "moderate"},
        {"drug": "Apomorphine", "effect": "Antagonizes emetic effect of apomorphine", "severity": "moderate"}
    ],
    "orbifloxacin": [
        {"drug": "Antacids/cations", "effect": "Chelation reduces absorption", "severity": "major"},
        {"drug": "NSAIDs", "effect": "Increased seizure risk (fluoroquinolone class)", "severity": "moderate"}
    ],
    "ponazuril": [
        {"drug": "No significant drug interactions", "effect": "Triazine antiprotozoal with minimal systemic interactions", "severity": "minor"}
    ],
    "pradofloxacin": [
        {"drug": "Antacids (Mg/Al)", "effect": "Chelation reduces absorption", "severity": "moderate"},
        {"drug": "Theophylline", "effect": "May increase theophylline levels", "severity": "moderate"}
    ],
    "ronidazole": [
        {"drug": "Metronidazole", "effect": "Additive neurotoxicity risk; do not combine", "severity": "major"},
        {"drug": "Alcohol", "effect": "Disulfiram-like reaction (nitroimidazole class)", "severity": "moderate"}
    ],
    "sarolaner_oral": [
        {"drug": "No significant drug interactions", "effect": "Isoxazoline; no clinically relevant CYP interactions at label dose", "severity": "minor"}
    ],
    "toltrazuril": [
        {"drug": "No significant drug interactions", "effect": "Anticoccidial with minimal systemic interactions", "severity": "minor"}
    ],
    "timolol_ophthalmic": [
        {"drug": "Systemic beta-blockers", "effect": "Additive bradycardia and hypotension from ocular absorption", "severity": "major"},
        {"drug": "Calcium channel blockers (verapamil)", "effect": "Additive cardiac depression", "severity": "moderate"}
    ],
    "dextromethorphan": [
        {"drug": "MAO inhibitors", "effect": "Serotonin syndrome risk", "severity": "major"},
        {"drug": "SSRIs", "effect": "Increased serotonergic effects", "severity": "moderate"}
    ],
    "fuzapladib": [
        {"drug": "No well-documented drug interactions", "effect": "Novel leukocyte adhesion inhibitor; limited interaction data", "severity": "minor"}
    ],
    "cabergoline_prolactin": [
        {"drug": "Metoclopramide", "effect": "Dopamine antagonist opposes cabergoline effect", "severity": "major"},
        {"drug": "Phenothiazines", "effect": "Dopamine antagonism reduces efficacy", "severity": "moderate"}
    ],
    "deslorelin": [
        {"drug": "No significant drug interactions", "effect": "GnRH agonist implant; peptide with no CYP interaction", "severity": "minor"}
    ],
    "deslorelin_implant": [
        {"drug": "No significant drug interactions", "effect": "GnRH agonist implant; minimal systemic interactions", "severity": "minor"}
    ],
    "deslorelin_reproductive": [
        {"drug": "No significant drug interactions", "effect": "GnRH agonist implant; no CYP metabolism", "severity": "minor"}
    ],
    # Topicals, supplements, and nutritional support — minimal interactions
    "acriflavine": [
        {"drug": "No significant systemic interactions", "effect": "Topical antiseptic for aquarium use", "severity": "minor"}
    ],
    "aquarium_salt": [
        {"drug": "No significant drug interactions", "effect": "Supportive electrolyte for fish; not a pharmaceutical", "severity": "minor"}
    ],
    "artificial_tears": [
        {"drug": "Other ophthalmic drugs", "effect": "Space 5 minutes between eye drops", "severity": "minor"}
    ],
    "chlorhexidine": [
        {"drug": "No significant systemic interactions", "effect": "Topical antiseptic with negligible absorption", "severity": "minor"}
    ],
    "chlorhexidine_topical": [
        {"drug": "No significant systemic interactions", "effect": "Topical antiseptic/shampoo; not systemically absorbed", "severity": "minor"}
    ],
    "cobalamin_injection": [
        {"drug": "Chloramphenicol", "effect": "May reduce hematologic response to B12", "severity": "minor"}
    ],
    "copper_sulfate": [
        {"drug": "No significant systemic interactions", "effect": "Aquatic antiparasitic bath treatment", "severity": "minor"}
    ],
    "cranberry_extract": [
        {"drug": "Warfarin", "effect": "Case reports of increased INR; monitor", "severity": "moderate"}
    ],
    "critical_care_herbivore": [
        {"drug": "No significant drug interactions", "effect": "Nutritional support product; not a pharmaceutical", "severity": "minor"}
    ],
    "carnivore_care": [
        {"drug": "No significant drug interactions", "effect": "Nutritional support product; not a pharmaceutical", "severity": "minor"}
    ],
    "emeraid_ic": [
        {"drug": "No significant drug interactions", "effect": "Intensive care nutritional support; not a pharmaceutical", "severity": "minor"}
    ],
    "epsom_salt": [
        {"drug": "No significant drug interactions", "effect": "Magnesium sulfate bath for fish; negligible interaction", "severity": "minor"}
    ],
    "calcium_glubionate": [
        {"drug": "Tetracyclines", "effect": "Chelation reduces tetracycline absorption", "severity": "moderate"},
        {"drug": "Digoxin", "effect": "Hypercalcemia increases digoxin toxicity", "severity": "major"}
    ],
    "calcium_supplement_reptile": [
        {"drug": "Tetracyclines", "effect": "Chelation reduces absorption; space feeding times", "severity": "moderate"}
    ],
    "cyclopentolate": [
        {"drug": "Pilocarpine", "effect": "Antagonistic—opposing effects on pupil and ciliary muscle", "severity": "moderate"}
    ],
    "ciprofloxacin_ophthalmic": [
        {"drug": "Other ophthalmic drugs", "effect": "Space 5 minutes between eye drops", "severity": "minor"}
    ],
    "erythromycin_ophthalmic": [
        {"drug": "No significant systemic interactions", "effect": "Ophthalmic ointment with minimal absorption", "severity": "minor"}
    ],
    "amikacin_ophthalmic": [
        {"drug": "Other ophthalmic drugs", "effect": "Space 5 minutes between drops", "severity": "minor"}
    ],
    "aluminum_sucrose": [
        {"drug": "No significant drug interactions", "effect": "Phosphate binder; acts locally in GI tract", "severity": "minor"}
    ],
    "eprinomectin_topical": [
        {"drug": "P-glycoprotein inhibitors", "effect": "Theoretical increased CNS penetration in MDR1 dogs", "severity": "moderate"}
    ],
    "esafoxolaner": [
        {"drug": "No significant drug interactions", "effect": "Isoxazoline; no clinically relevant interactions at label dose", "severity": "minor"}
    ],
    "formalin_fish": [
        {"drug": "No significant drug interactions", "effect": "External aquatic parasite treatment", "severity": "minor"}
    ],
    "fipronil_spray": [
        {"drug": "No significant drug interactions", "effect": "Topical ectoparasiticide; minimal systemic absorption", "severity": "minor"}
    ],
    "imidacloprid": [
        {"drug": "No significant drug interactions", "effect": "Topical neonicotinoid with minimal systemic absorption", "severity": "minor"}
    ],
    "emodepside": [
        {"drug": "No significant drug interactions", "effect": "Topical anthelmintic with minimal interactions", "severity": "minor"}
    ],
    "ecvn_for_joint": [
        {"drug": "Warfarin", "effect": "Glucosamine component may affect INR; monitor", "severity": "minor"}
    ],
    "ecvn_amino_complete": [
        {"drug": "No significant drug interactions", "effect": "Amino acid supplement; minimal pharmacological interactions", "severity": "minor"}
    ],
    "ecvn_booster_relax": [
        {"drug": "No significant drug interactions", "effect": "Nutritional supplement with adaptogenic herbs", "severity": "minor"}
    ],
    "ecvn_for_antioxidant": [
        {"drug": "No significant drug interactions", "effect": "Antioxidant supplement; minimal pharmacological interactions", "severity": "minor"}
    ],
    "ecvn_kamide_milk": [
        {"drug": "No significant drug interactions", "effect": "Liquid nutrition supplement", "severity": "minor"}
    ],
    "ecvn_msm_amino_complete": [
        {"drug": "Warfarin", "effect": "Theoretical: MSM may affect blood clotting; monitor", "severity": "minor"}
    ],
    "ecvn_nmn_mito_assist": [
        {"drug": "No significant drug interactions", "effect": "NMN supplement; limited pharmacokinetic data", "severity": "minor"}
    ],
    "ecvn_no_pain_quick_stop": [
        {"drug": "No significant systemic interactions", "effect": "Topical hemostatic product", "severity": "minor"}
    ],
    "ecvn_protain": [
        {"drug": "No significant drug interactions", "effect": "Protein supplement; not a pharmaceutical", "severity": "minor"}
    ],
    "glucosamine": [
        {"drug": "Warfarin", "effect": "Case reports of increased INR", "severity": "moderate"}
    ],
    "lysine": [
        {"drug": "No significant drug interactions", "effect": "Amino acid supplement for feline herpesvirus", "severity": "minor"}
    ],
}

# 追加パッチ: 残りの薬品
DRUG_INTERACTIONS_PATCH_27B: dict[str, list[dict]] = {
    "carnidazole": [
        {"drug": "Other nitroimidazoles", "effect": "Do not combine; additive neurotoxicity", "severity": "major"}
    ],
    "emodepside_topical": [
        {"drug": "No significant drug interactions", "effect": "Topical anthelmintic with minimal systemic interactions", "severity": "minor"}
    ],
    "heparin_laminitis": [
        {"drug": "NSAIDs", "effect": "Increased bleeding risk", "severity": "major"},
        {"drug": "Aspirin", "effect": "Additive anticoagulant effect", "severity": "major"}
    ],
    "imidacloprid_moxidectin": [
        {"drug": "P-glycoprotein inhibitors", "effect": "May increase moxidectin CNS levels in MDR1 dogs", "severity": "moderate"}
    ],
    "kanamycin_fish": [
        {"drug": "No significant drug interactions", "effect": "Aquatic antibiotic bath treatment", "severity": "minor"}
    ],
    "ketoconazole_shampoo": [
        {"drug": "No significant systemic interactions", "effect": "Topical antifungal shampoo; negligible absorption", "severity": "minor"}
    ],
    "levamisole_fish": [
        {"drug": "No significant drug interactions", "effect": "Aquatic anthelmintic treatment", "severity": "minor"}
    ],
    "lotilaner_oral": [
        {"drug": "No significant drug interactions", "effect": "Isoxazoline; no clinically relevant CYP interactions", "severity": "minor"}
    ],
    "lufenuron": [
        {"drug": "No significant drug interactions", "effect": "IGR with no systemic activity in mammals", "severity": "minor"}
    ],
    "malachite_green": [
        {"drug": "Formalin", "effect": "Often used in combination for fish parasites (safe combination)", "severity": "minor"}
    ],
    "maropitant_travel": [
        {"drug": "Highly protein-bound drugs", "effect": "Theoretical displacement; clinically minimal", "severity": "minor"}
    ],
    "melatonin": [
        {"drug": "Sedatives", "effect": "Theoretical additive sedation", "severity": "minor"},
        {"drug": "Immunosuppressants", "effect": "Melatonin has immunomodulatory properties", "severity": "minor"}
    ],
    "miconazole": [
        {"drug": "Warfarin", "effect": "Topical miconazole can increase INR even with minimal absorption", "severity": "moderate"}
    ],
    "miconazole_chlorhex": [
        {"drug": "No significant systemic interactions", "effect": "Topical combination; negligible systemic absorption", "severity": "minor"}
    ],
    "miconazole_topical": [
        {"drug": "Warfarin", "effect": "Topical miconazole may slightly increase INR", "severity": "minor"}
    ],
    "milbemycin_praziquantel": [
        {"drug": "P-glycoprotein inhibitors", "effect": "Increased milbemycin CNS penetration in MDR1 dogs", "severity": "moderate"}
    ],
    "natamycin_ophthalmic": [
        {"drug": "No significant drug interactions", "effect": "Ophthalmic antifungal with minimal systemic absorption", "severity": "minor"}
    ],
    "nitenpyram": [
        {"drug": "No significant drug interactions", "effect": "Rapid-acting insecticide with minimal systemic interactions", "severity": "minor"}
    ],
    "nystatin": [
        {"drug": "No significant systemic interactions", "effect": "Not absorbed from GI tract; acts locally", "severity": "minor"}
    ],
    "omega3": [
        {"drug": "Anticoagulants", "effect": "High doses may increase bleeding risk", "severity": "moderate"}
    ],
    "oxytetracycline": [
        {"drug": "Antacids/cations", "effect": "Chelation dramatically reduces absorption", "severity": "major"},
        {"drug": "Penicillins", "effect": "Bacteriostatic may antagonize bactericidal effect", "severity": "moderate"}
    ],
    "oxytetracycline_injectable": [
        {"drug": "Penicillins", "effect": "Bacteriostatic may antagonize bactericidal activity", "severity": "moderate"},
        {"drug": "Nephrotoxic drugs", "effect": "Additive nephrotoxicity with high-dose tetracyclines", "severity": "moderate"}
    ],
    "oxytocin": [
        {"drug": "Prostaglandins", "effect": "Synergistic uterotonic effect", "severity": "moderate"},
        {"drug": "Vasopressors", "effect": "Potentiated hypertensive response", "severity": "moderate"}
    ],
    "oxytocin_reproductive": [
        {"drug": "Prostaglandins", "effect": "Synergistic uterotonic effect", "severity": "moderate"}
    ],
    "penicillin_g": [
        {"drug": "Tetracyclines", "effect": "Bacteriostatic may antagonize penicillin's bactericidal effect", "severity": "moderate"},
        {"drug": "Probenecid", "effect": "Increases penicillin levels (reduced clearance)", "severity": "minor"},
        {"drug": "Aminoglycosides", "effect": "Synergistic bactericidal; do not mix in same syringe", "severity": "minor"}
    ],
    "pepcid_antacid": [
        {"drug": "Ketoconazole/itraconazole", "effect": "Reduced absorption (need acid pH)", "severity": "moderate"}
    ],
    "permethrin": [
        {"drug": "No significant drug interactions in dogs", "effect": "TOXIC TO CATS—never apply to or near cats", "severity": "minor"}
    ],
    "phenoxymethylpenicillin": [
        {"drug": "Tetracyclines", "effect": "Bacteriostatic may reduce bactericidal effect", "severity": "moderate"},
        {"drug": "Probenecid", "effect": "Increases penicillin levels", "severity": "minor"}
    ],
    "phenylbutazone": [
        {"drug": "Other NSAIDs", "effect": "Dramatically increased GI ulceration", "severity": "major"},
        {"drug": "Warfarin", "effect": "Protein binding displacement; severe bleeding risk", "severity": "major"},
        {"drug": "Phenytoin", "effect": "Displaces phenytoin from protein binding", "severity": "major"}
    ],
    "phenylephrine_ophthalmic": [
        {"drug": "MAO inhibitors", "effect": "Potentiated pressor response from systemic absorption", "severity": "moderate"}
    ],
    "poloxamer_407": [
        {"drug": "No significant drug interactions", "effect": "Wound care product; no systemic effects", "severity": "minor"}
    ],
    "polymyxin_b": [
        {"drug": "Aminoglycosides", "effect": "Additive nephro- and neurotoxicity", "severity": "major"},
        {"drug": "Neuromuscular blockers", "effect": "Additive neuromuscular blockade", "severity": "major"}
    ],
    "potassium_permanganate": [
        {"drug": "No significant drug interactions", "effect": "External oxidizing bath for fish/aquatic use", "severity": "minor"}
    ],
    "prednisolone_lymphoma": [
        {"drug": "NSAIDs", "effect": "Dramatically increased GI ulceration risk", "severity": "major"},
        {"drug": "Live vaccines", "effect": "Immunosuppression; vaccine-disease risk", "severity": "major"},
        {"drug": "Insulin", "effect": "Antagonizes insulin; dose adjustment needed", "severity": "major"}
    ],
    "propofol": [
        {"drug": "Opioids", "effect": "Synergistic CNS depression; reduce propofol dose", "severity": "moderate"},
        {"drug": "Benzodiazepines", "effect": "Reduces propofol requirement 20-50%", "severity": "moderate"},
        {"drug": "Alpha-2 agonists", "effect": "Additive hypotension and CNS depression", "severity": "moderate"}
    ],
    "prostaglandin_f2a": [
        {"drug": "NSAIDs", "effect": "Prostaglandin synthesis inhibitors may reduce PGF2α effects", "severity": "moderate"},
        {"drug": "Oxytocin", "effect": "Synergistic uterotonic effect", "severity": "moderate"}
    ],
    "robenacoxib": [
        {"drug": "Other NSAIDs", "effect": "Never combine; GI ulceration risk", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Increased GI toxicity", "severity": "major"}
    ],
    "romifidine": [
        {"drug": "Opioids", "effect": "Synergistic sedation in horses", "severity": "moderate"},
        {"drug": "IV potentiated sulfonamides", "effect": "Fatal dysrhythmias (alpha-2 class in horses)", "severity": "major"},
        {"drug": "Atipamezole", "effect": "Specific reversal agent", "severity": "minor"}
    ],
    "sab_antivenom": [
        {"drug": "No significant drug interactions", "effect": "Fab antivenom fragments; supportive therapy", "severity": "minor"}
    ],
    "same": [
        {"drug": "No clinically significant interactions", "effect": "Hepatoprotectant supplement", "severity": "minor"}
    ],
    "sardine_oil": [
        {"drug": "Anticoagulants", "effect": "High omega-3 doses may slightly increase bleeding risk", "severity": "minor"}
    ],
    "sarolaner": [
        {"drug": "No significant drug interactions", "effect": "Isoxazoline class; no CYP interactions at label dose", "severity": "minor"}
    ],
    "selamectin": [
        {"drug": "No significant drug interactions", "effect": "Topical avermectin; safe at label dose even in MDR1 dogs", "severity": "minor"}
    ],
    "selamectin_sarolaner": [
        {"drug": "No significant drug interactions", "effect": "Topical combination; no clinically relevant interactions", "severity": "minor"}
    ],
    "selenium_vitamin_e": [
        {"drug": "No significant drug interactions", "effect": "Nutritional supplement; minimal pharmacological interactions", "severity": "minor"}
    ],
    "sevoflurane": [
        {"drug": "Epinephrine/catecholamines", "effect": "Cardiac sensitization; arrhythmia risk (less than halothane)", "severity": "moderate"},
        {"drug": "Non-depolarizing NMBAs", "effect": "Potentiates neuromuscular blockade", "severity": "moderate"}
    ],
    "silver_honey": [
        {"drug": "No significant drug interactions", "effect": "Topical wound care product", "severity": "minor"}
    ],
    "silver_sulfadiazine_cream": [
        {"drug": "Enzymatic debriding agents", "effect": "Silver may inactivate papain/collagenase", "severity": "moderate"}
    ],
    "solensia": [
        {"drug": "No significant drug interactions", "effect": "Anti-NGF monoclonal antibody; no hepatic metabolism", "severity": "minor"}
    ],
    "spinosad": [
        {"drug": "Ivermectin", "effect": "Reports of increased ivermectin toxicity in MDR1 dogs", "severity": "major"}
    ],
    "spironolactone": [
        {"drug": "ACE inhibitors", "effect": "Additive hyperkalemia", "severity": "major"},
        {"drug": "Potassium supplements", "effect": "Severe hyperkalemia risk", "severity": "major"},
        {"drug": "Digoxin", "effect": "May increase digoxin levels", "severity": "moderate"}
    ],
    "sulfasalazine": [
        {"drug": "Digoxin", "effect": "May reduce digoxin absorption", "severity": "moderate"},
        {"drug": "Folic acid", "effect": "Sulfasalazine reduces folate absorption", "severity": "minor"}
    ],
    "tacrolimus_ophthalmic": [
        {"drug": "No significant systemic interactions", "effect": "Ophthalmic formulation; minimal systemic absorption", "severity": "minor"}
    ],
    "tadalafil": [
        {"drug": "Nitrates", "effect": "Severe hypotension; contraindicated", "severity": "major"},
        {"drug": "Alpha-blockers", "effect": "Additive hypotension", "severity": "major"}
    ],
    "theophylline": [
        {"drug": "Fluoroquinolones (enrofloxacin)", "effect": "Increases theophylline levels", "severity": "moderate"},
        {"drug": "Cimetidine", "effect": "Increases theophylline levels", "severity": "moderate"},
        {"drug": "Phenobarbital", "effect": "Decreases theophylline levels", "severity": "moderate"}
    ],
    "thyroxine_monitoring": [
        {"drug": "No drug interactions", "effect": "Diagnostic monitoring; not a therapeutic agent", "severity": "minor"}
    ],
    "tobramycin_ophthalmic": [
        {"drug": "Other ophthalmic drugs", "effect": "Space 5 minutes between drops", "severity": "minor"}
    ],
    "tramadol_lactation": [
        {"drug": "SSRIs", "effect": "Serotonin syndrome risk", "severity": "major"},
        {"drug": "MAO inhibitors", "effect": "Severe serotonin syndrome", "severity": "major"}
    ],
    "tranexamic_acid": [
        {"drug": "Thrombolytics", "effect": "Antagonizes thrombolytic effect", "severity": "major"},
        {"drug": "Estrogens", "effect": "Additive thrombotic risk", "severity": "moderate"}
    ],
    "trichlorfon": [
        {"drug": "Other organophosphates", "effect": "Additive cholinesterase inhibition; toxicity", "severity": "major"}
    ],
    "tropicamide_ophthalmic": [
        {"drug": "Pilocarpine", "effect": "Antagonistic—opposing effects on pupil", "severity": "moderate"}
    ],
    "tylosin": [
        {"drug": "Chloramphenicol", "effect": "Competitive ribosomal binding; antagonism", "severity": "moderate"},
        {"drug": "Digoxin", "effect": "May increase digoxin levels (gut flora alteration)", "severity": "moderate"}
    ],
    "uvb_therapy": [
        {"drug": "Photosensitizing drugs (tetracyclines, fluoroquinolones)", "effect": "Increased photosensitivity reaction risk", "severity": "moderate"}
    ],
    "vitamin_a_injectable": [
        {"drug": "Retinoids (isotretinoin)", "effect": "Additive vitamin A toxicity", "severity": "major"},
        {"drug": "Warfarin", "effect": "High-dose vitamin A may increase INR", "severity": "moderate"}
    ],
    "vitamin_b12": [
        {"drug": "Chloramphenicol", "effect": "May reduce hematologic response to B12", "severity": "minor"}
    ],
    "vitamin_c_guinea_pig": [
        {"drug": "No significant drug interactions", "effect": "Essential dietary supplement for guinea pigs", "severity": "minor"}
    ],
    "voriconazole": [
        {"drug": "Cyclosporine", "effect": "Doubles cyclosporine levels (potent CYP3A4 inhibitor)", "severity": "major"},
        {"drug": "Sirolimus", "effect": "Dramatically increases sirolimus levels", "severity": "major"},
        {"drug": "Rifampin", "effect": "Reduces voriconazole levels 95%; contraindicated", "severity": "major"},
        {"drug": "Phenobarbital", "effect": "Reduces voriconazole levels significantly", "severity": "major"}
    ],
    "voriconazole_ophthalmic": [
        {"drug": "Other ophthalmic drugs", "effect": "Space 5 minutes between drops", "severity": "minor"}
    ],
    "xylazine": [
        {"drug": "Opioids", "effect": "Synergistic sedation; reduce both doses", "severity": "moderate"},
        {"drug": "IV potentiated sulfonamides", "effect": "Fatal arrhythmias in horses (alpha-2 class)", "severity": "major"},
        {"drug": "Epinephrine", "effect": "Potentiates hypertension and arrhythmias", "severity": "major"},
        {"drug": "Yohimbine/atipamezole", "effect": "Specific reversal agents", "severity": "minor"}
    ],
    "oxylinic_acid": [
        {"drug": "No significant drug interactions", "effect": "Aquatic antibiotic for fish", "severity": "minor"}
    ],
}
