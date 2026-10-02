#!/usr/bin/env python3
"""The 90-Day Rebuild (new edition): every day is six pages of NEW writing.
Guide (goal, Bible in context, what research suggests, step by step) → Standing (2) → Coming Home → Write It → Pocket page.
No uploaded text is reproduced. Usage: python build_new.py [--ink]   (--ink = plain white pages, less ink)
"""
import os, re, sys, html as _html
import lib
import art_pages as A
import build_all as B
from lib import BRAND, esc
from mdbook import mk
from companion import COMPANION_DAYS
from rb_sources import SRC
from rb_love import N as LOVE, LV
import rb_days_1, rb_days_2, rb_days_3, rb_days_4, rb_days_5, rb_days_6

INK = "--ink" in sys.argv
RB = {d[0]: d for d in rb_days_1.R1 + rb_days_2.R2 + rb_days_3.R3 + rb_days_4.R4 + rb_days_5.R5 + rb_days_6.R6}
assert sorted(RB) == list(range(1, 91))
ST = {d[0]: d for d in COMPANION_DAYS}
OUT = lib.OUT
ARCS = B.ARCS
ARC_OF = {d: a for a in ARCS for d in range(a[2], a[3] + 1)}
ARC_COLORS = B.ARC_COLORS

def arc_of(n):
    a = ARC_OF[n]
    return a[0], a[1], ARC_COLORS[a[0] - 1]

def foot(label):
    return f'<div class="nfoot"><span>{BRAND}</span><span>{label}</span></div>'

def guide(n):
    _, goal, ctx, keys, research, steps, future, nugget, choose = RB[n]
    an, at, ac = arc_of(n)
    title = ST[n][1]
    vref = ST[n][3]
    cite = "; ".join(SRC[k][0] for k in keys)
    res = ""
    if research:
        res = f'<div class="nbox sci"><div class="ntag">What research suggests</div><p>{esc(research)}</p>' + (f'<p class="cite">Source{"s" if len(keys) > 1 else ""}: {esc(cite)}. Full citations are in the back of the book.</p>' if keys else '<p class="cite">Source: 988 Lifeline (988lifeline.org).</p>') + '</div>'
    stp = "".join(f'<li><span class="bx"></span><span>{esc(s)}</span></li>' for s in steps)
    return f'''<section class="npg guide" style="--ac:{ac}">
<div class="ntop"><span class="npill">Arc {an} · {esc(at)}</span><span class="nday">Day {n:02d}<small> / 90</small></span></div>
<h1 class="ntitle">{esc(title)}</h1>
<div class="ngoal"><div class="ntag">Today’s goal</div><p>{esc(goal)}</p></div>
<div class="nbox bib"><div class="ntag">The Bible in context · {esc(vref)} (ESV)</div><p>{esc(ctx)}</p></div>
{res}
<div class="nbox steps"><div class="ntag">Do this, step by step <span class="mins">about 15 minutes · check each box</span></div><ol>{stp}</ol><div class="ntag" style="margin-top:.12in">My notes while I do these steps</div><div class="lines">{"<div></div>"*6}</div></div>
<div class="nsafe">Too much today? Stop at any step. Press your feet into the floor, name five things you can see, and reach for someone safe. Numbers are at the back.</div>
{foot(f"Day {n} · Guide")}</section>'''

