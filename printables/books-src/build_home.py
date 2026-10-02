"""Ninety Days of Coming Home — a guided, Jesus-centered inner-child journey with daily prayer,
affirmation, challenge and task, paired day-for-day with the journal and the Standing companion."""
import os

import lib
from lib import BRAND, esc
from mdbook import mk
from companion import COMPANION_DAYS
from build_companion import JOURNAL_TITLES, ARC_COLORS
from home_days_1 import H1
from home_days_2 import H2
from home_days_3 import H3

HOME_DAYS = H1 + H2 + H3
assert [d[0] for d in HOME_DAYS] == list(range(1, 91))
STAND = {d[0]: d for d in COMPANION_DAYS}

STAGES = [
 (1, "Build Her a Safe Place", 1, 10, "Before going anywhere near the past, you build a place, a team, and ground rules in the present."),
 (2, "Meet Her at the Doorway", 11, 20, "Short, gentle visits from the doorway. Listening, naming, and telling her what is true."),
 (3, "Stand Guard for Her", 21, 30, "You become the adult who stands between her and the old voices, with Jesus beside you."),
 (4, "Release What She Promised", 31, 45, "The vows, words, and holds she took on. Released, one at a time, with comfort."),
 (5, "Show Her Her Family Line", 46, 55, "What she inherited, the good she gets to keep, and a promise that the line stops here."),
 (6, "Build Her a House", 56, 68, "Routine, comfort, boundaries, and a plan for the hard days. A home that holds."),
 (7, "Where Was Jesus?", 69, 76, "Honest questions, honest anger, quiet, and what God can use."),
 (8, "Say Goodbye and Hello", 77, 84, "Grief, release, and welcoming what comes next."),
 (9, "Meet the New You", 85, 90, "She meets the woman she is becoming. You bring her home."),
]

FALLBACK = [
 "Too much today? Open your eyes, name five things you see, and stop. Stopping is part of the practice.",
 "If this stirs up more than you can hold, do your landing (warm drink, a walk, a text) and come back tomorrow.",
 "You can do the prayer and skip the step. That still counts.",
 "If you feel far away or numb, press your feet into the floor and look around the room for the exit and the date.",
 "Swap the step for something small and kind: water, a snack, a stretch. That is practice too.",
 "If nothing comes, nothing is required. Rest is allowed.",
]

JAR_CHALLENGES = ["Text someone a photo of something beautiful you see today.", "Drink a full glass of water before anything else.", "Walk around the block and count how many different trees or flowers you see.", "Listen to a song you loved as a kid, all the way through.", "Write three things you can smell, taste, or feel right now.", "Tidy one drawer for five minutes.", "Sincerely compliment someone.", "Take a slow bath or shower and thank your body.", "Call someone you have not talked to in a month.", "Stand in sunlight for five minutes.", "Make your bed with care.", "Give away one thing you no longer need.", "Eat something colorful.", "Write a thank-you note to someone who helped you.", "Turn off screens an hour before bed.", "Pray the Lord’s Prayer slowly, one line at a time.", "Do ten slow stretches.", "Doodle for ten minutes with no goal.", "Sing one worship song out loud, even badly.", "Read one psalm aloud.", "Smile at yourself in the mirror and say your new name.", "Write one thing you did well today.", "Water or care for something living.", "Make something with your hands.", "Sit outside for ten minutes and just notice.", "Wear your favorite color today.", "Ask someone how they are, and really listen.", "Say no to one thing you do not have to do.", "List ten things you are grateful for.", "Dance silly for one song."]
JAR_PRAYERS = ["Lord, I am here. Be here too.", "Jesus, hold her hand and mine.", "Father, thank You for getting me through today.", "God, I do not have words. You know them.", "Holy Spirit, quiet what is loud in me.", "Lord, show me one thing I can do next.", "Jesus, stay near while I do the hard part.", "Father, give me rest tonight.", "God, protect the ones I love.", "Lord, teach me to be gentle with myself.", "Jesus, be the shelter I run to.", "Father, give me courage for one small step.", "God, I give You what I cannot fix.", "Lord, turn my eyes to what is true.", "Jesus, thank You for not giving up on me.", "Father, put safe people around me.", "God, help me forgive in my time.", "Lord, meet me in the quiet.", "Jesus, heal what I cannot reach.", "Father, I belong to You. Amen."]
JAR_AFFIRM = ["I am not too much and I am not too late.", "She was a child, and it was not her fault.", "I am allowed to rest.", "I can learn slowly and still be growing.", "God has not given up on me.", "I can be kind to myself today.", "I do not have to earn love.", "My story is not finished.", "I am safer than I used to be.", "I can ask for help.", "My feelings are information, not a verdict.", "I am allowed to have boundaries.", "I am more than my worst day.", "What I survived does not define my worth.", "I can start again as many times as I need.", "I am known and loved by God.", "I can tell the truth and still be held.", "My body kept me alive, and I can thank it.", "I can be gentle and strong.", "I am coming home."]
JAR_TASKS = ["Put 988 and your safe person’s number in your phone favorites.", "Write your safe-place details on a card and keep it with you.", "Schedule one appointment or call you have been avoiding.", "Clear one surface in your home for five minutes.", "Restock your landing kit.", "Reread one day of your journal.", "Pack a small bag: water, a snack, and a note to yourself.", "List your three safest people.", "Write your date and plan on a sticky note.", "Delete one app or contact that keeps you stuck.", "Lay out tomorrow’s clothes tonight.", "Save your boundary sentence in your phone notes.", "Make a simple three-day meal plan.", "Move your bedtime fifteen minutes earlier.", "Write one question for your counselor.", "Wash dishes or fold laundry as a prayer.", "Clean out one stress spot (a bag, a car, a purse).", "Write down your three early-warning signs.", "Look up one local support group or class.", "Take a photo of one thing that makes you feel safe."]

