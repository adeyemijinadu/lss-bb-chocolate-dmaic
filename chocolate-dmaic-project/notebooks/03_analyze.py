# %% [markdown]
# # 03 — Analyze Phase
# BOK: 3.1 Patterns of variation, 3.2 Inferential statistics, 3.3 Hypothesis testing concepts,
# 3.4 Hypothesis testing with normal data, 3.5 Hypothesis testing with non-normal data.

# %%
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

df = pd.read_csv("../data/manufacturing_defects.csv")
Y = "defect_rate"

# %% [markdown]
# ## 3.1 Multi-vari analysis
# Plot Y across every categorical/grouping variable you have (shift, line, supplier, operator)
# to visually spot which factor(s) explain the most variation before you run formal tests.
# Minitab: Stat > Quality Tools > Multi-Vari Chart

# %%
group_cols = [c for c in df.columns if df[c].dtype == "object" or df[c].nunique() < 10]
for col in group_cols[:4]:
    fig, ax = plt.subplots(figsize=(6, 3))
    df.boxplot(column=Y, by=col, ax=ax)
    plt.title(f"{Y} by {col}")
    plt.suptitle("")
    plt.tight_layout()
    plt.show()

# %% [markdown]
# ## 3.3/3.4 Hypothesis testing — NORMAL data path
# Decide which test applies the same way the exam expects: how many groups, is Y continuous
# or attribute, is variance equal, is the data normal (from 02_measure.py's Shapiro/AD test).
#
# 2-sample t-test — compare defect rate between two shifts/lines
# Minitab: Stat > Basic Statistics > 2-Sample t

# %%
if "shift" in df.columns and df["shift"].nunique() == 2:
    groups = df["shift"].unique()
    g1 = df.loc[df["shift"] == groups[0], Y].dropna()
    g2 = df.loc[df["shift"] == groups[1], Y].dropna()
    # Levene's test for equal variance first (Minitab: Stat > ANOVA > Test for Equal Variances)
    lev_stat, lev_p = stats.levene(g1, g2)
    equal_var = lev_p >= 0.05
    t_stat, t_p = stats.ttest_ind(g1, g2, equal_var=equal_var)
    print(f"Levene p={lev_p:.4f} (equal_var={equal_var}) | t-test: t={t_stat:.3f}, p={t_p:.4f}")

# %% [markdown]
# One-Way ANOVA — compare 3+ groups (e.g. across lines or suppliers)
# Minitab: Stat > ANOVA > One-Way

# %%
import statsmodels.api as sm
import statsmodels.formula.api as smf

cat_for_anova = next((c for c in group_cols if df[c].nunique() >= 3), None)
if cat_for_anova:
    model = smf.ols(f"{Y} ~ C({cat_for_anova})", data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)
    # p < 0.05 on the categorical term -> at least one group differs -> follow up with Tukey HSD
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    tukey = pairwise_tukeyhsd(df[Y].dropna(), df.loc[df[Y].notna(), cat_for_anova])
    print(tukey)

# %% [markdown]
# ## 3.5 Hypothesis testing — NON-NORMAL data path
# Use these instead of the t-test/ANOVA above if 02_measure.py's normality test failed (p<0.05).
#
# Mann-Whitney U (non-parametric 2-sample) — Minitab: Stat > Nonparametrics > Mann-Whitney

# %%
if "shift" in df.columns and df["shift"].nunique() == 2:
    u_stat, u_p = stats.mannwhitneyu(g1, g2)
    print(f"Mann-Whitney: U={u_stat:.1f}, p={u_p:.4f}")

# %% [markdown]
# Kruskal-Wallis (non-parametric 3+ groups) — Minitab: Stat > Nonparametrics > Kruskal-Wallis

# %%
if cat_for_anova:
    groups_list = [g[Y].dropna().values for _, g in df.groupby(cat_for_anova)]
    kw_stat, kw_p = stats.kruskal(*groups_list)
    print(f"Kruskal-Wallis: H={kw_stat:.3f}, p={kw_p:.4f}")

# %% [markdown]
# Chi-Square test of independence (attribute data, e.g. pass/fail by shift)
# Minitab: Stat > Tables > Chi-Square Test for Association

# %%
if "shift" in df.columns and "pass_fail" in df.columns:
    contingency = pd.crosstab(df["shift"], df["pass_fail"])
    chi2, p_chi, dof, expected = stats.chi2_contingency(contingency)
    print(f"Chi-square: {chi2:.3f}, p={p_chi:.4f}, dof={dof}")

# %% [markdown]
# ## Next steps
# Document, in `charter/fishbone.md`, which X's came out statistically significant (p<0.05)
# and practically significant (meaningful effect size, not just significant p on a huge sample).
# Carry the significant X's into `04_improve.py` for regression and the simulated DOE.
