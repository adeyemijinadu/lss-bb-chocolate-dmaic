# %% [markdown]
# # 02 — Measure Phase (real CQI coffee-lot data, reframed as cocoa/couverture intake QC)
# BOK: 2.1 Process definition, 2.2 Six Sigma statistics, 2.3 MSA, 2.4 Process Capability.

# %%
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("../data/coffee_arabica.csv")
rename_map = {
    "Total.Cup.Points": "lot_quality_score", "Moisture": "moisture_pct",
    "Category.One.Defects": "defects_cat1", "Category.Two.Defects": "defects_cat2",
    "Country.of.Origin": "origin_country", "Processing.Method": "processing_method",
    "altitude_mean_meters": "altitude_m", "Variety": "variety", "Harvest.Year": "harvest_year",
}
df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
df = df[df["lot_quality_score"] > 0]
df = df[(df["altitude_m"].isna()) | (df["altitude_m"] < 4500)]

Y = "lot_quality_score"

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
# Minitab: Stat > Basic Statistics > Normality Test (Anderson-Darling)

# %%
stat, p = stats.shapiro(df[Y].dropna())
print(f"Shapiro-Wilk: W={stat:.4f}, p={p:.4f}")
ad_result = stats.anderson(df[Y].dropna(), dist="norm")
print(f"Anderson-Darling statistic: {ad_result.statistic:.4f} (critical values: {ad_result.critical_values})")
is_normal = p >= 0.05
print("Normal enough for parametric tests?", is_normal)

# %% [markdown]
# ## 2.3 Measurement System Analysis (Gage R&R)
# Real cupping scores ARE a measurement system (human panel scoring against a rubric), but this
# dataset doesn't include repeated cupper-level scores per lot, so we simulate a small Gage R&R
# study exactly as we would for a real sensory panel: 10 lots x 3 cuppers x 2 sessions.
# Minitab: Stat > Quality Tools > Gage Study > Gage R&R Study (Crossed)

# %%
rng = np.random.default_rng(42)
parts = np.repeat(np.arange(1, 11), 3 * 2)
cuppers = np.tile(np.repeat(["A", "B", "C"], 2), 10)
part_effect = np.repeat(rng.normal(0, 3.0, 10), 6)
cupper_effect = np.tile(np.repeat(rng.normal(0, 0.4, 3), 2), 10)
measurement_error = rng.normal(0, 0.6, 60)
score = 82 + part_effect + cupper_effect + measurement_error

grr_df = pd.DataFrame({"lot": parts, "cupper": cuppers, "score": score})
import statsmodels.api as sm
import statsmodels.formula.api as smf
model = smf.ols("score ~ C(lot) + C(cupper) + C(lot):C(cupper)", data=grr_df).fit()
print(sm.stats.anova_lm(model, typ=2))
# %GRR = (repeatability + reproducibility variance) / total variance; compare to AIAG thresholds
# (<10% acceptable, 10-30% marginal, >30% unacceptable) — same as Minitab's Gage R&R output.

# %% [markdown]
# ## 2.4 Process capability (Cp, Cpk, Pp, Ppk, sigma level)
# Minitab: Stat > Quality Tools > Capability Analysis > Normal
# Spec: a specialty-grade lot must score >= 80 (industry-standard specialty threshold) with an
# informal upper ceiling around 100.

# %%
def capability(series, lsl, usl):
    mu, sigma = series.mean(), series.std(ddof=1)
    cp = (usl - lsl) / (6 * sigma)
    cpu = (usl - mu) / (3 * sigma)
    cpl = (mu - lsl) / (3 * sigma)
    cpk = min(cpu, cpl)
    sigma_level = cpk * 3 + 1.5
    return {"mean": mu, "std": sigma, "Cp": cp, "Cpk": cpk, "sigma_level": sigma_level}

LSL, USL = 80.0, 100.0
print(capability(df[Y].dropna(), LSL, USL))

# Attribute view: define an out-of-spec flag for later P-chart / DPMO work
df["out_of_spec"] = (df[Y] < LSL).astype(int)
print(f"Out-of-spec rate: {df['out_of_spec'].mean():.2%}")

# %% [markdown]
# ## Next steps
# Carry forward: which X's look related to variation (moisture, altitude, origin, processing
# method), whether Y is normal, your %GRR verdict, and baseline Cpk/sigma level/out-of-spec rate
# as the "before" numbers for the results table in the top-level README.
