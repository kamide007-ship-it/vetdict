"""drug_batch_25.py - 薬物相互作用パッチ

既存薬品248品の薬物相互作用データを追加するパッチ。
"""

DRUG_INTERACTIONS_PATCH_25: dict[str, list[dict]] = {
    "acetaminophen": [
        {"drug": "NSAIDs", "effect": "Additive hepatotoxicity and GI risk", "severity": "major"},
        {"drug": "Phenobarbital", "effect": "Increased hepatotoxicity risk (enzyme induction)", "severity": "major"},
        {"drug": "Warfarin", "effect": "Enhanced anticoagulant effect", "severity": "moderate"},
    ],
    "alfaxalone": [
        {
            "drug": "Benzodiazepines",
            "effect": "Additive CNS/respiratory depression; reduced alfaxalone dose needed",
            "severity": "moderate",
        },
        {"drug": "Opioids", "effect": "Additive CNS depression; reduce alfaxalone dose 25-50%", "severity": "moderate"},
        {
            "drug": "Alpha-2 agonists",
            "effect": "Synergistic sedation; significantly reduce alfaxalone dose",
            "severity": "moderate",
        },
    ],
    "altrenogest": [
        {
            "drug": "Prostaglandins (PGF2α)",
            "effect": "Antagonistic—prostaglandins lyse CL, opposing progestagen effect",
            "severity": "major",
        },
        {"drug": "Oxytocin", "effect": "Progestins may reduce uterine response to oxytocin", "severity": "moderate"},
    ],
    "atenolol": [
        {
            "drug": "Calcium channel blockers (diltiazem)",
            "effect": "Additive bradycardia and AV block risk",
            "severity": "major",
        },
        {"drug": "Insulin", "effect": "May mask hypoglycemia signs (tachycardia)", "severity": "moderate"},
        {"drug": "NSAIDs", "effect": "May reduce antihypertensive effect", "severity": "moderate"},
    ],
    "atipamezole": [
        {
            "drug": "Opioids",
            "effect": "Reversal of alpha-2 component may unmask inadequate opioid analgesia",
            "severity": "moderate",
        },
        {
            "drug": "Ketamine",
            "effect": "Reversal may unmask ketamine-induced muscle rigidity/seizures",
            "severity": "major",
        },
    ],
    "amphotericin_b": [
        {"drug": "Aminoglycosides", "effect": "Additive nephrotoxicity", "severity": "major"},
        {"drug": "NSAIDs", "effect": "Additive nephrotoxicity", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Exacerbates hypokalemia", "severity": "moderate"},
        {"drug": "Digoxin", "effect": "Hypokalemia increases digoxin toxicity risk", "severity": "major"},
    ],
    "bosentan": [
        {"drug": "Cyclosporine", "effect": "Markedly increases bosentan levels; contraindicated", "severity": "major"},
        {"drug": "Sildenafil", "effect": "Bosentan reduces sildenafil levels; adjust dose", "severity": "moderate"},
        {"drug": "Warfarin", "effect": "Bosentan reduces warfarin effect (CYP induction)", "severity": "moderate"},
    ],
    "budesonide": [
        {
            "drug": "Ketoconazole",
            "effect": "Inhibits budesonide CYP3A4 metabolism; increased systemic exposure",
            "severity": "moderate",
        },
        {"drug": "NSAIDs", "effect": "Additive GI ulceration risk", "severity": "moderate"},
    ],
    "cabergoline": [
        {"drug": "Metoclopramide", "effect": "Dopamine antagonist opposes cabergoline effect", "severity": "major"},
        {
            "drug": "Phenothiazines",
            "effect": "Dopamine antagonism reduces cabergoline efficacy",
            "severity": "moderate",
        },
    ],
    "cefovecin": [
        {"drug": "Aminoglycosides", "effect": "Synergistic bactericidal activity", "severity": "minor"},
        {"drug": "Probenecid", "effect": "Prolongs cefovecin half-life further", "severity": "minor"},
    ],
    "cephalexin": [
        {
            "drug": "Aminoglycosides",
            "effect": "Additive nephrotoxicity risk with prolonged use",
            "severity": "moderate",
        },
        {"drug": "Probenecid", "effect": "Reduces renal clearance; increases cephalexin levels", "severity": "minor"},
    ],
    "chlorambucil": [
        {"drug": "Other myelosuppressive drugs", "effect": "Additive bone marrow suppression", "severity": "major"},
        {"drug": "Live vaccines", "effect": "Risk of vaccine-induced disease", "severity": "major"},
        {"drug": "Phenobarbital", "effect": "May alter chlorambucil metabolism", "severity": "moderate"},
    ],
    "ciprofloxacin": [
        {
            "drug": "Antacids (Al/Mg)",
            "effect": "Chelation reduces ciprofloxacin absorption by 90%",
            "severity": "major",
        },
        {"drug": "Theophylline", "effect": "Increases theophylline levels 15-30%", "severity": "moderate"},
        {"drug": "NSAIDs", "effect": "Increased seizure risk", "severity": "moderate"},
        {"drug": "Sucralfate", "effect": "Reduces absorption; give ciprofloxacin 2h before", "severity": "moderate"},
    ],
    "clenbuterol": [
        {"drug": "Beta-blockers", "effect": "Antagonizes bronchodilatory effect", "severity": "major"},
        {"drug": "Halothane/Isoflurane", "effect": "Cardiac sensitization to catecholamines", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Additive hypokalemia", "severity": "moderate"},
    ],
    "detomidine": [
        {"drug": "Opioids", "effect": "Synergistic sedation; reduce doses of both", "severity": "moderate"},
        {"drug": "Potentiated sulfonamides IV", "effect": "Fatal dysrhythmias reported in horses", "severity": "major"},
        {"drug": "Epinephrine", "effect": "Potentiates hypertension and arrhythmias", "severity": "major"},
    ],
    "diphenhydramine": [
        {"drug": "CNS depressants", "effect": "Additive sedation", "severity": "moderate"},
        {"drug": "MAO inhibitors", "effect": "Prolonged anticholinergic effects", "severity": "moderate"},
        {"drug": "Heparin", "effect": "May partially antagonize heparin effect", "severity": "minor"},
    ],
    "dobutamine": [
        {"drug": "Beta-blockers", "effect": "Antagonizes dobutamine cardiac effects", "severity": "major"},
        {"drug": "Halothane", "effect": "Ventricular arrhythmia risk", "severity": "major"},
        {"drug": "Calcium channel blockers", "effect": "May reduce positive inotropic effect", "severity": "moderate"},
    ],
    "dopamine": [
        {"drug": "MAO inhibitors", "effect": "Severe hypertensive crisis—reduce dose 90%", "severity": "major"},
        {"drug": "Phenothiazines", "effect": "Antagonizes dopamine vasopressor effect", "severity": "major"},
        {"drug": "Phenytoin", "effect": "Hypotension and bradycardia", "severity": "moderate"},
    ],
    "epinephrine": [
        {"drug": "Beta-blockers", "effect": "Unopposed alpha stimulation; severe hypertension", "severity": "major"},
        {
            "drug": "Halothane/Isoflurane",
            "effect": "Cardiac sensitization; ventricular arrhythmias",
            "severity": "major",
        },
        {"drug": "MAO inhibitors", "effect": "Potentiated pressor response", "severity": "major"},
        {"drug": "Digoxin", "effect": "Increased risk of ventricular arrhythmias", "severity": "major"},
    ],
    "erythropoietin": [
        {"drug": "ACE inhibitors", "effect": "May blunt EPO response", "severity": "moderate"},
        {"drug": "Iron supplements", "effect": "Required concurrent use for adequate response", "severity": "minor"},
    ],
    "famciclovir": [
        {"drug": "Probenecid", "effect": "Increases famciclovir levels (reduced renal clearance)", "severity": "minor"},
        {"drug": "Raltitrexed", "effect": "Increased toxicity risk", "severity": "moderate"},
    ],
    "fenbendazole": [
        {
            "drug": "Dexamethasone",
            "effect": "May reduce fenbendazole efficacy (immunosuppression)",
            "severity": "minor",
        },
        {"drug": "Praziquantel", "effect": "Often used in combination safely", "severity": "minor"},
    ],
    "fipronil": [
        {
            "drug": "No significant drug interactions",
            "effect": "Topical with minimal systemic absorption",
            "severity": "minor",
        }
    ],
    "flunixin": [
        {"drug": "Other NSAIDs", "effect": "Dramatically increased GI ulceration risk", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Dramatically increased GI ulceration risk", "severity": "major"},
        {"drug": "Aminoglycosides", "effect": "Increased nephrotoxicity", "severity": "major"},
        {"drug": "Anticoagulants", "effect": "Increased bleeding risk", "severity": "major"},
    ],
    "fluralaner": [
        {
            "drug": "No significant drug interactions",
            "effect": "Highly protein-bound but no clinically relevant interactions reported",
            "severity": "minor",
        }
    ],
    "fosfomycin": [
        {
            "drug": "Metoclopramide",
            "effect": "Reduces fosfomycin levels by increasing GI transit",
            "severity": "moderate",
        },
        {"drug": "Calcium supplements", "effect": "May reduce oral absorption", "severity": "minor"},
    ],
    "gabapentin_oral": [
        {"drug": "Opioids", "effect": "Additive CNS/respiratory depression", "severity": "moderate"},
        {"drug": "Antacids", "effect": "Reduce gabapentin absorption by 20%", "severity": "minor"},
    ],
    "hetastarch": [
        {"drug": "Aminoglycosides", "effect": "Potential additive nephrotoxicity", "severity": "moderate"},
        {"drug": "Coagulation factors", "effect": "Dilutional coagulopathy at high volumes", "severity": "moderate"},
    ],
    "hydrogen_peroxide_emetic": [
        {"drug": "Antiemetics", "effect": "Antagonizes emetic effect", "severity": "major"},
        {"drug": "Activated charcoal", "effect": "Give charcoal AFTER emesis is complete", "severity": "moderate"},
    ],
    "imipenem_cilastatin": [
        {"drug": "Ganciclovir", "effect": "Increased seizure risk", "severity": "major"},
        {"drug": "Valproic acid", "effect": "Drastically reduces valproate levels", "severity": "major"},
        {"drug": "Cyclosporine", "effect": "Increased neurotoxicity risk", "severity": "moderate"},
    ],
    "insulin_nph": [
        {"drug": "Corticosteroids", "effect": "Antagonizes insulin effect; increases glucose", "severity": "major"},
        {"drug": "Beta-blockers", "effect": "Masks hypoglycemia signs", "severity": "moderate"},
        {"drug": "ACE inhibitors", "effect": "May potentiate hypoglycemia", "severity": "moderate"},
    ],
    "insulin_pzi": [
        {"drug": "Corticosteroids", "effect": "Antagonizes insulin effect; hyperglycemia", "severity": "major"},
        {"drug": "Progesterone", "effect": "Insulin resistance in intact females", "severity": "moderate"},
    ],
    "iron_dextran": [
        {"drug": "Chloramphenicol", "effect": "May reduce iron utilization", "severity": "moderate"},
        {"drug": "ACE inhibitors", "effect": "Increased anaphylactoid reaction risk", "severity": "moderate"},
    ],
    "lactulose": [
        {"drug": "Antacids", "effect": "May reduce lactulose efficacy (alter colonic pH)", "severity": "minor"},
        {"drug": "Neomycin", "effect": "Synergistic for hepatic encephalopathy", "severity": "minor"},
    ],
    "levothyroxine": [
        {"drug": "Phenobarbital", "effect": "Increases T4 metabolism; may need higher dose", "severity": "moderate"},
        {"drug": "Calcium/Iron supplements", "effect": "Reduce absorption; give 4h apart", "severity": "moderate"},
        {"drug": "Corticosteroids", "effect": "May reduce T4-to-T3 conversion", "severity": "minor"},
    ],
    "mannitol_iv": [
        {"drug": "Loop diuretics", "effect": "Additive diuresis and risk of hypovolemia", "severity": "moderate"},
        {"drug": "Lithium", "effect": "Increased lithium excretion", "severity": "moderate"},
        {"drug": "Nephrotoxic drugs", "effect": "Increased nephrotoxicity risk if dehydrated", "severity": "moderate"},
    ],
    "maropitant_oral": [
        {"drug": "Highly protein-bound drugs", "effect": "Potential displacement; monitor", "severity": "minor"},
        {"drug": "Erythromycin", "effect": "CYP inhibition may increase maropitant levels", "severity": "minor"},
    ],
    "meropenem": [
        {"drug": "Valproic acid", "effect": "Drastically reduces valproate levels (50-80%)", "severity": "major"},
        {"drug": "Probenecid", "effect": "Increases meropenem levels and half-life", "severity": "minor"},
    ],
    "methimazole": [
        {"drug": "Phenobarbital", "effect": "May alter thyroid hormone metabolism", "severity": "minor"},
        {
            "drug": "Digoxin",
            "effect": "Correction of hyperthyroidism increases digoxin sensitivity",
            "severity": "moderate",
        },
        {
            "drug": "Warfarin",
            "effect": "Correction of hyperthyroidism alters anticoagulant requirement",
            "severity": "moderate",
        },
    ],
    "methylene_blue": [
        {
            "drug": "Serotonergic drugs (SSRIs)",
            "effect": "Serotonin syndrome (methylene blue is MAO-A inhibitor)",
            "severity": "major",
        }
    ],
    "metronidazole": [
        {"drug": "Phenobarbital", "effect": "Reduces metronidazole levels (enzyme induction)", "severity": "moderate"},
        {"drug": "Warfarin", "effect": "Increases anticoagulant effect", "severity": "major"},
        {"drug": "Cyclosporine", "effect": "May increase cyclosporine levels", "severity": "moderate"},
        {"drug": "Alcohol/ethanol", "effect": "Disulfiram-like reaction", "severity": "major"},
    ],
    "mirtazapine_oral": [
        {"drug": "SSRIs", "effect": "Serotonin syndrome risk", "severity": "major"},
        {
            "drug": "Cyproheptadine",
            "effect": "Serotonin antagonism may reduce appetite stimulant effect",
            "severity": "moderate",
        },
        {"drug": "Tramadol", "effect": "Serotonin syndrome risk", "severity": "moderate"},
    ],
    "naloxone": [
        {
            "drug": "All opioids",
            "effect": "Complete reversal of opioid effects; may precipitate withdrawal",
            "severity": "moderate",
        }
    ],
    "nitrofurantoin": [
        {"drug": "Antacids (Mg trisilicate)", "effect": "Reduces nitrofurantoin absorption", "severity": "moderate"},
        {"drug": "Probenecid", "effect": "Reduces urinary levels (decreased tubular secretion)", "severity": "major"},
    ],
    "n_acetylcysteine": [
        {"drug": "Activated charcoal", "effect": "Charcoal adsorbs NAC; give separately or IV", "severity": "major"},
        {"drug": "Nitroglycerin", "effect": "Enhanced hypotensive effect", "severity": "moderate"},
    ],
    "omeprazole_injectable": [
        {
            "drug": "Clopidogrel",
            "effect": "Reduces clopidogrel activation (CYP2C19 inhibition)",
            "severity": "moderate",
        },
        {"drug": "Ketoconazole", "effect": "Reduced ketoconazole absorption (needs acid pH)", "severity": "moderate"},
        {"drug": "Iron supplements", "effect": "Reduced iron absorption", "severity": "minor"},
    ],
    "ondansetron": [
        {"drug": "Tramadol", "effect": "Reduces analgesic effect of tramadol", "severity": "moderate"},
        {"drug": "Apomorphine", "effect": "Antagonizes emetic effect", "severity": "moderate"},
        {"drug": "QT-prolonging drugs", "effect": "Additive QT prolongation risk", "severity": "moderate"},
    ],
    "phenobarbital_oral": [
        {
            "drug": "Other CNS depressants",
            "effect": "Additive sedation and respiratory depression",
            "severity": "major",
        },
        {"drug": "Cyclosporine", "effect": "Reduces cyclosporine levels 50% (CYP induction)", "severity": "major"},
        {"drug": "Doxycycline", "effect": "Reduces doxycycline half-life (CYP induction)", "severity": "moderate"},
        {"drug": "Corticosteroids", "effect": "Accelerates steroid metabolism", "severity": "moderate"},
        {"drug": "Digoxin", "effect": "Reduces digoxin levels", "severity": "moderate"},
        {"drug": "Metronidazole", "effect": "Reduces metronidazole levels", "severity": "moderate"},
    ],
    "prednisolone": [
        {"drug": "NSAIDs", "effect": "Dramatically increased GI ulceration risk", "severity": "major"},
        {"drug": "Insulin", "effect": "Antagonizes insulin; hyperglycemia", "severity": "major"},
        {"drug": "Diuretics", "effect": "Additive hypokalemia", "severity": "moderate"},
        {"drug": "Phenobarbital", "effect": "Increases prednisolone metabolism", "severity": "moderate"},
        {"drug": "Live vaccines", "effect": "Immunosuppression may cause vaccine-induced disease", "severity": "major"},
    ],
    "rifampin": [
        {
            "drug": "Nearly all hepatically metabolized drugs",
            "effect": "Potent CYP inducer; reduces levels of most drugs",
            "severity": "major",
        },
        {"drug": "Cyclosporine", "effect": "Reduces cyclosporine levels dramatically", "severity": "major"},
        {"drug": "Ketoconazole", "effect": "Bidirectional interaction; both reduced", "severity": "major"},
        {"drug": "Doxycycline", "effect": "Reduces doxycycline levels 50%", "severity": "moderate"},
    ],
    "s_adenosylmethionine": [
        {"drug": "Serotonergic drugs", "effect": "Theoretical serotonin syndrome risk", "severity": "minor"},
        {
            "drug": "No clinically significant interactions",
            "effect": "Generally safe as hepatoprotectant supplement",
            "severity": "minor",
        },
    ],
    "selegiline": [
        {"drug": "SSRIs/TCAs", "effect": "Serotonin syndrome risk", "severity": "major"},
        {"drug": "Meperidine/tramadol", "effect": "Severe serotonin syndrome risk", "severity": "major"},
        {"drug": "Ephedrine/pseudoephedrine", "effect": "Hypertensive crisis", "severity": "major"},
    ],
    "sodium_bicarbonate": [
        {"drug": "Fluoroquinolones", "effect": "Alkalinization increases renal excretion", "severity": "minor"},
        {"drug": "Aspirin/salicylates", "effect": "Increases renal clearance of salicylates", "severity": "moderate"},
        {"drug": "Tetracyclines", "effect": "Alkaline pH reduces absorption", "severity": "moderate"},
    ],
    "sucralfate": [
        {"drug": "Fluoroquinolones", "effect": "Reduces absorption by 50-90%; give 2h apart", "severity": "major"},
        {"drug": "Tetracyclines", "effect": "Reduces absorption; space 2h apart", "severity": "moderate"},
        {"drug": "Digoxin", "effect": "Reduces absorption; space 2h apart", "severity": "moderate"},
        {"drug": "Phenytoin", "effect": "Reduces absorption; space 2h apart", "severity": "moderate"},
    ],
    "terbinafine": [
        {"drug": "Cimetidine", "effect": "Reduces terbinafine clearance", "severity": "minor"},
        {"drug": "Rifampin", "effect": "Increases terbinafine clearance 100%", "severity": "moderate"},
        {"drug": "Cyclosporine", "effect": "Terbinafine increases cyclosporine clearance", "severity": "moderate"},
    ],
    "trazodone": [
        {"drug": "MAO inhibitors", "effect": "Serotonin syndrome risk", "severity": "major"},
        {"drug": "Other serotonergic drugs", "effect": "Additive serotonergic effects", "severity": "moderate"},
        {"drug": "CNS depressants", "effect": "Additive sedation", "severity": "moderate"},
        {"drug": "Digoxin", "effect": "May increase digoxin levels", "severity": "moderate"},
    ],
    "ursodiol": [
        {
            "drug": "Aluminum antacids",
            "effect": "Reduces ursodiol absorption (bile acid binding)",
            "severity": "moderate",
        },
        {"drug": "Cholestyramine", "effect": "Reduces ursodiol absorption", "severity": "major"},
    ],
    "vasopressin": [
        {"drug": "Carbamazepine", "effect": "Potentiates antidiuretic effect", "severity": "moderate"},
        {"drug": "Lithium", "effect": "Antagonizes antidiuretic effect", "severity": "moderate"},
    ],
    "vitamin_k1": [
        {"drug": "Warfarin", "effect": "Antagonizes anticoagulant effect (therapeutic use)", "severity": "major"},
        {"drug": "Mineral oil", "effect": "Reduces vitamin K absorption", "severity": "moderate"},
    ],
    "desmopressin": [
        {"drug": "NSAIDs", "effect": "Potentiates antidiuretic effect; water retention risk", "severity": "moderate"},
        {"drug": "Lithium", "effect": "Antagonizes antidiuretic effect", "severity": "moderate"},
    ],
    "cosyntropin": [
        {
            "drug": "Cortisol assay interference",
            "effect": "Exogenous steroids affect ACTH stim test interpretation",
            "severity": "moderate",
        }
    ],
    "desoxycorticosterone": [
        {"drug": "Digoxin", "effect": "DOCP-induced hypokalemia increases digoxin toxicity", "severity": "major"},
        {
            "drug": "Potassium-sparing diuretics",
            "effect": "May partially counteract DOCP effect",
            "severity": "moderate",
        },
    ],
    "darbepoetin": [
        {"drug": "ACE inhibitors", "effect": "May blunt erythropoietic response", "severity": "moderate"},
        {"drug": "Iron supplements", "effect": "Required concurrent use for adequate response", "severity": "minor"},
    ],
    "fludrocortisone": [
        {"drug": "Digoxin", "effect": "Mineralocorticoid-induced hypokalemia increases toxicity", "severity": "major"},
        {"drug": "NSAIDs", "effect": "Additive sodium retention and GI risk", "severity": "moderate"},
        {"drug": "Potassium-depleting diuretics", "effect": "Additive hypokalemia", "severity": "moderate"},
    ],
    "activated_charcoal": [
        {
            "drug": "All oral medications",
            "effect": "Reduces absorption of co-administered drugs; space 2h",
            "severity": "major",
        },
        {"drug": "N-acetylcysteine (oral)", "effect": "Adsorbs NAC; use IV NAC instead", "severity": "major"},
    ],
    "apomorphine": [
        {"drug": "Ondansetron/maropitant", "effect": "Antiemetics antagonize emetic effect", "severity": "major"},
        {"drug": "Opioids", "effect": "CNS depression may enhance sedation", "severity": "moderate"},
    ],
    "intralipid": [
        {
            "drug": "Lipophilic drugs (local anesthetics)",
            "effect": "Sequesters lipophilic toxins—therapeutic use",
            "severity": "minor",
        }
    ],
    "dexamethasone_sp": [
        {"drug": "NSAIDs", "effect": "Dramatically increased GI ulceration risk", "severity": "major"},
        {"drug": "Insulin", "effect": "Antagonizes insulin; dose adjustment needed", "severity": "major"},
        {"drug": "Phenobarbital", "effect": "Increases dexamethasone metabolism", "severity": "moderate"},
        {"drug": "Diuretics", "effect": "Additive hypokalemia", "severity": "moderate"},
    ],
    "methylprednisolone": [
        {"drug": "NSAIDs", "effect": "Increased GI ulceration risk", "severity": "major"},
        {"drug": "Phenobarbital", "effect": "Accelerates corticosteroid metabolism", "severity": "moderate"},
        {"drug": "Cyclosporine", "effect": "Mutual inhibition of metabolism; dose-sparing", "severity": "moderate"},
    ],
    "cisapride": [
        {
            "drug": "Ketoconazole/itraconazole",
            "effect": "QT prolongation; arrhythmia risk (CYP3A4 inhibition)",
            "severity": "major",
        },
        {"drug": "Erythromycin/clarithromycin", "effect": "QT prolongation risk", "severity": "major"},
        {"drug": "Anticholinergics", "effect": "Antagonizes prokinetic effect", "severity": "moderate"},
    ],
    "clindamycin": [
        {"drug": "Erythromycin", "effect": "Antagonism—both bind 50S ribosome", "severity": "moderate"},
        {"drug": "Neuromuscular blockers", "effect": "Enhanced neuromuscular blockade", "severity": "moderate"},
        {"drug": "Kaolin/pectin", "effect": "Reduced clindamycin absorption", "severity": "moderate"},
    ],
    "enrofloxacin": [
        {"drug": "Theophylline", "effect": "Increases theophylline levels 20-50%", "severity": "moderate"},
        {"drug": "NSAIDs", "effect": "Increased seizure risk", "severity": "moderate"},
        {"drug": "Sucralfate/antacids", "effect": "Chelation reduces absorption 50-90%", "severity": "major"},
        {"drug": "Cyclosporine", "effect": "May increase cyclosporine levels", "severity": "moderate"},
    ],
    "amoxicillin_clavulanate": [
        {"drug": "Methotrexate", "effect": "Reduced methotrexate clearance; toxicity risk", "severity": "major"},
        {"drug": "Allopurinol", "effect": "Increased risk of skin rash", "severity": "minor"},
        {"drug": "Probenecid", "effect": "Increases amoxicillin levels (reduced clearance)", "severity": "minor"},
    ],
    "doxycycline": [
        {
            "drug": "Antacids (Ca/Mg/Al/Fe)",
            "effect": "Chelation reduces absorption 50-90%; space 2h",
            "severity": "major",
        },
        {"drug": "Phenobarbital", "effect": "Reduces doxycycline half-life by 50%", "severity": "moderate"},
        {"drug": "Warfarin", "effect": "Increases anticoagulant effect", "severity": "moderate"},
        {"drug": "Cyclosporine", "effect": "May increase cyclosporine levels", "severity": "moderate"},
    ],
    "azithromycin": [
        {"drug": "Cyclosporine", "effect": "Increases cyclosporine levels (CYP3A4 inhibition)", "severity": "moderate"},
        {"drug": "Digoxin", "effect": "May increase digoxin absorption (gut flora effect)", "severity": "moderate"},
        {"drug": "Warfarin", "effect": "May increase anticoagulant effect", "severity": "moderate"},
    ],
    "acepromazine": [
        {"drug": "Opioids", "effect": "Synergistic sedation; reduce both doses", "severity": "moderate"},
        {"drug": "Organophosphates", "effect": "Increased toxicity (inhibits metabolism)", "severity": "major"},
        {
            "drug": "Epinephrine",
            "effect": "Unopposed beta effect → paradoxical hypotension (use phenylephrine instead)",
            "severity": "major",
        },
        {"drug": "Propofol", "effect": "Additive hypotension", "severity": "moderate"},
    ],
    "diazepam": [
        {"drug": "Opioids", "effect": "Additive CNS/respiratory depression", "severity": "moderate"},
        {"drug": "Cimetidine", "effect": "Inhibits diazepam metabolism; prolonged effect", "severity": "moderate"},
        {"drug": "Phenobarbital", "effect": "Accelerates diazepam metabolism; reduced effect", "severity": "moderate"},
        {"drug": "Flumazenil", "effect": "Specific reversal agent", "severity": "minor"},
    ],
    "meloxicam": [
        {"drug": "Other NSAIDs", "effect": "Dramatically increased GI ulceration risk", "severity": "major"},
        {"drug": "Corticosteroids", "effect": "Dramatically increased GI ulceration risk", "severity": "major"},
        {"drug": "ACE inhibitors", "effect": "Reduced antihypertensive effect; renal risk", "severity": "moderate"},
        {"drug": "Aminoglycosides", "effect": "Increased nephrotoxicity", "severity": "major"},
        {"drug": "Anticoagulants", "effect": "Increased bleeding risk", "severity": "moderate"},
    ],
    "chloramphenicol": [
        {
            "drug": "Phenobarbital",
            "effect": "Bidirectional: PB reduces chloramphenicol; chloramphenicol increases PB levels",
            "severity": "major",
        },
        {"drug": "Cyclophosphamide", "effect": "Reduced cyclophosphamide activation", "severity": "moderate"},
        {"drug": "Iron/B12", "effect": "Chloramphenicol may antagonize hematopoietic response", "severity": "moderate"},
    ],
    "praziquantel": [
        {"drug": "Dexamethasone", "effect": "Reduces praziquantel levels (CYP induction)", "severity": "moderate"},
        {"drug": "Cimetidine", "effect": "Increases praziquantel levels", "severity": "minor"},
    ],
    "pyrantel_pamoate": [
        {"drug": "Levamisole", "effect": "Additive neuromuscular effects; synergistic", "severity": "minor"},
        {"drug": "Piperazine", "effect": "Antagonistic—opposing mechanisms on nematode muscle", "severity": "major"},
    ],
    "levetiracetam_oral": [
        {"drug": "Phenobarbital", "effect": "May increase levetiracetam clearance in dogs", "severity": "moderate"},
        {
            "drug": "No significant hepatic interactions",
            "effect": "Renally cleared; minimal CYP involvement",
            "severity": "minor",
        },
    ],
    "silymarin": [
        {
            "drug": "CYP-metabolized drugs",
            "effect": "Theoretical mild CYP inhibition; clinically insignificant",
            "severity": "minor",
        }
    ],
    "famotidine_injectable": [
        {"drug": "Ketoconazole", "effect": "Reduced ketoconazole absorption (needs acid pH)", "severity": "moderate"},
        {
            "drug": "Sucralfate",
            "effect": "H2 blockers may reduce sucralfate activation (needs acid)",
            "severity": "minor",
        },
    ],
    "calcium_gluconate": [
        {
            "drug": "Digoxin",
            "effect": "IV calcium can precipitate digoxin toxicity—contraindicated in digitalized patients",
            "severity": "major",
        },
        {"drug": "Tetracyclines", "effect": "Chelation reduces tetracycline absorption", "severity": "moderate"},
        {"drug": "Verapamil", "effect": "Calcium antagonizes verapamil effect", "severity": "moderate"},
    ],
    "potassium_chloride": [
        {"drug": "ACE inhibitors", "effect": "Additive hyperkalemia risk", "severity": "major"},
        {"drug": "Potassium-sparing diuretics", "effect": "Severe hyperkalemia risk", "severity": "major"},
        {"drug": "Digoxin", "effect": "Hypokalemia correction may alter digoxin effect", "severity": "moderate"},
    ],
    "tramadol": [
        {"drug": "SSRIs", "effect": "Serotonin syndrome risk", "severity": "major"},
        {"drug": "MAO inhibitors", "effect": "Severe serotonin syndrome", "severity": "major"},
        {
            "drug": "Other CNS depressants",
            "effect": "Additive sedation and respiratory depression",
            "severity": "moderate",
        },
        {"drug": "Ondansetron", "effect": "Reduces tramadol analgesic effect (5-HT3 involved)", "severity": "moderate"},
    ],
    "fluconazole_oral": [
        {
            "drug": "Cyclosporine",
            "effect": "Increases cyclosporine levels 2-3x (CYP3A4 inhibition)",
            "severity": "major",
        },
        {"drug": "Warfarin", "effect": "Increases anticoagulant effect significantly", "severity": "major"},
        {"drug": "Phenytoin", "effect": "Increases phenytoin levels", "severity": "major"},
        {"drug": "Cisapride", "effect": "QT prolongation risk; contraindicated", "severity": "major"},
    ],
    "itraconazole_oral": [
        {"drug": "Cyclosporine", "effect": "Increases cyclosporine levels 2-3x", "severity": "major"},
        {"drug": "Digoxin", "effect": "Increases digoxin levels", "severity": "major"},
        {"drug": "Midazolam", "effect": "Markedly increased sedation (CYP3A4 inhibition)", "severity": "major"},
        {"drug": "Cisapride", "effect": "QT prolongation; contraindicated", "severity": "major"},
        {
            "drug": "Antacids/H2 blockers/PPIs",
            "effect": "Reduced itraconazole absorption (needs acid)",
            "severity": "major",
        },
    ],
    "trilostane_oral": [
        {
            "drug": "ACE inhibitors",
            "effect": "Potential hyperkalemia from aldosterone suppression",
            "severity": "moderate",
        },
        {"drug": "Potassium-sparing diuretics", "effect": "Hyperkalemia risk", "severity": "major"},
        {"drug": "NSAIDs", "effect": "GI ulceration risk compounded by cortisol suppression", "severity": "moderate"},
    ],
    "amlodipine_feline": [
        {"drug": "Beta-blockers", "effect": "Additive hypotension and bradycardia", "severity": "moderate"},
        {"drug": "Cyclosporine", "effect": "Amlodipine may increase cyclosporine levels", "severity": "moderate"},
    ],
    "benazepril_ckd": [
        {"drug": "Potassium supplements", "effect": "Hyperkalemia risk", "severity": "major"},
        {"drug": "NSAIDs", "effect": "Reduced efficacy; increased renal risk", "severity": "moderate"},
        {"drug": "Spironolactone", "effect": "Additive hyperkalemia risk", "severity": "moderate"},
    ],
    "telmisartan_feline": [
        {
            "drug": "ACE inhibitors",
            "effect": "Dual RAAS blockade; hyperkalemia and hypotension risk",
            "severity": "major",
        },
        {"drug": "NSAIDs", "effect": "Reduced efficacy; renal risk in CKD cats", "severity": "moderate"},
        {"drug": "Potassium supplements", "effect": "Hyperkalemia risk", "severity": "moderate"},
    ],
    "vincristine_injectable": [
        {
            "drug": "Itraconazole/ketoconazole",
            "effect": "Increased vincristine neurotoxicity (CYP3A4 inhibition)",
            "severity": "major",
        },
        {"drug": "Phenytoin", "effect": "Reduced phenytoin absorption", "severity": "moderate"},
        {
            "drug": "L-asparaginase",
            "effect": "Give vincristine 12-24h before L-asp (reduced clearance)",
            "severity": "moderate",
        },
    ],
    "doxorubicin_injectable": [
        {"drug": "Cyclophosphamide", "effect": "Additive cardiotoxicity", "severity": "major"},
        {"drug": "Phenobarbital", "effect": "May increase doxorubicin clearance", "severity": "moderate"},
        {"drug": "Dexrazoxane", "effect": "Cardioprotective agent; give before doxorubicin", "severity": "minor"},
        {"drug": "Live vaccines", "effect": "Immunosuppression; vaccine-disease risk", "severity": "major"},
    ],
    "cyclophosphamide_oral": [
        {"drug": "Allopurinol", "effect": "Increased myelosuppression", "severity": "major"},
        {"drug": "Doxorubicin", "effect": "Additive cardiotoxicity", "severity": "major"},
        {
            "drug": "Phenobarbital",
            "effect": "Increases cyclophosphamide activation and toxicity",
            "severity": "moderate",
        },
        {"drug": "Chloramphenicol", "effect": "Reduced cyclophosphamide activation", "severity": "moderate"},
    ],
    "oxytocin_injectable": [
        {"drug": "Prostaglandins", "effect": "Synergistic uterotonic effect; monitor closely", "severity": "moderate"},
        {"drug": "Vasopressors", "effect": "Potentiated hypertensive response", "severity": "moderate"},
    ],
    "domperidone": [
        {"drug": "Ketoconazole", "effect": "Increases domperidone levels (CYP3A4 inhibition)", "severity": "moderate"},
        {"drug": "Anticholinergics", "effect": "Antagonizes prokinetic effect", "severity": "moderate"},
    ],
    "pimobendan_oral": [
        {
            "drug": "Beta-blockers",
            "effect": "May partially antagonize positive inotropic effect",
            "severity": "moderate",
        },
        {
            "drug": "Calcium channel blockers (verapamil)",
            "effect": "Additive negative effects on contractility",
            "severity": "major",
        },
    ],
    "furosemide_injectable": [
        {"drug": "Aminoglycosides", "effect": "Additive ototoxicity and nephrotoxicity", "severity": "major"},
        {"drug": "ACE inhibitors", "effect": "First-dose hypotension; reduce furosemide first", "severity": "moderate"},
        {"drug": "Digoxin", "effect": "Hypokalemia increases digoxin toxicity risk", "severity": "major"},
        {"drug": "NSAIDs", "effect": "Reduced diuretic efficacy", "severity": "moderate"},
        {"drug": "Corticosteroids", "effect": "Additive hypokalemia", "severity": "moderate"},
    ],
    "spironolactone_oral": [
        {"drug": "ACE inhibitors", "effect": "Additive hyperkalemia risk; monitor K+", "severity": "major"},
        {"drug": "Potassium supplements", "effect": "Severe hyperkalemia risk", "severity": "major"},
        {"drug": "NSAIDs", "effect": "Reduced diuretic effect and hyperkalemia risk", "severity": "moderate"},
        {"drug": "Digoxin", "effect": "Spironolactone may increase digoxin levels", "severity": "moderate"},
    ],
    "digoxin_oral": [
        {"drug": "Amiodarone", "effect": "Doubles digoxin levels; reduce dose 50%", "severity": "major"},
        {"drug": "Diuretics (K+-depleting)", "effect": "Hypokalemia increases toxicity", "severity": "major"},
        {"drug": "Quinidine", "effect": "Doubles digoxin levels", "severity": "major"},
        {"drug": "Verapamil/diltiazem", "effect": "Increases digoxin levels 50-70%", "severity": "major"},
        {"drug": "Calcium IV", "effect": "Can precipitate fatal arrhythmias", "severity": "major"},
    ],
    "diltiazem_oral": [
        {"drug": "Beta-blockers", "effect": "Severe bradycardia and AV block", "severity": "major"},
        {"drug": "Digoxin", "effect": "Increases digoxin levels 20-50%", "severity": "moderate"},
        {"drug": "Cyclosporine", "effect": "Increases cyclosporine levels (CYP3A4 inhibition)", "severity": "moderate"},
        {"drug": "Phenobarbital", "effect": "Reduces diltiazem levels (CYP induction)", "severity": "moderate"},
    ],
    "clopidogrel_oral": [
        {"drug": "Omeprazole", "effect": "Reduces clopidogrel activation (CYP2C19 inhibition)", "severity": "moderate"},
        {"drug": "NSAIDs", "effect": "Additive bleeding risk", "severity": "moderate"},
        {"drug": "Aspirin", "effect": "Additive antiplatelet effect (may be therapeutic)", "severity": "moderate"},
    ],
    "sildenafil_cardiac": [
        {"drug": "Nitrates", "effect": "Severe life-threatening hypotension; contraindicated", "severity": "major"},
        {"drug": "Alpha-blockers (prazosin)", "effect": "Additive hypotension", "severity": "major"},
        {"drug": "Ketoconazole", "effect": "Increases sildenafil levels (CYP3A4 inhibition)", "severity": "moderate"},
    ],
}
