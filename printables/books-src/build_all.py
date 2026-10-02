#!/usr/bin/env python3
"""One printable book from all five: each day is four pages that flow together
(Journal → Standing → Standing → Coming Home), followed by the Reference Library
(Workbook and Volume II). Assembled from the already-built per-book HTML so the
text is identical to the standalone books. Run build.py first.
"""
import os
import re

from lxml import etree, html as LH

import html as _html
import lib
import art_pages as A
from lib import BRAND, esc
from mdbook import mk

OUT = lib.OUT
MK = re.compile(r'<span class="mk">§H\d+§</span>')

def load(slug):
    raw = open(os.path.join(OUT, slug + ".html"), encoding="utf-8").read()
    doc = LH.document_fromstring(raw)
    styles = "\n".join(s.text or "" for s in doc.findall(".//style"))
    body = doc.find("body")
    return styles, list(body)

def ser(el):
    return etree.tostring(el, encoding="unicode", method="html")

def h1(el):
    h = el.find(".//h1")
    return re.sub(r"§H\d+§", "", "".join(h.itertext())).strip() if h is not None else ""

def classes(el):
    return (el.get("class") or "").split()

def strip(s):
    return MK.sub("", s)

def tag(html, title, k):
    return html.replace(f"<h1>{title}</h1>", f"<h1>{title}{mk(k)}</h1>", 1)

JOURNAL_STYLES, J = load("90-days-of-freedom-journal")
STAND_STYLES, S = load("ninety-days-of-standing")
HOME_STYLES, H = load("ninety-days-of-coming-home")
WB_STYLES, W = load("trauma-and-the-spiritual-realm-workbook")
V2_STYLES, V = load("the-whole-story-volume-ii")

# ---------------- gather pieces ----------------
j_days = [e for e in J if "dayp" in classes(e) and h1(e) != "Begin Again"]
j_day91 = next(e for e in J if "dayp" in classes(e) and h1(e) == "Begin Again")
assert len(j_days) == 90, len(j_days)
j_by = {h1(e): e for e in J if "fm" in classes(e)}
s_days = [e for e in S if "sp" in classes(e)]
assert len(s_days) == 180
s_by = {h1(e): e for e in S if "fm" in classes(e)}
h_days = [e for e in H if "hd" in classes(e)]
assert len(h_days) == 90
h_by = {h1(e): e for e in H if "fm" in classes(e)}
h_jar = [e for e in H if "jar" in classes(e)]
h_letters = [e for e in H if "letter" in classes(e)]
wb_main = next(e for e in W if e.tag == "main")
v2_main = next(e for e in V if e.tag == "main")
v2_intro = next(e for e in V if "fm" in classes(e) and h1(e) == "Introduction")
j_cert = next(e for e in J if "cert" in classes(e))
j_closing = [e for e in J if h1(e) in ("Final Reflection", "Where I Am Now", "Next-Step Challenge")]
j_res = next(e for e in J if h1(e) == "Help, Right Now")

LAYER_FOOT = {"j": "The Journal · Write the truth", "s": "Standing · Understand and stand", "h": "Coming Home · Go to her"}

def fix_journal(e):
    s = ser(e)
    s = re.sub(r'<div class="pair">.*?</div>', "", s, flags=re.S)
    s = s.replace("Reaching back. Freeing the bound.", LAYER_FOOT["j"])
    return strip(s)

def fix_pairs(s, layer):
    s = re.sub(r'<div class="pairs">.*?(<b>Also read</b>)', r'<div class="pairs"><b>Same day, other pages:</b> Journal · Standing · Coming Home &nbsp;·&nbsp; <b>Go deeper</b>', s, flags=re.S, count=1)
    return s

def fix_standing(e):
    s = fix_pairs(ser(e), "s")
    s = s.replace("Ninety Days of Standing", LAYER_FOOT["s"]).replace("Reaching back. Freeing the bound.", LAYER_FOOT["s"])
    return strip(s)

def fix_home(e):
    s = fix_pairs(ser(e), "h")
    s = s.replace("Ninety Days of Coming Home", LAYER_FOOT["h"])
    return strip(s)

# ---------------- arcs ----------------
ARCS = [(1, "Telling the Truth", 1, 10), (2, "The Lies and the Names", 11, 20), (3, "The Realm and Your Authority", 21, 30),
        (4, "The Contracts", 31, 45), (5, "The Bloodline", 46, 55), (6, "The Playbook and the Structure", 56, 68),
        (7, "God", 69, 76), (8, "Brandi and Letting Go", 77, 84), (9, "Becoming Her", 85, 90)]
