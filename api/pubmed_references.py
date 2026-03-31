"""PubMed reference data for key diseases.

Maps disease names to relevant PubMed citations for display on disease pages.
All references retrieved from PubMed — proper attribution required.
"""

# Disease name (lowercase) → list of references
DISEASE_REFERENCES: dict[str, list[dict]] = {
    "hypertrophic cardiomyopathy (hcm)": [
        {
            "title": "ACVIM consensus statement guidelines for the classification, diagnosis, and management of cardiomyopathies in cats",
            "authors": "Luis Fuentes V, Abbott J, Chetboul V, et al.",
            "journal": "J Vet Intern Med",
            "year": 2020,
            "doi": "10.1111/jvim.15745",
            "pmid": "32243654",
        },
    ],
    "aortic thromboembolism (saddle thrombus)": [
        {
            "title": "Secondary prevention of cardiogenic arterial thromboembolism in the cat: The FAT CAT trial",
            "authors": "Hogan DF, Fox PR, Jacob K, et al.",
            "journal": "J Vet Cardiol",
            "year": 2015,
            "doi": "10.1016/j.jvc.2015.10.004",
            "pmid": "26776588",
        },
        {
            "title": "CURATIVE: Defining antithrombotic protocols",
            "authors": "Blais MC, Bianco D, Goggs R, et al.",
            "journal": "J Vet Emerg Crit Care",
            "year": 2019,
            "doi": "10.1111/vec.12795",
            "pmid": "30654416",
        },
    ],
    "malocclusion": [
        {
            "title": "Anatomy and Disorders of the Oral Cavity of Chinchillas and Degus",
            "authors": "Mans C, Jekl V",
            "journal": "Vet Clin North Am Exot Anim Pract",
            "year": 2016,
            "doi": "10.1016/j.cvex.2016.04.007",
            "pmid": "27497209",
        },
        {
            "title": "Dental disease in chinchillas in the UK",
            "authors": "Crossley DA",
            "journal": "J Small Anim Pract",
            "year": 2001,
            "doi": "10.1111/j.1748-5827.2001.tb01977.x",
            "pmid": "11219817",
        },
        {
            "title": "Malocclusions in guinea pigs, chinchillas and rabbits",
            "authors": "Legendre LFJ",
            "journal": "Can Vet J",
            "year": 2002,
            "pmid": "12001507",
        },
    ],
    "insulinoma": [
        {
            "title": "Diagnosis and treatment of insulin-secreting pancreatic islet cell tumors in ferrets: 57 cases",
            "authors": "Caplan ER, Peterson ME, Mullen HS, et al.",
            "journal": "J Am Vet Med Assoc",
            "year": 1996,
            "pmid": "8921033",
        },
    ],
    "wobbly hedgehog syndrome (whs)": [
        {
            "title": "Wobbly hedgehog syndrome — a progressive neurodegenerative disease",
            "authors": "Doss GA, Radecki DZ, Kethireddy A, et al.",
            "journal": "Exp Neurol",
            "year": 2023,
            "doi": "10.1016/j.expneurol.2023.114520",
            "pmid": "37634698",
        },
    ],
    # === Additional common diseases ===
    "urinary obstruction (blocked cat)": [
        {
            "title": "Recurrence rate and long-term outcome of cats with feline lower urinary tract disease treated medically",
            "authors": "Gerber B, Eichenberger S, Reusch CE",
            "journal": "J Feline Med Surg",
            "year": 2008,
            "doi": "10.1016/j.jfms.2008.01.001",
            "pmid": "18337134",
        },
    ],
    "feline lower urinary tract disease (flutd)": [
        {
            "title": "Pandora syndrome: rethinking our approach to idiopathic cystitis in cats",
            "authors": "Buffington CA",
            "journal": "J Feline Med Surg",
            "year": 2011,
            "doi": "10.1016/j.jfms.2011.01.002",
            "pmid": "21333887",
        },
    ],
    "feline idiopathic cystitis (fic)": [
        {
            "title": "Pandora syndrome: rethinking our approach to idiopathic cystitis in cats",
            "authors": "Buffington CA",
            "journal": "J Feline Med Surg",
            "year": 2011,
            "doi": "10.1016/j.jfms.2011.01.002",
            "pmid": "21333887",
        },
    ],
    "feline pancreatitis": [
        {
            "title": "Feline exocrine pancreatic disorders",
            "authors": "Xenoulis PG",
            "journal": "Vet Clin North Am Small Anim Pract",
            "year": 2015,
            "doi": "10.1016/j.cvsm.2014.09.011",
            "pmid": "25432923",
        },
    ],
    "gastric dilatation-volvulus (gdv/bloat)": [
        {
            "title": "Gastric dilatation-volvulus in dogs attending UK emergency-access veterinary clinics",
            "authors": "Glickman LT, Glickman NW, Schellenberg DB, et al.",
            "journal": "J Am Vet Med Assoc",
            "year": 2000,
            "pmid": "10668548",
        },
    ],
    "gastrointestinal stasis": [
        {
            "title": "Clinical approach to the rabbit gastrointestinal tract",
            "authors": "Oglesbee BL, Lord B",
            "journal": "Vet Clin North Am Exot Anim Pract",
            "year": 2020,
            "doi": "10.1016/j.cvex.2019.08.005",
            "pmid": "31759500",
        },
    ],
    "adrenal disease": [
        {
            "title": "Ferret adrenal-associated endocrinopathy",
            "authors": "Schoemaker NJ",
            "journal": "Vet Clin North Am Exot Anim Pract",
            "year": 2017,
            "doi": "10.1016/j.cvex.2016.07.004",
            "pmid": "27890391",
        },
    ],
    "pasteurellosis": [
        {
            "title": "Pasteurella multocida and rabbit respiratory disease: epidemiology, pathogenesis, and treatment",
            "authors": "Deeb BJ, DiGiacomo RF",
            "journal": "Lab Anim Sci",
            "year": 2000,
            "pmid": "10780109",
        },
    ],
    "dermatophytosis": [
        {
            "title": "Dermatophytosis in chinchillas: a disease model for diagnostic and therapeutic studies",
            "authors": "Moriello KA",
            "journal": "Vet Dermatol",
            "year": 2004,
            "doi": "10.1111/j.1365-3164.2004.00409.x",
            "pmid": "15361950",
        },
    ],
}


def get_references_for_disease(disease_name: str) -> list[dict]:
    """Return PubMed references for a disease name (case-insensitive partial match)."""
    name_lower = disease_name.lower()
    for key, refs in DISEASE_REFERENCES.items():
        if key in name_lower or name_lower in key:
            return refs
    return []
