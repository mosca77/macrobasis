#!/usr/bin/env python3
"""
MacroBasis dashboard generator — TEMPLATE-FILL engine (v4.3, 19 Aug 2026).

VERSIONING: this docstring states the CURRENT engine version; the full version
history lives as the "Engine vX.Y" changelog sections in
engine/MacroBasis_DOCX_Format_Spec.md — bump BOTH when the engine changes.
v4.3 (19 Aug 2026): the Week by Week Development page (build_week_by_week_block)
replaces the heatmap render of Theme Light History — per theme, a dot strip of
every weekly light since June, a since-AIP verdict chip and a 'how it developed'
note, filled from light_history.evolution + the dot-strip pngs written by
engine/make_light_history.py; the heatmap render survives only as the fallback
for legacy content files.
v4.2 (13 Aug 2026): real chart insertion — the Co-Op's uploads in ChartsThemes/
are placed into their Insert <slot> cells at the slot's measured geometry;
unresolved slots keep the dashed placeholder.
v4.1 (6 Aug 2026): the Illiquid Assets block (build_illiquids_block, 2x2
framework grid, no light), centred block tables.

v4.0 (23 Jul 2026, the Co-Op's 17 Jul restructure folded in):
- **Jun-30 quadrant format.** The quadrant is the AIP's Jun 30th macroeconomic
  environment (map + note box + fixed Jun 30 reference point, all carried by the
  template). Each week shows ONE dated marker placed relative to that Jun 30
  baseline. `quadrant_relabel_and_move` renames the template's prior-week marker
  to this week's date and shifts it by `quadrant_marker.dx_emu/dy_emu`; the
  3-marker trail and the prev-docx transplant are RETIRED (pass
  `quadrant_transplant: true` to force the legacy path).
- **Exec pagination.** Page 1 = Weekly Direction + Influencing Factors + the
  quadrant; the Status Dashboard row page-breaks to page 2 with the Key
  Developments flowing after it.
- Monetary appendix title is now "Theme 1 Appendix — Monetary Policy Tracker",
  carries NO keydev row and a 7-row central-bank table.

v3.3 (6 Jul 2026): missing cells/blocks WARN and skip instead of crashing
(hand-edited dashboards can drop rows; the fill degrades gracefully).

v3.2 (from the Co-Op's 3 Jul hand edits): theme Status lines get an inline
'Status Ball' oval shape (identical to the exec dashboard lights) instead of
the coloured-text ●; the Monetary Tracker status line carries NO light and NO
status word (any leading 'Held ▸' in the JSON is stripped).

Clones MacroBasis_Report_Template.docx and injects ONLY placeholder text
(plus, since v3: exec Key Developments rows, tiered references, the weekly
risk-quadrant marker, and optional generated keydev chart images), so every
formatting detail is inherited from the template byte-for-byte.
Never rebuilds layout from scratch.

Usage:
    python3 macrobasis_fill.py <template.docx> <out.docx> <content.json>

LEGACY (retired with v4.0, 23 Jul 2026): a fourth [prev.docx] argument feeds the
old marker-trail transplant (three dated markers pruned oldest-first). That path
only runs when the content JSON sets `quadrant_transplant: true`; the default
flow uses the template's Jun-30 reference and the `quadrant_highlight` wash.

The content JSON schema is documented in MacroBasis_DOCX_Format_Spec.md.
"""
import sys, json, copy, re, datetime, os, tempfile
from io import BytesIO
from lxml import etree
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

MC_AC = '{http://schemas.openxmlformats.org/markup-compatibility/2006}AlternateContent'
WP = 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
PIC = 'http://schemas.openxmlformats.org/drawingml/2006/picture'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

def add_spacing_ordered(pPr):
    """Create and insert a <w:spacing> at the schema-correct position in pPr (before
    ind/jc/rPr etc.). Blindly appending puts it after <w:jc>, which violates OOXML
    element ordering, fails validation, and can hang LibreOffice's layout engine."""
    _after = {qn('w:' + t) for t in (
        'ind', 'contextualSpacing', 'mirrorIndents', 'suppressOverlap', 'jc',
        'textDirection', 'textAlignment', 'textboxTightWrap', 'outlineLvl', 'divId',
        'cnfStyle', 'rPr', 'sectPr', 'pPrChange')}
    spc = OxmlElement('w:spacing')
    ref = next((c for c in pPr if c.tag in _after), None)
    if ref is not None:
        ref.addprevious(spc)
    else:
        pPr.append(spc)
    return spc

def make_spacer():
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    spc = OxmlElement('w:spacing')
    spc.set(qn('w:before'), '120'); spc.set(qn('w:after'), '120')
    spc.set(qn('w:line'), '120'); spc.set(qn('w:lineRule'), 'auto')
    pPr.append(spc); p.append(pPr)
    return p

def compact_block_rows(block_tbl, min_twips):
    """9 Jul 2026: reset the reserved (fixed) row heights on a theme block to 'at least
    min_twips' so rows size to their content and the empty side-chart slots stop reserving
    excess vertical space — letting each theme fit one page. Header (row 0) and status
    (row 1) are left alone; content rows (What changed, keydev + chart, implication/watch)
    auto-grow to fit while pure chart-slot rows shrink to min_twips."""
    for tr in block_tbl.findall(qn('w:tr'))[2:]:
        trPr = tr.find(qn('w:trPr'))
        if trPr is None:
            trPr = OxmlElement('w:trPr'); tr.insert(0, trPr)
        he = trPr.find(qn('w:trHeight'))
        if he is None:
            he = OxmlElement('w:trHeight'); trPr.append(he)
        he.set(qn('w:val'), str(int(min_twips))); he.set(qn('w:hRule'), 'atLeast')
    # tighten paragraph spacing throughout the block so rows pack a little denser
    for p in block_tbl.iter(qn('w:p')):
        pPr = p.find(qn('w:pPr'))
        if pPr is None:
            pPr = OxmlElement('w:pPr'); p.insert(0, pPr)
        spc = pPr.find(qn('w:spacing'))
        if spc is None:
            spc = add_spacing_ordered(pPr)
        spc.set(qn('w:before'), '0'); spc.set(qn('w:after'), '20')
        # 30 Jul 2026: cap the line pitch too; the template carries auto leading that
        # LibreOffice renders taller than Word, and the block budget is per-line
        spc.set(qn('w:line'), '228'); spc.set(qn('w:lineRule'), 'auto')
    # 30 Jul 2026: drop TRAILING empty paragraphs inside every cell (placeholder
    # removal leaves them behind and each one costs a full line of row height)
    for tc in block_tbl.iter(qn('w:tc')):
        paras = tc.findall(qn('w:p'))
        while len(paras) > 1:
            last = paras[-1]
            if para_text(last).strip() or last.find('.//' + qn('w:drawing')) is not None:
                break
            tc.remove(last); paras = tc.findall(qn('w:p'))
    # compact nested-table rows too (e.g. the Monetary central-bank table) so they
    # size to their text rather than a reserved height
    for nt in block_tbl.iter(qn('w:tbl')):
        if nt is block_tbl:
            continue
        for tr in nt.findall(qn('w:tr')):
            trPr = tr.find(qn('w:trPr'))
            if trPr is None:
                trPr = OxmlElement('w:trPr'); tr.insert(0, trPr)
            he = trPr.find(qn('w:trHeight'))
            if he is None:
                he = OxmlElement('w:trHeight'); trPr.append(he)
            he.set(qn('w:val'), '250'); he.set(qn('w:hRule'), 'atLeast')

# CT_TblPrBase requires its children in this exact sequence. Word tolerates a wrong
# order, the OOXML validator does not, and a template that has been round-tripped
# through a hand edit can carry `tblLayout` appended after `tblLook`. Normalising at
# build time (6 Aug 2026) means a hand-edited template can never fail validation.
_TBLPR_ORDER = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize",
                "tblStyleColBandSize", "tblW", "jc", "tblCellSpacing", "tblInd",
                "tblBorders", "shd", "tblLayout", "tblCellMar", "tblLook",
                "tblCaption", "tblDescription", "tblPrChange"]


def centre_block_tables(doc):
    """6 Aug 2026 (the Co-Op): the template's page margins are asymmetric (left 720,
    right 284 twips), so a left-aligned 11038-twip block table shows a visibly larger
    gap on the left than the right. Rather than touch the template's page setup, give
    every TOP-LEVEL table an indent that centres it on the physical page: the white
    space either side of each bordered block becomes equal. Nested tables are left
    alone. Returns the count adjusted."""
    sect = doc.element.body.find(qn('w:sectPr'))
    if sect is None:
        return 0
    pg = sect.find(qn('w:pgSz'))
    mg = sect.find(qn('w:pgMar'))
    if pg is None or mg is None:
        return 0
    page_w = int(pg.get(qn('w:w')))
    left = int(mg.get(qn('w:left')))
    fixed = 0
    for t in top_tables(doc):
        tw = t.find(qn('w:tblPr'))
        if tw is None:
            continue
        we = tw.find(qn('w:tblW'))
        if we is None or we.get(qn('w:type')) != 'dxa':
            continue
        width = int(we.get(qn('w:w')))
        ind = (page_w - width) // 2 - left
        el = tw.find(qn('w:tblInd'))
        if el is None:
            el = OxmlElement('w:tblInd'); tw.append(el)
        el.set(qn('w:w'), str(ind)); el.set(qn('w:type'), 'dxa')
        # jc=left so the indent is authoritative in both renderers
        jc = tw.find(qn('w:jc'))
        if jc is not None:
            jc.set(qn('w:val'), 'left')
        fixed += 1
    return fixed


def restore_atleast_heights(doc):
    """Word drops hRule='atLeast' from row heights when it saves, and LibreOffice then
    reads the bare value as EXACT and clips whatever overflows. Because the template is
    built from a dashboard the Co-Op has hand-edited in Word, the exec direction row can
    arrive with an exact height that silently crops the top of the risk-quadrant map.
    That was invisible while the highlighted quadrant sat in the bottom row and became
    visible the first week it moved to the top row (6 Aug 2026). Restore atLeast on
    every row so a row can always grow to its content. Returns the count fixed."""
    fixed = 0
    for tr in doc.element.body.iter(qn('w:tr')):
        trPr = tr.find(qn('w:trPr'))
        if trPr is None:
            continue
        h = trPr.find(qn('w:trHeight'))
        if h is not None and h.get(qn('w:hRule')) != 'atLeast':
            h.set(qn('w:hRule'), 'atLeast')
            fixed += 1
    return fixed


def normalise_tblpr(doc):
    """Reorder every tblPr's children into schema sequence. Returns the count fixed."""
    rank = {qn('w:' + n): i for i, n in enumerate(_TBLPR_ORDER)}
    fixed = 0
    for tblPr in doc.element.body.iter(qn('w:tblPr')):
        kids = list(tblPr)
        want = sorted(kids, key=lambda e: rank.get(e.tag, len(rank)))
        if kids != want:
            for e in kids:
                tblPr.remove(e)
            for e in want:
                tblPr.append(e)
            fixed += 1
    return fixed


def hard_break_para():
    """A paragraph holding an explicit page break (w:br type=page) — reliably honored
    before engine-generated tables where pageBreakBefore-in-table is ignored."""
    return etree.fromstring(
        f'<w:p xmlns:w="{WNS}"><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr>'
        f'<w:r><w:br w:type="page"/></w:r></w:p>')

def break_before_para():
    """v4 (23 Jul 2026): a ZERO-HEIGHT top-level paragraph carrying pageBreakBefore.
    Unlike a literal w:br (which always advances a page, creating a blank page when
    the preceding block ends exactly at a boundary), pageBreakBefore is idempotent:
    it starts the paragraph on a fresh page only when the flow is mid-page. Renderers
    honour it reliably on top-level paragraphs (unlike first-paragraphs-in-tables)."""
    return etree.fromstring(
        f'<w:p xmlns:w="{WNS}"><w:pPr><w:pageBreakBefore/>'
        f'<w:spacing w:before="0" w:after="0"/>'
        f'<w:rPr><w:sz w:val="2"/><w:szCs w:val="2"/></w:rPr></w:pPr></w:p>')

def set_pagebreak_before(el):
    """9 Jul 2026: force a page break before the first paragraph inside `el` (a block
    table or a row), so each major block starts on a fresh page. Deterministic page
    schema. v4 fix (23 Jul 2026): pageBreakBefore must follow pStyle/keepNext/keepLines
    in pPr — inserting it at index 0 ahead of a pStyle (present throughout Word-saved
    dashboards) is schema-invalid and silently IGNORED by renderers."""
    p = el.find('.//' + qn('w:p'))
    if p is None:
        return
    pPr = p.find(qn('w:pPr'))
    if pPr is None:
        pPr = OxmlElement('w:pPr'); p.insert(0, pPr)
    if pPr.find(qn('w:pageBreakBefore')) is not None:
        return
    pbb = OxmlElement('w:pageBreakBefore')
    anchor = None
    for tag in ('w:keepLines', 'w:keepNext', 'w:pStyle'):
        e = pPr.find(qn(tag))
        if e is not None:
            anchor = e
            break
    if anchor is not None:
        anchor.addnext(pbb)
    else:
        pPr.insert(0, pbb)

def set_exec_row_heights(exec_t, r1=None, r2=None):
    """9 Jul 2026: the template reserves FIXED heights on exec R1 (direction/factors/quadrant,
    4881 twips) and R2 (status dashboard, 7095) — wasted space that pushes the 6th status row
    to page 2 no matter how small the quadrant is. Reset them to 'at least N' so the rows size
    to their content. R1 must stay >= the scaled quadrant height to avoid the float overlapping
    R2."""
    trs = exec_t.findall(qn('w:tr'))
    for idx, val in ((1, r1), (2, r2)):
        if val is None or idx >= len(trs):
            continue
        tr = trs[idx]
        trPr = tr.find(qn('w:trPr'))
        if trPr is None:
            trPr = OxmlElement('w:trPr'); tr.insert(0, trPr)
        he = trPr.find(qn('w:trHeight'))
        if he is None:
            he = OxmlElement('w:trHeight'); trPr.append(he)
        he.set(qn('w:val'), str(int(val))); he.set(qn('w:hRule'), 'atLeast')
        # Collapse the reserved EXACT heights on the nested tables inside this exec row
        # (the Weekly Direction | Influencing Factors 2-col table in R1, whose ~4964-twip
        # body row otherwise pins R1 tall, and the Status Dashboard grid in R2) to 'at
        # least' so they size to their text and all six status rows land on page 1. Only
        # EXACT heights are converted; the floating quadrant is handled by scale/behind.
        for nt in tr.iter(qn('w:tbl')):
            for ntr in nt.findall(qn('w:tr')):
                ntrPr = ntr.find(qn('w:trPr'))
                if ntrPr is None:
                    continue
                nhe = ntrPr.find(qn('w:trHeight'))
                if nhe is not None and nhe.get(qn('w:hRule')) != 'atLeast':
                    nhe.set(qn('w:val'), '200'); nhe.set(qn('w:hRule'), 'atLeast')

def defloat_and_space(doc):
    """Convert page-anchored floating block tables to inline flowing tables and
    insert spacer paragraphs between them (mirrors what Word does once filled)."""
    body = doc.element.body
    blocks = body.findall(qn('w:tbl'))
    for t in blocks:
        tblPr = t.find(qn('w:tblPr'))
        if tblPr is None:
            continue
        tp = tblPr.find(qn('w:tblpPr'))
        if tp is not None:
            tblPr.remove(tp)
    last_block = blocks[-1]
    children = list(body.iterchildren())
    last_idx = children.index(last_block)
    for ch in children[:last_idx]:
        if ch.tag == qn('w:p'):
            txt = "".join(t.text or "" for t in ch.iter(qn('w:t'))).strip()
            has_draw = ch.find('.//' + qn('w:drawing')) is not None
            if txt == "" and not has_draw:
                body.remove(ch)
    for t in blocks[1:]:
        t.addprevious(make_spacer())

# ---------- low-level helpers ----------
def iter_paras(tc):
    return tc.findall(qn('w:p'))

def para_text(p):
    return "".join(t.text or "" for t in p.iter(qn('w:t')))

def _set_run_bold(r, bold):
    rPr = r.find(qn('w:rPr'))
    if rPr is None:
        rPr = OxmlElement('w:rPr'); r.insert(0, rPr)
    b = rPr.find(qn('w:b'))
    if bold and b is None:
        rPr.append(OxmlElement('w:b'))
    elif not bold and b is not None:
        rPr.remove(b)

