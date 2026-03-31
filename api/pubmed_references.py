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
}


def get_references_for_disease(disease_name: str) -> list[dict]:
    """Return PubMed references for a disease name (case-insensitive partial match)."""
    name_lower = disease_name.lower()
    for key, refs in DISEASE_REFERENCES.items():
        if key in name_lower or name_lower in key:
            return refs
    return []
