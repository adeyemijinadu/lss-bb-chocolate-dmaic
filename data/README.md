# Data source

**Dataset:** Coffee Quality Institute (CQI) Arabica review database — real, expert-graded
green-coffee lot assessments (aroma, flavor, moisture, defects, altitude, origin, processing
method), scraped from the CQI's public review pages (Jan 2018) by jldbc.

- Source repo: https://github.com/jldbc/coffee-quality-database
- Direct file used here: `data/arabica_data_cleaned.csv` (1,311 lots)
- License: MIT (per the source repository)

## Why this dataset for the chocolate/confectionery project
No public dataset documents an actual chocolate production line (that data is proprietary to
manufacturers and isn't published). Coffee and cocoa are the closest real, richly-documented
public analog: both are agricultural commodities put through an almost identical incoming-QC
workflow — lot-level cupping/sensory scoring, moisture testing, defect counting, and grading by
origin/processing method — before they enter a food manufacturer's process. This dataset is
**real, not synthetic**, and is reframed here as **incoming raw-material (cocoa/couverture) lot
quality control** for a chocolate manufacturer, which is a genuine, common Black Belt project
type (supplier/incoming-material quality, not just the production line itself).

## Columns and their DMAIC role

| Column | Type | Reframe / role |
|---|---|---|
| Total.Cup.Points | continuous (0-100) | **Primary Y** — overall lot quality score (reframe as "couverture/cocoa liquor quality score") |
| Aroma, Flavor, Aftertaste, Acidity, Body, Balance, Uniformity, Clean.Cup, Sweetness, Cupper.Points | continuous (0-10 each) | Secondary Y's / sub-CTQs — reframe as sensory panel sub-scores (aroma, flavor intensity, mouthfeel, etc.) |
| Moisture | continuous (%) | Key X — moisture at intake, directly capability/SPC-relevant (real chocolate/cocoa QC tracks bean moisture) |
| Category.One.Defects, Category.Two.Defects | count (attribute) | Defect counts — use for Pareto, DPU/DPMO, P/U charts |
| Country.of.Origin, Region, Variety | categorical X | Supplier/origin — ANOVA/Kruskal-Wallis across origins |
| Processing.Method | categorical X | e.g. Washed/Natural/Honey — reframe as roast/conch profile category; ANOVA/Chi-square driver |
| altitude_mean_meters | continuous X | Growing altitude — regression predictor of quality score |
| Harvest.Year, Grading.Date | date/time | Use to build a time-ordered "batch intake" sequence for I-MR/EWMA control charts |
| Number.of.Bags, Bag.Weight | continuous | Lot size — optional covariate |

## Data quality notes
- Real data has messiness (a few blank/zero altitude rows, some rare/duplicate country labels,
  one famous zero-altitude outlier lot) — cleaning/handling this is itself a legitimate MSA/data
  cleaning exercise to document in `02_measure.py`.
- Only 1,311 rows and no true "designed experiment" or repeated-measures structure — the Improve
  phase's DOE and the Measure phase's Gage R&R are still simulated on top of this real data
  exactly as described in the master guide (this is standard for any BB training project using
  observational data).

## Optional secondary dataset (Define-phase VOC / finished-product context only)
"Chocolate Bar Ratings" — https://www.kaggle.com/datasets/rtatman/chocolate-bar-ratings
(real, finished-chocolate-bar consumer ratings — useful for a Define-phase VOC section, not for
process statistics).