def write_page(n):
    an, at, ac = arc_of(n)
    goal = RB[n][1]
    dots = "".join(f'<i class="{"on" if d <= n else ""}"></i>' for d in range(1, 91))
    return f'''<section class="npg writep" style="--ac:{ac}">
<div class="ntop"><span class="npill">Write it down · Day {n:02d}</span><span class="ndate">Date: ____ / ____ / ________</span></div>
<h1 class="ntitle small">{esc(ST[n][1])}</h1>
<div class="rate"><div><span class="ntag">Before I started</span><div class="scale">{''.join(f"<b>{i}</b>" for i in range(0, 11))}</div><small>0 = calm · 10 = most distressed</small></div>
<div><span class="ntag">When I finished</span><div class="scale">{''.join(f"<b>{i}</b>" for i in range(0, 11))}</div><small>Circle one number each time. This is how you can see what works for you.</small></div></div>
<h3>What came up for me today</h3><div class="lines">{"<div></div>"*5}</div>
<h3>What I did (circle the steps I finished)</h3><div class="stepc">{''.join(f"<span>{i}</span>" for i in range(1, 6))} <em>and one thing I did not do, and why:</em></div><div class="lines">{"<div></div>"*3}</div>
<h3>What I noticed in my body</h3><div class="lines">{"<div></div>"*3}</div>
<h3>What I am taking with me</h3><div class="lines">{"<div></div>"*4}</div>
<div class="dots">{dots}</div>
{foot(f"Day {n} · Write it")}</section>'''

def pocket(n):
    an, at, ac = arc_of(n)
    _, goal, ctx, keys, research, steps, future, nugget, choose = RB[n]
    vref, vq = ST[n][3], ST[n][4]
    note, lref = LOVE[n - 1]
    return f'''<section class="npg pocket" style="--ac:{ac}">
<div class="ntop"><span class="npill">Pocket page · Day {n:02d}</span><span class="nday cut">Cut it out, tape it up, or carry it</span></div>
<div class="pv"><div class="ntag">A verse to carry</div><blockquote>“{esc(vq)}”<span class="ref">{esc(vref)} · ESV</span></blockquote></div>
<div class="pgrid">
<div class="pl"><div class="ntag">A note of love</div><p>{esc(note)}</p><blockquote class="lv">“{esc(LV[lref])}”<span class="ref">{esc(lref)} · ESV</span></blockquote><p class="small">The note is mine. The verse is what Scripture actually says.</p></div>
<div class="pn"><div class="ntag">A nugget</div><p>{esc(nugget)}</p></div>
</div>
<div class="pc"><div class="ntag">Today I choose</div><p>{esc(choose)}</p></div>
<div class="pf"><div class="ntag">A note from Future Me</div><p>{esc(future)}</p><div class="fl"><span>Write Future Me one line of your own:</span><div class="lines">{"<div></div>"*3}</div></div></div>
{foot(f"Day {n} · Pocket page")}</section>'''