GOING_BACK = """<section class="fm"><div class="band"></div><div class="kick">Read this first</div><h1>Going Back Safely</h1>
<p>This book walks you through a prayerful, imaginative practice: visiting the child you were, comforting her, releasing what she promised to survive, and bringing her home to the woman you are becoming. It is a tool, not a cure, and these are the rules that keep it safe.</p>
<h2>What it is</h2>
<p>Prayerful imagination and compassion practice anchored in Scripture: God sees and comforts (Psalm 139:12; Isaiah 66:13), and Jesus welcomes children (Mark 10:14). The “room” and the “doorway” are pictures. They are not visions, and they are not literal memories.</p>
<h2>What it is not</h2>
<p>It is not memory recovery. You never hunt for memories, and you never try to reconstruct what you do not already know. It is not a ritual that frees anyone by itself, and it does not replace therapy, medicine, or safety planning. Imagining something does not make it true history.</p>
<h2>Your rules</h2>
<ul style="line-height:1.5"><li>You choose the pace. A stop word, a ten-minute timer, and a landing (warm drink, walk, a text to someone) are part of every visit.</li>
<li>Visit from the doorway. You never have to go into a scene.</li>
<li>Use only what you already know. If nothing comes, nothing is required.</li>
<li>Jesus is central. If you cannot picture Him, pray His words aloud instead.</li>
<li>If you feel far away, numb, flooded, or have flashbacks, stop, open your eyes, find the date and the exit, and do your landing.</li></ul>
<div class="safety"><h3>Do this with a trained trauma therapist if</h3><ul>
<li>your history includes severe or ongoing abuse, trafficking, or ritual abuse</li>
<li>you lose time, dissociate, or feel like parts of you are separate</li>
<li>visits leave you worse for more than a day</li></ul>
<p>If you are thinking about ending your life, call or text <strong>988</strong>. If you are in danger, call 911.</p></div></section>"""

HOWDAY = """<section class="fm"><div class="band"></div><div class="kick">How the daily page works</div><h1>Five Small Pieces</h1>
<div class="ahead">
<div class="item"><div class="n">1</div><div><div class="t">Return to Her</div><p>One short step for the day. It builds from safe place, to doorway, to guard, to release, to home, to meeting the new you.</p></div></div>
<div class="item"><div class="n">2</div><div><div class="t">Prayer</div><p>A few honest lines to say aloud. Skip it if words will not come; the step still counts.</p></div></div>
<div class="item"><div class="n">3</div><div><div class="t">Affirmation</div><p>A truth to say out loud: grounded in Scripture or fact, never a prediction or a guarantee.</p></div></div>
<div class="item"><div class="n">4</div><div><div class="t">Today’s challenge</div><p>One small, playful, or practical thing, to bring the body into it.</p></div></div>
<div class="item"><div class="n">5</div><div><div class="t">What she said / what I noticed</div><p>A few lines to write. No stories required.</p></div></div>
<div class="item"><div class="n">★</div><div><div class="t">The Challenge Jar</div><p>Cut the cards at the back. Draw one at random any time: when a day feels flat, when it feels too heavy, or when you finish early.</p></div></div>
</div>
<p style="margin-top:.15in"><strong>Same day, same path.</strong> Day N here pairs with Journal Day N and Standing Day N. Do the journal page first, then the Standing spread, then this page, or any order that fits your day. Each page tells you which Workbook section and Volume II chapter to read if you want more.</p>
</section>"""

