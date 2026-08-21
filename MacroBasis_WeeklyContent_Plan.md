# MacroBasis WeeklyContent Split — Migration Plan (21 Aug 2026)

> **Status: PLAN ONLY — nothing below is operative yet.** On execution, every rule moves into its
> owning spec (checklist in §7) and this file retires to `memory/projects/` as decision history.
> Router principle preserved throughout: each rule lives in exactly one spec.

---

## 1. Objective and target architecture

Split the weekly pipeline across two surfaces while keeping this repo the canonical home of every
rule and every record:

| Surface | Owns | Produces |
|---|---|---|
| **claude.ai Project: MacroBasis DailyNews** (scheduled, daily 9:00 AM) | The daily sweep (protocol unchanged in substance) | One `YYYY-MM-DD_News.md` per day, as a chat artifact |
| **claude.ai Project: MacroBasis WeeklyContent** (run Thu/Fri) | Research + drafting: Run Prompt Phases 0–7 in Projects mode | `MacroBasis_Content_YYYY-MM-DD.md` + `MacroBasis_State_YYYY-MM-DD.md` + the Phase 1–4 checkpoint |
| **This repo, driven from VS Code (Copilot + Claude)** | Formatting + build: validate the content MD, convert to JSON, build the docx, file it | `engine/content_*.json`, the dashboard docx, archive rotation, commits |

The 2026-08-21 Projects run (state file, checkpoint, content MD now in hand) proved the middle row
works; this plan hardens it, fixes its context deficit, and gives the repo side a formal
content-fed build contract. **The full "Run the weekly cycle" pipeline stays intact as a fallback
and audit path — MacroAgent is kept, not retired.**

**The sync contract (the one new structural rule).** A new `projects/` folder in this repo holds
the canonical masters of every file uploaded to either Project. Uploaded copies are **exports, not
forks**: each carries a banner with version + sync date (the pattern already proven by the
Evaluator Projects copy). When a repo spec changes, its export is regenerated the same day and the
Co-Op re-uploads it. Rules never live only in a Project.

---

## 2. Workstream 1 — MacroBasis DailyNews Project

**New master: `projects/MacroBasis_Daily_Projects.md`** — the daily protocol (README v2.1) adapted
to Projects mode. Substance unchanged: beats 1–9, the completeness loop, the Weekly Signal block,
the exact file format, checked-null discipline, both war legs by name. What changes:

1. **No repo, no commit.** Step 7 (check_specs gate → commit → PR → merge) is replaced by: output
   the finished file as a downloadable artifact named `YYYY-MM-DD_News.md`, byte-compatible with
   the README v2.1 skeleton (so `check_specs.py --daily` still passes when the file later reaches
   the repo, and the WeeklyContent Phase 1 ledger builds identically).
2. **No subagents.** Beats run sequentially in one chat — the same named-reduction honesty flag the
   Projects-mode weekly run already uses. Never skip a beat; a beat that hits a budget ceiling is a
   named gap.
3. **Continuity re-based** (the real design problem: a scheduled chat cannot see yesterday's chat).
   Continuity comes from three layers, in order:
   - the **latest weekly state file** in project knowledge (refreshed weekly at filing) — gives the
     window start, watch items, and standing threads;
   - **yesterday's daily file if present in project knowledge** — the Co-Op's one-minute morning
     routine is: download yesterday's artifact, add it to project knowledge (and remove files older
     than the window);
   - each file's **Weekly Signal block stays fully self-describing** (persistent stories carry
     their own day counts and first-flag dates), so a missed upload degrades day-count precision,
     never correctness — the same recompute-from-presence rule the Run Prompt already applies to
     pre-13-Aug files.
4. **Task prompt stays minimal**, mirroring the existing Routine: "Follow
   `MacroBasis_Daily_Projects.md` in project knowledge exactly; never overwrite a day's file."

**Project knowledge — fixed:** the Daily Projects protocol; `MacroBasis_Theme_Charter.md` (the
full Charter, not a derived query digest — a digest would be a fork that drifts); optionally
`memory/glossary.md`. **Rotating:** the latest state file; the current week's daily files as they
accrue.

---

## 3. Workstream 2 — MacroBasis WeeklyContent Project

**New master: `projects/MacroBasis_Content_Spec.md`** — the file the Project already runs on,
brought into the repo as canonical and improved. Ownership model: the Run Prompt remains the owning
spec for research, scoring and voice rules; the Content Spec is a **derived rendering of Phases
0–7 for Projects mode** (translation banner, like the Evaluator copy) plus a small Projects-only
section it owns outright: the in-chat Phase 4 gate, the output-file contract, and the filing
checklist. Amendment rule extended: a Run Prompt change triggers a same-day Content Spec re-export.

