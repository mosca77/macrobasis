#!/usr/bin/env python3
"""Layout checker (v4, 12 Aug 2026) — run after EVERY build; exits non-zero on any failure.

Required page schema (v4 layout, 30 Jul / 6 Aug 2026 per Eduardo — UNCHANGED):
  page 1  Executive Summary: Weekly Direction + Influencing Factors + the HIGHLIGHTED
          quadrant + the 'Why this quadrant' bullets + the FULL Status Dashboard
          (all 6 rows). The standing AIP note box is gone and so is the dot marker.
  RETIRED the exec 'Key Developments | Implication for Themes' page (30 Jul 2026) —
          it restated the theme blocks. Themes now start on page 2.
  themes  each block (Theme 1, Monetary appendix, Themes 2-6) occupies exactly ONE
          page, on consecutive pages (via the block-internal 'Watch next week' marker)
  then    Illiquid Assets (6 Aug 2026 v4 — one page: 'What changed this week' PE news +
          the Performance | Valuations / Leverage | Dry powder grid, carries NO traffic
          light and no exec status row), then Light Scoring, then the Inflation and
          Growth Read, then Light History, each on its own page.

RENDERER RECALIBRATION (v4, 12 Aug 2026) — checker only, no docx/template/engine change
  Calibrated in: LibreOffice 24.2.7.2 420(Build:2) headless + poppler, this sandbox.
  Basis files (both KNOWN-GOOD, rendered here):
    - Dashboards_Claude_Generated/MacroBasis_Dashboard_2026-08-06.docx (passed the gate
      in its own build environment)
    - Dashboards_Eduardo_Updated/MacroBasis_Dashboard_2026-08-07.docx (Eduardo-approved;
      fits one-page-per-block in Word)
  Why v3 failed here: this LibreOffice paginates MORE tightly than the environment v3
  was calibrated in. A Word page that is full does not stay one page — it OVERFLOWS onto
  a following CONTINUATION page. The overflow varies in size: theme blocks spill a line
  or two (~11-16% fill), but the exec Status Dashboard spills to a ~44%-fill page and the
  Illiquids grid's bottom row (Leverage / Dry powder) spills to a ~30%-fill page. So the
  physical page numbers no longer match Word's logical pages, and literal cell text lands
  a page later than v3 expects.
  Fixes (checker only):
    1. LOGICAL PAGE RECONSTRUCTION. A physical page STARTS a new logical page iff it bears
       a section header (the '(As of 2026_…)' date stamp); every other page is a
       continuation and is merged back into the logical page it overflowed from. The
       page-schema checks (status rows on page 1, consecutive theme pages, Illiquids
       grid, back-matter order) run on this reconstructed logical sequence. This subsumes
       the near-blank artifacts AND the larger structural splits (a pure <20% rule would
       miss the 44%/30% continuations). Near-blank (<20% fill) continuation pages are the
       degenerate case; they are also counted/capped/reported on their own below.
    2. FILL_CEILING re-derived empirically (see the constant). Max legit non-reference
       page fill across BOTH known-good files is 90.8% here, so the ceiling sits ~1 line
       above that with headroom for the renderer's 1-2 line jitter.
    3. Literal cell/section matching is whitespace- and linebreak-tolerant (a cell like
       'Dry powder' can wrap as 'Dry\\npowder' or gain padding across the split).

Usage: python3 engine/check_layout.py <dashboard.docx>
"""
import sys, subprocess, tempfile, os, glob, re

FILL_CEILING = 92.5      # % of page height. Recalibrated 12 Aug 2026 in LibreOffice
                         # 24.2.7.2 against BOTH known-good files (08-06 built-good,
                         # 08-07 Eduardo-approved): their highest non-reference page
                         # renders at 90.8% here (08-06 p6/p8/p10, 08-07 p6) WITHOUT
                         # spilling — in this renderer that is a healthy full page, not
                         # an overflow. Ceiling set just above that max with ~1 line of
                         # headroom (a body line is ~1.4% of page height at 60 DPI) so
                         # the 1-2 line render jitter never trips a good page, while a
                         # genuinely over-full page (>=92.5%) still fails.

NEAR_BLANK = 20.0        # % fill; an interior page below this is a renderer continuation
                         # artifact (content that overflowed from the page before it).
NEAR_BLANK_CAP = 6       # both known-good files show exactly 3 such pages here; cap at 6
                         # (2x) so ordinary spill is fine but a render that has exploded
                         # into many blank pages still fails.

_PDF = None


def _norm(s):
    """Collapse every run of whitespace (incl. line breaks) to a single space."""
    return re.sub(r"\s+", " ", s)