NCSS = '''
:root{--navy:#1f3b63;--gold:#a06f1c;--wine:#7a2c4a}
.npg{page:day;height:10.12in;break-after:page;position:relative;display:flex;flex-direction:column;color:#2a2230;font:400 10.4pt/1.5 'Libre Franklin'}
.ntop{display:flex;justify-content:space-between;align-items:center;margin-bottom:.07in}
.npill{font:700 8.4pt 'Libre Franklin';letter-spacing:.07em;text-transform:uppercase;color:#fff;background:var(--ac);padding:3px 12px;border-radius:20px}
.nday{font:400 17pt 'Rye';color:var(--navy)} .nday small{font:600 9pt 'Libre Franklin';color:#6b5f78} .nday.cut{font:600 8.5pt 'Libre Franklin';color:#6b5f78}
.ntitle{font:400 21pt/1.12 'Rye';color:var(--navy);margin:.02in 0 .1in} .ntitle.small{font-size:16pt}
.ntag{font:700 8.2pt 'Libre Franklin';letter-spacing:.09em;text-transform:uppercase;color:var(--gold);margin-bottom:.03in} .mins{font-weight:600;letter-spacing:0;text-transform:none;color:#6b5f78;margin-left:.08in}
.ngoal{border-left:6px solid var(--ac);padding:.07in .16in;margin-bottom:.1in;background:rgba(255,250,238,.7)} .ngoal p{margin:0;font:700 12.2pt/1.4 'Caveat';font-size:15pt;color:var(--wine)}
.nbox{border:1.5px solid #c9b88f;border-radius:10px;padding:.09in .16in .08in;margin-bottom:.1in;background:rgba(255,251,240,.78);break-inside:avoid} .nbox p{margin:.02in 0;font-size:9.9pt}
.nbox.sci{border-color:#9db4c9;background:rgba(240,246,252,.75)} .cite{font-size:8pt!important;color:#5c6b7c;font-style:italic}
.nbox.steps{flex:1;background:rgba(255,251,240,.9);border-width:2px} .nbox.steps ol{list-style:none;margin:.04in 0 0;padding:0;counter-reset:s}
.nbox.steps li{display:flex;gap:.11in;align-items:flex-start;margin:.075in 0;font-size:10.2pt;counter-increment:s} .bx{flex:none;width:.19in;height:.19in;border:1.8px solid var(--navy);border-radius:4px;margin-top:2px;background:#fff}
.nbox.steps li:before{content:counter(s);flex:none;font:400 13pt 'Rye';color:var(--gold);width:.2in;margin-top:-1px}
.nsafe{margin-bottom:.2in;font-size:8.4pt;color:#5a4d66;font-style:italic;border-top:1px dashed #c9b88f;padding-top:.06in;margin-top:.03in}
.nfoot{position:absolute;bottom:-.03in;left:0;right:0;display:flex;justify-content:space-between;font:600 7.6pt 'Libre Franklin';letter-spacing:.06em;color:#7a6c88;text-transform:uppercase}
.writep h3{font:400 11pt 'Rye';color:var(--navy);margin:.12in 0 .02in}
.lines div{height:.3in;border-bottom:1.2px solid #bfae83}
.rate{display:grid;grid-template-columns:1fr 1fr;gap:.18in;margin:.04in 0} .scale{display:flex;gap:3px;margin:.03in 0} .scale b{flex:1;text-align:center;border:1.3px solid #9d8f6a;border-radius:50%;font:700 8pt 'Libre Franklin';aspect-ratio:1;display:flex;align-items:center;justify-content:center;background:#fff} .rate small{font-size:7.4pt;color:#6b5f78}
.stepc{display:flex;gap:.1in;align-items:center;font-size:9pt} .stepc span{width:.27in;height:.27in;border:1.5px solid var(--navy);border-radius:50%;display:flex;align-items:center;justify-content:center;font:700 9pt 'Libre Franklin';background:#fff} .stepc em{color:#6b5f78}
.ndate{font:600 8.4pt 'Libre Franklin';color:#6b5f78}
.dots{display:flex;flex-wrap:wrap;gap:2px;margin-top:.12in} .dots i{width:5px;height:5px;border-radius:50%;background:#ddd2b6;display:block} .dots i.on{background:var(--ac)}
.pocket .pv{border:2px solid var(--gold);border-radius:12px;padding:.12in .2in;background:rgba(255,250,235,.85);margin-bottom:.12in}
.pocket blockquote{margin:.04in 0;font:400 13pt/1.45 'Libre Franklin';font-style:italic;color:#27304a;border:0;padding:0;background:none} .pocket blockquote .ref{display:block;font:700 8.5pt 'Libre Franklin';font-style:normal;color:var(--wine);margin-top:.05in}
.pgrid{display:grid;grid-template-columns:1.35fr 1fr;gap:.14in;margin-bottom:.12in}
.pl,.pn,.pc,.pf{border:1.5px solid #c9b88f;border-radius:10px;padding:.1in .16in;background:rgba(255,251,240,.8)} .pl p,.pn p,.pc p,.pf p{margin:.03in 0;font-size:10.3pt}
.pl blockquote.lv{font-size:10.4pt;margin-top:.08in} .pn{background:rgba(238,246,244,.8);border-color:#8fb7ae} .pn p{font:700 14pt/1.35 'Caveat';color:#1f5c55}
.pc{border-left:7px solid var(--wine);margin-bottom:.12in} .pc p{font:700 17pt/1.25 'Caveat';color:var(--wine)}
.pf{flex:1;border-color:var(--gold)} .pf>p{font:700 14pt/1.35 'Caveat';color:#3b2f52} .fl span{font-size:8.6pt;color:#6b5f78} .small{font-size:8.2pt!important;color:#7a6c88}
.revw{background:none}
html,body{background:transparent!important}
.lens,.ahead .item,.work,.sp .sanct,.sp .soft,.sp .supp,.hd .box1,.hd .two .c,blockquote.prayer,blockquote.decl,blockquote.epigraph,.jar .card{background:rgba(255,251,240,.82)!important}
.src p{font-size:8.6pt;line-height:1.38;margin:.05in 0;text-indent:-.2in;padding-left:.2in}
'''
BG = '''
.bgR,.bgL{position:relative}
.bgR::before,.bgL::before{content:"";position:absolute;z-index:-1;top:-.38in;width:8.5in;height:11in}
.bgR::before{left:-.95in;background:url(books-src/art/bg_right.jpg) 0 0/100% 100% no-repeat}
.bgL::before{left:-.4in;background:url(books-src/art/bg_left.jpg) 0 0/100% 100% no-repeat}
'''

