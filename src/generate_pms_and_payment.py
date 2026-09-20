"""
GuestPath Analytics - synthetic PMS + payment-gateway log generator
Generates a benign baseline plus explicit, labelled attack sequences,
joined by session_id/attack_id so PMS and payment events correlate.
"""
from faker import Faker
import pandas as pd
import random

fake = Faker()
Faker.seed(821)
random.seed(821)

# --------------------------------------------------------------
# Fixed hotel workforce, role-based (not fully random)
# --------------------------------------------------------------
USERS = {
    "STF0001": "front_desk", "STF0002": "front_desk", "STF0003": "front_desk",
    "STF0004": "finance", "STF0005": "finance",
    "STF0006": "housekeeping", "STF0007": "housekeeping",
    "STF0008": "manager", "STF0009": "it_admin",
}

# What "normal" looks like per role -- this is what makes the later anomaly
# detection meaningful, since attack events deliberately break this pattern.
ROLE_MODULES = {
    "front_desk":  {"reservations": ["view_reservation","create_reservation","modify_reservation"],
                     "profiles": ["view_profile","search_profile"],
                     "front_desk": ["check_in","check_out","assign_room"]},
    "finance":     {"billing": ["view_bill","add_charge","close_bill"],
                     "folio": ["view_folio","add_folio_charge"],
                     "payments": ["view_payment","initiate_payment","refund_payment"]},
    "housekeeping":{"housekeeping": ["view_status","update_room_status"]},
    "manager":     {"reports": ["view_report","export_report"],
                     "reservations": ["view_reservation"]},
    "it_admin":    {"administration": ["view_user","create_user","modify_user","change_role"]},
}

N_BENIGN = 5000

def make_benign_event(i):
    user_id, role = random.choice(list(USERS.items()))
    module = random.choice(list(ROLE_MODULES[role].keys()))
    action = random.choice(ROLE_MODULES[role][module])
    return {
        "event_id": f"PMS{i+1:06d}",
        "timestamp": fake.date_time_between(start_date="-30d", end_date="now"),
        "property_id": f"P{random.randint(1,5):03d}",
        "session_id": f"SES{random.randint(1,10000):05d}",
        "attack_id": "BENIGN",
        "user_id": user_id, "role": role,
        "source_ip": fake.ipv4_private(),
        "source_segment": "staff",
        "module": module, "action": action,
        "is_suspicious": 0, "attack_stage": "benign",
    }

pms_rows = [make_benign_event(i) for i in range(N_BENIGN)]

# --------------------------------------------------------------
# Explicit, labelled attack sequences -- guest wifi -> compromised
# staff credential -> PMS -> administration -> payment access
# --------------------------------------------------------------
def make_attack_sequence(attack_id, compromised_user, start_time):
    session_id = f"SES_ATTACK_{attack_id}"
    stages = [
        ("profiles", "view_profile", "initial_access"),
        ("reservations", "search_profile", "discovery"),
        ("administration", "view_user", "privilege_discovery"),
        ("payments", "view_payment", "payment_access"),
    ]
    events = []
    for j, (module, action, stage) in enumerate(stages):
        events.append({
            "event_id": f"PMS-ATK-{attack_id}-{j+1:02d}",
            "timestamp": start_time + pd.Timedelta(seconds=j * 25),
            "property_id": "P001",
            "session_id": session_id, "attack_id": attack_id,
            "user_id": compromised_user, "role": USERS[compromised_user],
            "source_ip": fake.ipv4(),  # public-looking IP, not the staff private range
            "source_segment": "guest",
            "module": module, "action": action,
            "is_suspicious": 1, "attack_stage": stage,
        })
    return events, session_id

attack_start = fake.date_time_between(start_date="-2d", end_date="-1d")
attack1_events, attack1_session = make_attack_sequence("001", "STF0004", attack_start)
attack2_events, attack2_session = make_attack_sequence("002", "STF0007", attack_start + pd.Timedelta(hours=6))

pms_df = pd.DataFrame(pms_rows + attack1_events + attack2_events).sort_values("timestamp").reset_index(drop=True)

# --------------------------------------------------------------
# Payment-gateway log, joined by session_id/attack_id
# --------------------------------------------------------------
def make_payment_event(i, session_id, attack_id, is_suspicious, ts):
    return {
        "event_id": f"PAY{i+1:06d}",
        "timestamp": ts,
        "gateway_id": "GW01",
        "session_id": session_id, "attack_id": attack_id,
        "transaction_id": f"TXN{random.randint(100000,999999)}",
        "source_ip": fake.ipv4_private() if attack_id == "BENIGN" else fake.ipv4(),
        "destination_port": 443, "protocol": "TCPS",
        "amount": round(random.uniform(20, 800), 2), "currency": "NAD",
        "payment_method": random.choice(["card", "eft"]),
        "gateway_status": "approved" if is_suspicious == 0 else random.choice(["approved", "flagged"]),
        "is_suspicious": is_suspicious,
    }

payment_rows = []
for i in range(1200):  # benign payment events, independent of PMS benign volume
    payment_rows.append(make_payment_event(i, f"SES{random.randint(1,10000):05d}", "BENIGN", 0,
                                            fake.date_time_between(start_date="-30d", end_date="now")))
# attack-linked payment events -- same session_id as the PMS attack sequence's last event
payment_rows.append(make_payment_event(9001, attack1_session, "001", 1, attack_start + pd.Timedelta(seconds=100)))
payment_rows.append(make_payment_event(9002, attack2_session, "002", 1, attack_start + pd.Timedelta(hours=6, seconds=100)))

payment_df = pd.DataFrame(payment_rows).sort_values("timestamp").reset_index(drop=True)

# --------------------------------------------------------------
# Save + validate
# --------------------------------------------------------------
pms_df.to_csv("synthetic_pms_logs.csv", index=False)
payment_df.to_csv("synthetic_payment_logs.csv", index=False)

print("PMS dataset:", pms_df.shape, "| attack rows:", (pms_df.is_suspicious == 1).sum())
print("Payment dataset:", payment_df.shape, "| attack rows:", (payment_df.is_suspicious == 1).sum())
print("\nAttack stage breakdown:")
print(pms_df["attack_stage"].value_counts())
print("\nJoin check -- PMS attack sessions found in payment log:",
      set(pms_df[pms_df.attack_id != "BENIGN"]["session_id"]).issubset(set(payment_df["session_id"])))
