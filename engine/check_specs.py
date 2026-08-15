#!/usr/bin/env python3
"""Spec-consistency linter (v1, 13 Aug 2026) — the check_layout.py of the paper.

Born from the 13 Aug audit (runs/2026-08-13/spec_audit.md): 43 inconsistencies had
accumulated because nothing checked the specs the way check_layout checks the docx.
This gate turns spec drift into a same-day build failure. Run it in Phase 8 (weekly),
before committing a daily file (--daily <file>), and in both Routines; it must exit 0.

Checks:
  1. Version stamps agree: macrobasis_fill.py docstring == Format Spec title.
  2. Canonical strings hold: schema example topics are canonical; the Illiquids
     display title matches between _canonical, the engine default, and the schema
     template default; canonical status words unchanged.
  3. Banned patterns outside sanctioned lines (retirement/ban statements allowlisted):
     attach-era workflow language, Buy/Hold/Sell as a live instruction, a literal
     "Macro take:" template, the retired "exactly 3" factor rule, stale budgets.
  4. Sync stamps present in the companion docs (Evaluator, Charter, HANDOFF).
  5. runs/ contract: every runs/20* dir has the four checkpoint files or ABORTED.md.
  6. Daily-file skeleton (newest file, or --daily <file>): the README v2 template's
     required headers are present (enforced for files dated >= 2026-08-13).

Usage: python3 engine/check_specs.py [--daily <Monitoring News/YYYY-MM-DD_News.md>]
"""
import io, json, os, re, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fails = []


def check(cond, msg):
    print(("  PASS " if cond else "  FAIL ") + msg)
    if not cond:
        fails.append(msg)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
        return f.read()


# ---- 1. version stamps ----
print("== Version stamps ==")
fill = read("engine/macrobasis_fill.py")
spec = read("engine/MacroBasis_DOCX_Format_Spec.md")
m_fill = re.search(r"TEMPLATE-FILL engine \(v(\d+\.\d+)", fill)
m_spec = re.search(r"exact-match contract \(v(\d+\.\d+)", spec)
check(bool(m_fill and m_spec and m_fill.group(1) == m_spec.group(1)),
      f"engine docstring version == Format Spec title version "
      f"({m_fill and m_fill.group(1)} vs {m_spec and m_spec.group(1)})")

# ---- 2. canonical strings ----
print("== Canonical strings ==")
schema = json.loads(read("engine/content_schema.json"))
canon = schema["_canonical"]
topics = set(canon["reference_topics"])
example_topics = {g["topic"] for g in schema.get("references", []) if "topic" in g}
bad_topics = example_topics - topics
check(not bad_topics, f"schema references example uses only canonical topics (bad: {sorted(bad_topics)})")

title = canon.get("illiquids_display_title", "")
check(bool(title) and "Illiquid Assets" in title,
      "canonical illiquids_display_title set and check_layout-compatible")
check(title in fill, "engine build_illiquids_block default carries the canonical display title")
check(schema.get("illiquids", {}).get("title") == title,
      "schema template illiquids.title == canonical display title")
check(title in canon.get("block_order", []), "block_order carries the canonical display title")
check(canon["status_words"] == ["Escalating", "Held", "Deescalating"],
      "status words unchanged (Escalating/Held/Deescalating)")
check("budgets" in canon, "_canonical.budgets exists (single source for layout budgets)")

# ---- 3. banned patterns ----
print("== Banned patterns (allowlist: retirement/ban statements) ==")
SPECS = ["CLAUDE.md", "MacroBasis_Weekly_Run_Prompt.md", "MacroBasis_Evaluator.md",
         "MacroBasis_Theme_Charter.md", "HANDOFF.md", "memory/glossary.md",
         "memory/projects/macroagent.md", "engine/MacroBasis_DOCX_Format_Spec.md",
         "engine/content_schema.json"]
