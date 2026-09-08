# %% [markdown]
# # 01 — Define Phase
# Chocolate/confectionery project — incoming cocoa/couverture lot quality control.
# Data: real Coffee Quality Institute (CQI) Arabica lot database, reframed as incoming
# raw-material (cocoa/couverture) lot QC for a chocolate manufacturer (see data/README.md
# for why coffee data is the closest real public analog to cocoa intake QC).
#
# BOK topics covered here: 1.1 Basics of Six Sigma, 1.2 Fundamentals (CTQ, COPQ, Pareto,
# DPU/DPMO/FTY/RTY), 1.3 Project selection, 1.4 Lean/waste.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %% [markdown]
# ## Load data

# %%
df = pd.read_csv("../data/coffee_arabica.csv")
df.shape

# %% [markdown]
# Rename columns to the cocoa/couverture-intake narrative (see the mapping table in
# data/README.md). This is REAL data, so a few columns need light cleaning first.

# %%
rename_map = {
    "Total.Cup.Points": "lot_quality_score",       # primary Y
    "Moisture": "moisture_pct",                    # key continuous X
    "Category.One.Defects": "defects_cat1",
    "Category.Two.Defects": "defects_cat2",
    "Country.of.Origin": "origin_country",
    "Processing.Method": "processing_method",
    "altitude_mean_meters": "altitude_m",
    "Variety": "variety",
    "Harvest.Year": "harvest_year",
}
df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

# Real-data cleanup: a few lots have altitude/quality-score data entry errors (e.g. altitude in
# feet instead of meters, or a zero total score). Standard practice — document what you drop.
before = len(df)
df = df[df["lot_quality_score"] > 0]                 # drop the known zero-score entry error
df = df[(df["altitude_m"].isna()) | (df["altitude_m"] < 4500)]  # drop implausible altitude outlier(s)
print(f"Dropped {before - len(df)} rows as data-entry errors; {len(df)} lots remain")
df.columns.tolist()

# %% [markdown]
# ## Basic Six Sigma metrics: DPU, DPMO, FTY, RTY
# Minitab equivalent: no single menu — usually computed manually. Here Y is a continuous
# quality score with defect counts as a secondary attribute measure, so we compute DPU/DPMO
# on the defect counts (treat each lot as a "unit" with 2 inspection "opportunities":
# Category 1 and Category 2 defects).

# %%
units = len(df)
total_defects = df["defects_cat1"].sum() + df["defects_cat2"].sum()
dpu = total_defects / units
opportunities_per_unit = 350  # SCA standard 350g cupping sample size (beans inspected per lot)
dpmo = dpu / opportunities_per_unit * 1_000_000
print(f"Units (lots): {units}\nTotal defects: {total_defects}\nDPU: {dpu:.3f}\nDPMO: {dpmo:,.0f}")

# %% [markdown]
# ## Pareto analysis (80:20 rule)
# Minitab: Stat > Quality Tools > Pareto Chart
# Pareto of mean defect count by origin country — which suppliers/origins drive most defects?

# %%
counts = (
    df.groupby("origin_country")[["defects_cat1", "defects_cat2"]]
    .sum()
    .sum(axis=1)
    .sort_values(ascending=False)
    .head(15)
)
fig, ax1 = plt.subplots(figsize=(9, 4))
counts.plot(kind="bar", ax=ax1, color="steelblue")
ax2 = ax1.twinx()
cum_pct = counts.cumsum() / counts.sum() * 100
ax2.plot(range(len(counts)), cum_pct.values, color="red", marker="o")
ax2.axhline(80, color="grey", linestyle="--")
ax1.set_ylabel("Total defects (Cat 1 + Cat 2)")
ax2.set_ylabel("Cumulative %")
plt.title("Pareto — defects by origin/supplier (top 15)")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig("../charter/pareto_defects.png", dpi=150)
plt.show()

# %% [markdown]
# ## Next steps
# - Fill in `charter/project_charter.md`, `charter/sipoc.md`, `charter/fishbone.md` with what
#   this exploration revealed (which origins/processing methods dominate defects).
# - Move to `02_measure.py` for descriptive stats, normality testing, MSA, and capability analysis.