CSS = r"""
.hd{page:day;height:10.12in;break-after:page;position:relative;display:flex;flex-direction:column}
.hd .dband{height:8px;background:linear-gradient(90deg,var(--ac),#7a4c9e 60%,#d6598f);border-radius:4px;margin-bottom:.1in}
.hd .dtop{display:flex;justify-content:space-between;align-items:center}
.hd .arcpill{background:var(--ac);color:#fff;font:800 8pt 'Libre Franklin';letter-spacing:.14em;text-transform:uppercase;padding:3px 12px;border-radius:20px}
.hd .dnum{font:700 26pt/1 'Caveat';color:var(--ac)} .hd .dnum small{font:700 10pt 'Libre Franklin';color:#8f82a3}
.hd .dtitle{font:700 33pt/1.02 'Caveat';color:#7a4c9e;margin:.05in 0 .04in;border:0;padding:0}
.hd .pairs{background:#f6f1fa;border:1px solid var(--line);border-radius:10px;padding:.06in .12in;font-size:8.1pt;line-height:1.4;margin-bottom:.12in}
.hd .pairs b{color:#7a4c9e}
.hd .box1{border:1.6px solid var(--line);border-left:7px solid var(--ac);border-radius:12px;background:#fff;padding:.15in .2in .1in;margin:.06in 0 .1in;position:relative}
.hd .tagx{position:absolute;top:-10px;left:14px;color:#fff;font:800 7.6pt 'Libre Franklin';letter-spacing:.12em;text-transform:uppercase;padding:2px 11px;border-radius:20px;background:var(--ac)}
.hd .box1 p{margin:0;font-size:11.2pt;line-height:1.55}
.hd .anchor{font:700 8pt 'Libre Franklin';letter-spacing:.1em;text-transform:uppercase;color:#4a6486;margin-top:.05in}
.hd .two{display:grid;grid-template-columns:1fr 1fr;gap:.14in;margin:.04in 0 .1in}
.hd .two .c{border:1.6px solid var(--line);border-radius:12px;background:#fff;padding:.15in .16in .1in;position:relative}
.hd .two .c.p{border-left:7px solid #d6598f} .hd .two .c.a{border-left:7px solid #7a4c9e}
.hd .two .c .tagx{background:#d6598f} .hd .two .c.a .tagx{background:#7a4c9e}
.hd .two .c p{margin:0;font-size:10.2pt;line-height:1.5}
.hd .two .c.a p{font:700 16pt/1.18 'Caveat';color:#7a4c9e;text-align:center}
.hd .chal{border:1.6px dashed #4a6486;border-radius:12px;background:#fbf8fd;padding:.13in .2in .09in;margin:.04in 0 .08in;position:relative;display:flex;gap:10px;align-items:flex-start}
.hd .chal .tagx{background:#4a6486}
.hd .chal p{margin:0;font-size:10.4pt;line-height:1.5}
.hd .toomuch{font:italic 600 8.6pt/1.4 'Libre Franklin';color:#4a6486;margin:0 0 .08in}
.hd .kick2{font:800 8.4pt 'Libre Franklin';letter-spacing:.16em;text-transform:uppercase;color:var(--ac);margin:.02in 0 .02in}
.hd .notes{flex:1;overflow:hidden}
.hd .notes div{height:.3in;border-bottom:1.2px solid #d3c8e0}
.hd .dfoot{margin-top:.08in;text-align:center}
.hd .dots{display:flex;gap:2px;justify-content:center;margin-bottom:.04in}
.hd .dots i{display:block;width:5px;height:5px;border-radius:50%;background:#e3dcec}
.hd .dots i.on{background:var(--ac)}
.hd .bl{font:800 7pt 'Libre Franklin';letter-spacing:.2em;text-transform:uppercase;color:#7a4c9e}
.jopen{page:day;width:auto;height:10.12in;border-radius:18px;padding:.9in .8in}
.jopen:before{inset:.2in;border-radius:12px}
.jopen .bm{left:.8in;bottom:.7in}
.jar{page:day;height:10.12in;break-after:page}
.jar h2{font:700 24pt 'Caveat';color:#7a4c9e;margin:0 0 .04in;border:0}
.jar .grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.08in}
.jar .card{border:1.5px dashed #8f82a3;border-radius:8px;padding:.07in .09in;font-size:8.6pt;line-height:1.35;min-height:.74in;background:#fff}
.jar .card b{display:block;font:800 6.8pt 'Libre Franklin';letter-spacing:.14em;text-transform:uppercase;margin-bottom:2px}
.jar .ch b{color:#27857f} .jar .pr b{color:#d6598f} .jar .af b{color:#7a4c9e} .jar .tk b{color:#4a6486}
.letter .lines div{height:.31in;border-bottom:1.2px solid #d3c8e0}
.mk{font-size:2px;line-height:0;color:rgba(255,255,255,.01);letter-spacing:0}
"""

