# %% [markdown]
# # 04 — Improve Phase
# BOK: 4.1 Simple linear regression, 4.2 Multiple regression, 4.3-4.5 Designed experiments.

# %%
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import matplotlib.pyplot as plt

df = pd.read_csv("../data/manufacturing_defects.csv")
Y = "defect_rate"

# %% [markdown]
# ## 4.1 Correlation & simple linear regression
# Minitab: Stat > Basic Statistics > Correlation; Stat > Regression > Fitted Line Plot

# %%
numeric_cols = df.select_dtypes(include=np.number).columns.drop(Y, errors="ignore")
corr = df[numeric_cols.tolist() + [Y]].corr()[Y].sort_values(key=abs, ascending=False)
print(corr)

x_col = corr.index[1] if len(corr) > 1 else numeric_cols[0]  # strongest correlate with Y
X = sm.add_constant(df[x_col])
simple_model = sm.OLS(df[Y], X, missing="drop").fit()
print(simple_model.summary())

# %% [markdown]
# ### Residuals analysis (check regression assumptions — same checks Minitab plots automatically
# under Stat > Regression > Regression > Four in One)

# %%
fitted = simple_model.fittedvalues
resid = simple_model.resid
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].scatter(fitted, resid)
axes[0].axhline(0, color="red")
axes[0].set_title("Residuals vs Fitted")
stats.probplot(resid, plot=axes[1])
axes[1].set_title("Normal probability plot of residuals")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 4.2 Multiple regression
# Minitab: Stat > Regression > Regression > Fit Regression Model

# %%
predictors = [c for c in numeric_cols if c != x_col][:4]  # pick a handful of candidate X's
X_multi = sm.add_constant(df[predictors])
multi_model = sm.OLS(df[Y], X_multi, missing="drop").fit()
print(multi_model.summary())
print("VIFs (check multicollinearity):")
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif_data = pd.DataFrame({
    "feature": X_multi.columns,
    "VIF": [variance_inflation_factor(X_multi.dropna().values, i) for i in range(X_multi.shape[1])],
})
print(vif_data)

# %% [markdown]
# ## Data transformation — Box-Cox (use if Y was non-normal in 02_measure.py)
# Minitab: Stat > Control Charts > Box-Cox Transformation (or under Capability Analysis options)

# %%
y_positive = df[Y].dropna()
y_positive = y_positive[y_positive > 0]
if len(y_positive) > 10:
    transformed, lam = stats.boxcox(y_positive)
    print(f"Box-Cox lambda: {lam:.3f}")

# %% [markdown]
# ## 4.3–4.5 Designed Experiments (simulated)
# Real Kaggle data is observational, not from a designed experiment — so a genuine factorial
# DOE isn't possible on it directly. The standard workaround: take the 2 strongest X's from the
# regression above, define realistic low/high levels around their observed range, and run a
# SIMULATED 2^2 full factorial (with a center point) using a response model informed by the
# regression coefficients + noise. This lets you practice DOE design, confounding/resolution
# concepts, and effect/interaction analysis exactly as the exam tests them.
# Minitab: Stat > DOE > Factorial > Create Factorial Design / Analyze Factorial Design

# %%
x1_name, x2_name = predictors[0], predictors[1]
x1_low, x1_high = df[x1_name].quantile([0.1, 0.9])
x2_low, x2_high = df[x2_name].quantile([0.1, 0.9])

# 2^2 factorial + 3 center points, coded -1/+1
design = pd.DataFrame({
    x1_name: [x1_low, x1_high, x1_low, x1_high, (x1_low + x1_high) / 2] * 3,
    x2_name: [x2_low, x2_low, x2_high, x2_high, (x2_low + x2_high) / 2] * 3,
})
rng = np.random.default_rng(7)
# Simulate a response using the fitted multi_model's coefficients as the "true" process behavior
b0 = multi_model.params.get("const", df[Y].mean())
b1 = multi_model.params.get(x1_name, 0)
b2 = multi_model.params.get(x2_name, 0)
design["defect_rate_sim"] = (
    b0 + b1 * design[x1_name] + b2 * design[x2_name] + rng.normal(0, df[Y].std() * 0.2, len(design))
)

doe_model = sm.OLS(
    design["defect_rate_sim"],
    sm.add_constant(design[[x1_name, x2_name]].assign(interaction=design[x1_name] * design[x2_name])),
).fit()
print(doe_model.summary())
# Interpret exactly like a real Minitab factorial analysis: significant main effects and
# interaction terms (p<0.05) tell you which factor(s), and combination(s), to set at their
# "improved" level going into the Control phase.

# %% [markdown]
# ## Next steps
# Pick the improved factor settings suggested by the regression + simulated DOE, state the
# "should-be" process (e.g. "run tempering temp at X°C, line speed at Y") in the charter, and
# move to `05_control.py` to build the SPC charts that will hold the gain.
