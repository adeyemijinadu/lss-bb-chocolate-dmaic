# %% [markdown]
# # 05 — Control Phase
# BOK: 5.1 Lean controls, 5.2 Statistical Process Control, 5.3 Control plans.

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("../data/manufacturing_defects.csv")
Y = "defect_rate"

# %% [markdown]
# ## 5.2 SPC — I-MR chart (individuals, no natural subgroup)
# Minitab: Stat > Control Charts > Variables Charts for Individuals > I-MR

# %%
def i_mr_chart(series, title="I-MR Chart"):
    x = series.dropna().reset_index(drop=True)
    mr = x.diff().abs().dropna()
    x_bar, mr_bar = x.mean(), mr.mean()
    ucl_i, lcl_i = x_bar + 2.66 * mr_bar, x_bar - 2.66 * mr_bar
    ucl_mr = 3.267 * mr_bar

    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    axes[0].plot(x, marker="o")
    axes[0].axhline(x_bar, color="green")
    axes[0].axhline(ucl_i, color="red", linestyle="--")
    axes[0].axhline(lcl_i, color="red", linestyle="--")
    axes[0].set_title(f"{title} — Individuals")

    axes[1].plot(mr, marker="o", color="orange")
    axes[1].axhline(mr_bar, color="green")
    axes[1].axhline(ucl_mr, color="red", linestyle="--")
    axes[1].set_title("Moving Range")
    plt.tight_layout()
    plt.savefig("i_mr_chart.png", dpi=150)
    plt.show()
    return {"UCL_I": ucl_i, "LCL_I": lcl_i, "UCL_MR": ucl_mr, "center_I": x_bar}

print(i_mr_chart(df[Y], title=f"{Y} — I-MR"))

# %% [markdown]
# ## Xbar-R chart (rational subgroups — e.g. subgroup by shift/batch of size 3-5)
# Minitab: Stat > Control Charts > Variables Charts for Subgroups > Xbar-R

# %%
subgroup_col = next((c for c in df.columns if df[c].nunique() < 50 and df[c].dtype != float), None)
if subgroup_col:
    A2, D3, D4 = 0.577, 0, 2.114  # constants for subgroup size n=5 (adjust for your actual n)
    grouped = df.groupby(subgroup_col)[Y]
    xbar = grouped.mean()
    r = grouped.apply(lambda s: s.max() - s.min())
    xbar_bar, r_bar = xbar.mean(), r.mean()
    ucl_xbar, lcl_xbar = xbar_bar + A2 * r_bar, xbar_bar - A2 * r_bar
    ucl_r, lcl_r = D4 * r_bar, D3 * r_bar

    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    xbar.plot(ax=axes[0], marker="o")
    axes[0].axhline(xbar_bar, color="green")
    axes[0].axhline(ucl_xbar, color="red", linestyle="--")
    axes[0].axhline(lcl_xbar, color="red", linestyle="--")
    axes[0].set_title(f"Xbar chart of {Y} by {subgroup_col}")
    r.plot(ax=axes[1], marker="o", color="orange")
    axes[1].axhline(r_bar, color="green")
    axes[1].axhline(ucl_r, color="red", linestyle="--")
    axes[1].set_title("R chart")
    plt.tight_layout()
    plt.savefig("xbar_r_chart.png", dpi=150)
    plt.show()

# %% [markdown]
# ## Attribute charts — P chart (proportion defective, varying subgroup size)
# Minitab: Stat > Control Charts > Attributes Charts > P

# %%
if "pass_fail" in df.columns and subgroup_col:
    p_data = df.groupby(subgroup_col)["pass_fail"].agg(["sum", "count"])
    p_data["p"] = p_data["sum"] / p_data["count"]
    p_bar = p_data["sum"].sum() / p_data["count"].sum()
    p_data["ucl"] = p_bar + 3 * np.sqrt(p_bar * (1 - p_bar) / p_data["count"])
    p_data["lcl"] = (p_bar - 3 * np.sqrt(p_bar * (1 - p_bar) / p_data["count"])).clip(lower=0)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(p_data["p"].values, marker="o")
    ax.plot(p_data["ucl"].values, "r--")
    ax.plot(p_data["lcl"].values, "r--")
    ax.axhline(p_bar, color="green")
    ax.set_title("P Chart — proportion defective")
    plt.tight_layout()
    plt.savefig("p_chart.png", dpi=150)
    plt.show()

# %% [markdown]
# ## Finalize
# 1. Fill in `control/control_plan.md` with the real spec limits, chart type, and reaction plan
#    for each characteristic you controlled.
# 2. Update the "Results summary" table in the top-level `README.md` with before/after defect
#    rate, Cpk, and sigma level (baseline from `02_measure.py`, "after" from a re-run of the
#    capability function on data filtered to the "improved" settings from `04_improve.py`).
# 3. Commit this notebook and the generated PNGs, then push the repo to GitHub.
