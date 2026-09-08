# Data source

**Primary dataset:** "Predicting Manufacturing Defects Dataset" by Rabie El Kharoua
https://www.kaggle.com/datasets/rabieelkharoua/predicting-manufacturing-defects-dataset
License: check the dataset page on Kaggle and record it here before publishing (typically CC / open license — verify current terms).

**Optional secondary dataset (Define-phase VOC / industry context only):**
"Chocolate Bar Ratings" by rtatman — https://www.kaggle.com/datasets/rtatman/chocolate-bar-ratings

## Download
```bash
pip install kaggle --break-system-packages
# put your kaggle.json API token in ~/.kaggle/kaggle.json (chmod 600), then:
kaggle datasets download -d rabieelkharoua/predicting-manufacturing-defects-dataset -p . --unzip
```

## Chocolate-line reframing (rename columns to match your narrative)
The raw dataset is a generic production-line dataset (process parameters + defect outcome). Recommended
reframing for a chocolate enrobing/wrapping line — rename columns in `01_define.py` once you've inspected
the actual file, e.g.:

| Raw dataset column (typical) | Reframed as |
|---|---|
| ProductionVolume | Batches produced |
| ProductionCost | Cost per batch (€) |
| SupplierQuality | Cocoa butter / couverture supplier quality score |
| DeliveryDelay | Raw material delivery delay (days) |
| DefectRate | Wrapper/coating defect rate (%) |
| QualityScore | In-line QC score |
| MaintenanceHours | Enrober/tempering unit maintenance hours |
| DowntimePercentage | Line downtime (%) |
| Temperature-type field | Tempering temperature (°C) |
| Line/Shift-type field | Line / Shift |

> Open the CSV once downloaded and confirm actual column names — they may differ slightly by dataset
> version. Update the mapping above and the code in `01_define.py` accordingly.