def bg(h, side):
    return h.replace('<section class="', f'<section class="bg{side} ', 1)

def how_works():
    return f"""<section class="fm"><div class="band"></div><div class="kick">Read this first</div><h1>How This Book Works</h1>
<p>Every day has <strong>six pages</strong>, always in this order, so you never have to decide what to do next:</p>
<div class="ahead">
<div class="item"><div class="n">1</div><div><div class="t">Guide · Understand and plan</div><p>Today’s goal, what the Bible passage actually says in its setting, what research suggests, and five numbered steps with check boxes.</p></div></div>
<div class="item"><div class="n">2</div><div><div class="t">Standing, left page</div><p>An optional grounding exercise, Scripture, and teaching on spiritual warfare, family wounds, and addiction.</p></div></div>
<div class="item"><div class="n">3</div><div><div class="t">Standing, right page</div><p>Reflection prompts, one soft action, a prayer, and a declaration.</p></div></div>
<div class="item"><div class="n">4</div><div><div class="t">Coming Home · Go to her</div><p>One gentle step toward the child you were, with a prayer, an affirmation, and a challenge.</p></div></div>
<div class="item"><div class="n">5</div><div><div class="t">Write it down</div><p>Rate your distress before and after, circle the steps you finished, and write what came up. Over time the numbers show you what actually helps.</p></div></div>
<div class="item"><div class="n">6</div><div><div class="t">Pocket page</div><p>A verse to carry, a note of love with an ESV verse, a nugget, “Today I choose,” and a note from Future Me.</p></div></div>
</div>
<div class="safety"><h3>Be honest about the science</h3><ul>
<li>The research notes are plain-language summaries of published studies. They describe what has been found across groups of people. They are not promises about you.</li>
<li>Citations were written from memory and have not been checked against the originals. Look up any you plan to rely on, and ask a counselor or doctor about anything that affects your care.</li>
<li>The Bible “in context” notes explain a passage’s setting. Where I apply a verse beyond its own subject, I say so.</li></ul></div>
<div class="safety"><h3>Pace yourself</h3><ul>
<li>Do all six pages in one sitting, or spread them across the day. Doing only the Guide on a hard day still counts.</li>
<li>Skip any step or any grounding exercise that does not feel safe. Nothing here asks you to tell a story or remember anything.</li>
<li>This book does not replace counseling, treatment, medical care, or a safety plan. Prayer sits beside those things, not instead of them.</li></ul></div></section>"""