def fill_para_placeholder(p, text):
    """Replace a '[[ ... ]]' placeholder that may span MULTIPLE runs.
    Supports **bold** segments inside `text` (matches the guide's habit of
    bolding the direction words, e.g. '**slower growth**')."""
    runs = p.findall(qn('w:r'))
    spans = ["".join(t.text or "" for t in r.findall(qn('w:t'))) for r in runs]
    full = "".join(spans)
    if '[[' not in full:
        return False
    si = next(i for i, s in enumerate(spans) if '[[' in s)
    ei = si
    for i in range(si, len(spans)):
        if ']]' in spans[i]:
            ei = i; break
    sr = runs[si]
    segments = []                       # [(text, bold)]
    for j, part in enumerate(text.split('**')):
        if part:
            segments.append((part, j % 2 == 1))
    if not segments:
        segments = [("", False)]
    ts = sr.findall(qn('w:t'))
    if ts:
        ts[0].text = segments[0][0]
        ts[0].set(qn('xml:space'), 'preserve')
        for extra in ts[1:]:
            extra.getparent().remove(extra)
        if segments[0][1]:
            _set_run_bold(sr, True)
        prev = sr
        for seg, bold in segments[1:]:
            nr = copy.deepcopy(sr)
            nt = nr.findall(qn('w:t'))[0]
            nt.text = seg
            nt.set(qn('xml:space'), 'preserve')
            _set_run_bold(nr, bold)
            prev.addnext(nr)
            prev = nr
    for r in runs[si + 1:ei + 1]:
        r.getparent().remove(r)
    return True

def set_para_text(p, text):
    return fill_para_placeholder(p, text)

def fill_cell_placeholder(tc, text):
    for p in tc.findall(qn('w:p')):
        if '[[' in para_text(p):
            fill_para_placeholder(p, text)
            return True
    return False

def fill_bullets(tc, items):
    ph = [p for p in iter_paras(tc) if '[[' in para_text(p)]
    if not ph:
        return
    template_p = ph[0]
    anchor = ph[-1]
    for it in items:
        newp = copy.deepcopy(template_p)
        anchor.addnext(newp)
        anchor = newp
        set_para_text(newp, it)
    for p in ph:
        p.getparent().remove(p)

STATUS_LIGHTS = {"deescalating": "EE0000", "de-escalating": "EE0000",
                 "escalating": "92D050", "held": "FFC000"}
MC = 'http://schemas.openxmlformats.org/markup-compatibility/2006'
WPS = 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'
_STATUS_WORD_RE = re.compile(r'^\s*(?:de-?escalating|escalating|held)\s*▸?\s*', re.I)

def _status_ball_run(col):
    """An inline 'Status Ball' oval — the SAME wps ellipse shape as the exec
    Status Dashboard lights (0.16x0.17in), filled with the status colour.
    Since 3 Jul 2026 this replaces the old coloured-text ● (the Co-Op's standard:
    theme status lights match the dashboard ovals exactly)."""
    did = _next_id()
    xml = f'''<w:r xmlns:w="{WNS}" xmlns:mc="{MC}" xmlns:wp="{WP}" xmlns:a="{A}" xmlns:wps="{WPS}">
  <w:rPr><w:noProof/></w:rPr>
  <mc:AlternateContent><mc:Choice Requires="wps"><w:drawing>
    <wp:inline distT="0" distB="0" distL="0" distR="0">
      <wp:extent cx="146649" cy="154880"/>
      <wp:effectExtent l="0" t="0" r="6350" b="0"/>
      <wp:docPr id="{did}" name="Status Ball {did}"/>
      <wp:cNvGraphicFramePr/>
      <a:graphic><a:graphicData uri="{WPS}">
        <wps:wsp><wps:cNvSpPr/><wps:spPr>
          <a:xfrm><a:off x="0" y="0"/><a:ext cx="146649" cy="154880"/></a:xfrm>
          <a:prstGeom prst="ellipse"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="{col}"/></a:solidFill>
          <a:ln><a:noFill/></a:ln>
        </wps:spPr><wps:bodyPr rot="0" anchor="ctr"/></wps:wsp>
      </a:graphicData></a:graphic>
    </wp:inline>
  </w:drawing></mc:Choice></mc:AlternateContent>
</w:r>'''
    return etree.fromstring(xml)

def fill_status_line(block_tbl, text, light=True):
    """Fill the Status line. Theme blocks (light=True): prepend the coloured
    'Status Ball' oval (same shape as the exec dashboard lights) + a space run,
    colour from the status word. Monetary Tracker appendix (light=False,
    the Co-Op's 3 Jul standard): NO light and NO status word — any leading
    'Held ▸' etc. is stripped so the line starts at the deciding sentence."""
    for p in block_tbl.iter(qn('w:p')):
        if '[[Status' in para_text(p):
            if not light:
                text = _STATUS_WORD_RE.sub('', text)
            # 9 Jul 2026: never render a literal "Macro take:" label — weave the read in.
            text = re.sub(r'\.\s*Macro take:\s*', '. ', text)
            text = re.sub(r'\bMacro take:\s*', '', text)
            fill_para_placeholder(p, text)
            # 9 Jul 2026: the status line is plain body text (10pt sz20, black, not bold); ONLY
            # the ball carries colour. Overrides the template placeholder run (was 15pt green
            # 92D050), matching the Co-Op's approved 07-03 status lines exactly.
            for r in p.findall(qn('w:r')):
                if r.find('.//' + qn('w:drawing')) is not None or r.find(MC_AC) is not None:
                    continue
                rpr = r.find(qn('w:rPr'))
                if rpr is None:
                    rpr = OxmlElement('w:rPr'); r.insert(0, rpr)
                for tag, val in (('sz', '20'), ('szCs', '20'), ('color', '000000')):
                    e = rpr.find(qn('w:' + tag))
                    if e is None:
                        e = OxmlElement('w:' + tag); rpr.append(e)
                    e.set(qn('w:val'), val)
                bd = rpr.find(qn('w:b'))
                if bd is not None:
                    bd.getparent().remove(bd)
            if not light:
                return
            word = text.strip().split()[0].strip('.').strip(':').lower()
            col = next((v for k, v in sorted(STATUS_LIGHTS.items(), key=lambda x: -len(x[0]))
                        if word.startswith(k)), None)
            if col:
                for r in p.findall(qn('w:r')):
                    ts = r.findall(qn('w:t'))
                    if ts and (ts[0].text or '').strip():
                        # spacer run (cloned so font props match the text run)
                        sp = copy.deepcopy(r)
                        for extra in sp.findall(qn('w:t'))[1:]:
                            extra.getparent().remove(extra)
                        st = sp.findall(qn('w:t'))[0]
                        st.text = ' '
                        st.set(qn('xml:space'), 'preserve')
                        r.addprevious(_status_ball_run(col))
                        r.addprevious(sp)
                        break
            return

def fill_single_placeholder_cell(tc, text):
    for p in iter_paras(tc):
        if '[[' in para_text(p):
            fill_para_placeholder(p, text)
            return

# ---------- block / cell locators ----------
def top_tables(doc):
    return [t for t in doc.element.body.findall(qn('w:tbl'))]

def block_title(tbl):
    tr = tbl.find(qn('w:tr'))
    return para_text(tr.find(qn('w:tc'))).strip()

def nested_table(block_tbl):
    for t in block_tbl.iter(qn('w:tbl')):
        if t is not block_tbl:
            return t
    return None

def cells(block_tbl):
    return block_tbl.findall('.//' + qn('w:tc'))

def para_text_all(tc):
    return "\n".join(para_text(p) for p in iter_paras(tc))

def cell_containing(block_tbl, needle):
    for tc in cells(block_tbl):
        if needle in para_text_all(tc):
            return tc
    return None

def fill_data_table(tbl, rows):
    trs = tbl.findall(qn('w:tr'))
    body = trs[1:]
    template_tr = body[0]
    anchor = body[-1]
    for rd in rows:
        newtr = copy.deepcopy(template_tr)
        anchor.addnext(newtr)
        anchor = newtr
        tcs = newtr.findall(qn('w:tc'))
        for tc, val in zip(tcs, rd):
            fill_cell_placeholder(tc, val)
    for tr in body:
        tr.getparent().remove(tr)

def _body_note_para(note):
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    spc = OxmlElement('w:spacing'); spc.set(qn('w:before'), '40'); spc.set(qn('w:after'), '80')
    jc = OxmlElement('w:jc'); jc.set(qn('w:val'), 'both')
    pPr.append(spc); pPr.append(jc); p.append(pPr)
    r = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
    col = OxmlElement('w:color'); col.set(qn('w:val'), '000000')
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '20')
    szCs = OxmlElement('w:szCs'); szCs.set(qn('w:val'), '20')
    rPr.append(col); rPr.append(sz); rPr.append(szCs); r.append(rPr)
    t = OxmlElement('w:t'); t.set(qn('xml:space'), 'preserve'); t.text = note
    r.append(t); p.append(r)
    return p

_docpr_id = [90000]
def _next_id():
    _docpr_id[0] += 1
    return str(_docpr_id[0])

def _seed_ids(doc):
    """Duplicate drawing ids make renderers drop the whole drawing layer.
    Seed the counter above every docPr/cNvPr id already in the document
    (templates built from filled dashboards carry prior runs' ids)."""
    mx = _docpr_id[0]
    for el in doc.element.body.iter():
        if el.tag.endswith('}docPr') or el.tag.endswith('}cNvPr'):
            try:
                mx = max(mx, int(el.get('id') or 0))
            except ValueError:
                pass
    _docpr_id[0] = mx

def _inline_image_para(doc, png_path, width_emu, center=True):
    """A paragraph containing one inline picture, width_emu wide, aspect kept."""
    rid, image = doc.part.get_or_add_image(png_path)
    h_emu = int(width_emu * image.px_height / image.px_width)
    did = _next_id()
    xml = f'''<w:p xmlns:w="{WNS}" xmlns:wp="{WP}" xmlns:a="{A}" xmlns:pic="{PIC}" xmlns:r="{R}">
  <w:pPr><w:spacing w:before="40" w:after="40"/>{'<w:jc w:val="center"/>' if center else ''}</w:pPr>
  <w:r><w:drawing>
    <wp:inline distT="0" distB="0" distL="0" distR="0">
      <wp:extent cx="{width_emu}" cy="{h_emu}"/>
      <wp:docPr id="{did}" name="keydev_chart_{did}"/>
      <a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
        <pic:pic>
          <pic:nvPicPr><pic:cNvPr id="{did}" name="keydev_chart_{did}"/><pic:cNvPicPr/></pic:nvPicPr>
          <pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>
          <pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{width_emu}" cy="{h_emu}"/></a:xfrm>
            <a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>
        </pic:pic>
      </a:graphicData></a:graphic>
    </wp:inline>
  </w:drawing></w:r>
</w:p>'''
    return etree.fromstring(xml)

def _caption_para(text):
    """Small italic grey caption under the keydev chart (the 'how it was built'
    footnote)."""
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    spc = OxmlElement('w:spacing'); spc.set(qn('w:before'), '20'); spc.set(qn('w:after'), '40')
    jc = OxmlElement('w:jc'); jc.set(qn('w:val'), 'both')
    pPr.append(spc); pPr.append(jc); p.append(pPr)
    r = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
    i = OxmlElement('w:i'); rPr.append(i)
    col = OxmlElement('w:color'); col.set(qn('w:val'), '7F7F7F'); rPr.append(col)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '14')
    szCs = OxmlElement('w:szCs'); szCs.set(qn('w:val'), '14')
    rPr.append(sz); rPr.append(szCs); r.append(rPr)
    t = OxmlElement('w:t'); t.set(qn('xml:space'), 'preserve'); t.text = text
    r.append(t); p.append(r)
    return p

def _empty_para():
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    spc = OxmlElement('w:spacing'); spc.set(qn('w:before'), '0'); spc.set(qn('w:after'), '0')
    sz_pr = OxmlElement('w:rPr'); sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '2')
    sz_pr.append(sz); pPr.append(spc); pPr.append(sz_pr); p.append(pPr)
    return p

def _no_border_tbl(left_w, right_w):
    """A borderless fixed 1x2 nested table element (text left, chart right)."""
    xml = f'''<w:tbl xmlns:w="{WNS}">
  <w:tblPr>
    <w:tblW w:w="{left_w + right_w}" w:type="dxa"/>
    <w:tblBorders>
      <w:top w:val="none" w:sz="0" w:space="0"/><w:left w:val="none" w:sz="0" w:space="0"/>
      <w:bottom w:val="none" w:sz="0" w:space="0"/><w:right w:val="none" w:sz="0" w:space="0"/>
      <w:insideH w:val="none" w:sz="0" w:space="0"/><w:insideV w:val="none" w:sz="0" w:space="0"/>
    </w:tblBorders>
    <w:tblLayout w:type="fixed"/>
    <w:tblCellMar>
      <w:top w:w="20" w:type="dxa"/><w:left w:w="40" w:type="dxa"/>
      <w:bottom w:w="20" w:type="dxa"/><w:right w:w="216" w:type="dxa"/>
    </w:tblCellMar>
  </w:tblPr>
  <w:tblGrid><w:gridCol w:w="{left_w}"/><w:gridCol w:w="{right_w}"/></w:tblGrid>
  <w:tr>
    <w:tc><w:tcPr><w:tcW w:w="{left_w}" w:type="dxa"/><w:vAlign w:val="top"/></w:tcPr></w:tc>
    <w:tc><w:tcPr><w:tcW w:w="{right_w}" w:type="dxa"/><w:vAlign w:val="top"/></w:tcPr></w:tc>
  </w:tr>
</w:tbl>'''
    return etree.fromstring(xml)

def material_to_note(doc, block_tbl, note, chart_png=None, chart_note=None):
    """Key Development of the Week. With a generated chart: a borderless nested
    2-col table puts the note text LEFT and the chart RIGHT, with a small italic
    footnote under the chart explaining how it was built (chart_note). Without a
    chart the note keeps its '(Insert <theme>_keydev_chart.)' marker."""
    md_cell = cell_containing(block_tbl, "Key Development of the Week")
    if md_cell is None:
        if note:
            print("WARN: no 'Key Development of the Week' cell in block '%s' — skipped" % block_title(block_tbl)[:40])
        return
    for t in list(md_cell.findall(qn('w:tbl'))):
        t.getparent().remove(t)
    label_p = None
    for p in iter_paras(md_cell):
        if "Key Development of the Week" in para_text(p):
            label_p = p; break
    if label_p is None:
        print("WARN: keydev label paragraph missing in block '%s' — skipped" % block_title(block_tbl)[:40])
        return
    if chart_png:
        tbl = _no_border_tbl(5950, 4850)
        tcs = tbl.findall('.//' + qn('w:tc'))
        tcs[0].append(_body_note_para(note))
        tcs[1].append(_inline_image_para(doc, chart_png, width_emu=2500000))
        if chart_note:
            tcs[1].append(_caption_para(chart_note))
        else:
            tcs[1].append(_empty_para())
        label_p.addnext(tbl)
        tbl.addnext(_empty_para())     # a table may not end a cell
    else:
        label_p.addnext(_body_note_para(note))

# ---------- Executive Summary: Key Developments | Implication rows ----------
def fill_key_developments(exec_t, items):
    trs = exec_t.findall(qn('w:tr'))
    hdr_i = None
    for i, tr in enumerate(trs):
        txt = "".join(para_text(p) for p in tr.iter(qn('w:p'))).strip()
        if txt.startswith("Key Developments"):
            hdr_i = i; break
    if hdr_i is None or hdr_i + 1 >= len(trs):
        return
    template_tr = trs[hdr_i + 1]
    anchor = template_tr
    for it in items:
        ntr = copy.deepcopy(template_tr)
        anchor.addnext(ntr)
        anchor = ntr
        tcs = ntr.findall(qn('w:tc'))
        fill_cell_placeholder(tcs[0], it["development"])
        if len(tcs) > 1:
            fill_cell_placeholder(tcs[1], it["implication"])
    template_tr.getparent().remove(template_tr)

# ---------- Risk quadrant ----------
_DATE_RE = re.compile(r'^\d{2}[-/]\d{2}$')
_MC_CHOICE = '{http://schemas.openxmlformats.org/markup-compatibility/2006}Choice'

def _choice_text(anch):
    """Anchor text read from the mc:Choice branch ONLY (Word-saved files carry a
    VML Fallback duplicating every w:t, which doubles naive text joins)."""
    ch = anch.find('.//' + _MC_CHOICE)
    scope = ch if ch is not None else anch
    return "".join(t.text or '' for t in scope.iter(qn('w:t'))).strip()

