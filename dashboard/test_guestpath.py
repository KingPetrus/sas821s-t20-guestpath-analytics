"""
GuestPath Analytics -- formal test suite (Implementation Plan Section 13)
Run with: python test_guestpath.py
Each test checks something specific about the notebook's actual output files
in data/, produced by running GuestPath_Starter_Notebook.ipynb end to end.
"""
import pandas as pd
import json
import os
import sys

DATA_DIR = "data"
results = []

def check(test_id, name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    results.append((test_id, name, status, detail))
    print(f"[{status}] {test_id}: {name}" + (f" -- {detail}" if detail else ""))

# ---- T01: Notebook produced all expected output files ----
expected_files = [
    "user_anomaly_scores.csv", "incident_timeline.csv", "attack_path_techniques.csv",
    "adversarial_test_results.csv", "simulation_results.json", "composite_risk_score.json",
]
missing = [f for f in expected_files if not os.path.exists(os.path.join(DATA_DIR, f))]
check("T01", "Notebook end-to-end run produces all expected outputs",
      len(missing) == 0, f"missing: {missing}" if missing else "all 6 files present")

# ---- T02: PMS/payment generator produces a valid, joined dataset ----
try:
    pms = pd.read_csv(os.path.join(DATA_DIR, "synthetic_pms_events.csv")) if os.path.exists(
        os.path.join(DATA_DIR, "synthetic_pms_events.csv")) else None
    t02_ok = pms is not None and len(pms) > 0 and pms.isnull().sum().sum() == 0
    check("T02", "PMS synthetic dataset is non-empty with zero nulls", t02_ok,
          f"{len(pms)} rows" if pms is not None else "file not found")
except Exception as e:
    check("T02", "PMS synthetic dataset is non-empty with zero nulls", False, str(e))

# ---- T03: Anomaly detector flags a plausible, non-trivial fraction of users ----
try:
    anomaly_df = pd.read_csv(os.path.join(DATA_DIR, "user_anomaly_scores.csv"))
    n_flagged = int(anomaly_df["is_anomalous"].sum())
    t03_ok = 0 < n_flagged < len(anomaly_df)  # not zero, not everyone
    check("T03", "Anomaly detector flags a non-trivial, non-total fraction of users", t03_ok,
          f"{n_flagged} of {len(anomaly_df)} flagged")
except Exception as e:
    check("T03", "Anomaly detector flags a non-trivial, non-total fraction of users", False, str(e))

# ---- T04: Adversarial Case 2 ("low and slow") evades detection -- documented finding, not a bug ----
try:
    adv_df = pd.read_csv(os.path.join(DATA_DIR, "adversarial_test_results.csv"))
    case2 = adv_df[adv_df["case"].str.contains("Low and slow", case=False, na=False)]
    t04_ok = len(case2) == 1 and case2.iloc[0]["flagged"] == False
    check("T04", "Adversarial Case 2 (low and slow) evades detection as expected", t04_ok,
          f"flagged={case2.iloc[0]['flagged']}" if len(case2) == 1 else "case not found")
except Exception as e:
    check("T04", "Adversarial Case 2 (low and slow) evades detection as expected", False, str(e))

# ---- T05: Segmentation simulation shows Control A outperforming Control B ----
try:
    with open(os.path.join(DATA_DIR, "simulation_results.json")) as f:
        sim = json.load(f)
    t05_ok = sim["control_a_risk_reduction"] > sim["control_b_risk_reduction"]
    check("T05", "Segmentation (Control A) reduces risk more than MFA alone (Control B)", t05_ok,
          f"A={sim['control_a_risk_reduction']:.0%}, B={sim['control_b_risk_reduction']:.0%}")
except Exception as e:
    check("T05", "Segmentation (Control A) reduces risk more than MFA alone (Control B)", False, str(e))

# ---- Summary ----
print()
n_pass = sum(1 for r in results if r[2] == "PASS")
print(f"{n_pass}/{len(results)} tests passed.")
if n_pass < len(results):
    print("Some tests failed -- check that the notebook has been run end to end first (data/ populated).")
    sys.exit(1)
