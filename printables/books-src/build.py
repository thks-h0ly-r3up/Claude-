#!/usr/bin/env python3
"""Build the three 7HE H0LY R3UP books (journal, workbook, Volume II) into printables/.

    python3 books-src/build.py            # all three
    python3 books-src/build.py workbook   # one of: journal | workbook | volume2

Sources live in books-src/original/ and are never modified. Editorial corrections are
applied from edits_*.py; the build stops if any correction no longer matches exactly once.
"""
import importlib.util
import os
import re
import sys

import lib
from lib import BRAND, esc, inline
from mdbook import convert, mk

HERE = lib.HERE
OUT = lib.OUT

EXTRA_CSS = ".mk{font-size:2px;line-height:0;color:rgba(255,255,255,.01);letter-spacing:0}"

def load_edits(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.EDITS

def apply_edits(text, edits, label):
    for i, (old, new) in enumerate(edits):
        c = text.count(old)
        if c != 1:
            raise SystemExit(f"[{label}] edit #{i} matched {c} times: {old[:90]!r}")
        text = text.replace(old, new)
    return text

def brand_fix(text, label):
    text = text.replace("**7HE H0LY KIL0 SYNDICATE (THKS)**", "")
    text = re.sub(r"\*\*7HE H0LY KIL0 SYNDICATE\*\*\n\*Reaching back\. Freeing the bound\. Saying the things everybody's afraid to say\.\*\n?", "", text)
    text = text.replace("7HE H0LY KIL0 SYNDICATE", BRAND)
    for bad in ("THKS", "KIL0", "SYNDICATE", "REUP"):
        if bad in text:
            i = text.index(bad)
            raise SystemExit(f"[{label}] retired name still present: {text[max(0,i-60):i+60]!r}")
    return text

def read(name):
    return open(os.path.join(HERE, "original", name), encoding="utf-8").read()

# ---------------------------------------------------------------------------
def build_md_book(cfg):
    label = cfg["slug"]
    md = apply_edits(read(cfg["src"]), load_edits(cfg["edits"]), label)
    md = cfg["slice"](md)
    md = brand_fix(md, label)
    main_html, heads = convert(md, chapter_breaks=cfg["chapter_breaks"], start_key=100)

    front = [(1, "What’s Ahead", 1), (1, "How to Read This Book", 2), (1, "Your 90-Day Path", 5)]
    if cfg.get("intro_html"):
        front.append((1, "Introduction", 3))
    back = [(1, "Final Reflection", 50), (1, "Where I Am Now", 51), (1, "Next-Step Challenge and Closing Prayer", 52),
            (1, "Certificate of Completion", 53), (1, "Help, Right Now", 54)]
    entries = front + [(l, t, k) for (l, t, k) in heads] + back
    keys = [str(k) for (_, _, k) in entries]

    def body(pmap):
        ahead = lib.ahead_page("What’s ahead", "What’s Ahead", cfg["ahead"]).replace("<h1>What’s Ahead</h1>", f"<h1>What’s Ahead{mk(1)}</h1>")
        how = lib.how_to_read().replace("<h1>How to Read This Book</h1>", f"<h1>How to Read This Book{mk(2)}</h1>")
        pathp = lib.path_page().replace("<h1>Your 90-Day Path</h1>", f"<h1>Your 90-Day Path{mk(5)}</h1>")
        intro = ""
        if cfg.get("intro_html"):
            intro = cfg["intro_html"].replace("<h1>Introduction</h1>", f"<h1>Introduction{mk(3)}</h1>")
        toc = lib.toc_html(entries)
        for k in keys:
            toc = toc.replace(f"@@P{k}@@", pmap.get(k, ""))
        closing = lib.closing_pages(cfg["title"], cfg["units"], cfg["unit_word"], cfg["challenge"])
        closing = (closing.replace("<h1>Final Reflection</h1>", f"<h1>Final Reflection{mk(50)}</h1>")
                          .replace("<h1>Where I Am Now</h1>", f"<h1>Where I Am Now{mk(51)}</h1>")
                          .replace("<h1>Next-Step Challenge</h1>", f"<h1>Next-Step Challenge{mk(52)}</h1>"))
        cert = lib.certificate(cfg["cert_title"]).replace("Certificate of Completion</div>", f"Certificate of Completion{mk(53)}</div>", 1)
        res = lib.resources_page().replace("<h1>Help, Right Now</h1>", f"<h1>Help, Right Now{mk(54)}</h1>")
        return "\n".join([
            lib.cover(cfg["cover_title"], cfg["cover_sub"], "You survived. Now we rebuild.", cfg["cover_by"]),
            lib.title_page(cfg["cover_title"], cfg["title_sub"], cfg["dedication"]),
            lib.copyright_page(cfg["full_title"]),
            toc, ahead, how, pathp, intro,
            '<main class="body" style="break-before:page">' + main_html + "</main>",
            closing, cert, res])

    html_path = os.path.join(OUT, cfg["slug"] + ".html")
    pdf_path = os.path.join(OUT, cfg["slug"] + ".pdf")
    n = lib.build_with_toc(cfg["full_title"], body, keys, html_path, pdf_path)
    print(f"{cfg['slug']}: {n} pages -> {pdf_path}")
    return n

# ---------------------------------------------------------------------------
WORKBOOK = dict(
    slug="trauma-and-the-spiritual-realm-workbook",
    src="workbook.md", edits="edits_workbook",
    title="Trauma and the Spiritual Realm",
    full_title="Trauma and the Spiritual Realm — A Complete Unfiltered Workbook",
    cover_title="Trauma and the<br>Spiritual Realm",
    cover_sub="A Complete Unfiltered Workbook",
    cover_by="Built by a survivor.<br>Written for the ones still in the gap.",
    title_sub="A Complete Unfiltered Workbook<br>Built by a survivor. Written for the ones still in the gap.",
    dedication="For Brandi Renee — and for the one who finds this in the middle of the night.",
    cert_title="Trauma and the Spiritual Realm<br>Workbook",
    chapter_breaks=False,
    slice=lambda md: md[md.index("> This is for the person who knows"): md.index("## RESOURCES — KEEP THIS PAGE")],
    ahead=[
        ("I", "Trauma — what actually happened to you", "Name what trauma did to your body, mind, and spirit; sort the lies it taught you; learn body-based resets you can use right away."),
        ("II", "The Spiritual Realm — the crash course", "A plain-language look at what Scripture says is real, how to sort body, wound, flesh, and spirit, and how to pray it through."),
        ("III", "The Chosen One — the deep dive", "What “chosen” and “called” mean in Scripture, what they cost, and how to tell calling from ego."),
        ("IV", "Survivor of Addiction and Abuse", "How the two braid together, what addiction was doing for you, naming abuse without softening it, and the moral injury nobody writes workbooks about."),
        ("V", "Roadmap: Breaking Addiction", "Ten steps, in order — honesty, medical care, a date, trigger chains, replacements, structure, cravings, a relapse plan, spiritual support, and milestones."),
        ("VI", "Roadmap: Breaking Generational Curses", "Map the patterns in your family, find where they may have started, and build the new behavior that prayer alone does not teach."),
        ("VII", "Letting People Go, and Sitting Silent With God", "Four kinds of letting go, grieving someone you lost to addiction, and a slow practice of silence for people whose nervous systems learned that quiet means danger."),
    ],
    units=["I · Trauma", "II · The Spiritual Realm", "III · The Chosen One", "IV · Addiction and Abuse", "V · Breaking Addiction", "VI · Generational Patterns", "VII · Letting Go and Silence"],
    unit_word="Part",
    challenge="Pick one Work Page you skipped or rushed. Go back to it this week — with a safe person nearby if you can — and write one honest paragraph. Then tell one person you did.",
)

VOLUME2 = dict(
    slug="the-whole-story-volume-ii",
    src="volume2.md", edits="edits_volume2",
    title="The Whole Story, Volume II",
    full_title="The Whole Story, Volume II — Soul Contracts, Covenants, Curses, the Enemy’s Full Playbook, and Exactly Where God Was",
    cover_title="The Whole Story",
    cover_sub="Volume II · The Master Companion to<br>Trauma and the Spiritual Realm",
    cover_by="Nothing left out. No topic untouched.<br>Every painful thing named — and then worked through.",
    title_sub="Volume II<br>Soul Contracts, Covenants, Curses, the Enemy’s Full Playbook, and Exactly Where God Was",
    dedication="For Brandi Renee — and for the one who finds this at 3 a.m.",
    cert_title="The Whole Story<br>Volume II",
    chapter_breaks=True,
    slice=lambda md: md[md.index("# BOOK ONE"): md.index("## RESOURCES — KEEP THIS PAGE")],
    ahead=[
        ("I", "The Architecture of Bondage", "A courtroom picture drawn from Scripture’s own language, a catalog of twenty-two agreements people make in pain, soul ties, words that bind, and how family patterns travel."),
        ("II", "The Enemy’s Complete Playbook", "Who he is, what he cannot do, twelve patterns that keep showing up, how callings get derailed, and how the church can be used to hurt people."),
        ("III", "Exactly How God Is Involved", "What God does not do, where He was, every honest answer to “why didn’t He stop it,” the cross, judgment, and what to do when He feels silent."),
        ("IV", "The Chosen One, Complete", "What “chosen” means, marks and seasons of a called life, the wilderness, temptations, costs, and the ones who fell."),
        ("V", "The Unraveling: Step by Step", "Thirty-three steps in four phases — excavation, praying it through, filling and rebuilding, and walking it out — with safety gates first."),
        ("VI", "The Unanswered Questions", "Forty questions people are afraid to ask, answered straight."),
        ("VII", "Brandi Renee", "Grieving someone lost to addiction: what you could and could not do, what her passing is and is not allowed to become, and laying her down without letting her go."),
        ("VIII", "The Two Futures", "A look at where an unchanged pattern tends to lead, and what can grow when someone does the work — not a prophecy and not a promise."),
        ("IX", "Becoming the Woman God Chose", "An identity, a twelve-month roadmap, a daily rule of life, and a commission — plus a Scripture arsenal by need."),
    ],
    units=["I · Architecture of Bondage", "II · The Enemy’s Playbook", "III · How God Is Involved", "IV · The Chosen One", "V · The Unraveling", "VI · Unanswered Questions", "VII · Brandi Renee", "VIII · The Two Futures", "IX · Becoming Her"],
    unit_word="Book",
    challenge="Choose one thing from Book Five you have been circling. Put a date on it, tell one person, and take the smallest honest version of the step this week.",
    intro_html=f"""<section class="fm"><div class="band"></div><div class="kick">Start here</div><h1>Introduction</h1>
<blockquote class="epigraph"><p>If you are reading this, you already know something got its hooks in you and you have never been able to name it.</p>
<p>This book names it. Every agreement, every door, every pattern, and the exact place God was standing while it happened. Then it shows you how to work through it, step by step, with Scripture, with safe people, and with the authority Christ gives His own.</p></blockquote>
<p>This is the companion to <em>Trauma and the Spiritual Realm</em>. That workbook gave you the crash course. This book goes deeper: what vows and agreements made in pain can do to a life, how patterns travel through families, what Scripture says about the enemy, where God was, and how to walk it out over months, not a weekend.</p>
<p><strong>How to use it.</strong> Read Books One through Three straight through once. Work Book Five slowly, with a safe person beside you. Come back to Books Six through Nine when you are ready for the harder questions. Write on the lines. Skip whatever stirs up more than you can hold.</p>
<p><strong>A word about the big pictures.</strong> Contracts, doors, stages, seasons — these are pictures. Scripture uses legal and relational language, and these pictures lean on it, but Christians hold different views about how literally to take them. Test all of it against the Bible and with people who know you. Keep what helps. Put down what does not.</p>
<p><strong>You do not have to do this alone.</strong> If you can reach a trauma-informed counselor, do. Prayer and professional care belong side by side. And if a page ever opens something you cannot close, stop and call someone. The page will wait.</p>
</section>""",
)

# ---------------------------------------------------------------------------
# Journal
# ---------------------------------------------------------------------------
ARC_COLORS = ["#27857f", "#7a4c9e", "#d6598f", "#4a6486", "#27857f", "#7a4c9e", "#d6598f", "#4a6486", "#c58a2d"]
ARC_NOTES = {
    1: "Say what is true. Get the medical picture, learn six body resets, and set a date.",
    2: "Find the lies trauma taught you and trade the names you answered to for the ones God gives.",
    3: "A plain look at what Scripture says is real, what you can and cannot do, and how to forgive without reopening the door.",
    4: "The vows, words, and agreements made in pain — named and released, one at a time.",
    5: "What ran in your family, what is yours to change, and how to honor without repeating.",
    6: "Patterns to notice, and the daily structure that holds: HALT, cravings, replacing the function, boundaries, and a plan for the day you fall.",
    7: "Where God was, why He did not stop it, and how to be angry at Him and still stay.",
    8: "Grief, guilt, and letting go — of the one you lost and the living you have to release.",
    9: "Consecrated, sent, and stewarding what you have learned for somebody else.",
}

def build_journal():
    from companion import COMPANION_DAYS
    STAND = {d[0]: d[1] for d in COMPANION_DAYS}
    from home_days_1 import H1
    from home_days_2 import H2
    from home_days_3 import H3
    HOME = {d[0]: d[1] for d in H1 + H2 + H3}
    label = "journal"
    t = open(os.path.join(HERE, "original", "journal_text.txt"), encoding="utf-8").read()
    t = apply_edits(t, load_edits("edits_journal"), label)
    t = t.replace("7HE H0LY KIL0 SYNDICATE", BRAND)
    lines = [l for l in t.split("\n")]
    # --- days ---
    days, arcs = {}, []
    i = 0
    cur_arc = 0
    while i < len(lines):
        ln = lines[i].strip()
        m = re.match(r"^ARC (\w+) · DAYS (\d+)[–-](\d+)$", ln)
        if m:
            cur_arc += 1
            title = lines[i + 1].strip()
            arcs.append(dict(n=cur_arc, title=title, first=int(m.group(2)), last=int(m.group(3))))
            i += 3
            continue
        m = re.match(r"^(.+?)\tDAY (\d\d)$", ln)
        if m:
            n = int(m.group(2))
            blk = []
            j = i + 1
            while j < len(lines) and not re.match(r"^(.+?)\tDAY \d\d$", lines[j].strip()) and not lines[j].startswith("ARC ") and not lines[j].startswith("DAY NINETY-ONE"):
                if lines[j].strip():
                    blk.append(lines[j].strip())
                j += 1
            title, verse, teach = blk[0], blk[1], blk[2]
            assert blk[3].startswith("TODAY"), (n, blk[3])
            prompt, decl = blk[4], blk[5]
            mv = re.match(r'^"(.*)"\s+—\s+(.*)$', verse)
            days[n] = dict(arc=cur_arc, title=title, vtext=mv.group(1), vref=mv.group(2), teach=teach, prompt=prompt, decl=decl)
            i = j
            continue
        i += 1
    assert sorted(days) == list(range(1, 91)), len(days)
    k91 = next(idx for idx, l in enumerate(lines) if l.startswith("DAY NINETY-ONE"))
    tail = [l.strip() for l in lines[k91:] if l.strip()]

    def dots(n):
        return "".join(f'<i class="{"on" if d <= n else ""}"></i>' for d in range(1, 91))

    RULES = "<div></div>" * 24

    def day_html(n):
        d = days[n]
        c = ARC_COLORS[d["arc"] - 1]
        arc_title = arcs[d["arc"] - 1]["title"]
        return f"""<section class="dayp" style="--ac:{c}">
<div class="dband"></div>
<div class="dtop"><span class="arcpill">Arc {d['arc']} · {esc(arc_title)}</span><span class="dnum">Day {n:02d}<small> / 90</small></span></div>
<h1 class="dtitle">{esc(d['title'])}</h1>
<div class="pair">Pairs with <em>Ninety Days of Standing</em> · Day {n}: {esc(STAND[n])} &nbsp;|&nbsp; <em>Ninety Days of Coming Home</em> · Day {n}: {esc(HOME[n])}</div>
<blockquote class="dverse">“{esc(d['vtext'])}” <span class="ref">{esc(d['vref'])} · ESV</span></blockquote>
<p class="teach">{esc(d['teach'])}</p>
<div class="dwork"><span class="tag">Today’s Work</span><span class="date">Date: ____ / ____ / ________</span>
<div class="prompt">{esc(d['prompt'])}</div><div class="rules">{RULES}</div></div>
<div class="dsay"><span class="tag2">Say it out loud</span><div class="decl">{esc(d['decl'])}</div>
<div class="done"><span class="box"></span> I said it. I wrote it. That is enough for today.</div></div>
<div class="dfoot"><div class="dots">{dots(n)}</div><div class="bl">{BRAND} · Reaching back. Freeing the bound.</div></div>
</section>"""

    def arc_divider(a):
        c = ARC_COLORS[a["n"] - 1]
        return f"""<section class="opener jopen" style="background:linear-gradient(175deg,{c} 0%,#7a4c9e 62%,#d6598f 100%)">
<div class="kicker">Arc {a['n']} · Days {a['first']}–{a['last']}</div><h1>{esc(a['title'])}{mk(100 + a['n'])}</h1>
<div class="orn"></div><div class="sub">{esc(ARC_NOTES[a['n']])}</div><div class="bm">{BRAND} · {a['last']-a['first']+1} pages</div></section>"""

    # --- front matter ---
    prayer_paras = [
        "Father, I come to You through Jesus Christ, who died for me and rose again. I am not coming to You cleaned up. I am coming to You honest.",
        "You already know every page of this. You know what was done to me, what I did afterward, what I have never said out loud, and what I am still afraid is true about me. Nothing in these ninety days is going to surprise You.",
        "So I am asking: come into it. Do not let me do this alone and do not let me do it in my own strength, because my own strength is what got me this far and this far is not far enough.",
        "Show me the truth even where it costs me. Show me the doors I left open. Show me the words I agreed with. Show me what is mine to carry and what I have been carrying that was never mine. Give me the courage to write it down instead of managing it for one more year.",
        "Where I am about to find shame, bring light. Where I am about to find grief, sit with me in it and do not rush me out. Where I am about to find rage, let me bring it to You instead of holding it against You.",
        "Release me from every agreement I made in pain. Loosen every vow I made to survive. Close every door I opened and never knew how to shut. Let the pattern in my family stop with me. And fill every room that empties, because I am not willing to be a house standing open again.",
        "For my sister Brandi Renee — I put her in Your hands, not mine. I am not paying a debt with my life. I am carrying her name because I loved her.",
        "And when these ninety days are done, let me be who You made me before anybody ever hurt me. Let somebody else get out because I did. In Jesus’ name. Amen.",
    ]
    prayer = "".join(f"<p>{esc(p)}</p>" for p in prayer_paras)
    howto = [
        ("One page per day, and only one.", "The pace is the point. This is not information you need — you have had information for years. This is practice, a little at a time."),
        ("Write on the lines.", "In pen if you can. Thinking about the answer is not the same as writing it. Written words are evidence, and evidence is what you will read back on the hard days."),
        ("Say the declaration out loud.", "At the bottom of every page. Standing if you can, even when you do not believe it yet. Especially then."),
        ("Do the pages in order.", "The arcs build. You cannot change what you have not named, and you cannot name it while you are still calling it your personality."),
        ("Date every page.", "In ninety days you will want to know when things turned."),
        ("Tell one person you are doing this.", "Isolation makes everything harder. Do not carry this alone."),
        ("If a page opens something too big, stop and call somebody.", "Not tomorrow. That day. The crisis numbers are in the back of this book, and using them is not weakness — it is what the pages are for."),
        ("Missing a day is not failure.", "Pick the page back up. The identity is in the rising."),
        ("You are allowed to adjust.", "Skip the writing and only say the declaration. Keep your eyes open. Use a different anchor — cold water, your feet on the floor. This journal does not replace counseling, medical care, or safety planning."),
    ]
    howto_html = "".join(f'<li><strong>{esc(a)}</strong> {esc(b)}</li>' for a, b in howto)
    ahead_items = [(str(a["n"]), f"{a['title']} · Days {a['first']}–{a['last']}", ARC_NOTES[a["n"]]) for a in arcs]

    entries = [(1, "What’s Ahead", 1), (1, "How to Read This Book", 2), (1, "Your 90-Day Path", 5), (1, "The Prayer Over This Book", 3), (1, "How to Use This Journal", 4)]
    for a in arcs:
        entries.append((1, f"Arc {a['n']} · {a['title']} (Days {a['first']}–{a['last']})", 100 + a["n"]))
    entries += [(1, "Day 91 · Begin Again", 60), (1, "Final Reflection", 50), (1, "Where I Am Now", 51),
                (1, "Next-Step Challenge and Closing Prayer", 52), (1, "Certificate of Completion", 53), (1, "Help, Right Now", 54)]
    keys = [str(k) for (_, _, k) in entries]

    # day 91 page
    ninety1 = [l for l in tail]
    # tail: DAY NINETY-ONE, Begin Again, THE NEXT LAYER..., AFTER NINETY DAYS, p, p, p, p, Signed..., KEEP THIS PAGE ...
    idx_after = ninety1.index("AFTER NINETY DAYS")
    idx_signed = next(ix for ix, l in enumerate(ninety1) if l.startswith("Signed:"))
    paras91 = ninety1[idx_after + 1: idx_signed]

    def body(pmap):
        toc = lib.toc_html(entries)
        for k in keys:
            toc = toc.replace(f"@@P{k}@@", pmap.get(k, ""))
        ahead = lib.ahead_page("What’s ahead", "What’s Ahead", ahead_items).replace("<h1>What’s Ahead</h1>", f"<h1>What’s Ahead{mk(1)}</h1>")
        how = lib.how_to_read().replace("<h1>How to Read This Book</h1>", f"<h1>How to Read This Book{mk(2)}</h1>")
        pathp = lib.path_page().replace("<h1>Your 90-Day Path</h1>", f"<h1>Your 90-Day Path{mk(5)}</h1>")
        prayer_pg = f'<section class="fm"><div class="band"></div><div class="kick">Say it out loud before day one</div><h1>The Prayer Over This Book{mk(3)}</h1><p class="small">Say it again any day you need it.</p><blockquote class="prayer" style="font-size:10.2pt;line-height:1.6">{prayer}</blockquote></section>'
        howto_pg = f'<section class="fm"><div class="band"></div><div class="kick">Ninety pages · one a day</div><h1>How to Use This Journal{mk(4)}</h1><ol style="font-size:10pt;line-height:1.55">{howto_html}</ol></section>'
        parts = []
        for a in arcs:
            parts.append(arc_divider(a))
            for n in range(a["first"], a["last"] + 1):
                parts.append(day_html(n))
        day91 = f"""<section class="dayp" style="--ac:#c58a2d;page:day">
<div class="dband"></div>
<div class="dtop"><span class="arcpill">After ninety days</span><span class="dnum">Day 91</span></div>
<h1 class="dtitle">Begin Again{mk(60)}</h1>
<blockquote class="dverse">The next layer is only visible from ground you already took.</blockquote>
{''.join(f'<p class="teach" style="font-size:11.5pt">{esc(p)}</p>' for p in paras91)}
<div class="dsay" style="margin-top:.2in"><span class="tag2">Sign it</span>
<div class="decl" style="margin-top:.25in">Signed: ______________________________________ &nbsp; Date: ____ / ____ / ________</div></div>
<div class="dfoot"><div class="dots">{dots(90)}</div><div class="bl">{BRAND} · Reaching back. Freeing the bound.</div></div></section>"""
        closing = lib.closing_pages("90 Days of Freedom", [f"Arc {a['n']} · {a['title']}" for a in arcs], "Arc",
            "Go back to Day 1 and read what you wrote — not to grade yourself, to see it. Then choose one practice (the armor, the craving protocol, the silence, the release) and keep it for the next thirty days. Tell one person which one.")
        closing = (closing.replace("<h1>Final Reflection</h1>", f"<h1>Final Reflection{mk(50)}</h1>")
                          .replace("<h1>Where I Am Now</h1>", f"<h1>Where I Am Now{mk(51)}</h1>")
                          .replace("<h1>Next-Step Challenge</h1>", f"<h1>Next-Step Challenge{mk(52)}</h1>"))
        cert = lib.certificate("Ninety Days of Freedom").replace("Certificate of Completion</div>", f"Certificate of Completion{mk(53)}</div>", 1)
        res = lib.resources_page().replace("<h1>Help, Right Now</h1>", f"<h1>Help, Right Now{mk(54)}</h1>")
        return "\n".join([
            lib.cover("Ninety Days<br>of Freedom", "A Daily Journal · One Page a Day", "You survived. Now we rebuild.",
                      "A daily companion to <em>The Whole Story</em><br>One page a day. Ninety days. Written lines."),
            lib.title_page("Ninety Days<br>of Freedom", "One Page a Day<br>A daily companion to The Whole Story — trauma, the spiritual realm, the agreements made in pain, the family line, and becoming who God made you to be.",
                           "For Brandi Renee — and for the one who finds this at 3 a.m."),
            lib.copyright_page("Ninety Days of Freedom — A Daily Journal"),
            toc, ahead, how, pathp, prayer_pg, howto_pg] + parts + [day91, closing, cert, res])

    css = EXTRA_CSS + r"""
.jopen{page:day;width:auto;height:10.12in;border-radius:18px;padding:.9in .8in}
.jopen:before{inset:.2in;border-radius:12px}
.jopen .bm{left:.8in;bottom:.7in}
.dayp .dband{height:8px;background:linear-gradient(90deg,var(--ac),#7a4c9e 60%,#d6598f);border-radius:4px;margin-bottom:.11in}
.dayp .dtop{display:flex;justify-content:space-between;align-items:center}
.dayp .arcpill{background:var(--ac);color:#fff;font:800 8pt 'Libre Franklin';letter-spacing:.14em;text-transform:uppercase;padding:3px 12px;border-radius:20px}
.dayp .dnum{font:700 26pt/1 'Caveat';color:var(--ac)} .dayp .dnum small{font:700 10pt 'Libre Franklin';color:#8f82a3}
.dayp .pair{font:700 7.8pt 'Libre Franklin';letter-spacing:.06em;color:#4a6486;margin:-.01in 0 .05in;text-transform:none}
.dayp .pair em{font-style:normal;color:#d6598f}
.dayp .dtitle{font:700 36pt/1.02 'Caveat';color:#7a4c9e;margin:.06in 0 .04in;border:0;padding:0}
.dayp .dverse{font:600 14pt/1.25 'Caveat';color:var(--ink);background:linear-gradient(90deg,rgba(63,182,176,.14),rgba(214,89,143,.09));border-radius:12px;padding:.08in .2in;margin:.06in 0 .09in;text-align:center}
.dayp .dverse .ref{display:block;font:700 7.6pt 'Libre Franklin';letter-spacing:.14em;text-transform:uppercase;color:#4a6486;margin-top:2px}
.dayp .teach{font-size:10.6pt;line-height:1.52;margin:0 0 .1in}
.dayp .dwork{flex:1;border:1.6px solid var(--line);border-radius:14px;background:#fff;position:relative;padding:.2in .2in .1in;display:flex;flex-direction:column;min-height:0}
.dayp .tag,.dayp .tag2{position:absolute;top:-12px;left:16px;color:#fff;font:800 8.2pt 'Libre Franklin';letter-spacing:.12em;text-transform:uppercase;padding:3px 12px;border-radius:20px;background:var(--ac)}
.dayp .tag2{background:#d6598f}
.dayp .date{position:absolute;top:-10px;right:16px;background:#fff;border:1px solid var(--line);font:700 8pt 'Libre Franklin';color:#4a6486;padding:2px 10px;border-radius:20px}
.dayp .prompt{font:700 10pt/1.35 'Libre Franklin';font-style:italic;color:#4a6486;margin:.02in 0 .02in}
.dayp .rules{flex:1;min-height:.6in;overflow:hidden}
.dayp .rules div{height:.3in;border-bottom:1.2px solid #d3c8e0}
.dayp .dsay{border:1.6px solid var(--line);border-left:7px solid #d6598f;border-radius:12px;background:#fff;position:relative;padding:.16in .2in .09in;margin-top:.17in}
.dayp .decl{font:700 18pt/1.15 'Caveat';color:#7a4c9e;text-align:center}
.dayp .done{display:flex;align-items:center;justify-content:center;gap:8px;font:700 8.6pt 'Libre Franklin';color:#7a4c9e;margin-top:.05in}
.dayp .dfoot{margin-top:.1in;text-align:center}
.dayp .dots{display:flex;gap:2px;justify-content:center;margin-bottom:.05in}
.dayp .dots i{display:block;width:5px;height:5px;border-radius:50%;background:#e3dcec}
.dayp .dots i.on{background:var(--ac)}
.dayp .bl{font:800 7pt 'Libre Franklin';letter-spacing:.2em;text-transform:uppercase;color:#7a4c9e}
"""
    slug = "90-days-of-freedom-journal"
    html_path = os.path.join(OUT, slug + ".html")
    pdf_path = os.path.join(OUT, slug + ".pdf")
    # custom two-pass with extra css
    pmap = {k: "000" for k in keys}
    open(html_path, "w").write(lib.page("Ninety Days of Freedom — A Daily Journal", body(pmap), css))
    lib.render_pdf(html_path, pdf_path)
    found, n = lib.find_marker_pages(pdf_path, keys)
    missing = [k for k in keys if k not in found]
    if missing:
        print("  warn: missing TOC keys", missing)
    pmap = {k: str(found.get(k, "")) for k in keys}
    open(html_path, "w").write(lib.page("Ninety Days of Freedom — A Daily Journal", body(pmap), css))
    lib.render_pdf(html_path, pdf_path)
    f2, n2 = lib.find_marker_pages(pdf_path, keys)
    if any(f2.get(k) != found.get(k) for k in keys):
        print("  warn: page numbers shifted")
    print(f"{slug}: {n2} pages -> {pdf_path}")

# ---------------------------------------------------------------------------
if __name__ == "__main__":
    want = sys.argv[1:] or ["journal", "workbook", "volume2", "companion", "home"]
    lib_page = lib.page
    # inject the marker css into every md book
    lib.page = lambda title, body, extra_css="": lib_page(title, body, EXTRA_CSS + extra_css)
    if "workbook" in want:
        build_md_book(WORKBOOK)
    if "volume2" in want:
        build_md_book(VOLUME2)
    if "journal" in want:
        build_journal()
    if "companion" in want:
        import build_companion
        build_companion.build()
    if "home" in want:
        import build_home
        build_home.build()
