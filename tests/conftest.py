import os
import sys
import tempfile
from pathlib import Path

import pytest

# Ensure repo root is importable.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Ensure SECRET_KEY and debug mode are set BEFORE any app module imports
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("FLASK_DEBUG", "1")

# Set test database path BEFORE any module imports
_test_db_fd, _test_db_path = tempfile.mkstemp(suffix=".db")
os.close(_test_db_fd)
os.environ["VETDICT_DB_PATH"] = _test_db_path

# Initialize test database schema
from api.database import init_db

init_db(_test_db_path)


@pytest.fixture()
def temp_instance(tmp_path, monkeypatch):
    """Provide an isolated instance/ and HOME for tests."""
    inst = tmp_path / "instance"
    inst.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("RECO3_INSTANCE_DIR", str(inst))

    # Isolate HOME for reco3_agent (~/.reco3)
    home = tmp_path / "home"
    home.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("HOME", str(home))

    return inst


@pytest.fixture(autouse=True)
def clear_test_db():
    """Clear and populate test database for each test."""
    import sqlite3

    db_path = os.environ.get("VETDICT_DB_PATH", _test_db_path)
    with sqlite3.connect(db_path) as conn:
        conn.executescript("""
            DELETE FROM diseases;
            DELETE FROM symptoms;
            DELETE FROM drugs;
            DELETE FROM drug_species_info;
        """)

        # Insert test data for common species
        test_diseases = [
            ("dog_disease_1", "dog", "Canine Parvovirus", "犬パルボウイルス感染症", "Viral infection", "ウイルス感染症", "Dehydration and enteritis", "脱水と腸炎", "Causes", "原因", "Supportive care", "対症療法", "Prevention through vaccination", "ワクチン接種による予防", "Good with treatment", "適切な治療で良好", "high", '["symptom_1","symptom_2"]', '["blood_work"]', '["acute"]', '["juvenile"]'),
            ("cat_disease_1", "cat", "Feline Leukemia", "猫白血病", "Viral infection", "ウイルス感染症", "Immunosuppression", "免疫抑制", "Causes", "原因", "Antiviral therapy", "抗ウイルス療法", "Isolation and supportive care", "隔離と対症療法", "Guarded", "不確定", "high", '["symptom_3"]', '["serology"]', '["chronic"]', '["adult"]'),
            ("horse_disease_1", "horse", "Equine Influenza", "馬インフルエンザ", "Viral respiratory infection", "ウイルス性呼吸器感染症", "Coughing and fever", "咳と発熱", "Causes", "原因", "Antiviral and rest", "抗ウイルス剤と休息", "Vaccination and hygiene", "ワクチン接種と衛生管理", "Good with rest", "休息で良好", "moderate", '["symptom_4"]', '["culture"]', '["seasonal"]', '["adult"]'),
        ]

        for disease_data in test_diseases:
            conn.execute(
                """INSERT INTO diseases
                   (id, species, name, name_ja, description, description_ja,
                    pathophysiology, pathophysiology_ja, causes, causes_ja,
                    treatment, treatment_ja, prevention, prevention_ja,
                    prognosis, prognosis_ja, urgency, symptoms, recommended_tests,
                    onset_pattern, age_predisposition, enriched_at, enrichment_phase)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,NULL,NULL)""",
                disease_data
            )

        # Insert test symptoms for various species
        test_symptoms = [
            ("symptom_1", "Vomiting", "嘔吐", "dog", 1.0),
            ("symptom_2", "Diarrhea", "下痢", "dog", 1.0),
            ("appetite_loss", "Appetite Loss", "食欲不振", "dog", 1.0),
            ("symptom_3", "Lymphadenopathy", "リンパ節腫大", "cat", 1.0),
            ("cyanosis", "Cyanosis", "チアノーゼ", "cat", 1.0),
            ("symptom_4", "Cough", "咳", "horse", 1.0),
            ("limb_bucked_shin", "Bucked Shin", "すねの前面が腫れている（バックドシン）", "horse", 1.0),
        ]

        for symptom_data in test_symptoms:
            conn.execute(
                """INSERT INTO symptoms (id, name_en, name_ja, species, clinical_weight)
                   VALUES (?,?,?,?,?)""",
                symptom_data
            )

        conn.commit()

    yield
