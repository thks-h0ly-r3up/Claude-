"""Ninety Days of Standing — spiritual warfare, childhood trauma, addiction, and motherhood.
A 90-day companion whose Day N pairs with Journal Day N."""
import os

import lib
from lib import BRAND, esc, inline
from mdbook import mk
from companion import COMPANION_DAYS

ARCS = [(1, "Telling the Truth", 1, 10), (2, "The Lies and the Names", 11, 20), (3, "The Realm and Your Authority", 21, 30),
        (4, "The Contracts", 31, 45), (5, "The Bloodline", 46, 55), (6, "The Playbook and the Structure", 56, 68),
        (7, "God", 69, 76), (8, "Brandi and Letting Go", 77, 84), (9, "Becoming Her", 85, 90)]
ARC_COLORS = ["#27857f", "#7a4c9e", "#d6598f", "#4a6486", "#27857f", "#7a4c9e", "#d6598f", "#4a6486", "#c58a2d"]

JOURNAL_TITLES = {1: "You Are Not Crazy", 2: "Tell One Person", 3: "The Two Hands", 4: "Shame or Repentance", 5: "Your Body Is Not Broken", 6: "Where It Lives", 7: "Six Resets", 8: "The Inventory", 9: "Get the Medical Picture", 10: "The Date", 11: "What It Taught You", 12: "Lie, Evidence, Truth", 13: "The False Name", 14: "Trading Names", 15: "It Was Not Your Fault", 16: "Why You Went Back", 17: "Why You Miss Them", 18: "The Memory Gaps", 19: "Moral Injury", 20: "Forgiving Yourself", 21: "Two Realms", 22: "Four Categories", 23: "What He Cannot Do", 24: "Seated, Not Cowering", 25: "The Order Matters", 26: "The Doors", 27: "Get Under Cover", 28: "Forgive, By Name", 29: "Forgiveness Is Not Access", 30: "The Armor, Daily", 31: "There Is Always a Legal Question", 32: "The Survival Vow", 33: "Breaking the Vow", 34: "The Self-Curse", 35: "The Shame Covenant", 36: "The Silence Contract", 37: "Soul Ties", 38: "Cutting the Tie", 39: "The Substance Covenant", 40: "The Trauma Bond", 41: "The Control Contract", 42: "The Performance Contract", 43: "The Self-Punishment Contract", 44: "The Death Agreement", 45: "Agreement With the Accuser", 46: "Not Your Guilt, Your Terrain", 47: "Map the Line", 48: "Four Layers", 49: "Where It Got Permission", 50: "Standing in the Gap", 51: "The Bloodline Prayer", 52: "My Own Agreements", 53: "Change the Behavior", 54: "Honor Without Repeating", 55: "The Line Stops Here", 56: "Twelve Stages", 57: "Isolation Is the Hinge", 58: "The One Who Can Correct You", 59: "Running Out the Clock", 60: "Map the Trigger Chain", 61: "HALT", 62: "The Craving Protocol", 63: "Play the Tape Forward", 64: "Replace the Function", 65: "Fill the House", 66: "Architecture, Not Willpower", 67: "Boundaries in the Real World", 68: "When You Fall", 69: "Where He Was", 70: "Why He Did Not Stop It", 71: "Not Punishment", 72: "Angry at God", 73: "Take Your Case Out of Court", 74: "The Silence", 75: "Sitting Silent With Him", 76: "All Things Work Together", 77: "You Were Her Sister", 78: "Who Was Responsible", 79: "Where She Is", 80: "Not a Debt", 81: "The Letter", 82: "Grief Is Not a Relapse", 83: "Letting the Living Go", 84: "The Release", 85: "Consecrated Before Formed", 86: "The Wound Is the Shape", 87: "Chosen Means Sent", 88: "The Two Futures", 89: "Steward, Not Survivor", 90: "The Commission"}

ANCHORS = [
 "Feel your feet on the floor. Keep your eyes open.",
 "Hold something warm or cold in your hands for a minute.",
 "Name three things you can see and one thing you can hear.",
 "Put a hand on your chest and let one long breath out.",
 "Look around until your eyes find the exit. You can leave if you need to.",
 "Press your palms together, then let go.",
 "Sit with your back against something solid.",
 "Take a slow sip of water.",
]
SANCT = [
 "Lord, You were here before I said anything.",
 "Jesus, I do not have to perform for You.",
 "Father, meet me exactly where I am.",
 "Holy Spirit, stay near, and do not let me go further than I can hold.",
 "God, I am here. You are here. That is enough to start.",
 "Jesus, You are bigger than what I am about to read.",
]

