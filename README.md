# Cocoa/Couverture Intake Lot Quality — DMAIC Project
### A simulated Lean Six Sigma Black Belt DMAIC project

**Author:** Yemi (DCLM Belgium) — Lean Six Sigma Black Belt portfolio project (self-guided)
**Status:** in progress — working through DMAIC myself, phase by phase

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
> Fill in after Define phase.


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

## Results summary (fill in at the end)
| Metric | Baseline | After improvement |
|---|---|---|
| | | |
| | | |
