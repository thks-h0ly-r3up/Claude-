"""Shared layout, colors, front/back matter and PDF rendering for the 7HE H0LY R3UP books."""
import html as _html
import os
import re

BRAND = "7HE H0LY R3UP"
BRAND_CO = "7HE H0LY R3UP & CO."
DATE = "September 30, 2026"
YEAR = "2026"
MEMORIAL = "In Memory of Brandi Renee — 12787–121721"

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)            # printables/

def esc(s):
    return _html.escape(s, quote=False)

def inline(s):
    """Escape plain text, then allow *italic* and **bold**."""
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    return s

# --------------------------------------------------------------------------
# CSS  (palette and type match the current printables: turquoise / purple /
# pink / denim on cream, Caveat headings, Libre Franklin body, gradient band)
# --------------------------------------------------------------------------
def fonts_css():
    return open(os.path.join(HERE, "fonts.css")).read()

CSS = r"""
:root{
  --pink:#d6598f; --purple:#7a4c9e; --turquoise:#3fb6b0; --turq-d:#27857f;
  --denim:#4a6486; --cream:#fdfaf5; --ink:#2b2430; --line:#c9bfd6;
  --gold:#e3a94b; --peach:#f4c9a5; --paper:#ffffff;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#fff;color:var(--ink);
  font-family:'Libre Franklin',Arial,sans-serif;font-size:10pt;line-height:1.55;
  -webkit-print-color-adjust:exact;print-color-adjust:exact}

/* ---------- page setup ---------- */
@page{size:8.5in 11in;margin:0.7in 0.78in 0.85in;
  @bottom-left{content:"7HE H0LY R3UP";width:3.2in;white-space:nowrap;text-align:left;font:700 7pt 'Libre Franklin';letter-spacing:.18em;color:#7a4c9e;vertical-align:top;padding-top:.22in}
  @bottom-right{content:counter(page);width:1in;text-align:right;font:700 8.5pt 'Libre Franklin';color:#7a4c9e;vertical-align:top;padding-top:.2in}
  @bottom-center{content:"";border-top:1.5px solid #c9bfd6;width:100%;vertical-align:top;margin-top:.1in}
}
@page cover{margin:0;@bottom-left{content:none}@bottom-right{content:none}@bottom-center{content:none}}
@page opener{margin:0;@bottom-left{content:none}@bottom-right{content:none}@bottom-center{content:none}}
@page cert{margin:.35in;@bottom-left{content:none}@bottom-center{content:none}@bottom-right{content:counter(page);font:700 8pt 'Libre Franklin';color:#7a4c9e}}
@page day{margin:.38in .5in .42in;
  @bottom-left{content:none}@bottom-center{content:none}
  @bottom-right{content:counter(page);font:700 8pt 'Libre Franklin';color:#7a4c9e;vertical-align:bottom}}

.cover{page:cover;width:8.5in;height:11in;break-after:page;position:relative;overflow:hidden}
.opener{page:opener;width:8.5in;height:11in;break-before:page;break-after:page;position:relative;overflow:hidden}
.cert{page:cert;height:10.25in;break-before:page;break-after:page;position:relative}
.dayp{page:day;height:10.12in;break-after:page;position:relative;display:flex;flex-direction:column}

/* ---------- cover ---------- */
.cover{background:linear-gradient(180deg,#7a4c9e 0%,#d6598f 38%,#f4c9a5 66%,#e3a94b 100%)}
.cover .leather{position:absolute;left:0;right:0;top:0;height:6.25in;
  background-color:#2f9e98;
  background-image:
    radial-gradient(rgba(255,255,255,.10) 1px,transparent 1.4px),
    radial-gradient(rgba(0,0,0,.10) 1px,transparent 1.6px),
    linear-gradient(160deg,#3fb6b0 0%,#2a8f8a 55%,#23807b 100%);
  background-size:7px 7px,11px 11px,100% 100%;background-position:0 0,3px 4px,0 0;
  clip-path:polygon(0 0,100% 0,100% 94%,96% 96%,91% 93.5%,86% 96%,80% 94%,74% 96.5%,68% 94%,62% 96%,55% 93.5%,49% 96.5%,43% 94%,37% 96%,30% 93.5%,24% 96%,17% 94%,11% 96.5%,5% 94%,0 96%)}
.cover .stitch{position:absolute;left:.32in;right:.32in;top:.32in;height:5.5in;border:2px dashed rgba(253,250,245,.75);border-radius:10px}
.cover .denim{position:absolute;left:0;right:0;bottom:0;height:4.05in;
  background-color:#4a6486;
  background-image:
    repeating-linear-gradient(45deg,rgba(255,255,255,.07) 0 1px,transparent 1px 4px),
    repeating-linear-gradient(-45deg,rgba(0,0,0,.10) 0 1px,transparent 1px 4px),
    linear-gradient(180deg,#56729a,#3c5474);
  clip-path:polygon(0 9%,4% 6%,9% 9.5%,15% 6.5%,22% 10%,29% 6%,35% 9%,42% 5.5%,48% 9.5%,55% 6%,62% 10%,69% 6.5%,75% 9%,82% 5.5%,88% 9.5%,94% 6.5%,100% 9%,100% 100%,0 100%)}
.cover .denim:before{content:"";position:absolute;left:.4in;right:.4in;bottom:.35in;top:.85in;border:2px dashed rgba(244,201,165,.75);border-radius:8px}
.cover .inner{position:absolute;left:0;right:0;top:.72in;text-align:center;color:var(--cream)}
.cover .kicker{font:800 10pt 'Libre Franklin';letter-spacing:.42em;text-transform:uppercase;color:#f8e4b9}
.cover .emblem{margin:.18in auto .02in;width:1.25in;height:1.25in}
.cover h1{font:700 70pt/0.92 'Caveat';margin:.08in .6in 0;color:#fffaf0;text-shadow:0 3px 0 rgba(20,60,62,.45),0 0 18px rgba(20,60,62,.35)}
.cover .subtitle{font:700 12.5pt 'Libre Franklin';letter-spacing:.2em;text-transform:uppercase;margin:.14in .7in 0;color:#fff3d6}
.cover .tag{position:absolute;left:0;right:0;top:6.3in;text-align:center;font:700 26pt 'Caveat';color:#fff6e0;text-shadow:0 2px 6px rgba(0,0,0,.35)}
.cover .lower{position:absolute;left:.9in;right:.9in;bottom:.75in;text-align:center;color:#fdfaf5}
.cover .lower .by{font:600 10.5pt 'Libre Franklin';line-height:1.5;color:#fdf1dc}
.cover .lower .mark{font:800 9.5pt 'Libre Franklin';letter-spacing:.3em;text-transform:uppercase;margin-top:.14in;color:#f8e4b9}
.cover .lower .mark2{font:700 8pt 'Libre Franklin';letter-spacing:.22em;text-transform:uppercase;margin-top:.05in;color:#f4c9a5}

/* ---------- front matter ---------- */
.fm{break-before:page}
.fm h1{font:700 40pt/1 'Caveat';color:var(--purple);margin:0 0 .04in}
.fm .band,.band{height:7px;width:100%;background:linear-gradient(90deg,var(--turquoise),var(--purple) 55%,var(--pink));border-radius:4px;margin:0 0 .14in}
.fm .kick{font:800 8.5pt 'Libre Franklin';letter-spacing:.22em;text-transform:uppercase;color:var(--denim)}
.fm h2{font:700 24pt 'Caveat';color:var(--purple);margin:.22in 0 .05in;border:0}
.fm p{margin:0 0 .1in}
.small{font-size:8.3pt;line-height:1.45;color:#4a4254}
.center{text-align:center}
.titlepage{text-align:center;padding-top:1.3in}
.titlepage .brand{font:800 10pt 'Libre Franklin';letter-spacing:.35em;color:var(--purple);text-transform:uppercase}
.titlepage h1{font:700 58pt/.95 'Caveat';color:var(--purple);margin:.25in .3in .05in}
.titlepage .sub{font:700 12pt 'Libre Franklin';letter-spacing:.14em;text-transform:uppercase;color:var(--denim);margin:.1in .6in}
.titlepage .ded{font:700 19pt/1.3 'Caveat';color:var(--pink);margin:.55in 1in 0}
.titlepage .rule{height:5px;width:2.2in;background:linear-gradient(90deg,var(--turquoise),var(--purple),var(--pink));margin:.3in auto;border-radius:3px}
.legal{font-size:7.9pt;line-height:1.45;color:#4a4254}
.legal p{margin:0 0 .07in}
.legal h3{font:800 8pt 'Libre Franklin';letter-spacing:.14em;text-transform:uppercase;color:var(--purple);margin:.12in 0 .04in;border:0;padding:0}

.lenses{display:grid;grid-template-columns:1fr 1fr;gap:.12in .16in;margin:.12in 0}
.lens{border:1.5px solid var(--line);border-radius:12px;padding:.1in .14in .11in;background:#fff;position:relative;break-inside:avoid}
.lens .chip{position:absolute;top:-10px;left:12px;color:#fff;font:800 7.5pt 'Libre Franklin';letter-spacing:.12em;text-transform:uppercase;padding:2px 10px;border-radius:20px}
.lens p{margin:.06in 0 0;font-size:8.8pt;line-height:1.45}
.c1 .chip{background:var(--turq-d)}.c2 .chip{background:var(--purple)}.c3 .chip{background:var(--pink)}.c4 .chip{background:var(--denim)}

.ahead{display:grid;grid-template-columns:1fr;gap:.09in;margin-top:.1in}
.ahead .item{display:flex;gap:.14in;border:1.5px solid var(--line);border-radius:12px;padding:.08in .14in;background:#fff;break-inside:avoid}
.ahead .item .n{flex:0 0 .55in;font:700 22pt/1 'Caveat';color:var(--purple);text-align:center;padding-top:.02in}
.ahead .item .t{font:800 8.5pt 'Libre Franklin';letter-spacing:.08em;text-transform:uppercase;color:var(--denim)}
.ahead .item p{margin:.02in 0 0;font-size:8.8pt;line-height:1.42}

.safety{border:2px solid var(--pink);border-radius:12px;padding:.1in .16in;background:#fff7fb;margin:.14in 0;break-inside:avoid}
.safety h3{margin:0 0 .04in;border:0;padding:0;font:800 8.5pt 'Libre Franklin';letter-spacing:.14em;text-transform:uppercase;color:var(--pink)}
.safety p,.safety li{font-size:8.9pt;line-height:1.45;margin:0 0 .04in}
.safety ul{margin:.02in 0 0 .2in;padding:0}

/* ---------- table of contents ---------- */
.toc h1{font:700 40pt/1 'Caveat';color:var(--purple);margin:0 0 .06in}
.toc .e{display:flex;align-items:baseline;gap:.06in;font-size:9pt;line-height:1.35;margin:0}
.toc .e .t{flex:0 1 auto}
.toc .e .d{flex:1 1 auto;border-bottom:1.2px dotted #b4a6c6;height:.7em;min-width:.3in}
.toc .e .p{flex:0 0 auto;font-weight:700;color:var(--purple)}
.toc .e1{margin-top:.1in;font-weight:800;text-transform:uppercase;letter-spacing:.05em;font-size:8.6pt;color:var(--purple)}
.toc .e2{padding-left:.2in;color:#3a3142}

/* ---------- part / book openers ---------- */
.opener{background:linear-gradient(175deg,#2a8f8a 0%,#7a4c9e 52%,#d6598f 100%);color:#fff;display:flex;flex-direction:column;justify-content:center;padding:1in 1in}
.opener:before{content:"";position:absolute;inset:.35in;border:2px dashed rgba(253,250,245,.65);border-radius:14px}
.opener:after{content:"";position:absolute;left:0;right:0;bottom:0;height:.55in;background:linear-gradient(90deg,#f4c9a5,#e3a94b)}
.opener .kicker{font:800 11pt 'Libre Franklin';letter-spacing:.4em;text-transform:uppercase;color:#ffe9b8;margin-bottom:.12in}
.opener h1{font:700 54pt/1 'Caveat';margin:0;color:#fffaf0;text-shadow:0 2px 14px rgba(0,0,0,.3);border:0}
.opener .sub{font:600 13pt/1.45 'Libre Franklin';font-style:italic;margin-top:.22in;color:#fff3de;max-width:5.6in}
.opener .orn{height:4px;width:1.6in;background:linear-gradient(90deg,#f4c9a5,#e3a94b);border-radius:3px;margin:.28in 0}
.opener .bm{position:absolute;bottom:.75in;left:1in;font:800 8.5pt 'Libre Franklin';letter-spacing:.3em;text-transform:uppercase;color:#fff3de}

/* ---------- body typography ---------- */
h2{font:700 27pt/1.05 'Caveat';color:var(--purple);margin:.34in 0 .1in;padding-bottom:.04in;
  border-bottom:3px solid transparent;border-image:linear-gradient(90deg,var(--turquoise),var(--purple) 55%,var(--pink)) 1;break-after:avoid}
h2.chapter{break-before:page;margin-top:0}
h3{font:800 9.6pt/1.3 'Libre Franklin';letter-spacing:.07em;text-transform:uppercase;color:var(--denim);
  border-left:5px solid var(--turquoise);padding:.02in 0 .02in .1in;margin:.22in 0 .09in;break-after:avoid}
h4{font:800 9.6pt 'Libre Franklin';color:var(--purple);margin:.16in 0 .05in;break-after:avoid}
p{margin:0 0 .11in;orphans:3;widows:3}
strong{font-weight:700;color:#1d1822}
em{font-style:italic}
ul,ol{margin:0 0 .12in .24in;padding:0}
li{margin:0 0 .04in}
ul.chk{list-style:none;margin-left:.04in}
ul.chk li{padding-left:.26in;position:relative}
ul.chk li .box{position:absolute;left:0;top:.06em}
.box{display:inline-block;width:10px;height:10px;border:1.7px solid var(--purple);border-radius:2.5px;vertical-align:-1px;margin-right:5px}
hr{border:0;height:2px;width:1.6in;margin:.2in auto;background:linear-gradient(90deg,var(--turquoise),var(--purple),var(--pink));border-radius:2px}
.fill{display:inline-block;border-bottom:1.4px solid #8f82a3;height:.95em;vertical-align:baseline;margin:0 2px}
td .fill{width:.6in}

table{border-collapse:separate;border-spacing:0;width:100%;margin:.1in 0 .16in;font-size:8.7pt;line-height:1.35;
  border:1.5px solid var(--line);border-radius:10px;overflow:hidden}
thead{display:table-header-group}
tr{break-inside:avoid}
th{background:linear-gradient(90deg,#27857f,#7a4c9e);color:#fff;font-weight:700;text-align:left;padding:5px 7px;vertical-align:bottom}
td{padding:5px 7px;border-top:1px solid #e3dcec;border-right:1px solid #eee8f3;vertical-align:top}
td:last-child,th:last-child{border-right:0}
tbody tr:nth-child(even) td{background:#faf7fc}
tr.blank td{height:.36in}
table.wide{font-size:6.6pt}
table.wide th,table.wide td{padding:3px 3px}
table.wide th{font-size:6.4pt}

blockquote{margin:.14in 0;padding:0}
blockquote p:last-child{margin-bottom:0}
blockquote.verse{background:linear-gradient(90deg,rgba(63,182,176,.14),rgba(214,89,143,.09));border-radius:12px;padding:.1in .22in;text-align:center;
  font:600 14.5pt/1.25 'Caveat';color:var(--ink);break-inside:avoid}
blockquote.verse em{font-style:normal}
blockquote.prayer,blockquote.decl{background:#fff;border:1.5px solid var(--line);border-left:7px solid var(--pink);border-radius:10px;padding:.2in .2in .11in;margin:.26in 0 .16in;font-size:9.5pt}
blockquote.prayer:before,blockquote.decl:before{display:block;width:max-content;margin:-.3in 0 .07in -.06in;color:#fff;font:800 7.6pt 'Libre Franklin';letter-spacing:.14em;text-transform:uppercase;padding:2px 11px;border-radius:20px}
blockquote.prayer:before{content:"Prayer";background:var(--pink)}
blockquote.decl:before{content:"Say it out loud";background:var(--purple)}
blockquote.decl{border-left-color:var(--purple)}
blockquote.epigraph{border-left:0;text-align:center;font:600 12pt/1.5 'Libre Franklin';font-style:italic;color:#3a3142;background:#fff;border:1.5px solid var(--line);border-radius:12px;padding:.14in .3in;margin:.1in 0 .2in}
blockquote.prayer h2,blockquote.decl h2{font-size:20pt;border:0;margin:0 0 .05in;text-align:center}

blockquote.prayer,blockquote.decl,blockquote.verse{break-inside:avoid}
p:has(+blockquote.prayer),p:has(+blockquote.decl){break-after:avoid}
.writing{margin:.06in 0 .16in;break-inside:auto}
.writing .wl{height:.31in;border-bottom:1.3px solid var(--line)}
.writing .wrow{display:flex;align-items:flex-end;gap:7px;min-height:.31in;line-height:1.3}
.writing .wrow .fill{flex:1;height:.27in;margin:0}
.writing .wrow span.tx{padding-bottom:2px;white-space:nowrap}

.work{break-inside:avoid;border:1.6px solid var(--line);border-radius:16px;padding:.27in .24in .14in;background:#fff;position:relative;margin:.3in 0 .16in}
.work>h3{display:inline-block;margin:-.43in 0 .08in -.02in;border:0;color:#fff;background:linear-gradient(90deg,var(--pink),var(--purple));
  padding:3px 13px;border-radius:20px;font-size:8.6pt;letter-spacing:.1em}
.work>p:first-of-type{margin-top:.02in}

.card3{border-left:6px solid var(--purple)}
"""