def _is_red_dot(anch):
    """The dated marker's dot: a Flowchart Connector (circle) solid-filled EE0000."""
    for wsp in anch.iter('{%s}wsp' % WPS):
        geom = wsp.find('.//{%s}prstGeom' % A)
        fill = wsp.find('.//{%s}solidFill/{%s}srgbClr' % (A, A))
        if geom is not None and geom.get('prst') == 'flowChartConnector' \
           and fill is not None and (fill.get('val') or '').upper() == 'EE0000':
            return True
    return False

def quadrant_relabel_and_move(exec_t, marker):
    """Jun-30 reference format (17 Jul 2026 standard): the exec quadrant carries
    the AIP Jun 30th environment (map + note box + fixed reference point) and ONE
    dated weekly marker. Rename the template's prior-week marker (date label +
    red EE0000 dot) to this week's label and shift both by (dx_emu, dy_emu) —
    the displacement of this week's read vs the prior marker, both measured
    against the Jun 30 baseline. Any extra dated labels/red dots are pruned so
    exactly one dated marker remains. Everything else is untouched."""
    r1c0 = exec_t.findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    labels, dots = [], []
    for p in r1c0.findall(qn('w:p')):
        for run in p.findall(qn('w:r')):
            anch = run.find('.//{%s}anchor' % WP)
            if anch is None:
                continue
            txt = _choice_text(anch)
            if _DATE_RE.match(txt):
                labels.append((run, anch))
            elif _is_red_dot(anch):
                dots.append((run, anch))
    if not labels:
        print("WARN: quadrant has no dated marker label — marker not updated")
        return
    keep_lbl, extra_lbls = labels[0], labels[1:]
    keep_dot, extra_dots = (dots[0], dots[1:]) if dots else ((None, None), [])
    for run, _ in extra_lbls + extra_dots:
        run.getparent().remove(run)
    dx, dy = int(marker.get('dx_emu', 0)), int(marker.get('dy_emu', 0))
    for _, anch in (keep_lbl, keep_dot):
        if anch is None:
            continue
        for tag in ('positionH', 'positionV'):
            pos = anch.find('{%s}%s' % (WP, tag))
            if pos is None:
                continue
            off = pos.find('{%s}posOffset' % WP)
            if off is not None and (off.text or '').lstrip('-').isdigit():
                off.text = str(int(off.text) + (dx if tag == 'positionH' else dy))
    # relabel (strip the VML fallback so the text lives in one place)
    _strip_fallback(keep_lbl[0])
    first = True
    for t in keep_lbl[1].iter(qn('w:t')):
        t.text = marker['label'] if first else ''
        t.set(qn('xml:space'), 'preserve')
        first = False

def _anchor_info(run):
    """Return (anchor_el, name, date_text, x, y) for a run holding one wp:anchor."""
    anch = run.find('.//{%s}anchor' % WP)
    if anch is None:
        return None
    docpr = anch.find('{%s}docPr' % WP)
    name = docpr.get('name') if docpr is not None else ''
    txt = "".join(t.text or '' for t in anch.iter(qn('w:t'))).strip()
    offs = anch.findall('.//{%s}posOffset' % WP)
    x = int(offs[0].text) if len(offs) > 0 else 0
    y = int(offs[1].text) if len(offs) > 1 else 0
    return anch, name, txt, x, y

def _set_anchor_pos(anch, x, y):
    offs = anch.findall('.//{%s}posOffset' % WP)
    if len(offs) > 0: offs[0].text = str(x)
    if len(offs) > 1: offs[1].text = str(y)

def _strip_fallback(run):
    for ac in run.findall('.//' + MC_AC):
        fb = ac.find('{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback')
        if fb is not None:
            ac.remove(fb)

def _marker_runs(exec_t):
    """All runs in exec R1 that hold a floating anchor; classified."""
    r1c0 = exec_t.findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    out = {'date': [], 'oval': [], 'other': []}
    for p in r1c0.findall(qn('w:p')):
        for run in p.findall(qn('w:r')):
            info = _anchor_info(run)
            if info is None:
                continue
            anch, name, txt, x, y = info
            if _DATE_RE.match(txt):
                out['date'].append((run, anch, txt, x, y))
            elif 'Connector' in name:
                out['oval'].append((run, anch, x, y))
            else:
                out['other'].append((run, anch, name, x, y))
    return r1c0, out

def _marker_date_key(txt, asof):
    m, d = int(txt[:2]), int(txt[3:])
    y = asof.year
    dt = datetime.date(y, m, d)
    if dt > asof + datetime.timedelta(days=7):
        dt = datetime.date(y - 1, m, d)
    return dt

def quadrant_add_marker(exec_t, marker, asof_str):
    """Clone the newest dated marker (label textbox + oval), place it at the
    given EMU offsets, then prune so only the 3 newest dated markers remain."""
    asof = datetime.date(*[int(x) for x in asof_str.split('_')])
    r1c0, mk = _marker_runs(exec_t)
    if not mk['date'] or not mk['oval']:
        return
    dated = sorted(mk['date'], key=lambda t: _marker_date_key(t[2], asof))
    src_run, src_anch, src_txt, sx, sy = dated[-1]        # newest label
    # its paired oval = nearest oval by offset distance
    def pair_for(lx, ly):
        return min(mk['oval'], key=lambda o: (o[2] - lx) ** 2 + (o[3] - ly) ** 2)
    src_oval = pair_for(sx, sy)
    lbl_dx, lbl_dy = sx - src_oval[2], sy - src_oval[3]   # label offset vs oval
    ox, oy = int(marker['x_emu']), int(marker['y_emu'])
    # clone oval
    new_oval = copy.deepcopy(src_oval[0])
    _strip_fallback(new_oval)
    oinfo = _anchor_info(new_oval)
    _set_anchor_pos(oinfo[0], ox, oy)
    dp = oinfo[0].find('{%s}docPr' % WP)
    if dp is not None: dp.set('id', _next_id())
    src_oval[0].addnext(new_oval)
    # clone label
    new_lbl = copy.deepcopy(src_run)
    _strip_fallback(new_lbl)
    linfo = _anchor_info(new_lbl)
    _set_anchor_pos(linfo[0], ox + lbl_dx, oy + lbl_dy)
    dp = linfo[0].find('{%s}docPr' % WP)
    if dp is not None: dp.set('id', _next_id())
    first = True
    for t in linfo[0].iter(qn('w:t')):
        if first:
            t.text = marker['label']; first = False
        else:
            t.text = ''           # label may be split across runs (hand edits)
    src_run.addnext(new_lbl)
    # prune: keep the 3 newest dated markers (labels + their paired ovals)
    r1c0, mk = _marker_runs(exec_t)
    dated = sorted(mk['date'], key=lambda t: _marker_date_key(t[2], asof))
    excess = dated[:-3] if len(dated) > 3 else []
    for run, anch, txt, lx, ly in excess:
        ov = pair_for2(mk['oval'], lx, ly)
        run.getparent().remove(run)
        if ov is not None:
            ov[0].getparent().remove(ov[0])
            mk['oval'].remove(ov)

def pair_for2(ovals, lx, ly):
    if not ovals:
        return None
    return min(ovals, key=lambda o: (o[2] - lx) ** 2 + (o[3] - ly) ** 2)

def quadrant_from_prev(doc, exec_t, prev_path):
    """Transplant the whole quadrant drawing cluster (pictures, markers, arrows)
    from last week's dashboard so the trail carries forward. Image rels remapped."""
    prev = Document(prev_path)
    prev_exec = prev.element.body.findall(qn('w:tbl'))[0]
    if 'Executive Summary' not in block_title(prev_exec):
        return False
    prev_r1 = prev_exec.findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    cur_r1 = exec_t.findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    # collect prev anchor runs
    prev_runs = []
    for p in prev_r1.findall(qn('w:p')):
        for run in p.findall(qn('w:r')):
            if run.find('.//{%s}anchor' % WP) is not None:
                prev_runs.append(copy.deepcopy(run))
    if not prev_runs:
        return False
    # remap image rels
    prev_rels = {rid: rel for rid, rel in prev.part.rels.items() if 'image' in rel.reltype}
    for run in prev_runs:
        xml = etree.tostring(run).decode()
        for rid in set(re.findall(r'r:embed="(rId\d+)"', xml)):
            part = prev_rels[rid].target_part
            new_rid, _ = doc.part.get_or_add_image(BytesIO(part.blob))
            xml = xml.replace(f'r:embed="{rid}"', f'r:embed="{new_rid}"')
        run_new = etree.fromstring(xml)
        run.getparent() if run.getparent() is not None else None
        prev_runs[prev_runs.index(run)] = run_new
    # drop current anchor runs, insert prev ones into first paragraph
    first_p = cur_r1.find(qn('w:p'))
    for p in cur_r1.findall(qn('w:p')):
        for run in list(p.findall(qn('w:r'))):
            if run.find('.//{%s}anchor' % WP) is not None:
                p.remove(run)
    for run in prev_runs:
        first_p.append(run)
    return True

def scale_exec_quadrant(exec_t, factor):
    """9 Jul 2026: shrink the whole floating quadrant cluster (map, legend, markers,
    date labels, arrow) to `factor` of its size, scaling toward its top-left corner so
    the top stays put and the bottom moves UP, freeing page-1 room for all six status
    rows. Opt-in via `quadrant_scale`; 1.0 leaves it untouched. Uniform scale keeps the
    marker trail aligned on the map."""
    if not factor or abs(factor - 1.0) < 1e-6:
        return
    r1c0 = exec_t.findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    anchors = list(r1c0.iter('{%s}anchor' % WP))
    if not anchors:
        return
    xs, ys = [], []
    for a in anchors:
        for tag, bucket in (('positionH', xs), ('positionV', ys)):
            p = a.find('{%s}%s' % (WP, tag))
            if p is not None:
                o = p.find('{%s}posOffset' % WP)
                if o is not None and (o.text or '').lstrip('-').isdigit():
                    bucket.append(int(o.text))
    ox, oy = (min(xs) if xs else 0), (min(ys) if ys else 0)
    sc = lambda v: int(round(v * factor))
    for a in anchors:
        ext = a.find('{%s}extent' % WP)
        if ext is not None:
            ext.set('cx', str(sc(int(ext.get('cx'))))); ext.set('cy', str(sc(int(ext.get('cy')))))
        for tag, org in (('positionH', ox), ('positionV', oy)):
            p = a.find('{%s}%s' % (WP, tag))
            if p is not None:
                o = p.find('{%s}posOffset' % WP)
                if o is not None and (o.text or '').lstrip('-').isdigit():
                    o.text = str(org + sc(int(o.text) - org))
        for aext in a.iter('{%s}ext' % A):        # inner DrawingML shape/picture sizes
            if aext.get('cx') and aext.get('cy'):
                aext.set('cx', str(sc(int(aext.get('cx'))))); aext.set('cy', str(sc(int(aext.get('cy')))))
    return

def quadrant_behind_text(exec_t, on):
    """9 Jul 2026: put the floating quadrant cluster BEHIND text (behindDoc=1) so it
    never pushes the Status Dashboard down — the nested table then flows right after a
    short Influencing-Factors cell and all six theme rows fit on page 1 (the quadrant
    sits in the upper-right band above them). Opt-in via `quadrant_behind`."""
    if not on:
        return
    r1c0 = exec_t.findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    for anch in r1c0.iter('{%s}anchor' % WP):
        anch.set('behindDoc', '1')

# ---------- Quadrant highlight format (30 Jul 2026 standard, the Co-Op) ----------
# Replaces the single dated dot marker. The whole quadrant the week sits in is
# shaded with a translucent wash, the standing AIP note box is removed, and the
# reasons the marker used to imply are spelled out as bullets in the exec cell.

QUADRANT_CELLS = {
    # fractional bounds of each panel inside the map picture, measured from the
    # template's image (511 x 433 px): left col x 65-274, right col x 287-498;
    # top row y 8-189, bottom row y 202-384.
    "productivity boost": (0.1272, 0.0185, 0.5362, 0.4365),
    "inflation":          (0.5616, 0.0185, 0.9746, 0.4365),
    "deflation":          (0.1272, 0.4665, 0.5362, 0.8869),
    "stagflation":        (0.5616, 0.4665, 0.9746, 0.8869),
}
QUADRANT_ALIASES = {"productivity": "productivity boost", "growth": "productivity boost"}


def _quadrant_picture_anchor(r1c0):
    """The map image anchor — the largest picture-bearing anchor in the cell."""
    best, best_area = None, -1
    for a in r1c0.iter('{%s}anchor' % WP):
        if a.find('.//{%s}blip' % A) is None:
            continue
        ext = a.find('{%s}extent' % WP)
        if ext is None:
            continue
        area = int(ext.get('cx')) * int(ext.get('cy'))
        if area > best_area:
            best, best_area = a, area
    return best


def quadrant_strip_marker_and_note(exec_t, drop_note=True):
    """30 Jul 2026: remove the weekly dated dot + its date label, and (by default) the
    standing 'Note: The referenced chart is respective to the AIP Jun 30th
    Macroeconomic environment' box. The Jun 30 reference point lives inside the map
    image itself, so it survives. Returns the number of anchors removed."""
    r1c0 = exec_t.findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    pic = _quadrant_picture_anchor(r1c0)
    dropped = 0
    global _NOTE_SLOT
    _NOTE_SLOT = None
    for a in list(r1c0.iter('{%s}anchor' % WP)):
        if a is pic:
            continue
        txt = "".join(t.text or '' for t in a.iter(qn('w:t'))).strip()
        geom = a.find('.//{%s}prstGeom' % A)
        prst = geom.get('prst') if geom is not None else ''
        is_dot = prst == 'flowChartConnector'
        is_datelabel = bool(re.fullmatch(r'\d{2}\s*-?\s*\d{0,2}', txt.replace(' ', '')))
        is_note = txt.lower().startswith('note:') or 'referenced chart' in txt.lower()
        if is_dot or is_datelabel or (drop_note and is_note):
            if is_note:
                # remember exactly where the note box sat: the rationale bullets take
                # over that slot, which is a position the template already renders well.
                ext = a.find('{%s}extent' % WP)
                _NOTE_SLOT = {
                    "x": int(a.find('{%s}positionH/{%s}posOffset' % (WP, WP)).text),
                    "y": int(a.find('{%s}positionV/{%s}posOffset' % (WP, WP)).text),
                    "cx": int(ext.get('cx')), "cy": int(ext.get('cy')),
                    "relH": a.find('{%s}positionH' % WP).get('relativeFrom'),
                    "relV": a.find('{%s}positionV' % WP).get('relativeFrom'),
                }
            # the anchor sits inside an AlternateContent / run wrapper — drop the run
            node = a
            while node is not None and node.tag != qn('w:r'):
                node = node.getparent()
            (node if node is not None else a).getparent().remove(node if node is not None else a)
            dropped += 1
    return dropped


_NOTE_SLOT = None


def quadrant_apply_highlight(doc, exec_t, spec):
    """Shade the whole quadrant the week's read sits in, instead of plotting a dot.

    The wash is composited INTO the map image rather than drawn as a floating shape.
    Floating shapes in this cell carry deep negative offsets that LibreOffice clamps
    (Word does not), so an overlay drifts off the intended panel when the document is
    converted. Baking it into the picture is renderer-proof and moves and scales with
    the map for free. `spec` = {quadrant, colour, alpha}."""
    if not spec:
        return
    name = str(spec.get("quadrant", "")).strip().lower()
    name = QUADRANT_ALIASES.get(name, name)
    box = QUADRANT_CELLS.get(name)
    if box is None:
        print("WARN: unknown quadrant %r — highlight skipped" % spec.get("quadrant"))
        return
    r1c0 = exec_t.findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    pic = _quadrant_picture_anchor(r1c0)
    if pic is None:
        print("WARN: no quadrant map picture found — highlight skipped")
        return
    blip = pic.find('.//{%s}blip' % A)
    rid = blip.get('{%s}embed' % R)
    part = doc.part.related_parts[rid]
    _bake_wash(part, box, spec)
    print("quadrant highlight baked into map image: %s" % name)


