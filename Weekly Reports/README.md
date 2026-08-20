# Weekly Reports

The weekly deliverable folder (since 20 Aug 2026; replaces `Dashboards_Claude_Generated/` + `Dashboards_Eduardo_Updated/`).

- The top level holds exactly ONE file: the current week's `MacroBasis_Dashboard_YYYY-MM-DD.docx`, finalized and ready to send. It is next week's prior state and the formatting ground truth.
- `archive/` holds every older report and is history, never prior state:
  - `archive/approved/` = hand-edited copies from the retired approval loop (through 2026-08-07);
  - `archive/generated/` = raw engine outputs from before consolidation (through 2026-08-06).
- Each weekly run writes the new final file here and moves the file it replaces into `archive/`.
- There is no separate approval copy. A hand-edited replacement committed by the Co-Op is calibration data (regression rule in `MacroBasis_Evaluator.md`).
