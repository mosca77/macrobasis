# ChartsThemes — Eduardo's weekly theme charts

Here you will find the charts that will be used inside each theme. Take them for the weeks run.

**How they are used (since 13 Aug 2026):** the build engine (`engine/macrobasis_fill.py`) reads this folder every run and inserts each chart into its matching `Insert <slot>` cell of the dashboard, letterboxed to the slot's measured size so the page layout never reflows. Nothing to do beyond uploading here.

**Naming:** one file per slot, theme name + slot number. Matching is tolerant to case, separators and doubled `.png.png` — all current spellings resolve:

| Upload name | Slot |
|---|---|
| `fiscal_chart_1/2` | fiscal_chart_1/2 |
| `monetary_1` | monetary_1 |
| `Currency_debasement_1/2/3` | currency_1/2/3 |
| `energy1/2` | energy_1/2 |
| `artficial_intelligence1/2` | AI_1/2 |
| `geopolitics_1` / `Geopolitics_2` | geo_1/2 |
| `domestic1/2` | domestic_1/2 |
| `Illiquids_1/2` | illiquid_1/2 |

**Retiring a chart:** rename it to start with `retired` (or delete it). Files named `retired*` and empty files are skipped; a slot with no chart gets the old dashed placeholder + `Insert <slot>` marker for a hand paste, and the build names the gap.

Full mechanics: Engine v4.2 in `engine/MacroBasis_DOCX_Format_Spec.md`.