def page(title, body, extra_css=""):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{esc(title)}</title>
<style>{fonts_css()}
{CSS}
{extra_css}</style></head><body>
{body}
</body></html>"""

# --------------------------------------------------------------------------
# emblem: cross inside a vine wreath with a small anchor
# --------------------------------------------------------------------------
EMBLEM = """<svg class="emblem" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<circle cx="60" cy="60" r="54" fill="none" stroke="#f8e4b9" stroke-width="2.4"/>
<circle cx="60" cy="60" r="49" fill="none" stroke="#f8e4b9" stroke-width="1" stroke-dasharray="3 3"/>
<g fill="#fffaf0"><rect x="55.5" y="22" width="9" height="62" rx="2"/><rect x="38" y="38" width="44" height="9" rx="2"/></g>
<g fill="none" stroke="#fffaf0" stroke-width="3.2" stroke-linecap="round"><path d="M60 88v14"/><path d="M50 98c0 6 20 6 20 0"/><path d="M54 93h12"/></g>
<g fill="#f4c9a5"><path d="M24 70c-9-2-14-9-13-17 9 1 15 7 13 17z"/><path d="M30 82c-8-4-11-12-8-19 8 3 12 11 8 19z"/>
<path d="M96 70c9-2 14-9 13-17-9 1-15 7-13 17z"/><path d="M90 82c8-4 11-12 8-19-8 3-12 11-8 19z"/></g>
<g fill="none" stroke="#f4c9a5" stroke-width="2"><path d="M24 70c4 10 12 18 22 22"/><path d="M96 70c-4 10-12 18-22 22"/></g>
</svg>"""

def cover(title_html, subtitle, tagline, byline):
    return f"""<section class="cover">
