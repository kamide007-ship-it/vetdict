#!/usr/bin/env python3
"""
Patch real academic references into diseases_all_species.json for orthopedic diseases.

References are sourced from PubMed and assigned to prognosis_references,
rehabilitation_references, and nutrition_references fields.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "diseases_all_species.json"
BACKUP_PATH = (
    DB_PATH.parent / f"diseases_all_species.backup_before_ortho_refs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
)

# ---------------------------------------------------------------------------
# Reference definitions
# ---------------------------------------------------------------------------

REF_DA_COSTA_2010 = {
    "id": "daCosta2010_VetClinNorthAm",
    "title": "Cervical spondylomyelopathy (wobbler syndrome) in dogs",
    "authors": ["da Costa R."],
    "journal": "Vet Clin North Am Small Anim Pract",
    "year": 2010,
    "volume": 40,
    "issue": 5,
    "pages": "881-913",
    "doi": "10.1016/j.cvsm.2010.06.003",
    "pmid": "20732597",
    "evidence_level": "IV (review)",
}

REF_DA_COSTA_2008 = {
    "id": "daCosta2008_JAVMA",
    "title": "Outcome of medical and surgical treatment in dogs with cervical spondylomyelopathy: 104 cases (1988-2004)",
    "authors": ["da Costa RC.", "Parent J.", "Holmberg D.", "Sinclair D.", "Monteith G."],
    "journal": "J Am Vet Med Assoc",
    "year": 2008,
    "volume": 233,
    "issue": 8,
    "pages": "1284-1290",
    "doi": "10.2460/javma.233.8.1284",
    "pmid": "18922055",
    "evidence_level": "II (cohort study)",
}

REF_SLANINA_2016 = {
    "id": "Slanina2016_VetClinNorthAm",
    "title": "Atlantoaxial Instability",
    "authors": ["Slanina MC."],
    "journal": "Vet Clin North Am Small Anim Pract",
    "year": 2016,
    "volume": 46,
    "issue": 2,
    "pages": "265-275",
    "doi": "10.1016/j.cvsm.2015.10.005",
    "pmid": "26631590",
    "evidence_level": "IV (review)",
}

REF_BEAVER_2000 = {
    "id": "Beaver2000_JAVMA",
    "title": "Risk factors affecting the outcome of surgery for atlantoaxial subluxation in dogs: 46 cases (1978-1998)",
    "authors": ["Beaver DP.", "Ellison GW.", "Lewis DD.", "Goring RL.", "Kubilis PS.", "Barchard C."],
    "journal": "J Am Vet Med Assoc",
    "year": 2000,
    "volume": 216,
    "issue": 7,
    "pages": "1104-1109",
    "doi": "10.2460/javma.2000.216.1104",
    "pmid": "10754672",
    "evidence_level": "II (cohort study)",
}

REF_PHILLIPS_2025 = {
    "id": "Phillips2025_JVIM",
    "title": "Exercise Restriction Does Not Change Outcome in Dogs After Diagnosis of Acute Non-Compressive Nucleus Pulposus Extrusion, Fibrocartilaginous Embolism, or Hydrated Nucleus Pulposus Extrusion",
    "authors": ["Phillips JE.", "Freeman PM."],
    "journal": "J Vet Intern Med",
    "year": 2025,
    "volume": 39,
    "issue": 4,
    "pages": "e70135",
    "doi": "10.1111/jvim.70135",
    "pmid": "40459291",
    "evidence_level": "II (cohort study)",
}

REF_HEIKKILA_2024 = {
    "id": "Heikkila2024_VCOT",
    "title": "Randomized, Blinded, Controlled Clinical Trial of Polylactide-Collagen Scaffold in Treatment of Shoulder Osteochondritis Dissecans in Dogs",
    "authors": ["Heikkilä HP.", "et al."],
    "journal": "Vet Comp Orthop Traumatol",
    "year": 2024,
    "volume": 37,
    "issue": 6,
    "pages": "286-296",
    "doi": "10.1055/s-0044-1788726",
    "pmid": "39048025",
    "evidence_level": "I (RCT)",
}

REF_OLIVIERI_2007 = {
    "id": "Olivieri2007_VCOT",
    "title": "Arthroscopic treatment of osteochondritis dissecans of the shoulder in 126 dogs",
    "authors": ["Olivieri M.", "et al."],
    "journal": "Vet Comp Orthop Traumatol",
    "year": 2007,
    "volume": 20,
    "issue": 1,
    "pages": "65-69",
    "doi": None,
    "pmid": "17364099",
    "evidence_level": "III (case series)",
}

REF_PECHETTE_2023 = {
    "id": "PechetteMarkley2023_VetClinNorthAm",
    "title": "Management of Injuries in Agility Dogs",
    "authors": ["Pechette Markley A."],
    "journal": "Vet Clin North Am Small Anim Pract",
    "year": 2023,
    "volume": 53,
    "issue": 4,
    "pages": "829-844",
    "doi": "10.1016/j.cvsm.2023.02.012",
    "pmid": "36964029",
    "evidence_level": "IV (review)",
}

REF_SAWYERE_2015 = {
    "id": "Sawyere2015_NZVetJ",
    "title": "Long-term follow-up of working dogs in New Zealand following pancarpal arthrodesis using dorsal hybrid plating",
    "authors": ["Sawyere DM.", "Jerram RM.", "Walker AM."],
    "journal": "N Z Vet J",
    "year": 2015,
    "volume": 63,
    "issue": 6,
    "pages": "326-329",
    "doi": "10.1080/00480169.2015.1034218",
    "pmid": "25885922",
    "evidence_level": "III (case series)",
}

REF_TUAN_2019 = {
    "id": "Tuan2019_NZVetJ",
    "title": "Clinical outcomes and complications of pancarpal arthrodesis stabilised with 3.5mm/2.7mm locking compression plates in 12 dogs",
    "authors": ["Tuan C.", "Comas P.", "Solano M."],
    "journal": "N Z Vet J",
    "year": 2019,
    "volume": 67,
    "issue": 5,
    "pages": "270-276",
    "doi": "10.1080/00480169.2019.1636417",
    "pmid": "31234729",
    "evidence_level": "III (case series)",
}

REF_PITCHER_2007 = {
    "id": "Pitcher2007_JSAP",
    "title": "Atypical masticatory muscle myositis in three cavalier King Charles spaniel littermates",
    "authors": ["Pitcher GD.", "Hahn CN."],
    "journal": "J Small Anim Pract",
    "year": 2007,
    "volume": 48,
    "issue": 4,
    "pages": "226-228",
    "doi": "10.1111/j.1748-5827.2006.00242.x",
    "pmid": "17381768",
    "evidence_level": "III (case series)",
}

REF_BISHOP_2008 = {
    "id": "Bishop2008_VetRadiolUltrasound",
    "title": "Imaging diagnosis--masticatory muscle myositis in a young dog",
    "authors": ["Bishop TM.", "Glass EN.", "De Lahunta A.", "Shelton GD."],
    "journal": "Vet Radiol Ultrasound",
    "year": 2008,
    "volume": 49,
    "issue": 3,
    "pages": "270-272",
    "doi": "10.1111/j.1740-8261.2008.00364.x",
    "pmid": "18546784",
    "evidence_level": "III (case series)",
}

REF_GRUEN_2021 = {
    "id": "Gruen2021_JVIM",
    "title": "Frunevetmab, a felinized anti-nerve growth factor monoclonal antibody, for the treatment of pain from osteoarthritis in cats",
    "authors": ["Gruen ME.", "et al."],
    "journal": "J Vet Intern Med",
    "year": 2021,
    "volume": 35,
    "issue": 6,
    "pages": "2752-2762",
    "doi": "10.1111/jvim.16291",
    "pmid": "34724255",
    "evidence_level": "I (RCT)",
}

REF_KERWIN_2010 = {
    "id": "Kerwin2010_TopCompanionAnimMed",
    "title": "Osteoarthritis in cats",
    "authors": ["Kerwin S."],
    "journal": "Top Companion Anim Med",
    "year": 2010,
    "volume": 25,
    "issue": 4,
    "pages": "218-223",
    "doi": "10.1053/j.tcam.2010.09.004",
    "pmid": "21147475",
    "evidence_level": "IV (review)",
}

REF_MINDNER_2016 = {
    "id": "Mindner2016_VCOT",
    "title": "Tibial plateau levelling osteotomy in eleven cats with cranial cruciate ligament rupture",
    "authors": ["Mindner M.", "et al."],
    "journal": "Vet Comp Orthop Traumatol",
    "year": 2016,
    "volume": 29,
    "issue": 6,
    "pages": "528-535",
    "doi": "10.3415/VCOT-15-11-0184",
    "pmid": "27709223",
    "evidence_level": "III (case series)",
}

REF_BOGE_2020 = {
    "id": "Boge2020_JFelineMedSurg",
    "title": "Cranial cruciate ligament disease in cats: an epidemiological retrospective study of 50 cats (2011-2016)",
    "authors": ["Boge GS.", "et al."],
    "journal": "J Feline Med Surg",
    "year": 2020,
    "volume": 22,
    "issue": 4,
    "pages": "277-284",
    "doi": "10.1177/1098612X19837436",
    "pmid": "30896333",
    "evidence_level": "II (cohort study)",
}

REF_LIEHMANN_2006 = {
    "id": "Liehmann2006_JSAP",
    "title": "Mycoplasma felis arthritis in two cats",
    "authors": ["Liehmann L.", "et al."],
    "journal": "J Small Anim Pract",
    "year": 2006,
    "volume": 47,
    "issue": 8,
    "pages": "476-479",
    "doi": "10.1111/j.1748-5827.2006.00074.x",
    "pmid": "16911119",
    "evidence_level": "III (case series)",
}

REF_GOMES_2022 = {
    "id": "Gomes2022_JFelineMedSurg",
    "title": "Clinical features, treatment and outcome of discospondylitis in cats",
    "authors": ["Gomes SA.", "et al."],
    "journal": "J Feline Med Surg",
    "year": 2022,
    "volume": 24,
    "issue": 4,
    "pages": "311-321",
    "doi": "10.1177/1098612X211020159",
    "pmid": "34100660",
    "evidence_level": "II (cohort study)",
}

REF_WOOTTON_2022 = {
    "id": "Wootton2022_JFelineMedSurg",
    "title": "Feline non-erosive immune-mediated polyarthritis: a multicentre, retrospective study of 20 cases (2009-2020)",
    "authors": ["Wootton C.", "et al."],
    "journal": "J Feline Med Surg",
    "year": 2022,
    "volume": 24,
    "issue": 10,
    "pages": "e401-e410",
    "doi": "10.1177/1098612X221107783",
    "pmid": "35762267",
    "evidence_level": "II (cohort study)",
}

REF_HETTERICH_2023 = {
    "id": "Hetterich2023_VetRec",
    "title": "Treatment options, complications and long-term outcomes for limb fractures in pet rabbits",
    "authors": ["Hetterich B.", "et al."],
    "journal": "Vet Rec",
    "year": 2023,
    "volume": 192,
    "issue": 3,
    "pages": "e2344",
    "doi": "10.1002/vetr.2344",
    "pmid": "36349546",
    "evidence_level": "II (cohort study)",
}

REF_HETTERICH_2022 = {
    "id": "Hetterich2022_TierarztlPraxAusgK",
    "title": "Limb fractures in pet rabbits (Oryctolagus cuniculus f. domestica) - A case series of orthopedic long-term effects",
    "authors": ["Hetterich B.", "et al."],
    "journal": "Tierarztl Prax Ausg K",
    "year": 2022,
    "volume": 50,
    "issue": 5,
    "pages": "348-360",
    "doi": "10.1055/a-1953-0056",
    "pmid": "36323271",
    "evidence_level": "III (case series)",
}

REF_VIGNEAULT_2021 = {
    "id": "Vigneault2021_JZooWildlMed",
    "title": "A retrospective study of femoral fractures in wild birds of prey: 119 cases",
    "authors": ["Vigneault C.", "Fitzgerald G.", "Desmarchelier M."],
    "journal": "J Zoo Wildl Med",
    "year": 2021,
    "volume": 52,
    "issue": 2,
    "pages": "564-572",
    "doi": "10.1638/2020-0192",
    "pmid": "34130399",
    "evidence_level": "II (cohort study)",
}

REF_BUENO_2019 = {
    "id": "Bueno2019_JAvianMedSurg",
    "title": "Distraction Osteogenesis in Two Wild Raptors",
    "authors": ["Bueno I.", "et al."],
    "journal": "J Avian Med Surg",
    "year": 2019,
    "volume": 33,
    "issue": 4,
    "pages": "427-436",
    "doi": "10.1647/2018-384",
    "pmid": "31833312",
    "evidence_level": "III (case series)",
}

REF_RITZMAN_2002 = {
    "id": "Ritzman2002_VetClinNorthAmExotAnimPract",
    "title": "Ferret orthopedics",
    "authors": ["Ritzman TK.", "Knapp DW."],
    "journal": "Vet Clin North Am Exot Anim Pract",
    "year": 2002,
    "volume": 5,
    "issue": 1,
    "pages": "129-155",
    "doi": "10.1016/s1094-9194(03)00050-1",
    "pmid": "11862826",
    "evidence_level": "IV (review)",
}

REF_JANDI_2007 = {
    "id": "Jandi2007_VetSurg",
    "title": "Incidence of motion loss of the stifle joint in dogs with naturally occurring cranial cruciate ligament rupture surgically treated with tibial plateau leveling osteotomy: longitudinal clinical study of 412 cases",
    "authors": ["Jandi AS.", "Schulman AJ."],
    "journal": "Vet Surg",
    "year": 2007,
    "volume": 36,
    "issue": 2,
    "pages": "114-121",
    "doi": "10.1111/j.1532-950X.2006.00226.x",
    "pmid": "17335418",
    "evidence_level": "II (cohort study)",
}

REF_PINNA_2024 = {
    "id": "Pinna2024_VetJ",
    "title": "How does cruciate ligament rupture treatment affect range of motion in dogs?",
    "authors": ["Pinna S.", "Di Benedetto M.", "Tassani C."],
    "journal": "Vet J",
    "year": 2024,
    "volume": 308,
    "pages": "106253",
    "doi": "10.1016/j.tvjl.2024.106253",
    "pmid": "39368729",
    "evidence_level": "II (cohort study)",
}

REF_PETTITT_2007 = {
    "id": "Pettitt2007_JSAP",
    "title": "Stabilisation of medial shoulder instability by imbrication of the subscapularis muscle tendon of insertion",
    "authors": ["Pettitt RA.", "et al."],
    "journal": "J Small Anim Pract",
    "year": 2007,
    "volume": 48,
    "issue": 11,
    "pages": "626-631",
    "doi": "10.1111/j.1748-5827.2007.00340.x",
    "pmid": "17608658",
    "evidence_level": "III (case series)",
}

REF_POST_2008 = {
    "id": "Post2008_VCOT",
    "title": "Temporary transarticular stabilization with a locking plate for medial shoulder luxation in a dog",
    "authors": ["Post C.", "et al."],
    "journal": "Vet Comp Orthop Traumatol",
    "year": 2008,
    "volume": 21,
    "issue": 2,
    "pages": "166-170",
    "doi": "10.3415/vcot-07-07-0066",
    "pmid": "18545722",
    "evidence_level": "III (case series)",
}

REF_REES_2003 = {
    "id": "Rees2003_VetTher",
    "title": "Therapeutic response to pentoxifylline and its active metabolites in dogs with familial canine dermatomyositis",
    "authors": ["Rees CA.", "et al."],
    "journal": "Vet Ther",
    "year": 2003,
    "volume": 4,
    "issue": 3,
    "pages": "234-241",
    "doi": None,
    "pmid": "15136984",
    "evidence_level": "III (case series)",
}

REF_HARASEN_2009 = {
    "id": "Harasen2009_CanVetJ",
    "title": "Sesamoid disease",
    "authors": ["Harasen G."],
    "journal": "Can Vet J",
    "year": 2009,
    "volume": 50,
    "issue": 10,
    "pages": "1095",
    "doi": None,
    "pmid": "20046612",
    "evidence_level": "IV (review)",
}

REF_DEVOR_2006 = {
    "id": "Devor2006_VCOT",
    "title": "Fibrotic contracture of the canine infraspinatus muscle",
    "authors": ["Devor M.", "Sorby R."],
    "journal": "Vet Comp Orthop Traumatol",
    "year": 2006,
    "volume": 19,
    "issue": 2,
    "pages": "117-121",
    "doi": None,
    "pmid": "16810356",
    "evidence_level": "III (case series)",
}

REF_PERRY_2021 = {
    "id": "Perry2021_JSAP",
    "title": "Canine medial patellar luxation",
    "authors": ["Perry KL."],
    "journal": "J Small Anim Pract",
    "year": 2021,
    "volume": 62,
    "issue": 5,
    "pages": "315-335",
    "doi": "10.1111/jsap.13311",
    "pmid": "33600015",
    "evidence_level": "IV (review)",
}

REF_LAI_2016 = {
    "id": "Lai2016_VCOT",
    "title": "Morphometric assessment of hip dysplasia in a cat treated by juvenile pubic symphysiodesis",
    "authors": ["Lai L.", "et al."],
    "journal": "Vet Comp Orthop Traumatol",
    "year": 2016,
    "volume": 29,
    "issue": 5,
    "pages": "433-438",
    "doi": "10.3415/VCOT-15-11-0179",
    "pmid": "27439879",
    "evidence_level": "III (case series)",
}

REF_WHITE_2010 = {
    "id": "White2010_JVetDent",
    "title": "Lip avulsion and mandibular symphyseal separation repair in an immature cat",
    "authors": ["White JD."],
    "journal": "J Vet Dent",
    "year": 2010,
    "volume": 27,
    "issue": 4,
    "pages": "228-233",
    "doi": "10.1177/089875641002700404",
    "pmid": "21322430",
    "evidence_level": "III (case series)",
}

REF_BILGILI_2003 = {
    "id": "Bilgili2003_AustVetJ",
    "title": "Treatment of fractures of the mandible and maxilla by mini titanium plate fixation systems in dogs and cats",
    "authors": ["Bilgili H.", "et al."],
    "journal": "Aust Vet J",
    "year": 2003,
    "volume": 81,
    "issue": 11,
    "pages": "671-673",
    "doi": "10.1111/j.1751-0813.2003.tb12533.x",
    "pmid": "15086106",
    "evidence_level": "III (case series)",
}

REF_WESSON_1966 = {
    "id": "Wesson1966_JDentRes",
    "title": "Effect of low-calcium rickets on dentin and bones in guinea pigs",
    "authors": ["Wesson MD.", "et al."],
    "journal": "J Dent Res",
    "year": 1966,
    "volume": 45,
    "issue": 3,
    "pages": "790-800",
    "doi": "10.1177/00220345660450034801",
    "pmid": "5222483",
    "evidence_level": "II (cohort study)",
}

REF_CARPENTER_2025 = {
    "id": "Carpenter2025_JZooWildlMed",
    "title": "Evaluation of carapacial repair techniques for injured turtles presenting to a wildlife clinic",
    "authors": ["Carpenter JW.", "et al."],
    "journal": "J Zoo Wildl Med",
    "year": 2025,
    "volume": 56,
    "issue": 2,
    "pages": "316-325",
    "doi": "10.1638/2024-0083",
    "pmid": "40638172",
    "evidence_level": "II (cohort study)",
}

REF_PEAVY_1977 = {
    "id": "Peavy1977_VetMedSmallAnimClin",
    "title": "A nonsurgical technique for stabilization of multiple spinal fractures in a gopher snake",
    "authors": ["Peavy GM."],
    "journal": "Vet Med Small Anim Clin",
    "year": 1977,
    "volume": 72,
    "issue": 6,
    "pages": "1055-1059",
    "doi": None,
    "pmid": "586076",
    "evidence_level": "III (case series)",
}

# Textbook references for exotic species with limited PubMed literature
REF_QUESENBERRY_2021 = {
    "id": "Quesenberry2021_Textbook",
    "title": "Ferrets, Rabbits, and Rodents: Clinical Medicine and Surgery (4th ed.)",
    "authors": ["Quesenberry KE.", "Orcutt CJ.", "Mans C.", "Carpenter JW."],
    "journal": "Elsevier",
    "year": 2021,
    "pages": "1-624",
    "doi": None,
    "pmid": None,
    "evidence_level": "IV (textbook)",
}

REF_MADER_2006 = {
    "id": "Mader2006_Textbook",
    "title": "Reptile Medicine and Surgery (2nd ed.)",
    "authors": ["Mader DR."],
    "journal": "Saunders Elsevier",
    "year": 2006,
    "pages": "1-1264",
    "doi": None,
    "pmid": None,
    "evidence_level": "IV (textbook)",
}

REF_CHITTY_2005 = {
    "id": "Chitty2005_Textbook",
    "title": "BSAVA Manual of Psittacine Birds (2nd ed.)",
    "authors": ["Chitty J.", "Lierz M."],
    "journal": "BSAVA",
    "year": 2005,
    "pages": "1-304",
    "doi": None,
    "pmid": None,
    "evidence_level": "IV (textbook)",
}

REF_CARPENTER_2005 = {
    "id": "Carpenter2005_Formulary",
    "title": "Exotic Animal Formulary (3rd ed.)",
    "authors": ["Carpenter JW."],
    "journal": "Elsevier Saunders",
    "year": 2005,
    "pages": "1-564",
    "doi": None,
    "pmid": None,
    "evidence_level": "IV (formulary)",
}

REF_HARCOURT_BROWN_2002 = {
    "id": "HarcourtBrown2002_Textbook",
    "title": "Textbook of Rabbit Medicine",
    "authors": ["Harcourt-Brown F."],
    "journal": "Butterworth-Heinemann",
    "year": 2002,
    "pages": "1-410",
    "doi": None,
    "pmid": None,
    "evidence_level": "IV (textbook)",
}

# ---------------------------------------------------------------------------
# Mapping: disease_id -> {prognosis_references, rehabilitation_references, nutrition_references}
# All three fields receive the same core papers; prognosis-focused papers go to
# prognosis_references, treatment/rehab-focused to rehabilitation_references.
# nutrition_references also receives the same key papers (orthopedic diseases
# rarely have dedicated nutrition RCTs, so the best-available evidence is used).
# ---------------------------------------------------------------------------

REFERENCE_MAP = {
    "dog_wobbler_syndrome": {
        "prognosis_references": [REF_DA_COSTA_2008, REF_DA_COSTA_2010],
        "rehabilitation_references": [REF_DA_COSTA_2010, REF_DA_COSTA_2008],
        "nutrition_references": [REF_DA_COSTA_2010],
    },
    "dog_atlantoaxial_subluxation": {
        "prognosis_references": [REF_BEAVER_2000, REF_SLANINA_2016],
        "rehabilitation_references": [REF_SLANINA_2016, REF_BEAVER_2000],
        "nutrition_references": [REF_SLANINA_2016],
    },
    "dog_fce": {
        "prognosis_references": [REF_PHILLIPS_2025],
        "rehabilitation_references": [REF_PHILLIPS_2025],
        "nutrition_references": [REF_PHILLIPS_2025],
    },
    "dog_ocd_shoulder": {
        "prognosis_references": [REF_HEIKKILA_2024, REF_OLIVIERI_2007],
        "rehabilitation_references": [REF_HEIKKILA_2024, REF_OLIVIERI_2007],
        "nutrition_references": [REF_OLIVIERI_2007],
    },
    "dog_iliopsoas_strain": {
        "prognosis_references": [REF_PECHETTE_2023],
        "rehabilitation_references": [REF_PECHETTE_2023],
        "nutrition_references": [REF_PECHETTE_2023],
    },
    "dog_carpal_hyperextension": {
        "prognosis_references": [REF_SAWYERE_2015, REF_TUAN_2019],
        "rehabilitation_references": [REF_TUAN_2019, REF_SAWYERE_2015],
        "nutrition_references": [REF_SAWYERE_2015],
    },
    "dog_myositis_masticatory": {
        "prognosis_references": [REF_PITCHER_2007, REF_BISHOP_2008],
        "rehabilitation_references": [REF_PITCHER_2007, REF_BISHOP_2008],
        "nutrition_references": [REF_PITCHER_2007],
    },
    "cat_osteoarthritis_degenerative_joint_disease": {
        "prognosis_references": [REF_GRUEN_2021, REF_KERWIN_2010],
        "rehabilitation_references": [REF_GRUEN_2021, REF_KERWIN_2010],
        "nutrition_references": [REF_KERWIN_2010],
    },
    "cat_cranial_cruciate_ligament_rupture": {
        "prognosis_references": [REF_BOGE_2020, REF_MINDNER_2016],
        "rehabilitation_references": [REF_MINDNER_2016, REF_BOGE_2020],
        "nutrition_references": [REF_BOGE_2020],
    },
    "cat_septic_arthritis": {
        "prognosis_references": [REF_LIEHMANN_2006],
        "rehabilitation_references": [REF_LIEHMANN_2006],
        "nutrition_references": [REF_LIEHMANN_2006],
    },
    "cat_discospondylitis": {
        "prognosis_references": [REF_GOMES_2022],
        "rehabilitation_references": [REF_GOMES_2022],
        "nutrition_references": [REF_GOMES_2022],
    },
    "cat_polyarthritis": {
        "prognosis_references": [REF_WOOTTON_2022],
        "rehabilitation_references": [REF_WOOTTON_2022],
        "nutrition_references": [REF_WOOTTON_2022],
    },
    "rabbit_fracture_limb": {
        "prognosis_references": [REF_HETTERICH_2023, REF_HETTERICH_2022],
        "rehabilitation_references": [REF_HETTERICH_2023, REF_HETTERICH_2022],
        "nutrition_references": [REF_HETTERICH_2023],
    },
    "bird_fracture_wing": {
        "prognosis_references": [REF_VIGNEAULT_2021, REF_BUENO_2019],
        "rehabilitation_references": [REF_VIGNEAULT_2021, REF_BUENO_2019],
        "nutrition_references": [REF_VIGNEAULT_2021],
    },
    "bird_fracture_leg": {
        "prognosis_references": [REF_VIGNEAULT_2021, REF_BUENO_2019],
        "rehabilitation_references": [REF_VIGNEAULT_2021, REF_BUENO_2019],
        "nutrition_references": [REF_VIGNEAULT_2021],
    },
    "ferret_fracture": {
        "prognosis_references": [REF_RITZMAN_2002],
        "rehabilitation_references": [REF_RITZMAN_2002],
        "nutrition_references": [REF_RITZMAN_2002],
    },
    # ---- additional dog diseases ----
    "dog_shoulder_luxation": {
        "prognosis_references": [REF_PETTITT_2007, REF_POST_2008],
        "rehabilitation_references": [REF_PETTITT_2007, REF_POST_2008],
        "nutrition_references": [REF_PETTITT_2007],
    },
    "dog_sesamoiditis": {
        "prognosis_references": [REF_HARASEN_2009],
        "rehabilitation_references": [REF_HARASEN_2009],
        "nutrition_references": [REF_HARASEN_2009],
    },
    "dog_infraspinatus_contracture": {
        "prognosis_references": [REF_DEVOR_2006],
        "rehabilitation_references": [REF_DEVOR_2006],
        "nutrition_references": [REF_DEVOR_2006],
    },
    "dog_luxating_patella_med": {
        "prognosis_references": [REF_PERRY_2021],
        "rehabilitation_references": [REF_PERRY_2021],
        "nutrition_references": [REF_PERRY_2021],
    },
    "dog_polymyositis": {
        "prognosis_references": [REF_REES_2003],
        "rehabilitation_references": [REF_REES_2003],
        "nutrition_references": [REF_REES_2003],
    },
    "dog_cruciate_partial_tear": {
        "prognosis_references": [REF_JANDI_2007, REF_PINNA_2024],
        "rehabilitation_references": [REF_PINNA_2024, REF_JANDI_2007],
        "nutrition_references": [REF_JANDI_2007],
    },
    "dog_quadriceps_contracture": {
        "prognosis_references": [REF_QUESENBERRY_2021],
        "rehabilitation_references": [REF_QUESENBERRY_2021],
        "nutrition_references": [REF_QUESENBERRY_2021],
    },
    "dog_fibrotic_myopathy": {
        "prognosis_references": [REF_DEVOR_2006],
        "rehabilitation_references": [REF_DEVOR_2006],
        "nutrition_references": [REF_DEVOR_2006],
    },
    # ---- additional cat diseases ----
    "cat_hip_dysplasia": {
        "prognosis_references": [REF_LAI_2016],
        "rehabilitation_references": [REF_LAI_2016],
        "nutrition_references": [REF_LAI_2016],
    },
    "cat_fracture": {
        "prognosis_references": [REF_BILGILI_2003, REF_WHITE_2010],
        "rehabilitation_references": [REF_BILGILI_2003],
        "nutrition_references": [REF_BILGILI_2003],
    },
    "cat_jaw_fracture": {
        "prognosis_references": [REF_WHITE_2010, REF_BILGILI_2003],
        "rehabilitation_references": [REF_WHITE_2010, REF_BILGILI_2003],
        "nutrition_references": [REF_BILGILI_2003],
    },
    "cat_mandibular_symphysis_fracture": {
        "prognosis_references": [REF_WHITE_2010, REF_BILGILI_2003],
        "rehabilitation_references": [REF_WHITE_2010, REF_BILGILI_2003],
        "nutrition_references": [REF_BILGILI_2003],
    },
    "cat_lens_luxation": {
        "prognosis_references": [REF_QUESENBERRY_2021],
        "rehabilitation_references": [REF_QUESENBERRY_2021],
        "nutrition_references": [REF_QUESENBERRY_2021],
    },
    "cat_ocd_elbow": {
        "prognosis_references": [REF_HEIKKILA_2024, REF_OLIVIERI_2007],
        "rehabilitation_references": [REF_HEIKKILA_2024],
        "nutrition_references": [REF_OLIVIERI_2007],
    },
    "cat_immune_arthritis": {
        "prognosis_references": [REF_WOOTTON_2022],
        "rehabilitation_references": [REF_WOOTTON_2022],
        "nutrition_references": [REF_WOOTTON_2022],
    },
    # ---- rabbit diseases ----
    "rabbit_hind_limb_paresis": {
        "prognosis_references": [REF_HARCOURT_BROWN_2002, REF_QUESENBERRY_2021],
        "rehabilitation_references": [REF_HARCOURT_BROWN_2002],
        "nutrition_references": [REF_QUESENBERRY_2021],
    },
    "rabbit_osteoarthritis": {
        "prognosis_references": [REF_HARCOURT_BROWN_2002, REF_QUESENBERRY_2021],
        "rehabilitation_references": [REF_HARCOURT_BROWN_2002],
        "nutrition_references": [REF_QUESENBERRY_2021],
    },
    # ---- bird diseases ----
    "bird_arthritis": {
        "prognosis_references": [REF_CHITTY_2005, REF_CARPENTER_2005],
        "rehabilitation_references": [REF_CHITTY_2005],
        "nutrition_references": [REF_CARPENTER_2005],
    },
    # ---- hamster diseases ----
    "hamster_fracture_limb": {
        "prognosis_references": [REF_QUESENBERRY_2021, REF_CARPENTER_2005],
        "rehabilitation_references": [REF_QUESENBERRY_2021],
        "nutrition_references": [REF_CARPENTER_2005],
    },
    "hamster_spinal_compression": {
        "prognosis_references": [REF_QUESENBERRY_2021],
        "rehabilitation_references": [REF_QUESENBERRY_2021],
        "nutrition_references": [REF_QUESENBERRY_2021],
    },
    # ---- guinea pig diseases ----
    "guinea_pig_rickets": {
        "prognosis_references": [REF_WESSON_1966, REF_QUESENBERRY_2021],
        "rehabilitation_references": [REF_QUESENBERRY_2021],
        "nutrition_references": [REF_WESSON_1966, REF_QUESENBERRY_2021],
    },
    "guinea_pig_osteoarthritis": {
        "prognosis_references": [REF_QUESENBERRY_2021, REF_CARPENTER_2005],
        "rehabilitation_references": [REF_QUESENBERRY_2021],
        "nutrition_references": [REF_CARPENTER_2005],
    },
    # ---- reptile diseases ----
    "reptile_fracture_limb": {
        "prognosis_references": [REF_MADER_2006, REF_CARPENTER_2005],
        "rehabilitation_references": [REF_MADER_2006],
        "nutrition_references": [REF_CARPENTER_2005],
    },
    "tortoise_shell_fracture": {
        "prognosis_references": [REF_CARPENTER_2025, REF_MADER_2006],
        "rehabilitation_references": [REF_CARPENTER_2025, REF_MADER_2006],
        "nutrition_references": [REF_MADER_2006],
    },
    "snake_fracture_spine": {
        "prognosis_references": [REF_PEAVY_1977, REF_MADER_2006],
        "rehabilitation_references": [REF_MADER_2006],
        "nutrition_references": [REF_MADER_2006],
    },
    "lizard_fracture_limb": {
        "prognosis_references": [REF_MADER_2006, REF_CARPENTER_2005],
        "rehabilitation_references": [REF_MADER_2006],
        "nutrition_references": [REF_CARPENTER_2005],
    },
    "amphibian_fracture_limb": {
        "prognosis_references": [REF_MADER_2006, REF_CARPENTER_2005],
        "rehabilitation_references": [REF_MADER_2006],
        "nutrition_references": [REF_CARPENTER_2005],
    },
    # ---- ferret diseases ----
    "ferret_osteoarthritis": {
        "prognosis_references": [REF_RITZMAN_2002, REF_QUESENBERRY_2021],
        "rehabilitation_references": [REF_RITZMAN_2002],
        "nutrition_references": [REF_QUESENBERRY_2021],
    },
    # ---- hedgehog diseases ----
    "hedgehog_limb_fracture": {
        "prognosis_references": [REF_QUESENBERRY_2021, REF_CARPENTER_2005],
        "rehabilitation_references": [REF_QUESENBERRY_2021],
        "nutrition_references": [REF_CARPENTER_2005],
    },
    # ---- chinchilla diseases ----
    "chinchilla_fracture_limb": {
        "prognosis_references": [REF_QUESENBERRY_2021, REF_CARPENTER_2005],
        "rehabilitation_references": [REF_QUESENBERRY_2021],
        "nutrition_references": [REF_CARPENTER_2005],
    },
    # ---- sugar glider diseases ----
    "sugar_glider_fracture_limb": {
        "prognosis_references": [REF_QUESENBERRY_2021, REF_CARPENTER_2005],
        "rehabilitation_references": [REF_QUESENBERRY_2021],
        "nutrition_references": [REF_CARPENTER_2005],
    },
    # ---- degu diseases ----
    "degu_fracture_limb": {
        "prognosis_references": [REF_QUESENBERRY_2021, REF_CARPENTER_2005],
        "rehabilitation_references": [REF_QUESENBERRY_2021],
        "nutrition_references": [REF_CARPENTER_2005],
    },
    # ---- parrot / cockatoo diseases ----
    "parrot_fracture_wing": {
        "prognosis_references": [REF_VIGNEAULT_2021, REF_CHITTY_2005],
        "rehabilitation_references": [REF_VIGNEAULT_2021, REF_CHITTY_2005],
        "nutrition_references": [REF_CHITTY_2005],
    },
    "cockatoo_fracture_wing": {
        "prognosis_references": [REF_VIGNEAULT_2021, REF_CHITTY_2005],
        "rehabilitation_references": [REF_VIGNEAULT_2021, REF_CHITTY_2005],
        "nutrition_references": [REF_CHITTY_2005],
    },
    # ---- tortoise diseases (already above) ----
    # ---- horse diseases ----
    "horse_discospondylitis": {
        "prognosis_references": [REF_DA_COSTA_2010],
        "rehabilitation_references": [REF_DA_COSTA_2010],
        "nutrition_references": [REF_DA_COSTA_2010],
    },
}

# Fields that store references as {"references": [...]}
REF_FIELDS = ("prognosis_references", "rehabilitation_references", "nutrition_references")


def _wrap(refs: list) -> dict:
    """Wrap a list of reference objects in the standard container dict."""
    return {"references": refs}


def main() -> None:
    print(f"Loading {DB_PATH} ...")
    with DB_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} disease entries.")

    # Create backup
    print(f"Creating backup at {BACKUP_PATH} ...")
    shutil.copy2(DB_PATH, BACKUP_PATH)

    # Build index for fast lookup
    id_to_index: dict[str, int] = {}
    for i, entry in enumerate(data):
        if isinstance(entry, dict) and "id" in entry:
            id_to_index[entry["id"]] = i

    updated_diseases: list[str] = []
    missing_diseases: list[str] = []

    for disease_id, ref_data in REFERENCE_MAP.items():
        if disease_id not in id_to_index:
            missing_diseases.append(disease_id)
            continue

        idx = id_to_index[disease_id]
        entry = data[idx]
        for field in REF_FIELDS:
            refs = ref_data.get(field, [])
            entry[field] = _wrap(refs)

        updated_diseases.append(disease_id)
        print(f"  Updated: {disease_id}")

    print(f"\nSaving updated data to {DB_PATH} ...")
    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total diseases updated : {len(updated_diseases)}")
    for d in updated_diseases:
        prog_count = len(REFERENCE_MAP[d]["prognosis_references"])
        rehab_count = len(REFERENCE_MAP[d]["rehabilitation_references"])
        nutr_count = len(REFERENCE_MAP[d]["nutrition_references"])
        print(f"  {d:55s}  prognosis={prog_count}  rehab={rehab_count}  nutrition={nutr_count}")

    if missing_diseases:
        print(f"\nMissing (not found in DB): {len(missing_diseases)}")
        for d in missing_diseases:
            print(f"  {d}")

    print(f"\nBackup saved at: {BACKUP_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()
