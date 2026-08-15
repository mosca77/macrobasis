# Spec-consistency audit register — 13 Aug 2026

Standing input for the cleanup Eduardo will commission ("extensively fix these issues, keep the agent's quality"). Produced by six verified audit agents; full evidence with both-sides quotes in the session artifact ("MacroBasis Drift Audit"). This file is the repo-resident copy so ANY session can execute the fix phases without the original conversation. Corpus as of commit 13115cd.

**Prime directive for the fixing session:** the agent's quality lives in the single owning copy of each rule (calibration log, voice rules, gates, tape veto, checked-nulls, beats, chart insertion, auto-merge). Fixes DELETE duplicate/stale restatements and align stale text to the current contract; they never weaken, reword, or remove the owning rule itself. When in doubt which copy is the owning one: the newest dated standard wins, ground truth = Eduardo's approved dashboards.

## Findings by root cause (43 confirmed; severity = risk of a wrong report this cycle)

### A · Amend-by-append (dated notes stacked, superseded text never deleted)
1. HIGH — Run Prompt v5.4 banner (:9) still mandates Buy/Hold/Sell Illiquids; body (:156, :230) retired it. Fix banner.
2. HIGH — Influencing Factors ~14-18 words (:132) vs ~12-15 (:134) in the same Block B. Keep 14-18 (schema :81, :366 agree, load-tested).
3. HIGH — Phase 8 render check (:248) inspects retired dated marker + exec Key Dev rows (:129, :131). Rewrite to: highlighted quadrant, six rows, ovals.
4. MED — "Version: v5.2" line (:26) inside the v5.6 doc. Move to changelog.
5. MED — Outputs line (:23) lists retired keydev PNGs (vs :142, :244). Replace with light_history/quadrant_history PNGs.
6. MED — Reviewer checklist (:265, :268): "nudge the quadrant marker", "review generated keydev charts" — both retired. Replace with quadrant-shade check + ChartsThemes resolution check.
7. MED — Illiquids budgets 180/75 (schema :244) vs 160/65 (schema :437). Newer (13 Aug measured) wins; update :244.
8. LOW — "3-4 bullets" (:130) vs "4 bullets" (:134) rationale. Keep 3-4.
9. LOW — Theme text budget "420-500 words with the 17 Jul sizes" (:139) stale two re-measurements later. Re-estimate for 07-Aug-measured slots or point at schema.

### B · Lagging companion specs
10. HIGH — Evaluator :39-40 status-line template carries the banned literal "Macro take:" label (Run Prompt :137 bans it, 9 Jul). Rewrite to woven-clause form.
11. HIGH — Evaluator :85 enforces "exactly 3" Influencing Factors (retired 6 Aug, Run Prompt :132). Update to 4-6 filling the cell.
12. HIGH — HANDOFF.md: archive/ listed as available (:35, retired per CLAUDE.md :21/:53); stale "state as of 11 Aug" (:37-42, wrong current dashboards); references a .pptx deck and Interim Review doc that do not exist (:28, :42). Rewrite state section as "read the newest files", drop dead references.
13. MED — Evaluator :85 permits one-liner "kickers"; voice rules ban kickers (Run Prompt :194, :222). Remove allowance (or Eduardo carves an explicit exception).
14. MED — Theme Charter :233 routes risk deltas through the retired exec "Key Developments | Implication" rows; version line :2 says "June 2026 (rev. 2)" despite Aug content. Point risk deltas at theme narratives + Light Scoring; refresh version line.
15. MED — memory/glossary.md missing post-Jul terms (Illiquids grid categories, ChartsThemes, quadrant highlight, regime signs); baseline-mode row (:19) says "attached". Add entries, fix wording.
16. LOW — Evaluator §7 (:88-90) references-group list omits Illiquid Assets; §1 (:8) "Key Developments" phrasing ambiguous vs the retired exec block. Add group; disambiguate to per-theme keydev.

### C · Migration residue (12-13 Aug GitHub move)
17. HIGH — "attached / folder connected" workflow language: Run Prompt :22 (preconditions) and :261 ("attach that file on the next Execute"); HANDOFF :20; glossary :19; memory/projects/macroagent.md :48. All → repo-read language per CLAUDE.md.
18. HIGH — Daily-file structural drift: only 2026-08-13 matches README v2's mandated template ("keep exactly this structure", README :45-96); 07-12 Aug files used ad hoc structures (bridge-offline era) and defaulted NEW/CARRIED tags to NEW. Forward-fixed; add a Phase 1 note that pre-13-Aug tags/day-counts are unreliable — recompute from cross-file presence.
19. MED — CLAUDE.md :25 dates the GitHub-native daily "since 12 Aug"; first conforming self-committed file is 13 Aug. Correct the date.
20. MED — runs/2026-08-12/ orphan: ledger + two beat-log files, no panel/triage/self_audit; runs/README.md has no aborted-run convention. Delete the dir (superseded per runs/2026-08-13/ledger.md) AND add an aborted-run rule to runs/README.md.
21. LOW — Orphan root files: "Agent title" (stray, delete) and TASKS.md (frozen 18 Jun, superseded by runs/ — delete or declare in CLAUDE.md file map).
22. LOW — Unstated conventions: approved-dashboard filename date may differ from the generated file it approves (08-06 vs 08-07) — document in Run Prompt file conventions; daily README hardcodes "9:00 AM" vs actual 9:15-11:30 compiles — make the template line a variable timestamp.

