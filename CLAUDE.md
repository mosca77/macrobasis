# Memory

## Me
The Co-Op — the current co-op in the office of the OCIO (Office of the Chief Investment Officer) at OPTrust (OPSEU Pension Trust). Tracks and monitors macro developments for the team. The seat rotates: "the Co-Op" always means the current holder (personal names removed 20 Aug 2026 so the setup hands over cleanly).

## Preferences
- Concise and direct; minimal verbosity.
- Standardized, repeatable formatting for macro reporting (consistency matters).
- Outputs always tie back to investment implications.

## Project: MacroAgent / MacroBasis
Weekly macro-theme tracker for the OCIO team: **6 themes** (Fiscal & Deregulation · Currency Debasement · Energy/Transition · AI · Geopolitics & Trade · Domestic Investing) **+ a Monetary Policy appendix** after Theme 1 **+ an Illiquid Assets page** after Theme 6 (since 6 Aug 2026), rendered as a bordered-block dashboard `.docx` that continues last week's report. Background + decision history: `memory/projects/macroagent.md`.

**This file is a router, not a rulebook (since 6 Jul 2026).** Every rule lives in exactly ONE spec below. Read the owning spec before acting — never work from a remembered summary of it.

## Environment (GitHub deployment, since 12 Aug 2026)
This repo IS the agent's working directory; it runs in Claude Code's cloud sandbox (no Claude Desktop, no local folders, no attachments).
- **Session setup, every fresh sandbox, before Phase 8:** `sudo apt-get install -y libreoffice poppler-utils` (no `apt-get update` first — the sandbox image carries dead third-party PPAs that 403 and abort the chain) and `pip install python-docx lxml matplotlib pillow numpy`. (`check_layout.py` needs headless LibreOffice + poppler; the engine needs python-docx + lxml.)
- **Prior state comes from the repo, never from attachments:** last week's report = the newest `MacroBasis_Dashboard_*.docx` at the top level of `Weekly Reports/` (`Weekly Reports/archive/` is history, never prior state); prior histories = the newest `engine/content_*.json`.
- **Outputs are committed, same layout as always:** finished dashboard → `Weekly Reports/` (moving the file it replaces into `Weekly Reports/archive/`, so the top level always holds exactly one current file); content JSON → `engine/`; charts → `engine/charts/YYYY-MM-DD/`; checkpoints → `runs/YYYY-MM-DD/`. Commit messages: "Weekly run YYYY-MM-DD" / "Daily news YYYY-MM-DD". **Single-file workflow since 20 Aug 2026: no separate approval copy — the generated file IS the weekly deliverable, final and ready to send, gated on check_layout.** A hand-edited replacement committed by the Co-Op is calibration data (invariant 7).
- The OneDrive folder and the old root-level `archive/` live outside this repo; never reference them as available paths. The only in-repo archive is `Weekly Reports/archive/`.

## How to run
- **Weekly report:** say **"Run the weekly cycle for [date]"** (alias "Execute"). Prior dashboard is read from `Weekly Reports/` per the Environment section (nothing attached). Pipeline = `MacroBasis_Weekly_Run_Prompt.md` (v5.1+, Phases 0–8, gates checkpointed to `runs/YYYY-MM-DD/`). No prior dashboard in the folder = baseline mode, confirm first. **Unattended (Routine) runs finish themselves: push → PR → auto-merge, gated on check_layout — contract = "Automated (Routine) finish" in the Run Prompt (v5.8).**
- **Daily monitor:** scheduled 9:00 AM task (claude.ai scheduled task + GitHub connector, since 12 Aug 2026: reads the protocol from this repo, commits `Monitoring News/YYYY-MM-DD_News.md`; the first file actually produced GitHub-native is 13 Aug — 07-12 Aug files came from the old relay path and their NEW/CARRIED tags are unreliable); protocol = `Monitoring News/README.md` (v2.1). Never overwrite a day's file. **Daily runs finish themselves since 18 Aug 2026: commit → push → PR → immediate merge to `main`, gated only on `check_specs.py --daily` — contract = step 7 of the protocol.**

