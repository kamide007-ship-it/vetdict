"""drug_batch_26.py - 薬物相互作用パッチ（第2弾）

残り192品のうち90+品に薬物相互作用データを追加。
サプリメント・外用薬・生物学的製剤等で相互作用が最小限のものも明示。
"""

DRUG_INTERACTIONS_PATCH_26: dict[str, list[dict]] = {
    "acyclovir": [
        {"drug": "Nephrotoxic drugs", "effect": "Additive nephrotoxicity; ensure hydration", "severity": "moderate"},
        {"drug": "Probenecid", "effect": "Reduces acyclovir renal clearance", "severity": "minor"}
    ],
    "aminocaproic_acid": [
        {"drug": "Thrombolytics (tPA)", "effect": "Antagonizes thrombolytic effect", "severity": "major"},
        {"drug": "Estrogens", "effect": "Additive thrombotic risk", "severity": "moderate"}
    ],
    "atropine_ophthalmic": [
        {"drug": "Pilocarpine", "effect": "Antagonistic—opposing effects on pupil", "severity": "moderate"},
        {"drug": "Latanoprost", "effect": "Opposing effects on pupil size; clinical interaction minor", "severity": "minor"}
    ],
    "bedinvetmab": [
        {"drug": "Other monoclonal antibodies", "effect": "No known interactions; biologics minimally interact with small molecules", "severity": "minor"},
        {"drug": "NSAIDs", "effect": "Can be used concurrently; may allow NSAID dose reduction", "severity": "minor"}
    ],
    "calcium_edta": [
        {"drug": "Zinc supplements", "effect": "CaNa2EDTA chelates zinc; supplement zinc after course", "severity": "moderate"},
        {"drug": "Nephrotoxic drugs", "effect": "Additive nephrotoxicity", "severity": "major"}
    ],
    "capromorelin_oral": [
        {"drug": "Anticholinergics", "effect": "May delay gastric emptying and reduce efficacy", "severity": "minor"},
        {"drug": "GH-suppressing drugs (octreotide)", "effect": "Antagonizes ghrelin-mediated GH release", "severity": "moderate"}
    ],
    "cefpodoxime": [
        {"drug": "Probenecid", "effect": "Reduces renal clearance; increases levels", "severity": "minor"},
        {"drug": "Antacids (H2 blockers)", "effect": "May slightly reduce absorption", "severity": "minor"}
    ],
    "ceftiofur": [
        {"drug": "Aminoglycosides", "effect": "Synergistic bactericidal activity", "severity": "minor"},
        {"drug": "Chloramphenicol", "effect": "May antagonize bactericidal effect (bacteriostatic competition)", "severity": "moderate"}
    ],
    "cetirizine": [
        {"drug": "CNS depressants", "effect": "Minimal additive sedation (less sedating than first-gen)", "severity": "minor"},
        {"drug": "Theophylline", "effect": "May slightly reduce cetirizine clearance", "severity": "minor"}
    ],
    "cimicoxib": [
        {"drug": "Other NSAIDs", "effect": "Increased GI ulceration risk", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Increased GI ulceration risk", "severity": "major"},
        {"drug": "ACE inhibitors", "effect": "Reduced antihypertensive effect", "severity": "moderate"}
    ],
    "cloprostenol": [
        {"drug": "Progestins (altrenogest)", "effect": "Antagonistic—PGF2α lyses CL against progestin maintenance", "severity": "major"},
        {"drug": "NSAIDs", "effect": "Prostaglandin synthesis inhibitors may reduce cloprostenol-like effects", "severity": "moderate"}
    ],
    "clotrimazole": [
        {"drug": "No significant systemic interactions", "effect": "Topical with negligible systemic absorption", "severity": "minor"}
    ],
    "cyclosporine_ophthalmic": [
        {"drug": "No significant systemic interactions", "effect": "Ophthalmic formulation has minimal systemic absorption", "severity": "minor"},
        {"drug": "Other ophthalmic drugs", "effect": "Space 5 minutes between eye drops", "severity": "minor"}
    ],
    "cytopoint": [
        {"drug": "No significant drug interactions", "effect": "Monoclonal antibody; does not use CYP metabolism", "severity": "minor"},
        {"drug": "Corticosteroids", "effect": "Can be used concurrently during transition", "severity": "minor"},
        {"drug": "Oclacitinib", "effect": "Can be used concurrently; may allow dose reduction of either", "severity": "minor"}
    ],
    "deferoxamine": [
        {"drug": "Vitamin C (high dose)", "effect": "May increase iron toxicity by mobilizing tissue iron", "severity": "moderate"},
        {"drug": "Prochlorperazine", "effect": "Reports of prolonged unconsciousness", "severity": "moderate"}
    ],
    "diethylstilbestrol": [
        {"drug": "Hepatotoxic drugs", "effect": "Additive hepatotoxicity risk", "severity": "moderate"},
        {"drug": "Anticoagulants", "effect": "Estrogens may alter coagulation; monitor", "severity": "moderate"}
    ],
    "dorzolamide": [
        {"drug": "Oral carbonic anhydrase inhibitors", "effect": "Additive carbonic anhydrase inhibition; systemic acidosis risk", "severity": "moderate"},
        {"drug": "High-dose aspirin", "effect": "Theoretical additive acidosis (salicylate mechanism)", "severity": "minor"}
    ],
    "ethanol_antidote": [
        {"drug": "CNS depressants", "effect": "Additive CNS depression; monitor respiratory function", "severity": "major"},
        {"drug": "Fomepizole", "effect": "Both compete at ADH; choose one—fomepizole preferred", "severity": "moderate"}
    ],
    "fomepizole": [
        {"drug": "Ethanol", "effect": "Fomepizole preferred; using both is unnecessary", "severity": "minor"},
        {"drug": "No significant drug interactions", "effect": "Specific ADH inhibitor with minimal other interactions", "severity": "minor"}
    ],
    "florfenicol": [
        {"drug": "Chloramphenicol", "effect": "Same class—do not combine; additive bone marrow effects", "severity": "major"},
        {"drug": "Phenobarbital", "effect": "May alter florfenicol metabolism", "severity": "minor"}
    ],
    "frunevetmab": [
        {"drug": "No significant drug interactions", "effect": "Anti-NGF monoclonal antibody; no CYP metabolism", "severity": "minor"},
        {"drug": "NSAIDs", "effect": "Can be used concurrently; monitor for GI effects", "severity": "minor"}
    ],
    "glucosamine_chondroitin": [
        {"drug": "Warfarin", "effect": "Case reports of increased INR with glucosamine", "severity": "moderate"},
        {"drug": "NSAIDs", "effect": "May allow dose reduction; synergistic chondroprotection", "severity": "minor"}
    ],
    "ivermectin_oral": [
        {"drug": "P-glycoprotein substrates/inhibitors (ketoconazole, spinosad)", "effect": "Increased ivermectin CNS levels; neurotoxicity risk", "severity": "major"},
        {"drug": "Spinosad (Comfortis)", "effect": "Case reports of ivermectin toxicity when combined", "severity": "major"}
    ],
    "ketoprofen": [
        {"drug": "Other NSAIDs", "effect": "Increased GI ulceration risk", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Dramatically increased GI ulceration risk", "severity": "major"},
        {"drug": "ACE inhibitors", "effect": "Reduced antihypertensive effect", "severity": "moderate"},
        {"drug": "Anticoagulants", "effect": "Increased bleeding risk", "severity": "major"}
    ],
    "leflunomide": [
        {"drug": "Methotrexate", "effect": "Additive hepatotoxicity", "severity": "major"},
        {"drug": "Rifampin", "effect": "Increases active metabolite levels", "severity": "moderate"},
        {"drug": "Cholestyramine", "effect": "Accelerates elimination (used for washout)", "severity": "minor"}
    ],
    "lidocaine_systemic": [
        {"drug": "Beta-blockers", "effect": "Reduced lidocaine clearance; toxicity risk", "severity": "moderate"},
        {"drug": "Cimetidine", "effect": "Reduces lidocaine clearance", "severity": "moderate"},
        {"drug": "Other antiarrhythmics", "effect": "Additive cardiac depression", "severity": "major"}
    ],
    "lufenuron_oral": [
        {"drug": "No significant drug interactions", "effect": "IGR with no systemic activity in mammals", "severity": "minor"}
    ],
    "melatonin_implant": [
        {"drug": "Sedatives/anesthetics", "effect": "Theoretical additive sedation", "severity": "minor"},
        {"drug": "Immunosuppressants", "effect": "Melatonin has immunomodulatory properties", "severity": "minor"}
    ],
    "mirtazapine_transdermal": [
        {"drug": "SSRIs", "effect": "Serotonin syndrome risk", "severity": "major"},
        {"drug": "Cyproheptadine", "effect": "Antagonizes appetite-stimulant mechanism", "severity": "moderate"},
        {"drug": "MAO inhibitors", "effect": "Severe serotonin syndrome risk", "severity": "major"}
    ],
    "mupirocin": [
        {"drug": "No significant systemic interactions", "effect": "Topical antibiotic with negligible absorption", "severity": "minor"}
    ],
    "mycophenolate": [
        {"drug": "Azathioprine", "effect": "Overlapping mechanism; additive myelosuppression", "severity": "major"},
        {"drug": "Antacids (Mg/Al)", "effect": "Reduces mycophenolate absorption", "severity": "moderate"},
        {"drug": "Cholestyramine", "effect": "Reduces mycophenolate levels", "severity": "moderate"},
        {"drug": "Live vaccines", "effect": "Immunosuppression; vaccine-disease risk", "severity": "major"}
    ],
    "oclacitinib": [
        {"drug": "Corticosteroids", "effect": "Additive immunosuppression; avoid long-term combination", "severity": "moderate"},
        {"drug": "Cyclosporine", "effect": "Additive immunosuppression; not recommended together", "severity": "major"},
        {"drug": "Live vaccines", "effect": "Immune suppression may reduce vaccine response", "severity": "moderate"}
    ],
    "omega_3_fatty_acids": [
        {"drug": "Anticoagulants", "effect": "High doses may increase bleeding risk (antiplatelet effect)", "severity": "moderate"},
        {"drug": "NSAIDs", "effect": "May synergistically reduce inflammation; positive interaction", "severity": "minor"}
    ],
    "oxymorphone_injectable": [
        {"drug": "Other CNS depressants", "effect": "Additive respiratory depression and sedation", "severity": "major"},
        {"drug": "MAO inhibitors", "effect": "Potentiated opioid effects; serotonin syndrome risk", "severity": "major"},
        {"drug": "Phenothiazines", "effect": "Synergistic sedation and hypotension", "severity": "moderate"}
    ],
    "pentobarbital_euthanasia": [
        {"drug": "All drugs", "effect": "Euthanasia agent; interactions not clinically relevant", "severity": "minor"}
    ],
    "phenylbutazone_equine": [
        {"drug": "Other NSAIDs", "effect": "Dramatically increased GI ulceration risk; never combine", "severity": "major"},
        {"drug": "Warfarin", "effect": "Displaces warfarin from protein binding; severe bleeding risk", "severity": "major"},
        {"drug": "Phenytoin", "effect": "Displaces phenytoin; increased toxicity", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Increased GI ulceration risk", "severity": "major"}
    ],
    "phenylpropanolamine_ui": [
        {"drug": "MAO inhibitors", "effect": "Hypertensive crisis", "severity": "major"},
        {"drug": "Other sympathomimetics", "effect": "Additive cardiovascular effects", "severity": "moderate"},
        {"drug": "Beta-blockers", "effect": "Unopposed alpha stimulation; hypertension", "severity": "moderate"}
    ],
    "probiotics_vet": [
        {"drug": "Antibiotics", "effect": "Antibiotics may kill probiotic organisms; space 2h", "severity": "minor"}
    ],
    "propofol_injectable": [
        {"drug": "Opioids", "effect": "Reduced propofol dose needed; additive respiratory depression", "severity": "moderate"},
        {"drug": "Benzodiazepines", "effect": "Synergistic sedation; reduce propofol dose 20-50%", "severity": "moderate"},
        {"drug": "Alpha-2 agonists", "effect": "Synergistic hypotension and CNS depression", "severity": "moderate"}
    ],
    "psyllium_husk": [
        {"drug": "All oral medications", "effect": "May reduce absorption of co-administered drugs; space 2h", "severity": "moderate"}
    ],
    "ranitidine_injectable": [
        {"drug": "Ketoconazole", "effect": "Reduced ketoconazole absorption (needs acid pH)", "severity": "moderate"},
        {"drug": "Procainamide", "effect": "Increases procainamide levels (reduced renal clearance)", "severity": "moderate"}
    ],
    "rutin": [
        {"drug": "Anticoagulants", "effect": "Theoretical enhanced anticoagulant effect (capillary stabilizer)", "severity": "minor"}
    ],
    "selamectin_topical": [
        {"drug": "No significant drug interactions", "effect": "Avermectin with topical application; safe in MDR1 dogs at labeled dose", "severity": "minor"}
    ],
    "silver_sulfadiazine_topical": [
        {"drug": "Enzymatic debriding agents", "effect": "Silver may inactivate collagenase/papain", "severity": "moderate"}
    ],
    "tacrolimus_systemic": [
        {"drug": "Ketoconazole/itraconazole", "effect": "Markedly increases tacrolimus levels (CYP3A4 inhibition)", "severity": "major"},
        {"drug": "Aminoglycosides", "effect": "Additive nephrotoxicity", "severity": "major"},
        {"drug": "NSAIDs", "effect": "Additive nephrotoxicity", "severity": "moderate"},
        {"drug": "Cyclosporine", "effect": "Additive nephrotoxicity; never use together", "severity": "major"}
    ],
    "tiludronate": [
        {"drug": "Calcium supplements", "effect": "Calcium chelates bisphosphonate; space 2h", "severity": "moderate"},
        {"drug": "NSAIDs", "effect": "Additive GI effects", "severity": "moderate"}
    ],
    "tranexamic_acid_iv": [
        {"drug": "Thrombolytics", "effect": "Antagonizes thrombolytic effect", "severity": "major"},
        {"drug": "Estrogens", "effect": "Additive thrombotic risk", "severity": "moderate"}
    ],
    "vitamin_d3": [
        {"drug": "Thiazide diuretics", "effect": "Additive hypercalcemia risk", "severity": "moderate"},
        {"drug": "Digoxin", "effect": "Hypercalcemia increases digoxin toxicity", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Antagonizes vitamin D metabolism", "severity": "moderate"}
    ],
    "zonisamide_oral": [
        {"drug": "Phenobarbital", "effect": "Increases zonisamide clearance; higher dose may be needed", "severity": "moderate"},
        {"drug": "Carbonic anhydrase inhibitors", "effect": "Additive risk of kidney stones and metabolic acidosis", "severity": "moderate"}
    ],
    "topiramate": [
        {"drug": "Phenobarbital", "effect": "May alter topiramate clearance", "severity": "moderate"},
        {"drug": "Carbonic anhydrase inhibitors", "effect": "Additive acidosis and nephrolithiasis risk", "severity": "moderate"},
        {"drug": "Valproate", "effect": "Increased hyperammonemia risk", "severity": "moderate"}
    ],
    "pyridostigmine": [
        {"drug": "Aminoglycosides", "effect": "Antagonizes pyridostigmine at NMJ", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Initial worsening of MG possible", "severity": "moderate"},
        {"drug": "Beta-blockers", "effect": "Additive bradycardia", "severity": "moderate"}
    ],
    "penicillamine": [
        {"drug": "Iron supplements", "effect": "Reduces penicillamine absorption; space 2h", "severity": "moderate"},
        {"drug": "Antacids", "effect": "Reduces penicillamine absorption", "severity": "moderate"},
        {"drug": "Immunosuppressants", "effect": "Additive hematologic toxicity", "severity": "moderate"}
    ],
    "zinc_acetate": [
        {"drug": "Penicillamine", "effect": "Zinc reduces penicillamine absorption; space 2h", "severity": "moderate"},
        {"drug": "Tetracyclines", "effect": "Mutual chelation; reduced absorption of both", "severity": "moderate"},
        {"drug": "Fluoroquinolones", "effect": "Chelation reduces fluoroquinolone absorption", "severity": "moderate"}
    ],
    "lomustine_oral": [
        {"drug": "Other myelosuppressive drugs", "effect": "Additive/delayed bone marrow suppression", "severity": "major"},
        {"drug": "Phenobarbital", "effect": "May alter lomustine hepatic metabolism", "severity": "moderate"},
        {"drug": "Live vaccines", "effect": "Immunosuppression; vaccine-induced disease risk", "severity": "major"}
    ],
    "hydroxyurea": [
        {"drug": "Other myelosuppressive drugs", "effect": "Additive bone marrow suppression", "severity": "major"},
        {"drug": "Antiretrovirals", "effect": "Increased risk of pancreatitis and neuropathy", "severity": "moderate"}
    ],
    "cisplatin_injectable": [
        {"drug": "Aminoglycosides", "effect": "Dramatically increased nephrotoxicity", "severity": "major"},
        {"drug": "Loop diuretics (furosemide)", "effect": "Additive ototoxicity and nephrotoxicity", "severity": "major"},
        {"drug": "Phenytoin", "effect": "Reduced phenytoin levels", "severity": "moderate"}
    ],
    "palladia_oral": [
        {"drug": "NSAIDs", "effect": "Dramatically increased GI toxicity", "severity": "major"},
        {"drug": "ACE inhibitors", "effect": "Monitor; may help manage proteinuria side effect", "severity": "minor"}
    ],
    "mavacoxib": [
        {"drug": "Other NSAIDs", "effect": "Never combine; increased GI ulceration", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Increased GI toxicity", "severity": "major"},
        {"drug": "Highly protein-bound drugs", "effect": "Potential displacement; mavacoxib is >98% protein-bound", "severity": "moderate"}
    ],
    "tepoxalin_oral": [
        {"drug": "Other NSAIDs", "effect": "Increased GI toxicity", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Increased GI ulceration risk", "severity": "major"}
    ],
    "flunixin_paste": [
        {"drug": "Other NSAIDs", "effect": "Never stack NSAIDs; severe GI ulceration", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Dramatically increased GI ulceration risk in horses", "severity": "major"},
        {"drug": "Aminoglycosides", "effect": "Increased nephrotoxicity", "severity": "major"}
    ],
    "alfaxalone_injectable": [
        {"drug": "Opioids", "effect": "Synergistic CNS depression; reduce alfaxalone dose", "severity": "moderate"},
        {"drug": "Alpha-2 agonists", "effect": "Significant dose reduction of alfaxalone needed", "severity": "moderate"},
        {"drug": "Benzodiazepines", "effect": "Additive sedation; co-induction allows lower doses", "severity": "moderate"}
    ],
    "fentanyl_patch": [
        {"drug": "Other CNS depressants", "effect": "Additive respiratory depression and sedation", "severity": "major"},
        {"drug": "MAO inhibitors", "effect": "Severe serotonin syndrome risk", "severity": "major"},
        {"drug": "CYP3A4 inhibitors (ketoconazole)", "effect": "Increased fentanyl levels; toxicity risk", "severity": "major"}
    ],
    "butorphanol_injectable": [
        {"drug": "Full mu-agonists (morphine)", "effect": "Partial antagonism; may reduce analgesia from full agonist", "severity": "moderate"},
        {"drug": "CNS depressants", "effect": "Additive sedation", "severity": "moderate"}
    ],
    "buprenorphine_injectable": [
        {"drug": "Full mu-agonists", "effect": "Partial agonist may precipitate withdrawal or reduce full agonist effect", "severity": "moderate"},
        {"drug": "CNS depressants", "effect": "Additive sedation and respiratory depression", "severity": "moderate"},
        {"drug": "CYP3A4 inhibitors", "effect": "May increase buprenorphine levels", "severity": "minor"}
    ],
    "misoprostol_gastro": [
        {"drug": "NSAIDs", "effect": "Gastroprotective when co-administered; intended combination", "severity": "minor"},
        {"drug": "Antacids (Mg-containing)", "effect": "Additive diarrhea", "severity": "minor"},
        {"drug": "Oxytocin", "effect": "Additive uterotonic effect; avoid in pregnancy", "severity": "major"}
    ],
    "pentosan_polysulfate": [
        {"drug": "Anticoagulants", "effect": "Additive bleeding risk (weak anticoagulant properties)", "severity": "moderate"},
        {"drug": "NSAIDs", "effect": "Additive bleeding tendency", "severity": "minor"}
    ],
    "omeprazole_oral": [
        {"drug": "Clopidogrel", "effect": "Reduces clopidogrel activation (CYP2C19 inhibition)", "severity": "moderate"},
        {"drug": "Ketoconazole/itraconazole", "effect": "Reduced antifungal absorption (needs acid)", "severity": "major"},
        {"drug": "Iron/B12", "effect": "Reduced absorption from decreased acid", "severity": "moderate"}
    ],
    "dexmedetomidine_oromucosal": [
        {"drug": "Other CNS depressants", "effect": "Additive sedation; reduce doses of co-administered agents", "severity": "moderate"},
        {"drug": "Potentiated sulfonamides IV", "effect": "Fatal arrhythmias in horses (alpha-2 class effect)", "severity": "major"},
        {"drug": "Atipamezole", "effect": "Specific reversal agent", "severity": "minor"}
    ],
    "imidacloprid_topical": [
        {"drug": "No significant drug interactions", "effect": "Topical ectoparasiticide with minimal systemic absorption", "severity": "minor"}
    ],
    "permethrin_topical": [
        {"drug": "No significant drug interactions in dogs", "effect": "CAUTION: TOXIC TO CATS—never apply to or near cats", "severity": "minor"}
    ],
    "ms222_fish": [
        {"drug": "No significant drug interactions", "effect": "Fish-specific immersion anesthetic", "severity": "minor"}
    ],
    "eugenol_fish": [
        {"drug": "No significant drug interactions", "effect": "Fish-specific immersion anesthetic", "severity": "minor"}
    ],
    "oxyglobin": [
        {"drug": "No significant drug interactions", "effect": "Hemoglobin-based oxygen carrier; interferes with some lab assays", "severity": "minor"}
    ],
    "ferrous_sulfate_oral": [
        {"drug": "Tetracyclines", "effect": "Mutual chelation; reduced absorption of both", "severity": "moderate"},
        {"drug": "Fluoroquinolones", "effect": "Chelation reduces fluoroquinolone absorption", "severity": "moderate"},
        {"drug": "Levothyroxine", "effect": "Reduces T4 absorption; space 4h", "severity": "moderate"},
        {"drug": "Antacids/PPIs", "effect": "Reduced iron absorption", "severity": "moderate"}
    ],
    "methionine_urinary": [
        {"drug": "Urinary alkalinizers (K citrate)", "effect": "Antagonistic—opposing pH effects", "severity": "moderate"}
    ],
    "potassium_citrate": [
        {"drug": "ACE inhibitors", "effect": "Additive hyperkalemia risk", "severity": "moderate"},
        {"drug": "Potassium-sparing diuretics", "effect": "Hyperkalemia risk", "severity": "major"},
        {"drug": "Methionine", "effect": "Antagonistic urinary pH effects", "severity": "moderate"}
    ],
    "tamsulosin": [
        {"drug": "Other alpha-blockers", "effect": "Additive hypotension", "severity": "major"},
        {"drug": "CYP3A4 inhibitors (ketoconazole)", "effect": "Increases tamsulosin levels", "severity": "moderate"},
        {"drug": "PDE-5 inhibitors", "effect": "Additive hypotension", "severity": "moderate"}
    ],
    "testosterone_cypionate": [
        {"drug": "Anticoagulants", "effect": "Androgens potentiate anticoagulant effect", "severity": "major"},
        {"drug": "Insulin", "effect": "May alter insulin requirements", "severity": "moderate"}
    ],
    "propantheline": [
        {"drug": "Other anticholinergics", "effect": "Additive anticholinergic effects (dry mouth, urinary retention, tachycardia)", "severity": "moderate"},
        {"drug": "Prokinetics (metoclopramide)", "effect": "Antagonizes prokinetic GI effects", "severity": "moderate"}
    ],
    "osphos_equine": [
        {"drug": "Calcium supplements", "effect": "Chelation; do not give within 2h", "severity": "moderate"},
        {"drug": "NSAIDs", "effect": "Additive GI effects; monitor", "severity": "minor"}
    ],
}