<div class="leather"></div><div class="stitch"></div>
<div class="inner"><div class="kicker">{BRAND}</div>{EMBLEM}<h1>{title_html}</h1>
<div class="subtitle">{subtitle}</div></div>
<div class="tag">{tagline}</div>
<div class="denim"></div>
<div class="lower"><div class="by">{byline}</div><div class="mark">{BRAND}</div><div class="mark2">Bando to Vineyard</div></div>
</section>"""

SCRIPTURE_NOTICE = ("Scripture quotations are from the ESV® Bible (The Holy Bible, English Standard Version®), "
    "copyright © 2001 by Crossway, a publishing ministry of Good News Publishers. Used by permission. All rights reserved. "
    "Some verses are shortened with ellipses (…) or summarized; summaries are marked as references rather than quotations.")

DISCLAIMER = [
 ("Please read", "This book is a faith-based companion for reflection and practice. It is not medical, mental-health, legal, or addiction-treatment advice, and it does not replace a doctor, therapist, counselor, pastor, or emergency services. The author is not a licensed clinician. Prayer belongs beside — not in place of — treatment, medication, safe housing, and safety planning."),
 ("Your safety comes first", "If you are in danger, call 911 (or your local emergency number). If you are thinking about ending your life, call or text 988 (U.S.). If you are physically dependent on alcohol, benzodiazepines, or barbiturates, do not stop suddenly without medical supervision — withdrawal can be dangerous. The resource page at the back of the book lists additional help. Phone numbers and services change; please confirm them before you rely on them."),
 ("About the stories and ideas", "Personal testimony is shared as lived experience, not as a formula or a promise of any outcome. Interpretations of Scripture are labeled as interpretation and offered for you to test against the Bible and with wise, trusted people. Nothing in this book guarantees healing, deliverance, income, or any particular result."),
]

def copyright_page(full_title, extra_note=""):
    d = "".join(f"<h3>{esc(h)}</h3><p>{esc(p)}</p>" for h, p in DISCLAIMER)
    return f"""<section class="fm legal">
