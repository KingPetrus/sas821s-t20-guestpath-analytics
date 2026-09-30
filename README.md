# GuestPath Analytics
**T20 · Hospitality Guest-System Compromise and Payment-Data Security Analytics**
SAS821S Capstone — Namibia University of Science and Technology

- **Mfon Charten Petrus** (221017984)-  Data and Modelling Lead
- **TJIRI NDJARAKANAi** (219067058 )- Security Engineering and Intelligence Lead
- **Lecturer: Prof. Atlee Gamundani**

## What this project does

Reconstructs a plausible attack path from guest Wi-Fi / a compromised staff account into a hotel's
PMS and payment-gateway environment using public and synthetic data, and quantifies how much a
segmentation / Zero Trust control would reduce that risk. See `docs/charter.docx` for the full
project charter, including problem statement, objectives, methods, and reference list.

## Repository structure

sas821s-clean/
├── .agents/
├── .git/
├── artifacts/
│   ├── enriched_pms_events.csv
│   └── prioritized_risk_output.csv
├── dashboard/
│   ├── data/
│   │   ├── adversarial_test_results.csv
│   │   ├── attack_path_techniques.csv
│   │   ├── attck_layer.json
│   │   ├── composite_risk_score.json
│   │   ├── incident_timeline.csv
│   │   ├── segmentation_comparison.json
│   │   ├── simulation_results.json
│   │   ├── synthetic_pms_events.csv
│   │   └── user_anomaly_scores.csv
│   ├── app.py
│   └── test_guestpath.py
├── data/
├── docs/
│   ├── SAS821S_MC_Petrus_221017984_T_Ndjarakana_... (.docx / .pdf files)
│   └── ...
├── intelligence/
│   ├── behavioral_anomaly_scatter.png
│   ├── control_simulation_report.json
│   ├── mitre_ttp_distribution.png
│   └── top_risky_users.png
├── models/
│   ├── phishing_rf_model.pkl
│   └── tfidf_vectorizer.pkl
├── notebooks/
│   ├── .ipynb_checkpoints/
│   ├── data/
│   │   ├── .ipynb_checkpoints/
│   │   ├── Network Intrusion dataset(CIC-IDS- 2017)/
│   │   ├── synthetic/
│   │   ├── The-Enron-Email-Dataset/
│   │   ├── adversarial_test_results.csv
│   │   ├── attack_path_techniques.csv
│   │   ├── attck_layer.json
│   │   ├── auth.txt.gz
│   │   ├── composite_risk_score.json
│   │   ├── incident_timeline.csv
│   │   ├── nazario_phishing.mbox
│   │   ├── Network Intrusion dataset(CIC-IDS- 2017).zip
│   │   ├── phishing3.zip
│   │   ├── redteam.txt.gz
│   │   ├── segmentation_comparison.json
│   │   ├── simulation_results.json
│   │   ├── synthetic_payment_logs.csv
│   │   ├── synthetic_pms_events.csv
│   │   ├── synthetic_pms_logs.csv
│   │   └── The-Enron-Email-Dataset.zip
│   ├── intelligence/
│   ├── sas821s-t20-guestpath-analytics/
│   ├── 01_Phishing_Text_Mining_GuestPath.ipynb
│   └── GuestPath_WITH_RESULTS.ipynb
├── src/
│   └── generate_pms_and_payment.py
├── .gitignore
├── check_real_data_usage.py
├── check_real_data_usage_v2.py
├── check_zips.py
├── extract_real_data.py
├── guestpath_security_analytics_and_intelligence.ipynb
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
| 5. Prototype dashboard, integration, final report | Both | 22 Sep 2026 |
| 6. Phishing text-mining, breach-risk modelling, simulation | Both | 27 Sep 2026 |

## Branching convention

- `main` — always working, always demoable
- `Mfon/*` — feature branches for modelling/anomaly work
- `Tjiri/*` — feature branches for segmentation/ATT&CK work
- Open a pull request into `main` before merging, even working solo on a branch — gives you both a
  reviewable history for the RACI evidence trail (charter Section 9).

## Data & ethics note

No real hotel, guest, or payment data is used anywhere in this repository — see charter Section 6.
All datasets are public (LANL, CICIDS2017, Enron, Nazario) or synthetically generated.