ARC_COLORS = ["#27857f", "#7a4c9e", "#d6598f", "#4a6486", "#27857f", "#7a4c9e", "#d6598f", "#4a6486", "#c58a2d"]

def arc_review(n, title):
    c = ARC_COLORS[n - 1]
    q = [("What did I tell the truth about in this arc?", 5), ("What was hardest, and what helped?", 5), ("What do I want to carry into the next arc?", 5)]
    inner = "".join(f'<h3>{esc(a)}</h3><div class="lines5">{"<div></div>" * k}</div>' for a, k in q)
    return f'''<section class="fm revw" style="--ac:{c}"><div class="band"></div><div class="kick">Arc {n} review</div>
<h1 style="font-size:32pt">Looking Back: {esc(title)}</h1>
<p class="small">A few honest lines before you turn the page. This sheet also keeps each arc starting on a fresh sheet of paper for your binder.</p>{inner}</section>'''

def notes_page():
    return '<section class="fm revw"><div class="band"></div><div class="kick">Notes</div><h1>Notes</h1><div class="lines5">' + "<div></div>" * 24 + "</div></section>"

def arc_divider(n, title, a, b):
    row = lib.PATH_ROWS[n - 1]
    sub = f"The Journal: {title}. Standing: {row[2]}. Coming Home: {lib.HOME_STAGES[n - 1]}."
    return A.divider(A.PLATES[(n - 1) % 3], f"Arc {n} · Days {a}–{b}", title, sub, f"{b - a + 1} days · {4 * (b - a + 1)} pages", mk(100 + n))

def ref_divider(kicker, title, sub, k):
    return A.divider(A.PLATES[2], kicker, title, sub, "Reference Library", mk(k))

_OPEN = re.compile(r'<section class="opener"><div class="kicker">(?P<k>.*?)</div><h1>(?P<t>.*?)<span class="mk">(?P<m>§H\d+§)</span></h1><div class="orn"></div>(?:<div class="sub">(?P<s>.*?)</div>)?<div class="bm">.*?</div></section>', re.S)
_cnt = [0]
def art_openers(html_str):
    def rep(m):
        _cnt[0] += 1
        u = lambda x: _html.unescape(x or "")
        return A.divider(A.PLATES[_cnt[0] % 3], u(m.group("k")), u(m.group("t")), u(m.group("s")), "Reference Library", f'<span class="mk">{m.group("m")}</span>')
    return _OPEN.sub(rep, html_str)

# ---------------- front matter ----------------
HOW = f"""<section class="fm"><div class="band"></div><div class="kick">One book, five voices</div>
<h1>How This Book Works</h1>
<p>Five books became one so that every day lines up. For each of the ninety days you get <strong>four pages in a row</strong>, always in this order:</p>
<div class="ahead">
<div class="item"><div class="n">1</div><div><div class="t">The Journal page · Write the truth</div><p>A short teaching, a verse, a question to write on the lines, and a declaration to say out loud.</p></div></div>
<div class="item"><div class="n">2</div><div><div class="t">Standing, left page · Understand</div><p>Optional grounding, Scripture, and what it means: spiritual warfare, your mother, your father, your addiction, and ending the cycle.</p></div></div>
<div class="item"><div class="n">3</div><div><div class="t">Standing, right page · Stand</div><p>Three reflection prompts, one soft action, a prayer, and a declaration.</p></div></div>
<div class="item"><div class="n">4</div><div><div class="t">Coming Home page · Go to her</div><p>One step toward the child you were, a prayer, an affirmation, a challenge, and room to write what she said.</p></div></div>
</div>
<p style="margin-top:.14in"><strong>After the ninety days</strong> come the Challenge Jar (cut-out cards to draw at random), the three letters for Day 90, a final reflection, a certificate, and the help page. Then the <strong>Reference Library</strong>: the Workbook and Volume II, whole, for when a day says <em>Go deeper</em>. Every Reference section is listed with its page number in the Contents.</p>
<div class="safety"><h3>Pace yourself</h3><ul>
<li>Do all four pages in one sitting, or spread them across the day: Journal in the morning, Standing at midday, Coming Home at night. Both work.</li>
<li>You can do only one page on a hard day. Missing a day is not failure. Pick the page back up.</li>
<li>Stop whenever it is too much. Reach for a safe person or the numbers at the back.</li></ul></div></section>"""

def toc_section(entries, pmap):
    s = lib.toc_html(entries)
    for _, _, k in entries:
        s = s.replace(f"@@P{k}@@", pmap.get(str(k), ""))
    return s

