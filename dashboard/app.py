"""
GuestPath Analytics -- SOC prototype dashboard (Task 6)
Reads the notebook's exported data/ files. No re-computation happens here --
this is a read-only view over results already produced by the notebook.
"""
import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(page_title="GuestPath Analytics", layout="wide")

DATA_DIR = "data"

def load_csv(name):
    path = os.path.join(DATA_DIR, name)
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

def load_json(name):
    path = os.path.join(DATA_DIR, name)
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return None

st.title("GuestPath Analytics — SOC Prototype")
st.caption("T20 · Hospitality Guest-System Compromise and Payment-Data Security Analytics")

anomaly_df = load_csv("user_anomaly_scores.csv")
incident_df = load_csv("incident_timeline.csv")
attck_df = load_csv("attack_path_techniques.csv")
adversarial_df = load_csv("adversarial_test_results.csv")
sim_results = load_json("simulation_results.json")
risk_score = load_json("composite_risk_score.json")

missing = [n for n, d in [("user_anomaly_scores.csv", anomaly_df), ("incident_timeline.csv", incident_df),
                          ("attack_path_techniques.csv", attck_df), ("adversarial_test_results.csv", adversarial_df),
                          ("simulation_results.json", sim_results), ("composite_risk_score.json", risk_score)] if d is None]
if missing:
    st.warning(f"Missing files (run the notebook first to generate them): {', '.join(missing)}")

# ---- Top-line metrics ----
col1, col2, col3, col4 = st.columns(4)
with col1:
    n_flagged = int(anomaly_df["is_anomalous"].sum()) if anomaly_df is not None and "is_anomalous" in anomaly_df else "-"
    st.metric("Flagged accounts", n_flagged)
with col2:
    n_incident = len(incident_df) if incident_df is not None else "-"
    st.metric("Incident timeline events", n_incident)
with col3:
    composite = f"{risk_score['composite_risk_score']:.2f}" if risk_score else "-"
    st.metric("Composite breach-risk score", composite)
with col4:
    n_techniques = len(attck_df) if attck_df is not None else "-"
    st.metric("ATT&CK techniques mapped", n_techniques)

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Session / Identity Anomalies", "Incident Timeline", "ATT&CK Mapping",
    "Segmentation Simulation", "Adversarial Test Results"
])

with tab1:
    st.subheader("Session / Identity UEBA Anomaly Scoring")
    if anomaly_df is not None:
        flagged_only = anomaly_df[anomaly_df["is_anomalous"] == True] if "is_anomalous" in anomaly_df else anomaly_df
        st.write(f"{len(flagged_only)} of {len(anomaly_df)} accounts flagged as anomalous.")
        st.dataframe(anomaly_df.sort_values("anomaly_score") if "anomaly_score" in anomaly_df else anomaly_df,
                     use_container_width=True)
    else:
        st.info("No anomaly data found. Run the notebook's Step 3 and Step 7 export first.")

with tab2:
    st.subheader("Reconstructed Incident Timeline")
    st.caption("PMS events tied to a flagged account inside the attack window (notebook Step 5).")
    if incident_df is not None:
        st.dataframe(incident_df, use_container_width=True)
    else:
        st.info("No incident timeline found. Run the notebook's Step 5 and Step 7 export first.")

with tab3:
    st.subheader("MITRE ATT&CK Technique Mapping")
    st.caption("Each row cites the notebook step that produced its evidence -- not asserted without evidence.")
    if attck_df is not None:
        st.dataframe(attck_df, use_container_width=True)
        st.markdown("[Open in MITRE ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) "
                    "and upload `data/attck_layer.json` for the heat-map view.")
    else:
        st.info("No ATT&CK mapping found. Run the notebook's Step 9 first.")

with tab4:
    st.subheader("Segmentation Simulation — Two Alternative Controls")
    if sim_results:
        c1, c2, c3 = st.columns(3)
        c1.metric("Baseline (flat network)", f"{sim_results['baseline_success_rate']:.1%}")
        c2.metric("Control A: Network segmentation",
                  f"{sim_results['control_a_segmentation_success_rate']:.1%}",
                  delta=f"-{sim_results['control_a_risk_reduction']:.0%} risk", delta_color="normal")
        c3.metric("Control B: Identity MFA gate",
                  f"{sim_results['control_b_mfa_success_rate']:.1%}",
                  delta=f"-{sim_results['control_b_risk_reduction']:.0%} risk", delta_color="normal")
        st.bar_chart(pd.DataFrame({
            "Attack success rate": [
                sim_results["baseline_success_rate"],
                sim_results["control_a_segmentation_success_rate"],
                sim_results["control_b_mfa_success_rate"],
            ]
        }, index=["Baseline", "Control A: Segmentation", "Control B: MFA gate"]))
        st.caption(f"Based on {sim_results.get('n_iterations', '?')} Monte Carlo iterations per scenario "
                   "(notebook Step 13). Segmentation outperforms MFA alone because the flat network's "
                   "direct guest-to-PMS shortcut bypasses the identity layer MFA protects.")
    else:
        st.info("No simulation results found. Run the notebook's Step 13 first.")

with tab5:
    st.subheader("Adversarial Evasion Testing")
    st.caption("Tests whether the anomaly detector (Step 3) can be evaded by an attacker who knows roughly how it works.")
    if adversarial_df is not None:
        st.dataframe(adversarial_df, use_container_width=True)
        evaded = adversarial_df[adversarial_df["flagged"] == False] if "flagged" in adversarial_df else None
        if evaded is not None and len(evaded) > 0:
            st.warning(f"**Key finding:** {len(evaded)} case(s) evaded detection entirely -- "
                       f"see: {', '.join(evaded['case'].tolist())}. This is a genuine limitation of "
                       "volume-sensitive anomaly detection, not a bug.")
    else:
        st.info("No adversarial test results found. Run the notebook's Step 14 first.")

st.divider()
st.caption("GuestPath Analytics prototype -- SAS821S Capstone T20. All data is public/synthetic; "
           "no real guest, staff, or payment data is used at any stage.")
