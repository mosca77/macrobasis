# Monitoring News — daily market monitor (protocol v2.1, 18 Aug 2026)

**What this folder is.** One file per day, named `YYYY-MM-DD_News.md`, written every morning at 9:00 AM by a scheduled task. Each file is an exhaustive raw log of ALL market-relevant developments of the last 24 hours — **market-first, not theme-first**: anything with material market implications belongs, whether or not a theme query would have surfaced it. Theme mapping happens after capture. The files do two jobs: (1) they break the weekly research problem into daily slices — the weekly run consolidates them into its Week Ledger (Run Prompt, Phase 1) before sweeping; (2) they accumulate the week's signal — each file opens with a **Weekly Signal block** tracking persistent stories and likely report candidates, so the Co-Op can watch the report build during the week and see whether each theme is developing.

**What these files are NOT.** Not a report, not verified-for-publication data. Raw-log entries are leads; verification (recency gate, tier conversion, no-standalone-numbers context) happens at weekly run time. The Weekly Signal block is the ONE interpretive section; the raw log below it stays analysis-free (no adjectives, no implications).

## How it runs: orchestrator + Sonnet sweep beats

The scheduled task acts as **orchestrator**. It dispatches the sweep as parallel subagents (Agent tool, general-purpose, **model: sonnet**), consolidates their returns, runs the completeness loop, and writes the file. If subagent dispatch is unavailable, run the same beats sequentially in-session — never skip a beat.

## Daily protocol (every morning, 9:00 AM)

**0. Setup.**
- Window: the 24 hours ending now. Date the file with today's date. If `YYYY-MM-DD_News.md` already exists, stop and report — never overwrite.
- Read this week's earlier daily files for continuity: every daily file dated after the most recent `MacroBasis_Dashboard_*.docx` in the MacroAgent folder (fallback: the last 5 daily files). These feed the persistence tracking in step 4 and the calendar check in step 3.

**1. Round 1 — dispatch the sweep beats (parallel, Sonnet).** Each beat returns entries in file format: 1–2 factual sentences, key numbers, as-of time if intraday, source name + tier in parentheses, and its key links. Err on inclusion — a marginal item costs one line; a missed item costs the weekly report.

- **Beat 1 — Market-wide (the anchor beat, NOT theme-scoped):** front-page recaps ("markets today <date>", "stock market recap <date>", "market news last 24 hours", Europe variant, Asia variant), session wraps, biggest single-name movers with a macro read, cross-asset stories. Plus the **tape snapshot**: 2y & 10y UST, DXY, USD/CAD, USD/JPY, WTI/Brent, gold, copper, S&P 500, Nasdaq, SOX, VIX, bitcoin — levels with daily change; note holiday closures.
- **Beats 2–8 — one per theme (the MacroBasis six + Monetary), 3–4 queries each:** the Charter anchors PLUS one open expansion query beyond the keywords ("<theme> news <date>") for adjacent and second-order stories:
  1. Fiscal & Deregulation (NATO/defence budgets, US deficit/Treasury/refunding, Canada programs, Germany/EU packages, deregulation)
  2. Monetary (Fed/BoC/ECB/BoJ/PBoC decisions and speakers, CPI/PCE/payrolls-type releases)
  3. Currency Debasement (dollar, gold, reserves/COFER/TIC, yen, bitcoin as the speculative wing)
  4. Energy & Transition (grid, data-centre power, renewables, LNG, curtailment, IEA/FERC)
  5. AI (hyperscaler capex, semis/memory, AI financing/raises, monetization datapoints)
  6. Geopolitics & Trade — **both war legs BY NAME: US-Iran AND Russia-Ukraine** — plus CUSMA/tariffs/fertilizer channel
  7. Domestic Canada (BoC, Canada Strong Fund/CGF/CIB, pension policy, CAD-relevant data)
- **Beat 9 — Calendar:** reconstruct what was SCHEDULED in the window (yesterday's releases, meetings, auctions — from the prior file's Watch list plus the standard calendar) so nothing scheduled goes unchecked; and build the next-7-days Watch list (decisions, summits, releases, auctions, earnings with macro read).

**2. Consolidate.** Merge beat returns; dedupe (same fact = one entry, best source); place each item in its theme section, and genuinely unthemed items under "Broad market & other developments" — that section is a first-class product of Beat 1, not a leftover bucket.