**Context deficit fixes (the "much less context than the agent had" problem), in impact order:**

1. **Add the Knowledge Base to project knowledge.** `knowledge/events_2026H1.md` (built 20 Aug) is
   exactly the deep-history lineage Projects mode lacks. The Projects triage table keeps the
   Run Prompt's `KB thread` column so every finding can be tagged as advancing a named prior event.
2. **Add a Week Digest log to the state file** — new appended section 12, one ~120-word block per
   week: the week's one-story read, the six lights, any verdict rewrites, watch items resolved and
   which way. Append-only like sections 5–7, so the connective tissue deepens every week inside a
   single rotating file instead of an ever-growing pile of uploads. **One-time backfill** by the
   repo agent from `engine/content_2026-06-18.json` → `content_2026-08-13.json` (nine weeks — the
   repo has the history; the Project does not).
3. **Keep the prior full content MD in project knowledge**, not just the state file — it is the
   voice ground truth and the anchor cross-check. One week deep is enough alongside the digest.
4. **Calibration continuity:** the Evaluator Projects export carries the calibration log; the
   Co-Op's overrides at the in-chat gates are recorded in the state file by the run itself; hand
   edits observed at build time (§4) flow back into `MacroBasis_Evaluator.md` in the repo and
   re-export. Invariant 7 survives the split intact.

**Output contract per run (all as downloadable artifacts):** the content MD (blocks keyed to
`content_schema.json` names, word budgets printed per block), the state MD (fixed shape, now with
section 12), and the Phase 1–4 checkpoint. The run ends by printing a **filing checklist** — the
exact project-knowledge swap list (replace state, replace prior content MD, delete the window's
dailies, leave the spec exports alone) plus the repo hand-off list (§4 inputs). This is the honest
version of "auto-update its context": Projects knowledge cannot update itself, so the run produces
exact replacement files and a mechanical checklist instead.

**Project knowledge — fixed:** the Content Spec; `MacroBasis_Theme_Charter.md`;
`MacroBasis_Evaluator_Projects.md`; `MacroBasis_Indicator_Panel.md`; `knowledge/events_2026H1.md`;
optionally `memory/glossary.md`. **Rotating:** the latest state file; the prior week's content MD;
the window's daily files.

---

## 4. Workstream 3 — repo (MacroAgent) changes, minimal and additive

1. **NEW `MacroBasis_Build_Run.md` (root)** — the content-fed build contract for the VS Code agent.
   - **Trigger:** "Build the report for [date] from the content file."
   - **Inputs:** `MacroBasis_Content_YYYY-MM-DD.md` + `MacroBasis_State_YYYY-MM-DD.md` (dropped
     into `runs/YYYY-MM-DD/` by the Co-Op), the window's daily files (optional batch, §6 D2),
     charts already uploaded to `ChartsThemes/`, and the prior dashboard in `Weekly Reports/`.
   - **Steps:** validate the MD against a **block→field mapping table** (owned by this doc, enums
     deferred to `_canonical` per invariant 8: every schema block present, canonical status words
     and labels, word budgets, light-history and regime rows appended not rewritten, six exec rows,
     no Illiquids light) → convert to `engine/content_YYYY-MM-DD.json` → light-history/quadrant
     images via `make_light_history.py` → build via `macrobasis_fill.py` + newest template →
     `check_layout.py` gate → file to `Weekly Reports/` with archive rotation → commit
     "Weekly run YYYY-MM-DD".
   - **Division of labour (hard rule):** the build agent never researches, rewrites substance, or
     fills a gap with its own words. A missing block, budget violation, enum mismatch, or
     state-vs-content inconsistency is a **named validation error back to the Co-Op**, not a fix.
   - Build/file/commit mechanics are POINTERS to Run Prompt Phase 8 ("Producing the file"), which
     stays the owning spec — no duplicated rules.
2. **NEW `projects/` folder** with `README.md` (the sync contract in §1) and the masters:
   `MacroBasis_Content_Spec.md`, `MacroBasis_Daily_Projects.md`,
   `MacroBasis_Evaluator_Projects.md` (moves here from wherever it lives today; regenerated from
   the root Evaluator), `MacroBasis_State_TEMPLATE.md` (the state-file shape incl. section 12).
3. **`engine/check_specs.py` extensions:** a `--content <md>` mode (skeleton check for the content
   MD: block presence, canonical enums, appended histories) the build run gates on before
   converting; and a second valid run-dir shape (`content.md` + `state.md` + `build_audit.md`) so
   content-fed run folders pass the existing four-file check.