<div class="band"></div>
<h3>Copyright</h3>
<p><strong>{esc(full_title)}</strong><br>Created {DATE} · First edition</p>
<p>© {YEAR} {BRAND}. All rights reserved. No part of this work may be reproduced, distributed, copied, transmitted, or commercially exploited without prior written permission, except as permitted by applicable law.</p>
{d}
<h3>Scripture</h3><p>{esc(SCRIPTURE_NOTICE)}</p>
{extra_note}
<h3>In memory</h3><p>{esc(MEMORIAL)}</p>
<p class="center" style="margin-top:.3in;font:700 15pt 'Caveat';color:#d6598f">You survived. Now we rebuild.</p>
</section>"""

def title_page(title_html, subtitle, dedication):
    return f"""<section class="fm titlepage">
<div class="brand">{BRAND}</div>
<h1>{title_html}</h1><div class="rule"></div>
<div class="sub">{subtitle}</div>
<div class="ded">{dedication}</div>
</section>"""

LENSES = [
 ("c1", "What Scripture says", "Verses are quoted or cited by reference and read in context. Unless noted, quotations are from the ESV. When the Bible is clear, these pages say so plainly."),
 ("c2", "My testimony", "Places where I am sharing what I lived and what I am still learning. It is one woman's experience — not a rule for yours, and not a finished recovery story."),
 ("c3", "Interpretation and practice", "Pictures like doors, contracts, stages, and seasons are ways of seeing and tools to practice with. Christians hold different views on some of them. Test them; keep what helps."),
 ("c4", "Symbol and image", "Broken chains, vineyards, anchors, and re-ups are pictures of freedom and renewal. A page of writing can help you practice something new. It does not, by itself, break a curse or change God's mind."),
]

def how_to_read(intro_extra=""):
    chips = "".join(f'<div class="lens {c}"><span class="chip">{esc(t)}</span><p>{esc(p)}</p></div>' for c, t, p in LENSES)
    return f"""<section class="fm">