def prayer():
    ps = ["Father, I come to You through Jesus. I am not coming cleaned up. I am coming honest.",
          "You know what was done to me, what I did to get through it, and what I am still afraid is true about me. Nothing in these ninety days will surprise You.",
          "Walk through each page with me. Where I find shame, bring light. Where I find grief, sit with me and do not rush me. Where I find anger, let me bring it to You instead of holding it against You.",
          "Give me the courage to take the next small step, and the sense to ask for help when I need it. Let what I learn become something somebody else can use.",
          "I put my sister Brandi Renee in Your hands, not mine. In Jesus’ name. Amen."]
    return f'<section class="fm"><div class="band"></div><div class="kick">Say it before day one</div><h1>An Opening Prayer{mk(9)}</h1><p class="small">Say it again any day you need it.</p><blockquote class="prayer">' + "".join(f"<p>{esc(p)}</p>" for p in ps) + "</blockquote></section>"

def sources_pages():
    used = []
    for n in range(1, 91):
        for k in RB[n][3]:
            if k not in used:
                used.append(k)
    items = "".join(f"<p>{esc(SRC[k][1])}</p>" for k in sorted(used, key=lambda k: SRC[k][1]))
    half = len(used) // 2
    return f'''<section class="fm src"><div class="band"></div><div class="kick">For the curious and the careful</div><h1>Sources{mk(80)}</h1>
<p class="small">These are the studies and books behind the “What research suggests” boxes. Each box summarizes a finding in plain words and does not claim more than that. <strong>These citations were written from memory and have not been verified against the originals, so please look them up before relying on them.</strong> A librarian, a counselor, or a search engine can help.</p>{items}</section>'''

def arc_divider(n, title, a, b):
    row = lib.PATH_ROWS[n - 1]
    sub = f"Standing: {row[2]}. Coming Home: {lib.HOME_STAGES[n - 1]}."
    return A.divider(A.PLATES[(n - 1) % 3], f"Arc {n} · Days {a}–{b}", title, sub, f"{b - a + 1} days · {6 * (b - a + 1)} pages", mk(100 + n))

