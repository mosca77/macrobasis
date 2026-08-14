# MacroBasis DOCX Format Spec — exact-match contract (v4.2, 13 Aug 2026)

> **How versions work here:** the number in this title = the newest "Engine vX.Y"
> changelog section below (the engine and this contract move together; the same
> number is stamped in `macrobasis_fill.py`'s docstring). It is NOT the template's
> version — the template is the newest `MacroBasis_Report_Template_v*.docx` at the
> repo root (currently **v6**) — and NOT the Run Prompt's (v5.x) or the Illiquids
> page format's ("v4 settled", 6 Aug 2026) numbering, which are independent tracks.

**Goal:** every weekly dashboard must be a byte-faithful match of the **current
report template — the newest `MacroBasis_Report_Template*.docx` in the folder root**
(layout, fonts, colours, spacing, table sizes, chart positions). The ONLY way to
guarantee this is to **fill the template**, never to rebuild it from scratch. This
folder's `macrobasis_fill.py` does exactly that.

Template lineage: the plain `MacroBasis_Report_Template.docx` filename is retired
(6 Jul 2026) — use the newest `MacroBasis_Report_Template*` file. **Current:
`MacroBasis_Report_Template_v6.docx`, built 30 Jul 2026 from Eduardo's approved
30 Jul dashboard** (inline three-column exec, one page per section, 14 chart
slots; supersedes v5, which was built 23 Jul from the approved 17 Jul dashboard:
Jun-30 reference quadrant, two-page exec, charts beside bulleted 'What changed',
full-width text keydev, Implication | Watch side by side, 7-row central-bank
table, no Monetary keydev) with
`engine/build_template_from_dashboard.py` (v2) — run that script
against the newest approved dashboard whenever his structural hand edits should
become the template (it re-inserts every placeholder token, restores Insert
markers and any keydev/implication/watch rows a hand edit removed, resets the
status ovals to the engine's base colour, and re-stamps YYYY_MM_DD). His newest
approved dashboard (`Dashboards_Eduardo_Updated/`) stays the formatting ground truth.

Engine v3.3 (6 Jul 2026): missing cells warn-and-skip instead of crashing; drawing
ids are seeded past existing ids (duplicate ids made renderers drop the whole
quadrant layer); marker labels handle split runs. **Layout caveat:** the quadrant
cluster is anchored below the Influencing Factors cell — if the factors run long,
the cluster slides off page 1. The factor-count budget (4-6 lines since 6 Aug 2026; was exactly 3) is what keeps the
exec block on one page; treat it as layout-critical, not just voice.

Engine v3.4 (9 Jul 2026, Eduardo's hand-edit feedback folded in):
- **Status line = plain 10pt BLACK body text.** `fill_status_line` now forces every
  text run in a theme Status line to sz 20 / colour 000000 / not-bold, overriding the
  template placeholder run (which carried sz 30 green 92D050 and rendered a "big green"
  status word). Only the Status Ball oval carries colour — matching Eduardo's approved
  07-03 lines. The `tblLayout`/`tblCellMar` order in the keydev nested table was also
  fixed so output validates.
- **"Macro take:" label stripped.** The engine removes any literal "Macro take:" from the
  status text; the read is woven into the sentence as a clause.
- **Exec page-1 layout knobs** (content fields): `quadrant_scale` shrinks the whole floating
  quadrant cluster toward its top-left (uniform, markers stay aligned; 0.72 = smaller/cleaner);
  `quadrant_shift_up_emu` lifts it; `quadrant_behind` sets behindDoc. Keep `influencing_factors`
  ~14 rendered lines and the six one-liners ~3 lines each or the nested status table orphans in
  LibreOffice (~8.4in of content fits a 10in page, so Word places all six status rows on page 1;
  the headless previewer shows ~5). `scale_exec_quadrant`, `shift_exec_quadrant`,
  `quadrant_behind_text`.
- **Two new engine-generated blocks after Theme 6** (before the Lights Guide Appendix), styled
  to match the theme blocks:
  - `build_light_scoring_block` (from `light_scoring`) — SPLIT INTO COLUMNS
    Theme | Light | Supports | Against | Net, so the grading reads cleanly.
  - `build_light_history_block` (from `light_history` + `light_history_png`) — embeds a
    matplotlib HEATMAP image (themes x all weeks, coloured cells) that scales to any number of
    weeks; falls back to a coloured word-matrix if no png.

Engine v3.5 (9 Jul 2026 — deterministic page schema + automated check):
- The template reserves FIXED row heights on exec R1 (4881 twips) and R2 (7095) and on each
  theme block's rows, which wasted space and pushed content off-page no matter how small the
  quadrant was. `set_exec_row_heights` (fields `exec_r1_height_twips`/`exec_r2_height_twips`)
  and `compact_block_rows` (`theme_row_min_twips`) reset these to 'at least N' so rows size to
  content and empty side-chart slots stop reserving space. `compact_block_rows` also tightens
  paragraph spacing and compacts nested tables (e.g. the Monetary central-bank table).
- `scale_exec_quadrant` shrinks the floating quadrant toward its top-left so it is no taller
  than the factors (0.5). Together these fit Weekly Direction + Influencing Factors + ALL 6
  status rows on page 1.
- Page schema forced with `set_pagebreak_before` (theme blocks) and `hard_break_para`
  (engine-generated Light blocks, where pageBreakBefore-in-table is not honoured), with the
  redundant inter-block spacer dropped so no near-blank spill page appears.
- **`engine/check_layout.py`** renders the docx and asserts the whole schema (6 status rows on
  p1, Key Developments p2, one theme per page, Light Scoring then Light History, no spill
  pages). MANDATORY after every build; must exit 0 before filing. This is the regression guard
  so the layout never silently breaks again.

Engine v4.0 (23 Jul 2026 — Eduardo's 17 Jul restructure folded in):
- **Jun-30 quadrant.** The template carries the AIP Jun 30th environment (map + black
  Jun 30 reference point + standing note box) and ONE dated marker. Each run
  `quadrant_relabel_and_move` renames that marker to this week's MM-DD and shifts it
  by `quadrant_marker.dx_emu/dy_emu` (displacement vs the prior week, both measured
  against the Jun 30 baseline; +x right = firmer inflation expectations, -y up =
  firmer growth). The 3-marker trail and prev-docx transplant are retired (legacy
  path via `quadrant_transplant: true`); the fill no longer needs a prev argument.
- **Exec pagination (24 Jul 2026).** Page 1 = Weekly Direction + bulleted
  Influencing Factors + full-size quadrant + ALL SIX status rows; the engine SPLITS
  the exec table at the Key Developments header into a second table preceded by a
  zero-height pageBreakBefore paragraph (in-table row breaks are unreliable in
  renderers), so the Key Developments always open page 2. `exec_r1_height_twips`
  (~5400) reserves the quadrant-cluster height in R1.
- **Theme geometry (from the v5 template).** Charts occupy a column beside the
  bulleted 'What changed' cell (side varies by theme); keydev = full-width text row
  (no nested chart table); Implication | Watch share the bottom row; chart cells
  carry `Insert <theme>_chart_N` markers for Eduardo's own charts. The Monetary
  appendix has NO keydev row and a 7-row central-bank table
  (| Central Bank | Key Policy Rate | Expected Cycle / Note |).
- **Page schema mechanics.** Each theme table is preceded by a zero-height
  `pageBreakBefore` paragraph (`break_before_para`) — in-table pageBreakBefore at a
  table START is honoured by Word but ignored by LibreOffice, and a literal `w:br`
  leaves a blank page when the prior block ends exactly at the boundary; the engine
  also strips template-carried pageBreakBefore from each table's first paragraph so
  the two mechanisms never double-break. `check_layout.py` (v2) asserts the new
  schema: p1 direction+factors+quadrant (no status rows), p2 all six status rows +
  Key Developments, one theme per page, Light Scoring then Light History, no spills.
- **Charts.** The only engine-generated image is the light-history heatmap
  (`engine/charts/YYYY-MM-DD/light_history.png`). Keydev chart generation is retired.
  Since 13 Aug 2026 the side-chart slots are filled with Eduardo's UPLOADED charts
  from `ChartsThemes/` at build time (see Engine v4.2 below); the agent still never
  generates or fabricates a side chart.

Engine v4.1 (6 Aug 2026 — Eduardo's Illiquids page):
- **`build_illiquids_block` (from `illiquids`)** — a new engine-generated bordered block
  inserted **after Theme 6 and before Light Scoring**, on its own page, built in the
  **theme block grammar**: 2 columns of 5519 twips, burgundy borders, the same bold
  `#7B2952` section labels. Rows are Header → Signals → [chart column | "What changed
  this week"] → full-width "Key Development of the Week" → "Implication for the theme" |
  "Watch next week". The chart cells carry `Insert illiquid_1` / `Insert illiquid_2` and
  are filled by `fill_chart_placeholders` exactly like a theme's.
- **v4 (6 Aug 2026, settled): the framework GRID replaces both the strip and the
  keydev / implication / watch rows.** Block layout: header → [chart column
  (`Insert illiquid_1/2`) | "What changed this week"] → a 2x2 grid of cells in
  canonical order (Performance | Valuations over Leverage | Dry powder,
  `ILLIQUID_CATEGORIES` / `_canonical.illiquid_categories`). "What changed" carries
  the window's most important PRIVATE EQUITY news from the beat's own Sonnet 5 sweep.
  Each grid cell: burgundy category label + one bold read line + theme-style bullets
  (evidence, implication, watch), filled from `illiquids.framework[].{category,read,points}`.
  Retired: Buy / Hold / Sell calls (v1-v2) and the one-word tone strip (v3);
  `_signal_strip_xml` and the palettes remain in the engine only for legacy renders,
  and `check_illiquids` warns if a content file still carries `signals`.
- **Block tables are centred on the page at build.** `centre_block_tables` gives every
  top-level table a `tblInd` that equalises the white space either side of the block,
  compensating for the template's asymmetric page margins (left 720 / right 284 twips)
  without touching the section setup. 6 Aug 2026, per Eduardo.
- **The block carries no light by design.** `check_illiquids` warns at build if an
  Illiquids row leaks into `light_scoring` or `light_history`, if the exec
  `status_dashboard` is not still six rows, if the grid categories drift from
  canonical order, or **if a cell's read IS one of the retired Buy / Hold / Sell
  words** (it prompts for a descriptive direction instead).
- `_gen_prefixes` now includes `"Illiquid Assets"` so the block gets its own hard page
  break like the other generated blocks, and `check_layout.py` (v4) asserts the block
  exists, occupies exactly one page, carries "What changed this week" plus all four
  grid category labels and no status word, sits directly
  after the last theme page, and is directly followed by Light Scoring.

Engine v4.2 (13 Aug 2026 — real chart insertion from `ChartsThemes/`):
- **Eduardo's charts are now placed INTO the report at build time.** He uploads the
  week's theme charts to `ChartsThemes/` at the repo root; `fill_chart_placeholders`
  fills every `Insert <slot>` cell with the REAL chart when one resolves, and only
  falls back to the 30 Jul dashed placeholder (marker line kept) when none does.
- **Resolution.** `index_chart_dir` scans the source dir once (`chart_source_dir`
  key, default `ChartsThemes`); `resolve_chart_image` maps slot → file tolerantly:
  case, separators and doubled `.png.png` are ignored, and the alias table accepts
  the upload spellings (`Currency_debasement_2` → `currency_2`,
  `artficial_intelligence1` → `AI_1`, `Geopolitics_2` → `geo_2`, `Illiquids_1` →
  `illiquid_1`, `energy1` → `energy_1`). Files named `retired*` and zero-byte files
  are skipped. Per-slot explicit overrides via the `chart_images` content key win.
- **Formatting is preserved by construction.** The source image is letterboxed onto
  a white canvas of EXACTLY the slot's measured geometry (`chart_slots`, aspect
  kept, centred, 150 dpi), so the inserted picture carries the same `wp:extent` as
  the placeholder it replaces and the calibrated page layout cannot reflow. When a
  real chart lands the `Insert <slot>` marker line is dropped (the chart replaces
  the paste step); a placeholder slot keeps its marker for hand navigation.
- **Manifest.** The build prints `charts resolved from <dir>: N/M slots` plus a
  named `placeholder fallback:` list, and the final `chart slots:` line shows each
  slot's source file — an unresolved slot is a visible gap, never a silent null.
  Record the resolution line in `self_audit.md`.

## Fitting a hand-charted dashboard to one page per theme (`engine/fit_pages.py`)

**Status since 13 Aug 2026 (Engine v4.2): FALLBACK ONLY.** The engine now inserts
charts at the slot's exact measured geometry, so a normal build cannot reflow and
never needs fitting. fit_pages remains for one case: a HAND-EDITED dashboard where
someone pasted an image at arbitrary size outside the engine's insertion path.
Note it deliberately trims the top/bottom margins to 468 twips — an intentional
exception to the "do not change" margins row in the Fixed formatting facts below.

After a hand paste into the `Insert <theme>_chart_N` cells and a
re-save (often via Word), a block can grow past one page — Currency especially,
which carries three charts. `python3 engine/fit_pages.py <dashboard.docx>` fixes
pagination WITHOUT touching text: it trims top/bottom margins to 468 twips, zeroes
paragraph before/after spacing and reserved row-height minimums in the bordered
block tables, normalises inter-block breaks to a single page break (no blank
pages), then iteratively shrinks the charts of any block that still crosses a page
until it fits (status-ball ovals and the light-history heatmap are never touched).
A block that is text-heavy AND chart-heavy (Currency) also takes a ~0.9x line
compression so its charts stay readable rather than being shrunk to fit. Run it as
the last step on any hand-edited dashboard; then `check_layout.py` should pass and
`validate.py` should be clean. (24 Jul 2026: used to fit Eduardo's charted 07-24.)

## How to generate a report (every week)

```
python3 engine/macrobasis_fill.py \
    <newest MacroBasis_Report_Template*.docx> \
    MacroBasis_Dashboard_YYYY-MM-DD.docx \
    engine/content_YYYY-MM-DD.json
```

No prev-docx argument since v4.0: the template itself carries the Jun-30 quadrant
and its single dated marker (relabelled/moved each run). When Eduardo approves a
restructured dashboard, fold it back into the next template first:
`python3 engine/build_template_from_dashboard.py <approved.docx> MacroBasis_Report_Template_vN.docx`.

The agent's job each week is to produce `content_YYYY-MM-DD.json` (the researched
content) plus any generated keydev chart PNGs (`engine/charts/`). The engine handles
all formatting by cloning the template and injecting placeholder text. Do NOT write
a new docx with docx-js / python-docx from scratch — that is what produced the
off-spec 17 June draft.

Then validate + visually check (see "Verification").

## What the engine does (and why it's faithful)

1. Loads the template (inherits page size, margins, fonts, colours, borders,
   header bands, chart slots, the risk quadrant, and the nested tables).
2. Replaces `(As of YYYY_MM_DD)` in every block header with the run date.
3. **Risk quadrant (exec top):** transplants the quadrant + marker trail from the
   previous dashboard when given, adds this week's dated marker at the position in
   `quadrant_marker`, and prunes the trail to the **newest three** dated markers
   (this week + the two prior weeks). The quadrant picture, LTARP oval and legend
   are part of the drawing cluster and carry over untouched.
4. Fills the nested **Weekly Direction | Influencing Factors** 2-col table
   (`weekly_direction`, `influencing_factors`). `**bold**` inside any filled text
   becomes real bold (use it on the direction words). Since v3.2
   `influencing_factors` is a LIST (4 to 6 short lines since the 6 Aug 2026
   standard); the engine renders one paragraph per item.
5. Fills the Status-Dashboard grid (6 rows: status word + one-line development) and
   **auto-colours each oval** from the status word: **Escalating→green `#92D050`,
   Held→amber `#FFC000`, Deescalating→red `#EE0000`**. The Lights Guide Appendix is
   static in the template.
6. **RETIRED BY DEFAULT (30 Jul 2026):** the exec Key Developments | Implication
   rows are DROPPED at build (`drop_exec_key_developments`) and the Executive
   Summary ends at the Status Dashboard. Only `keep_exec_key_developments: true`
   restores the old fill path (`key_developments`, row cloned per item; that
   layout had replaced the Cross-theme takeaways / Key Risks cells on 2 Jul).
7. Per theme block: Status line **with the coloured traffic light** — since v3.2
   the engine prepends an inline **'Status Ball' oval shape** (the SAME wps
   ellipse as the exec dashboard lights, 0.16×0.17in / 146649×154880 EMU), NOT a
   text ●, coloured from the status word: Escalating→green `92D050`, Held→amber
   `FFC000`, Deescalating→red `EE0000`. **Exception (3 Jul standard): the
   Monetary Tracker appendix status line carries NO light and NO status word** —
   the engine strips any leading "Held ▸" so the line starts at the deciding
   sentence. Then "What changed this week" bullets, and the
   **Key Development of the Week** as full-width TEXT (generation of keydev charts
   is RETIRED, 17 Jul 2026). Legacy embed path, honoured only if a content file
   ever sets it again: with `keydev_chart_png` the engine builds a borderless
   nested 1×2 table (note LEFT, chart RIGHT ~3.2" wide, italic grey
   `keydev_chart_note` footnote). Then Implication and Watch next week.
8. Leaves every side chart slot exactly as the template defines it (see Chart Map).
9. Replaces the References list, **grouped by TOPIC mirroring the document's
   sections** (bold un-bulleted headers; every item tier-labelled in parentheses).
   The engine accepts `topic` (v3.1) or legacy `tier` as the group label key.
10. De-floats the page-anchored block tables to inline flow and inserts one spacer
    between blocks.

Placeholder replacement is bracket-aware (`[[ … ]]` may span several runs) and
preserves the run properties of the template, so font/size/italic/colour always match.

## Fixed formatting facts (from the template — do not change)

| Property | Value |
|----------|-------|
| Page | US Letter, 12240 × 15840 twips |
| Margins | top/bottom 720, left 720, right 284 twips (0.5"/0.5"/0.2") |
| Body font | Myriad Pro, 11pt (Normal style); developments & table cells 10pt (sz 20) |
| Theme/block accent colour | `#7B2952` (burgundy) — headers, borders, labels |
| Block header | full-width, fill `#7B2952`, white text 16pt bold, centred; right-tab "(As of YYYY_MM_DD)" |
| Section labels | bold `#7B2952` ("Status:", "What changed this week", "Key Development of the Week:", "Implication for the theme", "Watch next week") |
| Block table width | 11038 twips, 2 columns 5519/5519, all borders single sz 4 `#7B2952` |
| **Exec block** | R0 header → R1 [nested Weekly Direction \| Influencing Factors \| Current Environment table, quadrant INLINE with rationale beneath] → R2 [nested Status Dashboard, all six rows]. The template may still carry R3+ "Key Developments \| Implication" rows; the engine DROPS them by default (30 Jul 2026; `keep_exec_key_developments: true` restores) |
| Risk quadrant | map with the fixed Jun-30 reference point; the week's quadrant SHADED via `quadrant_highlight` baked into the image (30 Jul 2026 standard — no dot, no date label, no trail). Legacy dated-marker cluster (max 3 markers) reachable only via `quadrant_marker`/`quadrant_transplant` |
| Status-Dashboard grid | 3 cols; header fill `#7B2952`; Status cell = one word + a vector oval the engine recolours from that word (MORE/LESS of the theme, not good-vs-bad) |
| Theme Status line | engine-inserted **Status Ball oval** (same wps ellipse as the dashboard lights, 0.16×0.17in) + status word + deciding signal + the macro read WOVEN IN as a clause (9 Jul 2026: never a literal "Macro take:" label — the engine strips one if present; droppable when the signal line carries it). Monetary Tracker: no ball, no status word — straight to the sentence |
| Cell margins | every table carries a **0.15" (216 twips) right cell margin** (tblCellMar) so text never touches the border; template-wide since 2 Jul pm, incl. the engine's nested keydev table |
| Key Developments rows | dev cell = bulleted 10pt justified; implication cell = plain 10pt; engine clones the single template row per item |
| Keydev layout | borderless nested 1×2 table in the keydev cell: note text left (5950 dxa), generated chart right (4850 dxa) + 7pt italic grey how-built footnote |
| Lights Guide Appendix | static section before References explaining the more/less system |
| Monetary central-bank table | 3-col (Bank \| Rate \| Cycle) in the appendix's 2nd slot; engine fills from `central_bank`; first monetary chart slot stays blank |
| Key Development of the Week | per-theme prose block: advancement on the theme's most important topic + data point + a chart **beside it** (generated PNG embedded by the engine, or an `(Insert <theme>_keydev_chart.)` marker when no solid-data chart could be built) |
| Footer | "Public" (classification) + burgundy page number — inherited, never edit |
| Developments / watch | justified bullets, numId 3 level 1, 10pt black |

## Block & Chart Map (the composition that must never move)

Order: Executive Summary → Theme 1 → Theme 1 (Appendix) Monetary → Theme 2 →
Theme 3 → Theme 4 → Theme 5 → Theme 6 → **Illiquid Assets** → Light Scoring →
Inflation and Growth Read → Theme Light History → Lights Guide Appendix → References.

Side chart slots, by theme (manual insert, unchanged):

| Block | Chart slots (canonical marker text in the template) | Text column |
|-------|-----------------------------------------------------|-------------|
| Theme 1 Fiscal | `Insert fiscal_chart_1`, `Insert fiscal_chart_2` (left col) | right |
| Monetary appendix | `Insert monetary_1` (left col; 2nd slot = central-bank table) | right |
| Theme 2 Currency | `Insert currency_1` (R2 right), `Insert currency_2`, `Insert currency_3` (R3) | "What changed" top-left |
| Theme 3 Energy | `Insert energy_1`, `Insert energy_2` (left col) | right |
| Theme 4 AI | `Insert AI_1`, `Insert AI_2` (left col) | right |
| Theme 5 Geopolitics | `Insert geo_1`, `Insert geo_2` (left col) | right |
| Theme 6 Domestic | `Insert domestic_1` (R2 right), `Insert domestic_2` (R3) | "What changed" top-left |
| Illiquid Assets (generated block) | `Insert illiquid_1`, `Insert illiquid_2` | "What changed" right |

**Since 13 Aug 2026 (Engine v4.2) the engine fills these slots from Eduardo's
`ChartsThemes/` uploads at build**; a slot with no upload keeps the sized dashed
placeholder + marker for a hand paste. Slot names above are the canonical
`<base>_<n>` forms the alias resolver and `build_template_from_dashboard.py`
both use. **Keydev chart generation is RETIRED (17 Jul 2026):** the keydev row
is text only; the `keydev_chart_png` embed path remains in the engine for legacy
renders but no run should produce one. Never fabricate a series.

## content JSON schema

See `content_schema.json` for the blank template and field notes. **The schema's
`_canonical` block is the single source of enums and labels** — status words +
colours, block order, exact reference topic headers, war-leg names; prose
documents defer to it. Since v3:
- `key_developments` (4–6 dev/implication pairs) replaces `cross_theme` + `key_risks`.
- `quadrant_marker` places this week's outlook marker (EMU offsets; trail capped at 3).
- per-theme optional `keydev_chart_png`.
- `references` is a list of topic groups `{topic, items[]}` mirroring the document's sections, every item tier-labelled in its text (legacy `tier` group key still accepted).
- `weekly_direction` = ONE sentence: the inflation call + growth call (bold the
  direction words), no follow-up sentence.
- `influencing_factors` = a LIST of 4-6 short factor lines (6 Aug 2026 standard; was exactly 3 at v3.2)
  (growth evidence / inflation evidence / market confirmation), supporting
  evidence only — offsets live elsewhere. One paragraph rendered per item.
- `monetary.status` (v3.2) = no status word, no light; starts at the sentence.
- `material_note` never starts with "Key development:" (the row label says it).

## Verification (run every time)

```
python3 .../skills/docx/scripts/office/validate.py MacroBasis_Dashboard_YYYY-MM-DD.docx
# confirm zero leftover "[[" and zero "YYYY_MM_DD"
# render to PDF/images and eyeball: quadrant + 3 markers, status ovals/colours,
# Key Developments rows, keydev charts beside their notes, by-topic references
```

## Rules of engagement
- Edit the **Charter** when views change; edit **this engine/spec** only when the
  template structure itself changes. Never hand-format a one-off docx.
- If the template is revised, re-run the analyzer and update the Block & Chart Map.
- Eduardo's updated dashboards (`Dashboards_Eduardo_Updated/`) are the formatting
  ground truth; when he restructures a block by hand, fold it back into the template.