<div class="band"></div><div class="kick">Before you begin</div>
<h1>How to Read This Book</h1>
<p>I am not a doctor, therapist, or pastor. I am a survivor who is still building, reaching back with what I have learned, what Scripture actually teaches, and something practical you can use. Four kinds of writing share these pages, and I want you to know which is which:</p>
<div class="lenses">{chips}</div>
<div class="safety"><h3>A few honest ground rules</h3><ul>
<li>You can skip any exercise. You can keep your eyes open. You can use a different anchor — a cold glass of water, your feet on the floor, a hand on a pet. You never have to relive something to complete a page.</li>
<li>Prayers here are conversations with God, not formulas. Saying words out loud helps many people mean them; it does not force anything.</li>
<li>Not every struggle is spiritual, and not every hard day is an attack. Sleep, food, pain, grief, and old wounds are real too. Sort them out with people who know you.</li>
<li>Forgiving someone is not the same as trusting them again. Boundaries protect; they are not punishment. A relapse does not make you disposable.</li>
<li>If a page opens more than you can carry, stop. Reach for a safe person or one of the numbers at the back. The page will wait.</li></ul></div>
{intro_extra}
</section>"""

def ahead_page(kicker, title, items):
    rows = "".join(f'<div class="item"><div class="n">{esc(n)}</div><div><div class="t">{esc(t)}</div><p>{esc(d)}</p></div></div>' for n, t, d in items)
    return f"""<section class="fm"><div class="band"></div><div class="kick">{esc(kicker)}</div><h1>{esc(title)}</h1><div class="ahead">{rows}</div></section>"""

def toc_html(entries):
    """entries: list of (level, text, key)"""
    out = ['<section class="fm toc"><div class="band"></div><div class="kick">Table of contents</div><h1>Contents</h1>']
    for lvl, text, key in entries:
        out.append(f'<div class="e e{lvl}"><span class="t">{esc(text)}</span><span class="d"></span><span class="p">@@P{key}@@</span></div>')
    out.append("</section>")
    return "\n".join(out)

CLOSING_PRAYER = ("Father, thank You for walking with me through these pages. I did not do this perfectly, and You never asked me to. "
 "Where I told the truth, thank You for staying. Where I skipped, meet me there with patience. Where I found grief, hold me in it. "
 "Where I found anger, let me bring it to You instead of away from You. Give me safe people, good help, and a next step small enough to take. "
 "Keep me honest without letting me shame myself. Teach me to tend what You have given me — slowly, the way a vineyard is tended. "
 "I belong to You, and I am still building. In Jesus' name. Amen.")

def lines(n, h=".31in"):
    return '<div class="writing">' + '<div class="wl"></div>' * n + "</div>"

def closing_pages(book_title, units, unit_word, challenge):
    """Final reflection, progress review, next-step challenge, closing prayer."""
    rows = "".join(f"<tr><td style='height:.46in'><strong>{esc(u)}</strong></td><td></td><td></td><td></td></tr>" for u in units)
    return f"""<section class="fm"><div class="band"></div><div class="kick">Looking back</div>
