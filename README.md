# Reducing Out-of-Spec Rate on Incoming Cocoa/Couverture Lots
### A simulated Lean Six Sigma Black Belt DMAIC project

**Author:** Yemi (DCLM Belgium) — Lean Six Sigma Black Belt portfolio project
**Status:** complete — full DMAIC cycle run end-to-end on real data, see Results summary below

## Disclaimer
This is a **simulated training project**. The underlying data is the real, publicly available
Coffee Quality Institute (CQI) Arabica lot database (MIT license — see `data/README.md`),
reframed as incoming cocoa/couverture lot quality control for a chocolate manufacturer, for
Lean Six Sigma Black Belt exam preparation. Coffee and cocoa share a near-identical
agri-commodity incoming-QC workflow (lot cupping/sensory scoring, moisture testing, defect
counting, grading by origin/processing method), which is why this real dataset was chosen over
a purely synthetic one. It does not represent, and is not derived from, any employer's
proprietary data or process.

## Problem statement
> Across 1,306 incoming cocoa/couverture lots, **13.71%** fall below the specialty-grade quality
> threshold (score < 80/100) at intake, against a goal of under 8%. Baseline process capability
> Cpk = 0.27 (well below the 1.33 benchmark for a capable process), DPMO ~ 11,472. A simulated
> intake policy change (favoring the best-performing origin/processing-method combination found
> in Analyze) demonstrably cuts the out-of-spec rate to 11.15% and raises Cpk to 0.31 — see
> Results summary below and `charter/project_charter.md` for the full analysis.

## Project structure
```
charter/        Project charter, SIPOC, fishbone/Ishikawa, FMEA
data/           Data source, license, and download instructions (raw data not committed)
notebooks/      01_define.py ... 05_control.py — run as Jupyter cells (# %%) or plain scripts
control/        Control plan and response plan
requirements.txt
```

## How to reproduce
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
curl -L -o data/coffee_arabica.csv https://raw.githubusercontent.com/jldbc/coffee-quality-database/master/data/arabica_data_cleaned.csv
# then open notebooks/01_define.py in Jupyter/VS Code and run each # %% cell in order
```

## Results summary
| Metric | Baseline | After improvement |
|---|---|---|
| Out-of-spec lot rate (score < 80) | 13.71% | 11.15% |
| Cpk | 0.27 | 0.31 |
| Sigma level | 2.31 | 2.42 |
| DPMO | 11,472 | — (re-run after adopting the tightened sourcing policy) |

Improvement basis: simulated intake policy favoring the best-performing origin/processing-method
combination found in Analyze (Ethiopia + Natural/Dry, mean score 85.41), applied to n=278 lots.
See `charter/project_charter.md` for full findings and honest limitations.
