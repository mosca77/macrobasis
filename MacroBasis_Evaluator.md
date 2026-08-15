# MacroBasis Evaluator (Phase 7 — run every week, after drafting, before the file; v2, 6 Jul 2026)

> Last synced against Run Prompt v5.6 (13 Aug 2026). When a Run Prompt rule changes, this file gets a sync pass the same day — format rules here are POINTERS to the Run Prompt's current standard, never an independent copy.

The evaluator is a second, adversarial pass over the drafted content. Its job, in order: (1) the north-star read, (2) score each theme's light with an explicit framework, (3) check the sweep actually caught the week's market developments, (4) reconcile the report against what the daily monitor flagged, (5) check the data, (6) check the writing reads like a human macro/outlook report, (7) check the references. Fix what fails, then produce the file.

## 1. North star — the minimal-edits read

The report succeeds when Eduardo files it with minimal hand edits. Read the full draft once as he would, asking:
- **Is it the week's story, well rounded?** Beginning (where last week left off), middle (what happened and how the market read it), end (where the themes stand, what to watch). Exec and theme blocks tell ONE coherent week — the Weekly Direction, the woven status reads, and each theme's Key Development row must not disagree with each other (the exec Key Developments page is retired; this check applies to the per-theme rows).
- **Is anything missing** that the week's daily files or the tape said mattered? (Section 4 makes this mechanical.)
- **Is anything included** that fails the relevance test — an item that says nothing about regime direction, theme outlook, the market's story, or an actionable implication?
- **Would his hand pass change the words?** Check against the voice rules (Run Prompt, Phase 6) — his past edits are the calibration set: facts-first openers, no kickers, one layer of data, measured verbs, glossed jargon, exposures not advice.
Anything that fails becomes a fix, not a footnote.

## 2. Status framework (Escalating / Held / Deescalating)

