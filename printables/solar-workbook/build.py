#!/usr/bin/env python3
"""Builds the 7HE H0LY R3UP Solar Workbook (HTML + PDF) from data/*.txt.

Usage:  python3 build.py            -> writes solar-workbook.html and solar-workbook.pdf
        python3 build.py --check    -> also reports any page whose content overflows
"""
import datetime as dt
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
START = dt.date(2026, 10, 7)          # Day 1 (a Wednesday)
TOTAL_DAYS = 91
BRAND = "7HE H0LY R3UP"
BOOK = "The Solar Workbook"

# ---------------------------------------------------------------- calendars
ETH_MONTHS = ["Meskerem", "Tikimt", "Hidar", "Tahsas", "Tir", "Yekatit", "Megabit",
              "Miazia", "Ginbot", "Sene", "Hamle", "Nehasse", "Pagume"]


def ethiopian(d):
    """Gregorian date -> (year, month index 1-13, day) in the Ethiopian calendar."""
    jdn = d.toordinal() + 1721425
    era = 1723856
    r = (jdn - era) % 1461
    n = (r % 365) + 365 * (r // 1460)
    year = 4 * ((jdn - era) // 1461) + r // 365 - r // 1460
    return year, n // 30 + 1, n % 30 + 1


# self-test against dates I can state with confidence
assert ethiopian(dt.date(2026, 9, 11)) == (2019, 1, 1), ethiopian(dt.date(2026, 9, 11))
assert ethiopian(dt.date(2027, 1, 7)) == (2019, 4, 29), ethiopian(dt.date(2027, 1, 7))
assert ethiopian(dt.date(2023, 9, 12)) == (2016, 1, 1), ethiopian(dt.date(2023, 9, 12))


def eth_str(d, short=False):
    y, m, dd = ethiopian(d)
    name = ETH_MONTHS[m - 1]
    return f"{name} {dd}" if short else f"{name} {dd}, {y} E.C."


def day_date(n):
    return START + dt.timedelta(days=n - 1)


def month_of(n):
    return 1 if n <= 30 else 2 if n <= 60 else 3


def day_in_month(n):
    return n if n <= 30 else n - 30 if n <= 60 else n - 60


def month_len(m):
    return 31 if m == 3 else 30


WEEKDAYS = ["Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday"]
WD3 = ["Wed", "Thu", "Fri", "Sat", "Sun", "Mon", "Tue"]
ROLE = [
    ("Fourth Day", "The Lights Are Set", "Orient and plan"),
    ("Fifth Day", "Water and Sky", "Body and breath"),
    ("Sixth Day", "Made for Each Other", "Connect and do the work"),
    ("Seventh Day", "Sabbath", "Rest"),
    ("First Day", "Let There Be Light", "Worship and gratitude"),
    ("Second Day", "The Great Separation", "Boundaries and truth"),
    ("Third Day", "Ground and Vine", "Plant and prune"),
]
GROUND = [
    "Name five things you can see. Eyes open is fine.",
    "Press your feet into the floor and take three slow breaths, out longer than in.",
    "Hold something warm or cool and notice its weight and texture.",
    "Rest a hand on your chest, or on a pet if you have one, and feel something steady.",
    "Look toward the nearest light or window and let your shoulders drop.",
    "Press your palms together for ten seconds, then let go.",
    "Name three sounds you can hear, near or far.",
]
PRESENCE = [
    "Lord, I am here. Meet me here.",
    "God, You are nearer than my next breath.",
    "Jesus, be with me in this room.",
    "Father, I am Yours, resting or not.",
    "Spirit of God, make this hour Yours.",
    "Lord, stand beside me while I tell the truth.",
    "God, steady my hands for what is ahead.",
]
MONTH_INFO = {
    1: ("Month 1", "The Lights Are Set", "Orient, ground, and learn the rhythm.",
        "Where am I standing, and what is one small rhythm I can keep?"),
    2: ("Month 2", "The Ground Is Broken", "Tell the truth, build the circle, and name the walls.",
        "What is hard and packed in me, and who can help me break it up?"),
    3: ("Month 3", "The Vine Is Tended", "Rest, walk in the light, tend the vineyard, and choose.",
        "What am I tending, and what am I choosing for the next season?"),
}
SPECIAL = {  # day number -> short calendar tag
    26: "Clocks fall back (US)", 51: "Thanksgiving (US)", 54: "Advent begins",
    76: "Winter solstice", 79: "Christmas Eve", 80: "Christmas Day",
    86: "New Year’s Eve", 87: "New Year’s Day", 91: "Final day. Next season Wed Jan 6",
    1: "Day 1. Today.",
}

# ---------------------------------------------------------------- data
def parse(path):
    out = {}
    cur = None
    for raw in open(path, encoding="utf-8").read().splitlines():
        m = re.match(r"^=== (\d+)\s*$", raw)
        if m:
            cur = int(m.group(1))
            out[cur] = {}
            continue
        if cur is None or not raw.strip():
            continue
        k, _, v = raw.partition(":")
        out[cur][k.strip()] = v.strip()
    return out


WEEKS = parse(os.path.join(HERE, "data", "weeks.txt"))
DAYS = {}
for f in ("days_m1.txt", "days_m2.txt", "days_m3.txt"):
    DAYS.update(parse(os.path.join(HERE, "data", f)))
assert sorted(DAYS) == list(range(1, TOTAL_DAYS + 1)), "days missing"
assert sorted(WEEKS) == list(range(1, 14)), "weeks missing"


def E(s):
    return html.escape(s or "", quote=False)


def first_sentence(s):
    m = re.match(r"(.+?[.!?])(\s|$)", s)
    return m.group(1) if m else s


def week_of(n):
    return (n - 1) // 7 + 1


# ---------------------------------------------------------------- html bits
CSS = """
@page { size: 8.5in 11in; margin: 0; }
:root{
  --turq:#1f9d9a; --turq2:#3fb6b0; --denim:#3b5778; --denim2:#263f5c; --gold:#d9a02f;
  --peach:#f6b894; --pink:#d6598f; --purple:#7a4c9e; --cream:#fdfaf5; --ink:#2b2430;
  --line:#c9bfd6; --soft:#f3eef7;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#e9e2ee;color:var(--ink);
  font-family:'DejaVu Sans','Verdana',sans-serif;font-size:10pt;line-height:1.38}
.serif{font-family:'DejaVu Serif','Georgia',serif}
.page{width:8.5in;height:11in;background:var(--cream);position:relative;overflow:hidden;
  page-break-after:always;break-after:page;display:flex;flex-direction:column;
  padding:.36in .52in .3in}
.page::before{content:'';position:absolute;inset:.16in;border:1.3px dashed #e3b958;
  pointer-events:none}
.band{height:6px;border-radius:4px;margin-bottom:6px;flex:none;
  background:linear-gradient(90deg,var(--turq),var(--denim) 40%,var(--purple) 72%,var(--pink))}
.topbar{display:flex;justify-content:space-between;align-items:baseline;flex:none;
  font-size:7.6pt;letter-spacing:1.4px;font-weight:700;text-transform:uppercase;color:var(--purple)}
.topbar .r{color:var(--denim)}
.body{flex:1;min-height:0;display:flex;flex-direction:column;overflow:hidden}
.foot{flex:none;display:flex;justify-content:space-between;font-size:7.4pt;letter-spacing:1px;
  color:var(--denim);text-transform:uppercase;padding-top:3px;border-top:1px solid var(--line);margin-top:4px}
h1,h2,h3{font-family:'DejaVu Serif',Georgia,serif;margin:0;color:var(--denim2)}
.lab{font-size:7.4pt;font-weight:800;letter-spacing:1.6px;text-transform:uppercase;color:var(--turq);margin-bottom:2px}
.lab.p{color:var(--purple)} .lab.g{color:#b07d12} .lab.d{color:var(--denim)} .lab.k{color:var(--pink)}
.box{border:1.2px solid var(--line);border-radius:8px;padding:6px 9px;background:#fff}
.t10{font-size:10pt;line-height:1.42}
.small{font-size:9.2pt;line-height:1.36}
.ital{font-style:italic}
.ruled{overflow:hidden}
.wl{height:.27in;border-bottom:1px solid #cdbfdc}
.ck{display:inline-block;width:.15in;height:.15in;border:1.4px solid var(--denim);border-radius:3px;
  vertical-align:-2px;margin-right:5px;flex:none}
/* ---- day page */
.datehead{margin-top:5px;display:flex;justify-content:space-between;align-items:flex-end;gap:10px}
.datebig{font-family:'DejaVu Serif',Georgia,serif;font-weight:700;font-size:15pt;color:var(--denim2);line-height:1.1}
.chips{display:flex;flex-wrap:wrap;gap:4px;margin-top:4px}
.chip{font-size:7.4pt;font-weight:700;border-radius:20px;padding:2px 8px;color:#fff;letter-spacing:.3px;white-space:nowrap}
.c1{background:var(--turq)} .c2{background:var(--denim)} .c3{background:var(--purple)} .c4{background:var(--pink)}
.daynum{white-space:nowrap;font-family:'DejaVu Serif',Georgia,serif;text-align:right;line-height:1;color:var(--gold);font-weight:700;font-size:26pt}
.daynum small{display:block;font-family:'DejaVu Sans',sans-serif;font-size:7pt;letter-spacing:1.4px;color:var(--denim);font-weight:700}
.dtitle{font-size:18pt;line-height:1.15;margin:7px 0 5px;color:var(--purple)}
.sanct{font-size:9.4pt;background:linear-gradient(90deg,#e6f6f5,#f4ecf9);border:1.2px solid #bfe3e1;border-radius:8px;padding:5px 9px}
.scrip{margin-top:6px;padding:6px 10px 7px;border-left:4px solid var(--gold);background:#fffaf0;border-radius:0 8px 8px 0}
.scrip .ref{font-weight:800;color:#8a6208;font-size:9pt}
.scrip .q{font-family:'DejaVu Serif',Georgia,serif;font-style:italic;font-size:10pt;line-height:1.4;margin:3px 0 5px}
.scrip .teach{font-family:'DejaVu Serif',Georgia,serif;font-size:10.4pt;line-height:1.46}
.weave{display:flex;gap:6px;margin-top:6px}
.weave .box{flex:1;padding:6px 9px;font-size:9.2pt;line-height:1.36}
.weave .i{border-color:#bfe3e1;background:#f0fbfa}
.weave .qm{border-color:#d8c7ea;background:#f8f3fc}
.weave .cn{border-color:#f0c9d9;background:#fff3f7}
.lower{display:flex;gap:9px;margin-top:6px;flex:1;min-height:0}
.lower .l{flex:1.05;display:flex;flex-direction:column;min-height:0}
.lower .r{flex:1;display:flex;flex-direction:column;gap:6px}
.pg{flex:1;display:flex;flex-direction:column;min-height:0}
.prompt{font-size:9.8pt;font-weight:700;color:var(--denim2);margin-top:3px;line-height:1.3}
.steps{margin:4px 0 0;padding:0;list-style:none;font-size:9.4pt;line-height:1.32}
.steps li{display:flex;align-items:flex-start;margin-bottom:3px}
.act{font-size:9.8pt;font-weight:700;line-height:1.34}
.pray{font-family:'DejaVu Serif',Georgia,serif;font-size:9.6pt;line-height:1.42;font-style:italic}
.decl{margin-top:5px;text-align:center;font-family:'DejaVu Serif',Georgia,serif;font-weight:700;
  color:var(--denim2);font-size:9.6pt;border-top:2px solid var(--gold);border-bottom:2px solid var(--gold);padding:3px 6px}
/* ---- week pages */
.wtitle{font-size:23pt;color:var(--purple);margin:4px 0 2px;line-height:1.1}
.wk{display:grid;grid-template-columns:1.08in 1fr;gap:0 8px;border-top:1px solid var(--line);padding:5px 0}
.wk .dl{font-size:8.2pt;line-height:1.3}
.wk .dl b{display:block;font-size:10pt;color:var(--denim2)}
.wk .dl i{display:block;color:var(--purple);font-style:normal;font-weight:700;font-size:7.6pt}
.wk .ds .tt{font-family:'DejaVu Serif',Georgia,serif;font-weight:700;color:var(--purple);font-size:10pt;margin-bottom:1px}
.wk .ds .st{display:flex;align-items:flex-start;font-size:8.8pt;line-height:1.3;margin-bottom:1px}
/* ---- calendar */
.cal{display:grid;grid-template-columns:repeat(7,1fr);grid-template-rows:auto repeat(5,1fr);gap:3px;flex:1;min-height:0}
.ch{background:var(--denim2);color:#fff;text-align:center;font-weight:800;font-size:8pt;letter-spacing:1px;
  padding:3px 0;border-radius:4px}
.ch.sab{background:var(--purple)}
.cell{border:1.2px solid var(--line);border-radius:6px;background:#fff;padding:3px 4px;overflow:hidden;
  display:flex;flex-direction:column;min-height:0}
.cell.sab{background:#f6f0fb}
.cell.empty{background:transparent;border-style:dotted;border-color:#e2dbea}
.cell .n{display:flex;justify-content:space-between;align-items:baseline;font-size:7.4pt;font-weight:800;color:var(--denim)}
.cell .n b{font-family:'DejaVu Serif',Georgia,serif;font-size:10.5pt;color:var(--purple)}
.cell .t{font-size:8pt;line-height:1.25;margin-top:2px;font-weight:600}
.cell .tag{margin-top:auto;font-size:6.6pt;line-height:1.2;font-weight:800;color:#b07d12;letter-spacing:.2px}
.cell .wkt{font-size:6.6pt;font-weight:800;color:var(--pink)}
/* ---- cover */
.cover{padding:0;background:#17606a}
.cover::before{display:none}
.cv{position:absolute;inset:0;
  background:
   radial-gradient(circle at 50% 37%, rgba(255,214,150,.95) 0, rgba(246,184,148,.75) 12%, rgba(214,89,143,.28) 36%, rgba(0,0,0,0) 62%),
   linear-gradient(180deg,#2fb5b0 0%,#1f9d9a 34%,#2d6b86 62%,#263f5c 100%)}
.stitch{position:absolute;inset:.28in;border:2px dashed #f0c46a;border-radius:10px}
.stitch2{position:absolute;inset:.38in;border:1px solid rgba(255,255,255,.35);border-radius:8px}
.cvc{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;color:#fff;text-align:center}
.cvc .brand{margin-top:.78in;font-size:12pt;letter-spacing:5px;font-weight:800;color:#fff3d6}
.cvc .kicker{margin-top:.1in;font-size:8.5pt;letter-spacing:3px;color:#d9f4f2;font-weight:700}
.cvc h1{color:#fff;font-size:44pt;line-height:1.02;margin-top:.24in;text-shadow:0 3px 10px rgba(20,30,50,.5);letter-spacing:1px}
.cvc .sub{font-family:'DejaVu Serif',Georgia,serif;font-style:italic;font-size:13pt;margin-top:.14in;color:#fff3d6;max-width:5.6in;line-height:1.35}
.cvc .sun{margin-top:.12in}
.cvc .tag{position:absolute;bottom:1.52in;font-family:'DejaVu Serif',Georgia,serif;font-size:15pt;font-weight:700;color:#fff;letter-spacing:.5px}
.cvc .by{position:absolute;bottom:.98in;font-size:8.8pt;letter-spacing:1.2px;color:#e6f7f6;line-height:1.6;max-width:5.8in}
.cvc .dt{position:absolute;bottom:.62in;font-size:8pt;letter-spacing:2px;color:#f0c46a;font-weight:800}
/* ---- misc pages */
.h-big{font-size:25pt;color:var(--purple);margin:4px 0 6px;line-height:1.1}
.p{margin:0 0 7px}
.toc{display:grid;grid-template-columns:1fr 1fr;gap:0 .3in;font-size:9.3pt}
.toc .row{display:flex;gap:6px;align-items:baseline;padding:2px 0;border-bottom:1px dotted var(--line)}
.toc .row .d{flex:1;border-bottom:0}
.toc .row b{color:var(--denim2)}
.toc .grp{grid-column:1/3;margin-top:6px;font-weight:800;color:var(--purple);letter-spacing:1px;font-size:8.4pt;text-transform:uppercase}
table.rt{width:100%;border-collapse:collapse;font-size:8.8pt}
table.rt td,table.rt th{border:1px solid var(--line);padding:3px 6px;vertical-align:top;text-align:left}
table.rt th{background:var(--denim2);color:#fff;font-size:8pt;letter-spacing:.8px}
ul.tight{margin:2px 0 6px;padding-left:16px} ul.tight li{margin-bottom:2px}
.cert{border:5px double var(--gold);margin:.1in 0 .1in;flex:1;border-radius:6px;padding:.3in .4in;display:flex;flex-direction:column;
  align-items:center;text-align:center;background:linear-gradient(180deg,#fffaf0,#fdf0f6)}
.cert h1{font-size:26pt;color:var(--purple)}
.sig{display:flex;gap:.4in;width:100%;margin-top:auto}
.sig div{flex:1;border-top:1.5px solid var(--denim);padding-top:3px;font-size:8pt;letter-spacing:1px;text-transform:uppercase;color:var(--denim)}
.nameline{width:80%;border-bottom:1.5px solid var(--denim);height:.34in;margin-top:.1in}
"""

SUN_SVG = """<svg width="250" height="190" viewBox="0 0 250 190" xmlns="http://www.w3.org/2000/svg">
<g transform="translate(125 95)">
 <g stroke="#f0c46a" stroke-width="3" stroke-linecap="round" opacity=".95">
  %s
 </g>
 <circle r="38" fill="#f6b894" opacity=".95"/><circle r="30" fill="#fff3d6"/>
 <rect x="-3.2" y="-24" width="6.4" height="48" rx="2" fill="#263f5c"/>
 <rect x="-15" y="-10" width="30" height="6.4" rx="2" fill="#263f5c"/>
</g></svg>"""


def sun_rays():
    import math
    parts = []
    for i in range(0, 360, 15):
        a = math.radians(i)
        r1, r2 = 46, 62 if i % 30 == 0 else 54
        parts.append(f'<line x1="{r1*math.cos(a):.1f}" y1="{r1*math.sin(a):.1f}" '
                     f'x2="{r2*math.cos(a):.1f}" y2="{r2*math.sin(a):.1f}"/>')
    return "\n".join(parts)


def page(inner, cls="", top_r="", running=True):
    """One printed page. Page numbers are injected afterwards via the {{PN}} token."""
    inner = re.sub(r'<div class="ruled"([^>]*)></div>', lambda m: f'<div class="ruled"{m.group(1)}>' + '<div class="wl"></div>' * 16 + '</div>', inner)
    top = ""
    if running:
        top = (f'<div class="band"></div><div class="topbar"><span>{BRAND}</span>'
               f'<span class="r">{E(top_r)}</span></div>')
    foot = (f'<div class="foot"><span>{BRAND} · {BOOK} · Original Lights</span>'
            f'<span>Page {{{{PN}}}}</span></div>') if running else ""
    return f'<section class="page {cls}">{top}<div class="body">{inner}</div>{foot}</section>'


def lines(n):
    return "".join('<div class="wl"></div>' for _ in range(n))


def label_split(q):
    m = re.match(r"^(Analogy|Physics note):\s*(.*)$", q)
    return (m.group(1), m.group(2)) if m else ("Analogy", q)


# ---------------------------------------------------------------- page builders
def cover():
    inner = f"""
<div class="cv"></div>
<div class="stitch"></div><div class="stitch2"></div>
<div class="cvc">
  <div class="brand">{BRAND}</div>
  <div class="kicker">A SURVIVOR-BUILT SANCTUARY WORKBOOK</div>
  <h1>THE SOLAR<br>WORKBOOK</h1>
  <div class="sub">Original Lights: 91 days of the 364-day calendar, the Ethiopian canon,
    quantum physics, and the Word, one day per page.</div>
  <div class="sun" style="transform:scale(1.55);margin-top:.5in">{SUN_SVG % sun_rays()}</div>
  <div style="position:absolute;bottom:2.35in;font-size:8.2pt;letter-spacing:2.2px;color:#e6f7f6;font-weight:700">ONE DAY PER PAGE · 3 MONTHLY CALENDARS · 13 WEEKLY MAPS</div>
  <div class="tag">You survived. Now we rebuild.</div>
  <div class="by">Written from the floor up by Hellshaker<br>and her loyal service dog, Big Boy</div>
  <div class="dt">SEASON ONE · BEGINS WEDNESDAY, OCTOBER 7, 2026</div>
</div>"""
    return page(inner, "cover", running=False).replace('<div class="body">', '<div class="body" style="padding:0">', 1)


def copyright_page():
    inner = f"""
<h1 class="h-big">About This Book</h1>
<div class="small">
<p class="p"><b>{BRAND}</b> · {BOOK}: Original Lights · Season One (91 days)<br>
Created October 7, 2026 · Version 1.0 · © 2026 {BRAND}. All rights reserved. Personal use only.
Please do not copy, resell, or redistribute without written permission.</p>
<p class="p"><b>Scripture.</b> Scripture quotations are from the ESV Bible (The Holy Bible, English Standard Version),
copyright © 2001 by Crossway, a publishing ministry of Good News Publishers. All rights reserved.
Quotations are identified as ESV on the page. Please read each passage in its full context in your own Bible.
Where a verse is not quoted, the reference is given and the idea is paraphrased.</p>
<p class="p"><b>Not treatment.</b> This workbook is a devotional and journaling tool. It is not medical care, therapy,
addiction treatment, legal advice, or crisis support, and the author is not a licensed clinician. Prayer sits beside
treatment, medical care, safe housing, and safety planning. It does not replace them. If a page raises something
heavy, skip it. You never have to relive anything to finish a page.</p>
<p class="p"><b>Not an emergency service.</b> If you are in immediate danger, call 911 (US). The numbers below are for the
United States and may change, so confirm them. Outside the US, look up your local equivalents.</p>
</div>
<div class="box" style="margin:2px 0 8px">
<div class="lab p">Help when you need it (US)</div>
<table class="rt" style="margin-top:3px">
<tr><td><b>Suicide &amp; Crisis Lifeline</b></td><td>Call or text <b>988</b>, any time</td></tr>
<tr><td><b>SAMHSA National Helpline</b> (substance use and mental health)</td><td><b>1-800-662-4357</b> · FindTreatment.gov</td></tr>
<tr><td><b>National Human Trafficking Hotline</b></td><td><b>1-888-373-7888</b> · text <b>233733</b></td></tr>
<tr><td><b>National Domestic Violence Hotline</b></td><td><b>1-800-799-7233</b> · text START to <b>88788</b></td></tr>
<tr><td><b>211</b> (local housing, food, and services)</td><td>Dial <b>211</b></td></tr>
</table></div>
<div class="small">
<p class="p"><b>About the Ethiopian canon texts.</b> 1 Enoch (Henok), Jubilees (Kufale), Sirach, Wisdom of Solomon, and Baruch
are quoted or referenced here as ancient writings. The Ethiopian Orthodox Tewahedo Church receives them as canon.
Most Protestant, Catholic, and Eastern Orthodox churches do not treat all of them as Scripture, though Jude 14–15
quotes 1 Enoch 1:9. Read them as witnesses to how God’s people understood time and creation, and let Scripture
carry the weight. Chapter references follow common translations, so verse numbers may differ slightly in yours.</p>
<p class="p"><b>About the physics.</b> Every quantum-physics idea in this book is offered as an analogy or a picture, and each
one is labeled that way. These ideas do not prove Scripture and do not show that thoughts control reality.
Scripture is not a physics textbook, and physics is not a theology. Where an idea is popular but wrong, the page says so.</p>
<p class="p"><b>About the creative symbols.</b> Broken chains, vineyards, and sunrise are symbols of freedom and renewal.
A page or a prayer does not literally break a curse or guarantee an outcome. Real change also takes support, time,
and often professional help.</p>
</div>"""
    return page(inner, top_r="Before you begin")


def whats_ahead():
    rows = ""
    for n in range(1, 14):
        w = WEEKS[n]
        a, b = day_date((n - 1) * 7 + 1), day_date(n * 7)
        rows += (f'<tr><td><b>{n}</b></td><td><b>{E(w["title"])}</b><br><span class="small">{E(w["goal"])}</span></td>'
                 f'<td>{a.strftime("%b %-d")} – {b.strftime("%b %-d")}</td></tr>')
    inner = f"""
<h1 class="h-big">What’s Ahead</h1>
<div class="small"><p class="p">Ninety-one days is thirteen weeks, one full quarter of the 364-day calendar.
Each week has a theme, a Scripture, a thread from the Ethiopian canon, and one quantum-physics picture. Each day gives you a
page to read, write on, and act from. Here is the road.</p></div>
<table class="rt"><tr><th style="width:.4in">Wk</th><th>Theme and goal</th><th style="width:1.2in">Dates</th></tr>{rows}</table>
<div class="small" style="margin-top:6px"><b>Three months:</b> Month 1, <i>The Lights Are Set</i> (Oct 7 – Nov 5).
Month 2, <i>The Ground Is Broken</i> (Nov 6 – Dec 5). Month 3, <i>The Vine Is Tended</i> (Dec 6 – Jan 5).</div>"""
    return page(inner, top_r="What’s ahead")


def intro_page():
    inner = f"""
<h1 class="h-big">Start Here</h1>
<div class="t10 serif">
<p class="p">I did not build this on a clean stage. I built it on the floor. I know what it is to be alone and scared of
people, to go looking for another plug, and to reach for help and find strings attached. I also know what it is to be
handed a watered-down verse and told to pray it away. I needed somewhere that could hold the truth about trauma without
pushing God out of the room. This is my attempt to build that for you.</p>
<p class="p">I am not finished. I am not a counselor or a doctor, and surviving something did not make me qualified to treat you.
I am building as I go, with my American Bully, Big Boy, beside me. What I can do is reach back with what I have learned, what
Scripture actually teaches, and something practical you can use today.</p>
<p class="p">This workbook starts today, October 7, 2026, and runs ninety-one days. Each day is one page. Each page has the same five
parts, so when you are tired you will always know where to go next:</p></div>
<table class="rt"><tr><th style="width:1.3in">Part</th><th>What it is</th></tr>
<tr><td><b>1. Sanctuary</b></td><td>A short, optional grounding exercise and a one-line prayer. Skip it, keep your eyes open, or use any anchor that works for you.</td></tr>
<tr><td><b>2. Scripture &amp; Teaching</b></td><td>A passage, what it meant in context, and how it speaks to someone rebuilding. Then three boxes: God’s original intent, a quantum-physics picture, and an Ethiopian canon thread.</td></tr>
<tr><td><b>3. Sacred Reflection</b></td><td>Three prompts with room to write. Grief, anger, doubt, honesty, and hope are all welcome here.</td></tr>
<tr><td><b>4. Soft Action</b></td><td>One realistic step, broken into three small steps with checkboxes. You are allowed to do less.</td></tr>
<tr><td><b>5. Supplication</b></td><td>A prayer for the days you cannot find your own words, and one short declaration.</td></tr></table>
<div class="t10 serif" style="margin-top:8px">
<p class="p">Grace is not enabling, and understanding is not excusing. A relapse does not make you disposable. Forgiveness does not
automatically restore trust or access. You can tell God the truth before you know how to clean it up.</p>
<p class="p"><b>You survived. Now we rebuild.</b> We do not have to rebuild your whole life before sundown. We do need to choose what
happens next. Turn the page.</p>
<p class="p ital" style="color:var(--purple)">Hellshaker &amp; Big Boy</p></div>"""
    return page(inner, top_r="Start here")


def howto_calendar():
    rows = ""
    for i, (a, b, c) in enumerate(ROLE):
        rows += f"<tr><td><b>{WEEKDAYS[i]}</b></td><td>{a}: {b}</td><td>{c}</td></tr>"
    inner = f"""
<h1 class="h-big">How the Calendar Works</h1>
<div class="small">
<p class="p"><b>The 364-day pattern.</b> 1 Enoch 72–82 and Jubilees 6 describe a solar year of exactly 364 days: 52 weeks and four seasons
of 91 days (13 weeks). As scholars read these texts, each season begins on the fourth day of the week, a Wednesday. Each season is three months of
30, 30, and 31 days. This workbook is one season of that pattern.</p>
<p class="p"><b>Why today is Day 1.</b> Wednesday is the fourth day of the creation week, when God set the sun, moon, and stars
(Gen. 1:14–19), and today, October 7, 2026, is a Wednesday. So Day 1 is today and Day 91 is Tuesday, January 5, 2027. I chose
that anchor. I am <b>not</b> claiming October 7 is the official new year of the Enoch calendar. Scholars reconstruct how the
364-day year lined up with the Gregorian one in different ways, and the ancient sources do not settle it. The 364-day year is also about
a day and a quarter shorter than the sun’s true year (about 365.24 days), and the old texts do not clearly say how that
was corrected. Staying inside one 91-day season avoids guessing.</p>
<p class="p"><b>Every page shows three dates.</b> The Gregorian date, the workbook’s 364-day position (Month, Day, Week), and the Ethiopian date.
The Ethiopian calendar is a different solar calendar with 12 months of 30 days plus a short thirteenth month, and it is about seven to eight years behind
the Gregorian one. Today, October 7, 2026, is Meskerem 27, 2019 E.C.</p>
<p class="p"><b>Weeks run Wednesday to Tuesday.</b> Each weekday keeps one job all season, matched to the creation week:</p></div>
<table class="rt"><tr><th>Weekday</th><th>Creation day</th><th>Job for the day</th></tr>{rows}</table>
<div class="small" style="margin-top:7px"><p class="p"><b>About Sabbath.</b> Saturday is the seventh day, and it is your Sabbath. If your church gathers on Sunday, keep both:
rest on one and worship on the other. Rest was never meant to be a performance. It is the first thing slavery takes, and the first thing God gives back
(Deut. 5:15). Take what you can get, even twenty minutes.</p>
<p class="p"><b>Where to start each week.</b> Read the Week Map first, then the Day-by-Day Steps, then each day’s page. Fill in the monthly calendar as you go.</p></div>
<div class="box" style="margin-top:4px;flex:1;min-height:0;display:flex;flex-direction:column"><div class="lab">My Day 1 check-in (October 7, 2026): how am I, honestly?</div><div class="ruled" style="flex:1"></div></div>"""
    return page(inner, top_r="How the calendar works")


def toc_page(toc):
    left = ""
    def row(label, pg):
        return f'<div class="row"><b>{E(label)}</b><span class="d"></span><span>{pg}</span></div>'
    parts = ['<div class="grp">Front matter</div>']
    for lab, key in [("About this book", "about"), ("What’s ahead", "ahead"), ("Start here", "intro"),
                     ("How the calendar works", "howto")]:
        parts.append(row(lab, toc[key]))
    groups = {1: range(1, 5), 2: range(5, 9), 3: range(9, 14)}
    for m in (1, 2, 3):
        parts.append(f'<div class="grp">{MONTH_INFO[m][0]}: {E(MONTH_INFO[m][1])}</div>')
        parts.append(row(f"Month {m} calendar", toc[f"m{m}"]))
        for n in groups[m]:
            a_, b_ = (n - 1) * 7 + 1, n * 7
            parts.append(row(f"Week {n}: {WEEKS[n]['title']}  (Days {a_}–{b_})", toc[f"w{n}"]))
    parts.append('<div class="grp">Finish the season</div>')
    for lab, key in [("Final reflection", "final"), ("Progress review", "review"), ("Next-step challenge", "next"),
                     ("Closing prayer", "closing"), ("Certificate of completion", "cert"), ("Help when you need it", "help")]:
        parts.append(row(lab, toc[key]))
    inner = f'<h1 class="h-big">Table of Contents</h1><div class="toc">{"".join(parts)}</div>' \
            f'<div class="small" style="margin-top:8px">Each week has a <b>Week Map</b> page, a <b>Day-by-Day Steps</b> page, and then seven daily pages in order. ' \
            f'Page numbers listed are for the Week Map. Month 2 begins Friday, November 6 (Week 5), and Month 3 begins Sunday, December 6 (Week 9).</div>'
    return page(inner, top_r="Contents")


def month_page(m):
    name, theme, line, ask = MONTH_INFO[m]
    first = (m - 1) * 30 + 1
    last = first + month_len(m) - 1
    d1, d2 = day_date(first), day_date(last)
    wd0 = (first - 1) % 7           # 0=Wed column
    cells = ['<div class="ch">WED</div><div class="ch">THU</div><div class="ch">FRI</div>'
             '<div class="ch sab">SAT · SABBATH</div><div class="ch">SUN</div><div class="ch">MON</div><div class="ch">TUE</div>']
    cells += ['<div class="cell empty"></div>'] * wd0
    for n in range(first, last + 1):
        d = day_date(n)
        wd = (n - 1) % 7
        tags = []
        if n in SPECIAL:
            tags.append(SPECIAL[n])
        y, em, ed = ethiopian(d)
        if ed == 1:
            tags.append(f"{ETH_MONTHS[em-1]} 1 (Eth.)")
        wk = f'<span class="wkt">Wk {week_of(n)}</span>' if wd == 0 else ""
        cells.append(
            f'<div class="cell{" sab" if wd == 3 else ""}"><div class="n"><span><b>{d.day}</b> {d.strftime("%b")}</span>'
            f'<span>D{n}</span></div>{wk}<div class="t">{E(DAYS[n]["cal"])}</div>'
            f'<div class="tag">{E("; ".join(tags))}</div></div>')
    used = wd0 + month_len(m)
    cells += ['<div class="cell empty"></div>'] * ((7 - used % 7) % 7)
    inner = f"""
<div class="lab d">{name} · Days {first}–{last} of 91 · {month_len(m)} days</div>
<h1 style="font-size:23pt;color:var(--purple);line-height:1.1;margin-bottom:2px">{E(theme)}</h1>
<div class="small"><b>{d1.strftime("%A, %B %-d, %Y")}</b> to <b>{d2.strftime("%A, %B %-d, %Y")}</b>
· Ethiopian: {eth_str(d1, True)} to {eth_str(d2, True)}<br>{E(line)}</div>
<div class="cal" style="margin-top:5px">{"".join(cells)}</div>
<div style="display:flex;gap:8px;margin-top:5px">
 <div class="box" style="flex:1.2"><div class="lab p">Monthly question</div><div class="small">{E(ask)}</div>{lines(2)}</div>
 <div class="box" style="flex:1"><div class="lab">My intention for this month</div>{lines(2)}</div>
</div>"""
    return page(inner, top_r=f"{name} calendar")


def week_map(n):
    w = WEEKS[n]
    a, b = (n - 1) * 7 + 1, n * 7
    da, db = day_date(a), day_date(b)
    chips = ""
    for k in range(a, b + 1):
        d = day_date(k)
        chips += (f'<div class="box" style="flex:1;padding:4px 5px;text-align:center"><div class="lab p" style="margin:0">{WD3[(k-1)%7]} {d.strftime("%b %-d")}</div>'
                  f'<div style="font-size:8pt;line-height:1.25;font-weight:700;color:var(--denim2)">{E(DAYS[k]["title"])}</div></div>')
    q = w["q"]
    inner = f"""
<div class="lab d">Week {n} of 13 · Days {a}–{b} · {da.strftime("%B %-d")} – {db.strftime("%B %-d, %Y")} · Ethiopian {eth_str(da, True)} – {eth_str(db, True)}</div>
<h1 class="wtitle">{E(w["title"])}</h1>
<div class="scrip"><div class="ref">{E(w["ref"])}</div><div class="q">{E(q)}</div></div>
<div class="box" style="margin-top:6px;border-color:#bfe3e1;background:#f0fbfa"><div class="lab">God’s original intent</div><div class="t10 serif">{E(w["intent"])}</div></div>
<div class="box" style="margin-top:6px;border-color:#f0c9d9;background:#fff3f7"><div class="lab k">Ethiopian canon thread</div><div class="small">{E(w["canon"])}</div></div>
<div class="box" style="margin-top:6px;border-color:#d8c7ea;background:#f8f3fc"><div class="lab p">Quantum picture (an analogy, not a proof)</div>
 <div class="small">{E(w["science"])}</div>
 <div class="small" style="margin-top:3px"><b>Where this picture stops:</b> {E(w["limit"])}</div></div>
<div class="box" style="margin-top:6px"><div class="lab g">This week’s goal</div><div class="t10"><b>{E(w["goal"])}</b></div></div>
<div class="lab d" style="margin-top:7px">The week at a glance</div>
<div style="display:flex;gap:3px">{chips}</div>
<div class="box" style="margin-top:7px"><div class="lab p">My support this week</div><div class="small">Who I will check in with, and what I need from them:</div><div class="ruled" style="height:.54in"></div></div>
<div class="box" style="margin-top:7px;flex:1;min-height:0;display:flex;flex-direction:column"><div class="lab">My intention for the week, in my own words</div><div class="ruled" style="flex:1"></div></div>"""
    return page(inner, top_r=f"Week {n} map")


def week_steps(n):
    w = WEEKS[n]
    a, b = (n - 1) * 7 + 1, n * 7
    rows = ""
    for k in range(a, b + 1):
        d = DAYS[k]
        dd = day_date(k)
        wd = (k - 1) % 7
        steps = "".join(f'<div class="st"><span class="ck"></span><span>{E(d["s"+str(i)])}</span></div>' for i in (1, 2, 3))
        rows += (f'<div class="wk"><div class="dl"><b>{WD3[wd]} {dd.strftime("%b %-d")}</b>Day {k}<i>{ROLE[wd][0]}: {ROLE[wd][2]}</i></div>'
                 f'<div class="ds"><div class="tt">{E(d["title"])}</div>{steps}</div></div>')
    inner = f"""
<div class="lab d">Week {n} · Day-by-Day Steps</div>
<h1 style="font-size:17pt;color:var(--purple);margin:1px 0 3px;line-height:1.15">{E(w["title"])}: broken down</h1>
{rows}
<div class="box" style="margin-top:5px;flex:1;min-height:0;display:flex;flex-direction:column"><div class="lab p">End-of-week review</div>
<div class="small"><span class="ck"></span>I rested on Saturday, even a little. &nbsp; <span class="ck"></span>I reached one safe person. &nbsp; <span class="ck"></span>I took one real step.</div>
<div style="display:flex;gap:10px;flex:1.3;min-height:0;margin-top:3px"><div style="flex:1;display:flex;flex-direction:column"><div class="small"><b>What held this week?</b></div><div class="ruled" style="flex:1"></div></div>
<div style="flex:1;display:flex;flex-direction:column"><div class="small"><b>What cost me?</b></div><div class="ruled" style="flex:1"></div></div></div>
<div class="small" style="margin-top:3px"><b>One thing I will carry into next week:</b></div><div class="ruled" style="flex:.6;min-height:.27in"></div></div>"""
    return page(inner, top_r=f"Week {n} · day-by-day")


def day_page(n):
    d = DAYS[n]
    w = WEEKS[week_of(n)]
    dd = day_date(n)
    wd = (n - 1) % 7
    m = month_of(n)
    role = ROLE[wd]
    chips = (f'<span class="chip c1">Solar Walk · Month {m}, Day {day_in_month(n)} of {month_len(m)}</span>'
             f'<span class="chip c2">Week {week_of(n)} · Day {wd+1} of 7</span>'
             f'<span class="chip c3">{role[0]}: {role[1]}</span>'
             f'<span class="chip c4">Ethiopian: {eth_str(dd)}</span>')
    # weave boxes
    boxes = f'<div class="box i"><div class="lab">God’s original intent</div>{E(d["intent"])}</div>'
    if d.get("quantum"):
        lab, txt = label_split(d["quantum"])
        boxes += f'<div class="box qm"><div class="lab p">Quantum picture · {lab}</div>{E(txt)}</div>'
    else:
        boxes += (f'<div class="box qm"><div class="lab p">This week’s quantum picture · Analogy</div>'
                  f'{E(first_sentence(w["science"]))}</div>')
    if d.get("canon"):
        boxes += f'<div class="box cn"><div class="lab k">Ethiopian canon thread</div>{E(d["canon"])}</div>'
    else:
        boxes += (f'<div class="box cn"><div class="lab k">This week’s canon thread</div>'
                  f'{E(first_sentence(w["canon"]))}</div>')
    steps = "".join(f'<li><span class="ck"></span><span>{E(d["s"+str(i)])}</span></li>' for i in (1, 2, 3))
    prompts = "".join(f'<div class="pg"><div class="prompt">{i}. {E(d["r"+str(i)])}</div><div class="ruled" style="flex:1;min-height:.5in"></div></div>' for i in (1, 2, 3))
    inner = f"""
<div class="datehead"><div><div class="datebig">{dd.strftime("%A, %B %-d, %Y")}</div><div class="chips">{chips}</div></div>
 <div class="daynum"><small>DAY</small>{n}<small>OF 91</small></div></div>
<h2 class="dtitle">{E(d["title"])}</h2>
<div class="sanct small"><span class="lab" style="margin:0">1 · Sanctuary</span> <i style="color:var(--denim)">optional. Skip it or swap in any anchor that works for you.</i><br>
 <b>Ground:</b> {E(GROUND[wd])} &nbsp; <b>Pray:</b> <i>{E(PRESENCE[wd])}</i></div>
<div class="scrip"><div class="lab g" style="margin:0">2 · Scripture &amp; Teaching</div><div class="ref">{E(d["ref"])}</div>
 <div class="q">{E(d["q"])}</div><div class="teach">{E(d["teach"])}</div></div>
<div class="weave">{boxes}</div>
<div class="lower">
 <div class="l box"><div class="lab p">3 · Sacred Reflection</div>{prompts}</div>
 <div class="r">
  <div class="box"><div class="lab">4 · Soft Action</div><div class="act">{E(d["action"])}</div><ul class="steps">{steps}</ul></div>
  <div class="box" style="flex:1;display:flex;flex-direction:column;min-height:0"><div class="lab k">5 · Supplication</div><div class="pray">{E(d["prayer"])}</div><div class="lab" style="margin-top:5px">In my own words to God</div><div class="ruled" style="flex:1;min-height:.3in"></div></div>
 </div>
</div>
<div class="decl">{E(d["decl"])}</div>"""
    return page(inner, top_r=f"Day {n} of 91 · Week {week_of(n)} · Month {m}")


def final_reflection():
    prompts = ["What did these ninety-one days teach me about God, and about me?",
               "Where did I tell the truth for the first time? What was it like?",
               "What am I still grieving or angry about? What do I need next for that?",
               "Which day or page do I want to return to, and why?"]
    inner = '<h1 class="h-big">Final Reflection</h1><div class="small"><p class="p">There are no wrong answers. Write what is true. If a prompt is too heavy today, skip it.</p></div>'
    for p in prompts:
        inner += f'<div class="prompt" style="font-size:10pt;margin-top:6px">{E(p)}</div><div class="ruled" style="height:1.18in"></div>'
    return page(inner, top_r="Final reflection")


def progress_review():
    rows = ""
    for n in range(1, 14):
        rows += (f'<tr><td><b>{n}</b></td><td>{E(WEEKS[n]["title"])}</td><td style="width:.55in;text-align:center"><span class="ck"></span></td>'
                 f'<td style="width:2.5in"></td></tr>')
    scales = ["Rest and sleep", "Safe connection", "Honesty with God and myself", "Safety and stability",
              "Practical steps (appointments, documents, work)", "Faith that feels real"]
    sr = "".join(f'<tr><td>{s}</td><td style="text-align:center">1 &nbsp;2 &nbsp;3 &nbsp;4 &nbsp;5</td><td style="text-align:center">1 &nbsp;2 &nbsp;3 &nbsp;4 &nbsp;5</td></tr>' for s in scales)
    inner = f"""<h1 class="h-big">Progress Review</h1>
<div class="small"><p class="p">This is not a grade. It is information. Mark the weeks you showed up to, even partly, and write one thing each taught you.</p></div>
<table class="rt"><tr><th style="width:.4in">Wk</th><th>Theme</th><th>Done</th><th>One thing I learned</th></tr>{rows}</table>
<div class="lab p" style="margin-top:8px">How I am doing (circle 1 = hard, 5 = steady)</div>
<table class="rt"><tr><th>Area</th><th style="width:1.7in">Day 1 (Oct 7)</th><th style="width:1.7in">Day 91 (Jan 5)</th></tr>{sr}</table>
<div class="small" style="margin-top:4px">A lower number is not failure. It may simply be honest.</div>
<div class="box" style="margin-top:8px;flex:1;min-height:0;display:flex;flex-direction:column"><div class="lab p">What I would tell the person who starts on Day 1</div><div class="ruled" style="flex:1"></div></div>"""
    return page(inner, top_r="Progress review")


def next_step():
    inner = f"""<h1 class="h-big">Next-Step Challenge</h1>
<div class="small"><p class="p">One season ends and another can begin. In the 364-day pattern, the next 91-day season starts on a Wednesday, which is
<b>January 6, 2027</b>. You can repeat this book, start another, or simply keep the rhythm. Choose what is realistic. Do not choose what looks impressive.</p></div>
<div class="box"><div class="lab">My next seven days</div><div class="small">Pick one anchor from each part of your life, small enough to do on a bad day.</div>
<table class="rt" style="margin-top:4px">
<tr style="height:.4in"><td style="width:1.4in"><b>Rest</b></td><td></td></tr><tr style="height:.4in"><td><b>Connection</b></td><td></td></tr>
<tr style="height:.4in"><td><b>Care (medical, clinical, recovery)</b></td><td></td></tr><tr style="height:.4in"><td><b>Practical</b></td><td></td></tr>
<tr style="height:.4in"><td><b>Faith</b></td><td></td></tr></table></div>
<div class="box" style="margin-top:7px"><div class="lab p">My safety and support plan</div><div class="small">Three people or numbers I can call, one place I can go, and one thing I will do if a craving or a crisis hits.</div><div class="ruled" style="height:1.1in"></div></div>
<div class="box" style="margin-top:7px;flex:1;min-height:0;display:flex;flex-direction:column"><div class="lab k">Letter to the person I was on October 7</div><div class="ruled" style="flex:1"></div></div>
<div class="small" style="margin-top:6px"><b>Challenge:</b> Tell one safe person today what you finished. Then pick the day you will begin your next step and write it here:
______________________.</div>"""
    return page(inner, top_r="Next-step challenge")


def closing_prayer():
    inner = f"""<h1 class="h-big">Closing Prayer</h1>
<div class="serif t10" style="font-style:italic;line-height:1.6;margin-top:6px">
<p class="p">Lord, I came into this season tired, and You met me here. Thank You for the lights You hung before I ever needed them,
and for the light that has not been overcome by any dark I have walked through.</p>
<p class="p">Thank You for the days I showed up, and the days I could only open the book. Thank You for what I told the truth about,
and for the people You sent. Where I fell, thank You for helping me rise. Where I am still in the middle of it, stay close.</p>
<p class="p">Keep my body, my mind, and my heart. Give me rest that is real and safe people to walk with. Give me wisdom to ask for the
help I need, from doctors, counselors, and friends, and the humility to take it.</p>
<p class="p">Teach me to tend my vineyard. Water what is dry. Fence what is vulnerable. Prune what must be cut, with care and not with punishment.
Let me abide in You, and let fruit come in its time. I will not measure it before then.</p>
<p class="p">For everyone who is still on the floor tonight, and for those I love who did not make it out, I ask Your mercy. Show me one way to reach back.
Make my small step useful to someone else.</p>
<p class="p">The Lord bless me and keep me. The Lord make His face to shine upon me and be gracious to me. The Lord lift up His countenance upon me
and give me peace. In the name of Jesus, amen.</p></div>
<div class="small" style="margin-top:4px">The last paragraph is the blessing from Numbers 6:24–26 (ESV), prayed in the first person.</div>
<div class="decl" style="margin-top:10px">You survived. Now we rebuild.</div>"""
    return page(inner, top_r="Closing prayer")


def certificate():
    ln = "border-top:1.5px solid var(--denim);padding-top:3px;font-size:8pt;letter-spacing:1px;text-transform:uppercase;color:var(--denim)"
    inner = f"""<div class="cert" style="justify-content:space-evenly">
<div style="transform:scale(.62);margin:-.35in 0 -.45in">{SUN_SVG % sun_rays()}</div>
<div class="lab d" style="font-size:9pt;letter-spacing:4px">{BRAND}</div>
<h1>Certificate of Completion</h1>
<div class="small" style="font-size:10.5pt">This certifies that</div>
<div style="width:82%"><div style="height:.38in"></div><div style="{ln};text-align:center">Participant’s name</div></div>
<div class="small" style="font-size:10.5pt">has walked through 91 days of</div>
<h2 style="font-size:18pt;color:var(--denim2)">{BOOK}: Original Lights</h2>
<div style="width:82%"><div style="height:.38in"></div><div style="{ln};text-align:center">Devotional title completed (write it here)</div></div>
<div class="small" style="font-size:10pt;max-width:5.4in">showing up with honesty, tending what God has given, and choosing the next step. Brokenness is not the destination.</div>
<div class="serif" style="font-size:13pt;font-weight:700;color:var(--purple)">You survived. Now we rebuild.</div>
<div style="width:100%;display:flex;gap:.4in"><div style="flex:1"><div style="height:.34in"></div><div style="{ln}">Date completed</div></div>
<div style="flex:1"><div style="height:.34in"></div><div style="{ln}">Participant’s signature</div></div></div>
<div style="width:100%;display:flex;gap:.4in"><div style="flex:1"><div style="height:.34in"></div><div style="{ln}">Witness or support person (optional)</div></div>
<div style="flex:1"><div style="height:.34in"></div><div style="{ln}">Date</div></div></div>
</div>"""
    return page(inner, top_r="Certificate")


def help_page():
    inner = f"""<h1 class="h-big">Help When You Need It</h1>
<div class="small"><p class="p">Prayer belongs beside practical care. If you are in danger, go to safety first. Numbers are for the United States and can change. Confirm them, and look up local options outside the US.</p></div>
<table class="rt"><tr><th>When</th><th>Who</th></tr>
<tr><td>Immediate danger</td><td><b>911</b></td></tr>
<tr><td>Thoughts of suicide, or a mental-health crisis</td><td>Call or text <b>988</b> (Suicide &amp; Crisis Lifeline), any time</td></tr>
<tr><td>Substance use, or looking for treatment</td><td>SAMHSA National Helpline <b>1-800-662-4357</b> (free, confidential, 24/7) · FindTreatment.gov</td></tr>
<tr><td>Trafficking, coercion, or forced work</td><td>National Human Trafficking Hotline <b>1-888-373-7888</b> · text <b>233733</b></td></tr>
<tr><td>Abuse or an unsafe relationship</td><td>National Domestic Violence Hotline <b>1-800-799-7233</b> · text START to <b>88788</b></td></tr>
<tr><td>Housing, food, ID, and local services</td><td>Dial <b>211</b></td></tr></table>
<div class="box" style="margin-top:8px"><div class="lab p">My own list</div><div class="small">Write the numbers and names you trust here.</div><div class="ruled" style="height:2.4in"></div></div>
<div class="small" style="margin-top:8px"><p class="p"><b>A note on leaving unsafe situations.</b> Leaving abuse is not easy, and it is not always safe to do quickly.
An advocate at one of the hotlines above can help you plan. Nothing in this workbook asks you to stay, to reconcile, or to forgive on a timeline.</p></div>"""
    return page(inner, top_r="Help")


# ---------------------------------------------------------------- assemble
def assemble():
    pages = []     # (key, html)
    pages.append(("cover", cover()))
    pages.append(("about", copyright_page()))
    pages.append(("toc", None))
    pages.append(("ahead", whats_ahead()))
    pages.append(("intro", intro_page()))
    pages.append(("howto", howto_calendar()))
    for n in range(1, 14):
        start = (n - 1) * 7 + 1
        if n in (1, 5, 9):
            m = {1: 1, 5: 2, 9: 3}[n]
            pages.append((f"m{m}", month_page(m)))
        pages.append((f"w{n}", week_map(n)))
        pages.append((f"w{n}s", week_steps(n)))
        for k in range(start, start + 7):
            pages.append((f"d{k}", day_page(k)))
    pages.append(("final", final_reflection()))
    pages.append(("review", progress_review()))
    pages.append(("next", next_step()))
    pages.append(("closing", closing_prayer()))
    pages.append(("cert", certificate()))
    pages.append(("help", help_page()))
    toc = {k: i + 1 for i, (k, _) in enumerate(pages)}
    pages[2] = ("toc", toc_page(toc))
    out = []
    for i, (k, h) in enumerate(pages):
        out.append(h.replace("{{PN}}", str(i + 1)))
    return pages, "\n".join(out)


def main():
    pages, body = assemble()
    doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{BRAND} · {BOOK}: Original Lights</title>'
           f'<meta name="description" content="A 91-day, one-page-per-day devotional workbook on the 364-day solar calendar, '
           f'mixing Scripture, the Ethiopian canon, and quantum-physics pictures.">'
           f'<style>{CSS}</style></head><body>{body}</body></html>')
    out_html = os.path.join(HERE, "solar-workbook.html")
    open(out_html, "w", encoding="utf-8").write(doc)
    print(f"wrote {out_html} ({len(pages)} pages)")

    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"))
        pg = b.new_page()
        pg.goto("file://" + out_html)
        pg.wait_for_timeout(500)
        over = pg.evaluate("""() => {
          const res = [];
          document.querySelectorAll('.page').forEach((pgEl, i) => {
            const body = pgEl.querySelector('.body');
            if (!body) return;
            // overflow if content taller than the box, or any descendant extends below the body box
            const bb = body.getBoundingClientRect();
            let worst = 0;
            body.querySelectorAll('*').forEach(el => {
              if (el.closest('.ruled') && !el.classList.contains('ruled')) return;
              const r = el.getBoundingClientRect();
              worst = Math.max(worst, r.bottom - bb.bottom);
            });
            if (body.scrollHeight > body.clientHeight + 1 || worst > 1)
              res.push([i + 1, Math.round(body.scrollHeight - body.clientHeight), Math.round(worst)]);
          });
          return res;
        }""")
        if over:
            print("OVERFLOW (page, scroll-excess px, descendant-excess px):", over)
        else:
            print("no overflow detected")
        if "--shots" in sys.argv:
            os.makedirs(os.path.join(HERE, "_shots"), exist_ok=True)
            for idx in [int(x) for x in sys.argv[sys.argv.index("--shots") + 1].split(",")]:
                el = pg.query_selector_all(".page")[idx - 1]
                el.screenshot(path=os.path.join(HERE, "_shots", f"p{idx:03d}.png"))
        pg.pdf(path=os.path.join(HERE, "solar-workbook.pdf"), width="8.5in", height="11in",
               print_background=True, prefer_css_page_size=True)
        b.close()
    print("wrote solar-workbook.pdf")


if __name__ == "__main__":
    main()
