# %% [markdown]
# # 03 — Analyze Phase (real CQI coffee-lot data, reframed as cocoa/couverture intake QC)
# BOK: 3.1 Patterns of variation, 3.2 Inferential statistics, 3.3-3.5 Hypothesis testing.

# %%
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

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
# ## 3.1 Multi-vari analysis — Y across processing method and top origins
# Minitab: Stat > Quality Tools > Multi-Vari Chart

# %%
fig, ax = plt.subplots(figsize=(7, 4))
df.boxplot(column=Y, by="processing_method", ax=ax)
plt.title(f"{Y} by processing method"); plt.suptitle("")
plt.tight_layout(); plt.show()

top_origins = df["origin_country"].value_counts().head(6).index
fig, ax = plt.subplots(figsize=(8, 4))
df[df["origin_country"].isin(top_origins)].boxplot(column=Y, by="origin_country", ax=ax)
plt.title(f"{Y} by origin (top 6 by lot count)"); plt.suptitle("")
plt.tight_layout(); plt.show()

# %% [markdown]
# ## 3.3/3.4 Hypothesis testing — NORMAL data path
# 2-sample t-test — compare two processing methods (e.g. Washed vs Natural)
# Minitab: Stat > Basic Statistics > 2-Sample t

# %%
methods = df["processing_method"].value_counts().head(2).index
g1 = df.loc[df["processing_method"] == methods[0], Y].dropna()
g2 = df.loc[df["processing_method"] == methods[1], Y].dropna()
lev_stat, lev_p = stats.levene(g1, g2)
equal_var = lev_p >= 0.05
t_stat, t_p = stats.ttest_ind(g1, g2, equal_var=equal_var)
print(f"Comparing '{methods[0]}' vs '{methods[1]}'")
print(f"Levene p={lev_p:.4f} (equal_var={equal_var}) | t-test: t={t_stat:.3f}, p={t_p:.4f}")

# %% [markdown]
# One-Way ANOVA — Y across top origins (3+ groups)
# Minitab: Stat > ANOVA > One-Way

# %%
import statsmodels.api as sm
import statsmodels.formula.api as smf
sub = df[df["origin_country"].isin(top_origins)]
model = smf.ols(f"{Y} ~ C(origin_country)", data=sub).fit()
print(sm.stats.anova_lm(model, typ=2))
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukey = pairwise_tukeyhsd(sub[Y], sub["origin_country"])
print(tukey)

# %% [markdown]
# ## 3.5 Hypothesis testing — NON-NORMAL data path (use if 02_measure.py rejected normality)
# Mann-Whitney U — Minitab: Stat > Nonparametrics > Mann-Whitney

# %%
u_stat, u_p = stats.mannwhitneyu(g1, g2)
print(f"Mann-Whitney: U={u_stat:.1f}, p={u_p:.4f}")

# %% [markdown]
# Kruskal-Wallis (3+ groups) — Minitab: Stat > Nonparametrics > Kruskal-Wallis

# %%
groups_list = [g[Y].dropna().values for _, g in sub.groupby("origin_country")]
kw_stat, kw_p = stats.kruskal(*groups_list)
print(f"Kruskal-Wallis: H={kw_stat:.3f}, p={kw_p:.4f}")

# %% [markdown]
# Chi-Square test of independence — is out-of-spec rate associated with processing method?
# Minitab: Stat > Tables > Chi-Square Test for Association

# %%
df["out_of_spec"] = (df[Y] < 80).astype(int)
contingency = pd.crosstab(df["processing_method"], df["out_of_spec"])
chi2, p_chi, dof, expected = stats.chi2_contingency(contingency)
print(contingency)
print(f"Chi-square: {chi2:.3f}, p={p_chi:.4f}, dof={dof}")

# %% [markdown]
# ## Next steps
# Document which X's (origin, processing method, moisture, altitude) came out statistically
# AND practically significant. Carry those into `04_improve.py` for regression and DOE.
