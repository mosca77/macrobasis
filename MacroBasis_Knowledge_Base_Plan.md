# MacroBasis Knowledge Base — Integration Plan (20 Aug 2026)

> **Status: PLAN ONLY — nothing below is operative yet.** No weekly-contract behaviour changes until the execution run described here is completed and approved. On execution, every rule in this document moves into its owning spec (`knowledge/README.md` for the KB itself, plus the small edits listed in §6); this file then retires to `memory/projects/` as decision history. Router principle preserved: each rule will live in exactly one spec.

---

## 1. Objective

Build a **repo-resident knowledge base (KB) of the defining events of H1 2026** (1 January – 30 June 2026) for every surface the agent tracks: the six themes, the Monetary Policy appendix, and Illiquids (private equity). Three uses, in priority order:

1. **Reference during weekly runs** — sweeps and triage can tag a new development as advancing a known prior thread ("this extends the March X"), the same way triage already builds provenance from daily files.
2. **Synthesis on demand** — when the team needs materials, the defining events can be turned into a brief without re-researching anything.
3. **Optional extension** — a designed-but-dormant mechanism to keep promoting post-June defining events into the KB, so it can eventually cover "all main events to date". **Not built in the first run; switched off until the Co-Op enables it.**

**Key constraint discovered while planning:** the repo's own records begin **18 June 2026** (oldest `engine/content_2026-06-18.json`; light history starts week 06-18; oldest approved dashboard is 03 July). `archive/` was retired to OneDrive at migration and is not reachable from here. So roughly January–mid-June must be **reconstructed by research sweeps**, anchored by the Charter's baked-in references (OBBBA, Hormuz, the 30% cap removal, Germany's €500B package, etc.) and by the two June content JSONs. This drives the build design and the token plan in §8.

---

## 2. The deliverable

### 2.1 Location and files

```
knowledge/
  README.md            ← owning spec: format, ID rules, usage, update rules (written at execution)
  events_2026H1.md     ← the KB itself, H1 2026
  events_2026H2.md     ← future, only if the §4.5 extension is switched on
```

- Markdown is the single source of truth. **No parallel JSON index** — the strict block format below is machine-parseable, and one file cannot drift from itself.
- `knowledge/` gets a row in the CLAUDE.md routing table and file map (router edit only, no rules there).
- Like the specs, the KB is agent-written and Co-Op-corrected: **their hand edits to KB entries are calibration data** (same as invariant 7).

### 2.2 Entry format and ID scheme

One block per event, strict format:

```markdown
### KB-GEO-004 — 2026-06-13 — Israel strikes Iran; Hormuz risk premium opens
- **Theme:** Geopolitics & Trade (also: Energy & Transition)
- **Driver:** Hormuz supply shock & conflict trajectory
- **What happened:** 2–3 sentences, dated, figures tier-labelled.
- **Why it mattered:** the mechanism, glossed for a generalist reader.
- **Implication:** the investment implication as it stood at the time.
- **Status effect:** Escalating at the time (omit line if it did not move a light / predates the lights).
- **Sources:** Tier 1, named and dated.
- **Thread:** → KB-GEO-006; → weekly 2026-07-03 onward (ceasefire arc)
```

- **IDs:** `KB-<CODE>-<NNN>`, chronological within a section, **immutable once assigned** (never renumber; a retired entry keeps its ID with a one-line tombstone). Codes: `REG` (regime timeline), `FIS`, `CUR`, `ENE`, `AI`, `GEO`, `DOM`, `MON`, `ILL`.
- **Theme names, status words, display labels** = the `_canonical` block in `engine/content_schema.json`, verbatim. Driver names = the Charter's driver lists, verbatim (or "narrative" for off-list events, matching triage convention).
- **Voice = report voice** (Phase 6 rules: British/Canadian spelling, no em-dashes inside entry prose, no standalone numbers, acronyms expanded on first use per file, mechanisms glossed). This makes entries liftable straight into synthesis output or report continuity phrasing.
- **Cross-theme events are written once**, owned by the primary theme, listed under `also:` for the others — no duplicate entries.

### 2.3 Sections and coverage

Nine sections, in this order:

| # | Section | Code | Notes |
|---|---|---|---|
| 0 | Regime timeline H1 2026 | REG | Quadrant/inflation-growth arc and any theme status flips; from 18 Jun extracted from `light_history`/`quadrant_history`, before that reconstructed narrative (5–8 dated entries) |
| 1 | Fiscal & Deregulation | FIS | |
| 2 | Currency Debasement | CUR | |
| 3 | Energy & Transition | ENE | |
| 4 | Artificial Intelligence | AI | |
| 5 | Geopolitics & Trade | GEO | **Both war legs — US-Iran AND Russia-Ukraine — must each have thread coverage (invariant 6), plus the tariff/trade arc** |
| 6 | Domestic Investing | DOM | |
| 7 | Monetary Policy | MON | Fed/BoC path, aligned to the appendix's reference topics |
| 8 | Illiquids (Private Equity) | ILL | Charter sleeve definition; framework-grid axes (performance, valuations, leverage, dry powder) as selection lens; no Buy/Hold/Sell language |

- Each theme section opens with a **≤3-line "Pre-2026 context" preamble** for carried baselines that predate the window (e.g. Canada Budget 2025) — context lines only, never full entries. Window discipline: full entries are H1 2026 only.

### 2.4 Selection bar and caps

An event earns an entry only if it passes the **defining-event test** — at least one of:
(a) it materially moved the theme's thesis or status at the time; (b) it is a **thread head** that later developments demonstrably built on; (c) it explains a current anchor or baseline the weekly report still carries.

**Caps: 6–10 entries per section, hard cap 12** (REG capped at 8). Total ≈ 55–80 entries, ≈ 10–14k words. Everything that fails the bar is dropped or folded into a surviving entry — the KB is a spine, not a chronicle.

### 2.5 Relationship to the weekly contract

- **Recency gate (invariant 3) explicitly does not apply to KB builds** — the KB is historical by definition. State this in `knowledge/README.md` so it never reads as a contradiction.
- **Source-tier policy applies unchanged**: Tier 1 preferred, lower tiers converted or dropped; every figure dated and tier-labelled.
- The KB **never supplies prior anchors or statuses** to a weekly run — those still come only from last week's approved dashboard (invariant 2). The KB supplies lineage and context, nothing that feeds a number or a light.

---

## 3. Build pipeline (execution run — this is the work being planned, not done now)

Run as its own session on a dedicated branch (suggest `claude/knowledge-base-build`), checkpointed to `runs/YYYY-MM-DD-kb/` under the existing runs contract (manifest + named gaps).

- **K0 — State.** Read this plan, the Charter, `_canonical`, and the two June content JSONs. Fix the window (2026-01-01 to 2026-06-30) and the section caps.
- **K1 — Repo harvest (orchestrator, cheap, do first).** Extract every dated H1 event already present in the repo: `content_2026-06-18/25.json` developments and histories, `light_history`/`quadrant_history`/`regime_history`, the earliest approved dashboards (which reference June events), and the Charter's own baked-in H1 references (drivers and watchpoints encode many of them: OBBBA, Hormuz shock and passthrough table, NATO/EU 5% commitments, Germany €500B, 30% cap removal, Canada Strong Fund, CUSMA review…). Output: per-theme **seed lists** with what is already known and what is missing.
- **K2 — Research beats (9 beats, one per section, all on Sonnet 5, dispatched explicitly — invariant 10).** Each beat receives its Charter section, its seed list, the entry schema, and the defining-event test; it returns candidate entries with Tier 1 sourcing. Beats fill gaps around the seeds; they do not re-research what K1 already established. Any beat hitting a search-budget ceiling returns a **named gap**, never a silent null.
- **K3 — Adjudication (orchestrator).** Dedupe cross-theme (assign primary owner + `also:`), apply the bar and caps, assign IDs chronologically, wire `Thread:` links between entries and forward to the weekly reports that exist (03 Jul onward).
- **K4 — Write and validate.** Write `knowledge/events_2026H1.md` + `knowledge/README.md`. Validation pass: every entry in-window, dated, sourced, canonical theme and driver names, voice rules, unique sequential IDs, both war legs present, caps respected. *(Optional, additive: a small `engine/check_kb.py` in the spirit of `check_specs.py` to lint IDs/dates/enums — nice to have, not required for v1.)*
- **K5 — Deliver.** Manifest + gap list to `runs/`, commit, push, **PR for the Co-Op's manual review — no auto-merge** (the KB becomes ground truth, so a human approves it; the Routine auto-merge contract stays weekly-only). The Co-Op's edits on review are folded back as calibration.

**Cost lever (optional, the Co-Op's call):** if any archived H1 dashboards or notes can be dropped into the repo (or pasted into the run) before K2, the research beats shrink to gap-filling — roughly halves the expensive step. Not required; the pipeline works without it.

---

## 4. Integration into the weekly agent (triage-style referencing)

Small, additive hooks — Run Prompt bumps to v5.7. Nothing visual changes in the report.

- **4.1 Phase 2 (sweeps).** Each theme beat's dispatch includes its KB section (≈1–2k tokens, that section only, never the whole file). Beats are instructed to flag when a finding **advances a KB thread** and name the ID.
- **4.2 Phase 4 (triage table).** One new column: **`KB thread`** (an ID or "—"). This is the exact analogue of the existing Provenance column: Provenance says where the finding came from this week; KB thread says which prior defining event it builds on. Discard lines and checked-null lines are unaffected.
- **4.3 Content JSON.** Optional per-theme `kb_refs` array (IDs the week's developments advanced). Schema edit is non-breaking (optional field); **the fill engine ignores it — zero engine/template/layout risk.**
- **4.4 Report prose.** No new blocks, rows, or pages. Writers may use thread context for continuity phrasing under the existing continuity discipline; that is the only visible effect.
- **4.5 The extension option (designed now, OFF by default).** A gated Phase 0 step, "KB maintenance": when enabled, the orchestrator checks last week's dashboard against the **promotion rule** — an event is promoted into `events_2026H2.md` only if it (a) flipped a status light, (b) moved the quadrant, or (c) the Co-Op flags it. One entry max per theme per week, same format, IDs continue. This is the whole mechanism for "extend to all main events to date": no separate project later, just flip the gate. Until enabled, weekly runs read the KB and never write it.

**Evaluator (optional one-liner):** QA check that any KB ID cited in triage or `kb_refs` exists in `knowledge/`.

---

## 5. Synthesis on demand

Documented in `knowledge/README.md` as an invocation: **"Synthesize the defining events for [theme(s) / period]"** → reads the KB only (no sweeps, no web research), outputs a dated brief in report voice. Default output is Markdown committed to `runs/` or handed back in chat; a `.docx` only if asked, built as a plain document — **never via `macrobasis_fill.py`, which stays dashboard-only.** This is deliberately the cheapest possible operation: the KB exists precisely so materials cost near-zero tokens.

---

## 6. Spec-edit checklist for the execution run

| File | Edit | Size |
|---|---|---|
| `knowledge/README.md` | NEW — owning spec for everything in §2, §4.5 promotion rule, §5 synthesis | new file |
| `knowledge/events_2026H1.md` | NEW — the KB | new file |
| `CLAUDE.md` | Routing-table row + file-map mention (router only, no rules) | 2 lines |
| `MacroBasis_Weekly_Run_Prompt.md` | v5.7: Phase 2 KB-context injection; Phase 4 `KB thread` column; gated Phase 0 "KB maintenance" step; changelog line | ~10 lines |
| `engine/content_schema.json` | Optional `kb_refs` per theme + `_kb_note` | ~5 lines |
| `MacroBasis_Evaluator.md` | Optional: KB-ID-exists QA check | 1 line |
| `HANDOFF.md` | One-line pointer to `knowledge/` | 1 line |
| `MacroBasis_Theme_Charter.md` | **No edits — team-owned** | — |
| `engine/macrobasis_fill.py`, template, `check_layout.py` | **No edits** | — |

## 7. What does not change

Layout and block order; the lights system, scoring, and Light History; prior-anchor discipline (invariant 2); the recency gate for weekly developments; the engine, template, and `check_layout` gate; Co-Op-upload-only folders; the daily monitor protocol; the Illiquids page contract. The KB is context infrastructure beside the pipeline, not a new pipeline stage in the report path.

## 8. Execution model and token plan

**Recommendation: run the entire execution on Sonnet 5** — orchestrator and all nine research beats (the beats are mandatory Sonnet 5 anyway under invariant 10).

Why Sonnet 5 is sufficient for the orchestrator here: every design decision is already made in this plan; what remains is retrieval, curation against a strict schema, and small mechanical spec edits — squarely Sonnet-shaped work, at a fraction of the cost of a larger model. Escalate a single step to Opus 5 only if review shows the K3 adjudication or the Run Prompt edits came back sloppy; do not use Haiku (the voice rules and cross-theme adjudication are too fragile for it).

**Sequencing to preserve tokens:**
1. **Step 1 — KB build (K0–K5)**, fresh Sonnet 5 session, prompt: "Execute `MacroBasis_Knowledge_Base_Plan.md`, Step 1." This is the dominant cost; the nine web-research beats drive it. Rough order: comparable to one weekly run's Phase 2, plus ~12k words of writing — roughly 250–500k tokens on Sonnet 5, and materially less if archived H1 material is seeded first (§3 cost lever).
2. **Step 2 — Integration edits (§6)**, same or separate Sonnet 5 session after the KB PR is approved — small, ~30–60k tokens.
3. Steps 1 and 2 are independently shippable; the KB alone already delivers uses 1 (partially) and 2 (fully) of §1.

## 9. Acceptance criteria (gate for the execution run)

1. `knowledge/README.md` and `events_2026H1.md` exist; every entry has a unique immutable ID, an in-window date, a canonical theme, a tier-labelled dated source, and an implication.
2. Section caps respected; every section present, including REG, MON, ILL.
3. GEO covers **both** US-Iran and Russia-Ukraine by name, plus the tariff arc.
4. Thread links resolve (KB→KB and KB→existing weekly report dates); voice rules hold (no em-dashes in entry prose, British/Canadian spelling, no standalone numbers).
5. Named gaps in the run manifest for anything a beat could not source — no silent nulls.
6. Weekly pipeline untouched except the §6 edits; no engine/template/`check_layout` diffs; a subsequent weekly run passes unchanged with the KB present.
7. PR reviewed and merged by the Co-Op; their edits logged as calibration.

## 10. Non-blocking confirms for the Co-Op (answer any time before the build run)

1. Can any pre-June H1 dashboards or notes be seeded from the OneDrive archive into the repo first? (Halves the research cost; optional.)
2. Per-section hard cap 12 acceptable, or tighter?
3. `knowledge/` at repo root confirmed as the home?