def _dots(n):
    return "".join(f'<i class="{"on" if d <= n else ""}"></i>' for d in range(1, 91))

def stage_of(n):
    for s in STAGES:
        if s[2] <= n <= s[3]:
            return s

def day_page(d):
    n, title, step, pray, aff, chal, anchor = d
    st = stage_of(n)
    c = ARC_COLORS[st[0] - 1]
    s = STAND[n]
    return f"""<section class="hd" style="--ac:{c}"><div class="dband"></div>
<div class="dtop"><span class="arcpill">Stage {st[0]} · {esc(st[1])}</span><span class="dnum">Day {n:02d}<small> / 90</small></span></div>
<h1 class="dtitle">{esc(title)}</h1>
<div class="pairs"><b>Pairs with</b> Journal Day {n}: {esc(JOURNAL_TITLES[n])} &nbsp;·&nbsp; Standing Day {n}: {esc(s[1])} &nbsp;·&nbsp; <b>Also read</b> {esc(s[10])}</div>
<div class="box1"><span class="tagx">Return to her</span><p>{esc(step)}</p><div class="anchor">Anchor: {esc(anchor)}</div></div>
<div class="two"><div class="c p"><span class="tagx">Prayer</span><p>{esc(pray)}</p></div>
<div class="c a"><span class="tagx">Affirmation</span><p>{esc(aff)}</p></div></div>
<div class="chal"><span class="tagx">Today’s challenge</span><span class="box"></span><p>{esc(chal)}</p></div>
<div class="toomuch">{esc(FALLBACK[(n - 1) % len(FALLBACK)])}</div>
<div class="kick2">What she said · what I noticed</div><div class="notes">{"<div></div>" * 14}</div>
<div class="dfoot"><div class="dots">{_dots(n)}</div><div class="bl">{BRAND} · Ninety Days of Coming Home</div></div></section>"""

def stage_divider(st):
    n, t, a, b, note = st
    c = ARC_COLORS[n - 1]
    return f"""<section class="opener jopen" style="background:linear-gradient(175deg,{c} 0%,#7a4c9e 62%,#d6598f 100%)">
<div class="kicker">Stage {n} · Days {a}–{b}</div><h1>{esc(t)}{mk(100 + n)}</h1><div class="orn"></div>
<div class="sub">{esc(note)}</div><div class="bm">{BRAND} · Ninety Days of Coming Home</div></section>"""

def jar_pages():
    cards = ([("ch", "Challenge", t) for t in JAR_CHALLENGES] + [("pr", "Prayer", t) for t in JAR_PRAYERS] +
             [("af", "Affirmation", t) for t in JAR_AFFIRM] + [("tk", "Task", t) for t in JAR_TASKS])
    pages = []
    per = 24
    for i in range(0, len(cards), per):
        chunk = cards[i:i + per]
        inner = "".join(f'<div class="card {k}"><b>{lab}</b>{esc(t)}</div>' for k, lab, t in chunk)
        head = ""
        if i == 0:
            head = f"<h2>The Challenge Jar{mk(60)}</h2><p class=\"small\">Cut along the dashed lines, fold each card, and keep them in a jar or envelope. Draw one at random any time — when a day feels flat, when it feels too heavy, or when you finish early. Use as many or as few as you like.</p>"
        pages.append(f'<section class="jar">{head}<div class="grid">{inner}</div></section>')
    return "".join(pages)

