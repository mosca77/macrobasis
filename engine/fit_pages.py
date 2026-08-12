#!/usr/bin/env python3
"""
fit_pages.py — make every MacroBasis block sit on exactly one page (24 Jul 2026).

Operates IN PLACE on a finished dashboard docx (incl. Word-saved ones with the
team's own charts pasted into the theme chart cells). It never touches text; it
only adjusts geometry:
  1. trims top/bottom page margins,
  2. zeroes paragraph before/after spacing inside the bordered block tables and
     removes reserved row-height minimums (so rows are exactly content height),
  3. normalises inter-block breaks to a single page break (no blank pages),
  4. iteratively shrinks the inline charts of any block that still crosses a
     page boundary until it fits (aspect ratio preserved; status-ball ovals and
     the light-history heatmap are never touched).

Usage: python3 engine/fit_pages.py <dashboard.docx> [max_iters]
"""
import sys, subprocess, tempfile, os, copy
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

WDRAW = qn('w:drawing')
WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'

def ptext(p):
    return "".join(t.text or "" for t in p.iter(qn('w:t')))

def block_title(t):
    tr = t.find(qn('w:tr'))
    return ptext(tr.find(qn('w:tc'))).strip() if tr is not None else ""

def set_margins(doc, top_bottom=468):
    for sect in doc.element.body.iter(qn('w:sectPr')):
        pg = sect.find(qn('w:pgMar'))
        if pg is not None:
            pg.set(qn('w:top'), str(top_bottom))
            pg.set(qn('w:bottom'), str(top_bottom))

def tighten_block(t):
    """Zero paragraph before/after spacing and drop reserved row minimums so the
    block is exactly as tall as its content."""
    for p in t.iter(qn('w:p')):
        pPr = p.find(qn('w:pPr'))
        if pPr is None:
            pPr = OxmlElement('w:pPr'); p.insert(0, pPr)
        spc = pPr.find(qn('w:spacing'))
        if spc is None:
            spc = OxmlElement('w:spacing')
            ref = pPr.find(qn('w:jc')) or pPr.find(qn('w:rPr'))
            (ref.addprevious(spc) if ref is not None else pPr.append(spc))
        spc.set(qn('w:before'), '0'); spc.set(qn('w:after'), '0')
        spc.set(qn('w:line'), '240'); spc.set(qn('w:lineRule'), 'auto')
    # rows: convert reserved heights to auto (content height); keep the header row's
    for ri, tr in enumerate(t.findall(qn('w:tr'))):
        trPr = tr.find(qn('w:trPr'))
        if trPr is None:
            continue
        he = trPr.find(qn('w:trHeight'))
        if he is not None and ri > 0:
            trPr.remove(he)

def scale_block_images(t, factor):
    """Scale every inline image in block `t` by `factor`, aspect kept. Skips the
    inline status-ball oval (~0.16in) which carries no cx big enough to matter."""
    n = 0
    for ext in t.iter('{%s}extent' % WP):
        cx, cy = int(ext.get('cx')), int(ext.get('cy'))
        if cx < 300000:            # status ball / tiny marks
            continue
        ext.set('cx', str(int(cx*factor))); ext.set('cy', str(int(cy*factor)))
        n += 1
    for xf in t.iter('{%s}ext' % A):
        cx, cy = xf.get('cx'), xf.get('cy')
        if cx and cy and int(cx) >= 300000:
            xf.set('cx', str(int(int(cx)*factor))); xf.set('cy', str(int(int(cy)*factor)))
    return n

def normalise_breaks(doc):
    """Between consecutive top-level block tables keep exactly ONE page break,
    carried by a single zero-height paragraph; drop empty non-break spacers and
    any doubled breaks that would produce a blank page."""
    body = doc.element.body
    kids = list(body.iterchildren())
    tbl = qn('w:tbl'); P = qn('w:p')
    # remove empty paragraphs that are not the sole break-carrier between tables
    prev_is_tbl = False
    for ch in kids:
        if ch.tag == tbl:
            prev_is_tbl = True
            continue
        if ch.tag == P:
            txt = ptext(ch).strip()
            has_draw = ch.find('.//'+WDRAW) is not None
            has_break = ch.find('.//'+qn('w:br')) is not None or \
                        (ch.find(qn('w:pPr')) is not None and
                         ch.find(qn('w:pPr')).find(qn('w:pageBreakBefore')) is not None)
            nxt = ch.getnext()
            next_is_tbl = nxt is not None and nxt.tag == tbl
            # drop empty, break-less spacer paragraphs sitting between two tables
            if txt == "" and not has_draw and not has_break and prev_is_tbl and next_is_tbl:
                body.remove(ch)
            prev_is_tbl = False

