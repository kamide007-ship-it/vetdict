"""Clinical-tone regression guards for system-generated triage guidance.

VetDict targets veterinarians and veterinary students, so the advice the
platform generates must frame the next clinical action (stabilization,
workup, referral) rather than instructing the reader to "see a vet."

These tests lock in that the severity-keyed triage dictionaries stay
clinician-facing and bilingual.
"""

from api.species.helpers import ADVICE as GENERIC_ADVICE
from api.symptom_checker import _ADVICE as CHECKER_ADVICE

# Phrases that address a pet owner rather than the attending clinician.
OWNER_FACING_JA = (
    "獣医師の診察を受け",
    "獣医師に相談",
    "獣医師にご相談",
    "動物病院を受診",
    "受診してください",
)
OWNER_FACING_EN = (
    "consult a veterinarian",
    "consult your veterinarian",
    "seek immediate veterinary",
    "see a veterinarian",
    "examined by a veterinarian",
    "schedule an appointment",
)

SEVERITIES = ("low", "moderate", "high", "emergency")


class TestTriageAdviceTone:
    """Both triage dictionaries must be clinician-facing and complete."""

    def _check(self, advice):
        for severity in SEVERITIES:
            assert severity in advice, f"missing severity: {severity}"
            pair = advice[severity]
            ja = pair["ja"]
            en = pair["en"].lower()
            assert ja.strip(), f"{severity} JA empty"
            assert en.strip(), f"{severity} EN empty"
            for phrase in OWNER_FACING_JA:
                assert phrase not in ja, f"{severity} JA still owner-facing: {phrase}"
            for phrase in OWNER_FACING_EN:
                assert phrase not in en, f"{severity} EN still owner-facing: {phrase}"

    def test_symptom_checker_advice_is_clinician_facing(self):
        self._check(CHECKER_ADVICE)

    def test_generic_species_advice_is_clinician_facing(self):
        self._check(GENERIC_ADVICE)
