"""
Extracts Nazario phishing mbox and locates the Enron file, matching what the
notebook's Step 10 loader expects: data/enron_emails.csv and data/nazario_phishing.mbox
Safe to run multiple times -- won't overwrite if already done correctly.
"""
import zipfile
import os
import glob

DATA_DIR = os.path.join("notebooks", "data")

# ---- Nazario: extract the single mbox file from phishing3.zip ----
nazario_zip = os.path.join(DATA_DIR, "phishing3.zip")
nazario_target = os.path.join(DATA_DIR, "nazario_phishing.mbox")

if os.path.exists(nazario_zip):
    with zipfile.ZipFile(nazario_zip) as zf:
        names = zf.namelist()
        mbox_name = names[0]  # the single phishing3.mbox entry
        print(f"Extracting {mbox_name} from phishing3.zip...")
        with zf.open(mbox_name) as src, open(nazario_target, "wb") as dst:
            dst.write(src.read())
    print(f"Done. Saved to {nazario_target}")
    print(f"Size: {os.path.getsize(nazario_target):,} bytes")
else:
    print(f"phishing3.zip not found at {nazario_zip}")

print()

# ---- Enron: find any file/zip with "enron" in the name, case-insensitive ----
print("Looking for any Enron-related file in", DATA_DIR, "...")
matches = glob.glob(os.path.join(DATA_DIR, "*"))
enron_matches = [m for m in matches if "enron" in os.path.basename(m).lower()]

if not enron_matches:
    print("No file with 'enron' in the name found. Files actually present:")
    for m in matches:
        print(" ", os.path.basename(m))
else:
    for m in enron_matches:
        print(f"Found: {m}")
        if m.lower().endswith(".zip"):
            try:
                with zipfile.ZipFile(m) as zf:
                    names = zf.namelist()
                    print(f"  Contains {len(names)} entries. First 10:")
                    for n in names[:10]:
                        info = zf.getinfo(n)
                        print(f"    {n}  ({info.file_size:,} bytes)")
            except Exception as e:
                print(f"  Could not read as zip: {e}")
