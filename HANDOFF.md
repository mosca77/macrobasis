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

## How to run

- **Weekly:** say "Run the weekly cycle for [date]" and attach last week's approved dashboard from `Dashboards_Eduardo_Updated/`. Details in `MacroBasis_Weekly_Run_Prompt.md`.
- **Daily:** a scheduled 9:00 AM task writes one file per day to `Monitoring News/`. Protocol in `Monitoring News/README.md`. **The schedule does NOT travel with this folder** — it lives in the Claude app on the owner's account, so you must create it once on yours: open this folder in Claude (Cowork), then ask Claude to "create a scheduled task, daily at 9:00 AM: follow `Monitoring News/README.md` (v2) exactly and write today's news file; never overwrite an existing day's file." Everything else (beats, subagents on Sonnet, file format) is in the README — the schedule prompt stays minimal on purpose.
- After you hand-edit and approve a weekly dashboard, save the approved copy to `Dashboards_Eduardo_Updated/` — it becomes next week's prior state. This step is load-bearing.

## Folder map

| Path | What lives there |
|---|---|
| root | The four specs, `CLAUDE.md`, current template (`MacroBasis_Report_Template_v6.docx`), current explainer deck (`_v3.pptx`), current deliverables |
| `engine/` | `macrobasis_fill.py` (the only way a dashboard docx gets built), `content_schema.json` (canonical enums), format spec, per-week content JSONs, charts |
| `Monitoring News/` | Daily news files, one per day, never overwritten |
| `runs/YYYY-MM-DD/` | Per-run checkpoints (contract in `runs/README.md`): ledger, panel, triage, self-audit |
| `Dashboards_Claude_Generated/` | Raw pipeline outputs |
| `Dashboards_Eduardo_Updated/` | **Approved copies = next week's prior state + formatting ground truth** |
| `memory/` | Glossary, project background, company context |
| `archive/` | Retired versions with dated manifests — check here before assuming something is lost |

## State as of 11 Aug 2026

- Last approved dashboard: **2026-07-30** (`Dashboards_Eduardo_Updated/`).
- Latest generated: **2026-08-06** (`Dashboards_Claude_Generated/`) — approved copy **not yet** saved to `Dashboards_Eduardo_Updated/`; do that (or re-review) before the next weekly run uses it as prior.
- Daily monitor last wrote **2026-08-06** and the scheduled task no longer exists (verified 11 Aug) — you must create it on your account (recipe above). 07–10 Aug files are missing; the next weekly sweep still covers its full window, so no backfill is required unless you want the daily record complete.
- `MacroBasis_Interim_Thematic_Review_2026-08-11.docx` at root is current one-off work.
- Illiquids page and Sonnet-5-for-all-research are recent changes (6 Aug 2026) — decision history in `memory/projects/macroagent.md`.