4. **Router edits, no new rules:** `CLAUDE.md` — Environment gains the operating model (research in
   the two Projects, build via "Build the report for [date]"), routing-table rows for
   `MacroBasis_Build_Run.md` and `projects/`, and a How-to-run line; `HANDOFF.md` — orientation
   update; `Monitoring News/README.md` — a dated mode note (files now produced by the DailyNews
   Project; how they reach the repo per §6 D2); `memory/projects/macroagent.md` — the decision
   entry.
5. **What does not change:** the engine, template, `check_layout` gate, and schema enums; archive
   rotation and commit messages; the Charter (team-owned); the full weekly cycle and its Run Prompt
   (kept as fallback/audit); the KB; all invariants (invariant 10's Sonnet-5 dispatch reads, in
   Projects mode, as the already-proven "sequential beats, named reduction" flag).

---

## 5. The weekly operating loop (as it will read in HANDOFF)

Daily: the 9:00 task runs in DailyNews → morning routine: add yesterday's file to project
knowledge. Thu/Fri: (1) run WeeklyContent → confirm the Phase 4 gate and lights in-chat → download
the three output files; (2) BBG: run the charts macro, upload `2026-mm-dd` to `ChartsThemes/`;
(3) drop content + state MDs into `runs/YYYY-MM-DD/`, tell the VS Code agent "Build the report for
[date]" → it validates, builds, gates on check_layout, files and commits; (4) execute the filing
checklist in both Projects. Done — one current file at `Weekly Reports/` top level, same as today.

---

## 6. Decision points for the Co-Op (answer any time before execution)

- **D1 — GitHub connector from the claude.ai account: still available?** If yes (Mode A), the
  dailies keep auto-committing to `Monitoring News/` exactly as today and WeeklyContent reads
  state/dailies/KB live from the repo — most of the manual download/upload in §2–3 disappears.
  The plan is written Mode-B-safe (no connector, manual moves); Mode A is a pure simplification.
- **D2 — dailies into the repo weekly?** Recommended: the build run batch-commits the window's
  daily files alongside the report, keeping provenance, the fallback full cycle, and
  `check_specs` coverage. Alternative: dailies live only in the Project (repo loses its daily
  corpus; fallback cycle degrades to sweep-only).
- **D3 — existing Routines at cutover:** pause the Thursday unattended weekly Routine (else it
  files a competing report); retire the daily 9:00 Routine if Mode B (replaced by the Project
  task) or keep it if Mode A.
- **D4 — pilot:** build 2026-08-21 from the already-produced Projects output as the first
  content-fed build (the repo's current dashboard is still 08-13, so this week is the natural
  test), before the specs are finalized. Recommended: yes — it validates the mapping table against
  a real content MD.

## 7. Spec-edit checklist for the execution run

| File | Edit |
|---|---|
| `MacroBasis_Build_Run.md` | NEW — content-fed build contract + block→field mapping (§4.1) |
| `projects/README.md` | NEW — sync contract |
| `projects/MacroBasis_Content_Spec.md` | NEW master — Phases 0–7 Projects rendering + output/filing contract (§3) |
| `projects/MacroBasis_Daily_Projects.md` | NEW master — daily protocol, Projects mode (§2) |
| `projects/MacroBasis_State_TEMPLATE.md` | NEW — state shape incl. section 12 Week Digest log |
| `projects/MacroBasis_Evaluator_Projects.md` | Moved/regenerated export of the root Evaluator |
| `engine/check_specs.py` | `--content` mode + content-fed run-dir shape (§4.3) |
| `CLAUDE.md`, `HANDOFF.md`, `Monitoring News/README.md`, `memory/projects/macroagent.md` | Router/orientation/mode-note/decision-history edits only |
| Charter, engine fill/template/check_layout, Run Prompt research phases | **No edits** (Run Prompt gains only the same-day re-export amendment line) |

## 8. Build order

1. **PR 1 (repo):** everything in §7, plus the nine-week digest backfill into the state template's
   section 12 seed. Reviewed by the Co-Op, no auto-merge.
2. **Project setup (Co-Op, ~15 min):** create/refresh both Projects from the `projects/` masters
   with the §2–3 knowledge lists; set the daily scheduled task.
3. **Pilot (D4):** build 08-21 in VS Code from the existing content MD; fold any mapping-table or
   validation fixes into `MacroBasis_Build_Run.md`.
4. **Cutover:** pause/retire Routines per D3; first full new-flow week; Co-Op edits logged as
   calibration; this file retires to `memory/projects/`.
