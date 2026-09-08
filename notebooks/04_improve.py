# %% [markdown]
# # 04 — Improve Phase (real CQI coffee-lot data, reframed as cocoa/couverture intake QC)
# BOK: 4.1 Simple regression, 4.2 Multiple regression, 4.3-4.5 Designed experiments.

# %%
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
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
df = df[(df["altitude_m"].isna()) | (df["altitude_m"] < 4500)].dropna(subset=["altitude_m"])
Y = "lot_quality_score"

# %% [markdown]
# ## 4.1 Correlation & simple linear regression
# Minitab: Stat > Basic Statistics > Correlation; Stat > Regression > Fitted Line Plot

# %%
numeric_cols = ["moisture_pct", "defects_cat1", "defects_cat2", "altitude_m"]
corr = df[numeric_cols + [Y]].corr()[Y].sort_values(key=abs, ascending=False)
print(corr)

x_col = corr.index[1]
X = sm.add_constant(df[x_col])
simple_model = sm.OLS(df[Y], X, missing="drop").fit()
print(simple_model.summary())

# %% [markdown]
# ### Residuals analysis

# %%
fitted, resid = simple_model.fittedvalues, simple_model.resid
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
axes[0].scatter(fitted, resid); axes[0].axhline(0, color="red"); axes[0].set_title("Residuals vs Fitted")
stats.probplot(resid, plot=axes[1]); axes[1].set_title("Normal probability plot")
plt.tight_layout(); plt.show()

# %% [markdown]
# ## 4.2 Multiple regression
# Minitab: Stat > Regression > Regression > Fit Regression Model

# %%
predictors = [c for c in numeric_cols if c != x_col]
X_multi = sm.add_constant(df[predictors])
multi_model = sm.OLS(df[Y], X_multi, missing="drop").fit()
print(multi_model.summary())
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif_data = pd.DataFrame({
    "feature": X_multi.columns,
    "VIF": [variance_inflation_factor(X_multi.dropna().values, i) for i in range(X_multi.shape[1])],
})
print(vif_data)

# %% [markdown]
# ## Data transformation — Box-Cox (if Y was non-normal in 02_measure.py)
# Minitab: Stat > Control Charts > Box-Cox Transformation

# %%
y_positive = df[Y][df[Y] > 0]
if len(y_positive) > 10:
    transformed, lam = stats.boxcox(y_positive)
    print(f"Box-Cox lambda: {lam:.3f}")

# %% [markdown]
# ## 4.3-4.5 Designed Experiments (simulated)
# This is REAL observational data, not a designed experiment — a genuine factorial DOE isn't
# possible on it directly. Standard workaround: take the 2 strongest X's from the regression
# above, define realistic low/high levels from their observed range, and run a SIMULATED 2^2
# full factorial (+ center points) using the regression's own coefficients as the "true" process
# behavior. Minitab: Stat > DOE > Factorial > Create/Analyze Factorial Design

# %%
x1_name, x2_name = predictors[0], predictors[1]
x1_low, x1_high = df[x1_name].quantile([0.1, 0.9])
x2_low, x2_high = df[x2_name].quantile([0.1, 0.9])

design = pd.DataFrame({
    x1_name: [x1_low, x1_high, x1_low, x1_high, (x1_low + x1_high) / 2] * 3,
    x2_name: [x2_low, x2_low, x2_high, x2_high, (x2_low + x2_high) / 2] * 3,
})
rng = np.random.default_rng(7)
b0 = multi_model.params.get("const", df[Y].mean())
b1 = multi_model.params.get(x1_name, 0)
b2 = multi_model.params.get(x2_name, 0)
design["quality_score_sim"] = (
    b0 + b1 * design[x1_name] + b2 * design[x2_name] + rng.normal(0, df[Y].std() * 0.2, len(design))
)
doe_model = sm.OLS(
    design["quality_score_sim"],
    sm.add_constant(design[[x1_name, x2_name]].assign(interaction=design[x1_name] * design[x2_name])),
).fit()
print(doe_model.summary())

# %% [markdown]
# ## Next steps
# State the "should-be" intake spec (e.g. "require moisture <= X%, source only from origins
# with mean score >= Y") in the charter, then move to `05_control.py`.