def md_entries(main_html_el, offset, label):
    """Collect TOC entries (level, text, key) from headings carrying markers, remapping keys."""
    out = []
    for el in main_html_el.iter("h1", "h2"):
        m = re.search(r"§H(\d+)§", "".join(el.itertext()))
        if not m:
            continue
        key = int(m.group(1)) + offset
        title = re.sub(r"§H\d+§", "", "".join(el.itertext())).strip()
        lvl = 1 if el.tag == "h1" else 2
        if el.tag == "h1":
            par = el.getparent()
            kick = par.find(".//div[@class='kicker']") if par is not None else None
            if kick is not None and (kick.text or "").strip():
                title = f"{kick.text.strip()} — {title}"
        out.append((lvl, title, key))
    return out

def remap(el, offset):
    s = ser(el)
    return re.sub(r"§H(\d+)§", lambda m: f"§H{int(m.group(1)) + offset}§", s)

GUTTER_CSS = '''
@page:right{margin-left:1.05in;margin-right:.7in}
@page:left{margin-left:.7in;margin-right:1.05in}
@page day:right{margin-left:.95in;margin-right:.4in}
@page day:left{margin-left:.4in;margin-right:.95in}
@page cert:right{margin-left:.95in;margin-right:.35in}
@page cert:left{margin-left:.35in;margin-right:.95in}
.lines5 div{height:.3in;border-bottom:1.2px solid #d3c8e0}
'''

