# knowledge/ — Owning spec

Router entry: `CLAUDE.md` → "Knowledge base (H1 2026 defining events)" → this file. Full background and the build plan live in `MacroBasis_Knowledge_Base_Plan.md` (root); this file is the operative spec going forward, per the router principle in `CLAUDE.md`.

## What this is

`events_2026H1.md` is a repo-resident record of the defining events that shaped each of the agent's six themes, the Monetary Policy appendix and the Illiquids page, across 1 January to 30 June 2026. It exists for three uses, in priority order: (1) letting weekly sweeps and triage reference a new finding as advancing a known prior thread, the same way triage already carries a Provenance column; (2) fast, near-zero-token synthesis of "what defined this theme" without re-running research; (3) an optional future extension to keep the base current past H1 2026 (§4 below), off by default.

**Why H1 2026 specifically, and not earlier:** the repo's own memory (content JSON, light history, approved dashboards) only reaches back to 18 June 2026; `archive/` moved to OneDrive at the 12 Aug 2026 migration and is not reachable from here. Everything before 18 June in this file was reconstructed by dedicated research sweeps, not extracted from repo records. Treat it with the same source-tier discipline as anything else the agent writes, not as ground truth by virtue of being pre-built.

## Format

One Markdown file, nine sections in this fixed order: Regime timeline, then the six themes (Fiscal & Deregulation, Currency Debasement, Energy & Transition, Artificial Intelligence, Geopolitics & Trade, Domestic Investing), then Monetary Policy, then Illiquids. No parallel JSON index; the Markdown block structure below is the only machine-parseable form and is kept strict so it stays that way.

Each entry:

```
### KB-<CODE>-<NNN> — YYYY-MM-DD — Headline
- **Theme:** <canonical theme name, plus "(also: ...)" if cross-theme>
- **Driver:** <Charter driver name verbatim, or "narrative">
- **What happened:** dated, tier-labelled, 2-3 sentences.
- **Why it mattered:** the mechanism, glossed for a generalist reader.
- **Implication:** the investment implication as it stood at the time (never with hindsight).
- **Status effect:** Escalating/Held/Deescalating if it moved a light at the time; omitted if not applicable.
- **Sources:** Tier-labelled, dated.
- **Thread:** → other KB IDs or weekly report dates, where a real lineage exists. Optional; omit rather than force one.
```

Codes: `REG` (regime timeline), `FIS`, `CUR`, `ENE`, `AI`, `GEO`, `DOM`, `MON`, `ILL`. IDs are chronological within their section and **immutable once assigned** — never renumbered. Retiring an entry means adding a one-line tombstone under its existing ID, not deleting or reusing the number.

Canonical theme names, status words and driver names come from `engine/content_schema.json`'s `_canonical` block and `MacroBasis_Theme_Charter.md`, exactly as the weekly pipeline uses them. Voice matches the weekly report (Phase 6 of the Run Prompt): British/Canadian spelling, no em-dashes in entry prose, no standalone unlabelled numbers, acronyms expanded on first use, mechanisms glossed. This is deliberate: it means an entry can be lifted straight into a synthesis brief or continuity phrasing without rewriting.

**The recency gate does not apply to this file.** Every other spec's recency gate exists to keep the weekly report current; this file is historical by design. Source-tier policy is unchanged: Tier 1 preferred, Tier 2 usable per the normal corroboration rule, Tier 3 must be converted or dropped. A beat that could not source something to the required tier says so as a named gap rather than guessing; several genuinely do, in `runs/kb-build-2026-08-20/manifest.md`.

**Selection bar** (an event needs at least one to earn an entry): it materially moved a theme's thesis or status at the time; it is a thread head later developments visibly built on; or it explains an anchor or baseline the weekly report still carries. Caps are 6 to 10 entries per section, hard cap 12, to keep this a spine rather than a chronicle; the Regime timeline section is capped at 8 (it landed at 6) because its job is cross-theme synthesis, not primary sourcing, so most of its entries thread to a fuller entry elsewhere rather than duplicating it.

## How the weekly pipeline uses this (triage-style referencing)

This is additive to the Run Prompt, not a new gate:
- **Phase 2 (sweeps):** each theme beat's dispatch may include its own KB section (that section only, never the whole file) as context, so a beat can recognise when a new finding advances a known thread and name the ID.
- **Phase 4 (triage):** a `KB thread` column is the backward-looking analogue of the existing Provenance column. Provenance says where this week's finding came from; KB thread says which prior defining event it builds on. An ID or an em dash, same convention as Provenance.
- **Content JSON:** an optional per-theme `kb_refs` array may list IDs a week's developments advanced. The fill engine ignores this field; it carries zero layout or template risk.
- **What never changes:** layout, block order, the lights system, prior-anchor discipline, the recency gate for weekly developments, or anything in the engine, template or `check_layout` gate. This file is context sitting beside the pipeline, not a new stage inside it.

## Synthesis on demand

To ask for a brief built only from this file, no web research, no sweeps: **"Synthesize the defining events for [theme(s) / period]."** This reads `events_2026H1.md` (and `events_2026H2.md` once §4 below is switched on) and returns a dated brief in report voice. Default output is Markdown, handed back in chat or written to `runs/`; only build a `.docx` if asked, and build it as a plain document, never through `engine/macrobasis_fill.py`, which stays dashboard-only. This is meant to be the cheapest possible operation the agent offers: the whole point of the file existing is that a materials request costs a file read, not a research pass.

## §4 — Extending past H1 2026 (designed now, OFF by default)

Not built in the 20 Aug 2026 run. To switch it on, add a gated Phase 0 step, "KB maintenance," to the Run Prompt: each week, after the dashboard is approved, check it against the promotion rule below; a matching event gets a new entry in `events_2026H2.md` (create the file the first time this fires), same format and ID scheme as this file, IDs continuing from where a section left off if the theme already appears here, or starting fresh with `KB-<CODE>-001` for a section that does not yet exist.

**Promotion rule:** at most one entry per theme per week, and only if the event did at least one of: flip a status light, move the quadrant, or get flagged by Eduardo directly. Until this gate is turned on, weekly runs only read this file; they never write to it.

## Calibration

Eduardo's hand edits to any KB entry are calibration data, the same as anywhere else in this project (`CLAUDE.md`, invariant 7): a correction here means the underlying research or framing was off and should inform how future beats are briefed, not just a one-off fix.
