#!/usr/bin/env python3
"""Regenerate the Theme Light History heatmap from a run's content JSON.

Was an ad-hoc step before 30 July 2026; made reusable so every run produces the
image the same way. Reads `light_history` out of the content file and writes the
png to `light_history_png` (creating the folder).

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


def main():
    content = json.load(open(sys.argv[1]))
    make_quadrant_chart(content)
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