<h1>Final Reflection</h1>
<p>Take your time. Answer in pencil if that feels safer. You are not grading yourself — you are noticing.</p>
<h3>What is one thing I told the truth about that I had been avoiding?</h3>{lines(4)}
<h3>Where did I feel the most resistance, and what might that be protecting?</h3>{lines(4)}
<h3>What is one thing that is different — even slightly — from when I started?</h3>{lines(4)}
<h3>What do I still need help with, and who could I ask?</h3>{lines(4)}
</section>
<section class="fm"><div class="band"></div><div class="kick">Progress review</div>
<h1>Where I Am Now</h1>
<p>Fill this in honestly. “Still hard” is an allowed answer. Finishing is not the same as being finished.</p>
<table><thead><tr><th style="width:2.1in">{esc(unit_word)}</th><th>What I finished or practiced</th><th>What shifted</th><th>What still needs care</th></tr></thead><tbody>{rows}</tbody></table>
</section>
<section class="fm"><div class="band"></div><div class="kick">Your next step</div>
<h1>Next-Step Challenge</h1>
<blockquote class="decl"><p>{inline(challenge)}</p></blockquote>
<h3>My one next step</h3>{lines(3)}
<h3>Who will know about it, and by when?</h3>{lines(2)}
<h3>What will I do if I miss a day?</h3>
<p class="small">Pick the page back up. Missing a day is not failure — the identity is in the rising.</p>{lines(2)}
<h2 style="margin-top:.3in">Closing Prayer</h2>
<blockquote class="prayer"><p>{esc(CLOSING_PRAYER)}</p></blockquote>
</section>"""

def certificate(title_line):
    return f"""<section class="cert">
