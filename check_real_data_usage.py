"""
Checks your SAVED notebook's actual printed output to determine, definitively,
which data sources were really used the last time you ran and saved it.
This reads what already happened -- it does not re-run anything.
"""
import nbformat
import sys

NOTEBOOK_PATH = "notebooks/GuestPath_Starter_Notebook.ipynb"

try:
    nb = nbformat.read(NOTEBOOK_PATH, as_version=4)
except FileNotFoundError:
    print(f"Could not find {NOTEBOOK_PATH} -- run this from your sas821s-clean folder.")
    sys.exit(1)

def get_output_text(cell):
    texts = []
    for out in cell.get("outputs", []):
        if "text" in out:
            texts.append(out["text"])
    return "".join(texts)

print("=" * 70)
print("LANL (auth.txt.gz / redteam.txt.gz)")
print("=" * 70)
found_step1 = False
for cell in nb.cells:
    if cell.cell_type == "code" and "AUTH_URL" in cell.source and "using_real_lanl_data" in cell.source:
        found_step1 = True
        out = get_output_text(cell)
        if not out.strip():
            print("This cell has NOT been run since the notebook was last saved (no output).")
        elif "Downloaded real LANL files" in out:
            print("REAL DATA WAS USED.")
            print("Actual printed output:", out.strip())
        elif "Falling back" in out:
            print("SYNTHETIC FALLBACK WAS USED (real files not found/reachable at run time).")
            print("Actual printed output:", out.strip())
        else:
            print("Cell ran but output doesn't match expected pattern. Raw output:")
            print(out.strip())
if not found_step1:
    print("Could not find the LANL-loading cell in this notebook.")

print()
print("=" * 70)
print("Enron + Nazario (guest-support / phishing text)")
print("=" * 70)
found_step10 = False
for cell in nb.cells:
    if cell.cell_type == "code" and "ENRON_PATH" in cell.source and "using_real_phishing_data" in cell.source:
        found_step10 = True
        out = get_output_text(cell)
        if not out.strip():
            print("This cell has NOT been run since the notebook was last saved (no output).")
        elif "Loaded REAL data" in out:
            print("REAL DATA WAS USED.")
            for line in out.splitlines():
                if "Loaded REAL data" in line:
                    print("Actual printed output:", line.strip())
        elif "using synthetic templates" in out:
            print("SYNTHETIC FALLBACK WAS USED (real files not found, or fewer than 20 messages per class).")
            for line in out.splitlines():
                if "synthetic templates" in line:
                    print("Actual printed output:", line.strip())
        else:
            print("Cell ran but output doesn't match expected pattern. Raw output:")
            print(out.strip())
if not found_step10:
    print("Could not find the Enron/Nazario-loading cell in this notebook.")

print()
print("=" * 70)
print("CICIDS2017 (network flow)")
print("=" * 70)
print("This notebook's Step 8 was never built with a real-data loader for CICIDS2017 --")
print("it always generates synthetic flow data, regardless of what's in your data folder.")
print("VERDICT: CICIDS2017 was NOT used in this iteration of the analysis, by design,")
print("not by accident. This is already disclosed in your Implementation Plan and Final")
print("Documentation as a known limitation.")
