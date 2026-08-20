#!/usr/bin/env python3
"""Regenerate the light-history images for a run's content JSON.

Was an ad-hoc step before 30 July 2026; made reusable so every run produces the
images the same way. Three products, all from `light_history` (+ `quadrant_history`):

1. DOT STRIPS (19 Aug 2026, Eduardo's Week by Week Development page): a shared
   date-header png plus one dot-strip png per theme — `history_dates.png` and
   `history_dots_1.png` .. `history_dots_N.png` — written into the same folder as
   `light_history_png`. All strips share IDENTICAL geometry (same width, same x
   positions, no tight cropping, transparent background) so the date row and every
   theme row stay column-aligned when the engine embeds them in the block table.
   Dots compress as weeks accumulate, so the strip scales to any number of weeks.
2. The legacy HEATMAP (`light_history_png`) — kept as the engine's fallback render
   for content files that carry no `light_history.evolution`.
3. The quadrant residency bar chart (`quadrant_history_png`).

Usage: python3 engine/make_light_history.py engine/content_YYYY-MM-DD.json
"""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

COL = {"escalating": "#92D050", "held": "#FFC000",
       "deescalating": "#EE0000", "de-escalating": "#EE0000"}
TXT = {"escalating": "#1b1b1b", "held": "#1b1b1b",
       "deescalating": "#FFFFFF", "de-escalating": "#FFFFFF"}
ABBR = {"escalating": "E", "held": "H", "deescalating": "D", "de-escalating": "D"}


def make_quadrant_chart(content):
    """30 Jul 2026: horizontal bar of weekly reads per AIP quadrant, from
    `quadrant_history` to `quadrant_history_png`. Agent-maintained: append the
    current week's quadrant each run (highlight standard, 24 Jul 2026 onward)."""
    qh = content.get("quadrant_history")
    out = content.get("quadrant_history_png")
    if not qh or not out:
        return
    order = ["Productivity Boost", "Inflation", "Deflation", "Stagflation"]
    cols = {"Productivity Boost": "#8FAADC", "Inflation": "#F4B183",
            "Deflation": "#A9D18E", "Stagflation": "#C00000"}
    counts = {q: 0 for q in order}
    for e in qh.get("weeks", []):
        q = e.get("quadrant")
        if q in counts:
            counts[q] += 1
    fig, ax = plt.subplots(figsize=(4.6, 1.12), dpi=220)
    ys = range(len(order))
    vals = [counts[q] for q in order]
    ax.barh(list(ys), vals, color=[cols[q] for q in order], height=0.58)
    ax.set_yticks(list(ys)); ax.set_yticklabels(order, fontsize=7.5)
    ax.invert_yaxis()
    mx = max(vals + [1])
    ax.set_xlim(0, mx + 0.6)
    ax.set_xticks(range(0, mx + 1))
    ax.tick_params(axis="x", labelsize=7)
    for y, v in zip(ys, vals):
        ax.text(v + 0.08, y, str(v), va="center", fontsize=8, fontweight="bold")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    plt.tight_layout(pad=0.3)
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    print("wrote", out, "counts:", counts)


def make_dot_strips(content):
    """19 Aug 2026 (Eduardo): the Week by Week Development page renders each theme's
    lights as a row of coloured dots under a shared date header. Every figure here
    uses the SAME width, x-limits and margins and is saved WITHOUT tight cropping,
    so the columns align across the date header and all theme strips when the engine
    stacks them in the block table. Transparent background so cell shading shows."""
    hist = content.get("light_history") or {}
    themes, weeks = hist.get("themes"), hist.get("weeks")
    png = content.get("light_history_png")
    if not themes or not weeks or not png:
        return
    outdir = os.path.dirname(png) or "."
    os.makedirs(outdir, exist_ok=True)
    n = len(weeks)
    W_IN = 2.9
    cell_pt = W_IN / n * 72
    ms = min(11.0, cell_pt * 0.62)          # dot diameter in points, shrinks with n
    every = max(1, -(-n // 8))              # label at most ~8 dates, newest kept
    # Reserve half a label width at both edges (in cell units) so the newest and
    # oldest date labels are never clipped as the series grows; the SAME pad goes
    # on every figure so the date header and the dot strips stay column-aligned.
    pad = 12.0 / cell_pt

    def _short(d):
        """'06-18' -> '6/18' (the compact form Eduardo's mock uses)."""
        parts = str(d).replace("/", "-").split("-")
        if len(parts) == 2 and all(p.isdigit() for p in parts):
            return f"{int(parts[0])}/{int(parts[1])}"
        return str(d)

    def _axes(h_in):
        fig = plt.figure(figsize=(W_IN, h_in), dpi=220)
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(-pad, n + pad); ax.set_ylim(0, 1); ax.axis("off")
        return fig, ax

    fig, ax = _axes(0.24)
    for c, wk in enumerate(weeks):
        if (n - 1 - c) % every == 0:
            ax.text(c + 0.5, 0.5, _short(wk["date"]), ha="center", va="center",
                    fontsize=min(8.0, cell_pt * every * 0.30), color="#7B2952",
                    fontweight="bold")
    fig.savefig(os.path.join(outdir, "history_dates.png"), transparent=True)
    plt.close(fig)

    for r in range(len(themes)):
        fig, ax = _axes(0.22)
        for c, wk in enumerate(weeks):
            word = (wk["lights"][r] or "").strip().lower()
            ax.plot(c + 0.5, 0.5, "o", markersize=ms,
                    color=COL.get(word, "#D9D9D9"), markeredgewidth=0)
        fig.savefig(os.path.join(outdir, f"history_dots_{r + 1}.png"), transparent=True)
        plt.close(fig)
    print(f"wrote {outdir}/history_dates.png + {len(themes)} dot strips ({n} weeks)")


def main():
    content = json.load(open(sys.argv[1]))
    make_quadrant_chart(content)
    make_dot_strips(content)
    hist = content["light_history"]
    out = sys.argv[2] if len(sys.argv) > 2 else content["light_history_png"]
    themes, weeks = hist["themes"], hist["weeks"]
    nr, nc = len(themes), len(weeks)

    cell_w, cell_h = 0.86, 0.46
    fig_w = 2.9 + cell_w * nc
    fig_h = 0.62 + cell_h * nr
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=220)

    for r, theme in enumerate(themes):
        for c, wk in enumerate(weeks):
            word = (wk["lights"][r] or "").strip().lower()
            ax.add_patch(Rectangle((c, nr - 1 - r), 1, 1,
                                   facecolor=COL.get(word, "#D9D9D9"),
                                   edgecolor="white", linewidth=1.6))
            ax.text(c + 0.5, nr - 1 - r + 0.5, ABBR.get(word, "?"),
                    ha="center", va="center", fontsize=8.5, fontweight="bold",
                    color=TXT.get(word, "#1b1b1b"))

    ax.set_xlim(0, nc); ax.set_ylim(0, nr)
    ax.set_xticks([c + 0.5 for c in range(nc)])
    ax.set_xticklabels([w["date"] for w in weeks], fontsize=8)
    ax.set_yticks([nr - 1 - r + 0.5 for r in range(nr)])
    ax.set_yticklabels(themes, fontsize=8)
    ax.xaxis.set_ticks_position("top"); ax.xaxis.set_label_position("top")
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    plt.tight_layout(pad=0.35)

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    print("wrote", out, f"({nr} themes x {nc} weeks)")


if __name__ == "__main__":
    main()
