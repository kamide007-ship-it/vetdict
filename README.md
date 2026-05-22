# VetDict - Veterinary Differential Diagnosis Platform

A clinical decision support platform for veterinarians and veterinary students — **7,000+ diseases** across **21 animal species**, **610+ drugs** with species-specific safety data, **188 sedation/anesthesia protocols**, and an AI integrity control layer (RECO2/RECO3).

> Built by a practicing veterinarian. Bilingual (Japanese / English).

---

## Key Numbers

| Metric | Value |
|--------|-------|
| Animal Species | 21 |
| Diseases | 7,000+ |
| Drugs | 610+ |
| Drug Categories | 49 |
| Sedation/Anesthesia Protocols | 188 |
| Symptoms | 52 |
| Breeds (cat) | 15 |
| API Endpoints | 28+ |

## Features

### Differential Diagnosis Engine
- Symptom-based analysis with clinical likelihood ratios
- Support for age stage, breed, and onset type (acute / subacute / chronic)
- Real-time animated disease counts on the landing page

### Disease Database
- 7,000+ diseases with Japanese / English bilingual descriptions
- 21 species: Dog (622), Cat (550), Horse (621), Rabbit (452), Bird (551), Parakeet (459), Parrot (283), Guinea Pig (346), Hamster (321), Chinchilla (278), Ferret (277), Hedgehog (244), Sugar Glider (221), Degu (201), Reptile (286), Tortoise (288), Snake (248), Lizard (250), Amphibian (258), Fish (45), Exotic Other (292)

### Drug Dictionary
- 610+ drugs across 49 categories with species-specific dosage, safety, routes, formulations, and drug interactions
- Includes biologics (Cytopoint, Librela, Solensia), antivirals (GS-441524, molnupiravir), and ECVN-formulated nutraceuticals

### Sedation & Anesthesia Protocols
- 188 protocols across all 21 species (sedation, premedication, induction, maintenance, locoregional, monitoring, recovery, emergency)
- Includes non-narcotic Japanese-market protocols (medetomidine/dexmedetomidine + butorphanol + midazolam)
- Drug–disease contraindication warnings (31 rules)

### Bilingual Mode (JP / EN)
- One-click language toggle (JP / EN) in the header
- All UI labels, placeholders, error messages, and data fields switch between Japanese and English
- Language preference saved in localStorage

### Health Checker UI
- Checkbox-based symptom selection with breed-specific risk analysis
- Interactive single-page application with responsive design

### Diagnostic Chat
- Conversational diagnostic interface powered by LLM

### AI Integrity Control (RECO2 / RECO3)
- **Input Gate** — Detects ambiguity, overconfident assertions, emotional language, and unrealistic expectations
- **Output Gate** — Checks for unsupported claims, missing evidence, contradictions, and inappropriate content
- **Orchestrator** — Temperature-controlled generation with automatic regeneration when confidence (psi) falls below threshold

## Accessibility & UI/UX

- WCAG 2.1 AA compliant (ARIA roles, keyboard navigation, skip link)
- `prefers-reduced-motion` support
- Responsive design: desktop / tablet (1024px) / mobile (600px)
- Hamburger menu for mobile
- URL hash routing with `history.replaceState`

## Architecture

```
vetdict/
├── app.py                  # Entry point
├── api/
│   ├── vetdict_api.py      # Flask app & routes (v5.0.0)
│   ├── symptom_checker.py  # Dog symptom analysis
│   ├── species_analyzer.py # Multi-species analyzer
│   ├── health_checker.py   # Checkbox UI blueprint
│   ├── diagnostic_chat.py  # Chat interface
│   ├── drug_dictionary.py  # Drug database
│   └── species/            # 21 species disease modules
├── reco2/                  # AI integrity control layer
│   ├── engine.py           # Evaluation algorithm (psi scoring)
│   ├── input_gate.py       # Input risk analysis
│   ├── output_gate.py      # Output quality checks
│   ├── orchestrator.py     # Full pipeline orchestration
│   └── llm_adapter.py      # LLM abstraction
├── templates/
│   └── index.html          # Single-page application
├── tests/                  # Test suite
├── render.yaml             # Render.com deployment
└── requirements.txt
```

## Tech Stack

- **Backend**: Python / Flask / flask-cors
- **Frontend**: Vanilla HTML / CSS / JS (single-page)
- **Deployment**: Render.com (gunicorn)
- **AI Safety**: RECO2 / RECO3 integrity layer

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000`.

## Deployment (Render.com)

The project includes `render.yaml` for automatic deployment.

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Flask secret key (auto-generated) |
| `FLASK_DEBUG` | `0` for production |
| `PYTHON_VERSION` | `3.11.0` |

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/health` | Health check & feature availability |
| GET | `/api/species-stats` | Disease/drug counts per species |
| POST | `/api/analyze-symptoms` | Differential diagnosis |
| GET | `/api/breeds/<species>` | Breed list for a species |
| GET | `/api/drugs` | Drug dictionary |
| POST | `/api/r3/chat` | Diagnostic chat with RECO3 |
| POST | `/api/r3/analyze_input` | Input risk analysis |
| POST | `/api/r3/analyze_output` | Output quality analysis |

## References

Disease and drug data compiled from 190+ veterinary references including Merck Veterinary Manual, Plumb's Veterinary Drug Handbook, BSAVA manuals, Lumb & Jones (5th ed.), Carpenter's Exotic Animal Formulary (6th ed.), Ettinger's Textbook of Veterinary Internal Medicine (8th ed.), AAHA/AVMA/WSAVA clinical guidelines, ISCAID 2019 UTI guidelines, and species-specific clinical texts.

## Sponsor

**[Equine & Canine Vet Nutrition](https://www.caninevet.jp/)**
Veterinarian-formulated supplements manufactured in Japan. Passed Racing Chemistry Laboratory testing.

- [Horse Supplements (evet-nutrition.com)](https://www.evet-nutrition.com/)
- [Dog Supplements (caninevet.jp)](https://www.caninevet.jp/)

## Developer

**Kentaro Kamide, DVM** — Minamisoma Animal Clinic

- [minamisoma-vet.com](https://www.minamisoma-vet.com/)
- [Instagram](https://www.instagram.com/k.kamide.canine_vet_nutrition/?hl=ja)

## License

All rights reserved.
