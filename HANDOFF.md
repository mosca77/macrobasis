# MacroAgent — co-op handoff

Orientation for the incoming co-op. This file tells you where things are and what to read first. It deliberately contains **no rules** — every rule lives in exactly one spec, and `CLAUDE.md` routes you to the right one. If this file and a spec ever disagree, the spec wins.

## What this is

MacroBasis is the OCIO team's weekly macro-theme tracker: six themes (Fiscal & Deregulation, Currency Debasement, Energy/Transition, AI, Geopolitics & Trade, Domestic Investing) plus a Monetary Policy appendix and an Illiquid Assets page, rendered as a bordered-block dashboard `.docx` that continues from last week's approved report. A daily 9:00 AM monitor feeds the weekly cycle. Claude runs the pipeline; you adjudicate, hand-edit, and approve.

## Read in this order (day one)

1. `CLAUDE.md` — the router: invariants, how to run, which spec owns which task.
2. `memory/projects/macroagent.md` — background and decision history (why things are the way they are).
3. `MacroBasis_Theme_Charter.md` — what we track and why (team-owned).
4. `MacroBasis_Weekly_Run_Prompt.md` — the weekly pipeline, Phases 0–8.
5. Last approved dashboard in `Dashboards_Eduardo_Updated/` — the format ground truth.
6. `memory/glossary.md` — acronyms and terms.

## How to run (since the 12-13 Aug 2026 GitHub migration)

- **Weekly:** say "Run the weekly cycle for [date]" in a Claude Code session on this repo — the prior dashboard is READ from `Dashboards_Eduardo_Updated/` in the repo, nothing is attached. A scheduled weekly Routine (Thursdays 10am ET) also runs the full cycle unattended and auto-merges its pull request, gated on the layout check. Details in `MacroBasis_Weekly_Run_Prompt.md` (incl. the "Automated (Routine) finish" contract).
- **Daily:** a scheduled 9:00 AM Routine reads `Monitoring News/README.md` (v2) from this repo and commits one file per day to `Monitoring News/`. **Routines do NOT travel with the repo** — they live on the owner's claude.ai account (Routines UI). On takeover, recreate both there; the daily prompt stays minimal ("follow the README exactly; never overwrite a day's file") and the weekly Routine's full prompt is reconstructable from the Run Prompt's Automated finish section.
- After you hand-edit and approve a weekly dashboard, upload the approved copy to `Dashboards_Eduardo_Updated/` — it becomes next week's prior state (its filename may carry your approval date rather than the build date; the newest file rules). This step is load-bearing.

## Folder map

| Path | What lives there |
|---|---|
| root | The four specs, `CLAUDE.md`, current template (newest `MacroBasis_Report_Template_v*.docx`) |
| `engine/` | `macrobasis_fill.py` (the only way a dashboard docx gets built), `content_schema.json` (canonical enums), format spec, per-week content JSONs, charts |
| `ChartsThemes/` | Eduardo's weekly chart uploads — the engine inserts them into the report at build (upload-only folder) |
| `Monitoring News/` | Daily news files, one per day, never overwritten |
| `runs/YYYY-MM-DD/` | Per-run checkpoints (contract in `runs/README.md`): ledger, panel, triage, self-audit |
| `Dashboards_Claude_Generated/` | Raw pipeline outputs |
| `Dashboards_Eduardo_Updated/` | **Approved copies = next week's prior state + formatting ground truth** (upload-only) |
| `memory/` | Glossary, project background, company context |

(`archive/` and the OneDrive folder live OUTSIDE this repo since the 12 Aug 2026 migration — never treat them as available paths.)

## Current state — read it, don't trust a snapshot

This file deliberately carries **no dated state section** (the 11 Aug snapshot it once held went stale within two days). To orient:
- Last approved dashboard = newest file in `Dashboards_Eduardo_Updated/`; latest generated = newest in `Dashboards_Claude_Generated/`.
- Last runs and their gates: newest `runs/YYYY-MM-DD/` folder (read `self_audit.md` first).
- Recent decisions: `git log --oneline -20` and `memory/projects/macroagent.md`.

> Last synced against Run Prompt v5.6 (13 Aug 2026).