def _bake_wash(part, box, spec):
    from PIL import Image, ImageDraw
    im = Image.open(BytesIO(part.blob)).convert("RGBA")
    W, H = im.size
    x0, y0, x1, y1 = box
    rect = [int(W * x0), int(H * y0), int(W * x1), int(H * y1)]
    colour = (spec.get("colour") or "C00000").upper().lstrip('#')
    rgb = tuple(int(colour[i:i + 2], 16) for i in (0, 2, 4))
    a = int(round(255 * float(spec.get("alpha", 20)) / 100.0))

    wash = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(wash)
    d.rounded_rectangle(rect, radius=max(4, int(W * 0.012)),
                        fill=rgb + (a,), outline=rgb + (215,), width=max(2, int(W * 0.006)))
    out = Image.alpha_composite(im, wash).convert("RGB")
    buf = BytesIO()
    out.save(buf, format="PNG")
    part._blob = buf.getvalue()


# ---------- Chart slot placeholders (30 Jul 2026 standard, the Co-Op) ----------
# The chart cells used to hold only an "Insert <slot>" marker, so they reserved ONE
# LINE of height. The block then fitted a page while empty and overflowed the moment a
# real chart was pasted in. Each slot now carries a placeholder image at the exact size
# the final chart should be, so the page is laid out against the true geometry and
# swapping the placeholder for a same-size chart moves nothing.

_PH_CACHE = {}


def _placeholder_png(label, w_in, h_in, dpi=96):
    """A light dashed frame stating the slot name and the exact size to match."""
    key = (label, round(w_in, 3), round(h_in, 3))
    if key in _PH_CACHE:
        return _PH_CACHE[key]
    from PIL import Image, ImageDraw
    W, H = max(8, int(w_in * dpi)), max(8, int(h_in * dpi))
    im = Image.new("RGB", (W, H), "#FFFFFF")
    d = ImageDraw.Draw(im)
    dash, gap, inset, col = 9, 6, 3, "#B79AAA"
    for x in range(inset, W - inset, dash + gap):
        d.line([(x, inset), (min(x + dash, W - inset), inset)], fill=col, width=2)
        d.line([(x, H - inset), (min(x + dash, W - inset), H - inset)], fill=col, width=2)
    for y in range(inset, H - inset, dash + gap):
        d.line([(inset, y), (inset, min(y + dash, H - inset))], fill=col, width=2)
        d.line([(W - inset, y), (W - inset, min(y + dash, H - inset))], fill=col, width=2)
    t1 = f"Insert {label}"
    t2 = f'{w_in:.2f}" x {h_in:.2f}"'
    try:
        b1 = d.textbbox((0, 0), t1); b2 = d.textbbox((0, 0), t2)
    except Exception:
        b1 = b2 = (0, 0, 60, 10)
    d.text(((W - (b1[2] - b1[0])) / 2, H / 2 - 12), t1, fill="#7B2952")
    d.text(((W - (b2[2] - b2[0])) / 2, H / 2 + 2), t2, fill="#9C8090")
    path = os.path.join(tempfile.gettempdir(), f"mb_ph_{abs(hash(key))}.png")
    im.save(path)
    _PH_CACHE[key] = path
    return path


# ---------- Real chart insertion from ChartsThemes/ (13 Aug 2026, the Co-Op) ----------
# The Co-Op now uploads their weekly theme charts to ChartsThemes/ at the repo root, and the
# engine places them INTO the report at build time instead of leaving a dashed
# placeholder for a hand paste. Three rules keep the calibrated layout intact:
# (a) the chart is letterboxed onto a white canvas of EXACTLY the slot's measured
#     geometry (aspect kept, centred), so the inserted picture has the same wp:extent
#     as the placeholder it replaces and nothing on the page can reflow;
# (b) when a real chart lands, the "Insert <slot>" marker line is dropped — the chart
#     replaces the paste step, and a marker over a filled slot would read as an error;
# (c) a slot with no matching file falls back to the sized placeholder + marker exactly
#     as before, and the gap is printed for the manifest — never a silent null.
# File names are matched tolerantly (case, separators, doubled ".png.png", the
# currency_debasement_N / artficial_intelligence-N / Geopolitics_N / Illiquids_N
# spellings all resolve); names starting with "retired" and zero-byte files are skipped.

_CHART_ALIASES = {
    "fiscalchart": ("fiscalchart", "fiscal"),
    "monetary":    ("monetary",),
    "currency":    ("currencydebasement", "currency"),
    "energy":      ("energy",),
    "ai":          ("artificialintelligence", "artficialintelligence", "intelligence", "ai"),
    "geo":         ("geopolitics", "geo"),
    "domestic":    ("domestic",),
    "illiquid":    ("illiquids", "illiquid"),
}


def _norm_stem(name):
    s = name.lower()
    while s.endswith((".png", ".jpg", ".jpeg")):
        s = s.rsplit(".", 1)[0]
    return re.sub(r"[^a-z0-9]", "", s)


def _split_idx(s):
    m = re.match(r"^(.*?)(\d+)$", s)
    return (m.group(1), m.group(2).lstrip("0") or "0") if m else (s, None)


def index_chart_dir(source_dir):
    """(normalised base, index) -> path for every usable image in ChartsThemes/."""
    idx = {}
    if not source_dir:
        return idx
    if not os.path.isdir(source_dir):
        # engine may be invoked from anywhere; fall back to repo root = script's parent
        alt = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", source_dir)
        if os.path.isdir(alt):
            source_dir = alt
        else:
            return idx
    for f in sorted(os.listdir(source_dir)):
        p = os.path.join(source_dir, f)
        if not os.path.isfile(p) or os.path.getsize(p) == 0:
            continue
        if not f.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        stem = _norm_stem(f)
        if stem.startswith("retired"):
            continue
        base, num = _split_idx(stem)
        if num is None:
            continue
        idx.setdefault((base, num), p)
    return idx


def resolve_chart_image(slot, dir_index, overrides=None):
    """Source image for a slot: explicit `chart_images` override first, then the
    ChartsThemes index via the alias table, then a substring last resort. None = gap."""
    if overrides and overrides.get(slot):
        return overrides[slot]
    sbase, snum = _split_idx(_norm_stem(slot))
    snum = snum or "1"
    aliases = _CHART_ALIASES.get(sbase, (sbase,))
    for a in aliases:
        hit = dir_index.get((a, snum))
        if hit:
            return hit
    for (b, n), p in sorted(dir_index.items()):
        if n == snum and any(a in b for a in aliases):
            return p
    return None


_CHART_IMG_CACHE = {}


