# Fishbone / Ishikawa — Causes of Out-of-Spec Cocoa/Couverture Lot Quality

- **Material**: origin country (ANOVA p=1.9e-17, confirmed significant), moisture % at intake
  (strongest regression driver, p<0.001), variety
- **Method**: processing method — Washed/Wet vs Natural/Dry (t-test p=0.049; Chi-square vs.
  out-of-spec p=0.022, confirmed significant)
- **Man**: cupper/panel consistency — simulated Gage R&R used in 02_measure.py to check panel
  agreement (part-to-part variance strongly dominates gauge variance in the simulation, as
  expected for a well-run panel)
- **Measurement**: moisture meter calibration/precision, cupping protocol adherence (SCA
  standard sample size assumed = 350g)
- **Machine**: N/A at intake stage for this project (relevant to downstream conching/tempering,
  out of scope here)
- **Environment**: growing altitude (weak but present regression relationship), harvest-year
  weather variation (visible in the I-MR/Xbar-R charts by harvest year)

## Confirmed significant (carried into Improve phase)
1. Origin country — highly significant (p=1.9e-17)
2. Moisture % — highly significant regression driver (p<0.001)
3. Processing method — significant (p=0.049 / p=0.022)
4. Category 1 defect count — significant regression driver (p<0.001)

## Not significant / weak in this data
- Altitude — statistically detectable but practically small (coefficient 0.0008 per meter)
