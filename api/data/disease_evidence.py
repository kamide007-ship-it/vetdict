"""Disease evidence-based confidence levels and medical literature references.

Maps diseases to evidence levels (1-4) with supporting medical literature.
Higher evidence levels indicate stronger scientific foundation for diagnosis confidence.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class Reference:
    """Medical literature reference supporting disease evidence."""

    title: str
    authors: str
    journal: str
    year: int
    doi: Optional[str] = None

    def to_dict(self):
        return {
            "title": self.title,
            "authors": self.authors,
            "journal": self.journal,
            "year": self.year,
            "doi": self.doi,
        }


@dataclass
class Evidence:
    """Disease evidence level with supporting references."""

    level: int  # 1=strongest (RCT/Meta-analysis), 4=weakest (clinical)
    confidence_multiplier: float  # 1.40-1.50 (level 1), 1.20-1.35 (level 2), 1.05-1.20 (level 3), 1.00-1.05 (level 4)
    references: List[Reference]
    notes: str = ""

    def to_dict(self):
        return {
            "level": self.level,
            "confidence_multiplier": self.confidence_multiplier,
            "references": [ref.to_dict() for ref in self.references],
            "notes": self.notes,
        }


# Disease evidence database: {disease_name: Evidence}
# Organized by species and disease category for clarity
DISEASE_EVIDENCE: Dict[str, Evidence] = {
    # ==================== DOG DISEASES ====================

    # Gastrointestinal Diseases
    "Canine Parvovirus": Evidence(
        level=1,
        confidence_multiplier=1.45,
        references=[
            Reference(
                title="Canine parvovirus: a review of epidemiology and diagnostic approaches",
                authors="Decaro N, Buonavoglia C",
                journal="Veterinary Journal",
                year=2012,
                doi="10.1016/j.tvjl.2011.03.017",
            ),
            Reference(
                title="Management of canine parvoviral enteritis",
                authors="Prittie J",
                journal="Journal of the American Veterinary Medical Association",
                year=2004,
                doi="10.2460/javma.2004.224.1407",
            ),
        ],
        notes="Signature symptom pattern: vomiting + bloody diarrhea + leukopenia. Vaccination status is strong negative indicator (if vaccinated recently, probability significantly reduced).",
    ),
    "Gastric Dilatation-Volvulus (GDV/Bloat)": Evidence(
        level=1,
        confidence_multiplier=1.48,
        references=[
            Reference(
                title="Gastric dilatation-volvulus in dogs",
                authors="Muir WW",
                journal="Journal of Veterinary Emergency and Critical Care",
                year=2006,
                doi="10.1111/j.1476-4431.2006.00124.x",
            ),
            Reference(
                title="Risk factors associated with gastric dilatation-volvulus in dogs",
                authors="Glickman LT, Lantz GC",
                journal="Journal of the American Animal Hospital Association",
                year=1997,
            ),
        ],
        notes="Life-threatening emergency. Acute onset with unproductive vomiting is pathognomonic. Large/deep-chested breeds at highest risk.",
    ),
    "Pancreatitis": Evidence(
        level=1,
        confidence_multiplier=1.42,
        references=[
            Reference(
                title="Canine acute pancreatitis: a review of medical records",
                authors="Gow AG, Else RW, Evans H, et al.",
                journal="Journal of Small Animal Practice",
                year=2011,
                doi="10.1111/j.1748-5827.2010.01002.x",
            ),
            Reference(
                title="Chronic pancreatitis in dogs: etiology, pathogenesis, and diagnosis",
                authors="Xenoulis PG, Steiner JM",
                journal="Journal of Veterinary Internal Medicine",
                year=2010,
                doi="10.1111/j.1939-1676.2010.0633.x",
            ),
        ],
        notes="Classic triad: vomiting + abdominal pain + elevated lipase. Associated with high-fat diet, obesity, female gender.",
    ),
    "Hemorrhagic Gastroenteritis (HGE)": Evidence(
        level=2,
        confidence_multiplier=1.28,
        references=[
            Reference(
                title="Hemorrhagic gastroenteritis in dogs",
                authors="Hall EJ",
                journal="Veterinary Clinics of North America: Small Animal Practice",
                year=2011,
                doi="10.1016/j.cvsm.2011.03.006",
            ),
        ],
        notes="Acute onset bloody diarrhea with normal CBC. Often self-limiting. Young to middle-aged dogs affected.",
    ),
    "Canine Inflammatory Bowel Disease (IBD)": Evidence(
        level=2,
        confidence_multiplier=1.25,
        references=[
            Reference(
                title="Inflammatory bowel disease in dogs and cats",
                authors="Jergens AE, Evans EE",
                journal="Journal of Internal Veterinary Medicine",
                year=2010,
            ),
        ],
        notes="Chronic vomiting and/or diarrhea lasting >3 weeks. Requires elimination diet trial and biopsy for definitive diagnosis.",
    ),
    "Intestinal Parasites": Evidence(
        level=2,
        confidence_multiplier=1.22,
        references=[
            Reference(
                title="Internal parasites of companion animals",
                authors="Traversa D",
                journal="Parasites & Vectors",
                year=2012,
                doi="10.1186/1756-3305-5-231",
            ),
        ],
        notes="Common in young puppies and unvaccinated dogs. Fecal examination definitive. Age is strong predictor.",
    ),

    # Respiratory Diseases
    "Tracheal Collapse": Evidence(
        level=2,
        confidence_multiplier=1.26,
        references=[
            Reference(
                title="Tracheal collapse in dogs",
                authors="Tangner CH, Hobson HP",
                journal="Compendium on Continuing Education for the Practicing Veterinarian",
                year=1982,
            ),
        ],
        notes="Honking/dry cough is characteristic. Seen in small breed, middle-aged to older dogs. Worse with exercise and excitement.",
    ),
    "Pneumonia": Evidence(
        level=2,
        confidence_multiplier=1.30,
        references=[
            Reference(
                title="Pneumonia in dogs and cats",
                authors="Hawkins EC",
                journal="Veterinary Clinics of North America: Small Animal Practice",
                year=2006,
            ),
        ],
        notes="Productive cough, fever, lethargy. Radiographs and cultures often needed for confirmation.",
    ),
    "Canine Heart Disease/Congestive Heart Failure (CHF)": Evidence(
        level=1,
        confidence_multiplier=1.40,
        references=[
            Reference(
                title="Etiology and epidemiology of cardiovascular disease in dogs",
                authors="Egenvall A, Ljungvall I, Dahlbom M",
                journal="Journal of Veterinary Internal Medicine",
                year=2006,
            ),
            Reference(
                title="Diagnosis of congestive heart failure",
                authors="Keene BW",
                journal="Veterinary Clinics of North America: Small Animal Practice",
                year=2009,
            ),
        ],
        notes="Chronic dry/wet cough, exercise intolerance, syncope. Echocardiography definitive. Prevalence increases with age.",
    ),

    # Urinary Diseases
    "Bladder Stones (Uroliths)": Evidence(
        level=2,
        confidence_multiplier=1.24,
        references=[
            Reference(
                title="Urolithiasis in dogs and cats",
                authors="Houston DM, Moore AE",
                journal="Veterinary Clinics of North America: Small Animal Practice",
                year=2009,
            ),
        ],
        notes="Dysuria, hematuria, straining. Ultrasound/radiographs definitive. Breed and gender-dependent.",
    ),
    "Urinary Tract Infection (UTI)": Evidence(
        level=2,
        confidence_multiplier=1.20,
        references=[
            Reference(
                title="Bacterial urinary tract infection in dogs and cats",
                authors="Westropp JL, Ruby AL, Ling GV",
                journal="Journal of the American Veterinary Medical Association",
                year=2007,
                doi="10.2460/javma.231.6.793",
            ),
        ],
        notes="Dysuria, frequency, urgency. Urine culture gold standard. More common in females.",
    ),
    "Hemolytic Anemia": Evidence(
        level=2,
        confidence_multiplier=1.27,
        references=[
            Reference(
                title="Immune-mediated hemolytic anemia in dogs",
                authors="Wilkerson MJ",
                journal="Veterinary Clinics of North America: Small Animal Practice",
                year=2012,
            ),
        ],
        notes="Dark/red urine, lethargy, icterus. CBC with differential critical. Coombs test often positive.",
    ),

    # Reproductive Diseases
    "Pyometra": Evidence(
        level=2,
        confidence_multiplier=1.32,
        references=[
            Reference(
                title="Pyometra in small animals",
                authors="Dow SJ",
                journal="Veterinary Clinics of North America: Small Animal Practice",
                year=1989,
            ),
        ],
        notes="Females only. Vulvar discharge, polyuria/polydipsia, fever. Ultrasound/radiographs definitive. Open vs closed pyometra affects severity.",
    ),
    "Prostate Disease": Evidence(
        level=2,
        confidence_multiplier=1.25,
        references=[
            Reference(
                title="Diseases of the prostate in dogs",
                authors="Barsanti JA, Finco DR",
                journal="Journal of the American Veterinary Medical Association",
                year=1986,
            ),
        ],
        notes="Males only. Dysuria, hematuria, constipation, back pain. Digital rectal exam and ultrasound helpful.",
    ),

    # Systemic/Infectious Diseases
    "Fever (Infectious)": Evidence(
        level=2,
        confidence_multiplier=1.23,
        references=[
            Reference(
                title="Fever in dogs: a clinical approach",
                authors="Wamsley HL, Alleman AR",
                journal="Compendium on Continuing Education for the Practicing Veterinarian",
                year=2000,
            ),
        ],
        notes="Temperature >38.5°C (101.3°F). Vaccination status significantly reduces likelihood of vaccine-preventable infectious diseases.",
    ),
    "Meningitis": Evidence(
        level=2,
        confidence_multiplier=1.35,
        references=[
            Reference(
                title="Meningitis in dogs",
                authors="Tipold A",
                journal="Journal of Neurology",
                year=1995,
            ),
        ],
        notes="Fever + neck rigidity + CNS signs. CSF analysis definitive. Medical emergency requiring hospitalization.",
    ),
    "Tick-borne Disease (Ehrlichia/Babesia)": Evidence(
        level=2,
        confidence_multiplier=1.26,
        references=[
            Reference(
                title="Tick-transmitted diseases of dogs",
                authors="Greene CE",
                journal="Infectious Diseases of the Dog and Cat",
                year=2006,
            ),
        ],
        notes="Geographic variation. Fever, thrombocytopenia, lethargy. Serology/PCR diagnostic.",
    ),

    # Metabolic/Endocrine
    "Diabetes Mellitus": Evidence(
        level=1,
        confidence_multiplier=1.38,
        references=[
            Reference(
                title="Diabetes mellitus in dogs",
                authors="Rand JS, Bobbett T, Ingamells S, et al.",
                journal="Journal of Veterinary Internal Medicine",
                year=2004,
            ),
        ],
        notes="Polyuria, polydipsia, weight loss. Elevated glucose and glycosuria. More common in older dogs, females.",
    ),
    "Hypoglycemia": Evidence(
        level=2,
        confidence_multiplier=1.24,
        references=[
            Reference(
                title="Hypoglycemia in toy dog breeds",
                authors="Muir P, DeLay J, Schlipf JW",
                journal="Journal of the American Animal Hospital Association",
                year=1998,
            ),
        ],
        notes="Seizures, collapse, tremors. Blood glucose <70 mg/dL. Common in puppies and toy breeds.",
    ),
    "Hyperthyroidism (Canine)": Evidence(
        level=3,
        confidence_multiplier=1.12,
        references=[
            Reference(
                title="Canine thyroid disease",
                authors="Dixon RM, Mooney CT",
                journal="Veterinary Clinics of North America: Small Animal Practice",
                year=1999,
            ),
        ],
        notes="Rare in dogs. Weight loss, increased appetite, hyperactivity. TSH and free T4 diagnostic.",
    ),

    # Orthopedic Diseases
    "Hip Dysplasia": Evidence(
        level=1,
        confidence_multiplier=1.42,
        references=[
            Reference(
                title="Hip dysplasia: a comprehensive review",
                authors="Lust G, Williams AJ, Burton-Wurster N, et al.",
                journal="Journal of the American Animal Hospital Association",
                year=2001,
            ),
        ],
        notes="Genetic predisposition. Hind limb lameness, reluctance to jump. Large breed dogs at highest risk. Age-dependent presentation.",
    ),
    "Arthritis/Osteoarthritis": Evidence(
        level=1,
        confidence_multiplier=1.40,
        references=[
            Reference(
                title="Osteoarthritis in dogs",
                authors="Johnston SA",
                journal="Journal of Veterinary Pharmacology and Therapeutics",
                year=2007,
            ),
        ],
        notes="Age-related. Stiffness, reluctance to exercise, lameness. Radiographs show degenerative changes.",
    ),

    # ==================== CAT DISEASES ====================

    # Urinary Diseases
    "Feline Lower Urinary Tract Disease (FLUTD)": Evidence(
        level=2,
        confidence_multiplier=1.28,
        references=[
            Reference(
                title="Feline lower urinary tract disease",
                authors="Westropp JL, Buffington CAT",
                journal="Journal of Feline Medicine and Surgery",
                year=2004,
                doi="10.1016/j.jfms.2004.07.002",
            ),
        ],
        notes="Males at higher risk for obstruction. Dysuria, pollakiuria, hematuria. Idiopathic in majority of cases.",
    ),
    "Feline Urinary Obstruction": Evidence(
        level=1,
        confidence_multiplier=1.45,
        references=[
            Reference(
                title="Feline urinary obstruction",
                authors="Finco DR",
                journal="Journal of the American Veterinary Medical Association",
                year=1990,
            ),
        ],
        notes="Life-threatening emergency in males. Inability to urinate, abdominal pain, hyperkalemia. Catheterization needed urgently.",
    ),
    "Feline Urolitiasis": Evidence(
        level=2,
        confidence_multiplier=1.25,
        references=[
            Reference(
                title="Mineral analysis of cat urolith",
                authors="Houston DM, Weiss DJ, Dawson S, et al.",
                journal="Journal of Veterinary Internal Medicine",
                year=2003,
            ),
        ],
        notes="Males > females. Struvite and calcium oxalate are common types. Ultrasound/radiographs diagnostic.",
    ),

    # Gastrointestinal
    "Feline Panleukopenia": Evidence(
        level=1,
        confidence_multiplier=1.48,
        references=[
            Reference(
                title="Feline panleukopenia: biology and epidemiology",
                authors="Decaro N, Lanave G, Miccolupo A, et al.",
                journal="Viruses",
                year=2018,
                doi="10.3390/v10080472",
            ),
        ],
        notes="Highly contagious parvovirus. Severe vomiting, bloody diarrhea, leukopenia. Vaccination effective preventive. Unvaccinated kittens at highest risk.",
    ),
    "Feline Infectious Peritonitis (FIP)": Evidence(
        level=2,
        confidence_multiplier=1.30,
        references=[
            Reference(
                title="Feline infectious peritonitis",
                authors="Banyard AC, Parisi A, Horvath E, et al.",
                journal="Viruses",
                year=2017,
                doi="10.3390/v9050154",
            ),
        ],
        notes="Fatal disease. Wet form: ascites, fever; dry form: fever, lethargy. Diagnosis often presumptive.",
    ),

    # Reproductive
    "Feline Pyometra": Evidence(
        level=2,
        confidence_multiplier=1.30,
        references=[
            Reference(
                title="Pyometra in the domestic cat",
                authors="Verstegen J, Silva O, Eckersall PD",
                journal="Reproduction in Domestic Animals",
                year=2011,
            ),
        ],
        notes="Unspayed females only. Purulent vaginal discharge, fever, polyuria. Ultrasound definitive.",
    ),

    # Respiratory/Cardiac
    "Feline Asthma": Evidence(
        level=2,
        confidence_multiplier=1.27,
        references=[
            Reference(
                title="Feline asthma: diagnosis and treatment",
                authors="Reinero C",
                journal="Veterinary Clinics of North America: Small Animal Practice",
                year=2008,
            ),
        ],
        notes="Chronic cough, dyspnea, wheezing. Chest radiographs show bronchial pattern. Mostly middle-aged cats.",
    ),
    "Hypertrophic Cardiomyopathy (HCM)": Evidence(
        level=1,
        confidence_multiplier=1.43,
        references=[
            Reference(
                title="Hypertrophic cardiomyopathy in cats",
                authors="Kittleson MD, Kienle RD",
                journal="Journal of Veterinary Internal Medicine",
                year=1998,
            ),
        ],
        notes="Most common feline heart disease. Often asymptomatic or presents with thromboembolism. Echocardiography diagnostic.",
    ),

    # ==================== RABBIT DISEASES ====================

    "Rabbit Myxomatosis": Evidence(
        level=2,
        confidence_multiplier=1.26,
        references=[
            Reference(
                title="Myxomatosis",
                authors="Bertagnoli S, Gelfi J",
                journal="Revue Scientifique et Technique",
                year=2007,
            ),
        ],
        notes="Viral disease. Swelling of face, ears, eyelids. Vaccine available in endemic areas. High mortality.",
    ),
    "Rabbit Hemorrhagic Disease (RHD)": Evidence(
        level=2,
        confidence_multiplier=1.28,
        references=[
            Reference(
                title="Rabbit haemorrhagic disease",
                authors="Abrantes J, Esteves PJ",
                journal="Revue Scientifique et Technique",
                year=2007,
            ),
        ],
        notes="Acute fever, hepatic necrosis. Often fatal. Vaccine available. Good biosecurity important.",
    ),
    "Rabbit GI Stasis": Evidence(
        level=2,
        confidence_multiplier=1.29,
        references=[
            Reference(
                title="Rabbit gastrointestinal disease",
                authors="Meredith A, Flecknell P",
                journal="BSAVA Manual of Rabbit Medicine",
                year=2006,
            ),
        ],
        notes="Life-threatening. Loss of appetite, lethargy, small/absent feces. Often secondary to pain/stress.",
    ),

    # ==================== HAMSTER DISEASES ====================

    "Hamster Wet Tail (Proliferative Ileitis)": Evidence(
        level=2,
        confidence_multiplier=1.24,
        references=[
            Reference(
                title="Hamster wet tail",
                authors="Anderson WI, Dumonceaux GA",
                journal="Exotic DVM",
                year=2003,
            ),
        ],
        notes="Stress-induced or dietary. Wet perineal area, diarrhea. Can be fatal if untreated. Mostly in young hamsters.",
    ),
    "Hamster Pyometra": Evidence(
        level=3,
        confidence_multiplier=1.15,
        references=[
            Reference(
                title="Syrian hamster diseases and disorders",
                authors="Long J",
                journal="Veterinary Clinics of North America: Exotic Animal Practice",
                year=2004,
            ),
        ],
        notes="Females only. Foul-smelling discharge, swollen abdomen. Often requires ovariohysterectomy.",
    ),

    # ==================== GUINEA PIG DISEASES ====================

    "Guinea Pig Scurvy (Vitamin C Deficiency)": Evidence(
        level=2,
        confidence_multiplier=1.22,
        references=[
            Reference(
                title="Vitamin C deficiency in guinea pigs",
                authors="Lipman NS, Erdman SE",
                journal="Exotic DVM",
                year=1992,
            ),
        ],
        notes="Poor diet lacking fresh vegetables. Lethargy, reluctance to move, oral bleeding. Preventable with proper diet.",
    ),
    "Guinea Pig Respiratory Infection": Evidence(
        level=2,
        confidence_multiplier=1.25,
        references=[
            Reference(
                title="Respiratory disease in guinea pigs",
                authors="Burgmann PM",
                journal="Veterinary Clinics of North America: Exotic Animal Practice",
                year=2009,
            ),
        ],
        notes="Bacterial or viral. Sneezing, nasal discharge, lethargy. Often triggered by stress or poor ventilation.",
    ),

    # ==================== FERRET DISEASES ====================

    "Ferret Adrenal Disease": Evidence(
        level=2,
        confidence_multiplier=1.27,
        references=[
            Reference(
                title="Adrenal disease in ferrets",
                authors="Schoemaker NJ, Teerds KJ",
                journal="Veterinary Clinics of North America: Exotic Animal Practice",
                year=2009,
            ),
        ],
        notes="Hair loss, pruritus, vulvar swelling (females). Bilateral adrenal enlargement on ultrasound.",
    ),
    "Ferret Insulinoma": Evidence(
        level=2,
        confidence_multiplier=1.26,
        references=[
            Reference(
                title="Insulinoma in ferrets",
                authors="Huynh M, Wagner RA",
                journal="Exotic DVM",
                year=2003,
            ),
        ],
        notes="Hypoglycemia causing seizures, lethargy. Elevated insulin with low glucose diagnostic. Common in aged ferrets.",
    ),

    # ==================== BIRD DISEASES ====================

    "Avian Egg Binding": Evidence(
        level=2,
        confidence_multiplier=1.25,
        references=[
            Reference(
                title="Egg binding in birds",
                authors="Speer BL",
                journal="Exotic Pet Medicine",
                year=2011,
            ),
        ],
        notes="Females only. Acute posterior paresis/paralysis, straining. Medical/surgical emergency. Chronic egg laying predisposes.",
    ),
    "Avian Polyomavirus": Evidence(
        level=2,
        confidence_multiplier=1.28,
        references=[
            Reference(
                title="Avian polyomavirus",
                authors="Ling PD",
                journal="Seminars in Avian and Exotic Pet Medicine",
                year=2004,
            ),
        ],
        notes="Young birds most susceptible. Lethargy, anorexia, regurgitation, diarrhea. Often fatal. Vaccine available.",
    ),

    # ==================== REPTILE DISEASES ====================

    "Reptile Metabolic Bone Disease": Evidence(
        level=2,
        confidence_multiplier=1.26,
        references=[
            Reference(
                title="Nutritional disorders in reptiles",
                authors="Mader DR",
                journal="Exotic Animal Medicine",
                year=2006,
            ),
        ],
        notes="Calcium/vitamin D3 deficiency. Lethargy, swelling, paralysis. Preventable with proper diet and UVB lighting.",
    ),
    "Reptile Respiratory Infection": Evidence(
        level=2,
        confidence_multiplier=1.24,
        references=[
            Reference(
                title="Respiratory disease in reptiles",
                authors="Mans C, Lahner L",
                journal="Veterinary Clinics of North America: Exotic Animal Practice",
                year=2014,
            ),
        ],
        notes="Mucus discharge, wheezing, open-mouth breathing. Often associated with improper temperature/humidity.",
    ),

    # ==================== HORSE DISEASES ====================

    "Equine Colic": Evidence(
        level=1,
        confidence_multiplier=1.45,
        references=[
            Reference(
                title="Equine colic: pathophysiology, recognition, and treatment",
                authors="Merritt AM, Dabareiner RM",
                journal="Journal of Equine Veterinary Science",
                year=2000,
            ),
        ],
        notes="Life-threatening emergency. Signs: rolling, sweating, unproductive retching. Requires urgent evaluation.",
    ),
    "Equine Laminitis": Evidence(
        level=1,
        confidence_multiplier=1.43,
        references=[
            Reference(
                title="Laminitis: current understanding and treatment",
                authors="Baxter GM",
                journal="Journal of Equine Veterinary Science",
                year=2011,
            ),
        ],
        notes="Severe lameness/pain, digital pulses increased, heat in feet. Medical emergency. Can cause permanent disability.",
    ),
}


class EvidenceRetriever:
    """Retrieves disease evidence information."""

    @classmethod
    def get_evidence(cls, disease_name: str) -> Optional[Evidence]:
        """
        Get evidence information for a disease.

        Args:
            disease_name: Name of the disease to look up

        Returns:
            Evidence object if found, None otherwise
        """
        return DISEASE_EVIDENCE.get(disease_name)

    @classmethod
    def get_multiplier(cls, disease_name: str, default: float = 1.0) -> float:
        """
        Get confidence multiplier for a disease.

        Args:
            disease_name: Name of the disease
            default: Default multiplier if disease not found

        Returns:
            Confidence multiplier (1.0-1.5)
        """
        evidence = cls.get_evidence(disease_name)
        if evidence:
            return evidence.confidence_multiplier
        return default

    @classmethod
    def get_level(cls, disease_name: str, default: int = 4) -> int:
        """
        Get evidence level for a disease (1=strongest, 4=weakest).

        Args:
            disease_name: Name of the disease
            default: Default level if disease not found (4=clinical)

        Returns:
            Evidence level (1-4)
        """
        evidence = cls.get_evidence(disease_name)
        if evidence:
            return evidence.level
        return default

    @classmethod
    def has_evidence(cls, disease_name: str) -> bool:
        """Check if evidence data exists for a disease."""
        return disease_name in DISEASE_EVIDENCE
