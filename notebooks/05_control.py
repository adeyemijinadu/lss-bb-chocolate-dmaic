# %% [markdown]
# # 05 — Control Phase (real CQI coffee-lot data, reframed as cocoa/couverture intake QC)
# BOK: 5.1 Lean controls, 5.2 SPC, 5.3 Control plans.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("../data/coffee_arabica.csv")
rename_map = {
    "Total.Cup.Points": "lot_quality_score", "Moisture": "moisture_pct",
    "Category.One.Defects": "defects_cat1", "Category.Two.Defects": "defects_cat2",
    "Country.of.Origin": "origin_country", "Processing.Method": "processing_method",
    "altitude_mean_meters": "altitude_m", "Harvest.Year": "harvest_year", "Grading.Date": "grading_date",
}
df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
df = df[df["lot_quality_score"] > 0]
Y = "lot_quality_score"

# Real dates -> a genuine time-ordered sequence for control charts (a real advantage over
# synthetic data, which has no authentic chronology)
df["grading_date_parsed"] = pd.to_datetime(df["grading_date"], errors="coerce")
df = df.sort_values("grading_date_parsed").reset_index(drop=True)

# %% [markdown]
# ## 5.2 SPC — I-MR chart (individuals, lot-by-lot in grading-date order)
# Minitab: Stat > Control Charts > Variables Charts for Individuals > I-MR

# %%
def i_mr_chart(series, title="I-MR Chart"):
    x = series.dropna().reset_index(drop=True)
    mr = x.diff().abs().dropna()
    x_bar, mr_bar = x.mean(), mr.mean()
    ucl_i, lcl_i = x_bar + 2.66 * mr_bar, x_bar - 2.66 * mr_bar
    ucl_mr = 3.267 * mr_bar
    fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    axes[0].plot(x, marker="o", ms=2)
    axes[0].axhline(x_bar, color="green"); axes[0].axhline(ucl_i, color="red", linestyle="--")
    axes[0].axhline(lcl_i, color="red", linestyle="--"); axes[0].set_title(f"{title} — Individuals")
    axes[1].plot(mr, marker="o", ms=2, color="orange")
    axes[1].axhline(mr_bar, color="green"); axes[1].axhline(ucl_mr, color="red", linestyle="--")
    axes[1].set_title("Moving Range")
    plt.tight_layout(); plt.savefig("i_mr_chart.png", dpi=150); plt.show()
    return {"UCL_I": ucl_i, "LCL_I": lcl_i, "UCL_MR": ucl_mr, "center_I": x_bar}

print(i_mr_chart(df[Y], title=f"{Y} by grading date (real chronology)"))

# %% [markdown]
# ## Xbar-R chart — subgroup by harvest year
# Minitab: Stat > Control Charts > Variables Charts for Subgroups > Xbar-R

# %%
A2, D3, D4 = 0.577, 0, 2.114  # constants for subgroup size n=5 (adjust to your real avg subgroup size)
grouped = df.groupby("harvest_year")[Y]
xbar, r = grouped.mean(), grouped.apply(lambda s: s.max() - s.min())
xbar_bar, r_bar = xbar.mean(), r.mean()
ucl_xbar, lcl_xbar = xbar_bar + A2 * r_bar, xbar_bar - A2 * r_bar
ucl_r, lcl_r = D4 * r_bar, D3 * r_bar

fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
xbar.plot(ax=axes[0], marker="o")
axes[0].axhline(xbar_bar, color="green"); axes[0].axhline(ucl_xbar, color="red", linestyle="--")
axes[0].axhline(lcl_xbar, color="red", linestyle="--"); axes[0].set_title(f"Xbar chart of {Y} by harvest year")
r.plot(ax=axes[1], marker="o", color="orange")
axes[1].axhline(r_bar, color="green"); axes[1].axhline(ucl_r, color="red", linestyle="--")
axes[1].set_title("R chart")
plt.tight_layout(); plt.savefig("xbar_r_chart.png", dpi=150); plt.show()

# %% [markdown]
# ## P chart — proportion out-of-spec lots by harvest year
# Minitab: Stat > Control Charts > Attributes Charts > P

# %%
df["out_of_spec"] = (df[Y] < 80).astype(int)
p_data = df.groupby("harvest_year")["out_of_spec"].agg(["sum", "count"])
p_data["p"] = p_data["sum"] / p_data["count"]
p_bar = p_data["sum"].sum() / p_data["count"].sum()
p_data["ucl"] = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / p_data["count"])
p_data["lcl"] = (p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / p_data["count"])).clip(lower=0)
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(p_data["p"].values, marker="o"); ax.plot(p_data["ucl"].values, "r--")
ax.plot(p_data["lcl"].values, "r--"); ax.axhline(p_bar, color="green")
ax.set_title("P Chart — proportion of out-of-spec (below-specialty-grade) lots")
plt.tight_layout(); plt.savefig("p_chart.png", dpi=150); plt.show()

# %% [markdown]
# ## Finalize
# 1. Fill in `control/control_plan.md` with real spec limits, chart type, and reaction plan.
# 2. Update the "Results summary" table in the top-level README with before/after out-of-spec
#    rate, Cpk, and sigma level.
# 3. Commit and push.
