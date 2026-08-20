#!/usr/bin/env python3
"""
Build a fill-template from an APPROVED dashboard (v3, 13 Aug 2026).

v3 (13 Aug 2026): the Illiquid Assets block (either header spelling) is now DROPPED
like the other engine-generated back-matter blocks — it is rebuilt from content every
run, so it must never ride into a template as fixed text (spec_audit item 26).

Turns Eduardo's newest approved dashboard (formatting ground truth) into the
next MacroBasis_Report_Template_vN.docx by stripping the week's content and
re-inserting the [[placeholder]] tokens macrobasis_fill.py expects. Run it
whenever his structural hand edits should become the new template.

v2 (23 Jul 2026) — rebuilt for Eduardo's 17 Jul restructure:
  * exec: quadrant cluster in the Jun-30 reference format is KEPT VERBATIM
    (AIP Jun 30 map + note box + prior week's single dated marker; the fill
    engine relabels/moves that marker, no transplant, no trail);
  * exec status dashboard now lives on page 2 (fill engine breaks before it);
  * theme blocks: charts LEFT/RIGHT of a bulleted "What changed" column,
    keydev = full-width text row, Implication | Watch side by side;
  * chart cells -> "Insert <theme>_chart_N" markers (one per image removed);
  * Monetary appendix carries NO keydev row (17 Jul standard) and a 7-row
    central-bank table (tokenized to one clone-row);
  * the engine-generated back-matter tables (Light Scoring, the history page under
    either header — Theme Light History or Week by Week Development — the Inflation
    and Growth Read and the sign-history strip) are REMOVED
    (the fill engine regenerates them every run);
  * a keydev row is restored to any THEME block whose hand edit deleted it
    (Monetary appendix excluded by design).

Usage:
    python3 engine/build_template_from_dashboard.py <approved_dashboard.docx> <out_template.docx>
"""
import sys, os, re, copy
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

W_DRAW = qn('w:drawing')
MC_AC_TAG = '{http://schemas.openxmlformats.org/markup-compatibility/2006}AlternateContent'

TOK_STATUS = ("[[Status word (Escalating / Held / Deescalating) ▸ what decided it, with the data; "
              "the read woven in as a clause.]]")
TOK_DEV = "[[Development 1 — the week's story, facts first, every number with prior/expectation/trend context.]]"
TOK_IMPL = "[[2–3 sentences tying the week to the thesis and the asset-class read.]]"
TOK_WATCH = "[[Named release/event — falsifiable, dated.]]"
TOK_KD_DEV = "[[Key development — the news: what happened, with the data.]]"
TOK_KD_IMP = "[[Implication — what this development means for the theme(s).]]"
TOK_REF_INTRO = "[[Only sources cited this week. Deduplicate. Include retrieval date. Do not reproduce the AIP references.]]"
TOK_REF_ITEM = "[[Source name. “Title.” Publication date. URL. Retrieved [date].]]"

# Chart Map v5 (engine/MacroBasis_DOCX_Format_Spec.md): marker names consumed in
# document order of the image-bearing chart cells; one marker per image removed.
SLOT_MARKERS = {
    "Theme 1 —": ["Insert fiscal_chart_1", "Insert fiscal_chart_2"],
    "Theme 1 Appendix": ["Insert monetary_1"],
    "Theme 2": ["Insert currency_1", "Insert currency_2", "Insert currency_3"],
    "Theme 3": ["Insert energy_1", "Insert energy_2"],
    "Theme 4": ["Insert AI_1", "Insert AI_2"],
    "Theme 5": ["Insert geo_1", "Insert geo_2"],
    "Theme 6": ["Insert domestic_1", "Insert domestic_2"],
}
LIGHT_VALS = {"92D050", "FFC000", "EE0000"}

def ptext(p):
    return "".join(t.text or "" for t in p.iter(qn('w:t')))

def cell_text(tc):
    return "\n".join(ptext(p) for p in tc.findall(qn('w:p')))

def block_title(tbl):
    tr = tbl.find(qn('w:tr'))
    return ptext(tr.find(qn('w:tc'))).strip()

def cells(tbl):
    return tbl.findall('.//' + qn('w:tc'))

def cell_containing(tbl, needle):
    for tc in cells(tbl):
        if needle in cell_text(tc):
            return tc
    return None