def _chart_png(src, w_in, h_in, dpi=150):
    """The source chart letterboxed onto white at EXACTLY the slot geometry."""
    key = (os.path.abspath(src), round(w_in, 3), round(h_in, 3))
    if key in _CHART_IMG_CACHE:
        return _CHART_IMG_CACHE[key]
    from PIL import Image
    W, H = max(8, int(round(w_in * dpi))), max(8, int(round(h_in * dpi)))
    im = Image.open(src).convert("RGBA")
    scale = min(W / im.width, H / im.height)
    nw, nh = max(1, int(im.width * scale)), max(1, int(im.height * scale))
    im = im.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), "#FFFFFF")
    canvas.paste(im, ((W - nw) // 2, (H - nh) // 2), im)
    path = os.path.join(tempfile.gettempdir(), f"mb_chart_{abs(hash(key))}.png")
    canvas.save(path)
    _CHART_IMG_CACHE[key] = path
    return path


def fill_chart_placeholders(doc, blk, slots, default, images=None):
    """Fill every 'Insert <slot>' cell of a block: the real chart from ChartsThemes/
    at the slot's exact measured geometry when one resolves, else the sized dashed
    placeholder (30 Jul 2026 behaviour, unchanged).

    `slots` maps slot name -> {"width_in", "height_in"}; `default` supplies either;
    `images` maps slot name -> source image path (resolved once in main()).
    Returns the list of (slot, w_in, h_in, source) filled, for the manifest."""
    if not default and not slots:
        return []
    filled = []
    seen = set()
    # match PER PARAGRAPH, not per cell: some blocks (Theme 6) carry both markers as two
    # paragraphs inside a single vertically merged cell.
    for p in list(blk.iter(qn('w:p'))):
        m = re.match(r'^Insert\s+([A-Za-z0-9_]+)\s*$', para_text(p).strip())
        if not m:
            continue
        slot = m.group(1)
        if slot in seen:          # merged cells repeat their content in the XML walk
            continue
        seen.add(slot)
        cfg = dict(default or {})
        cfg.update((slots or {}).get(slot, {}))
        w_in = float(cfg.get("width_in", 3.5))
        h_in = float(cfg.get("height_in", 2.2))
        src = (images or {}).get(slot)
        if src and os.path.isfile(src):
            png = _chart_png(src, w_in, h_in)
            source = os.path.basename(src)
        else:
            png = _placeholder_png(slot, w_in, h_in)
            source = "placeholder"
        ip = _inline_image_para(doc, png, width_emu=int(w_in * 914400), center=True)
        p.addnext(ip)
        # 6 Aug 2026 white-space discipline: the marker line and the frame each carried
        # default before/after spacing, so a two-slot block spent roughly a fifth of an
        # inch on gaps around images that are themselves fixed-size. Zeroing it is the
        # only way to buy height in a chart-bound block without touching a MEASURED slot
        # size, which must stay exactly what the Co-Op pastes in. This is what lets the
        # AI block, whose two slots reserve 4.64in, clear the 89.5% fill ceiling.
        _paras = (ip,) if source != "placeholder" else (p, ip)
        for _p in _paras:
            pPr = _p.find(qn('w:pPr'))
            if pPr is None:
                pPr = OxmlElement('w:pPr'); _p.insert(0, pPr)
            spc = pPr.find(qn('w:spacing'))
            if spc is None:
                spc = add_spacing_ordered(pPr)
            spc.set(qn('w:before'), '0'); spc.set(qn('w:after'), '0')
            spc.set(qn('w:line'), '240'); spc.set(qn('w:lineRule'), 'auto')
        if source != "placeholder":
            # the chart replaces the paste step: drop the "Insert <slot>" marker line
            p.getparent().remove(p)
        filled.append((slot, w_in, h_in, source))
    return filled


def quadrant_inline_layout(doc, exec_t, C):
    """30 Jul 2026 v2 (the Co-Op): the quadrant map becomes an INLINE image in a third
    column of the Weekly Direction table, with the 'Why this quadrant' bullets styled
    directly beneath it in the same cell. Kills the floating-anchor machinery for this
    path entirely: floats with deep negative offsets render differently across Word and
    LibreOffice, while an inline image in a table cell is deterministic everywhere and
    the rationale can never drift away from the map it explains."""
    # the nested Weekly Direction / Influencing Factors table
    nested = None
    for nt in exec_t.iter(qn('w:tbl')):
        if nt is exec_t:
            continue
        hr = nt.find(qn('w:tr'))
        if hr is not None and "Weekly Direction" in para_text(hr):
            nested = nt
            break
    if nested is None:
        print("WARN: no Weekly Direction table — inline layout skipped")
        return False

    # v6 TEMPLATE MODE (30 Jul 2026): the template already carries the 3-column
    # direction table with the clean map INLINE in column 3. Bake this week's wash
    # into that image and write the rationale under it; no restructuring.
    grid = nested.find(qn('w:tblGrid'))
    if grid is not None and len(grid.findall(qn('w:gridCol'))) >= 3:
        trs = nested.findall(qn('w:tr'))
        qc = trs[1].findall(qn('w:tc'))[-1]
        blip = qc.find('.//{%s}blip' % A)
        if blip is not None:
            spec = C.get("quadrant_highlight") or {}
            nm = QUADRANT_ALIASES.get(str(spec.get("quadrant", "")).strip().lower(),
                                      str(spec.get("quadrant", "")).strip().lower())
            box = QUADRANT_CELLS.get(nm)
            if box:
                rid = blip.get('{%s}embed' % R)
                _bake_wash(doc.part.related_parts[rid], box, spec)
                print("v6 exec: highlight baked into inline map (%s)" % nm)
            # rationale under the image (any stale ones were stripped at template build)
            sz = str(C.get("quadrant_rationale_sz", 14))
            heading = C.get("quadrant_rationale_heading", "Why this quadrant")
            anchor = None
            for q in qc.findall(qn('w:p')):
                if q.find('.//' + qn('w:drawing')) is not None:
                    anchor = q
            if anchor is not None and C.get("quadrant_rationale"):
                hp = etree.fromstring(
                    f'<w:p xmlns:w="{WNS}"><w:pPr><w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="7B2952"/></w:pBdr>'
                    f'<w:spacing w:before="60" w:after="30" w:line="240" w:lineRule="auto"/>'
                    f'<w:ind w:left="120" w:right="60"/></w:pPr>'
                    f'<w:r><w:rPr><w:b/><w:color w:val="7B2952"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
                    f'<w:t xml:space="preserve">{_su.escape(heading)}</w:t></w:r></w:p>')
                anchor.addnext(hp); anchor = hp
                for it in C["quadrant_rationale"]:
                    bp = etree.fromstring(
                        f'<w:p xmlns:w="{WNS}"><w:pPr><w:spacing w:before="0" w:after="35" w:line="230" w:lineRule="auto"/>'
                        f'<w:ind w:left="290" w:right="60" w:hanging="170"/></w:pPr>'
                        f'<w:r><w:rPr><w:b/><w:color w:val="7B2952"/><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
                        f'<w:t xml:space="preserve">▪  </w:t></w:r>'
                        f'<w:r><w:rPr><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
                        f'<w:t xml:space="preserve">{_su.escape(it)}</w:t></w:r></w:p>')
                    anchor.addnext(bp); anchor = bp
            return "v6"

    r1c0 = exec_t.findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    pic = _quadrant_picture_anchor(r1c0)
    if pic is None:
        print("WARN: no quadrant map picture — inline layout skipped")
        return False
    blip = pic.find('.//{%s}blip' % A)
    rid = blip.get('{%s}embed' % R)

    # drop the floating map run
    node = pic
    while node is not None and node.tag != qn('w:r'):
        node = node.getparent()
    if node is not None:
        node.getparent().remove(node)

    # widen the nested table to the full block width and add the third column
    total_w = int(C.get("exec_direction_total_twips", 10900))
    col3_w = int(C.get("exec_quadrant_col_twips", 5250))
    grid = nested.find(qn('w:tblGrid'))
    gcs = grid.findall(qn('w:gridCol'))
    old = [int(g.get(qn('w:w'))) for g in gcs]
    left_total = total_w - col3_w
    scale = left_total / max(1, sum(old))
    for g, w in zip(gcs, old):
        g.set(qn('w:w'), str(int(w * scale)))
    g3 = OxmlElement('w:gridCol'); g3.set(qn('w:w'), str(col3_w)); grid.append(g3)
    tw = nested.find(qn('w:tblPr'))
    if tw is not None:
        we = tw.find(qn('w:tblW'))
        if we is not None:
            we.set(qn('w:w'), str(total_w)); we.set(qn('w:type'), 'dxa')

    trs = nested.findall(qn('w:tr'))
    # header row: clone an existing header cell so the band stays visually continuous
    hdr_tc = trs[0].findall(qn('w:tc'))[-1]
    new_hdr = copy.deepcopy(hdr_tc)
    tcW = new_hdr.find(qn('w:tcPr')).find(qn('w:tcW'))
    if tcW is not None:
        tcW.set(qn('w:w'), str(col3_w))
    for p in list(new_hdr.findall(qn('w:p')))[1:]:
        new_hdr.remove(p)
    hp = new_hdr.find(qn('w:p'))
    for r_ in list(hp.findall(qn('w:r')))[1:]:
        hp.remove(r_)
    fr = hp.find(qn('w:r'))
    if fr is not None:
        for t_ in fr.findall(qn('w:t')):
            t_.text = C.get("exec_quadrant_header", "Current Environment")
    trs[0].append(new_hdr)

    # content cell: centred inline map + styled rationale panel beneath it
    img_w_in = float(C.get("quadrant_img_width_in", 3.30))
    img_w = int(img_w_in * 914400)
    img_h = int(img_w * 433 / 511)          # template map aspect
    _id = _next_id()
    img_p = (f'<w:p><w:pPr><w:spacing w:before="40" w:after="30" w:line="240" w:lineRule="auto"/>'
             f'<w:jc w:val="center"/></w:pPr><w:r><w:drawing>'
             f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
             f'<wp:extent cx="{img_w}" cy="{img_h}"/><wp:effectExtent l="0" t="0" r="0" b="0"/>'
             f'<wp:docPr id="{_id}" name="Risk Quadrant"/><wp:cNvGraphicFramePr/>'
             f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
             f'<pic:pic><pic:nvPicPr><pic:cNvPr id="{_id}" name="Risk Quadrant"/><pic:cNvPicPr/></pic:nvPicPr>'
             f'<pic:blipFill><a:blip r:embed="{rid}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
             f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{img_w}" cy="{img_h}"/></a:xfrm>'
             f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr>'
             f'</pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')
    sz = str(C.get("quadrant_rationale_sz", 14))
    heading = C.get("quadrant_rationale_heading", "Why this quadrant")
    rat = (f'<w:p><w:pPr><w:pBdr><w:top w:val="single" w:sz="4" w:space="4" w:color="7B2952"/></w:pBdr>'
           f'<w:spacing w:before="60" w:after="30" w:line="240" w:lineRule="auto"/>'
           f'<w:ind w:left="120" w:right="60"/></w:pPr>'
           f'<w:r><w:rPr><w:b/><w:color w:val="7B2952"/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
           f'<w:t xml:space="preserve">{_su.escape(heading)}</w:t></w:r></w:p>')
    for it in (C.get("quadrant_rationale") or []):
        rat += (f'<w:p><w:pPr><w:spacing w:before="0" w:after="40" w:line="235" w:lineRule="auto"/>'
                f'<w:ind w:left="290" w:right="60" w:hanging="170"/></w:pPr>'
                f'<w:r><w:rPr><w:b/><w:color w:val="7B2952"/><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
                f'<w:t xml:space="preserve">▪  </w:t></w:r>'
                f'<w:r><w:rPr><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
                f'<w:t xml:space="preserve">{_su.escape(it)}</w:t></w:r></w:p>')
    body_tc = etree.fromstring(
        f'<w:tc xmlns:w="{WNS}" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
        f'xmlns:a="{A}" xmlns:pic="{PIC}" xmlns:r="{R}">'
        f'<w:tcPr><w:tcW w:w="{col3_w}" w:type="dxa"/>'
        f'<w:tcMar><w:top w:w="20" w:type="dxa"/><w:left w:w="60" w:type="dxa"/>'
        f'<w:bottom w:w="20" w:type="dxa"/><w:right w:w="60" w:type="dxa"/></w:tcMar>'
        f'<w:vAlign w:val="top"/></w:tcPr>{img_p}{rat}</w:tc>')
    trs[1].append(body_tc)
    return True


def fill_quadrant_rationale(exec_t, items, heading="Why this quadrant", font_half_pt="15"):
    """30 Jul 2026: the bullets that replace the removed AIP note box. They say WHY the
    week sits in the highlighted quadrant, and are deliberately distinct from the three
    Influencing Factors (which carry the week's general evidence).

    Rendered as a floating text box in the space the note box vacated, directly under
    the map, so it uses the empty right-hand band instead of lengthening the narrow
    Weekly Direction column (which pushed the Status Dashboard off page 1). Call AFTER
    scale/shift/behind so the geometry is read off the final picture position."""
    if not items:
        return
    r1c0 = exec_t.findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    pic = _quadrant_picture_anchor(r1c0)
    if pic is None:
        print("WARN: no quadrant map picture — rationale box skipped")
        return
    # Find the nested Weekly Direction / Influencing Factors table and append a row
    # that spans both its columns. In-flow, so it renders identically everywhere.
    nested = None
    for nt in exec_t.iter(qn('w:tbl')):
        if nt is exec_t:
            continue
        hr = nt.find(qn('w:tr'))
        if hr is not None and "Weekly Direction" in para_text(hr):
            nested = nt
            break
    if nested is None:
        print("WARN: no Weekly Direction table — quadrant rationale skipped")
        return
    grid = nested.find(qn('w:tblGrid'))
    ncols = len(grid.findall(qn('w:gridCol'))) if grid is not None else 2
    total = sum(int(gc.get(qn('w:w'))) for gc in grid.findall(qn('w:gridCol'))) if grid is not None else 4000

    paras = (f'<w:p><w:pPr><w:spacing w:before="20" w:after="30" w:line="240" w:lineRule="auto"/></w:pPr>'
             f'<w:r><w:rPr><w:b/><w:color w:val="7B2952"/><w:sz w:val="17"/><w:szCs w:val="17"/></w:rPr>'
             f'<w:t xml:space="preserve">{_su.escape(heading)}</w:t></w:r></w:p>')
    for it in items:
        paras += (f'<w:p><w:pPr><w:spacing w:before="0" w:after="30" w:line="230" w:lineRule="auto"/>'
                  f'<w:ind w:left="160" w:hanging="160"/></w:pPr>'
                  f'<w:r><w:rPr><w:color w:val="7B2952"/><w:sz w:val="{font_half_pt}"/>'
                  f'<w:szCs w:val="{font_half_pt}"/></w:rPr><w:t xml:space="preserve">•  </w:t></w:r>'
                  f'<w:r><w:rPr><w:sz w:val="{font_half_pt}"/><w:szCs w:val="{font_half_pt}"/></w:rPr>'
                  f'<w:t xml:space="preserve">{_su.escape(it)}</w:t></w:r></w:p>')

    tr = etree.fromstring(
        f'<w:tr xmlns:w="{WNS}"><w:tc><w:tcPr><w:tcW w:w="{total}" w:type="dxa"/>'
        f'<w:gridSpan w:val="{ncols}"/>'
        f'<w:tcMar><w:top w:w="40" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
        f'<w:bottom w:w="40" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tcMar>'
        f'<w:vAlign w:val="top"/></w:tcPr>{paras}</w:tc></w:tr>')
    nested.append(tr)


def drop_exec_key_developments(exec_t):
    """30 Jul 2026 (the Co-Op): the exec 'Key Developments | Implication for Themes' page
    was a restatement of the theme blocks. Remove the header row and every row after
    it, so the Executive Summary ends at the Status Dashboard."""
    trs = exec_t.findall(qn('w:tr'))
    hi = next((i for i, tr in enumerate(trs)
               if para_text(tr).strip().startswith("Key Developments")), None)
    if hi is None:
        return 0
    for tr in trs[hi:]:
        tr.getparent().remove(tr)
    return len(trs) - hi


def shift_exec_quadrant(exec_t, dy):
    """9 Jul 2026: lift the whole floating quadrant cluster (pictures, markers, arrow,
    legend) UP by dy EMU so the Status Dashboard rows fit on page 1. Opt-in via the
    content's `quadrant_shift_up_emu`; 0 leaves the transplanted position untouched."""
    if not dy:
        return
    r1c0 = exec_t.findall(qn('w:tr'))[1].findall(qn('w:tc'))[0]
    for anch in r1c0.iter('{%s}anchor' % WP):
        pv = anch.find('{%s}positionV' % WP)
        if pv is None:
            continue
        off = pv.find('{%s}posOffset' % WP)
        if off is None or not (off.text or '').lstrip('-').isdigit():
            continue
        off.text = str(int(off.text) - int(dy))

# ---------- references (top-level paragraphs; tiered since v3) ----------
def _make_bold(p):
    for r in p.findall(qn('w:r')):
        rPr = r.find(qn('w:rPr'))
        if rPr is None:
            rPr = OxmlElement('w:rPr'); r.insert(0, rPr)
        if rPr.find(qn('w:b')) is None:
            rPr.append(OxmlElement('w:b'))

def _unbullet(p):
    pPr = p.find(qn('w:pPr'))
    if pPr is not None:
        np = pPr.find(qn('w:numPr'))
        if np is not None:
            pPr.remove(np)

def fill_references(doc, intro, refs):
    body = doc.element.body
    ps = body.findall(qn('w:p'))
    intro_p = None
    ref_ps = []
    for p in ps:
        txt = para_text(p)
        if '[[Only sources' in txt:
            intro_p = p
        elif '[[Source name' in txt:
            ref_ps.append(p)
    if intro_p is not None:
        set_para_text(intro_p, intro)
    if not ref_ps:
        return
    template_p = ref_ps[0]
    anchor = [ref_ps[-1]]
    def add(text, bold=False, unbullet=False):
        newp = copy.deepcopy(template_p)
        anchor[0].addnext(newp)
        anchor[0] = newp
        set_para_text(newp, text)
        if bold: _make_bold(newp)
        if unbullet: _unbullet(newp)
    if refs and isinstance(refs[0], dict):          # grouped (by topic since v3.1; by tier in v3)
        for grp in refs:
            if grp.get("items"):
                add(grp.get("topic") or grp.get("tier"), bold=True, unbullet=True)
                for it in grp["items"]:
                    add(it)
    else:                                            # legacy flat list
        for r in refs:
            add(r)
    for p in ref_ps:
        p.getparent().remove(p)

# ---------- main ----------
# ---------- new sections (9 Jul 2026): light-scoring transparency + light history ----------
import xml.sax.saxutils as _su

_LIGHT_COL = {"escalating": "92D050", "held": "FFC000",
              "deescalating": "EE0000", "de-escalating": "EE0000"}

def _light_fill(word):
    return _LIGHT_COL.get((word or "").strip().lower(), None)

def _light_textcol(word):
    return "FFFFFF" if (word or "").strip().lower().startswith("de") else "000000"

def _p_xml(text, color="000000", bold=False, size="20", align="left"):
    b = '<w:b/>' if bold else ''
    return (f'<w:p><w:pPr>'
            f'<w:spacing w:before="10" w:after="10" w:line="228" w:lineRule="auto"/>'
            f'<w:jc w:val="{align}"/></w:pPr>'
            f'<w:r><w:rPr>{b}<w:color w:val="{color}"/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
            f'<w:t xml:space="preserve">{_su.escape(text)}</w:t></w:r></w:p>')

def _tc_xml(w, paras_xml, fill=None, span=None, valign="center"):
    shd = f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else ''
    gs = f'<w:gridSpan w:val="{span}"/>' if span else ''
    return (f'<w:tc><w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>{gs}{shd}'
            f'<w:tcMar><w:top w:w="25" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
            f'<w:bottom w:w="25" w:type="dxa"/><w:right w:w="110" w:type="dxa"/></w:tcMar>'
            f'<w:vAlign w:val="{valign}"/></w:tcPr>{paras_xml or "<w:p/>"}</w:tc>')

def _header_row_xml(title, asof, total_w, ncols):
    inner = (_p_xml(title, color="FFFFFF", bold=True, size="32", align="center")
             + _p_xml(f"(As of {asof})", color="FFFFFF", bold=True, size="20", align="center"))
    return f'<w:tr>{_tc_xml(total_w, inner, fill="7B2952", span=ncols)}</w:tr>'

def _no_split_rows(tbl):
    """30 Jul 2026: mark every row cantSplit so a row moves whole to the next page
    instead of straddling; Word and LibreOffice then break at the same row edges."""
    for tr in tbl.findall(qn('w:tr')):
        trPr = tr.find(qn('w:trPr'))
        if trPr is None:
            trPr = OxmlElement('w:trPr'); tr.insert(0, trPr)
        if trPr.find(qn('w:cantSplit')) is None:
            trPr.append(OxmlElement('w:cantSplit'))


def _block_tbl_xml(grid_widths, rows_xml):
    borders = "".join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="7B2952"/>'
                      for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in grid_widths)
    total = sum(grid_widths)
    return (f'<w:tbl xmlns:w="{WNS}"><w:tblPr><w:tblW w:w="{total}" w:type="dxa"/><w:jc w:val="left"/>'
            f'<w:tblBorders>{borders}</w:tblBorders><w:tblLayout w:type="fixed"/></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>{rows_xml}</w:tbl>')

def _cells_xml(w, val, size="18"):
    val = val if isinstance(val, list) else [val]
    return _tc_xml(w, "".join(_p_xml(x, size=size) for x in val), valign="top")

def build_light_scoring_block(asof, entries, sz="17"):
    """Explicit per-theme light scoring, SPLIT into columns (9 Jul 2026) so it reads
    cleanly instead of one bundled paragraph: Theme | Light | Supports | Against | Net.

    6 Aug 2026 geometry fix: the Theme and Net columns were wide enough to wrap their
    own labels onto three lines while the two evidence columns wrapped every bullet,
    which pushed the sixth row onto a second page no matter how tight the prose got.
    Widths rebalanced toward the evidence columns and the body set at 8.5pt, so the
    block holds all six themes on ONE page as the fill gauge requires. Tune with
    `light_scoring_sz` in the content JSON if a week's scoring runs unusually long."""
    widths = [1180, 1180, 3550, 3300, 1828]         # sum 11038 (block width)
    total = sum(widths)
    rows = _header_row_xml("Light Scoring and Developments", asof, total, len(widths))
    sub = (_tc_xml(widths[0], _p_xml("Theme", color="7B2952", bold=True, size=sz), fill="EFE7EB")
           + _tc_xml(widths[1], _p_xml("Light", color="7B2952", bold=True, align="center", size=sz), fill="EFE7EB")
           + _tc_xml(widths[2], _p_xml("Supports (more of the theme)", color="4A7A30", bold=True, size=sz), fill="EAF3E2")
           + _tc_xml(widths[3], _p_xml("Against (less of the theme)", color="9A2B2B", bold=True, size=sz), fill="F6E4E4")
           + _tc_xml(widths[4], _p_xml("Net read", color="7B2952", bold=True, size=sz), fill="EFE7EB"))
    rows += f'<w:tr>{sub}</w:tr>'
    for e in entries:
        cells = (_tc_xml(widths[0], _p_xml(e["theme"], bold=True, size=sz), valign="top")
                 + _tc_xml(widths[1], _p_xml(e["light"], color=_light_textcol(e["light"]), bold=True,
                                             align="center", size=sz),
                           fill=_light_fill(e["light"]))
                 + _cells_xml(widths[2], e.get("supports", ""), size=sz)
                 + _cells_xml(widths[3], e.get("against", ""), size=sz)
                 + _cells_xml(widths[4], e.get("net", ""), size=sz))
        rows += f'<w:tr>{cells}</w:tr>'
    _t = etree.fromstring(_block_tbl_xml(widths, rows)); _no_split_rows(_t); return _t

# ---------- Illiquids block (NEW, 6 Aug 2026, per the Co-Op; framework v3 same day) ----------
# A full page on private / unlisted markets, sitting AFTER Theme 6 and BEFORE Light
# Scoring, written in the THEME BLOCK grammar. It deliberately stays OUTSIDE the lights
# system: no traffic light, no exec status row, no Light Scoring or Light History entry.
# v3 (6 Aug 2026, the Co-Op): the Buy / Hold / Sell per sleeve is RETIRED. The page now
# assesses the asset class through FOUR PRIMARY CATEGORIES, each carrying a short
# directional read in the strip where a theme carries its light:
#   Performance — how illiquids are doing against public alternatives, literally returns
#   Valuations  — whether illiquids are getting more expensive or cheaper, and the tells
#   Leverage    — how much is being taken, what moves the needle, how it is measured
#   Dry powder  — capital demand: abundant money chasing deals, or no one willing to buy
# The read cell is coloured by TONE, the same warm / cool / grey palette as the regime
# signs (Inflation and Growth Read), NOT the light palette: these are directions of a
# metric, not good-versus-bad and not more-or-less of a theme.
ILLIQUID_CATEGORIES = ["Performance", "Valuations", "Leverage", "Dry powder"]
_TONE_COL = {"warm": ("F4B183", "000000"),     # rising / more / richer
             "cool": ("9DC3E6", "000000"),     # falling / less / cheaper
             "neutral": ("D9D9D9", "000000"),  # mixed or two-sided
             "mixed": ("D9D9D9", "000000")}
# legacy palette, kept only so an old content file still renders
_CALL_COL = {"buy": ("92D050", "000000"),
             "hold": ("FFC000", "000000"),
             "sell": ("EE0000", "FFFFFF")}


def _call_style(entry):
    """Colour a strip cell. Preferred: an explicit `tone` (warm / cool / neutral) using
    the regime-sign palette. Legacy: a Buy / Hold / Sell call word. Unknown goes grey."""
    if isinstance(entry, dict):
        tone = (entry.get("tone") or "").strip().lower()
        if tone in _TONE_COL:
            return _TONE_COL[tone]
        word = (entry.get("read") or entry.get("call") or "")
    else:
        word = entry or ""
    key = word.strip().lower().split()[0] if word.strip() else ""
    return _CALL_COL.get(key, ("D9D9D9", "000000"))


def _label_p(text, size="20"):
    """A theme block's bold burgundy section label ('What changed this week', etc.)."""
    return _p_xml(text, color="7B2952", bold=True, size=size)


def _bullet_p_xml(text, size="20"):
    """A justified 10pt bullet matching the theme blocks' 'What changed' bullets."""
    return (f'<w:p><w:pPr>'
            f'<w:spacing w:before="20" w:after="40" w:line="228" w:lineRule="auto"/>'
            f'<w:ind w:left="230" w:hanging="170"/><w:jc w:val="both"/></w:pPr>'
            f'<w:r><w:rPr><w:color w:val="7B2952"/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
            f'<w:t xml:space="preserve">▪  </w:t></w:r>'
            f'<w:r><w:rPr><w:color w:val="000000"/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
            f'<w:t xml:space="preserve">{_su.escape(text)}</w:t></w:r></w:p>')


def _bullets_cell(w, items, label=None, extra=""):
    inner = (_label_p(label) if label else "")
    inner += "".join(_bullet_p_xml(x) for x in (items or []))
    return _tc_xml(w, inner + extra, valign="top")


def _signal_strip_xml(signals, total):
    """The framework strip that sits where a theme block carries its light: category
    names over colour-filled directional reads (Performance / Valuations / Leverage /
    Dry powder). Two nested rows, borderless so it reads as part of the Status row
    rather than as a table of its own."""
    n = max(1, len(signals))
    w = total // n
    names = "".join(_tc_xml(w, _p_xml(s.get("category", s.get("sleeve", "")),
                                      color="7B2952", bold=True,
                                      size="16", align="center"), fill="EFE7EB")
                    for s in signals)
    calls = ""
    for s in signals:
        fill, txt = _call_style(s)
        word = s.get("read", s.get("call", ""))
        body = _p_xml(word, color=txt, bold=True, size="22", align="center")
        if s.get("note"):
            body += _p_xml(s["note"], color=txt, size="13", align="center")
        calls += _tc_xml(w, body, fill=fill)
    borders = "".join(f'<w:{s} w:val="single" w:sz="4" w:space="0" w:color="FFFFFF"/>'
                      for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for _ in signals)
    return (f'<w:tbl><w:tblPr><w:tblW w:w="{w*n}" w:type="dxa"/><w:jc w:val="left"/>'
            f'<w:tblBorders>{borders}</w:tblBorders><w:tblLayout w:type="fixed"/></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>'
            f'<w:tr>{names}</w:tr><w:tr>{calls}</w:tr></w:tbl>'
            # a table must be followed by a paragraph; keep it zero-height so the strip
            # sits tight against the deciding sentence instead of leaving a white band
            f'<w:p><w:pPr><w:spacing w:before="0" w:after="0" w:line="20" '
            f'w:lineRule="exact"/></w:pPr></w:p>')


def build_illiquids_block(doc, asof, illiquids, slots=None, default=None):
    """Illiquid Assets (6 Aug 2026 v4, per the Co-Op).

    Layout: header → [chart column | 'What changed this week'] → a 2x2 FRAMEWORK GRID.
    'What changed this week' carries the window's most important PRIVATE EQUITY news,
    from its own Sonnet 5 sweep. The grid replaces the keydev / implication / watch
    rows entirely: four cells in canonical order — Performance | Valuations over
    Leverage | Dry powder — each self-contained: the category header, a short bold
    directional read, then the evidence, the implication and what to watch for that
    category as bullets. The v3 Signals strip and status sentence are RETIRED: a strip
    of one-word reads proved too hard to keep consistent week to week, while a cell of
    prose per category is stable. The block still sits OUTSIDE the lights system.

    Fill from `illiquids`:
        {"title", "chart_slots"[], "developments"[],
         "framework": [{"category", "read", "points": [...]}, x4 canonical order]}
    """
    widths = [5519, 5519]                                # sum 11038 (block width)
    total = sum(widths)
    title = illiquids.get("title", "Allocation Insights - Illiquid Assets")
    rows = _header_row_xml(title, asof, total, len(widths))

    # R1 — chart column left, 'What changed this week' (the PE news sweep) right
    chart_cell = ""
    for slot in (illiquids.get("chart_slots") or ["illiquid_1", "illiquid_2"]):
        chart_cell += _p_xml(f"Insert {slot}", color="7B2952", bold=True, align="center")
    rows += ('<w:tr>' + _tc_xml(widths[0], chart_cell, valign="top")
             + _bullets_cell(widths[1], illiquids.get("developments"),
                             label="What changed this week") + '</w:tr>')

    # R2 + R3 — the framework grid: Performance | Valuations / Leverage | Dry powder
    fw = list(illiquids.get("framework") or [])
    if fw:
        def cell(e, w):
            inner = _label_p(e.get("category", ""))
            if e.get("read"):
                inner += _p_xml(e["read"], bold=True)
            inner += "".join(_bullet_p_xml(x) for x in (e.get("points") or []))
            return _tc_xml(w, inner, valign="top")
        for i in range(0, len(fw), 2):
            pair = fw[i:i + 2]
            if len(pair) == 1:
                rows += '<w:tr>' + _tc_xml(total, cell(pair[0], total), span=2) + '</w:tr>'
            else:
                rows += ('<w:tr>' + cell(pair[0], widths[0])
                         + cell(pair[1], widths[1]) + '</w:tr>')

    _t = etree.fromstring(_block_tbl_xml(widths, rows)); _no_split_rows(_t)
    return _t


def check_illiquids(C):
    """The Illiquids block sits outside the lights system by design (6 Aug 2026,
    the Co-Op). Warn loudly if it ever leaks into the light machinery, and if a call
    is not one of the three permitted words."""
    ill = C.get("illiquids")
    if not ill:
        return
    if ill.get("signals"):
        print("WARN: illiquids `signals` strip is RETIRED (6 Aug 2026 v4) — the framework "
              "lives in the four grid cells; the strip will not render")
    fw = ill.get("framework") or []
    if not fw:
        print("WARN: illiquids has no `framework` — the four category cells "
              "(Performance / Valuations / Leverage / Dry powder) are the block's core")
    cats = [(e.get("category") or "").strip() for e in fw]
    if cats and cats != ILLIQUID_CATEGORIES:
        print(f"WARN: illiquids categories {cats} != canonical {ILLIQUID_CATEGORIES} "
              f"(fixed order: Performance, Valuations, Leverage, Dry powder)")
    for e in fw:
        if not e.get("points"):
            print(f"WARN: illiquids category {e.get('category')!r} has no content points")
        w = (e.get("read") or "").strip().lower().split()[0] if (e.get("read") or "").strip() else ""
        if w in ("buy", "hold", "sell"):
            print(f"WARN: illiquids read {w!r} — Buy/Hold/Sell is retired; describe the direction instead")
        if w in ("escalating", "deescalating"):
            print(f"WARN: illiquids read {w!r} is a light word — the block is outside the lights system")
    if not ill.get("developments"):
        print("WARN: illiquids has no `developments` — 'What changed this week' carries "
              "the window's most important private equity news from its own Sonnet sweep")
    names = {s.lower() for s in (C.get("light_history") or {}).get("themes", [])}
    if any("illiquid" in n for n in names):
        print("WARN: 'Illiquids' appears in light_history — it is outside the lights "
              "system by design; remove it")
    for e in C.get("light_scoring") or []:
        if "illiquid" in (e.get("theme") or "").lower():
            print("WARN: 'Illiquids' appears in light_scoring — it carries no light; remove it")
    if len(C.get("status_dashboard") or []) != 6:
        print("WARN: status_dashboard should still be SIX rows — Illiquids does not get an exec row")


# 30 Jul 2026 (the Co-Op): signs are BINARY, + or - only. The pair IS the quadrant
# coordinate, so a third state cannot exist: (+,+) Inflation, (+,-) Stagflation,
# (-,+) Productivity Boost, (-,-) Deflation. Nuance (held vs rising) lives in the
# label and the prose, never in the sign.
_REGIME_SIGN = {
    "+": ("F4B183", "000000"),      # inflation firmer / growth firmer than baseline
    "-": ("9DC3E6", "000000"),      # softer than baseline
    "−": ("9DC3E6", "000000"),  # unicode minus
}

QUAD_FROM_SIGNS = {("+", "+"): "Inflation", ("+", "-"): "Stagflation",
                   ("-", "+"): "Productivity Boost", ("-", "-"): "Deflation"}


def check_signs_vs_quadrant(C):
    """The regime signs, the page-1 chips and the highlighted quadrant are three
    renderings of ONE call. Warn loudly on any mismatch."""
    rows = (C.get("regime_table") or {}).get("rows", [])
    signs = {r.get("factor", "").lower(): r.get("sign", "").replace("−", "-") for r in rows}
    pair = (signs.get("inflation"), signs.get("growth"))
    want = QUAD_FROM_SIGNS.get(pair)
    have = (C.get("quadrant_highlight") or {}).get("quadrant")
    if want and have and want.lower() != str(have).lower():
        print(f"WARN: regime signs {pair} imply {want} but quadrant_highlight is {have} — fix one")
    for d in C.get("direction_signs") or []:
        f = d.get("factor", "").lower()
        if f in signs and d.get("sign", "").replace("−", "-") != signs[f]:
            print(f"WARN: page-1 chip for {d.get('factor')} is {d.get('sign')} "
                  f"but the regime table says {signs[f]} — fix one")
    hist = (C.get("regime_history") or {}).get("weeks", [])
    for wk in hist:
        for k in ("inflation", "growth"):
            v = str(wk.get(k, "")).replace("−", "-")
            if v not in ("+", "-"):
                print(f"WARN: regime_history {wk.get('date')} {k} is {v!r} — signs are binary, + or - only")


def _regime_sign_style(sign):
    key = (sign or "").strip().replace("−", "-").replace("−", "-")
    return _REGIME_SIGN.get(key, ("D9D9D9", "000000"))


def drop_empty_fullwidth_rows(block_tbl):
    """30 Jul 2026: delete rows whose every cell is empty (no text, no image, no nested
    table, no vertical-merge continuation). The Monetary appendix carries an empty
    keydev row by design and it rendered as a white band."""
    dropped = 0
    for tr in list(block_tbl.findall(qn('w:tr'))):
        tcs = tr.findall(qn('w:tc'))
        if not tcs:
            continue
        killable = True
        for tc in tcs:
            if para_text_all(tc).strip():
                killable = False; break
            if tc.find('.//' + qn('w:drawing')) is not None or tc.find(qn('w:tbl')) is not None:
                killable = False; break
            tcPr = tc.find(qn('w:tcPr'))
            if tcPr is not None and tcPr.find(qn('w:vMerge')) is not None:
                killable = False; break
        if killable:
            tr.getparent().remove(tr); dropped += 1
    return dropped


def fill_direction_signs(exec_t, signs):
    """30 Jul 2026: compact sign chips under the Weekly Direction sentence, mirroring
    the Inflation and Growth Read at the back, so the direction cell carries content
    instead of white space. `signs` = [{factor, sign, label}, ...]."""
    if not signs:
        return
    host = None
    for p in exec_t.iter(qn('w:p')):
        # runs AFTER the direction placeholder is filled: find the cell by its content
        if "inflation" in para_text(p).lower() and "growth" in para_text(p).lower():
            node = p
            while node is not None and node.tag != qn('w:tc'):
                node = node.getparent()
            if node is not None and "Weekly Direction" not in para_text_all(node):
                host = (node, p)
                break
    if host is None:
        print("WARN: direction cell not found — sign chips skipped")
        return
    tc, anchor = host
    for s in signs:
        fill, txtcol = _regime_sign_style(s.get("sign"))
        xml = (f'<w:p xmlns:w="{WNS}"><w:pPr><w:spacing w:before="70" w:after="0" '
               f'w:line="240" w:lineRule="auto"/><w:jc w:val="center"/></w:pPr>'
               f'<w:r><w:rPr><w:b/><w:sz w:val="18"/><w:szCs w:val="18"/></w:rPr>'
               f'<w:t xml:space="preserve">{_su.escape(s["factor"])}  </w:t></w:r>'
               f'<w:r><w:rPr><w:b/><w:sz w:val="24"/><w:szCs w:val="24"/>'
               f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/></w:rPr>'
               f'<w:t xml:space="preserve"> {_su.escape(s["sign"])} </w:t></w:r>'
               f'<w:r><w:rPr><w:i/><w:sz w:val="16"/><w:szCs w:val="16"/>'
               f'<w:color w:val="595959"/></w:rPr>'
               f'<w:t xml:space="preserve">  {_su.escape(s.get("label", ""))}</w:t></w:r></w:p>')
        np_ = etree.fromstring(xml)
        anchor.addnext(np_); anchor = np_


def build_regime_history_block(doc, asof, hist, quad_hist=None, quad_png=None):
    """30 Jul 2026 (the Co-Op): companion strip under the Inflation and Growth Read.
    (a) sign history, the weekly + / = / - for each factor across all tracked weeks,
    the regime analogue of the theme light history; (b) quadrant residency, a count of
    weekly reads per AIP quadrant with a bar chart, agent-maintained from the
    quadrant-highlight standard onward."""
    total = 11038
    weeks = hist.get("weeks", [])
    label_w = 1600
    wk_w = (total - label_w) // max(1, len(weeks))
    widths = [label_w] + [wk_w] * len(weeks)
    ttl = sum(widths)
    rows = ''
    sub = _tc_xml(label_w, _p_xml("Sign history", color="7B2952", bold=True), fill="EFE7EB")
    for wk in weeks:
        sub += _tc_xml(wk_w, _p_xml(wk["date"], color="7B2952", bold=True, size="16", align="center"), fill="EFE7EB")
    rows += f'<w:tr>{sub}</w:tr>'
    for key, name in (("inflation", "Inflation"), ("growth", "Growth")):
        cells = _tc_xml(label_w, _p_xml(name, bold=True, size="18"))
        for wk in weeks:
            sign = wk.get(key, "=")
            fill, txtcol = _regime_sign_style(sign)
            cells += _tc_xml(wk_w, _p_xml(sign, color=txtcol, bold=True, size="20", align="center"), fill=fill)
        rows += f'<w:tr>{cells}</w:tr>'
    tbl = etree.fromstring(_block_tbl_xml(widths, rows))
    if quad_hist:
        counts = {}
        for e in quad_hist.get("weeks", []):
            q = e.get("quadrant", "")
            counts[q] = counts.get(q, 0) + 1
        order = ["Productivity Boost", "Inflation", "Deflation", "Stagflation"]
        line = "Weekly reads per AIP quadrant since %s: %s." % (
            quad_hist.get("since", "the highlight standard began"),
            ", ".join(f"{q} {counts.get(q, 0)}" for q in order))
        # side by side: counts text left, bar chart right, one chart-height row.
        # Split by WIDTH, not column count: with few history weeks the columns are
        # wide and a count-based split leaves the text a sliver.
        n_left, acc = 1, widths[0]
        for w in widths[1:-1]:
            if acc + w > ttl * 0.58:
                break
            acc += w; n_left += 1
        w_left = sum(widths[:n_left]); w_right = ttl - w_left
        tc_txt = etree.fromstring(
            f'<w:tc xmlns:w="{WNS}"><w:tcPr><w:tcW w:w="{w_left}" w:type="dxa"/>'
            f'<w:gridSpan w:val="{n_left}"/>'
            f'<w:tcMar><w:top w:w="50" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
            f'<w:bottom w:w="50" w:type="dxa"/><w:right w:w="90" w:type="dxa"/></w:tcMar>'
            f'<w:vAlign w:val="center"/></w:tcPr>'
            + _p_xml("Quadrant residency", color="7B2952", bold=True)
            + _p_xml(line, size="18")
            + '</w:tc>')
        tc_img = etree.fromstring(
            f'<w:tc xmlns:w="{WNS}"><w:tcPr><w:tcW w:w="{w_right}" w:type="dxa"/>'
            f'<w:gridSpan w:val="{len(widths) - n_left}"/>'
            f'<w:tcMar><w:top w:w="30" w:type="dxa"/><w:bottom w:w="30" w:type="dxa"/></w:tcMar>'
            f'<w:vAlign w:val="center"/></w:tcPr></w:tc>')
        if quad_png:
            tc_img.append(_inline_image_para(doc, quad_png, width_emu=2750000))
        else:
            tc_img.append(etree.fromstring(f'<w:p xmlns:w="{WNS}"/>'))
        tr = etree.fromstring(f'<w:tr xmlns:w="{WNS}"></w:tr>')
        tr.append(tc_txt); tr.append(tc_img); tbl.append(tr)
    _no_split_rows(tbl)
    return tbl


def build_regime_block(asof, regime):
    """30 Jul 2026 (the Co-Op): the Inflation / Growth read that FEEDS the page-1 quadrant,
    stated explicitly and gradeable the same way the lights are. Two rows, each with a
    + or - sign cell (the analogue of the Light cell) and bulleted reasons, so the
    quadrant call on page 1 can be audited against the evidence at the back."""
    widths = [1400, 1500, 4929, 3209]                    # sum 11038 (block width)
    total = sum(widths)
    rows = _header_row_xml("Inflation and Growth Read", asof, total, len(widths))
    sub = (_tc_xml(widths[0], _p_xml("Factor", color="7B2952", bold=True), fill="EFE7EB")
           + _tc_xml(widths[1], _p_xml("Read", color="7B2952", bold=True, align="center"), fill="EFE7EB")
           + _tc_xml(widths[2], _p_xml("Why (the evidence this week)", color="7B2952", bold=True), fill="EFE7EB")
           + _tc_xml(widths[3], _p_xml("What argues the other way", color="7B2952", bold=True), fill="EFE7EB"))
    rows += f'<w:tr>{sub}</w:tr>'
    for e in regime.get("rows", []):
        fill, txtcol = _regime_sign_style(e.get("sign"))
        cells = (_tc_xml(widths[0], _p_xml(e["factor"], bold=True), valign="top")
                 + _tc_xml(widths[1],
                           _p_xml(e.get("sign", "="), color=txtcol, bold=True, size="32", align="center")
                           + _p_xml(e.get("label", ""), color=txtcol, size="16", align="center"),
                           fill=fill)
                 + _cells_xml(widths[2], e.get("why", ""))
                 + _cells_xml(widths[3], e.get("against", "")))
        rows += f'<w:tr>{cells}</w:tr>'
    if regime.get("quadrant_read"):
        rows += ('<w:tr>' + _tc_xml(total,
                                    _p_xml(regime["quadrant_read"], bold=True),
                                    fill="EFE7EB", span=len(widths), valign="top") + '</w:tr>')
    _t = etree.fromstring(_block_tbl_xml(widths, rows)); _no_split_rows(_t); return _t


# ---------- Week by Week Development (19 Aug 2026, per the Co-Op) ----------
# The since-June history page: per theme, a dot strip of every weekly light, a
# SINCE-THE-AIP verdict chip, and a short account of how the development took place.
# Replaces the heatmap render of Theme Light History; the heatmap remains only as
# the fallback for legacy content files that carry no `light_history.evolution`.
# Verdict chips carry their own palette (NOT the weekly light palette — the verdict
# is a cumulative since-AIP call, not a weekly light): suggested vocabulary
# Intensified / Held / Volatility driven / Deescalated, free-form verdicts allowed;
# the `tone` key (or the verdict's first word) picks the colour.
EVOLUTION_TONES = {"intensified": ("538135", "FFFFFF"),   # more of the theme since the AIP
                   "held": ("BF9000", "FFFFFF"),          # at baseline
                   "mixed": ("7F7F7F", "FFFFFF"),         # two-sided / qualified
                   "deescalated": ("C00000", "FFFFFF")}   # less of the theme since the AIP


def _evolution_tone(entry):
    tone = (entry.get("tone") or "").strip().lower()
    if tone in EVOLUTION_TONES:
        return EVOLUTION_TONES[tone]
    w = (entry.get("verdict") or "").strip().lower()
    if w.startswith("intensif"):
        return EVOLUTION_TONES["intensified"]
    if w.startswith(("deescalat", "de-escalat")):
        return EVOLUTION_TONES["deescalated"]
    if w.startswith("held"):
        return EVOLUTION_TONES["held"]
    return EVOLUTION_TONES["mixed"]


def _legend_p_xml(items, size="16"):
    """One centred paragraph of coloured-dot legend entries (text ● runs are fine
    here — only status lines demand the vector oval)."""
    runs = ""
    for i, (col, label) in enumerate(items):
        sep = "      " if i < len(items) - 1 else ""
        runs += (f'<w:r><w:rPr><w:color w:val="{col}"/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr>'
                 f'<w:t xml:space="preserve">● </w:t></w:r>'
                 f'<w:r><w:rPr><w:color w:val="404040"/><w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
                 f'<w:t xml:space="preserve">{_su.escape(label)}{sep}</w:t></w:r>')
    return (f'<w:p><w:pPr><w:spacing w:before="20" w:after="10"/>'
            f'<w:jc w:val="center"/></w:pPr>{runs}</w:p>')


def _italic_p_xml(text, size="15", align="center", color="595959"):
    return (f'<w:p><w:pPr><w:spacing w:before="10" w:after="0" w:line="216" w:lineRule="auto"/>'
            f'<w:jc w:val="{align}"/></w:pPr>'
            f'<w:r><w:rPr><w:i/><w:color w:val="{color}"/>'
            f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
            f'<w:t xml:space="preserve">{_su.escape(text)}</w:t></w:r></w:p>')


def build_week_by_week_block(doc, asof, hist, dates_png, strip_pngs):
    """The Week by Week Development block (19 Aug 2026, per the Co-Op). Table rows:
    header → explainer + legend → column headers (with the shared date strip) →
    one row per theme: name | dot strip | since-AIP verdict chip | how it developed.
    The dot strips are the pngs from engine/make_light_history.py, all with identical
    x-geometry so the date header and every row stay column-aligned; they compress
    as weeks accumulate, so the page holds any number of tracked weeks."""
    widths = [1650, 3350, 1600, 4438]                    # sum 11038 (block width)
    total = sum(widths)
    evo = hist["evolution"]
    # HARD GATE (19 Aug 2026): the Routine finish auto-merges on the checks, and a
    # blank verdict chip or a verdict on the wrong theme row is invisible to
    # check_layout (it reads rendered text, not which row carries it). So an
    # incomplete or misordered evolution set FAILS the build outright, never
    # warn-and-skips: six complete entries in AIP theme order or no dashboard.
    problems = []
    if len(evo) != len(hist["themes"]):
        problems.append(f"{len(evo)} evolution entries for {len(hist['themes'])} themes")
    for i, (theme, e) in enumerate(zip(hist["themes"], evo)):
        if not (e.get("verdict") or "").strip():
            problems.append(f"evolution[{i}] ({theme}) has an empty verdict")
        if not (e.get("description") or "").strip():
            problems.append(f"evolution[{i}] ({theme}) has an empty description")
        lbl = (e.get("theme") or "").strip()
        if lbl and lbl != theme.strip():
            problems.append(f"evolution[{i}] labelled {lbl!r} but themes[{i}] is "
                            f"{theme!r} (rows match by ORDER)")
    if problems:
        sys.exit("FATAL: Week by Week Development content incomplete — "
                 + "; ".join(problems)
                 + ". Fill light_history.evolution (six complete entries in AIP "
                   "theme order, schema _light_history_note) and rebuild.")
    tbl = etree.fromstring(_block_tbl_xml(
        widths, _header_row_xml("Week by Week Development", asof, total, len(widths))))

    intro = (_italic_p_xml(
        "Each dot is that week's status call from the weekly dashboard: the direction "
        "of the theme, not whether it was good or bad for the portfolio. The verdict "
        "states how each theme has evolved since the Annual Investment Plan (AIP) "
        "baseline; series starts 18 June 2026 (three lights since 2 July).")
        + _legend_p_xml([("92D050", "Escalating, more of the theme"),
                         ("FFC000", "Held, mixed or null"),
                         ("EE0000", "Deescalating, less of the theme")]))
    tbl.append(etree.fromstring(
        f'<w:tr xmlns:w="{WNS}">{_tc_xml(total, intro, span=len(widths))}</w:tr>'))

    def _tc_el(xml_tc):
        return etree.fromstring(
            f'<w:tr xmlns:w="{WNS}">{xml_tc}</w:tr>').find(qn('w:tc'))

    hdr = etree.fromstring(f'<w:tr xmlns:w="{WNS}"></w:tr>')
    hdr.append(_tc_el(_tc_xml(
        widths[0], _p_xml("Theme", color="7B2952", bold=True, size="17"),
        fill="EFE7EB")))
    tc_dates = etree.fromstring(
        f'<w:tc xmlns:w="{WNS}"><w:tcPr><w:tcW w:w="{widths[1]}" w:type="dxa"/>'
        f'<w:shd w:val="clear" w:color="auto" w:fill="EFE7EB"/>'
        f'<w:tcMar><w:top w:w="10" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
        f'<w:bottom w:w="10" w:type="dxa"/><w:right w:w="110" w:type="dxa"/></w:tcMar>'
        f'<w:vAlign w:val="center"/></w:tcPr></w:tc>')
    tc_dates.append(_inline_image_para(doc, dates_png, width_emu=1980000))
    hdr.append(tc_dates)
    hdr.append(_tc_el(_tc_xml(
        widths[2], _p_xml("Since the AIP", color="7B2952", bold=True, size="17",
                          align="center"), fill="EFE7EB")))
    hdr.append(_tc_el(_tc_xml(
        widths[3], _p_xml("How it developed", color="7B2952", bold=True, size="17"),
        fill="EFE7EB")))
    tbl.append(hdr)

    for ti, theme in enumerate(hist["themes"]):
        e = evo[ti]
        fill, txt = _evolution_tone(e)
        tr = etree.fromstring(f'<w:tr xmlns:w="{WNS}"></w:tr>')
        tr.append(_tc_el(_tc_xml(
            widths[0], _p_xml(theme, color="7B2952", bold=True, size="18"))))
        tc_dots = etree.fromstring(
            f'<w:tc xmlns:w="{WNS}"><w:tcPr><w:tcW w:w="{widths[1]}" w:type="dxa"/>'
            f'<w:tcMar><w:top w:w="10" w:type="dxa"/><w:left w:w="90" w:type="dxa"/>'
            f'<w:bottom w:w="10" w:type="dxa"/><w:right w:w="110" w:type="dxa"/></w:tcMar>'
            f'<w:vAlign w:val="center"/></w:tcPr></w:tc>')
        tc_dots.append(_inline_image_para(doc, strip_pngs[ti], width_emu=1980000))
        tr.append(tc_dots)
        tr.append(_tc_el(_tc_xml(
            widths[2], _p_xml(e.get("verdict", ""), color=txt, bold=True, size="17",
                              align="center"), fill=fill)))
        desc = e.get("description", "")
        desc = desc if isinstance(desc, list) else [desc]
        tr.append(_tc_el(_tc_xml(
            widths[3], "".join(_p_xml(d, size="17", align="both") for d in desc),
            valign="top")))
        tbl.append(tr)
    _no_split_rows(tbl)
    return tbl


def build_light_history_block(doc, asof, hist, png=None):
    """The history page. Since 19 Aug 2026 the PREFERRED render is the Week by Week
    Development block (dot strips + since-AIP verdict + how it developed), taken when
    `light_history.evolution` exists and the dot-strip pngs (make_light_history.py)
    sit beside `light_history_png`. Legacy renders, for old content files only: the
    heatmap image (9 Jul 2026), else a coloured word matrix."""
    total = 11038
    if hist.get("evolution"):
        # Regenerate the dot strips at build (19 Aug 2026) so they can never go
        # stale against light_history.weeks (e.g. a resumed session that appended
        # the week after an earlier render). make_light_history.py stays the
        # standalone way to produce them plus the fallback heatmap and the
        # quadrant chart; this call only refreshes the strips.
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            import make_light_history as _mlh
            _mlh.make_dot_strips({"light_history": hist, "light_history_png": png})
        except SystemExit:
            raise
        except Exception as _e:
            print(f"WARN: dot strips not regenerated at build ({_e}); "
                  f"using the existing files if present")
        dots_dir = os.path.dirname(png) if png else None
        dates_png = os.path.join(dots_dir, "history_dates.png") if dots_dir else None
        strips = [os.path.join(dots_dir, f"history_dots_{i + 1}.png")
                  for i in range(len(hist.get("themes") or []))] if dots_dir else []
        if dates_png and os.path.exists(dates_png) and strips \
                and all(os.path.exists(s) for s in strips):
            return build_week_by_week_block(doc, asof, hist, dates_png, strips)
        print(f"WARN: light_history.evolution is set but the dot strips are missing in "
              f"{dots_dir!r} — run engine/make_light_history.py first; falling back to "
              f"the legacy heatmap render (check_layout will fail on the block title)")
    if png:
        rows = _header_row_xml("Theme Light History", asof, total, 1)
        tbl = etree.fromstring(_block_tbl_xml([total], rows))
        tc = etree.fromstring(
            f'<w:tc xmlns:w="{WNS}"><w:tcPr><w:tcW w:w="{total}" w:type="dxa"/>'
            f'<w:tcMar><w:top w:w="80" w:type="dxa"/><w:bottom w:w="80" w:type="dxa"/></w:tcMar>'
            f'</w:tcPr></w:tc>')
        tc.append(_inline_image_para(doc, png, width_emu=5850000))
        tc.append(_caption_para("Each cell is that week's light: green Escalating (more of the theme), "
                                "amber Held (mixed or null), red Deescalating (less). 3-light system since 2 July 2026."))
        tr = etree.fromstring(f'<w:tr xmlns:w="{WNS}"></w:tr>'); tr.append(tc); tbl.append(tr)
        return tbl
    themes, weeks = hist["themes"], hist["weeks"]
    theme_w = 2150
    wk_w = (total - theme_w) // max(1, len(weeks))
    widths = [theme_w] + [wk_w] * len(weeks)
    ttl = sum(widths); ncols = len(widths)
    rows = _header_row_xml("Theme Light History", asof, ttl, ncols)
    sub = _tc_xml(theme_w, _p_xml("Theme", color="7B2952", bold=True), fill="EFE7EB")
    for wk in weeks:
        sub += _tc_xml(wk_w, _p_xml(wk["date"], color="7B2952", bold=True, align="center"), fill="EFE7EB")
    rows += f'<w:tr>{sub}</w:tr>'
    for ti, th in enumerate(themes):
        cells = _tc_xml(theme_w, _p_xml(th, bold=True))
        for wk in weeks:
            lw = wk["lights"][ti]
            cells += _tc_xml(wk_w, _p_xml(lw, color=_light_textcol(lw), bold=True, align="center"), fill=_light_fill(lw))
        rows += f'<w:tr>{cells}</w:tr>'
    _t = etree.fromstring(_block_tbl_xml(widths, rows)); _no_split_rows(_t); return _t

_CHART_SLOTS_FILLED = []


def main():
    tmpl, out, contentf = sys.argv[1], sys.argv[2], sys.argv[3]
    prev = sys.argv[4] if len(sys.argv) > 4 else None
    C = json.load(open(contentf))
    check_signs_vs_quadrant(C)
    check_illiquids(C)
    doc = Document(tmpl)
    _seed_ids(doc)
    asof = C["asof"]            # e.g. 2026_07_02

    # 1) date stamps everywhere
    for p in doc.element.body.iter(qn('w:p')):
        for t in p.iter(qn('w:t')):
            if t.text and 'YYYY_MM_DD' in t.text:
                t.text = t.text.replace('YYYY_MM_DD', asof)

    tbls = top_tables(doc)

    # 1b) resolve the Co-Op's uploaded charts (13 Aug 2026): one pass over ChartsThemes/
    # (or `chart_source_dir`), explicit `chart_images` overrides win per slot. Every
    # resolved slot gets the REAL chart at the slot's measured geometry; unresolved
    # slots keep the dashed placeholder and are named here — never a silent gap.
    chart_dir = C.get("chart_source_dir", "ChartsThemes")
    _dir_index = index_chart_dir(chart_dir)
    chart_images = {}
    for _slot in (C.get("chart_slots") or {}):
        _src = resolve_chart_image(_slot, _dir_index, C.get("chart_images"))
        if _src:
            chart_images[_slot] = _src
    if _dir_index or C.get("chart_images"):
        _missing = [s for s in (C.get("chart_slots") or {}) if s not in chart_images]
        print("charts resolved from %s: %d/%d slots%s" % (
            chart_dir, len(chart_images), len(C.get("chart_slots") or {}),
            ("; placeholder fallback: " + ", ".join(_missing)) if _missing else ""))
    else:
        print("no chart source dir (%s) and no chart_images — all slots get placeholders" % chart_dir)

    # 2) Executive Summary
    exec_t = next(t for t in tbls if block_title(t).startswith("Executive Summary"))
    # 2a) quadrant — Jun-30 reference format (default since 23 Jul 2026): the template
    # carries the AIP Jun 30 environment; relabel/move its single dated marker.
    # Legacy trail transplant only when explicitly requested (quadrant_transplant).
    if C.get("quadrant_transplant"):
        if prev:
            quadrant_from_prev(doc, exec_t, prev)
        if C.get("quadrant_marker"):
            quadrant_add_marker(exec_t, C["quadrant_marker"], asof)
    elif C.get("quadrant_highlight"):
        # 30 Jul 2026 standard: shade the whole quadrant, drop the dot and the AIP note,
        # then (v2, same day) move the map INLINE with the rationale styled beneath it.
        quadrant_strip_marker_and_note(
            exec_t, drop_note=C["quadrant_highlight"].get("drop_aip_note", True))
        # v6 template: exec already inline, bake + rationale happen inside inline_layout.
        # v5 template: bake into the floating map FIRST, then convert it inline.
        _is_v6 = False
        for _nt in exec_t.iter(qn('w:tbl')):
            if _nt is exec_t: continue
            _hr = _nt.find(qn('w:tr'))
            if _hr is not None and "Weekly Direction" in para_text(_hr):
                _g = _nt.find(qn('w:tblGrid'))
                _is_v6 = _g is not None and len(_g.findall(qn('w:gridCol'))) >= 3
                break
        if not _is_v6:
            quadrant_apply_highlight(doc, exec_t, C["quadrant_highlight"])
        quadrant_inline_layout(doc, exec_t, C)
    elif C.get("quadrant_marker"):
        quadrant_relabel_and_move(exec_t, C["quadrant_marker"])
    scale_exec_quadrant(exec_t, C.get("quadrant_scale", 1.0))
    shift_exec_quadrant(exec_t, C.get("quadrant_shift_up_emu", 0))
    quadrant_behind_text(exec_t, C.get("quadrant_behind", False))
    if not C.get("quadrant_highlight"):
        # legacy dot path only: the highlight path renders the rationale inline
        fill_quadrant_rationale(exec_t, C.get("quadrant_rationale"),
                                C.get("quadrant_rationale_heading", "Why this quadrant"),
                                str(C.get("quadrant_rationale_sz", 15)))
    set_exec_row_heights(exec_t, C.get("exec_r1_height_twips"), C.get("exec_r2_height_twips"))
    # 2b) status dashboard nested table
    sd = None
    for nt in exec_t.iter(qn('w:tbl')):
        if nt is exec_t:
            continue
        hr = nt.find(qn('w:tr'))
        if hr is not None and para_text(hr).strip().startswith("Theme"):
            sd = nt
            break
    sd_trs = sd.findall(qn('w:tr'))[1:]
    LIGHTS = {"deescalating": ("EE0000", "#e00"),
              "de-escalating": ("EE0000", "#e00"),
              "escalating": ("92D050", "#92d050"),
              "held": ("FFC000", "#ffc000")}
    for tr, row in zip(sd_trs, C["status_dashboard"]):
        tcs = tr.findall(qn('w:tc'))
        fill_cell_placeholder(tcs[1], row["status"])
        fill_cell_placeholder(tcs[2], row["oneliner"])
        key = row["status"].strip().lower()
        col = next((v for k, v in sorted(LIGHTS.items(), key=lambda x: -len(x[0])) if key.startswith(k)), None)
        if col:
            dml, vml = col
            for el in tcs[1].iter():
                if (el.get('val') or '').upper() == "EE0000":
                    el.set('val', dml)
                if el.get('fillcolor'):
                    el.set('fillcolor', vml)
    # 2c) weekly direction & influencing factors (nested 2-col table beside the quadrant)
    def fill_token(scope, token, text):
        for p in scope.iter(qn('w:p')):
            if token in para_text(p):
                fill_para_placeholder(p, text); return True
        return False
    if C.get("weekly_direction"):
        fill_token(exec_t, "[[weekly_direction]]", C["weekly_direction"])
        fill_direction_signs(exec_t, C.get("direction_signs"))
    if C.get("influencing_factors"):
        fac = C["influencing_factors"]
        if isinstance(fac, list):
            # one short paragraph per factor (4-6 lines filling the cell since 6 Aug 2026;
            # was exactly 3 from 3 Jul to 6 Aug 2026)
            target = None
            for p in exec_t.iter(qn('w:p')):
                if "[[influencing_factors]]" in para_text(p):
                    target = p; break
            if target is not None:
                anchor = target
                for extra in fac[1:]:
                    np = copy.deepcopy(target)
                    anchor.addnext(np); anchor = np
                    fill_para_placeholder(np, extra)
                fill_para_placeholder(target, fac[0])
        else:
            fill_token(exec_t, "[[influencing_factors]]", fac)
    # 2d) Key Developments | Implication for Themes rows.
    # RETIRED 30 Jul 2026 (the Co-Op): the exec keydev page restated the theme blocks.
    # Set `keep_exec_key_developments: true` to bring it back.
    if not C.get("keep_exec_key_developments", False):
        drop_exec_key_developments(exec_t)
    elif C.get("key_developments"):
        fill_key_developments(exec_t, C["key_developments"])
        # compact the key-dev rows (template reserves 1975 twips each) so all 6 fit page 2
        _trs = exec_t.findall(qn('w:tr'))
        _hi = next((i for i, tr in enumerate(_trs) if para_text(tr).strip().startswith("Key Developments")), None)
        if _hi is not None:
            for tr in _trs[_hi + 1:]:
                trPr = tr.find(qn('w:trPr'))
                if trPr is None:
                    trPr = OxmlElement('w:trPr'); tr.insert(0, trPr)
                he = trPr.find(qn('w:trHeight'))
                if he is None:
                    he = OxmlElement('w:trHeight'); trPr.append(he)
                he.set(qn('w:val'), '1150'); he.set(qn('w:hRule'), 'atLeast')
                for p in tr.iter(qn('w:p')):
                    pPr = p.find(qn('w:pPr'))
                    if pPr is None:
                        pPr = OxmlElement('w:pPr'); p.insert(0, pPr)
                    spc = pPr.find(qn('w:spacing'))
                    if spc is None:
                        spc = add_spacing_ordered(pPr)
                    spc.set(qn('w:before'), '0'); spc.set(qn('w:after'), '20')
    # legacy cells (kept for backward compatibility with old templates)
    ct = cell_containing(exec_t, "Cross-theme takeaways")
    if ct is not None and C.get("cross_theme"):
        fill_bullets(ct, C["cross_theme"])
    kr = cell_containing(exec_t, "Key Risks register")
    if kr is not None and C.get("key_risks"):
        fill_bullets(kr, C["key_risks"])

    # 3) theme blocks
    def do_block(title_startswith, key, light=True):
        blk = next((t for t in tbls if block_title(t).startswith(title_startswith)), None)
        if blk is None:
            print("WARN: block '%s' not found in template — skipped entirely" % title_startswith)
            return
        b = C[key]
        fill_status_line(blk, b["status"], light=light)
        wc = cell_containing(blk, "What changed this week")
        if wc is not None:
            fill_bullets(wc, b["developments"])
        else:
            print("WARN: no 'What changed' cell in '%s'" % title_startswith)
        if b.get("material_rows"):
            fill_data_table(nested_table(blk), b["material_rows"])
        else:
            material_to_note(doc, blk, b["material_note"],
                             b.get("keydev_chart_png"), b.get("keydev_chart_note"))
        im = cell_containing(blk, "Implication for the theme")
        if im is not None:
            fill_single_placeholder_cell(im, b["implication"])
        else:
            print("WARN: no 'Implication' cell in '%s'" % title_startswith)
        wa = cell_containing(blk, "Watch next week")
        if wa is not None:
            fill_bullets(wa, b["watch"])
        else:
            print("WARN: no 'Watch next week' cell in '%s'" % title_startswith)
        drop_empty_fullwidth_rows(blk)
        # 30 Jul 2026: reserve the real chart geometry so the Co-Op's inserts do not
        # reflow; 13 Aug 2026: slots with a ChartsThemes upload get the REAL chart.
        got = fill_chart_placeholders(doc, blk, C.get("chart_slots"),
                                      C.get("chart_slot_default"), chart_images)
        if got:
            _CHART_SLOTS_FILLED.extend(got)

    do_block("Theme 1 — Fiscal", "theme1")
    do_block("Theme 1 Appendix", "monetary", light=False)     # tracker: no light, no status word
    do_block("Theme 2", "theme2")
    do_block("Theme 3", "theme3")
    do_block("Theme 4", "theme4")
    do_block("Theme 5", "theme5")
    do_block("Theme 6", "theme6")

    # 3b) central-bank table in the monetary appendix
    if C.get("central_bank"):
        mon = next(t for t in tbls if block_title(t).startswith("Theme 1 Appendix"))
        cbt = None
        for nt in mon.iter(qn('w:tbl')):
            if nt is not mon:
                hr = nt.find(qn('w:tr'))
                if hr is not None and "Central Bank" in para_text(hr):
                    cbt = nt; break
        if cbt is not None:
            fill_data_table(cbt, C["central_bank"])
            # 30 Jul 2026: the template's note column is too narrow and wraps every
            # note to 5-7 lines, making the table the tallest thing in the block and
            # leaving white space beside it. Rebalance: bank 1500 / rate 1210 / note 2780.
            _g = cbt.find(qn('w:tblGrid'))
            if _g is not None and len(_g.findall(qn('w:gridCol'))) == 3:
                for _gc, _w in zip(_g.findall(qn('w:gridCol')), (1500, 1210, 2780)):
                    _gc.set(qn('w:w'), str(_w))
                for _tr in cbt.findall(qn('w:tr')):
                    for _tc, _w in zip(_tr.findall(qn('w:tc')), (1500, 1210, 2780)):
                        _tcw = _tc.find(qn('w:tcPr')).find(qn('w:tcW'))
                        if _tcw is not None:
                            _tcw.set(qn('w:w'), str(_w))

    # 4) references (tiered)
    fill_references(doc, C["references_intro"], C["references"])

    # 4b) NEW sections (9 Jul 2026): light-scoring transparency + theme light history,
    #     inserted after Theme 6 and before the Lights Guide Appendix.
    lg_anchor = None
    for p in doc.element.body.findall(qn('w:p')):
        if "".join(t.text or '' for t in p.iter(qn('w:t'))).strip().startswith("Lights Guide Appendix"):
            lg_anchor = p; break
    if lg_anchor is not None:
        # 6 Aug 2026 (the Co-Op): Illiquids goes FIRST of the generated back-matter blocks,
        # i.e. immediately after Theme 6 and before Light Scoring. It carries no light.
        if C.get("illiquids"):
            _ib = build_illiquids_block(doc, asof, C["illiquids"])
            lg_anchor.addprevious(_ib)
            # same sized chart placeholders as a theme block, so the Co-Op's own charts
            # paste in without reflowing the page
            _got = fill_chart_placeholders(doc, _ib, C.get("chart_slots"),
                                           C.get("chart_slot_default"), chart_images)
            if _got:
                _CHART_SLOTS_FILLED.extend(_got)
        if C.get("light_scoring"):
            lg_anchor.addprevious(build_light_scoring_block(
                asof, C["light_scoring"], str(C.get("light_scoring_sz", 17))))
        if C.get("regime_table"):
            # 30 Jul 2026: Inflation / Growth read, immediately after Light Scoring
            lg_anchor.addprevious(build_regime_block(asof, C["regime_table"]))
            if C.get("regime_history"):
                lg_anchor.addprevious(build_regime_history_block(
                    doc, asof, C["regime_history"],
                    C.get("quadrant_history"), C.get("quadrant_history_png")))
        if C.get("light_history"):
            lg_anchor.addprevious(build_light_history_block(doc, asof, C["light_history"], C.get("light_history_png")))
    elif C.get("light_scoring") or C.get("light_history") or C.get("illiquids"):
        print("WARN: no 'Lights Guide Appendix' anchor found — new sections skipped")

    # 5) de-float blocks to inline flow + space them
    defloat_and_space(doc)

    # 6) force the page schema (9 Jul 2026): Key Developments on page 2, one theme per page.
    _tbls = top_tables(doc)
    _theme_prefixes = ("Theme 1 —", "Theme 1 -", "Theme 1 Appendix", "Theme 1 (Appendix)",
                       "Theme 2", "Theme 3", "Theme 4", "Theme 5", "Theme 6")
    # 13 Aug 2026: the Co-Op's approved 07 Aug dashboard renamed the Illiquids header to
    # "Allocation Insights - Illiquid Assets"; match both so the block keeps its own page.
    # 19 Aug 2026: "Week by Week Development" replaces "Theme Light History" as the
    # history page's header; the old header stays matched for legacy renders.
    _gen_prefixes = ("Illiquid Assets", "Allocation Insights", "Light Scoring",
                     "Inflation and Growth Read", "Week by Week Development",
                     "Theme Light History")
    _tmin = int(C.get("theme_row_min_twips", 1250))
    def _drop_spacer_before(tbl):
        prev = tbl.getprevious()
        if prev is not None and prev.tag == qn('w:p') and \
           not "".join(x.text or '' for x in prev.iter(qn('w:t'))).strip() and \
           prev.find('.//' + qn('w:br')) is None:
            prev.getparent().remove(prev)
    for t in _tbls:
        ttl = block_title(t)
        if any(ttl.startswith(pfx) for pfx in _theme_prefixes):
            # v4 (23 Jul 2026): zero-height pageBreakBefore paragraph before the table.
            # A pageBreakBefore INSIDE the table's first paragraph (carried into the
            # template from prior engine output) is honoured by Word but ignored by
            # LibreOffice at a table START (it only splits tables at interior rows),
            # and it double-breaks against the paragraph — strip it here.
            fp = t.find('.//' + qn('w:p'))
            if fp is not None:
                fpPr = fp.find(qn('w:pPr'))
                if fpPr is not None:
                    _pbb = fpPr.find(qn('w:pageBreakBefore'))
                    if _pbb is not None:
                        fpPr.remove(_pbb)
            _drop_spacer_before(t)
            t.addprevious(break_before_para())
            compact_block_rows(t, _tmin)
        elif any(ttl.startswith(pfx) for pfx in _gen_prefixes):
            _drop_spacer_before(t)
            t.addprevious(break_before_para())
    # Exec pagination (24 Jul 2026 standard, per the Co-Op): page 1 = Weekly Direction +
    # Influencing Factors + Jun-30 quadrant + the FULL Status Dashboard; the Key
    # Developments start page 2. In-table row breaks are unreliable in renderers, so
    # the exec table is SPLIT at the Key Developments header into a second table with
    # a zero-height pageBreakBefore paragraph between (prints identically). Keep
    # factors and one-liners tight (~2 rendered lines) so page 1 holds all six rows.
    exec_b = next((t for t in _tbls if block_title(t).startswith("Executive Summary")), None)
    if exec_b is not None:
        _etrs = exec_b.findall(qn('w:tr'))
        _ki = next((i for i, tr in enumerate(_etrs)
                    if para_text(tr).strip().startswith("Key Developments")), None)
        if _ki is not None and _ki > 0:
            kd_tbl = OxmlElement('w:tbl')
            _tp = exec_b.find(qn('w:tblPr'))
            _tg = exec_b.find(qn('w:tblGrid'))
            if _tp is not None:
                kd_tbl.append(copy.deepcopy(_tp))
            if _tg is not None:
                kd_tbl.append(copy.deepcopy(_tg))
            for tr in _etrs[_ki:]:
                kd_tbl.append(tr)          # moves the row out of exec_b
            # strip any template-carried pageBreakBefore in the moved header row
            # (prior engine generations set it; it double-breaks against the paragraph)
            for _p in kd_tbl.iter(qn('w:p')):
                _pPr = _p.find(qn('w:pPr'))
                if _pPr is not None:
                    _pbb = _pPr.find(qn('w:pageBreakBefore'))
                    if _pbb is not None:
                        _pPr.remove(_pbb)
            exec_b.addnext(kd_tbl)
            kd_tbl.addprevious(break_before_para())

    _cfix = centre_block_tables(doc)
    if _cfix:
        print("centred %d block tables on the page (margin asymmetry fix)" % _cfix)
    _hfix = restore_atleast_heights(doc)
    if _hfix:
        print("restored hRule=atLeast on %d row heights" % _hfix)
    _nfix = normalise_tblpr(doc)
    if _nfix:
        print("normalised %d table property blocks into schema order" % _nfix)
    doc.save(out)
    if _CHART_SLOTS_FILLED:
        print("chart slots: " + ", ".join(
            f"{n} {w:.2f}x{h:.2f}in <- {s}" for n, w, h, s in _CHART_SLOTS_FILLED))
    print("saved", out)

if __name__ == "__main__":
    main()