<div style="position:absolute;inset:0;border:9px double #7a4c9e;border-radius:18px"></div>
<div style="position:absolute;inset:.22in;border:2px solid #3fb6b0;border-radius:12px"></div>
<div style="position:absolute;left:.5in;right:.5in;top:.5in;height:7px;background:linear-gradient(90deg,#3fb6b0,#7a4c9e 55%,#d6598f);border-radius:4px"></div>
<div style="position:absolute;left:.7in;right:.7in;top:1in;text-align:center">
<div style="font:800 10pt 'Libre Franklin';letter-spacing:.4em;color:#7a4c9e;text-transform:uppercase">{BRAND}</div>
<div style="font:700 50pt/1 'Caveat';color:#7a4c9e;margin-top:.2in">Certificate of Completion</div>
<div style="width:2.4in;height:4px;margin:.22in auto;background:linear-gradient(90deg,#f4c9a5,#e3a94b);border-radius:3px"></div>
<p style="font:600 11pt 'Libre Franklin';margin:.22in 0 .05in">This certifies that</p>
<div style="border-bottom:2px solid #8f82a3;height:.55in;margin:0 .6in"></div>
<div class="small" style="margin-top:.04in">Participant’s name</div>
<p style="font:600 11pt 'Libre Franklin';margin:.3in 0 .05in">has completed</p>
<div style="font:700 28pt/1.1 'Caveat';color:#d6598f;margin:.04in .3in">{title_line}</div>
<p style="font:600 10.5pt/1.5 'Libre Franklin';margin:.3in .6in 0;color:#3a3142">with honesty, courage, and grace for the days that were hard. Brokenness is not the destination. Keep going — one next step at a time.</p>
<div style="display:flex;gap:.7in;margin:.85in .3in 0">
<div style="flex:1"><div style="border-bottom:2px solid #8f82a3;height:.5in"></div><div class="small" style="margin-top:.04in">Signature</div></div>
<div style="flex:1"><div style="border-bottom:2px solid #8f82a3;height:.5in"></div><div class="small" style="margin-top:.04in">Date</div></div></div>
<div style="font:700 22pt 'Caveat';color:#7a4c9e;margin-top:.75in">You survived. Now we rebuild.</div>
<div style="font:800 8pt 'Libre Franklin';letter-spacing:.3em;color:#7a4c9e;margin-top:.25in;text-transform:uppercase">{BRAND_CO}</div>
</div></section>"""

RESOURCES = [
 ("988 Suicide & Crisis Lifeline", "Call or text 988 · free, 24/7, confidential"),
 ("Crisis Text Line", "Text HOME to 741741"),
 ("SAMHSA National Helpline (substance use, treatment referrals)", "1-800-662-4357 · free, 24/7, confidential"),
 ("National Domestic Violence Hotline", "1-800-799-7233, or text START to 88788"),
 ("RAINN (sexual assault)", "1-800-656-4673"),
 ("National Human Trafficking Hotline", "1-888-373-7888, or text 233733"),
 ("Veterans Crisis Line", "Dial 988, then press 1"),
]

def resources_page(extra_rows="", my_people=True):
    rows = "".join(f"<tr><td><strong>{esc(a)}</strong></td><td>{esc(b)}</td></tr>" for a, b in RESOURCES)
    people = ""
    if my_people:
        pr = "".join(f"<tr class='blank'><td>{esc(r)}</td><td></td><td></td></tr>" for r in ["Knows everything", "Further ahead", "Behind me", "Just a friend", "Can correct me"])
        people = f"<h3>My people</h3><table><thead><tr><th>Role</th><th>Name</th><th>Number</th></tr></thead><tbody>{pr}</tbody></table>"
    return f"""<section class="fm"><div class="band"></div><div class="kick">Keep this page</div>