def has(hay, needle):
    """Whitespace-/linebreak-tolerant containment (v4): match on normalised text so a
    cell label split across a line ('Dry\\npowder') or padded across a page overflow
    still matches its literal ('Dry powder')."""
    return _norm(needle) in _norm(hay)


def page_fills(pdf):
    """Content-bottom as % of page height per page, footer band excluded."""
    from PIL import Image
    import numpy as np
    d = tempfile.mkdtemp()
    subprocess.run(["pdftoppm", "-png", "-r", "60", pdf, os.path.join(d, "p")], check=True)
    out = []
    for f in sorted(glob.glob(os.path.join(d, "p-*.png"))):
        a = np.array(Image.open(f).convert("L")); H = a.shape[0]
        ink = (a < 150)[:int(H * 0.91), :]
        rows = ink.sum(1)
        nz = [i for i, v in enumerate(rows) if v > 3]
        out.append((nz[-1] / H * 100) if nz else 0.0)
    return out


def pages_text(docx):
    d = tempfile.mkdtemp()
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", d, docx],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    pdf = os.path.join(d, os.path.splitext(os.path.basename(docx))[0] + ".pdf")
    global _PDF
    _PDF = pdf
    txt = os.path.join(d, "o.txt")
    subprocess.run(["pdftotext", "-layout", pdf, txt], check=True)
    return open(txt, encoding="utf-8", errors="ignore").read().split("\x0c")


def logical_pages(P):
    """Collapse renderer continuation pages into the logical page they overflowed from.

    In LibreOffice 24.2 a full Word page overflows onto one or more following physical
    pages; those continuation pages never carry a section header. A page STARTS a new
    logical page iff it bears an '(As of 2026_…)' date stamp (or it is the first page);
    every other page's text is appended to the logical page in progress. Returns
    (logical_texts, mapping) where mapping[k] lists the 1-based physical page numbers
    fused into logical page k+1."""
    logical, mapping = [], []
    for i, p in enumerate(P):
        # A page opens a new logical page if it bears a dated section header, or if it is
        # a References page (tier-tagged) — otherwise reference citations, some of which
        # name sections like 'Illiquid Assets', would fold into Light History and be
        # mistaken for those sections' own pages.
        starts = (not logical) or ("(As of 2" in p) or ("(Tier 1)" in p) or ("(Tier 2)" in p)
        if starts:
            logical.append(p)
            mapping.append([i + 1])
        else:
            logical[-1] += "\n" + p
            mapping[-1].append(i + 1)
    return logical, mapping