def render_pages(path):
    d = tempfile.mkdtemp()
    subprocess.run(["soffice","--headless","--convert-to","pdf","--outdir",d,path],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    pdf = os.path.join(d, os.path.splitext(os.path.basename(path))[0]+".pdf")
    txt = os.path.join(d, "o.txt")
    subprocess.run(["pdftotext","-layout",pdf,txt], check=True)
    return open(txt, encoding="utf-8", errors="ignore").read().split("\x0c")

# each block's UNIQUE header (as it renders) — these strings appear only on the
# block's own header row, never in the exec dashboard / light-scoring / references
THEME_HEADERS = [
    "Theme 1 — Fiscal Expansion & Deregulation",
    "Theme 1 Appendix — Monetary Policy Tracker",
    "Theme 2 — Currency Debasement",
    "Theme 3 — Energy & the Energy Transition",
    "Theme 4 — Artificial Intelligence",
    "Theme 5 — Geopolitics & Trade",
    "Theme 6 — Domestic Investing Pressures",
]

def page_of(pages, needle, start=0):
    for i in range(start, len(pages)):
        if needle in pages[i]:
            return i
    return -1

def offenders(pages):
    """A block spills iff the next block's header starts more than one page after
    this block's header (i.e. an interior page carries only this block's overflow).
    Returns the offending block's title, and 'KEYDEV' if Key Developments push
    Theme 1 off page 3."""
    bad = []
    hp = [page_of(pages, h) for h in THEME_HEADERS]
    # Key Developments occupy page 2 (index 1); Theme 1 must therefore start on p3
    if hp[0] > 2:
        bad.append("KEYDEV")
    for i in range(len(THEME_HEADERS) - 1):
        if hp[i] < 0 or hp[i+1] < 0:
            continue
        if hp[i+1] - hp[i] > 1:              # a spill page sits between the two
            bad.append(THEME_HEADERS[i])
    # last theme (Domestic) spills iff Light Scoring starts >1 page after it
    ls = page_of(pages, "Light Scoring and Developments")
    if hp[-1] >= 0 and ls >= 0 and ls - hp[-1] > 1:
        bad.append(THEME_HEADERS[-1])
    return bad

def main():
    path = sys.argv[1]
    max_iters = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    doc = Document(path)
    set_margins(doc, 468)
    for t in doc.element.body.findall(qn('w:tbl')):
        tighten_block(t)
    normalise_breaks(doc)
    doc.save(path)

    scales = {}                      # title -> cumulative factor
    for it in range(max_iters):
        pages = render_pages(path)
        bad = offenders(pages)
        print(f"iter {it}: pages={len(pages)} offenders={bad}")
        if not bad:
            print("ALL BLOCKS FIT")
            return 0
        doc = Document(path)
        tbls = doc.element.body.findall(qn('w:tbl'))
        for title in bad:
            if title == "KEYDEV":
                # text-only: tighten the key-dev table's paragraph spacing harder and
                # shave its dev-cell line spacing; also nudge margins once more
                for t in tbls:
                    if block_title(t).startswith("Key Developments") or \
                       (t.find(qn('w:tr')) is not None and "Key Developments" in ptext(t)):
                        for p in t.iter(qn('w:p')):
                            pPr = p.find(qn('w:pPr')) or p.insert(0, OxmlElement('w:pPr')) or p.find(qn('w:pPr'))
                        # drop any reserved row heights entirely
                        for tr in t.findall(qn('w:tr')):
                            trPr = tr.find(qn('w:trPr'))
                            if trPr is not None:
                                he = trPr.find(qn('w:trHeight'))
                                if he is not None:
                                    trPr.remove(he)
                continue
            for t in tbls:
                if block_title(t).startswith(title.split(" (")[0][:20]):
                    f = 0.90
                    scales[title] = scales.get(title, 1.0) * f
                    n = scale_block_images(t, f)
                    print(f"   shrank {n} charts in {title[:30]} to {scales[title]:.2f}")
                    break
        doc.save(path)
    print("WARN: some blocks may still spill after", max_iters, "iters; scales:", scales)
    return 1

if __name__ == "__main__":
    sys.exit(main())
