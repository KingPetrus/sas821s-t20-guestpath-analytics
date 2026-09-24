"""
Diagnostic only -- lists what's inside each zip without extracting or changing anything.
Run this first so we know the real structure before writing extraction code.
"""
import zipfile
import os

DATA_DIR = os.path.join("notebooks", "data")

zips_to_check = [
    "The Enron Email Dataset.zip",
    "phishing3.zip",
    "Network Intrusion dataset(CIC-IDS- 2017).zip",
]

for zip_name in zips_to_check:
    path = os.path.join(DATA_DIR, zip_name)
    print(f"\n=== {zip_name} ===")
    if not os.path.exists(path):
        print("  NOT FOUND at this path")
        continue
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            print(f"  {len(names)} entries total. First 15:")
            for n in names[:15]:
                info = zf.getinfo(n)
                print(f"    {n}  ({info.file_size:,} bytes)")
    except Exception as e:
        print(f"  ERROR reading zip: {e}")