## Hard invariants (full detail in the owning spec)
0. **Layout since 30 Jul 2026:** page 1 = exec (direction, factors, **highlighted quadrant**, "Why this quadrant" bullets, all six status rows); **no exec Key Developments page**; themes from page 2; back matter = Light Scoring → **Inflation and Growth Read** → **Week by Week Development** (since 19 Aug 2026: per theme, the weekly light dots since June + a since-AIP verdict chip + a "How it developed" note, agent-maintained in `light_history` and reassessed every run — replaced the Theme Light History heatmap). Voice is pitched at generalist investment professionals: acronyms expanded on first use, mechanisms glossed, numbers rounded.
1. NEVER hand-build a dashboard docx — always `engine/macrobasis_fill.py` + the newest `MacroBasis_Report_Template*.docx` at root (plain unversioned filename retired 6 Jul 2026). **Since 13 Aug 2026 the engine also inserts the Co-Op's uploaded charts from `ChartsThemes/` into the theme chart slots at build** (unresolved slots fall back to sized placeholders; rules in the Run Prompt v5.5 + Format Spec v4.2).
2. Prior anchors and statuses come from last week's report (the newest file at `Weekly Reports/` top level), never from memory.
3. Recency gate: only in-window developments are developments; figures prefer Tier 1, lower tiers converted or dropped.
4. Statuses are exactly **Escalating / Held / Deescalating** = MORE/LESS of the theme (not good-vs-bad); the tape veto caps at Held.
5. No standalone numbers; no em-dashes in prose; British/Canadian spelling; every theme lands on an investment implication.
6. Both war legs — **US-Iran** AND **Russia-Ukraine** — tracked by name, every run.
7. The Co-Op's read wins: their hand edits (any human commit over the weekly file) are calibration data, folded back into the specs (regression rule in the Evaluator).
8. Canonical enums and labels (theme names, reference topic headers, status words, **illiquid categories and tones**) = the `_canonical` block in `engine/content_schema.json`.
9. **Illiquids (since 6 Aug 2026, v4 settled):** its own Phase 2 sweep beat (Sonnet 5) and its own page after Theme 6. Layout: charts beside **"What changed this week" = the window's most important PRIVATE EQUITY news**, then a **2x2 framework grid — Performance | Valuations / Leverage | Dry powder — each cell self-contained** (label, bold directional read, evidence + implication + watch bullets). **Retired, do not revive: Buy/Hold/Sell calls and the one-word Signals strip.** It sits **outside the lights system** — no light, no exec status row (still six), no Light Scoring or Week by Week Development (light-history) entry. Block tables are centred on the page at build (margin-asymmetry fix, engine).
10. **Every sweep and every delegated research task runs on Sonnet 5**, dispatched explicitly, never inherited. The orchestrator adjudicates and writes; the beats research. Any beat that hits a search-budget ceiling is a named gap in the manifest, never a silent null.

## Routing table — task → read this first
| Doing what | Owning spec |
|---|---|
| Weekly cycle, any phase (incl. format + voice rules, Phase 6) | `MacroBasis_Weekly_Run_Prompt.md` |
| What to track: theses, drivers, queries, watchpoints, source tiers, **the Illiquids beat** | `MacroBasis_Theme_Charter.md` (team-owned) |
| Scoring lights, QA checks, calibration log | `MacroBasis_Evaluator.md` |
| Market confirmation sweep (tape) | `MacroBasis_Indicator_Panel.md` |
| Writing a daily news file | `Monitoring News/README.md` |
| Building the `.docx` | `engine/MacroBasis_DOCX_Format_Spec.md` + `engine/content_schema.json` |
| Past run audit / resume | `runs/YYYY-MM-DD/` (contract: `runs/README.md`) |
| Acronyms & terms | `memory/glossary.md` |

## File map
Specs at root · `engine/` (fill script, schema, format spec, charts) · `ChartsThemes/` (**the Co-Op's weekly chart uploads — engine inserts them into the report at build; Co-Op-upload only**) · `Monitoring News/` (daily files) · `runs/` (per-run checkpoints) · `Weekly Reports/` (**the weekly deliverable: one current finalized file at top level = next week's prior state + formatting ground truth; `archive/` beneath it holds every older copy — `approved/` = pre-consolidation hand-edited history, `generated/` = pre-consolidation raw outputs**) · `memory/` (glossary, project background) · `HANDOFF.md` (co-op orientation — read first on takeover). Root `archive/` retired to OneDrive at migration (12 Aug 2026); `Dashboards_Claude_Generated/` + `Dashboards_Eduardo_Updated/` merged into `Weekly Reports/` (20 Aug 2026).