Score each theme from its triaged in-window findings:
- Each finding gets a **direction** on the theme's more/less axis (+1 more of the theme, −1 less, 0 mixed/neutral) and a **materiality weight** (high = 3, medium = 2, low = 1).
- **Net score = Σ(direction × weight).**
- 🟢 **Escalating**: net ≥ +3 AND at least one high-materiality supporting finding.
- 🔴 **Deescalating**: net ≤ −3 AND at least one high-materiality opposing finding.
- 🟡 **Held**: everything else, including the **contradiction rule**: if both directions carry a high-materiality finding in the same week, the light is Held and the Status line names the tension.
- The Status line must name the deciding signal(s). No light moves on low-materiality findings alone.
- **Market confirmation:** where a theme has tradeable gauges (Indicator Panel, section C), a 🟢 or 🔴 needs at least one market-price confirmation alongside the news (e.g., more debasement = gold up AND the dollar's prop weakening, not a headline alone). News without tape = Held unless the market simply has no instrument for it.
- **Tape veto (since 3 Jul 2026, the stronger form):** confirmation is necessary but not sufficient — if the tradeable tape moved materially AGAINST the theme in-window, the light caps at 🟡 Held **no matter how big the supporting news**, and the Status line carries both sides. The score sheet must show the contradicting tape finding at high materiality, not bury it at low weight.
- **Weekly Direction conservatism (since 3 Jul 2026):** the same logic governs the growth/inflation words. Claim "slower"/"faster" only on unambiguous cross-asset evidence; a stall-not-break labour read plus a positive GDP surprise = "**held** growth", not "slower".
- **Human override:** Eduardo's read wins. When he re-scores a light, adopt it, keep the exec dashboard consistent with it, and record the override here as a calibration point for future scoring. Calibration log:
  - 2 Jul — Currency Debasement Held→**Escalating**: gold reclaiming $4,000 plus the dollar slipping read as more debasement, not mixed.
  - 3 Jul — AI **Escalating→Held** (tape veto): Korea ~$880B + DRAM +89% vs the SOX sliding on oversupply concerns and half-year liquidations; the market's reception of the news decides.
  - 3 Jul — Weekly Direction growth call **slower→held**: jobs argued stall-not-break, April GDP surprised up.
  - 17 Jul — Fiscal **Escalating→Held**: a $95B framework advanced and dereg moved, but the NDAA stalled and market confirmation was mixed; "execution and financing limit the weekly acceleration". Delivery, not announcement, moves the light. (24 Jul: the House passing the stack + record prime backlogs = delivery, so Escalating returned.)
  - 17 Jul — Currency **Held→Deescalating**: the reserve share RISING (57.13%), strong indirect Treasury demand and gold falling through a war week outweighed the official-sector gold bid; a week that argues against the theme can go red even with the structural bid intact.
  - 17 Jul — Energy **Held→Escalating**: the PJM record-price-but-short auction + FERC computational-load order + Hormuz lifting oil/LNG read as scarcity visible in BOTH the physical grid and traded energy; policy/physical proof can carry the light when the clean-energy tape is quiet.
  - 17 Jul — Domestic **Held→Escalating**: named contracts (GDLS, TKMS) = "programme design toward deployment"; concrete deployment outweighs silent steering machinery.
  - 17 Jul — Weekly Direction **cooling→firming inflation, held→moderating growth**: Eduardo weighted the FORWARD oil re-shock over the backward CPI print, and the BoC growth cut + China miss over US labour. Market-implied direction outranks the spot prints when they disagree.
  - 17 Jul — Exec Key Developments: inline source parentheticals REMOVED (the citation ban now covers the exec rows; References carry all sourcing).
  - 17 Jul — Process: the sweep-skipped straight render forced heavy hand additions (Treasury MTS, auction internals, COFER detail, PJM, TKMS, Gordie Howe). The full sweep is the default; dailies alone are not a report.
- **Regression rule (v2):** when any scoring or voice rule changes, re-score every calibration-log entry under the proposed rule BEFORE adopting it. If a logged human override flips, the change is miscalibrated — fix the change, not the log.

**Status line format (theme blocks, 9 Jul 2026 standard):** engine-inserted Status Ball oval (same shape as the dashboard lights — never a typed ●) + word + reason, with the macro read WOVEN IN as a clause — **never a literal "Macro take:" label** (the engine strips one if present):
`Escalating ▸ <what decided it, with the data>; <the read as a clause tying the week to growth / inflation / policy pricing>.`
The woven read names the **concrete driver** ("growth picked up mostly from commodities, policy unchanged"), not an aphorism ("growth less bad"), and may be dropped when the reason sentence already carries the read. When the tape veto fired, the reason names both sides ("…, but markets see concern of oversupply and liquidated positions").
**Monetary Tracker exception (3 Jul):** its status line has NO light and NO status word — it starts at the deciding sentence.

## 3. Sweep-completeness checks (did we catch everything?)

Run all seven; any miss goes back through triage:
1. **Indicator-matrix audit.** Confirm the FULL Weekly Panel was pulled, bucket by bucket, against the §A table of `MacroBasis_Indicator_Panel.md` (the Panel owns the list; never audit from a remembered copy). Any bucket not checked = the sweep is incomplete. Then audit claim coverage against the thresholds THIS file owns: the Weekly Direction carries ≥3 confirming indicators from ≥2 asset classes **per axis**; every Escalating/Deescalating light has at least one market-price confirmation where the theme is tradeable; market-implied direction (breakevens) is distinguished from spot level (CPI/PCE) wherever they disagree.
2. **Divergence review.** Walk the panel indicator by indicator: anything that moved AGAINST the report's narrative must be either explained in the text (e.g., "JOLTS at a two-year high argues stall, not break") or triaged as an open question. An unexplained divergence is a failed check, and a persistent one (two-plus weeks) must be surfaced to the reader.
3. **Calendar check.** Reconstruct the week's scheduled calendar (last week's Watch lists + standard releases: payrolls/JOLTS/claims, PMIs incl. RatingDog and Tankan-type surveys, CPI/PCE prints, central-bank meetings and speeches, auctions, OPEC+, summits, reviews). Each item is either reported or explicitly checked-null. Do not let a Watch item from last week vanish.
4. **Reaction-function check.** For each top development, confirm the other side is covered: the release AND the market reaction AND the policy read (e.g., payrolls → yields, dollar, gold, Fed pricing).
5. **Front-page test.** Run 2-3 generic recap queries ("markets this week", "week recap <date>", regional variants). Any story appearing in two or more recaps that is absent from triage is a miss.
6. **Conflict-legs check (3 Jul).** Both standing war legs — US-Iran AND Russia-Ukraine — were searched by name up to filing time, each has its own read in the Geopolitics status, and defence-budget-relevant escalation also surfaced in Fiscal. The 2 Jul run missing the Kyiv attack is the calibration miss: a leg with no line in the report needs an explicit checked-null.
7. **Late-breaking check (v2).** The daily files end at ~9:00 AM; confirm the hours between the last daily file and filing were swept (front-page recap + both conflict legs at minimum). Filing-day news the dailies could not have caught is the residual blind spot.

## 4. Daily-coverage reconciliation (v2 — the monitor is a contract)

