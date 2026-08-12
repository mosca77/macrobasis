#!/usr/bin/env python3
"""Layout checker (v3, 30 Jul 2026) — run after EVERY build; exits non-zero on any failure.

Required page schema (v4, 30 Jul 2026 per Eduardo):
  page 1  Executive Summary: Weekly Direction + Influencing Factors + the HIGHLIGHTED
          quadrant + the 'Why this quadrant' bullets + the FULL Status Dashboard
          (all 6 rows). The standing AIP note box is gone and so is the dot marker.
  RETIRED the exec 'Key Developments | Implication for Themes' page (30 Jul 2026) —
          it restated the theme blocks. Themes now start on page 2.
  themes  each block (Theme 1, Monetary appendix, Themes 2-6) occupies exactly ONE
          page, on consecutive pages (via the block-internal 'Watch next week' marker)
  then    Illiquid Assets (NEW 6 Aug 2026, per Eduardo — one page, Buy/Hold/Sell per
          sleeve, carries NO traffic light and no exec status row), then Light Scoring,
          then the Inflation and Growth Read, then Light History, each on its own page
  no interior blank / near-blank spill pages (a single trailing blank is allowed)

Usage: python3 engine/check_layout.py <dashboard.docx>
"""
import sys, subprocess, tempfile, os, glob

FILL_CEILING = 89.5      # % of page height; calibrated 30 Jul 2026 against Eduardo's
                         # approved 07-17 dashboard, whose Word-fitting pages render at
                         # up to 90.8% in LibreOffice while SPILLING there — the two
                         # renderers diverge by 1-2 lines, so blocks must keep headroom.

_PDF = None


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


def main():
    P = pages_text(sys.argv[1]); fails = []

    def check(cond, msg):
        print(("  PASS " if cond else "  FAIL ") + msg)
        if not cond:
            fails.append(msg)

    print("== Executive page 1 (direction + factors + quadrant rationale + ALL 6 status rows) ==")
    check("Weekly Direction" in P[0], "Weekly Direction on page 1")
    check("Influencing Factors" in P[0], "Influencing Factors on page 1")
    check("Why this quadrant" in P[0], "quadrant rationale bullets on page 1 (30 Jul standard)")
    check("AIP Jun 30" not in P[0],
          "standing AIP note box REMOVED from page 1 (30 Jul standard)")
    for n in ["1. Fiscal", "2. Currency", "3. Energy", "4. Artificial", "5. Geopolitics", "6. Domestic"]:
        check(n in P[0], f"status row '{n}' on page 1")

    print("== Exec Key Developments page retired (30 Jul standard) ==")
    check(not any("Implication for Themes" in p for p in P),
          "no exec 'Key Developments | Implication for Themes' block anywhere")

    print("== One theme block per page (via 'Watch next week') ==")
    # 6 Aug 2026 v4: the Illiquids page carries the framework grid instead of a Watch,
    # so the Watch count is back to SEVEN and Illiquids is asserted separately below.
    watch = [i + 1 for i, p in enumerate(P) if "Watch next week" in p]
    check(len(watch) == 7,
          f"7 theme blocks with a Watch (T1+Monetary+T2-6); found {len(watch)} at {watch}")
    check(len(set(watch)) == len(watch), "each block's Watch on a distinct page (no shared pages)")
    check(all(watch[i + 1] - watch[i] == 1 for i in range(len(watch) - 1)),
          f"block Watch pages consecutive: {watch}")
    if watch:
        check(watch[0] in (2, 3), f"first theme block on page 2 or 3 (Watch at p{watch[0]})")

    print("== Illiquid Assets block (6 Aug 2026 v4: PE news + framework grid) ==")
    il = [i + 1 for i, p in enumerate(P) if "Illiquid Assets" in p and "(As of" in p]
    check(bool(il), f"Illiquid Assets block present (p{il})")
    if il:
        check(len(il) == 1, f"Illiquid Assets occupies ONE page (found on {il})")
        page = P[il[0] - 1]
        check("What changed this week" in page,
              "Illiquid Assets carries 'What changed this week' (the private equity news sweep)")
        for cat in ("Performance", "Valuations", "Leverage", "Dry powder"):
            check(cat in page, f"framework cell '{cat}' on the Illiquids page")
        check("Escalating" not in page and "Deescalating" not in page,
              "Illiquid Assets carries NO traffic-light status word")
        if watch:
            check(il[0] == watch[-1] + 1,
                  f"Illiquid Assets (p{il[0]}) directly follows the themes (last theme p{watch[-1]})")

    print("== Back sections: Light Scoring -> Inflation and Growth Read -> Light History ==")
    ls = [i + 1 for i, p in enumerate(P) if "Light Scoring and Developments" in p and "(As of" in p]
    rg = [i + 1 for i, p in enumerate(P) if "Inflation and Growth Read" in p and "(As of" in p]
    lh = [i + 1 for i, p in enumerate(P) if "Theme Light History" in p and "(As of" in p]
    check(bool(ls) and bool(rg) and bool(lh),
          f"Light Scoring (p{ls}), Inflation and Growth Read (p{rg}), Light History (p{lh}) all present")
    if ls and rg and lh and watch:
        # Light Scoring may run to 2 pages: since 30 Jul 2026 it must spell out HOW each
        # finding feeds its theme, which is deliberately longer than a one-page table.
        # Since 6 Aug 2026 the Illiquid Assets page sits between the themes and it.
        _prev = il[0] if il else watch[-1]
        check(ls[0] == _prev + 1,
              f"Light Scoring starts (p{ls[0]}) right after "
              f"{'Illiquid Assets' if il else 'the themes'} (p{_prev})")
        check(rg[0] - ls[0] <= 1,
              f"Light Scoring occupies ONE page (30 Jul 2026: one page per section) (p{ls[0]} -> p{rg[0]})")
        check(rg[0] > ls[0],
              f"Inflation and Growth Read (p{rg[0]}) follows Light Scoring (p{ls[0]})")
        check(lh[0] == rg[0] + 1,
              f"Light History (p{lh[0]}) directly follows the regime table (p{rg[0]})")

    print("== Fill gauge: headroom on every block page (Word calibration) ==")
    fills = page_fills(_PDF)
    refs_start = next((i + 1 for i, p in enumerate(P) if "References" in p or "(Tier 1)" in p or "(Tier 2)" in p), len(P))
    gauge = [(i + 1, f) for i, f in enumerate(fills) if i + 1 < refs_start]
    print("   fills: " + " ".join(f"p{n}:{f:.0f}%" for n, f in gauge))
    over = [(n, f) for n, f in gauge if f > FILL_CEILING]
    check(not over, f"every block page ends <= {FILL_CEILING}% of page height "
                    f"(offenders: {[(n, round(f, 1)) for n, f in over]})")

    print("== No blank / spill pages (trailing blank allowed) ==")
    blanks = [i + 1 for i, p in enumerate(P[:-1]) if len(p.split()) <= 8]
    check(not blanks, f"no interior near-blank pages (offenders: {blanks})")

    print(f"\nTotal pages: {len(P)}   Failures: {len(fails)}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