def set_para_token(p, token):
    """Keep the paragraph's first text run (formatting), set its text to the
    token, remove every other run (incl. drawings/Status Balls)."""
    runs = p.findall(qn('w:r'))
    keeper = None
    for r in runs:
        ts = r.findall(qn('w:t'))
        if ts and r.find('.//' + W_DRAW) is None:
            keeper = r
            break
    if keeper is None:
        keeper = OxmlElement('w:r')
        t = OxmlElement('w:t'); keeper.append(t)
        p.append(keeper)
    ts = keeper.findall(qn('w:t'))
    ts[0].text = token
    ts[0].set(qn('xml:space'), 'preserve')
    for extra in ts[1:]:
        extra.getparent().remove(extra)
    for r in runs:
        if r is not keeper:
            r.getparent().remove(r)

def set_text_runs_token(p, token):
    """Like set_para_token but PRESERVES drawing runs (used where an oval shares
    the paragraph with the text, e.g. the exec Status Dashboard cells)."""
    def is_drawing(r):
        return r.find('.//' + W_DRAW) is not None or any(e.tag == MC_AC_TAG for e in r.iter())
    text_runs = [r for r in p.findall(qn('w:r')) if r.findall(qn('w:t')) and not is_drawing(r)]
    if not text_runs:
        r = OxmlElement('w:r'); t = OxmlElement('w:t'); r.append(t); p.append(r)
        text_runs = [r]
    ts = text_runs[0].findall(qn('w:t'))
    ts[0].text = token
    ts[0].set(qn('xml:space'), 'preserve')
    for extra in ts[1:]:
        extra.getparent().remove(extra)
    for r in text_runs[1:]:
        r.getparent().remove(r)

def label_and_content(tc, label):
    lab, content = None, []
    for p in tc.findall(qn('w:p')):
        if lab is None and label in ptext(p):
            lab = p
        elif ptext(p).strip() or p.find('.//' + W_DRAW) is not None:
            content.append(p)
    return lab, content

def one_token_para(tc, label, token):
    """Reduce a labelled cell to: label para + ONE token para (formatting —
    incl. list numbering — cloned from the first content para)."""
    lab, content = label_and_content(tc, label)
    if not content:
        np = OxmlElement('w:p')
        if lab is not None:
            lab.addnext(np)
        else:
            tc.append(np)
        set_para_token(np, token)
        return
    tpl = content[0]
    set_para_token(tpl, token)
    for p in content[1:]:
        p.getparent().remove(p)

def marker_para(text):
    np = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    jc = OxmlElement('w:jc'); jc.set(qn('w:val'), 'center')
    pPr.append(jc); np.append(pPr)
    if text:
        r = OxmlElement('w:r')
        t = OxmlElement('w:t'); t.text = text
        t.set(qn('xml:space'), 'preserve')
        r.append(t); np.append(r)
    return np

def strip_chart_cell(tc, markers, mi):
    """Replace a chart cell's contents with one 'Insert ...' marker per image
    it held; returns the updated marker index."""
    n_imgs = len(tc.findall('.//' + W_DRAW))
    for p in list(tc.findall(qn('w:p'))):
        tc.remove(p)
    for _ in range(max(1, n_imgs)):
        m = markers[mi] if mi < len(markers) else None
        tc.append(marker_para(m))
        mi += 1
    return mi

def clean_keydev_cell(tc):
    for t in list(tc.findall(qn('w:tbl'))):
        tc.remove(t)
    lab, content = label_and_content(tc, "Key Development of the Week")
    for p in content:
        p.getparent().remove(p)
    if lab is not None:
        lab.addnext(OxmlElement('w:p'))

def row_of(tbl, tc):
    for tr in tbl.findall(qn('w:tr')):
        if tc in tr.findall('.//' + qn('w:tc')):
            return tr
    return None