WARFARE = """<section class="fm"><div class="band"></div><div class="kick">Before day one</div><h1>Spiritual Warfare, Plainly</h1>
<p>I want to be careful with this language, because it has been used on people who needed help, not hype. So here is what I stand on.</p>
<h2>What Scripture says</h2>
<p>There is a real adversary: a liar, an accuser, a thief (John 10:10; Revelation 12:10; 1 Peter 5:8). He is a created being, limited by God (Job 1–2), and already defeated at the cross (Colossians 2:15; 1 John 3:8). Our part is to submit to God, resist the devil, stand firm in the armor God gives, answer lies with what is written (as Jesus did in Matthew 4), and pray (James 4:7; Ephesians 6:10–18).</p>
<h2>What Scripture does not say</h2>
<p>It does not hand us a formula. In Acts 19:13–16, men tried to use Jesus’ name like a tool and were beaten. It does not say every problem is demonic. It does not say we should shout or boast about authority; Jesus told His disciples to rejoice not that spirits submit to them but that their names are written in heaven (Luke 10:20), and even the archangel Michael did not presume to rebuke the devil on his own (Jude 9). It does not say a child’s struggle is a spirit, or that words on a page break a curse.</p>
<h2>How this book uses the word “warfare”</h2>
<p>Here, warfare means refusing to agree with lies, standing in Christ, and doing the ordinary faithful things together with practical care: sleep, food, doctors, counselors, safety, honest friends, and prayer. Test every spirit (1 John 4:1). If something makes you more ashamed, more isolated, or more afraid, it is not from Him.</p>
<p class="small"><em>Where I offer a picture (doors, agreements, stages) it is interpretation. Scripture is the authority; the pictures are tools.</em></p>
</section>"""

MOTHERS = """<section class="fm"><div class="band"></div><div class="kick">Before day one</div><h1>A Word to Mothers</h1>
<p>This book is for anyone who mothers or has been mothered: raising children, grieving them, separated from them, fostering, adopting, stepping in, pregnant, hoping to be, or healing from your own mother. It is also for women with no children who are still carrying what motherhood meant in their house.</p>
<h2>What I will not do</h2>
<p>I will not promise how your children will turn out. Proverbs 22:6 is a proverb about wisdom, not a guarantee, and every child makes choices. I will not tell you that your child is cursed, demonic, or being punished for your past. I will not tell you to stay somewhere unsafe, and I will not use guilt to pressure you.</p>
<h2>What I will do</h2>
<p>Put safety first. Name the grief and the guilt without making them your identity. Point toward real help: doctors, counselors, treatment programs that welcome mothers, legal aid, advocates. Be honest that fear of losing your children keeps many mothers from getting help, and that hiding usually makes it worse while support usually helps. Hold hope without guarantees.</p>
<h2>Right now</h2>
<p>If a child is in danger, call 911. Childhelp National Child Abuse Hotline: 1-800-422-4453. If you are thinking about hurting yourself or your child, call or text 988 now. Postpartum Support International: 1-800-944-4773. National Maternal Mental Health Hotline: 1-833-852-6262. <span class="small">(Please confirm numbers before relying on them.)</span></p>
</section>"""

USE = """<section class="fm"><div class="band"></div><div class="kick">How it works</div><h1>How to Use This Book</h1>
<ol style="line-height:1.55">
<li><strong>One spread a day.</strong> The left page is grounding, Scripture, and teaching. The right page is reflection, one soft action, and a prayer.</li>
<li><strong>Same day, same theme.</strong> Day N here pairs with Journal Day N and names the Workbook section and Volume II chapter to read with it.</li>
<li><strong>Grounding is optional.</strong> Skip it, change it, or keep your eyes open. Use another anchor if that one does not work for you.</li>
<li><strong>Write on the lines.</strong> You never have to write the story. Titles and single sentences are enough.</li>
<li><strong>One soft action.</strong> Small enough to do on a bad day. Doing less is allowed. Doing it is the point.</li>
<li><strong>Not every day will fit your life.</strong> If you are not a mother, read “my kids” as the people you are responsible for, or the child you were.</li>
<li><strong>Stop when it is too much.</strong> Reach for a safe person or a number in the back. The page will wait.</li>
</ol></section>"""

