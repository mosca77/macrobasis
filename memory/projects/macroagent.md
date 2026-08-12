# Project: MacroAgent (MacroBasis) — as of 6 Jul 2026

## What it is
A weekly macro-theme tracking + reporting agent for the OPTrust OCIO team. It produces a
standardized **dashboard report** (`MacroBasis_Dashboard_YYYY-MM-DD.docx`) that picks up exactly
where last week's report left off. "MacroBasis" is the system name; "MacroAgent" is the project.

**Operating docs (authoritative, this folder):** `MacroBasis_Weekly_Run_Prompt.md` (v5.1, Phases 0–8,
invocation contract + gates checkpointed to `runs/YYYY-MM-DD/`), `MacroBasis_Evaluator.md` (Phase 7,
v2 — north-star minimal-edits read, daily-coverage reconciliation, calibration regression rule),
`MacroBasis_Theme_Charter.md` (what to track),
`Monitoring News/README.md` (daily monitor protocol v2: Sonnet fan-out, completeness loop, Weekly
Signal block),
`MacroBasis_Indicator_Panel.md` (market confirmation sweep), `engine/` (fill engine v3.2 + format
spec + content schema — the schema is the canonical source of enums/labels), the current template =
newest `MacroBasis_Report_Template*.docx` at root (plain unversioned filename retired 6 Jul 2026),
`Dashboards_Eduardo_Updated/` (formatting ground truth), `runs/` (per-run checkpoints: ledger, panel,
triage, self_audit + manifest w/ edits-count KPI). **CLAUDE.md is a thin router (since 6 Jul 2026):**
invariants + routing table only; the specs own all detail. This file is a summary only — where it
conflicts with those files, they win.

## The six themes (fixed order)
1. Fiscal Expansion & Deregulation (+ Monetary Policy Tracker as Theme 1 Appendix)
2. Currency Debasement
3. Energy & the Energy Transition
4. Artificial Intelligence
5. Geopolitics & Trade (both war legs BY NAME: US-Iran, Russia-Ukraine; + CUSMA/trade)
6. Domestic Investing Pressures (Canada)

## Status system (lights, since 2 Jul 2026)
🟢 Escalating / 🟡 Held / 🔴 Deescalating = MORE/LESS of the theme, not good-vs-bad.
Scored with the Evaluator (direction × materiality, ±3 thresholds, contradiction rule).
**Tape veto (3 Jul):** tradeable tape contradicting the news caps the light at Held.
Human overrides win and are logged as calibration points (2 Jul Currency, 3 Jul AI).
Old Intact/Strengthening/Weakening vocabulary and the exec Key Risks register are retired;
the six Charter risks are tracked in triage.

## Report structure (engine-rendered)
Title → Exec Summary (quadrant + marker trail of 3 · Weekly Direction ONE sentence +
3 Influencing-Factor lines · Status Dashboard · Key Developments | Implications) →
Theme 1 → Monetary appendix (no light/status word) → Themes 2–6 → Lights Guide → References
(by topic, tier-labelled). Theme blocks: Status Ball + status line, What changed (3–5
facts-first paragraphs incl. the market's reaction), Key Development (text left, chart right,
no "Key development:" prefix), Implication (growth/inflation sign + offsets), Watch next week.

## Non-negotiable mechanics
- **Never hand-build the docx.** Fill engine only: `engine/macrobasis_fill.py` + content JSON.
- Weekly mode needs last week's dashboard attached (state carry + quadrant trail); baseline mode = confirm first.
- Recency gate; no standalone numbers; prior anchors from last week's report, never memory.
- Sources: all tiers searchable, figures prefer Tier 1, lower-tier findings converted or dropped.
- Research order (v5): Phase 1 Week Ledger from the daily files FIRST (story threads + candidates +
  coverage map), then Phase 2 = the FULL sweep unchanged in scope: exhaustive (all Charter queries)
  AND expansive (narrative sweep) AND both conflict legs AND late-breaking (post-9AM filing-day gap);
  Phase 3 market confirmation (full Indicator Panel + claim→indicator protocol), every run.
- Phase 4 triage pause (provenance column; every daily candidate reconciled) → Phase 7 evaluator
  pass → Phase 8 self-audit + validate/render check.
- Daily monitor (9AM scheduled task, protocol v2): orchestrator + parallel Sonnet beats, market-first
  capture, completeness loop (front-page / tape-attribution / calendar / coverage, max 3 rounds),
  Weekly Signal block on top (persistent stories, NEW/CARRIED candidates, theme temperature).

## Settled facts
- Audience: OCIO pension investment team; human (Eduardo) reviews before it circulates.
- Cadence: weekly. Spelling: British/Canadian. Accent `#7B2952`, body Myriad Pro 11pt.
- Voice: Eduardo's macro/outlook style — facts first, no scene-setting or kickers, measured verbs,
  glossed jargon, hyphenated year ranges, exposures not trade advice. See CLAUDE.md 2 Jul + 3 Jul
  voice bullets for the full list.
- Latest state: `Dashboards_Eduardo_Updated/` holds his approved versions; his 3 Jul tweaked
  2026-07-02 dashboard (THISWEEK) is the current formatting + voice ground truth.

## Open questions
- The AIP "Back Pocket Document" is referenced as knowledge but not in this folder — get it if charts/figs needed.
