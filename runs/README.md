# runs/ — per-run checkpoints (weekly cycle)

One folder per weekly run, `runs/YYYY-MM-DD/`, written by the Run Prompt as each gate passes:

| File | Written at | Contains |
|---|---|---|
| `ledger.md` | Phase 1 | Week Ledger: story threads (day-by-day), candidate union, Charter coverage map |
| `panel.md` | Phase 3 | Full Indicator Panel pull + confirm / diverge / null tag per claim |
| `triage.md` | Phase 4 | Confirmed triage table (provenance column; every daily candidate included or discarded). Updated after Eduardo's confirmation — this is the record Phase 7 reconciles against |
| `self_audit.md` | Phase 8 | Checklist confirmations + the **run manifest**: window, files read, thread counts, lights, divergences carried, and `edits_after_review:` (Eduardo fills after his hand pass — the minimal-edits KPI, tracked week over week) |

Purpose: resumability (an interrupted run continues from the first missing artifact), post-hoc audit (no scrolling dead chats), mechanical reconciliation, and the weekly quality metric. These are working records, not deliverables — the deliverable is the dashboard `.docx`.

## Aborted runs (13 Aug 2026 rule)

A run directory that will not be completed (superseded by a later run, or abandoned mid-cycle) must either be **deleted** or keep an **`ABORTED.md`** stating one line: why it stopped, and which run supersedes it. A directory with neither the full four-file set nor an `ABORTED.md` fails `engine/check_specs.py`. Beat-level working notes belong inside the run folder under `beats/` if kept at all — the four contract files above are the only names the resume logic reads.