CSS = r"""
.sp{page:day;height:10.12in;break-after:page;position:relative;display:flex;flex-direction:column}
.sp .dband{height:8px;background:linear-gradient(90deg,var(--ac),#7a4c9e 60%,#d6598f);border-radius:4px;margin-bottom:.1in}
.sp .dtop{display:flex;justify-content:space-between;align-items:center}
.sp .arcpill{background:var(--ac);color:#fff;font:800 8pt 'Libre Franklin';letter-spacing:.14em;text-transform:uppercase;padding:3px 12px;border-radius:20px}
.sp .dnum{font:700 26pt/1 'Caveat';color:var(--ac)} .sp .dnum small{font:700 10pt 'Libre Franklin';color:#8f82a3}
.sp .dtitle{font:700 34pt/1.02 'Caveat';color:#7a4c9e;margin:.05in 0 .03in;border:0;padding:0}
.sp .lens{font:800 8pt 'Libre Franklin';letter-spacing:.16em;text-transform:uppercase;color:#d6598f;margin-bottom:.07in;border:0;background:none;padding:0;border-radius:0;position:static;display:block}
.sp .pairs{background:#f6f1fa;border:1px solid var(--line);border-radius:10px;padding:.06in .12in;font-size:8.3pt;line-height:1.4;margin-bottom:.1in}
.sp .pairs b{color:#7a4c9e}
.sp .sanct{border:1.5px dashed var(--line);border-radius:12px;padding:.1in .16in;margin-bottom:.12in;background:#fff;position:relative;font-size:9.2pt}
.sp .sanct .tag{position:absolute;top:-10px;left:14px;background:#4a6486;color:#fff;font:800 7.4pt 'Libre Franklin';letter-spacing:.12em;text-transform:uppercase;padding:2px 11px;border-radius:20px}
.sp .sanct i{color:#7a4c9e;font-style:italic}
.sp .verse{background:linear-gradient(90deg,rgba(63,182,176,.14),rgba(214,89,143,.09));border-radius:12px;padding:.11in .24in;margin:0 0 .12in;text-align:center;font:600 13.6pt/1.28 'Caveat';color:var(--ink)}
.sp .verse .ref{display:block;font:700 7.8pt 'Libre Franklin';letter-spacing:.14em;text-transform:uppercase;color:#4a6486;margin-top:3px}
.sp .teach{font-size:12pt;line-height:1.62;margin:0 0 .1in}
.sp .notes{flex:1;overflow:hidden;margin-bottom:.05in}
.sp .notes div{height:.3in;border-bottom:1.2px solid #d3c8e0}
.sp .kick2{font:800 8.4pt 'Libre Franklin';letter-spacing:.16em;text-transform:uppercase;color:var(--ac);margin:.04in 0 .04in}
.sp .ask{margin:0 0 .02in;flex:1;display:flex;flex-direction:column;min-height:0}
.sp .ask .q{font:700 10pt/1.35 'Libre Franklin';font-style:italic;color:#4a6486}
.sp .ask .rules{flex:1;overflow:hidden}
.sp .ask .rules div{height:.3in;border-bottom:1.2px solid #d3c8e0}
.sp .soft{border:1.6px solid var(--line);border-left:7px solid #4a6486;border-radius:12px;background:#fff;padding:.12in .18in .08in;margin:.08in 0 .1in;position:relative}
.sp .soft .tag2{position:absolute;top:-10px;left:14px;background:#4a6486;color:#fff;font:800 7.6pt 'Libre Franklin';letter-spacing:.12em;text-transform:uppercase;padding:2px 11px;border-radius:20px}
.sp .soft p{margin:0;font-size:10.2pt;line-height:1.5}
.sp .supp{border:1.6px solid var(--line);border-left:7px solid #d6598f;border-radius:12px;background:#fff;padding:.14in .2in .08in;position:relative}
.sp .supp .tag2{position:absolute;top:-10px;left:14px;background:#d6598f;color:#fff;font:800 7.6pt 'Libre Franklin';letter-spacing:.12em;text-transform:uppercase;padding:2px 11px;border-radius:20px}
.sp .supp p{margin:0 0 .05in;font-size:10pt;line-height:1.5}
.sp .decl{font:700 17pt/1.15 'Caveat';color:#7a4c9e;text-align:center;margin-top:.05in}
.sp .done{display:flex;align-items:center;justify-content:center;gap:8px;font:700 8.4pt 'Libre Franklin';color:#7a4c9e;margin-top:.04in}
.sp .dfoot{margin-top:.08in;text-align:center}
.sp .dots{display:flex;gap:2px;justify-content:center;margin-bottom:.04in}
.sp .dots i{display:block;width:5px;height:5px;border-radius:50%;background:#e3dcec}
.sp .dots i.on{background:var(--ac)}
.sp .bl{font:800 7pt 'Libre Franklin';letter-spacing:.2em;text-transform:uppercase;color:#7a4c9e}
.jopen{page:day;width:auto;height:10.12in;border-radius:18px;padding:.9in .8in}
.jopen:before{inset:.2in;border-radius:12px}
.jopen .bm{left:.8in;bottom:.7in}
.mk{font-size:2px;line-height:0;color:rgba(255,255,255,.01);letter-spacing:0}
"""

