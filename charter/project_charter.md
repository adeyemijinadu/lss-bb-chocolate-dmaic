# Project Charter

| Field | Detail |
|---|---|
| Project title | Reducing out-of-spec rate on incoming cocoa/couverture lots (chocolate manufacturer) |
| Problem statement | Across 1,306 incoming lots, 13.7% fall below the specialty-grade quality threshold (score < 80/100), driving rework, downgrade, and rejected-shipment cost. Baseline Cpk = 0.27 (well below the 1.33 target for a capable process). |
| Goal statement | Reduce out-of-spec lot rate from 13.7% to below 8% and raise Cpk from 0.27 to at least 0.5 within one sourcing cycle, by tightening intake requirements on the drivers identified below. |
| Business case | At current volume, cutting the out-of-spec rate by ~2.5 points (13.7% -> 11.2%, demonstrated achievable below) avoids rework/downgrade cost on roughly 1 in 40 additional lots — quantify with real €/lot rework cost when applying this to an actual supply chain. |
| Scope (in/out) | In: incoming lot QC decision (accept/reject/downgrade) at intake. Out: downstream conching/tempering process itself. |
| Project metrics (Primary Y) | Lot quality score (0-100, specialty threshold 80), out-of-spec rate, Cpk |
| Secondary metrics | Category 1 / Category 2 defect counts, moisture % |
| Team (simulated) | Black Belt: Yemi · Process Owner: Sourcing/QA Lead (simulated) · SMEs: Cupping panel (simulated) |
| Data | Real Coffee Quality Institute (CQI) Arabica lot database, reframed as cocoa/couverture intake QC — see data/README.md |

## Y = f(X) — confirmed by Analyze/Improve phases
Lot quality score is a function of: **moisture %** (strongest regression driver, coefficient
-8.39, p<0.001 — every 1-point rise in moisture % costs ~8.4 quality-score points), origin
country (ANOVA p = 1.9e-17 — highly significant), processing method (t-test p = 0.049,
Chi-square vs. out-of-spec p = 0.022), and Category 1 defect count (p<0.001).

## Key findings (from the notebooks, real data)
- **Define:** DPU = 4.02 defects/lot, DPMO ≈ 11,472 (SCA 350g sample standard). Mexico,
  Guatemala, and Brazil are the top 3 origins by total defect count in this sample.
- **Measure:** Data is **not normal** (Shapiro-Wilk p ≈ 1e-30) — non-parametric tests
  (Mann-Whitney, Kruskal-Wallis) are the primary Analyze-phase tools, with the t-test/ANOVA
  results cross-checked against them. Baseline capability: mean 82.18, std 2.69, **Cp 1.24,
  Cpk 0.27**, out-of-spec rate 13.71%.
- **Analyze:** Origin is a highly significant driver of quality score (ANOVA p = 1.9e-17).
  Processing method also matters (t-test p = 0.049 between the two most common methods;
  Chi-square p = 0.022 for association with out-of-spec status). Best-performing
  origin/method combination in the data (n>=10 lots): **Ethiopia + Natural/Dry** processing,
  mean score 85.41.
- **Improve:** Multiple regression R^2 = 0.06 (modest — realistic for real, noisy agricultural
  data; no single lever dominates). Simulated "improved" intake policy — favor the
  best-performing origin/method combination — moves capability from Cpk 0.27 -> **0.31** and
  out-of-spec rate from 13.71% -> **11.15%** (n=278 lots meeting the tightened criteria). A
  real project would combine this with the moisture-% control found in the regression for a
  larger effect.
- **Control:** I-MR chart on lot quality score by grading date: center 82.18, UCL 86.79,
  LCL 77.57. See `control/control_plan.md`.

## Honest limitations of this simulated project
- Gage R&R (MSA) and the factorial DOE are **simulated**, not from a real repeated-measures
  study or a real designed experiment — this dataset is observational, so those two BOK
  elements are practiced on synthetic add-ons as described in the master guide. This is
  standard practice for any BB training project built on public/observational data.
- The 80-point specialty threshold is a real industry convention (SCA specialty-grade cutoff),
  not an invented spec — this is one of the strengths of using real coffee-quality data.