ALLOW = re.compile(r"retired|RETIRED|Retired|never|NEVER|not attached|no attachments|"
                   r"NOT|strip|banned|BANNED|was exactly 3|replaces the exactly-3|"
                   r"IS one of|reads? as|check_specs|spec_audit|Changelog|changelog")
BANNED = [
    (r"attached or pointed to|attach last week|attach that file|folder connected", "attach-era workflow language"),
    (r"Buy\s*/\s*Hold\s*/\s*Sell", "Buy/Hold/Sell as a live instruction"),
    (r"Macro take:", "literal 'Macro take:' as a template"),
    (r"exactly 3 short", "the retired exactly-3 factors rule"),
    (r"12-15 words", "the superseded 12-15 factor budget"),
    (r"180 words of PE news", "the superseded Illiquids budget"),
]
for pat, label in BANNED:
    hits = []
    rx = re.compile(pat)
    for rel in SPECS:
        for i, line in enumerate(read(rel).splitlines(), 1):
            if rx.search(line) and not ALLOW.search(line):
                hits.append(f"{rel}:{i}")
    check(not hits, f"no live '{label}' ({hits[:4]})")

# ---- 4. sync stamps ----
print("== Companion-doc sync stamps ==")
for rel in ["MacroBasis_Evaluator.md", "MacroBasis_Theme_Charter.md", "HANDOFF.md"]:
    check("Last synced against Run Prompt" in read(rel), f"{rel} carries a sync stamp")
rp = read("MacroBasis_Weekly_Run_Prompt.md")
m_rp = re.search(r"Run Prompt \(v(\d+\.\d+)", rp)
if m_rp:
    ver = m_rp.group(1)
    stale = [rel for rel in ["MacroBasis_Evaluator.md", "MacroBasis_Theme_Charter.md", "HANDOFF.md"]
             if f"Run Prompt v{ver}" not in read(rel)]
    check(not stale, f"sync stamps reference the current Run Prompt v{ver} (stale: {stale})")

# ---- 5. runs/ contract ----
print("== runs/ checkpoint contract ==")
REQ = {"ledger.md", "panel.md", "triage.md", "self_audit.md"}
bad_runs = []
runs_dir = os.path.join(ROOT, "runs")
for d in sorted(os.listdir(runs_dir)):
    p = os.path.join(runs_dir, d)
    if not (os.path.isdir(p) and d[:2] == "20"):
        continue
    names = set(os.listdir(p))
    if not (REQ <= names or "ABORTED.md" in names):
        bad_runs.append(d)
check(not bad_runs, f"every run dir complete or marked ABORTED (bad: {bad_runs})")

# ---- 6. daily-file skeleton ----
print("== Daily-file skeleton (README v2 template) ==")
REQUIRED_HEADERS = ["## Weekly signal (interpretive", "## Top of the tape",
                    "## Market tape snapshot", "## Watch (next 7 days)",
                    "## Checked, nothing found", "## Key links"]
daily = None
if "--daily" in sys.argv:
    daily = sys.argv[sys.argv.index("--daily") + 1]
else:
    mn = os.path.join(ROOT, "Monitoring News")
    cands = sorted(f for f in os.listdir(mn) if re.match(r"\d{4}-\d{2}-\d{2}_News\.md$", f))
    daily = os.path.join("Monitoring News", cands[-1]) if cands else None
if daily:
    base = os.path.basename(daily)
    if base[:10] >= "2026-08-13":     # relay-era files are exempt (see CLAUDE.md)
        txt = read(daily)
        missing = [h for h in REQUIRED_HEADERS if h not in txt]
        check(not missing, f"{base} matches the README v2 skeleton (missing: {missing})")
    else:
        print(f"  SKIP {base} predates the GitHub-native monitor (13 Aug 2026)")
else:
    print("  SKIP no daily file found")

print(f"\nFailures: {len(fails)}")
sys.exit(1 if fails else 0)
