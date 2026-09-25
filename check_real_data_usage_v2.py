"""
Checks EVERY .ipynb file in notebooks/ (and its root) for saved output,
so it doesn't matter which filename ended up with the real results.
"""
import nbformat
import glob
import os

paths = glob.glob("notebooks/*.ipynb") + glob.glob("*.ipynb")
paths = sorted(set(paths))

if not paths:
    print("No .ipynb files found in notebooks/ or the current folder.")
    print("Run this from your sas821s-clean folder.")
    exit()

def get_output_text(cell):
    return "".join(out.get("text", "") for out in cell.get("outputs", []))

for path in paths:
    print("=" * 70)
    print(f"FILE: {path}  ({os.path.getsize(path):,} bytes)")
    print("=" * 70)
    try:
        nb = nbformat.read(path, as_version=4)
    except Exception as e:
        print(f"  Could not open: {e}")
        continue

    executed_cells = sum(1 for c in nb.cells if c.cell_type == "code" and c.get("execution_count") is not None)
    total_code_cells = sum(1 for c in nb.cells if c.cell_type == "code")
    print(f"  {executed_cells} of {total_code_cells} code cells have been run.")

    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        out = get_output_text(cell)
        if "AUTH_URL" in cell.source and "using_real_lanl_data" in cell.source:
            if "Downloaded real LANL files" in out:
                print("  LANL: REAL DATA USED ->", out.strip().splitlines()[-1] if out.strip() else "")
            elif "Falling back" in out:
                print("  LANL: synthetic fallback ->", [l for l in out.splitlines() if "Falling back" in l or "Could not reach" in l])
            elif not out.strip():
                print("  LANL: cell not run in this file")
        if "ENRON_PATH" in cell.source and "using_real_phishing_data" in cell.source:
            if "Loaded REAL data" in out:
                print("  Enron/Nazario: REAL DATA USED ->", [l for l in out.splitlines() if "Loaded REAL" in l])
            elif "synthetic templates" in out:
                print("  Enron/Nazario: synthetic fallback")
            elif not out.strip():
                print("  Enron/Nazario: cell not run in this file")
    print()

print("=" * 70)
print("CICIDS2017: never has a real-data loader in this notebook (any copy) --")
print("always synthetic, by design. Already disclosed as a known limitation.")
print("=" * 70)
