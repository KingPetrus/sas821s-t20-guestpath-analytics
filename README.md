# GuestPath Analytics
**T20 · Hospitality Guest-System Compromise and Payment-Data Security Analytics**
SAS821S Capstone — Namibia University of Science and Technology

- **Mfon Charten Petrus** (221017984) — Data and Modelling Lead
- **TJIRI NDJARAKANAi** (219067058 ) — Security Engineering and Intelligence Lead
- Lecturer: Prof. Atlee Gamundani

## What this project does

Reconstructs a plausible attack path from guest Wi-Fi / a compromised staff account into a hotel's
PMS and payment-gateway environment using public and synthetic data, and quantifies how much a
segmentation / Zero Trust control would reduce that risk. See `docs/charter.docx` for the full
project charter, including problem statement, objectives, methods, and reference list.

## Repository structure

```
├── docs/
│   └── charter.docx              # Full project charter
├── notebooks/
│   └── 01_starter_pipeline.ipynb # Phase 0/1 starter: anomaly detection + segmentation simulation
├── data/                          # Generated/downloaded data (gitignored — do not commit raw datasets)
├── src/                           # Reusable pipeline code, factored out of notebooks as it matures
├── dashboard/                     # Streamlit app (Phase 4)
├── requirements.txt
└── README.md
```

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebooks/01_starter_pipeline.ipynb
```

## Work plan (see charter Section 10 for full detail)

| Task | Owner | Target |
|---|---|---|
| 1. Charter, environment setup, data acquisition | Both | 10 Aug 2026 |
| 2. Data preparation & baseline EDA | Mfon | 24 Aug 2026 |
| 3. Session/identity ML & UEBA anomaly modelling | Mfon | 14 Sep 2026 |
| 4. Segmentation, lateral-movement & ATT&CK mapping | Tjiri | 14 Sep 2026 |
| 5. Phishing text-mining, breach-risk modelling, simulation | Both | 12 Oct 2026 |
| 6. Prototype dashboard, integration, final report | Both | TBD |

## Branching convention

- `main` — always working, always demoable
- `Mfon/*` — feature branches for modelling/anomaly work
- `Tjiri/*` — feature branches for segmentation/ATT&CK work
- Open a pull request into `main` before merging, even working solo on a branch — gives you both a
  reviewable history for the RACI evidence trail (charter Section 9).

## Data & ethics note

No real hotel, guest, or payment data is used anywhere in this repository — see charter Section 6.
All datasets are public (LANL, CICIDS2017, Enron, Nazario) or synthetically generated. Do not commit
raw downloaded datasets to git; `data/` is git-ignored for this reason.