**3. Completeness loop (repeat until pass, max 3 rounds).** The sweep is done when the checks pass, not when the queries run out:
- **a. Front-page test:** any story appearing in 2+ recap sources but absent from the log = gap.
- **b. Tape attribution:** every material move in the tape snapshot (roughly: equities/FX >0.5%, rates >5bp, commodities >1%, or any move the recaps lead with) has a logged driver entry, or an explicit "driver unclear" line.
- **c. Calendar closure:** every item scheduled in the window (from Beat 9's reconstruction) is logged or checked-null.
- **d. Coverage:** every theme, both war legs by name, and Monetary have entries or an explicit checked-null line.

Gaps → dispatch targeted Sonnet sweepers for just those gaps → merge → re-check. If a gap survives round 3 (e.g. search outages), record it under "Checked, nothing found" with a recheck note — never silently.

**4. Weekly Signal block (orchestrator writes it LAST, after the raw log is complete).** Using this week's earlier files plus today's log:
- **Persistent stories:** every story seen on 2+ days since the last dashboard — story, day count, direction of travel, theme(s). Persistence is the strongest weekly-inclusion signal.
- **Likely report candidates:** the 5–8 items most likely to make the weekly report, each with theme + one line why (persistence, materiality, tape confirmation). Mark each NEW (first flag today) or CARRIED (flagged on a prior day — keep carrying until the dashboard runs or the story dies). Be willing to drop a dead candidate; say so ("dropped: no follow-through").
- **Theme temperature:** one row per theme + Monetary: **Developing / Quiet** plus a one-line direction note. This is a leading read for the Co-Op, not a status call — no lights, no Escalating/Held/Deescalating words.

**5. File format (keep exactly this structure):**

```
# Daily News Monitor — YYYY-MM-DD (window: <prev day ~9AM> → <today 9AM>)
Generated automatically at 9:00 AM. Raw leads, verified at weekly run time.

## Weekly signal (interpretive — the one non-raw section)
**Persistent stories (since last dashboard):**
- <story> — day N · <direction of travel> · <theme(s)>
**Likely report candidates:**
- <item> — <theme> — <why> (NEW / CARRIED since DD Mon)
**Theme temperature:**
| Theme | Temp | Direction note |
|---|---|---|
| 1 Fiscal & Dereg | Developing/Quiet | <one line> |
| Monetary | … | … |
| 2 Currency Debasement | … | … |
| 3 Energy & Transition | … | … |
| 4 AI | … | … |
| 5 Geopolitics & Trade | … | … |
| 6 Domestic (Canada) | … | … |

## Top of the tape
- <the 3–6 items likely to lead any recap, one line each>

## Market tape snapshot (as of ~9AM ET)
- <levels with daily change where found; note market closures>

## 1 · Fiscal & Deregulation
- <entries>
## Monetary
- <entries>
## 2 · Currency Debasement
- <entries>
## 3 · Energy & Transition
- <entries>
## 4 · AI
- <entries>
## 5 · Geopolitics & Trade
- <entries — US-Iran and Russia-Ukraine each get a line even if checked-null>
## 6 · Domestic (Canada)
- <entries>
## Broad market & other developments
- <entries — everything material that maps to no theme>
## Watch (next 7 days)
- <dated items>
## Checked, nothing found
- <themes/legs/calendar items with no in-window development — say so explicitly; note any unrecovered search gaps>

## Key links (for weekly verification)
- <URLs>
```

**6. Save as** `Monitoring News/YYYY-MM-DD_News.md`. Never overwrite a previous day's file.

**7. Automated finish (v2.1, 18 Aug 2026) — the run lands the file on `main` itself; the Co-Op clicks nothing.**
- **Gate first:** run `python3 engine/check_specs.py --daily "Monitoring News/YYYY-MM-DD_News.md"` (stdlib-only, no pip installs needed) and fix any missing headers it names before committing. Do not commit a file that fails the skeleton check.
- **Then:** commit the new file to the session's working branch (commit message `Daily news YYYY-MM-DD`), push with `git push -u origin <branch>`, open a PR to `main` titled `Add daily news monitor for YYYY-MM-DD`, and **merge it immediately** (merge commit, matching the repo's history). The daily monitor has no layout gate — the skeleton check above is its only gate — so the merge is unconditional once that passes.
- **Scope:** the automatic merge covers ONLY the new `Monitoring News/YYYY-MM-DD_News.md` file (plus, when a run was explicitly asked to change this protocol, that spec change). A daily run must never fold unrelated file changes into the auto-merged PR.
- **If any step fails** (push rejected, PR blocked, merge refused): stop, leave the PR open if one was created, and notify the Co-Op with the finished file delivered in-chat — never retry by force-push and never leave the file only on an unmerged branch silently. A file that exists only on a side branch does not exist for the weekly run, which reads dailies from `main`.

## How the weekly run uses these files

At Phase 1 the weekly run reads every daily file dated inside its window and consolidates them into the **Week Ledger** (story threads with day-by-day progression + the union of all flagged candidates) BEFORE running its full Charter sweep — the dailies are the primary corpus; the sweep verifies, extends, and contradicts. Entries are leads, not pre-verified facts: each is verified in-window and converted to sourced form before use. Reconciliation is enforced by the Evaluator: every flagged candidate ends up in the report or gets an explicit discard line with a reason — nothing the monitor flagged is silently dropped.