def _dots(n):
    return "".join(f'<i class="{"on" if d <= n else ""}"></i>' for d in range(1, 91))

def left(d, arc_n):
    n, title, lens, vref, vq, teach, asks, act, pray, decl, also = d
    c = ARC_COLORS[arc_n - 1]
    an = ARCS[arc_n - 1][1]
    a = ANCHORS[(n - 1) % len(ANCHORS)]
    s = SANCT[(n - 1) % len(SANCT)]
    verse = f'<div class="verse">“{esc(vq)}”<span class="ref">{esc(vref)} · ESV</span></div>' if vq else f'<div class="verse"><span class="ref">{esc(vref)}</span></div>'
    return f"""<section class="sp" style="--ac:{c}"><div class="dband"></div>
<div class="dtop"><span class="arcpill">Arc {arc_n} · {esc(an)}</span><span class="dnum">Day {n:02d}<small> / 90</small></span></div>
<h1 class="dtitle">{esc(title)}</h1><div class="lens">{esc(lens)}</div>
<div class="pairs"><b>Pairs with</b> Journal Day {n}: {esc(JOURNAL_TITLES[n])} &nbsp;·&nbsp; <b>Also read</b> {esc(also)}</div>
<div class="sanct"><span class="tag">Sanctuary · optional</span>{esc(a)} <i>{esc(s)}</i></div>
{verse}
<div class="kick2">What this means</div>
<p class="teach">{esc(teach)}</p>
<div class="kick2">What stood out to me</div><div class="notes">{"<div></div>" * 14}</div>
<div class="dfoot"><div class="bl">{BRAND} · Ninety Days of Standing</div></div></section>"""

def right(d, arc_n):
    n, title, lens, vref, vq, teach, asks, act, pray, decl, also = d
    c = ARC_COLORS[arc_n - 1]
    rules = "<div></div>" * 8
    q = "".join(f'<div class="ask"><div class="q">{i+1}. {esc(a)}</div><div class="rules">{rules}</div></div>' for i, a in enumerate(asks))
    return f"""<section class="sp" style="--ac:{c}"><div class="dband"></div>
<div class="dtop"><span class="arcpill">Day {n:02d} · {esc(title)}</span><span class="dnum">Date: ___/___/____</span></div>
<div class="kick2" style="margin-top:.1in">Sacred reflection</div>
{q}
<div class="soft"><span class="tag2">Soft action</span><p>{esc(act)}</p></div>
<div class="supp"><span class="tag2">Supplication</span><p>{esc(pray)}</p>
<div class="decl">{esc(decl)}</div><div class="done"><span class="box"></span> I said it. I wrote it. That is enough for today.</div></div>
<div class="dfoot"><div class="dots">{_dots(n)}</div><div class="bl">{BRAND} · Reaching back. Freeing the bound.</div></div></section>"""

def arc_divider(arc):
    n, t, a, b = arc
    focus = lib.PATH_ROWS[n - 1][2]
    c = ARC_COLORS[n - 1]
    return f"""<section class="opener jopen" style="background:linear-gradient(175deg,{c} 0%,#7a4c9e 62%,#d6598f 100%)">
<div class="kicker">Arc {n} · Days {a}–{b}</div><h1>{esc(t)}{mk(100 + n)}</h1><div class="orn"></div>
<div class="sub">{esc(focus)}.</div><div class="bm">{BRAND} · Ninety Days of Standing</div></section>"""