def build():
    front = [(1, "How This Book Works", 3), (1, "Your 90-Day Path", 4), (1, "Going Back Safely", 6), (1, "Spiritual Warfare, Plainly", 7),
             (1, "A Word About Your Mother", 8), (1, "An Opening Prayer", 9)]
    arcs = [(1, f"Arc {n} · {t} (Days {a}–{b})", 100 + n) for n, t, a, b in ARCS]
    tail = [(1, "Sources", 80), (1, "The Challenge Jar", 61), (1, "A Letter From Her", 62), (1, "A Letter From the New Me", 63), (1, "Our Promise", 64),
            (1, "Final Reflection", 50), (1, "Where I Am Now", 51), (1, "Next-Step Challenge and Closing Prayer", 52),
            (1, "Certificate of Completion", 53), (1, "Help, Right Now", 54)]
    entries = front + arcs + tail
    keys = [str(k) for (_, _, k) in entries]
    rows = "".join(f"<tr><td><strong>{d}</strong></td><td>{esc(a)}</td><td>{esc(s)}</td><td>{esc(h)}</td></tr>" for (d, a, s, w, v), h in zip(lib.PATH_ROWS, lib.HOME_STAGES))
    pathp = f'<section class="fm"><div class="band"></div><div class="kick">The whole map</div><h1>Your 90-Day Path{mk(4)}</h1><p>Nine arcs, ten to fifteen days each. Each arc has one theme and one place on the road from surviving toward living.</p><table><thead><tr><th>Days</th><th>Arc</th><th>Standing focus</th><th>Coming Home stage</th></tr></thead><tbody>{rows}</tbody></table></section>'

    def body(pmap, pad=False):
        P = []
        P.append(lib.cover("The 90-Day<br>Rebuild", "Bible · Research · Step by Step", "You survived. Now we rebuild.", "Six pages a day for ninety days:<br>Scripture in context, what research suggests, and what to do next"))
        P.append(lib.title_page("The 90-Day<br>Rebuild", "Scripture in its setting · what research suggests · five steps a day<br>Understand it. Stand on it. Go to her. Write it down. Carry it.", "For Brandi Renee, January 27, 1986 – December 17, 2021, and for the little girl who was not protected."))
        P.append(lib.copyright_page("The 90-Day Rebuild: Bible, Research, and Step-by-Step Healing for Ninety Days"))
        P.append(B.toc_section(entries, pmap))
        P.append(how_works().replace("<h1>How This Book Works</h1>", f"<h1>How This Book Works{mk(3)}</h1>"))
        P.append(pathp)
        P.append(B.tag(B.strip(B.ser(B.h_by["Going Back Safely"])), "Going Back Safely", 6))
        P.append(B.tag(B.strip(B.ser(B.s_by["Spiritual Warfare, Plainly"])), "Spiritual Warfare, Plainly", 7))
        P.append(B.tag(B.strip(B.ser(B.s_by["A Word About Your Mother"])), "A Word About Your Mother", 8))
        P.append(prayer())
        if pad:
            P.append(B.notes_page())
        for n, t, a, b in ARCS:
            P.append(arc_divider(n, t, a, b))
            for d in range(a, b + 1):
                P.append(bg(guide(d), 'R'))
                P.append(bg(B.fix_standing(B.s_days[2 * (d - 1)]), 'L'))
                P.append(bg(B.fix_standing(B.s_days[2 * (d - 1) + 1]), 'R'))
                P.append(bg(B.fix_home(B.h_days[d - 1]), 'L'))
                P.append(bg(write_page(d), 'R'))
                P.append(bg(pocket(d), 'L'))
            P.append(B.arc_review(n, t))
        P.append(sources_pages())
        jar = "".join(B.strip(B.ser(e)) for e in B.h_jar)
        P.append(jar.replace("<h2>The Challenge Jar</h2>", f"<h2>The Challenge Jar{mk(61)}</h2>", 1) if "<h2>The Challenge Jar" in jar else jar)
        letters = "".join(B.strip(B.ser(e)) for e in B.h_letters)
        for t_, k_ in (("A Letter From Her", 62), ("A Letter From the New Me", 63), ("Our Promise", 64)):
            letters = letters.replace(f"<h1>{t_}</h1>", f"<h1>{t_}{mk(k_)}</h1>", 1)
        P.append(letters)
        for e, (t_, k_) in zip(B.j_closing, (("Final Reflection", 50), ("Where I Am Now", 51), ("Next-Step Challenge", 52))):
            P.append(B.tag(B.strip(B.ser(e)), t_, k_))
        P.append(A.certificate("The 90-Day Rebuild", mk(53)))
        P.append(B.tag(B.strip(B.ser(B.j_res)), "Help, Right Now", 54))
        return "\n".join(P)

    css = "\n".join([B.JOURNAL_STYLES, B.STAND_STYLES, B.HOME_STYLES, A.CSS, B.GUTTER_CSS, NCSS, "" if INK else BG])
    name = "the-90-day-rebuild-ink-saver" if INK else "the-90-day-rebuild"
    html_path = os.path.join(OUT, name + ".html")
    pdf_path = os.path.join(OUT, name + ".pdf")
    page = lambda b_: f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>The 90-Day Rebuild</title><style>{css}\n.mk{{font-size:2px;line-height:0;color:rgba(255,255,255,.01);letter-spacing:0}}</style></head><body>{b_}</body></html>"
    def render(pmap, pad):
        open(html_path, "w").write(page(body(pmap, pad)))
        lib.render_pdf(html_path, pdf_path)
        return lib.find_marker_pages(pdf_path, keys)
    pmap = {k: "000" for k in keys}
    found, n = render(pmap, False)
    pad = int(found["101"]) % 2 == 1
    if pad:
        found, n = render(pmap, True)
    pmap = {k: str(found.get(k, "")) for k in keys}
    f2, n2 = render(pmap, pad)
    odd = [k for k in ("101","102","103","104","105","106","107","108","109") if int(f2[k]) % 2 == 1]
    print("arc dividers on odd pages (should be none):", odd, "| padded:", pad)
    print(f"{name}: {n2} pages -> {pdf_path}")

if __name__ == "__main__":
    build()
