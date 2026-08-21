# Projects mode — running the weekly cycle with no repo and no engine

**What this folder is.** Everything needed to produce the week's report **content** inside a
claude.ai Project, with no GitHub connector, no local files, no Python and no build step. The agent
researches, adjudicates and writes; the Co-Op does the formatting by hand into
`MacroBasis_Report_Template_v6.docx`.

**What it is not.** It is not a replacement for the repo pipeline. The repo run still owns the
deterministic gates (`check_layout.py`, `check_specs.py`), chart insertion from `ChartsThemes/`, the
`runs/` checkpoints and the calibration loop. Section 6 of the Content Spec lists what is lost, in
plain terms. Use Projects mode when the repo path is unavailable or when you want the content
without the build.

---

## Setup, once

Create a Project and upload these six files to **Project knowledge**:

| File | Words | What it does |
|---|---:|---|
| `MacroBasis_Content_Spec.md` | ~7,300 | The contract. Phases 0-7, the field-by-field output contract, the canonical enums and word budgets, the voice rules, the self-audit checklist |
| `MacroBasis_Theme_Charter.md` | ~4,800 | What to track. Verbatim copy of the repo root file |
| `MacroBasis_Indicator_Panel.md` | ~1,300 | The market-confirmation layer. Verbatim copy of the repo root file |
| `MacroBasis_Evaluator_Projects.md` | ~2,700 | The seven QA families. Repo file plus a banner translating three repo-only references |
| `MacroBasis_Glossary_Projects.md` | ~550 | Acronyms and house terms |
| `MacroBasis_Output_Template.md` | ~1,650 | The skeleton the agent fills and returns |

Roughly 18,300 words, about 24,000 tokens. Set the Project's custom instructions to one line:

> Read `MacroBasis_Content_Spec.md` first and follow it exactly. It is the contract for every run.

---

## Every week

**1. Attach to the chat** (not to Project knowledge — Project knowledge is retrieved in fragments,
and Phase 1 requires every daily file read whole):

- `MacroBasis_State_YYYY-MM-DD.md` — last week's state file. `MacroBasis_State_2026-08-13.md` in this
  folder is the seed; after that, each run writes the next one.
- The window's daily files, `YYYY-MM-DD_News.md`, one per day.
- *Optional:* last week's dashboard `.docx`, as voice and register ground truth.

Typical load: ~34,000 words of dailies for a seven-day window, about 45,000 tokens. With the static
knowledge that is roughly 73,000 tokens before any searching, which leaves comfortable headroom.

**2. Say:** `Run the weekly cycle for YYYY-MM-DD`

**3. The agent stops once**, at the Phase 4 triage gate, and asks you to confirm or correct the
triage before it drafts. Say "run straight through" up front if you do not want the pause.

**4. You get back two documents:**

- `MacroBasis_Content_YYYY-MM-DD.md` — the full report content in block order, every field labelled
  to match the template's cells, every budgeted field carrying its own word count, plus four
  appendices: the Week Ledger, the Indicator Panel, the confirmed triage table, and the self-audit
  with the run manifest.
- `MacroBasis_State_YYYY-MM-DD.md` — next week's state file. **Save it.** It is the only memory the
  next run has.

**5. Format it.** Paste block by block into the template, insert your charts into the named slots,
shade the named quadrant, render the dot strips and the residency bar chart from the tables the agent
hands over, then check every block still fits on its page in Word.

---

## The state file is the whole design

In repo mode, prior state comes from two places: last week's dashboard at the top level of
`Weekly Reports/` (statuses, prior anchors, watch items) and the newest `engine/content_*.json` (the
light history, the since-AIP verdicts, the regime signs, the quadrant residency, the illiquids
reads). In a Project neither exists, and the histories are **not recoverable from the .docx** because
they render as images.

So the state file carries all of it, in one markdown document the agent rewrites every run. It has
eleven sections: run state, statuses and one-liners, prior anchors by theme, the twenty-one
pre-registered watch items, the light history, the since-AIP evolution entries, the regime signs and
quadrant residency, the illiquids reads, the central bank table, the open threads, and the carried
divergences.

**A number dropped from the state file is a number next week cannot anchor against.** That is the
single failure mode of this setup, and it is worth a glance each week before you file the state file
away.

---

## Keeping this folder honest

These files restate rules that also live in the repo specs. Nothing enforces that automatically
except one check: `engine/check_specs.py` verifies that the word budgets and canonical enums inlined
in `MacroBasis_Content_Spec.md` section 1 still match `_canonical` in `engine/content_schema.json`.
When a budget or an enum changes in the schema, that check fails until this folder is updated too.

Everything else is manual. When a rule changes in `MacroBasis_Weekly_Run_Prompt.md`, grep this folder
for every restatement of it and update or delete each one. The Content Spec's header says it plainly:
where it and the Run Prompt disagree on content, the Run Prompt wins and this folder is stale.