def build():
    entries = [(1, "What’s Ahead", 1), (1, "How to Read This Book", 2), (1, "Your 90-Day Path", 5), (1, "Spiritual Warfare, Plainly", 6),
               (1, "A Word to Mothers", 7), (1, "How to Use This Book", 8)]
    for n, t, a, b in ARCS:
        entries.append((1, f"Arc {n} · {t} (Days {a}–{b})", 100 + n))
    entries += [(1, "Final Reflection", 50), (1, "Where I Am Now", 51), (1, "Next-Step Challenge and Closing Prayer", 52),
                (1, "Certificate of Completion", 53), (1, "Help, Right Now", 54)]
    keys = [str(k) for (_, _, k) in entries]
    ahead_items = [(str(n), f"{t} · Days {a}–{b}", lib.PATH_ROWS[n - 1][2] + ".") for n, t, a, b in ARCS]
    by_day = {d[0]: d for d in COMPANION_DAYS}

    def body(pmap):
        toc = lib.toc_html(entries)
        for k in keys:
            toc = toc.replace(f"@@P{k}@@", pmap.get(k, ""))
        def tag(html, h1, k):
            return html.replace(f"<h1>{h1}</h1>", f"<h1>{h1}{mk(k)}</h1>")
        ahead = tag(lib.ahead_page("What’s ahead", "What’s Ahead", ahead_items), "What’s Ahead", 1)
        how = tag(lib.how_to_read(), "How to Read This Book", 2)
        pathp = tag(lib.path_page(), "Your 90-Day Path", 5)
        warf = tag(WARFARE, "Spiritual Warfare, Plainly", 6)
        moms = tag(MOTHERS, "A Word to Mothers", 7)
        use = tag(USE, "How to Use This Book", 8)
        parts = []
        for arc in ARCS:
            parts.append(arc_divider(arc))
            for n in range(arc[2], arc[3] + 1):
                parts.append(left(by_day[n], arc[0]))
                parts.append(right(by_day[n], arc[0]))
        closing = lib.closing_pages("Ninety Days of Standing", [f"Arc {n} · {t}" for n, t, a, b in ARCS], "Arc",
            "Go back to Day 1 of this book and the journal and read what you wrote. Then choose one practice (the armor, the craving protocol, the silence, a boundary, a blessing for your children) and keep it for thirty days. Tell one person which one.")
        closing = (closing.replace("<h1>Final Reflection</h1>", f"<h1>Final Reflection{mk(50)}</h1>")
                          .replace("<h1>Where I Am Now</h1>", f"<h1>Where I Am Now{mk(51)}</h1>")
                          .replace("<h1>Next-Step Challenge</h1>", f"<h1>Next-Step Challenge{mk(52)}</h1>"))
        cert = lib.certificate("Ninety Days of Standing").replace("Certificate of Completion</div>", f"Certificate of Completion{mk(53)}</div>", 1)
        extra = "".join(f"<tr><td><strong>{esc(a)}</strong></td><td>{esc(b)}</td></tr>" for a, b in [
            ("Childhelp National Child Abuse Hotline", "1-800-422-4453"),
            ("Postpartum Support International", "1-800-944-4773"),
            ("National Maternal Mental Health Hotline", "1-833-852-6262")])
        res = lib.resources_page(extra_rows=extra).replace("<h1>Help, Right Now</h1>", f"<h1>Help, Right Now{mk(54)}</h1>")
        return "\n".join([
            lib.cover("Ninety Days<br>of Standing", "Spiritual Warfare for Survivors and Mothers", "You survived. Now we rebuild.",
                      "Childhood · Addiction · Motherhood · Faith<br>A daily companion to the 90-Day Journal"),
            lib.title_page("Ninety Days<br>of Standing", "Spiritual warfare, childhood trauma, addiction, and motherhood<br>One spread a day, paired with the 90 Days of Freedom Journal, the Workbook, and Volume II",
                           "For Brandi Renee — and for every mother, and every daughter, still standing."),
            lib.copyright_page("Ninety Days of Standing — A Daily Companion on Spiritual Warfare, Childhood Trauma, Addiction, and Motherhood"),
            toc, ahead, how, pathp, warf, moms, use] + parts + [closing, cert, res])

    slug = "ninety-days-of-standing"
    html_path = os.path.join(lib.OUT, slug + ".html")
    pdf_path = os.path.join(lib.OUT, slug + ".pdf")
    title = "Ninety Days of Standing — Spiritual Warfare Companion"
    pmap = {k: "000" for k in keys}
    open(html_path, "w").write(lib.page(title, body(pmap), CSS))
    lib.render_pdf(html_path, pdf_path)
    found, n = lib.find_marker_pages(pdf_path, keys)
    miss = [k for k in keys if k not in found]
    if miss:
        print("  warn: missing TOC keys", miss)
    pmap = {k: str(found.get(k, "")) for k in keys}
    open(html_path, "w").write(lib.page(title, body(pmap), CSS))
    lib.render_pdf(html_path, pdf_path)
    f2, n2 = lib.find_marker_pages(pdf_path, keys)
    if any(f2.get(k) != found.get(k) for k in keys):
        print("  warn: page numbers shifted")
    print(f"{slug}: {n2} pages -> {pdf_path}")