The week's daily files are commitments, not suggestions. The confirmed triage record is `runs/YYYY-MM-DD/triage.md` — diff against it, not against memory of the chat. Walk the daily files one by one:
1. **Candidates:** every item flagged as a "Likely report candidate" in ANY in-window daily file appears in the report or on an explicit triage discard line with a reason ("no follow-through", "failed verification", "superseded by X"). A silently missing candidate is a fail.
2. **Persistent stories:** any story the Weekly Signal blocks tracked on 3+ days that is absent from the report is a fail unless its discard reason is explicit and convincing.
3. **Temperature cross-check:** a theme the dailies marked "Developing" all week that lands with a null body or an unexplained Held gets re-examined — either the dailies over-flagged (say so in triage) or the report under-tells it (fix the body).
4. **Raw-log spot check:** pick the 2 biggest "Top of the tape" items from each daily file; confirm each is in the report, in triage as discarded, or checked-null. Nothing the monitor caught is silently dropped.

## 5. Data check

- Re-trace the **five most load-bearing numbers** of the draft to their primary source (or two independent outlets) before the file is produced.
- Re-trace every **panel level** quoted in the report (yields, breakevens, spreads, FX, commodity prices, VIX) to a data page (FRED, Trading Economics, exchange/index pages), each with its as-of date; intraday vs close vs futures labelled.
- **No standalone numbers.** Every figure carries context: prior/anchor, expectation where one exists, and the trend (e.g., not "ISM 53.3" but "ISM 53.3, down from 54.0 and below the 54 expected, a sixth month of expansion"). A number without context fails review.
- Where sources disagree (spot vs futures, intraday vs close), report the range or the conservative figure and say which is which; never silently pick the flattering print.
- Generated keydev charts: every underlying value re-checked against its source; the chart footnote states exactly what was plotted and where it came from.

## 6. Style check (macro/outlook voice)

Each section must read like a human macro strategist telling the week's story:
- **Story arc**: what happened → the data → why it matters → what to watch. Not a list of facts.
- **Relevance test, item by item**: does this development tell me something about the direction of (a) the regime (growth/inflation/policy), (b) the theme's outlook, (c) the story the markets are telling, or (d) an actionable implication? Anything that answers none of the four gets cut. Standalone information is not valuable.
- **Connection test**: every kept development is anchored in last week's state ("markets were priced for X") and shown against the market's reaction ("the dollar slid, gold repriced, the 2-year fell; they all showcase the same repricing"). News and market move must appear in the same thread, not in separate bullets.
- Short sentences. Data woven into sentences, not bracketed lists. Brief where possible without losing the story.
- **Facts-first paragraph check (3 Jul):** no paragraph opens with a scene-setting or framing line ("Ankara is the next test.", "Oil finished the round trip and kept going."); no paragraph closes on an aphoristic kicker ("Fragmentation is broadening, not fading."). Open at the fact; end on the plain read. Plain connectives ("The thing to note is:"), not clever ones ("The caveat matters:").
- **Trim check (3 Jul):** one layer of supporting data per point — second-order breakdowns (survey sub-indices, named sub-programmes, bank level targets) are cut once the headline point stands. Themes run ~3–5 body paragraphs. Null items ("crypto stayed out of the trade") are cut from the body; they live in triage as checked-null.
- **Dedupe check (3 Jul):** no market move narrated fully in two themes. It is told once in its owning theme; elsewhere one back-referencing clause. A retold Fed-repricing paragraph in Currency is a fail.
- **Keydev prefix check (3 Jul):** no keydev note starts with "Key development:" — the row label says it.
- **No inline source citations in body text**: no "(Bloomberg.)" parentheticals anywhere; the by-topic References carry all sourcing. Measured verbs over drama; **jargon glossed at first use in EVERY block, not only the first theme**; keydev notes short (headline call + read).
- No em-dashes or double dashes in prose. No AI-voice filler (crucially, notably, moreover, "Net:"). Fiscal-year ranges hyphenated ("2023-24", never "2023/24"); levels quote their prior ("4.11% from 4.18%").
- Every theme lands on an investment read that spells the growth/inflation sign and the offsets; exposures named, no trade construction ("moved from beta to execution risk" was cut). The exec lands on the growth/inflation call.
- **Exec cell check (6 Aug 2026 standard):** Weekly Direction is one sentence, bold direction words; Influencing Factors are 4 to 6 lines that fill the cell (~14-18 words each) with no offset line; dashboard one-liners may close on a short interpretive read of the theme's direction (the schema sanctions this — it is distinct from the BANNED aphoristic kickers in body prose) and name specific conflict legs.
- Read the Weekly Direction and each Status macro take together: they must tell one coherent week.

## 7. References check (by topic)

References mirror the document: one group per section, with the exact topic labels owned by `_canonical.reference_topics` in `engine/content_schema.json` (Executive Summary, Theme 1, Monetary Policy Tracker, Themes 2-6, and Illiquid Assets — Private Markets), each item carrying its tier in parentheses, covering where each section's data actually came from. A section whose numbers cannot be matched to its reference group fails.