### D · Canonical enums that aren't
23. HIGH — Illiquids block named four ways: schema block_order :24 ("…Private Markets Read", dead key — nothing reads it), reference_topics :40, title default :226 ("Illiquid Assets"), shipped title "Allocation Insights - Illiquid Assets" (content_2026-08-13.json, Eduardo's approved rename, undocumented in Run Prompt :152 / Format Spec). Adopt the approved title as canonical everywhere; delete or fix block_order.
24. MED — Schema example :301 "Energy & the Clean Transition" contradicts canonical :36/:63 "Energy & the Energy Transition". Fix example.
25. LOW — Legacy keys inconsistently documented: cross_theme/key_risks honoured by engine (macrobasis_fill.py :2241-2245) but absent from schema notes; 4 other documented backward-compat fields accumulate. Document or drop.

### E · Code contracts vs code (incl. the one functional landmine)
26. HIGH (LANDMINE) — build_template_from_dashboard.py (v2, 23 Jul) only matches tables whose header starts with "Theme" (:320-321) and never tokenises the Illiquids block: run on any post-6-Aug approved dashboard it bakes that week's literal Illiquids text + charts into the template. FIX BEFORE THE NEXT TEMPLATE REBUILD; until then template rebuilds are manual-review-required.
27. MED — Format Spec :137-143 states check_illiquids BACKWARDS (code warns when a read IS buy/hold/sell, fill.py :1827-1829) and claims a check_layout "call and portfolio read" assertion that does not exist (:90-101 checks grid categories). Rewrite both passages.
28. MED — fill.py Usage docstring (:42-48) documents [prev.docx] transplant as the normal path; retired behind quadrant_transplant (:20-21, :2124). Mark legacy.
29. MED — Format Spec presents keydev chart generation (:235-239, :293-298 vs "retired" :108-109) and exec Key Dev rows (:224-226, :262) as current. Add retired-by-default caveats.
30. LOW — check_layout.py docstring (:12) still says Buy/Hold/Sell; header v3 (:2) vs v4 comments. Update.
31. LOW — fit_pages.py premise predates 13-Aug chart insertion (:5-6); also trims margins the spec's "do not change" table (:251-256) declares fixed. State its post-insertion status (fallback for hand-edits only) + annotate the margins exception.
32. LOW — Format Spec Block & Chart Map (:285-291) stale slot names (energy1.png, AI_vs_snp500…). Refresh to canonical `<base>_<n>`.

### F · Numbering collisions
33. MED — "Beat 10" orphan: Run Prompt :9 "eighth beat" vs :72 "Beat 10"; beats 1-9 enumerated only in the DAILY protocol (README :19-28). Name beats, drop the number.
34. LOW — Three unrelated "v4"s (engine v4.x, Illiquids "v4 settled", check_layout v4 schema). Reserve vN for engine+Format-Spec; page formats get dated names.

## Fix phases (execute in order; each phase = one commit through the v5.6 finish)
- **Phase A — mechanical (one commit):** items 1-9, 16, 19, 21-22, 24-25, 28, 30, 32, 34 + glossary adds (15). Deletions and one-line alignments only; zero behaviour change. Verify: grep for "Buy / Hold / Sell", "Macro take:", "attached", "12-15 words" afterwards.
- **Phase B — companion-doc passes:** items 10-14, 16-17 (Evaluator, Charter, HANDOFF rewritten against Run Prompt v5.6; sync stamps added: "last synced against Run Prompt vX.Y").
- **Phase C — structure:** contract/changelog split of Run Prompt + Format Spec (dated banners move to a non-operative changelog zone); extend schema `_canonical` with display titles + word budgets (23, 7, 2); write engine/check_specs.py (version stamps agree; canonical strings match; banned phrases outside changelog zones; daily files match README skeleton; runs/ dirs complete-or-marked) and wire it into Phase 8 + both Routine prompts; items 18, 20, 33.
- **Phase D — the landmine:** item 26 — teach build_template_from_dashboard.py the Illiquids block (chart cells → Insert illiquid_1/2 tokens; grid cells → placeholder tokens), test by rebuilding a template from the approved 08-07 dashboard and diffing against v6.

**Regression guard (applies to every phase):** after fixing, re-run the Evaluator's regression rule in spirit — no calibration-log entry, voice rule, gate, or canonical enum may change meaning; check_layout.py must still pass on a rebuild of the 2026-08-13 dashboard from its unchanged content JSON.

---

## Execution log (13-14 Aug 2026)

All four phases executed and committed: Phase A (mechanical, incl. under-assigned items 27/29/31 folded in), Phase B (companion docs + attach purge + sync stamps; the Evaluator's one-liner "kicker" allowance was DISAMBIGUATED rather than deleted because the schema sanctions it — prime-directive call), Phase C (contract/changelog split, _canonical display title + budgets, engine/check_specs.py wired into Phase 8 and both Routines, aborted-run rule, beats named, runs/2026-08-12 removed), Phase D (Illiquids drop-list fix PROVEN — no Brookfield/KKR text leaks into a rebuilt template — plus hRule=atLeast restore on ingest).

**Residual item (pre-existing, out of register scope):** a template rebuilt from a v6-era approved dashboard still produces a taller exec (status rows can fall to page 2). Documented in the Format Spec with a MANDATORY rebuild acceptance test (fill + check_layout exit 0 before adoption); hand-tune the exec geometry on the next real rebuild, as was done for v6 itself. Every gate protecting production passes: check_specs 0 failures, and the 2026-08-13 dashboard rebuilt from its unchanged content JSON against the CURRENT v6 template passes check_layout with 0 failures.
