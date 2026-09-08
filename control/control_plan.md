# Control Plan

| Characteristic (Y or X) | Spec/Target | Measurement method | Frequency | Chart type | Reaction plan |
|---|---|---|---|---|---|
| Lot quality (cupping) score | >= 80 (specialty grade) | Certified cupper panel scoring (SCA protocol) | Every incoming lot | I-MR chart (center 82.18, UCL 86.79, LCL 77.57) | Any point beyond UCL/LCL or a run of 7+ points on one side of center -> hold lot, re-cup, escalate to QA lead |
| Moisture % | Target band per regression (lower moisture = higher score; confirm real spec with QA) | In-line moisture meter | Every incoming lot | I-MR chart on moisture % | Out-of-band reading -> reject/downgrade lot, notify supplier |
| Out-of-spec rate (score < 80) | <= 8% (goal, from 13.7% baseline) | Derived from cupping score | Weekly rollup | P chart | Rate exceeds UCL for 2 consecutive weeks -> escalate to sourcing/process owner, review supplier mix |
| Origin / processing method mix | Bias sourcing toward Ethiopia + Natural/Dry-equivalent profile (highest mean score combination found) | Procurement record | Per purchase order | — | Sourcing decisions reviewed monthly against origin/method performance data |

## Lean controls
- 5S-equivalent: standardized intake sample prep and cupping station audit checklist
- Kanban-equivalent: reorder trigger tied to approved-supplier stock levels
- Poka-yoke: automatic hold/flag in the intake system for any lot with moisture % or defect
  count outside the control limits before it reaches the cupping panel

## Response plan
If the out-of-spec rate on the weekly P chart exceeds the UCL for 2 consecutive weeks:
1. Pull the run chart by origin/processing method to identify which supplier(s) are driving it.
2. Re-verify moisture meter calibration (MSA check).
3. Temporarily tighten acceptance criteria for the implicated origin/method until root cause
   (5-Why) is closed.