def build():
    wb_entries = md_entries(wb_main, 1000, "wb")
    v2_entries = md_entries(v2_main, 2000, "v2")
    front_entries = [(1, "How to Read This Book", 2), (1, "How This Book Works", 3), (1, "Your 90-Day Path", 4),
                     (1, "Going Back Safely", 6), (1, "Spiritual Warfare, Plainly", 7), (1, "A Word About Your Mother", 8),
                     (1, "The Prayer Over This Book", 9)]
    arc_entries = [(1, f"Arc {n} · {t} (Days {a}–{b})", 100 + n) for n, t, a, b in ARCS]
    mid_entries = [(1, "Day 91 · Begin Again", 60), (1, "The Challenge Jar", 61), (1, "A Letter From Her", 62),
                   (1, "A Letter From the New Me", 63), (1, "Our Promise", 64), (1, "Final Reflection", 50),
                   (1, "Where I Am Now", 51), (1, "Next-Step Challenge and Closing Prayer", 52), (1, "Certificate of Completion", 53),
                   (1, "Help, Right Now", 54)]
    ref_entries = [(1, "Reference One · Trauma and the Spiritual Realm Workbook", 70)] + wb_entries + \
                  [(1, "Reference Two · The Whole Story, Volume II", 71)] + v2_entries
    entries = front_entries + arc_entries + mid_entries + ref_entries
    keys = [str(k) for (_, _, k) in entries]

    rows = "".join(f"<tr><td><strong>{d}</strong></td><td>{esc(a)}</td><td>{esc(s)}</td><td>{esc(h)}</td><td>{esc(w)}</td><td>{esc(v)}</td></tr>"
                   for (d, a, s, w, v), h in zip(lib.PATH_ROWS, lib.HOME_STAGES))
    pathp = f"""<section class="fm"><div class="band"></div><div class="kick">The whole map</div><h1>Your 90-Day Path{mk(4)}</h1>
<p>Each arc has one theme, seen four ways. The last two columns tell you where to read more in the Reference Library when a day says <em>Go deeper</em>. (Workbook numbers are section numbers such as 2.4; Volume II numbers are chapters. Look them up in the Contents.)</p>
<table><thead><tr><th>Days</th><th>Journal arc</th><th>Standing focus</th><th>Coming Home stage</th><th>Workbook</th><th>Volume II</th></tr></thead><tbody>{rows}</tbody></table></section>"""

    def body(pmap, pad=False):
        parts = []
        parts.append(lib.cover("The 90-Day<br>Rebuild", "Journal · Standing · Coming Home · Workbook · Volume II", "You survived. Now we rebuild.",
                               "Four pages a day for ninety days,<br>with the whole reference library behind them"))
        parts.append(lib.title_page("The 90-Day<br>Rebuild", "One book, five voices<br>Write the truth. Understand it. Stand. Go to her. Then go deeper.",
                                    "For Brandi Renee — and for the little girl who was not protected, and the woman who is standing now."))
        parts.append(lib.copyright_page("The 90-Day Rebuild — The Journal, Standing, Coming Home, the Workbook, and Volume II in One Book"))
        parts.append(toc_section(entries, pmap))
        parts.append(tag(strip(ser(j_by["How to Read This Book"])), "How to Read This Book", 2))
        parts.append(HOW.replace("<h1>How This Book Works</h1>", f"<h1>How This Book Works{mk(3)}</h1>"))
        parts.append(pathp)
        parts.append(tag(strip(ser(h_by["Going Back Safely"])), "Going Back Safely", 6))
        parts.append(tag(strip(ser(s_by["Spiritual Warfare, Plainly"])), "Spiritual Warfare, Plainly", 7))
        parts.append(tag(strip(ser(s_by["A Word About Your Mother"])), "A Word About Your Mother", 8))
        parts.append(tag(strip(ser(j_by["The Prayer Over This Book"])), "The Prayer Over This Book", 9))
        if pad:
            parts.append(notes_page())
        for n, t, a, b in ARCS:
            parts.append(arc_divider(n, t, a, b))
            for d in range(a, b + 1):
                parts.append(fix_journal(j_days[d - 1]))
                parts.append(fix_standing(s_days[2 * (d - 1)]))
                parts.append(fix_standing(s_days[2 * (d - 1) + 1]))
                parts.append(fix_home(h_days[d - 1]))
            parts.append(arc_review(n, t))
        parts.append(fix_journal(j_day91).replace("Begin Again</h1>", f"Begin Again{mk(60)}</h1>", 1))
        jar = "".join(strip(ser(e)) for e in h_jar)
        parts.append(jar.replace("<h2>The Challenge Jar</h2>", f"<h2>The Challenge Jar{mk(61)}</h2>", 1) if "<h2>The Challenge Jar" in jar else jar)
        letters = "".join(strip(ser(e)) for e in h_letters)
        for t_, k_ in (("A Letter From Her", 62), ("A Letter From the New Me", 63), ("Our Promise", 64)):
            letters = letters.replace(f"<h1>{t_}</h1>", f"<h1>{t_}{mk(k_)}</h1>", 1)
        parts.append(letters)
        for e, (t_, k_) in zip(j_closing, (("Final Reflection", 50), ("Where I Am Now", 51), ("Next-Step Challenge", 52))):
            parts.append(tag(strip(ser(e)), t_, k_))
        cert = A.certificate("The 90-Day Rebuild", mk(53))
        parts.append(cert)
        parts.append(tag(strip(ser(j_res)), "Help, Right Now", 54))
        parts.append(ref_divider("Reference One", "Trauma and the Spiritual Realm", "The Workbook, whole. Come here when a day says Go deeper.", 70))
        parts.append(art_openers(remap(wb_main, 1000)))
        parts.append(ref_divider("Reference Two", "The Whole Story, Volume II", "The master companion, whole: contracts, family patterns, the enemy's playbook, where God was, and the step-by-step unraveling.", 71))
        parts.append(strip(ser(v2_intro)))
        parts.append(art_openers(remap(v2_main, 2000)))
        return "\n".join(parts)

    css = "\n".join([JOURNAL_STYLES, STAND_STYLES, HOME_STYLES, A.CSS, GUTTER_CSS])
    html_path = os.path.join(OUT, "the-90-day-rebuild.html")
    pdf_path = os.path.join(OUT, "the-90-day-rebuild.pdf")
    title = "The 90-Day Rebuild"
    page = lambda t, b_: f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{esc(t)}</title><style>{css}\n.mk{{font-size:2px;line-height:0;color:rgba(255,255,255,.01);letter-spacing:0}}</style></head><body>{b_}</body></html>"
    def render(pmap, pad):
        open(html_path, "w").write(page(title, body(pmap, pad)))
        lib.render_pdf(html_path, pdf_path)
        return lib.find_marker_pages(pdf_path, keys)
    pmap = {k: "000" for k in keys}
    found, n = render(pmap, False)
    pad = int(found["101"]) % 2 == 1          # first arc divider must land on a back (even) page
    if pad:
        found, n = render(pmap, True)
    pmap = {k: str(found.get(k, "")) for k in keys}
    f2, n2 = render(pmap, pad)
    if any(f2.get(k) != found.get(k) for k in keys):
        print("  warn: page numbers shifted")
    odd = [k for k in ("101","102","103","104","105","106","107","108","109") if int(f2[k]) % 2 == 1]
    print("  arc dividers on odd pages (should be none):", odd, "| padded front:", pad)
    print(f"the-90-day-rebuild: {n2} pages -> {pdf_path}")

if __name__ == "__main__":
    build()
