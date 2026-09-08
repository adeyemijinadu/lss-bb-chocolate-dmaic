# %% [markdown]
# # 01 — Define Phase
# Chocolate enrobing/wrapping line — defect reduction project.
#
# This file uses the `# %%` cell-marker format (Jupytext "light" style). In VS Code or
# Jupyter (with jupytext installed) each `# %%` block runs as its own notebook cell.
# You can also just run `python notebooks/01_define.py` top to bottom as a plain script.
#
# BOK topics covered here: 1.1 Basics of Six Sigma, 1.2 Fundamentals (CTQ, COPQ, Pareto,
# DPU/DPMO/FTY/RTY), 1.3 Project selection, 1.4 Lean/waste.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
# ## Load data
# Download first (see data/README.md), then point this at the actual CSV filename.

# %%
df = pd.read_csv("../data/manufacturing_defects.csv")  # <-- rename to the real downloaded filename
df.head()

# %% [markdown]
# Rename columns to the chocolate-line narrative (see the mapping table in data/README.md).
# Example — EDIT the left-hand names to match what's actually in your CSV:

# %%
rename_map = {
    "DefectRate": "defect_rate",
    "ProductionVolume": "batches_produced",
    "SupplierQuality": "supplier_quality_score",
    "DeliveryDelay": "material_delay_days",
    "MaintenanceHours": "maintenance_hours",
    "DowntimePercentage": "downtime_pct",
    "QualityScore": "qc_score",
}
df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
df.columns.tolist()

# %% [markdown]
# ## Basic Six Sigma metrics: DPU, DPMO, FTY, RTY
# Minitab equivalent: no single menu — usually computed manually or via the Six Sigma
# calculator add-in. In Python we just do the arithmetic directly, which is exactly what
# you'd do on the exam (closed-book, 4-function calculator).
#
# DPU  = defects / units
# DPMO = (defects / (units * opportunities_per_unit)) * 1,000,000
# FTY  = units passing without rework / units started
# RTY  = product of FTY across all steps in the process

# %%
# Example using a defect-rate style column as a stand-in for "defects per unit produced"
units = df["batches_produced"].sum() if "batches_produced" in df else len(df)
defects = (df["defect_rate"] / 100 * df.get("batches_produced", 1)).sum() if "defect_rate" in df else None
dpu = defects / units if defects is not None else None
opportunities_per_unit = 3  # e.g. coating, seal, weight — set to your real opportunity count
dpmo = dpu / opportunities_per_unit * 1_000_000 if dpu is not None else None
print(f"DPU: {dpu}\nDPMO: {dpmo}")

# %% [markdown]
# ## Pareto analysis (80:20 rule)
# Minitab: Stat > Quality Tools > Pareto Chart

# %%
# If you have a defect-category column, do a classic Pareto. Otherwise, bucket defect_rate
# by a categorical field (e.g. shift, line, supplier) to see where defects concentrate.
if "defect_category" in df.columns:
    counts = df["defect_category"].value_counts().sort_values(ascending=False)
else:
    # fallback: bucket mean defect_rate by an available categorical column
    cat_col = next((c for c in ["shift", "line", "supplier_quality_score"] if c in df.columns), None)
    counts = df.groupby(cat_col)["defect_rate"].mean().sort_values(ascending=False) if cat_col else None

if counts is not None:
    fig, ax1 = plt.subplots(figsize=(8, 4))
    counts.plot(kind="bar", ax=ax1, color="steelblue")
    ax2 = ax1.twinx()
    cum_pct = counts.cumsum() / counts.sum() * 100
    ax2.plot(range(len(counts)), cum_pct.values, color="red", marker="o")
    ax2.axhline(80, color="grey", linestyle="--")
    ax1.set_ylabel("Defect count / mean defect rate")
    ax2.set_ylabel("Cumulative %")
    plt.title("Pareto — defect drivers")
    plt.tight_layout()
    plt.savefig("../charter/pareto_defects.png", dpi=150)
    plt.show()

# %% [markdown]
# ## Next steps
# - Fill in `charter/project_charter.md`, `charter/sipoc.md`, `charter/fishbone.md` with what
#   this exploration revealed (which categories/shifts/suppliers dominate defects).
# - Move to `02_measure.py` for descriptive stats, normality testing, MSA, and capability analysis.