def main():
    P = pages_text(sys.argv[1]); fails = []
    L, lmap = logical_pages(P)

    def check(cond, msg):
        print(("  PASS " if cond else "  FAIL ") + msg)
        if not cond:
            fails.append(msg)

    # Show how the physical render was folded back into logical pages.
    merged = [(k + 1, phys) for k, phys in enumerate(lmap) if len(phys) > 1]
    print("== Logical page reconstruction (renderer continuation pages merged, v4) ==")
    print(f"   physical pages: {len([p for p in P if p.strip()])}   logical pages: {len(L)}")
    if merged:
        print("   merged continuations (logical <- physical): "
              + "  ".join(f"L{k}<-{phys}" for k, phys in merged))

    print("== Executive page 1 (direction + factors + quadrant rationale + ALL 6 status rows) ==")
    check(has(L[0], "Weekly Direction"), "Weekly Direction on logical page 1")
    check(has(L[0], "Influencing Factors"), "Influencing Factors on logical page 1")
    check(has(L[0], "Why this quadrant"), "quadrant rationale bullets on logical page 1 (30 Jul standard)")
    check(not has(L[0], "AIP Jun 30"),
          "standing AIP note box REMOVED from logical page 1 (30 Jul standard)")
    for n in ["1. Fiscal", "2. Currency", "3. Energy", "4. Artificial", "5. Geopolitics", "6. Domestic"]:
        check(has(L[0], n), f"status row '{n}' on logical page 1")

    print("== Exec Key Developments page retired (30 Jul standard) ==")
    check(not any(has(p, "Implication for Themes") for p in L),
          "no exec 'Key Developments | Implication for Themes' block anywhere")

    print("== One theme block per page (via 'Watch next week') ==")
    # 6 Aug 2026 v4: the Illiquids page carries the framework grid instead of a Watch,
    # so the Watch count is SEVEN (T1 + Monetary + T2-6). Logical pages, so a theme that
    # spilled onto a continuation page still counts once.
    watch = [k + 1 for k, p in enumerate(L) if has(p, "Watch next week")]
    check(len(watch) == 7,
          f"7 theme blocks with a Watch (T1+Monetary+T2-6); found {len(watch)} at {watch}")
    check(len(set(watch)) == len(watch), "each block's Watch on a distinct logical page (no shared pages)")
    check(all(watch[i + 1] - watch[i] == 1 for i in range(len(watch) - 1)),
          f"block Watch logical pages consecutive: {watch}")
    if watch:
        check(watch[0] in (2, 3), f"first theme block on logical page 2 or 3 (Watch at L{watch[0]})")

    print("== Illiquid Assets block (6 Aug 2026 v4: PE news + framework grid) ==")
    il = [k + 1 for k, p in enumerate(L) if has(p, "Illiquid Assets") and has(p, "(As of 2")]
    check(bool(il), f"Illiquid Assets block present (L{il})")
    if il:
        check(len(il) == 1, f"Illiquid Assets occupies ONE logical page (found on {il})")
        page = L[il[0] - 1]
        check(has(page, "What changed this week"),
              "Illiquid Assets carries 'What changed this week' (the private equity news sweep)")
        for cat in ("Performance", "Valuations", "Leverage", "Dry powder"):
            check(has(page, cat), f"framework cell '{cat}' on the Illiquids page")
        check(not has(page, "Escalating") and not has(page, "Deescalating"),
              "Illiquid Assets carries NO traffic-light status word")
        if watch:
            check(il[0] == watch[-1] + 1,
                  f"Illiquid Assets (L{il[0]}) directly follows the themes (last theme L{watch[-1]})")

    print("== Back sections: Light Scoring -> Inflation and Growth Read -> Light History ==")
    ls = [k + 1 for k, p in enumerate(L) if has(p, "Light Scoring and Developments") and has(p, "(As of 2")]
    rg = [k + 1 for k, p in enumerate(L) if has(p, "Inflation and Growth Read") and has(p, "(As of 2")]
    lh = [k + 1 for k, p in enumerate(L) if has(p, "Theme Light History") and has(p, "(As of 2")]
    check(bool(ls) and bool(rg) and bool(lh),
          f"Light Scoring (L{ls}), Inflation and Growth Read (L{rg}), Light History (L{lh}) all present")
    if ls and rg and lh and watch:
        # Since 6 Aug 2026 the Illiquid Assets page sits between the themes and Light
        # Scoring. Logical pages, so each back section is one page even if it spilled.
        _prev = il[0] if il else watch[-1]
        check(ls[0] == _prev + 1,
              f"Light Scoring starts (L{ls[0]}) right after "
              f"{'Illiquid Assets' if il else 'the themes'} (L{_prev})")
        check(rg[0] - ls[0] <= 1,
              f"Light Scoring occupies ONE logical page (L{ls[0]} -> L{rg[0]})")
        check(rg[0] > ls[0],
              f"Inflation and Growth Read (L{rg[0]}) follows Light Scoring (L{ls[0]})")
        check(lh[0] == rg[0] + 1,
              f"Light History (L{lh[0]}) directly follows the regime table (L{rg[0]})")

    print("== Fill gauge: headroom on every block page (renderer calibration, physical pages) ==")
    fills = page_fills(_PDF)
    refs_start = next((i + 1 for i, p in enumerate(P)
                       if has(p, "References") or has(p, "(Tier 1)") or has(p, "(Tier 2)")), len(P))
    gauge = [(i + 1, f) for i, f in enumerate(fills) if i + 1 < refs_start]
    print("   fills: " + " ".join(f"p{n}:{f:.0f}%" for n, f in gauge))
    over = [(n, f) for n, f in gauge if f > FILL_CEILING]
    check(not over, f"every block page ends <= {FILL_CEILING}% of page height "
                    f"(offenders: {[(n, round(f, 1)) for n, f in over]})")

    print("== Renderer continuation pages: near-blank count within cap (trailing blank allowed) ==")
    # v4: this renderer inserts near-blank continuation pages by design (see header).
    # Count/report them and fail only if there are pathologically many; the last physical
    # page is an allowed trailing blank.
    nb = [(i + 1, f) for i, f in enumerate(fills) if i + 1 < len(fills) and f < NEAR_BLANK]
    print(f"   interior near-blank (<{NEAR_BLANK:.0f}% fill) continuation pages: "
          f"{[(n, round(f, 1)) for n, f in nb]}")
    check(len(nb) <= NEAR_BLANK_CAP,
          f"near-blank continuation-page count within cap ({len(nb)} <= {NEAR_BLANK_CAP})")

    print(f"\nPhysical pages: {len(fills)}   Logical pages: {len(L)}   Failures: {len(fails)}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