def letter_pages():
    def pg(kick, title, intro, k=None):
        mkk = mk(k) if k else ""
        return f"""<section class="fm letter"><div class="band"></div><div class="kick">{kick}</div><h1>{title}{mkk}</h1><p>{intro}</p><div class="lines">{"<div></div>" * 23}</div></section>"""
    return "".join([
        pg("Day 87–90", "A Letter From Her", "Write as the girl at the doorway. Let her say what she has wanted to say. She can be angry, tender, funny, or quiet. You do not have to edit her.", 61),
        pg("Day 88–90", "A Letter From the New Me", "Write as the woman you are becoming: “I am here now. I am safe. I will not leave you. Here is what I promise.” Be specific and kind.", 62),
        f"""<section class="fm letter"><div class="band"></div><div class="kick">Day 90</div><h1>Our Promise{mk(63)}</h1>
<p>Read both letters aloud, then write one promise you can keep, small enough to do on a bad day.</p><div class="lines">{"<div></div>" * 9}</div>
<p style="margin-top:.3in">Signed: ____________________________________ &nbsp; Date: ____ / ____ / ________</p>
<p>Witnessed by: ____________________________________</p>
<p class="center" style="font:700 22pt 'Caveat';color:#d6598f;margin-top:.4in">Welcome home. We are a team. We are not finished, and we are not alone.</p></section>"""])

def build():
    entries = [(1, "What’s Ahead", 1), (1, "How to Read This Book", 2), (1, "Your 90-Day Path", 5), (1, "Going Back Safely", 6), (1, "Five Small Pieces", 7)]
    for s in STAGES:
        entries.append((1, f"Stage {s[0]} · {s[1]} (Days {s[2]}–{s[3]})", 100 + s[0]))
    entries += [(1, "The Challenge Jar", 60), (1, "A Letter From Her", 61), (1, "A Letter From the New Me", 62), (1, "Our Promise", 63),
                (1, "Final Reflection", 50), (1, "Where I Am Now", 51), (1, "Next-Step Challenge and Closing Prayer", 52),
                (1, "Certificate of Completion", 53), (1, "Help, Right Now", 54)]
    keys = [str(k) for (_, _, k) in entries]
    ahead_items = [(str(s[0]), f"{s[1]} · Days {s[2]}–{s[3]}", s[4]) for s in STAGES]

    def body(pmap):
        toc = lib.toc_html(entries)
        for k in keys:
            toc = toc.replace(f"@@P{k}@@", pmap.get(k, ""))
        def tag(html, h1, k):
            return html.replace(f"<h1>{h1}</h1>", f"<h1>{h1}{mk(k)}</h1>")
        ahead = tag(lib.ahead_page("What’s ahead", "What’s Ahead", ahead_items), "What’s Ahead", 1)
        how = tag(lib.how_to_read(), "How to Read This Book", 2)
        pathp = tag(lib.path_page(), "Your 90-Day Path", 5)
        going = tag(GOING_BACK, "Going Back Safely", 6)
        howday = tag(HOWDAY, "Five Small Pieces", 7)
        parts = []
        for s in STAGES:
            parts.append(stage_divider(s))
            for n in range(s[2], s[3] + 1):
                parts.append(day_page(HOME_DAYS[n - 1]))
        closing = lib.closing_pages("Ninety Days of Coming Home", [f"Stage {s[0]} · {s[1]}" for s in STAGES], "Stage",
            "Choose one practice from these ninety days (the doorway visit, the armor, the comfort box, the promise) and keep it for thirty days. Draw a card from the Challenge Jar whenever it feels flat, and tell one person what you chose.")
        closing = (closing.replace("<h1>Final Reflection</h1>", f"<h1>Final Reflection{mk(50)}</h1>")
                          .replace("<h1>Where I Am Now</h1>", f"<h1>Where I Am Now{mk(51)}</h1>")
                          .replace("<h1>Next-Step Challenge</h1>", f"<h1>Next-Step Challenge{mk(52)}</h1>"))
        cert = lib.certificate("Ninety Days of Coming Home").replace("Certificate of Completion</div>", f"Certificate of Completion{mk(53)}</div>", 1)
        res = lib.resources_page().replace("<h1>Help, Right Now</h1>", f"<h1>Help, Right Now{mk(54)}</h1>")
        return "\n".join([
            lib.cover("Ninety Days<br>of Coming Home", "Return to Her · Meet the New You", "You survived. Now we rebuild.",
                      "A guided, prayerful journey with daily prayers,<br>affirmations, challenges, and tasks"),
            lib.title_page("Ninety Days<br>of Coming Home", "Return to her. Free her. Bring her home.<br>Paired day-for-day with the 90 Days of Freedom Journal and Ninety Days of Standing",
                           "For the little girl at the doorway — and the woman she becomes."),
            lib.copyright_page("Ninety Days of Coming Home — A Guided Daily Journey"),
            toc, ahead, how, pathp, going, howday] + parts + [jar_pages(), letter_pages(), closing, cert, res])

    slug = "ninety-days-of-coming-home"
    html_path = os.path.join(lib.OUT, slug + ".html")
    pdf_path = os.path.join(lib.OUT, slug + ".pdf")
    title = "Ninety Days of Coming Home"
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