def main():
    src, out = sys.argv[1], sys.argv[2]
    doc = Document(src)
    body = doc.element.body

    # v3 (13 Aug 2026): restore hRule="atLeast" on EVERY row height when ingesting a
    # hand-edited dashboard. Word drops the attribute on save; renderers then treat the
    # saved height as fixed, the exec block balloons and the six status rows fall off
    # page 1 (the lesson recorded in content_schema.json's _chart_slots_note, never
    # implemented here). atLeast lets rows shrink back to content in the fill.
    _fixed = 0
    for trh in body.iter(qn('w:trHeight')):
        if trh.get(qn('w:hRule')) != 'atLeast':
            trh.set(qn('w:hRule'), 'atLeast')
            _fixed += 1
    if _fixed:
        print(f"restored hRule=atLeast on {_fixed} row heights (Word drops it on save)")

    # ---------- drop the engine-generated blocks (regenerated every run) ----------
    # v3 (13 Aug 2026): the Illiquid Assets block joined the drop-list. It is engine-
    # generated from `illiquids` content every run (build_illiquids_block), exactly like
    # Light Scoring; before this fix the script carried the approved week's literal
    # Illiquids text and charts into the new template as fixed content (audit item 26).
    # Both header spellings are matched: the original "Illiquid Assets" and Eduardo's
    # approved rename "Allocation Insights - Illiquid Assets" (canonical display title).
    for t in list(body.findall(qn('w:tbl'))):
        ttl = block_title(t)
        if ttl.startswith(("Light Scoring and Developments", "Theme Light History",
                           "Week by Week Development",
                           "Inflation and Growth Read", "Sign history",
                           "Illiquid Assets", "Allocation Insights")):
            body.remove(t)
    # stray empty / hard-page-break paragraphs left behind between blocks
    tbls = body.findall(qn('w:tbl'))
    last_tbl = tbls[-1]
    kids = list(body.iterchildren())
    for ch in kids:
        if ch.tag != qn('w:p'):
            continue
        txt = "".join(t.text or '' for t in ch.iter(qn('w:t'))).strip()
        has_draw = ch.find('.//' + W_DRAW) is not None
        has_break = ch.find('.//' + qn('w:br')) is not None
        if txt == "" and not has_draw and has_break:
            body.remove(ch)

    tbls = body.findall(qn('w:tbl'))

    # ---------- Executive Summary ----------
    ex = next(t for t in tbls if block_title(t).startswith("Executive Summary"))
    # weekly direction (short para naming inflation/growth inside the nested 2-col table)
    wd_done = False
    for p in ex.iter(qn('w:p')):
        txt = ptext(p).strip()
        if not wd_done and txt and ("inflation" in txt.lower() or "growth" in txt.lower()) and len(txt) < 160 \
           and p.getparent().tag == qn('w:tc'):
            nt = p.getparent().getparent().getparent()   # tc -> tr -> tbl
            if nt.tag == qn('w:tbl') and "Weekly Direction" in "".join(ptext(q) for q in nt.iter(qn('w:p'))):
                set_para_token(p, "[[weekly_direction]]")
                wd_done = True
    # influencing factors: ONE token para (keeps the bullet numbering of the first line)
    for nt in ex.iter(qn('w:tbl')):
        if nt is ex:
            continue
        head = "".join(ptext(q) for q in nt.findall(qn('w:tr'))[0].iter(qn('w:p')))
        if "Influencing Factors" in head:
            trs = nt.findall(qn('w:tr'))
            body_tcs = trs[1].findall(qn('w:tc'))
            # 30 Jul 2026: direction table has 3 columns (direction | factors | quadrant);
            # the factors cell is the one under the "Influencing Factors" header
            fac_tc = body_tcs[1] if len(body_tcs) >= 3 else body_tcs[-1]
            ps = [p for p in fac_tc.findall(qn('w:p')) if ptext(p).strip()]
            if ps:
                set_para_token(ps[0], "[[influencing_factors]]")
                for p in ps[1:]:
                    p.getparent().remove(p)
            break
    # quadrant column (30 Jul 2026 highlight format): the map image stays INLINE in
    # the direction table's third column, but three weekly artefacts are stripped so
    # the engine can regenerate them each run: (a) the sign chips under the direction
    # sentence; (b) the "Why this quadrant" heading + bullets; (c) the baked-in
    # highlight wash, by swapping the map image part for the CLEAN base map from the
    # prior template (engine/quadrant_base_map.png, extracted once from v5).
    for nt in ex.iter(qn('w:tbl')):
        if nt is ex:
            continue
        if "Weekly Direction" not in "".join(ptext(q) for q in nt.findall(qn('w:tr'))[0].iter(qn('w:p'))):
            continue
        trs_d = nt.findall(qn('w:tr'))
        if len(trs_d) < 2:
            continue
        body_tcs = trs_d[1].findall(qn('w:tc'))
        # (a) sign chips: any para in the direction cell mentioning a bare sign chip
        for tc in body_tcs[:1]:
            for q in list(tc.findall(qn('w:p'))):
                t_ = ptext(q).strip()
                if t_ and ("Inflation" in t_ or "Growth" in t_) and len(t_) < 60 and "[[" not in t_:
                    tc.remove(q)
        # (b) + (c) in the quadrant column
        if len(body_tcs) >= 3:
            qc = body_tcs[-1]
            kill = False
            for q in list(qc.findall(qn('w:p'))):
                t_ = ptext(q).strip()
                if t_.startswith("Why this quadrant"):
                    kill = True
                if kill and q.find('.//' + W_DRAW) is None:
                    qc.remove(q)
            base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quadrant_base_map.png")
            if os.path.exists(base):
                for blip in qc.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}blip'):
                    rid = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                    part = doc.part.related_parts.get(rid)
                    if part is not None:
                        part._blob = open(base, 'rb').read()
                        print("quadrant map reset to clean base")
                    break
            else:
                print("WARN: engine/quadrant_base_map.png missing — map keeps last week's wash")
        break
    # status dashboard: tokens + base-colour ovals
    sd = None
    for nt in ex.iter(qn('w:tbl')):
        if nt is ex:
            continue
        hr = nt.find(qn('w:tr'))
        if hr is not None and ptext(hr).strip().startswith("Theme"):
            sd = nt; break
    for tr in sd.findall(qn('w:tr'))[1:]:
        tcs = tr.findall(qn('w:tc'))
        stat_ps = [p for p in tcs[1].findall(qn('w:p')) if ptext(p).strip()]
        if stat_ps:
            set_text_runs_token(stat_ps[0], "[[Status word]]")
            for p in stat_ps[1:]:
                if p.find('.//' + W_DRAW) is None and not any(e.tag == MC_AC_TAG for e in p.iter()):
                    p.getparent().remove(p)
        one_token_para(tcs[2], " NO_LABEL ", "[[One-line development]]")
        for el in tcs[1].iter():
            v = el.get('val')
            if v and v.upper() in LIGHT_VALS:
                el.set('val', "EE0000")
            if el.get('fillcolor'):
                el.set('fillcolor', "#e00")
    # key developments: keep ONE token row (bulleted dev cell | arrowed implication cell)
    trs = ex.findall(qn('w:tr'))
    hdr_i = next((i for i, tr in enumerate(trs)
                  if "".join(ptext(p) for p in tr.iter(qn('w:p'))).strip().startswith("Key Developments")), None)
    if hdr_i is not None:
        data_rows = trs[hdr_i + 1:]
        first = data_rows[0]
        tcs = first.findall(qn('w:tc'))
        one_token_para(tcs[0], " NO_LABEL ", TOK_KD_DEV)
        if len(tcs) > 1:
            one_token_para(tcs[1], " NO_LABEL ", TOK_KD_IMP)
        for tr in data_rows[1:]:
            tr.getparent().remove(tr)
    # else: exec keydev page retired 30 Jul 2026 — nothing to tokenise

    # ---------- theme blocks ----------
    def theme_tables():
        return [t for t in body.findall(qn('w:tbl')) if block_title(t).startswith("Theme")]

    def is_appendix(t):
        return "Appendix" in block_title(t)

    # 1) clean surviving keydev cells; remember a clean single-cell row to clone
    clean_kd_tr = None
    for t in theme_tables():
        kd = cell_containing(t, "Key Development of the Week")
        if kd is not None:
            clean_keydev_cell(kd)
            tr = row_of(t, kd)
            for tc in tr.findall('.//' + qn('w:tc')):
                if tc is kd:
                    continue
                if cell_text(tc).strip() or tc.find('.//' + W_DRAW) is not None:
                    for p in list(tc.findall(qn('w:p'))):
                        tc.remove(p)
                    tc.append(OxmlElement('w:p'))
            if clean_kd_tr is None and len(tr.findall('.//' + qn('w:tc'))) == 1:
                clean_kd_tr = tr
    # 1.5) restore Implication/Watch rows where a hand edit deleted them
    donor = next((t for t in theme_tables()
                  if cell_containing(t, "Implication for the theme") is not None
                  and cell_containing(t, "Watch next week") is not None), None)
    if donor is not None:
        d_impl_tr = row_of(donor, cell_containing(donor, "Implication for the theme"))
        for t in theme_tables():
            if cell_containing(t, "Implication for the theme") is None:
                t.append(copy.deepcopy(d_impl_tr))
    # 2) restore keydev rows where a hand edit deleted them — THEME blocks only;
    #    the Monetary appendix carries no keydev by design (17 Jul standard)
    if clean_kd_tr is not None:
        for t in theme_tables():
            if is_appendix(t):
                continue
            if cell_containing(t, "Key Development of the Week") is None:
                impl = cell_containing(t, "Implication for the theme")
                if impl is not None:
                    row_of(t, impl).addprevious(copy.deepcopy(clean_kd_tr))
                    print("restored keydev row in:", block_title(t)[:50])

    for t in theme_tables():
        ttl = block_title(t)
        # status line: token + strip Status Ball
        stat_tc = cell_containing(t, "Status")
        lab, content = label_and_content(stat_tc, "Status")
        if content:
            set_para_token(content[0], TOK_STATUS)
            for p in content[1:]:
                p.getparent().remove(p)
        elif lab is not None:
            set_para_token(lab, "Status: " + TOK_STATUS)
        # what changed / implication / watch
        wc = cell_containing(t, "What changed this week")
        if wc is not None:
            one_token_para(wc, "What changed this week", TOK_DEV)
        im = cell_containing(t, "Implication for the theme")
        if im is not None:
            one_token_para(im, "Implication for the theme", TOK_IMPL)
        wa = cell_containing(t, "Watch next week")
        if wa is not None:
            one_token_para(wa, "Watch next week", TOK_WATCH)
        # central-bank table (monetary): ONE token row (engine clones per JSON row)
        cb_tc = None
        for nt in t.iter(qn('w:tbl')):
            if nt is t:
                continue
            hr = nt.find(qn('w:tr'))
            if hr is not None and "Central Bank" in ptext(hr):
                rows = nt.findall(qn('w:tr'))[1:]
                ftcs = rows[0].findall(qn('w:tc'))
                for tc, tok in zip(ftcs, ["[[cb_bank]]", "[[cb_rate]]", "[[cb_cycle]]"]):
                    one_token_para(tc, " NO_LABEL ", tok)
                for r_ in rows[1:]:
                    r_.getparent().remove(r_)
                for anc in nt.iterancestors():
                    if anc.tag == qn('w:tc'):
                        cb_tc = anc
                        break
        # chart cells: any image-bearing cell that is not status / keydev / CB / labelled
        markers = list(SLOT_MARKERS.get(next((k for k in SLOT_MARKERS if ttl.startswith(k)), ""), []))
        kd = cell_containing(t, "Key Development of the Week")
        mi = 0
        for tc in t.findall('.//' + qn('w:tc')):
            if tc is stat_tc or tc is kd:
                continue
            if any(lbl in cell_text(tc) for lbl in
                   ("What changed", "Implication for the theme", "Watch next week", "Central Bank", "Theme")):
                continue
            n_imgs = len(tc.findall('.//' + W_DRAW))
            if n_imgs == 0:
                continue
            if tc is cb_tc or tc.find(qn('w:tbl')) is not None:
                # cell hosting the CB table with a chart above it: keep the table,
                # replace the image paragraph(s) with a marker
                for p in list(tc.findall(qn('w:p'))):
                    if p.find('.//' + W_DRAW) is not None:
                        m = markers[mi] if mi < len(markers) else None
                        p.addprevious(marker_para(m))
                        mi += 1
                        tc.remove(p)
                continue
            mi = strip_chart_cell(tc, markers, mi)

    # ---------- references ----------
    children = list(body.iterchildren())
    last_tbl = body.findall(qn('w:tbl'))[-1]
    zone = children[children.index(last_tbl) + 1:]
    intro_done, item_kept = False, False
    for ch in zone:
        if ch.tag != qn('w:p'):
            continue
        txt = ptext(ch).strip()
        if not txt:
            continue
        if not intro_done and txt.startswith("Only sources"):
            set_para_token(ch, TOK_REF_INTRO)
            intro_done = True
            continue
        if txt.startswith("(Tier"):
            if not item_kept:
                set_para_token(ch, TOK_REF_ITEM)
                item_kept = True
            else:
                body.remove(ch)
            continue
        if intro_done and (txt.startswith("Theme") or txt.startswith("Executive Summary")
                           or txt.startswith("Monetary Policy Tracker")):
            body.remove(ch)

    # ---------- stamps (dates may be SPLIT ACROSS RUNS) ----------
    PAT = re.compile(r'20\d\d_\d\d_\d\d')
    for para in body.iter(qn('w:p')):
        ts = [t for t in para.iter(qn('w:t'))]
        full = "".join(t.text or '' for t in ts)
        m = PAT.search(full)
        if not m:
            continue
        while m:
            s, e = m.span()
            pos = 0
            for t in ts:
                txt = t.text or ''
                a, b = pos, pos + len(txt)
                pos = b
                if b <= s or a >= e:
                    continue
                pre = txt[:max(0, s - a)]
                post = txt[e - a:] if e <= b else ''
                t.text = (pre + 'YYYY_MM_DD' + post) if a <= s else post
                t.set(qn('xml:space'), 'preserve')
            full = "".join(t.text or '' for t in ts)
            m = PAT.search(full)

    doc.save(out)
    print("template written:", out)

if __name__ == "__main__":
    main()
