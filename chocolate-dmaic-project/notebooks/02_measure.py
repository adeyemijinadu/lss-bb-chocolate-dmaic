# %% [markdown]
# # 02 — Measure Phase
# BOK: 2.1 Process definition (already in charter/), 2.2 Six Sigma statistics,
# 2.3 Measurement System Analysis, 2.4 Process Capability.

# %%
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../data/manufacturing_defects.csv")  # rename as in 01_define.py
# ... re-apply the same rename_map from 01_define.py here if needed

Y = "defect_rate"  # set to your primary continuous/attribute Y column name

# %% [markdown]
# ## 2.2 Descriptive statistics & graphical analysis
# Minitab: Stat > Basic Statistics > Display Descriptive Statistics; Graph > Histogram/Boxplot

# %%
print(df[Y].describe())
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
sns.histplot(df[Y], kde=True, ax=axes[0])
sns.boxplot(y=df[Y], ax=axes[1])
plt.tight_layout()
plt.savefig("descriptive_plots.png", dpi=150)
plt.show()

# %% [markdown]
# ## Normality test
# Minitab: Stat > Basic Statistics > Normality Test (Anderson-Darling is Minitab's default;
# scipy's Shapiro-Wilk is the closest common equivalent for n < 5000, or use
# `scipy.stats.anderson` directly for an Anderson-Darling statistic to match Minitab exactly).

# %%
stat, p = stats.shapiro(df[Y].dropna())
print(f"Shapiro-Wilk: W={stat:.4f}, p={p:.4f}")
ad_result = stats.anderson(df[Y].dropna(), dist="norm")
print(f"Anderson-Darling statistic: {ad_result.statistic:.4f} (compare to critical values: {ad_result.critical_values})")
# Rule of thumb (matches exam logic): p < 0.05 -> reject normality -> use non-normal methods in Analyze phase.
is_normal = p >= 0.05
print("Normal enough for parametric tests?" , is_normal)

# %% [markdown]
# ## 2.3 Measurement System Analysis (Gage R&R)
# If your dataset doesn't include repeated measurements by operator/part (most Kaggle
# manufacturing sets don't), simulate a small Gage R&R study — this is a legitimate and common
# BB-training substitute: 10 parts x 3 operators x 2 trials, analyzed exactly like a real study.
# Minitab: Stat > Quality Tools > Gage Study > Gage R&R Study (Crossed)

# %%
rng = np.random.default_rng(42)
parts = np.repeat(np.arange(1, 11), 3 * 2)          # 10 parts
operators = np.tile(np.repeat(["A", "B", "C"], 2), 10)  # 3 operators x 2 trials
part_effect = np.repeat(rng.normal(0, 1.0, 10), 6)
operator_effect = np.tile(np.repeat(rng.normal(0, 0.15, 3), 2), 10)
measurement_error = rng.normal(0, 0.25, 60)
measured_value = 10 + part_effect + operator_effect + measurement_error

grr_df = pd.DataFrame({"part": parts, "operator": operators, "value": measured_value})

# Two-way ANOVA to split variance into part, operator, and repeatability (error)
import statsmodels.api as sm
import statsmodels.formula.api as smf

model = smf.ols("value ~ C(part) + C(operator) + C(part):C(operator)", data=grr_df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
print(anova_table)
# Reading it: Repeatability = MS(Residual); Reproducibility ~ MS(operator) & interaction;
# Part-to-part = MS(part). %GRR = (Repeatability+Reproducibility) variance / Total variance.
# Compare your computed %GRR to the standard AIAG thresholds: <10% acceptable, 10-30% marginal,
# >30% unacceptable — same thresholds Minitab reports automatically in its Gage R&R output.

# %% [markdown]
# ## 2.4 Process capability (Cp, Cpk, Pp, Ppk, sigma level)
# Minitab: Stat > Quality Tools > Capability Analysis > Normal (or Nonnormal / Binomial for
# attribute data)

# %%
def capability(series, lsl, usl):
    mu, sigma = series.mean(), series.std(ddof=1)
    cp = (usl - lsl) / (6 * sigma)
    cpu = (usl - mu) / (3 * sigma)
    cpl = (mu - lsl) / (3 * sigma)
    cpk = min(cpu, cpl)
    sigma_level = cpk * 3 + 1.5  # shifted (long-term) sigma level convention
    return {"mean": mu, "std": sigma, "Cp": cp, "Cpk": cpk, "sigma_level": sigma_level}

# Set your spec limits based on the business requirement (e.g. defect_rate must be <= 2%)
LSL, USL = 0, 2.0  # EDIT to your real spec
print(capability(df[Y].dropna(), LSL, USL))

# %% [markdown]
# ## Next steps
# Carry forward: (1) which X's look like they drive variation (from the Pareto/boxplots above),
# (2) whether Y is normal or not (drives which hypothesis tests you use in 03_analyze.py),
# (3) your %GRR verdict, (4) your baseline Cpk/sigma level — this is your "before" number for
# the results table in the top-level README.