<h1>Help, Right Now</h1>
<p>If you are in danger right now, or the thought of dying has teeth in it today, stop reading and call. That is not failure. That is the correct use of this page.</p>
<table><thead><tr><th style="width:3.3in">Need</th><th>Contact</th></tr></thead><tbody>{rows}{extra_rows}</tbody></table>
<div class="safety"><h3>Good to know</h3><ul>
<li><strong>Narcan (naloxone)</strong> is available without an individual prescription at most pharmacies, and free through many health departments and harm-reduction programs. Keep it in the house even if you do not use. It can reverse an opioid overdose and will not hurt someone who did not take opioids.</li>
<li><strong>Withdrawal from alcohol, benzodiazepines, and barbiturates can kill you.</strong> Do not detox from those alone. That is a medical detox, not a willpower problem. Call SAMHSA or go to an emergency room.</li>
<li>Numbers and services change. Confirm them before you rely on them.</li></ul></div>
{people}
<p class="center" style="margin-top:.25in"><span style="font:700 15pt 'Caveat';color:#d6598f">Reaching back. Freeing the bound.</span><br><span class="small" style="letter-spacing:.2em;text-transform:uppercase;font-weight:800;color:#7a4c9e">{BRAND_CO}</span></p>
</section>"""

# --------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------
def render_pdf(html_path, pdf_path):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/opt/pw-browsers/chromium", args=["--no-sandbox"])
        pg = b.new_page()
        pg.goto("file://" + html_path)
        pg.wait_for_timeout(800)
        pg.evaluate("document.fonts.ready")
        pg.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True)
        b.close()

def find_marker_pages(pdf_path, keys):
    import pymupdf
    doc = pymupdf.open(pdf_path)
    found = {}
    for i, pg in enumerate(doc):
        t = pg.get_text() or ""
        for m in re.finditer(r"§H(\d+)§", t):
            found.setdefault(m.group(1), i + 1)
    n = len(doc)
    doc.close()
    return found, n

def build_with_toc(title, build_body, toc_keys, html_path, pdf_path):
    """build_body(page_map) -> body html. Two passes so the TOC carries real page numbers."""
    pmap = {k: "000" for k in toc_keys}
    body = build_body(pmap)
    open(html_path, "w").write(page(title, body))
    render_pdf(html_path, pdf_path)
    found, n = find_marker_pages(pdf_path, toc_keys)
    missing = [k for k in toc_keys if k not in found]
    if missing:
        print("  warn: no page found for TOC keys", missing[:8])
    pmap = {k: str(found.get(k, "")) for k in toc_keys}
    body = build_body(pmap)
    open(html_path, "w").write(page(title, body))
    render_pdf(html_path, pdf_path)
    found2, n2 = find_marker_pages(pdf_path, toc_keys)
    drift = [k for k in toc_keys if found2.get(k) != found.get(k)]
    if drift:
        print("  warn: page numbers shifted after TOC fill:", drift[:8])
    return n2


# --------------------------------------------------------------------------
# the shared 90-day path (journal arcs = companion arcs = workbook/Vol. II reading)
# --------------------------------------------------------------------------
PATH_ROWS = [
 ("1–10", "Telling the Truth", "The war underneath: childhood, body, secrecy, a date", "Part I · Part V Steps 1–3", "Ch. 1, 10, 17 · Steps 1–2"),
 ("11–20", "The Lies and the Names", "Lies, names, and a mother’s moral injury", "1.5–1.6 · 4.3–4.4", "Ch. 10, 12, 48 · Step 31"),
 ("21–30", "The Realm and Your Authority", "Warfare, plainly: sorting, standing, forgiving", "Part II", "Ch. 1, 11, 15, 17 · Steps 8–10"),
 ("31–45", "The Contracts", "Vows, words, ties, the cistern, wanting out", "2.4–2.6", "Ch. 2–6 · Steps 13–15"),
 ("46–55", "The Bloodline", "Family patterns and the nursery", "Part VI", "Ch. 8–9 · Steps 16, 26"),
 ("56–68", "The Playbook and the Structure", "Patterns, cravings, daily structure, boundaries, falling", "Part V Steps 4–8", "Ch. 12–18 · Steps 23–29"),
 ("69–76", "God", "Where He was, honest anger, silence", "3.3 · 7.6", "Ch. 19–27"),
 ("77–84", "Brandi and Letting Go", "Grief, guilt, children out of reach, release", "Part VII", "Ch. 38–42 · Step 30"),
 ("85–90", "Becoming Her", "Stewarding what you have learned", "Part III", "Ch. 28–34, 46–52 · Step 32"),
]

HOME_STAGES = ["Build Her a Safe Place", "Meet Her at the Doorway", "Stand Guard for Her", "Release What She Promised", "Show Her Her Family Line", "Build Her a House", "Where Was Jesus?", "Say Goodbye and Hello", "Meet the New You"]

def path_page(title_note=""):
    rows = "".join(f"<tr><td><strong>{d}</strong></td><td>{esc(a)}</td><td>{esc(s)}</td><td>{esc(h)}</td><td>{esc(w)}</td><td>{esc(v)}</td></tr>" for (d, a, s, w, v), h in zip(PATH_ROWS, HOME_STAGES))
    return f"""<section class="fm"><div class="band"></div><div class="kick">One path, four books</div>
<h1>Your 90-Day Path</h1>
<p>These books were built to be used together. <strong>Day 7 in the journal is Day 7 in <em>Ninety Days of Standing</em> and Day 7 in <em>Ninety Days of Coming Home</em></strong>, and each day names the Workbook section and Volume II chapter that go with it. You do not have to read everything every day. Do the journal page; read the Standing spread; dip into the Workbook or Volume II when a day points you there.</p>
<table><thead><tr><th>Days</th><th>Journal arc</th><th>Standing focus</th><th>Coming Home stage</th><th>Workbook</th><th>Volume II</th></tr></thead><tbody>{rows}</tbody></table>
<div class="safety"><h3>A simple daily rhythm (about 25 minutes)</h3><ul>
<li><strong>Journal page:</strong> read it, write on the lines, say the declaration.</li>
<li><strong>Standing spread:</strong> optional grounding, Scripture, reflection, one soft action, a prayer.</li>
<li><strong>Coming Home page:</strong> one step toward the child you were, a prayer, an affirmation, and a small challenge.</li>
<li><strong>Workbook or Volume II:</strong> only when the day points you there, and only as much as you can hold.</li>
<li>Missed a day? Pick the page back up. The pace is the point, and the identity is in the rising.</li></ul></div>
</section>"""
