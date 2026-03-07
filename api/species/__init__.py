# This package contains species-specific disease dictionaries and analysis functions.
# Each module under this package should define a `DISEASES` list containing
# dictionaries describing diseases for the species, a `SYMPTOM_NAMES` mapping
# of symptom identifiers to bilingual names, and an `analyze_symptoms` function
# that takes a list of symptom identifiers and returns an analysis result in
# the same format as the dog symptom checker.
